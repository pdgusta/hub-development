# Porta 8: sessão aberta num repositório de código fora do hub

Pesquisa em fonte primária (texto bruto via curl, 2026-10-10). Ticket: `.scratch/context-hub/issues/36-portas-de-entrada-do-hub.md`.

## Pergunta

Com a sessão aberta num repositório de código fora do hub (ex.: videos-transcriptor), como cada harness (Claude Code, Codex, Copilot) carrega a camada global de instruções, importa arquivo de outra pasta (ex.: `C:/context-hub/AGENTS.md`), trata diretórios adicionais e aceita skills globais apontando para o hub?

## Respostas (por harness)

### 1. Camada global de instruções e ordem

**Claude Code**
- Global: "`~/.claude/CLAUDE.md` | Personal preferences for all projects". Ordem: "The table below lists them in load order, from broadest scope to most specific, so a project instruction appears in context after a user instruction." (memory.md)
- Entre diretórios: "content is ordered from the filesystem root down to your working directory ... instructions closer to where you launched Claude are read last." Tudo é concatenado: "All discovered files are concatenated into context rather than overriding each other."
- `~/.claude/AGENTS.md`: a documentação não cita esse arquivo (zero ocorrências em memory.md, settings.md, skills.md, permissions.md, cli-reference.md). Ver "Não verificado".
- `AGENTS.md` do projeto: "By default, Claude reads `AGENTS.md` only when you have no `CLAUDE.md` in your working directory or above it." O global não conta nessa checagem: "**Don't count, and keep loading alongside `AGENTS.md`**: your `~/.claude/CLAUDE.md`, your organization's managed `CLAUDE.md`, and `.claude/rules/` files". Exige v2.1.277 ou posterior. Opção `claude-md-and-agents-md`: "Your `CLAUDE.md` and `AGENTS.md` files together, each directory's `CLAUDE.md` files first and its `AGENTS.md` after them."
- Fonte: https://code.claude.com/docs/en/memory.md (seções "Choose where to put CLAUDE.md files", "How CLAUDE.md files load", "AGENTS.md").

**Codex**
- Global: "In your Codex home directory (defaults to `~/.codex`, unless you set `CODEX_HOME`), Codex reads `AGENTS.override.md` if it exists. Otherwise, Codex reads `AGENTS.md`. Codex uses only the first non-empty file at this level."
- Projeto: "Starting at the project root (typically the Git root), Codex walks down to your current working directory ... Codex includes at most one file per directory."
- Ordem: "Codex concatenates files from the root down ... Files closer to your current directory override earlier guidance because they appear later in the combined prompt." Limite: "`project_doc_max_bytes` (32 KiB by default)".
- Fonte: https://developers.openai.com/codex/guides/agents-md.md

**Copilot CLI**
- Global: "`$HOME/.copilot/copilot-instructions.md` | User-level instructions that apply across repositories." e "`$HOME/.copilot/instructions/**/*.instructions.md` | Modular user-level instructions." "If you set the `COPILOT_HOME` environment variable, Copilot CLI uses that directory instead of `$HOME/.copilot`".
- Projeto: `.github/copilot-instructions.md`, `AGENTS.md`, `CLAUDE.md` (também `.claude/CLAUDE.md`), `GEMINI.md`, "discovered in the standard locations: the repository root, the current working directory, intermediate directories between them".
- Ordem: "Copilot CLI combines their instructions ... but does not define a general precedence order between these files. Avoid conflicting instructions."
- Fonte: https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-custom-instructions

### 2. Import de arquivo de outra pasta

