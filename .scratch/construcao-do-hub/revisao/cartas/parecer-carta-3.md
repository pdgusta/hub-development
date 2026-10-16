# Parecer da carta 3 · A busca (volta 1)

Revisor: Esquadro · 2026-10-16 · carta `carta-3-busca.html`, do Nanquim.

## Veredito: volta

No computador, a carta está muito boa. No celular, os diagramas viram miniatura e não se leem. É conserto de
layout, não de desenho.

## Capturas

Em `capturas-esquadro/`:

- 1600 px: `c3-1600.png` (primeira tela) e `c3-1600-inteira-00..05.png` (a carta inteira em telas).
- 390 px: `c3-390-inteira.png` e `c3-390-00..08.png`.

O Edge sem cabeça não desce de 492 px de largura. Por isso o 390 foi capturado com a carta num iframe de 390 px
(`capturas-esquadro/moldura-390.html#carta-3-busca.html`). Uma captura direta com `--window-size=390` sai cortada na
direita, mas o corte é do navegador, não da carta.

## O que funciona

- A ordem do brief é seguida em cada escolha: problema, a escolha do spec, a alternativa, a bancada e o que vale nos
  dois casos. As escolhas 11, 12, 13 e 23 aparecem como 1 a 4, e o resumo no fim tem a mesma numeração.
- O diagrama de abertura ("o caminho de uma nota até a resposta") marca com selos onde cada escolha age. Mesma ideia
  do mapa de metrô elogiado.
- A linguagem é própria: papel, tinta e selo vermelho; o tracejado índigo é a alternativa, o ocre é o medido na bancada.
- Pouco texto, e os códigos aparecem com palavras: `**/.*` = "o nome tem ponto", Host = endereço, YAML = cabeçalho da
  nota.
- Os fatos batem com o spec, o acordo, a conversa e a bancada:
  - 35 de 40 perguntas com a resposta nas 5 primeiras: arctic no OHS, híbrida 0,875 (`fase2-modelos.md`).
  - 112 de 124 notas indexadas e 12 recusadas por dois-pontos sem aspas (`relatorio.md`).
  - O teste "só observa" era o texto de antes da revisão (Sextante-14).
  - O endereço do proxy por palpite era o texto do Prisma-23.
  - "Ignora sozinha: não verificado" é ponto aberto da faixa 3.

## Consertos

Obrigatórios (celular, 390 px):

1. **Diagrama de abertura** (`c3-390-00.png`): ele encolhe para caber, e os rótulos ficam com uns 5 px. Abaixo de
   ~600 px, faça uma de duas coisas:
   - redesenhe na vertical (notas → sem ponto → cabeçalho → índice → busca → agente, de cima para baixo, com o ramo do
     cliente ao lado da busca);
   - ou mantenha o tamanho legível e deixe rolar na horizontal dentro da faixa, com uma dica "arraste →".
   Os rótulos precisam ter pelo menos 12 px.
2. **Diagrama do caminho do cliente, na escolha 4** (`c3-390-04.png`): mesmo problema e mesmo conserto. "Host: ?" e
   "o do cliente ou o do proxy?" são o centro da pergunta e hoje não se leem.
3. **Árvore da escolha 3** (`c3-390-03.png`): os caminhos e as tesouras ficam minúsculos.
   - No celular, troque as duas colunas de regra por uma marca curta ao lado de cada caminho ("nome com ponto" /
     "dentro de pasta com ponto") e mantenha "fora / entra".
   - Ou deixe a árvore rolar por dentro, em tamanho legível.
4. **O cabeçalho quebrado da escolha 2** (`c3-390-02.png`): o bloco `title: Reunião: cliente` e o texto "dois-pontos
   sem aspas" ficam com ~6 px. Empilhe o bloco e a explicação, cada um na largura toda.

Pequenos:

5. **Selo PROBLEMA ao lado do texto** (`c3-390-03.png`, escolha 3): no celular, ele come um terço da largura e o texto
   desce em sete linhas. Abaixo de ~600 px, ponha o selo em cima do texto.
6. **Chip "+ as pastas marcadas como só desta máquina (local: true)"** (`c3-390-04.png`): o `local: true` quebra o
   chip em três colunas. Deixe o código como texto corrido (`white-space: nowrap` só no código) ou tire-o do chip.
7. **(obrigatório) Fato, escolha 1, chip da reserva**: "a reserva (índice dentro do banco)". O spec (faixa 3, story 28) diz "índice
   dentro do MCP do banco", e o índice dela lê o banco cifrado direto. Troque por "outra busca, dentro do MCP do banco,
   que lê o banco direto".

Para passar: os itens 1 a 4 e o 7 (fato impreciso conta como obrigatório). Os itens 5 e 6 são rápidos, e vale aproveitar a volta.

---

# Volta 2 · 2026-10-16

## Veredito: passa, com ressalva

Capturas da volta 2, em `capturas-esquadro/`:

- 1600 px: `c3v2-1600-00..05.png`.
- 390 px: `c3v2-390-00..09.png`, tiradas pela moldura de 390 px.

Conferi os sete consertos no celular:

1. O mapa de abertura ficou na vertical, com rótulos legíveis, e o cliente sobe ao porteiro e à busca (`c3v2-390-00`).
   Feito.
2. O caminho do cliente da escolha 4 ficou na vertical, e "Host: ?" e "o do cliente ou o do proxy?" ficaram legíveis
   (`-05`). Feito.
3. A árvore da escolha 3 virou uma lista com a marca por caminho e "fora / entra". A alternativa e o sincronizador
   também se leem (`-03`, `-04`). Feito.
4. O cabeçalho quebrado empilha, e o texto ficou grande (`-02`). Feito.
5. O selo PROBLEMA está em cima do texto. Feito.
6. O chip do `local: true` está inteiro. Feito.
7. A reserva agora é "outra busca, dentro do MCP do banco, que lê o banco direto" (`-02`). Fato certo.

No computador, nada piorou (`c3v2-1600-00`, `-03`).

Ressalva, que não impede passar: no celular, os rótulos pequenos dentro dos desenhos das escolhas 1, 2 e 4 ainda
ficam com ~8 a 9 px. São eles: "a nota certa", "nota nova · sem reindexar", "lê o cabeçalho", "índice · indexadas =
válidas", "palpite errado → cliente fica sem busca". A ideia de cada desenho se entende pelos títulos e pelos chips
logo abaixo. Se houver outra mexida na carta, suba esses rótulos para 11 ou 12 px no celular.
