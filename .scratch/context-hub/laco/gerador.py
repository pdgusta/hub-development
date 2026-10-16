"""Gerador: tira pedidos da fila do seu grupo de línguas, pede um modelo ao despachante, chama o gateway
com o modelo fixado, valida a resposta e grava tudo no livro-razão `livros/<grupo>.jsonl`.

Uso: python gerador.py --grupo pt-es   (grupos em config.json; vários trabalhadores em paralelo)
Para quando o teto é atingido ou quando `controle.parar` é verdadeiro; retoma de onde parou.
"""
import argparse, json, random, threading, time, uuid
from comum import abrir_banco, agora, anexar, caminho, carregar_config, cabecalho, extrair_json, http, iso, ler_controle
import despachante

TIPOS = {"tool", "library", "concept", "assembly", "service"}


def validar(o):
    """Devolve (itens, None) ou (None, explicação do erro, para reenviar ao modelo)."""
    if not isinstance(o, dict) or not isinstance(o.get("items"), list):
        return None, 'the answer must be a JSON object with an "items" array'
    itens = o["items"]
    if not 1 <= len(itens) <= 20:
        return None, f'"items" must have between 1 and 20 entries, got {len(itens)}'
    for n, i in enumerate(itens):
        if not isinstance(i, dict):
            return None, f"items[{n}] is not an object"
        falta = {"name", "url", "kind", "summary"} - set(i)
        if falta:
            return None, f"items[{n}] is missing {sorted(falta)}"
        if not isinstance(i["name"], str) or not i["name"].strip():
            return None, f"items[{n}].name is empty"
        if i["kind"] not in TIPOS:
            return None, f'items[{n}].kind must be one of {sorted(TIPOS)}'
        if not isinstance(i.get("url"), str):
            return None, f'items[{n}].url must be a string (use "" when unsure)'
        if "terms" in i and not isinstance(i["terms"], list):
            return None, f"items[{n}].terms must be a list of strings"
    return itens, None


def classificar(st, h, d):
    msg = str((d.get("error") or {}).get("message", "") if isinstance(d.get("error"), dict) else d.get("error", ""))
    if st == 200:
        return "200", msg
    if st == 429:
        return "cota", msg
    if st == 404:
        return "sumiu", msg
    if st == 400 and ("audio/speech" in msg or "model name format" in msg or "not chat" in msg.lower()):
        return "nao_e_chat", msg
    if st == 400:
        return "invalido", msg
    return "provedor", msg