**Claude Code: sim, caminho absoluto permitido.**
- "CLAUDE.md files can import additional files using `@path/to/import` syntax. ... Both relative and absolute paths are allowed. Relative paths resolve relative to the file containing the import ... maximum depth of four hops."
- No escopo de usuário não há diálogo: "User-scope memory files, such as `~/.claude/CLAUDE.md` and `~/.claude/rules/`, are files you wrote yourself. Except in Cowork sessions on your desktop, Claude Code loads their imports without the dialog". (Em Cowork no desktop: "skips any import in a user-scope file that resolves to a path outside the session's working directory".)
- Imports também valem dentro de `AGENTS.md` lido pela configuração: "Inside each `AGENTS.md`: `@path` imports are expanded".
- Em arquivo de projeto, import fora do diretório de trabalho é "external" e pede aprovação única por projeto.
- "imported files also load at launch" (não reduz custo de contexto). Espaço no caminho: barra invertida antes de cada espaço; aspas fazem o import não ocorrer.
- Fonte: https://code.claude.com/docs/en/memory.md ("Import additional files").

**Codex: não verificado.** A página oficial de AGENTS.md não descreve sintaxe de import; só concatenação dos arquivos descobertos e `project_doc_fallback_filenames` (nomes de arquivo dentro dos diretórios do projeto, não caminho externo).

**Copilot CLI: sim, mas só caminho relativo dentro do repositório (ou do diretório de instruções locais); absoluto não.**
- "In `.github/copilot-instructions.md`, `AGENTS.md`, or `CLAUDE.md`, use `@` followed by a relative path to include another file."
- "Referenced files must remain within the repository, or within the custom instructions directory for local instructions. Absolute paths and paths beginning with `~/` are not loaded. File references are not expanded in `GEMINI.md` or `*.instructions.md` files."
- Fonte: página de instruções do Copilot CLI acima ("Referencing other files").

### 3. Diretórios adicionais

**Claude Code**
- "The `--add-dir` flag gives Claude access to additional directories outside your main working directory. By default, CLAUDE.md files from these directories are not loaded."
- Variável: "`CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1 claude --add-dir ../shared-config`". "This loads `CLAUDE.md`, `.claude/CLAUDE.md`, `.claude/rules/*.md`, and `CLAUDE.local.md` from the additional directory." Pode ir no bloco `env` de `~/.claude/settings.json`.
- O diretório adicional carrega o `AGENTS.md` dele? Não: tabela "Where AGENTS.md differs from CLAUDE.md": "Directories you add with `--add-dir` while `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD` is set | Their `CLAUDE.md` loads | Their `AGENTS.md` doesn't load". A doc não descreve o contorno (um `CLAUDE.md` no diretório adicional com `@AGENTS.md`); ver "Precisa de teste".
- Persistência: "To persist these directories across sessions, set `permissions.additionalDirectories` in settings". Porém: "Directories listed in `permissions.additionalDirectories` in a settings file grant file access only and don't load any of the configuration below." As exceções (skills, CLAUDE.md com a variável) valem para `--add-dir` / `/add-dir`.
- Skills em `--add-dir`: "Skills in `.claude/skills/`: Yes, with live reload".
- Fontes: https://code.claude.com/docs/en/memory.md ("Load from additional directories", "Where AGENTS.md differs from CLAUDE.md"); https://code.claude.com/docs/en/permissions.md ("Additional directories grant file access, not configuration"); https://code.claude.com/docs/en/cli-reference.md (`--add-dir`).

**Codex**
- `--add-dir` existe como acesso de escrita: "When you need to grant Codex write access to more directories, prefer `--add-dir` rather than forcing `--sandbox danger-full-access`." Em config: `sandbox_workspace_write.writable_roots` = "Additional writable roots when `sandbox_mode = "workspace-write"`".
- A documentação lida não diz que um diretório adicional carregue seu `AGENTS.md`; a descoberta descrita é só da raiz do projeto até o cwd. Não verificado.
- Fontes: https://developers.openai.com/codex/cli/reference.md ; https://developers.openai.com/codex/config-reference.md ; https://developers.openai.com/codex/guides/agents-md.md

