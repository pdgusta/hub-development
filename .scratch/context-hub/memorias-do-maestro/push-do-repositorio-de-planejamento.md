---
name: push-do-repositorio-de-planejamento
description: "o maestro faz push do repositório de planejamento (pdgusta/hub-development) ao fim de cada etapa; do hub, nunca"
metadata:
  node_type: memory
  type: feedback
  originSessionId: b0a41a14-28ae-40a4-93d6-4cf53f710781
  modified: 2026-10-21T16:07:24.715Z
---

Desde 2026-10-17 ~23h10, o repositório de planejamento `C:\Projetos\context-hub` tem remoto privado
(`github.com/pdgusta/hub-development`) e está clonado na outra máquina do Gustavo, onde roda outro maestro. O maestro
**faz `git push` deste repositório ao fim de cada etapa**, com `git pull` antes. O repositório do hub
(`C:\context-hub`) continua: push só com o Gustavo.

**Why:** o Gustavo escolheu a opção A ("eu mesmo faço o push deste repositório") para a outra máquina receber o
trabalho sem depender dele.

**How to apply:** ao fechar uma etapa (ticket, rodada, entrega), commit + `git pull --rebase` + `git push`. Se o modo
automático barrar o push, pedir a regra de permissão ao Gustavo, sem contornar. A regra já existe
(`Bash(git -C C:/Projetos/context-hub push:*)` em `.claude/settings.local.json`): use essa forma do comando. Se falhar
com "could not read Username" / "user interactivity has been disabled", não é login vencido: o GCM tem duas contas do
GitHub (pdgusta e a do trabalho) e quer perguntar qual; o conserto é `git config --local
credential.https://github.com.username pdgusta` (feito aqui em 2026-10-21; o clone do par B precisa do mesmo). Ao mudar uma memória, atualizar a cópia
em `.scratch/context-hub/memorias-do-maestro/` no mesmo commit. Ver [[autonomia-na-construcao]].
