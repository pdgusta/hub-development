"""A torre: servidor local e API do portal (§3.4).

Uso: ``python nucleo/torre.py <caminho do projeto.json>``

Escuta só em ``127.0.0.1``, na porta do ``projeto.json``. Lê os arquivos do projeto a cada pedido,
devolve JSON e grava apenas na caixa. Só biblioteca padrão.
"""

from __future__ import annotations

import datetime as _dt
import json
import os
import re
import sys
import threading
import urllib.parse
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

if __package__:
    from . import aviso as _aviso
    from . import caixa as _caixa
    from . import lacos as _lacos
    from . import leitores
else:  # executado como script: python nucleo/torre.py
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import aviso as _aviso  # type: ignore
    import caixa as _caixa  # type: ignore
    import lacos as _lacos  # type: ignore
    import leitores  # type: ignore

TAMANHO_MAXIMO = 256 * 1024
TEXTO_MAXIMO = 20_000
INTERVALO_REPARO = 30.0
EXTENSOES_CARTA = {".html", ".htm", ".js", ".mjs", ".css", ".json", ".svg", ".png", ".jpg", ".jpeg", ".gif",
                   ".webp", ".woff", ".woff2", ".ttf", ".mp3", ".mp4", ".webm"}
MIME = {
    ".html": "text/html; charset=utf-8", ".htm": "text/html; charset=utf-8",
    ".css": "text/css; charset=utf-8", ".js": "text/javascript; charset=utf-8",
    ".mjs": "text/javascript; charset=utf-8", ".json": "application/json; charset=utf-8",
    ".svg": "image/svg+xml", ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
    ".gif": "image/gif", ".webp": "image/webp", ".ico": "image/x-icon",
    ".woff": "font/woff", ".woff2": "font/woff2", ".ttf": "font/ttf",
    ".mp3": "audio/mpeg", ".mp4": "video/mp4", ".webm": "video/webm",
    ".txt": "text/plain; charset=utf-8", ".md": "text/plain; charset=utf-8",
}
PASTA_WEB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "web")


class ErroApi(Exception):
    """Erro que vira resposta JSON ``{"erro", "mensagem", "campo"}``."""

    def __init__(self, status: int, codigo: str, mensagem: str, campo: str | None = None, extra: dict | None = None):
        super().__init__(mensagem)
        self.status = status
        self.codigo = codigo
        self.mensagem = mensagem
        self.campo = campo
        self.extra = extra or {}


# ----------------------------------------------------------------------------------------------
# Validação do POST /api/caixa (§3.4)
# ----------------------------------------------------------------------------------------------


def _texto_livre(valor, campo: str, obrigatorio: bool = False) -> str | None:
    if valor is None or valor == "":
        if obrigatorio:
            raise ErroApi(400, "texto-obrigatorio", f"o campo {campo} precisa de texto", campo)
        return None
    if not isinstance(valor, str):
        raise ErroApi(400, "tipo-errado", f"o campo {campo} precisa ser texto", campo)
    if len(valor) > TEXTO_MAXIMO:
        raise ErroApi(400, "texto-longo", f"o campo {campo} passa de {TEXTO_MAXIMO} caracteres", campo)
    if obrigatorio and not valor.strip():
        raise ErroApi(400, "texto-obrigatorio", f"o campo {campo} precisa de texto", campo)
    return valor


def _so_chaves(objeto: dict, permitidas: set[str], campo: str) -> None:
    for chave in objeto:
        if chave not in permitidas:
            raise ErroApi(400, "chave-desconhecida", f"chave desconhecida em {campo}: {chave}", f"{campo}.{chave}")


def _achar_alvo(alvo, estado: dict) -> tuple[dict, str | None, str | None]:
    """Devolve ``(alvo normalizado, ticket dono, título em palavras)``; 400 se não existe."""
    if not isinstance(alvo, dict):
        raise ErroApi(400, "alvo-invalido", "alvo precisa ser um objeto com tipo e id", "alvo")
    _so_chaves(alvo, {"tipo", "id"}, "alvo")
    tipo, aid = alvo.get("tipo"), alvo.get("id")
    if tipo not in ("ticket", "carta", "rodada"):
        raise ErroApi(400, "alvo-invalido", "alvo.tipo precisa ser ticket, carta ou rodada", "alvo.tipo")
    if not isinstance(aid, str) or not aid:
        raise ErroApi(400, "alvo-invalido", "alvo.id precisa ser texto", "alvo.id")
    if tipo == "ticket":
        t = next((t for t in estado["tickets"] if t["numero"] == aid), None)
        if t is None:
            raise ErroApi(400, "alvo-inexistente", f"não existe ticket {aid}", "alvo.id")
        return {"tipo": tipo, "id": aid, "titulo": t["titulo"]}, aid, t["titulo"]
    if tipo == "carta":
        c = next((c for c in estado["cartas"] if c["id"] == aid), None)
        if c is None:
            raise ErroApi(400, "alvo-inexistente", f"não existe carta {aid}", "alvo.id")
        return {"tipo": tipo, "id": aid, "titulo": c.get("titulo")}, c.get("ticket"), c.get("titulo")
    r = next((r for r in estado["rodadas"] if r["id"] == aid), None)
    if r is None:
        raise ErroApi(400, "alvo-inexistente", f"não existe rodada {aid}", "alvo.id")
    return {"tipo": tipo, "id": aid, "titulo": r.get("titulo")}, r.get("ticket"), r.get("titulo")


