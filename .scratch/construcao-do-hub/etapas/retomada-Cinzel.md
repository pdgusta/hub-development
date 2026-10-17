# Retomada do Cinzel (construtor, Claude)

Leia antes: `etapas/regras-da-construcao.md` (inteiras, com os "Achados comuns"), o ticket 11
(`issues/11-mcp-do-banco-pelos-tres-harnesses.md`, com os comentários) e esta retomada.

## Feitos (nada pendente)

- 09 e 10: juntados e resolvidos pelo Rebite. Hub `integracao` 9cc878b; fork `C:/Projetos/hub-mcp-banco`, ramo
  `integracao` 34c3e50. O fork principal (a pasta) segue no ramo `ticket-09`. A worktree do fork
  `C:/Projetos/hub-mcp-banco-wt/ticket-10` ainda existe. Ao remover qualquer worktree do fork, solte antes as junções
  com `cmd /c rmdir <wt>\node_modules` e `cmd /c rmdir <wt>\lib\livesync-commonlib`.

## Ticket 11: MCP do banco pelos três harnesses (em revisão com o Fiel; falta o Codex)

- **Hub:** worktree `C:/context-hub-wt/ticket-11`, ramo `ticket-11`, ponta ab374b4 (com `integracao` e2b7607 juntada).
- **Fork:** sem mudança. Worktree `C:/Projetos/hub-mcp-banco-wt/ticket-11`, ramo `ticket-11` do `integracao` do fork,
  34c3e50. O `dist` está montado (`npx tsup`); as junções são as de cima.
- **Costuras:** `etapas/costuras-11-Cinzel.md`. Decisões do maestro, registradas no 11:
  - o fork roda em modo local, sem Docker;
  - duas sessões do Copilot;
  - a "regra seguida" e o banco recriado ficam fora, como ressalva para o 25 (já no relatório).
- **Relatório:** `etapas/relatorio-11-mcp-do-banco-pelos-harnesses.md`, com a rodada 1 analisada e o Codex marcado
  PENDENTE.
- **Código** (tudo em `agents/code/test/`):
  - `11-mcp-banco/montagem.mjs`: marcas, `iniciarFork`, `mcp`, `conferir`;
  - `11-mcp-banco/captura.mjs`: o repasse que guarda a requisição; `ondeEsta`;
  - `11-mcp-banco.test.mjs`: sem harness, 4/4;
  - `ponta-a-ponta/11-mcp-banco.test.mjs`: o aceite. Rodadas `claude`, `codex`, `copilot-sem` e `copilot-com`, ou só
    as escolhidas por `RODADAS=`.
- **Rodada 1** (07:28 a 07:36, `etapas/logs/11-harness-1.log`, evidência `ponta-a-ponta/evidencia-11/`, já no commit):
  - Claude passou. A cabeça chega inteira; a regra curta só depois de um `ToolSearch` (ferramentas adiadas).
  - Copilot sem a opção: `NAO-RECEBI`. As instruções estão no evento `session.mcp_servers_loaded`, mas fora do prompt.
  - Copilot com a opção: tudo chega.
  - Codex: falhou por erro do teste. O `spawnSync` travava o repasse, que roda no mesmo processo. Conserto em bfd1af3:
    o Codex roda por `spawn` (`rodarSemTravar`).
- **Próximo passo exato:**
  1. Feito: parecer da rodada 1 do Fiel, sem conserto (`etapas/parecer-11-Cinzel.md`). Ressalvas levadas ao maestro.
  2. **Depois de 12h15** (cota do Codex), na vez da fila (item 4 de `etapas/fila-pesada.md`), na pasta da construção:
     `pwsh -NoProfile -File etapas/logs/11-corredor.ps1 -Rodadas codex`. O corredor pega e solta a trava; o estado fica
     em `etapas/logs/11-corredor.status` e o log em `11-harness-<n>.log`. Ao soltar a trava, avisar o maestro.
  3. (Maestro, 07:58: tirar da evidência a lista de skills da máquina — `%USERPROFILE%/.agents/skills` — na rodada 2, também a do Copilot.) Ler `evidencia-11/codex/lido.json` (`captura`: em que campo vão as marcas A e B, a regra e o `estado_do_hub`, mais
     `em_volta_de_A`). Pôr no relatório (rodada 2 e critérios), fazer o commit da evidência e pedir a rodada 2 ao Fiel.
  4. Depois do "passa": avisar o Rebite (hub `ticket-11`; o fork não muda).
