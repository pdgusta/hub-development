---
name: portal-decide-terminal-conversa
description: "Regra fechada com o Gustavo: perguntas de decisão só no portal (explicação lá, nunca reescrever respondida); terminal para o resto, aviso de uma linha"
metadata:
  type: feedback
---
- **Portal:** só perguntas que pedem decisão do Gustavo, com a explicação completa na própria rodada e na carta.
  Nunca reescrever uma rodada já respondida: abrir uma rodada nova, que aparece como "aguardando você". O que a opção
  decide fica no texto da opção.
- **Terminal:** o resto da conversa. Ao abrir uma rodada, uma linha: "pergunta nova no portal: <título>", sem repetir
  a explicação. Quando ele responder lá, uma linha confirmando o que ficou decidido.

**Why:** 2026-10-14, Gustavo: "eu respondo lá e você me explique pifiamente aqui, daí envia algo la pra eu responder
daí tenho que caçar aonde você alterou. Ta ruim". Ele aceitou a regra: "fechamos assim".

**How to apply:** toda decisão vai para `portal/rodadas/` como arquivo novo, e o chat não duplica explicação.
Ver [[rodada-no-portal-o-essencial-na-opcao]], [[portal-do-projeto]].
