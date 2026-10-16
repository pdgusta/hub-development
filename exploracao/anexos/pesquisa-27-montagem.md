---
title: Pesquisa 27, montagem do caminho O2 (Dolt como servidor central)
data: 2026-10-04
origem: subagente de pesquisa (Claude Code), ticket 27 "Montar: Dolt como servidor central"
aviso: saída de modelo. Fontes primárias: páginas `.md` da documentação oficial do Dolt (dolthub.com/docs, a partir do índice oficial `llms.txt`), posts do blog oficial da DoltHub baixados em HTML e convertidos para texto localmente, README e docs brutos (raw.githubusercontent.com) de dolthub/dolt-mcp, dolthub/doltlite, dolthub/dolt-workbench, gastownhall/beads e uppinote20/obsidian-auto-note-importer, API REST do GitHub (metadados e releases, até esgotar a cota anônima) e o community-plugins.json oficial do Obsidian. Material reaproveitado das pesquisas 05, 13, 18, 21, 23 e 24, sem refazer. Nada foi clonado, instalado ou executado. O que não foi conferido na fonte está marcado como **não verificado** (NV). Onde escrevo "inferência", a conclusão sai da doc citada, mas não foi testada. Estimativas de esforço são grosseiras, em dias de trabalho de um agente com o Gustavo revisando.
---

# Montagem do caminho O2: Dolt como servidor central

## Resumo (uma tela)

1. **O núcleo está pronto.** O Dolt já entrega o que o caminho pede: banco SQL com commits, merge de três vias
   por célula e colisão visível em `dolt_conflicts_<tabela>`, junção desfeita sozinha em autocommit, servidor
   (`dolt sql-server`) para vários clientes, clone/pull/push para trabalhar offline e instalador Windows
   (winget, choco, scoop, `.msi`). Fonte: docs oficiais citadas na seção 3.
2. **Peça nova que muda a montagem: o MCP já vem dentro do servidor.** O `config.yaml` do `dolt sql-server`
   tem um bloco `mcp_server` que sobe o **dolthub/dolt-mcp** em HTTP na porta 7007; a doc mostra
   `claude mcp add -t http dolt-mcp http://localhost:7007/mcp`. O dolt-mcp também existe como binário
   Windows (`dolt-mcp-server-windows-amd64.zip`, v0.3.8) em stdio ou HTTP, com 40+ ferramentas (query, exec,
   branch, commit, diff, merge status, push, pull). Claude Code, Codex e Copilot falam MCP por stdio e HTTP
   (pesquisas 13 e 18).
3. **O servidor central também é o remote.** Com `remotesapi.port` no `config.yaml`, um `dolt sql-server`
   aceita `clone`, `push`, `pull` e `fetch`. Assim, a máquina pessoal pode ser, ao mesmo tempo, o banco ao
   vivo e o ponto de encontro, alcançada pela tailnet. Alternativas prontas para o ponto de encontro: o
   GitHub privado (remote git, `refs/dolt/data`), DoltHub privado (grátis até 1 GB), DoltLab (DoltHub
   próprio), S3/R2/MinIO, SSH, pasta de rede, ou Hosted Dolt (gerenciado).
4. **Modo offline:** cada máquina roda o seu próprio `dolt sql-server` local, e os agentes falam sempre com
   `localhost`. A sincronização é `dolt_pull`/`dolt_push` contra o remote central. Sem rede, nada muda para
   o agente; só o estado do sync fica "atrasado". É o modelo que a própria doc chama de "Offline First".
5. **A colisão para e avisa por construção:** pull com colisão em autocommit é desfeito e devolve erro; com
   transação aberta, a colisão fica em `dolt_conflicts_<t>` (base, ours, theirs) e o commit é recusado.
   Há ainda `DOLT_PREVIEW_MERGE_CONFLICTS()` (ensaio de merge sem gravar) e `DOLT_BRANCH_STATUS()` (quantos
   commits à frente/atrás), que dão a checagem de início de sessão quase pronta.
6. **O que falta construir** (seção 9): o sincronizador por máquina (envoltório de pull/push com estado e
   notificação), a **vista `.md` de mão dupla** (a maior peça; três opções, de 3 a 10 dias), a conferência
   de versão na gravação (padrão SQL simples), a nota de colisão legível para o humano e a ligação com a
   busca. Total grosseiro: **9 a 20 dias**, conforme a opção de vista.
7. **A busca encaixa de dois jeitos, combináveis:** (a) a vista `.md` materializada no disco é um vault
   comum, então as candidatas já levantadas (memtomem, markdown-vault-mcp, zvec-grep, ck) indexam a vista
   sem mudança; (b) dentro do Dolt há índice FULLTEXT (básico) e índice VECTOR com `VEC_DISTANCE`, com
   os embeddings gerados fora.
