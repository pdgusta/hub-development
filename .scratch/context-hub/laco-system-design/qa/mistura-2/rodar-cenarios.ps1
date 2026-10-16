param([string]$Raiz,[string]$Saida,[int[]]$Larguras=@(1280,320))
$edge='C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'; if(-not(Test-Path $edge)){$edge='C:\Program Files\Microsoft\Edge\Application\msedge.exe'}
$porta=Get-Random -Min 40000 -Max 60000
$srv=Start-Process python -ArgumentList '-I','-m','http.server',$porta,'--bind','127.0.0.1','--directory',$Raiz -PassThru -WindowStyle Hidden
Start-Sleep 2
try{ foreach($w in $Larguras){
  $prof=Join-Path $env:TEMP "qa-cen-$([guid]::NewGuid())"
  $p=Start-Process $edge -ArgumentList '--headless=new','--disable-gpu','--no-first-run',"--user-data-dir=$prof","--window-size=$($w),1000",'--virtual-time-budget=60000','--dump-dom',"http://127.0.0.1:$porta/qa/mistura-2/cenarios/harness.html?w=$w" -RedirectStandardOutput "$Saida\dom-$w.html" -PassThru -WindowStyle Hidden
  if(-not $p.WaitForExit(150000)){ Stop-Process -Id $p.Id -Force }
  $t=Get-Content "$Saida\dom-$w.html" -Raw -Encoding UTF8
  if($t -match '(?s)<pre id="out">(.*?)</pre>'){ [System.Net.WebUtility]::HtmlDecode($Matches[1]) | Set-Content "$Saida\cenarios-$w.json" -Encoding UTF8 }
  Remove-Item "$Saida\dom-$w.html" -ErrorAction SilentlyContinue
  Remove-Item $prof -Recurse -Force -ErrorAction SilentlyContinue
}} finally { Stop-Process -Id $srv.Id -Force }

