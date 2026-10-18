/* ============================================================================
   Context Hub explainer — animation engine + player
   Coordinate space: the stage is 1600 x 900 units (CSS px before scaling).
   Scenes register themselves with:  SCENES.push({ id, build(stage, ctx) => gsap.timeline })
   ctx = { dur: <narration seconds>, narration: <string>, style: <string> }
   The timeline returned must be paused (the player controls it) and should
   last about ctx.dur seconds (it may be a little shorter; never much longer).
   ========================================================================== */
window.SCENES = window.SCENES || [];
window.H = (function () {
  const NS = 'http://www.w3.org/2000/svg';
  const W = 1600, HH = 900;
  const H = { W, H: HH, NS };

  /* ---------- element creation ---------- */
  H.el = (tag, attrs = {}, parent) => {
    const e = document.createElement(tag);
    for (const k in attrs) {
      if (k === 'text') e.textContent = attrs[k];
      else if (k === 'html') e.innerHTML = attrs[k];
      else if (k === 'style') Object.assign(e.style, attrs[k]);
      else e.setAttribute(k, attrs[k]);
    }
    if (parent) parent.appendChild(e);
    return e;
  };
  H.sv = (tag, attrs = {}, parent) => {
    const e = document.createElementNS(NS, tag);
    for (const k in attrs) {
      if (k === 'text') e.textContent = attrs[k];
      else e.setAttribute(k, attrs[k]);
    }
    if (parent) parent.appendChild(e);
    return e;
  };
  /* full-stage SVG canvas (viewBox 0 0 1600 900) */
  H.svg = (parent, cls = '') => H.sv('svg', { viewBox: `0 0 ${W} ${HH}`, class: 'canvas ' + cls, width: W, height: HH }, parent);
  /* group helper */
  H.g = (parent, attrs = {}) => H.sv('g', attrs, parent);

  /* ---------- hand-drawn icons (see ICONS keys) ----------
     H.icon(parent, 'robot', {x, y, size, cls, color, sw})
     x,y = top-left of the icon box; size = box size in units (default 100).
     Returns the <g>. Paths are prepared for H.draw (hidden strokes) only if o.hidden === true. */
  H.icon = (parent, name, o = {}) => {
    const { x = 0, y = 0, size = 100, cls = '', color, sw } = o;
    const g = H.sv('g', {
      class: 'icon icon-' + name + ' ' + cls,
      transform: `translate(${x} ${y}) scale(${size / 100})`,
      fill: 'none', stroke: 'currentColor', 'stroke-width': sw || 3,
      'stroke-linecap': 'round', 'stroke-linejoin': 'round'
    }, parent);
    g.innerHTML = window.ICONS[name] || '';
    if (color) g.style.color = color;
    g.querySelectorAll('path').forEach(p => p.setAttribute('pathLength', '1'));
    if (o.hidden) H.prep(g);
    return g;
  };
  H.iconNames = () => Object.keys(window.ICONS || {});

  /* ---------- path utilities ---------- */
  H.paths = (x) => {
    if (!x) return [];
    if (typeof x === 'string') return [...document.querySelectorAll(x)];
    if (Array.isArray(x)) return x.flatMap(H.paths);
    if (x.tagName && x.tagName.toLowerCase() === 'path') return [x];
    if (x.querySelectorAll) return [...x.querySelectorAll('path')];
    return [];
  };
  /* make strokes invisible so they can be "drawn" later */
  H.prep = (target) => {
    const ps = H.paths(target);
    ps.forEach(p => { p.setAttribute('pathLength', '1'); p.style.strokeDasharray = '1 2'; p.style.strokeDashoffset = '1.03'; });
    return ps;
  };
  /* whiteboard: draw strokes one after another over `dur` seconds. pos = timeline position */
  H.draw = (tl, target, dur = 1, pos, o = {}) => {
    const ps = H.prep(target);
    if (!ps.length) return tl;
    const each = dur / ps.length;
    tl.to(ps, { strokeDashoffset: 0, duration: each * (o.overlap || 1.4), stagger: each, ease: o.ease || 'power1.inOut' }, pos);
    return tl;
  };
  /* erase (reverse of draw) */
  H.undraw = (tl, target, dur = 0.6, pos) => {
    const ps = H.paths(target);
    tl.to(ps, { strokeDashoffset: -1.03, duration: dur, ease: 'power1.in' }, pos);
    return tl;
  };
  /* small random wobble on a polyline, for a hand-drawn feel */
  H.wobbly = (pts, amp = 3) => {
    let d = `M${pts[0][0]} ${pts[0][1]}`;
    for (let i = 1; i < pts.length; i++) {
      const [x0, y0] = pts[i - 1], [x1, y1] = pts[i];
      const mx = (x0 + x1) / 2 + (Math.random() - .5) * amp * 2, my = (y0 + y1) / 2 + (Math.random() - .5) * amp * 2;
      d += ` Q${mx} ${my} ${x1} ${y1}`;
    }
    return d;
  };
  /* hand-drawn line through points [[x,y],...]. o: {sw, cls, amp, dash, color} */
  H.line = (parent, pts, o = {}) => {
    const p = H.sv('path', { d: H.wobbly(pts, o.amp ?? 3), class: 'ink ' + (o.cls || ''), 'stroke-width': o.sw || 5, pathLength: 1, fill: 'none' }, parent);
    if (o.dash) p.style.strokeDasharray = o.dash;
    if (o.color) p.style.color = o.color;
    return p;
  };
  /* hand-drawn rectangle (slightly imperfect). returns <path> */
  H.rect = (parent, x, y, w, h, o = {}) => {
    const a = o.amp ?? 2;
    const r = (v) => v + (Math.random() - .5) * a * 2;
    const d = `M${r(x)} ${r(y)} L${r(x + w)} ${r(y)} L${r(x + w)} ${r(y + h)} L${r(x)} ${r(y + h)} Z`;
    const p = H.sv('path', { d, class: 'ink ' + (o.cls || ''), 'stroke-width': o.sw || 5, pathLength: 1, fill: o.fill || 'none' }, parent);
    if (o.color) p.style.color = o.color;
    return p;
  };
  /* hand-drawn circle/ellipse. returns <path> */
  H.circle = (parent, cx, cy, r, o = {}) => {
    const ry = o.ry || r, k = 0.5523, j = (o.amp ?? 2);
    const n = () => (Math.random() - .5) * j * 2;
    const d = `M${cx + r} ${cy} C${cx + r} ${cy + ry * k + n()} ${cx + r * k + n()} ${cy + ry} ${cx} ${cy + ry} C${cx - r * k + n()} ${cy + ry} ${cx - r} ${cy + ry * k + n()} ${cx - r} ${cy} C${cx - r} ${cy - ry * k + n()} ${cx - r * k + n()} ${cy - ry} ${cx} ${cy - ry} C${cx + r * k + n()} ${cy - ry} ${cx + r + n()} ${cy - ry * k} ${cx + r} ${cy}`;
    const p = H.sv('path', { d, class: 'ink ' + (o.cls || ''), 'stroke-width': o.sw || 5, pathLength: 1, fill: o.fill || 'none' }, parent);
    if (o.color) p.style.color = o.color;
    return p;
  };
  /* arrow from (x1,y1) to (x2,y2). o: {bend (px, +/-), sw, head, cls, color, dash}. returns <g> with 2 paths */
  H.arrow = (parent, x1, y1, x2, y2, o = {}) => {
    const g = H.sv('g', { class: 'arrow ink ' + (o.cls || '') }, parent);
    if (o.color) g.style.color = o.color;
    const bend = o.bend || 0;
    const mx = (x1 + x2) / 2, my = (y1 + y2) / 2, dx = x2 - x1, dy = y2 - y1, len = Math.hypot(dx, dy) || 1;
    const nx = -dy / len, ny = dx / len, cx = mx + nx * bend, cy = my + ny * bend;
    const shaft = H.sv('path', { d: `M${x1} ${y1} Q${cx} ${cy} ${x2} ${y2}`, class: 'ink', 'stroke-width': o.sw || 5, pathLength: 1, fill: 'none' }, g);
    if (o.dash) shaft.style.strokeDasharray = o.dash;
    const ang = Math.atan2(y2 - cy, x2 - cx), hl = o.head || 22, a1 = ang + 2.6, a2 = ang - 2.6;
    H.sv('path', { d: `M${x2 + Math.cos(a1) * hl} ${y2 + Math.sin(a1) * hl} L${x2} ${y2} L${x2 + Math.cos(a2) * hl} ${y2 + Math.sin(a2) * hl}`, class: 'ink', 'stroke-width': o.sw || 5, pathLength: 1, fill: 'none' }, g);
    return g;
  };
  /* speech bubble (rounded box + tail) as a drawable <g>. (x,y)=top-left, tail points to (tx,ty) */
  H.bubble = (parent, x, y, w, h, tx, ty, o = {}) => {
    const g = H.sv('g', { class: 'bubble ink ' + (o.cls || '') }, parent);
    const r = 24;
    const d = `M${x + r} ${y} L${x + w - r} ${y} Q${x + w} ${y} ${x + w} ${y + r} L${x + w} ${y + h - r} Q${x + w} ${y + h} ${x + w - r} ${y + h} L${x + r} ${y + h} Q${x} ${y + h} ${x} ${y + h - r} L${x} ${y + r} Q${x} ${y} ${x + r} ${y}`;
    H.sv('path', { d, class: 'ink', 'stroke-width': o.sw || 5, pathLength: 1, fill: o.fill || 'var(--paper)' }, g);
    const bx = x + w * 0.25, by = y + h;
    H.sv('path', { d: `M${bx} ${by} L${tx} ${ty} L${bx + 40} ${by}`, class: 'ink', 'stroke-width': o.sw || 5, pathLength: 1, fill: o.fill || 'var(--paper)' }, g);
    return g;
  };
  /* SVG text (handwritten font by default). o: {x,y,size,cls,anchor,weight}. classes: soft|accent|blue|warn|display */
  H.text = (parent, str, o = {}) => {
    const t = H.sv('text', { x: o.x ?? 0, y: o.y ?? 0, class: 't ' + (o.cls || ''), 'text-anchor': o.anchor || 'middle', 'font-size': o.size || 44, text: str }, parent);
    if (o.weight) t.setAttribute('font-weight', o.weight);
    return t;
  };
  /* highlighter stroke behind text: a thick translucent rect */
  H.highlight = (parent, x, y, w, h) => H.sv('rect', { x, y, width: w, height: h, rx: 6, class: 'hl', pathLength: 1 }, parent);

  /* ---------- kinetic typography (HTML words, centered at x,y) ----------
     H.word(stage, 'ACHAR', {x, y, size, cls})   cls: accent|blue|soft|warn|green|hand
     Returns the element, already centered with xPercent/yPercent (-50). Animate with gsap (x, y, scale, rotation, opacity...). */
  H.word = (stage, str, o = {}) => {
    const e = H.el('div', { class: 'word ' + (o.cls || ''), text: str }, stage);
    gsap.set(e, { x: o.x ?? W / 2, y: o.y ?? HH / 2, xPercent: -50, yPercent: -50, fontSize: (o.size || 120) + 'px', opacity: o.opacity ?? 1 });
    return e;
  };
  /* split a word element into per-character spans (.ch). returns the spans */
  H.chars = (el) => {
    const s = el.textContent; el.textContent = '';
    return [...s].map(c => { const sp = H.el('span', { class: 'ch', text: c === ' ' ? ' ' : c }, el); return sp; });
  };

  /* ---------- 2.5D ----------
     H.layer(stage, {z, cls}) -> absolutely positioned full-stage div, translateZ(z). Put HTML/SVG inside.
     H.card(parent, {x,y,w,h,z,rotX,rotY,cls,html}) -> a paper card in 3D space (top-left at x,y). */
  H.layer = (stage, o = {}) => {
    const e = H.el('div', { class: 'layer ' + (o.cls || '') }, stage);
    gsap.set(e, { z: o.z || 0, rotationX: o.rotX || 0, rotationY: o.rotY || 0, transformOrigin: '50% 50%' });
    return e;
  };
  H.card = (parent, o = {}) => {
    const e = H.el('div', { class: 'card ' + (o.cls || ''), html: o.html || '' }, parent);
    gsap.set(e, { left: o.x ?? 0, top: o.y ?? 0, width: o.w ?? 300, height: o.h ?? 200, z: o.z || 0, rotationX: o.rotX || 0, rotationY: o.rotY || 0, transformOrigin: '50% 50%' });
    return e;
  };
  /* an inline SVG box (own viewBox) for use inside HTML layers/cards. returns the <svg> */
  H.box = (parent, vb = '0 0 100 100', o = {}) => {
    const s = H.sv('svg', { viewBox: vb, class: o.cls || '' }, parent);
    Object.assign(s.style, { position: 'absolute', left: (o.x ?? 0) + 'px', top: (o.y ?? 0) + 'px', width: (o.w ?? 100) + 'px', height: (o.h ?? 100) + 'px', overflow: 'visible' });
    return s;
  };

  /* ---------- stop motion ----------
     Use ease 'steps(n)' so motion jumps frame to frame (n = seconds * H.FPS).
     H.stepTo(tl, targets, vars, pos): like tl.to but with stepped easing at H.FPS.
     H.jitter(tl, targets, {dur, amp, rot, pos}): tiny random nudges each frame = "hand-placed paper" look. */
  H.FPS = 8;
  H.steps = (sec) => `steps(${Math.max(1, Math.round(sec * H.FPS))})`;
  H.stepTo = (tl, targets, vars, pos) => { vars = Object.assign({}, vars); vars.ease = H.steps(vars.duration || 1); tl.to(targets, vars, pos); return tl; };
  H.jitter = (tl, targets, o = {}) => {
    const { dur = 3, amp = 3, rot = 1.5, fps = 4 } = o;
    const sub = gsap.timeline();
    const n = Math.max(1, Math.round(dur * fps));
    for (let i = 0; i < n; i++) {
      sub.to(targets, { x: gsap.utils.random(-amp, amp, 0.5), y: gsap.utils.random(-amp, amp, 0.5), rotation: gsap.utils.random(-rot, rot, 0.1), duration: 1 / fps, ease: 'steps(1)' });
    }
    tl.add(sub, o.pos);
    return sub;
  };
  /* paper cutout shape (filled, with hard shadow). o: {fill: 'var(--cut-1)', rot, r, cls, stroke}. returns <g class="cut"> containing a <rect> */
  H.paper = (parent, x, y, w, h, o = {}) => {
    const g = H.sv('g', { class: 'cut ' + (o.cls || '') }, parent);
    gsap.set(g, { transformOrigin: `${x + w / 2}px ${y + h / 2}px`, rotation: o.rot || 0 });
    H.sv('rect', { x, y, width: w, height: h, rx: o.r ?? 10, fill: o.fill || 'var(--cut-1)', stroke: o.stroke || 'var(--ink)', 'stroke-width': o.sw ?? 3 }, g);
    return g;
  };
  /* torn/cut paper polygon. pts: [[x,y],...] */
  H.poly = (parent, pts, o = {}) => {
    const g = H.sv('g', { class: 'cut ' + (o.cls || '') }, parent);
    H.sv('path', { d: 'M' + pts.map(p => p.join(' ')).join(' L') + ' Z', fill: o.fill || 'var(--cut-2)', stroke: o.stroke || 'var(--ink)', 'stroke-width': o.sw ?? 3, 'stroke-linejoin': 'round' }, g);
    return g;
  };

  /* ---------- common tweens ---------- */
  H.pop = (tl, t, pos, o = {}) => { tl.fromTo(t, { scale: 0, opacity: 0 }, { scale: 1, opacity: 1, duration: o.dur || 0.5, ease: 'back.out(2)', transformOrigin: o.origin || '50% 50%', stagger: o.stagger || 0 }, pos); return tl; };
  H.fade = (tl, t, pos, o = {}) => { tl.fromTo(t, { opacity: 0 }, { opacity: 1, duration: o.dur || 0.5, stagger: o.stagger || 0 }, pos); return tl; };
  H.out = (tl, t, pos, o = {}) => { tl.to(t, { opacity: 0, duration: o.dur || 0.4, scale: o.scale ?? 1, y: o.y ?? 0 }, pos); return tl; };
  H.shake = (tl, t, pos, o = {}) => { tl.to(t, { x: `+=${o.amp || 8}`, duration: 0.05, repeat: o.n || 7, yoyo: true, ease: 'none' }, pos); return tl; };
  /* hide at build time (so the scene starts blank) */
  H.hide = (...els) => { els.flat().forEach(e => gsap.set(e, { opacity: 0 })); return els; };

  return H;
})();

