# Relatório do ticket 30: o montador mostra a falha do git

Construtora: Vela. Ramo `ticket-30`, worktree `C:\context-hub-wt\ticket-30`, de `integracao` f83c8f5. 2026-10-17.

## O que mudou

- `agents/code/test/hub-de-ensaio/montar.mjs` (c52ccc1): quando um comando git sai diferente de 0, ou nem abre,
  o montador imprime no stderr cinco linhas e sai 1:
  `falhou: git <args> (em <destino>)`, `saída: <código | sinal X>`, `stdout: ...`, `stderr: ...`,
  `erro: <código> <mensagem>` (o `r.error` do `spawnSync`). Antes ele imprimia só `r.stderr`; sem processo, isso
  era `undefined`.
- Testes (c52ccc1), em `agents/code/test/04-esqueleto.test.mjs`, pela linha de comando do montador:
  - PATH só com a pasta do node (sem git): nomeia `git init -q -b main` e traz `erro: ... ENOENT`.
  - `GIT_INDEX_FILE` numa pasta que não existe: nomeia `git add -A` e traz o stderr do git (`index.lock`).
  - Vermelho antes do conserto conferido nos dois (o primeiro imprimia só `undefined`).
- As 17 asserções que montam hub de ensaio (o 27-pastas e todos os outros, inclusive a ponta a ponta) mostram
  `stdout + stderr` do montador quando ele falha (03cbbb6).

## Conserto fora do ticket, com aval do maestro (ca5b389)

- `05-frontmatter.test.mjs` tinha bomba de data: dois testes gravam nota com `updated: 2026-10-16` e esperam o
  arquivo igual depois do `--corrigir`; o verificador sobe o `updated` até a data do arquivo (gravado agora). Desde a
  meia-noite de 17/10 os dois ficavam vermelhos. Agora o fixture usa a data de hoje (`toLocaleDateString('sv-SE')`,
  a mesma do verificador). Só o teste mudou.
- Varredura das outras datas fixas da suíte: as demais (12-busca, 14-guardas, 15-leitura, harness-real, 20-acervo,
  ponta a ponta) não comparam com hoje: são conteúdo de nota usado só para busca ou guarda, horários fixos de um
  cálculo puro, ou nomes de arquivo. O teste do mapa flow no 05 é recusa, sem troca. Nenhuma outra bomba.

## Sobre o vermelho intermitente da junção do 20

- O log (`juncao-20-suite-falha-27.log`) dizia "montar saiu 1, stderr vazio". Com o conserto, a próxima vez diz qual
  comando git falhou e por quê. Causa provável (não provada): o git não abriu (r.error, por exemplo falta de recurso
  com vários recrutas rodando suítes ao mesmo tempo) ou falhou sem stderr. Não reproduzi.

## Testes

- `node --test "agents/code/test/**/*.test.mjs"`: ver o fim deste relatório.
- Em 03cbbb6 (antes do conserto da data): 176 testes, 166 verdes, 2 vermelhos (a bomba de data do 05), 8 pulados.
- Em ca5b389, suíte inteira: 159 verdes, 9 vermelhos, 8 pulados. Os 9 são todos do 12-busca: "a busca não ficou
  pronta em 3 minutos" (indexação lenta, máquina com memória no limite e outros recrutas rodando). Log:
  `etapas/ticket-30-suite-falha-12.log`. O 12-busca sozinho, logo depois: 9/9. Mesma falha de tempo da junção do 15.
- Harness real: não rodado (o 30 não mexe na prova 03, nas guardas nem nos hooks).
