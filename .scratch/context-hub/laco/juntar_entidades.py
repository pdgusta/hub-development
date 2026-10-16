"""Cobertura, passo 1: segunda junção de entidades, depois de `consolidar.py`. Nenhum modelo é chamado.

O consolidar junta só pelo nome-base idêntico, então "Lucene", "Apache Lucene QueryParser" e "Lucene.NET" ficaram
separados. Aqui, uma entidade vira candidata a filha de outra quando:
- as duas citam o mesmo repositório do GitHub (mesmo projeto); ou
- as palavras do nome-base da mãe estão todas no nome da filha, e a mãe tem ao menos uma palavra própria (não
  genérica) com 4 letras ou mais.

Cada filha fica com uma mãe só: a mais citada entre as possíveis. As outras ficam anotadas em `tambem`. Os grupos vão
a `sintese/entidades2-candidatos.json` ("mae" é só o nome do grupo, a mais citada; ela também está nos membros) para um juiz, que devolve a partição do
grupo em `sintese/entidades2-decisoes.jsonl`:
{"grupo": "<mae proposta>", "entidades": [{"principal": "<chave>", "mesmo": ["<chave>"], "parte": ["<chave>"]}, ...]}
- "nome" (opcional): o nome que a entidade passa a ter (quando a principal tem nome de imagem, cliente etc.);
- "principal": a entidade que fica (pode ser qualquer membro do grupo, não só a mãe proposta);
- "mesmo": a mesma entidade com outro nome; chaves, URLs, menções e famílias somam na principal;
- "parte": cliente, plugin, imagem, recurso, modelo ou modo da principal; entra em `componentes` dela e também soma;
- cada entidade é citada pela `chave` dela no candidato (a primeira chave, única; dois membros podem ter o mesmo nome);
- membro que não aparece em lugar nenhum fica separado, como está.
Grupo sem decisão fica como está e reaparece nos candidatos.

Ajustes à mão do maestro, depois do juiz, em `sintese/entidades2-ajustes.json`:
{"renomear": {"<chave>": "<nome>"}, "juntar": [["<chave principal>", "<chave igual>", ...]]} ("juntar" é "mesmo").

Saída: sintese/catalogo-entidades.json (o catálogo depois da junção).
Uso: python juntar_entidades.py
"""
import collections, json, os, re

from consolidar import base

AQUI = os.path.dirname(os.path.abspath(__file__))
S = lambda *p: os.path.join(AQUI, "sintese", *p)
GENERICAS = {"portuguese", "stemmer", "stemming", "analyzer", "analysis", "vector", "hybrid", "client", "clients",
             "plugin", "plugins", "index", "model", "models", "embeddings", "embed", "text", "full", "semantic",
             "markdown", "frontmatter", "multilingual", "sentence", "transformers", "obsidian", "couchdb", "docker",
             "image", "node", "python", "pipeline", "ingest", "query", "cloud", "sdk", "yaml", "change", "feed"}


def repos(e):
    s = set()
    for u in e["urls"]:
        m = re.search(r"github\.com/([^/\s]+)/([^/\s#?]+)", u, re.I)
        if m:
            s.add((m.group(1) + "/" + m.group(2)).lower().removesuffix(".git"))
    return s


def candidatos(cat):
    n = len(cat)
    toks = [set(base(e["nome"]).split()) for e in cat]
    pode_ser_mae = [bool(t - GENERICAS) and any(len(x) >= 4 for x in t - GENERICAS) for t in toks]
    maes = collections.defaultdict(set)  # filha -> mães possíveis
    por_repo = collections.defaultdict(list)
    for i, e in enumerate(cat):
        for r in repos(e):
            por_repo[r].append(i)
    for ix in por_repo.values():
        for j in ix:
            maes[j].update(k for k in ix if k != j)
    for i in range(n):
        if not pode_ser_mae[i]:
            continue
        for j in range(n):
            if i != j and toks[i] < toks[j]:
                maes[j].add(i)
    # componentes ligados (mãe e filhas, em qualquer sentido); a mãe do grupo é a mais citada dele
    par = list(range(n))
    def acha(i):
        while par[i] != i:
            par[i] = par[par[i]]
            i = par[i]
        return i
    for j, ms in maes.items():
        for m in ms:
            par[acha(j)] = acha(m)
    comp = collections.defaultdict(list)
    for i in range(n):
        comp[acha(i)].append(i)
    grupos, tambem = {}, {}
    for ix in comp.values():
        if len(ix) > 1:
            m = max(ix, key=lambda k: (cat[k]["mencoes"], -k))
            grupos[m] = [j for j in ix if j != m]
            for j in grupos[m]:
                tambem[j] = sorted(cat[k]["nome"] for k in maes.get(j, ()) if k != m)
    return grupos, tambem


