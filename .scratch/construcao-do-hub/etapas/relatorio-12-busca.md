# Relatório do ticket 12: busca local com aceite (Trilho)

## Estado

- Ramo `ticket-12` (HEAD cc96be2), worktree `C:\context-hub-wt\ticket-12`. Parte de `integracao` 8d1d785; junta `integracao` dc56d47
  (27, 29 e 19).
- Commits pedidos à parte: 58b9563 (testes do 14 apagam as próprias pastas do `%TEMP%`, mesmo falhando), 9cb10f4 (o
  mesmo no 04 e no 05), cb71dcf (teste do 05 "nota arquivada" com as saídas na mensagem da asserção, pedido do Rebite:
  falhou uma vez na suíte de `integracao` dc56d47 sem a causa; aqui, 6 de 6 verdes sob carga, 3,4 a 6,4 s).
- **Pendente: o aceite do Codex com harness real.** A conta do Codex bateu no limite de uso ("You've hit your usage
  limit ... try again at Oct 17th, 2026 1:34 AM"). Decisão do maestro: revisão já; quando a cota voltar, rodo o Codex
  num commit só de evidência e peço ao Fiel uma rodada curta.

## Decisões do maestro (2026-10-16)

1. As linhas de registro do MCP de busca nos três harnesses entram no 12 (spec, faixa 3, user story 22: o fragmento de
   kit as entrega; o kit, ticket 23, só junta). Formato nativo de cada harness, pela doc oficial.
2. O aceite com harness real entra no 12, atrás de `HUB_HARNESS_REAL=1`: o teste confere que o harness chamou a busca e
   devolveu o caminho certo, não a redação.
3. Aval para instalar o obsidian-hybrid-search 0.16.2 por npm, só local (`.local\busca` do hub), versão fixa com lock.

## O que foi construído

- **Skill** `agents/skills/busca/`:
  - `iniciar.ps1`: roda o gerador de exclusões (recusa dele, recusa da busca), lê `.local/exclusoes/busca.env`, fixa
    `LOCAL_EMBEDDING_MODEL=Snowflake/snowflake-arctic-embed-m-v2.0` e o estado em `.local\busca\estado`, tira
    `OPENAI_*`, converte o hub para caminho longo e sobe `serve --foreground --host 127.0.0.1 --port N`.
  - `relatorio.mjs [--url] [--consertar]`: indexadas, válidas, `faltando`, `recusadas` (caminho, erro, `no_indice`),
    modelo, pendentes, consertadas; grava `.local/busca/relatorio.json`; código 1 se falta nota. `--consertar` chama o
    `reindex` incremental.
  - `SKILL.md`: a busca é a porta; ferramenta `search` do `hub-busca` (modos, `queries`, `path`), `read` e `status`; o
    que fica fora; subir; conferir o índice.
- **Kit** `agents/code/kit/par/`:
  - `03-busca.ps1` (+ `busca/package.json` e `package-lock.json`): `npm ci` em `<hub>\.local\busca`, idempotente pelo
    hash do lock e pela versão instalada, `-WhatIf`.
  - `busca/registro/{claude.json,codex.toml,copilot.json}` + `README.md`: a linha de registro do servidor `hub-busca`
    em cada harness, com `{{URL}}` (o kit troca por `HUB_MCP_BUSCA_URL`). Não precisa de `{{DIR}}` nem `{{HUB}}`: é um
    servidor HTTP.
  - `env/03.env`: `HUB_MCP_BUSCA_URL=http://127.0.0.1:3939/mcp`.
- **Testes** (`agents/code/test/`):
  - `12-busca.test.mjs` (9): palavra; paráfrase sem palavra em comum; nota nova com o tempo medido; exclusões (ponto e
    `local: true`, na partida e com a busca ligada); relatório; `Host` estranho e só 127.0.0.1; inglês, `.pdf.md` e
    binário fora; rajada de 200; segunda partida reaproveitando o índice, com `--consertar`. Sem `HUB_BUSCA_OHS`, instala
    a busca no ensaio pelo kit (~1 min).
  - `12-kit-busca.test.mjs` (4): `-WhatIf` não grava; instala pelo lock; segunda rodada não muda; a busca sobe com a
    instalação do kit.
  - `12-busca/servidor.mjs`: os ajudantes comuns (subir, MCP por fetch, parar).
  - `ponta-a-ponta/12-busca.test.mjs` (harness real, pulado sem `HUB_HARNESS_REAL=1`): um hub de ensaio e uma busca;
    nota nova em pt-BR gravada com a busca ligada; cada harness com HOME de ensaio e o fragmento do kit; pedido de duas
    buscas (`fulltext` com "pitangueira", `semantic` com "em que lugar se criam árvores pequenas no topo do edifício");
    confere o servidor registrado, as chamadas de `search` e o caminho na resposta final. Evidência em
    `ponta-a-ponta/evidencia-12/<harness>/` (`saida.jsonl`, `erros.txt`, `lido.json`) e os hashes.

## Docs conferidas (curl, 2026-10-16; cópias em `etapas/doc-12/`)

- **Claude Code**, `code.claude.com/docs/en/mcp.md`: "User-scoped servers are stored in `~/.claude.json`"; "A JSON
  entry that has a `url` but no `type` is a configuration error"; exemplo `{"mcpServers": {"shared-server": {"type":
  "http", "url": "https://example.com/mcp"}}}`. A doc não diz onde fica o `.claude.json` com `CLAUDE_CONFIG_DIR`;
  **provado ao vivo**: `<CLAUDE_CONFIG_DIR>/.claude.json` com o fragmento deixou o `hub-busca` `connected` no `init`.
- **Codex**, `developers.openai.com/codex/mcp.md`: "Codex stores MCP configuration in `config.toml` ... By default this
  is `~/.codex/config.toml`"; "Configure each MCP server with a `[mcp_servers.<server-name>]` table"; Streamable HTTP:
  "`url` (required): The server address." A referência (`learn.chatgpt.com/docs/config-file/config-reference.md`)
  lista `default_tools_approval_mode` e `tools.<tool>.approval_mode` (`auto | prompt | writes | approve`); o fragmento
  não fixa nenhum, e se o `codex exec` pedir aprovação, a rodada pendente mostra.
- **Copilot CLI**, `docs.github.com/api/article/body?pathname=/en/copilot/how-tos/copilot-cli/customize-copilot/add-mcp-servers`:
  "You can also add MCP servers by editing the configuration file at `~/.copilot/mcp-config.json`"; exemplo
  `"context7": {"type": "http", "url": "https://mcp.context7.com/mcp", ..., "tools": ["*"]}`. Referência da CLI:
  "`COPILOT_HOME` | Override the configuration and state directory. Default: `$HOME/.copilot`"; `--allow-tool='MyMCP'`
  libera as ferramentas de um servidor.

## Testes

- `node --test "agents/code/test/**/*.test.mjs"` (comum, sem variável): 147 testes, 141 passam, 6 pulados (harness real), 0 falham (em d5df151); depois de 21f561f, as duas suítes do 12 de novo: 13/13.
- `12-busca.test.mjs`: 9/9 sem `HUB_BUSCA_OHS` (instalando pelo kit). `12-kit-busca.test.mjs`: 4/4.
- Conserto 1 do Fiel (rodada 1): as medidas saem no log do teste (`medidas do ticket 12:`); `medidas.json` só é
  regravado com `HUB_GRAVAR_MEDIDAS=1`. Depois dos 13, `git status` limpo.
- Harness real (`HUB_HARNESS_REAL=1 --test-concurrency=1`):
  - Claude Code (haiku): passa. `hub-busca` `connected`; chamou `search` duas vezes (`fulltext` "pitangueira" e
    `semantic` com a paráfrase); resposta `inbox/viveiro-na-cobertura.md`.
  - Copilot CLI (claude-haiku-5.5): passa. `hub-busca` `connected` no `session.mcp_servers_loaded`; as mesmas duas
    chamadas; resposta com o caminho.
  - Codex (gpt-6-luna, baixo): **não rodou** (limite de uso da conta). O teste agora diz o motivo do turno que falha.

## Medidas (última rodada, `agents/code/test/12-busca/evidencia/medidas.json`)

- Nota nova até aparecer: ~5 s (sem limite de aceite).
- Rajada de 200: 13 a 27 s, todas achadas.
- Partida 1: 11 a 21 s até pronta; partida 2 (índice reaproveitado): 5 a 7 s, indexação de 6 s para 1 s.
- `reindexadas_pelo_consertar`: o que o `reindex` incremental indexou depois de 20 notas gravadas logo na partida (as
  que o vigia perdeu, mais a nota quebrada que entra no reindex). Variou de 0 a 21 entre rodadas.

## Usos de login (aval da rodada `2026-10-16-login-dos-harnesses-no-ensaio`)

| Harness | O que copiou | Copiado (UTC) | Apagado (UTC) |
| --- | --- | --- | --- |
| Claude | `%USERPROFILE%\.claude\.credentials.json` → `CLAUDE_CONFIG_DIR` de ensaio | 01:39:45 | 01:40:05 |
| Codex | `%USERPROFILE%\.codex\auth.json` → `CODEX_HOME` de ensaio | 01:42:16 | 01:42:26 |
| Copilot | só `lastLoggedInUser` e `loggedInUsers` do `config.json` → `COPILOT_HOME` de ensaio (token no cofre, não copiado) | 01:42:26 | 01:42:48 |
| Codex (2ª tentativa, ainda sem cota) | `%USERPROFILE%\.codex\auth.json` → `CODEX_HOME` de ensaio | 01:59:28 | 01:59:35 |

A 2ª tentativa do Codex mostrou que o "1:34 AM" da mensagem é hora de São Paulo (a cota volta às 01:34 de 2026-10-17,
04:34 UTC). Configurações reais iguais nessa rodada também; a evidência dela não foi versionada (a falha é a mesma da
1ª, que está em `evidencia-12/codex/`).

Datas de 2026-10-17 em UTC (22h39 a 22h43 de 2026-10-16 em São Paulo). Pastas apagadas (`apagado: true`). Hashes antes e
depois em `evidencia-12/hashes-claude.json` e `hashes-codex-copilot.json`: `.claude/settings.json`,
`.codex/config.toml`, `.copilot/config.json` e `.copilot/mcp-config.json` iguais. O `~/.claude.json` real mudou na
rodada do Claude; ele é só registrado, porque as sessões abertas na máquina o regravam o tempo todo (o ensaio usou o
`.claude.json` da pasta de ensaio, como o `init` mostrou).

## Achados

1. **Caminho curto do Windows** (`GUSTAV~1.DEL`): o vigia de arquivos do servidor aborta na primeira mudança
   ("Assertion failed: !_wcsnicmp(filename, dir, dirlen)", libuv `src\win\fs-event.c`). Conserto no `iniciar.ps1`
   (`realpathSync.native`). O aceite usa o `%TEMP%` curto de propósito.
2. **Vigia perde nota logo depois da partida**: notas gravadas em pastas novas logo que o MCP responde podem ficar fora.
   O `reindex` incremental recupera. Sugestão: a vigia (faixa 7) roda `relatorio.mjs --consertar` a cada passada.
3. **Cabeçalho quebrado entra no índice no reindex**: o gray-matter guarda o texto em cache; na segunda leitura passa
   vazio. O relatório continua listando a nota, com `no_indice: true`.
4. **Índice guarda caminho em NFD**; o relatório compara em NFC.
5. Sem a lista do gerador, a busca leria `inbox/.rascunho-oculto.md` e a pasta `local: true` (provado por mutação); a
   ferramenta não ignora arquivo com ponto sozinha.
6. O servidor faz `GET https://registry.npmjs.org/obsidian-hybrid-search/latest` na partida (checagem de versão);
   `rerank: true` baixaria um modelo de ~570 MB (não usado).
7. O aceite comum dependia de `HUB_BUSCA_OHS` (a instalação da bancada); sem ela falhava. Agora instala pelo kit.

## Downloads

- `npm install` do obsidian-hybrid-search 0.16.2 (aval do maestro): 261 pacotes, 538 MB em `node_modules`, ~1 min;
  os scripts de instalação (better-sqlite3, onnxruntime-node, protobufjs) rodaram apesar do aviso `allow-scripts` do
  npm 11. Cada rodada do aceite sem `HUB_BUSCA_OHS` faz `npm ci` pelo lock (do cache do npm).
- Modelo arctic: já estava em `~\.cache\huggingface\Snowflake` (313 MB); nada baixado.

## Fora / não verificado

- O gemini (configuração, rodada única ao lado do arctic): não está no aceite do ticket 12; fica para quem o maestro
  indicar.
- O `03-busca.ps1` lê o HOME de `HUB_HOME_ENSAIO` (contrato do instalador) só para o campo `modelo_no_cache`; ele não
  grava nada no HOME.
- Juntar os fragmentos nos arquivos dos harnesses de verdade: ticket 23.
