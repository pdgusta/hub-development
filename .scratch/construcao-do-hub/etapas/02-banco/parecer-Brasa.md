# Parecer do Fiel — ticket 07, banco do par (Brasa)

## Rodada 1 — 2026-10-17 — ramo ticket-07, código em 7fa0e56

Veredito: **volta**. Fiel e Fielzinho de acordo (parecer-Brasa-fielzinho.md, em `etapas/`). Os três consertos são do
Fielzinho, reproduzidos por ele e conferidos pelo Fiel no código.

### Consertos (em `agents/code/kit/par/banco/banco.psm1`)

1. **PID salvo aceito só pelo nome `node`** (linha 215). Depois de reiniciar a máquina, o PID do arquivo pode ser outro
   `node` (há vários: harnesses, recrutas). `Start-Sincronizador` então não sobe o daemon, e `Stop` mata um processo
   alheio — contra a regra "só o PID que você abriu". Conferir a linha de comando (o `CliDb`/`daemon` do par), não só
   o nome; teste com um `node` inofensivo no PID salvo.
2. **`isConfigured` encerra a configuração sem conferir** (linha 185). Com `isConfigured: true`, banco, cifra
   (`encrypt`), frase e caminho ofuscado diferentes do `.env` passam calados (ex.: `.env` cifrado e `settings.json` sem
   cifra). Comparar os campos que o kit grava e recusar (ou refazer) a divergência; teste.
3. **`isConfigured` gravado antes do `mark-resolved`** (linhas 197 e 199). Se o `mark-resolved` falhar, a próxima
   chamada volta cedo pela linha 185 e o dispositivo nunca é aceito. Gravar `isConfigured` só depois do `ACCEPTED`
   (ou conferir o aceite); teste com o CLI falhando no `mark-resolved` uma vez.

### Execução (Fiel, Docker, um de cada vez, em 7fa0e56)

- 1ª passada (máquina carregada pela suíte do ticket 29 rodando junto): `07-banco.test.ps1` 1 FALHA (replicação de envio
  do par A sem estado em 30 s; o hub chegou em 97,4 s), prova 01 passa, prova 02 1 FALHA (controle não chegou ao disco
  do B no CLI rodando), `sincronizador.ps1` passa. Logs `etapas/revisao-07-r1-*.log`.
- Repetição com a máquina quieta: `07-banco.test.ps1` tudo passou (hub de 141 arquivos em 28,7 s), prova 02 tudo
  passou. Logs `etapas/revisao-07-r1b-*.log`. Sem contêiner nem pasta hub-ensaio sobrando.

### Ressalvas (não seguram)

- As esperas fixas (30 s para o estado da replicação, 60 s para o controle) falham com a máquina carregada. Vale
  esperar pelo estado, com folga maior, ou dizer na falha que foi tempo.
- Limites, laço e retrato do banco são do ticket 08 (Fielzinho).

Fielzinho: a leitura dele do 07 foi feita antes de a cota acabar; a rodada 2 fica para ele ler depois de 01:34.

## Rodada 2 — 2026-10-17 — ramo ticket-07 em 99ea624 (consertos 6911857, 87ce68b)

Veredito: **volta** (2ª volta). Fiel e Fielzinho de acordo (parecer-Brasa-fielzinho.md, rodada 2). A próxima é a 3ª
rodada: passa, com ressalvas escritas se sobrar algo.

Conferido pelo Fiel no diff de `banco.psm1`: (1) `Get-PidSincronizador` agora exige `node.exe`, o `CliDb` na linha de
comando e `daemon`; (2) `Initialize-Dispositivo` confere cifra, frase, ofuscação e o remoto (db, porta, usuário) pela
marca `hub-aceito` e recusa o que não confere; (3) a marca só nasce depois do `ACCEPTED`, e a falha do `mark-resolved`
volta o `isConfigured` a falso. A espera do daemon subiu para 180 s (87ce68b). Fielzinho: `kit-sem-docker.ps1` 11 PASSA.

### Consertos (os dois do Fielzinho, aceitos pelo Fiel)

1. **PID por substring.** `$linha.Contains($par.CliDb)` aceita outro dispositivo cujo caminho começa igual
   (`...\cli-db-outro` contém `...\cli-db`). Conferir o argumento exato (o caminho entre aspas, como o kit o passa) e o
   CLI do par; teste com um `node` cujo argumento é `cli-db-outro`.
2. **Configurado sem marca é refeito calado.** Com `isConfigured: true` e sem `hub-aceito` (dispositivo de antes deste
   código, ou queda entre o `ACCEPTED` e a gravação da marca), o kit cai no `init-settings --force` e reconfigura com o
   `.env` atual — justamente o caso que o conserto 2 da r1 quer recusar se o `.env` mudou. Recusar com mensagem
   ("configurado sem a marca do aceite; apague para refazer"), ou conferir os campos como no caminho com marca; teste.

Docker: não repetido pelo Fiel nesta rodada (vai na 3ª, com a trava); a Brasa relatou tudo verde, um de cada vez, e
suíte comum 179/8/0.

## Rodada 3 — 2026-10-17 — ramo ticket-07 em 6b1d7e8

Veredito: **passa**. Fiel e Fielzinho de acordo (parecer-Brasa-fielzinho.md, rodada 3).

1. Diff 99ea624..6b1d7e8: `Get-PidSincronizador` exige o CLI e o `CliDb` como argumentos inteiros (com ou sem aspas),
   além de `node.exe` e `daemon`; `Initialize-Dispositivo` recusa `isConfigured` sem a marca `hub-aceito`, sem
   `init-settings` nem regravar o `settings.json`. Fielzinho: `kit-sem-docker.ps1` 14 PASSA.
2. Docker do Fiel, com a trava pesada (02:21, apagada no fim), um de cada vez, máquina sem outra carga pesada:
   `07-banco.test.ps1`, prova 01, prova 02 e `sincronizador.ps1`: os quatro "tudo passou", saída 0. Logs
   `etapas/revisao-07-r3-*.log`. Sem contêiner nem pasta hub-ensaio sobrando; worktree limpo.

Ressalvas da rodada 1 seguem (esperas fixas sob carga; limites, laço e retrato são do 08).
