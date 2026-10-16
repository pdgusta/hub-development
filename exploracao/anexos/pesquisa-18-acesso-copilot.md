---
title: Pesquisa 18, acesso do GitHub Copilot ao hub (VS Code e Copilot CLI; contrato, skills, MCP, Windows, Maestri)
data: 2026-10-01
origem: subagente de pesquisa (Claude Code), ticket "Acesso dos agentes: Copilot"
aviso: saída de modelo. Cada afirmação traz a fonte primária (docs oficiais em docs.github.com e code.visualstudio.com, changelog e issues do repositório oficial github/copilot-cli, docs e changelog do Maestri, ou arquivo local lido), com citação curta conferida no texto da página. Nada foi instalado, testado nem configurado. O que não foi conferido na fonte está marcado como **não verificado**.
---

# Acesso do GitHub Copilot ao hub: levantamento de 01/10/2026

## Resumo (uma tela)

**Pergunta:** como o GitHub Copilot, no modo agente do VS Code e no Copilot CLI, avulso ou dentro do Maestri,
carrega o contrato do hub, acha as skills do hub e tem o MCP do hub, numa pasta compartilhada no Windows?

**Resposta curta:** os dois Copilots **convergiram para o mesmo runtime e a mesma pasta de usuário**,
`~/.copilot` (troca-se com `COPILOT_HOME`). No VS Code, o agente "Copilot" agora roda no **Agent Host** com o
runtime do Copilot CLI e lê `~/.copilot`. O agente antigo do VS Code ("Local") continua existindo, com regras
próprias, mas está marcado para remoção. Portanto, o hub entra no Copilot quase todo por um único lugar.

1. **Contrato.** Camada global: `~/.copilot/copilot-instructions.md` e `~/.copilot/instructions/**/*.instructions.md`
   (CLI e Agent Host do VS Code). Para apontar para fora do projeto existem duas vias documentadas:
   - **`COPILOT_CUSTOM_INSTRUCTIONS_DIRS`** (CLI): diretórios extras com `AGENTS.md` e `*.instructions.md`. Uma
     issue aberta relata que, desde a v1.0.66, o `AGENTS.md` dessa pasta deixou de entrar como instrução global.
   - **`@caminho`** dentro de `AGENTS.md`, `CLAUDE.md` e `copilot-instructions.md` (desde a v1.0.66). A doc
     **se contradiz** sobre caminho absoluto: a página de how-to diz que absoluto e `~/` *"are not loaded"*; a
     referência diz que o caminho pode ser *"relative … or absolute"*.

   O CLI lê **ao mesmo tempo** `AGENTS.md`, `CLAUDE.md`, `GEMINI.md` e `.github/copilot-instructions.md` (raiz
   git e pasta atual), soma tudo e descarta duplicatas idênticas. Não há ordem de precedência. Não há limite de
   tamanho documentado.
2. **Skills.** Pessoais: `~/.copilot/skills` e **`~/.agents/skills`**. É a mesma pasta lida pelo Codex e pelo
   OpenCode (pesquisa 13). Pastas extras: `COPILOT_SKILLS_DIRS`, a chave `skillDirectories` do `settings.json` ou
   `copilot skill add <pasta>` (registra a pasta sem copiar). O CLI **não** lista `~/.claude/skills` como pasta
   pessoal (só `.claude/skills` de projeto). A doc do VS Code lista as três pastas pessoais. Symlink de pasta de
   skill funciona pelo changelog (v1.0.62); **junction não é documentada**. Atenção: com `COPILOT_HOME`
   definido, o CLI **para de ler `~/.agents/skills`** (changelog v1.0.66).
3. **MCP.** CLI: `~/.copilot/mcp-config.json` (`mcpServers`), mais `.mcp.json` / `.github/mcp.json` do projeto,
   subindo da pasta atual até a raiz git, só em pasta confiável. Transportes: stdio, HTTP streamable e SSE.
   Para compartilhar: `--additional-mcp-config @<arquivo>` (por sessão), plugin (`--plugin-dir` ou marketplace
   local, que carrega "ao vivo" da pasta) ou `COPILOT_HOME`. VS Code: `.vscode/mcp.json` e `mcp.json` do perfil
   (formato `servers`), e o formato portátil `.mcp.json` / `~/.copilot/mcp-config.json`, que o Agent Host lê
   direto. O CLI **não lê** `.vscode/mcp.json` desde a v1.0.22.
4. **Maestri.** A doc oficial não cita o Copilot entre os agentes, e o app instalado não tem tipo de agente
   "copilot" (tem `claude_code`, `codex`, `gemini_cli`, `antigravity_cli`, `open_code`, `custom` e
   `generic_shell`). O changelog oficial menciona *"Improved compatibility with Ink-based terminals like GitHub
   Copilot CLI"*. Portanto, o Copilot CLI entra como **preset personalizado** com o comando `copilot`. Com papel,
   o Maestri o inicia em `<projeto>/.maestri/roles/<id>/`. Ali, pela doc do CLI, ele leria o `AGENTS.md` e o
   `CLAUDE.md` do papel **e também** os da raiz git do projeto (diferente do Claude Code), além da camada global.
   O VS Code não roda dentro do Maestri, e a doc do Maestri não fala dele.
5. **Windows.** Home de config: `C:\Users\<user>\.copilot`. Cache: `%LOCALAPPDATA%\copilot`. O CLI exige
   PowerShell 6+ e prefere `pwsh` 7. Há bugs abertos de instrução carregada em dobro no Windows (caixa da letra
   de drive no Agent Host do VS Code).

**Leitura para o ticket:**
- O hub pode entrar no Copilot (CLI e VS Code/Agent Host) pela pasta `~/.copilot` de cada máquina, sem
  `COPILOT_HOME`, para não perder `~/.agents/skills`.
