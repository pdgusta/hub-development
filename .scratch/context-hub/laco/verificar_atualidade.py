"""Teste de atualidade: os modelos buscam na web ou respondem de memória?

A mesma pergunta, cuja resposta certa só existe depois do treino da maioria dos modelos, vai aos N modelos que
mais tiveram respostas aceitas no laço, em duas versões: sem pedir busca e com "Search the web first" no
começo. Gabarito em --gabarito (conferido pelo maestro na fonte primária antes de rodar).
Saída: verificacao/atualidade.jsonl e verificacao/atualidade.md. As tentativas entram no uso do despachante.
Uso: python verificar_atualidade.py --modelos 30
"""
import argparse, collections, concurrent.futures as cf, glob, json, re, time
from comum import abrir_banco, anexar, caminho, carregar_config, cabecalho, extrair_json, http, iso, janela

PERGUNTA = ('What is the most recent stable desktop release of Obsidian (the note-taking app)? Reply ONLY with JSON: '
            '{"version":"x.y.z","release_date":"YYYY-MM-DD","today":"YYYY-MM-DD","did_you_search_the_web":true|false,'
            '"source_url":"https://..."}')
PREFIXO = "Search the web first, then answer. "


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--modelos", type=int, default=30)
    ap.add_argument("--gabarito", default="1.14")
    a = ap.parse_args()
    cfg, con = carregar_config(), abrir_banco()
    aceitos = collections.Counter()
    for f in glob.glob(caminho("livros", "*.jsonl")):
        for l in open(f, encoding="utf-8"):
            r = json.loads(l)
            if r.get("estado") == "aceito":
                aceitos[r["modelo"]] += 1
    alvos = []
    for mid, _ in aceitos.most_common():
        m = con.execute("SELECT * FROM modelos WHERE id=?", (mid,)).fetchone()
        if m and m["excluido"] is None:
            alvos.append(dict(m))
        if len(alvos) >= a.modelos:
            break
    saida = caminho("verificacao", "atualidade.jsonl")

    def chamar(m, com_busca):
        corpo = {"model": m["id"], "messages": [{"role": "user", "content": (PREFIXO if com_busca else "") + PERGUNTA}],
                 "max_tokens": 4000 if m["raciocina"] else 1000, "temperature": 0}
        t0 = time.time()
        st, h, d = http(cfg, "POST", "/v1/chat/completions", corpo, timeout=cfg["timeout_s"])
        extra = int(cabecalho(h, "X-Fallback-Attempts") or 0)
        con2 = abrir_banco()
        con2.execute("INSERT INTO uso VALUES (?,?,?) ON CONFLICT(modelo, janela) DO UPDATE SET tentativas = tentativas + ?",
                     (m["id"], janela(cfg, m["plataforma"]), 1 + extra, 1 + extra))
        texto = (((d.get("choices") or [{}])[0].get("message") or {}).get("content") or "") if st == 200 else ""
        o = extrair_json(texto) or {}
        versao = str(o.get("version") or "")
        rec = {"ts": iso(), "modelo": m["id"], "familia": m["familia"], "via": cabecalho(h, "X-Routed-Via"), "pediu_busca": com_busca,
               "http": st, "latencia_s": round(time.time() - t0, 1), "versao": versao, "data": o.get("release_date"),
               "hoje": o.get("today"), "diz_que_buscou": o.get("did_you_search_the_web"), "fonte": o.get("source_url"),
               "acertou": versao.startswith(a.gabarito), "texto": texto[:800],
               "erro": None if st == 200 else str((d.get("error") or {}).get("message", ""))[:300]}
        anexar(saida, rec)
        return rec

    jobs = [(m, b) for m in alvos for b in (False, True)]
    with cf.ThreadPoolExecutor(10) as ex:
        res = list(ex.map(lambda j: chamar(*j), jobs))
    ok = [r for r in res if r["http"] == 200]
    linhas = [f"# Teste de atualidade ({time.strftime('%Y-%m-%d %H:%M')})", "",
              f"Pergunta: a versão estável mais recente do Obsidian desktop. Gabarito: {a.gabarito} (conferido pelo maestro na fonte primária).",
              f"{len(alvos)} modelos, 2 versões cada; {len(ok)} de {len(res)} chamadas responderam.", "",
              "| Modelo | Provedor | Sem pedir busca | Pedindo busca | Diz que buscou (com pedido) |", "|---|---|---|---|---|"]
    por = collections.defaultdict(dict)
    for r in res:
        por[r["modelo"]][r["pediu_busca"]] = r
    for mid, d in por.items():
        cel = lambda r: "erro" if not r or r["http"] != 200 else f'{r["versao"] or "?"} ({r["data"] or "?"})' + (" ✔" if r["acertou"] else "")
        via = (d.get(False) or d.get(True) or {}).get("via") or "?"
        linhas.append(f"| {mid} | {via.split('/')[0]} | {cel(d.get(False))} | {cel(d.get(True))} | {(d.get(True) or {}).get('diz_que_buscou')} |")
    acertos = collections.Counter((r["pediu_busca"], r["acertou"]) for r in ok)
    linhas += ["", f"Acertos sem pedir busca: {acertos[(False, True)]}; pedindo busca: {acertos[(True, True)]}."]
    open(caminho("verificacao", "atualidade.md"), "w", encoding="utf-8").write("\n".join(linhas) + "\n")
    print("\n".join(linhas[-3:]))


if __name__ == "__main__":
    main()
