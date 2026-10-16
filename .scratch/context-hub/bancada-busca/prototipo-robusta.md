# Protótipo da Robusta (fase 1): Orama pt + sqlite-vec + RRF, e5-small local

Teste de 2026-10-14, mesma máquina da bancada (Windows 11, Node 24.19, CPU sem GPU). Só dados, sem recomendação.
Pasta de trabalho: `C:\Projetos\bancada-busca\robusta\`. Scripts: `scripts/robusta/` (`lib.mjs`, `indexar-fs.mjs`,
`avaliar.mjs`, `changes.mjs`, `lancar-changes.py`, `yaml-invalido.cjs`). Resultados brutos (top 5 por pergunta, mesmo
formato do `avaliar.py`): `C:\Projetos\bancada-busca\resultados\robusta-*.json`.

## 1. O que foi montado

- **Léxico:** Orama 3.1.18 + `@orama/stemmers/portuguese` 3.1.18 (README do pacote: 30 idiomas, inclui português). BM25 do
  Orama, `threshold: 1` (qualquer termo), lista de palavras vazias pt+en escrita por mim (~70), um documento Orama por
  trecho, resultado agregado por arquivo (melhor trecho). Campo opcional `title` (título + palavras do caminho) com
  peso (`boost`).
- **Vetorial:** `sqlite-vec` 0.1.9 (tabela `vec0`, float[384]) carregado no `better-sqlite3` 12.11.1. **Instalou e rodou
  no Windows sem troca** (o vetor do Orama não foi preciso). Observação: `better-sqlite3` 13.0.3 (a versão mais nova na
  hora) tentou compilar com node-gyp e falhou; a 12.11.1 (a mesma do OHS) vem com binário pronto.
- **Embedding:** `Xenova/multilingual-e5-small` quantizado (`dtype: q8`, o mesmo `model_quantized.onnx` do cache do OHS)
  via `@huggingface/transformers`, prefixos `passage: `/`query: `, média + normalização. Nenhuma chamada ao FreeLLMAPI.
- **Chunking meu:** por cabeçalho (até `####`), trechos de até 1400 caracteres com 200 de sobreposição, mínimo 50;
  cada trecho vai ao embedding com "título | cadeia de cabeçalhos" na frente. Frontmatter removido por regex (não
  rejeita YAML inválido, ao contrário do OHS).
- **Fusão:** RRF, k=60, sobre as listas por arquivo (léxica e vetorial, 50 itens cada).
- **Índice persistido** num arquivo SQLite (`docs`, `chunks`, `vec_chunks`); o índice Orama é reconstruído na memória
  a cada partida (`seg_montar_orama` ~0,2 s para 1862 trechos; não foi persistido).

## 2. Qualidade (hit@5 / MRR, 40 perguntas, mesmas do OHS)

Corpus: os 124 `.md` (sem `rajada/`). O OHS indexou só 112 (12 com YAML inválido). Para igualar o conjunto de candidatos
há linhas "sem os 12" (resultados filtrados: tiro dos resultados os 12 arquivos que o `gray-matter`, parser do OHS,
rejeita; lista em `robusta/yaml-invalido.json`, são 12 de fato). "título +3" = campo título/caminho com peso 3 no Orama.

