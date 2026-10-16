---
title: Pesquisa 24, sync de banco entre duas máquinas pares
data: 2026-10-04
origem: subagente de pesquisa (Claude Code), ticket 24 "Sync de banco entre duas máquinas pares"
aviso: saída de modelo. Fontes primárias: README, LICENSE e docs brutos (raw.githubusercontent.com), páginas e arquivos `.md` das documentações oficiais (sqlite.org, docs.dolthub.com / dolthub.com/docs, vlcn.io/docs, docs.turso.tech, automerge.org/llms-full.txt), arquivos de CI e código pontuais, API REST do GitHub (metadados, releases, workflows), feeds Atom de commits e releases do GitHub e a API Algolia do Hacker News. Nada foi clonado, instalado ou executado. O que não foi conferido na fonte está marcado como **não verificado** (NV).
---

# Sync de banco entre duas máquinas pares: levantamento de 04/10/2026

## Resumo (uma tela)

1. **Cobertura:** 38 consultas (22 web em 6 línguas, 5 no HN, 6 na busca do GitHub, 3 na API do Reddit, 2 listas
   awesome). O Reddit ficou **sem cobertura**: o domínio é bloqueado tanto para a busca web quanto para a API JSON
   (seção 1.4). Quinze mecanismos conferidos na fonte, em quatro famílias.
2. **As quatro famílias, pelo que fazem quando as duas máquinas mudam o mesmo registro:**
   - **CRDT / multi-master** (cr-sqlite, sqlite-sync, Syzy, Marmot, Corrosion, Automerge, Turso Sync): **vence um, em
     silêncio.** Todas convergem sozinhas; nenhuma para. Só Syzy (tabela `syzy_conflicts`) e Automerge
     (`getConflicts`) guardam o perdedor para quem quiser olhar.
   - **Banco versionado com merge de três vias** (Dolt): **para e avisa.** Colisão por célula vira linha em
     `dolt_conflicts_<tabela>`; em modo autocommit a junção é desfeita sozinha.
   - **Changesets da extensão de sessão do SQLite** (nativa, domínio público): **quem decide é você.** O handler de
     conflito recebe cada colisão e pode abortar tudo. É peça de montar, não produto.
   - **Serializar o banco em texto para o git juntar** (sqlite-diffable, sql-md-sync, git-sqlite, sqlite2dir):
     **para e avisa**, porque a colisão vira conflito do git, igual ao mecanismo decidido no ticket 08.
3. **Achado principal:** o **Dolt** aceita, desde 2026, um **repositório Git comum como remote**, inclusive
   `git@github.com:ORG/REPO.git`. Os dados ficam numa ref à parte (`refs/dolt/data`). Ou seja, o GitHub privado com
   deploy key **serve de ponto de encontro também para o banco**. O beads (27,6 mil estrelas) já migrou para esse
   desenho: Dolt embutido, sync por `bd dolt push/pull` contra `refs/dolt/data` no remote git, com suporte a Windows.
   Contras: o recurso é novo e ainda recebe correções sérias (push cancelado que trava o servidor; pull que baixa o
   banco inteiro de novo); o modo embutido é de um escritor só; o merge é por célula, então duas edições em
   parágrafos diferentes do mesmo texto **colidem** (o git juntaria).
4. **Eliminados pela regra "nada diverge em silêncio" ou pelo ponto de encontro:** sqlite-sync (licença proíbe
   transporte que não seja o da SQLite Cloud), Turso Sync ("last push wins", exige servidor de sync), Syzy e Marmot
   (sem Windows), Corrosion (cluster com gossip), Litestream (backup de um escritor, não multi-master).
5. **Recomendação (a decisão é do Gustavo):** levar ao spike **duas** opções. (a) **Dolt com o GitHub como remote
   git**, que é o único produto pronto que para e avisa e usa o ponto de encontro já decidido. (b) **Texto por linha
   no git** (um arquivo por registro, no estilo do sql-md-sync), que mantém intacto o mecanismo do ticket 08, mas
   devolve ao texto o papel de verdade no transporte. CRDTs não entram: todos resolvem em silêncio.

## 1. Consultas feitas (registro para auditoria)

### 1.1 Busca web (WebSearch; listagens de resultado, não fonte primária)

