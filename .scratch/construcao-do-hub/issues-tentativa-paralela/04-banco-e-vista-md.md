# 04: Banco e vista .md

Type: task
Status: claimed
Dono: Worker 4
Com: Prumo
Blocked by: None (can start immediately)

Faixa 4 da spec (`../spec.md`, seção "Faixas", Worker 4). Fatia vertical: entrega funcionando de ponta a ponta no hub
de ensaio e no HOME de ensaio, sem esperar as outras faixas.

## O que construir

**Banco e vista `.md`** (faixa 4 do corte; tickets 25, 33, 34, 47, 48 e comentários de 2026-10-13 e 2026-10-14 do 16): par A e par B de ensaio nesta máquina, cada um com o seu CouchDB 3.5.2 (contêineres `hub-ensaio-04-a` e `-b`, portas 5994 e 5995 em 127.0.0.1, usuário e senha de ensaio gerados, nada copiado do spike) e uma replicação de envio em cada um (S3); o sincronizador é o CLI do LiveSync (build do commit `14141446` do spike, sem recompilar), configurado pelo caminho dos testes oficiais (`init-settings`, `remote-add`), um dispositivo por par aceito com `mark-resolved`, **E2EE com caminho ofuscado** (34), `syncMaxSizeInMB` 200, exclusão de tudo que tem ponto em qualquer nível pelo `.livesync/ignore` (linhas `.*` e `.*/`; ver fronteira da volta 2); roda em laço no terminal, e a tarefa agendada sai como XML. Tudo sobe por `kit/par/04-banco.ps1`. Caminhos da faixa: `kit/par/banco/**`, `kit/par/04-banco.ps1`, `kit/par/env/04.env`, `agents/test/04-banco.ps1`, `execucao/ensaio/banco/`

## Critério de aceite (de ponta a ponta)

- [ ] prova: `pwsh agents/test/04-banco.ps1`, em ordem de corte. **Núcleo (min 0–35):** (N1) o kit sobe os dois CouchDB e as duas replicações, e o `_scheduler/docs` de cada um mostra a sua em `running`; (N2) nota criada na pasta A aparece na B, e a editada na B volta à A, em até 30 s, sem texto claro nos documentos crus do CouchDB; (N3) a mesma linha editada nos dois pares com a replicação pausada vira `_conflicts` nos dois CouchDB, sem versão perdida; (N4) `.oculto/x.md`, `.env`, `projeto/.git/config`, `projeto/.venv/x` e `projeto/.secrets/x` não chegam ao banco, com o CLI rodando **e** na varredura de partida depois de reiniciá-lo. **Se sobrar (min 35–50), nesta ordem:** (S1) 60 MiB viaja, 201 MiB não; (S2) colisão de binário deixa a perdida num ramo apagado; (S3) o kit roda de novo sem mudar nada e o `-WhatIf` não grava; (S4) CLI morto e CouchDB fora na partida: o laço religa; (S5) retrato do banco de ensaio (conflito aberto, binário com ramo apagado, `_scheduler/docs` parado) em `execucao/ensaio/banco/`, para as faixas 5 e 7 na próxima execução; (S6) `claude -p` grava na pasta A e chega à B (só com o login de ensaio)

## Como segue sem esperar

nada para começar. Entrega cedo: no min 0–10, `kit/par/banco/compose.yml` e `kit/par/env/04.env` (fronteira "Banco de ensaio"); no min 15, `execucao/ensaio/banco/scheduler-docs-em-dia.json` e `scheduler-docs-parado.json` tirados do CouchDB de ensaio (pedidos dos Workers 10 e 7), que até lá usam os seus dublês. O hub de ensaio (Worker 2) é o conteúdo das pastas A e B. Fronteiras no plano (`../planejamento/plano.md`): "Worker 4 (volta 1)" e "Worker 4 (volta 2)".

## Regras

- Ramo e pasta próprios (git worktree) do repositório do hub em `C:\context-hub`; nada global de verdade sem o aval do
  Gustavo (HOME de ensaio); a execução inteira dura 1 hora: o que não couber vai para "Fica para outra execução" no plano.
- Até 10 subagentes; parte muito complexa: um subagente Fable 5.1 médio.
- Antes de juntar: revisão do Prumo (decisões) e do Prumo 2 (construção).
- Erro achado na spec: corrija a spec na sua faixa.

## Comments
