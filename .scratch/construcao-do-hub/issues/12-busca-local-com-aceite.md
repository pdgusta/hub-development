# 12: Busca local com aceite

Type: task
Status: ready-for-agent
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
