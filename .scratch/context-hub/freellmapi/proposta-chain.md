# Proposta: fallback chain e perfil `auto:pesquisa` (2026-10-13)

Parte do ticket "Preparar o FreeLLMAPI para a pesquisa da busca". Base: [relatório da bancada](relatorio-bancada.md),
[`qualidade-urls.json`](qualidade-urls.json) e os limites de cada linha da chain (`GET /api/fallback`).
Proposta, não decisão: o Gustavo decide e aplica no painel.

## Regras do Gustavo (rodadas 2 e 3)

1. Todo gerador precisa de ferramenta de busca, porque sem ela o modelo inventa da memória.
2. Rodada 2: seguir "com os modelos que possuem cota por token, não por quantidade diária". Na primeira
   versão desta proposta eu escrevi "por token ou por minuto"; o "por minuto" foi acréscimo meu, e o
   Gustavo corrigiu. Os da NVIDIA (40/min) e da OVH (2/min por IP) têm limite por minuto e nenhum por dia;
   ficam na tabela até o Gustavo dizer se valem.
3. Rodada 3: o Google volta, com mais 3 chaves (10 no total), e o limite de cota tem de ser respeitado.

Daí saem os filtros: `supportsTools: true`, sem limite de pedidos por dia (a exceção é o Google, com
orçamento; ver abaixo) e 100% de URLs reais ou perto disso na bancada.

## O que a regra 1 pede fora do Google

Fora do Google, o FreeLLMAPI não tem busca: o `google_search` é traduzido só pelo provedor Google
(`server/src/providers/google.ts`), e não há outra busca na web na documentação nem nos provedores do
clone. Para os outros modelos, a busca tem de ser uma **função que o laço oferece e executa**. O modelo
pede `web_search(query)`, o script busca e devolve o resultado, e o modelo continua sem tocar no disco.
Isso abre uma pergunta para a pesquisa ampla: qual serviço de busca o laço chama. O teste de tool calling
(rodada 3, no [relatório](relatorio-bancada.md)) mostrou que 10 dos 11 modelos fora do Google chamam a
função com `query` válida pelo gateway, e 7 deles usaram só as URLs do resultado em todas as conversas.

## Perfil `auto:pesquisa` (geradores)

| # | Modelo (provedor) | Família | Limite | URLs reais | Acertos | Latência mediana |
|---|---|---|---|---|---|---|
| 1 | `nvidia/nemotron-3-super-120b-a12b` (NVIDIA) | Nemotron | 40/min | 9/9 | 3/3 | 8 s |
| 2 | `gpt-oss:120b` (Ollama Cloud) | gpt-oss | tokens/mês (~10-20M) | 9/9 | 3/3 | 22 s |
| 3 | `@cf/openai/gpt-oss-120b` (Cloudflare) | gpt-oss | neurons/dia | 9/9 | 3/3 | 22 s |
| 4 | `Meta-Llama-3_3-70B-Instruct` (OVH) | Llama | 2/min por IP | 9/9 | 3/3 | 17 s |
| 5 | `Mistral-Small-3.2-24B-Instruct-2506` (OVH) | Mistral | 2/min por IP | 9/9 | 3/3 | 8 s |
| 6 | `Qwen3.5-397B-A17B` (OVH) | Qwen | 2/min por IP | 6/6 | 2/6 | 29 s |
| ~~7~~ | ~~`poolside/laguna-xs-2.1` (NVIDIA)~~ | Poolside | 40/min | 6/6 | 2/3 | 22 s; sai: 502 nas 2 conversas do teste de tool calling |
| ~~8~~ | ~~`agnes-2.5-flash` (agnes)~~ | Agnes | promoção, $0/token | 8/9 | 3/3 | 10 s; sai: resposta final vazia nas 2 conversas |
| 9 | `nemotron-3-super` (Ollama Cloud) | Nemotron | tokens/mês (~5-10M) | 8/9 | 3/3 | 10 s |
| 10 | `nvidia/nemotron-3.5-lightning-30b-a3b` (NVIDIA) | Nemotron | 40/min | 8/9 | 3/6 | 80 s |

### Google, com orçamento de cota

