# Parecer do ticket 08 (Brasa): banco, limites e robustez

## Rodada 1 — 2026-10-17 ~07h (ramo ticket-08, ponta 124f43d, com integracao 9cc878b)

Veredito: **VOLTA**, em acordo com o Fielzinho (troca 1), só pelo conserto 1. Fatias 1 e 2 (Docker, Fiel) na rodada 2
ou na hora quieta que o maestro marcar; a 2 não foi dispensada.

Leitura do Fielzinho (`parecer-08-Brasa-fielzinho.md`): PASSA de código, com 21 PASSA no `kit-sem-docker.ps1`; a
ressalva dele sobre `local: true` virou o conserto 1, com as sondas do Fiel. Ele acrescenta ao conserto: a raiz e o
`FullName` na mesma forma longa (o `GetRelativePath` sozinho não resolve o nome curto). Ressalvas dele aceitas: o
`Restore-RamoApagado` não apaga a cópia e o leitor num `finally`; o ciclo real do Agendador não foi provado.

### Conferido pelo Fiel

- Ramo contém `integracao` 9cc878b; árvore limpa.
- `node --test agents/code/test/07-kit-sem-docker.test.mjs`: 1/1. `kit-sem-docker.ps1` direto: tudo passou (17 casos,
  7 novos do 08: tarefa, Agendador aceita sem registrar, escrever de novo não muda, acima do limite, nada registrado).
- Logs Docker em `etapas/logs/`: fatias 3 (10 PASSA), 4 (5), 5 (5), 6 (8), 7 (4) e 07 (24), todos com saída 0,
  corredor em `08-fatias.status`. A fatia 1 tem log só na worktree (`.local/08-f1a.log`, 03h37, 14 PASSA), de antes
  das junções de integracao (o gerador de exclusões mudou no 28). Reroda junto com a fatia 2, na hora quieta
  (`-Fatias 1,2`, mesma subida).
- Limite: o CLI compara `syncMaxSizeInMB * 1024 * 1024 < size` (`livesync-commonlib`, `VaultService.isFileSizeTooLarge`);
  o kit usa `Length -gt 200 * 1MB`: igual.
- Laço (`Invoke-VoltaLaco`): CouchDB fora → `Start-CouchDBPar` (espera `_up`); CLI vivo com banco religado → para e
  religa; CLI morto (PID conferido pela linha de comando, 07) → gerador + `Start-Sincronizador`. Fatia 6 cobre os três.
- Retrato: 4 JSON + README, sem senha, frase nem sal; caminhos ofuscados. Ninguém o consome ainda (o 16 monta o dele).

### Consertos

