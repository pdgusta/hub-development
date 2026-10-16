# Brief do Designer: a carta da direção visual da cidade

Do maestro, 2026-10-15. Ticket 56 (laço do system design), fase 3, etapa 10 do `orquestracao.md`: a única parada do
Gustavo antes de construir. Ele escolhe uma direção, pede mistura ou recusa todas.

## O que existe

- Três conceitos que passaram na porta (QA, UX revisor e Tech lead), em
  `.scratch/context-hub/laco-system-design/conceitos/final/`: `conceito-a.html` (Linhas do hub, metrô),
  `conceito-b.html` (Duas cidades e a estrada), `conceito-c.html` (A cidade em corte), cada um com seu `.md` (a ideia em
  uma frase e a tabela de papel na cidade). O UI engineer está fazendo um acabamento pequeno neles agora, nos próprios
  arquivos; a carta os carrega como estão.
- O parecer da porta: `portas/volta-3/resultado.md` (resumo) e os pareceres em `portas/volta-1|2|3/`.

## A carta

- Arquivo: `.scratch/context-hub/laco-system-design/conceitos/final/carta.html` (na mesma pasta, para carregar os
  conceitos pelo leitor de cartas; só `.html`, `.js`, `.css`, `.svg`, `.png` etc. são servidos, `.md` não).
- Diagrama no centro: os três conceitos são o conteúdo; a carta mostra cada um grande (um por vez com seletor, ou lado
  a lado em miniatura que abre), com a mesma fidelidade e **sem marcar favorito**.
- Por conceito, pouco texto: a ideia em uma frase, como se lê (seguir linhas, procurar lugares, ler pela altura) e
  "onde é melhor", nas palavras dos juízes (resultado.md). Nada de laudo: notas por dimensão ficam fora; quem quiser
  abre os pareceres.
- Uma linha no topo dizendo que os três passaram em três voltas de porta e o que vem depois (a amostra da direção
  escolhida, em página à parte, sem tocar o `system-design.html`).
- Leitura confortável, como a Mesa de mapas elogiada.

## Cadastro

Entrada nova no `portal/cartas.json`: `id: "direcao-visual-cidade"`, `titulo` curto, `arquivo` e `pasta`
(`.scratch/context-hub/laco-system-design/conceitos/final`), `ticket: "56"`, `decisao: "em aberto: A, B, C, mistura ou
recusar (rodada do maestro)"`, `situacao: "vigente"`, `mestra: false` e **`"pede_veredito": true`**. Não abra rodada:
a rodada é do maestro e cita a carta pelo id.

## Regras

- Capturas com o Edge sem cabeça: perfil próprio (`--user-data-dir` único); mate só os `msedge` desse perfil, nunca
  `taskkill` por nome.
- Confira a carta no portal (`http://127.0.0.1:8770/`) em 1280 e 320 px.
- Ao terminar: `maestri ask "Claude Code" "pronto: <caminho da carta>"`.
