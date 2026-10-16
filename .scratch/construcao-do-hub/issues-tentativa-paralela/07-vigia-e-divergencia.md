# 07: Vigia e divergência

Type: task
Status: ready-for-agent
Dono: Worker 7
Com: Prumo 2
Blocked by: None (can start immediately)

Faixa 7 da spec (`../spec.md`, seção "Faixas", Worker 7). Fatia vertical: entrega funcionando de ponta a ponta no hub
de ensaio e no HOME de ensaio, sem esperar as outras faixas.

## O que construir

**Vigia e divergência** (faixa 7 do corte; Answers dos tickets 33 "Aviso" e "Divergência", 08, 14 "Checagem de início" e "Estado da vigia na tela", 34 "Segurança"), em `agents/vigia/` (Node ≥ 22, `.mjs`, como as faixas 6 e 9; `livesync-commonlib` para decifrar, como no ticket 09): (a) `vigia passada`: uma passada lê o CouchDB local (`_scheduler/docs`; conflitos abertos; ramo apagado de binário pela resolução por `mtime`), o disco (arquivo acima de 200 MiB), se o sincronizador está vivo e se o outro par responde; com E2EE, decifra o caminho com a frase-senha do `.env`; grava `estado.json` por troca atômica; (b) notificação do Windows **só quando o estado piora** em relação à passada anterior; (c) `vigia recuperar <caminho>` grava a versão perdida do binário num arquivo ao lado; (d) `hooks/07-vigia/`: hook de início de sessão nos três harnesses que injeta o resumo (com o outro par desligado, só a hora da última troca), o programa do `notify` do Codex, o script de `statusLine` do Copilot e `mods/07-vigia/` (Claude Code, estado o tempo todo); (e) a tarefa agendada de 5 min como XML e `kit/par/07-vigia.ps1` só com `-WhatIf` (registrar é `ready-for-human`); na hora, a vigia roda em laço no terminal; (f) se couber: Config Doctor travando o plugin

## Critério de aceite (de ponta a ponta)

- [ ] `node --test` com um CouchDB dublê (respostas gravadas) e o disco do hub de ensaio, oito cenários dão o `estado.json` esperado: tudo em ordem; conflito de texto; binário descartado; replicação parada há mais de 15 min com o outro par ligado (`divergencia`); outro par desligado (`informa`, com a hora da última troca); arquivo de 201 MiB (`fsutil file createnew`, rápido); sincronizador parado; item `copia_diaria` da faixa 10. A notificação sai só na passada que piora (notificador dublê; uma real à vista do Gustavo, se ele quiser). `vigia recuperar` devolve os bytes do ramo apagado. Ponta a ponta no CouchDB de ensaio (porta 5997, com E2EE): no retrato da faixa 4, a vigia acusa o conflito e o binário **pelo caminho decifrado**; o hook de início, rodado com a entrada JSON de cada harness, devolve o resumo; o mod e a `statusLine` mostram o estado de um arquivo de exemplo

## Como segue sem esperar

banco (faixa 4): uso o `.env.modelo` e as portas do Worker 4 desde o minuto 0; até o retrato do item 6 chegar, forjo o conflito e o ramo apagado no meu CouchDB (5997) pela API e começo sem E2EE, ligando a frase-senha antes do fim. Outro par: `HUB_OUTRO_PAR_URL` (no ensaio, o CouchDB B do Worker 4 ou um dublê parado). Kit (faixa 8): entrego `hooks/07-vigia/fragmento.json` no minuto 15, no formato do Worker 8, e o kit liga o `notify` do Codex ao meu programa. Faixa 2: hook de início próprio, separado do da nota. Faixa 10: só leio o item `copia_diaria`. Não espero ninguém

## Regras

- Ramo e pasta próprios (git worktree) do repositório do hub em `C:\context-hub`; nada global de verdade sem o aval do
  Gustavo (HOME de ensaio); a execução inteira dura 1 hora: o que não couber vai para "Fica para outra execução" no plano.
- Até 10 subagentes; parte muito complexa: um subagente Fable 5.1 médio.
- Antes de juntar: revisão do Prumo (decisões) e do Prumo 2 (construção).
- Erro achado na spec: corrija a spec na sua faixa.

## Comments

- 2026-10-15 ~22h, Worker 7: **parado pelo limite de uso da sessão.** Ramo `faixa-07` (worktree `C:\context-hub-wt\faixa-07`),
  commit com o contrato comum (`agents/skills/vigia/CONTRATO.md`: layout, variáveis, esquema do `estado.json`), o dublê
  HTTP do CouchDB (`test/apoio/couchdb-duble.mjs`). Os três subagentes (telas, aviso e kit, E2EE) foram parados antes
  de gravar qualquer arquivo. Nenhum teste rodou. Falta tudo do critério de aceite: o núcleo `vigia passada`/`recuperar` em TDD (oito
  cenários), hooks, `notify`, `statusLine`, mod, notificação, kit e E2EE; depois a revisão do Prumo 2. Desenho do núcleo: replicação parada
  medida pela própria vigia entre passadas (memória em `.local/vigia/`), binário descartado = `_deleted_conflicts` em
  arquivo que não é `.md`/`.txt`/`.csv`, sincronizador vivo pela linha de comando dos processos, entradas da faixa 10 em
  `.local/vigia/entradas/`.
