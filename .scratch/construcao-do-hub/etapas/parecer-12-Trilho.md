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

# Rodada 3 (nova, pedida pelo maestro) — Fiel — 2026-10-17 ~04h

Ramo ticket-12, HEAD 8558abe; contém integracao 763813a. Commits 0ea1016, 34ed657, 3faad20, 8558abe. Decisão (A) do
ticket 15 (~03h50): o fragmento expõe só a `search` do hub-busca nos três. Fielzinho sem cota até 06h58: Fiel sozinho,
leitura do Fielzinho pendente.

## Veredito: PASSA (com ressalvas)

## Conferido
- Fragmentos: `claude-settings.json` (deny `mcp__hub-busca__read|reindex|status`, JSON válido), `codex.toml`
  (`enabled_tools = ["search"]`, `tools.search.approval_mode = "approve"`, TOML válido), `copilot.json`
  (`tools: ["search"]`). README cita a doc (permissions.md, codex mcp.md, Copilot add-mcp-servers).
- Nome canônico do deny: a evidência do Claude (`evidencia-12/claude/lido.json`) traz `ferramentas` do `init` =
  só `mcp__hub-busca__search`; o deny pelo nome tirou as outras do contexto.
- Copilot: a saída antiga (integracao) listava `hub-busca-read`, `-reindex`, `-status`; a nova não lista nenhuma
  delas, só `hub-busca-search`.
- Real nos três: 2 chamadas de `search` cada (fulltext e semantic), `outras: []`, resposta
  `inbox/viveiro-na-cobertura.md`. Hashes: login igual antes/depois; `.claude.json` muda, mas está em `SO_REGISTRO`
  (a sessão viva do Claude grava nele; já aceito nas rodadas anteriores). Pastas de ensaio apagadas (`usos`).
- `node --test ponta-a-ponta/12-busca.test.mjs` sem variável: 1 pulado, 0 falhas. Árvore limpa. Harness real não
  repetido pelo Fiel: evidência fresca do commit 8558abe.

## Ressalvas (não bloqueiam)
1. O teste só afirma a lista de ferramentas no Claude (`if (lido.ferramentas)`). No Copilot a saída já mostra a lista
   e daria para afirmar "sem `hub-busca-read`"; no Codex não há lista na saída, só "não chamou". A prova de que a
   `read` não está ao alcance no Codex fica para o real do 15.
2. Ao ligar com o 15: o `15-leitura.test.mjs` de integracao grava `claude.json`, mas não grava o
   `claude-settings.json`. Sem o deny, o Claude do real do 15 ainda vê a `read`. A rodada do 15 precisa gravar o
   fragmento novo.
3. Nada instala o `claude-settings.json` fora dos testes. O kit que fizer isso tem de **juntar** a regra na
   `permissions.deny` do `settings.json` de verdade, sem sobrescrever.

## Leitura do Fielzinho — rodada 3 — 2026-10-17

**PASSA, sem achado novo.** Leitura concluída em 8558abe; detalhes no parecer-12-Trilho-fielzinho.md. Conferidos fragmentos e evidências dos três: duas buscas, sem outra ferramenta, caminho esperado; Claude só expõe search. Costura do deny com o 15 conferida em 3d34bd1. Prova própria sem HUB_HARNESS_REAL: 1 skip, 0 falhas; não representa rerun do aceite real. Hashes e limpeza lidos na evidência existente; só .claude.json difere como registro documentado. Sem indexação nem harness real próprios. Ressalvas registradas mantidas.
