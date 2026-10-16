"""Aviso ao agente (§4.3): como o agente fica sabendo que há mensagens novas na caixa.

Dois canais sobre a mesma fila ``caixa/.avisos.json`` (§3.5); entrega pelo menos uma vez, absorção idempotente
(o aviso só aponta arquivos; o agente ignora um ``.md`` que já está ``estado: lida``).

- **Canal A, emissor no servidor** (``Emissor``): uma thread junta os ``pendente`` cuja hora chegou numa mensagem
  só e roda ``<executavel> ask <agente> <mensagem>``. Saída 0 → confere com ``<executavel> check <agente>`` se o
  texto ficou digitado sem Enter no terminal do agente (acontece quando ele está no meio de um turno): se o começo
  da mensagem ainda aparece, manda ``ask <agente> --raw "\\r"`` (o Enter), confere de novo e, se continua lá, manda
  ``ask <agente> "(enviar)"``, que leva o texto parado junto. Só então ``entregue``. Saída diferente de 0, exceção
  ou tempo esgotado → ``pendente`` com ``ultimo_erro`` em palavras e nova tentativa em 1, 5 e 15 min; na quarta
  falha, ``falhou`` (visível; ``POST /api/aviso/tentar`` devolve a ``pendente`` e acorda o emissor). ``check`` que
  falha é entrega ambígua: ``pendente`` do mesmo jeito (um aviso repetido não faz mal; um perdido faz).
  Nunca dois ``ask`` ao mesmo tempo. Só existe com ``MAESTRI_PIPE`` e ``MAESTRI_TERMINAL_ID`` no ambiente e o
  executável encontrável; fora disso nada é marcado por este canal (fica ``pendente``).
- **Canal B, vigia do lado do agente** (``vigiar`` / ``python nucleo/aviso.py --vigiar <pasta do portal>``):
  processo separado que a cada poucos segundos lê a fila e os arquivos da caixa (não a tela), imprime UMA linha
  por mensagem ``pendente`` e a marca ``entregue`` ao imprimir. Não toca no que está ``enviando`` (é do canal A).

Convivência dos dois canais na mesma ``.avisos.json``: toda gravação é atômica (``escrever_atomico``) e cada
canal relê a fila imediatamente antes de marcar; só ``pendente`` é tomado pelo vigia, só ``pendente`` com hora
chegada pelo emissor. A janela entre reler e gravar é de milissegundos; se os dois gravarem ao mesmo tempo, o
pior caso é um aviso repetido, nunca um perdido (regra "pelo menos uma vez" da §4.3).

Só biblioteca padrão; nada do projeto: executável e agente vêm de ``projeto.json`` → ``aviso``.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import io
import os
import subprocess
import sys
import tempfile
import threading
import time

try:
    from . import caixa as _caixa
    from . import leitores
except ImportError:  # executado como script solto (python nucleo/aviso.py)
    import caixa as _caixa  # type: ignore
    import leitores  # type: ignore

ESPERAS = (60, 300, 900)   # segundos até a nova tentativa, por número de tentativas já feitas (1, 2, 3)
TIMEOUT_ASK = 1800.0       # o ``ask`` bloqueia até o agente ficar ocioso
TIMEOUT_CHECK = 60.0       # ``check`` e ``--raw`` são rápidos
PASSO_OLHAR = 2.0          # segundos entre as procuras de prova de entrega enquanto o ``ask`` não volta
OLHAR_TELA_POR = 120.0     # por quanto tempo o ``check`` procura a mensagem na tela; depois, só o ``.md`` lido
INTERVALO = 5.0            # segundos entre verificações da fila (o POST e o "tentar de novo" acordam antes)
TAMANHO_DO_COMECO = 40     # caracteres da mensagem procurados na saída do ``check``
TIPOS_EM_PALAVRAS = {"resposta": "resposta", "comentario": "comentário", "aprovacao": "aprovação",
                     "alteracao-laco": "alteração de laço"}
INSTRUCAO = "Absorva no ticket dono e troque estado: nova por lida."
INSTRUCAO_COM_LACO = ("Absorva no ticket dono e troque estado: nova por lida; nas alterações de laço, grave o "
                      "desfecho conforme a §4.5.")


# ----------------------------------------------------------------------------------------------
# A mensagem (§4.3)
# ----------------------------------------------------------------------------------------------


def compor_mensagem(itens: list[dict]) -> str:
    """``itens``: ``[{"tipo", "titulo", "caminho"}]`` → o texto do aviso, uma linha por mensagem."""
    n = len(itens)
    cabeca = f"Portal: {n} {'mensagens novas' if n != 1 else 'mensagem nova'} do Gustavo na caixa."
    linhas = [cabeca]
    for it in itens:
        tipo = TIPOS_EM_PALAVRAS.get(it.get("tipo"), str(it.get("tipo")))
        linhas.append(f"- {tipo}: {it.get('titulo') or 'sem título'}; {it.get('caminho')}")
    # a instrução das alterações de laço (§4.5) só entra quando há uma delas no aviso
    linhas.append(INSTRUCAO_COM_LACO if any(it.get("tipo") == "alteracao-laco" for it in itens) else INSTRUCAO)
    return "\n".join(linhas)


def item_da_mensagem(dados: dict, caminho_md: str, resolver_titulo=None) -> dict:
    """O que o aviso diz de uma mensagem, a partir do seu ``.json`` e do caminho do ``.md`` irmão.

    ``resolver_titulo(tipo_do_alvo, id)`` é opcional (a torre dá o seu): só é consultado quando o ``.json`` não
    guardou ``alvo.titulo``; sem ele, o alvo sai como "tipo id".
    """
    alvo = dados.get("alvo") or {}
    titulo = alvo.get("titulo")
    if not titulo and dados.get("tipo") == "resposta":
        titulo = (dados.get("rodada") or {}).get("titulo")
    if dados.get("tipo") == "alteracao-laco":
        # o título do laço e a operação em palavras (§4.5, "Aviso ao maestro")
        titulo = (f"{titulo or (dados.get('laco') or {}).get('titulo') or alvo.get('id')}, "
                  f"{_caixa.operacao_em_palavras(dados)}")
    if not titulo and resolver_titulo is not None:
        try:
            titulo = resolver_titulo(alvo.get("tipo"), alvo.get("id"))
        except Exception:  # noqa: BLE001 - título é só decoração do aviso
            titulo = None
    return {"tipo": dados.get("tipo"), "titulo": titulo or f"{alvo.get('tipo')} {alvo.get('id')}",
            "caminho": caminho_md}


def texto_no_prompt(saida: str) -> str:
    """Só a caixa de digitação do agente, na tela devolvida pelo ``check``.

    A mensagem entregue continua no histórico da tela; procurar nela inteira acusa texto preso que não existe. No
    Claude Code a caixa fica entre as duas últimas réguas (linhas só de ``─``); sem réguas, valem as 6 últimas linhas.
    """
    linhas = saida.splitlines()
    inicio, fim = _limites_do_prompt(linhas)
    return "\n".join(linhas[inicio:fim])


def _limites_do_prompt(linhas: list[str]) -> tuple[int, int]:
    reguas = [i for i, l in enumerate(linhas) if len(l.strip()) >= 20 and set(l.strip()) == {"─"}]
    if len(reguas) >= 2:
        return reguas[-2] + 1, reguas[-1]
    return max(len(linhas) - 6, 0), len(linhas)


def prova_na_tela(saida: str, envios: list[str]) -> bool:
    """A mensagem já saiu da caixa de digitação: o começo do UUID de cada envio aparece na tela FORA dela.

    O UUID está no caminho do ``.md`` de cada linha do aviso, e só este aviso o traz. Compara sem espaços nem
    quebras de linha, porque a largura do terminal quebra o caminho no meio.
    """
    if not envios:
        return False
    linhas = saida.splitlines()
    inicio, fim = _limites_do_prompt(linhas)
    fora = "".join("".join(l.split()) for l in linhas[:inicio] + linhas[fim:])
    return all(envio[:8] in fora for envio in envios)


def comando_do_executavel(caminho: str) -> list[str]:
    """Como invocar o executável resolvido: um ``.py`` roda com este Python (é o que os testes usam como falso)."""
    if caminho.lower().endswith(".py"):
        return [sys.executable, caminho]
    return [caminho]


# ----------------------------------------------------------------------------------------------
# Canal A: emissor no servidor
# ----------------------------------------------------------------------------------------------


class Emissor:
    """Thread que entrega os avisos ``pendente`` pelo ``ask`` do executável do canvas.

    ``ciclo(agora)`` é um passo só (usado também pelos testes, sem thread); ``iniciar()`` liga o laço, que roda
    um ciclo, espera ``intervalo`` ou um ``acordar()``, e repete até ``parar()``.
    """

    def __init__(self, caixa: _caixa.Caixa, projeto: leitores.Projeto, ambiente, intervalo: float | None = None) -> None:
        self.caixa = caixa
        self.fila = caixa.fila
        self.projeto = projeto
        self.ambiente = ambiente
        self.intervalo = INTERVALO if intervalo is None else intervalo
        self.agente = str(projeto.aviso.get("agente") or "")
        self.lock_envio = threading.Lock()  # nunca duas entregas ao mesmo tempo
        self._em_curso: list[subprocess.Popen] = []  # ask já provados entregues que ainda não voltaram
        self._acordar = threading.Event()
        self._parar = threading.Event()
        self._thread: threading.Thread | None = None
        self.ultimo: dict | None = None     # o último ciclo que enviou algo (diagnóstico)
        self.ciclos = 0

    # -- disponibilidade -----------------------------------------------------------------------

    def disponibilidade(self) -> dict:
        return leitores.disponibilidade_do_aviso(self.projeto, self.ambiente)

    def _comando(self) -> list[str] | None:
        caminho = leitores.resolver_executavel(self.projeto.aviso.get("executavel"), self.ambiente)
        return comando_do_executavel(caminho) if caminho else None

    # -- laço ------------------------------------------------------------------------------------

    def iniciar(self) -> None:
        def laco() -> None:
            while not self._parar.is_set():
                try:
                    self.ciclo()
                except Exception as e:  # noqa: BLE001 - o emissor nunca morre por um erro inesperado
                    self.ultimo = {"erro": f"ciclo do emissor falhou: {e}"}
                self._acordar.wait(self.intervalo)
                self._acordar.clear()
        self._thread = threading.Thread(target=laco, name="emissor-de-avisos", daemon=True)
        self._thread.start()

    def acordar(self) -> None:
        """Chamado depois de um POST na caixa e de um "tentar de novo": não espera o intervalo."""
        self._acordar.set()

    def parar(self) -> None:
        """Parada normal: encerra também os ``ask`` já provados entregues (a thread que os vigiava morre junto).

        Um ``ask`` ainda sem prova não é encerrado: ele sobrevive à queda e entrega (§4.3). Numa queda abrupta nada
        disso roda; os remanescentes saem pelo procedimento do LEIA.
        """
        self._parar.set()
        self._acordar.set()
        if self._thread is not None:
            self._thread.join(timeout=5)
        self.encerrar_asks()

    # -- um passo ---------------------------------------------------------------------------------

    def ciclo(self, agora: _dt.datetime | None = None) -> dict | None:
        """Junta os ``pendente`` cuja hora chegou, manda um ``ask`` só e marca o resultado.

        Devolve ``None`` quando não havia o que mandar (ou o canal está indisponível: nada é marcado) e, quando
        mandou, ``{"envios", "mensagem", "erro"}`` (``erro`` ``None`` = ``entregue``).
        """
        self.ciclos += 1
        agora = agora or _dt.datetime.now().astimezone()
        if not self.disponibilidade()["disponivel"]:
            return None
        comando = self._comando()
        if comando is None:
            return None
        with self.lock_envio:
            pendentes = self.fila.pendentes(agora)
            envios: list[str] = []
            itens: list[dict] = []
            lidos: list[tuple[str, str | None]] = []  # (nome, tipo): o .md lido também prova a entrega
            for envio, _reg in pendentes:
                nome = self.caixa.nome_de(envio)
                if nome is None:
                    continue  # registro sem mensagem na caixa: nada a apontar
                try:
                    dados = self.caixa.dados_de(nome)
                except (OSError, ValueError):
                    dados = {"tipo": None, "alvo": {"tipo": "mensagem", "id": nome}}
                if leitores.entrega_confirmada(dados.get("tipo"), self.caixa.estado_md(nome)):
                    # o agente já leu (ex.: o ask anterior esgotou o tempo depois da entrega): não repetir. Em
                    # alteracao-laco vale qualquer estado válido além de nova; estado desconhecido não confirma
                    self.fila.marcar(envio, "entregue")
                    continue
                caminho_md = self.projeto.relativo(os.path.join(self.caixa.pasta, nome + ".md"))
                envios.append(envio)
                itens.append(item_da_mensagem(dados, caminho_md, self.caixa.resolver_titulo))
                lidos.append((nome, dados.get("tipo")))
            if not envios:
                return None
            mensagem = compor_mensagem(itens)
            for envio in envios:
                self.fila.marcar(envio, "enviando")
            erro = self._entregar(comando, mensagem, envios, lidos)
            for envio in envios:
                if erro is None:
                    self.fila.marcar(envio, "entregue")
                    continue
                reg = self.fila.obter(envio) or {}
                tentativas = int(reg.get("tentativas") or 0)
                if tentativas > len(ESPERAS):
                    self.fila.marcar(envio, "falhou", erro=erro)
                else:
                    proximo = (agora + _dt.timedelta(seconds=ESPERAS[tentativas - 1])).isoformat(timespec="seconds")
                    self.fila.marcar(envio, "pendente", erro=erro, proximo=proximo)
            self.ultimo = {"envios": envios, "mensagem": mensagem, "erro": erro}
            return self.ultimo

    # -- o ask e a conferência -------------------------------------------------------------------

    def _rodar(self, comando: list[str], args: list[str], timeout: float) -> tuple[str, str | None]:
        """Roda ``comando + args``; devolve ``(saída, None)`` ou ``(saída, erro em palavras)``."""
        nome = args[0]
        try:
            r = subprocess.run(comando + args, shell=False, capture_output=True, timeout=timeout,
                               env={k: str(v) for k, v in dict(self.ambiente).items()})
        except subprocess.TimeoutExpired:
            return "", f"{nome} não respondeu em {timeout:g} s"
        except (OSError, ValueError) as e:
            return "", f"não deu para rodar o {nome}: {e}"
        saida = r.stdout.decode("utf-8", errors="replace") + r.stderr.decode("utf-8", errors="replace")
        if r.returncode != 0:
            detalhe = r.stderr.decode("utf-8", errors="replace").strip().splitlines()
            return saida, f"{nome} terminou com código {r.returncode}" + (f": {detalhe[-1][:200]}" if detalhe else "")
        return saida, None

    def _ask_com_prova(self, comando: list[str], args: list[str], envios: list[str],
                       lidos: list[tuple[str, str | None]]) -> tuple[str, str | None]:
        """Roda o ``ask`` sem segurar a fila até ele voltar.

        O ``ask`` só volta quando o agente fica ocioso; um agente sempre ocupado segurava a fila e o aviso seguinte
        não saía (incidente de 2026-10-14, 23h36). Enquanto o ``ask`` não volta, procura prova de entrega a cada
        ``PASSO_OLHAR``: o ``.md`` de todas as mensagens já lido, ou (nos primeiros ``OLHAR_TELA_POR`` s) o UUID de
        cada envio na tela fora da caixa de digitação. Com prova, devolve ``("provado", None)`` e o ``ask`` segue
        sozinho até voltar ou até ``TIMEOUT_ASK``. Sem prova, espera como antes: ``("voltou", erro|None)``.
        """
        nome = args[0]
        saida_f, erro_f = tempfile.TemporaryFile(), tempfile.TemporaryFile()  # nunca PIPE: a resposta pode ser longa
        try:
            processo = subprocess.Popen(comando + args, shell=False, stdout=saida_f, stderr=erro_f,
                                        env={k: str(v) for k, v in dict(self.ambiente).items()})
        except (OSError, ValueError) as e:
            saida_f.close()
            erro_f.close()
            return "voltou", f"não deu para rodar o {nome}: {e}"
        inicio = time.monotonic()
        while True:
            passado = time.monotonic() - inicio
            if passado >= TIMEOUT_ASK:
                processo.kill()
                processo.wait()
                saida_f.close()
                erro_f.close()
                return "voltou", f"{nome} não respondeu em {TIMEOUT_ASK:g} s"
            try:
                processo.wait(timeout=min(PASSO_OLHAR, TIMEOUT_ASK - passado))
                break
            except subprocess.TimeoutExpired:
                pass
            if self._provado(comando, envios, lidos, time.monotonic() - inicio):
                saida_f.close()
                erro_f.close()
                self._acompanhar(processo, inicio)
                return "provado", None
        saida_f.seek(0)
        erro_f.seek(0)
        detalhe = erro_f.read().decode("utf-8", errors="replace").strip().splitlines()
        saida_f.close()
        erro_f.close()
        if processo.returncode != 0:
            return "voltou", f"{nome} terminou com código {processo.returncode}" + (f": {detalhe[-1][:200]}" if detalhe else "")
        return "voltou", None

    def _provado(self, comando: list[str], envios: list[str], lidos: list[tuple[str, str | None]],
                 passado: float) -> bool:
        if lidos and all(leitores.entrega_confirmada(tipo, self.caixa.estado_md(nome)) for nome, tipo in lidos):
            return True
        if passado > OLHAR_TELA_POR:
            return False
        saida, erro = self._rodar(comando, ["check", self.agente], TIMEOUT_CHECK)
        return erro is None and prova_na_tela(saida, envios)

    def _acompanhar(self, processo: subprocess.Popen, inicio: float) -> None:
        """O ``ask`` já entregue segue até voltar; no ``TIMEOUT_ASK`` é encerrado (não fica processo eterno)."""
        self._em_curso.append(processo)

        def esperar() -> None:
            try:
                processo.wait(timeout=max(TIMEOUT_ASK - (time.monotonic() - inicio), 0))
            except subprocess.TimeoutExpired:
                processo.kill()
                processo.wait()
            finally:
                if processo in self._em_curso:
                    self._em_curso.remove(processo)
        threading.Thread(target=esperar, name="ask-entregue", daemon=True).start()

    def asks_em_curso(self) -> list[subprocess.Popen]:
        return [p for p in self._em_curso if p.poll() is None]

    def encerrar_asks(self) -> None:
        """Encerra os ``ask`` já provados entregues que ainda não voltaram (na parada normal e nos testes)."""
        for p in list(self._em_curso):
            if p.poll() is None:
                p.kill()
                p.wait()

    def _entregar(self, comando: list[str], mensagem: str, envios: list[str] | None = None,
                  lidos: list[tuple[str, str | None]] | None = None) -> str | None:
        """``ask`` e depois a conferência do texto preso. ``None`` = entregue; texto = erro em palavras."""
        envios, lidos = envios or [], lidos or []
        como, erro = self._ask_com_prova(comando, ["ask", self.agente, mensagem], envios, lidos)
        if como == "provado":
            return None
        if erro is not None:
            return erro
        comeco = mensagem[:TAMANHO_DO_COMECO]
        saida, erro = self._rodar(comando, ["check", self.agente], TIMEOUT_CHECK)
        if erro is not None:
            return f"entrega ambígua, o check falhou: {erro}"
        if comeco not in texto_no_prompt(saida):
            return None
        # o texto ficou digitado sem Enter no terminal do agente: manda o Enter
        _, erro = self._rodar(comando, ["ask", self.agente, "--raw", "\r"], TIMEOUT_CHECK)
        if erro is not None:
            return f"entrega ambígua, o Enter não pôde ser mandado: {erro}"
        saida, erro = self._rodar(comando, ["check", self.agente], TIMEOUT_CHECK)
        if erro is not None:
            return f"entrega ambígua, o segundo check falhou: {erro}"
        if comeco not in texto_no_prompt(saida):
            return None
        # ainda preso: um ask curto leva o texto parado junto
        _, erro = self._ask_com_prova(comando, ["ask", self.agente, "(enviar)"], envios, lidos)
        if erro is not None:
            return f"entrega ambígua, o '(enviar)' falhou: {erro}"
        return None


# ----------------------------------------------------------------------------------------------
# Canal B: vigia (processo separado, do lado do agente)
# ----------------------------------------------------------------------------------------------


def vigiar_uma_vez(projeto: leitores.Projeto, saida=None) -> list[str]:
    """Lê a fila e a caixa agora; imprime uma linha por ``pendente`` com mensagem e marca ``entregue``.

    Uma mensagem cujo ``.md`` já está ``estado: lida`` (em ``alteracao-laco``, qualquer estado válido além de ``nova``)
    é marcada ``entregue`` sem imprimir (não há o que avisar).
    Registros ``enviando``, ``entregue`` e ``falhou`` ficam como estão. Devolve as linhas impressas.
    """
    saida = saida or sys.stdout
    if not projeto.caixa:
        return []
    # barato primeiro: só a fila; a caixa inteira só é lida quando há algum pendente
    brutos = leitores.ler_avisos_json(projeto.caixa) or {}
    if not any(isinstance(r, dict) and r.get("estado") == "pendente" for r in brutos.values()):
        return []
    jsons, estados, _erros = leitores.listar_caixa(projeto.caixa)
    por_envio = {d["envio"]: nome for nome, d in jsons.items()}
    fila = _caixa.Fila(projeto.caixa, threading.RLock())  # relê a fila agora, grava de forma atômica
    linhas: list[str] = []
    for envio, reg in sorted(fila.todos().items()):
        if reg.get("estado") != "pendente":
            continue
        nome = por_envio.get(envio)
        if nome is None:
            continue
        if leitores.entrega_confirmada(jsons[nome].get("tipo"), estados.get(nome)):
            fila.marcar(envio, "entregue")
            continue
        item = item_da_mensagem(jsons[nome], projeto.relativo(os.path.join(projeto.caixa, nome + ".md")))
        linha = (f"{TIPOS_EM_PALAVRAS.get(item['tipo'], item['tipo'])}: {item['titulo']}; {item['caminho']}; "
                 f"envio {envio}")
        print(linha, file=saida, flush=True)
        linhas.append(linha)
        fila.marcar(envio, "entregue")
    return linhas


def vigiar(pasta_portal: str, intervalo: float = 3.0, uma_vez: bool = False, saida=None,
           parar: threading.Event | None = None) -> int:
    """O laço do canal B. ``0`` ao sair limpo (Ctrl+C ou ``uma_vez``); ``2`` se a pasta não tem projeto.json."""
    saida = saida or sys.stdout
    caminho = os.path.join(pasta_portal, "projeto.json")
    try:
        projeto = leitores.Projeto(caminho)
    except (OSError, ValueError) as e:
        print(f"vigia: não deu para ler {caminho}: {e}", file=sys.stderr)
        return 2
    if not projeto.caixa:
        print("vigia: a caixa do projeto.json está fora da pasta do portal; nada a vigiar", file=sys.stderr)
        return 2
    parar = parar or threading.Event()
    try:
        while True:
            try:
                vigiar_uma_vez(projeto, saida)
            except (OSError, ValueError) as e:
                print(f"vigia: leitura falhou, tento de novo: {e}", file=sys.stderr, flush=True)
            if uma_vez or parar.wait(intervalo):
                return 0
    except KeyboardInterrupt:
        return 0


def main(argv: list[str] | None = None) -> int:
    for fluxo in (sys.stdout, sys.stderr):  # a saída é lida por outro programa: sempre UTF-8
        if hasattr(fluxo, "reconfigure"):
            fluxo.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(prog="aviso.py", description="Canal B do aviso: vigia a caixa do portal.")
    parser.add_argument("--vigiar", metavar="PASTA_DO_PORTAL", required=True,
                        help="pasta onde está o projeto.json; imprime uma linha por mensagem pendente e marca entregue")
    parser.add_argument("--intervalo", type=float, default=3.0, help="segundos entre leituras (padrão 3)")
    parser.add_argument("--uma-vez", action="store_true", help="lê uma vez e sai (para testes e scripts)")
    args = parser.parse_args(argv)
    return vigiar(args.vigiar, intervalo=args.intervalo, uma_vez=args.uma_vez)


if __name__ == "__main__":
    sys.exit(main())
