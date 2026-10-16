"""Laços (§4.4 e §4.5): leitura só leitura dos laços registrados e validação dos pedidos ``alteracao-laco``.

Um laço é descrito pelo ``laco.json`` que o maestro escreve na pasta do laço; o registro ``lacos.json`` (na pasta
do portal, caminho no ``projeto.json``) diz quais laços existem. Tudo é relido a cada pedido. O portal **só lê** a
pasta do laço: nunca grava, cria nem executa nada ali. Caminhos do ``laco.json`` são relativos à pasta do laço, sem
``..``, sem absoluto, sem componente com ponto, e confinados por ``realpath`` + ``commonpath``. SQLite é aberto com
``file:<caminho real>?mode=ro`` (``uri=True``), ``timeout`` de 2 s e ``PRAGMA query_only=ON``, uma conexão por
leitura, fechada logo depois (nunca ``immutable=1``, que ignoraria o WAL).

Pontos de entrada (a torre chama): ``resumo_dos_lacos`` (``GET /api/lacos``), ``detalhe_do_laco``
(``GET /api/laco/<id>``), ``problemas_dos_lacos`` (vão para ``problemas`` de ``GET /api/estado``) e
``validar_alteracao`` (o ``POST /api/caixa`` de ``tipo: alteracao-laco``).

Só biblioteca padrão.
"""

from __future__ import annotations

import datetime as _dt
import hashlib
import json
import math
import os
import pathlib
import re
import sqlite3

try:
    from . import leitores
except ImportError:  # executado como script solto (python nucleo/torre.py)
    import leitores  # type: ignore

FORMATO = 1
PAPEIS = ("etapa", "decisao", "controle", "observador", "fora-dos-scripts")
TIPOS_LIGACAO = ("segue", "repete", "condiciona", "observa")
TIPOS_CONTROLE = ("numero", "inteiro", "duracao", "escolha", "lista", "texto-curto")
TIPOS_CONTADOR = ("inteiro", "numero", "texto", "hora", "lista", "contagem", "serie")
QUANDO_VALE = ("agora", "proxima-onda", "ao-reiniciar", "proxima-execucao")
RELEITURA = ("continua", "ao-ligar", "manual")
UNIDADES_DURACAO = ("s", "min", "h")
CAPACIDADES = ("parar-apos-onda", "parar-de-despachar", "pausar-retomar")
OPERACOES = leitores.OPERACOES_LACO
COMENTARIOS = ("comentario-no", "comentario-laco")
PARADAS = ("pedir-parada", "pedir-pausa", "pedir-retomada")
ESTADOS = leitores.ESTADOS_ALTERACAO
EFEITOS = ("valeu", "aguarda", "nao-confirmado")
TAMANHO_LACO = 256 * 1024
TAMANHO_ORIGEM = 16 * 1024 * 1024
CAUDA_JSONL = 64 * 1024
TEXTO_MAXIMO = 20_000
TEXTO_CURTO = 200
MOTIVO_MAXIMO = 500
# a definição de um controle que entra na revisão (§4.4): só estas chaves, as que o controle tem
CHAVES_DA_DEFINICAO = ("no", "tipo", "unidade", "escala", "faixa", "opcoes", "itens", "aceita_nulo", "quando_vale",
                       "releitura", "configurado", "em_uso", "precondicoes")

_RE_ID = re.compile(r"^[a-z0-9-]+$")
_RE_ID_CONTROLE = re.compile(r"^[a-z0-9][a-z0-9_-]*$")
_RE_IDENT = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
_RE_HEX64 = re.compile(r"^[0-9a-f]{64}$")
_FALTA = object()  # "não há valor" (linha, campo ou registro ausente): regra 2 da precedência


class LacoMalformado(ValueError):
    """O ``laco.json`` fora do contrato (§4.4): o laço aparece com selo "malformado", sem controles nem botões."""


class Recusa(Exception):
    """Um pedido ``alteracao-laco`` recusado; a torre o devolve como erro da API."""

    def __init__(self, status: int, codigo: str, mensagem: str, campo: str | None = None,
                 extra: dict | None = None) -> None:
        super().__init__(mensagem)
        self.status = status
        self.codigo = codigo
        self.mensagem = mensagem
        self.campo = campo
        self.extra = extra or {}


class _Ilegivel(Exception):
    """Uma origem que não pôde ser lida: só aquele número fica "ilegível" (nunca torna o laço malformado)."""


# ----------------------------------------------------------------------------------------------
# Horas e tipos de valor
# ----------------------------------------------------------------------------------------------


def _iso(instante: _dt.datetime | None) -> str | None:
    return instante.astimezone().isoformat(timespec="seconds") if instante else None


def _instante_de_texto(texto) -> _dt.datetime | None:
    """ISO 8601 → hora com fuso (sem fuso: hora local); ``None`` se não é hora."""
    if not isinstance(texto, str) or not texto:
        return None
    try:
        instante = _dt.datetime.fromisoformat(texto)
    except ValueError:
        return None
    return instante if instante.tzinfo else instante.astimezone()


def _hora_com_fuso(texto) -> _dt.datetime | None:
    """ISO 8601 **com fuso** (as chaves de desfecho exigem); ``None`` se não é."""
    if not isinstance(texto, str) or not texto:
        return None
    try:
        instante = _dt.datetime.fromisoformat(texto)
    except ValueError:
        return None
    return instante if instante.tzinfo else None


def _mtime(caminho: str) -> _dt.datetime:
    return _dt.datetime.fromtimestamp(os.stat(caminho).st_mtime).astimezone()


def _e_inteiro(v) -> bool:
    return isinstance(v, int) and not isinstance(v, bool)


def _e_numero(v) -> bool:
    return isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v)


def _uma_linha(texto: str) -> bool:
    return "\n" not in texto and "\r" not in texto


def tipo_do_valor(tipo: str, valor) -> str | None:
    """O valor (não nulo) tem a forma do tipo do controle? Devolve o motivo em palavras, ou ``None``."""
    if tipo in ("numero", "duracao"):
        return None if _e_numero(valor) else "precisa ser um número"
    if tipo == "inteiro":
        return None if _e_inteiro(valor) else "precisa ser um inteiro"
    if tipo == "escolha":
        return None if isinstance(valor, str) or _e_numero(valor) else "precisa ser o valor de uma opção"
    if tipo == "lista":
        return None if isinstance(valor, list) and all(isinstance(x, str) for x in valor) \
            else "precisa ser uma lista de textos"
    if tipo == "texto-curto":
        return None if isinstance(valor, str) else "precisa ser texto"
    return f"tipo de controle desconhecido: {tipo!r}"


def valor_valido(controle: dict, valor) -> str | None:
    """O valor cabe na definição do controle (§4.5: faixa, opções, itens, nulo)? Motivo em palavras, ou ``None``."""
    if valor is None:
        return None if controle.get("aceita_nulo") else "este controle não aceita nulo"
    tipo = controle.get("tipo")
    motivo = tipo_do_valor(tipo, valor)
    if motivo:
        return motivo
    if tipo in ("numero", "inteiro", "duracao"):
        faixa = controle.get("faixa") or [None, None]
        if not (faixa[0] <= valor <= faixa[1]):
            return f"fora da faixa {faixa[0]} a {faixa[1]}"
    elif tipo == "escolha":
        if valor not in [o.get("valor") for o in controle.get("opcoes") or []]:
            return "não está entre as opções"
    elif tipo == "lista":
        itens = controle.get("itens") or {}
        if len(set(valor)) != len(valor):
            return "item repetido (a lista é um conjunto)"
        if len(valor) > itens.get("max", 0):
            return f"passa de {itens.get('max')} itens"
        for x in valor:
            if len(x) > itens.get("comprimento", 0) or not _uma_linha(x):
                return f"item com mais de {itens.get('comprimento')} caracteres ou mais de uma linha"
        opcoes = controle.get("opcoes")
        if opcoes is not None and any(x not in [o.get("valor") for o in opcoes] for x in valor):
            return "item fora das opções"
    elif tipo == "texto-curto":
        if len(valor) > TEXTO_CURTO or not _uma_linha(valor):
            return f"passa de {TEXTO_CURTO} caracteres ou tem mais de uma linha"
    return None


def iguais(tipo: str, a, b) -> bool:
    """Dois valores de controle são o mesmo? Em ``lista``, como conjunto."""
    if tipo == "lista" and isinstance(a, list) and isinstance(b, list):
        return set(a) == set(b)
    if isinstance(a, bool) != isinstance(b, bool):
        return False
    return a == b


# ----------------------------------------------------------------------------------------------
# Validação do laco.json (§4.4)
# ----------------------------------------------------------------------------------------------

_FORMAS = ("arquivo", "jsonl", "sqlite", "mtime", "declarado")
_CHAVES_ORIGEM = {
    "arquivo": {"arquivo", "campo", "formato", "ausente"},
    "jsonl": {"jsonl", "campo", "formato", "ausente"},
    "sqlite": {"sqlite", "tabela", "onde", "coluna", "json", "campo", "soma", "contagem", "agrupar", "formato",
               "ausente"},
    "mtime": {"mtime"},
    "declarado": {"declarado"},
}


def motivo_do_caminho(relativo) -> str | None:
    """Regra léxica de um caminho do ``laco.json``: relativo à pasta do laço, sem ``..``, sem absoluto, sem letra de
    unidade e sem componente que comece com ponto. Devolve o motivo em palavras, ou ``None``."""
    if not isinstance(relativo, str) or not relativo.strip():
        return "precisa ser um caminho relativo (texto)"
    if "\x00" in relativo:
        return "tem caractere nulo"
    if os.path.isabs(relativo) or os.path.splitdrive(relativo)[0] or relativo.startswith(("/", "\\")) \
            or re.match(r"^[A-Za-z]:", relativo):
        return "caminho absoluto não é aceito"
    for parte in re.split(r"[\\/]", relativo):
        if parte == "":
            return "tem componente vazio"
        if parte == "..":
            return "não pode ter .."
        if parte.startswith("."):
            return "não pode ter componente que começa com ponto"
        if ":" in parte:
            return "não pode ter dois-pontos"
    return None


