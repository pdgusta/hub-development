# 41: A busca não indexa `agents/code/` (código e documentação técnica)

Type: task
Status: claimed
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
