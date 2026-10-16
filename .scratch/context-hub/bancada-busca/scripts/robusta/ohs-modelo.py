"""Fase 2, etapa 2: roda o OHS (obsidian-hybrid-search 0.16.2 da bancada) com outro modelo local.
Uso: python ohs-modelo.py <slug> <repo HF>
Copia os 124 .md do corpus (sem rajada/ e sem o .db do OHS) para fase2/vault-ohs-<slug>, roda `ohs reindex` com
LOCAL_EMBEDDING_MODEL=<repo> medindo tempo e pico de RSS (run_rss.py da bancada) e depois o avaliar.py da bancada
nos modos hybrid e semantic. Saida: resultados/ohs-<slug>-<modo>.json e fase2/ohs.jsonl."""
import json, os, shutil, subprocess, sys, time
slug, repo = sys.argv[1], sys.argv[2]
B = r"C:\Projetos\bancada-busca"; S = r"C:\Projetos\context-hub\.scratch\context-hub\bancada-busca\scripts"
src = B + r"\corpus"; dst = B + rf"\fase2\vault-ohs-{slug}"
shutil.rmtree(dst, ignore_errors=True)
for root, dirs, files in os.walk(src):
    dirs[:] = [d for d in dirs if d != "rajada" and not d.startswith(".")]
    for f in files:
        if f.endswith(".md"):
            o = os.path.join(dst, os.path.relpath(os.path.join(root, f), src)); os.makedirs(os.path.dirname(o), exist_ok=True)
            shutil.copy2(os.path.join(root, f), o)
env = dict(os.environ, OBSIDIAN_VAULT_PATH=dst, LOCAL_EMBEDDING_MODEL=repo)
env.pop("OPENAI_API_KEY", None)
ohs = B + r"\ohs\node_modules\.bin\ohs.cmd"
r = subprocess.run(["python", S + r"\run_rss.py", B + rf"\fase2\ohs-{slug}-reindex.log", ohs, "reindex"], env=env, capture_output=True, text=True)
idx = json.loads(r.stdout.strip().splitlines()[-1]) if r.stdout.strip() else {"erro": r.stderr[-300:]}
st = subprocess.run([ohs, "status", "--json"], env=env, capture_output=True, text=True, encoding="utf-8")
out = {"slug": slug, "repo": repo, "reindex": idx, "status": st.stdout.strip()[:600]}
for mode in ("hybrid", "semantic"):
    t = time.time()
    a = subprocess.run(["python", S + r"\avaliar.py", "ohs", f"ohs-{slug}-{mode}", "--mode", mode], env=env, capture_output=True, text=True, encoding="utf-8")
    out[mode] = a.stdout.strip().splitlines()[-1][:600] if a.stdout.strip() else a.stderr[-300:]
    out[mode + "_seg"] = round(time.time() - t, 1)
with open(B + r"\fase2\ohs.jsonl", "a", encoding="utf-8") as g: g.write(json.dumps(out, ensure_ascii=False) + "\n")
print(json.dumps(out, ensure_ascii=False))
