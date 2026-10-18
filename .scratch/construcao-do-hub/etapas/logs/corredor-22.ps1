# Corredor destacado do ticket 22, com a trava (etapas/trava-pesada.md) e as guardas de memória do 08: sai se a trava
# estiver ocupada; piso de 2 GB livres antes de cada fase (20 min sem chegar: para); abaixo de 700 MB durante uma fase,
# corta e limpa. Fases: (1) 22-proxy.test.ps1 -Manter; (2) se verde, os três harnesses como cliente; no fim, desce a
# pilha (.local/limpar-22.ps1) e solta a trava. Estado em etapas/logs/22.status; logs em etapas/logs/22-*.log.
# Uso: Start-Process pwsh -WindowStyle Hidden -ArgumentList '-NoProfile','-File','C:/context-hub-wt/ticket-22/.local/corredor-22.ps1'
param([switch]$SoDocker, [switch]$Wsl, [string]$Harnesses = 'claude,codex,copilot')   # -Harnesses codex: só o Codex
$ErrorActionPreference = 'Stop'
$wt = 'C:\context-hub-wt\ticket-22'
$etapas = 'C:\Projetos\context-hub\.scratch\construcao-do-hub\etapas'
$trava = Join-Path $etapas 'trava-pesada.md'
$logs = Join-Path $etapas 'logs'
$status = Join-Path $logs '22.status'
function Nota([string]$t) { "$(Get-Date -Format 'HH:mm:ss') $t" | Add-Content -Encoding utf8NoBOM $status }
function Livre { [math]::Round((Get-CimInstance Win32_OperatingSystem).FreePhysicalMemory / 1KB) }
function Get-Arvore([int]$id) { $id; Get-CimInstance Win32_Process -Filter "ParentProcessId=$id" | ForEach-Object { Get-Arvore $_.ProcessId } }

Nota "corredor $PID começou$(if ($SoDocker) { ' (só Docker)' })"
try {
    $f = [IO.File]::Open($trava, 'CreateNew', 'Write')
    $b = [Text.UTF8Encoding]::new($false).GetBytes("- Brasa (construtora), 2026-10-17 $(Get-Date -Format HH:mm): ticket 22, Docker do proxy (hub-ensaio-22-a/b, 5996/5997, MCP 8796-8798) e os três harnesses como cliente; corredor destacado PID $PID. Apago ao fim.`n")
    $f.Write($b, 0, $b.Length); $f.Close()
} catch [IO.IOException] { Nota 'trava ocupada: saio sem esperar'; exit 5 }
Nota 'PEGOU a trava'

# Aval do maestro (08h30): com a trava e nenhum contêiner rodando, wsl --shutdown devolve a memória da VM do Docker;
# espera o Docker religar (até 3 min).
# Docker parado (a fila às vezes o deixa assim, pela memória): liga o Docker Desktop e espera até 4 min. Recém-ligado,
# a VM está vazia: o wsl --shutdown não tem o que devolver.
docker info *> $null
if ($LASTEXITCODE) {
    Nota "docker: parado; ligo o Docker Desktop ($(Livre) MB livres)"
    Start-Process (Join-Path $env:LOCALAPPDATA 'Programs\DockerDesktop\Docker Desktop.exe')
    $ate = (Get-Date).AddMinutes(4)
    do { Start-Sleep -Seconds 5; docker info *> $null } while ($LASTEXITCODE -and (Get-Date) -lt $ate)
    Nota "docker: $(if ($LASTEXITCODE) { 'NÃO ligou' } else { 'ligou' }) ($(Livre) MB livres)"
    if ($LASTEXITCODE) { Remove-Item $trava -ErrorAction SilentlyContinue; Nota 'SOLTOU a trava; corredor terminou (codigo 6)'; exit 6 }
    $Wsl = $false
}

