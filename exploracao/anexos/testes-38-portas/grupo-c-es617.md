# Testes 38, grupo C: MCP do es617 (2026-10-10)

Ticket: "Testes das portas de entrada". Ambiente: o spike do LiveSync (`C:\Projetos\spike-livesync`),
com a instância de escrita do spike (porta 8787) e uma segunda instância de teste, só de leitura
(porta 8788, `READ_ONLY=true`, token de teste próprio, `MCP_INSTRUCTIONS_FILE` com um `AGENTS.md` de
teste de 5.000 caracteres e marcadores nas posições 100, 500, 1.000, 2.000, 2.100, 3.000 e 4.500),
as duas sobre o mesmo CouchDB. Imagem `ghcr.io/es617/obsidian-sync-mcp:latest`.

## Resultados

| Teste | Resultado |
|---|---|
| Ferramentas da instância só de leitura | `read_note`, `list_notes`, `search_notes`, `list_folders`, `list_tags`, `get_note_metadata`; somem `write_note`, `edit_note`, `delete_note`, `move_note` |
| Chamar `write_note` direto na instância só de leitura | recusado: `MCP error -32601: Unknown tool: write_note`; a nota não foi criada |
| Duas instâncias no mesmo CouchDB | a de escrita gravou uma nota e a de leitura leu e achou pela busca segundos depois; nenhum erro |
| `search_notes` | **não existe na imagem de 2026-10-04** (a do spike); **existe na de 2026-10-09** (argumento `terms`, lista de substrings; devolve caminhos com uma linha de contexto, nunca o corpo) |
| `instructions` no `initialize` | o servidor entrega 5.329 caracteres: um prefácio próprio (329) mais o arquivo inteiro |
| Claude Code (2.1.296) recebe o `instructions` | **sim**, mas cortado com "[truncated]": viu até o marcador da posição 3.329 e não o da 4.829. O corte fica entre esses dois pontos, não em 2.048 como a doc dizia |
| Codex (0.161.0) recebe o `instructions` | **não**: conectou e listou as ferramentas, mas duas perguntas diretas deram "NONE" e "NOT PRESENT" (uma terceira, de sim ou não, disse "yes" sem conseguir citar nada) |
| Copilot CLI (1.0.94) recebe o `instructions` | **não**: conectou e listou as ferramentas, sem nenhum marcador |
| Codex chamando ferramenta MCP em `codex exec` | bloqueado pela política de aprovação padrão ("approval policy is never") |

Limpeza: a nota de teste foi apagada pela instância de escrita, a instância e o volume de teste foram
removidos, e o spike foi parado (estava parado antes). A imagem `:latest` do spike passou a ser a de
2026-10-09.

## O que isso decide

- **`READ_ONLY` funciona no servidor:** a ferramenta de escrita some e a chamada direta é recusada.
- **Duas instâncias por par funcionam** sobre o mesmo CouchDB.
- **A busca existe no es617**, só na imagem nova; a pesquisa 26 estava certa para a imagem velha.
- **O `AGENTS.md` pelo `instructions` do MCP só chega ao Claude Code**, e cortado depois de uns 3.300
  caracteres. Para Codex e Copilot, um cliente só pelo MCP não recebe o contrato por esse canal.
