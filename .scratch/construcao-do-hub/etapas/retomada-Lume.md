# Retomada do Lume (documentador técnico)

**2026-10-17 ~20h45: construção fechada; os docs estão atrás da `integracao`.** Todos os tickets resolvidos, menos o
26 (instalação de verdade, com o Gustavo). `integracao` em ca62332. Ramo `docs` (worktree `C:/context-hub-wt/docs`)
em a71e407: 4 páginas sobre f640bbd (pastas-e-links, mcp-do-banco, decisões, README, pelo 44) ainda **não juntadas**;
a `integracao` andou depois de f640bbd e **não** está no `docs`.

Leia nesta ordem: `etapas/documentacao-tecnica.md` (o plano), `etapas/regras-da-construcao.md`,
`etapas/estado-documentacao.md` (feito e avisos), esta retomada.

## Fila viva

1. `git -C C:/context-hub log --oneline f640bbd..integracao` e `git -C C:/context-hub-wt/docs merge integracao`.
   Juntados desde f640bbd (conferido no log): 24 (a4fa7e3), evidência do Codex do 22 (56cd23a), 25 (ca62332).
2. Pôr as páginas em dia, uma por commit, com a linha do topo no hash novo:
   - **24:** `componentes/kit-de-par.md`, `operacao.md`, `HUB_PAR_ID` na §5 de `componentes/pastas-e-links.md`.
   - **22 (evidência do Codex):** `componentes/proxy-e-kit-de-cliente.md` (o Codex como cliente deixa de ser "não
     verificado": PASSA com `gpt-6-luna`, janela quieta 17:19; ressalva: o `lido.json` não grava o modelo),
     `componentes/infraestrutura-de-teste.md` se tocar.
   - **25:** prova do hub de ensaio inteiro (relatório `etapas/relatorio-25-hub-inteiro.md`); par novo leva minutos
     para receber o hub (o subir espera o B convergir, fc6b10c).
   - Depois: decisões, arquitetura e README (estado e mapa).
3. `node agents/code/bin/verificar-pastas.mjs --raiz . agents/code/docs` na raiz do docs (rc 0).
4. Pedir a 6ª junção ao Rebite (molde abaixo) e conferir com `maestri check "Rebite"`.

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
