"""Os leitores e a torre sobre os arquivos reais deste projeto (só estrutura; nada de fatos).

O ``projeto.json`` real ainda não existe na pasta do portal; este teste cria um temporário com o
conteúdo da §3.2 da proposta, com ``raiz`` apontando para o repositório real. Problemas encontrados são
impressos, não derrubam o teste: só exceção ou estrutura errada falham.
"""

from __future__ import annotations

import json
import os
import shutil
import sys
import tempfile
import unittest

PASTA_PORTAL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PASTA_NUCLEO = os.path.join(PASTA_PORTAL, "nucleo")
PASTA_TESTES_NUCLEO = os.path.join(PASTA_NUCLEO, "testes")
for p in (PASTA_NUCLEO, PASTA_TESTES_NUCLEO):
    if p not in sys.path:
        sys.path.insert(0, p)

import apoio  # noqa: E402
import leitores  # noqa: E402

RAIZ_REAL = os.path.realpath(os.path.join(PASTA_PORTAL, "..", "..", ".."))


def criar_projeto_temporario() -> tuple[str, str]:
    tmp = tempfile.mkdtemp(prefix="torre-projeto-real-")
    os.makedirs(os.path.join(tmp, "rodadas"))
    os.makedirs(os.path.join(tmp, "caixa"))
    cartas = [{
        "id": "system-design",
        "titulo": "System design",
        "arquivo": ".scratch/context-hub/system-design.html",
        "pasta": ".scratch/context-hub",
        "proposito": "o desenho do hub de bater o olho",
        "ticket": None,
        "decisao": "a confirmar",
        "data": {"valor": None, "tipo": "modificado"},
        "situacao": "vigente",
        "mestra": True,
    }]
    with open(os.path.join(tmp, "cartas.json"), "w", encoding="utf-8") as f:
        json.dump(cartas, f, ensure_ascii=False, indent=2)
    projeto = {
        "nome": "Context hub",
        "raiz": RAIZ_REAL,
        "porta": 8770,
        "mapa": ".scratch/context-hub/map.md",
        "tickets": ".scratch/context-hub/issues",
        "estrategia": ".scratch/context-hub/estrategia-pos-pesquisa.md",
        "glossario": "GLOSSARY.md",
        "rodadas": "rodadas",
        "caixa": "caixa",
        "cartas": "cartas.json",
        "criterios": [
            {"palavra": "acha"},
            {"palavra": "grava sozinho"},
            {"palavra": "Obsidian e disco"},
            {"palavra": "sem divergência"},
            {"palavra": "edição concorrente"},
        ],
        "aviso": {"agente": "Claude Code", "executavel": "maestri"},
    }
    caminho = os.path.join(tmp, "projeto.json")
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(projeto, f, ensure_ascii=False, indent=2)
    return tmp, caminho


