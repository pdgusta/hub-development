# Parecer 22 (Brasa): segunda leitura

## Rodada curta: evidência do Codex (2026-10-17)

Leitor: 2ª leitura independente do Fiel. Não li o `parecer-22-Brasa.md`.
Ramo `ticket-22`, ponta 22811cb, sobre `integracao` f640bbd. Worktree `C:/context-hub-wt/ticket-22`.

**Veredito: PASSA.** Nenhum conserto.

### O que conferi

1. **Modelo pela constante.** O teste chama `-m MODELO_CODEX`
   (`agents/code/test/ponta-a-ponta/22-cliente.test.mjs:20` importa; `:102` usa). A constante:
   `agents/code/test/harness-real.mjs:9` = `process.env.HUB_MODELO_CODEX || 'gpt-6-luna'`.
   O corredor só põe `HUB_HARNESS_REAL` e `HARNESSES` (`etapas/logs/corredor-22.ps1:87`). Nada de
   `HUB_MODELO_CODEX` nem modelo à mão. O teste `nenhum teste escreve o modelo do Codex à mão` passa.
2. **Login copiado e apagado.** `evidencia-22/hashes-codex.json`, campo `usos`: codex, copiado
   20:18:48.126Z, apagado 20:18:59.894Z, `apagado: true`. Bate com o relatório (linhas 191-192).
   O `finally` do teste apaga a casa e grava `apagado` (`22-cliente.test.mjs:171-175`).
3. **Hashes.** Antes = depois em `.codex/auth.json`, `.codex/config.toml`, `.codex/AGENTS.md`,
   `.claude/.credentials.json` e nas configs do Claude e do Copilot. Só `.claude.json` mudou
   (6c756b… → 504a58…), como o relatório diz (linhas 193-194). O `after` do teste confere as `CONFIGS` por
   `relatorioDeHashes` e passou (1/1).
4. **Sem token nem caminho do usuário.** `grep -rn -E "ghu_|sk-|refresh_token|access_token|Bearer|eyJ"` e
   `grep -rni -E "gustavo|delfino|GUSTAV~1|C:/Users|C:\\Users"` em `evidencia-22/`: nada. `erros.txt` só tem
   "Reading additional input from stdin...".
5. **Ramo contém a integracao.** `git merge-base --is-ancestor integracao ticket-22` → ok.
   `git diff integracao...ticket-22 --stat`: só 3 arquivos de evidência (`codex/lido.json`, `codex/saida.jsonl`,
   `hashes-codex.json`), 48+/5-.
6. **A evidência sustenta o relatório e o critério.** `saida.jsonl`: `mcp_tool_call` `hub-busca/search`
   (`query: marca1402cf63`, `mode: fulltext`), depois `hub-banco/read_note` do primeiro resultado; resposta com o
   path e a frase da palavra rara. `lido.json` sem `erro`. Token só no ambiente: o teste passa os tokens por `env`
   (`22-cliente.test.mjs:73` e `:96`); o kit grava `bearer_token_env_var` (asserção em
   `agents/code/test/22-kit-cliente.test.mjs:66-67`). Log `etapas/logs/22-harness.log`: 1 pass, 0 fail;
   `22.status` 17:19:03 `harness: saida=0`, 17:19:20 contêineres que sobraram: 0.
7. **Junção.** Diff só de evidência, ramo já sobre a `integracao` atual. Nada a quebrar.

Testes leves (TEMP/TMP = `C:/Users/gustavo.delfino/AppData/Local/Temp`, sem `HUB_*`):
`node --test agents/code/test/22-kit-cliente.test.mjs agents/code/test/22-proxy-sem-docker.test.mjs agents/code/test/harness-real.test.mjs`
→ 14 testes, 14 pass, 0 fail. `git status` limpo depois.

### Ressalvas

1. O modelo não aparece na evidência. O `codex exec --json` não registra o modelo, e o teste não grava o
   `MODELO_CODEX` no `lido.json`. A prova do luna é o código e o corredor sem `HUB_MODELO_CODEX`; uma variável
   herdada do shell que lançou o corredor não deixaria rastro. Para o radar: gravar `modelo: MODELO_CODEX` no
   `lido.json` dos testes com harness.
2. A evidência traz ~156 mil tokens de entrada no turno (`turn.completed`). Só registro de custo.
