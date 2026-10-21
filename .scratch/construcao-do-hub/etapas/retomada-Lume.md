# Retomada do Lume (documentador técnico)

**2026-10-21: docs em dia com `integracao` b506910 (49 a 52); 9ª junção feita (`integracao` b2ae3db, `main` 70a9f73).** Ramo `docs` (worktree
`C:/context-hub-wt/docs`) em 1820326. A caminho: o 26 (par B; e no par A, a reaplicação da tarefa do 52).

Leia nesta ordem: `etapas/documentacao-tecnica.md` (o plano), `etapas/regras-da-construcao.md`,
`etapas/estado-documentacao.md` (feito e avisos), esta retomada.

## Fila viva

1. 9ª junção feita: `integracao` b2ae3db, `main` 70a9f73. Nada pendente.
2. O 26 (par B, e o `LastTaskResult` 0 da reaplicação no par A): pôr em dia `instalacao.md` com o que se aprender.

## Molde e regras do papel

- Topo: `# <título>` e "Conferido em `integracao` <hash> (data)." As 9 seções do plano (para que serve, onde mora,
  como funciona, interfaces, configuração, decisões e porquês, limites, testes leve x PESADO, armadilhas).
- Só o conferido; "não verificado" quando não deu. Páginas sem frontmatter (o verificador ignora `agents/code/**`).
- Commit: `docs: página de <peça> (<tickets>)` + `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`.
- Só leitura e comando leve; nunca teste pesado, Docker, harness real ou trava. Não muda código nem ticket.
- Divergência: anotar na página e avisar o maestro numa linha (`maestri ask "Claude Code" "..."`, caminhos com `/`).
- Fontes: código em `C:/context-hub-wt/docs`; fork em `C:/Projetos/hub-mcp-banco-wt/integracao` (só leitura);
  `etapas/relatorio-NN-*`, `parecer-NN-*`, `issues/NN-*`, `registro-de-juncoes.md`. Decisões do Gustavo em
  `.scratch/context-hub/issues/` ("ticket de decisão N", não confundir com o de construção de mesmo número).
- Pedido de junção: `maestri ask "Rebite" "Lume: 6ª junção dos docs. Ramo docs (worktree C:/context-hub-wt/docs),
  ponta <hash>, integracao <hash> contida. Diff só em agents/code/docs/ (páginas: ...). Plano: conferir o diff, rodar
  12-busca.test.mjs e o verificador de frontmatter; sem suíte, sem revisão."`

## Lições práticas

- Script Python com `\`: gravar o script num arquivo do scratchpad e usar `chr(92)` (heredoc perde a barra).
- `grep` com `.env` no padrão é barrado pela guarda de segredos.
- `verificar-pastas` roda da raiz do docs com `--raiz .`.
- `maestri ask` pode sair com 124 com o recado na fila: conferir com `maestri check`.
- Desde o 44, link `[texto](alvo)` e `../` dentro de código são permitidos nas páginas.

## Como retomar

Ler os arquivos acima e aguardar a ordem do maestro para seguir a fila viva (o Windows reinicia às 21h; nada a meio
caminho sem commit).
