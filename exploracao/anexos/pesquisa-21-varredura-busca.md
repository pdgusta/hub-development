---
title: Pesquisa 21, varredura de candidatas à camada de busca
data: 2026-10-04
origem: subagente de pesquisa (Claude Code), ticket 21 "Varredura de candidatas à camada de busca"
aviso: saída de modelo. Fontes primárias: README e docs brutos (raw.githubusercontent.com), arquivos de CI e código-fonte pontuais, API REST do GitHub (metadados, commits, releases, árvore de arquivos), API do registry oficial de MCP, API Algolia do Hacker News e o README bruto do punkpeye/awesome-mcp-servers. Nada foi clonado, instalado ou executado. O que não foi conferido na fonte está marcado como **não verificado** (NV).
---

# Varredura de candidatas à camada de busca: levantamento de 04/10/2026

## Resumo (uma tela)

1. **Cobertura:** 48 consultas (18 web, 16 na API do GitHub, 9 no registry, 4 no HN, 1 lista awesome) em 7 frentes (busca web em 8 línguas, API de busca do GitHub, registry oficial de MCP,
   Hacker News, awesome-mcp-servers, Glama/Smithery/mcp.so via busca, Reddit e Product Hunt via busca). O vocabulário saiu
   de "vault Markdown" para "semantic grep", "local-first search for agents", "hybrid search CLI", "local-first RAG",
   "embedding grep/ripgrep" e equivalentes em chinês, japonês, coreano, alemão, espanhol e português.
2. **A lacuna existia.** A frente "semantic grep / busca local para agentes" tem ferramentas maduras que a varredura 3
   não viu: **BeaconBay/ck** (1.735 estrelas), **yoanbernabeu/grepai** (1.901), **mixedbread-ai/mgrep** (4.410),
   **kantord/SeaGOAT** (1.311), **scarletkc/vexor** (242). A maioria é feita para **código**, mas indexa `.md`.
3. **Triagem:** 19 candidatas novas conferidas na fonte (tabela da seção 3) e 25 de cauda longa só listadas (seção 4).
   Reapareceram 24 já conhecidas (seção 5).
4. **Melhores novas:**
   - **memtomem/memtomem**: o desenho mais próximo do hub. Markdown é a fonte da verdade, o banco é cache
     reconstruível, CI roda em `windows-latest`, modelo multilíngue por padrão e há um guia oficial de sincronização
     por git entre máquinas. Contra: 15 estrelas, projeto de março de 2026, escopo amplo de "memória".
   - **BeaconBay/ck**: o par mais maduro do zvec-grep (grep híbrido para humanos e agentes, binário Windows). Contra:
     só modelos em inglês, sem endpoint compatível com OpenAI, sem filtro de frontmatter, CI sem Windows.
   - **yoanbernabeu/grepai**: CI em Windows e endpoint compatível com OpenAI. Contra: feito para código, cortes por
     token e não por título, a parte "palavra" é contagem simples (não BM25), híbrido desligado por padrão.
5. **Recomendação (decisão do Gustavo):** levar **memtomem** ao spike como terceira candidata, ou como substituta do
   markdown-vault-mcp se o spike tiver de ficar com duas. **ck** fica como reserva, caso o zvec-grep falhe no
   Windows. Nenhuma das outras justifica entrar.

## 1. Consultas feitas (registro para auditoria)

### 1.1 Busca web (WebSearch; listagens de resultado, não fonte primária)

