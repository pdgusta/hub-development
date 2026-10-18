# Parecer (2ª leitura, rodada 2 do Codex): ticket 11, Cinzel

Worktree `C:/context-hub-wt/ticket-11`, ponta e63d951. Veredito: **VOLTA** (1 conserto, pequeno e mecânico). A evidência em si está boa.

## Conferido e certo
1. Evidência do Codex bate com o relatório: `codex/lido.json` e `medidas-codex.json` têm A (hub-a-42d88f), B (hub-b-a55729) e C (hub-c-5caf0d) citadas (`citou` comeco/fim/estado true; regra false, dito no relatório); `chamadas: [estado_do_hub]`; `saida.jsonl` tem o agent_message com as três marcas. Captura: 5 pedidos (2 `/models`, 3 `/responses`); 1º `/responses` sem A/B; A, B e regra só em `input[9].output[1].text` (listagem, `mcp__hub_banco__delete_note`, instruções à frente da descrição); C em `input[11].output[1].text`. Campos sem `instructions` nem `tools`. Tudo como afirmado.
2. Login: `.codex/auth.json` copiado 17:47:36Z, apagado 17:47:47Z (`apagado: true`); hashes antes/depois iguais em todos, menos `.claude.json` (registro, já ressalvado). Nenhum token/segredo na evidência (grep por eyJ, sk-, bearer, tokens: vazio). Nenhuma pasta `hub-ensaio-11-*` sobrando em %TEMP%.
3. Modelo gpt-6-luna e esforço baixo, conforme "Codex só para testes".
4. `11-mcp-banco.test.mjs` (os dois): 4 passam, 1 pulado, como o relatório.

## Conserto
1. **`node --test agents/code/test/harness-real.test.mjs` falha (7/8).** Teste "nenhum teste escreve o modelo do Codex à mão" (`harness-real.test.mjs:144`, vindo da integracao/ticket 43) acusa `ponta-a-ponta/11-mcp-banco.test.mjs`: o commit e7e1dd3 escreveu `'gpt-6-luna'` à mão em `agents/code/test/ponta-a-ponta/11-mcp-banco.test.mjs:141`. Conserto: importar `MODELO_CODEX` de `../harness-real.mjs` (linha 23, como o 12 faz em `12-*.mjs:19`) e usar `'-m', MODELO_CODEX` na linha 141. Reprodução: o comando acima na worktree. Ao juntar na integracao esse teste do 43 quebra a suíte. A evidência não precisa ser refeita (mesmo modelo, mesmo valor).

## Ressalvas (não seguram)
- Não conferido se as 12 ferramentas trazem as instruções (o relatório já diz); só `delete_note` está na captura.
- `duration_ms` do log (431 s) é bem maior que o teste (35 s): é o carregamento do arquivo, não o harness; sem efeito.
- `.claude.json` mudou nos hashes: regravado por sessões abertas, igual às rodadas 1.

## Conserto 28782df

Veredito: PASSA.

- `git diff e63d951 28782df`: 1 arquivo, 2 linhas, só `agents/code/test/ponta-a-ponta/11-mcp-banco.test.mjs`. Importa `MODELO_CODEX` de `../harness-real.mjs` e troca o `'gpt-6-luna'` à mão por ele. Nada mais mudou.
- `harness-real.test.mjs`: 8 passam, 0 falham (inclui "nenhum teste escreve o modelo do Codex à mão").
- `11-mcp-banco.test.mjs` + ponta-a-ponta (HUB_MCP_BANCO_DIR=C:/Projetos/hub-mcp-banco-wt/ticket-11): 4 passam, 0 falham, 1 pulado (o de harness de verdade, sem HUB_HARNESS_REAL=1, como previsto).
