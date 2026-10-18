# Reprodução da nota que não desce do A ao B (25; Brasa, 2026-10-17). Sobe os pares de ensaio do 07 como o pares.ps1
# do 25 ('novo' + 'subir', sem o MCP), mas com o sincronizador em --verbose; grava uma nota no A logo depois da subida e
# mede quando ela chega ao B. Guarda, por volta, os registros do CLI (sem segredo), o seq dos dois bancos, o estado da
# replicação, o OOM dos contêineres e a semente (tasks.md) no B. Precisa da trava (Docker).
# Uso: pwsh -NoProfile -File repro-25-desce.ps1 -Voltas 4 [-Modo live|intervalo] [-Segundos 120]
param([int]$Voltas = 4, [ValidateSet('live', 'intervalo')][string]$Modo = 'live', [int]$Segundos = 120,
    [string]$Repo = 'C:\context-hub-wt\ticket-25', [string]$Memoria = '384m', [int]$Convergir = 0)
$ErrorActionPreference = 'Stop'
Import-Module (Join-Path $Repo 'agents\code\test\banco\ensaio.psm1') -Force
$saida = Join-Path $PSScriptRoot "repro-25\$Modo-$(Get-Date -Format HHmmss)"
New-Item -ItemType Directory -Force $saida | Out-Null
$tmp = & node -p "require('fs').realpathSync.native(require('os').tmpdir())"
function Nota([string]$t) { "$(Get-Date -Format HH:mm:ss) $t" | Tee-Object -Append (Join-Path $saida 'resumo.log') }
function Livre { [math]::Round((Get-CimInstance Win32_OperatingSystem).FreePhysicalMemory / 1KB) }