| Configuração | Total (40) | L (20) | P (20) | pt (36) | en (4) |
|---|---|---|---|---|---|
| **OHS só palavra (bancada)** | 0,725 / 0,504 | 0,950 / 0,804 | 0,500 / 0,203 | 0,750 / 0,532 | 0,500 / 0,250 |
| **OHS híbrida, e5 local (bancada)** | 0,750 / 0,509 | 0,900 / 0,643 | 0,600 / 0,374 | 0,722 / 0,495 | 1,000 / 0,633 |
| **OHS só semântica, e5 (bancada)** | 0,750 / 0,532 | 0,900 / 0,639 | 0,600 / 0,425 | 0,722 / 0,499 | 1,000 / 0,833 |
| Robusta só palavra (Orama pt), 124 arquivos | 0,450 / 0,211 | 0,650 / 0,343 | 0,250 / 0,079 | 0,500 / 0,235 | 0,000 / 0,000 |
| Robusta só vetor (sqlite-vec), 124 | 0,725 / 0,474 | 0,850 / 0,537 | 0,600 / 0,410 | 0,694 / 0,450 | 1,000 / 0,688 |
| Robusta híbrida RRF, 124 | 0,650 / 0,399 | 0,800 / 0,508 | 0,500 / 0,289 | 0,639 / 0,378 | 0,750 / 0,583 |
| Robusta só palavra, 124, título +3 | 0,525 / 0,355 | 0,700 / 0,487 | 0,350 / 0,223 | 0,556 / 0,367 | 0,250 / 0,250 |
| Robusta híbrida, 124, título +3 (índice feito pelo `_changes`) | 0,675 / 0,457 | 0,750 / 0,575 | 0,600 / 0,338 | 0,667 / 0,456 | 0,750 / 0,458 |
| Robusta só palavra, sem os 12 | 0,500 / 0,242 | 0,700 / 0,379 | 0,300 / 0,104 | 0,528 / 0,259 | 0,250 / 0,083 |
| Robusta só vetor, sem os 12 | 0,725 / 0,532 | 0,850 / 0,625 | 0,600 / 0,439 | 0,694 / 0,499 | 1,000 / 0,833 |
| Robusta híbrida, sem os 12 | 0,700 / 0,450 | 0,850 / 0,610 | 0,550 / 0,291 | 0,667 / 0,446 | 1,000 / 0,487 |
| Robusta só palavra, sem os 12, título +3 | 0,525 / 0,388 | 0,700 / 0,512 | 0,350 / 0,263 | 0,556 / 0,403 | 0,250 / 0,250 |
| Robusta híbrida, sem os 12, título +3 | 0,750 / 0,455 | 0,850 / 0,556 | 0,650 / 0,355 | 0,722 / 0,450 | 1,000 / 0,508 |

Leitura dos números (sem recomendação):
- Cada pergunta vale 2,5 pontos de hit@5; as diferenças de 1 a 3 acertos estão no ruído, e o título +3 foi escolhido depois
  de ver resultados (experimentei pesos 0, 2, 3, 4 e `threshold` 1 e 0,5, que não mudou nada; nível de documento inteiro
  em vez de trecho também foi testado: 0,450 / 0,240 sem peso e 0,575 / 0,371 com peso 3, só palavra). Não houve conjunto
  separado para afinar: as 40 perguntas serviram de ajuste e de medida.
- **A parte léxica do Robusta ficou abaixo do BM25 do OHS** (0,45 a 0,53 contra 0,725, nas perguntas L 0,65 a 0,70 contra
  0,95). Causa **não investigada**. Diferenças conhecidas que podem pesar (hipóteses, não verificadas): Orama usa OR com
  BM25 por trecho e minha lista de palavras vazias; o OHS usa SQLite FTS5 (documentação do OHS: BM25), com tokenização e
  campos que não li; o stemmer pt do Orama se aplica também às 4 perguntas em inglês (en 0,0 a 0,25 na parte léxica).
- A parte vetorial do Robusta, com o mesmo e5-small, ficou igual ao OHS em hit@5 (0,725 contra 0,750) e abaixo em MRR com 124
  arquivos (0,474 contra 0,532); sem os 12 arquivos o MRR é 0,532, igual. Chunking e agregação são diferentes dos do OHS.
- Perguntas que nenhuma configuração do Robusta acerta não foram listadas; estão nos JSON.

## 3. Tempo e memória

