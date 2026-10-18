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

## Rodada 2 (só o Codex, gpt-6-luna) — 2026-10-17 ~15h30 (Fiel + 2ª leitura por subagente Sonnet 5.5)

Ramo `ticket-11`, e63d951 (merge da integracao d298826; evidência e96cd70). **Veredito: VOLTA** por 1 conserto
mecânico, em acordo com a 2ª leitura (`parecer-11-Cinzel-segunda-leitura.md`).

O que confere:
- Critérios do Codex: A, B e C citadas (`medidas-codex.json`, `saida.jsonl`); captura de 5 pedidos em `codex/lido.json`
  bate com o relatório (1º `/responses` sem marcas; A, B e a regra só em `input[9].output[1].text`, a listagem de
  ferramentas; C em `input[11]`). Modelo `gpt-6-luna`.
- Login: `auth.json` copiado 17:47:36Z e apagado 17:47:47Z; hashes reais iguais (só `~/.claude.json`, de registro).
  Evidência sem segredo (varredura por `ghu_`, `sk-`, `refresh_token`, `access_token`, `Bearer`, `eyJ`).
- `11-mcp-banco.test.mjs` + ponta a ponta, com `HUB_MCP_BANCO_DIR` do fork: 4 passam, 1 pulado. `git status` limpo.

Conserto:
1. (Fiel e 2ª leitura) `agents/code/test/ponta-a-ponta/11-mcp-banco.test.mjs:141` escreve `'gpt-6-luna'` à mão (e7e1dd3).
   Com o 43 já na integracao, `node --test agents/code/test/harness-real.test.mjs` dá 7/8: "nenhum teste escreve o
   modelo do Codex à mão" acusa esse arquivo; a suíte da junção fica vermelha. Trocar por `MODELO_CODEX` de
   `../harness-real.mjs`, como os outros ponta a ponta. A evidência não precisa ser refeita.

Ressalva: a captura mostra as instruções só em volta da `delete_note` (o relatório já diz).

## Rodada 3 (conserto 28782df) — 2026-10-17 ~15h45 (Fiel + 2ª leitura Sonnet 5.5)

Diff e63d951..28782df: só `ponta-a-ponta/11-mcp-banco.test.mjs`, importa `MODELO_CODEX` e o usa no `-m`. Conserto 1
feito. Fiel: `harness-real.test.mjs` 8/8; 2ª leitura: 8/8 e 11-mcp-banco + aceite 4 passam, 1 pulado.
**Veredito: PASSA em acordo**, com a ressalva da r2 (instruções vistas só em volta da `delete_note`) e as ressalvas da
r1 para o 23 e o 25.

Nota para o 24 (65cb752): o aceite já usa `MODELO_CODEX`, mas o ramo ainda não tem o 43 (17-vigia-tela, 22-cliente e
22-kit-cliente com o modelo à mão); juntar a integracao antes do Rebite e rodar o `harness-real.test.mjs`.
