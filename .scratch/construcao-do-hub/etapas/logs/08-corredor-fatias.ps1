# Corredor destacado das fatias do teste do ticket 08 (aval do maestro, 2026-10-17 ~04h10): uma fatia por vez, com a
# trava; antes de cada fatia, o piso de 2 GB livres (20 min sem chegar: para e avisa); durante, abaixo de ~700 MB livres
# para a fatia e limpa (daemon pelo PID, contêineres, pasta). Saída e estado em etapas/logs/.
# Uso: Start-Process pwsh -ArgumentList '-NoProfile','-File','.local\fatias.ps1','-Fatias','2,3'
param([string]$Fatias)
$ErrorActionPreference = 'Stop'
$wt = 'C:\context-hub-wt\ticket-08'
$etapas = 'C:\Projetos\context-hub\.scratch\construcao-do-hub\etapas'
$trava = Join-Path $etapas 'trava-pesada.md'
$logs = Join-Path $etapas 'logs'
$estado = Join-Path $logs '08-fatias.status'
$ensaio = Join-Path $env:TEMP 'hub-ensaio-08'
New-Item -ItemType Directory -Force $logs | Out-Null
function Nota([string]$t) { "$(Get-Date -Format 'HH:mm:ss') $t" | Add-Content -Encoding utf8NoBOM $estado }
function Livre { [math]::Round((Get-CimInstance Win32_OperatingSystem).FreePhysicalMemory / 1KB) }   # MB

function Limpa {
    foreach ($p in Get-CimInstance Win32_Process -Filter "Name='node.exe'" | Where-Object { "$($_.CommandLine)".Contains($ensaio) }) {
        Stop-Process -Id $p.ProcessId -Force -ErrorAction SilentlyContinue
    }
    foreach ($l in 'a', 'b') {
        $env = Join-Path $ensaio "$l\04.env"
        if (Test-Path $env) { & pwsh -NoProfile -File (Join-Path $wt 'agents\code\kit\par\04-banco.ps1') -EnvFile $env -Descer -ApagarDados *> $null }
    }
    foreach ($c in docker ps -a --filter "name=^$(Split-Path -Leaf $ensaio)-" --format '{{.Names}}') { docker rm -f $c *> $null }
    Start-Sleep -Seconds 1
    Remove-Item -Recurse -Force $ensaio -ErrorAction SilentlyContinue
}

# a árvore de processos do teste (pwsh do teste e os filhos dele)
function Get-Arvore([int]$raiz) {
    $todos = @(Get-CimInstance Win32_Process | Select-Object ProcessId, ParentProcessId)
    $ids = @($raiz); $i = 0
    while ($i -lt $ids.Count) { $ids += @($todos | Where-Object { $_.ParentProcessId -eq $ids[$i] } | ForEach-Object ProcessId); $i++ }
    $ids
}

