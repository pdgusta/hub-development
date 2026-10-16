# Porta 6: Claude fora de um harness de terminal

Pesquisa em fonte primária para o ticket 36 (portas de entrada do hub). Coleta em 2026-10-10. Textos lidos brutos com `curl -sL` (support.claude.com vem em HTML e foi reduzido a texto; claude.com/docs, code.claude.com e platform.claude.com vêm em Markdown). Nenhum teste foi rodado.

## Pergunta

O Gustavo diz usar "o claude (com work)". O hub é uma pasta de Markdown no disco, cada máquina com um servidor MCP por HTTP com token, alcançável só pela tailnet (sem Funnel). Cada superfície do Claude fora do terminal consegue ser porta de entrada?

1. Claude Desktop e Cowork leem e gravam uma pasta local? Como se escolhe a pasta? Leem AGENTS.md ou CLAUDE.md?
2. Conector remoto (custom connector) versus servidor MCP local no Desktop: de onde parte a conexão, um MCP só da tailnet é alcançável, que autenticação é aceita?
3. Projetos do claude.ai e memória: porta para o hub ou cópias?
4. O celular alcança conectores remotos e MCP local?

## Respostas

### 1. Claude Desktop e Cowork: pasta local

**Cowork lê e grava pastas locais, pelo app Desktop aberto.**

