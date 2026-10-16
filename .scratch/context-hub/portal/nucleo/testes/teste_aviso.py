"""Marco 7: o aviso ao agente (§4.3) com um ``maestri`` FALSO. Nada de rede nem de ``maestri`` real."""

from __future__ import annotations

import datetime as _dt
import io
import json
import os
import subprocess
import sys
import threading
import time
import unittest
import uuid
from unittest import mock

import apoio

import aviso as modulo_aviso
import caixa as modulo_caixa
import leitores

ENVIO_ORFAO = "c2d4e6f8-1a3b-4c5d-8e7f-9a0b1c2d3e4f"
ORFAO = "2026-10-03-090000-comentario-ticket-04-c2d4e6f8-1a3b-4c5d-8e7f-9a0b1c2d3e4f"

MAESTRI_FALSO = r'''
"""maestri falso: grava cada chamada em chamadas.jsonl e responde conforme controle.json."""
import json, os, sys, time
pasta = os.path.dirname(os.path.abspath(__file__))
sys.stdout.reconfigure(encoding="utf-8")
args = sys.argv[1:]
with open(os.path.join(pasta, "chamadas.jsonl"), "a", encoding="utf-8") as f:
    f.write(json.dumps(args, ensure_ascii=False) + "\n")
try:
    with open(os.path.join(pasta, "controle.json"), "r", encoding="utf-8") as f:
        controle = json.load(f)
except OSError:
    controle = {}
def salvar():
    with open(os.path.join(pasta, "controle.json"), "w", encoding="utf-8") as f:
        json.dump(controle, f, ensure_ascii=False)
sub = args[0] if args else ""
if sub == "check":
    if controle.get("check_codigo"):
        print("check quebrou", file=sys.stderr)
        sys.exit(controle["check_codigo"])
    try:
        with open(os.path.join(pasta, "ultima-mensagem.txt"), "r", encoding="utf-8") as f:
            ultima = f.read()
    except OSError:
        ultima = ""
    # tela no formato do Claude Code: a mensagem entregue fica no histórico, acima da caixa entre réguas
    regua = "─" * 60
    presas = int(controle.get("check_preso_vezes", 0))
    # texto preso fica só na caixa de digitação; no histórico, só depois de enviado
    if not controle.get("check_sem_historico") and presas <= 0:
        print("❯ " + ultima)
    print("● Lendo a caixa…")
    print(regua)
    if presas > 0:
        controle["check_preso_vezes"] = presas - 1
        salvar()
        print("❯ " + ultima)  # o texto parado no prompt do agente
    else:
        print("❯ ")
    print(regua)
    print("  rodapé do agente")
    sys.exit(0)
if sub == "ask":
    modo = controle.get("ask", "ok")
    if modo == "erro":
        # o ask que falha (agente inexistente) não põe nada na tela de ninguém
        print("agente desconhecido", file=sys.stderr)
        sys.exit(7)
    if "--raw" not in args:
        with open(os.path.join(pasta, "ultima-mensagem.txt"), "w", encoding="utf-8") as f:
            f.write(args[2] if len(args) > 2 else "")
    if modo == "dormir":
        time.sleep(float(controle.get("segundos", 30)))
        sys.exit(0)
    sys.exit(0)
sys.exit(0)
'''


