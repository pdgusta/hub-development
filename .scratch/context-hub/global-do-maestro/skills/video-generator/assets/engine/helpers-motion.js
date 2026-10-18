/* ============================================================================
   Video 2 helpers (dark motion-graphics style). Added to window.H.
   All HTML helpers place elements inside `stage` (1600 x 900 units).
   ========================================================================== */
(function (H) {
  /* section label, mono small caps, top-left. Returns the element (starts hidden: opacity 0) */
  H.label = (stage, text, o = {}) => {
    const e = H.el('div', { class: 'word label', text }, stage);
    gsap.set(e, { x: o.x ?? 80, y: o.y ?? 64, xPercent: 0, yPercent: -50, opacity: 0 });
    return e;
  };
  /* punchline at the bottom: white part + colored end. Returns {el, parts:[a,b]} hidden */
  H.punch = (stage, white, colored, o = {}) => {
    const e = H.el('div', { class: 'word body' }, stage);
    const a = H.el('span', { text: white }, e);
    const b = H.el('span', { text: colored, class: o.cls || 'green' }, e);
    b.style.color = `var(--${o.color || 'accent'})`;
    gsap.set(e, { x: o.x ?? 800, y: Math.min(o.y ?? 712, 712), xPercent: -50, yPercent: -50, fontSize: (o.size || 44) + 'px', opacity: 0 });
    return e;
  };
  /* reveal punchline (fade + rise) */
  H.punchIn = (tl, el, pos) => { tl.fromTo(el, { opacity: 0, y: '+=18' }, { opacity: 1, y: '-=18', duration: 0.6, ease: 'power3.out' }, pos); return tl; };

  /* pill chip. cls: accent|green|blue|amber|warn|violet|orange (border+text color). hidden */
  H.pill = (stage, text, o = {}) => {
    const e = H.el('div', { class: 'pill ' + (o.cls || ''), text }, stage);
    if (o.mono) e.style.fontFamily = 'var(--font-mono)';
    gsap.set(e, { x: o.x ?? 800, y: o.y ?? 450, xPercent: -50, yPercent: -50, fontSize: (o.size || 22) + 'px', opacity: 0, scale: 0.9 });
    return e;
  };
  /* tilted stamp (verdict). cls: '' (green) | warn | amber. hidden */
  H.stamp = (stage, text, o = {}) => {
    const e = H.el('div', { class: 'stamp ' + (o.cls || ''), text }, stage);
    gsap.set(e, { x: o.x ?? 800, y: o.y ?? 450, xPercent: -50, yPercent: -50, rotation: o.rot ?? -8, fontSize: (o.size || 34) + 'px', opacity: 0, scale: 1.6 });
    return e;
  };
  /* slam a stamp in (scale down + opacity), with a tiny shake */
  H.slam = (tl, el, pos) => { tl.to(el, { opacity: 1, scale: 1, duration: 0.18, ease: 'power4.in' }, pos); tl.to(el, { x: '+=4', duration: 0.04, yoyo: true, repeat: 3 }, pos + 0.18); return tl; };

  /* big mono number that counts. Returns {el, set(v), tween(tl, to, pos, dur)}; format(v) -> string */
  H.counter = (stage, o = {}) => {
    const fmt = o.format || (v => Math.round(v).toString());
    const e = H.el('div', { class: 'word mono ' + (o.cls || ''), text: fmt(o.from ?? 0) }, stage);
    gsap.set(e, { x: o.x ?? 800, y: o.y ?? 450, xPercent: -50, yPercent: -50, fontSize: (o.size || 120) + 'px', opacity: o.opacity ?? 0 });
    const obj = { v: o.from ?? 0 };
    return {
      el: e,
      set(v) { obj.v = v; e.textContent = fmt(v); },
      tween(tl, to, pos, dur = 1.2, ease = 'power2.out') { tl.to(obj, { v: to, duration: dur, ease, onUpdate: () => { e.textContent = fmt(obj.v); } }, pos); return tl; }
    };
  };

  /* terminal window mockup (HTML). lines: array of strings or {t:'text', c:'p|k|o|w|r'} tokens arrays.
     Returns {el, body, typeLine(tl, line, pos, dur)}. hidden */
  H.terminal = (stage, o = {}) => {
    const e = H.el('div', { class: 'term' }, stage);
    const bar = H.el('div', { class: 'bar' }, e); for (let i = 0; i < 3; i++) H.el('i', {}, bar);
    if (o.title) { const t = H.el('span', { text: o.title }, bar); Object.assign(t.style, { marginLeft: '10px', fontSize: '16px', color: 'var(--ink-dim)', fontFamily: 'var(--font-mono)' }); }
    const body = H.el('div', { class: 'body' }, e);
    Object.assign(e.style, { left: (o.x ?? 200) + 'px', top: (o.y ?? 200) + 'px', width: (o.w ?? 700) + 'px', height: (o.h ?? 320) + 'px', fontSize: (o.font || 22) + 'px' });
    gsap.set(e, { opacity: 0 });
    const line = (spec) => {
      const row = H.el('div', {}, body);
      const toks = typeof spec === 'string' ? [{ t: spec }] : spec;
      toks.forEach(k => H.el('span', { class: k.c || '', text: k.t }, row));
      return row;
    };
    (o.lines || []).forEach(line);
    /* typeLine: adds a row and reveals its characters over dur seconds */
    const typeLine = (tl, spec, pos, dur = 0.8) => {
      const row = line(spec); const spans = [...row.querySelectorAll('span')];
      const chars = []; spans.forEach(s => { const txt = s.textContent; s.textContent = ''; [...txt].forEach(c => { const ch = H.el('span', { text: c }, s); chars.push(ch); }); });
      gsap.set(row, { opacity: 0 }); gsap.set(chars, { opacity: 0 });
      tl.set(row, { opacity: 1 }, pos);
      tl.to(chars, { opacity: 1, duration: 0.01, stagger: dur / Math.max(1, chars.length), ease: 'none' }, pos);
      return row;
    };
    return { el: e, body, line, typeLine };
  };

  /* agent character (blob head with a green antenna), SVG group in a canvas. mood: 'happy'|'neutral'|'doubt'|'angry'|'dizzy'. size ~ 100 units box. hidden strokes if o.hidden */
  H.agent = (parent, o = {}) => {
    const { x = 0, y = 0, size = 120, mood = 'happy', cls = '' } = o;
    const g = H.sv('g', { class: 'agent icon ' + cls, transform: `translate(${x} ${y}) scale(${size / 100})`, fill: 'none', stroke: 'currentColor', 'stroke-width': 3.2, 'stroke-linecap': 'round', 'stroke-linejoin': 'round' }, parent);
    // head (slightly irregular rounded blob)
    H.sv('path', { d: 'M22 58 C20 30 36 18 52 19 C70 20 82 34 80 58 C79 78 66 88 50 88 C34 88 23 77 22 58 Z', pathLength: 1 }, g);
    // antenna + tip (green)
    const ant = H.sv('g', { class: 'c-green' }, g);
    H.sv('path', { d: 'M50 19 L50 6', pathLength: 1 }, ant);
    H.sv('path', { d: 'M46 5 A4 4 0 1 0 54 5 A4 4 0 1 0 46 5', pathLength: 1, fill: 'currentColor' }, ant);
    // eyes
    const eyes = H.sv('g', { class: 'eyes' }, g);
    const mouth = H.sv('g', { class: 'mouth' }, g);
    const set = (m) => {
      eyes.innerHTML = ''; mouth.innerHTML = '';
      const P = (d, extra = {}) => H.sv('path', Object.assign({ d, pathLength: 1 }, extra), eyes);
      const M = (d, extra = {}) => H.sv('path', Object.assign({ d, pathLength: 1 }, extra), mouth);
      if (m === 'dizzy') { P('M34 46 a5 5 0 1 1 5 5 a2.5 2.5 0 1 1 -2.5 -2.5'); P('M60 46 a5 5 0 1 1 5 5 a2.5 2.5 0 1 1 -2.5 -2.5'); M('M40 70 Q50 64 60 70'); }
      else if (m === 'doubt') { P('M36 48 a3 3 0 1 0 6 0 a3 3 0 1 0 -6 0', { fill: 'currentColor' }); P('M58 48 a3 3 0 1 0 6 0 a3 3 0 1 0 -6 0', { fill: 'currentColor' }); P('M56 36 L68 40'); M('M42 70 L58 70'); }
      else if (m === 'angry') { P('M34 40 L44 46'); P('M66 40 L56 46'); P('M37 52 a3 3 0 1 0 6 0 a3 3 0 1 0 -6 0', { fill: 'currentColor' }); P('M57 52 a3 3 0 1 0 6 0 a3 3 0 1 0 -6 0', { fill: 'currentColor' }); M('M40 72 Q50 64 60 72'); }
      else if (m === 'neutral') { P('M36 48 a3 3 0 1 0 6 0 a3 3 0 1 0 -6 0', { fill: 'currentColor' }); P('M58 48 a3 3 0 1 0 6 0 a3 3 0 1 0 -6 0', { fill: 'currentColor' }); M('M42 70 L58 70'); }
      else { P('M36 48 a3 3 0 1 0 6 0 a3 3 0 1 0 -6 0', { fill: 'currentColor' }); P('M58 48 a3 3 0 1 0 6 0 a3 3 0 1 0 -6 0', { fill: 'currentColor' }); M('M40 66 Q50 76 60 66'); }
    };
    set(mood);
    g.setMood = set;
    if (o.hidden) H.prep(g);
    return g;
  };
  /* stick-figure human with a laptop (optional). SVG group, 100-unit box. */
  H.human = (parent, o = {}) => {
    const { x = 0, y = 0, size = 120, cls = '', laptop = false } = o;
    const g = H.sv('g', { class: 'human icon ' + cls, transform: `translate(${x} ${y}) scale(${size / 100})`, fill: 'none', stroke: 'currentColor', 'stroke-width': 3.2, 'stroke-linecap': 'round', 'stroke-linejoin': 'round' }, parent);
    H.sv('path', { d: 'M50 12 a10 10 0 1 0 0.1 0', pathLength: 1 }, g);          // head
    H.sv('path', { d: 'M50 32 L50 64', pathLength: 1 }, g);                         // body
    H.sv('path', { d: 'M50 40 L30 56 M50 40 L70 56', pathLength: 1 }, g);          // arms
    H.sv('path', { d: 'M50 64 L36 92 M50 64 L64 92', pathLength: 1 }, g);          // legs
    if (laptop) H.sv('path', { d: 'M24 56 L46 56 L46 72 L20 72 Z M18 74 L48 74', pathLength: 1 }, g);
    if (o.hidden) H.prep(g);
    return g;
  };
  /* a thin, straight connector line (SVG) with optional arrowhead, in a canvas. */
  H.link = (parent, x1, y1, x2, y2, o = {}) => {
    const g = H.sv('g', { class: 'ink ' + (o.cls || 'c-dim') }, parent);
    const p = H.sv('path', { d: `M${x1} ${y1} L${x2} ${y2}`, 'stroke-width': o.sw || 2, pathLength: 1, fill: 'none' }, g);
    if (o.dash) p.style.strokeDasharray = o.dash;
    if (o.arrow) { const a = Math.atan2(y2 - y1, x2 - x1), hl = o.head || 12; H.sv('path', { d: `M${x2 + Math.cos(a + 2.6) * hl} ${y2 + Math.sin(a + 2.6) * hl} L${x2} ${y2} L${x2 + Math.cos(a - 2.6) * hl} ${y2 + Math.sin(a - 2.6) * hl}`, 'stroke-width': o.sw || 2, pathLength: 1, fill: 'none' }, g); }
    return g;
  };
  /* a cut to black between sections: fades everything in the stage out over 0.25 s at pos (used rarely; the player already fades scenes) */
  H.blackout = (tl, stage, pos, dur = 0.25) => { tl.to(stage.children, { opacity: 0, duration: dur, ease: 'power1.in' }, pos); return tl; };
})(window.H);
