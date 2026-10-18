---
name: sem-ticket-cego
description: "Nenhum ticket decide em cima de algo que outro ticket aberto ou \"em revisão\" ainda pode derrubar; conferir os Blocked by antes de sugerir"
metadata:
  node_type: memory
  type: feedback
  originSessionId: e3edfb68-e253-4373-a168-fa90c3f8a5e6
  modified: 2026-10-06T19:54:33.465Z
---

Antes de sugerir ou pegar um ticket, conferir se ele depende de uma decisão ainda aberta ou marcada
"em revisão" em outro ticket. Se depende, o `Blocked by` tem de dizer isso. Um ticket resolvido com
comentário "em revisão" não serve de base enquanto não houver um ticket dono da revisão.

**Why:** o Gustavo (2026-10-06): "Não quero ticket cego que defini informação em cima de algo que
claramente não vai dar certo por conta de uma decisão de outro ticket." Na sessão de 2026-10-04 eu
sugeri "Acesso dos agentes: decisão" como próximo, mas o MCP e a checagem de sync dele dependiam do
caminho do banco, ainda aberto.

**How to apply:** ao listar a fronteira, ler a Question e os comentários de cada candidato contra as
decisões abertas; corrigir o `Blocked by` antes de recomendar. Ver [[context-hub-frente-planejamento]].