| Medida | Valor |
|---|---|
| Indexação total, 124 `.md` do disco, 1862 trechos (carregar modelo 3,5 s incluído) | 347,5 s (344 s indexando); pico de RSS 1859 MB (árvore de processos, `run_rss.py`) |
| Indexação total pelo `_changes` (mesmo corpus, 2ª execução da máquina) | 233,9 s (`_changes` 0,75 s, montar texto 4,3 s, chunk+embedding+gravação 227,9 s); pico 1718 MB |
| Referência da bancada, OHS | 116 s (1933 trechos), pico 767 MB |
| Tamanho do `indice.db` | não medido |
| Consulta (40 perguntas, processo aquecido, modelo já carregado) | só palavra 0,13 a 0,18 s; só vetor 0,4 a 0,5 s; híbrida 0,5 a 0,7 s (para as 40 juntas) |
| Montar o Orama a partir do SQLite | ~0,2 s por 1862 trechos (valor guardado em `seg_montar_orama` nos JSON) |

O tempo do mesmo trabalho variou de 347 s para 234 s entre as duas execuções (máquina compartilhada, ruído). O embedding
roda um lote de 16 trechos por vez, no processo principal do Node, sem paralelismo e sem ordenar por tamanho; não otimizado.
O pico de RSS acima de 1,7 GB é o do Node com onnxruntime e lotes de até 512 tokens; a causa exata não foi investigada.
O RSS foi medido para o processo todo, não separado por componente.

## 4. Alimentação pelo `_changes` do CouchDB

Ambiente: o CouchDB do spike (`docker compose up -d couchdb`; o contêiner do MCP não foi subido), 127.0.0.1:5984. Nenhuma
credencial foi lida ou impressa por mim: o consumidor recebe a autenticação por variável de ambiente, posta pelo
`lancar-changes.py`, que a pega do `cdb.py` do próprio spike.

**Banco sem E2EE, corpus real.** Criei o banco `bancada` e o populei com o CLI do LiveSync (`daemon --vault`) a partir de
uma cópia dos 124 `.md`: 4620 documentos (124 notas + chunks `h:`; o CLI quebra em trechos pequenos), pronto em menos de 60 s.
`changes.mjs` lê `GET /bancada/_changes?include_docs=true&since=0`, monta o texto de cada nota juntando o campo `data` dos
`children` (em `_all_docs` por lote; usa `eden` quando existe), ignora o que não termina em `.md` e o que não é `plain`,
trata `deleted` e grava o `last_seq` num arquivo.
- Reindexação total pelo `_changes`: **233,9 s, 124 notas indexadas**, 1 linha ignorada (não `.md`), 0 erros. Os 4620
  documentos vieram em **0,75 s**; montar o texto das 124 notas levou 4,3 s no total. O resto (228 s) é o embedding.
- A busca sobre esse índice está na linha "índice feito pelo `_changes`" (título +3). Só vetor deu os mesmos 0,725 / 0,474
  do índice do disco; a híbrida difere (0,675 / 0,457 contra 0,650 / 0,477 do disco com peso 4) porque são pesos de título
  diferentes; não rodei o disco com peso 3 na mesma base de 124 arquivos. O texto montado do CouchDB e o do disco são o mesmo
  (o `diff` foi feito só no caso E2EE; no caso sem E2EE não comparei byte a byte).
- **Incremental:** editei um arquivo na pasta do cofre; o CLI o levou ao CouchDB (rev 1 para 2) e uma nova passada de
  `changes.mjs` (com `since` guardado) leu 2 linhas, reindexou 1 nota em **1,4 s no total** (0,4 s de embedding); o texto
  novo ficou no índice (consulta direta ao SQLite).
- Conflitos: o consumidor lê só a revisão vencedora do CouchDB (sem `conflicts=true`). Não testado com conflito.
- Não testado: `feed=continuous`/`longpoll` (rodei só passadas sob demanda), arquivos binários e anexos, notas grandes
  (>1 MB), arquivo `.md` renomeado/movido (o `_changes` mostra como exclusão + criação; não exercitei), pasta com ponto.

