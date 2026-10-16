"""Calibração do limiar de repetidas: pares da amostra por faixa de Jaccard ponderado (IDF), para ler e decidir.
Uso: python calibrar.py [--base teste] [--prefixo 6] [--por-faixa 7]"""
import argparse, itertools, random
import juntar
ap = argparse.ArgumentParser(); ap.add_argument("--base", default="teste"); ap.add_argument("--prefixo", type=int, default=6)
ap.add_argument("--por-faixa", type=int, default=6); ap.add_argument("--sem-idf", action="store_true")
a = ap.parse_args()
qs = list(dict.fromkeys(q["pergunta"] for r in juntar.ler_livro(a.base) for q in r["perguntas"]))
idf, _ = juntar.calcular_idf(qs, a.prefixo)
tk = [juntar.tokens(q, a.prefixo) for q in qs]
faixas = {}
for i, j in itertools.combinations(range(len(qs)), 2):
    s = juntar.jaccard(tk[i], tk[j], None if a.sem_idf else idf)
    if not juntar.mesmo_assunto(juntar.entidades(tk[i], a.prefixo), juntar.entidades(tk[j], a.prefixo)):
        continue
    if s >= 0.3:
        faixas.setdefault(min(int(s * 10), 9), []).append((s, qs[i], qs[j]))
random.seed(1)
print(len(qs), "perguntas distintas; prefixo", a.prefixo, "idf", not a.sem_idf)
for f in sorted(faixas):
    ps = faixas[f]
    print(f"\n== {f/10:.1f}-{(f+1)/10:.1f}: {len(ps)} pares")
    for s, x, y in random.sample(ps, min(a.por_faixa, len(ps))):
        print(f"  {s:.2f} | {x}\n       | {y}")
