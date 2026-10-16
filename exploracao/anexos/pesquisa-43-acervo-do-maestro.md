# Pesquisa 43: acervo do maestro

Pesquisa em fonte primária, só leitura. Data: 2026-10-12. Ticket: `.scratch/context-hub/issues/43-acervo-do-maestro-pesquisa.md`.
Executado só: `curl` das 22 páginas da doc do Maestri, `maestri help`, `maestri <comando> --help` de todos os
comandos, `maestri list`, `preset list`, `role list`, `routine list`, `workspace list`, `floor list`; leitura das
skills `maestri*` instaladas; leitura do código empacotado do app instalado (`resources/app.asar`, build 87,
`sha 9a4e3e5e`, 2026-10-11), extraído para o scratchpad e lido como texto, sem executar. Nenhum workspace, papel,
nota, rotina, floor ou configuração foi criado ou alterado. Prompts de papéis e dados de cliente não foram
copiados (só nomes).

Complementa, sem repetir, `exploracao/anexos/pesquisa-37-portas/porta-3-4-maestri.md` e os comentários de
"Maestri: padrão e liberdade" (ticket 40).

Convenção: **"a fonte diz"** é citação de doc, `--help`, skill oficial ou código do app; **"sugestão"** é
proposta desta pesquisa. "Código do app" quer dizer o bundle `out/main/index.js` ou o renderer
`out/renderer/assets/*.js` dentro de `C:\Users\gustavo.delfino\AppData\Local\Programs\Maestri\resources\app.asar`.
O código diz o que o build 87 faz no Windows; a doc pode descrever outra versão ou o Mac.

## Pergunta

1. Que outros tipos de peça cabem no acervo, além de papéis, setups e contratos-opção? Para cada um: o que a
   fonte diz do recurso, o que a peça guardaria, com que comando o maestro a usa, e se dá para personalizar por
   workspace.
2. Como a família oficial `maestri-*` se organiza, como modelo para o acervo, sem colidir com os nomes dela.
3. O que a fonte diz do CLAUDE.md/AGENTS.md "do workspace" (onde fica, o que chega a um terminal com e sem
   papel), e que mecanismo leva uma "primeira instrução" a todo workspace novo, inclusive fora do hub.

## Achados que mudam o desenho