| # | Consulta | Língua | Alvo |
|---|---|---|---|
| W1 | semantic grep CLI local embeddings hybrid search MCP server github | en | GitHub geral |
| W2 | local-first search for AI agents markdown docs hybrid BM25 vector MCP Windows | en | geral |
| W3 | "semantic search" ripgrep alternative embeddings CLI agents 2026 | en | geral |
| W4 | 本地 语义搜索 markdown 文档 MCP 混合检索 BM25 向量 开源 | zh | geral |
| W5 | busca semântica local arquivos markdown agentes de IA MCP busca híbrida ferramenta open source | pt | geral |
| W6 | Show HN local hybrid search CLI for codebase and docs MCP embeddings | en | HN |
| W7 | "local-first RAG" notes markdown folder watcher MCP server embeddings OpenAI-compatible endpoint | en | geral |
| W8 | awesome-mcp-servers search "markdown" hybrid semantic local index file watcher | en | listas awesome |
| W9 | reddit LocalLLaMA tool semantic search my notes folder CLI embeddings BM25 MCP Claude Code 2026 | en | Reddit |
| W10 | Product Hunt local semantic search documents for AI agents MCP offline | en | Product Hunt |
| W11 | ローカル セマンティック検索 Markdown MCP ハイブリッド検索 CLI エージェント | ja | geral |
| W12 | lokale semantische Suche Markdown Notizen MCP Server hybride Suche Embeddings | de | geral |
| W13 | site:glama.ai mcp server hybrid search markdown folder local embeddings file watcher | en | Glama |
| W14 | smithery.ai OR mcp.so local semantic search markdown files BM25 embeddings server | en | Smithery, mcp.so |
| W15 | reddit r/ClaudeAI semantic search local docs MCP ck grepai qmd alternative Windows | en | Reddit |
| W16 | búsqueda semántica local notas markdown servidor MCP búsqueda híbrida embeddings Ollama | es | geral |
| W17 | single binary Rust local hybrid search markdown notes MCP Windows release tantivy embeddings | en | geral |
| W18 | 로컬 시맨틱 검색 마크다운 MCP 하이브리드 검색 BM25 임베딩 오픈소스 | ko | geral |

### 1.2 API de busca de repositórios do GitHub (`api.github.com/search/repositories`, ordem por estrelas)

| # | Consulta | Total |
|---|---|---|
| G1 | `semantic grep pushed:>2026-04-01` | 97 |
| G2 | `hybrid search mcp markdown pushed:>2026-04-01` | 83 |
| G3 | `"local-first" search agents pushed:>2026-04-01` | 642 |
| G4 | `topic:semantic-search topic:mcp pushed:>2026-04-01` | 1.196 |
| G5 | `embeddings ripgrep pushed:>2026-04-01` | 15 |
| G6 | `"hybrid search" cli docs local pushed:>2026-04-01` | 1 |
| G7 | `语义搜索 markdown MCP pushed:>2026-04-01` | 3 |
| G8 | `notes semantic search watch mcp pushed:>2026-04-01` | 0 |
| G9 | `topic:local-first topic:semantic-search pushed:>2026-04-01` | 671 |
| G10 | `documentation search mcp embeddings offline pushed:>2026-04-01` | 2 |
| G11–G16 | buscas por nome (`in:name`) para localizar repositórios citados em registros: local-knowledge-search, seeklink, vault-semantic-mcp, metamind-vault-rag, corpus-search-mcp, brain-mcp | — |

### 1.3 Registry oficial de MCP (`registry.modelcontextprotocol.io/v0/servers?search=`)

R1 `semantic`, R2 `hybrid`, R3 `markdown`, R4 `grep`, R5 `notes`, R6 `knowledge`, R7 `local-search` (vazio), R8 `vault`,
R9 `rag`. A busca do registry casa só o nome, e o resultado é ruidoso. O que trouxe de novo: `io.github.ArkNill/embgrep`
(repositório QuartzUnit/embgrep), `io.github.Stahldavid/sensegrep`, `io.github.bvolpato/ivygrep`,
`io.github.gronare/notes-vault-mcp`, `io.github.Abhishekkumar2021/notes`. `io.github.scarletkc/vexor` consta no README do
próprio vexor (`<!-- mcp-name: io.github.scarletkc/vexor -->`).

### 1.4 Hacker News (API Algolia, `tags=show_hn`, posts desde 01/01/2026)

H1 `semantic search local markdown` (16), H2 `hybrid search MCP` (33), H3 `semantic grep` (79), H4 `local search agents
notes` (32). Trouxe: nia-vault, Veles, context-harness, Recall Lite/Rememex, cgrep, next-plaid/colgrep,
obsidian-semantic-search (ravila4), darc, Traul, openground.