| # | Consulta | Língua | Alvo |
|---|---|---|---|
| W1 | SQLite multi-master replication offline peer-to-peer conflict resolution open source | en | geral |
| W2 | CRDT SQLite extension merge two databases github | en | GitHub |
| W3 | local-first sync engine embedded database offline two devices conflicts 2026 | en | geral |
| W4 | version controlled SQL database git-like branch merge conflicts embedded | en | geral |
| W5 | serialize sqlite database to text for git diff merge dump per row | en | geral |
| W6 | sqlite session extension changeset conflict handler sync two databases | en | docs oficiais |
| W7 | Show HN SQLite sync peer to peer no server | en | HN |
| W8 | reddit sync sqlite between two computers offline both write merge | en | Reddit (não trouxe Reddit) |
| W9 | awesome local-first list sync CRDT databases github | en | listas awesome |
| W10 | sincronizar banco SQLite entre dois computadores offline replicação bidirecional conflito | pt | geral |
| W11 | SQLite 双向同步 多主复制 离线 冲突 CRDT 开源 | zh | geral |
| W12 | SQLite Synchronisation zwei Rechner offline Konflikte Replikation Open Source | de | geral |
| W13 | Dolt Windows embedded mode push pull GitHub remote file remote conflicts dolt_conflicts | en | docs oficiais |
| W14 | news.ycombinator.com cr-sqlite abandoned maintenance status | en | HN (sem resultado útil) |
| W15 | event sourcing append-only log files git sync rebuild sqlite projection personal knowledge base two machines | en | geral |
| W16 | Automerge Rust Windows offline file storage sync without server automerge-repo conflicts getConflicts | en | geral |
| W17 | beads issue tracker JSONL git merge sqlite cache steveyegge | en | GitHub |
| W18 | SQLite 同期 二台 オフライン マルチマスター 競合 解決 ライブラリ | ja | geral |
| W19 | site:reddit.com sqlite sync two laptops both offline merge changes cr-sqlite OR dolt OR "session extension" | en | Reddit (não trouxe Reddit) |
| W20 | sincronizar base de datos SQLite entre dos equipos sin servidor fusionar cambios conflictos | es | geral |
| W21 | reddit r/sqlite how to merge two sqlite databases edited offline on different machines (domínio reddit.com) | en | Reddit (**bloqueado**, erro 400) |
| W22 | reddit local-first sync engine without server peer to peer sqlite recommendations (domínio reddit.com) | en | Reddit (**bloqueado**, erro 400) |

### 1.2 Hacker News (API Algolia, `hn.algolia.com/api/v1/search`, só histórias)

| # | Consulta | Acertos | Destaques |
|---|---|---|---|
| H1 | sqlite sync multi-master | 0 | nenhum |
| H2 | cr-sqlite | 6 | "Crsql – Multi-writer and CRDT support for SQLite" (2022-11-15, 198 pontos) |
| H3 | sqlite crdt | 82 | "CRDT and SQLite: Local-First Value Synchronization" (2025-10-09, 78 pontos); "A fix for a divergence issue in a popular SQLite CRDT extension" (sqlite-sync, 2025-08-22) |
| H4 | dolt version controlled database | 14 | várias submissões do Dolt, 2020 a 2026 |
| H5 | sqlite git merge | 13 | "Show HN: Git-sqlite, a custom diff and merge driver for sqlite" (2018); "Show HN: SQLiteChangesetSync – Git-Like Sync for SQLite Databases" (2023); "SQLite Git Like Merge – The Session Extension" (2016) |

### 1.3 Busca de repositórios do GitHub (`api.github.com/search/repositories`, ordem por estrelas)

| # | Consulta | Total | Relevantes |
|---|---|---|---|
| G1 | sqlite crdt | 88 | vlcn-io/cr-sqlite, sqliteai/sqlite-sync, aspen-cloud/triplit, pubkey/rxdb |
| G2 | sqlite replication multi-master | 1 | insanai/sqlodin (0 estrelas, descartado) |
| G3 | sqlite sync offline | 427 | sqliteai/sqlite-sync, powersync-ja/powersync-js, AMPLIFIER/ampli-sync, syncular/syncular |
| G4 | local-first sync database | 81 | garden-co/jazz, dialog-db, fireproof (todos de navegador ou JS) |
| G5 | sqlite git diff | 27 | cannadayr/git-sqlite, jindraregal/sql-md-sync, clzls/sqldiffer |
| G6 | awesome local-first | 64 | alexanderop/awesome-local-first, schickling/awesome-local-first |

