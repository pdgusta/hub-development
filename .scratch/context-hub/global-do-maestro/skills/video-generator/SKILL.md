---
name: video-generator
description: Fast production of narrated explainer videos from content the user hands over (a document or a folder), delivered as (1) an HTML artifact with play/pause on space and (2) an MP4, in a visual style extracted from reference videos the user points at. The user supplies the content, the video specs (length, language, audience, deliverables) and the style references, plus an optional direction (script idea, register, how complex the speech may be); the skill asks when one of the three required inputs is missing. Covers reading the content into a citable fact sheet, style extraction from YouTube references, script and captions, narration through the local FreeLLMAPI gateway (or Gemini TTS), scene building by parallel subagents on a GSAP engine, visual QA with headless Edge, artifact publishing and MP4 rendering. Use this whenever the user asks for a video, an animated explainer, a narrated animation, "um vídeo explicando…", a motion-graphics piece, a whiteboard/2.5D/kinetic-typography/stop-motion explainer, a dubbed or subtitled clip, or an MP4 plus HTML artifact of any explanation, even if they do not say "video"; also when they ask to turn a document, a research folder, notes or docs into a narrated visual explanation.
---

# Video generator

You are the orchestrator. You own the thinking (direction, script, engine, integration, QA, delivery); subagents do the
parallel and the mechanical work. The pipeline below produced three videos (a pt-BR whiteboard/2.5D/stop-motion/kinetic
explainer, an English dark motion-graphics technical one, and a pt-BR dark sketch one) and every rule here was learned
from them. The purpose is speed: a complex thing explained well, in one sitting, from material the user already has.
The skill makes videos; it does not research the subject on the web and it does not open tickets or write into the
user's project. Follow the phases in order; each one leaves files on disk so a `/clear` loses nothing.

## 0. The four inputs (no tools yet)

The user hands over, in their own words and order:

1. **Content**: a document, a folder, a few files. Everything the narration says comes from here (phase 1).
2. **Specs**: length, narration language, captions (language, or none), audience (lay or technical), deliverables
   (artifact, MP4 or both), and anything about where to write or which provider to use.
3. **Style references**: URLs of videos. The style is extracted from them (phase 2), never assumed and never the
   engine's default look.
4. **Direction** (optional): a script idea, a thesis, a metaphor to carry the piece, the register and how complex the
   speech may be, what to leave out.

If content, specs or references are missing or ambiguous (no folder, no length, no reference URL, "a video" with no
language), ask one short question listing exactly what is missing, and wait: a video built on a guessed length or style
is a video rebuilt. Defaults you may fill without asking, saying so: captions off unless requested (and in the narration
language when requested); deliverables = both; provider = the FreeLLMAPI gateway when the user has it (`localhost:3001`,
key `FREELLM_API_KEY`), else Gemini; 30 fps; working files in the scratchpad unless the user names a folder. A
"dubbing" that is "small, centred at the bottom" means burned-in captions, not a second audio track; say which you
understood.

If the direction is missing, write it yourself in three lines (thesis; the spine, an image or phrase the video returns
to; register and audience) and put it in your opening line so the user can redirect in seconds rather than after thirty
minutes. A video that merely lists the content is correct and dull; the ones the user kept had a proposal: an opening
image that comes back changed, a sentence that carries the piece ("an agent pays twice for what it forgets"), a lay
analogy for a technical mechanism. Creativity goes in the direction and the script; production stays strict.

Model roles when the user does not set them: Opus = video analysts; Sonnet = readers of big content and scene builders;
Haiku = icon drawing and plain summaries; you = everything with judgment.

Then say in one line what you will do first, and go.

## 1. Read the content into a fact sheet

Read `references/content-reading.md`. In short: read the content yourself when it fits (about 2,000 lines); for bigger
folders spawn one reader subagent per file family in the same turn, with "quotes only, listed files only" briefs, then
read their files. You write `00-fact-sheet.md`: thesis, the pieces with pointers and quotes, a table concept → what the
content says → what the video does with it, and "not in the content". Nothing on screen or in the narration without a
row in that table. If the content does not cover something the video needs, it goes to the recap or to a question, not
to a web search.

## 2. Extract the style from the references (Opus analysts)

