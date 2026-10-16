---
title: Relatório de varredura (texto integral do agente)
data: 2026-09-29
origem: subagente da sessão 3be42b76 (Claude Code, workspace TRF3)
aviso: saída de modelo; afirmações principais conferidas na seção 10 da exploração
---

# Ferramentas de memória e contexto compartilhado para agentes de código, e quais convivem com um vault Markdown (Obsidian + git)

Data da pesquisa: 29/09/2026. Estrelas, licença e último push vêm da API do GitHub, lidos no dia. O último release vem de `releases/latest`. As colunas A a F vêm dos READMEs e docs de cada projeto. "n/d" quer dizer que a documentação não trata do assunto; não quer dizer que o recurso não exista.

## Conclusão

- **Leem ou indexam uma pasta Markdown que já existe (o vault do humano):**
  - Basic Memory
  - memsearch
  - sqlite-memory
  - obsidian-second-brain
  - Open Second Brain
  - obsidian-wiki
  - agentcairn
  - SecondMind
  - nfvelten/agent-memory
  - Obsidian Palace MCP
  - second-brain-mcp
- **Guardam tudo em Markdown, mas numa pasta própria.** Essa pasta pode ficar dentro do repositório ou do vault e ser versionada em git:
  - akitaonrails/ai-memory
  - xChuCx/agent-memory
  - OKF Agent Memory
  - seamless
  - Memoria
  - memoro
  - llm-wiki
  - Serena
  - opencode-agent-memory e opencode-claude-memory
- **Mais parecidas com o guild (tarefas + conhecimento + handoff):**
  - **seamless**: Go, fila de tarefas com dependências, claim atômico, Markdown como fonte da verdade.
  - **beads**: Dolt, com sync por git.
  - **akitaonrails/ai-memory**: handoff tipado com "claim-once", decaimento, wiki Markdown em git.
  - **mcp_agent_mail**: coordenação por mensagens, sem tarefas.
- **Três cuidados de licença e compatibilidade:**
  - **mcp_agent_mail**: a licença MIT tem um anexo ("rider") que nega qualquer direito à OpenAI, à Anthropic e a quem age em nome delas. Leia antes de usar.
  - **sqlite-memory**: o README diz MIT, mas o arquivo LICENSE é Elastic License 2.0 modificada.
  - **Basic Memory**: o PR #1477, incorporado em 05/09/2026, tornou obrigatório o `permalink` em notas Markdown. Não confirmei se ele passa a gravar frontmatter em notas humanas já existentes. Teste numa cópia do vault antes.

## Tabela A–G

Legenda:
- **A**: onde fica o estado.
- **B**: indexa uma pasta Markdown já existente?
- **C**: como os agentes acessam.
- **D**: local ou nuvem; Windows.
- **E**: várias máquinas.
- **F**: ciclo de vida do conhecimento.
- **G**: licença, estrelas, último release.

