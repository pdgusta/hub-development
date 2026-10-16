---
titulo: Acesso dos agentes: o marcador de raiz, explicado
ticket: 14
aberta: 2026-10-15
estado: absorvida
---

Refazendo a pergunta que ficou confusa na rodada anterior.

**O problema que o marcador resolvia.** Quando você abre o Codex ou o Copilot numa subpasta do hub (a pasta de uma
iniciativa ou de um papel), eles sobem pelas pastas procurando o `AGENTS.md` até a **raiz do projeto**. Eles reconhecem
a raiz por um `.git`. Quando o desenho foi feito, o hub não tinha `.git`. Então o kit ia criar um arquivo vazio na raiz
do hub, o **marcador**, e configurar o Codex para tratar esse arquivo como sinal de raiz. Sem isso, um Codex aberto numa
subpasta não leria o contrato da raiz.

**O que mudou.** Depois ficou decidido que cada máquina do par tem um `.git` na raiz do hub (a cópia de segurança diária
no GitHub). E o teste mostrou que, com esse `.git`, o Codex e o Copilot já chegam ao `AGENTS.md` da raiz quando abertos
numa subpasta ou na pasta de um papel, sem marcador nenhum.

**A pergunta:** o kit ainda cria o marcador?

## O marcador de raiz
id: marcador
tipo: escolha
recomendada: A

- A: Não cria mais: o `.git` da raiz já faz o papel do marcador, e o kit fica com uma peça a menos
- B: Cria assim mesmo, junto com o `.git`, como garantia caso um dia o `.git` saia da raiz ou uma máquina fique sem ele

## Algo mais?
id: algo-mais
tipo: texto
