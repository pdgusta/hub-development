# Calibração do limiar de repetidas (2026-10-15)

Amostra: o teste curto (`teste/`), 3 células × 4 modelos, 155 perguntas distintas. Script: `python calibrar.py
--base teste --por-faixa 12` (lista pares por faixa de similaridade, para ler à mão).

## O que mudou no método ao ler os pares

1. **Jaccard simples de tokens** (sem palavras vazias, raiz por prefixo de 6): as perguntas de molde igual dominam.
   "O Sincronizador faz parte do grupo de componentes que vivem na máquina?" × "O banco faz parte do grupo de
   componentes que vivem na máquina?" dá 0,75, e são perguntas diferentes. Nenhum limiar separa.
2. **Jaccard ponderado por IDF** (peso log(N/df) sobre todas as perguntas do livro-razão): melhora, mas o mesmo par
   ainda fica em 0,77.
3. **Mais uma condição: as peças e os atores citados precisam coincidir** (léxicos `ENTIDADES` e `ATORES` em
   `juntar.py`, tirados do resumo neutro), com Jaccard de pelo menos 0,5 em cada conjunto. "Eu" vira "Gustavo" (é a
   voz da lente dele). Com isso o molde igual sobre peças diferentes deixa de ser repetida.

## Pares com o método final, por faixa (amostra)

| Faixa | Pares | Leitura |
|---|---|---|
| 0,7 a 0,8 | 1 | "criar uma nova iniciativa" × "criar uma nova casa para uma iniciativa": repetida |
| 0,5 a 0,6 | 4 | vigia "roda periodicamente" × "vive na máquina": repetida; arquivo de 200 MiB criado por mim × detectado pelo sincronizador: repetida; "o banco" × "o MCP do banco" no mesmo molde: distintas; pasta com ponto × pasta não replicada: distintas |
| 0,4 a 0,5 | 5 | 1 repetida ("agente altera arquivo no disco" × "agente de código altera arquivo no hub"); 4 distintas (ler × criar nota, criar × alterar iniciativa, pasta com ponto × pasta nova) |
| 0,3 a 0,4 | 10 | quase todas distintas; 3 a 4 são a mesma pergunta com outra redação (GitHub como backup, sincronizador parado, MCP fora do ar) |

## Escolha

**Limiar 0,50** (Jaccard ponderado por IDF, mais as peças e atores com Jaccard ≥ 0,5). Na faixa ≥ 0,5, 3 de 5 pares
são repetidas; abaixo, a maioria é distinta. O método é conservador: deixa passar repetidas de redação diferente
(faixa 0,3 a 0,4), o que **superestima a taxa de novas** e tende a alongar a corrida (o teto de 2 h segura). A
junção fina por sentido é a etapa 2 do plano (maestro). Efeito na amostra: 155 → 150 únicas (0,45 daria 148;
0,55 daria 152).
