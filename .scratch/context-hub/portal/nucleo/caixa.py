"""A caixa: gravação atômica das mensagens do controlador, idempotência e recuperação (§3.5).

Uma mensagem = ``<nome>.json`` (a fonte, imutável) + ``<nome>.md`` (a vista para o agente, gerada
do ``.json`` de forma determinística; só o ``estado:`` é dele). O índice ``envio → nome`` vive só em
memória e é refeito no arranque. A fila ``.avisos.json`` guarda o que já foi avisado.

Ponto de extensão para o marco 7 (o envio do aviso): ``Fila.pendentes()`` devolve o que precisa sair;
``Fila.marcar(envio, estado, erro=None, proximo=None)`` registra ``enviando``, ``entregue``,
``pendente`` (nova tentativa, com ``proximo``) ou ``falhou``; ``Caixa.dados_de(nome)`` dá o ``.json``
da mensagem para compor o texto do aviso.
"""

from __future__ import annotations

import datetime as _dt
import json
import os
import re
import threading
import time
import uuid

try:
    from . import leitores
except ImportError:  # executado como script solto (python nucleo/torre.py)
    import leitores  # type: ignore

ESTADOS_AVISO = ("pendente", "enviando", "entregue", "falhou")
_RE_NOME = re.compile(
    r"^(\d{4}-\d{2}-\d{2}-\d{6})-(resposta|comentario|aprovacao|alteracao-laco)-(.+)-"
    r"([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})$")


class GravacaoParcial(Exception):
    """O ``.json`` foi confirmado, mas o ``.md``, o índice ou a fila falharam (§3.5)."""

    def __init__(self, nome: str, causa: BaseException) -> None:
        super().__init__(f"gravação parcial de {nome}: {causa}")
        self.nome = nome
        self.causa = causa


def envio_valido(valor) -> bool:
    """UUID na forma canônica em minúsculas (é o que entra no nome do arquivo); regra única em leitores."""
    return leitores.envio_valido(valor)


def slug_de(texto: str) -> str:
    """Só ``[a-z0-9-]``; nunca vem de texto livre (vem do id da rodada ou do alvo)."""
    s = re.sub(r"[^a-z0-9-]+", "-", texto.lower()).strip("-")
    return s[:80] or "sem-nome"


def nome_mensagem(quando: _dt.datetime, tipo: str, slug: str, envio: str) -> str:
    return f"{quando:%Y-%m-%d-%H%M%S}-{tipo}-{slug}-{envio}"


# ----------------------------------------------------------------------------------------------
# Escrita atômica
# ----------------------------------------------------------------------------------------------


def conferir_pasta_tmp(caixa_real: str, pasta_tmp: str) -> None:
    """``pasta_tmp`` precisa ser exatamente ``<caixa real>/.tmp``: sem atalho nem junction no caminho.

    Regra única do confinamento interno da caixa (§3.2, "sem exceção"), conferida antes de criar, escrever ou
    limpar. Levanta ``ValueError`` em palavras; quem chama não toca em nada fora da caixa.
    """
    esperado = os.path.join(caixa_real, ".tmp")
    real = os.path.realpath(pasta_tmp)
    if os.path.normcase(real) != os.path.normcase(esperado):
        raise ValueError(f"caixa: a pasta temporária {pasta_tmp} é um atalho ou junction para {real}; "
                         "nada foi apagado nem gravado fora da caixa; não há onde gravar com segurança")
    if os.path.lexists(pasta_tmp) and not os.path.isdir(pasta_tmp):
        raise ValueError(f"caixa: {pasta_tmp} existe mas não é uma pasta; não há onde gravar com segurança")


# No Windows, ``os.replace`` falha com acesso negado enquanto outro handle (um leitor de outra thread ou
# processo) está com o destino aberto; a leitura dura milissegundos, então tenta de novo por até ~1 s.
TENTATIVAS_TROCA = 20
ESPERA_TROCA_S = 0.05


def _trocar(origem: str, destino: str) -> None:
    for tentativa in range(TENTATIVAS_TROCA):
        try:
            os.replace(origem, destino)
            return
        except PermissionError:
            if tentativa == TENTATIVAS_TROCA - 1:
                raise
            time.sleep(ESPERA_TROCA_S)


def escrever_atomico(destino: str, texto: str, pasta_tmp: str, caixa_real: str | None = None) -> None:
    """Escreve em ``pasta_tmp``, ``flush`` + ``fsync``, e ``os.replace`` para ``destino``.

    Com ``caixa_real``, confere antes que ``pasta_tmp`` é a ``.tmp`` da caixa (sem atalho) e que ``destino``
    fica dentro da caixa; fora disso levanta ``ValueError`` sem gravar nada.
    """
    if caixa_real is not None:
        conferir_pasta_tmp(caixa_real, pasta_tmp)
        if not leitores.dentro_de(os.path.realpath(os.path.dirname(destino) or "."), caixa_real):
            raise ValueError(f"caixa: o destino {destino} fica fora da caixa; nada foi gravado")
    os.makedirs(pasta_tmp, exist_ok=True)
    temporario = os.path.join(pasta_tmp, f"{os.path.basename(destino)}.{uuid.uuid4().hex[:8]}.parcial")
    try:
        with open(temporario, "w", encoding="utf-8", newline="\n") as f:
            f.write(texto)
            f.flush()
            os.fsync(f.fileno())
        _trocar(temporario, destino)
    finally:
        if os.path.exists(temporario):
            try:
                os.remove(temporario)
            except OSError:
                pass


