"""Juntador: fecha cada onda, junta os itens, cria as células da bola de neve e mede o gate dos 5%.

Uso: python juntador.py --servico   (fica de olho e fecha cada onda quando ela termina)
     python juntador.py --agora     (fecha a onda atual já, mesmo com pedidos adiados)
     python juntador.py --rejuntar  (só refaz itens.json e ambiguos.json com as decisões; não fecha onda nem
                                     olha o `parar`; guarda a versão anterior em catalogo/itens-antes-de-rejuntar.json)
Saídas: catalogo/itens.json (o catálogo inteiro, reescrito a cada onda), catalogo/ambiguos.json (para o
recruta Juntador decidir), ondas/onda-N.md (o relatório da onda) e o controle `parar` no fim.
Decisões do recruta: catalogo/decisoes.jsonl, uma por linha:
  {"juntar": ["chave1", "chave2"]}  {"separar": "nome normalizado"}  {"quarentena": "chave", "motivo": "..."}
"""
import argparse, collections, glob, json, os, re, time, unicodedata
from comum import abrir_banco, agora, caminho, carregar_config, gravar_controle, iso, ler_controle
from plano import criar_celula, ler_plano, montar_prompt

RE_GH = re.compile(r"github\.com/([A-Za-z0-9_.-]+)/([A-Za-z0-9_.-]+)", re.I)


def norm_nome(s):
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode().lower()
    s = re.sub(r"\(.*?\)", "", s)
    s = re.sub(r"[^a-z0-9]+", "", s)
    return s


def chave_url(url):
    m = RE_GH.search(url or "")
    if m:
        repo = re.sub(r"\.git$", "", m.group(2).lower())
        return f"gh:{m.group(1).lower()}/{repo}"
    u = (url or "").strip().lower()
    u = re.sub(r"^https?://(www\.)?", "", u).split("#")[0].split("?")[0].rstrip("/")
    return f"web:{u}" if "." in u else None


def ler_decisoes():
    d = {"juntar": [], "separar": set(), "quarentena": {}}
    try:
        for l in open(caminho("catalogo", "decisoes.jsonl"), encoding="utf-8"):
            r = json.loads(l)
            if "juntar" in r:
                d["juntar"].append(r["juntar"])
            if "separar" in r:
                d["separar"].add(r["separar"])
            if "quarentena" in r:
                d["quarentena"][r["quarentena"]] = r.get("motivo", "")
    except OSError:
        pass
    return d


def juntar_tudo():
    """Relê todos os livros-razão e monta o catálogo do zero (determinístico e retomável)."""
    dec = ler_decisoes()
    itens, alias, ambiguos = {}, {}, collections.defaultdict(set)
    regs = []
    for f in sorted(glob.glob(caminho("livros", "*.jsonl"))):
        for l in open(f, encoding="utf-8"):
            r = json.loads(l)
            if r.get("estado") == "aceito":
                regs.append(r)
    regs.sort(key=lambda r: r["ts"])
    for r in regs:
        for it in r["itens"]:
            n = norm_nome(it["name"])
            ku = chave_url(it.get("url"))
            pode = bool(n) and n not in dec["separar"]
            if ku and ku.startswith("gh:"):
                chave = ku
                ant = alias.get(n) if pode else None
                if ant and ant.startswith("gh:") and ant != ku:
                    ambiguos[n].update({ant, ku})
                elif pode:
                    alias[n] = ku          # um repositório vence o apelido só por nome
            else:
                chave = (alias.get(n) if pode else None) or ku or f"nome:{n}"
                if pode and n not in alias:
                    alias[n] = chave
            e = itens.setdefault(chave, {"chave": chave, "nomes": [], "urls": [], "tipos": [], "resumos": [], "termos": [],
                                          "fontes": [], "primeira_onda": r["onda"]})
            for campo, valor in (("nomes", it["name"]), ("urls", it.get("url") or ""), ("tipos", it["kind"])):
                if valor and valor not in e[campo]:
                    e[campo].append(valor)
            if it.get("summary") and len(e["resumos"]) < 6:
                e["resumos"].append({"lingua": r["lingua"], "modelo": r["modelo"], "texto": it["summary"]})
            for t in it.get("terms") or []:
                if isinstance(t, str) and t.strip() and t not in e["termos"]:
                    e["termos"].append(t.strip())
            e["fontes"].append({"pedido": r["pedido"], "modelo": r["modelo"], "familia": r["familia"],
                                "lingua": r["lingua"], "onda": r["onda"]})
            e["primeira_onda"] = min(e["primeira_onda"], r["onda"])
    # nomes sem URL que depois ganharam um repositório viram parte dele
    for chave in [k for k in itens if not k.startswith("gh:")]:
        if chave not in itens:
            continue
        for nome in itens[chave]["nomes"]:
            destino = alias.get(norm_nome(nome))
            if destino and destino.startswith("gh:") and destino in itens:
                fundir(itens, destino, chave)
                break
    for grupo in dec["juntar"]:
        presentes = [k for k in grupo if k in itens]
        for k in presentes[1:]:
            fundir(itens, presentes[0], k)
    for k, motivo in dec["quarentena"].items():
        if k in itens:
            itens[k]["quarentena"] = motivo
    for e in itens.values():
        e["mencoes"] = len(e["fontes"])
        e["familias"] = sorted({f["familia"] for f in e["fontes"]})
    return itens, {n: sorted(ks) for n, ks in ambiguos.items()}