### 1.5 Lista awesome

README bruto de `punkpeye/awesome-mcp-servers` (4.541 linhas), filtrado por `semantic|hybrid|bm25|embedding` e
`markdown|notes|docs|files|grep|local|vault|folder`. Trouxe: scarletkc/vexor, epicsagas/alcove, dnotitia/akb,
ChrisGVE/workspace-qdrant-mcp, hyunjae-labs/lore, além de várias já conhecidas.

### 1.6 Fontes que só apareceram em listagens (não naveguei direto)

Glama, Smithery, mcp.so, mcpmarket, lobehub, Reddit e Product Hunt. **Reddit:** nenhuma consulta trouxe um tópico do
Reddit, só páginas de terceiros. **Product Hunt:** a busca trouxe só servidores MCP *do* Product Hunt; a única ponte é o
selo do Product Hunt no README do grepai.

## 2. Critérios usados na tabela

- **R1** arquivos no lugar (índice derivado, fora da pasta ou ignorável pelo git, reconstruível);
  **R2** híbrida palavra+sentido, retorno por trecho/título, filtro de frontmatter desejável;
  **R3** MCP de busca (gravar conferindo versão é bônus); **R4** Windows nativo no NTFS, sem WSL;
  **R5** acompanha edição externa e `git pull`; **R6** modelo local ou endpoint compatível com OpenAI;
  **R7** licença aberta e commit nos últimos 6 meses (desde 04/04/2026).
- **S** = sim, **P** = parcial, **N** = não, **NV** = não verificado.
- **Estrelas, licença, push, último commit e release:** API do GitHub em 04/10/2026. "Último commit" é o do ramo padrão.
- **pt-BR/multilíngue:** coluna informativa. Não elimina ninguém.

## 3. Candidatas novas conferidas na fonte

