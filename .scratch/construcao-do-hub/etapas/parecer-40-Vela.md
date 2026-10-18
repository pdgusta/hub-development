# Parecer do ticket 40 (Vela): a regra de roteamento no AGENTS.md

## Rodada 1 — 2026-10-17 ~13h55 (Fiel sozinho; Fielzinho sem cota até 17h15, leitura pendente)

Ramo `ticket-40`, db6b52c (de `integracao` e7203b4; merge com a ponta de agora, c42ffa0, limpo). **Veredito: PASSA**
com 2 ressalvas.

- Aceite 1: `## Roteamento de skills` no corpo do `AGENTS.md`, depois de `<!-- cabeca:fim -->`, com o texto do
  relatório do 19 ("Texto da regra no contrato") e uma frase a mais sobre o hook no Claude Code e no Codex.
- Aceite 2: o hub de ensaio copia o `AGENTS.md` da raiz; o teste novo no `19-roteamento` olha o hub montado.
- Aceite 3: cabeça 1.691 de 2.000 (`conferir-cabeca`). Fiel: 19, 04, 21 e o detector: 58/58; `git status` limpo.

Ressalvas:
1. A regra lista os gatilhos ("uma das `palavras` ...; um caminho ...; o nome do papel ...") como se bastasse um;
   o `routing.yml` diz "com mais de um gatilho, todos precisam casar". Um Copilot que leia só o contrato pode indicar
   a skill de uma linha com `palavras` e `papel` só pelas palavras. Trocar por "todos os gatilhos da linha casam".
2. Junção com o 18: `git merge-tree ticket-18 ticket-40` dá CONFLICT em `AGENTS.md` (as duas seções no mesmo ponto),
   como o relatório já diz; manter as duas e conferir a cabeça de novo.

## Rodada curta — 2026-10-17 ~14h50 (Fiel; leitura do Fielzinho pendente)

Ponta 535d86b (e581b96 + 535d86b sobre db6b52c): `AGENTS.md` diz "a linha casa quando todos os gatilhos dela casam",
como o `routing.yml:7`; o `19-roteamento` cobra "todos os gatilhos". Ressalva 1 feita. Fiel: 19-roteamento 20/20;
`git status` limpo. **Veredito: PASSA.** Ressalva 2 (conflito no `AGENTS.md` com o 18) segue para a junção.
Acordo (~15h05): Fielzinho leu sozinho a curta (parecer-40-Vela-fielzinho.md, 20/20, cabeça 1691), PASSA; concorda com a ressalva da junção com o 18. **PASSA em acordo.** Copilot real segue não verificado.
