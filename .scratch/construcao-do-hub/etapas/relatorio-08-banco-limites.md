# Relatório do ticket 08: banco, limites e robustez

Brasa, 2026-10-17. Ramo `ticket-08`, worktree `C:/context-hub-wt/ticket-08`, de `integracao` 763813a.

## O que foi feito

### Costuras (confirmadas pelo maestro, ~03h15)

1. Teste de ponta a ponta com Docker: `agents/code/test/08-banco-limites.test.ps1`. Ele passa pelo passo do kit
   (`04-banco.ps1`), pelas duas pastas, pelos CouchDB crus e por um dispositivo leitor. As esperas são pelo estado, com
   folga, e a falha por espera diz "tempo esgotado em N s" (lição do 07). Roda por fatias (`-Fatias`), cada uma sobre
   a mesma subida dos dois pares.
2. O laço: `agents/code/kit/par/banco/laco.ps1`, uma volta por chamada. O kit só escreve o XML da tarefa agendada,
   nunca o registra.
3. O retrato do banco: `agents/code/test/banco/retrato/`.

### No kit (`agents/code/kit/par/banco/banco.psm1`)

- `Write-TarefaSincronizador`: escreve `<estado>/tarefa-sincronizador.xml`.
  - Gatilho no logon, repetido a cada minuto (`PT1M`), sem segunda instância (`IgnoreNew`), sem "reiniciar se falhar".
  - A ação é `pwsh -File laco.ps1 -EnvFile <par>.env`.
  - Só grava se mudou. Para registrar: `schtasks /create /tn <nome> /xml <arquivo>`, com o Gustavo.
  - Novo passo no `Install-ParBanco` (o `-WhatIf` só o lista).
- `Invoke-VoltaLaco` e `laco.ps1`: uma volta do laço.
  - Se o CouchDB não responde, religa (`compose up -d`).
  - Se o banco foi religado e o CLI está vivo, para o CLI, para ele retomar o feed.
  - Se o CLI não está vivo (pelo PID conferido), roda o gerador de exclusões e religa o CLI.
  - Nada caído: não faz nada. Registro em `<estado>/laco.log`.
- `Get-AcimaDoLimite`: lista o que passa dos 200 MiB (`$script:LimiteMiB`, o mesmo do `syncMaxSizeInMB`), sem o que tem
  ponto. É para a vigia (faixa 7).

### No ensaio (`agents/code/test/banco/ensaio.psm1`)

- `Get-InfoNoBanco`: o `info` do CLI pelo leitor.
- `Get-FolhasCruas`, `Get-RamosApagados`: as folhas de um documento no CouchDB cru (`open_revs=all`).
- `Restore-RamoApagado`: recupera a versão perdida de um binário (ver "Achados").

## Achados

### O CLI sai quando o observador de arquivos cai (EBUSY)

Na primeira rodada, gravar o arquivo de 60 MiB derrubou o observador do CLI do par A:

```
(Notice) [CLIWatchAdapter] Fatal watcher error — file watching stopped:
(Notice) Error: EBUSY: resource busy or locked, watch '...\hub\anexos\sessenta.bin'
(Notice) [CLIWatchAdapter] Exiting for systemd restart.
```

- O `chokidar` tenta observar o arquivo enquanto ele ainda está sendo gravado. O Windows recusa (EBUSY).
- O CLI então sai de propósito, contando com um supervisor que o religue.
- Sem supervisor, o par para de sincronizar sem aviso. Na rodada, nem o arquivo de controle seguinte chegou ao B.
- Vai acontecer no uso: copiar um PDF ou um vídeo grande para o hub.
- **O laço é esse supervisor.** A tarefa agendada roda uma volta a cada minuto. O CLI morto é religado, e a varredura de
  partida sobe o que ficou para trás.
- No teste, a espera dos arquivos grandes faz o papel da tarefa: chama o laço a cada minuto (`Espera-ComLaco`). O que o
  laço fez sai no detalhe do caso.

### Colisão de binário: o CLI resolve sozinho, e a perdida fica num ramo apagado

- Pelo fonte do CLI (`src/serviceFeatures/conflictResolution/operations.ts`): para binário, ele compara o `mtime` e
  apaga a revisão mais velha, sem perguntar.
- O apagamento (`EntryManagerImpls.js`, `deleteDBEntryByPath` com `rev`) grava `_deleted: true` sobre o documento
  inteiro. A folha apagada guarda a lista de pedaços (como no ticket 48), e a compactação não a tira, porque é folha.
