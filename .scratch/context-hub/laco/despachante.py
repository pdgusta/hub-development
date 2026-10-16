"""Despachante: o roteamento do laço. Fixa um modelo por pedido, com orçamento, ritmo e saúde.

Dois usos:
- como serviço (`python despachante.py --servico`): a cada ciclo relê o gateway (catálogo, limites,
  pools), atualiza a tabela `modelos`, devolve à fila pedidos presos em voo e grava o retrato
  `estado/despachante.json`. É o processo que o recruta Despachante toca.
- como biblioteca: os geradores chamam `escolher()` e `liberar()`. As duas rodam numa transação
  `BEGIN IMMEDIATE` no banco comum, então a folga de cota de um modelo nunca é gasta duas vezes.

Outros comandos: `--uma-vez` (um ciclo e sai), `--estado` (mostra a tabela), `--teto PEDIDOS HORAS`.
"""
import argparse, json, math, random, sys, time
from comum import (abrir_banco, agora, anexar, caminho, carregar_config, familia, gravar_controle, http, iso,
                   janela, ler_controle)


# ---------------------------------------------------------------- leitura do gateway

def ler_bancada(cfg):
    """O que a bancada de 2026-10-13 provou por modelo: excluir, aceita response_format, raciocina."""
    info = {}
    try:
        linhas = [json.loads(l) for l in open(caminho(cfg["bancada"]), encoding="utf-8")]
    except OSError:
        return info
    for r in linhas:
        i = info.setdefault(r["model"], {"rf": False, "raciocina": False, "excluir": None})
        erro = r.get("error") or ""
        if r.get("http") == 200 and r.get("schema_ok") and r["kind"] == "json":
            i["rf"] = True
        if r.get("finish_reason") == "length" or (r["kind"] == "json_big" and r.get("schema_ok")):
            i["raciocina"] = True
        if "audio/speech" in erro or "Native Audio" in erro or "unexpected model name format" in erro:
            i["excluir"] = "nao_e_chat"
        if r.get("http") == 404:
            i["excluir"] = "sumiu_no_provedor"
    return info


