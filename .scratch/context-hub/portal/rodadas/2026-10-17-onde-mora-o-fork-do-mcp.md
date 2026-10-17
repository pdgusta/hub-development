---
titulo: Onde mora o fork do MCP do banco
ticket: 16
aberta: 2026-10-17
estado: aberta
---

O próximo ticket da Vela é o 09: o **MCP do banco**, por onde o agente lê e grava a verdade do hub, conferindo a versão
lida e mostrando o conflito. Ele é um **fork nosso** do MCP do es617 (obsidian-sync-mcp, TypeScript, Node 22 ou mais
novo). O spec diz "repositório próprio fora do hub (pergunta abaixo)", mas a pergunta nunca foi respondida. A sua
decisão "Onde mora o código do hub" (quem chama: skill em `agents/skills/`, motor em `agents/code/`) tratou do código
que nós escrevemos; o fork é diferente: traz o histórico do upstream e um `node_modules` de centenas de MB.

O que pesa:
- **Dentro do hub**, o `node_modules` precisaria ficar fora da réplica (o gerador de exclusões resolve) e o histórico do
  es617 se perde: puxar uma correção do upstream vira cópia manual.
- **Fora do hub**, o fork guarda o histórico e os ramos por ticket, e o hub leva só o passo do kit que o sobe e o teste
  de ponta a ponta. A outra máquina recebe o fork pelo kit de par (tickets 23 e 24), não pelo LiveSync.
- Já existe um clone limpo do upstream em `C:\Projetos\hub-mcp-banco` (v0.10.0, de 2026-10-15).

## Onde mora o fork do MCP do banco
id: fork-do-mcp
tipo: escolha
recomendada: A

- A: Repositório próprio fora do hub, em `C:\Projetos\hub-mcp-banco` (o clone que já existe), só local, com um ramo por ticket; no hub ficam o passo do kit que o sobe e o teste de ponta a ponta; publicar no GitHub fica para depois, com o seu aval
- B: Dentro do hub, em `agents/code/mcp-banco/`, como o resto do motor: o código do es617 copiado sem o histórico, o `node_modules` fora da réplica
- C: Fork no GitHub agora (público ou privado), clonado em `C:\Projetos\hub-mcp-banco`; a outra máquina clona de lá

## Algo mais?
id: algo-mais
tipo: texto
