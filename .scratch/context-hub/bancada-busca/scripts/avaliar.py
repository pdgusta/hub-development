"""Busca as 40 perguntas numa ferramenta e grava o top 5 + metricas.
Uso: avaliar.py <ferramenta: ohs|mm> <config> [--mode M] ; env fornece o resto.
Saida: resultados/<config>.json"""
import sys,json,subprocess,os,time,re
BASE=r"C:\Projetos\bancada-busca"
Q=json.load(open(BASE+r"\perguntas.json",encoding='utf-8'))
def norm(p): return p.replace(chr(92),'/')
def run_ohs(q,mode):
    cmd=[BASE+r"\ohs\node_modules\.bin\ohs.cmd","search","--json","--limit","5","--mode",mode,q]
    r=subprocess.run(cmd,capture_output=True,text=True,encoding='utf-8')
    try: data=json.loads(r.stdout)
    except Exception: return None,(r.stdout+r.stderr)[:500]
    return [norm(d['path']) for d in data],None
def run_mm(q,_mode):
    cmd=[BASE+r"\mm\Scripts\mm.exe","search",q,"--format","json","-k","30"]
    r=subprocess.run(cmd,capture_output=True,text=True,encoding='utf-8')
    try:
        data=json.loads(r.stdout)
    except Exception: return None,(r.stdout+r.stderr)[:500]
    out=[]
    pre=norm(BASE+r"\corpus")+"/"
    for d in data:
        p=norm(d['source'])
        if p.lower().startswith(pre.lower()): p=p[len(pre):]
        if p not in out: out.append(p)
    return out,None
def metrics(rows):
    def agg(sel):
        s=[r for r in rows if sel(r)]
        if not s: return None
        return dict(n=len(s),hit5=round(sum(r['rank'] is not None for r in s)/len(s),3),
                    mrr=round(sum((1/r['rank']) if r['rank'] else 0 for r in s)/len(s),3))
    return dict(total=agg(lambda r:True),L=agg(lambda r:r['tipo']=='L'),P=agg(lambda r:r['tipo']=='P'),
                pt=agg(lambda r:r['lang']=='pt'),en=agg(lambda r:r['lang']=='en'))
def score(q,paths):
    rank=None
    for i,p in enumerate(paths[:5],1):
        if p in q['files']: rank=i;break
    return rank
if __name__=="__main__":
    tool,cfg=sys.argv[1],sys.argv[2]
    mode=sys.argv[sys.argv.index('--mode')+1] if '--mode' in sys.argv else 'hybrid'
    fn=run_ohs if tool=='ohs' else run_mm
    rows=[];t=time.time()
    for q in Q:
        paths,err=fn(q['q'],mode)
        if paths is None: print('ERRO',q['n'],err); paths=[]
        if tool=='mm':
            pass
        rows.append(dict(n=q['n'],tipo=q['tipo'],lang=q['lang'],q=q['q'],esperado=q['files'],top5=paths[:5],rank=score(q,paths)))
    res=dict(config=cfg,segundos=round(time.time()-t,1),metricas=metrics(rows),perguntas=rows)
    os.makedirs(BASE+r"\resultados",exist_ok=True)
    json.dump(res,open(BASE+rf"\resultados\{cfg}.json","w",encoding='utf-8'),ensure_ascii=False,indent=1)
    print(cfg,json.dumps(res['metricas']),res['segundos'],'s')
