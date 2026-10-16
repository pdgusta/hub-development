# Parecer do Tech lead, porta da amostra, volta 1

2026-10-15. Peça: `amostra/amostra.html`, com `amostra.md` e `decisoes.md`. Fonte: `descricao/descricao-do-hub.md`
(v3.2). Base: a mistura aprovada pelo Gustavo (`conceitos/mistura/mistura.html`, portas `mistura-1` e `mistura-2`).
Julgo R4, R5 e R6 e o que a mistura tinha e a amostra precisa manter.

Evidência usada:
- captura do QA a 1280 px (`qa/amostra-1/captura-1280.png`) e o relatório (`qa/amostra-1/relatorio.md`);
- comparação, por programa, dos dados da amostra com os da mistura aprovada: objeto das fichas (`G`), objeto dos
  cenários (`C`) e a lista de `data-ligacao`;
- o código da camada de detalhe (`amostra.html`, linhas 249 a 265), que diz de onde vêm as 40 etiquetas.

---

## 1. O que a mistura aprovada tinha e a amostra mantém

| O que | Situação | Evidência |
|---|---|---|
| Fichas: componentes, dono, aciona, lê, só vê, aprova, também em, selos | **iguais** | objeto `G` da amostra idêntico ao da mistura final |
| Os sete cenários, passos, frases e o que cada passo acende | **iguais** | objeto `C` idêntico; 39 passos (QA) |
| Ligações | **iguais** | mesma lista de `data-ligacao` nas duas peças |
| Meu conserto pequeno da volta 2 da mistura (o checkpoint cobra o agente, só no cenário) | **mantido** | "agente novo" 6 e "altere" 6 acendem Checkpoint → Agentes; a frase: "o checkpoint cobra o agente e confere a nota; o agente a grava" |
| A marca do passo 5 em "o Gustavo edita" | **corrigida** | QA, seção 4: 5 marcas no passo 5, 6 no passo 6 |
| A planta: bairros, ordem, pontos de encontro, cor de quem aciona, "confere, só lê", tracejado "a decidir", contorno "a construir" | **iguais** | captura 1280; `amostra.md`, item 5 (as fileiras só ficaram mais altas) |
| O Gustavo chega pela vista Markdown; a busca como porta do conteúdo | **iguais** | captura 1280: Gustavo → Obsidian → Vista Markdown; a linha mais grossa é a de buscar |

Nada do que foi aprovado se perdeu.

---

## 2. O que é novo, contra a descrição

**Dois rótulos novos na visão inicial.** "Agendador do Windows" e "Biblioteca do Maestri": são os rótulos da seção 3
(3.1, ator Agendador; 3.1 "Periferia e máquina", rótulo "Biblioteca do Maestri"). Cada um no bairro do grupo principal
de 5.1 (Periferia do par; Ferramentas da máquina). Certo.

**A configuração de cada ferramenta saiu do desenho como ícone e virou etiqueta.** Continua no bairro certo
(Ferramentas da máquina, 5.1) e com a ficha. Certo.

**Camada de detalhe (40 etiquetas a partir de 140%).** O código gera cada etiqueta a partir da ficha do próprio bairro:
o nome é o nome do componente na ficha, que eu já conferi na mistura contra os rótulos da seção 3, e o bairro é o grupo
principal (5.1). Por construção, não há nome inventado nem componente fora do seu grupo. O título de cada etiqueta traz
o papel numa frase, e o clique abre a ficha nela. As etiquetas não têm linha. Não são componentes soltos: são os
membros do bairro, mostrados ao aproximar, e as ligações deles estão na ficha. A régua põe o detalhe nessa camada.

**O que a camada não mostra.** As pessoas não são bairro, então os atores de "Quem chega" que não estão desenhados
(Claude Desktop, Cliente, Recruta, Subagente) não ganham etiqueta. O Desktop usa a busca e o Cliente a porta de leitura
(rodada 8; 3.4; 8.10). Sem o teto de rótulos, dá para mostrá-los ao aproximar. Conserto 1, opcional. Os selos "a
decidir", "a construir" e "não verificado" seguem só na ficha, como na mistura aprovada. Não peço que vão para a
etiqueta: quem decide se isso polui é o UX revisor.

---

## 3. As três regras

- **R4 Nomes: passa.** Evidência: 27 rótulos na visão inicial, os 25 da mistura mais dois rótulos da seção 3; as 40
  etiquetas usam os nomes das fichas, já conferidos.
- **R5 Papel na cidade: passa.** Evidência: o relógio agora diz que é o Agendador do Windows, e as linhas dele vão ao
  sincronizador e à vigia (4.1; 4.2: aciona os dois). O caderno é a biblioteca do Maestri, que o maestro alcança no
  cenário dele (4.5). A linha do Agendador até a vigia passou pela direita do bairro, sem mudar quem liga a quem.
  Nenhum papel mudou.
- **R6 Forma nova: passa.** Evidência: é a forma aprovada pelo Gustavo. O canvas muda a navegação, não a forma. A
  camada ao aproximar leva o detalhe a uma camada e não apaga nada.
- R1, R2, R3: não é do meu papel. (QA: 0 cruzamentos; razão entre grupos 1,53, de novo a 0,03 do limite; na camada
  de detalhe, 10,6 a 12 px entre textos. São do UX revisor.)

| Dimensão | Nota | Por quê |
|---|---|---|
| 4 Nomes | 5 | Nada a consertar. |
| 5 Papel na cidade | 5 | Nada a consertar; o conserto 1 é opcional. |
| 6 Forma nova | 5 | Nada a consertar. |
| 7 a 12 | não é do meu papel | UX revisor. |

**Veredito, nas minhas regras: passa.**

---

## 4. Consertos

Nenhum bloqueia a porta.

1. [Opcional] Camada de detalhe, junto às pessoas: o Claude Desktop e o Cliente não aparecem nem ao aproximar → com o
   teto solto, mostrar os dois como etiquetas perto do Gustavo (o Desktop é o Gustavo pelo app) e dos Agentes (o
   cliente é um agente numa sandbox), abrindo a ficha "Quem chega". Evidência: 5.1, "Quem chega"; 8.9, "Quem usa a
   busca"; 8.10.

Observação para o Prumo, não conserto meu: quando uma etiqueta não acha lugar no bairro, o código a tira sem aviso
visível (só marca `data-sobra` no bairro). Hoje cabem as 40 (QA). Quando um ticket somar um componente à ficha, ele pode
sumir da camada sem ninguém notar. Ajuda se o QA ou o próprio código acusar `data-sobra`.