def _validar_substitui(valor, caixa: _caixa.Caixa, alvo_id: str, tipo: str) -> str | None:
    if valor is None:
        return None
    if not isinstance(valor, str) or valor not in caixa.nomes():
        raise ErroApi(400, "substitui-invalido", "substitui precisa ser o nome de uma mensagem da caixa", "substitui")
    try:
        anterior = caixa.dados_de(valor)
    except (OSError, ValueError):
        raise ErroApi(400, "substitui-invalido", "a mensagem substituída não pôde ser lida", "substitui") from None
    if anterior["tipo"] != tipo or anterior["alvo"]["id"] != alvo_id:
        raise ErroApi(400, "substitui-invalido", "substitui aponta para mensagem de outro alvo ou tipo", "substitui")
    return valor


def _validar_resposta_pergunta(pergunta: dict, resposta, campo: str) -> dict:
    if not isinstance(resposta, dict):
        raise ErroApi(400, "resposta-invalida", f"a resposta em {campo} precisa ser um objeto", campo)
    tipo = pergunta["tipo"]
    limpa: dict = {}
    if tipo in ("escolha", "varias"):
        _so_chaves(resposta, {"escolha", "outra", "comentario"}, campo)
        escolha = resposta.get("escolha")
        if escolha is None:
            escolha = []
        if not isinstance(escolha, list) or not all(isinstance(e, str) for e in escolha):
            raise ErroApi(400, "escolha-invalida", f"{campo}.escolha precisa ser uma lista de chaves", f"{campo}.escolha")
        chaves = {o["chave"] for o in pergunta["opcoes"]}
        for e in escolha:
            if e not in chaves:
                raise ErroApi(400, "chave-inexistente", f"a opção {e!r} não existe na pergunta", f"{campo}.escolha")
        if len(set(escolha)) != len(escolha):
            raise ErroApi(400, "escolha-invalida", "opção repetida na escolha", f"{campo}.escolha")
        if tipo == "escolha" and len(escolha) > 1:
            raise ErroApi(400, "escolha-invalida", "esta pergunta aceita uma opção só", f"{campo}.escolha")
        limpa["escolha"] = escolha
        limpa["outra"] = _texto_livre(resposta.get("outra"), f"{campo}.outra")
        limpa["comentario"] = _texto_livre(resposta.get("comentario"), f"{campo}.comentario")
    elif tipo == "aprovar":
        _so_chaves(resposta, {"veredito", "comentario"}, campo)
        veredito = resposta.get("veredito")
        if veredito is not None and veredito not in ("aprovado", "aprovado-com-ajuste", "recusado"):
            raise ErroApi(400, "veredito-invalido", "veredito precisa ser aprovado, aprovado-com-ajuste ou recusado",
                          f"{campo}.veredito")
        comentario = _texto_livre(resposta.get("comentario"), f"{campo}.comentario")
        if veredito in ("aprovado-com-ajuste", "recusado") and not (comentario and comentario.strip()):
            raise ErroApi(400, "comentario-obrigatorio", f"{veredito} exige comentário", f"{campo}.comentario")
        limpa["veredito"] = veredito
        limpa["comentario"] = comentario
    elif tipo == "texto":
        _so_chaves(resposta, {"texto", "comentario"}, campo)
        limpa["texto"] = _texto_livre(resposta.get("texto"), f"{campo}.texto")
        limpa["comentario"] = _texto_livre(resposta.get("comentario"), f"{campo}.comentario")
    elif tipo == "proposta":
        _so_chaves(resposta, {"linhas", "comentario"}, campo)
        linhas = resposta.get("linhas")
        if linhas is not None:
            limpa["linhas"] = _validar_linhas_proposta(pergunta, linhas, f"{campo}.linhas")
        limpa["comentario"] = _texto_livre(resposta.get("comentario"), f"{campo}.comentario")
    else:
        raise ErroApi(400, "tipo-desconhecido", f"pergunta de tipo desconhecido: {tipo}", campo)
    return limpa


