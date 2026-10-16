# Proposta: roteamento da pesquisa ampla sobre o mecanismo de busca

Ticket "Camada de busca", rodada 6 (2026-10-13). Responde à rodada 5: o Gustavo recusou um fluxo reto de
quatro etapas com seis geradores e pediu um laço sério, que aguente queda de requisição, cota estourada e
resposta picotada, com os geradores presos ao escopo e sem ferramenta que escreva. A descoberta de modelos,
cotas e a melhoria da fallback chain do FreeLLMAPI entram como etapa. Proposta, não decisão: nada roda
antes do "pode iniciar".

Fontes do FreeLLMAPI (clone local `C:\Projetos\freellmapi`, README e `docs/en/api/01-rest-api.md`):
`GET /v1/models?execution_status=ready|exhausted|needsKey`; `GET /api/free-tier` (pools, `remaining`,
`resetAt`); perfis de fallback chain chamados por `auto:<perfil>`; estratégias `auto:smart|fast|reliable`;
cabeçalhos `X-Routed-Via`, `X-Fallback-Trail`, `X-Fallback-Detail`; `tools` e `response_format` repassados
por provedor; ferramenta `google_search` nos modelos Google; modelo virtual `fusion` (painel de modelos e
juiz).

## Princípio

**Os modelos só respondem; quem grava é o laço.** Cada gerador é uma chamada de API, sem harness e sem
ferramenta, exceto a busca do Google (só leitura). O laço é um script que guarda o estado num livro-razão
em arquivo, valida cada resposta e decide o próximo passo. Nenhum modelo toca o disco.

## Etapas

### 0. Preparar o provedor (etapa da montagem, antes de o laço existir)

Correção do Gustavo (2026-10-13): esta etapa não roda dentro do laço. É uma etapa de **montagem**, feita
uma vez antes de começar, para deixar o FreeLLMAPI em forma.

- **Levantar o que existe:** `/v1/models` (catálogo inteiro e `execution_status`), `/api/free-tier` (pools,
  orçamento, `remaining`, `resetAt`), as chaves por provedor e a fallback chain e os perfis atuais.
- **Ensaio de bancada:** um pedido-padrão curto (com esquema JSON) a cada modelo candidato. Mede se devolve
  JSON válido, se trunca, latência, taxa de erro e se o `google_search` funciona nele.
- **Propor estratégias melhores para a fallback chain atual:** ordem, modelos que saem ou entram, diversidade
  de famílias, pools que se esgotam juntos, perfis por tipo de trabalho (gerar com busca na web, juntar,
  conferir) e o perfil `auto:pesquisa`. O Gustavo decide o que vale para o dia a dia e o que é só da pesquisa,
  e aplica no painel.
- **Saída:** `provedor.json` (o retrato), o relatório da bancada e a proposta da chain.

Dentro do laço fica só uma **vigia do provedor**, leve: relê `execution_status` e `resetAt` entre ondas e
quando o `X-Fallback-Trail` mostra falhas seguidas, para adiar pedidos e tirar modelos que caíram. Ela não
muda a chain; só a montagem muda.

### 1. Plano de cobertura (maestro)

- Monta a **matriz de células**: ângulo × língua × formulação. Ângulos: lugares e topologias; ferramentas
  prontas; peças e bibliotecas; conceitos e montagens (agregador, roteador, busca federada); pt-BR e
  multilíngue; clientes sem rede e reservas; vizinhos (memória de agentes, RAG local, busca de código).
  Línguas: pt, en, es, zh, ja, de, ru. Duas ou três formulações por célula.
- Cada célula vira um **pedido** no livro-razão: id, prompt fechado, esquema JSON, orçamento de tokens.
- **Sementes ocultas:** as candidatas já conhecidas (zvec-grep, memtomem, ck, markdown-vault-mcp,
  grooveseek e as das pesquisas antigas) ficam numa lista que os geradores nunca veem. Medem a cobertura.

### 2. Laço de geração (o coração)

Cada pedido tem um estado no livro-razão: `pendente → em voo → aceito`, ou `inválido`, `truncado`,
`adiado por cota`, `fora do escopo`, `esgotado`.

- **Despacho:** pedidos vão em ondas, com paralelismo limitado por pool (não estoura a cota de uma vez).
  Cada pedido vai a **dois modelos de famílias diferentes** (redundância e diversidade); o `X-Routed-Via`
  fica gravado em cada item.
- **Validação de cada resposta:**
  - JSON que não passa no esquema → `inválido` → reenvia com o erro apontado, até 2 vezes, depois outro
    modelo;
  - `finish_reason: length` ou JSON cortado → `truncado` → a célula se **divide em duas menores** (não
    só repete);
  - resposta vazia ou recusa → outro modelo;
  - item fora do escopo → vai para uma caixa de **quarentena** (não é apagado; o maestro olha no fim).
