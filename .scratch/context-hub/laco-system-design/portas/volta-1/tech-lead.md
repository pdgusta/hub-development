# Parecer do Tech lead, volta 1 (porta da fase 3)

2026-10-15. Julgado pela régua da cidade (`regras.md`, `como-julgar.md`), contra o `texto-do-hub.md` (rodada 2).
Meu papel: Nomes (R4), Papel na cidade (R5) e Forma nova (R6). As outras regras e dimensões são do UX revisor e do
QA; cito os números do QA só como fundo.

Evidência usada:
- capturas do QA a 1280 px (`qa/volta-1/conceito-a|b|c/captura-1280.png`), visão geral;
- marcação no HTML (`data-item`, `data-grupo`, `data-ligacao`, `data-encontro`) e textos do desenho, extraídos dos três
  arquivos;
- os dados das fichas (objeto `G` no script): **idênticos nos três** (mesmo conteúdo, conferido por soma);
- as tabelas de papel nos `.md` e `decisoes.md` do UI engineer.

---

## O que vale para os três

**Rótulos do desenho.** 23 por conceito: 7 bairros, 15 itens, 1 selo "a decidir".
- Os 7 bairros têm os nomes exatos dos agrupamentos naturais (texto do hub, 3.5).
- Os 15 itens batem com a coluna "Rótulo" (seções 3.1, 3.3 e 3.4). Exceção justificada: **Par B** não tem linha na
  seção 3; vem da seção 4 ("banco local do par B") e "par" é termo do glossário. Aceito.
- 0 códigos internos (QA e conferência minha). Nenhum componente rotulado como "peça". Nenhum nome inventado para a
  metáfora: a metáfora fica no desenho.
- As linhas da legenda (buscar, gravar, disco e banco, troca entre pares, vigiar, editar, disciplina e acervo) vêm dos
  fluxos da seção 5 e ficam fora do desenho. Aceito.

**Ligações.** As 11 marcadas (10 em B) estão na seção 4, salvo `Gustavo → Obsidian` e `Maestro → Acervo do maestro`,
tiradas da 3.4 ("Como"). Aceito; o `decisoes.md` diz a origem. Nenhuma ligação inventada: a busca como porta do
conteúdo vai na forma, sem traço (`decisoes.md`, item 9). Correto.

**Itens "a decidir" (seção 7).** Marcados hoje: Camada de busca (desenho e ficha), Pasta não replicada, Claude Desktop
(se grava) e Guarda do acervo (não verificado), nas fichas. **Faltam** três assuntos da seção 7 que tocam itens da
peça:
1. "Como os agentes gravam" (disco, porta do banco ou os dois; conferência de versão no disco). Toca a Porta do banco
   e a linha gravar. A ficha da Porta do banco não tem selo.
2. "Árvore interna e frontmatter" (só as seis raízes estão decididas). Toca Raiz e Conteúdo.
3. "Duas instâncias do MCP por par": **não verificado**. Toca Porta do banco e Porta de leitura.
Também "Como cada ferramenta carrega contrato e MCP" (em curso) toca a ligação do Contrato com a configuração de cada
ferramenta, que está na ficha da Disciplina sem selo.

Pelo limiar de R4 ("os itens da seção 7 aparecem marcados a decidir"), isso é **falha** nos três. O conserto é só nos
dados da ficha, igual nos três, sem mexer no desenho.

**Texto dos `.md`.** Os três dizem "13 estações (ou itens) com o selo a decidir". Na peça, o selo aparece em um item
só (Camada de busca). A frase descreve errado a peça. Conserto pequeno.

**Forma nova (R6).** O acabamento é o mesmo nos três (`decisoes.md`, item 13), e as peças continuam diferentes: o teste
de troca de acabamento já está feito pela própria construção. Nenhum repete forma recusada: não há centro com anéis,
nem seções de texto empilhadas, nem ícones soltos ligados por setas. Cada um muda o que o leitor faz: A segue linhas,
B procura lugares, C lê pela altura.

---

## Conceito A: Linhas do hub

- **R1 Linhas sem se cruzar:** não é do meu papel. (QA: 0 cruzamentos.)
- **R2 Vista mais de cima:** não é do meu papel. (QA: 23 rótulos.)
- **R3 Distância entre os itens:** não é do meu papel. (QA: folga mínima 23,5 px, a mais justa dos três.)
- **R4 Nomes:** falha. Evidência: rótulos 100% conferidos contra o texto do hub, 0 códigos; mas as fichas não marcam
  os três assuntos da seção 7 listados acima. Conserto: selos nas fichas (consertos 1 a 3).
- **R5 Papel na cidade:** passa. Evidência: tabela do `.md` cobre todos os itens do desenho e das fichas; nenhum
  equivalente contradiz o papel. O banco como estação de baldeação onde gravar, editar, vigiar, disco e troca se
  encontram é exato (seção 4: todas essas ligações chegam ao banco). Obsidian como estação de embarque só do Gustavo:
  fechada, só a linha dele para (3.1, "pode ficar fechado"). Bairros = os sete de 3.5. Ressalva: na captura, a
  estação Camada de busca fica dentro do bairro Portas, separada do bairro Conteúdo por um vão; a ideia "a busca é a
  porta do conteúdo" (seção 1, princípio da seção 2) quase não se lê. Conserto 4.
