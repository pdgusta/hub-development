# Porta 7: cliente pelo MCP de um par

Pesquisa em fonte primária, feita em 2026-10-10 com `curl -sL` sobre o texto bruto. Nada foi instalado nem executado. Saída de modelo: confira as citações antes de decidir.

## Pergunta

Cada par roda CouchDB + o MCP do es617 (um fork) por HTTP. Um cliente (sandbox ou máquina de passagem) entra na tailnet com chave efêmera e usa o MCP de um par com token, por padrão só leitura (`READ_ONLY=true`). O que as fontes sustentam sobre: (1) o MCP do es617; (2) como Claude Code, Codex e Copilot configuram MCP remoto por HTTP com cabeçalho de token; (3) chave efêmera, tags e grants no Tailscale; (4) como um cliente que só usa o MCP recebe o AGENTS.md do hub.

## Respostas (com citações)

### 1. O MCP do es617

Repositório oficial: https://github.com/es617/obsidian-sync-mcp (texto lido em `main`, ver Fontes). O fork do Gustavo pode divergir; tudo abaixo é do upstream.

**1.1 Transporte HTTP.** `main.ts` inicia FastMCP em HTTP:
`server.start({ transportType: "httpStream", httpStream: { port: PORT, endpoint: "/mcp", host: process.env.HOST ?? "0.0.0.0" } });`
README: *"Both modes expose the same MCP tools over HTTP"* e *"Your MCP endpoint is `http://localhost:8787/mcp`."* Porta padrão `8787` (`PORT`), bind padrão `0.0.0.0` (`HOST`; *"`127.0.0.1` to restrict to localhost"*). O README também cita o modo de teste com o Inspector: *"Set transport to **Streamable HTTP**, enter `http://localhost:8787/mcp`"*.

**1.2 Autenticação por token.** README: *"Set `MCP_AUTH_TOKEN` to a password to enable authentication"* e *"For non-OAuth clients (curl, MCP Inspector, custom agents), you can also pass the token directly as `Authorization: Bearer <MCP_AUTH_TOKEN>`."* O código (`main.ts`) confirma: `const expected = \`Bearer ${AUTH_TOKEN}\`; if (header && safeEqual(header, expected)) { return { authenticated: true }; }` e, se falhar, responde 401 com `WWW-Authenticate: Bearer resource_metadata=...`. Observação lida no código: há uma única variável `MCP_AUTH_TOKEN` comparada por igualdade; não há lista de tokens nem token por cliente. Sem a variável: *"Without `MCP_AUTH_TOKEN`, the server runs without authentication — suitable for local use or behind a private network."* e o README diz que, sem token, o servidor só aceita `Host` local salvo `MCP_ALLOWED_HOSTS` (*"No-auth mode rejects any other Host to block browser DNS-rebinding; localhost is always allowed. Ignored when `MCP_AUTH_TOKEN` is set."*). O `main.ts` imprime no modo sem token: *"any non-browser client that can reach this port has full vault access"*.

**1.3 O que READ_ONLY desliga.** README: *"Set to `true` to disable all write tools (`write_note`, `edit_note`, `delete_note`, `move_note`). Only read tools are exposed via MCP, and the vault backend rejects writes as well."* e *"This protects the vault from MCP clients; it is not a database-level guarantee. To make CouchDB itself refuse writes, use CouchDB-side controls, such as a `validate_doc_update` function that rejects the server's CouchDB user."* Código: em `tools.ts` as quatro ferramentas de escrita são registradas com `if (!readOnly) server.addTool(...)`; `vault-readonly.ts` embrulha o backend com `writeNote: deny, deleteNote: deny, moveNote: deny` e a mensagem *"READ_ONLY is enabled: the vault cannot be modified."* `READ_ONLY` é lida uma vez de `process.env` (`const READ_ONLY = process.env.READ_ONLY === "true";`): vale para a instância inteira, não por token. `WRITE_FOLDERS` é a alternativa parcial: *"the whole vault stays readable but `write_note`, `edit_note`, `delete_note`, and `move_note` refuse paths outside these folders"*; é *"Ignored when `READ_ONLY=true`"*.

