/* REFERENCE SCENE for video 2 — dark motion-graphics idioms with the v2 helpers (window.H).
   A real scene file is exactly this shape: one SCENES.push({ id, build }) and nothing else at top level. */
SCENES.push({
  id: '_template',
  build(stage, ctx) {
    const D = ctx.dur, tl = gsap.timeline({ paused: true });

    /* 1) section label (mono, top-left) fades in first: the anchor of the section */
    const label = H.label(stage, '02 CACHE');
    tl.to(label, { opacity: 1, duration: 0.4 }, 0.1);

    /* 2) a terminal mockup that types one line, then prints a result line */
    const term = H.terminal(stage, { x: 120, y: 150, w: 720, h: 300, title: 'context-hub', lines: [[{ t: '$ ', c: 'p' }, { t: 'claude --model opus --effort low', c: 'w' }]] });
    tl.to(term.el, { opacity: 1, y: 0, duration: 0.5, ease: 'power3.out' }, 0.4);
    term.typeLine(tl, [{ t: '> ', c: 'k' }, { t: 'reading AGENTS.md', c: 'w' }, { t: '  ✓', c: 'p' }], 1.2, 0.8);
    term.typeLine(tl, [{ t: 'Prompt cache: ', c: 'o' }, { t: '91% of input tokens from cache', c: 'w' }], 2.4, 1.0);

    /* 3) SVG canvas for drawn things: an agent character, a human, a link with an arrow, an icon */
    const svg = H.svg(stage);
    const ag = H.agent(svg, { x: 1000, y: 180, size: 180, mood: 'happy', hidden: true });
    const hu = H.human(svg, { x: 1280, y: 190, size: 160, laptop: true, hidden: true, cls: 'c-soft' });
    const ln = H.link(svg, 1190, 270, 1270, 270, { arrow: true, cls: 'c-dim' }); H.prep(ln);
    const db = H.icon(svg, 'database', { x: 1060, y: 420, size: 90, cls: 'c-orange', hidden: true });
    H.draw(tl, ag, 1.0, 0.8);            // strokes draw in
    H.draw(tl, hu, 0.8, 1.6);
    H.draw(tl, ln, 0.4, 2.4);
    H.draw(tl, db, 0.6, 3.0);
    tl.call(() => ag.setMood('doubt'), null, 3.6);   // expression change (instant, like a cut)
    tl.call(() => ag.setMood('happy'), null, 5.0);

    /* 4) a counter that counts in place, a pill annotation, a stamp verdict */
    const c = H.counter(stage, { x: 1170, y: 640, size: 110, cls: 'green', format: v => Math.round(v) + '%' });
    tl.to(c.el, { opacity: 1, duration: 0.3 }, 3.2); c.tween(tl, 84, 3.3, 1.4);
    const pill = H.pill(stage, 'from cache', { x: 1170, y: 725, cls: 'green', mono: true });
    tl.to(pill, { opacity: 1, scale: 1, duration: 0.35, ease: 'back.out(2)' }, 4.2);
    const st = H.stamp(stage, 'PASS', { x: 760, y: 420, rot: -10 });
    H.slam(tl, st, 4.8);

    /* 5) the section punchline: white + green end, bottom center, after the scene made its point */
    const punch = H.punch(stage, 'Stable prefix. ', 'Warm cache.');
    H.punchIn(tl, punch, 5.6);

    tl.to({}, { duration: Math.max(0.1, D - tl.duration()) });
    return tl;
  }
});
