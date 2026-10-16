# Porta 2: sessão de harness aberta numa subpasta do hub

Pesquisa em fonte primária, 2026-10-10. Insumo do ticket 36 (`.scratch/context-hub/issues/36-portas-de-entrada-do-hub.md`). Nenhum teste foi rodado; nada foi inferido sem marcação. Trechos entre aspas estão no idioma original.

## Pergunta

Uma sessão de harness aberta numa SUBPASTA do hub (ex.: `clients/voegol/app-migration/`), em que o hub tem `AGENTS.md` na raiz e seis raízes (`clients/`, `operations/`, `initiatives/`, `reference/`, `agents/`, `inbox/`), para Claude Code, OpenAI Codex (CLI) e GitHub Copilot (CLI e VS Code):

1. Abrir numa subpasta limita o que o agente pode LER e GRAVAR fora dela? Como funcionam diretório de trabalho, permissões, sandbox e diretórios adicionais?
2. Quais arquivos de instrução das pastas acima carregam (o `AGENTS.md` da raiz do hub carregaria)?
3. Há um jeito oficial de restringir uma sessão a uma pasta (só leitura dela, negar o resto)?

## Respostas

### Resumo cruzado

| | Claude Code | Codex CLI | Copilot CLI | Copilot no VS Code |
|---|---|---|---|---|
| `AGENTS.md` da raiz carrega a partir da subpasta? | Sim, sobe a árvore de diretórios (não exige git) | Só se a raiz for "project root" (por padrão, pasta com `.git`) | Documentado como "Git root and cwd" (ver nota) | Por padrão só a pasta aberta; sobe até `.git` com `chat.useCustomizationsInParentRepositories` |
| Leitura fora da subpasta | Fora do diretório de trabalho e dos adicionais pergunta (modo manual) | Não verificado para o modo padrão | Fora das pastas confiáveis, proteção heurística | "Built-in agent tools can only read and write files within the current workspace folder" |
| Gravação fora da subpasta | Pede aprovação; Bash em sandbox só grava no diretório de trabalho | "Codex asks for approval to edit files outside the workspace" | Sandbox grava só no cwd | Idem leitura (workspace) |
| Restringir a uma pasta | `permissions.blockReadsOutsideWorkingDirectories` + sandbox `denyRead`/`allowRead` + regras `Read`/`Edit` deny | Perfil de permissões `:root = "deny"` + `:minimal = "read"` (beta) | Sandbox local com caminhos negados | `chat.agent.sandbox.fileSystem.userConfiguredPaths` |

### Claude Code

**Diretório de trabalho e permissões.**

