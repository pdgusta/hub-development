# 12: Busca local com aceite

Type: task
Status: claimed
Etapa: 4 (busca)
Blocked by: 04, 06

**What to build:** A busca local (obsidian-hybrid-search com o modelo local decidido) servindo MCP sobre o hub de ensaio, com as exclusões do gerador, e o teste de aceite.

**Fonte:** Bloco do Worker 3; faixa 3 em `spec-partes/faixas-03-04.md`; tickets 09 e 54; escolhas aceitas 11 (com o ajuste do Gustavo), 12, 13 e 23. Regras comuns: `../etapas/regras-da-construcao.md`.

**Blocked by:** 04 (Esqueleto do hub e hub de ensaio), 06 (Gerador de exclusões)

- [ ] uma pergunta em pt-BR por palavra e uma por paráfrase acham a nota esperada entre as 3 primeiras
- [ ] o tempo até uma nota nova aparecer é medido e gravado, sem limite de aceite
- [ ] nada com ponto nem de pasta `local: true` aparece em resultado
- [ ] o relatório conta as notas indexadas e lista as recusadas por cabeçalho quebrado
- [ ] pedido com endereço estranho é recusado; roda duas vezes seguidas reaproveitando o índice

## Comments
- 2026-10-16 ~21h10 (maestro): passado ao Trilho (antecipação da etapa 4; bloqueios 04 e 06 resolvidos). Primeiro commit do ramo, separado: os testes do 14 apagam as pastas `%TEMP%/hub-ensaio-14-*` no fim (ressalva do Rebite na junção do 14) e as 33 antigas saem.
- 2026-10-16 ~21h15 (maestro): aval para o Trilho instalar o obsidian-hybrid-search 0.16.2 por npm, só local (`.local/busca` do ensaio, versão fixa com lock), nada global; o modelo arctic já estava no cache. Os testes do 04 e 05 também apagam as próprias pastas do TEMP (commit separado neste ramo).
- 2026-10-16 ~21h30 (Trilho): pego (`claimed`). Worktree `C:\context-hub-wt\ticket-12`, ramo `ticket-12`, de `integracao` 8d1d785. Commits separados: 58b9563 (testes do 14 apagam as próprias pastas, mesmo falhando; 33 hub-ensaio-14-* e 86 fora-do-hub-14-*/ponte-14-* antigas apagadas) e 9cb10f4 (o mesmo no 04 e no 05, pedido do maestro; ~1.500 antigas apagadas). Maestro liberou baixar o obsidian-hybrid-search 0.16.2 (npm install local em .local/busca do ensaio, versão fixa com package-lock; registrar o que baixou e o tamanho). O modelo arctic já está em ~/.cache/huggingface/Snowflake (313 MB, não baixa). Falta: teste de aceite (tdd), iniciar.ps1, 03-busca.ps1, relatório, revisão.
- 2026-10-16 ~21h55 (Trilho): aceite em `agents/code/test/12-busca.test.mjs` com 7 verdes (palavra, paráfrase, nota nova com tempo, exclusões, relatório, Host, segunda partida), usando a instalação da bancada por `HUB_BUSCA_OHS`. Skill: `agents/skills/busca/iniciar.ps1` e `relatorio.mjs`. Ramo até d3783c6. Falta: inglês e `.pdf.md`, rajada de 200, kit `03-busca.ps1` com package-lock (download liberado; lock gerado no scratchpad), SKILL.md, relatório, revisão.
- 2026-10-16 ~22h30 (Trilho): HEAD 616a1c0, 13 testes verdes (9 do aceite, 4 do kit). Feito: iniciar.ps1, relatorio.mjs (--consertar), kit 03-busca.ps1 com package-lock. Achados no `etapas/retomada-Trilho.md`. Falta: merge de integracao (d5e4e16), SKILL.md, env/03.env, relatório, revisão.
- 2026-10-16 ~22h15 (maestro): perguntas do Trilho: (1) as linhas de registro do MCP de busca nos três harnesses entram no 12 (spec faixa 3, user story 22: o fragmento de kit as entrega, o 23 só junta), formato nativo lido na doc; (2) o aceite por harness real entra no 12, atrás de `HUB_HARNESS_REAL=1`.