| # | Ferramenta | O que é | R1 | R2 | R3 | R4 | R5 | R6 | R7 | Licença | ★ | Último commit / release | pt-BR / multilíngue |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | **memtomem/memtomem** | Memória/busca "Markdown-first" para agentes; CLI, MCP, Web UI | S | S (frontmatter: P) | S | S | P | S | S | Apache-2.0 | 15 | 04/10/2026 / v0.6.6 (02/10) | **S**: `multilingual-e5-small` é o padrão ONNX; `bge-m3` opcional |
| 2 | **BeaconBay/ck** | "grep semântico" híbrido, CLI+TUI+MCP, Rust | S | P | S | S (binário; CI sem Windows) | S | S (local) | S | Apache-2.0 (README: MIT/Apache) | 1.735 | 09/07/2026 / 0.7.11 (24/05) | **N** por padrão (modelos em inglês); reranker `bge` multilíngue |
| 3 | **yoanbernabeu/grepai** | Busca semântica de código + grafo de chamadas, CLI+MCP, Go | S | P | S | **S** (CI `windows-latest`) | S | **S** (OpenAI-compatível) | S | MIT | 1.901 | 10/09/2026 / v0.37.0 (10/09) | S por configuração (`bge-m3`, `nomic-embed-text-v2-moe` via Ollama) |
| 4 | scarletkc/vexor | Busca semântica de arquivos, CLI+MCP+API Python | S | P | S | P (`.exe` no release; sem CI) | S | **S** (`custom` OpenAI-compatível) | S | MIT | 242 | 02/10/2026 / v0.30.0 (27/09) | P: tokenizador BM25 multilíngue; modelo à escolha |
| 5 | yoshihirosuzuki/mdya | "Primitiva de busca" para Markdown, CLI+MCP, Rust | S | P | S | **S** (zip msvc, instalador `.ps1`, smoke em `windows-latest`) | P (`update-all` manual) | S (local; Ollama) | S | Apache-2.0 | 1 | 02/10/2026 / v0.4.1 (20/08) | **N** por padrão (modelo e tokenizador japoneses); Ollama como saída |
| 6 | wirux/mcp-markdown-vault | MCP "headless" para pasta Markdown, com edição por AST (homônimo do pvliesdonk, outro projeto) | S (local do índice NV) | P | S (+ escrita) | NV (CI só ubuntu) | P | S (local; Ollama) | S | MIT | 12 | 03/10/2026 / v2.3.1 (03/10) | N por padrão (`all-MiniLM-L6-v2`) |
| 7 | parallax-labs/context-harness | Ingestão de fontes em SQLite + CLI `ctx` + MCP HTTP, Rust | P (ingere cópia) | P | S (só HTTP) | S (zip Windows; CI NV) | P (`ctx sync` manual) | S | P (AGPL) | AGPL-3.0 | 42 | 04/10/2026 / v0.8.0 (08/06) | NV |
| 8 | os-tack/ostk-recall | Busca e "recall" local para notas, código e sessões, Rust | S | S (frontmatter vira grafo, não filtro) | S | S (zip Windows; CI NV) | S (`serve --watch`) | S (local) | S | Apache-2.0 | 6 | 12/08/2026 / v0.9.5 (12/08) | N/NV (`potion-retrieval-32M`, inglês) |
| 9 | ambicuity/KINDX | Busca híbrida local CLI+MCP no molde do qmd, Node | S | S | S | NV | S (`kindx watch`) | **S** (GGUF ou OpenAI-compatível) | S | MIT | 0 | 17/08/2026 / v1.3.6 (09/06) | NV |
| 10 | benmaster82/Kwipu | GraphRAG sobre pasta de Markdown; terminal, web e MCP | NV | S | S | S (guia de instalação em PowerShell) | S (watcher) | P (só endpoint Ollama; LLM obrigatório) | S | MIT | 607 | 07/09/2026 / sem release | NV |
| 11 | devwhodevs/engraph | "Vault intelligence": busca em 5 vias + MCP, Rust | S | S | S | **N** (binários só macOS arm64 e Linux) | S | S (local) | S | MIT | 171 | 27/05/2026 / v1.7.2 | P ("model overrides for multilingual") |
| 12 | Furkiozknn/local-notes-search-mcp | MCP de busca semântica em pastas | S | P (só semântico) | S | S (autor mediu no Windows 11) | P | S (local) | S | MIT | 0 | 30/09/2026 / sem release | **S** (`paraphrase-multilingual-MiniLM-L12-v2`) |
| 13 | gronare/notes-vault-mcp | MCP para vault com esquema de frontmatter | S | P (só BM25) | S | NV | NV | — | S | MIT | 0 | push 03/10/2026 | — |
| 14 | QuartzUnit/embgrep | grep por embedding + MCP | S | P (só semântico) | S | NV | P (`update` manual) | S (local) | P (último push 15/04/2026) | MIT | 0 | — | N (`bge-small-en-v1.5`) |
| 15 | mixedbread-ai/mgrep | grep semântico da Mixedbread | **N** (índice no "Mixedbread store", na nuvem) | S | P | NV | S | **N** (API da Mixedbread) | S | Apache-2.0 | 4.410 | push 25/04/2026 | NV |
| 16 | kantord/SeaGOAT | Busca semântica de código com servidor local | S | P | **N** (README sem MCP) | **N** (Windows "help needed") | S | S (Ollama) | S | MIT | 1.311 | push 04/10/2026 | NV |
| 17 | jina-ai/jina-grep-cli | grep semântico com MLX | S | P | NV | **N** ("Apple Silicon Mac") | — | S | S | Apache-2.0 | 248 | push 13/05/2026 | S (Jina v5) |
| 18 | martintrojer/vecgrep | "ripgrep com vetores" | S | S (`--hybrid`) | **N** (README sem MCP) | NV | NV | S (Ollama, LM Studio, OpenAI-compatível) | S | MIT | 11 | push 12/09/2026 | NV |
| 19 | XiaoConstantine/sgrep | Busca semântica/híbrida de código e histórico | S | S | **N/NV** (README cita hooks, não MCP) | NV | S (watch) | NV | S | Apache-2.0 | 15 | push 19/09/2026 | NV |

