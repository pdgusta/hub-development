"""Etapa 3 do pós-laço: monta os pacotes da conferência (cartão + respostas da triagem) para os subagentes Sonnet.

Entram os itens triados (repositórios e sites) em que a triagem marcou "search" ou "stack", ou dúvida, ou em que os
dois modelos do FreeLLMAPI divergiram. Conceitos não entram (vão direto à auditoria). Nenhum modelo é chamado; pode
rodar de novo para incluir itens triados depois.

Saídas: etapas/conferencia/pacotes/<slug>.json e etapas/conferencia/fila.json ([{"chave", "slug", "motivo"}]).
Uso: python preparar_conferencia.py
"""
import collections, glob, json, os, re

AQUI = os.path.dirname(os.path.abspath(__file__))
E = lambda *p: os.path.join(AQUI, "etapas", *p)


def slug(ch):
    return re.sub(r"[^A-Za-z0-9._-]+", "__", ch)[:150]


def main():
    respostas = collections.defaultdict(list)
    for l in open(E("triagem", "freellm.jsonl"), encoding="utf-8"):
        r = json.loads(l)
        respostas[r["chave"]].append({"por": r["modelo"], "resposta": r["resposta"]})
    for f in glob.glob(E("triagem", "haiku", "*.json")):
        r = json.load(open(f, encoding="utf-8"))
        respostas[r["chave"]].append({"por": r.get("modelo", "claude-haiku-5-5"), "resposta": r["resposta"]})
    os.makedirs(E("conferencia", "pacotes"), exist_ok=True)
    fila, motivos = [], collections.Counter()
    for ch, rs in sorted(respostas.items()):
        rs = rs[:2]
        servs = {x["resposta"].get("serve") for x in rs}
        if len(servs) > 1:
            motivo = "divergente"
        elif any(x["resposta"].get("doubt") for x in rs):
            motivo = "duvida"
        elif servs & {"search", "stack"}:
            motivo = servs.pop()
        else:
            continue
        cartao = json.load(open(E("cartoes", slug(ch) + ".json"), encoding="utf-8"))
        pac = {k: cartao.get(k) for k in ("chave", "nomes", "urls", "readme_cortado", "readme")}
        pac["fonte"] = cartao.get("fonte", "readme")
        pac["respostas"] = rs
        json.dump(pac, open(E("conferencia", "pacotes", slug(ch) + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        fila.append({"chave": ch, "slug": slug(ch), "motivo": motivo, "fonte": pac["fonte"]})
        motivos[motivo] += 1
    json.dump(fila, open(E("conferencia", "fila.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    print(len(fila), "itens para conferir:", dict(motivos), dict(collections.Counter(f["fonte"] for f in fila)))


if __name__ == "__main__":
    main()
