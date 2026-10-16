---
tipo: resposta
rodada: 2026-10-14-arquitetura-de-pastas-e-frontmatter-r14
ticket: 12
enviada: 2026-10-14T20:51:28-03:00
envio: cf455bcf-30f0-48fe-aa85-17ad92f610de
estado: lida
substitui:
---

# Resposta: O que entra em cada bloco, a ficha, segredos e scripts

## O que entra em cada bloco
mudanças:
- linha "runs": entra de "trabalho de agentes: briefs, handoffs, execuções e revisões, uma subpasta por…" para "execuções e revisões, uma subpasta por execução"
- linha nova "nova-1": bloco "work/", entra "trabalho de agentes: briefs, handoffs, contexto antes de clear", não entra ""
- ordem nova: inputs, research, design, plans, deliverables, evidence, tools, runs, nova-1, procedures, cases, queries, knowledge, notes, labs, other
versão completa: no .json irmão, em corpo.respostas.blocos
comentário:
> sugira algo para o 'não entra' do work/ e melhore ou incremente o texto do 'entra' do work/

## Os campos da ficha (`initiative.md`)
mudanças:
- linha "cadence": valores de "monthly, quarterly, none" para "weekly, monthly, quarterly, none"
versão completa: no .json irmão, em corpo.respostas.ficha
comentário:
> ok

## Onde ficam senhas e tokens
escolha: B, Numa pasta com ponto, `.secrets/`, dentro da iniciativa, fora do `.git`, contando que o LiveSync ignora pastas com ponto (a recomendada era A)
comentário:
> Essa opção selecionada, porém senhas de CONTAS que acessam tenant ficam o KeePass

## Scripts de apoio
escolha: C, Em `tools/` enquanto são scripts de apoio; viram repositório próprio quando ganham testes, dependências ou uso fora da iniciativa (a recomendada)

## Algo mais?
em branco
