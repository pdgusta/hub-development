# Retomada do Cinzel (construtor, Claude)

Leia antes: `etapas/regras-da-construcao.md` (inteiras), o ticket do momento e esta retomada.

## Ticket 09: MCP do banco, gravar com versão (em revisão com o Fiel)

- Fork `C:/Projetos/hub-mcp-banco`, ramo `ticket-09`: 289ec4c, dd9ddb5, 61a6e70 (base v0.10.0 1a4d53f). O
  `package-lock.json` modificado fica fora dos commits (efeito do `npm install`: tirou o `jose` opcional).
- Hub: worktree `C:/context-hub-wt/ticket-09`, ramo `ticket-09`: ce9790b, 619655f e a junção de `integracao` 33b817a
  em 3d9d0bb.
- Relatório: `etapas/relatorio-09-mcp-do-banco.md`. As decisões do maestro estão nos comentários do ticket 09.
- Testes:
  - Costura A: `cd C:/Projetos/hub-mcp-banco && node scripts/e2e-banco.mjs` (Docker `hub-ensaio-09-f`, 5996, com a
    trava). Deu 12/12.
  - Costura B: `pwsh -NoProfile -File agents/code/test/09-mcp-banco.test.ps1` na worktree (Docker
    `hub-ensaio-09-a/b`, 5996/5997, com a trava, ~3 min). Deu 21 PASSA (`etapas/logs/09-docker-4.log`).
  - Sem Docker: `node --test agents/code/test/09-mcp-banco-sem-docker.test.mjs` (12 PASSA dentro).
  - Upstream: unitários `node --import tsx --test "src/**/*.test.ts"` com `TEMP` em caminho longo dá 272/1; e2e local
    `sh .local/e2e-local.sh` dá 36/7. As falhas são as mesmas da base (separador `\` do Windows).
- Leitura prévia do Fiel (04:43), antes do parecer:
  - Concorrência: duas gravações simultâneas da mesma base viva responderiam as duas "gravado, conflito segue
    aberto". Conserto pensado: é conflito quando, depois da gravação, há folha nova que não estava em `before` nem é a
    nossa (`outcome` em `src/vault.ts`).
  - Ressalvas: o `move_note` com conflito na origem não diz que o destino já foi gravado; o passo 05 remonta um build
    velho mas não religa o MCP que já roda (o código velho segue rodando).
  - A sonda dele: `etapas/logs/sonda-09-fiel.e2e.test.ts`.
- Rodada 1: VOLTA (`etapas/parecer-09-Cinzel.md`); consertos levados por fast-forward: fork `ticket-09` d2a5a40, hub
  `ticket-09` ca17738 (worktrees e ramos de conserto apagados). Rodada 2 curta pedida ao Fiel (sem Docker: árvore igual).
- Próximo: o "passa" da rodada 2. Depois do "passa", avisar o Rebite:
  `maestri ask "Rebite" "Cinzel: ticket 09 passou na revisão, ramo ticket-09 (hub) e ticket-09 (fork hub-mcp-banco), testes ..., relatório ..., parecer ..."`.

## Ticket 10: três instâncias, cabeça, regra curta e estado (próximo; código só depois do "passa" do 09)

- Ramo `ticket-10` no fork, a partir de `ticket-09`. No hub, `ticket-10` a partir de `ticket-09`, até o 09 entrar
  em `integracao`; depois, `git merge integracao`.
- Costuras e decisões (a) a (e) aceitas pelo maestro, registradas no ticket 10:
  - Portas: 8796 (escrita do par), 8797 (leitura), 8798 (escrita do cliente). No `.env`: `HUB_MCP_BANCO_URL/TOKEN`,
    `HUB_MCP_BANCO_LEITURA_URL/TOKEN` e `HUB_MCP_BANCO_CLIENTE_URL/TOKEN`.
  - Regra curta completa nas 4 ferramentas de gravação.
  - Cabeça ausente ou acima de 2.000 caracteres: o MCP sobe sem ela e o `instructions` diz "cabeça do AGENTS.md
    indisponível: <motivo>".
  - A validação de frontmatter vale também para nota nova. É feita pelo `HUB_ROOT/agents/code/bin/lib/frontmatter.mjs`
    (`carregarCatalogo` e `analisar`).
  - Estado da vigia: `<hub>/.local/vigia/estado.json`, como combinado com o Trilho (16). O JSON vai como está, menos
    o campo `vistos`. Sem arquivo ou ilegível: "estado indisponível: <motivo>". Com `passada` de mais de 15 min, vai
    junto o aviso "a vigia não roda desde <hora>"; sem `passada`, sem aviso.
- O FastMCP cria cada sessão lendo `this.#options.instructions` (`node_modules/fastmcp/dist/chunk-DMSZ2FEE.js`,
  linhas 1508 e 1680). Conferido (05:05): o construtor guarda `options` por referência; só copia (`...options`) quando
  há `options.auth` sem `oauth`. O fork usa `serverOptions.authenticate` (`src/main.ts` 337 e 363), não `auth`: um
  getter `instructions` em `serverOptions` (main.ts 326) é relido a cada sessão. O upstream já tem `READ_ONLY=true`
  (main.ts 43; `registerTools` não registra as de gravação): base da instância de leitura.

