#!/usr/bin/env python3
"""Automatic checks for an idea2spec shape HTML (sketch phones + document text).

Usage:
  python3 audit.py path/to/shape.html [--forbidden spec/forbidden-copy.txt]
                   [--lang auto|es|en|...] [--register tu|vos|usted|none]
                   [--phone "figure.shot, figure.fig, [data-phone]"] [--frame ".ios-phone, .frame"]
                   [--shots DIR] [--json] [--skip check1,check2] [--max-min 10]

Conventions the checks rely on (the build skill should follow them):
  - Each phone is a `figure.shot` (templates/shape.html; also `figure.fig` or `[data-phone]`)
    with an `id`; its screen is the `.ios-phone` (or `.frame`) inside it, else the element itself.
    The `figcaption` is document text, not screen text.
  - Sheets: an element whose class token ends in "sheet" (t-sheet, bottomsheet...),
    or `[data-role=sheet]`, or `[role=dialog]`. Scrim: token ending in "-dim"/"scrim"
    or `[data-role=scrim]`.
  - Primary action: `[data-role=primary]`, or any button-sized element (32-72 pt tall,
    >= 50% of the frame width) with an opaque, saturated background.
  - Anything inside `[data-audit-ignore]` (system keyboard, home screen) is skipped.

Forbidden-copy file (optional; default: spec/forbidden-copy.txt next to the HTML,
in its parent, or in the cwd). One entry per line, `#` for comments:
  term                      -> case-insensitive literal, matched on word boundaries
  term => replacement       -> same, with the suggested replacement in the report
  re:regex => replacement   -> raw regex
  ! term                    -> also checked in document text (not only screens)

Severity: B blocking · I important · M minor. Exit code 1 if there is any B.
Requires: pip install playwright && playwright install chromium
"""
import argparse, json, os, re, sys, unicodedata
from collections import Counter, defaultdict

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    sys.exit("Missing Playwright: pip install playwright && playwright install chromium")

# ---------------------------------------------------------------- generic copy rules
# Voice rules that apply to any app (Apple-style voice, never blame, no hype).
# Disable with --skip base-copy. Project-specific terms go in forbidden-copy.txt.
BASE_COPY = {
    "es": [
        (r"\boops\b", "say what happened and what to do"),
        (r"\bincorrect[oa]s?\b", "never blame the person"),
        (r"\bte equivocaste\b|\bte perdiste\b|\bhiciste mal\b", "never blame the person"),
        (r"\b(ok|aceptar)\b", "verb + object ('Guardar cambios')"),
        (r"\bperfect[oa]\b|\bm[aá]gic[oa]\b|\bincre[ií]ble\b|\binteligente\b|\bcon ia\b|\brevolucionari[oa]\b",
         "no hype: show what it does"),
        (r"[¡!]", "no exclamation marks"),
        (r"\bpor favor\b", "no pleading in UI copy"),
    ],
    "en": [
        (r"\boops\b|\bwhoops\b", "say what happened and what to do"),
        (r"\byou (made a mistake|got lost|failed)\b|\binvalid\b|\billegal\b", "never blame the person"),
        (r"^(ok|okay)$", "verb + object ('Save changes')"),
        (r"\bperfect\b|\bmagic(al)?\b|\bamazing\b|\bsmart\b|\bai-powered\b|\bwith ai\b|\brevolutionary\b",
         "no hype: show what it does"),
        (r"!", "no exclamation marks"),
    ],
}
EMOJI = re.compile("[\U0001F300-\U0001FAFF\U00002600-\U000027BF\U0001F000-\U0001F2FF\U0001F900-\U0001F9FF]")

