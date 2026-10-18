# Retomada do Lume (documentador técnico)

**2026-10-17 (depois do reinício): docs em dia com `integracao` ca62332; 6ª junção pedida ao Rebite.** Ramo `docs`
(worktree `C:/context-hub-wt/docs`) em b20bf5f: merge de ca62332 (48eb75d) e 12 commits de páginas (24, 22, 25; página
nova `componentes/prova-do-hub-inteiro.md`). Construção fechada; a caminho só o 26 (instalação nas duas máquinas).

Leia nesta ordem: `etapas/documentacao-tecnica.md` (o plano), `etapas/regras-da-construcao.md`,
`etapas/estado-documentacao.md` (feito e avisos), esta retomada.

## Fila viva

1. 6ª junção feita: `integracao` dc514db; verificador 0, 27-pastas 24/24; 12-busca pendente (espera o maestro, memória). Aguardar o 26.
2. Quando o 26 juntar (ou a cada junção nova): `git merge integracao` no docs e pôr as páginas em dia (kit de par,
   operação, pastas e links se o 26 definir `HUB_PAR_ID`, arquitetura, decisões, README).
3. Divergência avisada ao maestro: nenhum ticket define `HUB_PAR_ID` no kit (pastas e links §5).

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
