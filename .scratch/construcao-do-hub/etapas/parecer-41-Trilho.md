# Parecer do ticket 41 (Trilho): a busca não indexa `agents/code/`

## Rodada 1 — 2026-10-17 ~14h35 (Fiel; Fielzinho voltou e lê depois)

Ramo `ticket-41`, 8497eb7 (ae102ed + merge da integracao com 38 e 39, limpo). **Veredito: VOLTA** por 1 conserto curto.

O que confere:
- Gerador (`gerar-exclusoes.mjs:21,57`): `agents/code/**` só na lista da busca; sincronizador e git iguais.
- O OHS 0.16.2 tira do índice o que passa a ser ignorado (`indexer.js:298`, `getPathsToRemoveForIgnoreChange`): um hub
  com índice antigo perde as páginas de `agents/code/` na partida seguinte, sem reindexar à mão.
- `relatorio.mjs` usa os `ignore_patterns` do status do servidor: não conta `agents/code/` como faltando.
- Hook de leitura (`leitura.mjs:14,117`): `relativoAoHub` devolve `/`; a página grande de `agents/code/` passa sem aviso.
- Fiel: 15-leitura, gerador, 16-vigia, 17-vigia-tela e o detector do 29 (`harness-real.test.mjs`): **64/64** em
  8497eb7; `git status` limpo.
- 12-busca com os docs juntados (log `logs/trilho-41-12-busca-com-docs.log`): 9/9, 50 notas, pronta em 50 s,
  indexação 38 s. Não repeti (trava do Rebite na suíte); a junção dos docs roda de novo.

Conserto:
1. (Fiel) `agents/skills/busca/SKILL.md:27-28`, "Fica fora da busca, de propósito", não cita `agents/code/`. A SKILL
   diz que a busca é a porta; um agente que busque o código ou os docs técnicos não acha nada e não sabe que é por
   regra. Acrescentar: `agents/code/` (motor e documentação técnica) fica fora; leia pelo caminho. O 12 já mostra que
   quem mexe num `SKILL.md` roda o `12-busca` (YAML): aqui o cabeçalho não muda, basta o leve.

Ressalva (não pede conserto):
- O hook de leitura ainda manda "busque antes" para página grande com ponto no caminho ou em pasta `local: true`, que a
  busca também nunca aponta. Anterior ao 41.

## Rodada 2 (curta) — 2026-10-17 ~14h45 (Fiel; leitura do Fielzinho pendente)

Ponta 6a728a4: só `agents/skills/busca/SKILL.md`, corpo (linhas 25-27); cabeçalho YAML igual. Conserto 1 feito.
**Veredito: PASSA.** O 12-busca desta ponta fica para a junção do Rebite (maestro); com os docs deu 9/9 em ae102ed.
Acordo (14h55): Fielzinho leu sozinho (parecer-41-Trilho-fielzinho.md, 18/18), PASSA r2 sem achado novo; aceita a ressalva. **PASSA em acordo.**
