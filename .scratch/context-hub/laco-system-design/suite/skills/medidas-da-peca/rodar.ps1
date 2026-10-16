<#
.SYNOPSIS
  Mede uma peça HTML/SVG em várias larguras com o Edge sem cabeça e grava o resultado em qa/.

.DESCRIPTION
  1. Sobe um servidor local só em 127.0.0.1, que serve a pasta -Raiz e, em /__medidas/, o medir.html e o medir.js
     desta skill (mesma origem, para o navegador deixar medir a peça dentro do iframe).
  2. Para cada largura: abre o medir.html no Edge sem cabeça com perfil temporário próprio (--dump-dom), tira o JSON
     de <pre id="medidas"> e grava medidas-<largura>.json; depois tira uma captura da peça nessa largura
     (captura-<largura>.png). Um Edge por vez.
  3. Roda o links.mjs (Node) e grava links.json.
  4. Encerra só o Edge do próprio perfil e o próprio servidor. Nunca mata processo pelo nome.

  Não altera a peça. Não acessa rede além de 127.0.0.1. Não usa mouse nem teclado.

.EXAMPLE
  .\rodar.ps1 -Raiz C:\Projetos\context-hub\.scratch\context-hub -Peca amostras/cidade.html -Saida .\qa
#>
param(
  [Parameter(Mandatory = $true)][string]$Raiz,
  [Parameter(Mandatory = $true)][string]$Peca,
  [string]$Saida = (Join-Path (Get-Location) 'qa'),
  [int[]]$Larguras = @(320, 768, 1280, 1920),
  [int]$Altura = 1000,
  [int]$Espera = 1500,
  [switch]$SemCaptura,
  [switch]$SemLinks
)

$ErrorActionPreference = 'Stop'
$skill = $PSScriptRoot
$edge = 'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
if (-not (Test-Path $edge)) { $edge = 'C:\Program Files\Microsoft\Edge\Application\msedge.exe' }
if (-not (Test-Path $edge)) { throw 'Edge não encontrado.' }