| Ferramenta | A | B | C | D | E | F | G |
|---|---|---|---|---|---|---|---|
| **mathomhaus/guild** (referência) | SQLite em `~/.guild/`; gera um bloco no AGENTS.md | Não documentado (lore inserida via `lore inscribe`) | MCP + CLI (Claude Code, Codex, Cursor) | Local. Há binário Windows, mas lá a busca semântica fica desligada (só BM25) | n/d, foco em uma máquina | Quests (prioridade, dependências, claim atômico, cascata); tipos de lore com expiração ("research" em 30 dias, "decision" em 180); oath = princípios carregados no início; brief = nota de handoff | Apache-2.0, 302★, v0.3.2 (27/05/2026) |
| **basicmachines-co/basic-memory** | Markdown com frontmatter (title/type/permalink/tags), observations e relations; índice SQLite (ou Postgres) com embeddings | **Sim**: `basic-memory project add <nome> <pasta>`; a doc sugere abrir a pasta no Obsidian | MCP, CLI, API (Claude Code, Codex, Cursor, VS Code, ChatGPT) | Local grátis; nuvem opcional paga (US$15/mês); Windows sim | Nuvem com sync bidirecional (rclone); git possível ("git-friendly") | Tipo por frontmatter; sem expiração, rascunho ou handoff documentados | AGPL-3.0, 4.062★, v0.23.2 (25/08/2026) |
| **akitaonrails/ai-memory** | Wiki `.md` em git como fonte da verdade (`wiki/`); `raw/` com transcrições sanitizadas; índices SQLite/FTS5/embeddings em `db/` | Parcial: `ai-memory bootstrap` para projetos com histórico; apontar um vault externo não documentado | MCP, HTTP API, hooks de ciclo de vida, CLI (Claude Code, Codex, Cursor, OpenCode, Gemini CLI e 15+ outros) | Local, binário único; Windows via WSL2 suportado, nativo "experimental" | Wiki em git + servidor compartilhado (LAN/homelab) com autenticação multiusuário e auditoria | Handoff tipado "claim-once"; decaimento por camada, mais lento para o que é acessado; observações → consolidação → páginas | MIT, 8.623★, v2.4.1 (25/09/2026) |
| **zilliztech/memsearch** | `.md` como fonte da verdade (`.memsearch/memory/AAAA-MM-DD.md`); Milvus como "shadow index" reconstruível | **Sim**: `memsearch index ./notes/` (qualquer pasta) | Plugins/hooks (Claude Code, Codex, OpenCode, OpenClaw), CLI, API Python | Milvus Lite local; Zilliz Cloud ou Milvus self-hosted opcionais; Windows não documentado | Mesmo URI de Milvus compartilhado entre máquinas | Journals diários; PROJECT.md (estado durável) e USER.md; skills candidatas ficam inertes até instaladas | MIT, 2.681★, v0.4.21 (24/09/2026) |
| **sqliteai/sqlite-memory** | Markdown como fonte da verdade + SQLite (vetores/FTS) | **Sim**: `memory_add_directory('/path')` com sync incremental | Extensão SQLite, CLI `sqlmem`, que expõe MCP | Local (llama.cpp) ou nuvem (SQLite Cloud); Windows não documentado | Sync offline-first (CRDT/LWW) via sqlite-sync/SQLiteCloud | Sem conceitos de ciclo de vida | **Elastic 2.0 modificada** (README diz MIT), 122★, 1.3.5 (10/06/2026) |
| **xChuCx/agent-memory** | Markdown em `.agent-memory/` no repo (conventions, decisions, pitfalls, modules, sessions, staging, archive); FTS5 reconstruível | Não (só reconstrói o índice dos próprios `.md`) | MCP (3 tools) + CLI (Claude, Cursor, Codex, Gemini) | Local; binários windows_amd64/arm64 | Git é o sync; merge driver próprio | **Staging com revisão humana** (`review --diff` → `apply`); TTL no staging; arquivo write-once; notas de trabalho vs durável | Apache-2.0, 11★, v0.6.1 (23/09/2026) |
| **okf-memory/okf-agent-memory** | `knowledge/` no repo, Markdown com frontmatter no formato OKF v0.2 | Não documentado (o bootstrap cria a estrutura) | MCP stdio + CLI (Claude Code, Cursor) | Local, binário Go; Windows não documentado | Git; "hub push/sync" criptografado opcional | Níveis de confiança `verified: human` vs `generated: agent`; `stale_after`; log.md | MIT, 738★, v0.4.4 (27/09/2026) |
| **0spoon/seamless** | Markdown com frontmatter em `~/.seamless` como fonte da verdade; SQLite com índice e estado (sessões, tarefas) | Não documentado | MCP, CLI `seam`, daemon com console web (Claude Code, Codex CLI, qualquer cliente MCP) | Local; Go puro; macOS/Linux/Windows | n/d | Tarefas com fila de prontos por dependência, claim por lease, planos, supersessão com proveniência | MIT, 5★, v0.5.3 (28/09/2026) |
| **gastownhall/beads** (ex-steveyegge) | Dolt em `.beads/`; `issues.jsonl` exportado, mas "não é a fonte da verdade" | Não | CLI `bd` + MCP (Claude Code, Codex, Cursor, Copilot…) | Local ou servidor Dolt; Windows 11 documentado | `bd dolt push/pull` via remote git | Issues com dependências, `bd ready`, claim, compactação ("memory decay"), `bd remember`/`bd prime` | MIT, 27.504★, v1.3.0 (15/09/2026) |
| **Gentleman-Programming/engram** | SQLite+FTS5 em `~/.engram/engram.db` | Não; **exporta para Obsidian (beta)** | MCP, CLI, HTTP, TUI (Claude Code, OpenCode, Codex, Cursor…) | Local; Engram Cloud opcional; Windows suportado | "Git Sync" (chunks comprimidos) + nuvem | Tipos (decision, bugfix, discovery, pattern…); `topic_key` para atualizar em vez de duplicar; `mem_session_summary` como handoff | MIT, 6.929★, v2.2.1 (25/09/2026) |
| **thedotmack/claude-mem** | SQLite + Chroma | Não | Hooks (5 de ciclo de vida), MCP, CLI, viewer web (Claude Code, OpenCode, Codex, Cursor…) | Local; sync opcional com cmem.ai; Windows sim | Nuvem cmem.ai | Observações tipadas; resumos por sessão | Apache-2.0, 94.898★, v13.28.0 (26/09/2026) |
| **rohitg00/agentmemory** | KV em arquivos JSON (iii-engine), Redis opcional, vetores em memória | Não (tem `memory_compress_file` e import de JSONL) | MCP (54 tools), REST, hooks, skills | Local; Windows nativo manual, WSL2/Docker | Sync P2P (`memory_mesh_sync`), compartilhamento em equipe | Camadas working → episodic → semantic → procedural; decaimento Ebbinghaus; consolidação | Apache-2.0, 29.008★, v0.9.29 (16/08/2026) |
| **doobidoo/mcp-memory-service** | sqlite-vec, Cloudflare, híbrido ou Milvus | Não documentado | MCP, REST, CLI | Local, nuvem Cloudflare opcional; Windows sim | Backend Cloudflare/híbrido | Consolidação autônoma, decaimento, tags | Apache-2.0, 1.973★, v11.14.0 (25/09/2026) |
| **GreatScottyMac/context-portal** (ConPort) | SQLite por workspace + vetores | Importa `projectBrief.md` e `import_markdown_to_conport` | MCP stdio (Roo, Cline, Windsurf, Cursor) | Local; Windows sim | **Export/import de Markdown** | Product Context, Active Context, decisões, progresso com status, padrões; histórico de versões | Apache-2.0, 768★, v0.3.13 (29/10/2025); último push jan/2026 |
| **Dicklesworthstone/mcp_agent_mail** | Repo git com mensagens `.md` (frontmatter JSON) + SQLite FTS5 | Não | MCP HTTP/stdio, web UI, CLI (Claude Code, Codex, Gemini CLI…) | Local ou servidor HTTP; Windows não documentado (scripts bash) | Servidor compartilhado; export estático | Identidades, threads, reservas de arquivo com TTL, confirmação de leitura | **MIT com anexo que exclui OpenAI e Anthropic**, 2.173★, v0.3.2 (16/04/2026) |
| **campfirein/byterover-cli** (ex-Cipher) | Context tree de Markdown em `.brv/` | `brv source add <path>` (não confirmado para pastas arbitrárias) | CLI `brv`, MCP (22+ agentes) | Local; nuvem para colaboração | `brv vc push/pull`, versionamento tipo git | curate, versões | Elastic-2.0, 4.965★, v3.16.1 (27/05/2026); **arquivado em 27/09/2026** |
| **eugeniughelbur/obsidian-second-brain** | Markdown no próprio vault Obsidian | **Sim**: "safe to run on my existing vault", não apaga nada sem confirmação | Slash commands, skills (Codex/OpenCode), MCP, CLI | Local (pesquisa web opcional em nuvem); Windows sim (desde v0.15) | Obsidian Sync, iCloud, Syncthing, git | Fatos bitemporais; política de frescor (fato "timeless, dated, or pointer") | MIT, 4.638★, v0.17.0 (26/09/2026) |
| **itechmeat/open-second-brain** | Markdown em `Brain/` dentro do vault + índice | **Sim**: vault que já existe | MCP/adapters (Claude Code, Codex, Cursor, opencode…) | Local; **Windows nativo** | Syncthing | "Dream passes" determinísticos; preferências candidatas → confirmadas com confiança; regras sem uso são aposentadas | MIT, 425★, v1.61.0 (29/09/2026) |
| **Ar9av/obsidian-wiki** | Wiki Markdown no vault (index.md, log.md, hot.md, `_meta/`) | **Sim**: ingere fontes (docs, PDFs, notas) → wiki | Skills em Markdown, API Python (Claude Code, Codex, Cursor…) | Local, sem embeddings; Windows n/d | Repo privado em git; serviço Docker opcional | Fontes brutas → ingestão com delta → lint (contradições); páginas marcadas extracted/inferred/ambiguous | MIT, 3.506★, v2026.09.3 (23/09/2026) |
| **ccf/agentcairn** | Vault Markdown canônico + cache DuckDB | **Sim**; importa MEMORY.md do Claude Code | MCP, CLI, hooks | Local; Windows n/d | n/d | `valid_from`/`valid_until`/`superseded_by` | Apache-2.0, 60★, v0.26.2 (28/09/2026) |
| **geniallabsai/secondmind** (em PT-BR) | Vault Obsidian (protocols/, 01-sessions/, templates/, MANIFEST.json) | **Sim**: "qualquer vault Obsidian" | Skills + scripts Python (14 agentes) | Local, só arquivos; Windows via Python | Vault = repo git | Ciclo de 5 fases; handoffs em `01-sessions/handoffs/`; `supersede`; destilar após 3 sessões | MIT, 0★, sem release |
| **nfvelten/agent-memory** | Vault Obsidian + FTS5 + LanceDB em `<vault>/.agent-memory/index/` | **Sim** | MCP (16 tools) + CLI | Local; Windows n/d | n/d | Daily notes; decaimento por tipo de documento | AGPL-3.0, 0★ |
| **Probably-Computers/obsidian-palace-mcp** | Vault + `.palace/index.sqlite` | **Sim**: vigia alterações externas; grava em pastas em camadas (configurável) | MCP | Local (Node); Windows n/d | Vários vaults com modo ro/rw | Proveniência, confiança, tipos, status | AGPL-3.0, 0★, último push fev/2026 |
| **ddmanyes/second-brain-mcp** | Vault Markdown + índice DuckDB ou pgvector | Sim (PARA: 00-inbox…40-archive) | MCP + CLI | Local/offline | Menciona setups multi-máquina / servidor central | Inbox; compressão de notas velhas; ranking Ebbinghaus | MIT, 6★ |
| **passionworkeer/obsidian-shared-memory-bus** | Eventos JSONL + índices + Markdown derivado em `00-System/ai-memory` do vault | Detecta o vault, mas escreve só na subpasta dele | MCP + HTTP local + CLI | Local | n/d | 5 camadas (evento → sessão → projeto → compartilhado → arquivo); TTL e promoção | MIT, 0★ |
| **Agripp87/memoria_mcp** | Markdown + YAML em `MEMORIA_DIR`; FTS5 derivado | Não documentado | MCP stdio + HTTP com OAuth 2.1 | Local ou nuvem (Cloud Run) | **Repo git privado; union merge para logs diários** | Tipos (user, project, decision, feedback, reference, session, reflection); decaimento/promoção; "compile, don't retrieve" | Apache-2.0, 1★ |
| **bargisula/ai-memory-mcp** | Um `.md` por memória em `~/.ai-memory/notes/<projeto>/`; SQLite descartável | Não | MCP + CLI (Claude Code, Codex) | Local (Ollama opcional) | Recomenda git em `notes/` | Tipos decision/progress/failure/handoff; `get_handoff` | MIT, 0★ |
| **jayzeng/agentmemory** | `~/.agent-memory/` (MEMORY.md, SCRATCHPAD.md, daily/, topics/) | Só troca de diretório (`AGENT_MEMORY_DIR`) | CLI, MCP, skills (Claude Code, Codex, Cursor) | Local; Windows n/d | n/d | Durável vs diário vs scratchpad | MIT, 25★, sem release |
| **yubinkim444/repo-memory** | `.ai-memory/` no repo (facts.jsonl + decisions .md + gotchas) | Não | MCP + CLI | Local | Git | Fatos append-only com `verified_at` | MIT, 1★ |
| **Towano/memoro** | Markdown em repo git local (`~/.memoro`), commit a cada escrita | Não | MCP stdio/HTTP + CLI | Local/Docker; binário Windows | `sync_push`/`sync_pull` para remote | n/d | MIT, 0★ |
| **dck/brain-mcp** | Vault Markdown (`~/brain`) + SQLite | Vault dedicado com categorias fixas | MCP + CLI | Local; **sem Windows** | Uma máquina | Categorias (procedures, decisions, learnings…) | MIT, 0★ |
| **Fr4nZ82/mwe-mcp** | `wikis/` Markdown (prosa compilada) + `engine.db` com governança por fato | "Bulk ingest" de legado | MCP + dashboard | Self-hosted; .exe Windows | Multiusuário com ACL por fragmento | Janelas de validade dos fatos; ciclo noturno de dedup/merge/compile | AGPL-3.0 (ou comercial), 6★ |
| **WellyngtonF/llm-wiki** | Vault próprio (knowledge/{daily,notes,projects,raw,inbox}) | Não (Obsidian só como visualizador) | MCP (13 tools) + hooks (OpenCode, Codex, Claude Code) | Local (a compilação usa LLM configurado) | n/d | Classificação de sessões; compila logs diários em páginas; arquivamento por tipo (debugging 60 dias, padrões 180, decisões nunca) | MIT, 0★ |
| **oraios/serena** (memórias) | `.serena/memories/*.md` por projeto + `~/.serena/memories/global/` | Não (pasta própria) | MCP (list/read/write_memory) | Local | Via git do projeto | Onboarding; referências `mem:` | Licença não identificada pelo GitHub, 29.894★, v1.7.0 (09/08/2026) |
| **joshuadavidthomas/opencode-agent-memory** | Blocos `.md` + YAML (`~/.config/opencode/memory`, `.opencode/memory`) | Não | Só plugin do OpenCode | Local | n/d | Escopo global/projeto, read-only, limite de tamanho, journal | MIT, 339★, v0.3.0 (22/09/2026) |
| **kuitos/opencode-claude-memory** | **Reusa o diretório de memória nativo do Claude Code** (`~/.claude/projects/<repo>/memory/`) | Usa a memória Markdown do Claude Code | Plugin do OpenCode | Multiplataforma | n/d | Tipos user/feedback/project/reference; "auto-dream" | MIT, 64★ |
| **letta-ai/letta-code** (MemFS) | Markdown + YAML num repo git (local ou Letta Cloud) | n/d | Só dentro do harness Letta Code | Local ou nuvem; auto-reflexão desligada no Windows | Push para repo GitHub | `system/` sempre no prompt; o resto sob demanda | Apache-2.0, 3.480★, v0.33.6 (29/09/2026) |
| **sageox/ox** | Cache local → repo git **hospedado em sageox.ai** | Não | CLI + hooks/plugins (Claude Code, Codex, OpenCode…) | Nuvem obrigatória (sem self-host); Windows n/d | Sim, em equipe | Gravação de sessões | MIT, 62★, v0.19.0 (28/09/2026) |
| **mcp-memory-keeper** (mkreyman) | SQLite em `~/mcp-data/memory-keeper/context.db` | Não | MCP (Claude Code) | Local; Windows sim | Export/import JSON | Canais por branch git, checkpoints, categorias e prioridades | MIT, 136★ |
| **mem0 OpenMemory** | Docker com API + Qdrant + Postgres (fonte secundária) | Não | MCP | Local via Docker ou hospedado | n/d | n/d | mem0: Apache-2.0, 66.302★ |
| **getzep/graphiti** (MCP) | Grafo em Neo4j/FalkorDB; exige chave de LLM | Não documentado | MCP HTTP/stdio | Docker | Servidor | Fatos temporais (`valid_at`/`invalid_at`) | Apache-2.0, 31.303★ |
| **@modelcontextprotocol/server-memory** | Arquivo JSONL (entidades, relações, observações) | Não | MCP | Local | n/d | n/d | MIT (monorepo 90.666★) |
| **Bumblebiber/hmem** | Arquivo SQLite `.hmem` com hierarquia de 5 níveis | Não | MCP | Local | Arquivo portátil | Categorias por prefixo; carregamento preguiçoso | MIT, 24★, v1.3.8 (24/05/2026) |
| **linklore/linklore-mcp** | SQLite em `.linklore/` | Não | MCP + CLI | Local | n/d | Lore (decisões, armadilhas, journal) e Doc (specs, planos) com links | Elastic-2.0, 1★ |