# ----------------------------------------------------------------------------------------------
# Análise de proposta (compartilhada pela validação e pelo .md)
# ----------------------------------------------------------------------------------------------


def analisar_proposta(original: dict, linhas_resposta: list) -> dict:
    """Compara a proposta-base com as linhas respondidas.

    Devolve ``{"editadas": [(id, coluna, de, para)], "novas": [linha], "removidas": [id],
    "desligadas": [id], "reordenada": bool, "ordem": [ids], "operacoes": set}``.
    Pressupõe linhas já validadas na forma (``id`` str, ``ativa`` bool, ``valores`` dict).
    """
    colunas = list(original.get("colunas", []))
    base = {l["id"]: l for l in original.get("linhas", [])}
    ordem_base = [l["id"] for l in original.get("linhas", [])]
    editadas: list[tuple] = []
    novas: list[dict] = []
    desligadas: list[str] = []
    ids_resposta: list[str] = []
    for linha in linhas_resposta:
        lid = linha["id"]
        ids_resposta.append(lid)
        valores = linha.get("valores") or {}
        if lid in base:
            for col in colunas:
                if col in valores and valores[col] != base[lid].get(col):
                    editadas.append((lid, col, base[lid].get(col), valores[col]))
        else:
            novas.append(linha)
        if linha.get("ativa", True) is False:
            desligadas.append(lid)
    removidas = [i for i in ordem_base if i not in ids_resposta]
    sobreviventes = [i for i in ids_resposta if i in base]
    esperado = [i for i in ordem_base if i in ids_resposta]
    # reordenada se a ordem das linhas antigas mudou, ou se uma nova entrou no meio delas
    n_novas = len(novas)
    novas_no_fim = all(i not in base for i in ids_resposta[len(ids_resposta) - n_novas:]) if n_novas else True
    reordenada = sobreviventes != esperado or not novas_no_fim
    operacoes: set[str] = set()
    if editadas:
        operacoes.add("editar")
    if novas:
        operacoes.add("adicionar")
    if removidas:
        operacoes.add("remover")
    if desligadas:
        operacoes.add("ligar")
    if reordenada:
        operacoes.add("reordenar")
    return {"editadas": editadas, "novas": novas, "removidas": removidas, "desligadas": desligadas,
            "reordenada": reordenada, "ordem": ids_resposta, "operacoes": operacoes}


# ----------------------------------------------------------------------------------------------
# O .md gerado do .json (§4.2)
# ----------------------------------------------------------------------------------------------


def _citacao(texto) -> list[str]:
    """Texto livre, linha a linha, sempre com ``> `` na frente: nada dele vira estrutura."""
    if texto is None:
        return []
    linhas = str(texto).replace("\r\n", "\n").replace("\r", "\n").split("\n")
    return ["> " + l if l else ">" for l in linhas]


def _inline(valor) -> str:
    """Um valor de célula numa linha só, curto, entre aspas."""
    s = "" if valor is None else str(valor)
    s = re.sub(r"\s+", " ", s).strip()
    if len(s) > 80:
        s = s[:77] + "…"
    return '"' + s.replace('"', "'") + '"'


def _rotulo_alvo(dados: dict) -> str:
    alvo = dados.get("alvo") or {}
    return f"{alvo.get('tipo')} {alvo.get('id')}"


def _titulo_alvo(dados: dict, resolver=None) -> str:
    alvo = dados.get("alvo") or {}
    titulo = alvo.get("titulo")
    if not titulo and resolver is not None:
        try:
            titulo = resolver(alvo.get("tipo"), alvo.get("id"))
        except Exception:  # noqa: BLE001 - título é só decoração
            titulo = None
    return titulo or _rotulo_alvo(dados)


def _bloco_comentario(texto, rotulo: str = "comentário") -> list[str]:
    if texto is None or str(texto) == "":
        return []
    return [f"{rotulo}:"] + _citacao(texto)