$Raiz = (Resolve-Path $Raiz).Path
$Peca = $Peca.TrimStart('/', '\') -replace '\\', '/'
$arquivoPeca = Join-Path $Raiz $Peca
if (-not (Test-Path $arquivoPeca)) { throw "Peça não encontrada: $arquivoPeca" }
New-Item -ItemType Directory -Force $Saida | Out-Null
$Saida = (Resolve-Path $Saida).Path
$pastaPeca = (Resolve-Path (Split-Path $arquivoPeca -Parent)).Path
if ($Saida -eq $pastaPeca -or $Saida -eq $Raiz) { throw 'A saída não pode ser a pasta da peça nem a raiz servida; use qa/.' }

function Gravar([string]$caminho, [string]$conteudo) {
  [IO.File]::WriteAllText($caminho, $conteudo, (New-Object Text.UTF8Encoding($false)))
}

function PortaLivre {
  $l = New-Object Net.Sockets.TcpListener([Net.IPAddress]::Loopback, 0)
  $l.Start(); $p = $l.LocalEndpoint.Port; $l.Stop(); return $p
}

# Encerra só os processos do Edge cujo comando traz o perfil temporário desta execução.
function EncerrarPerfil([string]$perfil) {
  $esc = [regex]::Escape($perfil)
  Get-CimInstance Win32_Process -Filter "Name='msedge.exe'" |
    Where-Object { $_.CommandLine -and $_.CommandLine -match $esc } |
    ForEach-Object { try { Stop-Process -Id $_.ProcessId -Force -ErrorAction Stop } catch {} }
}

# Roda o Edge sem cabeça com perfil próprio; devolve o caminho do arquivo com a saída padrão.
function Edge([string[]]$extras, [int]$largura, [string]$saidaPadrao) {
  $perfil = Join-Path $env:TEMP ('medidas-edge-' + [guid]::NewGuid().ToString('N'))
  New-Item -ItemType Directory -Force $perfil | Out-Null
  $argv = @('--headless=new', '--disable-gpu', '--no-first-run', '--disable-extensions', "--user-data-dir=`"$perfil`"",
    "--window-size=$largura,$Altura", '--virtual-time-budget=12000') + $extras
  try {
    $sp = @{ FilePath = $edge; ArgumentList = $argv; PassThru = $true; WindowStyle = 'Hidden' }
    if ($saidaPadrao) { $sp.RedirectStandardOutput = $saidaPadrao; $sp.RedirectStandardError = "$saidaPadrao.err" }
    $p = Start-Process @sp
    if (-not $p.WaitForExit(90000)) { Write-Warning "Edge passou de 90 s na largura $largura" }
  } finally {
    EncerrarPerfil $perfil
    Start-Sleep -Milliseconds 400
    try { Remove-Item -Recurse -Force $perfil -ErrorAction Stop } catch {}
    if ($saidaPadrao -and (Test-Path "$saidaPadrao.err")) { Remove-Item -Force "$saidaPadrao.err" }
  }
}

# Servidor local: a raiz da peça, mais /__medidas/medir.html e /__medidas/medir.js desta skill.
$codigoServidor = @'
import sys, os, functools, http.server, urllib.parse
raiz, skill, porta = sys.argv[1], sys.argv[2], int(sys.argv[3])
class H(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        p = urllib.parse.unquote(urllib.parse.urlsplit(path).path)
        if p.startswith('/__medidas/'):
            nome = p[len('/__medidas/'):]
            return os.path.join(skill, nome) if nome in ('medir.html', 'medir.js') else os.path.join(skill, '__nada__')
        return super().translate_path(path)
    def end_headers(self):
        self.send_header('Cache-Control', 'no-store')
        super().end_headers()
    def log_message(self, *a):
        pass
http.server.ThreadingHTTPServer(('127.0.0.1', porta), functools.partial(H, directory=raiz)).serve_forever()
'@
$b64 = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($codigoServidor))
$porta = PortaLivre
$py = (Get-Command python -ErrorAction Stop).Source
$servidor = Start-Process -FilePath $py -ArgumentList @('-I', '-c', "`"import base64;exec(base64.b64decode('$b64'))`"", "`"$Raiz`"", "`"$skill`"", $porta) -PassThru -WindowStyle Hidden

try {
  $base = "http://127.0.0.1:$porta"
  $ok = $false
  for ($i = 0; $i -lt 40 -and -not $ok; $i++) {
    try { $null = Invoke-WebRequest "$base/__medidas/medir.html" -UseBasicParsing -TimeoutSec 2; $ok = $true } catch { Start-Sleep -Milliseconds 250 }
  }
  if (-not $ok) { throw 'O servidor local não subiu.' }

  $urlPeca = "$base/" + ((($Peca -split '/') | ForEach-Object { [Uri]::EscapeDataString($_) }) -join '/')
  $caminhoPeca = $urlPeca.Substring($base.Length)
  $resumo = @()

  foreach ($w in $Larguras) {
    $tmp = Join-Path $Saida "dom-$w.tmp"
    $q = '/__medidas/medir.html?peca=' + [Uri]::EscapeDataString($caminhoPeca) + "&largura=$w&altura=$Altura&espera=$Espera"
    Edge @('--dump-dom', "`"$base$q`"") ([Math]::Max($w, 400)) $tmp
    $dom = if (Test-Path $tmp) { Get-Content $tmp -Raw -Encoding UTF8 } else { '' }
    if (Test-Path $tmp) { Remove-Item -Force $tmp }
    $m = [regex]::Match($dom, '<pre id="medidas" data-pronto="1">([\s\S]*?)</pre>')
    if (-not $m.Success) { Write-Warning "Largura ${w}: sem resultado no DOM"; continue }
    $json = [Net.WebUtility]::HtmlDecode($m.Groups[1].Value)
    Gravar (Join-Path $Saida "medidas-$w.json") $json
    try {
      $o = $json | ConvertFrom-Json
      if ($o.erro) { Write-Warning "Largura ${w}: $($o.erro)" }
      else {
        $resumo += [pscustomobject]@{
          largura = $w
          rolagem_horizontal = $o.pagina.rolagem_horizontal
          ligacoes = $o.cruzamentos.ligacoes_medidas
          cruzamentos = $o.cruzamentos.cruzamentos
          suspeitas = $o.cruzamentos.suspeitas
          itens = $o.distancias.itens
          folga_min_px = $o.distancias.folga_minima_px
          altura_rotulo_px = $o.distancias.altura_rotulo_px
          razao_grupos = $o.distancias.razao_entre_sobre_dentro
          contraste_falham = $o.contraste.falham
          contraste_nao_verif = $o.contraste.nao_verificados
          focaveis = $o.teclado.focaveis
          sem_nome = $o.teclado.sem_nome
          bytes = $o.peso_e_tempo.total_bytes_descomprimidos
        }
      }
    } catch { Write-Warning "Largura ${w}: JSON ilegível" }

    if (-not $SemCaptura) {
      $png = Join-Path $Saida "captura-$w.png"
      Edge @("--screenshot=`"$png`"", "`"$urlPeca`"") $w $null
    }
  }

  if (-not $SemLinks) {
    $node = Get-Command node -ErrorAction SilentlyContinue
    if ($node) {
      $links = & $node.Source (Join-Path $skill 'links.mjs') $urlPeca | Out-String
      Gravar (Join-Path $Saida 'links.json') $links
    } else { Write-Warning 'Node não encontrado: links não conferidos.' }
  }

  $tabela = $resumo | Format-Table -AutoSize | Out-String -Width 220
  Gravar (Join-Path $Saida 'resumo.txt') ("Peça: $Peca`r`nQuando: $(Get-Date -Format s)`r`n" + $tabela)
  $tabela
} finally {
  try { Stop-Process -Id $servidor.Id -Force -ErrorAction Stop } catch {}
}
