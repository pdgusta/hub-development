# 54: A busca dentro do vault deixa o CLI do LiveSync lento

Type: task
Status: ready-for-agent
Etapa: conserto do 26 (achado na instalação do par B)
Blocked by: nenhum

**What to build:** Achado do maestro do par B em 2026-10-21 ~13h45 e confirmado às 13h58
(`.scratch/context-hub/retomada-maestro-par-b.md`, recados ao A). O passo 03 instala a busca em
`C:/context-hub/.local/busca` (8.588 arquivos, 538 MB) antes de o hub descer. A cada arquivo que grava, o CLI do
LiveSync refaz a lista do vault inteiro no filtro de nomes repetidos (`isAcceptedInFilenameDuplicationFactory` →
`getFileNames()` → `scanDirectoryInto`, sem pular pastas com ponto, com `lstat` em cada segmento). No B foram 83.947
`lstat` e 13,6 s por volta; o perfil de CPU deu 62% em `assertNoSymbolicLinks`. Com a busca fora do vault, a descida
foi de 10 arquivos a cada 4 min para cerca de 1 arquivo/s. O custo também vale em regime, no A inclusive (cada evento
de arquivo dispara a varredura inteira; não medido no A).

Caminhos a decidir (antes, fonte primária no código do CLI do LiveSync):
- busca fora do vault (por exemplo, `C:/hub-par/busca`), com o kit e o MCP da busca apontando para lá;
- ou a varredura do CLI sem as pastas com ponto (mudança no fork ou na configuração, se houver opção).

## Pesquisa (2026-10-24, maestro do B, fonte primária)

Código lido: o CLI instalado no B (`C:/hub-par/livesync`, commit 14141446, commonlib 0.1.36) e o `main` de hoje dos
dois repositórios (`vrtmrz/obsidian-livesync` e `vrtmrz/livesync-commonlib`, pelo `gh api`).

- **O filtro.** `isAcceptedInFilenameDuplicationFactory` (`livesync-commonlib`, `src/serviceFeatures/targetFilter.ts`)
  é o primeiro filtro de `vault.isTargetFile` (prioridade 10). Quando muda o `totalStorageFileEventCount`, ele chama
  `storageAccess.getFileNames()` e conta os nomes do vault inteiro. Essa contagem vem **antes** de olhar
  `shouldCheckCaseInsensitively()`, ou seja, ela roda mesmo com `handleFilenameCaseSensitive` ligado. O único desvio
  é a opção `skipCaseCollisionCheck`, que só o `ServiceFileHandlerBase` passa, e só em `canRecordStorageDeletion`
  (remoções), não nas gravações.
- **Ignorar não ajuda.** O filtro dos arquivos de ignorar (`useIgnoreFiles`/`ignoreFiles`, prioridade 20) e o do
  banco local (`isTargetFile`, prioridade 30) vêm depois e não encurtam a lista que o `getFileNames()` monta. Não há
  configuração que tire uma pasta dessa varredura.
- **Onde está a diferença.** No Obsidian, `getFileNames()` usa a lista de arquivos do próprio Obsidian, que não entra
  nas pastas com ponto: o LiveSync precisa de um recurso à parte, o Hidden File Sync, para essas pastas
  (`docs/glossary.md`, `docs/tips/hidden-file-sync.md`). No CLI, `NodeFileSystemAdapter.getFiles()`
  (`src/apps/cli/adapters/NodeFileSystemAdapter.ts`) chama `scanDirectoryInto("")`, que desce em **todas** as
  pastas, `.local` e `.git` inclusive, sem filtro. O `getFilesIncludeHidden` da commonlib pula `.git`, `.trash` e
  `node_modules`; o `getFiles` do CLI não pula nada.
- **No `main` de hoje continua igual.** O B está 98 commits atrás; nesse intervalo o adaptador e o filtro mudaram
  (NFC, 2026-10-17), mas a varredura continua inteira e sem filtro. Nenhuma issue achada sobre isso (`gh search
  issues`, duas buscas).
- **Tamanho no B hoje:** `.local/busca` tem 8.592 arquivos (538 MB); o resto de `.local` tem 5 arquivos pequenos;
  `.git` tem 30 arquivos; o hub fora disso tem 599.
- **Quem usa o caminho `.local/busca`:** `kit/par/03-busca.ps1` (destino da instalação), `skills/busca/iniciar.ps1`
  (pacote, com a variável `HUB_BUSCA_OHS` como desvio, e `XDG_CACHE_HOME` fixo em `.local/busca/estado`),
  `skills/busca/relatorio.mjs`, `skills/busca/SKILL.md`, `kit/cliente/ligar-cliente.ps1`, `kit/par/proxy/proxy.psm1`,
  `kit/par/08-harnesses.mjs`, o teste `12-kit-busca` e as docs (`busca.md`, `kit-de-par.md`, `instalacao.md`,
  `operacao.md`). Não conferido linha a linha em cada um.

Caminhos, com o que a pesquisa mostrou:
- **A. Busca fora do vault** (por exemplo, `C:/hub-par/busca`, ao lado de `banco`, `cli-db` e `livesync`): conserto só
  no kit e na skill da busca, sem mexer no CLI. Tira 93% da varredura; o que sobra (~640 arquivos) custa pouco. Pede
  uma chave nova no `.env` (ex.: `HUB_BUSCA_DIR`) e a mudança nos dois pares.
- **B. Remendo no CLI**: `getFiles()` pulando as pastas com ponto, como o Obsidian faz. Pega também `.git` e qualquer
  pasta com ponto futura, mas é um remendo para manter a cada versão do CLI, que hoje montamos do original sem fork.
  Pode virar issue ou PR no projeto original (pede o aval do Gustavo: publica fora).

## Decisão (Gustavo, 2026-10-24, Maestri Chat, thread azul)

**Caminho A: a busca sai do vault.** Instalação e estado da busca em `C:/hub-par/busca` (ao lado de `banco`, `cli-db`
e `livesync`), por uma chave nova no `.env` (nome a definir na construção; sugestão `HUB_BUSCA_DIR`). O CLI do LiveSync
não muda; issue no projeto original não foi pedida.

- [x] decisão registrada aqui
- [ ] conserto no kit, com teste
- [ ] medida no A antes e depois (tempo da varredura com e sem `.local`)

## Comments

- 2026-10-24 (maestro do A): aberto a partir do recado do B. Precisa de triagem: escolher o caminho.
- 2026-10-24 (maestro do A): Gustavo: o maestro do B conserta. Dono: maestro do par B.
- 2026-10-24 (maestro do B): pesquisa feita (seção acima). Recomendação: caminho A (busca fora do vault). Esperando
  a escolha do Gustavo.
- 2026-10-24 (maestro do B): Gustavo escolheu o caminho A. Pronto para agente.
