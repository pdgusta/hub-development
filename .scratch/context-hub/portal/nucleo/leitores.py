"""Leitores do portal: transformam os arquivos do projeto no estado que a API devolve.

Tudo aqui é função pura sobre caminhos: recebe onde estão os arquivos, devolve dicts no esquema
de ``GET /api/estado`` (ver ``testes/fixtures/LEIA.md``). Cada leitor captura o erro por arquivo e
o registra em ``problemas``; um arquivo ruim nunca derruba o estado inteiro.

Só biblioteca padrão.
"""

from __future__ import annotations

import datetime as _dt
import hashlib
import json
import os
import re
import shutil

ESTADOS_TICKET = ("open", "claimed", "resolved", "wontfix")
ESTADOS_RODADA = ("aberta", "suspensa", "absorvida")
TIPOS_PERGUNTA = ("escolha", "varias", "aprovar", "texto", "proposta")
OPERACOES_PROPOSTA = ("editar", "reordenar", "ligar", "adicionar", "remover")
ESTADOS_AVISO = ("pendente", "enviando", "entregue", "falhou")

_RE_TICKET_ARQUIVO = re.compile(r"^(\d+)-([A-Za-z0-9._-]+)\.md$")
_RE_FRONTMATTER_LINHA = re.compile(r"^([a-z_]+):[ \t]*(.*)$")
_RE_OPCAO = re.compile(r"^- ([A-Za-z0-9-]+): (.*)$")
_RE_CABECALHO_PERGUNTA = re.compile(r"^(id|tipo|recomendada):[ \t]*(.*)$")
_RE_ID_PERGUNTA = re.compile(r"^[a-z0-9-]+$")
_RE_DECISAO = re.compile(r"^- \[(.+?)\]\(([^)]+)\):\s*(.*)$")
_RE_ITEM_NUMERADO = re.compile(r"^(\d+)\.\s+(.*)$")
_RE_GLOSSARIO_TERMO = re.compile(r"^\*\*(.+?)\*\*:\s*(.*)$")
_RE_DATA = re.compile(r"^\d{4}-\d{2}-\d{2}$")
_RE_PREFIXO_CODIGO = re.compile(r"^[A-Za-z]{1,3}$")
_RE_UUID = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$")
TIPOS_MENSAGEM = ("resposta", "comentario", "aprovacao", "alteracao-laco")
TIPOS_ALVO = ("rodada", "ticket", "carta", "laco")
# alteração de laço (§4.5): as seis operações e os estados válidos do ``.md`` (o maestro grava todos menos ``nova``)
OPERACOES_LACO = ("mudar-controle", "pedir-parada", "pedir-pausa", "pedir-retomada", "comentario-no",
                  "comentario-laco")
ESTADOS_ALTERACAO = ("nova", "lida", "aplicando", "aplicado", "recusado", "conflito", "encerrado-sem-aplicar")
_RE_ID_LACO = re.compile(r"^[a-z0-9-]+$")


# ----------------------------------------------------------------------------------------------
# Utilidades
# ----------------------------------------------------------------------------------------------


class Problemas:
    """Coleção de problemas (arquivo + mensagem em palavras), sem repetição."""

    def __init__(self) -> None:
        self._itens: list[tuple[str, str]] = []

    def anotar(self, arquivo: str, mensagem: str) -> None:
        par = (arquivo, mensagem)
        if par not in self._itens:
            self._itens.append(par)

    def lista(self) -> list[dict]:
        return [{"arquivo": a, "mensagem": m} for a, m in sorted(self._itens)]


def ler_texto(caminho: str) -> str:
    """Lê um arquivo de texto em UTF-8, tolerando BOM e fins de linha do Windows.

    Levanta ``OSError`` se não dá para abrir e ``UnicodeDecodeError`` (um ``ValueError``) se os bytes não
    são UTF-8 válido: nada é substituído em silêncio, para a corrupção não passar despercebida.
    """
    with open(caminho, "r", encoding="utf-8-sig", newline="") as f:
        return f.read().replace("\r\n", "\n").replace("\r", "\n")


def motivo_de_leitura(e: BaseException) -> str:
    """O erro de leitura de um arquivo, em palavras (codificação ou I/O)."""
    if isinstance(e, UnicodeDecodeError):
        return "arquivo não é UTF-8 válido"
    if isinstance(e, OSError):
        return str(e.strerror or e)
    return str(e)


def envio_valido(valor) -> bool:
    """UUID na forma canônica em minúsculas (é o que entra no nome do arquivo da caixa)."""
    return isinstance(valor, str) and bool(_RE_UUID.fullmatch(valor))


def hora_iso_valida(valor) -> bool:
    """Texto no formato ISO 8601 que ``datetime.fromisoformat`` aceita."""
    if not isinstance(valor, str) or not valor:
        return False
    try:
        _dt.datetime.fromisoformat(valor)
    except ValueError:
        return False
    return True


