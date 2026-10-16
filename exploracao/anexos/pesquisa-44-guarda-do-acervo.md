# Pesquisa 44: guarda do acervo com mods e hooks

Pesquisa em fonte primária, feita em 2026-10-12. Li a skill embutida `plugin-authoring` do Claude Code 2.1.296
(SKILL.md, `reference.md`, `examples/tool-call.ts` e o arquivo de tipos `types/claude-code.d.ts` que o próprio
Claude Code escreve ao carregar a skill), as páginas `.md` brutas de code.claude.com/docs (via `curl`), a doc de
hooks do Codex (`.md` bruto de developers.openai.com/learn.chatgpt.com e `docs/config.md` do repositório
openai/codex), a doc de hooks do Copilot (API de artigos do docs.github.com) e a página de hooks do VS Code (HTML
convertido em texto). Do Maestri: `maestri help` e `maestri workspace --help`, e só os **nomes das chaves** de
`~/.maestri/workspaces/*/workspace.json`. Nada foi instalado, executado (fora os `--help`) ou testado; nenhum
mod ou hook foi criado. É saída de modelo: confira as citações antes de decidir.

Ticket: `.scratch/context-hub/issues/44-guarda-do-acervo-mods-e-hooks-pesquisa.md`. Não repete a pesquisa 43
(tipos de peça do acervo).

## Pergunta

O que um "mod" do Claude Code (e os hooks de que ele depende) consegue fazer como guarda do acervo do maestro,
no uso e na alteração de uma peça: que eventos intercepta, se bloqueia, pede confirmação, avisa, injeta contexto
ou obriga o agente a disparar um subagente com outro modelo antes de seguir; onde mora e como se instala; se
Codex e Copilot têm equivalente; e como a guarda saberia quais workspaces usam a peça. Exemplo do Gustavo: um
maestro em Opus quer alterar uma peça, e a guarda o obriga a disparar um subagente em Sonnet 5.5 que lista os
workspaces que usam a peça, ou detecta se a mudança já roda em algum workspace sem ter virado global.

---

## 1. O que é um mod e do que ele é feito

### A fonte diz

**Definição.** Doc "Mods overview": *"A mod is a [plugin] that changes how Claude Code looks and behaves. It's
made of JavaScript or TypeScript event handlers: Claude Code calls one when an event happens, such as a tool
call, a submitted prompt, or a part of the interface being drawn, and the handler can watch the event, change
it, or take it over."* (https://code.claude.com/docs/en/plugins/mods/overview.md)

**Mod × hook de settings.** Mesma página: *"Claude Code's existing hooks also run on events, as a shell
command, HTTP request, or prompt you configure in a settings file. A mod's handlers are functions that run inside
Claude Code instead. Claude Code calls both kinds hooks: on these pages, "hook" means a mod's handler, and the
settings-file kind is a "settings hook"."* Na skill embutida, o hook de settings é chamado de "classic":
*"The settings hooks' own events are hookable as `classic.<Event>`"* (`plugin-authoring/reference.md`).