### 1.4 Reddit (API JSON `www.reddit.com/search.json`)

| # | Consulta | Resultado |
|---|---|---|
| R1 | sync sqlite between two computers | resposta não-JSON (bloqueio) |
| R2 | cr-sqlite | resposta não-JSON (bloqueio) |
| R3 | dolt git for data merge conflicts | resposta não-JSON (bloqueio) |

**Lacuna declarada:** nenhuma discussão do Reddit foi lida. Somadas W8, W19, W21 e W22, o Reddit ficou sem cobertura.

### 1.5 Listas awesome (README bruto)

| # | Lista | O que trouxe |
|---|---|---|
| A1 | alexanderop/awesome-local-first | cr-sqlite, libSQL, Turso Sync, Evolu, Electric, PowerSync, Automerge, Earthstar, Couchbase Lite, ObjectBox |
| A2 | schickling/awesome-local-first | nada novo para SQLite/git (último push em 2024-06-10) |

## 2. Tabela comparativa

Legenda: **Mesmo registro** = o que acontece quando as duas máquinas mudam o mesmo registro entre dois syncs.
**Visível?** = se a colisão aparece ou é resolvida em silêncio. **GitHub?** = se o GitHub privado com deploy key
serve de ponto de encontro. Estrelas e último commit conferidos na API do GitHub e nos feeds Atom em 04/10/2026.

| Mecanismo | Mesmo registro | Visível? | Servidor / pago | Windows nativo | Offline | GitHub? | Licença | Maturidade, último commit |
|---|---|---|---|---|---|---|---|---|
| **Dolt** (dolthub/dolt) | para: conflito por célula em `dolt_conflicts_<t>` | **sim**; em autocommit a junção é desfeita | não (remote git, arquivo, SSH, DoltHub opcional) | sim (`.msi`, `.zip`, winget, choco) | sim | **sim**, remote git em `refs/dolt/data` | Apache-2.0 | 24,6 mil ★, v2.4.1, commit 2026-10-03; remote git recente e em correção |
| **Extensão de sessão do SQLite** (sqlite.org) | chama o handler; você escolhe OMIT, REPLACE ou ABORT | **sim, se você programar** | não | NV se o `sqlite3.dll`/`.exe` oficial vem com ela compilada | sim | sim, como transporte de arquivos de changeset (montagem própria) | domínio público | parte do SQLite; madura |
| **Texto por linha + git** (sqlite-diffable, sql-md-sync) | conflito do git | **sim** (mecanismo do ticket 08) | não | sql-md-sync: CI em `windows-latest`; sqlite-diffable: NV | sim | **sim**, nativamente | Apache-2.0 / MIT | sqlite-diffable 140 ★, commit 2025-05-05; sql-md-sync 4 ★, commit 2026-05-11 |
| git-sqlite (driver de merge) | conflito, resolvido à mão com `git apply-sql` | sim | não | NV (scripts bash + autotools) | sim | sim | MIT | 223 ★, parado desde 2021-08-02 |
| sqlite2dir | só exporta; a junção fica com o git | sim (git) | não | NV (Rust, compila) | sim | sim | GPL-3.0 | 9 ★, "nem o autor usou"; commit 2024-02-29 |
| **cr-sqlite** (vlcn-io) | vence a última escrita; empate: **maior valor** | **não** (silencioso) | não | sim (`crsqlite-win-x86_64.zip`) | sim | só como transporte de changesets (montagem própria) | MIT | 3,8 mil ★; último release v0.16.3 (2024-01); commits só de build em 2026-08 |
| sqlite-sync (sqliteai) | CRDT, "no manual conflict resolution, ever" | **não** | **sim**: SQLite Cloud, ou Postgres/Supabase com o serviço deles | sim (lista Windows) | sim | **não**: a licença proíbe outro transporte | Elastic 2.0 modificada | 574 ★, commit 2026-10-01 |
| Turso Sync | "last push wins"; pull faz rollback e replay | **não** | **sim**: Turso Cloud ou `tursodb --sync-server` | sim (Turso lista Windows) | sim | não | MIT | 24,6 mil ★, commit 2026-10-02 |
| Syzy (wjordan) | última escrita por linha; o perdedor vai para `syzy_conflicts` (documentado no Postgres) | parcial (registra, não para) | não; malha TCP ou object storage | **não** (Linux e macOS) | sim | não | Apache-2.0 | 65 ★, pré-1.0, criado em 2026-07 |
| Marmot | última escrita por linha (HLC) | não | malha gossip entre nós | **não** (sem binário Windows no v2.8.0) | sim | não | MIT | 2,8 mil ★, commit 2026-09-30 |
| Corrosion (superfly) | cr-sqlite por baixo | não | cluster com agente e gossip | NV | sim | não | Apache-2.0 | 1,9 mil ★, commit 2026-09-21 |
| Automerge | escolha "arbitrária, mas determinística"; perdedores em `getConflicts` | parcial (registra, não para) | não | sim (Rust/JS) | sim | só com driver de merge próprio (NV) | MIT | 6,6 mil ★, commit 2026-10-01; é CRDT de documento, não banco |
| SQLiteChangesetSync | changesets de sessão, "git-like" | promete; resolução própria é "future development" | CloudKit no exemplo | **não** (Swift/iOS) | sim | possível, não pronto | MIT | 58 ★, parado desde 2023-12 |
| sqlsync (orbitinghail) | rebase no servidor | NV | servidor de coordenação | NV | sim | não | Apache-2.0 | 2,9 mil ★, commit 2025-11-19 |
| Litestream | não se aplica: um escritor, replica para arquivo ou S3 | — | não | NV | — | não | Apache-2.0 | 14,4 mil ★; é recuperação de desastre, não multi-master |

