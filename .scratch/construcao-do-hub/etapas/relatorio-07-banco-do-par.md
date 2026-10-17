# Relatório do ticket 07: banco do par (Brasa)

Ramo `ticket-07` (worktree `C:\context-hub-wt\ticket-07`), da ponta de `integracao` 8b9beef (com o 06), com
`integracao` 8d1d785 (ticket 14) juntada em 3babfb2. Commits: 4967c69 (kit e teste), 810bbde (provas sobre o módulo),
7fa0e56 (religar o CLI quando a lista muda).

## O que foi construído

**O passo do kit:** `agents/code/kit/par/04-banco.ps1`.

| Uso | O que faz |
|---|---|
| `pwsh 04-banco.ps1 -EnvFile <par>.env` | sobe ou confere o par (idempotente) |
| `... -WhatIf` | só lista o que faria; não sobe contêiner nem grava arquivo |
| `... -Descer [-ApagarDados]` | para o sincronizador e o CouchDB; com `-ApagarDados`, `down -v` e apaga estado e banco local do CLI |

Lê tudo do `.env` do par (modelo em `agents/code/kit/par/env/04.env.modelo`), nunca de `~`.

**A ordem da subida** (módulo `agents/code/kit/par/banco/banco.psm1`, com `compose.yml` e `couchdb.ini`):

1. CouchDB do par em `127.0.0.1:<porta>`, com o `couchdb.ini` copiado para a pasta de estado do par.
2. O sal da E2EE em `_local/obsidian_livesync_sync_parameters`, o mesmo nos dois bancos.
3. A replicação de envio ao outro par (uma tarefa no `_replicator` de cada par).
4. O dispositivo do CLI do LiveSync: cifra de ponta a ponta e caminho ofuscado ligados.
5. As exclusões: o gerador do ticket 06 escreve o `.livesync/ignore` do hub.
6. O sincronizador (o CLI em daemon) sobre o hub, a vista `.md` de mão dupla.

**Proteções no passo:**
- Recusa um banco que já tem outro sal: regravar deixaria ilegível o que já está cifrado.
- Recusa `HUB_ROOT` sob pasta com ponto: o CLI ignoraria tudo.
- Se o gerador diz `mudou` com o daemon rodando, o passo religa o CLI, que só lê a lista na partida (commit 7fa0e56).
  Sem mudança, o daemon segue o mesmo.
- O daemon sobe sem herdar os handles de quem chama o kit. Com eles, quem lê a saída do passo travava para sempre.
- O PID do daemon fica em `<estado>\sincronizador.pid`. Para parar, só esse PID; nunca por nome.

**O ensaio:** `agents/code/test/banco/ensaio.psm1`.
- Monta dois pares nesta máquina sobre o módulo do kit: `New-EnsaioBanco`, `Start-EnsaioBanco`, `Remove-EnsaioBanco`.
- Dá aos testes o que eles olham: as pastas, os bancos crus, a amostra do hub para "nada em claro" e um dispositivo
  leitor para ver o banco em claro.

## Critérios do ticket

Teste de ponta a ponta: `pwsh -NoProfile -File agents/code/test/07-banco.test.ps1`. Ele usa Docker e fica fora do
`node --test`. Chama o passo como o kit chama (`pwsh 04-banco.ps1 -EnvFile ...`), nos contêineres
`hub-ensaio-07-a/b` (portas 5994/5995). Resultado: **24 PASSA, saída 0** (log `C:\context-hub-wt\ticket-07\.local\07-verde-2.log`).

| Critério | Evidência no teste |
|---|---|
| o kit sobe os dois bancos e as duas replicações em andamento | o passo sobe A e B (código 0); a replicação de envio de cada par fica em `running` no `_scheduler` |
| nota criada na pasta A aparece na B, e a editada na B volta à A, sem texto claro no banco | o hub de ensaio inteiro A→B (104 arquivos, 53 s); criar, editar e apagar nos dois sentidos (1 a 5 s cada); nada em claro nos documentos crus dos dois bancos (84 nomes e trechos procurados) |
| a mesma linha editada nos dois pares vira conflito nos dois bancos, sem versão perdida | com a replicação pausada, cada par grava a sua versão; ao religar, 1 documento com `_conflicts` em cada banco, e as duas versões lidas pelo dispositivo leitor (2 folhas) |

Casos a mais no mesmo teste:
- `-WhatIf` não sobe contêiner nem grava arquivo (retrato da pasta igual).
- Rodar o passo de novo sem mudança não religa o CLI (mesmo PID).
- Com pasta local nova, o passo religa o CLI (PID novo), e a nota nova dela fica na A; o controle chega à B.
- `-Descer -ApagarDados` apaga os dois contêineres.

## As ressalvas do ticket 01 (comentário do Rebite)

1. **"Nada em claro" com o hub de ensaio.** O teste procura nos documentos crus (`_all_docs?include_docs=true`) o que
   ele escreveu, mais nomes de arquivo e trechos de corpo do hub de ensaio (`Get-AmostraHub`): 84 procurados, nenhum
   achado.
