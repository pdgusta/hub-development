You are triaging one CONCEPT (a technique or idea, not a specific product) for a specific system. There is no
primary source: judge from the names, the summaries written by other models and the terms on the card, plus your
general knowledge of the concept. Mark "doubt": true when the card is too thin or the concept is unclear.

## The system (the "hub")

A personal context hub: a folder of Markdown notes, edited by a person in Obsidian and by AI coding agents
(Claude Code, Codex, GitHub Copilot) on two Windows machines. The notes live in a CouchDB database kept in sync
by the Obsidian LiveSync plugin and its CLI; agents read and write through an MCP server. The hub needs a
**search layer** (agents find the right passage without reading everything, over Markdown in Portuguese and
English) and **other parts of the stack** (sync, conflict handling, MCP, Obsidian, agent memory, indexing...).

## Answer

Reply with ONLY one JSON object, no prose, with exactly these keys:

```
{
  "concept_en": "<canonical English name of the concept, short, lowercase, e.g. 'hybrid search', 'bm25', 'stemming'>",
  "serve": "search" | "stack" | "none",
  "role": "<what this concept would do in the hub, max 15 words; empty if none>",
  "mechanism": ["bm25" | "full_text" | "vector" | "hybrid" | "grep" | "graph" | "reranker" | "embeddings" | "other" | "n/a"],
  "place": ["disk" | "inside_db_mcp" | "network_service" | "light_client" | "library" | "n/a"],
  "tools_on_card": ["<names of concrete tools or projects mentioned on the card that implement it>"],
  "doubt": true | false,
  "evidence": "<short quote(s) from the card's summaries; max 200 chars>"
}
```

- "search" = a technique the search layer could use; "stack" = useful to another part of the hub; "none" =
  unrelated to the hub.
- Different cards may be the same concept in other words or languages ("busca híbrida", "hybrid retrieval");
  "concept_en" lets them be grouped later, so use the most common English name.

## The concept

```
{CARTAO}
```
