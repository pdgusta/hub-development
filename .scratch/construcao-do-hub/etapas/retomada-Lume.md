# Retomada do Lume (documentador técnico)

**2026-10-18: docs em dia com `integracao` 8c01cfb (45 e 46); 7ª junção feita (`integracao` 7b6c406, `main` fe55b12); terminal fechado pelo maestro até 2026-10-19.** Ramo `docs` (worktree
`C:/context-hub-wt/docs`) em e33b71f: merge fast-forward de 8c01cfb e 8 commits (banco do par, kit de par, pastas e
links + fim + roteamento, operação + stack, **página nova `instalacao.md`**, arquitetura, decisões, README). `main` do
hub em 7d0c25d. A caminho só o 26 (instalação de verdade, com o Gustavo).

Leia nesta ordem: `etapas/documentacao-tecnica.md` (o plano), `etapas/regras-da-construcao.md`,
`etapas/estado-documentacao.md` (feito e avisos), esta retomada.

## Fila viva

1. 7ª junção feita: `integracao` 7b6c406, `main` fe55b12 (Rebite). Aguardar o 26.
2. Avisos ao maestro (2026-10-18), anotados na `instalacao.md`: fork em `C:/Projetos/hub-mcp-banco` no ramo
   `ticket-09`, fora de `integracao`; `HUB_MCP_BANCO_TOKEN` sem script que o ponha no ambiente; B com o clone no disco
   não provado. A divergência do `HUB_PAR_ID` fechou com o 46.
3. Quando o 26 andar (ou ticket novo juntar): `git merge integracao` no docs e pôr em dia `instalacao.md` com o que o
   26 aprender, e as páginas tocadas.

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
