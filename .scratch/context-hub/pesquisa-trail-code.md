# Pesquisa: Trail-Code (trailhq/Trail-Code)

Feita pelo maestro em 2026-10-17 ~09h45, a pedido do Gustavo ("acho que esse sim pode nos ajudar"). Fonte primária: o
README do repositório (`https://github.com/trailhq/Trail-Code`, ramo `main`, lido por curl em 2026-10-17) e a API do
GitHub. Leitura do README só; código não lido, nada instalado. Onde digo "não verificado", é o que o README afirma sem
eu ter conferido.

## O que é

"The self-learning context layer for coding agents" (README, topo). MIT, TypeScript, Node; ~10,3 mil estrelas, criado
em 2026-07-03, ativo (último push 2026-10-17). Nome antigo: graft (`@nanonets/graft`), hoje `@trailhq/trail-code`.
Duas partes, as duas locais (README, "How it works"):

1. **Mapa do código (graft map):** `trail init` lê o repositório com tree-sitter e monta um grafo de arquivos, funções e
   quem chama quem; sem modelo e sem chave; atualiza sozinho com a árvore de trabalho. O agente recebe ponteiros para
   os arquivos certos a cada prompt e o "blast radius" depois de editar.
2. **Learnings:** o que o agente e a equipe aprenderam, gravado como arquivo Markdown com frontmatter em
   `.trail/learnings/` (no repositório, versionado) ou `~/.trail/` (pessoal). Quatro tipos: decisões, preferências,
   skills e guardrails (estes dois "soon"). O arquivo traz `## Decided`, `## Tried and ruled out`, `## Watch out` e um
   `touches:` com os arquivos a que se refere (README, "A learning is a file").

Números do README (não verificados): SWE-bench Verified 33/50 com o mapa contra 27/50 sem, com 23% menos tokens; 32%
menos custo e 60% menos tempo em 162 rodadas.

## Onde encosta no hub

- **É sobre repositório de código; o hub é sobre contexto.** Os repositórios de código das iniciativas moram fora do
  hub (decisão de 2026-10-16). O Trail-Code serve exatamente a eles: mapa do código e decisões presas ao código.
  Complementa o hub; não o substitui.
- **Ideias que o hub pode copiar** (para depois da construção, não agora):
  - o formato da decisão: **Decidido / Tentado e descartado / Cuidado**, com `touches:` apontando o que ela cobre;
  - "**nunca reescreve** uma decisão: quando vai contra uma, diz por quê e grava outra" (README, "Your agent does the
    saving"), parecido com o nosso `status: superada`;
  - `trail init` lê as mensagens do próprio usuário nas sessões passadas do Claude Code e guarda **o que foi dito em
    duas ou mais sessões** (tira segredos, deixa de fora saída de ferramenta e texto colado). Serviria ao acervo e às
    memórias de feedback;
  - `trail check` antes do PR compara a mudança com as decisões e cita quem decidiu e por quê. É o mesmo papel do nosso
    verificador, mas para código;
  - pedir ao agente, **uma vez por sessão**, que grave o que descobriu depois de um turno de "trabalho de verdade".

## Riscos para a nossa construção

- **Escreve fora do repositório** (README, "Writes outside the repo"): hooks `SessionStart`, `UserPromptSubmit`,
  `PostToolUse` e `Stop` em `~/.claude/settings.json`, servidor MCP em `~/.claude.json`, `~/.codex/config.toml` e
  `~/.codex/hooks.json`, e um `statusLine` no projeto. Diz que junta sem apagar o que existe e que `--no-global` e
  `--dry-run` existem. Isso esbarra no kit de par (ticket 23), que compõe os mesmos arquivos e o mesmo fim de turno; e
  um `statusLine` de projeto esconde o do usuário (o próprio README avisa).
- **Telemetria anônima ligada por padrão**; desliga com `trail telemetry disable` ou `DO_NOT_TRACK=1` (README).
- `trail init` em terminal lê o histórico de sessões e as revisões dos 50 últimos PRs pelo `gh`, com o login do
  usuário; o texto vai à Anthropic pelo Claude Code do usuário (README, "What stays on your machine"). Com dado de
  cliente nos repositórios, isso pede cuidado.

## Recomendação do maestro

Não mexer na construção em curso (mudaria o kit no meio). Depois do 25: um ensaio do Trail-Code num repositório de
código de iniciativa, com `--dry-run` primeiro, `--no-global` e `DO_NOT_TRACK=1`, para ver (1) se o mapa ajuda os
agentes no código das iniciativas e (2) como os hooks globais dele convivem com os do kit. As ideias do formato de
decisão entram como proposta para o acervo e os esquemas de frontmatter, numa rodada com o Gustavo.

## Decisão do Gustavo (2026-10-17 ~09h50)

Aceita: fica para depois do 25, no radar. Nada muda na construção em curso.
