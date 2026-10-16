# Parecer do Tech lead, volta 2 (porta da fase 3)

2026-10-15. Régua da cidade (`regras.md`, `como-julgar.md`) contra o `texto-do-hub.md` (rodada 2). Meu papel: Nomes
(R4), Papel na cidade (R5) e Forma nova (R6). As outras regras são do UX revisor e do QA; cito os números do QA só como
fundo.

Evidência usada:
- capturas do QA a 1280 px (`qa/volta-2/conceito-a|b|c/captura-1280.png`);
- marcação e textos do desenho extraídos dos três HTML;
- dados das fichas (objeto `G`): **idênticos nos três** (mesma soma), lidos por inteiro;
- `consertos.md`, `decisoes.md` (itens 16 a 25) e a diferença entre os `.md` da volta 1 e da volta 2.

---

## 1. Os consertos que pedi na volta 1

| Conserto (volta 1) | Situação | Conferido em |
|---|---|---|
| Comum 1. Selo "como os agentes gravam" na Porta do banco | **feito**, e também na ligação Agentes → Porta do banco → Banco local | ficha Portas do par |
| Comum 2. Selo "árvore abaixo das seis raízes e frontmatter" na Raiz | **feito**, mais "zonas por ciclo de vida" (seção 7, aceito) | ficha Conteúdo |
| Comum 3. "não verificado: duas instâncias do MCP" e "a decidir: como cada ferramenta carrega contrato e MCP" | **feito**; "não verificado" com selo de cor própria (aceito: a seção 7 separa as duas palavras) | fichas Portas do par e Disciplina |
| Comum 5/6. Frase "13 itens com o selo a decidir" nos `.md` | **feito**: os três contam os 25 rótulos por tipo | `.md` dos três |
| A 4. Camada de busca separada do Conteúdo | **feito**: a estação fica sobre a borda comum de Portas e Conteúdo | captura A, centro |
| B 6. Maestro passa por cima da muralha | **feito**: portão sem nome na muralha esquerda (aceito; nenhum `data-item` novo) | captura B, canto superior esquerdo |
| B 7. Par B com blocos genéricos | **feito**: miniatura da mesma planta, cofre no mesmo lugar | captura B, direita |
| C 4. Chave da altura com o Conteúdo no alto | **feito pela segunda saída**: Conteúdo no primeiro subsolo, logo acima do núcleo. A chave "mais fundo, mais perto da verdade" agora vale para todo item | captura C; subtítulo da peça |
| C 5. Busca abre para cima, oposta à Porta do banco | **feito**: porta tracejada sem seta; a ficha diz as duas moradas em teste; a frase saiu do `.md`. A seta da Porta do banco para baixo fica (aceito: a ligação ao banco está decidida, seção 4) | captura C; ficha Portas do par |

Além da lista, o UI engineer marcou os outros assuntos da seção 7 que tocam itens (forma do mod da vigia, hooks no
Codex e no Copilot, perfil por máquina, convivência com o Obsidian do vault, arquivos entre 50 e 200 MiB, guarda do
acervo por extenso, roteamento de skills). Conferi linha a linha contra a seção 7: todos estão lá, e nenhum selo
marca como aberto algo decidido. A seção 7 fica coberta por inteiro onde toca um componente. Os assuntos sem
componente na peça (passagem para o hub real, FreeLLMAPI além de embeddings) não precisam de selo.

## 2. Nomes (R4), o que vale para os três

- 25 rótulos no desenho: 7 bairros, 15 itens, 1 selo "a decidir", 2 nomes de linha (buscar, gravar).
- Os 15 itens e os 7 bairros batem com o texto do hub (seções 3 e 3.5); "Par B" segue aceito (seção 4 + glossário).
- "buscar" e "gravar" são os nomes dos fluxos 5.2 e 5.1. Não são rótulo de item; aceito.
- 0 códigos internos (QA e conferência minha).
- Ressalva para o maestro: o relatório do QA diz que entrou no desenho "cada bairro abre uma ficha". Na peça, essa
  frase está só na legenda em HTML. Os 25 são 23 + buscar + gravar. O número está certo; a descrição do QA, não.
