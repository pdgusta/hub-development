# Brief da volta 1: conceitos de cidade

Do maestro ao UI engineer, 2026-10-15. Fase 3 do `orquestracao.md`, etapa 8.

## O pedido

Três conceitos de direção visual para a "cidade", o diagrama de system design do context hub. Têm de ser **formas
realmente diferentes**: cada uma muda o que o leitor faz ou como lê, não só cor, fonte e arredondamento (regra R6).
Amostra, não a peça inteira: o bastante para mostrar a direção, estática, com a régua aplicada.

## Conteúdo

- Só do `texto-do-hub.md`. Componentes e rótulos da seção 3 (use a coluna "rótulo"), agrupamentos da 3.5 (os sete),
  ligações da seção 4. Gente e agentes ficam fora dos grupos, chegando pelas portas.
- A camada de busca é a porta do conteúdo (princípio da seção 2): o desenho deixa isso visível.
- Itens da seção 7 que aparecerem vão marcados "a decidir".
- Na visão geral, no máximo 25 rótulos visíveis (R2); o detalhe fica numa camada que se abre.
- Partes do hub são "componentes", nunca "peças" (aviso do texto do hub).

## Antes de construir

1. Leia `regua-da-cidade` inteira: `regras.md`, `como-julgar.md` e as imagens de `referencias/` com o `LEIA.md`.
   Elogiados: o mapa de metrô (diagrama no centro, texto só em rótulos), a maré (uma metáfora que carrega a pergunta,
   pouco texto), a Mesa de mapas (leitura confortável). Recusados: o laudo (texto demais), a cidade radial v2
   ("poluído, precisa de distância"), a trilha até o cume (triângulos soltos sem sentido).
2. Nenhum conceito pode ser a cidade radial com outra roupa.

## Entrega, em `conceitos/volta-1/`

- `conceito-a.html`, `conceito-b.html`, `conceito-c.html`: HTML único cada, CSS e SVG embutidos, sem CDN nem rede.
  Legível em 1280 px (visão geral) e utilizável em 320 px.
- Marcação obrigatória: `data-item`, `data-grupo`, `data-ligacao` ("De → Para"), `data-encontro` (ver `regras.md`,
  "Marcação na peça"). O QA mede por ela.
- `conceito-a.md` etc.: a ideia em uma frase, a tabela de R5 (item, papel no hub, equivalente na cidade) e o que
  muda na leitura em relação aos outros dois e às formas recusadas.
- `index.html`: seletor entre os três (um por vez, ou lado a lado), mesma fidelidade nos três, sem marcar favorito.
- `decisoes.md`: o que você decidiu sozinho onde caberia pergunta.

Depois, a porta: o QA mede, o UX revisor e o Tech lead julgam. Se reprovarem, você recebe a lista de consertos.