# Spanish register: voseo + Rioplatense slang when the project uses "tú".
VOS_STOP = set("""más además jamás atrás detrás después inglés francés país demás quizás estás está aquí allí ahí sí
café también según través japonés sofás menú bebé mamá papá ojalá así allá mamás papás cafés
interés compás anís maní sofá qué fe té puré rubí colibrí jabalí bambú""".split())
VOS_EXPLICIT = re.compile(r"^(vos|sos|acá|che|dale|tranqui|laburo|bondi|birra|valijas?|pegal[ao]s?|tocal[ao]s?|tra[eé]l[ao]s?|sugerime|armame|proponeme|decinos|bajate|fijate|mandal[ao]|avisame|contame|decime|mirala|elegila|dejala|probala)$")
DOC_TECH = re.compile(r"\b(API|SDK|SwiftUI|UIKit|React Native|Expo|JSON|endpoint|backend|frontend|schema|props?|hooks?|CSS|HTML|z-index|webhook|OAuth|SQL)\b|\b\d+\s?(px|pt)\b")


def load_forbidden(path):
    rules = []
    if not path or not os.path.exists(path):
        return rules
    for raw in open(path, encoding="utf-8"):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        doc = line.startswith("!")
        if doc:
            line = line[1:].strip()
        term, _, repl = line.partition("=>")
        term, repl = term.strip(), repl.strip()
        if term.startswith("re:"):
            pat = term[3:].strip()
        else:
            pat = r"(?<!\w)" + re.escape(term) + r"(?!\w)"
        try:
            rules.append((re.compile(pat, re.I | re.M), term, repl, doc))
        except re.error as e:
            print(f"[warn] bad regex in {path}: {term} ({e})", file=sys.stderr)
    return rules


def find_forbidden_file(html, explicit):
    if explicit:
        return explicit
    d = os.path.dirname(os.path.abspath(html))
    for c in (os.path.join(d, "spec", "forbidden-copy.txt"),
              os.path.join(os.path.dirname(d), "spec", "forbidden-copy.txt"),
              os.path.join(os.getcwd(), "spec", "forbidden-copy.txt")):
        if os.path.exists(c):
            return c
    return None


def detect_lang(text):
    words = re.findall(r"[a-záéíóúñ]+", text.lower())
    es = sum(w in {"el", "la", "de", "que", "tu", "con", "para", "los", "las", "una", "del", "por"} for w in words)
    en = sum(w in {"the", "your", "and", "to", "of", "with", "for", "you", "this", "is", "on"} for w in words)
    return "es" if es >= en else "en"


def voseo(text):
    found = set()
    for m in re.finditer(r"\b([a-zñáéíóú]+)\b", text.lower()):
        w = m.group(1)
        if w in VOS_STOP:
            continue
        if VOS_EXPLICIT.match(w):
            found.add(w)
        elif re.search(r"[^aeiouáéíóú](ás|és|ís)$", w) and not re.search(r"(rás|rés|rís)$", w):
            found.add(w)  # present voseo (llegás); excludes tú future (verás)
        elif re.search(r"^[a-zñ]{2,}[áéí]$", w) and not re.search(r"(rá|ré|rí)$", w) and w not in {"pasé", "llegué", "bajé", "salí", "comí", "viví", "elegí", "perdí"}:
            found.add(w)  # imperative voseo (tocá); excludes 1st-person preterite
    return sorted(found)


