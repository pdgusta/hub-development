# Porta 1: sessão de harness aberta na raiz do hub

Pesquisa em fonte primária (texto bruto via `curl`), 2026-10-10. Saída de modelo; consultar as fontes para decisões.

## Pergunta

Com a sessão aberta na RAIZ do hub (AGENTS.md na raiz; subpastas clients/, operations/, initiatives/, reference/, agents/, inbox/), para Claude Code, Codex CLI e GitHub Copilot (CLI e VS Code):
1. Quais arquivos de instrução carregam sozinhos (pasta atual, acima, subpastas)? Quando um AGENTS.md de subpasta é lido?
2. Há limite de tamanho/quantidade? Imports (@arquivo) funcionam?
3. Como a sessão chega a um arquivo em subpasta funda: só por ferramentas de leitura e busca do harness?

## Respostas

### Claude Code (code.claude.com/docs/en/memory.md)

**1. Carga automática**
- Acima da pasta atual, no início: "CLAUDE.md and CLAUDE.local.md files in the directory hierarchy above the working directory are loaded at launch. Files in subdirectories load on demand."
- Ordem: "Across the directory tree, content is ordered from the filesystem root down to your working directory."
- AGENTS.md é lido diretamente, mas só se não houver CLAUDE.md: "An `AGENTS.md`, and no `CLAUDE.md` or `CLAUDE.local.md` in your working directory or above it | Your `AGENTS.md`" e "An `AGENTS.md` and a `CLAUDE.md` or `CLAUDE.local.md` in your working directory or above it | Your `CLAUDE.md` files only". Versão: "Reading `AGENTS.md` directly requires Claude Code v2.1.277 or later."
- Início da sessão: "every `AGENTS.md` and `.claude/AGENTS.md` in your working directory and the directories above it."
- Subpasta, sob demanda: "a subdirectory's `AGENTS.md`, when Claude opens a file there with the Read tool and that subdirectory has none of the three `CLAUDE.md` files of its own".
- CLAUDE.md de subpasta: "Instead of loading them at launch, Claude Code loads each one once Claude reads, writes, or edits another file in that subdirectory. Reading includes viewing the file with a Bash command that counts as a read, such as `cat` or `head` on a single file."
- Opção para ler os dois: `claude-md-and-agents-md` = "Your `CLAUDE.md` and `AGENTS.md` files together, each directory's `CLAUDE.md` files first and its `AGENTS.md` after them."
- AGENTS.md lido pela configuração não dispara hooks `InstructionsLoaded` ("Don't fire").

**2. Limites e imports**
- Tamanho (recomendação, não corte): "target under 200 lines per CLAUDE.md file. Longer files consume more context and reduce adherence."
- "first 200 lines or 25KB" vale para o MEMORY.md da auto memory, não para CLAUDE.md: "The first 200 lines of `MEMORY.md`, or the first 25KB, whichever comes first, are loaded at the start of every conversation."
- Imports funcionam: "CLAUDE.md files can import additional files using `@path/to/import` syntax. Imported files are expanded and loaded into context at launch". "Relative paths resolve relative to the file containing the import, not the working directory. Imported files can recursively import other files, with a maximum depth of four hops."
- Em AGENTS.md também: "Inside each `AGENTS.md`: `@path` imports are expanded".
- "Imports help you organize a long file but don't reduce its context cost, because imported files also load at launch."
- Limite de quantidade de arquivos: não declarado na página.

**3. Chegar a arquivo fundo**
- A página de memória descreve só o gatilho (ler/escrever/editar na subpasta). Ferramentas (code.claude.com/docs/en/tools-reference.md): "`Read` | Reads the contents of files", "`Glob` | Finds files based on pattern matching", "`Grep` | Searches for patterns in file contents". Nota da tabela: Glob e Grep "Absent by default on macOS, Linux, and WSL".

### OpenAI Codex CLI (developers.openai.com/codex/guides/agents-md.md; o docs/agents_md.md do repo só aponta para essa página)

**1. Carga automática**
- "Codex builds an instruction chain when it starts (once per run; in the TUI this usually means once per launched session)."
- Global: "In your Codex home directory ... Codex reads `AGENTS.override.md` if it exists. Otherwise, Codex reads `AGENTS.md`."
- Projeto: "Starting at the project root (typically the Git root), Codex walks down to your current working directory. If Codex cannot find a project root, it only checks the current directory. In each directory along the path, it checks for `AGENTS.override.md`, then `AGENTS.md`, then any fallback names in `project_doc_fallback_filenames`. Codex includes at most one file per directory."
- Ordem: "Codex concatenates files from the root down, joining them with blank lines. Files closer to your current directory override earlier guidance because they appear later in the combined prompt."
- Subpastas abaixo do cwd: "Codex stops searching once it reaches your current directory". Com sessão na raiz do hub, a doc descreve só o AGENTS.md da raiz (e o global); não descreve AGENTS.md de subpasta sendo lido ao trabalhar ali. O exemplo da doc para ativar um de subpasta é `codex --cd subdir`.
- CLAUDE.md e copilot-instructions.md: "Filenames not on this list are ignored for instruction discovery" (lista = AGENTS.override.md, AGENTS.md e `project_doc_fallback_filenames`).

**2. Limites e imports**
- "Codex skips empty files and stops adding files once the combined size reaches the limit defined by `project_doc_max_bytes` (32 KiB by default)." Já a página de config avançada descreve o parâmetro como "how much to read from each `AGENTS.md` file" (as duas descrições diferem).
- "Codex includes at most one file per directory."
- Imports `@arquivo`: nada nas páginas consultadas.

