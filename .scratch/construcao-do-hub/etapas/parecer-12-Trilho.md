# Parecer do Fiel — ticket 12, busca local com aceite (Trilho)

## Rodada 1 — 2026-10-17 — ramo ticket-12 em 0ba8532

Veredito: **volta**, por um conserto pequeno; o resto passa. A rodada curta já combinada para o Codex fecha os dois.
Revisado pelo Fiel; leitura do Fielzinho fica para depois (cota do Codex), por ordem do maestro.

Conferido: integracao dc56d47 ancestral; worktree limpo antes. Li o ticket 12, o relatório, `iniciar.ps1`, os
fragmentos de registro (`claude.json`, `codex.toml`, `copilot.json`) e o teste de Host.

Evidências (Fiel):
1. `node --test --test-concurrency=1 agents/code/test/12-busca.test.mjs agents/code/test/12-kit-busca.test.mjs`, sem
   `HUB_BUSCA_OHS` nem `HUB_HARNESS_REAL` (instala pelo kit): 13/13. Os cinco critérios do ticket estão cobertos
   (palavra e paráfrase entre as 3; tempo da nota nova medido; nada com ponto nem `local: true`; relatório com
   recusadas; Host estranho 403 e segunda partida reaproveitando o índice). Log `etapas/revisao-12-r1-testes.log`.
2. `.obsidian-hybrid-search.db*` está no `.gitignore` da raiz (o servidor respeita o `.gitignore`).
3. Aceite com harness real: Claude e Copilot pela evidência do relatório; Codex pendente (cota).

### Consertos

1. **(Fiel) O teste comum regrava evidência versionada.** `12-busca.test.mjs:28` grava
   `agents/code/test/12-busca/evidencia/medidas.json` a cada rodada, sem variável: depois da minha rodada, o arquivo
   ficou modificado (12 linhas; desfeito por mim com `git checkout`). É a classe que o ticket 29 fechou: o comando
   comum não pode sujar a árvore. Gravar as medidas fora do git (ex.: `%TEMP%` ou `.local`) no teste comum e versionar
   só sob pedido (variável própria ou a rodada de evidência); `git status` limpo depois da suíte.

### Ressalvas (não seguram)

- O servidor faz `GET registry.npmjs.org/.../latest` a cada partida (achado 6 do relatório): rede na partida.
- Proxy (faixa 10): o `iniciar.ps1` não passa `--allowed-host`; quando a busca for servida por proxy, o Host observado
  precisa entrar (spec, Worker 3).
- O `reindex` incremental pela vigia (achado 2) é costura com a faixa 7.

### Rodada curta

O commit de evidência do Codex junto com o conserto 1; eu confiro a evidência do Codex, rodo os 13 e o `git status`.

## Rodada 2 (curta) — 2026-10-17 — ramo ticket-12 em cc96be2

Veredito: **passa**. Revisado pelo Fiel sozinho (Fielzinho sem cota; lê depois).

1. Diff 0ba8532..cc96be2: só `12-busca.test.mjs`; medidas sempre no log ("medidas do ticket 12:"), `medidas.json` só
   com `HUB_GRAVAR_MEDIDAS=1`.
2. 12-busca + 12-kit-busca sem `HUB_BUSCA_OHS`, `HUB_HARNESS_REAL` nem `HUB_GRAVAR_MEDIDAS`: 13/13, saída 0;
   `git status` vazio depois. Log `etapas/revisao-12-r2-testes.log`.

Pendente (não segura, por decisão do maestro): o aceite real do Codex, num commit só de evidência depois das 01:34
(hora de São Paulo), com outra rodada curta do Fiel.
