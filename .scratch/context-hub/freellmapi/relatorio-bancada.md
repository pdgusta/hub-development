# Bancada do FreeLLMAPI (2026-10-13)

Parte do ticket "Preparar o FreeLLMAPI para a pesquisa da busca". Dados brutos:
[`bancada.jsonl`](bancada.jsonl) (uma linha por chamada), [`provedor.json`](provedor.json) (retrato do
gateway, sem segredos) e [`qualidade-urls.json`](qualidade-urls.json) (URLs reais por modelo).

## Como rodou

- Gateway local `http://localhost:3001`, clone `C:\Projetos\freellmapi` @ `ac6d29d`.
- Alvos: os 185 modelos do catálogo com `execution_status=ready`. Cada chamada fixou o modelo, nunca
  `model: auto`. Com o "unify" ligado, fixar um id leva ao grupo daquele modelo, e o gateway troca de
  provedor só dentro do grupo (`server/src/routes/proxy.ts`, comentário do #335). O provedor que
  respondeu ficou gravado em `X-Routed-Via`.
- Pedido-padrão: 3 projetos open-source de busca em pasta de Markdown para agente, em JSON
  (`{"items":[{name,url,kind,why}]}`), com `response_format: json_schema`, `max_tokens` 700 e
  temperatura 0,2. Foram 3 vezes por modelo, um provedor por vez (2 s entre chamadas; OVH 31 s, que é
  2/min por IP), e os provedores em paralelo entre si.
- Repescagem: os modelos que só bateram cota tentaram de novo, os que recusaram `response_format`
  repetiram com o JSON pedido só no texto, e os que cortaram a resposta repetiram com `max_tokens` 4000.
  O `google_search` foi testado nos modelos do Google com uma pergunta de fato recente.
- **Repescagem incompleta:** o Claude Code parou o processo porque faltou memória na máquina, quando
  faltavam 10 das 234 chamadas. Não reiniciei.
- No fim, as URLs citadas foram conferidas com GET, para saber se existem.

## Resultado

827 chamadas no total.

| Resultado | Chamadas |
|---|---|
| JSON válido no esquema | 145 |
| Cota ou espera (429) | 445 |
| Erro do provedor (502, 503, timeout de 60 s do gateway) | 125 |
| O gateway recusa `response_format` naquele provedor | 61 |
| Resposta cortada (`finish_reason: length`) | 27 |
| Modelo sumiu no provedor (404) | 11 |
| Não é modelo de chat (áudio, TTS) | 8 |
| JSON fora do esquema | 5 |

- **49 dos 185 modelos** devolveram JSON válido ao menos uma vez, e **36** acertaram as 3 tentativas.
  Quando o JSON veio, veio limpo: em todos os acertos, sem texto em volta.
- **Provedores que responderam:** Cloudflare, Mistral, NVIDIA, OVH, Groq, OpenRouter, Ollama Cloud e
  agnes. **Os que ficaram em cota o dia inteiro:** Google (a mensagem é "You exceeded your current
  quota"; as 7 chaves estavam em espera), lucidity, orcarouter e cohere. Kilo e AI Horde quase não
  aceitam `response_format`.
- **A espera depois de um 429 derruba as tentativas seguintes:** depois de um 429, o gateway põe o
  modelo em espera, e as chamadas seguintes falham em 2 s com "1 route checked (1 rate-limited or on
  cooldown)". Por isso, a taxa de erro de um modelo em cota mede a cota, não o modelo.
- **Modelos que raciocinam antes de responder cortam em 700 tokens.** Com 4000 tokens, 14 dos 30
  voltaram válidos. O próprio gateway avisa: "raise max_tokens for this json_schema request".
- **Latência mediana dos acertos:** 3 a 10 s nos modelos pequenos e médios, 20 a 30 s nos que
  raciocinam e mais de 100 s nos grandes de visão da NVIDIA. O gateway desiste do Google em 60 s.

## URLs inventadas (o achado mais importante para a pesquisa)

Das 169 URLs únicas que os modelos citaram sem busca, **65 existem** e a maior parte do resto dá 404:
repositórios inventados com cara de plausíveis, como `github.com/MarkdownSearch/markdown-search`.

- **Acertaram todas as URLs** (9 de 9): qwen3.8-27b (Groq), nemotron-3-super-120b (NVIDIA e
  OpenRouter), nemotron-3-120b (Cloudflare), gpt-oss-120b (Ollama e Cloudflare), llama-3.3-70b (OVH),
  mistral-small-3.2-24b (OVH), gemma-4-31b (Ollama), gemini-3.1-flash-lite (Google e dreamprompting),
  gemma-sea-lion-v4-27b (Cloudflare) e north-mini-code (OpenRouter).
- **Inventaram quase tudo** (0 a 11%): toda a família codestral e mistral-code, granite-4.0-h-micro,
  gemma-2b, mistral-nemo e mistral-7b. O `codestral-latest` é o 3º da chain Default.
- Limite da medida: URL que existe não quer dizer que o projeto sirva. Os modelos grandes tendem a
  citar os famosos (LangChain, LlamaIndex, Haystack), que existem mas são genéricos. A relevância fica
  para a etapa de conferência da pesquisa.

## O que ainda não foi medido

- **`google_search`:** as 86 tentativas falharam: 83 com 429 (cota, ou "model lacks
  tool-calling" na família gemma, que o gateway também devolve como 429) e 3 com 400. Sem isso não dá para saber se a ferramenta de busca, a única que os geradores da pesquisa
  terão, funciona pelo gateway. A cota do Google volta à meia-noite do Pacífico (04:00 BRT).
- **lucidity, orcarouter e cohere:** só cota, nenhuma resposta.

## Notas da chain atual (do `provedor.json`)

- Default: 339 linhas, todas habilitadas, e 16 plataformas sem chave nenhuma. A zhipu, sem chave, está
  em 2º lugar.
- Os 3 primeiros da Default são gemini-2.5-flash (em cota hoje), glm-4.5-flash (sem chave) e
  codestral-latest (0% de URLs reais).
- Roteamento global em `smartest` (inteligência 0,55, confiabilidade 0,35, velocidade 0,10), com
  exploração ligada. Os perfis `gsd-fast` (6) e `gsd-smart` (8) existem; o `auto:pesquisa` ainda não.

## Teste de tool calling (rodada 3, 2026-10-13)

Dados: [`toolcall.jsonl`](toolcall.jsonl). Cada conversa tinha 2 chamadas. Na 1ª, o modelo recebia a
função `web_search(query)`; na 2ª, recebia um resultado fixo com 3 URLs reais (khoj, ripgrep, chroma) e
tinha de responder em JSON usando só essas URLs. `max_tokens` 1500, temperatura 0,2.

| Modelo (provedor que serviu) | Chamou `web_search` com `query` válida | JSON final só com URLs do resultado |
|---|---|---|
| `nemotron-3-super` (Ollama Cloud) | 2/2 | 2/2 |
| `nemotron-3.5-lightning-30b-a3b` (NVIDIA) | 2/2 | 2/2 |
| `llama-3.3-70b-fp8-fast` (Cloudflare) | 2/2 | 2/2 |
| `llama-4-scout` (Cloudflare) | 2/2 | 2/2 |
| `nemotron-3-super-120b` (Kilo na 1ª, NVIDIA na 2ª) | 2/2 | 1/2 |
| `gpt-oss-120b` (Cloudflare) | 2/2 | 1/2 |
| `llama-3.3-70b`, `mistral-small-3.2-24b`, `qwen3.5-397b` (OVH) | 1/1 | 1/1 (a 2ª conversa bateu 429) |
| `agnes-2.5-flash` (agnes) | 2/2 | 0/2 |
| `poolside-laguna-xs-2.1` (NVIDIA, depois Kilo) | 0/2 (502 do provedor) | - |

- **Resposta final vazia:** nas 4 falhas com tool calling (agnes ×2, nemotron-3-super-120b e
  gpt-oss-120b ×1), a 2ª chamada voltou 200 com o texto vazio. O provável é que o modelo tenha pedido outra
  busca, mas o script não gravou os `tool_calls` da 2ª chamada; **não verificado**. O laço da pesquisa tem
  de aceitar várias rodadas de busca por pedido.
- **OVH:** o limite é 2 por minuto. Uma conversa já usa os 2, e o intervalo de 31 s não bastou para a 2ª
  conversa. Conta certa: uma conversa por minuto por modelo, ou menos, se o limite for por IP para todos os
  modelos (o painel diz "2/min per IP"; não verifiquei se o limite é dividido entre os modelos).
- **Google:** os 2 pedidos com `google_search` (`gemini-3.1-flash-lite` e `gemini-3.5-flash`) voltaram 429.
  Em cada um, o gateway tentou 3 chaves ("after 3 attempts", trail `key1`, `key2`, `key3`), todas em
  espera. Pelo cabeçalho, foram 8 tentativas no Google, acima do teto de 6 que eu tinha prometido: o
  contador conferia o teto antes de cada chamada, mas uma chamada sozinha gasta até 4 tentativas. Não sei se
  alguma das 3 chaves novas foi tentada (o trail não diz qual chave é qual); **não verificado**. O
  `google_search` continua sem medida.