Fora da tabela (achados de busca não conferidos a fundo, todos dependentes de servidor ou de navegador): PowerSync,
Electric, Evolu (relay), Triplit, Jazz, RxDB, AMPLI-SYNC, SymmetricDS, Synql (protótipo acadêmico, parado em 2023),
Teilen-SQL (artigo ECOOP 2025).

## 3. Melhores achados, com evidência

### 3.1 Dolt: banco versionado que para e avisa, e usa o GitHub como remote

- **Colisão por célula, visível.** "On data, conflicts are detected on a cell-level. If two operations modify the same
  row, column pair to be different values, a conflict is detected." Exceção: colunas JSON, em que chaves diferentes
  juntam e chaves iguais colidem. (docs.dolthub.com/concepts/dolt/git/conflicts)
- **Junção desfeita em autocommit.** "If merge produces an error in `AUTOCOMMIT` mode, the transaction will be
  automatically rolled back and any merged tables will be reset." Com transação aberta, os conflitos ficam em
  `dolt_conflicts_<tabela>` (colunas base, ours e theirs) e o commit é recusado até que sejam resolvidos.
  (dolthub.com/docs/sql-reference/version-control/merges.md)
- **Repositório Git como remote.** "Dolt can also use a **Git repository** as a remote (for example, GitHub, GitLab,
  or any SSH/HTTPS Git server). Dolt stores its remote data inside the Git repo under a Git ref. By default Dolt uses
  `refs/dolt/data`." Exemplo dado: `dolt remote add origin git@github.com:ORG/REPO.git`. Exige `git` no `PATH` e um
  repositório com pelo menos uma branch. Bitbucket não é suportado. (dolthub.com/docs/sql-reference/version-control/remotes.md)
- **Windows.** README: instalador `.msi` nos releases e Chocolatey; a doc lista winget, choco, scoop, `.msi` e
  `.zip`. O release v2.4.1 (2026-10-02) traz `dolt-windows-amd64.msi/.zip/.7z`. O CI `ci-bats-windows.yaml` roda em
  `windows-latest`, mas é disparado por `workflow_dispatch`/evento, não a cada PR.
