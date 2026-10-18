# Relatório do ticket 45: o banco do par entre duas máquinas (rede e segredos)

Brasa, 2026-10-17. Ramo `ticket-45`, worktree `C:\context-hub-wt\ticket-45`, de `integracao` dc514db. Ticket:
`../issues/45-banco-entre-duas-maquinas.md`. Combinado com o Cinzel (46): `logs/46-combinado-brasa.md`.

## Costuras (aceitas pelo maestro, 2026-10-17 ~22h30)

1. `Read-EnvPar` com `HUB_BANCO_ENDERECO` (padrão `127.0.0.1`; recusa `0.0.0.0`, `::` e o que não for IPv4).
2. `kit/par/gerar-env-pares.ps1`: os dois `.env` fora do hub e de repositório git, mesma frase e sal, `HUB_PAR_ID`
   diferentes, cada par apontando o outro pelo endereço dele; diz qual levar à mão.
3. Conferência do CLI no passo 04 (também no `-WhatIf`) e `kit/par/montar-cli-livesync.ps1`.
4. Prova pesada com Docker pelo endereço.

**Decisões do maestro:** a prova 4 pelo Tailscale desta máquina (100.120.188.50), com a trava, senha aleatória, o
menor tempo possível, tudo descido e apagado, conferido por porta; a prova do `montar` faz `npm ci` uma vez, com a
trava.

## O que foi feito

### Rede (`banco.psm1`, `compose.endereco.yml`, `04.env.modelo`)

- `HUB_BANCO_ENDERECO` no `.env` do par. Vazio = `127.0.0.1`. `Assert-EnderecoBanco` aceita só IPv4 inteiro e recusa
  `0.0.0.0` (e `::`, `[::]`, `localhost`, IPv6, IP incompleto ou fora da faixa).
- **Desenho:** o `compose.yml` segue publicando em `127.0.0.1` (o kit, o CLI, o MCP e a vigia falam com o banco por
  ali, sem mudança). Com endereço diferente, o `Invoke-Compose` junta o `compose.endereco.yml`, que publica a mesma
  porta também nesse endereço. O par lido ganha `Endereco`; o `Url` do kit segue `http://127.0.0.1:<porta>`.
- `HUB_OUTRO_PAR_URL` aponta o outro par pelo endereço dele (`http://<IP Tailscale do outro>:<porta>`); o
  contêiner chega lá pela rede do Docker Desktop (provado).
- O `-WhatIf` diz os dois endereços ("CouchDB ... em 127.0.0.1:5984 e 100.x:5984").

### Segredos (`kit/par/gerar-env-pares.ps1`, `New-EnvParesBanco`)

- `New-EnvParesBanco` ganhou, por par: `Id` (`HUB_PAR_ID`; sem ele, o nome do contêiner), `Endereco`, `Cli` e
  `VigiaLeitor` (`HUB_VIGIA_LEITOR_DB`). Recusa id fora de `[a-z0-9-]` (`Assert-IdPar`) e id igual nos dois. Sem
  `Endereco`, segue `host.docker.internal` (os ensaios de antes não mudam).
- `gerar-env-pares.ps1 -Saida <pasta> -IdA -EnderecoA -IdB -EnderecoB [-HubA/B] [-PastaParA/B] [-CliA/B]
  [-PortaA/B]`: grava `<IdA>.env` e `<IdB>.env`. Recusa a pasta dentro do hub (replicaria) e dentro de repositório
  git; nunca sobrescreve. Diz: "leve <IdB>.env à mão à máquina do par <IdB> (pendrive ou pasta só sua), nunca pelo
  git", e "depois de copiá-lo, apague-o daqui". Não mostra segredo na saída.
- `PastaPar` (padrão `C:\hub-par`) de cada máquina: `banco` (estado), `cli-db`, `vigia-leitor-db` e, por padrão, o CLI
  em `livesync\src\apps\cli\dist\index.cjs` (onde o `montar` põe).
- O par B recusa um sal que não confere: já recusava (`Set-SalBanco`); não mudou.

### CLI do LiveSync na outra máquina (`conferir-cli.mjs`, `Assert-CliLiveSync`, `montar-cli-livesync.ps1`)

- **Achado:** o `dist/index.cjs` não é autossuficiente: pede por `require` pacotes do `node_modules` da raiz do
  repositório (pouchdb-*, chokidar, werift). Levar só o `dist` não serve. E o CLI não tem `--version`: a versão é o
  HEAD do repositório (`14141446a14deab3353a8864dee41e44c372d006`).
- `Install-ParBanco` (passo 04, também no `-WhatIf`) confere antes de tudo: o arquivo existe; cada pacote que ele pede
  se acha a partir da pasta dele (`conferir-cli.mjs`); o repositório dele está no commit 14141446. O `-WhatIf` lista
  "CLI do LiveSync em <cli> (commit 14141446, conferido)".
