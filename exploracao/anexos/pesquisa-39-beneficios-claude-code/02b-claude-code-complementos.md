---
title: "Claude Code — complementos (memória, settings, fast mode, modelos, worktrees, contexto, SDK, hooks)"
data: 2026-10-10
origem: "subagente de pesquisa (Sonnet 5.5), ticket 39"
fontes:
  - https://code.claude.com/docs/en/memory
  - https://code.claude.com/docs/en/settings
  - https://code.claude.com/docs/en/fast-mode
  - https://code.claude.com/docs/en/model-config
  - https://code.claude.com/docs/en/worktrees
  - https://code.claude.com/docs/en/context-window
  - https://code.claude.com/docs/en/agent-sdk/overview
  - https://code.claude.com/docs/en/headless
  - https://code.claude.com/docs/en/hooks
---

> Aviso: saída de modelo (subagente), não revisada pelo Gustavo. As citações em inglês foram copiadas das páginas oficiais acima, buscadas em 2026-10-10 via WebFetch; o que não foi conferido está em "Não verificado". As páginas model-config e hooks vieram em parte por resumo do WebFetch (trechos longos podem ter sido recortados pelo resumidor); trate números dessas duas como "conferir antes de decidir".

## 1. Memória: CLAUDE.md, AGENTS.md, imports, auto memory

O Claude Code carrega `CLAUDE.md` e `CLAUDE.local.md` do diretório de trabalho e de todos os diretórios acima dele; os de subdiretórios abaixo só entram sob demanda, quando Claude lê/edita um arquivo ali. Os arquivos são concatenados (não sobrescrevem), do mais amplo ao mais específico, e `CLAUDE.local.md` vem depois do `CLAUDE.md` no mesmo nível. `~/.claude/CLAUDE.md` é o escopo de usuário (todos os projetos) e `./CLAUDE.local.md` é o escopo pessoal do projeto (deve ir no `.gitignore`).

> Claude Code loads `CLAUDE.md` and `CLAUDE.local.md` from your current working directory and every directory above it. Run Claude Code in `foo/bar/` and it loads instructions from `foo/bar/CLAUDE.md`, `foo/CLAUDE.md`, and any `CLAUDE.local.md` files alongside them.

> Claude also discovers `CLAUDE.md` and `CLAUDE.local.md` files in subdirectories under your current working directory. Instead of loading them at launch, Claude Code loads each one once Claude reads, writes, or edits another file in that subdirectory.

> | **User instructions** | `~/.claude/CLAUDE.md` | Personal preferences for all projects |
> | **Project instructions** | `./CLAUDE.md` or `./.claude/CLAUDE.md`.
> | **Local instructions** | `./CLAUDE.local.md` | Personal project-specific preferences; add to `.gitignore` |

Quanto ao `--add-dir`, os CLAUDE.md dos diretórios adicionais não são carregados por padrão:

> The `--add-dir` flag gives Claude access to additional directories outside your main working directory. By default, CLAUDE.md files from these directories are not loaded.

> CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1 claude --add-dir ../shared-config

**AGENTS.md.** Desde a v2.1.277 o Claude Code lê `AGENTS.md` diretamente, mas só quando não há nenhum `CLAUDE.md`/`CLAUDE.local.md` no diretório de trabalho ou acima (o `~/.claude/CLAUDE.md`, o CLAUDE.md gerenciado e `.claude/rules/` não contam). É exatamente o caso deste repositório (há `AGENTS.md`, não há `CLAUDE.md`). Não são lidos `AGENTS.local.md`, `AGENTS.override.md` nem nada sob `.agents/`. Para ler ambos, use a opção "Project instructions" (`/config`) ou um `@AGENTS.md` dentro de um `CLAUDE.md`.

> | An `AGENTS.md`, and no `CLAUDE.md` or `CLAUDE.local.md` in your working directory or above it | Your `AGENTS.md` |
> | An `AGENTS.md` and a `CLAUDE.md` or `CLAUDE.local.md` in your working directory or above it | Your `CLAUDE.md` files only |

> Reading `AGENTS.md` directly requires Claude Code v2.1.277 or later.

> **Count, so Claude reads them instead of `AGENTS.md`**: a `CLAUDE.md`, `.claude/CLAUDE.md`, or `CLAUDE.local.md` in your working directory or any directory above it
> **Don't count, and keep loading alongside `AGENTS.md`**: your `~/.claude/CLAUDE.md`, your organization's managed `CLAUDE.md`, and `.claude/rules/` files

> **At session start**: every `AGENTS.md` and `.claude/AGENTS.md` in your working directory and the directories above it.
> **As Claude works in subdirectories**: a subdirectory's `AGENTS.md`, when Claude opens a file there with the Read tool and that subdirectory has none of the three `CLAUDE.md` files of its own
> **Not read**: `AGENTS.local.md`, `AGENTS.override.md`, or anything under a `.agents/` directory

> Because `CLAUDE.local.md` counts, adding one to keep your own uncommitted instructions in a project that relies on `AGENTS.md` stops Claude from reading `AGENTS.md` for you.

Valores da opção "Project instructions" e o arquivo de settings equivalente:

> | `claude-md-or-agents-md` | ... This is the default |
> | `claude-md-and-agents-md` | Your `CLAUDE.md` and `AGENTS.md` files together, each directory's `CLAUDE.md` files first and its `AGENTS.md` after them.
> | `claude-md` | Your `CLAUDE.md` files only |
> | `managed-only` | Only your organization's managed `CLAUDE.md` and [auto memory](#auto-memory) at launch.

