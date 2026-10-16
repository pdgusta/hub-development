"""Pós-laço, extensão da etapa 1: baixa o texto da página dos itens com link fora do GitHub e URL viva, e monta o
cartão no mesmo formato dos READMEs (o texto vai no campo "readme", com "fonte": "site").

Entram os itens `web:` fora da quarentena, que não são só conceito (esses vão à frente dos conceitos) e com ao
menos uma URL que deu 200 na conferência (verificacao/urls.json). Só GET; nenhum modelo é chamado. Retoma.

Saídas (em etapas/): sites/<slug>.txt, sites/indice.json, cartoes/<slug>.json.
Uso: python baixar_sites.py [--trabalhadores 6] [--corte 12000]
"""
import argparse, concurrent.futures as cf, html, json, os, re, urllib.error, urllib.request
from html.parser import HTMLParser

AQUI = os.path.dirname(os.path.abspath(__file__))
E = lambda *p: os.path.join(AQUI, "etapas", *p)


def slug(chave):
    return re.sub(r"[^A-Za-z0-9._-]+", "__", chave)[:150]


class Texto(HTMLParser):
    PULAR = {"script", "style", "noscript", "svg", "nav", "footer", "header", "form"}

    def __init__(self):
        super().__init__()
        self.partes, self.fundo, self.titulo, self._no_titulo = [], 0, "", False

    def handle_starttag(self, tag, attrs):
        if tag in self.PULAR:
            self.fundo += 1
        if tag == "title":
            self._no_titulo = True
        if tag in ("p", "li", "h1", "h2", "h3", "h4", "pre", "tr", "br", "div"):
            self.partes.append("\n")

    def handle_endtag(self, tag):
        if tag in self.PULAR and self.fundo:
            self.fundo -= 1
        if tag == "title":
            self._no_titulo = False

    def handle_data(self, d):
        if self._no_titulo:
            self.titulo += d
        elif not self.fundo:
            self.partes.append(d)

    def texto(self):
        t = html.unescape("".join(self.partes))
        t = re.sub(r"[ \t\r\f\v]+", " ", t)
        return re.sub(r"\n\s*\n+", "\n\n", t).strip()


def baixar(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (pos-laco-sites)", "Accept": "text/html,*/*"})
    try:
        with urllib.request.urlopen(req, timeout=20) as f:
            tipo = f.headers.get("Content-Type", "")
            corpo = f.read(2_000_000)
    except urllib.error.HTTPError as e:
        return {"status": "erro", "http": e.code}
    except Exception as e:
        return {"status": "erro", "http": type(e).__name__}
    enc = (re.search(r"charset=([\w-]+)", tipo) or [None, "utf-8"])[1]
    bruto = corpo.decode(enc, errors="replace")
    if "html" in tipo or bruto.lstrip()[:15].lower().startswith(("<!doctype", "<html")):
        p = Texto()
        try:
            p.feed(bruto)
        except Exception:
            pass
        txt, titulo = p.texto(), p.titulo.strip()
    elif "text" in tipo or "json" in tipo or "markdown" in tipo:
        txt, titulo = bruto, ""
    else:
        return {"status": "erro", "http": f"tipo {tipo[:40]}"}
    if len(txt) < 200:
        return {"status": "pouco_texto", "bytes": len(txt)}
    return {"status": "ok", "texto": txt, "titulo": titulo[:200]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--trabalhadores", type=int, default=6)
    ap.add_argument("--corte", type=int, default=12000)
    a = ap.parse_args()
    os.makedirs(E("sites"), exist_ok=True)
    os.makedirs(E("cartoes"), exist_ok=True)
    itens = json.load(open(os.path.join(AQUI, "catalogo", "itens.json"), encoding="utf-8"))
    urls = json.load(open(os.path.join(AQUI, "verificacao", "urls.json"), encoding="utf-8"))
    alvo = []
    for i in itens:
        if not i["chave"].startswith("web:") or i.get("quarentena") or i["tipos"] == ["concept"]:
            continue
        vivas = [u for u in i["urls"] if u and urls.get(u) == 200]
        if vivas:
            alvo.append((i, vivas[0]))
    p_ind = E("sites", "indice.json")
    indice = json.load(open(p_ind, encoding="utf-8")) if os.path.exists(p_ind) else {}
    faltam = [(i, u) for i, u in alvo if indice.get(i["chave"], {}).get("status") not in ("ok", "pouco_texto", "erro")]
    print(len(alvo), "sites com URL viva;", len(faltam), "a baixar", flush=True)
    with cf.ThreadPoolExecutor(a.trabalhadores) as ex:
        for n, ((i, u), r) in enumerate(zip(faltam, ex.map(lambda x: baixar(x[1]), faltam)), 1):
            ch = i["chave"]
            if r["status"] == "ok":
                arq = slug(ch) + ".txt"
                open(E("sites", arq), "w", encoding="utf-8").write(r["texto"])
                indice[ch] = {"status": "ok", "arquivo": arq, "url": u, "titulo": r["titulo"], "bytes": len(r["texto"])}
                c = {k: i[k] for k in ("chave", "urls", "tipos", "termos", "mencoes", "familias", "primeira_onda")}
                c.update(nomes=i["nomes"][:12], resumos=[x["texto"] for x in i["resumos"][:4]], fonte="site",
                         readme_status="ok", readme_nome=u, readme_cortado=len(r["texto"]) > a.corte,
                         readme=(f"[{r['titulo']}]\n\n" if r["titulo"] else "") + r["texto"][:a.corte])
                json.dump(c, open(E("cartoes", slug(ch) + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
            else:
                indice[ch] = dict(r, url=u)
            if n % 50 == 0:
                json.dump(indice, open(p_ind, "w", encoding="utf-8"), ensure_ascii=False)
                print(n, "feitos", flush=True)
    json.dump(indice, open(p_ind, "w", encoding="utf-8"), ensure_ascii=False)
    print("FIM", flush=True)


if __name__ == "__main__":
    main()
