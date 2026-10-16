---
title: Pesquisa 23, banco como verdade com vista Markdown editável
data: 2026-10-04
origem: subagente de pesquisa (Claude Code), ticket 23 "Banco como verdade com vista Markdown editável"
aviso: saída de modelo. Fontes primárias: README, docs e código-fonte brutos (raw.githubusercontent.com), listagem de arquivos pelo jsDelivr (data.jsdelivr.com, sem conteúdo resumido), arquivos de CI, API de busca do GitHub (estrelas, licença, último push), API do registry oficial de MCP, API Algolia do Hacker News, o community-plugins.json oficial do Obsidian, o README bruto do punkpeye/awesome-mcp-servers, as páginas de ajuda do fossil-scm.org e da CouchDB, e um tópico do fórum do Obsidian (JSON do Discourse). Nada foi clonado, instalado ou executado. O que não foi conferido na fonte está marcado como **não verificado** (NV). Onde escrevo "inferência", a conclusão sai do código ou da doc citada, mas não foi testada.
---

# Banco como verdade com vista Markdown editável: levantamento de 04/10/2026

## Resumo (uma tela)

1. **Cobertura:** 45 consultas (21 web em 6 línguas, 10 na API de busca do GitHub, 7 no registry oficial de MCP,
   3 no HN, 2 no awesome-mcp-servers, 1 no catálogo de plugins do Obsidian, 1 no fórum do Obsidian). Foram
   conferidas na fonte 24 ferramentas (seção 3). Outras 9 já vistas foram reavaliadas só contra a pergunta nova
   (seção 5).
2. **Não existe ferramenta pronta que cumpra tudo:** banco como verdade, vista `.md` editável com volta segura,
   Windows nativo e duas máquinas pares sem servidor. Na categoria "memória de agentes" que tem banco e vista
   Markdown, **nenhuma ferramenta protege a edição humana**:
   - **memo** sobrescreve em silêncio a edição do corpo;
   - **khaled1174/agent-memory** ignora edições em memórias que já existem;
   - **Engram** declara a vista "one-way";
   - **ConPort** reimporta duplicando decisões ou sobrescrevendo o contexto.
3. **Três achados com semântica de volta séria:**
   - **Self-hosted LiveSync (CouchDB) + um servidor MCP** (es617/obsidian-sync-mcp e outros). A verdade é um
     banco replicado com árvore de revisões, e o vault do Obsidian é a vista viva e editável. Há merge de três
     vias quando existe uma base comum; sem ela, o conflito vai ao humano. O plugin é maduro (12,6 mil estrelas,
     MIT). **Contra:** exige um servidor CouchDB ou uma relay de sinalização (P2P), os MCPs são pequenos (59
     estrelas ou menos), e o "banco" guarda arquivos, não registros estruturados.
   - **beads (Dolt) + o plugin obsidian-beads.** A verdade é o Dolt, com merge por célula. O sync entre máquinas
     usa `bd dolt push/pull` num remote git (`refs/dolt/data`), o que serve ao GitHub como ponto de encontro. O CI
     roda em `windows-latest`. O plugin edita a issue como frontmatter e corpo e grava só os campos mudados.
     **Contra:** cobre só tarefas, a "vista" é um painel do plugin e não arquivos `.md` no disco, e o plugin tem
     3 estrelas.
   - **sqlite-memory + sqlite-sync.** O banco guarda o conteúdo, `memory_materialize_files()` gera os arquivos e
     `memory_add_directory()` traz as edições de volta. O sync entre máquinas é por CRDT LWW por bloco.
     **Contra:** exige backend (SQLite Cloud, Postgres ou Supabase), a licença é Elastic 2.0, e não há proteção
     de base na volta (inferência).
4. **Recomendação (a decisão é do Gustavo):** não adotar nenhuma ferramenta de memória de agentes como o hub.
   Levar ao próximo ticket a escolha entre duas formas:
   - **(A)** um banco replicado com o vault como vista viva, no modelo LiveSync/CouchDB;
   - **(B)** um banco próprio que gera a vista e aceita a volta com verificação de base (hash ou revisão por
     arquivo), no modelo obsidian-beads/memo-reconcile. O sync do banco viria do Dolt ou de um CRDT.

   O beads pode servir de casa das **tarefas** em qualquer das duas.