# ---------------------------------------------------------------- in-page probes
JS_PHONES = r"""
([phoneSel, frameSel]) => {
  const vis = el => { const r = el.getBoundingClientRect(); const s = getComputedStyle(el);
    return r.width > 2 && r.height > 2 && s.display !== 'none' && s.visibility !== 'hidden' && parseFloat(s.opacity) > 0.05; };
  const ignored = el => !!el.closest('[data-audit-ignore]') || [...(el.closest('[class*=kbd],[class*=keyboard]')?.classList || [])].some(t => /(^|-)(kbd|keyboard)$/i.test(t));
  const rgba = c => { const m = c.match(/rgba?\(([^)]+)\)/); if (!m) return null;
    const p = m[1].split(/[ ,/]+/).filter(Boolean).map(Number); return {r:p[0],g:p[1],b:p[2],a:p.length>3?p[3]:1}; };
  const hsl = c => { const r=c.r/255,g=c.g/255,b=c.b/255, mx=Math.max(r,g,b), mn=Math.min(r,g,b), l=(mx+mn)/2;
    const s = mx===mn ? 0 : (l>0.5 ? (mx-mn)/(2-mx-mn) : (mx-mn)/(mx+mn)); return {s,l}; };
  const lum = c => { const f = v => { v/=255; return v<=0.03928 ? v/12.92 : Math.pow((v+0.055)/1.055,2.4); };
    return 0.2126*f(c.r)+0.7152*f(c.g)+0.0722*f(c.b); };
  const tokEnds = (el, re) => [...el.classList].some(t => re.test(t));
  const out = [];
  [...document.querySelectorAll(phoneSel)].filter(el => !el.parentElement.closest(phoneSel)).forEach((ph, i) => {
    const frame = ph.querySelector(frameSel) || ph;
    const fr = frame.getBoundingClientRect(); const sc = fr.width / 390 || 1;
    const cap = ph.querySelector('figcaption');
    const rec = { id: ph.id || ('phone-' + (i+1)), caption: cap ? cap.innerText.replace(/\s+/g,' ').trim().slice(0,70) : '',
      text: '', nodes: [], sheets: [], scrims: 0, primaries: [], wideGray: [], tabs: null, chipX: [], backAndClose: false,
      lowContrast: [], caps: [], hidden: [], small: [] };
    const all = [...frame.querySelectorAll('*')].filter(el => !ignored(el));
    // screen text (no figcaption, no ignored)
    const tw = document.createTreeWalker(frame, NodeFilter.SHOW_TEXT);
    let n; const parts = [];
    while ((n = tw.nextNode())) { const p = n.parentElement; if (!p || ignored(p) || p.closest('figcaption,style,script')) continue;
      const t = n.textContent.replace(/\s+/g,' ').trim(); if (!t || !vis(p)) continue; parts.push(t);
      rec.nodes.push(t);
      const tt = getComputedStyle(p).textTransform; const shown = tt === 'uppercase' ? t.toUpperCase() : t;
      if (/[A-ZÁÉÍÓÚÑ]{2,}(\s+[A-ZÁÉÍÓÚÑ]{2,})+/.test(shown) && shown === shown.toUpperCase()) rec.caps.push(shown.slice(0,40));
    }
    rec.text = parts.join(' · ').replace(/(\s·\s)+/g, ' · ');
    // sheets and scrims
    const sheets = all.filter(el => vis(el) && (tokEnds(el, /sheet$/i) || el.matches('[data-role=sheet],[role=dialog]')));
    rec.sheets = sheets.map(el => [...el.classList].join('.') || el.getAttribute('role') || 'sheet');
    rec.scrims = all.filter(el => vis(el) && (tokEnds(el, /(-dim|scrim)$/i) || el.matches('[data-role=scrim]'))).length;
    // primaries and wide gray buttons
    const cands = [];
    for (const el of all) {
      if (!vis(el)) continue; const r = el.getBoundingClientRect(); const s = getComputedStyle(el);
      const explicit = el.matches('[data-role=primary]');
      if (!explicit && !(r.height >= 32*sc && r.height <= 72*sc && r.width >= 0.5*fr.width)) continue;
      if (!el.innerText || !el.innerText.trim()) continue;
      const bg = rgba(s.backgroundColor); if (!explicit && (!bg || bg.a < 0.9)) continue;
      const h = bg ? hsl(bg) : {s:1,l:.5};
      const label = el.innerText.replace(/\s+/g,' ').trim().slice(0,40);
      const box = {x:r.left-fr.left, y:r.top-fr.top, w:r.width, h:r.height};
      if (explicit || (h.s >= 0.25 && h.l > 0.12 && h.l < 0.85)) cands.push({el, label, box});
      else if (r.width >= 0.9*fr.width && h.s < 0.15 && h.l > 0.12 && h.l < 0.97 && /button|btn|cta/i.test(el.tagName + ' ' + el.className + ' ' + (el.getAttribute('role')||'')))
        rec.wideGray.push(label);
    }
    const prim = cands.filter(c => !cands.some(o => o !== c && o.el.contains(c.el)));
    rec.primaries = prim.map(c => c.label);
    // primary clipped or covered
    for (const c of prim) {
      const r = c.el.getBoundingClientRect();
      if (r.bottom > fr.bottom + 1 || r.top < fr.top - 1 || r.right > fr.right + 1 || r.left < fr.left - 1) { rec.hidden.push(c.label + ' (clipped by the frame)'); continue; }
      c.el.scrollIntoView({block:'center', inline:'center'}); const r2 = c.el.getBoundingClientRect();
      const top = document.elementFromPoint(r2.left + r2.width/2, r2.top + r2.height/2);
      if (top && !c.el.contains(top) && !top.contains(c.el)) rec.hidden.push(c.label + ' (covered by ' + (top.className || top.tagName) + ')');
    }
    // tab bar
    const bar = all.find(el => vis(el) && (el.matches('[role=tablist]') || tokEnds(el, /tab-?bar$/i)));
    if (bar) rec.tabs = [...bar.querySelectorAll('[role=tab]')].length || [...bar.querySelectorAll('*')].filter(e => tokEnds(e, /(^|-)tab$/i)).length;
    // chip with an x inside (web pattern)
    for (const el of all) { if (!vis(el)) continue; const r = el.getBoundingClientRect(); const s = getComputedStyle(el);
      const rad = parseFloat(s.borderTopLeftRadius) || 0;
      if (r.height <= 40*sc && r.height >= 20*sc && rad >= r.height/2 - 2 && r.width < 0.6*fr.width &&
          r.width > 1.6*r.height && /[A-Za-zÁ-úñ0-9]/.test(el.innerText||'') &&
          (/[×✕✖]/.test(el.innerText||'') || el.querySelector('use[href*="xmark"],use[href*="close"],use[href$="-x"]'))) rec.chipX.push((el.innerText||'').trim().slice(0,30)); }
    // back and close in the same header (top 14% of the frame)
    const top = all.filter(el => { const r = el.getBoundingClientRect(); return vis(el) && r.top - fr.top < 0.14*fr.height; });
    const ref = el => (el.getAttribute && (el.getAttribute('href') || el.getAttribute('xlink:href') || '')) + ' ' + (el.getAttribute && el.getAttribute('aria-label') || '');
    const hasBack = top.some(el => /chev(ron)?[-_.]?(l|left)\b|chevl|back/i.test(ref(el)) || /^‹$/.test((el.innerText||'').trim()));
    const hasClose = top.some(el => /xmark|close|#t-x\b|-x$/i.test(ref(el)) || /^[✕×]$/.test((el.innerText||'').trim()));
    rec.backAndClose = hasBack && hasClose;
    // contrast: what is really painted under the text (elementsFromPoint); skips text over images, gradients, blur
    frame.scrollIntoView({block:'center', inline:'center'});
    for (const el of all) {
      if (!vis(el) || el instanceof SVGElement || el.closest('[disabled],[aria-disabled=true],.disabled,.dis')) continue;
      const own = [...el.childNodes].some(c => c.nodeType === 3 && c.textContent.trim()); if (!own) continue;
      const r = el.getBoundingClientRect(); const cx = r.left + r.width/2, cy = r.top + r.height/2;
      if (cx < 0 || cy < 0 || cx > innerWidth || cy > innerHeight) continue;
      const s = getComputedStyle(el); const fg = rgba(s.color); if (!fg) continue;
      const stack = document.elementsFromPoint(cx, cy); const k = stack.indexOf(el); if (k < 0) continue;
      let bg = null, unknown = false;
      for (const p of stack.slice(k)) { const ps = getComputedStyle(p);
        if (/^(IMG|CANVAS|VIDEO|IFRAME)$/.test(p.tagName) || (p instanceof SVGElement && p !== el) || ps.backgroundImage !== 'none' ||
            (ps.backdropFilter && ps.backdropFilter !== 'none')) { unknown = true; break; }
        const b = rgba(ps.backgroundColor); if (b && b.a >= 0.95) { bg = b; break; } if (b && b.a > 0.05) { unknown = true; break; } }
      if (unknown || !bg) continue;
      let op = 1; for (let q = el; q && q !== document.documentElement; q = q.parentElement) op *= parseFloat(getComputedStyle(q).opacity);
      const a = fg.a * op; const mix = {r: fg.r*a + bg.r*(1-a), g: fg.g*a + bg.g*(1-a), b: fg.b*a + bg.b*(1-a)};
      const L1 = lum(mix), L2 = lum(bg); const ratio = (Math.max(L1,L2)+0.05)/(Math.min(L1,L2)+0.05);
      const fs = parseFloat(s.fontSize), fw = parseInt(s.fontWeight) || 400;
      const need = (fs >= 24 || (fs >= 18.66 && fw >= 700)) ? 3 : 4.5;
      if (ratio < need) rec.lowContrast.push({t: (el.textContent || '').trim().slice(0,30), ratio: +ratio.toFixed(1), need});
    }
    out.push(rec);
  });
  return out;
}
"""

