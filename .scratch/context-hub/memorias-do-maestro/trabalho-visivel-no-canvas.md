---
name: trabalho-visivel-no-canvas
description: "Revisor ou executor que o Gustavo aprova vira recruta no canvas do Maestri, não subagente escondido; ele quer ver com o que cada um anda"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 204bd16a-a2be-4754-ab82-c5326a4d8833
  modified: 2026-10-16T17:29:51.298Z
---

Quando uma rodada aprova "um revisor" (ou outro executor), ele nasce como **recruta no canvas do Maestri**, não como
subagente do maestro.

**Why:** 2026-10-16, depois da execução de 10 workers com vários subagentes cada ("nem sei com o que cada um andou"), o
Gustavo tirou todos do canvas e, na rodada `2026-10-16-revisao-do-spec-r1`, comentou: "esse revisor deve estar no canvas
do maestri".

**How to apply:** propor recruta visível, com papel claro e saída em arquivo; evitar camadas de subagentes que ele não
enxerga. Ver [[portal-decide-terminal-conversa]], [[pesquisa-pelo-freellmapi]].

**Atualização 2026-10-17 ~04h:** limite de **4 agentes paralelos** (construtores) e cada recruta pode usar **até 1
subagente** por vez, para tarefa fechada e leve, **mais até 3 subagentes Haiku 5.5 médio** só para tarefa realmente simples ou QA; o trabalho principal segue visível no canvas.
