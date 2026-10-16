# 02: Retomada e checkpoint

Type: task
Status: claimed
Dono: Worker 2
Com: Prumo
Blocked by: None (can start immediately)

Faixa 2 da spec (`../spec.md`, seção "Faixas", Worker 2). Fatia vertical: entrega funcionando de ponta a ponta no hub
de ensaio e no HOME de ensaio, sem esperar as outras faixas.

## O que construir

Retomada e checkpoint (ticket 10): nota de retomada de sete campos por trabalho, hook de fim de resposta que a grava e leva ao hub o que só a memória privada sabe, checagem de início de sessão que a abre

## Critério de aceite (de ponta a ponta)

- [ ] numa sessão `claude -p` com HOME de ensaio, aberta numa iniciativa do hub de ensaio: o fim da resposta deixa `retomada.md` com os sete campos; a sessão seguinte começa com a nota no contexto; teste automatizado dos dois hooks

## Como segue sem esperar

o esqueleto de pastas (faixa 1): usa a forma decidida no ticket 12 sobre o hub de ensaio pronto antes da hora; o instalador segue o contrato do kit (faixa 8)

## Regras

- Ramo e pasta próprios (git worktree) do repositório do hub em `C:\context-hub`; nada global de verdade sem o aval do
  Gustavo (HOME de ensaio); a execução inteira dura 1 hora: o que não couber vai para "Fica para outra execução" no plano.
- Até 10 subagentes; parte muito complexa: um subagente Fable 5.1 médio.
- Antes de juntar: revisão do Prumo (decisões) e do Prumo 2 (construção).
- Erro achado na spec: corrija a spec na sua faixa.

## Comments
- 2026-10-15 21:58, Worker 2 (parada pedida pelo Gustavo às 21:56): **construção interrompida no começo.** Ramo
  `faixa-02` (worktree `C:\context-hub-wt\faixa-02`, a partir de `integracao` 69cb383), nada juntado em `integracao`.
  - Feito: só os testes (fase vermelha do tdd), sem implementação: `hooks/02-retomada/testes/apoio.mjs` (hub de ensaio
    descartável em `%TEMP%`, nota de sete campos, chamada dos hooks com evento na entrada padrão) e
    `hooks/02-retomada/testes/fim.test.mjs` (fim da resposta nos três harnesses: fora do hub calado; trabalho mudado sem
    nota devolve com os sete campos; nota tocada solta; só conversa solta; `stop_hook_active` solta; raiz do hub solta;
    subpasta da iniciativa; `workingDirectory` da extensão do Copilot; pasta com ponto não conta).
  - Achado: rodar `node --test` no arquivo travou (passou de 120 s) porque `fim.mjs` não existe e `spawnSync` sem
    timeout; pôr `timeout` no `rodar()` antes de seguir.
  - Falta: `fim.mjs`, `inicio.mjs` e a biblioteca comum; o mod `mods/02-retomada/` (pode chamar `node fim.mjs` por
    `$.process.run`, que a API de mods tem); a extensão `extensoes-copilot/02-retomada/`; `fragmento.json`;
    `regra-contrato.md`; os testes do início; `agents/test/02-retomada.ps1`; a prova ao vivo com
    `claude -p --plugin-dir`.
  - Base para retomar: a bancada do ticket 14 (`C:\Projetos\bancada-acesso\`: `scripts/fim.py`, `scripts/inicio.py`,
    `mods/fim-retomada/`, `extensoes-copilot/fim-retomada/`).
