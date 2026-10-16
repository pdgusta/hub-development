"""Marco L2: os laços (§4.4) e o pedido ``alteracao-laco`` (§4.5) sobre uma cópia da fixture.

A fixture tem dois laços (``testes/fixtures/LEIA.md``, "Laços"): ``pesquisa-de-regas`` em voo, com SQLite, como o
A.1 da proposta, e ``censo-de-sementes`` terminado, com ``laco_final.json``, como o A.2. Nada aqui grava na pasta
de um laço pelo portal: os testes mudam as fontes por conta própria (simulando o laço ou o maestro) e conferem
que o portal só lê.
"""

from __future__ import annotations

import datetime as _dt
import hashlib
import io
import json
import os
import sqlite3
import unittest
import uuid
from unittest import mock

import apoio
from teste_aviso import ComMaestriFalso
from teste_torre import _criar_junction

import aviso as modulo_aviso
import caixa as modulo_caixa
import lacos as modulo_lacos
import leitores

EM_VOO = apoio.LACO_EM_VOO
TERMINADO = apoio.LACO_TERMINADO
EXECUCAO = "regas-2026-10-14"
PEDIDO_APLICADO = "2026-10-14-215930-alteracao-laco-pesquisa-de-regas-5b0c7e2a-3f41-4d8e-9a17-2c6e8f0b4d31"
COMENTARIO_LIDO = "2026-10-14-215930-alteracao-laco-pesquisa-de-regas-8d2f4a61-7c3b-4e95-b0a8-1f6d3c9e2a74"


def novo_envio() -> str:
    return str(uuid.uuid4())


def ler_json(caminho: str):
    with open(caminho, "r", encoding="utf-8") as f:
        return json.load(f)


def gravar_json(caminho: str, dados) -> None:
    with open(caminho, "w", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(dados, ensure_ascii=False, indent=2) + "\n")


class ComLacos(unittest.TestCase):
    """Cópia da fixture com servidor em porta livre e atalhos para mexer nas fontes dos laços."""

    def setUp(self) -> None:
        self.tmp, self.projeto_json = apoio.copiar_horta()
        self.raiz = os.path.dirname(os.path.dirname(self.projeto_json))
        self.regas = apoio.pasta_do_laco(self.raiz, "regas")
        self.sementes = apoio.pasta_do_laco(self.raiz, "sementes")
        self.projeto = leitores.Projeto(self.projeto_json)
        self.s = apoio.ServidorDeTeste(self.projeto_json)
        self.addCleanup(apoio.apagar, self.tmp)
        self.addCleanup(lambda: self.s.parar())

    # -- leitura pela API ----------------------------------------------------------------------------

    def lista(self) -> list[dict]:
        st, _, r = self.s.get("/api/lacos")
        self.assertEqual(st, 200, r)
        return r

    def linha(self, lid: str = EM_VOO) -> dict:
        return next(x for x in self.lista() if x["id"] == lid)

    def laco(self, lid: str = EM_VOO) -> dict:
        st, _, r = self.s.get(f"/api/laco/{lid}")
        self.assertEqual(st, 200, r)
        return r

    @staticmethod
    def controle(laco: dict, cid: str) -> dict:
        return next(c for c in laco["controles"] if c["id"] == cid)

    @staticmethod
    def contador(laco: dict, cid: str) -> dict:
        return next(c for c in laco["contadores"] if c["id"] == cid)

    @staticmethod
    def pedido(laco: dict, arquivo: str) -> dict:
        return next(p for p in laco["pedidos"] if p["arquivo"] == arquivo)

    def problemas_do_estado(self) -> list[dict]:
        return self.s.estado()["problemas"]

    # -- mexer nas fontes (o laço ou o maestro, nunca o portal) --------------------------------------

    def mexer_laco(self, func, pasta: str | None = None) -> None:
        caminho = os.path.join(pasta or self.regas, "laco.json")
        dados = ler_json(caminho)
        func(dados)
        gravar_json(caminho, dados)

    def mexer_config(self, **valores) -> None:
        caminho = os.path.join(self.regas, "config.json")
        dados = ler_json(caminho)
        dados.update(valores)
        gravar_json(caminho, dados)

    def banco(self, sql: str, params=()) -> None:
        con = sqlite3.connect(os.path.join(self.regas, "estado", "laco.db"))
        try:
            con.execute(sql, params)
            con.commit()
        finally:
            con.close()

    def mexer_despachante(self, **valores) -> None:
        caminho = os.path.join(self.regas, "estado", "despachante.json")
        dados = ler_json(caminho)
        dados.update(valores)
        gravar_json(caminho, dados)

    def caminho_md(self, nome: str) -> str:
        return os.path.join(self.projeto.caixa, nome + ".md")

    def desfecho(self, nome: str, **chaves) -> None:
        """O maestro grava estado e chaves de desfecho no frontmatter do ``.md`` (uma linha cada)."""
        caminho = self.caminho_md(nome)
        with open(caminho, "r", encoding="utf-8") as f:
            linhas = f.read().split("\n")
        fim = linhas.index("---", 1)
        for i in range(1, fim):
            chave = linhas[i].split(":", 1)[0]
            if chave in chaves:
                linhas[i] = f"{chave}: {chaves.pop(chave)}".rstrip()
        self.assertFalse(chaves, f"chaves que não existem no frontmatter: {chaves}")
        with open(caminho, "w", encoding="utf-8", newline="\n") as f:
            f.write("\n".join(linhas))

    # -- envio -------------------------------------------------------------------------------------------

    def corpo(self, operacao: str = "mudar-controle", lid: str = EM_VOO, **campos) -> dict:
        laco = self.laco(lid)
        corpo = {"envio": novo_envio(), "tipo": "alteracao-laco", "laco": lid, "execucao": laco["execucao"]["id"],
                 "operacao": operacao, "revisao": laco["revisao"]}
        if operacao == "mudar-controle":
            corpo.update(no="parada", controle="gate_novos", antes={"tipo": "numero", "valor": 0.1},
                         depois={"tipo": "numero", "valor": 0.2}, texto=None)
        corpo.update(campos)
        return corpo

    def enviar(self, corpo: dict, status: int = 200, codigo: str | None = None, campo: str | None = None) -> dict:
        st, _, r = self.s.post("/api/caixa", corpo)
        self.assertEqual(st, status, r)
        if codigo is not None:
            self.assertEqual(r.get("erro"), codigo, r)
        if campo is not None:
            self.assertEqual(r.get("campo"), campo, r)
        return r


# ==================================================================================================
# Leitura (§4.4)
# ==================================================================================================