8. **Peças alternativas achadas:** **DoltLite** (fork do SQLite com versionamento do Dolt, em beta, com
   binário Windows e servidor de remote próprio), útil se o hub quiser ficar no dialeto SQLite;
   **obsidian-auto-note-importer** (plugin com núcleo de sync de mão dupla e conflito por campo, base para
   um provedor Dolt); **Dolt Workbench** (GUI na Microsoft Store, com diff, log e pull requests); o modo
   servidor do **beads** (`BEADS_DOLT_SERVER_HOST`), que aponta para o mesmo `dolt sql-server`.

## 1. Diagrama da montagem

```text
                     PONTO DE ENCONTRO (escolher 1; seção 4)
         ┌──────────────────────────────────────────────────────────────┐
         │ A. sql-server da máquina pessoal com remotesapi (pela tailnet)│
         │ B. GitHub privado, remote git em refs/dolt/data               │
         │ C. DoltHub privado / DoltLab / Hosted Dolt                    │
         │ D. S3/R2/MinIO, SSH ou pasta de rede                          │
         └──────────────▲──────────────────────────────▲────────────────┘
          dolt_push/pull│ (sincronizador, 15 min)      │dolt_push/pull
                        │                              │
  MÁQUINA PESSOAL (Windows) ───────────────   NOTEBOOK (Windows) ─────────────────
  ┌───────────────────────────────────────┐   ┌───────────────────────────────────┐
  │ dolt sql-server  :3306 (SQL)          │   │ dolt sql-server :3306 (clone)     │
  │   ├─ mcp_server  :7007/mcp  ◄── agentes  │   ├─ mcp_server :7007/mcp ◄── agentes
  │   └─ remotesapi  :50051 (se opção A)  │   │                                   │
  │ banco do hub (tabelas de notas)       │   │ banco do hub (mesmo histórico)    │
  │   ▲            ▲                      │   │   ▲            ▲                  │
  │   │ SQL        │ SQL condicional      │   │   │            │                  │
  │ [MCP do hub]  [ponte da vista .md] ◄─┐│   │ [MCP do hub]  [ponte da vista]◄─┐ │
  │  busca,ler,   gera .md / devolve     ││   │                                 │ │
  │  gravar com    edição com versão     ││   │                                 │ │
  │  versão, sync  ─────────► vault/*.md ┘│   │                vault/*.md ──────┘ │
  │                          ▲ Obsidian   │   │                ▲ Obsidian         │
  │ [busca: indexa vault/*.md ou usa      │   │ [busca]                           │
  │  FULLTEXT/VECTOR do Dolt]             │   │                                   │
  │ [sincronizador + estado + aviso]      │   │ [sincronizador + estado + aviso]  │
  └───────────────────────────────────────┘   └───────────────────────────────────┘
  Legenda: [ ] = a construir ou configurar; o resto vem pronto.
```

## 2. Peças, com status e evidência

Status: **pronta** (usa-se como vem), **configurar** (pronta, mas exige ajuste), **construir** (escrever código).

