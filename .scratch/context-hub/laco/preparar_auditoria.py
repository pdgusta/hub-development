"""Etapa 4 do pós-laço: sorteia a amostra da auditoria (10% da conferência e 10% dos conceitos, estratificada) e
monta os pacotes para os subagentes Opus. Nenhum modelo é chamado.

Estratos: conferência por (resultado, fonte); conceitos por veredito (busca, stack, nada, dúvida). Semente fixa.
Saídas: etapas/auditoria/pacotes/<slug>.json e etapas/auditoria/fila.json ([{"chave", "slug", "tipo", "estrato"}]).
Uso: python preparar_auditoria.py [--fracao 0.1]
"""
import argparse, collections, glob, json, math, os, random, re

AQUI = os.path.dirname(os.path.abspath(__file__))
E = lambda *p: os.path.join(AQUI, "etapas", *p)


def slug(ch):
    return re.sub(r"[^A-Za-z0-9._-]+", "__", ch)[:150]


def amostra(grupos, fracao, rnd):
    out = []
    for k in sorted(grupos):
        g = sorted(grupos[k], key=lambda x: x["chave"])
        n = max(1, round(len(g) * fracao))
        out += [dict(x, estrato=k) for x in rnd.sample(g, min(n, len(g)))]
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fracao", type=float, default=0.1)
    a = ap.parse_args()
    rnd = random.Random(20261013)
    os.makedirs(E("auditoria", "pacotes"), exist_ok=True)
    fila = []
    # conferência
    g = collections.defaultdict(list)
    for p in glob.glob(E("conferencia", "respostas", "*.json")):
        r = json.load(open(p, encoding="utf-8"))
        fonte = "site" if r["chave"].startswith("web:") else "readme"
        g[f'{r.get("resultado")}/{fonte}'].append({"chave": r["chave"], "conf": r})
    for x in amostra(g, a.fracao, rnd):
        pac = json.load(open(E("conferencia", "pacotes", slug(x["chave"]) + ".json"), encoding="utf-8"))
        pac["conferencia_sonnet"] = x["conf"]
        json.dump(pac, open(E("auditoria", "pacotes", slug(x["chave"]) + ".json"), "w", encoding="utf-8"),
                  ensure_ascii=False, indent=1)
        fila.append({"chave": x["chave"], "slug": slug(x["chave"]), "tipo": "conferencia", "estrato": x["estrato"]})
    # conceitos
    g = collections.defaultdict(list)
    for p in glob.glob(E("conceitos", "respostas", "*.json")):
        r = json.load(open(p, encoding="utf-8"))
        o = r.get("resposta") or {}
        g["duvida" if o.get("doubt") else o.get("serve")].append({"chave": r["chave"], "resp": r})
    for x in amostra(g, a.fracao, rnd):
        s = slug(x["chave"])
        pac = json.load(open(E("conceitos", "cartoes", s + ".json"), encoding="utf-8"))
        pac["triagem"] = x["resp"]
        json.dump(pac, open(E("auditoria", "pacotes", s + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        fila.append({"chave": x["chave"], "slug": s, "tipo": "conceito", "estrato": x["estrato"]})
    json.dump(fila, open(E("auditoria", "fila.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    c = collections.Counter(f["tipo"] for f in fila)
    print(len(fila), "na amostra:", dict(c), dict(collections.Counter(f["estrato"] for f in fila)))


if __name__ == "__main__":
    main()
