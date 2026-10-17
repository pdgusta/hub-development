# Relatório do ticket 23 (Cinzel): kit de par, a forma

Ramo `ticket-23` (hub), worktree `C:/context-hub-wt/ticket-23`, de `integracao` e2b7607. Costuras e respostas:
`costuras-23-Cinzel.md`.

## Fatos de fonte (lidos por curl em 2026-10-17)

- Claude Code, <https://code.claude.com/docs/en/mcp.md>, "Environment variable expansion in `.mcp.json`": `${VAR}` e
  `${VAR:-default}` valem em `command`, `args`, `env`, `url` e `headers`; exemplo `"Authorization": "Bearer
  ${API_KEY}"`. A seção cobre também o escopo do usuário (`~/.claude.json`): "For a server in the local, project, or
  user scope ... show a `${VAR}` reference by name". Variáveis de credencial do próprio Claude (`ANTHROPIC_*`,
  `NPM_TOKEN`, `HTTPS_PROXY`...) chegam vazias; `HUB_MCP_BANCO_TOKEN` não é uma delas.
- Copilot CLI, referência de comandos
  (`docs.github.com/api/article/body?pathname=/en/copilot/reference/copilot-cli-reference/cli-command-reference`):
  no `mcp-config.json`, `headers` "Supports variable expansion"; `env` "Supports `$VAR`, `${VAR}`, and
  `${VAR:-default}` expansion". `--allow-all-mcp-server-instructions`: "By default, only allowlisted server
  instructions are included up front; other servers' instructions are retrieved on demand."
- Copilot CLI, referência da pasta de configuração (`.../cli-config-dir-reference`): nenhuma chave de configuração nem
  variável de ambiente liga as instruções de todos os servidores; a lista permitida não é do usuário. **Logo, o kit não
  tem como ligar a opção por arquivo**: quem abre o Copilot passa `--allow-all-mcp-server-instructions` (o preset
  `custom` do Maestri, user story 40 da faixa 8; ticket 24/26).

## Sondas

- 2026-10-17 ~08h40, app-server do Codex (`hooks/list`, sem modelo, sem login), mesmo `hooks.json` em duas pastas:
  `currentHash` igual (`sha256:08eb88...`) nas duas; a chave é `<caminho do hooks.json>:<evento>:<grupo>:<hook>`. O
  app-server grava no `CODEX_HOME` (`*.sqlite`, `installation_id`, `skills/`, `tmp/`, `.tmp/`). **Por isso o kit lista
  os hooks numa cópia temporária do `hooks.json` e do `config.toml` e troca o caminho da chave pelo real**: a casa não
  ganha arquivo do app-server, e a segunda passada e o desfazer ficam limpos.
