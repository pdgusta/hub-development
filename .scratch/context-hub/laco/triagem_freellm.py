"""Etapa 2 do pós-laço, metade FreeLLMAPI: cada item sorteado para "freellm" é triado por 2 modelos de famílias
e pools diferentes, com o roteamento do despachante (mesmo banco, mesmo orçamento por modelo).

O prompt é `etapas/triagem/prompt.md` (o mesmo dos subagentes Haiku), com o cartão do item no lugar de {CARTAO}.
Cada resposta aceita vira uma linha em `etapas/triagem/freellm.jsonl`; as recusadas vão para
`etapas/triagem/freellm-erros.jsonl`. Retoma: item com 2 respostas aceitas não é pedido de novo.

Uso:
    python triagem_freellm.py --sortear            (sorteia as metades, uma vez; semente fixa)
    python triagem_freellm.py --sortear-novos web: (acrescenta os cartões de site, sem refazer o sorteio)
    python triagem_freellm.py --trabalhadores 20   (roda até acabar, até o teto ou até `parar_triagem`)
Parar: python -c "from comum import *; c=abrir_banco(); gravar_controle(c,'parar_triagem',True)"
"""
import argparse, collections, glob, json, os, random, re, threading, time
from comum import abrir_banco, agora, anexar, cabecalho, carregar_config, extrair_json, http, iso, ler_controle
import despachante
from gerador import classificar

AQUI = os.path.dirname(os.path.abspath(__file__))
E = lambda *p: os.path.join(AQUI, "etapas", *p)
SAIDA, ERROS = E("triagem", "freellm.jsonl"), E("triagem", "freellm-erros.jsonl")
ENUM = {
    "serve": {"search", "stack", "none"},
    "mcp": {"yes", "no", "unknown"}, "windows": {"yes", "no", "unknown"}, "portuguese": {"yes", "no", "unknown"},
    "maturity": {"stable", "beta", "alpha", "archived", "unknown"},
}
LISTAS = {
    "place": {"disk", "inside_db_mcp", "network_service", "light_client", "library", "n/a"},
    "mechanism": {"bm25", "full_text", "vector", "hybrid", "grep", "graph", "reranker", "embeddings", "other", "n/a"},
}
trava = threading.Lock()


def validar(o):
    if not isinstance(o, dict):
        return "the answer must be one JSON object"
    for k, ok in ENUM.items():
        if o.get(k) not in ok:
            return f'"{k}" must be one of {sorted(ok)}'
    for k, ok in LISTAS.items():
        v = o.get(k)
        if not isinstance(v, list) or not v or any(x not in ok for x in v):
            return f'"{k}" must be a non-empty list with values from {sorted(ok)}'
    if not isinstance(o.get("doubt"), bool):
        return '"doubt" must be true or false'
    for k in ("role", "license", "evidence"):
        if not isinstance(o.get(k), str):
            return f'"{k}" must be a string'
    return None


