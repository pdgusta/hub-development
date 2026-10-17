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
| 2 | 51 MiB viaja (60 na primeira versão; baixado pela memória da máquina, maestro 05h20); 201 MiB não viaja, não entra no banco e fica identificável | PENDENTE: roda como evidência numa hora de máquina quieta, combinada pelo maestro; o Fiel fecha a rodada com ela (o código não muda por ela; maestro, 2026-10-17) |
| 3 | colisão de binário: a mais nova nas duas pastas; a perdida num ramo apagado, recuperada byte a byte antes e depois da compactação | verde (06h20, 10 PASSA: a base chegou em 33 s; a mais nova nas duas pastas em 6 s; ramo apagado nos dois bancos; recuperada byte a byte antes e depois da compactação). A 1ª tentativa (05h25) caiu na base gravada direto no hub |
| 4 | conflito de texto aberto; retrato em dia | verde (06h24, 5 PASSA) |
| 5 | o kit de novo não muda nada (arquivos do kit, contêiner, replicação, PID) | verde (06h26, 5 PASSA: os dois pares) |
| 6 | laço: nada caído, nada a fazer; CLI morto; CLI morto e CouchDB fora; nada se perde | verde (06h27, 8 PASSA: CLI religado; CouchDB e CLI religados e o sync retoma nos dois sentidos em 4 s) |
| 7 | retrato com a replicação parada | verde (06h39, 4 PASSA) |
| 07 | o teste do 07 (o passo do kit ganhou o passo da tarefa) | verde (06h39, 24 PASSA) |

A primeira rodada (todas as fatias, 03h37) foi parada pelo Claude Code por falta de memória na máquina aos 18 min, na
fatia 2. Limpei o daemon pelo PID, os contêineres, a pasta e a trava.

A segunda tentativa da fatia 2 (05h11, destacada) foi cortada pelo próprio corredor: a memória livre caiu de 2.900 para
513 MB em um minuto, com o arquivo de 60 MiB indo aos dois bancos. O Docker roda no WSL (`vmmemWSL`), que cresce com a
carga. O maestro decidiu: fatias 3 a 7 e o teste do 07 antes; a 2 por último, com 51 MiB, numa hora de máquina quieta.

Retrato gravado em `agents/code/test/banco/retrato/` (b02fa4f), com um README: binário com ramo apagado, conflito
aberto, `_scheduler/docs` em dia e parado. Sem senha, frase nem sal.

O corredor (`.local/fatias.ps1` na worktree) tem cópia em `etapas/logs/08-corredor-fatias.ps1`.

## Estado para a revisão

- Ponta `124f43d`: `integracao` 9cc878b (ticket 10 e 36) juntada sobre b02fa4f. Depois da junção, sem Docker: `kit-sem-docker.ps1` tudo passou.
- A fatia 2 fica pendente por decisão do maestro: a revisão começa sem ela, e ela entra como evidência quando a máquina estiver quieta.

## Não verificado

- Registrar a tarefa de verdade (regra: nada global). O XML foi validado pelo Agendador sem registrar.
- Se o Agendador mata o CLI quando a volta do laço termina: o CLI sobe por `cmd /c` como processo filho. Conferir no
  primeiro registro de verdade.

## Rodada 2 (consertos do parecer r1, `etapas/parecer-08-Brasa.md`)

Ponta `514db7a`.

1. **`Get-AcimaDoLimite`**:
   - Lê a raiz na forma longa e sem barra no fim (`realpathSync.native`), a mesma forma do `FullName` dos arquivos. O
     relativo sai por `GetRelativePath`.
   - Tira as pastas locais pela mesma regra do gerador (`agents/code/bin/lib/locais.mjs`), só lendo. O gerador grava
     as listas e pediria religar o CLI.
   - Casos novos no `kit-sem-docker.ps1`, primeiro vermelhos e depois verdes: 201 MiB numa pasta local não entra; o
     caminho certo com o hub terminando em barra; o caminho certo pelo nome curto do Windows.
   - `kit-sem-docker.ps1`: tudo passou. `integracao` em dia (9cc878b).

As ressalvas ficam como estão no parecer. Fatias 1 e 2 (Docker): com o Fiel, na hora quieta.

### Fatias 1 e 2 na hora quieta (07h37, 1ª tentativa)

Cortada pelo corredor às 07h39: a memória livre caiu de 3.183 para 621 MB ainda na subida dos pares (2 PASSA: o passo
sobe o par A). Limpo: nenhum contêiner, nenhuma pasta. Depois da limpeza, 881 MB livres, com a `vmmemWSL` segurando
2,1 GB (o WSL não devolve a memória ao Windows sozinho). Log: `etapas/logs/08-fatias-1-2.log`.

**Decisão do maestro (07h45):** a fatia 2 não roda de novo hoje. Ela derruba a máquina na subida dos pares mesmo com
3 GB livres. Vira item para o Gustavo, de dia, com menos agentes abertos ou com a memória do Docker ajustada por ele. A
revisão fecha com a fatia 2 pendente, por escrito:

- tentativa de 05h11: com 60 MiB, de 2.900 para 513 MB livres em 1 min;
- tentativa de 07h37: fatias 1+2, de 3.183 para 621 MB em 2 min, ainda na subida dos pares;
- a `vmmemWSL` ficou com 2,1 GB depois, até o `wsl --shutdown`.

A fatia 1 também não rerodou depois das junções. O último verde dela é o de 03h37.
