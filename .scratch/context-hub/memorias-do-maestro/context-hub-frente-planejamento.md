---
name: context-hub-frente-planejamento
description: "Este repositório (C:\\Projetos\\context-hub, workspace Maestri 'Context Hub') é a casa da frente context hub + reorganização do Maestri; processo só do Matt Pocock; file-first; uma decisão por vez"
metadata:
  node_type: memory
  type: project
  originSessionId: 84287e4b-6e90-408d-9a3a-1a49e67d6531
  modified: 2026-10-01T02:26:14.533Z
---

Desde 2026-09-30, a frente "organizar a criação e gestão de workspaces e maestros do Maestri + context
engineering + context hub em 2 máquinas" vive **aqui**: workspace Maestri **"Context Hub"**, pasta
`C:\Projetos\context-hub` (repositório git). Esta pasta é **só prova de conceito**: o hub final nasce
do zero em `C:\context-hub` ou dentro do WSL, se for mais viável; nenhuma decisão está fechada
(exploração §12, 2026-09-30).

- Fonte canônica: `exploracao/2026-09-28-context-hub.md` (objetivo proposto na §7.1, candidatos a
  tickets na §11). Relatórios das varreduras em `exploracao/anexos/`.
- Processo: **só o fluxo do Matt Pocock**: `/setup-matt-pocock-skills` → `/wayfinder` → `/to-spec`
  → `/to-tickets` → `/implement`. Nada de brainstorming/writing-plans do superpowers nem GSD nesta frente.
  Essas skills têm `disable-model-invocation`: só o Gustavo as invoca.
- O workspace "context-hub (antigo)" (ex-"TRF3", pasta compartilhada `C:\Projetos\maestri`) fica
  para o Gustavo apagar na interface (a CLI não apaga).
- Há dados de clientes (STRATA, VOEGOL, AVIANCA, TRF3, SBF) nas pastas dos workspaces; política para a
  segunda máquina em aberto. Nunca copiar dados pessoais para notas, tickets ou handoffs.

**Why:** a pasta compartilhada `C:\Projetos\maestri` mistura memória e papéis de SOC, VOEGOL e SBF.
Esta frente quer acabar com isso, e o Gustavo quer `/clear` seguro a qualquer momento.

**How to apply:**
- Gravar cada rodada de decisão no arquivo ou ticket certo enquanto acontece, não só no chat.
- Uma decisão por vez, com uma recomendação; ele responde em texto livre que pode mudar o rumo.
- Desenhar com pontos de encaixe para o que vai mudar (redesenho do vault `ai-operating-system`,
  hub na segunda máquina, camada de busca, versões novas do Maestri), sem acoplar ao vault atual.

Ver [[pesquisar-antes-de-explicar]].
