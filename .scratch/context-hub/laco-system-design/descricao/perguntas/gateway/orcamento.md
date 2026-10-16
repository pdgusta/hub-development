# Orçamento de cota da corrida de perguntas (2026-10-15)

Lido do gateway às 17:01 UTC (`GET /v1/models`, `GET /api/fallback`, `GET /api/free-tier`, como o
`laco/despachante.py` faz). Hoje nenhum outro laço estava rodando (último log do `laco/` às 22:16 de ontem).
Nunca `model: auto`: só os 21 modelos explícitos abaixo, cada um com um **teto por dia** em tentativas de chave
(1 + `X-Fallback-Attempts`), que o roteador da corrida respeita. A janela vira às 00:00 UTC (Google às 07:00 UTC).

## Por provedor

| Provedor (pool) | Limite publicado | Modelos escolhidos | Teto da corrida | Sobra para o dia |
|---|---|---|---|---|
| Google (`google::project`) | gemini flash: 20 pedidos/dia por chave, 5 chaves; gemma 1000/dia por chave | `gemma-4-31b-it` (300), `gemini-3.1-flash-lite` (15), `gemini-3.5-flash-lite` (15) | 330 | gemini: 85 de 100 por modelo; nenhum outro gemini usado. No teste, o `gemma-4-31b-it` foi roteado ao Ollama |
| Groq | `gpt-oss-120b` e `gpt-oss-20b`: 1000/dia, 30/min, **200 mil tokens/dia e 8 mil/min** | os dois, 50/dia e 2/min cada | 100 | cada chamada gasta ~3,5 mil tokens: 50 chamadas usam ~175 mil dos 200 mil. Teto baixo para o Groq não estourar e o gateway não cair no Cloudflare |
| Cohere | 33/dia por modelo | `command-a` (10), `aya-expanse-32b` (10) | 20 | 23 por modelo; os outros Cohere intocados |
| NVIDIA | sem limite diário, 40/min, 2 chaves | `diffusiongemma-26b-a4b-it` (300), `ising-calibration-1.5-31b` (200), `nemotron-3-nano-omni-30b-a3b-reasoning` (150) | 650 | sem limite publicado |
| Kilo | sem limite diário | `nemotron-3-ultra-550b` (300; cai na NVIDIA), `dots3-note-preview` (200) | 500 | sem limite publicado |
| Mistral | sem limite diário, 2/min por modelo | `ministral-14b` (200), `ministral-8b`, `mistral-code`, `voxtral-small` (150 cada) | 650 | sem limite publicado; no máximo 4 em voo no pool |
| OVH | sem limite diário, 2/min no pool | `llama-3.3-70b`, `mistral-small-3.2-24b` (150 cada) | 300 | o ritmo de 2/min limita a ~240 em 2 h; 1 em voo |
| Ollama | sem limite | `nemotron-3-super`, `nemotron-3-ultra` (150 cada) | 300 | 2 em voo |
| Routeway | sem limite | `deepseek-v4-flashfree` (100) | 100 | |
| **Total** | | 21 modelos, 11 famílias | **2.950 tentativas** | |

Fora de propósito:
- **OpenRouter** (50 pedidos/dia na conta toda): fora. Os dois modelos que mais renderam no laço da pesquisa
  (`gemma-4-31b`, `nemotron-3-super-120b`) começam a cadeia no OpenRouter, por isso ficaram de fora. Único risco
  residual: o `dots3-note-preview` cai no OpenRouter se o Kilo falhar.
- **Cloudflare** (10 mil neurons/dia, usados pelo TTS em inglês): nenhum modelo Cloudflare escolhido; o `gpt-oss-120b`
  cai no Cloudflare só se o Groq falhar, e o teto do Groq foi posto abaixo do limite de tokens para isso não acontecer.
- Os demais gemini, os Cohere menores, AI Horde, dreamprompting: fora (cota curta, modelos pequenos ou histórico ruim
  no laço da pesquisa).

## Chamadas esperadas

- Onda 1: as 288 células (12 lentes × 12 tipos × 2 formulações), uma chamada cada. Ondas seguintes: as 96 células
  menos cobertas.
- Ritmo medido no teste: latência de 5 a 95 s por chamada (média ~37 s); com 20 trabalhadores e os limites por pool,
  perto de 20 a 30 chamadas por minuto.
- Estimativa: **de 1.500 a 2.950 tentativas** (onda 1 mais 12 a 25 ondas de 96), cada uma de ~2 mil tokens de entrada
  e ~1,5 mil de saída. O que parar primeiro: saturação (duas ondas seguidas com 15% ou menos de novas), 2 h, ou o
  fim da cota orçada acima (a corrida para sozinha se nenhum modelo tem folga na próxima hora). O teto do Gustavo
  de 40 mil tentativas fica muito acima e não deve ser atingido.
- Gasto do teste curto (já feito): 15 tentativas em 14 chamadas.
