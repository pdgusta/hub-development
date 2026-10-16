import sys
p = sys.argv[1]
s = open(p, encoding='utf-8').read()
R = [
# ---------- comum: anel de foco nas pessoas
("""    corpo = (f'<circle cx="{x}" cy="{y-15}" r="7" class="cabeca"/>'""",
 """    corpo = (f'<rect x="{x-17}" y="{y-28}" width="34" height="42" rx="10" class="anel"/>'
             f'<circle cx="{x}" cy="{y-15}" r="7" class="cabeca"/>'"""),
(""".pessoa:hover .corpo,.pessoa:focus-visible .corpo{stroke:var(--tinta);stroke-width:3.5}""",
 """.anel{fill:transparent;stroke:transparent;stroke-width:2.5}
.pessoa:hover .anel,.pessoa:focus-visible .anel{fill:#fff2bf;stroke:var(--tinta)}"""),
# ---------- comum: sinal sempre antes do nome
("""    if anchor == 'start':
        sinal = abre(lx + 8, ly - 5, gid); lx += 22
    else:
        sinal = abre(lx + 12, ly - 5, gid)""",
 """    assert anchor == 'start'  # o sinal vai sempre antes do nome
    sinal = abre(lx + 8, ly - 5, gid); lx += 22"""),
# ---------- A
("""    z.append(zona('disciplina', '<rect x="40" y="60" width="210" height="140" rx="22"/>', (52, 88),
        inner=item('Checkpoint', est(150, 145, 'c-disc') + t(150, 178, 'Checkpoint', anchor='middle'))))""",
 """    z.append(zona('disciplina', '<rect x="40" y="60" width="210" height="155" rx="22"/>', (52, 88),
        inner=item('Checkpoint', est(150, 160, 'c-disc') + t(150, 193, 'Checkpoint', anchor='middle'))))"""),
("""        inner=item('Nota de retomada', est(370, 145, 'c-disc') + t(370, 178, 'Nota de retomada', anchor='middle')) +
              item('Acervo do maestro', est(530, 145, 'c-disc') + t(530, 178, 'Acervo do maestro', anchor='middle'))))
    # portas""",
 """        inner=item('Nota de retomada', est(370, 160, 'c-disc') + t(370, 193, 'Nota de retomada', anchor='middle')) +
              item('Acervo do maestro', est(530, 160, 'c-disc') + t(530, 193, 'Acervo do maestro', anchor='middle'))))
    # portas"""),
("""z.append(zona('portas', '<rect x="280" y="300" width="330" height="222" rx="22"/>', (292, 510),""",
 """z.append(zona('portas', '<rect x="280" y="300" width="330" height="222" rx="22"/>', (292, 330),"""),
("""    z.append(zona('vigilancia', '<rect x="630" y="170" width="280" height="150" rx="22"/>', (642, 198),""",
 """    z.append(zona('vigilancia', '<rect x="745" y="170" width="165" height="150" rx="22"/>', (757, 198),"""),
("lig('Checkpoint → Nota de retomada', 'M159,145 H361', 'disc'),\n        lig('Maestro → Acervo do maestro', 'M748,90 H590 L539,141', 'disc'),\n    ]\n    nomes = nome_linha(330, 324, 'buscar', 'n-busca')",
 "lig('Checkpoint → Nota de retomada', 'M159,160 H361', 'disc'),\n        lig('Maestro → Acervo do maestro', 'M748,90 H600 L539,151', 'disc'),\n    ]\n    nomes = nome_linha(250, 290, 'buscar', 'n-busca')"),
# ---------- B
("""def raiz_quarteirao(x0, y0, gid):  # um quarteirão só, com seis telhados
    f, s, c = COR[gid]
    w = 22.5
    d = f'M{x0},{y0+58} V{y0+16} ' + ' '.join(f'L{x0+w*i+w/2},{y0} L{x0+w*(i+1)},{y0+16}' for i in range(6)) + f' V{y0+58} Z'
    return f'<path d="{d}" fill="#fffdf8" stroke="{s}" stroke-width="2.5" stroke-linejoin="round"/>'""",
 """def raiz_quarteirao(x0, y0, gid):  # um quarteirão só: seis casinhas encostadas, cada uma com o seu telhado
    f, s, c = COR[gid]
    w, alt = 22.5, [44, 36, 48, 40, 46, 38]
    out = ''
    for i, h in enumerate(alt):
        x, base = x0 + w * i, y0 + 58
        out += (f'<path d="M{x},{base} V{base-h+10} L{x+w/2},{base-h} L{x+w},{base-h+10} V{base} Z" fill="#fffdf8" '
                f'stroke="{s}" stroke-width="2.2" stroke-linejoin="round"/>')
    return out"""),
("""def oficina(x, y, gid):
    f, s, c = COR[gid]
    return (f'<path d="M{x},{y+40} V{y+14} L{x+20},{y} V{y+14} L{x+40},{y} V{y+14} L{x+60},{y} V{y+40} Z" fill="#fffdf8" stroke="{s}" stroke-width="2.5" stroke-linejoin="round"/>'
            f'<rect x="{x+22}" y="{y+22}" width="16" height="18" fill="none" stroke="{s}" stroke-width="2"/>')""",
 """def oficina(x, y, gid):  # oficina pequena, telhado de duas águas, porta e janela
    f, s, c = COR[gid]
    return (f'<path d="M{x+4},{y+40} V{y+16} L{x+28},{y+2} L{x+52},{y+16} V{y+40} Z" fill="#fffdf8" stroke="{s}" stroke-width="2.5" stroke-linejoin="round"/>'
            f'<rect x="{x+12}" y="{y+24}" width="12" height="16" fill="none" stroke="{s}" stroke-width="2"/>'
            f'<rect x="{x+32}" y="{y+22}" width="12" height="9" fill="none" stroke="{s}" stroke-width="2"/>')"""),
("""        inner=item('Vigia do sync', '<rect x="728" y="390" width="16" height="64" class="torre"/><path d="M720,390 L736,372 L752,390 Z" class="torre"/>' + t(736, 524, 'Vigia do sync', anchor='middle', extra=' textLength="90" lengthAdjust="spacingAndGlyphs"'))))""",
 """        inner=item('Vigia do sync', t(736, 374, 'Vigia do sync', anchor='middle', extra=' textLength="90" lengthAdjust="spacingAndGlyphs"') +
                   '<path d="M716,398 L736,386 L756,398 Z" class="torre"/><rect x="720" y="398" width="32" height="22" class="torre"/>'
                   '<rect x="728" y="404" width="16" height="9" fill="#c08a2e"/>'
                   '<rect x="731" y="420" width="10" height="56" class="torre"/><path d="M722,476 H750" stroke="#c08a2e" stroke-width="3"/>')))"""),
("""    z.append(zona('periferia', '<rect x="520" y="590" width="255" height="125" rx="16"/>', (744, 616), anchor='end',""",
 """    z.append(zona('periferia', '<rect x="520" y="590" width="255" height="125" rx="16"/>', (532, 616),"""),
("""    mini += ''.join(f'<rect x="{ox+(x-190)*k:.1f}" y="{oy+(y-40)*k:.1f}" width="{w*k:.1f}" height="{h*k:.1f}" rx="5" class="fantasma-bloco"/>' for x, y, w, h in QA)""",
 """    mini += ''.join(f'<rect x="{ox+(x-190)*k:.1f}" y="{oy+(y-40)*k:.1f}" width="{w*k:.1f}" height="{h*k:.1f}" rx="5" fill="{COR[g][1]}" fill-opacity=".3" stroke="{COR[g][1]}" stroke-opacity=".6" stroke-width="1.2"/>'
                    for (x, y, w, h), g in zip(QA, ['portas', 'conteudo', 'nucleo', 'vigilancia', 'disciplina', 'periferia']))"""),
("""    estrada = ('<rect x="848" y="548" width="100" height="24" rx="6" class="via"/>' +
               ''.join(f'<line x1="{x}" y1="560" x2="{x+8}" y2="560" class="faixa"/>' for x in range(856, 940, 18)))""",
 """    estrada = ('<rect x="808" y="548" width="142" height="24" rx="4" class="via"/>' +
               ''.join(f'<line x1="{x}" y1="560" x2="{x+8}" y2="560" class="faixa"/>' for x in range(816, 944, 18)))"""),
("""z.append(zona('fora', '<rect x="815" y="312" width="375" height="378" rx="22" stroke-dasharray="7 5"/>', (1162, 338), anchor='end',""",
 """z.append(zona('fora', '<rect x="838" y="312" width="352" height="378" rx="22" stroke-dasharray="7 5"/>', (850, 338),"""),
("t(898, 598, 'Rede privada', anchor='middle')", "t(879, 598, 'Rede privada', anchor='middle')"),
("""        lig('Vigia do sync → Banco local', 'M736,454 V487 H600', 'vigiar'),
        lig('Banco local → Par B', f'M590,511 V560 H1080 V{oy+(463+48-40)*k:.1f}', 'trocar'),""",
 """        lig('Vigia do sync → Banco local', 'M720,440 H580 V463', 'vigiar'),
        lig('Banco local → Par B', f'M600,495 H660 V560 H1080 V{oy+(463+48-40)*k:.1f}', 'trocar'),"""),
# ---------- C
("""             '<rect x="874" y="108" width="12" height="44" class="torre-fuste"/>'""",
 """             '<rect x="954" y="108" width="12" height="212" class="torre-fuste"/>'
             '<rect x="307" y="322" width="30" height="118" rx="3" fill="#fbf3d6" stroke="#a07800" stroke-dasharray="5 4" stroke-width="2"/>'"""),
("""    z.append(zona('vigilancia', '<rect x="840" y="30" width="220" height="110" rx="18"/>', (852, 58),
        inner=item('Vigia do sync', '<circle cx="880" cy="96" r="13" class="lanterna"/>' + t(903, 101, 'Vigia do sync'))))""",
 """    z.append(zona('vigilancia', '<rect x="920" y="30" width="230" height="110" rx="18"/>', (932, 58),
        inner=item('Vigia do sync', '<circle cx="960" cy="96" r="13" class="lanterna"/>' + t(983, 101, 'Vigia do sync'))))"""),
("item('Checkpoint', sala(740, 205, 'disciplina') + t(722, 210, 'Checkpoint', anchor='end'))",
 "item('Checkpoint', sala(740, 205, 'disciplina') + t(760, 210, 'Checkpoint'))"),
("""    z.append(zona('conteudo', '<rect x="260" y="440" width="660" height="110" rx="0"/>', (272, 466),
        inner=item('Acervo do maestro', sala(580, 495, 'conteudo') + t(580, 528, 'Acervo do maestro', anchor='middle')) +""",
 """    z.append(zona('conteudo', '<rect x="260" y="440" width="660" height="110" rx="0"/>', (772, 466),
        inner=item('Acervo do maestro', sala(340, 500, 'conteudo') + t(340, 476, 'Acervo do maestro', anchor='middle')) +"""),
("""    z.append(zona('periferia', '<rect x="960" y="205" width="160" height="135" rx="18"/>', (972, 231),
        inner=item('Obsidian', '<path d="M985,320 V274 L1030,250 L1075,274 V320 Z" fill="#fffdf8" stroke="#8b857b" stroke-width="2.5"/>' + t(1030, 302, 'Obsidian', anchor='middle'))))""",
 """    z.append(zona('periferia', '<rect x="990" y="205" width="150" height="135" rx="18"/>', (1000, 231),
        inner=item('Obsidian', '<path d="M1012,320 V274 L1057,250 L1102,274 V320 Z" fill="#fffdf8" stroke="#8b857b" stroke-width="2.5"/>' + t(1057, 302, 'Obsidian', anchor='middle'))))"""),
("gente = pessoa('Agentes', 110, 320) + pessoa('Gustavo', 1162, 320) + pessoa('Maestro', 580, 60, 'right')",
 "gente = pessoa('Maestro', 42, 320) + pessoa('Agentes', 150, 320) + pessoa('Gustavo', 1168, 320)"),
("""        lig('Agentes → Camada de busca', 'M126,312 H304', 'buscar'),
        lig('Agentes → Porta do banco', 'M126,330 L156,360 H414', 'gravar'),""",
 """        lig('Agentes → Camada de busca', 'M166,312 H304', 'buscar'),
        lig('Agentes → Porta do banco', 'M166,330 L196,360 H414', 'gravar'),"""),
("lig('Vigia do sync → Banco local', 'M880,109 V588 H660 V645', 'vigiar'),",
 "lig('Vigia do sync → Banco local', 'M960,109 V588 H660 V645', 'vigiar'),"),
("""        lig('Gustavo → Obsidian', 'M1146,312 H1075', 'editar'),
        lig('Obsidian → Banco local', 'M1030,320 V658 H700', 'editar'),
        lig('Checkpoint → Nota de retomada', 'M740,217 V483', 'disc'),
        lig('Maestro → Acervo do maestro', 'M580,78 V483', 'disc'),
    ]
    nomes = nome_linha(214, 302, 'buscar', 'n-busca')""",
 """        lig('Gustavo → Obsidian', 'M1152,312 H1102', 'editar'),
        lig('Obsidian → Banco local', 'M1057,320 V658 H700', 'editar'),
        # checkpoint e maestro descem por fora das salas: o checkpoint pelo poço da direita, o maestro pela lateral esquerda
        lig('Checkpoint → Nota de retomada', 'M752,205 H935 V495 H752', 'disc'),
        lig('Maestro → Acervo do maestro', 'M42,330 V500 H328', 'disc'),
    ]
    nomes = nome_linha(250, 302, 'buscar', 'n-busca')"""),
("'A cidade vista de lado: quanto mais fundo, mais perto da verdade. A gente chega pela rua; regras e portas ficam em cima; o conteúdo mora no subsolo, junto do cofre que o guarda.'",
 "'Vista de lado: quanto mais fundo, mais perto da verdade. O conteúdo mora no subsolo, junto do cofre.'"),
]
for a, b in R:
    assert s.count(a) == 1, (a[:80], s.count(a))
    s = s.replace(a, b)
open(p, 'w', encoding='utf-8').write(s)
print('ok')
