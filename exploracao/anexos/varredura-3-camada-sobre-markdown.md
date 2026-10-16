---
title: Relatório de varredura (texto integral do agente)
data: 2026-09-29
origem: subagente da sessão 3be42b76 (Claude Code, workspace TRF3)
aviso: saída de modelo; afirmações principais conferidas na seção 10 da exploração
---

## Camadas de contexto MCP sobre um vault Markdown: levantamento de 29/09/2026

**Resumo:** achei 47 ferramentas e conferi 45 no README ou na documentação de cada uma. Só uma cumpre R1 a R6 juntos no papel: pvliesdonk/markdown-vault-mcp, que já estava na lista. Nenhuma delas tem uso comprovado no Windows. As duas melhores alternativas novas são **grooveseek** (binário em Rust com build para Windows, só leitura) e **obsidian-hybrid-search** (CI roda em Windows, modelo multilíngue por padrão). Uma descoberta muda o quadro das já conhecidas: **mathomhaus/guild não serve para R1**. Ela não indexa arquivos .md; guarda o estado em SQLite em `~/.guild`. E no Windows a busca vetorial vem desativada ("On Windows, semantic (vector) retrieval is currently disabled").

**Como coletei:**
- **Estrelas:** tiradas da página HTML do GitHub em 29/09/2026.
- **Último release:** do `releases.atom`. "—" quer dizer sem release no GitHub; pode haver pacote no npm ou no PyPI.
- **Atividade:** último commit, do `commits.atom`.
- **Legenda:** S = sim, P = parcial, N = não, NV = não verificado.

### Tabela

