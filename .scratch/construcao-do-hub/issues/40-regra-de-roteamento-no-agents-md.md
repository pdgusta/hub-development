# 40: A regra de roteamento das skills no AGENTS.md (para o Copilot)

Type: task
Status: claimed
Etapa: conserto do 19 (fora da sequência)
Blocked by: 19

**What to build:** No 19, o Copilot descarta a saída do hook de pedido, e a indicação da skill ficou para o texto do
contrato: o relatório do 19 entrega à faixa 1 a regra de roteamento para entrar no `AGENTS.md` da raiz. Em `integracao`
(e7203b4) o `AGENTS.md` tem só a cabeça e não tem a regra; hoje, no Copilot, nada indica a skill. Pôr o texto da regra no
`AGENTS.md` do hub, no corpo (fora do bloco da cabeça, que está em 1.869 de 2.000 caracteres), e no hub de ensaio.

**Fonte:** divergência achada pelo Lume (2026-10-17 ~12h25); relatório do 19 (`../etapas/relatorio-19-*.md`).

**Blocked by:** 19 (resolvido)

- [ ] o `AGENTS.md` da raiz traz a regra de roteamento do relatório do 19, fora da cabeça
- [ ] o hub de ensaio montado pelo `montar.mjs` traz a mesma regra
- [ ] a cabeça segue dentro dos 2.000 caracteres; a suíte segue verde

## Comments

- 2026-10-17 12h25 (maestro): publicado pela divergência do Lume. Dona: a Vela (fez o 19), enquanto espera o Codex.