class Leitura(ComLacos):
    def test_lista_dos_dois_lacos(self) -> None:
        lista = self.lista()
        self.assertEqual([x["id"] for x in lista], [EM_VOO, TERMINADO])  # a ordem do registro
        regas, sementes = lista
        self.assertEqual((regas["grupo"], regas["situacao"], regas["execucao"]), ("em-voo", "rodando", EXECUCAO))
        self.assertEqual(regas["destaque"]["rotulo"], "tentativas")
        self.assertEqual(regas["destaque"]["valor"], 1684)  # SQLite, soma
        self.assertEqual(regas["pedidos_abertos"], 1)       # o aplicado que aguarda efeito; o comentário lido não
        self.assertIsNone(regas["problema"])
        self.assertIsNotNone(regas["ultimo_sinal"]["hora"])
        self.assertEqual((sementes["grupo"], sementes["situacao"]), ("terminado", "terminado"))
        self.assertEqual(sementes["terminou_em"], "2026-10-13T15:13:09-03:00")
        self.assertEqual(sementes["destaque"]["valor"], 738)
        self.assertEqual(sementes["ultimo_sinal"]["fonte"], "estado/laco_final.json → terminou_em")

    def test_detalhe_do_laco_em_voo(self) -> None:
        laco = self.laco()
        self.assertEqual(laco["ticket"], "05")
        self.assertEqual(laco["execucao"], {"id": EXECUCAO, "inicio": "2026-10-14T20:36:47-03:00", "terminou_em": None})
        self.assertEqual(len(laco["nos"]), 8)
        self.assertEqual(len(laco["ligacoes"]), 9)
        self.assertRegex(laco["revisao"], r"^[0-9a-f]{64}$")
        self.assertEqual(laco["problemas"], [])
        gate = self.controle(laco, "gate_novos")
        self.assertEqual(gate["configurado"]["valor"], 0.1)
        self.assertEqual((gate["configurado"]["como"], gate["configurado"]["fonte"]), ("lido", "config.json → gate_novos"))
        self.assertEqual(gate["em_uso"]["estado"], "nao-confirmado")  # releitura ao-ligar: o arquivo não prova uso
        teto = self.controle(laco, "teto-tentativas")
        self.assertEqual(teto["configurado"]["valor"], 5000)
        self.assertEqual(teto["em_uso"]["estado"], "relido")          # continua, rodando, sem em_uso declarada
        self.assertIsNotNone(teto["precondicoes"]["inicio"]["valor"])
        self.assertEqual(self.controle(laco, "teto-horas")["configurado"]["valor"], 2)
        self.assertEqual(self.controle(laco, "excluir_manual")["configurado"]["valor"],
                         ["regador-antigo", "mangueira-furada"])
        modelo = self.controle(laco, "juntador-modelo")
        self.assertEqual((modelo["configurado"]["valor"], modelo["configurado"]["como"]),
                         ("claude-sonnet-5-5", "declarado"))
        self.assertEqual(self.contador(laco, "onda")["valor"], 2)
        self.assertEqual(self.contador(laco, "pedidos")["valor"], {"feito": 40, "pendente": 10, "em_voo": 3})
        self.assertEqual(len(self.contador(laco, "curva")["valor"]), 2)
        self.assertEqual(self.contador(laco, "aptos")["valor"], 12)
        self.assertEqual(_dt.datetime.fromisoformat(self.contador(laco, "aptos")["hora"]),
                         _dt.datetime.fromisoformat("2026-10-14T21:12:40-03:00"))  # a hora declarada do dado
        self.assertEqual(_dt.datetime.fromisoformat(self.contador(laco, "ultima-chamada")["valor"]),
                         _dt.datetime.fromisoformat("2026-10-14T21:11:30-03:00"))  # última linha do JSONL
        self.assertEqual(laco["capacidades"], [{"id": "parar-apos-onda", "onda_atual": 2, "onda_ilegivel": None},
                                               {"id": "parar-de-despachar"}])
        self.assertEqual(laco["parado"]["valor"], False)
        self.assertEqual((laco["cota"]["aptos"], laco["cota"]["fora"]), (12, 3))
        # os pedidos, do mais novo ao mais velho, com estado e recibo
        aplicado = self.pedido(laco, PEDIDO_APLICADO)
        self.assertEqual((aplicado["estado"], aplicado["recibo"]["valido"], aplicado["recibo"]["efeito"]),
                         ("aplicado", True, "aguarda"))
        self.assertTrue(aplicado["trabalho_pendente"])
        comentario = self.pedido(laco, COMENTARIO_LIDO)
        self.assertEqual(comentario["estado"], "lida")
        self.assertFalse(comentario["trabalho_pendente"])  # comentário lido encerra
        self.assertEqual(laco["pedidos_abertos"], 1)

    def test_laco_terminado(self) -> None:
        laco = self.laco(TERMINADO)
        self.assertEqual((laco["grupo"], laco["situacao"]), ("terminado", "terminado"))
        self.assertEqual(self.contador(laco, "ultima-taxa")["valor"], 0.1346)  # campo com índice negativo
        self.assertEqual(self.controle(laco, "teto-tentativas")["configurado"],
                         {"valor": 2000, "como": "declarado", "fonte": "declarado pelo maestro", "hora": None,
                          "ilegivel": None})
        self.assertEqual(self.controle(laco, "teto-tentativas")["em_uso"]["estado"], "nao-confirmado")
        self.assertIsNotNone(laco["parado"]["ilegivel"])  # o banco não existe: ilegível, nunca "não parado"
        self.assertEqual(laco["capacidades"][0], {"id": "parar-apos-onda", "onda_atual": None, "onda_ilegivel": None})

    def test_jsonl_vale_a_ultima_linha_valida(self) -> None:
        with open(os.path.join(self.regas, "livros", "manha.jsonl"), "a", encoding="utf-8") as f:
            f.write('{"quando": "2026-10-14T21:30:00-03:00", "modelo": "poço"}\n{"quando": cortada\n\n')
        laco = self.laco()
        self.assertEqual(_dt.datetime.fromisoformat(self.contador(laco, "ultima-chamada")["valor"]),
                         _dt.datetime.fromisoformat("2026-10-14T21:30:00-03:00"))

    def test_jsonl_sem_linha_valida_e_ilegivel(self) -> None:
        with open(os.path.join(self.regas, "livros", "manha.jsonl"), "w", encoding="utf-8") as f:
            f.write("nada de json\n")
        self.assertIn("sem valor", self.contador(self.laco(), "ultima-chamada")["ilegivel"])

    def test_arquivo_acima_de_16_mib_e_ilegivel(self) -> None:
        caminho = os.path.join(self.regas, "estado", "despachante.json")
        with open(caminho, "w", encoding="utf-8") as f:
            f.write('{"aptos": 1, "pad": "' + "x" * (16 * 1024 * 1024) + '"}')
        laco = self.laco()
        self.assertIn("16 MiB", self.contador(laco, "aptos")["ilegivel"])
        self.assertIsNotNone(laco["cota"]["ilegivel"])
        self.assertEqual(laco["situacao"], "rodando")  # cota ilegível: a regra não vale

    def test_tipo_errado_nunca_e_convertido(self) -> None:
        self.mexer_config(trabalhadores_por_gerador="20", gate_novos=None)
        laco = self.laco()
        trab = self.controle(laco, "trabalhadores_por_gerador")["configurado"]
        self.assertIsNone(trab["valor"])
        self.assertIn("tipo errado", trab["ilegivel"])
        gate = self.controle(laco, "gate_novos")["configurado"]
        self.assertIn("nulo", gate["ilegivel"])  # null sem aceita_nulo nem ausente

    def test_sem_lacos_no_projeto_json(self) -> None:
        dados = ler_json(self.projeto_json)
        del dados["lacos"]
        gravar_json(self.projeto_json, dados)
        self.s.parar()
        self.s = apoio.ServidorDeTeste(self.projeto_json)
        self.assertEqual(self.lista(), [])
        st, _, r = self.s.get(f"/api/laco/{EM_VOO}")
        self.assertEqual((st, r["erro"]), (404, "laco-inexistente"))
        self.assertFalse(any("lacos" in p["arquivo"] for p in self.problemas_do_estado()))

    def test_registro_ausente_ou_com_entradas_ruins(self) -> None:
        caminho = os.path.join(self.projeto.pasta_portal, "lacos.json")
        os.remove(caminho)
        self.assertEqual(self.lista(), [])
        self.assertIn("portal/lacos.json", [p["arquivo"] for p in self.problemas_do_estado()])
        gravar_json(caminho, [
            {"id": EM_VOO, "pasta": "lacos/regas"},
            {"id": EM_VOO, "pasta": "lacos/sementes"},      # id repetido: vale o primeiro
            {"id": "Maiúsculo", "pasta": "lacos/regas"},     # id fora do formato: ignorado
            {"id": "fora", "pasta": "../fora"},              # sai da raiz: aparece malformado
            {"id": "no-portal", "pasta": "portal"},          # é a pasta do portal: malformado
        ])
        lista = self.lista()
        self.assertEqual([x["id"] for x in lista], [EM_VOO, "fora", "no-portal"])
        self.assertIsNotNone(lista[1]["problema"])
        self.assertIn("pasta do portal", lista[2]["problema"])
        st, _, r = self.s.get("/api/laco/fora")
        self.assertEqual((st, r["erro"]), (422, "laco-malformado"))
        mensagens = [p["mensagem"] for p in self.problemas_do_estado() if p["arquivo"] == "portal/lacos.json"]
        self.assertEqual(len(mensagens), 4, mensagens)

    def test_laco_inexistente_404(self) -> None:
        for rota in ("/api/laco/nada", "/api/laco/..%2fportal", "/api/laco/MAIUSCULO"):
            st, _, r = self.s.get(rota)
            self.assertEqual((st, r["erro"]), (404, "laco-inexistente"), rota)

    def test_lacos_nao_entram_no_estado(self) -> None:
        estado = self.s.estado()
        self.assertNotIn("lacos", estado)
        tipos = [c["tipo"] for c in estado["caixa"]]
        self.assertEqual(tipos.count("alteracao-laco"), 2)  # os pedidos aparecem na caixa como as outras mensagens


class Versao(ComLacos):
    def versao(self) -> str:
        return self.s.get("/api/versao")[2]["versao"]

    def test_versao_ve_so_descritores_e_registro(self) -> None:
        v0 = self.versao()
        # fontes de estado mudam a cada segundo e não entram
        self.banco("UPDATE uso SET tentativas = tentativas + 1")
        self.mexer_despachante(aptos=11)
        self.mexer_config(gate_novos=0.12)
        apoio.avivar_laco(self.raiz, idade_s=5)
        self.assertEqual(self.versao(), v0)
        # o laco.json (desenho) e o registro entram
        self.mexer_laco(lambda d: d.update(titulo="Pesquisa de regas, v2"))
        v1 = self.versao()
        self.assertNotEqual(v1, v0)
        caminho = os.path.join(self.projeto.pasta_portal, "lacos.json")
        gravar_json(caminho, list(reversed(ler_json(caminho))))
        self.assertNotEqual(self.versao(), v1)


# ==================================================================================================
# Situação e grupo (§4.4, §3.4)
# ==================================================================================================


