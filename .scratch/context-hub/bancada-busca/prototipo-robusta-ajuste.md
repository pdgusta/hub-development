# Protótipo da Robusta, ajuste antes da fase 2: FTS5 no léxico e E2EE decifrado no consumidor

Teste de 2026-10-14 (noite), mesma máquina e mesmo corpus da fase 1 (`prototipo-robusta.md`). Pedido: rodada 9 do ticket 09.
Só dados, sem recomendação. Nenhuma chamada ao FreeLLMAPI (só o e5-small local); nada de dado de cliente.
Scripts alterados ou novos em `scripts/robusta/`: `lib.mjs` (FTS5), `avaliar.mjs` (`LEX_ENGINE=fts5`), `changes.mjs`
(reescrito com `--e2ee`, `--dump`, `--no-embed`, `--wait`), `lancar-changes.py` (passa a passphrase de teste), `fts-preencher.mjs`
(novo). Resultados brutos: `C:\Projetos\bancada-busca\resultados\robusta-fts5-*.json`.

## 1. Busca por palavra com FTS5

### Como o OHS usa a FTS5 (fonte: código do pacote instalado na bancada, `obsidian-hybrid-search` 0.16.2)

- `C:\Projetos\bancada-busca\ohs\node_modules\obsidian-hybrid-search\dist\src\db.js`, `runMigrations` (linhas 319 a 371):
  `CREATE VIRTUAL TABLE notes_fts_bm25 USING fts5(title, aliases, content, content='notes', content_rowid='id',
  tokenize = "unicode61 tokenchars '+#'")`. Um registro **por nota** (não por trecho). Há uma segunda tabela
  `notes_fts_fuzzy` (`trigram`, só título e aliases) usada para casar título aproximado.
- `dist/src/searcher.js`, `searchBm25` (linhas 135 a 166): `bm25(notes_fts_bm25, 10.0, 5.0, 1.0)` (pesos título 10,
  aliases 5, conteúdo 1); a consulta passa por `sanitizeFtsQuery` (tira `"*^()`) e `toFtsQuery(query, 'OR')`: cada palavra
  vira `"palavra"*` (prefixo), unidas por `OR`. Sem lista de palavras vazias, sem stemmer.
- `dist/src/indexer.js` (linhas 142 a 153): `title` = `title` do frontmatter (gray-matter) ou o nome do arquivo sem `.md`;
  `content` = corpo sem o frontmatter; `aliases` do frontmatter.
- Na híbrida o OHS funde quatro listas: `rrfFusion([vector, bm25, exactAlias, partialFuzzy], 60, [1.5, 1.5, 2.0, 0.25])`
  (`searcher.js`, linha 1360).

### O que montei (decidido antes de medir; uma medição por configuração, sem afinar)

- Tabela `fts_docs(path UNINDEXED, title, aliases, content)` no mesmo `indice.db` do sqlite-vec, um registro por nota,
  `tokenize = "unicode61 remove_diacritics 2 tokenchars '+#'"`, `bm25(fts_docs, 0, 10, 5, 1)`, consulta igual à do OHS
  (`"palavra"*` com OR). Título: frontmatter (gray-matter), senão linha `title:` por regex (para os 12 YAML inválidos, que o
  OHS descarta e eu mantenho), senão nome do arquivo. Gravada dentro da mesma transação de `indexDoc`; `deleteDoc` apaga.
- Diferença minha em relação ao OHS: `remove_diacritics 2` em vez do padrão. Conferi só pelo comportamento (teste em memória,
  SQLite 3.53.2 do `better-sqlite3` 12.11.1): `"decisao"*` casa "decisão" com 1 e com 2; a documentação do SQLite sobre a
  diferença entre 1 e 2 **não foi lida nesta rodada** (não verificado).
- **Não copiei** a lista de título aproximado (`trigram`) nem os pesos 1,5/1,5/2,0/0,25 da fusão do OHS: a híbrida aqui é a
  mesma RRF da fase 1 (k=60, duas listas, pesos iguais).
- O Orama continua selecionável (padrão sem `LEX_ENGINE`); com `LEX_ENGINE=fts5` o `avaliar.mjs` nem monta o Orama.
- O índice do disco da fase 1 foi copiado para `indice-fase1.db` e o `indice.db` recebeu só a tabela FTS
  (`fts-preencher.mjs`, sem refazer embedding). O índice feito pelo `_changes` cifrado (seção 2) já nasce com a FTS.

### Qualidade (hit@5 / MRR, as mesmas 40 perguntas)

