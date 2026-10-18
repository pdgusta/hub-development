---
name: contexto-dos-recrutas-40
description: "O maestro vigia o contexto dos recrutas; acima de 40%, salvar retomada no próximo ponto seguro e só então /clear"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 69195c9e-6f25-449f-9c8e-6a01925ab770
  modified: 2026-10-16T23:45:20.004Z
---

2026-10-16, Gustavo: "os agentes estão passando de 40% hein, tome conta disso também". Brasa estava em 41%, Vela e
Trilho em 55%.

**Why:** contexto cheio deixa o recruta mais lento, caro e esquecido; o maestro é quem vê o canvas inteiro.

**How to apply:** a cada aviso de recruta ou passagem de ticket, conferir a barra de contexto no `maestri check`. Acima de
40%: pedir `etapas/retomada-<nome>.md` no próximo ponto seguro (regra "Contexto acima de 40%" em
`construcao-do-hub/etapas/regras-da-construcao.md`), esperar "salvo para limpar", mandar `/clear` com
`MSYS_NO_PATHCONV=1 maestri ask "<nome>" --raw "/clear\r"` (sem a variável, o Git Bash troca `/clear` por
`C:/Program Files/Git/clear` e o texto fica preso no prompt: aconteceu com a Vela em 2026-10-16), só com o recruta
ocioso e sem mensagem na fila, e depois "leia a sua retomada". Nunca limpar antes de salvar
([[limpar-recruta-so-depois-de-salvar]]).

No Codex (Fielzinho): a barra não mostra %, e o Codex compacta sozinho. Para limpar, com ele ocioso: `--raw "/new\r"`,
depois `--raw "1"` (usar a worktree atual) e então a retomada. "salvo para limpar" pode chegar antes de o recruta
terminar o turno: conferir no `maestri check` que está ocioso e sem fila antes do `/clear`. Monitores em segundo plano não
devem usar `&` dentro do comando (o envio morre com o shell).