def _secao_pergunta(pergunta: dict, resposta) -> list[str]:
    tipo = pergunta.get("tipo")
    recomendada = list(pergunta.get("recomendada") or [])
    textos = {o["chave"]: o["texto"] for o in pergunta.get("opcoes") or [] if isinstance(o, dict)}
    linhas: list[str] = [f"## {pergunta.get('titulo')}"]
    if not isinstance(resposta, dict) or _em_branco(tipo, resposta):
        linhas.append("em branco")
        return linhas
    comentario = resposta.get("comentario")
    if tipo == "escolha":
        escolha = list(resposta.get("escolha") or [])
        if escolha:
            chave = escolha[0]
            texto = f"escolha: {chave}, {textos.get(chave, '')}".rstrip(", ")
            if recomendada and chave == recomendada[0]:
                texto += " (a recomendada)"
            elif recomendada:
                texto += f" (a recomendada era {', '.join(recomendada)})"
            linhas.append(texto)
        elif resposta.get("outra"):
            linhas.append("escolha: nenhuma das opções")
        else:
            linhas.append("escolha: em branco")
        linhas += _bloco_comentario(resposta.get("outra"), "outra")
        linhas += _bloco_comentario(comentario)
    elif tipo == "varias":
        escolhas = list(resposta.get("escolha") or [])
        if escolhas:
            texto = "escolhas: " + ", ".join(escolhas)
            if recomendada and set(escolhas) == set(recomendada):
                texto += " (a recomendada)"
            elif recomendada:
                texto += f" (a recomendada era {', '.join(recomendada)})"
            linhas.append(texto)
        elif resposta.get("outra"):
            linhas.append("escolhas: nenhuma das opções")
        else:
            linhas.append("escolhas: em branco")
        linhas += _bloco_comentario(resposta.get("outra"), "outra")
        linhas += _bloco_comentario(comentario)
    elif tipo == "aprovar":
        veredito = resposta.get("veredito")
        nomes = {"aprovado": "aprovado", "aprovado-com-ajuste": "aprovado com ajuste", "recusado": "recusado"}
        linhas.append(f"aprovação: {nomes.get(veredito, veredito) if veredito else 'em branco'}")
        linhas += _bloco_comentario(comentario)
    elif tipo == "texto":
        texto = resposta.get("texto")
        linhas += _citacao(texto) if texto else ["em branco"]
        linhas += _bloco_comentario(comentario)
    elif tipo == "proposta":
        original = pergunta.get("proposta") or {"colunas": [], "linhas": []}
        linhas_resp = resposta.get("linhas")
        if isinstance(linhas_resp, list):
            an = analisar_proposta(original, linhas_resp)
            itens: list[str] = []
            for lid, col, de, para in an["editadas"]:
                itens.append(f'- linha "{lid}": {col} de {_inline(de)} para {_inline(para)}')
            for nova in an["novas"]:
                valores = nova.get("valores") or {}
                celulas = ", ".join(f"{c} {_inline(valores.get(c))}" for c in original.get("colunas", [])
                                    if c in valores)
                itens.append(f'- linha nova "{nova["id"]}": {celulas}'.rstrip(": ") if celulas
                             else f'- linha nova "{nova["id"]}"')
            for lid in an["desligadas"]:
                itens.append(f'- linha "{lid}": desligada')
            for lid in an["removidas"]:
                itens.append(f'- linha "{lid}": removida')
            if an["reordenada"]:
                itens.append("- ordem nova: " + ", ".join(an["ordem"]))
            if itens:
                linhas.append("mudanças:")
                linhas += itens
            else:
                linhas.append("mudanças: nenhuma (a proposta ficou como veio)")
            linhas.append(f"versão completa: no .json irmão, em corpo.respostas.{pergunta.get('id')}")
        else:
            linhas.append("mudanças: nenhuma (a proposta ficou como veio)")
        linhas += _bloco_comentario(comentario)
    else:
        linhas.append("em branco")
    return linhas


def _em_branco(tipo: str | None, resposta: dict) -> bool:
    """Uma resposta a uma pergunta está em branco? (regra única, usada também na validação)."""
    def tem(chave) -> bool:
        v = resposta.get(chave)
        return v is not None and v != "" and v != []
    if tem("comentario"):
        return False
    if tipo in ("escolha", "varias"):
        return not tem("escolha") and not tem("outra")
    if tipo == "aprovar":
        return not tem("veredito")
    if tipo == "texto":
        return not tem("texto")
    if tipo == "proposta":
        return not isinstance(resposta.get("linhas"), list)
    return True


# ----------------------------------------------------------------------------------------------
# Alteração de laço (§4.5): a vista .md e os valores em palavras
# ----------------------------------------------------------------------------------------------

# as chaves de desfecho nascem vazias e só o maestro as preenche (uma linha cada)
CHAVES_DESFECHO = ("aplicando_desde", "aplicado_em", "efeito", "valeu_em", "recibo_execucao", "recibo_antes",
                   "recibo_depois", "recibo_revisao", "agora_esta", "motivo")
QUANDO_VALE_EM_PALAVRAS = {
    "agora": "agora (no ciclo seguinte do laço, sem religar nada)",
    "proxima-onda": "na próxima onda (quando a onda em curso fechar)",
    "ao-reiniciar": "ao reiniciar o processo que lê o valor",
    "proxima-execucao": "só numa partida nova (próxima execução)",
}
RELEITURA_EM_PALAVRAS = {
    "continua": "o laço relê a fonte sozinho a cada ciclo",
    "ao-ligar": "quem lê o valor só lê ao ligar (aplicar = gravar e religar quem lê)",
    "manual": "o maestro troca à mão",
}


def _numero_curto(v) -> str:
    if isinstance(v, bool):
        return str(v).lower()
    if isinstance(v, int):
        return str(v)
    if isinstance(v, float):
        return f"{v:.10g}"
    return str(v)


