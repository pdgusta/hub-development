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
