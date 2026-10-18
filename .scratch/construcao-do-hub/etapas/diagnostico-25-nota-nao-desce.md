# Diagnóstico: a nota gravada no par A não desce ao par B (25, intermitente)

Brasa, 2026-10-17 ~18h20, a pedido do maestro, com os dados da Vela. A leitura de logs e de código veio primeiro, e
depois a reprodução com Docker (18:23-18:47).

## Resultado da reprodução (18:23-18:47; vale mais que a hipótese abaixo)

**Causa:** a fila da semente, não uma replicação morta.
- Logo depois da subida dos pares, o daemon do B tem de escrever no disco a semente inteira do hub de ensaio: 523
  arquivos e 7 MB, quase todos de `agents/code/`. Ele escreve **cerca de 1 arquivo por segundo**, e uma nota nova entra
  na mesma fila.
- O 25 confere o B dentro dos primeiros 1-2 min da subida: 60 s na fase 2 e 120 s na base do conflito. Às vezes a nota
  fura a fila a tempo, às vezes não.
- A contínua do B partiu em todas as voltas. Não apareceu "Replication is already in progress" nem erro de conexão. O
  B estava sempre vivo e escrevendo. A hipótese da contínua que não parte (abaixo) não se confirmou.

Voltas (`etapas/logs/repro-25/live-182350/` e `live-183445/`; log `--verbose` dos dois CLIs, sem segredo):

| Volta | Nota no B (espera até 120 s) | Semente (`tasks.md`) no B | seq A = B | Tarefa `_replicator` | OOM |
|---|---|---|---|---|---|
| 1 | 109 s | não | 1956 = 1956 | running nos dois | não |
| 2 | 31 s | não | 1925 = 1925 | running | não |
| 3 | 87 s | sim | 1925 = 1925 | running | não |
| 4 | **não chegou** em 120 s | não | 1925 = 1925 | running | não |
| 5 (medida) | **não chegou** em 120 s | não | 2009 = 2009 | running | não |

- Os dois CouchDB ficam em dia na hora (seq igual). O atraso é só o daemon do B levando os documentos ao disco. Na
  volta 4, aos 120 s, o log do B mostrava 201 arquivos feitos e outros começando.
- Curva da volta 5 (desde a gravação da nota, logo depois da subida): B com 261 arquivos aos 121 s, 351 aos 183 s,
  451 aos 277 s e **524 aos 380 s**. Daí em diante não muda. Os 2 que faltam para os 526 do A são os da pasta local
  `initiatives/context-hub/labs/` (`local: true`), que não replicam. Ou seja, **a semente leva ~6,5 min para descer
  inteira**, com 2,5 GB livres. Com a máquina cheia, mais.
- Isso explica o quadro da Vela:
  - falhou quando a conferência veio logo depois de uma subida nova (14:06, 17:22, 18:09);
  - passou quando a subida já tinha alguns minutos (18:00, a fase 3 depois da fase 2);
  - passou também quando a nota furou a fila.
- O `--interval` não resolve: o atraso não é da replicação. Fica fora do conserto.

**Conserto (no 25, não no kit):**
- O `pares.ps1 subir` só devolve "subiu" depois de o B **convergir**. Convergir é ter os mesmos arquivos que replicam
  do A (sem os com ponto e sem as pastas locais, pela regra do gerador), com o mesmo hash.
- Espera de até 15 min, e o tempo gasto vai no JSON de saída (para o relatório).
- Com isso, as esperas de 60 e 120 s das fases voltam a medir só a nota nova. A fase 2 pode subir de 60 para 120 s,
  como as outras.
- Também: guardar os logs do CLI antes do `descer` quando uma conferência falha (a Vela já disse que fará).

**Para o kit (observação, não defeito):** um par novo leva minutos para receber o hub inteiro (~1 arquivo/s no daemon,
nesta máquina). A instalação do segundo par deveria dizer isso, ou esperar a convergência antes de dar o par por
pronto. Fica para o maestro decidir se vira ticket.

## Hipótese da leitura de código (antes da reprodução; não se confirmou)

## O que se viu (Vela)