> Add it to `pluginConfigs` under `cc-plugin-agents-md@builtin` ... `"options": { "instructionFiles": "claude-md-and-agents-md" }`

Diferenças do AGENTS.md lido pela opção: hooks `InstructionsLoaded` não disparam; `--add-dir` com a variável não carrega AGENTS.md; import `@path` fora do diretório carrega sem pedir aprovação se já houve aprovação.

**Imports `@path`.** Caminhos relativos ou absolutos; relativos resolvem a partir do arquivo que importa. Profundidade máxima de quatro saltos. Imports não reduzem custo de contexto (carregam no início). Blocos/trechos de código são ignorados no parsing. Um import fora do diretório de trabalho pede aprovação uma vez por projeto (em arquivos de escopo de usuário, não).

> CLAUDE.md files can import additional files using `@path/to/import` syntax. Imported files are expanded and loaded into context at launch alongside the CLAUDE.md that references them.

> Both relative and absolute paths are allowed. Relative paths resolve relative to the file containing the import, not the working directory. Imported files can recursively import other files, with a maximum depth of four hops.

> Import parsing skips Markdown code spans and fenced code blocks. To mention a path in your CLAUDE.md without importing it, wrap it in backticks

> Imports help you organize a long file but don't reduce its context cost, because imported files also load at launch.

> target under 200 lines per CLAUDE.md file.

> Claude Code loads a CLAUDE.md file of up to 4 MiB in full and skips a larger file.

**Auto memory.** Notas que o próprio Claude escreve (tipos `user`, `feedback`, `project`, `reference`). Ligada por padrão em sessões locais. Fica em `~/.claude/projects/<project>/memory/`, onde `<project>` vem do repositório git (todos os worktrees compartilham). Diretório contém `MEMORY.md` (índice) e arquivos de tópico. Só as primeiras 200 linhas ou 25KB do `MEMORY.md` entram no início de cada sessão; arquivos de tópico são lidos sob demanda. É local à máquina.

> Each project gets its own memory directory at `~/.claude/projects/<project>/memory/`. The `<project>` path is derived from the git repository, so all worktrees and subdirectories within the same repo share one auto memory directory. Outside a git repo, the project root is used instead.

> The first 200 lines of `MEMORY.md`, or the first 25KB, whichever comes first, are loaded at the start of every conversation. Content beyond that threshold is not loaded at session start.

> Claude Code doesn't load topic files such as `user_role.md` or `feedback_testing.md` at startup. Claude reads them on demand using its standard file tools when it needs the information.

> Auto memory is machine-local. ... Files are not shared across machines or cloud environments.

> To store auto memory in a different location, set `autoMemoryDirectory` in your `settings.json`. ... The value must be an absolute path or start with `~/`.

> To disable auto memory via environment variable, set `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1.` [a página grafa `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`]

> To toggle it, open `/memory` in a session and use the auto memory toggle, which saves `autoMemoryEnabled` to your user settings at `~/.claude/settings.json`.

> The main conversation's auto memory isn't loaded into subagents; the exception is a fork

