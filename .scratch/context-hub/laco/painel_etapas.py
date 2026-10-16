"""Dados do painel das etapas depois do laço: grava `painel/etapas.js` (window.ETAPAS = {...}).

Lê só arquivos (nenhum modelo é chamado). Uso:
    python painel_etapas.py              (grava uma vez)
    python painel_etapas.py --servico    (grava a cada 60 s)

Onde cada etapa grava (tudo em `etapas/`):
    marcos.json                 estado de cada etapa (o maestro escreve): {"1": {"estado": "em_curso", "inicio": ts}, ...}
    readmes/indice.json         {chave: {"status": "ok"|"sem_readme"|"morto"|"bloqueado"|"erro", "arquivo": ...}}
    cartoes/<slug>.json         o cartão do item, com o README
    triagem/sorteio.json        {chave: "freellm"|"haiku"}
    triagem/freellm.jsonl       uma linha por resposta de modelo do FreeLLMAPI
    triagem/haiku/<slug>.json   uma resposta de subagente Haiku
    conferencia/respostas/<slug>.json  uma conferência de subagente Sonnet
    auditoria/respostas/<slug>.json    uma auditoria do Opus (auditoria/conceitos/ para os conceitos)
"""
import argparse, collections, glob, json, os, time
from datetime import datetime, timezone

AQUI = os.path.dirname(os.path.abspath(__file__))
E = lambda *p: os.path.join(AQUI, "etapas", *p)
NOMES = {1: "Limpar", 2: "Triagem", 3: "Conferência", 4: "Auditoria", 5: "Síntese"}


def ler_json(p, padrao):
    try:
        return json.load(open(p, encoding="utf-8"))
    except (OSError, ValueError):
        return padrao


def ler_jsonl(p):
    try:
        return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]
    except OSError:
        return []


def pasta_json(*p):
    out = []
    for f in glob.glob(E(*p, "*.json")):
        r = ler_json(f, None)
        if isinstance(r, dict):
            out.append(r)
    return out