- **Atenção:** os três estão em 25, o limite da vista de cima. Nenhum conserto meu abaixo acrescenta rótulo.

---

## Conceito A: Linhas do hub

- **R1, R2, R3:** não é do meu papel. (QA: 0 cruzamentos; 25 rótulos; folga 29,5 px.)
- **R4 Nomes:** passa. Evidência: 15 itens e 7 bairros conferidos contra o texto do hub; fichas com toda a seção 7 que
  toca componentes; 0 códigos.
- **R5 Papel na cidade:** passa. Evidência: tabela cobre todos os itens. A linha buscar termina na divisa de Portas e
  Conteúdo, e a busca se lê como entrada do conteúdo (seção 1). O banco como baldeação de anel duplo segue exato
  (seção 4). Rede privada como trilho só sob a linha de troca = "o único caminho entre pares". Par B como terminal
  com batente: a linha acaba num banco igual. Não vi problema novo.
- **R6 Forma nova:** passa. Evidência: mapa de linhas; banco como baldeação, não centro.

| Dimensão | Nota | Por quê |
|---|---|---|
| 4 Nomes (R4) | 5 | Nada a consertar. |
| 5 Papel na cidade (R5) | 5 | Nada a consertar. |
| 6 Forma nova (R6) | 5 | Outra leitura, nenhuma forma recusada. |
| 1 a 3, 7 a 12 | não é do meu papel | UX revisor e QA. |

**Veredito, nas minhas regras: passa.** O veredito do conceito depende do parecer do UX revisor.

Consertos: nenhum.

---

## Conceito B: Duas cidades e a estrada

- **R1, R2, R3:** não é do meu papel. (QA: 0; 25; 29,1 px.)
- **R4 Nomes:** passa. Evidência: como em A; Raiz e Contrato, que estão à vista, agora têm os selos nas fichas.
- **R5 Papel na cidade:** passa. Evidência: Maestro entra por portão, como toda a gente (3.5). Par B é a mesma planta
  em miniatura, e a rua de troca liga cofre a cofre: "pares, nenhum é referência" (3.1) se lê sem legenda. Contrato
  como prefeitura combina. **Problema novo que o conserto criou:**
  - o Obsidian virou "oficina de telhado em serra". Na captura, o desenho lê como fábrica. A régua dá como exemplo de
    contradição justamente "o Obsidian como usina, quando ele pode ficar fechado e nada para" (R5). A tabela diz
    oficina, que combina; o desenho diz fábrica. Não chega a contradizer o papel, mas puxa para o lado errado.
    Conserto 1;
  - a Raiz, "um quarteirão com seis telhados", usa o mesmo serrilhado. Lida ao lado do Obsidian, parece outro galpão
    industrial; as "seis raízes" não se leem como seis lugares distintos. Conserto 2.
- **R6 Forma nova:** passa. Evidência: planta em grade, muralha e estrada; o cofre é um quarteirão entre outros.

| Dimensão | Nota | Por quê |
|---|---|---|
| 4 Nomes (R4) | 5 | Nada a consertar. |
| 5 Papel na cidade (R5) | 4 | Papéis certos; o desenho do Obsidian e da Raiz puxa para galpão industrial. |
| 6 Forma nova (R6) | 5 | Outra leitura, nenhuma forma recusada. |
| 1 a 3, 7 a 12 | não é do meu papel | UX revisor e QA. |

**Veredito, nas minhas regras: passa.** Os consertos abaixo são pequenos e não mudam a leitura.

Consertos:
1. [R5] desenho, Obsidian: telhado em serra (lê como fábrica) → oficina pequena de telhado de duas águas, com porta
   e janela, sem serrilhado; deixa claro que é uma bancada que pode fechar, não algo que produz. Evidência: captura
   B, bairro Periferia; régua, R5 (exemplo do Obsidian como usina).
