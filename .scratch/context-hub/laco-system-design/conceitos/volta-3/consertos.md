# Consertos da volta 3

Uma linha por conserto dos pareceres da porta da volta 2 (`portas/volta-2/ux-revisor.md` e `portas/volta-2/tech-lead.md`).

Conferência própria (a oficial é do QA e do UX revisor):
- `medidas-da-peca` numa pasta minha, a 320 e a 1280 px: 25 rótulos em cada desenho (nenhum somado), 0 cruzamentos,
  nenhum par abaixo de 1 altura de rótulo, contraste sem falha, sem rolagem lateral. Razão entre grupos a 1280: A 1,96;
  B 2,23; C 1,69.
- Tab real (tecla mandada pelo protocolo de depuração do Edge, perfil próprio): as 10 paradas de cada conceito casam
  `:focus-visible`. Nos 7 bairros, o contorno fica escuro e com 3,5 px; nas 3 pessoas, aparece o anel escuro com fundo
  amarelo. 30 de 30.

## UX revisor

### Comum aos três

| Conserto | Situação |
|---|---|
| 1. [Affordance] Foco e passar o mouse invisíveis nas pessoas | feito: ao focar ou passar o mouse, um retângulo arredondado de traço escuro (2,5 px) com fundo amarelo-claro envolve a figura. Conferido com Tab real nas 9 pessoas (3 por conceito). |

### Conceito A

| Conserto | Situação |
|---|---|
| 2. [Hierarquia] Nome de Portas do par na base | feito: o nome voltou ao topo, à esquerda; buscar entra pela borda de cima, à direita dele, e o nome "buscar" passou para cima da linha. |
| 3. [Composição] Vigia na ponta de uma caixa larga | feito: o bairro Vigilância foi estreitado até a estação (de 280 para 165 unidades). |
| 4. [Composição] Metade de baixo do Conteúdo vazia | feito em parte: as duas estações desceram 15 unidades, para mais perto do meio. Mais que isso desalinharia a linha do Checkpoint, que vem reta do bairro ao lado. |

### Conceito B

| Conserto | Situação |
|---|---|
| 2. [Linhas] Verde e vinho descendo lado a lado da base do Banco local | feito: a troca sai pelo lado direito do Banco local, desce entre o Núcleo e a Vigilância até a rua. A vigiar passou a entrar por cima. |
| 3. [Hierarquia] Rede privada como um toco | feito: a estrada vai de muralha a muralha, da saída do par A até a miniatura do Par B, na altura da rua, com o nome embaixo. |
| 4. [Densidade] Raiz e Obsidian com a mesma serra | feito: a Raiz são seis casinhas encostadas, de alturas diferentes, cada uma com o seu telhado; a serra saiu também do Obsidian (ver Tech lead, 1). |
| 5. [Vista de cima] Miniatura do Par B em cinza | feito: os quarteirões da miniatura têm as cores dos bairros do par A, a 30%. |
| 6. [Respiro] Fora do par a 10 px da muralha | feito: 30 unidades entre a muralha e a caixa de Fora do par. |
| 7. [Tipografia] ⊕ à direita em Periferia e Fora do par | feito: o sinal fica sempre antes do nome, à esquerda, nos sete bairros dos três conceitos. |
| 8. [Densidade] Vigilância como seta para cima | feito: uma torre de vigia, com haste, guarita com janela e telhado; o nome "Vigia do sync" fica em cima. |

### Conceito C

| Conserto | Situação |
|---|---|
| 2. [Composição e Densidade] Maestro e Checkpoint atravessam andares | feito: o Checkpoint desce por um poço de serviço à direita do prédio; o Maestro chega pela rua e desce pela lateral esquerda. Nenhum traço passa por andar onde não para, e o rótulo "Porta do banco" ficou livre. |
| 3. [Hierarquia] Buscar termina no térreo, longe do Conteúdo | feito: um poço tracejado, claro, desce da porta da busca até a laje do Conteúdo, sem rótulo e sem `data-ligacao` (igual ao Tech lead, 1). |
| 4. [Composição] Subtítulo em três linhas | feito: "Vista de lado: quanto mais fundo, mais perto da verdade. O conteúdo mora no subsolo, junto do cofre." Duas linhas a 1280. |

## Tech lead

### Conceito B

| Conserto | Situação |
|---|---|
| 1. [R5] Obsidian com telhado em serra, lê como fábrica | feito: oficina pequena de telhado de duas águas, com porta e janela. |
| 2. [R5] Raiz como barra serrilhada | feito: seis casinhas encostadas numa fileira, cada uma com o próprio telhado, sem rótulo novo. |

### Conceito C

| Conserto | Situação |
|---|---|
| 1. [R5] Nada liga a busca ao Conteúdo | feito: poço tracejado no mesmo amarelo do "a decidir", do piso da busca até a laje do Conteúdo; forma, não ligação. As duas moradas em teste seguem na ficha. |
| 2. [R5] Maestro fura dois andares | feito pela segunda saída do parecer: chega pela rua (à esquerda, ao lado dos agentes) e desce pela lateral do prédio até o primeiro subsolo. Um acesso próprio na faixa das portas cruzaria a linha da Porta do banco (`decisoes.md`, item 27). |

## O que mudou além da lista

- No C, para o poço de serviço do Checkpoint não cruzar a linha da vigia, a torre passou para a rua, entre o prédio e
  a oficina; a oficina ficou mais estreita para o Gustavo ter respiro (`decisoes.md`, item 28).
- No C, o Acervo do maestro foi para a ponta esquerda do Conteúdo, com o nome em cima, para a linha do Maestro chegar
  pela lateral sem cruzar nada.
