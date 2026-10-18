# Engine and player contract

Stage = 1600 × 900 units, letterboxed by the player; export mode renders it exactly. Scenes are `<div class="scene">`
stacked in the stage; one is `.on`. Each scene file is:

```js
SCENES.push({ id: 's05', build(stage, ctx) {         // ctx = { dur, narration, section }
  const D = ctx.dur, tl = gsap.timeline({ paused: true });
  /* create elements inside stage, add tweens at absolute seconds */
  tl.to({}, { duration: Math.max(0.1, D - tl.duration()) });   // hold to the narration's end
  return tl;
}});
```
`build.py` wraps each file in an IIFE and concatenates `helpers.js + helpers-motion.js + player.js` as the engine.

## Data the build injects

`ROTEIRO` (scene order, titles, sections, narration), `DURATIONS`, `ICONS` (name → inner SVG paths), `AUDIO` (data URIs),
`CUES` (`{id: [[start, end, text], …]}`).

## Player (player.js)

- One shared `Audio` element: scene clips can never overlap; pause freezes audio and timeline together.
- Flow by `setTimeout` and CSS classes, not the GSAP ticker (the desktop app's browser pane freezes `requestAnimationFrame`;
  the flow still works there and everywhere else). Drift correction syncs `tl.time()` to `audio.currentTime` on
  `timeupdate` (>0.3 s off).
- Transitions: `.scene.on` (enter: rise 40 px + fade, 0.55 s), `.scene.leaving` (exit: lift 28 px + fade, 0.45 s), gap
  0.12 s. Constants `FADE_IN, FADE_OUT, GAP, HOLD, MAXWAIT, LEAD, TAIL` at the top of the player; `plan()` and `renderAt(T)`
  reproduce the same timing deterministically for export.
- Keys: Space toggles (ignores key repeat), ←/→ jump scenes, click on the stage toggles (phones have no space bar; audio
  needs a gesture). Pauses when the tab is hidden. Guards against double init.
- Dev/export modes by query: `?scene=s05&t=6` seeks a scene paused with transitions disabled (`.static`);
  `?export=1&T=123.4` renders the whole video's state at T (title card for the first `LEAD` s, end card for the last
  `TAIL` s, captions, progress bar, fades computed from `plan()`); `?theme=dark|light` forces a theme in dev.
- `#title` (name + subtitle + "space" hint), `#end` (replay hint), `#paused` badge, `#bar` progress segments, `#cap`
  caption. The hints are hidden in export mode.

## Helpers (helpers.js) — drawing and SVG

- `H.svg(parent)` full-stage `<svg viewBox="0 0 1600 900">`; `H.g`, `H.sv(tag, attrs, parent)`, `H.el(tag, attrs, parent)`.
- `H.icon(parent, name, {x, y, size, cls, color, sw, hidden})` hand-drawn icon group; `hidden:true` prepares strokes for
  `H.draw`. Icons: arrows-sync, bell, clock, cloud, database, document, folder, house, laptop, lock, pencil, person,
  robot, search, sticky-notes, warning.
- `H.prep(target)`, `H.draw(tl, target, dur, pos)`, `H.undraw(...)` stroke drawing via `pathLength=1` (dash `1 2`, offset
  1.03→0; the 0.03 hides the round-cap dot at the path start).
- `H.line(parent, pts, {sw, cls, amp, dash, color})` wobbly polyline; `H.rect`, `H.circle` (hand-drawn, `amp` = wobble);
  `H.arrow(parent, x1,y1,x2,y2, {bend, head, dash})`; `H.bubble(parent, x,y,w,h, tx,ty, {fill})` speech bubble;
  `H.text(parent, str, {x,y,size,cls,anchor})` SVG text (`cls`: soft|dim|accent|blue|green|amber|warn|violet|orange|mono|
  display|serif|label); `H.highlight(parent, x,y,w,h)`.
- `H.word(stage, str, {x,y,size,cls})` HTML word centred at x,y (cls: body|mono|serif|label + color names);
  `H.chars(el)` splits into spans.
- 2.5D: `H.layer(stage, {z, rotX, rotY})`, `H.card(parent, {x,y,w,h,z,rotX,rotY,html})`, `H.box(parent, viewBox, {x,y,w,h})`
  an inline SVG inside HTML.
- Stop motion: `H.FPS=8`, `H.steps(sec)`, `H.stepTo(tl, t, vars, pos)`, `H.jitter(tl, t, {dur, amp, rot, fps, pos})`,
  `H.paper(parent, x,y,w,h, {fill, rot, r})`, `H.poly(parent, pts, {fill})`.
- Tweens: `H.pop`, `H.fade`, `H.out`, `H.shake`, `H.hide(...els)`.

## Motion helpers (helpers-motion.js)

- `H.label(stage, '02 CACHE')` section label (hidden; fade it in at 0.1–0.5 s).
- `H.punch(stage, 'White part. ', 'Accent end.', {y, size, color})` + `H.punchIn(tl, el, pos)`; `y` is clamped to 712.
- `H.pill(stage, text, {x,y,cls,mono,size})`, `H.stamp(stage, text, {x,y,rot,cls})` + `H.slam(tl, el, pos)`.
- `H.counter(stage, {x,y,size,cls,from,format})` → `{el, set(v), tween(tl, to, pos, dur)}`.
- `H.terminal(stage, {x,y,w,h,title,font,lines})` → `{el, body, line(spec), typeLine(tl, spec, pos, dur)}`; token classes
  `p` (prompt, accent) `k` (blue) `o` (amber) `w` (white) `r` (red).
- `H.agent(svg, {x,y,size,mood,hidden})` blob character with antenna (`g.setMood('happy|neutral|doubt|angry|dizzy')`);
  `H.human(svg, {x,y,size,laptop,hidden})` stick figure; `H.link(svg, x1,y1,x2,y2, {arrow, dash, cls, sw})`.

## CSS tokens and classes (style.css)

`:root` tokens: `--bg --paper --paper-2 --paper-3 --edge --ink --ink-soft --ink-dim --accent --accent-2 --amber --warn
--violet --orange --hl --glow --shadow --font-display --font-body --font-mono --font-serif`. Classes: `c-*` for SVG
color, `.t.*` for SVG text, `.word.*`, `.pill.*`, `.stamp.*`, `.card`, `.card.glow`, `.term`, `.cut`. Rewrite the token
values per project; keep the names so helpers and briefs stay valid. The structural rules (`.ink:not([fill])`, `.ink`
before `.c-*`, `.static *{transition:none}`, `.export` layout, `#cap` placement) are load-bearing: do not reorder them.

## Build and serve

`python scripts/build.py <dir> --dev` → `dist/<slug>.html` (publish), `dist/export.html` (charset-wrapped, render),
`dist/dev.html` (includes `_template`). Serve `dist/` with `python -m http.server 8766 --bind 127.0.0.1` in the
background for QA and render; `dev.html` and `export.html` carry their own charset, the bare artifact page does not
(the artifact skeleton adds it on publish).
