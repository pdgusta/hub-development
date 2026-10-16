---
titulo: Fim da resposta: quando soltar o agente
ticket: 16
aberta: 2026-10-16
estado: aberta
---

No fim de cada resposta de agente, um hook (mod no Claude Code, `Stop` no Codex, `agentStop` no Copilot) roda o
verificador sobre as notas que mudaram naquela resposta. Se falta algo (um campo obrigatório, uma descrição no
`index.md`, um link que devia ser `par://`), o hook **devolve** a resposta ao agente com a lista, e ele conserta antes de
terminar. O mesmo vale, no ticket 18, para a nota de retomada que não reflete o trabalho.

O spec diz "a resposta não termina enquanto houver falta", mas deixa em aberto a **proteção contra laço**: se o agente
não consegue consertar (não entendeu, não tem como, o modelo é fraco), ele para, é devolvido, para de novo, é devolvido
de novo, sem fim. A prova do ticket 03 mostrou que o Codex avisa quando a parada já é uma volta de devolução
(`stop_hook_active`), e os outros dois harnesses têm sinal parecido.

A Vela (ticket 27) pergunta qual regra seguir. A resposta vale também para o hook de fim da retomada (ticket 18).

## Quando o hook solta o agente que ainda tem falta
id: laco-fim-da-resposta
tipo: escolha
recomendada: A

- A: Devolve uma vez; se o agente parar de novo logo em seguida ainda com falta, solta e registra a falta (no `estado.json` da vigia, como item que aparece no início da próxima sessão e na tela de estado); nunca prende o agente, e nada some calado
- B: Devolve até três vezes seguidas; na quarta parada, solta e registra a falta como na A
- C: Nunca solta enquanto houver falta, como o spec diz hoje; se o agente não conseguir consertar, só você interrompe a sessão

## Algo mais?
id: algo-mais
tipo: texto
