# Bancada da camada de busca: obsidian-hybrid-search (OHS) × memtomem

Teste de 2026-10-14, Windows 11 nativo, Node 24.19, Python 3.12.10 (venv), CPU sem GPU. Corpus: cópia de
`issues/`, `exploracao/` (com `anexos/`) e `armis-docs/`, em
`C:\Projetos\bancada-busca\corpus\` (124 `.md`, 150 arquivos no total, 2,9 MB). 40 perguntas
(20 L, 20 P; 36 pt, 4 en). Só dados, sem recomendação. Scripts em `scripts/`; resultados brutos em
`resultados.json` (top 5 por pergunta e configuração).

## 1. Resumo

**Nenhuma configuração com o gateway foi medida:** o FreeLLMAPI devolveu 429 na primeira chamada de
`bge-m3` e de `embeddinggemma-300m` ("you have used up your daily free allocation of 10,000 neurons",
Cloudflare). Regra do teste cumprida: parei de usar os dois modelos. As quatro combinações (OHS e memtomem ×
dois modelos) ficam **não verificadas**.

Qualidade (hit@5 / MRR; n entre parênteses; o MRR conta a posição do primeiro arquivo certo, 0 se fora do top 5):

| Configuração | Total (40) | L (20) | P (20) | pt (36) | en (4) |
|---|---|---|---|---|---|
| OHS só palavra (`--mode fulltext`, BM25) | 0,725 / 0,504 | 0,950 / 0,804 | 0,500 / 0,203 | 0,750 / 0,532 | 0,500 / 0,250 |
| OHS híbrida, e5-small local | 0,750 / 0,509 | 0,900 / 0,643 | 0,600 / 0,374 | 0,722 / 0,495 | 1,000 / 0,633 |
| OHS só semântica, e5-small local (extra) | 0,750 / 0,532 | 0,900 / 0,639 | 0,600 / 0,425 | 0,722 / 0,499 | 1,000 / 0,833 |
| memtomem só BM25 (provider none) | 0,675 / 0,439 | 0,900 / 0,627 | 0,450 / 0,252 | 0,694 / 0,446 | 0,500 / 0,375 |
| memtomem híbrida, e5-small ONNX | 0,800 / 0,491 | 0,950 / 0,613 | 0,650 / 0,370 | 0,778 / 0,503 | 1,000 / 0,383 |
| OHS / memtomem com `embeddinggemma-300m` e `bge-m3` (gateway) | não medido (429) | | | | |

Observações de leitura: com 40 perguntas, uma pergunta vale 2,5 pontos de hit@5; as diferenças entre as
linhas (um a três acertos) estão dentro do ruído. Só 4 perguntas em inglês (um acerto vale 25 pontos).
Outros números: indexação completa local OHS 1 min 56 s (112 notas, 1933 trechos); memtomem BM25 15 s
(1058 trechos); memtomem e5 12 min 28 s (2229 trechos). Pico de memória na indexação: OHS 767 MB,
memtomem BM25 117 MB, memtomem e5 1242 MB. Rajada de 200 arquivos: OHS tudo achável em ≤ 147 s (medição
com sondagem); memtomem 186 s até indexar os 200 (2ª rodada).

## 2. Instalação

Tudo dentro de `C:\Projetos\bancada-busca\`, sem instalação global.

**OHS** (README: `npm install -g obsidian-hybrid-search`; usei `npm install` local em `ohs\`):
- `npm init -y && npm install obsidian-hybrid-search`: 57 s. Aviso do npm 11 sobre scripts de instalação
  não aprovados (`better-sqlite3`, `onnxruntime-node`, `protobufjs`); mesmo assim `better_sqlite3.node`
  estava presente e tudo rodou, sem rodar `npm approve-scripts`.
- Binário em `node_modules\.bin\ohs.cmd`. O cofre vem de `OBSIDIAN_VAULT_PATH` (o corpus não tem `.obsidian/`,
  então a detecção automática não vale).
- **Diferente do documentado:** `--db <caminho>` não move o banco; ele foi gravado em
  `corpus\.obsidian-hybrid-search.db` (raiz da pasta indexada) apesar de eu passar outro caminho. O banco
  fica, portanto, dentro do corpus (arquivo `.db`, não entra como nota).
- `ohs reindex` (primeira vez, inclui o download de ~117 MB do modelo): 1 min 56 s. **12 arquivos de
  `exploracao/anexos/` não foram indexados** (contados como "12 errors"): frontmatter YAML inválido
  (`title: ... — ...: ...`, dois-pontos sem aspas). Nenhum deles é resposta de pergunta, mas podem ser
  distratores que o OHS não vê. `ohs status` diz `total: 112` contra 124 `.md`.
- Busca: `ohs search --json --limit 5 --mode fulltext|hybrid|semantic`. Cada chamada CLI custa 1 a 3 s.
  Retorna uma nota por resultado (sem trechos repetidos). O modo `fulltext` isola o BM25.
- Remoto (`OPENAI_BASE_URL`, `OPENAI_EMBEDDING_MODEL`): **não verificado** (cota do gateway).

**memtomem** 0.6.8 (README: `uv tool install 'memtomem[all]'`; usei `uv venv mm` + `uv pip install
'memtomem[all]'` em vez de `uv tool`):
- Instalação 56 s (Python 3.12 do venv).
- **Só com variáveis `MEMTOMEM_*` não funciona:** `mm status` diz "memtomem is not configured. Run 'mm init'".
  Foi preciso `mm init --non-interactive --preset ... --memory-dir ... --db-path ... --mcp skip`.
- `mm init` grava em `~/.memtomem`. Para não tocar o perfil do Gustavo, apontei `USERPROFILE` e `HOME` para
  `bancada-busca\mmhome\`. Efeito colateral: o `memtomem-server` falhou com `SHGetKnownFolderPath(LocalAppData)
  failed` até eu criar `mmhome\AppData\Local\Temp`.
- Uma variável `MEMTOMEM_INDEXING__MEMORY_DIRS` que eu pus em JSON quebrou o `mm init` com erro de parsing
  do pydantic (causa não investigada; usei o `config.json` gerado pelo init).
- O preset `english` liga um **reranker** (`Xenova/ms-marco-MiniLM-L-6-v2`) e namespaces automáticos.
  Desliguei o reranker (`rerank.enabled=false`) para comparar só busca; a medição com reranker **não foi feita**.
  O preset `minimal` (BM25) não baixa nada.
- `mm index <corpus>` indexa mais que `.md`: 141 arquivos (inclui `.json` e `.py` do corpus). 2 arquivos
  bloqueados pela trava de segredos (`2026-10-02-magpie-vs-freellmapi.md`, `pesquisa-26-montagem.md`); o comando
  sai com código 1 por isso. Contornos documentados: `--force-unsafe` ou `redaction: documents-patterns`
  (não usados).
- Busca: `mm search "..." --format json -k 30` devolve trechos (chunks); contei o arquivo do trecho, sem
  repetir. Cada chamada carrega o modelo ONNX (~5 s com e5).
- Uma chamada `mm search` travou mais de 8 min (CPU parada) logo depois de eu matar um servidor de teste; matei
  o processo e as buscas voltaram a 6 s. Causa não identificada (suspeita de trava no banco; **não verificado**).
- Remoto (`MEMTOMEM_EMBEDDING__BASE_URL`, provider openai): **não verificado** (cota).

## 3. Rajada (200 `.md` copiados de uma vez com a ferramenta vigiando, embedding local)

Arquivos: cópias de 6 KB dos tickets, cada um com `marcadorrajadaNNNN` (um token só, por causa do FTS5).

| | OHS (`ohs serve --foreground`) | memtomem (`memtomem-server`, stdio com cliente MCP) |
|---|---|---|
| Cópia dos 200 | 6,4 s | 0,3 s |
| Primeiro marcador achável | 33 s | 67 s (1ª rodada) |
| Todos os 200 | ≤ 147 s (3 sondas em 86 s; os 200 confirmados em 147 s) | 186 s (DB tinha 200 arquivos; 200/200 achados na busca depois) |
| Resultado | 200/200 achados | 1ª rodada: 111/200 em 300 s; 2ª rodada (sem sondar durante): 200/200 |

Ressalvas: o OHS foi medido sondando por busca CLI (que também gasta CPU), então 86 s e 147 s têm folga
para cima. Na 1ª rodada do memtomem, a sondagem com `mm search` (que recarrega o modelo a cada chamada)
competiu com o indexador; na 2ª, contei por SQLite somente leitura. Na 2ª rodada, as marcas de 1, 50 e 100
arquivos não valem (restavam 111 linhas da rodada anterior no banco); valem as de 150 (74 s) e 200 (186 s).
**O watcher do memtomem não indexou nada em 300 s quando o `memtomem-server` ficou de pé em stdio sem cliente
MCP**: só começou depois de um `initialize` e uma chamada `mem_status` de um cliente MCP de verdade. O
OHS não precisa de cliente.

## 4. Memória (pico de RSS somado da árvore de processos)

| Situação | OHS | memtomem |
|---|---|---|
| Indexação completa, só palavra | não aplicável (o `reindex` sempre embute) | 117 MB (BM25) |
| Indexação completa, e5 local | 767 MB | 1242 MB |
| Servidor vigiando, ocioso (45 s) | 96 a 118 MB | 372 MB (modelo carregado) |
| Durante a rajada | 880 MB | 1214 a 1226 MB |

O RSS ocioso do OHS foi medido sem nenhuma consulta (modelo provavelmente ainda não carregado); o do
memtomem foi medido depois de `mem_status`. Não comparável em igualdade.

## 5. Arquivo com ponto e o LiveSync

Ambiente: `C:\Projetos\spike-livesync` (CouchDB 3.5 do docker-compose, cofre `cofre-c`, só o CLI do commit
`14141446`, comando `node livesync-src\src\apps\cli\dist\index.cjs cli-db --vault cofre-c daemon`). Arquivos
novos de teste na raiz do `cofre-c`, 300 e 400 KB de bytes aleatórios:

| Arquivo na raiz do cofre | Caso | Foi ao banco? |
|---|---|---|
| `.obsidian-hybrid-search.db` | já existia ao ligar o CLI (varredura de partida) | **não** |
| `.teste54-ponto-raiz.txt` (controle) | idem | **não** |
| `teste54-normal-partida.txt` (controle) | idem | sim |
| `.obsidian-hybrid-search.db` | apagado e recriado com o CLI rodando | **não** |
| `.teste54-ponto-ligado.txt` (controle) | criado com o CLI rodando | **não** |
| `teste54-normal-ligado.txt` (controle) | criado com o CLI rodando | sim (em < 40 s) |

Conclusão: arquivos com ponto no primeiro nível da raiz do cofre ficam fora, na partida e com o CLI
rodando, o que confere com o item 8 do ticket 48 (pastas com ponto de primeiro nível). **Não testado:** o
mesmo arquivo dentro de uma subpasta (o ticket 48 achou que pastas com ponto aninhadas vazam na partida) e os
arquivos `-wal` e `-shm` que o SQLite cria ao lado; o plugin do Obsidian (só o CLI foi usado). Estado ao
fim: CLI morto, `docker compose stop` (CouchDB e o contêiner do MCP, que o compose sobe junto), os três
arquivos com ponto apagados do disco do `cofre-c`. **Ficaram no banco e no disco do `cofre-c`** os dois
arquivos de controle `teste54-normal-*.txt` (dados meus; apagá-los pelo CLI propagaria exclusões).

## 6. Perguntas que todas as cinco configurações erraram

Quatro, todas do tipo P e em pt:

- **25** (assistente numa caixa isolada, sem rede privada): a resposta usa "sandbox", "Tailscale" e "porta de
  entrada"; a pergunta tem só descrição. Os tickets 36/37/40 e as pesquisas de acervo ganham por falar de
  assistentes e acesso. Hipótese: vocabulário totalmente diferente, e o e5-small fraco em paráfrases longas.
- **26** (sistema de anotações antigo): o arquivo certo é `01-licoes-do-vault.md`; "vault" não aparece na
  pergunta, e "anotações" casa com as pesquisas de "benefícios do Claude Code" (memória, notas). Hipótese:
  sinônimo (anotações = vault) e um arquivo curto contra documentos longos com muitas ocorrências.
- **29** (jeitos de arrumar diretórios para o topo do acervo): a resposta é `35-metodos-de-organizar-a-raiz.md`;
  todas devolvem os tickets de "acervo do Maestro" (43/44), que repetem "acervo" no título. Hipótese: a palavra
  "acervo" da pergunta puxa para os arquivos errados; "raiz" e "métodos" não aparecem na pergunta.
- **32** (banco versionado ao estilo git como plano B): a resposta é o ticket do Dolt (`31`); a pergunta não diz
  "Dolt". Os resultados são tickets que citam o Dolt de passagem (27, 48, 24). Hipótese: o nome próprio é a única
  ponte entre a pergunta e o arquivo, e o modelo não conhece "estilo git" = Dolt.

Outros erros que variaram entre configurações (por exemplo 21, 22, 27, 28, 30, 7, 19) estão em
`resultados.json`.

## 7. Neurons e chamadas no gateway

- Chamadas feitas: 3 (uma com `bge-m3` e uma com `embeddinggemma-300m`, ambas em um texto de poucas
  palavras, e uma terceira `bge-m3` para ler o corpo do erro, quando a primeira cortou a mensagem). As três
  deram 429. **Neurons consumidos: 0**, nenhum texto do corpus saiu da máquina. Uma chamada a mais do que
  "uma por modelo" porque reenviei o `bge-m3` para ver a resposta, o que a regra de não repetir desencorajava.
- Planejamento que não foi executado: o corpus tem ~1,7 M de caracteres em `.md`, ou cerca de 0,5 M de tokens
  (~3,5 caracteres por token, estimativa). A ~1000 neurons por milhão de tokens (valor de memória, **não
  verificado** na tabela da Cloudflare), uma indexação completa custaria cerca de 500 a 600 neurons por
  modelo e por ferramenta; duas indexações por modelo nas duas ferramentas cabiam nos 3 mil.
- Não esperei a virada de dia (a cota da Cloudflare zera à 00:00 UTC, ~9 h depois do teste).

## 8. Limites do teste

- Sem gateway: a comparação "modelo local × modelo maior" que motivou o teste **não foi feita**.
- 40 perguntas, 4 em inglês; intervalos de confiança largos (um acerto = 2,5 pontos). Nenhuma repetição.
- Os rótulos de "arquivo certo" vêm do arquivo `perguntas.md`; perguntas com mais de um arquivo certo contam
  acerto em qualquer um.
- OHS indexou 112 de 124 `.md` (12 com YAML inválido) e memtomem 141 arquivos (inclui `.json`/`.py`, menos 2 por
  trava de segredos): os dois conjuntos não são idênticos. Os arquivos não indexados do OHS não são resposta
  de nenhuma pergunta.
- memtomem usou `unicode61` e chunks diferentes entre BM25 (1058 trechos) e e5 (2229), pela configuração do
  preset (não investigado); as duas tabelas de memtomem diferem também por isso. Reranker desligado.
- O RSS do memtomem inclui o modelo; o do OHS ocioso, não. O tempo de rajada do OHS inclui o custo das
  próprias sondas.
- Máquina compartilhada com outros processos (Docker, Claude Code); tempos têm ruído.
- Item 5 testou só o CLI, só a raiz do cofre, sem o plugin e sem `-wal`/`-shm`.
- A busca do OHS roda uma CLI por pergunta; um servidor aquecido (`ohs serve`) seria mais rápido. Não medi.
- Processos encerrados no fim: nenhum `ohs`, `memtomem-server`, `mm` ou CLI do LiveSync rodando; Docker do
  spike parado. O banco `corpus\.obsidian-hybrid-search.db` e `corpus\rajada\` (OHS) ficaram na pasta de
  trabalho.
