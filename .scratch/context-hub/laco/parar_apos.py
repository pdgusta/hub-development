"""Para o laço quando uma onda fechar: grava controle.parar = true assim que o histórico tiver a onda pedida.

Uso: python parar_apos.py --onda 5
Os geradores e o juntador leem `parar` e saem; o painel manda a última mensagem e sai.
"""
import argparse, time
from comum import abrir_banco, anexar, caminho, gravar_controle, iso, ler_controle


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--onda", type=int, required=True)
    a = ap.parse_args()
    con = abrir_banco()
    while not any(h["onda"] >= a.onda for h in ler_controle(con, "historico", [])):
        time.sleep(30)
    gravar_controle(con, "parar", True)
    anexar(caminho("estado", "despachante.log.jsonl"), {"gerado_em": iso(), "evento": f"parar depois da onda {a.onda}"})
    print(iso(), "parar gravado depois da onda", a.onda, flush=True)


if __name__ == "__main__":
    main()