- **O maestro não tem comando para partituras nem para hooks de floor.** `maestri help` não lista nenhum dos
  dois, e a palavra "partitura" não aparece no binário `resources\cli\maestri.exe`. Partitura só se aplica pela
  interface ou pela API Wire (`POST /api/workspaces/{ws}/partituras`, "the host fills the terminals and adopts
  the embedded roles"; https://themaestri.app/en/docs/wire). Logo, um setup do acervo que o maestro monte
  sozinho precisa ser receita de comandos (`recruit`, `role`, `connect`, `note`, `routine`, `floor`), não
  partitura.
- **Papel global = papel sem `workspaceId`.** Wire: "`workspaceId` marks the ones scoped to one workspace
  (absent means global)". Resolve um "não verificado" da porta 3-4. Hoje os 41 papéis são de workspace; `maestri
  role list` no Context Hub mostra só "Current workspace" (5 papéis de debate), nenhum global.
- **O CLAUDE.md/AGENTS.md "do workspace" são os arquivos da pasta de trabalho do workspace.** O código grava em
  `join(workingDirectory, "CLAUDE.md" | "AGENTS.md")`, e a interface diz "Edit {{file}} in the workspace folder.
  Saving writes this file only." O Maestri não injeta nada: quem lê é o próprio agente (detalhes na seção
  própria).
- **A "sincronia" CLAUDE.md/AGENTS.md é um botão de cópia, não automática, neste build.** Interface: "Syncing
  makes one file a copy of the other. Choose which version both files should keep." A doc diz "keep both files
  in sync automatically"; o código do build 87 não guarda opção nenhuma (precisa de teste se há outro gatilho).
- **O app reescreve só sete pastas de skill, por nome fixo.** Código: lista `["maestri","maestri-portal",
  "maestri-portal-devices","maestri-manager","maestri-routines","maestri-workspace","maestri-chat"]`; grava
  `<base>/<nome>/SKILL.md` em cada "skill base" ligada, e a remoção apaga a pasta inteira desses nomes. As bases
  padrão são `.claude/skills`, `.agents/skills`, `.hermes/skills` e `.gemini/config/skills`. Um acervo com
  outro nome não colide.

## Tipos de peça candidatos

Cada bloco: **A fonte diz** (recurso), **Peça guardaria**, **Como o maestro usa**, **Personalização por
workspace**. Os três tipos já confirmados (papéis, setups, contratos-opção) não são repetidos, só citados quando
uma peça nova se encaixa neles.

### 1. Preset de agente (receita de lançamento)

**A fonte diz.**
- Doc Terminals: "An agent preset in Settings → Terminal → Quick Start carries the same fields: icon, accent
  color, terminal theme, and font. Every way of creating an agent honors them — [...] a teammate a Maestro
  recruits". Doc Chat: "Set it on an agent preset and every terminal you create from that preset opens in chat."
- Wire: `GET /api/agent-presets` lista `{id, name, agentType, icon, isManager, isDefault, command?, accountId?,
  accountName?}`; "Editing a preset changes later creations, never terminals already using it."
- `maestri preset list` (só Maestro) imprime os nomes aceitos por `--preset`; hoje: "Claude Code", "Codex",
  "Antigravity", "OpenCode", "Shell". Não há comando para criar ou editar preset.
- Arquivo local `~/.maestri/preferences.json` → `payload.agentPresets`: campos `command`, `agentType`,
  `maestroMode`, `startInChatMode`, `icon` (ex.: Codex com `command: "codex --no-daemon"`).
- `maestri recruit --help`: `--command C` sobrepõe o comando; a skill diz "Almost never needed; use the preset."

**Peça guardaria (sugestão).** A linha de comando de cada preset que o Gustavo quer ter (por exemplo um Claude
Code com `--model` fixo, um Codex com `--profile`, um "Maestro" com `maestroMode` ligado), mais conta fixada e
modo chat. É o elo entre o contrato de roteamento de modelos e o `recruit`.

**Como o maestro usa.** `maestri preset list` para saber o que existe; `maestri recruit "Nome" --preset P`; quando
o preset não existe, `--command "..."` com a linha do acervo. Criar o preset é tarefa do Gustavo na interface
(Settings → Terminal → Quick Start).

**Personalização.** O preset é da máquina, sem escopo de workspace (a doc e a Wire não citam escopo). A
variação por workspace fica no setup (`--command`, `--account`).

### 2. Conta (identidade por agente)

**A fonte diz.** Doc Terminals, Accounts: "Run Claude Code and Codex from different accounts side by side";
"pin one in a preset"; "A change takes effect at the terminal's next launch"; "Only the login is separate.
Sessions, settings, skills, instructions, plugins and hooks are shared". `maestri recruit --help`: "--account
runs the teammate on one of its CLI's accounts [...] It wins over an account the preset pins". Contas com API
key aceitam "an optional API Endpoint".

**Peça guardaria (sugestão).** Não é peça própria: é um campo dos contratos de roteamento e dos setups (qual
conta para qual tipo de tarefa). O campo "API Endpoint" de uma conta por API key é um caminho documentado para
apontar Claude Code ou Codex a outro endpoint; se serve ao gateway FreeLLMAPI é **precisa de teste**.

**Como o maestro usa.** `maestri preset list` (mostra as contas), `recruit --account A`, `recruit --replace
"X" --account A`.

**Personalização.** Por recruta, a cada `recruit`.

### 3. Nota-modelo e quadro de fichários

**A fonte diz.**
- `maestri note create ["content"] [--name "Name"] [--stack ["Fichário"]]`; `note stack`, `note edit`,
  `note write` (`maestri note --help`). `--name` "pins a stable name".
- Doc Notes: notas são "real markdown files saved to disk"; "Lock Contents [...] connected agents are refused:
  they still read the note, but every attempt to write to it fails" ("the way to hand an agent a spec it must
  follow"); "Move to..." grava a nota num caminho escolhido; arquivos `.md` soltos no canvas ficam "at their
  original location".
- Doc Fichários: "Name a few Fichários for the stages you care about — Backlog, Building, Review, Shipped — and
  they hold their place as empty folders waiting for work".
- Doc Maestro: "write the brief once into a note connected to the Maestro, then ask the Maestro to connect that
  note to whichever recruits need it". `maestri connect "nota" "Recruta"`.
- A CLI não tem comando de travar nota nem de escolher o caminho da nota (só interface; a Wire tem
  `PUT …/nodes/{id}/note/lock`).

**Peça guardaria (sugestão).** Modelos de nota com marcadores a preencher: brief de tarefa, "Rodada atual" de
grilling, nota de handoff, quadro de fichários por etapas, nota de "spec travada". O setup cita a nota-modelo
pelo nome.

**Como o maestro usa.** Lê o modelo na skill do acervo, preenche, `note create --name ... --stack ...`,
`connect` aos recrutas. Travar fica com o Gustavo.

**Personalização.** Total: o maestro preenche o modelo para o workspace.

### 4. Rotina-modelo

**A fonte diz.** `maestri routine create "Name" --command "..." <schedule>` com `--every`, `--daily`,
`--weekly`, `--once`, `--terminal`, `--reminder`, `--count`, `--until`, `--pre-run`, `--no-notify`,
`--disabled`; "--pre-run output is inserted where the command contains the {{output}} placeholder"
(`maestri routine --help`). Skill `maestri-routines`: "You can only see and manage routines in the current
workspace"; variáveis do pre-run: `$MAESTRI_WORKSPACE_NAME`, `$MAESTRI_WORKSPACE_DIR`, `$MAESTRI_ROUTINE_NAME`,
`$MAESTRI_TERMINAL_NAME`. Doc Routines: encadeamento com `&&` em linha própria. Wire: rotinas guardam
`schedule`, `endRepeat`, `skipIfBusy`, `preRunScript`.

**Peça guardaria (sugestão).** Rotinas parametrizadas: "auto-checagem a cada hora", "resumo diário com
`git log` no pre-run", "lembrete de standup", "vigiar dashboard num portal". Cada uma com nome, comando com
`{{output}}`, agenda e alvo.

**Como o maestro usa.** `maestri routine create ...` a partir do modelo; `routine list/show` para conferir.

**Personalização.** Por workspace, porque a rotina é do workspace.

### 5. Receita de floor e hooks de floor

**A fonte diz.**
- `maestri floor create "Name" [--branch B] [--existing-branch] [--copy] [--no-git] [--copy-ground]` e
  `--pull-request`; `floor status` com `--state working|blocked|review|done` e `--progress`; `land`/`delete`
  só do Ground (`maestri floor --help`).
- Skill `maestri-manager`, "Isolated-experiment flow" e "Floor status": criar floor, recrutar com `--floor`,
  pedir `floor status` e o "ask back".
- Doc Floors, Hooks: "Setup: runs when a floor is created [...] Run: runs when you click the play button [...]
  Teardown: runs when a floor is deleted", com `$MAESTRI_FLOOR_NAME`, `$MAESTRI_BRANCH_NAME`,
  `$MAESTRI_FLOOR_PATH`, `$MAESTRI_ROOT_PATH`, `$MAESTRI_PROJECT_NAME`. Configuração: "right-click the floor
  button in the canvas and select Configure Hooks…". Wire: hooks são do workspace (`GET/PUT
  /api/workspaces/{ws}/hooks`, owner-only).
- Windows: "Copy-on-write [...] Windows: Not available. The floor is a plain checkout"; "Use a setup hook to
  install dependencies on those floors."
- A CLI não tem comando de hooks.

**Peça guardaria (sugestão).** Receitas de floor por tipo de trabalho (experimento, revisão de PR, iniciativa
com branch) e os comandos de hook de setup que cada tipo de repositório pede no Windows.

**Como o maestro usa.** `floor create` + `recruit --floor`; os hooks o Gustavo cola na interface (ou um
script pela Wire, ver item 12).

**Personalização.** Por workspace (hooks e floors são do workspace).

### 6. Workspace-modelo (clonar um workspace)

**A fonte diz.** `maestri workspace create "Name" --dir PATH [--from "Source"] [--group] [--folder]`;
"--from clones an existing workspace's layout, agents, and connections, then retargets the copy at the new
directory" (`maestri workspace --help`). Skill `maestri-workspace`: "The user's 'template' is just a normal
workspace — suggest they keep one laid out the way they like and clone it by name". Doc Environments:
"Programmatically provisioned workspaces inherit the requesting workspace environment."

**Peça guardaria (sugestão).** Uma lista de workspaces-modelo vivos no Maestri ("Modelo iniciativa", "Modelo
código") com o que cada um traz, e o contrato-opção "onde abrir o workspace" (pasta, grupo, pasta da
barra lateral). O acervo guarda o texto; o modelo em si vive no Maestri de cada máquina.

**Como o maestro usa.** `maestri workspace list`, `workspace create ... --from "Modelo X"`.

**Personalização.** O clone nasce igual ao modelo e depois diverge. Se o clone copia os arquivos
CLAUDE.md/AGENTS.md da pasta do modelo: **precisa de teste** (o código trata esses arquivos como da pasta, não
do workspace, então a expectativa é que não copie).

### 7. Partitura (setup visual, para o Gustavo)

**A fonte diz.** Doc Partituras: "a saved arrangement of your canvas: terminals with their agents and roles,
notes, portals, file trees, drawings, groups, and every connection between them"; "The role presets your
terminals reference are embedded in the partitura itself"; removidos ao salvar: "Absolute filesystem paths",
"SSH, Docker, Sandbox, and custom runtime configs, plus environment overrides"; "Every partitura is either
Global [...] or scoped to a single workspace"; "Each one is a single JSON file under `~/.maestri/partituras/`";
importação por "Import Partituras…" ou arquivo `.maestripartitura`. Mescla de papéis: "A role whose name matches
one of yours reuses your definition". Wire: formato 2 pode embutir histórico de chat ("Include chat history,
off by default"). A CLI não tem comando de partitura.

**Peça guardaria (sugestão).** A versão visual de um setup já testado, exportada como `.maestripartitura`, para
o Gustavo importar à mão em outra máquina. Não substitui o setup em texto, porque o maestro não a aplica.

**Como o maestro usa.** Não usa pela CLI. Pode indicar ao Gustavo qual partitura importar.

**Personalização.** Pouca: escopo global ou de um workspace; caminhos se refazem no destino ("Paths are refilled
from the destination").

### 8. Receita de portal (QA visual, painéis a vigiar)

**A fonte diz.** `maestri portal create URL ["Name"] [--size WxH]`, `portal resize`, `portal ua [preset]`
(ios, android, chrome, edge, firefox, desktop), `logs-start`/`logs`, `snapshot`, `screenshot`
(`maestri portal --help`). Doc Portals: "Each portal runs an isolated WebKit (Safari) instance with its own
storage"; "you can have multiple logged-in sessions to the same service simultaneously". Doc Routines: "Connect
an agent to a browser portal and schedule it to check a dashboard".

**Peça guardaria (sugestão).** Conjuntos de tamanhos de tela para QA, sequência padrão (snapshot → ação →
screenshot → logs), e os painéis que cada tipo de workspace costuma abrir.

**Como o maestro usa.** `portal create`, `connect "Recruta" "Portal"`, e o papel do recruta cita o portal (a
skill manda: "name it and tell the recruit to drive it with `maestri portal ...`").

**Personalização.** URLs e tamanhos por workspace.

### 9. Ambiente de execução (Local, tmux, WSL, SSH, Docker)

**A fonte diz.** Doc Environments: "A workspace can run locally, on an SSH server, inside a Docker container,
inside a Docker Sandbox, or through a compatible custom command-line runtime"; WSL é "Windows only"; "Recruited
agents inherit the manager terminal environment when appropriate"; um terminal pode sobrepor o ambiente do
workspace ("Workspace Default, Local, or another enabled environment"). Partituras descartam essas configurações.
A CLI não tem flag de ambiente (`recruit --workspace W` leva o recruta a rodar "where that workspace runs").

**Peça guardaria (sugestão).** O ambiente indicado por tipo de workspace (ex.: WSL com distro e usuário para
trabalho Linux), como campo do setup e do contrato "onde abrir".

**Como o maestro usa.** Indiretamente: recruta no workspace certo (`--workspace`), já que não escolhe ambiente.

**Personalização.** Por workspace e por terminal, na interface.

### 10. Protocolo de condução (como orquestrar recrutas)

**A fonte diz.** Skill `maestri-manager`: "Reuse before recruiting", "Invent the name yourself", "Bake
collaboration discoverability into the prompt" (mandar o recruta rodar `maestri list`, nomear o par, a nota e o
portal), fluxo de 6 passos; skill `maestri`: o "ask back approach" e `ask --batch`; `maestri ask --help`:
"If the timeout expires, do NOT re-send the prompt".

**Peça guardaria (sugestão).** Já é o tipo 3 (contrato-opção de orquestração). O achado é de forma: a skill
oficial já cobre a mecânica; a peça do acervo só deve guardar as escolhas do Gustavo (quando recrutar, quando
usar floor, como reportar, quem revisa quem), citando a skill oficial em vez de repeti-la.

**Personalização.** Por setup.

### 11. Provedor de máquina (uso, git host) e tema

**A fonte diz.** Doc Terminals: "Each provider is one JSON file in `~/.maestri/usage/providers/` [...] Maestri
writes an `AGENTS.md` guide next to them"; "Turning Agent Usage off deletes the whole providers folder". Doc
Floors: provedores de git host em `~/.maestri/git-hosts/providers/`, exemplo de "A second GitHub account"; "A
provider file is a program that runs with your permissions." Temas: "Drop any Ghostty-format theme file into
`~/.maestri/terminal/themes/`".

**Peça guardaria (sugestão).** Configuração da máquina, não do maestro: os arquivos de provedor que as duas
máquinas devem ter iguais. Cabe no kit de par, não no acervo do maestro.

**Personalização.** Não há escopo de workspace.

### 12. Receita pela API Wire (o que a CLI não faz)

**A fonte diz.** Doc Wire: "open to anything you build: a script that pings you when an agent needs attention,
a button that approves a prompt, a small dashboard"; pareamento com código de seis dígitos e "a long-lived device
token"; papel `owner` ou `guest`; rotas para partituras, hooks de floor, rotinas, trava de nota, papéis
(`PUT /api/roles/{id}`: "a changed prompt restarts every running terminal holding the role"). "Maestri Wire is in
beta".

**Peça guardaria (sugestão, com cautela).** Scripts para o que o maestro não alcança pela CLI: aplicar uma
partitura, gravar hooks de floor, travar a nota de spec. Exige um token de dispositivo com controle total
guardado em algum lugar, o que é decisão de segurança à parte. Não recomendo para o primeiro lote.

### 13. Peças dos harnesses (Claude Code, Codex, Copilot)

Levantado por um subagente desta pesquisa, com `curl` das páginas brutas (lista em Fontes); três citações
foram reconferidas no texto baixado. Os mesmos recursos existem nos três harnesses com nomes diferentes, então
cada bloco abaixo vira, no acervo, **uma peça neutra com uma tradução por harness**.

#### 13a. Subagente / agente customizado (papel que roda dentro de um terminal)

**A fonte diz.**
- Claude Code: "Each subagent runs in its own context window with a custom system prompt, specific tool access,
  and independent permissions." Moram em `.claude/agents/` (projeto) e `~/.claude/agents/` (usuário); campos
  `name`, `description`, `tools`, `model`, `skills`, `initialPrompt` e outros; "When multiple subagents share the
  same name, Claude Code uses the one from the higher-priority location" (projeto vence usuário); também
  `claude --agents '{...}'`, que "exist only for that session and aren't saved to disk", e `claude --agent
  <name>` para a sessão inteira (https://code.claude.com/docs/en/sub-agents.md).
- Codex: "add standalone TOML files under `~/.codex/agents/` for personal agents or `.codex/agents/` for
  project-scoped agents", com `name`, `description`, `developer_instructions`, `model`
  (https://learn.chatgpt.com/docs/agent-configuration/subagents.md).
- Copilot CLI: arquivo `.agent.md` em `.github/agents/` ou `~/.copilot/agents/`; "If personal and repository
  custom agents have the same ID, the personal agent is used"; `copilot --agent <id>`
  (https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/create-custom-agents-for-cli).

**Peça guardaria (sugestão).** Ajudantes que não merecem um terminal no canvas (revisor rápido, pesquisador de
fonte primária, verificador de citações). Um papel do Maestri custa um terminal e uma sessão; um subagente roda
dentro do recruta.

**Como o maestro usa.** Escreve no papel ou no `ask` do recruta "delegue a verificação ao subagente X"; ou
recruta com `--command "claude --agent X"` (precisa de teste dentro do Maestri).

**Personalização.** Claude Code e Codex aceitam versão de projeto; no Claude Code a do projeto vence, no
Copilot vence a do usuário.

#### 13b. Perfil de modelo (a parte executável do contrato de roteamento)

**A fonte diz.**
- Claude Code: `--model` "Overrides the `model` setting and `ANTHROPIC_MODEL`"; alias `opusplan` "uses `opus`
  during plan mode, then switches to `sonnet` for execution"; `--settings` aceita arquivo ou JSON e "override the
  same keys in your `settings.json` files for this session"; `ANTHROPIC_BASE_URL`: "Override the API endpoint to
  route requests through a proxy or gateway" (https://code.claude.com/docs/en/cli-reference.md,
  https://code.claude.com/docs/en/model-config.md, https://code.claude.com/docs/en/env-vars.md).
- Codex: "When you pass `--profile profile-name`, Codex loads `~/.codex/config.toml`, then overlays
  `~/.codex/profile-name.config.toml`"; provedor próprio com `[model_providers.<id>]` e `base_url`; o
  `.codex/config.toml` de projeto ignora `model_provider`, `model_providers` e `profile`
  (https://learn.chatgpt.com/docs/config-file/config-advanced.md).
- Copilot CLI: "Use `--model=MODEL` or the `COPILOT_MODEL` environment variable"; BYOK com
  `COPILOT_PROVIDER_BASE_URL` para "OpenAI-compatible endpoints [...] including locally running models such as
  Ollama" (https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/use-byok-models).

**Peça guardaria (sugestão).** Para cada linha do contrato de roteamento (tarefa pesada, simples, pesquisa,
revisão), a linha de comando por harness: `claude --model ... --settings <arquivo>`, `codex --profile ...`,
`copilot --model ...`, e a variante que aponta ao FreeLLMAPI. Se o FreeLLMAPI fala o formato que cada harness
espera (Anthropic `/v1/messages` para o Claude Code; Responses para o Codex): **precisa de teste**.

**Como o maestro usa.** `recruit --preset P --command "<linha do perfil>"` ou um preset criado com essa linha
(item 1).

**Personalização.** Por recruta, na linha de comando.

#### 13c. Hook de início de sessão (injetar contexto)

**A fonte diz.** Claude Code: `SessionStart` com `additionalContext`, "String added to Claude's context at the
start of the conversation, before the first prompt", "capped at 10,000 characters"; configurável em
`~/.claude/settings.json` (https://code.claude.com/docs/en/hooks.md). Codex: "That `additionalContext` text is
added as extra developer context"; hooks em `~/.codex/hooks.json` ou `config.toml`, revisados em `/hooks`
(https://learn.chatgpt.com/docs/hooks.md). Copilot CLI: "Only `additionalContext` is consumed for
`sessionStart`"; hooks em `~/.copilot/hooks/` (https://docs.github.com/en/copilot/reference/hooks-reference).

**Peça guardaria (sugestão).** Um script único que, quando a variável `MAESTRI_TERMINAL_ID` existe (o Maestri a
exporta em todo terminal local, ver código `buildEnv`), devolve como contexto "você está no Maestri; o acervo do
maestro é a skill X". É candidato forte a "primeira instrução" (seção própria).

**Personalização.** O script pode ler `MAESTRI_WORKSPACE_ID` e o diretório e variar a mensagem.

#### 13d. Estilo de saída

**A fonte diz.** "An output style is a set of instructions that sets Claude's role, tone, and response format
for every response in a session"; mora em `~/.claude/output-styles` ou `.claude/output-styles`; "Other
subagents run their own system prompt, so styles don't change how they respond"
(https://code.claude.com/docs/en/output-styles.md). Equivalente em Codex e Copilot: não verificado.

**Peça guardaria (sugestão).** Formatos de resposta por papel (relatório curto, rodada de grilling). Pouco
ganho: só Claude Code, e o papel já carrega o formato. Baixa prioridade.

#### 13e. Skill de procedimento (playbook carregado sob demanda)

**A fonte diz.** Claude Code: "skill descriptions are loaded into context so Claude knows what's available, but
full skill content only loads when invoked"; "Keep `SKILL.md` under 500 lines. Move detailed reference material
to separate files"; "the combined `description` and `when_to_use` text is truncated at 1,536 characters"
(https://code.claude.com/docs/en/skills.md). Codex lê skills de usuário em "`$HOME/.agents/skills`"
(https://learn.chatgpt.com/docs/build-skills.md); Copilot CLI em "`~/.copilot/skills` or `~/.agents/skills`"
(https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-skills). Claude Code não lista
`~/.agents/skills` entre os seus caminhos (skills.md), por isso a junction precisa existir nas duas pastas.

**Peça guardaria (sugestão).** Procedimentos que um recruta segue (rodada de grilling, varredura da §10.4,
revisão cruzada), no formato de arquivo de referência dentro da skill do acervo, para o papel citar pelo nome
em vez de copiar o texto.

#### 13f. Plugin (forma de empacotar)

**A fonte diz.** "A Claude Code plugin is a directory of skills, agents, hooks, MCP servers, or other components
that Claude Code installs and loads as one unit"; escopo User, Project ou Local
(https://code.claude.com/docs/en/plugins/overview.md, https://code.claude.com/docs/en/plugins/install.md).

**Peça guardaria (sugestão).** Não é peça; é uma alternativa de distribuição do acervo inteiro (skill +
subagentes + hook) só para o Claude Code. A junction serve aos três harnesses; o plugin, a um.

#### 13g. Prompt de comando (atalho de barra)

**A fonte diz.** Claude Code: "Custom commands have been merged into skills." Codex: "Custom prompts are
deprecated. Use skills" (https://learn.chatgpt.com/docs/custom-prompts.md). VS Code: "Prompt files are
deprecated for Agent Host sessions" (vscode-docs, prompt-files.md).

**Conclusão.** Não vale como tipo de peça: os três empurram para skills.

## Família `maestri-*` como modelo

### O que existe (fato local e código do app)

| Skill | Tamanho | Descrição que dispara (resumo da frase literal) | Papel na família |
|---|---|---|---|
| `maestri` | 7.087 B, 53 linhas | "Send messages to connected AI agents [...] Also read and write connected sticky notes. [...] Look for actions like 'ask [name] to...'" | base: `list`, `ask`, `check`, notas, "ask back" |
| `maestri-manager` | 18.036 B, 177 linhas | "Create and connect agent terminals [...] manage agent roles, send push notifications. Use when the user asks to assemble a team [...] or to invoke Maestro Mode." | time: `recruit`, `dismiss`, `connect`, `role`, `preset`, `notify` |
| `maestri-workspace` | 14.145 B, 145 linhas | "Create new Maestri workspaces and floors [...] land or delete a floor [...] and whenever you are working on a task on a floor, to keep its status current." | workspaces e floors |
| `maestri-routines` | 4.847 B, 79 linhas | "Manage scheduled routines [...] Use to schedule a command or recurring prompt [...] set a reminder" | rotinas |
| `maestri-portal` | 6.844 B, 120 linhas | "Use a browser portal [...] Use when the user asks to browse a URL, test a web UI" | portal web |
| `maestri-portal-devices` | 4.131 B, 68 linhas | "Drive an Android emulator or physical Android phone [...]" | portal de dispositivo |
| `maestri-chat` | 3.258 B, 64 linhas | "Applies only to messages carrying a Maestri Chat header [...] You MUST read this skill before replying" | face de chat |

Arquivos: `C:\Users\gustavo.delfino\.claude\skills\maestri*\SKILL.md` (iguais em `~/.agents/skills`; `diff -rq`
do `maestri-manager` sem diferença). Datas de 12/out 12:42, ou seja, regravadas na atualização do app.

### Como a família se organiza (a fonte diz)

- **Uma pasta, um arquivo.** Cada skill é só `SKILL.md`, sem `references/` nem scripts. O instalador do app
  escreve exatamente `F(base, nome, "SKILL.md")` para cada nome (função `installSkillsAtPaths`).
- **Frontmatter mínimo:** `name`, `description`, `user-invocable: true`. Nada de `allowed-tools` ou
  `disable-model-invocation`.
- **Divisão por verbo de domínio**, não por papel: falar com agentes (base), montar time, provisionar lugar
  (workspace/floor), agendar, navegar, conversar. Cada descrição começa com o que faz e termina com "Use when
  ..." e exemplos de frase do usuário.
- **Preâmbulo repetido** em todas: "You're running inside Maestri [...] If `maestri` is not found, use
  `"$MAESTRI_CLI"` instead". Cada skill se basta para achar a CLI.
- **Referência cruzada por nome**, sem duplicar: "`maestri ask` (from the base `maestri` skill)", "`maestri
  recruit "Name" --floor "Floor"`, from the maestri-manager skill".
- **Portão de permissão explícito:** "These commands require **Maestro Mode** [...] If a command returns 'This
  terminal is not the Maestro', the user must toggle Maestro on".
- **Seção de segurança** em quem apaga: "`delete` is destructive. Only run it when the user explicitly asks."
- **Ligação com a interface:** o Prompt Composer traduz menções em skills: "@Maestro [...] help the agent load
  the `/maestri-manager` skill" (doc Maestro); a ação New Floor manda `<maestri-create-floor
  skill="maestri-workspace" />` (skill `maestri-workspace`). No renderer, as menções `maestri-manager`,
  `maestri-routines`, `maestri-workspaces` e `maestri-create-floor` têm ícone e rótulo próprios.
- **Instalação nas "skill bases":** código `defaultSkillBases`: `.claude/skills` ("Claude Code"),
  `.agents/skills` ("Agent Skills"), `.hermes/skills` ("Hermes"), `.gemini/config/skills` ("Antigravity"), cada
  uma com `enabled`; a doc diz "Settings > Agents > Skills". `maestri-portal-devices` só entra quando o runtime
  de dispositivos registra o conteúdo (`registerDeviceSkillContent`).
- **Remoção:** `removeSkillsAtPaths` apaga, em cada base, a pasta inteira de cada um dos sete nomes
  (`gt(o,{recursive:!0,force:!0})`). Qualquer arquivo extra posto dentro de uma pasta `maestri-*` oficial se
  perde.

### O que isso diz para o acervo (sugestão)

- **Nome:** qualquer nome fora dos sete fixos não colide. Para não confundir leitor nem um futuro oitavo nome
  oficial, evitar o prefixo `maestri-`; por exemplo `maestro-acervo` (porta de entrada) e, se virar família,
  `maestro-papeis`, `maestro-setups`, `maestro-rotas`.
- **Forma da família oficial com uma diferença:** a oficial cabe em um arquivo porque descreve uma CLI; o acervo
  cresce com o uso (50 setups, como o Gustavo disse). Isso pede o padrão de skill com arquivos de referência
  ("Move detailed reference material to separate files", doc de skills do Claude Code; Codex aceita
  `references/`): um `SKILL.md` curto, que é o catálogo e as regras de uso, e um arquivo por peça.
- **Descrição que dispara:** como a oficial, verbo de domínio + "Use when" com frases do Gustavo ("monte o
  workspace", "recrute um revisor", "qual modelo para isso"). Limite de 1.536 caracteres no Claude Code e 1.024
  no VS Code.
- **Referência cruzada à oficial em vez de cópia:** a peça diz "recrute com `--role` (skill
  `maestri-manager`)", e não reexplica a CLI. Quando o app atualizar a CLI, o acervo não fica velho.
- **Preâmbulo e portão:** repetir o "se não achar `maestri`, use `$MAESTRI_CLI`" e dizer quais peças exigem
  Maestro Mode.
- **Junction:** a pasta do acervo no hub, ligada em `~/.claude/skills/<nome>` (Claude Code e VS Code) e
  `~/.agents/skills/<nome>` (Codex, Copilot CLI e VS Code). O app grava as dele nas mesmas bases, lado a lado,
  sem tocar na do acervo.

## Primeira instrução e CLAUDE.md/AGENTS.md do workspace

### Onde fica o CLAUDE.md/AGENTS.md "do workspace"

**A doc diz.** "From the workspace edit screen, you can manage `CLAUDE.md` and `AGENTS.md` files. These files
contain instructions that agents automatically receive when they start inside that workspace"; "Maestri includes
an option to keep both files in sync automatically" (https://themaestri.app/en/docs/workspaces).

**O código do build 87 diz.**
- Os arquivos são os da pasta de trabalho: `resolveTarget` usa `workspace.workingDirectory`, e `pathFor` faz
  `join(directory, "CLAUDE.md" | "AGENTS.md")`. Nada vai para `workspace.json` (a estrutura dele não tem campo
  de instruções).
- Interface (seção "Config Files" da tela de edição): "Edit {{file}} in the workspace folder. Saving writes this
  file only."; apagar: "The file goes to the trash. The other config file is left alone."; sem pasta: "This
  workspace has no working directory, so there is nowhere to keep config files."
- Sincronia: estados "CLAUDE.md and AGENTS.md hold the same content." / "hold different content." / "Only
  {{file}} exists."; botão "Sync"; no conflito, "Syncing makes one file a copy of the other. Choose which version
  both files should keep." A função `sync` copia os bytes de um para o outro uma vez. Não achei opção salva nem
  sincronia automática neste build.
- Limite de edição na tela: 1 MiB ("past the 1048576 byte limit for editing here").

Consequência: para o workspace Context Hub, o "CLAUDE.md/AGENTS.md do workspace" **é** o `AGENTS.md` da raiz do
hub. Para um workspace aberto em `C:\Projetos\maestri`, são os arquivos dessa pasta, compartilhados pelos
workspaces que abrem nela (SOC, SBF, TRF3, VOEGOL, "context-hub (antigo)").

### O que chega a um terminal sem papel

O Maestri não injeta instruções. A doc: "New terminals will open here by default" (pasta de trabalho). O
ambiente do terminal local recebe `MAESTRI_TERMINAL_ID`, `MAESTRI_WORKSPACE_ID`, `MAESTRI_CLI` e `TERM_PROGRAM`
(código `buildEnv`). Quem lê CLAUDE.md/AGENTS.md é o agente, pelas regras dele:
- Claude Code: "loads `CLAUDE.md` and `CLAUDE.local.md` from your current working directory and every directory
  above it"; AGENTS.md só sem CLAUDE.md, salvo `claude-md-and-agents-md` (porta 3-4).
- Codex: global em `~/.codex` ("reads `AGENTS.override.md` if it exists. Otherwise, Codex reads `AGENTS.md`") e
  do projeto, da raiz git até o cwd, um arquivo por pasta; limite "`project_doc_max_bytes` (32 KiB by
  default)" (https://learn.chatgpt.com/docs/agent-configuration/agents-md.md).
- Copilot CLI: lê `AGENTS.md`, `CLAUDE.md`, `.github/copilot-instructions.md` e `~/.copilot/copilot-instructions.md`;
  "does not define a general precedence order between these files" (docs.github.com, add-custom-instructions).

### O que chega a um terminal com papel

Código `installRoleStrict`: cria `<projeto>/.maestri/roles/<id>/` com `CLAUDE.md` e `AGENTS.md` de conteúdo
idêntico, montado por `buildContent`: bloco `<your_assigned_role>` com o prompt e bloco `<working_directory>`
("IMPORTANT: You were started in this directory to receive the above role assignment. The actual project you
should be working on is located at: ..."), mais `role.json`. Limite: "role content exceeds 1048576 bytes". Os
arquivos só são reescritos se faltarem ou com `force`; senão o app os atualiza (`sb`, não lido em detalhe). Para
comandos que contêm `gemini` ou `qwen`, grava também `.gemini/settings.json` ou `.qwen/settings.json` com
`"context": {"fileName": ["AGENTS.md"], "includeDirectories": ["<projeto>"]}`, ou seja, só esses dois harnesses
ganham do Maestri um ponteiro explícito para o AGENTS.md do projeto. A skill `maestri-manager` resume: "A role
is a reusable prompt prepended to a teammate's instructions" (`maestri role --help`).

Pela doc de cada harness (sem teste):
- Claude Code no papel: lê o `CLAUDE.md` do papel e os `CLAUDE.md` das pastas acima, incluindo um `CLAUDE.md`
  na raiz do workspace; o `AGENTS.md` da raiz só com `claude-md-and-agents-md` (já testado no grupo A de
  "Testes das portas de entrada").
- Codex no papel: se a raiz git é a raiz do workspace, lê o `AGENTS.md` da raiz e o do papel, nessa ordem (o
  mais próximo prevalece). **Precisa de teste** (era a R37).
- Copilot CLI no papel: não verificado em que pastas acima ele procura.

### Mecanismos para a "primeira instrução" em todo workspace, inclusive fora do hub

**O Maestri não tem instrução global de workspace.** Nem a doc nem o código mostram instruções padrão para
workspace novo: os Config Files são da pasta, `maestri workspace create` não tem flag de instruções, e o
`--from` promete copiar "layout, agents, and connections", sem citar os arquivos da pasta (se leva: precisa de
teste).

Mecanismos que alcançam todo terminal, em ordem de alcance:

| Mecanismo | Alcança | A fonte diz | Observação |
|---|---|---|---|
| Arquivo global de cada harness (`~/.claude/CLAUDE.md`, `~/.codex/AGENTS.md`, `~/.copilot/copilot-instructions.md`) | todo terminal, com ou sem papel, dentro ou fora do Maestri | docs de memória/AGENTS.md/instruções de cada um | já testado por link no ticket 42 (Codex e Copilot recebem por link; `@import` não funciona no Codex) |
| Skill global do acervo nas duas bases | todo agente que lista skills | skills.md, build-skills.md, add-skills | carrega sob demanda pela descrição; não garante leitura no início |
| Hook `SessionStart` de usuário, condicionado a `MAESTRI_TERMINAL_ID` | todo terminal do Maestri, nos três harnesses | hooks.md (Claude Code e Codex), hooks-reference (Copilot) | sugestão; Codex exige aprovar o hook em `/hooks` |
| Preset com flag (ex.: `claude --append-system-prompt-file <arquivo>`) | terminais criados daquele preset, inclusive recrutas | doc Terminals (presets) e cli-reference | sugestão; vale só para Claude Code e só para quem usa o preset |
| Papel global (`role create --scope global`) | terminais com aquele papel, em qualquer workspace | `maestri role --help` | não chega a terminal sem papel |
| Partitura global com uma nota "primeira instrução" | quem aplicar a partitura | doc Partituras | manual |
| Config Files do workspace (CLAUDE.md/AGENTS.md da pasta) | só aquele workspace | doc Workspaces, código | é o ponto por workspace, não o global |

Sugestão: a "primeira instrução" mora no arquivo global de cada harness (que o ticket 42 mostrou ser ligável ao hub por link) e diz
"se `MAESTRI_TERMINAL_ID` existe e você é maestro, carregue a skill do acervo". O hook `SessionStart` é o reforço
para quando a regra do arquivo global não bastar.

## Não verificado

- Se presets de agente têm escopo de workspace (doc e Wire não falam de escopo; `preferences.json` não tem
  `workspaceId` nos presets).
- Onde a partitura guarda o escopo (global ou workspace): o arquivo local tem `payload.sourceWorkspaceId`, mas o
  campo de escopo não foi identificado.
- Como o app atualiza os arquivos de papel já existentes (função `sb`, não lida em detalhe), e se o "Discover
  Roles" aceita outra pasta (segue da porta 3-4).
- O que `MAESTRI_DATA_DIR` permite além de fixar a pasta de dados: o código diz "The storage location is pinned
  by the MAESTRI_DATA_DIR environment variable. Unset it to move the data root", e existe um
  `storage-location.json`, o que sugere uma opção de mover a pasta de dados pela interface; não conferido.
- Precedência entre subagente de projeto e de usuário no Codex, e entre skill de projeto e de usuário no Copilot
  CLI.
- Em que pastas acima do cwd o Copilot CLI procura `AGENTS.md`.
- Se junction do Windows conta como "symlink" para Claude Code e Codex (as docs falam de symlink; o ticket 42
  testou junction com Codex e Copilot e funcionou).
- Equivalente a output styles em Codex e Copilot.
- A versão `pt-br` da doc do Maestri não foi cotejada.

## Precisa de teste

- Se a sincronia CLAUDE.md/AGENTS.md tem algum gatilho automático (a doc diz que sim; o código do build 87 só
  mostra o botão "Sync").
- Se `workspace create --from` leva os arquivos CLAUDE.md/AGENTS.md da pasta do modelo para a pasta nova.
- Codex e Copilot dentro da pasta de um papel: que AGENTS.md cada um carrega (a R37 aprovada).
- Se `recruit --command "claude --agent X"` ou `--command "codex --profile Y"` funciona no Maestri e mantém conta,
  papel e skills.
- Se o FreeLLMAPI atende Claude Code por `ANTHROPIC_BASE_URL`, Codex por `[model_providers]` e Copilot por BYOK,
  e se o campo "API Endpoint" de uma conta do Maestri serve para isso.
- Hook `SessionStart` condicionado a `MAESTRI_TERMINAL_ID`: se a variável já existe quando o hook roda, nos três
  harnesses.
- Se um preset com `--append-system-prompt-file` é honrado pelos recrutas (a doc diz que recrutas usam o preset;
  não diz da linha de comando inteira).

## Fontes

Documentação do Maestri (curl, 2026-10-12; índice em https://themaestri.app/en/docs):
- https://themaestri.app/en/docs/intro, /workspaces, /terminals, /maestro, /notes, /ficharios, /connections,
  /partituras, /routines, /portals, /floors, /environments, /chat, /prompt-composer, /batuta-search, /canvas,
  /file-tree, /ombro, /shortcuts, /troubleshooting, /wire (seções Agent roles, Agent accounts, Terminals,
  Partituras, Floor hooks, Routines)

CLI do Maestri (build 87):
- `maestri help`; `maestri <list|notify|ask|check|say|recall|note|portal|recruit|dismiss|connect|preset|role|routine|workspace|floor|debug> --help`
- `maestri list`, `preset list`, `role list`, `routine list`, `workspace list`, `floor list` (só nomes citados)

Skills oficiais instaladas:
- `C:\Users\gustavo.delfino\.claude\skills\{maestri,maestri-chat,maestri-manager,maestri-portal,maestri-portal-devices,maestri-routines,maestri-workspace}\SKILL.md`

Código do app (lido como texto, sem executar):
- `C:\Users\gustavo.delfino\AppData\Local\Programs\Maestri\resources\app.asar` → `out/main/index.js`
  (funções `createWorkspaceConfigFiles`, `resolveTarget$1`, `pathFor`, `syncStateOf`, `installRoleStrict`,
  `buildContent`, `workingDirectoryBlock`, `buildSettingsJson`, `defaultSkillBases`, `installableSkills`,
  `installSkillsAtPaths`, `removeSkillsAtPaths`, `buildEnv`, `readEnvPin`), `out/renderer/assets/index-*.js`
  (`WorkspaceConfigFiles`, `ConflictSheet`), `out/renderer/assets/global-*.js` (textos em inglês de
  `sheet.configFiles`)
- `resources\build-info.json` (build 87, sha `9a4e3e5e`, 2026-10-11); `resources\cli\maestri.exe` (busca da
  palavra "partitura": ausente)

Arquivos locais (só estrutura):
- `C:\Users\gustavo.delfino\.maestri\preferences.json` (`agentPresets`, chaves de topo)
- `C:\Users\gustavo.delfino\.maestri\workspaces\271fe5c6-...\workspace.json` (chaves)
- `C:\Users\gustavo.delfino\.maestri\partituras\*.maestripartitura` (chaves de topo)

Claude Code (curl de https://code.claude.com/docs/en/...): skills.md, sub-agents.md, hooks.md, hooks-guide.md,
output-styles.md, plugins/overview.md, plugins/components.md, plugins/install.md, settings.md, model-config.md,
memory.md, cli-reference.md, env-vars.md, llm-gateway-connect.md

Codex (curl de https://learn.chatgpt.com/docs/..., via https://developers.openai.com/codex/llms.txt):
agent-configuration/agents-md.md, agent-configuration/subagents.md, build-skills.md, skills-and-plugins.md,
config-file/config-basic.md, config-file/config-advanced.md, config-file/config-reference.md, custom-prompts.md,
hooks.md, codex/cli.md

GitHub Copilot (https://docs.github.com/en/copilot/...): how-tos/copilot-cli/customize-copilot/{add-custom-instructions,
add-skills, create-custom-agents-for-cli, use-hooks, change-settings, use-byok-models},
reference/copilot-cli-reference/cli-command-reference, reference/custom-agents-configuration,
reference/hooks-reference, concepts/agents/about-agent-skills

VS Code (https://raw.githubusercontent.com/microsoft/vscode-docs/main/docs/agent-customization/...):
custom-instructions.md, custom-agents.md, agent-skills.md, prompt-files.md

Anexos anteriores: `exploracao/anexos/pesquisa-37-portas/porta-3-4-maestri.md`,
`exploracao/anexos/testes-42-repositorio-fora-do-hub.md`, `exploracao/anexos/testes-38-portas/grupo-a-carga-de-instrucoes.md`.
