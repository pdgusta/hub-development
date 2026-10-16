"""Síntese S1: consolida o catálogo depois da auditoria. Nenhum modelo é chamado.

Registro final de cada item: auditoria do Opus > conferência do Sonnet > triagem (marcada "sem conferência").
Entidades: junta chaves gh:/web:/nome: que são o mesmo projeto, pelo nome-base (sem parênteses, sem enfeite) e pelo
domínio/repositório; grupos com mais de uma chave útil vão a `sintese/entidades-ambiguas.json` para um juiz decidir,
e as decisões dele em `sintese/entidades-decisoes.jsonl` ({"grupo": "<nome-base>", "entidades": [[chaves do mesmo
projeto], [outra], ...]}) valem na rodada seguinte. Conceitos: agrupados por concept_en; entram os citados por 2+ cartões ou ligados a um projeto.

Saídas em sintese/: catalogo-final.json, conceitos-final.json, tabelas.md.
Uso: python consolidar.py
"""
import collections, glob, json, os, re, unicodedata

AQUI = os.path.dirname(os.path.abspath(__file__))
E = lambda *p: os.path.join(AQUI, "etapas", *p)
S = lambda *p: os.path.join(AQUI, "sintese", *p)
ENFEITE = r"\b(local|mode|modo|self ?hosted|server|search|engine|db|database|python|js|rs|go|lib|library|the|cli|mcp|" \
          r"plugin|api|core|oss|open source|community|edition)\b"


def ler(p, padrao=None):
    try:
        return json.load(open(p, encoding="utf-8"))
    except (OSError, ValueError):
        return padrao


def base(nome):
    n = re.sub(r"\(.*?\)|\[.*?\]|\*", " ", nome)
    n = unicodedata.normalize("NFKD", n).encode("ascii", "ignore").decode().lower()
    n = re.sub(r"[^a-z0-9+]+", " ", n)
    n2 = re.sub(ENFEITE, " ", n).strip()
    return re.sub(r"\s+", " ", n2 or n).strip()