def valor_em_palavras(controle: dict, valor) -> str:
    """Um valor de controle como a tela e o ``.md`` o dizem: escala, unidade, nulo e rótulo da opção."""
    controle = controle or {}
    if valor is None:
        return controle.get("nulo") or "nulo"
    tipo = controle.get("tipo")
    if tipo in ("numero", "inteiro", "duracao") and isinstance(valor, (int, float)) and not isinstance(valor, bool):
        if controle.get("escala") == "porcento":
            return _numero_curto(round(valor * 100, 10)) + "%"
        unidade = controle.get("unidade")
        return _numero_curto(valor) + (f" {unidade}" if unidade else "")
    if tipo == "escolha":
        rotulos = {o.get("valor"): o.get("rotulo") for o in controle.get("opcoes") or [] if isinstance(o, dict)}
        rotulo = rotulos.get(valor)
        return _inline(valor) + (f" ({rotulo})" if rotulo and rotulo != valor else "")
    if tipo == "lista" and isinstance(valor, list):
        return "{" + ", ".join(_inline(v) for v in valor) + "}"
    if isinstance(valor, str):
        return _inline(valor)
    return _numero_curto(valor)


def onde_esta_em_palavras(origem) -> str:
    """De onde o valor configurado é lido, em palavras (a origem declarada no ``laco.json``, §4.4)."""
    if not isinstance(origem, dict):
        return "origem desconhecida"
    if "declarado" in origem:
        return "declarado pelo maestro no laco.json (não é lido de arquivo)"
    if "arquivo" in origem:
        campo = origem.get("campo")
        return f"{origem['arquivo']}" + (f", chave {campo}" if campo else "")
    if "jsonl" in origem:
        campo = origem.get("campo")
        return f"{origem['jsonl']}, última linha" + (f", chave {campo}" if campo else "")
    if "sqlite" in origem:
        partes = [str(origem["sqlite"]), f"tabela {origem.get('tabela')}"]
        if isinstance(origem.get("onde"), dict):
            partes.append("linha " + " e ".join(f"{k} = {v}" for k, v in origem["onde"].items()))
            partes.append(f"coluna {origem.get('coluna')}")
            if origem.get("campo"):
                partes.append(f"campo {origem['campo']}")
        elif origem.get("soma"):
            partes.append(f"soma de {origem['soma']}")
        elif origem.get("contagem"):
            partes.append("contagem" + (f" por {origem['agrupar']}" if origem.get("agrupar") else ""))
        return ", ".join(partes)
    if "mtime" in origem:
        return f"{origem['mtime']} (hora do arquivo)"
    return "origem desconhecida"


def operacao_em_palavras(dados: dict) -> str:
    """A operação de um pedido de alteração, curta (vai no aviso ao agente e no título da linha)."""
    corpo = dados.get("corpo") or {}
    retrato = dados.get("laco") or {}
    op = corpo.get("operacao")
    no = retrato.get("no") or {}
    if op == "mudar-controle":
        controle = retrato.get("controle") or {}
        return f"mudar \"{controle.get('rotulo') or corpo.get('controle')}\""
    if op == "pedir-parada":
        if corpo.get("capacidade") == "parar-apos-onda":
            return f"pedir parada depois da onda {corpo.get('onda')}"
        return "pedir parada (parar de despachar)"
    if op == "pedir-pausa":
        return "pedir pausa"
    if op == "pedir-retomada":
        return "pedir retomada"
    if op == "comentario-no":
        return f"comentário no nó {no.get('titulo') or corpo.get('no')}"
    if op == "comentario-laco":
        return "comentário no laço inteiro"
    return str(op)


