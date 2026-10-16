# Pesquisa 47: disco e banco sem o Obsidian

Pesquisa em fonte primária, feita em 2026-10-12. Arquivos lidos brutos (`raw.githubusercontent.com`, API do
GitHub e registro do npm), baixados num diretório temporário fora do repo. Nada foi instalado, executado ou
testado, e nenhum contêiner foi tocado. A única leitura local foi a de chaves de configuração do spike
(`C:\Projetos\spike-livesync\cofre-*\.obsidian\plugins\obsidian-livesync\data.json` e `couchdb-init.ini`), sem
copiar segredos. É saída de modelo: confira as citações antes de decidir.

Ticket: `.scratch/context-hub/issues/47-disco-e-banco-sem-o-obsidian-pesquisa.md`. Contexto: "Spike: CouchDB e
LiveSync" (`30-spike-couchdb-livesync.md`) e os comentários de "Revisão do sync e da divergência com o banco"
(`33-revisao-do-sync-e-da-divergencia.md`, R61, R68 e R69).

**Versões lidas**

| Fonte | Versão | Observação |
|---|---|---|
| `vrtmrz/obsidian-livesync` | `main` em [`1414144`](https://github.com/vrtmrz/obsidian-livesync/tree/14141446a14deab3353a8864dee41e44c372d006) (2026-10-05) | 1 commit à frente da tag `1.0.35`, a versão do spike; o CLI do `main` tem `"version": "1.0.35-cli"` |
| `vrtmrz/livesync-commonlib` | `main` em [`c81c08b`](https://github.com/vrtmrz/livesync-commonlib/tree/c81c08b36f136e9b2c733e27d399acb0fc5ccee4) (2026-10-12) | o plugin 1.0.35 fixa o pacote npm `@vrtmrz/livesync-commonlib` **0.1.36**; os fatos-chave (padrão de 50 MB, `isPlainText`, tamanhos de chunk) foram conferidos também no `dist/` do tarball 0.1.36 |
| `vrtmrz/livesync-bridge` | `main` em [`5645cf6`](https://github.com/vrtmrz/livesync-bridge/tree/5645cf6a74e863ccc29bc2e9dedef1c4941e096b) (2026-10-05) | fixa a commonlib **0.1.19** |
| `apache/couchdb` | branch `3.5.x` (docs e `rel/overlay/etc/default.ini`) | o spike roda CouchDB 3.5.2 |
| `paulmillr/chokidar` | tag `4.0.3` | a versão travada no `package-lock.json` do LiveSync 1.0.35 |
| `obsidianmd/obsidian-api`, `obsidianmd/obsidian-help` | `master` | |

Abreviações nos links: **LS** = `vrtmrz/obsidian-livesync@1414144`, **CL** = `vrtmrz/livesync-commonlib@c81c08b`,
**BR** = `vrtmrz/livesync-bridge@5645cf6`, **CDB** = `apache/couchdb@3.5.x`.

## Resumo

- **O plugin só leva o que o Obsidian enxerga.** Ele ouve os eventos do cofre do Obsidian, sem filtro de
  extensão próprio. A doc de problemas do LiveSync manda ligar o **"Detect all file extensions"** do Obsidian
  quando um ZIP "ou outra extensão" não sincroniza. Sem essa opção, `.docx`, `.xlsx`, `.zip` e até `.csv` (que
  não está na lista de formatos do Obsidian) ficam fora. Pastas com ponto ficam fora sempre.
- **Binário vira `newnote`**: o conteúdo é cortado em pedaços e cada pedaço é gravado como texto Base64
  (+33%). Quem decide se é texto é a extensão (`isPlainText`: `.md`, `.txt`, `.svg`, `.html`, `.csv`, `.css`,
  `.js`, `.xml`, `.canvas`). O resto é binário.
- **Correção da rodada 1:** colisão de binário **não** pergunta ao usuário. O código resolve sozinho: fica a
  versão de `mtime` mais novo, e o outro ramo é apagado, mesmo com "Always overwrite with a newer file"
  desligado. A doc chama isso de comportamento herdado, "not a new 1.0 guarantee".
- **`syncMaxSizeInMB` padrão = 50** (cofre novo e no spike). Acima disso, a mudança é pulada nos dois sentidos,
  com um aviso no log. O arquivo fica só no disco de quem tem, e a versão antiga continua no banco.
- **O limite do CouchDB não é o gargalo.** `max_document_size` vale 8 000 000 bytes por padrão. O LiveSync e o
  spike sobem para 50 MB, e um pedaço de binário tem no máximo 4 MiB brutos (cerca de 5,6 MB em Base64). Como
  o LiveSync não usa anexos, `max_attachment_size` (1 GiB) não entra. `max_http_request_size` padrão: 4 GB.
- **O custo do binário está no histórico.** Cada versão nova de um formato já comprimido (docx, xlsx, pdf,
  jpg) gera pedaços quase todos novos (inferência). Os pedaços antigos são documentos vivos: a compactação
  automática não os remove, e a replicação os leva ao outro par. Só o "Garbage Collection V3" os apaga, e ele é
  beta, manual, fica no "Edge Case mode" e troca histórico por espaço.
- **CLI `daemon` no Windows:** o README declara "Cross-platform (Windows, macOS, Linux)", mas a instalação
  documentada é só systemd ou Docker, e todo o CI roda em `ubuntu-latest`. Para instalar, compila-se do
  código-fonte com Node (a commonlib pede Node >= 20; a imagem Docker usa Node 22). Não há receita de serviço
  para Windows. O observador é o chokidar 4.0.3 com `fs.watch`, que no Windows usa `ReadDirectoryChangesW`.
  O CLI leva **todo arquivo** fora de pastas com ponto, da regra de ignorar e do limite de tamanho. Tem banco
  LevelDB próprio, e o conflito sem resolução automática fica aberto até um `resolve`.
- **Riscos abertos no CLI:** a issue
  [#835](https://github.com/vrtmrz/obsidian-livesync/issues/835) (documento vazio no remoto com E2EE e
  ofuscação de caminho, reproduzida no `main` em 2026-09-16) está aberta. Há também uma suspeita minha, a
  testar, sobre o filtro de pastas com ponto no Windows (ver a pergunta 3).
- **Plugin e CLI na mesma pasta:** nenhuma fonte primária trata disso. O README do plugin diz "Do not enable
  this plug-in alongside another synchronisation solution". O revezamento está mais perto do desenho: os dois
  fazem varredura de partida e detectam edições e apagamentos feitos enquanto estavam parados. Os dois sempre
  ligados é território não documentado. Ambos precisam de teste.
- **`livesync-bridge`:** existe e é do mesmo autor. Roda em Deno, cuida explicitamente do Windows nos caminhos,
  grava direto no CouchDB sem banco local e **não trata conflito**. Fixa uma commonlib antiga e tem issues
  abertas de perda silenciosa de mudanças. Não serve como peça principal.

## 1. Arquivos além do `.md` no plugin Self-hosted LiveSync

### 1.1 Que arquivos o plugin leva

- O plugin ouve os eventos do cofre do Obsidian (`create`, `modify`, `delete`, `rename`, `raw`), sem filtro de
  extensão no adaptador ([LS `src/managers/ObsidianStorageEventManagerAdapter.ts`, linhas 106-111](https://github.com/vrtmrz/obsidian-livesync/blob/14141446a14deab3353a8864dee41e44c372d006/src/managers/ObsidianStorageEventManagerAdapter.ts#L106-L111)):

  ```ts
  plugin.registerEvent(plugin.app.vault.on("create", boundHandlers.onCreate));
  plugin.registerEvent(plugin.app.vault.on("modify", boundHandlers.onChange));
  ```

- Por isso o plugin depende do que o Obsidian indexa. A doc de problemas do LiveSync diz isso com todas as
  letras ([LS `docs/troubleshooting.md`](https://github.com/vrtmrz/obsidian-livesync/blob/14141446a14deab3353a8864dee41e44c372d006/docs/troubleshooting.md)):

  > ### ZIP or another extension is not synchronised
  > Enable Obsidian's `Detect all file extensions`, then check LiveSync selectors, ignore rules, and size limits

  > Check Obsidian's `Detect all file extensions`, LiveSync selectors, ignore files, file-size limits,
  > modification-time limits, and Hidden File Sync rules.

- A ajuda do Obsidian lista os formatos que ele "supports": `.md`, `.base`, `.canvas`, imagens (`.avif`, `.bmp`,
  `.gif`, `.jpeg`, `.jpg`, `.png`, `.svg`, `.webp`), áudio, vídeo e `.pdf`
  ([obsidian-help `en/Files and folders/Accepted file formats.md`](https://github.com/obsidianmd/obsidian-help/blob/master/en/Files%20and%20folders/Accepted%20file%20formats.md)).
  `.docx`, `.xlsx`, `.zip` e `.csv` não estão na lista.
- **Não verificado:** a ajuda do Obsidian não documenta o "Detect all file extensions" (nem onde fica, nem o
  efeito exato sobre `vault.getFiles()`). A API só diz "Get all files in the vault"
  ([obsidian-api `obsidian.d.ts`](https://github.com/obsidianmd/obsidian-api/blob/master/obsidian.d.ts)). O
  efeito vem só da doc do LiveSync citada acima.
- Pastas com ponto (`.git`, `.obsidian`) ficam fora do sync normal e só entram pelo "Hidden File Sync", que é
  um recurso à parte ([LS `docs/tips/hidden-file-sync.md`](https://github.com/vrtmrz/obsidian-livesync/blob/14141446a14deab3353a8864dee41e44c372d006/docs/tips/hidden-file-sync.md)). Isso confirma o
  fato já registrado na R61.
- Filtros do próprio plugin, na ordem da doc de configurações
  ([LS `docs/settings.md`, "Selector (Advanced)"](https://github.com/vrtmrz/obsidian-livesync/blob/14141446a14deab3353a8864dee41e44c372d006/docs/settings.md)):
  "Synchronising files" (regex, vazio = tudo), "Non-Synchronising files" (regex), "Maximum file size"
  (`syncMaxSizeInMB`) e "(Beta) Use ignore files" (`useIgnoreFiles`, que lê `.gitignore` por padrão).

### 1.2 Como um binário é guardado

- Cada arquivo é **um documento de metadados mais vários pedaços (chunks)**
  ([LS `docs/datastructure.md`](https://github.com/vrtmrz/obsidian-livesync/blob/14141446a14deab3353a8864dee41e44c372d006/docs/datastructure.md)):

  > - `plain`, for text content represented by literal text Chunks; and
  > - `newnote`, for binary content represented by Base64 Chunks.

  > A `leaf` stores one content-addressed piece. For `plain` Metadata, `data` is literal text. For `newnote`
  > Metadata, `data` is Base64 text representing binary bytes.

- Os pedaços são documentos `h:…` com ID derivado do conteúdo. Com E2EE, viram `h:+…`, "Chunk whose identifier
  incorporates encryption material" (mesma página). Não há anexos do CouchDB (`_attachments`) no formato.
- **Quem é texto e quem é binário** é decidido só pela extensão
  ([CL `src/string_and_binary/path.ts`, linhas 167-178](https://github.com/vrtmrz/livesync-commonlib/blob/c81c08b36f136e9b2c733e27d399acb0fc5ccee4/src/string_and_binary/path.ts#L167-L178);
  igual no `dist/` da 0.1.36):

  ```ts
  export function isPlainText(filename: string): boolean {
      if (filename.endsWith(".md")) return true;
      if (filename.endsWith(".txt")) return true;
      if (filename.endsWith(".svg")) return true;
      if (filename.endsWith(".html")) return true;
      if (filename.endsWith(".csv")) return true;
      if (filename.endsWith(".css")) return true;
      if (filename.endsWith(".js")) return true;
      if (filename.endsWith(".xml")) return true;
      if (filename.endsWith(".canvas")) return true;
      return false;
  }
  ```

  Ou seja, `.pdf`, `.docx`, `.xlsx`, `.png` e `.zip` são binários, e `.csv` e `.svg` são texto.
- **Tamanho dos pedaços** (algoritmo padrão `v3-rabin-karp`;
  [CL `src/string_and_binary/chunks.ts`, linhas 493-536](https://github.com/vrtmrz/livesync-commonlib/blob/c81c08b36f136e9b2c733e27d399acb0fc5ccee4/src/string_and_binary/chunks.ts#L493-L536),
  e [CL `src/ContentSplitter/ContentSplitterBase.ts`, linhas 66-73](https://github.com/vrtmrz/livesync-commonlib/blob/c81c08b36f136e9b2c733e27d399acb0fc5ccee4/src/ContentSplitter/ContentSplitterBase.ts#L66-L73)):

  ```ts
  const chunkUnitBinary = 256 * 1024; // 256KB for binary
  const fixedAvgChunkSize = plainSplit ? chunkUnitPlain * 4 : chunkUnitBinary * 4; // 256B (in unit) for text, 1MB for binary
  const fixedMaxChunkSize = plainSplit ? chunkUnitPlain * 16 : chunkUnitBinary * 16; // 1KB for text, 4MB for binary
  ...
  const maxChunkSize = Math.min(fixedMaxChunkSize, effectiveAbsoluteMaxPieceSize);
  ```

  O teto vem de `MAX_DOC_SIZE_BIN (102400) * (customChunkSize + 1)`, com piso de 30 KiB. A conta é minha, a
  partir desse código:

  | `customChunkSize` | Pedaço de binário (mín / médio / máx) | Onde aparece |
  |---|---|---|
  | 0 | 100 / 100 / 100 KiB (tamanho fixo) | **no spike** (`data.json` dos dois cofres) |
  | 60 | 256 KiB / 1 MiB / 4 MiB | `PREFERRED_SETTING_SELF_HOSTED` ([CL `src/common/models/setting.const.preferred.ts`](https://github.com/vrtmrz/livesync-commonlib/blob/c81c08b36f136e9b2c733e27d399acb0fc5ccee4/src/common/models/setting.const.preferred.ts)) |

  - Texto `.md`, `.txt` ou `.canvas` com 4 MB ou mais passa a ser cortado como binário ("For very large text
    files, we should increase the chunk size", mesmo arquivo).
  - **Inferência:** com `customChunkSize: 0`, o corte do binário é de tamanho fixo. Um byte inserido no meio
    desloca todos os pedaços seguintes. O "Config Doctor" que reclamou do tamanho de chunk no spike deve ter
    apontado para isso; não conferi a mensagem.

### 1.3 Por que binário não tem junção automática

- A junção automática só existe para texto e dados estruturados que tenham uma revisão comum
  ([LS `docs/specs_conflict_resolution.md`](https://github.com/vrtmrz/obsidian-livesync/blob/14141446a14deab3353a8864dee41e44c372d006/docs/specs_conflict_resolution.md)):

  > | Binary contents differ | Prefer an explicit user selection; semantic merge is unavailable. |

  > The compatibility implementation currently selects the newer modification time for differing binary
  > conflicts even when the general **Always overwrite with a newer file** option is disabled. This is existing
  > behaviour, not a new 1.0 guarantee.

- O código confirma: binário cai no mesmo caminho do "mais novo vence" e apaga o ramo perdedor sem abrir o modal
  ([LS `src/serviceFeatures/conflictResolution/operations.ts`, linhas 146-162](https://github.com/vrtmrz/obsidian-livesync/blob/14141446a14deab3353a8864dee41e44c372d006/src/serviceFeatures/conflictResolution/operations.ts#L146-L162)):

  ```ts
  const isSame = leftLeaf.data == rightLeaf.data && leftLeaf.deleted == rightLeaf.deleted;
  const isBinary = !isPlainText(path);
  const alwaysNewer = dependencies.currentSettings().resolveConflictsByNewerFile;
  if (isSame || isBinary || alwaysNewer) {
      const result = compareMTime(leftLeaf.mtime, rightLeaf.mtime);
      ...
      return await dependencies.conflict.resolveByDeletingRevision(path, loser.rev, subTitle);
  }
  ```

- Esse recurso vive em `LiveSyncBaseCore` (`useConflictResolutionFeature(this)`), que o CLI também usa
  ([LS `src/LiveSyncBaseCore.ts`, linha 293](https://github.com/vrtmrz/obsidian-livesync/blob/14141446a14deab3353a8864dee41e44c372d006/src/LiveSyncBaseCore.ts#L293)).
  A mesma regra vale para o CLI.
- **Por que não há junção (explicação):** a junção de texto compara linhas e trechos contra a revisão comum
  (`diff_match_patch` no mesmo arquivo). Num binário, um byte não tem sentido isolado, e não existe "trecho"
  que se possa juntar sem conhecer o formato.
- **Correção do que foi registrado na R61** ("colisão é sempre escolher um lado"): o lado é escolhido **pelo
  `mtime`, sem perguntar**. O ramo perdedor vira uma revisão apagada. Pela doc de GC, seus pedaços ficam até um
  GC; o corpo dos metadados fica até a compactação (ver a pergunta 2).
- **Não verificado:** como o Gustavo recuperaria a versão perdida de um binário pela interface do plugin. O
  CLI tem `cat-rev` e `pull-rev`, mas só para revisões ainda legíveis.

### 1.4 `syncMaxSizeInMB`: padrão e arquivo grande

- **Padrão: 50** nos três lugares do código: o padrão do esquema, `PREFERRED_BASE` (cofre novo) e o modelo de
  "tweak values" compartilhados
  ([CL `src/common/models/setting.const.defaults.ts`](https://github.com/vrtmrz/livesync-commonlib/blob/c81c08b36f136e9b2c733e27d399acb0fc5ccee4/src/common/models/setting.const.defaults.ts),
  [CL `setting.const.preferred.ts`](https://github.com/vrtmrz/livesync-commonlib/blob/c81c08b36f136e9b2c733e27d399acb0fc5ccee4/src/common/models/setting.const.preferred.ts);
  `syncMaxSizeInMB: 50` também em `dist/common/models/tweak.definition.js` da 0.1.36). No spike, os dois
  cofres estão com `"syncMaxSizeInMB": 50`.
- A regra ([CL `src/services/base/VaultService.ts`, linhas 73-81](https://github.com/vrtmrz/livesync-commonlib/blob/c81c08b36f136e9b2c733e27d399acb0fc5ccee4/src/services/base/VaultService.ts#L73-L81)):

  ```ts
  isFileSizeTooLarge(size: number) {
      const maxSize = this.settings.syncMaxSizeInMB;
      if (maxSize > 0 && size > 0) {
          if (maxSize * 1024 * 1024 < size) {
  ```

  Ou seja, o limite é de 50 MiB, e 0 desliga a checagem.
- O que acontece com arquivo grande:
  - **Disco → banco:** a mudança é pulada com aviso no log, nível NOTICE
    ([CL `src/managers/StorageEventManager.ts`, linhas 209-217](https://github.com/vrtmrz/livesync-commonlib/blob/c81c08b36f136e9b2c733e27d399acb0fc5ccee4/src/managers/StorageEventManager.ts#L209-L217)):
    `The storage file has been changed but exceeds the maximum size. Skipping`.
  - **Banco → disco:** a entrada também é pulada ("is too large (on database) to be processed") e, se o
    arquivo do disco é grande, ele não é sobrescrito ("too large (on storage)")
    ([CL `src/serviceModules/ServiceFileHandlerBase.ts`, linhas 1650-1675](https://github.com/vrtmrz/livesync-commonlib/blob/c81c08b36f136e9b2c733e27d399acb0fc5ccee4/src/serviceModules/ServiceFileHandlerBase.ts#L1650-L1675)).
  - A doc de configurações: "changes to local and remote files that are larger than this will be skipped. If
    the file becomes smaller again, a newer one will be used." O mesmo trecho diz que, quando os critérios se
    alargam, o LiveSync reavalia o que já está no banco, e que estreitá-los "does not delete files which have
    already been reflected".
  - **Consequência (inferência):** um arquivo que cresce além do limite fica com a última versão pequena no
    banco e na outra máquina. A diferença só aparece como aviso no log; não há conflito nem marca de
    divergência.
- Issues abertas com arquivos grandes, no celular e no plugin:
  [#469](https://github.com/vrtmrz/obsidian-livesync/issues/469) (MP4 pulados pelo limite; um usuário
  relata travamentos com 60-100 MB), [#359](https://github.com/vrtmrz/obsidian-livesync/issues/359) e
  [#680](https://github.com/vrtmrz/obsidian-livesync/issues/680) (iOS). Na #359, o autor explica que o limite
  por tamanho nasceu justamente disso: "we seem unable to synchronise the large file on the mobile platform".

## 2. Limites do CouchDB e impacto de binários

### 2.1 Os limites

| Opção | Padrão do CouchDB 3.5 | No LiveSync e no spike | Vale para o formato do LiveSync? |
|---|---|---|---|
| `[couchdb] max_document_size` | 8 000 000 bytes | 50 000 000 (`docker/config/livesync.ini` do LiveSync; `couchdb-init.ini` do spike) | Sim: cada pedaço e cada metadado é um documento |
| `[couchdb] max_attachment_size` | 1 073 741 824 (1 GiB) | não mexido | **Não**: o formato não usa anexos |
| `[chttpd] max_http_request_size` | 4 294 967 296 (4 GB) | 4 294 967 296 | Sim: vale para o `_bulk_docs` inteiro |
| `[smoosh]` compactação automática | ratio >= 2.0 ou slack >= 512 MiB | não mexido | Sim |

- `max_document_size`
  ([CDB `src/docs/src/config/couchdb.rst`](https://github.com/apache/couchdb/blob/3.5.x/src/docs/src/config/couchdb.rst)):

  > Limit maximum document body size. Size is calculated based on the serialized Erlang representation of the
  > JSON document body [...] In particular, this limit does not include attachments. HTTP requests which create
  > or update documents will fail with error code 413 if one or more documents is larger than this
  > configuration value.

- `max_attachment_size` só aparece comentado no `default.ini` ("Maximum attachment size", 1 gibibyte)
  ([CDB `rel/overlay/etc/default.ini`, linhas 70-72](https://github.com/apache/couchdb/blob/3.5.x/rel/overlay/etc/default.ini#L70-L72)).
- `max_http_request_size`
  ([CDB `src/docs/src/config/http.rst`](https://github.com/apache/couchdb/blob/3.5.x/src/docs/src/config/http.rst)):
  "This setting applies to all requests and it doesn't discriminate between single vs. multi-document
  operations", com padrão `4294967296 ; 4 GB`.
- A config recomendada do LiveSync
  ([LS `docker/config/livesync.ini`](https://github.com/vrtmrz/obsidian-livesync/blob/14141446a14deab3353a8864dee41e44c372d006/docker/config/livesync.ini)):

  ```ini
  [couchdb]
  ; Max size per document (50MB). Large enough for binary attachments.
  max_document_size = 50000000
  ```

- **Conta (inferência a partir das fontes acima):** o maior pedaço de binário tem 4 MiB brutos, ou cerca de
  5,6 MB em Base64. Pelo RFC 4648 §4, o Base64 transforma "24-bit groups of input bits as output strings of 4
  encoded characters", ou seja, +33%
  ([RFC 4648](https://www.rfc-editor.org/rfc/rfc4648.txt)). Isso cabe até no padrão de 8 MB. No spike
  (`customChunkSize: 0`), cada pedaço tem cerca de 137 KB em Base64. **O limite que manda é o `syncMaxSizeInMB`
  do plugin, não o do CouchDB.**
- **Não verificado:** quanto o E2EE acrescenta ao tamanho de um pedaço já em Base64.
- Proxy reverso: a doc do LiveSync avisa do `413 Entity too large` no nginx (`client_max_body_size 50M`,
  [LS `docs/setup_own_server.md`](https://github.com/vrtmrz/obsidian-livesync/blob/14141446a14deab3353a8864dee41e44c372d006/docs/setup_own_server.md)).
  Na topologia decidida, um CouchDB por par ligado direto pela tailnet, não há proxy (inferência).

### 2.2 O que cada versão nova de um binário custa

- **Espaço.**
  - Os pedaços têm endereço pelo conteúdo e são compartilhados: "matching chunks can be shared between
    branches" ([LS `docs/specs_conflict_resolution.md`](https://github.com/vrtmrz/obsidian-livesync/blob/14141446a14deab3353a8864dee41e44c372d006/docs/specs_conflict_resolution.md)).
    Um pedaço igual não é regravado.
  - **Inferência, não testado:** formatos já comprimidos (docx e xlsx são pacotes ZIP, além de pdf, jpg e png)
    mudam quase todos os bytes a cada salvamento, então cada versão gera quase só pedaços novos. Um docx de
    10 MB salvo 5 vezes ocupa cerca de 6 × 10 MB × 1,33 ≈ 80 MB em cada CouchDB, mais o banco local de cada
    cliente.
  - Um `.md` editado gera só os pedaços dos trechos tocados (pedaços de cerca de 256 B a 1 KB, mesmo arquivo
    `chunks.ts`).
  - A issue aberta [#866](https://github.com/vrtmrz/obsidian-livesync/issues/866) relata inchaço do banco
    (2 GB em semanas) com edições pequenas num `.md` enorme. O autor ainda investiga.
- **Os pedaços antigos não somem sozinhos.** O "Garbage Collection V3"
  ([LS `docs/specs_garbage_collection.md`](https://github.com/vrtmrz/obsidian-livesync/blob/14141446a14deab3353a8864dee41e44c372d006/docs/specs_garbage_collection.md))
  é "a beta maintenance operation", disponível "in Edge Case mode for CouchDB", e exige "Fetch chunks on demand"
  desligado. Sobre o que ele libera:

  > An ordinary superseded linear revision does not protect its former chunks. Once no current file or conflict
  > leaf references a chunk, it can be collected.

  > Garbage Collection deliberately trades historical recoverability for storage.

- **Compactação do CouchDB.**
  - Automática desde a 2.1.1 ("smoosh"). Entra na fila quando `sizes.file / sizes.active` passa de 2,0 ou a
    folga passa de 512 MiB
    ([CDB `default.ini`, `[smoosh.ratio_dbs]` e `[smoosh.slack_dbs]`](https://github.com/apache/couchdb/blob/3.5.x/rel/overlay/etc/default.ini)).
  - Ela "requires roughly twice the disk storage", e "Old documents revisions are replaced with small amount of
    metadata called `tombstone`"
    ([CDB `src/docs/src/maintenance/compaction.rst`](https://github.com/apache/couchdb/blob/3.5.x/src/docs/src/maintenance/compaction.rst)).
  - **Inferência:** um pedaço é um documento com uma revisão só, e continua vivo. A compactação não o remove;
    ela só enxuga as revisões antigas dos **metadados**. Por isso o espaço do binário só volta com o GC V3.
- **Replicação entre pares.** O protocolo copia as revisões-folha: "the Replicator MUST fetch all Document
  Leaf Revisions from Source that are missed at Target", com `revs=true` só para a lista de ancestrais
  ([CDB `src/docs/src/replication/protocol.rst`](https://github.com/apache/couchdb/blob/3.5.x/src/docs/src/replication/protocol.rst)).
  Duas inferências:
  - Todo pedaço novo de toda versão de um binário vai ao outro par, porque cada pedaço é um documento vivo.
  - O corpo de uma revisão **antiga** de metadados não viaja; só a mais nova. O "rastro até a compactação" que
    o spike viu existe só no banco onde a revisão antiga foi gravada.
- **E2EE e compressão.**
  - Com E2EE, o ID do pedaço passa a `h:+…` e "incorporates encryption material"
    ([LS `docs/datastructure.md`](https://github.com/vrtmrz/obsidian-livesync/blob/14141446a14deab3353a8864dee41e44c372d006/docs/datastructure.md)).
    **Inferência:** a deduplicação entre versões continua, porque o ID é determinístico para a mesma
    passphrase.
  - A compressão opcional roda antes do E2EE. No benchmark do autor, ela reduziu os dados de pedaços em cerca
    de 9% num conjunto misto, com redução de **0%** no binário de alta entropia; JPEG, PNG e gzip "had already
    undergone format-level compression"
    ([LS `docs/specs_data_compression.md`](https://github.com/vrtmrz/obsidian-livesync/blob/14141446a14deab3353a8864dee41e44c372d006/docs/specs_data_compression.md)).
    Para binário de escritório, não compensa (inferência).

## 3. CLI do LiveSync em modo `daemon` no Windows nativo

### 3.1 O que é e como instalar

- Fonte: [LS `src/apps/cli/README.md`](https://github.com/vrtmrz/obsidian-livesync/blob/14141446a14deab3353a8864dee41e44c372d006/src/apps/cli/README.md).
  - "Command-line version of Self-hosted LiveSync plug-in for syncing vaults without Obsidian", "Cross-platform
    (Windows, macOS, Linux)", "built using the same core as the Obsidian plug-in".
  - `daemon` é o comando padrão: "Run mirror scan then continuously sync CouchDB <-> local filesystem".
    - **CouchDB → disco:** pelo feed `_changes` ("sub-second latency") ou por sondagem com `--interval N`.
    - **Disco → CouchDB:** "via chokidar file watching. Any file created, modified, or deleted in the vault
      directory is pushed to CouchDB."
- **Instalação documentada:** só compilar do código-fonte (`npm install` na raiz, depois
  `npm run build -w self-hosted-livesync-cli` e `node src/apps/cli/dist/index.cjs …`), systemd (`deploy/install.sh`)
  ou Docker. **Nada para Windows nativo:** nem script, nem serviço, nem tarefa agendada.
- **Node:** o pacote npm da commonlib declara `"engines":{"node":">=20"}`
  ([registro npm, 0.1.36](https://registry.npmjs.org/@vrtmrz%2flivesync-commonlib/0.1.36)), e o Dockerfile do
  CLI usa `node:22-slim`
  ([LS `src/apps/cli/Dockerfile`](https://github.com/vrtmrz/obsidian-livesync/blob/14141446a14deab3353a8864dee41e44c372d006/src/apps/cli/Dockerfile)).
- **Banco local próprio:** PouchDB com `pouchdb-adapter-leveldb`
  ([LS `src/apps/cli/lib/pouchdb-node.ts`](https://github.com/vrtmrz/obsidian-livesync/blob/14141446a14deab3353a8864dee41e44c372d006/src/apps/cli/lib/pouchdb-node.ts)).
  A pasta do banco ganha o sufixo `-livesync-v2` (`SuffixDatabaseName`, na commonlib).
  **Não verificado:** se o módulo nativo do LevelDB compila ou tem binário pronto no Windows.
- **Onde ficam as coisas:**
  - `database-path` guarda `.livesync/settings.json` (com usuário, senha do CouchDB e passphrase em texto,
    como mostra o exemplo do README), `.livesync/runtime/` e a pasta LevelDB.
  - `--vault <path>` separa o cofre do banco ("Allows the PouchDB database directory and the actual vault
    directory to be different locations").
  - Sem `--vault`, o cofre é o próprio `database-path`. O código prevê esse caso: "PouchDB LevelDB database
    directory lives in the vault directory"
    ([LS `src/apps/cli/main.ts`, linhas 532-544](https://github.com/vrtmrz/obsidian-livesync/blob/14141446a14deab3353a8864dee41e44c372d006/src/apps/cli/main.ts#L532-L544)).
  - **Inferência:** para o hub, o banco e as credenciais devem ficar fora do cofre, com `--vault`. Senão o
    Obsidian enxerga a pasta LevelDB, que não começa com ponto.
- O CLI é um **dispositivo novo** para o remoto. Comentário na
  [#815](https://github.com/vrtmrz/obsidian-livesync/issues/815): o nó do dispositivo headless precisa estar
  em `accepted_nodes`. Para isso servem os comandos `mark-resolved` e `unlock-remote` (README do CLI).

### 3.2 Rodar como serviço ou tarefa agendada no Windows

- A fonte do LiveSync só cobre o systemd. A unidade usa `Restart=on-failure`, e o código conta com isso: no
  erro do observador, "Exiting for systemd restart", com `process.exit(1)`
  ([LS `src/apps/cli/managers/CLIStorageEventManagerAdapter.ts`, linhas 189-196](https://github.com/vrtmrz/obsidian-livesync/blob/14141446a14deab3353a8864dee41e44c372d006/src/apps/cli/managers/CLIStorageEventManagerAdapter.ts#L189-L196)).
  Se o CouchDB não responde na partida, o daemon também sai: "[Daemon] Initial replication failed, cannot
  continue" ([LS `src/apps/cli/commands/runCommand.ts`, linhas 59-66](https://github.com/vrtmrz/obsidian-livesync/blob/14141446a14deab3353a8864dee41e44c372d006/src/apps/cli/commands/runCommand.ts#L59-L66)).
  Sem um reinício automático, o daemon morre calado.
- **Caminho nativo do Windows (doc da Microsoft, não do LiveSync):** o `schtasks /create /sc ONLOGON` "runs
  whenever a user (any user) logs on", e `/delay` vale para ONSTART e ONLOGON
  ([windowsserverdocs `schtasks-create.md`](https://github.com/MicrosoftDocs/windowsserverdocs/blob/main/WindowsServerDocs/administration/windows-commands/schtasks-create.md)).
  **Não verificado:** reinício automático em falha pelo Agendador de Tarefas (a página do `schtasks /create`
  não tem esse parâmetro) e serviço do Windows por wrapper de terceiros.

### 3.3 O observador de arquivos (chokidar) em NTFS

- A configuração do CLI
  ([LS `CLIStorageEventManagerAdapter.ts`, linhas 141-162](https://github.com/vrtmrz/obsidian-livesync/blob/14141446a14deab3353a8864dee41e44c372d006/src/apps/cli/managers/CLIStorageEventManagerAdapter.ts#L141-L162)):

  ```ts
  const baseIgnored = [
      /(^|[/\\])\./,
      /(^|[/\\])[^/\\]*-livesync-v2([/\\]|$)/,
  ];
  ...
  const watcher = chokidarWatch(this.basePath, {
      ignored, ignoreInitial: true, persistent: true,
      awaitWriteFinish: { stabilityThreshold: 500, pollInterval: 100 },
  });
  ```

  As expressões aceitam `/` e `\`, então o observador ignora pastas com ponto também no Windows.
- O chokidar 4.0.3 usa `fs.watch` por padrão. O `usePolling` "is typically necessary [...] to successfully
  watch files over a network", e a variável `CHOKIDAR_USEPOLLING` liga a sondagem sem mexer no código. Sobre o
  `awaitWriteFinish`: "For accurate detection this parameter should be relatively high"
  ([chokidar 4.0.3 README](https://github.com/paulmillr/chokidar/blob/4.0.3/README.md)). O CLI usa 500 ms.
- No Windows, o `fs.watch` do Node "depends on `ReadDirectoryChangesW`". Além disso: "On Windows, no events will
  be emitted if the watched directory is moved or renamed. An `EPERM` error is reported when the watched
  directory is deleted" ([nodejs `doc/api/fs.md`, Caveats](https://github.com/nodejs/node/blob/v22.x/doc/api/fs.md#caveats)).
- **Suspeita (inferência, precisa de teste):** o filtro `isTargetFile` do CLI, usado na varredura de partida,
  quebra o caminho com `path.sep`
  ([LS `main.ts`, linhas 532-541](https://github.com/vrtmrz/obsidian-livesync/blob/14141446a14deab3353a8864dee41e44c372d006/src/apps/cli/main.ts#L532-L541)):

  ```ts
  const parts = targetPath.split(path.sep);
  if (parts.some((part) => part.startsWith("."))) { return false; }
  if (parts[0]?.endsWith("-livesync-v2")) { return false; }
  ```

  - O `path` é o `node:path`, cujo `sep` no Windows é `\`.
  - Mas os caminhos do cofre usam `/`: o `NodeStorageAdapter.list` faz `.replace(/\\/g, "/")`
    ([CL `src/platform/node/storage.ts`, linha 164](https://github.com/vrtmrz/livesync-commonlib/blob/c81c08b36f136e9b2c733e27d399acb0fc5ccee4/src/platform/node/storage.ts#L164)).
  - Então, no Windows, o caminho inteiro vira uma parte só. Uma pasta com ponto **na raiz** (`.git/…`) continua
    excluída. Uma pasta com ponto **aninhada** (`projeto/.venv/…`) passaria nesse filtro na varredura de
    partida; o observador, por sua vez, a ignora.

### 3.4 Que arquivos o CLI leva

- **Todo arquivo**, sem filtro de extensão. Ficam fora:
  - caminhos com parte começando por ponto;
  - a pasta `*-livesync-v2`;
  - os padrões de `.livesync/ignore` (minimatch, com `import: .gitignore`, sem negação; "Changes to this file
    require a daemon restart");
  - os filtros comuns da commonlib (regex do seletor, ignore files, `syncMaxSizeInMB`).
- O tipo `plain` ou `newnote` segue o `isPlainText` da seção 1.2. A ponte entre os dois clientes é a mesma
  commonlib.
- O daemon cuida de apagamentos. As notas da 1.0.29 dizem "The CLI daemon now synchronises files already
  present at start-up and picks up edits and deletions made while it was stopped"
  ([LS `docs/releases/1.0.md`](https://github.com/vrtmrz/obsidian-livesync/blob/14141446a14deab3353a8864dee41e44c372d006/docs/releases/1.0.md)).
  O teste de partida do daemon verifica apagamento feito com ele parado
  ([LS `src/apps/cli/testdeno/test-daemon-startup.ts`](https://github.com/vrtmrz/obsidian-livesync/blob/14141446a14deab3353a8864dee41e44c372d006/src/apps/cli/testdeno/test-daemon-startup.ts)).
  Isso difere do comando `mirror`, que segundo o README "does not respect file deletions".
- Regra da varredura (`NEWER_WINS`): o apagamento local só é aceito quando um mapa local de "última vez visto"
  prova que o arquivo existia ([CL `docs/offline-scanner.md`](https://github.com/vrtmrz/livesync-commonlib/blob/c81c08b36f136e9b2c733e27d399acb0fc5ccee4/docs/offline-scanner.md)).

### 3.5 Comportamento em conflito

- O núcleo é o mesmo do plugin (seção 1.3):
  - texto com revisão comum e trechos separados → junta sozinho;
  - binário → o `mtime` mais novo vence sozinho;
  - o resto pede interação.
- **Inferência:** o CLI não registra tratador para `resolveByUserInteraction` (nada no `NodeServiceHub.ts`).
  O conflito fica aberto no banco.
- Para ver e resolver, o README traz `ls` (o `*` marca conflito), `info` (lista `conflicts`) e
  `resolve <path> <rev>`. A varredura pula documentos em conflito ("Conflicted documents [...] are always
  skipped"), e o arquivo do disco não recebe nenhuma das duas versões até a resolução.
- O daemon desliga a checagem de configuração divergente: "The daemon should accept whatever configuration the
  remote has" ([LS `runCommand.ts`, linhas 52-55](https://github.com/vrtmrz/obsidian-livesync/blob/14141446a14deab3353a8864dee41e44c372d006/src/apps/cli/commands/runCommand.ts#L52-L55)).

### 3.6 Maturidade (issues oficiais)

| Issue | Estado | O que diz |
|---|---|---|
| [#835](https://github.com/vrtmrz/obsidian-livesync/issues/835) | aberta | No `daemon` com E2EE e ofuscação de caminho, o metadado chega ao remoto **vazio** (`children: []`, `size: 0`). Reproduzida no `main` (imagem `edge`) em 2026-09-16, no CouchDB 3.5.2 |
| [#847](https://github.com/vrtmrz/obsidian-livesync/issues/847) | aberta | Comentários de maio e junho: no `daemon` da linha 0.25.7x, edições depois da partida **não subiam**, só na varredura inicial (contorno: reiniciar o serviço a cada gravação). **Não verificado se persiste na 1.0** |
| [#1143](https://github.com/vrtmrz/obsidian-livesync/issues/1143) | aberta, mas corrigida | Na partida, o daemon apagava do banco arquivos presentes no disco. O autor diz que a correção (#1191) está na 1.0.29 |
| [#1142](https://github.com/vrtmrz/obsidian-livesync/issues/1142) | aberta | O `install.sh` (systemd) instalava um CLI quebrado. Corrigido na 1.0.26, segundo o autor |

- CI: os workflows do CLI (`cli-e2e.yml`, `cli-deno-tests.yml`, `unit-ci.yml`) rodam só em `ubuntu-latest`
  ([LS `.github/workflows/`](https://github.com/vrtmrz/obsidian-livesync/tree/14141446a14deab3353a8864dee41e44c372d006/.github/workflows)).
- Os testes do daemon que li cobrem regras de ignorar e a varredura de partida com dois daemons. Não cobrem
  edição contínua com o daemon rodando, binários nem Windows.

## 4. Plugin e CLI na mesma pasta

- **Nenhuma fonte primária trata desse caso**: README do CLI, docs do plugin, issues buscadas (consultas na
  seção "Registro de consultas").
- O que as fontes dizem e que se aplica:
  - O README do plugin, em destaque: "Do not enable this plug-in alongside another synchronisation solution
    (including iCloud and Obsidian Sync)"
    ([LS `README.md`](https://github.com/vrtmrz/obsidian-livesync/blob/14141446a14deab3353a8864dee41e44c372d006/README.md)).
    **Inferência:** um daemon do CLI na mesma pasta é outro escritor do mesmo disco, ainda que fale o mesmo
    formato.
  - Cada cliente guarda, no seu banco local, "the exact revision most recently reflected in each Vault file".
    Um arquivo que difere dessa revisão "is an edit of that revision", e "File bytes, rather than path, size,
    modification time, or revision generation, determine whether content is known"
    ([LS `docs/specs_conflict_resolution.md`](https://github.com/vrtmrz/obsidian-livesync/blob/14141446a14deab3353a8864dee41e44c372d006/docs/specs_conflict_resolution.md)).
  - Folhas com bytes idênticos são colapsadas sozinhas ("Both leaves contain identical bytes | Collapse the
    duplicate leaf", mesma página).
  - O CLI é "Compatible with Self-hosted LiveSync plug-in settings" e é um dispositivo próprio, com nó próprio
    no remoto (seção 3.1).
- **Os dois sempre ligados (inferência, precisa de teste).** Quando um dos dois grava no disco uma versão
  vinda do banco, o outro vê uma mudança de arquivo. Se ele ainda não recebeu essa revisão pela replicação, a
  regra acima o faz gravar uma revisão "filha" da versão anterior, com os mesmos bytes. Quando os dois ramos se
  encontram, os bytes iguais devem colapsar. O provável resultado é revisões extras, conflitos transitórios e
  gravações duplicadas no disco. Um ciclo sem fim parece improvável, porque os bytes convergem, mas isso não é
  garantia documentada.
- **Revezamento (inferência, precisa de teste).** É o uso mais próximo do que as fontes descrevem.
  - O plugin, ao abrir, faz a mesma varredura de partida, a "Full offline scan" da commonlib. Ela já pegou no
    spike a edição feita no disco com o Obsidian fechado.
  - O daemon, ao partir, "picks up edits and deletions made while it was stopped".
  - Na troca, cada lado encontra arquivos gravados pelo outro e decide pelo conteúdo e pela revisão
    registrada. O ponto a medir é se isso gera conflito falso em arquivo que o outro só baixou.

## 5. Outras ferramentas que ligam disco e CouchDB no formato do LiveSync

| Ferramenta | O que é | Windows | Banco local | Conflito | Situação |
|---|---|---|---|---|---|
| **livesync-bridge** ([BR `readme.md`](https://github.com/vrtmrz/livesync-bridge/blob/5645cf6a74e863ccc29bc2e9dedef1c4941e096b/readme.md)) | "custom replicator between Self-hosted LiveSync remote vaults and storage", em Deno; pares `couchdb` e `storage` | O exemplo traz um par Windows (`"cmd": "cmd", "args": ["/C", "script\\test.bat", …]`), e o código converte `\` em `/` (PR #78, fechado) | **Nenhum**: grava direto no CouchDB (`DirectFileManipulator`) | **Não trata.** O `put` grava por cima e só pula conteúdo igual ([BR `PeerCouchDB.ts`, linhas 72-100](https://github.com/vrtmrz/livesync-bridge/blob/5645cf6a74e863ccc29bc2e9dedef1c4941e096b/PeerCouchDB.ts#L72-L100)); inferência: o último a gravar vence | commonlib 0.1.19 ([BR `deno.jsonc`](https://github.com/vrtmrz/livesync-bridge/blob/5645cf6a74e863ccc29bc2e9dedef1c4941e096b/deno.jsonc)); issues abertas [#64](https://github.com/vrtmrz/livesync-bridge/issues/64) (o ponto do feed não é persistido: "restarts silently skip missed changes"), [#73](https://github.com/vrtmrz/livesync-bridge/issues/73) ("sometimes stops"), [#82](https://github.com/vrtmrz/livesync-bridge/issues/82) (perde `unlink`) e [#67](https://github.com/vrtmrz/livesync-bridge/issues/67) (observador morto sem alarme); 142 estrelas |
| **WebApp** do LiveSync ([LS `src/apps/webapp/README.md`](https://github.com/vrtmrz/obsidian-livesync/blob/14141446a14deab3353a8864dee41e44c372d006/src/apps/webapp/README.md)) | "experimental proof of concept" no navegador, com File System Access API | só com uma aba do Chromium aberta; "background execution [...] experimental" | IndexedDB | núcleo do LiveSync (não conferido) | não serve como daemon |
| **es617/obsidian-sync-mcp** (já no spike) | MCP que grava no CouchDB | Docker | não | `write_note` grava por cima (spike 30) | não observa o disco |
| **livesync-serverpeer** | par P2P sem interface (citado na #815) | não verificado | não verificado | não verificado | não liga disco (não verificado); último push em 2026-03-17 |

- Para o recorte dos itens 3 e 4, o bridge tem uma particularidade: o par `storage` usa `Deno.watchFs` por
  padrão e chokidar como opção ("For addressing Deno's and chokidar's compatibility issues (especially on
  Windows), we use Deno's fs watcher as the primary watcher",
  [BR `PeerStorage.ts`, linha 363](https://github.com/vrtmrz/livesync-bridge/blob/5645cf6a74e863ccc29bc2e9dedef1c4941e096b/PeerStorage.ts#L363)).
  Ele tem `scanOfflineChanges` para mudanças feitas com ele parado.
- **Inferência:** com o plugin aberto na mesma pasta, o bridge é um terceiro escritor que não respeita
  revisões. É pior que o CLI para a garantia de não perder versão.

## Por que binário é um problema, limite do CouchDB e impacto

Em linguagem simples, para a pergunta do Gustavo na R68:

1. **Não dá para juntar.** Num texto, duas pessoas mexendo em parágrafos diferentes podem ser costuradas. Num
   PDF ou num docx, os bytes não têm "parágrafos" que o LiveSync entenda. Então, numa colisão, ele **escolhe
   sozinho a versão mais nova pelo relógio e descarta a outra, sem perguntar**. Isso está no código e na doc,
   e corrige o que eu disse na rodada 1 ("escolher um lado"). A versão descartada some do disco, e o rastro no
   banco dura até a faxina.
2. **Cada salvamento pesa o arquivo inteiro.** O LiveSync corta o arquivo em pedaços e reaproveita os pedaços
   iguais. No `.md`, uma edição troca uns poucos pedaços pequenos. Num docx, xlsx, pdf ou imagem, o formato já
   vem comprimido e quase todos os bytes mudam, então quase todos os pedaços são novos (inferência, a medir no
   teste). Dez salvamentos de um docx de 10 MB pesam perto de 130 MB.
3. **Fica mais gordo no banco.** O binário é guardado como texto Base64, um terço maior.
4. **Nada é apagado sozinho.** Os pedaços de versões antigas continuam no banco e vão para a outra máquina. A
   compactação automática do CouchDB não os tira, porque são documentos vivos. Só uma faxina manual e beta do
   LiveSync (Garbage Collection V3) os remove, e ela apaga também a possibilidade de voltar a versões antigas.
5. **O limite do CouchDB não atrapalha.** Por padrão, cada documento pode ter até 8 MB. O LiveSync e o spike
   sobem para 50 MB, e ele nunca grava um pedaço maior que cerca de 5,6 MB. O limite que vale é o do plugin:
   **50 MB por arquivo**. Acima disso, o arquivo é pulado com um aviso no log, fica só no disco onde está, e a
   outra máquina continua com a versão antiga, sem conflito nem alarme.
6. **Impacto para a R68.** Levar todo arquivo comum até 50 MB funciona. O preço é:
   - ligar "Detect all file extensions" no Obsidian, ou docx, xlsx, zip e csv não entram pelo plugin;
   - aceitar que a colisão de binário é resolvida pelo mais novo;
   - acompanhar o crescimento do banco nas duas máquinas, com uma faxina eventual.

## Precisa de teste

Itens para "Teste: disco e banco sem o Obsidian" (`48-teste-disco-e-banco-sem-o-obsidian.md`), na montagem do
spike e com conteúdo de teste:

1. **Extensões no plugin:** gravar no cofre A um `.pdf`, `.png`, `.docx`, `.xlsx`, `.zip` e `.csv`, com
   "Detect all file extensions" desligado e depois ligado. Ver quais chegam ao banco (`h:` e metadados) e
   descem no cofre B.
2. **Limite de 50 MB:** um arquivo de cerca de 49 MB e outro de cerca de 51 MB. Conferir o aviso
   `exceeds the maximum size`, o que o cofre B recebe e o que acontece quando um arquivo que já estava no
   banco cresce além do limite.
3. **Colisão de binário:** editar o mesmo `.docx` nos dois cofres com B fechado. Confirmar que não abre modal
   e que fica o de `mtime` mais novo. Achar onde está a versão perdida (`info` e `cat-rev` do CLI, ou o Hatch
   "Inspect conflicts") antes e depois da compactação.
4. **Colisão de `.csv`:** é texto pelo `isPlainText`. Ver se abre o modal de diferenças como o `.md`.
5. **Custo em espaço:** registrar `GET /obsidian` (`sizes.file`, `sizes.active`, `sizes.external`,
   `doc_count`) e a contagem de documentos `h:` antes e depois de salvar 5 vezes um docx ou xlsx de cerca de
   10 MB, depois de `POST /obsidian/_compact` e, se o Gustavo quiser, depois do Garbage Collection V3.
   Repetir com `customChunkSize` 0 (atual) e 60 (preferido para servidor próprio) e anotar o que o "Config
   Doctor" diz.
6. **CLI no Windows, instalação:** Node 22, `npm install` e build na raiz. Ver se o LevelDB nativo instala
   sem compilador e se `node dist/index.cjs --help` roda. Usar `--vault` com o banco e as credenciais fora do
   cofre.
7. **CLI `daemon` contínuo com o Obsidian fechado:**
   - edição de `.md` e de binário **depois** da partida chega ao banco (o sintoma dos comentários da #847);
   - o que vem do banco desce ao disco;
   - Ctrl+C;
   - queda do CouchDB na partida e no meio.
8. **CLI e pastas com ponto aninhadas no Windows:** criar `projeto/.venv/x.txt` e `projeto/.git/HEAD` antes
   da partida. Ver se a varredura inicial os leva ao banco (suspeita do `split(path.sep)`).
9. **CLI como serviço:** tarefa agendada `ONLOGON` (`schtasks`). O que acontece quando o observador falha ou o
   CouchDB não responde (o processo sai com código 1), e como reiniciar sozinho.
10. **`awaitWriteFinish` de 500 ms:** copiar para o cofre um arquivo de cerca de 40 MB vindo de outra pasta ou
    do OneDrive. Ver se sobe um arquivo pela metade.
11. **CLI e E2EE:** se o hub for usar E2EE, repetir o item 7 com E2EE e ofuscação de caminho (o defeito da
    #835: metadado vazio no remoto).
12. **CLI como dispositivo novo:** precisa de `mark-resolved` ou `unlock-remote`? Ele aceita a configuração
    remota sem avisar (`disableCheckingConfigMismatch`)?
13. **Conflito de texto no CLI:** sem interface, ver se fica aberto (`ls` com `*`) e se o plugin mostra o modal
    ao abrir o Obsidian depois.
14. **Os dois sempre ligados:** uma edição no Obsidian e uma gravação do agente pelo MCP. Contar revisões e
    conflitos por nota (`info` do CLI ou `?revs_info=true`), procurar gravações repetidas no disco e checar se
    entra em ciclo.
15. **Revezamento:** CLI ligado com o Obsidian fechado (edição, apagamento e gravação vinda do banco), depois
    CLI parado e Obsidian aberto, e o inverso. Nada se perde? Aparece conflito falso em arquivo que o outro só
    baixou?
16. **livesync-bridge:** fora do teste, salvo se o Gustavo pedir. Não trata conflito e fixa uma commonlib
    antiga.

## Não verificado

- O efeito exato e o local do "Detect all file extensions" na documentação do próprio Obsidian.
- O tamanho de um pedaço com E2EE; a deduplicação entre versões com E2EE (inferida).
- Que formatos de escritório regravam quase todos os pedaços a cada salvamento (inferido do fato de serem
  comprimidos).
- O LevelDB nativo do CLI no Windows; o reinício automático pelo Agendador de Tarefas; o funcionamento do
  `daemon` no Windows em geral.
- Se o defeito dos comentários da #847 (edição depois da partida não sobe) persiste na 1.0.
- Recuperar pela interface do plugin a versão de binário descartada numa colisão.
- O comportamento do plugin e do CLI juntos na mesma pasta: nenhuma fonte trata disso.
- O `livesync-serverpeer` e o tratamento de conflito da WebApp.
- O quanto o banco local de cada cliente guarda de pedaços com "Fetch chunks on demand" ligado.

## Registro de consultas

- **Árvores completas** (API do GitHub, `git/trees/<ref>?recursive=1`): `vrtmrz/obsidian-livesync@main`,
  `vrtmrz/livesync-commonlib@main`, `vrtmrz/livesync-bridge@main`, `apache/couchdb@3.5.x` e
  `obsidianmd/obsidian-help@master`.
- **Arquivos brutos lidos:**
  - LiveSync: `README.md`, `docs/{settings,tech_info,datastructure,specs_conflict_resolution,specs_garbage_collection,specs_data_compression,troubleshooting,setup_own_server,releases/1.0}.md`,
    `docs/design_docs/intention_of_chunks.md`, `docs/adr/2026_07_feature_maturity_for_1_0.md`,
    `docker/config/livesync.ini`, `src/apps/cli/{README.md,package.json,main.ts,Dockerfile}`,
    `src/apps/cli/commands/runCommand.ts`, `src/apps/cli/managers/*`, `src/apps/cli/adapters/{NodeFileSystemAdapter,NodePathAdapter}.ts`,
    `src/apps/cli/services/NodeServiceHub.ts`, `src/apps/cli/testdeno/{test-daemon,test-daemon-startup}.ts`,
    `src/managers/ObsidianStorageEventManagerAdapter.ts`, `src/serviceFeatures/conflictResolution/*`,
    `src/LiveSyncBaseCore.ts`, `src/apps/webapp/README.md`, `.github/workflows/{cli-e2e,cli-deno-tests,unit-ci}.yml`,
    `package.json` e `package-lock.json` da tag `1.0.35`.
  - Commonlib: `src/string_and_binary/{path,chunks}.ts`, `src/ContentSplitter/*`,
    `src/common/models/setting.const.{defaults,preferred}.ts`, `src/services/base/{VaultService,ConflictService}.ts`,
    `src/managers/{StorageEventManager,ConflictManager}.ts`, `src/serviceModules/ServiceFileHandlerBase.ts`,
    `src/serviceFeatures/targetFilter.ts`, `src/platform/node/{index,storage}.ts`,
    `docs/{storage-events-and-reflection,offline-scanner,conflict-resolution}.md`; tarball npm 0.1.36 (`dist/`).
  - Bridge: `readme.md`, `PeerStorage.ts`, `PeerCouchDB.ts`, `Peer.ts`, `Hub.ts`, `deno.jsonc` e
    `dat/config.sample.json`.
  - CouchDB 3.5.x: `config/{couchdb,http,compaction,replicator}.rst`, `maintenance/compaction.rst`,
    `replication/{protocol,replicator,conflicts}.rst` e `rel/overlay/etc/default.ini`.
  - Outros: `obsidian-api/obsidian.d.ts`; obsidian-help `Accepted file formats.md`, `File explorer.md` e
    `How Obsidian stores data.md`; chokidar `README.md` em `4.0.3`; Node `doc/api/fs.md` (v22.x);
    windowsserverdocs `schtasks-create.md`; RFC 4648.
- **Buscas de issues** (API `search/issues`, só no repositório oficial):
  - `repo:vrtmrz/obsidian-livesync CLI windows`;
  - `… daemon`;
  - `… headless`;
  - `… CLI "same vault"`;
  - `… CLI obsidian simultaneously` (sem resultado);
  - `… CLI binary`;
  - `… "large file"`.
- **Issues lidas na íntegra ou nos últimos comentários:** LiveSync #359, #469, #815, #835, #843, #847, #866,
  #1142, #1143 e #1188; a lista de issues do bridge (30 mais recentes).
