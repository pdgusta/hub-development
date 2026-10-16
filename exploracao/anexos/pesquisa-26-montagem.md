---
title: Pesquisa 26, montagem do caminho O1 (CouchDB, LiveSync e MCP)
data: 2026-10-04
origem: subagente de pesquisa (Claude Code), ticket 26 "Montar: CouchDB, LiveSync e MCP"
aviso: saída de modelo. Fontes primárias: README, docs e código-fonte brutos (raw.githubusercontent.com) do vrtmrz/obsidian-livesync, vrtmrz/livesync-commonlib (no commit fixado pelo submódulo do es617), es617/obsidian-sync-mcp, odiak/livesync-workers e pouchdb/pouchdb; docs RST do apache/couchdb; API REST do GitHub (metadados, árvores de arquivos); registry do npm; páginas oficiais de MCP do Claude Code, do Codex, do VS Code e do Copilot CLI. Nada foi clonado, instalado ou executado. O que não foi conferido na fonte está marcado como **não verificado** (NV). Onde escrevo "inferência", a conclusão sai do código ou da doc citada, mas não foi testada. Pesquisa de montagem: lacuna vira "o que falta montar", com opções e esforço.
---

# Montagem do caminho O1: CouchDB como verdade, LiveSync como vista, MCP para o agente

## Resumo (uma tela)

1. **Quase tudo existe pronto.** CouchDB (instalador Windows com serviço), o plugin LiveSync (vista de mão dupla
   no vault, com árvore de revisões, merge de três vias e diálogo de conflito), um MCP que grava no mesmo banco
   pela biblioteca do próprio LiveSync (es617/obsidian-sync-mcp, HTTP, publicado no npm e no GHCR) e os três
   agentes (Claude Code, Codex, Copilot) aceitam MCP por HTTP.
2. **A peça nova mais útil:** o LiveSync tem agora um **CLI oficial** (`src/apps/cli`) com `cat`, `put`, `info`
   (mostra conflitos), `resolve`, `cat-rev` e um `daemon` que espelha banco e pasta sem o Obsidian aberto.
3. **A lacuna principal é a revisão na escrita do agente.** O es617 diz *"No conflict resolution… last write
   wins"*. No código, a escrita lê o `_rev` atual logo antes de gravar. Mas a função de baixo
   (`putDBEntry`) já aceita um `conflictBaseRev`, e o PouchDB, com `force: true`, grava como **filho** dessa
   revisão (`new_edits: false`). Inferência: passar a revisão que o agente leu faz uma escrita atrasada virar
   **um ramo de conflito no banco**, que o LiveSync mostra ao Gustavo no diálogo de merge. É uma alteração
   pequena num fork ou PR do es617 (estimativa: 1 a 2 dias, com teste).
4. **Alternativa pronta para a guarda de revisão:** o odiak/livesync-workers já exige `expectedContentHash`
   no `writeNote` e traz busca BM25 e semântica, mas roda só na Cloudflare e substitui o CouchDB por um
   subconjunto compatível, sem E2EE.
5. **Onde o servidor mora:** cinco opções viáveis (seção 4). A mais simples com os recursos já disponíveis é
   CouchDB + MCP em container numa das máquinas, alcançado pela outra via Tailscale (o compose oficial do
   LiveSync já tem perfil `tailscale`, testado em Docker Desktop for Windows).
6. **Busca do agente:** o es617 não tem busca de texto (só metadados). Caminho mais curto: buscar **no vault**
   em disco (o LiveSync materializa os `.md`) com a camada de busca da pesquisa 21, e gravar pelo MCP.
7. **O que falta construir** (seção 7): guarda de revisão no MCP (P), configuração e serviço no Windows (P),
   ligação dos três agentes (P), busca (P a M, conforme a opção), aviso de conflito ao agente (P).
   P = horas a 2 dias; M = 3 a 7 dias.

## 1. Diagrama da montagem

