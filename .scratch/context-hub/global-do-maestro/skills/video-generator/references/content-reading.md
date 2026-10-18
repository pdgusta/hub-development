# Reading the content into a fact sheet

The video explains the content the user handed over (a document, a folder, a few files). The narration must be
traceable to it: every number, name, path, flag or claim on screen or in the voice should exist as a quote in the
content. Model-written summaries drift; quotes do not. This phase is reading, not research: no web, no tickets, no new
sources. If the content lacks something the video needs, the gap goes in the recap (or in a question to the user), not
in a fetch.

## When to read it yourself and when to delegate

- Up to roughly 2,000 lines in total: read everything yourself. You will write the script, so the facts must be in
  your head, not only in a file.
- Bigger folders: one reader subagent per file family (one per report, one per folder of notes), all spawned in the
  same turn, Haiku for plain summaries of local files, Sonnet when the reader must judge what matters for the video.
  Then read their fact files yourself. Delegation saves your context, not your reading.

Reader brief skeleton (adapt the nouns):

```
You are a reader subagent. Tools allowed: Read (only the files listed), Write (one file). No web, no other files.
Files: <exact paths>. Subject of the video: <one sentence>. Audience: <lay | technical>.
Write to: <absolute path>/<nn>-<family>.md
Format: frontmatter (files read, date, a warning line that this is model output with verbatim quotes).
One section per file or topic, each with: (a) 2–4 sentences of what it says; (b) 1–3 verbatim quotes carrying every
number/path/flag/name you state, with the file and section; (c) one line on how it serves the video
(or "does not apply"). Copy no keys, tokens or personal data. End with "Not in the content": what the subject would
need that these files do not say. Reply with 3 lines: file written, what is covered, what is missing.
```

Why the limits: a reader that may write anywhere overwrites a sibling's file; a reader allowed to search beyond the
list brings facts the user did not hand over, which the video then states as if they were in the document.

## The fact sheet (you write it)

`00-fact-sheet.md` in the project folder:

1. **Thesis** in one sentence: what the viewer should believe at the end.
2. **The pieces**: each idea the video will carry, with the pointer (file + section or line range) and the quote.
3. **Table** concept → what the content says (quote) → what the video does with it (scene, mockup, number on screen).
   The video's sections come straight from this table; if you cannot write a row, you cannot write the scene.
4. **Not in the content**: what you would have liked to say and cannot. The script must not fill it from memory; the
   recap lists it.

Direction lives next to the facts: if the user gave a direction (a script idea, a register, "for lay people"), the table's
third column follows it; if not, the three lines you wrote in phase 0 do. The fact sheet is the only place where the
content and the direction meet before the script, so a reader can check in one file that nothing was invented.