- "Local file access. Claude reads and writes files in folders you've connected on your computer. A session in the cloud reaches these files only while the desktop app is open, only for folders you've connected, and with the permissions you've already set." (https://support.claude.com/en/articles/15520349-use-claude-cowork-on-web-desktop-and-mobile)
- "Claude can only read and write files in folders you've connected" (https://support.claude.com/en/articles/13345190-get-started-with-claude-cowork)
- Windows é suportado: "Claude Desktop for Windows — Available on all paid plans. Cowork requires the latest version of Claude for Windows." (mesmo artigo 13345190)

**Como se escolhe a pasta.** Em projetos do Cowork: "Use an existing folder on your computer: If you select 'Use an existing folder,' you'll be prompted to pick a file to use as context for the new Cowork project... After selecting a folder, you can name the new Cowork project, choose where to save it on your computer, add instructions, and attach any additional files." Também: "Projects you create from an existing folder on your computer stay on that computer and aren't saved to your Claude account." (https://support.claude.com/en/articles/14116274-organize-your-tasks-with-projects-in-claude-cowork). As pastas liberadas ficam listadas: "Folders you gave Cowork access to are listed under Trusted folders." (https://support.claude.com/en/articles/16761823-claude-cowork-and-chat-are-one-claude)

**Importante: onde a sessão roda mudou em 6 de outubro de 2026 (Pro e Max).** "On October 6, 2026, new Cowork tasks on Pro and Max plans run in the cloud. The Only on your computer option in Settings > General was removed." Sobre as pastas: "Your folders stay on your computer. Claude reaches only the folders you've connected, through the desktop app, and only while it's open. When a task needs a file in the cloud, Claude fetches a copy of just that file." (https://support.claude.com/en/articles/15520349-use-claude-cowork-on-web-desktop-and-mobile). Ou seja, em Pro/Max o agente roda nos servidores da Anthropic e lê a pasta por uma ponte via app Desktop; os arquivos que ele abre são processados lá: "the work Claude does there, including any local files it opens through the desktop app, is processed on Anthropic's servers rather than staying on your computer." (https://support.claude.com/en/articles/13364135-use-claude-cowork-safely). Para tarefas só locais, a fonte indica o Claude Code no app Desktop: "For new tasks that run only on your computer, use Claude Code in the desktop app." (mesmo artigo 15520349). Em Team/Enterprise a fonte diz que sessões locais existem para implantações atuais e que a nuvem está em beta ("Cowork sessions run in the cloud by default... Local execution remains available for existing desktop deployments", https://support.claude.com/en/articles/14479288-claude-cowork-architecture-overview).

**Leem AGENTS.md ou CLAUDE.md da pasta?** No Cowork, a fonte não diz. O que ela descreve são "Folder instructions": "Folder instructions add project-specific context to Cowork when you select a local folder on desktop. Claude can also update these on its own during a session." (https://support.claude.com/en/articles/13345190-get-started-with-claude-cowork). Não há menção a CLAUDE.md nem a AGENTS.md nesse artigo nem nos de projetos e arquitetura do Cowork. Sobre a aba Code do Desktop (que é Claude Code com interface gráfica): "Desktop and CLI read the same configuration files, so your setup carries over: CLAUDE.md and CLAUDE.local.md files in your project are used by both" (https://code.claude.com/docs/en/desktop.md, seção Shared configuration). AGENTS.md não aparece nessa página.

**Aba Chat do Desktop com pasta?** O artigo de transição diz: "Files and folders: In Claude Desktop, give Claude access to a folder on your computer so it can read, organize, and create files there." (https://support.claude.com/en/articles/16761823-claude-cowork-and-chat-are-one-claude). Sem mais detalhe sobre leitura de arquivos de instrução.

### 2. Conector remoto versus MCP local no Desktop

**De onde parte a conexão de um conector remoto: dos servidores da Anthropic, em todos os clientes.**

> "When you add a custom connector, Claude connects to your remote MCP server from Anthropic's cloud infrastructure, rather than from your local device. This is true across every Claude client, including claude.ai, Claude Desktop, Cowork, and the mobile apps."

> "This means your MCP server must be reachable over the public internet from Anthropic's IP ranges. Servers hosted on a private corporate network, behind a VPN, or blocked by a firewall won't connect, even if you can reach them from your own machine."

> "Even though Cowork and Claude Desktop run on your computer, remote connectors are configured and brokered through your Claude account. The connection to your MCP server originates from Anthropic's servers, not from your machine's network interface."

Fonte: https://support.claude.com/en/articles/11175166-get-started-with-custom-connectors-using-remote-mcp

Reforço de arquitetura: "Connector authorization tokens never enter the sandbox; connector calls are made on the server side." e o sandbox "can't reach private, internal, link-local, or cloud-metadata addresses" (https://support.claude.com/en/articles/14479288-claude-cowork-architecture-overview).

**Consequência para a tailnet.** Pelas citações acima, um MCP que só existe na tailnet (sem Funnel, sem IP público) não é alcançável por conector remoto: quem conecta são os servidores da Anthropic, que não estão na tailnet. A fonte não menciona Tailscale; a conclusão decorre de "behind a VPN... won't connect". Para servidor em rede privada a fonte oferece duas saídas: (a) liberar o IP de saída da Anthropic no firewall, o que exige o servidor ser alcançável da internet pública ("you'll need to allowlist Anthropic's IP addresses in your firewall so inbound connections from Claude can reach your server"; faixa de saída `160.79.104.0/21`, https://platform.claude.com/docs/en/api/ip-addresses.md); (b) MCP tunnels, descrito abaixo.

**MCP tunnels (única rota oficial para rede privada).** "MCP tunnels connect Claude to MCP servers that run inside your private network. You run a small tunnel stack on a host in your network, the stack opens an outbound-only connection to Anthropic... Your firewall needs no inbound rules and your MCP servers need no public endpoint." Restrições: "MCP tunnels are in research preview and are available to organizations on the Claude Enterprise plan by request." Requer "A claude.ai organization on the Enterprise plan with MCP tunnels enabled", papel Owner/Primary Owner, um host com Kubernetes ou Docker Compose, e servidores MCP com transporte Streamable HTTP. Depende da Cloudflare (cloudflared). "The tunnel carries traffic to your MCP servers but does not authenticate to them. Configure each MCP server to require OAuth" (https://claude.com/docs/connectors/mcp-tunnels/overview.md). A fonte não diz se existe para Pro/Max/Team; diz Enterprise sob pedido.

**Servidor MCP local no Desktop (extensão desktop / MCPB).** "Desktop extensions run locally and are only available in Claude Desktop and Claude Code—not on web or mobile." (https://support.claude.com/en/articles/11725091-when-to-use-desktop-and-web-connectors). "A desktop extension is a local MCP server packaged with MCPB (MCP Bundles) that runs on your device inside Claude Desktop." (https://claude.com/docs/connectors/custom/add-unlisted.md). Instalação: Settings > Extensions, arrastar o arquivo `.mcpb` (mesma página). Servidores configurados em `claude_desktop_config.json` são outro mecanismo e usam a rede local: "Local MCP servers configured in Claude Desktop via claude_desktop_config.json are a separate mechanism and do use your local network, but those aren't available in Cowork or claude.ai." (artigo 11175166). Como a conexão parte da máquina, um alvo na tailnet seria alcançável pela rede da própria máquina. A fonte não afirma isso expressamente para tailnet nem diz se esse mecanismo aceita uma URL HTTP direta (ver Não verificado). Extensões suportam "Node.js, Python, and binary MCP servers" e valores marcados `"sensitive": true` são guardados no cofre do sistema (Credential Manager no Windows) (https://support.claude.com/en/articles/10949351-getting-started-with-local-mcp-servers-on-claude-desktop).

**Cowork e MCP local.** "Local MCP servers don't run in sessions in the cloud." (artigo 14479288). Plugins com MCP local: "works in Cowork and Claude Code, not in chat" (artigo 11725091). O artigo de superfícies diz: "Local connectors and plugins that include local MCP servers work through the desktop app only." (artigo 15520349).

**Autenticação aceita por conector remoto** (https://claude.com/docs/connectors/building/authentication.md e https://claude.com/docs/connectors/custom/add-unlisted.md):

- OAuth: "Sign in now", "Sign in when needed"; identidade do cliente via "Claude's published identity" (Client ID Metadata Document), registro automático (DCR) ou cliente OAuth próprio. Callback fixo `https://claude.ai/api/mcp/auth_callback`.
- Token em cabeçalho existe, mas em beta restrito: "Request header authentication is in beta and available to a limited set of organizations. If you don't see the Request headers section in the Add custom connector dialog, your organization doesn't have access yet." Detalhes: "Claude sends the value exactly as you enter it. It doesn't add an authentication scheme" (para Bearer, digitar `Bearer seu-token`); "You can add up to four headers"; nomes de cabeçalho precisam de aprovação da Anthropic, com `authorization`, `x-api-key` e `x-auth-token` válidos para todos; "On an OAuth connection you can't configure Authorization as a request header." Sem OAuth, escolher "No sign-in" e pôr a chave em Request headers. Em Team/Enterprise todos que usam o conector compartilham a credencial.
- Sem autenticação: "none... Supported by default".
- Após criar, "You can't change authentication settings after you add a connector"; é preciso remover e recriar.
- URL deve ser HTTPS: "enter the HTTPS address where the server accepts MCP requests, for example https://mcp.example.com/mcp". Transporte SSE só com URL terminando em `/sse`.
- Quem adiciona: Pro/Max adicionam em Customize > Connectors; Team só Owners; Enterprise Owners ou papel com "Manage access to Libraries"; Free limita a um conector custom.

### 3. Projetos do claude.ai e memória: porta ou cópia?

**Projetos (chat) são cópias.** "You can upload relevant documents, text, code, or other files to a project's knowledge base" e "define project instructions" (https://support.claude.com/en/articles/9517075-what-are-projects). O conteúdo é enviado para a conta, não é um espelho de pasta local. Em Cowork, importar um projeto de chat faz cópia: "Clicking 'Create' will transfer the files and instructions from your existing Claude project and create a new Cowork project." Há também a nota: "Cowork won't change a project's contents, so add anything you want to keep to the project yourself." (artigos 14116274 e 15520349). Projetos criados a partir de pasta local ficam no computador. Com muito conteúdo, a base usa RAG ("expand capacity by up to 10x", planos pagos; artigo 9517075).

**Memória não serve de porta.** É resumo gerado pelo Claude a partir das conversas: "Claude can also remember context from your chats and carry it into new conversations and Cowork tasks." Cada projeto tem memória e resumo separados ("Each project has its own separate memory space and dedicated project summary"); a memória é compartilhada entre chat e Cowork só quando o Cowork roda na nuvem ("Memory across Cowork and chat only works when Cowork runs in the cloud"). Há exportar/importar memória, marcado "experimental" (https://support.claude.com/en/articles/11817273-use-claude-s-chat-search-and-memory-to-build-on-previous-context). Nada nessas páginas descreve leitura ou gravação de uma pasta de arquivos pela memória.

Leitura: projeto com arquivos e memória são armazenamentos próprios do Claude, copiados do hub; não leem a pasta viva. A porta de verdade para o hub vivo seria um conector (remoto, ver 2) ou a pasta conectada ao Cowork/Desktop (ver 1).

### 4. Celular

- "Claude mobile app: remote connectors" (https://claude.com/docs/connectors/getting-started.md, seção sobre onde os conectores funcionam); "Claude mobile app" faz conexões remotas a partir da nuvem da Anthropic (artigo 11175166: "This is true across every Claude client, including claude.ai, Claude Desktop, Cowork, and the mobile apps").
- MCP local não: "Desktop extensions run locally and are only available in Claude Desktop and Claude Code—not on web or mobile." (artigo 11725091).
- Pasta local pelo celular: o Cowork no celular alcança arquivos locais só via Desktop ligado: "Local file access, local connectors, browser use, and computer use from web and mobile work through the Claude Desktop app. A cloud session can read and write files in folders you've connected on your computer only while the desktop app is open on that computer and the session was started on desktop or is a scheduled task. If the app is closed, the session keeps running but can't reach your local files." (artigo 15520349). Na tabela da mesma página, "Local file access" aparece com asterisco em Web e Mobile.
- Conector remoto adicionado na conta aparece no celular ("A connected connector is available in your conversations on the web, desktop, and mobile", artigo claude.com/docs/connectors/getting-started.md).

Consequência: no celular, um MCP só da tailnet não é alcançável via conector (mesma regra dos servidores da Anthropic) e MCP local não existe. A fonte não menciona se o app Tailscale no celular muda isso; pela regra citada, a conexão não parte do aparelho.

## Não verificado

- Se o Cowork (pasta conectada) lê CLAUDE.md ou AGENTS.md da pasta: as páginas lidas só falam de "Folder instructions" e "Instructions" do projeto, sem citar esses arquivos. A aba Code do Desktop lê CLAUDE.md (citado), mas AGENTS.md não foi encontrado em code.claude.com/docs/en/desktop.md.
- Se a aba Chat do Desktop com pasta liberada lê arquivos de instrução da pasta.
- Se `claude_desktop_config.json` aceita hoje uma entrada com URL HTTP remota, ou só comandos stdio. A página do MCP sobre servidores locais (https://modelcontextprotocol.io/docs/develop/connect-local-servers.md) trata de comandos e logs "stdio"; não afirma o contrário nem a favor de HTTP. Não li a seção de schema completa.
- Se a extensão MCPB (ou um stdio que faça proxy) pode falar com um servidor na tailnet. A fonte só diz que roda "on your device" com "your user permissions".
- Se o tráfego de uma sessão Cowork em nuvem que lê pasta pelo Desktop usa a rede da máquina para algo além dos arquivos (a fonte descreve só "Anthropic-brokered connection").
- Disponibilidade de MCP tunnels fora do Enterprise (a fonte diz só Enterprise, por pedido, research preview). O plano do Gustavo (Pro, Max, Team ou Enterprise) não foi informado.
- Se o plano dele tem "Request headers" (beta, "limited set of organizations").
- Nada da documentação do Tailscale foi consultado (o enunciado pedia só quando preciso); a conclusão de inalcançabilidade vem da regra da Anthropic.
- Limites de tamanho/timeouts do conector custom (existe tabela em https://claude.com/docs/connectors/building/index.md; não transcrita aqui).

## Precisa de teste

- Cowork com a pasta do hub (ex.: C:\context-hub) conectada: o agente aplica AGENTS.md/CLAUDE.md da raiz?
- Desktop (Chat) com MCP local por `claude_desktop_config.json` ou `.mcpb` apontando para `http://<maquina>.<tailnet>.ts.net:porta` com token: conecta e lista as ferramentas?
- Aba Code do Desktop (sessão local, `.mcp.json` com URL da tailnet): conecta? A página diz que MCP de `.mcp.json` funciona nas duas interfaces, mas a rede de origem de cada sessão (local, SSH, nuvem) não foi testada.
- Conector custom com URL de tailnet (MagicDNS ou 100.x): esperado falhar pela regra citada; só um teste confirma a mensagem e o comportamento.
- Pro/Max: comportamento real da leitura de pasta com a sessão na nuvem e o app Desktop fechado ou aberto.

## Fontes

- https://support.claude.com/en/articles/11175166-get-started-with-custom-connectors-using-remote-mcp
- https://support.claude.com/en/articles/11725091-when-to-use-desktop-and-web-connectors
- https://support.claude.com/en/articles/10949351-getting-started-with-local-mcp-servers-on-claude-desktop
- https://support.claude.com/en/articles/13345190-get-started-with-claude-cowork
- https://support.claude.com/en/articles/15520349-use-claude-cowork-on-web-desktop-and-mobile
- https://support.claude.com/en/articles/14479288-claude-cowork-architecture-overview
- https://support.claude.com/en/articles/13364135-use-claude-cowork-safely
- https://support.claude.com/en/articles/14116274-organize-your-tasks-with-projects-in-claude-cowork
- https://support.claude.com/en/articles/16761823-claude-cowork-and-chat-are-one-claude
- https://support.claude.com/en/articles/9517075-what-are-projects
- https://support.claude.com/en/articles/11817273-use-claude-s-chat-search-and-memory-to-build-on-previous-context
- https://claude.com/docs/connectors/custom/add-unlisted.md
- https://claude.com/docs/connectors/building/authentication.md
- https://claude.com/docs/connectors/getting-started.md
- https://claude.com/docs/connectors/mcp-tunnels/overview.md
- https://claude.com/docs/connectors/building/testing.md (um servidor local precisa de URL pública via túnel para o Claude alcançá-lo)
- https://platform.claude.com/docs/en/api/ip-addresses.md
- https://code.claude.com/docs/en/desktop.md
- https://modelcontextprotocol.io/docs/develop/connect-local-servers.md