2. **Nome do contêiner.** Vem do `.env` (`HUB_BANCO_CONTEINER`). O modelo diz `hub-banco`. Os ensaios usam
   `hub-ensaio-<nome>-a/b`: 07 para este ticket, 00 para a prova 01, 02 para a prova 02, 06 para o teste do 06.
3. **Uma cópia só do módulo.** As provas 01 e 02 e o teste do 06 importam `agents/code/test/banco/ensaio.psm1`, que
   importa o módulo do kit. As cópias foram apagadas (`banco.psm1`, `compose.yml`, `couchdb.ini`, `04.env.modelo` das
   duas provas). O que mudou nelas:
   - A prova 01 e a 02 sobem por `Start-EnsaioBanco`: as peças do kit na ordem do passo. O CLI só parte depois de os
     dois bancos estarem de pé.
   - A contraprova `-SemSalComum` da prova 01 virou `New-EnsaioBanco -SemSalComum`: o B ganha um sal só dele.
   - Na prova 02, a lista agora vem do gerador do 06. `-SemExclusao` ainda sobe sem lista nenhuma.
     `Set-ExclusaoComPonto` (a lista só de ponto) mudou para o `ensaio.psm1`, para o `-SoPonto` do teste do 06.
   - Na prova 01, a comparação A→B tira as pastas locais, porque o gerador agora roda.
   - O `-Reiniciar` saiu. O `Start-Sincronizador` do kit nunca refaz o dispositivo.

