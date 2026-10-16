# Portas 3 e 4: workspace do Maestri sem papel e com papel

Pesquisa em fonte primária (leitura apenas). Data: 2026-10-10. Nada foi executado além de `maestri help` e `maestri <comando> --help`; nenhum workspace, terminal, papel ou recruta foi criado. Os prompts dos papéis e os dados dos outros workspaces não foram copiados.

## Pergunta

1. Ao abrir um terminal de agente num workspace do Maestri, qual é o diretório de trabalho, e o que o Maestri exporta e instala (variáveis `MAESTRI_*`, skills em `~/.claude/skills` e `~/.agents/skills`)?
2. Com papel: o agente abre em `<workspace>/.maestri/roles/<id>/`. O que o Maestri grava ali (CLAUDE.md, AGENTS.md, role.json) e com que conteúdo?
3. Com um CLAUDE.md na pasta do papel, o Claude Code lê o AGENTS.md de uma pasta acima? E com `claude-md-and-agents-md`?
4. Onde a documentação do Maestri diz que ficam papéis, presets, partituras e equipes, e se podem ser lidos de uma pasta escolhida (padronização do Maestri em `agents/` do hub)?

## Respostas

### 1. Workspace sem papel

**Diretório de trabalho.**
- Doc de Workspaces: "Working directory — The root folder for this project. New terminals will open here by default." (https://themaestri.app/en/docs/workspaces)
- Evidência local (fato lido, não doc): `C:\Users\gustavo.delfino\.maestri\workspaces\271fe5c6-f63d-41e9-85d9-75981ab3dbce\workspace.json` traz `"name": "Context Hub"` e `"workingDirectory": "C:\\Projetos\\context-hub"`.
- Com `--dir`: "`--dir` must point at a directory that already exists." (`maestri recruit --help`); e na skill: "`--dir`: start the recruit in this working directory instead of inheriting yours." (`~/.claude/skills/maestri-manager/SKILL.md`). A doc não descreve outro caminho de mudar o diretório de um terminal.

**CLAUDE.md e AGENTS.md do workspace.** Doc de Workspaces, seção "CLAUDE.md and AGENTS.md": "From the workspace edit screen, you can manage CLAUDE.md and AGENTS.md files. These files contain instructions that agents automatically receive when they start inside that workspace". Também: "Since Claude Code only understands CLAUDE.md while most other agents have standardized on AGENTS.md, Maestri includes an option to keep both files in sync automatically. Enable it in the workspace settings if you run mixed agent setups." A doc não diz em que caminho esses arquivos ficam.

**Variáveis exportadas.**
- Doc de Environments (terminais remotos): "Remote shells receive values including:" `MAESTRI_TERMINAL_ID=<terminal-uuid>`, `MAESTRI_HOST=<bridge-endpoint>`, `MAESTRI_TOKEN=<per-terminal-secret>`, `MAESTRI_CLI=<remote-cli-path>`; e "Overrides cannot replace HOME, PATH, or any MAESTRI_ value." (https://themaestri.app/en/docs/environments)
- Terminal local, observado no ambiente deste terminal (`env`, token omitido): `MAESTRI_WORKSPACE_ID`, `MAESTRI_CLI`, `MAESTRI_DATA_DIR=C:\Users\gustavo.delfino\.maestri`, `MAESTRI_PIPE=\\.\pipe\maestri-...`, `MAESTRI_TERMINAL_ID`. Doc de Environments: "Local terminals use the Unix socket created by Maestri, so they do not need the TCP Bridge Port. The Maestri CLI and Skills are installed locally by the app." A doc lida não descreve `MAESTRI_DATA_DIR`, `MAESTRI_PIPE` nem `MAESTRI_WORKSPACE_ID`.
- Skill `maestri`: "If `maestri` is not found, use `"$MAESTRI_CLI"` instead; this environment variable always points to the full binary path." (`~/.claude/skills/maestri/SKILL.md`)
- Rotinas, só para `--pre-run`: "Available env vars: `$MAESTRI_WORKSPACE_NAME`, `$MAESTRI_WORKSPACE_DIR`, `$MAESTRI_ROUTINE_NAME`, `$MAESTRI_TERMINAL_NAME`." (`~/.claude/skills/maestri-routines/SKILL.md`)
- Hooks de floor: `$MAESTRI_FLOOR_NAME`, `$MAESTRI_BRANCH_NAME`, `$MAESTRI_FLOOR_PATH`, `$MAESTRI_ROOT_PATH`, `$MAESTRI_PROJECT_NAME` (https://themaestri.app/en/docs/floors).

**Skills e CLI instalados.**
- Doc de Environments: "Skills are installed per distribution, under Settings > Agents > Skills." (WSL); remoto: "Installs the Maestri CLI wrapper and enabled Skills."; "The default remote CLI path is: ~/.maestri/bin/maestri".
- Evidência local (diretórios listados): `C:\Users\gustavo.delfino\.claude\skills\` e `C:\Users\gustavo.delfino\.agents\skills\` contêm ambos `maestri`, `maestri-chat`, `maestri-manager`, `maestri-portal`, `maestri-portal-devices`, `maestri-routines`, `maestri-workspace` (datados de 9/out). A doc lida não nomeia esses dois caminhos; a instalação nos dois é fato local.
- CLI local: `C:\Users\gustavo.delfino\AppData\Local\Programs\Maestri\resources\cli\maestri.exe` (valor de `MAESTRI_CLI`), no PATH.
- Comandos de papel, recruit e workspace são "(Maestro only)" em `maestri help`.

### 2. Workspace com papel

**Onde o agente abre.** `maestri-manager/SKILL.md`: "--role — name of an existing role preset. The recruit is launched in `.maestri/roles/<id>/` so the role's prompt becomes its starting context." Doc de Environments: "Assigned roles are installed inside the effective project directory: <project>/.maestri/roles/<role-id>/".

**Mecanismo.** Doc de Terminals: "Roles work by starting the agent in a project subdirectory with its own CLAUDE.md / AGENTS.md, so each agent can have unique instructions. Alongside those, Maestri writes a portable role.json sidecar that describes the role — name, badge color, and prompt — so a role travels with the directory across workspaces and across machines." Também: "When a role is assigned, Maestri automatically injects those instructions when the agent starts".

**Conteúdo observado** em `C:\Projetos\context-hub\.maestri\roles\` (5 pastas, nome = UUID do papel; `.maestri` contém só `roles`):
- Cada pasta tem exatamente `AGENTS.md`, `CLAUDE.md`, `role.json`.
- `CLAUDE.md` e `AGENTS.md` são idênticos nas 5 (`cmp`).
- Estrutura do CLAUDE.md gerado (prompt omitido): um bloco `<your_assigned_role>` com o prompt do papel e, depois, um bloco `<working_directory>` com o texto: "IMPORTANT: You were started in this directory to receive the above role assignment. The actual project you should be working on is located at: C:\Projetos\context-hub".
- `role.json`: chaves `color`, `icon`, `id`, `name`, `prompt`, `schemaVersion` (valor 1). `icon` = `person.text.rectangle`; `id` em maiúsculas, igual ao nome da pasta em minúsculas.
- O CLAUDE.md do papel não importa nem menciona o AGENTS.md da raiz do projeto; só traz o prompt e aponta o diretório do projeto.

Consequência: o diretório de trabalho do agente com papel é `...\.maestri\roles\<id>\`, não a raiz do workspace. O `AGENTS.md` do hub (na raiz) fica três níveis acima (`<id>` → `roles` → `.maestri` → raiz).

### 3. Claude Code: AGENTS.md acima, com CLAUDE.md na pasta do papel

Fonte: https://code.claude.com/docs/en/memory.md (curl, 2026-10-10).

Seção "How CLAUDE.md files load": "Claude Code loads `CLAUDE.md` and `CLAUDE.local.md` from your current working directory and every directory above it."

Seção "AGENTS.md", tabela do que se lê por padrão:
- "An `AGENTS.md`, and no `CLAUDE.md` or `CLAUDE.local.md` in your working directory or above it | Your `AGENTS.md`"
- "An `AGENTS.md` and a `CLAUDE.md` or `CLAUDE.local.md` in your working directory or above it | Your `CLAUDE.md` files only"

Seção "When Claude Code reads AGENTS.md": "By default, Claude reads `AGENTS.md` only when you have no `CLAUDE.md` in your working directory or above it." Contam: "a `CLAUDE.md`, `.claude/CLAUDE.md`, or `CLAUDE.local.md` in your working directory or any directory above it". Não contam: "your `~/.claude/CLAUDE.md`, your organization's managed `CLAUDE.md`, and `.claude/rules/` files". Carregamento: "At session start: every `AGENTS.md` and `.claude/AGENTS.md` in your working directory and the directories above it."

Resposta pela doc, no padrão: com o CLAUDE.md gerado na pasta do papel, o `AGENTS.md` da raiz do hub não é lido (só os CLAUDE.md). O `~/.claude/CLAUDE.md` global não conta nessa verificação.

Seção "Choose which instruction files load" ("type `/config` ... set **Project instructions** to one of these values"):
- `claude-md-or-agents-md`: "Your `CLAUDE.md` files, or your `AGENTS.md` files when you have no `CLAUDE.md` or `CLAUDE.local.md` in your working directory or above it. This is the default"
- `claude-md-and-agents-md`: "Your `CLAUDE.md` and `AGENTS.md` files together, each directory's `CLAUDE.md` files first and its `AGENTS.md` after them. Claude Code skips an `AGENTS.md` it has already loaded, so one that your `CLAUDE.md` imports or symlinks to isn't read twice"
- Via settings: `pluginConfigs` → `cc-plugin-agents-md@builtin` → `"options": { "instructionFiles": "claude-md-and-agents-md" }`, lido de `~/.claude/settings.json`, `--settings` ou managed settings, "and ignores it in project and local settings files."
- Também: "To keep your `CLAUDE.local.md` and still have Claude read `AGENTS.md`, set **Project instructions** to `claude-md-and-agents-md`."

Resposta pela doc, com `claude-md-and-agents-md`: lê CLAUDE.md e AGENTS.md "together", e a frase de carregamento cobre "the directories above it". A doc não escreve a combinação exata "opção ligada + AGENTS.md três níveis acima do cwd" (ver Precisa de teste).

Alternativa documentada: "A `CLAUDE.md` that already imports `AGENTS.md` | Your `CLAUDE.md`, with `AGENTS.md` included through the import"; "putting an `@AGENTS.md` import in a `CLAUDE.md` next to it". Requisito: "Reading `AGENTS.md` directly requires Claude Code v2.1.277 or later."

### 4. Onde ficam papéis, presets, partituras e equipes

**Papéis (biblioteca).**
- Doc de Terminals: "Go to Settings → Agents to create, edit, and organize roles. Each role has a name, a color badge, and a set of instructions."
- Escopo: `maestri role create ... [--scope current|global]`; "Roles belong to this workspace unless created with --scope global, which makes them reusable everywhere." (`maestri role --help`); "You can only scope roles to your own workspace, never to a different one." (maestri-manager).
- Arquivo local: `C:\Users\gustavo.delfino\.maestri\preferences.json`, em `payload.rolePresets` (objetos com `color`, `icon`, `id`, `name`, `prompt`, `workspaceId`). Observado: 41 papéis, todos com `workspaceId`. Papel global não foi observado; a hipótese "global = sem workspaceId" não está na doc.
- Cópia por projeto: `<workspace>/.maestri/roles/<id>/` (item 2). Doc de Environments: "Role installation, updates, cleanup, and terminal restart work for every environment."

**Ler papéis de uma pasta.** Doc de Terminals, "Discovering roles in your repo": "the Discover Roles button scans the working directory for role.json files and lets you import them. You see a preview of each discovered role and can multi-select which ones to add to your library — handy when checking out a teammate's branch that ships its own .maestri folder." É importação manual para a biblioteca, a partir do "working directory"; a doc não diz que dê para escolher outra pasta nem que seja leitura contínua.

**Presets (agentes).** Doc de Terminals: "An agent preset in Settings → Terminal → Quick Start carries the same fields: icon, accent color, terminal theme, and font." Local: `preferences.json` → `payload.agentPresets`. `maestri preset list` só lista. A doc não descreve pasta de presets nem escopo por workspace.

**Partituras.** Doc de Partituras: "Each one is a single JSON file under `~/.maestri/partituras/`, and it's the same document you get when you export or share one. Plain text you can read and diff, with no database in the way." Escopo: "Every partitura is either Global, meaning it shows up in every workspace, or scoped to a single workspace." Compartilhar: arquivos `.maestripartitura` e pacote `.maestripartituras`; "Import Partituras…" e "double-click a partitura file in Finder or drop it onto the canvas — both send it to your library". É cópia para a biblioteca, não leitura de pasta escolhida. Os papéis vão embutidos: "The role presets your terminals reference are embedded in the partitura itself". Local: `C:\Users\gustavo.delfino\.maestri\partituras\` existe, com um arquivo `.maestripartitura`.

**Equipes.** A doc lida não tem "equipe/team" como objeto salvo. A equipe é a árvore de recrutas de um terminal Maestro (Maestro Mode: Recruit, Connect, Dismiss); o que se salva de um arranjo é a partitura ("terminals with their agents and roles, notes, portals, file trees, drawings, groups, and every connection between them").

**Estado geral.** `C:\Users\gustavo.delfino\.maestri\` (observado): `app-state.json`, `backups`, `chats`, `git-hosts`, `license.json`, `manifest.json`, `partituras`, `preferences.json`, `routines.json`, `usage`, `workspaces` (cada um com `workspace.json`, `files`, `notes`, `snapshots`, `terminals`), entre outros. A doc cita ainda `~/.maestri/terminal/themes/`, `~/.maestri/usage/providers/`, `~/.maestri/git-hosts/providers/` e `~/.maestri/bin/maestri` (remoto).

**Padronização do Maestri em `agents/` do hub.** A doc lida não oferece configuração para apontar a biblioteca de papéis, presets ou partituras a uma pasta escolhida. O que existe: (a) `<workspace>/.maestri/roles/<id>/` por workspace, gravado pelo Maestri; (b) Discover Roles, que importa `role.json` achados no working directory do terminal; (c) importar/exportar `.maestripartitura(s)`; (d) `MAESTRI_DATA_DIR` no ambiente, sem doc.

## Não verificado

- Em que caminho o Maestri grava o CLAUDE.md/AGENTS.md "do workspace" (tela de edição do workspace) e o que é injetado num terminal sem papel.
- O significado de `MAESTRI_DATA_DIR`, `MAESTRI_PIPE`, `MAESTRI_WORKSPACE_ID`, e se `MAESTRI_DATA_DIR` pode ser trocado para mudar a pasta de dados (aparece no ambiente; a doc lida não o menciona).
- Como o papel global é gravado em `preferences.json` (nenhum observado).
- Se o app instala skills em `~/.claude/skills` e `~/.agents/skills` por regra documentada: a doc diz só "Settings > Agents > Skills" e "configured remote Skill roots"; os dois caminhos locais são fato observado.
- Se Discover Roles aceita pasta diferente do working directory do terminal.
- Se existe pasta de presets ou de papéis configurável em Settings (a interface não foi aberta).
- A versão `pt-br` da doc do Maestri não foi cotejada com a inglesa.

## Precisa de teste

- Com o CLAUDE.md gerado na pasta do papel, `/memory` lista o `AGENTS.md` da raiz do hub? (a doc diz que não, no padrão).
- Com `instructionFiles: "claude-md-and-agents-md"` em `~/.claude/settings.json`, o `AGENTS.md` da raiz (três níveis acima do cwd do papel) é carregado, e em que ordem em relação ao CLAUDE.md do papel e ao `~/.claude/CLAUDE.md`?
- Se o Maestri regenera CLAUDE.md/AGENTS.md do papel a cada início de terminal (qualquer ajuste manual se perderia).
- Se um `@../../../AGENTS.md` no prompt do papel sobrevive à geração e é resolvido pelo Claude Code.
- Se a opção de manter CLAUDE.md e AGENTS.md em sincronia atua nas pastas de papel ou só na raiz.
- Se Discover Roles importa `role.json` de `agents/roles/` do hub quando o working directory do terminal é a raiz do hub.
- Quais `MAESTRI_*` o terminal enxerga sem papel versus com papel no Windows.

## Fontes

Documentação oficial do Maestri (curl, 2026-10-10):
- https://themaestri.app/en/docs/workspaces
- https://themaestri.app/en/docs/terminals
- https://themaestri.app/en/docs/maestro
- https://themaestri.app/en/docs/partituras
- https://themaestri.app/en/docs/environments
- https://themaestri.app/en/docs/floors

Documentação do Claude Code:
- https://code.claude.com/docs/en/memory.md (seções "How CLAUDE.md files load", "AGENTS.md", "When Claude Code reads AGENTS.md", "Choose which instruction files load")

Arquivos locais:
- `C:\Users\gustavo.delfino\.claude\skills\maestri\SKILL.md`, `maestri-manager\SKILL.md`, `maestri-routines\SKILL.md`, `maestri-workspace\SKILL.md`
- `C:\Users\gustavo.delfino\.maestri\workspaces\271fe5c6-f63d-41e9-85d9-75981ab3dbce\workspace.json` (só `name` e `workingDirectory`)
- `C:\Users\gustavo.delfino\.maestri\preferences.json` (só a estrutura de `payload.rolePresets` e `agentPresets`; prompts não copiados)
- `C:\Projetos\context-hub\.maestri\roles\*\{CLAUDE.md,AGENTS.md,role.json}` (estrutura e texto gerado pelo Maestri)
- `maestri help`, `maestri recruit --help`, `maestri role --help`, `maestri preset --help`
- Ambiente do terminal (`env` filtrado por `maestri`, token omitido)
