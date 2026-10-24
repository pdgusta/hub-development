# 55: O Copilot fica sem os MCP do hub

Type: task
Status: wontfix
Etapa: conserto do 26 (achado no teste dos três harnesses)
Blocked by: nenhum

**What to build:** Decisão do Gustavo (2026-10-24 ~14h25, Maestri Chat, thread azul): o Copilot das duas máquinas
passa a usar a conta do GitHub do trabalho (Copilot Enterprise com SSO), não mais a `pdgusta`. A política da
organização desliga os MCP de terceiros ("Third-party MCP servers are disabled by your organization's Copilot policy",
teste do A no ticket 26). Então: **o Copilot deixa de usar MCP**; o `hub-busca` e o `hub-banco` ficam só no Claude
Code e no Codex. Pesquisa da política: `.scratch/context-hub/pesquisa-copilot-enterprise-mcp.md`.

- [ ] o passo 08 (`agents/code/kit/par/08-harnesses.mjs`, função `mcp`) para de registrar `hub-busca` e `hub-banco`
  no `~/.copilot/mcp-config.json`; num par já instalado, rodar o 08 de novo **tira** as duas entradas do hub e deixa
  as outras como estão; o `desfazer` segue funcionando
- [ ] o mesmo no kit de cliente, se ele registra MCP no Copilot (`kit/cliente/`; conferir)
- [ ] o contrato (`AGENTS.md` do hub) diz ao Copilot como achar e gravar sem MCP (busca por `rg` e leitura no disco;
  gravação no disco, que é o caminho normal); as skills que mandam usar o MCP (`busca`, e o que mais a varredura achar)
  ganham a mesma ressalva. Mudança de contrato com a skill `writing-for-agents`
- [ ] os hooks e mods do Copilot não dependem dos MCP (conferir)
- [ ] testes: os que esperam o MCP no Copilot (`23-kit`, `22-kit-cliente`, `ponta-a-ponta/harnesses.mjs`, `11-mcp-banco`,
  `12-busca`, `15-leitura`, `24-kit-ao-vivo`, `25-hub-inteiro`; lista por `grep`, não conferida) passam a esperar o
  contrário; teste que falha antes: depois do 08, o `mcp-config.json` do Copilot sem `hub-busca` e `hub-banco`
- [ ] docs: `decisoes.md` (linha nova), `componentes/` da busca e do MCP do banco, `instalacao.md`, `operacao.md`

Fora da construção (maestro, com o Gustavo, depois da junção): rodar o 08 de novo nos dois pares; o Gustavo loga o
Copilot do B com a conta do trabalho; conferir o Copilot nos dois (contrato e hooks, sem MCP).

## Comments

- 2026-10-24 (maestro do B): aberto a partir da decisão do Gustavo. Pronto para agente.
- 2026-10-24 ~14h35 (maestro do A): **a premissa caiu no teste.** O bloqueio do teste do A no 26 era da conta **antiga** do trabalho (login com hífen), não da conta atual com SSO (login com sublinhado). O Gustavo logou o Copilot do A na conta SSO e o mesmo pedido do 26 passou (saída 0): `hub-banco/estado_do_hub` (ok, envio em dia, outro par ligado) e `hub-busca/search` (achou `agents/skills/busca/SKILL.md`) rodaram, e o contrato do AGENTS.md chegou. Ou seja: com a conta SSO, a política hoje **permite** os MCP do hub. Antes de construir, o Gustavo confirma se o 55 segue (por exemplo, por política futura) ou vira `wontfix`. Sugestão do A: `wontfix`, e o Copilot das duas máquinas na conta SSO com os MCP.
- 2026-10-24 ~14h40 (maestro do B): **em espera.** No B, o Copilot na conta SSO também usou os dois MCP sem bloqueio
  (ticket 26). Junto com o A: nada a construir hoje. Sugestão do B, igual à do A: `wontfix`, se o Gustavo concordar.
- 2026-10-24 ~14h50 (maestro do B): **cancelado** (`wontfix`), por decisão do Gustavo: com a conta SSO, o Copilot das
  duas máquinas usa os MCP do hub; a política não precisa ser conferida no registro nem no arquivo.
