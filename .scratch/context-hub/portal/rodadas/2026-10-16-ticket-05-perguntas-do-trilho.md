---
titulo: Frontmatter imposto: três perguntas do Trilho
ticket: 16
aberta: 2026-10-16
estado: absorvida
---

O Trilho pegou o ticket 05 (os esquemas de frontmatter, o verificador sem IA e o script "nova iniciativa") e achou três
pontos que o spec deixa abertos. Enquanto você decide, ele segue com o núcleo usando a opção recomendada de cada um como
provisória; mudar depois é trocar o esquema.

**1. O que mais o verificador faz.** O spec dá ao verificador oito tarefas. O ticket 05 cobre três: validar a nota
contra o esquema do tipo, completar o que se deduz (`type`, `initiative`, o `title` do núcleo, `updated`, o `status` a
partir do `stage`) e a "nova iniciativa". As outras quatro ficaram fora de todos os 26 tickets quando eles foram
fatiados:

- criar o `index.md` de uma pasta quando ela chega a 10 arquivos (ou guarda arquivo que a busca não lê) e manter a
  lista dele, preservando o texto livre do topo;
- conferir os links e corrigir nos dois sentidos (um link para o que não replica tem de ser `par://`, e o contrário);
- avisar quando três notas parecidas em `other/` pedem um bloco novo;
- rodar sozinho no fim de cada resposta de agente nos três harnesses: o fragmento do mod ou hook de cada um, que o kit
  de par junta depois.

**2. Como o `stage` vira o `status`.** Toda nota tem um `status` comum (rascunho, em uso ou superada). Nos tipos com
ciclo, quem escreve preenche só o `stage` e o verificador deduz o `status` por uma tabela. Você decidiu a regra
("Arquitetura de pastas", rodada 19), não a tabela. A proposta do Trilho, tipo por tipo:

| Tipo | rascunho | em uso | superada |
|---|---|---|---|
| ficha da iniciativa (`initiative.md`) | backlog | doing, on-hold, done | archived |
| pesquisa (`research/`) | open | answered | dropped |
| desenho (`design/`) | draft, proposed | approved | superseded |
| plano (`plans/`) | draft | active, done | dropped |
| entrega (`deliverables/`) | draft, review | delivered | (nenhum) |
| trabalho de agente (`work/`) | (nenhum) | open | closed |
| caso (`cases/`) | (nenhum) | open, closed | (nenhum) |
| laboratório (`labs/`) | (nenhum) | active | torn-down |

O critério dele: "em uso" é o que continua valendo como registro, mesmo terminado (iniciativa concluída, plano
cumprido, entrega feita, caso fechado). "Superada" é o que deixou de valer: arquivado, abandonado, substituído, o
`work/` fechado (um brief ou handoff já consumido) e o laboratório desmontado.

**3. `operations/` e iniciativa.** O campo `initiative` só é exigido onde o caminho mostra uma iniciativa (escolha 19,
aceita). O glossário separa `operations/` (trabalho contínuo, sem fim) das iniciativas (que terminam), e o spec deixa
em aberto se uma operação leva o núcleo de seis arquivos.

## O que mais o verificador faz, e em qual ticket
id: escopo-do-verificador
tipo: escolha
recomendada: A

- A: Um ticket novo, o 27 ("O verificador cuida das pastas: `index.md`, links `par://`, `other/` e o fim da resposta"), na etapa 1, depois do 05 e do 06, porque os links e o `local: true` do `index.md` dependem do gerador de exclusões; o 05 fica do tamanho de hoje e revisável
- B: Tudo entra no 05: um ticket só, maior, que não termina sem o 06 (a fila do Trilho para até o 06 andar)
- C: As quatro tarefas ficam para depois da construção (o hub de ensaio sai sem `index.md` automático, sem correção de links e sem o verificador no fim da resposta)

## Como o `stage` de cada tipo vira o `status` comum
id: tabela-stage-status
tipo: escolha
recomendada: A

- A: A tabela do Trilho, como está no texto acima
- B: A tabela do Trilho, mas o que terminou vira "superada": `done` (ficha e plano), `delivered` e o `closed` do caso passam de "em uso" para "superada"
- C: Outra tabela: escreva no "Algo mais?" o que muda

## O que mora em `operations/` conta como iniciativa?
id: operacao-e-iniciativa
tipo: escolha
recomendada: A

- A: Não conta: só `clients/<cliente>/<iniciativa>/` e `initiatives/<iniciativa>/` exigem `initiative`; nota em `operations/<operação>/` leva só os campos comuns, sem `initiative`
- B: Conta: `operations/<operação>/` também exige `initiative`, com o nome da operação, para filtrar por ela como se filtra por iniciativa

## Algo mais?
id: algo-mais
tipo: texto