class _Validador:
    """Valida um ``laco.json``; ``avisos`` junta o que vira problema sem tornar o laço malformado."""

    def __init__(self) -> None:
        self.avisos: list[str] = []

    @staticmethod
    def falha(mensagem: str):
        raise LacoMalformado(mensagem)

    def chaves(self, objeto: dict, permitidas, onde: str) -> None:
        for chave in objeto:
            if chave not in permitidas:
                self.avisos.append(f"{onde}: chave desconhecida ignorada: {chave}")

    def ref(self, valor, validos, onde: str, o_que: str = "nó") -> str:
        """Uma referência a um id (nó, contador): o tipo é conferido antes de procurar o id, para lista ou objeto
        virarem "malformado" e nunca ``TypeError`` num ``set`` ou ``dict``."""
        if not isinstance(valor, str):
            self.falha(f"{onde} precisa ser o id de um {o_que} (texto), não {type(valor).__name__}")
        if valor not in validos:
            self.falha(f"{onde} aponta para {o_que} inexistente: {valor!r}")
        return valor

    def texto(self, objeto: dict, chave: str, onde: str, obrigatorio: bool = True) -> str | None:
        valor = objeto.get(chave)
        if valor is None and not obrigatorio:
            return None
        if not isinstance(valor, str) or not valor.strip():
            self.falha(f"{onde}.{chave} precisa ser texto")
        return valor

    def origem(self, o, onde: str, declarado: bool = False) -> dict:
        if not isinstance(o, dict):
            self.falha(f"{onde} precisa ser uma origem (objeto)")
        formas = [f for f in _FORMAS if f in o]
        if len(formas) != 1:
            self.falha(f"{onde} precisa ter exatamente uma forma: arquivo, jsonl, sqlite, mtime"
                       + (" ou declarado" if declarado else ""))
        forma = formas[0]
        if forma == "declarado" and not declarado:
            self.falha(f"{onde}: declarado só vale em configurado")
        self.chaves(o, _CHAVES_ORIGEM[forma], onde)
        if forma == "declarado":
            return {"forma": "declarado", "declarado": o["declarado"], "bruta": o}
        motivo = motivo_do_caminho(o[forma])
        if motivo:
            self.falha(f"{onde}: o caminho {o[forma]!r} {motivo} (fica fora da pasta do laço)")
        n: dict = {"forma": forma, "caminho": o[forma], "bruta": o, "campo": None, "formato": None,
                   "tem_ausente": "ausente" in o, "ausente": o.get("ausente")}
        if "campo" in o:
            n["campo"] = self.texto(o, "campo", onde)
        if "formato" in o:
            if o["formato"] not in ("iso", "epoch"):
                self.falha(f"{onde}.formato precisa ser iso ou epoch")
            n["formato"] = o["formato"]
        if forma == "sqlite":
            tabela = o.get("tabela")
            if not isinstance(tabela, str) or not _RE_IDENT.fullmatch(tabela):
                self.falha(f"{onde}.tabela precisa casar [A-Za-z_][A-Za-z0-9_]*")
            n["tabela"] = tabela
            modos = [m for m in ("onde", "soma", "contagem") if m in o]
            if len(modos) != 1:
                self.falha(f"{onde}: SQLite precisa de exatamente um de onde (uma linha), soma ou contagem")
            n["modo"] = modos[0]
            if n["modo"] == "onde":
                onde_ = o["onde"]
                if not isinstance(onde_, dict) or not onde_:
                    self.falha(f"{onde}.onde precisa ser um objeto coluna → valor")
                for k, v in onde_.items():
                    if not _RE_IDENT.fullmatch(k):
                        self.falha(f"{onde}.onde: a coluna {k!r} precisa casar [A-Za-z_][A-Za-z0-9_]*")
                    if not (isinstance(v, str) or _e_numero(v)):
                        self.falha(f"{onde}.onde.{k} precisa ser texto ou número")
                coluna = o.get("coluna")
                if not isinstance(coluna, str) or not _RE_IDENT.fullmatch(coluna):
                    self.falha(f"{onde}.coluna precisa casar [A-Za-z_][A-Za-z0-9_]*")
                if "json" in o and not isinstance(o["json"], bool):
                    self.falha(f"{onde}.json precisa ser true ou false")
                n.update(onde=dict(onde_), coluna=coluna, json=bool(o.get("json", False)))
            else:
                for chave in ("coluna", "json", "campo"):
                    if chave in o:
                        self.falha(f"{onde}.{chave} só existe no SQLite de uma linha (onde)")
                if n["modo"] == "soma":
                    if not isinstance(o["soma"], str) or not _RE_IDENT.fullmatch(o["soma"]):
                        self.falha(f"{onde}.soma precisa casar [A-Za-z_][A-Za-z0-9_]*")
                    n["soma"] = o["soma"]
                else:
                    if o["contagem"] is not True:
                        self.falha(f"{onde}.contagem precisa ser true")
                    agrupar = o.get("agrupar")
                    if agrupar is not None and (not isinstance(agrupar, str) or not _RE_IDENT.fullmatch(agrupar)):
                        self.falha(f"{onde}.agrupar precisa casar [A-Za-z_][A-Za-z0-9_]*")
                    n["agrupar"] = agrupar
            if "agrupar" in o and n["modo"] != "contagem":
                self.falha(f"{onde}.agrupar só existe na contagem")
        return n

    def controle(self, c, i: int, nos: set[str]) -> dict:
        onde = f"controles[{i}]"
        if not isinstance(c, dict):
            self.falha(f"{onde} precisa ser um objeto")
        self.chaves(c, {"id", "no", "rotulo", "tipo", "faixa", "opcoes", "itens", "unidade", "escala", "aceita_nulo",
                        "nulo", "quando_vale", "releitura", "configurado", "em_uso", "precondicoes"}, onde)
        cid = c.get("id")
        if not isinstance(cid, str) or not _RE_ID_CONTROLE.fullmatch(cid):
            self.falha(f"{onde}.id precisa casar [a-z0-9][a-z0-9_-]*")
        onde = f"controle {cid}"
        self.ref(c.get("no"), nos, f"{onde}.no")
        self.texto(c, "rotulo", onde)
        tipo = c.get("tipo")
        if tipo not in TIPOS_CONTROLE:
            self.falha(f"{onde}: tipo desconhecido: {tipo!r}")
        n = {"id": cid, "no": c["no"], "rotulo": c["rotulo"], "tipo": tipo, "faixa": None, "opcoes": None,
             "itens": None, "unidade": None, "escala": None, "aceita_nulo": False, "nulo": None,
             "quando_vale": None, "releitura": None, "bruta": c}
        if tipo in ("numero", "inteiro", "duracao"):
            faixa = c.get("faixa")
            if not isinstance(faixa, list) or len(faixa) != 2 or not all(_e_numero(x) for x in faixa):
                self.falha(f"{onde}: {tipo} exige faixa [mínimo, máximo] com números")
            if tipo == "inteiro" and not all(_e_inteiro(x) for x in faixa):
                self.falha(f"{onde}: a faixa de um inteiro precisa ser de inteiros")
            if faixa[0] > faixa[1]:
                self.falha(f"{onde}: faixa invertida ({faixa[0]} > {faixa[1]})")
            n["faixa"] = list(faixa)
        elif "faixa" in c:
            self.falha(f"{onde}: faixa só existe em numero, inteiro e duracao")
        if tipo == "escolha" or (tipo == "lista" and "opcoes" in c):
            opcoes = c.get("opcoes")
            if not isinstance(opcoes, list) or not opcoes:
                self.falha(f"{onde}: {tipo} exige opcoes (lista não vazia)" if tipo == "escolha"
                           else f"{onde}: opcoes precisa ser uma lista não vazia")
            valores = []
            for j, o in enumerate(opcoes):
                if not isinstance(o, dict) or not (isinstance(o.get("valor"), str) or _e_numero(o.get("valor"))) \
                        or not isinstance(o.get("rotulo"), str):
                    self.falha(f"{onde}.opcoes[{j}] precisa ser {{valor, rotulo}}")
                if tipo == "lista" and not isinstance(o["valor"], str):
                    self.falha(f"{onde}.opcoes[{j}]: numa lista o valor é texto")
                valores.append(o["valor"])
            if len(set(map(repr, valores))) != len(valores):
                self.falha(f"{onde}: valores de opção repetidos")
            n["opcoes"] = [{"valor": o["valor"], "rotulo": o["rotulo"]} for o in opcoes]
        elif "opcoes" in c:
            self.falha(f"{onde}: opcoes só existe em escolha e lista")
        if tipo == "lista":
            itens = c.get("itens")
            if not isinstance(itens, dict) or not _e_inteiro(itens.get("max")) or itens["max"] < 1 \
                    or not _e_inteiro(itens.get("comprimento")) or itens["comprimento"] < 1:
                self.falha(f"{onde}: lista exige itens {{max, comprimento}} (inteiros ≥ 1)")
            n["itens"] = {"max": itens["max"], "comprimento": itens["comprimento"]}
        elif "itens" in c:
            self.falha(f"{onde}: itens só existe em lista")
        if tipo == "duracao":
            if c.get("unidade") not in UNIDADES_DURACAO:
                self.falha(f"{onde}: duracao exige unidade s, min ou h")
            n["unidade"] = c["unidade"]
        elif "unidade" in c:
            n["unidade"] = self.texto(c, "unidade", onde)
        if "escala" in c:
            if c["escala"] != "porcento" or tipo != "numero":
                self.falha(f"{onde}: escala só pode ser porcento, num controle numero")
            n["escala"] = "porcento"
        if "aceita_nulo" in c:
            if not isinstance(c["aceita_nulo"], bool):
                self.falha(f"{onde}.aceita_nulo precisa ser true ou false")
            n["aceita_nulo"] = c["aceita_nulo"]
        if "nulo" in c:
            n["nulo"] = self.texto(c, "nulo", onde)
        if c.get("quando_vale") not in QUANDO_VALE:
            self.falha(f"{onde}.quando_vale precisa ser agora, proxima-onda, ao-reiniciar ou proxima-execucao")
        if c.get("releitura") not in RELEITURA:
            self.falha(f"{onde}.releitura precisa ser continua, ao-ligar ou manual")
        n["quando_vale"], n["releitura"] = c["quando_vale"], c["releitura"]
        if "configurado" not in c:
            self.falha(f"{onde} sem configurado")
        n["configurado"] = self.origem(c["configurado"], f"{onde}.configurado", declarado=True)
        n["em_uso"] = self.origem(c["em_uso"], f"{onde}.em_uso") if "em_uso" in c else None
        pre = c.get("precondicoes", {})
        if not isinstance(pre, dict):
            self.falha(f"{onde}.precondicoes precisa ser um objeto nome → origem")
        n["precondicoes"] = {}
        for nome, o in pre.items():
            if not _RE_ID_CONTROLE.fullmatch(nome):
                self.falha(f"{onde}.precondicoes: nome fora do formato: {nome!r}")
            n["precondicoes"][nome] = self.origem(o, f"{onde}.precondicoes.{nome}")
        return n