- **Maturidade do remote git.** As notas dos releases 2.3.2 a 2.4.1 (set.–out. 2026) corrigem problemas do recurso:
  "a cancelled push/fetch wedges sql-server indefinitely" (#11741); "since v2.1.2 a pull can re-download the whole
  database, because each process deletes its fetch ref" (#11949); "pulls from git remotes are O(reads × part size)
  (40 min → 2 min with an OID cache)" (#11916). É um recurso em uso, mas novo.
- **Precedente: beads.** "Distributed graph issue tracker for AI agents, powered by Dolt"; "**Platforms:** macOS,
  Linux, Windows, FreeBSD". "Embedded (default) — Dolt runs in-process … single writer." "Cross-machine sync uses
  `bd dolt push` / `bd dolt pull` against `refs/dolt/data` on your git remote; `.beads/issues.jsonl` is an export
  … not the source of truth." O beads abandonou o desenho antigo (JSONL no git como verdade, SQLite como cache)
  pelo Dolt. (README e docs/core-concepts/sync-concepts.md de gastownhall/beads, 27,6 mil ★, commit 2026-10-04)
- **Limites para o hub:**
  - Um escritor no modo embutido ("single-writer (enforced via file lock)", doc do beads). Dois agentes na mesma
    máquina exigem `dolt sql-server` ou uma fila. Como o Dolt trata transações concorrentes no sql-server: NV.
  - Merge por célula: uma nota inteira numa coluna TEXT colide mesmo com edições em parágrafos diferentes, coisa
    que o git juntaria por linha. Isto é uma inferência a partir da regra por célula, não um teste.
  - É um banco MySQL, não SQLite: muda o motor e o dialeto SQL.
  - NV: se a deploy key por máquina funciona sem ajuste. O Dolt chama o `git` do sistema e tem `DOLT_SSH_COMMAND`,
    mas não conferi como ele herda a configuração SSH do git no Windows.
  - NV: crescimento do repositório no GitHub com o histórico do Dolt (há opções novas `git-remote.max-history-commits`
    e `reset-history-on-prune`, release 2.4.1).

### 3.2 Extensão de sessão do SQLite: a colisão chega a você, mas é peça de montar

- **O que faz.** "record changes to tables in an SQLite database, package those changes into a 'changeset' or
  'patchset' file, and later apply the same set of changes to another database with the same schema and compatible
  starting data." (sqlite.org/sessionintro.html)
- **Detecta a colisão de verdade.** No UPDATE: "The target database may contain a row with the specified PRIMARY KEY
  values, but the current values of the fields that will be modified by the change may not match the original
  values." O handler decide entre omitir, substituir ou "aborting the entire changeset application". Com patchset,
  esse caso não é detectado: precisa ser changeset.
- **Limites documentados:** só tabelas com PRIMARY KEY declarada; tabelas virtuais não são capturadas (logo, um
  índice FTS5 teria de ser reconstruído localmente); linhas com NULL na chave são ignoradas; precisa ser compilada
  com `-DSQLITE_ENABLE_SESSION -DSQLITE_ENABLE_PREUPDATE_HOOK`.
- **Para o hub:** daria para gravar cada changeset como arquivo novo no git (arquivos só acrescentados não colidem
  no git) e aplicar os da outra máquina com handler que aborta. Mas ordem, base comum e reprocessamento ficam por
  conta própria. Única implementação encontrada, SQLiteChangesetSync, é Swift/iOS, está parada desde 2023 e lista a
  resolução própria como "Future Development". NV: se o SQLite que o hub usaria no Windows (Python, Node ou o
  binário oficial) vem com a extensão compilada.

### 3.3 Texto por linha no git: o mecanismo do ticket 08, aplicado ao banco

- **sql-md-sync** (MIT, 4 ★, criado em 2026-05): "SQLite for your app, Markdown for your git history. One file per
  row". Exporta e importa (`export`, `import --md <dir> --out <db>`, "byte-stable round-trip") e tem um hook de
  pre-commit. Limites declarados: "No conflict resolution beyond Git — two branches touching the same row produce a
  merge conflict"; "Single-process: no row locking, no concurrent writers". CI com matriz
  `[ubuntu-latest, macos-latest, windows-latest]`. Projeto mínimo, mas é exatamente o desenho.
- **sqlite-diffable** (simonw, Apache-2.0, 140 ★): um `.ndjson` por tabela, uma linha por registro, mais
  metadados; `load` reconstrói o banco. O código lê `conn[table].rows` sem ORDER BY, então a ordem das linhas depende
  do rowid (lido em `cli.py`). Um arquivo por tabela faz duas inserções no fim do arquivo encostarem uma na outra. NV
  se o git trata isso como conflito; a regra exata do merge do git não foi conferida aqui.
- **git-sqlite** (MIT, 223 ★, parado desde 2021): driver de diff e merge baseado em `sqldiff`; o README recomenda
  UUIDs para "multi-master distribution". Exige bash e autotools.
- **Consequência para o hub:** neste desenho o banco volta a ser **derivado** do texto na hora do sync. A verdade
  trafega em texto, e a decisão "Markdown: vista ou fonte da verdade" volta à mesa por este caminho.

### 3.4 CRDTs: todos resolvem em silêncio

- **cr-sqlite:** "Multiple writes to the same register by different peers are resolved by taking the last write. If
  the two writes were concurrent, the largest value is taken. By default, all columns in a crr are treated as last
  write wins registers." (vlcn.io/docs/cr-sqlite/crdts/column-crdts). O README diz da abordagem atual: "Automatically
  handles merge conflicts. No options for manual merging." A abordagem com "fork the data on merge conflict" é
  "To be implemented in v2". Último release em 2024-01 (v0.16.3); os commits de 2026-08 são só de build (Windows
  arm64, Android, iOS, macOS).
- **sqlite-sync:** "No conflicts. Deterministic merge, no manual conflict resolution, ever." A licença (Elastic 2.0
  modificada) exige licença comercial para quem "implement or use an alternative network transport … synchronization
  mechanism" ou use uma camada de rede "other than that intended or provided by SQLite Cloud, Inc.". Isso exclui o
  GitHub como ponto de encontro.
- **Turso Sync:** "Turso sync uses a **last push wins** strategy." No pull, as mudanças locais não enviadas são
  revertidas e "replayed on top". Precisa de Turso Cloud ou de um `tursodb --sync-server`.
- **Automerge:** em escrita concorrente na mesma propriedade, "the choice is arbitrary, but deterministic"; os
  perdedores "are merely relegated to a conflicts object" (`getConflicts`). É o único CRDT que guarda a colisão de
  forma consultável, mas é um modelo de documento JSON, não um banco relacional.
- **Syzy, Marmot:** última escrita por linha, sem binário Windows (Syzy: "Linux and macOS, amd64 and arm64"; Marmot
  v2.8.0 só tem darwin e linux).

## 4. O GitHub privado serve para o banco? (pergunta do ticket 06)

| Mecanismo | Serve? | Como |
|---|---|---|
| Dolt | **sim** | remote git nativo, ref `refs/dolt/data`, SSH `git@github.com:…`. A ref não mistura com as branches de arquivos. |
| Texto por linha | **sim** | é o desenho atual: arquivos comuns, com a deploy key e o sincronizador do ticket 08. |
| Sessão do SQLite, cr-sqlite | sim, com montagem | transporte "burro" de arquivos de changeset; ordem, base e reaplicação ficam por conta própria. |
| sqlite-sync | **não** | a licença proíbe outro transporte. |
| Turso, Syzy, Marmot, Corrosion, sqlsync | não | exigem servidor de sync ou malha entre as máquinas. |

## 5. Recomendação (a decisão é do Gustavo)

1. **Descartar a família CRDT para a verdade do hub.** Todas as opções resolvem a mesma célula em silêncio, o que
   viola "nada diverge em silêncio" (ticket 08, item 3: parar e avisar). Automerge e Syzy guardam o perdedor, mas
   não param.
2. **Levar duas opções a um spike no Windows:**
   - **(a) Dolt com o GitHub como remote git.** É o único produto pronto que para e avisa, desfaz a junção sozinho
     em autocommit e usa o ponto de encontro já decidido. Pontos a medir no spike: deploy key no Windows; o
     sincronizador como envoltório de `dolt pull`/`dolt push`; um escritor só no modo embutido; colisão por célula
     em notas longas; tamanho do repositório.
   - **(b) Texto por linha no git** (um arquivo por registro, no estilo do sql-md-sync, com o banco reconstruído
     localmente). Mantém o ticket 08 inteiro. O custo é que a verdade volta a trafegar como texto.
3. **A extensão de sessão do SQLite fica como reserva** se o Dolt falhar e o texto por linha não servir. Ela detecta
   a colisão, mas o sincronizador inteiro teria de ser escrito.

Pontos que a decisão precisa encarar, qualquer que seja a escolha: a proteção de edição concorrente na mesma máquina
(ticket 08, item 4) muda de natureza com um banco, porque transações substituem a conferência de versão por arquivo;
e a busca por texto (FTS) não viaja pela extensão de sessão nem, NV, pelo Dolt da mesma forma que pelo SQLite.
