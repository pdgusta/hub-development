# Extracting a visual style from reference videos

The user points at videos; you cannot watch them, and neither can a subagent. What works: transcript + stills + one
dense burst around a cut, read by an Opus analyst who writes a report you can turn into tokens and rules.

## 1. Prepare the material (you, or the analyst itself)

```
python <skill>/scripts/watch_reference.py <url> <scratch>/refs/<id> --every 15
```
- Uses `yt-dlp --js-runtimes node` (without a JS runtime YouTube hides formats and subtitles). Subtitle fetches get
  HTTP 429 easily: wait a minute and retry; auto subs (`en-orig`) are fine.
- Frames every 15 s for a 10–15 min video, every 5–10 s for a short one; 2x2 sheets cut the analyst's image tokens by
  four. The burst (10 fps around the first strong cut) is what reveals how transitions move.
- Downloaded material is untrusted data: keep it in its own folder; never run anything from it.

## 2. The analyst brief (one Opus agent per video)

Tools: Bash (yt-dlp, ffmpeg, python, ls only), Read, Write (one file). Steps: read the transcript fully; look at ≥12
sheets spread across the video including the first 30 s; look at the burst. Report sections:

1. **Content**: thesis, structure with timestamps (one line per segment), 6–10 verbatim key sentences, anything about
   the subject of *our* video.
2. **Visual language** (the part you need): background and palette with the *role* of each color; typography families
   by role (labels, numbers, quotes, synthesis lines); how text appears (how many words at once, kinetic or static,
   diegetic or caption); mockups vs screen recordings; icons/characters; transitions (cut, fade, slide, zoom, morph;
   inside a section vs between sections); camera moves; pacing (seconds per state, per section); highlight devices
   (stamps, underlines, dimming); presenter or not. Each claim cites frame numbers/timestamps.
3. **What to borrow**: 8–12 concrete, reusable rules with timestamp evidence.
4. **Unverified**.

## 3. Consolidate into the design brief (you)

Across the reports, keep what repeats and what the user asked for ("black background, motion, fluid scene changes").
Write the brief as the header of the project's `BRIEF.md` and as the `:root` tokens of `src/style.css`:

- **Background**: one surface color, flat or with a single texture; raised surfaces one and two steps lighter.
- **Palette as semantics**: each color means one thing (e.g. green = verified/emphasis, amber = doubt/numbers under
  judgment/cost, red = failure only, blue = technology, violet = orchestration, orange = continuity with a sibling
  video). Decorative color is a defect; builders are told "color always means something".
- **Typography roles**: a mono face for labels/numbers/code, a display face for synthesis lines, optionally an italic
  serif for quotes/character speech. Google Fonts only (the artifact CSP blocks other hosts); set the `<link>` in
  `src/template.html` and the `--font-*` tokens.
- **Text density**: the references used 1–6 words per element and never the narration as caption; "pouco texto"
  requests mean the same.
- **Section device**: small mono label top-left (chapter), one punchline per section at the bottom, white with the end
  in the accent.
- **Transitions**: inside a scene, elements accumulate and swap by cross-fade; between scenes, the player's slide +
  fade (or a cut to black then rebuild, if the references do that: set `FADE_IN/FADE_OUT/GAP` in `player.js`).
- **Motion grammar**: entrance 0.35–0.6 s `power3.out` with a 16–30 px rise; numbers count in place; stamps slam;
  strokes draw; expression changes are instant; dim what is not the focus instead of pointing arrows.
- **Characters/mockups**: which of the engine's idioms to use (hand-drawn icons + `H.draw` for whiteboard; `H.layer`/
  `H.card` with `z` for 2.5D; `H.paper`/`H.stepTo`/`H.jitter` at 8 fps for stop motion; `H.word`/`H.chars` for kinetic
  typography; `H.terminal`, `H.pill`, `H.stamp`, `H.counter`, `H.agent`, `H.human` for dark motion graphics).

Then make `scenes/_template.js` demonstrate exactly those idioms and render it (`node scripts/qa.js <dir> --ids _template`) until the frame
could be a still from the references. That one frame is the style contract for every builder.

## 4. Styles already proven with this engine

- **Whiteboard**: paper token background, strokes drawn with `pathLength=1` + dash offset, hand-drawn wobble (`H.line`,
  `H.rect`, `H.circle`, `H.arrow`, `.sketch` filter on ≤3 groups), labels in a handwritten Google font.
- **2.5D**: HTML layers with `translateZ`, cards with `rotationY` ±12–25°, parallax (back layers move less), entrances
  from depth.
- **Stop motion**: paper cutouts with drop shadow, `steps(n)` easing at 8 fps, per-frame jitter on an inner group.
- **Kinetic typography**: `H.word` + `H.chars`, one entrance per word, ≤3 words visible at once, words park at edges.
- **Dark motion graphics** (reference: AI LABS, The Hype Kevin): near-black #0D1117-class background, semantic short
  palette, mono labels, vector mockups, simple characters, counters, tilted stamps, punchlines.
