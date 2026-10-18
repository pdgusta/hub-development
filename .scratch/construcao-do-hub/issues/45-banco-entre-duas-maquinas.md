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

- [ ] endereço de publicação pela variável; `0.0.0.0` recusado; ensaio com endereço diferente de `127.0.0.1` verde
- [ ] os dois `.env` gerados fora do hub, com aviso de qual levar à mão; nada de segredo no git
- [ ] o par B sabe montar ou conferir o CLI do LiveSync na versão certa
- [ ] a suíte segue verde

## Comments

- 2026-10-17 ~21h50 (maestro): publicado pela decisão do Gustavo (Maestri Chat). Dona: a Brasa (fez o 07 e o 08).