class SituacaoEGrupo(ComLacos):
    def test_parado(self) -> None:
        self.banco("UPDATE controle SET valor = 'true' WHERE chave = 'parar'")
        self.assertEqual(self.linha()["situacao"], "parado")

    def test_terminado_vence_parado(self) -> None:
        self.banco("UPDATE controle SET valor = 'true' WHERE chave = 'parar'")
        self.mexer_laco(lambda d: d["execucao"].update(terminou_em="2026-10-14T23:00:00-03:00"))
        self.assertEqual((self.linha()["situacao"], self.linha()["grupo"]), ("terminado", "terminado"))

    def test_sem_sinal(self) -> None:
        apoio.avivar_laco(self.raiz, idade_s=3600)
        self.mexer_despachante(gerado_em="2026-01-01T00:00:00-03:00")
        os.utime(os.path.join(self.regas, "estado", "despachante.json"), None)
        self.assertEqual(self.linha()["situacao"], "sem-sinal")

    def test_desconhecido_sem_nenhuma_fonte_de_sinal(self) -> None:
        for nome in ("manha.jsonl", "tarde.jsonl"):
            os.remove(os.path.join(self.regas, "livros", nome))
        os.remove(os.path.join(self.regas, "estado", "despachante.json"))
        linha = self.linha()
        self.assertEqual(linha["situacao"], "desconhecido")
        self.assertIsNone(linha["ultimo_sinal"])

    def test_esperando_cota(self) -> None:
        self.mexer_despachante(aptos=0, fora_agora=0)
        self.assertEqual(self.linha()["situacao"], "esperando-cota")
        self.mexer_despachante(aptos=5, fora_agora=5)
        self.assertEqual(self.linha()["situacao"], "esperando-cota")
        self.mexer_despachante(aptos=5, fora_agora=4)
        self.assertEqual(self.linha()["situacao"], "rodando")
        self.mexer_despachante(aptos=0, fora_agora="muitos")  # fora ilegível: a regra não vale
        laco = self.laco()
        self.assertEqual(laco["situacao"], "rodando")
        self.assertIn("fora", laco["cota"]["ilegivel"])

    def test_teto_relido_so_enquanto_rodando(self) -> None:
        apoio.avivar_laco(self.raiz, idade_s=3600)
        self.mexer_despachante(gerado_em="2026-01-01T00:00:00-03:00")
        self.assertEqual(self.controle(self.laco(), "teto-tentativas")["em_uso"]["estado"], "nao-confirmado")

    # -- critério do L2: rodada respondida na versão atual × reescrita --------------------------------------

    def _rodada(self, ticket: str = "05", nome: str = "2026-10-14-horario-de-rega-r1") -> str:
        caminho = os.path.join(self.projeto.rodadas, nome + ".md")
        with open(caminho, "w", encoding="utf-8", newline="\n") as f:
            f.write(f"---\ntitulo: Que horas regar\nticket: {ticket}\naberta: 2026-10-14\nestado: aberta\n---\n\n"
                    "Contexto curto.\n\n## Algo mais?\nid: algo-mais\ntipo: texto\n")
        return nome

    def test_rodada_aberta_poe_espera_voce_e_respondida_tira(self) -> None:
        rid = self._rodada()
        self.assertEqual(self.linha()["grupo"], "espera-voce")
        rodada = next(r for r in self.s.estado()["rodadas"] if r["id"] == rid)
        self.enviar({"envio": novo_envio(), "tipo": "resposta", "rodada": rid, "base": rodada["base"],
                     "respostas": {"algo-mais": {"texto": "de manhã cedo"}}})
        self.assertEqual(self.linha()["grupo"], "em-voo")  # respondida na versão atual
        # o maestro reescreve a rodada depois da resposta: volta a esperar
        with open(os.path.join(self.projeto.rodadas, rid + ".md"), "a", encoding="utf-8") as f:
            f.write("\nUma linha nova do maestro.\n")
        self.assertEqual(self.linha()["grupo"], "espera-voce")

    def test_rodada_malformada_ou_de_laco_terminado_nao_espera(self) -> None:
        caminho = os.path.join(self.projeto.rodadas, self._rodada() + ".md")
        with open(caminho, "w", encoding="utf-8") as f:
            f.write("---\ntitulo: x\nticket: 05\naberta: 2026-10-14\nestado: aberta\n---\n\n## Sem id\ntipo: texto\n")
        self.assertEqual(self.linha()["grupo"], "em-voo")
        self._rodada(ticket="10", nome="2026-10-14-colheita-r1")
        self.assertEqual(self.linha(TERMINADO)["grupo"], "terminado")  # terminado nunca "espera você"

    # -- critério do L2: conflito atual × substituído, de execução anterior, de laço terminado -------------

    def _conflito(self) -> str:
        r = self.enviar(self.corpo())
        self.desfecho(r["arquivo"], estado="conflito", agora_esta='{"tipo": "numero", "valor": 0.12}')
        return r["arquivo"]

    def test_conflito_atual_poe_espera_voce(self) -> None:
        nome = self._conflito()
        self.assertEqual(self.linha()["grupo"], "espera-voce")
        pedido = self.pedido(self.laco(), nome)
        self.assertEqual((pedido["estado"], pedido["recibo"]["valido"]), ("conflito", True))
        self.assertEqual(pedido["recibo"]["agora_esta"], {"tipo": "numero", "valor": 0.12})

    def test_conflito_substituido_nao_espera(self) -> None:
        nome = self._conflito()
        r = self.enviar(self.corpo(substitui=nome, depois={"tipo": "numero", "valor": 0.25}))
        self.assertEqual(self.linha()["grupo"], "em-voo")
        laco = self.laco()
        self.assertEqual(self.pedido(laco, nome)["substituido_por"], r["arquivo"])
        self.assertEqual(self.pedido(laco, r["arquivo"])["substitui"], nome)  # os dois ficam no histórico

    def test_conflito_de_execucao_anterior_nao_espera(self) -> None:
        self._conflito()
        self.mexer_laco(lambda d: d["execucao"].update(id="regas-2026-10-15"))
        linha = self.linha()
        self.assertEqual(linha["grupo"], "em-voo")
        self.assertEqual(linha["pedidos_abertos"], 0)  # os pedidos são da execução anterior

    def test_conflito_de_laco_terminado_nao_espera(self) -> None:
        self._conflito()
        self.mexer_laco(lambda d: d["execucao"].update(terminou_em="2026-10-14T23:00:00-03:00"))
        self.assertEqual(self.linha()["grupo"], "terminado")


# ==================================================================================================
# Revisão (§4.4)
# ==================================================================================================