def fundir(itens, destino, origem):
    a, b = itens[destino], itens.pop(origem)
    for campo in ("nomes", "urls", "tipos", "termos"):
        a[campo] += [v for v in b[campo] if v not in a[campo]]
    a["resumos"] = (a["resumos"] + b["resumos"])[:6]
    a["fontes"] += b["fontes"]
    a["primeira_onda"] = min(a["primeira_onda"], b["primeira_onda"])


def onda_terminou(con, onda, forcar):
    pend = con.execute("""SELECT p.estado, p.proximo_em FROM pedidos p JOIN celulas c ON p.celula=c.id
                          WHERE c.onda=? AND p.estado IN ('pendente','em_voo','adiado')""", (onda,)).fetchall()
    if not pend:
        return True
    if forcar:
        return True
    # só sobraram pedidos adiados: a onda fecha (e eles passam para a próxima) se estão longe ou se são poucos
    if not all(p["estado"] == "adiado" for p in pend):
        return False
    total = con.execute("SELECT COUNT(*) FROM pedidos p JOIN celulas c ON p.celula=c.id WHERE c.onda=?", (onda,)).fetchone()[0]
    poucos = len(pend) <= max(1, total * (1 - cfg_fracao_para_fechar()))
    return poucos or all(p["proximo_em"] > agora() + 600 for p in pend)


def cfg_fracao_para_fechar():
    return carregar_config().get("fracao_para_fechar", 0.97)