def validar_laco(dados, id_registro: str | None = None) -> tuple[dict, list[str]]:
    """Confere um ``laco.json`` já decodificado contra o contrato (§4.4).

    Devolve ``(laço normalizado, avisos)``; levanta ``LacoMalformado`` em palavras. Avisos (chave desconhecida,
    capacidade desconhecida) viram problema sem tornar o laço malformado. Não lê nenhuma fonte de estado.
    """
    v = _Validador()
    if not isinstance(dados, dict):
        v.falha("o laco.json precisa ser um objeto JSON")
    obrigatorias = ("formato", "id", "titulo", "ticket", "execucao", "nos", "ligacoes", "controles", "capacidades",
                    "contadores", "sinal")
    faltam = [c for c in obrigatorias if c not in dados]
    if faltam:
        v.falha("falta campo obrigatório: " + ", ".join(faltam))
    v.chaves(dados, set(obrigatorias) | {"parado", "esperando_cota"}, "laco.json")
    if not _e_inteiro(dados["formato"]) or dados["formato"] != FORMATO:
        v.falha(f"formato precisa ser {FORMATO} (a versão deste contrato), não {dados['formato']!r}")
    lid = dados["id"]
    if not isinstance(lid, str) or not _RE_ID.fullmatch(lid):
        v.falha("id precisa casar [a-z0-9-]+")
    if id_registro is not None and lid != id_registro:
        v.falha(f"o id do laco.json ({lid}) é diferente do id do registro ({id_registro})")
    v.texto(dados, "titulo", "laco.json")
    v.texto(dados, "ticket", "laco.json")

    execucao = dados["execucao"]
    if not isinstance(execucao, dict):
        v.falha("execucao precisa ser um objeto {id, inicio, terminou_em}")
    v.chaves(execucao, {"id", "inicio", "terminou_em"}, "execucao")
    if not isinstance(execucao.get("id"), str) or not _RE_ID.fullmatch(execucao["id"]):
        v.falha("execucao.id precisa casar [a-z0-9-]+")
    for chave in ("inicio", "terminou_em"):
        valor = execucao.get(chave)
        if valor is not None and _instante_de_texto(valor) is None:
            v.falha(f"execucao.{chave} precisa ser hora ISO 8601 ou null")

    if not isinstance(dados["nos"], list):
        v.falha("nos precisa ser uma lista")
    nos: list[dict] = []
    ids_nos: set[str] = set()
    for i, no in enumerate(dados["nos"]):
        if not isinstance(no, dict):
            v.falha(f"nos[{i}] precisa ser um objeto")
        v.chaves(no, {"id", "titulo", "papel", "detalhe", "carta"}, f"nos[{i}]")
        nid = no.get("id")
        if not isinstance(nid, str) or not _RE_ID.fullmatch(nid):
            v.falha(f"nos[{i}].id precisa casar [a-z0-9-]+")
        if nid in ids_nos:
            v.falha(f"id de nó repetido: {nid}")
        ids_nos.add(nid)
        v.texto(no, "titulo", f"nó {nid}")
        if no.get("papel") not in PAPEIS:
            v.falha(f"nó {nid}: papel desconhecido: {no.get('papel')!r}")
        v.texto(no, "detalhe", f"nó {nid}", obrigatorio=False)
        v.texto(no, "carta", f"nó {nid}", obrigatorio=False)
        nos.append({"id": nid, "titulo": no["titulo"], "papel": no["papel"], "detalhe": no.get("detalhe"),
                    "carta": no.get("carta")})

    if not isinstance(dados["ligacoes"], list):
        v.falha("ligacoes precisa ser uma lista")
    ligacoes: list[dict] = []
    for i, lig in enumerate(dados["ligacoes"]):
        if not isinstance(lig, dict):
            v.falha(f"ligacoes[{i}] precisa ser um objeto")
        v.chaves(lig, {"de", "para", "palavra", "tipo"}, f"ligacoes[{i}]")
        for chave in ("de", "para"):
            v.ref(lig.get(chave), ids_nos, f"ligacoes[{i}].{chave}")
        v.texto(lig, "palavra", f"ligacoes[{i}]")
        if lig.get("tipo") not in TIPOS_LIGACAO:
            v.falha(f"ligacoes[{i}]: tipo desconhecido: {lig.get('tipo')!r}")
        ligacoes.append({"de": lig["de"], "para": lig["para"], "palavra": lig["palavra"], "tipo": lig["tipo"]})

    if not isinstance(dados["controles"], list):
        v.falha("controles precisa ser uma lista")
    controles: list[dict] = []
    for i, c in enumerate(dados["controles"]):
        n = v.controle(c, i, ids_nos)
        if any(x["id"] == n["id"] for x in controles):
            v.falha(f"id de controle repetido: {n['id']}")
        controles.append(n)

    if not isinstance(dados["contadores"], list):
        v.falha("contadores precisa ser uma lista")
    contadores: list[dict] = []
    for i, c in enumerate(dados["contadores"]):
        onde = f"contadores[{i}]"
        if not isinstance(c, dict):
            v.falha(f"{onde} precisa ser um objeto")
        v.chaves(c, {"id", "no", "rotulo", "tipo", "escala", "origem", "hora", "campos"}, onde)
        cid = c.get("id")
        if not isinstance(cid, str) or not _RE_ID_CONTROLE.fullmatch(cid):
            v.falha(f"{onde}.id precisa casar [a-z0-9][a-z0-9_-]*")
        if any(x["id"] == cid for x in contadores):
            v.falha(f"id de contador repetido: {cid}")
        onde = f"contador {cid}"
        v.ref(c.get("no"), ids_nos, f"{onde}.no")
        v.texto(c, "rotulo", onde)
        if c.get("tipo") not in TIPOS_CONTADOR:
            v.falha(f"{onde}: tipo desconhecido: {c.get('tipo')!r}")
        if "escala" in c and (c["escala"] != "porcento" or c["tipo"] != "numero"):
            v.falha(f"{onde}: escala só pode ser porcento, num contador numero")
        campos = c.get("campos")
        if campos is not None and (not isinstance(campos, list) or not all(isinstance(x, str) for x in campos)):
            v.falha(f"{onde}.campos precisa ser uma lista de textos")
        if "origem" not in c:
            v.falha(f"{onde} sem origem")
        contadores.append({"id": cid, "no": c["no"], "rotulo": c["rotulo"], "tipo": c["tipo"],
                           "escala": c.get("escala"), "campos": campos,
                           "origem": v.origem(c["origem"], f"{onde}.origem"),
                           "hora": v.origem(c["hora"], f"{onde}.hora") if "hora" in c else None})

    if not isinstance(dados["capacidades"], list):
        v.falha("capacidades precisa ser uma lista")
    capacidades: list[dict] = []
    for i, cap in enumerate(dados["capacidades"]):
        if not isinstance(cap, dict) or not isinstance(cap.get("id"), str):
            v.falha(f"capacidades[{i}] precisa ser um objeto com id")
        if cap["id"] not in CAPACIDADES:
            v.avisos.append(f"capacidade desconhecida ignorada: {cap['id']}")
            continue
        if any(x["id"] == cap["id"] for x in capacidades):
            v.falha(f"capacidade repetida: {cap['id']}")
        v.chaves(cap, {"id", "onda_atual"} if cap["id"] == "parar-apos-onda" else {"id"}, f"capacidade {cap['id']}")
        onda_atual = cap.get("onda_atual") if cap["id"] == "parar-apos-onda" else None
        if onda_atual is not None:
            v.ref(onda_atual, {x["id"] for x in contadores}, "capacidade parar-apos-onda: onda_atual", "contador")
        bruta = {k: cap[k] for k in cap if k == "id" or (k == "onda_atual" and cap["id"] == "parar-apos-onda")}
        capacidades.append({"id": cap["id"], "onda_atual": onda_atual, "bruta": bruta})

    sinal = dados["sinal"]
    if not isinstance(sinal, dict) or not isinstance(sinal.get("fontes"), list):
        v.falha("sinal precisa ser um objeto {fontes, sem_sinal_apos_s}")
    v.chaves(sinal, {"fontes", "sem_sinal_apos_s"}, "sinal")
    if not _e_inteiro(sinal.get("sem_sinal_apos_s")) or sinal["sem_sinal_apos_s"] < 1:
        v.falha("sinal.sem_sinal_apos_s precisa ser um inteiro ≥ 1")
    fontes = [v.origem(o, f"sinal.fontes[{i}]") for i, o in enumerate(sinal["fontes"])]

    parado = v.origem(dados["parado"], "parado") if "parado" in dados else None
    cota = None
    if "esperando_cota" in dados:
        ec = dados["esperando_cota"]
        if not isinstance(ec, dict) or "aptos" not in ec or "fora" not in ec:
            v.falha("esperando_cota precisa ser {aptos, fora} (duas origens)")
        v.chaves(ec, {"aptos", "fora"}, "esperando_cota")
        cota = {"aptos": v.origem(ec["aptos"], "esperando_cota.aptos"),
                "fora": v.origem(ec["fora"], "esperando_cota.fora")}

    laco = {"id": lid, "titulo": dados["titulo"], "ticket": dados["ticket"],
            "execucao": {"id": execucao["id"], "inicio": execucao.get("inicio"),
                         "terminou_em": execucao.get("terminou_em")},
            "nos": nos, "ligacoes": ligacoes, "controles": controles, "capacidades": capacidades,
            "contadores": contadores, "sinal": {"fontes": fontes, "sem_sinal_apos_s": sinal["sem_sinal_apos_s"]},
            "parado": parado, "esperando_cota": cota}
    return laco, v.avisos


def carregar_laco(entrada: dict) -> tuple[dict, list[str]]:
    """Lê e valida o ``laco.json`` de uma entrada do registro; levanta ``LacoMalformado`` em palavras."""
    if entrada.get("erro"):
        raise LacoMalformado(entrada["erro"])
    caminho = os.path.join(entrada["pasta_real"], "laco.json")
    try:
        if not os.path.isfile(caminho):
            raise LacoMalformado("a pasta do laço não tem laco.json")
        if not leitores.dentro_de(os.path.realpath(caminho), entrada["pasta_real"]):
            raise LacoMalformado("o laco.json é um atalho para fora da pasta do laço")
        if os.path.getsize(caminho) > TAMANHO_LACO:
            raise LacoMalformado("o laco.json passa de 256 KiB")
        dados = json.loads(leitores.ler_texto(caminho))
    except LacoMalformado:
        raise
    except UnicodeDecodeError:
        raise LacoMalformado("o laco.json não é UTF-8 válido") from None
    except ValueError as e:
        raise LacoMalformado(f"o laco.json não é JSON válido: {e}") from None
    except OSError as e:
        raise LacoMalformado(f"o laco.json não pôde ser lido: {leitores.motivo_de_leitura(e)}") from None
    return validar_laco(dados, entrada["id"])


