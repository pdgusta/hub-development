"""Pós-laço: monta os cartões dos conceitos (itens só do tipo "concept", fora da quarentena) para os subagentes Haiku.

Junta variantes óbvias do mesmo conceito pelo nome sem parênteses e sem palavras de enfeite ("algorithm",
"pattern", "strategy"...). Não há fonte primária: o cartão leva os nomes, os resumos dos geradores e os termos.
Nenhum modelo é chamado.

Saídas: etapas/conceitos/cartoes/<slug>.json e etapas/conceitos/fila.json ([{"chave", "slug", "mencoes"}], por
menções). Uso: python cartoes_conceitos.py
"""
import collections, json, os, re, unicodedata

AQUI = os.path.dirname(os.path.abspath(__file__))
E = lambda *p: os.path.join(AQUI, "etapas", "conceitos", *p)
ENFEITE = r"\b(algorithm|algorithms|pattern|patterns|strategy|strategies|approach|technique|techniques|method|" \
          r"concept|model|architecture|system|systems|the|a|an|de|da|do|para|em)\b"


def slug(ch):
    return re.sub(r"[^A-Za-z0-9._-]+", "__", ch)[:150]


def base(nome):
    n = re.sub(r"\(.*?\)|\[.*?\]", " ", nome)
    n = unicodedata.normalize("NFKD", n).encode("ascii", "ignore").decode().lower()
    n = re.sub(ENFEITE, " ", n)
    n = re.sub(r"[^a-z0-9+]+", " ", n).strip()
    return n


def main():
    itens = json.load(open(os.path.join(AQUI, "catalogo", "itens.json"), encoding="utf-8"))
    conc = [i for i in itens if i["tipos"] == ["concept"] and not i.get("quarentena")]
    grupos = collections.defaultdict(list)
    for i in conc:
        b = base(i["nomes"][0]) or i["chave"]
        grupos[b].append(i)
    os.makedirs(E("cartoes"), exist_ok=True)
    fila = []
    for b, gs in grupos.items():
        gs.sort(key=lambda i: -i["mencoes"])
        ch = "conceito:" + b.replace(" ", "-")[:120]
        nomes, resumos, termos = [], [], []
        for i in gs:
            nomes += [n for n in i["nomes"] if n not in nomes]
            resumos += [r["texto"] for r in i["resumos"] if r["texto"] not in resumos]
            termos += [t for t in i["termos"] if t not in termos]
        c = {"chave": ch, "chaves_do_catalogo": [i["chave"] for i in gs], "nomes": nomes[:15],
             "mencoes": sum(i["mencoes"] for i in gs), "familias": sorted({f for i in gs for f in i["familias"]}),
             "resumos": resumos[:8], "termos": termos[:20], "urls": [u for i in gs for u in i["urls"] if u][:5]}
        json.dump(c, open(E("cartoes", slug(ch) + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        fila.append({"chave": ch, "slug": slug(ch), "mencoes": c["mencoes"]})
    fila.sort(key=lambda x: -x["mencoes"])
    json.dump(fila, open(E("fila.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    um = sum(1 for f in fila if f["mencoes"] == 1)
    print(len(conc), "itens de conceito ->", len(fila), "cartões;", um, "com uma menção só")


if __name__ == "__main__":
    main()
