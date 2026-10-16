# Proposta do plano de construção em etapas (maestro, 2026-10-16)

Base: a ideia do Gustavo ("encarar cada worker como uma etapa sequencial e eu te digo como executar cada etapa, mas
ajustemos isso", ticket 16, 2026-10-16), o spec revisto (`spec.md`, com as 23 escolhas aceitas), a nota do núcleo "Se
cada faixa virar uma etapa sequencial" e as lições dos revisores (`revisao/licoes/`).

## Por que essa ordem

Cada etapa usa a entrega **real** da anterior; dublê só onde o real exige a segunda máquina (nota do núcleo). A ordem
segue o que cada faixa pede das outras na seção "Como segue sem esperar as outras faixas" do `spec.md`:

| Etapa | Faixa | O que entrega | Usa de verdade |
|---|---|---|---|
| 0 | provas de risco | testa o que é "não verificado" e pode derrubar o desenho (lições do Prisma): replicação de dois CouchDB com os documentos do LiveSync; `.livesync/ignore` com pastas com ponto aninhadas; hooks do Codex em acesso total | nada |
| 1 | 1. esqueleto, contrato e frontmatter | a árvore, o `AGENTS.md`, os esquemas, o verificador e o hub de ensaio | nada |
| 2 | 4. banco e vista `.md` | os dois CouchDB de ensaio, o LiveSync e a vista | o hub de ensaio |
| 3 | 5. MCP do banco com versão | o fork com versão, conflito visível, três instâncias, estado do hub | o banco |
| 4 | 3. busca | a busca local e o aceite | o hub de ensaio |
| 5 | 6. guardas de gravação no disco | os hooks que recusam e avisam | o verificador, a busca, o MCP do banco |
| 6 | 7. vigia e divergência | a vigia, o estado, os avisos | o banco, o MCP (reserva da checagem) |
| 7 | 2. retomada e checkpoint | os hooks de início e de fim | o contrato, o estado da vigia, o MCP |
| 8 | 9. skills e acervo do maestro | o roteamento, a família `maestro-*`, a guarda do acervo | o hub de ensaio |
| 9 | 10. manutenção e kit de cliente | arquivar, cópia diária, proxy e kit de cliente | a busca, o MCP, a vigia, o banco |
| 10 | 8. portas dos harnesses e kit de par | o kit que liga tudo nos três harnesses | os fragmentos de todas as etapas |
| 11 | junção | juntar e provar o hub de ensaio inteiro | tudo |

Uma etapa só começa quando a anterior passou na revisão e foi juntada em `integracao`.

**Onde a ordem não fecha sozinha** (achados da Aquarela ao conferir o spec, 2026-10-16): vai com exemplo e troca pelo
real depois, sem mudar a ordem.

- O MCP do banco (etapa 3) e a vigia (etapa 6) se pedem: a ferramenta de estado do MCP devolve o estado da vigia, e a
  vigia usa o MCP como reserva da checagem. A etapa 3 usa um `estado.json` de exemplo no esquema da vigia (spec, Worker
  5); a etapa 6 usa o MCP de verdade e confere a ferramenta com o estado real.
- A vigia (etapa 6) lê o item da cópia diária, que só a manutenção (etapa 9) grava: a etapa 6 testa com um item de
  exemplo; a etapa 9 confere que a vigia lê o item real.
- O hub de ensaio é entrega da etapa 1 (o spec antigo dizia que o maestro o entregava antes da hora).
- As URLs dos MCP: cada etapa escreve os seus nomes no `.env.modelo`; o kit de par (etapa 10) só os junta, e o proxy
  da etapa 9 já lê do `.env.modelo`.

## Os ramos de ontem

Em `C:\context-hub`: commits parciais só em `faixa-01` (2), `02`, `03`, `07` e `09`, nenhum com teste de ponta a ponta
verde, escritos contra o spec antigo. Proposta: guardar como referência (renomear para `ontem/faixa-NN` e tirar as
worktrees), e cada etapa recomeça da ponta de `integracao`, podendo consultar o ramo de ontem.

## O que fica para depois desta rodada

As perguntas que dependem de cada etapa vão na hora da etapa: login dos harnesses no HOME de ensaio (etapas 7 e 10),
pilotos do vault (etapa 1), teste do gemini (etapa 4), bancos de ensaio no Docker (etapas 0, 2, 3 e 6), e as três
lacunas de dono (etapa 8: registro do aval de mudança no contrato, modelo do verificador da guarda, erro de peça que
sumiu).

## Decidido na rodada `2026-10-16-plano-de-construcao-r1` (Gustavo, 18:32)

- Ordem aceita, com **paralelismo de até 3 agentes**: além da etapa em curso, até 2 agentes adiantam o que não depende
  das etapas anteriores. Exemplos pela tabela: a busca (etapa 4) e as skills e o acervo (etapa 8) só usam o hub de
  ensaio, então podem andar logo depois da etapa 1, junto com o banco e o MCP.
- Etapa zero sim, prevendo as dificuldades de ligar o testado ao resultado final.
- Ramos de ontem em `tentativa-paralela/faixa-NN`.
- Antes de cada etapa, o maestro propõe a receita pelo resultado da anterior e conta o que já foi antecipado.
