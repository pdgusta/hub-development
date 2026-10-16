"""Executa um comando, amostra o RSS somado da arvore de processos a cada 0.5s. Uso: run_rss.py <log> <cmd...>
Imprime tempo e pico de RSS (MB) em JSON na ultima linha."""
import sys,subprocess,time,psutil,json,os
log=sys.argv[1]; cmd=sys.argv[2:]
t=time.time()
f=open(log,'wb')
p=subprocess.Popen(cmd,stdout=f,stderr=subprocess.STDOUT)
root=psutil.Process(p.pid); peak=0
while p.poll() is None:
    try:
        procs=[root]+root.children(recursive=True)
        s=sum(x.memory_info().rss for x in procs if x.is_running())
        peak=max(peak,s)
    except Exception: pass
    time.sleep(0.5)
print(json.dumps(dict(rc=p.returncode,seconds=round(time.time()-t,1),peak_rss_mb=round(peak/1048576))))
