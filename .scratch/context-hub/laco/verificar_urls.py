"""Confere se as URLs citadas pelos geradores existem, e mede a taxa de URL real por provedor e por modelo.

Só faz GET nas URLs (nenhum modelo é chamado). Saída: verificacao/urls.json (status por URL) e
verificacao/urls-por-provedor.md. Retoma: URLs já conferidas não são pedidas de novo.
Uso: python verificar_urls.py [--trabalhadores 6]
     python verificar_urls.py --repetir 429,403,URLError --trabalhadores 1 --pausa 2   (reconferir devagar)
Com --repetir, as URLs com esses status são pedidas de novo; depois de um 429, espera o Retry-After (ou 60 s)
e tenta a mesma URL até 3 vezes.
"""
import argparse, collections, concurrent.futures as cf, glob, json, os, time, urllib.error, urllib.request
from comum import caminho


PAUSA = 0.0


def checar_devagar(url):
    for _ in range(3):
        time.sleep(PAUSA)
        st, espera = checar(url, com_espera=True)
        if st != 429:
            return st
        time.sleep(espera)
    return st


def checar(url, com_espera=False):
    req = urllib.request.Request(url, method="GET", headers={"User-Agent": "Mozilla/5.0 (verificacao-laco)"})
    try:
        with urllib.request.urlopen(req, timeout=15) as f:
            st, espera = f.status, 0
    except urllib.error.HTTPError as e:
        try:
            espera = int(e.headers.get("Retry-After") or 60)
        except ValueError:
            espera = 60
        st = e.code
    except Exception as e:
        st, espera = type(e).__name__, 0
    return (st, min(espera, 300)) if com_espera else st


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--trabalhadores", type=int, default=6)
    ap.add_argument("--repetir", default="", help="status a reconferir, separados por vírgula")
    ap.add_argument("--pausa", type=float, default=0.0, help="segundos antes de cada pedido (por trabalhador)")
    a = ap.parse_args()
    global PAUSA
    PAUSA = a.pausa
    os.makedirs(caminho("verificacao"), exist_ok=True)
    saida = caminho("verificacao", "urls.json")
    feito = json.load(open(saida, encoding="utf-8")) if os.path.exists(saida) else {}
    citacoes = []  # (url, provedor, modelo)
    for f in glob.glob(caminho("livros", "*.jsonl")):
        for l in open(f, encoding="utf-8"):
            r = json.loads(l)
            if r.get("estado") != "aceito":
                continue
            prov = (r.get("via") or "?").split("/")[0]
            for it in r.get("itens") or []:
                u = (it.get("url") or "").strip()
                if u.startswith("http"):
                    citacoes.append((u, prov, r["modelo"]))
    repetir = {x.strip() for x in a.repetir.split(",") if x.strip()}
    faltam = sorted({u for u, _, _ in citacoes if u not in feito or str(feito[u]) in repetir})
    print(len(citacoes), "citações com URL;", len(set(u for u, _, _ in citacoes)), "URLs únicas;", len(faltam), "a conferir", flush=True)
    with cf.ThreadPoolExecutor(a.trabalhadores) as ex:
        for n, (u, st) in enumerate(zip(faltam, ex.map(checar_devagar if (a.pausa or repetir) else checar, faltam)), 1):
            feito[u] = st
            if n % 100 == 0:
                json.dump(feito, open(saida, "w", encoding="utf-8"), ensure_ascii=False)
                print(n, "conferidas", flush=True)
    json.dump(feito, open(saida, "w", encoding="utf-8"), ensure_ascii=False)
    por = {"provedor": collections.defaultdict(collections.Counter), "modelo": collections.defaultdict(collections.Counter)}
    for u, prov, mod in citacoes:
        st = feito.get(u)
        k = "real" if st == 200 else ("bloqueado" if st in (403, 429) else "nao_existe" if st == 404 else "outro")
        por["provedor"][prov][k] += 1
        por["modelo"][mod][k] += 1
    def tabela(d, titulo):
        linhas = [f"## {titulo}", "", "| | Citações | Reais (200) | Não existem (404) | Bloqueadas (403/429) | Outras |", "|---|---|---|---|---|---|"]
        for k, c in sorted(d.items(), key=lambda x: -sum(x[1].values())):
            t = sum(c.values())
            linhas.append(f"| {k} | {t} | {c['real'] / t:.0%} | {c['nao_existe'] / t:.0%} | {c['bloqueado'] / t:.0%} | {c['outro'] / t:.0%} |")
        return linhas
    total = collections.Counter(feito.values())
    md = [f"# URLs citadas pelos geradores ({time.strftime('%Y-%m-%d %H:%M')})", "",
          f"{len(feito)} URLs únicas conferidas com GET. Status: " + ", ".join(f"{k}: {v}" for k, v in total.most_common(8)), ""]
    md += tabela(por["provedor"], "Por provedor") + [""] + tabela(por["modelo"], "Por modelo")
    open(caminho("verificacao", "urls-por-provedor.md"), "w", encoding="utf-8").write("\n".join(md) + "\n")
    print("FIM", flush=True)


if __name__ == "__main__":
    main()
