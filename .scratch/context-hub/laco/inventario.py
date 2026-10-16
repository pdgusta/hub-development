"""Cobertura, passo 3: inventário completo da pesquisa ampla, por script. Nenhum modelo é chamado.

Lê o catálogo depois da junção (`sintese/catalogo-entidades.json`), as áreas da stack (`sintese/stack-areas.json`),
a régua com fonte (`sintese/s3/*.json` e, se existir, `sintese/s6/*.json`) e os conceitos (`sintese/conceitos-final.json`).
Grava `exploracao/anexos/pesquisa-50-inventario.md`: cada entidade de busca e de stack, com o que se sabe e de onde
veio, os finalistas que entraram por fora do catálogo, os conceitos e o que ficou fora (e por qual regra).

Uso: python inventario.py
"""
import collections, glob, json, os, re

AQUI = os.path.dirname(os.path.abspath(__file__))
S = lambda *p: os.path.join(AQUI, "sintese", *p)
RAIZ = os.path.abspath(os.path.join(AQUI, "..", "..", ".."))
SAIDA = os.path.join(RAIZ, "exploracao", "anexos", "pesquisa-50-inventario.md")
AREAS = [("sync_couchdb", "Sync e CouchDB"), ("mcp", "MCP"), ("markdown_frontmatter", "Markdown e frontmatter"),
         ("text_pt", "Texto em português (PLN)"), ("embeddings_rerank", "Embeddings e rerank"),
         ("llm_runtime", "Modelos locais e gateways"), ("text_extraction", "Extração de texto"),
         ("storage_db", "Bancos e armazenamento"), ("events_jobs", "Eventos, filas e vigias"),
         ("api_service", "Serviço e API"), ("agent_framework", "Frameworks de agente e RAG"),
         ("obsidian", "Obsidian"), ("other", "Outros")]
FIT = {"core": "central", "optional": "opcional", "unlikely": "improvável", None: "?"}
REG = {"conferencia-sonnet": "Sonnet", "auditoria-opus": "Opus"}
VAL = {"yes": "sim", "no": "não", "unknown": "?", "partial": "parcial", None: "?"}


def norm(s):
    return re.sub(r"[^a-z0-9]", "", (s or "").lower())


def url_norm(u):
    return re.sub(r"^https?://(www\.)?", "", (u or "").strip().lower()).rstrip("/")


def celula(s, n=90):
    s = re.sub(r"\s+", " ", str(s or "")).replace("|", "/").strip()
    return s if len(s) <= n else s[: n - 1] + "…"


def url_principal(e):
    """A URL da chave principal (gh: vira o repositório; web: vira o endereço); senão, a primeira URL não vazia."""
    k = e["chaves"][0]
    if k.startswith("gh:"):
        return "https://github.com/" + k[3:]
    if k.startswith("web:"):
        return "https://" + k[4:]
    return next((u.strip() for u in e["urls"] if u.strip()), "")


def reguas():
    """Fichas da régua com fonte: {arquivo: ficha}."""
    out = {}
    for pasta in ("s3", "s6"):
        for p in sorted(glob.glob(S(pasta, "*.json"))):
            try:
                out[f"{pasta}/{os.path.basename(p)}"] = json.load(open(p, encoding="utf-8"))
            except ValueError:
                pass
    return out


