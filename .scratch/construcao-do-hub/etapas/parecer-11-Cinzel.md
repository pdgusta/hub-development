# Parecer do ticket 11 (Cinzel): MCP do banco pelos três harnesses

## Rodada 1 — 2026-10-17 ~08h30 (hub ticket-11 ab374b4, com integracao e2b7607; fork ticket-11 = integracao 34c3e50)

Veredito: **sem conserto; aceite final pendente do Codex (rodada 2, depois das 12h15).** Fiel sozinho (Fielzinho sem
cota até 12h15; leitura dele pendente).

### Conferido pelo Fiel

- integracao ancestral; árvore limpa antes e depois. `HUB_MCP_BANCO_DIR=C:/Projetos/hub-mcp-banco-wt/ticket-11 node
  --test agents/code/test/11-mcp-banco.test.mjs`: 4/4.
- Costuras aceitas seguidas: harness fora do hub (a marca só chega pelo servidor), só `estado_do_hub` aprovado, o
  teste afirma A/B/C por harness e não chamar gravação; o resto só registra (`medidas-*.json`).
- Captura (`captura.mjs`): guarda só cabeçalhos de formato (sem `Authorization`, cookie, conta); a resposta não é
  guardada; escuta em 127.0.0.1. Evidência sem token (procurado `ghu_`, `sk-`, `refresh_token`, `access_token`,
  `Bearer`, `eyJ`; o único casamento é "ask-matt", nome de skill). `apagado: true` nas quatro rodadas.
- Medidas da rodada 1: Claude cita A, B, C e a regra (esta depois de um `ToolSearch`); Copilot sem a opção: só C e a
  regra; com `--allow-all-mcp-server-instructions`: tudo. Codex: nenhum pedido chegou à captura (erro do teste,
  consertado em bfd1af3 com `spawn`).

### Pendente (rodada 2)

O Codex: a citação e a captura (os dois critérios do Codex). Rodada curta só com a evidência dele e o diff do teste.

### Ressalvas (não seguram; levar ao maestro)

1. **Copilot sem a opção não põe as instruções do servidor no prompt.** Em produção, a cabeça do `AGENTS.md` só chega
   ao Copilot se o kit (ticket 23) ligar `--allow-all-mcp-server-instructions` ou puser o `hub-banco` na lista
   permitida. Vira requisito do kit.
2. **Claude Code adia as ferramentas MCP:** a regra curta do `write_note` só chega quando o modelo procura a
   ferramenta. A cabeça chega pelas instruções do servidor.
3. Para o 25 (decisão do maestro): regra seguida, banco recriado no meio da sessão, banco cifrado pelos harnesses.
4. A evidência do Copilot traz a lista de skills de `%USERPROFILE%\.agents\skills` da máquina (nomes e descrições):
   não é segredo, mas é ambiente pessoal no repositório (o mesmo vale para evidências anteriores).
