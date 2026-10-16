# Consertos da volta 2

Uma linha por conserto dos dois pareceres da porta da volta 1 (`portas/volta-1/tech-lead.md` e
`portas/volta-1/ux-revisor.md`). Medi de novo os três com `medidas-da-peca` numa pasta minha, a 320 e a 1280 px: 25
rótulos em cada desenho, 0 cruzamentos, nenhum par abaixo de 1 altura de rótulo, contraste sem falha, sem rolagem
lateral. A medição oficial é do QA.

## Tech lead

### Comuns aos três (Nomes, R4)

| Conserto | Situação |
|---|---|
| 1. Ficha da Porta do banco: selo "como os agentes gravam" | feito: "a decidir: como os agentes gravam: disco, porta do banco ou os dois, e como conferem a versão no disco". O mesmo selo vai também na ligação "Agentes → Porta do banco → Banco local". |
| 2. Ficha da Raiz: selo "árvore abaixo das seis raízes e frontmatter" | feito. Junto, "a decidir: zonas por ciclo de vida" (seção 7, também toca a Raiz). |
| 3. Porta do banco e Porta de leitura: "não verificado: duas instâncias do MCP por par"; ligação do Contrato: "a decidir: como cada ferramenta carrega contrato e MCP" | feito. O selo "não verificado" tem cor própria (cinza-azulado), diferente do "a decidir" (amarelo). Na ligação do Contrato entrou também "a decidir: roteamento de skills". |
| (além da lista) os outros assuntos da seção 7 que tocam itens da peça | feito: Avisos (forma do mod da vigia), Checkpoint (hooks no Codex e no Copilot), Pasta não replicada (perfil por máquina), Obsidian (convivência com o Obsidian do vault), Banco local (arquivos entre 50 e 200 MiB, não verificado), Guarda do acervo (detalhes não verificados, agora por extenso), Camada de busca (as duas moradas em teste e a ferramenta e o modelo). |
| 5. (A), 5. (B), 6. (C) Frase "13 itens com o selo a decidir" nos `.md` | feito: os três `.md` dizem agora "o selo a decidir (na Camada de busca)" e contam os 25 rótulos por tipo. |

### Conceito A

| Conserto | Situação |
|---|---|
| 4. [R5] Camada de busca separada do Conteúdo por um vão | feito: os bairros Portas e Conteúdo agora se encostam, e a estação final da linha buscar fica sobre a borda comum. |

### Conceito B

| Conserto | Situação |
|---|---|
| 4. (não se aplica) | não se aplica: a rua da busca já levava ao Conteúdo; mantida. |
| 6. [R5] Maestro entra por cima da muralha | feito: um portão pequeno, sem nome, na muralha esquerda (o mesmo lado dos portões das portas); a linha do Maestro passa por ele até o armazém do acervo. |
| 7. [R5] Par B com blocos genéricos | feito: o Par B é a mesma planta em miniatura (40%): a muralha, a rua e os seis quarteirões na mesma disposição, com o cofre no mesmo lugar. A linha de troca entra pela rua e chega ao cofre dele. |

### Conceito C

| Conserto | Situação |
|---|---|
| 4. [R5] Chave da altura com o Conteúdo no alto | feito pela segunda opção do parecer: o Conteúdo desceu para o primeiro subsolo, logo acima do núcleo. A chave "mais fundo, mais perto da verdade" fica de pé (ver `decisoes.md`, item 17). |
| 5. [R5] Camada de busca abre para cima, oposta à Porta do banco | feito: porta tracejada sem seta; a ficha diz as duas moradas em teste; a frase "apontam para lados opostos" saiu do `.md`. |

## UX revisor

### Comuns aos três

| Conserto | Situação |
|---|---|
| Cor: buscar, gravar e disco e banco são três azuis vizinhos (6 de A; 7 de B; 6 de C) | feito: disco e banco virou linha pontilhada cinza-azulada; gravar ficou marinho mais escuro e buscar continua petróleo e mais grossa. O nome curto aparece uma vez sobre cada traço (buscar, gravar), em itálico, na cor da linha. |
| Affordance: nada diz que o bairro abre (7 de A; 8 de B; 7 de C) | feito: um sinal ⊕ junto do nome de cada bairro (desenho, sem texto); ao passar o mouse, o contorno do bairro escurece igual ao foco e o sinal se inverte; a legenda termina com "⊕ cada bairro abre uma ficha", em tinta escura e negrito. |
| Tipografia: nome do bairro em 11 px, caixa alta (8 de A; 9 de B; 8 de C) | feito de outro jeito: 14 px, semibold, em caixa normal (não alta). Em caixa alta a 13 px, nomes como "Núcleo de dados do par" não cabiam nos bairros estreitos; em caixa normal leem melhor e ocupam menos. Legenda subiu para 13 px em tinta mais escura. |
| 320 px: a primeira vista corta rótulos e esconde o Banco local (9 de A; 9 de B; 8 de C) | feito: a faixa abre já rolada com o Banco local no meio, e um degradê nas duas bordas mostra que há mais dos lados. Rótulos nas bordas ainda saem cortados, porque é uma faixa; a lista dos bairros segue embaixo. Conferido numa moldura de 320 px de verdade. |