| # | Peça | Status | O que já existe e como encaixa | Evidência |
|---|---|---|---|---|
| P1 | Motor do banco: Dolt no Windows | pronta | `winget install dolt`, `choco`, `scoop`, `.msi`, `.zip`. v2.4.1 de 2026-10-02 com `dolt-windows-amd64.msi` (pesquisa 24). | [installation/windows.md](https://dolthub.com/docs/introduction/installation/windows.md) |
| P2 | Servidor `dolt sql-server` | configurar | "allows multiple local or remote clients to connect to the same database"; porta 3306; `config.yaml` com listener, usuários, TLS. Rodar como serviço no Windows: a doc de "Application Server" é só Linux (systemd); no Windows fica por Agendador de Tarefas ou envoltório de serviço (**NV**). | [rdbms/server.md](https://dolthub.com/docs/concepts/dolt/rdbms/server.md), [server/configuration.md](https://dolthub.com/docs/sql-reference/server/configuration.md), [application-server.md](https://dolthub.com/docs/introduction/installation/application-server.md) |
| P3 | MCP para os agentes | configurar | Bloco `mcp_server` (porta 7007, usuário, senha, banco) no `config.yaml`: "your AI agents can call tools against your Dolt database". Binário avulso dolthub/dolt-mcp v0.3.8 (2026-08-18) com zip Windows, stdio ou HTTP, 40+ ferramentas. Apache-2.0, 19 estrelas. | [configuration.md §mcp_server](https://dolthub.com/docs/sql-reference/server/configuration.md), [dolt-mcp README](https://raw.githubusercontent.com/dolthub/dolt-mcp/main/README.md), API de releases |
| P4 | MCP "do hub" (ferramentas de alto nível) | construir | O dolt-mcp expõe SQL cru (`query`, `exec`). Para as garantias do hub (gravar com versão, estado do sync, busca), vale um MCP fino por cima, ou skills que ensinem o padrão SQL ao agente. | inferência a partir da lista de ferramentas do dolt-mcp |
| P5 | Concorrência na mesma máquina | pronta + construir | Transações: "If two writers attempt to write the same data, one writer is allowed to commit their transaction and the other is rolled back"; isolamento Read Committed. Isso cobre gravações simultâneas. A "conferência de versão ao gravar" (ler, pensar, gravar depois) precisa de uma coluna de versão e `UPDATE ... WHERE versao = ?` (construir, pequeno). | [sql/transaction.md](https://dolthub.com/docs/concepts/dolt/sql/transaction.md) |
| P6 | Commits automáticos | configurar | `@@dolt_transaction_commit = 1` "creates a Dolt commit for every SQL transaction commit", com mensagem configurável. Mantém o working set limpo, o que destrava o push para o servidor (P8). | [dolt-sysvars.md](https://dolthub.com/docs/sql-reference/version-control/dolt-sysvars.md) |
| P7 | Sync entre máquinas (pull/push) | pronta | Clone, fetch, push, pull; também por SQL (`CALL dolt_pull`, `dolt_push`). Push exige fast-forward; pull faz merge de três vias. | [git/remotes.md](https://dolthub.com/docs/concepts/dolt/git/remotes.md), [version-control/remotes.md](https://dolthub.com/docs/sql-reference/version-control/remotes.md) |
| P8 | Servidor como remote (remotesapi) | configurar | "A running Dolt SQL server can serve as a Dolt remote … you can clone, push, pull, and fetch from a running Dolt SQL Server". Push exige usuário com privilégio de super usuário e `DOLT_REMOTE_PASSWORD`; push para branch com mudanças não commitadas é a "additional complication" do servidor. | [configuration.md §remotesapi](https://dolthub.com/docs/sql-reference/server/configuration.md), [blog: SQL Server Push Support](https://www.dolthub.com/blog/2023-12-29-sql-server-push-support/) |
| P9 | Colisão visível | pronta | "conflicts are detected on a cell-level"; em autocommit "the transaction will be automatically rolled back"; `dolt_conflicts_<t>` com base/ours/theirs; `dolt_allow_commit_conflicts` padrão 0 (commit com colisão falha). JSON: chaves diferentes juntam, chaves iguais colidem. | [git/conflicts.md](https://dolthub.com/docs/concepts/dolt/git/conflicts.md), [merges.md](https://dolthub.com/docs/sql-reference/version-control/merges.md), [dolt-sysvars.md](https://dolthub.com/docs/sql-reference/version-control/dolt-sysvars.md) |
| P10 | Checagem de estado do sync | pronta (consultas) + construir (hook) | `DOLT_BRANCH_STATUS(base, alvo)` dá commits à frente/atrás; `DOLT_PREVIEW_MERGE_CONFLICTS_SUMMARY()` faz "dry run" do merge; `dolt_remote_branches`, `dolt_status`, `dolt_merge_status`. O hook de início de sessão que lê isso é a construir (o beads já faz o mesmo com `bd prime` em Claude, Codex e Copilot CLI). | [dolt-sql-functions.md](https://dolthub.com/docs/sql-reference/version-control/dolt-sql-functions.md), [dolt-system-tables.md](https://dolthub.com/docs/sql-reference/version-control/dolt-system-tables.md), [beads copilot-cli.md](https://raw.githubusercontent.com/gastownhall/beads/main/docs/integrations/copilot-cli.md) |
| P11 | Sincronizador por máquina | construir | Envoltório de `dolt_pull` + `dolt_push` a cada 15 min (Agendador do Windows), com estado local e notificação na falha. É o desenho do ticket 08 trocando git-sync por Dolt; a parte de "desfazer a junção" já vem do Dolt (P9). | ticket 08 (Answer, "Para a construção"); P7, P9 |
| P12 | Vista `.md` de mão dupla | construir | Não existe ponte pronta Dolt ↔ vault. Há três moldes prontos para copiar (seção 6.2): obsidian-beads (plugin chama CLI, recarrega e avisa), obsidian-auto-note-importer (núcleo de sync agnóstico de provedor, conflito por campo) e um daemon externo. | [obsidian-beads README](https://raw.githubusercontent.com/rome-1/obsidian-beads/main/README.md) (pesquisa 23), [auto-note-importer README](https://raw.githubusercontent.com/uppinote20/obsidian-auto-note-importer/main/README.md) |
| P13 | Busca | configurar ou construir | (a) indexar a vista `.md` com as candidatas da pesquisa 21; (b) `FULLTEXT` (🟠 "Only basic functionality") e `VECTOR INDEX` + `VEC_DISTANCE` no Dolt. | seção 7 |
| P14 | Ligar as máquinas | configurar | Tailscale só no Windows, grants mínimos (pesquisa 05). Para P2/P8 bastam as portas 3306, 7007 e a do remotesapi, dentro da tailnet. | pesquisa 05 |
| P15 | GUI para o humano ver histórico e diff | pronta | Dolt Workbench na Microsoft Store e nos releases: grafo de commits, diff, pull requests, "Agent Mode". Exibição de `dolt_conflicts`: **NV**. | [dolt-workbench README](https://raw.githubusercontent.com/dolthub/dolt-workbench/main/README.md), [products/workbench.md](https://dolthub.com/docs/products/workbench.md) |
| P16 | Tarefas (beads) no mesmo servidor | configurar | `bd init --server` "Connects to an external `dolt sql-server` for multiple concurrent writers"; `BEADS_DOLT_SERVER_HOST`/`PORT`; modo de servidor compartilhado. | [beads README](https://raw.githubusercontent.com/gastownhall/beads/main/README.md), [beads docs/architecture/dolt.md](https://raw.githubusercontent.com/gastownhall/beads/main/docs/architecture/dolt.md) |
| P17 | Backup | configurar | Página oficial de backups do servidor; `bd backup` no beads. Detalhe não lido (**NV**). | [server/backups.md](https://dolthub.com/docs/sql-reference/server/backups.md) (só no índice) |

## 3. Evidências principais, citadas

- **Offline first é caso de uso oficial.** "With Dolt you write to the database disconnected… When it is safe to
  connect to the internet, Dolt computes the difference between what you have and what a peer database has and
  only sends these differences both ways… Conflicting writes are surfaced quickly and an operator or software can
  take additional action to resolve." ([use-cases/offline-first.md](https://dolthub.com/docs/introduction/use-cases/offline-first.md))
- **Dois escritores com remote comum é suportado, com a ressalva certa.** "It is possible to connect several write
  targets with a common remote middleman, but they would need to reconcile merge conflicts in the same way an
  offline Dolt database does." ([server/replication.md §Multi-Primary](https://dolthub.com/docs/sql-reference/server/replication.md))
  É exatamente o desenho "parar e avisar" do ticket 08.
- **Replicação pronta, se quiser leitura sempre fresca.** "On the primary, you configure 'push on write' and on
  the replicas you configure 'pull on read'" (`dolt_replicate_to_remote`, `dolt_read_replica_remote`). Só
  replica commits; réplica não escreve. ([rdbms/replication.md](https://dolthub.com/docs/concepts/dolt/rdbms/replication.md))
  Serve como variante (seção 4, T3), não como o modo de duas máquinas que escrevem.
- **Tipos de remote.** "Dolt also supports filesystem, SSH, HTTPS, AWS, and GCS remotes"; Git (GitHub, GitLab;
  Bitbucket não), `s3://` com R2 e MinIO, `oci://`. SSH: "You cannot push to a data directory that is locked by a
  running sql-server"; de dentro do servidor, `dolt_push()`/`dolt_pull()` funcionam. DoltHub: "Private
  repositories are free up to a Gigabyte. After a Gigabyte, private repositories are $50 a month".
  ([version-control/remotes.md](https://dolthub.com/docs/sql-reference/version-control/remotes.md))
- **MCP embutido.** "Starts a Dolt MCP HTTP server that will be connected to the started Dolt SQL server…
  `claude mcp add -t http dolt-mcp http://localhost:7007/mcp`". ([configuration.md](https://dolthub.com/docs/sql-reference/server/configuration.md))
  Em qual versão do Dolt o bloco entrou e se o binário Windows do Dolt o inclui: **NV**.
- **Maturidade do remote git** (pesquisa 24): recurso de 2026, com correções recentes (#11741 push cancelado
  travando o servidor; #11916 pulls lentos). Vale para a opção B do ponto de encontro.

## 4. Onde o servidor mora (opções)

Os agentes falam sempre com um `dolt sql-server`. A pergunta é onde ele roda e qual é o ponto de encontro.

| Topologia | Como funciona | Pronto? | Riscos e mitigação | Esforço |
|---|---|---|---|---|
| **T1. Servidor local em cada máquina + remote central** (recomendada) | Cada máquina tem seu clone e seu `sql-server` em `localhost`; o sincronizador faz pull/push contra o ponto de encontro (A a D abaixo). | Sim (P1, P2, P7) | Colisão só aparece no sync, não na hora. Mitigação: sync a cada 15 min, checagem de sessão (P10). | 1 a 2 dias para configurar as duas máquinas |
| **T2. Servidor único na máquina pessoal, notebook conecta pela tailnet** | Um banco só; não há merge entre máquinas enquanto há rede; o notebook usa `mysql://pessoal:3306` e `http://pessoal:7007/mcp`. | Sim (P2, P3, P14) | Sem rede, o notebook não escreve. Mitigação: clone de reserva no notebook e troca para T1 quando offline (o sincronizador muda o alvo). Também exige a máquina pessoal ligada (modo unattended do Tailscale, pesquisa 05). | 1 dia; +1 a 2 dias para a troca automática |
| **T3. Primário + réplica de leitura** | Pessoal escreve com push on write; notebook lê com pull on read. | Sim | Notebook não escreve. Serve só se o notebook for leitor. | 0,5 dia |
| **T4. Hosted Dolt (gerenciado)** | Servidor na nuvem da DoltHub, com workbench, backups, remotesapi para clonar localmente. | Sim | Custo e dados de cliente fora de casa (preço **NV**). Mitigação: só para dados sem cliente, ou não usar. | 0,5 dia |

Ponto de encontro em T1:

| Opção | Pronto? | Prós | Riscos e mitigação |
|---|---|---|---|
| **A. remotesapi do `sql-server` da máquina pessoal**, pela tailnet | Sim (P8) | Sem terceiros; o mesmo processo é banco e remote. | Push exige super usuário e working set limpo. Mitigação: `dolt_transaction_commit=1` (P6), usuário só para sync, porta só na tailnet. Se a pessoal estiver desligada, o notebook acumula commits e sincroniza depois (é só "atraso", que a checagem mostra). |
| **B. GitHub privado** (remote git) | Sim | Já disponível, sempre online, credencial já decidida (deploy key/PAT, pesquisa 05). | Recurso novo, com correções em curso (pesquisa 24). Mitigação: fixar versão do Dolt nas duas máquinas; ter A ou C como reserva (um banco pode ter vários remotes). Crescimento do repositório: opções `git-remote.max-history-commits` (**NV** no detalhe). |
| **C. DoltHub privado / DoltLab** | Sim | Interface web com diff e pull requests; grátis até 1 GB. DoltLab roda em casa (download só `linux/amd64`, então WSL ou VM, **NV**). | Dados de cliente num terceiro (DoltHub). Mitigação: DoltLab, ou A/B. |
| **D. S3/R2/MinIO, SSH ou pasta** | Sim | `s3://` com escrita condicional, sem DynamoDB. | SSH não pode receber push num diretório travado pelo servidor. Mitigação: pasta de remote separada do banco vivo. |

## 5. Como funciona o modo offline

1. Em T1, o agente nunca sabe se há rede: sempre grava no `sql-server` local (via MCP). Cada transação vira
   commit (P6).
2. O sincronizador (P11) tenta `CALL dolt_pull('origin','main')` e depois `CALL dolt_push('origin','main')`.
   Sem rede, falha; grava "última sync ok" no estado local e, depois de 30 min (dois ciclos), dispara o aviso
   do ticket 08.
3. Ao voltar a rede: pull faz fast-forward ou merge de três vias por célula. Sem colisão, segue e faz push.
   Com colisão, em autocommit o pull é desfeito ("automatically rolled back"), o banco fica com a versão local
   limpa e o sincronizador para de empurrar, como decidido no ticket 08, item 3.
4. Em T2, o notebook offline troca para o clone local (inferência: é o mesmo mecanismo de T1, com um passo
   de troca de alvo a construir).

## 6. Vista `.md` de mão dupla

### 6.1 O que o desenho precisa

- Banco gera um `.md` por registro (frontmatter com `id`, `versao` e campos; corpo = texto).
- Edição do Gustavo no Obsidian volta ao banco com conferência: só grava se `versao` no banco ainda é a do
  arquivo. Se não for, não sobrescreve: gera aviso/nota de colisão.
- Mudança vinda do banco (agente ou sync) regrava o arquivo, salvo se ele tiver edição não devolvida.

### 6.2 Opções para montar

| Opção | Molde pronto | Como encaixa | Riscos e mitigação | Esforço |
|---|---|---|---|---|
| **V1. Daemon externo** (script Python/Node/Go no Agendador ou em segundo plano) | Padrão "exporta, observa, devolve" (sqlite-memory, pesquisa 23), sem a falha da volta sem conferência. | Exporta com `SELECT`; observa o vault (watcher de arquivos); devolve com `UPDATE ... WHERE id=? AND versao=?`; se 0 linhas, escreve nota de colisão. Pode usar `dolt_diff_<t>` para regenerar só o que mudou. | A vista vira um arquivo comum, então busca e grafo do Obsidian funcionam. Corrida com o Obsidian salvando: mitigar com debounce e hash do conteúdo no frontmatter. | 3 a 6 dias |
| **V2. Plugin do Obsidian no molde do obsidian-beads** | obsidian-beads: painel e editor; "Save … writes only the changed fields via `bd update`"; "An open bead editor reloads when its bead changes. If you have unsaved edits it keeps them and says the bead changed". | Plugin fala com o `sql-server` (driver MySQL em Node, desktop) ou chama o `dolt` CLI. Aviso de colisão aparece dentro do editor. | O obsidian-beads usa `ItemView`, sem `.md` no disco; para a busca e o grafo verem, o plugin deve materializar arquivos (vira V1 dentro do plugin). Windows do obsidian-beads: **NV**. | 5 a 10 dias |
| **V3. Provedor Dolt no obsidian-auto-note-importer** | "Built on a provider-agnostic core — every provider gets the same multi-config, conflict-resolution, and safety machinery"; conflito `Manual` (avisa e pula) / `Obsidian wins` / `Remote wins`; "Watch for changes". MIT, 18 estrelas (pesquisa 23). | Fork com um provedor MySQL/Dolt. | Hoje empurra só **frontmatter**; o corpo é só leitura ("The body is pull-only"). Mitigação: estender o push ao corpo. Alternativa sem fork: DoltgreSQL + PostgREST no lugar do Supabase (**NV**, inferência). | 3 a 5 dias |

Recomendação de montagem (a decisão é do Gustavo): **V1**, porque mantém o `.md` como arquivo comum (o que a
busca da seção 7 aproveita) e é independente do Obsidian. V2 pode vir depois, como camada de conforto.

### 6.3 Granularidade da colisão e como reduzi-la

Merge por célula: a nota inteira numa coluna TEXT colide mesmo com edições em parágrafos diferentes
(pesquisa 24, inferência). Opções:

- **Uma linha por bloco** (seção ou parágrafo, chave `nota_id + bloco_id`): edições em blocos diferentes
  juntam sozinhas. A ponte remonta o `.md`. Esforço: +1 a 2 dias na ponte.
- **Corpo em JSON por seção**: "changes that modify different keys in a JSON object are merged without
  generating conflicts" ([git/conflicts.md](https://dolthub.com/docs/concepts/dolt/git/conflicts.md)).
  Mais simples que a anterior; +0,5 a 1 dia.
- **Aceitar a colisão por nota inteira** no início: com sync a cada 15 min e duas máquinas de uma pessoa, é
  rara (inferência).

## 7. Como a busca do agente entra

| Caminho | O que existe | Encaixe | Limites e mitigação | Esforço |
|---|---|---|---|---|
| **B1. Indexar a vista `.md`** | Candidatas da pesquisa 21: memtomem, markdown-vault-mcp, zvec-grep, ck. Todas leem `.md` do disco. | A vista materializada (V1) é o corpus. O agente busca pelo MCP da ferramenta de busca e grava pelo MCP do Dolt. | O índice fica alguns segundos atrás do banco (o tempo de a ponte regravar o arquivo). Mitigação: a ponte dispara reindexação após gerar. | 0,5 a 1 dia (além do spike do ticket 09) |
| **B2. Busca dentro do Dolt** | FULLTEXT com `MATCH … AGAINST` ([blog](https://www.dolthub.com/blog/2023-07-26-announcing-fulltext-indexes/)); `VECTOR INDEX` e `VEC_DISTANCE`, tipo `VECTOR` dedicado ([blog 2025-01-16](https://www.dolthub.com/blog/2025-01-16-announcing-vector-indexes/), [blog 2025-09-03](https://www.dolthub.com/blog/2025-09-03-improving-vector-performance/)). Os índices são versionados e viajam com o banco (inferência a partir de "Version-Controlled Vector Indexes"). | Uma ferramenta "buscar" no MCP do hub: embedding da consulta (FreeLLMAPI ou modelo local) + `ORDER BY VEC_DISTANCE(...) LIMIT k`, somado a FULLTEXT. | FULLTEXT é básico: faltam "different text parsers, stopword support, … phrase matching", sem stemmer pt-BR; e a tabela de funções lista `MATCH` como ❌ (contradição entre páginas, **NV** qual vale hoje). Distância só euclidiana no anúncio de 2025 (atualização **NV**). Mitigação: usar B2 para o vetor e B1 ou `LIKE` para palavra. | 2 a 4 dias |
| **B3. Híbrido** | B1 + B2 | A ferramenta "buscar" do MCP do hub chama as duas e funde. | Mais peças. | +1 dia sobre B1+B2 |

## 8. Como a colisão aparece para o humano

1. **No sync:** o sincronizador vê o erro do pull, mantém a versão local (o Dolt já desfez a junção),
   grava `colisao=true` no estado local e dispara a notificação do Windows (ticket 08, item 2; notificação
   a partir de tarefa agendada continua **NV**).
2. **No início da sessão de agente:** o hook lê o estado e roda `DOLT_BRANCH_STATUS('main','origin/main')` e
   `DOLT_PREVIEW_MERGE_CONFLICTS_SUMMARY(...)`, mostrando quantas notas colidem e quais. O agente resolve com
   o Gustavo: abre transação, `CALL dolt_pull`, lê `dolt_conflicts_<t>` (base, ours, theirs), decide, apaga as
   linhas resolvidas ou usa `dolt_conflicts_resolve('--ours'|'--theirs', t)`, commita.
3. **No Obsidian (a construir na ponte):** para cada nota em colisão, a ponte escreve uma nota irmã
   `<nota>.colisao.md` com três seções (base, esta máquina, outra máquina) e um aviso no topo da nota
   original. Isso não é uma "cópia de conflito" que vira verdade: é só a vista do que está em
   `dolt_conflicts_<t>`, e some quando o banco resolve. Esforço: 1 a 2 dias.
4. **Edição do Gustavo que perde a corrida** (o banco mudou enquanto ele editava): a ponte recusa a volta
   (versão diferente) e mostra o mesmo tipo de nota/aviso, no molde do obsidian-beads ("keeps them and says
   the bead changed; Revert loads the new version").
5. **Visual extra pronto:** Dolt Workbench para histórico e diff (P15).

## 9. O que falta construir, com esforço

| # | Item | Opções | Esforço grosseiro |
|---|---|---|---|
| C1 | Schema do hub (notas, blocos ou JSON por seção, coluna `versao`, metadados) | tabela simples / por bloco / JSON | 0,5 a 1 dia |
| C2 | Configuração das duas máquinas: Dolt, `config.yaml` (MCP, remotesapi, `dolt_transaction_commit`), início automático no Windows, usuários SQL, portas só na tailnet | Agendador de Tarefas ou envoltório de serviço (**NV**) | 1 a 2 dias |
| C3 | Sincronizador por máquina: pull/push, estado local, aviso de 30 min, notificação | script PowerShell ou Python | 1 a 2 dias |
| C4 | Checagem de início de sessão em Claude Code, Codex e Copilot | molde `bd prime`/`bd setup` do beads | 0,5 a 1 dia |
| C5 | MCP do hub (buscar, ler, gravar com versão, estado do sync) por cima do Dolt | MCP próprio fino, ou só skills + dolt-mcp cru | 2 a 4 dias (ou 0,5 dia só com skills) |
| C6 | Ponte da vista `.md` | V1 / V2 / V3 (seção 6.2) | 3 a 10 dias |
| C7 | Nota de colisão legível no Obsidian | parte da ponte | 1 a 2 dias |
| C8 | Busca | B1 / B2 / B3 (seção 7) | 0,5 a 5 dias |
| C9 | Migração do conteúdo inicial para o banco | script de importação único | 0,5 a 1 dia |
| | **Total** | caminho mínimo (T1 + A ou B, V1, B1, skills) a completo (V2, B3, MCP próprio) | **≈ 9 a 20 dias** |

Riscos gerais e mitigação:

- **Recursos novos do Dolt** (remote git, MCP embutido): fixar a mesma versão nas duas máquinas e testar no
  spike; manter dois remotes.
- **Dialeto MySQL em vez de SQLite:** se pesar, **DoltLite** dá o mesmo modelo (branches, merge, conflitos,
  remotes por arquivo ou HTTP com `doltlite-remotesrv`) num arquivo SQLite. Contra: beta, "One durable writer at
  a time" (`SQLITE_BUSY` para o segundo), remote só por arquivo ou HTTP próprio (sem remote git), licença
  `NOASSERTION` na API do GitHub (**NV**), FTS5 **NV**. O dolt-mcp tem modo DoltLite com zip Windows.
  ([doltlite README](https://raw.githubusercontent.com/dolthub/doltlite/master/README.md),
  [remotes.md](https://raw.githubusercontent.com/dolthub/doltlite/master/doc/doltlite/remotes.md),
  [remotesrv.md](https://raw.githubusercontent.com/dolthub/doltlite/master/doc/doltlite/remotesrv.md))
- **Credenciais:** `DOLT_REMOTE_PASSWORD` em variável de ambiente (o blog admite que "isn't ideal").
  Mitigação: opção B (deploy key) ou C (credencial `dolt login`) no lugar de A.
- **Agente usando `exec` cru e pulando a conferência de versão:** mitigação com o MCP do hub (C5) e usuário SQL
  do MCP sem permissão de `UPDATE` direto na tabela de notas, só via procedure (inferência; permissões em
  [access-management.md](https://dolthub.com/docs/sql-reference/server/access-management.md), detalhe **NV**).

## 10. Consultas e fontes

### 10.1 Consultas feitas

| # | Consulta | Tipo | Resultado |
|---|---|---|---|
| Q1 | `https://www.dolthub.com/docs/llms.txt` | índice oficial da doc | mapa das páginas `.md`; base das demais |
| Q2 | 17 páginas `.md` de dolthub.com/docs (offline-first, transaction, server, replication ×2, remotes ×2, merges, conflicts, windows, application-server, configuration, doltlab, workbench, branch-permissions, remote-authentication, access-management) | doc oficial | seções 2 a 8 |
| Q3 | `indexes.md`, `data-description.md`, `types.md`, `miscellaneous.md`, `expressions-functions-operators.md`, `dolt-sysvars.md`, `dolt-system-tables.md`, `dolt-sql-functions.md` | doc oficial | FULLTEXT, `MATCH`, variáveis, funções de status |
| Q4 | WebSearch "dolthub blog vector index Dolt VEC_DISTANCE" (só dolthub.com) | busca (listagem) | URLs dos posts; conteúdo lido depois em Q5 |
| Q5 | WebSearch "dolthub blog full-text search … MATCH AGAINST" (só dolthub.com) | busca (listagem) | URL do post de FULLTEXT |
| Q6 | Posts do blog baixados: 2025-01-16 vector indexes, 2025-09-03 VECTOR columns, 2023-07-26 fulltext, 2023-12-29 sql-server push, 2026-06-04 agentic writes | blog oficial, HTML convertido localmente | citações das seções 2, 4 e 7 |
| Q7 | API GitHub `repos/dolthub/dolt-mcp`, `releases?per_page=1`; raw README | API + raw | 19 ★, Apache-2.0, v0.3.8 com zip Windows |
| Q8 | API GitHub `repos/dolthub/doltlite`; raw README, `doc/doltlite/{remotes,sqlite-compatibility,remotesrv,concurrency}.md` | API + raw | 286 ★, push 2026-10-04, beta |
| Q9 | raw README de dolthub/dolt-workbench | raw | GUI Windows, PRs, diff, Agent Mode |
| Q10 | raw README, `docs/architecture/dolt.md`, `docs/integrations/copilot-cli.md` de gastownhall/beads | raw | modo servidor, host externo, hooks |
| Q11 | raw `community-plugins.json` do Obsidian (8.405 plugins), filtro mysql/dolt/sql/sqlite/postgres/two-way/bidirectional | catálogo oficial | nenhum plugin Dolt/MySQL de mão dupla; moldes: auto-note-importer, postgres-sync, notion-database-sync |
| Q12 | raw README de uppinote20/obsidian-auto-note-importer | raw | núcleo agnóstico de provedor, push só de frontmatter |
| Q13 | API GitHub `repos/dolthub/docs` e árvore | API | 404; a cota anônima (60/h) esgotou depois de Q12; metadados que faltaram ficaram **NV** |
| Q14 | Leitura local: pesquisas 05, 13, 18, 21, 23, 24; tickets 08, 09, 25 | material do repositório | reaproveitado sem refazer |

### 10.2 Não verificado (lista consolidada)

- Rodar `dolt sql-server` como serviço no Windows (a doc só cobre systemd).
- Versão do Dolt em que o bloco `mcp_server` entrou e se o binário Windows do Dolt o traz; autenticação do
  endpoint HTTP do MCP (o README mostra `Authorization: Bearer`, mas não vi a configuração do token).
- Se `MATCH … AGAINST` funciona hoje (o post e a página de DDL dizem que sim; a tabela de funções diz ❌).
- Funções de distância além da euclidiana no índice vetorial.
- Exibição de `dolt_conflicts` no Dolt Workbench.
- obsidian-beads no Windows; DoltLab fora de Linux; preço do Hosted Dolt; DoltgreSQL + PostgREST.
- Licença do DoltLite (API retorna `NOASSERTION`); FTS5 no DoltLite.
- Notificação do Windows a partir de tarefa agendada (herdado do ticket 08).
