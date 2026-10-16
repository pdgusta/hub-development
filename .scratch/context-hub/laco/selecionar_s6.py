"""Cobertura, passo 4: a segunda lista da régua com fonte (S6), por regra. Nenhum modelo é chamado.

Regra (gravada também em `sintese/s6-lista.json`):
- Busca: as 20 entidades mais citadas que ainda não têm régua conferida, tirando os serviços só na nuvem (SAAS), mais
  todas as sem régua dos lugares que ficaram vazios no laço: dentro do MCP do banco, cópia leve no cliente, e grep no
  disco.
- Stack: em cada área do hub (menos "other"), as 3 mais citadas em que os modelos que acertaram a área deram,
  todos, encaixe "central", tirando o que já está decidido no mapa (CouchDB e os recursos dele, a especificação do
  MCP, o registro de plugins do Obsidian), runtime genérico (Node.js) e o que a síntese já tirou com motivo
  (DistilBERT, fastText: não são embeddings de trechos).
Lotes de 4 em `sintese/s6-lotes.json`, com a busca primeiro.

Uso: python selecionar_s6.py
"""
import collections, json, os
import inventario as inv

AQUI = os.path.dirname(os.path.abspath(__file__))
S = lambda *p: os.path.join(AQUI, "sintese", *p)
SAAS = {"Algolia", "Cohere"}
FORA_STACK = {"Node.js": "runtime genérico", "DistilBERT": "a síntese já tirou: não é embedding de trechos",
              "fastText": "a síntese já tirou: não é embedding de trechos",
              "MCP (Model Context Protocol)": "decidido no mapa", "Obsidian (registro de plugins)": "decidido no mapa"}
LUGARES_VAZIOS = {"inside_db_mcp", "light_client"}


def main():
    cat = json.load(open(S("catalogo-entidades.json"), encoding="utf-8"))
    areas = {a["chave"]: a for a in json.load(open(S("stack-areas.json"), encoding="utf-8"))}
    fichas = inv.reguas()
    urls = {inv.url_norm(f.get("url")) for f in fichas.values()}
    nomes = {inv.norm(f.get("nome")) for f in fichas.values()}
    for f in fichas.values():  # "Tantivy / tantivy-py", "SQLite FTS5 + sqlite-vec"...
        for parte in (f.get("nome") or "").replace("+", "/").split("/"):
            nomes.add(inv.norm(parte))
    tem = lambda e: any(inv.url_norm(u) in urls for u in e["urls"]) or inv.norm(e["nome"]) in nomes
    item = lambda e, motivo, area=None: {"nome": e["nome"], "chave": e["chaves"][0], "urls": e["urls"][:4],
                                         "papel": e["registro"].get("role"), "serve": e["registro"].get("serve"),
                                         "area": area, "motivo": motivo}
    busca = [e for e in cat if e["registro"].get("serve") == "search" and not tem(e) and e["nome"] not in SAAS]
    lista = [item(e, "busca: 20 mais citadas sem régua") for e in busca[:20]]
    lista += [item(e, "busca: lugar vazio no laço (" + ", ".join(sorted(set(e["registro"].get("place") or []) & LUGARES_VAZIOS)
                                                                  or ["grep no disco"]) + ")")
              for e in busca[20:] if set(e["registro"].get("place") or []) & LUGARES_VAZIOS
              or "grep" in (e["registro"].get("mechanism") or [])]
    por_area, fora = collections.defaultdict(list), []
    for e in cat:
        a = areas.get(e["chaves"][0])
        if e["registro"].get("serve") != "stack" or not a or not a.get("area") or a["area"] == "other" or tem(e):
            continue
        certos = [r for r in a["respostas"] if r["area"] == a["area"]]
        if not certos or any(r["fit"] != "core" for r in certos):
            continue
        if e["nome"] in FORA_STACK or e["nome"].lower().startswith("couchdb"):
            fora.append({"nome": e["nome"], "motivo": FORA_STACK.get(e["nome"], "decidido no mapa (CouchDB)")})
            continue
        por_area[a["area"]].append(e)
    for area, es in por_area.items():
        lista += [item(e, f"stack: 3 mais citadas da área {area} com encaixe central unânime", area) for e in es[:3]]
    lotes = [lista[i:i + 4] for i in range(0, len(lista), 4)]
    json.dump({"regra": __doc__.split("Regra")[1].split("Lotes")[0].strip(), "fora_por_regra": fora, "itens": lista},
              open(S("s6-lista.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump(lotes, open(S("s6-lotes.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(len(lista), "itens em", len(lotes), "lotes;", collections.Counter(i["serve"] for i in lista))
    for i in lista:
        print(" ", i["serve"], "|", i["area"] or "", "|", i["nome"])


if __name__ == "__main__":
    main()