**Copilot CLI**
- `--add-dir=PATH`: "Allow file access to a directory and load its `.github/skills` and `.github/agents` as trusted configurations (can be used multiple times)." `/add-dir PATH` idem. O texto não cita instruções nem `AGENTS.md`.
- Variável para instruções: na tabela de locais, "Directories listed in `COPILOT_CUSTOM_INSTRUCTIONS_DIRS` | Additional `AGENTS.md` and `*.instructions.md` files. Separate multiple directories with commas." Logo, essa variável apontando para a pasta do hub é o mecanismo documentado para carregar o `AGENTS.md` de lá. Skills: "`COPILOT_SKILLS_DIRS` | Comma-separated list of additional directories for skills."
- Fontes: https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-command-reference ; página de instruções do Copilot CLI.

### 4. Skills globais apontando para uma pasta do hub

**Claude Code: symlink sim.**
- "Personal | `~/.claude/skills/<skill-name>/SKILL.md` | All your projects on this machine".
- "**Symlinked folders**: a `<skill-name>` entry in the enterprise, personal, or project location can be a symlink to a directory elsewhere on disk. Claude Code reads `SKILL.md` from the target and loads the skill once even if several locations point at the same target."
- Junction: a doc diz só "symlink". `~/.agents/skills` não é citado na doc do Claude Code. Sobre Windows, a doc (seção AGENTS.md) avisa: "Creating a symlink there needs Administrator privileges or Developer Mode".
- Fonte: https://code.claude.com/docs/en/skills.md ("Where skills live").

**Codex: symlink sim.**
- "`USER` | `$HOME/.agents/skills` | Use to curate skills relevant to a user that apply to any repository the user may work in."
- "Codex supports symlinked skill folders and follows the symlink target when scanning these locations."
- Fonte: https://developers.openai.com/codex/skills.md

**Copilot CLI: locais sim, symlink não citado.**
- "For **personal skills**, shared across projects, create a `~/.copilot/skills` or `~/.agents/skills` directory in your local home directory." Projeto: `.github/skills`, `.claude/skills` ou `.agents/skills`.
- Alternativa documentada sem symlink: `COPILOT_SKILLS_DIRS` (acima).
- Fonte: https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-skills ; cli-command-reference.

## Não verificado

- `~/.claude/AGENTS.md`: a documentação do Claude Code não menciona; sem evidência de que seja lido.
- Codex: suporte a import (`@`) em `AGENTS.md`; se `--add-dir` carrega `AGENTS.md` do diretório adicional; se `~/.codex/AGENTS.md` pode ser symlink.
- Copilot CLI: se a regra "absolute paths and `~/` not loaded" vale também para `$HOME/.copilot/copilot-instructions.md`; se `--add-dir` carrega instruções/`AGENTS.md`; symlink em pastas de skill.
- Junction do Windows como alternativa a symlink, em qualquer harness: nenhuma doc lida cita junction.
- `~/.agents/skills` no Claude Code: não citado.

## Precisa de teste

- Claude Code: `~/.claude/CLAUDE.md` com `@C:/context-hub/AGENTS.md` (caminho Windows com `C:/`) carrega sem dialog? Conferir em `/memory`.
- Claude Code: `--add-dir C:\context-hub` com `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1` carrega um `CLAUDE.md` de lá que importe `@AGENTS.md`? E o `AGENTS.md` sozinho não carrega (como a tabela diz)?
- Claude Code no Windows: junction em `~/.claude/skills/<nome>` apontando para o hub é descoberta?
- Codex: import em `AGENTS.md`; `--add-dir` carregando `AGENTS.md`.
- Copilot CLI: `COPILOT_CUSTOM_INSTRUCTIONS_DIRS=C:\context-hub` carrega o `AGENTS.md` do hub no Windows (`/instructions` lista o arquivo).

## Fontes

- https://code.claude.com/docs/en/memory.md
- https://code.claude.com/docs/en/permissions.md
- https://code.claude.com/docs/en/skills.md
- https://code.claude.com/docs/en/cli-reference.md
- https://developers.openai.com/codex/guides/agents-md.md
- https://developers.openai.com/codex/skills.md
- https://developers.openai.com/codex/cli/reference.md
- https://developers.openai.com/codex/config-reference.md
- https://developers.openai.com/codex/config-advanced.md
- https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-custom-instructions
- https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-skills
- https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-command-reference
