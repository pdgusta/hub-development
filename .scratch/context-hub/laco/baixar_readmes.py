"""Etapa 1 do pós-laço: baixa o README bruto de cada item com repositório no GitHub e monta o cartão do item.

Só faz GET em raw.githubusercontent.com (nenhum modelo é chamado). Tenta os nomes comuns de README no ramo
padrão (HEAD). Retoma: itens já com status "ok", "sem_readme" ou "morto" não são pedidos de novo.

Saídas (em etapas/):
    readmes/<slug>.md       o README inteiro
    readmes/indice.json     {chave: {"status": "ok"|"sem_readme"|"morto"|"bloqueado"|"erro", "arquivo", "bytes"}}
    cartoes/<slug>.json     o cartão: dados do catálogo + README (cortado em --corte caracteres)

"sem_readme" e "morto" se distinguem pela conferência de URLs (verificacao/urls.json): se a página do
repositório deu 404, o item é "morto"; senão, "sem_readme".

Uso: python baixar_readmes.py [--trabalhadores 4] [--pausa 0.3] [--corte 12000] [--so-cartoes]
"""
import argparse, concurrent.futures as cf, json, os, threading, time, urllib.error, urllib.request

AQUI = os.path.dirname(os.path.abspath(__file__))
E = lambda *p: os.path.join(AQUI, "etapas", *p)
NOMES = ["README.md", "readme.md", "Readme.md", "README.rst", "README", "README.markdown", "README.txt",
         "readme.rst", "docs/README.md"]
PAUSA = 0.3
trava = threading.Lock()


def slug(chave):
    return chave.replace(":", "__").replace("/", "__")


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (pos-laco-readmes)"})
    for _ in range(4):
        time.sleep(PAUSA)
        try:
            with urllib.request.urlopen(req, timeout=20) as f:
                return 200, f.read()
        except urllib.error.HTTPError as e:
            if e.code == 429:
                try:
                    espera = int(e.headers.get("Retry-After") or 60)
                except ValueError:
                    espera = 60
                time.sleep(min(espera, 300))
                continue
            return e.code, b""
        except Exception as e:
            return type(e).__name__, b""
    return 429, b""


def baixar(chave):
    dono_repo = chave[3:]
    ultimo = None
    for nome in NOMES:
        st, corpo = get(f"https://raw.githubusercontent.com/{dono_repo}/HEAD/{nome}")
        if st == 200 and corpo.strip():
            arq = slug(chave) + ".md"
            open(E("readmes", arq), "wb").write(corpo)
            return {"status": "ok", "arquivo": arq, "nome": nome, "bytes": len(corpo)}
        if st == 429:
            return {"status": "bloqueado"}
        if st != 404:
            ultimo = st
    return {"status": "erro", "ultimo": ultimo} if ultimo else {"status": "sem_readme_raw"}


def classificar_sem_readme(indice, itens, urls):
    for it in itens:
        r = indice.get(it["chave"])
        if not r or r["status"] not in ("sem_readme_raw", "sem_readme", "morto"):
            continue
        pagina = f"https://github.com/{it['chave'][3:]}"
        sts = [str(v) for u, v in urls.items() if u.lower().rstrip("/") == pagina]
        r["status"] = "morto" if sts and all(s == "404" for s in sts) else "sem_readme"


def cartao(it, r, corte):
    c = {k: it[k] for k in ("chave", "urls", "tipos", "termos", "mencoes", "familias", "primeira_onda")}
    c["nomes"] = it["nomes"][:12]
    c["resumos"] = [x["texto"] for x in it["resumos"][:4]]
    c["readme_status"] = r["status"]
    if r["status"] == "ok":
        texto = open(E("readmes", r["arquivo"]), encoding="utf-8", errors="replace").read()
        c["readme_nome"] = r["nome"]
        c["readme_cortado"] = len(texto) > corte
        c["readme"] = texto[:corte]
    return c


def main():
    global PAUSA
    ap = argparse.ArgumentParser()
    ap.add_argument("--trabalhadores", type=int, default=4)
    ap.add_argument("--pausa", type=float, default=0.3)
    ap.add_argument("--corte", type=int, default=12000)
    ap.add_argument("--so-cartoes", action="store_true")
    a = ap.parse_args()
    PAUSA = a.pausa
    for p in ("readmes", "cartoes"):
        os.makedirs(E(p), exist_ok=True)
    itens = json.load(open(os.path.join(AQUI, "catalogo", "itens.json"), encoding="utf-8"))
    gh = [i for i in itens if i["chave"].startswith("gh:") and not i.get("quarentena")]
    caminho_ind = E("readmes", "indice.json")
    indice = json.load(open(caminho_ind, encoding="utf-8")) if os.path.exists(caminho_ind) else {}
    faltam = [i["chave"] for i in gh if indice.get(i["chave"], {}).get("status") not in ("ok", "sem_readme", "morto", "sem_readme_raw")]
    if a.so_cartoes:
        faltam = []
    print(len(gh), "itens com repositório;", len(faltam), "a baixar", flush=True)

    def gravar():
        tmp = caminho_ind + ".tmp"
        json.dump(indice, open(tmp, "w", encoding="utf-8"), ensure_ascii=False)
        os.replace(tmp, caminho_ind)

    with cf.ThreadPoolExecutor(a.trabalhadores) as ex:
        for n, (ch, r) in enumerate(zip(faltam, ex.map(baixar, faltam)), 1):
            with trava:
                indice[ch] = r
            if n % 50 == 0:
                gravar()
                print(n, "feitos", flush=True)
    urls = {}
    try:
        urls = json.load(open(os.path.join(AQUI, "verificacao", "urls.json"), encoding="utf-8"))
    except OSError:
        pass
    classificar_sem_readme(indice, gh, urls)
    gravar()
    for it in gh:
        r = indice.get(it["chave"])
        if r:
            json.dump(cartao(it, r, a.corte), open(E("cartoes", slug(it["chave"]) + ".json"), "w", encoding="utf-8"),
                      ensure_ascii=False, indent=1)
    print("FIM", flush=True)


if __name__ == "__main__":
    main()
