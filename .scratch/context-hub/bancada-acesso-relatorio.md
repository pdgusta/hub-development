# Bancada de acesso: relatório (ticket 14, "Acesso dos agentes: decisão")

Rodada em 2026-10-14/15 (23h45 às 00h30) por um subagente Opus 5.5 médio. Só dados, sem recomendação.
Hub de mentira em `C:\Projetos\bancada-acesso\` (um `AGENTS.md` com a frase-sonda `SONDA-RAIZ girassol-azul-42`,
`iniciativa-teste\retomada.md`, `papeis\papel-teste\` com `AGENTS.md`, `CLAUDE.md` e `role.json` próprios
(`SONDA-PAPEL lontra-verde-17`), um `.git` real, `vigia\estado-sync.json` simulado). Não há dado de cliente.

**Versões:** Claude Code 2.1.300; Codex CLI 0.161.0; Copilot CLI 1.0.96 no começo e 1.0.98 no fim (a
atualização automática dele trocou a versão no meio da bancada; os testes de extensão e de status line rodaram
na 1.0.98, conforme o log do próprio Copilot).
**Modelos:** Claude `haiku`; Codex `gpt-6-luna` com `model_reasoning_effort=low`; Copilot `claude-haiku-5.5`.

**Peças da bancada** (todas em `C:\Projetos\bancada-acesso\`):
- `scripts\inicio.py`: o hook de início, o mesmo arquivo nos três harnesses (`python inicio.py claude|codex|copilot`).
  Primeiro lê `vigia\estado-sync.json`. Se ele falta, chama a ferramenta `estado_sync` do MCP de teste. Sem os dois,
  avisa "DESCONHECIDO". O texto devolvido leva a frase `SONDA-INICIO pinheiro-dourado-07`, e cada execução grava uma
  linha em `logs\inicio.log`, com `MAESTRI_TERMINAL_ID`.
- `scripts\fim.py`: o fim da resposta sem modelo, para Codex e Copilot. `marca` roda no envio do prompt e `fim` no fim
  da resposta. Se a nota não mudou desde a marca, devolve o agente com `decision: block`. Só age com
  `BANCADA_FIM=1`. O log fica em `logs\fim.log`.
- `mods\fim-retomada\`: o mod do Claude Code (`turn.start` e `classic.Stop`), com log em `logs\mod-fim.log`.
- `extensoes-copilot\fim-retomada\extension.mjs`: a extensão do Copilot CLI (`onUserPromptSubmitted` e
  `onAgentStop`), com log em `logs\ext-fim.log`.
- `scripts\mcp_teste.py`: o MCP de teste, HTTP em `127.0.0.1:8799/mcp`. O token Bearer vem de `BANCADA_MCP_TOKEN` (valor
  falso `bancada-fake-7f3a`). Tem a ferramenta `estado_sync` e as `instructions` com `SONDA-MCP-INSTRUCOES coruja-roxa-88`.
  O log fica em `logs\mcp.log`.
- `scripts\status_vigia.py`: a linha de estado do Copilot; `scripts\codex_rodar.py`: roda o `codex exec`, com ou sem
  os hashes pré-aprovados; `scripts\codex_hooks_list.py`: lê pelo `codex app-server` a lista de hooks, com a chave, o
  hash e a confiança; `scripts\globais_maestri.py`: liga e desliga os arquivos globais do teste do Maestri.
- Configs do teste: `config\claude-inicio.json`, `config\claude-instr.json`, `config\claude-mcp.json`,
  `config\copilot-mcp.json`, `.codex\hooks.json` e `.github\hooks\bancada.json`.
- Cópias das fontes primárias lidas: `fontes\`.

Um fato que vale para todos os testes: a variável `MAESTRI_TERMINAL_ID` chegou a todos os hooks, com o valor
`141c914b-...`, que é o terminal do maestro, de onde esta bancada desceu. Ela é herdada pelo processo. Isso não
substitui o teste 11, que fica com o maestro.

## Placar

| # | Teste | Resultado |
|---|---|---|
| 1 | Hook de início no Codex, e a pré-aprovação pelo kit | **passou** (as duas partes) |
| 2 | Hook de início no Copilot CLI | **passou** pelo hook de usuário; **falhou** pelo hook do repositório (pasta sem confiança) |
| 3 | Hook de início no Claude Code, mesmo script | **passou** |
| 4 | Fim da resposta: mod no Claude Code; correlato no Codex e no Copilot | Claude Code (mod) **passou**; Copilot, extensão e hook `agentStop`: **passou**; Codex: plugin sem correlato de código, então hook `Stop`: **passou em parte** (devolve, mas o Codex não conseguiu gravar a nota nesta máquina) |
| 5 | Checagem com reserva (arquivo, MCP, nenhum) | **passou** nos três, nos três casos |
| 6 | `.git` real no lugar do marcador de raiz | **passou** (Codex e Copilot, subpasta e pasta de papel) |
| 7 | Contrato em dobro na raiz | **não duplicou** no Copilot (link simbólico) nem no Claude Code (import) |
| 8 | MCP com token de variável de ambiente | **passou** nos três |
| 9 | Copilot com `--allow-all-mcp-server-instructions` | **passou** (sem a opção, não chega) |
| 10 | Estado da vigia o tempo todo no Codex e no Copilot | Copilot: **existe e o script é chamado** (o que aparece na tela não foi conferido); Codex: **não existe** item alimentado por script |
| 11 | Hooks dentro de um terminal do Maestri | **pendente: o maestro roda** (passo a passo no fim) |
| 12 | VS Code e a política da empresa | **lista para o Gustavo** (no fim) |

## 1. Hook de início no Codex

**Passou.** O texto do hook chega ao modelo, e o kit consegue deixar o hook aprovado sem passar por `/hooks`.

- Hook de projeto em `.codex\hooks.json` (`SessionStart` → `python .../inicio.py codex`).
- Sem confiança no projeto, o Codex nem lista os hooks do projeto. A fonte diz: *"Project-local hooks load only
  when the project `.codex/` layer is trusted"* (learn.chatgpt.com/docs/hooks.md). A confiança passada por `-c
  projects...trust_level` **não valeu** (o `hooks/list` não mostrou os hooks do projeto). Valeu só gravada no
  `~/.codex/config.toml` (`[projects.'c:\projetos\bancada-acesso'] trust_level = "trusted"`), que foi restaurado depois.
- Com o projeto confiável e sem aprovação, o hook é pulado. A saída mostra só `hook: SessionStart`, que é o hook global
  do GSD, já aprovado. O modelo respondeu `NAO-VEIO`, e `inicio.log` ficou sem linha do Codex. A fonte diz: *"Codex
  records trust against the hook's current hash, so new or changed hooks are marked for review and skipped until
  trusted"*.
- **Pré-aprovação pelo kit:** o hash atual de cada hook sai do `codex app-server` (método `hooks/list`), por
  `scripts\codex_hooks_list.py`. Por exemplo, chave `C:\Projetos\bancada-acesso\.codex\hooks.json:session_start:0:0`,
  hash `sha256:1e3dbbd3...`. Com esse hash passado por `-c hooks.state={ "<chave>" = { trusted_hash = "<hash>" } }`,
  o hook rodou e o modelo respondeu:
  `SONDA-INICIO pinheiro-dourado-07 · Estado do sync: ultima sync ok 2026-10-14T23:50:00-03:00, colisao=False`.
  O código-fonte confirma que o estado de confiança é lido das camadas do usuário e da sessão
  (`codex-rs/hooks/src/config_rules.rs`, `hook_states_from_stack`: `ConfigLayerSource::User { .. } |
  ConfigLayerSource::SessionFlags`). Então a mesma tabela `[hooks.state.'<chave>'] trusted_hash = ...` gravada no
  `~/.codex/config.toml` (o formato que o GSD já usa nesta máquina) também aprova. **Não testado** dessa forma, mas
  `scripts\globais_maestri.py` faz exatamente isso para o teste 11.
- O hash vem da identidade normalizada do hook: evento, matcher e handler (`discovery.rs`, `hook_hash`). Mudar o comando
  do hook muda o hash, e o kit tem de recalcular. A chave leva o caminho absoluto do `hooks.json`.
- Não usado: `--dangerously-bypass-hook-trust` existe, mas o classificador de segurança desta sessão recusou a chamada.

## 2. Hook de início no Copilot CLI

**Passou pelo hook de usuário. Falhou pelo hook do repositório.**

- `.github\hooks\bancada.json` na raiz do repositório: o hook **não rodou**. O log do Copilot (`--log-level all`)
  mostra `folder_trust ... "reason":"repository_untrusted"`. A pasta confiável fica guardada no `~/.copilot/config.json`,
  que também guarda dados de login (*"Stores internal application state ... including authentication data"*,
  cli-config-dir-reference), e por isso não foi lido nem alterado. Confiar na pasta pelo interativo resolveria;
  **não verificado**.
- Hook de usuário `~/.copilot/hooks/zz-bancada-acesso.json`, temporário e com saída imediata fora da bancada: rodou
  (`inicio.log`: `"harness": "copilot", "evento": "sessionStart", "fonte": "new"`), e o modelo repetiu
  `SONDA-INICIO pinheiro-dourado-07, com sync: última sync ok 2026-10-14T23:50:00-03:00`. O modelo comentou que o texto
  "veio na sua mensagem, não em contexto de sistema": o `additionalContext` do Copilot entra junto da mensagem do usuário.
- Formato da saída: `{"additionalContext": "..."}`. A fonte diz: *"Only `additionalContext` is consumed for
  `sessionStart`"* (docs.github.com/en/copilot/reference/hooks-configuration).
- Um achado de passagem: segundo a mesma fonte, o Copilot lê também os hooks do `.claude/settings.json` do repositório
  (*"Cross-tool `.claude/settings.json` and `.claude/settings.local.json` files in the repository are also read"*).

## 3. Hook de início no Claude Code

**Passou.** O mesmo `inicio.py`, ligado por `claude -p --settings config\claude-inicio.json` (sem mexer no
`~/.claude/settings.json`). O modelo respondeu
`SONDA-INICIO pinheiro-dourado-07 (sync: última sync ok em 2026-10-14T23:50:00-03:00, colisao=False)`.
O stdin do hook traz `cwd`, `hook_event_name`, `session_id`, `source` e `transcript_path`.

## 4. Fim da resposta

### Claude Code: mod

**Passou.** O mod `mods\fim-retomada` (`hooks\register.ts`) foi carregado só para a sessão de teste
(`claude -p --plugin-dir`), e o `claude plugin validate` passou. Ele grava o mtime da nota em `turn.start` e, em
`classic.Stop`, devolve `{ block }` se a nota não mudou. Fora da bancada, chama `next(e)`, e um `.catch` deixa passar se o
mod falhar.
- Caso A ("Diga apenas: ok"): `Stop devolvido`, o agente gravou a linha pedida e veio `Stop solto tocada=true`.
- Caso B (o próprio pedido mandava tocar a nota): `Stop solto tocada=true stop_hook_active=false`, sem devolver.
- Aviso do `claude plugin validate`: *"hooks on classic.Stop do not run in a plugin a person installs where an
  organization manages Claude Code: there, these events pass over the plugins you install, and only a plugin the
  organization lists in managed settings runs them"*. Se o Claude Code desta máquina ou da outra é gerenciado por
  organização: **não verificado** (aqui rodou).
- A fonte é a declaração de tipos da API de mods que o próprio Claude Code 2.1.299/300 escreve (skill `plugin-authoring`):
  `classic.Stop` aceita `block` (*"`decision: "block"` with this text as `reason` ... the event's block, veto or
  re-prompt"*).

### Copilot CLI: extensão, o correlato mais próximo de um mod

**Passou.** As fontes:
- github/copilot-sdk, `nodejs/docs/extensions.md`: *"Extensions add custom tools, hooks, and behaviors to the Copilot
  CLI. They run as separate Node.js processes that communicate with the CLI over JSON-RPC"*; ficam em
  `.github/extensions/<nome>/extension.mjs` (projeto) ou no diretório de extensões do usuário (`~/.copilot/extensions/`,
  cli-config-dir-reference).
- github/copilot-sdk, `docs/hooks/session-lifecycle.md`: `onAgentStop` (*"Return a block decision to enqueue another
  user message and continue"*).
- cli-command-reference: `/extensions` *"Only available in experimental mode"*; `GITHUB_COPILOT_PROMPT_MODE_EXTENSIONS`
  *"Set to `true` to load project extensions ... in prompt mode (`-p`)"*.

O que se viu:
- A extensão foi copiada para `~/.copilot/extensions/zz-bancada-fim-retomada/` (temporária e já removida). Sem
  `--experimental`, não carregou. Com `--experimental`, o log do Copilot diz `prompt mode: loaded 1 extension(s)` e o log
  dela mostra: `stop devolvido` → o agente gravou "resposta registrada pela extensao" → `stop solto tocada=true`.
- A entrada do `onAgentStop` traz `sessionId, transcriptPath, stopReason, timestamp, workingDirectory, stopHookActive`.
  A pasta vem em `workingDirectory`, não em `cwd`, e a guarda do arquivo já foi corrigida para isso.
- **Efeito colateral:** `--experimental` gravou `{"experimental": true}` num `~/.copilot/settings.json` novo. O arquivo
  foi apagado no fim (ele não existia antes).
- Não testado: a extensão de projeto (`.github/extensions/`), que depende da pasta confiável e de
  `GITHUB_COPILOT_PROMPT_MODE_EXTENSIONS=true`; e a extensão entregue dentro de um plugin (o changelog diz *"Plugins
  can now ship extensions"*).

### Copilot CLI: hook `agentStop`, sem modelo (o mesmo `fim.py`)

**Passou.** Pelo hook de usuário temporário:
- Caso A: `devolvido`, depois `solto, nota_tocada: true`. O texto do bloqueio entrou como um novo prompt e o
  `userPromptSubmitted` disparou de novo.
- Caso B: `solto, nota_tocada: true, stop_hook_active: false`.

### Codex: correlato de mod

**Não há correlato de código.** Os plugins do Codex empacotam skills, MCP, apps e os mesmos hooks de comando
(developers.openai.com/plugins/build/plugins.md: *"Lifecycle hooks are supported for plugins installed manually in
Codex desktop"*; hooks.md: *"Plugin hooks use the same event schema as other hooks"* e *"Installing or enabling a
plugin doesn't automatically trust its hooks"*). Não achei, na documentação nem na árvore do código lidas, API de
código dentro do processo como a dos mods ou das extensões do Copilot. Por isso o teste foi o hook `Stop` com o
`fim.py`. O plugin com hooks **não foi testado**: exige instalar o plugin na configuração global.

**Hook `Stop`: passou em parte.**
- Caso A: `hook: Stop Blocked`, e o agente tentou gravar a nota (o `fim.log` mostra `devolvido`). A segunda parada
  saiu solta por `stop_hook_active: true`.
- Nesta máquina, o `codex exec` **não conseguiu gravar arquivo nenhum**, nem por shell (`Failed to create unified exec
  process: helper_unknown_error: setup refresh had errors`) nem por `apply_patch` (`patch: failed`), com
  `sandbox_mode="workspace-write"`. Por isso o "solta quando a nota foi tocada" **não pôde ser visto no Codex**. O
  código do script é o mesmo que soltou no Copilot. A falha de gravação é do sandbox do Codex no Windows (causa **não
  verificada**).
- Fonte: hooks.md, `Stop`: *"`decision: "block"` doesn't reject the turn. Instead, it tells Codex to continue and
  automatically creates a new continuation prompt"*.

## 5. Checagem com reserva

**Passou nos três harnesses, nos três casos.** Origem gravada em `inicio.log` e frase repetida pelo modelo:

| Caso | Claude Code | Codex | Copilot CLI |
|---|---|---|---|
| Com arquivo | `arquivo` | `arquivo` | `arquivo` |
| Sem arquivo, MCP de pé | `mcp` (o modelo citou 23:40, a hora do MCP) | `mcp` (`SONDA-MCP-ESTADO: ...`) | `mcp` (`fonte: estado_sync do MCP`) |
| Sem os dois | `nenhuma` (`DESCONHECIDO ... MCP falhou com URLError`) | `nenhuma` | `nenhuma` |

O token chegou ao hook pelo ambiente nos três (`BANCADA_MCP_TOKEN` herdado do processo do harness).
Não verificado: o tempo que o hook leva com o MCP fora do ar pela tailnet (aqui, recusa imediata em 127.0.0.1;
o tempo limite do script é de 3 s).

## 6. `.git` real no lugar do marcador de raiz

**Passou.** Não há `project_root_markers` no `~/.codex/config.toml`.
- Codex (`codex debug prompt-input`, que mostra o que o modelo recebe, sem chamar o modelo):
  - de `iniciativa-teste\sub`: `SONDA-RAIZ girassol-azul-42`;
  - de `papeis\papel-teste`: `SONDA-RAIZ ...` e `SONDA-PAPEL lontra-verde-17`;
  - o Codex lê só o `AGENTS.md`, não o `CLAUDE.md` do papel.
  - Com o modelo, de `iniciativa-teste`, também respondeu `SONDA-RAIZ`.
- Copilot (`copilot instruction list`): de `/`, `iniciativa-teste`, `iniciativa-teste\sub` e `papeis\papel-teste`,
  sempre `Repository instructions: AGENTS.md`. No papel, aparece também `Working directory instructions: CLAUDE.md from
  papeis\papel-teste\AGENTS.md + papeis\papel-teste\CLAUDE.md` (os dois arquivos idênticos viram uma fonte só). Com o
  modelo, no papel, respondeu as duas frases.

## 7. Contrato em dobro com a sessão na raiz

**Não duplicou** nos dois harnesses testados.
- **Copilot:** `~/.copilot/copilot-instructions.md` trocado, por um instante, por um link simbólico para o
  `AGENTS.md` da bancada (o original era um arquivo comum, guardado e restaurado com o mesmo SHA-256). Na raiz e em
  `iniciativa-teste`, o `copilot instruction list` passou a mostrar **só** `Personal instructions: Home
  copilot-instructions.md`, e a linha `Repository instructions: AGENTS.md` sumiu: o Copilot ficou com uma cópia.
  Não testado: um arquivo global que seja cópia, e não link.
- **Claude Code:** a linha `@C:/Projetos/bancada-acesso/AGENTS.md` ficou por um instante no fim do `~/.claude/CLAUDE.md`
  (restaurado, SHA-256 conferido), com um hook `InstructionsLoaded` de log por `--settings`. O hook registrou
  `~/.claude/CLAUDE.md (User, session_start)` e `bancada-acesso\AGENTS.md (User, include)`, uma vez só. Perguntado, o
  modelo disse "1 — ... importado por ... CLAUDE.md".
- Ressalva: sem o import, o `InstructionsLoaded` **não registra** o `AGENTS.md` da raiz, e mesmo assim o modelo responde
  `SONDA-RAIZ` com as ferramentas de leitura desligadas. O hook não enxerga esse carregamento, então a prova de que
  não houve dobro no Claude Code se apoia no que o modelo diz e no log do include. Evidência média.
- Codex: fora do escopo do teste 7, conforme o pedido.

## 8. MCP com token lido de variável de ambiente

**Passou nos três.** O `mcp.log` mostra `token_ok=True` com o agente de cada um:
- **Claude Code:** `--mcp-config config\claude-mcp.json --strict-mcp-config`, com cabeçalho
  `"Authorization": "Bearer ${BANCADA_MCP_TOKEN}"`. O modelo repetiu o texto do `estado_sync`
  (`ua=claude-code/2.1.300`).
- **Codex:** `-c mcp_servers.bancada.url=... -c mcp_servers.bancada.bearer_token_env_var="BANCADA_MCP_TOKEN"`. Conectou
  na primeira tentativa (`initialize`, `tools/list`), mas o `codex exec` recusou a chamada: *"MCP tool call requires
  approval, but approval policy is never"*. Com `mcp_servers.bancada.default_tools_approval_mode="approve"`, a chamada
  completou e o modelo repetiu o texto.
- **Copilot CLI:** `--additional-mcp-config @config\copilot-mcp.json`, com `"Bearer ${BANCADA_MCP_TOKEN}"`; chamou
  `estado_sync` (`ua=copilot-cli`).

## 9. Instruções do MCP no Copilot CLI

**Passou.** Mesmo MCP e mesma pergunta, com só a ferramenta `view` disponível:
- Sem a opção: `NAO-VEIO`.
- Com `--allow-all-mcp-server-instructions`: `coruja-roxa-88`.

Na primeira forma da pergunta, o modelo admitiu que tinha a frase e se recusou a repeti-la ("conteúdo confidencial");
foi preciso perguntar pela palavra seguinte.

## 10. Estado da vigia o tempo todo no Codex e no Copilot

- **Copilot CLI: existe.** A fonte, cli-config-dir-reference, chave `statusLine` do `~/.copilot/settings.json`, diz:
  *"`type`: must be `"command"`. `command`: path to an executable script that receives session JSON on stdin and
  prints status content to stdout ... `refreshInterval`: optional integer number of seconds"*.
  - Teste: `statusLine` → `python scripts\status_vigia.py`, `refreshInterval: 5`, num Copilot interativo aberto por 30 s
    (`Start-Process`, minimizado, encerrado depois: só os processos que eu abri).
  - O script foi chamado 8 vezes, com `cwd=c:\projetos\bancada-acesso\iniciativa-teste`. O JSON da sessão traz
    `ai_used, allow_all_enabled, context_window, cost, cwd, model, remote, session_id, session_name, transcript_path,
    username, version, workspace`.
  - **O que aparece na tela não foi conferido** (sem captura de tela). O texto que o script imprime é
    `vigia: sync ok 23:50 colisao=nao`.
  - Não verificado: se `statusLine` vale também no `.github/copilot/settings.json` do repositório.
- **Codex: não existe item alimentado por script.**
  - Fonte: config-reference, `tui.status_line`, *"Ordered list of TUI footer status-line item identifiers"*.
  - A lista fechada está em `codex-rs/tui/src/bottom_pane/status_line_setup.rs` (`enum StatusLineItem`: modelo,
    pasta, branch, contexto, limites, tokens, `ThreadName`, `ThreadTitle`, `TaskProgress` e outros), sem item de comando.
  - O mais perto: `systemMessage` de um hook, *"Surfaced as a warning in the UI"* (hooks.md), que aparece na hora e
    não fica.
  - Não testado.

## 11. Hooks dentro de um terminal do Maestri: pendente, o maestro roda

Ver o passo a passo no fim. Fato já visto: a variável `MAESTRI_TERMINAL_ID` passa do terminal do Maestri para os hooks
dos harnesses que descendem dele (aqui chegou com o id do terminal do maestro).

## 12. VS Code e a política da empresa

Lista para o Gustavo, no fim.

## O que ficou não verificado

- Codex: a aprovação pela tabela `hooks.state` gravada no `~/.codex/config.toml` (o código diz que vale; testada só a
  forma `-c`); o "solta quando a nota foi tocada" (o `codex exec` não grava arquivo nesta máquina); o plugin com hooks;
  e a causa do erro do sandbox.
- Copilot: confiar na pasta para os hooks e as extensões do repositório; `statusLine` no arquivo do repositório; o que
  a status line mostra na tela; o arquivo global como cópia (e não link) no teste do dobro.
- Claude Code: o `classic.Stop` do mod quando o Claude Code é gerenciado por organização; o `InstructionsLoaded` não
  mostrar o `AGENTS.md` da raiz.
- O tempo do hook de início com o MCP pela tailnet.

## Estado dos arquivos globais (todos restaurados)

Cópias em `C:\Projetos\bancada-acesso\backup-globais\`.

| Arquivo | O que mudou durante o teste | Estado final |
|---|---|---|
| `~/.codex/config.toml` | + confiança do projeto da bancada | restaurado da cópia; `sha256sum -c` OK; `diff` com a cópia vazio |
| `~/.codex/hooks.json` | nada | `sha256sum -c` OK |
| `~/.copilot/hooks/zz-bancada-acesso.json` | criado (hook de usuário) | apagado; a lista da pasta é igual à de antes |
| `~/.copilot/extensions/zz-bancada-fim-retomada/` | criada (extensão) | apagada, com a pasta `extensions/`, que não existia |
| `~/.copilot/copilot-instructions.md` | trocado por link simbólico por um instante | restaurado; mesmo SHA-256; arquivo comum como antes |
| `~/.copilot/settings.json` | criado pelo `--experimental` e depois recebeu `statusLine` | apagado (não existia antes); cópia do que ele tinha em `copilot-settings.criado-pelo-teste.json` |
| `~/.claude/CLAUDE.md` | + uma linha `@import` por um instante | restaurado; `sha256sum -c` OK |
| `~/.claude/settings.json` | nada (tudo por `--settings`, `--plugin-dir` e `--mcp-config`) | intocado |

Ficou fora do restauro, por ser o uso normal: o histórico de sessões que os `-p` criaram (`~/.copilot/session-state`,
`~/.claude/projects/...bancada-acesso`) e a atualização automática do Copilot de 1.0.96 para 1.0.98. Nenhum arquivo de
login ou credencial foi lido, impresso ou copiado. Os processos que eu abri (MCP de teste e Copilot interativo) foram
encerrados pelo PID.

---

## Teste 11, passo a passo para o maestro (Maestri)

Objetivo: o hook de início roda num recruta, e `MAESTRI_TERMINAL_ID` chega a ele com o id **do recruta**, diferente do
id do maestro (`141c914b-2287-4c8c-93a7-8c6772439e73`). Uns 10 minutos.

1. Num terminal (não precisa ser recruta), ligue os globais do teste:
   `python C:\Projetos\bancada-acesso\scripts\globais_maestri.py instalar`. Ele guarda uma cópia do
   `~/.codex/config.toml`, acrescenta a confiança do projeto e o hash do hook de início da bancada (o Codex roda o hook
   sem `/hooks`) e copia o hook de usuário do Copilot. Os scripts saem sem fazer nada fora da bancada.
2. Suba o MCP de teste (para a reserva), num PowerShell:
   `$env:BANCADA_MCP_TOKEN='bancada-fake-7f3a'; Start-Process python 'C:\Projetos\bancada-acesso\scripts\mcp_teste.py' -WindowStyle Hidden -PassThru`.
   Anote o PID.
3. Crie um recruta de teste por harness, com a pasta de trabalho `C:\Projetos\bancada-acesso\papeis\papel-teste`:
   - Claude Code: comando `claude --settings C:/Projetos/bancada-acesso/config/claude-inicio.json` (o hook entra só
     nessa sessão);
   - Codex: comando `codex`;
   - Copilot CLI: comando `copilot`.
   Se o Copilot pedir para confiar na pasta, responda pelo `maestri ask` ou peça o clique ao Gustavo.
4. Mande a cada recruta, por `maestri ask`:
   "Repita a frase SONDA-INICIO e o estado do sync que vieram no início da sessão, e diga o valor da sua variável de
   ambiente MAESTRI_TERMINAL_ID."
5. Confira:
   - em `C:\Projetos\bancada-acesso\logs\inicio.log`, uma linha nova por recruta (`harness` claude/codex/copilot,
     `cwd` = `...\papeis\papel-teste`), com `MAESTRI_TERMINAL_ID` igual ao id do recruta (o que ele respondeu, ou o do
     `maestri list`/`check`) e **diferente** de `141c914b-...`;
   - a resposta de cada recruta com `SONDA-INICIO pinheiro-dourado-07` e o estado `arquivo`;
   - de lambuja, a raiz: o Codex e o Copilot dizerem `SONDA-RAIZ girassol-azul-42` e `SONDA-PAPEL lontra-verde-17`.
6. Opcional, para a reserva: renomeie `vigia\estado-sync.json` para `estado-sync.off`, crie mais um recruta (ou dê
   `/clear`, que dispara `SessionStart` com `source: clear` no Claude Code e no Codex) e confira `origem_estado: mcp`.
   Depois, volte o nome do arquivo.
7. Desfaça tudo: dispense os recrutas de teste; `Stop-Process -Id <PID do MCP>`;
   `python C:\Projetos\bancada-acesso\scripts\globais_maestri.py remover`, que deve imprimir
   `config.toml igual a copia: True` e `hook do Copilot removido: True`.

## Teste 12, lista passo a passo para o Gustavo (VS Code e conta da empresa, uns 10 minutos)

Antes: suba o MCP de teste como no passo 2 acima. Para o Copilot do VS Code e do CLI enxergarem o token, a variável
`BANCADA_MCP_TOKEN=bancada-fake-7f3a` tem de estar no ambiente de quem abre o VS Code. Abra o VS Code a partir desse
mesmo PowerShell, com `code C:\Projetos\bancada-acesso`.

**VS Code com Copilot:**
1. Abra `C:\Projetos\bancada-acesso` no VS Code e o chat do Copilot no modo agente.
2. Paleta de comandos → **"Developer: Policy Diagnostics"**. Anote o que aparece sobre `ChatHooks`, `ChatMCP`,
   `ChatAllowedMcpServers`, `ChatAllowManagedMcpServersOnly` e `ChatStrictPluginOnlyCustomization`. Uma foto da tela
   basta.
3. Hooks de usuário: copie `C:\Projetos\bancada-acesso\.github\hooks\bancada.json` para
   `%USERPROFILE%\.copilot\hooks\zz-bancada-acesso.json`. Abra um chat **novo** e pergunte: "Repita a frase SONDA-INICIO
   que veio no início da sessão". Confira se apareceu uma linha nova em
   `C:\Projetos\bancada-acesso\logs\inicio.log`, e se a resposta traz `pinheiro-dourado-07`.
4. MCP com token: crie `C:\Projetos\bancada-acesso\.vscode\mcp.json` com
   `{ "servers": { "bancada": { "type": "http", "url": "http://127.0.0.1:8799/mcp", "headers": { "Authorization": "Bearer ${env:BANCADA_MCP_TOKEN}" } } } }`.
   A sintaxe `${env:...}` no `mcp.json` do VS Code **não foi verificada** na documentação: se o servidor não subir, troque pelo token escrito direto (é falso). Inicie o servidor pelo link "Start" que o VS Code mostra no arquivo, e no chat peça "chame a ferramenta estado_sync
   do MCP bancada". Confira em `logs\mcp.log` se apareceu `token_ok=True`, e se a resposta traz `SONDA-MCP-ESTADO`.
5. Repita os passos 3 e 4 na sessão do Copilot do tipo "Agent Host / Copilot CLI" do VS Code, se ela aparecer na sua
   lista de sessões: a doc diz que ela só alcança MCP local sem autenticação.
6. Desfaça: apague `%USERPROFILE%\.copilot\hooks\zz-bancada-acesso.json` e a pasta `.vscode` da bancada.

**Copilot CLI com a conta da empresa:**
7. Num PowerShell com `BANCADA_MCP_TOKEN` definido e logado na conta da empresa (`copilot login`, se precisar),
   rode `copilot --additional-mcp-config @C:/Projetos/bancada-acesso/config/copilot-mcp.json` em
   `C:\Projetos\bancada-acesso`.
8. Dentro dele: `/env` (anote se os hooks, as instruções e os MCPs aparecem) e `/mcp`. Veja se o `bancada` aparece
   conectado ou com **"blocked by your enterprise"** (foto da tela).
9. Peça "chame a ferramenta estado_sync do MCP bancada" e confira `token_ok=True` em `logs\mcp.log`.
10. Saia com `/exit` e pare o MCP de teste (`Stop-Process -Id <PID>`).