- **Falha de rede e cota:** 429 ou `exhausted` → `adiado por cota` até o `resetAt` do pool, com espera
  exponencial e jitter; disjuntor por provedor quando o `X-Fallback-Trail` mostra falhas seguidas;
  pedido `em voo` sem resposta por tempo demais volta a `pendente`.
- **Esgotado:** o pedido chega aqui quando não sobra caminho: todos os modelos prontos já falharam nele
  (inválido depois das duas reenviadas, recusa, vazio) ou a célula já foi dividida até o tamanho mínimo e
  ainda corta. Não é apagado: fica no livro-razão como **lacuna de cobertura**, aparece no painel, e o
  maestro decide no fim (reformular a célula, tentar depois da virada de cota, ou registrar a lacuna).
- **Retomada:** o livro-razão é só de acréscimo (JSONL) e cada pedido é idempotente. Se o script, a
  máquina ou o gateway cair, o laço recomeça de onde parou, sem repetir o que já foi aceito.
- **Bola de neve (o que faz dele um laço, não uma fila):** depois de cada onda, o juntador conta os itens
  novos. Nomes, termos e ideias novas viram **novas células** ("alternativas a X", "o que se monta com X",
  o termo novo em outras línguas).
- **Parada:** quando duas ondas seguidas trazem menos de 5% de itens novos (saturação), ou quando o
  orçamento acaba. Antes de parar, a **calibração**: se alguma semente oculta não apareceu, o laço gera
  células com o vocabulário vizinho dela (sem citar o nome) e roda mais uma onda. A falha vira dado: qual
  vocabulário faltava.

### 3. Juntar (contínuo, a cada onda)

- Parte mecânica no script: chave canônica (URL do repositório, nome normalizado). Item repetido vira um
  item só, com todas as fontes e todos os modelos que o citaram.
- Haiku 5.5 só para os casos ambíguos (mesma coisa com nomes diferentes; fork contra original).
- **Nada sai:** afirmações que se contradizem ficam lado a lado, com a origem de cada uma.

### 4. Conferir (fila própria, mesmo laço de falhas)

- Sonnet 5.5, com leitura só de fonte primária (README, docs, código bruto, API do GitHub). Resumo de
  WebFetch não conta.
- Preenche as colunas do catálogo e marca cada célula: `verificado`, `não verificado`, `contradito pela
  fonte`.
- Itens com mais menções e as sementes vão primeiro; tudo é conferido, a ordem só define o que chega antes.

### 5. Auditoria por amostra

- Opus confere uma amostra (cerca de 10%) do que o Sonnet marcou. Se o erro passar de um limiar, o lote
  inteiro volta para a fila de conferência.

### 6. Síntese (maestro)

- Mapa de **lugares × mecanismos**, combinações leves e robustas, o que falta montar em cada uma, e a
  pergunta da próxima rodada. O Designer transforma em página.

## Painel e registro

- Um arquivo de progresso por onda: pedidos por estado, itens novos, curva de saturação, cota restante por
  pool, sementes achadas.
- Registro de todas as consultas (protocolo de varredura §10.4 da exploração).

## Colunas do catálogo (pedido da rodada 5: mais colunas)

- **Identidade:** nome, link, tipo (ferramenta pronta, biblioteca ou peça, conceito, montagem), licença,
  linguagem e runtime.
- **Onde roda:** SO (Windows nativo, WSL, Linux, macOS), lugar (disco local, servidor na rede, dentro de
  outro MCP, cliente), recursos (RAM, CPU, GPU), funciona offline.
- **Como o agente chega:** transporte (stdio, HTTP, CLI, biblioteca), MCP nativo, autenticação, vários
  clientes ao mesmo tempo.
- **Como acha:** por palavra (BM25 e afins; stemming e acento em pt-BR), por sentido (embeddings locais ou
  remotos), híbrida, reranking, trechos por título, filtros por metadados e frontmatter, citação do trecho.
- **AI Provider:** aceita endpoint compatível com OpenAI (embedding, rerank, chat), modelos multilíngues.
- **Índice:** onde fica, como se refaz (watcher, hash, na hora da busca), aguenta disco reescrito o tempo
  todo, tempo de reindexar, escala.
- **Formatos:** md, txt, csv, pdf, docx, xlsx, código, imagens.
- **Composição:** pode agregar ou ser agregado (federação), extensível por plugin, como se encaixa no MCP do
  banco (repasse).
- **Maturidade:** versão, estrelas, último commit, mantenedores, CI por SO, documentação.
- **Para o hub:** o que falta montar, esforço estimado, fontes, estado da conferência.