## Classificação

**(1) Usam o Markdown do humano como fonte**

- (1a) Leem ou indexam uma pasta ou vault que já existe:
  - Basic Memory (ver ressalva do permalink)
  - memsearch
  - sqlite-memory
  - obsidian-second-brain
  - Open Second Brain
  - obsidian-wiki
  - agentcairn
  - SecondMind
  - nfvelten/agent-memory
  - Obsidian Palace MCP
  - second-brain-mcp
  - kuitos/opencode-claude-memory (sobre a memória Markdown do Claude Code)
- (1b) Markdown como fonte da verdade, mas em pasta própria, que pode ficar dentro do repo ou do vault e ir para o git:
  - akitaonrails/ai-memory
  - xChuCx/agent-memory
  - OKF Agent Memory
  - seamless
  - Memoria
  - bargisula/ai-memory-mcp
  - jayzeng/agentmemory
  - memoro
  - repo-memory
  - llm-wiki
  - brain-mcp
  - Serena
  - opencode-agent-memory
  - Letta MemFS (preso ao Letta Code)
  - ByteRover (arquivado)

**(2) Base própria, mas exporta ou sincroniza para Markdown ou git**

- ConPort: export/import de Markdown.
- Engram: exportação para Obsidian (beta) e git sync.
- mcp_agent_mail: mensagens `.md` num repo git + SQLite.
- beads: Dolt sobre remote git, com JSONL exportado.
- obsidian-shared-memory-bus: JSONL com Markdown derivado.
- mwe-mcp: prosa em Markdown compilada de um banco de fatos.