Diretório do memory de projeto relevante para este repositório: o `MEMORY.md` de `C:\Users\gustavo.delfino\.claude\projects\C--Projetos-context-hub\memory\` é exatamente esse mecanismo.

## 2. Settings: arquivos, precedência, `env`, `permissions`, `model`, `effort`, `hooks`

Há quatro arquivos/fontes: gerenciado (organização), usuário (`~/.claude/settings.json`), projeto compartilhado (`.claude/settings.json`) e projeto local (`.claude/settings.local.json`). Precedência, do mais alto ao mais baixo: gerenciado, linha de comando (`--settings`), local do projeto, projeto compartilhado, usuário. Listas (por exemplo `permissions.allow`) são combinadas entre arquivos em vez de substituídas. Variáveis de ambiente não são um nível: a regra é por par (ex.: `ANTHROPIC_MODEL` vence a chave `model`).

> Claude Code reads settings from four files, and an organization can also deliver managed settings from the claude.ai console.

> | User | `~/.claude/settings.json` | You, in every project on this machine |
> | Shared project | `.claude/settings.json` | Everyone working in the folder that contains it. In a git repository, commit it so teammates get it |
> | Project local | `.claude/settings.local.json` | You, in this one project only. |

> In order, highest precedence first:
> 1. **Managed settings** ...
> 2. **Command line**: JSON you pass with `--settings <file-or-json>` when you start `claude`, for that session only ...
> 3. **Project local settings** (`.claude/settings.local.json`): your personal settings for this project.
> 4. **Shared project settings** (`.claude/settings.json`): settings your team checks into source control.
> 5. **User settings** (`~/.claude/settings.json`): your personal settings for every project.

> When you set the same list key, such as `permissions.allow`, in more than one file, Claude Code combines the lists instead of picking one, so each file can add entries without removing another file's.

> Environment variables aren't a level in this stack. ... `ANTHROPIC_MODEL` exported in your shell applies over the `model` key from any file, while `ANTHROPIC_DEFAULT_MODEL` applies only when no file sets `model`. ... An `env` block inside a settings file is an ordinary key and follows the levels above.

> On Windows, `~/.claude` means `%USERPROFILE%\.claude`. To keep the home-directory files somewhere else, set `CLAUDE_CONFIG_DIR`

**`permissions`** (exemplo oficial; regras `allow`, `deny` e `ask`; `deny` e `ask` valem de imediato, `allow` de projeto espera confiança na pasta):

> ```json
> {
>   "permissions": {
>     "allow": ["Bash(npm run lint)", "Bash(npm run test *)"],
>     "deny": ["Read(./.env)", "Read(./.env.*)"]
>   }
> }
> ```

> `permissions.allow` rules, `permissions.additionalDirectories`, `extraKnownMarketplaces`, and most `env` values apply only after each teammate trusts the folder. ... `deny` and `ask` rules apply right away.

> [`permissions.defaultMode`] values `auto` and `bypassPermissions` don't take effect from project or local settings; set them in user or managed settings instead

**`model`, esforço e raciocínio.** A chave `model` define o padrão; `/model` grava essa chave em `~/.claude/settings.json`. Para esforço, `effortLevel` (aceita `low`, `medium`, `high`, `xhigh`; `max` não é aceito em chave nem variável). `alwaysThinkingEnabled` liga/desliga o raciocínio estendido por padrão. Detalhes na seção 4.

> if your team's file sets `"model": "claude-sonnet-5"` and you want Opus, put `"model": "claude-opus-5-5"` in your local file and only your sessions change.

> claude --settings '{"model": "claude-opus-5-5"}'

> A flag for that key: some keys have their own flag, such as `--model` for `model` and `--effort` for `effortLevel` and `modelSettings`.

> Claude Code watches your settings files and reloads them when they change, so it applies most edits to the running session without a restart, including edits to `permissions`, `hooks`, and credential helpers such as `apiKeyHelper`.

**`hooks`.** Fica na chave de topo `hooks` do mesmo JSON de settings (usuário, projeto ou local): evento, depois grupos com `matcher`, depois lista `hooks` de handlers.

> Hooks are defined in JSON settings files. The configuration has three levels of nesting:
> 1. Choose a hook event to respond to, like `PreToolUse` or `Stop`
> 2. Add a matcher group to filter when it fires, like "only for the Bash tool"
> 3. Define one or more hook handlers to run when matched

> ```json
> { "hooks": { "PreToolUse": [ { "matcher": "Bash", "hooks": [ { "type": "command", "command": "${CLAUDE_PROJECT_DIR}/.claude/hooks/block-rm.sh", "args": [] } ] } ] } }
> ```

> `~/.claude/settings.json` | All your projects | No, local to your machine
> `.claude/settings.json` | Single project | Yes, can be committed to the repo
> `.claude/settings.local.json` | Single project | No, gitignored when Claude Code saves a setting to it

Chave `env`: a página de settings só confirma que `env` é uma chave comum que segue os níveis; a lista de variáveis e as regras finas estão em `settings-reference#env` (não lida; ver "Não verificado"). Exemplo oficial do uso de `env` em settings: `CLAUDE_CODE_NEW_INIT` "in the `env` block of a settings file", e `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD` "to the `env` block in `~/.claude/settings.json`".

## 3. Fast mode

Fast mode é uma configuração de API de alta velocidade para o Opus (até 2,5x mais rápido, a um custo por token maior); não é outro modelo, e não existe para Sonnet, Haiku ou outros. Ativa-se com `/fast` ou `"fastMode": true` no arquivo de settings do usuário. No cache de prompt: na primeira vez que você liga o fast mode numa conversa, paga o preço cheio de entrada não cacheada de fast mode por todo o contexto, então convém ligar no início da sessão. Em planos de assinatura é cobrado só por créditos de uso (fora dos limites do plano).

> Fast mode is a high-speed configuration for Claude Opus, making the model up to 2.5x faster at a higher cost per token.

> Fast mode is not a different model. It uses Claude Opus with a different API configuration that prioritizes speed over cost efficiency. You get identical quality and capabilities with faster responses. Fast mode is supported on Opus 5.5, Opus 5, and Opus 4.8. It is not available on Sonnet, Haiku, or other models.

> Opus 5.5 is the fast mode default in Claude Code v2.1.280 and later.

> Fast mode pricing per MTok input/output is $8/$40 on Opus 5.5 and $10/$50 on Opus 5 and Opus 4.8.

> Fast mode pricing is flat across the full 1M token context window.

> The first time you enable fast mode in a conversation, you pay the full fast mode uncached input token price for the entire conversation context. The deeper into a conversation you are, the more this costs, so the charge is smallest when you enable fast mode at the start. The cost applies once per conversation, so toggling fast mode off and on again later doesn't repeat it.

> For Claude Code users on subscription plans (Pro/Max/Team/Enterprise), fast mode is available via usage credits only and not included in the subscription rate limits.

> Set `"fastMode": true` in your user settings file

> Fast mode is available through the Anthropic Console API and for Claude subscription plans using usage credits. It is not available on Amazon Bedrock, Google Cloud's Agent Platform, Microsoft Foundry, or Claude Platform on AWS.

> Fast mode has separate rate limits from standard Opus. ... When you hit the fast mode rate limit: 1. Fast mode automatically falls back to standard speed ... 4. When the cooldown expires, fast mode automatically re-enables

> Fast mode and effort level both affect response speed, but differently: **Fast mode** | Same model quality, lower latency, higher cost; **Lower effort level** | Less thinking time, faster responses, potentially lower quality on complex tasks

> Another option to disable fast mode entirely is to set `CLAUDE_CODE_DISABLE_FAST_MODE=1`.

> By default, fast mode a user turns on in an interactive session persists across sessions. ... set `fastModePerSessionOptIn` to `true` in any settings file

O mecanismo detalhado do cache fica em `prompt-caching#turning-on-fast-mode` (não lido). A própria página de fast mode também diz que, em modo não interativo, `/fast` só funciona com `claude -p --settings '{"fastMode": true}'` (v2.1.205 ou superior, segundo a página; o trecho cita v2.1.205).

