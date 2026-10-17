# Relatório do ticket 10: MCP do banco, três instâncias, cabeça, regra curta e estado (Cinzel)

Dois ramos `ticket-10`:
- **Fork** `C:\Projetos\hub-mcp-banco`, worktree `C:\Projetos\hub-mcp-banco-wt\ticket-10`, ramo `ticket-10` a partir de
  `ticket-09` d2a5a40. Commits c182dcc (cabeça), 98a407e (regra curta; cabeça indisponível dita), d40dffa
  (`estado_do_hub`) e 58c8504 (frontmatter pelo verificador do hub; instância de leitura no e2e). O fork principal fica
  em `ticket-09`. Na worktree, `node_modules` e `lib/livesync-commonlib` são junções para o fork principal.
- **Hub**: worktree `C:\context-hub-wt\ticket-10`, ramo `ticket-10` a partir de `integracao` 9453e3e (já com o 09).
  Commits f7a8358 (o passo 05 com as três instâncias), b2d855e (o teste Docker do 10; o do 09 com as três no `.env`) e
  6095213 (consertos do teste do 10).

Decisões do maestro (comentários do ticket 10, 04:45 e 04:46): portas 8796 escrita do par, 8797 leitura, 8798 escrita do
cliente; regra curta completa nas 4 ferramentas de gravação; cabeça ausente ou acima de 2.000 caracteres fica de fora
inteira, com o motivo; validação também para nota nova; `estado.json` ilegível vira "estado indisponível: <motivo>";
`passada` com mais de 15 min leva o aviso "a vigia não roda desde <hora>"; o campo `vistos` não sai.

## O que foi construído

### No fork

Tudo só vale com `HUB_ROOT` definido (a pasta do hub na vista `.md`). Sem ele, o fork se comporta como no 09.

| Peça | O que faz |
|---|---|
| `instructions` | Um getter em `serverOptions` (`src/main.ts`). O FastMCP relê `options.instructions` a cada sessão nova, e o fork usa `authenticate`, não `auth`, então as opções não são copiadas. A cada `initialize`, o bloco `<!-- cabeca:inicio -->…<!-- cabeca:fim -->` do `HUB_ROOT/AGENTS.md` é lido do disco e vai **antes** do texto do upstream. Sem arquivo, sem bloco ou acima de 2.000 caracteres: o texto do upstream mais a linha "cabeça do AGENTS.md indisponível: <motivo>". Nunca uma cabeça cortada (`src/hub.ts`, `readHead` e `hubInstructions`). |
| Regra curta | `SHORT_RULE` no começo da descrição de `write_note`, `edit_note`, `delete_note` e `move_note`: "Antes de gravar, leia `AGENTS.md`. Grave com a `base_rev` lida; conflito = releia e refaça." (`src/tools.ts`, no invólucro do `addTool`). |
| `estado_do_hub` | Lê `HUB_ROOT/.local/vigia/estado.json` (combinado com o Trilho, ticket 16). `content[0]` traz o JSON como está, menos `vistos`. Com `passada` de mais de 15 min, vem um `content[1]` "a vigia não roda desde <passada>". Sem arquivo, ilegível ou fora de objeto: "estado indisponível: <motivo>". Existe nas três instâncias. |
| Frontmatter | `write_note`, `edit_note` (o texto resultante) e `move_note` (no destino) chamam o verificador do próprio hub (`HUB_ROOT/agents/code/bin/lib/frontmatter.mjs`, `carregarCatalogo` e `analisar`, ticket 05): o mesmo verificador do disco. Fora do esquema: "Recusado: a nota <caminho> ficaria fora do esquema do tipo <tipo>: <faltas>…", e nada grava. Sem o verificador: recusa ("não carregou"), nunca grava sem checar. `AGENTS.md`, `SKILL.md` e afins passam (o verificador os ignora). |
| Instância de leitura | `READ_ONLY=true` do upstream: as 4 ferramentas de gravação não são registradas, e o backend recusa gravar. |

### No hub: o passo 05 do kit