def _validar_linhas_proposta(pergunta: dict, linhas, campo: str) -> list[dict]:
    original = pergunta["proposta"] or {"colunas": [], "linhas": [], "pode": []}
    colunas = set(original["colunas"])
    ids_base = {l["id"] for l in original["linhas"]}
    if not isinstance(linhas, list):
        raise ErroApi(400, "proposta-invalida", f"{campo} precisa ser uma lista de linhas", campo)
    vistos: set[str] = set()
    limpas: list[dict] = []
    for i, linha in enumerate(linhas):
        c = f"{campo}[{i}]"
        if not isinstance(linha, dict):
            raise ErroApi(400, "proposta-invalida", "cada linha precisa ser um objeto", c)
        _so_chaves(linha, {"id", "ativa", "valores"}, c)
        lid = linha.get("id")
        if not isinstance(lid, str) or not lid:
            raise ErroApi(400, "proposta-invalida", "linha sem id", f"{c}.id")
        if lid in vistos:
            raise ErroApi(400, "linha-repetida", f"id de linha repetido: {lid}", f"{c}.id")
        vistos.add(lid)
        if lid not in ids_base and not re.fullmatch(r"nova-\d+", lid):
            raise ErroApi(400, "proposta-invalida", f"linha {lid!r} não é da rodada nem segue nova-N", f"{c}.id")
        ativa = linha.get("ativa", True)
        if not isinstance(ativa, bool):
            raise ErroApi(400, "proposta-invalida", "ativa precisa ser true ou false", f"{c}.ativa")
        valores = linha.get("valores", {})
        if valores is None:
            valores = {}
        if not isinstance(valores, dict):
            raise ErroApi(400, "proposta-invalida", "valores precisa ser um objeto", f"{c}.valores")
        for col, v in valores.items():
            if col not in colunas:
                raise ErroApi(400, "coluna-inexistente", f"a coluna {col!r} não existe na proposta", f"{c}.valores.{col}")
            if v is not None and not isinstance(v, (str, int, float, bool)):
                raise ErroApi(400, "proposta-invalida", f"valor de {col} precisa ser texto ou número", f"{c}.valores.{col}")
            if isinstance(v, str) and len(v) > TEXTO_MAXIMO:
                raise ErroApi(400, "texto-longo", f"valor de {col} passa de {TEXTO_MAXIMO} caracteres", f"{c}.valores.{col}")
        limpas.append({"id": lid, "ativa": ativa, "valores": valores})
    analise = _caixa.analisar_proposta(original, limpas)
    pode = set(original.get("pode") or [])
    fora = sorted(analise["operacoes"] - pode)
    if fora:
        raise ErroApi(400, "operacao-nao-permitida", "a proposta não permite: " + ", ".join(fora), campo)
    return limpas


def validar_post(corpo: dict, estado: dict, caixa: _caixa.Caixa) -> dict:
    """Valida um corpo novo (envio ainda não gravado) e devolve o ``.json`` pronto para a caixa."""
    tipo = corpo.get("tipo")
    if tipo not in ("resposta", "comentario", "aprovacao"):
        raise ErroApi(400, "tipo-invalido", "tipo precisa ser resposta, comentario, aprovacao ou alteracao-laco",
                      "tipo")
    envio = corpo["envio"]
    corpo_sem_envio = {k: v for k, v in corpo.items() if k != "envio"}
    dados: dict = {"envio": envio, "tipo": tipo, "enviada": leitores.agora_iso()}

    if tipo == "resposta":
        _so_chaves(corpo, {"envio", "tipo", "rodada", "base", "respostas", "substitui"}, "corpo")
        rid = corpo.get("rodada")
        if not isinstance(rid, str) or not rid:
            raise ErroApi(400, "rodada-invalida", "rodada precisa ser o id de uma rodada", "rodada")
        rodada = next((r for r in estado["rodadas"] if r["id"] == rid), None)
        if rodada is None:
            raise ErroApi(409, "rodada-mudou", f"a rodada {rid} não existe (mais)", "rodada")
        if rodada["malformada"]:
            raise ErroApi(400, "rodada-malformada", f"a rodada está malformada: {rodada['erro']}", "rodada")
        if rodada["estado"] != "aberta":
            raise ErroApi(409, "rodada-mudou", f"a rodada não está aberta (estado: {rodada['estado']})", "rodada")
        if corpo.get("base") != rodada["base"]:
            raise ErroApi(409, "rodada-mudou", "a rodada foi editada depois que a página a carregou", "base")
        respostas = corpo.get("respostas")
        if not isinstance(respostas, dict):
            raise ErroApi(400, "respostas-invalidas", "respostas precisa ser um objeto id → resposta", "respostas")
        por_id = {p["id"]: p for p in rodada["perguntas"]}
        limpas: dict = {}
        for pid, resposta in respostas.items():
            if pid not in por_id:
                raise ErroApi(400, "pergunta-inexistente", f"a pergunta {pid!r} não existe na rodada", f"respostas.{pid}")
            limpas[pid] = _validar_resposta_pergunta(por_id[pid], resposta, f"respostas.{pid}")
        if all(_caixa._em_branco(por_id[pid]["tipo"], r) for pid, r in limpas.items()):
            raise ErroApi(400, "nada-respondido", "nenhuma pergunta foi respondida", "respostas")
        dados["alvo"] = {"tipo": "rodada", "id": rid, "titulo": rodada["titulo"]}
        dados["ticket"] = rodada["ticket"]
        dados["substitui"] = _validar_substitui(corpo.get("substitui"), caixa, rid, tipo)
        dados["rodada"] = {
            "id": rid, "base": rodada["base"], "titulo": rodada["titulo"], "ticket": rodada["ticket"],
            "perguntas": [{"id": p["id"], "titulo": p["titulo"], "tipo": p["tipo"], "recomendada": p["recomendada"],
                           "opcoes": p["opcoes"], "proposta": p["proposta"]} for p in rodada["perguntas"]],
        }
    else:
        permitidas = {"envio", "tipo", "alvo", "texto", "substitui"}
        if tipo == "aprovacao":
            permitidas.add("veredito")
        _so_chaves(corpo, permitidas, "corpo")
        alvo, ticket, _ = _achar_alvo(corpo.get("alvo"), estado)
        if tipo == "comentario":
            _texto_livre(corpo.get("texto"), "texto", obrigatorio=True)
        else:
            veredito = corpo.get("veredito")
            if veredito not in ("aprovado", "recusado"):
                raise ErroApi(400, "veredito-invalido", "veredito precisa ser aprovado ou recusado", "veredito")
            _texto_livre(corpo.get("texto"), "texto", obrigatorio=(veredito == "recusado"))
        dados["alvo"] = alvo
        dados["ticket"] = ticket
        dados["substitui"] = _validar_substitui(corpo.get("substitui"), caixa, alvo["id"], tipo)
    # o corpo guardado é o que a página mandou (sem o envio): o hash dele é o da idempotência
    dados["corpo_hash"] = leitores.hash_corpo(corpo_sem_envio)
    dados["corpo"] = corpo_sem_envio
    return dados