### Evidências por linha (citações da fonte primária)

**1. memtomem**
- R1: *"Your `.md` files are the source of truth. The DB is a rebuildable cache"* (README). O banco fica em
  `~/.memtomem/memtomem.db` (`MEMTOMEM_STORAGE__SQLITE_PATH`, docs/guides/configuration.md). Há
  `indexing.read_only_memory_dirs` para *"roots that are indexed but never rewritten"*.
- R2: *"Hybrid search — BM25 keyword + dense vector + RRF fusion in one query"* e *"Semantic chunking —
  heading-aware Markdown"* (README). Filtros: *"Selection filters — `tag_filter`, chunk types, created-date"*
  (configuration.md). Filtro por campo arbitrário do frontmatter: **NV**.
- R3: servidor `memtomem-server`, registrado com `claude mcp add memtomem ...`; tem plugin para Codex (README). Gravar
  conferindo versão: **NV**.
- R4: `.github/workflows/ci.yml` tem os jobs `test-windows-shard` e `test-windows`, com `runs-on: windows-latest`.
- R5: o watcher *"reindexes files when the filesystem emits modify / create / move events"*, e quando a fila estoura ele
  *"rescans that root"*. Ressalva: *"Pre-existing files on disk at the time the watcher starts are NOT auto-scanned"*;
  a semeadura é por `mm index <dir>`, que é idempotente (configuration.md). O guia multi-device-sync.md manda encerrar
  o cliente MCP antes do `git pull`, *"or trust `startup_backfill` on the next launch"*. Mas a configuração descreve
  `MEMTOMEM_INDEXING__STARTUP_BACKFILL` (padrão `false`) como algo que vale para *"`mm web`"*. Se vale também para o
  servidor MCP, as duas fontes não deixam claro: **NV**.
- Sincronização entre máquinas: há guia oficial, *"keep the markdown in a private git repo, leave the database local,
  and let `git pull` carry edits between machines"* (docs/guides/multi-device-sync.md).
- R6: provedores `onnx` (local), `ollama` e `openai`, mais `MEMTOMEM_EMBEDDING__BASE_URL` (*"API endpoint URL"*,
  configuration.md). Se esse campo aceita um endpoint OpenAI-compatível de terceiros (FreeLLMAPI): **NV**.
- pt-BR: *"`provider=onnx` with no model selects `multilingual-e5-small`"*. A doc cita só *"KR/EN/JP/CN"*; o português
  não é citado (docs/guides/embeddings.md).

**2. ck**
- R1: *"Indexes are stored in `.ck/` directories alongside your code"*, *"The `.ck/` directory is a cache — safe to
  delete"*, e `CK_INDEX_DIR` *"to keep indexes out of your source tree entirely"* (README).
- R2: modos `--sem`, `--hybrid` e regex. Para Markdown, a tabela de linguagens diz *"Headings, sections, code blocks"*.
  Não há filtro de frontmatter no README.
- R3: ferramentas MCP `semantic_search`, `regex_search`, `hybrid_search`, `index_status` e `reindex` (README). Nenhuma
  grava.
- R4: o release 0.7.11 traz `ck-0.7.11-x86_64-pc-windows-msvc.zip` (API de releases). O CI (`ci.yaml`) roda em
  `["ubuntu-latest", "macos-latest"]`, sem Windows.
- R5: *"Semantic and hybrid searches transparently create and refresh their indexes before running"*, com
  *"Chunk-level incremental indexing"*. É reconciliação na hora da busca, não watcher.
- R6: o código `ck-embed/src/lib.rs` só aceita os provedores `"fastembed"` e `"mixedbread"`. Não há endpoint
  OpenAI-compatível. Os modelos do registro (`ck-models/src/lib.rs`) são `BAAI/bge-small-en-v1.5`, `all-MiniLM-L6-v2`,
  `nomic-embed-text-v1.5`, `jina-embeddings-v2-base-code` e `mxbai-embed-xsmall-v1`.
