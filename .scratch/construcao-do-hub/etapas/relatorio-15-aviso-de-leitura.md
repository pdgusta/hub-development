# Relatório do ticket 15: guardas, aviso de leitura fora da busca (Trilho)

## Estado

- Ramo `ticket-15` (HEAD c789b9d), worktree `C:\context-hub-wt\ticket-15`, de `integracao` c5b946a.
- **Pendente: o ponta a ponta do Codex.** A conta do Codex está no limite de uso até 01:34 de 2026-10-17 (hora de São
  Paulo), o mesmo do ticket 12. Rodo depois, com o do 12.

## Decisões do maestro (2026-10-16)

1. Costuras: (1) o script do hook pela linha de comando, com eventos JSON de cada harness numa sessão em sequência;
   (2) ponta a ponta atrás de `HUB_HARNESS_REAL=1`: Claude dá os avisos; Codex e Copilot medem se a leitura chega ao
   hook. Peça separada em `agents/code/hooks/leitura/`, com fragmentos dos três.
2. "Grande" medido no vault antigo: só tamanhos (bytes e linhas) dos `.md`, só números agregados no relatório, nada de
   caminho nem nome.

## Medida de "grande" (vault antigo, só agregados)

`.md` fora de pastas com ponto (como a busca os vê): **737 notas**.

| | p50 | p75 | p90 | p95 | p99 | maior |
| --- | --- | --- | --- | --- | --- | --- |
| bytes | 6 278 | 14 625 | 40 097 | 84 456 | 185 935 | 347 820 |
| linhas | 74 | 167 | 359 | 654 | 1 245 | 3 016 |

| limite (bytes) | notas acima | bytes dessas notas |
| --- | --- | --- |
| 8 000 | 41% | 89% |
| 16 000 | 23% | 77% |
| **20 000** | **19%** | **72%** |
| 32 000 | 12% | 63% |
| 40 000 | 10% | 58% |

**Proposta: 20 000 bytes** (cerca de 5 mil tokens). As notas acima disso são uma em cada cinco, mas somam 72% do que
um agente leria abrindo tudo inteiro: o aviso cai onde o contexto mais se gasta, e calado na maioria das aberturas.
Abaixo (8 a 16 KB), o aviso sairia em quase metade das notas e viraria ruído; acima (32 a 40 KB), deixaria de fora
mais de um terço dos bytes. Ajustável por `HUB_LEITURA_GRANDE` sem mudar código.

## Desenho

- **Hook depois da ferramenta nos três harnesses**, não antes. Doc (curl, `etapas/doc-15/`):
  - Copilot CLI (`docs.github.com/api/article/body?pathname=/en/copilot/reference/hooks-configuration`): a saída do
    `preToolUse` só tem `permissionDecision`, `permissionDecisionReason` e `modifiedArgs` (sem contexto para o modelo);
    e "Command `preToolUse` hooks are **fail-closed** on errors—a crash or non-zero exit ... denies the tool call". O
    `postToolUse` tem `additionalContext`: "Additional guidance appended to `textResultForLlm` so the model sees it after
    the tool output on the same turn."
  - Claude Code (`code.claude.com/docs/en/hooks.md`), PostToolUse: "`additionalContext` | String added to Claude's
    context alongside the tool result". (O PreToolUse também o tem, entregue no mesmo ponto, "alongside the tool
    result": avisar antes não chega antes.)
  - Codex (`developers.openai.com/codex/hooks.md`), PostToolUse: "`tool_response` | ... MCP tools send the MCP call
    result"; "That `additionalContext` text is added as extra developer context."
  - Resultado: um aviso que nunca recusa e nunca trava a leitura, com a mesma forma nos três.
