---
name: nunca-editar-papel-em-uso
description: "Nunca editar (role edit/write/assign) o papel de um recruta que está trabalhando: o Maestri reinicia o terminal e a sessão perde o contexto"
metadata:
  type: feedback
---
`maestri role edit`, `role write` e `role assign` reescrevem os arquivos do papel e **reiniciam na hora todos os
terminais com aquele papel**. A sessão e o contexto se perdem, e os subagentes em voo também.

**Why:** em 2026-10-14 editei os papéis do Designer (Fable 5.1, 20% de contexto, com um subagente rodando) e do Prumo
para acrescentar uma regra, e os dois reiniciaram no meio do portal. O Gustavo: "pq você reiniciou eles mid session
meu Deus [...] e o contexto deles cara?". O fato já estava registrado em "Testes do papel do Maestri" ("editar o
papel os reescreve e reinicia os terminais"), e eu não conferi.

**How to apply:** a instrução nova vai por `maestri ask` ao recruta, e ele a grava no próprio arquivo de estado (ex.:
`construcao.md`). O papel só se edita com o recruta parado entre frentes, ou com o aval do Gustavo, dizendo que reinicia.
Ver [[ask-a-recruta-ocupado]], [[portal-do-projeto]].