`agents/code/kit/par/mcp-banco/mcp-banco.psm1`:
- Tabela `$script:Instancias`: `HUB_MCP_BANCO` (escrita do par), `HUB_MCP_BANCO_LEITURA` (leitura) e
  `HUB_MCP_BANCO_CLIENTE` (escrita do cliente). Cada uma tem `_URL` e `_TOKEN` no `.env`.
- `Read-EnvMcpBanco` devolve a de escrita, com as três em `McpInstancias`. Recusa chave faltando, URL fora de
  `http://127.0.0.1:<porta>/mcp`, duas com a mesma porta e duas com o mesmo token.
- `Start-McpBanco` passa `HUB_ROOT` (a pasta do hub do par) e `READ_ONLY`, e guarda o estado de cada uma em
  `mcp-banco-<porta>`.
- `Install` sobe as três; `Uninstall` (o `-Descer`) para as três.
- `env/05.env.modelo` ganhou as 6 linhas.

## Critérios do ticket

| Critério | Costura A (fork, modo local, sem Docker) | Costura B (hub, par do 07 com cifra, Docker) |
|---|---|---|
| a de leitura não lista ferramenta de gravação e recusa gravar; as duas de escrita gravam com a guarda de versão, cada uma com o seu token | PASSA (leitura) | PENDENTE (2ª rodada). Na 1ª: as três sobem em processos distintos; o token de cada uma, e o vazio, dão 401 nas outras duas; a leitura lista 8 ferramentas, nenhuma de gravação, e a gravação é recusada sem mudar o `.md`; o cliente com versão velha ouve "conflito" |
| a conexão traz a cabeça do `AGENTS.md` de ensaio e, trocado o arquivo, a sessão nova traz a cabeça nova | PASSA | 1ª: a cabeça nova chega sem religar o processo; acima de 2.000, a cabeça fica de fora com o motivo. A checagem da cabeça original falhou por erro do teste (CRLF) |
| as descrições das ferramentas trazem a regra curta como aceita | PASSA | PASSA nas duas de escrita (regex tirado do texto do spec, não do código) |
| os testes de versão passam de novo com a cifra ligada | — | PASSA: `09-mcp-banco.test.ps1` com o fork do 10 e as três instâncias, 21 PASSA |
| `estado_do_hub` devolve o estado de exemplo e, sem arquivo, "estado indisponível" | PASSA | PASSA: igual ao exemplo, sem `vistos`, nas instâncias de leitura e de escrita; aviso com `passada` de 20 min; "estado indisponível" sem o arquivo |
| nota fora do esquema é recusada | PASSA (nota nova, edit; AGENTS.md e SKILL.md gravam) | PASSA: recusada nas duas de escrita, sem chegar ao banco nem ao disco; com o campo que faltava, grava e chega ao disco |

### Costura A: e2e do fork, sem Docker

`HUB_TESTE_HUB=C:/context-hub-wt/ticket-10 node --import tsx --test test/hub.e2e.test.ts`, na worktree do fork: **10/10**.
- Modo local: `VAULT_PATH = HUB_ROOT` = um hub de ensaio em `%TEMP%`, pelo `realpath`. O caminho curto `GUSTAV~1.DEL`
  derruba o `fs.watch`.
- Sem `HUB_TESTE_HUB`, o bloco do frontmatter aparece pulado, porque precisa de `agents/frontmatter` e do verificador
  de um checkout do hub.
- Casos:
  - cabeça, e troca do arquivo;
  - cabeça acima de 2.000 caracteres, ou ausente;
  - regra curta nas 4 ferramentas;
  - `estado_do_hub`: recente, velha, sem `passada`, ilegível, sem arquivo;
  - instância de leitura;
  - frontmatter: nota nova recusada, a certa grava, edit recusado, `AGENTS.md` e `SKILL.md` gravam.

### Costura B: ponta a ponta no hub, com Docker