def atualizar(con, cfg):
    st, _, cat = http(cfg, "GET", "/v1/models")
    st2, _, linhas = http(cfg, "GET", "/api/fallback", painel=True)
    st3, _, ft = http(cfg, "GET", "/api/free-tier", painel=True)
    if st != 200 or st2 != 200:
        print(iso(), "gateway não respondeu:", st, st2, file=sys.stderr)
        return False
    pool_de = {}
    for p in (ft.get("pools", []) if st3 == 200 else []):
        for m in p.get("memberModelIds", []):
            pool_de[(p["platform"], m)] = p["poolKey"]
    por_id = {}
    for r in sorted(linhas, key=lambda r: r["effectivePriority"]):
        for k in {r["canonicalId"], r["modelId"]}:
            por_id.setdefault(k, []).append(r)
    bancada = ler_bancada(cfg)
    vistos = set()
    for m in cat.get("data", []):
        mid, status = m["id"], m.get("execution_status")
        if status is None:  # auto, fusion, perfis: entradas do roteador, não modelos
            continue
        rows = [r for r in por_id.get(mid, []) if (r.get("keyCount") or 0) > 0] or por_id.get(mid, [])
        if not rows:
            continue
        vistos.add(mid)
        r0 = rows[0]
        chaves = sum(r.get("keyCount") or 0 for r in rows)
        rpms = [r["rpmLimit"] for r in rows if r.get("rpmLimit")]
        # limite diário só existe se TODAS as rotas do grupo têm um; uma rota sem limite libera o grupo
        rpd = sum((r["rpdLimit"] or 0) * max(r.get("keyCount") or 0, 1) for r in rows) \
            if all(r.get("rpdLimit") for r in rows) else None
        b = bancada.get(mid, {})
        excl = b.get("excluir") or (None if status == "ready" else "status_" + status)
        if mid in cfg.get("excluir_manual", []):
            excl = "manual"
        con.execute("""INSERT INTO modelos (id, plataforma, pool, familia, rpm, rpd, chaves, aceita_rf, raciocina,
                         status, excluido, atualizado) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
                       ON CONFLICT(id) DO UPDATE SET plataforma=excluded.plataforma, pool=excluded.pool,
                         familia=excluded.familia, rpm=excluded.rpm, rpd=excluded.rpd, chaves=excluded.chaves,
                         aceita_rf=MAX(modelos.aceita_rf, excluded.aceita_rf),
                         raciocina=MAX(modelos.raciocina, excluded.raciocina), status=excluded.status,
                         excluido=CASE WHEN modelos.excluido IN ('sumiu_no_provedor','nao_e_chat') THEN modelos.excluido
                                       ELSE excluded.excluido END,
                         atualizado=excluded.atualizado""",
                    (mid, r0["platform"], pool_de.get((r0["platform"], r0["modelId"]), r0["platform"]),
                     familia(mid), min(rpms) if rpms else None, rpd, chaves, int(b.get("rf", False)),
                     int(b.get("raciocina", False)), status, excl, iso()))
    if vistos:
        marcas = ",".join("?" * len(vistos))
        con.execute(f"UPDATE modelos SET status='fora_do_catalogo' WHERE id NOT IN ({marcas})", tuple(vistos))
    # pedidos presos em voo (gerador caiu) voltam para a fila
    limite = agora() - 2 * cfg["timeout_s"]
    con.execute("UPDATE pedidos SET estado='pendente', modelo=NULL WHERE estado='em_voo' AND em_voo_desde < ?", (limite,))
    con.execute("""UPDATE modelos SET em_voo = (SELECT COUNT(*) FROM pedidos p WHERE p.estado='em_voo' AND p.modelo=modelos.id)""")
    con.execute("DELETE FROM ritmo WHERE ts < ?", (agora() - 120,))
    retrato(con, cfg)
    return True


def retrato(con, cfg):
    linhas = con.execute("SELECT * FROM modelos ORDER BY plataforma, id").fetchall()
    usos = {(r["modelo"], r["janela"]): r["tentativas"] for r in con.execute("SELECT * FROM uso")}
    aptos = [r for r in linhas if r["excluido"] is None and r["status"] == "ready"]
    resumo = {
        "gerado_em": iso(),
        "modelos": len(linhas), "aptos": len(aptos),
        "fora_agora": sum(1 for r in aptos if r["fora_ate"] > agora()),
        "familias_aptas": sorted({r["familia"] for r in aptos}),
        "pools_aptos": sorted({r["pool"] for r in aptos}),
        "tentativas_total": con.execute("SELECT COALESCE(SUM(tentativas),0) t FROM uso").fetchone()["t"],
        "teto": ler_controle(con, "teto"),
        "por_modelo": [{"id": r["id"], "pool": r["pool"], "familia": r["familia"], "excluido": r["excluido"],
                        "acertos": r["acertos"], "erros": r["erros"], "em_voo": r["em_voo"],
                        "fora_ate": iso(r["fora_ate"]) if r["fora_ate"] > agora() else None,
                        "uso_hoje": usos.get((r["id"], janela(cfg, r["plataforma"])), 0),
                        "orcamento_dia": orcamento(cfg, r)} for r in linhas],
    }
    with open(caminho("estado", "despachante.json"), "w", encoding="utf-8") as f:
        json.dump(resumo, f, ensure_ascii=False, indent=1)
    return resumo


# ---------------------------------------------------------------- escolha e devolução

def orcamento(cfg, m):
    """Tentativas permitidas na janela de hoje; None = sem limite diário publicado."""
    return None if m["rpd"] is None else int(math.floor(m["rpd"] * cfg["fracao_da_cota"]))


