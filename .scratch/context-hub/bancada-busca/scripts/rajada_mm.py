"""Rajada do memtomem: sobe memtomem-server por stdio com um cliente MCP real (initialize + mem_status),
mede RSS ocioso, copia 200 .md e mede o tempo ate os marcadores aparecerem na busca."""
import asyncio,os,sys,time,json,shutil,glob,subprocess,psutil
from concurrent.futures import ThreadPoolExecutor
from mcp import ClientSession,StdioServerParameters
from mcp.client.stdio import stdio_client
B=r"C:\Projetos\bancada-busca"
env=dict(os.environ); env['USERPROFILE']=env['HOME']=B+r"\mmhome"; env['PYTHONIOENCODING']='utf-8'
def search(m):
    r=subprocess.run([B+r"\mm\Scripts\mm.exe","search",m,"--format","json","-k","10"],capture_output=True,text=True,encoding='utf-8',env=env,timeout=120)
    try: return [d['source'].replace(chr(92),'/') for d in json.loads(r.stdout)]
    except Exception: return []
def found(i): return any(p.endswith(f"rajada/rajada-{i:04d}.md") for p in search(f"marcadorrajada{i:04d}"))
def rss():
    me=psutil.Process(); tot=0
    for c in me.children(recursive=True):
        try:
            if 'memtomem-server' in ' '.join(c.cmdline()) or c.name().startswith('memtomem'): tot+=c.memory_info().rss
        except Exception: pass
    return tot
async def main():
    shutil.rmtree(B+r"\corpus\rajada",ignore_errors=True)
    out={}
    params=StdioServerParameters(command=B+r"\mm\Scripts\memtomem-server.exe",env=env)
    async with stdio_client(params) as (r,w):
        async with ClientSession(r,w) as s:
            await s.initialize()
            res=await s.call_tool("mem_status",{}); out['mem_status']=str(res.content)[:200]
            peak=0;t=time.time()
            while time.time()-t<45: peak=max(peak,rss()); await asyncio.sleep(1)
            out['rss_ocioso_pico_mb_45s']=round(peak/1048576); out['rss_ocioso_final_mb']=round(rss()/1048576)
            os.makedirs(B+r"\corpus\rajada"); t0=time.time()
            for f in glob.glob(B+r"\rajada-src\*.md"): shutil.copy(f,B+r"\corpus\rajada")
            out['copia_s']=round(time.time()-t0,2)
            loop=asyncio.get_running_loop(); peak=0; t_first=t_probe=None
            while time.time()-t0<300:
                peak=max(peak,rss())
                hits=await asyncio.gather(*[loop.run_in_executor(None,found,i) for i in (1,100,200)])
                if any(hits) and t_first is None: t_first=round(time.time()-t0,1)
                if all(hits): t_probe=round(time.time()-t0,1);break
            out['primeiro_marcador_s']=t_first; out['tres_sondas_s']=t_probe
            resl=[]
            if t_probe is not None:
                with ThreadPoolExecutor(4) as ex: resl=await loop.run_in_executor(None,lambda:list(ex.map(found,range(1,201))))
                out['verificacao_completa_s']=round(time.time()-t0,1)
            out['marcadores_achados']=sum(resl); out['pico_rss_mb_rajada']=round(max(peak,rss())/1048576)
            out['faltando']=[i for i,x in enumerate(resl,1) if not x][:20] if resl else 'sem verificacao'
    print(json.dumps(out)); json.dump(out,open(B+r"\resultados\rajada-mm.json","w"),indent=1)
asyncio.run(main())
