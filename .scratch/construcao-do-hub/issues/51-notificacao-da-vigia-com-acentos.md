# 51: A notificação da vigia chega com os acentos certos

Type: task
Status: ready-for-agent
Etapa: conserto do 26 (fora da sequência)
Blocked by: nenhum

**What to build:** Achado do Gustavo em 2026-10-21 (print da notificação do Windows): "replica├º├úo", "h├í",
"m├íquina". O `notificar()` de `agents/skills/vigia/vigia.mjs` manda o texto em UTF-8 pela entrada padrão ao
`powershell` 5.1 (`notificar.ps1`), que lê `$input` na página do console (OEM 850). Hipótese, a confirmar com teste
antes do conserto: é essa a quebra. Consertar para que título e corpo cheguem ao toast com os acentos certos, sem mudar
o contrato `HUB_VIGIA_NOTIFICAR` (texto na entrada padrão).

- [ ] teste que falha antes: texto com acentos passa pelo `notificar.ps1` (ou pela parte que lê a entrada) e sai igual
- [ ] conserto; o mesmo teste verde
- [ ] a suíte segue verde

## Comments

- 2026-10-21 (maestro): publicado. Dona: a Brasa. Revisão: o Fiel.