- R7: último commit no `main` em 09/07/2026 (o `pushed_at` de 30/09 vem de outros ramos).

**3. grepai**
- R2: *"Hybrid search combines vector similarity with text matching using Reciprocal Rank Fusion"*, mas está
  *"Disabled by default"*, e a parte textual é *"Simple keyword matching"*, pontuada por *"`matches / total_words`"*
  (docs/hybrid-search.md). O corte é por tamanho (`chunking: size: 512, overlap: 50`, configuration.md), não por
  título. Indexa `.md`: `".md": true` em `SupportedExtensions` (indexer/scanner.go).
- R1: índice padrão em `.grepai/index.gob` (docs/backends/stores.md). Se `.grepai/` entra sozinho no `.gitignore`:
  **NV**.
- R3: ferramenta `grepai_search`, além das de grafo de chamadas (docs/mcp.md).
- R4: o CI tem a matriz `os: [ubuntu-latest, macos-latest, windows-latest]`; há instalador PowerShell e zips
  `windows_amd64`/`windows_arm64`.
- R5: `grepai watch` faz o *"Initial scan: Compares disk state with existing index, removes obsolete entries, indexes new
  files"* e depois monitora em tempo real (docs/watch-guide.md). Exige o daemon rodando.
- R6: *"For Azure OpenAI or other OpenAI-compatible providers, use a custom endpoint"* (docs/backends/embedders.md).

**4. vexor**
- R2: a busca é semântica; o híbrido é uma etapa de rerank (`vexor config --rerank hybrid  # optional: fuse exact
  keyword + semantic ranking`, README). Markdown no modo `outline`: *"Chunk Markdown by heading hierarchy with
  breadcrumbs"* (docs/cli.md).
- R6: *"`custom` is OpenAI-compatible and requires both `model` and `base_url`"*, e há um provedor `local`
  (docs/configuration.md).
- R4: o release v0.30.0 traz `vexor-0.30.0-windows.exe`. Os workflows do repositório são só `conventional-commits.yml`
  e `publish.yml`, sem testes em Windows.

**5. mdya**
- *"BM25 full-text search … Vector search … Hybrid search — fuses BM25 and vector results via Reciprocal Rank Fusion"*,
  *"Markdown chunking — splits along heading and code-fence boundaries"*, *"MCP server — `mdya mcp` (stdio / HTTP)"*
  (README).
- O modelo padrão é *"`cl-nagoya/ruri-v3-30m` (256 dimensions, strong for Japanese)"*; o BM25 usa *"Japanese
  morphological analysis (lindera/ipadic)"*. Aceita `ollama:<name>` (docs/manual/en/configuration.md).
- R5: o fluxo é `collection add` → `update-all`. Não há watcher no README nem no manual de MCP.
- 1 estrela; criado em 06/2026.

### Leitura rápida das demais

- **wirux/mcp-markdown-vault:** a busca é *"cosine-similarity vectors + TF-IDF + word proximity"*. Mudança fora do MCP
  pede reindexação manual: *"`system.reindex`: Only use this for recovery or after making out-of-band file changes"*
  (README). Isso fere R5.
- **context-harness:** *"ingests external knowledge … into a local SQLite store"*; a atualização é por `ctx sync`. O MCP
  só existe por HTTP (`ctx serve mcp`, endpoint `/mcp`). A licença é AGPL-3.0.
- **ostk-recall:** *"Pre-alpha but functional"*. O Markdown é *"split on headings, soft-wrap ~400 tokens"*; `serve
  --watch` mantém o índice. O modelo padrão é `minishlab/potion-retrieval-32M` (README).
- **KINDX:** *"local-first hybrid CLI/MCP search engine … combining BM25, vector retrieval, and LLM reranking … or use an
  OpenAI-compatible remote backend"*. A pasta `training/` é *"a separate Python project named `qmd-finetune`"*, o que
  sugere que derivou do qmd. O GitHub não marca o repositório como fork. Tem 0 estrelas.
- **Kwipu:** *"The intentional default LLM is `gpt-oss:20b-cloud`"*. Extrai relações com um LLM, então o LLM é parte do
  índice. Pesado demais para o papel de camada de busca.
