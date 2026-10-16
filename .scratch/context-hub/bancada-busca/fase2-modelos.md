# Fase 2: modelos de embeddings na Robusta e no OHS

Ticket 54 (rodada 2: lista de 15 modelos, duas etapas, API liberada, dois rerankers). Rodou o agente do ajuste
(`aa5ada2d3595885dc`, Opus 5.5 médio) de ~01h a ~03h25 de 2026-10-15. Ele caiu duas vezes por erro de API (sem
resposta por 13 min) antes de escrever este relatório; **o maestro escreveu este texto a partir dos arquivos brutos**
em `C:\Projetos\bancada-busca\fase2\` (`avaliacao.jsonl`, `ohs.jsonl`, `rerank.jsonl`, `sonda*.log.*.out`,
`api*.log.*.out`). Leitura de números, sem nova execução.

Mesmas 40 perguntas e 124 notas da fase 1. Métrica: hit@5 / MRR. L = perguntas com as palavras da nota; P = perguntas
com outras palavras. "124" = todas as notas; "sem 12" = sem as 12 notas que o OHS não lê (YAML inválido), para
comparar com ele.

## Etapa 1: na Robusta (9 de 15 avaliados)

| Modelo | Só vetor, 124 | Só vetor, sem 12 | P só vetor, 124 | Híbrida RRF, 124 | ms por consulta |
|---|---|---|---|---|---|
| gemini-embedding-001 (API Google) | **0,900 / 0,728** | **0,925 / 0,775** | 0,85 / 0,679 | 0,825 / 0,578 | 102 |
| embeddinggemma-300m | 0,875 / 0,632 | 0,875 / 0,672 | 0,85 / 0,629 | 0,800 / 0,553 | 228 |
| arctic-embed-m-v2.0 | 0,850 / 0,600 | 0,875 / 0,668 | 0,80 / 0,595 | 0,825 / 0,567 | 46 |
| harrier-270m | 0,800 / 0,585 | 0,825 / 0,651 | 0,80 / 0,512 | 0,800 / 0,514 | 512 |
| gte-multilingual-base | 0,725 / 0,543 | 0,750 / 0,590 | 0,65 / 0,522 | 0,850 / 0,517 | 18 |
| bge-m3 | 0,825 / 0,540 | 0,825 / 0,628 | 0,80 / 0,535 | 0,750 / 0,496 | 41 |
| granite-311m | 0,825 / 0,492 | 0,825 / 0,595 | 0,75 / 0,493 | 0,850 / 0,549 | 36 |
| e5-small (o da fase 1) | 0,700 / 0,461 | 0,700 / 0,519 | 0,55 / 0,367 | 0,650 / 0,430 | 6 |
| granite-97m | 0,575 / 0,421 | 0,625 / 0,459 | 0,40 / 0,275 | 0,725 / 0,467 | 9 |

Leitura:
- **Todos menos o granite-97m superam o e5-small da fase 1**, e o ganho mora nas perguntas P (paráfrase): de 0,37 para
  0,5 a 0,68 de MRR.
- **Melhor local:** embeddinggemma-300m e arctic-embed-m-v2.0, quase empatados; o arctic é 5 vezes mais rápido na
  consulta (46 contra 228 ms).
- **Melhor geral:** gemini-embedding-001 pela API, com folga (MRR 0,728 só vetor).
- **A híbrida RRF fica abaixo do vetor sozinho nos bons modelos** (gemini 0,578 contra 0,728). É o mesmo efeito visto
  no ajuste; a fusão de pesos iguais puxa para baixo as perguntas P. Causa não investigada.

## Fora da etapa 1 (6 de 15)

| Modelo | O que aconteceu |
|---|---|
| harrier-0.6b, embeddinggemma-2, e5-large-instruct, Qwen3-Embedding-0.6B | Sonda passou (carrega e gera vetor; estimativa de 44 a 102 min de indexação cada, Qwen3 com 5,4 GB de RAM). Não chegaram a ser indexados: o agente seguiu para as etapas seguintes e caiu antes de voltar a eles. |
| text-embedding-3-large (API OpenAI) | O gateway FreeLLMAPI não conhece esse nome ("Unknown embedding model … Use a family name, or a provider model id"). Zero feito; falta achar o id certo no gateway. |
| embed-v4.0 (API Cohere) | Limite da chave de teste da Cohere: 100 mil tokens por minuto. Parou em 672 de 1.862 trechos. |

## Etapa 2: os 3 melhores também no OHS

O agente escolheu arctic-m-v2, granite-311m e gte-multilingual-base (critério não registrado; embeddinggemma e gemini
ficaram fora, motivo não verificado: talvez o OHS só aceite modelos ONNX do Hugging Face).

| Modelo no OHS | Híbrida | Só semântica | Reindexação |
|---|---|---|---|
| e5-small (fase 1, referência) | 0,750 / 0,509 | | |
| **arctic-embed-m-v2.0** | **0,875 / 0,632** | 0,850 / 0,667 | 388 s, 1,5 GB |
| granite-311m | 0 / 0 (falhou) | 0 / 0 | o arquivo `onnx/model_quantized.onnx` não existe no repositório do modelo; o OHS não gerou vetor |
| gte-multilingual-base | 0,400 / 0,207 (anômalo) | 0,200 / 0,101 | 958 s, pico de 8,1 GB; resultado abaixo do e5, provável defeito, causa não investigada |

**O arctic no OHS sobe a híbrida de 0,509 para 0,632 de MRR**, a melhor híbrida de toda a bancada.

## Rerankers (sobre a híbrida RRF do arctic na Robusta)

| Reranker | 124: antes → depois | P: antes → depois | L: antes → depois | Tempo por consulta (20 candidatos) | RAM |
|---|---|---|---|---|---|
| bge-reranker-v2-m3 | 0,825/0,567 → 0,850/0,588 | 0,425 → 0,595 | 0,708 → 0,581 | 14 s (máx. 18 s) | 2,2 GB |
| gte-multilingual-reranker-base | 0,825/0,567 → 0,775/0,565 | 0,425 → 0,521 | 0,708 → 0,608 | 6,7 s | 3,0 GB |

Leitura: o bge ajuda nas paráfrases e atrapalha nas literais, quase empata no total, e custa 14 s por busca nesta
máquina (CPU). O gte piora. **Rerank local não compensa aqui.**

## Avisos

- Máquina de 15,7 GB: o gte no OHS chegou a 8,1 GB e a pressão de memória fez o Claude Code matar um processo de
  fundo às ~04h.
- 40 perguntas, das quais só 4 em inglês: diferenças de 0,02 a 0,03 de MRR não separam modelos.
- Não verificado: o critério da escolha dos 3 para o OHS; se o OHS aceita embeddinggemma ou um modelo por API.

## Rodada 3: os quatro locais maiores (completar, 2026-10-15)

Disparado pelo maestro às ~07h55 (`fase2/completar.sh`, sem agente Claude), fim às 11h46 (`completar.fim`). Mesmas 40
perguntas e 124 notas. Tabela final, ordenada pelo MRR só vetor (gerada de `avaliacao.jsonl`, a última avaliação de
cada modelo):

| Modelo | Só vetor, 124 | Só vetor, sem 12 | P só vetor, 124 | Híbrida RRF, 124 | ms por consulta |
|---|---|---|---|---|---|
| gemini-embedding-001 (API Google) | **0,900 / 0,728** | **0,925 / 0,775** | **0,850 / 0,679** | 0,825 / 0,578 | 102 |
| embeddinggemma-2 (novo) | 0,900 / 0,639 | 0,925 / 0,719 | 0,800 / 0,547 | 0,825 / 0,553 | 542 |
| embeddinggemma-300m | 0,875 / 0,632 | 0,875 / 0,672 | 0,850 / 0,629 | 0,800 / 0,553 | 228 |
| arctic-embed-m-v2.0 | 0,850 / 0,600 | 0,875 / 0,668 | 0,800 / 0,595 | 0,825 / 0,567 | 46 |
| harrier-270m | 0,800 / 0,585 | 0,825 / 0,651 | 0,800 / 0,512 | 0,800 / 0,514 | 512 |
| gte-multilingual-base | 0,725 / 0,543 | 0,750 / 0,590 | 0,650 / 0,522 | 0,850 / 0,517 | 18 |
| bge-m3 | 0,825 / 0,540 | 0,825 / 0,628 | 0,800 / 0,535 | 0,750 / 0,496 | 41 |
| harrier-0.6b (novo) | 0,800 / 0,535 | 0,900 / 0,627 | 0,700 / 0,417 | 0,750 / 0,565 | 1.093 |
| granite-311m | 0,825 / 0,492 | 0,825 / 0,595 | 0,750 / 0,493 | 0,850 / 0,549 | 36 |
| e5-large-instruct (novo) | 0,750 / 0,491 | 0,750 / 0,565 | 0,700 / 0,449 | 0,750 / 0,471 | 175 |
| e5-small (fase 1) | 0,700 / 0,461 | 0,700 / 0,519 | 0,550 / 0,367 | 0,650 / 0,430 | 6 |
| granite-97m | 0,575 / 0,421 | 0,625 / 0,459 | 0,400 / 0,275 | 0,725 / 0,467 | 9 |
| Qwen3-Embedding-0.6B (novo) | 0,625 / 0,395 | 0,700 / 0,486 | 0,500 / 0,257 | 0,750 / 0,468 | 160 |

Indexação dos novos (1.862 trechos, CPU): embeddinggemma-2 41 min e 3,4 GB; e5-large-instruct 50 min e 2,4 GB;
harrier-0.6b 80 min e 3,2 GB; Qwen3 67 min e 7,5 GB de pico.

Leitura:
- **Nenhum dos maiores muda o quadro.** O embeddinggemma-2 empata com o embeddinggemma-300m (0,639 contra 0,632,
  dentro do ruído de 40 perguntas) e é pior nas paráfrases (0,547 contra 0,629), com o dobro do tempo por consulta.
- **O Qwen3 ficou abaixo do e5-small**, o que é estranho para o tamanho dele. Configuração usada: q8, pooling do último
  token, instrução na consulta (`modelos.mjs`). Causa **não investigada** (pode ser a quantização ou o lado do
  preenchimento no pooling do último token).
- O quadro de cima segue: o gemini pela API é o melhor; entre os locais, embeddinggemma-300m e arctic-embed-m-v2.0
  quase empatados, e o arctic é o único que já rodou no OHS (híbrida 0,632, a melhor da bancada).

Fora, de vez nesta fase:
- **embed-v4.0 (Cohere):** a primeira tentativa parou no limite da chave de teste (100 mil tokens por minuto) em 960 de
  1.862; a relançada caiu com HTTP 502 em 240. Sem avaliação.
- **text-embedding-3-large (OpenAI):** o gateway não tem essa família registrada (a documentação do FreeLLMAPI a põe no
  GitHub Models). Sem avaliação.