def sortear():
    cartoes = sorted(glob.glob(E("cartoes", "*.json")))
    elegiveis = []
    for f in cartoes:
        c = json.load(open(f, encoding="utf-8"))
        if c.get("readme_status") == "ok":
            elegiveis.append(c["chave"])
    rnd = random.Random(20261013)
    rnd.shuffle(elegiveis)
    meio = len(elegiveis) // 2
    s = {ch: ("freellm" if n < meio else "haiku") for n, ch in enumerate(elegiveis)}
    json.dump(s, open(E("triagem", "sorteio.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    print(len(elegiveis), "itens com README;", collections.Counter(s.values()))


def sortear_novos(prefixo):
    """Acrescenta ao sorteio os cartões novos com a chave começando por `prefixo`, sem mexer nos já sorteados."""
    s = json.load(open(E("triagem", "sorteio.json"), encoding="utf-8"))
    novos = []
    for f in sorted(glob.glob(E("cartoes", "*.json"))):
        c = json.load(open(f, encoding="utf-8"))
        if c["chave"].startswith(prefixo) and c.get("readme_status") == "ok" and c["chave"] not in s:
            novos.append(c["chave"])
    rnd = random.Random(f"20261013-{prefixo}")
    rnd.shuffle(novos)
    for n, ch in enumerate(novos):
        s[ch] = "freellm" if n < len(novos) // 2 else "haiku"
    json.dump(s, open(E("triagem", "sorteio.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    print(len(novos), "novos;", collections.Counter(s[ch] for ch in novos))


def slug(ch):
    """O mesmo de baixar_sites.py; para chaves gh: dá o mesmo que trocar ":" e "/" por "__"."""
    return re.sub(r"[^A-Za-z0-9._-]+", "__", ch)[:150]


def chamar(con, cfg, m, prompt):
    corpo = {"model": m["id"], "messages": [{"role": "user", "content": prompt}], "temperature": 0.1,
             "max_tokens": cfg["max_tokens_raciocina"] if m["raciocina"] else cfg["max_tokens"]}
    t0 = agora()
    st, h, d = http(cfg, "POST", "/v1/chat/completions", corpo, timeout=cfg["timeout_s"])
    extra = int(cabecalho(h, "X-Fallback-Attempts") or 0)
    tipo, msg = classificar(st, h, d)
    esc = ((d.get("choices") or [{}])[0]) if isinstance(d, dict) else {}
    texto = (esc.get("message") or {}).get("content") or ""
    reg = {"ts": iso(), "modelo": m["id"], "familia": m["familia"], "pool": m["pool"], "http": st,
           "latencia_s": round(agora() - t0, 1), "fim": esc.get("finish_reason"),
           "uso": d.get("usage") if isinstance(d, dict) else None}
    return tipo, msg, texto, extra, reg


def triar_vaga(con, cfg, chave, prompt, ja):
    """Uma resposta aceita de um modelo de outra família/pool que as já aceitas. Devolve o registro ou None."""
    fam = ja[0]["familia"] if ja else None
    pool = ja[0]["pool"] if ja else None
    excluir = {r["modelo"] for r in ja}
    tentados = 0
    while tentados < cfg["max_modelos_por_pedido"]:
        m = despachante.escolher(con, cfg, excluir=excluir, familia_proibida=fam, pool_proibido=pool)
        if m == "teto":
            return "teto"
        if m is None:
            if ler_controle(con, "parar_triagem", False):
                return "teto"
            time.sleep(cfg["espera_sem_modelo_s"] * (0.5 + random.random()))
            continue
        tentados += 1
        p = prompt
        for reenvio in range(cfg["reenvios_json"] + 1):
            tipo, msg, texto, extra, reg = chamar(con, cfg, m, p)
            reg.update(chave=chave, reenvio=reenvio)
            if tipo != "200":
                anexar(ERROS, dict(reg, estado=tipo, erro=msg[:300]))
                despachante.liberar(con, cfg, m["id"], m["plataforma"], tipo, extra)
                break
            o = extrair_json(texto)
            erro = validar(o) if o is not None else ("no JSON object found" if texto.strip() else "empty answer")
            if erro is None:
                despachante.liberar(con, cfg, m["id"], m["plataforma"], "ok", extra)
                return dict(reg, estado="aceito", resposta=o)
            anexar(ERROS, dict(reg, estado="invalido", erro=erro, conteudo=texto[:1500]))
            if reenvio == cfg["reenvios_json"] or not texto.strip():
                despachante.liberar(con, cfg, m["id"], m["plataforma"], "invalido", extra)
                break
            con.execute("""INSERT INTO uso VALUES (?,?,?) ON CONFLICT(modelo, janela) DO UPDATE SET tentativas = tentativas + ?""",
                        (m["id"], despachante.janela(cfg, m["plataforma"]), 1 + extra, 1 + extra))
            p = prompt + f"\n\nYour previous answer was rejected: {erro}. Reply again with ONLY the JSON object."
        excluir.add(m["id"])
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sortear", action="store_true")
    ap.add_argument("--sortear-novos", metavar="PREFIXO", help='ex.: "web:" para os sites')
    ap.add_argument("--trabalhadores", type=int, default=20)
    ap.add_argument("--limite", type=int, default=0, help="só os N primeiros itens (piloto)")
    a = ap.parse_args()
    if a.sortear:
        sortear()
        return
    if a.sortear_novos:
        sortear_novos(a.sortear_novos)
        return
    cfg = carregar_config()
    modelo_prompt = open(E("triagem", "prompt.md"), encoding="utf-8").read()
    sorteio = json.load(open(E("triagem", "sorteio.json"), encoding="utf-8"))
    feitas = collections.defaultdict(list)
    if os.path.exists(SAIDA):
        for l in open(SAIDA, encoding="utf-8"):
            r = json.loads(l)
            feitas[r["chave"]].append(r)
    fila = [ch for ch, metade in sorted(sorteio.items()) if metade == "freellm" and len(feitas[ch]) < 2]
    if a.limite:
        fila = fila[:a.limite]
    print(iso(), len(fila), "itens a triar", flush=True)
    vivo = [True]

    def trabalhar():
        con = abrir_banco()
        while vivo[0]:
            if ler_controle(con, "parar_triagem", False):
                return
            with trava:
                if not fila:
                    return
                ch = fila.pop(0)
            cartao = json.load(open(E("cartoes", slug(ch) + ".json"), encoding="utf-8"))
            c = {k: cartao.get(k) for k in ("chave", "nomes", "urls", "readme_cortado", "readme")}
            prompt = modelo_prompt.replace("{CARTAO}", json.dumps(c, ensure_ascii=False, indent=1))
            try:
                while len(feitas[ch]) < 2:
                    r = triar_vaga(con, cfg, ch, prompt, feitas[ch])
                    if r == "teto":
                        vivo[0] = False
                        return
                    if r is None:
                        anexar(ERROS, {"ts": iso(), "chave": ch, "estado": "esgotado", "vaga": len(feitas[ch])})
                        break
                    with trava:
                        feitas[ch].append(r)
                        anexar(SAIDA, r)
            except Exception as e:
                anexar(ERROS, {"ts": iso(), "chave": ch, "estado": "erro_do_script", "erro": repr(e)[:300]})
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
    print(iso(), "fim;", sum(1 for ch in sorteio if sorteio[ch] == "freellm" and len(feitas[ch]) >= 2), "itens com 2 respostas",
          flush=True)


if __name__ == "__main__":
    main()