| Configuração | Total (40) | L (20) | P (20) | pt (36) | en (4) |
|---|---|---|---|---|---|
| **OHS só palavra (bancada)** | 0,725 / 0,504 | 0,950 / 0,804 | 0,500 / 0,203 | 0,750 / 0,532 | 0,500 / 0,250 |
| **OHS híbrida, e5 local (bancada)** | 0,750 / 0,509 | 0,900 / 0,643 | 0,600 / 0,374 | 0,722 / 0,495 | 1,000 / 0,633 |
| Antes: só palavra Orama, 124 | 0,450 / 0,211 | 0,650 / 0,343 | 0,250 / 0,079 | 0,500 / 0,235 | 0,000 / 0,000 |
| Antes: só palavra Orama, 124, título +3 | 0,525 / 0,355 | 0,700 / 0,487 | 0,350 / 0,223 | 0,556 / 0,367 | 0,250 / 0,250 |
| **Depois: só palavra FTS5, 124** | **0,700 / 0,449** | 0,950 / 0,713 | 0,450 / 0,185 | 0,722 / 0,475 | 0,500 / 0,208 |
| Antes: só palavra Orama, sem os 12 | 0,500 / 0,242 | 0,700 / 0,379 | 0,300 / 0,104 | 0,528 / 0,259 | 0,250 / 0,083 |
| Antes: só palavra Orama, sem os 12, título +3 | 0,525 / 0,388 | 0,700 / 0,512 | 0,350 / 0,263 | 0,556 / 0,403 | 0,250 / 0,250 |
| **Depois: só palavra FTS5, sem os 12** | **0,700 / 0,495** | 0,950 / 0,796 | 0,450 / 0,193 | 0,722 / 0,522 | 0,500 / 0,250 |
| Só vetor (inalterado), 124 | 0,725 / 0,474 | 0,850 / 0,537 | 0,600 / 0,410 | 0,694 / 0,450 | 1,000 / 0,688 |
| Só vetor (inalterado), sem os 12 | 0,725 / 0,532 | 0,850 / 0,625 | 0,600 / 0,439 | 0,694 / 0,499 | 1,000 / 0,833 |
| Antes: híbrida Orama, 124 | 0,650 / 0,399 | 0,800 / 0,508 | 0,500 / 0,289 | 0,639 / 0,378 | 0,750 / 0,583 |
| Antes: híbrida Orama, 124, título +3 (índice `_changes`) | 0,675 / 0,457 | 0,750 / 0,575 | 0,600 / 0,338 | 0,667 / 0,456 | 0,750 / 0,458 |
| **Depois: híbrida FTS5 + vetor, 124** | **0,625 / 0,444** | 0,850 / 0,633 | 0,400 / 0,254 | 0,639 / 0,470 | 0,500 / 0,208 |
| Antes: híbrida Orama, sem os 12 | 0,700 / 0,450 | 0,850 / 0,610 | 0,550 / 0,291 | 0,667 / 0,446 | 1,000 / 0,487 |
| Antes: híbrida Orama, sem os 12, título +3 | 0,750 / 0,455 | 0,850 / 0,556 | 0,650 / 0,355 | 0,722 / 0,450 | 1,000 / 0,508 |
| **Depois: híbrida FTS5 + vetor, sem os 12** | **0,700 / 0,495** | 0,900 / 0,727 | 0,500 / 0,264 | 0,667 / 0,510 | 1,000 / 0,362 |
| Índice feito pelo `_changes` cifrado (seção 2), FTS5, 124 | só palavra, só vetor e híbrida idênticos às três linhas "124" acima | | | | |

Leitura dos números (sem recomendação):
- A FTS5 com o desenho do OHS levou o só palavra de 0,45 a 0,53 para **0,700** (L 0,95, igual ao OHS). Sem os 12, 0,700 / 0,495
  contra 0,725 / 0,504 do OHS: um acerto de diferença em hit@5 (cada pergunta vale 0,025), dentro do ruído.
- A híbrida RRF (pesos iguais, sem a lista de título aproximado) ficou **abaixo** da FTS5 sozinha com 124 arquivos (0,625 contra
  0,700) e igual a ela sem os 12 (0,700). A perda está nas perguntas P (0,45 a 0,40 com 124). Causa não investigada; a fusão do OHS
  é diferente (quatro listas, pesos 1,5/1,5/2,0/0,25), e não a reproduzi.
- Nada foi afinado: uma medida por configuração; os pesos 10/5/1 e o OR com prefixo vêm do OHS, o `remove_diacritics 2` foi
  decidido antes de medir. As 40 perguntas continuam sendo a única base (não há conjunto separado).

### Tempo e tamanho da parte léxica