- **Peça** `agents/code/hooks/leitura/`:
  - `depois-da-ferramenta.mjs <claude|codex|copilot> [--hub]`: lê o evento, decide, devolve o `additionalContext` no
    formato do harness, grava uma linha por leitura do hub em `.local/leitura/registro.jsonl` (hora, harness, sessão,
    caminho, trecho, apontado, aviso). Erro do hook: sem aviso, conta no stderr, sai 0.
  - `leitura.mjs`: adaptadores e decisão. Estado por sessão em `.local/leitura/<sessão>.json` (o que a busca apontou e o
    que já avisou). Caminhos comparados em NFC (o índice da busca guarda NFD; achado 4 do 12). "Dentro do hub" pelo
    mesmo `relativoAoHub` da guarda do 14 (exportado de `guardas/guarda.mjs`).
  - Regras: leitura de arquivo grande que a busca não apontou: "busque antes"; apontado e lido inteiro: "leia o trecho
    que a busca apontou"; apontado e lido em trecho: calado; pequeno: calado; uma vez por arquivo por sessão; fora do
    hub: nada.
  - Contrato com a busca (faixa 3, "Fronteira com a faixa 6"): o servidor `hub-busca`, a ferramenta `search` e os
    `results[].path` do JSON do resultado. O hook acha esse JSON em qualquer bloco de texto do resultado, porque a
    embalagem muda por harness (Claude: `tool_response`; Codex: o resultado MCP; Copilot: `toolResult.textResultForLlm`).
  - Adaptadores: Claude, `Read` (trecho = `offset` ou `limit`) e `mcp__hub-busca__search`; Copilot, `view` (trecho =
    `view_range`) e `hub-busca-search`; Codex, `mcp__hub-busca__search` e `Bash` (ler = `cat`, `type`, `Get-Content`,
    `gc`, `more`, `head`, `tail`, `sed`; trecho = `head`, `tail`, `sed`, `-TotalCount`, `-First`, `-Skip` e afins;
    procurar com `rg`, `grep` ou `Select-String` não conta como ler).
- **Fragmentos** `agents/code/hooks/leitura/fragmentos/{claude,codex,copilot}.json` (com `{{DIR}}` e `{{HUB}}`), no
  molde do 14: Claude `PostToolUse` `Read|mcp__hub-busca__search`; Codex `PostToolUse` `^(Bash|mcp__hub-busca__search)$`;
  Copilot `postToolUse` `view|hub-busca-search`. Timeout de 10 s.

## Testes

- `agents/code/test/15-leitura.test.mjs` (9, pela linha de comando): Claude, os quatro casos e "uma vez por sessão,
  de novo noutra"; pequeno calado; fora do hub; Copilot pelo `view` e pela busca; Codex pelo shell (`Get-Content -Raw`,
  `cat`, `Select-Object -First`, `sed -n`, `rg`) e pela busca; o registro da máquina.
- `node --test "agents/code/test/**/*.test.mjs"` (comum, sem variável): 157 testes, 150 passam, 7 pulados (harness real), 0 falham; `git status` limpo depois.
- Ponta a ponta (`agents/code/test/ponta-a-ponta/15-leitura.test.mjs`, `HUB_HARNESS_REAL=1 --test-concurrency=1`): hub
  de ensaio com a busca do 12 e três notas grandes (A sem a palavra; B e C com "jabuticabeira"); uma sessão com os
  passos: ler A inteira, buscar, ler as linhas 1 a 5 de B, ler C inteira, ler A de novo.
  - Claude Code (haiku): passa. Registro: A "busque antes", B trecho apontado calado, C "leia o trecho", A de novo
    calado; o aviso aparece no evento de hook da saída. Prova também o formato real do `tool_response` da busca.
  - Copilot CLI (claude-haiku-5.5): passa, com o mesmo registro: **o `view` do Copilot alcança o hook**; o aviso veio
    na saída da ferramenta para o modelo.
  - Codex: **não rodou** (cota). O que falta medir: se o `PostToolUse` do `Bash` dispara na leitura por PowerShell do
    Codex no Windows e se as formas de comando que ele usa caem no reconhecimento do adaptador.
  - Evidência: `ponta-a-ponta/evidencia-15/<harness>/` (`saida.jsonl`, `erros.txt`, `registro.jsonl`) e hashes.

## Usos de login (aval da rodada `2026-10-16-login-dos-harnesses-no-ensaio`)

| Harness | O que copiou | Copiado (UTC) | Apagado (UTC) |
| --- | --- | --- | --- |
| Claude | `%USERPROFILE%\.claude\.credentials.json` → `CLAUDE_CONFIG_DIR` de ensaio | 02:24:56 | 02:25:19 |
| Copilot | só `lastLoggedInUser` e `loggedInUsers` do `config.json` → `COPILOT_HOME` de ensaio (token no cofre, não copiado) | 02:29:54 | 02:30:46 |

