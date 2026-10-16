# Cartographer: o que é e se serve à construção (2026-10-16)

Pedido do Gustavo: "pesquise como o plugin cartographer pode ajudar na execução e se podemos instalá-lo agora".
Fonte primária: README do repositório `kingbootoshi/cartographer` (raw do GitHub, ramo `main`) e a API do GitHub
(772 estrelas, último push 2026-05-13, não arquivado; a API não reconhece licença, o README diz MIT).

## O que é, nas palavras do autor

"A standalone Cartographer CLI plus Claude Code plugin for mapping and navigating codebases." São duas coisas:

1. **Plugin do Claude Code (o fluxo antigo, "legacy"):** `/cartographer` "orchestrates multiple Sonnet subagents to
   analyze your entire codebase in parallel", gera `docs/CODEBASE_MAP.md` e "Updates `CLAUDE.md` with a summary pointing
   to the map". Avisa: "this can use significant tokens". Pede `tiktoken`. Instala por `/plugin marketplace add
   kingbootoshi/cartographer` e `/plugin install cartographer`.
2. **CLI v2 (Bun) com MCP stdio:** "index a repo into a local SQLite graph, compile bounded briefs, run
   removal/completeness audits, manage evidence-backed notes, and score whether agents used graph context before
   editing". Grava em `.cartographer/`. O `brief` "emit bounded agent-facing context around a path, package, symbol...
   or changed files"; o `verify --fresh` falha quando o grafo fica velho. O autor recomenda a v2 para "new
   agent/orchestrator workflows".

## Relação com a construção

- **Onde ajudaria:** com etapas sequenciais, o agente de cada etapa precisa saber o que as anteriores construíram. O
  `brief` da v2 dá esse contexto limitado por caminho ou pelos arquivos mudados, sem reler o repositório inteiro; o
  `verify --fresh` mostra se o mapa ficou velho. O valor cresce com o código: hoje `C:\context-hub` só tem o "Início do
  hub".
- **Choques com decisões fechadas:**
  - O plugin escreve `CLAUDE.md`; "Portas de entrada do hub" decidiu que o hub não tem `CLAUDE.md` (e um `CLAUDE.md`
    acima desliga os `AGENTS.md`, pelos testes das portas de entrada).
  - O plugin espalha subagentes Sonnet: contra o trabalho visível no canvas que o Gustavo pediu hoje, e gasta cota do
    Claude.
  - Instalar plugin no escopo do usuário é mudança global; o roteamento de skills deixou global só o que é de uso geral.
- **Não verificado:** suporte a Windows (o README não fala; os evals citam caminhos do macOS do autor); se o plugin
  instala só no projeto.
- **Nesta máquina:** Node e `tiktoken` 0.14.0 instalados; Bun não.

## Conclusão do maestro

Dá para instalar agora, mas não compensa: o repositório do hub ainda está quase vazio, e o plugin fere duas decisões
fechadas. O caminho que faz sentido é a **CLI v2**, testada no repositório do hub entre uma etapa e outra da construção,
quando houver código; pede Bun e um teste no Windows. Fica no radar com esse gatilho, até o Gustavo decidir.
