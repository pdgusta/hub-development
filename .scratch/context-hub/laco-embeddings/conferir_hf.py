"""Confere no Hugging Face (fonte primária: a API pública de modelos) os itens hf: do catálogo da pesquisa de
embeddings (ticket 54). Nenhum modelo de linguagem é chamado.

Entra: itens hf: com 2 menções ou mais, as sementes e uma busca no próprio HF por modelos de português.
Sai: verificacao/hf.json (um registro por modelo, com o que a API diz). Retoma: o que já foi conferido não é pedido de
novo. Uso: python conferir_hf.py [--trabalhadores 6]
"""
import argparse, concurrent.futures as cf, json, os, time, urllib.error, urllib.parse, urllib.request

AQUI = os.path.dirname(os.path.abspath(__file__))
SAIDA = os.path.join(AQUI, "verificacao", "hf.json")
API = "https://huggingface.co/api/models/"
BUSCAS = ["portuguese sentence", "portuguese embedding", "pt-br sentence", "bertimbau sentence", "serafim"]


def pedir(url):
    req = urllib.request.Request(url, headers={"User-Agent": "conferencia-ticket-54"})
    for tentativa in range(3):
        try:
            with urllib.request.urlopen(req, timeout=20) as f:
                return json.load(f)
        except urllib.error.HTTPError as e:
            if e.code == 429:
                time.sleep(int(e.headers.get("Retry-After", "30")))
                continue
            return {"_erro": e.code}
        except Exception as e:  # rede
            if tentativa == 2:
                return {"_erro": type(e).__name__}
            time.sleep(3)
    return {"_erro": 429}


def resumo(repo, d):
    if "_erro" in d:
        return {"repo": repo, "existe": False, "erro": d["_erro"]}
    card = d.get("cardData") or {}
    st = d.get("safetensors") or {}
    tags = d.get("tags") or []
    return {
        "repo": d.get("id", repo), "existe": True,
        "pipeline": d.get("pipeline_tag"), "biblioteca": d.get("library_name"),
        "downloads": d.get("downloads"), "likes": d.get("likes"),
        "atualizado": d.get("lastModified"), "criado": d.get("createdAt"), "gated": d.get("gated"),
        "licenca": card.get("license") or next((t[8:] for t in tags if t.startswith("license:")), None),
        "linguas": card.get("language"),
        "parametros": st.get("total"),
        "onnx": "onnx" in tags or any("onnx" in t for t in tags),
        "gguf": "gguf" in tags,
        "sentence_transformers": "sentence-transformers" in tags,
        "multilingual": "multilingual" in tags or (isinstance(card.get("language"), list) and len(card["language"]) > 5),
        "pt": "pt" in tags or (isinstance(card.get("language"), list) and "pt" in card["language"]) or card.get("language") == "pt",
        "base": card.get("base_model"),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--trabalhadores", type=int, default=6)
    a = ap.parse_args()
    itens = json.load(open(os.path.join(AQUI, "catalogo", "itens.json"), encoding="utf-8"))
    sementes = json.load(open(os.path.join(AQUI, "sementes.json"), encoding="utf-8"))["sementes"]
    alvos = {}
    for i in itens:
        if i["chave"].startswith("hf:") and i["mencoes"] >= 2:
            alvos[i["chave"][3:]] = {"mencoes": i["mencoes"], "familias": len(i["familias"]), "origem": "catalogo"}
    for s in sementes:
        for u in s["urls"]:
            if "huggingface.co/" in u:
                alvos.setdefault(u.split("huggingface.co/")[1].lower(), {"mencoes": 0, "familias": 0, "origem": "semente"})
    for q in BUSCAS:
        url = API[:-1] + "?" + urllib.parse.urlencode({"search": q, "sort": "downloads", "limit": 30})
        achados = pedir(url)
        for m in achados if isinstance(achados, list) else []:
            alvos.setdefault(m["id"].lower(), {"mencoes": 0, "familias": 0, "origem": "busca-hf:" + q})
    feito = {}
    if os.path.exists(SAIDA):
        feito = {r["chave"]: r for r in json.load(open(SAIDA, encoding="utf-8"))}
    falta = [k for k in alvos if k not in feito]
    print(len(alvos), "alvos;", len(falta), "a conferir")
    with cf.ThreadPoolExecutor(a.trabalhadores) as ex:
        for k, d in zip(falta, ex.map(lambda k: pedir(API + k), falta)):
            feito[k] = {"chave": k, **alvos[k], **resumo(k, d)}
    os.makedirs(os.path.dirname(SAIDA), exist_ok=True)
    json.dump(sorted(feito.values(), key=lambda r: -(r.get("mencoes") or 0)), open(SAIDA, "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print("existem:", sum(1 for r in feito.values() if r["existe"]), "de", len(feito))


if __name__ == "__main__":
    main()
