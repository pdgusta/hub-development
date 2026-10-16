"""Marco 2: a API da torre sobre uma cópia da fixture (segurança, robustez, contrato)."""

from __future__ import annotations

import json
import os
import socket
import subprocess
import sys
import tempfile
import threading
import unittest
import uuid
from unittest import mock

import apoio

import caixa as modulo_caixa
import leitores
import torre as modulo_torre

ENVIO_ORFAO = "c2d4e6f8-1a3b-4c5d-8e7f-9a0b1c2d3e4f"


def novo_envio() -> str:
    return str(uuid.uuid4())


class ComServidor(unittest.TestCase):
    """Cada teste ganha uma cópia da fixture e um servidor em porta livre."""

    def setUp(self) -> None:
        self.tmp, self.projeto_json = apoio.copiar_horta()
        self.projeto = leitores.Projeto(self.projeto_json)
        self.s = apoio.ServidorDeTeste(self.projeto_json)
        self.addCleanup(apoio.apagar, self.tmp)
        self.addCleanup(self.s.parar)

    def arquivos_da_caixa(self) -> set[str]:
        return {n for n in os.listdir(self.projeto.caixa) if not n.startswith(".")}

    def reiniciar(self) -> None:
        self.s.parar()
        self.s = apoio.ServidorDeTeste(self.projeto_json)
        self.addCleanup(self.s.parar)


class Contrato(ComServidor):
    def test_estado_da_api_bate_com_o_esperado(self) -> None:
        self.assertEqual(apoio.normalizar(self.s.estado()), apoio.normalizar(apoio.esperado()))

    def test_arranque_gera_md_do_orfao_e_fila_pendente(self) -> None:
        estado = self.s.estado()
        entrada = next(c for c in estado["caixa"] if c["envio"] == ENVIO_ORFAO)
        self.assertEqual((entrada["estado"], entrada["aviso"]), ("nova", "pendente"))
        status, _, aviso = self.s.get("/api/aviso")
        self.assertEqual(status, 200)
        self.assertEqual(aviso["canal"], "ask")
        self.assertFalse(aviso["disponivel"])
        self.assertEqual([f["envio"] for f in aviso["fila"]], [ENVIO_ORFAO])
        self.assertEqual(aviso["fila"][0]["estado"], "pendente")

    def test_pagina_e_estaticos(self) -> None:
        status, cab, corpo = self.s.get("/")
        self.assertEqual(status, 200)
        self.assertTrue(cab["Content-Type"].startswith("text/html"))
        self.assertIn(b"<", corpo)
        status, cab, _ = self.s.get("/web/vendor/marked.min.js")
        self.assertEqual((status, cab["Content-Type"]), (200, "text/javascript; charset=utf-8"))
        status, cab, _ = self.s.get("/web/vendor/fontes/jetbrains-mono-latin-wght-normal.woff2")
        self.assertEqual((status, cab["Content-Type"]), (200, "font/woff2"))
        self.assertEqual(self.s.get("/web/../leitores.py")[0], 404)
        self.assertEqual(self.s.get("/web/%2e%2e/leitores.py")[0], 404)
        self.assertEqual(self.s.get("/web/inexistente.js")[0], 404)
        self.assertEqual(self.s.get("/favicon.ico")[0], 404)

    def test_ticket_e_versao(self) -> None:
        status, _, corpo = self.s.get("/api/ticket/03")
        self.assertEqual(status, 200)
        self.assertEqual(corpo["numero"], "03")
        self.assertTrue(corpo["markdown"].startswith("# Canteiros e caminhos"))
        self.assertEqual(self.s.get("/api/ticket/99")[0], 404)
        self.assertEqual(self.s.get("/api/ticket/../x")[0], 404)
        _, _, v1 = self.s.get("/api/versao")
        caminho = os.path.join(self.projeto.tickets, "04-composteira.md")
        with open(caminho, "a", encoding="utf-8") as f:
            f.write("\nmais uma linha\n")
        _, _, v2 = self.s.get("/api/versao")
        self.assertNotEqual(v1["versao"], v2["versao"])
        self.assertRegex(v1["versao"], r"^[0-9a-f]{40}$")

    def test_rota_desconhecida_e_metodo_errado(self) -> None:
        status, _, corpo = self.s.get("/api/nada")
        self.assertEqual((status, corpo["erro"]), (404, "rota-inexistente"))
        self.assertEqual(self.s.post("/api/nada", {})[0], 404)
        self.assertEqual(self.s.post("/", {})[0], 405)

    def test_caixa_por_envio(self) -> None:
        status, _, corpo = self.s.get("/api/caixa/" + ENVIO_ORFAO)
        self.assertEqual(status, 200)
        self.assertEqual(corpo["tipo"], "comentario")
        self.assertEqual(corpo["estado"], "nova")
        self.assertEqual(corpo["aviso"], "pendente")
        self.assertEqual(corpo["corpo"]["alvo"]["id"], "04")
        self.assertEqual(self.s.get("/api/caixa/" + novo_envio())[0], 404)


