#!/usr/bin/env python3
"""shots.py: render an HTML document with Playwright, check it and screenshot every phone.

Checks, at each width (default 1000 and 390 px):
  - console errors, uncaught page errors, failed requests (e.g. a missing annotate.js or ios-kit.css);
  - horizontal page scroll, listing the elements that stick out (intended sideways scrollers are ignored);
  - collapsibles: every <details> opens and shows content; the scroll check is repeated with all of them open.
Then it saves a PNG of every phone so the agent can look at them.

Usage:
  python3 shots.py docs/shape.html
  python3 shots.py docs/annex.html --only ph-f2 --out /tmp/annex-shots
  python3 shots.py http://localhost:4570/shape.html --phone-widths 1000,390 --full

Options:
  --out DIR            where PNGs go. Default: <html folder>/../_shots/<name>/ when the HTML lives in a
                       folder called docs/ (so screenshots are never published with the docs), else
                       <html folder>/_shots/<name>/.
  --selector CSS       what a "phone" is. Default: ".ios-phone, .phone, .frame". When matches are nested,
                       only the outermost one is captured.
  --widths LIST        viewport widths to check. Default: 1000,390.
  --phone-widths LIST  widths at which phones are captured. Default: 1000.
  --only TEXT          capture only phones whose id (or an ancestor's id) or data-screen contains TEXT
                       (comma-separated for several). Useful to look only at what changed.
  --full               also save a full-page screenshot per width.
  --no-details         skip opening <details>.
  --json               print the report as JSON instead of text.

Exit code: 0 when there are no errors and no horizontal scroll; 1 otherwise; 2 on bad usage.
Requires: pip install playwright && python3 -m playwright install chromium
"""
import argparse
import json
import re
import sys
from pathlib import Path

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    sys.exit("Playwright is missing: pip install playwright && python3 -m playwright install chromium")

OVERFLOW_JS = r"""
() => {
  const vw = document.documentElement.clientWidth;
  const sw = Math.max(document.documentElement.scrollWidth, document.body ? document.body.scrollWidth : 0);
  const clipped = (el) => {
    for (let p = el.parentElement; p && p !== document.body; p = p.parentElement) {
      const ox = getComputedStyle(p).overflowX;
      if (ox !== 'visible') return true;   // inside a scroller or a clipping box (e.g. a phone)
    }
    return false;
  };
  const name = (el) => {
    let s = el.tagName.toLowerCase();
    if (el.id) s += '#' + el.id;
    if (typeof el.className === 'string' && el.className.trim())
      s += '.' + el.className.trim().split(/\s+/).slice(0, 2).join('.');
    return s;
  };
  const out = [];
  for (const el of document.body ? document.body.querySelectorAll('*') : []) {
    const cs = getComputedStyle(el);
    if (cs.position === 'fixed' || cs.display === 'none') continue;
    const r = el.getBoundingClientRect();
    if (r.width === 0 || r.right <= vw + 1) continue;
    if (clipped(el)) continue;
    const parent = el.parentElement;
    if (parent && parent !== document.body && parent.getBoundingClientRect().right > vw + 1 && !clipped(parent)) continue;
    out.push({ el: name(el), right: Math.round(r.right) });
    if (out.length >= 8) break;
  }
  return { viewport: vw, scrollWidth: sw, overflow: sw > vw + 1, offenders: out };
}
"""

DETAILS_JS = r"""
() => {
  const ds = Array.from(document.querySelectorAll('details'));
  const bad = [];
  ds.forEach((d, i) => {
    d.open = true;
    const kids = Array.from(d.children).filter(c => c.tagName !== 'SUMMARY');
    const h = kids.reduce((a, c) => a + c.getBoundingClientRect().height, 0);
    if (h < 4) {
      const s = d.querySelector('summary');
      bad.push((s ? s.textContent.trim().slice(0, 60) : 'details #' + (i + 1)));
    }
  });
  return { count: ds.length, empty: bad };
}
"""

PHONES_JS = r"""
(sel) => {
  const all = Array.from(document.querySelectorAll(sel));
  const outer = all.filter(el => !all.some(o => o !== el && o.contains(el)));
  return outer.map((el, i) => {
    let id = el.id, p = el;
    while (!id && p.parentElement) { p = p.parentElement; id = p.id; }
    const tagged = el.closest('[data-screen]');
    el.setAttribute('data-shot-index', String(i));
    return { index: i, id: id || '', screen: tagged ? tagged.getAttribute('data-screen') : '' };
  });
}
"""


def slug(text, limit=60):
    s = re.sub(r"[^A-Za-z0-9._-]+", "-", text).strip("-")
    return s[:limit] or "phone"


def default_out(html: Path) -> Path:
    if html.parent.name == "docs":
        return html.parent.parent / "_shots" / html.stem
    return html.parent / "_shots" / html.stem


