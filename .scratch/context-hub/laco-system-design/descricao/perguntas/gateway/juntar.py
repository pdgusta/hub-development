"""Juntador: tira repetidas por sentido de forma barata e grava perguntas.jsonl.

Repetida = Jaccard ponderado dos tokens (sem acentos, sem palavras vazias, raiz por prefixo), com peso IDF calculado
sobre todas as perguntas do livro-razão (palavra de molde, como "grupo" ou "Gustavo", pesa pouco; nome de peça pesa
muito), acima do limiar do config.json, E as peças e atores citados (léxicos ATORES e ENTIDADES, tirados do resumo
neutro) com Jaccard de pelo menos 0,5 em cada um: perguntas de molde igual sobre peças diferentes não são repetidas. A comparação é contra o texto representante de cada grupo (a primeira vez
que a pergunta apareceu). Calibração em calibracao.md.
Determinístico: relê o livro-razão inteiro em ordem e monta tudo do zero.

Uso avulso: python juntar.py [--base PASTA]   (refaz perguntas.jsonl a partir de livros/chamadas.jsonl)
"""
import argparse, collections, json, os, re, unicodedata

AQUI = os.path.dirname(os.path.abspath(__file__))

VAZIAS = set("""
a o as os um uma uns umas de do da dos das no na nos nas em ao aos à às pelo pela pelos pelas por para pra pro
e ou mas nem que se é ser sao são foi sera será esta está estao estão isso isto esse essa esses essas este estes
ele ela eles elas lhe seu sua seus suas meu minha nosso nossa com sem sobre entre ate até ja já mais muito
the of to and in on for is are be
acontece acontecer aconteceria acontecem ocorre ocorrer hub context contexto
""".split())

# peças e atores (palavras do resumo neutro); "eu" vira "gustavo" porque é a voz da lente do Gustavo
ATORES_TXT = """
gustavo agente agentes maestro maestri recruta recrutas cliente clientes sandbox par pares maquina maquinas notebook
pessoal outra codex copilot claude desktop harness leitor construtor
"""
ENTIDADES_TXT = """
obsidian markdown vista banco couchdb sincronizador sync livesync
plugin cli mcp busca embeddings vigia notificacao github backup tailscale tailnet rede ssh pasta pastas replicada
contrato agents skill skills hook nota notas retomada porta portas raiz raizes clients operations initiatives
reference inbox archive arquivo arquivos arquivar iniciativa iniciativas casa acervo papel papeis guarda colisao
conflito divergencia tela versao binario strata voegol avianca trf3 sbf vault tarefa checagem sessao disco senha
chave chaves token setup contrato-opcao peca pecas grande 200 mib ponto
"""
ENT_MIN = 0.5

INTERROGATIVAS = {"quem", "onde", "quando", "qual", "quais", "como", "porque", "quanto", "quantos", "nao"}


def tirar_acentos(s):
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()


def normalizar(texto):
    s = tirar_acentos((texto or "").lower())
    s = re.sub(r"\bpor\s+que\b|\bpor\s+que\b", "porque", s)
    s = re.sub(r"[^a-z0-9]+", " ", s)
    s = re.sub(r"eu", "gustavo", s)
    return " ".join(s.split())


VAZIAS_N = {tirar_acentos(w) for w in VAZIAS}


def tokens(texto, prefixo=6):
    out = set()
    for w in normalizar(texto).split():
        if w in VAZIAS_N and w not in INTERROGATIVAS:
            continue
        if len(w) > 4 and w.endswith("s"):
            w = w[:-1]
        out.add(w[:prefixo])
    return frozenset(out)


def entidades(tk, prefixo=6):
    """(atores, peças) citados na pergunta."""
    at, pc = _ent(prefixo)
    return frozenset(t for t in tk if t in at), frozenset(t for t in tk if t in pc)


_ENT = {}


def _ent(prefixo):
    if prefixo not in _ENT:
        _ENT[prefixo] = (tokens(ATORES_TXT, prefixo), tokens(ENTIDADES_TXT, prefixo))
    return _ENT[prefixo]


def mesmo_assunto(ea, eb):
    """Atores e peças precisam coincidir em pelo menos ENT_MIN (Jaccard), cada conjunto por si."""
    for a, b in zip(ea, eb):
        if (a or b) and jaccard(a, b) < ENT_MIN:
            return False
    return True


def jaccard(a, b, w=None):
    if not a or not b:
        return 0.0
    if w is None:
        i = len(a & b)
        return i / (len(a) + len(b) - i)
    p = lambda s: sum(w.get(t, 1.0) for t in s)
    i = p(a & b)
    return i / (p(a) + p(b) - i)


def calcular_idf(textos, prefixo=6, piso=0.05):
    """Peso de cada token: log(N/df), com piso, sobre as perguntas distintas (normalizadas)."""
    import math
    distintos = {normalizar(t): t for t in textos}
    n = max(len(distintos), 1)
    df = collections.Counter()
    for t in distintos.values():
        df.update(tokens(t, prefixo))
    return {k: max(math.log(n / v), piso) for k, v in df.items()}, max(math.log(n), piso)