- `montar-cli-livesync.ps1 -Destino <pasta> [-Fonte <url ou .bundle>] [-WhatIf]`: clone (padrão: o repositório
  público), checkout do commit, `npm ci` na raiz, `npm run build -w self-hosted-livesync-cli` (README do CLI, "Build
  from source"), a mesma conferência do passo 04 e a linha `HUB_LIVESYNC_CLI=` para o `.env`. Idempotente (build
  já conferido: "já montado"); recusa pasta alheia não vazia. Bundle da máquina A: `git -C <repositório do LiveSync>
  bundle create livesync.bundle HEAD` (o repositório daqui é raso, 5,5 MiB).

## Testes

### Sem Docker (suíte comum)

`node --test agents/code/test/45-duas-maquinas-sem-docker.test.mjs` (chama `test/banco/duas-maquinas-sem-docker.ps1`):
o endereço (padrão, aceito, 7 recusas); os dois `.env` (frase e sal iguais, admin próprio, `HUB_PAR_ID`, endereço,
cada um aponta o outro, hub, CLI e leitor, o kit lê os dois, a saída diz o que levar sem segredo, não sobrescreve);
5 recusas sem gravar (repositório git, dentro do hub, ids iguais, maiúscula, `0.0.0.0`); a conferência do CLI pelo
passo 04 `-WhatIf` (não existe, sem dependência, outro commit, o build desta máquina passa); o `montar` (`-WhatIf`
não grava, "já montado" sem tocar no build daqui, pasta alheia recusada).

Leves do banco que usam os arquivos mexidos: 07-kit-sem-docker, 38, 28-sem-docker, 09-sem-docker, 22-sem-docker,
25-pares-sem-docker, 25-cliente-sem-docker, 16-vigia, com o do 45: 38/38 (de novo depois da prova, em 02dabc4).

### Com Docker e Tailscale (trava)

`pwsh -NoProfile -File agents/code/test/45-banco-endereco.test.ps1` (log `logs/45-banco-endereco.log`), 13/13 PASSA:

- os dois pares sobem pelo passo do kit no endereço 100.120.188.50;
- escutas: só `127.0.0.1:5994/5995` e `100.120.188.50:5994/5995`, nada em `0.0.0.0` nem `::`;
- os dois CouchDB respondem no endereço; as duas replicações `running` com o alvo `http://100.120.188.50:<porta>`;
- nota A→B em 3,7 s e B→A em 1,0 s pela tailnet;
- contraprova: o A com o `.env` padrão escuta só em `127.0.0.1` e não responde no 100.x;
- no fim: nada escuta nas portas do ensaio, 0 contêineres, 0 volumes, a pasta saiu, nenhum `node` do ensaio. As
  escutas que ficam no 100.x são do `tailscaled` (porta 53454) e do Windows (139), não do ensaio.

### O montar (trava, `npm ci`)

`pwsh -NoProfile -File agents/code/test/45-montar-cli.test.ps1` (log `logs/45-montar-cli.log`; memória em
`logs/45-montar-memoria.log`), 6/6 PASSA: o bundle do repositório daqui (5,4 MiB); montar pelo bundle numa pasta de
ensaio em 141 s (clone, commit, `npm ci` com 832 pacotes em 2 min, build); a conferência do passo 04 aceita o build
montado; montar de novo diz "já montado" e não roda `npm ci`; o CLI montado roda (`init-settings`); a pasta saiu.
Pico: 1431 MB livres (Docker ligado, vmmemWSL ~1,95 GB).

**Achado:** o `index.cjs` montado (sha256 `1669d00a...`) não é igual ao desta máquina (`29978ec4...`), do mesmo
commit. O daqui foi feito em 2026-10-13 com `npm install`, que reescreveu o `package-lock.json` (diff só de ordem e
`devOptional`); o montado usa `npm ci` sobre o lockfile do commit. A conferência é pelo commit, não pelo hash, e
passa nos dois. Sugestão para o 26: montar o CLI também no par A com o `montar-cli-livesync.ps1` (um `C:\hub-par\
livesync` em cada máquina), para os dois pares rodarem o mesmo build.

## Ressalvas para o 26

- O gerador escreve só as linhas do banco (04), `HUB_PAR_ID` e o leitor da vigia. As dos passos 03, 05 (tokens do
  MCP, `HUB_MCP_BANCO_DIR`), 10 (proxy, `HUB_MAQUINA`, cópia) vêm dos modelos em `kit/par/env/`; a saída lembra.
- Só IPv4 no endereço (o Tailscale dá também um IPv6; não usado).
- A prova foi com os dois pares nesta máquina, pelo IP Tailscale dela: prova o contêiner chegando ao IP da tailnet e
  a publicação nele; o caminho entre duas máquinas de verdade (ACL da tailnet, firewall do Windows na outra) é o 26.
- O fork do MCP do banco (`C:\Projetos\hub-mcp-banco`) também só existe aqui (roteiro do 26, item 4): fora deste
  ticket.
- Docs (`agents/code/docs/componentes/banco-do-par.md` §5 e §7, `operacao.md`): para o Lume.
