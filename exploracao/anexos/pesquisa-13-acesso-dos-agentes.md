---
title: Pesquisa 13, acesso dos agentes ao hub (contrato, skills, MCP, Windows × WSL, Maestri)
data: 2026-10-01
origem: subagente de pesquisa (Claude Code), ticket "Acesso dos agentes: pesquisa"
aviso: saída de modelo. Cada afirmação traz a fonte primária (docs oficiais, código do repositório oficial ou arquivo local lido), com citação curta. Nada foi instalado, testado nem configurado. O que não foi conferido na fonte está marcado como **não verificado**.
---

# Acesso dos agentes ao hub: levantamento de 01/10/2026

## Resumo (uma tela)

**Pergunta:** como fazer Claude Code, Codex CLI e OpenCode, avulsos ou dentro do Maestri, em qualquer pasta
e nas duas máquinas, carregarem o contrato do hub, acharem as skills do hub e terem o MCP do hub, sem cópia
manual por máquina?

**Resposta curta:** os três harnesses têm uma **camada global por usuário**. Ela é o único ponto que vale em
qualquer pasta de trabalho, e é por ela que o hub deve entrar. Mas cada um a expõe de um jeito:

1. **Contrato.** Só o Claude Code tem import de arquivo: um `@caminho` dentro do `~/.claude/CLAUDE.md` puxa um
   arquivo fora do projeto, sem diálogo de aprovação. O OpenCode v1 aceita caminhos absolutos ou com `~` na
   chave `instructions` do `opencode.json` global. O Codex **não tem import**: lê um único `AGENTS.md` em
   `~/.codex` (ou em `CODEX_HOME`), com teto de 32 KiB somando todas as camadas. Para o Codex, o contrato precisa
   *estar* em `~/.codex/AGENTS.md`, por link ou por cópia gerada. Se esse link funciona é **não verificado**.
2. **Skills.** Existe uma convenção compartilhada: `~/.agents/skills` é a pasta USER do Codex e uma das pastas
   globais do OpenCode. O **Claude Code não lê `~/.agents/skills`**: só `~/.claude/skills`, que o OpenCode
   também lê. Na prática, cada skill do hub precisa de duas entradas, uma em `~/.agents/skills` e outra em
   `~/.claude/skills`. É o padrão que o vault já usa hoje nesta máquina. Os três documentam suporte a
   *symlink*; nenhum documenta *junction*. Nesta máquina, o Claude Code carrega skills ligadas por junction
   (observado). No Codex e no OpenCode há issues oficiais fechadas sobre links e caminhos no Windows.
3. **MCP.** Cada harness tem formato e arquivo próprios: `~/.claude.json` ou `.mcp.json` (JSON),
   `~/.codex/config.toml` (TOML) e `opencode.json` (chave `mcp`). Os três aceitam stdio e HTTP streamable.
   Nenhum lê o arquivo do outro. Para compartilhar entre máquinas, os pontos mais limpos são: um arquivo do hub
   passado ao Claude Code (`--mcp-config`, ou um plugin com `.mcp.json` carregado por `CLAUDE_CODE_PLUGIN_DIRS`),
   um arquivo do hub apontado por `OPENCODE_CONFIG` e, no Codex, um bloco `[mcp_servers.*]` no `config.toml` de
   cada máquina. O Codex não documenta include de outro arquivo de config.
4. **Windows × WSL.** Nos três, uma instalação dentro do WSL usa o **home Linux** e **não enxerga** a
   configuração do lado Windows. Só o Codex documenta um jeito de compartilhar: `CODEX_HOME=/mnt/c/Users/<user>/.codex`.
   Num WSL, o Maestri instala as skills dele **por distribuição**.
5. **Maestri** (docs oficiais em themaestri.app): abre o shell na pasta de trabalho do workspace e digita o
   comando do preset (`claude`, `codex --no-daemon`, `opencode`). Para injetar um papel (role), **inicia o
   agente em `<projeto>/.maestri/roles/<role-id>/`**, uma pasta que leva `CLAUDE.md`, `AGENTS.md` e `role.json`.
   Também exporta variáveis `MAESTRI_*` e instala as skills oficiais dele em `~/.claude/skills` e
   `~/.agents/skills`.

**Leitura para o ticket:**
- O contrato do hub deve entrar pela camada **global** de cada harness, e não pela pasta do workspace. Dois
  motivos levantados aqui:
  - Com papel, o Maestri põe o agente numa subpasta que tem `CLAUDE.md` próprio. Pela regra do Claude Code, um
    `CLAUDE.md` na pasta de trabalho ou acima dela faz o `AGENTS.md` do workspace deixar de ser lido.
  - Se a pasta do workspace não for repositório git, o Codex só olha a pasta atual, ou seja, a pasta do papel.
- Skills e MCP pedem, por máquina e por lado (Windows/WSL), um passo de "ligar" que hoje nenhum harness faz
  sozinho.

## Tabela comparativa

Legenda: S = sim, P = parcial, N = não, NV = não verificado.

