# Parecer do Fiel — ticket 27, o verificador cuida das pastas (Vela)

## Rodada 1 — 2026-10-17 — ramo ticket-27 em 8d8f1b9

Veredito: **volta**. Fiel e Fielzinho de acordo (parecer-Vela-fielzinho.md, nesta pasta).

Conferido pelo Fiel: integracao 8d1d785 ancestral; worktree limpo; li ticket 27, relatório, `nucleo.mjs`,
`verificar-pastas.mjs`, `lib/pastas.mjs`, e o spec (faixa 1, story 44). Ponta a ponta real não repetida nesta
rodada (os consertos mexem no núcleo; repetir na rodada 2).

### Consertos (cinco; os cinco achados pelo Fielzinho; 2, 4 e 5 reproduzidos também pelo Fiel)

1. **AGENTS.md e SKILL.md tocados pela conferência de links** (`verificar-pastas.mjs:58`). O spec (faixa 1) diz que
   o verificador não toca esses dois. Reprodução no parecer do Fielzinho. Excluir os dois nomes, com teste no CLI e
   pelo fim.
2. **Turno sem gravação faz a passada no hub inteiro.** `nucleo.mjs:69` chama `verificar-pastas` mesmo com a lista
   vazia, e o CLI (`verificar-pastas.mjs:94`) entende "sem alvo" como o hub inteiro, com `--corrigir`. Reprodução do
   Fiel: no hub de ensaio limpo (git), o CLI sem alvo regravou `clients/aurora/migracao-de-tenant/inputs/index.md` e
   `initiatives/context-hub/labs/index.md`. O fim não deve rodar o verificador sem arquivo mudado; teste de que nada
   muda num turno sem gravação.
3. **Avisos não chegam ao agente.** `nucleo.mjs:73` só guarda `falta|recusa`; o link corrigido nos dois sentidos e o
   aviso de `other/` se perdem, e o `registro.jsonl` também não os guarda. O ticket pede "avisando o agente" e "geram o
   aviso de bloco novo". Entregar os avisos no fim sem contar como devolução (ex.: texto de saída/aviso do harness,
   ou junto da próxima devolução) e provar links e `other/` pelo canal do fim; guardar no registro.
4. **URI malformada derruba o verificador e o fim diz "sem falta".** `pastas.mjs:109` (`decodeURI` sem `try`);
   `nucleo.mjs:57` ignora `status`/`stderr` do `spawnSync`. Reprodução do Fiel: nota com `[a](x%ZZ.md)` → `URIError`
   no CLI. Tratar por link (vira falta daquela nota), seguir as outras notas, e tratar queda do subprocesso como
   falta, nunca "sem falta".
5. **`par://` para dentro de `.secrets/` passa calado.** `pastas.mjs:142-144` volta o original quando não replica,
   sem `emSegredo`. Reprodução do Fiel: `[a](par://pc/clients/aurora/.secrets/senha.txt)` → nenhuma linha de falta.
   Aplicar a regra do `.secrets/` também ao `par://`; teste no CLI e pelo fim.

### Ressalvas (não seguram)

- **Link para fora do hub** (story 44 e spec "Links" incluem "fora do hub" no `par://`, mas o caminho é "a partir da
  raiz do hub", o que não existe para fora dele). O critério do ticket 27 cita só `local: true`. Não é conserto
  desta rodada; ponto aberto para o maestro.
- `.codex/config.toml` real mudou durante a rodada dos três (00:15:51 UTC); a causa (sessões reais do Codex) é
  hipótese; a repetição do Codex saiu com hashes iguais.
- A vigia regravar o `estado.json` inteiro e apagar o item `fim-da-resposta`: costura com o dono da vigia.
- O deslize do subagente está declarado no relatório.

### Para a rodada 2

Commit com hash; suíte sem harness; ponta a ponta dos três de novo (o núcleo muda), com a regra do login.

## Rodada 2 — 2026-10-17 — ramo ticket-27 em 5df8972

Veredito: **passa**. Fiel e Fielzinho de acordo (parecer-Vela-fielzinho.md, rodada 2).

Evidências (Fiel):
1. Diff 8d8f1b9..5df8972 lido: `INTOCAVEIS` (AGENTS.md, SKILL.md) em `conferirLinks`; `conferir` não roda nada sem
   arquivo mudado; avisos entregues uma vez por sessão (`avisados`), sem gastar devolução, e no registro; `porLink`
   pega `URIError` por link; `rodar` trata saída fora de 0/1, erro e pilha no stderr como queda = falta;
   `emSegredo` no ramo `par://`.
2. `node --test "agents/code/test/*.test.mjs" agents/code/test/gerar-exclusoes/gerador.test.mjs`: 106/106 (sem
   ponta-a-ponta, pela regra provisória do maestro).
3. Minhas reproduções da rodada 1 no código novo: `par://` para `.secrets/` → falta; `[b](x%ZZ.md)` → falta
   "caminho malformado", e a nota seguinte continua conferida; link para `labs/` → aviso de `par://`; `inbox/AGENTS.md`
   com link para `labs/` → intocado.
4. Ponta a ponta dos três: não repetida pelo Fiel; evidência nova lida pelo Fielzinho (três devolvem e soltam,
   continuação do Copilot, 8 hashes iguais, 3 pastas apagadas).

Ressalvas: as da rodada 1 seguem (link para fora do hub, aberto ao maestro; vigia × item `fim-da-resposta`). Menor: na
quarta parada (solta para a vigia) os avisos novos daquela parada não são entregues nem marcados como avisados.
