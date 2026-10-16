import sys
p = sys.argv[1]
s = open(p, encoding='utf-8').read()
R = [
# A (e todos): rótulo de pessoa ao lado 6 px mais longe do anel
("""        corpo += t(x + 18, y + 2, rotulo, 'rot pess', 'start')
    else:
        corpo += t(x - 18, y + 2, rotulo, 'rot pess', 'end')""",
 """        corpo += t(x + 24, y + 2, rotulo, 'rot pess', 'start')
    else:
        corpo += t(x - 24, y + 2, rotulo, 'rot pess', 'end')"""),
# B: acervo como armazém (porta larga de galpão, sem janela)
("""def armazem(x, y, gid):
    f, s, c = COR[gid]
    return (f'<path d="M{x},{y+18} L{x+30},{y} L{x+60},{y+18} V{y+52} H{x} Z" fill="#fffdf8" stroke="{s}" stroke-width="2.5" stroke-linejoin="round"/>'
            f'<rect x="{x+20}" y="{y+30}" width="20" height="22" fill="none" stroke="{s}" stroke-width="2"/>')""",
 """def armazem(x, y, gid):  # galpão baixo e largo, porta de enrolar, sem janela
    f, s, c = COR[gid]
    ripas = ''.join(f'<line x1="{x+12}" y1="{y+33+i*5}" x2="{x+56}" y2="{y+33+i*5}" stroke="{s}" stroke-width="1.4"/>' for i in range(4))
    return (f'<path d="M{x-4},{y+52} V{y+16} Q{x+34},{y} {x+72},{y+16} V{y+52} Z" fill="#fffdf8" stroke="{s}" stroke-width="2.5" stroke-linejoin="round"/>'
            f'<rect x="{x+10}" y="{y+26}" width="48" height="26" fill="none" stroke="{s}" stroke-width="2.2"/>{ripas}')"""),
("item('Acervo do maestro', armazem(630, 128, 'conteudo') + t(660, 214, 'Acervo do maestro', anchor='middle'))",
 "item('Acervo do maestro', armazem(626, 128, 'conteudo') + t(660, 214, 'Acervo do maestro', anchor='middle'))"),
("lig('Maestro → Acervo do maestro', 'M90,104 H660 V128', 'disc'),",
 "lig('Maestro → Acervo do maestro', 'M90,104 H660 V136', 'disc'),"),
# B: nome da Periferia na base da caixa, longe da linha verde
("""    z.append(zona('periferia', '<rect x="520" y="590" width="255" height="125" rx="16"/>', (532, 616),""",
 """    z.append(zona('periferia', '<rect x="520" y="590" width="255" height="125" rx="16"/>', (532, 704),"""),
# C: prédio e faixas terminam em 900; poço do checkpoint a 10 da parede
("""             '<rect x="260" y="150" width="660" height="170" class="predio"/>'""",
 """             '<rect x="260" y="150" width="640" height="170" class="predio"/>'"""),
("""zona('disciplina', '<rect x="260" y="150" width="660" height="90" rx="0"/>'""", """zona('disciplina', '<rect x="260" y="150" width="640" height="90" rx="0"/>'"""),
("""zona('portas', '<rect x="260" y="270" width="660" height="125" rx="0"/>'""", """zona('portas', '<rect x="260" y="270" width="640" height="125" rx="0"/>'"""),
("""zona('nucleo', '<rect x="260" y="600" width="660" height="190" rx="0"/>'""", """zona('nucleo', '<rect x="260" y="600" width="640" height="190" rx="0"/>'"""),
# C: Conteúdo com o nome à esquerda, sob a boca do poço; o nome do acervo embaixo da estação
("""    z.append(zona('conteudo', '<rect x="260" y="440" width="660" height="110" rx="0"/>', (772, 466),
        inner=item('Acervo do maestro', sala(340, 500, 'conteudo') + t(340, 476, 'Acervo do maestro', anchor='middle')) +""",
 """    z.append(zona('conteudo', '<rect x="260" y="440" width="640" height="110" rx="0"/>', (272, 466),
        inner=item('Acervo do maestro', sala(340, 500, 'conteudo') + t(340, 534, 'Acervo do maestro', anchor='middle')) +"""),
("lig('Checkpoint → Nota de retomada', 'M740,193 V168 H935 V495 H752', 'disc'),",
 "lig('Checkpoint → Nota de retomada', 'M740,193 V168 H910 V495 H752', 'disc'),"),
]
for a, b in R:
    assert s.count(a) == 1, (a[:80], s.count(a))
    s = s.replace(a, b)
open(p, 'w', encoding='utf-8').write(s)
print('ok')