JS_DOC = r"""
([phoneSel]) => {
  const vis = el => { const s = getComputedStyle(el); return s.display !== 'none' && s.visibility !== 'hidden'; };
  const body = document.body.cloneNode(true);
  body.querySelectorAll(phoneSel + ',script,style,noscript,template,[data-audit-ignore]').forEach(e => e.remove());
  // collapsed content does not count as reading text, but its summary does
  body.querySelectorAll('details').forEach(d => [...d.children].forEach(c => { if (c.tagName !== 'SUMMARY') c.remove(); }));
  const host = document.createElement('div'); host.style.cssText = 'position:absolute;left:-99999px;width:900px';
  host.appendChild(body); document.documentElement.appendChild(host);
  const text = host.innerText; host.remove();
  // all images
  const brokenImgs = [...document.images].filter(i => i.complete && i.naturalWidth === 0).map(i => i.getAttribute('src') || '').slice(0, 20);
  const ids = new Set([...document.querySelectorAll('[id]')].map(e => e.id));
  const brokenUse = [...new Set([...document.querySelectorAll('use')].map(u => u.getAttribute('href') || u.getAttribute('xlink:href') || '')
      .filter(h => h.startsWith('#') && !ids.has(h.slice(1))))].slice(0, 20);
  return { text, brokenImgs, brokenUse, details: document.querySelectorAll('details').length,
           toggles: document.querySelectorAll('[aria-expanded][aria-controls]').length };
}
"""

