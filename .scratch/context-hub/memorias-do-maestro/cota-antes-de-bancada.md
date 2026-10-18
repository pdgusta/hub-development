---
name: cota-antes-de-bancada
description: Antes de qualquer bancada ou teste que chame provedores do FreeLLMAPI, conferir os limites de pedidos por dia (rpdLimit) e orçar as chamadas
metadata:
  type: feedback
---

Antes de rodar bancada, teste ou varredura que chame modelos pelo FreeLLMAPI, ler `rpdLimit`, `rpmLimit` e
`tpdLimit` de cada linha (`GET /api/fallback`) e orçar quantas chamadas cada pool aguenta, deixando sobra para o
trabalho do dia. O gateway tenta até 3 chaves por chamada fixada (`attemptCount`).

**Why:** em 2026-10-13 a bancada mandou 3 pedidos por modelo a 15 modelos do Google (20 pedidos por dia por
modelo) e gastou a cota do dia: o primeiro 429 veio 6 min depois do início, e a pesquisa ampla ficou sem o Google
no dia. O Gustavo: "Seu levantamento acabou com a pesquisa hoje, parabéns você merece palmas".

**How to apply:** pools com limite de pedidos por dia (Google, OpenRouter 50/dia na conta toda, Groq) entram com
1 chamada por modelo, ou ficam fora se o trabalho do dia precisa deles; diga o orçamento na rodada antes do
"pode iniciar". Ver [[freellmapi-tts-e-transcricao]].