**Arquivos.** Skill `plugin-authoring` (SKILL.md): três arquivos, *"`.claude-plugin/plugin.json`"*,
*"`hooks/hooks.json`: `{ "modules": ["./register.tsx"] }`"* e *"`hooks/register.tsx` (or `.ts`): the hooks
module, `export const register: Register = (on, options) => { ... }`"*. A doc "Mods reference" acrescenta que o
`hooks.json` *"Can also hold [settings hooks] under `hooks`"* (https://code.claude.com/docs/en/plugins/mods/reference.md).

**Forma de um hook.** SKILL.md: *"`on(event, matcher?, hook)` adds a hook, and every hook is `($, e, next)`: `$`
is the engine interface ... `e` is the event's input ... `next(e)` runs the plugins beneath and then the
engine's own behaviour"*; *"A hook that returns without `next` answers for itself"*. O módulo *"runs in an
environment of its own, with no DOM and no Node: `$` reaches everything outside it."*

**Do que um mod pode ser feito** (tabela da SKILL.md "From the ask to the shape"):

| Peça | Como a fonte descreve |
| :- | :- |
| Painel (pane) | *"`$.ui.open({ id, title })`, drawn by a `ui.render` hook on `{ component: 'Pane', requestId: id }`"* |
| Faixa acima do prompt | *"a `ui.render` hook on `{ component: 'AbovePrompt' }`"* |
| Linha de status, toast | *"`$.ui.status(text)`"*, *"`$.ui.toast(text)`"* |
| Bloquear/reescrever chamada de ferramenta | *"`on('tool.call', { tool }, hook)`: return `{ deny }`, call `next({ ...e, ... })`, or `await next(e)` and act on the result"* |
| Mexer no prompt / no system prompt | *"`on('prompt.submit', hook)`"*, *"`on('prompt.compose', hook)`"* |
| Comando de barra | *"`$.command.register({ name, description })` in `session.start`, answered by a `command.run` hook"* |
| Timer, ferramenta, tipo de subagente, chamada de modelo, arquivos, processos | *"`$.clock`, `$.tool`, `$.agent`, `$.model`, `$.fs`, `$.process`"* |

**Alcance.** "Mods overview", seção "What a mod can reach": *"Act on your machine as you: read and write files
anywhere your user account can, start programs, and make network requests"*; *"See your session: every prompt
you send and every tool call Claude makes"*; *"Act without asking you: approve a tool call before you're
asked"*; *"Spend your usage: call a model on your plan or API key"*. E: *"Mods aren't sandboxed."*

**Versão e estado.** *"Mods are on by default. In the terminal, use Claude Code v2.1.287 or later."* O arquivo de
tipos avisa: *"EARLY ACCESS: this surface may change between releases without notice."*
(`types/claude-code.d.ts`, cabeçalho, escrito pelo Claude Code 2.1.296).

**Onde rodam** (tabela "Where mods run"): terminal *"Yes"*; *"The VS Code extension's chat panel | Yes | No"*
(hooks rodam, nada é desenhado); *"`claude -p` and the Agent SDK | Yes | No"*; *"A WSL session in the Desktop
app | No, because plugins aren't available in WSL sessions"*.

**Comparação oficial** (mesma página): o hook de settings muda *"Whether a tool call or prompt goes ahead, a
tool call's arguments and result, and context added for Claude"*; o mod muda *"Tool calls, prompts, commands,
turns, and what the interface draws"*.

---

## 2. Como guarda do acervo: eventos, decisões e garantia

### 2a. Hooks de settings (o tipo "clássico", em JSON)

#### A fonte diz

**Eventos úteis para a guarda** (https://code.claude.com/docs/en/hooks.md, tabela inicial):

- `PreToolUse`: *"Before a tool call executes. Can block it"*. Casa pelo nome da ferramenta (`Edit|Write`,
  `Bash`, `Skill`, `Agent`...).
- `UserPromptExpansion`: *"When a user-typed command expands into a prompt, before it reaches Claude. Can block
  the expansion"*. A doc explica a lacuna que ele cobre: *"a `PreToolUse` hook matching the `Skill` tool fires
  only when Claude calls the tool, but typing `/skillname` directly bypasses `PreToolUse`.
  `UserPromptExpansion` fires on that direct path."*
- `UserPromptSubmit`, `Stop`, `SubagentStart`, `SubagentStop`, `InstructionsLoaded` (só CLAUDE.md e
  `.claude/rules`), `ConfigChange` (matcher inclui `skills`), `FileChanged`.

**Filtro por caminho.** Campo `if`: *"Permission rule syntax to filter when this hook runs, such as
`"Bash(git *)"` or `"Edit(*.ts)"`"*. Aviso da própria doc: *"Because the `if` filter is best-effort, use the
permission system rather than a hook to enforce a hard allow or deny."* No Windows, regras de caminho:
*"`C:\Users\alice` becomes `/c/Users/alice`, so use `//c/**/.env`"* (https://code.claude.com/docs/en/permissions.md).

**Decisões do `PreToolUse`**: *"`"allow"` skips the permission prompt ... `"deny"` prevents the tool call.
`"ask"` prompts the user to confirm. `"defer"` exits gracefully"*; *"When multiple PreToolUse hooks return
different decisions, precedence is `deny` > `defer` > `ask` > `allow`."* O `ask` mostra a origem: *"`[settings]`
... `[plugin:<name>]` for a plugin's hook, or `[skill]` for a hook from skill frontmatter"*, e vale em auto mode:
*"A hook's `"ask"` also forces a permission prompt in auto mode"*.

**Injetar contexto.** `additionalContext`: *"Claude Code wraps the string in a system reminder and inserts it
into the conversation at the point where the hook fired."* Em `PreToolUse` fica *"next to the tool result"*; em
`Stop`, *"The conversation continues so Claude can act on the feedback."* A doc pede texto factual: *"Text
framed as out-of-band system commands can trigger Claude's prompt-injection defenses"*.

**Obrigar a continuar.** `Stop`: *"`"block"` prevents Claude from stopping"*, com limite: *"the
8-consecutive-continuation cap"*.

**Hooks que chamam modelo.** Cinco tipos de handler: *"`command`, `http`, `mcp_tool`, `prompt`, or `agent`"*.

- `prompt`: *"send a prompt to a Claude model for single-turn evaluation"*; resposta `{"ok": true|false,
  "reason": ...}`.
- `agent`: *"spawn a subagent that can use tools like Read, Grep, and Glob to verify conditions before
  returning a decision. Agent hooks are experimental and may change."* *"After up to 50 turns, the subagent
  returns a structured `{ "ok": true/false }` decision"*. Vale em `PreToolUse`, `Stop`, `UserPromptSubmit`,
  `UserPromptExpansion`, entre outros, mas não em `PermissionRequest`.
- **Modelo escolhido:** campo `model`, *"Model to use for evaluation. Defaults to the model Claude Code uses for
  background functionality"*. A configuração do `agent` é *"the same as prompt hooks"*, então aceita `model`.
- **Tempo:** padrão *"30 for `prompt`; 60 for `agent`"* segundos, ajustável por `timeout`.
- **Efeito do `ok: false` no `PreToolUse`:** prompt hook, *"the tool call is denied; by default the turn ends"*,
  ou, com `continueOnBlock: true`, *"return the reason to Claude as the tool error so it can adjust and
  continue"*. Agent hook: tratado *"the same way as a prompt hook with `continueOnBlock: true`"*.

**Hooks numa skill.** Frontmatter `hooks` de uma skill: *"Claude Code registers them when you or Claude invoke
the skill and keeps running them for the rest of the session"*. Ou seja, uma peça do acervo pode trazer a
própria guarda, que só passa a valer depois que a peça é usada.

**Subagentes.** *"Hooks from settings files, managed policy settings, and plugins also run inside subagents."*

#### Garantia

O hook `agent` com `model` é disparado **pelo harness**, não pelo maestro: o Opus não decide se ele roda. Isso é
força de fato sobre "rodar a verificação em outro modelo antes da ferramenta". Mas a doc marca o tipo `agent`
como experimental, e o `if` como "best-effort". Sobre a ferramenta Bash: um `PreToolUse` em `Edit|Write` não pega
uma escrita feita por `Bash`/`PowerShell` (`cp`, `Set-Content`). A doc não diz o que acontece quando um hook
`prompt`/`agent` estoura o tempo (não verificado).

### 2b. Mods (handlers em TypeScript)

#### A fonte diz

**Eventos** (https://code.claude.com/docs/en/plugins/mods/reference.md):

| Evento | Quando | O que o hook devolve |
| :- | :- | :- |
| `tool.call` | *"A tool is about to run"* (inclui subagentes: *"including calls a subagent makes"*) | *"`next(e)`, `{ deny: reason }`, or `{ result }`"* |
| `tool.check` | decisão de permissão, *"after the `tool.call` and `PreToolUse` hooks"* | *"`{ decision }`, which is `allow`, `ask`, or `deny`"* |
| `skill.prompt` | *"A skill's text is expanded for Claude"* | *"`{ text }`"* |
| `prompt.submit` | prompt enviado | reescrever, `context`, ou *"`{ drop: reason }`"* |
| `agent.spawn` | *"A subagent or an agent team teammate is about to start"* | *"`next({ ...e, model })` to choose its model, or `{ deny: reason }`"* |
| `agent.offer` | tipo de subagente oferecido ao modelo | *"`{ isOffered: false }` to withhold it"* |
| `turn.complete` | fim do turno | *"`next(e)`, or `{ text }` to show a line under the answer"* |
| `classic.<Event>` | os eventos dos hooks de settings | (reference.md da skill) |

`skill.prompt` cobre os três caminhos de uso de uma skill: *"Typed as `/name`, called through the Skill tool,
or preloaded into a subagent: the same event at each."* (`types/claude-code.d.ts`, `SkillPromptInput`).

**Segurar a chamada e pedir aval.** "React to events with a mod": *"A `tool.call` hook can `await` before it
calls `next` or returns, and the tool call stays pending until then. To put the question to the user, call
`$.ui.ask`."* E: *"`$.ui.ask` rejects when the user dismisses the question or picks Chat about this, and in a
`claude -p` run"* (https://code.claude.com/docs/en/plugins/mods/events.md).

**Disparar subagente e escolher o modelo.**
- O próprio mod dispara: `$.agent.spawn`, *"Spawns a subagent: the event `agent.spawn`, the same call the engine
  makes when the Agent tool starts one"*; resolve *"`{ model, agentId }` once the subagent started (its answer is
  its `turn.complete`)"*. `AgentSpawnArgs` aceita `prompt`, `description`, `subagentType`, `model`, `name`, `cwd`
  (`types/claude-code.d.ts`).
- O mod impõe o modelo de um subagente que o maestro dispara: no `agent.spawn`, *"A hook sets this to pick the
  subagent's model."* (campo `model`), exceto em fork: *"Ignored for forks, which always inherit."*
- Chamada direta de modelo, sem ferramentas: `$.model.complete({ model, prompt })` (*"runs one text completion
  with no history on the session's own client"*, reference.md da skill).
- `$.agent.list()`: *"Returns the session's agents so far"*.

**Tempo (a parte que decide o desenho).** *"A hook's own execution time for one event, not counting time inside
`next` or a mods API call other than `$.clock.sleep` | 10 seconds"*; *"A `.catch` handler's execution time | 1
second"*. E a doc de eventos: *"Keep the wait inside a mods API call such as `$.ui.ask`, because that time
doesn't count against the hook's time limit. Time spent awaiting a promise of your own does count. Claude Code
skips a hook that times out, so the held command would run."* Consequência literal: `$.model.complete` e
`$.ui.ask` não gastam o orçamento; esperar a resposta de um `$.agent.spawn` (que chega por `turn.complete`, numa
promessa do próprio mod) gasta.

**Falhar fechado.** *"To make a hook that blocks calls fail closed, add a `.catch` error handler that answers in
its place"*; modelo da skill: *"`on(...).catch(($, e, next) => next.called ? next(e) : { deny: 'why' })`"*.

**Caminhos com link.** reference.md da skill: *"`$.fs.stat(path, { resolve: true })` also answers `realPath`,
every symbolic link and `..` resolved ... so a guard's robust form is an allow-list on `realPath` under a root it
resolved the same way, and a deny-list on spellings is best effort."*

**Ordem e precedência.** *"Hooks in your organization's managed settings run before any mod's `tool.call`
hook"*; os `PreToolUse` de settings comuns e de plugins *"run after the last mod calls `next`"*; *"A mod that
answers `tool.call` without calling `next` keeps them from running"*. E o aviso de segurança: *"A mod that
approves tool calls can approve one that an `ask` rule would prompt for, or that one of your own `PreToolUse`
hooks blocked."*

### 2c. Resposta curta à pergunta 2

| Pergunta | Hook de settings | Mod |
| :- | :- | :- |
| Pega gravação numa pasta? | Sim, `PreToolUse` em `Edit\|Write` com `if` de caminho (best-effort) | Sim, `tool.call` lendo `e.file_path`; pode resolver link com `$.fs.stat` |
| Pega uso de skill? | `PreToolUse` em `Skill` + `UserPromptExpansion` | `skill.prompt` (os três caminhos) |
| Bloqueia? | Sim (`deny`, exit 2) | Sim (`{ deny }`) |
| Pede confirmação? | Sim (`ask`) | Sim (`$.ui.ask`, ou `ask` em `tool.check`) |
| Avisa / injeta contexto? | `additionalContext`, `systemMessage` | `context` no resultado, `$.ui.toast`/`status`, reescrever `skill.prompt` |
| Roda outro modelo antes? | Sim, hook `agent`/`prompt` com `model`, disparado pelo harness | Sim, `$.model.complete` (livre de orçamento) ou `$.agent.spawn` (espera conta no orçamento) |
| Obriga o **maestro** a disparar o subagente? | Só instrui (texto do `deny`/`Stop`); o que força é o próprio hook rodar o verificador | Força de fato se o mod recusa a edição até existir o relatório; o modelo do subagente é imposto em `agent.spawn` |

### Sugestão de desenho: o exemplo do Gustavo

(Não é fonte; é composição das peças acima.)

1. **Saber que é peça do acervo.** O mod resolve o caminho real (`$.fs.stat(..., { resolve: true })`) e compara
   com a raiz do acervo no hub, também resolvida. Isso cobre gravar pelo caminho da junction em
   `~/.claude/skills/...` ou pelo caminho real em `C:\context-hub\...`.
2. **Recusar a primeira tentativa** (`tool.call` em `Edit`/`Write`/`NotebookEdit`, e um filtro best-effort em
   `Bash`/`PowerShell`): `{ deny: "Esta peça é citada por outras. Antes de alterar, dispare o subagente
   acervo-impacto ..." }`. O texto é instrução para o Opus; sozinho, só instrui.
3. **Impor o modelo do verificador**: o mod registra o tipo `acervo:impacto` (`$.agent.register`) e, no
   `agent.spawn` desse tipo, troca `model` para Sonnet. Mesmo que o Opus peça outro modelo, o hook decide.
4. **Liberar só com relatório e aval**: o relatório do subagente (lido no `turn.complete` dele) vai para
   `$.state`/`$.store` com o hash da peça. Na próxima tentativa de gravação, o mod confere se há relatório para
   aquele hash e pede o aval por `$.ui.ask` (a espera não gasta orçamento). Sem relatório ou sem aval, `deny`.
   Com `.catch` fechado.
5. **Alternativa mais simples, sem LLM:** listar workspaces é leitura de arquivos (seção 5). O mod pode montar a
   lista com `$.fs` dentro do próprio hook e usar `$.model.complete({ model: "sonnet" })` só para resumir o
   impacto. Ou, só com JSON: um hook de settings `PreToolUse` do tipo `agent` com `"model": "sonnet"` e `if`
   no caminho do acervo, mais um hook `command` que devolve `ask`. É o caminho de menos código, mas experimental
   e sem pegar `Bash`.

O "detectar se a mudança já roda em algum workspace sem ter virado global" cabe no mesmo verificador: comparar
o conteúdo da peça global com cópias locais (ver seção 5).

---

## 3. Onde mora e como se instala; papéis do Maestri

### A fonte diz

**Hooks de settings** (https://code.claude.com/docs/en/hooks.md, "Hook locations"): `~/.claude/settings.json`
(*"All your projects"*), `.claude/settings.json` e `.claude/settings.local.json` (projeto), managed, plugin
`hooks/hooks.json` (*"When plugin is enabled"*), frontmatter de skill e de subagente.

**Mods.** São plugins. Formas de carregar:
- **Instalar de um marketplace**, com escopo: *"User scope: the plugin is enabled for you in every project on
  this machine. The entry goes in `enabledPlugins` in `~/.claude/settings.json`."*
  (https://code.claude.com/docs/en/plugins/install.md). Um marketplace pode ser uma pasta local: *"A relative
  or absolute path to a directory that holds `.claude-plugin/marketplace.json`"*. E esse plugin é lido no
  lugar, sem cópia: *"Relative-path plugins in a marketplace you added from a local path: the plugin loads in
  place from its path inside the marketplace folder. Your edits to the source directory take effect at the next
  session start or `/reload-plugins`"* (https://code.claude.com/docs/en/plugins/loading.md).
- **Pasta de skills como plugin**: *"add a `.claude-plugin/plugin.json` to a skill folder and it loads as a
  plugin named `<name>@skills-dir`, so it can bundle agents, hooks, and MCP servers"*
  (https://code.claude.com/docs/en/skills.md). Ativação: *"The manifest's `defaultEnabled`, unless a settings
  file sets `"<name>@skills-dir"` to `true` or `false`"*; e *"`--plugin-dir` and skills-directory plugins: the
  directory loads in place and is never copied"* (loading.md). A skill embutida confirma que esse plugin é
  vigiado: *"a plugin auto-loaded from a skills folder (`~/.claude/skills/<name>`, the project's
  `.claude/skills/<name>`)"*.
- **`CLAUDE_CODE_PLUGIN_DIRS`**: *"Environment, or `env` in `~/.claude/settings.json` | Plugin directories to
  load as `--plugin-dir` does ... Absolute paths separated by `:`, or `;` on Windows."* (mods reference).

**Links.** Skills: *"a `<skill-name>` entry in the enterprise, personal, or project location can be a symlink to
a directory elsewhere on disk"* (skills.md). Plugins: *"A plugin folder given as a link is watched at the folder
the link names."* (reference.md da skill). A doc fala de **symlink**; junction do Windows não é citada.
Regras de permissão atravessam link só em parte: *"On macOS and Linux, a deny or ask rule written through a
symlinked directory ... also applies at the directory's real location"* (permissions.md). O Windows não está
nessa frase.

**Projeto × pasta do papel.** *"Claude Code reads the shared `.claude/settings.json` from the session's primary
working directory"* (https://code.claude.com/docs/en/settings.md). Para plugins de `.claude/skills/` do projeto:
*"a plugin at the repository root doesn't load. Claude Code reads the `.claude/skills/` of the session's primary
working directory and, unlike plain skills and commands, doesn't search parent directories for plugins"*
(loading.md). A pesquisa 37 (porta 3-4) já registrou que um papel do Maestri abre em
`<workspace>/.maestri/roles/<id>/`.

**Desligar.** *"`"disableAllHooks": true` in `~/.claude/settings.json`. Your settings hooks and custom status
line stop too."*; *"start Claude Code with `--safe-mode`"* (mods overview).

### Resposta

- No escopo **usuário** (`~/.claude/settings.json`, plugin instalado em escopo user, ou plugin em
  `~/.claude/skills/<nome>`), a guarda vale em qualquer pasta, **inclusive dentro de um papel do Maestri**,
  porque não depende do diretório de trabalho.
- No escopo **projeto**, um terminal com papel lê `.claude/settings.json` e plugins de `.claude/skills/` da pasta
  do papel, não da raiz do workspace. Pela doc, guarda posta só na raiz do workspace **não** alcança o papel.

### Sugestão de desenho

A guarda pode morar no hub como uma pasta de plugin (com `.claude-plugin/plugin.json`, `hooks/hooks.json` e o
módulo) e entrar no Claude Code por um destes caminhos: (a) a mesma junction que já leva o acervo para
`~/.claude/skills/<nome>`, se o Claude Code aceitar junction (precisa de teste); (b) `CLAUDE_CODE_PLUGIN_DIRS`
apontando para a pasta do hub, no `env` de `~/.claude/settings.json`; (c) o hub como marketplace local,
instalado em escopo user. O (c) é o que a doc descreve com mais detalhe (lido no lugar, recarrega com
`/reload-plugins`).

---

## 4. Equivalentes no Codex e no Copilot

### Codex CLI

**A fonte diz** (https://learn.chatgpt.com/docs/hooks.md, mesma página de developers.openai.com/codex/hooks):

- Eventos: *"`PreToolUse`, `PermissionRequest`, `PostToolUse`, `PreCompact`, `PostCompact`,
  `UserPromptSubmit`, `SubagentStop`, `Stop`"*, mais `SessionStart`, `SubagentStart`, `SessionEnd`, `Interrupt`.
- Onde: *"`~/.codex/hooks.json`, `~/.codex/config.toml`, `<repo>/.codex/hooks.json`, `<repo>/.codex/config.toml`"*;
  plugins com `hooks/hooks.json`.
- Confiança: *"Before a non-managed hook can run, Codex requires you to review and trust the exact hook
  definition. Codex records trust against the hook's current hash"*.
- Edição de arquivo: *"`apply_patch` | Match as `apply_patch`, `Edit`, or `Write`"*; a entrada traz
  *"`tool_input.command`"* (o texto do patch, não um `file_path`).
- Decisões no `PreToolUse`: `deny` e `updatedInput` com `allow`; mas *"`permissionDecision: "ask"` ... are parsed
  but not supported yet. Codex marks the hook run as failed, reports the error, and continues the tool call."*
- `PermissionRequest`: *"runs when Codex is about to ask for approval ... It can allow the request, deny the
  request, or decline to decide and let the normal approval prompt continue."*
- `Stop`: *"`decision: "block"` ... tells Codex to continue and automatically creates a new continuation prompt"*.
- Subagente: `SubagentStart` só injeta contexto; *"`continue: false` ... doesn't stop the subagent from
  starting."*
- Hooks com modelo: *"`command` and `mcp_tool` handlers are supported. `prompt` and `agent` handlers are parsed
  but skipped."*
- Windows: *"`commandWindows` is an optional Windows-only command override."*
- Limite declarado: *"Some specialized tool paths can opt out of the default hook path. Treat tool hooks as a
  useful guardrail, not a complete enforcement boundary."*
- Caminho fora do workspace: *"Codex asks for approval to edit files outside the workspace"*; e no sandbox
  `workspace-write`, *"`<writable_root>/.agents` is protected as read-only when it exists as a directory."*
  (https://learn.chatgpt.com/docs/agent-approvals-security.md). As regras (`.rules`) só tratam comandos:
  *"Use rules to control which commands Codex can run outside the sandbox."*
  (https://learn.chatgpt.com/docs/agent-configuration/rules.md).
- **Não existe** no Codex: mod (handler em processo), hook `prompt`/`agent` que rode outro modelo, `ask` vindo
  de hook no `PreToolUse`, evento próprio de uso de skill (não achei na doc lida).

### GitHub Copilot CLI

**A fonte diz** (https://docs.github.com/en/copilot/reference/hooks-configuration, via API de artigos):

- Fontes: *"Policy-level hook files"*, *"`.github/hooks/*.json` in the repository root"*, *"`~/.copilot/hooks/`
  on macOS and Linux, or `%USERPROFILE%\.copilot\hooks\` on Windows"*, `~/.copilot/settings.json` e plugins. E:
  *"Cross-tool `.claude/settings.json` and `.claude/settings.local.json` files in the repository are also read."*
- `preToolUse`: *"`permissionDecision` | `"allow"`, `"deny"`, `"ask"`"*, mais `modifiedArgs`.
- Falha: *"`preToolUse` command hooks are fail-closed on exit `2` and on non-timeout errors"*; mas
  *"Timeouts are always fail-open"*. Padrão: *"default: 30"* segundos (`timeoutSec`).
- `agentStop`/`subagentStop`: *"`"block"` forces another agent turn using `reason` as the prompt."*
- `subagentStart`: *"cannot block creation, but `additionalContext` is prepended to the subagent's prompt."*
- Hook "prompt" do Copilot é outra coisa: *"Prompt hooks auto-submit text as if the user typed it. They are only
  supported on `sessionStart`."* Não há hook que chame um modelo para dar veredito.
- Ferramentas casáveis: `create`, `edit`, `apply_patch`, `view`, `powershell`, `task` (*"Run subagents"*),
  `skill` (*"Invoke custom skills"*) (https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-command-reference).
- Caminho por regra: *"`--deny-tool='write(PATH)'` scopes the denial to that path ... The match resolves
  symlinks and `.`/`..` segments, and is case-insensitive on macOS and Windows."*, com *"no glob support yet"*.

### GitHub Copilot no VS Code

**A fonte diz** (https://code.visualstudio.com/docs/copilot/customization/hooks):

- *"The VS Code hooks experience is in Preview."* Quem roda o hook depende do "Session Target": sessões Copilot
  no Agent Host usam *"Shared Copilot SDK implementation"* (a mesma referência do Copilot CLI); sessões Claude
  usam *"Claude Agent SDK"*; sessões Codex usam *"Codex runtime"*; e há o harness *"Local"*.
- Local: eventos `SessionStart`, `UserPromptSubmit`, `PreToolUse` (*"Block an operation, request approval, or
  change tool input"*), `PostToolUse`, `PreCompact`, `SubagentStart`, `SubagentStop`, `Stop`. Arquivos
  `.github/hooks/*.json`, `~/.copilot/hooks/*.json`, e o formato Claude só com `chat.useClaudeHooks` (desligado
  por padrão), que *"ignores matcher values, so every command for the event runs."*
- Aviso: *"This file compatibility does not make their behavior identical."*
- Aprovação por caminho: *"Configure `chat.tools.edits.autoApprove` with glob patterns (for example,
  `"**/.env": false`) to require manual approval for edits to sensitive files."*
  (https://code.visualstudio.com/docs/copilot/security).
- Mods do Claude Code na extensão do VS Code: hooks rodam, nada é desenhado (tabela da seção 1).

---

## Tabela: harness × capacidade de guarda

| Capacidade | Claude Code (mod) | Claude Code (hook de settings) | Codex CLI | Copilot CLI | Copilot VS Code (Local) |
| :- | :- | :- | :- | :- | :- |
| Interceptar gravação de arquivo | `tool.call` (`file_path`) | `PreToolUse` `Edit\|Write` + `if` | `PreToolUse` `apply_patch` (patch em texto) | `preToolUse` `edit`/`create` | `PreToolUse` |
| Interceptar uso de skill | `skill.prompt` | `PreToolUse` `Skill` + `UserPromptExpansion` | não achado | `preToolUse` `skill` (por nome da ferramenta) | não verificado |
| Bloquear | sim | sim | sim | sim (falha fecha, timeout abre) | sim |
| Pedir confirmação ao humano | `$.ui.ask`, `tool.check` `ask` | `ask` | não por `PreToolUse`; `PermissionRequest` só onde já haveria aprovação | `ask` | "request approval" |
| Injetar contexto | sim | `additionalContext` | `additionalContext` | `additionalContext` (alguns eventos) | sim |
| Rodar outro modelo como verificador | `$.model.complete`, `$.agent.spawn` | hook `prompt`/`agent` com `model` (agent experimental) | não (`prompt`/`agent` ignorados) | não | não verificado |
| Impor o modelo de um subagente | `agent.spawn` → `model` | não (frontmatter `model` do subagente é fixo, não condicional) | não verificado | não verificado | não verificado |
| Forçar continuar o turno | não verificado em mod; `classic.Stop` | `Stop` `block` (máx. 8) | `Stop` `block` | `agentStop` `block` (máx. 8) | `Stop` |
| Regra fixa por caminho, sem código | regras `Edit(//c/...)` | idem | aprovação fora do workspace | `--deny-tool='write(PATH)'` | `chat.tools.edits.autoApprove` |
| Global para o usuário | plugin user / `~/.claude/skills/<x>` / `CLAUDE_CODE_PLUGIN_DIRS` | `~/.claude/settings.json` | `~/.codex/hooks.json` | `~/.copilot/hooks/*.json` | `~/.copilot/hooks/*.json` |

---

## 5. Como a guarda saberia quais workspaces usam a peça

### A fonte diz

- `maestri help`: *"maestri workspace list (Maestro only) Print the sidebar hierarchy (pinned, groups, folders,
  workspaces) with directories"*; *"maestri role list (Maestro only) List role presets, grouped by current
  workspace vs global"*; *"maestri role delete "Name" [--force] (Maestro only) Delete a role; --force also
  unassigns it from any terminals still using it"*. Nenhum comando lista **quais terminais ou workspaces usam**
  um papel, preset ou skill. Todos esses são "Maestro only": um hook comum (fora de um terminal maestro) talvez
  não possa chamá-los (não verificado).
- Arquivos (só nomes de chave lidos em 2026-10-12, nada copiado): cada `~/.maestri/workspaces/<id>/workspace.json`
  tem `payload.workingDirectory` e `payload.nodes[].content.terminal._0` com chaves que incluem `agentType`,
  `assignedRoleId`, `command`, `isManager` e `workingDirectory`. São 8 workspaces e 48 terminais; os arquivos têm
  de 2,6 KB a 89 KB (abaixo do limite de 4 MiB do `$.fs.read`). A pesquisa 37 já registrou `preferences.json` →
  `payload.rolePresets` (com `workspaceId`) e `<workspace>/.maestri/roles/<id>/role.json`. Esses formatos não têm
  doc pública (não verificado como contrato estável).
- O Maestri não registra uso de skill. O que registra uso de skill é o próprio harness: o Claude Code passa
  `transcript_path` a cada hook (doc de hooks, "Common input fields"); o formato do transcript não foi lido.

### Sugestão de desenho

- **"Quem usa a peça" para papéis:** varrer `workspace.json` atrás de `assignedRoleId` igual ao id do papel, e
  `preferences.json` atrás do escopo (com ou sem `workspaceId`). Para setups e presets: procurar o nome no
  `command` dos terminais.
- **"Quem usa a peça" para skills:** o Maestri não sabe. Duas fontes possíveis: (a) um hook de uso
  (`skill.prompt` no mod, ou `PreToolUse` `Skill` + `UserPromptExpansion`) que grava num registro do hub
  "peça X usada no workspace Y" (o `MAESTRI_WORKSPACE_ID` está no ambiente do terminal, pesquisa 37); (b) varrer
  os transcripts.
- **"Já roda num workspace sem ter virado global":** para cada `workingDirectory` de workspace, procurar cópias
  locais da peça (`.claude/skills/<nome>`, `.agents/skills/<nome>`, `.maestri/roles/*/role.json`, papéis com
  `workspaceId`) e comparar o conteúdo com a versão global do hub.
- Tudo isso é leitura de arquivo e cabe num `command` hook, num mod (`$.fs`) ou num subagente com `Read`/`Grep`.
  O modelo (Sonnet) só é necessário para resumir ou julgar o impacto, não para achar os workspaces.

---

## Não verificado

- O que acontece quando um hook `prompt` ou `agent` do Claude Code estoura o tempo (bloqueia ou deixa passar).
- Se o subagente de um hook `agent` pode usar `Bash`; a doc cita *"tools like Read, Grep, and Glob"*.
- O id exato do Sonnet 5.5 para o campo `model`; a doc de subagentes lista os apelidos `sonnet`, `opus`, `haiku`,
  `fable` e o exemplo `claude-opus-5-5`.
- Se um mod pode forçar a continuação do turno além de `classic.Stop` (não achei campo para isso em
  `TurnCompleteResult`, que só tem `text` e `usage`).
- Evento de uso de skill no Codex e no Copilot do VS Code.
- Se o Codex e o Copilot, rodando como harness dentro do VS Code ou do Maestri, leem os hooks do usuário do mesmo
  jeito que na CLI.
- Se os comandos "Maestro only" respondem quando chamados por um hook ou por um terminal que não é maestro.
- Estabilidade do formato de `workspace.json` e `preferences.json` do Maestri (sem doc).
- A API de mods é "early access" e muda entre versões; tudo da seção 2b vale para o Claude Code 2.1.296.

## Precisa de teste

- Se o Claude Code carrega como plugin `@skills-dir` uma pasta de `~/.claude/skills/` que é **junction** (a doc
  fala de symlink) e se a observa para recarregar.
- Se regras `deny`/`ask` e o `if` de um hook pegam a gravação pelos dois caminhos no Windows (o da junction em
  `~/.claude/skills/...` e o real em `C:\context-hub\...`).
- Se um mod consegue esperar, dentro do orçamento de 10 s, a resposta de um subagente disparado por
  `$.agent.spawn`; a doc diz que esperar promessa própria conta no orçamento, então o desenho de "recusar, depois
  liberar com relatório" parece o seguro.
- Se `$.ui.ask` aparece e espera num terminal do Maestri que ninguém está olhando, e o que acontece com o
  maestro enquanto isso.
- Se um hook `agent` com `"model": "sonnet"` roda mesmo com o maestro em Opus, e quanto tempo leva com os
  workspaces reais.
- Se o Copilot CLI aplica os hooks do `.claude/settings.json` do repositório com os nomes de ferramenta do Claude
  (`Edit|Write`) ou só com os seus (`edit`, `create`).
- Se um `command` hook do Codex pode chamar outro agente (por exemplo `claude -p --model sonnet`) dentro do
  `timeout`, como substituto do hook `agent` que o Codex ignora.
- Como cada harness se comporta dentro da pasta de um papel (`.maestri/roles/<id>/`) com hooks de usuário.

## Fontes

Claude Code (curl dos `.md`, 2026-10-12):
- https://code.claude.com/docs/en/hooks.md (Hook lifecycle, Hook locations, Matcher patterns, Common fields,
  Prompt and agent hook fields, Hooks in skills and agents, Add context for Claude, Decision control, PreToolUse
  decision control, Stop decision control, UserPromptExpansion, Prompt-based hooks, Agent-based hooks, Windows
  PowerShell tool)
- https://code.claude.com/docs/en/plugins/mods/overview.md
- https://code.claude.com/docs/en/plugins/mods/events.md (Guard or change a tool call, Hold a tool call until
  the user decides, Approve or refuse a tool call, The order mods run in, Handle a hook that fails)
- https://code.claude.com/docs/en/plugins/mods/reference.md (Files, Events, Subagents, Limits, Settings and
  environment variables)
- https://code.claude.com/docs/en/plugins/install.md (Choose an install scope, Add a marketplace)
- https://code.claude.com/docs/en/plugins/loading.md (Find where a plugin came from, Plugins shared through a
  repository, In-place and copied plugins)
- https://code.claude.com/docs/en/skills.md (Choose where skills load; frontmatter `model` e `hooks`)
- https://code.claude.com/docs/en/sub-agents.md (frontmatter `model`, `hooks`)
- https://code.claude.com/docs/en/settings.md (leitura de `.claude/settings.json` do diretório de trabalho)
- https://code.claude.com/docs/en/permissions.md (regras de caminho, Windows, symlink)

Skill embutida `plugin-authoring` do Claude Code 2.1.296 (pasta temporária da sessão):
- `SKILL.md`, `reference.md`, `examples/tool-call.ts`
- `types/claude-code.d.ts`: `EventCalls`, `AgentSpawnArgs`, `AgentSpawnInput`, `AgentSpawnResult`, `agent`
  (`spawn`, `list`, `register`), `ToolCallResult`, `ToolCheckResult`, `SkillPromptInput`,
  `TurnCompleteResult`, `PromptSubmitResult`, `HookBudget`

Codex:
- https://learn.chatgpt.com/docs/hooks.md (mesmo texto de https://developers.openai.com/codex/hooks)
- https://raw.githubusercontent.com/openai/codex/main/docs/config.md (Lifecycle hooks)
- https://learn.chatgpt.com/docs/agent-approvals-security.md
- https://learn.chatgpt.com/docs/agent-configuration/rules.md

GitHub Copilot:
- https://docs.github.com/en/copilot/concepts/agents/coding-agent/about-hooks
- https://docs.github.com/en/copilot/reference/hooks-configuration
- https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-command-reference (Tool permission
  patterns, tool names)
- https://code.visualstudio.com/docs/copilot/customization/hooks
- https://code.visualstudio.com/docs/copilot/security

Maestri e arquivos locais (só leitura):
- `maestri help`, `maestri workspace --help`
- `C:\Users\gustavo.delfino\.maestri\workspaces\*\workspace.json` (só nomes de chave, contagens e tamanhos)
- `exploracao/anexos/pesquisa-37-portas/porta-3-4-maestri.md`