- **R6 Forma nova:** passa. Evidência: mapa de linhas, sem centro nem anéis; o banco é baldeação, não centro do mundo.

Nota por dimensão (só as minhas):

| Dimensão | Nota | Por quê |
|---|---|---|
| 4 Nomes (R4) | 2 | Regra em falha (seção 7 incompleta nas fichas). Os rótulos em si estão certos. |
| 5 Papel na cidade (R5) | 4 | Papéis certos; a busca como porta do conteúdo fica fraca. |
| 6 Forma nova (R6) | 5 | Outra leitura, nenhuma forma recusada. |
| 1 a 3, 7 a 12 | não é do meu papel | UX revisor e QA. |

**Veredito: volta.** Motivo: Nomes (R4) em falha.

Consertos:
1. [R4] ficha do bairro Portas do par, item Porta do banco: sem selo → selo "a decidir: como os agentes gravam (disco,
   porta do banco ou os dois) e como conferem a versão no disco". Evidência: texto do hub, seção 7, e 5.1 passo 4.
2. [R4] ficha do bairro Conteúdo, item Raiz: sem selo → selo "a decidir: a árvore abaixo das seis raízes e o
   frontmatter". Evidência: seção 7.
3. [R4] fichas Portas do par (Porta do banco e Porta de leitura) e Disciplina do agente (ligação Contrato →
   configuração de cada ferramenta): sem marca → "não verificado: duas instâncias do MCP por par" e "a decidir: como
   cada ferramenta carrega contrato e MCP". Evidência: seção 7.
4. [R5] desenho, estação Camada de busca: separada do bairro Conteúdo por um vão → pôr a estação na borda comum dos
   dois bairros (ou encostar o Conteúdo no fim da linha buscar), para a linha buscar terminar visivelmente na entrada
   do conteúdo. Evidência: captura 1280, bairro Portas (y ≈ 380) e Conteúdo (fundo y ≈ 340).
5. [texto] `conceito-a.md`: "13 estações com o selo a decidir" → "13 estações; o selo a decidir na Camada de busca".

---

## Conceito B: Duas cidades e a estrada

- **R1, R2, R3:** não é do meu papel. (QA: 0 cruzamentos, 23 rótulos, folga 29,1 px.)
- **R4 Nomes:** falha. Evidência: rótulos 100% conferidos, 0 códigos; mesmas lacunas da seção 7 nas fichas. Aqui pesa
  mais: Raiz e Contrato estão na visão geral, e os dois tocam assuntos "a decidir" (árvore interna; como cada
  ferramenta carrega o contrato) sem marca em lugar nenhum. Conserto: 1 a 3.
- **R5 Papel na cidade:** passa. Evidência: tabela cobre todos os itens; nenhum equivalente contradiz. É o que melhor
  diz "pares iguais, nenhum é referência" (3.1): a outra cidade do outro lado da estrada, com a rua de troca de cofre a
  cofre. A rua desenhada do portão da busca ao bairro Conteúdo diz a busca como porta do conteúdo sem inventar
  ligação. Raiz como seis casas = as seis raízes (3.2). Contrato como prefeitura e checkpoint, guarda e registro como
  fiscais: combina com "regras do hub para os agentes". Ressalvas:
  - o Maestro entra por cima da muralha, sem portão, enquanto a tabela diz que gente "só entra pelos portões"
    (3.5: gente chega pelas portas). Conserto 6.
  - Par B é "a mesma planta", mas na captura os blocos dele não repetem a disposição do par A. Conserto 7.
  - Checkpoint fica fora da visão geral; o princípio "o checkpoint grava sem pedido" (seção 2, que pede os princípios
    visíveis) só aparece na ficha. Não é falha; é o preço da escolha de B (`decisoes.md`, item 7).
- **R6 Forma nova:** passa. Evidência: planta em grade com muralha e estrada; o cofre é um quarteirão entre outros.

| Dimensão | Nota | Por quê |
|---|---|---|
| 4 Nomes (R4) | 2 | Regra em falha; Raiz e Contrato à vista sem a marca da seção 7. |
| 5 Papel na cidade (R5) | 4 | Papéis certos; duas ressalvas de forma (entrada do Maestro, Par B). |
| 6 Forma nova (R6) | 5 | Outra leitura, nenhuma forma recusada. |
| 1 a 3, 7 a 12 | não é do meu papel | UX revisor e QA. |

**Veredito: volta.** Motivo: Nomes (R4) em falha.

