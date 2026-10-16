# Como julgar

Roteiro da nota por dimensão e da lista de consertos. É a porta do laço: o Tech lead e o UX revisor julgam os
conceitos e a amostra por aqui (`orquestracao.md`, etapas 9 e 12).

## 1. Antes de dar nota

1. Olhe as referências (`referencias/LEIA.md`): o que o Gustavo elogiou e o que recusou, e por quê.
2. Tenha em mãos a captura real (1280 px de largura, visão geral) e, se houver, o JSON de `medidas-da-peca`.
3. Tenha aberto o `texto-do-hub.md` (seções 3, 3.5, 4 e 7).

## 2. As seis linhas das regras

Uma linha por regra, no formato do `SKILL.md`:

`R<n> <nome curto>: passa | falha | não verificado. Evidência: <...>. Conserto: <...>.`

Quem julga o quê:

| Regra | UX revisor | Tech lead | QA tester |
|---|---|---|---|
| R1 linhas sem se cruzar | olho, na captura | | número de `cruzamentos` |
| R2 vista mais de cima | olho apertado | | contagem de rótulos |
| R3 distância | olho, na captura | | números de `distancias` |
| R4 nomes | | lista de rótulos x texto do hub | lista de rótulos |
| R5 papel na cidade | | tabela x texto do hub | |
| R6 reinventar a forma | teste de troca de acabamento | idem | |

Quem não julga uma regra escreve "não é do meu papel", não "passa".

## 3. Nota por dimensão

Escala de 1 a 5 para cada dimensão:

- **5:** nada a consertar.
- **4:** consertos pequenos, que não mudam a leitura.
- **3:** lê, mas com esforço; um conserto muda a leitura.
- **2:** falha visível em uma parte importante.
- **1:** a dimensão falha na peça toda.

Dimensões:

| # | Dimensão | De onde vem | Pergunta |
|---|---|---|---|
| 1 | Linhas (R1) | régua | Alguma ligação cruza outra fora de ponto de encontro? |
| 2 | Vista de cima (R2) | régua | Em um relance, só zonas e ligações principais? |
| 3 | Respiro (R3) | régua | Cada item tem folga, e o espaço mostra os grupos? |
| 4 | Nomes (R4) | régua | Cada rótulo diz o que o item é no hub? |
| 5 | Papel na cidade (R5) | régua | O papel de cada item na cidade combina com o do hub? |
| 6 | Forma nova (R6) | régua | É outro desenho, ou o anterior com outra roupa? |
| 7 | Hierarquia visual | `critique-visual-hierarchy` | O olho cai primeiro no que importa? |
| 8 | Composição | `critique-composition` | O peso está equilibrado e a disposição tem lógica? |
| 9 | Densidade | `critique-information-density` | Há coisas demais competindo pelo olhar? |
| 10 | Affordance | `critique-affordance` | Dá para ver o que se clica e o que abre? |
| 11 | Cor | `critique-color` | A cor separa bairros e marca estado sem depender só dela? |
| 12 | Tipografia | `critique-typography` | O texto se lê com conforto (peso, tamanho)? |

Regra de nota: dimensão com regra em "falha" não passa de 2; com regra "não verificado", a nota leva a marca "(sem
evidência)".

**Decidido pelo maestro (2026-10-15):** a peça passa na porta quando R1 a R6 estão em "passa" e nenhuma
dimensão fica abaixo de 3.

## 4. Lista de consertos

Para a volta ao UI engineer e para a carta ao Gustavo. Um conserto por linha, na ordem de prioridade:

`<n>. [R<n> ou dimensão] <onde, na peça> — <o que está> → <o que fazer>. Evidência: <número ou captura>.`

Regras da lista:
- primeiro o que falha nas regras, depois o resto;
- cada conserto diz o que fazer, não só o que está errado;
- simplificar é comunicar a mesma coisa de uma forma melhor, não cortar informação: o conserto leva o detalhe para
  uma camada (ficha, passar o mouse, aproximar), nunca o apaga;
- na carta ao Gustavo, sem códigos internos soltos: escrever "Linhas sem se cruzar (R1)", nunca só "R1".