- "By default, Claude has access to files in the directory where you launched it. That directory is the session's primary working directory until you move the session with `/cd`. You can extend this access:" com `--add-dir <path>` na partida, `/add-dir` na sessão, ou `additionalDirectories` nos arquivos de settings. (https://code.claude.com/docs/en/permissions.md, seção Working directories)
- "Files in additional directories follow the same permission rules as the original working directory: they become readable without prompts apart from the network path check, and file editing permissions follow the current permission mode." (idem)
- Tabela de permissões: leitura (File reads, Grep) "No, within the working directory and additional directories" precisa de aprovação; modificação de arquivo "Yes" precisa de aprovação (modo manual). (idem, Permission system)
- Em modo auto, sem o bloqueio, leitura fora é livre: "While `permissions.blockReadsOutsideWorkingDirectories` is off, file reads other than reads from network paths run without a prompt in auto mode, including reads outside the working directories. The first time Claude uses the Read, Grep, or Glob tool on a path outside them, Claude Code asks whether to allow that read." (https://code.claude.com/docs/en/permission-modes.md)
- `/cd` move o diretório primário: "To move the session to a different primary working directory, rather than adding a directory alongside the current one, run `/cd <path>`." Regras `Cd` restringem: "A bare `Cd` deny rule disables `/cd` entirely." e "Adding any `Cd` allow rule switches `/cd` to allowlist mode". "`Cd` is not a model-invocable tool: Claude can't call it, and the rules apply only when you run `/cd` yourself." (permissions.md, seção Cd)

**Diretórios adicionais dão acesso a arquivos, não a configuração.**

- "Adding a directory extends where Claude can read and edit files. It doesn't make that directory a full configuration root: most `.claude/` configuration is not discovered from additional directories, though a few types are loaded as exceptions." (permissions.md)
- "Directories listed in `permissions.additionalDirectories` in a settings file grant file access only and don't load any of the configuration below." (idem)
- Tabela: CLAUDE.md, `.claude/rules/` e `CLAUDE.local.md` de `--add-dir` carregam "Only when `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1` is set." (idem)
- Settings do projeto não sobem da subpasta: "Hooks and other `.claude/settings.json` keys load from the current working directory's `.claude/` folder with no parent-directory fallback, alongside your user `~/.claude/settings.json` and managed settings." E "`.claude/settings.local.json` loads from the git repository root instead, even when you start Claude Code in a subdirectory, except in the cases where Claude Code doesn't use the repository root, such as on Windows". (permissions.md) Ou seja, um `.claude/settings.json` na raiz do hub não vale para sessão aberta em subpasta.

**Sandbox.**

- Desligado por padrão: "The sandbox is off by default." Escrita padrão: "The working directory, a per-user temp directory, and directories you've added". Leitura padrão: "Most of the machine, including credential files such as `~/.ssh` and `~/.aws/credentials`". (https://code.claude.com/docs/en/sandboxing.md)
- O sandbox só cobre comandos shell: "Built-in file and web tools: tools such as Read, Edit, Write, WebFetch, and WebSearch follow permission rules instead. A `denyRead` entry doesn't stop the Read tool". (idem)
- Pontos de partida para restringir: `"denyRead": ["~/"]` com `"allowRead": ["."]` (exemplo na seção do sandbox); "To deny sandboxed commands read access to home directories and mounted volumes while keeping the working directories readable, set `permissions.blockReadsOutsideWorkingDirectories` instead of writing path rules." (idem)

**Instruções (pergunta 2).**

- "Claude Code loads `CLAUDE.md` and `CLAUDE.local.md` from your current working directory and every directory above it. Run Claude Code in `foo/bar/` and it loads instructions from `foo/bar/CLAUDE.md`, `foo/CLAUDE.md`" e "Across the directory tree, content is ordered from the filesystem root down to your working directory." (https://code.claude.com/docs/en/memory.md, How CLAUDE.md files load)
- `AGENTS.md`: "By default, Claude reads `AGENTS.md` only when you have no `CLAUDE.md` in your working directory or above it." Carrega no início da sessão: "every `AGENTS.md` and `.claude/AGENTS.md` in your working directory and the directories above it." (memory.md, When Claude Code reads AGENTS.md). A página indica v2.1.277 ou posterior.
- Se houver qualquer `CLAUDE.md` na subpasta ou acima, o `AGENTS.md` deixa de ser lido: "An `AGENTS.md` and a `CLAUDE.md` or `CLAUDE.local.md` in your working directory or above it | Your `CLAUDE.md` files only". A opção `claude-md-and-agents-md` lê os dois. (memory.md)
- Subpastas abaixo do diretório de trabalho carregam sob demanda: "Instead of loading them at launch, Claude Code loads each one once Claude reads, writes, or edits another file in that subdirectory." (memory.md). Para `AGENTS.md` em subpasta: "when Claude opens a file there with the Read tool and that subdirectory has none of the three `CLAUDE.md` files of its own".
- Para ignorar ancestrais: "In large monorepos, ancestor CLAUDE.md files may contain instructions that aren't relevant to your work. The `claudeMdExcludes` setting lets you skip specific files by path or glob pattern." (memory.md)

**Restringir a uma pasta (pergunta 3).**

- `permissions.blockReadsOutsideWorkingDirectories`: "Make Claude's file tools refuse reads outside your working directories in every permission mode, including `bypassPermissions`. Claude Code denies `Read`, `Grep`, `Glob`, and `LSP` calls on those paths". Ressalva da própria doc: "Claude Code doesn't refuse shell commands the same way". "A `true` in any file applies, so a repository can turn the block on for itself but can't lift yours." (https://code.claude.com/docs/en/settings-reference.md). Exige v2.1.257 ou posterior.
- Regras de negação por caminho: "To block Claude's file tools from reading a file or directory, add a `Read` deny rule for its path, such as `Read(./.env)` or `Read(./secrets/**)`". "A `Read` deny rule also blocks the Edit and Write tools on the same path". Padrões: "`//path` Absolute path from filesystem root". Limite: "Read and Edit deny rules apply to Claude's built-in file tools, to file commands Claude Code recognizes in Bash... They don't apply to ... arbitrary subprocesses ... For OS-level enforcement that blocks all processes from accessing a path, enable the sandbox." (permissions.md, Read and Edit)
- Sandbox: `filesystem.denyRead` e `allowRead`: "re-allow specific paths within a denied region using `sandbox.filesystem.allowRead`. When read rules overlap, the rule with the narrower path applies". Em settings gerenciados: "Set `allowManagedReadPathsOnly` to `true` in managed settings so that only `allowRead` entries from managed settings are honored." (sandboxing.md)
- Gravação fora: "`acceptEdits` Automatically accepts file edits and common filesystem commands such as `mkdir`, `touch`, `mv`, and `cp` for paths in the working directory or `additionalDirectories`" (https://code.claude.com/docs/en/permission-modes.md); fora disso o modo manual pergunta.

### OpenAI Codex (CLI)

**Diretório de trabalho, sandbox e aprovações.**

- Dois eixos: "Sandbox mode: What Codex can do technically (for example, where it can write and whether it can reach the network) when it executes model-generated commands." e "Approval policy: When Codex must ask you before it executes an action". (https://developers.openai.com/codex/agent-approvals-security.md)
- Padrões: "Codex CLI / IDE extension: OS-level mechanisms enforce sandbox policies. Defaults include no network access and write permissions limited to the active workspace."; "Codex asks for approval to edit files outside the workspace or to run commands that require network access." (idem)
- Modos: "`read-only`: The agent can inspect files, but it can't edit files or run commands without approval. `workspace-write`: The agent can read files, edit within the workspace, and run routine local commands inside that boundary." (https://developers.openai.com/codex/concepts/sandboxing.md)
- Padrão por pasta: "Version-controlled folders: `Auto` (workspace write + on-request approvals); Non-version-controlled folders: `read-only`" e "Codex may also start in `read-only` until you explicitly trust the working directory". (agent-approvals-security.md, Defaults and recommendations)
- Definição de workspace: "The workspace includes the current directory and temporary directories like `/tmp`. Use the `/status` command to see which directories are in the workspace." (idem)
- Diretório de trabalho: `--cd, -C`: "Set the working directory for the agent before it starts processing your request." Diretórios extras: `--add-dir`: "Grant additional directories write access alongside the main workspace. Repeat for multiple paths." (https://developers.openai.com/codex/cli/reference, tabela de flags; o `.md` desta página não traz a tabela, os trechos vêm do HTML servido). Também: "When you need to grant Codex write access to more directories, prefer `--add-dir` rather than forcing `--sandbox danger-full-access`." (cli/reference.md). Via config: `sandbox_workspace_write.writable_roots`: "Additional writable roots when `sandbox_mode = "workspace-write"`." (https://developers.openai.com/codex/config-reference.md)
- Caminhos protegidos dentro de raízes graváveis: "`<writable_root>/.git` is protected as read-only", "`<writable_root>/.agents` is protected as read-only when it exists as a directory", "`<writable_root>/.codex` is protected as read-only when it exists as a directory." (agent-approvals-security.md)

**Instruções (pergunta 2).**

- "Project scope: Starting at the project root (typically the Git root), Codex walks down to your current working directory. If Codex cannot find a project root, it only checks the current directory. In each directory along the path, it checks for `AGENTS.override.md`, then `AGENTS.md`, then any fallback names in `project_doc_fallback_filenames`. Codex includes at most one file per directory." (https://developers.openai.com/codex/guides/agents-md.md)
- Ordem: "Codex concatenates files from the root down, joining them with blank lines. Files closer to your current directory override earlier guidance because they appear later in the combined prompt." Limite: "stops adding files once the combined size reaches the limit defined by `project_doc_max_bytes` (32 KiB by default)". Escopo global: `~/.codex/AGENTS.override.md` ou `AGENTS.md`. (idem)
- Detecção da raiz: "By default, Codex treats a directory containing `.git` as the project root. To customize this behavior, set `project_root_markers` in `config.toml`" e "Set `project_root_markers = []` to skip searching parent directories and treat the current working directory as the project root." (https://developers.openai.com/codex/config-advanced.md, Project root detection). Consequência literal: se a raiz do hub não contém um marcador (padrão `.git`), "it only checks the current directory" e o `AGENTS.md` da raiz do hub não entra. Um marcador próprio via `project_root_markers` faria a raiz contar, mas isso não foi testado.

**Restringir a uma pasta (pergunta 3).**

- Perfis de permissão (beta): "Beta. Permission profiles are under active development and may change." Há exemplo oficial "File access limited to workspace": "a permission profile that will make your workspace folders writable by Codex while denying reads to the rest of the filesystem (with limited exceptions, as determined by `:minimal`)", com `":root" = "deny"` e `":minimal" = "read"`, estendendo `:workspace`. (https://developers.openai.com/codex/permissions.md)
- Precedência: "More specific entries override broader entries. When two entries target the same path, `deny` takes precedence over `write`, and `write` takes precedence over `read`." Caminhos aceitos: `:root`, `:minimal`, `:workspace_roots`, `:tmpdir`, `/absolute/path`, `~/path`. Raízes extras: `[permissions.<name>.workspace_roots]`. (idem)
- Não se combina com o modelo antigo: "Permission profiles do not compose with the older sandbox settings. Configure either `default_permissions` and `[permissions]`, or `sandbox_mode` / `sandbox_workspace_write`, but not both." (idem)
- Sessão só leitura: `codex --sandbox read-only --ask-for-approval on-request` (agent-approvals-security.md). `--sandbox`: "Select the sandbox policy for model-generated shell commands." (cli/reference).

### GitHub Copilot CLI

**Diretórios confiáveis, permissões e sandbox.**

- "Trusted directories control where Copilot CLI can read, modify, and execute files." "When you start a Copilot CLI session, you'll be asked to confirm that you trust the files in, and below, the directory from which you launched the CLI." Opções: sessão atual, ou "This and future sessions". Lista persistida em `~/.copilot/config.json`, array `trustedFolders`. (fonte bruta de https://docs.github.com/copilot/how-tos/copilot-cli/set-up-copilot-cli/configure-copilot-cli : https://raw.githubusercontent.com/github/docs/main/content/copilot/how-tos/copilot-cli/set-up-copilot-cli/configure-copilot-cli.md)
- Aviso da própria doc: "Scoping of permissions is heuristic and GitHub does not guarantee that all files outside trusted directories will be protected." Também: "Typically, you should not launch Copilot CLI from your home directory." (https://raw.githubusercontent.com/github/docs/main/content/copilot/concepts/copilot-surfaces/copilot-cli.md, Trusted directories)
- Diretórios extras: `--add-dir=PATH`: "Allow file access to a directory and load its `.github/skills` and `.github/agents` as trusted configurations (can be used multiple times)." `/add-dir PATH` é equivalente na sessão. `--allow-all-paths`: "Disable file path verification and allow access to any path." `--disallow-temp-dir`: "Prevent automatic access to the system temporary directory." `-C` e `/cd` trocam o diretório de trabalho. (https://raw.githubusercontent.com/github/docs/main/content/copilot/reference/copilot-cli-reference/cli-command-reference.md)
- Aprovações: "While read-only operations like searching, reading files, and running read-only shell commands are allowed automatically, tools that can modify your system ... require your explicit approval". Aprovação persistida "scoped to the current location: either the Git repository root, or the working directory if you aren't in a repository." (https://raw.githubusercontent.com/github/docs/main/content/copilot/how-tos/copilot-cli/use-copilot-cli/allowing-tools.md)
- Negar escrita por caminho: `--deny-tool='write(PATH)'` "scopes the denial to that path"; "(exact or trailing-path-segment match; no glob support yet)". (cli-command-reference.md)
- Sandbox local (opt-in com `/sandbox enable`): "The sandbox is deny-by-default: unless a path is explicitly granted, a command cannot use it." Diretório de trabalho com leitura e escrita por padrão. "When you work in a subdirectory of a Git repository, Copilot grants read access to the whole repository so that commands can see the full project, while limiting writes to your current working directory and the repository's Git metadata". Os tools internos de arquivo não passam pelo sandbox do SO: "the check is a software-only safeguard rather than one the operating system enforces." (https://raw.githubusercontent.com/github/docs/main/content/copilot/concepts/agents/copilot-cli/understanding-local-sandboxing.md)
- Configurar caminhos: "You can specify paths that you want to add to the sandbox. This allows you to grant read-only or read/write access to directories and files outside the working directory. You can also deny access". "Sandbox settings are not supported in repository-level settings files." (https://raw.githubusercontent.com/github/docs/main/content/copilot/how-tos/cloud-and-local-sandboxes/configuring-local-sandbox-settings.md)

**Instruções (pergunta 2).**

- Tabela de locais: `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `.github/copilot-instructions.md`, entre outros, com a nota "Unless noted in the table below, Copilot CLI discovers repository and agent instruction files in the standard locations: the repository root, the current working directory, intermediate directories between them, and any directories nested in the path of a file it is working on." (https://raw.githubusercontent.com/github/docs/main/content/copilot/how-tos/copilot-cli/customize-copilot/add-custom-instructions.md)
- A referência de comandos é mais curta: `AGENTS.md` "In Git root and cwd". (cli-command-reference.md, Custom instructions locations). As duas páginas divergem sobre "diretórios intermediários"; para o caso do hub, ambas dizem que a raiz do repositório git e o cwd contam. Sem git, a doc só diz "Git root or current directory" para a chave de localização das permissões.
- Pasta extra por variável: "Directories listed in `COPILOT_CUSTOM_INSTRUCTIONS_DIRS` | Additional `AGENTS.md` and `*.instructions.md` files."
- Imports `@`: "Referenced files must remain within the repository... Absolute paths and paths beginning with `~/` are not loaded." (add-custom-instructions.md)

**Restringir a uma pasta (pergunta 3).** O mais próximo documentado é o sandbox local com "Include working directory" (leitura e escrita só do cwd), ressalvando que dentro de repositório git a leitura abrange o repositório inteiro e exige regras de negação. Não há, nas páginas lidas, uma opção "só esta pasta" dedicada.

### GitHub Copilot no VS Code

- Pasta aberta é o limite: "Workspace-limited file access: Built-in agent tools can only read and write files within the current workspace folder. You can optionally grant read-only access to additional folders with the `chat.additionalReadAccessFolders` setting." (https://raw.githubusercontent.com/microsoft/vscode-docs/main/docs/agents/run/security.md)
- Gravações detectadas fora do workspace no terminal: "`chat.tools.terminal.blockDetectedFileWrites` ... defaults to `outsideWorkspace`, which requires approval for detected writes outside the workspace." (https://raw.githubusercontent.com/microsoft/vscode-docs/main/docs/agents/run/approvals.md)
- Instruções, sessão local: "By default, VS Code only discovers customization files within your open workspace folder(s). Enable the `chat.useCustomizationsInParentRepositories` setting to also discover customizations from the parent repository." "When this setting is enabled, VS Code walks up the folder hierarchy from each workspace folder until it finds a `.git` folder. If found, it collects customizations from all folders between the workspace folder and the repository root (inclusive)" (inclui `AGENTS.md`). (https://raw.githubusercontent.com/microsoft/vscode-docs/main/docs/agent-customization/overview.md)
- `AGENTS.md` aninhados: "`chat.useNestedAgentsMdFiles` ... The setting is disabled by default."; "Place the primary file at the repository root." (https://raw.githubusercontent.com/microsoft/vscode-docs/main/docs/agent-customization/custom-instructions.md)
- Sessões em Agent Host seguem as regras do harness escolhido: "Agent Host sessions use the discovery rules and file formats of the selected harness." (idem)
- Sandbox: "The sandbox automatically grants read and write access to the current working directory." Caminhos via `chat.agent.sandbox.fileSystem.userConfiguredPaths` com `readwritePaths`, `readonlyPaths`, `deniedPaths`; "`deniedPaths` takes precedence over `readonlyPaths`, which takes precedence over `readwritePaths`." (https://raw.githubusercontent.com/microsoft/vscode-docs/main/docs/agents/run/agent-sandboxing.md)

## Não verificado

- Codex, modo `workspace-write` padrão: a doc diz que "Codex can read files, make edits, and run commands in the workspace", mas não afirma literalmente se leitura FORA do workspace é permitida ou bloqueada. O exemplo de perfil "denying reads to the rest of the filesystem" sugere que o padrão lê fora, o que é inferência e não foi tratado como fato.
- Codex: se o `AGENTS.md` de pastas ACIMA do cwd carrega quando a raiz é marcada por `project_root_markers` customizado. A doc descreve o mecanismo; não foi exercitado.
- Copilot CLI: quais diretórios acima do cwd carregam `AGENTS.md` sem `.git` (as duas páginas oficiais divergem: "intermediate directories" versus "In Git root and cwd").
- Copilot CLI: comportamento de leitura fora das pastas confiáveis em modo padrão (sem sandbox) além da frase "heuristic"; as páginas consultadas não listam as regras de verificação de caminho.
- VS Code: aplicação de `chat.additionalReadAccessFolders` e regras do Agent Host para harness Claude/Codex dentro do VS Code (a doc manda seguir "the selected harness's working-folder and nested-instruction rules" sem detalhar).
- Claude Code: se há forma documentada de "negar tudo e permitir só uma pasta" só com regras `Read`/`Edit` (ex.: deny em `//**` com allow na subpasta). A doc dá `blockReadsOutsideWorkingDirectories` e sandbox `denyRead`+`allowRead`; a precedência entre deny e allow nas regras `Read` não foi lida nesta varredura.

## Precisa de teste

1. Claude Code aberto em `clients/voegol/app-migration/` num hub sem `CLAUDE.md`: confirmar que o `AGENTS.md` da raiz carrega (linha `no CLAUDE.md found; AGENTS.md loaded: ...`) e que um `CLAUDE.md` em qualquer ancestral suprime os `AGENTS.md`.
2. Claude Code: com `blockReadsOutsideWorkingDirectories: true`, confirmar que `Read` em outra raiz do hub é recusado, e o que ocorre com `cat`/`grep` via Bash fora do sandbox.
3. Codex: com hub sem `.git`, confirmar que só o `AGENTS.md` do cwd carrega; com `project_root_markers` customizado, confirmar que o da raiz carrega.
4. Codex: em `workspace-write`, tentar ler `../../reference/x.md` (fora do cwd) e gravar em `../../inbox/x.md`; verificar se a leitura passa e se a gravação pede aprovação.
5. Codex: perfil `:root = "deny"` + `:minimal = "read"` (beta) numa subpasta com `workspace_roots` de uma segunda raiz; confirmar o comportamento no Windows nativo.
6. Copilot CLI: com e sem `.git` na raiz do hub, quais `AGENTS.md` carregam a partir de uma subpasta (`/instructions` lista os descobertos).
7. Copilot CLI sandbox: se o hub for repositório git, confirmar que a leitura do repositório inteiro vale mesmo com cwd na subpasta e que regras de negação fecham as outras raízes.
8. VS Code: abrir só a subpasta como workspace e verificar se o `AGENTS.md` da raiz carrega com e sem `chat.useCustomizationsInParentRepositories` (exige `.git`).

## Fontes

- Claude Code: https://code.claude.com/docs/en/permissions.md ; https://code.claude.com/docs/en/permission-modes.md ; https://code.claude.com/docs/en/memory.md ; https://code.claude.com/docs/en/sandboxing.md ; https://code.claude.com/docs/en/settings.md ; https://code.claude.com/docs/en/settings-reference.md
- Codex: https://developers.openai.com/codex/guides/agents-md.md ; https://developers.openai.com/codex/agent-approvals-security.md ; https://developers.openai.com/codex/concepts/sandboxing.md ; https://developers.openai.com/codex/permissions.md ; https://developers.openai.com/codex/config-advanced.md ; https://developers.openai.com/codex/config-reference.md ; https://developers.openai.com/codex/cli/reference.md e a página HTML https://developers.openai.com/codex/cli/reference (tabela de flags `--cd`, `--add-dir`, `--sandbox`); repositório https://github.com/openai/codex (docs/sandbox.md e docs/agents_md.md apenas redirecionam para developers.openai.com)
- Copilot CLI (fonte bruta do repositório github/docs, espelho de docs.github.com), todos sob https://raw.githubusercontent.com/github/docs/main/content/copilot/ : how-tos/copilot-cli/set-up-copilot-cli/configure-copilot-cli.md ; how-tos/copilot-cli/customize-copilot/add-custom-instructions.md ; how-tos/copilot-cli/use-copilot-cli/allowing-tools.md ; reference/copilot-cli-reference/cli-command-reference.md ; concepts/copilot-surfaces/copilot-cli.md ; concepts/agents/copilot-cli/understanding-local-sandboxing.md ; how-tos/cloud-and-local-sandboxes/configuring-local-sandbox-settings.md ; e https://raw.githubusercontent.com/github/copilot-cli/main/README.md
- Copilot no VS Code (fonte bruta de microsoft/vscode-docs, espelho de code.visualstudio.com), todos sob https://raw.githubusercontent.com/microsoft/vscode-docs/main/docs/ : agent-customization/overview.md ; agent-customization/custom-instructions.md ; agents/run/security.md ; agents/run/approvals.md ; agents/run/agent-sandboxing.md
