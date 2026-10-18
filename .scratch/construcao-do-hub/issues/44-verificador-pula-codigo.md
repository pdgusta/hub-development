# 44: O verificador de pastas não lê link dentro de código

Type: task
Status: resolved
Etapa: conserto do 27 (fora da sequência)
Blocked by: 27

**What to build:** Na suíte de 41+40+43+docs (Rebite, 98a7ced), o `27-pastas.test.mjs:247` ("onde o catálogo diz tipo
null não nasce cartão") caiu porque a página `agents/code/docs/componentes/mcp-do-banco.md:105` traz, em código inline
numa tabela, o exemplo `[Open in Obsidian](...)`, e o verificador de pastas o leu como link de verdade ("precisa virar
`par://`, falta `HUB_PAR_ID`"). Link dentro de código (inline ou bloco cercado) é texto, não link: o verificador passa a
pulá-lo. O Lume troca a página na hora para destravar; este ticket conserta a causa.

**Fonte:** Rebite, log `../etapas/juncao-docs-suite-falha-27.log`.

**Blocked by:** 27 (resolvido)

- [x] link em código inline e em bloco cercado não é lido pelo verificador de pastas (teste)
- [x] link Markdown relativo com `../` resolve a partir da pasta da nota (hoje `alvoNoHub` lê da raiz do hub e `naoReplica` toma o `..` por parte com ponto: vira "não replica" sem `HUB_PAR_ID` e `par://` errado com ela) (teste)
- [x] link de verdade segue lido como antes
- [ ] a suíte segue verde

## Comments

- 2026-10-17 15h20 (maestro, mandato): publicado. Dona: a Brasa (livre até a vez do Codex do 22). Pequeno; revisão curta do Fiel.
- 2026-10-17 15h25 (maestro): acrescido o link relativo com `../` (divergência do Lume, anotada em `agents/code/docs/componentes/pastas-e-links.md`).
- 2026-10-17 16h00 (Brasa): feito no ramo `ticket-44` (worktree `C:/context-hub-wt/ticket-44`, com integracao a7d1517). Código em linha fica de fora por marcador (link com código no rótulo segue lido); link Markdown com `./`/`../` lido da pasta da nota (`corrigirLinks` recebe `nota`); doc `pastas-e-links.md` atualizada (§7 sem a divergência e sem a ressalva 2 do 33). Dois testes "44:" no `27-pastas` (vermelho→verde); 27-pastas + 27-fim-da-resposta 39/39. Relatório `etapas/relatorio-44-verificador-pula-codigo.md`. Revisão curta pedida ao Fiel.
- 2026-10-17 ~16h15 (Brasa): r1 do Fiel VOLTA por 1 conserto (wikilink com ../ derrubava o verificador); feito em a63cbb7, com teste; 40/40. Rodada 2 pedida.
- 2026-10-17 ~16h25 (Brasa): r2 PASSA (Fiel). integracao 9f122c2 juntada (2609f21); 27-pastas + 27-fim-da-resposta 43/43. Levado ao Rebite.
- 2026-10-17 17h14 (integrador, Rebite): juntado em `integracao`, commit df6c2e5 (merge `--no-ff` de `ticket-44` 2609f21; o Fiel deu "passa" em acordo em a63cbb7, e depois só entrou o merge de `integracao` 9f122c2, sem resolução manual). Testes: `27-pastas` + `27-fim-da-resposta` 43/43 (log `etapas/logs/juncao-44-docs5-leves.log`); suíte `node --test --test-concurrency=1 "agents/code/test/**/*.test.mjs"` sem variáveis, com a trava, junto com a 5ª leva dos docs (f640bbd): 358, 345 verdes, 13 pulados, 0 falhas, `git status` limpo (log `etapas/logs/juncao-44-docs5-suite.log`). Conserta a causa da falha do 27-pastas de 15h18 (link de exemplo dentro de código). Ressalvas do parecer (r1): o marcador U+E000 e a crase escapada; wikilink com `../` lido da raiz. **Resolvido.**