## 1. Consultas feitas (registro para auditoria)

### 1.1 Busca web (WebSearch; listagens de resultado, não fonte primária)

| # | Consulta | Língua |
|---|---|---|
| W1 | two-way sync SQLite database markdown files obsidian edit back to database tool github | en |
| W2 | agent memory MCP server sqlite "export to markdown" "import" obsidian round-trip | en |
| W3 | database as source of truth markdown view editable "bidirectional" notes AI agents MCP local-first | en |
| W4 | Joplin MCP server Claude Code notes SQLite external editor markdown | en |
| W5 | khaled1174 agent-memory sqlite "sync-from-vault" obsidian | en |
| W6 | site:news.ycombinator.com Show HN memory for agents sqlite markdown mirror obsidian edit | en (HN) |
| W7 | reddit ObsidianMD sqlite source of truth generate markdown notes edit sync back database | en (Reddit) |
| W8 | AIエージェント メモリ SQLite Markdown エクスポート Obsidian 双方向同期 MCP | ja |
| W9 | AI 智能体 记忆 SQLite 为真相源 Markdown 镜像 可编辑 回写 数据库 MCP github | zh |
| W10 | memória agentes IA banco SQLite espelho markdown editável sincronização bidirecional obsidian MCP | pt |
| W11 | Wissensdatenbank KI-Agenten SQLite Markdown Export Import Obsidian Rücksync MCP Server | de |
| W12 | "markdown mirror" agent memory sqlite "source of truth" human editable reconcile watcher github | en |
| W13 | SQLite peer-to-peer sync two machines merge CRDT cr-sqlite OR "sqlite-sync" OR Dolt Windows local-first notes | en |
| W14 | beads bd export markdown edit import issues jsonl "bd edit" obsidian view | en |
| W15 | engram Gentleman-Programming obsidian export beta one-way memories markdown | en |
| W16 | 메모리 AI 에이전트 SQLite 마크다운 내보내기 옵시디언 양방향 동기화 MCP 서버 | ko |
| W17 | memoria agentes IA base de datos fuente de verdad vista markdown editable Obsidian sincronización de vuelta | es |
| W18 | Trilium Notes OR TriliumNext MCP server AI agents sqlite sync server markdown export import | en |
| W19 | obsidian plugin "beads" pane edit issues frontmatter save bd update github | en |
| W20 | ybonda memo MCP sqlite obsidian vault render memories markdown edit | en |
| W21 | reddit obsidian livesync couchdb claude code MCP agent write notes conflict | en (Reddit) |

W5, W19 e W20 só localizaram repositórios já achados por outras consultas.

### 1.2 API de busca do GitHub (`/search/repositories`, ordenado por estrelas)

| # | Consulta | Resultado útil |
|---|---|---|
| G1 | sqlite markdown mirror agent memory | huangjua/dsh-local-memory (Markdown como verdade, fora da premissa) |
| G2 | obsidian two-way sync sqlite memory | 0 |
| G3 | sync-to-vault sync-from-vault | 0 |
| G4 | agent memory sqlite obsidian export import | 0 |
| G5 | markdown round-trip database notes mcp | limite de taxa estourado |
| G6 | obsidian mirror sqlite memory mcp | 0 |
| G7 | markdown projection sqlite agent | Orange-hanter/cod-doc (não avaliado) |
| G8 | two-way markdown sqlite sync | **jindraregal/sql-md-sync**, sergi039/obsidian-kanban-app |
| G9 | dolt obsidian | 0 |
| G10 | couchdb mcp obsidian | 9 servidores MCP sobre o LiveSync (seção 6) |

Metadados (estrelas, licença, último push) vieram de quatro consultas `repo:a+repo:b+...` na mesma API.

### 1.3 Registry oficial de MCP (`registry.modelcontextprotocol.io/v0.1/servers?search=`)

| # | Termo | Resultado útil |
|---|---|---|
| R1 | obsidian | **es617/obsidian-sync-mcp** ("local files or Self-hosted LiveSync"); os demais leem ou gravam o vault direto |
| R2–R3 | memory-sqlite, markdown-mirror | 0 |
| R4 | memory | io.agentage/memory (Markdown como verdade) |
| R5 | sqlite | só servidores genéricos de SQL |
| R6 | knowledge | nada com Markdown |
| R7 | notes | só notas em Markdown como verdade |

