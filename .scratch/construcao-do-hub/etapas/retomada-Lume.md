# Retomada do Lume (documentador técnico)

**2026-10-21: docs em dia com `integracao` 35da1e6 (49 e 50); 8ª junção pedida ao Rebite.** Ramo `docs` (worktree
`C:/context-hub-wt/docs`) em 4219de9: `instalacao.md` reescrita com o caminho do par B (hub vazio, git depois),
banco do par, gerador de exclusões, decisões, README. A caminho: 51 (acentos da notificação da vigia), 52 (tarefa
`hub-sincronizador` com o pwsh que o Agendador acha: pôr em dia `instalacao.md` §12 e `banco-do-par.md`), o 26.

Leia nesta ordem: `etapas/documentacao-tecnica.md` (o plano), `etapas/regras-da-construcao.md`,
`etapas/estado-documentacao.md` (feito e avisos), esta retomada.

## Fila viva

1. 8ª junção pedida (docs 4219de9): esperar o Rebite.
2. Quando o 51 e o 52 juntarem: `git merge integracao` no docs; o 52 muda o XML do laço (`instalacao.md` §12, tirar o
   achado; `banco-do-par.md` §3 e §7); o 51, a vigia (`vigia.md`).
3. O 26 (par B): pôr em dia `instalacao.md` com o que a instalação do B ensinar.

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
