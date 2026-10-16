# Pesquisa 46: o Copilot com a assinatura Business/Enterprise da empresa

Pesquisa em fonte primária, feita em 2026-10-12. O texto foi lido bruto com `curl`: a API de artigos do
docs.github.com (`/api/article/body?pathname=...`), o Markdown do repositório `microsoft/vscode-docs` (branch
`main`, páginas com `DateApproved: 10/7/2026`), o `changelog.md` do `github/copilot-cli` e a ajuda local do
Copilot CLI 1.0.96 (`copilot help`, `copilot instruction --help`, `copilot help commands`, `copilot help config`).
Nada foi testado nem configurado. A leitura local se limitou a conferir se existem os locais de política da
máquina. É saída de modelo: confira as citações antes de decidir.

Ticket: `.scratch/context-hub/issues/46-copilot-com-assinatura-enterprise-pesquisa.md`. Fatos de partida:
`pesquisa-18-acesso-copilot.md`, `pesquisa-41-contrato-pelo-mcp.md` e `testes-42-repositorio-fora-do-hub.md`.

## Pergunta

1. Que instruções a organização ou a empresa podem configurar para o Copilot, e quais chegam ao Copilot CLI e
   ao Copilot do VS Code.
2. Precedência e ordem entre as instruções da organização, do repositório, do usuário
   (`~/.copilot/copilot-instructions.md`), do `AGENTS.md` e das configurações do VS Code.
3. Que políticas da empresa ou da organização podem bloquear o desenho já decidido: arquivo global ligado ao
   contrato, skills por junction em `~/.agents/skills`, MCP do hub em `~/.copilot/mcp-config.json` e hooks.
4. Como o Gustavo pode ver, sem ser admin, o que a organização aplica.

## Resumo

- **Instruções da organização** existem (texto livre em *Settings → Copilot → Custom instructions* da
  organização, só em Business ou Enterprise). Pela doc do GitHub, valem **só no github.com** (Chat, code review e
  cloud agent). **Não chegam ao Copilot CLI.** A doc do VS Code diz o contrário para o VS Code: as "sessões
  Copilot suportadas" incluem as instruções da organização quando `github.copilot.chat.organizationInstructions.enabled`
  está ligado, e o padrão é `true`. As duas docs se contradizem; para o VS Code, **precisa de teste**.
- **Precedência:** só o github.com define uma ordem (pessoal > repositório > organização, e todas vão ao modelo).
  O CLI e o VS Code somam tudo e dizem expressamente que **não há ordem**.
- **A empresa governa sobretudo por "managed settings"** (`managed-settings.json`). Eles chegam ao CLI e ao VS
  Code por três vias: o servidor (repositório `.github-private` da empresa), o MDM (registro do Windows) ou um
  arquivo local. Nenhuma chave desse arquivo trata de instruções nem de skills. Há chaves para **MCP**
  (`allowedMcpServers`/`deniedMcpServers`), permissões, sandbox, plugins, modelo padrão e telemetria.
- **Maiores ameaças ao desenho:**
  1. uma **allowlist de MCP**, que bloquearia o MCP do hub se ele não estiver na lista;
  2. a política de dispositivo do VS Code **`ChatStrictPluginOnlyCustomization`**, que bloqueia skills,
     instruções, MCP e hooks avulsos de usuário (só passa o que vem por plugin);
  3. políticas de **hooks só gerenciados**;
  4. um **sandbox** ou regras de permissão impostos que limitem leitura ou rede.

  Nada disso está documentado como ligado por padrão.
- **Nesta máquina** não há política de dispositivo: o registro e as pastas de política do Copilot e do VS Code
  estão vazios. Há um cache de configurações gerenciadas pelo servidor, ilegível como JSON; se ele contém
  regras, não se sabe.

---

## 1. Que instruções a organização ou a empresa podem configurar

### 1.1 Instruções personalizadas da organização (texto livre no GitHub)

