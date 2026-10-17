# 09: MCP do banco: gravar com versão e conflito à vista

Type: task
Status: ready-for-agent
Etapa: 3 (MCP do banco)
Blocked by: 07

**What to build:** O fork do MCP do banco grava sempre conferindo a versão lida e mostra o conflito ao agente dos dois jeitos aceitos, contra o banco real da etapa 2.

**Fonte:** Bloco do Worker 5; faixa 5 em `spec-partes/faixas-05-06.md`; tickets 25, 30, 11; escolha aceita 1. Regras comuns: `../etapas/regras-da-construcao.md`.

**Blocked by:** 07 (Banco do par: dois CouchDB, LiveSync e vista `.md`)

- [ ] ler e gravar com a versão lida grava, e a leitura seguinte traz a versão nova
- [ ] gravar com versão velha deixa as duas versões no banco e a resposta diz "conflito: releia e refaça"
- [ ] regravar nota existente sem a versão é recusado
- [ ] a leitura de nota em conflito avisa e lista as versões; a ferramenta de conflitos lista os abertos

## Comments

- 2026-10-17 ~02h50 (maestro): reservado para a Vela; começa quando o 07 for resolvido em `integracao`. Até lá, só leitura (ticket, faixa 5 do spec, relatório do 07).
- 2026-10-17 ~03h00 (Vela): só leitura (ticket, faixa 5, Worker 5, relatório do 07, upstream em C:/Projetos/hub-mcp-banco v0.10.0). Esperando o Gustavo (onde mora o fork) e o 07 em integracao.

- 2026-10-17 ~03h00 (maestro): a Vela perguntou onde mora o fork do es617 (o spec deixou a pergunta aberta). Levado ao Gustavo: rodada `2026-10-17-onde-mora-o-fork-do-mcp` (recomendada A, repositório próprio em `C:\Projetos\hub-mcp-banco`). Respondido pelo maestro: banco de ensaio pelo `ensaio.psm1` do 07 (`hub-ensaio-09-*`, 5996); o fork importa o `lib/frontmatter.mjs` do hub por `HUB_ROOT`, sem segundo validador.

- 2026-10-17 ~03h15 (maestro): o 07 foi resolvido; o 09 segue reservado para a Vela, que começa quando o Gustavo responder sobre o fork (até lá ela faz o 28).