### Conceito A

| Conserto | Situação |
|---|---|
| 1. [R3] Rede privada e Par B a 23,5 px | feito: com a rede privada deitada, a menor folga do A passou a ser outra (29,5 px, Banco local e Sincronizador); Rede privada e Par B ficaram a 31 px. |
| 2. [Composição] Rede privada em pé, atravessada | feito: virou um trilho deitado, com dormentes, sob a linha de troca. |
| 3. [R3] Nome do Núcleo encostado em Vista Markdown | feito: o nome subiu para o topo da caixa. Para a linha da vigia não cortar o nome, a Vigia do sync foi para a direita do bairro e a linha entra no Banco local pelo lado direito. |
| 4. [R6] Só caixas arredondadas | feito: Banco local como grande baldeação de anel duplo; Rede privada como trilho com dormentes; Par B como estação terminal com o batente de fim de linha. Os bairros continuam caixas (é o fundo do mapa de linhas). |
| 5. [Hierarquia] Buscar para longe do Conteúdo | feito: igual ao conserto 4 do Tech lead. |
| 6, 7, 8, 9 | feitos: ver os comuns. |

### Conceito B

| Conserto | Situação |
|---|---|
| 1. [R1] Dois verdes paralelos até o Obsidian | feito: o Gustavo chega à oficina pela esquerda; a linha do Obsidian ao Banco local sai por cima. |
| 2. [Hierarquia e Composição] Outra cidade ocupa um terço | feito: o Par B é uma miniatura a 40% e a área de "Fora do par" encolheu; a muralha do par A ganhou 70 unidades de largura. |
| 3. [R3] Núcleo e Vigilância a 15 px | feito: 40 unidades entre as caixas. |
| 4. [R3] "Agentes" e "Gustavo" encostam nas linhas | feito: as linhas começam à direita da figura, com um trecho reto antes de virar; os nomes ficam acima. |
| 5. [Densidade] Contrato e Obsidian como caixas vazias; seis telhados soltos | feito: Contrato é uma prefeitura (frontão e colunas), Obsidian uma oficina de telhado em serra, Raiz um quarteirão só com seis telhados. |
| 6. [Tipografia] "Rede privada" em pé | feito: a estrada está deitada, na altura da rua, e o nome deitado embaixo dela. |
| 7, 8, 9 | feitos: ver os comuns. |

### Conceito C

| Conserto | Situação |
|---|---|
| 1. [R1] Vigiar e editar em dois L encaixados junto ao Banco local | feito: a vigiar desce e entra por cima; a editar entra pelo lado direito, acima da troca. |
| 2. [R2] Andares encostados | feito: entre as faixas há agora uma laje de 45 a 50 unidades. |
| 3. [R3] "Sincronizador" perto do nome do bairro | feito: rótulo à direita da estação, como o da Vista Markdown; o nome do bairro foi para o topo da caixa. |
| 4. [Composição] Linha da vigia do topo ao subsolo | feito em parte: a Vigilância foi para o alto da torre, à direita, sobre a Periferia, como pedido, e a linha desce reta. Ela continua longa porque, com o Conteúdo no subsolo (Tech lead, conserto 4), o cofre ficou mais fundo. Encurtar mais pediria a torre no subsolo, contra a ideia da vigia que olha de cima. |
| 5. [Densidade] Disciplina com um item numa faixa larga | feito de outro jeito: baixei a altura do andar (de 104 para 90 unidades) em vez de pôr salas sem rótulo. Salas sem nome seriam formas soltas, o que a régua recusa (a trilha até o cume). |
| 6, 7, 8 | feitos: ver os comuns. No 320, a faixa abre no Banco local, com o subsolo à vista. |