- **O que é.** *"Organization custom instructions apply to conversations within the context of an organization
  on the GitHub website. [...] Organization custom instructions can only be set by organization owners for
  organizations with a Copilot Business or Copilot Enterprise subscription."*
  ([response-customization](https://docs.github.com/en/copilot/concepts/prompting/response-customization))
- **Onde se configura.** *"In the left sidebar, click Copilot then click Custom instructions. Under
  "Preferences and instructions", add natural language instructions to the text box."*
  ([add-organization-instructions](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/add-custom-instructions/add-organization-instructions))
- **Alcance pela doc do GitHub.** *"Organization custom instructions are currently only supported for Copilot
  Chat on GitHub.com, Copilot code review on GitHub.com and Copilot cloud agent on GitHub.com."* (mesma página).
  A tabela de suporte confirma: a seção **Copilot CLI** lista só repository-wide, path-specific, agent
  instructions e *"Personal instructions (using ~/.copilot/copilot-instructions.md or
  ~/.copilot/instructions/**/*.instructions.md files)"*. A seção **Visual Studio Code / Copilot Chat** lista só
  `.github/copilot-instructions.md`, `.github/instructions/**/*.instructions.md` e `AGENTS.md`, sem "Organization".
  ([custom-instructions-support](https://docs.github.com/en/copilot/reference/custom-instructions-support))
- **Valem para quem é membro, venha a licença de onde vier.** *"Custom instructions defined in an organization's
  Copilot settings are used for all members of the organization, irrespective of whether they receive their
  Copilot subscription from that organization."* (response-customization)
- **O que diz a doc do VS Code, em contradição com a do GitHub.** A tabela de escopos traz *"Organization |
  Centrally managed requirements for supported Copilot sessions | GitHub organization settings"*. A seção
  "Share custom instructions across teams" diz *"Supported Copilot sessions automatically include organization
  instructions that your account can access. Organization instructions are additive to user and repository
  instructions."* e *"To enable discovery of organization-level custom instructions, set
  `github.copilot.chat.organizationInstructions.enabled` to `true`."*
  ([custom-instructions, VS Code](https://code.visualstudio.com/docs/agent-customization/custom-instructions)).
  A referência de configurações dá o padrão `true`: *"Enable discovery of custom instructions defined at the GitHub
  organization level. | `true`"* ([ai-settings](https://code.visualstudio.com/docs/agents/reference/ai-settings)).
  A página de administração repete a regra: *"When `github.copilot.chat.organizationInstructions.enabled` is `true`,
  supported Copilot sessions in VS Code include organization instructions that the signed-in account can access."*
  ([manage-ai-settings](https://code.visualstudio.com/docs/enterprise/manage-ai-settings)).
  - Nenhuma das duas páginas diz se "sessões suportadas" inclui o harness **Copilot (Agent Host)** ou só o
    **Local**: **não verificado**.
  - No changelog do GitHub não achei anúncio de instruções da organização no VS Code nem no CLI. Achei só no
    github.com (2025-04-17, [changelog](https://github.blog/changelog/2025-04-17-organization-custom-instructions-now-available/)),
    no cloud agent (2025-11-05, [changelog](https://github.blog/changelog/2025-11-05-copilot-coding-agent-supports-organization-custom-instructions/))
    e no Visual Studio, que é outro produto (2026-07-30, [changelog](https://github.blog/changelog/2026-07-30-github-copilot-in-visual-studio-july-update/)).
- **No CLI, não há fonte de instruções da organização.** A lista completa de locais do CLI (*"loads custom
  instructions from these locations simultaneously (all are merged)"*) tem `CLAUDE.md`, `GEMINI.md`, `AGENTS.md`,
  `.github/instructions/**/*.instructions.md`, `.claude/rules/**/*.md`, `.github/copilot-instructions.md`,
  `$HOME/.copilot/copilot-instructions.md`, `$HOME/.copilot/instructions/**/*.instructions.md` e
  `COPILOT_CUSTOM_INSTRUCTIONS_DIRS`, sem fonte remota
  ([cli-command-reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-command-reference#custom-instructions-locations)).
  A ajuda local (1.0.96) confirma: *"Instructions come from your repository, the working directory, your personal
  configuration, and installed plugins."* (`copilot instruction --help`).
  - **Via indireta: plugins impostos.** Um plugin pode levar regras (*"Rules | `com.github.copilot/rules/`"*,
    [cli-plugin-reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference)),
    e a empresa pode forçar plugins com `enabledPlugins` (§3.4). Assim a empresa conseguiria pôr texto nas
    instruções do CLI e do VS Code. A doc não descreve isso como "instruções da empresa"; é inferência a partir
    das duas regras.
- **Instruções "da empresa" (enterprise) em texto livre:** nenhuma página as descreve. As instruções são da
  **organização**, não da empresa (**não verificado** se existe algo no nível enterprise).

### 1.2 Instruções do repositório

`.github/copilot-instructions.md`, `.github/instructions/**/*.instructions.md` e `AGENTS.md`/`CLAUDE.md`/`GEMINI.md`
são arquivos do **repositório**, e quem os escreve é quem tem acesso ao repositório, não a organização como tal.
Valem no CLI e no VS Code como na pesquisa 18. Só pesam no hub se o Copilot abrir dentro de um repositório da
empresa que tenha esses arquivos. Nesse caso, entram somados ao contrato (§2).

### 1.3 Prompt files

São arquivos `*.prompt.md` do workspace, acionados pelo usuário: *"Prompt files are only available in VS Code,
Visual Studio, and JetBrains IDEs"* (response-customization, aba VS Code). A pesquisa 18 já registrou que o
Agent Host não os carrega. Não há prompt file "da organização" documentado (**não verificado**).

### 1.4 Agentes personalizados da organização ou da empresa

- **Onde ficam.** *"Organization level: Create `/agents/CUSTOM-AGENT-NAME.md` in the organization's `.github` or
  `.github-private` repository"* e *"Enterprise level: Create `/agents/CUSTOM-AGENT-NAME.md` in the
  `.github-private` repository of an organization that an enterprise owner has designated"*
  ([about-custom-agents, CLI](https://docs.github.com/en/copilot/concepts/agents/copilot-cli/about-custom-agents)).
- **Chegam ao CLI**, com a menor prioridade: *"6 (lowest) | Remote | Organization or enterprise agents"*, depois
  de `~/.copilot/agents/`, `.github/agents/`, `.claude/agents/`, `--add-dir` e plugins (cli-command-reference,
  "Custom agent locations"). A página de administração confirma: *"Enterprise-configured custom agents are
  available to use with Copilot CLI."* ([administer-copilot-cli-for-your-enterprise](https://docs.github.com/en/copilot/how-tos/copilot-cli/administer-copilot-cli-for-your-enterprise)).
  O usuário pode desligá-los com `customAgents.defaultLocalOnly`: *"Only use local custom agents (no remote
  organization or enterprise agents)."* ([cli-config-dir-reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-config-dir-reference)).
- **Chegam ao VS Code:** *"VS Code automatically detects custom agents defined at the organization level to which
  your account has access"*, com `github.copilot.chat.organizationCustomAgents.enabled`, padrão `true`
  ([custom-agents, VS Code](https://code.visualstudio.com/docs/agent-customization/custom-agents); ai-settings).

### 1.5 Skills da organização ou da empresa

Só o CLI as menciona: *"(org/enterprise) | Remote | Skills hosted by your organization or enterprise, projected via
the AHP relay. Content is fetched on demand when the skill is invoked."* e *"Remote skills are projected alongside
local skills and follow the same name-based priority when a local skill has the same name."* Na tabela, as remotas
vêm por último, depois de `~/.agents/skills` (cli-command-reference, "Skill locations"). Como um admin publica
essas skills, a doc não diz (**não verificado**).

### 1.6 Quadro: o que chega aonde

| Fonte controlada pela organização ou empresa | github.com | Copilot CLI | Copilot no VS Code |
|---|---|---|---|
| Instruções da organização (texto livre) | sim | **não** (doc GitHub e lista de locais do CLI) | doc do GitHub: não; doc do VS Code: sim, com `organizationInstructions.enabled` (padrão `true`). **Contradição** |
| Arquivos de instrução do repositório | sim | sim | sim |
| Agentes da organização ou da empresa | cloud agent | sim, prioridade mínima | sim, com `organizationCustomAgents.enabled` (padrão `true`) |
| Skills remotas da organização ou da empresa | n/d | sim, prioridade mínima | não documentado |
| Plugins impostos (`enabledPlugins`), que podem levar regras, skills, MCP e hooks | n/d | sim | sim |

---

## 2. Precedência e ordem

- **github.com (a única ordem documentada).** *"Personal instructions take the highest priority. Repository
  instructions come next, and then organization instructions are prioritized last. However, all sets of relevant
  instructions are provided to Copilot."* Ordem completa: pessoal → repositório (path-specific →
  `.github/copilot-instructions.md` → agent instructions, como `AGENTS.md`) → organização. (response-customization,
  "Precedence of custom instructions"; a página avisa que essa versão é *"about custom instructions on the GitHub
  website"*.)
- **Copilot CLI: sem ordem.** *"When multiple applicable user-level and repository instruction files exist,
  Copilot CLI combines their instructions. It removes duplicate copies of identical user-level
  `copilot-instructions.md`, repository-wide, and agent instructions, but does not define a general precedence
  order between these files. Avoid conflicting instructions."*
  ([add-custom-instructions, CLI](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-custom-instructions)).
  Não há instrução da organização para ordenar (§1.1).
- **VS Code: sem ordem, inclusive para as da organização.** *"Applicable instruction sources are additive. Do not
  depend on a file order or precedence rule to resolve conflicts because discovery and merge behavior can differ by
  harness."* E, sobre organização × repositório × pessoal: *"Don't add a new instruction or assume that one source
  overrides the others."* (custom-instructions, VS Code, "Resolve conflicting instructions").
- **Instruções nas configurações do VS Code (`settings`).** As instruções de geração de código e de testes por
  configuração estão obsoletas: *"Settings-based code generation and test generation instructions are deprecated as
  of VS Code 1.102. Use file-based instructions instead."* Ficam só as de revisão de seleção, mensagem de commit e
  descrição de PR (`github.copilot.chat.reviewSelection.instructions`,
  `...commitMessageGeneration.instructions`, `...pullRequestDescriptionGeneration.instructions`). Essas não
  entram no modo agente (mesma página).
- **Não confundir com a precedência das *configurações*.** Para chaves de configuração (não instruções), a ordem
  da empresa é *"1. MDM-managed settings 2. Server-managed settings 3. File-based settings 4. User-level settings"*,
  e `sandbox` e `permissions.deny/ask/allow` se combinam *"in the most restrictive direction"*
  ([deploy-managed-settings](https://docs.github.com/en/copilot/how-tos/administer-copilot/manage-for-enterprise/use-managed-settings/deploy-managed-settings)).
  No VS Code, *"If both systems configure the same control, the enterprise-managed setting takes precedence"* sobre
  a política de dispositivo (manage-ai-settings).

**Leitura para o hub:** onde o contrato do hub e uma instrução da empresa (ou de um repositório da empresa) se
contradisserem, nenhuma regra documentada decide qual vence no CLI nem no VS Code; o modelo recebe as duas.

---

## 3. Políticas que podem bloquear o desenho

### 3.1 As três vias de controle

- **Políticas no GitHub** (organização ou empresa, *AI controls*). Ligam e desligam recursos e modelos, por conta.
  *"A user is governed by the policies of the enterprise or organization where they receive a Copilot Business or
  Copilot Enterprise license."* Com licença de várias organizações da mesma empresa, *"the **least restrictive**
  policy usually applies"*
  ([policies](https://docs.github.com/en/copilot/concepts/enterprise/policies)).
- **Managed settings** (`managed-settings.json`): servidor (`.github-private/copilot/managed-settings.json`), MDM
  (Windows: *"String (`REG_SZ`) values under `HKEY_LOCAL_MACHINE\SOFTWARE\Policies\GitHubCopilot`"*) ou arquivo
  (*"Windows | `%ProgramFiles%\GitHubCopilot\managed-settings.json`"*). Valem para *"Copilot CLI, VS Code, The
  GitHub Copilot app, Copilot cloud agent, JetBrains IDEs"*
  ([get-started](https://docs.github.com/en/copilot/how-tos/administer-copilot/manage-for-enterprise/use-managed-settings/get-started);
  deploy-managed-settings).
- **Políticas de dispositivo do VS Code** (Group Policy, Intune), gravadas em *"`Software\Policies\Microsoft\VSCode`"*
  ([policies, VS Code](https://code.visualstudio.com/docs/enterprise/policies)). A versão 1.141 traduz parte delas
  para managed settings no Agent Host: *"VS Code translates supported legacy policies into unified managed settings
  at runtime when possible"* ([notas da 1.141](https://code.visualstudio.com/updates/v1_141)).

As chaves aceitas em managed settings são `permissions.*`, `features.computerUse`, `model`, `autoTier`,
`enabledPlugins`, `extraKnownMarketplaces`, `strictKnownMarketplaces`, `forceRemoteSettingsRefresh`, `telemetry`,
`remoteControl`, `allowedMcpServers`, `deniedMcpServers` e `sandbox`
([enterprise-managed-settings](https://docs.github.com/en/copilot/reference/enterprise-administrators/enterprise-managed-settings)).
O CLI aceita ainda `forceLoginOrgs`, `policyHelper` e `shellShortcut` (cli-config-dir-reference). **Nenhuma
chave trata de instruções nem de skills.**

### 3.2 MCP

- **Política "MCP servers in Copilot".** *"defines whether MCP servers can run at all across Copilot clients"*
  ([mcp-management](https://docs.github.com/en/copilot/concepts/enterprise/mcp-management)). Na tabela de
  superfícies, vale para IDEs e para o Copilot CLI
  ([supported-surfaces-for-policies](https://docs.github.com/en/copilot/reference/supported-surfaces-for-policies)).
  - **Contradição:** a página conceitual do CLI diz *"Copilot CLI can't currently support the following
    organization-level MCP server policies: MCP servers in Copilot [...] MCP Registry URL"*
    ([copilot-cli, conceito](https://docs.github.com/en/copilot/concepts/copilot-surfaces/copilot-cli)).
  - A página de administração do CLI diz *"Enterprise and organization MCP policies apply to Copilot CLI."*
    (administer-copilot-cli-for-your-enterprise).
  - O changelog do CLI registra *"Block third-party MCP servers when the Copilot MCP policy does not allow them"* e
    *"Organization policy for third-party MCP servers is now enforced for all users"*
    ([changelog](https://github.com/github/copilot-cli/blob/main/changelog.md)).

  O peso das fontes indica que a política vale no CLI, mas a doc se contradiz.
- **Allowlist pelos managed settings (a via que o GitHub recomenda).** *"When set, only servers matching at least
  one entry are allowed. Any server that is not matched is blocked."*
  - Formas de casar o servidor: `serverName`, `serverUrl` (*"Supports `*` wildcards"*) e `serverCommand`
    (*"Matches the exact command and each argument for a local server [...] Wildcards and command-line expansion
    are not supported."*). Fonte: enterprise-managed-settings.
  - Regras de avaliação ([configure-enterprise-allowlist](https://docs.github.com/en/copilot/how-tos/administer-copilot/manage-mcp-usage/configure-enterprise-allowlist)):
    - *"Block the server if its URL or command contains an unresolved variable, such as `${VARIABLE}` or
      `$VARIABLE`, because the client cannot verify the server."*
    - *"If an allowlist or denylist is malformed [...] This blocks all servers except built-in default servers."*
  - No CLI, a checagem *"is fail-closed: if the evaluate endpoint is unreachable or returns an error, non-default
    servers are blocked until the policy can be verified"*. A mensagem é *"MCP server "SERVER-NAME" was blocked by
    your enterprise "ENTERPRISE-NAME"."* (cli-command-reference, "Enterprise MCP allowlist").
- **Registro privado ("Restrict MCP access to registry servers": Allow all / Registry only).** Está em preview e
  *"not the recommended method"*. Casa só por nome ou ID (*"can be bypassed by editing configuration files"*). Com
  "Registry only", *"local servers must be included in your registry with the correct server ID"*. Vale no CLI a
  partir da 1.0.11 e no VS Code a partir da 1.109.3
  ([mcp-private-registry-enforcement](https://docs.github.com/en/copilot/reference/enterprise-administrators/mcp-private-registry-enforcement)).
- **VS Code, políticas de dispositivo:** `ChatMCP` (*"Controls access to installed Model Context Protocol
  servers"*), `ChatAllowedMcpServers`, `ChatDeniedMcpServers`, `ChatAllowManagedMcpServersOnly` e
  `McpGalleryServiceUrl` (policies, VS Code). A seção de MCP da página de administração do VS Code está comentada
  no código-fonte, isto é, não publicada.

### 3.3 Skills, instruções e MCP avulsos no VS Code: `ChatStrictPluginOnlyCustomization`

Política de dispositivo do VS Code, desde a 1.132: *"Blocks standalone user and workspace skills, agents, hooks,
instructions, and MCP servers while keeping eligible plugin customizations available."* (policies, VS Code). A
página de administração a descreve assim: *"Set `ChatStrictPluginOnlyCustomization` when you also need to block
standalone user and workspace skills, agents, instructions, and MCP servers."* (manage-ai-settings).

Se ligada, ela derruba **as três peças do desenho no VS Code**: o `copilot-instructions.md` ligado, as skills em
`~/.agents/skills` e o MCP em `~/.copilot/mcp-config.json`. Só sobraria entregar o hub como **plugin**. Se ela vale
também no harness Copilot (Agent Host) ou só no Local: **não verificado**. As notas da 1.141 dizem apenas que
políticas antigas são traduzidas "when possible". No CLI, não achei política equivalente.

### 3.4 Plugins

`enabledPlugins` força a ligar ou desligar plugins, `extraKnownMarketplaces` acrescenta marketplaces e
`strictKnownMarketplaces` restringe a instalação a marketplaces listados (*"An empty array means complete
lockdown"*). As três valem no CLI e no VS Code (enterprise-managed-settings). O desenho decidido não usa plugin, mas
um plugin é a saída se §3.3 estiver ligada; com `strictKnownMarketplaces`, ele teria de vir de um marketplace
aprovado.

### 3.5 Hooks

- **CLI.** A empresa pode instalar *policy hooks* em `C:\ProgramData\GitHub\Copilot\policy.d\*.json` ou em
  `HKLM\Software\Policies\GitHub\Copilot`. Eles *"load before all other hooks and cannot be disabled by
  `disableAllHooks`"* e somam-se aos do usuário: *"When the same event appears in multiple sources, all hook entries
  from all sources are run."* ([hooks-reference](https://docs.github.com/en/copilot/reference/hooks-reference)).
  Um hook de política `preToolUse` que negue pode vetar ferramentas do hub.
  - O changelog 1.0.85 cita uma política **`allowManagedHooksOnly`** (*"now also blocks extension-registered
    `preToolUse` [...] callbacks, which previously bypassed the managed-only lockdown"*), mas ela não aparece na
    referência de managed settings nem na de hooks. Onde ela se configura: **não verificado**.
- **VS Code.** `ChatAllowManagedHooksOnly` (*"Allows hooks only from enterprise-managed sources and plugins
  force-enabled by policy"*). `ChatHooks` desliga hooks só no harness Local: *"does not apply to Copilot sessions
  that use Agent Host"*. As sessões Agent Host *"load Copilot Policy Hooks"* (manage-ai-settings;
  [agent-harnesses](https://code.visualstudio.com/docs/agents/run/agent-harnesses)).

### 3.6 Permissões e sandbox impostos

- `permissions.deny` com `Read(...)`/`Edit(...)` bloqueia caminhos, e `Domain(...)` e `limitTo` fecham a rede.
  *"A deny rule set by any managed settings source blocks the operation for all users"*. Um `ask` gerenciado *"can't
  be satisfied by bypass mode [...] a hook or other approval shortcut"*. No VS Code, as regras granulares valem só
  no Agent Host (enterprise-managed-settings).
- `sandbox` impõe um piso que o usuário não afrouxa. Inclui `sandboxMcpServers` (*"sandboxing MCP and LSP servers
  cannot be turned off"*) e regras de sistema de arquivos e de rede (cli-config-dir-reference). Vale no CLI e no
  Agent Host do VS Code (1.138+).
- **Inferência:** um sandbox imposto que só libere a pasta de trabalho pode impedir comandos de shell de ler
  `C:\context-hub` quando o Copilot abre na pasta da iniciativa, e um MCP local sandboxado pode perder acesso ao
  hub. Se isso acontece depende das regras que a empresa escrever: **não verificado**.

### 3.7 Copilot CLI ligado ou não; agentes; modelos

- **Copilot CLI.** Política própria, em *"Features & clients → Clients"*. *"If the enterprise policy is set to "Let
  organizations decide," [...] Copilot CLI must be enabled in **at least one** of the organization granting them a
  GitHub Copilot license."* (administer-copilot-cli-for-your-enterprise). Ela é independente do app: *"Disabling
  Copilot CLI does not disable the GitHub Copilot app."*
- **Modo agente no VS Code.** Política *"Copilot Agent Mode in IDE Chat"* no GitHub
  ([policy-conflicts](https://docs.github.com/en/copilot/reference/enterprise-administrators/policy-conflicts)) e
  `ChatAgentMode` no dispositivo (*"the **Agent** option is not available"*, manage-ai-settings). A página de
  gestão de agentes do GitHub diz *"Agents running in Visual Studio Code are not managed through GitHub at all"*
  ([agent-management](https://docs.github.com/en/copilot/concepts/enterprise/agent-management)). Isso briga com a
  política de modo agente e com os managed settings, que a doc do VS Code diz valerem no editor.
- **Agentes de terceiros.** No github.com são políticas separadas para Claude e Codex como cloud agents (*"Disabling
  or restricting Copilot cloud agent does not automatically disable third-party agents"*, agent-management). No VS
  Code são as políticas de dispositivo `Claude3PIntegration` e `Codex3PIntegration` (policies, VS Code). Não afetam
  o desenho do hub.
- **Modelos.** *"Users can only access AI models that are enabled at the enterprise level."* Vê-se com `/model`
  (administer-copilot-cli-for-your-enterprise). Um repositório pode limitar modelos com `.github/allowed_models.txt`
  (cli-config-dir-reference). A chave gerenciada `model` só define o padrão. Não afeta o desenho; limita a escolha.
- **Login preso à organização:** `forceLoginOrgs` no CLI e `ChatApprovedAccountOrganizations` no VS Code.

### 3.8 Content exclusion

- Vale no Copilot CLI (*"GitHub Copilot CLI | Not applicable | [Supported]"*) e **não** vale no modo agente do VS
  Code (*"Content exclusion is currently not supported in Edit and Agent modes of Copilot Chat in Visual Studio Code
  and other editors."*). ([content-exclusion](https://docs.github.com/en/copilot/concepts/security-governance-and-network-settings/content-exclusion))
- A organização e a empresa podem excluir arquivos **fora de qualquer repositório**: *"The files can be within a Git
  repository or anywhere on the file system that is not under Git control."*, com o padrão `"*":`
  ([exclude-content-from-copilot](https://docs.github.com/en/copilot/how-tos/configure-content-exclusion/exclude-content-from-copilot)).
  Em tese, uma regra ampla poderia pegar arquivos do hub no CLI.
- *"Currently, content exclusions do not apply to symbolic links (symlinks)"* (content-exclusion). O contrato chega
  por link simbólico. Se isso o livraria de uma exclusão: **não verificado**.

---

## 4. Como ver o que a organização aplica, sem ser admin

**No Copilot CLI** (comandos da referência e da ajuda local 1.0.96):

- `/env`: *"Show loaded environment details (instructions, MCP servers, skills, agents, hooks, plugins, LSPs,
  extensions)"*. É o retrato mais completo de uma sessão.
- `/instructions` (*"View and toggle custom instruction files"*) e `copilot instruction list [--json]`. Ressalva da
  doc: *"an instruction enabled by a trusted repository or by managed settings might not appear here even though a
  live session applies it"* (cli-command-reference).
- `/mcp` e `copilot mcp list`: o servidor bloqueado por política aparece como bloqueado, e a mensagem cita a
  empresa (changelog: *"An MCP server blocked by an enterprise policy now shows as blocked in /mcp"*).
- `/model`: o seletor separa *"Available, Blocked/Disabled, and Upgrade"* (changelog).
- `/settings`: *"Settings managed by your repository or organization are shown for reference"*
  ([change-settings](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/change-settings)).
- `/plugin`: o painel marca com *"Managed"* os plugins impostos (cli-plugin-reference).
- `/sandbox policy`: mostra os caminhos resolvidos por origem. `/skills` e `/agent` listam skills e agentes, os
  remotos inclusive.
- Avisos de política aparecem na linha do tempo, por exemplo quando a política suprime `--yolo`
  (cli-command-reference).

**No VS Code:**

- **Developer: Policy Diagnostics**: *"Applied Policy: settings that are currently overridden by a policy, with the
  setting key, policy name, policy source [...]"*, mais a política da conta e o estado do *Account Policy Gate*
  ([policies, VS Code](https://code.visualstudio.com/docs/enterprise/policies#_verify-policy-enforcement)). Mostra a
  origem: dispositivo, servidor ou arquivo (manage-ai-settings).
- O editor de configurações marca o que é *"managed by the organization"* (policies, VS Code).
- O **Agent Customizations editor**, os **Agent Debug Logs** e o **References** de cada resposta mostram que
  instruções entraram (custom-instructions, VS Code).

**No github.com:**

- Se a empresa usa managed settings pelo servidor, o arquivo fica em `.github-private/copilot/managed-settings.json`
  de uma organização designada. A doc recomenda deixá-lo visível aos membros: *"We recommend giving the repository
  internal visibility, so that enterprise members can view the governance settings"* (get-started). Os agentes da
  organização ficam em `/agents` do `.github` ou `.github-private` (prepare-for-custom-agents).
- A página pessoal [Copilot features](https://github.com/settings/copilot/features) mostra *"Usage billed to"*, ou
  seja, de qual empresa ou organização vem a licença (get-started; policies). Se ela também mostra cada política
  imposta: **não verificado**.
- O texto das instruções da organização fica na tela de configurações da organização, que é de admin. Se um membro
  consegue lê-lo: **não verificado**.

**Na máquina** (leitura de registro e pastas, sem admin):

- `HKLM\SOFTWARE\Policies\GitHubCopilot` (MDM do Copilot), `%ProgramFiles%\GitHubCopilot\managed-settings.json`
  (arquivo), `HKLM\Software\Policies\GitHub\Copilot` e `C:\ProgramData\GitHub\Copilot\policy.d\` (policy hooks), e
  `HKLM`/`HKCU\Software\Policies\Microsoft\VSCode` (políticas do VS Code).
- **Observação local (2026-10-12):** nenhum desses locais existe nesta máquina, ou seja, não há política de
  dispositivo. O CLI tem em `%LOCALAPPDATA%\copilot\managed-settings\` um arquivo de 252 bytes, de nome em hash, que
  não abre como JSON. É o cache das configurações vindas do servidor (inferência pelo nome; formato não
  documentado). Se ele contém regras ou está vazio: **não verificado**. O `settings.json` do VS Code não tem
  nenhuma chave `github.copilot.chat.organization*`, então valem os padrões (`true`).

---

## O que muda ou ameaça o desenho já decidido

| Peça decidida | Pode ser afetada por | Fonte | Peso |
|---|---|---|---|
| Contrato por link simbólico em `~/.copilot/copilot-instructions.md` | Nada no CLI. No VS Code, `ChatStrictPluginOnlyCustomization` bloqueia "instructions" avulsas. Instruções da organização podem entrar somadas no VS Code, sem precedência | policies e custom-instructions (VS Code) | Médio: depende de política de dispositivo que hoje não existe nesta máquina |
| Skills por junction em `~/.agents/skills` | `ChatStrictPluginOnlyCustomization` (VS Code). Skills remotas de mesmo nome perdem para as locais | policies (VS Code); cli-command-reference | Baixo no CLI, médio no VS Code |
| MCP do hub em `~/.copilot/mcp-config.json` | Política "MCP servers in Copilot" desligada; `allowedMcpServers` sem o hub; "Registry only" sem o ID do hub; `ChatMCP`; `ChatStrictPluginOnlyCustomization`; um sandbox imposto | §3.2, §3.3, §3.6 | **O maior risco.** Se a empresa ligar uma allowlist, o hub precisa entrar nela por `serverCommand` exato e **sem variáveis não resolvidas** no comando |
| Hooks do hub (se houver) | `allowManagedHooksOnly` (CLI, só no changelog) e `ChatAllowManagedHooksOnly` (VS Code); policy hooks da empresa rodam antes e somam | §3.5 | Médio |
| Copilot abrindo na pasta da iniciativa | Repositórios da empresa com `.github/copilot-instructions.md`/`AGENTS.md` somam-se ao contrato; `.github/allowed_models.txt` limita modelos; content exclusion no CLI | §1.2, §3.7, §3.8 | Baixo |
| Usar o CLI e o modo agente | Política "Copilot CLI" e "Agent Mode in IDE Chat" | §3.7 | Liga/desliga tudo; hoje funciona (testes 42) |

**O que não muda:** as instruções da organização não substituem nem bloqueiam o arquivo global do usuário. Na pior
hipótese, somam texto. Nenhuma chave de managed settings mexe em instruções ou skills do usuário. O teste 42
(Copilot CLI 1.0.95 e VS Code 1.141.0, com a conta da empresa) já mostrou o contrato e a skill chegando, o que indica
que hoje nenhuma das políticas de §3.3 e §3.5 está ligada para o Gustavo. **Inferência**: o teste não olhou
políticas, e o MCP do hub não entrou nele.

**Saída se a empresa travar:** entregar o hub como plugin (skills, regras, MCP e hooks num pacote) por um
marketplace aprovado, ou pedir a inclusão do servidor do hub na allowlist. As duas exigem a empresa.

## Não verificado

- Se as instruções da organização entram no Copilot do VS Code (doc do VS Code diz sim, doc do GitHub diz não) e,
  se entram, se é no harness Copilot (Agent Host) ou só no Local.
- Se a organização do Gustavo tem instruções personalizadas configuradas, e se um membro consegue lê-las.
- Se a política "MCP servers in Copilot" vale no CLI (três fontes dizem sim, a página conceitual do CLI diz não).
- Onde se configura `allowManagedHooksOnly` no CLI (só aparece no changelog).
- Se `ChatStrictPluginOnlyCustomization` e `ChatAllowManagedHooksOnly` valem nas sessões Agent Host.
- Como a organização ou a empresa publica "skills remotas" para o CLI.
- O conteúdo do cache `%LOCALAPPDATA%\copilot\managed-settings\*.json` (formato não documentado).
- Se a página `github.com/settings/copilot/features` lista as políticas impostas.
- Se a content exclusion pegaria arquivos do hub lidos por link simbólico.
- Instruções no nível da empresa (não da organização): nenhuma fonte as descreve.

## Precisa de teste

- Abrir `/env`, `/instructions`, `/mcp` e `/model` no CLI, e **Developer: Policy Diagnostics** no VS Code, com a conta
  da empresa. Isso mostra o que a organização aplica hoje, sem mudar nada.
- Com o MCP do hub configurado: ver se `/mcp` o mostra conectado ou "blocked by your enterprise".
- No VS Code, harness Copilot: ver no **References** ou nos Agent Debug Logs se entra alguma instrução da
  organização.

## Fontes

GitHub Docs (texto pela API `docs.github.com/api/article/body`):
- https://docs.github.com/en/copilot/reference/custom-instructions-support
- https://docs.github.com/en/copilot/concepts/prompting/response-customization
- https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/add-custom-instructions/add-organization-instructions
- https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-custom-instructions
- https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-command-reference
- https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-config-dir-reference
- https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference
- https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/change-settings
- https://docs.github.com/en/copilot/how-tos/copilot-cli/administer-copilot-cli-for-your-enterprise
- https://docs.github.com/en/copilot/concepts/copilot-surfaces/copilot-cli
- https://docs.github.com/en/copilot/concepts/agents/copilot-cli/about-custom-agents
- https://docs.github.com/en/copilot/reference/enterprise-administrators/enterprise-managed-settings
- https://docs.github.com/en/copilot/how-tos/administer-copilot/manage-for-enterprise/use-managed-settings/get-started
- https://docs.github.com/en/copilot/how-tos/administer-copilot/manage-for-enterprise/use-managed-settings/deploy-managed-settings
- https://docs.github.com/en/copilot/concepts/enterprise/mcp-management
- https://docs.github.com/en/copilot/how-tos/administer-copilot/manage-mcp-usage/configure-enterprise-allowlist
- https://docs.github.com/en/copilot/how-tos/administer-copilot/manage-mcp-usage/restrict-based-on-registry
- https://docs.github.com/en/copilot/reference/enterprise-administrators/mcp-private-registry-enforcement
- https://docs.github.com/en/copilot/reference/supported-surfaces-for-policies
- https://docs.github.com/en/copilot/concepts/enterprise/policies
- https://docs.github.com/en/copilot/reference/enterprise-administrators/policy-conflicts
- https://docs.github.com/en/copilot/how-tos/administer-copilot/manage-for-organization/manage-policies
- https://docs.github.com/en/copilot/concepts/enterprise/agent-management
- https://docs.github.com/en/copilot/how-tos/administer-copilot/manage-for-organization/prepare-for-custom-agents
- https://docs.github.com/en/copilot/concepts/enterprise/plugin-standards
- https://docs.github.com/en/copilot/reference/hooks-reference
- https://docs.github.com/en/copilot/concepts/security-governance-and-network-settings/content-exclusion
- https://docs.github.com/en/copilot/how-tos/configure-content-exclusion/exclude-content-from-copilot

VS Code (Markdown de `raw.githubusercontent.com/microsoft/vscode-docs/main/...`):
- https://code.visualstudio.com/docs/agent-customization/custom-instructions
- https://code.visualstudio.com/docs/agent-customization/custom-agents
- https://code.visualstudio.com/docs/agents/reference/ai-settings
- https://code.visualstudio.com/docs/enterprise/manage-ai-settings
- https://code.visualstudio.com/docs/enterprise/policies
- https://code.visualstudio.com/docs/agents/run/agent-harnesses
- https://code.visualstudio.com/updates/v1_141 (notas de versão, seção "Enterprise")

Changelog:
- https://github.com/github/copilot-cli/blob/main/changelog.md (até a 1.0.96, 2026-10-12)
- https://github.blog/changelog/2025-04-17-organization-custom-instructions-now-available/
- https://github.blog/changelog/2025-11-05-copilot-coding-agent-supports-organization-custom-instructions/
- https://github.blog/changelog/2026-07-30-github-copilot-in-visual-studio-july-update/

Leitura local (sem alterar nada): `copilot --version`, `copilot help`, `copilot help commands`, `copilot help config`,
`copilot help permissions`, `copilot instruction --help`; `reg query` nas chaves de política citadas em §4; listagem
de `%ProgramFiles%\GitHubCopilot`, `C:\ProgramData\GitHub\Copilot\policy.d` e `%LOCALAPPDATA%\copilot\managed-settings`;
busca de `github.copilot.chat.organization*` no `settings.json` do VS Code.
