You are checking a triage verdict against the primary source. The package file holds the project's README (or the
text of its web page, when "fonte" is "site") in the field "readme". Its triage answers were written by
other models (one or two of them; they may disagree). Read the README carefully and decide.

## The system (the "hub")

A personal context hub: a folder of Markdown notes, edited by a person in Obsidian and by AI coding agents
(Claude Code, Codex, GitHub Copilot) on two Windows machines (native NTFS). The notes live in a CouchDB database
kept in sync by the Obsidian LiveSync plugin and its CLI; agents read and write through an MCP server. The hub
needs a **search layer** (agents find the right passage without reading everything, over Markdown in Portuguese
and English, reachable over MCP) and **other parts of the stack** (sync, conflict handling, MCP servers, Obsidian
plugins, agent memory, embeddings, indexing, file watching, backup...).

## Answer

Reply with ONLY one JSON object:

```
{
  "resultado": "confirma" | "corrige" | "rejeita",
  "final": { ...the triage object with the corrected values, same keys as the triage answers:
             serve, role, place, mechanism, mcp, windows, portuguese, license, maturity, doubt, evidence... },
  "o_que_mudou": ["<field>: <old> -> <new>, short reason", ...],
  "nota": "<one sentence: why it matters (or not) for the hub; max 30 words>"
}
```

- "confirma": the (majority or only) verdict is right as is; "final" repeats it (pick the better answer if two).
- "corrige": the project is useful ("search" or "stack") but some field is wrong; fix it in "final".
- "rejeita": the project is not useful to the hub ("serve": "none" in "final"), or the card is broken (README of a
  different project, empty page, wrong link) — say which in "nota".
- Only what the README supports; "unknown" when it does not say. "doubt" must be false unless the README truly does
  not allow a decision.

## Input

The package file holds the card (fields "chave", "nomes", "urls", "fonte", "readme") and "respostas": the triage
answers, each with "por" (who wrote it) and "resposta" (the triage object).