class Banco:
    """Grupos de perguntas com o mesmo sentido; índice invertido por token para achar candidatas."""

    def __init__(self, limiar, prefixo=6, idf=None, idf_novo=1.0):
        self.limiar, self.prefixo = limiar, prefixo
        self.idf, self.idf_novo = idf or {}, idf_novo
        self.grupos = []          # dicts
        self.toks = []            # frozenset do representante
        self.pesos = []           # soma dos pesos do representante
        self.indice = collections.defaultdict(list)
        self.exatas = {}
        self.ents = []

    def achar(self, tk, norm):
        if norm in self.exatas:
            return self.exatas[norm], 1.0
        w = lambda t: self.idf.get(t, self.idf_novo)
        conta = collections.Counter()
        for t in tk:
            for g in self.indice.get(t, ()):
                conta[g] += w(t)
        pa = sum(w(t) for t in tk)
        ea = entidades(tk, self.prefixo)
        melhor, mj = None, 0.0
        for g, inter in conta.items():
            j = inter / (pa + self.pesos[g] - inter)
            if j > mj and mesmo_assunto(ea, self.ents[g]):
                melhor, mj = g, j
        return (melhor, mj) if mj >= self.limiar else (None, mj)

    def adicionar(self, q, meta):
        """Devolve (indice_do_grupo, nova?)."""
        norm = normalizar(q["pergunta"])
        tk = tokens(q["pergunta"], self.prefixo)
        g, j = self.achar(tk, norm)
        if g is None:
            g = len(self.grupos)
            self.grupos.append({"id": f"g{g + 1:05d}", "pergunta": q["pergunta"].strip(), "tipo": q["tipo"],
                                "lente": q["lente"], "cita": list(q.get("cita") or []), "vezes": 0,
                                "modelos": collections.Counter(), "familias": set(), "celulas": set(),
                                "lentes": set(), "tipos": set(), "primeira_onda": meta["onda"], "variantes": []})
            self.toks.append(tk)
            self.ents.append(entidades(tk, self.prefixo))
            self.pesos.append(sum(self.idf.get(t, self.idf_novo) for t in tk))
            for t in tk:
                self.indice[t].append(g)
            self.exatas[norm] = g
            nova = True
        else:
            nova = False
            e = self.grupos[g]
            if len(e["variantes"]) < 3 and normalizar(e["pergunta"]) != norm:
                e["variantes"].append(q["pergunta"].strip())
        e = self.grupos[g]
        e["vezes"] += 1
        e["modelos"][meta["modelo"]] += 1
        e["familias"].add(meta["familia"])
        e["celulas"].add(meta["celula"])
        e["lentes"].add(q["lente"])
        e["tipos"].add(q["tipo"])
        return g, nova


def ler_livro(base):
    f = os.path.join(base, "livros", "chamadas.jsonl")
    regs = []
    if os.path.exists(f):
        for l in open(f, encoding="utf-8"):
            try:
                r = json.loads(l)
            except Exception:
                continue
            if r.get("estado") == "aceito":
                regs.append(r)
    regs.sort(key=lambda r: (r["onda"], r["ts"]))
    return regs


def juntar(base, limiar, prefixo=6):
    """Remonta o banco do zero. Devolve (banco, estatística por onda, estatística por célula)."""
    regs = ler_livro(base)
    idf, idf_novo = calcular_idf([q["pergunta"] for r in regs for q in r["perguntas"]], prefixo)
    b = Banco(limiar, prefixo, idf, idf_novo)
    por_onda = collections.defaultdict(lambda: {"chamadas": 0, "validas": 0, "novas": 0})
    por_celula = collections.defaultdict(lambda: {"chamadas": 0, "validas": 0, "novas": 0, "familias": set(),
                                                  "ultima_taxa": None})
    for r in regs:
        o, c = por_onda[r["onda"]], por_celula[r["celula"]]
        o["chamadas"] += 1
        c["chamadas"] += 1
        c["familias"].add(r["familia"])
        vistas, novas = set(), 0
        for q in r["perguntas"]:
            n = normalizar(q["pergunta"])
            if n in vistas:          # a mesma pergunta duas vezes na mesma chamada conta uma vez
                continue
            vistas.add(n)
            _, nova = b.adicionar(q, r)
            novas += nova
        o["validas"] += len(vistas)
        o["novas"] += novas
        c["validas"] += len(vistas)
        c["novas"] += novas
        c["ultima_taxa"] = novas / len(vistas) if vistas else 0.0
    return b, por_onda, por_celula


def gravar_perguntas(base, banco):
    caminho = os.path.join(base, "perguntas.jsonl")
    tmp = caminho + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        for e in banco.grupos:
            f.write(json.dumps({
                "id": e["id"], "pergunta": e["pergunta"], "tipo": e["tipo"], "lente": e["lente"], "cita": e["cita"],
                "vezes": e["vezes"], "modelos": dict(e["modelos"].most_common()), "familias": sorted(e["familias"]),
                "celulas": sorted(e["celulas"]), "lentes": sorted(e["lentes"]), "tipos": sorted(e["tipos"]),
                "primeira_onda": e["primeira_onda"], "variantes": e["variantes"]}, ensure_ascii=False) + "\n")
    os.replace(tmp, caminho)
    return caminho


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default=AQUI)
    a = ap.parse_args()
    cfg = json.load(open(os.path.join(AQUI, "config.json"), encoding="utf-8"))
    b, po, _ = juntar(a.base, cfg["limiar_jaccard"], cfg["prefixo_raiz"])
    print(gravar_perguntas(a.base, b), len(b.grupos), "únicas")
    for k in sorted(po):
        v = po[k]
        print("onda", k, v, f"{(v['novas'] / v['validas'] if v['validas'] else 0):.1%}")


if __name__ == "__main__":
    main()