| Medida | Valor |
|---|---|
| Preencher a FTS5 dos 124 arquivos a partir do disco (gray-matter incluído) | 0,38 s |
| 40 consultas só palavra, FTS5 | 0,48 a 0,49 s (Orama na fase 1: 0,13 a 0,18 s) |
| 40 consultas híbridas, FTS5 + vetor (modelo carregado) | 1,1 a 1,2 s (fase 1 com Orama: 0,5 a 0,7 s; máquina compartilhada, uma medida) |
| Montar o Orama na partida | não se aplica com FTS5 (persistida no SQLite); era ~0,2 s |
| `indice.db` sem FTS5 / com FTS5 | 6,37 MB / 9,20 MB (`fts_docs_content` 1,80 MB, porque guarda uma cópia do texto; `fts_docs_data` 0,84 MB) |

## 2. E2EE decifrado direto no consumidor do `_changes`

### Fonte lida

O código do MCP do es617 **não está na máquina** (só o README em `C:\Projetos\spike-livesync\docs\es617_obsidian-sync-mcp_main_README.md`,
que diz: "reads from CouchDB directly using livesync-commonlib ... for proper chunk handling and E2E encryption support").
Segui, portanto, a `@vrtmrz/livesync-commonlib` 0.1.36 que está em `C:\Projetos\spike-livesync\livesync-src\node_modules\`:
- `dist/pouchdb/encryption.js`, `outgoingDecryptHKDF`: chunk com `data` começando por `%=` → `decryptHKDF(data, passphrase, salt)`;
  meta com `path` começando por `/\:` (`ENCRYPTED_META_PREFIX`) → `decryptMetaWithHKDF` → JSON `{path, mtime, ctime, size, children}`
  copiado para o documento; eden cifrado em `eden["h:++encrypted-hkdf"].data` → JSON com os chunks embutidos.
- `dist/replication/SyncParamsHandler.js`: o sal PBKDF2 é `pbkdf2salt` (base64) do documento `_local/obsidian_livesync_sync_parameters`
  (`dist/common/models/sync.definition.js`, `DOCID_SYNC_PARAMETERS`); `getPBKDF2Salt` devolve o `Uint8Array` decodificado.
- `dist/worker/bgWorker.direct.js`: `decryptHKDFWorker` chama `decrypt` de `octagonal-wheels/encryption/hkdf` (0.1.54), que é o
  que o `changes.mjs` importa direto (`dist/encryption/hkdf.js`, `decrypt(input, passphrase, pbkdf2Salt)`, exige o prefixo `%=`).
- Configuração do banco de teste (lida do `settings.json` do CLI de teste, só as chaves não secretas): `encrypt: true`,
  `E2EEAlgorithm: "v2"`, `usePathObfuscation: true`, `enableCompression: false`, `useDynamicIterationCount: false`.

### Como ficou

`lancar-changes.py bancada-e2ee --e2ee` lê só a chave `passphrase` do `settings.json` do CLI de teste (`robusta\cli-e2ee\.livesync\`,
a mesma que o subagente da fase 1 definiu) e a passa por variável de ambiente; não foi impressa (imprimi só o comprimento, 18). A
autenticação do CouchDB segue pelo `cdb.py`. O `changes.mjs` busca o sal, decifra meta, eden e chunks (estes vêm do próprio feed;
o que faltar vai por `_all_docs`), monta o texto e indexa. Uma tabela `ids(id, path)` guarda o caminho de cada `_id` ofuscado, para
tratar lápide (`_deleted`) que não traz caminho. Com `--wait N` fica em `feed=longpoll` até indexar ao menos uma nota.

### Medidas

| Medida | Valor |
|---|---|
| Passada só de decifragem (sem embedding), 4620 linhas do `_changes` | 3,0 s no total: `_changes` 1,07 s, montar texto 1,37 s (dos quais decifrar 1,34 s); 2ª passada: 1,25 / 1,46 / 1,43 s |
| **Reindexação total pelo `_changes` cifrado, com embedding** | **277,4 s** (relógio, `run_rss.py`); 124 notas, 1 ignorada (não `.md`), 0 erros; `_changes` 1,34 s, montar 11,46 s (decifrar 11,4 s), chunk+embedding+gravação 262 s, carregar modelo 1,5 s |
| Pico de RSS dessa reindexação | 1725 MB (árvore de processos) |
| Referência: reindexação pelo `_changes` sem E2EE (fase 1) | 233,9 s, pico 1718 MB |
| **Edição até entrar no índice** | **2,1 s** (de acrescentar uma linha no arquivo do cofre, com o CLI do LiveSync em `daemon`, até o consumidor em longpoll gravar a nota: 2112 ms); dentro disso, decifrar 0,1 s e embedding 1,2 s |

- A decifragem levou 1,3 s sozinha e 11,4 s quando intercalada com o embedding (mesmas 124 notas); a diferença é atribuída por mim à
  disputa de CPU com o onnxruntime, **não investigada**. O total é dominado pelo embedding (262 de 277 s).
- O `seg_ler_changes` da passada de edição (11,4 s) é a espera do longpoll antes da edição, não custo de leitura.

### Conferência do texto (diff)

- O texto decifrado de **124 de 124** notas é idêntico byte a byte à pasta do cofre de teste (`diff -rq vault-e2ee dump-e2ee2`:
  só aparece `.livesync-snapshot.json`, arquivo do CLI). Contra o corpus original, 123 idênticas; a 124ª
  (`issues/01-licoes-do-vault.md`) difere só pelas linhas de marcador acrescentadas nos testes de edição (fase 1 e esta).
- Depois da edição: a nota nova foi achada na FTS5 (`"quokka"*`, 1 nota) e nos trechos (1 trecho), e o despejo cifrado→texto feito
  depois continuou idêntico ao cofre.
- A busca sobre o índice feito pelo `_changes` cifrado deu os mesmos números do índice do disco (última linha da tabela da seção 1).

## 3. Desvios do pedido

- **MCP do es617:** o código dele não foi lido (não está na máquina); a decifragem segue a `livesync-commonlib`, que o README do es617
  diz usar. Que o es617 chame exatamente essas funções é **não verificado**.
- **Fusão híbrida** não reproduz a do OHS (sem lista de título aproximado, pesos iguais); só a parte léxica seguiu o OHS.
- `remove_diacritics 2` diverge do OHS (escolha minha, antes de medir).
- O `changes.mjs` foi reescrito (o modo sem E2EE segue igual na lógica, mas passou a usar os chunks que vêm no próprio feed antes do
  `_all_docs`; o modo sem E2EE **não foi rodado de novo** nesta rodada).
- A passphrase de teste é lida do `settings.json` do CLI de teste, que também guarda a senha do CouchDB; o lançador lê só a chave
  `passphrase`, e só nomes de chaves não secretas e o comprimento da passphrase foram impressos.
- Estado deixado: subi o contêiner `spike-livesync-couchdb-1` e o parei no fim; o daemon do CLI que abri foi encerrado pelo PID; o
  consumidor terminou sozinho. O banco `obsidian` não foi tocado. O cofre de teste `vault-e2ee` e o banco `bancada-e2ee` ficaram com
  a linha de marcador desta rodada (`marcador-ajuste-fts5-quokka`). Arquivos novos em `C:\Projetos\bancada-busca\robusta\`:
  `indice-fase1.db` (cópia de antes), `indice-e2ee.db`(+`.seq`), `dump-e2ee2\` (texto decifrado), `e2ee.log`, `e2ee.rss.txt`,
  `edicao.log`, `edicao.ts`, `logs\cli-e2ee-aj.*`. Nada em `laco-embeddings/`, `laco/` nem `portal/`.

## 4. Não verificado

- Por que a híbrida RRF ficou abaixo da FTS5 sozinha com 124 arquivos.
- Diferença entre `remove_diacritics` 1 e 2 na documentação do SQLite (só o teste de comportamento acima).
- Caminhos de E2EE que o banco de teste não exercita e que o código não trata: cifra V1 (`%` sem `=`, `tryDecryptV1AsFallback`),
  eden V1 (`h:++encrypted`), caminho ofuscado sem HKDF, compressão (`enableCompression`), arquivos binários (tipo diferente de
  `plain`), conflitos, metadados internos cifrados. Exclusão (por `deleted` e por lápide com a tabela `ids`) está no código e **não
  foi exercitada**; renomear também não.
- Repetição das medidas: cada tempo foi medido uma vez (a decifragem sozinha, duas).
- `feed=continuous`: só o longpoll de uma passada foi testado, não um consumidor que fique de pé.

## 5. O que muda para a fase 2 (trocar o embedding pelos modelos da lista curta)

- A parte léxica (FTS5) é a mesma para todos os modelos; a diferença entre modelos fica nas linhas "só vetor" e híbrida. Avaliar com
  `LEX_ENGINE=fts5 node avaliar.mjs <rótulo>` (e `EXCLUI_YAML=1` para "sem os 12").
- Reindexar cada modelo pelo banco cifrado: `ROBUSTA_DB=<arquivo do modelo> ROBUSTA_MODEL=... ROBUSTA_DIM=... python lancar-changes.py
  bancada-e2ee --fresh --e2ee` (a FTS5 nasce junto). Um índice feito pelo disco antes desta rodada ganha a FTS5 com `fts-preencher.mjs`.
- A decifragem custa ~1,3 s por reindexação total sozinha; o tempo de cada modelo é praticamente o do embedding (262 s com o e5-small).
- `embedFn` continua sendo o ponto de troca (`indexDoc`, `searchVec`); o prefixo `query:`/`passage:` só liga para e5.
- Se a fusão for comparada entre modelos, ela segue com dois sinais e pesos iguais; a do OHS (com título aproximado e pesos) não foi
  implementada.
- Cota do FreeLLMAPI: nada foi gasto nesta rodada.