def coletar():
    marcos = ler_json(E("marcos.json"), {})
    itens = ler_json(os.path.join(AQUI, "catalogo", "itens.json"), [])
    ambiguos = ler_json(os.path.join(AQUI, "catalogo", "ambiguos.json"), {})
    tocadas, separados = set(), set()
    for r in ler_jsonl(os.path.join(AQUI, "catalogo", "decisoes.jsonl")):
        if "separar" in r:
            separados.add(r["separar"])
        tocadas.update(r.get("juntar", []))
        if "quarentena" in r:
            tocadas.add(r["quarentena"])
    amb_feitos = sum(1 for n, chs in ambiguos.items() if n in separados or tocadas & set(chs))

    urls = ler_json(os.path.join(AQUI, "verificacao", "urls.json"), {})
    urls_st = collections.Counter(str(v) for v in urls.values())
    readmes = ler_json(E("readmes", "indice.json"), {})
    rd_st = collections.Counter(v.get("status") for v in readmes.values())
    alvo_readme = sum(1 for i in itens if i["chave"].startswith("gh:") and not i.get("quarentena"))

    sites = ler_json(E("sites", "indice.json"), {})
    st_sites = collections.Counter(v.get("status") for v in sites.values())
    alvo_sites = sum(1 for i in itens if i["chave"].startswith("web:") and not i.get("quarentena")
                     and i["tipos"] != ["concept"] and any(urls.get(u) == 200 for u in i["urls"] if u))
    sorteio = ler_json(E("triagem", "sorteio.json"), {})
    metade = collections.Counter(sorteio.values())
    fl = ler_jsonl(E("triagem", "freellm.jsonl"))
    fl_por_item = collections.defaultdict(list)
    for r in fl:
        fl_por_item[r.get("chave")].append(r)
    hk = pasta_json("triagem", "haiku")

    PT = {"search": "busca", "stack": "stack", "none": "nada"}

    def serve(r):
        o = r.get("resposta", r)
        return "duvida" if o.get("doubt") else PT.get(o.get("serve"), "nada")

    def por_minuto(regs):
        agora_ = time.time()
        v = [0] * 60
        for r in regs:
            try:
                t = datetime.strptime(r["ts"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc).timestamp()
            except (KeyError, ValueError, TypeError):
                continue
            k = int((agora_ - t) // 60)
            if 0 <= k < 60:
                v[k] += 1
        return v

    ver_fl, ver_hk = collections.Counter(), collections.Counter()
    discord = 0
    completos = {ch: rs for ch, rs in fl_por_item.items() if len(rs) >= 2}
    for ch, rs in completos.items():
        if len({serve(r) for r in rs[:2]}) > 1:
            discord += 1
            ver_fl["divergente"] += 1
        else:
            ver_fl[serve(rs[0])] += 1
    for r in hk:
        ver_hk[serve(r)] += 1
    veredito = ver_fl + ver_hk

    def fonte(ch):
        return "site" if ch.startswith("web:") else "readme"

    def por_fonte(chaves_feitas, vered_de, metade_nome):
        out = {}
        for f in ("readme", "site"):
            tot = sum(1 for ch, m in sorteio.items() if m == metade_nome and fonte(ch) == f)
            feitos = [ch for ch in chaves_feitas if fonte(ch) == f]
            out[f] = {"feito": len(feitos), "total": tot,
                      "veredito": dict(collections.Counter(vered_de(ch) for ch in feitos))}
        return out

    def vered_fl(ch):
        rs = completos[ch]
        return "divergente" if len({serve(r) for r in rs[:2]}) > 1 else serve(rs[0])

    hk_por = {r.get("chave"): r for r in hk}
    fl_fontes = por_fonte(list(completos), vered_fl, "freellm")
    hk_fontes = por_fonte(list(hk_por), lambda ch: serve(hk_por[ch]), "haiku")

    # conceitos (só Haiku; o resultado vai à auditoria)
    C = lambda *p: os.path.join(AQUI, "etapas", "conceitos", *p)
    fila_c = ler_json(C("fila.json"), [])
    resp_c = [r for r in (ler_json(f, None) for f in glob.glob(C("respostas", "*.json"))) if r]
    ver_c = collections.Counter(serve(r) for r in resp_c)
    conc_en = collections.Counter(((r.get("resposta") or {}).get("concept_en") or "?").lower() for r in resp_c)
    fl_modelos = collections.Counter(r.get("modelo") for r in fl)

    conf = pasta_json("conferencia", "respostas")
    conf_res = collections.Counter((r.get("resultado") or "?") for r in conf)
    aud = pasta_json("auditoria", "respostas")
    aud_res = collections.Counter((r.get("resultado") or "?") for r in aud)

    def marco(n):
        m = marcos.get(str(n), {})
        return {"n": n, "nome": NOMES[n], "estado": m.get("estado", "pendente"),
                "inicio": m.get("inicio"), "fim": m.get("fim")}

    etapas = [marco(n) for n in range(1, 6)]
    etapas[0]["partes"] = [
        {"nome": "ambíguos", "feito": amb_feitos, "total": len(ambiguos)},
        {"nome": "URLs bloqueadas", "feito": urls_st.get("200", 0) + urls_st.get("404", 0),
         "total": len(urls), "detalhe": dict(urls_st.most_common(6))},
        {"nome": "READMEs", "feito": sum(1 for i in itens if i["chave"] in readmes and not i.get("quarentena")), "total": alvo_readme, "detalhe": dict(rd_st)},
        {"nome": "sites", "feito": len(sites), "total": alvo_sites, "detalhe": dict(st_sites)},
        {"nome": "cartões de conceito", "feito": len(fila_c), "total": len(fila_c),
         "itens_do_catalogo": sum(1 for i in itens if i["tipos"] == ["concept"] and not i.get("quarentena"))},
    ]
    etapas[1]["partes"] = [
        {"nome": "FreeLLMAPI", "feito": len(completos), "total": metade.get("freellm", 0),
         "respostas": len(fl), "divergentes": discord, "modelos": dict(fl_modelos.most_common(8)),
         "veredito": dict(ver_fl), "por_minuto": por_minuto([rs[1] for rs in completos.values()]),
         "por_fonte": fl_fontes},
        {"nome": "Haiku", "feito": len(hk), "total": metade.get("haiku", 0),
         "veredito": dict(ver_hk), "por_minuto": por_minuto(hk), "por_fonte": hk_fontes},
        {"nome": "Conceitos (Haiku)", "feito": len(resp_c), "total": len(fila_c), "veredito": dict(ver_c),
         "por_minuto": por_minuto(resp_c), "conceitos_mais_comuns": dict(conc_en.most_common(15))},
    ]
    etapas[1]["veredito"] = dict(veredito)
    piloto = marcos.get("3", {}).get("piloto", {})
    etapas[2]["partes"] = [
        {"nome": "piloto", "feito": min(len(conf), piloto.get("itens", 10)), "total": piloto.get("itens", 10),
         "tokens_por_item": piloto.get("tokens_por_item")},
        {"nome": "Sonnet", "feito": len(conf), "total": marcos.get("3", {}).get("alvo", 0),
         "subagentes": marcos.get("3", {}).get("subagentes", 0)},
    ]
    etapas[2]["resultado"] = dict(conf_res)
    aud_c = pasta_json("auditoria", "conceitos")
    etapas[3]["partes"] = [{"nome": "amostra do Sonnet", "feito": len(aud), "total": marcos.get("4", {}).get("amostra", 0)},
                           {"nome": "conceitos", "feito": len(aud_c), "total": marcos.get("4", {}).get("conceitos", 0)}]
    etapas[3]["resultado"] = dict(aud_res)
    etapas[4]["partes"] = marcos.get("5", {}).get("partes", [])

    laco = ler_json(os.path.join(AQUI, "estado", "laco_final.json"), None)
    return {
        "gerado_em": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "atual": next((e["n"] for e in etapas if e["estado"] == "em_curso"), None),
        "funil": {
            "catalogo": sum(1 for i in itens if not i.get("quarentena")),
            "quarentena": sum(1 for i in itens if i.get("quarentena")),
            "com_readme": rd_st.get("ok", 0),
            "com_site": len([1 for v in sites.values() if v.get("status") == "ok"]),
            "conceitos": len(fila_c),
            "fora": sum(1 for i in itens if i["chave"].startswith("nome:") and not i.get("quarentena")
                        and i["mencoes"] == 1 and i["tipos"] != ["concept"]),
            "triados": len(completos) + len(hk) + len(resp_c),
            "uteis": veredito.get("busca", 0) + veredito.get("stack", 0),
            "conferidos": len(conf),
            "auditados": len(aud),
        },
        "laco": laco,
        "etapas": etapas,
        "conteudo": conteudo(itens, readmes, fl_por_item, hk),
        "execucao": execucao(fl, hk),
    }


# ---------------------------------------------------------------- conteúdo e execução

def mtime_iso(p):
    try:
        return datetime.fromtimestamp(os.path.getmtime(p), timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    except OSError:
        return None


def ts_epoch(r):
    try:
        return datetime.strptime(r["ts"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc).timestamp()
    except (KeyError, ValueError, TypeError):
        return None


def minutos(tempos):
    """60 contagens, índice 0 = minuto atual."""
    agora_ = time.time()
    v = [0] * 60
    for t in tempos:
        if t is None:
            continue
        k = int((agora_ - t) // 60)
        if 0 <= k < 60:
            v[k] += 1
    return v


def conteudo(itens, readmes, fl_por_item, hk):
    """O que o catálogo e a triagem dizem sobre os projetos em si."""
    vivos = [i for i in itens if not i.get("quarentena")]
    por_chave = {i["chave"]: i for i in itens}
    nome = lambda ch: (por_chave.get(ch) or {"nomes": [ch]})["nomes"][0]
    tipos = collections.Counter(t for i in vivos for t in i.get("tipos", []))
    origem = collections.Counter(i["chave"].split(":")[0] for i in vivos)
    familias = collections.Counter(f for i in vivos for f in i.get("familias", []))
    mais_citados = [{"nome": i["nomes"][0], "chave": i["chave"], "mencoes": i["mencoes"],
                     "readme": (readmes.get(i["chave"]) or {}).get("status")} for i in vivos[:15]]
    quarentena = [{"nome": i["nomes"][0], "motivo": i["quarentena"][:80]} for i in itens if i.get("quarentena")][:8]
    arqs = sorted(glob.glob(E("readmes", "*.md")), key=os.path.getmtime, reverse=True)[:10]
    rev = {v.get("arquivo"): k for k, v in readmes.items() if v.get("arquivo")}
    readmes_recentes = [{"nome": nome(rev[os.path.basename(a)]), "chave": rev[os.path.basename(a)],
                         "kb": round(os.path.getsize(a) / 1024, 1), "ts": mtime_iso(a)}
                        for a in arqs if os.path.basename(a) in rev]
    tam = sorted(v.get("bytes", 0) for v in readmes.values() if v.get("status") == "ok")
    # uma resposta por item: a 1ª do FreeLLMAPI, a do Haiku
    respostas = [(rs[-1].get("ts"), ch, "freellm", rs[0].get("modelo"), rs[0].get("resposta") or {})
                 for ch, rs in fl_por_item.items() if rs]
    respostas += [(r.get("ts"), r.get("chave"), "haiku", r.get("modelo"), r.get("resposta") or {}) for r in hk]
    respostas.sort(key=lambda x: x[0] or "", reverse=True)
    col = {k: collections.Counter() for k in ("mechanism", "place", "mcp", "windows", "portuguese", "maturity", "license")}
    for _, _, _, _, o in respostas:
        for k in ("mechanism", "place"):
            col[k].update(x for x in (o.get(k) or []) if isinstance(x, str))
        for k in ("mcp", "windows", "portuguese", "maturity", "license"):
            if isinstance(o.get(k), str):
                col[k][o[k]] += 1
    recentes = [{"nome": nome(ch), "chave": ch, "metade": metade, "modelo": modelo, "serve": o.get("serve"),
                 "duvida": o.get("doubt"), "papel": o.get("role"), "mecanismo": o.get("mechanism"),
                 "mcp": o.get("mcp"), "windows": o.get("windows"), "ts": ts}
                for ts, ch, metade, modelo, o in respostas[:12]]
    candidatos = sorted(({"nome": nome(ch), "chave": ch, "papel": o.get("role"), "mecanismo": o.get("mechanism"),
                          "mcp": o.get("mcp"), "windows": o.get("windows"),
                          "mencoes": (por_chave.get(ch) or {}).get("mencoes", 0)}
                         for _, ch, _, _, o in respostas
                         if o.get("serve") == "search" and o.get("mcp") == "yes" and o.get("windows") != "no"),
                        key=lambda x: -x["mencoes"])
    return {
        "tipos": dict(tipos.most_common()), "origem": dict(origem),
        "familias_que_citaram": dict(familias.most_common(12)),
        "mais_citados": mais_citados, "quarentena_exemplos": quarentena, "readmes_recentes": readmes_recentes,
        "readme_kb": {"mediana": round(tam[len(tam) // 2] / 1024, 1) if tam else None,
                      "maior": round(tam[-1] / 1024, 1) if tam else None},
        "colunas": {k: dict(v.most_common(10)) for k, v in col.items()},
        "triados_recentes": recentes,
        "candidatos_busca_mcp": candidatos[:12],
    }


def processo(nome, log, fim="FIM"):
    p = os.path.join(AQUI, "logs", log)
    try:
        linhas = [l.strip() for l in open(p, encoding="utf-8", errors="replace") if l.strip()]
    except OSError:
        return {"nome": nome, "estado": "nao_iniciado"}
    ult = linhas[-1] if linhas else ""
    parado = time.time() - os.path.getmtime(p) > 900
    estado = "terminou" if ult.startswith(fim) or f" {fim}" in ult else ("parado?" if parado else "ativo")
    return {"nome": nome, "estado": estado, "ultima_linha": ult[:120], "atualizado": mtime_iso(p)}


def execucao(fl, hk):
    """Como a máquina está trabalhando: processos, ritmo, erros, tokens, cota."""
    erros = ler_jsonl(E("triagem", "freellm-erros.jsonl"))
    lat = sorted(r["latencia_s"] for r in fl if r.get("latencia_s") is not None)
    desp = ler_json(os.path.join(AQUI, "estado", "despachante.json"), {})
    levas = ler_jsonl(E("triagem", "haiku-levas.jsonl")) + ler_jsonl(E("conceitos", "levas.jsonl"))
    ok = collections.Counter(r.get("modelo") for r in fl)
    err = collections.Counter(r.get("modelo") for r in erros if r.get("modelo"))
    return {
        "processos": [processo("READMEs", "readmes.out"), processo("URLs", "urls-reconferir.out"),
                      processo("Sites", "sites.out"),
                      processo("Triagem FreeLLMAPI", "triagem-freellm.out", fim="fim;")],
        "readmes_por_minuto": minutos(os.path.getmtime(a) for a in glob.glob(E("readmes", "*.md"))),
        "freellm": {
            "chamadas_por_minuto": minutos(ts_epoch(r) for r in fl + [r for r in erros if r.get("modelo")]),
            "aceitas_por_minuto": minutos(ts_epoch(r) for r in fl),
            "aceitas": len(fl), "recusadas": len(erros),
            "erros": dict(collections.Counter(r.get("estado") for r in erros)),
            "latencia_mediana_s": lat[len(lat) // 2] if lat else None,
            "tokens": sum(((r.get("uso") or {}).get("total_tokens") or 0) for r in fl),
            "modelos": [{"id": m, "aceitas": n, "erros": err.get(m, 0)} for m, n in ok.most_common(10)],
            "familias": dict(collections.Counter(r.get("familia") for r in fl).most_common(10)),
        },
        "haiku": {"levas": len(levas), "subagentes": sum(l.get("subagentes", 0) for l in levas),
                  "tokens": sum(l.get("tokens", 0) for l in levas), "itens": len(hk)},
        "cota": {"aptos": desp.get("aptos"), "fora_agora": desp.get("fora_agora"),
                 "tentativas_total": desp.get("tentativas_total"), "teto": desp.get("teto")},
    }


def gravar():
    d = coletar()
    os.makedirs(os.path.join(AQUI, "painel"), exist_ok=True)
    tmp = os.path.join(AQUI, "painel", "etapas.js.tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        f.write("window.ETAPAS = " + json.dumps(d, ensure_ascii=False) + ";\n")
    os.replace(tmp, os.path.join(AQUI, "painel", "etapas.js"))
    return d


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--servico", action="store_true")
    a = ap.parse_args()
    while True:
        try:
            gravar()
        except Exception as e:  # o serviço não pode morrer por um arquivo a meio caminho
            if not a.servico:
                raise
            print(datetime.now(timezone.utc).isoformat(), "erro:", repr(e)[:300], flush=True)
        if not a.servico:
            break
        time.sleep(60)


if __name__ == "__main__":
    main()