Nota "corredor $PID começou: fatias $Fatias"
# a trava para a sequência inteira (fila em etapas/fila-pesada.md: quem solta avisa o próximo)
function Pega-Trava {
    while ($true) {
        if (-not (Test-Path $trava)) {
            try {
                $s = [IO.File]::Open($trava, 'CreateNew', 'Write')
                $b = [Text.UTF8Encoding]::new($false).GetBytes("- Brasa (construtora), 2026-10-17 $(Get-Date -Format HH:mm): ticket 08, fatias $Fatias do 08-banco-limites.test.ps1 (Docker), uma por vez, worktree ticket-08; corredor destacado PID $PID. Apago ao fim.`n")
                $s.Write($b, 0, $b.Length); $s.Close(); break
            } catch [IO.IOException] { }
        }
        Start-Sleep -Seconds 30
    }
}
# só parte com a trava livre (lançado depois do aviso da fila); ocupada: não espera, termina
if (Test-Path $trava) { Nota 'trava OCUPADA na partida; não espero (relançar depois do aviso)'; exit 5 }
Pega-Trava
Nota 'PEGOU a trava'
$codigo = 0
try {
    $cedeu = $false; $primeira = $true
    foreach ($f in $Fatias -split ',') {
        # entre fatias, depois das 06:58, uma vez: se o Trilho ainda espera o Codex do 15 na fila, cede a trava a ele
        $fila = Get-Content -Raw (Join-Path $etapas 'fila-pesada.md') -ErrorAction SilentlyContinue
        # ou quando alguém pediu a vez entre fatias: o arquivo .local/ceder (com o nome de quem) existe
        $sinal = Join-Path $wt '.local/ceder'
        $pedido = if (-not $primeira -and (Test-Path $sinal)) { (Get-Content -Raw $sinal).Trim() }
        $codex = -not $primeira -and -not $cedeu -and (Get-Date).TimeOfDay -ge [TimeSpan]'06:58' -and "$fila" -match 'Trilho:.*Codex do 15'
        if ($pedido -or $codex) {
            Remove-Item $trava -ErrorAction SilentlyContinue
            Remove-Item $sinal -ErrorAction SilentlyContinue
            Nota "CEDE a trava a $(if ($pedido) { $pedido } else { 'Trilho (Codex do 15)' }) antes da fatia $f"
            # não retoma sozinho (maestro, 05h50): grava o que falta e termina; a Brasa relança depois do aviso da fila
            $faltam = @($Fatias -split ',' | Select-Object -Skip ([array]::IndexOf(@($Fatias -split ','), $f)))
            Nota "PARA depois de ceder; faltam: $($faltam -join ',')"
            $script:cedido = $true
            return
        }
        $primeira = $false
        $inicio = Get-Date
        while ((Livre) -lt 2048) {
            if (((Get-Date) - $inicio).TotalMinutes -gt 20) {
                Nota "fatia ${f}: SEM-MEMORIA ($(Livre) MB livres em 20 min); parei sem forçar"
                $codigo = 3; return
            }
            Start-Sleep -Seconds 30
        }
        Nota "fatia ${f}: começa ($(Livre) MB livres)"
        $ensaio = Join-Path $env:TEMP $(if ($f -eq '07') { 'hub-ensaio-07' } else { 'hub-ensaio-08' })
        # '1+2' = as fatias 1 e 2 numa subida só (revisão do Fiel, r2), log 08-fatias-1-2.log
        $log = Join-Path $logs $(if ($f.Contains('+')) { "08-fatias-$($f.Replace('+', '-')).log" } else { "08-fatia-$f.log" })
        $p = Start-Process pwsh -PassThru -WindowStyle Hidden -RedirectStandardOutput $log -RedirectStandardError "$log.err" `
            -ArgumentList $(if ($f -eq '07') { @('-NoProfile', '-File', (Join-Path $wt 'agents\code\test\07-banco.test.ps1')) }   # o passo do kit mudou
                            # por -Command: com -File, "-Fatias 1,2" chega como o número 12
                            else { @('-NoProfile', '-Command', "& '$(Join-Path $wt 'agents\code\test\08-banco-limites.test.ps1')' -Fatias $($f.Replace('+', ',')); exit `$LASTEXITCODE") })
        $null = $p.Handle   # sem o handle aberto, o ExitCode sai vazio
        while (-not $p.HasExited) {
            if ((Livre) -lt 700) {
                Nota "fatia ${f}: CORTADA, $(Livre) MB livres; paro o teste e limpo"
                $arvore = @(Get-Arvore $p.Id); [array]::Reverse($arvore)
                foreach ($id in $arvore) { Stop-Process -Id $id -Force -ErrorAction SilentlyContinue }
                Limpa
                $codigo = 4; return
            }
            Start-Sleep -Seconds 5
        }
        $p.WaitForExit()
        $resumo = (Select-String -Path $log -Pattern '\[(PASSA|FALHA)\]' | ForEach-Object { $_.Matches[0].Groups[1].Value } | Group-Object | ForEach-Object { "$($_.Count) $($_.Name)" }) -join ', '
        Nota "fatia ${f}: saida=$($p.ExitCode) ($resumo; $(Livre) MB livres)"
        if (Test-Path $ensaio) { Limpa; Nota "fatia ${f}: sobrou ensaio, limpei" }
    }
}
finally {
    if (-not $script:cedido) { Remove-Item $trava -ErrorAction SilentlyContinue }
    Nota "SOLTOU a trava; corredor terminou (codigo $codigo)"
}
exit $codigo
