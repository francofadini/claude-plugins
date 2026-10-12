/**
 * annotate.js: drop-in annotation layer for local HTML documents.
 *
 * Usage:
 *   <script src="annotate.js"></script>   (right before </body>)
 *   (or paste this whole file inside a <script>...</script> at the end of <body>)
 *
 * What it does:
 *   - Floating button to enter/leave "annotate mode".
 *   - In annotate mode, the element under the pointer is highlighted.
 *   - Click an element → a popup to write a comment.
 *   - The element gets a numbered pin; click the pin to edit or delete the note.
 *   - "Pause" → stops capturing so the page can be used normally (open details, scroll carousels).
 *   - "Resume" → back to annotating.
 *   - "Finish" → copies every note to the clipboard as markdown, ready to paste in the chat.
 *
 * Context in the output (helps the agent find what each note refers to):
 *   - Screen: the closest [data-screen] value, else the caption title of the closest <figure>,
 *     else the id of the closest .ios-phone.
 *   - Section: the closest [data-section] value, else the <h2> of the closest <section>.
 *   Templates set data-screen on each phone figure, e.g. <figure class="shot" data-screen="S03 Home, empty">.
 */
(function () {
  'use strict';
  if (window.__i2sAnnotate) return; // avoid loading twice
  window.__i2sAnnotate = true;

  // ---------- state ----------
  /** @type {Array<{id:number, selector:string, snippet:string, screen:string, section:string, text:string, el:HTMLElement, pin?:HTMLElement}>} */
  const notes = [];
  let counter = 0;
  let active = false;   // annotate mode on/off
  let paused = false;   // inside annotate mode, capture paused
  let hoverEl = null;

  // ---------- styles ----------
  const style = document.createElement('style');
  style.textContent = `
    .i2s-ann-highlight { outline: 2px dashed #ff3d7f !important; outline-offset: 1px !important; cursor: crosshair !important; background: rgba(255,61,127,.06) !important; }
    .i2s-ann-marked { outline: 2px solid #ff3d7f !important; outline-offset: 1px !important; }
    .i2s-ann-pin {
      position: absolute; z-index: 2147483646; transform: translate(-50%, -50%);
      width: 22px; height: 22px; border-radius: 50%; background: #ff3d7f; color: #fff;
      font: 700 12px/22px -apple-system, system-ui, sans-serif; text-align: center;
      box-shadow: 0 1px 4px rgba(0,0,0,.4); cursor: pointer; user-select: none;
    }
    .i2s-ann-bar {
      position: fixed; bottom: 18px; right: 18px; z-index: 2147483647;
      display: flex; gap: 6px; align-items: center; padding: 8px 10px;
      background: #111; color: #fff; border-radius: 12px;
      font: 13px/1 -apple-system, system-ui, sans-serif; box-shadow: 0 4px 20px rgba(0,0,0,.35);
    }
    .i2s-ann-bar button {
      border: 0; border-radius: 8px; padding: 7px 11px; font: inherit; font-weight: 600;
      cursor: pointer; background: #2a2a2a; color: #fff;
    }
    .i2s-ann-bar button:hover { background: #3a3a3a; }
    .i2s-ann-bar button.primary { background: #ff3d7f; }
    .i2s-ann-bar button.primary:hover { background: #ff5a92; }
    .i2s-ann-bar button.ghost { background: transparent; padding: 7px 8px; }
    .i2s-ann-bar .count { opacity: .6; font-size: 12px; padding: 0 4px; }
    .i2s-ann-pop {
      position: fixed; z-index: 2147483647; left: 50%; top: 8vh; transform: translateX(-50%);
      width: min(520px, calc(100vw - 24px)); max-height: 82vh; overflow-y: auto; box-sizing: border-box;
      background: #fff; color: #111; border-radius: 14px; box-shadow: 0 12px 44px rgba(0,0,0,.4);
      padding: 16px; font: 14px/1.5 -apple-system, system-ui, sans-serif;
    }
    .i2s-ann-pop .ref { font-size: 11px; color: #888; margin-bottom: 6px; word-break: break-word; }
    .i2s-ann-pop textarea {
      width: 100%; box-sizing: border-box; min-height: 120px; resize: vertical;
      border: 1px solid #ddd; border-radius: 8px; padding: 10px; font: inherit; font-size: 16px;
    }
    .i2s-ann-pop .row { display: flex; gap: 6px; margin-top: 8px; justify-content: flex-end; }
    .i2s-ann-pop button { border: 0; border-radius: 8px; padding: 9px 13px; font: inherit; font-weight: 600; cursor: pointer; }
    .i2s-ann-pop .save { background: #ff3d7f; color: #fff; }
    .i2s-ann-pop .del { background: #f1f1f1; color: #c0392b; margin-right: auto; }
    .i2s-ann-pop .cancel { background: #f1f1f1; color: #444; }
    .i2s-ann-toast {
      position: fixed; bottom: 70px; right: 18px; z-index: 2147483647;
      background: #1e8e3e; color: #fff; padding: 10px 14px; border-radius: 10px;
      font: 13px -apple-system, system-ui, sans-serif; box-shadow: 0 4px 20px rgba(0,0,0,.3);
      opacity: 0; transition: opacity .2s;
    }
    .i2s-ann-paused .i2s-ann-highlight { outline: none !important; background: none !important; cursor: auto !important; }
    .i2s-ann-backdrop { position: fixed; inset: 0; z-index: 2147483646; background: rgba(0,0,0,.45); }
  `;
  document.head.appendChild(style);

  // ---------- helpers ----------
  function cssPath(el) {
    if (!(el instanceof Element)) return '';
    if (el.id) return '#' + CSS.escape(el.id);
    const parts = [];
    let node = el;
    while (node && node.nodeType === 1 && node !== document.body && parts.length < 5) {
      let part = node.nodeName.toLowerCase();
      if (node.id) { parts.unshift('#' + CSS.escape(node.id)); break; }
      const cls = (node.className && typeof node.className === 'string')
        ? node.className.trim().split(/\s+/).filter(c => !c.startsWith('i2s-ann')).slice(0, 2)
        : [];
      if (cls.length) part += '.' + cls.map(CSS.escape).join('.');
      const parent = node.parentNode;
      if (parent) {
        const sameTag = Array.from(parent.children).filter(c => c.nodeName === node.nodeName);
        if (sameTag.length > 1) part += `:nth-of-type(${sameTag.indexOf(node) + 1})`;
      }
      parts.unshift(part);
      node = node.parentNode;
    }
    return parts.join(' > ');
  }

  function clean(t) { return (t || '').trim().replace(/\s+/g, ' '); }

  function snippetOf(el) {
    const t = clean(el.innerText || el.textContent);
    if (t) return '“' + t.slice(0, 60) + (t.length > 60 ? '…' : '') + '”';
    return '<' + el.nodeName.toLowerCase() + '>';
  }

  function screenOf(el) {
    const tagged = el.closest('[data-screen]');
    if (tagged) return tagged.getAttribute('data-screen');
    const fig = el.closest('figure');
    if (fig) {
      const cap = fig.querySelector('figcaption b, figcaption strong, figcaption');
      if (cap && clean(cap.textContent)) return clean(cap.textContent).slice(0, 80);
    }
    const phone = el.closest('.ios-phone');
    if (phone && phone.id) return '#' + phone.id;
    return '';
  }

  function sectionOf(el) {
    const tagged = el.closest('[data-section]');
    if (tagged) return tagged.getAttribute('data-section');
    let sec = el.closest('section');
    while (sec) {
      const h = sec.querySelector(':scope > h2, :scope > header h2, :scope > .head h2, :scope h2');
      if (h && clean(h.textContent)) return clean(h.textContent).slice(0, 80);
      sec = sec.parentElement && sec.parentElement.closest('section');
    }
    return '';
  }

  // ---------- pins ----------
  function placePin(note) {
    const r = note.el.getBoundingClientRect();
    let pin = note.pin;
    if (!pin) {
      pin = document.createElement('div');
      pin.className = 'i2s-ann-pin';
      pin.textContent = note.id;
      pin.title = 'Edit note #' + note.id;
      pin.addEventListener('click', (e) => { e.stopPropagation(); openPopup(note.el, note); });
      document.body.appendChild(pin);
      note.pin = pin;
    }
    pin.style.left = (window.scrollX + r.left + r.width - 4) + 'px';
    pin.style.top = (window.scrollY + r.top + 4) + 'px';
  }

  function repositionPins() { notes.forEach(placePin); }
  window.addEventListener('scroll', repositionPins, true);
  window.addEventListener('resize', repositionPins);
  document.addEventListener('toggle', repositionPins, true); // <details> opening moves things

  // ---------- popup ----------
  let pop = null;
  let backdrop = null;
  function closePopup() {
    if (pop) { pop.remove(); pop = null; }
    if (backdrop) { backdrop.remove(); backdrop = null; }
    document.body.style.overflow = '';
  }

  function openPopup(el, existing) {
    closePopup();
    pop = document.createElement('div');
    pop.className = 'i2s-ann-pop';
    pop.innerHTML = `
      <div class="ref"></div>
      <textarea placeholder="Write your comment…"></textarea>
      <div class="row">
        ${existing ? '<button class="del">Delete</button>' : ''}
        <button class="cancel">Cancel</button>
        <button class="save">Save</button>
      </div>`;
    const where = [screenOf(el), snippetOf(el)].filter(Boolean).join(' · ');
    pop.querySelector('.ref').textContent = (existing ? '#' + existing.id + ' · ' : '') + where;
    const ta = pop.querySelector('textarea');
    ta.value = existing ? existing.text : '';

    // always a centered modal with a blocking backdrop (independent of scroll and element position)
    backdrop = document.createElement('div');
    backdrop.className = 'i2s-ann-backdrop';
    backdrop.addEventListener('click', closePopup);
    document.body.appendChild(backdrop);
    document.body.style.overflow = 'hidden';
    document.body.appendChild(pop);
    setTimeout(() => ta.focus(), 50);

    pop.querySelector('.cancel').onclick = closePopup;
    pop.querySelector('.save').onclick = () => {
      const text = ta.value.trim();
      if (!text) { closePopup(); return; }
      if (existing) {
        existing.text = text;
      } else {
        counter++;
        const note = {
          id: counter, selector: cssPath(el), snippet: snippetOf(el),
          screen: screenOf(el), section: sectionOf(el), text, el
        };
        notes.push(note);
        el.classList.add('i2s-ann-marked');
        placePin(note);
      }
      closePopup();
      updateBar();
    };
    if (existing) {
      pop.querySelector('.del').onclick = () => {
        existing.el.classList.remove('i2s-ann-marked');
        if (existing.pin) existing.pin.remove();
        notes.splice(notes.indexOf(existing), 1);
        closePopup();
        updateBar();
      };
    }
    ta.addEventListener('keydown', (e) => {
      if ((e.metaKey || e.ctrlKey) && e.key === 'Enter') pop.querySelector('.save').click();
      if (e.key === 'Escape') closePopup();
    });
  }

  // ---------- pointer capture ----------
  function isOurs(el) {
    return el.closest('.i2s-ann-bar, .i2s-ann-pop, .i2s-ann-pin, .i2s-ann-backdrop');
  }

  function onOver(e) {
    if (!active || paused) return;
    const el = e.target;
    if (isOurs(el)) return;
    if (hoverEl && hoverEl !== el) hoverEl.classList.remove('i2s-ann-highlight');
    hoverEl = el;
    el.classList.add('i2s-ann-highlight');
  }
  function onOut(e) {
    if (e.target.classList) e.target.classList.remove('i2s-ann-highlight');
  }
  function onClick(e) {
    if (!active || paused) return;
    if (isOurs(e.target)) return;
    e.preventDefault();
    e.stopPropagation();
    if (hoverEl) hoverEl.classList.remove('i2s-ann-highlight');
    openPopup(e.target);
  }

  document.addEventListener('mouseover', onOver, true);
  document.addEventListener('mouseout', onOut, true);
  document.addEventListener('click', onClick, true);

  // ---------- toolbar ----------
  const bar = document.createElement('div');
  bar.className = 'i2s-ann-bar';
  document.body.appendChild(bar);

  function toast(msg) {
    const t = document.createElement('div');
    t.className = 'i2s-ann-toast';
    t.textContent = msg;
    document.body.appendChild(t);
    requestAnimationFrame(() => { t.style.opacity = '1'; });
    setTimeout(() => { t.style.opacity = '0'; setTimeout(() => t.remove(), 250); }, 1800);
  }

  function buildOutput() {
    const lines = [`# Annotations — ${document.title || location.pathname}`, `URL: ${location.href}`, ''];
    notes.sort((a, b) => a.id - b.id).forEach(n => {
      lines.push(`## #${n.id} — ${n.snippet}`);
      if (n.section) lines.push(`Section: ${n.section}`);
      if (n.screen) lines.push(`Screen: ${n.screen}`);
      lines.push(`Selector: \`${n.selector}\``);
      lines.push('');
      lines.push(n.text);
      lines.push('');
    });
    return lines.join('\n');
  }

  async function finish() {
    if (!notes.length) { toast('No annotations yet'); return; }
    const out = buildOutput();
    try {
      await navigator.clipboard.writeText(out);
      toast(`✓ ${notes.length} annotation(s) copied. Paste them in the chat.`);
    } catch (_) {
      // execCommand fallback (pages served over plain http, older browsers)
      const ta = document.createElement('textarea');
      ta.value = out; document.body.appendChild(ta); ta.select();
      try { document.execCommand('copy'); toast(`✓ ${notes.length} copied. Paste them in the chat.`); }
      catch (e) { console.log(out); toast('Could not copy: see the console'); }
      ta.remove();
    }
  }

  function setActive(on) {
    active = on;
    paused = false;
    document.body.classList.toggle('i2s-ann-paused', false);
    if (!on && hoverEl) hoverEl.classList.remove('i2s-ann-highlight');
    if (!on) closePopup();
    updateBar();
  }

  function togglePause() {
    paused = !paused;
    document.body.classList.toggle('i2s-ann-paused', paused);
    if (paused && hoverEl) hoverEl.classList.remove('i2s-ann-highlight');
    updateBar();
  }

  function updateBar() {
    if (!active) {
      bar.innerHTML = `<button class="primary" data-act="start">✏️ Annotate</button>`;
    } else {
      bar.innerHTML = `
        <span class="count">${notes.length} note(s)</span>
        <button data-act="pause">${paused ? '▶︎ Resume' : '⏸ Pause'}</button>
        <button class="primary" data-act="finish">✓ Finish</button>
        <button class="ghost" data-act="exit" title="Leave without copying">✕</button>`;
    }
    bar.querySelectorAll('button').forEach(b => {
      b.onclick = () => {
        const act = b.dataset.act;
        if (act === 'start') setActive(true);
        else if (act === 'pause') togglePause();
        else if (act === 'finish') finish();
        else if (act === 'exit') setActive(false);
      };
    });
  }

  updateBar();
  console.log('%c[annotate] ready: "Annotate" button at the bottom right', 'color:#ff3d7f;font-weight:bold');
})();