class ComMaestriFalso(unittest.TestCase):
    """Cópia da fixture + ``maestri`` falso apontado por ``aviso.executavel`` + ambiente "de canvas"."""

    def setUp(self) -> None:
        self.tmp, self.projeto_json = apoio.copiar_horta()
        self.addCleanup(apoio.apagar, self.tmp)
        self.pasta_falso = os.path.join(self.tmp, "maestri-falso")
        os.makedirs(self.pasta_falso)
        self.falso = os.path.join(self.pasta_falso, "maestri_falso.py")
        with open(self.falso, "w", encoding="utf-8") as f:
            f.write(MAESTRI_FALSO)
        with open(self.projeto_json, "r", encoding="utf-8") as f:
            dados = json.load(f)
        dados["aviso"] = {"agente": "Agente Teste", "executavel": self.falso}
        with open(self.projeto_json, "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False)
        self.projeto = leitores.Projeto(self.projeto_json)
        self.ambiente = dict(apoio.ambiente_limpo(), MAESTRI_PIPE="\\\\.\\pipe\\falso", MAESTRI_TERMINAL_ID="t-1")
        self.controlar(ask="ok")

    def controlar(self, **controle) -> None:
        with open(os.path.join(self.pasta_falso, "controle.json"), "w", encoding="utf-8") as f:
            json.dump(controle, f)

    def chamadas(self) -> list[list[str]]:
        caminho = os.path.join(self.pasta_falso, "chamadas.jsonl")
        if not os.path.exists(caminho):
            return []
        with open(caminho, "r", encoding="utf-8") as f:
            return [json.loads(l) for l in f if l.strip()]

    def asks(self) -> list[list[str]]:
        return [c for c in self.chamadas() if c[:1] == ["ask"] and "--raw" not in c and c[2:3] != ["(enviar)"]]

    def esperar(self, condicao, segundos: float = 6.0) -> None:
        fim = time.monotonic() + segundos
        while time.monotonic() < fim:
            if condicao():
                return
            time.sleep(0.05)
        self.fail("a condição não aconteceu em %.0f s" % segundos)

    def novo_comentario(self, caixa: modulo_caixa.Caixa, texto: str = "um comentário") -> str:
        envio = str(uuid.uuid4())
        corpo = {"tipo": "comentario", "alvo": {"tipo": "ticket", "id": "04"}, "texto": texto}
        caixa.gravar({"envio": envio, "tipo": "comentario", "enviada": "2026-10-10T10:00:00-03:00",
                      "alvo": {"tipo": "ticket", "id": "04", "titulo": "Composteira"}, "ticket": "04",
                      "substitui": None, "corpo_hash": leitores.hash_corpo(corpo), "corpo": corpo})
        return envio


class Mensagem(unittest.TestCase):
    def test_formato_da_secao_4_3(self) -> None:
        texto = modulo_aviso.compor_mensagem([
            {"tipo": "resposta", "titulo": "Como ficam os canteiros", "caminho": "portal/caixa/a.md"},
            {"tipo": "comentario", "titulo": "Composteira", "caminho": "portal/caixa/b.md"},
            {"tipo": "aprovacao", "titulo": None, "caminho": "portal/caixa/c.md"},
        ])
        self.assertEqual(texto.split("\n"), [
            "Portal: 3 mensagens novas do Gustavo na caixa.",
            "- resposta: Como ficam os canteiros; portal/caixa/a.md",
            "- comentário: Composteira; portal/caixa/b.md",
            "- aprovação: sem título; portal/caixa/c.md",
            "Absorva no ticket dono e troque estado: nova por lida.",
        ])
        self.assertTrue(modulo_aviso.compor_mensagem([{"tipo": "resposta", "titulo": "x", "caminho": "y"}])
                        .startswith("Portal: 1 mensagem nova do Gustavo na caixa.\n"))


class EmissorSemThread(ComMaestriFalso):
    """``Emissor.ciclo(agora)`` passo a passo, com a hora controlada pelo teste."""

    def setUp(self) -> None:
        super().setUp()
        self.caixa = modulo_caixa.Caixa(self.projeto.caixa)  # o órfão da fixture fica pendente
        self.emissor = modulo_aviso.Emissor(self.caixa, self.projeto, self.ambiente)
        self.t0 = _dt.datetime(2026, 10, 14, 12, 0, 0).astimezone()

    def test_entregue_junta_os_pendentes_num_ask_so(self) -> None:
        segundo = self.novo_comentario(self.caixa, "segundo")
        resultado = self.emissor.ciclo(self.t0)
        self.assertIsNone(resultado["erro"])
        self.assertEqual(set(resultado["envios"]), {ENVIO_ORFAO, segundo})
        asks = self.asks()
        self.assertEqual(len(asks), 1, self.chamadas())
        self.assertEqual(asks[0][:2], ["ask", "Agente Teste"])
        mensagem = asks[0][2]
        linhas = mensagem.split("\n")
        self.assertEqual(linhas[0], "Portal: 2 mensagens novas do Gustavo na caixa.")
        self.assertEqual(linhas[-1], "Absorva no ticket dono e troque estado: nova por lida.")
        # o órfão da fixture não guardou alvo.titulo e aqui não há resolvedor: sai "ticket 04" (na torre, "Composteira")
        self.assertIn(f"- comentário: ticket 04; portal/caixa/{ORFAO}.md", linhas)
        self.assertTrue(any(segundo in l and l.startswith("- comentário: Composteira; portal/caixa/") for l in linhas))
        # depois do ask vem um check (sem texto preso: nada mais)
        self.assertEqual([c[0] for c in self.chamadas()], ["ask", "check"])
        for envio in (ENVIO_ORFAO, segundo):
            self.assertEqual(self.caixa.fila.obter(envio), {"estado": "entregue", "tentativas": 1, "ultimo_erro": None,
                                                            "proximo": None})
        self.assertIsNone(self.emissor.ciclo(self.t0))  # nada mais a mandar
        self.assertEqual(len(self.asks()), 1)

    def test_erro_vira_pendente_com_esperas_1_5_15_e_depois_falhou(self) -> None:
        self.controlar(ask="erro")
        r = self.emissor.ciclo(self.t0)
        self.assertIn("código 7", r["erro"])
        reg = self.caixa.fila.obter(ENVIO_ORFAO)
        self.assertEqual((reg["estado"], reg["tentativas"]), ("pendente", 1))
        self.assertIn("código 7", reg["ultimo_erro"])
        self.assertIn("agente desconhecido", reg["ultimo_erro"])
        self.assertEqual(reg["proximo"], (self.t0 + _dt.timedelta(minutes=1)).isoformat(timespec="seconds"))
        # antes da hora nada sai
        self.assertIsNone(self.emissor.ciclo(self.t0 + _dt.timedelta(seconds=59)))
        self.assertEqual(len(self.asks()), 1)
        t1 = self.t0 + _dt.timedelta(seconds=60)
        self.emissor.ciclo(t1)
        reg = self.caixa.fila.obter(ENVIO_ORFAO)
        self.assertEqual((reg["estado"], reg["tentativas"], reg["proximo"]),
                         ("pendente", 2, (t1 + _dt.timedelta(minutes=5)).isoformat(timespec="seconds")))
        t2 = t1 + _dt.timedelta(minutes=5)
        self.emissor.ciclo(t2)
        reg = self.caixa.fila.obter(ENVIO_ORFAO)
        self.assertEqual((reg["estado"], reg["tentativas"], reg["proximo"]),
                         ("pendente", 3, (t2 + _dt.timedelta(minutes=15)).isoformat(timespec="seconds")))
        t3 = t2 + _dt.timedelta(minutes=15)
        self.emissor.ciclo(t3)
        reg = self.caixa.fila.obter(ENVIO_ORFAO)
        self.assertEqual((reg["estado"], reg["tentativas"], reg["proximo"]), ("falhou", 4, None))
        self.assertIn("código 7", reg["ultimo_erro"])
        self.assertEqual(len(self.asks()), 4)
        self.assertIsNone(self.emissor.ciclo(t3 + _dt.timedelta(days=1)))  # falhou fica, até "tentar de novo"
        # tentar de novo volta a pendente e o próximo ciclo manda
        self.controlar(ask="ok")
        self.caixa.fila.tentar_de_novo(ENVIO_ORFAO)
        self.assertIsNone(self.emissor.ciclo(t3)["erro"])
        self.assertEqual(self.caixa.fila.estado(ENVIO_ORFAO), "entregue")

    def test_tempo_esgotado_segue_o_mesmo_caminho(self) -> None:
        # sem prova de entrega (nada na tela, .md ainda nova), o emissor espera o ask até o limite, como antes
        self.controlar(ask="dormir", segundos=20, check_sem_historico=True)
        with mock.patch.object(modulo_aviso, "TIMEOUT_ASK", 1.0):
            inicio = time.monotonic()
            r = self.emissor.ciclo(self.t0)
            self.assertLess(time.monotonic() - inicio, 10)
        self.assertIn("não respondeu em 1 s", r["erro"])
        reg = self.caixa.fila.obter(ENVIO_ORFAO)
        self.assertEqual((reg["estado"], reg["tentativas"]), ("pendente", 1))
        self.assertEqual(reg["proximo"], (self.t0 + _dt.timedelta(minutes=1)).isoformat(timespec="seconds"))
        self.assertIn("não respondeu", reg["ultimo_erro"])

    def test_texto_preso_no_check_manda_enter_uma_vez(self) -> None:
        self.controlar(ask="ok", check_preso_vezes=1)
        r = self.emissor.ciclo(self.t0)
        self.assertIsNone(r["erro"])
        chamadas = self.chamadas()
        self.assertEqual([c[0] for c in chamadas], ["ask", "check", "ask", "check"])
        self.assertEqual(chamadas[2], ["ask", "Agente Teste", "--raw", "\r"])
        self.assertEqual(len([c for c in chamadas if "--raw" in c]), 1)
        self.assertEqual(self.caixa.fila.estado(ENVIO_ORFAO), "entregue")

    def test_texto_ainda_preso_depois_do_enter_manda_enviar(self) -> None:
        self.controlar(ask="ok", check_preso_vezes=2)
        r = self.emissor.ciclo(self.t0)
        self.assertIsNone(r["erro"])
        chamadas = self.chamadas()
        self.assertEqual([c[0] for c in chamadas], ["ask", "check", "ask", "check", "ask"])
        self.assertEqual(chamadas[2][2:], ["--raw", "\r"])
        self.assertEqual(chamadas[4], ["ask", "Agente Teste", "(enviar)"])
        self.assertEqual(self.caixa.fila.estado(ENVIO_ORFAO), "entregue")

    def test_check_que_falha_e_entrega_ambigua_pendente(self) -> None:
        self.controlar(ask="ok", check_codigo=3)
        r = self.emissor.ciclo(self.t0)
        self.assertIn("ambígua", r["erro"])
        self.assertIn("código 3", r["erro"])
        reg = self.caixa.fila.obter(ENVIO_ORFAO)
        self.assertEqual((reg["estado"], reg["tentativas"]), ("pendente", 1))
        self.assertIn("ambígua", reg["ultimo_erro"])
        self.assertEqual([c[0] for c in self.chamadas()], ["ask", "check"])

    def test_pendente_ja_lido_vira_entregue_sem_ask(self) -> None:
        # ask que esgota o tempo depois de o agente absorver não pode gerar aviso repetido
        md = os.path.join(self.caixa.pasta, ORFAO + ".md")
        with open(md, "r", encoding="utf-8") as f:
            texto = f.read()
        self.assertIn("estado: nova", texto)
        with open(md, "w", encoding="utf-8") as f:
            f.write(texto.replace("estado: nova", "estado: lida", 1))
        self.assertIsNone(self.emissor.ciclo(self.t0))
        self.assertEqual(self.chamadas(), [])
        self.assertEqual(self.caixa.fila.estado(ENVIO_ORFAO), "entregue")

    def test_mensagem_entregue_no_historico_nao_e_texto_preso(self) -> None:
        # teste real de 2026-10-14: a mensagem entregue aparecia no histórico e o emissor mandava '(enviar)' à toa
        regua = "─" * 40
        historico = ["❯ Portal: 1 mensagem nova do Gustavo na caixa.", "● Lendo…"]
        tela = "\n".join(historico + [regua, "❯ ", regua, "rodapé"])
        self.assertNotIn("Portal: 1 mensagem", modulo_aviso.texto_no_prompt(tela))
        preso = "\n".join(historico + [regua, "❯ Portal: 1 mensagem nova", regua, "rodapé"])
        self.assertIn("Portal: 1 mensagem", modulo_aviso.texto_no_prompt(preso))
        # sem réguas (outro tipo de agente): só as últimas linhas contam
        sem_reguas = "\n".join(["› Portal: 1 mensagem nova"] + ["trabalho"] * 10 + ["› ", "rodapé"])
        self.assertNotIn("Portal", modulo_aviso.texto_no_prompt(sem_reguas))

    def test_canal_indisponivel_nao_marca_nada(self) -> None:
        sem_canvas = modulo_aviso.Emissor(self.caixa, self.projeto, apoio.ambiente_limpo())
        self.assertIsNone(sem_canvas.ciclo(self.t0))
        self.assertEqual(self.caixa.fila.estado(ENVIO_ORFAO), "pendente")
        self.assertEqual(self.chamadas(), [])
        os.remove(self.falso)  # executável sumiu: também não marca
        self.assertIsNone(self.emissor.ciclo(self.t0))
        self.assertEqual(self.caixa.fila.estado(ENVIO_ORFAO), "pendente")
        self.assertFalse(self.emissor.disponibilidade()["disponivel"])
        self.assertIn("não encontrado", self.emissor.disponibilidade()["motivo"])


class EntregaSemEsperarOAsk(ComMaestriFalso):
    """Incidente de 2026-10-14 23h36: o ``ask`` só volta quando o agente fica ocioso; um agente sempre ocupado
    segurava a fila e o aviso seguinte nunca saía. A entrega vale com prova (UUID na tela fora da caixa de
    digitação, ou o ``.md`` já ``lida``); o ``ask`` segue sozinho até voltar ou até ``TIMEOUT_ASK``."""

    def setUp(self) -> None:
        super().setUp()
        self.caixa = modulo_caixa.Caixa(self.projeto.caixa)  # o órfão da fixture fica pendente
        self.emissor = modulo_aviso.Emissor(self.caixa, self.projeto, self.ambiente)
        self.t0 = _dt.datetime(2026, 10, 14, 23, 32, 0).astimezone()
        for nome, valor in (("PASSO_OLHAR", 0.1), ("OLHAR_TELA_POR", 30.0)):
            p = mock.patch.object(modulo_aviso, nome, valor)
            p.start()
            self.addCleanup(p.stop)
        self.addCleanup(self.emissor.encerrar_asks)

    def test_agente_ocupado_com_prova_na_tela_nao_segura_a_fila(self) -> None:
        self.controlar(ask="dormir", segundos=30)
        inicio = time.monotonic()
        r = self.emissor.ciclo(self.t0)
        self.assertLess(time.monotonic() - inicio, 8)
        self.assertIsNone(r["erro"])
        self.assertEqual(self.caixa.fila.estado(ENVIO_ORFAO), "entregue")
        # a mensagem seguinte (a das 23h36) sai no ciclo seguinte, com o primeiro ask ainda em curso
        segundo = self.novo_comentario(self.caixa, "segundo")
        inicio = time.monotonic()
        r2 = self.emissor.ciclo(self.t0)
        self.assertLess(time.monotonic() - inicio, 8)
        self.assertEqual(r2["envios"], [segundo])
        self.assertIsNone(r2["erro"])
        self.assertEqual(len(self.asks()), 2, self.chamadas())
        self.assertEqual(self.caixa.fila.estado(segundo), "entregue")
        self.assertEqual([c for c in self.chamadas() if "--raw" in c or c[2:3] == ["(enviar)"]], [])

    def test_prova_pelo_md_lido_sem_nada_na_tela(self) -> None:
        self.controlar(ask="dormir", segundos=30, check_sem_historico=True)
        md = os.path.join(self.caixa.pasta, ORFAO + ".md")

        def ler_como_o_agente() -> None:
            time.sleep(0.6)
            with open(md, "r", encoding="utf-8") as f:
                texto = f.read()
            with open(md, "w", encoding="utf-8") as f:
                f.write(texto.replace("estado: nova", "estado: lida", 1))
        threading.Thread(target=ler_como_o_agente, daemon=True).start()
        inicio = time.monotonic()
        r = self.emissor.ciclo(self.t0)
        self.assertLess(time.monotonic() - inicio, 8)
        self.assertIsNone(r["erro"])
        self.assertEqual(self.caixa.fila.estado(ENVIO_ORFAO), "entregue")

    def test_ask_em_curso_e_encerrado_no_limite(self) -> None:
        self.controlar(ask="dormir", segundos=30)
        with mock.patch.object(modulo_aviso, "TIMEOUT_ASK", 1.5):
            r = self.emissor.ciclo(self.t0)
            self.assertIsNone(r["erro"])
            self.assertEqual(len(self.emissor.asks_em_curso()), 1)
            self.esperar(lambda: not self.emissor.asks_em_curso(), segundos=8)

    def test_parada_normal_encerra_os_asks_ja_provados(self) -> None:
        # pedido do Prumo: a thread que vigia o ask morre com o servidor; na parada normal o ask provado sai junto
        self.controlar(ask="dormir", segundos=30)
        r = self.emissor.ciclo(self.t0)
        self.assertIsNone(r["erro"])
        [processo] = self.emissor.asks_em_curso()
        self.emissor.parar()
        self.assertIsNotNone(processo.poll())
        self.assertEqual(self.emissor.asks_em_curso(), [])
        self.assertEqual(self.caixa.fila.estado(ENVIO_ORFAO), "entregue")  # encerrar não desfaz a entrega

    def test_uuid_quebrado_pela_largura_da_tela_ainda_conta(self) -> None:
        regua = "─" * 40
        tela = "\n".join(["❯ Portal: 1 mensagem nova do Gustavo na caixa.", "  - resposta: X; portal/caixa/2026-a-f67a",
                          "  c890-3cef.md", regua, "❯ ", regua, "rodapé"])
        self.assertTrue(modulo_aviso.prova_na_tela(tela, ["f67ac890-3cef-4f86-b4b6-f2a68d379c0d"]))
        self.assertFalse(modulo_aviso.prova_na_tela(tela, ["65d183a8-88c0-4d6d-994f-a2f995a583a1"]))
        presa = "\n".join(["● trabalho", regua, "❯ Portal: 1 mensagem nova; portal/caixa/x-f67ac890-3c.md", regua, "rodapé"])
        self.assertFalse(modulo_aviso.prova_na_tela(presa, ["f67ac890-3cef-4f86-b4b6-f2a68d379c0d"]))


class EmissorNoServidor(ComMaestriFalso):
    """A thread ligada à torre: arranque, acordar por POST e por "tentar de novo", dois envios em 5 s."""

    def subir(self, ambiente=None) -> apoio.ServidorDeTeste:
        s = apoio.ServidorDeTeste(self.projeto_json, ambiente=self.ambiente if ambiente is None else ambiente)
        self.addCleanup(s.parar)
        return s

    def test_reinicio_com_pendente_sai_depois_de_subir(self) -> None:
        with mock.patch.object(modulo_aviso, "INTERVALO", 0.5):
            s = self.subir()
            self.assertIsNotNone(s.torre.emissor)
            self.esperar(lambda: s.torre.caixa.fila.estado(ENVIO_ORFAO) == "entregue")
        asks = self.asks()
        self.assertEqual(len(asks), 1)
        self.assertIn(f"- comentário: Composteira; portal/caixa/{ORFAO}.md", asks[0][2])  # título pelo resolvedor da torre
        st, _, corpo = s.get("/api/aviso")
        self.assertEqual((st, corpo["disponivel"], corpo["canal"]), (200, True, "ask"))
        self.assertEqual(next(f for f in corpo["fila"] if f["envio"] == ENVIO_ORFAO)["estado"], "entregue")

    def test_tentar_de_novo_acorda_o_emissor(self) -> None:
        # três tentativas já feitas: a próxima falha vira falhou
        with open(os.path.join(self.projeto.caixa, ".avisos.json"), "w", encoding="utf-8") as f:
            json.dump({ENVIO_ORFAO: {"estado": "pendente", "tentativas": 3, "ultimo_erro": "x", "proximo": None}}, f)
        self.controlar(ask="erro")
        with mock.patch.object(modulo_aviso, "INTERVALO", 60.0):  # só um acordar move o emissor
            s = self.subir()
            self.esperar(lambda: s.torre.caixa.fila.estado(ENVIO_ORFAO) == "falhou")
            self.assertEqual(len(self.asks()), 1)
            self.controlar(ask="ok")
            time.sleep(1.0)
            self.assertEqual(len(self.asks()), 1)  # dormindo: nada sai sozinho
            st, _, corpo = s.post("/api/aviso/tentar", {"envio": ENVIO_ORFAO})
            self.assertEqual((st, corpo["estado"]), (200, "pendente"))
            self.esperar(lambda: s.torre.caixa.fila.estado(ENVIO_ORFAO) == "entregue", 5.0)
        self.assertEqual(len(self.asks()), 2)
        self.assertEqual(s.torre.caixa.fila.obter(ENVIO_ORFAO)["tentativas"], 5)

    def test_dois_envios_em_cinco_segundos_nenhum_perdido_nem_repetido(self) -> None:
        with mock.patch.object(modulo_aviso, "INTERVALO", 60.0):  # o POST acorda; o intervalo não ajuda
            s = self.subir()
            self.esperar(lambda: s.torre.caixa.fila.estado(ENVIO_ORFAO) == "entregue")
            envios = []
            for texto in ("primeiro", "segundo"):
                envio = str(uuid.uuid4())
                st, _, r = s.post("/api/caixa", {"envio": envio, "tipo": "comentario",
                                                 "alvo": {"tipo": "ticket", "id": "04"}, "texto": texto})
                self.assertEqual(st, 200, r)
                envios.append(envio)
                time.sleep(0.7)
            self.esperar(lambda: all(s.torre.caixa.fila.estado(e) == "entregue" for e in envios))
        asks = self.asks()
        self.assertIn(len(asks), (2, 3))  # o do órfão, mais um ou dois para os novos
        todas = "\n".join(a[2] for a in asks)
        for envio in envios + [ENVIO_ORFAO]:
            self.assertEqual(todas.count(envio), 1, f"{envio} apareceu {todas.count(envio)} vez(es)")
        for e in envios:
            self.assertEqual(s.torre.caixa.fila.obter(e)["tentativas"], 1)

    def test_sem_canvas_indisponivel_com_motivo_e_nada_vira_falhou(self) -> None:
        with mock.patch.object(modulo_aviso, "INTERVALO", 0.2):
            s = self.subir(ambiente=apoio.ambiente_limpo())
            self.assertIsNone(s.torre.emissor)
            st, _, corpo = s.get("/api/aviso")
            self.assertEqual((st, corpo["disponivel"]), (200, False))
            self.assertIn("fora do canvas", corpo["motivo"])
            self.assertIn("MAESTRI_PIPE", corpo["motivo"])
            self.assertEqual(s.estado()["aviso"], {"disponivel": False, "motivo": corpo["motivo"]})
            time.sleep(0.8)
            self.assertEqual(s.torre.caixa.fila.estado(ENVIO_ORFAO), "pendente")
            self.assertEqual(self.chamadas(), [])
            # executável que não existe: indisponível com o motivo, e o servidor sobe
            s.parar()
            os.remove(self.falso)
            s2 = self.subir()
            self.assertIsNone(s2.torre.emissor)
            motivo = s2.get("/api/aviso")[2]["motivo"]
            self.assertIn("não encontrado", motivo)


class Vigia(ComMaestriFalso):
    """Canal B: ``--vigiar`` imprime uma linha por pendente, marca entregue e não rouba o que está ``enviando``."""

    def test_imprime_pendentes_marca_entregue_e_respeita_enviando(self) -> None:
        caixa = modulo_caixa.Caixa(self.projeto.caixa)
        em_envio = self.novo_comentario(caixa, "em envio pelo canal A")
        caixa.fila.marcar(em_envio, "enviando")
        saida = io.StringIO()
        linhas = modulo_aviso.vigiar_uma_vez(self.projeto, saida)
        self.assertEqual(len(linhas), 1, linhas)
        self.assertEqual(saida.getvalue(), linhas[0] + "\n")
        self.assertEqual(linhas[0], f"comentário: ticket 04; portal/caixa/{ORFAO}.md; envio {ENVIO_ORFAO}")
        fila = modulo_caixa.Fila(self.projeto.caixa, threading.RLock())
        self.assertEqual(fila.estado(ENVIO_ORFAO), "entregue")
        self.assertEqual(fila.estado(em_envio), "enviando")
        # nada mais a imprimir; o que está enviando continua do canal A
        self.assertEqual(modulo_aviso.vigiar_uma_vez(self.projeto, io.StringIO()), [])
        # .md já lida: marcado entregue sem imprimir
        lida = self.novo_comentario(caixa, "já lida")
        nome = caixa.nome_de(lida)
        md = os.path.join(self.projeto.caixa, nome + ".md")
        with open(md, "r", encoding="utf-8") as f:
            texto = f.read()
        with open(md, "w", encoding="utf-8") as f:
            f.write(texto.replace("estado: nova", "estado: lida", 1))
        self.assertEqual(modulo_aviso.vigiar_uma_vez(self.projeto, io.StringIO()), [])
        self.assertEqual(modulo_caixa.Fila(self.projeto.caixa, threading.RLock()).estado(lida), "entregue")

    def test_pela_linha_de_comando(self) -> None:
        modulo_caixa.Caixa(self.projeto.caixa)  # o órfão fica pendente
        script = os.path.join(apoio.PASTA_NUCLEO, "aviso.py")
        r = subprocess.run([sys.executable, script, "--vigiar", self.projeto.pasta_portal, "--uma-vez"],
                           capture_output=True, timeout=60)
        self.assertEqual(r.returncode, 0, r.stderr)
        linhas = r.stdout.decode("utf-8").strip().splitlines()
        self.assertEqual(len(linhas), 1, linhas)
        self.assertTrue(linhas[0].startswith("comentário: ticket 04; portal/caixa/"), linhas[0])
        self.assertTrue(linhas[0].endswith(f"envio {ENVIO_ORFAO}"))
        self.assertEqual(modulo_caixa.Fila(self.projeto.caixa, threading.RLock()).estado(ENVIO_ORFAO), "entregue")
        # pasta sem projeto.json: sai com 2 e diz por quê
        r = subprocess.run([sys.executable, script, "--vigiar", self.tmp, "--uma-vez"], capture_output=True, timeout=60)
        self.assertEqual(r.returncode, 2)
        self.assertIn("projeto.json", r.stderr.decode("utf-8", errors="replace"))

    def test_laco_para_com_o_evento_e_convive_com_o_servidor(self) -> None:
        with mock.patch.object(modulo_aviso, "INTERVALO", 60.0):
            s = apoio.ServidorDeTeste(self.projeto_json, ambiente=apoio.ambiente_limpo())  # sem canal A
            self.addCleanup(s.parar)
            parar = threading.Event()
            saida = io.StringIO()
            t = threading.Thread(target=modulo_aviso.vigiar, args=(self.projeto.pasta_portal,),
                                 kwargs={"intervalo": 0.2, "saida": saida, "parar": parar}, daemon=True)
            t.start()
            self.esperar(lambda: ENVIO_ORFAO in saida.getvalue())
            envio = str(uuid.uuid4())
            st, _, r = s.post("/api/caixa", {"envio": envio, "tipo": "comentario",
                                             "alvo": {"tipo": "ticket", "id": "04"}, "texto": "com o servidor no ar"})
            self.assertEqual(st, 200, r)
            self.esperar(lambda: envio in saida.getvalue())
            parar.set()
            t.join(timeout=5)
            self.assertFalse(t.is_alive())
        self.assertEqual(len(saida.getvalue().strip().splitlines()), 2)
        self.assertEqual(s.torre.caixa.fila.estado(envio), "entregue")  # a fila em memória do servidor vê? (relida abaixo)
        self.assertEqual(modulo_caixa.Fila(self.projeto.caixa, threading.RLock()).estado(envio), "entregue")


if __name__ == "__main__":
    unittest.main()
