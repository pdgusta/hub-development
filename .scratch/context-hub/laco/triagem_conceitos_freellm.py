"""Conceitos pelo FreeLLMAPI (pedido do Gustavo: 200 conceitos sorteados saem dos Haiku para ir mais rápido).

Um modelo por conceito, pelo roteamento do despachante. Prompt: etapas/conceitos/prompt.md. A resposta aceita é
gravada em etapas/conceitos/respostas/<slug>.json, no mesmo formato dos subagentes (assim a Osmose pula o item), e
também em etapas/conceitos/freellm.jsonl; recusas em etapas/conceitos/freellm-erros.jsonl.

Uso:
    python triagem_conceitos_freellm.py --reservar 200   (sorteia os 200 da parte da fila que a Osmose ainda não pegou)
    python triagem_conceitos_freellm.py --trabalhadores 20
"""
import argparse, json, os, random, threading
from comum import abrir_banco, anexar, carregar_config, iso, ler_controle
import triagem_freellm as tf

AQUI = os.path.dirname(os.path.abspath(__file__))
C = lambda *p: os.path.join(AQUI, "etapas", "conceitos", *p)
SERVE = {"search", "stack", "none"}
MEC = {"bm25", "full_text", "vector", "hybrid", "grep", "graph", "reranker", "embeddings", "other", "n/a"}
LUGAR = {"disk", "inside_db_mcp", "network_service", "light_client", "library", "n/a"}


def validar(o):
    if not isinstance(o, dict):
        return "the answer must be one JSON object"
    if not isinstance(o.get("concept_en"), str) or not o["concept_en"].strip():
        return '"concept_en" must be a non-empty string'
    if o.get("serve") not in SERVE:
        return f'"serve" must be one of {sorted(SERVE)}'
    for k, ok in (("mechanism", MEC), ("place", LUGAR)):
        v = o.get(k)
        if not isinstance(v, list) or not v or any(x not in ok for x in v):
            return f'"{k}" must be a non-empty list with values from {sorted(ok)}'
    if not isinstance(o.get("tools_on_card"), list):
        return '"tools_on_card" must be a list of strings'
    if not isinstance(o.get("doubt"), bool):
        return '"doubt" must be true or false'
    for k in ("role", "evidence"):
        if not isinstance(o.get(k), str):
            return f'"{k}" must be a string'
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--reservar", type=int)
    ap.add_argument("--trabalhadores", type=int, default=20)
    a = ap.parse_args()
    fila = json.load(open(C("fila.json"), encoding="utf-8"))
    if a.reservar:
        # a Osmose vai do fim para o início; a 1ª leva dela (19 x 25) cobre as posições 399 a 873
        livres = [f for f in fila[25:399] if not os.path.exists(C("respostas", f["slug"] + ".json"))]
        res = random.Random(20261013).sample(livres, min(a.reservar, len(livres)))
        json.dump(res, open(C("freellm-reservados.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=0)
        print(len(res), "reservados de", len(livres), "livres")
        return
    tf.validar, tf.ERROS = validar, C("freellm-erros.jsonl")
    cfg = carregar_config()
    modelo_prompt = open(C("prompt.md"), encoding="utf-8").read()
    res = json.load(open(C("freellm-reservados.json"), encoding="utf-8"))
    pend = [f for f in res if not os.path.exists(C("respostas", f["slug"] + ".json"))]
    print(iso(), len(pend), "conceitos a triar", flush=True)
    trava = threading.Lock()

    def trabalhar():
        con = abrir_banco()
        while True:
            if ler_controle(con, "parar_triagem", False):
                return
            with trava:
                if not pend:
                    return
                f = pend.pop(0)
            cartao = json.load(open(C("cartoes", f["slug"] + ".json"), encoding="utf-8"))
            prompt = modelo_prompt.replace("{CARTAO}", json.dumps(cartao, ensure_ascii=False, indent=1))
            try:
                r = tf.triar_vaga(con, cfg, f["chave"], prompt, [])
            except Exception as e:
                anexar(tf.ERROS, {"ts": iso(), "chave": f["chave"], "estado": "erro_do_script", "erro": repr(e)[:300]})
                try:
                    con.execute("ROLLBACK")
                except Exception:
                    pass
                continue
            if r == "teto":
                return
            if r is None:
                anexar(tf.ERROS, {"ts": iso(), "chave": f["chave"], "estado": "esgotado"})
                continue
            anexar(C("freellm.jsonl"), r)
            saida = {"chave": f["chave"], "modelo": r["modelo"], "ts": r["ts"], "resposta": r["resposta"], "via": "freellmapi"}
            json.dump(saida, open(C("respostas", f["slug"] + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    ts = [threading.Thread(target=trabalhar, daemon=True) for _ in range(a.trabalhadores)]
    for t in ts:
        t.start()
    for t in ts:
        t.join()
    print(iso(), "fim;", sum(1 for f in res if os.path.exists(C("respostas", f["slug"] + ".json"))), "de", len(res), flush=True)


if __name__ == "__main__":
    main()
