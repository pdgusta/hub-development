---
titulo: Como revisar o spec da construção
ticket: 16
aberta: 2026-10-16
estado: absorvida
---

**O que ficou da execução de ontem** (15/10, das 21h50 às 22h20, parada a seu pedido). Dos 10 workers, 5 deixaram
commit no próprio ramo, todos parciais e nenhum com teste de ponta a ponta passando: o esqueleto (13 arquivos), a
retomada (testes ainda vermelhos), a busca (notas de ensaio e teste de aceite), a vigia (dublê do banco; parou por limite
de uso) e as skills (biblioteca comum dos hooks). Os outros 5 não chegaram a gravar commit. Nada foi juntado no ramo de
integração. Está tudo em `C:\context-hub`, nos ramos `faixa-01` a `faixa-10`, e nada é apagado até você decidir.

**O spec tem duas camadas.** O núcleo (`.scratch/construcao-do-hub/spec.md`, cerca de 170 linhas) traz o problema, a
solução, as decisões e os testes comuns, o que fica fora e 8 pontos abertos. As partes por faixa
(`spec-partes/`, 5 arquivos) somam 398 user stories. O spec foi escrito para "1 hora, 10 workers em paralelo", e a
revisão pode mudar esse formato também.

A rodada de ontem com os quatro avais (Docker, login, pilotos, teste de embedding) continua aberta e pode esperar: ela só
vale quando a construção recomeçar.

## Como revisamos o spec
id: modo
tipo: escolha
recomendada: A

- A: Em duas camadas: o núcleo com você, uma rodada por bloco, começando pelos pontos abertos e pelo formato da execução; as 398 user stories passam por um revisor que confere cada uma contra as decisões já fechadas no mapa e só traz a você as divergências (eu digo o custo do revisor antes de rodar)
- B: Você lê o spec inteiro e marca o que muda; eu transformo as marcas em rodadas
- C: Só o revisor confere tudo, núcleo e partes, contra as decisões fechadas, e você decide só as divergências

## Algo mais?
id: algo-mais
tipo: texto