**(3) Base própria fechada (SQLite, vetorial, JSON ou nuvem)**

- guild
- claude-mem
- rohitg00/agentmemory (export em JSON)
- mcp-memory-service
- mcp-memory-keeper (export em JSON)
- OpenMemory
- Graphiti
- server-memory (JSONL)
- hmem
- linklore
- sageox/ox (nuvem)

## Cauda longa (só vista em listas e registros, sem verificação na fonte)

- **awesome-mcp-servers, seção Knowledge & Memory:** Magnemo, klypix-mcp, coldstart, BovedIA, whitemagic, shadowgraph, memini, agentpack, robo-cortex, flaiwheel, Myco, deja-vu, ChatCrystal, crbro-memory, a2cr, claude-handoff, recallnest, agentmem, mengram, Cortex.
- **Glama:** ozankasikci/global-agent-memory (vault Markdown revisado por humano; 14★, MIT), Lolaplex agents-memory, Mnemo Agent Memory, total-agent-memory.
- **awesome-agent-orchestrators:** Mnemoverse, Overlay, Hivekeep, Concord MCP, foremerge, AgentBridge, hcom.
- **Hacker News:** Friday, Strata.
- **Outros:** agtx (quadro de tarefas para agentes), Snipara (SaaS), agentbrain-handoffs, ai-agent-handoff, AgentGit, MOM, agent-memory-hub.