## Ticket 10: andamento (salvo às ~06h00, contexto em 47%)

- 09 passou (rodada 2) e já está em `integracao` 9453e3e; Rebite avisado. Nada pendente no 09.
- Fork: worktree `C:/Projetos/hub-mcp-banco-wt/ticket-10`, ramo `ticket-10` (de `ticket-09` d2a5a40), ponta 58c8504.
  `node_modules` e `lib/livesync-commonlib` são junções para o fork principal: soltar com `cmd /c rmdir` antes de
  remover a worktree. O fork principal (`C:/Projetos/hub-mcp-banco`) fica em `ticket-09`.
  - Feito, costura A sem Docker, `test/hub.e2e.test.ts` (modo local; VAULT_PATH = HUB_ROOT = hub de ensaio em %TEMP%
    com realpath): 10/10 com `HUB_TESTE_HUB=C:/context-hub-wt/ticket-10 node --import tsx --test test/hub.e2e.test.ts`
    (sem a variável, o bloco de frontmatter aparece pulado). Cabeça e troca de arquivo; cabeça > 2.000 ou ausente;
    regra curta nas 4; `estado_do_hub` (recente, velha > 15 min, sem `passada`, ilegível, sem arquivo); instância de
    leitura; frontmatter (nota nova recusada, certa grava, edit recusado, AGENTS.md e SKILL.md gravam).
  - Código: `src/hub.ts` (`readHead`, `hubInstructions`, `SHORT_RULE`, `hubState`, `checkFrontmatter` por import
    dinâmico de `HUB_ROOT/agents/code/bin/lib/frontmatter.mjs`, mensagem da guarda de disco com "Recusado:"); getter
    `instructions` e `HUB_ROOT` em `src/main.ts`; regra curta no invólucro do `addTool`, `estado_do_hub` e `offSchema`
    (write, edit, move no destino) em `src/tools.ts`. Sem HUB_ROOT, tudo como o upstream.
  - Upstream: unitários 272/1 (a falha de base) com TEMP longo; tipos iguais à base. Falta rodar o e2e local do upstream
    (`sh .local/e2e-local.sh` no fork principal dava 36/7; rodar o equivalente na worktree, precisa de `npx tsup`).
- Hub: worktree `C:/context-hub-wt/ticket-10`, ramo `ticket-10` de `integracao` 9453e3e, ponta f7a8358.
  - Feito: `mcp-banco.psm1` com as três instâncias (tabela `$script:Instancias`; `Read-EnvMcpBanco` devolve a de
    escrita com `McpInstancias`; recusa chave faltando, fora de 127.0.0.1, mesma porta, mesmo token); `Start-McpBanco`
    passa `HUB_ROOT = $par.Vault` e `READ_ONLY`; `Install`/`Uninstall` sobem e param as três; `env/05.env.modelo` com
    as 6 linhas. Sem Docker verde: `node --test agents/code/test/09-mcp-banco-sem-docker.test.mjs` (1/1, 18 casos).
- 05h45: feito o passo 1 e 2 abaixo (hub `ticket-10` b2d855e: `09-mcp-banco.test.ps1` com as 6 linhas e parando as três;
  `10-mcp-banco.test.ps1` novo, sintaxe ok). Fork montado (`npx tsup`); e2e local do upstream na worktree 36/7, igual à
  base (a 1ª rodada caiu inteira por partida lenta do servidor: rodar de novo). Fila: sou o 1º depois da Brasa (ela
  avisa); ao soltar a trava, avisar o **Rebite** (2º). Corredor: `etapas/logs/10-corredor.ps1`.
- **Próximo passo exato (era):**
  1. `agents/code/test/09-mcp-banco.test.ps1` linha 55: o `.env` de ensaio tem de ganhar as linhas
     `HUB_MCP_BANCO_LEITURA_URL/TOKEN` (8797) e `HUB_MCP_BANCO_CLIENTE_URL/TOKEN` (8798), tokens distintos
     (`New-Segredo 24`); senão o passo recusa.
  2. Escrever `agents/code/test/10-mcp-banco.test.ps1` (costura B, Docker `hub-ensaio-10-a/b` 5996/5997, par cifrado do
     07 por `ensaio.psm1`, fork por `HUB_MCP_BANCO_DIR` = a worktree do fork): as três sobem; leitura sem ferramenta de
     gravação e recusa gravar; escrita e cliente gravam com base e dão conflito com base velha, cada uma só com o seu
     token (o token de uma não abre outra: 401); cabeça do AGENTS.md do hub de ensaio no `initialize` e, trocado o
     arquivo, sessão nova com a nova; regra curta; `estado_do_hub` com um `estado.json` de exemplo em
     `<hub>/.local/vigia/` e sem ele "estado indisponível"; nota fora do esquema recusada (conferir se o hub montado
     pelo `ensaio.psm1` tem `agents/frontmatter` e `agents/code/bin/lib`); `-Descer` para as três; nada sobra.
  3. Com a trava (`etapas/trava-pesada.md` e a fila): rodar o 10 e o 09 (os de versão de novo com a cifra), logs em
     `etapas/logs/10-docker-*.log`.
  4. Relatório `etapas/relatorio-10-mcp-do-banco.md`, comentário no ticket 10, pedir revisão ao Fiel.
