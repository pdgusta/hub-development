# Desce a pilha deixada de pé por 22-proxy.test.ps1 -Manter (lê %TEMP%\hub-ensaio-22\cliente.json): proxy, busca (o
# PID que o teste abriu), as três instâncias do MCP do banco e os dois pares (contêineres e pasta).
$ErrorActionPreference = 'Stop'
$repo = 'C:\context-hub-wt\ticket-22'
Import-Module (Join-Path $repo 'agents\code\test\banco\ensaio.psm1') -Force
Import-Module (Join-Path $repo 'agents\code\kit\par\proxy\proxy.psm1') -Force
$arq = Join-Path $env:TEMP 'hub-ensaio-22\cliente.json'
if (-not (Test-Path $arq)) { Write-Output 'sem pilha'; exit 0 }
$p = Get-Content -Raw $arq | ConvertFrom-Json
$par = Read-EnvProxy $p.env
Stop-Proxy $par
if ($p.busca) { & taskkill /T /F /PID $p.busca 2>&1 | Out-Null }
foreach ($i in $par.McpInstancias) { Stop-McpBanco $i }
$a = Read-EnvPar $p.env; $b = Read-EnvPar $p.envB
Remove-EnsaioBanco ([pscustomobject]@{ Raiz = $p.raiz; A = $a; B = $b })
$sobra = docker ps -a --filter 'name=hub-ensaio-22-' -q
Write-Output "pilha descida; contêineres que sobraram: $(@($sobra).Count)"