Limite: a busca devolve as 100 primeiras entradas, com muitas versões repetidas do mesmo servidor.

### 1.4 Hacker News (API Algolia), listas e fórum

- **H1** "sqlite markdown obsidian agent memory": Screenpipe, Echos e G-Spot, nenhum pertinente.
- **H2** "markdown view database source of truth notes": 0.
- **H3** "livesync mcp": Strata (editor Markdown montável como sistema de arquivos; NV) e Fireproof (banco
  local-first, fora do escopo).
- **A1–A2** README bruto do punkpeye/awesome-mcp-servers (4.541 linhas), com grep por "two-way",
  "bidirectional", "markdown mirror" e "sqlite…markdown". Nenhuma ferramenta de memória com volta ao banco. Só
  apareceram as de Markdown como verdade (krimto, rms-memory-mcp, LINZA-MCP).
- **O1** `obsidianmd/obsidian-releases/community-plugins.json` (8.405 plugins), com grep por beads, engram,
  joplin, trilium, dolt, couchdb, "two-way sync" e "agent memory". Achados: **obsidian-beads**,
  **obsidian-joplin-server-sync**, **obsidian-postgres-sync**, **obsidian-auto-note-importer**, vários
  plugins de CouchDB e de memória.
- **F1** Fórum do Obsidian, tópico 112547 ("Self-hosted LiveShare: Agent / Automation CLI"), sobre o
  fanselau/obsidian-vault-cli.

## 2. Como as ferramentas se dividem sob a premissa nova

| Classe | O que faz com a edição no `.md` | Ferramentas |
|---|---|---|
| **V0. Vista só de ida** | Ignora ou sobrescreve a edição | memo, Engram, khaled1174/agent-memory (para edições), Mnehmos synch (NV) |
| **V1. Volta por reimportação** | Importa sem verificar a base, então a última gravação vence, duplica ou apaga | ConPort, xiangzi1126/ai-agent-memory-mcp, sqlite-memory, sql-md-sync, obsidian-postgres-sync |
| **V2. Volta com verificação** | Detecta que o banco mudou e faz merge, avisa ou pergunta | LiveSync (árvore de revisões, merge de três vias), obsidian-beads (recarrega e avisa), obsidian-auto-note-importer (conflito por campo), obsidian-joplin-server-sync |
| **Fora da premissa** | O Markdown é a verdade e o banco é índice | Basic Memory, ai-memory, seamless, open-zk-kb, agentcairn e o resto da classe (1) da varredura 2 |
| **Infraestrutura** | Não tem vista; resolve o sync do banco | Dolt, cr-sqlite, sqlite-sync, Fossil |

## 3. Tabela comparativa (conferida na fonte)

Legenda:
- **Acesso**: como o agente acessa.
- **Vista e volta**: se há vista Markdown e como a edição volta ao banco.
- **Se o banco mudou**: o que acontece quando o banco mudou entre a geração da vista e a edição.
- **2ª máquina**: como o banco chega à outra máquina.
- **Atividade**: estrelas e último push, lidos em 04/10/2026.