```
 Máquina A (Windows)                               Máquina B (Windows)
 ┌───────────────────────────────┐                 ┌───────────────────────────────┐
 │ Obsidian + LiveSync (plugin)  │                 │ Obsidian + LiveSync (plugin)  │
 │   vault .md  <->  PouchDB local│                 │   vault .md  <->  PouchDB local│
 │        ^ busca (rg / pesq.21) │                 │        ^ busca (rg / pesq.21) │
 │ Claude Code / Codex / Copilot │                 │ Claude Code / Codex / Copilot │
 │   leitura: vault em disco     │                 │   leitura: vault em disco     │
 │   escrita: MCP (HTTP) --------+--------+        │   escrita: MCP (HTTP) --------+--+
 └──────────────┬────────────────┘        |        └──────────────┬────────────────┘  |
                | replicação CouchDB      |                       | replicação        |
                | (HTTPS via Tailscale)   v                       v                   |
          ┌─────────────────────────────────────────────────────────────┐            |
          │ Servidor (opções na seção 4)                                 │ <----------+
          │  CouchDB  = verdade (árvore de revisões, _conflicts)         │
          │  es617/obsidian-sync-mcp (fork com guarda de revisão)        │
          │     DirectFileManipulator -> putDBEntry(conflictBaseRev)     │
          └─────────────────────────────────────────────────────────────┘
 Colisão: a escrita atrasada vira ramo no CouchDB -> replica -> LiveSync tenta merge de três vias
          -> se não for seguro, abre o diálogo de conflito no Obsidian do Gustavo.
```

## 2. As peças

