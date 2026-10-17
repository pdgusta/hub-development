# Relatório do ticket 13: gemini pronto e desligado (Trilho)

## Estado

- Ramo `ticket-13` (HEAD 95e37b7), worktree `C:\context-hub-wt\ticket-13`, de `integracao` f83c8f5.
- Primeiro commit, separado (pedido do maestro): f8b8769, o teste do 12 prova o reaproveitamento do índice pelo índice.
- Teste único do gemini: feito, liberado pelo Gustavo (rodada "Busca: o teste único do gemini", opção A).

## 1. Teste do 12 pelo índice (f8b8769)

O Rebite viu `12-busca.test.mjs` falhar sob carga na junção do 15: a 2ª partida levou 40,6 s para ficar pronta, contra
26,7 s da 1ª. Esse tempo inclui carregar o modelo; não prova nada sobre o índice. Agora:
- antes de parar a 1ª partida, o teste lê do índice (o sqlite da própria busca, num processo filho, só leitura) os ids
  dos pedaços (`chunks`) de cada nota; depois da 2ª partida, lê de novo; reindexar uma nota apaga os pedaços dela e
  grava outros, com ids novos;
- exige pelo menos 200 notas no índice e nenhuma reindexada (fora a nota de cabeçalho quebrado, que o servidor tenta
  de novo a cada partida, achado 3 do 12). Rodada: 256 de 256 reaproveitadas, 9/9;
- `pronta_ms` e a duração da indexação ficam só medidos.
- Tentativa descartada: a "fila" do progresso do servidor ("N/total") não serve; a 2ª partida põe as 257 notas na fila
  e pula as que estão em dia em 0 s.
- Armadilha achada: carregar o `better-sqlite3` no processo do teste trava a pasta do ensaio no Windows (DLL carregada),
  e ela não sai no fim (EPERM). Por isso o processo filho.

## 2. Configuração do gemini, desligada (32e77b2)

- `agents/skills/busca/gemini.env`: `OPENAI_BASE_URL=${FREELLM_BASE_URL}/v1` e
  `OPENAI_EMBEDDING_MODEL=gemini-embedding-001` (modelo explícito, nunca `auto`); sem chave no arquivo; comentário com o
  que ligar significa (o texto indexado vai ao Google; depende da rede e da cota) e o aviso de usar hub e índice
  separados (trocar o modelo reindexa tudo; o `--db` não separa o índice).
- `agents/skills/busca/iniciar.ps1 -Gemini`: só com a opção ele lê o `gemini.env`, exige `FREELLM_BASE_URL` (recusa alta
  sem ela) e a chave (`FREELLM_API_KEY` do processo, senão a do usuário, onde o FreeLLMAPI a guarda), e avisa
  "gemini LIGADO". Sem a opção, o embedding é sempre o local: o script tira os `OPENAI_*` do ambiente.
- Fonte: o obsidian-hybrid-search 0.16.2 entra em modo API quando há `OPENAI_API_KEY` ou `OPENAI_BASE_URL`
  (`embedder.js`, `useRemoteEmbeddings`), pede `GET {base}/models/{modelo}` (o `context_length`) e
  `POST {base}/embeddings`. O FreeLLMAPI (`docs/en/api/01-rest-api.md`, clone local) tem `/v1/embeddings`
  OpenAI-compatível, família `gemini-embedding-001` (3072 dimensões, Google, padrão), "failover never crosses models".
- Testes `agents/code/test/13-gemini.test.mjs` (4, sem chamar o gateway; o gateway é um dublê em 127.0.0.1): o arquivo
  tem o modelo explícito, o gateway por variável e nenhuma chave; desligado, a busca sobe com o arctic e não chama o
  gateway mesmo com `OPENAI_*` e `FREELLM_*` no ambiente; `-Gemini` sem `FREELLM_BASE_URL` é recusado; ligado, num hub
  separado, os embeddings vão ao gateway com `gemini-embedding-001` e `Bearer <FREELLM_API_KEY>`.
- Armadilha: script PowerShell sem `[CmdletBinding()]` não recusa opção desconhecida (vai para `$args`); na rodada
  vermelha, sem o `-Gemini`, o script subiu a busca de verdade e o teste ficou esperando. O teste da recusa agora tem
  `timeout`.

