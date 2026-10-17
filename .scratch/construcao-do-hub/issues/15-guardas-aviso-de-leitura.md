# 15: Guardas: aviso de leitura fora da busca

Type: task
Status: claimed
Etapa: 5 (guardas no disco)
Blocked by: 14, 12

**What to build:** O aviso, sem recusa, quando o agente lê um arquivo grande sem ter buscado antes: guarda por sessão o que a busca devolveu e o que foi aberto.

**Fonte:** Bloco do Worker 6, item (c); ticket 11, rodadas 3 e 4. Regras comuns: `../etapas/regras-da-construcao.md`.

**Blocked by:** 14 (Guardas: regravação inteira e ficha fora do esquema), 12 (Busca local com aceite)

- [ ] ler arquivo grande sem busca antes dá um aviso, uma vez por arquivo por sessão
- [ ] ler o trecho que a busca apontou não avisa

## Comments
- 2026-10-16 ~23h15 (maestro): passado ao Trilho depois do 12 (juntado c5b946a); bloqueios 14 e 12 resolvidos. Às 01:40 ele pausa para o aceite do Codex do 12.
- 2026-10-16 ~23h25 (Trilho): pego (`claimed`). Worktree `C:/context-hub-wt/ticket-15`, ramo `ticket-15`, de `integracao` c5b946a. Às 01:40 pausa para o Codex do 12.
- 2026-10-16 ~23h25 (maestro): costuras do Trilho aceitas; 'grande' medido no vault antigo (só tamanhos, números agregados no relatório, sem caminho nem nome), como pede a user story 29 da faixa 6.
