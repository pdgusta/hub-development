"""Fila sequencial: python fila.py <sonda|indexar> <log> slug...  (um processo node por modelo; indexar mede RSS pela arvore e corta em 40 min)"""
import sys, subprocess, json, time, os, psutil
modo, log, slugs = sys.argv[1], sys.argv[2], sys.argv[3:]
here = os.path.dirname(os.path.abspath(__file__))
script = {"sonda": "sonda.mjs", "indexar": "indexar-modelo.mjs", "ambos": "indexar-modelo.mjs", "avaliar": "avaliar-modelo.mjs"}[modo]
LIM = int(os.environ.get("FILA_LIM_MIN", "40")) * 60
for s in slugs:
    t = time.time()
    with open(log + "." + s + ".out", "wb") as f:
        p = subprocess.Popen(["node", os.path.join(here, script), s], stdout=f, stderr=subprocess.STDOUT, env=os.environ)
        root = psutil.Process(p.pid); peak = 0; cortado = False
        while p.poll() is None:
            try: peak = max(peak, sum(x.memory_info().rss for x in [root] + root.children(recursive=True)))
            except Exception: pass
            if time.time() - t > LIM and modo in ("indexar", "ambos"):
                p.kill(); cortado = True; break
            time.sleep(0.5)
        p.wait()
    last = ""
    try: last = [l for l in open(log + "." + s + ".out", encoding="utf-8", errors="replace").read().splitlines() if l.startswith("{")][-1]
    except Exception: pass
    with open(log, "a", encoding="utf-8") as g:
        g.write(json.dumps(dict(slug=s, rc=p.returncode, seg=round(time.time() - t, 1), pico_rss_mb=round(peak / 1048576), cortado_40min=cortado, ultima=last), ensure_ascii=False) + "\n")
with open(log, "a") as g: g.write('{"fila":"fim"}\n')