def teto_atingido(con):
    t = ler_controle(con, "teto")
    if not t:
        return False
    total = con.execute("SELECT COALESCE(SUM(tentativas),0) t FROM uso").fetchone()["t"]
    if t.get("pedidos") and total >= t["pedidos"]:
        return True
    if t.get("horas") and agora() - t["inicio"] >= t["horas"] * 3600:
        return True
    return False


def escolher(con, cfg, excluir=(), familia_proibida=None, pool_proibido=None):
    """Escolhe e reserva um modelo. Devolve dict do modelo, 'teto', ou None (ninguém disponível agora)."""
    con.execute("BEGIN IMMEDIATE")
    try:
        if teto_atingido(con):
            con.execute("COMMIT")
            return "teto"
        t = agora()
        cands = []
        em_voo_pool = {r["pool"]: r["n"] for r in
                       con.execute("SELECT pool, SUM(em_voo) n FROM modelos GROUP BY pool")}
        for m in con.execute("SELECT * FROM modelos WHERE excluido IS NULL AND status='ready' AND fora_ate <= ?", (t,)):
            if m["id"] in excluir or m["familia"] == familia_proibida or m["pool"] == pool_proibido:
                continue
            if m["em_voo"] >= cfg["max_em_voo_modelo"]:
                continue
            if em_voo_pool.get(m["pool"], 0) >= cfg["max_em_voo_pool"].get(m["plataforma"], cfg["max_em_voo_pool"]["padrao"]):
                continue
            jan = janela(cfg, m["plataforma"], t)
            usado = (con.execute("SELECT tentativas FROM uso WHERE modelo=? AND janela=?", (m["id"], jan)).fetchone() or [0])[0]
            orc = orcamento(cfg, m)
            # reserva o pior caso: uma chamada fixada pode gastar várias tentativas de chave
            if orc is not None and usado + cfg["tentativas_por_chamada_reserva"] > orc:
                continue
            if m["rpm"]:
                n = con.execute("SELECT COUNT(*) FROM ritmo WHERE chave=? AND ts > ?", ("m:" + m["id"], t - 60)).fetchone()[0]
                if n >= m["rpm"] * max(m["chaves"] or 1, 1):
                    continue
            rpm_pool = cfg["rpm_por_pool"].get(m["plataforma"])
            if rpm_pool:
                n = con.execute("SELECT COUNT(*) FROM ritmo WHERE chave=? AND ts > ?", ("p:" + m["plataforma"], t - 60)).fetchone()[0]
                if n >= rpm_pool:
                    continue
            folga = (orc - usado) if orc is not None else cfg["folga_sem_limite"]
            taxa = (m["acertos"] + 1) / (m["acertos"] + m["erros"] + 2)
            cands.append((m, min(folga, cfg["folga_sem_limite"]) * taxa))
        if not cands:
            con.execute("COMMIT")
            return None
        m = random.choices([c[0] for c in cands], weights=[max(c[1], 0.01) for c in cands])[0]
        con.execute("UPDATE modelos SET em_voo = em_voo + 1 WHERE id=?", (m["id"],))
        con.execute("INSERT INTO ritmo VALUES (?,?)", ("m:" + m["id"], t))
        con.execute("INSERT INTO ritmo VALUES (?,?)", ("p:" + m["plataforma"], t))
        con.execute("""INSERT INTO uso VALUES (?,?,1) ON CONFLICT(modelo, janela) DO UPDATE SET tentativas = tentativas + 1""",
                    (m["id"], janela(cfg, m["plataforma"], t)))
        con.execute("COMMIT")
        return dict(m)
    except Exception:
        con.execute("ROLLBACK")
        raise


