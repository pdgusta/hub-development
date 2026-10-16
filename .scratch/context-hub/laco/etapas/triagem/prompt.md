You are triaging one software project for a specific system. Judge ONLY from the README below (the primary
source). Do not use outside knowledge about the project; if the README does not say, answer "unknown".

## The system (the "hub")

A personal context hub: a folder of Markdown notes, edited by a person in Obsidian and by AI coding agents
(Claude Code, Codex, GitHub Copilot) on two Windows machines (native NTFS, not WSL). The notes live in a
CouchDB database that the Obsidian LiveSync plugin and its CLI keep in sync with the folders; agents read and
write through an MCP server. The hub needs:
- a **search layer**: agents must find the right passage without reading everything (keyword/BM25, semantic,
  hybrid, grep, graph...), over Markdown in Portuguese (pt-BR) and English, reachable by agents over MCP;
- **other parts of the stack**: sync, conflict handling, MCP servers, Obsidian plugins, agent memory,
  embeddings, indexing, file watching, backup, and similar.

## Answer

Reply with ONLY one JSON object, no prose, with exactly these keys:

```
{
  "serve": "search" | "stack" | "none",
  "role": "<what it would do in the hub, max 15 words; empty if none>",
  "place": ["disk" | "inside_db_mcp" | "network_service" | "light_client" | "library" | "n/a"],
  "mechanism": ["bm25" | "full_text" | "vector" | "hybrid" | "grep" | "graph" | "reranker" | "embeddings" | "other" | "n/a"],
  "mcp": "yes" | "no" | "unknown",
  "windows": "yes" | "no" | "unknown",
  "portuguese": "yes" | "no" | "unknown",
  "license": "<SPDX id or unknown>",
  "maturity": "stable" | "beta" | "alpha" | "archived" | "unknown",
  "doubt": true | false,
  "evidence": "<short quote(s) from the README backing serve, mcp and windows; max 200 chars>"
}
```

- "search" = it could be (part of) the search layer; "stack" = useful to another part of the hub; "none" =
  not useful to the hub (unrelated domain, cloud-only SaaS with no self-host, a course, a paper list...).
- "place": where it would run — on each machine's disk, inside the database's MCP server, as a network
  service, as a light copy in a remote client, or as a library to build with. Several allowed.
- "portuguese": "yes" only if the README says it supports Portuguese or is multilingual.
- "doubt": true when the README is too thin or ambiguous to judge "serve" with confidence.

## The project

```
{CARTAO}
```