## 4. Configuração de modelos: aliases, `/model`, esforço, raciocínio

Aliases oficiais: `default` (limpa o override), `best`, `fable`, `sonnet`, `opus`, `haiku`, `sonnet[1m]`, `opus[1m]` e `opusplan` (Opus no plan mode, Sonnet na execução). Não há alias "advisor": o advisor é uma ferramenta separada (`advisorModel` / `--advisor`, página `/docs/en/advisor`, não lida). Ordem de prioridade para definir o modelo: `/model` na sessão, `--model` na partida, `ANTHROPIC_MODEL`, a chave `model` em settings, `ANTHROPIC_DEFAULT_MODEL`. As citações desta seção vêm de um WebFetch que resumiu a página (primeira chamada) e de uma segunda leitura direta da parte final; trate versões de modelo como sujeitas a mudança.

> | **`best`** | "Uses the model the `fable` alias resolves to where Fable is available to you, otherwise the same model as `opus`" |
> | **`sonnet`** | "Uses the latest Sonnet model for daily coding tasks" |
> | **`opus`** | "Uses the latest Opus model for complex reasoning tasks" |
> | **`haiku`** | "Uses the fast and efficient Haiku model for simple tasks" |
> | **`opusplan`** | "Special mode that uses `opus` during plan mode, then switches to `sonnet` for execution" |
> | **`default`** | "Special value that clears any model override and reverts to the runtime default for your account. Not itself a model alias" |

> The `opusplan` model alias provides an automated hybrid approach: **In plan mode**: uses `opus` for complex reasoning and architecture decisions; **In execution mode**: automatically switches to `sonnet` for code generation and implementation

> For a hybrid approach where Claude decides mid-task when to consult a second model rather than switching at the plan boundary, see the advisor tool.

> the [`advisorModel`](/docs/en/advisor) setting and the `--advisor` flag

> 1. During session: use `/model <alias|name>` to switch immediately, or run `/model` with no argument to open the picker.
> 2. At startup: launch with `claude --model <alias|name>`
> 3. Environment variable: set `ANTHROPIC_MODEL=<alias|name>`
> 4. Settings: configure permanently in your settings file using the `model` field
> 5. Default for new sessions: set `ANTHROPIC_DEFAULT_MODEL=<alias|name>`

> `/model` saves your choice as the default for new sessions by writing the `model` field in your user settings. In the picker: `Enter`: switch model and save as your default; `s`: switch model for this session only and leave your default unchanged.

Resolução dos aliases por versão (tabela "Version history" da página): `haiku` aponta para Haiku 5.5 (v2.1.293), `sonnet` para Sonnet 5.5 (v2.1.284), `opus` para Opus 5.5 (v2.1.280), `fable` para Fable 5.1 (v2.1.257), todos na API da Anthropic.

> | v2.1.293 | `haiku` resolves to Haiku 5.5 on the Anthropic API |
> | v2.1.284 | `sonnet` resolves to Sonnet 5.5 on the Anthropic API |
> | v2.1.280 | `opus` resolves to Opus 5.5 on the Anthropic API, Claude Platform on AWS, Amazon Bedrock, and Google Cloud's Agent Platform |
> | v2.1.257 | `fable` resolves to Fable 5.1, except in Claude apps gateway sessions |

**Níveis de esforço.** `low`, `medium`, `high`, `xhigh`, `max` (para Fable 5.1/5; Opus 4.6 e Sonnet 4.6 vão até `max` sem `xhigh`, e um nível não suportado cai para o mais alto suportado abaixo). Formas de ajustar: `/effort` (slider, nível direto ou `/effort auto`), `--effort`, `CLAUDE_CODE_EFFORT_LEVEL`, chave `effortLevel` (`low`/`medium`/`high`/`xhigh`; `max` não é aceito nessas duas chaves). Padrão do modelo: `high`, exceto Opus 5.5, Sonnet 5.5 e Haiku 5.5, que usam `medium`.

> **Resolution order:** 1. An explicit choice: the `CLAUDE_CODE_EFFORT_LEVEL` environment variable, launching with `--effort`, or `/effort` in the session 2. Your settings: the level you saved for the model or an `effortLevel` key 3. The model's default effort: `high` on every model that supports effort, except that Opus 5.5, Sonnet 5.5, and Haiku 5.5 default to `medium`, Opus 4.7 defaults to `xhigh`...

> run `/effort` with no arguments to open an interactive slider, `/effort` followed by a level name to set it directly, or `/effort auto` to clear your saved level for the active model.

> set `effortLevel` to `low`, `medium`, `high`, or `xhigh` as the default for models without one. `max` isn't accepted as a level in either key

> Claude Code falls back to the highest supported level at or below the one you set. For example, `xhigh` runs as `high` on Opus 4.6.

**Raciocínio estendido e `MAX_THINKING_TOKENS`.** Alternância na sessão com `Alt+T` (Windows/Linux) / `Option+T` (macOS); padrão global com `alwaysThinkingEnabled` em `~/.claude/settings.json` (via `/config`). `MAX_THINKING_TOKENS=0` desliga o raciocínio na API da Anthropic, exceto em Opus 5.5, Sonnet 5.5, Haiku 5.5 e modelos Fable, onde não é possível desligar. Orçamento fixo com `MAX_THINKING_TOKENS` só vale para Opus 4.6 e Sonnet 4.6 com `CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING=1`.

> Press `Option+T` on macOS or `Alt+T` on Windows and Linux

> Run `/config` and toggle thinking mode. Saved as `alwaysThinkingEnabled` in `~/.claude/settings.json`