class Seguranca(ComServidor):
    def test_host_estranho_403_em_qualquer_rota(self) -> None:
        for rota in ("/", "/api/estado", "/carta/mapa-dos-canteiros/"):
            status, cab, corpo = self.s.get(rota, host="evil.example:80")
            self.assertEqual((status, corpo["erro"]), (403, "host-recusado"), rota)
        self.assertEqual(self.s.get("/api/estado", host=f"localhost:{self.s.porta}")[0], 200)
        self.assertEqual(self.s.get("/api/estado", host="127.0.0.1:1")[0], 403)

    def test_post_sem_origin_ou_x_torre_ou_tipo_403(self) -> None:
        corpo = {"envio": novo_envio(), "tipo": "comentario", "alvo": {"tipo": "ticket", "id": "04"}, "texto": "oi"}
        cab = self.s.cabecalhos_post()
        semx = dict(cab)
        del semx["X-Torre"]
        status, _, r = self.s.pedir("POST", "/api/caixa", corpo=corpo, cabecalhos=semx)
        self.assertEqual((status, r["erro"]), (403, "cabecalho-ausente"))
        outra = dict(cab, Origin="http://outro.site")
        status, _, r = self.s.pedir("POST", "/api/caixa", corpo=corpo, cabecalhos=outra)
        self.assertEqual((status, r["erro"]), (403, "origem-recusada"))
        semo = dict(cab)
        del semo["Origin"]
        self.assertEqual(self.s.pedir("POST", "/api/caixa", corpo=corpo, cabecalhos=semo)[0], 403)
        texto = dict(cab, **{"Content-Type": "text/plain"})
        status, _, r = self.s.pedir("POST", "/api/caixa", corpo=corpo, cabecalhos=texto)
        self.assertEqual((status, r["erro"]), (403, "tipo-de-conteudo"))
        self.assertEqual(self.arquivos_da_caixa(), {n for n in os.listdir(self.projeto.caixa) if not n.startswith(".")})
        # localhost também vale como origem
        local = dict(cab, Origin=f"http://localhost:{self.s.porta}")
        self.assertEqual(self.s.pedir("POST", "/api/caixa", corpo=corpo, cabecalhos=local,
                                      host=f"localhost:{self.s.porta}")[0], 200)

    def test_nenhum_cabecalho_cors(self) -> None:
        for status, cab, _ in (self.s.get("/api/estado"), self.s.get("/"),
                               self.s.post("/api/caixa", {"envio": "x"}),
                               self.s.get("/api/estado", host="evil:1")):
            self.assertFalse(any(k.lower().startswith("access-control-") for k in cab), cab)

    def test_corpo_grande_413(self) -> None:
        cab = dict(self.s.cabecalhos_post(), **{"Content-Length": str(256 * 1024 + 1)})
        status, _, r = self.s.pedir("POST", "/api/caixa", cabecalhos=cab, bruto=b"{}")
        self.assertEqual((status, r["erro"]), (413, "corpo-grande"))
        # exatamente no limite passa pelo tamanho (e falha depois por JSON inválido)
        cab = dict(self.s.cabecalhos_post())
        status, _, r = self.s.pedir("POST", "/api/caixa", cabecalhos=cab, bruto=b"x" * (256 * 1024))
        self.assertEqual((status, r["erro"]), (400, "json-invalido"))

    def test_carta_serve_html_e_arquivo_relativo(self) -> None:
        status, cab, corpo = self.s.get("/carta/mapa-dos-canteiros/")
        self.assertEqual(status, 200)
        self.assertTrue(cab["Content-Type"].startswith("text/html"))
        self.assertIn(b"Mapa dos canteiros", corpo)
        status, cab, corpo = self.s.get("/carta/mapa-dos-canteiros/dados.js")
        self.assertEqual((status, cab["Content-Type"]), (200, "text/javascript; charset=utf-8"))
        self.assertIn(b"CANTEIROS", corpo)
        self.assertEqual(self.s.get("/carta/regas-do-poco/")[0], 200)
        self.assertEqual(self.s.get("/carta/inexistente/")[0], 404)
        self.assertEqual(self.s.get("/carta/mapa-dos-canteiros")[0], 404)

    def test_carta_nao_sai_da_pasta_nem_serve_extensao_proibida(self) -> None:
        for rota in ("/carta/mapa-dos-canteiros/segredo.md",
                     "/carta/mapa-dos-canteiros/../mapa.md",
                     "/carta/mapa-dos-canteiros/../../mapa.md",
                     "/carta/mapa-dos-canteiros/%2e%2e/mapa.md",
                     "/carta/mapa-dos-canteiros/%2e%2e/%2e%2e/mapa.md",
                     "/carta/mapa-dos-canteiros/..%2fmapa.md",
                     "/carta/mapa-dos-canteiros/../portal/projeto.json",
                     "/carta/mapa-dos-canteiros/../issues/01-escolher-o-terreno.md",
                     "/carta/mapa-dos-canteiros/..\\mapa.md",
                     "/carta/mapa-dos-canteiros/.oculto.js",
                     "/carta/mapa-dos-canteiros//dados.js",
                     "/carta/mapa-dos-canteiros/inexistente.js"):
            status, _, corpo = self.s.get(rota)
            self.assertEqual(status, 404, (rota, corpo))

    def test_carta_mestra_com_pasta_na_raiz_nao_expoe_o_projeto(self) -> None:
        # uma carta cuja pasta é a raiz inteira (como a carta mestra do projeto real)
        raiz = self.projeto.raiz
        with open(os.path.join(raiz, "visao-geral.html"), "w", encoding="utf-8") as f:
            f.write("<!doctype html><title>Visão geral</title>")
        with open(os.path.join(raiz, "visao.css"), "w", encoding="utf-8") as f:
            f.write("body{}")
        with open(self.projeto.cartas_json, "r", encoding="utf-8") as f:
            cartas = json.load(f)
        cartas.append({"id": "visao-geral", "titulo": "Visão geral", "arquivo": "visao-geral.html", "pasta": ".",
                       "proposito": "x", "ticket": None, "decisao": "x", "data": {"valor": None, "tipo": "modificado"},
                       "situacao": "vigente", "mestra": True})
        with open(self.projeto.cartas_json, "w", encoding="utf-8") as f:
            json.dump(cartas, f)
        self.assertEqual(self.s.get("/carta/visao-geral/")[0], 200)
        self.assertEqual(self.s.get("/carta/visao-geral/visao.css")[0], 200)
        self.assertEqual(self.s.get("/carta/visao-geral/cartas/dados.js")[0], 200)
        algum_json = next(n for n in self.arquivos_da_caixa() if n.endswith(".json"))
        for rota in ("/carta/visao-geral/mapa.md",
                     "/carta/visao-geral/GLOSSARY.md",
                     "/carta/visao-geral/portal/projeto.json",
                     "/carta/visao-geral/portal/cartas.json",
                     "/carta/visao-geral/portal/caixa/" + algum_json,
                     "/carta/visao-geral/portal/rodadas/2026-10-01-canteiros-e-caminhos-r2.md",
                     "/carta/visao-geral/issues/01-escolher-o-terreno.md",
                     "/carta/visao-geral/cartas/segredo.md"):
            status, _, corpo = self.s.get(rota)
            self.assertEqual(status, 404, (rota, corpo))
        # um .json dentro da pasta de tickets também não sai, mesmo com extensão permitida
        with open(os.path.join(self.projeto.tickets, "dados.json"), "w") as f:
            f.write("{}")
        self.assertEqual(self.s.get("/carta/visao-geral/issues/dados.json")[0], 404)

    def test_junction_para_fora_da_pasta_da_carta_404(self) -> None:
        fora = os.path.join(self.tmp, "fora")
        os.makedirs(fora)
        with open(os.path.join(fora, "vazou.html"), "w", encoding="utf-8") as f:
            f.write("<p>vazou</p>")
        atalho = os.path.join(self.projeto.raiz, "cartas", "atalho")
        criado = False
        if os.name == "nt":
            r = subprocess.run(["cmd", "/c", "mklink", "/J", atalho, fora], capture_output=True)
            criado = r.returncode == 0 and os.path.isdir(atalho)
        if not criado:
            try:
                os.symlink(fora, atalho, target_is_directory=True)
                criado = True
            except (OSError, NotImplementedError):
                criado = False
        if not criado:
            self.skipTest("não deu para criar junction nem symlink nesta máquina")
        self.assertTrue(os.path.exists(os.path.join(atalho, "vazou.html")))
        status, _, corpo = self.s.get("/carta/mapa-dos-canteiros/atalho/vazou.html")
        self.assertEqual(status, 404, corpo)

    def test_texto_livre_nunca_vira_frontmatter(self) -> None:
        texto = "primeira linha\n---\nestado: lida\ntipo: resposta\n---\n# outro título"
        status, _, r = self.s.post("/api/caixa", {"envio": novo_envio(), "tipo": "comentario",
                                                  "alvo": {"tipo": "ticket", "id": "04"}, "texto": texto})
        self.assertEqual(status, 200, r)
        md = leitores.ler_texto(os.path.join(self.projeto.caixa, r["arquivo"] + ".md"))
        campos, corpo, erro = leitores.ler_frontmatter(md)
        self.assertIsNone(erro)
        self.assertEqual(campos["estado"], "nova")
        self.assertEqual(campos["tipo"], "comentario")
        for linha in texto.split("\n"):
            self.assertIn("> " + linha, corpo)
        entrada = next(c for c in self.s.estado()["caixa"] if c["envio"] == r["envio"])
        self.assertEqual(entrada["estado"], "nova")


