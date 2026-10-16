"""Amostra RSS somado da arvore de um PID por N segundos. Uso: rss_pid.py <pid> <segundos>"""
import sys,time,psutil,json
root=psutil.Process(int(sys.argv[1])); end=time.time()+float(sys.argv[2]); peak=0; last=0
while time.time()<end:
    try:
        procs=[root]+root.children(recursive=True)
        last=sum(x.memory_info().rss for x in procs); peak=max(peak,last)
    except Exception: break
    time.sleep(0.5)
print(json.dumps(dict(peak_rss_mb=round(peak/1048576),last_rss_mb=round(last/1048576))))