**3. Chegar a arquivo fundo**
- Páginas consultadas não descrevem o mecanismo de leitura/busca de arquivos.

### GitHub Copilot CLI (docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-custom-instructions)

**1. Carga automática**
- "Copilot CLI discovers repository and agent instruction files in the standard locations: the repository root, the current working directory, intermediate directories between them, and any directories nested in the path of a file it is working on."
- Tabela: `.github/copilot-instructions.md` ("Repository-wide instructions, discovered in the standard locations"); `AGENTS.md` ("Agent instructions, discovered in the standard locations"); `CLAUDE.md` ("Agent instructions, discovered in the standard locations. Copilot CLI also uses `.claude/CLAUDE.md`."); `$HOME/.copilot/copilot-instructions.md`; "Directories listed in `COPILOT_CUSTOM_INSTRUCTIONS_DIRS` | Additional `AGENTS.md` and `*.instructions.md` files."
- "Modular instruction files (those matching `*.instructions.md`) are path-specific—a file with an `applyTo` value applies only to matching files."
- "Copilot CLI combines their instructions. It removes duplicate copies ... but does not define a general precedence order between these files."

**2. Limites e imports**
- "In `.github/copilot-instructions.md`, `AGENTS.md`, or `CLAUDE.md`, use `@` followed by a relative path to include another file. Copilot CLI reads the referenced file immediately and supports references within referenced files."
- Limite de tamanho/quantidade: não declarado na página.

**3.** "any directories nested in the path of a file it is working on" indica carga ao trabalhar em arquivo de subpasta; o gatilho exato não é descrito (ver Não verificado).

### GitHub Copilot no VS Code (code.visualstudio.com/docs/copilot/customization/custom-instructions)

**1. Carga automática**
- "Project instructions are automatically included according to the selected harness."
- "AGENTS.md is a cross-agent format for project guidance. It is supported by multiple harnesses, including Copilot and OpenAI Codex, and by the Local agent. Place the primary file at the repository root."
- Setting `chat.useAgentsMdFile` liga/desliga AGENTS.md; a página também remete a ele para CLAUDE.md ("To enable or disable support for CLAUDE.md files, configure the chat.useAgentsMdFile"). Locais do agente Local: ".github/copilot-instructions.md, AGENTS.md, or CLAUDE.md".
- Subpastas: "Nested AGENTS.md files is experimental and might change or be removed." "`chat.useNestedAgentsMdFiles` ... The setting is disabled by default." "When enabled, VS Code lists nested AGENTS.md files with their folder locations so the Local agent can load relevant instructions for the task." (lista os arquivos; o agente carrega os relevantes).
- Agent Host: "follow the selected harness's working-folder and nested-instruction rules."

**2. Limites e imports**
- Imports `@`: não descritos; a doc usa links Markdown: "To reference files or URLs in instructions, use Markdown links. Relative file paths resolve from the instructions file."
- Limite de tamanho/quantidade: não encontrado.

**3.** Não descrito na página.

### Contexto lateral: Copilot no GitHub.com (cloud agent)
docs.github.com/en/copilot/how-tos/configure-custom-instructions/add-repository-instructions: "You can create one or more `AGENTS.md` files, stored anywhere within the repository. When Copilot is working, the nearest `AGENTS.md` file in the directory tree will take precedence." Não é sessão local.

## Não verificado

- Codex: imports `@arquivo` em AGENTS.md; mecanismo de leitura/busca de arquivos fundos; se AGENTS.md abaixo do cwd é lido ao trabalhar ali (a doc só descreve da raiz do projeto até o cwd).
- Codex: contradição "32 KiB combinado" (guia) x "per file" (config avançada); qual vale no código.
- Copilot CLI: gatilho exato dos "directories nested in the path of a file"; limite de tamanho.
- Copilot VS Code: limite de tamanho/quantidade; se `@` funciona; como o agente Local carrega um nested AGENTS.md depois de listado.
- Claude Code: se Glob/Grep existem por padrão no Windows (a tabela só cita macOS, Linux e WSL); se Grep/Glob sem Read disparam a carga de instruções de subpasta (a doc cita Read/Write/Edit e Bash cat/head); limite de quantidade de arquivos.
- Nenhuma fonte tratou de harness sobre pasta mantida por LiveSync/CouchDB.

## Precisa de teste

- Claude Code na raiz, AGENTS.md na raiz e outro em `initiatives/x/`: confirmar que o de subpasta só carrega após Read ali e se Grep/Glob bastam.
- Claude Code: qualquer CLAUDE.md acima do cwd (pasta pai do hub) desliga a leitura direta de AGENTS.md.
- Codex na raiz: confirmar que AGENTS.md de subpasta não entra; confirmar imports `@`.
- Copilot VS Code com `chat.useNestedAgentsMdFiles` ligado e Copilot CLI: comportamento de carga dos aninhados.

## Fontes

- https://code.claude.com/docs/en/memory.md
- https://code.claude.com/docs/en/tools-reference.md
- https://developers.openai.com/codex/guides/agents-md.md
- https://developers.openai.com/codex/config-advanced.md (seção "Project instructions discovery")
- https://raw.githubusercontent.com/openai/codex/main/docs/agents_md.md
- https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-custom-instructions
- https://docs.github.com/en/copilot/how-tos/configure-custom-instructions/add-repository-instructions
- https://code.visualstudio.com/docs/copilot/customization/custom-instructions