| Ferramenta | Acesso | Vista e volta | Se o banco mudou | Windows | 2ª máquina | Licença | Atividade |
|---|---|---|---|---|---|---|---|
| **vrtmrz/obsidian-livesync** (plugin) + CouchDB | Sem MCP próprio. Ver as linhas seguintes. | O vault é a vista viva, e o plugin grava as duas direções | Árvore de revisões do PouchDB. Merge automático só com uma base comum disponível; sem ela, pergunta ao humano. "Always overwrite with a newer file" é beta, só para teste | Sim: plugin do Obsidian, que roda em todas as plataformas dele; a CouchDB tem instalação para Windows | Servidor CouchDB, object storage (S3/MinIO/R2) ou P2P por WebRTC (exige relay de sinalização e um par online) | MIT | 12.648★, 2026-10-04 |
| **es617/obsidian-sync-mcp** | MCP (HTTP): read/write/edit/move/delete_note e metadados | Grava no CouchDB pela `livesync-commonlib`, e a edição aparece no vault | Tratamento de `_rev` na escrita do agente: **NV** | **NV**: CI só `ubuntu-latest`; scripts de deploy "macOS/Linux, or WSL" | O do LiveSync | MIT | 59★, 2026-10-04 |
| fanselau/obsidian-vault-cli (fórum) | CLI + skill para Claude Code | Igual ao anterior, pelo feed de mudanças | NV | NV (Node 20+) | O do LiveSync | NV | NV |
| **gastownhall/beads** | CLI `bd` + MCP (`beads-mcp` no PyPI) | `issues.jsonl` é exportação "não a fonte da verdade"; import é só upsert | Merge por célula no Dolt (`bd dolt pull`) | Sim: README e jobs `windows-latest` no `pr.yml` | `bd dolt push/pull` em `refs/dolt/data` de um remote git | MIT | 27.635★, 2026-10-04 |
| **Rome-1/obsidian-beads** (plugin) | Para o humano, roda `bd` por `child_process` | Painel e editor (frontmatter + corpo Markdown), e Save grava "só os campos mudados" via `bd update`. **Não há `.md` no disco.** | Editor aberto recarrega quando a issue muda; com edições não salvas, mantém e avisa ("Revert" carrega a nova) | Só desktop; Windows NV | O do beads | MIT | 3★, 2026-09-28 |
| **sqliteai/sqlite-memory** + sqlite-sync | Extensão SQLite, CLI `sqlmem` (expõe MCP) | `memory_materialize_files()` gera os arquivos; `memory_add_directory()` traz de volta (substitui o que mudou e apaga o que sumiu) | Sem verificação de base: o arquivo alterado substitui o conteúdo do banco (inferência da doc) | sqlite-sync: "Linux, macOS, Windows…"; sqlite-memory NV | CRDT "block-level LWW" via SQLite Cloud ou Postgres/Supabase próprio | **Elastic 2.0 modificada** (o README diz MIT) | 123★, 2026-07-21 (sqlite-sync 574★) |
| **ybonda/memo** | MCP + CLI | Vista "One-way projection of DB"; `memo reconcile --apply` só traz exclusões e mudança de pasta | Edições no corpo "are silently overwritten on the next sync" | NV (Go) | Não documentado | MIT | 4★, 2026-04-23 |
| **khaled1174/agent-memory** | MCP (12 ferramentas) + CLI | Espelho automático; `sync-from-vault` importa | O código pula todo arquivo cujo `id` já existe, então **edições em memórias existentes são ignoradas** | README: "macOS, Linux, WSL, Windows" (CI NV) | Não documentado (há uma ponte HTTP "hermes") | MIT | 1★, 2026-05-14 |
| **xiangzi1126/ai-agent-memory-mcp** | MCP + CLI | Espelho "editable"; `cli sync` reconstrói SQLite + Chroma a partir do Markdown | O Markdown vence por inteiro na reconstrução; concorrência NV | Docs com comandos PowerShell (CI NV) | Dados em `.aamm/` do projeto ("travel with the project"); NV | MIT | 0★, 2026-07-15 |
| **Gentleman-Programming/engram** | MCP, CLI, HTTP, TUI | `obsidian-export` (beta): "the exporter is one-way… edits are overwritten" | Sobrescreve | Sim (doc de Task Scheduler) | Git Sync por chunks JSONL.gz só de acréscimo, ou Engram Cloud | MIT | 7.033★, 2026-10-04 |
| **GreatScottyMac/context-portal** | MCP | `export_conport_to_markdown` / `import_markdown_to_conport` | Decisões e progresso: `INSERT` (duplica). Padrões e custom data: `INSERT OR REPLACE`. Product/active context: sobrescreve | README cita Windows (instalação Python) | Não documentado (`context.db` por workspace) | Apache-2.0 | 767★, 2026-01-27 |
| **mathomhaus/guild** | MCP + CLI | Nenhuma vista Markdown; "Switching MCP clients requires no export" | — | Zip Windows só com busca por palavra-chave | Não documentado | Apache-2.0 | 302★, 2026-09-14 |
| Fr4nZ82/mwe-mcp | MCP + dashboard | O wiki é prosa compilada; a correção é feita **no dashboard**, "not by rewriting a paragraph in a text editor" | — | Sim (zip `windows-msvc`) | Servidor multiusuário | AGPL-3.0 | 6★, 2026-09-19 |
| Mnehmos/mnehmos.synch.mcp | MCP | SQLite "with Markdown file fallbacks"; volta não documentada | NV | Sim (caminho `%USERPROFILE%`) | Não documentado | MIT | 3★, 2026-01-10 |
| passionworkeer/obsidian-shared-memory-bus | MCP HTTP | Markdown "派生" (derivado); volta não documentada | NV | Badge Windows/macOS/Linux | Não documentado | MIT | 0★, 2026-09-21 |
| Dicklesworthstone/mcp_agent_mail | MCP | `.md` em git como artefato de auditoria, não como vista editável | — | NV | Servidor | MIT com anexo (ver varredura 2) | 2.183★, 2026-09-29 |
| **jindraregal/sql-md-sync** | CLI (npm) | Uma linha da tabela por `.md`; `export` e `import` (reconstrói o banco); `status` mostra o drift | Sem resolução além do git; sem watcher | NV | Os `.md` vão no git e o banco é reconstruído | MIT | 4★, 2026-08-03 |
| uppinote20/obsidian-auto-note-importer | Agente acessa o banco remoto (Supabase, Airtable…) | Plugin: linha vira nota; empurra de volta as **edições de frontmatter** | Conflito por campo: `Manual` (avisa e pula), `Obsidian wins`, `Remote wins` | Plugin desktop (Windows NV) | O banco é remoto (nuvem ou Supabase próprio) | MIT | 18★, 2026-10-04 |
| lanjak/obsidian-postgres-sync | Agente acessa o Postgres | O vault vira tabela no Postgres via PostgREST | "Last-write-wins by modification time" | NV | Postgres + PostgREST num servidor | MIT | 2★, 2026-08-31 |
| laurent22/joplin | MCPs da comunidade pela API local (NV) | Sem vault. Editor externo por nota (Ctrl+E); vault Obsidian só com o plugin obsidian-joplin-server-sync (Joplin Server, estratégias duplicate/local/remote e merge de três vias) | Sync: copia a nota local para o caderno *Conflict* e a remota substitui | Sim | Sistema de arquivos, OneDrive, Nextcloud, WebDAV, S3, Dropbox, Joplin Cloud | AGPL-3.0-or-later | 56.591★, 2026-10-04 |
| TriliumNext/Trilium | MCPs da comunidade via ETAPI (NV) | Import/export de Markdown pontual; o editor é WYSIWYG | — | Sim | Servidor de sync próprio | AGPL-3.0 | 38.200★, 2026-10-04 |
| dolthub/dolt | CLI, SQL | Nenhuma | `merge`, `conflicts` | Sim (`.msi`) | `push/pull` para remotes (o beads usa um remote git) | Apache-2.0 | 24.570★, 2026-10-03 |
| vlcn-io/cr-sqlite | Extensão SQLite | Nenhuma | Merge CRDT por coluna; dá para escolher "fork the data on merge conflict" | Sim (`.dll`) | Troca de patches `crsql_changes` entre pares, sem servidor | MIT | 3.806★, 2026-08-10 |
| Fossil SCM | CLI, web | `fossil wiki export` / `fossil wiki commit` (Markdown suportado) | Edições concorrentes em repositórios distintos fazem a página "fork"; a web mostra a última e não há interface de merge | NV | Sync entre repositórios por HTTPS ou SSH, qualquer um serve | NV (fora do GitHub) | NV |

