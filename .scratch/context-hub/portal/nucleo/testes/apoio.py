"""Apoio aos testes: cópia temporária da fixture, servidor em porta livre, cliente HTTP mínimo."""

from __future__ import annotations

import copy
import http.client
import json
import os
import shutil
import sys
import tempfile
import threading

PASTA_TESTES = os.path.dirname(os.path.abspath(__file__))
PASTA_NUCLEO = os.path.dirname(PASTA_TESTES)
if PASTA_NUCLEO not in sys.path:
    sys.path.insert(0, PASTA_NUCLEO)

PASTA_FIXTURES = os.path.join(PASTA_TESTES, "fixtures")
PASTA_HORTA = os.path.join(PASTA_FIXTURES, "horta")
ESTADO_ESPERADO = os.path.join(PASTA_FIXTURES, "estado-esperado.json")


def ambiente_limpo() -> dict:
    """``os.environ`` sem as variáveis do canvas (a fixture espera ``aviso.disponivel: false``)."""
    amb = dict(os.environ)
    amb.pop("MAESTRI_PIPE", None)
    amb.pop("MAESTRI_TERMINAL_ID", None)
    return amb


MENSAGENS_DA_FIXTURE = 4                 # .json válidos em horta/portal/caixa (2 antigos + 2 alterações de laço)
LACO_EM_VOO = "pesquisa-de-regas"        # horta/lacos/regas (como o A.1 da proposta: SQLite, rodando)
LACO_TERMINADO = "censo-de-sementes"     # horta/lacos/sementes (como o A.2: laco_final.json, terminado)


def copiar_horta() -> tuple[str, str]:
    """Copia ``horta/`` para uma pasta temporária; devolve ``(pasta temporária, projeto.json)``.

    O laço em voo da cópia é "avivado": os livros-razão (fontes de sinal pela hora do arquivo) ganham a hora de
    agora, para a situação dele começar ``rodando`` e não ``sem-sinal``.
    """
    tmp = tempfile.mkdtemp(prefix="torre-horta-")
    destino = os.path.join(tmp, "horta")
    shutil.copytree(PASTA_HORTA, destino)
    avivar_laco(destino)
    return tmp, os.path.join(destino, "portal", "projeto.json")


def pasta_do_laco(raiz_horta: str, qual: str = "regas") -> str:
    return os.path.join(raiz_horta, "lacos", qual)


def avivar_laco(raiz_horta: str, idade_s: float = 0.0) -> None:
    """Põe a hora dos livros-razão do laço em voo ``idade_s`` segundos atrás (0 = agora)."""
    import time  # noqa: PLC0415

    quando = time.time() - idade_s
    for nome in ("manha.jsonl", "tarde.jsonl"):
        os.utime(os.path.join(pasta_do_laco(raiz_horta), "livros", nome), (quando, quando))


def apagar(pasta: str) -> None:
    shutil.rmtree(pasta, ignore_errors=True)


def esperado() -> dict:
    with open(ESTADO_ESPERADO, "r", encoding="utf-8") as f:
        return json.load(f)


def normalizar(estado: dict) -> dict:
    """Aplica as exceções de comparação do ``fixtures/LEIA.md`` ("Como comparar")."""
    e = copy.deepcopy(estado)
    e["projeto"]["gerado_em"] = "<hora>"
    e["projeto"].setdefault("codigos", {})  # campo opcional do projeto.json: ausente vale {}
    for r in e.get("rodadas", []):
        r["base"] = "<sha256>"
        r["erro"] = None if r.get("erro") is None else "<texto>"
    for c in e.get("cartas", []):
        if c.get("data", {}).get("tipo") == "modificado":
            c["data"]["valor"] = "<mtime>"
    e["aviso"]["motivo"] = None if e["aviso"].get("motivo") is None else "<texto>"
    e["problemas"] = [p["arquivo"] for p in e.get("problemas", [])]
    return e