- **Se o Codex falhar na captura:** o provedor próprio (`model_provider = "hub_captura"`, `requires_openai_auth`,
  `supports_websockets = false`) foi respeitado: na rodada 1, ele foi ao repasse. Se o backend recusar, a reserva é
  `openai_base_url` (ver a doc abaixo). Se nada servir, perguntar ao maestro.

## Ticket 23: kit de par, a forma (desde ~08h20)

- Hub: worktree `C:/context-hub-wt/ticket-23`, ramo `ticket-23` de `integracao` e2b7607.
- Costuras em `etapas/costuras-23-Cinzel.md`, respondidas (as três como recomendado). Relatório em
  `etapas/relatorio-23-kit-de-par-a-forma.md` (fatos de fonte e sonda do app-server).
- Feito (tdd, `agents/code/test/23-kit.test.mjs`, 6/6, commit no ramo): instalar.ps1, registro da casa (`kit/casa.mjs`),
  contrato, skills gerais por junction (8 skills marcadas `metadata.camada: geral`), MCP de busca e banco nos três.
- Falta: hooks (fragmentos + hooks.state pelo app-server numa cópia temporária), GSD, Codex (sandbox), 00 conferir,
  10-manutencao.ps1, copilot-instructions com texto além do GSD (parar e mostrar).
- Próximo passo antigo (já feito): com as respostas, `tdd` pelo
  `23-kit.test.mjs` sem harness; antes de codar o MCP, ler por curl a doc do Claude e do Copilot sobre variável de
  ambiente no cabeçalho e a chave do Copilot para as instruções do servidor.
- O Codex do 11 tem prioridade às 12h15.

## Fatos de fonte (doc do Codex lida por curl em 2026-10-17)

- <https://developers.openai.com/codex/mcp.md>:
  - "Codex reads the MCP `instructions` field returned during initialization and uses it as server-wide guidance
    alongside the server's tools";
  - "Keep the first 512 characters self-contained";
  - HTTP: `bearer_token_env_var`, `http_headers`, `enabled_tools` e `tools.<tool>.approval_mode`.
- <https://developers.openai.com/codex/config-reference.md>:
  - `openai_base_url`: "Base URL override for the built-in `openai` model provider";
  - `model_providers.<id>.base_url`, `requires_openai_auth` e `supports_websockets` ("Whether that provider supports
    the Responses API WebSocket transport");
  - `chatgpt_base_url` é só o fluxo de login.
- O Codex 0.162.1 tem login do ChatGPT (`auth_mode: chatgpt`): o endereço de verdade é
  `https://chatgpt.com/backend-api/codex`. O `codex exec` fora de repositório git pede `--skip-git-repo-check`.

## Armadilhas

- `%TEMP%` é curto (`GUSTAV~1.DEL`): use `realpath` para o Claude Code e o fork em modo local.
- `src/*.ts` do fork: editar com o Edit.
- Os unitários do fork pedem `TEMP` e `TMP` no caminho longo (272/1 é a base). No e2e local (36/7 é a base), a
  primeira rodada às vezes cai inteira porque o servidor demora a subir: rode de novo.
- Codex: o hífen do nome do servidor vira sublinhado no hook (achado do 15). A leitura do 11 aceita os dois.
- `maestri ask` sem barra invertida nos caminhos. `ask` longo vai em segundo plano: ele espera a resposta do outro.
- Contagem de PASSA: conte as linhas `[PASSA]` no log, não de cabeça (no 10, eu errei: eram 32, não 34).
