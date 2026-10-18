# QA, export and the pitfalls already paid for

## Why headless Edge and not the browser pane

The desktop app's browser pane freezes `requestAnimationFrame` (GSAP's ticker stood at 0.4 s after 20 s) and its
screenshots time out when the window is behind another. It cannot open `file://` outside the project either. Serve
`dist/` on `localhost` and render stills with headless Edge; drive logic checks through the pane's JavaScript tool only.

One Edge process per screenshot (`msedge --headless=new --screenshot=...`) is unreliable: the process returns before the
PNG is written, and when another headless Edge is already running on the machine it comes up without a renderer and never
writes the file (two hangs in one production). `qa.js` spawns a single Edge with `--remote-debugging-port`, connects with
puppeteer-core, navigates once per frame (`dev.html?scene=<id>&t=<s>&v=<timestamp>`, the `v` defeats the HTTP cache) and
kills only its own process by profile path, never all `msedge.exe`: that is the user's browser.

`puppeteer.launch` fails with msedge ("Failed to launch the browser process"); spawn Edge with
`--remote-debugging-port` and `puppeteer.connect` (`render.js`, `test_player.js`). ≈120 ms per 1600×900 JPEG frame;
three workers on frame ranges cut a 9-minute video from ~35 to ~12 minutes.

## Defects seen in builder scenes and their fixes

| Symptom in the sheet | Cause | Fix |
|---|---|---|
| A word/counter sits at the top edge (y=0) | `tl.fromTo(el, {y:16}, {y:0})` on an element positioned by `gsap x/y` (absolute) | tween `y` between absolute values (`y: 536 → 520`) or use `yPercent` |
| Bars float above their axis, or a bar is off-frame | `scaleY` + `svgOrigin` on paths, evaluated after seeks | rise + fade entrances (`y: 24 → 0`, opacity) |
| Labels clipped at the top | same relative-`y` pattern through a shared `rise()` helper | give words their own absolute tween |
| Punchline hidden behind the caption | caption wraps to three lines | `H.punch` clamps `y ≤ 712`; caption 25 px, 22 px from the bottom |
| Colored strokes render white | `.ink{color}` declared after `.c-*` | keep `.ink` before `.c-*` (already fixed in the asset) |
| Fills missing on `H.rect`/`H.bubble` | `.ink{fill:none}` beat the `fill` attribute | `.ink:not([fill]){fill:none}` (already fixed) |
| Stray dots where strokes are not yet drawn | round caps at dash boundaries with offset exactly 1 | dash `1 2`, offset 1.03 (already in `H.prep`) |
| Dashed line renders solid | `pathLength=1` makes dash units normalized | dash in normalized units (`0.02 0.014`) or drop `pathLength` on that path |
| Title overlay still visible in stills | CSS transitions never advance in a static render | `.static` class in dev mode disables transitions (already in player) |
| Mojibake in captions of the MP4 (`sÃ³`) | page served without charset by `http.server` | render `dist/export.html` (charset-wrapped), never the bare page |
| `_template` scene at the end of the MP4 | rendered from `dev.html` | render from `export.html` |
| Audio inputs "No such file" when muxing | input index off by one (video is input 0) | `[i+1:a]` (already in `render.js`) |
| Two clips overlapping / pause not pausing audio | one `Audio` per scene | one shared `Audio` element (already in player) |

## Functional checks that count

- `test_player.js`: pause freezes `audio.currentTime`; resume continues; the scene index advances when the clip ends;
  pausing in the hand-off window holds the next scene until resume.
- MP4: `ffprobe` shows h264 1600×900 at the requested fps and an aac stream; sampled frames at 1 s (title card), first
  scene, two mid points, a transition and the last second (end card); `volumedetect` ≈ −91 dB on the cards and ≈ −1 dB on
  scenes.
- Frame count ≈ duration × fps (the plan's `total` includes `LEAD` and `TAIL`).

## What you cannot verify, say so

You cannot listen to the narration: report that you checked durations, levels, provider and word-level alignment
counts (`tts-log.json`: words vs matched), not pronunciation.