2. [R5] desenho, Raiz: barra serrilhada → seis casinhas encostadas numa fileira, cada uma com o próprio telhado (o
   mesmo quarteirão, sem rótulo novo). Evidência: captura B, bairro Conteúdo; texto do hub, 3.2 (seis raízes, "cada
   uma com comportamento próprio").

---

## Conceito C: A cidade em corte

- **R1, R2, R3:** não é do meu papel. (QA: 0; 25; 28,9 px, a menor folga dos três, entre Camada de busca e Porta do
  banco.)
- **R4 Nomes:** passa. Evidência: como em A.
- **R5 Papel na cidade:** passa. Evidência: as duas contradições da volta 1 saíram. O Conteúdo fica no primeiro
  subsolo, logo acima do cofre, e a ficha diz "é o que o banco guarda e a vista mostra" (seção 1; 3.2). A busca não
  aponta mais contra a opção "índice dentro da porta do banco" (seção 7). Ressalvas:
  - **Problema novo que o conserto criou:** ao perder a seta, a Camada de busca ficou sem relação visível com o
    Conteúdo. A tabela diz "é por ela que se entra para achar o conteúdo", mas na captura nada sai da busca para
    baixo; o único traço que desce do térreo é o da Porta do banco. A ideia central do hub, "a busca é a porta do
    conteúdo" (seção 1; princípios da seção 2), não se lê. Conserto 1;
  - a linha do Maestro desce reta do alto, atravessando a Disciplina e as Portas sem passar por porta nenhuma.
    Antes ele chegava ao andar de cima; agora fura dois andares. Pela 3.5, gente chega pelas portas. Não contradiz
    papel (o maestro começa pelo acervo), mas a forma diz "entra por fora das portas". Conserto 2.
- **R6 Forma nova:** passa. Evidência: corte em faixas com lajes entre elas, cada faixa com desenho e poucos nomes,
  não seções de texto.

| Dimensão | Nota | Por quê |
|---|---|---|
| 4 Nomes (R4) | 5 | Nada a consertar. |
| 5 Papel na cidade (R5) | 4 | Chave coerente agora; a busca não se lê como porta do conteúdo e o Maestro fura os andares. |
| 6 Forma nova (R6) | 4 | Forma nova; as faixas ficam perto de "camadas empilhadas", sem cair nela. |
| 1 a 3, 7 a 12 | não é do meu papel | UX revisor e QA. |

**Veredito, nas minhas regras: passa.** O conserto 1 vale a pena antes da carta, porque toca a ideia central do hub.

Consertos:
1. [R5] desenho, abaixo da Camada de busca: nada a liga ao Conteúdo → um poço ou escada tracejada (forma, não
   ligação, sem `data-ligacao` e sem rótulo) do piso da busca até a laje do Conteúdo, no mesmo tracejado "a decidir".
   Descer não decide a morada: as duas opções em teste (disco, índice na porta do banco) ficam abaixo do térreo.
   Evidência: captura C, faixa Portas do par (x ≈ 350) e Conteúdo logo abaixo; texto do hub, seção 1 e seção 7.
2. [R5] desenho, linha do Maestro: fura Disciplina e Portas → fazer o Maestro chegar pela rua, como as outras pessoas,
   e descer ao acervo por um acesso próprio na faixa das portas (sem rótulo novo); ou levar a linha pela lateral do
   prédio até o primeiro subsolo. Evidência: captura C, linha vertical em x ≈ 620; texto do hub, 3.5 (gente chega
   pelas portas).

---

## Onde cada conceito é melhor (sem ranking)

- **Nomes (R4):** empate. Mesmos rótulos, mesmas fichas, seção 7 coberta nos três.
- **Papel na cidade (R5):** A diz melhor a busca como entrada do conteúdo (a estação na divisa) e o banco como ponto
  por onde tudo passa. B diz melhor que os pares são iguais (a mesma planta do outro lado da estrada). C diz melhor
  quão perto da verdade cada coisa está, agora que a chave vale para todos, mas é o que pior mostra a busca como
  porta.
- **Forma nova (R6):** A e B no mesmo nível; C um pouco abaixo pelo risco das faixas.

Para a carta: nas minhas regras, os três passam. Nenhum conserto meu acrescenta rótulo; os três estão no limite de 25
da vista de cima.