JS_COLLAPSIBLES = r"""
async () => {
  const bad = []; const vis = el => { const r = el.getBoundingClientRect(); return r.height > 1 && getComputedStyle(el).display !== 'none'; };
  const ds = [...document.querySelectorAll('details')];
  for (const [i, d] of ds.entries()) {
    const s = d.querySelector(':scope > summary'); const label = (s ? s.innerText : 'details #' + i).trim().slice(0, 50);
    if (!s) { bad.push(label + ' (no summary)'); continue; }
    const was = d.open; if (was) { s.click(); await new Promise(r => setTimeout(r, 20)); }
    s.click(); await new Promise(r => setTimeout(r, 30));
    const body = [...d.children].filter(c => c !== s);
    if (!d.open || !body.some(vis) || !body.some(c => (c.innerText || '').trim() || c.querySelector('img,svg,figure'))) bad.push(label);
    if (!was) s.click();
  }
  for (const t of document.querySelectorAll('[aria-expanded][aria-controls]')) {
    const tgt = document.getElementById(t.getAttribute('aria-controls')); const was = t.getAttribute('aria-expanded') === 'true';
    t.click(); await new Promise(r => setTimeout(r, 30));
    const now = t.getAttribute('aria-expanded') === 'true';
    if (!was && (!now || !tgt || !vis(tgt))) bad.push((t.innerText || t.id || 'toggle').trim().slice(0, 50));
    if (now !== was) t.click();
  }
  return bad;
}
"""