- Combinado com a Vela (17): ver o comentário de 05h25 no ticket 10.

## Armadilhas

- `%TEMP%` é caminho curto (`GUSTAV~1.DEL`): o `fs.watch` do modo local cai (assert do libuv). Nos testes, `realpath`.
- `src/*.ts` do fork tem CRLF: editar com o Edit, nunca com python em modo texto.

- Rode a trava e a fila: `etapas/trava-pesada.md` e `etapas/fila-pesada.md`. Ao soltar, avise quem o maestro mandar.
- O passo 05 só remontava o fork quando faltava o `dist`. Depois de mudar o `src`, rode `npx tsup` no fork, ou
  confie no `Test-BuildVelho`.
- No e2e, uma chamada por vez: os pedidos usam o mesmo `id` JSON-RPC na mesma sessão.
- O sincronizador do LiveSync funde sozinho conflitos de linhas diferentes. Um conflito de verdade, no teste, é na
  mesma linha.
- `maestri ask` sem barra invertida nos caminhos.
- Cinzel 05:35: 1º da fila, à espera do aviso da Brasa. Corredor pronto: `pwsh -NoProfile -File etapas/logs/10-corredor.ps1` (pega e solta a trava; estado em `logs/10-corredor.status`).
- Cinzel 05:58: Docker 05:49-05:55 (`logs/10-docker-1.log` 10: 28 PASSA 4 FALHA do teste; `logs/10-docker-2.log` 09: 21 PASSA). Conserto do teste em hub 6095213 (cabeça com CRLF; conflito na mesma linha). Próximo: rodar só o 10, item 2b da fila, depois do aviso do Rebite: `pwsh -NoProfile -File etapas/logs/10-corredor.ps1 -Testes 10`; ao soltar, avisar a **Brasa**. Depois: relatório `etapas/relatorio-10-mcp-do-banco.md` (rascunho), comentário no ticket 10, revisão ao Fiel.
- Cinzel 06:20: Docker do 10, 2ª rodada: 32 PASSA (`logs/10-docker-3.log`); trava solta 06:15, Brasa avisada, fora da fila. Relatório completo; comentário no ticket 10; revisão pedida ao Fiel. Fork sem `integracao` ainda (o Rebite cria de d2a5a40; o meu `ticket-10` parte dele: sem merge). Próximo: o parecer do Fiel; depois do "passa", avisar o Rebite (hub `ticket-10` e fork `ticket-10`).
- Cinzel 06:55: rodada 1 VOLTA; conserto feito (fork 1e86ad1, hub a40ec84), relatório com a seção "Rodada 2". Rodada 2 pedida ao Fiel; ele roda o Docker. Próximo: o "passa"; depois avisar o Rebite (hub ticket-10 e fork ticket-10; o integracao do fork ele cria de d2a5a40).
- Cinzel ~06:45: rodada 2 PASSA (Fiel). Rebite avisado. Nada pendente no 10 além da junção.
- Cinzel ~07h: o 10 foi juntado pelo Rebite (hub integracao 9cc878b; fork integracao 34c3e50). Ele resolve o ticket depois da suíte e do npm test. Nada pendente comigo. Próximo: o maestro passa o próximo ticket.

## Ticket 11: MCP do banco pelos três harnesses (pego ~06h45)

- Worktree `C:/context-hub-wt/ticket-11`, ramo `ticket-11` de `integracao` 9cc878b. Costuras propostas: `etapas/costuras-11-Cinzel.md` (à espera do maestro). Modelo: `agents/code/test/ponta-a-ponta/12-busca.test.mjs`. Doc do Codex por curl no scratchpad (openai_base_url; instructions: "Codex reads the MCP instructions field"; 512 primeiros caracteres).
- Cinzel 06:50: costuras aceitas (modo local; duas do Copilot; regra seguida e banco recriado fora, ressalva para o 25). Hub `ticket-11` c21dbf1: `11-mcp-banco.test.mjs` sem harness 4/4 (montagem, captura, onde, leitura; com `HUB_MCP_BANCO_DIR` do fork com o 10, senão a montagem aparece pulada) e `ponta-a-ponta/11-mcp-banco.test.mjs` (pulado sem `HUB_HARNESS_REAL=1`). Fork: worktree `C:/Projetos/hub-mcp-banco-wt/ticket-11` (ramo ticket-11 de integracao 34c3e50; node_modules e lib/livesync-commonlib são junções), dist montado, sem mudança. Na fila (item 4) para o harness real. Comando: `HUB_HARNESS_REAL=1 HUB_MCP_BANCO_DIR=C:/Projetos/hub-mcp-banco-wt/ticket-11 node --test --test-concurrency=1 agents/code/test/ponta-a-ponta/11-mcp-banco.test.mjs` na worktree do hub.