- O `pull-rev` do CLI recusa revisão apagada (`if (!source || source.deleted) return false`).
- A recuperação do ensaio não decifra nada:
  1. copia o banco para `<db>-recupera` no mesmo CouchDB (`_replicate`);
  2. reabre a folha apagada na cópia, com um PUT do mesmo corpo sem `_deleted`;
  3. grava o sal da E2EE na cópia (documento `_local` não replica);
  4. um leitor apontado para a cópia faz `sync` e `pull-rev` da revisão nova;
  5. apaga a cópia e o leitor.
- O comando de recuperar binário (faixa 7) pode seguir essa receita.
- Achados do Trilho no Docker do 16 (`relatorio-16-vigia.md`, Achados 4 a 6), aplicados aqui:
  - com o caminho ofuscado, `path`, `mtime` e a lista de pedaços vão cifrados no campo `path`, e o `children` em claro
    vem vazio. A folha apagada se reconhece pelo `path`, porque o toco de um DELETE comum não tem;
  - o `open_revs=all` responde em multipart sem `Accept: application/json`, e o `Invoke-RestMethod` devolve o array
    como um item só (o ensaio desenrola);
  - o JSON do `info` vem entre linhas de registro: o ensaio lê da linha `{` até a linha `}`.

## Testes

### Sem Docker (entra na suíte comum)

`pwsh -NoProfile -File agents/code/test/banco/kit-sem-docker.ps1`, chamado por `07-kit-sem-docker.test.mjs`: tudo
passou. Casos novos do 08:

- a tarefa: logon e a cada minuto; sem segunda instância e sem reiniciar se falhar; a ação é o laço com o `.env` do par;
- o Agendador aceita a definição: o COM `Schedule.Service`, com `NewTask(0).XmlText`, valida o XML sem registrar. Uma
  contraprova à mão (intervalo estragado) foi recusada;
- escrever de novo não muda o arquivo; nada registrado no Agendador;
- acima do limite: só o de 201 MiB que replicaria (arquivos esparsos; o de 200 MiB e o com ponto ficam de fora).

### Com Docker

Corredor destacado `.local/fatias.ps1` (aval do maestro, ~04h10):

- uma fatia por vez, com a trava;
- piso de 2 GB livres antes de cada fatia (20 min sem chegar, com a trava livre: para e avisa);
- abaixo de ~700 MB livres durante a fatia: para e limpa;
- saída em `etapas/logs/08-fatia-N.log`, estado em `etapas/logs/08-fatias.status`.

| Fatia | O que prova | Resultado |
|---|---|---|
| 1 | nada com ponto nem `local: true` chega ao banco, na varredura de partida e com o CLI rodando | verde (rodada 03h37, 14 PASSA) |
| 2 | 51 MiB viaja (60 na primeira versão; baixado pela memória da máquina, maestro 05h20); 201 MiB não viaja, não entra no banco e fica identificável | PREENCHER |
| 3 | colisão de binário: a mais nova nas duas pastas; a perdida num ramo apagado, recuperada byte a byte antes e depois da compactação | 1ª (05h25): vermelha, o binário de base não chegou (EBUSY provável); consertada em e0e0ecc; repetir |
| 4 | conflito de texto aberto; retrato em dia | PREENCHER |
| 5 | o kit de novo não muda nada (arquivos do kit, contêiner, replicação, PID) | PREENCHER |
| 6 | laço: nada caído, nada a fazer; CLI morto; CLI morto e CouchDB fora; nada se perde | PREENCHER |
| 7 | retrato com a replicação parada | PREENCHER |

A primeira rodada (todas as fatias, 03h37) foi parada pelo Claude Code por falta de memória na máquina aos 18 min, na
fatia 2. Limpei o daemon pelo PID, os contêineres, a pasta e a trava.

A segunda tentativa da fatia 2 (05h11, destacada) foi cortada pelo próprio corredor: a memória livre caiu de 2.900 para
513 MB em um minuto, com o arquivo de 60 MiB indo aos dois bancos. O Docker roda no WSL (`vmmemWSL`), que cresce com a
carga. O maestro decidiu: fatias 3 a 7 e o teste do 07 antes; a 2 por último, com 51 MiB, numa hora de máquina quieta.

## Não verificado

- Registrar a tarefa de verdade (regra: nada global). O XML foi validado pelo Agendador sem registrar.
- Se o Agendador mata o CLI quando a volta do laço termina: o CLI sobe por `cmd /c` como processo filho. Conferir no
  primeiro registro de verdade.