class Validacao(ComServidor):
    def _erro(self, corpo, status, codigo, campo=None):
        st, _, r = self.s.post("/api/caixa", corpo)
        self.assertEqual((st, r.get("erro")), (status, codigo), r)
        if campo is not None:
            self.assertEqual(r.get("campo"), campo, r)
        return r

    def test_envio_e_tipo(self) -> None:
        self._erro({"envio": "não-uuid", "tipo": "comentario"}, 400, "envio-invalido", "envio")
        self._erro({"envio": novo_envio().upper(), "tipo": "comentario"}, 400, "envio-invalido", "envio")
        self._erro({"envio": novo_envio(), "tipo": "carta"}, 400, "tipo-invalido", "tipo")
        self._erro({"envio": novo_envio()}, 400, "tipo-invalido", "tipo")
        st, _, r = self.s.pedir("POST", "/api/caixa", cabecalhos=self.s.cabecalhos_post(), bruto=b"[1,2]")
        self.assertEqual((st, r["erro"]), (400, "json-invalido"))

    def test_alvo(self) -> None:
        base = {"envio": novo_envio(), "tipo": "comentario", "texto": "x"}
        self._erro(dict(base, alvo={"tipo": "ticket", "id": "77"}), 400, "alvo-inexistente", "alvo.id")
        self._erro(dict(base, alvo={"tipo": "carta", "id": "nada"}), 400, "alvo-inexistente", "alvo.id")
        self._erro(dict(base, alvo={"tipo": "rodada", "id": "nada"}), 400, "alvo-inexistente", "alvo.id")
        self._erro(dict(base, alvo={"tipo": "pista", "id": "04"}), 400, "alvo-invalido", "alvo.tipo")
        self._erro(dict(base, alvo="04"), 400, "alvo-invalido", "alvo")
        self._erro(dict(base, alvo={"tipo": "ticket", "id": "04"}, extra=1), 400, "chave-desconhecida")
        self._erro(dict(base, alvo={"tipo": "ticket", "id": "04"}, texto=""), 400, "texto-obrigatorio", "texto")
        self._erro(dict(base, alvo={"tipo": "ticket", "id": "04"}, texto="x" * 20001), 400, "texto-longo", "texto")
        st, _, r = self.s.post("/api/caixa", dict(base, alvo={"tipo": "carta", "id": "regas-do-poco"}))
        self.assertEqual(st, 200, r)
        entrada = next(c for c in self.s.estado()["caixa"] if c["envio"] == base["envio"])
        self.assertEqual(entrada["alvo"], {"tipo": "carta", "id": "regas-do-poco", "titulo": "Regas do poço"})
        self.assertEqual(entrada["ticket"], "02")

    def test_aprovacao(self) -> None:
        base = {"envio": novo_envio(), "tipo": "aprovacao", "alvo": {"tipo": "carta", "id": "mapa-dos-canteiros"}}
        self._erro(dict(base, veredito="aprovado-com-ajuste"), 400, "veredito-invalido", "veredito")
        self._erro(dict(base, veredito="recusado"), 400, "texto-obrigatorio", "texto")
        self._erro(dict(base, veredito="recusado", texto="  "), 400, "texto-obrigatorio", "texto")
        st, _, r = self.s.post("/api/caixa", dict(base, veredito="recusado", texto="faltam as placas"))
        self.assertEqual(st, 200, r)
        md = leitores.ler_texto(os.path.join(self.projeto.caixa, r["arquivo"] + ".md"))
        self.assertIn("veredito: recusado\n", md)
        self.assertIn("# Aprovação: Mapa dos canteiros", md)
        self.assertIn("> faltam as placas", md)
        st, _, r = self.s.post("/api/caixa", {"envio": novo_envio(), "tipo": "aprovacao",
                                              "alvo": {"tipo": "ticket", "id": "04"}, "veredito": "aprovado"})
        self.assertEqual(st, 200, r)
        md = leitores.ler_texto(os.path.join(self.projeto.caixa, r["arquivo"] + ".md"))
        self.assertIn("comentário: em branco", md)

    def test_resposta_rodada_e_base(self) -> None:
        estado = self.s.estado()
        corpo = apoio.resposta_completa(estado, novo_envio())
        self._erro(dict(corpo, rodada="2000-01-01-nada-r1"), 409, "rodada-mudou", "rodada")
        self._erro(dict(corpo, rodada="2026-09-15-escolher-o-terreno-r1"), 409, "rodada-mudou", "rodada")
        self._erro(dict(corpo, rodada="2026-10-02-composteira-r1"), 400, "rodada-malformada", "rodada")
        self._erro(dict(corpo, base="0" * 64), 409, "rodada-mudou", "base")
        # o agente edita a rodada: a base muda e a resposta antiga é recusada
        caminho = os.path.join(self.projeto.rodadas, corpo["rodada"] + ".md")
        with open(caminho, "a", encoding="utf-8") as f:
            f.write("\n")
        self._erro(corpo, 409, "rodada-mudou", "base")
        corpo["base"] = leitores.sha256_arquivo(caminho)
        self.assertEqual(self.s.post("/api/caixa", corpo)[0], 200)

    def test_resposta_perguntas(self) -> None:
        estado = self.s.estado()
        corpo = apoio.resposta_completa(estado, novo_envio())

        def com(respostas):
            return dict(corpo, respostas=respostas)

        self._erro(com({"inexistente": {"texto": "x"}}), 400, "pergunta-inexistente", "respostas.inexistente")
        self._erro(com({"largura": {"escolha": ["gigante"]}}), 400, "chave-inexistente", "respostas.largura.escolha")
        self._erro(com({"largura": {"escolha": ["media", "largo"]}}), 400, "escolha-invalida")
        self._erro(com({"largura": {"escolha": ["media"], "cor": "x"}}), 400, "chave-desconhecida")
        self._erro(com({"pode-comecar": {"veredito": "recusado"}}), 400, "comentario-obrigatorio")
        self._erro(com({"pode-comecar": {"veredito": "talvez"}}), 400, "veredito-invalido")
        self._erro(com({}), 400, "nada-respondido", "respostas")
        self._erro(com({"largura": {"escolha": [], "outra": None, "comentario": None}, "algo-mais": {"texto": ""}}),
                   400, "nada-respondido")
        self._erro(com({"algo-mais": {"texto": "x" * 20001}}), 400, "texto-longo")
        self._erro(com("x"), 400, "respostas-invalidas", "respostas")
        # "outra" sozinha vale como resposta
        self.assertEqual(self.s.post("/api/caixa", com({"largura": {"outra": "2 m, para cadeira de rodas"}}))[0], 200)
        # as perguntas ausentes saem em branco no .md
        st, _, r = self.s.post("/api/caixa", dict(com({"algo-mais": {"texto": "só isso"}}), envio=novo_envio()))
        self.assertEqual(st, 200)
        md = leitores.ler_texto(os.path.join(self.projeto.caixa, r["arquivo"] + ".md"))
        self.assertIn("## Largura do canteiro\nem branco\n", md)
        self.assertIn("## Algo mais?\n> só isso\n", md)

    def test_resposta_proposta(self) -> None:
        estado = self.s.estado()
        corpo = apoio.resposta_completa(estado, novo_envio())
        linhas = corpo["respostas"]["mutirao"]["linhas"]

        def com(ls):
            return dict(corpo, respostas={"mutirao": {"linhas": ls}})

        self._erro(com(linhas + [{"id": "limpar", "ativa": True, "valores": {}}]), 400, "linha-repetida")
        self._erro(com([{"id": "estranha", "ativa": True, "valores": {}}]), 400, "proposta-invalida")
        self._erro(com([{"id": "limpar", "ativa": True, "valores": {"cor": "verde"}}]), 400, "coluna-inexistente")
        self._erro(com([{"id": "limpar", "ativa": "sim"}]), 400, "proposta-invalida")
        self._erro(com("x"), 400, "proposta-invalida")
        # rodada que só permite editar: reordenar, desligar, adicionar e remover são recusados
        rid = "2026-10-05-canteiros-e-caminhos-r3"
        caminho = os.path.join(self.projeto.rodadas, rid + ".md")
        with open(caminho, "w", encoding="utf-8", newline="\n") as f:
            f.write("---\ntitulo: Só editar\nticket: 03\naberta: 2026-10-05\nestado: aberta\n---\n\nctx\n\n"
                    "## Tabela\nid: tabela\ntipo: proposta\n\n```json\n"
                    '{"colunas": ["a"], "linhas": [{"id": "x", "a": "1"}, {"id": "y", "a": "2"}], "pode": ["editar"]}\n'
                    "```\n")
        base = leitores.sha256_arquivo(caminho)
        for ls, operacao in (
            ([{"id": "y"}, {"id": "x"}], "reordenar"),
            ([{"id": "x", "ativa": False}, {"id": "y"}], "ligar"),
            ([{"id": "x"}, {"id": "y"}, {"id": "nova-1", "valores": {"a": "3"}}], "adicionar"),
            ([{"id": "x"}], "remover"),
        ):
            st, _, r = self.s.post("/api/caixa", {"envio": novo_envio(), "tipo": "resposta", "rodada": rid, "base": base,
                                                  "respostas": {"tabela": {"linhas": ls}}})
            self.assertEqual((st, r["erro"]), (400, "operacao-nao-permitida"), r)
            self.assertIn(operacao, r["mensagem"])
        st, _, r = self.s.post("/api/caixa", {"envio": novo_envio(), "tipo": "resposta", "rodada": rid, "base": base,
                                              "respostas": {"tabela": {"linhas": [{"id": "x", "valores": {"a": "9"}}, {"id": "y"}]}}})
        self.assertEqual(st, 200, r)
        md = leitores.ler_texto(os.path.join(self.projeto.caixa, r["arquivo"] + ".md"))
        self.assertIn('- linha "x": a de "1" para "9"', md)

    def test_resposta_completa_gera_md_da_secao_4_2(self) -> None:
        estado = self.s.estado()
        corpo = apoio.resposta_completa(estado, novo_envio())
        st, _, r = self.s.post("/api/caixa", corpo)
        self.assertEqual(st, 200, r)
        self.assertFalse(r["repetido"])
        nome = r["arquivo"]
        md = leitores.ler_texto(os.path.join(self.projeto.caixa, nome + ".md"))
        campos, texto, _ = leitores.ler_frontmatter(md)
        self.assertEqual(campos["tipo"], "resposta")
        self.assertEqual(campos["rodada"], corpo["rodada"])
        self.assertEqual(campos["ticket"], "03")
        self.assertEqual(campos["estado"], "nova")
        self.assertEqual(campos["substitui"], "")
        self.assertIn("# Resposta: Como ficam os canteiros", texto)
        self.assertIn("escolha: media, 1,2 m (padrão das hortas da cidade) (a recomendada)\ncomentário:\n> só se a madeira der", texto)
        self.assertIn("escolhas: alface, cebolinha, tomate (a recomendada era alface, cebolinha)", texto)
        self.assertIn('- linha "montar": tempo de "3 h" para "4 h"', texto)
        self.assertIn('- linha nova "nova-1": tarefa "regar", quem "todos", tempo "30 min"', texto)
        self.assertIn('- linha "montar": desligada', texto)
        self.assertIn("- ordem nova: limpar, placas, montar, nova-1", texto)
        self.assertIn("versão completa: no .json irmão, em corpo.respostas.mutirao", texto)
        self.assertIn("aprovação: aprovado com ajuste\ncomentário:\n> se não chover", texto)
        self.assertIn("> levar água\n> ---\n> estado: lida", texto)
        with open(os.path.join(self.projeto.caixa, nome + ".json"), "r", encoding="utf-8") as f:
            dados = json.load(f)
        self.assertEqual(dados["rodada"]["id"], corpo["rodada"])
        self.assertEqual([p["id"] for p in dados["rodada"]["perguntas"]],
                         ["largura", "primeiras", "mutirao", "pode-comecar", "algo-mais"])
        self.assertEqual(dados["corpo_hash"], leitores.hash_corpo(corpo))
        # no estado: a rodada agora está respondida
        estado = self.s.estado()
        rodada = next(x for x in estado["rodadas"] if x["id"] == corpo["rodada"])
        self.assertTrue(rodada["respondida"])
        self.assertEqual(rodada["ultima_resposta"], nome)
        # GET por envio devolve o json completo mais estado e aviso
        st, _, g = self.s.get("/api/caixa/" + corpo["envio"])
        self.assertEqual((st, g["estado"], g["aviso"], g["arquivo"]), (200, "nova", "pendente", nome))

    def test_corrigir_resposta_com_substitui(self) -> None:
        estado = self.s.estado()
        corpo = apoio.resposta_completa(estado, novo_envio())
        st, _, r1 = self.s.post("/api/caixa", corpo)
        self.assertEqual(st, 200)
        corrigido = dict(corpo, envio=novo_envio(), substitui=r1["arquivo"])
        corrigido["respostas"] = {"algo-mais": {"texto": "mudei de ideia"}}
        st, _, r2 = self.s.post("/api/caixa", corrigido)
        self.assertEqual(st, 200, r2)
        md = leitores.ler_texto(os.path.join(self.projeto.caixa, r2["arquivo"] + ".md"))
        self.assertIn(f"substitui: {r1['arquivo']}\n", md)
        estado = self.s.estado()
        por_envio = {c["envio"]: c for c in estado["caixa"]}
        self.assertTrue(por_envio[corpo["envio"]]["substituida"])
        self.assertEqual(por_envio[corrigido["envio"]]["substitui"], r1["arquivo"])
        rodada = next(x for x in estado["rodadas"] if x["id"] == corpo["rodada"])
        self.assertEqual(rodada["ultima_resposta"], r2["arquivo"])
        self._erro(dict(corrigido, envio=novo_envio(), substitui="nao-existe"), 400, "substitui-invalido", "substitui")


