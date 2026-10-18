---
name: perguntas-em-respostas-md
description: "Em rodadas de grilling, as perguntas vão para a nota Maestri 'Rodada atual' (só a rodada em curso), não para o chat nem para respostas.md"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 424c67ba-e218-44ae-9814-10ee18afdcb1
  modified: 2026-10-10T19:56:04.553Z
---

Durante rodadas de perguntas (grilling, /wayfinder), escreva as perguntas na nota do Maestri
"Rodada atual" (`maestri note write "Rodada atual" ...`), cada uma com a recomendação e uma linha
**Sua resposta:** vazia. A nota guarda só a rodada em curso. O chat leva só um aviso curto. O Gustavo
responde na nota. Absorva a resposta no arquivo dono (ticket, mapa) ANTES de reescrever a nota com a
rodada seguinte, porque a nota não tem histórico.

O `respostas.md` na raiz foi apagado em 2026-10-10 a pedido dele; não recrie.

**Why:** 2026-10-01 ele pediu as perguntas num arquivo em vez do chat; em 2026-10-10 trocou o arquivo
pela nota ("coloque o 'respostas.md' aqui no nota, só para a rodada atual... só manter nossa troca
pelas notas"). File-first continua valendo pelos tickets ([[context-hub-frente-planejamento]]).

**How to apply:** toda rodada de perguntas desta frente. Se a nota não aparecer em `maestri list`,
crie com `maestri note create --name "Rodada atual"`.

**Nunca reescrever a nota antes do aviso "respondi".** Em 2026-10-12 li respostas curtas (A, B, A) e
reescrevi a nota com a rodada seguinte enquanto ele ainda escrevia; a gravação dele trouxe a rodada
antiga de volta e apagou a nova. Esperar o aviso no chat antes de absorver e reescrever.


**Atualização 2026-10-14:** o portal do projeto foi entregue; as rodadas passam a ir para `portal/rodadas/` (formato da §4.1 da `portal/proposta.md`), e a resposta chega pela caixa com aviso automático. A nota "Rodada atual" fica aposentada. Ver [[portal-do-projeto]].
