---
name: retomada-do-maestro
description: "Ao retomar a sessão do maestro (após /clear ou sessão nova), ler primeiro .scratch/context-hub/retomada-maestro.md"
metadata:
  type: project
---
O estado em voo do maestro (fios do chat, trabalho dos recrutas, testes pendentes) fica em
`.scratch/context-hub/retomada-maestro.md`, sobrescrito a cada `/clear` pedido pelo Gustavo (primeira vez em
2026-10-14). Ler esse arquivo antes do `map.md`.

**Why:** o Gustavo reinicia o maestro com `/clear` e quer que nada se perca (file-first).
**How to apply:** ao retomar, ler o arquivo, conferir `maestri list` e `portal/caixa/` por `estado: nova`; antes
de um novo `/clear`, reescrevê-lo. Ver [[context-hub-frente-planejamento]], [[portal-do-projeto]].

**Desde 2026-10-16:** o arquivo abre com a seção "Leia nesta ordem", a lista exata do que ler e do que conferir no mundo
real para ficar na mesma página da sessão anterior (pedido do Gustavo: "crie seu próprio handoff de uma maneira que
saiba quais arquivos a próxima sessão tem que ler"). Seguir a lista na ordem; ao reescrever o arquivo antes de um
`/clear`, manter a lista em dia.
