# Benefícios técnicos do Claude Code com o context hub e o Maestri

Type: research
Status: resolved

## Question

Quais são, com fonte primária, os benefícios técnicos de usar o Claude Code junto com o context hub e
o Maestri, e como cada conceito da página da Anthropic "Optimizing for cost and intelligence"
(`platform.claude.com/docs/en/about-claude/models/optimizing-for-cost-and-intelligence`) se aplica a
esse conjunto? O resultado alimenta um vídeo explicativo técnico, em inglês com legenda em pt-BR
(artifact HTML e MP4), que explica a pesquisa inteira. Pedido do Gustavo em 2026-10-10.

Escopo da pesquisa, em cinco frentes, cada uma num relatório próprio em
`exploracao/anexos/pesquisa-39-beneficios-claude-code/`:

1. **Custo e inteligência**: todos os conceitos da página da Anthropic (cache de prompt, higiene de
   tokens, tool search, Files API, ciclo de vida do contexto, Batch API, auditoria de prompts, custo por
   tarefa, upgrade de modelo, effort, reexecução de falhas, orçamentos, tempo decorrido, advisor,
   orchestrator, medição), com citação literal.
2. **Claude Code**: os recursos oficiais que concretizam esses conceitos e os que o hub e o Maestri usam
   (memória `CLAUDE.md`/`AGENTS.md`, hooks, skills, subagentes, MCP, worktrees, modo headless e SDK,
   compactação de contexto, cache de prompt no Claude Code, modelo e effort por sessão, custos,
   plugins), só na documentação oficial (`code.claude.com/docs`).
3. **Maestri**: o que é e quais conceitos oferece (canvas, agentes e terminais, notas e fichários,
   portais, rotinas, workspaces e floors, manager), segundo as skills instaladas (fonte local).
4. **Context hub**: os conceitos e decisões já fechadas nesta frente (glossário, mapa, §7.1 e §9),
   com ponteiros.
5. **Referências de vídeo**: conteúdo e linguagem visual dos três vídeos de referência (fundo preto,
   motion, transições fluidas), para o estilo do vídeo.

Regras: protocolo da §10.4 (fonte primária, citação literal, o que não foi conferido fica "não
verificado"); nada instalado nem testado além do que o Gustavo pediu (o teste do freellmapi, feito
antes de tudo: `POST /v1/audio/speech` respondeu com WAV 24 kHz pelo provedor Google).

## Comments

- 2026-10-10: ticket aberto pelo Claude a pedido do Gustavo para abrigar a pesquisa que alimenta o
  vídeo técnico. Não é uma decisão do mapa: não entra em "Decisions so far" enquanto o Gustavo não
  disser o contrário. Executores: subagentes Sonnet 5.5 (frentes 1 e 2), Haiku 5.5 (frentes 3 e 4) e
  Opus 5.5 (frente 5, um por vídeo), coordenados pelo Claude Fable 5.1.

## Answer

Pesquisa concluída em 2026-10-10. Síntese em
[`00-sintese.md`](../../../exploracao/anexos/pesquisa-39-beneficios-claude-code/00-sintese.md); relatórios por
frente na mesma pasta: `01-custo-e-inteligencia.md` (26 seções, todas as alavancas da página, preços e níveis de
effort), `02-claude-code-recursos.md` e `02b-claude-code-complementos.md` (memória, hooks, skills, subagentes,
MCP, worktrees, headless e SDK, cache, compactação, custos, modelo, effort, fast mode, plugins, settings),
`03-maestri.md` (as sete skills instaladas), `04-context-hub.md` (glossário, mapa e decisões) e os três
`05-video-*.md` (conteúdo e linguagem visual das referências).

- **Tese:** o agente paga duas vezes pelo que não lembra (qualidade e tokens). O hub fecha a primeira conta por
  mecanismo (`AGENTS.md` na raiz lido nativamente; hook `Stop` que obriga a nota de retomada; busca que devolve
  o trecho, não o arquivo); as alavancas da Anthropic fecham a segunda; o Claude Code é onde as duas se
  encontram; o Maestri é a estratégia "orquestrador" na prática.
- **Alavancas, na ordem da página, e onde caem** (tabela da síntese, §3): prompt caching automático no Claude
  Code, por máquina e diretório, com terminais no mesmo diretório lendo o cache uns dos outros; definições de
  MCP adiadas por padrão; `/clear` e `/compact` como poda, e o file-first como a poda por mecanismo; respostas
  curtas e auditoria de prompts (o `AGENTS.md` é um prompt); custo por tarefa, não por token (Opus 5.5 `medium`
  empata com Fable 5.1 a um quinto do custo); aliases de modelo e `opusplan`; effort por sessão, terminal ou
  subagente (`low` para subagentes, e nos modelos 5.5 trocar mantém o cache); refazer falhas em effort maior só
  com sinal de falha; orçamentos (`--max-budget-usd`); advisor só compensa se o executor consulta; orquestrador
  só com volume independente; medir com `/usage` e `total_cost_usd`.
- **Não verificado:** como o Maestri abre cada terminal (diretório, `--model`, `--effort`); se terminais contam
  como "agent teams"; tabela de suporte de task budgets; se o Claude Code injeta tempo decorrido; tudo o que o
  WebFetch devolveu resumido. Nada foi testado além do `POST /v1/audio/speech` do freellmapi.
- **Vídeo:** roteiro em inglês com 20 cenas e sete seções (contexto, cache, trim, modelos, effort, combinar,
  medir), legenda em pt-BR, no estilo dos três vídeos de referência (fundo quase preto, paleta semântica, rótulo
  de seção em mono, frase-síntese por seção, mockups vetoriais). Artifact e MP4 ficam fora do repositório.

Este ticket não é uma decisão do mapa e não foi registrado em "Decisions so far".