def sha256_arquivo(caminho: str) -> str:
    with open(caminho, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def hash_corpo(corpo: dict) -> str:
    """sha256 canônico do corpo de uma mensagem (sem o campo ``envio``)."""
    sem_envio = {k: v for k, v in corpo.items() if k != "envio"}
    texto = json.dumps(sem_envio, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(texto.encode("utf-8")).hexdigest()


def agora_iso() -> str:
    return _dt.datetime.now().astimezone().isoformat(timespec="seconds")


def dentro_de(alvo: str, base: str) -> bool:
    """``alvo`` (já real) fica dentro de ``base`` (já real)? Regra única do portal (§3.2)."""
    try:
        comum = os.path.commonpath([alvo, base])
    except ValueError:
        return False
    return os.path.normcase(comum) == os.path.normcase(base)


def confinar(base: str, relativo, nome_base: str) -> tuple[str | None, str | None]:
    """Resolve ``relativo`` dentro de ``base`` (já real) pela regra da §3.2, "sem exceção".

    Devolve ``(caminho real, None)`` ou ``(None, motivo em palavras)``. Recusa caminho que não é texto,
    caminho absoluto (ou com letra de unidade) e qualquer resultado real que saia da base, inclusive por
    ``..``, symlink ou junction.
    """
    if not isinstance(relativo, str) or not relativo:
        return None, f"precisa ser um caminho relativo (texto) dentro de {nome_base}"
    if os.path.isabs(relativo) or os.path.splitdrive(relativo)[0] or relativo.startswith(("/", "\\")):
        return None, f"caminho absoluto não é aceito; precisa ser relativo a {nome_base}: {relativo!r}"
    real = os.path.realpath(os.path.join(base, relativo))
    if not dentro_de(real, base):
        return None, f"o caminho {relativo!r} sai de {nome_base} (por .., atalho ou junction)"
    return real, None


def arquivo_confinado(caminho: str, pasta_real: str) -> bool:
    """Um arquivo descoberto numa pasta continua dentro dela depois de seguir symlink e junction?"""
    return dentro_de(os.path.realpath(caminho), pasta_real)


def ler_frontmatter(texto: str) -> tuple[dict | None, str, str | None]:
    """Separa o frontmatter (§3.3) do corpo.

    Devolve ``(campos, corpo, erro)``. ``campos`` é ``None`` quando não há frontmatter ou ele é
    malformado (``erro`` diz por quê). Chave desconhecida fica no dict; quem usa escolhe o que ler.
    Aspas simples ou duplas em volta do valor são tiradas.
    """
    linhas = texto.split("\n")
    if not linhas or linhas[0].strip() != "---":
        return None, texto, "sem frontmatter (a primeira linha não é ---)"
    campos: dict[str, str] = {}
    for i in range(1, len(linhas)):
        linha = linhas[i]
        if linha.strip() == "---":
            corpo = "\n".join(linhas[i + 1 :])
            return campos, corpo, None
        if not linha.strip():
            continue  # linha em branco dentro do frontmatter é tolerada
        m = _RE_FRONTMATTER_LINHA.match(linha)
        if not m:
            return None, texto, f"linha {i + 1} do frontmatter fora do formato chave: valor: {linha.strip()!r}"
        valor = m.group(2).strip()
        if len(valor) >= 2 and valor[0] == valor[-1] and valor[0] in "\"'":
            valor = valor[1:-1]
        campos[m.group(1)] = valor
    return None, texto, "frontmatter sem a linha --- de fechamento"


def _juntar(linhas: list[str]) -> str:
    return " ".join(l.strip() for l in linhas if l.strip())


def _itens_de_lista(linhas: list[str]) -> list[list[str]]:
    """Agrupa linhas Markdown em itens ``- `` com suas continuações."""
    itens: list[list[str]] = []
    for linha in linhas:
        if not linha.strip() or linha.lstrip().startswith("<!--"):
            continue
        if linha.startswith("- "):
            itens.append([linha[2:]])
        elif itens:
            itens[-1].append(linha)
    return itens


def _secoes_nivel2(texto: str) -> dict[str, list[str]]:
    """Mapa ``título → linhas`` das seções ``## `` de um Markdown."""
    secoes: dict[str, list[str]] = {}
    atual: str | None = None
    for linha in texto.split("\n"):
        if linha.startswith("## "):
            atual = linha[3:].strip()
            secoes.setdefault(atual, [])
        elif atual is not None:
            secoes[atual].append(linha)
    return secoes


# ----------------------------------------------------------------------------------------------
# Projeto (projeto.json) e caminhos
# ----------------------------------------------------------------------------------------------


class Projeto:
    """O ``projeto.json`` resolvido: caminhos reais e a função de relativizar à raiz."""

    CHAVES_OBRIGATORIAS = ("nome", "raiz", "porta", "mapa", "tickets", "estrategia", "glossario",
                           "rodadas", "caixa", "cartas", "criterios", "aviso")

    def __init__(self, caminho_json: str) -> None:
        self.caminho_json = os.path.realpath(caminho_json)
        self.pasta_portal = os.path.dirname(self.caminho_json)
        try:
            with open(self.caminho_json, "r", encoding="utf-8-sig") as f:
                dados = json.load(f)
        except UnicodeDecodeError:
            raise ValueError("projeto.json não é UTF-8 válido") from None
        if not isinstance(dados, dict):
            raise ValueError("projeto.json precisa ser um objeto JSON")
        faltam = [c for c in self.CHAVES_OBRIGATORIAS if c not in dados]
        if faltam:
            raise ValueError("projeto.json sem as chaves: " + ", ".join(faltam))
        if not isinstance(dados["porta"], int):
            raise ValueError("projeto.json: porta precisa ser um número inteiro")
        if not isinstance(dados["criterios"], list):
            raise ValueError("projeto.json: criterios precisa ser uma lista")
        if not isinstance(dados["aviso"], dict) or "agente" not in dados["aviso"] \
                or "executavel" not in dados["aviso"]:
            raise ValueError("projeto.json: aviso precisa ter agente e executavel")
        if not isinstance(dados["raiz"], str) or not dados["raiz"]:
            raise ValueError("projeto.json: raiz precisa ser um caminho (texto)")
        self.dados = dados
        self.nome: str = str(dados["nome"])
        self.porta: int = dados["porta"]
        # a raiz é a escolha do projeto: pode subir quantos níveis quiser
        self.raiz = os.path.realpath(os.path.join(self.pasta_portal, dados["raiz"]))
        # todo outro caminho é confinado (§3.2): fora da base vira problema e o item não é lido nem gravado
        self.problemas_config: list[str] = []
        self.mapa = self._na_raiz("mapa", dados["mapa"])
        self.tickets = self._na_raiz("tickets", dados["tickets"])
        self.estrategia = self._na_raiz("estrategia", dados["estrategia"])
        self.glossario = self._na_raiz("glossario", dados["glossario"])
        self.rodadas = self._no_portal("rodadas", dados["rodadas"])
        self.caixa = self._no_portal("caixa", dados["caixa"])
        self.cartas_json = self._no_portal("cartas", dados["cartas"])
        # registro dos laços (§4.4), opcional: ausente = nenhum laço registrado, sem problema
        self.tem_lacos = "lacos" in dados
        self.lacos_json = self._no_portal("lacos", dados["lacos"]) if self.tem_lacos else None
        self.criterios: list[dict] = dados["criterios"]
        self.aviso: dict = dados["aviso"]
        self.codigos: dict[str, str] = self._ler_codigos(dados.get("codigos"))

    def _ler_codigos(self, bruto) -> dict[str, str]:
        """O campo opcional ``codigos``: prefixo de uma a três letras → explicação em palavras.

        Ausente → ``{}``. Presente mas fora da forma (não é objeto, chave fora de ``^[A-Za-z]{1,3}$``, valor que
        não é texto não vazio) → problema em palavras no ``projeto.json`` e o campo inteiro vira ``{}``; o
        servidor sobe mesmo assim.
        """
        if bruto is None:
            return {}
        if not isinstance(bruto, dict):
            self.problemas_config.append("codigos: precisa ser um objeto prefixo → explicação em palavras; "
                                         "o campo foi ignorado")
            return {}
        motivos: list[str] = []
        for chave, valor in bruto.items():
            if not _RE_PREFIXO_CODIGO.fullmatch(chave):
                motivos.append(f"a chave {chave!r} precisa ter de uma a três letras")
            if not isinstance(valor, str) or not valor.strip():
                motivos.append(f"a explicação de {chave!r} precisa ser texto não vazio")
        if motivos:
            self.problemas_config.append("codigos: " + "; ".join(motivos) + "; o campo foi ignorado")
            return {}
        return dict(bruto)

    def _na_raiz(self, chave: str, relativo) -> str | None:
        real, erro = confinar(self.raiz, relativo, "raiz")
        if erro:
            self.problemas_config.append(f"{chave}: {erro}; o item não foi lido")
        return real

    def _no_portal(self, chave: str, relativo) -> str | None:
        real, erro = confinar(self.pasta_portal, relativo, "a pasta do portal")
        if erro:
            self.problemas_config.append(f"{chave}: {erro}; o item não foi lido" + (
                " nem gravado" if chave == "caixa" else ""))
        return real

    def na_raiz(self, relativo) -> str | None:
        """Caminho real de algo relativo a ``raiz`` (cartas), ou ``None`` se sai dela."""
        return confinar(self.raiz, relativo, "raiz")[0]

    def relativo(self, caminho: str) -> str:
        """Caminho relativo à raiz com ``/``; absoluto se ficar fora dela.

        Resolve atalhos só na pasta, não no último componente: um atalho ou junction encontrado dentro do
        projeto é nomeado por onde está, nunca por onde aponta (o alvo de fora não aparece na API).
        """
        pai, nome = os.path.split(os.path.abspath(caminho))
        real = os.path.join(os.path.realpath(pai), nome) if nome else os.path.realpath(pai)
        if dentro_de(real, self.raiz):
            return os.path.relpath(real, self.raiz).replace(os.sep, "/")
        return real.replace(os.sep, "/")

    def arquivos_reservados(self) -> set[str]:
        """Arquivos do projeto.json que uma carta nunca pode servir (regra 3 da §3.2)."""
        return {c for c in (self.mapa, self.estrategia, self.glossario, self.caminho_json) if c}

    def arquivos_lidos(self) -> list[str]:
        """Tudo o que o estado lê, para ``GET /api/versao``: arquivos soltos e pastas inteiras."""
        caminhos = [c for c in (self.caminho_json, self.cartas_json, self.mapa, self.estrategia, self.glossario) if c]
        if self.caixa:
            caminhos.append(os.path.join(self.caixa, ".avisos.json"))
        for pasta in (self.tickets, self.rodadas, self.caixa):
            if not pasta:
                continue
            caminhos.append(pasta)
            try:
                with os.scandir(pasta) as it:
                    for entrada in it:
                        if entrada.is_file():
                            caminhos.append(entrada.path)
            except OSError:
                pass
        try:
            for carta in ler_cartas_json(self.cartas_json):
                if isinstance(carta, dict):
                    arquivo = self.na_raiz(carta.get("arquivo"))
                    if arquivo:
                        caminhos.append(arquivo)
        except Exception:  # noqa: BLE001 - versão não pode falhar por carta ruim
            pass
        # laços (§3.4): só os descritores, nunca as fontes de estado (os números mudam a cada segundo)
        if self.lacos_json:
            caminhos.append(self.lacos_json)
            try:
                entradas, _ = ler_registro_de_lacos(self)
                caminhos += [os.path.join(e["pasta_real"], "laco.json") for e in entradas if e["pasta_real"]]
            except Exception:  # noqa: BLE001 - versão não pode falhar por registro ruim
                pass
        return caminhos


def ler_registro_de_lacos(projeto: Projeto) -> tuple[list[dict], list[tuple[str, str]]]:
    """O ``lacos.json`` (§4.4): ``(entradas, problemas)``, só leitura, relido a cada pedido.

    Cada entrada: ``{"id", "pasta" (como escrita), "pasta_real" (ou ``None``), "erro" (em palavras, ou ``None``)}``,
    na ordem do registro. Entrada sem ``id`` válido ou com ``id`` repetido não entra (vira problema); entrada com id
    mas pasta ruim entra com ``erro`` (o laço aparece na lista pelo id, como malformado). ``pasta`` é relativa a
    ``raiz``, confinada nela, e não pode estar dentro da pasta do portal nem contê-la. Sem a chave ``lacos`` no
    ``projeto.json``: nenhuma entrada e nenhum problema.
    """
    entradas: list[dict] = []
    problemas: list[tuple[str, str]] = []
    if not projeto.lacos_json:
        return entradas, problemas  # ausente, ou fora da pasta do portal (já anotado no projeto.json)
    nome = projeto.relativo(projeto.lacos_json)
    try:
        with open(projeto.lacos_json, "r", encoding="utf-8-sig") as f:
            dados = json.load(f)
    except FileNotFoundError:
        problemas.append((nome, "registro de laços não existe; nenhum laço é mostrado"))
        return entradas, problemas
    except UnicodeDecodeError:
        problemas.append((nome, "registro de laços não pôde ser lido: arquivo não é UTF-8 válido"))
        return entradas, problemas
    except (OSError, ValueError) as e:
        problemas.append((nome, f"registro de laços não pôde ser lido: {motivo_de_leitura(e)}"))
        return entradas, problemas
    if not isinstance(dados, list):
        problemas.append((nome, "registro de laços precisa ser uma lista"))
        return entradas, problemas
    vistos: set[str] = set()
    for i, item in enumerate(dados):
        if not isinstance(item, dict) or not isinstance(item.get("id"), str) or not _RE_ID_LACO.fullmatch(item["id"]):
            problemas.append((nome, f"laço na posição {i} sem id válido ([a-z0-9-]+); ignorado"))
            continue
        lid = item["id"]
        if lid in vistos:
            problemas.append((nome, f"id de laço repetido: {lid}; vale o primeiro"))
            continue
        vistos.add(lid)
        for chave in item:
            if chave not in ("id", "pasta"):
                problemas.append((nome, f"laço {lid}: chave desconhecida ignorada: {chave}"))
        real, erro = confinar(projeto.raiz, item.get("pasta"), "raiz")
        if real is not None and (dentro_de(real, projeto.pasta_portal) or dentro_de(projeto.pasta_portal, real)):
            real, erro = None, "a pasta do laço não pode estar dentro da pasta do portal nem contê-la"
        entradas.append({"id": lid, "pasta": item.get("pasta"), "pasta_real": real,
                         "erro": f"pasta: {erro}" if erro else None})
    return entradas, problemas


def entrega_confirmada(tipo, estado) -> bool:
    """O ``estado:`` do ``.md`` confirma que o agente leu a mensagem (o aviso pode virar ``entregue``)?

    Nos tipos antigos, só ``lida``. Em ``alteracao-laco`` (§4.5), qualquer estado **válido** diferente de ``nova``
    (o maestro já gravou ``lida`` ou um desfecho); estado desconhecido não confirma nada. Isto confirma só a entrega,
    nunca o fim do trabalho (pendente de trabalho ≠ pendente de aviso).
    """
    if tipo == "alteracao-laco":
        return estado in ESTADOS_ALTERACAO and estado != "nova"
    return estado == "lida"


def versao_do_estado(projeto: Projeto) -> str:
    """sha1 das (caminho, mtime, tamanho) de tudo que o estado lê."""
    h = hashlib.sha1()
    for caminho in sorted(set(projeto.arquivos_lidos())):
        try:
            st = os.stat(caminho)
            h.update(f"{caminho}|{st.st_mtime_ns}|{st.st_size}\n".encode("utf-8"))
        except OSError:
            h.update(f"{caminho}|ausente\n".encode("utf-8"))
    return h.hexdigest()


# ----------------------------------------------------------------------------------------------
# Mapa
# ----------------------------------------------------------------------------------------------


def ler_mapa(caminho: str, criterios_config: list[dict], problemas: Problemas, nome_relativo: str,
             nome_projeto_json: str = "projeto.json") -> tuple[dict, list[dict], dict]:
    """Devolve ``(destino, decisoes, fora)`` do ``map.md``."""
    destino = {"texto": "", "criterios": []}
    decisoes: list[dict] = []
    fora = {"nao_especificado": [], "fora_do_escopo": []}
    try:
        texto = ler_texto(caminho)
    except (OSError, ValueError) as e:
        problemas.anotar(nome_relativo, f"mapa não pôde ser lido: {motivo_de_leitura(e)}")
        return destino, decisoes, fora
    secoes = _secoes_nivel2(texto)

    # Destino: parágrafos antes da lista numerada; cada item numerado é um critério.
    linhas_destino = secoes.get("Destination", [])
    paragrafo: list[str] = []
    criterios: list[list[str]] = []
    for linha in linhas_destino:
        m = _RE_ITEM_NUMERADO.match(linha)
        if m:
            criterios.append([m.group(2)])
        elif criterios:
            if linha.strip():
                criterios[-1].append(linha)
            else:
                break  # linha em branco depois da lista encerra os critérios
        else:
            paragrafo.append(linha)
    destino["texto"] = _juntar(paragrafo)
    palavras = [c.get("palavra") if isinstance(c, dict) else None for c in criterios_config]
    if len(palavras) != len(criterios):
        problemas.anotar(nome_relativo if not criterios else nome_projeto_json,
                         f"o mapa tem {len(criterios)} critérios e o projeto.json dá {len(palavras)} palavras")
    for i, linhas in enumerate(criterios):
        texto_c = _juntar(linhas).rstrip()
        if texto_c.endswith((";", ".")):
            texto_c = texto_c[:-1].rstrip()
        destino["criterios"].append({
            "n": i + 1,
            "palavra": palavras[i] if i < len(palavras) else None,
            "texto": texto_c,
        })
    if "Destination" not in secoes:
        problemas.anotar(nome_relativo, "mapa sem a seção ## Destination")

    # Decisões, na ordem do mapa.
    for item in _itens_de_lista(secoes.get("Decisions so far", [])):
        primeira = item[0]
        m = _RE_DECISAO.match("- " + primeira)
        if not m:
            problemas.anotar(nome_relativo, f"decisão fora do formato: {primeira.strip()[:80]!r}")
            continue
        titulo, link, resumo_inicio = m.groups()
        nome_arquivo = os.path.basename(link.replace("\\", "/"))
        mn = re.match(r"^(\d+)-", nome_arquivo)
        if not mn:
            problemas.anotar(nome_relativo, f"decisão sem número de ticket no link: {link!r}")
            numero = None
        else:
            numero = mn.group(1)
        decisoes.append({"numero": numero, "titulo": titulo.strip(),
                         "resumo": _juntar([resumo_inicio] + item[1:])})

    fora["nao_especificado"] = [_juntar(i) for i in _itens_de_lista(secoes.get("Not yet specified", []))]
    fora["fora_do_escopo"] = [_juntar(i) for i in _itens_de_lista(secoes.get("Out of scope", []))]
    return destino, decisoes, fora


# ----------------------------------------------------------------------------------------------
# Tickets
# ----------------------------------------------------------------------------------------------


def ler_ticket(caminho: str, numero: str, slug: str, problemas: Problemas, nome_relativo: str) -> dict:
    """Um ticket ``NN-slug.md``: título, tipo, estado e ``Blocked by`` (sem as relações ainda)."""
    ticket = {
        "numero": numero, "titulo": slug, "tipo": None, "estado": "desconhecido", "estado_cru": None,
        "bloqueado_por": [], "bloqueios_abertos": [], "bloqueios_inexistentes": [], "bloqueia": [],
        "cartas": [], "arquivo": nome_relativo,
    }
    try:
        texto = ler_texto(caminho)
    except (OSError, ValueError) as e:
        problemas.anotar(nome_relativo, f"ticket não pôde ser lido: {motivo_de_leitura(e)}")
        return ticket
    linhas = texto.split("\n")
    if linhas and linhas[0].startswith("# ") and linhas[0][2:].strip():
        ticket["titulo"] = linhas[0][2:].strip()
    else:
        problemas.anotar(nome_relativo, "ticket sem # Título na primeira linha")
    for linha in linhas[1:]:
        if linha.startswith("## "):
            break
        m = re.match(r"^(Type|Status|Blocked by):[ \t]*(.*)$", linha)
        if not m:
            continue
        chave, valor = m.group(1), m.group(2).strip()
        if chave == "Type":
            ticket["tipo"] = valor or None
        elif chave == "Status":
            ticket["estado_cru"] = valor or None
            if valor in ESTADOS_TICKET:
                ticket["estado"] = valor
            else:
                ticket["estado"] = "desconhecido"
                problemas.anotar(nome_relativo, f"Status desconhecido: {valor!r}".replace("'", '"'))
        elif chave == "Blocked by":
            partes = [p.strip() for p in valor.split(",") if p.strip()]
            for p in partes:
                if re.fullmatch(r"\d+", p):
                    ticket["bloqueado_por"].append(p)
                else:
                    problemas.anotar(nome_relativo, f"Blocked by com valor que não é número: {p!r}")
    if ticket["estado_cru"] is None:
        problemas.anotar(nome_relativo, "ticket sem linha Status:")
    return ticket


def ler_tickets(pasta: str, projeto: Projeto, problemas: Problemas) -> list[dict]:
    """Todos os tickets da pasta, por número, com as relações (bloqueia, bloqueios abertos…)."""
    tickets: list[dict] = []
    try:
        nomes = sorted(os.listdir(pasta))
    except OSError as e:
        problemas.anotar(projeto.relativo(pasta), f"pasta de tickets não pôde ser lida: {e.strerror or e}")
        return tickets
    vistos: dict[str, str] = {}
    pasta_real = os.path.realpath(pasta)
    for nome in nomes:
        m = _RE_TICKET_ARQUIVO.match(nome)
        if not m:
            continue  # outros arquivos na pasta não são tickets
        numero, slug = m.group(1), m.group(2)
        caminho = os.path.join(pasta, nome)
        if not os.path.isfile(caminho):
            continue
        if not arquivo_confinado(caminho, pasta_real):
            problemas.anotar(projeto.relativo(pasta) + "/" + nome,
                             "ticket ignorado: o arquivo real fica fora da pasta de tickets (atalho ou junction)")
            continue
        relativo = projeto.relativo(caminho)
        if numero in vistos:
            problemas.anotar(relativo, f"número {numero} repetido (já usado por {vistos[numero]})")
            continue
        vistos[numero] = nome
        tickets.append(ler_ticket(caminho, numero, slug, problemas, relativo))

    por_numero = {t["numero"]: t for t in tickets}
    bloqueia: dict[str, set[str]] = {n: set() for n in por_numero}
    for t in tickets:
        abertos: set[str] = set()
        for b in t["bloqueado_por"]:
            alvo = por_numero.get(b)
            if alvo is None:
                t["bloqueios_inexistentes"].append(b)
                problemas.anotar(t["arquivo"], f"Blocked by aponta para ticket inexistente: {b}")
                continue
            bloqueia[b].add(t["numero"])
            if alvo["estado"] in ("open", "claimed", "desconhecido"):
                abertos.add(b)
        t["bloqueios_abertos"] = sorted(abertos, key=_chave_numero)
        t["bloqueios_inexistentes"] = sorted(set(t["bloqueios_inexistentes"]), key=_chave_numero)
    for t in tickets:
        t["bloqueia"] = sorted(bloqueia[t["numero"]], key=_chave_numero)
    tickets.sort(key=lambda t: _chave_numero(t["numero"]))
    return tickets


def _chave_numero(n: str) -> tuple:
    return (int(n), n) if n.isdigit() else (10**9, n)


# ----------------------------------------------------------------------------------------------
# Plano de voo
# ----------------------------------------------------------------------------------------------


def plano_de_voo(tickets: list[dict], problemas: Problemas) -> dict:
    """Camadas por caminho mais longo entre os tickets ``open`` e ``claimed``; ciclos quebrados.

    Aresta = dependente → bloqueador. Num ciclo ignora-se a aresta de maior dependente (empate: maior
    bloqueador), só para desenhar, e o dependente ganha um problema.
    """
    no_plano = {t["numero"]: t for t in tickets if t["estado"] in ("open", "claimed")}
    deps: dict[str, list[str]] = {}
    for n, t in no_plano.items():
        deps[n] = sorted({b for b in t["bloqueado_por"] if b in no_plano}, key=_chave_numero)
    ciclos: list[dict] = []

    while True:
        ciclo = _achar_ciclo(deps)
        if ciclo is None:
            break
        # arestas do ciclo: (dependente, bloqueador) consecutivos
        arestas = [(ciclo[i], ciclo[(i + 1) % len(ciclo)]) for i in range(len(ciclo))]
        dependente, bloqueador = max(arestas, key=lambda a: (_chave_numero(a[0]), _chave_numero(a[1])))
        deps[dependente] = [b for b in deps[dependente] if b != bloqueador]
        nos = sorted(set(ciclo), key=_chave_numero)
        ciclos.append({"tickets": nos, "aresta_ignorada": [dependente, bloqueador]})
        problemas.anotar(no_plano[dependente]["arquivo"],
                         f"ciclo de dependência entre {' e '.join(nos)}; a aresta {dependente} → {bloqueador}"
                         " foi ignorada no plano de voo")

    camada: dict[str, int] = {}

    def nivel(n: str) -> int:
        if n in camada:
            return camada[n]
        camada[n] = 0  # guarda contra recursão (não deve acontecer sem ciclo)
        valor = 0 if not deps[n] else 1 + max(nivel(b) for b in deps[n])
        camada[n] = valor
        return valor

    for n in sorted(no_plano, key=_chave_numero):
        nivel(n)
    camadas: list[list[str]] = []
    if camada:
        for k in range(max(camada.values()) + 1):
            camadas.append(sorted([n for n, v in camada.items() if v == k], key=_chave_numero))
    return {"camadas": camadas, "ciclos": ciclos}


def _achar_ciclo(deps: dict[str, list[str]]) -> list[str] | None:
    """Devolve um ciclo (lista de nós, em ordem de aresta dependente → bloqueador) ou ``None``."""
    cor: dict[str, int] = {}
    pilha: list[str] = []

    def visitar(n: str) -> list[str] | None:
        cor[n] = 1
        pilha.append(n)
        for b in deps.get(n, []):
            if cor.get(b, 0) == 0:
                achado = visitar(b)
                if achado:
                    return achado
            elif cor[b] == 1:
                return pilha[pilha.index(b):]
        pilha.pop()
        cor[n] = 2
        return None

    for n in sorted(deps, key=_chave_numero):
        if cor.get(n, 0) == 0:
            achado = visitar(n)
            if achado:
                return achado
    return None


# ----------------------------------------------------------------------------------------------
# Estratégia (radar) e glossário
# ----------------------------------------------------------------------------------------------


def ler_radar(caminho: str, problemas: Problemas, nome_relativo: str) -> list[dict]:
    """Primeira tabela Markdown depois de ``### Radar``: colunas tema e gatilho, cruas."""
    try:
        texto = ler_texto(caminho)
    except (OSError, ValueError) as e:
        problemas.anotar(nome_relativo, f"estratégia não pôde ser lida: {motivo_de_leitura(e)}")
        return []
    linhas = texto.split("\n")
    inicio = next((i for i, l in enumerate(linhas) if l.strip() == "### Radar"), None)
    if inicio is None:
        problemas.anotar(nome_relativo, "estratégia sem a seção ### Radar")
        return []
    radar: list[dict] = []
    em_tabela = False
    for linha in linhas[inicio + 1:]:
        if linha.startswith("#"):
            break
        if not linha.strip().startswith("|"):
            if em_tabela:
                break
            continue
        em_tabela = True
        celulas = [c.strip() for c in linha.strip().strip("|").split("|")]
        if all(re.fullmatch(r":?-{2,}:?", c) for c in celulas if c):
            continue  # linha de traços
        if not radar and not em_tabela:
            continue
        if len(celulas) < 2:
            problemas.anotar(nome_relativo, f"linha do radar com menos de duas colunas: {linha.strip()[:60]!r}")
            continue
        radar.append({"tema": celulas[0], "gatilho": celulas[1]})
    # a primeira linha coletada é o cabeçalho
    return radar[1:] if radar else []


def ler_glossario(caminho: str, problemas: Problemas, nome_relativo: str) -> list[dict]:
    """``**Termo**:`` + linhas da definição até linha em branco ou ``_Avoid_:``."""
    try:
        texto = ler_texto(caminho)
    except (OSError, ValueError) as e:
        problemas.anotar(nome_relativo, f"glossário não pôde ser lido: {motivo_de_leitura(e)}")
        return []
    termos: list[dict] = []
    atual: dict | None = None
    definicao: list[str] = []

    def fechar() -> None:
        nonlocal atual, definicao
        if atual is not None:
            atual["definicao"] = _juntar(definicao)
            termos.append(atual)
        atual, definicao = None, []

    for linha in texto.split("\n"):
        m = _RE_GLOSSARIO_TERMO.match(linha)
        if m:
            fechar()
            atual = {"termo": m.group(1).strip(), "definicao": "", "evite": None}
            if m.group(2).strip():
                definicao.append(m.group(2))
            continue
        if atual is None:
            continue
        if linha.startswith("_Avoid_:"):
            atual["evite"] = linha[len("_Avoid_:"):].strip() or None
            fechar()
        elif not linha.strip():
            fechar()
        else:
            definicao.append(linha)
    fechar()
    return termos


# ----------------------------------------------------------------------------------------------
# Cartas
# ----------------------------------------------------------------------------------------------


def ler_cartas_json(caminho: str | None) -> list:
    if not caminho:
        raise ValueError("cartas.json fora da pasta do portal")
    try:
        with open(caminho, "r", encoding="utf-8-sig") as f:
            dados = json.load(f)
    except UnicodeDecodeError:
        raise ValueError("arquivo não é UTF-8 válido") from None
    if not isinstance(dados, list):
        raise ValueError("cartas.json precisa ser uma lista")
    return dados


def ler_cartas(projeto: Projeto, tickets: list[dict], problemas: Problemas) -> list[dict]:
    """As cartas do ``cartas.json`` com ``ticket_titulo``, ``url`` e a data real de modificação."""
    if not projeto.cartas_json:
        return []  # o problema de confinamento já foi anotado no projeto.json
    nome_relativo = projeto.relativo(projeto.cartas_json)
    try:
        entradas = ler_cartas_json(projeto.cartas_json)
    except (OSError, ValueError) as e:
        problemas.anotar(nome_relativo, f"cartas.json não pôde ser lido: {motivo_de_leitura(e)}")
        return []
    titulos = {t["numero"]: t["titulo"] for t in tickets}
    cartas: list[dict] = []
    ids: set[str] = set()
    for i, entrada in enumerate(entradas):
        if not isinstance(entrada, dict) or not isinstance(entrada.get("id"), str) or not entrada["id"]:
            problemas.anotar(nome_relativo, f"carta na posição {i} sem id")
            continue
        cid = entrada["id"]
        if not re.fullmatch(r"[A-Za-z0-9._-]+", cid) or cid.startswith("."):
            problemas.anotar(nome_relativo, f"id de carta inválido: {cid!r}")
            continue
        if cid in ids:
            problemas.anotar(nome_relativo, f"id de carta repetido: {cid}")
            continue
        ids.add(cid)
        ticket = entrada.get("ticket")
        data = entrada.get("data") if isinstance(entrada.get("data"), dict) else {"valor": None, "tipo": None}
        carta = {
            "id": cid,
            "titulo": entrada.get("titulo"),
            "arquivo": entrada.get("arquivo"),
            "pasta": entrada.get("pasta"),
            "proposito": entrada.get("proposito"),
            "ticket": ticket,
            "ticket_titulo": titulos.get(ticket) if isinstance(ticket, str) else None,
            "decisao": entrada.get("decisao"),
            "data": {"valor": data.get("valor"), "tipo": data.get("tipo")},
            "situacao": entrada.get("situacao"),
            "mestra": bool(entrada.get("mestra", False)),
        }
        for chave, valor in entrada.items():
            if chave not in carta:
                carta[chave] = valor
        carta["url"] = f"/carta/{cid}/"
        if isinstance(ticket, str) and ticket not in titulos:
            problemas.anotar(nome_relativo, f"carta {cid} aponta para ticket inexistente: {ticket}")
        if not isinstance(carta["arquivo"], str) or not isinstance(carta["pasta"], str):
            problemas.anotar(nome_relativo, f"carta {cid} sem arquivo ou pasta")
            cartas.append(carta)
            continue
        caminho, erro_arquivo = confinar(projeto.raiz, carta["arquivo"], "raiz")
        pasta, erro_pasta = confinar(projeto.raiz, carta["pasta"], "raiz")
        if caminho is None or pasta is None:
            problemas.anotar(nome_relativo, f"carta {cid}: {erro_arquivo or erro_pasta}; a carta não é servida")
            cartas.append(carta)
            continue
        if os.path.dirname(caminho) != pasta:
            problemas.anotar(nome_relativo, f"carta {cid}: o arquivo não está diretamente dentro da pasta")
        if not os.path.isfile(caminho):
            problemas.anotar(nome_relativo, f"carta {cid}: arquivo não existe: {carta['arquivo']}")
        elif carta["data"]["tipo"] == "modificado":
            mtime = os.stat(caminho).st_mtime
            carta["data"]["valor"] = _dt.datetime.fromtimestamp(mtime).strftime("%Y-%m-%d")
        if carta["data"]["tipo"] not in ("modificado", "feita"):
            problemas.anotar(nome_relativo, f"carta {cid}: data.tipo desconhecido: {carta['data']['tipo']!r}")
        cartas.append(carta)
    calcular_substituicoes(cartas, problemas, nome_relativo)
    return cartas


def calcular_substituicoes(cartas: list[dict], problemas: Problemas, nome_relativo: str) -> None:
    """Aplica o campo ``substitui`` das cartas, na leitura (o ``cartas.json`` nunca é regravado).

    Toda carta ganha ``substitui`` (como escrito, ou ``None``), ``substitui_titulo``, ``substituida_por``,
    ``substituida_por_titulo`` e ``situacao_efetiva``. A carta substituída fica com ``situacao_efetiva``
    ``historica`` e aponta a sua substituta direta; ``situacao`` continua a do arquivo. Casos ruins (id
    inexistente, a si mesma, carta mestra, ciclo) viram problema e a ligação é ignorada; duas cartas
    substituindo a mesma: vale a que vem depois no arquivo, e o caso é anotado.
    """
    por_id = {c["id"]: c for c in cartas}
    for c in cartas:
        c.setdefault("substitui", None)
        c["substitui_titulo"] = None
        c["substituida_por"] = None
        c["substituida_por_titulo"] = None
    # 1. ligações válidas, uma por carta nova (novo → antigo), na ordem do arquivo
    ligacoes: dict[str, str] = {}
    for c in cartas:
        alvo = c["substitui"]
        if alvo is None:
            continue
        cid = c["id"]
        if not isinstance(alvo, str) or not alvo:
            problemas.anotar(nome_relativo, f"carta {cid}: \"substitui\" precisa ser o id de outra carta; ignorado")
        elif alvo == cid:
            problemas.anotar(nome_relativo, f"carta {cid} diz que substitui a si mesma; ignorado")
        elif alvo not in por_id:
            problemas.anotar(nome_relativo, f"carta {cid} substitui uma carta que não existe: {alvo}")
        elif por_id[alvo]["mestra"]:
            problemas.anotar(nome_relativo, f"carta {cid} tenta substituir a carta mestra {alvo}; "
                                            "a mestra não é substituída por esta regra")
        else:
            ligacoes[cid] = alvo
    # 2. duas ou mais cartas substituindo a mesma: vale a última no arquivo
    substituta: dict[str, str] = {}
    for novo, antigo in ligacoes.items():  # dict mantém a ordem do arquivo
        if antigo in substituta:
            problemas.anotar(nome_relativo, f"cartas {substituta[antigo]} e {novo} substituem a mesma carta "
                                            f"{antigo}; vale a mais nova no arquivo ({novo})")
        substituta[antigo] = novo
    ligacoes = {novo: antigo for antigo, novo in substituta.items()}
    # 3. ciclos (A substitui B, B substitui A...): cada carta tem no máximo uma ligação de saída
    em_ciclo: set[str] = set()
    for inicio in ligacoes:
        caminho: list[str] = []
        atual = inicio
        while atual in ligacoes and atual not in caminho and atual not in em_ciclo:
            caminho.append(atual)
            atual = ligacoes[atual]
        if atual in caminho:
            ciclo = caminho[caminho.index(atual):]
            em_ciclo.update(ciclo)
            problemas.anotar(nome_relativo, "cartas substituem umas às outras em roda ("
                             + " → ".join(ciclo + [atual]) + "); nenhuma delas é tirada das vigentes")
    # 4. aplica
    for novo, antigo in ligacoes.items():
        if novo in em_ciclo:
            continue
        nova, velha = por_id[novo], por_id[antigo]
        velha["substituida_por"] = novo
        velha["substituida_por_titulo"] = nova["titulo"] if isinstance(nova["titulo"], str) else None
        nova["substitui_titulo"] = velha["titulo"] if isinstance(velha["titulo"], str) else None
    for c in cartas:
        c["situacao_efetiva"] = "historica" if c["substituida_por"] else c["situacao"]


def pasta_real_da_carta(projeto: Projeto, carta: dict) -> tuple[str, str] | None:
    """``(pasta real, arquivo real)`` de uma carta, ou ``None`` se os campos faltam ou saem da raiz."""
    pasta = projeto.na_raiz(carta.get("pasta"))
    arquivo = projeto.na_raiz(carta.get("arquivo"))
    if pasta is None or arquivo is None:
        return None
    return pasta, arquivo


# ----------------------------------------------------------------------------------------------
# Rodadas
# ----------------------------------------------------------------------------------------------


class RodadaMalformada(ValueError):
    pass


def _parse_perguntas(corpo: str) -> list[dict]:
    """As perguntas (``## ``) do corpo de uma rodada. Levanta ``RodadaMalformada``."""
    linhas = corpo.split("\n")
    blocos: list[tuple[str, list[str]]] = []
    for linha in linhas:
        if linha.startswith("## "):
            blocos.append((linha[3:].strip(), []))
        elif blocos:
            blocos[-1][1].append(linha)
    perguntas: list[dict] = []
    ids: set[str] = set()
    for titulo, corpo_linhas in blocos:
        cab: dict[str, str] = {}
        i = 0
        # fase 1: cabeçalho id/tipo/recomendada (linhas em branco toleradas)
        while i < len(corpo_linhas):
            l = corpo_linhas[i]
            if not l.strip():
                i += 1
                continue
            m = _RE_CABECALHO_PERGUNTA.match(l)
            if not m:
                break
            cab[m.group(1)] = m.group(2).strip()
            i += 1
        pid = cab.get("id")
        if not pid:
            raise RodadaMalformada(f'pergunta "{titulo}" sem id')
        if not _RE_ID_PERGUNTA.fullmatch(pid):
            raise RodadaMalformada(f'pergunta "{titulo}" com id fora do formato: {pid!r}')
        if pid in ids:
            raise RodadaMalformada(f"id de pergunta repetido: {pid}")
        ids.add(pid)
        tipo = cab.get("tipo")
        if not tipo:
            raise RodadaMalformada(f'pergunta "{titulo}" sem tipo')
        if tipo not in TIPOS_PERGUNTA:
            raise RodadaMalformada(f'pergunta "{titulo}" com tipo desconhecido: {tipo!r}')
        recomendada = [r.strip() for r in cab.get("recomendada", "").split(",") if r.strip()]
        # fase 2: opções
        opcoes: list[dict] = []
        chaves: set[str] = set()
        while i < len(corpo_linhas):
            l = corpo_linhas[i]
            if not l.strip():
                if opcoes:
                    # linha em branco depois das opções: fim das opções
                    i += 1
                    break
                i += 1
                continue
            m = _RE_OPCAO.match(l)
            if not m:
                break
            chave = m.group(1)
            if chave in chaves:
                raise RodadaMalformada(f'pergunta "{titulo}" com opção repetida: {chave}')
            chaves.add(chave)
            opcoes.append({"chave": chave, "texto": m.group(2).strip()})
            i += 1
        # fase 3: bloco json (proposta)
        proposta = None
        resto = corpo_linhas[i:]
        j = 0
        while j < len(resto) and not resto[j].strip():
            j += 1
        if j < len(resto) and resto[j].strip().startswith("```"):
            fim = next((k for k in range(j + 1, len(resto)) if resto[k].strip() == "```"), None)
            if fim is None:
                raise RodadaMalformada(f'pergunta "{titulo}" com bloco ``` sem fechamento')
            bruto = "\n".join(resto[j + 1:fim])
            if tipo == "proposta":
                proposta = _parse_proposta(bruto, titulo)
            resto = resto[fim + 1:]
        porque = "\n".join(resto).strip() or None
        if tipo == "proposta" and proposta is None:
            raise RodadaMalformada(f'pergunta "{titulo}" do tipo proposta sem bloco json')
        if tipo in ("escolha", "varias"):
            if not opcoes:
                raise RodadaMalformada(f'pergunta "{titulo}" do tipo {tipo} sem opções')
            for r in recomendada:
                if r not in chaves:
                    raise RodadaMalformada(f'pergunta "{titulo}" recomenda opção inexistente: {r}')
        perguntas.append({
            "id": pid, "titulo": titulo, "tipo": tipo, "recomendada": recomendada, "opcoes": opcoes,
            "porque": porque, "proposta": proposta,
        })
    return perguntas


def _escalar(valor) -> bool:
    """Um valor de célula de proposta: texto, número, true/false ou null (nunca lista nem objeto)."""
    return valor is None or isinstance(valor, (str, int, float, bool))


def validar_proposta(dados, onde: str) -> dict:
    """Regras da §4.1 para a proposta-base de uma pergunta (na rodada e no retrato gravado na caixa).

    ``colunas`` é lista de textos não vazios, sem repetição e sem "id"; ``linhas`` é lista de objetos com
    ``id`` texto único e só colunas conhecidas, cada célula escalar; ``pode`` ⊆ operações da proposta.
    Levanta ``ValueError`` com ``onde`` na frente; devolve ``{colunas, linhas, pode}``.
    """
    if not isinstance(dados, dict):
        raise ValueError(f"{onde}: a proposta precisa ser um objeto JSON")
    colunas = dados.get("colunas")
    linhas = dados.get("linhas")
    pode = dados.get("pode", [])
    if not isinstance(colunas, list) or not colunas or not all(isinstance(c, str) and c for c in colunas):
        raise ValueError(f"{onde}: proposta sem colunas válidas (lista de textos)")
    if len(set(colunas)) != len(colunas) or "id" in colunas:
        raise ValueError(f'{onde}: colunas repetidas ou chamada "id"')
    if not isinstance(linhas, list):
        raise ValueError(f"{onde}: proposta sem linhas")
    ids: set[str] = set()
    for l in linhas:
        if not isinstance(l, dict) or not isinstance(l.get("id"), str) or not l["id"]:
            raise ValueError(f"{onde}: linha da proposta sem id")
        if l["id"] in ids:
            raise ValueError(f"{onde}: id de linha repetido: {l['id']}")
        ids.add(l["id"])
        for chave, valor in l.items():
            if chave == "id":
                continue
            if chave not in colunas:
                raise ValueError(f"{onde}: linha {l['id']} com coluna desconhecida: {chave}")
            if not _escalar(valor):
                raise ValueError(f"{onde}: linha {l['id']}, célula {chave} precisa ser texto, número, "
                                 "true/false ou null (não lista nem objeto)")
    if not isinstance(pode, list) or not all(p in OPERACOES_PROPOSTA for p in pode):
        raise ValueError(f'{onde}: "pode" com operação desconhecida')
    return {"colunas": colunas, "linhas": linhas, "pode": pode}


def _parse_proposta(bruto: str, titulo: str) -> dict:
    try:
        dados = json.loads(bruto)
    except ValueError as e:
        raise RodadaMalformada(f'pergunta "{titulo}" com JSON da proposta inválido: {e}') from None
    try:
        return validar_proposta(dados, f'pergunta "{titulo}"')
    except ValueError as e:
        raise RodadaMalformada(str(e)) from None


def ler_rodada(caminho: str, rid: str, problemas: Problemas, nome_relativo: str) -> dict:
    """Uma rodada: frontmatter, contexto, perguntas; malformada vira ``malformada: true`` + erro."""
    rodada = {
        "id": rid, "titulo": None, "ticket": None, "ticket_titulo": None, "aberta": None, "estado": None,
        "carta": None, "contexto": None, "base": None, "perguntas": [], "respondida": False,
        "ultima_resposta": None, "malformada": False, "erro": None, "arquivo": nome_relativo,
    }

    def malformar(erro: str) -> dict:
        rodada["malformada"] = True
        rodada["erro"] = erro
        rodada["perguntas"] = []
        problemas.anotar(nome_relativo, f"rodada malformada: {erro}")
        return rodada

    try:
        with open(caminho, "rb") as f:
            bruto = f.read()
    except OSError as e:
        return malformar(f"arquivo não pôde ser lido: {e.strerror or e}")
    rodada["base"] = hashlib.sha256(bruto).hexdigest()
    try:
        texto = bruto.decode("utf-8-sig").replace("\r\n", "\n").replace("\r", "\n")
    except UnicodeDecodeError:
        return malformar("arquivo não está em UTF-8")
    campos, corpo, erro = ler_frontmatter(texto)
    if campos is None:
        return malformar(erro or "frontmatter inválido")
    rodada["titulo"] = campos.get("titulo") or None
    rodada["ticket"] = campos.get("ticket") or None
    rodada["aberta"] = campos.get("aberta") or None
    rodada["estado"] = campos.get("estado") or None
    rodada["carta"] = campos.get("carta") or None
    partes = corpo.split("\n## ", 1)
    contexto = partes[0]
    if contexto.startswith("## "):
        contexto = ""
    rodada["contexto"] = contexto.strip()
    faltam = [c for c in ("titulo", "ticket", "aberta", "estado") if not rodada[c]]
    if faltam:
        return malformar("frontmatter sem " + ", ".join(faltam))
    if not _RE_DATA.fullmatch(rodada["aberta"]):
        return malformar(f"aberta fora do formato AAAA-MM-DD: {rodada['aberta']!r}")
    if rodada["estado"] not in ESTADOS_RODADA:
        return malformar(f"estado desconhecido: {rodada['estado']!r}")
    try:
        rodada["perguntas"] = _parse_perguntas(corpo)
    except RodadaMalformada as e:
        return malformar(str(e))
    if not rodada["perguntas"]:
        return malformar("rodada sem perguntas")
    return rodada


def ler_rodadas(projeto: Projeto, tickets: list[dict], cartas: list[dict], problemas: Problemas) -> list[dict]:
    pasta = projeto.rodadas
    if not pasta:
        return []  # o problema de confinamento já foi anotado no projeto.json
    try:
        nomes = sorted(os.listdir(pasta))
    except OSError as e:
        problemas.anotar(projeto.relativo(pasta), f"pasta de rodadas não pôde ser lida: {e.strerror or e}")
        return []
    titulos = {t["numero"]: t["titulo"] for t in tickets}
    ids_cartas = {c["id"] for c in cartas}
    rodadas: list[dict] = []
    pasta_real = os.path.realpath(pasta)
    for nome in nomes:
        if not nome.endswith(".md") or nome.startswith("."):
            continue
        caminho = os.path.join(pasta, nome)
        if not os.path.isfile(caminho):
            continue
        if not arquivo_confinado(caminho, pasta_real):
            problemas.anotar(projeto.relativo(pasta) + "/" + nome,
                             "rodada ignorada: o arquivo real fica fora da pasta de rodadas (atalho ou junction)")
            continue
        rid = nome[:-3]
        rodada = ler_rodada(caminho, rid, problemas, projeto.relativo(caminho))
        if rodada["ticket"] is not None:
            rodada["ticket_titulo"] = titulos.get(rodada["ticket"])
            if rodada["ticket_titulo"] is None and not rodada["malformada"]:
                problemas.anotar(rodada["arquivo"], f"rodada aponta para ticket inexistente: {rodada['ticket']}")
        if rodada["carta"] is not None and rodada["carta"] not in ids_cartas and not rodada["malformada"]:
            problemas.anotar(rodada["arquivo"], f"rodada aponta para carta inexistente: {rodada['carta']}")
        rodadas.append(rodada)
    rodadas.sort(key=lambda r: r["id"])
    return rodadas


# ----------------------------------------------------------------------------------------------
# Caixa (leitura) e fila de avisos (leitura)
# ----------------------------------------------------------------------------------------------


def ler_avisos_json(pasta_caixa: str) -> dict | None:
    """O ``.avisos.json`` como dict ``envio → registro``; ``None`` se ausente; levanta se ilegível."""
    caminho = os.path.join(pasta_caixa, ".avisos.json")
    if not os.path.exists(caminho):
        return None
    try:
        with open(caminho, "r", encoding="utf-8-sig") as f:
            dados = json.load(f)
    except UnicodeDecodeError:
        raise ValueError("arquivo não é UTF-8 válido") from None
    if not isinstance(dados, dict):
        raise ValueError("fila de avisos não é um objeto JSON")
    return dados


def validar_registro_de_aviso(envio, reg) -> str | None:
    """Um registro ``envio → {...}`` da fila está na forma? Devolve o motivo em palavras, ou ``None``.

    Chave UUID; ``estado`` ∈ pendente, enviando, entregue, falhou; ``tentativas`` inteiro ≥ 0;
    ``ultimo_erro`` texto ou null; ``proximo`` hora ISO 8601 ou null.
    """
    if not envio_valido(envio):
        return "a chave não é um UUID"
    if not isinstance(reg, dict):
        return "o registro não é um objeto JSON"
    if reg.get("estado") not in ESTADOS_AVISO:
        return f"estado desconhecido: {reg.get('estado')!r}"
    tentativas = reg.get("tentativas", 0)
    if isinstance(tentativas, bool) or not isinstance(tentativas, int) or tentativas < 0:
        return f"tentativas precisa ser um inteiro maior ou igual a zero, não {tentativas!r}"
    if reg.get("ultimo_erro") is not None and not isinstance(reg["ultimo_erro"], str):
        return "ultimo_erro precisa ser texto ou null"
    if reg.get("proximo") is not None and not hora_iso_valida(reg["proximo"]):
        return f"proximo precisa ser uma hora ISO 8601 ou null, não {reg['proximo']!r}"
    return None


def _texto_ou_nulo(dados: dict, chave: str) -> None:
    valor = dados.get(chave)
    if valor is not None and not isinstance(valor, str):
        raise ValueError(f"{chave} precisa ser texto ou null")


def validar_json_caixa(dados) -> dict:
    """Confere tipo e forma de cada campo de um ``.json`` da caixa na fronteira; levanta ``ValueError``.

    Tudo o que a caixa, o índice e o ``.md`` gerado consomem depois é conferido aqui, inclusive a estrutura
    interna do retrato da rodada e das respostas: um arquivo editado à mão ou corrompido é rejeitado inteiro
    (vira problema, não entra no índice, não ganha ``.md``) e nunca chega a quebrar o estado nem o arranque.
    """
    if not isinstance(dados, dict):
        raise ValueError("não é um objeto JSON")
    for chave in ("envio", "tipo", "enviada", "alvo", "corpo", "corpo_hash"):
        if chave not in dados:
            raise ValueError(f"sem o campo {chave}")
    if not envio_valido(dados["envio"]):
        raise ValueError("envio precisa ser um UUID (texto)")
    if dados["tipo"] not in TIPOS_MENSAGEM:
        raise ValueError(f"tipo desconhecido: {dados['tipo']!r}")
    if not isinstance(dados["enviada"], str) or not dados["enviada"]:
        raise ValueError("enviada precisa ser texto (hora ISO)")
    alvo = dados["alvo"]
    if not isinstance(alvo, dict) or alvo.get("tipo") not in TIPOS_ALVO \
            or not isinstance(alvo.get("id"), str) or not alvo["id"]:
        raise ValueError("alvo precisa ser um objeto com tipo (rodada, ticket, carta ou laco) e id (texto)")
    if (dados["tipo"] == "alteracao-laco") != (alvo["tipo"] == "laco"):
        raise ValueError("alvo do tipo laco só existe em alteracao-laco, e alteracao-laco só aponta um laço")
    _texto_ou_nulo(alvo, "titulo")
    if not isinstance(dados["corpo"], dict):
        raise ValueError("corpo não é um objeto JSON")
    if not isinstance(dados["corpo_hash"], str) or not re.fullmatch(r"[0-9a-f]{64}", dados["corpo_hash"]):
        raise ValueError("corpo_hash precisa ser um sha256 em hexadecimal")
    _texto_ou_nulo(dados, "substitui")
    _texto_ou_nulo(dados, "ticket")
    if dados["tipo"] == "resposta":
        por_id = _validar_retrato_da_rodada(dados.get("rodada"))
        _validar_respostas_da_mensagem(dados["corpo"].get("respostas"), por_id)
    elif dados["tipo"] == "alteracao-laco":
        _validar_alteracao_da_mensagem(dados)
    else:
        _texto_ou_nulo(dados["corpo"], "texto")
    return dados


def _validar_alteracao_da_mensagem(dados: dict) -> None:
    """Forma de um ``.json`` de ``alteracao-laco`` (§4.5): o que o ``.md`` e a leitura dos pedidos consomem.

    Corpo com ``operacao`` conhecida, ``laco`` igual ao alvo, ``execucao`` e ``revisao`` textos, os campos tipados
    de cada operação; retrato ``laco`` com id, execução, revisão e, em ``mudar-controle``, o controle inteiro.
    """
    corpo = dados["corpo"]
    alvo_id = dados["alvo"]["id"]
    op = corpo.get("operacao")
    if op not in OPERACOES_LACO:
        raise ValueError(f"corpo.operacao desconhecida: {op!r}")
    if corpo.get("laco") != alvo_id:
        raise ValueError("corpo.laco precisa ser o id do laço do alvo")
    for chave in ("execucao", "revisao"):
        if not isinstance(corpo.get(chave), str) or not corpo[chave]:
            raise ValueError(f"corpo.{chave} precisa ser texto")
    _texto_ou_nulo(corpo, "texto")
    if op in ("mudar-controle", "comentario-no") and (not isinstance(corpo.get("no"), str) or not corpo["no"]):
        raise ValueError("corpo.no precisa ser o id de um nó")
    if op == "mudar-controle":
        if not isinstance(corpo.get("controle"), str) or not corpo["controle"]:
            raise ValueError("corpo.controle precisa ser o id de um controle")
        for chave in ("antes", "depois"):
            v = corpo.get(chave)
            if not isinstance(v, dict) or set(v) != {"tipo", "valor"} or not isinstance(v["tipo"], str):
                raise ValueError(f"corpo.{chave} precisa ser um objeto {{tipo, valor}}")
    if op == "pedir-parada":
        if not isinstance(corpo.get("capacidade"), str):
            raise ValueError("corpo.capacidade precisa ser texto")
        onda = corpo.get("onda")
        if onda is not None and (isinstance(onda, bool) or not isinstance(onda, int)):
            raise ValueError("corpo.onda precisa ser um inteiro")
    retrato = dados.get("laco")
    if not isinstance(retrato, dict) or retrato.get("id") != alvo_id:
        raise ValueError("alteracao-laco sem o retrato do laço (laco.id igual ao alvo)")
    _texto_ou_nulo(retrato, "titulo")
    _texto_ou_nulo(retrato, "ticket")
    execucao = retrato.get("execucao")
    if not isinstance(execucao, dict) or not isinstance(execucao.get("id"), str):
        raise ValueError("laco.execucao precisa ser um objeto com id (texto)")
    if not isinstance(retrato.get("revisao"), str):
        raise ValueError("laco.revisao precisa ser texto")
    if not isinstance(retrato.get("capacidades"), list):
        raise ValueError("laco.capacidades precisa ser uma lista")
    no = retrato.get("no")
    if no is not None and (not isinstance(no, dict) or not isinstance(no.get("id"), str)):
        raise ValueError("laco.no precisa ser um objeto com id (texto) ou null")
    if op == "mudar-controle":
        controle = retrato.get("controle")
        if not isinstance(controle, dict) or controle.get("id") != corpo.get("controle") \
                or not isinstance(controle.get("tipo"), str):
            raise ValueError("laco.controle precisa ser o controle do pedido, com id e tipo")
        if not isinstance(controle.get("configurado"), dict):
            raise ValueError("laco.controle.configurado precisa ser um objeto")


def _validar_retrato_da_rodada(retrato) -> dict[str, dict]:
    """O retrato da rodada guardado numa resposta (§3.5): o ``.md`` é gerado só dele.

    Aplica as mesmas regras da rodada (§4.1): id e tipo de cada pergunta, opções com chave e texto, recomendada
    só com opções existentes, proposta-base pela ``validar_proposta``. Devolve as perguntas por id.
    """
    if not isinstance(retrato, dict):
        raise ValueError("resposta sem o retrato da rodada")
    if not isinstance(retrato.get("id"), str) or not retrato["id"]:
        raise ValueError("rodada.id precisa ser texto")
    _texto_ou_nulo(retrato, "titulo")
    _texto_ou_nulo(retrato, "base")
    _texto_ou_nulo(retrato, "ticket")
    perguntas = retrato.get("perguntas")
    if not isinstance(perguntas, list):
        raise ValueError("rodada.perguntas precisa ser uma lista")
    por_id: dict[str, dict] = {}
    for i, p in enumerate(perguntas):
        onde = f"rodada.perguntas[{i}]"
        if not isinstance(p, dict) or not isinstance(p.get("id"), str) or not p["id"]:
            raise ValueError(f"{onde} precisa ser um objeto com id (texto)")
        if p["id"] in por_id:
            raise ValueError(f"{onde}: id de pergunta repetido: {p['id']}")
        tipo = p.get("tipo")
        if tipo not in TIPOS_PERGUNTA:
            raise ValueError(f"{onde}.tipo desconhecido: {tipo!r}")
        _texto_ou_nulo(p, "titulo")
        opcoes = p.get("opcoes")
        if opcoes is None:
            opcoes = []
        if not isinstance(opcoes, list):
            raise ValueError(f"{onde}.opcoes precisa ser uma lista de objetos com chave e texto")
        chaves: set[str] = set()
        for j, o in enumerate(opcoes):
            if not isinstance(o, dict) or not isinstance(o.get("chave"), str) or not o["chave"] \
                    or not isinstance(o.get("texto"), str):
                raise ValueError(f"{onde}.opcoes[{j}] precisa ser um objeto com chave e texto (textos)")
            if o["chave"] in chaves:
                raise ValueError(f"{onde}.opcoes[{j}]: opção repetida: {o['chave']}")
            chaves.add(o["chave"])
        recomendada = p.get("recomendada")
        if recomendada is None:
            recomendada = []
        if not isinstance(recomendada, list) or not all(isinstance(r, str) for r in recomendada):
            raise ValueError(f"{onde}.recomendada precisa ser uma lista de chaves (textos)")
        for r in recomendada:
            if r not in chaves:
                raise ValueError(f"{onde}.recomendada cita opção inexistente: {r}")
        if tipo in ("escolha", "varias") and not opcoes:
            raise ValueError(f"{onde} do tipo {tipo} sem opções")
        proposta = p.get("proposta")
        if tipo == "proposta":
            if proposta is None:
                raise ValueError(f"{onde} do tipo proposta sem a proposta-base")
            validar_proposta(proposta, f"{onde}.proposta")
        elif proposta is not None:
            raise ValueError(f"{onde}.proposta só existe em pergunta do tipo proposta")
        por_id[p["id"]] = {"tipo": tipo, "chaves": chaves,
                           "colunas": set(proposta["colunas"]) if tipo == "proposta" else set()}
    return por_id


_CHAVES_RESPOSTA = {
    "escolha": {"escolha", "outra", "comentario"}, "varias": {"escolha", "outra", "comentario"},
    "aprovar": {"veredito", "comentario"}, "texto": {"texto", "comentario"}, "proposta": {"linhas", "comentario"},
}
VEREDITOS_RESPOSTA = ("aprovado", "aprovado-com-ajuste", "recusado")


def _validar_respostas_da_mensagem(respostas, por_id: dict[str, dict]) -> None:
    """``corpo.respostas`` de uma resposta gravada: cada uma com a forma da §3.4 para o tipo da pergunta.

    Só estrutura e tipos (o que o ``.md`` consome): chaves conhecidas, textos onde há texto, escolha como lista
    de chaves existentes, veredito conhecido, linhas da proposta como objetos com ``id`` texto, ``ativa``
    true/false e ``valores`` com colunas conhecidas e células escalares.
    """
    if not isinstance(respostas, dict):
        raise ValueError("corpo.respostas precisa ser um objeto id → resposta")
    for pid, r in respostas.items():
        onde = f"corpo.respostas.{pid}"
        if pid not in por_id:
            raise ValueError(f"{onde}: a pergunta não existe no retrato da rodada")
        if not isinstance(r, dict):
            raise ValueError(f"{onde} precisa ser um objeto")
        pergunta = por_id[pid]
        tipo = pergunta["tipo"]
        desconhecidas = sorted(set(r) - _CHAVES_RESPOSTA[tipo])
        if desconhecidas:
            raise ValueError(f"{onde}: chave desconhecida para pergunta do tipo {tipo}: {desconhecidas[0]}")
        _texto_ou_nulo(r, "comentario")
        if tipo in ("escolha", "varias"):
            escolha = r.get("escolha")
            if escolha is None:
                escolha = []
            if not isinstance(escolha, list) or not all(isinstance(e, str) for e in escolha):
                raise ValueError(f"{onde}.escolha precisa ser uma lista de chaves (textos)")
            for e in escolha:
                if e not in pergunta["chaves"]:
                    raise ValueError(f"{onde}.escolha cita opção inexistente: {e}")
            if tipo == "escolha" and len(escolha) > 1:
                raise ValueError(f"{onde}.escolha: esta pergunta aceita uma opção só")
            _texto_ou_nulo(r, "outra")
        elif tipo == "aprovar":
            veredito = r.get("veredito")
            if veredito is not None and veredito not in VEREDITOS_RESPOSTA:
                raise ValueError(f"{onde}.veredito desconhecido: {veredito!r}")
        elif tipo == "texto":
            _texto_ou_nulo(r, "texto")
        elif tipo == "proposta":
            linhas = r.get("linhas")
            if linhas is None:
                continue
            if not isinstance(linhas, list):
                raise ValueError(f"{onde}.linhas precisa ser uma lista de linhas")
            ids: set[str] = set()
            for k, linha in enumerate(linhas):
                c = f"{onde}.linhas[{k}]"
                if not isinstance(linha, dict):
                    raise ValueError(f"{c} precisa ser um objeto")
                extras = sorted(set(linha) - {"id", "ativa", "valores"})
                if extras:
                    raise ValueError(f"{c}: chave desconhecida: {extras[0]}")
                lid = linha.get("id")
                if not isinstance(lid, str) or not lid:
                    raise ValueError(f"{c}.id precisa ser texto")
                if lid in ids:
                    raise ValueError(f"{c}.id repetido: {lid}")
                ids.add(lid)
                if not isinstance(linha.get("ativa", True), bool):
                    raise ValueError(f"{c}.ativa precisa ser true ou false")
                valores = linha.get("valores")
                if valores is None:
                    valores = {}
                if not isinstance(valores, dict):
                    raise ValueError(f"{c}.valores precisa ser um objeto coluna → célula")
                for col, v in valores.items():
                    if col not in pergunta["colunas"]:
                        raise ValueError(f"{c}.valores: a coluna {col!r} não existe na proposta")
                    if not _escalar(v):
                        raise ValueError(f"{c}.valores.{col} precisa ser texto, número, true/false ou null "
                                         "(não lista nem objeto)")


def listar_caixa(pasta_caixa: str, campos_md: dict | None = None
                 ) -> tuple[dict[str, dict], dict[str, str], list[tuple[str, str]]]:
    """Lê ``caixa/``: ``(jsons válidos por nome, estado do .md por nome, erros)``.

    ``erros`` é uma lista ``(nome do arquivo, mensagem)`` para ``.json`` inválidos, ``.md`` órfãos ou
    ilegíveis e arquivos cujo caminho real sai da pasta. Ignora ``.tmp/`` e arquivos começando com ponto.
    Um ``.json`` inválido não entra em ``jsons``: não é indexado nem tem o ``.md`` regerado.
    ``campos_md``, quando dado, recebe ``nome → frontmatter inteiro`` de cada ``.md`` com ``.json`` (``None`` se
    ilegível ou malformado): é o que a leitura dos desfechos de ``alteracao-laco`` usa (§4.5).
    """
    jsons: dict[str, dict] = {}
    mds: dict[str, str] = {}
    erros: list[tuple[str, str]] = []
    try:
        nomes = sorted(os.listdir(pasta_caixa))
    except OSError as e:
        raise OSError(f"pasta da caixa não pôde ser lida: {e.strerror or e}") from e
    pasta_real = os.path.realpath(pasta_caixa)
    for nome in nomes:
        if nome.startswith("."):
            continue
        caminho = os.path.join(pasta_caixa, nome)
        if not os.path.isfile(caminho):
            continue
        if not arquivo_confinado(caminho, pasta_real):
            erros.append((nome, "arquivo ignorado: o caminho real fica fora da pasta da caixa (atalho ou junction)"))
            continue
        base, ext = os.path.splitext(nome)
        if ext == ".json":
            try:
                with open(caminho, "r", encoding="utf-8-sig") as f:
                    jsons[base] = validar_json_caixa(json.load(f))
            except UnicodeDecodeError:
                erros.append((nome, "mensagem inválida: arquivo não é UTF-8 válido"))
            except (OSError, ValueError) as e:
                erros.append((nome, f"mensagem inválida: {e}"))
        elif ext == ".md":
            mds[base] = caminho
    estados: dict[str, str | None] = {}
    for base, caminho in mds.items():
        if base not in jsons:
            erros.append((os.path.basename(caminho), "mensagem sem dados: o .json irmão não existe"))
            continue
        try:
            campos, _, _ = ler_frontmatter(ler_texto(caminho))
        except (OSError, ValueError) as e:
            erros.append((os.path.basename(caminho), f"vista não pôde ser lida: {motivo_de_leitura(e)}"))
            campos = None
        estados[base] = (campos or {}).get("estado") if campos else None
        if campos_md is not None:
            campos_md[base] = campos
    return jsons, estados, erros


def ler_caixa(projeto: Projeto, tickets: list[dict], cartas: list[dict], rodadas: list[dict],
              problemas: Problemas, bases: dict[str, str | None] | None = None) -> list[dict]:
    """Uma entrada por ``.json`` válido da caixa, com estado (do ``.md``) e aviso (da fila).

    ``bases``, quando dado, recebe ``arquivo → base`` de cada resposta (o sha256 da rodada respondida, do retrato
    gravado no ``.json``); fica fora das entradas para não mudar o esquema de ``caixa[]`` no estado.
    """
    pasta = projeto.caixa
    if not pasta:
        return []  # o problema de confinamento já foi anotado no projeto.json
    try:
        jsons, estados, erros = listar_caixa(pasta)
    except OSError as e:
        problemas.anotar(projeto.relativo(pasta), str(e))
        return []
    for nome, msg in erros:
        problemas.anotar(projeto.relativo(os.path.join(pasta, nome)), msg)
    nome_avisos = projeto.relativo(os.path.join(pasta, ".avisos.json"))
    try:
        brutos = ler_avisos_json(pasta) or {}
    except (OSError, ValueError) as e:
        problemas.anotar(nome_avisos, f"fila de avisos ilegível, recomeça vazia: {e}")
        brutos = {}
    avisos: dict[str, dict] = {}
    for envio, reg in brutos.items():
        motivo = validar_registro_de_aviso(envio, reg)
        if motivo is None:
            avisos[envio] = reg
        else:
            problemas.anotar(nome_avisos, f"registro {envio!r} descartado da fila: {motivo}")
    titulos = {
        "rodada": {r["id"]: r["titulo"] for r in rodadas},
        "ticket": {t["numero"]: t["titulo"] for t in tickets},
        "carta": {c["id"]: c["titulo"] for c in cartas},
    }
    substituidas = {d.get("substitui") for d in jsons.values() if d.get("substitui")}
    caixa: list[dict] = []
    for nome in sorted(jsons):
        d = jsons[nome]
        alvo = d["alvo"]
        if bases is not None and d["tipo"] == "resposta":
            bases[nome] = (d.get("rodada") or {}).get("base")
        registro = avisos.get(d["envio"])
        aviso = registro["estado"] if registro else None
        caixa.append({
            "arquivo": nome,
            "tipo": d["tipo"],
            "alvo": {"tipo": alvo["tipo"], "id": alvo["id"],
                     "titulo": alvo.get("titulo") or titulos.get(alvo["tipo"], {}).get(alvo["id"])},
            "ticket": d.get("ticket"),
            "enviada": d["enviada"],
            "envio": d["envio"],
            # .json sem .md (queda entre os passos 1 e 2): o .md regerado dirá "nova"
            "estado": estados.get(nome, "nova"),
            "aviso": aviso,
            "substitui": d.get("substitui"),
            "substituida": nome in substituidas,
        })
    return caixa


def ligar_respostas(rodadas: list[dict], caixa: list[dict], bases: dict[str, str | None] | None = None) -> None:
    """Preenche ``respondida`` e ``ultima_resposta`` de cada rodada a partir da caixa.

    ``respondida`` quer dizer "respondida na versão atual": uma rodada ``aberta`` cuja resposta mais nova foi feita
    sobre outro ``base`` (o maestro reescreveu o arquivo depois) volta a esperar o Gustavo; ``ultima_resposta``
    continua apontando a resposta anterior, que a tela mostra como histórico e que a resposta nova substitui.
    Rodada ``absorvida`` ou ``suspensa`` nunca volta a esperar. Resposta sem ``base`` gravado conta como atual.
    """
    bases = bases or {}
    for r in rodadas:
        respostas = [c for c in caixa if c["tipo"] == "resposta" and c["alvo"]["id"] == r["id"]]
        pontas = [c for c in respostas if not c["substituida"]] or respostas
        r["ultima_resposta"] = max(c["arquivo"] for c in pontas) if pontas else None
        base_da_resposta = bases.get(r["ultima_resposta"]) if r["ultima_resposta"] else None
        desatualizada = (r.get("estado") == "aberta" and base_da_resposta is not None
                         and r.get("base") is not None and base_da_resposta != r["base"])
        r["respondida"] = bool(respostas) and not desatualizada


# ----------------------------------------------------------------------------------------------
# Aviso (disponibilidade) e montagem do estado
# ----------------------------------------------------------------------------------------------


def resolver_executavel(exe, ambiente) -> str | None:
    """O caminho do executável do aviso (``projeto.json`` → ``aviso.executavel``), ou ``None``.

    Um nome solto é procurado no ``PATH`` do ambiente dado; um caminho com pasta (absoluto ou relativo à pasta
    atual) só precisa existir como arquivo (é assim que os testes apontam um executável falso).
    """
    if not isinstance(exe, str) or not exe:
        return None
    if os.path.dirname(exe):
        return exe if os.path.isfile(exe) else None
    return shutil.which(exe, path=ambiente.get("PATH"))


def disponibilidade_do_aviso(projeto: Projeto, ambiente) -> dict:
    """``{"disponivel", "motivo"}``: precisa das variáveis do canvas e do executável encontrável."""
    faltam = [v for v in ("MAESTRI_PIPE", "MAESTRI_TERMINAL_ID") if not ambiente.get(v)]
    if faltam:
        return {"disponivel": False, "motivo": "fora do canvas: " + " e ".join(faltam) + " ausentes"
                if len(faltam) > 1 else f"fora do canvas: {faltam[0]} ausente"}
    exe = str(projeto.aviso.get("executavel") or "")
    if not resolver_executavel(exe, ambiente):
        return {"disponivel": False, "motivo": f"executável {exe!r} não encontrado no PATH"}
    return {"disponivel": True, "motivo": None}


def montar_estado(projeto_json_path: str, ambiente=None, projeto: Projeto | None = None) -> dict:
    """Monta a resposta inteira de ``GET /api/estado`` lendo os arquivos agora."""
    if ambiente is None:
        ambiente = os.environ
    problemas = Problemas()
    if projeto is None:
        projeto = Projeto(projeto_json_path)
    nome_projeto_json = projeto.relativo(projeto.caminho_json)
    for mensagem in projeto.problemas_config:
        problemas.anotar(nome_projeto_json, mensagem)
    # caminho confinado fora da base (§3.2): o item fica vazio; o problema já está anotado acima
    if projeto.mapa:
        destino, decisoes, fora = ler_mapa(projeto.mapa, projeto.criterios, problemas,
                                           projeto.relativo(projeto.mapa), nome_projeto_json)
    else:
        destino, decisoes, fora = {"texto": "", "criterios": []}, [], {"nao_especificado": [], "fora_do_escopo": []}
    tickets = ler_tickets(projeto.tickets, projeto, problemas) if projeto.tickets else []
    plano = plano_de_voo(tickets, problemas)
    radar = ler_radar(projeto.estrategia, problemas, projeto.relativo(projeto.estrategia)) if projeto.estrategia else []
    glossario = ler_glossario(projeto.glossario, problemas, projeto.relativo(projeto.glossario)) if projeto.glossario else []
    cartas = ler_cartas(projeto, tickets, problemas)
    por_ticket: dict[str, list[str]] = {}
    for c in cartas:
        if isinstance(c["ticket"], str):
            por_ticket.setdefault(c["ticket"], []).append(c["id"])
    for t in tickets:
        t["cartas"] = por_ticket.get(t["numero"], [])
    rodadas = ler_rodadas(projeto, tickets, cartas, problemas)
    bases_das_respostas: dict[str, str | None] = {}
    caixa = ler_caixa(projeto, tickets, cartas, rodadas, problemas, bases_das_respostas)
    ligar_respostas(rodadas, caixa, bases_das_respostas)
    return {
        "projeto": {"nome": projeto.nome, "gerado_em": agora_iso(), "codigos": projeto.codigos},
        "destino": destino,
        "tickets": tickets,
        "plano_de_voo": plano,
        "decisoes": decisoes,
        "fora": fora,
        "radar": radar,
        "glossario": glossario,
        "cartas": cartas,
        "rodadas": rodadas,
        "caixa": caixa,
        "aviso": disponibilidade_do_aviso(projeto, ambiente),
        "problemas": problemas.lista(),
    }
