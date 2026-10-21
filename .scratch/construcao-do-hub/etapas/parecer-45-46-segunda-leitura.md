# Parecer: 2ª leitura dos tickets 45 e 46

Revisor independente (subagente do Fiel), 2026-10-17. Ramos: `ticket-45` (Brasa, 02dabc4) e `ticket-46` (Cinzel,
4e89be6), os dois de `integracao` dc514db. Junção minha, sem commit: worktree destacada
`%TEMP%/hub-ensaio-45-46-fiel-2a` (ticket-46 + `git merge --no-commit --no-ff ticket-45`, sem conflito), apagada no
fim. Não li os pareceres do Fiel. Não rodei Docker, harness real nem npm.

## O que rodei

1. Gerador de verdade, fora do hub e de repositório:
   `pwsh agents/code/kit/par/gerar-env-pares.ps1 -Saida %TEMP%/hub-ensaio-45-46-2a-env/saida -IdA casa -EnderecoA 100.64.0.1 -IdB escritorio -EnderecoB 100.64.0.2 -HubA <junção>`
   → saída 0; `casa.env` com `HUB_PAR_ID=casa`, `HUB_BANCO_ENDERECO=100.64.0.1`, `HUB_OUTRO_PAR_URL=http://100.64.0.2:5984`,
   `HUB_VIGIA_LEITOR_DB=C:\hub-par\vigia-leitor-db`, CLI em `C:\hub-par\livesync\...`. Nenhum segredo na saída.