def _linha_do_pedido(dados: dict) -> list[str]:
    corpo = dados.get("corpo") or {}
    retrato = dados.get("laco") or {}
    op = corpo.get("operacao")
    no = retrato.get("no") or {}
    no_txt = f"nó {no.get('titulo') or corpo.get('no')}"
    if op == "mudar-controle":
        controle = retrato.get("controle") or {}
        antes = (corpo.get("antes") or {}).get("valor")
        depois = (corpo.get("depois") or {}).get("valor")
        rotulo = controle.get("rotulo") or corpo.get("controle")
        if controle.get("tipo") == "lista" and isinstance(antes, list) and isinstance(depois, list):
            novos = [v for v in depois if v not in antes]
            saem = [v for v in antes if v not in depois]
            partes = []
            if novos:
                partes.append("adicionar " + ", ".join(_inline(v) for v in novos))
            if saem:
                partes.append("remover " + ", ".join(_inline(v) for v in saem))
            linhas = [f"pedido: mudar \"{rotulo}\" ({no_txt}): {'; '.join(partes) or 'nada'} (configurado)",
                      "conjunto completo: no .json irmão, em corpo.depois"]
        else:
            linhas = [f"pedido: mudar \"{rotulo}\" ({no_txt}) de {valor_em_palavras(controle, antes)} para "
                      f"{valor_em_palavras(controle, depois)} (configurado)"]
        linhas.append(f"controle: {corpo.get('controle')}")
        linhas.append(f"onde está: {onde_esta_em_palavras(controle.get('origem_configurado'))}")
        vale = QUANDO_VALE_EM_PALAVRAS.get(controle.get("quando_vale"), str(controle.get("quando_vale")))
        rel = RELEITURA_EM_PALAVRAS.get(controle.get("releitura"), str(controle.get("releitura")))
        linhas.append(f"vale: {vale}; {rel}")
        config = controle.get("configurado") or {}
        if config.get("ilegivel"):
            linhas.append(f"configurado no envio: ilegível ({config['ilegivel']})")
        else:
            hora = f" às {config['hora']}" if config.get("hora") else ""
            linhas.append(f"configurado no envio: {valor_em_palavras(controle, config.get('valor'))}"
                          f" ({'declarado' if config.get('como') == 'declarado' else 'lido'}{hora})")
        em_uso = controle.get("em_uso") or {}
        if em_uso.get("estado") == "confirmado":
            linhas.append(f"em uso no envio: {valor_em_palavras(controle, em_uso.get('valor'))} "
                          f"(confirmado: {em_uso.get('como')})")
        elif em_uso.get("estado") == "relido":
            linhas.append("em uso no envio: relido pelo laço a cada ciclo (não é prova de uso)")
        else:
            linhas.append("em uso no envio: não confirmado")
        for nome, pre in sorted((controle.get("precondicoes") or {}).items()):
            if isinstance(pre, dict):
                valor = f"ilegível ({pre['ilegivel']})" if pre.get("ilegivel") else _numero_curto(pre.get("valor"))
                linhas.append(f"precondição {nome}: {valor}")
        return linhas
    if op == "pedir-parada":
        if corpo.get("capacidade") == "parar-apos-onda":
            linhas = [f"pedido: parar depois da onda {corpo.get('onda')} (parar-apos-onda: a onda fecha e o laço sai)"]
        else:
            linhas = ["pedido: parar de despachar (parar-de-despachar: nenhum trabalho novo sai; o que está em voo "
                      "termina)"]
        linhas.append("atenção: até valer, chamadas já em voo ainda gastam cota")
        return linhas
    if op == "pedir-pausa":
        return ["pedido: pausar o laço (pausar-retomar: retomada no mesmo ponto, na mesma execução)"]
    if op == "pedir-retomada":
        return ["pedido: retomar o laço pausado (mesma execução)"]
    if op == "comentario-no":
        return [f"pedido: comentário sobre o {no_txt} (id {corpo.get('no')})"]
    if op == "comentario-laco":
        return ["pedido: comentário sobre o laço inteiro"]
    return [f"pedido: {op}"]


def gerar_md_alteracao(dados: dict) -> str:
    """O ``.md`` de uma ``alteracao-laco`` (§4.5), só do ``.json``: frontmatter com as chaves de desfecho vazias."""
    corpo = dados.get("corpo") or {}
    retrato = dados.get("laco") or {}
    front: list[tuple[str, str]] = [
        ("tipo", "alteracao-laco"),
        ("laco", str((dados.get("alvo") or {}).get("id", ""))),
        ("ticket", "" if dados.get("ticket") is None else str(dados["ticket"])),
        ("execucao", str(corpo.get("execucao", ""))),
        ("operacao", str(corpo.get("operacao", ""))),
        ("enviada", str(dados.get("enviada", ""))),
        ("envio", str(dados.get("envio", ""))),
        ("estado", "nova"),
        ("substitui", "" if not dados.get("substitui") else str(dados["substitui"])),
    ] + [(c, "") for c in CHAVES_DESFECHO]
    linhas = ["---"] + [f"{k}: {v}".rstrip() for k, v in front] + ["---", ""]
    titulo = (dados.get("alvo") or {}).get("titulo") or retrato.get("titulo") or (dados.get("alvo") or {}).get("id")
    linhas.append(f"# Alteração de laço: {titulo}")
    linhas.append("")
    linhas += _linha_do_pedido(dados)
    linhas.append(f"revisão vista: {corpo.get('revisao')}")
    linhas.append("texto:")
    texto = corpo.get("texto")
    linhas += _citacao(texto) if texto else ["> (em branco)"]
    return "\n".join(linhas) + "\n"


