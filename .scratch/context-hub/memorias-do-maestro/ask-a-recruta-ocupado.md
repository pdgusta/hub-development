---
name: ask-a-recruta-ocupado
description: maestri ask para recruta Claude Code ocupado deixa o texto digitado sem Enter; conferir com check e reenviar com um ask novo
metadata:
  node_type: memory
  type: feedback
  originSessionId: 4e532614-47b2-44cc-8583-69674999bb43
  modified: 2026-10-13T21:44:43.983Z
---

Quando mando `maestri ask` (ou `--batch`) para um recruta Claude Code que está no meio de um turno, o texto
fica digitado no prompt dele, mas o Enter se perde. Ele termina o turno e fica parado com a minha mensagem no
prompt. `--raw "\r"` e `--raw "\n"` não enviaram; um `maestri ask` novo (mesmo curto, ex. "(enviar)") envia
o que estava digitado mais o texto novo.

**Why:** em 2026-10-13 o Gustavo avisou duas vezes ("sua mensagem pro tear tá com Enter pendente", "acho que o
tear travou"). O Tear e a Salina ficaram ~20 min parados com a tarefa da conferência no prompt.

**How to apply:** depois de mandar tarefa a um recruta ocupado, conferir com `maestri check` se a mensagem
saiu do prompt; se não, mandar um `maestri ask` curto quando ele terminar. Preferir mandar a próxima tarefa
quando o recruta estiver livre, ou junto do aviso de fim dele. Ver [[context-hub-frente-planejamento]].

**Limpar entre frentes:** recruta que acaba uma frente recebe `/clear` antes da próxima (com as instruções em
arquivo, nada se perde). Gustavo, 2026-10-13: "o tear tá com mais de 40% e era pra você já o ter limpado".
Nunca limpar no meio de uma leva de subagentes, porque se perdem os tokens dela.

**Teto de 40% de contexto por despachante:** nenhum recruta abre leva nova acima de 40% (barra do status line
no `maestri check`). Conferir antes de mandar trabalho e a cada aviso; se passar, mandar "pare de disparar" no
meio do turno (a mensagem fica enfileirada e chega quando a leva em voo devolve) e dar `/clear` depois.
Gustavo, 2026-10-13: "não podia passar de 40% e você deixou passar 80". Para mandar `/clear` pela CLI no Git
Bash: `MSYS_NO_PATHCONV=1 maestri ask "Nome" "/clear"`.
