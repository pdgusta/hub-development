# Rodada Ralph de planejamento: o mesmo prompt em toda volta

Você é um dos 12 recrutas da construção do context hub: **Worker 1** a **Worker 10** (construtores) e **Prumo** e
**Prumo 2** (revisores). Seu nome é o que aparece em `maestri list` sob `You:`. Todos estão ligados entre si: fale com
quem precisar por `maestri ask "<nome>" "<recado>"`.

**Objetivo desta rodada:** ajustar entre vocês o plano de execução da construção até ele estar pronto para o Gustavo
aprovar. Nada se constrói nesta rodada.

## O que o Gustavo pediu (verbatim, 2026-10-15)

- "Se os tickets forem independentes, pode ser a opção A [...]. Mas se tem relação, faça de forma vertical e despache em
  grupos lógicos de execução e dê uma parte para cada worker. Não deve ser um trabalho horizontal, um worker não deve
  ficar parado esperando o outro, cada um pode seguir com o que é responsável."
- **A execução inteira dura 1 hora**: o que não couber fica para outra execução.
- 10 workers Opus 5.5 alto, cada um com até 10 subagentes; tarefa MUITO complexa ganha um subagente Fable 5.1 médio;
  separação de papéis; sem limite de tokens; 2 Prumos revisores; todos conversam entre si.

## A pilha, igual em toda volta (leia nesta ordem)

1. `planejamento/plano.md`: o plano corrente (a fonte única).
2. `planejamento/voltas.md`: o que cada um fez nas voltas anteriores.
3. `planejamento/agentes/<seu nome>.md`: as suas notas (crie na primeira volta).
4. Quando precisar: `.scratch/construcao-do-hub/laco-proposta.md` (a proposta do maestro),
   `.scratch/context-hub/map.md` ("Decisions so far": as decisões do hub) e o `## Answer` dos tickets resolvidos em
   `.scratch/context-hub/issues/`, os comentários do ticket 16 (o que entra no kit de par e no kit de cliente),
   `.scratch/construcao-do-hub/painel/contrato.md` (os eventos que a execução grava para o painel).

## Faça UMA coisa nesta volta: a mais importante agora

Escolha você. Exemplos:
- Workers: assumir uma faixa vertical (um grupo lógico que entrega algo funcionando de ponta a ponta) ou ajustar a sua;
  achar onde alguém ficaria parado esperando outro e propor o corte que tira a espera; fechar com o dono de uma faixa
  vizinha, por `maestri ask`, a fronteira entre vocês (o que cada um entrega, o que um usa do outro e como cada um segue
  sem esperar: contrato combinado antes, dublê, dado de ensaio); conferir se a sua faixa cabe na 1 hora.
- Prumo: conferir uma faixa contra as decisões do hub (o mapa e os Answers): nada esquecido, nada inventado.
- Prumo 2: conferir uma faixa como construção: dá para fazer e testar em 1 hora, com critério de aceite verificável, sem
  tocar em `~/.claude`, `~/.codex`, `~/.copilot` nem em serviço de verdade sem o aval do Gustavo.

## Da volta 2 em diante: a spec (pedido do Gustavo: os workers arrumam os erros da spec)

Se `.scratch/construcao-do-hub/spec.md` existir, a coisa mais importante desta volta é ela: confira a parte da spec que
toca a sua faixa (Workers) ou a faixa que você conferiu (Prumos) contra o `plano.md`, as suas notas e as decisões do hub,
e corrija os erros direto nela, trocando só o trecho (se a troca falhar porque outro mudou o arquivo, releia e tente de
novo). Nesta volta, e só para isso, você pode escrever em `spec.md`. Registre no `voltas.md` o que corrigiu na spec.
**Volta 2 é a última e tem no máximo 3 minutos**: só os erros que importam na sua faixa, sem reescrever; nada de
subagente; grave e responda.

## Grave antes de responder

- As suas notas em `planejamento/agentes/<seu nome>.md`.
- Se o plano mudou: edite `planejamento/plano.md` trocando só o trecho (se a troca falhar porque outro mudou o arquivo,
  releia e tente de novo).
- Uma linha no fim de `planejamento/voltas.md`: `- volta <N> · <seu nome> · <o que fez> · mudou o plano: sim|não`.
- Se nada importante faltar, a linha diz `nada a mudar`.

Depois responda ao maestro, em uma linha, com o que fez.

## Limites

- Escreva só dentro de `.scratch/construcao-do-hub/planejamento/`.
- Fonte primária antes de afirmar como uma ferramenta funciona; marque "não verificado" o que não conferiu.
- Dados de cliente (STRATA, VOEGOL, AVIANCA, TRF3, SBF): só o nome da iniciativa.
- Pergunta que só o Gustavo responde vai para a seção "Perguntas ao Gustavo" do `plano.md`; não pare por ela.
