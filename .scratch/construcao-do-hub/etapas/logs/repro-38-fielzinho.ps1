$ErrorActionPreference = 'Stop'
# Executa apenas o finally real dos testes, com funções dublês. Não inicia processo nem Docker.
foreach ($ticket in '09', '10') {
    $arquivo = "C:/context-hub-wt/ticket-38/agents/code/test/$ticket-mcp-banco.test.ps1"
    $tokens = $null; $erros = $null
    $ast = [Management.Automation.Language.Parser]::ParseFile($arquivo, [ref]$tokens, [ref]$erros)
    if ($erros) { throw $erros }
    $bloco = ($ast.EndBlock.Statements | Where-Object { $_ -is [Management.Automation.Language.TryStatementAst] } | Select-Object -Last 1).Finally.Extent.Text
    $script:limpou = $false
    function Stop-McpBanco { throw 'falha forçada ao parar MCP' }
    function Remove-EnsaioBanco { $script:limpou = $true }
    $mcp = $par = [pscustomobject]@{ McpInstancias = @([pscustomobject]@{ McpNome = 'ensaio' }) }
    $ensaio = [pscustomobject]@{ Raiz = 'nao-usada' }
    $Manter = $false
    try { & ([scriptblock]::Create($bloco.Substring(1, $bloco.Length - 2))) }
    catch { Write-Output "$ticket erro=$($_.Exception.Message)" }
    Write-Output "$ticket Remove-EnsaioBanco chamado=$script:limpou"
    if ($script:limpou) { throw 'a reprodução deixou de mostrar o defeito' }
}
