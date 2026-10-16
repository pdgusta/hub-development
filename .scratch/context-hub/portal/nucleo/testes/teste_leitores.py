"""Marco 1: os leitores sobre a fixture "Horta do bairro" e o contrato ``estado-esperado.json``."""

from __future__ import annotations

import json
import os
import re
import unittest

import apoio

import caixa as modulo_caixa
import leitores


class EstadoDaFixture(unittest.TestCase):
    """``montar_estado`` sobre uma cópia da fixture bate com o esperado pelas regras do LEIA.md."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.tmp, cls.projeto_json = apoio.copiar_horta()
        projeto = leitores.Projeto(cls.projeto_json)
        # a reconciliação do arranque gera o .md que falta e põe o aviso pendente (§3.5)
        modulo_caixa.Caixa(projeto.caixa)
        cls.estado = leitores.montar_estado(cls.projeto_json, apoio.ambiente_limpo())
        cls.esperado = apoio.esperado()

    @classmethod
    def tearDownClass(cls) -> None:
        apoio.apagar(cls.tmp)

    def test_estado_inteiro_bate_com_o_esperado(self) -> None:
        self.assertEqual(apoio.normalizar(self.estado), apoio.normalizar(self.esperado))

    def test_secoes_uma_a_uma(self) -> None:
        # a mesma comparação, seção a seção, para o erro apontar o lugar
        real, esp = apoio.normalizar(self.estado), apoio.normalizar(self.esperado)
        for chave in esp:
            with self.subTest(secao=chave):
                self.assertEqual(real[chave], esp[chave])

    def test_base_e_sha256_do_arquivo(self) -> None:
        for r in self.estado["rodadas"]:
            caminho = os.path.join(leitores.Projeto(self.projeto_json).raiz, r["arquivo"])
            self.assertEqual(r["base"], leitores.sha256_arquivo(caminho))

    def test_gerado_em_tem_fuso(self) -> None:
        self.assertRegex(self.estado["projeto"]["gerado_em"], r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}[+-]\d{2}:\d{2}$")

    def test_aviso_indisponivel_fora_do_canvas(self) -> None:
        self.assertFalse(self.estado["aviso"]["disponivel"])
        self.assertTrue(self.estado["aviso"]["motivo"])

    def test_aviso_disponivel_com_canvas_e_executavel(self) -> None:
        amb = apoio.ambiente_limpo()
        amb.update({"MAESTRI_PIPE": "x", "MAESTRI_TERMINAL_ID": "y"})
        projeto = leitores.Projeto(self.projeto_json)
        # executável fora do PATH → indisponível com motivo
        amb["PATH"] = ""
        self.assertFalse(leitores.disponibilidade_do_aviso(projeto, amb)["disponivel"])
        # o próprio python no PATH serve de executável de teste
        projeto.aviso = {"agente": "x", "executavel": os.path.basename(os.sys.executable)}
        amb["PATH"] = os.path.dirname(os.sys.executable)
        self.assertEqual(leitores.disponibilidade_do_aviso(projeto, amb), {"disponivel": True, "motivo": None})

    def test_estado_sem_reconciliacao_so_difere_no_aviso(self) -> None:
        tmp, projeto_json = apoio.copiar_horta()
        try:
            puro = apoio.normalizar(leitores.montar_estado(projeto_json, apoio.ambiente_limpo()))
            esp = apoio.normalizar(self.esperado)
            # o .json órfão ainda não tem fila: aviso fica null até a reconciliação
            self.assertEqual(puro["caixa"][1]["aviso"], None)
            puro["caixa"][1]["aviso"] = "pendente"
            self.assertEqual(puro, esp)
        finally:
            apoio.apagar(tmp)


class Frontmatter(unittest.TestCase):
    def test_aspas_e_chaves_desconhecidas(self) -> None:
        campos, corpo, erro = leitores.ler_frontmatter('---\ntitulo: "Com aspas"\nx_y: \'a\'\nvazio:\n---\ncorpo\n')
        self.assertIsNone(erro)
        self.assertEqual(campos, {"titulo": "Com aspas", "x_y": "a", "vazio": ""})
        self.assertEqual(corpo, "corpo\n")

    def test_linha_fora_do_formato_e_malformado(self) -> None:
        campos, _, erro = leitores.ler_frontmatter("---\ntitulo: ok\n- lista\n---\n")
        self.assertIsNone(campos)
        self.assertIn("fora do formato", erro)

    def test_sem_fechamento(self) -> None:
        campos, _, erro = leitores.ler_frontmatter("---\ntitulo: ok\n")
        self.assertIsNone(campos)
        self.assertIn("fechamento", erro)

    def test_sem_frontmatter(self) -> None:
        campos, corpo, erro = leitores.ler_frontmatter("# título\n")
        self.assertIsNone(campos)
        self.assertEqual(corpo, "# título\n")


class PlanoDeVoo(unittest.TestCase):
    def _t(self, numero, estado, bloqueado_por=()):
        return {"numero": numero, "estado": estado, "bloqueado_por": list(bloqueado_por),
                "arquivo": f"issues/{numero}-x.md"}

    def test_camadas_por_caminho_mais_longo(self) -> None:
        tickets = [self._t("01", "resolved"), self._t("02", "open", ["01"]), self._t("03", "open", ["02"]),
                   self._t("04", "open", ["01", "03"]), self._t("05", "wontfix"), self._t("06", "desconhecido")]
        plano = leitores.plano_de_voo(tickets, leitores.Problemas())
        self.assertEqual(plano, {"camadas": [["02"], ["03"], ["04"]], "ciclos": []})

    def test_ciclo_de_tres_ignora_a_aresta_de_maior_dependente(self) -> None:
        tickets = [self._t("01", "open", ["03"]), self._t("02", "open", ["01"]), self._t("03", "open", ["02"])]
        problemas = leitores.Problemas()
        plano = leitores.plano_de_voo(tickets, problemas)
        self.assertEqual(plano["ciclos"], [{"tickets": ["01", "02", "03"], "aresta_ignorada": ["03", "02"]}])
        self.assertEqual(plano["camadas"], [["03"], ["01"], ["02"]])
        self.assertEqual([p["arquivo"] for p in problemas.lista()], ["issues/03-x.md"])

    def test_sem_tickets_abertos(self) -> None:
        plano = leitores.plano_de_voo([self._t("01", "resolved")], leitores.Problemas())
        self.assertEqual(plano, {"camadas": [], "ciclos": []})


class CaixaDeterministica(unittest.TestCase):
    def test_hash_do_corpo_bate_com_a_fixture(self) -> None:
        pasta = os.path.join(apoio.PASTA_HORTA, "portal", "caixa")
        for nome in os.listdir(pasta):
            if nome.endswith(".json"):
                with open(os.path.join(pasta, nome), "r", encoding="utf-8") as f:
                    d = json.load(f)
                self.assertEqual(leitores.hash_corpo(d["corpo"]), d["corpo_hash"], nome)

    def test_md_gerado_da_resposta_da_fixture_e_identico_ao_arquivo(self) -> None:
        pasta = os.path.join(apoio.PASTA_HORTA, "portal", "caixa")
        nome = "2026-09-16-093000-resposta-2026-09-15-escolher-o-terreno-r1-7f3a2c10-5b8e-4d21-9a6f-0c3e5d7b9a11"
        with open(os.path.join(pasta, nome + ".json"), "r", encoding="utf-8") as f:
            dados = json.load(f)
        gerado = modulo_caixa.gerar_md(dados)
        esperado = leitores.ler_texto(os.path.join(pasta, nome + ".md"))
        # o estado do arquivo da fixture já foi trocado pelo agente para "lida"
        self.assertEqual(gerado, esperado.replace("estado: lida", "estado: nova"))

    def test_md_do_comentario_orfao_vira_citacao(self) -> None:
        pasta = os.path.join(apoio.PASTA_HORTA, "portal", "caixa")
        nome = "2026-10-03-090000-comentario-ticket-04-c2d4e6f8-1a3b-4c5d-8e7f-9a0b1c2d3e4f"
        with open(os.path.join(pasta, nome + ".json"), "r", encoding="utf-8") as f:
            dados = json.load(f)
        md = modulo_caixa.gerar_md(dados, resolver_titulo=lambda tipo, i: "Composteira")
        campos, corpo, erro = leitores.ler_frontmatter(md)
        self.assertIsNone(erro)
        self.assertEqual(campos["estado"], "nova")
        self.assertEqual(campos["alvo"], "ticket 04")
        self.assertIn("# Comentário: Composteira", corpo)
        self.assertIn("> ---\n> estado: lida\n", corpo)

    def test_mudancas_da_proposta(self) -> None:
        original = {"colunas": ["etapa", "perfil"], "linhas": [
            {"id": "gerar", "etapa": "gerar", "perfil": "a"}, {"id": "juntar", "etapa": "juntar", "perfil": "b"},
            {"id": "velha", "etapa": "velha", "perfil": "c"}]}
        linhas = [{"id": "nova-1", "ativa": True, "valores": {"etapa": "conferir", "perfil": "r"}},
                  {"id": "juntar", "ativa": True, "valores": {"etapa": "juntar", "perfil": "r"}},
                  {"id": "gerar", "ativa": False, "valores": {"etapa": "gerar", "perfil": "a"}}]
        an = modulo_caixa.analisar_proposta(original, linhas)
        self.assertEqual(an["editadas"], [("juntar", "perfil", "b", "r")])
        self.assertEqual([n["id"] for n in an["novas"]], ["nova-1"])
        self.assertEqual(an["removidas"], ["velha"])
        self.assertEqual(an["desligadas"], ["gerar"])
        self.assertTrue(an["reordenada"])
        self.assertEqual(an["operacoes"], {"editar", "adicionar", "remover", "ligar", "reordenar"})
        sem_mudanca = [{"id": "gerar", "ativa": True, "valores": {"etapa": "gerar", "perfil": "a"}},
                       {"id": "juntar", "ativa": True, "valores": {}}, {"id": "velha", "ativa": True, "valores": {}}]
        self.assertEqual(modulo_caixa.analisar_proposta(original, sem_mudanca)["operacoes"], set())


class Confinar(unittest.TestCase):
    """A regra única de caminhos (§3.2) como função pura."""

    def setUp(self) -> None:
        import tempfile
        self.base = os.path.realpath(tempfile.mkdtemp(prefix="torre-confinar-"))
        self.addCleanup(apoio.apagar, self.base)
        os.makedirs(os.path.join(self.base, "sub"))

    def test_dentro_e_aceito(self) -> None:
        real, erro = leitores.confinar(self.base, "sub/x.md", "raiz")
        self.assertIsNone(erro)
        self.assertEqual(real, os.path.join(self.base, "sub", "x.md"))
        self.assertEqual(leitores.confinar(self.base, ".", "raiz"), (self.base, None))
        self.assertEqual(leitores.confinar(self.base, "sub/../sub", "raiz")[0], os.path.join(self.base, "sub"))

    def test_fora_absoluto_e_tipo_errado_sao_recusados(self) -> None:
        for relativo in ("..", "../x.md", "sub/../../x.md", self.base, os.path.join(self.base, "sub"), "/x", "\\x",
                         "C:x", None, 3, ""):
            with self.subTest(relativo=relativo):
                real, erro = leitores.confinar(self.base, relativo, "raiz")
                self.assertIsNone(real)
                self.assertIn("raiz", erro)

    def test_validar_json_caixa_recusa_forma_errada(self) -> None:
        pasta = os.path.join(apoio.PASTA_HORTA, "portal", "caixa")
        nome = "2026-10-03-090000-comentario-ticket-04-c2d4e6f8-1a3b-4c5d-8e7f-9a0b1c2d3e4f"
        with open(os.path.join(pasta, nome + ".json"), "r", encoding="utf-8") as f:
            base = json.load(f)
        leitores.validar_json_caixa(dict(base))  # o da fixture passa
        for mudar in (lambda d: d.update(envio=[]), lambda d: d.update(envio="X"), lambda d: d.update(tipo=None),
                      lambda d: d.update(enviada=1), lambda d: d.update(alvo=["ticket"]), lambda d: d.update(alvo={"tipo": "ticket"}),
                      lambda d: d.update(corpo="x"), lambda d: d.update(corpo_hash="abc"), lambda d: d.update(substitui=1),
                      lambda d: d.update(ticket=4), lambda d: d.update(tipo="resposta"),
                      lambda d: d.update(tipo="resposta", rodada={"id": "r", "perguntas": [{"id": 1}]})):
            d = json.loads(json.dumps(base))
            mudar(d)
            with self.subTest(d=d):
                with self.assertRaises(ValueError):
                    leitores.validar_json_caixa(d)

    def test_validar_registro_de_aviso(self) -> None:
        bom = "12345678-1234-4123-8123-123456789abc"
        self.assertIsNone(leitores.validar_registro_de_aviso(bom, {"estado": "pendente", "tentativas": 0}))
        self.assertIsNone(leitores.validar_registro_de_aviso(
            bom, {"estado": "falhou", "tentativas": 3, "ultimo_erro": "x", "proximo": "2026-01-01T00:00:00+00:00"}))
        for envio, reg in (("x", {"estado": "pendente"}), (bom, []), (bom, {"estado": "voando"}),
                           (bom, {"estado": "pendente", "tentativas": "abc"}), (bom, {"estado": "pendente", "tentativas": -1}),
                           (bom, {"estado": "pendente", "tentativas": 1.5}), (bom, {"estado": "pendente", "ultimo_erro": 1}),
                           (bom, {"estado": "pendente", "proximo": "nunca"})):
            with self.subTest(envio=envio, reg=reg):
                self.assertIsInstance(leitores.validar_registro_de_aviso(envio, reg), str)


class Neutralidade(unittest.TestCase):
    def test_nucleo_nao_cita_o_projeto_real(self) -> None:
        padrao = re.compile(r"context[ -]hub", re.IGNORECASE)
        achados = []
        for raiz, _, nomes in os.walk(apoio.PASTA_NUCLEO):
            for nome in nomes:
                caminho = os.path.join(raiz, nome)
                if os.path.splitext(nome)[1].lower() in (".woff2", ".png", ".jpg", ".pyc"):
                    continue
                try:
                    with open(caminho, "r", encoding="utf-8", errors="ignore") as f:
                        if padrao.search(f.read()):
                            achados.append(os.path.relpath(caminho, apoio.PASTA_NUCLEO))
                except OSError:
                    pass
        self.assertEqual(achados, [])



class ValidacaoDaProposta(unittest.TestCase):
    """§4.1 numa função só, usada pela rodada e pelo retrato gravado na caixa."""

    BOA = {"colunas": ["tarefa", "tempo"], "linhas": [{"id": "a", "tarefa": "x", "tempo": 2}, {"id": "b", "tempo": None}],
           "pode": ["editar"]}

    def test_aceita_a_forma_da_proposta(self) -> None:
        self.assertEqual(leitores.validar_proposta(self.BOA, "p"), self.BOA)
        sem_pode = {"colunas": ["c"], "linhas": []}
        self.assertEqual(leitores.validar_proposta(sem_pode, "p")["pode"], [])

    def test_recusa_estrutura_interna(self) -> None:
        casos = {
            "colunas lista de listas": dict(self.BOA, colunas=[[]]),
            "coluna vazia": dict(self.BOA, colunas=[""]),
            "coluna id": dict(self.BOA, colunas=["id"]),
            "coluna repetida": dict(self.BOA, colunas=["tarefa", "tarefa"]),
            "linha sem id": dict(self.BOA, linhas=[{"tarefa": "x"}]),
            "id numero": dict(self.BOA, linhas=[{"id": 1}]),
            "id repetido": dict(self.BOA, linhas=[{"id": "a"}, {"id": "a"}]),
            "celula lista": dict(self.BOA, linhas=[{"id": "a", "tarefa": ["x"]}]),
            "celula objeto": dict(self.BOA, linhas=[{"id": "a", "tarefa": {"x": 1}}]),
            "coluna desconhecida": dict(self.BOA, linhas=[{"id": "a", "custo": 1}]),
            "pode desconhecido": dict(self.BOA, pode=["voar"]),
            "pode texto": dict(self.BOA, pode="editar"),
            "nao objeto": [],
        }
        for nome, dados in casos.items():
            with self.subTest(caso=nome):
                with self.assertRaises(ValueError) as cm:
                    leitores.validar_proposta(dados, "pergunta x")
                self.assertTrue(str(cm.exception).startswith("pergunta x"), str(cm.exception))

    def test_rodada_com_celula_lista_fica_malformada(self) -> None:
        import tempfile
        pasta = tempfile.mkdtemp(prefix="torre-rodada-")
        self.addCleanup(apoio.apagar, pasta)
        caminho = os.path.join(pasta, "2026-10-14-x-r1.md")
        with open(caminho, "w", encoding="utf-8") as f:
            f.write("---\ntitulo: T\nticket: 01\naberta: 2026-10-14\nestado: aberta\n---\n\n## P\nid: p\ntipo: proposta\n\n"
                    "```json\n{\"colunas\": [\"a\"], \"linhas\": [{\"id\": \"l\", \"a\": [1, 2]}]}\n```\n")
        problemas = leitores.Problemas()
        rodada = leitores.ler_rodada(caminho, "2026-10-14-x-r1", problemas, "rodadas/2026-10-14-x-r1.md")
        self.assertTrue(rodada["malformada"])
        self.assertIn("célula a", rodada["erro"])
        self.assertEqual(rodada["perguntas"], [])
        with open(caminho, "w", encoding="utf-8") as f:
            f.write("---\ntitulo: T\nticket: 01\naberta: 2026-10-14\nestado: aberta\n---\n\n## P\nid: p\ntipo: proposta\n\n"
                    "```json\n{\"colunas\": [\"a\"], \"linhas\": [{\"id\": \"l\", \"a\": 2}]}\n```\n")
        rodada = leitores.ler_rodada(caminho, "2026-10-14-x-r1", leitores.Problemas(), "rodadas/2026-10-14-x-r1.md")
        self.assertFalse(rodada["malformada"], rodada["erro"])


class Codigos(unittest.TestCase):
    """Campo opcional ``codigos`` do projeto.json: prefixo de uma a três letras → explicação em palavras."""

    def setUp(self) -> None:
        self.tmp, self.projeto_json = apoio.copiar_horta()
        self.addCleanup(apoio.apagar, self.tmp)

    def _com(self, codigos) -> dict:
        with open(self.projeto_json, "r", encoding="utf-8") as f:
            dados = json.load(f)
        if codigos is None:
            dados.pop("codigos", None)
        else:
            dados["codigos"] = codigos
        with open(self.projeto_json, "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False)
        return leitores.montar_estado(self.projeto_json, apoio.ambiente_limpo())

    def _problemas_de_codigos(self, estado: dict) -> list[str]:
        return [p["mensagem"] for p in estado["problemas"]
                if p["arquivo"] == "portal/projeto.json" and p["mensagem"].startswith("codigos:")]

    def test_ausente_vale_objeto_vazio(self) -> None:
        estado = self._com(None)
        self.assertEqual(estado["projeto"]["codigos"], {})
        self.assertEqual(self._problemas_de_codigos(estado), [])
        self.assertEqual(set(estado["projeto"]), {"nome", "gerado_em", "codigos"})

    def test_valido_e_devolvido_como_veio(self) -> None:
        codigos = {"Q": "pergunta numerada das rodadas de mapeamento",
                   "R": "resposta numerada na estratégia pós-pesquisa", "ADR": "registro de decisão"}
        estado = self._com(codigos)
        self.assertEqual(estado["projeto"]["codigos"], codigos)
        self.assertEqual(self._problemas_de_codigos(estado), [])
        self.assertEqual(self._com({})["projeto"]["codigos"], {})

    def test_fora_da_forma_vira_problema_e_objeto_vazio(self) -> None:
        casos = {
            "chave com número": {"Q1": "pergunta"},
            "chave longa": {"QUAD": "pergunta"},
            "chave vazia": {"": "pergunta"},
            "chave com hífen": {"Q-": "pergunta"},
            "valor número": {"Q": 5},
            "valor nulo": {"Q": None},
            "valor vazio": {"Q": "   "},
            "valor lista": {"Q": ["pergunta"]},
            "não é objeto": ["Q"],
            "texto solto": "Q: pergunta",
            "boa e ruim juntas": {"Q": "pergunta", "R1": "resposta"},
        }
        for nome, codigos in casos.items():
            with self.subTest(caso=nome):
                estado = self._com(codigos)
                self.assertEqual(estado["projeto"]["codigos"], {})
                mensagens = self._problemas_de_codigos(estado)
                self.assertEqual(len(mensagens), 1, mensagens)
                self.assertIn("ignorado", mensagens[0])
                # o resto do estado continua inteiro: o arranque não é recusado por isso
                self.assertEqual(len(estado["tickets"]), 10)
        # a mensagem nomeia o que está errado
        self.assertIn("'R1'", self._problemas_de_codigos(self._com({"Q": "pergunta", "R1": "resposta"}))[0])
        self.assertIn("texto não vazio", self._problemas_de_codigos(self._com({"Q": 5}))[0])

if __name__ == "__main__":
    unittest.main()


class Substituicao(unittest.TestCase):
    """Campo ``substitui`` do cartas.json: a substituição é calculada na leitura, sem regravar o arquivo."""

    def setUp(self) -> None:
        self.tmp, self.projeto_json = apoio.copiar_horta()
        self.addCleanup(apoio.apagar, self.tmp)
        self.cartas_json = os.path.join(os.path.dirname(self.projeto_json), "cartas.json")
        with open(self.cartas_json, "r", encoding="utf-8") as f:
            self.base = json.load(f)  # mestra "mapa-dos-canteiros" + histórica "regas-do-poco"

    @staticmethod
    def _carta(cid: str, substitui=None, situacao: str = "vigente") -> dict:
        c = {"id": cid, "titulo": f"Carta {cid}", "arquivo": "cartas/regas-do-poco.html", "pasta": "cartas",
             "proposito": "p", "ticket": None, "decisao": "d", "data": {"valor": "2026-10-01", "tipo": "feita"},
             "situacao": situacao, "mestra": False}
        if substitui is not None:
            c["substitui"] = substitui
        return c

    def _estado(self, extras: list[dict]) -> tuple[dict, list[str]]:
        texto = json.dumps(self.base + extras, ensure_ascii=False)
        with open(self.cartas_json, "w", encoding="utf-8") as f:
            f.write(texto)
        estado = leitores.montar_estado(self.projeto_json, apoio.ambiente_limpo())
        with open(self.cartas_json, "r", encoding="utf-8") as f:
            self.assertEqual(f.read(), texto, "o cartas.json não pode ser regravado")
        por_id = {c["id"]: c for c in estado["cartas"]}
        problemas = [p["mensagem"] for p in estado["problemas"] if p["arquivo"] == "portal/cartas.json"]
        return por_id, problemas

    def test_simples(self) -> None:
        c, problemas = self._estado([self._carta("a"), self._carta("b", "a")])
        self.assertEqual(problemas, [])
        self.assertEqual(c["a"]["situacao"], "vigente")  # o campo do arquivo fica como está escrito
        self.assertEqual(c["a"]["situacao_efetiva"], "historica")
        self.assertEqual((c["a"]["substituida_por"], c["a"]["substituida_por_titulo"]), ("b", "Carta b"))
        self.assertEqual((c["b"]["substitui"], c["b"]["substitui_titulo"]), ("a", "Carta a"))
        self.assertEqual(c["b"]["situacao_efetiva"], "vigente")
        self.assertIsNone(c["b"]["substituida_por"])
        # sem substituição, a situação efetiva é a do arquivo
        self.assertEqual(c["regas-do-poco"]["situacao_efetiva"], "historica")
        self.assertIsNone(c["regas-do-poco"]["substitui"])

    def test_cadeia(self) -> None:
        c, problemas = self._estado([self._carta("a"), self._carta("b", "a"), self._carta("c", "b")])
        self.assertEqual(problemas, [])
        self.assertEqual(c["a"]["substituida_por"], "b")
        self.assertEqual(c["b"]["substituida_por"], "c")
        self.assertEqual([c[k]["situacao_efetiva"] for k in "abc"], ["historica", "historica", "vigente"])
        self.assertEqual(c["c"]["substitui_titulo"], "Carta b")

    def test_id_inexistente(self) -> None:
        c, problemas = self._estado([self._carta("b", "fantasma")])
        self.assertEqual(len(problemas), 1)
        self.assertIn("fantasma", problemas[0])
        self.assertEqual(c["b"]["situacao_efetiva"], "vigente")
        self.assertIsNone(c["b"]["substitui_titulo"])

    def test_a_si_mesma(self) -> None:
        c, problemas = self._estado([self._carta("a", "a")])
        self.assertEqual(len(problemas), 1)
        self.assertIn("si mesma", problemas[0])
        self.assertEqual(c["a"]["situacao_efetiva"], "vigente")
        self.assertIsNone(c["a"]["substituida_por"])

    def test_ciclo(self) -> None:
        c, problemas = self._estado([self._carta("a", "b"), self._carta("b", "a"), self._carta("x", "y"),
                                     self._carta("y", "z"), self._carta("z", "x")])
        self.assertEqual(len(problemas), 2)  # um por roda
        for k in "abxyz":
            self.assertEqual(c[k]["situacao_efetiva"], "vigente", k)
            self.assertIsNone(c[k]["substituida_por"], k)
            self.assertIsNone(c[k]["substitui_titulo"], k)

    def test_duas_substituem_a_mesma(self) -> None:
        c, problemas = self._estado([self._carta("a"), self._carta("b", "a"), self._carta("c", "a")])
        self.assertEqual(len(problemas), 1)
        self.assertIn("mesma carta", problemas[0])
        self.assertEqual(c["a"]["substituida_por"], "c")  # a mais nova pela ordem no arquivo
        self.assertEqual((c["b"]["situacao_efetiva"], c["c"]["situacao_efetiva"]), ("vigente", "vigente"))
        self.assertEqual(c["c"]["substitui_titulo"], "Carta a")
        self.assertIsNone(c["b"]["substitui_titulo"])

    def test_mestra_nao_e_substituida(self) -> None:
        c, problemas = self._estado([self._carta("b", "mapa-dos-canteiros")])
        self.assertEqual(len(problemas), 1)
        self.assertIn("mestra", problemas[0])
        m = c["mapa-dos-canteiros"]
        self.assertEqual((m["situacao_efetiva"], m["substituida_por"]), ("vigente", None))

    def test_substitui_fora_da_forma(self) -> None:
        c, problemas = self._estado([self._carta("a"), self._carta("b", 5)])
        self.assertEqual(len(problemas), 1)
        self.assertEqual(c["a"]["situacao_efetiva"], "vigente")