## 3. Teste único do gemini (95e37b7)

Condições da rodada: conferir antes o limite diário e o gasto do dia, parar se passar de um quarto do que resta;
cópia do hub de ensaio, segundo índice, as perguntas do aceite; configuração termina desligada.

- **Contêiner**: `docker start freellmapi-freellmapi-1` (o existente, parado; nenhum criado); memória livre antes:
  3,9 GB (piso 2 GB); trava pesada criada e apagada; parado de novo no fim (`docker stop`, "Exited").
- **Cota antes**: o FreeLLMAPI não guarda `rpd_limit` para embeddings; o limite está no rótulo da família:
  "100 rpm · 1K req/day" (`embedding_models.quota_label`). 5 chaves Google ativas. Gasto do dia, lido do banco do
  gateway (`/app/server/data/freeapi.db`, só leitura, por `docker exec`): 0 pedidos de embedding no dia UTC e 0 desde a
  meia-noite do Pacífico (o reset do Google). Restava 1000 (contando um projeto só); um quarto, 250.
- **Gasto do teste**: **62 pedidos** ao Google, todos `success`, 13 496 tokens de entrada. Abaixo dos 250. Eu tinha
  previsto ~15 (lotes de 10); o gateway conta um pedido por pedaço, mais um por pergunta.
- **O que rodou**: `FREELLM_BASE_URL=http://localhost:3001 node agents/code/test/13-gemini/teste-unico.mjs`: dois hubs de
  ensaio iguais (o do montador mais as notas do aceite do 12), um com o arctic e outro na porta 3940 com `-Gemini`.
- **Índices**: arctic 53 notas, 77 pedaços, 768 dimensões, indexação 27 s; gemini 53 notas, 53 pedaços, 3072
  dimensões, 0 pedaços com falha, indexação 5 s, `context_length` 20 000 (dado pelo gateway; por isso um pedaço por
  nota).
- **Perguntas do aceite** (posição da nota esperada entre as 5 primeiras; "-" = fora):

| pergunta | modo | arctic | gemini |
| --- | --- | --- | --- |
| palavra: "salas de reunião" | fulltext | 1 | 1 |
| palavra: "salas de reunião" | hybrid | 1 | 1 |
| paráfrase: "dividir transferência das mensagens eletrônicas por etapas" | semantic | 2 | 1 |
| a mesma | hybrid | - | - |
| paráfrase: "devolução do gasto com automóvel particular" | semantic | 1 | 1 |
| a mesma | hybrid | 4 | 2 |
| inglês: "how long are backups kept" | semantic | 1 | 1 |
| inglês | hybrid | 1 | 1 |
| pdf.md: "feriado de novembro" | fulltext | 1 | 1 |
| pdf.md | hybrid | 1 | 3 |

  Leitura: no modo por sentido, o gemini pôs a nota em 1º nas três perguntas; o arctic, em 1º, 2º e 1º. No modo
  `hybrid`, as duas paráfrases caem nos dois (uma fica fora das 5 nos dois): as notas novas das skills do maestro
  (ticket 20) competem pelas palavras. O aceite do 12 pede a paráfrase em `semantic`, onde os dois passam. Amostra
  pequena (53 notas): não é bancada.
- **Termina desligada**: o `gemini.env` não liga nada sozinho; a busca padrão (`iniciar.ps1` sem `-Gemini`) segue no
  arctic. O hub e o índice do teste foram apagados.
- Evidência: `agents/code/test/13-gemini/evidencia/teste-unico.json` (posições, as 5 primeiras de cada busca, o status
  dos dois índices). Sem chave.

## Testes

- `13-gemini.test.mjs`: 4/4. `12-busca.test.mjs`: 9/9.
- Suíte comum: a rodar com a trava antes da revisão.

## Não verificado / para o maestro

- A família do gemini no gateway é a padrão do FreeLLMAPI; se o Gustavo mudar a família padrão no painel, o
  `gemini.env` continua explícito e não muda.
- O `context_length` de 20 000 que o gateway devolve faz um pedaço por nota no gemini; notas longas viram um vetor só.