- As skills do hub já ficam visíveis ao Copilot pela convenção `~/.agents/skills`, a mesma do Codex e do
  OpenCode. Para o contrato, a via menos frágil é **não verificada**: as alternativas são
  `COPILOT_CUSTOM_INSTRUCTIONS_DIRS` (com regressão relatada), `@import` absoluto (doc contraditória) ou cópia
  gerada em `~/.copilot/copilot-instructions.md`.

## Tabela comparativa

Legenda: S = sim, P = parcial, N = não, NV = não verificado. "Local" = agente Local do VS Code (extension
host, legado). "Agent Host" = sessão com o harness Copilot no VS Code.

| | VS Code, agente Local | VS Code, harness Copilot (Agent Host) | Copilot CLI (1.0.x) |
|---|---|---|---|
| **Runtime** | extension host do VS Code | SDK do Copilot, *"agent runtime also used by Copilot CLI"* | runtime próprio |
| **Contrato global** | instruções no perfil do VS Code; `~/.claude/CLAUDE.md` | `~/.copilot/copilot-instructions.md`, `~/.copilot/instructions`, `~/.claude/rules` | `~/.copilot/copilot-instructions.md`, `~/.copilot/instructions/**/*.instructions.md` |
| **Contrato do projeto** | `.github/copilot-instructions.md`, `AGENTS.md`, `CLAUDE.md`, `.github/instructions`, `.claude/rules` | `.github/copilot-instructions.md` ou `AGENTS.md`; `.github/instructions` | `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `.github/copilot-instructions.md`, `.github/instructions`, `.claude/rules` (raiz git e pasta atual; todos somados) |
| **Pasta extra de instruções** | `chat.instructionsFilesLocations` (obsoleta) | NV | `COPILOT_CUSTOM_INSTRUCTIONS_DIRS` (env) |
| **Import de arquivo** | links Markdown (`chat.includeReferencedInstructions`, desligado por padrão) | NV | `@caminho` em `AGENTS.md`, `CLAUDE.md`, `copilot-instructions.md`; absoluto: **doc contraditória** |
| **Limite de tamanho** | nenhum documentado | nenhum documentado | nenhum documentado (*"size guards"* sem número) |
| **Skills: pessoais** | `~/.copilot/skills`, `~/.claude/skills`, `~/.agents/skills` (doc VS Code) | idem (doc VS Code); NV se `~/.agents/skills` vale com o `COPILOT_HOME` que o host define | `~/.copilot/skills`, `~/.agents/skills` |
| **Skills: pasta extra** | `chat.agentSkillsLocations` (obsoleta) | NV | `COPILOT_SKILLS_DIRS`, `skillDirectories`, `copilot skill add <pasta>`, `--add-dir` |
| **Skills por symlink** | NV | NV | S (changelog 1.0.62 e 1.0.68; issue #1021 fechada) |
| **Skills por junction** | NV | NV | NV (issue #3264 pede documentação; aberta) |
| **MCP: usuário** | `mcp.json` do perfil (`servers`); `~/.copilot/mcp-config.json` | `~/.copilot/mcp-config.json` (lê direto) + o que o VS Code repassa | `~/.copilot/mcp-config.json` |
| **MCP: projeto** | `.vscode/mcp.json` (`servers`), `.mcp.json` (`mcpServers`) | `.mcp.json` (lê direto); `.vscode/mcp.json` repassado, exceto `${input:...}` | `.mcp.json`, `.github/mcp.json` (pasta atual até raiz git; pasta confiável) |
| **MCP: arquivo avulso** | `code --add-mcp`; descoberta de outros apps | NV | `--additional-mcp-config @arquivo`; plugin |
| **Transportes** | stdio, HTTP (cai para SSE), socket/pipe | só **servidores locais sem autenticação**, por ora | `local`/`stdio`, `http`, `sse` |
| **Variáveis no MCP** | variáveis do VS Code (`${workspaceFolder}`, `${input:...}`), `envFile` | NV | `$VAR`, `${VAR}`, `${VAR:-padrão}` em `env` |
| **Trocar a pasta de usuário** | n/a (perfil do VS Code) | `COPILOT_HOME` (o host o define; issue #5022) | `COPILOT_HOME` (substitui `~/.copilot` inteiro) |
| **Dentro do Maestri** | n/a | n/a | sem preset oficial; preset personalizado `copilot` (inferência) |

## 1. Instruções e contrato

### 1.1 VS Code (modo agente)

> As páginas mudaram de `code.visualstudio.com/docs/copilot/...` para `/docs/agent-customization/...` e
> `/docs/agents/...` (redirecionamento 301 conferido para `custom-instructions` e `mcp-servers`). As citações
> vêm do repositório oficial `microsoft/vscode-docs` (branch `main`, `DateApproved: 9/30/2026`), e as frases
> principais foram conferidas também na página publicada.

- **Fato: há dois "agentes Copilot" no VS Code.**
  - O harness **Copilot**: *"uses the Copilot SDK to access the agent runtime also used by Copilot CLI and the
    GitHub Copilot app"*. Roda no **Agent Host**, um processo dedicado.
  - O harness **Local**: *"runs interactively in the VS Code extension host"*.

  ([agent-harnesses](https://code.visualstudio.com/docs/agents/run/agent-harnesses))
  O Local está a caminho da saída: *"the Local agent will be removed in a future release"*
  ([overview](https://code.visualstudio.com/docs/agent-customization/overview)). O alvo inicial recomendado para
  uma tarefa comum é *"Copilot for a general coding task"*, mas o editor só prefere o Copilot no lugar do Local
  com `chat.editor.preferCopilotHarness` (*Experimental*) (mesma página de harnesses).
- **Fato: o Agent Host lê a pasta de usuário do runtime.** *"The Agent Host reads user-level customizations from
  harness-agnostic folders like `~/.copilot` and `~/.claude`. Customizations stored only in your VS Code profile
  user data are a legacy location that the Copilot agent doesn't read."*
  ([agent-host](https://code.visualstudio.com/docs/agents/concepts/agent-host))
- **Fato: os formatos dependem do harness.** Tabela da página de instruções:
  - Copilot: *"`.github/copilot-instructions.md` or `AGENTS.md`"* e *"`.github/instructions/**/*.instructions.md`"*.
  - Local: *"`.github/copilot-instructions.md`, `AGENTS.md`, or `CLAUDE.md`"*, mais `.claude/rules`.

  ([custom-instructions](https://code.visualstudio.com/docs/agent-customization/custom-instructions))
- **Fato: camada de usuário.**
  - Harness Copilot: *"For personal, always-on instructions in Copilot Agent Host sessions, use
    `~/.copilot/copilot-instructions.md`."* Tabela de locais: *"Agent Host user, Copilot format |
    `~/.copilot/instructions`"* e *"Agent Host user, Claude format | `~/.claude/rules`"*.
  - Local: *"Local agent user | VS Code profile storage"*, mais `~/.claude/CLAUDE.md` com `chat.useClaudeMdFile`.
  - Sincronização: *"User instructions in Agent Host folders, such as `~/.copilot/instructions` and
    `~/.claude/rules`, do not roam through Settings Sync."*

  (mesma página)
- **Fato: não há precedência.** *"Applicable instruction sources are additive. Do not depend on a file order or
  precedence rule to resolve conflicts because discovery and merge behavior can differ by harness."* (mesma página)
- **Fato: apontar para fora do projeto.**
  - Referências: *"To reference files or URLs in instructions, use Markdown links. Relative file paths resolve
    from the instructions file."* No Local, isso depende de `chat.includeReferencedInstructions`, que vem
    `false` por padrão ([ai-settings](https://code.visualstudio.com/docs/agents/reference/ai-settings)).
  - A pasta extra `chat.instructionsFilesLocations` é *"deprecated and only used by the Local agent"*.
  - Se um link Markdown com caminho absoluto (`C:/context-hub/...`) é seguido pelo harness Copilot:
    **não verificado**.
- **Fato: AGENTS.md no Local.** `chat.useAgentsMdFile` (padrão `true`); aninhados com `chat.useNestedAgentsMdFiles`
  (padrão `false`). Pastas acima do workspace só com `chat.useCustomizationsInParentRepositories` (padrão `false`),
  e só até o `.git` ([overview](https://code.visualstudio.com/docs/agent-customization/overview)).
- **Fato: nas sessões Agent Host, as regras são as do harness.** *"Agent Host sessions use the discovery rules and
  file formats of the selected harness."* ([custom-instructions](https://code.visualstudio.com/docs/agent-customization/custom-instructions))
  - **Inferência:** com o harness Copilot valem as regras do Copilot CLI (§1.2), mas a página do VS Code não
    descreve `COPILOT_CUSTOM_INSTRUCTIONS_DIRS`. Se o Agent Host herda essa variável do ambiente do VS Code:
    **não verificado**.
- **Limite de tamanho:** nenhum documentado. A página só recomenda *"Keep your instructions short and
  self-contained"*.
- **Divergência entre docs:** a tabela do GitHub para "Visual Studio Code / Copilot Chat" lista só
  repository-wide, path-specific e `AGENTS.md` ([custom-instructions-support](https://docs.github.com/en/copilot/reference/custom-instructions-support)).
  Não cita `~/.copilot` nem `CLAUDE.md`. A doc do VS Code é mais nova e mais completa.

### 1.2 Copilot CLI

- **Fato: locais.** Tabela de how-to ([add-custom-instructions](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-custom-instructions)):
  - `$HOME/.copilot/copilot-instructions.md`: *"User-level instructions that apply across repositories."*
  - `$HOME/.copilot/instructions/**/*.instructions.md`: *"Modular user-level instructions."*
  - `.github/copilot-instructions.md`, `.github/instructions/**/*.instructions.md`, `AGENTS.md`, `CLAUDE.md`
    (*"Copilot CLI also uses `.claude/CLAUDE.md`"*) e `GEMINI.md`.
  - *"Directories listed in `COPILOT_CUSTOM_INSTRUCTIONS_DIRS` | Additional `AGENTS.md` and `*.instructions.md`
    files. Separate multiple directories with commas."*
  - *"If you set the `COPILOT_HOME` environment variable, Copilot CLI uses that directory instead of
    `$HOME/.copilot` for both user-level instruction locations."*
- **Fato: onde procura.** How-to: *"the repository root, the current working directory, intermediate directories
  between them, and any directories nested in the path of a file it is working on"*. A referência resume como
  *"In Git root and cwd"* e acrescenta `.claude/rules/**/*.md`
  ([cli-command-reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-command-reference#custom-instructions-locations)).
  O changelog v1.0.11 (23/03/2026) diz que instruções, MCP, skills e agentes *"are now discovered at every
  directory level from the working directory up to the git root"*.
  ([changelog](https://github.com/github/copilot-cli/blob/main/changelog.md))
- **Fato: tudo é somado.** *"Copilot CLI loads custom instructions from these locations simultaneously (all are
  merged)"* (referência). *"It removes duplicate copies of identical … instructions, but does not define a general
  precedence order between these files. Avoid conflicting instructions."* (how-to). Não há a regra "CLAUDE.md
  exclui AGENTS.md" do Claude Code.
- **Fato: imports.** O changelog v1.0.66 (30/06/2026) diz *"Expand @-style imports in AGENTS.md, CLAUDE.md, and
  Copilot instruction files"*. As duas páginas oficiais **se contradizem** sobre caminho absoluto:
  - How-to: *"Referenced files must remain within the repository, or within the custom instructions directory
    for local instructions. Absolute paths and paths beginning with `~/` are not loaded."* (conferido na página
    publicada)
  - Referência: *"Paths can be relative to the instruction file's directory or absolute. Imports are resolved
    recursively, up to a depth limit, with cycle and size guards."*

  Se `@C:/context-hub/...` dentro de `~/.copilot/copilot-instructions.md` carrega: **não verificado**. O trecho
  *"within the custom instructions directory for local instructions"* sugere que imports relativos dentro de
  `~/.copilot` valem (inferência).
- **Fato: `COPILOT_CUSTOM_INSTRUCTIONS_DIRS`.** *"Comma-separated list of additional directories for custom
  instructions."* ([cli-command-reference, Environment variables](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-command-reference#environment-variables))
  Há issues abertas, relatos de usuários sem resposta oficial:
  - [#3987](https://github.com/github/copilot-cli/issues/3987): *"Custom-dir AGENTS.md (COPILOT_CUSTOM_INSTRUCTIONS_DIRS)
    no longer injected globally as of 1.0.66"*. O arquivo passa a ser tratado como instrução "aninhada", restrita
    à própria pasta.
  - [#3507](https://github.com/github/copilot-cli/issues/3507) (Windows): só `AGENTS.md` e `.github/instructions/**`
    são honrados nessa pasta, não `copilot-instructions.md`, `CLAUDE.md` nem `GEMINI.md`.
  - [#3543](https://github.com/github/copilot-cli/issues/3543): travamento na partida por glob recursivo nessa pasta.
  - [#1433](https://github.com/github/copilot-cli/issues/1433): problema genérico com a variável.
  - [#4622](https://github.com/github/copilot-cli/issues/4622) pede caminhos de descoberta configuráveis por usuário.
- **Fato: desligar.** `--no-custom-instructions` *"Disable loading of custom instructions from `AGENTS.md` and
  related files."* `/instructions` lista e liga/desliga arquivos na sessão. `copilot instruction list --json` lista
  as fontes descobertas (referência).
- **Fato: recarga.** *"Changes you make to custom instructions files are not immediately available for use in
  active CLI sessions."* (how-to)
- **Limite de tamanho:** nenhum número documentado (**não verificado**).
- **Local (observação, sem alterar nada):** `~/.copilot/copilot-instructions.md` existe nesta máquina, com 728
  bytes e o cabeçalho *"GSD Configuration — managed by gsd-core installer"*. Um instalador de terceiros já usa
  essa camada.

## 2. Skills

### 2.1 VS Code

- **Fato: locais.** *"Project skills … `.github/skills/`, `.claude/skills/`, `.agents/skills/`"* e *"Personal
  skills, stored in your user profile | `~/.copilot/skills/`, `~/.claude/skills/`, `~/.agents/skills/`"*. *"Unless
  otherwise noted, the configuration options and controls on this page apply to Copilot."*
  ([agent-skills](https://code.visualstudio.com/docs/agent-customization/agent-skills))
- **Fato: pasta extra.** *"The `chat.agentSkillsLocations` setting is deprecated and only used by the Local
  agent."* Extensões podem contribuir skills (`chatSkills`), e plugins também (mesma página).
  Plugins locais entram por `chat.pluginLocations`. Plugins instalados pelo CLI em `~/.copilot/installed-plugins/`
  aparecem no VS Code ([agent-plugins](https://code.visualstudio.com/docs/agent-customization/agent-plugins)).
- **Fato: frontmatter.** `name` com no máximo 64 caracteres, *"Must match the parent directory name"*, e
  `description` com no máximo 1024 caracteres (mesma página).
- **Symlink e junction:** a página não fala de links (**não verificado**).
- **Possível conflito (inferência, não verificado):** a issue [#5022](https://github.com/github/copilot-cli/issues/5022)
  relata que o Agent Host inicia o runtime com `COPILOT_HOME=c:\Users\<user>\.copilot`. O changelog do CLI v1.0.66
  diz *"COPILOT_HOME and --config-dir stop loading skills from ~/.agents/skills"*. Se as duas coisas valem juntas, o
  harness Copilot do VS Code pode **não** ler `~/.agents/skills`, ao contrário do que a doc do VS Code lista.

### 2.2 Copilot CLI

- **Fato: locais e prioridade.** *"Skills are loaded from these locations in priority order (first found wins
  for duplicate names)"*:
  1. `.github/skills/`, `.agents/skills/` e `.claude/skills/` (projeto)
  2. pai `.github/skills/`
  3. `~/.copilot/skills/` e `~/.agents/skills/` (pessoal)
  4. plugins
  5. `COPILOT_SKILLS_DIRS` (*"Additional directories (comma-separated)"*)
  6. `--add-dir <path>` (lê o `.github/skills/` da pasta)
  7. embutidas
  8. remotas da organização

  ([cli-command-reference, Skill locations](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-command-reference#skill-locations))
  O how-to repete: *"For personal skills … `~/.copilot/skills` or `~/.agents/skills`"*
  ([add-skills](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-skills)).
- **Fato: não lê `~/.claude/skills` como pasta pessoal.** Nenhuma das páginas lista essa pasta. `.claude/skills`
  só vale no projeto. A página conceitual do GitHub confirma: *"Personal skills … (`~/.copilot/skills` or
  `~/.agents/skills`)"* ([about-agent-skills](https://docs.github.com/en/copilot/concepts/agents/about-agent-skills)).
- **Fato: outras vias de pasta extra.**
  - `skillDirectories` (`string[]`): *"Additional directories to search for custom skill definitions (in addition
    to `~/.copilot/skills/`)"*. Excluir: `ignoredSkillsLocations` (aceita `~`).
    ([cli-config-dir-reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-config-dir-reference#configuration-file-settings))
  - `copilot skill add <pasta>`: *"Installing a directory registers it as a custom skill source rather than
    copying it."* (referência)
- **Fato: `~/.agents/skills` e `COPILOT_HOME`.** O suporte entrou na v1.0.11 (*"Add ~/.agents/skills/ as a personal
  skill discovery directory"*). A v1.0.66 diz *"COPILOT_HOME and --config-dir stop loading skills from
  ~/.agents/skills"* ([changelog](https://github.com/github/copilot-cli/blob/main/changelog.md)).
  **Consequência:** trocar a pasta de usuário por `COPILOT_HOME` corta a convenção compartilhada com Codex e
  OpenCode.
- **Fato: symlink.**
  - Changelog v1.0.62: *"Load skills from symlinked directories outside the configured root"*.
  - Changelog v1.0.68: *"Avoid duplicate skill and command parse errors from symlinked scan roots"*.
  - Issues [#1021](https://github.com/github/copilot-cli/issues/1021) (*"Copilot CLI Not Detecting Symlinked Skills"*)
    e [#1090](https://github.com/github/copilot-cli/issues/1090) foram fechadas como *completed*.
- **Junction:** a doc não fala de junction. A issue [#3264](https://github.com/github/copilot-cli/issues/3264)
  (*"Document symlink behavior on Windows and other OS for files in .copilot folder"*) está aberta, sem resposta
  oficial. **Não verificado.**
- **Bugs abertos relevantes** (relatos de usuários):
  - [#4545](https://github.com/github/copilot-cli/issues/4545): *"Personal skills in ~/.copilot/skills/ are never
    discovered"* (1.0.81).
  - [#4401](https://github.com/github/copilot-cli/issues/4401): skill em `~/.agents/skills` não achada no Windows
    (1.0.78).
  - [#4700](https://github.com/github/copilot-cli/issues/4700): `skillDirectories` ignorado no modo `--acp`.
- **Fato: frontmatter.** `name` com no máximo 64 caracteres, e o CLI aceita pontos, dois-pontos e espaços (o VS
  Code não aceita). `description` com no máximo 1024 caracteres. `allowed-tools` pré-aprova ferramentas
  (referência e how-to).
- **Local (observação):** `~/.copilot/skills` tem pastas reais (GSD e graphify). `~/.agents/skills` tem 117
  entradas, todas pastas reais, nenhuma junction. Não há variável `COPILOT_*` no ambiente deste processo.

## 3. MCP

### 3.1 VS Code

- **Fato: arquivos.** *"Workspace, VS Code format: `.vscode/mcp.json` … top-level `servers` object"*; *"Workspace,
  portable format: … `.mcp.json` … top-level `mcpServers` object and works across compatible tools"*; *"User
  profile: … MCP: Open User Configuration"*; *"User, portable format: create `$COPILOT_HOME/mcp-config.json`, or
  `~/.copilot/mcp-config.json` when `COPILOT_HOME` is not set"*. O fluxo **MCP: Add Server** marca os destinos
  `.vscode/mcp.json` e perfil como *"deprecated"* e diz *"Prefer the portable destinations for new servers."*
  ([mcp-servers](https://code.visualstudio.com/docs/agent-customization/mcp-servers))
- **Fato: Agent Host.** *"The Agent Host reads harness-agnostic MCP config from `.mcp.json` (workspace) and
  `~/.copilot/mcp-config.json` (user). It doesn't read `.vscode/mcp.json` directly, but VS Code forwards servers you
  configure in VS Code to the Agent Host, except servers that require interactive input (for example,
  `${input:...}` variables)."* ([agent-host](https://code.visualstudio.com/docs/agents/concepts/agent-host))
  Limitação do harness Copilot: *"Copilot sessions can currently access only local MCP servers that don't require
  authentication."* ([agent-harnesses](https://code.visualstudio.com/docs/agents/run/agent-harnesses))
- **Fato: transportes.** stdio (`command`, `args`, `cwd`, `env`, `envFile`) e `http`/`sse`: *"VS Code first tries
  the HTTP Stream transport and falls back to SSE"*. Também aceita *"Unix sockets or Windows named pipes"*
  (`pipe:///...`). ([mcp-configuration](https://code.visualstudio.com/docs/agents/reference/mcp-configuration))
- **Fato: descoberta de configs de outros apps.** `chat.mcp.discovery.enabled` com a fonte `copilot` lê
  *"`<COPILOT_HOME>/mcp-config.json`, or `~/.copilot/mcp-config.json`"*. *"All discovery sources are off by
  default."* *"Agent Host sessions read the Copilot CLI MCP configuration independently."* (mesma página)
- **Fato: sandbox de MCP** só em macOS e Linux (mesma página). No Windows não existe.
- **Fato: migração.** O editor de customizações oferece **Migrate MCP Servers** para `.mcp.json` ou
  `$COPILOT_HOME/mcp-config.json`. *"the files don't stay synchronized"*
  ([overview](https://code.visualstudio.com/docs/agent-customization/overview)).
- **Local (observação):** `%APPDATA%\Code\User\mcp.json` usa o formato `servers`. O `settings.json` do VS Code tem
  a chave `chat.mcp.discovery.enabled`. Valores não copiados.

### 3.2 Copilot CLI

- **Fato: arquivos.** *"Configure persistent servers in `~/.copilot/mcp-config.json`. Use `--additional-mcp-config`
  to add servers for a single session."* No projeto, `.mcp.json` *"in any directory from your working directory up
  to the repository root"* e `.github/mcp.json`. O projeto vence o usuário quando os nomes coincidem.
  *"Project-level MCP servers are loaded only after you confirm folder trust on first launch. They are silently
  skipped in untrusted directories."* ([add-mcp-servers](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-mcp-servers))
- **Fato: ordem.** 1. `--additional-mcp-config`; 2. plugins; 3. workspace (`.mcp.json` e `.github/mcp.json`, da
  pasta atual até a raiz git, *"requires the folder to be trusted"*); 4. `~/.copilot/mcp-config.json`.
  ([cli-command-reference, MCP server loading priority](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-command-reference#mcp-server-loading-priority))
- **Fato: transportes.** `local`/`stdio`, `http` (*"streamable HTTP"*) e `sse`. Campos locais: `command`, `args`,
  `tools` (obrigatório no formato de usuário), `env` (*"Supports `$VAR`, `${VAR}`, and `${VAR:-default}`
  expansion"*), `cwd` e `timeout` (mesma página).
- **Fato: formato.** Os arquivos de projeto aceitam `mcpServers` ou o formato "nu", em que cada chave é um
  servidor (add-mcp-servers). *"The `.vscode/mcp.json` file for VS Code is not read by Copilot CLI."* O changelog
  v1.0.22 removeu `.vscode/mcp.json` como fonte.
- **Fato: compartilhar.**
  - `--additional-mcp-config=JSON`: *"The server configuration can be supplied as a JSON string or a file path
    (prefix with `@`)"*, com `~/` expandido desde a v1.0.85. Exige mudar o comando de lançamento.
  - Plugins: um plugin leva skills e MCP. Na lista de locais de arquivo, *"MCP configuration | Agent Plugins:
    `mcp.json`. Legacy plugins: `.mcp.json`…"*. *"Path-sourced plugins in a local (directory-source) marketplace
    load live from their real directory"*, e `--plugin-dir=DIRECTORY` carrega uma pasta.
    ([cli-plugin-reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference))
  - O CLI também reconhece manifesto `.claude-plugin/plugin.json` e as variáveis `CLAUDE_PLUGIN_ROOT` /
    `CLAUDE_PLUGIN_DATA` (mesma página). **Inferência:** um plugin do hub no formato Claude poderia servir ao
    Claude Code e ao Copilot CLI. Não testado.
  - Include de outro arquivo de config no `mcp-config.json`: não documentado (**não verificado**).
- **Fato: confiança.** *"you'll be asked to confirm that you trust the files in, and below, the directory from
  which you launched the CLI"*. As pastas confiáveis ficam em `trustedFolders` no `config.json`
  ([configure-copilot-cli](https://docs.github.com/en/copilot/how-tos/copilot-cli/set-up-copilot-cli/configure-copilot-cli)).
- **Local (observação):** `~/.copilot/mcp-config.json` existe, no formato `mcpServers`, com 1 servidor.

### 3.3 Observação comum

O formato portátil `.mcp.json` (`mcpServers`) é lido pelo CLI, pelo Agent Host do VS Code e pelo Claude Code
(pesquisa 13). Ele é o candidato natural a arquivo de MCP de projeto comum. **Inferência; não verificado:** se o
Claude Code tolera o campo `tools` exigido pelo formato de usuário do Copilot.

## 4. Windows

- **Fato: home.** *"Windows: `$HOME\.copilot\config.json`"* ([configure-copilot-cli](https://docs.github.com/en/copilot/how-tos/copilot-cli/set-up-copilot-cli/configure-copilot-cli)).
  *"On Windows, the default file is typically: `C:\Users\YOUR-USER\.copilot\permissions-config.json`"*
  ([cli-config-dir-reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-config-dir-reference)).
- **Fato: cache.** *"Windows: `%LOCALAPPDATA%/copilot`"*, fora do alcance de `COPILOT_HOME`; troca-se com
  `COPILOT_CACHE_HOME` (mesma página).
- **Fato: `COPILOT_HOME`.** *"replaces the entire `~/.copilot` path"*. `--config-dir` está obsoleto (mesma
  página). *"Previous XDG-based configuration locations are migrated to `~/.copilot` at startup when
  `COPILOT_HOME` isn't set."*
- **Fato: shell.** Pré-requisito: *"(On Windows) PowerShell v6 or higher"*. Instalação por `winget install
  GitHub.Copilot` ou npm ([install-copilot-cli](https://docs.github.com/en/copilot/how-tos/copilot-cli/set-up-copilot-cli/install-copilot-cli)).
  `powershellFlags` tem padrão `["-NoProfile", "-NoLogo"]`, e *"On Windows, the CLI prefers PowerShell 7+ (`pwsh`)
  and falls back to Windows PowerShell"* (cli-config-dir-reference).
- **Fato: política gerenciada.** `HKLM\SOFTWARE\Policies\GitHubCopilot` e `%ProgramFiles%\GitHubCopilot\managed-settings.json`
  (cli-config-dir-reference).
- **Fato: sandbox.** No Windows usa *"ProcessContainer"*. O changelog v1.0.76 diz *"Windows cannot deny per path"*.
- **Fato: bugs de caminho no Windows.**
  - [#4702](https://github.com/github/copilot-cli/issues/4702): instrução carregada duas vezes por `\` × `/`;
    fechada como *completed* em 08/09/2026.
  - [#5022](https://github.com/github/copilot-cli/issues/5022): aberta em 30/09/2026. *"VS Code agent host loads
    ~/.copilot/instructions twice (drive-letter case mismatch in dedup)"*.
- **Fato: VS Code.** O Agent Host pode rodar *"on an SSH, Tunnel, or WSL host"*
  ([agent-host](https://code.visualstudio.com/docs/agents/concepts/agent-host)). Com shell init, carrega *"your
  PowerShell profiles on Windows"* (`chat.agentHost.shellTool.initScript.enabled`) ([agent-harnesses](https://code.visualstudio.com/docs/agents/run/agent-harnesses)).
- **WSL** (fora do recorte deste ticket): a doc do CLI não descreve compartilhar `~/.copilot` entre Windows e WSL
  (**não verificado**).
- **Local (observação):**
  - Copilot CLI 1.0.80 instalado via npm (`%APPDATA%\npm\copilot`). O último release no changelog é o 1.0.91
    (01/10/2026).
  - VS Code com pastas das versões 1.139.1 e 1.140.0. A extensão embutida "GitHub Copilot" (`copilot-chat`) é a
    0.67.0 na 1.139.1.

## 5. Maestri

Fonte primária: docs oficiais em https://www.themaestri.app/en/docs/ (as 21 páginas do índice, varridas por busca textual), o changelog oficial em
https://www.themaestri.app/en/changelog e o app instalado, lido sem alterar nada.

- **Fato: a doc não cita o Copilot.** A introdução fala de *"coding agents like Claude Code, Codex, or OpenCode"*
  ([intro](https://www.themaestri.app/en/docs/intro)), e a página de terminais manda escolher *"a coding agent from
  the preset list"* ([terminals](https://www.themaestri.app/en/docs/terminals)). Nenhuma das 21 páginas contém
  "copilot".
- **Fato: o changelog cita o Copilot CLI uma vez.** Na 0.21.5 (16/04/2026): *"Improved compatibility with
  Ink-based terminals like GitHub Copilot CLI when sending prompts through 'ask'"*
  ([changelog](https://www.themaestri.app/en/changelog)).
- **Observação local: não há tipo de agente Copilot no app.**
  - O bundle (`resources/app.asar`) não contém a palavra "copilot". A função `agentIdentityFromLegacyType`
    reconhece `claude_code`, `codex`, `gemini_cli`, `antigravity_cli`, `open_code`, `custom` e `generic_shell`.
  - Os presets locais são Claude Code, Codex, Antigravity, OpenCode e Shell.
  - **Inferência:** o Copilot CLI entra como preset do tipo `custom` com o comando `copilot`.
- **Papel (role).** *"Roles work by starting the agent in a project subdirectory with its own CLAUDE.md /
  AGENTS.md"* ([terminals](https://www.themaestri.app/en/docs/terminals)), em *"`<project>/.maestri/roles/<role-id>/`"*
  ([environments](https://www.themaestri.app/en/docs/environments)).
  - No bundle, o instalador de papel grava `CLAUDE.md`, `AGENTS.md` e `role.json`. O `settings.json` extra só é
    criado quando o comando contém `gemini` ou `qwen`.
  - `resolveRoleAwareCwd` troca a pasta inicial para a do papel quando ela existe, sem olhar o tipo de agente
    (leitura de código minificado; **não verificado em execução**).
- **O que o Copilot CLI leria com papel** (inferência a partir da doc do CLI, §1.2 e §3.2):
  - Pasta atual = `…/.maestri/roles/<id>/`: `AGENTS.md` e `CLAUDE.md` do papel. Têm o mesmo conteúdo, e o CLI
    remove duplicatas idênticas.
  - **Também** `AGENTS.md`, `CLAUDE.md`, `.github/copilot-instructions.md` e `.github/instructions` da **raiz
    git** do projeto e das pastas intermediárias, mais a camada global (`~/.copilot/...`,
    `COPILOT_CUSTOM_INSTRUCTIONS_DIRS`). Ao contrário do Claude Code, o contrato do workspace não se perde, desde
    que o workspace seja repositório git. Se não for, o comportamento é **não verificado**: a doc só fala em
    "Git root and cwd".
  - Skills de projeto (`.github/skills`, `.agents/skills`, `.claude/skills`) e `.mcp.json` sobem da pasta do papel
    até a raiz git.
  - O MCP de projeto exige pasta confiável. Confiar no projeto cobre *"files in, and below"*; na primeira vez,
    pode aparecer o prompt de confiança na pasta do papel.
- **Skills do Maestri.** As raízes padrão do app (`defaultSkillBases`) são `.claude/skills`, `.agents/skills`,
  `.hermes/skills` e `.gemini/config/skills`. Não inclui `.copilot/skills`. **Inferência:** a skill do Maestri
  chega ao Copilot CLI por `~/.agents/skills`, a menos que `COPILOT_HOME` esteja definido (§2.2).
- **VS Code:** a doc do Maestri não menciona o VS Code. O VS Code não roda dentro do canvas.

### Consequências para o hub (análise, não decisão)

- **Uma pasta, dois Copilots.** Configurar `~/.copilot` em cada máquina atende o CLI e o harness Copilot do VS
  Code. O agente Local do VS Code é legado e lê do perfil do VS Code; serve como transição.
- **Skills:** a convenção `~/.agents/skills` (vault atual) já cobre o Copilot CLI, o Codex e o OpenCode. Não
  convém usar `COPILOT_HOME` (corta `~/.agents/skills`). `COPILOT_SKILLS_DIRS` e `skillDirectories` permitem
  apontar direto para `C:\context-hub\...` sem link.
- **Contrato:** três caminhos, nenhum firme na doc:
  - `COPILOT_CUSTOM_INSTRUCTIONS_DIRS` → pasta do hub (regressões relatadas);
  - `@` absoluto em `~/.copilot/copilot-instructions.md` (doc contraditória);
  - `~/.copilot/copilot-instructions.md` gerado ou ligado (symlink de arquivo não documentado).
- **MCP:** um `mcp-config.json` por máquina (o próprio CLI reescreve o arquivo, como o `/mcp add`), ou um plugin
  do hub carregado de uma pasta local. O `.mcp.json` de projeto é comum ao CLI, ao VS Code e ao Claude Code.

## Mudanças de nome e URL

- Docs do VS Code: `/docs/copilot/customization/custom-instructions` e `/docs/copilot/chat/mcp-servers` → 301
  para `/docs/agent-customization/...`. A área de agentes agora fica em `/docs/agents/...`.
- "Copilot coding agent" agora é **"Copilot cloud agent"** nas docs do GitHub e do VS Code.
- Copilot CLI:
  - `--config-dir` foi substituído por `COPILOT_HOME` (v1.0.40).
  - As configurações de usuário passaram de `config.json` para `settings.json` (migração automática).
  - `.vscode/mcp.json` deixou de ser lido (v1.0.22).
  - `copilot plugins --kind/--skill` deram lugar a `copilot skill`, `copilot mcp` e `copilot instruction`.
- VS Code:
  - `chat.instructionsFilesLocations`, `chat.agentSkillsLocations`, `chat.agentFilesLocations` e
    `chat.modeFilesLocations` estão obsoletas.
  - Prompt files (`*.prompt.md`) estão obsoletos no Agent Host (*"aren't loaded by Agent Host"*).
  - O agente Local será removido.

## Lacunas e não verificado

- **Contrato:**
  - Se `@C:/...` absoluto funciona no CLI: doc contraditória, **não verificado**.
  - Se `COPILOT_CUSTOM_INSTRUCTIONS_DIRS` injeta `AGENTS.md` globalmente na versão atual (1.0.91): **não
    verificado** (issue #3987 aberta).
  - Se o Agent Host do VS Code herda `COPILOT_CUSTOM_INSTRUCTIONS_DIRS` / `COPILOT_SKILLS_DIRS` do ambiente:
    **não verificado**.
  - Limite de tamanho de instruções: nenhum documentado.
- **Skills:**
  - Junction (pasta de skill ou `~/.copilot/skills` inteira) no Windows: **não verificado**; só symlink aparece
    no changelog.
  - Se o harness Copilot do VS Code lê `~/.agents/skills` e `~/.claude/skills`: a doc do VS Code diz que sim, mas
    o runtime do CLI não lista `~/.claude/skills` e corta `~/.agents/skills` com `COPILOT_HOME`. **Não verificado.**
  - Issue #4545 (skills pessoais não descobertas) aberta; estado na 1.0.91 **não verificado**.
- **MCP:**
  - Include de config ou variável de ambiente para um `mcp-config.json` alternativo, além de `COPILOT_HOME` e
    `--additional-mcp-config`: não documentado.
  - Se o Claude Code aceita o campo `tools` num `.mcp.json` comum: **não verificado**.
- **Maestri:**
  - Que o Copilot CLI funcione como preset `custom` com papel (cwd na pasta do papel), e o comportamento fora de
    repositório git: inferido do código e da doc, **não testado**.
- **Symlink de arquivo:** `~/.copilot/copilot-instructions.md` ou `mcp-config.json` como symlink. Só
  `settings.json` tem regra documentada (*"writes from the `/settings` command follow the symlink"*). Um
  comentário na #3264 relata o CLI trocando o symlink por arquivo comum em versões anteriores.

## Consultas

**Buscas na web (WebSearch):**
1. `Copilot CLI COPILOT_CUSTOM_INSTRUCTIONS_DIRS AGENTS.md user-level instructions` (domínios: docs.github.com, github.com, github.blog)
2. `VS Code Copilot agent host ~/.copilot skills instructions harness 2026` (domínios: code.visualstudio.com, github.com)
3. `Maestri themaestri GitHub Copilot CLI agent preset`
4. `copilot cli skills windows junction symlink ~/.copilot/skills not loaded` (domínio: github.com)
5. `github copilot cli mcp-config.json share across machines COPILOT_HOME --additional-mcp-config file` (domínios: docs.github.com, github.com, github.blog)

**Busca de issues (API do GitHub, `repo:github/copilot-cli`):** `skills symlink`, `skills junction`,
`COPILOT_SKILLS_DIRS`, `COPILOT_CUSTOM_INSTRUCTIONS_DIRS`, `instructions absolute path`, `skills windows`.
Issues lidas (corpo e estado): #1021, #1090, #1433, #2161, #2230, #3264 (com comentários), #3507, #3987, #4401,
#4545, #4622, #4700, #4702, #5011, #5022.

**Páginas lidas (na íntegra ou nas seções pertinentes):**
- VS Code (Markdown de `raw.githubusercontent.com/microsoft/vscode-docs/main/docs/...`; frases principais
  conferidas no HTML publicado):
  - na íntegra: `agent-customization/{custom-instructions,agent-skills,overview}`, `agents/concepts/{agent-harnesses,agent-host}`;
  - por seção ou busca textual: `agent-customization/{mcp-servers,agent-plugins}`, `agents/run/agent-harnesses`,
    `agents/reference/{mcp-configuration,ai-settings}`.
  - Baixadas mas não usadas: `custom-agents`, `concepts/customization`, `agents-window-configuration`, `memory`,
    `workspace-context`, `faq`.
  - Redirecionamentos 301 conferidos com `curl`.
- GitHub Docs (Markdown renderizado pela API oficial `docs.github.com/api/article/body?pathname=...`; frases-chave
  conferidas no HTML publicado):
  - na íntegra: `copilot/how-tos/copilot-cli/customize-copilot/{add-custom-instructions,add-skills}`,
    `copilot/concepts/agents/about-agent-skills`;
  - por seção ou busca textual: `.../customize-copilot/add-mcp-servers`,
    `copilot/how-tos/copilot-cli/set-up-copilot-cli/{configure-copilot-cli,install-copilot-cli}`,
    `copilot/reference/copilot-cli-reference/{cli-command-reference,cli-config-dir-reference,cli-plugin-reference}`,
    `copilot/reference/custom-instructions-support`, `copilot/concepts/agents/copilot-cli/about-copilot-cli`.
  - Baixadas mas não usadas: `change-settings`, `overview`, `plugins-creating`, `comparing-cli-features`,
    `connecting-vs-code`, `add-repository-instructions-in-your-ide`, `add-personal-instructions`.
- Copilot CLI: `raw.githubusercontent.com/github/copilot-cli/main/changelog.md` (busca textual por symlink,
  junction, skills, instruções, MCP, Windows, `COPILOT_HOME`).
- Maestri: `www.themaestri.app/en/docs/` (índice) e as 21 páginas listadas nele (busca textual por copilot, preset, gemini, opencode, codex); `www.themaestri.app/en/changelog`.

**Leitura local (sem alterar nada):**
- `%USERPROFILE%\.copilot\` (listagem; nomes de chave de `config.json` e `mcp-config.json`; tamanho e cabeçalho
  de `copilot-instructions.md`; listagem de `skills\` e tipo de link)
- `%USERPROFILE%\.agents\skills\` (contagem; tipo de link)
- `%APPDATA%\npm\copilot` e `node_modules\@github\copilot\package.json` (versão)
- `%LOCALAPPDATA%\Programs\Microsoft VS Code\*\resources\app\package.json` e `extensions\copilot\package.json` (versões)
- `%APPDATA%\Code\User\` (listagem; chaves `chat.*` de `settings.json`; chave de topo de `mcp.json`)
- `%USERPROFILE%\.maestri\preferences.json` (`agentPresets`: id, nome, tipo, comando)
- `%LOCALAPPDATA%\Programs\Maestri\resources\app.asar` (busca textual: `copilot`, `agentIdentityFromLegacyType`,
  `skillBases`, `roles/`, `AGENTS.md`, `role.json`)
- nomes das variáveis `COPILOT_*` do processo (nenhuma definida)