2. A costura do `.env` junto com os modelos (o que a saída do gerador manda fazer: "falta em cada um: as linhas dos
   passos 03, 05 e 10"): `cat casa.env env/03.env env/05.env.modelo env/10.env.modelo > junto.env`, depois
   `instalar.ps1 -Casa <casa de ensaio> -Hub <junção> -EnvFile ... -Passos 08 -WhatIf`:
   - `casa.env` puro → `passo 08 parou: HUB_MCP_BUSCA_URL falta no .env do par` (esperado: falta o 03);
   - `junto.env` → **`passo 08 parou: HUB_PAR_ID falta no .env do par`**, código 1. O arquivo tem `HUB_PAR_ID=casa`
     na linha 1 e `HUB_PAR_ID=` (vazio, do `10.env.modelo`) na linha 50.
3. Testes leves na junção (TEMP longo, sem `NODE_TEST_CONTEXT`, sem `HUB_HARNESS_REAL`, `--test-concurrency=1`):
   um arquivo por vez: `45-duas-maquinas-sem-docker` 1/1 (12 s), `46-kit-duas-maquinas` 18/18 (125 s), `23-kit` 25/25,
   `27-pastas` 24/24, `27-fim-da-resposta` 19/19, `19-roteamento` 20/20, `38-ensaio-banco` 7/7, `07-kit-sem-docker` 1/1
   (este passa pelo `Assert-CliLiveSync` novo com o CLI desta máquina). **Não rodados:** `16-vigia`, `22-kit-cliente`,
   `22-proxy-sem-docker`, `25-pares-sem-docker`, `25-cliente-sem-docker`, `21-copia-diaria`, `28-pastas-locais-sem-docker`,
   `09-mcp-banco-sem-docker`: o Claude Code parou o laço por falta de memória da máquina (não é falha do teste); não
   religuei. Ficam para a suíte do Rebite na junção. (Uma 1ª tentativa, todos num só `node --test`, estourou o meu
   `timeout 580` no 13º arquivo; sem falha vista antes disso.)
4. Logs das provas: `45-banco-endereco.log` 13/13, `45-montar-cli.log` 6/6, `46-espera-banco.log` 6 PASSA,
   `46-testes-46.log` 18/18, `46-testes-kit.log` 40/40, `46-testes-par.log` 88 + 3 pulados. `grep -il
   "password|passphrase|HUB_BANCO_SAL=|Basic "` nos logs 45-* e 46-*: nada. Nos dois diffs, nenhuma linha
   `(PASSWORD|PASSPHRASE|SAL|TOKEN)=<valor>`.

## Ticket 45 (Brasa): PASSA, com ressalvas

Cada critério confere com o código e a evidência:

- **Endereço pela variável; 0.0.0.0 recusado.** `banco.psm1` `Assert-EnderecoBanco`: só IPv4 de 4 octetos, `TryParse`, e
  recusa `[Net.IPAddress]::Any`. Chamada em `Read-EnvPar` (todo leitor do `.env`: 04, 05, proxy, vigia, laço,
  nova-pasta-local) e em `New-EnvParesBanco`. O `compose.yml` segue em `127.0.0.1`; o `compose.endereco.yml` só entra
  com endereço diferente. Prova: escutas só em `127.0.0.1` e `100.120.188.50`, nada em `0.0.0.0`/`::`; contraprova com
  o padrão; 7 recusas no teste leve (`duas-maquinas-sem-docker.ps1:40`).
- **Os dois `.env` fora do hub e de repositório; aviso do que levar à mão.** Conferido no meu passo 1. Recusa dentro
  do hub e dentro de repositório git; não sobrescreve; apaga os dois se a geração cai.
- **CLI na versão certa.** `Assert-CliLiveSync` no começo do `Install-ParBanco` (também `-Simular`); `montar-cli-livesync.ps1`
  com bundle, `npm ci`, build e a mesma conferência. O caminho padrão do gerador
  (`<PastaPar>\livesync\src\apps\cli\dist\index.cjs`) bate com o `-Destino <PastaPar>\livesync` do montar.
- **Junção com as outras etapas.** Todo objeto de par vem de `Read-EnvPar` (o `Read-EnvMcpBanco` faz `PSObject.Copy()`),
  então `Endereco` sempre existe onde o `Invoke-Compose` o usa (Start no 04, no laço do 07 e no Uninstall). Os nomes de
  ensaio (`07`, `08`, `09`, `10`, `16`, `21`, `22`, `25`, `28`, `06`, `00`, `02`, `x`, `07-sem-docker-<PID>`) passam
  no `Assert-IdPar` que o `New-EnvParesBanco` agora aplica ao id padrão (nome do contêiner).

### Ressalvas do 45 (não seguram o passa)

1. **Defesa do 0.0.0.0 depende do chamador.** `banco.psm1` `Invoke-Compose`: `if ($par.Endereco -ne '127.0.0.1')` com
   `Endereco` nulo junta o `compose.endereco.yml`, e `${HUB_BANCO_ENDERECO}` vazio vira `":<porta>:5984"`, que o Docker
   publica em todas as interfaces. Hoje nenhum chamador monta um par sem `Read-EnvPar` (conferido por grep), então não é
   bug vivo. Barato fechar: `${HUB_BANCO_ENDERECO:?}` no `compose.endereco.yml`, ou testar `$par.Endereco` não vazio.
2. **Endereço não precisa ser da tailnet.** Aceita qualquer IPv4 (ex.: o da rede local, 192.168.x), o que abriria o
   banco à rede local (com senha). Um aviso fora de `100.64.0.0/10` ajudaria o Gustavo no 26.
3. **Partida da máquina (26).** `compose.yml` tem `restart: unless-stopped`; com a porta presa ao IP do Tailscale, se o
   Docker subir antes do Tailscale, o contêiner pode não subir (nem em `127.0.0.1`) até o laço religá-lo. Não testado.
4. **A saída do gerador não fala do montar.** O CLI padrão aponta `C:\hub-par\livesync\...`, que não existe nas duas
   máquinas até rodar o `montar-cli-livesync.ps1` (o passo 04 recusa, com mensagem clara). Vale uma linha na saída
   ("monte o CLI com montar-cli-livesync.ps1 -Destino <PastaPar>\livesync nas duas máquinas"); casa com a sugestão da
   própria Brasa (mesmo build nos dois pares).
5. A saída do gerador manda juntar o `10.env.modelo`, que traz `HUB_PAR_ID=` vazio: ver o conserto 1 do 46.
6. Só IPv4; `git -C` no CLI pode falhar com "dubious ownership" se a pasta for de outro usuário na máquina B.

## Ticket 46 (Cinzel): VOLTA (um conserto)

Os critérios conferem, menos a costura com o `.env` gerado:

- **`HUB_PAR_ID` do `.env` aos verificadores e hooks.** `08-harnesses.mjs` `par()` grava `<hub>/.local/par.json`
  (`.local/` está no `.gitignore` e é pasta com ponto, que o CLI não replica); `bin/lib/par.mjs`: variável primeiro, arquivo
  de reserva; `verificar-pastas.mjs` e `registro.mjs` leem por ele. Testes: `46-kit-duas-maquinas.test.mjs:50` (link para
  fora do hub vira `par://` sem a variável), `:78` (pelo hook do fim da resposta), `:92` (registro do roteamento). Regra
  do id igual nos dois lados (`/^[a-z0-9]+(-[a-z0-9]+)*$/` no 08 e `-cnotmatch` igual no `Assert-IdPar`).
- **Espera com prazo.** `espera.mjs`: leitor da vigia (`HUB_VIGIA_LEITOR_DB`, gerado pelo 45 e iniciado pelo passo 04,
  `banco.psm1:438`), `HUB_VIGIA_OUTRO_PAR_URL` com recuo para `HUB_OUTRO_PAR_URL` (o 45 escreve o IP Tailscale do outro,
  alcançável do host), id da replicação `hub-envio-para-o-outro-par` igual ao `Get-IdReplicacao`. Sai 0 sempre. Prova com
  Docker: 315 s, 566 arquivos, igual ao `convergiu.mjs` por hash.
- **Proxy opcional e lista do que é à mão.** `instalar.ps1`: `proxy` fora da lista padrão; `a_mao` na saída e no JSON.

### Conserto 1 (costura 45×46): o `HUB_PAR_ID=` vazio do `10.env.modelo` apaga o id gerado

- **Onde:** `agents/code/kit/par/env/10.env.modelo` (linha nova `HUB_PAR_ID=`, deste ticket) + `08-harnesses.mjs`
  `lerEnv` (linhas 58-65: `env[m[1]] = m[2].trim()`, a última vence, também com valor vazio). O mesmo vale para o
  `lerEnv` do `espera.mjs` e para o `Read-EnvPar` (última vence).
- **Como quebra:** o gerador do 45 escreve `HUB_PAR_ID=<id>` e diz "falta em cada um: as linhas dos passos 03, 05 e 10
  (modelos em env)". Juntando o `10.env.modelo` como ele manda, a linha vazia vem depois e vence.
- **Evidência:** passo 2 acima: `junto.env` com `HUB_PAR_ID=casa` (linha 1) e `HUB_PAR_ID=` (linha 50) →
  `instalar.ps1 ... -Passos 08 -WhatIf` → `passo 08 parou: HUB_PAR_ID falta no .env do par`, código 1. Na instalação
  de verdade (passos padrão), o 04 já subiu o banco quando o 08 para; a mensagem diz "falta" com o id no arquivo, o que
  confunde no dia do 26.
- **Conserto sugerido (um dos dois, à escolha do Cinzel):** tirar `HUB_PAR_ID` do `10.env.modelo` (o gerador o escreve;
  pôr o comentário no `04.env.modelo`, que o gerador já cobre) **ou** o `lerEnv` do 08 não deixar valor vazio apagar um
  preenchido (ou recusar chave repetida com a linha das duas). Um teste: o `.env` do `gerar-env-pares.ps1` + os três
  modelos passa no `-Passos 08 -WhatIf` com o id gerado.

### Ressalvas do 46 (não seguram)

1. **Dois nomes para a máquina.** `HUB_MAQUINA` (cópia diária, ramo `par/<HUB_MAQUINA>`) e `HUB_PAR_ID` (par:// e
   registro do roteamento). O gerador escreve só o segundo. Para o 26: dizer que os dois devem ser iguais, ou um derivar
   do outro. E o registro de uso desta máquina muda de `<hostname>.md` para `<id>.md`.
2. **Mensagem da espera no par A.** No primeiro par (o que tem o hub no disco), o banco começa vazio e a espera diz "o
   banco do par ainda não tem nada do outro par", quando na verdade ele está subindo o disco. Só texto.
3. **Leitor da vigia em uso duplo.** A espera roda `sync`/`ls` no mesmo banco local do leitor da vigia; se a vigia rodar
   ao mesmo tempo (hook aberto num harness), pode haver trava do banco local. Na instalação é improvável.
4. `spawnSync` do `ls` com o `maxBuffer` padrão (1 MiB): basta para alguns milhares de arquivos; anotar se o hub crescer.
5. A espera compara tamanho, não hash (já dito no relatório). O `-Desfazer` não tira o `.local/par.json` (dito).

## Resumo

- 45: **PASSA**, com 6 ressalvas (a mais útil: fechar o `${HUB_BANCO_ENDERECO:?}` no compose e dizer o montar na saída
  do gerador).
- 46: **VOLTA**, 1 conserto: a linha `HUB_PAR_ID=` vazia do `10.env.modelo`, juntada como o gerador do 45 manda, vence a
  gerada e o passo 08 para com "HUB_PAR_ID falta" (reproduzido). O resto confere.
