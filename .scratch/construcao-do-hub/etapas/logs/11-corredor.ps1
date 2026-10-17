# Corredor do Cinzel (ticket 11): pega a trava, roda o aceite com os harnesses de verdade (uma rodada por vez) e solta
# a trava ao fim, também quando falha. Estado em 11-corredor.status; log em 11-harness-<n>.log.
# Uso: pwsh -NoProfile -File etapas/logs/11-corredor.ps1 [-Rodadas claude,codex,copilot-sem,copilot-com]
param([string]$Rodadas = 'claude,codex,copilot-sem,copilot-com')
$ErrorActionPreference = 'Stop'
$etapas = 'C:\Projetos\context-hub\.scratch\construcao-do-hub\etapas'
$trava = Join-Path $etapas 'trava-pesada.md'
$status = Join-Path $etapas 'logs\11-corredor.status'
$wt = 'C:\context-hub-wt\ticket-11'
if (Test-Path $trava) { "trava ocupada: $(Get-Content -Raw $trava)" | Add-Content $status; exit 2 }
"- Cinzel (construtor), $(Get-Date -Format 'yyyy-MM-dd HH:mm'): ticket 11, harness real ($Rodadas), uma sessão por vez, worktree ticket-11; corredor PID $PID. Apago ao fim." |
    Set-Content -Encoding utf8NoBOM $trava
try {
    $n = 1; while (Test-Path (Join-Path $etapas "logs\11-harness-$n.log")) { $n++ }
    $log = Join-Path $etapas "logs\11-harness-$n.log"
    "rodando $Rodadas (log 11-harness-$n.log, $(Get-Date -Format HH:mm:ss))" | Add-Content $status
    $env:HUB_HARNESS_REAL = '1'
    $env:HUB_MCP_BANCO_DIR = 'C:\Projetos\hub-mcp-banco-wt\ticket-11'
    $env:RODADAS = $Rodadas
    Push-Location $wt
    try { & node --test --test-concurrency=1 agents/code/test/ponta-a-ponta/11-mcp-banco.test.mjs *> $log } finally { Pop-Location }
    "código $LASTEXITCODE ($(Get-Date -Format HH:mm:ss))" | Add-Content $status
}
finally {
    Remove-Item $trava -ErrorAction SilentlyContinue
    "trava solta $(Get-Date -Format HH:mm:ss)" | Add-Content $status
}