class ProjetoReal(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.tmp, cls.projeto_json = criar_projeto_temporario()
        cls.estado = leitores.montar_estado(cls.projeto_json, apoio.ambiente_limpo())

    @classmethod
    def tearDownClass(cls) -> None:
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def test_estrutura(self) -> None:
        e = self.estado
        self.assertEqual(e["projeto"]["nome"], "Context hub")
        self.assertGreaterEqual(len(e["tickets"]), 52)
        self.assertEqual(len(e["destino"]["criterios"]), 5)
        self.assertEqual([c["palavra"] for c in e["destino"]["criterios"]],
                         ["acha", "grava sozinho", "Obsidian e disco", "sem divergência", "edição concorrente"])
        self.assertTrue(e["destino"]["texto"])
        for c in e["destino"]["criterios"]:
            self.assertTrue(c["texto"])
            self.assertFalse(c["texto"].endswith((";", ".")))
        self.assertTrue(e["decisoes"])
        for d in e["decisoes"]:
            self.assertRegex(d["numero"], r"^\d+$")
            self.assertTrue(d["titulo"] and d["resumo"])
        self.assertTrue(e["radar"])
        for r in e["radar"]:
            self.assertTrue(r["tema"] and r["gatilho"])
        self.assertTrue(e["glossario"])
        for g in e["glossario"]:
            self.assertTrue(g["termo"] and g["definicao"])
        self.assertTrue(e["fora"]["nao_especificado"] or e["fora"]["fora_do_escopo"])
        estados = {t["estado"] for t in e["tickets"]}
        self.assertTrue(estados <= {"open", "claimed", "resolved", "wontfix", "desconhecido"})
        for t in e["tickets"]:
            self.assertTrue(t["arquivo"].startswith(".scratch/context-hub/issues/"))
        self.assertEqual(len(e["cartas"]), 1)
        self.assertEqual(e["cartas"][0]["url"], "/carta/system-design/")
        self.assertRegex(e["cartas"][0]["data"]["valor"], r"^\d{4}-\d{2}-\d{2}$")
        self.assertIsInstance(e["plano_de_voo"]["camadas"], list)
        self.assertTrue(e["plano_de_voo"]["camadas"], "há tickets abertos, o plano de voo não pode estar vazio")
        self.assertFalse(e["aviso"]["disponivel"])

    def test_plano_de_voo_so_com_abertos(self) -> None:
        por_numero = {t["numero"]: t for t in self.estado["tickets"]}
        no_plano = [n for camada in self.estado["plano_de_voo"]["camadas"] for n in camada]
        self.assertEqual(len(no_plano), len(set(no_plano)))
        for n in no_plano:
            self.assertIn(por_numero[n]["estado"], ("open", "claimed"))
        abertos = {t["numero"] for t in self.estado["tickets"] if t["estado"] in ("open", "claimed")}
        self.assertEqual(set(no_plano), abertos)

    def test_lista_problemas(self) -> None:
        problemas = self.estado["problemas"]
        print(f"\n[projeto real] {len(problemas)} problema(s) encontrado(s):")
        for p in problemas:
            print(f"  - {p['arquivo']}: {p['mensagem']}")
        for p in problemas:
            self.assertTrue(p["arquivo"] and p["mensagem"])

    def test_servidor_sobre_o_projeto_real(self) -> None:
        s = apoio.ServidorDeTeste(self.projeto_json)
        self.addCleanup(s.parar)
        status, _, estado = s.get("/api/estado")
        self.assertEqual(status, 200)
        self.assertGreaterEqual(len(estado["tickets"]), 52)
        status, cab, corpo = s.get("/carta/system-design/")
        self.assertEqual(status, 200)
        self.assertTrue(cab["Content-Type"].startswith("text/html"))
        self.assertIn(b"<", corpo)
        for rota in ("/carta/system-design/map.md",
                     "/carta/system-design/issues/01-licoes-do-vault.md",
                     "/carta/system-design/portal/proposta.md",
                     "/carta/system-design/../../GLOSSARY.md",
                     "/carta/system-design/%2e%2e/%2e%2e/GLOSSARY.md"):
            self.assertEqual(s.get(rota)[0], 404, rota)
        status, _, ticket = s.get("/api/ticket/09")
        self.assertEqual(status, 200)
        self.assertTrue(ticket["markdown"].startswith("# "))
        self.assertEqual(s.get("/api/versao")[0], 200)
        # a caixa temporária continua vazia de mensagens (a torre não grava sem POST)
        self.assertTrue(set(os.listdir(os.path.join(self.tmp, "caixa"))) <= {".avisos.json", ".tmp"})
        # sem "lacos" no projeto.json: nenhum laço registrado, sem problema
        self.assertEqual(s.get("/api/lacos")[2], [])


PASTAS_DOS_LACOS = {"modelos-de-embeddings": ".scratch/context-hub/laco-embeddings",
                    "pesquisa-ampla": ".scratch/context-hub/laco"}


def exemplo_do_anexo(secao: str) -> dict:
    """O bloco ```json logo depois do título ``secao`` (ex.: "### A.1") na proposta: só texto, nada executado."""
    with open(os.path.join(PASTA_PORTAL, "proposta.md"), "r", encoding="utf-8") as f:
        texto = f.read()
    depois = texto[texto.index(secao):]
    inicio = depois.index("```json\n") + len("```json\n")
    return json.loads(depois[inicio:depois.index("\n```", inicio)])


class LacosDoProjeto(unittest.TestCase):
    """Os laços deste projeto, só leitura: os exemplos do Anexo A e as pastas reais (que podem estar rodando).

    Nada é gravado nas pastas dos laços; o ``lacos.json`` usado aqui fica na pasta temporária do teste.
    """

    def test_exemplos_do_anexo_a_seguem_o_contrato(self) -> None:
        import lacos  # noqa: PLC0415

        for secao, lid in (("### A.1", "modelos-de-embeddings"), ("### A.2", "pesquisa-ampla")):
            with self.subTest(exemplo=secao):
                laco, avisos = lacos.validar_laco(exemplo_do_anexo(secao), lid)
                self.assertEqual(avisos, [])
                self.assertEqual(laco["id"], lid)

    def test_pastas_reais_registradas_sem_laco_json_e_fontes_nao_servidas(self) -> None:
        tmp, projeto_json = criar_projeto_temporario()
        self.addCleanup(shutil.rmtree, tmp, True)
        with open(os.path.join(tmp, "lacos.json"), "w", encoding="utf-8") as f:
            json.dump([{"id": k, "pasta": v} for k, v in PASTAS_DOS_LACOS.items()], f)
        with open(projeto_json, "r", encoding="utf-8") as f:
            dados = json.load(f)
        dados["lacos"] = "lacos.json"
        with open(projeto_json, "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False)
        s = apoio.ServidorDeTeste(projeto_json)
        self.addCleanup(s.parar)
        status, _, lista = s.get("/api/lacos")
        self.assertEqual(status, 200)
        self.assertEqual([x["id"] for x in lista], list(PASTAS_DOS_LACOS))
        for linha in lista:
            pasta = os.path.join(RAIZ_REAL, PASTAS_DOS_LACOS[linha["id"]])
            if os.path.exists(os.path.join(pasta, "laco.json")):
                self.assertIn(linha["situacao"], ("rodando", "esperando-cota", "sem-sinal", "parado", "terminado",
                                                  "desconhecido"))
                print(f"\n[projeto real] laço {linha['id']}: {linha['situacao']}, {linha['problema']}")
            else:  # o maestro ainda não escreveu o laco.json: aparece pelo id, malformado
                self.assertIn("não tem laco.json", linha["problema"])
        # a carta mestra (pasta .scratch/context-hub) não serve as fontes dos laços
        for rota in ("/carta/system-design/laco/config.json", "/carta/system-design/laco-embeddings/config.json",
                     "/carta/system-design/laco/estado/laco_final.json"):
            self.assertEqual(s.get(rota)[0], 404, rota)
        # os painéis reais (cartas do cartas.json real, copiadas para o temporário) continuam servidos, sem as fontes;
        # e uma carta com a pasta na raiz do laço não serve nada de dentro dele
        with open(os.path.join(PASTA_PORTAL, "cartas.json"), "r", encoding="utf-8") as f:
            paineis = [c for c in json.load(f) if c["id"].startswith("painel-")]
        self.assertTrue(paineis)
        with open(os.path.join(tmp, "cartas.json"), "r", encoding="utf-8") as f:
            cartas = json.load(f)
        raiz_do_laco = dict(paineis[0], id="painel-na-raiz", pasta=PASTAS_DOS_LACOS["pesquisa-ampla"], mestra=False)
        with open(os.path.join(tmp, "cartas.json"), "w", encoding="utf-8") as f:
            json.dump(cartas + paineis + [raiz_do_laco], f, ensure_ascii=False)
        for carta in paineis:
            self.assertEqual(s.get(f"/carta/{carta['id']}/")[0], 200, carta["id"])
        for rota in ("/carta/painel-mare/dados.js", "/carta/painel-mare/etapas.js",
                     "/carta/painel-mare/fontes/sintese.css"):
            self.assertEqual(s.get(rota)[0], 200, rota)
        for rota in ("/carta/painel-mare/%2e%2e/config.json", "/carta/painel-mare/%2e%2e/laco.json",
                     "/carta/painel-mare/%2e%2e/estado/laco_final.json", "/carta/painel-na-raiz/",
                     "/carta/painel-na-raiz/config.json", "/carta/painel-na-raiz/laco.json",
                     "/carta/painel-na-raiz/painel/dados.js"):
            self.assertEqual(s.get(rota)[0], 404, rota)


if __name__ == "__main__":
    unittest.main()
