# Retomada e checkpoint

Type: task
Status: ready-for-agent
Dono: Worker 2
Com: Prumo
Blocked by:

Faixa 2 da spec (`../spec.md`, seção "Faixas", Worker 2). Fatia vertical: entrega funcionando de ponta a ponta no hub
de ensaio e no HOME de ensaio, sem esperar as outras faixas.

## O que construir

Retomada e checkpoint (ticket 10): nota de retomada de sete campos por trabalho, hook de fim de resposta que a grava e leva ao hub o que só a memória privada sabe, checagem de início de sessão que a abre

## Critério de aceite (de ponta a ponta)

numa sessão `claude -p` com HOME de ensaio, aberta numa iniciativa do hub de ensaio: o fim da resposta deixa `retomada.md` com os sete campos; a sessão seguinte começa com a nota no contexto; teste automatizado dos dois hooks

## Como segue sem esperar

o esqueleto de pastas (faixa 1): usa a forma decidida no ticket 12 sobre o hub de ensaio pronto antes da hora; o instalador segue o contrato do kit (faixa 8)

## Regras

- Ramo e pasta próprios (git worktree) do repositório do hub em `C:\context-hub`; nada global de verdade sem o aval do
  Gustavo (HOME de ensaio); a execução inteira dura 1 hora: o que não couber vai para "Fica para outra execução" no plano.
- Até 10 subagentes; parte muito complexa: um subagente Fable 5.1 médio.
- Antes de juntar: revisão do Prumo (decisões) e do Prumo 2 (construção).
- Erro achado na spec: corrija a spec na sua faixa.

## Comments