## Registro de cobertura

**Buscas (41; em inglês e português):**
1. agent memory MCP server markdown files Claude Code
2. persistent memory for Claude Code across sessions github
3. shared context between coding agents Claude Code Codex Cursor memory layer
4. obsidian vault MCP server memory for AI coding agents
5. session handoff between AI coding agents tool open source
6. knowledge graph memory MCP server local sqlite coding agents
7. memória persistente agentes de IA Claude Code markdown obsidian
8. "basic memory" basicmachines markdown MCP sync cloud release
9. git-backed memory for AI agents markdown repository MCP
10. awesome-mcp-servers knowledge memory section list
11. Hacker News Show HN memory for coding agents markdown local
12. reddit ClaudeAI best memory MCP for Claude Code obsidian vault
13. multi-agent coordination shared blackboard MCP Claude Code Codex OpenCode tasks notes
14. contexto compartilhado entre agentes Codex Claude Code ferramenta memória MCP
15. OpenCode plugin persistent memory agents markdown
16. "source of truth" markdown memory agents index existing notes folder MCP semantic search qmd
17. memory bank MCP Cline memory-bank markdown files multi-project server
18. mathomhaus guild quests lore oath agents
19. agent memory decay expiration "scratchpad" "durable" coding agents…
20. awesome-claude-code memory context management tools list
21. steveyegge beads memory for coding agents git issue tracker
22. Context Portal ConPort MCP project memory sqlite export markdown
23. doobidoo mcp-memory-service Claude Code Codex cloudflare sync
24. pulsemcp memory servers agent memory coding 2026
25. OpenMemory mem0 local MCP cursor claude code shared memory
26. mcp_agent_mail git-backed markdown coordination coding agents
27. Graphiti Zep MCP server temporal knowledge graph Claude Code Cursor memory
28. engram memory coding agents Go binary sqlite MCP
29. ByteRover cipher memory layer coding agents context tree markdown
30. "LLM wiki" Karpathy agent memory markdown vault tool github coding agents
31. Letta Code memory filesystem git-backed markdown memfs
32. smithery.ai memory server coding agents markdown notes
33. registry.modelcontextprotocol.io memory markdown server
34. github topic agent-memory markdown obsidian claude-code codex opencode
35. OpenMemory mem0 github openmemory self-hosted docker qdrant deprecated 2026
36. Obsidian Palace MCP Probably-Computers github
37. ByteRover CLI repository archived September 2026 moved new repo brv
38. serena ".serena/memories" markdown write_memory read_memory
39. site:reddit.com memory MCP Claude Code Codex shared markdown obsidian which one do you use
40. ozankasikci global agent memory human-reviewed markdown vault MCP daemon
41. basic memory existing obsidian vault frontmatter permalink…