| Modelo | Bancada | Observação |
|---|---|---|
| `gemini-3.1-flash-lite` | 3/3, 9/9 URLs reais, 6 s | o único Google que respondeu bem |
| `gemini-3.5-flash`, `3.6`, `3.7`, `3.8-flash` | 0/3 | 503 "high demand", timeout de 60 s do gateway e JSON cortado em 700 tokens (o gateway pede mais `max_tokens`) |
| `gemma-4-31b-it` | 3/3 | sem tool calling no catálogo |
| `gemini-2.5-flash`, `gemini-2.5-flash-lite` | 404 | "the catalog entry looks stale": o 1º e o 4º da Default não existem mais no Google |

- **Orçamento:** 20 pedidos por dia por modelo por chave, segundo o `rpdLimit` do catálogo; a cota volta às
  04:00 BRT. O laço conta os pedidos ao Google por modelo no dia, no livro-razão, e para antes do teto
  (proposta: 90%), em vez de descobrir pelo 429.
- **Cuidado (não verificado nesta bancada):** pela memória da frente, a cota do Gemini é por projeto, não por
  chave; só chaves de projetos diferentes somam. As 7 chaves antigas caíram juntas em 6 minutos e cerca de 80
  pedidos, o que combina com chaves do mesmo projeto. Se as 3 novas forem de projetos novos, dão +60 por modelo.
- Hoje, as 7 chaves antigas estão sem cota até as 04:00; sobram as 3 novas.

Reserva: `@cf/meta/llama-3.3-70b-instruct-fp8-fast` e `@cf/meta/llama-4-scout-17b-16e-instruct`
(Cloudflare, 7/9 e 6/9 de URLs reais). O contexto do primeiro é de 24k.

- **Depois do teste de tool calling:** saem Poolside e agnes; os mais firmes foram `nemotron-3-super`
  (Ollama), `nemotron-3.5-lightning` (NVIDIA, mas lento), `llama-3.3-70b-fp8-fast` e `llama-4-scout`
  (Cloudflare), que sobem de reserva para geradores. Ficam cinco famílias: Nemotron, gpt-oss, Llama,
  Mistral e Qwen.
- **Diversidade:** antes do teste eram sete famílias. Na pesquisa, cada pedido vai a dois modelos de famílias diferentes.
- **Pools que se esgotam juntos:** os da NVIDIA (1, 7 e 10) dividem 40 por minuto por chave; os do
  Ollama Cloud (2 e 9), o orçamento mensal; os da OVH são por modelo e por IP, então rodam em paralelo,
  mas cada um só 2 por minuto.
- **Ficaram fora pelas regras**, mesmo indo bem: `qwen3.8-27b` (Groq: 9/9, mas 250 pedidos por dia),
  `nemotron-3-super-120b:free` e `north-mini-code` (OpenRouter: 50 pedidos por dia na conta toda),
  `gemma4:31b`, `nemotron-3-120b` e `gemma-sea-lion` (o catálogo diz que não fazem tool calling).

## Chain Default (dia a dia)

Hoje a fila começa com gemini-2.5-flash (Google, 20 pedidos por dia por modelo), glm-4.5-flash (zhipu,
sem chave) e codestral-latest (0 de 9 URLs reais). A Default tem 339 linhas, e 16 plataformas não têm
chave nenhuma.

Sugestões para você decidir, uma a uma:

1. Descer `codestral-latest` e a família codestral para depois dos geradores acima (servem para código,
   não para fato).
2. Desligar as linhas das 16 plataformas sem chave (aion, bazaarlink, clod, electronhub, llm7, modelscope,
   nara, radeon, requesty, router9, sealion, septor, unorouter, waterfall, xkiro, zhipu), para a chain
   mostrar só o que pode responder.
3. Trocar o topo: `gemini-2.5-flash` e `gemini-2.5-flash-lite` dão 404 (catálogo velho). No lugar deles,
   `gemini-3.1-flash-lite`; logo depois, os 1 a 5 da tabela dos geradores, para que a queda do Google caia em
   modelos que não inventam URL.

## O que ficou de fora da medida

- `google_search` (cota do Google), lucidity, orcarouter e cohere (só cota).
- Tool calling pelo gateway em qualquer modelo.
- Relevância dos itens: URL que existe não quer dizer projeto que serve.