**Banco com E2EE.** Criei o banco `bancada-e2ee` com `encrypt: true`, uma passphrase de teste minha e `usePathObfuscation: true`.
Confirmei no CouchDB que os caminhos e o `data` dos chunks são cifrados (`%=...`). O texto **não** é lido pelo meu consumidor
nesse banco (não implementei a decifragem: a leitura passaria pelo `livesync-commonlib`, o que não tentei). Caminho
usado: um segundo CLI com a mesma configuração, banco local novo: `sync` (36,7 s para baixar o banco cifrado) e
`mirror <pasta>` (10,9 s para decifrar e gravar 124 `.md`), com `diff -rq` **idêntico** ao original. Ou seja, "CLI do
LiveSync como decifrador" funciona (~48 s por reindexação total, fora o embedding), mas isso é leitura do disco
depois de um espelho, não leitura direta do `_changes`. A leitura do `_changes` decifrando dentro do Node (no MCP do
es617, que decifra para ler) **não foi feita**; o código do MCP do es617 não foi lido por mim nesta fase (não verificado).

## 5. Desvios do pedido

- **Tecnologia:** não houve troca (sqlite-vec instalou e rodou); `better-sqlite3` foi fixado em 12.11.1 pelo motivo acima.
- **Chunking e títulos são meus**, não os do OHS; a comparação de qualidade mistura motor e chunking. O peso do título é um
  ajuste meu, escolhido sobre as mesmas 40 perguntas (veja a ressalva da seção 2).
- **Lista de palavras vazias** pt+en escrita por mim, não verificada em fonte.
- **E2EE:** não lido direto do `_changes`; lido por espelho pelo CLI (seção 4).
- **Memória:** medi o pico do processo Node inteiro (embedding incluído); a bancada mediu a árvore de processos do OHS, o
  que é comparável, mas o OHS mede um modelo cuja carga pode ter sido em outro momento.
- Corpus com `rajada/` e arquivo `.db` do OHS na pasta ficaram de fora (não eram `.md` da bancada).
- Estado deixado: o contêiner do CouchDB do spike foi parado; os dois daemons do CLI foram mortos. Os bancos `bancada` e
  `bancada-e2ee` continuam no volume do CouchDB do spike (dados de teste meus, sem dado de cliente); o banco `obsidian`
  do spike não foi alterado por mim (só lido pelo `cdb.py ls`). Nada em `laco-embeddings/` nem no portal.

## 6. Para a fase 2 (trocar o embedding pela lista curta)

- O modelo é parâmetro: `ROBUSTA_MODEL` e `ROBUSTA_DIM` em `lib.mjs`; `indexDoc` e `searchVec` aceitam uma função
  `embedFn(textos, 'passage'|'query')`, onde se encaixa uma chamada ao FreeLLMAPI ou outro modelo local. Cada modelo precisa de
  um `ROBUSTA_DB` próprio (a dimensão do `vec0` é fixa na criação da tabela) e do prefixo certo (`isE5` só liga
  `query:`/`passage:` para e5).
- Reindexar: `node indexar-fs.mjs` (disco) ou `lancar-changes.py bancada --fresh` (CouchDB); avaliar: `node avaliar.mjs <rótulo>`
  (variáveis `LEX_TITLE_BOOST`, `EXCLUI_YAML=1`, `ROBUSTA_DB`).
- A parte léxica fica igual entre modelos; a diferença esperada está na linha "só vetor" e na híbrida.
- Em aberto antes da comparação final: por que a parte léxica do Orama ficou abaixo do FTS5 do OHS (se for decidida a
  comparar léxico), medição do tamanho do `indice.db`, medição da rajada de 200 arquivos (não feita nesta fase), decifragem
  direta do E2EE no Node, e a repetição das medidas (nenhuma foi repetida além das duas indexações acima).
- Cota do FreeLLMAPI: nada foi gasto.
