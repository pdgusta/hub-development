# Medidor da Brasa: a cada 5 s, hora, MB livres e MB do vmmemWSL, até o arquivo de parada existir.
param([string]$Saida, [string]$Parar)
while (-not (Test-Path $Parar)) {
    $l = [math]::Round((Get-CimInstance Win32_OperatingSystem).FreePhysicalMemory / 1KB)
    $v = [math]::Round(((Get-Process vmmemWSL -ErrorAction SilentlyContinue | Measure-Object WorkingSet64 -Sum).Sum) / 1MB)
    "$(Get-Date -Format HH:mm:ss) $l $v" | Add-Content -Encoding utf8NoBOM $Saida
    Start-Sleep -Seconds 5
}
