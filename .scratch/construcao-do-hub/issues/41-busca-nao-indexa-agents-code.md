# 41: A busca não indexa `agents/code/` (código e documentação técnica)

Type: task
Status: resolved
Etapa: conserto do 12 (fora da sequência)
Blocked by: 12

**What to build:** A primeira junção da documentação técnica (Lume, `agents/code/docs/`) foi desfeita: o `12-busca`
indexa o repositório e, com as 14 páginas, a indexação passou do prazo de 3 min (67 notas, ~9 min estimados; sem os
docs, 51 s; já vinha subindo de 25 s às 06h). A busca serve às notas do hub; `agents/code/` é motor e documentação para
quem mantém o código, que se lê pelo caminho. Decidido (maestro, mandato): a busca não indexa `agents/code/**` (nem os
docs). O `12-busca` e o kit da busca passam a excluir essa árvore; o teste prova que uma página de `agents/code/docs/`
não entra no índice e que o tempo de indexação do hub de ensaio volta ao de antes.

**Fonte:** Rebite, junção dos docs (log `../etapas/juncao-docs-1-12-busca-falha.log`).

**Blocked by:** 12 (resolvido)

- [ ] `agents/code/**` fora do índice da busca (config do kit e o que o teste usa)
- [ ] com os docs do Lume juntados, o `12-busca` passa dentro do prazo
- [ ] a suíte segue verde

## Comments

- 2026-10-17 12h50 (maestro, mandato): publicado. Dono: o Trilho (fez o 12), antes do 39. A junção dos docs espera este.
- 2026-10-17 ~13h12 (Trilho): ramo ticket-41 (ae102ed). Gerador: agents/code/** na lista da busca; hook de leitura sem aviso para agents/code/. Leves 56/56; 12-busca com os docs juntados (provisório) 9/9, pronta em 50 s. Relatório etapas/relatorio-41-busca-sem-agents-code.md; revisão curta pedida ao Fiel.
- 2026-10-17 ~14h25 (Trilho): merge da integracao (c42ffa0, com 38 e 39) no ramo, limpo; ponta 8497eb7; leves 58/58 (logs/trilho-41-leves-2.log). 12-busca da ponta nova fica para a junção (pesado).
- 2026-10-17 ~14h35 (Trilho): r1 voltou (SKILL.md da busca sem agents/code/); conserto 6a728a4; r2 PASSA no Fiel. 12-busca da ponta fica para a junção (maestro). Levado ao Rebite.
- 2026-10-17 15h22 (integrador, Rebite): juntado em `integracao`, commit e8dde26 (merge `--no-ff` de `ticket-41` 6a728a4, o HEAD da rodada 2 curta "passa" do Fiel). Testes: suíte `node --test --test-concurrency=1 "agents/code/test/**/*.test.mjs"` sem variáveis (e sem `HUB_MODELO_CODEX`), com a trava, em 98a7ced (41, 40, 43 e três junções dos docs do Lume): 289, 278 verdes, 10 pulados, 1 falha, `git status` limpo (log `etapas/juncao-docs-suite-falha-27.log`). A falha é do `27-pastas.test.mjs:247` pelo conteúdo de uma página dos docs (`agents/code/docs/componentes/mcp-do-banco.md:105`, o exemplo `[Open in Obsidian](...)` lido como link); não toca este ticket. Decisão do maestro (15h20): resolver; a docs fica pendente; a causa no verificador vira o ticket 44 (Brasa). O `12-busca` desta ponta, com os docs juntados, passou (busca pronta em 21,8 s; indexação 16 s, contra o tempo esgotado das 12h37). Ressalva do parecer: o hook de leitura ainda manda "busque antes" para página grande com ponto no caminho ou em pasta `local: true` (anterior ao 41). **Resolvido.**
