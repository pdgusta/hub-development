---
titulo: O laço da construção
ticket: 16
aberta: 2026-10-15
estado: absorvida
carta: laco-construcao
---

A proposta inteira está em `.scratch/construcao-do-hub/laco-proposta.md`. O Designer está fazendo a carta
**"laco-construcao"** com o desenho do laço. Em resumo:

- **Três fases.** Você invoca `/to-spec`, os 2 Prumos revisam e você aprova. Você invoca `/to-tickets`: saem fatias
  verticais de até 1 hora cada, com papel dono e critério de aceite; os Prumos revisam o corte e você aprova. Você invoca
  `/implement-spec`: o maestro despacha em ondas até não sobrar ticket que um agente possa fazer.
- **Ticket feito** = passou pelos dois Prumos e pelo testador de aceite.
- **O hub nasce em `C:\context-hub`** (ticket "Windows ou WSL"). Cada construtor trabalha no seu ramo, em pasta
  própria. Nada global antes do seu aval: o que mexe em `~/.claude`, `~/.codex`, `~/.copilot`, hooks e serviços é
  testado num HOME de ensaio; a instalação de verdade, com cópia e hash, é ticket seu, como o notebook.
- **Fable 5.1 médio** quando um ticket estoura a 1 hora ou os Prumos o recusam duas vezes.
- **O painel** lê os eventos que hooks de projeto gravam (sem o agente lembrar); a execução não depende dele.
- **Conversas:** o maestro liga os recrutas entre si pela CLI (`maestri connect`), todos com todos; ninguém liga nada à mão.

## Como os 12 recrutas se dividem
id: papeis
tipo: escolha
recomendada: A

- A: 7 construtores (um ticket por vez, inteiro, com testes e até 10 subagentes), 1 integrador (fila, ordem dos bloqueios, ramos, junção, conflitos), 1 testador de aceite (roda o critério de cada ticket já junto com os outros), 1 pesquisador de fonte (confere em fonte primária o que o construtor vai usar) e os 2 Prumos (um revisa contra as decisões do hub, o outro revisa o código)
- B: 9 construtores e 1 integrador; os 2 Prumos fazem também o teste de aceite e a conferência de fonte. Mais mãos construindo, menos olhos separados
- C: 6 construtores, 1 integrador, 1 testador, 1 pesquisador e 1 guardião do ambiente (o HOME de ensaio, os serviços, a instalação de verdade), mais os 2 Prumos

## O limite de 1 hora vale para quê
id: hora
tipo: escolha
recomendada: A

- A: Por ticket: ao bater 60 minutos, o construtor para, grava o estado e devolve; o maestro divide o ticket ou o dá ao Fable
- B: Por volta do laço: cada volta dura até 1 hora; no fim dela todos gravam o estado, o maestro consolida e você vê o placar antes da próxima volta
- C: A execução inteira em 1 hora: o que não couber fica para outra execução

## Algo mais?
id: algo-mais
tipo: texto