| Volta | Subida dos pares | O que conferiu | Resultado |
|---|---|---|---|
| manhã | nova | fase 2 (Claude, Copilot) e fase 3 | desceu |
| 13:21 | nova | fase 4, base do conflito | desceu |
| 14:06 | nova (Docker recém-ligado) | fase 4, base do conflito | **não desceu** |
| 17:22 | nova | fase 4, base do conflito | **não desceu** |
| 18:00 | nova, depois do `wsl --shutdown` | fase 3, 1-2 min depois da fase 2 | desceu |
| 18:09 | nova, 4.736 MB livres | fase 2 do Codex | **não desceu**: `tasks.md` nem existe no B (`hash_b` null) |

- Quando falha, não chega nada. Nem a semente do hub (o `tasks.md` do `montar.mjs`, que o A sobe ao partir) chegou ao B
  na volta das 18:09.
- Não há log do CLI nem do CouchDB das voltas ruins: a pasta do ensaio e os contêineres somem no `descer`.

## A cadeia e o elo suspeito

A gravação desce assim: disco do A → o daemon do CLI do A (observa o disco e grava no banco local) → a replicação do
banco local do A ao CouchDB do A → a tarefa `_replicator` do A ao CouchDB do B → a replicação do daemon do B, do CouchDB
do B ao banco local dele → o disco do B.

No código do CLI (`src/apps/cli/commands/runCommand.ts` e o bundle `dist/index.cjs`, que vem da `livesync-commonlib`),
o `daemon` faz o seguinte:

1. Uma replicação única com o remoto ("Initial replication complete").
2. `applySettings()`. O ciclo de vida chama o `runAfterResume` (`src/serviceFeatures/replicationScheduling.ts:135`),
   que liga a replicação **contínua** (`startContinuous`).
3. Escreve "LiveSync active" logo depois, **sem esperar** a contínua partir. É esse o sinal de pronto do kit
   (`Start-Sincronizador`).

A contínua desiste calada em vários pontos, e ninguém a religa:

- No `runContinuousReplication` (`dist/index.cjs:~38719`):
  - outra replicação em curso: "Replication is already in progress", `return false`;
  - a replicação única de antes da contínua ("Before LiveSync, start OneShot once...") falha: `false`;
  - a conexão falha: "The connection to the remote has been prevented, or failed.", `false`;
  - `processSync` dá `FAILED`: `false`.
- Do lado de quem pede, `openReplication(setting, keepAlive=true)` não espera a tarefa (`dist/index.cjs:38102`). O
  `startContinuous` volta como "completo" mesmo quando a contínua desiste depois.
- No agendador, com `liveSync` ligado e `syncOnStart` desligado (o kit grava assim, `Initialize-Dispositivo`), o
  resultado que não completa só tira a "posse" da contínua (`replicationScheduling.ts:157-160`). Não há nova tentativa.
- O laço do kit (`Invoke-VoltaLaco`) religa o CLI só quando ele morre ou quando o banco é religado. Um daemon vivo sem a
  contínua passa por ele.

**Hipótese (falta prova):** numa subida, a contínua de um dos daemons (o do A ou o do B) não parte e fica desligada
até o fim. Ela não parte quando, no instante do `applySettings`, ainda há outra replicação em curso, ou quando o
CouchDB demora ou recusa.
- Isso combina com o "por subida": ou tudo desce, ou nada desce.
- Combina com a falta de mensagem: sem `--verbose`, esses avisos são de nível baixo.
- Combina com a carga: Docker recém-ligado, máquina cheia.
- No `pares subir`, o `docker update --memory 384m` vem logo depois dos daemons partirem, quando a contínua ainda pode
  estar se ligando. Isso pode apertar o CouchDB nesse instante.

**Hipóteses descartadas pelo caminho:**
- Caminho curto do Windows no `fs.watch` (Achados comuns): o 25 usa o caminho longo (`realpathSync.native`, linha 62).
- Espera curta só no teste: a semente não tinha chegado nem uns 3 minutos depois da subida.

## Reprodução (com a trava, depois da fase 7 da Vela)

O script é `etapas/logs/repro-25-desce.ps1` (fora do repositório).
- Ele sobe os pares como o `pares.ps1` (`novo` + `subir`, sem o MCP), com o daemon em `--verbose`. Depois de os
  pares ficarem de pé, aplica o limite de memória (`docker update --memory 384m`), como o `subir`.
