# Retomada do Cinzel (construtor)

**2026-10-17 ~23h25: nada pendente do Cinzel.** Ticket 46 (kit de par para duas máquinas) passou na revisão (Fiel r2,
dc4fd1a); ramo `ticket-46` em dd241ba (com `integracao` 6494a38, o 45, juntada; leves 117/117,
`logs/46-testes-juncao.log`). O Rebite junta depois da suíte do 45 (~23h35). Retomada anterior:
`logs/retomada-Cinzel-antes-46.md`.

## O 46, em uma linha cada

- `HUB_PAR_ID`: o passo 08 grava `<hub>/.local/par.json`; `bin/lib/par.mjs` (variável primeiro, arquivo de reserva).
- `lerEnv` do 08 e da espera: valor vazio não apaga o que já veio (conserto da r1: o modelo vazio apagava o id do 45).
- Passo `espera` (`kit/par/espera.mjs`, `-PrazoEspera`): leitor da vigia contra o disco + `changes_pending` do outro
  par; sai 0 sempre. Prova com Docker: `test/46-espera-banco.test.ps1` (6 PASSA; B convergiu em 315 s, 566 arquivos).
- Passo opcional `proxy`; chave `a_mao` e linhas `à mão:` na saída do kit.
- Para o 26: `HUB_MAQUINA` = `HUB_PAR_ID`; registro de uso passa a `<id>.md`; docs (operacao.md, pastas-e-links.md)
  ainda dizem que o kit não define o id nem espera: aviso ao Lume na junção, pelo maestro.

## Lições práticas

- `%TEMP%` é curto (`GUSTAV~1.DEL`): `TEMP`/`TMP` = `C:/Users/gustavo.delfino/AppData/Local/Temp` nos testes.
- Texto com `\` por python em heredoc vira escape (`\t` virou tabulação no 46): Edit ou raw string; depois `grep -P "\t"`.
- Saída de node dentro de pwsh: `$x = & node ...` só aparece no fim; para progresso, `| ForEach-Object`.
- `maestri ask` sem barra invertida nos caminhos; em segundo plano.
- Conferir a ponta de `integracao` antes de avisar o Rebite (no 46 ela andou entre o passa e o aviso).

## Como retomar

1. Ler `etapas/regras-da-construcao.md` (inteiras).
2. Aguardar ordem do maestro. Não pegar ticket nem trava por conta.