Read `references/style-extraction.md`. Mechanics: `scripts/watch_reference.py <url> <dir>` gets the transcript, a
low-res copy, frames every N seconds, 2x2 contact sheets, scene cuts and a 10 fps burst around the first cut. One Opus
subagent per video reads transcript + sheets + burst and writes a report: content with timestamps, visual language
(background, palette with roles, typography roles, how text appears, mockups vs recordings, transitions, camera, pacing,
highlights), and 8–12 reusable rules with timestamp evidence. If the user's content already contains such a report for
the same URL, reuse it and fetch frames only when a rule needs checking. You then consolidate the rules into the
project's **design brief**: tokens (colors with meanings), fonts (Google Fonts only, the artifact CSP allows nothing
else), motion grammar, section device, text density, whether the style uses continuous captions or only punchlines
(when the reference says no continuous captions and the user asked for captions, the user wins; say it), which engine
idioms map to which reference habits. The default engine assets are a dark motion-graphics look; rewrite
`src/style.css`'s `:root` tokens and the font link in `src/template.html` to the brief before any scene is built. Never
keep a palette because it shipped with the assets.

## 3. Script and captions

Write `roteiro.json` yourself (it is the creative core; do not delegate it):
- Top level: `title`, `lang` (narration language, e.g. `pt-BR` or `en`; it decides the TTS provider), `voice`.
- `scenes[]` with `id` (`s01`…), `section` (short label shown on screen, may be empty), `title`, `style` (the reference
  idiom used), `lines` = `[[narration sentence, caption sentence], …]` (caption in the caption language, 1:1 with the
  narration sentences so timing can be aligned), `visual` (beat-by-beat description), `on_screen_text` (the only words
  allowed on screen, 1–6 words each, plus one punchline per section if the style uses them).
