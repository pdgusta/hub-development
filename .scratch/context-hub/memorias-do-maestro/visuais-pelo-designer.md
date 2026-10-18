---
name: visuais-pelo-designer
description: "Visuais da frente (system-design.html, mapeamento.html e novos) são pedidos ao recruta Designer; o maestro nunca edita direto"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 8a0a694f-68fe-471b-8e15-59922a4a2a8d
  modified: 2026-10-13T03:52:07.229Z
---

Toda criação ou atualização de visual (o portal "System design", o visual do mapeamento e os que vierem)
é pedida ao recruta "Designer" (Claude Opus 5.5, esforço alto desde 2026-10-14, papel "Designer de visuais" no workspace
Context Hub), com `maestri ask` e retorno por ask back. Eu não edito essas páginas.

**Why:** 2026-10-12 o Gustavo pediu: "dispare um agente comandado por você [...] que vai cuidar dos
visuais, inclusive do portal do system design. Você só pede a ele, não faz direto." E: "o novo agente
deve saber me surpreender".

**Quando:** o `system-design.html` só é atualizado quando um ticket que mexe no desenho é marcado como
resolvido; rodada respondida não basta. Os outros visuais podem ser atualizados quando eu quiser.
(Gustavo, 2026-10-13: "o designer só atualiza o system design quando tickets são marcados como
resolved. Os outros designs podem continuar sendo atualizados quando desejar".)

**How to apply:** ao resolver um ticket que muda o desenho, mandar ao Designer o que mudou (fato e
ticket), não o HTML. Se o Designer não estiver no canvas, recrutar de novo com
`maestri recruit "Designer" --preset "Claude Code" --role "Designer de visuais" --command "claude --model claude-opus-5-5 --effort high"`.