Consertos:
1. a 3. [R4] iguais aos de A (selos nas fichas da Porta do banco, Raiz, Porta de leitura e ligação do Contrato).
4. (não se aplica: a rua da busca já leva ao Conteúdo.)
5. [texto] `conceito-b.md`: "13 itens com o selo a decidir" → corrigir como em A.
6. [R5] desenho, linha do Maestro: passa por cima da muralha → fazer a linha entrar por um portão (o mesmo lado dos
   portões das portas) até o armazém do acervo. Evidência: captura 1280, canto superior esquerdo.
7. [R5] desenho, Par B: blocos genéricos → repetir em miniatura a silhueta dos quarteirões do par A (mesma
   disposição), para "a outra cidade, mesma planta" se ler sem legenda. Evidência: captura 1280, lado direito.

---

## Conceito C: A cidade em corte

- **R1, R2, R3:** não é do meu papel. (QA: 0 cruzamentos, 23 rótulos, folga 34,1 px.) A dúvida "vista mais de cima
  como ângulo de câmera" (`decisoes.md`, item 10) é de R2, do UX revisor.
- **R4 Nomes:** falha. Evidência: rótulos 100% conferidos, 0 códigos; mesmas lacunas da seção 7 nas fichas.
  Conserto: 1 a 3.
- **R5 Papel na cidade:** falha. Evidência, duas contradições com o texto do hub:
  - A chave de leitura de C é "a altura diz quão perto da verdade cada coisa está" (`conceito-c.md`; subtítulo da
    peça). O Conteúdo fica no andar mais alto, o mais longe do cofre. Mas o conteúdo (raízes, iniciativas, notas,
    acervo) **é** o que o banco guarda e a vista mostra (seção 1; 3.2 "o que vai ao banco"). Pela própria chave de C,
    o leitor conclui que o conteúdo mora longe da verdade, como se fossem duas coisas.
  - C desenha a Camada de busca abrindo para cima e a Porta do banco descendo ao cofre, "em lados opostos"
    (`conceito-c.md`). A seção 7 tem em teste justamente "índice dentro da porta do banco" como uma das duas opções
    de onde a busca mora. O desenho decide contra essa opção; o tracejado não basta, porque a direção diz o
    contrário.
  - O resto da tabela combina: vigia no alto da torre com cabo até o cofre; rede privada como túnel fechado; Obsidian
    como oficina fora do prédio; checkpoint entre a porta e o conteúdo.
- **R6 Forma nova:** passa. Evidência: corte lateral em faixas, cada faixa com desenho e um ou dois nomes, não seções
  de texto; o cofre no fundo, não no centro.

| Dimensão | Nota | Por quê |
|---|---|---|
| 4 Nomes (R4) | 2 | Regra em falha (seção 7 incompleta nas fichas). |
| 5 Papel na cidade (R5) | 2 | Conteúdo longe da verdade; busca e porta do banco opostas, decidindo o que está em aberto. |
| 6 Forma nova (R6) | 4 | Forma nova; a leitura em faixas fica perto de "camadas empilhadas", sem cair nela. |
| 1 a 3, 7 a 12 | não é do meu papel | UX revisor e QA. |

**Veredito: volta.** Motivos: Nomes (R4) e Papel na cidade (R5) em falha.

Consertos:
1. a 3. [R4] iguais aos de A.
4. [R5] chave de leitura e posição do Conteúdo: "altura = perto da verdade" com o conteúdo no alto → ou trocar a chave
   (a altura diz **quem age**: gente na rua, regras e portas no meio, a guarda da verdade embaixo) e mostrar que os
   andares do conteúdo são a vista do que o cofre guarda (o elevador do sincronizador subindo até eles), ou descer o
   Conteúdo para junto do núcleo. Evidência: subtítulo da peça; texto do hub, seção 1 e 3.2.
5. [R5] direção da Camada de busca: abre para cima, oposta à Porta do banco → desenhar a busca sem direção fixa (porta
   tracejada sem seta, com as duas moradas possíveis indicadas na ficha), e tirar do `.md` a frase "apontam para
   lados opostos". Evidência: texto do hub, seção 7, primeira linha.
6. [texto] `conceito-c.md`: "13 itens com o selo a decidir" → corrigir como em A.

---

## Onde cada conceito é melhor (sem ranking)

- **Nomes (R4):** empate. Mesmos rótulos, mesmas fichas, mesma lacuna.
- **Papel na cidade (R5):** B diz melhor duas verdades do hub: os pares são iguais (a outra cidade) e a busca leva ao
  conteúdo (a rua). A diz melhor que tudo passa pelo banco (a baldeação). C diz melhor a vigilância de cima, mas falha
  no conteúdo.
- **Forma nova (R6):** A e B no mesmo nível; C um pouco abaixo pelo risco de faixas.

Fora do meu papel, mas registro: o QA achou foco sem mudança visível nos três (acessibilidade); confirmar é do UX
revisor.

Observação para a carta: os consertos de Nomes são só nos dados das fichas e iguais nos três. Feitos, A e B ficam
sem falha nas minhas regras; C ainda precisa dos consertos de Papel na cidade.