**Fontes primárias lidas (README ou docs):**
- **READMEs no GitHub:** guild, basic-memory, ai-memory (akitaonrails), memsearch, xChuCx/agent-memory, beads, engram, claude-mem, rohitg00/agentmemory, mcp-memory-service, jayzeng/agentmemory, sqlite-memory, context-portal, mcp_agent_mail, opencode-agent-memory, byterover-cli, brain-mcp, nfvelten/agent-memory, ai-memory-mcp, memoria_mcp, repo-memory, memoro, mwe-mcp, llm-wiki, obsidian-second-brain, open-second-brain, obsidian-wiki, secondmind, second-brain-mcp, opencode-claude-memory, obsidian-palace-mcp, seamless, agentcairn, sageox/ox, linklore-mcp, obsidian-shared-memory-bus, okf-agent-memory, letta-code, serena, README do MCP do Graphiti, server-memory.
- **Docs e páginas:** docs.letta.com/concepts/memfs, docs.basicmemory.com/local/user-guide, PR #1477 do basic-memory, docs/research-basic-memory.md do ai-memory, mem0.ai/openmemory.
- **Arquivos LICENSE:** mcp_agent_mail e sqlite-memory.
- **API do GitHub:** metadados e `releases/latest` de cerca de 45 repositórios.