**1.4 Duas instâncias.** README, "Known limitations": *"Single vault per instance. Each server connects to one vault. For multiple vaults, run multiple instances on different ports."* Variáveis `PORT` e `DATA_DIR` (*"Directory for persisted data (metadata index, auth tokens)"*) permitem separar instâncias. O README não trata explicitamente de duas instâncias sobre o mesmo CouchDB (uma `READ_ONLY=true`, outra não); ver Precisa de teste. Limitação relacionada: *"Single machine on Fly.io. Auth state is in-memory, so multiple machines break the OAuth flow."* (contexto Fly.io).

**1.5 Ferramentas para achar conteúdo.** Tabela do README:
- `read_note`: *"Read a note's markdown content by path"* (`path`: *"Vault-relative path to the note, e.g. 'daily/2026-03-23.md'"*).
- `list_folders`: *"List all folders in the vault with note counts — use to discover folder names"*.
- `list_notes`: *"List notes with timestamps. Filter by folder, name, tag, or date. Sort by name or modified."* (parâmetros no código: `folder`, `name`, `tag`, `sort_by`, `modified_after`, `limit`).
- `search_notes`: *"Search note text for terms (OR, case-insensitive substrings); paths and frontmatter titles are searched first. Filter by folder, tag, or date. Returns paths with one context line each, never the note body"*.
- `list_tags`, `get_note_metadata` (frontmatter, tags, links, backlinks), e as de escrita `write_note`, `edit_note`, `delete_note`, `move_note`.

**Divergência com a pesquisa 26.** `exploracao/anexos/pesquisa-26-montagem.md` registra que o es617 *"não tem busca de texto (só metadados)"*, citando `ARCHITECTURE.md`. O README e o `tools.ts` atuais em `main` descrevem `search_notes` com busca em conteúdo e índice. Vale reconferir a pesquisa 26 (a data do commit de `search_notes` não foi verificada).

**1.6 O que o es617 expõe além de ferramentas.** `grep` em `main.ts` e `tools.ts` por `addResource`, `addPrompt` e `resources` não retornou nada: o servidor registra só ferramentas. O canal de texto para o cliente é o `instructions` (ver 4.2).

### 2. Configurar MCP remoto por HTTP com cabeçalho de token

