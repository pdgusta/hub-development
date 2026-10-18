---
name: dado-de-cliente-nas-duas-maquinas
description: Conteúdo de cliente vive nas duas máquinas do Gustavo; não desenhar o hub supondo que ele não pode sair do notebook corporativo
metadata:
  node_type: memory
  type: feedback
  originSessionId: 8257bd8c-786d-44dd-ab83-fcca55d0699d
  modified: 2026-10-10T21:49:19.828Z
---

Não suponha que conteúdo de cliente é confidencial ao ponto de não poder sair do notebook da ARMIS.
O Gustavo trabalha com cliente também na máquina pessoal, e por enquanto tudo do context hub vive nas
duas máquinas. O controle de acesso por pasta (na camada de busca, ou como guardrail no `AGENTS.md`)
é um mecanismo que ele vai desenvolver depois, fora da frente do context hub, e sem ticket.

**Why:** em 2026-10-10 (R15 de "Arquitetura de pastas e frontmatter do hub"), ele corrigiu: "você
gosta de pensar que 'conteúdo de cliente' é algo confidencial e não pode 'sair' da minha máquina
corporativa, mas eu também executo trabalho na minha máquina pessoal". O debate de raiz tinha
desenhado pasta não replicada e entrada local em cima dessa suposição.

**How to apply:** não use "dado de cliente" como motivo para pasta não replicada, entrada local ou
qualquer restrição de máquina. A regra de dados pessoais do AGENTS.md (UPNs, e-mails e nomes ficam
nas pastas de origem, fora de notas e tickets) continua valendo. Ver [[oportunidades-nao-objecoes]]
e [[context-hub-frente-planejamento]].