if ($Wsl) {
    $rodando = @(docker ps -q)
    if ($rodando.Count) { Nota "wsl: NÃO desligo, $($rodando.Count) contêiner(es) rodando" }
    else {
        Nota "wsl: desligo ($(Livre) MB livres)"
        & wsl --shutdown
        $ate = (Get-Date).AddMinutes(3)
        do { Start-Sleep -Seconds 5; docker info *> $null } while ($LASTEXITCODE -and (Get-Date) -lt $ate)
        Nota "wsl: Docker $(if ($LASTEXITCODE) { 'NÃO religou' } else { 'religou' }) ($(Livre) MB livres)"
        if ($LASTEXITCODE) { Remove-Item $trava -ErrorAction SilentlyContinue; Nota 'SOLTOU a trava; corredor terminou (codigo 6)'; exit 6 }
    }
}

# Uma fase: espera o piso, roda destacada com o log, corta abaixo de 700 MB. Devolve o código de saída.
function Invoke-Fase([string]$nome, [string]$exe, [string[]]$argumentos, [hashtable]$ambiente) {
    $inicio = Get-Date
    while ((Livre) -lt 2048) {
        if (((Get-Date) - $inicio).TotalMinutes -gt 20) { Nota "${nome}: SEM-MEMORIA ($(Livre) MB em 20 min)"; return 3 }
        Start-Sleep -Seconds 30
    }
    Nota "${nome}: começa ($(Livre) MB livres)"
    $log = Join-Path $logs "22-$nome.log"
    $antes = @{}
    foreach ($k in $ambiente.Keys) { $antes[$k] = [Environment]::GetEnvironmentVariable($k); [Environment]::SetEnvironmentVariable($k, $ambiente[$k]) }
    try { $p = Start-Process $exe -PassThru -WindowStyle Hidden -WorkingDirectory $wt -RedirectStandardOutput $log -RedirectStandardError "$log.err" -ArgumentList $argumentos }
    finally { foreach ($k in $antes.Keys) { [Environment]::SetEnvironmentVariable($k, $antes[$k]) } }
    $null = $p.Handle
    while (-not $p.HasExited) {
        if ((Livre) -lt 700) {
            Nota "${nome}: CORTADA, $(Livre) MB livres; paro e limpo"
            $arvore = @(Get-Arvore $p.Id); [array]::Reverse($arvore)
            foreach ($id in $arvore) { Stop-Process -Id $id -Force -ErrorAction SilentlyContinue }
            return 4
        }
        Start-Sleep -Seconds 5
    }
    $p.WaitForExit()
    $resumo = (Select-String -Path $log -Pattern '\[(PASSA|FALHA|MEDIDA)\]|^ℹ (pass|fail|skipped) \d+' | ForEach-Object { $_.Matches[0].Value } | Group-Object | ForEach-Object { "$($_.Count)x $($_.Name)" }) -join ', '
    Nota "${nome}: saida=$($p.ExitCode) ($resumo; $(Livre) MB livres)"
    $p.ExitCode
}

$codigo = 0
try {
    $codigo = Invoke-Fase 'docker' 'pwsh' @('-NoProfile', '-File', (Join-Path $wt 'agents\code\test\22-proxy.test.ps1'), '-Manter') `
        @{ HUB_MCP_BANCO_DIR = 'C:\Projetos\hub-mcp-banco-wt\brasa-22'; COLUMNS = '400' }
    if ($codigo -eq 0 -and -not $SoDocker) {
        $codigo = Invoke-Fase 'harness' 'node' @('--test', '--test-concurrency=1', (Join-Path $wt 'agents\code\test\ponta-a-ponta\22-cliente.test.mjs')) @{ HUB_HARNESS_REAL = '1'; HARNESSES = $Harnesses }
    }
}
finally {
    $l = & pwsh -NoProfile -File (Join-Path $wt '.local\limpar-22.ps1') 2>&1
    Nota "limpeza: $($l -join ' | ')"
    Remove-Item $trava -ErrorAction SilentlyContinue
    Nota "SOLTOU a trava; corredor terminou (codigo $codigo)"
}
exit $codigo
