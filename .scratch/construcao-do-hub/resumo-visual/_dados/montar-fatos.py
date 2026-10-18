# Junta tickets-01-22.json e tickets-23-44.json com os fatos de fora dos tickets
# e grava ../fatos-peca-1.json. Depois injeta os fatos no modelo e grava ../peca-1-partitura.html.
# Regra do relógio: o git é o relógio certo. As horas dos comentários da noite de 16/10 estão
# adiantadas 2 a 3 h, e as do diário entre ~03h e ~04h45 de 17/10, ~1 h (diario-da-construcao.md:27).
import json, re, pathlib, sys

AQUI = pathlib.Path(__file__).parent
SAIDA = AQUI.parent

def ld(nome):
    return json.load(open(AQUI / nome, encoding="utf-8"))

tickets = ld("tickets-01-22.json") + ld("tickets-23-44.json")
tickets.sort(key=lambda t: int(t["id"]))

# primeiro commit de cada ticket: git -C C:/context-hub log --all (assunto "ticket NN"/"NN:"/"prova NN");
# 10 está no fork C:/Projetos/hub-mcp-banco; 20 não cita o número (o primeiro é o da guarda do acervo).
PRIMEIRO = {
 "01":("43a4ea9","2026-10-16T19:42"),"02":("6191e40","2026-10-16T19:48"),"03":("c1b3ead","2026-10-16T18:59"),
 "04":("7c6cc47","2026-10-16T18:57"),"05":("8b1e1a4","2026-10-16T19:16"),"06":("e07a481","2026-10-16T20:04"),
 "07":("4967c69","2026-10-16T20:52"),"08":("5110f3f","2026-10-17T03:10"),"09":("ce9790b","2026-10-17T03:51"),
 "10":("c182dcc (fork hub-mcp-banco)","2026-10-17T05:15"),"11":("bdd69e2","2026-10-17T06:46"),
 "12":("a685c4e","2026-10-16T21:35"),"13":("32e77b2","2026-10-17T00:57"),"14":("63153dd","2026-10-16T20:19"),
 "15":("1ffde0a","2026-10-16T23:19"),"16":("060da24","2026-10-17T04:30"),"17":("2947951","2026-10-17T05:14"),
 "18":("ca2bb45","2026-10-17T07:34"),"19":("d8e971a","2026-10-16T22:09"),"20":("2cc4eea","2026-10-16T23:00"),
 "21":("5061cc3","2026-10-17T07:39"),"22":("73c0693","2026-10-17T07:05"),"23":("6481f3a","2026-10-17T08:06"),
 "24":("555025a","2026-10-17T08:45"),"25":("92ee004","2026-10-17T08:55"),
 "27":("5d50370","2026-10-16T20:38"),"28":("e74327c","2026-10-17T03:05"),"29":("654c329","2026-10-16T21:43"),
 "30":("c52ccc1","2026-10-17T00:06"),"31":("9cb5ac6","2026-10-17T01:04"),"32":("94c42ac","2026-10-17T01:18"),
 "33":("4323d0c","2026-10-17T04:06"),"34":("cd52173","2026-10-17T02:29"),"35":("140417a","2026-10-17T02:25"),
 "36":("90f6463","2026-10-17T05:40"),"37":("977ea86","2026-10-17T09:31"),"38":("09b11d8","2026-10-17T11:22"),
 "39":("4309277","2026-10-17T12:19"),"40":("db6b52c","2026-10-17T12:41"),"41":("ae102ed","2026-10-17T12:50"),
 "42":("363e733","2026-10-17T12:58"),"43":("32e8217","2026-10-17T14:36"),"44":("70b1843","2026-10-17T15:40"),
}
# fim pelo git quando a hora de resolução da fonte é estimada e contradiz o git
FIM_PELO_GIT = {
 "03":("2026-10-16T19:20","git 3857c98 (junção); o registro diz ~21h20, estimado pelo maestro (registro-de-juncoes.md:4)"),
 "04":("2026-10-16T19:10","git b68f540 (junção); o registro diz ~20h55, estimado pelo maestro (registro-de-juncoes.md:3)"),
}

def hm(s): return s[:16] if s else None

