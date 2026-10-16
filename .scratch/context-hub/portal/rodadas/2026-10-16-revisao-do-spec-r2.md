---
titulo: Quem é o revisor das user stories
ticket: 16
aberta: 2026-10-16
estado: absorvida
---

O revisor fica no canvas, ligado só a mim, sem subagentes, para você ver o que ele faz. Ele lê o mapa de decisões e
confere uma parte do spec por vez (são 5 arquivos), abrindo um ticket resolvido só quando precisa tirar uma dúvida.
As divergências vão para um arquivo (`.scratch/construcao-do-hub/revisao/divergencias.md`), e eu as trago em rodadas.
Ele não muda o spec.

**Custo estimado** (não verificado): as 5 partes somam cerca de 190 KB, uns 55 mil tokens, e o mapa uns 8 mil. Com as
consultas aos tickets, devem ser algumas centenas de milhares de tokens de leitura, em cerca de 1 a 2 horas. Ontem uma
faixa parou por limite de uso do Claude, o que pesa na escolha do modelo.

Enquanto ele trabalha, você e eu fazemos o núcleo do spec.

## Quem revisa as user stories
id: revisor
tipo: escolha
recomendada: A

- A: Um recruta Codex (GPT 6.1 Sol, esforço médio), como era o Prumo: um modelo de outra família confere o que o Claude escreveu, e a cota do Claude fica para a construção
- B: Um recruta Claude Opus 5.5 com esforço médio: gasta a cota do Claude, a mesma que ontem bateu no limite
- C: Dois recrutas, um Codex e um Claude, cada um com metade das partes: termina na metade do tempo e gasta as duas cotas

## Algo mais?
id: algo-mais
tipo: texto