def ints(text):
    try:
        return [int(x) for x in text.split(",") if x.strip()]
    except ValueError:
        sys.exit(2)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("html")
    ap.add_argument("--out")
    ap.add_argument("--selector", default=".ios-phone, .phone, .frame")
    ap.add_argument("--widths", default="1000,390")
    ap.add_argument("--phone-widths", default="1000")
    ap.add_argument("--only")
    ap.add_argument("--full", action="store_true")
    ap.add_argument("--no-details", action="store_true")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    if re.match(r"^https?://", a.html):
        url = a.html
        stem = slug(Path(a.html.split("?")[0]).stem or "page")
        out = Path(a.out) if a.out else Path.cwd() / "_shots" / stem
    else:
        html = Path(a.html).resolve()
        if not html.is_file():
            print(f"File not found: {html}", file=sys.stderr)
            sys.exit(2)
        url = html.as_uri()
        out = Path(a.out) if a.out else default_out(html)
    out.mkdir(parents=True, exist_ok=True)
    for old in out.glob("*.png"):
        old.unlink()

    widths = ints(a.widths)
    phone_widths = ints(a.phone_widths)
    only = [x.strip() for x in a.only.split(",")] if a.only else []
    report = {"url": url, "out": str(out), "widths": {}}
    failed = False

    with sync_playwright() as p:
        browser = p.chromium.launch()
        for w in sorted(set(widths + phone_widths), reverse=True):
            page = browser.new_page(viewport={"width": w, "height": 900}, device_scale_factor=2)
            errors = []
            page.on("console", lambda m, e=errors: e.append(f"console.{m.type}: {m.text}") if m.type == "error" else None)
            page.on("pageerror", lambda exc, e=errors: e.append(f"pageerror: {exc}"))
            page.on("requestfailed", lambda r, e=errors: e.append(f"request failed: {r.url} ({r.failure})"))
            page.on("response", lambda r, e=errors: e.append(f"HTTP {r.status}: {r.url}") if r.status >= 400 else None)
            page.goto(url, wait_until="networkidle")
            page.evaluate("document.fonts ? document.fonts.ready : null")
            page.wait_for_timeout(300)

            entry = {"errors": errors}
            if w in widths:
                entry["scroll"] = page.evaluate(OVERFLOW_JS)
                if not a.no_details:
                    entry["details"] = page.evaluate(DETAILS_JS)
                    page.wait_for_timeout(150)
                    entry["scroll_details_open"] = page.evaluate(OVERFLOW_JS)
                    page.evaluate("document.querySelectorAll('details').forEach(d => d.open = false)")
                if a.full:
                    fp = out / f"{w}_full.png"
                    page.screenshot(path=str(fp), full_page=True)
                    entry["full"] = str(fp)

            if w in phone_widths:
                phones = page.evaluate(PHONES_JS, a.selector)
                shots = []
                for ph in phones:
                    label = ph["id"] or ph["screen"] or f"phone-{ph['index']}"
                    if only and not any(o in ph["id"] or o in ph["screen"] for o in only):
                        continue
                    el = page.locator(f'[data-shot-index="{ph["index"]}"]')
                    path = out / f"{w}_{ph['index'] + 1:02d}_{slug(label)}.png"
                    try:
                        el.scroll_into_view_if_needed(timeout=3000)
                        el.screenshot(path=str(path), timeout=10000)
                        shots.append({"file": str(path), "id": ph["id"], "screen": ph["screen"]})
                    except Exception as exc:  # keep going: one broken phone should not hide the rest
                        errors.append(f"screenshot failed for {label}: {exc}")
                entry["phones_found"] = len(phones)
                entry["shots"] = shots

            page.wait_for_timeout(100)
            entry["errors"] = list(dict.fromkeys(errors))
            if entry["errors"]:
                failed = True
            for k in ("scroll", "scroll_details_open"):
                if entry.get(k, {}).get("overflow"):
                    failed = True
            if entry.get("details", {}).get("empty"):
                failed = True
            report["widths"][str(w)] = entry
            page.close()
        browser.close()

    report["ok"] = not failed
    if a.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(f"{url}\nScreenshots: {out}")
        for w, e in report["widths"].items():
            print(f"\n[{w}px]")
            print(f"  errors: {len(e['errors'])}")
            for x in e["errors"][:15]:
                print(f"    - {x}")
            for k, label in (("scroll", "horizontal scroll"), ("scroll_details_open", "horizontal scroll, details open")):
                if k in e:
                    s = e[k]
                    print(f"  {label}: {'YES' if s['overflow'] else 'no'} (scrollWidth {s['scrollWidth']} / viewport {s['viewport']})")
                    for o in s["offenders"] if s["overflow"] else []:
                        print(f"    - {o['el']} ends at {o['right']}px")
            if "details" in e:
                d = e["details"]
                print(f"  collapsibles: {d['count']} opened, {len(d['empty'])} empty")
                for x in d["empty"]:
                    print(f"    - empty: {x}")
            if "shots" in e:
                print(f"  phones: {e['phones_found']} found, {len(e['shots'])} captured")
                for s in e["shots"]:
                    print(f"    - {Path(s['file']).name}" + (f"  [{s['screen']}]" if s["screen"] else ""))
            if "full" in e:
                print(f"  full page: {Path(e['full']).name}")
        print("\nRESULT: " + ("OK" if report["ok"] else "PROBLEMS FOUND"))
    sys.exit(0 if report["ok"] else 1)


if __name__ == "__main__":
    main()
