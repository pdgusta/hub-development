# As seis regras da cidade

Cada regra tem enunciado, como verificar e limiar. Os limiares de R1, R2 e R3 foram fixados pelo maestro em
2026-10-15 (`suite.md`, decisão 1) como **primeira calibragem**: o Tech lead e o UX revisor podem propor ajuste
depois dos primeiros conceitos, sempre com o motivo. Os de R4, R5 e R6 são da especificação (`categorias-v2.md`).

"Visão geral" é a cidade inteira na tela de 1280 a 1920 px de largura, sem zoom e sem nada aberto (nenhuma ficha,
nenhum detalhe expandido).

## Marcação na peça

Para a medição não depender de palpite, o UI engineer marca no código:

| Atributo | Onde | Valor |
|---|---|---|
| `data-item` | o elemento de cada item (prédio, praça, estação) | o rótulo do item, igual ao do texto do hub |
| `data-grupo` | o item, ou um elemento que contém os itens do grupo | o nome do agrupamento (texto do hub, 3.5) |
| `data-ligacao` | cada traço de ligação (`path`, `line`, `polyline`) | `De → Para`, com os rótulos do texto do hub |
| `data-encontro` | o elemento que marca um ponto de encontro (baldeação) | o nome do ponto |

Sem marcação, `medidas-da-peca` adivinha itens e ligações pela forma, e o relatório diz que adivinhou.

## R1. Linhas sem se cruzar

- **Enunciado:** nenhuma ligação cruza outra. A única exceção é um ponto de encontro marcado (`data-encontro`),
  desenhado como tal (estação de baldeação), onde as linhas se encontram de propósito.
- **Como verificar:** `medidas-da-peca`, medição `cruzamentos`. Cada par listado como "suspeita" se confere na
  captura: em curvas a amostragem é aproximada.
- **Limiar:** 0 cruzamentos fora de ponto de encontro marcado.
- **Falha típica:** rua que passa por cima de outra para "chegar mais curto"; ligação que atravessa um bairro
  inteiro.

## R2. Vista mais de cima

- **Enunciado:** na visão geral só aparecem as zonas e as ligações principais; o detalhe fica numa camada (ficha ao
  clicar, ao passar o mouse, ao aproximar).
- **Como verificar:**
  1. contar os rótulos visíveis na visão geral (`medidas-da-peca`, medição `rotulos`, contagem por desenho);
  2. teste do olho apertado: reduzir a captura de 1280 px para um quarto da largura e borrar; os agrupamentos
     (texto do hub, 3.5) ainda se distinguem como manchas separadas.
- **Limiar:** no máximo **25 rótulos** visíveis na visão geral; no olho apertado, cada agrupamento se lê como uma
  mancha própria.
- **Falha típica:** a cidade radial v2: 28 itens com rótulo, ruas, anéis e legenda numa tela só.

## R3. Distância entre os itens

- **Enunciado:** cada item tem respiro em volta, e o espaço mostra o que fica junto: dentro do grupo, perto; entre
  grupos, longe.
- **Como verificar:** `medidas-da-peca`, medição `distancias` (menor folga entre vizinhos, altura de rótulo, razão
  entre grupos e dentro do grupo).
- **Limiar:**
  - folga mínima entre itens vizinhos de **1 altura de rótulo** (a altura renderizada do texto dos rótulos);
  - o espaço entre grupos é pelo menos **1,5 vez** o espaço dentro do grupo.
- **Falha típica:** "tá tudo poluído… precisa de distância entre os itens" (Gustavo, cidade radial v2).

## R4. Nomes que dizem o que o item referencia

- **Enunciado:** cada rótulo é o nome do componente no texto do hub (coluna "Rótulo") ou um termo do
  `GLOSSARY.md`. Nada de código interno solto (T2, C3, R18, número de ticket sem o nome) e nada de nome inventado só
  para a metáfora ("Torre Azul" no lugar de "Banco local"). A metáfora vai no desenho, não no nome.
- **Como verificar:** `medidas-da-peca`, medição `rotulos` (lista de todos os textos da peça), conferida linha a
  linha contra o texto do hub, seção 3, pelo Tech lead.
- **Limiar:** 100% dos rótulos de item batem com o texto do hub ou o glossário; 0 códigos internos; os itens da
  seção 7 do texto do hub aparecem marcados "a decidir". O texto do hub avisa: os componentes não se rotulam como
  "peças".

## R5. Uma cidade em que o papel de cada item faz sentido

- **Enunciado:** a função de cada item na cidade corresponde à função dele no hub. Ninguém precisa de legenda para
  entender por que o banco é o cofre, a vigia é a torre de vigia, a rede privada é a estrada.
- **Como verificar:** tabela escrita pelo autor da peça, uma linha por item: item | papel no hub (frase do texto do
  hub) | equivalente na cidade | por que combina. O Tech lead confere contra o texto do hub.
- **Limiar:** todo item da peça está na tabela; nenhum equivalente contradiz o papel no hub (exemplo de
  contradição: o Obsidian como usina, quando ele pode ficar fechado e nada para); os agrupamentos da cidade (bairros)
  seguem os agrupamentos naturais do texto do hub (3.5) ou dizem por que não.

## R6. Reinventar a forma, não restilizar

- **Enunciado:** um conceito novo muda o que o leitor faz ou como ele lê (estrutura, disposição, narrativa,
  interação), não só cor, fonte, ícone e arredondamento. "Manter o conteúdo não é manter a disposição."
- **Como verificar:** o teste do `parallel-concepts`: aplicar ao conceito novo o acabamento do anterior (mesmas
  cores, mesma fonte). Se os dois ficarem iguais, foi restilização. Conferir contra as formas recusadas em
  `referencias/LEIA.md`.
- **Limiar:** o conceito passa no teste e não repete a disposição de nenhuma forma recusada (radial com o banco no
  centro e anéis; seções de texto empilhadas; ícones soltos ligados por setas).

## Regras de comparação entre conceitos

Valem quando há mais de um conceito atrás de um seletor:

- os conceitos têm a mesma fidelidade (nenhum mais acabado que os outros);
- todos usam o conteúdo real do hub (texto do hub), nunca texto de enchimento nem "três linhas";
- nenhum é marcado como favorito na peça; a recomendação, se houver, vai na carta, fora da peça.