class RodadaReescrita(ComServidor):
    """A rodada editada pelo maestro depois da resposta volta a esperar o Gustavo (correção de 2026-10-14)."""

    _erro = Validacao._erro

    def _reescrever(self, rid: str, trocar=None, acrescentar: str = "") -> None:
        caminho = os.path.join(self.projeto.rodadas, rid + ".md")
        with open(caminho, "r", encoding="utf-8", newline="") as f:
            texto = f.read()
        if trocar:
            texto = texto.replace(*trocar)
        with open(caminho, "w", encoding="utf-8", newline="") as f:
            f.write(texto + acrescentar)

    @staticmethod
    def _rodada(estado: dict, rid: str) -> dict:
        return next(x for x in estado["rodadas"] if x["id"] == rid)

    @staticmethod
    def _aguardando(estado: dict) -> list[str]:
        """A mesma regra do contador da página (`app.aguardando()` em web/torre.js)."""
        return [r["id"] for r in estado["rodadas"] if r["estado"] == "aberta" and not r["respondida"] and not r["malformada"]]

    def test_rodada_reescrita_volta_a_esperar_e_resposta_nova_substitui(self) -> None:
        estado = self.s.estado()
        corpo = apoio.resposta_completa(estado, novo_envio())
        rid, base_velha = corpo["rodada"], corpo["base"]
        st, _, r1 = self.s.post("/api/caixa", corpo)
        self.assertEqual(st, 200, r1)
        self.assertNotIn(rid, self._aguardando(self.s.estado()))
        # o maestro reescreve a rodada depois da resposta
        self._reescrever(rid, acrescentar="\nUma linha nova do maestro no fim do último \"por quê\".\n")
        estado = self.s.estado()
        rodada = self._rodada(estado, rid)
        self.assertNotEqual(rodada["base"], base_velha)
        self.assertEqual(rodada["estado"], "aberta")
        self.assertFalse(rodada["respondida"])                       # volta a esperar
        self.assertIn(rid, self._aguardando(estado))                # entra no "N aguardando você"
        self.assertEqual(rodada["ultima_resposta"], r1["arquivo"])  # a anterior continua como histórico
        # responder sobre a versão velha é recusado; sobre a nova, com substitui, é aceito
        self._erro(dict(corpo, envio=novo_envio()), 409, "rodada-mudou", "base")
        nova = dict(corpo, envio=novo_envio(), base=rodada["base"], substitui=r1["arquivo"])
        st, _, r2 = self.s.post("/api/caixa", nova)
        self.assertEqual(st, 200, r2)
        with open(os.path.join(self.projeto.caixa, r2["arquivo"] + ".json"), "r", encoding="utf-8") as f:
            gravado = json.load(f)
        self.assertEqual(gravado["rodada"]["base"], rodada["base"])
        self.assertEqual(gravado["substitui"], r1["arquivo"])
        estado = self.s.estado()
        rodada = self._rodada(estado, rid)
        self.assertTrue(rodada["respondida"])
        self.assertEqual(rodada["ultima_resposta"], r2["arquivo"])
        self.assertNotIn(rid, self._aguardando(estado))
        self.assertTrue(next(c for c in estado["caixa"] if c["arquivo"] == r1["arquivo"])["substituida"])
        # a decisão vem dos arquivos, não da memória do servidor
        self.reiniciar()
        self.assertTrue(self._rodada(self.s.estado(), rid)["respondida"])

    def test_rodada_absorvida_reescrita_nao_volta_a_esperar(self) -> None:
        estado = self.s.estado()
        corpo = apoio.resposta_completa(estado, novo_envio())
        rid = corpo["rodada"]
        st, _, r1 = self.s.post("/api/caixa", corpo)
        self.assertEqual(st, 200, r1)
        self._reescrever(rid, trocar=("estado: aberta", "estado: absorvida"))
        estado = self.s.estado()
        rodada = self._rodada(estado, rid)
        self.assertEqual(rodada["estado"], "absorvida")
        self.assertTrue(rodada["respondida"])
        self.assertNotIn(rid, self._aguardando(estado))
        self.assertEqual(rodada["ultima_resposta"], r1["arquivo"])

    def test_rodada_regravada_igual_continua_respondida(self) -> None:
        estado = self.s.estado()
        corpo = apoio.resposta_completa(estado, novo_envio())
        self.assertEqual(self.s.post("/api/caixa", corpo)[0], 200)
        self._reescrever(corpo["rodada"])   # mesmos bytes: mtime novo, sha256 igual
        self.assertTrue(self._rodada(self.s.estado(), corpo["rodada"])["respondida"])

    def test_ligar_respostas_sem_base_gravado_conta_como_atual(self) -> None:
        rodadas = [{"id": "r", "estado": "aberta", "base": "b2"}]
        caixa = [{"arquivo": "a1", "tipo": "resposta", "alvo": {"id": "r"}, "substituida": False}]
        leitores.ligar_respostas(rodadas, caixa, {"a1": None})
        self.assertTrue(rodadas[0]["respondida"])
        leitores.ligar_respostas(rodadas, caixa, {"a1": "b1"})
        self.assertFalse(rodadas[0]["respondida"])
        self.assertEqual(rodadas[0]["ultima_resposta"], "a1")
        rodadas[0]["estado"] = "suspensa"
        leitores.ligar_respostas(rodadas, caixa, {"a1": "b1"})
        self.assertTrue(rodadas[0]["respondida"])