> Set `MAX_THINKING_TOKENS=0`, which turns thinking off on the Anthropic API except on Opus 5.5, Sonnet 5.5, Haiku 5.5, and Fable models.

> You can't turn thinking off on Opus 5.5, Sonnet 5.5, Haiku 5.5, or the Fable models.

> On Opus 4.6 and Sonnet 4.6, "you can set `CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING=1` to revert to the previous fixed thinking budget controlled by `MAX_THINKING_TOKENS`."

**Contexto de 1M e cache.** Fable 5.1/5, Sonnet 5 e posteriores, Haiku 5.5 e Opus 4.7 e posteriores rodam com 1M por padrão, sem sufixo `[1m]`; Opus 4.6 e Sonnet 4.6 só chegam a 1M pela variante `[1m]`, dependente do plano. `CLAUDE_CODE_DISABLE_1M_CONTEXT=1` desliga. O cache de prompt é automático e se desliga com `DISABLE_PROMPT_CACHING=1` (ou por modelo: `_HAIKU`, `_SONNET`, `_OPUS`, `_FABLE`).

> Fable 5.1, Fable 5, Sonnet 5 and later, Haiku 5.5, and Opus 4.7 and later run with the 1M window by default, with no `[1m]` suffix needed.

> Opus 4.6 and Sonnet 4.6 reach 1M only through their `[1m]` variant, and access to that variant depends on your plan.

> set `CLAUDE_CODE_DISABLE_1M_CONTEXT=1` in your shell or in a settings file.

> Claude Code automatically uses prompt caching to optimize performance and reduce costs. ... `DISABLE_PROMPT_CACHING` | Set to `1` to disable prompt caching for all models.

> Each model has its own prompt cache, so the first request after a switch re-reads the whole conversation uncached

## 5. Worktrees e sessões paralelas

O padrão recomendado é uma sessão por worktree git: `claude --worktree <nome>` (ou `-w`) cria o worktree em `.claude/worktrees/<nome>/` numa branch nova `worktree-<nome>`. Também é possível pedir a Claude para "work in a worktree" (ferramenta `EnterWorktree`; há `ExitWorktree` para sair). A página compara worktrees (isolam edições de arquivo) com subagentes (dividem trabalho dentro de uma sessão) e mensagens entre sessões. `.worktreeinclude` copia arquivos gitignored (ex.: `.env`) para cada worktree novo. Subagentes podem ter worktree próprio com `isolation: worktree` no frontmatter.

> A git worktree is a separate working directory with its own files and branch, sharing the same repository history and remote as your main checkout. Running each Claude Code session in its own worktree gives it a separate copy of the files to edit, so one session can build a feature while a second fixes a bug.

> Pass `--worktree` or `-w` with a name to create an isolated worktree and start Claude in it. By default, the worktree is created under `.claude/worktrees/<name>/` at your repository root, on a new branch named `worktree-<name>`:
> `claude --worktree feature-auth`

> Run the command again with a different name in another terminal to start a second isolated session. If you omit the name, Claude generates one such as `bright-running-fox`.

> You can also ask Claude to "work in a worktree" during a session, and it creates one with the `EnterWorktree` tool. Once in a worktree, Claude can switch directly to another one under `.claude/worktrees/` by calling `EnterWorktree` with the target path

> Back inside the worktree, Claude can still exit it with the `ExitWorktree` tool.

> Worktrees are one of several ways to run Claude in parallel. They isolate file edits. Subagents split work up inside one session, and cross-session messaging lets Claude pass findings between the sessions in your worktrees.

> Add `.claude/worktrees/` to your `.gitignore` so worktree contents don't appear as untracked files in your main checkout.

> **The worktree is clean**: for an unnamed session, Claude removes the worktree and its branch automatically. A named session prompts you first ... **The worktree has work in it**: Claude prompts you to keep or remove the worktree.

> To return later, run the `claude --worktree <name> --resume` command that Claude Code prints on exit.

> `"fresh"` (default): branch from the repository's default branch on the remote, usually `main` ... `"head"`: branch from your current local `HEAD`

(configurável por `worktree.baseRef` em settings.)

> To carry gitignored files such as `.env` into every new worktree automatically, add a `.worktreeinclude` file

> Ask Claude to "use worktrees for your agents", or make the isolation permanent for a custom subagent by adding `isolation: worktree` to its frontmatter.

> `claude --worktree "#1234"` [ramificar a partir de um PR]

> **The repository's `.git` directory** ... **Plugins** ... **Permission approvals** ... **Untracked skills, agents, and commands**

> A worktree gets its own files and branch, but it shares the following with the main checkout

Relação com memória (página de memória): o auto memory é compartilhado entre worktrees; já o `CLAUDE.local.md` é gitignored e só existe no worktree onde foi criado.

> If you work across multiple git worktrees of the same repository, a gitignored `CLAUDE.local.md` only exists in the worktree where you created it. To share personal instructions across worktrees, import a file from your home directory instead

Observação: o checkout manual também é suportado (`git worktree add ../project-feature-a -b feature-a`, depois `cd` e `claude`). Esta seção usou a página `worktrees`, não `common-workflows`.

## 6. Janela de contexto e compactação

O Claude Code compacta automaticamente ao se aproximar do limite; o `/compact` aceita instruções de foco; `/clear` serve para trocar de tarefa; `/context` mostra o uso real por categoria (e quais arquivos de memória carregaram). Para modelos com janela nativa de 1M, a compactação ocorre antes de encher, em cerca de 967K tokens por padrão (modelos de 200K compactam no limite). A janela de auto-compactação é ajustável por `/autocompact`, `autoCompactWindow` (settings), `--autocompact` e `CLAUDE_CODE_AUTO_COMPACT_WINDOW`.

