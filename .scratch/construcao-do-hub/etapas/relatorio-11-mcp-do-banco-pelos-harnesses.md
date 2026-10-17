# Relatório do ticket 11: MCP do banco pelos três harnesses (Cinzel)

- **Hub:** worktree `C:\context-hub-wt\ticket-11`, ramo `ticket-11` da ponta de `integracao` 9cc878b (já com o 10).
- **Fork:** sem mudança. Uma worktree `C:\Projetos\hub-mcp-banco-wt\ticket-11` (ramo `ticket-11` do `integracao` do
  fork, 34c3e50), só para ter o `dist` montado com o 10. `node_modules` e `lib/livesync-commonlib` são junções para o
  fork principal.
- **Costuras:** `etapas/costuras-11-Cinzel.md`, aceitas pelo maestro (comentário do ticket 11).
  - O fork roda em modo local, sem Docker; o banco cifrado inteiro fica para o 25.
  - Duas sessões do Copilot.
  - A "regra seguida" e o banco recriado ficam fora (ressalva para o 25, abaixo).

## O que foi construído

Tudo em `agents/code/test/`. Nada em produção: o ticket mede o que chega a cada harness.

| Arquivo | O que faz |
|---|---|
| `11-mcp-banco/montagem.mjs` | Marca um hub de ensaio com três marcas aleatórias: A no começo e B no fim da cabeça do `AGENTS.md` (a cabeça fica abaixo de 2.000 caracteres), C no `resumo` de um `.local/vigia/estado.json` de exemplo. Sobe o fork em modo local (`VAULT_PATH` = `HUB_ROOT` = o hub) em 127.0.0.1, com token. `conferir` acha numa resposta as marcas e o começo da regra curta. |
| `11-mcp-banco/captura.mjs` | Um repasse em 127.0.0.1 que manda cada pedido ao endereço de verdade, devolve a resposta como veio (SSE aos pedaços) e guarda o corpo, uma linha JSON por pedido. Dos cabeçalhos, só os de formato: nada de `Authorization`, cookie ou conta. `ondeEsta` dá o caminho de cada campo do corpo que contém um texto. |
| `11-mcp-banco.test.mjs` | Sem harness, na suíte comum: 4 casos (montagem, captura, `ondeEsta`, leitura). O da montagem pede o fork com o 10 (`HUB_MCP_BANCO_DIR`); sem ele, aparece pulado. |
| `ponta-a-ponta/11-mcp-banco.test.mjs` | O aceite com os harnesses de verdade (`HUB_HARNESS_REAL=1`, `--test-concurrency=1`), no molde do 12. |

Como o aceite roda:
- **Fora do hub.** Cada harness roda numa pasta de trabalho vazia, fora do hub. O Codex e o Copilot leem o
  `AGENTS.md` do diretório, e assim a marca só chega pelo servidor.
- **O mesmo pedido para todos.** O harness tem de copiar:
  - a primeira linha das instruções do `hub-banco` (ou `NAO-RECEBI`);
  - a linha "Marca do fim";
  - as primeiras palavras da descrição do `write_note`;
  - o `resumo` do `estado_do_hub`, chamando a ferramenta.
- **Gravação.** Só `estado_do_hub` vai aprovada; as ferramentas de gravação ficam visíveis, sem aprovação.
- **O Codex** passa por um provedor de modelo próprio no `config.toml` de ensaio: `base_url` = o repasse,
  `requires_openai_auth = true`, `supports_websockets = false`. O repasse manda tudo a
  `https://chatgpt.com/backend-api/codex`, porque o login é do ChatGPT.

## Critérios do ticket

| Critério | Resultado |
|---|---|
| os três harnesses citam o que receberam do servidor | Claude Code e Copilot: PASSA (rodada 1). Codex: PENDENTE, sem cota até 12h15 |
| a requisição do Codex é capturada para ver onde o `instructions` chega | PENDENTE, sem cota até 12h15. A captura está pronta e testada sem harness (4/4) |
| no Copilot CLI, com e sem a opção que libera as instruções do MCP | PASSA: as duas sessões rodaram; o resultado está abaixo |

### Rodada 1 (07:28 a 07:36, com a trava)

`etapas/logs/11-harness-1.log`. Evidência em `agents/code/test/ponta-a-ponta/evidencia-11/`.

| Rodada | Marca A (começo da cabeça) | Marca B (fim da cabeça) | Regra curta (`write_note`) | `estado_do_hub` (marca C) |
|---|---|---|---|---|
| Claude Code 2.1.302, haiku | citada | citada | citada, **depois de um `ToolSearch`** | chamada e citada |
| Copilot CLI 1.0.98, claude-haiku-5.5, **sem** `--allow-all-mcp-server-instructions` | `NAO-RECEBI` | `NAO-RECEBI` | citada | chamada e citada |
| Copilot CLI, **com** a opção | citada | citada | citada | chamada e citada |
| Codex 0.162.1, gpt-6-luna baixo | — | — | — | falhou: erro do teste (abaixo) |

