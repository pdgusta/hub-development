"""Cobertura, passo 2: classifica as entidades de stack por área do hub, pelo FreeLLMAPI.

Dois modelos de famílias e pools diferentes por entidade, pelo roteamento do despachante (`triagem_freellm.triar_vaga`).
Se discordarem na área principal, um terceiro modelo desempata (maioria de 3). Sem maioria, fica "divergente" com as
três respostas. Prompt em `etapas/stack/prompt.md`. Entrada: `sintese/catalogo-entidades.json` (depois da junção) ou,
na falta dele, `sintese/catalogo-final.json`. O cartão leva o registro da conferência e, quando existe, o README.

Respostas aceitas em `etapas/stack/freellm.jsonl` (retoma); recusas em `etapas/stack/freellm-erros.jsonl`. Resultado
em `sintese/stack-areas.json`.

Uso:
    python classificar_stack.py --limite 5        (piloto)
    python classificar_stack.py --trabalhadores 20
    python classificar_stack.py --juntar          (só refaz sintese/stack-areas.json)
"""
import argparse, collections, json, os, threading, time
from comum import abrir_banco, anexar, carregar_config, iso, ler_controle
import triagem_freellm as tf

AQUI = os.path.dirname(os.path.abspath(__file__))
D = lambda *p: os.path.join(AQUI, "etapas", "stack", *p)
S = lambda *p: os.path.join(AQUI, "sintese", *p)
AREAS = {"sync_couchdb", "mcp", "markdown_frontmatter", "text_pt", "embeddings_rerank", "llm_runtime",
         "text_extraction", "storage_db", "events_jobs", "api_service", "agent_framework", "obsidian", "other"}
SAIDA, ERROS = D("freellm.jsonl"), D("freellm-erros.jsonl")


def validar(o):
    if not isinstance(o, dict):
        return "the answer must be one JSON object"
    if o.get("area") not in AREAS:
        return f'"area" must be one of {sorted(AREAS)}'
    if o.get("area_2") not in AREAS | {"none"}:
        return '"area_2" must be an area id or "none"'
    if o.get("fit") not in {"core", "optional", "unlikely"}:
        return '"fit" must be "core", "optional" or "unlikely"'
    if not isinstance(o.get("hub_use"), str):
        return '"hub_use" must be a string'
    if not isinstance(o.get("doubt"), bool):
        return '"doubt" must be true or false'
    return None


def entidades():
    p = S("catalogo-entidades.json") if os.path.exists(S("catalogo-entidades.json")) else S("catalogo-final.json")
    return [e for e in json.load(open(p, encoding="utf-8")) if e["registro"].get("serve") == "stack"]


def cartao(e):
    c = {"name": e["nome"], "urls": e["urls"][:5], "role": e["registro"].get("role"),
         "evidence": e["registro"].get("evidence"), "reviewer_note": e.get("nota"),
         "components": [x["nome"] for x in e.get("componentes", [])][:10]}
    for k in e["chaves"]:
        p = os.path.join(AQUI, "etapas", "cartoes", tf.slug(k) + ".json")
        if os.path.exists(p):
            r = json.load(open(p, encoding="utf-8")).get("readme")
            if r:
                c["readme"] = r[:4000]
                break
    return c


def ler_feitas():
    feitas = collections.defaultdict(list)
    if os.path.exists(SAIDA):
        for l in open(SAIDA, encoding="utf-8"):
            r = json.loads(l)
            feitas[r["chave"]].append(r)
    return feitas


def precisa(rs):
    """Quantas respostas a entidade ainda precisa: 2, e uma 3ª se as 2 discordarem na área."""
    if len(rs) < 2:
        return True
    return len(rs) == 2 and rs[0]["resposta"]["area"] != rs[1]["resposta"]["area"]


def juntar():
    feitas = ler_feitas()
    saida, cont = [], collections.Counter()
    for e in entidades():
        rs = feitas.get(e["chaves"][0], [])
        votos = collections.Counter(r["resposta"]["area"] for r in rs)
        area, n = votos.most_common(1)[0] if votos else (None, 0)
        estado = "sem_resposta" if not rs else "acordo" if n >= 2 else "divergente" if len(rs) >= 3 else "incompleto"
        fits = collections.Counter(r["resposta"]["fit"] for r in rs if r["resposta"]["area"] == area)
        saida.append({"nome": e["nome"], "chave": e["chaves"][0], "mencoes": e["mencoes"], "estado": estado,
                      "area": area if estado == "acordo" else None, "fit": fits.most_common(1)[0][0] if fits else None,
                      "respostas": [{"modelo": r["modelo"], **r["resposta"]} for r in rs]})
        cont[estado] += 1
    json.dump(saida, open(S("stack-areas.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(len(saida), "entidades de stack;", dict(cont), ";",
          dict(collections.Counter(s["area"] for s in saida if s["area"])))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--trabalhadores", type=int, default=20)
    ap.add_argument("--limite", type=int, default=0)
    ap.add_argument("--juntar", action="store_true")
    a = ap.parse_args()
    if a.juntar:
        juntar()
        return
    os.makedirs(D(), exist_ok=True)
    tf.validar, tf.ERROS = validar, ERROS
    cfg = carregar_config()
    modelo_prompt = open(D("prompt.md"), encoding="utf-8").read()
    feitas = ler_feitas()
    ents = sorted(entidades(), key=lambda e: -e["mencoes"])
    fila = [e for e in ents if precisa(feitas[e["chaves"][0]])]
    if a.limite:
        fila = fila[:a.limite]
    print(iso(), len(fila), "entidades a classificar", flush=True)
    trava, vivo = threading.Lock(), [True]

    def trabalhar():
        con = abrir_banco()
        while vivo[0]:
            if ler_controle(con, "parar_triagem", False):
                return
            with trava:
                if not fila:
                    return
                e = fila.pop(0)
            ch = e["chaves"][0]
            prompt = modelo_prompt.replace("{CARTAO}", json.dumps(cartao(e), ensure_ascii=False, indent=1))
            try:
                while precisa(feitas[ch]):
                    # outra família e pool que a 1ª resposta, e nenhum modelo já usado
                    r = tf.triar_vaga(con, cfg, ch, prompt, feitas[ch])
                    if r == "teto":
                        vivo[0] = False
                        return
                    if r is None:
                        anexar(ERROS, {"ts": iso(), "chave": ch, "estado": "esgotado", "vaga": len(feitas[ch])})
                        break
                    with trava:
                        feitas[ch].append(r)
                        anexar(SAIDA, r)
            except Exception as ex:
                anexar(ERROS, {"ts": iso(), "chave": ch, "estado": "erro_do_script", "erro": repr(ex)[:300]})
                try:
                    con.execute("ROLLBACK")
                except Exception:
                    pass
                time.sleep(5)

    ts = [threading.Thread(target=trabalhar, daemon=True) for _ in range(a.trabalhadores)]
    for t in ts:
        t.start()
    for t in ts:
        t.join()
    juntar()


if __name__ == "__main__":
    main()
