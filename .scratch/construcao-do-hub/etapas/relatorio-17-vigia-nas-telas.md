# Relatório do ticket 17: vigia nas telas dos harnesses

Vela, 2026-10-17. Ramo `ticket-17`, worktree `C:/context-hub-wt/ticket-17`, de `integracao` 9453e3e (com o 09).
Começou antes do 16, por mandato do maestro (05:09): contra o `estado.json` combinado em `etapas/costuras-16-Trilho.md`
(exemplo fixo nos testes). Costuras aceitas em `etapas/costuras-17-Vela.md` (05:12).

## O que se fez

- `agents/code/hooks/vigia/tela.mjs`, a regra do texto num lugar só (`resumo()` e `linha()`):
  - `inicio <claude|codex|copilot> --hub`: o resumo no começo da sessão. Claude Code e Codex pelo `SessionStart`
    (`hookSpecificOutput.additionalContext`); Copilot pelo `sessionStart` (`additionalContext` no topo). Divergência:
    o aviso, cada item pelo caminho, e "Comece a resposta com este aviso". Tudo em ordem: uma linha curta, e o agente
    não fala dela. Outro par sem resposta: só a hora da última troca. Passada com mais de 15 min: diz desde quando.
    Fora do hub (caminho real): nada.
  - Reserva sem o arquivo: o `estado_do_hub` do MCP do banco (leitura, Cinzel, ticket 10), por `HUB_MCP_BANCO_LEITURA_URL`
    e `HUB_MCP_BANCO_LEITURA_TOKEN` (Bearer). Streamable HTTP com resposta SSE, `initialize` antes, `mcp-session-id`
    depois. Pelo `node:http`, sem agente: o `fetch` deixava a conexão viva, e o node no Windows caía ao sair
    (asserção do libuv, `src\win\async.c`). Sem arquivo e sem MCP: "estado indisponível", nunca "em ordem".
  - `notify '<json>'`: o programa do `notify` do Codex (doc "Notifications": um argumento JSON, tipo
    `agent-turn-complete`). Com divergência, chama o notificador do 16 (`HUB_VIGIA_NOTIFICAR`, senão
    `agents/skills/vigia/notificar.ps1`), só quando a assinatura (os itens fora de `ok`, com o nível) muda. A memória
    fica em `<hub>/.local/vigia/notify-codex.json`. Se o notificador falha, a assinatura não é gravada.
  - `barra <claude|copilot> --hub`: uma linha (`hub: divergência: ...`, `hub: em ordem (hh:mm)`,
    `hub: estado indisponível`). Lê só o arquivo, sem MCP.
- Fragmentos em `agents/code/hooks/vigia/fragmentos/`: `claude`, `codex`, `copilot`, `codex-notify`,
  `copilot-statusline` (`{{DIR}}`, `{{HUB}}`; o kit, ticket 23, os junta).
- Mod do Claude Code `agents/code/mods/vigia/` (plugin `vigia-do-hub`): `session.start`, `turn.start` e
  `$.clock.every(60 s)` chamam `tela.mjs barra claude` e põem o texto em `$.ui.status`.

## Escolhas (aceitas pelo maestro, 05:12)

1. A reserva pelo MCP, com as variáveis e o formato confirmados com o Cinzel.
2. Mod pela linha de status (`$.ui.status`). A faixa acima do prompt fica para o Gustavo, se ele quiser.
3. `barra-copilot.cmd` só se precisasse. Não precisou: no `app.js` do `@github/copilot-win32-x64` 1.0.98, o
   `statusLine.command` roda com `shell: true`, na pasta da sessão, com o JSON na entrada e 10 s de limite; comando com
   argumentos funciona.
4. Com `ok`, a linha curta é injetada e o agente fica calado sobre ela.
- A barra não consulta o MCP: roda a cada 60 s, e o MCP é reserva do começo da sessão.
- O Codex tem dois canais: o início da sessão e o `notify`. A vigia notifica à parte quando piora (16). Os dois ficam,
  por decisão (spec, faixa 7).

## Testes

- `node --test agents/code/test/17-vigia-tela.test.mjs`: 15/15. Com o 29 (`harness-real.test.mjs`): 21/21.
- `cd agents/code/mods/vigia && claude plugin validate . && claude plugin test .`: 2/2.
- **Ponta a ponta real** (`agents/code/test/ponta-a-ponta/17-vigia-tela.test.mjs`, `HUB_HARNESS_REAL=1`), com a trava
  pesada, 2026-10-17 06:22 a 06:24:
  - Claude (haiku) e Copilot (claude-haiku-5.5): **4/4**. Com divergência, a resposta começa pelo aviso e cita
    `reuniao.md`. Sem arquivo e sem MCP, o agente repete "estado indisponível".
  - Evidência em `evidencia-17/<harness>/<cenario>/` (saída, resposta, erros) e `hashes-claude-copilot.json`.
  - Codex (gpt-6-luna, esforço baixo), 07:26, com a trava: **2/2**. O `notify` do fim do turno chamou o notificador
    (dublê) uma vez, com "Hub: divergência" e a nota. Evidência em `evidencia-17/codex/` e `hashes-codex.json`
    (copiado `%USERPROFILE%\.codex\auth.json` para o `CODEX_HOME` de ensaio; apagado; hashes iguais).
- Login no ensaio (aval do Gustavo, rodada `2026-10-16-login-dos-harnesses-no-ensaio`), uma sessão por harness e
  cenário:
  - Claude: copiado `%USERPROFILE%\.claude\.credentials.json` para o `CLAUDE_CONFIG_DIR` de ensaio;
  - Copilot: copiados só `lastLoggedInUser` e `loggedInUsers`; o token fica no cofre do Windows.
  - Pastas `%TEMP%\hub-ensaio-17-*` apagadas ao fim de cada sessão (`apagado: true` nas quatro). Hashes das pastas
    reais iguais antes e depois. Sem token na evidência (procurado por `ghu_`, `sk-`, `refresh_token`,
    `access_token`).
- Conserto de passagem (0e74227): o teste unitário do 17 dizia `'codex.json'`, e o detector do 29 (marca `codex\.js`)
  o tomava por teste de harness. O ajudante `fragmento()` recebe agora o nome sem a extensão.

## Não verificado

- A linha de status do mod do Claude Code e a statusLine do Copilot na tela de verdade: o modo `-p` não tem tela. O
  texto é o mesmo da `barra`, testada pela linha de comando e pelo `claude plugin test`.
- O toast do notificador de verdade: o dublê só conta as chamadas. O `notificar.ps1` vem com o 16.

## Falta

1. Quando o 16 entrar em `integracao`: `git merge integracao`, e um teste sobre o `estado.json` que o `vigia passada`
   grava, no lugar do exemplo fixo.
2. Revisão do Fiel, depois o Rebite. A junção só com o 16 resolvido.

Também feito: `integracao` 9cc878b juntada (5187a86, com o 36); o teste do 17 usa o ajudante comum de pasta de ensaio
(273579f), 15/15 sem sobra.
