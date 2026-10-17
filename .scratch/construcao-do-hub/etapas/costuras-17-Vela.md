# Ticket 17: costuras propostas (Vela, 2026-10-17 ~05h20)

Ramo `ticket-17`, worktree `C:/context-hub-wt/ticket-17`, da ponta de `integracao` (9453e3e, já com o 09). Contra o `estado.json`
combinado em `costuras-16-Trilho.md`: `{ passada, outro_par: { situacao: ligado|sem-resposta|nao-verificavel, motivo },
nivel, resumo, itens: [{ id, nivel, resumo, caminho?, ultima_troca?, fonte }], vistos }`, com um exemplo fixo nos testes
(um por cenário). Quando o 16 entrar: `git merge integracao` e um teste a mais sobre o arquivo que o `vigia passada`
grava.

## Onde mora
- `agents/code/hooks/vigia/tela.mjs`: um script, três modos, a regra num lugar só:
  - `inicio <claude|codex|copilot> --hub <hub>`: evento de início na entrada; devolve o resumo no formato de cada
    harness (Claude/Codex `hookSpecificOutput.additionalContext`; Copilot `additionalContext` no topo, como o 20).
  - `notify --hub <hub> '<json>'`: o programa do `notify` do Codex (um argumento JSON, `type: agent-turn-complete`,
    `cwd`; doc `developers.openai.com/codex/config-advanced.md`, "Notifications").
  - `barra <claude|copilot> --hub <hub>`: uma linha para a `statusLine` do Copilot (JSON da sessão na entrada; doc
    `cli-config-dir-reference`, `statusLine`) e para o mod.
- `agents/code/hooks/vigia/fragmentos/`: `claude.json`, `codex.json`, `copilot.json` (SessionStart/sessionStart),
  `codex-notify.json` (a linha `notify` do config.toml) e `copilot-statusline.json` (o `statusLine` do config.json).
- `agents/code/mods/vigia/`: mod do Claude Code; `$.ui.status(<linha>)` em `session.start` e num `$.clock` de 60 s,
  com a linha que o `barra claude` devolve (a regra fica no script).

## Regra do texto (um lugar só, no tela.mjs)
- Fonte: `<hub>/.local/vigia/estado.json`; sem ele, a ferramenta `estado_do_hub` do MCP do banco (leitura) por HTTP;
  sem os dois, "estado indisponível" (nunca "em ordem").
- `divergencia`: "Vigia do hub: divergência: <resumo>; <itens de divergência pelo caminho>. Comece a resposta com este
  aviso." `informa`: a linha, sem pedir aviso. `ok`: "Vigia do hub: tudo em ordem (passada <hora>)".
- Outro par sem resposta: só "a outra máquina não responde; última troca às <hora>" (sem alarme).
- Passada com mais de 15 min: "a vigia não roda desde <hora>" (o mesmo aviso do `estado_do_hub` do Cinzel).
- Fora do hub (caminho real, `lib/caminhos.mjs`): nada, nos três modos.

## Costuras (o teste só olha o lado de fora)
1. **`tela.mjs inicio`** com a entrada JSON de cada harness e um `estado.json` de exemplo: divergência (conflito
   citado pelo caminho), informa (outro par sem resposta, com a hora da última troca), ok, passada velha; sem arquivo
   e com um MCP dublê (servidor HTTP local que responde `initialize` e `tools/call estado_do_hub`), o resumo vem dele;
   sem arquivo e sem MCP, "estado indisponível"; fora do hub, saída vazia.
2. **`tela.mjs notify`** com o JSON do Codex: divergência notifica uma vez (notificador dublê por
   `HUB_VIGIA_NOTIFICAR`, o mesmo do 16); o mesmo estado de novo, não; o estado muda (outro item, ou volta a ok e
   diverge de novo), notifica; ok não notifica; fora do hub, nada. Memória em `<hub>/.local/vigia/notify-codex.json`.
3. **`tela.mjs barra`** com o JSON da sessão do Copilot: a linha do arquivo de exemplo; fora do hub, vazia.
4. **Mod**: `claude plugin validate` e `claude plugin test` (o status mostra a linha do exemplo).
5. **Harness real** (fila, aval de login, HOME de ensaio, molde do 27/19): `claude -p`, `copilot -p` e, depois das
   06h58, `codex exec`, com os fragmentos de início: com divergência no exemplo, a resposta começa com o aviso; sem
   arquivo e sem MCP, diz "estado indisponível"; fora do hub, nada. O toast do `notify` e a `statusLine` na tela não
   rodam em modo não interativo: ficam pelos testes 2 e 3 e como "não verificado" no relatório.

## Perguntas
1. **MCP de reserva**: as variáveis (`HUB_MCP_BANCO_LEITURA_URL` e `HUB_MCP_BANCO_LEITURA_TOKEN`, do spec) e o
   formato da resposta do `estado_do_hub` (texto do JSON?): confirmo com o Cinzel.
2. **Forma do mod**: proponho a linha de status (`$.ui.status`), sempre visível e leve; a faixa acima do prompt só se
   o Gustavo quiser.
3. **`statusLine` do Copilot**: a doc diz "path to an executable script"; se não aceitar argumentos, um
   `barra-copilot.cmd` ao lado. Confiro no real.
4. **Resumo com `ok`**: proponho injetar a linha curta também com `ok` (o agente não fala dela); o spec pede a resposta
   calada com `ok`.