- **engraph:** *"Pre-built binaries (macOS arm64, Linux x86_64)"*; o CI roda em *"macOS + Ubuntu"*. Fora por R4.

## 4. Cauda longa (só listadas; nada conferido além da descrição, tudo NV)

Projetos com 0 a 11 estrelas ou focados só em código. Ficam registrados para auditoria:

- **Markdown/notas + MCP híbrido, muito novos:** komplettsystem/local-knowledge-search (0★, sem licença no GitHub),
  simonsysun/seeklink (11★, MIT; reranker MLX), eman-hc/vault-semantic-mcp (0★, sem licença; embeddings da OpenAI),
  Nikitzu/metamind-vault-rag (0★, MIT), TheBitcoinBreakdown-95/corpus-search-mcp (0★, MIT), Artur0927/brain-mcp (0★,
  MIT), sysangel/brain-mcp (0★, MIT), sanqiuyef/lancedb-search-mcp (0★, criado em 03/10/2026), Eridanus117/memex
  (**arquivado**), yyh2003-10/DocMind, wshsds00/WSnote, MaybeJustLikeThis/Maybe-kb, 425732441/Kzone,
  raymond89huang-prog/local-knowledge-rag-mcp, ravila4/obsidian-semantic-search (19★; só CLI), bborbe/semantic-search-mcp,
  Ethan2298/personal-semantic-search-mcp, Abhishekkumar2021/mcp-suite (notes).
- **Sem embeddings ou sem MCP:** vdmk/tantivy-markdown-mcp (*"no embeddings"*, só Linux/macOS), epicsagas/alcove (só
  BM25), docsagent/docsagent (625★, **sem licença**, BM25 em C++), Mandoa-Labs/BM-25-Search.
- **Busca de código (AST/tree-sitter), fora do perfil do hub:** zilliztech/claude-context, probelabs/probe,
  officialalexeev/anyindex-mcp, yashharkawat/codebase-copilot, brandyn-s/code-search, flupkede/codesearch,
  julymetodiev/Veles, lightonai/next-plaid (colgrep), Stahldavid/sensegrep, bvolpato/ivygrep, CodeBendKit/codeseek.
- **Memória de agente com base própria (classe da Guild):** yoloshii/ClawMem (Windows só via WSL2, pelo README),
  SpillwaveSolutions/agent-brain, edwin-hao-ai/Awareness-Local, jordiboehme/crystalline, mraza007/echovault,
  liliu-z/stashbase (app de escrita; busca semântica exige chave OpenAI/OpenRouter).

## 5. Já conhecidas que reapareceram (não reavaliadas)

qmd (tobi/qmd, mais o fork ehc-io/qmd), markdown-vault-mcp (pvliesdonk), grooveseek, obsidian-hybrid-search, mcp-ragdown,
MCP-Markdown-RAG (Zackriya), ragdocs-mcp (andnp), mcp-local-rag (shinpr, mais o fork tmnd1991), knowledge-rag (lyonzin),
memo (jagoff), local-rag (QuverLabs), sqlite-memory (via local-rag), basic-memory, haypile, gnosis-mcp, devrag, agentcairn,
vault-cortex, obsidian-semantic-mcp (DalecB), enquire-mcp, stellavault, freshvault, maxkuminov/obsidian-mcp, NOUZ-MCP,
khoj, guild, cyanheads/obsidian-mcp-server, **zvec-grep** (G3, G4, G9 e a busca W3). O turbovec não reapareceu.

## 6. As melhores novas

### memtomem: a única nova que encosta em R1–R7 com Windows testado

- **Por que se destaca:**
  - A filosofia é a do hub: *"Your `.md` files are the source of truth. The DB is a rebuildable cache"*.
  - É a única candidata (velha ou nova) com **guia oficial de sincronização por git entre máquinas**, que separa o que
    vai para o git (`.md`) do que fica local (`*.db`, configuração).
  - Tem **CI em Windows** (`windows-latest`). O markdown-vault-mcp não tem (§10.4.1 da exploração).
  - O modelo padrão é multilíngue, e há raízes **só leitura** (`read_only_memory_dirs`), o que casa com "o hub é a fonte".