def gerar_md(dados: dict, resolver_titulo=None) -> str:
    """O ``.md`` de uma mensagem, só a partir do ``.json`` (determinístico).

    ``resolver_titulo(tipo_do_alvo, id)`` é opcional: dá o título em palavras quando o ``.json`` não
    guardou ``alvo.titulo``.
    """
    tipo = dados["tipo"]
    if tipo == "alteracao-laco":
        return gerar_md_alteracao(dados)
    corpo = dados.get("corpo") or {}
    front: list[tuple[str, str]] = [("tipo", tipo)]
    if tipo == "resposta":
        front.append(("rodada", str((dados.get("alvo") or {}).get("id", ""))))
    else:
        front.append(("alvo", _rotulo_alvo(dados)))
    front.append(("ticket", "" if dados.get("ticket") is None else str(dados["ticket"])))
    front.append(("enviada", str(dados.get("enviada", ""))))
    front.append(("envio", str(dados.get("envio", ""))))
    if tipo == "aprovacao":
        front.append(("veredito", str(corpo.get("veredito", ""))))
    front.append(("estado", "nova"))
    front.append(("substitui", "" if not dados.get("substitui") else str(dados["substitui"])))
    linhas = ["---"] + [f"{k}: {v}".rstrip() for k, v in front] + ["---", ""]

    if tipo == "resposta":
        retrato = dados.get("rodada") or {}
        linhas.append(f"# Resposta: {retrato.get('titulo') or retrato.get('id') or ''}".rstrip())
        respostas = corpo.get("respostas") or {}
        for pergunta in retrato.get("perguntas") or []:
            linhas.append("")
            linhas += _secao_pergunta(pergunta, respostas.get(pergunta.get("id")))
    elif tipo == "comentario":
        linhas.append(f"# Comentário: {_titulo_alvo(dados, resolver_titulo)}")
        linhas.append("")
        linhas += _citacao(corpo.get("texto")) or ["em branco"]
    elif tipo == "aprovacao":
        linhas.append(f"# Aprovação: {_titulo_alvo(dados, resolver_titulo)}")
        linhas.append("")
        linhas.append(f"veredito: {corpo.get('veredito')}")
        texto = corpo.get("texto")
        linhas += _bloco_comentario(texto) if texto else ["comentário: em branco"]
    return "\n".join(linhas) + "\n"


# ----------------------------------------------------------------------------------------------
# Fila de avisos (.avisos.json)
# ----------------------------------------------------------------------------------------------


class Fila:
    """``envio → {estado, tentativas, ultimo_erro, proximo}`` persistido em ``caixa/.avisos.json``.

    Ausente ou ilegível → recomeça vazia. Registro malformado (chave que não é UUID, estado desconhecido,
    ``tentativas`` que não é inteiro ≥ 0, ``ultimo_erro`` ou ``proximo`` fora da forma) é descartado com
    problema; a reconciliação recompõe a fila a partir das mensagens válidas. Toda mudança é gravada na hora,
    de forma atômica.

    O arquivo é a verdade e a memória é só cache: antes de cada operação a fila confere (um ``os.stat``) se o
    arquivo mudou em disco desde a última leitura ou gravação própria e, se mudou, relê. É o que deixa o vigia
    do canal B (outro processo) marcar ``entregue`` sem que o servidor reverta a marca na próxima gravação.
    """

    def __init__(self, pasta_caixa: str, lock: threading.RLock) -> None:
        self.pasta_caixa = pasta_caixa
        self.caixa_real = os.path.realpath(pasta_caixa)
        self.caminho = os.path.join(pasta_caixa, ".avisos.json")
        self.pasta_tmp = os.path.join(self.caixa_real, ".tmp")
        self.lock = lock
        self._dados: dict[str, dict] = {}
        self.problemas: list[str] = []  # em palavras; a reconciliação os recolhe
        self._marca: tuple | None = None  # (mtime_ns, tamanho, inode) do arquivo na última leitura/gravação própria
        self.carregar()

    def _marca_atual(self) -> tuple | None:
        try:
            st = os.stat(self.caminho)
        except OSError:
            return None
        return (st.st_mtime_ns, st.st_size, st.st_ino)

    def atualizar(self) -> None:
        """Relê o arquivo se outro processo o mudou (vigia do canal B); barato quando nada mudou."""
        with self.lock:
            if self._marca_atual() != self._marca:
                self.carregar()

    def carregar(self) -> None:
        with self.lock:
            self._marca = self._marca_atual()
            self.problemas = []
            try:
                dados = leitores.ler_avisos_json(self.pasta_caixa)
            except (OSError, ValueError) as e:
                self.problemas.append(f"fila de avisos ilegível, recomeçou vazia: {e}")
                dados = None
            limpos: dict[str, dict] = {}
            for envio, reg in (dados or {}).items():
                motivo = leitores.validar_registro_de_aviso(envio, reg)
                if motivo is not None:
                    self.problemas.append(f"registro {envio!r} descartado da fila: {motivo}")
                    continue
                limpos[envio] = {
                    "estado": reg["estado"],
                    "tentativas": reg.get("tentativas", 0),
                    "ultimo_erro": reg.get("ultimo_erro"),
                    "proximo": reg.get("proximo"),
                }
            self._dados = limpos
            if self.problemas:
                self.salvar()

    def salvar(self) -> None:
        with self.lock:
            escrever_atomico(self.caminho, json.dumps(self._dados, ensure_ascii=False, indent=2) + "\n",
                             self.pasta_tmp, self.caixa_real)
            self._marca = self._marca_atual()

    def obter(self, envio: str) -> dict | None:
        with self.lock:
            self.atualizar()
            reg = self._dados.get(envio)
            return dict(reg) if reg else None

    def estado(self, envio: str) -> str | None:
        reg = self.obter(envio)
        return reg["estado"] if reg else None

    def registrar(self, envio: str) -> None:
        """Entrada ``pendente`` nova (passo 4 da gravação). Não mexe numa que já existe."""
        with self.lock:
            self.atualizar()
            if envio not in self._dados:
                self._dados[envio] = {"estado": "pendente", "tentativas": 0, "ultimo_erro": None, "proximo": None}
                self.salvar()

    def marcar(self, envio: str, estado: str, erro: str | None = None, proximo: str | None = None) -> None:
        """Transição de estado feita por quem envia (marco 7)."""
        if estado not in ESTADOS_AVISO:
            raise ValueError(f"estado de aviso desconhecido: {estado!r}")
        with self.lock:
            self.atualizar()
            reg = self._dados.setdefault(
                envio, {"estado": "pendente", "tentativas": 0, "ultimo_erro": None, "proximo": None})
            if estado == "enviando":
                reg["tentativas"] = reg.get("tentativas", 0) + 1
            reg["estado"] = estado
            reg["ultimo_erro"] = erro
            reg["proximo"] = proximo
            self.salvar()

    def tentar_de_novo(self, envio: str) -> dict | None:
        """``falhou`` volta para ``pendente`` (``POST /api/aviso/tentar``). ``None`` se não existe."""
        with self.lock:
            self.atualizar()
            reg = self._dados.get(envio)
            if reg is None:
                return None
            if reg["estado"] == "falhou":
                reg["estado"] = "pendente"
                reg["proximo"] = None
                self.salvar()
            return dict(reg)

    def pendentes(self, agora: _dt.datetime | None = None) -> list[tuple[str, dict]]:
        """O que está ``pendente`` e já pode sair (``proximo`` vazio ou no passado)."""
        agora = agora or _dt.datetime.now().astimezone()
        saida: list[tuple[str, dict]] = []
        with self.lock:
            self.atualizar()
            for envio, reg in self._dados.items():
                if reg["estado"] != "pendente":
                    continue
                proximo = reg.get("proximo")
                if isinstance(proximo, str) and proximo:
                    try:
                        marca = _dt.datetime.fromisoformat(proximo)
                        if marca.tzinfo is None:
                            marca = marca.astimezone()
                        if marca > agora:
                            continue
                    except (ValueError, OverflowError):
                        pass  # hora ilegível não segura o aviso: sai agora
                saida.append((envio, dict(reg)))
        return saida

    def todos(self) -> dict[str, dict]:
        with self.lock:
            self.atualizar()
            return {k: dict(v) for k, v in self._dados.items()}