class Revisao(ComLacos):
    def test_regravar_o_teto_so_com_inicio_novo_muda_a_revisao(self) -> None:
        r0 = self.laco()["revisao"]
        self.banco("UPDATE controle SET valor = ? WHERE chave = 'teto'",
                   (json.dumps({"pedidos": 5000, "horas": 2, "inicio": 1792030000.0}),))
        laco = self.laco()
        self.assertEqual(self.controle(laco, "teto-tentativas")["configurado"]["valor"], 5000)  # o mesmo número
        self.assertNotEqual(laco["revisao"], r0)

    def test_mudar_a_faixa_muda_a_revisao(self) -> None:
        r0 = self.laco()["revisao"]
        self.mexer_laco(lambda d: d["controles"][0].update(faixa=[0.01, 0.4]))
        self.assertNotEqual(self.laco()["revisao"], r0)

    def test_mudar_valor_ou_capacidade_muda_a_revisao(self) -> None:
        r0 = self.laco()["revisao"]
        self.mexer_config(trabalhadores_por_gerador=21)
        r1 = self.laco()["revisao"]
        self.assertNotEqual(r1, r0)
        self.mexer_laco(lambda d: d.update(capacidades=[{"id": "parar-de-despachar"}]))
        self.assertNotEqual(self.laco()["revisao"], r1)

    def test_contadores_sinal_e_textos_nao_mudam_a_revisao(self) -> None:
        r0 = self.laco()["revisao"]
        self.banco("UPDATE uso SET tentativas = tentativas + 50")
        self.mexer_despachante(aptos=3, gerado_em="2026-10-14T22:00:00-03:00")
        apoio.avivar_laco(self.raiz, idade_s=10)

        def textos(d):
            d["titulo"] = "outro título"
            d["controles"][0]["rotulo"] = "outro rótulo"
            d["nos"][0]["detalhe"] = "outro detalhe"
            d["controles"][1]["nulo"] = "à vontade"
        self.mexer_laco(textos)
        self.assertEqual(self.laco()["revisao"], r0)

    def test_revisao_igual_ao_calculo_da_spec(self) -> None:
        laco = self.laco()
        bruto = ler_json(os.path.join(self.regas, "laco.json"))
        chaves = modulo_lacos.CHAVES_DA_DEFINICAO
        r = {"laco": EM_VOO, "execucao": EXECUCAO, "capacidades": bruto["capacidades"], "controles": {}}
        for c in bruto["controles"]:
            api = self.controle(laco, c["id"])
            r["controles"][c["id"]] = {
                "definicao": {k: c[k] for k in chaves if k in c},
                "configurado": api["configurado"]["valor"],
                "precondicoes": {n: p["valor"] for n, p in api["precondicoes"].items()},
            }
        esperado = hashlib.sha256(json.dumps(r, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()
        self.assertEqual(laco["revisao"], esperado)


# ==================================================================================================
# Origens: SQLite e precedência (§4.4)
# ==================================================================================================


class Origens(ComLacos):
    def test_sqlite_duas_linhas_e_ilegivel(self) -> None:
        self.banco("INSERT INTO controle VALUES ('teto', ?)", (json.dumps({"pedidos": 1, "horas": 1, "inicio": 1}),))
        laco = self.laco()
        teto = self.controle(laco, "teto-tentativas")["configurado"]
        self.assertIsNone(teto["valor"])
        self.assertIn("mais de uma linha", teto["ilegivel"])
        corpo = self.corpo(no="teto", controle="teto-tentativas", antes={"tipo": "inteiro", "valor": 5000},
                           depois={"tipo": "inteiro", "valor": 6000})
        self.enviar(corpo, 409, "configurado-ilegivel")

    def test_sqlite_sem_linha_com_ausente_vale_o_ausente(self) -> None:
        self.banco("DELETE FROM controle WHERE chave = 'teto'")
        laco = self.laco()
        teto = self.controle(laco, "teto-tentativas")
        self.assertEqual((teto["configurado"]["valor"], teto["configurado"]["ilegivel"]), (None, None))
        self.assertEqual(teto["precondicoes"]["inicio"]["valor"], None)
        self.assertIsNone(teto["precondicoes"]["inicio"]["ilegivel"])

    def test_sqlite_sem_linha_sem_ausente_e_ilegivel(self) -> None:
        self.banco("DELETE FROM controle WHERE chave = 'onda'")
        laco = self.laco()
        self.assertIn("sem valor", self.contador(laco, "onda")["ilegivel"])
        cap = laco["capacidades"][0]
        self.assertEqual(cap["onda_atual"], None)
        self.assertIsNotNone(cap["onda_ilegivel"])
        # com a onda em curso ilegível o servidor não inventa onda para comparar
        self.enviar(self.corpo("pedir-parada", capacidade="parar-apos-onda", onda=1, texto=None))

    def test_sqlite_null(self) -> None:
        # null num controle que aceita nulo: vale; num contador sem ausente: ilegível
        self.banco("UPDATE controle SET valor = ? WHERE chave = 'teto'",
                   (json.dumps({"pedidos": None, "horas": 2, "inicio": 1792021007.69}),))
        self.banco("UPDATE controle SET valor = 'null' WHERE chave = 'onda'")
        self.banco("UPDATE controle SET valor = NULL WHERE chave = 'parar'")
        laco = self.laco()
        teto = self.controle(laco, "teto-tentativas")["configurado"]
        self.assertEqual((teto["valor"], teto["ilegivel"]), (None, None))
        self.assertIn("nulo", self.contador(laco, "onda")["ilegivel"])
        self.assertIsNotNone(laco["parado"]["ilegivel"])   # NULL não é "não parado"
        self.assertEqual(laco["situacao"], "rodando")       # e a regra "parado" não vale

    def test_banco_ausente_e_tabela_ausente(self) -> None:
        self.banco("DROP TABLE uso")
        self.assertIn("no such table", self.contador(self.laco(), "tentativas")["ilegivel"])
        os.remove(os.path.join(self.regas, "estado", "laco.db"))
        laco = self.laco()
        self.assertIn("não existe", self.contador(laco, "tentativas")["ilegivel"])
        self.assertIsNotNone(self.controle(laco, "teto-tentativas")["configurado"]["ilegivel"])

    def test_sqlite_aberto_so_para_leitura(self) -> None:
        banco = os.path.join(self.regas, "estado", "laco.db")
        with open(banco, "rb") as f:
            antes = f.read()
        chamadas = []
        original = sqlite3.connect

        def espiar(*args, **kw):
            chamadas.append((args, kw))
            return original(*args, **kw)
        with mock.patch.object(modulo_lacos.sqlite3, "connect", side_effect=espiar):
            laco = self.laco()
        self.assertTrue(chamadas)
        for args, kw in chamadas:
            self.assertTrue(args[0].startswith("file:") and args[0].endswith("?mode=ro"), args[0])
            self.assertNotIn("immutable", args[0])
            self.assertEqual((kw.get("uri"), kw.get("timeout")), (True, 2))
        self.assertEqual(self.contador(laco, "tentativas")["valor"], 1684)
        with open(banco, "rb") as f:
            self.assertEqual(f.read(), antes)
        self.assertEqual(sorted(os.listdir(os.path.dirname(banco))), ["despachante.json", "laco.db"])

    def test_hora_do_sqlite_considera_o_wal(self) -> None:
        banco = os.path.join(self.regas, "estado", "laco.db")
        os.utime(banco, (1_700_000_000, 1_700_000_000))
        laco = self.laco()
        self.assertTrue(self.contador(laco, "tentativas")["hora"].startswith("2023-11-1"))
        wal = banco + "-wal"
        with open(wal, "wb"):
            pass  # um -wal vazio mais novo que o banco: a hora da leitura é a dele
        self.addCleanup(lambda: os.path.exists(wal) and os.remove(wal))
        hora = self.contador(self.laco(), "tentativas")["hora"]
        self.assertGreater(_dt.datetime.fromisoformat(hora), _dt.datetime(2024, 1, 1).astimezone())


# ==================================================================================================
# Segurança e laço malformado (§4.4)
# ==================================================================================================


class Seguranca(ComLacos):
    def _malformar(self, func) -> dict:
        self.mexer_laco(func)
        st, _, r = self.s.get(f"/api/laco/{EM_VOO}")
        self.assertEqual((st, r.get("erro")), (422, "laco-malformado"), r)
        linha = self.linha()
        self.assertIsNotNone(linha["problema"])
        self.assertIsNone(linha["destaque"])
        self.assertIn("lacos/regas/laco.json", [p["arquivo"] for p in self.problemas_do_estado()])
        return linha

    def test_caminhos_fora_da_pasta_do_laco_tornam_malformado(self) -> None:
        original = ler_json(os.path.join(self.regas, "laco.json"))
        for ruim in ("../fora.json", "C:/Windows/win.ini", "/etc/passwd", "\\\\servidor\\x.json", "estado/../config.json",
                     ".oculto/x.json", "estado//despachante.json", "c:config.json"):
            with self.subTest(caminho=ruim):
                gravar_json(os.path.join(self.regas, "laco.json"), original)
                linha = self._malformar(lambda d: d["controles"][0]["configurado"].update(arquivo=ruim))
                self.assertIn("pasta do laço", linha["problema"])

    def test_atalho_para_fora_nao_e_lido(self) -> None:
        fora = os.path.join(self.tmp, "fora")
        os.makedirs(fora)
        gravar_json(os.path.join(fora, "config.json"), {"gate_novos": 0.33})
        atalho = os.path.join(self.regas, "atalho")
        if not _criar_junction(atalho, fora):
            self.skipTest("não deu para criar junction nem symlink nesta máquina")
        self.mexer_laco(lambda d: d["controles"][0]["configurado"].update(arquivo="atalho/config.json"))
        laco = self.laco()
        gate = self.controle(laco, "gate_novos")["configurado"]
        self.assertIsNone(gate["valor"])
        self.assertIn("fora da pasta do laço", gate["ilegivel"])
        self.assertTrue(any("atalho/config.json" in p["mensagem"] for p in laco["problemas"]), laco["problemas"])
        self.assertNotIn("0.33", json.dumps(laco))

    def test_laco_json_atalho_para_fora_e_malformado(self) -> None:
        fora = os.path.join(self.tmp, "fora-laco")
        os.makedirs(fora)
        os.replace(os.path.join(self.regas, "laco.json"), os.path.join(fora, "laco.json"))
        try:
            os.symlink(os.path.join(fora, "laco.json"), os.path.join(self.regas, "laco.json"))
        except (OSError, NotImplementedError):
            self.skipTest("não deu para criar symlink de arquivo nesta máquina")
        st, _, r = self.s.get(f"/api/laco/{EM_VOO}")
        self.assertEqual((st, r["erro"]), (422, "laco-malformado"))

    def test_malformados(self) -> None:
        original = ler_json(os.path.join(self.regas, "laco.json"))
        casos = {
            "formato 2": lambda d: d.update(formato=2),
            "sem execucao": lambda d: d.pop("execucao"),
            "id diferente do registro": lambda d: d.update(id="outro-laco"),
            "papel desconhecido": lambda d: d["nos"][0].update(papel="chefe"),
            "nó repetido": lambda d: d["nos"].append(dict(d["nos"][0])),
            "ligação para nó inexistente": lambda d: d["ligacoes"][0].update(para="lugar-nenhum"),
            "controle em nó inexistente": lambda d: d["controles"][0].update(no="lugar-nenhum"),
            "faixa invertida": lambda d: d["controles"][0].update(faixa=[0.5, 0.01]),
            "escolha sem opções": lambda d: d["controles"][7].update(opcoes=[]),
            "lista sem itens": lambda d: d["controles"][6].pop("itens"),
            "tipo desconhecido": lambda d: d["controles"][0].update(tipo="porcentagem"),
            "duração sem unidade": lambda d: d["controles"][2].pop("unidade"),
            "tabela SQLite com aspas": lambda d: d["contadores"][0]["origem"].update(tabela='uso"; DROP TABLE uso; --'),
            "origem com duas formas": lambda d: d["contadores"][0]["origem"].update(arquivo="x.json"),
            "declarado num contador": lambda d: d["contadores"].__setitem__(0, dict(d["contadores"][0],
                                                                                    origem={"declarado": 1})),
            "onda_atual sem contador": lambda d: d["capacidades"][0].update(onda_atual="nada"),
        }
        for nome, func in casos.items():
            with self.subTest(caso=nome):
                gravar_json(os.path.join(self.regas, "laco.json"), original)
                self._malformar(func)
        # o banco nunca foi tocado pela tabela "injetada"
        gravar_json(os.path.join(self.regas, "laco.json"), original)
        self.assertEqual(self.contador(self.laco(), "tentativas")["valor"], 1684)

    def test_laco_json_ilegivel(self) -> None:
        with open(os.path.join(self.regas, "laco.json"), "wb") as f:
            f.write(b'{"formato": 1, "titulo": "\xff"}')
        st, _, r = self.s.get(f"/api/laco/{EM_VOO}")
        self.assertEqual((st, r["erro"]), (422, "laco-malformado"))
        self.assertIn("UTF-8", self.linha()["problema"])
        os.remove(os.path.join(self.regas, "laco.json"))
        self.assertIn("não tem laco.json", self.linha()["problema"])

    def test_chave_desconhecida_vira_problema_sem_malformar(self) -> None:
        self.mexer_laco(lambda d: (d.update(extra=1), d["nos"][0].update(cor="azul"),
                                   d["capacidades"].append({"id": "voar"})))
        laco = self.laco()
        mensagens = [p["mensagem"] for p in laco["problemas"]]
        self.assertTrue(any("extra" in m for m in mensagens), mensagens)
        self.assertTrue(any("cor" in m for m in mensagens), mensagens)
        self.assertTrue(any("voar" in m for m in mensagens), mensagens)
        self.assertEqual([c["id"] for c in laco["capacidades"]], ["parar-apos-onda", "parar-de-despachar"])
        estado = [p["mensagem"] for p in self.problemas_do_estado() if p["arquivo"] == "lacos/regas/laco.json"]
        self.assertEqual(len(estado), 3, estado)

    def test_portal_nunca_grava_na_pasta_do_laco(self) -> None:
        def retrato() -> dict:
            saida = {}
            for raiz, _, nomes in os.walk(os.path.join(self.raiz, "lacos")):
                for nome in nomes:
                    caminho = os.path.join(raiz, nome)
                    with open(caminho, "rb") as f:
                        saida[caminho] = (os.stat(caminho).st_mtime_ns, hashlib.sha256(f.read()).hexdigest())
            return saida
        antes = retrato()
        self.lista()
        self.laco()
        self.laco(TERMINADO)
        self.s.estado()
        self.s.get("/api/versao")
        self.enviar(self.corpo())
        self.enviar(self.corpo("pedir-parada", capacidade="parar-de-despachar"))
        self.enviar(self.corpo("comentario-laco", texto="tudo certo"))
        self.enviar(self.corpo(revisao="0" * 64), 409, "laco-mudou")
        self.s.parar()
        self.s = apoio.ServidorDeTeste(self.projeto_json)  # reconciliação do arranque
        self.lista()
        self.assertEqual(retrato(), antes)

    def test_fontes_do_laco_nao_sao_servidas_por_carta(self) -> None:
        with open(os.path.join(self.raiz, "indice.html"), "w", encoding="utf-8") as f:
            f.write("<p>índice</p>")
        painel = os.path.join(self.regas, "painel")
        os.makedirs(painel)
        with open(os.path.join(painel, "index.html"), "w", encoding="utf-8") as f:
            f.write("<p>painel</p>")
        caminho = self.projeto.cartas_json
        cartas = ler_json(caminho)
        cartas += [
            {"id": "raiz", "titulo": "Raiz", "arquivo": "indice.html", "pasta": ".", "proposito": "x", "ticket": None,
             "decisao": "x", "data": {"valor": None, "tipo": "modificado"}, "situacao": "vigente", "mestra": False},
            {"id": "painel-regas", "titulo": "Painel", "arquivo": "lacos/regas/painel/index.html",
             "pasta": "lacos/regas/painel", "proposito": "x", "ticket": None, "decisao": "x",
             "data": {"valor": None, "tipo": "modificado"}, "situacao": "vigente", "mestra": False},
        ]
        gravar_json(caminho, cartas)
        self.assertEqual(self.s.get("/carta/raiz/")[0], 200)
        for rota in ("/carta/raiz/lacos/regas/config.json", "/carta/raiz/lacos/regas/laco.json",
                     "/carta/raiz/lacos/sementes/estado/laco_final.json"):
            self.assertEqual(self.s.get(rota)[0], 404, rota)
        self.assertEqual(self.s.get("/carta/painel-regas/")[0], 200)  # a carta cuja pasta fica dentro do laço


class PainelDoLaco(ComLacos):
    """Achado 1 do Prumo (L2): carta-painel serve a apresentação, nunca fonte, descritor, banco ou config."""

    def registrar_carta(self, cid: str, arquivo: str, pasta: str) -> None:
        caminho = self.projeto.cartas_json
        cartas = ler_json(caminho)
        cartas.append({"id": cid, "titulo": cid, "arquivo": arquivo, "pasta": pasta, "proposito": "x", "ticket": None,
                       "decisao": "x", "data": {"valor": None, "tipo": "modificado"}, "situacao": "vigente",
                       "mestra": False})
        gravar_json(caminho, cartas)

    def escrever(self, relativo: str, texto: str) -> None:
        caminho = os.path.join(self.regas, *relativo.split("/"))
        os.makedirs(os.path.dirname(caminho), exist_ok=True)
        with open(caminho, "w", encoding="utf-8") as f:
            f.write(texto)

    def montar_painel(self) -> None:
        self.escrever("painel/index.html", "<p>painel</p>")
        self.escrever("painel/estilo.css", "p{}")
        self.escrever("painel/dados.js", "window.DADOS={}")       # gerado pelo atualizador: apresentação
        self.escrever("painel/resumo.json", '{"ondas": 2}')       # json de apresentação, não declarado como fonte
        self.escrever("painel/fontes/letra.woff2", "x")
        self.registrar_carta("painel-regas", "lacos/regas/painel/index.html", "lacos/regas/painel")

    def status(self, rota: str) -> int:
        return self.s.get(rota)[0]

    def test_painel_na_raiz_do_laco_nao_serve_nada_de_dentro(self) -> None:
        """O caso do Prumo: pasta = raiz do laço liberava /config.json com gate_novos."""
        self.escrever("painel.html", "<p>painel</p>")
        self.registrar_carta("painel-raiz", "lacos/regas/painel.html", "lacos/regas")
        for rota in ("/carta/painel-raiz/", "/carta/painel-raiz/painel.html", "/carta/painel-raiz/config.json",
                     "/carta/painel-raiz/laco.json", "/carta/painel-raiz/estado/despachante.json"):
            st, _, corpo = self.s.get(rota)
            self.assertEqual(st, 404, rota)
            self.assertNotIn("gate_novos", json.dumps(corpo) if isinstance(corpo, dict) else corpo.decode("utf-8"))

    def test_painel_em_subpasta_serve_a_apresentacao_e_nada_mais(self) -> None:
        self.montar_painel()
        for rota in ("/carta/painel-regas/", "/carta/painel-regas/estilo.css", "/carta/painel-regas/dados.js",
                     "/carta/painel-regas/resumo.json", "/carta/painel-regas/fontes/letra.woff2"):
            self.assertEqual(self.status(rota), 200, rota)
        for rota in ("/carta/painel-regas/config.json", "/carta/painel-regas/laco.json",
                     "/carta/painel-regas/../config.json", "/carta/painel-regas/%2e%2e/config.json",
                     "/carta/painel-regas/%2e%2e/laco.json", "/carta/painel-regas/%2e%2e/estado/despachante.json",
                     "/carta/painel-regas/..%5cconfig.json"):
            self.assertEqual(self.status(rota), 404, rota)

    def test_atalho_no_painel_para_uma_fonte_404(self) -> None:
        self.montar_painel()
        try:
            os.symlink(os.path.join(self.regas, "config.json"), os.path.join(self.regas, "painel", "atalho.json"))
        except (OSError, NotImplementedError):
            self.skipTest("não deu para criar symlink de arquivo nesta máquina")
        self.assertEqual(self.status("/carta/painel-regas/atalho.json"), 404)

    def test_pasta_com_fonte_declarada_nao_serve(self) -> None:
        self.montar_painel()
        # o laço passa a declarar um arquivo do painel como fonte: a pasta deixa de ser só de publicação
        self.mexer_laco(lambda d: d["contadores"].append(
            {"id": "ondas-painel", "no": "painel", "rotulo": "ondas", "tipo": "inteiro",
             "origem": {"arquivo": "painel/resumo.json", "campo": "ondas"}}))
        self.assertEqual(self.contador(self.laco(), "ondas-painel")["valor"], 2)
        for rota in ("/carta/painel-regas/", "/carta/painel-regas/resumo.json", "/carta/painel-regas/estilo.css"):
            self.assertEqual(self.status(rota), 404, rota)
        # uma carta na pasta estado/ (onde moram as fontes) também não serve nada
        self.escrever("estado/vista.html", "<p>x</p>")
        self.registrar_carta("vista-estado", "lacos/regas/estado/vista.html", "lacos/regas/estado")
        self.assertEqual(self.status("/carta/vista-estado/"), 404)
        self.assertEqual(self.status("/carta/vista-estado/despachante.json"), 404)

    def test_banco_declarado_conta_wal_e_shm(self) -> None:
        self.montar_painel()
        self.mexer_laco(lambda d: d["contadores"].append(
            {"id": "x", "no": "painel", "rotulo": "x", "tipo": "contagem",
             "origem": {"sqlite": "painel/painel.db", "tabela": "t", "contagem": True}}))
        self.assertEqual(self.status("/carta/painel-regas/"), 404)

    def test_laco_malformado_nao_serve_o_painel(self) -> None:
        self.montar_painel()
        self.mexer_laco(lambda d: d.update(formato=9))  # não se sabe mais o que é fonte
        self.assertEqual(self.status("/carta/painel-regas/"), 404)
        self.mexer_laco(lambda d: d.update(formato=1))
        self.assertEqual(self.status("/carta/painel-regas/"), 200)


class DescritorComTipoErrado(ComLacos):
    """Achado 2 do Prumo (L2): lista, objeto ou número num campo de id viram "malformado", nunca 500."""

    CAMPOS = {
        "ligacoes[0].de": lambda d, v: d["ligacoes"][0].update(de=v),
        "ligacoes[0].para": lambda d, v: d["ligacoes"][0].update(para=v),
        "nos[0].id": lambda d, v: d["nos"][0].update(id=v),
        "controles[0].id": lambda d, v: d["controles"][0].update(id=v),
        "controles[0].no": lambda d, v: d["controles"][0].update(no=v),
        "contadores[0].id": lambda d, v: d["contadores"][0].update(id=v),
        "contadores[0].no": lambda d, v: d["contadores"][0].update(no=v),
        "capacidades[0].id": lambda d, v: d["capacidades"][0].update(id=v),
        "capacidades[0].onda_atual": lambda d, v: d["capacidades"][0].update(onda_atual=v),
        "execucao.id": lambda d, v: d["execucao"].update(id=v),
        "id": lambda d, v: d.update(id=v),
    }
    FORMAS = (["parada"], {"id": "parada"}, 1)  # lista, objeto, número (a varredura abaixo cobre o resto)

    def test_campos_de_id_com_forma_errada(self) -> None:
        original = ler_json(os.path.join(self.regas, "laco.json"))
        for campo, mudar in self.CAMPOS.items():
            for forma in self.FORMAS:
                with self.subTest(campo=campo, forma=forma):
                    gravar_json(os.path.join(self.regas, "laco.json"), original)
                    self.mexer_laco(lambda d: mudar(d, forma))
                    regas, sementes = self.lista()                       # 200, a lista inteira
                    self.assertIsNotNone(regas["problema"])
                    self.assertIsNone(regas["destaque"])
                    self.assertEqual((sementes["problema"], sementes["destaque"]["valor"]), (None, 738))
                    st, _, r = self.s.get(f"/api/laco/{EM_VOO}")
                    self.assertEqual((st, r["erro"]), (422, "laco-malformado"))
                    self.assertEqual(self.s.get("/api/estado")[0], 200)

    def test_toda_folha_e_todo_no_do_descritor_com_forma_errada(self) -> None:
        """Varredura: cada valor do laco.json trocado por lista, objeto, número, texto, nulo ou booleano só pode dar
        laço válido ou ``LacoMalformado``; a leitura do que passar nunca levanta outra exceção."""
        original = ler_json(os.path.join(self.regas, "laco.json"))

        def caminhos(o, pre=()):
            yield pre
            filhos = o.items() if isinstance(o, dict) else enumerate(o) if isinstance(o, list) else ()
            for k, v in filhos:
                yield from caminhos(v, pre + (k,))

        aceitos = []
        for caminho in list(caminhos(original))[1:]:
            for forma in ([], {}, 1, "x", None, True):
                dados = json.loads(json.dumps(original))
                alvo = dados
                for p in caminho[:-1]:
                    alvo = alvo[p]
                alvo[caminho[-1]] = forma
                try:
                    modulo_lacos.validar_laco(dados, EM_VOO)
                except modulo_lacos.LacoMalformado:
                    continue
                if forma in ([], {}):
                    aceitos.append(dados)
        self.assertTrue(aceitos)
        for dados in aceitos:
            gravar_json(os.path.join(self.regas, "laco.json"), dados)
            modulo_lacos.resumo_dos_lacos(self.projeto)
            modulo_lacos.detalhe_do_laco(self.projeto, EM_VOO)
            modulo_lacos.problemas_dos_lacos(self.projeto)

    def test_post_com_ids_de_forma_errada_400_com_campo(self) -> None:
        casos = [
            (dict(controle=[]), "tipo-errado", "controle"),
            (dict(controle={"id": "gate_novos"}), "tipo-errado", "controle"),
            (dict(controle=7), "tipo-errado", "controle"),
            (dict(no=["parada"]), "tipo-errado", "no"),
            (dict(no={}), "tipo-errado", "no"),
            (dict(laco=[EM_VOO]), "laco-invalido", "laco"),
            (dict(execucao={}), "execucao-invalida", "execucao"),
            (dict(operacao=["mudar-controle"]), "operacao-invalida", "operacao"),
            (dict(substitui=[]), "substitui-invalido", "substitui"),
        ]
        for campos, codigo, campo in casos:
            with self.subTest(campos=campos):
                self.enviar(self.corpo(**campos), 400, codigo, campo)
        for no in ([], ["geradores"], {}, 3):
            with self.subTest(comentario_no=no):
                self.enviar(self.corpo("comentario-no", no=no, texto="oi"), 400, "tipo-errado", "no")
        for capacidade in ([], {}, 1):
            with self.subTest(capacidade=capacidade):
                self.enviar(self.corpo("pedir-parada", capacidade=capacidade), 400, "capacidade-invalida", "capacidade")
        self.enviar(self.corpo("pedir-parada", capacidade="parar-apos-onda", onda=[3]), 400, "onda-invalida", "onda")


# ==================================================================================================
# Envio alteracao-laco (§4.5)
# ==================================================================================================


class Envio(ComLacos):
    def test_mudar_controle_grava_json_e_md(self) -> None:
        corpo = self.corpo(texto="a curva achatou\n---\nestado: aplicado")
        r = self.enviar(corpo)
        self.assertRegex(r["arquivo"], r"^\d{4}-\d{2}-\d{2}-\d{6}-alteracao-laco-pesquisa-de-regas-" + corpo["envio"] + "$")
        dados = ler_json(os.path.join(self.projeto.caixa, r["arquivo"] + ".json"))
        self.assertEqual(dados["alvo"], {"tipo": "laco", "id": EM_VOO, "titulo": "Pesquisa de horários de rega"})
        self.assertEqual(dados["ticket"], "05")
        self.assertEqual(dados["corpo"], {k: v for k, v in corpo.items() if k != "envio"})
        retrato = dados["laco"]
        self.assertEqual(retrato["revisao"], corpo["revisao"])
        self.assertEqual(retrato["no"], {"id": "parada", "titulo": "Parada", "papel": "decisao"})
        self.assertEqual(retrato["controle"]["definicao"]["configurado"], {"arquivo": "config.json", "campo": "gate_novos"})
        self.assertEqual(retrato["controle"]["configurado"]["valor"], 0.1)
        self.assertEqual(retrato["controle"]["em_uso"]["estado"], "nao-confirmado")
        with open(self.caminho_md(r["arquivo"]), "r", encoding="utf-8") as f:
            md = f.read()
        campos, corpo_md, erro = leitores.ler_frontmatter(md)
        self.assertIsNone(erro)
        self.assertEqual(campos["estado"], "nova")
        self.assertEqual((campos["laco"], campos["ticket"], campos["execucao"], campos["operacao"]),
                         (EM_VOO, "05", EXECUCAO, "mudar-controle"))
        for chave in modulo_caixa.CHAVES_DESFECHO + ("substitui",):
            self.assertEqual(campos[chave], "", chave)  # as chaves de desfecho nascem vazias
        self.assertIn('pedido: mudar "novos por onda abaixo de" (nó Parada) de 10% para 20% (configurado)', corpo_md)
        self.assertIn("onde está: config.json, chave gate_novos", corpo_md)
        self.assertIn(f"revisão vista: {corpo['revisao']}", corpo_md)
        self.assertIn("> a curva achatou\n> ---\n> estado: aplicado", corpo_md)  # texto livre nunca vira estrutura
        # aparece na caixa do estado, na fila de avisos e nos pedidos do laço
        entrada = next(c for c in self.s.estado()["caixa"] if c["envio"] == corpo["envio"])
        self.assertEqual((entrada["tipo"], entrada["estado"], entrada["aviso"]), ("alteracao-laco", "nova", "pendente"))
        laco = self.laco()
        pedido = self.pedido(laco, r["arquivo"])
        self.assertEqual((pedido["estado"], pedido["aviso"], pedido["trabalho_pendente"]), ("nova", "pendente", True))
        self.assertEqual(laco["pedidos"][0]["arquivo"], r["arquivo"])  # o mais novo primeiro
        self.assertEqual(laco["pedidos_abertos"], 2)
        # o valor do nó continua o configurado: o pedido nunca vale sozinho
        self.assertEqual(self.controle(laco, "gate_novos")["configurado"]["valor"], 0.1)

    def test_revisao_diferente_409_com_conflito_e_nada_gravado(self) -> None:
        antes = set(os.listdir(self.projeto.caixa))
        corpo = self.corpo(revisao="0" * 64)
        r = self.enviar(corpo, 409, "laco-mudou", "revisao")
        self.assertEqual(r["conflito"], {"viu": corpo["antes"], "agora": {"tipo": "numero", "valor": 0.1},
                                         "pediu": corpo["depois"], "revisao": self.laco()["revisao"],
                                         "definicao_mudou": None})  # só o hash não diz o que mudou
        self.assertEqual(set(os.listdir(self.projeto.caixa)), antes)

    def test_definicao_mudou(self) -> None:
        corpo = self.corpo(depois={"tipo": "numero", "valor": 0.45})
        self.mexer_laco(lambda d: d["controles"][0].update(faixa=[0.01, 0.3]))
        r = self.enviar(corpo, 409, "laco-mudou")
        self.assertIs(r["conflito"]["definicao_mudou"], True)  # provado: o valor pedido não cabe mais

    def test_definicao_mudou_por_tipo_e_provado(self) -> None:
        corpo = self.corpo()
        self.mexer_laco(lambda d: d["controles"][0].update(tipo="inteiro", faixa=[0, 1], escala=None) or
                        d["controles"][0].pop("escala"))
        self.mexer_config(gate_novos=0)
        self.assertIs(self.enviar(corpo, 409, "laco-mudou")["conflito"]["definicao_mudou"], True)

    def test_mudanca_compativel_da_definicao_e_desconhecida_nunca_falsa(self) -> None:
        """O caso do Prumo: só o máximo da faixa muda (0,5 → 0,49) e o pedido 0,1 → 0,2 continua permitido."""
        casos = {
            "máximo da faixa": lambda d: d["controles"][0]["faixa"].__setitem__(1, 0.49),
            "unidade": lambda d: d["controles"][0].update(unidade="das células"),
            "origem do em uso": lambda d: d["controles"][0].update(em_uso={"arquivo": "config.json",
                                                                           "campo": "gate_novos"}),
            "releitura": lambda d: d["controles"][0].update(releitura="manual"),
            "outro controle": lambda d: d["controles"][3]["faixa"].__setitem__(1, 39),
        }
        original = ler_json(os.path.join(self.regas, "laco.json"))
        for nome, mudar in casos.items():
            with self.subTest(caso=nome):
                gravar_json(os.path.join(self.regas, "laco.json"), original)
                corpo = self.corpo()
                self.mexer_laco(mudar)
                self.assertNotEqual(self.laco()["revisao"], corpo["revisao"])
                r = self.enviar(corpo, 409, "laco-mudou", "revisao")
                self.assertIn("definicao_mudou", r["conflito"])
                self.assertIsNone(r["conflito"]["definicao_mudou"], r)

    def test_antes_diferente_com_revisao_igual_e_falso_provado(self) -> None:
        # a revisão é a da página e a definição entra no hash: aqui false é provado, não inferido
        with mock.patch.object(modulo_lacos, "iguais", side_effect=lambda t, a, b: False):
            r = self.enviar(self.corpo(), 409, "laco-mudou", "antes")
        self.assertIs(r["conflito"]["definicao_mudou"], False)

    def test_outro_controle_mudou_tambem_e_conflito(self) -> None:
        corpo = self.corpo()
        self.mexer_config(trabalhadores_por_gerador=12)  # muda a revisão: o segundo pedido nunca passa sem conferência
        self.enviar(corpo, 409, "laco-mudou")

    def test_antes_diferente_do_configurado_409(self) -> None:
        r = self.enviar(self.corpo(antes={"tipo": "numero", "valor": 0.15}), 409, "laco-mudou", "antes")
        self.assertEqual(r["conflito"]["agora"], {"tipo": "numero", "valor": 0.1})

    def test_execucao_mudou_e_laco_terminou(self) -> None:
        self.enviar(self.corpo(execucao="regas-2026-10-01"), 409, "execucao-mudou", "execucao")
        self.enviar(self.corpo("comentario-laco", execucao="regas-2026-10-01", texto="oi"), 409, "execucao-mudou")
        laco = self.laco(TERMINADO)
        base = {"tipo": "alteracao-laco", "laco": TERMINADO, "execucao": laco["execucao"]["id"],
                "revisao": laco["revisao"]}
        self.enviar(dict(base, envio=novo_envio(), operacao="pedir-parada", capacidade="parar-de-despachar"),
                    409, "laco-terminou")
        self.enviar(dict(base, envio=novo_envio(), operacao="mudar-controle", no="parada", controle="gate_novos",
                         antes={"tipo": "numero", "valor": 0.05}, depois={"tipo": "numero", "valor": 0.1}),
                    409, "laco-terminou")
        self.enviar(dict(base, envio=novo_envio(), operacao="comentario-laco", texto="ótimo censo"))
        self.enviar(dict(base, envio=novo_envio(), operacao="comentario-no", no="sintese", texto="ler de novo"))

    def test_laco_fora_do_registro_e_malformado(self) -> None:
        self.enviar(self.corpo(laco="laco-que-sumiu"), 409, "laco-mudou", "laco")
        corpo = self.corpo()
        self.mexer_laco(lambda d: d.update(formato=9))
        self.enviar(corpo, 400, "laco-malformado", "laco")

    def test_validacao_400(self) -> None:
        casos = [
            (dict(operacao="voar"), "operacao-invalida", "operacao"),
            (dict(caminho="config.json"), "chave-desconhecida", "caminho"),   # o navegador só manda ids
            (dict(capacidade="parar-de-despachar"), "chave-desconhecida", "capacidade"),
            (dict(controle="nada"), "controle-inexistente", "controle"),
            (dict(no="geradores"), "no-invalido", "no"),
            (dict(depois=0.2), "valor-invalido", "depois"),
            (dict(depois={"tipo": "numero", "valor": 0.2, "extra": 1}), "valor-invalido", "depois"),
            (dict(depois={"tipo": "inteiro", "valor": 1}), "tipo-errado", "depois.tipo"),
            (dict(depois={"tipo": "numero", "valor": 0.9}), "valor-invalido", "depois.valor"),
            (dict(depois={"tipo": "numero", "valor": None}), "valor-invalido", "depois.valor"),
            (dict(depois={"tipo": "numero", "valor": "0.2"}), "valor-invalido", "depois.valor"),
            (dict(depois={"tipo": "numero", "valor": 0.1}), "nada-muda", "depois"),
            (dict(revisao="abc"), "revisao-invalida", "revisao"),
            (dict(texto="x" * 20001), "texto-longo", "texto"),
        ]
        for campos, codigo, campo in casos:
            with self.subTest(codigo=codigo, campo=campo):
                self.enviar(self.corpo(**campos), 400, codigo, campo)
        inteiro = dict(no="geradores", controle="trabalhadores_por_gerador", antes={"tipo": "inteiro", "valor": 20})
        self.enviar(self.corpo(**inteiro, depois={"tipo": "inteiro", "valor": 20.5}), 400, "valor-invalido")
        self.enviar(self.corpo(**inteiro, depois={"tipo": "inteiro", "valor": 41}), 400, "valor-invalido")
        self.enviar(self.corpo(**inteiro, depois={"tipo": "inteiro", "valor": True}), 400, "valor-invalido")
        escolha = dict(no="juntador", controle="juntador-modelo", antes={"tipo": "escolha", "valor": "claude-sonnet-5-5"})
        self.enviar(self.corpo(**escolha, depois={"tipo": "escolha", "valor": "gpt-qualquer"}), 400, "valor-invalido")
        self.enviar(self.corpo(**escolha, depois={"tipo": "escolha", "valor": "claude-opus-5-5"}))
        # comentários: texto obrigatório; nó precisa existir
        self.enviar(self.corpo("comentario-laco", texto="  "), 400, "texto-obrigatorio", "texto")
        self.enviar(self.corpo("comentario-laco"), 400, "texto-obrigatorio", "texto")
        self.enviar(self.corpo("comentario-no", no="nada", texto="oi"), 400, "no-inexistente", "no")
        # parada, pausa e retomada
        self.enviar(self.corpo("pedir-pausa"), 400, "capacidade-ausente")
        self.enviar(self.corpo("pedir-retomada"), 400, "capacidade-ausente")
        self.enviar(self.corpo("pedir-parada", capacidade="voar"), 400, "capacidade-invalida", "capacidade")
        self.enviar(self.corpo("pedir-parada", capacidade="parar-apos-onda", onda=1), 400, "onda-invalida", "onda")
        self.enviar(self.corpo("pedir-parada", capacidade="parar-apos-onda", onda=0), 400, "onda-invalida", "onda")
        self.enviar(self.corpo("pedir-parada", capacidade="parar-apos-onda"), 400, "onda-invalida", "onda")
        self.enviar(self.corpo("pedir-parada", capacidade="parar-de-despachar", onda=3), 400, "onda-invalida", "onda")
        self.mexer_laco(lambda d: d.update(capacidades=[{"id": "parar-apos-onda", "onda_atual": "onda"}]))
        self.enviar(self.corpo("pedir-parada", capacidade="parar-de-despachar"), 400, "capacidade-ausente")

    def test_lista_e_conjunto_e_nulo_quando_aceito(self) -> None:
        lista = dict(no="despachante", controle="excluir_manual",
                     antes={"tipo": "lista", "valor": ["regador-antigo", "mangueira-furada"]})
        self.enviar(self.corpo(**lista, depois={"tipo": "lista", "valor": ["mangueira-furada", "regador-antigo"]}),
                    400, "nada-muda")
        self.enviar(self.corpo(**lista, depois={"tipo": "lista", "valor": ["a", "a"]}), 400, "valor-invalido")
        self.enviar(self.corpo(**lista, depois={"tipo": "lista", "valor": ["x" * 201]}), 400, "valor-invalido")
        self.enviar(self.corpo(**lista, depois={"tipo": "lista", "valor": ["duas\nlinhas"]}), 400, "valor-invalido")
        r = self.enviar(self.corpo(**dict(lista, antes={"tipo": "lista", "valor": ["mangueira-furada",
                                                                                  "regador-antigo"]}),
                                   depois={"tipo": "lista", "valor": ["regador-antigo", "cano-novo"]}))
        with open(self.caminho_md(r["arquivo"]), "r", encoding="utf-8") as f:
            md = f.read()
        self.assertIn('adicionar "cano-novo"; remover "mangueira-furada"', md)
        teto = dict(no="teto", controle="teto-tentativas", antes={"tipo": "inteiro", "valor": 5000})
        r = self.enviar(self.corpo(**teto, depois={"tipo": "inteiro", "valor": None}))
        with open(self.caminho_md(r["arquivo"]), "r", encoding="utf-8") as f:
            md = f.read()
        self.assertIn("de 5000 tentativas para sem limite (configurado)", md)
        self.assertIn("precondição inicio:", md)

    def test_parada_e_comentarios(self) -> None:
        r = self.enviar(self.corpo("pedir-parada", capacidade="parar-apos-onda", onda=2))
        with open(self.caminho_md(r["arquivo"]), "r", encoding="utf-8") as f:
            md = f.read()
        self.assertIn("pedido: parar depois da onda 2", md)
        self.assertIn("chamadas já em voo ainda gastam cota", md)
        r = self.enviar(self.corpo("comentario-no", no="geradores", texto="testar a manhã"))
        dados = ler_json(os.path.join(self.projeto.caixa, r["arquivo"] + ".json"))
        self.assertEqual(dados["laco"]["no"]["id"], "geradores")
        self.assertNotIn("controle", dados["laco"])
        r = self.enviar(self.corpo("comentario-laco", texto="tudo certo"))
        with open(self.caminho_md(r["arquivo"]), "r", encoding="utf-8") as f:
            self.assertIn("pedido: comentário sobre o laço inteiro", f.read())

    def test_idempotencia_vem_antes_de_tudo(self) -> None:
        corpo = self.corpo()
        r1 = self.enviar(corpo)
        self.mexer_config(gate_novos=0.3)  # o laço mudou depois: o reenvio do mesmo corpo continua aceito
        r2 = self.enviar(corpo)
        self.assertEqual((r2["arquivo"], r2["repetido"]), (r1["arquivo"], True))
        self.enviar(dict(corpo, texto="outro"), 409, "envio-conflito", "envio")

    # -- critério do L2: substitui -----------------------------------------------------------------------

    def test_substitui_valido(self) -> None:
        r1 = self.enviar(self.corpo())
        r2 = self.enviar(self.corpo(substitui=r1["arquivo"], depois={"tipo": "numero", "valor": 0.3}))
        dados = ler_json(os.path.join(self.projeto.caixa, r2["arquivo"] + ".json"))
        self.assertEqual(dados["substitui"], r1["arquivo"])
        with open(self.caminho_md(r2["arquivo"]), "r", encoding="utf-8") as f:
            self.assertIn(f"substitui: {r1['arquivo']}\n", f.read())
        self.assertTrue(os.path.exists(self.caminho_md(r1["arquivo"])))  # substituir não apaga nada
        # já substituído: não aceita outro substituto
        self.enviar(self.corpo(substitui=r1["arquivo"], depois={"tipo": "numero", "valor": 0.4}),
                    400, "substitui-invalido", "substitui")
        # parada, pausa e retomada substituem umas às outras
        p1 = self.enviar(self.corpo("pedir-parada", capacidade="parar-apos-onda", onda=3))
        self.enviar(self.corpo("pedir-parada", capacidade="parar-de-despachar", substitui=p1["arquivo"]))

    def test_substitui_de_outro_laco_execucao_ou_controle_400(self) -> None:
        outro_laco = self.enviar(self.corpo("comentario-laco", lid=TERMINADO, texto="x"))
        gate = self.enviar(self.corpo())
        trabalhadores = dict(no="geradores", controle="trabalhadores_por_gerador",
                             antes={"tipo": "inteiro", "valor": 20}, depois={"tipo": "inteiro", "valor": 30})
        casos = {
            "outro laço": self.corpo(substitui=outro_laco["arquivo"]),
            "outro controle": self.corpo(**trabalhadores, substitui=gate["arquivo"]),
            "comentário substituindo": self.corpo("comentario-laco", texto="x", substitui=gate["arquivo"]),
            "parada substituindo controle": self.corpo("pedir-parada", capacidade="parar-de-despachar",
                                                       substitui=gate["arquivo"]),
            "inexistente": self.corpo(substitui="2026-01-01-000000-alteracao-laco-x-" + novo_envio()),
            "outro tipo": self.corpo(substitui=next(n[:-5] for n in os.listdir(self.projeto.caixa)
                                                    if n.endswith(".json") and "-resposta-" in n)),
        }
        for nome, corpo in casos.items():
            with self.subTest(caso=nome):
                self.enviar(corpo, 400, "substitui-invalido", "substitui")
        # outra execução: o maestro abriu uma partida nova
        self.mexer_laco(lambda d: d["execucao"].update(id="regas-2026-10-15"))
        self.enviar(self.corpo(substitui=gate["arquivo"], depois={"tipo": "numero", "valor": 0.3}),
                    400, "substitui-invalido", "substitui")

    def test_substitui_so_nova_lida_ou_conflito(self) -> None:
        self.enviar(self.corpo(substitui=PEDIDO_APLICADO, antes={"tipo": "numero", "valor": 0.1}),
                    400, "substitui-invalido", "substitui")  # já aplicado
        r = self.enviar(self.corpo())
        self.desfecho(r["arquivo"], estado="lida")
        self.enviar(self.corpo(substitui=r["arquivo"], depois={"tipo": "numero", "valor": 0.3}))


# ==================================================================================================
# Recibos e estados lidos do .md (§4.5)
# ==================================================================================================


class Recibos(ComLacos):
    def recibo(self, nome: str = PEDIDO_APLICADO) -> dict:
        return self.pedido(self.laco(), nome)["recibo"]

    def test_recibo_valido_da_fixture(self) -> None:
        recibo = self.recibo()
        self.assertEqual((recibo["valido"], recibo["erros"]), (True, []))
        self.assertEqual(recibo["depois"], {"tipo": "numero", "valor": 0.1})
        self.assertEqual(recibo["execucao"], EXECUCAO)

    def test_recibos_invalidos_nunca_valem_como_aplicado(self) -> None:
        casos = {
            "tipo errado": dict(recibo_depois='{"tipo": "inteiro", "valor": 1}'),
            "execução diferente": dict(recibo_execucao="regas-2026-10-01"),
            "depois diferente do pedido": dict(recibo_depois='{"tipo": "numero", "valor": 0.12}'),
            "antes diferente do pedido": dict(recibo_antes='{"tipo": "numero", "valor": 0.2}'),
            "aplicado antes de aplicando": dict(aplicado_em="2026-10-14T22:04:00-03:00"),
            "aplicado antes do envio": dict(aplicando_desde="", aplicado_em="2026-10-14T21:00:00-03:00"),
            "valeu antes de aplicado": dict(efeito="valeu", valeu_em="2026-10-14T22:05:00-03:00"),
            "valeu sem valeu_em": dict(efeito="valeu"),
            "aguarda com valeu_em": dict(valeu_em="2026-10-14T23:00:00-03:00"),
            "efeito desconhecido": dict(efeito="talvez"),
            "hora sem fuso": dict(aplicado_em="2026-10-14T22:05:40"),
            "revisão fora do formato": dict(recibo_revisao="abc"),
            "recibo em várias chaves faltando": dict(recibo_antes="", recibo_revisao=""),
            "JSON quebrado": dict(recibo_depois='{"tipo": "numero", "valor": '),
            "motivo longo": dict(motivo="x" * 501),
        }
        with open(self.caminho_md(PEDIDO_APLICADO), "r", encoding="utf-8") as f:
            original = f.read()
        for nome, chaves in casos.items():
            with self.subTest(caso=nome):
                with open(self.caminho_md(PEDIDO_APLICADO), "w", encoding="utf-8", newline="\n") as f:
                    f.write(original)
                self.desfecho(PEDIDO_APLICADO, **chaves)
                laco = self.laco()
                pedido = self.pedido(laco, PEDIDO_APLICADO)
                self.assertEqual(pedido["estado"], "aplicado")        # o estado cru fica
                self.assertFalse(pedido["recibo"]["valido"])           # mas o recibo não vale
                self.assertTrue(pedido["recibo"]["erros"])
                self.assertNotEqual(self.controle(laco, "gate_novos")["em_uso"]["estado"], "confirmado")
                self.assertTrue(any(p["mensagem"].startswith("recibo inválido") for p in laco["problemas"]))
                self.assertTrue(any(p["mensagem"].startswith("recibo inválido") for p in self.problemas_do_estado()))

    def test_recibo_valeu_confirma_em_uso_so_com_revisao_igual(self) -> None:
        self.desfecho(PEDIDO_APLICADO, efeito="valeu", valeu_em="2026-10-14T22:10:00-03:00")
        laco = self.laco()
        em_uso = self.controle(laco, "gate_novos")["em_uso"]
        self.assertEqual((em_uso["estado"], em_uso["valor"]), ("confirmado", 0.1))
        self.assertIn("recibo do maestro", em_uso["como"])
        self.assertFalse(self.pedido(laco, PEDIDO_APLICADO)["trabalho_pendente"])
        self.assertEqual(laco["pedidos_abertos"], 0)
        self.mexer_config(trabalhadores_por_gerador=21)  # outra mudança: a revisão não é mais a do recibo
        self.assertEqual(self.controle(self.laco(), "gate_novos")["em_uso"]["estado"], "nao-confirmado")

    def test_em_uso_por_origem_declarada_e_divergencia(self) -> None:
        gravar_json(os.path.join(self.regas, "estado", "uso.json"), {"trabalhadores": 6})
        self.mexer_laco(lambda d: d["controles"][3].update(em_uso={"arquivo": "estado/uso.json",
                                                                   "campo": "trabalhadores"}))
        em_uso = self.controle(self.laco(), "trabalhadores_por_gerador")["em_uso"]
        self.assertEqual((em_uso["estado"], em_uso["valor"], em_uso["diverge"]), ("confirmado", 6, True))

    def test_desfechos_que_exigem_motivo_ou_agora_esta(self) -> None:
        r = self.enviar(self.corpo())
        nome = r["arquivo"]
        for estado, chaves, valido in (
                ("recusado", {}, False), ("recusado", {"motivo": "combinação inválida"}, True),
                ("encerrado-sem-aplicar", {}, False),
                ("encerrado-sem-aplicar", {"motivo": "substituído pelo envio x"}, True),
                ("conflito", {}, False), ("conflito", {"agora_esta": '{"tipo": "texto", "valor": "a faixa mudou"}'}, True),
                ("conflito", {"agora_esta": '{"tipo": "inteiro", "valor": 3}'}, False),
                ("aplicando", {}, False), ("aplicando", {"aplicando_desde": "2099-01-01T00:00:00-03:00"}, True)):
            with self.subTest(estado=estado, chaves=chaves):
                self.desfecho(nome, **{"estado": estado, "motivo": "", "agora_esta": "", "aplicando_desde": "",
                                       **chaves})
                pedido = self.pedido(self.laco(), nome)
                self.assertEqual(pedido["recibo"]["valido"], valido, pedido["recibo"])
        self.desfecho(nome, estado="aplicando", aplicando_desde="2099-01-01T00:00:00-03:00")
        self.assertTrue(self.pedido(self.laco(), nome)["trabalho_pendente"])  # aplicando continua pendente

    def test_comentario_so_passa_por_nova_e_lida(self) -> None:
        self.desfecho(COMENTARIO_LIDO, estado="aplicado")
        pedido = self.pedido(self.laco(), COMENTARIO_LIDO)
        self.assertFalse(pedido["recibo"]["valido"])
        self.assertIn("comentário só passa por nova e lida", pedido["recibo"]["erros"])

    def test_estado_desconhecido_e_problema(self) -> None:
        self.desfecho(COMENTARIO_LIDO, estado="pensando")
        laco = self.laco()
        pedido = self.pedido(laco, COMENTARIO_LIDO)
        self.assertEqual(pedido["estado"], "pensando")
        self.assertFalse(pedido["recibo"]["estado_valido"])
        self.assertTrue(pedido["trabalho_pendente"])
        self.assertTrue(any("estado desconhecido" in p["mensagem"] for p in laco["problemas"]))
        self.assertTrue(any("estado desconhecido" in p["mensagem"] for p in self.problemas_do_estado()))


# ==================================================================================================
# Aviso: pendente de aviso × pendente de trabalho (§4.3, §4.5)
# ==================================================================================================


class AvisoDeAlteracao(ComMaestriFalso):
    def gravar_pedido(self, caixa: modulo_caixa.Caixa, operacao: str = "comentario-laco") -> str:
        projeto = leitores.Projeto(self.projeto_json)
        laco = modulo_lacos.detalhe_do_laco(projeto, EM_VOO)
        corpo = {"envio": novo_envio(), "tipo": "alteracao-laco", "laco": EM_VOO, "execucao": EXECUCAO,
                 "operacao": operacao, "revisao": laco["revisao"], "texto": "um pedido"}
        if operacao == "pedir-parada":
            corpo["capacidade"] = "parar-de-despachar"
        dados = modulo_lacos.validar_alteracao(corpo, projeto, caixa)
        return caixa.gravar(dados)

    def trocar_estado(self, caixa: modulo_caixa.Caixa, nome: str, estado: str) -> None:
        caminho = os.path.join(caixa.pasta, nome + ".md")
        with open(caminho, "r", encoding="utf-8") as f:
            texto = f.read()
        with open(caminho, "w", encoding="utf-8", newline="\n") as f:
            f.write(texto.replace("estado: nova\n", f"estado: {estado}\n", 1))

    def test_mensagem_do_aviso_para_alteracao_de_laco(self) -> None:
        caixa = modulo_caixa.Caixa(self.projeto.caixa)
        nome = self.gravar_pedido(caixa, "pedir-parada")
        emissor = modulo_aviso.Emissor(caixa, self.projeto, self.ambiente)
        resultado = emissor.ciclo()
        self.assertIsNone(resultado["erro"])
        linhas = resultado["mensagem"].split("\n")
        self.assertIn(f"- alteração de laço: Pesquisa de horários de rega, pedir parada (parar de despachar); "
                      f"portal/caixa/{nome}.md", linhas)
        self.assertEqual(linhas[-1], modulo_aviso.INSTRUCAO_COM_LACO)
        self.assertIn("§4.5", linhas[-1])

    def test_estado_valido_marca_entregue_sem_ask_e_desconhecido_nao(self) -> None:
        caixa = modulo_caixa.Caixa(self.projeto.caixa)
        lido = self.gravar_pedido(caixa)
        aplicado = self.gravar_pedido(caixa, "pedir-parada")
        estranho = self.gravar_pedido(caixa)
        self.trocar_estado(caixa, lido, "lida")
        self.trocar_estado(caixa, aplicado, "recusado")   # um desfecho direto também confirma a leitura
        self.trocar_estado(caixa, estranho, "pensando")   # estado desconhecido: não confirma nada
        emissor = modulo_aviso.Emissor(caixa, self.projeto, self.ambiente)
        resultado = emissor.ciclo()
        self.assertIn(estranho[-36:], resultado["envios"])
        self.assertNotIn(lido[-36:], resultado["envios"])
        self.assertNotIn(aplicado[-36:], resultado["envios"])
        self.assertEqual(caixa.fila.estado(lido[-36:]), "entregue")
        self.assertEqual(caixa.fila.estado(aplicado[-36:]), "entregue")
        self.assertEqual(len(self.asks()), 1)  # só o de estado desconhecido (e o órfão da fixture) saíram por ask
        self.assertIn(f"{estranho}.md", self.asks()[0][2])

    def test_vigia_segue_a_mesma_regra(self) -> None:
        caixa = modulo_caixa.Caixa(self.projeto.caixa)
        lido = self.gravar_pedido(caixa)
        estranho = self.gravar_pedido(caixa)
        self.trocar_estado(caixa, lido, "aplicando")
        self.trocar_estado(caixa, estranho, "pensando")
        saida = io.StringIO()
        linhas = modulo_aviso.vigiar_uma_vez(leitores.Projeto(self.projeto_json), saida)
        self.assertTrue(any(estranho in l and l.startswith("alteração de laço: ") for l in linhas), linhas)
        self.assertFalse(any(lido in l for l in linhas), linhas)
        fila = modulo_caixa.Fila(self.projeto.caixa, __import__("threading").RLock())
        self.assertEqual(fila.estado(lido[-36:]), "entregue")

    def test_lida_nao_encerra_o_trabalho(self) -> None:
        caixa = modulo_caixa.Caixa(self.projeto.caixa)
        nome = self.gravar_pedido(caixa, "pedir-parada")
        self.trocar_estado(caixa, nome, "lida")
        modulo_aviso.Emissor(caixa, self.projeto, self.ambiente).ciclo()
        self.assertEqual(caixa.fila.estado(nome[-36:]), "entregue")             # entregue...
        pedido = next(p for p in modulo_lacos.detalhe_do_laco(self.projeto, EM_VOO)["pedidos"] if p["arquivo"] == nome)
        self.assertTrue(pedido["trabalho_pendente"])                              # ...mas o trabalho continua


if __name__ == "__main__":
    unittest.main()