> Claude Code compacts automatically as you approach the limit, so a full context window doesn't end your session.

> **Compact with a focus**: run `/compact` with instructions, like `/compact focus on the auth bug fix`, before starting a long new task. The summary keeps what you choose instead of what the automatic pass guesses is important.

> **Compact part of the conversation**: run `/rewind`, select a message, and choose **Summarize from here** or **Summarize up to here**.

> **Compact earlier**: run `/autocompact` with a token count, like `/autocompact 500k`, to set how full the context window gets before the automatic pass runs.

> **Clear between tasks**: run `/clear` when switching to unrelated work. Old conversation crowds out the files you need next and costs tokens on every message.

> **Delegate large reads**: send research to a subagent so the file contents stay in its context window, not yours.

> run `/context` for a live breakdown by category with optimization suggestions, including which CLAUDE.md and auto memory files loaded. Run `/memory` to open and edit those files.

> Models running with a native 1M window compact before the window fills, at about 967K tokens by default. These include the Fable models, Sonnet 5 and later, Haiku 5.5, and Opus 4.7 and later.

> Sonnet 4.6 and Opus 4.6 without extended context compact at the 200K boundary

> When you set `CLAUDE_CODE_DISABLE_1M_CONTEXT=1`, models with a native 1M window, such as Sonnet 5 and the Fable models, compact at the 200K boundary

> run `/autocompact` with a value, like `/autocompact 500k` ... Run `/autocompact auto` to return to the window tuned for your model.
> set `autoCompactWindow` in a settings file, such as `"autoCompactWindow": 200000` in `~/.claude/settings.json`.
> The command and the flag accept a window size from 100K to 1M tokens

> set `CLAUDE_CODE_AUTO_COMPACT_WINDOW`. While it's set, it takes precedence over the command, the flag, and the setting

**O que sobrevive à compactação** (relevante para o desenho do hub):

> | Project-root CLAUDE.md and unscoped rules | Re-injected from disk |
> | Auto memory | Re-injected from disk |
> | Rules with `paths:` frontmatter | Claude Code reloads them on demand |
> | Nested CLAUDE.md in subdirectories | Claude Code reloads them on demand |
> | Files Claude read or edited | Claude Code re-reads up to five, most recently modified first |
> | Invoked skill bodies | Re-injected, capped at 5,000 tokens per skill and 25,000 tokens total; oldest dropped first |
> | Context that hooks added earlier | Summarized with the rest of the conversation |
> | SessionStart hooks that match the `compact` source | Claude Code runs them and adds their output to the compacted context |

> If an instruction disappeared after compaction, it was given only in conversation, lives in a nested CLAUDE.md that hasn't reloaded yet, or is a path-scoped rule that hasn't matched a file since. Add conversation-only instructions to CLAUDE.md to make them persist.

> A file over 5,000 tokens comes back as a path reference without its content, shown as `Referenced file` instead of `Read`.

## 7. Agent SDK, modo headless (`claude -p`), subagentes programáticos

O Agent SDK dá em Python e TypeScript as mesmas ferramentas, o mesmo loop de agente e a mesma gestão de contexto do Claude Code; roda o binário do Claude Code como biblioteca. Para outras linguagens, rode o CLI como subprocesso com `-p` e `--output-format json`. Capacidades: ferramentas nativas, hooks, subagentes, MCP, permissões, sessões, skills/comandos/memória carregados de `.claude/` e `~/.claude/`, e plugins. O modo headless é `claude -p "<prompt>"`, com `--allowedTools` para auto-aprovar, `--output-format` (`text`, `json`, `stream-json`), `--json-schema`, `--continue`/`--resume`, `--append-system-prompt` e `--bare`.

> An agent is an application that completes a task by planning its own steps and calling tools that read files, run commands, or edit code. The Agent SDK gives you the same tools, agent loop, and context management that power Claude Code, programmable in Python and TypeScript.

> | Embed Claude Code's agent in your own Python or TypeScript application, in a process you operate | **Agent SDK** | A library that runs the Claude Code binary, with Claude Code's capabilities, such as built-in tools, permissions, sessions, and hooks. |

> To drive the same agent loop from a language other than Python or TypeScript, run the CLI as a subprocess with the `-p` flag and `--output-format json`.

> | Built-in tools | Read, write, edit files, run commands, and search the web |
> | Hooks | Run custom code at key points in the agent lifecycle |
> | Subagents | Spawn specialized agents for focused subtasks |
> | MCP | Connect external tools and data sources via the Model Context Protocol |
> | Skills, commands, and memory | Load automatically from your project's `.claude/` and from `~/.claude/`, same as Claude Code |

> Unless previously approved, Anthropic does not allow third party developers to offer claude.ai login or rate limits for their products, including agents built on the Claude Agent SDK. Use the API key authentication methods described in the Quickstart instead.

Headless:

> claude -p "Find and fix the bug in auth.py" --allowedTools "Read,Edit,Bash"

> Claude Code exits with code 0 on success and a non-zero code when the run fails, so your scripts can branch on the exit status.

> Use `--output-format` to control how responses are returned:
> * `text` (default): plain text output
> * `json`: structured JSON with result, session ID, and metadata
> * `stream-json`: newline-delimited JSON for real-time streaming

> With `--output-format json`, the response payload includes `total_cost_usd` and a per-model cost breakdown

> Use `--output-format stream-json` with `--verbose` and `--include-partial-messages` to receive tokens as they're generated.