# ----------------------------------------------------------------------------------------------
# Leitura das origens (só leitura)
# ----------------------------------------------------------------------------------------------


def descrever_origem(o: dict) -> str:
    """De onde vem um valor, curto (vai na API como ``fonte``)."""
    forma = o["forma"]
    if forma == "declarado":
        return "declarado pelo maestro"
    if forma == "mtime":
        return f"{o['caminho']} (hora do arquivo)"
    campo = f" → {o['campo']}" if o.get("campo") else ""
    if forma == "arquivo":
        return f"{o['caminho']}{campo}"
    if forma == "jsonl":
        return f"{o['caminho']} → última linha{campo.replace(' → ', '.') if campo else ''}"
    if o["modo"] == "onde":
        filtro = ", ".join(f"{k}={v}" for k, v in o["onde"].items())
        return f"{o['caminho']} → {o['tabela']}[{filtro}].{o['coluna']}{campo}"
    if o["modo"] == "soma":
        return f"{o['caminho']} → {o['tabela']} (soma de {o['soma']})"
    return f"{o['caminho']} → {o['tabela']} (contagem" + (f" por {o['agrupar']})" if o.get("agrupar") else ")")


def _pegar_campo(valor, campo: str | None):
    """``campo`` com pontos; segmento inteiro indexa lista (negativo conta do fim). Falta → ``_FALTA``."""
    if campo is None:
        return valor
    for seg in campo.split("."):
        if isinstance(valor, dict):
            if seg not in valor:
                return _FALTA
            valor = valor[seg]
        elif isinstance(valor, list) and re.fullmatch(r"-?\d+", seg):
            i = int(seg)
            if not -len(valor) <= i < len(valor):
                return _FALTA
            valor = valor[i]
        else:
            return _FALTA
    return valor


def _resolver(pasta_real: str, relativo: str) -> str:
    alvo = os.path.realpath(os.path.join(pasta_real, *re.split(r"[\\/]", relativo)))
    if not leitores.dentro_de(alvo, pasta_real):
        raise _Ilegivel("o caminho real fica fora da pasta do laço (atalho ou junction); não foi lido")
    return alvo


def _ultima_linha(caminho: str, campo: str | None):
    with open(caminho, "rb") as f:
        f.seek(0, os.SEEK_END)
        tamanho = f.tell()
        inicio = max(0, tamanho - CAUDA_JSONL)
        f.seek(inicio)
        bruto = f.read()
    linhas = bruto.split(b"\n")
    if inicio > 0:
        linhas = linhas[1:]  # a primeira pode ter sido cortada no meio
    for linha in reversed(linhas):
        texto = linha.strip()
        if not texto:
            continue
        try:
            objeto = json.loads(texto.decode("utf-8"))
        except (UnicodeDecodeError, ValueError):
            continue
        return _pegar_campo(objeto, campo)
    return _FALTA


def _ler_sqlite(caminho: str, o: dict):
    uri = pathlib.Path(caminho).as_uri() + "?mode=ro"
    try:
        con = sqlite3.connect(uri, uri=True, timeout=2)
    except sqlite3.Error as e:
        raise _Ilegivel(f"o banco não abriu: {e}") from None
    try:
        con.execute("PRAGMA query_only=ON")
        tabela = o["tabela"]
        if o["modo"] == "onde":
            filtro = " AND ".join(f'"{k}" = ?' for k in o["onde"])
            linhas = con.execute(f'SELECT "{o["coluna"]}" FROM "{tabela}" WHERE {filtro} LIMIT 2',
                                 list(o["onde"].values())).fetchall()
            if len(linhas) > 1:
                raise _Ilegivel("mais de uma linha casa o filtro")
            if not linhas:
                return _FALTA
            valor = linhas[0][0]
            if valor is None:
                return None  # NULL na coluna é um valor nulo (regra 3), não um campo ausente
            if o["json"]:
                if isinstance(valor, bytes):
                    try:
                        valor = valor.decode("utf-8")
                    except UnicodeDecodeError:
                        raise _Ilegivel("a coluna não é texto UTF-8") from None
                if not isinstance(valor, str):
                    raise _Ilegivel("a coluna não guarda texto JSON")
                try:
                    valor = json.loads(valor)
                except ValueError:
                    raise _Ilegivel("a coluna não guarda JSON válido") from None
            return _pegar_campo(valor, o.get("campo"))
        if o["modo"] == "soma":
            valor = con.execute(f'SELECT SUM("{o["soma"]}") FROM "{tabela}"').fetchone()[0]
            return 0 if valor is None else valor
        if o.get("agrupar"):
            linhas = con.execute(f'SELECT "{o["agrupar"]}", COUNT(*) FROM "{tabela}" GROUP BY "{o["agrupar"]}"'
                                 ).fetchall()
            return {("null" if k is None else str(k)): n for k, n in linhas}
        return con.execute(f'SELECT COUNT(*) FROM "{tabela}"').fetchone()[0]
    except sqlite3.Error as e:
        raise _Ilegivel(f"o banco não pôde ser lido: {e}") from None
    finally:
        con.close()


def _converter_hora(valor, formato: str) -> _dt.datetime | None:
    if formato == "iso":
        return _instante_de_texto(valor)
    if not _e_numero(valor):
        return None
    try:
        return _dt.datetime.fromtimestamp(valor).astimezone()
    except (OverflowError, OSError, ValueError):
        return None


def ler_origem(pasta_real: str, o: dict, anotar=None) -> dict:
    """Lê uma origem (§4.4). Devolve ``{valor, fonte, hora, instante, ilegivel, de_ausente}``.

    ``hora`` é a hora da leitura (arquivo e JSONL: mtime; SQLite: o mais novo entre o banco e o ``-wal``);
    ``instante`` é a hora que o próprio valor dá (``formato`` iso/epoch, ou ``mtime``). Aplica as regras 1 e 2 da
    precedência (mais de uma linha → ilegível; sem valor → ``ausente`` declarado, senão ilegível); as regras 3 (nulo)
    e 4 (tipo) ficam com quem usa o valor, porque dependem do controle ou contador. ``anotar(mensagem)`` recebe o
    problema de um caminho que sai da pasta do laço.
    """
    r = {"valor": None, "fonte": descrever_origem(o), "hora": None, "instante": None, "ilegivel": None,
         "de_ausente": False}
    if o["forma"] == "declarado":
        r["valor"] = o["declarado"]
        return r
    try:
        caminho = _resolver(pasta_real, o["caminho"])
    except _Ilegivel as e:
        r["ilegivel"] = str(e)
        if anotar:
            anotar(f"origem {o['caminho']}: {e}")
        return r
    try:
        if not os.path.exists(caminho):
            raise _Ilegivel("o arquivo não existe")
        if not os.path.isfile(caminho):
            raise _Ilegivel("não é um arquivo")
        if os.path.getsize(caminho) > TAMANHO_ORIGEM:
            raise _Ilegivel("o arquivo passa de 16 MiB")
        hora = _mtime(caminho)
        if o["forma"] == "mtime":
            valor = hora
        elif o["forma"] == "arquivo":
            valor = _pegar_campo(json.loads(leitores.ler_texto(caminho)), o.get("campo"))
        elif o["forma"] == "jsonl":
            valor = _ultima_linha(caminho, o.get("campo"))
        else:
            wal = caminho + "-wal"
            if os.path.isfile(wal):
                hora = max(hora, _mtime(wal))
            valor = _ler_sqlite(caminho, o)
    except _Ilegivel as e:
        r["ilegivel"] = str(e)
        return r
    except UnicodeDecodeError:
        r["ilegivel"] = "arquivo não é UTF-8 válido"
        return r
    except ValueError as e:
        r["ilegivel"] = f"JSON inválido: {e}"
        return r
    except OSError as e:
        r["ilegivel"] = leitores.motivo_de_leitura(e)
        return r
    r["hora"] = hora
    if o["forma"] == "mtime":
        r["instante"], r["valor"] = hora, _iso(hora)
        return r
    if valor is _FALTA:
        if not o.get("tem_ausente"):
            r["ilegivel"] = "sem valor (a linha, o campo ou o registro não existe)"
            return r
        valor, r["de_ausente"] = o.get("ausente"), True
    if o.get("formato") and valor is not None:
        instante = _converter_hora(valor, o["formato"])
        if instante is None:
            r["ilegivel"] = f"o valor não é uma hora no formato {o['formato']}"
            return r
        r["instante"], valor = instante, instante.astimezone().isoformat()
    r["valor"] = valor
    return r


# ----------------------------------------------------------------------------------------------
# Recibos e pedidos (o .md da caixa; §4.5)
# ----------------------------------------------------------------------------------------------


def _json_tipado(campos: dict, chave: str, erros: list[str]):
    """Uma chave de desfecho em JSON numa linha, ``{"tipo", "valor"}``; ``None`` (com erro) se fora da forma."""
    bruto = campos.get(chave) or ""
    if not bruto:
        return None
    try:
        valor = json.loads(bruto)
    except ValueError:
        erros.append(f"{chave} não é JSON numa linha")
        return None
    if not isinstance(valor, dict) or set(valor) != {"tipo", "valor"} or not isinstance(valor["tipo"], str):
        erros.append(f'{chave} precisa ser {{"tipo": ..., "valor": ...}}')
        return None
    return valor