def main():
    os.makedirs(S(), exist_ok=True)
    itens = {i["chave"]: i for i in json.load(open(os.path.join(AQUI, "catalogo", "itens.json"), encoding="utf-8"))}
    final = {}
    for p in glob.glob(E("triagem", "haiku", "*.json")):
        r = ler(p)
        final[r["chave"]] = {"registro": r["resposta"], "fonte_registro": "triagem-haiku"}
    for l in open(E("triagem", "freellm.jsonl"), encoding="utf-8"):
        r = json.loads(l)
        final.setdefault(r["chave"], {"registro": r["resposta"], "fonte_registro": "triagem-freellm"})
    for p in glob.glob(E("conferencia", "respostas", "*.json")):
        r = ler(p)
        c = r.get("conferencia") or {}
        final[r["chave"]] = {"registro": c.get("final") or {}, "fonte_registro": "conferencia-sonnet",
                             "resultado_sonnet": r.get("resultado"), "nota": c.get("nota")}
    for p in glob.glob(E("auditoria", "respostas", "*.json")):
        r = ler(p)
        a = r.get("auditoria") or {}
        final[r["chave"]].update(registro=a.get("final") or final[r["chave"]]["registro"], fonte_registro="auditoria-opus",
                                 auditoria=r.get("resultado"), gravidade=a.get("gravidade"), nota=a.get("nota"))
    uteis = {k: v for k, v in final.items() if (v["registro"] or {}).get("serve") in ("search", "stack")}

    # entidades: decisões do juiz por grupo, {"grupo": base, "entidades": [[k1, k2], [k3]]}
    part = {}
    if os.path.exists(S("entidades-decisoes.jsonl")):
        for l in open(S("entidades-decisoes.jsonl"), encoding="utf-8"):
            r = json.loads(l)
            part[r["grupo"]] = [list(e) for e in r["entidades"]]
    grupos = collections.defaultdict(set)
    for k in uteis:
        grupos[base(itens[k]["nomes"][0] if k in itens else k)].add(k)
    entidades, ambiguos = [], {}
    for b, ks in grupos.items():
        if len(ks) == 1:
            entidades.append(sorted(ks))
        elif b in part and set().union(*map(set, part[b])) >= ks:
            entidades += [[k for k in e if k in ks] for e in part[b] if any(k in ks for k in e)]
        else:
            ambiguos[b] = sorted(ks)
            entidades.append(sorted(ks))  # provisório: junto até o juiz decidir

    cat = []
    for ks in entidades:
        ks = sorted(ks, key=lambda k: (0 if k.startswith("gh:") else 1 if k.startswith("web:") else 2,
                                       -itens.get(k, {}).get("mencoes", 0)))
        princ = ks[0]
        regs = [final[k] for k in ks]
        melhor = next((r for r in regs if r["fonte_registro"] == "auditoria-opus"), None) or \
            next((r for r in regs if r["fonte_registro"] == "conferencia-sonnet"), regs[0])
        cat.append({
            "nome": itens.get(princ, {}).get("nomes", [princ])[0], "chaves": ks,
            "urls": sorted({u for k in ks for u in itens.get(k, {}).get("urls", []) if u})[:8],
            "mencoes": sum(itens.get(k, {}).get("mencoes", 0) for k in ks),
            "familias": sorted({f for k in ks for f in itens.get(k, {}).get("familias", [])}),
            "registro": melhor["registro"], "fonte_registro": melhor["fonte_registro"],
            "auditoria": melhor.get("auditoria"), "nota": melhor.get("nota"),
        })
    cat.sort(key=lambda e: -e["mencoes"])
    json.dump(cat, open(S("catalogo-final.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump(ambiguos, open(S("entidades-ambiguas.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    # conceitos
    conc = collections.defaultdict(lambda: {"cartoes": [], "serve": collections.Counter(), "duvidas": 0,
                                            "ferramentas": collections.Counter(), "papeis": []})
    aud_c = {r["chave"]: r for r in (ler(p) for p in glob.glob(E("auditoria", "conceitos", "*.json"))) if r}
    nomes_proj = {base(e["nome"]) for e in cat}
    for p in glob.glob(E("conceitos", "respostas", "*.json")):
        r = ler(p)
        o = r.get("resposta") or {}
        if r["chave"] in aud_c:
            o = (aud_c[r["chave"]].get("auditoria") or {}).get("final") or o
        g = conc[(o.get("concept_en") or r["chave"]).strip().lower()]
        g["cartoes"].append(r["chave"])
        g["serve"][o.get("serve")] += 1
        g["duvidas"] += bool(o.get("doubt"))
        g["ferramentas"].update(t for t in (o.get("tools_on_card") or []) if isinstance(t, str))
        if o.get("role"):
            g["papeis"].append(o["role"])
    cf = []
    for nome, g in conc.items():
        ligado = any(base(t) in nomes_proj for t in g["ferramentas"])
        if len(g["cartoes"]) >= 2 or ligado:
            cf.append({"conceito": nome, "cartoes": len(g["cartoes"]), "serve": g["serve"].most_common(1)[0][0],
                       "duvidas": g["duvidas"], "ferramentas": [t for t, _ in g["ferramentas"].most_common(8)],
                       "ligado_a_projeto": ligado, "papel": g["papeis"][0] if g["papeis"] else ""})
    cf.sort(key=lambda c: -c["cartoes"])
    json.dump(cf, open(S("conceitos-final.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    # tabelas
    pm = collections.Counter()
    for e in cat:
        r = e["registro"]
        if r.get("serve") == "search":
            for p in r.get("place") or ["n/a"]:
                for m in r.get("mechanism") or ["n/a"]:
                    pm[(p, m)] += 1
    serve = collections.Counter(e["registro"].get("serve") for e in cat)
    md = ["# Catálogo consolidado (S1)", "",
          f"- Entidades úteis: {len(cat)} (de {len(uteis)} chaves úteis); serve: {dict(serve)}",
          f"- Grupos de entidade ambíguos para o juiz: {len(ambiguos)}",
          f"- Conceitos na síntese: {len(cf)} (de {len(conc)} grupos por concept_en)", "",
          "## Lugar × mecanismo (busca)", "", "| lugar | mecanismo | itens |", "|---|---|---|"]
    md += [f"| {p} | {m} | {n} |" for (p, m), n in pm.most_common()]
    open(S("tabelas.md"), "w", encoding="utf-8").write("\n".join(md) + "\n")
    print(len(cat), "entidades úteis;", dict(serve), ";", len(ambiguos), "grupos ambíguos;", len(cf), "conceitos")


if __name__ == "__main__":
    main()
