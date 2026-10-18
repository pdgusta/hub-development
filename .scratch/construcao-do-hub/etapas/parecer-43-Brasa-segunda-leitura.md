# Parecer 43 (2a leitura, Brasa): modelo do Codex nos testes

Ramo ticket-43 @ 32e8217, base integracao d298826. Veredito: **PASSA** (sem consertos; 3 ressalvas).

## Critérios do ticket
1. `MODELO_CODEX` de `HUB_MODELO_CODEX`, senão `gpt-6-luna`: ok (harness-real.mjs:9; `||` trata variável vazia como ausente, bom). Teste novo cobre os dois casos por processo filho.
2. Nenhum teste com o modelo à mão: ok. Todo `codex exec` em agents/code/test (12-busca, 14, 15, 17, 19, 20, 22, 27 e provas/03-codex-hooks/prova.test.mjs) usa `-m MODELO_CODEX`. Nenhum .ps1 chama o Codex. `casos-da-bancada.json` tem `"model": "gpt-6-luna"` mas é dado da bancada do 11, lido só pelo 14-guardas.test.mjs (leve), nunca vira argumento do Codex.
3. Testes leves: `node --test harness-real.test.mjs 22-kit-cliente.test.mjs` = 12 passam, 0 falham (rodei).

## Ressalvas (não seguram)
1. O detector `/\bgpt-\d/` olha só `.mjs` (fora `evidencia*`). Deixa passar: modelo sem `gpt-` (ex. `o3`, `codex-mini`), `.ps1`/`.json`/`.py`, e o `-m` montado por concatenação. Hoje nada disso existe. Um guarda mais forte seria exigir `MODELO_CODEX` em todo `.mjs` com `codex exec`.
2. Pode falhar à toa se um comentário ou fixture de teste futuro citar `gpt-N` (ex. o config.toml de ensaio). O ticket já trocou `gpt-6-luna` por `o-do-usuario` no 22-kit-cliente por isso. Quem esbarrar sabe o motivo pela mensagem do deepEqual (lista os arquivos).
3. O 22-cliente ganhou `-c model_reasoning_effort="low"` além da troca do modelo (como os outros). Mudança de comportamento pequena, não pedida no ticket; vale um aviso no relatório.

## Junção
`git merge-tree ticket-43 integracao` limpo (sem conflito). Os 5 arquivos mudados não colidem com o que a integracao trouxe. Docs de skills (bateria-de-testes.md, construcao-em-etapas.md) ainda citam gpt-6-luna/astra para recrutas, fora do escopo.
