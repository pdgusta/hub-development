---
tipo: resposta
rodada: 2026-10-16-pastas-locais-depois-do-gerador
ticket: 16
enviada: 2026-10-16T20:38:21-03:00
envio: f3e5386f-cc9d-4ed1-958f-2653a407dafc
estado: lida
substitui:
---

# Resposta: Pastas locais: o que o gerador de exclusões deixou em aberto

## Como nasce uma pasta local
escolha: A, Por um script "nova pasta local" (skill em `agents/skills/`, como a "nova iniciativa"), que para o sincronizador, cria a pasta com o `index.md` `local: true`, roda o gerador e religa; o contrato manda usar o script, e criar à mão fica sujeito ao vazamento (a recomendada)

## Quem roda o gerador depois da instalação
escolha: A, A vigia, a cada passada (5 min): roda o gerador; se a lista mudou, religa o sincronizador e avisa; se o gerador recusar (YAML ilegível), vira item da vigia com o caminho; é a rede de segurança para `index.md` editado à mão (a recomendada)

## Pôr `local: true` numa pasta que já replicou
escolha: A, Um passo "tornar local" no mesmo script: para o sincronizador, gera a lista e apaga a pasta do banco pelo CLI do LiveSync, o que tira a cópia da outra máquina e mantém a desta; o 08 prova que a cópia desta máquina não é apagada junto (a recomendada)

## Como a pasta local sai do git
escolha: A, O mesmo gerador escreve `.git/info/exclude`, que vale só nesta máquina e não é versionado: cada máquina exclui as pastas locais dela, e o nome de uma pasta local não viaja para a outra nem para o GitHub (a recomendada)

## Algo mais?
em branco
