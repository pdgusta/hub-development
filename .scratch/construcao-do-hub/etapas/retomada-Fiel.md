# Retomada do Fiel (revisor, Claude Opus 5.5) — 2026-10-17

Leia nesta ordem: `regras-da-construcao.md`, `revisao-em-dupla.md`, `estado-revisor.md` (fim), este arquivo.

## Fechados (passa)
05 r4, 01 r1, 06 r2, 14 r2, 27 r2, 29 r2. Pareceres: `01-esqueleto/parecer-Trilho.md` (05), `00-provas/parecer-Brasa.md`
(01), `01-esqueleto/parecer-Vela.md` (06), `parecer-Trilho.md` (14), `parecer-Vela.md` (27), `parecer-29-Brasa.md`.
Também 19 r1 (`parecer-19-Vela.md`). Pendente: leitura do Fielzinho no 29 r2, 07 r2 e 19 r1 (sem cota até 01:34).

## 07 r1 fechado VOLTA (parecer `etapas/02-banco/parecer-Brasa.md`); Brasa avisada. Esperando a rodada 2.

## (histórico) ticket 07 (Brasa, banco do par), rodada 1
- Ramo ticket-07, worktree `C:/context-hub-wt/ticket-07`, código em 7fa0e56 (Brasa juntou integracao 0a8e17f em e3ff419
  depois; nada dela mudou). Relatório `etapas/relatorio-07-banco-do-par.md`.
- Docker do Fiel em sequência (07-banco.test.ps1, prova01, prova02, sincronizador): logs
  `etapas/revisao-07-r1-<nome>.log` (cada um termina com `saida=N` e a lista de contêineres hub-ensaio que sobraram).
- Fielzinho propôs VOLTA (parecer-Brasa-fielzinho.md) com três achados: (1) `Get-PidSincronizador` aceita qualquer
  node no PID salvo (impede daemon; Stop mata processo alheio); (2) `Initialize-Dispositivo` aceita
  `isConfigured:true` com banco/cifra/ofuscação divergentes do env; (3) `isConfigured` gravado antes do
  `mark-resolved`: falha no meio deixa o dispositivo nunca aceito. Falta: conferir os três no código
  (`agents/code/kit/par/banco/banco.psm1`), ler os logs Docker, gravar `etapas/02-banco/parecer-Brasa.md`, avisar Brasa.

## Regras vivas
- Não rodar `ponta-a-ponta/` nem `provas/03-codex-hooks/` (até o 29 em integracao; depois só com `HUB_HARNESS_REAL=1`).
- Docker só o Fiel; um teste por vez; derrubar o que sobrar.
- maestri ask com `/`, nunca `\`.
- Ressalva aberta ao maestro: link para fora do hub (story 44) no 27.
