# Pesquisa 41: o contrato pelo próprio MCP (Codex, Copilot CLI, Copilot no VS Code)

Pesquisa em fonte primária, feita em 2026-10-12. Li texto bruto com `curl` (raw.githubusercontent.com,
api.github.com, a API de artigos do docs.github.com e os `.md` das páginas de documentação). Nada foi
instalado, executado ou testado. É saída de modelo: confira as citações antes de decidir.

Ticket: `.scratch/context-hub/issues/41-contrato-pelo-mcp-pesquisa.md`. Fatos de partida:
`pesquisa-37-portas/porta-7-cliente-mcp.md` (os três canais do protocolo) e `testes-38-portas/grupo-c-es617.md`
(o `instructions` do es617, com um `AGENTS.md` de teste de 5.000 caracteres, chegou ao Claude Code 2.1.296
cortado depois de uns 3.300 caracteres, e **não** chegou ao Codex 0.161.0 nem ao Copilot CLI 1.0.94).

## Pergunta

Um cliente que só alcança o hub pelo MCP de um par: por quais canais do próprio servidor MCP o texto do
contrato (`AGENTS.md`) chega ao modelo, no Codex CLI, no Copilot CLI e no Copilot do VS Code? Por harness:
(C) a descrição das ferramentas chega ao modelo, e com que limite; (D) prompts e resources do MCP, e se algum
entra no contexto sem ação do usuário; (E) o campo `instructions` do `initialize`.

## O que a especificação do MCP diz (base comum)

Especificação 2025-11-25, fonte bruta em
`https://raw.githubusercontent.com/modelcontextprotocol/modelcontextprotocol/main/`.

- **`instructions`** (`schema/2025-11-25/schema.ts`, `InitializeResult`): *"Instructions describing how to use
  the server and its features. This can be used by clients to improve the LLM's understanding of available
  tools, resources, etc. It can be thought of like a "hint" to the model. For example, this information MAY be
  added to the system prompt."* Campo opcional; o cliente decide.
- **Descrição de ferramenta** (mesmo arquivo, `interface Tool`): *"A human-readable description of the tool.
  This can be used by clients to improve the LLM's understanding of available tools. It can be thought of like
  a "hint" to the model."* A especificação não fixa tamanho máximo.
- **Ferramentas** (`docs/specification/2025-11-25/server/tools.mdx`): *"Tools in MCP are designed to be
  **model-controlled**, meaning that the language model can discover and invoke tools automatically"*.
- **Resources** (`.../server/resources.mdx`): *"Resources in MCP are designed to be **application-driven**, with
  host applications determining how to incorporate context based on their needs."* A lista de exemplos inclui
  *"Implement automatic context inclusion, based on heuristics or the AI model's selection"*.
- **Prompts** (`.../server/prompts.mdx`): *"Prompts are designed to be **user-controlled**, meaning they are
  exposed from servers to clients with the intention of the user being able to explicitly select them for use."*

Lembrete da porta 7: o es617 (upstream) só registra ferramentas e `instructions`; não tem resources nem prompts.
Os canais D só existem se o fork os acrescentar.

---

## 1. OpenAI Codex CLI

Fontes: documentação `https://developers.openai.com/codex/mcp.md` (redireciona para
`https://learn.chatgpt.com/docs/extend/mcp.md?surface=cli`) e o código em `github.com/openai/codex`. Conferi o
código na tag `rust-v0.161.0` (publicada em 2026-10-07; é a versão do teste do grupo C) e em `main`
(2026-10-12); os trechos citados são iguais nas duas.

### E. `instructions` do servidor

**Documentação.** *"**Server instructions**: Codex reads the MCP `instructions` field returned during
initialization and uses it as server-wide guidance alongside the server's tools."* e *"If you build or maintain
an MCP server for Codex, use `instructions` for cross-tool workflows, constraints, and rate limits that apply
across the server. Keep the first 512 characters self-contained so the most important guidance is available
when Codex is deciding how to use the server."* (https://developers.openai.com/codex/mcp.md)

