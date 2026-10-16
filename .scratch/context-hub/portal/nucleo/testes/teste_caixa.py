"""Marco 2: a caixa sozinha (sem HTTP): reconciliação, quedas simuladas, fila de avisos."""

from __future__ import annotations

import json
import os
import subprocess
import unittest
from unittest import mock

import apoio

import caixa as modulo_caixa
import leitores

ORFAO = "2026-10-03-090000-comentario-ticket-04-c2d4e6f8-1a3b-4c5d-8e7f-9a0b1c2d3e4f"
ENVIO_ORFAO = "c2d4e6f8-1a3b-4c5d-8e7f-9a0b1c2d3e4f"
ENVIO_LIDA = "7f3a2c10-5b8e-4d21-9a6f-0c3e5d7b9a11"


def _dados_comentario(envio: str, texto: str = "um comentário") -> dict:
    corpo = {"tipo": "comentario", "alvo": {"tipo": "ticket", "id": "04"}, "texto": texto}
    return {"envio": envio, "tipo": "comentario", "enviada": "2026-10-10T10:00:00-03:00",
            "alvo": {"tipo": "ticket", "id": "04", "titulo": "Composteira"}, "ticket": "04", "substitui": None,
            "corpo_hash": leitores.hash_corpo(corpo), "corpo": corpo}


