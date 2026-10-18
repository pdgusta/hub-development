---
name: doc-por-curl
description: "Para ler documentação na construção, baixar a página com curl (de preferência a versão .md) e ler o original; nunca subagente web-fetch"
metadata:
  node_type: memory
  type: feedback
  originSessionId: f939b88d-0c21-4496-b068-1eaf38b218fa
  modified: 2026-10-17T00:29:33.035Z
---

Para ler documentação (ex.: docs.github.com), baixe a página com `curl` (as docs costumam ter versão `.md`) e leia o original. Vale como fonte primária.

**Why:** a construção proíbe subagentes (o Gustavo quer o trabalho visível no canvas); a Vela usou um web-fetch no ticket 27 e o maestro corrigiu em 2026-10-17.

**How to apply:** em qualquer etapa da construção, doc externa = `curl` direto no Bash, nunca o Agent/web-fetch. Ver [[pesquisar-antes-de-explicar]].
