# Peça 2 — conceito: "O rio estreito" (carta náutica)

Designer: Nanquim. Revisor: Esquadro.

## A metáfora

A construção é um **rio visto de cima, numa carta náutica**, que **desce a página**: o tempo corre de cima
(16/10 ~14h30, `/implement-spec`) para baixo (17/10 21h10, reinício do Windows), **em escala** (1 h = altura fixa).
Vertical de propósito: a peça 1 corre na horizontal; esta se lê rolando, inclusive no celular.

- **Largura do rio = memória livre medida**, em escala (0 a ~4,7 GB). Cada medida vira uma **sondagem** escrita na
  água, como nas cartas ("1,2" GB). Sem medida: margem pontilhada, "sem sondagem".
- **O baixio de 700 MB**: faixa hachurada no meio do leito. Quando o rio fica mais estreito que ela, o barco
  **encalha**: cada queda por memória é um ✕ no ponto exato (Docker do 08, fatia 2, Docker do 22, fases do 25...).
- **A trava = um barco por vez** no canal: barcos na cor do dono (Brasa, Vela, Trilho, Cinzel, Rebite) navegando no
  centro do rio durante o período em que seguraram a trava, com o rótulo do que levavam ("Docker do 16").
- **Janelas quietas**: as margens esvaziam. Os recrutas são pontos na margem (os que estão no canvas); na janela, os
  pontos saem e a faixa ganha o nome "janela quieta" e quem ficou.
- **Codex = um afluente** à direita: água quando tem cota, **leito seco** (areia pontilhada) quando não tem, com a hora
  da volta ("seco até 12h15"). Às 14h26, a **comporta** que o Gustavo abriu (redefinição da cota).
- **Reinícios = barragens** que cruzam a carta: Maestri ~10h05 (todos voltaram sozinhos), Windows 21h10.
- **Margem esquerda: pedras** (os achados que derrubaram algo). Cada pedra fica na hora em que foi achada e se liga
  por um traço à **ponte** (o conserto) na hora em que foi consertada: a distância entre as duas é o tempo do conserto,
  em escala. Rótulo curto ("hífen vira sublinhado no Codex"); o resto no toque.
- **Margem direita: placas** — regras novas do Gustavo (placa cheia) e decisões do maestro pelo mandato (marco
  menor; as "para rever" com um sinal).

## Esqueleto (de cima para baixo)

1. Cabeçalho curto: título em Fraunces e **números grandes** (mínimo de memória livre e a hora; quedas por memória;
   junções desfeitas; janelas quietas; vezes sem cota do Codex). Legenda da carta (rosa dos ventos + 5 símbolos).
2. A carta: o rio inteiro, de cima para baixo. Marcas de hora na lateral.
3. Rodapé: a foz (construção fechada 20h17, suíte 370) e as fontes.

Detalhe em camadas: passar o mouse ou tocar em qualquer pedra, barco, placa, sondagem abre um cartão (no celular, de
baixo). Nada obrigatório: os rótulos curtos já contam a história rolando.

## Visual

Papel de carta (bege claro), água em tinta azul, baixio em ocre hachurado, quedas em vermelho. Fraunces nos títulos
(peso médio, sem contraste extremo), Nunito Sans 16 px no texto, números das sondagens em Nunito Sans itálico.
1600 px: pedras | rio | afluente | placas. 390 px: rio estreito no meio, pedras e placas viram ícones com rótulo
curto dos dois lados; cartão de baixo no toque.

## Dúvidas para o Esquadro

- O dia 16 tem poucas medidas (a memória só vira gargalo de madrugada). Proponho manter a escala inteira e mostrar o
  trecho do dia 16 como rio "sem sondagem" com os poucos eventos (portal fechado 00h24 por RAM; suíte interrompida
  00h35). Alternativa: comprimir o dia 16 com uma quebra visível. Prefiro a escala inteira.
- Horas entre ~03h e ~04h45 no diário foram estimadas (adiantadas ~1 h, diz a linha 27): marco como "~".
