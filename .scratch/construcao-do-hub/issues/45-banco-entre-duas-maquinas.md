# 45: O banco do par entre duas máquinas (rede e segredos)

Type: task
Status: claimed
Etapa: preparo do 26 (duas máquinas)
Blocked by: 25

**What to build:** Preparo do banco do par para duas máquinas de verdade (roteiro `../etapas/roteiro-26.md`; decisão do
Gustavo, 2026-10-17 ~21h45, pelo Maestri Chat: "A", abrir agora).
1. **Rede:** hoje o `compose.yml` publica o CouchDB só em `127.0.0.1`. Uma variável do `.env` do par (ex.:
   `HUB_BANCO_ENDERECO`) passa a dizer em que endereço publicar: `127.0.0.1` por padrão, o IP do Tailscale no par de
   verdade; **nunca `0.0.0.0`** (o kit recusa). `HUB_OUTRO_PAR_URL` aponta para o endereço Tailscale do outro par.
   O Tailscale ainda não está nas máquinas: provar no ensaio com um endereço que não seja `127.0.0.1` (ex.: um IP de
   loopback alternativo ou o da máquina), e deixar a prova pela tailnet para o 26.
2. **Segredos entre máquinas:** um jeito de gerar os dois `.env` (mesma frase-senha e sal) numa máquina e entregar o do
   outro par por canal separado, nunca pelo git: um comando que gera os dois arquivos fora do hub e diz qual levar à
   mão; o par B recusa se o sal do banco não conferir (já recusa).
3. **CLI do LiveSync na outra máquina:** o CLI é um build local (`HUB_LIVESYNC_CLI`). Um passo (ou instrução conferida)
   para montar ou trazer o mesmo build no par B, com a versão (commit 14141446) conferida.

**Fonte:** ressalvas do 07 (`componentes/banco-do-par.md` §7 dos docs); roteiro do 26.

**Blocked by:** 25 (resolvido)

- [x] endereço de publicação pela variável; `0.0.0.0` recusado; ensaio com endereço diferente de `127.0.0.1` verde
- [x] os dois `.env` gerados fora do hub, com aviso de qual levar à mão; nada de segredo no git
- [x] o par B sabe montar ou conferir o CLI do LiveSync na versão certa
- [ ] a suíte segue verde

## Comments

- 2026-10-17 ~21h50 (maestro): publicado pela decisão do Gustavo (Maestri Chat). Dona: a Brasa (fez o 07 e o 08).
- 2026-10-17 ~22h10 (Brasa): claimed. Worktree `C:\context-hub-wt\ticket-45`, ramo `ticket-45`, de `integracao`
  dc514db. Lido o kit do banco. Achados: o Tailscale **já está nesta máquina** (100.120.188.50); o CLI do LiveSync
  precisa do `node_modules` da raiz do repositório do LiveSync (pouchdb-*, chokidar, werift), então "trazer" é o
  repositório inteiro montado, não só o `dist`; o CLI não tem `--version` (a versão se confere pelo HEAD do
  repositório, 14141446a14d...). Combinado com o Cinzel (46) em `etapas/logs/46-combinado-brasa.md`: o gerador
  escreve `HUB_PAR_ID`. Próximo: costuras ao maestro, depois o tdd.
- 2026-10-17 ~22h30 (Brasa): costuras aceitas pelo maestro: (1) `Read-EnvPar` com `HUB_BANCO_ENDERECO` (padrão
  `127.0.0.1`; recusa `0.0.0.0`, `::` e o que não for IP); o compose sempre publica em `127.0.0.1` e, com outro
  endereço, também nele (arquivo extra do compose); (2) `kit/par/gerar-env-pares.ps1` (dois `.env` fora do hub e de
  repositório git, `HUB_PAR_ID` diferentes, diz qual levar à mão); (3) conferência do CLI no passo 04 (commit
  14141446) e `kit/par/montar-cli-livesync.ps1`; (4) prova pesada com Docker. **Decisões do maestro:** prova 4 pelo
  Tailscale desta máquina (100.120.188.50), com a trava, senha aleatória, o menor tempo possível, tudo descido e
  apagado no fim, e conferir por porta que nada ficou escutando no 100.x; a prova do montar faz `npm ci` uma vez, com
  a trava. Próximo: tdd da costura 1.
- 2026-10-17 ~22h05 (maestro, mandato): costuras da Brasa aceitas (127.0.0.1 sempre + endereço extra por HUB_BANCO_ENDERECO; recusa 0.0.0.0, :: e não-IP; gerar-env-pares.ps1 fora do hub e de repositório git, HUB_PAR_ID diferentes; conferência do CLI no commit 14141446 e montar-cli-livesync.ps1). Prova 4 pelo Tailscale desta máquina (100.120.188.50), senha aleatória, minutos, descida conferida por porta; npm ci uma vez, com a trava.
- 2026-10-17 ~23h (Brasa): costuras 1 e 2 verdes, commits 340f857 (endereço; `compose.endereco.yml`) e c2cc1bd
  (`kit/par/gerar-env-pares.ps1`; `New-EnvParesBanco` escreve `HUB_PAR_ID`, `HUB_BANCO_ENDERECO`, CLI e leitor da
  vigia por par). Teste: `node --test agents/code/test/45-duas-maquinas-sem-docker.test.mjs` (25 casos); leves do
  banco (07, 38, 28, 09, 22, 25, 16) 37/37. Ressalva para o 26: o gerador não escreve as linhas dos passos 03, 05
  (tokens do MCP) e 10; vêm dos modelos. Próximo: costura 3 (conferência do CLI no passo 04, montar-cli-livesync.ps1).
- 2026-10-17 ~22h45 (Brasa): **pronto para revisão**, ramo `ticket-45` em 02dabc4. Costura 3: `Assert-CliLiveSync`
  no passo 04 (9ee7ec2) e `kit/par/montar-cli-livesync.ps1` (2a13e88). Provas com a trava: `45-banco-endereco`
  13/13 pelo Tailscale (100.120.188.50; nada ficou escutando; 0 contêineres e volumes) e `45-montar-cli` 6/6 (bundle,
  `npm ci`, build em 141 s). Leves 38/38. Achado: o `index.cjs` montado tem outro hash que o daqui (mesmo commit;
  `npm ci` x `npm install`). Relatório: `etapas/relatorio-45-banco-entre-duas-maquinas.md`. Trava solta e passada ao
  Cinzel. Próximo: revisão do Fiel (o maestro religa).
- 2026-10-17 ~22h55 (Brasa): o maestro religou o Fiel e passou o 45 a ele; achado do CLI anotado pelo maestro para
  o 26 (montar o CLI também no par A). Esperando o parecer.
