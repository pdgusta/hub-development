# Corredor do Cinzel (ticket 10): pega a trava, roda o Docker do 10 e o do 09 (com o fork da worktree ticket-10),
# um por vez, e solta a trava ao fim, também quando falha. Estado em 10-corredor.status.
param([string[]]$Testes = @('10', '09'))
$ErrorActionPreference = 'Stop'
$etapas = 'C:\Projetos\context-hub\.scratch\construcao-do-hub\etapas'
$trava = Join-Path $etapas 'trava-pesada.md'
$status = Join-Path $etapas 'logs\10-corredor.status'
$wt = 'C:\context-hub-wt\ticket-10'
$env:HUB_MCP_BANCO_DIR = 'C:\Projetos\hub-mcp-banco-wt\ticket-10'
if (Test-Path $trava) { "trava ocupada: $(Get-Content -Raw $trava)" | Set-Content $status; exit 2 }
"- Cinzel (construtor), $(Get-Date -Format 'yyyy-MM-dd HH:mm'): ticket 10, Docker de $($Testes -join ' e ') (hub-ensaio-<NN>-a/b, 5996/5997), worktree ticket-10; corredor PID $PID. Apago ao fim." |
    Set-Content -Encoding utf8NoBOM $trava
try {
    $n = 1; while (Test-Path (Join-Path $etapas "logs\10-docker-$n.log")) { $n++ }
    foreach ($t in $Testes) {
        "rodando $t (log 10-docker-$n.log, $(Get-Date -Format HH:mm:ss))" | Add-Content $status
        $log = Join-Path $etapas "logs\10-docker-$n.log"
        "# $t-mcp-banco.test.ps1, fork $env:HUB_MCP_BANCO_DIR, $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" | Set-Content $log
        & pwsh -NoProfile -File (Join-Path $wt "agents\code\test\$t-mcp-banco.test.ps1") *>> $log
        "${t}: código $LASTEXITCODE ($(Get-Date -Format HH:mm:ss))" | Add-Content $status
        $n++
    }
}
finally {
    Remove-Item $trava -ErrorAction SilentlyContinue
    "trava solta $(Get-Date -Format HH:mm:ss); contêineres: $(docker ps -a --filter 'name=hub-ensaio-' --format '{{.Names}}')" | Add-Content $status
}
