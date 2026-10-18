# Relatório do ticket 41: a busca não indexa `agents/code/`

Trilho, 2026-10-17. Ramo `ticket-41`, worktree `C:/context-hub-wt/ticket-41`, de `integracao` e7203b4. Commit ae102ed.

## O que se fez

- `agents/code/bin/gerar-exclusoes.mjs`: a lista da busca (`.local/exclusoes/busca.env`, `OBSIDIAN_IGNORE_PATTERNS`)
  ganha `agents/code/**`, depois dos padrões com ponto e antes das pastas locais. Só a busca: o sincronizador e o git
  seguem iguais (`agents/code/` replica e é versionado). O `iniciar.ps1` lê essa lista a cada partida; nada mais muda
  no kit.
- `agents/code/hooks/leitura/leitura.mjs` (ticket 15): página grande de `agents/code/` não recebe "busque antes" nem
  "leia o trecho": a busca nunca a aponta. Lê-se pelo caminho.
- Comentários do `iniciar.ps1` e do gerador em dia.

## Testes

- `gerar-exclusoes/gerador.test.mjs`: a lista da busca com `agents/code/**`; a política de exclusão do próprio pacote
  da busca deixa `agents/code/` de fora (vermelhos antes do conserto).
- `12-busca.test.mjs`: uma página `agents/code/docs/pagina-de-ensaio.md`, gravada antes e depois da busca subir, não
  aparece em nenhum modo de busca; o relatório conta as notas sem `agents/code/`.
- `15-leitura.test.mjs`: caso novo, página grande de `agents/code/docs/` lida inteira sem aviso.
- Leves 56/56 (`logs/trilho-41-leves.log`): 15-leitura, gerador, 16-vigia e 17-vigia-tela (usam o gerador).
- **12-busca com os docs do Lume juntados** (worktree provisória `ticket-41-docs`: o ramo do 41 com
  `git merge --no-commit docs`, 14 páginas em `agents/code/docs/`; desfeita depois), com a trava passada pela Vela:
  9/9, busca pronta em 50 s, indexação 38 s, 50 notas indexadas (`logs/trilho-41-12-busca-com-docs.log`). Antes: o
  prazo de 3 min estourava com os docs (67 notas, ~9 min estimados). O "1 errors" da indexação é a nota de cabeçalho
  quebrado que o teste grava de propósito. Nenhuma pasta `hub-ensaio-12-*` nova sobrou.

## Rodada 2 (parecer r1), 6a728a4

- `agents/skills/busca/SKILL.md`, "Fica fora da busca, de propósito": cita `agents/code/` (código, kit, testes e
  `agents/code/docs/`), lido pelo caminho. Só o corpo; cabeçalho intacto. O 12-busca desta ponta fica para a junção
  (maestro); com os docs já deu 9/9. Merge da integracao c42ffa0 (38 e 39) em 8497eb7, limpo; leves 58/58
  (`logs/trilho-41-leves-2.log`).