def main():
    cat = json.load(open(S("catalogo-entidades.json"), encoding="utf-8"))
    areas = {a["chave"]: a for a in (json.load(open(S("stack-areas.json"), encoding="utf-8"))
                                     if os.path.exists(S("stack-areas.json")) else [])}
    conc = json.load(open(S("conceitos-final.json"), encoding="utf-8"))
    fichas = reguas()
    # liga ficha -> entidade pela URL ou pelo nome
    por_url, por_nome, por_chave = {}, {}, {}
    for i, e in enumerate(cat):
        for k in e["chaves"]:
            por_chave[k] = i
        for u in e["urls"]:
            por_url.setdefault(url_norm(u), i)
        por_nome.setdefault(norm(e["nome"]), i)
        for c in e.get("componentes", []):
            por_nome.setdefault(norm(c["nome"]), i)
    regua_de, de_fora = collections.defaultdict(list), []
    for arq, f in fichas.items():
        i = por_chave.get(f.get("chave"))
        if i is None:
            i = por_url.get(url_norm(f.get("url"))) or por_nome.get(norm(f.get("nome")))
        if i is None:
            for parte in re.split(r"\s*[/+]\s*", f.get("nome") or ""):
                i = por_nome.get(norm(parte))
                if i is not None:
                    break
        if i is None:
            de_fora.append((arq, f))
        else:
            regua_de[i].append(arq)

    busca = [(i, e) for i, e in enumerate(cat) if e["registro"].get("serve") == "search"]
    stack = [(i, e) for i, e in enumerate(cat) if e["registro"].get("serve") == "stack"]
    md = ["# Pesquisa ampla: inventário completo", "",
          "Gerado por `.scratch/context-hub/laco/inventario.py` (sem modelo). Complementa a síntese "
          "(`pesquisa-50-sintese.md`): aqui está **tudo** o que a pesquisa achou e julgou útil, e não só o que a síntese "
          "discute. Nada daqui foi apagado dos dados; o que ficou fora está na última seção, com a regra.", "",
          "**Como ler.**",
          "- *Menções*: quantas vezes os geradores do laço citaram o item (memória dos modelos, não popularidade real).",
          "- *MCP / Win / pt*: o que o README diz (conferência do Sonnet ou auditoria do Opus); \"?\" = o README não diz.",
          "- *Régua*: arquivo com a régua do hub conferida em fonte primária, com citação (`laco/sintese/s3/` ou `s6/`). "
          "Sem arquivo, a régua não foi conferida fora do README.",
          "- *Registro*: quem deu o veredito final (Sonnet na conferência, Opus na auditoria).", "",
          f"Totais: **{len(busca)} entidades de busca**, **{len(stack)} de stack**, "
          f"**{len(conc)} conceitos**; {sum(1 for i, _ in busca + stack if regua_de[i])} entidades do catálogo e "
          f"{len(de_fora)} de fora com régua conferida.", ""]

    md += [f"## 1. Busca ({len(busca)} entidades)", "",
           "| # | Nome | Menções | Lugar | Mecanismo | MCP | Win | pt | Régua | Registro | URL | Papel |",
           "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for n, (i, e) in enumerate(busca, 1):
        r = e["registro"]
        md.append(f"| {n} | {celula(e['nome'], 50)} | {e['mencoes']} | {', '.join(r.get('place') or [])} | "
                  f"{', '.join(r.get('mechanism') or [])} | {VAL.get(r.get('mcp'), r.get('mcp'))} | "
                  f"{VAL.get(r.get('windows'), r.get('windows'))} | {VAL.get(r.get('portuguese'), r.get('portuguese'))} | "
                  f"{', '.join(regua_de[i]) or '—'} | {REG.get(e['fonte_registro'], e['fonte_registro'])} | "
                  f"{celula(url_principal(e), 60)} | {celula(r.get('role'))} |")

    md += ["", f"## 2. Stack ({len(stack)} entidades), por área do hub", "",
           "Área e encaixe pelo FreeLLMAPI (2 modelos de famílias diferentes; um 3º desempata). *Encaixe*: central, "
           "opcional ou improvável para este hub. \"Divergente\" = os 3 modelos discordaram.", ""]
    grupos = collections.defaultdict(list)
    for i, e in stack:
        a = areas.get(e["chaves"][0]) or {}
        grupos[a.get("area") or ("divergente" if a.get("estado") == "divergente" else "sem_area")].append((i, e, a))
    for chave, titulo in AREAS + [("divergente", "Divergentes (sem maioria)"), ("sem_area", "Sem classificação")]:
        g = grupos.get(chave)
        if not g:
            continue
        md += [f"### {titulo} ({len(g)})", "",
               "| Nome | Menções | Encaixe | Uso no hub | Régua | Registro | URL |", "|---|---|---|---|---|---|---|"]
        for i, e, a in sorted(g, key=lambda t: ({"core": 0, "optional": 1}.get(t[2].get("fit"), 2), -t[1]["mencoes"])):
            uso = next((r.get("hub_use") for r in a.get("respostas", []) if r.get("area") == a.get("area")), None) \
                or e["registro"].get("role")
            md.append(f"| {celula(e['nome'], 50)} | {e['mencoes']} | {FIT.get(a.get('fit'), a.get('fit'))} | {celula(uso)} | "
                      f"{', '.join(regua_de[i]) or '—'} | {REG.get(e['fonte_registro'], e['fonte_registro'])} | "
                      f"{celula(url_principal(e), 60)} |")
        md.append("")

    md += [f"## 3. Finalistas com régua que vieram de fora do catálogo ({len(de_fora)})", "",
           "Entraram pela varredura com web (S2) ou pelas pesquisas antigas; o laço não os trouxe.", "",
           "| Nome | Papel | Régua | URL |", "|---|---|---|---|"]
    for arq, f in sorted(de_fora, key=lambda t: t[1].get("nome", "").lower()):
        md.append(f"| {celula(f.get('nome'), 50)} | {celula(f.get('papel'), 40)} | {arq} | {celula(f.get('url'), 70)} |")

    md += ["", f"## 4. Conceitos ({len(conc)})", "",
           "Citados por 2 ou mais cartões ou ligados a um projeto do catálogo. Triagem sem fonte primária: na auditoria, "
           "12,5% tinham erro grave.", "", "| Conceito | Cartões | Serve | Ferramentas citadas |", "|---|---|---|---|"]
    for c in conc:
        md.append(f"| {celula(c['conceito'], 60)} | {c['cartoes']} | {c['serve']} | {celula(', '.join(c['ferramentas']), 80)} |")

    md += ["", f"## 5. A régua com fonte, em resumo ({len(fichas)} arquivos, 91 itens: o Tantivy tem duas fichas na S3)", "",
           "Primeiras palavras de cada campo; a ficha completa, com as citações, está no arquivo. \"nao_verificado\" = "
           "a fonte primária não respondeu.", "",
           "| Ficha | Projeto | Windows | MCP | Português | Licença | Último release | Maturidade | Encaixe |",
           "|---|---|---|---|---|---|---|---|---|"]
    for arq, f in sorted(fichas.items(), key=lambda t: (t[1].get("nome_canonico") or t[1].get("nome") or "").lower()):
        md.append(f"| {arq} | {celula(f.get('nome_canonico') or f.get('nome'), 40)} | {celula(f.get('windows'), 45)} | "
                  f"{celula(f.get('mcp'), 45)} | {celula(f.get('portugues'), 45)} | {celula(f.get('licenca'), 20)} | "
                  f"{celula(f.get('ultimo_release'), 30)} | {celula(f.get('maturidade'), 20)} | {celula(f.get('encaixe'), 160)} |")

    final = json.load(open(S("catalogo-final.json"), encoding="utf-8"))
    md += ["", "## 6. O que ficou fora, e por qual regra", "",
           "Números do ticket da pesquisa ampla; os itens continuam nos arquivos de `laco/`.", "",
           "| O quê | Quantos | Regra | Onde está |", "|---|---|---|---|",
           "| Só nome, citado uma vez | 1032 | decisão do Gustavo: fora da triagem | `catalogo/itens.json` |",
           "| Quarentena (ambíguos sem decisão segura) | 193 | Tear, na limpeza | `catalogo/itens.json` |",
           "| Repositórios inventados (README 404) | 620 | sem fonte | `etapas/cartoes/` |",
           "| Repositórios mortos (URL 404) | 212 | sem fonte | `etapas/cartoes/` |",
           "| Julgados sem uso para o hub | 529 | conferência Sonnet / auditoria Opus | `etapas/conferencia/respostas/` |",
           f"| Conceitos com uma citação e sem projeto | {632 - len(conc)} | filtro da S1 | `etapas/conceitos/respostas/` |",
           f"| Duplicatas juntadas | {len(final) - len(cat)} entidades | junção por nome (S1) e pelo juiz (cobertura) | "
           "`sintese/entidades2-decisoes.jsonl` |"]
    os.makedirs(os.path.dirname(SAIDA), exist_ok=True)
    open(SAIDA, "w", encoding="utf-8").write("\n".join(md) + "\n")
    print(SAIDA, "-", len(busca), "busca,", len(stack), "stack,", len(de_fora), "de fora,",
          sum(1 for i, _ in busca + stack if regua_de[i]), "do catálogo com régua")


if __name__ == "__main__":
    main()
