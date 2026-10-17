# 08: Banco: limites e robustez

Type: task
Status: claimed
Etapa: 2 (banco)
Blocked by: 07, 06

**What to build:** O banco aguenta o uso real: exclusões pela lista do gerador, limite de 200 MiB, colisão de binário recuperável, kit idempotente, laço que religa o sincronizador, e um retrato do banco (conflito aberto, binário com ramo apagado, replicação parada) para as etapas seguintes.

**Fonte:** Bloco do Worker 4 (os itens que eram "se sobrar" voltam a ser entrega cheia); tickets 33, 47, 48. Regras comuns: `../etapas/regras-da-construcao.md`.

**Blocked by:** 07 (Banco do par: dois CouchDB, LiveSync e vista `.md`), 06 (Gerador de exclusões)

- [ ] nada com ponto nem `local: true` chega ao banco, com o CLI rodando e na partida
- [ ] arquivo de 60 MiB viaja e o de 201 MiB não
- [ ] colisão de binário deixa a versão perdida num ramo recuperável
- [ ] o kit roda de novo sem mudar nada; com o CLI morto ou o banco fora na partida, o laço religa
- [ ] o retrato do banco está gravado para as etapas 3 e 6

## Comments
- 2026-10-17 03h00 (integrador, Rebite): lição do 07 (parecer do Fiel, `etapas/02-banco/parecer-Brasa.md`): as esperas fixas do teste do banco (30 s para o estado da replicação, 60 s para o controle) falham com a máquina carregada; esperar pelo estado, com folga maior, ou dizer na falha que foi tempo.
- 2026-10-17 ~03h10, Brasa: peguei (Status claimed). Worktree `C:/context-hub-wt/ticket-08`, ramo `ticket-08`, de `integracao` 763813a. Costuras propostas ao maestro (aguardo): (1) teste Docker `agents/code/test/08-banco-limites.test.ps1` pelo passo do kit, pastas e CouchDB crus (ponto e local na partida e rodando; 60/201 MiB; colisão de binário recuperada pelo cat-rev; kit de novo sem mudança); (2) laço `agents/code/kit/par/banco/laco.ps1`, uma volta por chamada, mais o XML da tarefa agendada sem registrar; (3) retrato do banco, local a decidir (proposto `agents/code/test/banco/retrato/`). Falta: tudo.
- 2026-10-17 ~03h15 (maestro, via Brasa): costuras confirmadas. (1) teste Docker `agents/code/test/08-banco-limites.test.ps1`, com esperas pelo estado e falha que diz "tempo"; piso de memória e trava no Docker. (2) laço `agents/code/kit/par/banco/laco.ps1`, uma volta por chamada; o kit só escreve o XML da tarefa agendada, nunca registra. (3) retrato em `agents/code/test/banco/retrato/` (o `execucao/` da raiz é do plano antigo).
- 2026-10-17 ~03h40, Brasa: commits 5110f3f e 08ce7c7. Sem Docker verde (`kit-sem-docker.ps1`: XML da tarefa aceito pelo Agendador sem registrar; `Get-AcimaDoLimite`). Laço `kit/par/banco/laco.ps1` (`Invoke-VoltaLaco`). Teste Docker `08-banco-limites.test.ps1` com as 8 fatias escrito; recuperação do ramo apagado por cópia do banco + folha reaberta + `pull-rev` (o CLI recusa revisão apagada). Primeira rodada Docker na fila da trava (`.local/pesado.ps1`, log `.local/08-f1a.log`).
- 2026-10-17 ~04h00, Brasa: 1ª rodada Docker parada pelo sistema por falta de memória aos 18 min (limpei: daemon pelo PID, contêineres, pasta, trava). Até ali: fatia 1 (exclusões, partida e rodando) toda verde. Achado: gravar o arquivo de 60 MiB derrubou o observador do CLI (EBUSY no arquivo ainda sendo gravado) e o CLI saiu sozinho ("Exiting for systemd restart"): sem supervisor, o par para de sincronizar. O laço é esse supervisor; o teste agora faz o papel da tarefa enquanto espera (a54e4aa). Espero aval para rodar de novo.
- 03:59 (maestro): a 1ª rodada Docker do 08 caiu por falta de memória aos 18 min (fatia 1 verde). Aval: rodar destacado (Start-Process, log, PID na trava), uma fatia por vez, piso de 2 GB antes de cada uma, parar e limpar abaixo de ~700 MB livres.
- 2026-10-17 ~04h15, Brasa: teste por fatias (527e3ed). Corredor destacado `.local/fatias.ps1` (trava uma vez para a sequência, piso 2 GB antes de cada fatia, corte abaixo de 700 MB com limpeza; estado em `etapas/logs/08-fatias.status`). Fila (`etapas/fila-pesada.md`): espero o Cinzel soltar para rodar as fatias 2 a 7. Relatório começado: `etapas/relatorio-08-banco-limites.md` (achado do EBUSY e o laço como supervisor).
- 2026-10-17 05h06, Brasa: peguei a trava; corredor destacado PID 224528 com as fatias 2 a 7 e o teste do 07 (`.local/fatias.ps1`; estado em `etapas/logs/08-fatias.status`). Cede a trava ao primeiro da fila ao fim da fatia 2 (`.local/ceder`) e retoma.
- 2026-10-17 05h12, Brasa: fatia 2 cortada pelo corredor (513 MB livres um minuto depois do começo; de 2.900); limpo, trava solta, Trilho avisado. O Docker roda no WSL (vmmemWSL ~2,2 GB, cresce com a carga). Propus ao maestro: fatias 3 a 7 e o 07 primeiro, a 2 depois ou com 51 MiB. Voltei ao fim da fila.

- 05:16 (maestro, mandato): a fatia 2 (60 e 201 MiB) derrubou a memória livre de 2.900 para 513 MB (Docker no WSL cresce com o CouchDB cifrado). Decidido: fatias 3 a 7 e o teste do 07 primeiro; a fatia 2 por último, numa hora de máquina quieta (sem outro construtor com teste rodando), com o arquivo de 51 MiB no lugar do de 60 (prova o mesmo limite acima de 50); o de 201 MiB fica.