| # | Nome | Link | O que é | R1 arquivos in place | R2 híbrida/seção/frontmatter | R3 MCP | R4 local + Windows | R5 2 máquinas / índice reconstruível | R6 escrita segura | Licença | ★ | Último release (último commit) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | markdown-vault-mcp *(conhecida)* | github.com/pvliesdonk/markdown-vault-mcp | MCP genérico para um vault Markdown | S (`SOURCE_DIR` aponta para o vault) | S: FTS5 BM25 + FastEmbed/Ollama com RRF; campos do frontmatter filtráveis; chunks por título | S (34 ferramentas) | P: FastEmbed local; o CI roda só em ubuntu e não há menção a Windows | S: integração git opcional (auto-commit, loop de pull); reindexação incremental por hash | **S**: `READ_ONLY=true`; etag via `if_match`; `WRITE_PROTECT_EXISTING=true` por padrão | MIT | 34 | 5.0.0 em 27/09/2026 (28/09) |
| 2 | guild *(conhecida)* | github.com/mathomhaus/guild | Memória e tarefas para agentes, binário Go | **N** (lore fica em SQLite `~/.guild`) | P: BM25+vetor com RRF, mas no Windows só BM25 | S | P: CI diz "Windows tests are not run" | N (estado local por máquina) | NV | Apache-2.0 | 302 | 0.3.2 em 12/06/2026 (26/08) |
| 3 | qmd | github.com/tobi/qmd | Buscador local: CLI + MCP | S (índice em `~/.cache/qmd`) | P: BM25+vetor+rerank por LLM; filtro só com bloco `qmd.metadata` no frontmatter | S (stdio/HTTP) | P: GGUF local; issue #31 sobre Windows fechada como "not planned"; issues #672 e #969 mostram falhas no Win11 | S: índice fora do vault; `update-cmd 'git pull --rebase'` | S (só leitura: query/get/multi_get) | MIT | 30.101 | v2.8.3 em 16/08/2026 (09/09) |
| 4 | basic-memory | github.com/basicmachines-co/basic-memory | Memória/grafo em Markdown | S* (aponta para um vault existente; permalinks passaram a ser obrigatórios no PR #1477 de 05/09/2026; não confirmei se ele grava frontmatter nos seus arquivos) | S: FTS + vetor FastEmbed, rerank opcional; filtros NV | S | S: Windows listado; vários fixes de Windows | P: localmente o sync é por sua conta (Git/Syncthing); a nuvem paga tem sync com conflitos | P: `write_note` "guards against accidental overwrites"; sem etag | AGPL-3.0 | 4.062 | v0.23.2 em 25/08/2026 (29/09) |
| 5 | **obsidian-hybrid-search** | github.com/flowing-abyss/obsidian-hybrid-search | CLI + MCP + plugin do Obsidian | S | S: BM25+fuzzy+semântico com RRF; chunks por título; `--frontmatter` no CLI (no MCP só scope/tag) | S | **S**: CI em windows-latest; multilingual-e5-small offline | P: DB `.obsidian-hybrid-search.db` fica **dentro** do vault, precisa ser ignorado no sync | S (MCP só search/read/reindex/status) | MIT | 107 | v0.16.0 em 29/09/2026 |
| 6 | **grooveseek** | github.com/alphabet-h/grooveseek | Servidor MCP em Rust (binário único) | S (`.groove.db` no diretório **pai** do vault) | **S**: FTS5 + sqlite-vec; chunks por título; filtros `fields` do frontmatter, tags, datas e path | S (6 ferramentas) | **S**: zip `x86_64-pc-windows-msvc`, ONNX estático; modelo padrão em inglês (usar `--model bge-m3` para PT) | S: o watcher cobre `git pull`; `index --force` reconstrói | S (nenhuma ferramenta de escrita) | MIT OR Apache-2.0 (README; o GitHub mostra NOASSERTION) | 8 | 1.13.0 em 23/09/2026 (26/09) |
| 7 | vault-cortex | github.com/aliasunder/vault-cortex | MCP completo para Obsidian | S | S: FTS5 BM25+vetor com RRF + cross-encoder; filtros de tag/pasta/propriedade/data | S | P: local só via Docker; Windows com Docker Desktop + `WINDOWS_MODE`; modelos locais (~45 MB) | P: índice DuckDB reconstruível; modo remoto depende de Obsidian Sync | P: `READONLY_MODE`; `write_note` falha se o arquivo existe; sem etag | MIT | 21 | v0.54.3 em 26/09/2026 |
| 8 | obsidian-semantic-mcp | github.com/DalecB/obsidian-semantic-mcp | Busca só leitura | S | S: chunks por título + FTS5 + vetor bge-m3; filtros NV | S (no registry oficial) | S: Ollama; instruções para Windows | S (SQLite fora do vault) | S (só leitura) | MIT | 1 | v0.3.1 em 06/08/2026 |
| 9 | mcp-ragdown | github.com/cubicecho/mcp-ragdown | MCP + hook para Claude Code | S | S: BM25+denso com RRF por seção; filtros tag/path; do frontmatter só tags e aliases | S | P: Node 26+, ONNX local; Windows NV | S (índice em `~/.cache/ragdown`) | **S**: `READ_ONLY` + `base_hash` nas edições | **sem licença** | 0 | v5.9.0 em 25/09/2026 |
| 10 | qkb | github.com/miguelarios/qkb | Busca híbrida para Obsidian | S ("read-only to qkb") | S: FTS5+sqlite-vec; filtros `fields`/tags/data no MCP | S | P: node-llama-cpp; Windows NV (CI ubuntu) | S (DB em `~/.local/share/qkb`) | S | MIT | 0 | v0.6.0 em 24/09/2026 |
| 11 | enquire-mcp | github.com/oomkapwn/enquire-mcp | MCP para Obsidian com PDF | S | S: BM25+TF-IDF+embeddings com RRF, rerank BGE; busca por frontmatter | S | S? (issues de CI e segurança de arquivos no Windows, todas fechadas) | NV | S: só leitura por padrão; escrita exige `--enable-write` | MIT | 33 | v4.0.0-rc.6 em 30/08/2026 (pré-release) |
| 12 | agentcairn | github.com/ccf/agentcairn | Memória de agente sobre vault | P (vault canônico; indexar um vault arbitrário é NV) | S: BM25+vetor com RRF + rerank; nomic local | S | P (Windows só no selo da awesome-list; CI ubuntu) | S (`.duckdb` fora do vault) | P (lock de escritor único) | Apache-2.0 | 60 | v0.26.2 em 28/09/2026 |
| 13 | obsidian-mcp (lstpsche) | github.com/lstpsche/obsidian-mcp | MCP em Rust, leitura e escrita | S | P: BM25 Tantivy; semântico separado; híbrido via `lexical_prefetch` + alpha | S | S (binários Windows com embeddings locais) | P: cache padrão `{vault}/.obsidian-mcp` (configurável) | P (toolset `read`; sem etag) | MIT | 34 | v3.1.0 em 07/09/2026 |
| 14 | memsearch | github.com/zilliztech/memsearch | Memória Markdown + Milvus | S | S: denso + BM25 com RRF | **N** (o plugin diz "no MCP servers": CLI+skill+hooks) | P: ONNX bge-m3; Milvus Lite no Windows NV | S (índice sombra reconstruível) | — | MIT | 2.681 | v0.4.21 em 24/09/2026 |
| 15 | mcp-local-rag | github.com/shinpr/mcp-local-rag | RAG local (LanceDB) | P (ingere em LanceDB; tem sync de diretório) | P (semântico + "keyword boost") | S | S? (Transformers.js; Windows NV) | S | P (só mexe no índice) | MIT | 404 | v0.19.1 em 22/09/2026 |
| 16 | knowledge-rag | github.com/lyonzin/knowledge-rag | RAG local (ChromaDB) | P (pasta `documents_dir`) | S (BM25+semântico+rerank; frontmatter NV) | S | S (CI em Windows/Linux/macOS; FastEmbed) | S | P | MIT | 288 | v4.9.1 em 28/09/2026 |
| 17 | smart-connections-mcp | github.com/msdanyg/smart-connections-mcp | Lê embeddings do Smart Connections | S | N (só semântico) | S | P (depende do plugin gerar os embeddings) | P | S (só leitura) | MIT | 57 | v2.0.1 em 22/08/2026 |
| 18 | vault-vector (PT-BR) | github.com/All-zen/vault-vector | Busca e escrita, em português | S | P: FTS5+vetor com RRF por título; **sem filtro de frontmatter** | S | S ("Testado no Windows"; Ollama bge-m3) | P (backup em `_historico/`) | P (histórico, sem etag) | MIT | 0 | — (16/09) |
| 19 | vault-mcp (videnovnebojsa; fork Ayorinha) | github.com/videnovnebojsa/vault-mcp | MCP para Obsidian (Bun) | S | S (híbrida; filtros tag/type/data) | S | S (`install.ps1`) | NV | NV | MIT | 2 | v0.2.2 em 03/06/2026 |
| 20 | haypile | github.com/BenyD/haypile | Busca em documentos (Go) | S (pastas observadas) | S (FTS5+vetor com RRF; frontmatter NV) | S (2 ferramentas) | S (instalador PowerShell; modelo embutido) | S | S | AGPL-3.0 | 2 | v0.3.1 em 07/08/2026 |
| 21 | quillrag | github.com/Ayush-yadav11/quillrag | RAG em binário Rust | S | P (denso+BM25 com RRF; MiniLM em inglês) | S | S (build Windows) | S | NV | MIT | 3 | v0.1.6 em 17/09/2026 |
| 22 | kx (PT-BR) | github.com/distu/kx | Índice local para agentes | S | P (sqlite-vec+FTS5 com RRF; MiniLM em inglês) | S | S? | S | NV | MIT | 5 | — (11/09) |
| 23 | stellavault | github.com/Evanciel/stellavault | App desktop + MCP | S | S (RRF ponderado: semântico+BM25+entidades) | S | S (zip para Windows) | NV | NV | MIT | 5 | v0.9.0 em 25/08/2026 |
| 24 | gnosis-mcp | github.com/nicholasglazer/gnosis-mcp | Busca em docs | P (ingest para SQLite/PG) | S (BM25+ONNX) | S | NV | S (`--prune`, `--wipe`) | NV | MIT | 29 | v0.17.5 em 11/09/2026 |
| 25 | mnemonic | github.com/danielmarbach/mnemonic | Memória em Markdown via git | P (vault próprio + fontes externas só leitura) | S | S | P (Ollama; Windows NV) | **S** (git nativo; embeddings no .gitignore) | P (commit por escrita) | Apache-2.0 | 30 | v0.47.1 em 28/09/2026 |
| 26 | freshvault | github.com/KIOKO-LAB/freshvault | Busca só leitura | S | P (BM25 desligado por decisão de projeto) | S | P (Ollama) | S | S | MIT | 0 | v0.4.0 em 06/08/2026 |
| 27 | maxkuminov/obsidian-mcp | github.com/maxkuminov/obsidian-mcp | MCP self-hosted | S | P (keyword e semântico são ferramentas separadas) | S | **N** ("Windows hosts are out of scope"; Postgres+Docker) | S | S (`expected_hash`) | MIT | 15 | v0.8.3 em 27/09/2026 |
| 28 | cyanheads/obsidian-mcp-server | github.com/cyanheads/obsidian-mcp-server | MCP via Local REST API | P (exige Obsidian aberto) | N (texto/BM25 Omnisearch; semântica ainda é só a issue #72) | S | S | — | P | Apache-2.0 | 687 | v3.6.0 em 23/09/2026 |
| 29 | MCPVault | github.com/bitbonsai/mcpvault | MCP de arquivos para Obsidian | S | N (só BM25) | S | S | — | S (`--read-only`) | MIT | 1.675 | — (26/08) |
| 30 | obsidian-mcp-connector | github.com/istefox/obsidian-mcp-connector | Plugin MCP dentro do Obsidian | P (exige Obsidian aberto) | P (semântico on-device; híbrido NV) | S | S (ponte para Windows) | NV | NV | MIT | 93 | 2.7.0 em 14/09/2026 |
| 31 | khoj | github.com/khoj-ai/khoj | "Second brain" self-hosted | P (sincroniza para o próprio servidor) | P | **NV** (README sem MCP oficial; entradas de marketplace são de terceiros) | P | — | — | AGPL-3.0 | 37.533 | 2.0.0-beta.28 em 26/03/2026 |

**Descartadas, mas registradas:**

| Ferramenta | Motivo | Licença / ★ |
|---|---|---|
| cxrobx/vault-mcp | Só macOS/Linux | MIT / 0 |
| St0nefish/mcp-md-wiki | Docker + Qdrant | AGPL / 0 |
| everton-dgn/vault-search-mcp | Python 3.14; "Windows does not yet have … CI coverage" | MIT / 0 / v0.1.0 |
| Cazy00/brain | Sem busca semântica | MIT / 0 |
| noesskeetit/second-brain-mcp | Windows não testado | MIT / 6 |
| ddmanyes/second-brain-mcp | Estrutura de vault opinativa | MIT / 6 |
| QuverLabs/local-rag | Sem licença | — / 0 |
| GCamposGit/SegundoCerebro | PT-BR, LanceDB+FTS5; pouco maduro | MIT / 0 |
| andnp/ragdocs-mcp | FAISS+Whoosh | MIT / 2 |
| Rajaguhan437/obsidian-mcp-semantic-metagraph | Fork do lstpsche; híbrido desligado | MIT / 1 |
| sqliteai/sqlite-memory | Extensão SQLite; MCP fica num projeto separado | licença NOASSERTION / 122 |
| Zackriya-Solutions/MCP-Markdown-RAG | Só semântico; inativo desde 07/2025 | Apache / 61 |
| tomohiro-owada/devrag | Só vetorial; licença não detectada | — / 64 |
| Minhao-Zhang/obsidian-mcp-server | Plugin; só semântico; filtro de frontmatter ainda em TODO | AGPL / 14 |
| jagoff/memo | Sem Windows | MIT / 19 |
| KVANTRA-dev/NOUZ-MCP | Não aprofundei | MIT / 21 |

### Top 3 para os seus requisitos

1. **pvliesdonk/markdown-vault-mcp**
   - **Por quê:** é a única que junta tudo:
     - busca híbrida BM25+vetor;
     - filtro por frontmatter;
     - chunk por título;
     - modo só leitura **e** etag com `if_match`, com proteção contra sobrescrita ligada por padrão;
     - integração git opcional.
   - **Riscos:**
     - Windows sem teste no CI (só ubuntu). É pip/Python, mas o uso real no Windows não está verificado.
     - Mudanças rápidas: a 5.0.0, uma versão major, saiu há 2 dias.
     - Uma pessoa só mantém; 34★.
     - Há bug aberto de reindexação O(N²) (issue #1535).

2. **alphabet-h/grooveseek**
   - **Por quê:**
     - binário único com build oficial para Windows (ONNX e SQLite estáticos);
     - chunk por título e filtros de frontmatter (`fields`/`fields_not`);
     - MCP sem nenhuma ferramenta de escrita, o que já resolve R6;
     - índice fora do vault;
     - o watcher cobre `git pull`.
   - **Riscos:**
     - 8★, mantenedor único.
     - O modelo padrão é em inglês: para notas em PT, `--model bge-m3` no index e no serve.
     - Se um dia precisar de escrita, não tem.

3. **flowing-abyss/obsidian-hybrid-search**
   - **Por quê:**
     - o CI roda em windows-latest;
     - o modelo padrão é multilíngue e offline;
     - o MCP é só leitura;
     - chunk por título; tem plugin do Obsidian e CLI.
   - **Riscos:**
     - O DB fica **dentro** do vault. Tem que excluí-lo do git e do Obsidian Sync, e cada máquina reconstrói o seu.
     - O filtro de frontmatter existe no CLI, mas não aparece nos parâmetros do MCP.
     - 107★.

**Outras que valem considerar:**
- **qmd:** de longe a mais madura (30k★), mas o Windows não tem suporte oficial.
- **basic-memory:** madura e com Windows, mas AGPL, tem formato próprio, não tem etag e pode mexer no frontmatter (não verifiquei).
- **mcp-ragdown:** o desenho de R6 é ideal (`base_hash` + só leitura), mas **não tem licença** e exige Node 26.
- **DalecB:** só leitura com Ollama, simples, porém 1★.

**Sobre R5 em geral:** nenhuma ferramenta resolve conflito de sincronização sozinha. A garantia de não ter conflito silencioso vem do git. O que as ferramentas oferecem é índice derivado, de preferência **fora** do vault, e reconstrução por máquina.

### Registro de cobertura

**Buscas feitas (36):**
1. MCP server markdown vault hybrid search BM25 embeddings
2. Obsidian MCP server semantic search local embeddings
3. local RAG markdown files MCP server Claude Code
4. personal knowledge base MCP hybrid search markdown frontmatter filter
5. agent memory markdown files git sync MCP server local-first
6. qmd tobi local search markdown MCP BM25 vector rerank
7. basic-memory MCP markdown knowledge graph semantic search
8. servidor MCP Obsidian busca semântica notas markdown local
9. "obsidian-hybrid-search" flowing-abyss
10. Hacker News Show HN MCP server Obsidian vault search agents
11. reddit ObsidianMD MCP semantic search Claude Code vault which server
12. markdown notes index in place sqlite-vec FTS5 MCP server Windows
13. memsearch zilliz markdown-first memory hybrid search MCP
14. base de conhecimento pessoal markdown busca híbrida agentes IA MCP Claude Code Codex
15. Khoj MCP server obsidian notes self-hosted search
16. "mathomhaus" guild MCP markdown
17. site:reddit.com LocalLLaMA MCP markdown notes local embeddings hybrid search
18. smithery obsidian semantic search MCP server
19. pulsemcp markdown knowledge base search server local embeddings
20. MCP server markdown notes "optimistic concurrency" OR etag OR "if_match" write safety
21. mcp.so obsidian vault hybrid search server
22. registry.modelcontextprotocol.io markdown vault search
23. github topic obsidian mcp-server rag hybrid search rust single binary
24. "second brain" MCP server markdown git sync two machines index rebuild
25. awesome-mcp-servers "Knowledge & Memory" obsidian semantic markdown hybrid
26. news.ycombinator.com Show HN local hybrid search markdown notes MCP
27. Obsidian forum MCP server semantic search Claude Code plugin local 2026
28. "read-only" MCP server obsidian vault hybrid search ollama sqlite index outside vault
29. vault-cortex github aliasunder obsidian DuckDB MCP
30. DalecB obsidian-semantic-mcp github bge-m3 read-only
31. tobi qmd Windows support issue sqlite-vec node-llama-cpp
32. basic-memory permalink frontmatter added to existing files sync disable
33. khoj MCP server docs.khoj.dev model context protocol
34. basic-memory issue modifies obsidian notes adds frontmatter permalink existing vault git diff
35. reddit r/ClaudeAI best MCP for Obsidian vault semantic search Claude Code qmd
36. Obsidian Claude Code busca vetorial MCP Windows embeddings locais cofre notas

**Fontes visitadas diretamente:**
- README bruto de cerca de 50 repositórios.
- Página do GitHub de cada um (estrelas e licença), mais `releases.atom` e `commits.atom`.
- GitHub Search API: issues com "windows" no título em 7 repositórios.
- Workflows de CI de 6 repositórios.
- README completo do punkpeye/awesome-mcp-servers, filtrado.
- API do registry oficial de MCP (buscas por obsidian, markdown, vault e freshvault; houve timeouts).
- Via WebFetch: PR #1477 do basic-memory; issue #31 do qmd; docs.basicmemory.com (user guide e página de integração com Obsidian).
- Documentação do grooveseek (`filters.md`, `usage.md`), do plugin de Claude Code do memsearch e o `installation.md` do markdown-vault-mcp.

**Só através de listagens de resultados de busca (não naveguei direto):** Glama, PulseMCP, mcp.so, Smithery, mcpservers.org, fórum do Obsidian, Hacker News.

### Limites

- **Nada foi instalado nem testado.** O suporte a Windows vem de docs e CI, não de execução.
- **Reddit:** as buscas não trouxeram nenhum tópico. Hacker News também só apareceu em listagens.
- **Não verificado:**
  - se o basic-memory grava frontmatter em notas existentes;
  - se Milvus Lite (usado pelo memsearch) roda no Windows;
  - como o markdown-vault-mcp resolve conflito no pull loop do git;
  - onde fica o índice do markdown-vault-mcp;
  - se o obsidian-mcp-connector faz busca híbrida;
  - se a Khoj tem MCP oficial.
- **Dados do GitHub:** estrelas e datas são raspadas do HTML e dos feeds do GitHub. "—" em release não quer dizer que o projeto está parado. A licença NOASSERTION do grooveseek contradiz o README (MIT OR Apache-2.0).
- **Qualidade de busca:** os benchmarks que os READMEs citam são alegações dos próprios autores e eu não os conferi. A qualidade para textos em português não foi medida em nenhum caso.
- **Cobertura:** o ecossistema é enorme (o PulseMCP lista 104 servidores de "obsidian"). Varri as fontes principais, mas pode haver projetos pequenos que ficaram de fora.

Rascunhos (READMEs baixados e listas de repositórios) estão em `C:\Users\GUSTAV~1.DEL\AppData\Local\Temp\claude\C--Projetos-maestri\3be42b76-debf-44ac-95f2-08dc0086471c\scratchpad\`.