**Listas e registros:**
- punkpeye/awesome-mcp-servers: README bruto, seção Knowledge & Memory.
- andyrewlee/awesome-agent-orchestrators.
- hesreallyhim/awesome-claude-code: página sem conteúdo útil.
- TensorBlock/awesome-mcp-servers: só via busca.
- Glama: busca "markdown memory coding agents".
- mcp.so: busca "memory markdown" deu 0 resultados.
- PulseMCP, Smithery, registry oficial e mcpservers.org: só via resultados de busca.
- Tópicos do GitHub (session-handoff, agent-handoff, claude-memory, codex-memory): só via busca.

**Hacker News:** itens 47103237 (Hmem), 49581240 (OKF), 49731353 (Friday), 49807583 (Strata).

## Limites

- **Reddit:** nenhuma página do reddit.com apareceu nas buscas, e não li threads do Reddit.
- **Listas e registros incompletos:**
  - awesome-claude-code: o WebFetch não trouxe o conteúdo da página.
  - Smithery, PulseMCP e o registry oficial: não naveguei, vi só trechos de busca.
  - Cauda longa: não verificada item a item (a seção Knowledge & Memory do awesome-mcp-servers tem cerca de 335 linhas).
- **Resumos gerados por modelo:** as colunas A–F vieram de resumos do WebFetch, feitos por um modelo pequeno, e algumas "citações" podem estar parafraseadas. Um exemplo concreto: o resumo do sqlite-memory disse MIT, mas o arquivo LICENSE é Elastic 2.0 modificada. Licenças e números vêm da API ou dos arquivos, que são mais confiáveis.
- **Windows:** não documentado em vários projetos (marcados n/d). Nada foi testado localmente.
- **Basic Memory:** não confirmei se ele reescreve o frontmatter de notas humanas existentes depois do PR #1477.
- **OpenMemory:** o README primário deu 404; os dados vêm do blog da mem0 e de trechos de busca.
- **Serena:** o GitHub devolve licença NOASSERTION, então não sei a licença.
- **Datas:** para projetos sem release, só tenho o último push. As estrelas são um retrato de 29/09/2026.
