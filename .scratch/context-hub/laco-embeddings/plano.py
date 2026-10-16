"""Plano de cobertura: cria as células da onda 1 (ângulo x língua x formulação) e os dois pedidos de cada uma.

Uso: python plano.py            (idempotente: não duplica células que já existem)
     python plano.py --mostrar  (conta células e pedidos por onda e estado)
"""
import argparse, json
from comum import abrir_banco, caminho, carregar_config, gravar_controle, ler_controle


def ler_plano():
    with open(caminho("plano.json"), encoding="utf-8") as f:
        return json.load(f)


def montar_prompt(plano, lingua, pergunta):
    l = plano["linguas"][lingua]
    return f'{l["contexto"]}\n\n{pergunta}\n\n{plano["formato"].replace("{lingua_nome}", l["nome"])}'


def grupo_de(cfg, lingua):
    for g, ls in cfg["grupos"].items():
        if lingua in ls:
            return g
    raise KeyError(lingua)


def criar_celula(con, cfg, cid, onda, lingua, angulo, origem, prompt):
    """Cria a célula e os dois pedidos (as duas vagas do par). Devolve False se ela já existe."""
    if con.execute("SELECT 1 FROM celulas WHERE id=?", (cid,)).fetchone():
        return False
    con.execute("INSERT INTO celulas (id, onda, grupo, lingua, angulo, origem, prompt) VALUES (?,?,?,?,?,?,?)",
                (cid, onda, grupo_de(cfg, lingua), lingua, angulo, origem, prompt))
    for vaga in (0, 1):
        con.execute("INSERT INTO pedidos (id, celula, vaga) VALUES (?,?,?)", (f"{cid}#{vaga}", cid, vaga))
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mostrar", action="store_true")
    a = ap.parse_args()
    cfg, con, plano = carregar_config(), abrir_banco(), ler_plano()
    if not a.mostrar:
        n = 0
        con.execute("BEGIN IMMEDIATE")
        for angulo, por_lingua in plano["angulos"].items():
            for lingua, perguntas in por_lingua.items():
                for k, pergunta in enumerate(perguntas):
                    n += criar_celula(con, cfg, f"o1.{angulo}.{lingua}.{k}", 1, lingua, angulo, "plano",
                                      montar_prompt(plano, lingua, pergunta))
        if ler_controle(con, "onda") is None:
            gravar_controle(con, "onda", 1)
        con.execute("COMMIT")
        print(n, "células novas na onda 1")
    for r in con.execute("SELECT c.onda, p.estado, COUNT(*) n FROM pedidos p JOIN celulas c ON p.celula=c.id GROUP BY 1, 2 ORDER BY 1, 2"):
        print("onda", r["onda"], r["estado"], r["n"])


if __name__ == "__main__":
    main()
