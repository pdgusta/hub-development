---
titulo: Como o agente acha tudo, e nada fica órfão
ticket: 12
aberta: 2026-10-14
estado: absorvida
carta: prototipo-12-sumario
---

Resposta à sua pergunta da rodada anterior: como os blocos ficam fáceis de usar e de achar pelos agentes, e como
nenhum arquivo fica sem nada que o referencie.

**A estratégia, em quatro pulos.** O agente nunca lista pastas para achar algo; ele segue índices:

1. `AGENTS.md` da raiz do hub (já decidido: uma cabeça curta, de até 2.000 caracteres) → aponta para o catálogo de
   blocos e para o índice de cada raiz;
2. `clients/index.md`, `operations/index.md`… → uma linha por iniciativa, com o que ela é;
3. `AGENTS.md` da iniciativa → o mapa: os seis arquivos do núcleo, os blocos em uso (uma linha cada) e os arquivos
   mais importantes, citados direto;
4. `index.md` de cada pasta de bloco, e de cada subpasta dentro dele → uma linha por arquivo ou subpasta, dizendo o
   que é.

Um arquivo fundo continua achável porque cada nível cita o de baixo, como um sumário de livro. Os importantes podem
ser promovidos ao mapa do `AGENTS.md` da iniciativa, para chegar em um pulo só.

## O catálogo de blocos
id: catalogo
tipo: escolha
recomendada: A

- A: Um arquivo `agents/blocks.md`, citado pelo `AGENTS.md` da raiz: cada bloco com uma linha do que entra, o que não entra e um exemplo, mais a pilha sugerida por tipo; uma skill "nova iniciativa" o usa para criar a pasta, o núcleo e os índices
- B: Só a skill "nova iniciativa", com o catálogo dentro dela
- C: A descrição de cada bloco escrita no `AGENTS.md` de cada iniciativa

Por que A: um lugar só, que todo agente acha a partir da raiz, inclusive quem vai gravar numa iniciativa que já
existe e não está criando nada. Em B, o catálogo só aparece quando a skill é chamada; em C, ele se repete em cada
iniciativa e diverge com o tempo.

## O bloco genérico
id: generico
tipo: escolha
recomendada: A

- A: `misc/`, para o que não cabe em nenhum bloco; quando três ou mais arquivos parecidos se juntam ali, o agente propõe um bloco novo para o catálogo
- B: `other/`, com a mesma regra
- C: Sem bloco genérico; o agente sempre escolhe o bloco mais próximo

Por que A: o órfão tem um lugar declarado, e a regra de promover evita que `misc/` vire o depósito de tudo. O
nome `misc/` é o mais comum em projetos; `other/` serve igual, se você preferir.

## Como nenhum arquivo fica sem referência
id: orfaos
tipo: escolha
recomendada: A

- A: Toda pasta tem um `index.md`, e um verificador sem IA roda no hook do fim de cada resposta: ele acha o arquivo que nenhum índice cita, já o inscreve no `index.md` da pasta como "sem descrição" e avisa o agente para descrevê-lo
- B: O mesmo verificador, mas ele só avisa, sem inscrever
- C: Só uma regra no `AGENTS.md` pedindo que o agente atualize os índices

Por que A: a primeira lição do vault foi "falha se corrige com mecanismo, nunca com regra nova", e a C é só regra.
Na A, o arquivo nunca fica sem referência nem por um instante depois da resposta, mesmo que o agente esqueça: no
pior caso, ele fica citado como "sem descrição", visível para quem passar. O hook do fim da resposta já foi
decidido no "Contrato file-first" para a nota de retomada; o verificador entra no mesmo lugar. **Não verificado:**
um hook equivalente no Codex e no Copilot, que é pergunta do ticket "Acesso dos agentes: decisão". Para eles, o
mesmo verificador roda também na checagem do início de sessão.

## Algo mais?
id: algo-mais
tipo: texto