# ----------------------------------------------------------------------------------------------
# A caixa
# ----------------------------------------------------------------------------------------------


class Caixa:
    """Gravação, índice em memória e reconciliação da pasta ``caixa/``."""

    def __init__(self, pasta_caixa: str, lock: threading.RLock | None = None, resolver_titulo=None) -> None:
        self.pasta = pasta_caixa
        self.pasta_real = os.path.realpath(pasta_caixa)
        self.pasta_tmp = os.path.join(self.pasta_real, ".tmp")
        self.lock = lock or threading.RLock()
        self.resolver_titulo = resolver_titulo
        self._indice: dict[str, tuple[str, str]] = {}  # envio → (nome, corpo_hash)
        self.problemas: list[tuple[str, str]] = []      # (caminho absoluto, mensagem), só de I/O
        # .tmp que resolve para fora da caixa (atalho ou junction) recusa o arranque sem tocar no alvo (ValueError)
        conferir_pasta_tmp(self.pasta_real, self.pasta_tmp)
        os.makedirs(self.pasta_tmp, exist_ok=True)
        self.fila = Fila(pasta_caixa, self.lock)
        self.reconciliar(arranque=True)

    # -- consulta ------------------------------------------------------------------------------

    def nome_de(self, envio: str) -> str | None:
        with self.lock:
            par = self._indice.get(envio)
            return par[0] if par else None

    def hash_de(self, envio: str) -> str | None:
        with self.lock:
            par = self._indice.get(envio)
            return par[1] if par else None

    def nomes(self) -> set[str]:
        with self.lock:
            return {nome for nome, _ in self._indice.values()}

    def dados_de(self, nome: str) -> dict:
        with open(os.path.join(self.pasta, nome + ".json"), "r", encoding="utf-8-sig") as f:
            return leitores.validar_json_caixa(json.load(f))

    def estado_md(self, nome: str) -> str | None:
        caminho = os.path.join(self.pasta, nome + ".md")
        try:
            campos, _, _ = leitores.ler_frontmatter(leitores.ler_texto(caminho))
        except (OSError, ValueError):
            return None
        return (campos or {}).get("estado") if campos else None

    # -- gravação -------------------------------------------------------------------------------

    def _gravar_json(self, nome: str, dados: dict) -> None:
        escrever_atomico(os.path.join(self.pasta, nome + ".json"),
                         json.dumps(dados, ensure_ascii=False, indent=2) + "\n", self.pasta_tmp, self.pasta_real)

    def _gravar_md(self, nome: str, dados: dict) -> None:
        escrever_atomico(os.path.join(self.pasta, nome + ".md"), gerar_md(dados, self.resolver_titulo),
                         self.pasta_tmp, self.pasta_real)

    def _indexar(self, nome: str, dados: dict) -> None:
        self._indice[dados["envio"]] = (nome, dados["corpo_hash"])

    def gravar(self, dados: dict, quando: _dt.datetime | None = None) -> str:
        """Grava uma mensagem nova na ordem da §3.5 e devolve o nome (sem extensão).

        ``dados`` é o ``.json`` completo e já validado (envio novo). Levanta ``GravacaoParcial``
        quando o ``.json`` foi confirmado mas um passo seguinte falhou: o envio fica no índice e a
        tarefa de reparo completa o resto.
        """
        quando = quando or _dt.datetime.now().astimezone()
        alvo = dados["alvo"]
        # resposta: o id da rodada; alteracao-laco: o id do laço (§4.5); os outros: "<tipo do alvo>-<id>"
        slug = slug_de(alvo["id"] if dados["tipo"] in ("resposta", "alteracao-laco")
                       else f"{alvo['tipo']}-{alvo['id']}")
        nome = nome_mensagem(quando, dados["tipo"], slug, dados["envio"])
        with self.lock:
            self._gravar_json(nome, dados)              # 1
            try:
                self._gravar_md(nome, dados)            # 2
                self._indexar(nome, dados)              # 3
                self.fila.registrar(dados["envio"])     # 4
            except Exception as e:  # noqa: BLE001 - qualquer falha de I/O vira gravação parcial
                self._indice[dados["envio"]] = (nome, dados["corpo_hash"])
                self.problemas.append((os.path.join(self.pasta, nome + ".json"), f"gravação parcial: {e}"))
                raise GravacaoParcial(nome, e) from e
        return nome

    # -- reconciliação ----------------------------------------------------------------------------

    def reconciliar(self, arranque: bool = False) -> list[tuple[str, str]]:
        """Passos 1–5 da §3.5. Roda no arranque, a cada 30 s e antes de cada POST. Idempotente.

        ``enviando`` só volta para ``pendente`` no arranque (``arranque=True``): com o servidor no ar, ``enviando`` é
        um ``ask`` em curso, que bloqueia até o agente ficar ocioso; desfazê-lo mostraria ``pendente`` falso e deixaria
        o vigia do canal B tomar o aviso.
        """
        with self.lock:
            problemas: list[tuple[str, str]] = []
            # 1. apaga caixa/.tmp/*, só o que de fato mora lá: a pasta precisa ser a .tmp real da caixa e cada
            #    item precisa resolver para si mesmo (atalho ou junction fica onde está e vira problema)
            tmp_ok = True
            try:
                conferir_pasta_tmp(self.pasta_real, self.pasta_tmp)
                os.makedirs(self.pasta_tmp, exist_ok=True)
            except (ValueError, OSError) as e:
                tmp_ok = False
                problemas.append((self.pasta_tmp, f"pasta temporária recusada, nada apagado nem gravado: {e}"))
            for nome in (os.listdir(self.pasta_tmp) if tmp_ok else []):
                caminho = os.path.join(self.pasta_tmp, nome)
                if os.path.islink(caminho) or os.path.normcase(os.path.realpath(caminho)) != os.path.normcase(caminho):
                    problemas.append((caminho, "sobra não apagada: é um atalho ou junction, aponta para fora da pasta temporária"))
                    continue
                try:
                    os.remove(caminho)
                except OSError as e:
                    problemas.append((caminho, f"sobra não pôde ser apagada: {e}"))
            # 2. lê todo caixa/*.json e monta o índice (inválido → problema, ignorado)
            jsons, estados, erros = leitores.listar_caixa(self.pasta)
            indice: dict[str, tuple[str, str]] = {}
            for nome, dados in jsons.items():
                indice[dados["envio"]] = (nome, dados.get("corpo_hash", ""))
            self._indice = indice
            # 3. .json sem .md → gera o .md com estado: nova
            for nome, dados in jsons.items():
                if nome not in estados and tmp_ok:
                    try:
                        self._gravar_md(nome, dados)
                        estados[nome] = "nova"
                    except Exception as e:  # noqa: BLE001
                        problemas.append((os.path.join(self.pasta, nome + ".md"), f"não deu para regerar o .md: {e}"))
            # 4. .md sem .json → problema (já vem em ``erros``; nunca apagado)
            # 5. .md com estado: nova sem aviso entregue → pendente; enviando → pendente (só no arranque)
            #    (registros descartados no carregamento são recompostos aqui a partir das mensagens)
            self.fila.atualizar()  # o vigia do canal B pode ter marcado entregue em disco
            for mensagem in self.fila.problemas:
                problemas.append((self.fila.caminho, mensagem))
            self.fila.problemas = []
            mudou = False
            fila = self.fila._dados
            for nome, dados in jsons.items():
                envio = dados["envio"]
                reg = fila.get(envio)
                if reg and reg["estado"] == "enviando":
                    if not arranque:
                        continue
                    reg["estado"] = "pendente"
                    mudou = True
                    continue
                if estados.get(nome) == "nova" and reg is None:
                    fila[envio] = {"estado": "pendente", "tentativas": 0, "ultimo_erro": None, "proximo": None}
                    mudou = True
            if mudou and tmp_ok:
                try:
                    self.fila.salvar()
                except (OSError, ValueError) as e:
                    problemas.append((self.fila.caminho, f"fila não pôde ser gravada: {e}"))
            self.problemas = problemas
            return problemas