# O Start-Sincronizador do kit, com argumentos a mais (--verbose; --interval no modo intervalo).
function Start-SincronizadorDiag($par, [string[]]$extra) {
    $settings = Join-Path $par.CliDb '.livesync\settings.json'
    $linha = "`"node `"$($par.Cli)`" `"$($par.CliDb)`" --settings `"$settings`" --vault `"$($par.Vault)`" daemon $($extra -join ' ') > `"$($par.Log)`" 2> `"$($par.Log).err`"`""
    $cmd = Start-Process cmd -PassThru -WindowStyle Hidden -ArgumentList @('/c', $linha)
    $node = Wait-Ate { Get-CimInstance Win32_Process -Filter "ParentProcessId=$($cmd.Id) and Name='node.exe'" | Select-Object -First 1 } 15
    if (-not $node) { throw "sincronizador de $($par.Conteiner) não partiu" }
    Set-Content -Path $par.PidArq -Value $node.ProcessId
    if (-not (Wait-Ate { ((Get-Content -Raw $par.Log, "$($par.Log).err" -ErrorAction SilentlyContinue) -join '') -match 'LiveSync active|Polling mode' } 180)) {
        throw "sincronizador de $($par.Conteiner) não ficou pronto"
    }
}
function Get-LogLimpo($par) {
    $segredos = @($par.PSObject.Properties | Where-Object { $_.Name -match 'Pass|Frase|Sal|Token' -and "$($_.Value)".Length -ge 6 } | ForEach-Object { "$($_.Value)" })
    foreach ($f in $par.Log, "$($par.Log).err") { if (Test-Path $f) { foreach ($l in (Get-Content $f)) { foreach ($s in $segredos) { $l = $l.Replace($s, '***') }; $l } } }
}

$extra = @('--verbose') + $(if ($Modo -eq 'intervalo') { @('--interval', '5') } else { @() })
for ($v = 1; $v -le $Voltas; $v++) {
    $raiz = Join-Path $tmp "hub-ensaio-25r-$v"
    $ensaio = $null
    try {
        Nota "volta ${v} ($Modo): começa ($(Livre) MB livres)"
        $ensaio = New-EnsaioBanco -Nome '25r' -Portas @(5996, 5997) -Raiz $raiz
        foreach ($par in $ensaio.A, $ensaio.B) {
            Start-CouchDBPar $par
            if ($par.Cifra) { Set-SalBanco $par }
            Set-ReplicacaoEnvio $par
            Initialize-Dispositivo $par $par.CliDb
        }
        foreach ($par in $ensaio.A, $ensaio.B) { Update-Exclusoes $par | Out-Null }
        foreach ($par in $ensaio.A, $ensaio.B) { Start-SincronizadorDiag $par $extra }
        foreach ($par in $ensaio.A, $ensaio.B) { docker update --memory $Memoria --memory-swap $Memoria $par.Conteiner | Out-Null }
        Nota "volta ${v}: pares de pé ($(Livre) MB livres)"
        $rel = "inbox/repro-$v.md"
        $t0 = Get-Date
        Set-NotaPar $ensaio.A $rel "---`ntitle: Repro $v`n---`n`nTexto inventado da volta $v.`n"
        $chegou = Wait-Ate { $null -ne (Get-NotaPar $ensaio.B $rel) } $Segundos
        $dt = [math]::Round(((Get-Date) - $t0).TotalSeconds)
        $semente = Test-Path (Join-Path $ensaio.B.Vault 'clients\aurora\migracao-de-tenant\tasks.md')
        # Convergência: quanto tempo, desde a subida, até o B ter a semente toda (os arquivos sem ponto do A).
        $conta = { param($h) @(Get-ChildItem -Recurse -File -LiteralPath $h | Where-Object { -not ([IO.Path]::GetRelativePath($h, $_.FullName) -split '[\\/]' | Where-Object { $_.StartsWith('.') }) }).Count }
        $curva = @()
        if ($Convergir) {
            $ate = $t0.AddSeconds($Convergir)
            do {
                $na = & $conta $ensaio.A.Vault; $nb = & $conta $ensaio.B.Vault
                $curva += "$([math]::Round(((Get-Date) - $t0).TotalSeconds))s A=$na B=$nb"
                if ($nb -ge $na) { break }
                Start-Sleep -Seconds 10
            } while ((Get-Date) -lt $ate)
            Nota "volta ${v}: convergência $($curva[-1])"
        }
        $diag = [ordered]@{
            curva = $curva
            volta = $v; modo = $Modo; chegou = [bool]$chegou; segundos = $dt; semente_no_b = $semente
            seq = @{ a = (Get-SeqBanco $ensaio.A); b = (Get-SeqBanco $ensaio.B) }
            replicacao = @{ a = $(try { Get-EstadoReplicacao $ensaio.A } catch { "$_" }); b = $(try { Get-EstadoReplicacao $ensaio.B } catch { "$_" }) }
            sincronizador = @{ a = [bool](Get-PidSincronizador $ensaio.A); b = [bool](Get-PidSincronizador $ensaio.B) }
            oom = @{ a = (docker inspect -f '{{.State.OOMKilled}} {{.RestartCount}}' $ensaio.A.Conteiner); b = (docker inspect -f '{{.State.OOMKilled}} {{.RestartCount}}' $ensaio.B.Conteiner) }
            livre_mb = (Livre)
        }
        $pasta = Join-Path $saida "volta-$v"
        New-Item -ItemType Directory -Force $pasta | Out-Null
        $diag | ConvertTo-Json -Depth 5 | Set-Content -Encoding utf8NoBOM (Join-Path $pasta 'diag.json')
        Get-LogLimpo $ensaio.A | Set-Content -Encoding utf8NoBOM (Join-Path $pasta 'cli-a.log')
        Get-LogLimpo $ensaio.B | Set-Content -Encoding utf8NoBOM (Join-Path $pasta 'cli-b.log')
        Nota "volta ${v}: chegou=$([bool]$chegou) em ${dt}s; semente no B=$semente; seq A=$($diag.seq.a) B=$($diag.seq.b); repl A=$($diag.replicacao.a) B=$($diag.replicacao.b)"
    }
    catch { Nota "volta ${v}: ERRO $_" }
    finally {
        if ($ensaio) { try { Remove-EnsaioBanco $ensaio } catch { Nota "volta ${v}: descer falhou: $_" } }
        elseif (Test-Path $raiz) { Remove-Item -Recurse -Force $raiz -ErrorAction SilentlyContinue }
    }
}
Nota "fim ($(Livre) MB livres)"