| # | Peça | Status | O que existe e como encaixa | Evidência |
|---|---|---|---|---|
| P1 | **CouchDB** (verdade) | configurar | Instalador MSI para Windows, com instalação silenciosa e serviço (`INSTALLSERVICE=1`); ou o compose do LiveSync (testado em Docker Desktop for Windows). Inicialização com `couchdb-init.sh` (CORS, auth, limites). | [windows.rst](https://raw.githubusercontent.com/apache/couchdb/main/src/docs/src/install/windows.rst): *"msiexec /i apache-couchdb-3.0.0.msi /quiet INSTALLSERVICE=1 ADMINUSER=admin ADMINPASSWORD=hunter2"*; [docker/README.md](https://raw.githubusercontent.com/vrtmrz/obsidian-livesync/main/docker/README.md): *"Tested on Docker Desktop for Windows (Docker 29.2, Compose v5, WSL2 backend)"* |
| P2 | **Plugin LiveSync** (vista de mão dupla) | pronta / configurar | Plugin do Obsidian (12.648★, MIT). Vault editável; a edição volta ao banco. Conflito por árvore de revisões, merge de três vias só com base comum; senão, pergunta. | [specs_conflict_resolution.md](https://raw.githubusercontent.com/vrtmrz/obsidian-livesync/main/docs/specs_conflict_resolution.md), tabela "Resolution patterns"; pesquisa 23, §4.1 |
| P3 | **MCP do agente**: es617/obsidian-sync-mcp | configurar + construir (guarda de revisão) | HTTP (FastMCP), modo CouchDB pela `livesync-commonlib`, E2EE suportado, `WRITE_FOLDERS`, `READ_ONLY`, `MCP_INSTRUCTIONS_FILE`, OAuth ou `Bearer`. Publicado: npm `obsidian-sync-mcp` 0.7.3 e imagem `ghcr.io/es617/obsidian-sync-mcp`. 59★, MIT, último push 2026-10-04. | [README](https://raw.githubusercontent.com/es617/obsidian-sync-mcp/main/README.md); registry npm (`latest: 0.7.3`) |
| P4 | **Guarda de revisão na escrita** | construir (P) | Ver seção 3. | [vault.ts](https://raw.githubusercontent.com/es617/obsidian-sync-mcp/main/src/vault.ts); [EntryManagerImpls.ts](https://raw.githubusercontent.com/vrtmrz/livesync-commonlib/50d4ab9c1a7d4f59ab29c7555b8dfb2d69555e92/src/managers/EntryManager/EntryManagerImpls.ts) |
| P5 | **CLI oficial do LiveSync** | pronta (construir do fonte) | `cat`, `put`, `push`, `pull`, `ls` (marca `*` em conflito), `info` (lista `conflicts`), `resolve <path> <rev>`, `cat-rev`, `mirror`, `daemon`. Mesmo núcleo do plugin. Não está no npm (registry: "Not found"); build do fonte ou Docker. | [src/apps/cli/README.md](https://raw.githubusercontent.com/vrtmrz/obsidian-livesync/main/src/apps/cli/README.md): *"Command-line version of Self-hosted LiveSync plug-in for syncing vaults without Obsidian"*; *"Cross-platform (Windows, macOS, Linux)"* |
| P6 | **Rede entre as máquinas** | configurar | Perfil `tailscale` no compose do LiveSync, com `ts-serve.json` fazendo proxy HTTPS para `127.0.0.1:5984`. O es617 sugere `tailscale funnel 8787` para o MCP. | [docker/README.md](https://raw.githubusercontent.com/vrtmrz/obsidian-livesync/main/docker/README.md): *"With Tailscale (no domain needed, private mesh or public Funnel)"*; [ts-serve.json](https://raw.githubusercontent.com/vrtmrz/obsidian-livesync/main/docker/config/ts-serve.json) |
| P7 | **Agentes** (Claude Code, Codex, Copilot) | configurar | Os três aceitam MCP por HTTP: `claude mcp add --transport http <name> <url>`; Codex "Streamable HTTP servers" com `url` e `bearer_token_env_var`; VS Code `"type": "http"`; Copilot CLI `copilot mcp add --transport http SERVER-NAME URL`. | [Claude Code MCP](https://code.claude.com/docs/en/mcp.md); [Codex MCP](https://developers.openai.com/codex/mcp); [VS Code MCP](https://code.visualstudio.com/docs/copilot/customization/mcp-servers); [Copilot CLI](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/use-copilot-cli) |
| P8 | **Busca do agente** | configurar ou construir | Ver seção 5. | [ARCHITECTURE.md do es617](https://raw.githubusercontent.com/es617/obsidian-sync-mcp/main/ARCHITECTURE.md): *"(no full-text search — metadata only)"* |
| P9 | **Aviso de colisão ao humano** | pronta | Diálogo de merge, aviso no arquivo ativo, comandos "Resolve if conflicted." e "Pick a file to resolve conflict", e a inspeção "Inspect conflicts and file/database differences". | specs_conflict_resolution.md, "Interactive dialogue policy"; [settings.md](https://raw.githubusercontent.com/vrtmrz/obsidian-livesync/main/docs/settings.md), linhas 686-703 e 860-864 |

### 2.1 Alternativas encontradas

| Peça alternativa | O que traz | Diferença para o O1 | Evidência |
|---|---|---|---|
| **odiak/livesync-workers** (13★, MIT, push 2026-10-03) | Backend compatível com LiveSync + MCP com 11 ferramentas, busca BM25 e semântica, `writeNote` com `expectedContentHash` | Roda só na Cloudflare (Durable Object SQLite), implementa *"the subset of the CouchDB API that the plugin uses, not CouchDB in general"*; E2EE **tem de ficar desligado** | [README](https://raw.githubusercontent.com/odiak/livesync-workers/main/README.md); [mcp/index.ts](https://raw.githubusercontent.com/odiak/livesync-workers/main/packages/livesync-workers/src/mcp/index.ts), linhas 325-353 |
| **CLI do LiveSync como "MCP de pobre"** | Uma skill ou um wrapper que chama `livesync-cli cat/put/info/resolve` | Sem servidor MCP; o agente roda o comando. `info` já mostra conflitos | CLI README |
| Cauda longa (só metadados da API do GitHub): yaharga/cinderlink-mcp (0★, sem licença, descrição cita "revision"), afonsofigs/obsidian-couchdb-mcp (1★), kodmis2008/obsidian-livesync-mcp (0★), muhammadkh4n/obsidian-vault-mcp (0★), suhasvemuri/obsidian-self-mcp (3★), mushrowan/yamos (9★) | MCPs sobre CouchDB/LiveSync | README e tratamento de revisão: **NV** (o README do cinderlink veio vazio pelo raw) | API REST do GitHub, 2026-10-04 |

## 3. Como a gravação do agente respeita a revisão

**O que o es617 faz hoje (código):** `writeNote` chama `manipulator.put(...)` sem revisão
([vault.ts](https://raw.githubusercontent.com/es617/obsidian-sync-mcp/main/src/vault.ts), linhas 226-247).
O `put` do `DirectFileManipulatorV2` chama `liveSyncLocalDB.putDBEntry(putDoc)` sem `conflictBaseRev`
([DirectFileManipulatorV2.ts](https://raw.githubusercontent.com/vrtmrz/livesync-commonlib/50d4ab9c1a7d4f59ab29c7555b8dfb2d69555e92/src/API/DirectFileManipulatorV2.ts), linhas 376-401).
Em `putDBEntry`, sem base, o código lê o documento atual e usa o `_rev` dele; depois grava com
`localDatabase.put(newDoc, { force: true })`
([EntryManagerImpls.ts](https://raw.githubusercontent.com/vrtmrz/livesync-commonlib/50d4ab9c1a7d4f59ab29c7555b8dfb2d69555e92/src/managers/EntryManager/EntryManagerImpls.ts), linhas 207-221).
Resultado: a escrita é filha da revisão vencedora do momento. Se o Gustavo editou entre a leitura e a escrita do
agente, a edição dele é sobrescrita. O próprio README confirma: *"No conflict resolution. If an agent and Obsidian
edit the same note simultaneously, last write wins."* O `edit_note` lê e grava em sequência
([tools.ts](https://raw.githubusercontent.com/es617/obsidian-sync-mcp/main/src/tools.ts), linhas 246-284), com a
mesma janela.

**O gancho que já existe:** `putDBEntry(note, onlyChunks?, conflictBaseRev?)`. Com `conflictBaseRev`, o código usa
essa revisão em vez da atual (linhas 209-210). E o PouchDB, com `force: true` e `_rev`, transforma a escrita em
`new_edits: false` com `_revisions = {start: n+1, ids: [novo, antigo]}`
([adapter.js do pouchdb-core](https://raw.githubusercontent.com/pouchdb/pouchdb/master/packages/node_modules/pouchdb-core/src/adapter.js),
linhas 243-267). Inferência: se a base que o agente leu não for mais a folha atual, o CouchDB guarda **duas folhas**
(um conflito), em vez de recusar com 409. Isso é exatamente o que o LiveSync sabe tratar (seção 6).

**Opções para montar (nenhuma descartada):**

| Opção | Como | Efeito na colisão | Esforço |
|---|---|---|---|
| **R1. Ramo de conflito** (recomendada) | Fork ou PR no es617: `read_note` devolve o `_rev` (o `get` do manipulador traz o documento; presença de `_rev` no retorno: inferência); `write_note`/`edit_note` aceitam `base_rev` e chamam `liveSyncLocalDB.putDBEntry(doc, false, base_rev)` | A escrita atrasada vira ramo; o LiveSync faz merge de três vias se as mudanças não se sobrepõem, senão abre o diálogo para o Gustavo. Nada se perde | P (1-2 dias com teste de integração) |
| **R2. Recusa com aviso** | Antes de gravar, compara `_rev` (ou hash do conteúdo) com o que o agente leu; se diferente, devolve erro e o agente relê | Nada diverge; o agente refaz. Janela residual entre a comparação e o `put` (pequena; o `putDBEntry` serializa por arquivo, linha 207) | P (horas) |
| **R3. Usar o odiak** | `writeNote` com `expectedContentHash` já pronto | Recusa se o hash não confere | configurar; muda o servidor (seção 4, S5) |
| **R4. Escrita só em pasta própria** | `WRITE_FOLDERS=Inbox` no es617 (pronto) | Reduz a colisão a quase zero, sem resolvê-la | configurar (minutos) |
| **R5. CLI do LiveSync** | O agente grava pelo `livesync-cli put` num banco local que replica | Escrita via o mesmo núcleo do plugin; o tratamento de base na escrita pelo CLI é **NV** | P a M |

R1 + R4 juntas dão a defesa em camadas: a pasta própria evita a maioria das colisões, e a revisão protege o resto.

## 4. Onde o servidor mora

| Opção | Como | Alcance das máquinas | Prós | Riscos e mitigação |
|---|---|---|---|---|
| **S1. Container numa das máquinas** (recomendada para começar) | `docker compose --profile tailscale up -d` do `docker/` do LiveSync, mais o container do es617 (`ghcr.io/es617/obsidian-sync-mcp`); ou o `docker-compose.yml` do es617 (CouchDB + MCP) | Tailscale: HTTPS na tailnet, sem domínio | Pronto, testado em Docker Desktop for Windows; tudo reconstruível | A outra máquina depende dessa ligada. Mitigação: cada plugin tem PouchDB local e sincroniza depois (inferência pela arquitetura "PouchDB local"; comportamento offline: NV); backup do volume (`docker/README.md`, "Data & Backup") |
| **S2. CouchDB nativo numa das máquinas** | MSI com `INSTALLSERVICE=1`; es617 por `npx obsidian-sync-mcp` ou Docker | Tailscale (`tailscale serve` para 5984 e 8787) | Sem Docker | es617 no Windows nativo: **NV** (CI só `ubuntu-latest`; o README pede WSL ou Git Bash só para o `setup.sh`). Mitigação: rodar o MCP em container ou WSL |
| **S3. Um CouchDB em cada máquina, replicação mestre-mestre** | Duas tarefas de replicação contínua em sentidos opostos; plugin e MCP apontam para o `localhost` | Tailscale entre os dois CouchDB | Sem ponto único; cada máquina trabalha sozinha | Conflitos entre as máquinas viram folhas na árvore, que o LiveSync já trata. Risco: documentos de controle do LiveSync (milestone, lock) replicados entre dois remotos: compatibilidade **NV**. Mitigação: testar num vault descartável. Fonte: [replication/intro.rst](https://raw.githubusercontent.com/apache/couchdb/main/src/docs/src/replication/intro.rst), *"Master - Master replication… two replication tasks in opposite direction"* |
| **S4. VPS / Fly.io** | `deploy/setup.sh` do es617, opção 1 (CouchDB + MCP), ou `docs/setup_flyio.md` do LiveSync | Internet com HTTPS (ou Tailscale na VPS) | Sempre ligado; ~US$ 3-4/mês segundo o es617 | Dados fora das máquinas: com E2EE do LiveSync o servidor guarda cifrado, e o MCP precisa da passphrase. Script exige bash (WSL ou Git Bash) |
| **S5. Serviço gerenciado** | IBM Cloudant Lite (`docs/setup_cloudant.md`) com o es617 apontando para ele; ou odiak/livesync-workers na Cloudflare | Internet | Zero manutenção | Cloudant: o doc do Fly.io registra *"we started to experience problems related to our IBM Cloudant account"*; compatibilidade do es617 com Cloudant: NV. odiak: não é CouchDB, sem E2EE |

## 5. Como a busca do agente entra

O es617 tem `list_notes` (filtro por pasta, nome, tag, data), `list_tags`, `list_folders` e `get_note_metadata`
(links e backlinks), mas não busca texto: o índice é *"metadata only"* e o FlexSearch foi removido
(ARCHITECTURE.md; o `search_vault` ainda citado ali não aparece no `tools.ts` atual nem na tabela do README).

| Opção | Como | Esforço |
|---|---|---|
| **B1. Busca no vault em disco** (recomendada) | O LiveSync materializa os `.md` em cada máquina; o agente lê e busca com `rg` ou a camada escolhida na pesquisa 21 (memtomem, ck, zvec-grep, markdown-vault-mcp) e grava pelo MCP | configurar. Atraso de índice = latência da replicação |
| **B2. Espelho sem Obsidian** | `livesync-cli daemon --vault <pasta>` mantém uma pasta espelho junto ao servidor, e a busca roda sobre ela | P. CLI Windows: CI só Ubuntu, **NV** |
| **B3. Busca dentro do MCP** | No fork do es617, indexar o conteúdo que o `_changes` já entrega (`index-sync.ts`) com um índice de texto; nova ferramenta `search_notes` | M |
| **B4. odiak/livesync-workers** | `searchNotes` (semântica) e `grepNotes` (BM25) prontos | configurar; implica S5 |
| B5. Busca no próprio CouchDB (views/Mango) | Impraticável direto: o conteúdo está em chunks e, com E2EE, cifrado (pesquisa 23, §4.1). Só como índice derivado (B3) | — |

## 6. Como a colisão aparece para o Gustavo

1. **No banco:** com a guarda R1, a escrita atrasada do agente vira uma segunda folha. O CouchDB escolhe um
   vencedor determinístico e lista as outras em `_conflicts`
   ([conflicts.rst](https://raw.githubusercontent.com/apache/couchdb/main/src/docs/src/replication/conflicts.rst)).
2. **No LiveSync:** se as mudanças não se sobrepõem e há base comum, merge de três vias conservador; se
   sobrepõem, se falta a base, ou se um lado apagou o que o outro mudou, *"Ask the user"* (tabela "Resolution
   patterns").
3. **Na tela:** diálogo de merge com comparação; aviso no arquivo ativo *"This file has unresolved conflicts."*;
   **Not now** adia, mas o aviso continua (*"Postponement therefore does not make the conflict invisible"*);
   comando "Pick a file to resolve conflict" para varrer; "Inspect conflicts and file/database differences" na
   manutenção (settings.md).
4. **Edição em andamento no Obsidian:** se o arquivo local difere da revisão que o dispositivo registrou, o
   LiveSync *"Preserve the edit as a child of that exact revision"*, e não sobrescreve.
5. **Para o agente:** `livesync-cli info <path>` lista `conflicts`; `ls` marca `*`. Uma ferramenta
   `get_conflicts` no fork do MCP é pequena (P).
6. **Configurações a manter:** "Always overwrite with a newer file" desligado (é *"Testing only"*). Atenção:
   em **binários** o LiveSync ainda escolhe o mais novo por mtime (*"existing behaviour, not a new 1.0
   guarantee"*). Mitigação: o agente grava só `.md`, e o es617 só expõe texto.

## 7. O que falta construir, com esforço

| # | Item | Opções | Esforço |
|---|---|---|---|
| F1 | Guarda de revisão no MCP | R1 (ramo de conflito) ou R2 (recusa), num fork ou PR do es617 | P (horas a 2 dias) |
| F2 | Servidor de pé | S1 com compose + Tailscale; ou S2, S3, S4, S5 | P (meio dia) |
| F3 | Ligar os três agentes ao MCP | `claude mcp add --transport http`, `config.toml` do Codex, `mcp.json` do VS Code / `copilot mcp add` | P (horas) |
| F4 | Busca | B1 (configurar), B2 (P), B3 (M), B4 (configurar, muda servidor) | P a M |
| F5 | Aviso de conflito ao agente | Ferramenta `get_conflicts` no fork, ou skill com `livesync-cli info` | P |
| F6 | Regras do agente | `MCP_INSTRUCTIONS_FILE` + `WRITE_FOLDERS` (prontos no es617) | configurar |
| F7 | Validação no Windows | es617 e CLI no Windows nativo são NV; rodar em container ou WSL até conferir | P (teste, a pedido do Gustavo) |
| F8 | Backup do banco | Volume Docker ou cópia do diretório do CouchDB; `cat-rev`/`pull-rev` do CLI para restaurar versões | P |

## 8. Pontos não verificados

- Presença de `_rev` no objeto devolvido por `manipulator.get` do `DirectFileManipulatorV2` (inferência pelo uso de
  PouchDB; não li a função até o fim).
- Comportamento real da escrita com `conflictBaseRev` desatualizado no CouchDB remoto (inferido do código do PouchDB;
  não testado).
- es617 e o CLI do LiveSync no Windows nativo (CI só Ubuntu).
- Comportamento do LiveSync com o Obsidian fechado e o modo offline do plugin.
- Replicação mestre-mestre (S3) com os documentos de controle do LiveSync.
- README e revisão dos MCPs da cauda longa.
- A página do Copilot CLI e a do Codex foram lidas em HTML (sem resumo de modelo), só nos trechos citados.

## 9. Consultas e fontes

**Arquivos brutos lidos (raw.githubusercontent.com):**
- es617/obsidian-sync-mcp `main`: `README.md`, `ARCHITECTURE.md`, `src/vault.ts`, `src/tools.ts`, `src/search.ts`,
  `package.json`, `.github/workflows/cicd.yml`.
- vrtmrz/livesync-commonlib no commit `50d4ab9c` (submódulo do es617): `src/API/DirectFileManipulator.ts`,
  `src/API/DirectFileManipulatorV2.ts`, `src/pouchdb/LiveSyncLocalDB.ts`, `src/pouchdb/LiveSyncDBFunctions.ts`,
  `src/managers/EntryManager/EntryManager.ts`, `src/managers/EntryManager/EntryManagerImpls.ts`.
- vrtmrz/obsidian-livesync `main`: `README.md`, `src/apps/cli/README.md`, `src/apps/cli/package.json`,
  `docker/README.md`, `docker/docker-compose.yml`, `docker/config/ts-serve.json`, `docs/setup_own_server.md`,
  `docs/specs_conflict_resolution.md`, `docs/settings.md`, `docs/setup_flyio.md`, `docs/setup_cloudant.md`,
  `.github/workflows/cli-e2e.yml`.
- pouchdb/pouchdb `master`: `packages/node_modules/pouchdb-core/src/adapter.js`.
- apache/couchdb `main`: `src/docs/src/install/windows.rst`, `src/docs/src/replication/intro.rst`,
  `src/docs/src/replication/conflicts.rst`.
- odiak/livesync-workers `main`: `README.md`, `packages/livesync-workers/src/mcp/index.ts`.
- yaharga/cinderlink-mcp `main`: `README.md` (veio vazio).

**API do GitHub:** árvores recursivas de es617/obsidian-sync-mcp, vrtmrz/obsidian-livesync,
vrtmrz/livesync-commonlib (`50d4ab9c`) e odiak/livesync-workers; conteúdo de `lib/` do es617 (SHA do submódulo);
metadados (estrelas, licença, último push) de 9 repositórios: es617/obsidian-sync-mcp, vrtmrz/obsidian-livesync,
odiak/livesync-workers, suhasvemuri/obsidian-self-mcp, afonsofigs/obsidian-couchdb-mcp,
kodmis2008/obsidian-livesync-mcp, muhammadkh4n/obsidian-vault-mcp, yaharga/cinderlink-mcp, mushrowan/yamos.

**Registry do npm:** `self-hosted-livesync-cli` (não encontrado), `@vrtmrz/livesync-commonlib` (`latest` 0.1.35),
`obsidian-sync-mcp` (`latest` 0.7.3).

**Docs oficiais de agentes:** `code.claude.com/docs/en/mcp.md` (Markdown);
`developers.openai.com/codex/mcp`, `code.visualstudio.com/docs/copilot/customization/mcp-servers` e
`docs.github.com/en/copilot/how-tos/use-copilot-agents/use-copilot-cli` (HTML, trechos por grep).

**Reaproveitado:** `exploracao/anexos/pesquisa-23-banco-com-vista.md` (§3, §4.1, §6, §8), sem refazer as consultas.