> To get output conforming to a specific schema, use `--output-format json` with `--json-schema` ... with the structured output in the `structured_output` field.

> Use `--allowedTools` to let Claude use certain tools without prompting. ... `claude -p "Run the test suite and fix any failures" --allowedTools "Bash,Read,Edit"`

> The `--allowedTools` flag uses permission rule syntax. The trailing ` *` enables prefix matching, so `Bash(git diff *)` allows any command starting with `git diff`.

> Use `--continue` to continue the most recent conversation, or `--resume` with a session ID to continue a specific conversation.

> Use `--append-system-prompt` to add instructions while keeping Claude Code's default behavior.

> Add `--bare` to reduce startup time by skipping auto-discovery of hooks, skills, custom commands, subagents, installed plugins, MCP servers, auto memory, and CLAUDE.md. Without it, `claude -p` loads the same context an interactive session would, including anything configured in the working directory or `~/.claude`.

> `--bare` is the recommended mode for scripted and SDK calls, and will become the default for `-p` in a future release.

> In bare mode Claude has access to the Bash, file read, and file edit tools. ... Custom agents | `--agents <file-or-json>`

> Without `--bare`, a `-p` session runs the hooks in a project's `.claude/settings.json` and connects the servers in its `.mcp.json`, even in a folder you've never trusted.

> `dontAsk`: Claude Code denies every call that would otherwise prompt, which is useful for locked-down CI runs.

> Pass `--permission-prompts none` when nobody is available to answer permission prompts, for example in a scheduled job.

Subagentes programáticos: no CLI, a via encontrada é `--agents <file-or-json>` (agentes personalizados por JSON/arquivo) e, para mensagens de subagentes no stream, `parent_tool_use_id`. A API programática dos subagentes no SDK (opção de agents no código) está na página `agent-sdk/subagents`, que não foi lida (ver "Não verificado").

> Messages from subagents and from skills that run in a subagent appear in the stream as `assistant` and `user` messages. Their `parent_tool_use_id` field says which run each one belongs to. Messages from the main conversation carry `null` in that field.

## 8. Hooks: eventos, Stop (bloquear/continuar) e SessionStart

Lista completa de eventos do resumo da página de hooks (31): `SessionStart`, `Setup`, `UserPromptSubmit`, `UserPromptExpansion`, `PreToolUse`, `PermissionRequest`, `PermissionDenied`, `PostToolUse`, `PostToolUseFailure`, `PostToolBatch`, `Notification`, `MessageDisplay`, `SubagentStart`, `SubagentStop`, `TaskCreated`, `TaskCompleted`, `Stop`, `StopFailure`, `TeammateIdle`, `InstructionsLoaded`, `ConfigChange`, `CwdChanged`, `DirectoryAdded`, `FileChanged`, `WorktreeCreate`, `WorktreeRemove`, `PreCompact`, `PostCompact`, `PreModelSwitch`, `PostModelSwitch`, `Elicitation`, `ElicitationResult`, `SessionEnd` (são 33 nomes na contagem; o número exato não foi conferido, ver "Não verificado"). O hook `Stop` roda quando Claude termina de responder e pode impedi-lo de parar: tanto com saída de código 2 (stderr vira o motivo) quanto com JSON `{"decision":"block","reason":"..."}`. Há um teto de 8 continuações consecutivas, e o campo `stop_hook_active` indica que Claude já está continuando por causa de um hook de parada. `SessionStart` dispara com os matchers `startup`, `resume`, `clear`, `compact` e `fork`, e o stdout (texto puro) ou `additionalContext` entra no contexto antes do primeiro prompt.

> | `SessionStart` | When a session begins or resumes
> | `Setup` | When you start Claude Code with `--init-only`, or with `--init` or `--maintenance` in `-p` mode. For one-time preparation in CI or scripts
> | `UserPromptSubmit` | When a prompt is submitted, before Claude processes it. Also fires on turns Claude Code starts on its own
> | `UserPromptExpansion` | When a user-typed command expands into a prompt, before it reaches Claude. Can block the expansion
> | `PreToolUse` | Before a tool call executes. Can block it
> | `PermissionRequest` | When a tool call needs a permission decision
> | `PermissionDenied` | When auto mode denies a tool call, including denials without a classifier verdict
> | `PostToolUse` | After a tool call succeeds
> | `PostToolUseFailure` | After a tool call fails
> | `PostToolBatch` | After a full batch of parallel tool calls resolves, before the next model call
> | `Notification` | When Claude Code sends a notification
> | `MessageDisplay` | While assistant message text is displayed
> | `SubagentStart` | When a subagent is spawned
> | `SubagentStop` | When a subagent finishes
> | `TaskCreated` | When a task is being created via `TaskCreate`
> | `TaskCompleted` | When a task is being marked as completed
> | `Stop` | When Claude finishes responding
> | `StopFailure` | When the turn ends due to an API error
> | `TeammateIdle` | When an agent team teammate is about to go idle
> | `InstructionsLoaded` | When a CLAUDE.md or `.claude/rules/*.md` file is loaded into context
> | `ConfigChange` | When a configuration file changes during a session
> | `CwdChanged` | When the working directory changes, for example when Claude executes a `cd` command
> | `DirectoryAdded` | When a working directory is added mid-session via `/add-dir` or the SDK `register_repo_root` control request
> | `FileChanged` | When a watched file changes on disk
> | `WorktreeCreate` | When a worktree is being created via `--worktree`, `isolation: "worktree"`, or for a background session
> | `WorktreeRemove` | When a worktree that a `WorktreeCreate` hook created is being removed
> | `PreCompact` | Before context compaction
> | `PostCompact` | After context compaction completes
> | `PreModelSwitch` | Before Claude Code applies a model switch that you or a client requested. Can block the switch
> | `PostModelSwitch` | After the session's model changes
> | `Elicitation` | When an MCP server requests user input during a tool call
> | `ElicitationResult` | After a user responds to an MCP elicitation, before the response is sent back to the server
> | `SessionEnd` | When a session terminates