def validar_recibo(dados: dict, campos: dict | None) -> dict:
    """Confere o estado e as chaves de desfecho que o maestro gravou no ``.md`` (§4.5, "recibo validado").

    ``dados`` é o ``.json`` da mensagem (o pedido e o retrato); ``campos``, o frontmatter do ``.md`` (``None`` se
    ilegível). Devolve o recibo da API: ``{valido, erros, estado_valido, aplicando_desde, aplicado_em, efeito,
    valeu_em, execucao, antes, depois, revisao, agora_esta, motivo}``. Recibo inválido nunca confirma aplicação.
    """
    erros: list[str] = []
    corpo = dados.get("corpo") or {}
    op = corpo.get("operacao")
    retrato = dados.get("laco") or {}
    controle = retrato.get("controle") or {}
    recibo = {"valido": True, "erros": erros, "estado_valido": True}
    if campos is None:
        erros.append("a vista .md não pôde ser lida (frontmatter malformado ou arquivo ilegível)")
        campos = {}
    for chave in ("aplicando_desde", "aplicado_em", "efeito", "valeu_em", "recibo_execucao", "recibo_revisao",
                  "motivo"):
        recibo[chave.replace("recibo_", "")] = campos.get(chave) or None
    recibo["antes"] = recibo["depois"] = recibo["agora_esta"] = None
    estado = campos.get("estado") or None
    if estado not in ESTADOS:
        recibo["estado_valido"] = False
        erros.append(f"estado desconhecido: {estado!r}")
    motivo = recibo["motivo"]
    if motivo is not None and len(motivo) > MOTIVO_MAXIMO:
        erros.append(f"motivo passa de {MOTIVO_MAXIMO} caracteres")
    if op in COMENTARIOS and estado in ESTADOS and estado not in ("nova", "lida"):
        erros.append("comentário só passa por nova e lida")
    enviada = _instante_de_texto(dados.get("enviada"))

    def hora(chave: str, obrigatoria: bool) -> _dt.datetime | None:
        bruto = campos.get(chave) or ""
        if not bruto:
            if obrigatoria:
                erros.append(f"falta {chave}")
            return None
        instante = _hora_com_fuso(bruto)
        if instante is None:
            erros.append(f"{chave} precisa ser hora ISO 8601 com fuso")
        return instante

    if estado == "aplicando":
        desde = hora("aplicando_desde", True)
        if desde and enviada and desde < enviada:
            erros.append("aplicando_desde é anterior ao envio")
    elif estado == "aplicado":
        desde = hora("aplicando_desde", False)
        aplicado = hora("aplicado_em", True)
        valeu = hora("valeu_em", False)
        if desde and enviada and desde < enviada:
            erros.append("aplicando_desde é anterior ao envio")
        if aplicado and enviada and aplicado < enviada:
            erros.append("aplicado_em é anterior ao envio")
        if aplicado and desde and aplicado < desde:
            erros.append("aplicado_em é anterior a aplicando_desde")
        efeito = campos.get("efeito") or ""
        if not efeito:
            erros.append("falta efeito")
        elif efeito not in EFEITOS:
            erros.append(f"efeito desconhecido: {efeito!r} (valeu, aguarda ou nao-confirmado)")
        elif efeito == "valeu":
            if not campos.get("valeu_em"):
                erros.append("efeito valeu exige valeu_em")
            elif valeu and aplicado and valeu < aplicado:
                erros.append("valeu_em é anterior a aplicado_em")
        elif campos.get("valeu_em"):
            erros.append(f"efeito {efeito} exige valeu_em vazio")
        execucao = campos.get("recibo_execucao") or ""
        if not execucao:
            erros.append("falta recibo_execucao")
        elif execucao != corpo.get("execucao"):
            erros.append(f"recibo_execucao ({execucao}) é diferente da execução do pedido ({corpo.get('execucao')})")
        revisao = campos.get("recibo_revisao") or ""
        if not revisao:
            erros.append("falta recibo_revisao")
        elif not _RE_HEX64.fullmatch(revisao):
            erros.append("recibo_revisao precisa ter 64 caracteres hexadecimais")
        for chave in ("recibo_antes", "recibo_depois"):
            if not campos.get(chave):
                erros.append(f"falta {chave}")
                continue
            tipado = _json_tipado(campos, chave, erros)
            if tipado is None:
                continue
            recibo[chave.replace("recibo_", "")] = tipado
            if op == "mudar-controle":
                pedido = corpo.get(chave.replace("recibo_", "")) or {}
                if tipado["tipo"] != controle.get("tipo"):
                    erros.append(f"{chave} com tipo {tipado['tipo']!r}; o controle é {controle.get('tipo')!r}")
                    continue
                motivo_valor = (valor_valido(controle, tipado["valor"]) if chave == "recibo_depois"
                                else (None if tipado["valor"] is None
                                      else tipo_do_valor(controle.get("tipo"), tipado["valor"])))
                if motivo_valor:
                    erros.append(f"{chave} inválido para o controle: {motivo_valor}")
                elif not iguais(controle.get("tipo"), tipado["valor"], pedido.get("valor")):
                    erros.append(f"{chave} diferente do pedido (isso não é aplicado: é recusado ou conflito)")
            elif tipado["tipo"] != "texto" or not isinstance(tipado["valor"], str) or not tipado["valor"].strip():
                erros.append(f'{chave} de {op} precisa ser {{"tipo": "texto", "valor": "<em palavras>"}}')
    elif estado in ("recusado", "encerrado-sem-aplicar"):
        if not motivo:
            erros.append(f"{estado} exige motivo")
    elif estado == "conflito":
        if not campos.get("agora_esta"):
            erros.append("conflito exige agora_esta")
        else:
            tipado = _json_tipado(campos, "agora_esta", erros)
            if tipado is not None:
                recibo["agora_esta"] = tipado
                if tipado["tipo"] == "texto":
                    if not isinstance(tipado["valor"], str):
                        erros.append("agora_esta de texto precisa de valor em palavras")
                elif op != "mudar-controle" or tipado["tipo"] != controle.get("tipo"):
                    erros.append("agora_esta precisa estar no tipo do controle, ou ser texto")
                elif tipado["valor"] is not None and tipo_do_valor(controle.get("tipo"), tipado["valor"]):
                    erros.append(f"agora_esta: {tipo_do_valor(controle.get('tipo'), tipado['valor'])}")
    recibo["valido"] = not erros
    return recibo


def trabalho_pendente(op, estado, efeito) -> bool:
    """Ainda há trabalho do maestro (§4.5, "pendente de trabalho ≠ pendente de aviso")?

    ``nova``, ``lida``, ``aplicando`` ou ``aplicado`` com ``efeito: aguarda``; comentários encerram na leitura (só
    ``nova`` pende). Estado desconhecido também pende: não dá para saber se o maestro terminou.
    """
    if estado not in ESTADOS:
        return True
    if op in COMENTARIOS:
        return estado == "nova"
    return estado in ("nova", "lida", "aplicando") or (estado == "aplicado" and efeito == "aguarda")


class Contexto:
    """O que um pedido de leitura dos laços lê uma vez só: registro, caixa, rodadas respondidas e fila de avisos."""

    def __init__(self, projeto: leitores.Projeto, avisos: dict | None = None) -> None:
        self.projeto = projeto
        self.entradas, self.problemas_do_registro = leitores.ler_registro_de_lacos(projeto)
        self.campos_md: dict[str, dict | None] = {}
        self.jsons: dict[str, dict] = {}
        if projeto.caixa:
            try:
                self.jsons, _, _ = leitores.listar_caixa(projeto.caixa, self.campos_md)
            except OSError:
                self.jsons = {}
        if avisos is None:
            try:
                avisos = leitores.ler_avisos_json(projeto.caixa) or {} if projeto.caixa else {}
            except (OSError, ValueError):
                avisos = {}
        self.avisos = avisos
        self._rodadas: list[dict] | None = None
        # substituto direto de cada mensagem (a primeira, no tempo, que a aponta)
        self.substituto: dict[str, str] = {}
        for nome in sorted(self.jsons):
            alvo = self.jsons[nome].get("substitui")
            if alvo and alvo not in self.substituto:
                self.substituto[alvo] = nome

    def rodadas(self) -> list[dict]:
        """As rodadas com ``respondida`` na versão atual (§3.7), para o grupo "espera você"."""
        if self._rodadas is None:
            p = leitores.Problemas()
            rodadas = leitores.ler_rodadas(self.projeto, [], [], p)
            bases: dict = {}
            caixa = leitores.ler_caixa(self.projeto, [], [], rodadas, p, bases)
            leitores.ligar_respostas(rodadas, caixa, bases)
            self._rodadas = rodadas
        return self._rodadas

    def caminho_md(self, nome: str) -> str:
        return os.path.join(self.projeto.caixa, nome + ".md")

    def pedidos(self, lid: str, execucao_atual: str | None) -> tuple[list[dict], list[tuple[str, str]]]:
        """Os pedidos ``alteracao-laco`` deste laço, do mais novo ao mais velho, com estado e recibo validado."""
        pedidos: list[dict] = []
        problemas: list[tuple[str, str]] = []
        nomes = [n for n, d in self.jsons.items() if d["tipo"] == "alteracao-laco" and d["alvo"]["id"] == lid]
        for nome in sorted(nomes, reverse=True):
            dados = self.jsons[nome]
            corpo = dados["corpo"]
            if nome in self.campos_md:
                campos = self.campos_md[nome]
            elif not os.path.exists(self.caminho_md(nome)):
                campos = {"estado": "nova"}  # .json sem .md: o reparo regera a vista com estado: nova
            else:
                campos = None
            recibo = validar_recibo(dados, campos)
            estado = (campos or {}).get("estado") or None
            relativo = self.projeto.relativo(self.caminho_md(nome))
            if not recibo["estado_valido"]:
                problemas.append((relativo, f"estado desconhecido: {estado!r}; não confirma a entrega do aviso"))
            if recibo["erros"] and recibo["estado_valido"]:
                problemas.append((relativo, "recibo inválido: " + "; ".join(recibo["erros"])))
            registro = self.avisos.get(dados["envio"])
            pedidos.append({
                "envio": dados["envio"], "arquivo": nome, "operacao": corpo.get("operacao"),
                "no": corpo.get("no") or ((dados.get("laco") or {}).get("no") or {}).get("id"),
                "controle": corpo.get("controle"), "capacidade": corpo.get("capacidade"), "onda": corpo.get("onda"),
                "antes": corpo.get("antes"), "depois": corpo.get("depois"), "texto": corpo.get("texto"),
                "revisao": corpo.get("revisao"), "execucao": corpo.get("execucao"),
                "atual": corpo.get("execucao") == execucao_atual, "enviada": dados["enviada"],
                "substitui": dados.get("substitui"), "substituido_por": self.substituto.get(nome),
                "estado": estado, "recibo": recibo,
                "trabalho_pendente": trabalho_pendente(corpo.get("operacao"), estado, (campos or {}).get("efeito")),
                "aviso": registro.get("estado") if isinstance(registro, dict) else None,
            })
        return pedidos, problemas


# ----------------------------------------------------------------------------------------------
# O laço inteiro: leitura, revisão, situação, grupo
# ----------------------------------------------------------------------------------------------


