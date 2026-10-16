# 15: Guardas: aviso de leitura fora da busca

Type: task
Status: ready-for-agent
Etapa: 5 (guardas no disco)
Blocked by: 14, 12

**What to build:** O aviso, sem recusa, quando o agente lê um arquivo grande sem ter buscado antes: guarda por sessão o que a busca devolveu e o que foi aberto.

**Fonte:** Bloco do Worker 6, item (c); ticket 11, rodadas 3 e 4. Regras comuns: `../etapas/regras-da-construcao.md`.

**Blocked by:** 14 (Guardas: regravação inteira e ficha fora do esquema), 12 (Busca local com aceite)

- [ ] ler arquivo grande sem busca antes dá um aviso, uma vez por arquivo por sessão
- [ ] ler o trecho que a busca apontou não avisa

## Comments