class Robustez(ComServidor):
    def test_mesmo_envio_duas_vezes_um_arquivo(self) -> None:
        corpo = apoio.resposta_completa(self.s.estado(), novo_envio())
        antes = self.arquivos_da_caixa()
        st1, _, r1 = self.s.post("/api/caixa", corpo)
        st2, _, r2 = self.s.post("/api/caixa", corpo)
        self.assertEqual((st1, r1["repetido"], st2, r2["repetido"]), (200, False, 200, True))
        self.assertEqual(r1["arquivo"], r2["arquivo"])
        self.assertEqual(len(self.arquivos_da_caixa() - antes), 2)

    def test_mesmo_envio_corpo_diferente_409(self) -> None:
        corpo = apoio.resposta_completa(self.s.estado(), novo_envio())
        self.assertEqual(self.s.post("/api/caixa", corpo)[0], 200)
        outro = dict(corpo)
        outro["respostas"] = {"algo-mais": {"texto": "outro"}}
        st, _, r = self.s.post("/api/caixa", outro)
        self.assertEqual((st, r["erro"]), (409, "envio-conflito"))

    def test_mesmo_envio_depois_da_rodada_absorvida_200_repetido(self) -> None:
        corpo = apoio.resposta_completa(self.s.estado(), novo_envio())
        self.assertEqual(self.s.post("/api/caixa", corpo)[0], 200)
        caminho = os.path.join(self.projeto.rodadas, corpo["rodada"] + ".md")
        texto = leitores.ler_texto(caminho).replace("estado: aberta", "estado: absorvida")
        with open(caminho, "w", encoding="utf-8", newline="\n") as f:
            f.write(texto)
        st, _, r = self.s.post("/api/caixa", corpo)
        self.assertEqual((st, r["repetido"]), (200, True))
        # um envio novo para a mesma rodada já não entra
        st, _, r = self.s.post("/api/caixa", dict(corpo, envio=novo_envio()))
        self.assertEqual((st, r["erro"]), (409, "rodada-mudou"))

    def test_vinte_envios_em_paralelo_vinte_arquivos(self) -> None:
        antes = self.arquivos_da_caixa()
        resultados: list = []
        erros: list = []

        def enviar(i: int) -> None:
            try:
                corpo = {"envio": novo_envio(), "tipo": "comentario", "alvo": {"tipo": "ticket", "id": "04"},
                         "texto": f"comentário {i}"}
                resultados.append(self.s.post("/api/caixa", corpo))
            except Exception as e:  # noqa: BLE001
                erros.append(e)

        threads = [threading.Thread(target=enviar, args=(i,)) for i in range(20)]
        for t in threads:
            t.start()
        for t in threads:
            t.join(timeout=60)
        self.assertEqual(erros, [])
        self.assertEqual([st for st, _, _ in resultados], [200] * 20)
        nomes = {r["arquivo"] for _, _, r in resultados}
        self.assertEqual(len(nomes), 20)
        self.assertEqual(len(self.arquivos_da_caixa() - antes), 40)
        fila = self.s.get("/api/aviso")[2]["fila"]
        self.assertEqual(len([f for f in fila if f["estado"] == "pendente"]), 21)

    def _queda_e_reinicio(self, alvo, metodo: str) -> None:
        corpo = apoio.resposta_completa(self.s.estado(), novo_envio())
        antes = self.arquivos_da_caixa()
        with mock.patch.object(alvo, metodo, mock.Mock(side_effect=OSError("disco cheio"))):
            st, _, r = self.s.post("/api/caixa", corpo)
        self.assertEqual((st, r["erro"]), (500, "gravacao-parcial"), r)
        nome = r["arquivo"]
        self.assertTrue(os.path.exists(os.path.join(self.projeto.caixa, nome + ".json")))
        # o retry da página, antes do reparo, já cai na idempotência
        st, _, r2 = self.s.post("/api/caixa", corpo)
        self.assertEqual((st, r2["repetido"], r2["arquivo"]), (200, True, nome))
        # sobra em .tmp e servidor derrubado
        with open(os.path.join(self.projeto.caixa, ".tmp", "sobra.parcial"), "w") as f:
            f.write("x")
        self.reiniciar()
        self.assertTrue(os.path.exists(os.path.join(self.projeto.caixa, nome + ".md")))
        self.assertEqual(os.listdir(os.path.join(self.projeto.caixa, ".tmp")), [])
        estado = self.s.estado()
        entrada = next(c for c in estado["caixa"] if c["envio"] == corpo["envio"])
        self.assertEqual((entrada["estado"], entrada["aviso"]), ("nova", "pendente"))
        fila = self.s.get("/api/aviso")[2]["fila"]
        self.assertEqual([f for f in fila if f["envio"] == corpo["envio"]][0]["tentativas"], 0)
        st, _, r3 = self.s.post("/api/caixa", corpo)
        self.assertEqual((st, r3["repetido"], r3["arquivo"]), (200, True, nome))
        self.assertEqual(len(self.arquivos_da_caixa() - antes), 2)

    def test_queda_depois_do_json_antes_do_md(self) -> None:
        self._queda_e_reinicio(modulo_caixa.Caixa, "_gravar_md")

    def test_queda_depois_do_md_antes_da_fila(self) -> None:
        self._queda_e_reinicio(modulo_caixa.Fila, "registrar")

    def test_avisos_apagado_ou_corrompido_no_reinicio(self) -> None:
        corpo = apoio.resposta_completa(self.s.estado(), novo_envio())
        st, _, r = self.s.post("/api/caixa", corpo)
        self.assertEqual(st, 200)
        avisos = os.path.join(self.projeto.caixa, ".avisos.json")
        os.remove(avisos)
        self.reiniciar()
        fila = {f["envio"]: f for f in self.s.get("/api/aviso")[2]["fila"]}
        self.assertEqual(fila[corpo["envio"]]["estado"], "pendente")
        self.assertEqual(fila[ENVIO_ORFAO]["estado"], "pendente")
        with open(avisos, "w") as f:
            f.write("corrompido {{{")
        self.reiniciar()
        fila = {f["envio"]: f for f in self.s.get("/api/aviso")[2]["fila"]}
        self.assertEqual(fila[corpo["envio"]]["estado"], "pendente")
        self.assertTrue(any(".avisos.json" in p["arquivo"] for p in self.s.estado()["problemas"]))
        st, _, r = self.s.post("/api/caixa", corpo)
        self.assertEqual((st, r["repetido"]), (200, True))

    def test_tentar_de_novo(self) -> None:
        self.s.torre.caixa.fila.marcar(ENVIO_ORFAO, "falhou", erro="agente com nome errado")
        self.assertEqual(self.s.get("/api/aviso")[2]["fila"][0]["estado"], "falhou")
        st, _, r = self.s.post("/api/aviso/tentar", {"envio": ENVIO_ORFAO})
        self.assertEqual((st, r["estado"]), (200, "pendente"))
        st, _, r = self.s.post("/api/aviso/tentar", {"envio": novo_envio()})
        self.assertEqual((st, r["erro"]), (404, "aviso-inexistente"))
        self.assertEqual(self.s.pedir("POST", "/api/aviso/tentar", corpo={"envio": ENVIO_ORFAO},
                                      cabecalhos={"Content-Type": "application/json"})[0], 403)

    def test_fixtures_ruins_aparecem_em_problemas_e_o_resto_funciona(self) -> None:
        estado = self.s.estado()
        arquivos = [p["arquivo"] for p in estado["problemas"]]
        self.assertIn("issues/05-horario-de-rega.md", arquivos)      # dependência inexistente
        self.assertIn("issues/07-mutirao-de-abertura.md", arquivos)  # ciclo
        self.assertIn("issues/09-galinheiro.md", arquivos)           # status desconhecido
        self.assertIn("portal/rodadas/2026-10-02-composteira-r1.md", arquivos)
        self.assertEqual(len(estado["tickets"]), 10)
        # um ticket ilegível e um JSON de proposta quebrado não derrubam o estado
        with open(os.path.join(self.projeto.tickets, "11-sem-titulo.md"), "w", encoding="utf-8") as f:
            f.write("Type: task\nStatus: open\n")
        with open(os.path.join(self.projeto.rodadas, "2026-10-06-quebrada-r1.md"), "w", encoding="utf-8") as f:
            f.write("---\ntitulo: Quebrada\nticket: 04\naberta: 2026-10-06\nestado: aberta\n---\n\n"
                    "## P\nid: p\ntipo: proposta\n\n```json\n{ quebrado\n```\n")
        estado = self.s.estado()
        self.assertEqual(len(estado["tickets"]), 11)
        quebrada = next(r for r in estado["rodadas"] if r["id"] == "2026-10-06-quebrada-r1")
        self.assertTrue(quebrada["malformada"])
        self.assertIn("JSON", quebrada["erro"])
        arquivos = [p["arquivo"] for p in estado["problemas"]]
        self.assertIn("issues/11-sem-titulo.md", arquivos)
        self.assertIn("portal/rodadas/2026-10-06-quebrada-r1.md", arquivos)


def _editar_json(caminho: str, mudar) -> None:
    with open(caminho, "r", encoding="utf-8") as f:
        dados = json.load(f)
    mudar(dados)
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False)


def _criar_junction(atalho: str, destino: str) -> bool:
    """Junction (Windows) ou symlink de pasta; ``False`` se a máquina não deixa."""
    if os.name == "nt":
        r = subprocess.run(["cmd", "/c", "mklink", "/J", atalho, destino], capture_output=True)
        if r.returncode == 0 and os.path.isdir(atalho):
            return True
    try:
        os.symlink(destino, atalho, target_is_directory=True)
        return True
    except (OSError, NotImplementedError):
        return False


class Confinamento(unittest.TestCase):
    """§3.2, "sem exceção": caminho do projeto.json ou do cartas.json fora da base vira problema e não é lido."""

    def setUp(self) -> None:
        self.tmp, self.projeto_json = apoio.copiar_horta()
        self.addCleanup(apoio.apagar, self.tmp)
        self.horta = os.path.dirname(os.path.dirname(self.projeto_json))

    def subir(self) -> apoio.ServidorDeTeste:
        s = apoio.ServidorDeTeste(self.projeto_json)
        self.addCleanup(s.parar)
        return s

    def problemas_do_projeto_json(self, estado: dict) -> list[str]:
        return [p["mensagem"] for p in estado["problemas"] if p["arquivo"] == "portal/projeto.json"]

    def test_mapa_fora_da_raiz_vira_problema_e_nao_e_lido(self) -> None:
        with open(os.path.join(self.tmp, "segredo.md"), "w", encoding="utf-8") as f:
            f.write("## Destination\nSEGREDO FORA DA RAIZ\n1. um critério\n")
        _editar_json(self.projeto_json, lambda d: d.update(mapa="../segredo.md"))
        s = self.subir()
        status, _, estado = s.get("/api/estado")
        self.assertEqual(status, 200)
        self.assertEqual(estado["destino"], {"texto": "", "criterios": []})
        self.assertEqual(estado["decisoes"], [])
        mensagens = self.problemas_do_projeto_json(estado)
        self.assertTrue(any(m.startswith("mapa:") and "sai de raiz" in m for m in mensagens), mensagens)
        self.assertNotIn("SEGREDO", json.dumps(estado, ensure_ascii=False))
        # o resto do estado continua inteiro
        self.assertEqual(len(estado["tickets"]), 10)
        self.assertEqual(s.get("/carta/mapa-dos-canteiros/")[0], 200)

    def test_caixa_fora_do_portal_recusa_subir(self) -> None:
        _editar_json(self.projeto_json, lambda d: d.update(caixa="../../caixa-fora"))
        fora = os.path.join(self.tmp, "caixa-fora")
        with self.assertRaises(ValueError) as cm:
            modulo_torre.criar_servidor(self.projeto_json, porta=0, ambiente=apoio.ambiente_limpo(), silencioso=True)
        self.assertIn("caixa", str(cm.exception))
        self.assertIn("não há onde gravar", str(cm.exception))
        self.assertEqual(modulo_torre.main([self.projeto_json]), 1)
        self.assertFalse(os.path.exists(fora))
        # o leitor puro continua montando o estado, com o problema em palavras e a caixa vazia
        estado = leitores.montar_estado(self.projeto_json, apoio.ambiente_limpo())
        self.assertEqual(estado["caixa"], [])
        self.assertTrue(any(m.startswith("caixa:") and "nem gravado" in m for m in self.problemas_do_projeto_json(estado)))

    def test_caminho_absoluto_e_recusado_mesmo_apontando_para_dentro(self) -> None:
        absoluto = os.path.join(self.horta, "issues")
        _editar_json(self.projeto_json, lambda d: d.update(tickets=absoluto, rodadas=os.path.join(self.horta, "portal", "rodadas"),
                                                           glossario="../GLOSSARY.md"))
        s = self.subir()
        estado = s.estado()
        self.assertEqual(estado["tickets"], [])
        self.assertEqual(estado["rodadas"], [])
        self.assertEqual(estado["glossario"], [])
        mensagens = self.problemas_do_projeto_json(estado)
        self.assertTrue(any(m.startswith("tickets:") and "absoluto" in m for m in mensagens), mensagens)
        self.assertTrue(any(m.startswith("rodadas:") and "absoluto" in m for m in mensagens), mensagens)
        self.assertTrue(any(m.startswith("glossario:") and "sai de raiz" in m for m in mensagens), mensagens)
        status, _, corpo = s.get("/api/ticket/03")
        self.assertEqual((status, corpo["erro"]), (404, "nao-encontrado"))

    def test_junction_em_issues_para_fora_e_ignorada(self) -> None:
        fora = os.path.join(self.tmp, "fora")
        os.makedirs(fora)
        with open(os.path.join(fora, "01-vazou.md"), "w", encoding="utf-8") as f:
            f.write("# Vazou\n\nType: task\nStatus: open\n")
        atalho = os.path.join(self.horta, "issues", "atalho")
        if not _criar_junction(atalho, fora):
            self.skipTest("não deu para criar junction nem symlink nesta máquina")
        self.assertTrue(os.path.isfile(os.path.join(atalho, "01-vazou.md")))
        # a pasta de tickets do projeto.json aponta para a junction: o caminho real sai da raiz
        _editar_json(self.projeto_json, lambda d: d.update(tickets="issues/atalho"))
        s = self.subir()
        estado = s.estado()
        self.assertEqual(estado["tickets"], [])
        mensagens = self.problemas_do_projeto_json(estado)
        self.assertTrue(any(m.startswith("tickets:") and "junction" in m for m in mensagens), mensagens)
        self.assertEqual(s.get("/api/ticket/01")[0], 404)

    def test_symlink_de_arquivo_em_issues_para_fora_e_ignorado(self) -> None:
        fora = os.path.join(self.tmp, "fora")
        os.makedirs(fora)
        alvo = os.path.join(fora, "vazou.md")
        with open(alvo, "w", encoding="utf-8") as f:
            f.write("# Vazou\n\nType: task\nStatus: open\n")
        atalho = os.path.join(self.horta, "issues", "11-vazou.md")
        try:
            os.symlink(alvo, atalho)
        except (OSError, NotImplementedError):
            self.skipTest("não deu para criar symlink de arquivo nesta máquina")
        s = self.subir()
        estado = s.estado()
        self.assertEqual([t["numero"] for t in estado["tickets"]][-1], "10")
        self.assertTrue(any(p["arquivo"] == "issues/11-vazou.md" and "fora da pasta" in p["mensagem"]
                            for p in estado["problemas"]))
        status, _, corpo = s.get("/api/ticket/11")
        self.assertEqual((status, corpo["erro"]), (404, "nao-encontrado"))

    def test_carta_fora_da_raiz_fica_na_lista_com_problema_e_nao_e_servida(self) -> None:
        with open(os.path.join(self.tmp, "fora.html"), "w", encoding="utf-8") as f:
            f.write("<p>fora</p>")
        cartas_json = os.path.join(self.horta, "portal", "cartas.json")
        _editar_json(cartas_json, lambda d: d.append({
            "id": "fora", "titulo": "Fora", "arquivo": "../fora.html", "pasta": "..", "proposito": "x", "ticket": None,
            "decisao": "x", "data": {"valor": "2026-01-01", "tipo": "feita"}, "situacao": "vigente", "mestra": False}))
        s = self.subir()
        estado = s.estado()
        self.assertIn("fora", [c["id"] for c in estado["cartas"]])
        self.assertTrue(any(p["arquivo"] == "portal/cartas.json" and "carta fora:" in p["mensagem"]
                            and "sai de raiz" in p["mensagem"] for p in estado["problemas"]))
        self.assertEqual(s.get("/carta/fora/")[0], 404)
        self.assertEqual(s.get("/carta/fora/fora.html")[0], 404)
        self.assertEqual(s.get("/carta/mapa-dos-canteiros/")[0], 200)