- Budget: 2.5 words/s of narration; 20–35 s per scene; ≤ the user's max length minus 5 s of cards and gaps.
- Every number or claim on screen or in narration must trace to a row of the fact sheet. For a lay audience, metaphors
  and one idea per scene; for a technical one, the real names (flags, files, commands) as diegetic mockup text. The
  direction (the user's or yours) decides the register; the fact sheet decides what may be said.
- Open and close with the same image, changed (the references all do it); state the thesis in the first 10 seconds.

## 4. Narration and cue timing

`python scripts/gen_tts.py <project> [--provider freellmapi|gemini] [--voice ash]` (one request per scene, 3 in parallel
on FreeLLMAPI, 2 on Gemini). On FreeLLMAPI the model follows `lang`: English narration goes to Cloudflare MeloTTS, any
other language to Gemini TTS (the user's rule; the gateway can only make MeloTTS speak English). Never send `model: auto`. It trims silence, normalises loudness, writes `audio/<id>.mp3`, `durations.json` and
`cues.json` (captions timed by transcribing each clip and aligning the script sentences to the transcript words). Read
`references/narration.md` for voices, languages, and what to do when a provider returns 429 or a different voice.
Durations drive everything after this point, so run it before spawning scene builders. If the total runs long, cut
scenes, never speed the audio: a sped-up voice is the first thing a listener notices.

## 5. Engine, project scaffold, reference scene

`python scripts/new_project.py <dir> --title "…"` copies the engine (`helpers.js`: drawing/SVG/whiteboard/2.5D/stop-motion
helpers; `helpers-motion.js`: labels, punchlines, pills, stamps, counters, terminal mockups, characters; `player.js`: one
shared audio element, timer-driven scene flow, captions, fluid transitions, export mode), `style.css`, `template.html`,
16 hand-drawn icons and `scenes/_template.js`. Read `references/engine-api.md` once per project, then:
1. Edit tokens and fonts to the design brief; adjust `_template.js` to show the idioms of *this* style (it is the
   reference every scene builder reads, so make it demonstrate the right things).
2. `cd <dir>/export && npm i puppeteer-core@23.11.1` (the Node scripts resolve it from `<dir>/export`), then
   `python scripts/build.py <dir> --dev`, serve `dist/` (`python -m http.server 8766 --bind 127.0.0.1`, background), and
   render the template with `node scripts/qa.js <dir> --ids _template --port 8766`; look at `qa/_template_sheet.png`.
   Fix the engine until the template frame looks exactly like the style brief. Do not spawn builders before this.
3. Icons you lack: Haiku subagents, 4 icons each, strict rules (stroke-only paths, 100×100 box, `currentColor`,
   path order = drawing order) so `H.draw` can animate them. Check them on a contact sheet.

## 6. Scenes in parallel (Sonnet builders)

Write `BRIEF.md` from `references/scene-brief-template.md` with the style rules filled in, then spawn one Sonnet
subagent per scene in a single turn (20 scenes = 20 agents; stay under the user's concurrency cap). Each gets: tools
limited to Read (brief, engine, template scene, style, roteiro), Write (its own file), Bash (`node --check` only); the
scene id and duration D; 3–6 scene-specific notes (which helper for which element, positions, colors by meaning). Ask
for a 3-line hand-back. Builders cannot render, so expect layout guesses; your QA catches them.

## 7. Visual QA, functional test, fixes

1. `build.py --dev`, then `node scripts/qa.js <dir> --port 8766` renders 4 frames per scene (12%, 40%, 70%, 98.5% of D)
   through one headless Edge into 2x2 sheets, seconds per scene. Read every sheet. Typical defects and fixes are in
   `references/qa-and-pitfalls.md` (elements at y=0 from a relative `y` tween on an absolutely positioned word; bars
   offset after `scaleY` + `svgOrigin`; caption colliding with the punchline; labels or bars outside the frame; mojibake
   when the page is served without charset; a scene that cuts instead of evolving).
2. Fix small things yourself in the scene files; send a scene back to a new builder only for a redesign.
3. `node scripts/test_player.js <dir> export.html --port 8766` (needs two or more scenes):
   start, pause (audio time must freeze), resume, scene change, pause at a scene edge (must hold), resume into the next.
4. Dark/light: the artifact runs in the viewer's theme; a single-look design (black-background video) is fine, but set
   `color-scheme` and an explicit body background. For two themes, render `qa.js --theme dark` too.

## 8. Deliver

- **Artifact**: load the `artifact-design` skill if the session requires it, then publish `dist/<slug>.html` with a
  short name as `<title>`, an `icon`, and a one-sentence description. Audio is embedded as base64 (≈0.5 MB/min at 64k);
  keep the page under 16 MB. Re-publish the same path to update.
- **MP4**: `node scripts/render.js <dir> --port 8766 --workers 3 --fps 30` renders `dist/export.html` (charset-safe) in
  parallel headless Edge instances (≈120 ms/frame/worker), concatenates, and mixes the clips at each scene's start.
  Verify with ffprobe (streams, duration), six sampled frames (title card, first scene, mid, a transition, end card) and
  `volumedetect` on the cards (silent) and a scene (≈ −1 dB peak). Send the file with the file tool when available.
- **Recap** in the user's language: the direction used (theirs or yours), what each deliverable is, how it was verified,
  what was not verified (you cannot listen to the narration: say so), and what the content did not cover.
- Stop the local server and leftover headless `msedge` processes (filter by your profile path, never kill the user's
  browser).

## Decision points that recur

- *The user corrects a premise mid-run* (e.g. "pause must also pause the audio"): fix the engine, re-run the functional
  test, re-publish the same artifact path, then re-render only if the MP4 is affected.
- *A provider rate-limits*: lower concurrency and retry with backoff; never switch provider silently.
- *A builder's scene breaks the text rule*: on-screen text is only the allowed words and diegetic mockup text; a sentence
  from the narration on screen is a defect.
- *Length over budget*: cut scenes, not words per scene, and never the audio speed; the script's pacing is what makes it
  legible.
- *The content is thinner than the video needs*: say it in the recap or ask; do not fetch, do not fill from memory.

## Files in this skill

- `scripts/new_project.py`, `build.py`, `gen_tts.py`, `qa.js`, `render.js`, `test_player.js`, `watch_reference.py`
- `assets/engine/*.js`, `assets/style.css`, `assets/template.html`, `assets/scene-template.js`, `assets/icons/*.svg`
- `references/content-reading.md`, `style-extraction.md`, `narration.md`, `engine-api.md`, `scene-brief-template.md`,
  `qa-and-pitfalls.md`