def main():
    cat = json.load(open(S("catalogo-final.json"), encoding="utf-8"))
    dec = {}
    if os.path.exists(S("entidades2-decisoes.jsonl")):
        for l in open(S("entidades2-decisoes.jsonl"), encoding="utf-8"):
            if l.strip():
                r = json.loads(l)
                dec[r["grupo"]] = r["entidades"]
    grupos, tambem = candidatos(cat)
    abs_ = set()  # índices absorvidos por uma principal
    pend = []
    saida = [dict(e, componentes=[]) for e in cat]
    for m, filhas in grupos.items():
        d = dec.get(cat[m]["nome"])
        if d is None:
            pend.append({"mae": cat[m]["nome"],
                         "membros": [{"nome": cat[j]["nome"], "chave": cat[j]["chaves"][0], "mencoes": cat[j]["mencoes"],
                                      "serve": cat[j]["registro"].get("serve"), "papel": cat[j]["registro"].get("role"),
                                      "urls": cat[j]["urls"][:3], "tambem_contem": tambem.get(j, [])}
                                     for j in [m] + filhas]})
            continue
        idx = {cat[i]["chaves"][0]: i for i in [m] + filhas}
        for ent in d:
            p = idx[ent["principal"]]
            if ent.get("nome"):
                saida[p]["nome"] = ent["nome"]
            for tipo in ("mesmo", "parte"):
                for ch in ent.get(tipo) or []:
                    j = idx[ch]
                    alvo, f = saida[p], cat[j]
                    alvo["chaves"] = alvo["chaves"] + f["chaves"]
                    alvo["urls"] = sorted(set(alvo["urls"]) | set(f["urls"]))
                    alvo["mencoes"] += f["mencoes"]
                    alvo["familias"] = sorted(set(alvo["familias"]) | set(f["familias"]))
                    if tipo == "parte":
                        alvo["componentes"].append({"nome": f["nome"], "papel": f["registro"].get("role"),
                                                    "serve": f["registro"].get("serve")})
                    abs_.add(j)
    aj = json.load(open(S("entidades2-ajustes.json"), encoding="utf-8")) if os.path.exists(S("entidades2-ajustes.json")) else {}
    por_chave = {e["chaves"][0]: i for i, e in enumerate(saida) if i not in abs_}
    for ks in aj.get("juntar", []):
        p = por_chave[ks[0]]
        for k in ks[1:]:
            j, alvo = por_chave[k], saida[por_chave[ks[0]]]
            f = saida[j]
            alvo["chaves"] = alvo["chaves"] + f["chaves"]
            alvo["urls"] = sorted(set(alvo["urls"]) | set(f["urls"]))
            alvo["mencoes"] += f["mencoes"]
            alvo["familias"] = sorted(set(alvo["familias"]) | set(f["familias"]))
            alvo["componentes"] += f["componentes"]
            abs_.add(j)
    for k, nome in aj.get("renomear", {}).items():
        saida[por_chave[k]]["nome"] = nome
    final = [e for i, e in enumerate(saida) if i not in abs_]
    final.sort(key=lambda e: -e["mencoes"])
    json.dump(final, open(S("catalogo-entidades.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump(pend, open(S("entidades2-candidatos.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    serve = collections.Counter(e["registro"].get("serve") for e in final)
    print(len(cat), "->", len(final), "entidades;", dict(serve), ";", len(pend), "grupos sem decisão,",
          sum(len(g["membros"]) for g in pend), "membros")


if __name__ == "__main__":
    main()
