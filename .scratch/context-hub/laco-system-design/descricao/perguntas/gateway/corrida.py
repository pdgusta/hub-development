"""Corrida do gerador de perguntas pelo FreeLLMAPI (etapa 1a do laço da descrição do hub).

Um processo só: roteador de modelos (orçamento por modelo, ritmo, saúde), 20 trabalhadores, ondas e juntador.
Os modelos só respondem; o script valida e grava. Retoma de onde parou se rodar de novo com a mesma --base.

Uso:
  python corrida.py                      # corrida inteira (onda 1 = todas as 288 células), base = esta pasta
  python corrida.py --teste              # teste curto: 3 células x 4 modelos, base = teste/
Para parar: crie o arquivo PARAR na base (a onda em curso fecha com o que já chegou e sai com fim.txt).
"""
import argparse, collections, concurrent.futures as cf, json, os, random, re, sys, threading, time, traceback
import urllib.error, urllib.parse, urllib.request
from datetime import datetime, timedelta, timezone

import juntar
import prompts

AQUI = os.path.dirname(os.path.abspath(__file__))


def iso(ts=None):
    return datetime.fromtimestamp(ts or time.time(), timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def segredo(nome):
    v = os.environ.get(nome)
    if v:
        return v
    if os.name == "nt":
        import winreg
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment") as k:
                return winreg.QueryValueEx(k, nome)[0]
        except OSError:
            pass
    raise SystemExit(f"variável {nome} não encontrada")


class Corrida:
    def __init__(self, base, cfg):
        self.base, self.cfg = base, cfg
        for d in ("livros", "ondas", "estado", "logs"):
            os.makedirs(os.path.join(base, d), exist_ok=True)
        self.chave = segredo(cfg["variavel_chave"])
        self.lock = threading.Lock()
        self.livro_lock = threading.Lock()
        self.parar = threading.Event()
        self.motivo = None
        self.estado = self.ler_json("estado/estado.json", None)
        if not self.estado:
            self.estado = {"inicio": time.time(), "onda": 1, "historico": [], "tentativas": 0, "fim": None}
        self.uso = self.ler_json("estado/uso.json", {})      # {modelo: {janela: tentativas}}
        self.m = {}
        for mid, info in cfg["modelos"].items():
            self.m[mid] = dict(info, id=mid, em_voo=0, fora_ate=0.0, falhas=0, acertos=0, erros=0, excluido=None,
                               ritmo=collections.deque())
        self.ritmo_pool = collections.defaultdict(collections.deque)

    # ------------------------------------------------------------ arquivos
    def p(self, rel):
        return os.path.join(self.base, rel)

    def ler_json(self, rel, padrao):
        try:
            with open(self.p(rel), encoding="utf-8") as f:
                return json.load(f)
        except (OSError, ValueError):
            return padrao

    def gravar_json(self, rel, obj):
        tmp = self.p(rel) + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(obj, f, ensure_ascii=False, indent=1)
        os.replace(tmp, self.p(rel))

    def anexar(self, reg):
        with self.livro_lock:
            with open(self.p("livros/chamadas.jsonl"), "a", encoding="utf-8") as f:
                f.write(json.dumps(reg, ensure_ascii=False) + "\n")

    def log(self, *a):
        print(iso(), *a, flush=True)

    # ------------------------------------------------------------ gateway
    def http(self, metodo, rota, corpo=None, timeout=150):
        req = urllib.request.Request(self.cfg["gateway"] + rota, method=metodo,
                                     data=json.dumps(corpo).encode() if corpo is not None else None,
                                     headers={"Authorization": "Bearer " + self.chave, "Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=timeout) as f:
                return f.status, dict(f.headers), json.load(f)
        except urllib.error.HTTPError as e:
            try:
                d = json.loads(e.read().decode("utf-8", "replace"))
            except Exception:
                d = {}
            return e.code, dict(e.headers or {}), d
        except Exception as e:
            return None, {}, {"error": {"message": f"{type(e).__name__}: {e}"}}

    def conferir_catalogo(self):
        st, _, cat = self.http("GET", "/v1/models", timeout=30)
        if st != 200:
            self.log("catálogo não respondeu:", st)
            return
        status = {m["id"]: m.get("execution_status") for m in cat.get("data", [])}
        for mid, m in self.m.items():
            s = status.get(mid)
            if s != "ready" and m["excluido"] is None:
                m["excluido"] = f"status_{s}"
                self.log("fora:", mid, s)
            elif s == "ready" and (m["excluido"] or "").startswith("status_"):
                m["excluido"] = None

    # ------------------------------------------------------------ roteador
    def janela(self, pool, t=None):
        hora = self.cfg["virada_utc"].get(pool, self.cfg["virada_utc"]["padrao"])
        d = datetime.fromtimestamp(t or time.time(), timezone.utc)
        ini = d.replace(hour=hora, minute=0, second=0, microsecond=0)
        if d < ini:
            ini -= timedelta(days=1)
        return ini.strftime("%Y-%m-%dT%H")

    def proxima_virada(self, pool):
        ini = datetime.strptime(self.janela(pool), "%Y-%m-%dT%H").replace(tzinfo=timezone.utc)
        return (ini + timedelta(days=1)).timestamp() + 60

    def usado(self, m):
        return self.uso.get(m["id"], {}).get(self.janela(m["pool"]), 0)

    def somar_uso(self, m, n):
        j = self.janela(m["pool"])
        self.uso.setdefault(m["id"], {})[j] = self.uso.get(m["id"], {}).get(j, 0) + n
        self.estado["tentativas"] += n

    def checar_tetos(self):
        if self.estado["tentativas"] >= self.cfg["teto_tentativas"]:
            self.encerrar("teto de tentativas")
        elif time.time() - self.estado["inicio"] >= self.cfg["teto_horas"] * 3600:
            self.encerrar("teto de tempo")
        elif os.path.exists(self.p("PARAR")):
            self.encerrar("arquivo PARAR")

    def encerrar(self, motivo):
        if not self.parar.is_set():
            self.motivo = motivo
            self.parar.set()
            self.log("parando:", motivo)

    def escolher(self, excluir, familias_evitar):
        with self.lock:
            self.checar_tetos()
            if self.parar.is_set():
                return "parar"
            t = time.time()
            voo_pool = collections.Counter()
            for m in self.m.values():
                voo_pool[m["pool"]] += m["em_voo"]
            cands = []
            for m in self.m.values():
                if m["excluido"] or m["fora_ate"] > t or m["id"] in excluir:
                    continue
                if m["em_voo"] >= self.cfg["max_em_voo_modelo"]:
                    continue
                if voo_pool[m["pool"]] >= self.cfg["max_em_voo_pool"].get(m["pool"], self.cfg["max_em_voo_pool"]["padrao"]):
                    continue
                if self.usado(m) + 1 > m["teto_dia"]:
                    continue
                while m["ritmo"] and m["ritmo"][0] < t - 60:
                    m["ritmo"].popleft()
                if m.get("rpm") and len(m["ritmo"]) >= m["rpm"]:
                    continue
                rp = self.cfg["rpm_pool"].get(m["pool"])
                if rp:
                    q = self.ritmo_pool[m["pool"]]
                    while q and q[0] < t - 60:
                        q.popleft()
                    if len(q) >= rp:
                        continue
                folga = min(m["teto_dia"] - self.usado(m), 100)
                taxa = (m["acertos"] + 1) / (m["acertos"] + m["erros"] + 2)
                peso = max(folga * taxa, 0.01) * (0.15 if m["familia"] in familias_evitar else 1.0)
                cands.append((m, peso))
            if not cands:
                vivos = [m for m in self.m.values() if not m["excluido"] and self.usado(m) < m["teto_dia"]
                         and m["fora_ate"] < t + 3600]
                if not vivos:
                    self.encerrar("cota orçada esgotada: nenhum modelo com folga na próxima hora")
                    return "parar"
                return None
            m = random.choices([c[0] for c in cands], weights=[c[1] for c in cands])[0]
            m["em_voo"] += 1
            m["ritmo"].append(t)
            self.ritmo_pool[m["pool"]].append(t)
            return m

    def liberar(self, m, resultado, tentativas):
        with self.lock:
            m["em_voo"] = max(m["em_voo"] - 1, 0)
            self.somar_uso(m, tentativas)
            t = time.time()
            if resultado == "ok":
                m["acertos"] += 1
                m["falhas"] = 0
            elif resultado == "invalido":
                m["erros"] += 1
            elif resultado in ("cota", "provedor"):
                m["erros"] += 1
                m["falhas"] += 1
                if resultado == "cota" and m["falhas"] >= self.cfg["cotas_seguidas_ate_dia"]:
                    m["fora_ate"] = self.proxima_virada(m["pool"])
                elif resultado == "cota":
                    m["fora_ate"] = t + self.cfg["espera_cota_s"]
                elif m["falhas"] >= self.cfg["falhas_ate_pausa"]:
                    m["fora_ate"] = t + self.cfg["pausa_falhas_s"]
            elif resultado == "sumiu":
                m["excluido"] = "sumiu_no_provedor"
            self.gravar_json("estado/uso.json", self.uso)
            self.gravar_json("estado/estado.json", self.estado)

    # ------------------------------------------------------------ uma chamada
    @staticmethod
    def classificar(st, d):
        e = d.get("error") if isinstance(d, dict) else None
        msg = str(e.get("message", "") if isinstance(e, dict) else (e or ""))
        if st == 200:
            return "200", msg
        if st == 429:
            return "cota", msg
        if st == 404:
            return "sumiu", msg
        if st == 400:
            return "invalido", msg
        return "provedor", msg

    @staticmethod
    def extrair_json(texto):
        t = re.sub(r"<think>.*?</think>", "", texto or "", flags=re.S).strip()
        for a, b in (("{", "}"), ("[", "]")):
            i, j = t.find(a), t.rfind(b)
            if i >= 0 and j > i:
                try:
                    return json.loads(t[i:j + 1])
                except Exception:
                    pass
        return None

    def validar(self, o, celula):
        lente, tipo, _ = celula.split("|")
        if isinstance(o, dict):
            lista = o.get("perguntas")
            if not isinstance(lista, list):
                lista = next((v for v in o.values() if isinstance(v, list)), None)
        else:
            lista = o if isinstance(o, list) else None
        if not isinstance(lista, list):
            return None, 'a resposta precisa ser um objeto JSON com a lista "perguntas"'
        boas = []
        for i in lista[: self.cfg["max_perguntas_por_chamada"]]:
            if isinstance(i, str):
                i = {"pergunta": i}
            if not isinstance(i, dict) or not isinstance(i.get("pergunta"), str):
                continue
            q = " ".join(i["pergunta"].split()).strip().strip('"')
            if not q.endswith("?"):
                q += "?"
            if q.count("?") > 1 or not 15 <= len(q) <= 350:
                continue
            ti = i.get("tipo") if i.get("tipo") in prompts.TIPOS else tipo
            cita = [str(c) for c in i.get("cita", []) if isinstance(c, (str, int))] if isinstance(i.get("cita"), list) else []
            boas.append({"pergunta": q, "tipo": ti, "lente": lente, "cita": cita[:8]})
        if len(boas) < self.cfg["min_perguntas_validas"]:
            return None, f"só {len(boas)} perguntas válidas; mande de 8 a 15, cada uma com o campo pergunta terminando em ?"
        return boas, None

    def atender(self, onda, celula, vaga, prompt, familias_evitar):
        tentados = []
        while len(tentados) < self.cfg["max_modelos_por_chamada"]:
            m = None
            while m is None:
                m = self.escolher(set(tentados), familias_evitar)
                if m is None:
                    time.sleep(self.cfg["espera_sem_modelo_s"] * (0.5 + random.random()))
            if m == "parar":
                return None
            tentados.append(m["id"])
            texto_prompt, max_tok = prompt, (self.cfg["max_tokens_raciocina"] if m.get("raciocina") else self.cfg["max_tokens"])
            gasto, resultado = 0, "invalido"
            for reenvio in range(self.cfg["reenvios_json"] + 2):
                corpo = {"model": m["id"], "messages": [{"role": "user", "content": texto_prompt}],
                         "temperature": self.cfg["temperatura"], "max_tokens": max_tok}
                t0 = time.time()
                st, h, d = self.http("POST", "/v1/chat/completions", corpo, timeout=self.cfg["timeout_s"])
                extra = 0
                for k, v in h.items():
                    if k.lower() == "x-fallback-attempts":
                        try:
                            extra = int(v)
                        except ValueError:
                            pass
                via = next((urllib.parse.unquote(v) for k, v in h.items() if k.lower() == "x-routed-via"), None)
                gasto += 1 + extra
                tipo, msg = self.classificar(st, d)
                esc = ((d.get("choices") or [{}])[0]) if isinstance(d, dict) else {}
                texto = (esc.get("message") or {}).get("content") or ""
                fim = esc.get("finish_reason")
                reg = {"ts": iso(), "onda": onda, "celula": celula, "vaga": vaga, "modelo": m["id"],
                       "familia": m["familia"], "pool": m["pool"], "via": via, "tentativas_chave": 1 + extra,
                       "http": st, "latencia_s": round(time.time() - t0, 1), "fim": fim, "reenvio": reenvio,
                       "uso": d.get("usage") if isinstance(d, dict) else None}
                if tipo != "200":
                    reg.update(estado=tipo, erro=msg[:400])
                    self.anexar(reg)
                    resultado = tipo
                    break
                o = self.extrair_json(texto)
                if o is None and fim == "length" and max_tok < self.cfg["max_tokens_raciocina"]:
                    reg.update(estado="truncado", conteudo=texto[:3000])
                    self.anexar(reg)
                    with self.lock:
                        m["raciocina"] = True
                    max_tok = self.cfg["max_tokens_raciocina"]
                    continue
                perguntas, erro = self.validar(o, celula) if o is not None else (
                    None, "não achei um objeto JSON na resposta" if texto.strip() else "resposta vazia")
                if perguntas:
                    reg.update(estado="aceito", perguntas=perguntas)
                    self.anexar(reg)
                    self.liberar(m, "ok", gasto)
                    return reg
                reg.update(estado="invalido", erro=erro, conteudo=texto[:3000])
                self.anexar(reg)
                resultado = "invalido"
                if not texto.strip() or reenvio >= self.cfg["reenvios_json"]:
                    break
                texto_prompt = prompt + f"\n\nSua resposta anterior foi recusada: {erro}. Responda de novo SÓ com o objeto JSON."
            self.liberar(m, resultado, gasto)
        self.anexar({"ts": iso(), "onda": onda, "celula": celula, "vaga": vaga, "estado": "esgotado", "tentados": tentados})
        return None

    # ------------------------------------------------------------ ondas
    def onda_arquivo(self, n):
        return f"ondas/onda-{n}.json"

    def feitas(self, n):
        """(celula, vaga) já aceitas nesta onda, para retomar."""
        out = set()
        for r in juntar.ler_livro(self.base):
            if r["onda"] == n:
                out.add((r["celula"], r.get("vaga", 0)))
        return out

    def rodar_onda(self, n, plano):
        feitas = self.feitas(n)
        fila = [x for x in plano["itens"] if (x["celula"], x["vaga"]) not in feitas]
        self.log(f"onda {n}: {len(plano['itens'])} chamadas no plano, {len(fila)} a fazer")
        self.conferir_catalogo()
        _, _, pc = juntar.juntar(self.base, self.cfg["limiar_jaccard"], self.cfg["prefixo_raiz"])
        contagem = {"ok": 0, "falhou": 0}

        def um(x):
            if self.parar.is_set():
                return
            try:
                evitar = set(pc[x["celula"]]["familias"]) if x["celula"] in pc else set()
                evitar |= set(x.get("evitar", []))
                r = self.atender(n, x["celula"], x["vaga"], prompts.montar_prompt(x["celula"], x.get("ja_temos", [])), evitar)
                with self.lock:
                    contagem["ok" if r else "falhou"] += 1
                    tot = contagem["ok"] + contagem["falhou"]
                if tot % 20 == 0:
                    self.log(f"onda {n}: {contagem['ok']} aceitas, {contagem['falhou']} sem resposta, "
                             f"{self.estado['tentativas']} tentativas no total")
            except Exception:
                self.anexar({"ts": iso(), "onda": n, "celula": x["celula"], "estado": "erro_do_script",
                             "erro": traceback.format_exc()[-800:]})

        with cf.ThreadPoolExecutor(self.cfg["trabalhadores"]) as ex:
            list(ex.map(um, fila))
        return contagem

    def fechar_onda(self, n, plano, contagem):
        b, po, pc = juntar.juntar(self.base, self.cfg["limiar_jaccard"], self.cfg["prefixo_raiz"])
        juntar.gravar_perguntas(self.base, b)
        o = po.get(n, {"chamadas": 0, "validas": 0, "novas": 0})
        taxa = o["novas"] / o["validas"] if o["validas"] else 0.0
        hist = [h for h in self.estado["historico"] if h["onda"] != n]
        hist.append({"onda": n, "fechada_em": iso(), "chamadas_plano": len(plano["itens"]), "aceitas": o["chamadas"],
                     "validas": o["validas"], "novas": o["novas"], "taxa_novas": round(taxa, 4),
                     "unicas_total": len(b.grupos), "tentativas_total": self.estado["tentativas"]})
        self.estado["historico"] = hist
        self.log(f"onda {n} fechada: {o['novas']} novas de {o['validas']} ({taxa:.1%}); {len(b.grupos)} únicas")
        return b, pc, taxa

    def planejar(self, n, b, pc):
        """Onda n: as células menos cobertas (menos perguntas novas creditadas), com o que já temos na lente e tipo."""
        cels = prompts.celulas()
        chave = lambda c: (pc[c]["novas"] if c in pc else -1, -(pc[c]["ultima_taxa"] if c in pc and pc[c]["ultima_taxa"] is not None else 1))
        escolhidas = sorted(cels, key=chave)[: self.cfg["celulas_por_onda_seguinte"]]
        por_lt = collections.defaultdict(list)
        for e in sorted(b.grupos, key=lambda e: -e["vezes"]):
            for c in e["celulas"]:
                l, t, _ = c.split("|")
                if len(por_lt[(l, t)]) < self.cfg["exemplos_ja_temos"] and e["pergunta"] not in por_lt[(l, t)]:
                    por_lt[(l, t)].append(e["pergunta"])
        itens = []
        for c in escolhidas:
            l, t, _ = c.split("|")
            itens.append({"celula": c, "vaga": 0, "ja_temos": por_lt.get((l, t), [])})
        return {"onda": n, "criada_em": iso(), "origem": "menos cobertas", "itens": itens}

    def relatorio(self, n, plano, contagem, b, pc, taxa, proximo):
        regs = [json.loads(l) for l in open(self.p("livros/chamadas.jsonl"), encoding="utf-8")] \
            if os.path.exists(self.p("livros/chamadas.jsonl")) else []
        regs = [r for r in regs if r.get("onda") == n and "modelo" in r]
        pm = collections.defaultdict(lambda: collections.Counter())
        for r in regs:
            pm[r["modelo"]][r["estado"]] += 1
            pm[r["modelo"]]["perguntas"] += len(r.get("perguntas", []))
        por_lente = collections.Counter(e["lente"] for e in b.grupos)
        por_tipo = collections.Counter(e["tipo"] for e in b.grupos)
        L = [f"# Onda {n}", "", f"Fechada em {iso()}. Plano: {len(plano['itens'])} chamadas ({plano['origem']}); "
             f"aceitas {contagem.get('ok', 0)}, sem resposta {contagem.get('falhou', 0)}.", ""]
        h = self.estado["historico"][-1]
        L += [f"Perguntas válidas na onda: {h['validas']}; novas: {h['novas']}; **taxa de novas: {taxa:.1%}**; "
                      f"únicas no banco: {len(b.grupos)}; tentativas no total: {self.estado['tentativas']}.", "",
                      "## Histórico", "", "| Onda | Aceitas | Válidas | Novas | Taxa | Únicas |", "|---|---|---|---|---|---|"]
        L += [f"| {x['onda']} | {x['aceitas']} | {x['validas']} | {x['novas']} | {x['taxa_novas']:.1%} | {x['unicas_total']} |"
              for x in self.estado["historico"]]
        L += ["", "## Modelos nesta onda", "", "| Modelo | Aceitas | Inválidas | Cota | Provedor | Perguntas |", "|---|---|---|---|---|---|"]
        L += [f"| {k} | {v['aceito']} | {v['invalido'] + v['truncado']} | {v['cota']} | {v['provedor'] + v['sumiu']} | {v['perguntas']} |"
              for k, v in sorted(pm.items(), key=lambda kv: -kv[1]["aceito"])]
        L += ["", "## Únicas por lente", ""] + [f"- {k}: {v}" for k, v in sorted(por_lente.items(), key=lambda kv: kv[1])]
        L += ["", "## Únicas por tipo", ""] + [f"- {k}: {v}" for k, v in sorted(por_tipo.items(), key=lambda kv: kv[1])]
        L += ["", "## Próximo passo", "", proximo, ""]
        with open(self.p(f"ondas/onda-{n}.md"), "w", encoding="utf-8") as f:
            f.write("\n".join(L))

    def fim(self, motivo):
        self.estado["fim"] = {"motivo": motivo, "em": iso()}
        self.gravar_json("estado/estado.json", self.estado)
        h = self.estado["historico"]
        L = [f"motivo: {motivo}", f"terminou em: {iso()}", f"começou em: {iso(self.estado['inicio'])}",
             f"ondas: {len(h)}", f"únicas: {h[-1]['unicas_total'] if h else 0}", f"tentativas: {self.estado['tentativas']}",
             "taxas de novas por onda: " + ", ".join(f"{x['onda']}={x['taxa_novas']:.1%}" for x in h)]
        with open(self.p("fim.txt"), "w", encoding="utf-8") as f:
            f.write("\n".join(L) + "\n")
        self.log("fim:", motivo)

    # ------------------------------------------------------------ laço
    def correr(self, plano1, uma_onda=False):
        with open(self.p("estado/pid.txt"), "w") as f:
            f.write(str(os.getpid()))
        if self.estado.get("fim"):
            self.log("esta base já terminou:", self.estado["fim"]); return
        n = self.estado["onda"]
        if not os.path.exists(self.p(self.onda_arquivo(1))):
            self.gravar_json(self.onda_arquivo(1), plano1)
        while True:
            plano = self.ler_json(self.onda_arquivo(n), None)
            contagem = self.rodar_onda(n, plano)
            b, pc, taxa = self.fechar_onda(n, plano, contagem)
            h = self.estado["historico"]
            k = self.cfg["ondas_seguidas_no_gate"]
            saturou = len(h) >= k and all(x["taxa_novas"] <= self.cfg["gate_novas"] for x in h[-k:])
            motivo = None
            if uma_onda:
                motivo = "teste de uma onda"
            elif saturou:
                motivo = f"saturação: {k} ondas seguidas com {self.cfg['gate_novas']:.0%} ou menos de novas"
            elif self.parar.is_set():
                motivo = self.motivo
            elif n >= self.cfg["max_ondas"]:
                motivo = "máximo de ondas"
            if motivo:
                self.relatorio(n, plano, contagem, b, pc, taxa, f"**Fim:** {motivo}.")
                self.fim(motivo)
                return
            prox = self.planejar(n + 1, b, pc)
            self.gravar_json(self.onda_arquivo(n + 1), prox)
            self.relatorio(n, plano, contagem, b, pc, taxa, f"Onda {n + 1}: {len(prox['itens'])} células menos cobertas.")
            n += 1
            self.estado["onda"] = n
            self.gravar_json("estado/estado.json", self.estado)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--teste", action="store_true")
    ap.add_argument("--base")
    a = ap.parse_args()
    cfg = json.load(open(os.path.join(AQUI, "config.json"), encoding="utf-8"))
    if a.teste:
        base = a.base or os.path.join(AQUI, "teste")
        cels = ["gustavo-dia-a-dia|se-x|pratica", "falhas-divergencia|falha|borda", "grupos-onde-vive|grupo|pratica"]
        plano1 = {"onda": 1, "criada_em": iso(), "origem": "teste: 3 células x 4 vagas",
                  "itens": [{"celula": c, "vaga": v} for c in cels for v in range(4)]}
        cfg = dict(cfg, trabalhadores=12)
    else:
        base = a.base or AQUI
        plano1 = {"onda": 1, "criada_em": iso(), "origem": "plano: 12 lentes x 12 tipos x 2 formulações",
                  "itens": [{"celula": c, "vaga": 0} for c in prompts.celulas()]}
    os.makedirs(base, exist_ok=True)
    c = Corrida(base, cfg)
    try:
        c.correr(plano1, uma_onda=a.teste)
    except Exception:
        c.log("erro fatal:", traceback.format_exc())
        c.fim("erro do script: " + traceback.format_exc().strip().splitlines()[-1][:300])
        raise


if __name__ == "__main__":
    main()
