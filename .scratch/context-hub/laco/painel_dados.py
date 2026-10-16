"""Dados do painel visual: grava `painel/dados.js` (window.DADOS = {...}) para a página do Designer.

Um arquivo .js e não .json porque a página abre por file:// e o navegador não deixa um file:// buscar
JSON; um <script src> funciona. A página recarrega o script de tempos em tempos.
"""
import collections, glob, json, os, time
from datetime import datetime, timezone
from comum import abrir_banco, caminho, ler_controle


def coletar():
    con = abrir_banco()
    onda = ler_controle(con, "onda", 1)
    teto = ler_controle(con, "teto") or {}
    agora = time.time()
    try:
        desp = json.load(open(caminho("estado", "despachante.json"), encoding="utf-8"))
    except OSError:
        desp = {}
    por_minuto = collections.Counter()
    aceitos_minuto = collections.Counter()
    familias, linguas, provedores = collections.Counter(), collections.Counter(), collections.Counter()
    estados = collections.Counter()
    itens_brutos = 0
    for f in glob.glob(caminho("livros", "*.jsonl")):
        for l in open(f, encoding="utf-8"):
            r = json.loads(l)
            try:
                ts = datetime.strptime(r["ts"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc).timestamp()
            except (KeyError, ValueError):
                continue
            estados[r.get("estado")] += 1
            m = int((agora - ts) // 60)
            if m < 120:
                por_minuto[m] += 1
                aceitos_minuto[m] += r.get("estado") == "aceito"
            if r.get("estado") == "aceito":
                familias[r.get("familia")] += 1
                linguas[r.get("lingua")] += 1
                provedores[(r.get("via") or "?").split("/")[0]] += 1
                itens_brutos += len(r.get("itens") or [])
    pedidos = dict(con.execute("""SELECT p.estado, COUNT(*) FROM pedidos p JOIN celulas c ON p.celula=c.id
                                  WHERE c.onda=? GROUP BY 1""", (onda,)).fetchall())
    try:
        catalogo = json.load(open(caminho("catalogo", "itens.json"), encoding="utf-8"))
    except OSError:
        catalogo = []
    try:
        sementes = json.load(open(caminho("sementes.json"), encoding="utf-8"))["sementes"]
    except OSError:
        sementes = []
    nomes_cat = {n.lower() for e in catalogo for n in e.get("nomes", [])}
    achadas = sum(1 for s in sementes if {s["nome"].lower(), *[a.lower() for a in s.get("aliases", [])]} & nomes_cat)
    return {
        "gerado_em": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "terminou": bool(ler_controle(con, "parar", False)),
        "onda": onda,
        "pedidos_da_onda": pedidos,                      # pendente, em_voo, aceito, adiado, esgotado, dividido, cancelado
        "historico": ler_controle(con, "historico", []),  # por onda fechada: itens_total, novos, taxa_novos
        "gate": 0.05,
        "tentativas": con.execute("SELECT COALESCE(SUM(tentativas),0) FROM uso").fetchone()[0],
        "teto_tentativas": teto.get("pedidos"),
        "inicio": teto.get("inicio"), "horas": teto.get("horas"), "agora": agora,
        "modelos": {"aptos": desp.get("aptos"), "fora_agora": desp.get("fora_agora"), "total": desp.get("modelos")},
        "chamadas_por_minuto": [por_minuto.get(i, 0) for i in range(120)],   # índice 0 = minuto atual
        "aceitas_por_minuto": [aceitos_minuto.get(i, 0) for i in range(120)],
        "estados_das_chamadas": dict(estados),
        "aceitas_por_familia": dict(familias.most_common(20)),
        "aceitas_por_lingua": dict(linguas),
        "aceitas_por_provedor": dict(provedores.most_common(20)),
        "itens_brutos": itens_brutos,
        "catalogo_itens": len(catalogo),
        "mais_citados": [{"nome": e["nomes"][0], "mencoes": e["mencoes"], "familias": len(e.get("familias", []))}
                         for e in catalogo[:12]],
        "sementes": {"achadas": achadas, "total": len(sementes)},
    }


def gravar():
    os.makedirs(caminho("painel"), exist_ok=True)
    d = coletar()
    tmp = caminho("painel", "dados.js.tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        f.write("window.DADOS = " + json.dumps(d, ensure_ascii=False) + ";\n")
    os.replace(tmp, caminho("painel", "dados.js"))
    return d


if __name__ == "__main__":
    print(json.dumps(gravar(), ensure_ascii=False, indent=1)[:3000])