Datas de 2026-10-17 em UTC (23h24 a 23h30 de 2026-10-16 em São Paulo). Pastas apagadas. Hashes em
`evidencia-15/hashes-claude.json` e `hashes-copilot.json`: as configurações reais (`.claude/settings.json`,
`.codex/config.toml`, `.codex/hooks.json`, `.copilot/config.json`, `.copilot/mcp-config.json`, `.copilot/hooks/*`)
iguais. O `~/.claude.json` real mudou **nas duas** rodadas, inclusive na do Copilot, que não toca o Claude: quem o
regrava são as sessões abertas na máquina (por isso ele só é registrado).

## O que vai doer / não verificado

- **Codex**: a leitura por shell depende de reconhecer o comando. Comando que lê por outro caminho (script, `python`,
  `node -e`, redirecionamento) não avisa; isso é do contrato (user story 30), como a regravação por shell do 14.
- **Trecho por shell**: `Get-Content x | Select-Object -First 20` conta como trecho mesmo quando o filtro está noutro
  comando da mesma linha. O caminho é reconhecido só se termina em `.md`.
- **Estado por sessão em `.local/leitura/`**: um arquivo por sessão, que não se apaga sozinho. Quem limpa (a vigia da
  faixa 7, ou uma passada do kit) fica para o maestro decidir.
- **Busca por `path`** (notas parecidas com uma nota): os `results[].path` contam como apontados, como os da `query`.
- Copilot no modo agente do VS Code: não testado (hooks em Preview, spec).

## Rodada de 2026-10-17 (Trilho): ponta a ponta com só a search do hub-busca
- Codex (03:09): falhou; usou a `read` do `hub-busca` (bloqueada por aprovação). A `read` furaria o aviso nos três
  harnesses. Conserto no 12 (opção A do maestro: só a `search`), trazido para cá por cherry-pick (46e44d2, c1b6133);
  3bc8c8b: o `settings.json` de ensaio do Claude junta o hook de leitura e o deny do `claude-settings.json`.
- Real nos três (03:3x, com a trava): Claude e Copilot passam (evidência 7ad8dee). Codex: "You've hit your usage
  limit ... try again at 6:58 AM". Falta o Codex depois das 06:58.
- Usos de login: Codex 03:09; Claude, Codex e Copilot na rodada dos três; todos apagados ao fim (`apagado: true` em
  `evidencia-15/hashes-claude-codex-copilot.json`). Configurações com hash igual; `.claude.json` só registro.
- Codex depois da cota (07:1x a 07:26, com a trava; `logs/trilho-15-codex-1.log`, `-2.log`, `trilho-15-codex.log`):
  1. Falhou: o shell do Codex foi recusado ("blocked by policy") e a leitura não chegou ao hook do Bash. O 15 não punha
     `sandbox_mode = "danger-full-access"` no `config.toml` de ensaio, como os outros ponta a ponta (14, 19, 20, 27).
     Conserto 03f85fb.
  2. Falhou no passo B (trecho apontado veio "busque antes"). Diagnóstico com um espião temporário (fora do commit,
     apagado): **o Codex entrega a busca ao hook como `mcp__hub_busca__search`**: troca o hífen do servidor por
     sublinhado (a doc oficial só mostra nomes sem hífen). Conserto 64d6875: adaptador e matcher do fragmento do Codex
     com o nome real; o teste sem harness usa o nome real (vermelho antes, 9/9 depois). Claude e Copilot não mudam.
  3. **Passou** (evidência 0283b2c, `evidencia-15/codex/` e `hashes-codex.json`): "busque antes" na leitura inteira sem
     busca; trecho apontado calado; arquivo apontado lido inteiro, "leia o trecho"; uma vez por arquivo.
- Usos de login do Codex nesta rodada: quatro sessões (uma por tentativa), `auth.json` copiado para o `CODEX_HOME` de
  ensaio e apagado ao fim de cada uma (`apagado: true`, 10:25:41 a 10:26:02 UTC na que passou). Configurações reais com
  hash igual antes e depois; `.claude.json` muda pelas sessões abertas (só registro). Sem chave na evidência.
- Ramo `ticket-15` com `integracao` 9cc878b (3d34bd1). Sem harness: `15-leitura.test.mjs` 9/9.