O que isso mostra:
- **Claude Code:** a cabeça chega inteira até a marca do fim, então os 2.000 caracteres cabem no corte. As
  ferramentas MCP vêm adiadas: as 12 do `hub-banco` estão listadas no início, mas a descrição do `write_note` só
  chegou depois de o modelo chamar `ToolSearch`. É a "busca de ferramentas adiada" dos pontos abertos do spec: a
  regra curta chega quando o modelo procura a ferramenta, não antes.
- **Copilot CLI sem a opção:** o servidor manda as instruções, e elas aparecem no evento
  `session.mcp_servers_loaded` da saída (`serverMetadata.instructions`). Mas o Copilot não as põe no prompt, e o
  modelo diz que não recebeu. Bate com a ajuda da 1.0.98: "Include initialization instructions from all MCP servers
  in the system prompt instead of only allowlisted servers". Com a opção, chegam. A descrição das ferramentas chega
  nos dois casos.
- **Codex:** nenhum pedido chegou à captura, e o Codex deu "failed to refresh available models: request timed out".
  Era erro do teste: o repasse roda no processo do teste, e o `spawnSync` do Codex parava esse processo. Ninguém
  atendia o pedido. Conserto (bfd1af3): o Codex roda por `spawn` sem travar o processo. Os outros harnesses não
  passam pelo repasse e seguem com `spawnSync`. O erro mostra também que o Codex respeitou o provedor próprio: ele
  foi ao repasse, não direto ao ChatGPT.
- **Hashes das pastas reais:** as quatro configurações não mudaram. O `.claude.json` mudou, mas é só registrado: as
  sessões de verdade abertas na máquina o regravam, como no 12. As quatro pastas de ensaio foram apagadas.

### Rodada 2: só o Codex

**PENDENTE: o Codex está sem cota até 12h15** (maestro, 2026-10-17 ~07h50). O conserto do teste está em bfd1af3, e a
rodada está na fila para depois de 12h15:
`pwsh -NoProfile -File etapas/logs/11-corredor.ps1 -Rodadas codex`, com a trava. Os dois critérios do Codex (a
citação e a captura) ficam abertos até lá; o resto do ticket está fechado com Claude Code e Copilot.

### Sem harness

- `node --test agents/code/test/11-mcp-banco.test.mjs`, com `HUB_MCP_BANCO_DIR` = a worktree do fork do 11: **4/4**.
- Com o padrão (`C:\Projetos\hub-mcp-banco`, ainda no 09): 3 passam e 1 pulado, a montagem.
- Fases: vermelho primeiro (os módulos não existiam), depois verde.

## Ressalvas para o 25 (decisão do maestro, item 3)

- **"Regra seguida"** (spec, faixa 5): pedir uma regravação inteira e ver se o agente leu o `AGENTS.md` antes. Não
  medida aqui.
- **Banco recriado ou reiniciado no meio da sessão:** se o MCP volta a responder sozinho. Não medido aqui; o fork rodou
  em modo local.
- **O banco cifrado de ponta a ponta com os harnesses:** o 11 usou o modo local. O caminho do CouchDB com cifra foi
  provado no 09 e no 10, pelo MCP direto, não pelos harnesses.

## Uso de harness e login

Rodada 1, 07:28 a 07:36, com a trava; uma sessão por vez, nas condições do aval do Gustavo.

| Rodada | O que foi copiado | Copiado | Apagado |
|---|---|---|---|
| claude | `%USERPROFILE%\.claude\.credentials.json` → `CLAUDE_CONFIG_DIR` de ensaio | ver `evidencia-11/hashes-…json` (`usos`) | idem, `apagado: true` |
| codex | `%USERPROFILE%\.codex\auth.json` → `CODEX_HOME` de ensaio | idem | idem |
| copilot-sem, copilot-com | só `lastLoggedInUser` e `loggedInUsers` de `%USERPROFILE%\.copilot\config.json` (o token fica no cofre do Windows) | idem | idem |

Hashes antes e depois: `evidencia-11/hashes-claude-codex-copilot-sem-copilot-com.json`.

## Skills da máquina fora da evidência (2026-10-17 ~11h15, decisão do maestro 07:58): 4bc2c23 e 4be0679

Ajudante `agents/code/test/ponta-a-ponta/skills-da-maquina.mjs`: troca o nome de cada skill das pastas reais
(`~/.claude/skills`, `~/.agents/skills`, `~/.copilot/skills`) por `SKILL-DA-MAQUINA`, **por estrutura**: as strings das
listas do init do Claude Code e os objetos de `data.skills` do Copilot com `path` numa dessas pastas. A troca no texto
inteiro (a do 24) pegava palavra comum: a skill `research` virava `SKILL-DA-MAQUINA` no contrato do hub ("os blocos
`research/`"). Evidência já gravada limpa a partir do commit anterior: Copilot com a opção, 585 trocas; Claude e Copilot
sem a opção, nenhuma (o Claude rodou com `CLAUDE_CONFIG_DIR` de ensaio; o Copilot sem a opção não manda a lista).
