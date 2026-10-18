# 40: A regra de roteamento das skills no AGENTS.md (para o Copilot)

Type: task
Status: resolved
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
- 2026-10-17 12:41 (Vela): claimed; feito em db6b52c (seção no corpo do AGENTS.md; teste no 19-roteamento; 52/52; cabeça 1.691). Relatório ../etapas/relatorio-40-regra-de-roteamento.md. Revisão pedida ao Fiel.
- 2026-10-17 14:31 (Vela): rodada curta do Fiel PASSA em 535d86b; Rebite avisado. Conflito previsto com o 18 no fim do AGENTS.md (manter as duas seções).
- 2026-10-17 15h22 (integrador, Rebite): juntado em `integracao`, commit 7caed05 (merge `--no-ff` de `ticket-40` 535d86b, o HEAD da rodada curta "passa" do Fiel; arquivos do 40 iguais aos do ramo). Testes: suíte `node --test --test-concurrency=1 "agents/code/test/**/*.test.mjs"` sem variáveis (e sem `HUB_MODELO_CODEX`), com a trava, em 98a7ced (41, 40, 43 e três junções dos docs do Lume): 289, 278 verdes, 10 pulados, 1 falha, `git status` limpo (log `etapas/juncao-docs-suite-falha-27.log`). A falha é do `27-pastas.test.mjs:247` pelo conteúdo de uma página dos docs (`agents/code/docs/componentes/mcp-do-banco.md:105`, o exemplo `[Open in Obsidian](...)` lido como link); não toca este ticket. Decisão do maestro (15h20): resolver; a docs fica pendente; a causa no verificador vira o ticket 44 (Brasa). Ressalvas do parecer: a 1 (todos os gatilhos) feita na rodada curta; a 2 segue: conflito previsto com o 18 no fim do `AGENTS.md` (as duas seções ficam, Retomada e depois Roteamento de skills; quem resolve é o 18, no ramo, e confere a cabeça). **Resolvido.**