1. **(Fiel) `Get-AcimaDoLimite` (`banco.psm1:276-281`): caminho relativo errado e pasta local listada.**
   - O relativo sai de `Substring((Resolve-Path $par.Vault).Path.Length + 1)`. Com o `HUB_ROOT` terminando em `\`, ou
     com nome curto do Windows (`GUSTAV~1.DEL`, que o `Resolve-Path` não expande e o `FullName` expande), o caminho
     sai cortado. Sonda: hub em `%TEMP%\...\hub-ensaio-08-sonda-fiel2\` com `anexos/video.bin` de 201 MiB →
     `nexos/video.bin`; hub pelo `$TEMP` curto → `el/clientes/rascunho/video.bin`.
   - Arquivo acima de 200 MiB dentro de pasta `local: true` é listado, mas não viaja de qualquer jeito (o gerador o
     exclui; sonda: `locais: ["clientes/rascunho"]` e a função lista `clientes/rascunho/video.bin`). A própria função
     já tira o que tem ponto pelo mesmo motivo. A vigia (faixa 7, ticket 16) vai listar isso como divergência falsa.
   - Conserto: raiz e `FullName` na mesma forma longa (sem barra no fim), e o relativo entre os dois (Fielzinho:
     trocar só o `Substring` mantém o nome curto divergente); tirar as pastas locais (as do gerador). Casos no
     `kit-sem-docker.ps1`: hub com barra no fim, hub pelo nome curto e 201 MiB numa pasta local.

### Ressalvas (não seguram o passa)

1. Cada religação apaga o registro do CLI que caiu (`Start-Sincronizador` remove `$par.Log` e `.err`): o motivo da
   queda (o EBUSY do relatório) some na volta seguinte do laço. Guardar o anterior (`.anterior`) ajudaria a vigia e o
   diagnóstico.
2. Falha do laço não vai ao `laco.log` (Docker ainda fora no logon: `Start-CouchDBPar` lança, a volta sai com erro,
   nada registrado). A tarefa repete a cada minuto, então religa quando o Docker subir; só o rastro falta.
3. Tarefa: `pwsh.exe -WindowStyle Hidden` disparado pelo Agendador com `InteractiveToken` costuma abrir e fechar uma
   janela de console (o console nasce antes do pwsh ler o argumento). A cada minuto, isso incomoda. Não verificado
   (nada registrado, regra); conferir no registro de verdade, com o "Agendador mata o CLI filho?" do relatório.
5. (Fielzinho) `Restore-RamoApagado` sem `finally`: um erro no meio deixa a cópia do banco e o leitor até a descida dos
   pares. Não promover à vigia sem limpeza garantida.
6. (Fielzinho) O XML validado não prova o ciclo real do Agendador nem se o CLI filho sobrevive ao fim do `laco.ps1`.
4. O retrato tira a frase e o sal: serve para a forma dos documentos, não para testar o decifrar do caminho. Quem
   precisar decifrar refaz com `-Fatias 3,4,7 -Manter`.

### Evidências

- Sondas do Fiel em `%TEMP%\hub-ensaio-08-sonda-fiel*` (apagadas).
- `git status` limpo depois.

### Fatia 2 (pendente)

Na hora quieta (maestro avisa): `-Fatias 1,2` com a trava, pelo Fiel; log `etapas/logs/revisao-08-r1-fatias-1-2.log`.

## Rodada 2 — 2026-10-17 07h30 (ponta 514db7a)

Veredito: **código PASSA em acordo com o Fielzinho (24 PASSA no kit-sem-docker dele, sem conserto novo); aceite final pendente das fatias 1 e 2 (Docker).**

- Conserto 1 feito (`banco.psm1`): raiz pelo `realpathSync.native` (forma longa, sem barra), relativo por
  `GetRelativePath`, pastas locais por `lib/locais.mjs` só lendo (index.md ilegível → erro, não lista calada).
- `kit-sem-docker.ps1` (Fiel): tudo passou, 3 casos novos (local, barra no fim, nome curto).
- Sondas da r1 de novo (hub pelo `$TEMP` curto e com barra no fim; 201 MiB em `clientes/rascunho/` local,
  `clientes/rascunho/sub/`, `clientes/rascunho-b/` irmã e `anexos/`): as duas formas dão
  `anexos/video.bin, clientes/rascunho-b/x.bin`. Certo. Sondas apagadas; `git status` limpo.
- Fila pesada (maestro): a fatia 2 é da Brasa, na hora quieta. Pedido: rodar `-Fatias 1,2` na mesma subida (a 1 de
  03h37 é anterior às junções; o gerador mudou no 28), log em `etapas/logs/`. O Fiel lê o log e fecha.

## Fechamento — 2026-10-17 ~08h10: **PASSA com ressalvas** (decisão do maestro sobre a fatia 2)

O maestro decidiu (via Brasa): a fatia 2 não roda de novo hoje e vira item para o Gustavo (de dia, com menos agentes
ou com a memória do Docker ajustada). O código passou em acordo na rodada 2; o Fielzinho é avisado desta decisão.

Ressalvas escritas do fechamento:
1. **Critério "arquivo de 60 (51) MiB viaja e o de 201 MiB não": sem prova Docker.** Tentativas: 05h11 (60 MiB), de
   2.900 para 513 MB livres em 1 min; 07h37 (`-Fatias 1,2`), de 3.183 para 621 MB em 2 min, ainda na subida dos pares
   (log `etapas/logs/08-fatias-1-2.log`: só "o passo do kit sobe o par A"), cortada e limpa; `vmmemWSL` com 2,1 GB até
   um `wsl --shutdown`. O que existe: o limite do kit igual ao do CLI (fonte do `livesync-commonlib`) e o
   `Get-AcimaDoLimite` testado com arquivos esparsos. Item para o Gustavo: rodar
   `pwsh -Command "& 'agents/code/test/08-banco-limites.test.ps1' -Fatias 1,2"` (por `-File`, "1,2" vira 12).
2. **Fatia 1 sem rodada depois das junções** (último verde 03h37). Atenuante: o teste do 07 (06h44, ponta b02fa4f, que
   já contém o 28 e o gerador novo) passou 24/24, com a pasta local nova fora do banco e nada em claro. A rodada 2 só
   mexeu no `Get-AcimaDoLimite`, fora do caminho do Docker das fatias 1 e 3-7.
3. As ressalvas 1-6 da rodada 1 seguem (registro do CLI caído apagado, falha do laço fora do log, janela do pwsh,
   retrato sem frase, `Restore-RamoApagado` sem `finally`, Agendador real).