class Gerador:
    def __init__(self, cfg, grupo, nome):
        self.cfg, self.grupo, self.nome = cfg, grupo, nome
        self.livro = caminho("livros", f"{grupo}.jsonl")
        self.vivo = True

    # -------------------------------------------------- fila
    def pegar(self, con):
        con.execute("BEGIN IMMEDIATE")
        onda = ler_controle(con, "onda", 1)
        p = con.execute("""SELECT p.*, c.prompt, c.onda, c.lingua, c.profundidade FROM pedidos p JOIN celulas c ON p.celula=c.id
                           WHERE c.grupo=? AND c.onda<=? AND p.estado IN ('pendente','adiado') AND p.proximo_em<=?
                           ORDER BY c.onda, p.proximo_em LIMIT 1""", (self.grupo, onda, agora())).fetchone()
        if p:
            con.execute("UPDATE pedidos SET estado='em_voo', em_voo_desde=?, gerador=? WHERE id=?", (agora(), self.nome, p["id"]))
        con.execute("COMMIT")
        return dict(p) if p else None

    def devolver(self, con, p, estado, espera=0.0, tentado=None, erro=None, modelo=None):
        tentados = json.loads(p["tentados"])
        if tentado and tentado not in tentados:
            tentados.append(tentado)
        if estado in ("pendente", "adiado") and len(tentados) >= self.cfg["max_modelos_por_pedido"]:
            estado = "esgotado"
        con.execute("""UPDATE pedidos SET estado=?, proximo_em=?, tentados=?, erro_ultimo=COALESCE(?, erro_ultimo),
                       modelo=COALESCE(?, modelo), em_voo_desde=NULL WHERE id=?""",
                    (estado, agora() + espera, json.dumps(tentados), erro, modelo, p["id"]))
        if estado in ("aceito", "esgotado", "dividido"):
            self.fechar_celula(con, p["celula"])
        return estado

    def fechar_celula(self, con, celula):
        estados = [r[0] for r in con.execute("SELECT estado FROM pedidos WHERE celula=?", (celula,))]
        if all(e in ("aceito", "esgotado", "dividido", "cancelado") for e in estados):
            novo = "concluida" if "aceito" in estados or "dividido" in estados else "esgotada"
            con.execute("UPDATE celulas SET estado=? WHERE id=?", (novo, celula))

    def par(self, con, p):
        """Família e pool do modelo da outra vaga, para o par ter famílias e pools diferentes."""
        o = con.execute("SELECT modelo FROM pedidos WHERE celula=? AND vaga<>?", (p["celula"], p["vaga"])).fetchone()
        if not o or not o["modelo"]:
            return None, None
        m = con.execute("SELECT familia, pool FROM modelos WHERE id=?", (o["modelo"],)).fetchone()
        return (m["familia"], m["pool"]) if m else (None, None)

    def dividir(self, con, p):
        """Resposta cortada num modelo que já raciocina: a célula vira duas menores."""
        c = con.execute("SELECT * FROM celulas WHERE id=?", (p["celula"],)).fetchone()
        if c["profundidade"] >= self.cfg["profundidade_max_divisao"]:
            return False
        for metade in self.cfg["metades_da_divisao"]:
            cid = f'{c["id"]}.{metade["sufixo"]}'
            if con.execute("SELECT 1 FROM celulas WHERE id=?", (cid,)).fetchone():
                continue
            prompt = c["prompt"] + "\n\n" + metade["instrucao"]
            con.execute("INSERT INTO celulas (id, onda, grupo, lingua, angulo, origem, prompt, profundidade) VALUES (?,?,?,?,?,?,?,?)",
                        (cid, c["onda"], c["grupo"], c["lingua"], c["angulo"], "divisao", prompt, c["profundidade"] + 1))
            for vaga in (0, 1):
                con.execute("INSERT INTO pedidos (id, celula, vaga) VALUES (?,?,?)", (f"{cid}#{vaga}", cid, vaga))
        con.execute("UPDATE pedidos SET estado='cancelado' WHERE celula=? AND id<>? AND estado IN ('pendente','adiado')",
                    (c["id"], p["id"]))
        return True

    # -------------------------------------------------- um pedido
    def atender(self, con, p):
        cfg = self.cfg
        fam, pool = self.par(con, p)
        m = despachante.escolher(con, cfg, excluir=set(json.loads(p["tentados"])), familia_proibida=fam, pool_proibido=pool)
        if m == "teto":
            self.devolver(con, p, "pendente")
            self.vivo = False
            return
        if m is None:
            self.devolver(con, p, "adiado", espera=cfg["espera_sem_modelo_s"] * (0.5 + random.random()))
            return
        prompt = p["prompt"]
        for reenvio in range(cfg["reenvios_json"] + 1):
            corpo = {"model": m["id"], "messages": [{"role": "user", "content": prompt}], "temperature": cfg["temperatura"],
                     "max_tokens": cfg["max_tokens_raciocina"] if m["raciocina"] else cfg["max_tokens"]}
            if m["aceita_rf"] and cfg.get("usar_response_format"):
                corpo["response_format"] = {"type": "json_object"}
            t0 = agora()
            st, h, d = http(cfg, "POST", "/v1/chat/completions", corpo, timeout=cfg["timeout_s"])
            extra = int(cabecalho(h, "X-Fallback-Attempts") or 0)
            tipo, msg = classificar(st, h, d)
            escolha = ((d.get("choices") or [{}])[0]) if isinstance(d, dict) else {}
            texto = (escolha.get("message") or {}).get("content") or ""
            fim = escolha.get("finish_reason")
            reg = {"ts": iso(), "pedido": p["id"], "celula": p["celula"], "onda": p["onda"], "lingua": p["lingua"],
                   "modelo": m["id"], "familia": m["familia"], "pool": m["pool"], "via": cabecalho(h, "X-Routed-Via"),
                   "tentativas_chave": 1 + extra, "http": st, "latencia_s": round(agora() - t0, 1), "fim": fim,
                   "uso": d.get("usage") if isinstance(d, dict) else None, "reenvio": reenvio, "gerador": self.nome}
            if tipo != "200":
                reg.update(estado=tipo, erro=msg[:500])
                anexar(self.livro, reg)
                despachante.liberar(con, cfg, m["id"], m["plataforma"], tipo, extra)
                if tipo == "cota":
                    k = len(json.loads(p["tentados"]))
                    self.devolver(con, p, "adiado", espera=min(cfg["espera_cota_s"] * 2 ** k, 1800) * (0.5 + random.random()))
                else:
                    self.devolver(con, p, "pendente", tentado=m["id"], erro=f"{tipo}: {msg[:200]}")
                return
            o = extrair_json(texto)
            cortado = fim == "length" or (o is None and texto.count("{") > texto.count("}"))
            if cortado:
                reg.update(estado="truncado", conteudo=texto[:cfg["guardar_chars"]])
                anexar(self.livro, reg)
                despachante.liberar(con, cfg, m["id"], m["plataforma"], "invalido" if m["raciocina"] else "neutro", extra)
                if not m["raciocina"]:
                    con.execute("UPDATE modelos SET raciocina=1 WHERE id=?", (m["id"],))
                    self.devolver(con, p, "pendente", erro="truncado: max_tokens subiu")
                elif self.dividir(con, p):
                    self.devolver(con, p, "dividido", erro="truncado: célula dividida")
                else:
                    self.devolver(con, p, "pendente", tentado=m["id"], erro="truncado no tamanho mínimo")
                return
            itens, erro = validar(o) if o is not None else (None, "no JSON object found in the answer" if texto.strip() else "empty answer")
            if itens is not None:
                reg.update(estado="aceito", itens=itens)
                anexar(self.livro, reg)
                despachante.liberar(con, cfg, m["id"], m["plataforma"], "ok", extra)
                self.devolver(con, p, "aceito", modelo=m["id"])
                return
            reg.update(estado="invalido", erro=erro, conteudo=texto[:cfg["guardar_chars"]])
            anexar(self.livro, reg)
            if not texto.strip() or reenvio == cfg["reenvios_json"]:
                despachante.liberar(con, cfg, m["id"], m["plataforma"], "invalido", extra)
                self.devolver(con, p, "pendente", tentado=m["id"], erro=f"invalido: {erro}")
                return
            # reenvia ao mesmo modelo, com o erro apontado; a vaga do modelo continua reservada
            con.execute("""INSERT INTO uso VALUES (?,?,?) ON CONFLICT(modelo, janela) DO UPDATE SET tentativas = tentativas + ?""",
                        (m["id"], despachante.janela(cfg, m["plataforma"]), 1 + extra, 1 + extra))
            prompt = p["prompt"] + f"\n\nYour previous answer was rejected: {erro}. Reply again with ONLY the JSON object."

    # -------------------------------------------------- trabalhadores
    def trabalhar(self):
        con = abrir_banco()
        while self.vivo:
            if ler_controle(con, "parar", False):
                break
            p = self.pegar(con)
            if not p:
                time.sleep(self.cfg["espera_fila_vazia_s"])
                continue
            try:
                self.atender(con, p)
            except Exception as e:  # nunca deixa o pedido preso em voo
                anexar(self.livro, {"ts": iso(), "pedido": p["id"], "estado": "erro_do_script", "erro": repr(e)[:500]})
                try:
                    con.execute("ROLLBACK")
                except Exception:
                    pass
                self.devolver(con, p, "pendente")
                time.sleep(5)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--grupo", required=True)
    ap.add_argument("--trabalhadores", type=int)
    a = ap.parse_args()
    cfg = carregar_config()
    if a.grupo not in cfg["grupos"]:
        raise SystemExit(f"grupo desconhecido; use um de {list(cfg['grupos'])}")
    g = Gerador(cfg, a.grupo, f"{a.grupo}-{uuid.uuid4().hex[:6]}")
    n = a.trabalhadores or cfg["trabalhadores_por_gerador"]
    ts = [threading.Thread(target=g.trabalhar, daemon=True) for _ in range(n)]
    for t in ts:
        t.start()
    print(iso(), g.nome, "com", n, "trabalhadores", flush=True)
    for t in ts:
        t.join()
    print(iso(), g.nome, "parou", flush=True)


if __name__ == "__main__":
    main()