Antes da junção de `integracao` (logs em `C:\context-hub-wt\ticket-07\.local\`):

| Teste | Resultado | Log |
|---|---|---|
| prova 01 | 17 PASSA, saída 0 | `prova01.log` |
| prova 02 | 12 PASSA, saída 0 | `prova02.log` |
| teste do 06 | 14 PASSA, saída 0 | `06.log` |

Depois da junção e do 7fa0e56: ver "Rodada final".

## Rodada final

Com `integracao` 8d1d785 juntada e o 7fa0e56, uma de cada vez (logs em `C:\context-hub-wt\ticket-07\.local\`):

| Teste | Resultado | Log |
|---|---|---|
| ticket 07 | 24 PASSA, saída 0 | `07-verde-2.log` |
| prova 01 | 17 PASSA, saída 0 (hub A→B: 113 arquivos, 28 s) | `prova01-2.log` |
| prova 02 | 12 PASSA, saída 0 | `prova02-2.log` |
| teste do 06 | 14 PASSA, saída 0 | `06-2.log` |
| `node --test "agents/code/test/**/*.test.mjs"` | 89 de 89 na segunda rodada; 1 falha na primeira (ver "O que vai doer") | `node-test.log` |

Nenhum contêiner `hub-ensaio-*` sobrou.

## O que vai doer ao ligar

- **O daemon não é serviço.** O passo sobe o CLI em segundo plano e grava o PID, mas nada o religa depois de reiniciar
  a máquina ou de o processo cair. As regras proíbem tarefa agendada no ensaio. Quem cuida disso (kit, vigia, tarefa
  do Windows) é decisão de outro ticket.
- **Pasta local nova com o CLI rodando.** O `index.md` com `local: true` e o que nasce na pasta antes de o passo
  rodar de novo replicam: o daemon só lê a lista na partida. O passo religa o CLI quando a lista muda, mas alguém
  precisa chamar o passo, ou o gerador e o religar, quando uma pasta vira local. Hoje ninguém chama sozinho.
- **O CLI vem de um build local.** `HUB_LIVESYNC_CLI` aponta o build do commit 14141446 em
  `C:\Projetos\spike-livesync\...`. A outra máquina precisa do mesmo build, ou o kit precisa de um passo que o monte.
- **O endereço do outro par.** No ensaio é `host.docker.internal:<porta>`. Entre as máquinas é o endereço Tailscale
  do outro par, e o CouchDB precisa aceitar conexão por ele: hoje o compose publica a porta só em `127.0.0.1`. A
  replicação é feita de dentro do contêiner, e o caminho até o outro par pela tailnet não foi provado aqui.
- **O sal e a frase-senha.** Os dois `.env` precisam do mesmo `HUB_BANCO_SAL` e da mesma `COUCHDB_PASSPHRASE`. O
  `New-EnvParesBanco` gera os dois numa máquina só. Entre duas máquinas, um `.env` tem de ser copiado à mão, ou por
  canal separado (ticket 34). Se o sal não confere, o passo recusa, o que é melhor que cifrar errado.
- **O conflito no disco.** Com o conflito aberto, cada disco mostra a própria versão (`[VÊ]` da prova 01). As duas
  versões ficam guardadas no banco, mas nada avisa a pessoa. Quem mostra e resolve é de outro ticket.
- **A suíte rápida chama os harnesses de verdade.** `node --test "agents/code/test/**/*.test.mjs"` inclui
  `ponta-a-ponta/14-guardas.test.mjs` e `provas/03-codex-hooks/prova.test.mjs`. Os dois copiam o login para
  `%TEMP%\hub-ensaio-14-*` e `hub-ensaio-03-*`, chamam o Claude, o Codex e o Copilot, e regravam as evidências
  versionadas deles. Não é "rápida", e quem a roda gasta login e cota sem saber. Não é do 07; aviso para quem junta.
- **O teste do 14 falha sozinho.** Ele compara o hash dos arquivos reais de configuração antes e depois. Na minha
  primeira rodada, o hash de `~/.codex/config.toml` mudou durante o teste (`a6cae9fa…` → `368753…`). A causa não foi
  apurada: outra sessão do Codex no canvas, ou a prova 03 rodando junto (o `node --test` roda os arquivos em paralelo).
  A segunda rodada deu 89 de 89.

## Uso de harness e login

O código do ticket 07 não chama Claude Code, Codex nem Copilot. A suíte rápida chamou, nas minhas duas rodadas dela
(o teste do 14 e a prova 03, ver acima):
- Os testes registraram cada cópia e o apagamento. Exemplo da segunda rodada: Claude copiado às 00:16:42Z e apagado
  às 00:17:16Z; Codex copiado às 00:17:21Z e apagado às 00:17:41Z; `login-apagado.txt` da prova 03 com `apagado=true`.
- Hashes dos logins reais iguais antes e depois: `.claude/.credentials.json` `13644f92…`, `.codex/auth.json` `9e42496b…`.
- Conferi depois: nenhum `auth.json` nem `.credentials.json` sobrou em `%TEMP%\hub-ensaio-*`.
- As evidências regravadas (`evidencia-14/`, `provas/03-codex-hooks/evidencia/`) voltaram ao commitado
  (`git checkout`): não são deste ticket.

Nada gravado em `~` pelo 07.

## Rodada 2 (consertos do parecer da rodada 1)

Commit 6911857, com `integracao` juntada até c5b946a (ticket 12) em 68cb1b6. Os três consertos estão em
`agents/code/kit/par/banco/banco.psm1`.

1. **O PID salvo só vale se for o daemon deste par.** `Get-PidSincronizador` confere a linha de comando do processo:
   ele precisa ser `node.exe`, com o `HUB_LIVESYNC_DB` do par e o comando `daemon`. Com um `node` alheio no PID salvo,
   o sincronizador não conta como de pé, e `Stop-Sincronizador` não mata o processo alheio.
2. **O dispositivo já aceito é conferido com o `.env`.**
   - Do `settings.json` saem `encrypt`, `passphrase` e `usePathObfuscation`.
   - Do remoto saem o banco, a porta e o usuário. O CLI de verdade guarda o remoto cifrado depois do aceite
     (`remoteConfigurations[...].uri` com `isEncrypted: true`; os `couchDB_*` ficam vazios). Com o daemon rodando,
     nenhum outro comando do CLI abre o banco local (o `remote-export` falhou assim no passo repetido). Por isso a
     conferência do remoto é contra a marca do aceite.
   - O que não confere é recusado, e a mensagem diz o campo. Regravar mudaria a cifra de um dispositivo que já tem dados.
3. **O aceite fica numa marca, gravada só depois do `ACCEPTED`.** A marca é `<cli-db>\.livesync\hub-aceito`, com o
   banco, a porta, o usuário e a hora, sem senha. Se o `mark-resolved` falha, o `isConfigured` volta a `false`, e a
   próxima chamada refaz o dispositivo.

**Testes sem Docker** (na suíte comum): `agents/code/test/banco/kit-sem-docker.ps1`, chamado por
`agents/code/test/07-kit-sem-docker.test.mjs`. Ele usa um CLI falso, `agents/code/test/banco/cli-falso.cjs`, que imita
o `init-settings`, o `remote-add` e o `mark-resolved` (com uma falha inventada). Resultado: 11 PASSA.
- Vermelho antes do conserto: 8 falhas.
- Conferido também com o CLI de verdade, num par só: a segunda chamada confere, e uma porta errada é recusada.

**Ressalva das esperas:** mais folga.
- Estado da replicação, conflito e chegada do controle: 120 s.
- Hub A→B: 300 s. O hub de ensaio tem 175 arquivos desde o ticket 19.
- A falha da replicação diz "sem estado em 120 s".

**Docker:**

| Teste | Resultado |
|---|---|
| `07-banco.test.ps1` em 6911857 | 24 PASSA, saída 0 (log `.local/07-r2e.log`; hub A→B, 175 arquivos, em 37 s) |
| prova 01, prova 02, teste do 06 | PREENCHER |

**Memória:** a máquina ficou sem memória duas vezes, e o sistema parou a fila.
- A primeira vez (~23h05) foi no meio da prova 01. Limpei os contêineres `hub-ensaio-00-a/b` e a pasta, pelos `.env`
  e PIDs do ensaio. Nenhum daemon tinha subido.
- A segunda vez (~23h40) foi enquanto a fila esperava memória.
- Desde o aval do maestro, a fila (`.local/fila-docker.ps1`) confere a memória livre antes de cada prova. Abaixo de
  3 GB, ela espera 3 minutos e confere de novo. O registro fica em `.local/fila-docker.log`.

