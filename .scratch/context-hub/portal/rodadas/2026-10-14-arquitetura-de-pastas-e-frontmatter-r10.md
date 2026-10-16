---
titulo: O núcleo e os modelos da pasta de uma iniciativa
ticket: 12
aberta: 2026-10-14
estado: suspensa
carta: prototipo-12-blocos
---

Esta rodada substitui a anterior ("O que é igual em toda pasta de iniciativa", suspensa) e atende ao seu comentário
na carta "Miolo da iniciativa": melhorar o núcleo e os modelos, e trocar a opção B, que você descartou.

O que suas pastas reais mostram: os tipos se **misturam**. O SOC STRATA é operação (casos, consultas), mas tem uma
base de conhecimento (`kb/`) e um backlog de melhorias. O `context-hub` é planejamento (tickets, decisões, glossário)
com pesquisa (anexos). A VOEGOL é entrega a cliente com scripts.

Já decidido em outros tickets, fora desta rodada: `_archive/` uma vez em cada raiz; `maestro/` só quando usada; o
código fica no repositório próprio, fora do hub.

## O que vai no núcleo, igual em toda iniciativa
id: nucleo
tipo: varias
recomendada: retomada, agents

- retomada: `retomada.md`, com onde o trabalho parou e o próximo passo (o "Contrato file-first" exige um lugar fixo)
- agents: `AGENTS.md` da iniciativa, com o que ela é, onde está o quê e como trabalhar nela, mais a ficha no topo (cliente, raiz, ativa ou pausada); o agente o lê sozinho ao abrir a sessão na pasta, como o `AGENTS.md` deste repositório
- readme: `README.md` separado, só com a ficha (cliente, raiz, ativa ou pausada)
- decisoes: `decisions.md`, o registro das decisões da iniciativa (como o `classification-decisions.md` do SOC)
- glossario: `GLOSSARY.md`, os termos próprios da iniciativa

Por que retomada e agents: são os dois arquivos que um agente precisa ao chegar, sem procurar. A ficha cabe no
topo do `AGENTS.md`, então um `README.md` à parte repetiria. Decisões e glossário não servem a toda iniciativa
(um spike curto não precisa deles); viram blocos da pergunta seguinte.

Conferido: o Claude Code lê o `AGENTS.md` da pasta onde a sessão abre e o das pastas de cima ("Portas de entrada do
hub"). **Não verificado com o hub:** o Codex e o Copilot lerem o `AGENTS.md` de uma subpasta.

## Como o resto da pasta se monta
id: modelos
tipo: escolha
recomendada: B

- A: Um modelo pronto por tipo, escolhido ao criar: cliente com entregas, operação contínua, produto com código, frente de planejamento, pesquisa ou spike, referência
- B: Blocos combináveis do acervo, escolhidos ao criar e somados depois: entregas (`inputs/`, `deliverables/`, `meetings/`), planejamento (`issues/`, `decisions.md`, `GLOSSARY.md`), operação (`runbooks/`, `cases/`, `queries/`), conhecimento (`kb/`), pesquisa (`sources/`, `results/`), código (`code.md` com o link do repositório)
- C: Só o núcleo; cada iniciativa cria as subpastas quando precisar, sem acervo

Exemplos com a opção B:
- SOC STRATA = operação + conhecimento + planejamento;
- `context-hub` = planejamento + pesquisa;
- uma frente da VOEGOL = entregas + código.

Por que B: com um modelo por tipo (A), uma iniciativa mista escolhe um tipo e improvisa o resto, ou o acervo
precisa de um modelo para cada mistura. Com blocos, cada pasta junta só o que usa, e um bloco novo entra quando a
iniciativa muda (um spike que vira produto ganha planejamento e código). Os nomes das subpastas de cada bloco ficam
para a rodada seguinte.

## Algo mais?
id: algo-mais
tipo: texto
