$ErrorActionPreference = 'Stop'
$env:HUB_LIVESYNC_CLI = 'C:/context-hub-wt/ticket-28/agents/code/test/banco/cli-falso.cjs'
Import-Module C:/context-hub-wt/ticket-28/agents/code/test/banco/ensaio.psm1 -Force
$e = New-EnsaioBanco -Nome ('28-fielzinho-' + [guid]::NewGuid().ToString('N'))
try {
 $par = $e.A
 New-Item -ItemType Directory -Force $par.Estado,$par.CliDb | Out-Null
 Set-NotaPar $par 'reference/exemplo/index.md' "---`ntitle: Exemplo`nstatus: em uso`nsummary: auto`n---`n`nExemplo de configuração:`nlocal: true`n"
 $saida = & pwsh -NoProfile -File C:/context-hub-wt/ticket-28/agents/skills/nova-pasta-local/nova-pasta-local.ps1 -EnvFile $par.Env -Pasta reference/exemplo 2>&1
 $codigo = $LASTEXITCODE
 Write-Output "CASO local:true só no corpo; codigo=$codigo"
 Write-Output ($saida -join "`n")
 Write-Output ('LISTA=' + (Get-NotaPar $par '.livesync/ignore'))
 Write-Output ('INDEX=' + (Get-NotaPar $par 'reference/exemplo/index.md'))
 Stop-Sincronizador $par
 $fora = Join-Path $e.Raiz 'fora-do-hub'
 New-Item -ItemType Directory -Path $fora | Out-Null
 New-Item -ItemType Junction -Path (Join-Path $par.Vault 'reference/atalho') -Target $fora | Out-Null
 $saida = & pwsh -NoProfile -File C:/context-hub-wt/ticket-28/agents/skills/nova-pasta-local/nova-pasta-local.ps1 -EnvFile $par.Env -Pasta reference/atalho/local 2>&1
 Write-Output "CASO junction para fora; codigo=$LASTEXITCODE"
 Write-Output ($saida -join "`n")
 Write-Output ('ARQUIVO_FORA=' + (Test-Path (Join-Path $fora 'local/index.md')))
 Write-Output ('LISTA_JUNCTION=' + (Get-NotaPar $par '.livesync/ignore'))
} finally {
 foreach ($par in $e.A,$e.B) { Stop-Sincronizador $par }
 $alvo = [IO.Path]::GetFullPath($e.Raiz)
 if ($alvo.StartsWith([IO.Path]::GetTempPath(),[StringComparison]::OrdinalIgnoreCase) -and (Split-Path $alvo -Leaf).StartsWith('hub-ensaio-28-fielzinho-')) { Remove-Item -LiteralPath $alvo -Recurse -Force }
}

