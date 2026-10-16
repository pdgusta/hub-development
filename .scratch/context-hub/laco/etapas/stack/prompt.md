You are sorting one software project into the part of a specific system it would serve. Use the card below (name,
role, evidence and, when present, the README, which is the primary source). Use general knowledge only to name the
area; never invent features.

## The system (the "hub")

A personal context hub: a folder of Markdown notes with YAML frontmatter, edited by a person in Obsidian and by AI
coding agents (Claude Code, Codex, GitHub Copilot) on two Windows machines (native NTFS, no WSL, no Docker). The
notes live in a CouchDB database on each machine (master-master replication); the Obsidian LiveSync plugin keeps
folders and database in sync. Agents read and write through an MCP server. Content is in Portuguese (pt-BR) and
English. A local OpenAI-compatible gateway can serve embeddings and LLM calls. Some clients reach the hub over a
tailnet; sandboxes have no tailnet. Search is handled elsewhere: here we only sort the rest of the stack.

## Areas (pick the main one, and optionally a second one)

- `sync_couchdb`: CouchDB, PouchDB, LiveSync, replication, change feeds, CouchDB clients.
- `mcp`: MCP servers, SDKs, proxies, gateways, registries.
- `markdown_frontmatter`: parsing Markdown or YAML frontmatter, chunking by heading, Markdown tooling.
- `text_pt`: language processing useful for Portuguese/multilingual text: stemmers, lemmatizers, tokenizers,
  accent folding, language detection, general NLP toolkits.
- `embeddings_rerank`: embedding or reranker models and the runtimes that execute them (ONNX, sentence models).
- `llm_runtime`: local LLM servers and gateways (Ollama, llama.cpp, LiteLLM, LocalAI).
- `text_extraction`: turning PDF, Office, HTML or images into text.
- `storage_db`: databases and stores other than CouchDB (SQLite, DuckDB, Redis, Postgres...).
- `events_jobs`: message queues, streams, pub/sub, file watchers, schedulers, background jobs.
- `api_service`: web/API frameworks to expose a service (FastAPI...).
- `agent_framework`: LLM app or agent frameworks, agent memory, RAG frameworks.
- `obsidian`: Obsidian itself, its plugin API and plugins.
- `other`: none of the above (say what in "hub_use").

## Answer

Reply with ONLY one JSON object, no prose, with exactly these keys:

```
{
  "area": "<one area id>",
  "area_2": "<another area id, or none>",
  "hub_use": "<what it would do in this hub, max 20 words>",
  "fit": "core" | "optional" | "unlikely",
  "doubt": true | false
}
```

- "fit": "core" = the hub would very likely need this kind of piece and this project fits the constraints
  (Windows native, local, light); "optional" = useful but replaceable or only for some cases; "unlikely" = heavy,
  cluster-scale, cloud-only, wrong platform, or off the hub's needs.
- "doubt": true when the card is too thin to sort with confidence.

## The project

```
{CARTAO}
```
