"""Rajada: liga a ferramenta vigiando, mede RSS ocioso, copia 200 .md de rajada-src para corpus\rajada
e mede o tempo ate a busca achar os marcadores. Uso: rajada.py ohs|mm"""
import sys,subprocess,time,json,os,shutil,psutil,glob
from concurrent.futures import ThreadPoolExecutor
B=r"C:\Projetos\bancada-busca"; tool=sys.argv[1]
env=dict(os.environ)
if tool=='ohs':
    env['OBSIDIAN_VAULT_PATH']=B+r"\corpus"
    srv=[B+r"\ohs\node_modules\.bin\ohs.cmd","serve","--foreground"]
    def search(m):
        r=subprocess.run([B+r"\ohs\node_modules\.bin\ohs.cmd","search","--json","--limit","5","--mode","fulltext",m],capture_output=True,text=True,encoding='utf-8',env=env)
        try: return [d['path'].replace(chr(92),'/') for d in json.loads(r.stdout)]
        except Exception: return []
else:
    env['USERPROFILE']=env['HOME']=B+r"\mmhome"; env['PYTHONIOENCODING']='utf-8'
    srv=[B+r"\mm\Scripts\memtomem-server.exe"]
    def search(m):
        r=subprocess.run([B+r"\mm\Scripts\mm.exe","search",m,"--format","json","-k","10"],capture_output=True,text=True,encoding='utf-8',env=env)
        try: return [d['source'].replace(chr(92),'/') for d in json.loads(r.stdout)]
        except Exception: return []
def found(i):
    return any(p.endswith(f"rajada/rajada-{i:04d}.md") for p in search(f"marcadorrajada{i:04d}"))
shutil.rmtree(B+r"\corpus\rajada",ignore_errors=True)
log=open(B+rf"\logs\rajada-{tool}-server.log","wb")
p=subprocess.Popen(srv,stdin=subprocess.PIPE,stdout=log,stderr=subprocess.STDOUT,env=env)
root=psutil.Process(p.pid)
def rss():
    try: return sum(x.memory_info().rss for x in [root]+root.children(recursive=True))
    except Exception: return 0
out={}
peak=0;t=time.time()
while time.time()-t<45: peak=max(peak,rss()); time.sleep(1)
out['rss_ocioso_pico_mb_45s']=round(peak/1048576); out['rss_ocioso_final_mb']=round(rss()/1048576)
os.makedirs(B+r"\corpus\rajada")
t0=time.time()
for f in glob.glob(B+r"\rajada-src\*.md"): shutil.copy(f,B+r"\corpus\rajada")
out['copia_s']=round(time.time()-t0,2)
peak=0; t_probe=None; t_first=None
while time.time()-t0<300:
    peak=max(peak,rss())
    hits=[found(i) for i in (1,100,200)]
    if any(hits) and t_first is None: t_first=round(time.time()-t0,1)
    if all(hits): t_probe=round(time.time()-t0,1);break
out['primeiro_marcador_s']=t_first; out['tres_sondas_s']=t_probe
res=[]
if t_probe is not None:
    with ThreadPoolExecutor(6) as ex: res=list(ex.map(found,range(1,201)))
    out['verificacao_completa_s']=round(time.time()-t0,1)
out['marcadores_achados']=sum(res); out['pico_rss_mb_rajada']=round(max(peak,rss())/1048576)
out['faltando']=[i for i,r in enumerate(res,1) if not r][:20] if res else 'sem verificacao'
print(json.dumps(out))
json.dump(out,open(B+rf"\resultados\rajada-{tool}.json","w"),indent=1)
# se nao chegou, deixa mais 0 s; encerra
try:
    for c in root.children(recursive=True): c.kill()
    root.kill()
except Exception: pass