## 4. Melhores achados, com evidência

### 4.1 LiveSync + CouchDB: o único com semântica de conflito pensada para a edição humana

- **O modelo.** O plugin *"leverages robust server solutions such as CouchDB or object storage… It also supports
  peer-to-peer synchronisation using WebRTC… A signalling relay is still required for peer discovery"*
  ([README](https://raw.githubusercontent.com/vrtmrz/obsidian-livesync/main/README.md)). O banco replicado é o
  que viaja entre as máquinas; o vault de cada uma é a vista editável.
- **O que acontece se o banco mudou.** *"PouchDB stores a document as a revision tree. It selects one current leaf
  as the deterministic winner and reports the other current leaves as conflicts… A conservative three-way merge
  therefore compares the changes from `A1` to each leaf"*. E ainda: *"Missing or compacted history stops
  conservative automatic merge instead of guessing a base"*
  ([specs_conflict_resolution.md](https://raw.githubusercontent.com/vrtmrz/obsidian-livesync/main/docs/specs_conflict_resolution.md)).
  A resolução pela data mais nova é *"Testing only… cannot establish which revision reflects the user's intent"*
  ([settings.md](https://raw.githubusercontent.com/vrtmrz/obsidian-livesync/main/docs/settings.md)).
- **Acesso do agente.** O es617/obsidian-sync-mcp tem um *"CouchDB mode — reads from a CouchDB database…
  using livesync-commonlib — the same library that powers the plugin"*. As ferramentas incluem `write_note` e
  `edit_note` ([README](https://raw.githubusercontent.com/es617/obsidian-sync-mcp/main/README.md)). O
  obsidian-vault-cli faz o mesmo por CLI, e *"Files show up in Obsidian immediately via the LiveSync change
  feed"* (fórum do Obsidian, tópico 112547).
- **Contras:**
  - Sem um servidor CouchDB ou object storage, só resta o P2P, e nele *"At least one device containing the
    required data must be online while another device synchronises"*. Nesse modo o agente lê o vault pelo
    disco, não o banco (inferência).
  - Por padrão o banco é cifrado e fragmentado (o fórum: *"everything is AES-256-GCM encrypted, chunked… path
    names are obfuscated"*). Só se lê com a `livesync-commonlib`, e o agente não ganha uma "forma mais
    adequada" que o Markdown: ganha as mesmas notas.
  - O CI do MCP é só Ubuntu, e o tratamento de `_rev` nas escritas do agente é NV.

### 4.2 beads + obsidian-beads: o banco estruturado que sincroniza pelo GitHub

- **Sync entre máquinas.** *"Cross-machine sync uses `bd dolt push` / `bd dolt pull` against `refs/dolt/data` on
  your git remote; `.beads/issues.jsonl` is an export for viewers and interchange, not the source of truth"*
  ([README](https://raw.githubusercontent.com/gastownhall/beads/main/README.md)). O Dolt faz *"cell-level
  merge"*, e o JSONL *"import is upsert-only"*
  ([sync-concepts.md](https://raw.githubusercontent.com/gastownhall/beads/main/docs/core-concepts/sync-concepts.md)).
  Isso resolve o problema do ticket 22 (o git não junta binário) sem servidor próprio: o GitHub serve de ponto
  de encontro.
- **Windows.** O `pr.yml` mantém jobs nativos `windows-latest` (`test-windows-liveness`,
  `worktree-remove-windows`).
- **Vista editável no Obsidian.** *"click a row and the bead opens like a note… Save (or ⌘/Ctrl-S) writes only
  the changed fields via `bd update`"*. E também: *"An open bead editor reloads when its bead changes. If you have
  unsaved edits it keeps them and says the bead changed; **Revert** loads the new version"*
  ([README](https://raw.githubusercontent.com/rome-1/obsidian-beads/main/README.md)).
- **Contras:**
  - Cobre só tarefas e dependências.
  - A vista é um `ItemView` do plugin: a busca e o grafo do Obsidian não a enxergam.
  - Salvar depois do aviso grava por cima, campo a campo (inferência).
  - Os syncs (`bd dolt pull`) não entram no journal de eventos, e o plugin os detecta por polling.

### 4.3 sqlite-memory: o banco gera os arquivos e os aceita de volta

- **Ida e volta.** O banco guarda o conteúdo (`dbmem_content`). `memory_add_directory` faz *"Cleanup: Removes
  database entries for files that no longer exist on disk"* e *"replacing modified ones"*.
  `memory_materialize_files()` gera os arquivos
  ([README](https://raw.githubusercontent.com/sqliteai/sqlite-memory/main/README.md)).
- **Sync entre máquinas.** *"block-level LWW CRDT… merges line-level changes from concurrent agents without
  conflicts"*, via sqlite-sync com SQLite Cloud, ou Postgres ou Supabase próprios
  ([sqlite-sync](https://raw.githubusercontent.com/sqliteai/sqlite-sync/main/README.md)).
- **Contras:**
  - A volta não confere a base. Um arquivo antigo reimportado vence o banco (inferência).
  - Exige um backend de sync.
  - O arquivo LICENSE é *"Elastic License 2.0 (modified for open-source use)"*, ao contrário do que o README
    diz.

### 4.4 O padrão que se repete na categoria "memória de agentes": a vista não volta

- **memo:** *"manual edits to a file's body are silently overwritten on the next sync… Body edits are still
  ignored by reconcile"* ([README](https://raw.githubusercontent.com/ybonda/memo/main/README.md)).
- **khaled1174/agent-memory:** o README promete *"two-way Markdown bridge"*, mas o `memory.py` faz `# Skip if ID
  already exists` antes de inserir
  ([memory.py](https://raw.githubusercontent.com/khaled1174/agent-memory/main/memory.py), linhas 431–437).
- **Engram:** *"the exporter is one-way. Engram writes to the vault, never reads from it"*. A volta com
  resolução de conflito está na lista de pedidos futuros
  ([obsidian-brain.md](https://raw.githubusercontent.com/Gentleman-Programming/engram/main/docs/beta/obsidian-brain.md)).
- **ConPort:** `log_decision` faz `INSERT INTO decisions`; `log_system_pattern` e `log_custom_data` fazem
  `INSERT OR REPLACE`
  ([database.py](https://raw.githubusercontent.com/GreatScottyMac/context-portal/main/src/context_portal_mcp/db/database.py)).
  Reimportar uma exportação editada duplica as decisões.

### 4.5 Ideias de desenho que valem para um hub próprio

Nenhuma destas ferramentas é candidata a hub, mas cada uma mostra um mecanismo aproveitável.

- **Nome de arquivo congelado** na primeira gravação, *"so Obsidian wikilinks remain stable"* (memo).
- **Gravar só os campos que mudaram**, e avisar quando o registro mudou com o editor aberto (obsidian-beads).
- **Conflito por campo com modo `Manual`**, que avisa e pula
  ([auto-note-importer](https://raw.githubusercontent.com/uppinote20/obsidian-auto-note-importer/master/README.md)).
- **Merge de três vias só com uma base comum comprovada** (LiveSync).
- **`status` de drift** entre o banco e a árvore de `.md`, e **`validate --round-trip`** no CI
  ([sql-md-sync](https://raw.githubusercontent.com/jindraregal/sql-md-sync/main/README.md)). O sql-md-sync
  também mostra o caminho inverso, que é relevante para o ticket 22: o banco em execução, mas os `.md` no git
  como formato de sync e merge.

## 5. Reavaliação das já vistas (só contra a pergunta nova)

- **Guild:** continua fora. Não tem vista Markdown nem exportação, e a busca vetorial está desligada no Windows
  ([README](https://raw.githubusercontent.com/mathomhaus/guild/main/README.md)).
- **ai-memory (akitaonrails):** continua com o Markdown como verdade (*"The source of truth is a git-backed wiki
  of ordinary `.md` files"*) e com Windows nativo "Experimental". Fica fora da premissa nova, mas cumpre a
  necessidade funcional: o agente lê pelo índice e o humano edita o `.md`.
- **seamless:** *"Files are the source of truth"*. O SQLite guarda o estado operacional (sessões e tarefas), que
  não tem vista Markdown. Fica fora.
- **beads:** sobe de posição (seção 4.2), porque a premissa nova aceita o Dolt como verdade.
- **Basic Memory:** *"the source of truth is always your files"*. Funcionalmente é o caso "banco para o agente,
  `.md` para o humano", mas com a verdade invertida. Licença AGPL-3.0, 4.090★.
- **Engram, ConPort, mwe-mcp, obsidian-shared-memory-bus, mcp_agent_mail:** a vista não volta, ou não está
  documentado que volte (tabela da seção 3).
- **sqlite-memory:** sobe de posição (seção 4.3). Na varredura 2 ele parecia só "Markdown como fonte", mas o
  banco guarda o conteúdo e materializa os arquivos.
- **Resto da classe (1) da varredura 2** (memsearch, agentcairn, open-zk-kb, obsidian-second-brain etc.): todas
  têm o Markdown como verdade. Não foram reabertas.

## 6. Cauda longa (só vista em busca, sem verificação na fonte)

- **MCPs sobre o LiveSync:** odiak/livesync-workers (13★), suhasvemuri/obsidian-self-mcp, afonsofigs/obsidian-couchdb-mcp,
  kodmis2008/obsidian-livesync-mcp, muhammadkh4n/obsidian-vault-mcp, yaharga/cinderlink-mcp (descrição cita
  "revision"), mushrowan/yamos, bestonephoenix/obsidian-livesync-couchdb-MCP-sidecontainer.
- **Plugins de sync com CouchDB:** couchdb-sync (chrisurf), vaultbridge (com visão de diff de conflito),
  mdfriday-sync, simple-sync-notes, mysync.
- **Memória com vista Obsidian:** Velixar (exporta para Obsidian), MemoryChat (dhawal-ss), coder-engram (inbox de
  revisão), agentage memory, hindsight-obsidian, qdrant-sync.
- **Plugins SQL sobre o vault:** VaultQuery (INSERT/UPDATE com "database-to-file sync"), Obsidian SQLite
  (edição inline num `.db`), obsidian-diy-sync.
- **Infraestrutura:** DoltLite (Dolt embutível como biblioteca C, 286★), SynQLite.

## 7. Recomendação (a decisão é do Gustavo)

1. **Não adotar uma ferramenta de "memória de agentes" como o hub.** Todas as que têm banco e vista Markdown
   descartam, ignoram ou duplicam a edição humana (seção 4.4). Isso viola a decisão do ticket 22 ("a edição
   dele volta para o banco").
2. **O próximo ticket deve escolher entre duas formas:**
   - **(A) Banco replicado com o vault como vista viva** (modelo LiveSync/CouchDB). A favor: o mecanismo de
     conflito é o mais sério encontrado, maduro e com volta automática. Contra: precisa de servidor ou relay;
     o "banco" guarda arquivos, então o agente continua lendo notas; e o MCP fica com um projeto pequeno.
   - **(B) Banco próprio com vista gerada e volta verificada** (modelo obsidian-beads e memo, mais o
     `if_match` do markdown-vault-mcp da §10.2). Cada `.md` carrega um id estável e a revisão ou o hash da
     base. A volta só aplica se a base confere; se não confere, avisa e não grava (o modo `Manual`). O sync do
     banco entre máquinas viria de uma peça pronta: Dolt por um remote git (dispensa servidor) ou um CRDT
     (cr-sqlite).
3. **beads como casa das tarefas, em qualquer das duas.** É a única peça madura (27,6 mil estrelas, MIT, CI
   Windows) que já é banco como verdade, sincroniza pelo GitHub e tem uma vista editável no Obsidian. Antes,
   vale um ticket de pesquisa sobre a vista: ela não gera `.md` no disco.
4. **Fica para o Gustavo uma pergunta de fundo,** que o ticket 22 deixou aberta: se o sync entre as máquinas
   continuar pelo git, o formato que o git junta bem é o `.md` (o sql-md-sync mostra o padrão). Nesse caso, o
   banco seria verdade só dentro de cada máquina.

## 8. Limites

- O limite da API do GitHub sem autenticação (60 por hora no núcleo, 10 por minuto na busca) impediu ler árvores
  de arquivos pela API. As listagens vieram do jsDelivr, e a do LiveSync estava defasada em relação ao `main`.
- O tratamento de `_rev` nas escritas do es617/obsidian-sync-mcp, o comportamento do LiveSync com o Obsidian
  fechado e o Windows de vários MCPs e plugins não foram conferidos (NV).
- **Reddit:** só apareceu por resultado de busca (um snapshot espelhado), sem leitura de tópicos.
- **Registry de MCP:** a busca devolve 100 entradas, com versões repetidas, então a cobertura é parcial.
- As estrelas são um retrato de 04/10/2026. O Fossil não está no GitHub, e a licença e a atividade dele não foram
  conferidas.
