# Copilot Enterprise e os MCP do hub (2026-10-24, maestro do B)

Pergunta do Gustavo (Maestri Chat, thread azul): a conta do Copilot passou a ser a do GitHub Enterprise com SSO
(`gustavo-delfino_armis`, Copilot Enterprise), com políticas novas; no A parece estar travando os MCP de terceiros.
Como checar o impacto no uso do hub?

## Fonte primária (docs.github.com, lida pelo `api/article/body`; cópias no scratchpad da sessão, `docs-copilot/`)

- `/en/copilot/concepts/enterprise/mcp-management`: a política **"MCP servers in Copilot"** decide se qualquer MCP
  roda nos clientes do Copilot. A restrição fina é uma allowlist no `managed-settings.json` da empresa.
- `/en/copilot/how-tos/administer-copilot/manage-mcp-usage/configure-enterprise-allowlist`, ordem de avaliação: (1)
  os servidores embutidos (o MCP do GitHub) sempre passam; (2) bloqueia o que casa com `deniedMcpServers`; (3) com
  `allowedMcpServers` presente, bloqueia o que não casa; (4) bloqueia servidor com variável não resolvida
  (`${VAR}`, `$VAR`) no URL ou no comando. JSON malformado conta como allowlist vazia (bloqueia tudo menos os
  embutidos). Sem conseguir baixar a política, o cliente fica com a anterior (só pode ficar mais restritivo).
- `/en/copilot/reference/enterprise-administrators/enterprise-managed-settings`: `allowedMcpServers` e
  `deniedMcpServers` valem no Copilot CLI. Casamento por `serverName` (o nome que o usuário deu: `hub-busca`,
  `hub-banco`), `serverUrl` (servidor remoto, HTTP ou SSE; aceita `*`) ou `serverCommand` (stdio). Existe também uma
  chave que suprime no CLI `--allow-all-tools`, `--yolo` e afins (linha ~273 da página).
- `/en/copilot/how-tos/administer-copilot/manage-for-enterprise/use-managed-settings/get-started` e
  `.../deploy-managed-settings`: três jeitos de entregar a política. **Servidor** (repositório `.github-private` da
  empresa, `copilot/managed-settings.json`; vale para quem recebe a licença da empresa; o GitHub recomenda deixar
  visível para os membros; chega em até 1 h, ou na hora ao reiniciar ou logar de novo). **MDM** no Windows, valores
  `REG_SZ` em `HKEY_LOCAL_MACHINE\SOFTWARE\Policies\GitHubCopilot`. **Arquivo** em
  `%ProgramFiles%\GitHubCopilot\managed-settings.json`. MDM e arquivo valem para todos os usuários da máquina,
  seja qual for a licença.

## O que isso quer dizer para o hub

- Só o **Copilot** é afetado. O Claude Code e o Codex não leem essas políticas.
- O kit registra no Copilot `hub-busca` (`http://127.0.0.1:3939/mcp`) e `hub-banco` (`http://127.0.0.1:8796/mcp`,
  header `Authorization` com o token escrito por extenso, sem `${...}`; conferido no B). A regra (4) não pega o
  Copilot. Pegaria uma config com `${VAR}`.
- Sem os dois MCP, o Copilot do A continua lendo o contrato (AGENTS.md), as skills e os hooks, que são arquivos
  locais. Perde a busca e o banco pelo MCP.
- **No B nada muda hoje:** o Copilot daqui está logado só como `pdgusta` (conta pessoal), não há política local
  (sem a chave de registro, sem o arquivo em Program Files) e o teste do 26 passou às ~13h55.

## Como checar no A (só leitura; ninguém rodou ainda)

1. Política local da máquina: `reg query HKLM\SOFTWARE\Policies\GitHubCopilot` e
   `Get-Content "$env:ProgramFiles\GitHubCopilot\managed-settings.json"`.
2. Política do servidor: o `copilot/managed-settings.json` do `.github-private` da empresa, se estiver visível para
   membros (`gh api` com a conta da empresa; o nome da organização dona não é conhecido aqui).
3. Efeito real: o mesmo teste do 26 no A (`copilot -p ... --allow-all-tools`), olhando se `hub-busca` e `hub-banco`
   são chamados ou recusados e se o `--allow-all-tools` é aceito. Dentro do Copilot, `/mcp` mostra os servidores (a
   forma exata da tela não foi verificada).

## Saídas, se estiver bloqueado (para decidir depois de checar)

- Pedir ao administrador para pôr na allowlist `serverName` `hub-busca` e `hub-banco`, ou os URLs
  `http://127.0.0.1:3939/*` e `http://127.0.0.1:8796/*`. Não verificado: se `serverUrl` casa com `127.0.0.1`. A doc só
  diz que o URL de servidor local não conta, e os nossos são do tipo HTTP.
- Copilot no A pela conta pessoal: não escapa da política MDM ou de arquivo, se houver; e depende da regra da
  empresa.
- Caminho sem MCP para o Copilot: skill que chama um script (busca e banco por HTTP, pelo shell). Pode esbarrar na
  política de sandbox ou de permissões, se a empresa ligar.