# texto que aparece na página: sem código interno nem hash solto
TROCAS = [("no 12-busca", "no teste da busca"), ("12-busca", "o teste da busca"),
          ("(27-pastas,", "(teste do verificador de pastas,"), ("do 27-pastas", "do teste do verificador de pastas"),
          ("27-pastas", "teste do verificador de pastas"),
          (" (commit 8d8f1b9)", ""), (" (merge 7c54148)", ""),
          ("; integracao voltou a e98a891", "; a integração voltou ao estado anterior"),
          ("; integracao voltou a e7203b4", "; a integração voltou ao estado anterior"),
          ("no TEMP", "na pasta temporária"), ("do TEMP", "da pasta temporária"),
          ("EPERM", "erro de permissão"), ("em CRLF", "com fim de linha do Windows"),
          ("no HOME", "na pasta do usuário"), ("41+40+43+documentação", "41, 40, 43 e documentação")]
def vis(x):
    if not x: return x
    for a, b in TROCAS: x = x.replace(a, b)
    return x

def nome_curto(titulo):
    return titulo

saida_t = []
sem_hora_total = 0
for t in tickets:
    tid = t["id"]
    c = t.get("construtor") or {}
    if isinstance(c, list): nomes = [x["nome"] if isinstance(x, dict) else x for x in c]
    elif isinstance(c, dict): nomes = [c.get("nome")] if c.get("nome") else (c.get("nomes") or [])
    else: nomes = [c] if c else []
    nomes = [n for n in nomes if n]
    principal = nomes[0] if nomes else None
    juncoes = [j for j in (t.get("juncoes") or []) if j.get("quando")]
    jun_verde = [dict(j, quando=j.get("commit_em") or j["quando"]) for j in juncoes if j.get("resultado") == "verde"]
    res = t.get("resolvido") or {}
    frase = None
    if tid in PRIMEIRO:
        h, q = PRIMEIRO[tid]
        fim, fim_fonte = hm(res.get("quando")), res.get("fonte")
        if tid in FIM_PELO_GIT:
            fim, fim_fonte = FIM_PELO_GIT[tid]
        elif fim and jun_verde and fim < hm(jun_verde[0]["quando"]):
            fim, fim_fonte = hm(jun_verde[0]["quando"]), "git " + jun_verde[0]["hash"] + " (junção; a hora de resolução da fonte vem antes da junção)"
        pend = t.get("pendencia_fechada") or res.get("pendencia_fechada")
        frase = {"ini": q, "ini_fonte": "git " + h + " (primeiro commit do ticket)", "ini_rotulo": "primeiro commit",
                 "fim": fim, "fim_fonte": fim_fonte}
        if pend and pend.get("quando") and fim and pend["quando"] > fim:
            frase["pendente_ate"] = hm(pend["quando"]); frase["pendente_fonte"] = pend.get("fonte")
    # revisões: no tempo só com hora confiável
    revs = []
    for r in t.get("revisao") or []:
        res_r = (r.get("resultado") or "")
        if res_r.upper().startswith("VOLTA"): rr = "VOLTA"
        elif res_r.upper().startswith("PASSA"): rr = "PASSA com ressalvas" if "ressalva" in res_r.lower() else "PASSA"
        else: continue  # leitura intermediária, não conta como rodada
        q = hm(r.get("quando"))
        no_tempo = bool(q) and q >= "2026-10-17T01:00"
        motivo = None
        if not q: motivo = "sem hora na fonte"
        elif not no_tempo: motivo = "hora de comentário da noite de 16/10 (relógio adiantado)"
        if no_tempo and r.get("aproximada") and "03:00" <= q[11:16] <= "04:50" and q.startswith("2026-10-17") and "diario" in (r.get("fonte") or ""):
            no_tempo, motivo = False, "hora do diário no trecho adiantado ~1 h (diario-da-construcao.md:27)"
        if no_tempo and frase:
            fim_total = frase.get("pendente_ate") or frase["fim"]
            if q < frase["ini"] or (fim_total and q > fim_total):
                no_tempo, motivo = False, "hora da fonte fora do intervalo do git (antes do primeiro commit ou depois da resolução)"
        # janela pelo git ("entre 08:45 (...) e 08:56 (conserto f304e6c)"): a rodada fica no intervalo
        jan = None
        m = re.search(r"entre.*?(\d{1,2}:\d\d).*? e .*?(\d{1,2}:\d\d)", (r.get("janela") or "") + " | " + (r.get("nota") or ""))
        if m and frase:
            a, b = m.group(1).zfill(5), m.group(2).zfill(5)
            for dia in ("2026-10-16", "2026-10-17"):
                ja, jb = f"{dia}T{a}", f"{dia}T{b}"
                fim_total = frase.get("pendente_ate") or frase["fim"]
                if ja <= jb and ja >= frase["ini"][:11] + "00:00" and frase["ini"] <= jb and (not fim_total or ja <= fim_total):
                    jan = [ja, jb]; break
        if jan:
            no_tempo, motivo = True, None
            q = jan[0][:11] + "%02d:%02d" % divmod((int(jan[0][11:13])*60+int(jan[0][14:16]) + int(jan[1][11:13])*60+int(jan[1][14:16]))//2, 60)
        if not no_tempo: sem_hora_total += 1
        revs.append({"rodada": r.get("rodada"), "resultado": rr, "quando": q if no_tempo else None,
                     "quando_na_fonte": hm(r.get("quando")), "quem": r.get("quem"), "fonte": r.get("fonte"),
                     **({"janela": jan, "janela_fonte": "git (janela entre commits, ver nota da fonte)"} if jan else {}),
                     **({"fora_do_tempo": motivo} if motivo else {})})
    # ordem: rodada com hora depois da seguinte sai do tempo
    for k in range(len(revs) - 1):
        a, b = revs[k], revs[k + 1]
        if a["quando"] and b["quando"] and a["quando"] > b["quando"]:
            alvo = b if b.get("janela") else a
            alvo["quando"] = None; alvo.pop("janela", None); alvo["fora_do_tempo"] = "hora da fonte fora da ordem das rodadas"; sem_hora_total += 1
    jj = [{"quando": hm(j.get("commit_em") or j["quando"]), "veredito": hm(j.get("registro_em") or (j["quando"] if j.get("commit_em") else None)), "hash": j.get("hash"), "resultado": "vermelha" if "desfeita" in (j.get("resultado") or "") else "verde", "resultado_na_fonte": j.get("resultado"),
           "suite": vis(j.get("suite")), "fonte": j.get("fonte"), "quando_fonte": j.get("quando_fonte")} for j in juncoes]
    orig = t.get("origem")
    if isinstance(orig, dict): orig = dict(orig, motivo=vis(orig.get("motivo")))
    saida_t.append({
        "id": tid, "titulo": t["titulo"], "titulo_curto": nome_curto(t["titulo"]),
        "status": t.get("status"), "blocked_by": t.get("blocked_by") or [], "blocked_by_fonte": t.get("blocked_by_fonte"),
        "origem": orig, "construtores": nomes, "construtor_principal": principal,
        "construtor_fonte": (c.get("fonte") if isinstance(c, dict) else None),
        "frase": frase, "revisao": revs, "juncoes": jj,
        "resolvido": ({"quando": hm(res.get("quando")), "fonte": res.get("fonte")} if res.get("quando") else None),
        "entrega_curta": vis(t.get("entrega_curta")),
        "momentos": [{"quando": hm(m.get("quando")) if (m.get("quando") or "") >= "2026-10-17T01:00" else None,
                      "texto": vis(m.get("evento") or m.get("texto")), "fonte": m.get("fonte")} for m in (t.get("momentos") or [])],
    })

# ---------- junções (acordes do Rebite): hora do commit de junção no git; veredito = hora do registro ----------
R = "etapas/registro-de-juncoes.md"
def S(total, verdes, pulados, falhas): return {"total": total, "verdes": verdes, "pulados": pulados, "falhas": falhas}
J = [
 ("2026-10-16T19:10", ["04"], False, "verde", S(11,11,0,0), "b68f540", 3, None),
 ("2026-10-16T19:20", ["03"], False, "verde", S(11,11,0,0), "3857c98", 4, None),
 ("2026-10-16T19:59", ["02"], False, "verde", S(14,14,0,0), "c8d2267", 5, "2026-10-16T20:00"),
 ("2026-10-16T20:10", ["05"], False, "verde", S(37,37,0,0), "0d04985", 6, "2026-10-16T20:11"),
 ("2026-10-16T20:27", ["01"], False, "verde", S(37,37,0,0), "45ec3b0", 7, "2026-10-16T20:28"),
 ("2026-10-16T20:31", ["06"], False, "verde", S(44,44,0,0), "8b9beef", 8, "2026-10-16T20:32"),
 ("2026-10-16T21:02", ["14"], False, "verde", S(81,81,0,0), "8d1d785", 9, "2026-10-16T21:03"),
 ("2026-10-16T21:49", ["27"], False, "verde", S(106,106,0,0), "0a8e17f", 10, "2026-10-16T21:51"),
 ("2026-10-16T22:00", ["29"], False, "verde", S(116,112,4,0), "d5e4e16", 11, "2026-10-16T22:02"),
 ("2026-10-16T22:24", ["19"], False, "verde", S(133,128,5,0), "dc56d47", 12, "2026-10-16T22:28"),
 ("2026-10-16T23:06", ["12"], False, "verde", S(147,141,6,0), "c5b946a", 13, "2026-10-16T23:10"),
 ("2026-10-16T23:39", ["15"], False, "verde", S(157,150,7,0), "ac1cd2c", 14, "2026-10-16T23:47"),
 ("2026-10-16T23:48", ["20"], False, "verde", S(174,166,8,0), "f83c8f5", 15, "2026-10-17T00:01"),
 ("2026-10-17T00:40", ["30"], False, "verde", S(176,168,8,0), "5d84d76", 17, "2026-10-17T00:53"),
 ("2026-10-17T01:28", ["31","32"], False, "verde", S(186,178,8,0), "357a2ba, 57e85cf", 18, "2026-10-17T01:50"),
 ("2026-10-17T02:02", ["13"], False, "verde", S(190,182,8,0), "236b3ef", 19, "2026-10-17T02:21"),
 ("2026-10-17T02:21", ["31"], False, "verde", S(191,183,8,0), "e82ce65", 20, "2026-10-17T02:51"),
 ("2026-10-17T02:51", ["07","34"], False, "verde", S(194,186,8,0), "24c7543, 763813a", 21, "2026-10-17T03:00"),
 ("2026-10-17T03:42", ["12"], False, "verde", S(194,186,8,0), "3c24d68", 22, "2026-10-17T04:08"),
 ("2026-10-17T04:22", ["35","33"], False, "verde", S(199,191,8,0), "ef38e4d, 33b817a", 23, "2026-10-17T04:53"),
 ("2026-10-17T05:10", ["28","09"], False, "verde", S(202,194,8,0), "ea6f353, 9453e3e", 24, "2026-10-17T06:12"),
 ("2026-10-17T06:28", ["36"], False, "verde", None, "85efe3b", 27, None),
 ("2026-10-17T06:37", ["10"], False, "verde", S(210,202,8,0), "9cc878b", 27, "2026-10-17T07:00"),
 ("2026-10-17T07:32", ["15"], False, "verde", S(210,202,8,0), "e2b7607", 29, "2026-10-17T08:06"),
 ("2026-10-17T08:07", ["08"], False, "verde", S(210,202,8,0), "e98a891", 30, "2026-10-17T08:56"),
 ("2026-10-17T10:12", ["16"], False, "desfeita", S(229,219,8,2), "fce0529", 32, "2026-10-17T10:46"),
 ("2026-10-17T10:52", ["22"], False, "verde", S(215,206,9,0), "4a47576", 31, "2026-10-17T11:21"),
 ("2026-10-17T11:21", ["16","21"], False, "verde", S(253,244,9,0), "30b735f, fdd3760", 33, "2026-10-17T11:41"),
 ("2026-10-17T11:58", ["17"], False, "verde", S(273,263,10,0), "e7203b4", 34, "2026-10-17T12:34"),
 ("2026-10-17T12:33", [], True, "desfeita", None, "74f201a", 35, "2026-10-17T12:37"),
 ("2026-10-17T12:53", ["38","39","22"], False, "verde", S(285,275,10,0), "462e35d, 2d5c528, c42ffa0", 36, "2026-10-17T14:06"),
 ("2026-10-17T14:13", ["42"], False, "verde", S(285,275,10,0), "d298826", 37, "2026-10-17T14:48"),
 ("2026-10-17T14:47", ["41","40","43"], True, "verde", S(289,278,10,1), "e8dde26, 7caed05, 45e34c7, d7a8e07, 576b462, 98a7ced", 38, "2026-10-17T15:22"),
 ("2026-10-17T15:21", [], True, "verde", None, "b22b099", 39, "2026-10-17T15:30"),
 ("2026-10-17T15:20", ["11"], True, "verde", S(294,282,12,0), "51fa382, a7d1517", 40, "2026-10-17T16:16"),
 ("2026-10-17T16:16", ["18","37","23"], False, "verde", S(355,342,13,0), "dc4ed6a, ebfbe6c, 9f122c2", 41, "2026-10-17T16:44"),
 ("2026-10-17T16:44", ["44"], True, "verde", S(358,345,13,0), "df6c2e5, f640bbd", 42, "2026-10-17T17:14"),
 ("2026-10-17T18:31", ["24","22"], False, "verde", S(359,345,14,0), "a4fa7e3, 56cd23a", 43, "2026-10-17T19:22"),
 ("2026-10-17T19:49", ["25"], False, "verde", S(370,355,15,0), "ca62332", 44, "2026-10-17T20:18"),
]
MOTIVO = {
 "fce0529": "a busca recusou o SKILL.md da vigia (YAML inválido); integracao voltou a e98a891",
 "74f201a": "documentação do Lume: a busca não ficou pronta em 3 min indexando os docs; integracao voltou a e7203b4",
 "e8dde26, 7caed05, 45e34c7, d7a8e07, 576b462, 98a7ced": "verde com 1 falha alheia, mantida: o teste do verificador de pastas caiu numa página dos docs; os três tickets resolvidos, os docs pendentes do conserto; a causa no verificador virou o ticket 44",
 "b22b099": "docs: conserto da página; o teste da busca e o do verificador de pastas verdes",
 "85efe3b": "suíte junto com a do 10 (07h00)",
 "51fa382, a7d1517": "a 4ª leva de docs entrou às 15h31, na mesma suíte",
}
juncoes = []
for q, tk, docs, res, suite, h, linha, ver in sorted(J, key=lambda x: x[0]):
    juncoes.append({"quando": q, "quando_fonte": "git " + h.split(",")[0].strip() + " (commit de junção)",
                    "tickets": tk, "docs": docs, "resultado": res, "suite": suite, "hash": h,
                    "veredito": ver, "fonte": f"{R}:{linha}", **({"motivo": vis(MOTIVO[h])} if h in MOTIVO else {}),
                    **({"falha_alheia": True, "resultado_na_fonte": "verde com 1 falha alheia, mantida"} if suite and suite["falhas"] and res != "desfeita" else {})})

n_jun = len(juncoes); n_desf = sum(1 for j in juncoes if j["resultado"] == "desfeita")
n_alheia = sum(1 for j in juncoes if j.get("falha_alheia"))
n_voltas = sum(1 for t in saida_t for r in t["revisao"] if r["resultado"] == "VOLTA")
n_rodadas = sum(len(t["revisao"]) for t in saida_t)
n_res = sum(1 for t in saida_t if (t["status"] or "").startswith("resolved"))
n_nasc = sum(1 for t in saida_t if t["origem"] != "original")
n_docs = sum(1 for j in juncoes if j["docs"])

# o fio do fim: do 25 para trás, o bloqueador que resolveu por último
TT = {t["id"]: t for t in saida_t}
cadeia = ["25"]
while TT[cadeia[-1]]["blocked_by"]:
    bs = [b for b in TT[cadeia[-1]]["blocked_by"] if TT[b]["frase"]]
    cadeia.append(max(bs, key=lambda b: TT[b]["frase"]["fim"]))
cadeia.reverse()
D = "etapas/diario-da-construcao.md"
fatos = {
 "meta": {
  "inicio_partitura": "2026-10-16T14:30", "inicio_fonte": D + ":8 (recomeço ~14h30, /implement-spec)",
  "fim": "2026-10-17T20:17", "fim_fonte": D + ":196 (25 resolvido, construção fechada)",
  "ticket_final": "25",
  "cadeia_fim": cadeia, "cadeia_fim_fonte": "Blocked by de cada ticket (issues/*.md); de cada um, o bloqueador que resolveu por último",
  "relogio": "git é o relógio: ticket = do primeiro commit à resolução; junção = hora do commit de junção. Horas de comentário da noite de 16/10 (adiantadas 2-3 h) e do diário entre ~03h e ~04h45 de 17/10 (~1 h, diario:27) não entram no tempo.",
  "subtitulo": "Trinta horas, do recomeço às 14h30 de 16/10 ao fechamento às 20h17 de 17/10. Cada linha da partitura são <b>{H} horas</b>; cada compasso, <b>uma hora</b>, em escala. Cada pauta é um papel do time.",
  "espera": {"de": "2026-10-16T14:30", "ate": "2026-10-16T18:30", "rotulo": "revisão do spec e /implement-spec", "fonte": D + ":8; primeiro commit de ticket às 18h57 (git 7c6cc47)"},
  "acorde_final": "Quem tocou o quê. Os números vêm dos tickets, dos pareceres da revisão e do registro de junções.",
  "coda": "<b>Fica para depois:</b> o ticket 26, instalação de verdade no par 1, é do Gustavo e segue aberto (vira instalação nas duas máquinas).",
  "rodape": "Fontes: diário do maestro, registro de junções, tickets (issues/), pareceres e git do hub. Arquivo de fatos: resumo-visual/fatos-peca-1.json.",
 },
 "numeros": {
  "tickets": {"v": len(saida_t), "d": f"{len(saida_t)-n_nasc} do plano e {n_nasc} que nasceram no caminho", "fonte": "issues/*.md"},
  "resolvidos": {"v": n_res, "d": "o 26, instalação de verdade, ficou com o Gustavo", "fonte": "issues/*.md (Status:)"},
  "voltas": {"v": n_voltas, "d": f"vezes que a revisão devolveu, em {n_rodadas} rodadas", "fonte": "etapas/parecer-*.md (contagem por ticket no campo revisao)"},
  "juncoes": {"v": n_jun, "d": f"vezes que o Rebite juntou e rodou a suíte; {n_desf} desfeitas: a vigia (10h46) e os docs (12h37)", "fonte": R},
  "testes": {"v": 370, "d": "355 verdes · 15 pulados · 0 falhas", "fonte": R + ":44"},
 },
 "equipe": [
  {"nome": "Fiel", "papel": "revisor", "v": n_rodadas, "r": "rodadas (com as do Fielzinho)", "d": f"{n_voltas} voltas. Com o Fielzinho (segunda leitura no Codex) até as 14h37.", "fonte": "pareceres; " + D + ":164"},
  {"nome": "Rebite", "papel": "integrador", "v": n_jun, "r": "junções", "d": f"{n_jun-n_desf-n_alheia} verdes, {n_alheia} com falha alheia mantida, {n_desf} desfeitas. A suíte cresceu de 11 para 370 testes.", "fonte": R},
  {"nome": "Lume", "papel": "documentador, desde 12h05", "v": n_docs, "r": "junções com docs", "d": "Documentação técnica em agents/code/docs/; uma leva desfeita às 12h37.", "fonte": R + ":35-42; " + D + ":140; git 62e93f7"},
  {"nome": "Maestro", "papel": "regência", "v": 9, "r": "decisões para rever", "d": "Tomadas pelo mandato do Gustavo, para conferir com ele.", "fonte": "../context-hub/retomada-maestro.md:70-85"},
 ],
 "maestro": [
  {"quando": "2026-10-16T14:30", "rotulo": "recomeço · /implement-spec", "fonte": D + ":8", "aproximada": True},
  {"quando": "2026-10-16T20:29", "rotulo": "etapa 0 completa", "fonte": "git f06368e (C:/Projetos/context-hub)"},
  {"quando": "2026-10-16T21:53", "rotulo": "etapa 1 fechada", "fonte": "git a42b952 (C:/Projetos/context-hub)"},
  {"quando": "2026-10-17T03:19", "rotulo": "mandato do Gustavo", "detalhe": "o maestro decide por ele, com critério, e registra", "fonte": "git d7a0f33 (C:/Projetos/context-hub); " + D + ":22"},
  {"quando": "2026-10-17T03:23", "rotulo": "até 4 construtores, 1 subagente", "detalhe": "Cinzel recrutado para o 09", "fonte": "git 2e605d1 (C:/Projetos/context-hub); " + D + ":23"},
  {"quando": "2026-10-17T03:25", "rotulo": "subagentes Haiku", "detalhe": "até três, para tarefa simples ou conferência", "fonte": "git 8493aaf (C:/Projetos/context-hub); " + D + ":24"},
  {"quando": "2026-10-17T04:15", "rotulo": "suíte só na junção", "detalhe": "a suíte inteira roda só com o Rebite, para poupar memória", "fonte": "git 1d3a611 (C:/Projetos/context-hub); " + D + ":31"},
  {"quando": "2026-10-17T12:05", "rotulo": "documentador: Lume entra", "detalhe": "pedido do Gustavo: um agente só de documentação técnica", "fonte": "git 62e93f7 (C:/Projetos/context-hub); " + D + ":140"},
  {"quando": "2026-10-17T14:33", "rotulo": "Codex só para testes", "detalhe": "execução e revisão no Claude; o Fielzinho sai", "fonte": "git a1c7fb0 (C:/Projetos/context-hub); " + D + ":163"},
  {"quando": "2026-10-17T20:17", "rotulo": "construção fechada", "fonte": D + ":196"},
 ],
 "reinicio": {"quando": "2026-10-17T10:05", "rotulo": "reinício do Maestri; os sete recrutas voltaram sozinhos", "fonte": D + ":201 (~10h05) e :117", "aproximada": True},
 "janelas_quietas": [
  {"inicio": "2026-10-17T09:34", "fim": "2026-10-17T10:03", "rotulo": "janela quieta", "fora": ["Rebite","Cinzel","Fiel","Trilho"], "fonte": D + ":109-111, :116"},
  {"inicio": "2026-10-17T13:22", "fim": "2026-10-17T14:17", "rotulo": "janela quieta 2", "fora": ["Trilho","Cinzel","Lume","Fiel","Brasa"], "fonte": D + ":153-154, :158"},
  {"inicio": "2026-10-17T16:52", "fim": "2026-10-17T18:20", "rotulo": "janela quieta da noite", "fora": ["Fiel","Vela","Cinzel","Lume"], "fonte": D + ":176, :185"},
 ],
 "lume": {"entra": "2026-10-17T12:05", "entra_fonte": D + ":140; git 62e93f7", "levas": [
  {"quando": j["quando"], "resultado": "verde" if j["resultado"] == "verde" else "vermelha",
   "rotulo": ("docs desfeitos: a busca estourou o prazo" if j["resultado"] == "desfeita" else "docs juntados"), "fonte": j["fonte"]}
  for j in juncoes if j["docs"]]},
 "fielzinho": {"sai": "2026-10-17T14:37", "fonte": D + ":164"},
 "tickets": saida_t,
 "juncoes": juncoes,
}
(SAIDA / "fatos-peca-1.json").write_text(json.dumps(fatos, ensure_ascii=False, indent=1), encoding="utf-8")
modelo = (AQUI / "peca-1.template.html").read_text(encoding="utf-8")
html = re.sub(r"/\*FATOS\*/.*?/\*FIM\*/", lambda m: json.dumps(fatos, ensure_ascii=False), modelo, flags=re.S)
(SAIDA / "peca-1-partitura.html").write_text(html, encoding="utf-8")
print(f"tickets {len(saida_t)} resolvidos {n_res} nascidos {n_nasc} voltas {n_voltas} rodadas {n_rodadas} "
      f"fora do tempo {sem_hora_total} junções {n_jun} desfeitas {n_desf}")
for t in saida_t:
    f = t["frase"]
    print(t["id"], t["construtor_principal"], f and f["ini"][5:], f and (f["fim"] or "")[5:], f and f.get("pendente_ate"),
          "".join(("V" if r["resultado"] == "VOLTA" else "P") + ("" if r["quando"] else "?") for r in t["revisao"]))