class Reconciliacao(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp, self.projeto_json = apoio.copiar_horta()
        self.pasta = leitores.Projeto(self.projeto_json).caixa

    def tearDown(self) -> None:
        apoio.apagar(self.tmp)

    def _arquivos(self) -> set[str]:
        return {n for n in os.listdir(self.pasta) if not n.startswith(".")}

    def test_arranque_limpa_tmp_gera_md_e_enfileira(self) -> None:
        self.assertTrue(os.listdir(os.path.join(self.pasta, ".tmp")))
        c = modulo_caixa.Caixa(self.pasta)
        self.assertEqual(os.listdir(os.path.join(self.pasta, ".tmp")), [])
        md = os.path.join(self.pasta, ORFAO + ".md")
        self.assertTrue(os.path.exists(md))
        campos, corpo, _ = leitores.ler_frontmatter(leitores.ler_texto(md))
        self.assertEqual(campos["estado"], "nova")
        self.assertIn("> estado: lida", corpo)
        self.assertEqual(c.fila.estado(ENVIO_ORFAO), "pendente")
        self.assertIsNone(c.fila.estado(ENVIO_LIDA))  # lida: nada a avisar
        self.assertEqual(c.nome_de(ENVIO_ORFAO), ORFAO)
        self.assertEqual(c.problemas, [])
        # o .md sem .json fica onde está
        self.assertTrue(any(n.startswith("2026-10-03-091500-aprovacao") for n in self._arquivos()))

    def test_reconciliar_duas_vezes_nao_muda_nada(self) -> None:
        c = modulo_caixa.Caixa(self.pasta)
        antes = self._arquivos()
        md = leitores.ler_texto(os.path.join(self.pasta, ORFAO + ".md"))
        c.reconciliar()
        c.reconciliar()
        self.assertEqual(self._arquivos(), antes)
        self.assertEqual(leitores.ler_texto(os.path.join(self.pasta, ORFAO + ".md")), md)
        self.assertEqual(c.fila.obter(ENVIO_ORFAO)["tentativas"], 0)

    def test_md_existente_nunca_e_reescrito(self) -> None:
        c = modulo_caixa.Caixa(self.pasta)
        md = os.path.join(self.pasta, ORFAO + ".md")
        with open(md, "a", encoding="utf-8") as f:
            f.write("\nanotação do agente\n")
        c.reconciliar()
        self.assertIn("anotação do agente", leitores.ler_texto(md))

    def test_json_invalido_vai_para_problemas_do_leitor(self) -> None:
        with open(os.path.join(self.pasta, "2026-10-05-000000-comentario-ticket-04-00000000-0000-4000-8000-000000000000.json"),
                  "w", encoding="utf-8") as f:
            f.write("{ quebrado")
        modulo_caixa.Caixa(self.pasta)
        estado = leitores.montar_estado(self.projeto_json, apoio.ambiente_limpo())
        self.assertTrue(any("00000000-0000-4000-8000-000000000000.json" in p["arquivo"] for p in estado["problemas"]))
        self.assertEqual(len(estado["caixa"]), apoio.MENSAGENS_DA_FIXTURE)

    def test_avisos_apagado_recomeca_vazio_e_reenfileira(self) -> None:
        modulo_caixa.Caixa(self.pasta)
        os.remove(os.path.join(self.pasta, ".avisos.json"))
        c = modulo_caixa.Caixa(self.pasta)
        self.assertEqual(c.fila.estado(ENVIO_ORFAO), "pendente")
        self.assertEqual(c.problemas, [])

    def test_avisos_corrompido_recomeca_vazio_com_problema(self) -> None:
        modulo_caixa.Caixa(self.pasta)
        with open(os.path.join(self.pasta, ".avisos.json"), "w", encoding="utf-8") as f:
            f.write("{{{ não é json")
        c = modulo_caixa.Caixa(self.pasta)
        self.assertEqual(c.fila.estado(ENVIO_ORFAO), "pendente")
        self.assertEqual(len(c.problemas), 1)
        self.assertIn("ilegível", c.problemas[0][1])
        with open(os.path.join(self.pasta, ".avisos.json"), "r", encoding="utf-8") as f:
            self.assertIn(ENVIO_ORFAO, json.load(f))

    def test_enviando_volta_para_pendente_e_entregue_fica(self) -> None:
        c = modulo_caixa.Caixa(self.pasta)
        c.fila.marcar(ENVIO_ORFAO, "enviando")
        self.assertEqual(c.fila.obter(ENVIO_ORFAO)["tentativas"], 1)
        c2 = modulo_caixa.Caixa(self.pasta)
        self.assertEqual(c2.fila.estado(ENVIO_ORFAO), "pendente")
        c2.fila.marcar(ENVIO_ORFAO, "entregue")
        c3 = modulo_caixa.Caixa(self.pasta)
        self.assertEqual(c3.fila.estado(ENVIO_ORFAO), "entregue")
        c3.fila.marcar(ENVIO_ORFAO, "falhou", erro="agente não existe")
        c4 = modulo_caixa.Caixa(self.pasta)
        self.assertEqual(c4.fila.estado(ENVIO_ORFAO), "falhou")  # falhou fica visível, não volta sozinho
        self.assertEqual(c4.fila.tentar_de_novo(ENVIO_ORFAO)["estado"], "pendente")
        self.assertIsNone(c4.fila.tentar_de_novo("11111111-1111-4111-8111-111111111111"))

    def test_reparo_periodico_nao_desfaz_enviando(self) -> None:
        # teste real de 2026-10-14: o ask bloqueia até o agente ficar ocioso e o reparo de 30 s o mostrava pendente
        c = modulo_caixa.Caixa(self.pasta)
        c.fila.marcar(ENVIO_ORFAO, "enviando")
        c.reconciliar()
        self.assertEqual(c.fila.estado(ENVIO_ORFAO), "enviando")
        self.assertEqual(c.fila.pendentes(), [])
        c.fila.marcar(ENVIO_ORFAO, "entregue")
        self.assertEqual(modulo_caixa.Caixa(self.pasta).fila.estado(ENVIO_ORFAO), "entregue")

    def test_pendentes_respeita_proximo(self) -> None:
        c = modulo_caixa.Caixa(self.pasta)
        self.assertEqual([e for e, _ in c.fila.pendentes()], [ENVIO_ORFAO])
        c.fila.marcar(ENVIO_ORFAO, "pendente", erro="tempo esgotado", proximo="2999-01-01T00:00:00+00:00")
        self.assertEqual(c.fila.pendentes(), [])
        c.fila.marcar(ENVIO_ORFAO, "pendente", proximo="2000-01-01T00:00:00+00:00")
        self.assertEqual(len(c.fila.pendentes()), 1)
        # proximo ilegível não segura o aviso nem derruba quem emite
        c.fila.marcar(ENVIO_ORFAO, "pendente", proximo="daqui a pouco")
        self.assertEqual(len(c.fila.pendentes()), 1)

    def test_fila_com_registro_malformado_descarta_so_ele_e_recompoe(self) -> None:
        modulo_caixa.Caixa(self.pasta)
        avisos = os.path.join(self.pasta, ".avisos.json")
        outro = "12345678-1234-4123-8123-123456789abc"
        with open(avisos, "w", encoding="utf-8") as f:
            json.dump({
                ENVIO_ORFAO: {"estado": "pendente", "tentativas": "abc"},        # tentativas texto
                outro: {"estado": "falhou", "tentativas": 2, "ultimo_erro": "x", "proximo": None},  # válido
                "x": {"estado": "pendente", "tentativas": 0},                     # chave não é UUID
                ENVIO_LIDA: {"estado": "voando", "tentativas": 0},                # estado desconhecido
                "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa": {"estado": "pendente", "tentativas": -1},
                "bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb": {"estado": "pendente", "tentativas": True},
                "cccccccc-cccc-4ccc-8ccc-cccccccccccc": {"estado": "pendente", "tentativas": 0, "ultimo_erro": 5},
                "dddddddd-dddd-4ddd-8ddd-dddddddddddd": "não é objeto",
            }, f)
        c = modulo_caixa.Caixa(self.pasta)  # o arranque não quebra
        self.assertEqual(c.fila.obter(outro), {"estado": "falhou", "tentativas": 2, "ultimo_erro": "x", "proximo": None})
        for ruim in ("x", ENVIO_LIDA, "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa", "bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb",
                     "cccccccc-cccc-4ccc-8ccc-cccccccccccc", "dddddddd-dddd-4ddd-8ddd-dddddddddddd"):
            self.assertIsNone(c.fila.estado(ruim), ruim)
        # o órfão perdeu o registro ruim e foi recomposto da mensagem (.md nova → pendente, do zero)
        self.assertEqual(c.fila.obter(ENVIO_ORFAO), {"estado": "pendente", "tentativas": 0, "ultimo_erro": None, "proximo": None})
        self.assertEqual([e for e, _ in c.fila.pendentes()], [ENVIO_ORFAO])
        mensagens = [m for caminho, m in c.problemas if caminho.endswith(".avisos.json")]
        self.assertEqual(len(mensagens), 7, mensagens)
        self.assertTrue(any(ENVIO_ORFAO in m and "tentativas" in m for m in mensagens))
        with open(avisos, "r", encoding="utf-8") as f:
            self.assertEqual(set(json.load(f)), {ENVIO_ORFAO, outro})
        # a segunda reconciliação não repete os problemas da fila
        self.assertEqual(c.reconciliar(), [])

    def test_json_com_envio_lista_nao_e_indexado_nem_gera_md(self) -> None:
        with open(os.path.join(self.pasta, ORFAO + ".json"), "r", encoding="utf-8") as f:
            dados = json.load(f)
        dados["envio"] = []
        with open(os.path.join(self.pasta, "quebrado.json"), "w", encoding="utf-8") as f:
            json.dump(dados, f)
        c = modulo_caixa.Caixa(self.pasta)
        self.assertNotIn("quebrado", c.nomes())
        self.assertFalse(os.path.exists(os.path.join(self.pasta, "quebrado.md")))
        self.assertEqual(c.fila.estado(ENVIO_ORFAO), "pendente")
        estado = leitores.montar_estado(self.projeto_json, apoio.ambiente_limpo())
        self.assertTrue(any(p["arquivo"].endswith("quebrado.json") and "envio" in p["mensagem"] for p in estado["problemas"]))
        self.assertEqual(len(estado["caixa"]), apoio.MENSAGENS_DA_FIXTURE)


class Gravacao(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp, self.projeto_json = apoio.copiar_horta()
        self.pasta = leitores.Projeto(self.projeto_json).caixa
        self.caixa = modulo_caixa.Caixa(self.pasta)
        self.antes = self._arquivos()

    def tearDown(self) -> None:
        apoio.apagar(self.tmp)

    def _arquivos(self) -> set[str]:
        return {n for n in os.listdir(self.pasta) if not n.startswith(".")}

    def test_grava_json_md_indice_e_fila(self) -> None:
        envio = "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa"
        nome = self.caixa.gravar(_dados_comentario(envio))
        self.assertRegex(nome, r"^\d{4}-\d{2}-\d{2}-\d{6}-comentario-ticket-04-" + envio + "$")
        self.assertEqual(self._arquivos() - self.antes, {nome + ".json", nome + ".md"})
        self.assertEqual(self.caixa.nome_de(envio), nome)
        self.assertEqual(self.caixa.fila.estado(envio), "pendente")
        self.assertEqual(self.caixa.estado_md(nome), "nova")
        self.assertEqual(os.listdir(os.path.join(self.pasta, ".tmp")), [])

    def _queda(self, alvo, metodo: str):
        envio = "bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb"
        with mock.patch.object(alvo, metodo, mock.Mock(side_effect=OSError("disco cheio"))):
            with self.assertRaises(modulo_caixa.GravacaoParcial) as cm:
                self.caixa.gravar(_dados_comentario(envio))
        nome = cm.exception.nome
        self.assertTrue(os.path.exists(os.path.join(self.pasta, nome + ".json")))
        self.assertEqual(self.caixa.nome_de(envio), nome)  # fica no índice mesmo assim
        return envio, nome

    def _conferir_reparo(self, envio: str, nome: str) -> None:
        # "sobe de novo": nova Caixa sobre a mesma pasta
        nova = modulo_caixa.Caixa(self.pasta)
        self.assertTrue(os.path.exists(os.path.join(self.pasta, nome + ".md")))
        self.assertEqual(nova.estado_md(nome), "nova")
        self.assertEqual(nova.nome_de(envio), nome)
        self.assertEqual(nova.fila.estado(envio), "pendente")
        self.assertEqual(nova.fila.obter(envio)["tentativas"], 0)  # o aviso sai uma vez
        self.assertEqual(len([n for n in self._arquivos() if envio in n]), 2)

    def test_queda_depois_do_json_e_antes_do_md(self) -> None:
        envio, nome = self._queda(modulo_caixa.Caixa, "_gravar_md")
        self.assertFalse(os.path.exists(os.path.join(self.pasta, nome + ".md")))
        self._conferir_reparo(envio, nome)

    def test_queda_depois_do_md_e_antes_da_fila(self) -> None:
        envio, nome = self._queda(modulo_caixa.Fila, "registrar")
        self.assertTrue(os.path.exists(os.path.join(self.pasta, nome + ".md")))
        self.assertIsNone(self.caixa.fila.estado(envio))
        self._conferir_reparo(envio, nome)

    def test_reparo_sem_reiniciar_completa_o_md(self) -> None:
        envio, nome = self._queda(modulo_caixa.Caixa, "_gravar_md")
        self.caixa.reconciliar()  # a tarefa de 30 s
        self.assertTrue(os.path.exists(os.path.join(self.pasta, nome + ".md")))
        self.assertEqual(self.caixa.fila.estado(envio), "pendente")

    def test_sobra_em_tmp_e_apagada_e_nao_vira_problema(self) -> None:
        with open(os.path.join(self.pasta, ".tmp", "sobra.json.parcial"), "w") as f:
            f.write("x")
        nova = modulo_caixa.Caixa(self.pasta)
        self.assertEqual(os.listdir(os.path.join(self.pasta, ".tmp")), [])
        self.assertEqual(nova.problemas, [])

    def test_escrever_atomico_nao_deixa_parcial(self) -> None:
        destino = os.path.join(self.pasta, "x.json")
        modulo_caixa.escrever_atomico(destino, "{}", os.path.join(self.pasta, ".tmp"))
        self.assertEqual(leitores.ler_texto(destino), "{}")
        self.assertEqual(os.listdir(os.path.join(self.pasta, ".tmp")), [])



def _area_sentinela(raiz_temporaria: str) -> tuple[str, str]:
    """Pasta irmã fora da caixa (mas dentro da árvore temporária do teste) com um arquivo que precisa sobreviver."""
    fora = os.path.join(raiz_temporaria, "area-sentinela")
    os.makedirs(fora, exist_ok=True)
    sentinela = os.path.join(fora, "nao-apagar.txt")
    with open(sentinela, "w", encoding="utf-8") as f:
        f.write("arquivo de prova\n")
    return fora, sentinela


def _trocar_tmp_por_atalho(pasta_caixa: str, destino: str, junction: bool) -> bool:
    """Substitui ``caixa/.tmp`` por symlink de pasta (ou junction, no Windows) para ``destino``."""
    tmp = os.path.join(pasta_caixa, ".tmp")
    if os.path.isdir(tmp) and not os.path.islink(tmp):
        for nome in os.listdir(tmp):
            os.remove(os.path.join(tmp, nome))
        os.rmdir(tmp)
    if junction and os.name == "nt":
        r = subprocess.run(["cmd", "/c", "mklink", "/J", tmp, destino], capture_output=True)
        if r.returncode != 0:
            return False
    else:
        try:
            os.symlink(destino, tmp, target_is_directory=True)
        except (OSError, NotImplementedError):
            return False
    return os.path.isdir(tmp)


class TrocaComDestinoAberto(unittest.TestCase):
    """No Windows, o destino aberto por um leitor barra o ``os.replace``; a gravação espera e conclui."""

    def test_destino_aberto_por_leitor_nao_derruba_a_gravacao(self):
        import tempfile
        import threading
        with tempfile.TemporaryDirectory() as pasta:
            destino = os.path.join(pasta, ".avisos.json")
            with open(destino, "w", encoding="utf-8") as f:
                f.write("{}")
            leitor = open(destino, "r", encoding="utf-8")
            threading.Timer(0.2, leitor.close).start()
            modulo_caixa.escrever_atomico(destino, '{"novo": 1}', os.path.join(pasta, ".tmp"))
            leitor.close()
            with open(destino, encoding="utf-8") as f:
                self.assertEqual(f.read(), '{"novo": 1}')
            self.assertEqual(os.listdir(os.path.join(pasta, ".tmp")), [])

    def test_acesso_negado_persistente_ainda_levanta(self):
        with mock.patch.object(modulo_caixa.os, "replace", side_effect=PermissionError("preso")):
            with mock.patch.object(modulo_caixa, "ESPERA_TROCA_S", 0):
                with self.assertRaises(PermissionError):
                    modulo_caixa._trocar("a", "b")


class ConfinamentoDaTmp(unittest.TestCase):
    """§3.2/§3.5: ``caixa/.tmp`` e tudo dentro dela ficam dentro da caixa real; fora disso nada é criado, apagado
    nem gravado. Nenhum teste aqui é pulado: Windows cria junction e symlink sem privilégio."""

    def setUp(self) -> None:
        self.tmp, self.projeto_json = apoio.copiar_horta()
        self.addCleanup(apoio.apagar, self.tmp)
        self.pasta = leitores.Projeto(self.projeto_json).caixa
        self.fora, self.sentinela = _area_sentinela(self.tmp)

    def _conferir_recusa(self) -> None:
        with self.assertRaises(ValueError) as cm:
            modulo_caixa.Caixa(self.pasta)
        self.assertIn("caixa", str(cm.exception))
        self.assertIn("atalho ou junction", str(cm.exception))
        self.assertIn("não há onde gravar", str(cm.exception))
        self.assertTrue(os.path.exists(self.sentinela), "a sentinela fora da caixa foi apagada")
        self.assertEqual(os.listdir(self.fora), ["nao-apagar.txt"])  # nada foi criado lá dentro
        self.assertEqual(leitores.ler_texto(self.sentinela), "arquivo de prova\n")

    def test_tmp_symlink_para_fora_recusa_arranque_e_preserva_sentinela(self) -> None:
        self.assertTrue(_trocar_tmp_por_atalho(self.pasta, self.fora, junction=False),
                        "não deu para criar o symlink de pasta; este teste não pode ser pulado")
        self._conferir_recusa()

    def test_tmp_junction_para_fora_recusa_arranque_e_preserva_sentinela(self) -> None:
        self.assertTrue(_trocar_tmp_por_atalho(self.pasta, self.fora, junction=True),
                        "não deu para criar a junction; este teste não pode ser pulado")
        self._conferir_recusa()

    def test_tmp_que_e_arquivo_recusa_arranque(self) -> None:
        tmp = os.path.join(self.pasta, ".tmp")
        for nome in os.listdir(tmp):
            os.remove(os.path.join(tmp, nome))
        os.rmdir(tmp)
        with open(tmp, "w", encoding="utf-8") as f:
            f.write("x")
        with self.assertRaises(ValueError) as cm:
            modulo_caixa.Caixa(self.pasta)
        self.assertIn("não é uma pasta", str(cm.exception))

    def test_item_de_tmp_apontando_para_fora_fica_e_vira_problema(self) -> None:
        tmp = os.path.join(self.pasta, ".tmp")
        atalho = os.path.join(tmp, "vazou.json.parcial")
        try:
            os.symlink(self.sentinela, atalho)
        except (OSError, NotImplementedError):
            self.fail("não deu para criar o symlink de arquivo; este teste não pode ser pulado")
        sobras = [n for n in os.listdir(tmp) if n != "vazou.json.parcial"]
        self.assertTrue(sobras, "a fixture precisa trazer uma sobra real em .tmp")
        c = modulo_caixa.Caixa(self.pasta)
        self.assertEqual(os.listdir(tmp), ["vazou.json.parcial"])  # a sobra real foi; o atalho ficou
        self.assertTrue(os.path.lexists(atalho))
        self.assertEqual(leitores.ler_texto(self.sentinela), "arquivo de prova\n")
        problemas = [(p, m) for p, m in c.problemas if os.path.basename(p) == "vazou.json.parcial"]
        self.assertEqual(len(problemas), 1, c.problemas)
        self.assertIn("atalho ou junction", problemas[0][1])
        # a reconciliação seguinte repete o problema (continua lá) e continua sem apagar
        self.assertEqual(len([1 for p, _ in c.reconciliar() if p.endswith("vazou.json.parcial")]), 1)
        self.assertTrue(os.path.exists(self.sentinela))
        # o resto do arranque aconteceu: o órfão ganhou .md e entrou na fila
        self.assertEqual(c.fila.estado(ENVIO_ORFAO), "pendente")

    def test_tmp_trocada_em_execucao_nao_grava_nem_apaga_fora(self) -> None:
        c = modulo_caixa.Caixa(self.pasta)
        self.assertTrue(_trocar_tmp_por_atalho(self.pasta, self.fora, junction=False),
                        "não deu para criar o symlink de pasta; este teste não pode ser pulado")
        envio = "dddddddd-dddd-4ddd-8ddd-dddddddddddd"
        with self.assertRaises(ValueError):
            c.gravar(_dados_comentario(envio))
        self.assertIsNone(c.nome_de(envio))
        self.assertFalse(any(envio in n for n in os.listdir(self.pasta)))
        self.assertEqual(os.listdir(self.fora), ["nao-apagar.txt"])  # nada gravado nem apagado lá
        problemas = c.reconciliar()
        self.assertTrue(any(p.endswith(".tmp") and "recusada" in m for p, m in problemas), problemas)
        self.assertEqual(os.listdir(self.fora), ["nao-apagar.txt"])
        self.assertEqual(leitores.ler_texto(self.sentinela), "arquivo de prova\n")
        with self.assertRaises(ValueError):
            c.fila.marcar(ENVIO_ORFAO, "enviando")  # a fila também não grava fora

    def test_escrever_atomico_recusa_tmp_e_destino_fora_da_caixa(self) -> None:
        caixa_real = os.path.realpath(self.pasta)
        destino = os.path.join(self.pasta, "x.json")
        with self.assertRaises(ValueError):
            modulo_caixa.escrever_atomico(destino, "{}", self.fora, caixa_real)
        with self.assertRaises(ValueError):
            modulo_caixa.escrever_atomico(os.path.join(self.fora, "x.json"), "{}", os.path.join(caixa_real, ".tmp"),
                                          caixa_real)
        self.assertEqual(os.listdir(self.fora), ["nao-apagar.txt"])
        self.assertFalse(os.path.exists(destino))
        modulo_caixa.escrever_atomico(destino, "{}", os.path.join(caixa_real, ".tmp"), caixa_real)  # dentro: passa
        self.assertEqual(leitores.ler_texto(destino), "{}")

if __name__ == "__main__":
    unittest.main()
