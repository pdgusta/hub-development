import sys
p = sys.argv[1]
s = open(p, encoding='utf-8').read()
R = [
("""    z.append(zona('periferia', '<rect x="990" y="205" width="150" height="135" rx="18"/>', (1000, 231),
        inner=item('Obsidian', '<path d="M1012,320 V274 L1057,250 L1102,274 V320 Z" fill="#fffdf8" stroke="#8b857b" stroke-width="2.5"/>' + t(1057, 302, 'Obsidian', anchor='middle'))))""",
 """    z.append(zona('periferia', '<rect x="985" y="205" width="132" height="135" rx="18"/>', (993, 231),
        inner=item('Obsidian', '<path d="M1002,320 V274 L1038,252 L1074,274 V320 Z" fill="#fffdf8" stroke="#8b857b" stroke-width="2.5"/>' + t(1038, 302, 'Obsidian', anchor='middle'))))"""),
("""        lig('Gustavo → Obsidian', 'M1152,312 H1102', 'editar'),
        lig('Obsidian → Banco local', 'M1057,320 V658 H700', 'editar'),""",
 """        lig('Gustavo → Obsidian', 'M1152,312 H1074', 'editar'),
        lig('Obsidian → Banco local', 'M1038,320 V658 H700', 'editar'),"""),
("lig('Checkpoint → Nota de retomada', 'M752,205 H935 V495 H752', 'disc'),",
 "lig('Checkpoint → Nota de retomada', 'M740,193 V168 H935 V495 H752', 'disc'),"),
]
for a, b in R:
    assert s.count(a) == 1, (a[:80], s.count(a))
    s = s.replace(a, b)
open(p, 'w', encoding='utf-8').write(s)
print('ok')
