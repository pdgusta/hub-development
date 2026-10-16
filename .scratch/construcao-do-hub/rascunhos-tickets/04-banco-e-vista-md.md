# Banco e vista .md

Type: task
Status: ready-for-agent
Dono: Worker 4
Com: Prumo
Blocked by:

Faixa 4 da spec (`../spec.md`, seção "Faixas", Worker 4). Fatia vertical: entrega funcionando de ponta a ponta no hub
de ensaio e no HOME de ensaio, sem esperar as outras faixas.

## O que construir

**Banco e vista `.md`** (faixa 4 do corte; tickets 25, 33, 34, 47, 48 e comentários de 2026-10-13 e 2026-10-14 do 16): par A e par B de ensaio nesta máquina, cada um com o seu CouchDB (`kit/par/banco/compose.yml`, `couchdb.ini`, `.env.modelo`, portas em 127.0.0.1) e replicação contínua nos dois sentidos (S3); o sincronizador é o CLI do LiveSync (build do commit `14141446` do ticket 48, sem recompilar) configurado pelo caminho dos testes oficiais, um dispositivo por par aceito com `mark-resolved`, **E2EE com caminho ofuscado** (ticket 34), `syncMaxSizeInMB` 200, exclusão de tudo que começa com ponto em qualquer nível; roda em laço no terminal e a tarefa agendada sai como XML

## Critério de aceite (de ponta a ponta)

seis testes automáticos: (1) nota criada na pasta A aparece na B, e a editada na B volta à A, em até 30 s; (2) nenhum texto claro nos documentos crus do CouchDB; (3) `.oculto/x.md`, `.env`, `projeto/.git/config` e `projeto/.venv/x` não chegam ao banco (o aninhado é o defeito 8 do ticket 48: se não fechar, sai teste vermelho documentado e a parte vira candidata a Fable); (4) 60 MiB viaja, 201 MiB não; (5) a mesma linha editada nos dois pares com a replicação pausada vira `_conflicts` nos dois CouchDB, sem versão perdida; (6) retrato do banco de ensaio com um conflito aberto e um binário com ramo apagado, em `execucao/ensaio/banco/`, para as faixas 5 e 7

## Como segue sem esperar

nada para começar. Entrega cedo aos outros: no minuto 0–10, o `compose.yml` e o `.env.modelo` do banco (fronteira "Banco de ensaio" abaixo); até lá, as faixas 5 e 7 sobem a imagem oficial com os mesmos nomes. O hub de ensaio (Worker 2) serve de conteúdo das pastas A e B

## Regras

- Ramo e pasta próprios (git worktree) do repositório do hub em `C:\context-hub`; nada global de verdade sem o aval do
  Gustavo (HOME de ensaio); a execução inteira dura 1 hora: o que não couber vai para "Fica para outra execução" no plano.
- Até 10 subagentes; parte muito complexa: um subagente Fable 5.1 médio.
- Antes de juntar: revisão do Prumo (decisões) e do Prumo 2 (construção).
- Erro achado na spec: corrija a spec na sua faixa.

## Comments
