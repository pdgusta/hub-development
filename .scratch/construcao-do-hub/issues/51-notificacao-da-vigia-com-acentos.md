# 51: A notificação da vigia chega com os acentos certos

Type: task
Status: resolved
Etapa: conserto do 26 (fora da sequência)
Blocked by: nenhum

**What to build:** Achado do Gustavo em 2026-10-21 (print da notificação do Windows): "replica├º├úo", "h├í",
"m├íquina". O `notificar()` de `agents/skills/vigia/vigia.mjs` manda o texto em UTF-8 pela entrada padrão ao
`powershell` 5.1 (`notificar.ps1`), que lê `$input` na página do console (OEM 850). Hipótese, a confirmar com teste
antes do conserto: é essa a quebra. Consertar para que título e corpo cheguem ao toast com os acentos certos, sem mudar
o contrato `HUB_VIGIA_NOTIFICAR` (texto na entrada padrão).

- [x] teste que falha antes: texto com acentos passa pelo `notificar.ps1` (ou pela parte que lê a entrada) e sai igual
- [x] conserto; o mesmo teste verde
- [ ] a suíte segue verde

## Comments

- 2026-10-21 (maestro): publicado. Dona: a Brasa. Revisão: o Fiel.
- 2026-10-21 (Brasa): feito no ramo `ticket-51` (02f026c, 16b0715). A hipótese se confirmou no teste (antes:
  "replica├º├úo parada h├í"). O notificar.ps1 lê os bytes da entrada em UTF-8; `-Xml` para o teste. Testes leves 41/41.
  Relatório: `etapas/relatorio-51-notificacao-com-acentos.md`. Pedida a revisão ao Fiel.
- 2026-10-21 (Brasa): r1 do Fiel (VOLTA) consertada em fe8be14: o documento em `$doc` (o `$xml` era o `-Xml`), o
  `-Xml` depois do `LoadXml` (teste vermelho com o defeito, verde com o conserto), erro com código diferente de zero.
  `integracao` juntada (4b05241). Leves 41/41. Pedida a r2.
- 2026-10-21 (Brasa): r2 do Fiel PASSA (parecer `etapas/parecer-51-Brasa.md`, seção r2). Pronto para o Rebite: ramo
  `ticket-51` (fe8be14), leves 41/41.
- 2026-10-21 12:49 (integrador, Rebite): resolvido. Junção 30564d3 (ticket-51 fe8be14; parecer do Fiel r2 PASSA em
  acordo). Leves 16, 17, 51 (com os do 52): 69/69. Suíte com --test-concurrency=1 e trava em b506910 (51+52): 391,
  376 verdes, 15 pulados, 0 falhas, git limpo (log etapas/logs/juncao-51-52-suite.log). Toast de verdade não repetido.