**Código: o texto vira a descrição do "namespace" das ferramentas do servidor.**
- `codex-rs/codex-mcp/src/rmcp_client.rs` guarda `initialize_result.instructions` e o passa a cada ferramenta;
  para servidores comuns: `namespace_description: server_instructions.map(str::to_string),` com o comentário
  *"Converts a regular MCP tool by removing reserved connector metadata, keeping its raw tool name, and using the
  MCP server name and instructions for the model-visible namespace."*
  (https://raw.githubusercontent.com/openai/codex/rust-v0.161.0/codex-rs/codex-mcp/src/rmcp_client.rs, linha 855)
- `codex-rs/core/src/tools/handlers/mcp.rs` monta a ferramenta como `ToolSpec::Namespace(ResponsesApiNamespace {
  name: ..., description: take_bytes_at_char_boundary(&description, MAX_MCP_NAMESPACE_DESCRIPTION_BYTES) ... })`,
  com `const MAX_MCP_NAMESPACE_DESCRIPTION_BYTES: usize = 512 * 1024;` e, só para MCP de "agent plugin",
  `const MAX_AGENT_PLUGIN_MCP_NAMESPACE_DESCRIPTION_BYTES: usize = 1_000;`
  (https://raw.githubusercontent.com/openai/codex/rust-v0.161.0/codex-rs/core/src/tools/handlers/mcp.rs, linhas 48-49 e 527).
- Quando as ferramentas MCP ficam adiadas (busca de ferramentas ligada), o mesmo texto entra na descrição da
  ferramenta `tool_search`: *"You have access to tools from the following sources:\n{source_descriptions}"*, uma
  linha `- <servidor>: <instructions>` por servidor, com teto agregado
  `const MAX_TOOL_SEARCH_SOURCE_DESCRIPTION_BYTES: usize = 512 * 1024;`
  (https://raw.githubusercontent.com/openai/codex/rust-v0.161.0/codex-rs/core/src/tools/handlers/tool_search_spec.rs, linhas 8 e 87).
- Histórico: o PR #35941 (2026-07-29) limitou a descrição do namespace a 1.000 bytes e a lista do `tool_search`
  a 4 KiB; o PR #37066 (2026-08-05) subiu o agregado para 512 KiB porque *"The 4 KiB aggregate limit can truncate
  source metadata before it reaches the model through the tool search description."*
  (https://api.github.com/repos/openai/codex/pulls/35941 e .../37066). Na 0.161.0 o teto do namespace comum já é
  512 KiB.

**Confronto com o teste.** O código da 0.161.0 envia o `instructions` na requisição, como descrição do namespace
(ferramentas diretas) ou dentro da descrição do `tool_search` (ferramentas adiadas). O teste do grupo C pediu ao
modelo que citasse os marcadores e ele respondeu "NONE"/"NOT PRESENT". As duas coisas podem ser verdade ao mesmo
tempo: o Codex põe o texto no campo `description` de um objeto `namespace` da Responses API, e como o servidor
da OpenAI apresenta essa descrição ao modelo não está no código aberto.
- **Não verificado:** como a Responses API mostra ao modelo a descrição de um namespace, e se a mostra inteira.
- **Não verificado:** de onde vem o número 512 da documentação; não achei truncamento em 512 caracteres no código
  para servidores comuns.
- **Precisa de teste:** capturar a requisição que o Codex 0.161.0 manda (log de depuração ou proxy) e ver se o
  texto do `AGENTS.md` está no `namespace.description` ou no `tool_search`; repetir a pergunta ao modelo sobre "a
  descrição do namespace <servidor>", em vez de "as instruções do servidor".

### C. Descrição das ferramentas

- Para servidor MCP comum, a descrição passa sem corte: `parse_mcp_tool` chama
  `parse_mcp_tool_with_description_limit(tool, /*description_limit*/ None, ...)`. O corte de 1.000 bytes
  (`const MAX_MCP_TOOL_DESCRIPTION_BYTES: usize = 1_000;`) vale só para `parse_agent_plugin_mcp_tool`
  (https://raw.githubusercontent.com/openai/codex/rust-v0.161.0/codex-rs/tools/src/mcp_tool.rs, linhas 9-35).
- O esquema de entrada pode ter orçamento por servidor (`tool_input_schema_max_bytes`, lido em
  `codex-rs/core/src/mcp_tool_exposure.rs`); o nome dessa chave não aparece na página de documentação lida.
- Com busca de ferramentas, as ferramentas MCP ficam adiadas e a descrição só chega depois do `tool_search`:
  `let exposure = if search_tool_enabled { ToolExposure::Deferred } else { ToolExposure::Direct };`
  (`codex-rs/core/src/mcp_tool_exposure.rs` em `main`). Nesse caso, o que chega no início é a linha do servidor no
  `tool_search` (o `instructions`), não a descrição de cada ferramenta.
- **Não verificado:** quais modelos ligam a busca de ferramentas (`model_info.supports_search_tool`).

### D. Prompts e resources

- **Resources: sim, como ferramentas que o modelo chama.** O Codex registra `list_mcp_resources`,
  `list_mcp_resource_templates` e `read_mcp_resource` sempre que há servidor MCP configurado
  (`if context.mcp.has_servers() || ...` em `codex-rs/core/src/tools/spec_plan.rs`). Descrição dada ao modelo:
  *"Lists resources provided by MCP servers. Resources allow servers to share data that provides context to
  language models, such as files, database schemas, or application-specific information. Prefer resources over
  web search when possible."*
  (https://raw.githubusercontent.com/openai/codex/rust-v0.161.0/codex-rs/core/src/tools/handlers/mcp_resource_spec.rs).
  Não há inclusão automática: o conteúdo só entra se o modelo chamar `read_mcp_resource`. Não exige ação do
  usuário, mas exige decisão do modelo.
- **Prompts: não achei suporte.** O cliente MCP do Codex (`codex-rs/rmcp-client/src/rmcp_client.rs`, tag
  0.161.0) expõe `list_tools`, `list_tools_with_connector_ids`, `list_resources`, `list_resource_templates` e
  `read_resource`, e nenhum método de prompts. A lista "Supported MCP features" da documentação não cita prompts
  nem resources.
- **Não verificado:** se algum outro módulo do Codex (fora de `codex-mcp`, `rmcp-client` e `core/src/tools`, que
  li) usa `prompts/list`.

---

## 2. GitHub Copilot CLI

O código do Copilot CLI não é aberto: o repositório `github/copilot-cli` só tem `README.md`, `changelog.md` e
`install.sh`. Fontes: a referência de comandos
(https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-command-reference, texto via
`https://docs.github.com/api/article/body?pathname=...`), a página de gestão de contexto
(https://docs.github.com/en/copilot/concepts/agents/copilot-cli/context-management) e o changelog
(https://raw.githubusercontent.com/github/copilot-cli/main/changelog.md, última versão 1.0.95 de 2026-10-09).

### E. `instructions` do servidor

**A documentação confirma o resultado do teste e diz por quê.** Opção da linha de comando:
*"`--allow-all-mcp-server-instructions` | Include initialization instructions from all MCP servers in the system
prompt. By default, only allowlisted server instructions are included up front; other servers' instructions are
retrieved on demand."* (referência de comandos).

Changelog:
- 0.0.400 (2026-01-30): *"Add MCP server instructions support"*.
- 1.0.5 (2026-03-13): *"Add experimental embedding-based dynamic retrieval of MCP and skill instructions per turn"*.
- 1.0.66 (2026-06-30): *"Add --allow-all-mcp-server-instructions to optionally include instructions from all MCP
  servers in system prompts"*.
- 1.0.92 (2026-10-05): *"MCP tools recover within the same turn when server instructions change"*.

Ou seja: por padrão, o `instructions` de um servidor fora da lista não vai para o prompt de sistema no início
da sessão; com `--allow-all-mcp-server-instructions`, vai.
- **Não verificado:** que lista é essa ("allowlisted"). A referência também descreve uma allowlist de MCP para
  empresas (*"GitHub Enterprise organizations can enforce an allowlist of permitted MCP servers"*), mas a frase da
  opção não diz se é a mesma.
- **Não verificado:** como funciona o "retrieved on demand" (recuperação por embeddings a cada turno, pela entrada
  de 1.0.5?) e se o texto chega inteiro ou cortado.
- **Precisa de teste:** repetir o grupo C com `--allow-all-mcp-server-instructions` e ver quantos marcadores
  chegam; e sem a opção, com uma pergunta ligada ao conteúdo, ver se a recuperação sob demanda traz algum trecho.

### C. Descrição das ferramentas

- A página de contexto diz que as definições de ferramentas ficam no contexto: *"**System instructions and tool
  definitions**: The built-in instructions that tell Copilot how to behave, plus the schemas of all available
  tools. These are always present and take up a fixed portion of the context window."* A referência cita o nome:
  *"MCP server names and tool names are sanitized before being sent to the model."* e *"The combined name
  (`serverName-toolName`) is capped at 64 characters."*
- Há busca de ferramentas com adiamento: changelog 1.0.49, *"Experimental: Tool search with deferred loading for
  MCP and external tools"*; campo de configuração *"`deferTools` | No | `"auto"` (default) or `"never"`. Set to
  `"never"` to keep this server's tools always visible even when tool search is active."*
- **Não verificado:** limite de tamanho ou corte da descrição das ferramentas MCP. Nenhuma página lida fala
  disso; o changelog só cita *"Remove unnecessary whitespace from tool descriptions"* (0.0.359).
- **Não verificado:** para que modelos a busca de ferramentas fica ligada no modo `"auto"` (o changelog cita
  modelos Claude em 1.0.6 e *"Enable tool search for Claude Haiku 4.5+"* em 1.0.72).

### D. Prompts e resources

- **Resources:** o changelog 1.0.70 (2026-07-09) traz *"Add paginated session.mcp.resources read/list/listTemplates
  RPCs for MCP server resources"*: chamadas do SDK/servidor do CLI. Nenhuma página lida descreve o modelo lendo
  resources nem o usuário anexando um resource.
- **Prompts:** nenhuma página lida nem entrada do changelog cita prompts do MCP no Copilot CLI.
- **Não verificado:** se o modelo do Copilot CLI tem uma ferramenta para ler resources do MCP, e se prompts do
  MCP viram comandos de barra. Sem código aberto, só um teste resolve.

---

## 3. GitHub Copilot no VS Code

Fontes: documentação em `microsoft/vscode-docs` (texto bruto) e código em `microsoft/vscode`, que hoje contém a
extensão do Copilot Chat em `extensions/copilot/` (o repositório `microsoft/vscode-copilot-chat` está arquivado).
Código lido em `main` em 2026-10-12.

### E. `instructions` do servidor

**Documentação.** O guia para quem escreve servidores lista *"Server instructions"* entre as capacidades MCP
suportadas, sem dizer como são usadas
(https://raw.githubusercontent.com/microsoft/vscode-docs/main/api/extension-guides/ai/mcp.md, seção
"VS Code supports the following MCP capabilities").

**Código: entra no prompt do agente, inteiro, numa tag por servidor.**
- O VS Code guarda o `instructions` como metadado do servidor e o passa como fonte das ferramentas:
  `instructions: metadata?.serverInstructions,` em `mcpServerToSourceData`
  (https://raw.githubusercontent.com/microsoft/vscode/main/src/vs/workbench/contrib/mcp/common/mcpTypesUtils.ts).
- A extensão do Copilot põe esse texto no prompt do modo agente:

  ```tsx
  export class McpToolInstructions extends PromptElement<...> {
    render() {
      const instructions = new Map<string, string>();
      for (const tool of this.props.tools) {
        if (tool.source instanceof LanguageModelToolMCPSource && tool.source.instructions) {
          // MCP tools are labelled `mcp_servername_toolname`, give instructions for `mcp_servername` prefixes
          const [, serverLabel] = tool.name.split('_');
          instructions.set(`mcp_${serverLabel}`, tool.source.instructions);
          ...
      <Tag name='instruction' attrs={{ forToolsWithPrefix: prefix }}>{instruction}</Tag>
  ```

  (https://raw.githubusercontent.com/microsoft/vscode/main/extensions/copilot/src/extension/prompts/node/agent/defaultAgentInstructions.tsx,
  linhas 385-400). O elemento aparece nos prompts das famílias de modelo lidas (padrão, Anthropic, Gemini,
  OpenAI/GPT-5.x, xAI, zAI), sempre como `{this.props.availableTools && <McpToolInstructions tools={this.props.availableTools} />}`.
- Não achei corte de tamanho nesse elemento: o texto vai inteiro.
- Condição lida no código: o texto entra se ao menos uma ferramenta daquele servidor estiver em `availableTools`
  (as ferramentas ligadas no seletor de ferramentas). A mesma lista `availableTools` inclui as ferramentas
  adiadas pela busca de ferramentas (`hasDeferredTool(...)` testa `availableTools` em
  `extensions/copilot/src/extension/prompts/node/agent/toolSearchInstructions.tsx`).
- **Não verificado:** se algum limite de orçamento de prompt (prompt-tsx) corta a tag quando o prompt fica grande.
- **Precisa de teste:** o grupo C não testou o VS Code. Repetir com o `AGENTS.md` de 5.000 caracteres e os
  marcadores.

### C. Descrição das ferramentas

- O VS Code registra a descrição do MCP como descrição para o modelo, sem corte:
  `modelDescription: tool.definition.description ?? '',`
  (https://raw.githubusercontent.com/microsoft/vscode/main/src/vs/workbench/contrib/mcp/common/mcpLanguageModelToolContribution.ts, linha 151).
- O normalizador de esquema da extensão corta em 1.024 caracteres as descrições **dentro do esquema de
  parâmetros**, e só para modelos da família `gpt-4`: *"object description is too long (truncated to
  ${gpt4oMaxStringLength} chars)"*, com `const gpt4oMaxStringLength = 1024;` e
  `const isGpt4ish = (family: string) => family.startsWith('gpt-4');`
  (https://raw.githubusercontent.com/microsoft/vscode/main/extensions/copilot/src/extension/tools/common/toolSchemaNormalizer.ts).
  A descrição da ferramenta em si só ganha *"No description provided"* quando vem vazia.
- Muitas ferramentas: a extensão agrupa ferramentas em "virtual tools" acima de
  `START_GROUPING_AFTER_TOOL_COUNT = HARD_TOOL_LIMIT / 2; // 64, currently` (`virtualToolsConstants.ts`) e tem
  busca de ferramentas adiadas (`toolSearchTool.ts`). Ferramenta agrupada ou adiada não manda a descrição no
  início.
- **Não verificado:** se o backend do Copilot corta descrições longas.

### D. Prompts e resources

Documentação (https://raw.githubusercontent.com/microsoft/vscode-docs/main/docs/agent-customization/mcp-servers.md):
- *"**Resources** | Access data from MCP servers as context in your prompts, such as files, database tables, or
  API responses. Resources provide read-only context that you attach to a chat request. | In the Chat view,
  select **Add Context** > **MCP Resources**. You can also use the **MCP: Browse Resources** command."*
- *"**Prompts** | Use preconfigured prompt templates from MCP servers to standardize common tasks. ... | Type
  `/<MCP server>.<prompt>` in the chat input."*

O guia para servidores repete: prompts são *"reusable chat prompt templates that users can invoke in chat by
using a slash command"* e *"When you include a resource type in the prompt response, VS Code attaches that
resource as context to the chat prompt."* (`api/extension-guides/ai/mcp.md`).

Os dois exigem ação do usuário. Uma ferramenta pode devolver um resource no resultado (o VS Code trata
`resource_link` e `resource` em `mcpLanguageModelToolContribution.ts`), mas isso depende de o modelo chamar a
ferramenta.
- **Não verificado:** se o modo agente tem uma ferramenta própria para o modelo listar ou ler resources do MCP
  sem o usuário anexar.

---

## 4. Claude Code (só para comparação)

Documentação https://code.claude.com/docs/en/mcp.md:
- *"Only tool names and server instructions load at session start"* (com busca de ferramentas).
- *"Claude Code truncates each tool description and each server's instructions at 2,048 characters by default.
  Keep them concise, and put critical details near the start."* e *"To change the limit for every MCP server in
  your session, set `CLAUDE_CODE_MAX_MCP_DESCRIPTION_LENGTH` to a number of characters. This variable requires
  Claude Code v2.1.280 or later."*
- Resources: *"Use the format `@server:protocol://resource/path` to reference a resource"*. Prompts: *"MCP servers
  can expose prompts that become available as commands in Claude Code."*
- **Não verificado:** por que o teste viu o corte entre 3.329 e 4.829 caracteres, e não em 2.048 (a variável
  estava definida? a contagem é outra?).

---

## Tabela final: harness × canal

"Sem ação" = entra no contexto sem o usuário fazer nada.

| Canal | Codex CLI 0.161.0 | Copilot CLI | Copilot no VS Code | Claude Code (comparação) |
|---|---|---|---|---|
| `instructions` do `initialize` | Doc: usado como orientação do servidor. Código: vai na requisição como descrição do namespace (até 512 KiB) ou no `tool_search`. Teste: o modelo não citou o texto. Como a API apresenta o namespace: **não verificado**; **precisa de teste** | Doc: por padrão só servidores "allowlisted" vão ao prompt; os outros são "retrieved on demand". `--allow-all-mcp-server-instructions` põe todos. Teste (sem a opção): não chegou. Com a opção: **precisa de teste** | Código: vai ao prompt do agente numa tag `<instruction forToolsWithPrefix="mcp_<servidor>">`, sem corte achado, se alguma ferramenta do servidor estiver ligada. **Precisa de teste** | Doc: carrega no início, cortado em 2.048 caracteres por padrão (ajustável). Teste: chegou, cortado em uns 3.300 |
| Descrição das ferramentas (C) | Sem corte para servidor comum (1.000 bytes só para "agent plugin"); adiada quando há busca de ferramentas | Definições de ferramentas ficam no contexto (doc); adiamento com `deferTools`; limite da descrição **não verificado** | Sem corte da descrição; 1.024 caracteres nas descrições do esquema em modelos `gpt-4*`; agrupamento acima de 64 ferramentas | 2.048 caracteres por padrão |
| Resources (D) | Ferramentas `list_mcp_resources` / `read_mcp_resource` para o modelo; sem inclusão automática | Só RPCs do SDK no changelog; uso pelo modelo ou usuário **não verificado** | O usuário anexa ("Add Context > MCP Resources"); sem inclusão automática | O usuário menciona com `@`; ferramentas de leitura para o modelo |
| Prompts (D) | Sem suporte achado no cliente MCP | **Não verificado** (nenhuma fonte cita) | Comando de barra `/<servidor>.<prompt>`; exige o usuário | Viram comandos; exigem o usuário |

## Não verificado (lista consolidada)

- Codex: como a Responses API apresenta ao modelo a descrição de um namespace; origem do "512 characters" da doc;
  que modelos ligam a busca de ferramentas; uso de prompts fora dos módulos lidos.
- Copilot CLI: o que é a lista "allowlisted" das instruções; como funciona o "retrieved on demand"; limite de
  tamanho do `instructions` e das descrições; suporte a resources e prompts do MCP para o modelo ou o usuário.
- VS Code: corte por orçamento de prompt na tag `<instruction>`; corte de descrições no backend do Copilot;
  ferramenta própria do agente para ler resources.
- Claude Code: a diferença entre o corte documentado (2.048) e o observado (uns 3.300).

## Precisa de teste

- Codex 0.161.0: capturar a requisição e achar o texto do `AGENTS.md` (namespace ou `tool_search`); perguntar ao
  modelo pela descrição do namespace.
- Copilot CLI 1.0.94 ou posterior: repetir o grupo C com `--allow-all-mcp-server-instructions`; sem a opção, ver
  se a recuperação sob demanda traz algum trecho.
- Copilot no VS Code: repetir o grupo C (5.000 caracteres, marcadores) com uma ferramenta do servidor ligada.

## Fontes

Texto bruto lido em 2026-10-12.
- Especificação MCP 2025-11-25: `https://raw.githubusercontent.com/modelcontextprotocol/modelcontextprotocol/main/schema/2025-11-25/schema.ts`;
  `.../docs/specification/2025-11-25/server/tools.mdx`, `.../resources.mdx`, `.../prompts.mdx`.
- Codex, documentação: https://developers.openai.com/codex/mcp.md (redireciona para https://learn.chatgpt.com/docs/extend/mcp.md?surface=cli).
- Codex, código (tag `rust-v0.161.0` e `main`), em `https://raw.githubusercontent.com/openai/codex/<ref>/`:
  `codex-rs/codex-mcp/src/rmcp_client.rs`, `codex-rs/core/src/tools/handlers/mcp.rs`,
  `codex-rs/core/src/tools/handlers/tool_search_spec.rs`, `codex-rs/tools/src/mcp_tool.rs`,
  `codex-rs/tools/src/tool_spec.rs`, `codex-rs/tools/src/responses_api.rs`, `codex-rs/core/src/mcp_tool_exposure.rs`,
  `codex-rs/core/src/tools/spec_plan.rs`, `codex-rs/core/src/tools/handlers/mcp_resource_spec.rs`,
  `codex-rs/rmcp-client/src/rmcp_client.rs`. PRs: https://github.com/openai/codex/pull/35941 e https://github.com/openai/codex/pull/37066.
  Release: https://github.com/openai/codex/releases/tag/rust-v0.161.0.
- Copilot CLI: https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-command-reference ;
  https://docs.github.com/en/copilot/concepts/agents/copilot-cli/context-management ;
  https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-mcp-servers (texto via
  `https://docs.github.com/api/article/body?pathname=...`); https://raw.githubusercontent.com/github/copilot-cli/main/changelog.md.
- VS Code, documentação: https://raw.githubusercontent.com/microsoft/vscode-docs/main/docs/agent-customization/mcp-servers.md ;
  https://raw.githubusercontent.com/microsoft/vscode-docs/main/api/extension-guides/ai/mcp.md.
- VS Code, código em `https://raw.githubusercontent.com/microsoft/vscode/main/`:
  `src/vs/workbench/contrib/mcp/common/mcpTypesUtils.ts`, `.../mcpServer.ts`, `.../mcpLanguageModelToolContribution.ts`;
  `extensions/copilot/src/extension/prompts/node/agent/defaultAgentInstructions.tsx`,
  `.../toolSearchInstructions.tsx`, `extensions/copilot/src/extension/tools/common/toolSchemaNormalizer.ts`,
  `.../virtualTools/virtualToolsConstants.ts`, `extensions/copilot/src/extension/tools/node/toolSearchTool.ts`.
- Claude Code: https://code.claude.com/docs/en/mcp.md.