- **Riscos:**
  - 15 estrelas e um projeto de março de 2026, com versão 0.6.x.
  - O escopo é amplo (memórias, sessões, Web UI, LLM opcional, plugins). A camada de busca usaria uma fração dele.
  - O watcher não varre na partida: depois de um `git pull` com o servidor parado, é preciso `mm index` ou confiar no
    `startup_backfill`, cuja abrangência é **NV**.
  - O endpoint OpenAI-compatível para o FreeLLMAPI é **NV**.

### ck: o equivalente maduro do zvec-grep, mas preso ao inglês

- **Por que se destaca:**
  - 1.735 estrelas.
  - Binário Windows oficial.
  - Busca híbrida com cortes por título em Markdown.
  - O índice é cache descartável e pode morar fora da pasta (`CK_INDEX_DIR`).
  - Reconcilia sozinho antes de cada busca, então `git pull` e edição externa ficam cobertos sem daemon.
- **Riscos:**
  - Só modelos em inglês; nenhum embedding multilíngue.
  - Não tem endpoint OpenAI-compatível (só FastEmbed local ou a API da Mixedbread).
  - Não filtra por frontmatter.
  - O CI não roda em Windows.
  - O foco declarado é código.

### grepai: Windows e FreeLLMAPI resolvidos, mas busca fraca para Markdown

- **Por que se destaca:** CI em Windows, endpoint OpenAI-compatível documentado e watcher com reconciliação na partida.
- **Contra:**
  - Os cortes são por token, não por título.
  - A parte "palavra" não é BM25 e vem desligada por padrão.
  - O produto é feito para código (grafo de chamadas).

## 7. Recomendação (a decisão é do Gustavo)

- **memtomem deve disputar o spike.** Recomendo incluí-lo como terceira candidata ao lado de markdown-vault-mcp e
  zvec-grep. Se o spike tiver de ficar com duas, ele disputa a vaga do **markdown-vault-mcp**: ocupa o mesmo nicho
  (Markdown como fonte, MCP, híbrida, filtros) e tem o que falta ao markdown-vault-mcp, que é teste em Windows e guia de
  git entre máquinas.
- **No spike, conferir dois pontos que ficaram NV:**
  1. se o servidor MCP reindexa sozinho, na partida, o que um `git pull` trouxe;
  2. se `BASE_URL` aceita o FreeLLMAPI.
- **ck fica de reserva** para a vaga do zvec-grep: só entra se o zvec-grep falhar no Windows. Os modelos em inglês e a
  falta de endpoint OpenAI-compatível pesam contra ele num hub em português.
- **As demais não entram:** grepai (feito para código, busca textual fraca), vexor (híbrido só como rerank), mdya
  (japonês, sem watcher, 1 estrela), wirux (reindexação manual após edição externa), context-harness (AGPL, ingestão
  manual), ostk-recall (pré-alfa, modelo em inglês), KINDX (0 estrelas, Windows NV), Kwipu (exige LLM) e engraph (sem
  Windows).

## 8. Limites

- **Nada foi instalado nem executado.** O suporte a Windows vem de CI, artefatos de release e READMEs.
- **Cota da API do GitHub sem autenticação** (60 chamadas por hora): só as 9 primeiras da tabela tiveram último commit e
  release conferidos. Nas outras, a data é o `pushed_at` do repositório.
- **Reddit e Product Hunt** só apareceram por listagens de terceiros, sem nenhum tópico direto. Glama, Smithery e mcp.so
  também só por listagem.
- **Qualidade de busca, e em português em especial, não foi medida em nenhum caso.** "Multilíngue" quer dizer só que o
  modelo padrão declara ser multilíngue.
- **Cobertura:** o ecossistema de "MCP de busca local" cresce rápido; a cauda longa (seção 4) tem dezenas de projetos de
  0 estrela que não foram abertos.
