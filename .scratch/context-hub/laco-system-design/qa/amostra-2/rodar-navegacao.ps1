param([string]$Raiz,[string]$Saida)
$edge='C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'; if(-not(Test-Path $edge)){$edge='C:\Program Files\Microsoft\Edge\Application\msedge.exe'}
$porta=Get-Random -Min 40000 -Max 60000
$srv=Start-Process python -ArgumentList '-I','-m','http.server',$porta,'--bind','127.0.0.1','--directory',$Raiz -PassThru -WindowStyle Hidden
Start-Sleep 2
try{ foreach($v in @(@(1280,1000),@(320,640),@(1920,1080))){ $w=$v[0];$h=$v[1]
  $prof=Join-Path $env:TEMP "qa-nav-$([guid]::NewGuid())"
  $p=Start-Process $edge -ArgumentList '--headless=new','--disable-gpu','--no-first-run',"--user-data-dir=$prof","--window-size=$($w),$($h)",'--virtual-time-budget=90000','--dump-dom',"http://127.0.0.1:$porta/qa/amostra-2/navegacao/harness.html?w=$w&h=$h" -RedirectStandardOutput "$Saida\dom-$w.html" -PassThru -WindowStyle Hidden
  if(-not $p.WaitForExit(200000)){ Stop-Process -Id $p.Id -Force }
  $t=Get-Content "$Saida\dom-$w.html" -Raw -Encoding UTF8
  if($t -match '(?s)<pre[^>]*id="out"[^>]*>(.*?)</pre>'){ [System.Net.WebUtility]::HtmlDecode($Matches[1]) | Set-Content "$Saida\nav-$w.json" -Encoding UTF8 }
  Remove-Item "$Saida\dom-$w.html" -ErrorAction SilentlyContinue
  Remove-Item $prof -Recurse -Force -ErrorAction SilentlyContinue
}} finally { Stop-Process -Id $srv.Id -Force }

