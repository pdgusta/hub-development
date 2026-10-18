---
name: portal-do-projeto
description: "Portal web local do projeto (pedido 2026-10-14): hub dos designs + gerenciar tickets/rodadas; respostas chegam ao maestro sem chat; Designer + revisor Codex Prumo"
metadata:
  type: project
---
Em 2026-10-14 o Gustavo pediu um **portal do projeto**: web system local, aberto no navegador ao lado do Maestri,
para entender o projeto, ver todos os designs e por que existem (o System design mora nele) e gerenciar sem DevOps
(tickets, rodadas, aprovar, responder, personalizar propostas do maestro). As respostas dele no portal chegam ao
maestro sem repetir no chat; quando pronto, substitui a nota "Rodada atual". Núcleo reaproveitável: ele quer um
portal assim em todo workspace de desenvolvimento (futura peça do acervo do maestro).

Briefing integral: `.scratch/context-hub/portal/pedido.md`. Time: Designer (Claude Opus 5.5 medium, dono, decide
tudo) e **Prumo** (Codex `gpt-6.1-sol`, `model_reasoning_effort="medium"`, papel "Revisor do portal",
obrigatório); os dois conversam direto. O maestro só chama o Gustavo para decisão crítica; ele opina no fim.

**Why:** abrir HTMLs avulsos sob demanda ficou desorganizado, e responder pela nota + "respondi" no chat é atrito.
**How to apply:** até o portal ficar pronto, as rodadas seguem na nota ([[perguntas-em-respostas-md]]). Depois,
rodadas vão no formato combinado com o Designer. Recrutar o Prumo de novo:
`maestri recruit "Prumo" --preset "Codex" --role "Revisor do portal" --command 'codex --no-daemon -m gpt-6.1-sol -c model_reasoning_effort="medium"'`
(na partida o Codex pede atualização, responder "2" = Skip, e confiança na pasta, responder Enter).
Ver [[visuais-pelo-designer]].

**Designer em Fable (Gustavo, 2026-10-14):** depois da proposta, o Designer passa a ser Claude Fable 5.1 com
esforço alto (`maestri recruit --preset "Claude Code" --command "claude --model claude-fable-5-1 --effort high" --replace "Designer"`),
com teto de contexto de **50%** (não os 40% dos despachantes, ver [[ask-a-recruta-ocupado]]).

**Designer em Opus alto (Gustavo, 2026-10-14 ~15h20):** saiu do Fable; agora
`maestri recruit --preset "Claude Code" --command "claude --model claude-opus-5-5 --effort high" --replace "Designer"`,
teto de 50% mantido.

**Entregue em 2026-10-14 ~18h** (Prumo: `portal/revisao-final.md`). Roda em http://127.0.0.1:8770/ pelo terminal "Portal" (`iniciar.cmd`). Rodadas em `portal/rodadas/`; respostas em `portal/caixa/`, com aviso ao maestro (canal A, `maestri ask`). Ao receber o aviso: absorver no ticket dono e trocar `estado: nova` por `lida`.