`pwsh -NoProfile -File agents/code/test/10-mcp-banco.test.ps1`, com `HUB_MCP_BANCO_DIR` apontando para a worktree do
fork.
- O par do 07 de verdade, pelo `ensaio.psm1`: `hub-ensaio-10-a/b` nas portas 5996/5997, cifra e caminho ofuscado
  ligados, o hub de ensaio do `montar.mjs` na pasta A (com `AGENTS.md`, `agents/frontmatter` e o verificador).
- O passo é chamado como o kit chama, e o MCP é falado por HTTP como um agente fala.
- Corredor: `etapas/logs/10-corredor.ps1`, que pega e solta a trava.

| Rodada | Resultado | Log (`etapas/logs/`) |
|---|---|---|
| 1 (05:49) | **30 PASSA, 4 FALHA, todas do teste.** (a) três casos "o initialize começa pela cabeça": o `AGENTS.md` do hub de ensaio tem CRLF, e o teste esperava `"# Context hub\n"`; a cabeça veio certa (`# Context hub\r\n`). (b) "as duas versões ficam no banco": 1 folha. O par gravou uma linha nova no fim; o cliente, com a mesma base, gravou outra linha nova no mesmo lugar. A resposta foi "conflito: releia e refaça", mas o sincronizador do LiveSync fundiu as duas mudanças sozinho, como no caso 4b do 09. Conserto do teste (6095213): a cabeça aceita `\r?\n`; o par grava a linha e depois a muda, e o cliente, com a versão velha, muda **a mesma linha**. Nenhum contêiner sobrou | `10-docker-1.log` |
| 09 de novo (05:51) | **21 PASSA, saída 0**, com o fork do 10 e as três instâncias no `.env` | `10-docker-2.log` |
| 2 | PENDENTE | |

### Sem Docker, na suíte comum

`node --test agents/code/test/09-mcp-banco-sem-docker.test.mjs`: 1/1 (18 casos dentro). Confere as três instâncias no
`.env`, a recusa de chave faltando, de URL fora de 127.0.0.1, de porta repetida e de token repetido, e o `-WhatIf` das
três.

### Testes do upstream (worktree do fork)

- Unitários (`node --import tsx --test "src/**/*.test.ts"`, `TEMP` em caminho longo): 272 passam e 1 falha, a mesma da
  base (separador `\` do Windows).
- e2e local (`test/e2e.test.ts`): 36 passam e 7 falham, as mesmas 7 da base. A primeira rodada caiu inteira: o
  servidor não subiu nos 10 s do teste (já visto no 09). Rodada de novo, passou.

## O que vai doer ao ligar

- **Busca de ferramentas adiada.** Com ela ligada no harness, a descrição das ferramentas pode não ser lida antes da
  chamada, e a regra curta passa despercebida (spec, faixas 05-06). A cabeça no `instructions` segue chegando.
- **O verificador é carregado uma vez.** O catálogo de esquemas é relido a cada gravação, mas o código do
  `frontmatter.mjs` fica no cache de `import`: um verificador novo pede religar o MCP. O passo 05 religa quando o
  `dist` do fork muda, não quando o hub muda.
- **O `estado.json` é de cada máquina.** Mora em `.local/` (pasta local, fora da sincronia), então cada par mostra o
  estado da sua vigia. Antes de a vigia (16) rodar na máquina, a resposta é "estado indisponível", o que está certo.
- **Os caminhos `/banco/mcp` e `/banco-escrita/mcp` do spec** (atrás de um proxy) não existem aqui: a decisão (a) foi
  uma porta por instância em 127.0.0.1. Quem expõe ao cliente é ticket seguinte.
- **A instância do cliente grava no mesmo banco do par.** A separação é só do token: tirar o token do cliente não
  mexe no do par. O que ele grava passa pela mesma guarda de versão e pelo mesmo verificador.
- **A cabeça vai com o fim de linha do arquivo** (CRLF no checkout do Windows). Os harnesses leem os dois.

## Uso de harness e login

Nenhum. O 10 não chama Claude Code, Codex nem Copilot, e não copiou login. Nada foi gravado em `~`. O teste (9) do spec,
com os três harnesses reais citando o `instructions`, não está nos critérios do ticket 10 e não rodou.
