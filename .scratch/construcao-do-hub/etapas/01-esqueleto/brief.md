# Etapa 1: esqueleto, contrato e frontmatter (brief do maestro, 2026-10-16)

Leia antes `..\regras-da-construcao.md`. Decidido na rodada `2026-10-16-etapa-0-receita`: esta etapa é **adiantada em
paralelo** com a etapa zero, porque não depende das provas. Se uma prova mudar algo seu (por exemplo, a exclusão de
pastas com ponto, que o gerador de exclusões desta etapa alimenta), o maestro avisa e você ajusta antes de juntar.

## O que construir

O bloco do **Worker 1** no `spec.md` e a faixa 1 em `spec-partes\faixas-01-02.md`, com as decisões do ticket 12
(arquitetura de pastas e frontmatter). Em resumo: a árvore das seis raízes, o `AGENTS.md` da raiz (com o bloco
`cabeca:inicio/fim`), os esquemas de frontmatter por tipo em `agents/frontmatter/`, o verificador sem IA, o script
"nova iniciativa" (sem criar o `AGENTS.md` da iniciativa: ele nasce à mão, decisão de 2026-10-16), o gerador de
exclusões (`local: true` e o que tem ponto) e **o hub de ensaio**, que é entrega desta etapa e base de todas as outras.

Ramos: um por ticket (`ticket-04`, depois `ticket-05` e `ticket-06`). Tickets: `issues\04-esqueleto-do-hub-e-hub-de-ensaio.md`, `05-frontmatter-imposto.md` e
`06-gerador-de-exclusoes.md` (o 06 espera a prova 02). Pode consultar o
ramo `tentativa-paralela/faixa-01` (dois commits parciais de 2026-10-15, escritos contra o spec antigo).

## Relatório

`C:\Projetos\context-hub\.scratch\construcao-do-hub\etapas\01-esqueleto\relatorio.md`: o que foi entregue, como provar
(os comandos dos testes), o que ficou de fora e por quê, e o que as próximas etapas precisam saber (nomes, assinatura
do verificador, caminho do hub de ensaio).