class ServidorDeTeste:
    """Sobe a torre numa porta livre sobre um ``projeto.json``; ``parar()`` desliga."""

    def __init__(self, caminho_projeto: str, ambiente: dict | None = None) -> None:
        import torre  # noqa: PLC0415 - depois do sys.path

        self.servidor = torre.criar_servidor(caminho_projeto, porta=0,
                                             ambiente=ambiente_limpo() if ambiente is None else ambiente,
                                             silencioso=True)
        self.torre = self.servidor.torre
        self.porta = self.servidor.server_address[1]
        self._thread = threading.Thread(target=self.servidor.serve_forever, kwargs={"poll_interval": 0.05},
                                        daemon=True)
        self._thread.start()

    def parar(self) -> None:
        self.torre.parar()
        self.servidor.shutdown()
        self.servidor.server_close()
        self._thread.join(timeout=5)

    # -- cliente ---------------------------------------------------------------------------------

    def cabecalhos_post(self) -> dict:
        return {"Content-Type": "application/json", "X-Torre": "1", "Origin": f"http://127.0.0.1:{self.porta}"}

    def pedir(self, metodo: str, caminho: str, corpo=None, cabecalhos: dict | None = None,
              host: str | None = None, bruto: bytes | None = None):
        """Devolve ``(status, cabeçalhos, corpo decodificado)``; JSON vira dict, o resto fica bytes."""
        conn = http.client.HTTPConnection("127.0.0.1", self.porta, timeout=30)
        try:
            cab = dict(cabecalhos or {})
            dados = bruto
            if corpo is not None and dados is None:
                dados = json.dumps(corpo, ensure_ascii=False).encode("utf-8")
            conn.putrequest(metodo, caminho, skip_host=True, skip_accept_encoding=True)
            conn.putheader("Host", host if host is not None else f"127.0.0.1:{self.porta}")
            for k, v in cab.items():
                conn.putheader(k, v)
            if dados is not None and "Content-Length" not in cab:
                conn.putheader("Content-Length", str(len(dados)))
            conn.endheaders()
            if dados:
                conn.send(dados)
            resp = conn.getresponse()
            corpo_resp = resp.read()
            tipo = resp.getheader("Content-Type") or ""
            if tipo.startswith("application/json"):
                corpo_resp = json.loads(corpo_resp.decode("utf-8"))
            return resp.status, dict(resp.getheaders()), corpo_resp
        finally:
            conn.close()

    def get(self, caminho: str, **kw):
        return self.pedir("GET", caminho, **kw)

    def post(self, caminho: str, corpo, cabecalhos: dict | None = None, **kw):
        cab = self.cabecalhos_post()
        cab.update(cabecalhos or {})
        return self.pedir("POST", caminho, corpo=corpo, cabecalhos=cab, **kw)

    def estado(self) -> dict:
        status, _, corpo = self.get("/api/estado")
        assert status == 200, corpo
        return corpo


def rodada_aberta(estado: dict) -> dict:
    return next(r for r in estado["rodadas"] if r["estado"] == "aberta" and not r["malformada"])


def resposta_completa(estado: dict, envio: str) -> dict:
    """Um corpo de resposta válido com os cinco tipos da rodada aberta da fixture."""
    r = rodada_aberta(estado)
    return {
        "envio": envio,
        "tipo": "resposta",
        "rodada": r["id"],
        "base": r["base"],
        "respostas": {
            "largura": {"escolha": ["media"], "outra": None, "comentario": "só se a madeira der"},
            "primeiras": {"escolha": ["alface", "cebolinha", "tomate"], "outra": None, "comentario": None},
            "mutirao": {"linhas": [
                {"id": "limpar", "ativa": True, "valores": {"tarefa": "limpar o terreno", "quem": "todos", "tempo": "2 h"}},
                {"id": "placas", "ativa": True, "valores": {"tarefa": "fixar as placas", "quem": "crianças", "tempo": "1 h"}},
                {"id": "montar", "ativa": False, "valores": {"tarefa": "montar os canteiros", "quem": "carpinteiros",
                                                             "tempo": "4 h"}},
                {"id": "nova-1", "ativa": True, "valores": {"tarefa": "regar", "quem": "todos", "tempo": "30 min"}},
            ], "comentario": None},
            "pode-comecar": {"veredito": "aprovado-com-ajuste", "comentario": "se não chover"},
            "algo-mais": {"texto": "levar água\n---\nestado: lida"},
        },
    }