# ---------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser(description="idea2spec shape auditor")
    ap.add_argument("html")
    ap.add_argument("--forbidden", help="forbidden-copy file (default: spec/forbidden-copy.txt)")
    ap.add_argument("--lang", default="auto", help="copy language: auto|es|en|... (default auto)")
    ap.add_argument("--register", default="tu", help="Spanish register: tu (default) | vos | usted | none")
    ap.add_argument("--phone", default="figure.shot, figure.fig, [data-phone]")
    ap.add_argument("--frame", default=".ios-phone, .frame")
    ap.add_argument("--shots", help="directory to save one screenshot per phone (for the visual review)")
    ap.add_argument("--skip", default="", help="comma-separated check ids to skip")
    ap.add_argument("--max-min", type=float, default=10, help="max reading time outside phones/collapsibles (min)")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    skip = {s.strip() for s in a.skip.split(",") if s.strip()}
    url = "file://" + os.path.abspath(a.html)
    fpath = find_forbidden_file(a.html, a.forbidden)
    rules = load_forbidden(fpath)
    findings = []  # (sev, check, where, detail)

    def add(sev, check, where, detail):
        if check not in skip:
            findings.append((sev, check, where, detail))

    with sync_playwright() as p:
        br = p.chromium.launch()
        # a3.1 console errors + a3.2 horizontal scroll, at both widths
        for w in (390, 1000):
            pg = br.new_page(viewport={"width": w, "height": 1000})
            errs = []
            pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
            pg.on("pageerror", lambda e: errs.append(str(e)))
            pg.goto(url, wait_until="load")
            pg.wait_for_timeout(300)
            for e in errs[:10]:
                add("B", "console-error", f"@{w}px", e[:160])
            sw = pg.evaluate("document.documentElement.scrollWidth")
            if sw > w + 1:
                add("I", "horizontal-scroll", f"@{w}px", f"scrollWidth {sw} > {w}")
            if w == 1000:
                doc = pg.evaluate(JS_DOC, [a.phone])
                bad = pg.evaluate(JS_COLLAPSIBLES)
                for b in bad:
                    add("I", "collapsible", "document", f"does not open or is empty: {b}")
                phones = pg.evaluate(JS_PHONES, [a.phone, a.frame])
                if a.shots:
                    os.makedirs(a.shots, exist_ok=True)
                    tops = [el for el in pg.query_selector_all(a.phone)
                            if not el.evaluate("(e, sel) => !!e.parentElement.closest(sel)", a.phone)]
                    for i, el in enumerate(tops):
                        fr = el.query_selector(a.frame) or el
                        pid = el.get_attribute("id") or f"phone-{i+1}"
                        try:
                            fr.scroll_into_view_if_needed(timeout=2000)
                            fr.screenshot(path=os.path.join(a.shots, f"{pid}.png"), timeout=5000)
                        except Exception as e:
                            add("M", "screenshot", pid, str(e)[:80])
            pg.close()
        br.close()

    # ---------------- document checks
    dtext = doc["text"]
    lang = a.lang if a.lang != "auto" else detect_lang(" ".join(x["text"] for x in phones) or dtext)
    words = len(re.findall(r"\w+", dtext))
    mins = words / 230
    if mins > a.max_min:
        add("I", "reading-time", "document", f"{words} words ≈ {mins:.1f} min > {a.max_min:g} (move detail into collapsibles)")
    for s in doc["brokenImgs"]:
        add("I", "broken-image", "document", s[:100])
    for s in doc["brokenUse"]:
        add("M", "broken-icon", "document", f"<use href='{s}'> points to a missing id")
    tech = Counter(m.group(0) for m in DOC_TECH.finditer(dtext))
    if tech:
        add("I", "tech-outside-collapsible", "document", "review: " + ", ".join(f"{k}×{v}" for k, v in tech.most_common(8)))
    sents = [re.sub(r"\s+", " ", s).strip().lower() for s in re.split(r"(?<=[.!?:])\s+|\n+", dtext)]
    for s, c in Counter(x for x in sents if len(x.split()) >= 8).items():
        if c > 1:
            add("M", "repeated-sentence", "document", f"×{c}: {s[:90]}")
    for rx, term, repl, docflag in rules:
        if docflag:
            for m in rx.finditer(dtext):
                add("I", "forbidden-copy-doc", "document", f"'{m.group(0)}'" + (f" → {repl}" if repl else ""))
                break

    # ---------------- phone checks
    base = BASE_COPY.get(lang, [])
    for x in phones:
        where = f"{x['id']} | {x['caption'][:40]}"
        t = x["text"]
        nsheets = len(x["sheets"])
        if nsheets > 1:
            add("B", "sheet-over-sheet", where, " + ".join(x["sheets"]))
        elif nsheets == 1 and x["scrims"]:
            add("M", "modal-sheet-review", where, "modal sheet over content: check the base is not a sheet and nothing inside opens another sheet")
        if len(x["primaries"]) > 1:
            add("B", "multiple-primaries", where, " | ".join(x["primaries"]))
        for g in x["wideGray"]:
            add("I", "wide-gray-button", where, f"full-width gray button looks primary-but-disabled: {g}")
        for h in x["hidden"]:
            add("I", "primary-hidden", where, h)
        if x["tabs"] is not None and x["tabs"] > 5:
            add("I", "tab-count", where, f"{x['tabs']} tabs (max 5; a tab bar is for sections, not actions)")
        for c in x["chipX"][:3]:
            add("B", "chip-with-x", where, f"capsule with × inside: '{c}'")
        if x["backAndClose"]:
            add("I", "back-and-close", where, "‹ and ✕ in the same header (one exit per screen)")
        for c in x["lowContrast"][:4]:
            sev = "I" if c["ratio"] < 3 or (c["need"] == 3 and c["ratio"] < 2.5) else "M"
            add(sev, "contrast", where, f"'{c['t']}' {c['ratio']}:1 (needs {c['need']}:1)")
        if len(x["caps"]) > 1:
            add("M", "all-caps", where, " | ".join(x["caps"][:3]))
        for n in x["nodes"]:
            if len(re.findall(r"(?<!·)·(?!·)", n)) > 2:  # separators only; "···" is the More button
                add("I", "too-many-dots", where, n[:80])
        emo = sorted(set(EMOJI.findall(t)) - set("✓✔✕✖✗✘☐☑"))
        if emo:
            add("I", "emoji", where, "".join(emo)[:20])
        if "base-copy" not in skip:
            for pat, why in base:
                for node in x["nodes"]:
                    m = re.search(pat, node, re.I)
                    if m:
                        add("I", "base-copy", where, f"'{m.group(0)}' in '{node[:50]}' → {why}")
                        break
        if lang == "es" and a.register == "tu":
            v = voseo(t)
            if v:
                add("B", "register", where, "voseo/regional (confirm): " + ", ".join(v[:12]))
        hits = []
        for rx, term, repl, _ in rules:
            m = rx.search(t)
            if m:
                hits.append(f"'{m.group(0)}'" + (f" → {repl}" if repl else ""))
        if hits:
            add("B", "forbidden-copy", where, "; ".join(hits[:8]))

    # ---------------- report
    order = {"B": 0, "I": 1, "M": 2}
    findings.sort(key=lambda f: (order[f[0]], f[1], f[2]))
    tot = Counter(f[0] for f in findings)
    meta = {"html": a.html, "phones": len(phones), "lang": lang, "register": a.register,
            "forbidden_file": fpath, "forbidden_rules": len(rules), "reading_min": round(mins, 1),
            "totals": {k: tot.get(k, 0) for k in "BIM"}}
    if a.json:
        print(json.dumps({"meta": meta, "findings": [dict(zip(("sev", "check", "where", "detail"), f)) for f in findings]},
                         ensure_ascii=False, indent=1))
    else:
        print(f"== {a.html}")
        print(f"   phones {len(phones)} · lang {lang} · register {a.register} · forbidden-copy: "
              f"{fpath or 'none'} ({len(rules)} rules) · reading {mins:.1f} min")
        by = defaultdict(list)
        for f in findings:
            by[f[0]].append(f)
        for sev in "BIM":
            if by[sev]:
                print(f"\n[{sev}] {len(by[sev])}")
                for _, ch, wh, de in by[sev]:
                    print(f"  {ch:26} {wh[:55]:55} {de}")
        print(f"\nTOTAL  B {tot.get('B',0)} · I {tot.get('I',0)} · M {tot.get('M',0)}"
              "   (deliver with 0 B and 0 I; voseo/tech/contrast hits are candidates a human confirms)")
    sys.exit(1 if tot.get("B") else 0)


if __name__ == "__main__":
    main()
