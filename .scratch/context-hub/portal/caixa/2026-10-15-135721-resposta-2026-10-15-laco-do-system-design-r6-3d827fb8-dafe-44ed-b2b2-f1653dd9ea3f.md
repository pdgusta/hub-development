---
tipo: resposta
rodada: 2026-10-15-laco-do-system-design-r6
ticket: 56
enviada: 2026-10-15T13:57:21-03:00
envio: 3d827fb8-dafe-44ed-b2b2-f1653dd9ea3f
estado: lida
substitui:
---

# Resposta: Como refazer a descrição do hub

## O caminho
escolha: A, O laço inteiro: modelo de sete eixos, umas 150 perguntas por vários modelos do FreeLLMAPI, metade escondida, teste de respostas por modelos que só leem a descrição, teste de três diagramas; depois a mistura. Uns 700 mil tokens de Claude e algumas centenas de chamadas do gateway, orçadas antes (a recomendada)
comentário:
> este laço inteiro, mas nem tudo vai só pros freellmapi, alguns devem ir pra subagentes haiku 5.5 Alto. Não preciso de painel disso, pode rodar tudo em background. Pros haiku O orçamento é ilimitado em tokens e limitado a 2h, máximo de 20 subagentes por lote, a quantidade de lote você diz. Para os FreellmAPI 20 workers, tentativas 40k, mas limitado em ondas (2x 15% igual a ultima) e tempo de 2h.

## Algo mais?
> Quero seguir com o resto do context hub enquanto isso roda em background. Já gere outras respostas para cada um dos tickets em andamento sem bloqueantes. Se tiver bloqueantes me diga quais.
