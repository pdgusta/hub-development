---
titulo: Busca: o teste único do gemini
ticket: 16
aberta: 2026-10-16
estado: aberta
---

A busca local entrou (ticket 12): o obsidian-hybrid-search com o modelo local (arctic) acha as notas do hub de ensaio
por palavra e por sentido, e o Claude e o Copilot de verdade já a usaram. Em "Busca" (ticket 09) ficou decidido que o
embedding do **gemini pelo FreeLLMAPI** fica **"configurado, testado uma vez, desligado"**: a configuração existe para
trocar de modelo um dia, mas não é usada.

O ticket 13 escreve essa configuração desligada e pede o seu aval para o **teste único**: indexar uma **cópia** do hub
de ensaio num **segundo índice** com o gemini, fazer as mesmas perguntas do aceite e gravar o resultado ao lado do
arctic. O hub de ensaio tem cerca de 18 notas com texto inventado, então são umas **25 chamadas** ao FreeLLMAPI (18 de
indexação e algumas perguntas). Antes de chamar, o Trilho confere o limite diário do provedor (`rpdLimit`) e o que já
foi gasto hoje, e para se o teste passar de um quarto do que resta (lição da bancada de 2026-10-13, que gastou o Google
do dia).

## O teste único do gemini
id: gemini-teste-unico
tipo: escolha
recomendada: A

- A: Liberado agora: umas 25 chamadas numa cópia do hub de ensaio (só texto inventado), com a cota conferida antes e parada se passar de um quarto do que resta no dia; o resultado fica no relatório e a configuração termina desligada
- B: Liberado, mas só amanhã cedo, com a cota do dia cheia
- C: Não testar agora: a configuração fica escrita e desligada, e o teste vira item do radar para quando a troca de modelo for considerada

## Algo mais?
id: algo-mais
tipo: texto