- Grava uma nota no A logo depois da subida e mede quando ela chega ao B.
- Por volta, guarda em `etapas/logs/repro-25/<modo>-<hora>/volta-N/`: os logs do CLI do A e do B (sem segredo), o seq
  dos dois bancos, o estado da tarefa `_replicator`, o OOM e o RestartCount dos contêineres, e se a semente está no B.
- Comandos:
  - `pwsh -NoProfile -File etapas/logs/repro-25-desce.ps1 -Voltas 4`: o modo de hoje;
  - `... -Modo intervalo`: o candidato a conserto (abaixo).
- O que separa os elos:
  - seq do B atrás do do A, ou a tarefa fora de `running`: a replicação CouchDB→CouchDB;
  - os dois seq iguais e a nota fora do disco do B, sem "LiveSync begin"/"Replication activated" no log do B: a
    contínua do B;
  - o seq do A sem andar depois da gravação: o daemon do A (o observador ou a contínua dele).

## Conserto proposto antes da reprodução (superado pelo "Resultado da reprodução" no topo)

1. **Se for a contínua que não parte, trocar o modo do daemon no kit:** `daemon --interval <N>` (por exemplo, 5 s) no
   lugar da contínua do `liveSync`. Nesse modo (`runCommand.ts:96-138`), o próprio daemon replica a cada N segundos.
   Numa falha, ele espera mais (até 5 min) e se recupera sozinho ("Replication recovered"). O observador do disco segue
   ligado.
   - Custo: até N segundos de atraso por nota, e uma volta de replicação a cada N segundos.
   - O sinal de pronto do `Start-Sincronizador` passa a ser "Polling mode". O `liveSync` do settings fica desligado,
     para a contínua não partir junto.
   - É mudança no kit de produção: a mesma falha deixaria uma máquina real sem sincronizar até o daemon morrer. Decisão
     do maestro (o spec fixa só o daemon "sempre ligado", faixas 03-04, "Elos dentro de cada par").
2. **Alternativa sem trocar o modo:**
   - o laço do kit passa a conferir se o daemon segue sincronizando (uma nota-sonda na pasta com ponto não replica;
     seria preciso outra marca, ou ler o log `--verbose`) e o religa;
   - e/ou o kit espera "LiveSync begin"/"Replication activated" antes de dar o par por pronto, e religa o daemon se
     não vier.
   - É mais frágil (depende de texto de log) e não cobre uma contínua que caia depois.
3. **No 25, enquanto isso:**
   - o `pares.ps1` guarda os logs do CLI e o `docker logs` antes do `descer` quando uma conferência falha (a Vela já
     disse que fará);
   - o `docker update --memory` passa para antes do `Start-Sincronizador`, para não apertar o CouchDB no meio da
     partida.

## Fonte do `--interval` (conferido no CLI, `C:/Projetos/spike-livesync/livesync-src/src/apps/cli/`)

- `README.md:385`: "`--interval <N>`, `-i <N>`: (daemon only) Poll CouchDB every N seconds instead of using the
  `_changes` feed".
- `README.md:503-508`: o `daemon` leva o CouchDB ao disco "via the `_changes` feed (LiveSync mode, default) or periodic
  polling (`--interval N`)". O disco vai ao CouchDB "via chokidar file watching", nos dois modos.
- `commands/runCommand.ts:96-138`: com `--interval`, o daemon escreve "Polling mode: syncing every Ns".
  - A cada volta, chama `replicateUnattended` (replicação nos dois sentidos).
  - Numa falha, conta as seguidas e dobra a espera até 5 min ("Poll error (k consecutive)"). Ao voltar, escreve
    "Replication recovered" e reduz a espera.
  - Cada volta agenda a seguinte. Nada desliga a sondagem, salvo o fim do processo.
- `commands/runCommand.ts:50` e `serviceFeatures/replicationScheduling.ts:94,129`: o
  `setExternalPollingMode(true)` impede o agendador de ligar a contínua (`canRunResume` e `canRunPeriodic` exigem
  `!externalPolling`). Mesmo com `liveSync` no settings, a contínua não parte junto.