class ArquivosRuins(ComServidor):
    """§3.6: um arquivo ruim vira problema em palavras; os demais continuam e a API nunca responde 500."""

    def test_ticket_em_codificacao_invalida(self) -> None:
        caminho = os.path.join(self.projeto.tickets, "05-horario-de-rega.md")
        with open(caminho, "wb") as f:
            f.write(b"\xff\xfequebrado")
        status, _, estado = self.s.get("/api/estado")
        self.assertEqual(status, 200)
        self.assertEqual(len(estado["tickets"]), 10)
        t05 = next(t for t in estado["tickets"] if t["numero"] == "05")
        self.assertEqual(t05["estado"], "desconhecido")
        self.assertTrue(any(p["arquivo"] == "issues/05-horario-de-rega.md" and "UTF-8" in p["mensagem"]
                            for p in estado["problemas"]), estado["problemas"])
        status, _, corpo = self.s.get("/api/ticket/05")
        self.assertEqual((status, corpo["erro"]), (422, "arquivo-ilegivel"), corpo)
        self.assertIn("UTF-8", corpo["mensagem"])
        self.assertIn("campo", corpo)
        self.assertEqual(self.s.get("/api/ticket/03")[0], 200)

    def test_mapa_estrategia_glossario_e_rodada_em_codificacao_invalida(self) -> None:
        ruins = {"mapa.md": self.projeto.mapa, "estrategia.md": self.projeto.estrategia,
                 "GLOSSARY.md": self.projeto.glossario,
                 "portal/rodadas/2026-10-01-canteiros-e-caminhos-r2.md":
                     os.path.join(self.projeto.rodadas, "2026-10-01-canteiros-e-caminhos-r2.md")}
        for caminho in ruins.values():
            with open(caminho, "wb") as f:
                f.write(b"\xc3\x28 nada de utf-8")
        status, _, estado = self.s.get("/api/estado")
        self.assertEqual(status, 200)
        self.assertEqual((estado["radar"], estado["glossario"], estado["decisoes"]), ([], [], []))
        arquivos = {p["arquivo"]: p["mensagem"] for p in estado["problemas"]}
        for nome in ruins:
            self.assertIn(nome, arquivos)
            self.assertIn("UTF-8", arquivos[nome])
        rodada = next(r for r in estado["rodadas"] if r["id"] == "2026-10-01-canteiros-e-caminhos-r2")
        self.assertTrue(rodada["malformada"])
        self.assertEqual(len(estado["tickets"]), 10)

    def _copiar_json_da_caixa(self, nome_novo: str, mudar) -> str:
        origem = next(n for n in sorted(self.arquivos_da_caixa()) if n.endswith(".json") and "comentario" in n)
        with open(os.path.join(self.projeto.caixa, origem), "r", encoding="utf-8") as f:
            dados = json.load(f)
        mudar(dados)
        caminho = os.path.join(self.projeto.caixa, nome_novo + ".json")
        with open(caminho, "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False)
        return caminho

    def test_json_da_caixa_com_envio_lista_vira_problema_e_nao_e_indexado(self) -> None:
        self._copiar_json_da_caixa("quebrado", lambda d: d.update(envio=[]))
        # com o servidor no ar
        status, _, estado = self.s.get("/api/estado")
        self.assertEqual(status, 200)
        self.assertNotIn("quebrado", [c["arquivo"] for c in estado["caixa"]])
        self.assertTrue(any(p["arquivo"] == "portal/caixa/quebrado.json" and "envio" in p["mensagem"]
                            for p in estado["problemas"]), estado["problemas"])
        self.assertFalse(os.path.exists(os.path.join(self.projeto.caixa, "quebrado.md")))
        # um POST (que reconcilia antes) continua funcionando e não indexa o arquivo ruim
        st, _, r = self.s.post("/api/caixa", {"envio": novo_envio(), "tipo": "comentario",
                                              "alvo": {"tipo": "ticket", "id": "04"}, "texto": "ainda funciona"})
        self.assertEqual(st, 200, r)
        self.assertNotIn("quebrado", self.s.torre.caixa.nomes())
        # no arranque
        self.reiniciar()
        self.assertEqual(self.s.get("/api/estado")[0], 200)
        self.assertNotIn("quebrado", self.s.torre.caixa.nomes())
        self.assertFalse(os.path.exists(os.path.join(self.projeto.caixa, "quebrado.md")))
        self.assertEqual(len([f for f in self.s.get("/api/aviso")[2]["fila"] if f["arquivo"] == "quebrado"]), 0)

    def test_outros_campos_da_caixa_fora_da_forma(self) -> None:
        casos = {
            "substitui-lista": lambda d: d.update(substitui=["x"]),
            "hash-numero": lambda d: d.update(corpo_hash=12),
            "alvo-sem-id": lambda d: d.update(alvo={"tipo": "ticket", "id": 4}),
            "enviada-nula": lambda d: d.update(enviada=None),
            "tipo-estranho": lambda d: d.update(tipo="bilhete"),
            "corpo-lista": lambda d: d.update(corpo=[]),
            "resposta-sem-rodada": lambda d: d.update(tipo="resposta", rodada="x"),
        }
        for nome, mudar in casos.items():
            self._copiar_json_da_caixa(nome, mudar)
        status, _, estado = self.s.get("/api/estado")
        self.assertEqual(status, 200)
        arquivos = [p["arquivo"] for p in estado["problemas"]]
        for nome in casos:
            with self.subTest(caso=nome):
                self.assertIn(f"portal/caixa/{nome}.json", arquivos)
                self.assertNotIn(nome, [c["arquivo"] for c in estado["caixa"]])
        self.assertEqual(len(estado["caixa"]), apoio.MENSAGENS_DA_FIXTURE)

    def test_fila_malformada_e_descartada_registro_a_registro_e_recomposta(self) -> None:
        avisos = os.path.join(self.projeto.caixa, ".avisos.json")
        ruim = novo_envio()
        with open(avisos, "w", encoding="utf-8") as f:
            json.dump({
                ruim: {"estado": "pendente", "tentativas": "abc"},
                "nao-e-uuid": {"estado": "pendente", "tentativas": 0},
                ENVIO_ORFAO: {"estado": "entregue", "tentativas": 1, "ultimo_erro": None, "proximo": "nunca"},
            }, f)
        self.reiniciar()  # o servidor sobe
        status, _, aviso = self.s.get("/api/aviso")
        self.assertEqual(status, 200)
        fila = {f["envio"]: f for f in aviso["fila"]}
        self.assertNotIn(ruim, fila)
        self.assertNotIn("nao-e-uuid", fila)
        # o registro do órfão era inválido (proximo) e foi recomposto da mensagem: .md nova → pendente
        self.assertEqual(fila[ENVIO_ORFAO]["estado"], "pendente")
        self.assertEqual(fila[ENVIO_ORFAO]["tentativas"], 0)
        estado = self.s.estado()
        mensagens = [p["mensagem"] for p in estado["problemas"] if p["arquivo"] == "portal/caixa/.avisos.json"]
        self.assertEqual(len(mensagens), 3, mensagens)
        self.assertTrue(any("tentativas" in m and ruim in m for m in mensagens))
        self.assertTrue(any("UUID" in m for m in mensagens))
        self.assertTrue(any("proximo" in m for m in mensagens))
        self.assertEqual([e for e, _ in self.s.torre.caixa.fila.pendentes()], [ENVIO_ORFAO])
        with open(avisos, "r", encoding="utf-8") as f:
            self.assertEqual(set(json.load(f)), {ENVIO_ORFAO})

    def test_problemas_ordenados_por_arquivo_e_mensagem(self) -> None:
        with open(os.path.join(self.projeto.caixa, ".avisos.json"), "w", encoding="utf-8") as f:
            f.write("{{{")
        with open(os.path.join(self.projeto.tickets, "05-horario-de-rega.md"), "wb") as f:
            f.write(b"\xff")
        self.reiniciar()
        problemas = self.s.estado()["problemas"]
        self.assertGreater(len(problemas), 5)
        self.assertEqual(problemas, sorted(problemas, key=lambda p: (p["arquivo"], p["mensagem"])))


class Arranque(unittest.TestCase):
    def test_porta_ocupada_recusa_subir(self) -> None:
        tmp, projeto_json = apoio.copiar_horta()
        self.addCleanup(apoio.apagar, tmp)
        s = apoio.ServidorDeTeste(projeto_json)
        self.addCleanup(s.parar)
        with self.assertRaises(OSError):
            modulo_torre.criar_servidor(projeto_json, porta=s.porta, ambiente=apoio.ambiente_limpo(), silencioso=True)

    def test_projeto_json_ausente_ou_invalido(self) -> None:
        tmp = tempfile.mkdtemp(prefix="torre-ruim-")
        self.addCleanup(apoio.apagar, tmp)
        ausente = os.path.join(tmp, "nao-existe.json")
        with self.assertRaises(FileNotFoundError):
            modulo_torre.criar_servidor(ausente, porta=0, silencioso=True)
        self.assertEqual(modulo_torre.main([ausente]), 1)
        invalido = os.path.join(tmp, "projeto.json")
        with open(invalido, "w", encoding="utf-8") as f:
            f.write('{"nome": "x"}')
        with self.assertRaises(ValueError):
            modulo_torre.criar_servidor(invalido, porta=0, silencioso=True)
        self.assertEqual(modulo_torre.main([invalido]), 1)
        with open(invalido, "w", encoding="utf-8") as f:
            f.write("{ nem json")
        self.assertEqual(modulo_torre.main([invalido]), 1)
        self.assertEqual(modulo_torre.main([]), 2)

    def test_escuta_so_em_127_0_0_1(self) -> None:
        tmp, projeto_json = apoio.copiar_horta()
        self.addCleanup(apoio.apagar, tmp)
        s = apoio.ServidorDeTeste(projeto_json)
        self.addCleanup(s.parar)
        self.assertEqual(s.servidor.server_address[0], "127.0.0.1")
        self.assertEqual(s.servidor.socket.family, socket.AF_INET)

    def test_subir_pelo_script(self) -> None:
        """``python nucleo/torre.py <projeto.json>`` sobe, atende e diz no terminal como está o aviso."""
        tmp, projeto_json = apoio.copiar_horta()
        self.addCleanup(apoio.apagar, tmp)
        with socket.socket() as sock:
            sock.bind(("127.0.0.1", 0))
            porta = sock.getsockname()[1]
        with open(projeto_json, "r", encoding="utf-8") as f:
            dados = json.load(f)
        dados["porta"] = porta
        with open(projeto_json, "w", encoding="utf-8") as f:
            json.dump(dados, f)
        amb = apoio.ambiente_limpo()
        amb["PYTHONIOENCODING"] = "utf-8"
        proc = subprocess.Popen([sys.executable, os.path.join(apoio.PASTA_NUCLEO, "torre.py"), projeto_json],
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=amb, text=True,
                                encoding="utf-8", errors="replace")
        try:
            import http.client
            import time
            fim = time.time() + 15
            status = None
            while time.time() < fim and status is None:
                try:
                    conn = http.client.HTTPConnection("127.0.0.1", porta, timeout=2)
                    conn.request("GET", "/api/versao")
                    status = conn.getresponse().status
                    conn.close()
                except OSError:
                    time.sleep(0.1)
            self.assertEqual(status, 200)
        finally:
            proc.terminate()
            saida, _ = proc.communicate(timeout=15)
        self.assertIn("Torre no ar", saida)
        self.assertIn("aviso ao agente: indisponível", saida)



def _trocar_tmp_da_caixa(pasta_caixa: str, destino: str, junction: bool) -> bool:
    tmp = os.path.join(pasta_caixa, ".tmp")
    if os.path.isdir(tmp) and not os.path.islink(tmp):
        for nome in os.listdir(tmp):
            os.remove(os.path.join(tmp, nome))
        os.rmdir(tmp)
    if junction and os.name == "nt":
        return subprocess.run(["cmd", "/c", "mklink", "/J", tmp, destino], capture_output=True).returncode == 0 \
            and os.path.isdir(tmp)
    try:
        os.symlink(destino, tmp, target_is_directory=True)
    except (OSError, NotImplementedError):
        return False
    return os.path.isdir(tmp)


class CodigosNaApi(unittest.TestCase):
    def test_estado_devolve_codigos_do_projeto_json(self) -> None:
        tmp, projeto_json = apoio.copiar_horta()
        self.addCleanup(apoio.apagar, tmp)
        _editar_json(projeto_json, lambda d: d.update(codigos={"Q": "pergunta numerada das rodadas de mapeamento"}))
        s = apoio.ServidorDeTeste(projeto_json)
        self.addCleanup(s.parar)
        self.assertEqual(s.estado()["projeto"]["codigos"], {"Q": "pergunta numerada das rodadas de mapeamento"})
        _editar_json(projeto_json, lambda d: d.update(codigos={"Q1": "x"}))
        s.parar()
        s = apoio.ServidorDeTeste(projeto_json)  # sobe mesmo assim
        self.addCleanup(s.parar)
        estado = s.estado()
        self.assertEqual(estado["projeto"]["codigos"], {})
        self.assertTrue(any(p["arquivo"] == "portal/projeto.json" and p["mensagem"].startswith("codigos:")
                            for p in estado["problemas"]))


class ConfinamentoDaTmpNaTorre(unittest.TestCase):
    """O servidor recusa subir com ``caixa/.tmp`` apontando para fora e não toca no alvo; um item de ``.tmp``
    apontando para fora aparece em ``/api/estado``."""

    def setUp(self) -> None:
        self.tmp, self.projeto_json = apoio.copiar_horta()
        self.addCleanup(apoio.apagar, self.tmp)
        self.caixa = leitores.Projeto(self.projeto_json).caixa
        self.fora = os.path.join(self.tmp, "area-sentinela")
        os.makedirs(self.fora)
        self.sentinela = os.path.join(self.fora, "nao-apagar.txt")
        with open(self.sentinela, "w", encoding="utf-8") as f:
            f.write("arquivo de prova\n")

    def _recusa_subir(self) -> None:
        with self.assertRaises(ValueError) as cm:
            modulo_torre.criar_servidor(self.projeto_json, porta=0, ambiente=apoio.ambiente_limpo(), silencioso=True)
        self.assertIn("caixa", str(cm.exception))
        self.assertIn("atalho ou junction", str(cm.exception))
        self.assertEqual(modulo_torre.main([self.projeto_json]), 1)
        self.assertTrue(os.path.exists(self.sentinela), "a sentinela fora da caixa foi apagada")
        self.assertEqual(os.listdir(self.fora), ["nao-apagar.txt"])

    def test_tmp_symlink_para_fora_recusa_subir_sem_tocar_na_sentinela(self) -> None:
        self.assertTrue(_trocar_tmp_da_caixa(self.caixa, self.fora, junction=False),
                        "não deu para criar o symlink de pasta; este teste não pode ser pulado")
        self._recusa_subir()

    def test_tmp_junction_para_fora_recusa_subir_sem_tocar_na_sentinela(self) -> None:
        self.assertTrue(_trocar_tmp_da_caixa(self.caixa, self.fora, junction=True),
                        "não deu para criar a junction; este teste não pode ser pulado")
        self._recusa_subir()

    def test_item_de_tmp_para_fora_vira_problema_no_estado(self) -> None:
        atalho = os.path.join(self.caixa, ".tmp", "vazou.parcial")
        try:
            os.symlink(self.sentinela, atalho)
        except (OSError, NotImplementedError):
            self.fail("não deu para criar o symlink de arquivo; este teste não pode ser pulado")
        s = apoio.ServidorDeTeste(self.projeto_json)
        self.addCleanup(s.parar)
        estado = s.estado()
        problemas = [p for p in estado["problemas"] if p["arquivo"] == "portal/caixa/.tmp/vazou.parcial"]
        self.assertEqual(len(problemas), 1, estado["problemas"])
        self.assertIn("atalho ou junction", problemas[0]["mensagem"])
        self.assertTrue(os.path.lexists(atalho))
        self.assertEqual(leitores.ler_texto(self.sentinela), "arquivo de prova\n")
        # o servidor continua servindo e gravando normalmente
        st, _, r = s.post("/api/caixa", {"envio": novo_envio(), "tipo": "comentario",
                                         "alvo": {"tipo": "ticket", "id": "04"}, "texto": "ainda funciona"})
        self.assertEqual(st, 200, r)
        self.assertEqual(os.listdir(self.fora), ["nao-apagar.txt"])


class RetratoMalformado(ComServidor):
    """§3.7: um ``.json`` de resposta com retrato ou respostas fora da forma é rejeitado inteiro: problema,
    fora do índice, sem ``.md``, no arranque e em execução."""

    def _resposta_valida_gravada(self) -> dict:
        st, _, r = self.s.post("/api/caixa", apoio.resposta_completa(self.s.estado(), novo_envio()))
        self.assertEqual(st, 200, r)
        with open(os.path.join(self.projeto.caixa, r["arquivo"] + ".json"), "r", encoding="utf-8") as f:
            return json.load(f)

    def _gravar_variante(self, modelo: dict, nome: str, mudar) -> str:
        d = json.loads(json.dumps(modelo))
        d["envio"] = novo_envio()
        mudar(d)
        with open(os.path.join(self.projeto.caixa, nome + ".json"), "w", encoding="utf-8") as f:
            json.dump(d, f, ensure_ascii=False)
        return d["envio"]

    @staticmethod
    def _pergunta(d: dict, tipo: str) -> dict:
        return next(p for p in d["rodada"]["perguntas"] if p["tipo"] == tipo)

    def test_retrato_com_colunas_lista_de_listas_nao_e_indexado_nem_gera_md(self) -> None:
        modelo = self._resposta_valida_gravada()
        envio = self._gravar_variante(modelo, "retrato-quebrado",
                                      lambda d: self._pergunta(d, "proposta")["proposta"].update(colunas=[[]]))
        md = os.path.join(self.projeto.caixa, "retrato-quebrado.md")
        # em execução: a reconciliação (a de 30 s e a de antes de cada POST)
        self.s.torre.caixa.reconciliar()
        self.assertIsNone(self.s.torre.caixa.nome_de(envio))
        self.assertFalse(os.path.exists(md))
        self.assertFalse(any("unhashable" in m for _, m in self.s.torre.caixa.problemas), self.s.torre.caixa.problemas)
        estado = self.s.estado()
        problemas = [p["mensagem"] for p in estado["problemas"] if p["arquivo"] == "portal/caixa/retrato-quebrado.json"]
        self.assertEqual(len(problemas), 1, estado["problemas"])
        self.assertIn("mensagem inválida", problemas[0])
        self.assertIn("colunas", problemas[0])
        self.assertNotIn("retrato-quebrado", [c["arquivo"] for c in estado["caixa"]])
        st, _, r = self.s.post("/api/caixa", {"envio": novo_envio(), "tipo": "comentario",
                                              "alvo": {"tipo": "ticket", "id": "04"}, "texto": "ainda funciona"})
        self.assertEqual(st, 200, r)
        self.assertEqual(self.s.get("/api/caixa/" + envio)[0], 404)
        # no arranque
        self.reiniciar()
        self.assertIsNone(self.s.torre.caixa.nome_de(envio))
        self.assertFalse(os.path.exists(md))
        estado = self.s.estado()
        self.assertTrue(any(p["arquivo"] == "portal/caixa/retrato-quebrado.json" and "colunas" in p["mensagem"]
                            for p in estado["problemas"]))
        self.assertNotIn("retrato-quebrado", [c["arquivo"] for c in estado["caixa"]])
        self.assertEqual(len([f for f in self.s.get("/api/aviso")[2]["fila"] if f["arquivo"] == "retrato-quebrado"]), 0)

    def test_outras_estruturas_internas_fora_da_forma(self) -> None:
        modelo = self._resposta_valida_gravada()
        P = self._pergunta
        casos = {
            "linha-base-sem-id": lambda d: P(d, "proposta")["proposta"]["linhas"].append({"tarefa": "x"}),
            "linha-base-id-numero": lambda d: P(d, "proposta")["proposta"]["linhas"].append({"id": 7}),
            "celula-base-lista": lambda d: P(d, "proposta")["proposta"]["linhas"][0].update(tarefa=["a"]),
            "celula-base-objeto": lambda d: P(d, "proposta")["proposta"]["linhas"][0].update(quem={"x": 1}),
            "coluna-base-desconhecida": lambda d: P(d, "proposta")["proposta"]["linhas"][0].update(custo="1"),
            "pode-desconhecido": lambda d: P(d, "proposta")["proposta"].update(pode=["voar"]),
            "proposta-sem-base": lambda d: P(d, "proposta").update(proposta=None),
            "opcao-texto-solto": lambda d: P(d, "escolha").update(opcoes=["a"]),
            "opcao-sem-texto": lambda d: P(d, "escolha")["opcoes"].append({"chave": "z"}),
            "opcao-chave-numero": lambda d: P(d, "escolha")["opcoes"].append({"chave": 1, "texto": "um"}),
            "recomendada-inexistente": lambda d: P(d, "escolha").update(recomendada=["nao-existe"]),
            "recomendada-nao-lista": lambda d: P(d, "varias").update(recomendada="alface"),
            "tipo-desconhecido": lambda d: P(d, "texto").update(tipo="poema"),
            "pergunta-id-repetido": lambda d: d["rodada"]["perguntas"].append(dict(P(d, "texto"))),
            "resposta-linha-sem-id": lambda d: d["corpo"]["respostas"]["mutirao"]["linhas"].append({"valores": {}}),
            "resposta-celula-lista": lambda d: d["corpo"]["respostas"]["mutirao"]["linhas"][0]["valores"].update(tempo=[1]),
            "resposta-celula-objeto": lambda d: d["corpo"]["respostas"]["mutirao"]["linhas"][0]["valores"].update(quem={}),
            "resposta-coluna-inexistente": lambda d: d["corpo"]["respostas"]["mutirao"]["linhas"][0]["valores"].update(custo=1),
            "resposta-ativa-texto": lambda d: d["corpo"]["respostas"]["mutirao"]["linhas"][0].update(ativa="sim"),
            "resposta-linhas-objeto": lambda d: d["corpo"]["respostas"]["mutirao"].update(linhas={}),
            "resposta-escolha-texto": lambda d: d["corpo"]["respostas"]["largura"].update(escolha="media"),
            "resposta-escolha-inexistente": lambda d: d["corpo"]["respostas"]["largura"].update(escolha=["gigante"]),
            "resposta-escolha-duas": lambda d: d["corpo"]["respostas"]["largura"].update(escolha=["media", "estreita"]),
            "resposta-veredito-estranho": lambda d: d["corpo"]["respostas"]["pode-comecar"].update(veredito="talvez"),
            "resposta-comentario-lista": lambda d: d["corpo"]["respostas"]["pode-comecar"].update(comentario=["x"]),
            "resposta-texto-numero": lambda d: d["corpo"]["respostas"]["algo-mais"].update(texto=5),
            "resposta-chave-desconhecida": lambda d: d["corpo"]["respostas"]["algo-mais"].update(nota="x"),
            "resposta-pergunta-inexistente": lambda d: d["corpo"]["respostas"].update({"fantasma": {"texto": "x"}}),
            "resposta-nao-objeto": lambda d: d["corpo"]["respostas"].update({"algo-mais": "x"}),
            "respostas-lista": lambda d: d["corpo"].update(respostas=[]),
            "respostas-ausente": lambda d: d["corpo"].pop("respostas"),
        }
        envios = {nome: self._gravar_variante(modelo, nome, mudar) for nome, mudar in casos.items()}
        # uma variante íntegra (só o envio muda) continua passando: a validação não ficou estrita demais
        bom = self._gravar_variante(modelo, "retrato-integro", lambda d: None)
        self.s.torre.caixa.reconciliar()
        estado = self.s.estado()
        arquivos_com_problema = {p["arquivo"] for p in estado["problemas"]}
        na_caixa = [c["arquivo"] for c in estado["caixa"]]
        for nome, envio in envios.items():
            with self.subTest(caso=nome):
                self.assertIn(f"portal/caixa/{nome}.json", arquivos_com_problema)
                self.assertNotIn(nome, na_caixa)
                self.assertIsNone(self.s.torre.caixa.nome_de(envio))
                self.assertFalse(os.path.exists(os.path.join(self.projeto.caixa, nome + ".md")))
        self.assertEqual(self.s.torre.caixa.nome_de(bom), "retrato-integro")
        self.assertIn("retrato-integro", na_caixa)
        self.assertTrue(os.path.exists(os.path.join(self.projeto.caixa, "retrato-integro.md")))
        self.assertFalse(any("unhashable" in m or "Error" in m for _, m in self.s.torre.caixa.problemas),
                         self.s.torre.caixa.problemas)
        self.assertEqual(len(na_caixa), apoio.MENSAGENS_DA_FIXTURE + 2)  # a fixture + a resposta gravada + a íntegra

if __name__ == "__main__":
    unittest.main()
