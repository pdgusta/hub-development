# Parecer da carta 4 · Ficha, porteiros e acervo (volta 1)

Revisor: Esquadro · 2026-10-16 · carta `carta-4-regras.html`, do Guache.

## Veredito: volta

No computador, a carta está pronta. No celular, a faixa do problema esconde metade da pergunta, e as palavras de
estado dentro dos diagramas ficam pequenas demais. Há também um fato impreciso, de uma linha.

## Capturas

Em `capturas-esquadro/`:

- 1600 px: `c4-1600.png` (primeira tela) e `c4-1600-00..06.png` (a carta inteira em telas).
- 390 px: `c4-390-inteira.png` e `c4-390-00..08.png`.

O Edge sem cabeça não desce de 492 px de largura. Por isso o 390 foi capturado com a carta num iframe de 390 px
(`capturas-esquadro/moldura-390.html#carta-4-regras.html`).

O tema escuro não foi conferido nesta volta.

## O que funciona

- A forma de manual de montagem é própria e não lembra a carta 3: um passo por escolha, e cada passo tem o problema, o
  par "com a escolha × sem ela" e a lista de conferência no fim. As escolhas 14 a 20 aparecem como 1 a 7, e o resumo
  final usa os mesmos números.
- A legenda "Peças" no começo dá nome a cada ícone, e os códigos sempre vêm com palavras: frontmatter = ficha,
  hook = porteiro, junction = atalho, HOME falso = casa de ensaio, `COPILOT_SKILLS_DIRS` = "lista extra de pastas de
  skills".
- Os diagramas carregam a ideia, e o texto fica em rótulos e chips. Hierarquia boa: o número grande, o título, o
  problema, depois o par.
- Os fatos batem com o spec e o acordo, seção (c):
  - o núcleo tem seis arquivos com os nomes certos;
  - revisão depois da sessão e FreeLLMAPI já estão fora por decisão;
  - a marca do Maestri não distingue maestro de recruta;
  - o ensaio por `COPILOT_HOME` prova contrato, MCP e porteiros, mas não as skills;
  - o `initiative` é esclarecimento, e o esquema dá a palavra final;
  - o instante entre reler e gravar não foi medido;
  - a montagem da nota final ainda não foi testada.

## Consertos

Obrigatórios:

1. **Faixa do problema no celular** (`c4-390-01.png`, `-02`, `-04`, `-06`): ela rola por dentro, mas:
   - o selo "O PROBLEMA" sai cortado no alto da faixa (só aparece a borda de baixo);
   - a parte que faz a pergunta fica fora da tela: "A MESMA NOTA" e o verificador no passo 1, o porteiro e "a ficha
     fica longe" no 2, "fora do hub / vale a regra geral?" no 4, os outros arquivos e o mapa no 7;
   - não há sinal de que a faixa rola.
   Abaixo de ~600 px, empilhe a faixa na vertical, que é o melhor: cada ator embaixo do anterior e a pergunta por
   último, inteira. Se mantiver a rolagem, mostre o selo inteiro, ponha "arraste →" e uma sombra na borda direita.
2. **Palavras de estado dentro dos diagramas, no celular**: "fica inteira", "refaz ou devolve ao agente", "pede o aval ·
   estante protegida", "grava sem aval · estante aberta", "recusada, ou com valor inventado", "toda iniciativa nasce com
   o seu mapa" e "o mesmo vale para o que o sincronizador acabou de trazer" ficam com ~6 a 8 px (`c4-390-01`, `-02`,
   `-04`, `-06`). São elas que dizem o resultado. Abaixo de ~600 px, leve esses rótulos para fora do SVG, em HTML de
   12 px ou mais, ou aumente o desenho e empilhe as linhas.
3. **Fato, passo 1, chip "só campos do caminho ou da data"**: o título do núcleo vem da ficha, não do caminho (spec,
   faixa 1: "`title` do núcleo pela ficha"). Troque por "só campos do caminho, da ficha ou da data", ou "só o que dá
   para deduzir".

Pequenos:

4. **Passo 4, "pede o aval"**: é assim no Claude Code. No Codex e no Copilot, a guarda recusa e aponta a pasta de
   propostas (faixa 9). Se couber, ponha "pede o aval (ou recusa e aponta as propostas)", ou uma nota curta.
5. **Rótulo "repetido" no passo 4**: "o lembrete também chega aos recrutas" fica solto, fora da caixa "em aberto", e
   repete a mesma ideia. Junte os dois numa linha só.

Para passar: os itens 1 a 3. Os itens 4 e 5 ficam a seu critério.

---

# Volta 2 · 2026-10-16

## Veredito: passa, com ressalva

Capturas da volta 2, em `capturas-esquadro/`:

- 1600 px: `c4v2-1600-00..07.png`.
- 390 px: `c4v2-390-00..10.png`, tiradas pela moldura de 390 px.

Conferi os cinco consertos:

1. No celular, a faixa do problema virou uma pilha: ícone e frase, de cima para baixo, e a pergunta por último num
   fundo amarelo. O selo aparece inteiro e não há mais rolagem (`c4v2-390-01`, `-02`, `-05`, `-08`). Feito, e a
   leitura ficou melhor que no computador.
2. As palavras de estado saíram dos desenhos para uma linha de leitura em HTML: "fica inteira", "refaz ou devolve ao
   agente", "chega", "pede o aval", "não chega", "sem aval", "só quando houver regra própria". Feito.
3. O chip agora diz "só campos do caminho, da ficha ou da data", no celular e no computador. Fato certo.
4. O chip "aval no Claude Code; Codex e Copilot recusam e apontam a pasta de propostas" entrou no passo 4. Feito.
5. "O lembrete também chega aos recrutas" entrou na caixa "em aberto". Feito.

No computador, nada piorou (`c4v2-1600-01`, `-03`).

Ressalva, que não impede passar: no celular, no passo 1, sob os três quadros "lê / relê / só a ficha", ficaram o
bonequinho do Gustavo e o ✗ sem rótulo (`c4v2-390-01`). A linha de leitura logo abaixo já explica o resultado. Se
houver outra mexida na carta, esconda esses dois ícones no celular. O tema escuro não foi conferido.