| | Claude Code | Codex CLI | OpenCode (v1, estável) |
|---|---|---|---|
| **Contrato global** | `~/.claude/CLAUDE.md` (+ `~/.claude/rules/`) | `~/.codex/AGENTS.override.md` ou `AGENTS.md` (1 arquivo) | `~/.config/opencode/AGENTS.md`; se ausente, `~/.claude/CLAUDE.md` |
| **Contrato do projeto** | `CLAUDE.md` da pasta de trabalho e das pastas acima; `AGENTS.md` só se não houver `CLAUDE.md` | `AGENTS.md` da raiz git até a pasta de trabalho | `AGENTS.md` (ou `CLAUDE.md`) achado subindo a partir da pasta de trabalho |
| **Apontar para arquivo fora do projeto** | S: `@caminho` absoluto ou relativo; 4 níveis; sem diálogo no escopo de usuário | N (sem import); só `CODEX_HOME`, `model_instructions_file` (substitui o prompt embutido) ou `developer_instructions` (texto inline) | S: `instructions` aceita absoluto, `~/` e glob (doc + código); **no v2 não é resolvido** |
| **Limite documentado** | carrega até 4 MiB por arquivo; recomenda < 200 linhas | 32 KiB no total (`project_doc_max_bytes`) | nenhum encontrado (NV) |
| **Skills: pastas globais** | `~/.claude/skills` | `~/.agents/skills` (+ `$CODEX_HOME/skills`, obsoleta) | `~/.config/opencode/skills`, `~/.claude/skills`, `~/.agents/skills` |
| **Skills: apontar outra pasta** | `--add-dir`, plugin (`--plugin-dir`, `CLAUDE_CODE_PLUGIN_DIRS`) | `[[skills.config]] path` (habilita/desabilita; descoberta por ali é NV) | `skills.paths` no `opencode.json` (schema oficial) |
| **Skills por symlink** | S (doc) | S (doc: "supports symlinked skill folders") | S (o código faz glob com `symlink: true`) |
| **Skills por junction (Windows)** | S, observado nesta máquina (não documentado) | NV; issue oficial #8400 relatava falha (fechada como duplicata) | NV |
| **MCP: usuário** | `claude mcp add --scope user` → `~/.claude.json` | `~/.codex/config.toml` `[mcp_servers.<id>]` | `~/.config/opencode/opencode.json` → `mcp` |
| **MCP: projeto** | `.mcp.json` na raiz (pede aprovação) | `.codex/config.toml` (só em projeto confiável) | `opencode.json` do projeto |
| **MCP: arquivo avulso** | `--mcp-config <arquivo>`; plugin com `.mcp.json` | `--profile` → `~/.codex/<nome>.config.toml`; `-c` | `OPENCODE_CONFIG=<arquivo>` |
| **Transportes** | stdio, HTTP (SSE e WS também) | stdio, HTTP streamable | `local` (stdio), `remote` (HTTP) |
| **Variáveis no MCP** | `${VAR}` e `${VAR:-padrão}` | `env`, `env_vars` | `{env:VAR}`, `{file:caminho}` |
| **Windows nativo: home** | `%USERPROFILE%\.claude`; troca com `CLAUDE_CONFIG_DIR` | `%USERPROFILE%\.codex`; troca com `CODEX_HOME` | `%USERPROFILE%\.config\opencode` (pelo código; NV em execução); troca com `OPENCODE_CONFIG_DIR` |
| **WSL: enxerga o lado Windows?** | N (instalação Linux, home Linux) | N por padrão; S com `CODEX_HOME=/mnt/c/...` (doc) | N ("config and sessions are stored within the WSL environment") |

## 1. Instruções e contrato

### 1.1 Claude Code

- **Onde carrega.** Usuário: `~/.claude/CLAUDE.md`. Projeto: `./CLAUDE.md` ou `./.claude/CLAUDE.md`. Pastas
  acima: *"Claude Code loads `CLAUDE.md` and `CLAUDE.local.md` from your current working directory and every
  directory above it."* ([memory](https://code.claude.com/docs/en/memory))