# ----------------------------------------------------------------------------------------------
# A torre (estado compartilhado do servidor)
# ----------------------------------------------------------------------------------------------


class Torre:
    def __init__(self, caminho_projeto: str, ambiente=None, silencioso: bool = False) -> None:
        self.projeto = leitores.Projeto(caminho_projeto)
        if not self.projeto.caixa:
            # sem caixa dentro da pasta do portal não há onde gravar com segurança (§3.2): não sobe
            motivo = next((m for m in self.projeto.problemas_config if m.startswith("caixa:")), "caixa inválida")
            raise ValueError(f"projeto.json: {motivo}; não há onde gravar com segurança")
        self.ambiente = os.environ if ambiente is None else ambiente
        self.silencioso = silencioso
        self.lock = threading.RLock()
        os.makedirs(self.projeto.caixa, exist_ok=True)
        self.caixa: _caixa.Caixa | None = None  # a reconciliação do arranque pode pedir títulos antes de existir
        self.caixa = _caixa.Caixa(self.projeto.caixa, self.lock, resolver_titulo=self._titulo_do_alvo)
        self.porta_real: int | None = None
        self._parar = threading.Event()
        self._reparo: threading.Thread | None = None
        self.emissor: _aviso.Emissor | None = None  # canal A; só existe com o canal disponível ao subir

    def _titulo_do_alvo(self, tipo: str | None, aid: str | None) -> str | None:
        estado = self.estado()
        colecao = {"ticket": ("tickets", "numero"), "carta": ("cartas", "id"), "rodada": ("rodadas", "id")}.get(tipo)
        if not colecao:
            return None
        item = next((x for x in estado[colecao[0]] if x[colecao[1]] == aid), None)
        return item.get("titulo") if item else None

    def estado(self) -> dict:
        estado = leitores.montar_estado(self.projeto.caminho_json, self.ambiente, projeto=self.projeto)
        extras = [{"arquivo": self.projeto.relativo(c), "mensagem": m}
                  for c, m in (self.caixa.problemas if self.caixa is not None else [])]
        # laços (§4.4): registro, laco.json malformado e pedidos com estado desconhecido ou recibo inválido; os
        # laços em si não entram no estado (têm rotas próprias)
        try:
            extras += [{"arquivo": a, "mensagem": m} for a, m in _lacos.problemas_dos_lacos(self.projeto)]
        except Exception as e:  # noqa: BLE001 - um laço ruim nunca derruba o estado
            extras.append({"arquivo": "lacos.json", "mensagem": f"laços não puderam ser lidos: {e}"})
        if extras:
            vistos = {(p["arquivo"], p["mensagem"]) for p in estado["problemas"]}
            estado["problemas"] += [p for p in extras if (p["arquivo"], p["mensagem"]) not in vistos]
            estado["problemas"].sort(key=lambda p: (p["arquivo"], p["mensagem"]))
        return estado

    def hosts_permitidos(self) -> set[str]:
        porta = self.porta_real or self.projeto.porta
        return {f"127.0.0.1:{porta}", f"localhost:{porta}"}

    def origens_permitidas(self) -> set[str]:
        return {"http://" + h for h in self.hosts_permitidos()}

    def iniciar_reparo(self) -> None:
        def laco() -> None:
            while not self._parar.wait(INTERVALO_REPARO):
                try:
                    self.caixa.reconciliar()
                except Exception as e:  # noqa: BLE001
                    self.avisar(f"reparo da caixa falhou: {e}")
        self._reparo = threading.Thread(target=laco, name="reparo-da-caixa", daemon=True)
        self._reparo.start()

    def iniciar_emissor(self) -> bool:
        """Liga o canal A se ``MAESTRI_PIPE``/``MAESTRI_TERMINAL_ID`` e o executável estão aí; ``False`` se não."""
        if not leitores.disponibilidade_do_aviso(self.projeto, self.ambiente)["disponivel"]:
            return False
        self.emissor = _aviso.Emissor(self.caixa, self.projeto, self.ambiente)
        self.emissor.iniciar()
        return True

    def acordar_emissor(self) -> None:
        if self.emissor is not None:
            self.emissor.acordar()

    def parar(self) -> None:
        self._parar.set()
        if self.emissor is not None:
            self.emissor.parar()

    def avisar(self, mensagem: str) -> None:
        if not self.silencioso:
            print(mensagem, file=sys.stderr, flush=True)