def calcular_revisao(laco: dict, configurados: dict, precondicoes: dict) -> str:
    """``sha256`` do retrato R da §4.4: definições relevantes, configurados, precondições e capacidades."""
    controles = {}
    for c in laco["controles"]:
        bruta = c["bruta"]
        config = configurados[c["id"]]
        controles[c["id"]] = {
            "definicao": {k: bruta[k] for k in CHAVES_DA_DEFINICAO if k in bruta},
            "configurado": {"ilegivel": True} if config["ilegivel"] else config["valor"],
            "precondicoes": {nome: ({"ilegivel": True} if p["ilegivel"] else p["valor"])
                             for nome, p in precondicoes[c["id"]].items()},
        }
    r = {"laco": laco["id"], "execucao": laco["execucao"]["id"],
         "capacidades": [cap["bruta"] for cap in laco["capacidades"]], "controles": controles}
    return hashlib.sha256(json.dumps(r, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()


def _configurado(pasta: str, c: dict, anotar) -> dict:
    r = ler_origem(pasta, c["configurado"], anotar)
    saida = {"valor": None, "como": "declarado" if c["configurado"]["forma"] == "declarado" else "lido",
             "fonte": r["fonte"], "hora": _iso(r["hora"]), "ilegivel": r["ilegivel"]}
    if r["ilegivel"]:
        return saida
    valor = r["valor"]
    if valor is None:
        if not (c["aceita_nulo"] or r["de_ausente"]):
            saida["ilegivel"] = "valor nulo, e o controle não aceita nulo"
            return saida
    elif tipo_do_valor(c["tipo"], valor):
        saida["ilegivel"] = f"valor do tipo errado: {tipo_do_valor(c['tipo'], valor)}"
        return saida
    saida["valor"] = valor
    return saida


def _contador(pasta: str, c: dict, anotar) -> dict:
    r = ler_origem(pasta, c["origem"], anotar)
    saida = {"id": c["id"], "no": c["no"], "rotulo": c["rotulo"], "tipo": c["tipo"], "escala": c["escala"],
             "campos": c["campos"], "valor": None, "fonte": r["fonte"], "hora": None, "ilegivel": r["ilegivel"]}
    if not r["ilegivel"]:
        v, tipo, motivo = r["valor"], c["tipo"], None
        if v is None:
            motivo = None if r["de_ausente"] else "valor nulo"
        elif tipo == "inteiro" and not _e_inteiro(v):
            motivo = "precisa ser um inteiro"
        elif tipo == "numero" and not _e_numero(v):
            motivo = "precisa ser um número"
        elif tipo == "texto" and not isinstance(v, str):
            motivo = "precisa ser texto"
        elif tipo == "hora":
            instante = r["instante"] or _instante_de_texto(v)
            if instante is None:
                motivo = "precisa ser uma hora (formato iso ou epoch)"
            else:
                v = _iso(instante)
        elif tipo == "lista" and not (isinstance(v, list) and all(isinstance(x, str) for x in v)):
            motivo = "precisa ser uma lista de textos"
        elif tipo == "contagem" and not (isinstance(v, dict) and all(_e_numero(x) for x in v.values())):
            motivo = "precisa ser um objeto chave → número"
        elif tipo == "serie" and not (isinstance(v, list) and all(isinstance(x, dict) for x in v)):
            motivo = "precisa ser uma lista de objetos"
        if motivo:
            saida["ilegivel"] = f"valor do tipo errado: {motivo}" if v is not None else motivo
        else:
            saida["valor"] = v
    hora = r["hora"]
    if c["hora"] is not None:
        rh = ler_origem(pasta, c["hora"], anotar)
        hora = None if rh["ilegivel"] else (rh["instante"] or _instante_de_texto(rh["valor"]) or rh["hora"])
    saida["hora"] = _iso(hora)
    return saida


def _numero_de(pasta: str, o: dict | None, anotar) -> tuple[float | None, str | None]:
    if o is None:
        return None, None
    r = ler_origem(pasta, o, anotar)
    if r["ilegivel"]:
        return None, r["ilegivel"]
    if not _e_numero(r["valor"]):
        return None, "o valor não é um número"
    return r["valor"], None


def _mesmo_ticket(a, b) -> bool:
    if isinstance(a, str) and isinstance(b, str) and a.isdigit() and b.isdigit():
        return int(a) == int(b)
    return a == b


def ler_laco(entrada: dict, contexto: Contexto, brutos: dict | None = None) -> dict:
    """O laço inteiro (``GET /api/laco/<id>``); levanta ``LacoMalformado`` se o ``laco.json`` está fora do contrato.

    ``brutos``, quando dado, recebe ``id do controle → controle como declarado no laco.json`` (o retrato do pedido
    guarda essa definição para o maestro conferir campo a campo).
    """
    laco, avisos = carregar_laco(entrada)
    if brutos is not None:
        brutos.update({c["id"]: c["bruta"] for c in laco["controles"]})
    pasta = entrada["pasta_real"]
    projeto = contexto.projeto
    nome_laco_json = projeto.relativo(os.path.join(pasta, "laco.json"))
    problemas: list[tuple[str, str]] = [(nome_laco_json, a) for a in avisos]

    def anotar(mensagem: str) -> None:
        par = (nome_laco_json, mensagem)
        if par not in problemas:
            problemas.append(par)

    agora = _dt.datetime.now().astimezone()
    execucao = laco["execucao"]
    terminado = bool(execucao["terminou_em"])

    # sinal: a hora mais nova entre as fontes legíveis (nunca "vivo")
    fontes_sinal = []
    ultimo = None
    for o in laco["sinal"]["fontes"]:
        r = ler_origem(pasta, o, anotar)
        instante = None
        if not r["ilegivel"]:
            instante = r["instante"] if o.get("formato") else r["hora"]
            if instante is None:
                r["ilegivel"] = "sem hora (valor nulo)"
        fontes_sinal.append({"fonte": r["fonte"], "hora": _iso(instante), "ilegivel": r["ilegivel"]})
        if instante is not None and (ultimo is None or instante > ultimo[0]):
            ultimo = (instante, r["fonte"])

    parado = None
    if laco["parado"] is not None:
        r = ler_origem(pasta, laco["parado"], anotar)
        motivo = r["ilegivel"]
        if not motivo and not isinstance(r["valor"], bool):
            motivo = "o valor não é verdadeiro/falso"
        parado = {"valor": None if motivo else r["valor"], "fonte": r["fonte"], "ilegivel": motivo}

    cota = None
    if laco["esperando_cota"] is not None:
        aptos, e1 = _numero_de(pasta, laco["esperando_cota"]["aptos"], anotar)
        fora, e2 = _numero_de(pasta, laco["esperando_cota"]["fora"], anotar)
        cota = {"aptos": aptos, "fora": fora,
                "ilegivel": None if not (e1 or e2) else "; ".join(f"{n}: {m}" for n, m in (("aptos", e1),
                                                                                            ("fora", e2)) if m)}

    # situação, a primeira regra que vale (§4.4)
    if terminado:
        situacao = "terminado"
    elif parado and parado["valor"] is True:
        situacao = "parado"
    elif ultimo is None:
        situacao = "desconhecido"
    elif (agora - ultimo[0]).total_seconds() > laco["sinal"]["sem_sinal_apos_s"]:
        situacao = "sem-sinal"
    elif cota and not cota["ilegivel"] and (cota["aptos"] == 0 or cota["fora"] >= cota["aptos"]):
        situacao = "esperando-cota"
    else:
        situacao = "rodando"

    contadores = [_contador(pasta, c, anotar) for c in laco["contadores"]]
    por_contador = {c["id"]: c for c in contadores}
    capacidades = []
    for cap in laco["capacidades"]:
        saida = {"id": cap["id"]}
        if cap["id"] == "parar-apos-onda":
            saida["onda_atual"] = None
            saida["onda_ilegivel"] = None
            if cap["onda_atual"]:
                contador = por_contador[cap["onda_atual"]]
                if contador["ilegivel"] or not _e_inteiro(contador["valor"]):
                    saida["onda_ilegivel"] = contador["ilegivel"] or "a onda não é um inteiro"
                else:
                    saida["onda_atual"] = contador["valor"]
        capacidades.append(saida)

    configurados = {c["id"]: _configurado(pasta, c, anotar) for c in laco["controles"]}
    precondicoes = {}
    for c in laco["controles"]:
        precondicoes[c["id"]] = {}
        for nome, o in c["precondicoes"].items():
            r = ler_origem(pasta, o, anotar)
            precondicoes[c["id"]][nome] = {"valor": None if r["ilegivel"] else r["valor"], "fonte": r["fonte"],
                                           "hora": _iso(r["hora"]), "ilegivel": r["ilegivel"]}
    revisao = calcular_revisao(laco, configurados, precondicoes)

    pedidos, problemas_pedidos = contexto.pedidos(laco["id"], execucao["id"])
    problemas += problemas_pedidos

    controles = []
    for c in laco["controles"]:
        config = configurados[c["id"]]
        em_uso = {"estado": "nao-confirmado", "valor": None, "como": None, "fonte": None, "hora": None,
                  "ilegivel": None, "diverge": False}
        if c["em_uso"] is not None:
            r = ler_origem(pasta, c["em_uso"], anotar)
            motivo = r["ilegivel"]
            if not motivo and r["valor"] is not None and tipo_do_valor(c["tipo"], r["valor"]):
                motivo = f"valor do tipo errado: {tipo_do_valor(c['tipo'], r['valor'])}"
            if not motivo and r["valor"] is None and not (c["aceita_nulo"] or r["de_ausente"]):
                motivo = "valor nulo"
            if motivo:
                em_uso["ilegivel"] = motivo
            else:
                em_uso.update(estado="confirmado", valor=r["valor"], como=f"lido de {r['fonte']}", fonte=r["fonte"],
                              hora=_iso(r["hora"]),
                              diverge=(not config["ilegivel"]) and not iguais(c["tipo"], r["valor"], config["valor"]))
        if em_uso["estado"] != "confirmado" and not config["ilegivel"]:
            ultimo_aplicado = next((p for p in pedidos if p["operacao"] == "mudar-controle"
                                    and p["controle"] == c["id"] and p["atual"] and p["estado"] == "aplicado"), None)
            recibo = (ultimo_aplicado or {}).get("recibo") or {}
            if ultimo_aplicado and recibo.get("valido") and recibo.get("efeito") == "valeu" \
                    and recibo.get("revisao") == revisao and recibo.get("depois") is not None \
                    and iguais(c["tipo"], recibo["depois"].get("valor"), config["valor"]):
                em_uso.update(estado="confirmado", valor=config["valor"],
                              como=f"recibo do maestro, {recibo.get('valeu_em')}", fonte="recibo do maestro",
                              hora=recibo.get("valeu_em"))
        if em_uso["estado"] != "confirmado" and c["releitura"] == "continua" and c["em_uso"] is None \
                and situacao in ("rodando", "esperando-cota"):
            em_uso.update(estado="relido", como="relido pelo laço a cada ciclo")
        controles.append({
            "id": c["id"], "no": c["no"], "rotulo": c["rotulo"], "tipo": c["tipo"], "faixa": c["faixa"],
            "opcoes": c["opcoes"], "itens": c["itens"], "unidade": c["unidade"], "escala": c["escala"],
            "aceita_nulo": c["aceita_nulo"], "nulo": c["nulo"], "quando_vale": c["quando_vale"],
            "releitura": c["releitura"], "configurado": config, "em_uso": em_uso,
            "precondicoes": precondicoes[c["id"]],
        })

    # grupo (§3.4): terminado; espera você (rodada aberta não respondida, ou conflito atual e acionável); em voo
    if terminado:
        grupo = "terminado"
    else:
        rodada_esperando = any(r.get("estado") == "aberta" and not r.get("malformada") and not r.get("respondida")
                               and _mesmo_ticket(r.get("ticket"), laco["ticket"]) for r in contexto.rodadas())
        conflito = any(p["estado"] == "conflito" and p["atual"] and not p["substituido_por"] for p in pedidos)
        grupo = "espera-voce" if rodada_esperando or conflito else "em-voo"

    problemas.sort()
    return {
        "id": laco["id"], "titulo": laco["titulo"], "ticket": laco["ticket"],
        "pasta": projeto.relativo(pasta), "execucao": dict(execucao), "grupo": grupo, "situacao": situacao,
        "lido_em": _iso(agora),
        "ultimo_sinal": {"hora": _iso(ultimo[0]), "fonte": ultimo[1]} if ultimo else None,
        "sinal": {"fontes": fontes_sinal, "sem_sinal_apos_s": laco["sinal"]["sem_sinal_apos_s"]},
        "parado": parado, "cota": cota, "revisao": revisao,
        "nos": laco["nos"], "ligacoes": laco["ligacoes"], "controles": controles, "capacidades": capacidades,
        "contadores": contadores, "pedidos": pedidos,
        "pedidos_abertos": sum(1 for p in pedidos if p["atual"] and p["trabalho_pendente"]),
        "problema": None,
        "problemas": [{"arquivo": a, "mensagem": m} for a, m in problemas],
    }


# ----------------------------------------------------------------------------------------------
# Pontos de entrada da torre
# ----------------------------------------------------------------------------------------------


def _linha_malformada(entrada: dict, erro: str) -> dict:
    return {"id": entrada["id"], "titulo": entrada["id"], "ticket": None, "execucao": None, "grupo": "em-voo",
            "situacao": "desconhecido", "terminou_em": None, "ultimo_sinal": None, "destaque": None,
            "pedidos_abertos": None, "problema": erro}


def resumo_dos_lacos(projeto: leitores.Projeto, avisos: dict | None = None) -> list[dict]:
    """``GET /api/lacos``: uma linha por laço do registro, na ordem dele; malformado vem com ``problema``."""
    contexto = Contexto(projeto, avisos)
    saida = []
    for entrada in contexto.entradas:
        try:
            laco = ler_laco(entrada, contexto)
        except LacoMalformado as e:
            saida.append(_linha_malformada(entrada, str(e)))
            continue
        primeiro = laco["contadores"][0] if laco["contadores"] else None
        saida.append({
            "id": laco["id"], "titulo": laco["titulo"], "ticket": laco["ticket"], "execucao": laco["execucao"]["id"],
            "grupo": laco["grupo"], "situacao": laco["situacao"], "terminou_em": laco["execucao"]["terminou_em"],
            "ultimo_sinal": laco["ultimo_sinal"],
            "destaque": {"rotulo": primeiro["rotulo"], "valor": primeiro["valor"], "ilegivel": primeiro["ilegivel"]}
            if primeiro else None,
            "pedidos_abertos": laco["pedidos_abertos"], "problema": None,
        })
    return saida


def detalhe_do_laco(projeto: leitores.Projeto, lid: str, avisos: dict | None = None) -> dict:
    """``GET /api/laco/<id>``: levanta ``Recusa`` 404 ``laco-inexistente`` ou 422 ``laco-malformado``."""
    contexto = Contexto(projeto, avisos)
    entrada = next((e for e in contexto.entradas if e["id"] == lid), None)
    if entrada is None:
        raise Recusa(404, "laco-inexistente", f"não há laço {lid} no registro")
    try:
        return ler_laco(entrada, contexto)
    except LacoMalformado as e:
        raise Recusa(422, "laco-malformado", f"o laço {lid} está malformado: {e}") from None


def arquivos_declarados(entrada: dict) -> set[str] | None:
    """O ``laco.json`` e todo arquivo que o laço declara como origem (bancos com ``-wal``, ``-shm`` e ``-journal``),
    como caminhos da pasta do laço, o léxico e o real. ``None`` quando o laço está malformado: aí não se sabe o que é
    fonte."""
    try:
        laco, _ = carregar_laco(entrada)
    except LacoMalformado:
        return None
    pasta = entrada["pasta_real"]
    origens: list = [laco["parado"], *laco["sinal"]["fontes"]]
    for c in laco["controles"]:
        origens += [c["configurado"], c["em_uso"], *c["precondicoes"].values()]
    for c in laco["contadores"]:
        origens += [c["origem"], c["hora"]]
    if laco["esperando_cota"]:
        origens += [laco["esperando_cota"]["aptos"], laco["esperando_cota"]["fora"]]
    lexicos = [os.path.join(pasta, "laco.json")]
    for o in origens:
        if o is None or o["forma"] == "declarado":
            continue
        caminho = os.path.normpath(os.path.join(pasta, *re.split(r"[\\/]", o["caminho"])))
        lexicos.append(caminho)
        if o["forma"] == "sqlite":
            lexicos += [caminho + "-wal", caminho + "-shm", caminho + "-journal"]
    return {c for lex in lexicos for c in (lex, os.path.realpath(lex))}


def carta_pode_servir(projeto: leitores.Projeto, pasta_carta: str, alvo: str) -> bool:
    """Regra das cartas diante dos laços (§4.4: as fontes de um laço não são servidas como arquivo).

    ``pasta_carta`` e ``alvo`` já são reais e ``alvo`` já está dentro de ``pasta_carta``. Para cada laço registrado
    que contém ``alvo``: carta cuja pasta é a raiz do laço ou a contém (ex.: a carta mestra numa pasta acima) não serve
    nada de dentro dele; carta cuja pasta fica **dentro** do laço só serve se for uma subpasta só de publicação (um
    painel): o laço está bem formado e nem o ``laco.json`` nem nenhuma origem declarada fica dentro dela. Atalhos já
    foram resolvidos (``realpath``): um atalho do painel para uma fonte cai fora da pasta da carta e não é servido.
    """
    entradas, _ = leitores.ler_registro_de_lacos(projeto)
    for entrada in entradas:
        pasta_laco = entrada["pasta_real"]
        if not pasta_laco or not leitores.dentro_de(alvo, pasta_laco):
            continue
        if leitores.dentro_de(pasta_laco, pasta_carta):  # a pasta da carta é a raiz do laço ou a contém
            return False
        declarados = arquivos_declarados(entrada)
        if declarados is None or any(leitores.dentro_de(c, pasta_carta) for c in declarados):
            return False
    return True


def problemas_dos_lacos(projeto: leitores.Projeto) -> list[tuple[str, str]]:
    """O que vai para ``problemas`` do estado: registro, ``laco.json`` malformado ou com chave desconhecida, e os
    pedidos com estado desconhecido ou recibo inválido. Não lê nenhuma fonte de estado dos laços."""
    contexto = Contexto(projeto)
    problemas = list(contexto.problemas_do_registro)
    nome_registro = projeto.relativo(projeto.lacos_json) if projeto.lacos_json else "lacos.json"
    for entrada in contexto.entradas:
        if entrada["erro"]:
            problemas.append((nome_registro, f"laço {entrada['id']} malformado: {entrada['erro']}"))
            continue
        nome = projeto.relativo(os.path.join(entrada["pasta_real"], "laco.json"))
        try:
            _, avisos = carregar_laco(entrada)
        except LacoMalformado as e:
            problemas.append((nome, f"laço malformado: {e}"))
            continue
        problemas += [(nome, a) for a in avisos]
    for lid in sorted({d["alvo"]["id"] for d in contexto.jsons.values() if d["tipo"] == "alteracao-laco"}):
        _, extras = contexto.pedidos(lid, None)
        problemas += extras
    return problemas


# ----------------------------------------------------------------------------------------------
# POST /api/caixa, tipo alteracao-laco (§4.5)
# ----------------------------------------------------------------------------------------------

_CHAVES_BASE = {"envio", "tipo", "laco", "execucao", "operacao", "revisao", "substitui"}
_CHAVES_OPERACAO = {
    "mudar-controle": {"no", "controle", "antes", "depois", "texto"},
    "pedir-parada": {"capacidade", "onda", "texto"},
    "pedir-pausa": {"texto"},
    "pedir-retomada": {"texto"},
    "comentario-no": {"no", "texto"},
    "comentario-laco": {"texto"},
}


def _texto(corpo: dict, obrigatorio: bool) -> None:
    valor = corpo.get("texto")
    if valor is None or valor == "":
        if obrigatorio:
            raise Recusa(400, "texto-obrigatorio", "o comentário precisa de texto", "texto")
        return
    if not isinstance(valor, str):
        raise Recusa(400, "tipo-errado", "o campo texto precisa ser texto", "texto")
    if len(valor) > TEXTO_MAXIMO:
        raise Recusa(400, "texto-longo", f"o campo texto passa de {TEXTO_MAXIMO} caracteres", "texto")
    if obrigatorio and not valor.strip():
        raise Recusa(400, "texto-obrigatorio", "o comentário precisa de texto", "texto")


def _grupo_de_substituicao(corpo: dict):
    op = corpo.get("operacao")
    if op == "mudar-controle":
        return ("controle", corpo.get("controle"))
    if op in PARADAS:
        return ("parada",)
    return None


def _validar_substitui(corpo: dict, lid: str, execucao: str, caixa, contexto: Contexto) -> str | None:
    valor = corpo.get("substitui")
    if valor is None:
        return None
    if not isinstance(valor, str) or valor not in caixa.nomes():
        raise Recusa(400, "substitui-invalido", "substitui precisa ser o nome de uma mensagem da caixa", "substitui")
    try:
        anterior = caixa.dados_de(valor)
    except (OSError, ValueError):
        raise Recusa(400, "substitui-invalido", "a mensagem substituída não pôde ser lida", "substitui") from None
    if anterior["tipo"] != "alteracao-laco":
        raise Recusa(400, "substitui-invalido", "substitui aponta para mensagem que não é alteração de laço",
                     "substitui")
    if anterior["alvo"]["id"] != lid:
        raise Recusa(400, "substitui-invalido", "substitui aponta para pedido de outro laço", "substitui")
    if anterior["corpo"].get("execucao") != execucao:
        raise Recusa(400, "substitui-invalido", "substitui aponta para pedido de outra execução", "substitui")
    grupo_novo, grupo_velho = _grupo_de_substituicao(corpo), _grupo_de_substituicao(anterior["corpo"])
    if grupo_novo is None or grupo_velho is None:
        raise Recusa(400, "substitui-invalido", "comentários não substituem nem são substituídos", "substitui")
    if grupo_novo != grupo_velho:
        raise Recusa(400, "substitui-invalido", "substitui aponta para pedido incompatível (outro controle ou outra "
                     "operação)", "substitui")
    estado = caixa.estado_md(valor)
    if estado is None and not os.path.exists(contexto.caminho_md(valor)):
        estado = "nova"
    if estado not in ("nova", "lida", "conflito"):
        raise Recusa(400, "substitui-invalido", f"o pedido substituído está em {estado!r}; só nova, lida ou "
                     "conflito podem ser substituídos", "substitui")
    if valor in contexto.substituto:
        raise Recusa(400, "substitui-invalido", f"o pedido já foi substituído por {contexto.substituto[valor]}",
                     "substitui")
    return valor


def validar_alteracao(corpo: dict, projeto: leitores.Projeto, caixa, avisos: dict | None = None) -> dict:
    """Valida um ``alteracao-laco`` novo (a idempotência já passou) e devolve o ``.json`` pronto para a caixa.

    Levanta ``Recusa`` com os códigos da §4.5 (400 com ``campo``; 409 ``laco-mudou``, ``execucao-mudou``,
    ``laco-terminou``, ``configurado-ilegivel``). O navegador só manda ids e valores tipados: tudo o mais vem do
    ``laco.json`` atual.
    """
    op = corpo.get("operacao")
    if op not in OPERACOES:
        raise Recusa(400, "operacao-invalida", "operacao precisa ser uma de: " + ", ".join(OPERACOES), "operacao")
    for chave in corpo:
        if chave not in _CHAVES_BASE | _CHAVES_OPERACAO[op]:
            raise Recusa(400, "chave-desconhecida", f"chave que não pertence a {op}: {chave}", chave)
    lid = corpo.get("laco")
    if not isinstance(lid, str) or not lid:
        raise Recusa(400, "laco-invalido", "laco precisa ser o id de um laço", "laco")
    contexto = Contexto(projeto, avisos)
    entrada = next((e for e in contexto.entradas if e["id"] == lid), None)
    if entrada is None:
        raise Recusa(409, "laco-mudou", f"o laço {lid} não está (mais) no registro", "laco")
    brutos: dict = {}
    try:
        laco = ler_laco(entrada, contexto, brutos)
    except LacoMalformado as e:
        raise Recusa(400, "laco-malformado", f"o laço está malformado: {e}", "laco") from None
    execucao = corpo.get("execucao")
    if not isinstance(execucao, str) or not execucao:
        raise Recusa(400, "execucao-invalida", "execucao precisa ser o id da execução", "execucao")
    if execucao != laco["execucao"]["id"]:
        raise Recusa(409, "execucao-mudou", f"a execução agora é {laco['execucao']['id']}; um pedido nunca passa "
                     "sozinho para a execução seguinte", "execucao", {"execucao_atual": laco["execucao"]["id"]})
    if laco["execucao"]["terminou_em"] and op not in COMENTARIOS:
        raise Recusa(409, "laco-terminou", "a execução terminou; só comentário é aceito", "execucao")
    revisao = corpo.get("revisao")
    if not isinstance(revisao, str) or not _RE_HEX64.fullmatch(revisao):
        raise Recusa(400, "revisao-invalida", "revisao precisa ser o sha256 que veio em GET /api/laco/<id>",
                     "revisao")
    _texto(corpo, obrigatorio=op in COMENTARIOS)
    nos = {n["id"]: n for n in laco["nos"]}
    declaradas = {c["id"]: c for c in laco["capacidades"]}
    no_retrato = None
    controle = None

    for chave in ("no", "controle"):  # ids: o tipo antes de procurar (lista ou objeto nunca chegam a um dict)
        if chave in corpo and not isinstance(corpo[chave], str):
            raise Recusa(400, "tipo-errado", f"{chave} precisa ser um id (texto)", chave)

    if op == "mudar-controle":
        controle = next((c for c in laco["controles"] if c["id"] == corpo.get("controle")), None)
        if controle is None:
            raise Recusa(400, "controle-inexistente", f"não há controle {corpo.get('controle')!r} neste laço",
                         "controle")
        if corpo.get("no") != controle["no"]:
            raise Recusa(400, "no-invalido", f"o controle {controle['id']} pertence ao nó {controle['no']}", "no")
        for chave in ("antes", "depois"):
            v = corpo.get(chave)
            if not isinstance(v, dict) or set(v) != {"tipo", "valor"} or not isinstance(v.get("tipo"), str):
                raise Recusa(400, "valor-invalido", f'{chave} precisa ser {{"tipo": ..., "valor": ...}}', chave)
        antes, depois = corpo["antes"], corpo["depois"]
        config = controle["configurado"]
        if config["ilegivel"]:
            raise Recusa(409, "configurado-ilegivel", f"o valor configurado não pôde ser lido: {config['ilegivel']}",
                         "controle")
        tipo = controle["tipo"]
        agora_tipado = {"tipo": tipo, "valor": config["valor"]}
        if revisao != laco["revisao"]:
            # só o hash não diz o que mudou: true só quando provado (o tipo mudou, ou o valor pedido não cabe mais na
            # definição atual); fora disso null = "a configuração ou a regra mudou; o portal não sabe qual". Nunca
            # false por inferência: mudar só o máximo da faixa, a unidade, a origem ou a releitura não deixa rastro aqui
            provado = antes["tipo"] != tipo or depois["tipo"] != tipo \
                or valor_valido(controle, depois["valor"]) is not None
            definicao_mudou = True if provado else None
            raise Recusa(409, "laco-mudou", "o laço mudou depois que a página o leu (revisão diferente)", "revisao",
                         {"conflito": {"viu": antes, "agora": agora_tipado, "pediu": depois,
                                       "revisao": laco["revisao"], "definicao_mudou": definicao_mudou}})
        for chave, v in (("antes", antes), ("depois", depois)):
            if v["tipo"] != tipo:
                raise Recusa(400, "tipo-errado", f"{chave}.tipo precisa ser {tipo}", f"{chave}.tipo")
        if (antes["valor"] is not None and tipo_do_valor(tipo, antes["valor"])) \
                or not iguais(tipo, antes["valor"], config["valor"]):
            # aqui a revisão é a mesma que a página viu, e a definição entra no hash: false é provado, não inferido
            raise Recusa(409, "laco-mudou", "o valor configurado não é mais o que a página viu", "antes",
                         {"conflito": {"viu": antes, "agora": agora_tipado, "pediu": depois,
                                       "revisao": laco["revisao"], "definicao_mudou": False}})
        motivo = valor_valido(controle, depois["valor"])
        if motivo:
            raise Recusa(400, "valor-invalido", f"depois.valor {motivo}", "depois.valor")
        if iguais(tipo, depois["valor"], antes["valor"]):
            raise Recusa(400, "nada-muda", "o valor pedido é igual ao configurado", "depois")
        no_retrato = nos[controle["no"]]
    elif op == "pedir-parada":
        capacidade = corpo.get("capacidade")
        if capacidade not in ("parar-apos-onda", "parar-de-despachar"):
            raise Recusa(400, "capacidade-invalida", "capacidade precisa ser parar-apos-onda ou parar-de-despachar",
                         "capacidade")
        if capacidade not in declaradas:
            raise Recusa(400, "capacidade-ausente", f"o laço não declara {capacidade}", "capacidade")
        onda = corpo.get("onda")
        if capacidade == "parar-apos-onda":
            if not _e_inteiro(onda) or onda < 1:
                raise Recusa(400, "onda-invalida", "onda precisa ser um inteiro ≥ 1", "onda")
            atual = declaradas[capacidade].get("onda_atual")
            if atual is not None and onda < atual:  # só com a onda em curso legível; nunca contra zero inventado
                raise Recusa(400, "onda-invalida", f"a onda {onda} já passou; a onda em curso é {atual}", "onda")
        elif onda is not None:
            raise Recusa(400, "onda-invalida", "onda só existe com parar-apos-onda", "onda")
    elif op in ("pedir-pausa", "pedir-retomada"):
        if "pausar-retomar" not in declaradas:
            raise Recusa(400, "capacidade-ausente", "o laço não declara pausar-retomar", "operacao")
    elif op == "comentario-no":
        if corpo.get("no") not in nos:
            raise Recusa(400, "no-inexistente", f"não há nó {corpo.get('no')!r} neste laço", "no")
        no_retrato = nos[corpo["no"]]

    substitui = _validar_substitui(corpo, lid, execucao, caixa, contexto)
    retrato = {"id": laco["id"], "titulo": laco["titulo"], "ticket": laco["ticket"],
               "execucao": dict(laco["execucao"]), "revisao": laco["revisao"],
               "no": {"id": no_retrato["id"], "titulo": no_retrato["titulo"], "papel": no_retrato["papel"]}
               if no_retrato else None,
               "capacidades": laco["capacidades"], "situacao": laco["situacao"]}
    if controle is not None:
        bruta = brutos[controle["id"]]
        retrato["controle"] = dict(controle, definicao=bruta, origem_configurado=bruta.get("configurado"))
    corpo_sem_envio = {k: v for k, v in corpo.items() if k != "envio"}
    return {
        "envio": corpo["envio"], "tipo": "alteracao-laco", "enviada": leitores.agora_iso(),
        "alvo": {"tipo": "laco", "id": lid, "titulo": laco["titulo"]}, "ticket": laco["ticket"],
        "substitui": substitui, "laco": retrato,
        "corpo_hash": leitores.hash_corpo(corpo_sem_envio), "corpo": corpo_sem_envio,
    }
