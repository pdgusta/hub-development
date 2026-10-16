---
title: Pesquisa 28, montagem do caminho O3 (banco central com plugin do Obsidian)
data: 2026-10-04
origem: subagente de pesquisa (Claude Code), ticket 28 "Montar: banco central com plugin do Obsidian"
aviso: saída de modelo. Fontes primárias: README, docs e código-fonte brutos (raw.githubusercontent.com), listagens de arquivos pelo jsDelivr (data.jsdelivr.com), API REST do GitHub (metadados e releases, até o limite sem autenticação), o community-plugins.json oficial do Obsidian, a API do registry oficial de MCP, a documentação oficial do PostgreSQL (postgresql.org), do PostgREST, do pgvector, do llama.cpp, do Supabase e do MCP Toolbox for Databases (repositórios oficiais). Nada foi clonado, instalado ou executado. O que não foi conferido na fonte está marcado como **não verificado** (NV). Onde escrevo "inferência", a conclusão sai do código ou da doc citada, mas não foi testada. Pesquisa de montagem: cada lacuna vira "o que falta montar", com opções e esforço grosseiro.
---

# Montagem do caminho O3: banco central com plugin do Obsidian, levantamento de 04/10/2026

## Resumo (uma tela)

1. **O O3 é montável com peças prontas.** No catálogo oficial de plugins do Obsidian (8.405 plugins) há pelo menos
   **quatro famílias** que já fazem as duas direções entre um banco central e o vault, e três delas já trazem um
   mecanismo de conferência de versão:
   - **Trilha A: Postgres puro + `obsidian-postgres-sync`** (PostgREST + pgvector). A nota inteira mora numa linha
     do Postgres, e o plugin já embute cada nota para busca semântica. Já existe uma **gravação condicional**
     (`sync_revision=eq.N`), mas a decisão é "última gravação vence" por mtime. Falta a **base por arquivo**.
   - **Trilha B: Supabase + `Supabase Vault Sync`.** Compara três estados (local, remoto e a última sincronização).
     Com edição dos dois lados, **renomeia a local para `nome (Sync Conflict).md`**, avisa e baixa a remota. A
     subida ainda é um `upsert` cego.
   - **Trilha C: servidor de sync com banco embutido e MCP pronto.** O mais completo é o **Fast Note Sync
     Service** (FNS): binário Go com build Windows, banco SQLite/MySQL/**PostgreSQL** e **MCP nativo** (HTTP
     streamable). Tem histórico de versões, `baseHash` na volta e a estratégia **Manual Merge**, que devolve
     base, servidor e local e abre um modal de resolução. Alternativas da mesma trilha: **Engram** (Postgres +
     Qdrant + MCP, cópia de conflito) e **Havemind** (SQLite, merge de três vias, cópia de conflito, Tailscale
     no desenho).
   - **Achados com o desenho certo e servidor NV:** **Central Vault Sync** (servidor autoritativo com revisões e
     cópias de conflito) e **Pageden** (push com `baseVersion` e `*.conflict.md`).
2. **O MCP do agente está pronto nas três trilhas:**
   - **Trilha A:** o **MCP Toolbox for Databases** (Google, Apache-2.0, binário Windows) aceita ferramentas SQL
     parametrizadas num `tools.yaml`. Uma ferramenta `UPDATE ... WHERE sync_revision = $n RETURNING ...` dá a
     conferência de versão **só com configuração**. Há também Postgres MCP Pro e o MCP oficial do Supabase.
   - **Trilha C:** o FNS já expõe `note_get`, `note_list` e `note_create_or_update`. Falta passar o hash
     esperado na gravação do agente: hoje ela não leva base.
3. **O modo offline vem de graça na vista.** Cada máquina tem o vault inteiro em `.md`. O humano edita offline, o
   plugin enfileira e, na volta, a conferência de base decide: sobe, junta ou gera cópia de conflito. Offline, o
   agente lê e grava os mesmos `.md` locais. Limite: os plugins só rodam com o **Obsidian aberto**. Mitigações:
   a checagem de início de sessão (ticket 08), um cliente headless (o FNS já tem um em Go) ou um daemon próprio.
4. **A busca do agente tem três encaixes, todos viáveis:**
   - **No servidor:** FTS `portuguese` do Postgres + pgvector (híbrido por RRF), exposto como ferramenta MCP.
   - **No FNS:** busca pronta por palavra no `note_list`.
   - **Na vista local:** a camada de busca dos tickets 09/19–21 (memtomem, zvec-grep, ck) sobre os `.md`, que
     funciona offline.
5. **A colisão aparece ao humano** como cópia de conflito ao lado da nota e um `Notice` (Trilhas A, com o
   trabalho a construir, e B; Engram; Havemind), ou como modal de três vias (FNS Manual Merge, SupSync `ask`).
   Para o agente, aparece como recusa da gravação condicional.
6. **O que falta construir é pequeno e localizado** (seção 8): de 0,5 a 3 dias por peça. O maior item opcional é
   um sincronizador sem Obsidian aberto (3 a 5 dias, se não usar o cliente headless do FNS).
7. **Recomendação de montagem (a decisão é do Gustavo):**
   - **ensaiar primeiro a Trilha C com o FNS**: tem mais peças prontas, roda nativo no Windows e já traz MCP,
     histórico e Manual Merge;
   - **em paralelo, a Trilha A** como alternativa de "Postgres puro", com o fork pequeno do plugin;
   - a **Trilha B** fica como opção quando se aceita Supabase (nuvem ou Docker).

## 1. Diagrama da montagem

```
                         ┌───────────────────── servidor (seção 4: desktop Windows, Linux pequeno ou gerenciado) ───────────────────┐
                         │                                                                                                           │
                         │   BANCO = VERDADE                     PORTA HTTP                         PORTA DO AGENTE                  │
                         │   Trilha A: Postgres + pgvector  ◄──  PostgREST (X-Api-Key)              MCP Toolbox / Postgres MCP Pro   │
                         │   Trilha B: Supabase (Postgres)  ◄──  API do Supabase (RLS)              MCP do Supabase / Toolbox        │
                         │   Trilha C: FNS (SQLite|Postgres) ◄─  REST + WebSocket do FNS            MCP nativo do FNS (/api/mcp)     │
                         │        │  linhas: path, content, hash, revisão/versão, (embedding)            ▲  ler / buscar /            │
                         │        └─ conferência de versão: revisão ou baseHash; recusa se a base mudou    │  gravar-se-base-confere    │
                         └──────────────────────────────▲───────────────────────────────▲─────────────────┼───────────────────────────┘
                                                        │ Tailscale (HTTPS)             │                 │
             ┌──────────────────────────────────────────┴─────┐       ┌─────────────────┴───────────────┐ │
             │ MÁQUINA 1 (Windows, NTFS)                      │       │ MÁQUINA 2 (Windows, NTFS)       │ │
             │  Obsidian + plugin de sync (A, B ou C)         │       │  Obsidian + plugin de sync      │ │
             │   ida:  evento modify → fila → sobe c/ base    │       │   (igual)                       │ │
             │   volta: pull por revisão → aplica ou conflito │       │                                 │ │
             │  vault/*.md  = VISTA editável (cópia inteira)  │       │  vault/*.md = VISTA             │ │
             │  agentes (Claude Code, Codex, Copilot):        │       │  agentes: idem                  │ │
             │   online  → MCP do servidor ───────────────────┼───────┼─────────────────────────────────┼─┘
             │   offline → .md locais + busca local (09/21)   │       │                                 │
             │  checagem de início de sessão (ticket 08):     │       │                                 │
             │   conflitos abertos, última sync ok, Obsidian? │       │                                 │
             └────────────────────────────────────────────────┘       └─────────────────────────────────┘
```

## 2. Consultas feitas (registro para auditoria)

### 2.1 Catálogo de plugins do Obsidian

- **C1:** `obsidianmd/obsidian-releases/community-plugins.json`, com 8.405 plugins. Grep (Python) em nome e
  descrição por `postgres|supabase|pocketbase|firebase|mongo|sqlite|mysql|database|sql|couch|appwrite|turso|libsql|electric|powersync|yjs|crdt|self-host|relay|planetscale|server`,
  cruzado com `sync|two-way|bidirection|collab|real-time`. Saíram 86 linhas, e as relevantes estão na seção 3.

### 2.2 Registry oficial de MCP (`registry.modelcontextprotocol.io/v0.1/servers?search=`)

| # | Termo | Resultado útil |
|---|---|---|
| R1 | postgres | Dezenas de servidores. A maioria é só leitura (contextflo, Eszetael, arifulislamat); com escrita: devart, itunified-io, jpka/sw-postgres-mcp ("preview-before-execute"). Nenhum foi conferido além da descrição (NV). |
| R2 | supabase | `com.supabase/mcp` (oficial) e variantes da comunidade |
| R3 | obsidian | es617/obsidian-sync-mcp (já visto na pesquisa 23), cyanheads/obsidian-mcp-server (Local REST API), flowing-abyss/obsidian-hybrid-search e outros, sem banco central |

### 2.3 Fontes brutas lidas (raw.githubusercontent.com, salvo indicação)

| # | Alvo | Arquivos |
|---|---|---|
| F1 | lanjak/obsidian-postgres-sync | README.md, manifest.json, sql/schema.sql, sql/migrations/0.1.1-sync-revision.sql, src/{main,sync,postgrest,conditional-write,push-snapshot,recovery,settings}.ts; árvore pelo jsDelivr; metadados e releases pela API do GitHub |
| F2 | dsnbyte/obsidian-supabase-sync | README.md, docs/SYNC_STRATEGY.md, schema.sql, manifest.json, src/sync-engine.ts, src/supabase-client.ts, src/file-operations.ts (grep); árvore pelo jsDelivr |
| F3 | jaliriogbarrios19/SupSync | README.md |
| F4 | haierkeys/fast-note-sync-service | README.md, docs/REST_API.md, docs/swagger.yaml, config/config.yaml, internal/service/conflict_service.go, internal/routers/websocket_router/ws_note.go, internal/routers/mcp_router/note_tools.go, internal/dao/note_fts_repository.go; árvore pelo jsDelivr; metadados e release 3.6.1 pela API |
| F5 | haierkeys/obsidian-fast-note-sync | README.md, src/i18n/locales/en.ts, src/setting.tsx (grep); árvore pelo jsDelivr; metadados pela API |
| F6 | erichll/go-fast-note-sync | README.md |
| F7 | engram-app/engram e engram-app/Engram-obsidian | README.md (os dois), docker-compose.yml, docs/user-guide.md; metadados pela API |
| F8 | MikolajSapek/havemind (obsidian-havemind) | README.md, docs/using-with-ai-agents.md, docs/pilot/known-limitations.md; metadados pela API |
| F9 | picassio/central-vault-sync | README.md; lista de repositórios do autor pela API (o servidor WebObsidian não é público) |
| F10 | kjoner/litesync, pageden/pageden-obsidian, omaryazeedi/graphite-sync, no-instructions/Relay, piriwata/pubScale, shangeethsivan/Syncidian, yoav6/obsidian-glassine-sync, dreamor/memvault-obsidian, ghloii/reliable-vault-sync | README.md |
| F11 | googleapis/mcp-toolbox (antigo genai-toolbox) | README.md, docs/en/integrations/postgres/tools/postgres-sql.md, docs/en/documentation/configuration/embedding-models/_index.md; árvore pelo jsDelivr |
| F12 | crystaldba/postgres-mcp, supabase-community/supabase-mcp | README.md; metadados do primeiro pela API |
| F13 | PostgREST/postgrest | docs/references/api/tables_views.rst (Update), docs/tutorials/tut0.rst (binário Windows) |
| F14 | pgvector/pgvector | README.md (Windows, Hybrid Search) |
| F15 | ggml-org/llama.cpp | tools/server/README.md (`/embedding`, `--embedding`), docs/install.md (winget) |
| F16 | supabase/supabase | apps/docs/content/guides/self-hosting/docker.mdx, apps/docs/content/guides/platform/billing-on-supabase.mdx |
| F17 | postgresql.org | /download/windows/ ("Interactive installer by EDB"), /docs/current/textsearch-psql.html (`portuguese_stem`) |
| F18 | Repositório local | tickets 08, 14, 25 e 28; pesquisas 05, 13, 18 e 23 |

Não houve busca web (WebSearch) nesta rodada: a descoberta veio do catálogo oficial (C1), do registry (R1–R3)
e da pesquisa 23. A API do GitHub esgotou o limite sem autenticação (60 por hora) no meio do trabalho. Por isso
as estrelas de várias peças ficaram NV.

## 3. As peças

Legenda de status: **pronta** (usa como está), **configurar** (só configuração, SQL ou parâmetro), **construir**
(código novo ou fork).

### 3.1 Trilha A: Postgres puro + obsidian-postgres-sync

| Peça | Status | Evidência |
|---|---|---|
| **Plugin `postgres-sync`** (lanjak/obsidian-postgres-sync, MIT, 2★, v0.1.2 de 31/08/2026, no catálogo oficial, `isDesktopOnly: false`) | pronta para as duas direções; **construir** a conferência de base | Ida: eventos `create/modify/delete/rename` do vault, com *debounce* de 2 s (`schedulePath(file.path, 2_000, "high")`, sync.ts). Volta: `pull` a cada `pullIntervalSeconds` (padrão 30) por `sync_revision > lastSyncRevision`, mais uma reconciliação completa a cada ≥ 5 min (sync.ts 225–233). |
| Gravação condicional já existente | pronta | `writeNoteConditionally` faz `PATCH /notes?id=eq.<id>&sync_revision=eq.<esperada>`; resposta vazia = `"conflict"` (conditional-write.ts). O servidor numera cada gravação por gatilho: `new.sync_revision := nextval(...)` (schema.sql). |
| **Lacuna: a decisão é por mtime** | **construir** | README: *"Last-write-wins by modification time. No conflict resolution beyond that"*. No código: `if (existing.stat.mtime > payload.mtime) return; // local edit is newer - last-write-wins keeps it`, senão `vault.modify(existing, payload.content)` (sync.ts 369–374). `reconciliationAction` devolve `local.mtime > remote.mtime ? "push" : "pull"` (recovery.ts 302–309). Inferência: uma edição offline mais antiga que a da outra máquina é **sobrescrita em silêncio** no pull. A revisão esperada vem do remoto lido na hora (`beforeUpload.remote?.syncRevision`, sync.ts 140–146), não de uma base gravada por arquivo. |
| Postgres + pgvector | configurar | Postgres no Windows: *"Interactive installer by EDB"* (postgresql.org/download/windows). pgvector no Windows compila com `nmake /F Makefile.win` (pgvector README §Windows). |
| PostgREST | configurar | *"distributed as a single binary… macOS, Windows, Linux"*; no Windows, *"All of the DLL files… are available in the windows installation of PostgreSQL"* (tut0.rst). Papéis `web_anon`, `note_writer` e `authenticator` e a chave em `X-Api-Key` vêm prontos no schema.sql. |
| Servidor de embedding | configurar | O plugin exige o endpoint llama.cpp `/embedding` (`isConfigured()` pede `embedUrl`, sync.ts 48–50). O llama.cpp tem `--embedding` e `POST /embedding` (server README) e instala por winget no Windows (docs/install.md). Coluna `vector(768)` por padrão (schema.sql). |
| MCP do agente | **configurar** | MCP Toolbox: ferramenta `type: postgres-sql` com *"pre-defined SQL statement… executed as a prepared statement"* e parâmetros `$1, $2…` (postgres-sql.md); stdio por `--stdio` (README); binário `toolbox.exe` para Windows (README). Alternativas: Postgres MCP Pro (crystaldba, MIT, 3.369★), com `--access-mode=unrestricted` ou `restricted` (só leitura) e `execute_sql` (README); a família de MCPs Postgres do registry (R1, NV). |

### 3.2 Trilha B: Supabase + Supabase Vault Sync (ou SupSync)

| Peça | Status | Evidência |
|---|---|---|
| **Plugin `supabase-vault-sync`** (dsnbyte, MIT, v1.1.3, no catálogo; estrelas NV) | pronta | *"offline-first… bidirectionally synchronizes vault notes to a Supabase PostgreSQL database"*. Mantém um *"local registry of file paths, last-modified timestamps, and SHA-256 hashes"* (README). |
| Conferência na volta (pull) | pronta | *"If a file has been changed on both sides since the last sync, the local version is renamed to `filename (Sync Conflict).ext` and the remote version is downloaded"* (SYNC_STRATEGY.md, princípio 5). No código: `new Notice("Sync Conflict: … changed in both places. Renaming local version to prevent loss.")` e `vault.rename(localFile, conflictPath)` (sync-engine.ts 377–388). |
| Conferência na ida (push) | **construir** (pequeno) | A subida é `upsert` sem filtro de base (file-operations.ts 256–259 e 306–309). O ciclo faz o pull antes da subida (*"SKIP (local is newer, will be uploaded in step 3)"*, SYNC_STRATEGY.md), então a janela de corrida é curta, mas existe (inferência). |
| Banco | configurar | Tabela `obsidian_vault_files(user_id, vault_id, path, content, hash, properties jsonb, title, tags, updated_at, deleted_at)` (schema.sql). Exige Supabase Auth (`REFERENCES auth.users`), então serve Supabase, não Postgres puro. |
| Supabase | configurar | Nuvem: o plano Free dá dois projetos, e *"no projects in your Pro Plan organization will be paused"* indica que os gratuitos podem pausar (billing-on-supabase.mdx). Auto-hospedado: Docker Compose, e no Windows *"Install Docker Desktop"* (self-hosting/docker.mdx). |
| MCP do agente | configurar | MCP oficial do Supabase. No auto-hospedado, *"offers a limited subset of tools and no OAuth 2.1"* (supabase-mcp README). `read_only=true` disponível. Ou o MCP Toolbox apontado para o Postgres do Supabase. |
| Variante: **SupSync** (jaliriogbarrios19, MIT) | pronta | Supabase com *"File locking — automatic lock acquisition when editing"* e *"side-by-side diff modal"*. `Conflict mode`: `local-wins`, `remote-wins` (padrão) ou `ask` (README). |

### 3.3 Trilha C: servidor de sync com banco embutido e MCP

| Peça | Status | Evidência |
|---|---|---|
| **Fast Note Sync Service** (haierkeys, Apache-2.0, Go, 2.395★, release 3.6.1 de 14/08/2026 com `windows-amd64`) | pronta | *"Native support for… SQLite, MySQL, and PostgreSQL"* (README). `database.type: sqlite \| mysql \| postgres` (config.yaml). Histórico por nota, lixeira, backup S3/WebDAV e espelho Git (README). |
| **Plugin Fast Note Sync** (Apache-2.0, 3.047★) | pronta; **configurar** a estratégia | Estratégias de edição offline: *"No Merge, Keep Latest"* (padrão: *"local modifications will be discarded"*), *"Merge Only if Local is Newer"*, *"Force Merge"*, *"Manual Merge… a window will pop up"* (en.ts 84–89). Padrão `offlineSyncStrategy: ""` (setting.tsx 140). **Configurar Manual Merge nas duas máquinas.** |
| Conferência de base no servidor | pronta | A requisição tem `baseHash` e `baseHashMissing` (swagger.yaml). Com `manualMerge` e `serverHash != baseHash`, o servidor *"block[s] the override immediately and return[s] 530"* com `serverContent`, `baseContent` e `serverHash` (ws_note.go 132–163). Quando a junção falha, `CreateConflictFile` *"save[s] the client content as a conflict file"* (conflict_service.go). |
| UI de colisão | pronta | Modal *"Resolve Note Conflicts"* com *"Keep Current"*, *"Overwrite with Copy"* e *"View Side by Side"*, além de aviso *"Conflict copy detected for ${path}. Click to view"* (en.ts 542–562). |
| **MCP do agente** | pronta; **construir** a base na gravação | *"provides both SSE and StreamableHTTP"* em `/api/mcp`, citando Claude Code (README). Ferramentas `note_list` (*"List or search notes"*), `note_get`, `note_create_or_update`, `note_patch_frontmatter`, `note_append` e outras (note_tools.go). **Lacuna:** `note_create_or_update` monta a requisição sem `BaseHash` (note_tools.go 140–150), então a gravação do agente não confere a base. |
| Busca | pronta (palavra) | `note_list` com `keyword`, `searchContent` e `searchMode (path, content, regex)` (REST_API.md 823–825). A doc diz *"SQLite FTS5"*, mas o código usa **Bleve** (`github.com/blevesearch/bleve/v2`, note_fts_repository.go). Não há semântica. |
| Cliente headless | pronta, Windows "não garantido" | go-fast-note-sync: *"Bidirectional sync"* e *"Live file watching… via fsnotify"*. Há binário `windows/amd64`, mas *"not guaranteed to work in production"* (README). |
| Alternativa C2: **Engram** (backend Elixir, PolyForm Small Business 1.0, 10★; plugin MIT, 3★) | pronta | Postgres 18 + Qdrant no compose (`DATABASE_URL: postgresql://…`, `QDRANT_URL`). *"MCP-native · semantic + keyword search · self-hostable"* (README). Colisão: *"your local version is saved beside the note as `your-note (conflict 2026-06-18).md`"* (user-guide.md). Licença source-available, não MIT. |
| Alternativa C3: **Havemind** (Apache-2.0, 2★, v1.5.8) | pronta | *"opaque server (Fastify + SQLite)"*, *"When two people change the same lines, both versions survive and a copy lands in `Havemind Conflicts/`"*, Docker Compose + Tailscale (README). O agente entra **pelos arquivos do vault**: *"it never talks to the Havemind server directly"*, e *"If Obsidian is closed… edits are not pushed"* (using-with-ai-agents.md). |

### 3.4 Achados com o desenho certo e servidor NV (para olhar depois)

- **Central Vault Sync** (picassio, MIT, 0★): *"The server is authoritative: every accepted mutation receives a
  stable entry identity, revision, content hash"*, *"Never silently overwrites a stale server revision"* e
  *"overlaps… become conflict copies"* (README). O servidor WebObsidian não aparece entre os repositórios
  públicos do autor (NV).
- **Pageden Sync**: *"server-owned Markdown workspace for teams and AI agents"*. *"Pushes send the recorded
  `baseVersion`… On a conflict, the local file is left untouched and the server copy is written as
  `*.conflict.md`"* (README). O código do servidor auto-hospedado é NV.
- **LiteSync** (kjoner): revisões por arquivo + SHA-256 + sequência global, *"automatic three-way merge for
  Markdown (diff3)"* e histórico imutável (README). Não tem MCP. O banco do servidor é NV.
- **Cauda (só descrição no catálogo, NV):** Syncidian (SQLite + MCP + GitHub), Graphite Sync (*"validate-first
  merge"*), Glassine Sync (REST), MemVault, Relay (Yjs, servidor `y-sweet` MIT auto-hospedável), PubScale
  (PlanetScale, só publica), Reliable Vault Sync (*"Git-backed server with recoverable conflicts"*).

## 4. Onde o servidor mora (opções)

| Opção | Como monta | A favor | Risco e mitigação |
|---|---|---|---|
| **S1. Desktop Windows pessoal** (o que fica ligado) | Trilha A: Postgres (instalador EDB) + `postgrest.exe` + `llama-server` (winget), como serviços do Windows. Trilha C: `fast-note-sync-service.exe` + SQLite. O notebook chega pelo Tailscale. | Nada novo para manter fora de casa; tudo nativo no Windows; sem custo. | Desktop desligado = notebook offline. Mitigação: o modo offline da seção 5 cobre isso. Risco corporativo do Tailscale no notebook (pesquisa 05). Mitigação: avaliar antes; servidor fora da tailnet da empresa; ou S3. |
| **S2. Linux pequeno** (mini PC, NAS ou VPS) | Docker Compose: FNS, Engram, Havemind e Supabase têm compose oficial. Postgres + PostgREST em contêiner. | Sempre ligado; as duas máquinas ficam iguais. | Custo e manutenção de mais uma máquina. Mitigação: Havemind já documenta *"Docker Compose + Tailscale, tailnet-only"*, e o FNS tem script de um passo (README). |
| **S3. Gerenciado** (Supabase nuvem; Postgres gerenciado) | Trilha B direta; Trilha A sobre qualquer Postgres com pgvector (PostgREST rodando onde for). | Zero manutenção; alcançável das duas máquinas sem Tailscale. | Projeto Free pode pausar (billing-on-supabase.mdx). Mitigação: plano pago ou atividade periódica. O conteúdo das notas fica fora de casa. Mitigação: HTTPS, RLS (Trilha B) e manter dados pessoais fora do hub, como o AGENTS.md já manda. |
| **S4. WSL no desktop** | Mesmo desenho de S2, dentro do WSL. | Usa o compose oficial sem Docker Desktop. | A VM do WSL desliga quando ociosa (`vmIdleTimeout`, pesquisa 05). Mitigação: preferir S1 nativo, ou ajustar o `vmIdleTimeout`. |

## 5. Como funciona o modo offline

1. **A vista já é uma cópia inteira.** Nas três trilhas, cada máquina guarda todos os `.md` no disco. Sem
   servidor, o Obsidian e os agentes continuam lendo e gravando normalmente.
2. **A fila guarda a ida:**
   - **Trilha A:** a fila é em memória, mas a reconciliação na partida e a cada ≥ 5 min recompara tudo por hash
     e mtime (sync.ts 245–298), e falhas repetem com *"capped backoff"* (README).
   - **Trilha B:** *"If you are offline, all changes queue up safely and sync automatically"* (README).
   - **Trilha C:** *"Offline deletions are automatically resolved… upon reconnection"*, e há um *"offline guard"*
     antes de ressuscitar arquivos (en.ts 538–539).
3. **Na reconexão, a conferência de base decide.** Se o servidor ainda está na base, sobe. Se os dois mudaram,
   gera cópia de conflito (B, Engram, Havemind), devolve 530 e abre o modal (FNS Manual Merge), ou, na Trilha A
   depois do fork (seção 8, item A1), gera a cópia.
4. **O agente offline** usa os `.md` locais e a busca local (seção 6, opção 3). Online, usa o MCP. Na Trilha C,
   uma gravação do agente direto nos arquivos sobe pelo plugin com a mesma conferência de base que a do humano.
5. **Limite: o plugin só roda com o Obsidian aberto.** O Havemind diz isso com todas as letras: *"If Obsidian is
   closed… edits are not pushed until you reopen it"*. Há três mitigações, que se combinam:
   - **(a)** a checagem de início de sessão do ticket 08 avisa "Obsidian fechado, fila pendente";
   - **(b)** um cliente headless: o go-fast-note-sync na Trilha C (Windows "não garantido");
   - **(c)** um daemon próprio que porta o `sync.ts` (Trilha A), com o esforço na seção 8.

## 6. Como a busca do agente entra

| Opção | Status | Como |
|---|---|---|
| **1. Híbrida no servidor (Trilhas A e B)** | configurar | O plugin postgres-sync já grava `embedding vector(768)` por nota (schema.sql), *"so the same table doubles as a semantic search index you can query from outside Obsidian"* (README). Somar uma coluna `tsvector` com dicionário `portuguese` (existe `portuguese_stem`, docs do PostgreSQL) e fundir as duas buscas: *"Use together with Postgres full-text search for hybrid search… Reciprocal Rank Fusion"* (pgvector README). Expor como ferramenta `postgres-sql` no MCP Toolbox. O embedding da **pergunta** precisa do mesmo modelo do plugin. O Toolbox só documenta embeddings Gemini (embedding-models), então a busca semântica pede um MCP pequeno próprio (seção 8, item A3). A busca por palavra sai só com configuração. |
| **2. Busca do próprio servidor (Trilha C)** | pronta | `note_list` do MCP do FNS com palavra-chave, conteúdo ou regex (Bleve). O Engram oferece *Semantic*, *Keyword* e *Hybrid* (README do plugin). |
| **3. Camada de busca local sobre a vista** | configurar | A vista é `.md` comum, então as candidatas dos tickets 09/19–21 (memtomem, zvec-grep, ck) indexam a pasta do vault sem saber do banco. Funcionam offline e independem da trilha. |

## 7. Como a colisão aparece para o humano (e para o agente)

| Trilha | Humano | Agente |
|---|---|---|
| A (hoje) | Não aparece: a última gravação vence por mtime. Só os conflitos de maiúsculas e minúsculas geram `Notice` (sync.ts 396–402). | A ferramenta `UPDATE … WHERE sync_revision = $esperada` volta vazia. O agente relê e refaz. |
| A (com o item A1) | Cópia `nota (conflito <máquina> <data>).md` ao lado + `Notice` + entrada numa tabela `conflicts`, que a checagem de sessão lê. | Igual ao de cima. |
| B | `Notice` *"Sync Conflict: … changed in both places"* + arquivo `nome (Sync Conflict).md` (sync-engine.ts). SupSync: modal lado a lado (`ask`). | Com o item B1, a gravação condicional recusa. |
| C (FNS) | Manual Merge: modal com base, servidor e local; ou cópia de conflito + aviso *"Conflict copy detected… Click to view"*, menu *"Note Conflicts"* e contador *"Found ${count} conflicting notes"* (en.ts). | Hoje a gravação não leva base. Com o item C1, recebe a recusa (530 ou erro do MCP). |
| C2/C3 (Engram, Havemind) | Cópia `(conflict <data>).md` ao lado (Engram); pasta `Havemind Conflicts/` + painel Activity com o autor por dispositivo (Havemind). | Engram: MCP (semântica de base NV). Havemind: o agente grava nos arquivos e cai na mesma regra. |

## 8. O que falta construir, com esforço

Estimativas grosseiras para uma pessoa com agente, incluindo testes. Nada aqui foi tentado.

| # | Trilha | Peça | Opções | Esforço |
|---|---|---|---|---|
| A1 | A | **Conferência de base no plugin postgres-sync** | Fork do plugin (o repo é pequeno: `sync.ts` tem 14,9 KB e já há testes em `tests/`). Gravar `baseRevision` e `baseHash` por caminho no `data.json`. Trocar a decisão por mtime por "mudou local desde a base?" × "mudou remoto desde a base?". Nos dois casos, cópia de conflito + `Notice`, sem `vault.modify` por cima. Usar a `baseRevision` gravada no `writeNoteConditionally`. Propor upstream como PR. | 1–3 dias |
| A2 | A | **Ferramentas MCP com conferência de versão** | `tools.yaml` do MCP Toolbox: `ler_nota` (devolve `content` e `sync_revision`); `gravar_nota_se_revisao` (`UPDATE notes SET content=$1, content_hash=encode(sha256(convert_to($1,'UTF8')),'hex'), mtime=<agora ms>, embedding=NULL WHERE path=$2 AND sync_revision=$3 RETURNING sync_revision`); `criar_nota` (o `id` é derivado do SHA-256 do caminho, como em `pathToId`, reproduzível em SQL); `buscar_texto` (FTS). O hash bate com o do plugin, que é SHA-256 hex do texto UTF-8 (`sha256()` em postgrest.ts), por inferência. | 0,5–1 dia |
| A3 | A | **Embedding das gravações do agente e busca semântica** | (a) Um script agendado que preenche `embedding IS NULL` chamando o `/embedding`. (b) Ou um MCP pequeno próprio (Python ou TS, ~200 linhas) que embute a pergunta e consulta o pgvector, substituindo A2. (c) Ou só tornar o embedding opcional no plugin (`isConfigured()` exige `embedUrl`). | (a) 0,5 dia; (b) 1–2 dias; (c) 2 h |
| A4 | A | Histórico de versões | Gatilho `AFTER UPDATE` que copia a linha antiga para `notes_history`. | 2–4 h |
| A5 | A | Busca híbrida | Coluna `tsvector` gerada (`portuguese`) + índice GIN + função SQL de RRF com o pgvector. | 0,5–1 dia |
| B1 | B | Conferência na subida | Trocar o `upsert` por um `UPDATE … WHERE hash = <base>` (ou uma RPC que confere), e cair no ramo de conflito quando nada for atualizado. Colocar máquina e data no nome da cópia (hoje é fixo `(Sync Conflict)`, então duas colisões disputam o mesmo nome). | 0,5–1 dia |
| B2 | B | Ferramentas MCP do agente | As mesmas de A2, sobre `obsidian_vault_files` (chave `user_id, vault_id, path`; coluna `hash`). | 0,5–1 dia |
| C1 | C | **Base na gravação do MCP do FNS** | (a) Patch em Go: parâmetro opcional `expected_hash` em `note_create_or_update`, repassado como `BaseHash`, com recusa clara (PR upstream). (b) Ou um MCP fino na frente: `note_get` → compara → grava. Tem janela de corrida, mas é zero código no servidor. | (a) 0,5–1 dia; (b) 0,5 dia |
| C2 | C | Configuração | Manual Merge nas duas máquinas; Postgres ou SQLite no `config.yaml`; registro desligado (`user.register-is-enable: false`); MCP nos três harnesses (stdio ou HTTP streamable, pesquisas 13 e 18). | 2–4 h |
| X1 | todas | **Checagem de início de sessão** (ticket 08) | Consulta ao servidor (conflitos abertos, última revisão) + estado local (Obsidian aberto? fila?). Hook no Claude Code; o equivalente no Codex e no Copilot é NV (ticket 14). | 1 dia |
| X2 | todas | Sincronizador sem Obsidian aberto (opcional) | (a) Aceitar e avisar (X1). (b) Trilha C: go-fast-note-sync no Windows (testar). (c) Trilha A: daemon Node que porta `sync.ts` com `chokidar`, como tarefa agendada. | (a) 0; (b) 0,5 dia de ensaio; (c) 3–5 dias |

## 9. Riscos registrados (com mitigação)

- **Projetos pequenos:** postgres-sync (2★), Havemind (2★), Engram (3★ e 10★), Central Vault Sync (0★).
  Mitigação: código curto e MIT ou Apache (fork viável); o FNS (2,4 mil e 3 mil ★) é a base mais madura.
- **O padrão do FNS descarta edição local** (*"local modifications will be discarded"*). Mitigação: Manual Merge
  configurado e conferido na checagem de sessão.
- **A doc e o código do FNS divergem na busca** (FTS5 × Bleve). Mitigação: tratar a busca do FNS como "por
  palavra" e somar a busca local.
- **Windows não testado no CI** dos plugins (NV em todos). Mitigação: os plugins rodam dentro do Obsidian
  desktop; ensaiar nas duas máquinas antes de ligar o hub real.
- **Licença do Engram** (PolyForm Small Business): uso pessoal parece coberto (*"free for organizations"* pequenas;
  o texto integral é NV).
- **Dados no servidor em texto claro** (Havemind e FNS; Havemind diz isso explicitamente). Mitigação: servidor
  só na tailnet, backup cifrado, sem dados pessoais no hub.

## 10. Recomendação (a decisão é do Gustavo)

1. **Ensaiar primeiro a Trilha C com o FNS (S1 ou S2).** Reúne o maior número de peças prontas: banco
   Postgres ou SQLite, binário Windows, MCP nativo, histórico, `baseHash` e Manual Merge com modal. A
   construção é a menor: C1 + C2 + X1, cerca de 2 dias.
2. **A Trilha A como alternativa de "Postgres puro e meu"**, com A1 + A2 + X1 (cerca de 3–5 dias). É a que dá ao
   agente o banco mais "adequado" (SQL e pgvector direto) e reaproveita o embedding que o plugin já faz.
3. **A Trilha B** quando o Supabase for aceito (nuvem ou Docker): tem a melhor colisão pronta na volta, e falta
   B1 + B2.
4. Em todas as trilhas, a **busca local sobre a vista** cobre o offline do agente sem peça nova.

## 11. Limites

- A API do GitHub sem autenticação esgotou: estrelas e datas de supabase-vault-sync, SupSync, LiteSync, Pageden e
  da cauda são NV.
- Não conferi: o comportamento real no Windows de nenhum plugin; o servidor WebObsidian (Central Vault Sync) nem
  o do Pageden; a semântica de base do MCP do Engram; o texto integral da licença PolyForm; o
  `max-affected` e outros detalhes do PostgREST além do `PATCH` com filtros.
- A estimativa de esforço é grosseira e não inclui o ensaio nas duas máquinas.
