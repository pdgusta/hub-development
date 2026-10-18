---
name: maestro-nao-executa
description: "O maestro não é o centro de toda comunicação nem executa a construção em worktrees; varredura e gestão de git ele pode fazer"
metadata:
  type: feedback
---
Em 2026-10-16 o maestro juntou os tickets 04 e 03 em `integracao` e rodou os testes na worktree de junção. O Gustavo
pediu um recruta para isso ("você é o maestro e deve estar sempre disponível pra orquestrar"), que virou o Rebite
("Integrador da construção", `construcao-do-hub/etapas/juntar-tickets.md`). O maestro leu isso como "nunca rodar
código" e o Gustavo corrigiu: "nessa operação não faz sentido você ser o centro de tanta comunicação e ficar executando
coisa em código em worktree isolada e etc. Mas esses comandos de varredura e git manage você pode sim."

**Why:** o maestro preso em execução longa ou no meio de cada troca entre recrutas trava a orquestração; comandos curtos
de leitura e de git não travam.

**How to apply:** junção, testes e construção em worktree vão para recruta; os recrutas falam entre si direto
(construtor → revisor → integrador), e o maestro recebe só o resultado. O maestro roda sem pedir varreduras de leitura
(grep, status, log, conferências) e gestão de git (commit, ramo, `.gitignore`) no repositório de planejamento. Ver
[[trabalho-visivel-no-canvas]], [[retomada-do-maestro]].