- **AGENTS.md (novo, v2.1.277+).** *"Claude Code can read `AGENTS.md` as your project instructions"*. O padrão é
  `claude-md-or-agents-md`: um `AGENTS.md` com um `CLAUDE.md` *"in your working directory or above it"* resulta
  em *"Your `CLAUDE.md` files only"*. O `~/.claude/CLAUDE.md` **não conta** para essa troca: *"Don't count, and
  keep loading alongside `AGENTS.md`: your `~/.claude/CLAUDE.md`…"*. Não é lido: *"`AGENTS.local.md`,
  `AGENTS.override.md`, or anything under a `.agents/` directory"*. Para ler os dois, existe o valor
  `claude-md-and-agents-md`, configurado em `pluginConfigs."agents-md@builtin"` no `~/.claude/settings.json`
  (ignorado em settings de projeto). ([memory](https://code.claude.com/docs/en/memory#agents-md))
  A documentação não menciona um `AGENTS.md` de usuário (em `~/.claude`), portanto **não verificado**.
- **Imports.** *"CLAUDE.md files can import additional files using `@path/to/import` syntax."* *"Both relative and
  absolute paths are allowed. Relative paths resolve relative to the file containing the import, not the
  working directory. … maximum depth of four hops."* Caminhos com espaço pedem `\` antes de cada espaço. Imports
  "externos" num CLAUDE.md **de projeto** abrem um diálogo de aprovação. Já os de escopo de usuário
  (`~/.claude/CLAUDE.md`, `~/.claude/rules/`) *"loads their imports without the dialog"*.
  ([memory](https://code.claude.com/docs/en/memory#import-additional-files))
  Os exemplos usam `@~/...` e caminhos POSIX. A forma exata de um absoluto com letra de drive no Windows
  (`@C:/...` ou `@C:\...`) é **não verificada**.
- **Regras compartilhadas.** `~/.claude/rules/` vale para todos os projetos. `.claude/rules/` aceita symlink,
  mas um symlink que aponta para fora da pasta de trabalho é tratado como import externo. Symlinks para caminho
  de rede (UNC) não carregam, e *"`\\wsl$` paths don't count as network paths."*
  ([memory](https://code.claude.com/docs/en/memory#share-rules-across-projects-with-symlinks))
- **`--add-dir`.** Não carrega CLAUDE.md, a não ser com `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1`. Mesmo
  assim, *"Their `AGENTS.md` doesn't load"*. ([memory](https://code.claude.com/docs/en/memory#load-from-additional-directories))
- **Outra via:** `--append-system-prompt-file` *"Load additional system prompt text from a file and append to
  the default prompt"* ([cli-reference](https://code.claude.com/docs/en/cli-reference)). Exige alterar o comando
  de lançamento.
- **Tamanho.** *"target under 200 lines per CLAUDE.md file"*. *"Imports … don't reduce its context cost"*.
  *"Claude Code loads a CLAUDE.md file of up to 4 MiB in full and skips a larger file."*
  ([memory](https://code.claude.com/docs/en/memory))

### 1.2 Codex CLI

> As URLs `developers.openai.com/codex/...` (citadas pelo `docs/*.md` de github.com/openai/codex) hoje
> redirecionam para `learn.chatgpt.com/docs/...`. As citações abaixo vêm do destino do redirecionamento.

- **Descoberta.** *"Global scope: In your Codex home directory (defaults to `~/.codex`, unless you set
  `CODEX_HOME`), Codex reads `AGENTS.override.md` if it exists. Otherwise, Codex reads `AGENTS.md`. Codex uses
  only the first non-empty file at this level."* *"Project scope: Starting at the project root (typically the
  Git root), Codex walks down to your current working directory. If Codex cannot find a project root, it only
  checks the current directory."* ([agents-md](https://learn.chatgpt.com/docs/agent-configuration/agents-md))
- **Limite.** *"stops adding files once the combined size reaches the limit defined by `project_doc_max_bytes`
  (32 KiB by default)"*, ajustável no `config.toml`. (mesma página)
- **Fora do projeto.** A documentação não descreve sintaxe de import em `AGENTS.md` (ausência = **não
  verificado**). As chaves que existem são:
  - `model_instructions_file`: *"Replacement for built-in instructions instead of `AGENTS.md`."* Substitui o
    prompt embutido, o que não serve para um contrato.
  - `developer_instructions`: *"Additional developer instructions injected into the session (optional)."*
    É texto inline.
  - `project_doc_fallback_filenames`: muda só o nome do arquivo procurado.

  ([config-reference](https://learn.chatgpt.com/docs/config-file/config-reference))
- Se `~/.codex/AGENTS.md` pode ser symlink ou junction para um arquivo do hub: **não verificado**.

### 1.3 OpenCode

> O repositório oficial `github.com/sst/opencode` responde 301 para `github.com/anomalyco/opencode` (branch
> padrão `dev`). A versão estável é a v1 (último release v1.18.34, 30/09/2026). Existe também uma **V2**
> documentada em `opencode.ai/v2/docs`, com comportamento diferente. Qual versão está instalada nas máquinas é
> **não verificado**.

- **v1, arquivos.** Projeto: `AGENTS.md` (*"Local files by traversing up from the current directory"*).
  Global: *"`~/.config/opencode/AGENTS.md`"*. Compatibilidade com Claude Code: `CLAUDE.md` do projeto *"used if
  no `AGENTS.md` exists"* e `~/.claude/CLAUDE.md` *"used if no `~/.config/opencode/AGENTS.md` exists"*.
  ([rules](https://opencode.ai/docs/rules/))
- **v1, `instructions`.** *"You can specify custom instruction files in your `opencode.json` or the global
  `~/.config/opencode/opencode.json`"*. Aceita glob e URL remota (*"fetched with a 5 second timeout"*).
  ([rules](https://opencode.ai/docs/rules/)) Caminho absoluto: o código trata `~/` e `path.isAbsolute`
  (`packages/opencode/src/session/instruction.ts`, linhas 136–149:
  `raw.startsWith("~/") ? path.join(global.home, …)` e `path.isAbsolute(instruction) ? fs.glob(…)`).
- **v1, sem import.** *"opencode doesn't automatically parse file references in `AGENTS.md`"*
  ([rules](https://opencode.ai/docs/rules/)). Portanto, se o OpenCode cair no `~/.claude/CLAUDE.md`, as
  linhas `@...` dele **não** são expandidas.
- **v1, `OPENCODE_CONFIG_DIR`.** No código, a pasta global vira `Flag.OPENCODE_CONFIG_DIR ?? Path.config`
  (`packages/core/src/global.ts`, linha 64). Assim, o `AGENTS.md` global passa a ser lido dessa pasta. Há uma
  issue aberta sobre exatamente isso: *"OPENCODE_CONFIG_DIR overrides global AGENTS.md path instead of adding to
  it"* ([#28658](https://github.com/anomalyco/opencode/issues/28658)).
- **V2.** *"OpenCode V2 recognizes AGENTS.md only. It does not use CLAUDE.md as a fallback."* *"The V2 config
  schema accepts an `instructions` array, but V2 does not currently resolve its files, glob patterns, or URLs."*
  ([v2 instructions](https://opencode.ai/v2/docs/instructions/))
- **Limite de tamanho:** nenhum encontrado na documentação (**não verificado**).

## 2. Skills

### 2.1 Claude Code

- **Locais.** Pessoal: `~/.claude/skills/<skill-name>/SKILL.md`. Projeto: `.claude/skills/...`. Também:
  aninhadas, pastas de `--add-dir`, plugins (`/plugin-name:skill-name`) e enterprise. As de projeto carregam
  *"in the directory where you start it and in every parent directory up to the repository root"*.
  ([skills](https://code.claude.com/docs/en/skills))
- **Symlink.** *"a `<skill-name>` entry in the enterprise, personal, or project location can be a symlink to a
  directory elsewhere on disk. Claude Code reads `SKILL.md` from the target and loads the skill once even if
  several locations point at the same target."* (mesma página)
- **Junction:** não aparece na página de skills.
  - **Observação local** (leitura, nesta sessão): `~/.claude/skills` tem 38 entradas do tipo `Junction` que
    apontam para `~/.agents/skills/<nome>`. Várias delas (`grilling`, `matt-code-review`, `tdd`…) aparecem
    na lista de skills disponíveis desta sessão do Claude Code. Na prática, junction funciona aqui. Não é
    garantia documentada.
  - Issue oficial relacionada: [anthropics/claude-code#38051](https://github.com/anthropics/claude-code/issues/38051)
    (*"User-level skills not loaded when ~/.claude/skills is a symlink"*, fechada como *completed* em 24/03/2026).
- **Não lê `~/.agents/skills`.** A página de skills não lista essa pasta. A página de memória diz que
  *"anything under a `.agents/` directory"* não é lido (essa frase trata de AGENTS.md).
- **Apontar outra pasta:**
  - `--add-dir` carrega o `.claude/skills/` da pasta adicionada. Já *"The `permissions.additionalDirectories`
    setting … grants file access only"*.
  - Plugins: `CLAUDE_CODE_PLUGIN_DIRS` (*"Plugin directories to load for the session … Separate multiple paths
    with `:` on Unix or `;` on Windows … Requires Claude Code v2.1.280 or later"*,
    [env-vars](https://code.claude.com/docs/en/env-vars)).
  - Um marketplace local cujos plugins *"load in place from its path inside the marketplace folder"*
    ([plugins/loading](https://code.claude.com/docs/en/plugins/loading)).

  Um plugin pode levar skills **e** MCP juntos: *"A Claude Code plugin is a directory of skills, agents, hooks,
  MCP servers"* ([plugins](https://code.claude.com/docs/en/plugins)).
- **Pasta do usuário inteira:** `CLAUDE_CONFIG_DIR` muda o `~/.claude` todo (*"All settings, session history,
  and plugins are stored under this path"*, [env-vars](https://code.claude.com/docs/en/env-vars)).
- **Padrão aberto:** *"Claude Code skills follow the [Agent Skills](https://agentskills.io) open standard"*
  ([skills](https://code.claude.com/docs/en/skills)).

### 2.2 Codex CLI

- **Locais.** *"For repositories, Codex scans `.agents/skills` in every directory from your current working
  directory up to the repository root."* USER: *"`$HOME/.agents/skills`"*. ADMIN: `/etc/codex/skills`. SYSTEM:
  embutidas. ([skills](https://learn.chatgpt.com/docs/build-skills))
- **Código** (`codex-rs/ext/skills/src/host_roots.rs`, linhas 96–107): a raiz do usuário é
  `home_dir().join(".agents").join("skills")`. Também lê a raiz obsoleta: *"Deprecated user skills location
  (`$CODEX_HOME/skills`), kept for backward compatibility."* O `home_dir` vem da crate `dirs`. Que no Windows
  isso seja `%USERPROFILE%` é **não verificado** aqui.
- **Symlink.** *"Codex supports symlinked skill folders and follows the symlink target when scanning these
  locations."* ([skills](https://learn.chatgpt.com/docs/build-skills)) No código: `SkillScope::User |
  SkillScope::Repo | SkillScope::Admin => DirectorySymlinkPolicy::Follow`
  (`codex-rs/ext/skills/src/loader/host.rs`, linhas 164–166).
- **Junction no Windows:** **não verificado**. A issue oficial [openai/codex#8400](https://github.com/openai/codex/issues/8400)
  (*"skills not detected on Windows with symlink or junctions"*) foi fechada como *duplicate*. A
  [#11314](https://github.com/openai/codex/issues/11314) (`.agents/skills` como symlink) foi fechada como
  *not_planned*.
- **Config.** `[[skills.config]]` com `path` e `enabled` serve para *"disable a skill without deleting it"*.
  Não está documentado como forma de **adicionar** uma pasta (**não verificado**).
  `skills.max_context_tokens`: *"Defaults to 2% of the model's context window"*
  ([config-reference](https://learn.chatgpt.com/docs/config-file/config-reference)).

### 2.3 OpenCode

- **v1, locais.** *"Global config: `~/.config/opencode/skills/<name>/SKILL.md`"*, *"Global Claude-compatible:
  `~/.claude/skills/<name>/SKILL.md`"*, *"Global agent-compatible: `~/.agents/skills/<name>/SKILL.md"`*, mais os
  equivalentes de projeto, *"walks up from your current working directory until it reaches the git worktree"*.
  ([skills](https://opencode.ai/docs/skills/))
- **v1, pasta extra.** O schema oficial (`https://opencode.ai/config.json`) tem `skills.paths`: *"Additional
  paths to skill folders"*, e `skills.urls`. No código (`packages/opencode/src/skill/index.ts`, linhas 211–220),
  um caminho com `~/` é expandido e um absoluto é usado como está. A varredura usa `symlink: true` (linha 154).
  Desliga a leitura das pastas do Claude: `OPENCODE_DISABLE_CLAUDE_CODE_SKILLS=1`
  ([rules](https://opencode.ai/docs/rules/)).
- **V2.** O mesmo conjunto de pastas, mais `"skills": [ "./team-skills", "~/shared/…", "/opt/…", "https://…" ]`.
  Um caminho relativo é resolvido *"From the active OpenCode working directory, not the config file"*
  ([v2 skills](https://opencode.ai/v2/docs/skills/)).
- **Windows:** a issue oficial [anomalyco/opencode#17007](https://github.com/anomalyco/opencode/issues/17007)
  (*"~/.agents/skills/ path not resolved on Windows"*) foi fechada como *not_planned* em 04/07/2026. O estado
  atual é **não verificado**.

### 2.4 Convenção compartilhada

`~/.agents/skills` é lido pelo Codex (USER) e pelo OpenCode (global). `~/.claude/skills` é lido pelo Claude Code
e pelo OpenCode. **Não existe uma pasta lida pelos três.** O formato `SKILL.md` com frontmatter `name` e
`description` é o padrão Agent Skills nos três. O OpenCode reconhece só `name`, `description`, `license`,
`compatibility` e `metadata` ([skills](https://opencode.ai/docs/skills/)).

## 3. MCP

### 3.1 Claude Code

- **Escopos.** *"Local | Current project only | … `~/.claude.json`"*, *"Project | … `.mcp.json` in project
  root"*, *"User | All your projects | … `~/.claude.json`"*. O `.mcp.json` de projeto pede aprovação em sessão
  interativa. ([mcp](https://code.claude.com/docs/en/mcp#mcp-installation-scopes))
- **Transportes:** `--transport http`, `sse` e stdio (`claude mcp add … -- <comando>`), além de `ws` via JSON.
  (mesma página)
- **Variáveis.** *"Claude Code supports environment variable expansion in `.mcp.json` files, allowing teams to
  share configurations while maintaining flexibility for machine-specific paths"*, com `${VAR}` e
  `${VAR:-default}` em `command`, `args`, `env`, `url` e `headers`. (mesma página)
- **Arquivo avulso:** `--mcp-config` *"Load MCP servers from JSON files or strings"*
  ([cli-reference](https://code.claude.com/docs/en/cli-reference)). Também é possível pelo plugin
  (`.mcp.json` na raiz do plugin), que carrega com `CLAUDE_CODE_PLUGIN_DIRS`.
- **Entre máquinas:** o `~/.claude.json` guarda estado da máquina (aprovações por projeto, por exemplo) e não
  serve para sincronizar inteiro. Isto é uma inferência a partir da doc, que diz que as escolhas são gravadas
  *"per project in `~/.claude.json"`*.

### 3.2 Codex CLI

- *"Codex stores MCP configuration in `config.toml` … By default this is `~/.codex/config.toml`, but you can
  also scope MCP servers to a project with `.codex/config.toml` (trusted projects only)."*
  ([mcp](https://learn.chatgpt.com/docs/mcp))
- **Transportes:** *"STDIO servers"* e *"Streamable HTTP servers"*. Chaves: `mcp_servers.<id>.command`, `args`,
  `env`, `env_vars`, `cwd` e `url` ([config-reference](https://learn.chatgpt.com/docs/config-file/config-reference)).
- **Precedência:** flags e `--config`, depois projeto (`.codex/config.toml`, só em projeto confiável), depois
  `--profile` (`~/.codex/<nome>.config.toml`), depois usuário (`~/.codex/config.toml`)
  ([config-basic](https://learn.chatgpt.com/docs/config-file/config-basic)).
- **Entre máquinas:** a documentação não menciona include de outro arquivo TOML (**não verificado**). O
  `config.toml` real desta máquina mistura tabelas `[projects.'<caminho>']` (confiança por pasta) com
  `[mcp_servers.*]` (observação local), então não serve para copiar inteiro entre máquinas.

### 3.3 OpenCode

- `mcp` no `opencode.json`, com `"type": "local"` (`command` como array, `environment`) ou `"type": "remote"`
  (`url`, `headers`, OAuth automático) ([mcp-servers](https://opencode.ai/docs/mcp-servers/)).
- **Arquivo avulso:** *"Specify a custom config file path using the `OPENCODE_CONFIG` environment variable"*.
  Ele é *"loaded between global and project configs"* ([config](https://opencode.ai/docs/config/)).
- **Variáveis:** *"Use `{env:VARIABLE_NAME}`"*, *"Use `{file:path/to/file}`"*. Os caminhos podem ser
  *"absolute paths starting with `/` or `~`"* (mesma página).

### 3.4 Observação comum

Os três aceitam stdio e HTTP. Com stdio, cada harness sobe o próprio processo do servidor. Com HTTP, um único
processo atende os três, mas alguém tem de mantê-lo no ar. O desenho disso não foi pesquisado aqui.

## 4. Windows × WSL

- **Claude Code.**
  - *"You can run Claude Code natively on Windows or inside WSL."* No WSL: *"You install and launch `claude`
    inside the WSL terminal"* ([setup](https://code.claude.com/docs/en/setup)).
  - No Windows: *"`~/.claude` means `%USERPROFILE%\.claude`"* ([settings](https://code.claude.com/docs/en/settings)).
    A política gerenciada também muda de lugar: *"Linux and WSL: `/etc/claude-code/CLAUDE.md`"* contra
    `C:\Program Files\ClaudeCode\CLAUDE.md` ([memory](https://code.claude.com/docs/en/memory)).
  - A documentação não diz que a instalação do WSL leia o `%USERPROFILE%\.claude`. Inferência: são duas
    configurações separadas.
  - Um Claude Code do Windows pode trabalhar num hub dentro do WSL: *"Mapped drive letters and `\\wsl$` paths
    don't count as network paths"*. Já *"Local paths that reach a network location through a symbolic link or
    junction"* são recusados ([errors](https://code.claude.com/docs/en/errors#working-directory-is-a-network-path)).
- **Codex.**
  - *"The Windows app uses the same Codex home directory as native Codex on Windows: `%USERPROFILE%\.codex`."*
  - *"If you also run the Codex CLI inside WSL, the CLI uses the Linux home directory by default, so it doesn't
    automatically share configuration, cached auth, or session history"*. A solução documentada é sincronizar
    os dois ou usar `export CODEX_HOME=/mnt/c/Users/<windows-user>/.codex`
    ([windows-app](https://learn.chatgpt.com/docs/windows/windows-app)).
  - Desempenho: *"Working in Windows-mounted paths like `/mnt/c/...` can be slower … fewer symlink and
    permission issues"* se o projeto ficar no home Linux ([wsl](https://learn.chatgpt.com/docs/windows/wsl)).
- **OpenCode.**
  - Recomenda WSL. *"Your OpenCode config and sessions are stored within the WSL environment at
    `~/.local/share/opencode/`"* ([windows-wsl](https://opencode.ai/docs/windows-wsl/)).
  - No Windows nativo, a pasta global vem de `xdgConfig`, que é `XDG_CONFIG_HOME || path.join(os.homedir(),
    '.config')` (código de `sindresorhus/xdg-basedir`, `index.js`, usado em `packages/core/src/global.ts`).
    Isso dá `%USERPROFILE%\.config\opencode` (**inferido do código, não verificado em execução**).
  - O arquivo gerenciado no Windows fica em `%ProgramData%\opencode` ([config](https://opencode.ai/docs/config/)).
- **Maestri:** *"Skills are installed per distribution, under Settings > Agents > Skills."* *"Set the working
  directory as it exists inside the distribution … Maestri keeps these paths in their Linux form"*
  ([environments](https://www.themaestri.app/en/docs/environments)).

## 5. Maestri

Fonte primária: a documentação oficial em https://www.themaestri.app/en/docs/, mais os arquivos locais de
instalação, lidos sem alterar nada.

- **Pasta de trabalho.** *"Working directory — The root folder for this project. New terminals will open here
  by default."* ([workspaces](https://www.themaestri.app/en/docs/workspaces)) No ambiente local: *"Maestri starts
  the configured shell directly on this machine in the selected working directory."*
  ([environments](https://www.themaestri.app/en/docs/environments)) O CLI aceita `--dir` para começar um
  recruta noutra pasta (skill oficial `maestri-manager`, instalada em `~/.claude/skills/maestri-manager/SKILL.md`).
- **Comando do agente:** vem do preset. Nas preferências locais (`%USERPROFILE%\.maestri\preferences.json`,
  `agentPresets`) os presets são `claude`, `codex --no-daemon`, `opencode`, `agy` e um shell (observação local).
- **Papéis (roles), a injeção de instruções:**
  - *"When a role is assigned, Maestri automatically injects those instructions when the agent starts"*.
  - *"Roles work by starting the agent in a project subdirectory with its own CLAUDE.md / AGENTS.md"*, com um
    `role.json` ao lado ([terminals](https://www.themaestri.app/en/docs/terminals)).
  - Caminho: *"`<project>/.maestri/roles/<role-id>/`"* ([environments](https://www.themaestri.app/en/docs/environments)).
  - Localmente, as pastas de papel do workspace `maestri` têm `AGENTS.md` e `CLAUDE.md` do mesmo tamanho, mais o
    `role.json`. O `config.toml` do Codex tem entradas de confiança para essas pastas (observação local).
- **Instruções do workspace.** *"From the workspace edit screen, you can manage CLAUDE.md and AGENTS.md
  files … Maestri includes an option to keep both files in sync automatically."*
  ([workspaces](https://www.themaestri.app/en/docs/workspaces)) A justificativa da página (*"Claude Code only
  understands CLAUDE.md"*) **está desatualizada**: o Claude Code lê `AGENTS.md` desde a v2.1.277 (§1.1).
- **Variáveis de ambiente.**
  - Documentadas para ambientes remotos: *"MAESTRI_TERMINAL_ID … MAESTRI_HOST … MAESTRI_TOKEN … MAESTRI_CLI"*,
    e *"Overrides cannot replace HOME, PATH, or any MAESTRI_ value"*
    ([environments](https://www.themaestri.app/en/docs/environments)).
  - Para floors: `$MAESTRI_FLOOR_NAME`, `$MAESTRI_BRANCH_NAME`, `$MAESTRI_FLOOR_PATH`, `$MAESTRI_ROOT_PATH`
    ([floors](https://www.themaestri.app/en/docs/floors)).
  - Num terminal local, este processo herdou `MAESTRI_CLI`, `MAESTRI_DATA_DIR`, `MAESTRI_PIPE`,
    `MAESTRI_TERMINAL_ID` e `MAESTRI_WORKSPACE_ID` (observação local; valores omitidos).
- **Skills do Maestri.** *"When two terminals are connected, Maestri installs a Maestri Agent Skill in each one."*
  ([connections](https://www.themaestri.app/en/docs/connections))
  - O pacote do app (`%LOCALAPPDATA%\Programs\Maestri\resources\app.asar`) define as raízes padrão de skill
    (`skillBases`): `.claude/skills` ("Claude Code"), `.agents/skills` ("Agent Skills"), `.hermes/skills` e
    outras.
  - Localmente, as skills `maestri*` existem como **pastas reais** (não links) em `~/.claude/skills` e
    `~/.agents/skills` (observação local).
- **Flags de lançamento:** não aparece `add-dir`, `append-system-prompt` nem `model_instructions_file` no
  `app.asar` (busca textual com 0 ocorrências). Isso sugere que o Maestri **não** injeta instruções por flag, só
  pela pasta do papel. O bundle é minificado, então isso fica **não verificado**.

### Consequências para o hub (análise, não decisão)

- **Claude Code com papel:** a pasta de trabalho é `…/.maestri/roles/<id>/`, que tem `CLAUDE.md`. Pela regra
  padrão, um `AGENTS.md` do workspace (acima) **não é lido**. Os `CLAUDE.md` acima continuam sendo lidos.
  O `~/.claude/CLAUDE.md` carrega sempre.
- **Codex com papel:** se o workspace for repositório git, o Codex lê da raiz git até a pasta do papel. Se não
  for, *"it only checks the current directory"*, ou seja, só o `AGENTS.md` do papel mais o global.
- **OpenCode com papel:** sobe a partir da pasta do papel (v1). Como acha `AGENTS.md` ali, deixa de procurar
  `CLAUDE.md`.
- Nos três casos, a única camada que sobrevive a qualquer pasta, papel ou workspace é a **global do usuário**.

## Lacunas e não verificado

- **Junction:**
  - Nenhum dos três documenta junction. No Claude Code funciona nesta máquina (observado).
  - No Codex e no OpenCode, Windows nativo: **não verificado** (há issues fechadas sem correção documentada).
  - Para `~/.codex/AGENTS.md` ou `~/.config/opencode/AGENTS.md` como link de *arquivo*: **não verificado**.
    No Windows, symlink de arquivo exige privilégio ou Modo de Desenvolvedor, e junction só existe para pastas.
    Essa regra do Windows também não foi conferida em fonte Microsoft nesta pesquisa.
- **Imports e caminhos:**
  - Sintaxe de `@import` com letra de drive no Windows (Claude Code): **não verificado**.
  - Codex com import em `AGENTS.md` ou include de outro `config.toml`: não documentado, **não verificado**.
- **OpenCode:**
  - Qual versão (v1 ou V2) está instalada nas máquinas: **não verificado**. Na V2 o `instructions` não funciona.
  - Pasta global no Windows nativo (`%USERPROFILE%\.config\opencode`): inferida do código, **não verificada em
    execução**.
  - Se `skills.paths` (v1) e `OPENCODE_CONFIG_DIR` somam ou substituem as pastas globais: lido no código
    (`skill/index.ts` soma; `global.ts` substitui a pasta global do `AGENTS.md`). Não testado.
- **Claude Code:**
  - Se o `.mcp.json` de projeto é procurado também nas pastas acima da pasta de trabalho (relevante para papéis
    do Maestri): **não verificado**.
  - Se existe `AGENTS.md` de nível de usuário: não documentado, **não verificado**.
- **Maestri:**
  - Se o Maestri passa alguma flag ou variável além das observadas, e como trata o OpenCode e o Codex num
    papel: **não verificado**. A documentação descreve só o mecanismo de pasta.
  - Se o "sync CLAUDE.md ↔ AGENTS.md" do workspace grava em disco na pasta do workspace: **não verificado**.
- **Fora do escopo:** limites de tamanho de skills (catálogo) por harness. Só os do Claude Code (1.536
  caracteres por descrição) e do Codex (2% do contexto) foram vistos.

## Consultas

**Buscas na web (WebSearch):**
1. `Maestri app canvas AI agents terminals documentation roles workspace`
2. `Codex CLI skills ~/.agents/skills symlink Windows junction` (domínios: github.com, developers.openai.com, learn.chatgpt.com)
3. `Claude Code skills directory Windows junction symlink not loading` (domínios: github.com, code.claude.com)
4. `opencode "skills" "paths" config AGENTS.md instructions absolute path Windows` (domínios: opencode.ai, github.com)

**Páginas lidas na íntegra (curl do Markdown ou HTML, com trechos conferidos por grep):**
- Claude Code: `code.claude.com/docs/en/{memory,skills,mcp,settings,plugins,plugins/loading,setup,env-vars,cli-reference,errors,desktop-wsl,third-party-integrations}.md`
- Codex: `developers.openai.com/codex/{guides/agents-md,skills,mcp,config-reference,config-basic,config-advanced,windows}.md`
  (redirecionam para `learn.chatgpt.com/docs/...`), `learn.chatgpt.com/docs/windows/{wsl,windows-app}.md`,
  `learn.chatgpt.com/llms.txt`, `raw.githubusercontent.com/openai/codex/main/docs/{skills,agents_md,config}.md`
- Código do Codex: `codex-rs/ext/skills/src/host_roots.rs`, `codex-rs/ext/skills/src/loader/{discovery,host}.rs` (branch `main`)
- OpenCode: `raw.githubusercontent.com/anomalyco/opencode/dev/packages/web/src/content/docs/{rules,skills,mcp-servers,config,windows-wsl}.mdx`,
  `opencode.ai/config.json` (schema), `opencode.ai/v2/docs/{instructions,skills}/`, `opencode.ai/v2/docs/`
- Código do OpenCode: `packages/opencode/src/skill/index.ts`, `packages/opencode/src/session/instruction.ts`,
  `packages/core/src/global.ts` (branch `dev`); dependência `sindresorhus/xdg-basedir/index.js`
- Maestri: `www.themaestri.app/en/docs/{intro,terminals,workspaces,environments,maestro,floors,troubleshooting,connections}`
- API do GitHub (estado): `repos/sst/opencode` (301 → `anomalyco/opencode`), releases mais recentes do
  OpenCode, issues `openai/codex#8400`, `#11314`, `anthropics/claude-code#38051`, `anomalyco/opencode#17007`,
  `#28658`

**Leitura local (sem alterar nada):**
- `%USERPROFILE%\.maestri\` (listagem; chaves de `preferences.json`)
- `%LOCALAPPDATA%\Programs\Maestri\resources\` (listagem; busca textual em `app.asar`)
- `~/.claude/skills/maestri*/SKILL.md`
- tipo de link das entradas de `~/.claude/skills` e `~/.agents/skills`
- `C:\Projetos\maestri\.maestri\roles\` (listagem; chaves de um `role.json`)
- busca por `maestri` e `mcp_servers` em `~/.codex/config.toml` e `~/.claude.json` (só nomes de chave)
- variáveis `MAESTRI_*` do processo
