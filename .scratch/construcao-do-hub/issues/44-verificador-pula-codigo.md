# 44: O verificador de pastas não lê link dentro de código

Type: task
Status: claimed
Etapa: conserto do 27 (fora da sequência)
Blocked by: 27

**What to build:** Na suíte de 41+40+43+docs (Rebite, 98a7ced), o `27-pastas.test.mjs:247` ("onde o catálogo diz tipo
null não nasce cartão") caiu porque a página `agents/code/docs/componentes/mcp-do-banco.md:105` traz, em código inline
numa tabela, o exemplo `[Open in Obsidian](...)`, e o verificador de pastas o leu como link de verdade ("precisa virar
`par://`, falta `HUB_PAR_ID`"). Link dentro de código (inline ou bloco cercado) é texto, não link: o verificador passa a
pulá-lo. O Lume troca a página na hora para destravar; este ticket conserta a causa.

**Fonte:** Rebite, log `../etapas/juncao-docs-suite-falha-27.log`.

**Blocked by:** 27 (resolvido)

- [ ] link em código inline e em bloco cercado não é lido pelo verificador de pastas (teste)
- [ ] link de verdade segue lido como antes
- [ ] a suíte segue verde

## Comments

- 2026-10-17 15h20 (maestro, mandato): publicado. Dona: a Brasa (livre até a vez do Codex do 22). Pequeno; revisão curta do Fiel.