# ----------------------------------------------------------------------------------------------
# O manipulador HTTP
# ----------------------------------------------------------------------------------------------


class Manipulador(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"
    server_version = "Torre/1"
    sys_version = ""
    timeout = 60

    @property
    def torre(self) -> Torre:
        return self.server.torre  # type: ignore[attr-defined]

    # -- respostas ---------------------------------------------------------------------------------

    def _enviar(self, status: int, corpo: bytes, tipo: str, cabecalhos: dict | None = None) -> None:
        self.send_response(status)
        self.send_header("Content-Type", tipo)
        self.send_header("Content-Length", str(len(corpo)))
        self.send_header("X-Content-Type-Options", "nosniff")
        for k, v in (cabecalhos or {}).items():
            self.send_header(k, v)
        if self.close_connection:
            self.send_header("Connection", "close")
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(corpo)

    def _json(self, status: int, obj) -> None:
        corpo = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self._enviar(status, corpo, "application/json; charset=utf-8", {"Cache-Control": "no-store"})

    def _erro(self, e: ErroApi) -> None:
        obj = {"erro": e.codigo, "mensagem": e.mensagem, "campo": e.campo}
        obj.update(e.extra)
        self._json(e.status, obj)

    def _arquivo(self, caminho: str) -> None:
        ext = os.path.splitext(caminho)[1].lower()
        tipo = MIME.get(ext)
        if tipo is None or not os.path.isfile(caminho):
            raise ErroApi(404, "nao-encontrado", "arquivo não encontrado")
        with open(caminho, "rb") as f:
            corpo = f.read()
        self._enviar(200, corpo, tipo, {"Cache-Control": "no-cache"})

    def log_message(self, formato, *args) -> None:  # noqa: D401 - assinatura da base
        if not self.torre.silencioso:
            super().log_message(formato, *args)

    # -- roteamento --------------------------------------------------------------------------------

    def _conferir_host(self) -> None:
        if self.headers.get("Host") not in self.torre.hosts_permitidos():
            raise ErroApi(403, "host-recusado", "este servidor só atende 127.0.0.1 e localhost")

    def do_GET(self) -> None:  # noqa: N802
        self._tratar("GET")

    def do_HEAD(self) -> None:  # noqa: N802
        self._tratar("HEAD")

    def do_POST(self) -> None:  # noqa: N802
        self._tratar("POST")

    def _tratar(self, metodo: str) -> None:
        try:
            self._conferir_host()
            caminho = urllib.parse.urlsplit(self.path).path
            if metodo in ("GET", "HEAD"):
                self._get(caminho)
            else:
                self._post(caminho)
        except ErroApi as e:
            self._erro(e)
        except (ConnectionError, BrokenPipeError):
            self.close_connection = True
        except Exception as e:  # noqa: BLE001 - nunca derrubar a thread sem resposta
            self.torre.avisar(f"erro interno em {metodo} {self.path}: {e!r}")
            try:
                self._erro(ErroApi(500, "erro-interno", f"erro interno: {e}"))
            except Exception:  # noqa: BLE001
                self.close_connection = True

    def _get(self, caminho: str) -> None:
        torre = self.torre
        if caminho == "/":
            return self._arquivo(os.path.join(PASTA_WEB, "index.html"))
        if caminho.startswith("/web/"):
            return self._estatico(PASTA_WEB, caminho[len("/web/"):])
        if caminho.startswith("/carta/"):
            return self._carta(caminho[len("/carta/"):])
        if caminho == "/api/estado":
            return self._json(200, torre.estado())
        if caminho == "/api/versao":
            return self._json(200, {"versao": leitores.versao_do_estado(torre.projeto)})
        if caminho == "/api/aviso":
            disp = leitores.disponibilidade_do_aviso(torre.projeto, torre.ambiente)
            fila = []
            for envio, reg in sorted(torre.caixa.fila.todos().items()):
                fila.append({"envio": envio, "arquivo": torre.caixa.nome_de(envio), **reg})
            return self._json(200, {**disp, "canal": "ask", "fila": fila})
        if caminho == "/api/lacos":
            return self._json(200, _lacos.resumo_dos_lacos(torre.projeto, torre.caixa.fila.todos()))
        m = re.fullmatch(r"/api/laco/([^/]+)", caminho)
        if m:
            return self._laco(urllib.parse.unquote(m.group(1)))
        m = re.fullmatch(r"/api/ticket/(\d+)", caminho)
        if m:
            return self._ticket(m.group(1))
        m = re.fullmatch(r"/api/caixa/([0-9a-f-]{36})", caminho)
        if m:
            return self._mensagem(m.group(1))
        if caminho.startswith("/api/"):
            raise ErroApi(404, "rota-inexistente", f"não existe a rota {caminho}")
        raise ErroApi(404, "nao-encontrado", "página não encontrada")

    def _laco(self, lid: str) -> None:
        if not re.fullmatch(r"[a-z0-9-]+", lid):
            raise ErroApi(404, "laco-inexistente", f"não há laço {lid!r} no registro")
        try:
            self._json(200, _lacos.detalhe_do_laco(self.torre.projeto, lid, self.torre.caixa.fila.todos()))
        except _lacos.Recusa as r:
            raise ErroApi(r.status, r.codigo, r.mensagem, r.campo, r.extra) from None

    def _componentes(self, relativo: str) -> list[str]:
        """Componentes seguros de um caminho relativo da URL; 404 em qualquer coisa estranha."""
        decodificado = urllib.parse.unquote(relativo)
        if "\\" in decodificado or "\x00" in decodificado:
            raise ErroApi(404, "nao-encontrado", "arquivo não encontrado")
        partes = decodificado.split("/")
        for p in partes:
            if not p or p.startswith(".") or ":" in p:
                raise ErroApi(404, "nao-encontrado", "arquivo não encontrado")
        return partes

    def _estatico(self, base: str, relativo: str) -> None:
        partes = self._componentes(relativo)
        base_real = os.path.realpath(base)
        alvo = os.path.realpath(os.path.join(base_real, *partes))
        if not leitores.dentro_de(alvo, base_real):
            raise ErroApi(404, "nao-encontrado", "arquivo não encontrado")
        self._arquivo(alvo)

    def _carta(self, resto: str) -> None:
        torre = self.torre
        if "/" not in resto:
            raise ErroApi(404, "nao-encontrado", "carta não encontrada")
        cid, relativo = resto.split("/", 1)
        cid = urllib.parse.unquote(cid)
        estado_cartas = leitores.ler_cartas(torre.projeto, [], leitores.Problemas())
        carta = next((c for c in estado_cartas if c["id"] == cid), None)
        if carta is None:
            raise ErroApi(404, "nao-encontrado", "carta não encontrada")
        pastas = leitores.pasta_real_da_carta(torre.projeto, carta)
        if pastas is None:
            raise ErroApi(404, "nao-encontrado", "carta sem arquivo ou pasta")
        pasta_real, arquivo_real = pastas
        if relativo == "":
            alvo = os.path.realpath(arquivo_real)
            partes = [os.path.basename(alvo)]
        else:
            partes = self._componentes(relativo)
            alvo = os.path.realpath(os.path.join(pasta_real, *partes))
        self._conferir_regras_da_carta(alvo, pasta_real)
        self._arquivo(alvo)

    def _conferir_regras_da_carta(self, alvo: str, pasta_real: str) -> None:
        """As três regras da §3.2; qualquer uma falhando é 404."""
        projeto = self.torre.projeto
        nao = ErroApi(404, "nao-encontrado", "arquivo não encontrado")
        if not leitores.dentro_de(alvo, pasta_real):                       # 1. dentro da pasta
            raise nao
        if os.path.splitext(alvo)[1].lower() not in EXTENSOES_CARTA:       # 2. extensão permitida
            raise nao
        if leitores.dentro_de(alvo, projeto.pasta_portal):                 # 3. fora do portal...
            raise nao
        if alvo in projeto.arquivos_reservados():                          # ...e dos arquivos do projeto.json
            raise nao
        if leitores.dentro_de(alvo, projeto.tickets):                      # ...e da pasta de tickets
            raise nao
        relativo = os.path.relpath(alvo, pasta_real)
        if any(p.startswith(".") for p in relativo.replace("\\", "/").split("/")):  # ...e sem componente com ponto
            raise nao
        # ...e das pastas dos laços (§4.4: as fontes de um laço não são servidas como arquivo): de dentro de um laço
        # só serve a carta cuja pasta é uma subpasta só de publicação (um painel, sem fonte declarada dentro)
        if not _lacos.carta_pode_servir(projeto, pasta_real, alvo):
            raise nao
        if not os.path.isfile(alvo):
            raise nao

    def _ticket(self, numero: str) -> None:
        pasta = self.torre.projeto.tickets
        if not pasta:
            raise ErroApi(404, "nao-encontrado", "pasta de tickets fora da raiz do projeto")
        try:
            nomes = sorted(os.listdir(pasta))
        except OSError:
            raise ErroApi(404, "nao-encontrado", "pasta de tickets não encontrada") from None
        nome = next((n for n in nomes if re.fullmatch(re.escape(numero) + r"-[A-Za-z0-9._-]+\.md", n)), None)
        if nome is None:
            raise ErroApi(404, "nao-encontrado", f"não existe ticket {numero}")
        caminho = os.path.join(pasta, nome)
        if not os.path.isfile(caminho) or not leitores.arquivo_confinado(caminho, os.path.realpath(pasta)):
            raise ErroApi(404, "nao-encontrado", f"não existe ticket {numero}")
        try:
            markdown = leitores.ler_texto(caminho)
        except (OSError, ValueError) as e:
            raise ErroApi(422, "arquivo-ilegivel",
                          f"o ticket {numero} não pôde ser lido: {leitores.motivo_de_leitura(e)}") from None
        self._json(200, {"numero": numero, "markdown": markdown})

    def _mensagem(self, envio: str) -> None:
        caixa = self.torre.caixa
        nome = caixa.nome_de(envio)
        if nome is None:
            raise ErroApi(404, "envio-inexistente", "não há mensagem com este envio")
        try:
            dados = caixa.dados_de(nome)
        except (OSError, ValueError) as e:
            raise ErroApi(422, "mensagem-ilegivel",
                          f"a mensagem não pôde ser lida: {leitores.motivo_de_leitura(e)}") from None
        dados["arquivo"] = nome
        dados["estado"] = caixa.estado_md(nome)
        dados["aviso"] = caixa.fila.estado(envio)
        self._json(200, dados)

    # -- POST ---------------------------------------------------------------------------------------

    def _ler_corpo_json(self) -> dict:
        torre = self.torre
        if self.headers.get("X-Torre") != "1":
            self.close_connection = True
            raise ErroApi(403, "cabecalho-ausente", "o pedido precisa do cabeçalho X-Torre: 1")
        if self.headers.get("Origin") not in torre.origens_permitidas():
            self.close_connection = True
            raise ErroApi(403, "origem-recusada", "Origin precisa ser o próprio portal")
        tipo = (self.headers.get("Content-Type") or "").split(";")[0].strip().lower()
        if tipo != "application/json":
            self.close_connection = True
            raise ErroApi(403, "tipo-de-conteudo", "o corpo precisa ser application/json")
        try:
            tamanho = int(self.headers.get("Content-Length") or "")
        except ValueError:
            self.close_connection = True
            raise ErroApi(411, "tamanho-ausente", "o pedido precisa de Content-Length") from None
        if tamanho > TAMANHO_MAXIMO:
            self.close_connection = True
            raise ErroApi(413, "corpo-grande", f"o corpo passa de {TAMANHO_MAXIMO // 1024} KiB")
        bruto = self.rfile.read(tamanho)
        try:
            corpo = json.loads(bruto.decode("utf-8"))
        except (UnicodeDecodeError, ValueError) as e:
            raise ErroApi(400, "json-invalido", f"o corpo não é JSON válido: {e}") from None
        if not isinstance(corpo, dict):
            raise ErroApi(400, "json-invalido", "o corpo precisa ser um objeto JSON")
        return corpo

    def _post(self, caminho: str) -> None:
        if caminho == "/api/caixa":
            return self._post_caixa()
        if caminho == "/api/aviso/tentar":
            return self._post_tentar()
        if caminho.startswith("/api/"):
            raise ErroApi(404, "rota-inexistente", f"não existe a rota {caminho}")
        raise ErroApi(405, "metodo-nao-permitido", "esta rota não aceita POST")

    def _post_caixa(self) -> None:
        torre = self.torre
        corpo = self._ler_corpo_json()
        envio = corpo.get("envio")
        if not _caixa.envio_valido(envio):
            raise ErroApi(400, "envio-invalido", "envio precisa ser um UUID", "envio")
        with torre.lock:
            torre.caixa.reconciliar()
            # idempotência vem antes de qualquer validação do conteúdo
            nome = torre.caixa.nome_de(envio)
            if nome is not None:
                if torre.caixa.hash_de(envio) == leitores.hash_corpo(corpo):
                    return self._json(200, {"envio": envio, "arquivo": nome, "repetido": True})
                raise ErroApi(409, "envio-conflito", "este envio já foi gravado com outro corpo", "envio")
            if corpo.get("tipo") == "alteracao-laco":
                # §4.5: validado contra o laco.json atual; o navegador só manda ids e valores tipados
                try:
                    dados = _lacos.validar_alteracao(corpo, torre.projeto, torre.caixa, torre.caixa.fila.todos())
                except _lacos.Recusa as r:
                    raise ErroApi(r.status, r.codigo, r.mensagem, r.campo, r.extra) from None
            else:
                estado = torre.estado()
                dados = validar_post(corpo, estado, torre.caixa)
            try:
                nome = torre.caixa.gravar(dados)
            except _caixa.GravacaoParcial as e:
                raise ErroApi(500, "gravacao-parcial",
                              "a mensagem foi salva, mas a vista ou o aviso ficaram para o reparo",
                              extra={"envio": envio, "arquivo": e.nome}) from None
        torre.acordar_emissor()
        self._json(200, {"envio": envio, "arquivo": nome, "repetido": False})

    def _post_tentar(self) -> None:
        corpo = self._ler_corpo_json()
        envio = corpo.get("envio")
        if not _caixa.envio_valido(envio):
            raise ErroApi(400, "envio-invalido", "envio precisa ser um UUID", "envio")
        reg = self.torre.caixa.fila.tentar_de_novo(envio)
        if reg is None:
            raise ErroApi(404, "aviso-inexistente", "não há aviso para este envio")
        self.torre.acordar_emissor()
        self._json(200, {"envio": envio, "arquivo": self.torre.caixa.nome_de(envio), **reg})


# ----------------------------------------------------------------------------------------------
# Servidor
# ----------------------------------------------------------------------------------------------


class Servidor(ThreadingHTTPServer):
    allow_reuse_address = False  # porta ocupada → recusa subir (também no Windows)
    daemon_threads = True
    torre: Torre


def criar_servidor(caminho_projeto: str, porta: int | None = None, ambiente=None,
                   silencioso: bool = False) -> Servidor:
    """Monta a torre e abre a porta (``porta=0`` escolhe uma livre, para testes).

    Levanta ``FileNotFoundError``/``ValueError`` para ``projeto.json`` ausente ou inválido e ``OSError``
    para porta ocupada. A reconciliação da caixa acontece antes de aceitar pedidos.
    """
    torre = Torre(caminho_projeto, ambiente=ambiente, silencioso=silencioso)
    servidor = Servidor(("127.0.0.1", torre.projeto.porta if porta is None else porta), Manipulador)
    servidor.torre = torre
    torre.porta_real = servidor.server_address[1]
    torre.iniciar_reparo()
    torre.iniciar_emissor()
    return servidor


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    for fluxo in (sys.stdout, sys.stderr):  # terminal do Windows pode não estar em UTF-8
        if hasattr(fluxo, "reconfigure"):
            fluxo.reconfigure(errors="replace")
    abrir = "--abrir" in argv
    argv = [a for a in argv if a != "--abrir"]
    if len(argv) != 1:
        print("uso: python nucleo/torre.py <caminho do projeto.json> [--abrir]", file=sys.stderr)
        return 2
    caminho = argv[0]
    try:
        servidor = criar_servidor(caminho)
    except FileNotFoundError:
        print(f"não subiu: projeto.json não encontrado em {caminho}", file=sys.stderr)
        return 1
    except (ValueError, KeyError) as e:
        motivo = str(e)
        if not motivo.startswith(("projeto.json", "caixa")):
            motivo = f"projeto.json inválido: {motivo}"
        print(f"não subiu: {motivo}", file=sys.stderr)
        return 1
    except OSError as e:
        print(f"não subiu: não deu para abrir a porta em 127.0.0.1 ({e})", file=sys.stderr)
        return 1
    torre = servidor.torre
    disp = leitores.disponibilidade_do_aviso(torre.projeto, torre.ambiente)
    print(f"Torre no ar: http://127.0.0.1:{torre.porta_real}/  (projeto: {torre.projeto.nome})", flush=True)
    if disp["disponivel"] and torre.emissor is not None:
        print(f"aviso ao agente: disponível (modo canvas: emissor ligado, {torre.projeto.aviso.get('executavel')!r} ask "
              f"{torre.projeto.aviso.get('agente')!r}; vigia opcional: python nucleo/aviso.py --vigiar <pasta do portal>)",
              flush=True)
    else:
        print(f"aviso ao agente: indisponível ({disp['motivo']}); modo fora do canvas: a página mostra a faixa "
              "\"diga 'respondi'\" e os avisos ficam pendentes para o vigia (python nucleo/aviso.py --vigiar)", flush=True)
    if abrir:
        import webbrowser  # noqa: PLC0415 - só quando pedido
        try:
            webbrowser.open(f"http://127.0.0.1:{torre.porta_real}/")
        except Exception as e:  # noqa: BLE001 - abrir o navegador é cortesia, não requisito
            print(f"não deu para abrir o navegador: {e}", file=sys.stderr, flush=True)
    if torre.caixa.problemas:
        for c, m in torre.caixa.problemas:
            print(f"caixa: {torre.projeto.relativo(c)}: {m}", flush=True)
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        torre.parar()
        servidor.server_close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
