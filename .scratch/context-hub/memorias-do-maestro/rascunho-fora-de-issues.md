---
name: rascunho-fora-de-issues
description: rascunhos e arquivos de apoio nunca em .scratch/context-hub/issues/ — o portal lê cada .md dali como ticket
metadata:
  node_type: memory
  type: feedback
  originSessionId: ae4d6d00-291c-40f8-a649-1878f444290c
  modified: 2026-10-15T20:06:22.490Z
---

Nada além de tickets `NN-slug.md` em `.scratch/context-hub/issues/`. Rascunho de Answer, notas de apoio e saídas de
subagente vão para `.scratch/context-hub/rascunhos/` (ou a pasta da frente).

**Why:** em 2026-10-15 o maestro pediu a um subagente o `issues/12-answer-rascunho.md`; o portal acusou "ticket sem
linha Status" e "número 12 repetido" num alerta ao Gustavo.

**How to apply:** ao delegar rascunho de ticket, dar o caminho em `rascunhos/`. Relacionado: [[portal-do-projeto]].