def fechar_onda(con, cfg, onda):
    plano = ler_plano()
    itens, ambiguos = juntar_tudo()
    hist = ler_controle(con, "historico", [])
    antes = ler_controle(con, "chaves_conhecidas", [])
    conhecidas = set(antes)
    novas = [k for k in itens if k not in conhecidas and not itens[k].get("quarentena")]
    total = sum(1 for e in itens.values() if not e.get("quarentena"))
    taxa = len(novas) / total if total else 1.0
    hist.append({"onda": onda, "fechada_em": iso(), "itens_total": total, "novos": len(novas), "taxa_novos": round(taxa, 4)})
    gravar_controle(con, "historico", hist)
    gravar_controle(con, "chaves_conhecidas", sorted(conhecidas | set(itens)))
    os.makedirs(caminho("catalogo"), exist_ok=True)
    json.dump(sorted(itens.values(), key=lambda e: -e["mencoes"]), open(caminho("catalogo", "itens.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    json.dump(ambiguos, open(caminho("catalogo", "ambiguos.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    sementes = json.load(open(caminho("sementes.json"), encoding="utf-8"))["sementes"]
    achadas = {s["nome"]: semente_achada(s, itens) for s in sementes}
    saturou = len(hist) >= 2 and all(h["taxa_novos"] < cfg["gate_novos"] for h in hist[-2:])
    calibrou = ler_controle(con, "calibracao_feita", False)
    proxima, criadas, fim = onda + 1, 0, False
    con.execute("BEGIN IMMEDIATE")
    # pedidos adiados que sobraram vão para a próxima onda
    con.execute("""UPDATE celulas SET onda=? WHERE onda=? AND id IN
                   (SELECT celula FROM pedidos WHERE estado IN ('pendente','adiado','em_voo'))""", (proxima, onda))
    if saturou and not calibrou:
        for s in sementes:
            if achadas[s["nome"]]:
                continue
            for lingua in cfg["linguas_calibracao"]:
                for k, frase in enumerate(s["vizinhanca"].get(lingua, [])):
                    criadas += criar_celula(con, cfg, f"o{proxima}.cal.{norm_nome(s['nome'])}.{lingua}.{k}", proxima, lingua,
                                            "calibracao", "calibracao", montar_prompt(plano, lingua, frase))
        gravar_controle(con, "calibracao_feita", True)
        if not criadas:
            fim = True
    elif saturou and calibrou:
        fim = True
    else:
        criadas = bola_de_neve(con, cfg, plano, itens, novas, proxima)
        if not criadas and not con.execute("SELECT 1 FROM celulas WHERE onda=?", (proxima,)).fetchone():
            fim = True
    if fim:
        gravar_controle(con, "parar", True)
    else:
        gravar_controle(con, "onda", proxima)
    con.execute("COMMIT")
    relatorio(con, cfg, onda, hist, novas, itens, achadas, criadas, ambiguos, fim)
    return fim


def semente_achada(s, itens):
    nomes = {norm_nome(n) for n in [s["nome"]] + s.get("aliases", [])}
    urls = {chave_url(u) for u in s.get("urls", [])} - {None}
    for k, e in itens.items():
        if k in urls or nomes & {norm_nome(n) for n in e["nomes"]}:
            return True
    return False


def bola_de_neve(con, cfg, plano, itens, novas, onda):
    """Nomes novos viram 'alternativas a X' e 'o que se monta com X'; termos repetidos viram busca por termo."""
    bn, criadas, limite = plano["bola_de_neve"], 0, cfg["max_celulas_novas_por_onda"]
    candidatos = sorted(novas, key=lambda k: -itens[k]["mencoes"])
    for k in candidatos:
        e = itens[k]
        nome = e["nomes"][0]
        linguas = list(dict.fromkeys([e["fontes"][0]["lingua"], "en"]))
        for modelo in ("alternativas", "montar_com"):
            for lingua in linguas:
                if criadas >= limite:
                    return criadas
                criadas += criar_celula(con, cfg, f"o{onda}.{modelo}.{norm_nome(nome)[:40]}.{lingua}", onda, lingua, modelo,
                                        "bola-de-neve", montar_prompt(plano, lingua, bn[modelo][lingua].replace("{x}", nome)))
    contagem = collections.Counter()
    lingua_do_termo = {}
    ja_nomes = {norm_nome(n) for e in itens.values() for n in e["nomes"]}
    for e in itens.values():
        for t in e["termos"]:
            n = norm_nome(t)
            if n and n not in ja_nomes:
                contagem[t] += 1
                lingua_do_termo.setdefault(t, e["fontes"][0]["lingua"])
    feitos = set(ler_controle(con, "termos_buscados", []))
    for t, n in contagem.most_common():
        if n < cfg["mencoes_minimas_termo"] or norm_nome(t) in feitos:
            continue
        for lingua in dict.fromkeys([lingua_do_termo[t], "en"]):
            if criadas >= limite:
                break
            criadas += criar_celula(con, cfg, f"o{onda}.termo.{norm_nome(t)[:40]}.{lingua}", onda, lingua, "termo",
                                    "bola-de-neve", montar_prompt(plano, lingua, bn["termo"][lingua].replace("{x}", t)))
        feitos.add(norm_nome(t))
    gravar_controle(con, "termos_buscados", sorted(feitos))
    return criadas


def relatorio(con, cfg, onda, hist, novas, itens, achadas, criadas, ambiguos, fim):
    estados = con.execute("""SELECT p.estado, COUNT(*) n FROM pedidos p JOIN celulas c ON p.celula=c.id
                             WHERE c.onda=? GROUP BY 1""", (onda,)).fetchall()
    lacunas = [r["id"] for r in con.execute("SELECT id FROM celulas WHERE onda=? AND estado='esgotada'", (onda,))]
    try:
        d = json.load(open(caminho("estado", "despachante.json"), encoding="utf-8"))
    except OSError:
        d = {}
    linhas = [f"# Onda {onda}", "", f"Fechada em {iso()}.", "",
              "## Pedidos por estado", ""] + [f"- {r['estado']}: {r['n']}" for r in estados] + [
              "", "## Curva de saturação", "", "| Onda | Itens | Novos | Taxa |", "|---|---|---|---|"] + [
              f"| {h['onda']} | {h['itens_total']} | {h['novos']} | {h['taxa_novos']:.1%} |" for h in hist] + [
              "", f"Gate: duas ondas seguidas abaixo de {cfg['gate_novos']:.0%}.", "",
              "## Sementes ocultas", "", f"{sum(achadas.values())} de {len(achadas)} achadas.", "",
              "## Provedor", "", f"Modelos aptos: {d.get('aptos')}; fora agora: {d.get('fora_agora')}; "
              f"tentativas no total: {d.get('tentativas_total')}.", "",
              f"## Próximo passo", "", "**Fim do laço.**" if fim else f"{criadas} células novas na onda {onda + 1}.", "",
              f"Lacunas de cobertura (células esgotadas): {len(lacunas)}.", f"Casos ambíguos para o recruta Juntador: {len(ambiguos)}.",
              "", "## Itens novos mais citados", ""] + [
              f"- {itens[k]['nomes'][0]} ({itens[k]['mencoes']} menções, {len(itens[k]['familias'])} famílias)"
              for k in sorted(novas, key=lambda k: -itens[k]["mencoes"])[:30]]
    os.makedirs(caminho("ondas"), exist_ok=True)
    with open(caminho("ondas", f"onda-{onda}.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(linhas) + "\n")
    print(iso(), f"onda {onda} fechada: {len(novas)} novos de {hist[-1]['itens_total']} ({hist[-1]['taxa_novos']:.1%})",
          "FIM" if fim else f"{criadas} células novas", flush=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--servico", action="store_true")
    ap.add_argument("--agora", action="store_true")
    ap.add_argument("--ate-fechar", action="store_true", help="espera a onda atual fechar, fecha e sai")
    ap.add_argument("--rejuntar", action="store_true")
    a = ap.parse_args()
    if a.rejuntar:
        import shutil
        shutil.copyfile(caminho("catalogo", "itens.json"), caminho("catalogo", "itens-antes-de-rejuntar.json"))
        itens, ambiguos = juntar_tudo()
        json.dump(sorted(itens.values(), key=lambda e: -e["mencoes"]),
                  open(caminho("catalogo", "itens.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        json.dump(ambiguos, open(caminho("catalogo", "ambiguos.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        q = sum(1 for e in itens.values() if e.get("quarentena"))
        print(len(itens), "itens;", q, "em quarentena;", len(ambiguos), "nomes ambíguos (antes das junções)")
        return
    cfg, con = carregar_config(), abrir_banco()
    while True:
        if ler_controle(con, "parar", False):
            print("laço parado"); break
        onda = ler_controle(con, "onda", 1)
        if onda_terminou(con, onda, a.agora):
            if fechar_onda(con, cfg, onda) or a.agora or a.ate_fechar:
                break
        elif not (a.servico or a.ate_fechar):
            print("onda", onda, "ainda em andamento"); break
        time.sleep(cfg["ciclo_juntador_s"])


if __name__ == "__main__":
    main()
