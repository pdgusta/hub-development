"""Junta as perguntas, tira repetidas e sorteia as duas metades (visíveis e escondidas), estratificado por tipo.

Uso: python dividir.py haiku            -> primeira divisão, só com as perguntas dos Haiku
     python dividir.py gateway <arquivo> -> acrescenta as do gateway; parecida com uma visível vai para as visíveis

Repetida: semelhança de Jaccard entre as palavras com conteúdo (sem palavras vazias) >= LIMIAR. A divisão é
determinística (semente fixa). As cinco perguntas do Gustavo (sementes) vão sempre para as escondidas.
"""
import json, glob, random, re, sys, unicodedata, collections, os

AQUI = os.path.dirname(os.path.abspath(__file__))
LIMIAR = 0.6
SEMENTE = 20261015
VAZIAS = set("""a o as os um uma uns umas de do da dos das em no na nos nas por pelo pela pelos pelas para pra com sem
e ou que se quando como qual quais quem onde porque por que é são está estão ser foi fica ficam isso esse essa este
esta ele ela eles elas seu sua seus suas ao aos à às mais menos já ainda também não sim o-que acontece hub context
gustavo""".split())


def palavras(t):
    t = unicodedata.normalize('NFKD', t.lower())
    t = ''.join(c for c in t if not unicodedata.combining(c))
    return {w for w in re.findall(r'[a-z0-9]+', t) if w not in VAZIAS and len(w) > 2}


def jacc(a, b):
    return len(a & b) / len(a | b) if a and b else 0.0


def ler(caminhos, fonte):
    out = []
    for f in caminhos:
        for l in open(f, encoding='utf-8'):
            l = l.strip()
            if not l:
                continue
            d = json.loads(l)
            d['fonte'] = fonte
            out.append(d)
    return out


def unicas(itens, ja=()):
    vistos = [palavras(x['pergunta']) for x in ja]
    out = []
    for x in itens:
        p = palavras(x['pergunta'])
        if any(jacc(p, v) >= LIMIAR for v in vistos):
            continue
        vistos.append(p)
        out.append(x)
    return out


def sortear(itens, rnd):
    por_tipo = collections.defaultdict(list)
    for x in itens:
        por_tipo[x.get('tipo', '?')].append(x)
    vis, esc = [], []
    for t in sorted(por_tipo):
        g = por_tipo[t]
        rnd.shuffle(g)
        meio = len(g) // 2
        esc += g[:meio]
        vis += g[meio:]
    return vis, esc


def gravar(nome, itens):
    with open(os.path.join(AQUI, nome), 'w', encoding='utf-8') as f:
        for i, x in enumerate(itens, 1):
            f.write(json.dumps(x, ensure_ascii=False) + '\n')


def sementes():
    txt = open(os.path.join(AQUI, 'sementes.md'), encoding='utf-8').read()
    return [{'pergunta': m, 'tipo': 'se-x', 'lente': 'gustavo', 'cita': [], 'fonte': 'gustavo'}
            for m in re.findall(r'^\d+\. (.+)$', txt, re.M)]


if __name__ == '__main__':
    rnd = random.Random(SEMENTE)
    if sys.argv[1] == 'haiku':
        sem = sementes()
        todos = ler(sorted(glob.glob(os.path.join(AQUI, 'haiku', '*.jsonl'))), 'haiku')
        u = unicas(todos, ja=sem)
        vis, esc = sortear(u, rnd)
        esc = sem + esc
        gravar('visiveis.jsonl', vis)
        gravar('escondidas.jsonl', esc)
        print(f'haiku: {len(todos)} lidas, {len(u)} únicas; visíveis {len(vis)}, escondidas {len(esc)} (5 do Gustavo)')
    else:
        vis = ler([os.path.join(AQUI, 'visiveis.jsonl')], None)
        esc = ler([os.path.join(AQUI, 'escondidas.jsonl')], None)
        novos = unicas(ler([sys.argv[2]], 'gateway'), ja=vis + esc)
        perto_vis = [x for x in novos if any(jacc(palavras(x['pergunta']), palavras(v['pergunta'])) >= LIMIAR / 2 for v in vis)]
        resto = [x for x in novos if x not in perto_vis]
        v2, e2 = sortear(resto, rnd)
        gravar('visiveis.jsonl', vis + perto_vis + v2)
        gravar('escondidas.jsonl', esc + e2)
        print(f'gateway: {len(novos)} novas; {len(perto_vis)} parecidas com visíveis foram às visíveis; '
              f'+{len(v2)} visíveis, +{len(e2)} escondidas')