**Claude Code** (https://code.claude.com/docs/en/mcp.md):
- Comando: *"claude mcp add --transport http secure-api https://api.example.com/mcp \ --header "Authorization: Bearer your-token""*.
- Escopos: *"`local` (default): available only to you in the current project; `project`: shared with everyone in the project via the `.mcp.json` file; `user`: available to you across all projects"*. Tabela: Local em `~/.claude.json`, Project em `.mcp.json` na raiz do projeto, User em `~/.claude.json`. Precedência: *"1. Local scope 2. Project scope 3. User scope"*.
- Arquivo de projeto com expansão de variável (evita gravar o token): `"type": "http", "url": "${API_BASE_URL:-https://api.example.com}/mcp", "headers": { "Authorization": "Bearer ${API_KEY}" }`.
- Cuidado documentado: *"In a remote server's `url` and `headers`, Claude Code reads credential variables from your environment as empty rather than expanding them"* (cobre variáveis de credencial do próprio Claude Code/nuvem, como `ANTHROPIC_AUTH_TOKEN`; a lista exata está na seção "Credential variables that read as empty" da página, não transcrita aqui). Um nome próprio como `API_KEY` aparece no exemplo oficial.
- Aprovação: *"Claude Code prompts for approval in interactive sessions before using project-scoped servers from `.mcp.json` files"*; em `claude -p`, Agent SDK e sessões na nuvem *"Claude Code can't show that prompt: it loads project-scoped servers without asking."*
- `Authorization` configurado e rejeitado: *"Claude Code reports the connection as failed instead of falling back to OAuth."*

**Codex** (https://developers.openai.com/codex/mcp.md, que redireciona 308 para `https://learn.chatgpt.com/docs/extend/mcp.md?surface=cli`):
- *"Codex stores MCP configuration in `config.toml` ... By default this is `~/.codex/config.toml`, but you can also scope MCP servers to a project with `.codex/config.toml` (trusted projects only)."*
- Servidor HTTP: `[mcp_servers.<nome>]` com `url` (obrigatório), `bearer_token_env_var` (*"Environment variable name for a bearer token to send in `Authorization`"*), `http_headers` (*"Map of header names to static values"*), `env_http_headers` (*"values pulled from the environment"*).
- Exemplo oficial: `[mcp_servers.figma] url = "https://mcp.figma.com/mcp" bearer_token_env_var = "FIGMA_OAUTH_TOKEN"`.
- Filtro de ferramentas por servidor: `enabled_tools` (*"Tool allow list"*), `disabled_tools`, `default_tools_approval_mode` (valores `auto`, `prompt`, `writes`, `approve`).
- Instruções do servidor: *"Codex reads the MCP `instructions` field returned during initialization and uses it as server-wide guidance alongside the server's tools."* e *"Keep the first 512 characters self-contained"*.

**GitHub Copilot CLI** (https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-mcp-servers):
- Usuário: *"The server is added to the user configuration at `~/.copilot/mcp-config.json`."* `copilot mcp add` aceita `--header "HEADER: VALUE"` (*"Set HTTP headers for remote servers. Repeat for multiple headers."*).
- Exemplo oficial em JSON: `"context7": { "type": "http", "url": "https://mcp.context7.com/mcp", "headers": { "CONTEXT7_API_KEY": "YOUR-API-KEY" }, "tools": ["*"] }`.
- Projeto: *".mcp.json (in any directory from your working directory up to the repository root)"* e *".github/mcp.json — Shared configuration that is committed to the repository"*; *"Project-level definitions also take precedence over those in `~/.copilot/mcp-config.json`."*
- *"The `.vscode/mcp.json` file for VS Code is not read by Copilot CLI."*

**VS Code (Copilot no editor)** (https://code.visualstudio.com/docs/agent-customization/mcp-servers, fonte bruta em https://raw.githubusercontent.com/microsoft/vscode-docs/main/docs/agent-customization/mcp-servers.md): *"Workspace, VS Code format: create or open `.vscode/mcp.json` ... top-level `servers` object"*; *"Workspace, portable format: create `.mcp.json` at the root of your project ... top-level `mcpServers` object"*; *"User profile: run the **MCP: Open User Configuration** command"*. O exemplo oficial de servidor HTTP na página não mostra cabeçalho (só `"type": "http", "url"`); o cabeçalho no VS Code não foi confirmado nesta página (ver Não verificado).

### 3. Tailscale: chave efêmera, tags, grants

**Chave efêmera** (https://tailscale.com/kb/1111/ephemeral-nodes):
- *"They are auto-removed from your network after a short period of inactivity. The next time an ephemeral node is created, it will have a new IP address."*
- *"They are immediately removed from your network if you run `tailscale logout`."*
- *"They can only be created using ephemeral auth keys (not through the regular authentication flow) or by running the `tailscaled` daemon with the `state=mem:` flag."*
- Quando a sandbox some: *"Ephemeral devices are auto-removed anywhere normally from 30 to 60 minutes after the last activity. This timeframe is subject to change"*; para remover já: `tailscale logout` (*"add `tailscale logout` as a last step in your ephemeral node deployment script"*). Com `--state=mem:` e Tailscale v1.30 ou posterior: *"when the device exits, the `tailscaled` daemon itself performs `tailscale logout` which immediately removes the device from your tailnet."*
- Cobrança: *"If an ephemeral node is present in the tailnet for four or more hours, it will not count against your balance of ephemeral minutes, and will count as a standard tagged device instead."* e *"Ephemeral node usage is included at no cost up to a monthly limit (measured in minutes), which varies by pricing plan."*
- Recomendação oficial: *"consider using an ephemeral tagged auth key, and update access control policies to restrict what tagged devices can access."*

**Chaves de autenticação** (https://tailscale.com/kb/1085/auth-keys):
- *"Auth keys are available for all plans."* Registro: `sudo tailscale up --auth-key=tskey-...`.
- Validade: *"You can choose the number of days, between 1 and 90 inclusive ... If you don't specify an expiry time, the auth key will expire after the maximum of 90 days."*
- Tipos: *"One-off, for one-time use"* e *"Reusable, for multiple uses"* (com o alerta *"Be very careful with reusable keys! These can be very dangerous if stolen."*).
- Tags na chave: *"if you use tags with an auth key, after a device logs in as the user who generated the auth key, the device assumes the identity of the auth key's tags."*
- Boa prática: *"Ephemeral, for authenticating ephemeral nodes as part of short-lived workloads ... containers or Lambda functions should use an ephemeral key to connect."*
- Revogar: *"Revoking a key does not deauthorize nodes using the key. To deauthorize a node, delete it from the Machines page."*
- Quem gera: *"You must be an Owner, Admin, IT admin, or Network admin of a tailnet to generate a key."*

**Tags** (https://tailscale.com/kb/1068/acl-tags, trecho extraído do HTML): *"Applying a tag to a device removes any user-based authentication."*, *"Tags are defined in the tailnet policy file in the `tagOwners` section. Only designated tag owners can apply tags to devices"*, *"You must be an Owner, Admin, or Network admin of a tailnet to define a tag in the tailnet policy file."*

**Grants** (https://tailscale.com/kb/1324/grants e https://tailscale.com/kb/1458/grants-syntax):
- *"They follow Tailscale's deny-by-default approach"* e *"grants operate on a default-deny basis, so you must explicitly allow any connections you want to permit (unless you keep the default allow all policy)."*
- Estrutura: *"a source (`src`), a destination (`dst`), and at least one type of permissions: network permissions (`ip`) or application permissions (`app`)."* Tags podem ser origem e destino: *"Tags (`tag:database`) for device groups."*
- Limitar a porta: *"`"ip": ["tcp:443", "udp:53"]` grants access to TCP port 443 (HTTPS) and UDP port 53 (DNS) on the destination."* Exemplo oficial da sintaxe: `{ "src": ["group:sales"], "dst": ["tag:internal-tools"], "ip": ["tcp:443", "tcp:22"] }` e `{ "src": ["autogroup:member"], "dst": ["tag:us-east-vpc"], "ip": ["tcp:80", "tcp:443"] }`. Logo, uma regra `src: tag:cliente`, `dst: tag:par`, `ip: ["tcp:8787"]` usa só campos documentados; o texto bruto não traz esse exemplo literal.
- A política padrão (permissiva) é `"grants": [{"src": ["*"], "dst": ["*"], "ip": ["*"]}]` (https://tailscale.com/kb/1337/policy-syntax): se ela continuar na política, a restrição por tag não vale (a página de grants avisa: *"unless you keep the default allow all policy"*).
- Tags usadas em `src`/`dst` precisam existir em `tagOwners` (*"The `tagOwners` section of the tailnet policy file defines the tags assignable to devices and the list of users allowed to assign each tag."*, kb/1337).

### 4. O cliente que só usa o MCP recebe o AGENTS.md?

Fonte: especificação do MCP, versão 2025-11-25 (https://modelcontextprotocol.io/specification/2025-11-25, fonte bruta em https://raw.githubusercontent.com/modelcontextprotocol/modelcontextprotocol/main/docs/specification/2025-11-25/). Existem também as versões `2026-07-28` e `draft` no repositório; só li o `instructions` na 2026-07-28 (mesmo campo, redação mais longa).

**4.1 `instructions` do servidor.** `schema.ts` (2025-11-25), `InitializeResult`: *"Instructions describing how to use the server and its features. This can be used by clients to improve the LLM's understanding of available tools, resources, etc. It can be thought of like a "hint" to the model. For example, this information MAY be added to the system prompt."* (`instructions?: string;`, campo opcional, `MAY`). Na versão 2026-07-28: *"It should focus on information that helps the model use the server effectively and should not duplicate information already in tool descriptions."*

**4.2 O es617 já usa esse canal.** `MCP_INSTRUCTIONS_FILE`: *"Path to a file (e.g. markdown) whose contents are appended to the MCP `instructions`."*; `MCP_INSTRUCTIONS`: *"Best-effort: not all clients respect `instructions`."* Limite: *"files larger than 32 KB are fatal startup errors"* (`MCP_INSTRUCTIONS_MAX_BYTES = 32 * 1024` no código). Aviso do README: *"its contents land in every MCP session's system prompt, so write access to it = prompt-injection access to every client."* No código, o texto final é `${BASE_INSTRUCTIONS}\n\n${MCP_EXTRA_INSTRUCTIONS}`. Ou seja, apontar `MCP_INSTRUCTIONS_FILE` para o AGENTS.md do hub (se couber em 32 KB) é uma entrega de instruções suportada pelo servidor.

**4.3 O que cada cliente faz com `instructions`.**
- Claude Code: *"Only tool names and server instructions load at session start"* (com tool search) e *"Claude Code truncates each tool description and each server's instructions at 2,048 characters by default."* Esse truncamento de 2.048 caracteres é um limite do cliente, bem menor que os 32 KB do servidor.
- Codex: usa o campo; *"Keep the first 512 characters self-contained"* (ver 2). O texto não diz se há truncamento.
- Copilot CLI e VS Code: as páginas lidas não tratam de `instructions`: não verificado.

**4.4 Recursos (resources).** Spec: *"The Model Context Protocol (MCP) provides a standardized way for servers to expose resources to clients. Resources allow servers to share data that provides context to language models, such as files..."*; *"Resources in MCP are designed to be application-driven, with host applications determining how to incorporate context"*; operações `resources/list` e `resources/read`. Claude Code: *"Type `@` in your prompt to see available resources"*, formato `@server:protocol://resource/path`, e *"Claude Code automatically provides tools to list and read MCP resources when servers support them"* (https://code.claude.com/docs/en/mcp.md, "Use MCP resources"). O es617 não registra recursos (ver 1.6); seria preciso acrescentar um no fork.

**4.5 Prompts.** Spec: *"Prompts are designed to be user-controlled, meaning they are exposed from servers to clients with the intention of the user being able to explicitly select them for use."* Claude Code: *"MCP servers can expose prompts that become available as commands in Claude Code."* Um prompt exige ação do usuário; não chega sozinho ao modelo. O es617 também não registra prompts.

**Resumo de 4.** O protocolo oferece três canais: `instructions` (empurrado no `initialize`, pode entrar no prompt de sistema, "hint" opcional), resources (a aplicação decide se e como incluir) e prompts (o usuário escolhe). Só o primeiro chega ao agente sem ação explícita, e o es617 já o expõe por `MCP_INSTRUCTIONS_FILE`.

## Não verificado

- Se o fork do Gustavo mantém as mesmas variáveis (`READ_ONLY`, `MCP_INSTRUCTIONS_FILE`) e ferramentas do upstream `main`; li só o upstream.
- Quando `search_notes` entrou no es617 e por que a pesquisa 26 diz que não há busca de texto (README e `tools.ts` atuais dizem que há).
- Cabeçalho de token no VS Code (`.vscode/mcp.json` / `.mcp.json`): o exemplo da página não traz `headers`; a referência de schema (`/docs/agents/reference/mcp-configuration.md`) não foi lida.
- Se Copilot CLI e VS Code usam o campo `instructions` do servidor.
- Se Codex trunca `instructions` além do primeiro trecho (a doc só recomenda 512 caracteres iniciais autossuficientes).
- Lista exata das variáveis de credencial que o Claude Code lê como vazias em `headers` (seção "Credential variables that read as empty" não transcrita).
- Se uma tag `tag:cliente` pode ser aplicada por chave efêmera de OAuth client em vez de chave gerada por humano (o texto de auth-keys cita OAuth clients, sem detalhe lido).
- O texto do auth-keys diz *"Enable Ephemeral to automatically remove the auth key after the device goes offline"*, redação ambígua (remove a chave ou o nó?); a página de ephemeral-nodes deixa claro que é o nó que é removido. Usei esta última.
- Disponibilidade de Tailscale Services/`svc:` e de grants por plano: não consultado.
- Esta pesquisa não leu o código do CouchDB nem do LiveSync (fora do escopo da porta 7).

## Precisa de teste

- Duas instâncias do es617 sobre o mesmo CouchDB (`PORT` e `DATA_DIR` distintos; uma `READ_ONLY=true`, outra de escrita): se o índice de busca e o feed de mudanças convivem sem conflito.
- Que Claude Code, Codex e Copilot CLI de fato injetam o `instructions` do es617 (com o AGENTS.md até 32 KB) no contexto, e quanto chega depois do truncamento de 2.048 caracteres do Claude Code.
- Que `READ_ONLY=true` realmente esconde as quatro ferramentas de escrita no `tools/list` visto pelo cliente e que o servidor rejeita escrita se o cliente tentar chamar o nome mesmo assim.
- Que um nó efêmero sem `tag:cliente` autorizada por grant não alcança a porta 8787 (e que as demais portas do par ficam fechadas) com a política real do Gustavo.
- Tempo real de remoção do nó efêmero após a sandbox sumir (a doc diz 30 a 60 minutos, sujeito a mudança), e se `tailscale logout` na saída é viável no ambiente da sandbox.
- Token estático Bearer do es617 por cabeçalho, em cada cliente, em instância sem OAuth ativado (o código aceita Bearer estático; o comportamento do cliente ao receber o 401 com `WWW-Authenticate` não foi testado).

## Fontes

Texto bruto lido com `curl -sL` em 2026-10-10.
- es617/obsidian-sync-mcp, README: https://raw.githubusercontent.com/es617/obsidian-sync-mcp/main/README.md
- es617: `src/main.ts`, `src/tools.ts`, `src/vault-readonly.ts`, `src/auth.ts` em https://raw.githubusercontent.com/es617/obsidian-sync-mcp/main/src/ (árvore: https://api.github.com/repos/es617/obsidian-sync-mcp/git/trees/main?recursive=1)
- Claude Code, MCP: https://code.claude.com/docs/en/mcp.md
- Codex, MCP: https://developers.openai.com/codex/mcp.md (redireciona para https://learn.chatgpt.com/docs/extend/mcp.md?surface=cli)
- GitHub Copilot CLI, MCP: https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-mcp-servers (texto via https://docs.github.com/api/article/body?pathname=/en/copilot/how-tos/copilot-cli/customize-copilot/add-mcp-servers)
- VS Code, MCP: https://code.visualstudio.com/docs/agent-customization/mcp-servers e https://raw.githubusercontent.com/microsoft/vscode-docs/main/docs/agent-customization/mcp-servers.md
- Tailscale: https://tailscale.com/kb/1111/ephemeral-nodes ; https://tailscale.com/kb/1085/auth-keys ; https://tailscale.com/kb/1068/acl-tags ; https://tailscale.com/kb/1324/grants ; https://tailscale.com/kb/1458/grants-syntax ; https://tailscale.com/kb/1337/policy-syntax (HTML convertido em texto por script local)
- Especificação MCP: https://modelcontextprotocol.io/specification/2025-11-25 ; fontes brutas em https://raw.githubusercontent.com/modelcontextprotocol/modelcontextprotocol/main/schema/2025-11-25/schema.ts , `.../schema/2026-07-28/schema.ts` e `.../docs/specification/2025-11-25/server/resources.mdx`, `.../server/prompts.mdx`
