---
titulo: Quais skills cada agente enxerga
ticket: 15
aberta: 2026-10-15
estado: absorvida
---

Você escolheu a tabela de roteamento com o hook de entrada. Falta decidir **quais skills cada agente enxerga**.

**O que pesa:**
- **Toda descrição de skill fica no contexto a cada turno.** A documentação do Claude Code diz: "for each skill, agent,
  and command that Claude can invoke on its own, the name and description are in Claude's context on every turn". Cada
  skill instalada custa contexto e disputa a atenção com as outras.
- **Hoje, nesta máquina:** 121 skills em `~/.claude/skills`, 72 delas do GSD, que não é o fluxo do Matt Pocock adotado
  no hub. Há 117 em `~/.agents/skills` (Codex e Copilot).
- **Há skill de uso geral e skill de um papel só.** São de uso geral a busca do hub, o FreeLLMAPI e o fluxo do Matt
  Pocock. São de um papel só, por exemplo, os `critique-*` do UX revisor e a `break-ui` do QA. O acervo do maestro (ticket
  "Maestri: padrão e liberdade") já guarda os papéis como peças em `agents/skills/`, e o setup de cada papel é uma receita
  de comandos.
- O Claude Code aceita skill no escopo do usuário (`~/.claude/skills`, "all your projects on this machine") e no escopo
  do projeto (`.claude/skills/`, "sessions in this repository"). A pasta do papel no Maestri é um projeto.

## Quais skills cada agente enxerga
id: escopo
tipo: escolha
recomendada: A

- A: Em duas camadas. A junction global leva só as skills de uso geral (a busca, o FreeLLMAPI, o fluxo do Matt Pocock, a família `maestro-*` e as poucas que servem a qualquer trabalho). As skills de um papel ficam no acervo e entram só na pasta daquele papel, pela receita de setup. O kit tira do escopo global o que não é do hub (o GSD) e guarda uma cópia antes. A tabela de roteamento cobre as duas camadas
- B: Tudo global: todas as skills do acervo pela junction, para todos os agentes, e a tabela de roteamento decide qual usar. Mais simples, mas cada agente carrega dezenas de descrições que não usa
- C: Por iniciativa: cada iniciativa escolhe as suas no `maestro/` dela, além das de uso geral. Mais fino, mas mais uma lista para manter em cada iniciativa

## Algo mais?
id: algo-mais
tipo: texto
