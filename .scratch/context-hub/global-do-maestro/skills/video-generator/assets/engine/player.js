/* ============================================================================
   Player v2 — one shared <audio>, timers (not the animation ticker) for scene
   flow, fluid leave/enter transitions, pt-BR captions (CUES), export mode.
   ========================================================================== */
window.Player = (function () {
  const P = { scenes: [], i: -1, playing: false, started: false, ended: false, inited: false, resumeTo: null };
  const stage = () => document.getElementById('stage');
  const q = new URLSearchParams(location.search);
  const EXPORT = q.has('export');
  const DEV = q.has('scene') || q.has('t') || EXPORT;
  const FADE_IN = 0.55, FADE_OUT = 0.45, GAP = 0.12, HOLD = 0.3, MAXWAIT = 1.6, LEAD = 2.0, TAIL = 2.5;
  const audio = new Audio(); audio.preload = 'auto';
  let cur = null;

  function fit() {
    if (EXPORT) { stage().style.transform = 'none'; return; }
    const s = Math.min((innerWidth - 32) / 1600, innerHeight / 900);
    stage().style.transform = 'scale(' + s + ')';
  }

  function build() {
    const order = window.ROTEIRO.scenes.slice();
    if (DEV) window.SCENES.forEach(m => { if (!order.some(s => s.id === m.id)) order.push({ id: m.id, title: m.id, style: 'mix', narration: '' }); });
    const bar = document.getElementById('bar');
    const total = order.reduce((a, s) => a + (window.DURATIONS[s.id] || 20), 0);
    order.forEach((meta) => {
      const mod = window.SCENES.find(m => m.id === meta.id);
      const dur = window.DURATIONS[meta.id] || 20;
      const el = H.el('div', { class: 'scene', 'data-id': meta.id }, stage());
      let tl;
      try { tl = mod ? mod.build(el, { dur, narration: meta.narration, section: meta.section || '' }) : null; }
      catch (err) { console.error('scene ' + meta.id + ' failed to build', err); tl = null; }
      if (!tl) { tl = gsap.timeline({ paused: true }); H.text(H.svg(el), meta.title, { x: 800, y: 450, size: 60, cls: 'soft' }); tl.to({}, { duration: dur }); }
      tl.pause(0);
      const seg = H.el('i', {}, bar); seg.style.flex = String(dur / total); const fill = H.el('b', {}, seg);
      P.scenes.push({ meta, el, tl, dur, src: window.AUDIO[meta.id] || '', fill, cues: (window.CUES && window.CUES[meta.id]) || [] });
    });
  }

  /* captions */
  const capEl = () => document.getElementById('cap');
  let capText = null;
  function caption(s, t) {
    let text = '';
    if (s) for (const c of s.cues) { if (t >= c[0] && t < c[1]) { text = c[2]; break; } }
    if (text === capText) return; capText = text;
    const el = capEl(); if (!el) return;
    if (text) { el.textContent = text; el.classList.add('on'); } else { el.classList.remove('on'); }
  }

  function load(s) { if (cur === s) return; cur = s; audio.src = s.src; }
  function play() { const p = audio.play(); if (p && p.catch) p.catch(() => { }); }
  function show(i) {
    P.scenes.forEach((s, k) => { if (k === i) { s.el.classList.remove('leaving'); s.el.classList.add('on'); } else { s.el.classList.remove('on'); if (!s.el.classList.contains('leaving')) s.tl.pause(0); } });
    P.i = i;
  }

  let advancing = false, timers = [];
  const clearTimers = () => { timers.forEach(clearTimeout); timers = []; };
  const later = (fn, ms) => { timers.push(setTimeout(fn, ms)); };

  function startScene(i) {
    clearTimers(); P.resumeTo = null;
    if (i >= P.scenes.length) return finish();
    advancing = false;
    show(i);
    const s = P.scenes[i];
    s.tl.pause(0);
    audio.pause(); load(s);
    try { audio.currentTime = 0; } catch (e) { }
    caption(s, 0);
    if (P.playing) { s.tl.play(); play(); }
  }
  audio.addEventListener('ended', () => endScene(P.i));
  audio.addEventListener('timeupdate', () => {
    const s = P.scenes[P.i]; if (!s || cur !== s) return;
    const t = audio.currentTime, tt = s.tl.time();
    if (Math.abs(t - tt) > 0.3 && t < s.tl.duration()) s.tl.time(t);
    s.fill.style.width = Math.min(100, t / s.dur * 100) + '%';
    caption(s, t);
  });
  /* keep captions in sync while the animation ticker runs (finer than timeupdate) */
  if (window.gsap) gsap.ticker.add(() => { const s = P.scenes[P.i]; if (s && P.playing && cur === s) caption(s, audio.currentTime); });

  function endScene(i) {
    if (advancing || P.i !== i) return; advancing = true;
    const s = P.scenes[i];
    s.fill.style.width = '100%';
    const wait = Math.max(0, Math.min(MAXWAIT, s.tl.duration() - s.tl.time()));
    later(() => {
      s.tl.pause(); s.tl.progress(1);
      caption(null, 0);
      s.el.classList.remove('on'); s.el.classList.add('leaving');
      later(() => { s.el.classList.remove('leaving'); s.tl.pause(0); }, 700);
      later(() => startScene(i + 1), GAP * 1000);
    }, (wait + HOLD) * 1000);
  }
  function finish() {
    P.playing = false; P.ended = true; audio.pause(); caption(null, 0);
    document.getElementById('end').classList.add('on');
  }
  function restart() {
    document.getElementById('end').classList.remove('on');
    P.scenes.forEach(s => { s.fill.style.width = '0%'; });
    P.ended = false; P.playing = true; startScene(0);
  }
  function toggle() {
    if (!P.started) { P.started = true; P.playing = true; document.getElementById('title').classList.add('off'); startScene(0); return; }
    if (P.ended) return restart();
    P.playing = !P.playing;
    document.getElementById('paused').classList.toggle('on', !P.playing);
    const s = P.scenes[P.i]; if (!s) return;
    if (P.playing) {
      if (P.resumeTo != null) { const n = P.resumeTo; P.resumeTo = null; return startScene(n); }
      s.tl.play(); if (!audio.ended) play();
    } else {
      s.tl.pause(); audio.pause();
      if (advancing) { clearTimers(); P.resumeTo = P.i + 1; }
    }
  }
  function jump(d) {
    if (!P.started || P.ended) return;
    const n = Math.max(0, Math.min(P.scenes.length - 1, P.i + d));
    P.scenes[P.i].el.classList.remove('on', 'leaving');
    startScene(n);
  }

  /* ---- export mode: deterministic rendering of the whole video at time T (seconds) ---- */
  P.plan = function () {
    let t = LEAD; const segs = [];
    P.scenes.forEach(s => {
      const extra = Math.max(0, Math.min(MAXWAIT, s.tl.duration() - s.dur));
      const len = s.dur + extra + HOLD + FADE_OUT + GAP;
      segs.push({ s, start: t, len }); t += len;
    });
    return { segs, total: t + TAIL, lead: LEAD };
  };
  const ease = (x) => 1 - Math.pow(1 - x, 3);
  P.renderAt = function (T) {
    document.documentElement.classList.add('export');
    const segs = P.plan().segs;
    const title = document.getElementById('title'), end = document.getElementById('end');
    const reset = (x) => { x.el.classList.remove('on', 'leaving'); x.el.style.opacity = ''; x.el.style.transform = ''; };
    if (T < LEAD) { P.scenes.forEach(reset); caption(null, 0); end.classList.remove('on'); title.classList.remove('off'); title.style.opacity = T < LEAD - 0.5 ? 1 : (LEAD - T) / 0.5; return; }
    title.classList.add('off'); title.style.opacity = '';
    const seg = segs.find(g => T >= g.start && T < g.start + g.len);
    if (!seg) { P.scenes.forEach(reset); caption(null, 0); end.classList.add('on'); return; }
    end.classList.remove('on');
    const local = T - seg.start;
    P.scenes.forEach(x => { if (x !== seg.s) reset(x); });
    seg.s.el.classList.add('on');
    seg.s.tl.pause(); seg.s.tl.time(Math.min(local, seg.s.tl.duration()));
    let op = 1, ty = 0, sc = 1;
    if (local < FADE_IN) { const k = ease(local / FADE_IN); op = k; ty = 40 * (1 - k); sc = 0.985 + 0.015 * k; }
    const outStart = seg.len - FADE_OUT - GAP;
    if (local > outStart) { const k = Math.min(1, (local - outStart) / FADE_OUT); op = 1 - k; ty = -28 * ease(k); sc = 1 + 0.012 * ease(k); }
    seg.s.el.style.opacity = op;
    seg.s.el.style.transform = `translateY(${ty}px) scale(${sc})`;
    caption(local > outStart ? null : seg.s, local);
    seg.s.fill.style.width = Math.min(100, local / seg.s.dur * 100) + '%';
    segs.forEach(g => { if (g.start + g.len <= T) g.s.fill.style.width = '100%'; else if (g.start > T) g.s.fill.style.width = '0%'; });
  };

  P.init = function () {
    if (P.inited) return; P.inited = true;
    fit(); addEventListener('resize', fit);
    build();
    addEventListener('keydown', (e) => {
      if (e.repeat) return;
      if (e.code === 'Space' || e.key === ' ') { e.preventDefault(); toggle(); }
      else if (e.code === 'ArrowRight') jump(1);
      else if (e.code === 'ArrowLeft') jump(-1);
    });
    stage().addEventListener('click', toggle);
    document.addEventListener('visibilitychange', () => { if (document.hidden && P.started && P.playing && !P.ended) toggle(); });
    if (DEV) {
      if (EXPORT) { document.documentElement.classList.add('export'); P.renderAt(parseFloat(q.get('T') || '0')); return; }
      document.documentElement.classList.add('static');
      const id = q.get('scene') || P.scenes[0].meta.id, t = parseFloat(q.get('t') || '0');
      const i = Math.max(0, P.scenes.findIndex(s => s.meta.id === id));
      document.getElementById('title').classList.add('off');
      P.started = true; P.playing = false; show(i); P.scenes[i].tl.time(t); caption(P.scenes[i], t);
      if (q.has('play')) { P.playing = true; startScene(i); }
    }
  };
  P.audio = audio;
  return P;
})();