**Stop: bloquear e continuar.**

> Stop | Yes | Prevents Claude from stopping, continues the conversation

> `Stop`, `SubagentStop`, `TeammateIdle`, and `TaskCompleted` hooks: exit code 2 on these events sends Claude back to keep working, and Claude can't repair a hook that won't run.

> In addition to the common input fields, Stop hooks receive `stop_hook_active`, `last_assistant_message`, `background_tasks`, and `session_crons`. The `stop_hook_active` field is `true` when Claude Code is already continuing as a result of a stop hook. Check this value or process the transcript to avoid blocking on a condition that will never resolve.

> Claude Code applies an 8-consecutive-continuation cap: after stop hooks have continued the turn eight times in a row, Claude Code overrides the next block and ends the turn. The count of consecutive continuations resets each time Claude calls a tool. To raise the cap, set `CLAUDE_CODE_STOP_HOOK_BLOCK_CAP`.

> `Stop` and `SubagentStop` hooks can control whether Claude continues.
> | `decision` | `"block"` prevents Claude from stopping. Omit to allow Claude to stop |
> | `reason` | Required when `decision` is `"block"`. Tells Claude why it should continue |
> | `hookSpecificOutput.additionalContext` | Non-error feedback for Claude. The conversation continues so Claude can act on it, but unlike `decision: "block"` it is shown in the transcript as hook feedback rather than a hook error |

> A hook that blocks by exiting 2 routes the same way as `reason`: Claude receives the stderr message as the explanation for why it should continue.

> ```json
> { "decision": "block", "reason": "Must be provided when Claude is blocked from stopping" }
> ```

> Stop and SubagentStop also accept `hookSpecificOutput.additionalContext` for non-error feedback that continues the conversation.

> `Stop`: `last_assistant_message` is available as the way to get the final assistant text of the current turn, instead of reading the transcript.

**SessionStart.**

> | `startup` | New session
> | `resume` | `--resume`, `--continue`, or `/resume`
> | `clear` | `/clear`
> | `compact` | Auto or manual compaction
> | `fork` | A new session forked from an existing one

> | `additionalContext` | String added to Claude's context at the start of the conversation, before the first prompt.

> A hook that only adds context can print it without building JSON, because Claude Code adds a SessionStart hook's plain-text stdout to Claude's context.

> Claude Code wraps the string in a system reminder and inserts it into the conversation at the point where the hook fired.

> {"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": "Current branch: feat/auth-refactor ...", "sessionTitle": "auth-refactor"}}

Nota sobre hooks no contexto: um `SessionStart` que imprima o `AGENTS.md` duplica contexto agora que o Claude lê `AGENTS.md` direto (página de memória, "Remove an earlier AGENTS.md workaround"). Hooks não são garantia de comportamento do modelo, mas são aplicados pelo cliente:

> Claude treats them as context, not enforced configuration. To block an action regardless of what Claude decides, use a PreToolUse hook instead.

> Hooks execute as shell commands at fixed lifecycle events and apply regardless of what Claude decides to do.

Outras notas da página de hooks relevantes: `InstructionsLoaded` serve para depurar quais CLAUDE.md/rules carregaram; hooks em `-p` sem `--bare` rodam mesmo em pastas não confiáveis; tipos de handler citados: `command`, `http`, `mcp_tool`, `prompt`, `agent` (extraído de um resumo do WebFetch, não verificado no texto).

## Não verificado

- Página `settings-reference` (chave `env`, lista completa de chaves, `permissions.ask` com exemplo, `effortLevel` exato, `modelSettings`, `hooks` na referência): não foi lida. Da chave `env` só consta aqui que é uma chave comum que segue a precedência e que a página de memória a usa como forma de definir variáveis. A sintaxe de regras `ask` não foi vista num exemplo.
- Página `common-workflows`: não lida; a seção 5 vem da página `worktrees`, que a própria documentação indica para esse assunto.
- Página `hooks-guide`: não lida; a seção 8 vem do `hooks` (referência). Do `hooks` foram lidos os caracteres 0 a 200000 de 266639 (por resumo do WebFetch); os últimos ~66 mil não foram lidos. A contagem exata de eventos e o detalhe de `SessionStart` (matcher por evento, regras de saída) vêm do resumo do WebFetch, não do texto integral.
- Página `advisor` (`/docs/en/advisor`): não lida; só consta que existem `advisorModel` e `--advisor`.
- Páginas `prompt-caching` (mecanismo do fast mode), `how-claude-code-works`, `costs`, `sub-agents`, `agent-sdk/subagents`, `agent-sdk/quickstart`, `cli-reference`, `env-vars`: não lidas. Como definir subagentes no código do SDK (opção `agents` em Python/TypeScript) não foi verificado.
- Valor exato da variável `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE`: não encontrado na leitura.
- A linha "aviso" do cabeçalho foi escrita sem acesso aos outros relatórios da pasta; ajustar ao padrão dos demais se divergir.
- Citações da seção 4 (aliases, esforço, `MAX_THINKING_TOKENS`) vêm de um WebFetch que resumiu a página; confirmar o texto literal na página se uma decisão depender de um número ou de um nome de modelo.
