# BRIEF.md template for scene builders

Copy to the project as `BRIEF.md`, fill the `{{…}}` parts from the design brief, keep the hard rules.

```markdown
# Brief for scene builders — "{{video title}}"

You are building ONE scene of a {{lay|technical}} explainer video (HTML + GSAP), narrated in {{language}}, with a
{{caption language}} caption the player adds by itself (you do NOT draw captions). The look: {{two or three sentences
distilled from the reference reports: background, palette roles, label device, mockups vs drawings, characters, pacing}}.
Inside a scene, elements accumulate and swap by fade; the player handles transitions between scenes, so your scene starts
blank and builds up.

## Files you may read (read all four before writing)
- `BRIEF.md`; `src/engine.js` (helper API, comments are the doc); `scenes/_template.js` (every idiom of this style);
  `src/style.css` (tokens and classes). Paths relative to `{{absolute project dir}}`.

## The file you write
Exactly one: `scenes/<id>.js`, shape:
SCENES.push({ id: '<id>', build(stage, ctx) { const D = ctx.dur; const tl = gsap.timeline({ paused: true });
  /* … */ tl.to({}, { duration: Math.max(0.1, D - tl.duration()) }); return tl; } });

## Hard rules
1. Coordinate space 1600 × 900, 70-unit margin. Keep y > 790 free except for the punchline (the caption lives there);
   punchline at y ≈ 712 (`H.punch(..., { y: 712 })`).
2. Colors only through tokens/classes. Meanings: {{accent = …; accent-2 = …; amber = …; warn = …; violet = …;
   orange = …}}. No literal hex. Color always means something.
3. Text on screen: only the strings in your spec's `on_screen_text` (fewer is fine), the section label from `section`,
   and purely diegetic mockup text (a prompt line, a file name, a number). Never a narration sentence. ≤ 6 words per
   element.
4. No external resources, no fonts, no images, no fetch; only `gsap` and `H`.
5. Scope to your stage: no global querySelector, no element ids.
6. Starts blank, builds up, ends composed (the last frame is a clean picture; the player holds it ~1 s).
7. Timeline ≈ D: last tween ends ≥ 0.8 s before D; never exceed D by > 1 s.
8. Sync to the words: even pacing, a line at character offset c of N is heard at t = D·c/N; lead by ~0.2 s. Label at
   0.1–0.5 s; punchline only after the point is made (last 25%).
9. ≤ ~150 SVG elements, no per-frame JS, no onUpdate loops (except H.counter).
10. Motion grammar: {{from the design brief: entrance timing/easing, rise, counters, stamps, strokes, dimming, no
    flashing above 3 Hz}}.
11. Code in English, short comments, no console.log.

## Style idioms (which helper for what)
{{list the 4–8 idioms with the helper calls, e.g. "section label: H.label; punchline: H.punch + H.punchIn; terminal:
H.terminal (+typeLine); numbers: H.counter mono; verdicts: H.stamp + H.slam; characters: H.agent / H.human; drawn
things: H.icon hidden:true + H.draw, H.line/H.rect/H.circle/H.arrow"}}

## Available icons
arrows-sync, bell, clock, cloud, database, document, folder, house, laptop, lock, pencil, person, robot, search,
sticky-notes, warning {{+ project icons}}.

## Verify before reporting
Run `node --check scenes/<id>.js` (the only command allowed). Re-read once against rules 1–8.

## Report (3 lines max)
file written; approximate timeline length; anything the integrator should know.
```

## The per-scene prompt (what you send with the brief)

```
You are a scene builder. Tools allowed: Read (only BRIEF.md, src/engine.js, scenes/_template.js, src/style.css and
roteiro.json), Write (only your scene file), Bash (only `node --check <your file>`). Nothing else.
Folder: <abs path>. Read BRIEF.md and the three files it names, then your scene in roteiro.json (id "<id>": section,
lines, visual, on_screen_text). D = <dur> s. Write scenes/<id>.js per the brief.
Scene notes: <3–6 sentences: which helper for each element, approximate positions (x,y,w,h), colors by meaning,
the order of beats, and the punchline text if any>.
```

Scene notes are where your judgment goes: give positions so twenty agents do not all centre everything, and name the
helper so they do not reinvent it. Expect them to add small diegetic strings (terminal titles, file names); that is fine.