def liberar(con, cfg, modelo, plataforma, resultado, tentativas_extra=0):
    """resultado: ok | neutro (não conta contra o modelo) | invalido | cota | provedor | sumiu | nao_e_chat."""
    t = agora()
    con.execute("BEGIN IMMEDIATE")
    try:
        con.execute("UPDATE modelos SET em_voo = MAX(em_voo - 1, 0) WHERE id=?", (modelo,))
        if tentativas_extra:
            con.execute("""INSERT INTO uso VALUES (?,?,?) ON CONFLICT(modelo, janela) DO UPDATE SET tentativas = tentativas + ?""",
                        (modelo, janela(cfg, plataforma, t), tentativas_extra, tentativas_extra))
        if resultado == "ok":
            con.execute("UPDATE modelos SET acertos = acertos + 1, falhas_seguidas = 0 WHERE id=?", (modelo,))
        elif resultado == "invalido":
            con.execute("UPDATE modelos SET erros = erros + 1 WHERE id=?", (modelo,))
        elif resultado in ("cota", "provedor"):
            m = con.execute("SELECT falhas_seguidas FROM modelos WHERE id=?", (modelo,)).fetchone()
            seguidas = (m["falhas_seguidas"] if m else 0) + 1
            if resultado == "cota" and seguidas >= cfg["cotas_seguidas_ate_virada"]:
                espera = proxima_virada(cfg, plataforma, t) - t      # cota do dia acabou
            elif resultado == "cota":
                espera = cfg["espera_cota_s"]
            elif seguidas >= cfg["falhas_ate_pausa"]:
                espera = cfg["pausa_falhas_s"]
            else:
                espera = 0
            con.execute("UPDATE modelos SET erros = erros + 1, falhas_seguidas = ?, fora_ate = ? WHERE id=?",
                        (seguidas, t + espera, modelo))
        elif resultado in ("sumiu", "nao_e_chat"):
            con.execute("UPDATE modelos SET excluido = ? WHERE id=?",
                        ("sumiu_no_provedor" if resultado == "sumiu" else "nao_e_chat", modelo))
        con.execute("COMMIT")
    except Exception:
        con.execute("ROLLBACK")
        raise


def proxima_virada(cfg, plataforma, t):
    from datetime import datetime, timedelta, timezone
    ini = datetime.strptime(janela(cfg, plataforma, t), "%Y-%m-%dT%H").replace(tzinfo=timezone.utc)
    return (ini + timedelta(days=1)).timestamp() + 60


# ---------------------------------------------------------------- linha de comando

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--servico", action="store_true")
    ap.add_argument("--uma-vez", action="store_true")
    ap.add_argument("--estado", action="store_true")
    ap.add_argument("--teto", nargs=2, metavar=("PEDIDOS", "HORAS"), help="0 = sem esse limite")
    a = ap.parse_args()
    cfg, con = carregar_config(), abrir_banco()
    if a.teto:
        p, h = int(a.teto[0]), float(a.teto[1])
        gravar_controle(con, "teto", {"pedidos": p or None, "horas": h or None, "inicio": agora()})
        print("teto gravado:", ler_controle(con, "teto"))
    if a.uma_vez or a.servico:
        while True:
            ok = atualizar(con, cfg)
            r = json.load(open(caminho("estado", "despachante.json"), encoding="utf-8")) if ok else {}
            print(iso(), "aptos", r.get("aptos"), "fora", r.get("fora_agora"), "tentativas", r.get("tentativas_total"), flush=True)
            anexar(caminho("estado", "despachante.log.jsonl"), {k: r.get(k) for k in ("gerado_em", "aptos", "fora_agora", "tentativas_total")})
            if a.uma_vez:
                break
            time.sleep(cfg["ciclo_despachante_s"])
    if a.estado:
        for m in con.execute("SELECT * FROM modelos ORDER BY excluido IS NOT NULL, plataforma, id"):
            print(m["id"], m["plataforma"], m["familia"], "rpm", m["rpm"], "rpd", m["rpd"], "acertos", m["acertos"],
                  "erros", m["erros"], "excluido", m["excluido"])


if __name__ == "__main__":
    main()
