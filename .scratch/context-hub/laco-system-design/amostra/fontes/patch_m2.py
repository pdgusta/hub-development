import sys, re
p = sys.argv[1]
s = open(p, encoding='utf-8').read()

def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:90], s.count(a))
    s = s.replace(a, b)

rep('# Mistura: planta da B com as linhas de quem aciona (da A) e cenários acesos. Conteúdo só de descricao-do-hub.md (v3.1)\n# mais as três respostas da rodada 8 avisadas pelo maestro.',
    '# Mistura, volta 2: planta da B com as linhas de quem aciona (da A) e cenários acesos. Conteúdo só de descricao-do-hub.md (v3.2).')

# ---------------- fichas (Tech lead 5, 6, 8)
rep("""       ('Banco local → Vista Markdown', 'O que chegou pela porta ou do outro par desce ao disco; pela porta, cerca de 0,2 s.', [])]),""",
    """       ('Banco local → Sincronizador → Vista Markdown', 'O que chegou pela porta ou do outro par desce ao disco: o sincronizador (ou o plugin) escreve; pela porta, cerca de 0,2 s.', [])]),""")
rep("""[(AC, 'a guarda de versão e o aviso de conflito: o servidor pronto grava por cima; obrigatórios antes de usar'), (D, 'como os agentes gravam: disco, porta do banco ou os dois'), (D, 'por onde o Claude Desktop grava')],""",
    """[(AC, 'a guarda de versão e o aviso de conflito: o servidor pronto grava por cima; obrigatórios antes de usar'), (D, 'como os agentes gravam: disco, porta do banco ou os dois'), (D, 'por onde o Claude Desktop grava'), (D, 'o que o agente faz quando a porta do banco está fora: grava no disco ou espera')],""")
rep("""     [(D, 'regra de rede que libera a busca aos clientes'), (D, 'a busca e a porta do banco num endereço só')],""",
    """     [(NV, 'como o Obsidian chega à busca do hub'), (D, 'por onde o Claude Desktop chega à busca'), (D, 'regra de rede que libera a busca aos clientes'), (D, 'a busca e a porta do banco num endereço só')],""")
rep("""       ('Obsidian → Camada de busca', 'O Gustavo também busca no hub, pelo Obsidian (ou pedindo a um agente).', []),
       ('Claude Desktop → Camada de busca', 'O Claude Desktop também usa a busca do hub.', []),""",
    """       ('Obsidian → Camada de busca', 'O Gustavo também busca no hub, pelo Obsidian (ou pedindo a um agente).', [(NV, 'como o Obsidian chega à busca do hub')]),
       ('Claude Desktop → Camada de busca', 'O Claude Desktop também usa a busca do hub.', [(D, 'por onde o Desktop chega à busca')]),""")
rep("""       ('Vigia do sync → Banco local, Sincronizador, plugin', 'Lê o estado, a cada 5 min.', []),""",
    """       ('Vigia do sync → Banco local, Sincronizador, plugin', 'Só confere: lê o estado, a cada 5 min; não age no banco.', []),""")
rep("""       ('Checkpoint → Agentes', 'A obrigação de gravar o que a resposta mudou e o que só a memória privada sabe. Ao fim de cada resposta.', []),
       ('Checkpoint → Nota de retomada', 'Confere se a nota reflete a resposta.', []),""",
    """       ('Checkpoint → Agentes', 'A obrigação de gravar o que a resposta mudou e o que só a memória privada sabe. Ao fim de cada resposta.', []),
       ('Checkpoint → Nota de retomada', 'Só confere se a nota reflete a resposta; o hook não grava.', []),
       ('Agentes → Nota de retomada', 'Quem grava a nota é o agente da sessão, obrigado pelo checkpoint.', []),
       ('Maestro → Gustavo', 'O pedido de aval do acervo: a guarda recusa, o verificador confere, o Gustavo aprova.', []),""")
rep("""     aprova='Gustavo, para alterar ou apagar peça citada ou usada, ou mexer em catálogo ou descrição de skill', tambem='Disciplina do agente'),""",
    """     [(D, 'como o erro de uma peça citada que não existe mais chega ao Gustavo')],
     aprova='Gustavo, para alterar ou apagar peça citada ou usada, ou mexer em catálogo ou descrição de skill', tambem='Disciplina do agente'),""")
rep("""     [(EC, 'níveis da árvore e perfil de cada máquina'), (D, 'quem confere os 30 dias do _archive/ e apaga'), (D, 'como algo volta do _archive/')],""",
    """     [(EC, 'níveis da árvore e perfil de cada máquina'), (D, 'quem confere os 30 dias do _archive/ e apaga'), (D, 'como algo volta do _archive/'), (D, 'proteção contra gravar dentro do _archive/'), (D, 'aviso de caminho mudado a quem guardava o caminho antigo')],""")
rep("""   c('Skills', 'Skills do hub, em agents/skills/.',""",
    """   c('Catálogo de blocos e skill "nova iniciativa"', 'agents/blocks.md, citado pelo contrato, e a skill que cria pasta, núcleo e blocos por script; a skill só muda com supervisão e aprovação.',
     [(EC, 'arquitetura de pastas')], dono='Gustavo', aciona='agente cria a pasta pela skill', le='agentes', aprova='Gustavo, para mudar a skill'),
   c('Skills', 'Skills do hub, em agents/skills/.',""")
rep("""       ('Checkpoint → Nota de retomada', 'Confere a nota ao fim de cada resposta; quem grava é o agente.', []),""",
    """       ('Agentes → Nota de retomada', 'O agente da sessão grava a nota, obrigado pelo checkpoint.', []),
       ('Checkpoint → Nota de retomada', 'Só confere a nota ao fim de cada resposta; quem grava é o agente.', []),""")
rep("""       ('Obsidian → Camada de busca', 'O Gustavo busca no hub pelo Obsidian.', [])]),""",
    """       ('Obsidian → Camada de busca', 'O Gustavo busca no hub pelo Obsidian.', [(NV, 'como o Obsidian chega à busca do hub')])]),""")
rep("""  lig=[('Banco local → Outro par', 'As mudanças do próprio par, contínuo, pela rede privada; com a outra desligada, esperam.',""",
    """  lig=[('Banco local ↔ Outro par', 'Cada par envia as próprias mudanças ao outro, contínuo, pela rede privada; com a outra desligada, esperam.',""")
rep("""  lig=[('Gustavo → Agentes', 'Pede: leia, altere, remova.', [])]),""",
    """  lig=[('Gustavo → Agentes', 'Pede: leia, altere, remova. O agente avisa o Gustavo quando algo falha.', []),
       ('Maestro → Gustavo', 'O maestro pede o aval para alterar ou apagar peça usada do acervo.', [])]),""")

# ---------------- cenários (Tech lead 3, 4, 6, 7; UX 2, 3)
ini = s.index('CENARIOS = [')
fim = s.index('CEN = {}')
s = s[:ini] + '''CENARIOS = [  # (texto, chaves, falha ou em aberto); a primeira chave recebe o número
 ('gustavo-edita', 'O Gustavo edita um arquivo', [
   ('O Gustavo abre a nota no Obsidian e edita.', ['Gustavo → Obsidian', 'Gustavo', 'Obsidian'], False),
   ('O Obsidian grava o .md no disco.', ['Obsidian → Vista Markdown', 'Vista Markdown'], False),
   ('O sincronizador (ou o plugin, se o Obsidian está aberto) leva ao banco.', ['Vista Markdown ↔ Sincronizador', 'Sincronizador', 'Sincronizador ↔ Banco local', 'Banco local'], False),
   ('O banco envia a mudança ao outro par, pela rede privada.', ['Banco local ↔ Outro par', 'Rede privada', 'Outro par'], False),
   ('Lá, o disco atualiza e a busca do outro par reindexa.', ['mini:nucleo', 'mini:portas', 'Outro par'], False),
   ('Se o mesmo trecho mudou lá antes da troca: colisão; a vigia avisa.', ['Vigia do sync', 'Vigia do sync → Banco local', 'Banco local'], True)]),
 ('agente-novo', 'Um agente novo abre sessão', [
   ('O Gustavo (ou o Maestri) abre a sessão numa porta de entrada.', ['Gustavo → Agentes', 'Gustavo', 'Agentes'], False),
   ('O contrato chega ao agente.', ['Contrato → Agentes', 'Contrato'], False),
   ('A checagem de sessão lê o estado da vigia e abre a nota de retomada.', ['Nota de retomada', 'Vigia do sync', 'Disciplina do agente'], False),
   ('O agente busca o trecho certo.', ['Agentes → Camada de busca', 'Camada de busca', 'Camada de busca → Vista Markdown', 'Vista Markdown'], False),
   ('Lê e grava pela porta do banco, levando a versão.', ['Agentes → Porta do banco', 'Porta do banco', 'Porta do banco → Banco local', 'Banco local'], False),
   ('Ao fim de cada resposta, o checkpoint confere a nota; se falta, o agente grava.', ['Agentes → Nota de retomada', 'Checkpoint → Nota de retomada', 'Checkpoint', 'Nota de retomada'], False)]),
 ('maestro-novo', 'Um maestro novo abre sessão', [
   ('Uma sessão do Maestri abre; o maestro chega.', ['Maestro'], False),
   ('O contrato (e o lembrete) o manda começar pelo acervo.', ['Contrato → Maestro', 'Contrato'], False),
   ('Lê o catálogo do acervo e escolhe setup e papéis.', ['Maestro → Acervo do maestro', 'Acervo do maestro'], False),
   ('Confere os papéis da biblioteca do Maestri; cria ou reescreve o que difere.', ['Maestro → Biblioteca do Maestri', 'Biblioteca do Maestri', 'Ferramentas da máquina'], False),
   ('O hook de uso registra cada peça usada, no registro de uso do acervo.', ['Acervo do maestro', 'Maestro → Acervo do maestro', 'Disciplina do agente'], False),
   ('Alterar peça usada: no Claude Code, a guarda recusa, o verificador confere e o Gustavo dá o aval.', ['Maestro → Gustavo', 'Gustavo', 'Disciplina do agente', 'Acervo do maestro'], False)]),
 ('pede-ler', 'O Gustavo pede a um agente: leia', [
   ('O Gustavo pede ao agente.', ['Gustavo → Agentes', 'Gustavo', 'Agentes'], False),
   ('O agente acha o trecho pela busca da máquina dele.', ['Agentes → Camada de busca', 'Camada de busca', 'Camada de busca → Vista Markdown', 'Vista Markdown'], False),
   ('Lê pela porta do banco: o texto e a versão.', ['Agentes → Porta do banco', 'Porta do banco', 'Porta do banco → Banco local', 'Banco local'], False),
   ('Se a nota está em conflito, a porta avisa e o agente avisa o Gustavo (a construir).', ['Porta do banco', 'Gustavo → Agentes', 'Gustavo'], True)]),
 ('pede-alterar', 'O Gustavo pede a um agente: altere', [
   ('O Gustavo pede ao agente.', ['Gustavo → Agentes', 'Gustavo', 'Agentes'], False),
   ('O agente lê a nota pela porta e guarda a versão.', ['Agentes → Porta do banco', 'Porta do banco'], False),
   ('Grava levando a versão; se mudou, vira conflito visível (a construir).', ['Porta do banco → Banco local', 'Banco local'], False),
   ('O sincronizador (ou o plugin) escreve no disco; a vista muda em cerca de 0,2 s.', ['Sincronizador ↔ Banco local', 'Sincronizador', 'Vista Markdown ↔ Sincronizador', 'Vista Markdown', 'Obsidian'], False),
   ('O banco envia ao outro par.', ['Banco local ↔ Outro par', 'Rede privada', 'Outro par'], False),
   ('O checkpoint confere a nota de retomada; o agente a grava.', ['Agentes → Nota de retomada', 'Checkpoint → Nota de retomada', 'Checkpoint', 'Nota de retomada'], False),
   ('Em aberto: gravar direto no disco, sem conferir a versão.', ['Agentes → Vista Markdown', 'Vista Markdown'], True)]),
 ('pede-remover', 'O Gustavo pede a um agente: remova', [
   ('O Gustavo pede ("remova a nota X").', ['Gustavo → Agentes', 'Gustavo', 'Agentes'], False),
   ('O script do _archive/ confere se o outro par está em dia e sem edição recente.', ['Banco local ↔ Outro par', 'Outro par', 'Periferia do par'], False),
   ('Move a nota para o _archive/ da raiz; por onde o script grava está em aberto.', ['Agentes → Vista Markdown', 'Vista Markdown', 'Vista Markdown ↔ Sincronizador', 'Sincronizador', 'Sincronizador ↔ Banco local', 'Banco local'], False),
   ('As duas mudanças viajam ao outro par; a busca de cada máquina reindexa.', ['Banco local ↔ Outro par', 'Outro par', 'Camada de busca → Vista Markdown', 'Camada de busca'], False),
   ('Passados 30 dias sem pedido de volta, pode ser apagado. Quem confere: em aberto.', ['Gustavo', 'Conteúdo'], True)]),
 ('outro-par', 'O outro par altera um arquivo', [
   ('Algo muda no banco do outro par.', ['Outro par'], False),
   ('O banco dele envia ao banco daqui, pela rede privada.', ['Banco local ↔ Outro par', 'Rede privada', 'Banco local'], False),
   ('O sincronizador escreve no disco daqui.', ['Sincronizador ↔ Banco local', 'Sincronizador', 'Vista Markdown ↔ Sincronizador', 'Vista Markdown'], False),
   ('A busca daqui reindexa; o Obsidian aberto mostra.', ['Camada de busca → Vista Markdown', 'Camada de busca', 'Obsidian'], False),
   ('Se o mesmo trecho mudou aqui: colisão; a vigia avisa.', ['Vigia do sync', 'Vigia do sync → Banco local', 'Banco local'], True)]),
]
''' + s[fim:]
rep("""for cid, _, passos in CENARIOS:
    for n, (_, chaves) in enumerate(passos, 1):""", """for cid, _, passos in CENARIOS:
    for n, (_, chaves, _f) in enumerate(passos, 1):""")
rep("cen_js = {cid: dict(nome=nome, passos=[[txt, ch] for txt, ch in passos]) for cid, nome, passos in CENARIOS}",
    "cen_js = {cid: dict(nome=nome, passos=[[txt, ch, fl] for txt, ch, fl in passos]) for cid, nome, passos in CENARIOS}")

# ---------------- desenho
rep("""def lig(de_para, d, cls, decidir=False):
    base = f'<path class="lig-fundo" d="{d}"/>' if decidir else ''
    return base + f'<path data-ligacao="{esc(de_para)}"{cen(de_para)} class="lig {cls}" d="{d}"/>'""",
    """def lig(de_para, d, cls, decidir=False):
    base = f'<path class="lig-fundo"{cen(de_para)} d="{d}"/>' if decidir else ''
    return base + f'<path data-ligacao="{esc(de_para)}"{cen(de_para)} class="lig {cls}" d="{d}"><title>{esc(de_para)}</title></path>'""")
rep("""def caixa_ferramentas(x, y, gid):  # decoração, sem item
    s = COR[gid][1]
    return (f'<g aria-hidden="true" opacity=".75"><rect x="{x}" y="{y+12}" width="70" height="34" rx="4" fill="#fffdf8" stroke="{s}" stroke-width="2.2"/>'
            f'<path d="M{x+24},{y+12} V{y+4} H{x+46} V{y+12}" fill="none" stroke="{s}" stroke-width="2.2"/><line x1="{x}" y1="{y+24}" x2="{x+70}" y2="{y+24}" stroke="{s}" stroke-width="1.6"/>'
            f'<rect x="{x+100}" y="{y+8}" width="34" height="38" rx="4" fill="#fffdf8" stroke="{s}" stroke-width="2.2"/><line x1="{x+106}" y1="{y+18}" x2="{x+128}" y2="{y+18}" stroke="{s}" stroke-width="1.6"/>'
            f'<line x1="{x+106}" y1="{y+26}" x2="{x+128}" y2="{y+26}" stroke="{s}" stroke-width="1.6"/><line x1="{x+106}" y1="{y+34}" x2="{x+122}" y2="{y+34}" stroke="{s}" stroke-width="1.6"/></g>')""",
    """def caixa_ferramentas(x, y, gid):  # dois componentes sem rótulo: a configuração (caixa) e a biblioteca do Maestri (caderno de papéis)
    s = COR[gid][1]
    return (item('Configuração de cada ferramenta', f'<rect x="{x}" y="{y+12}" width="70" height="34" rx="4" fill="#fffdf8" stroke="{s}" stroke-width="2.2"/>'
            f'<path d="M{x+24},{y+12} V{y+4} H{x+46} V{y+12}" fill="none" stroke="{s}" stroke-width="2.2"/><line x1="{x}" y1="{y+24}" x2="{x+70}" y2="{y+24}" stroke="{s}" stroke-width="1.6"/>') +
            item('Biblioteca do Maestri', f'<rect x="{x+100}" y="{y+8}" width="34" height="38" rx="4" fill="#fffdf8" stroke="{s}" stroke-width="2.2"/><line x1="{x+106}" y1="{y+18}" x2="{x+128}" y2="{y+18}" stroke="{s}" stroke-width="1.6"/>'
            f'<line x1="{x+106}" y1="{y+26}" x2="{x+128}" y2="{y+26}" stroke="{s}" stroke-width="1.6"/><line x1="{x+106}" y1="{y+34}" x2="{x+122}" y2="{y+34}" stroke="{s}" stroke-width="1.6"/>'))""")
rep("+ portao(190, 66) + portao(190, 182, 34) + portao(190, 262) + portao(190, 670) + portao(900, 262))",
    "+ portao(190, 66) + portao(190, 172, 46) + portao(190, 256) + portao(190, 670) + portao(900, 262))")
rep("item('Nota de retomada', quadro(515, 134, 'conteudo') + t(540, 222, 'Nota de retomada', anchor='middle') + marca2(567, 134, 'disciplina'))",
    "item('Nota de retomada', quadro(515, 134, 'conteudo') + t(577, 166, 'Nota de retomada') + marca2(567, 134, 'disciplina'))")
rep("+ t(430, 448, 'Vista Markdown')) +", "+ t(448, 448, 'Vista Markdown')) +")
# miniatura: os quarteirões da vista e da busca acendem no cenário
rep("""    mini += ''.join(f'<rect x="{X(x)}" y="{Y(y)}" width="{w*k:.1f}" height="{h*k:.1f}" rx="4" fill="{COR[g][1]}" fill-opacity=".3" stroke="{COR[g][1]}" stroke-opacity=".6" stroke-width="1.2"/>'
                    for x, y, w, h, g in QA)""",
    """    mini += ''.join(f'<rect x="{X(x)}" y="{Y(y)}" width="{w*k:.1f}" height="{h*k:.1f}" rx="4" fill="{COR[g][1]}" fill-opacity=".3" stroke="{COR[g][1]}" stroke-opacity=".6" stroke-width="1.2" class="mini"{cen("mini:" + g)}/>'
                    for x, y, w, h, g in QA)""")
ini = s.index('    L = [\n        # agentes (azul)')
fim = s.index('    return muralha + ')
s = s[:ini] + '''    L = [
        # agentes (azul): portas, busca, disco e a nota de retomada
        lig('Agentes → Porta do banco', 'M117,362 H138 L156,380 H178', 'agente'),
        lig('Porta do banco → Banco local', 'M202,380 H470', 'agente'),
        lig('Agentes → Vista Markdown', 'M117,377 H128 L151,414 H420 V466 H430', 'agente disco', decidir=True),
        lig('Agentes → Camada de busca', 'M117,390 H122 L170,485 H176', 'agente busca'),
        lig('Camada de busca → Vista Markdown', 'M204,485 H430', 'agente busca'),
        lig('Agentes → Nota de retomada', 'M117,354 L140,340 V256 H540 V193', 'agente'),
        # o disco e o banco, nos dois sentidos
        lig('Vista Markdown ↔ Sincronizador', 'M470,486 H610', 'sinc'),
        lig('Sincronizador ↔ Banco local', 'M625,471 V404', 'sinc'),
        # Gustavo
        lig('Gustavo → Obsidian', 'M117,670 H289', 'gustavo'),
        lig('Obsidian → Vista Markdown', 'M313,647 V597 H450 V512', 'gustavo'),
        lig('Obsidian → Camada de busca', 'M289,655 H250 V535 H190 V510', 'gustavo'),
        lig('Gustavo → Agentes', 'M100,645 V393', 'gustavo'),
        # regras: o contrato chega ao maestro e aos agentes
        lig('Contrato → Maestro', 'M228,157 H100 V123', 'disc'),
        lig('Contrato → Agentes', 'M226,188 H95 V355', 'disc'),
        # confere (só lê): o checkpoint e a vigia
        lig('Checkpoint → Nota de retomada', 'M407,150 H515', 'confere'),
        lig('Vigia do sync → Banco local', 'M786,379 H675', 'confere'),
        # maestro
        lig('Maestro → Acervo do maestro', 'M117,100 H150 V66 H770 V140', 'maestro'),
        # agendador
        lig('Agendador do Windows → Sincronizador', 'M783,655 H705 V486 H640', 'agendador'),
        lig('Agendador do Windows → Vigia do sync', 'M800,638 V472', 'agendador'),
        # troca entre pares, nos dois sentidos
        lig('Banco local ↔ Outro par', f'M655,356 V262 H{X(655)} V{Y(356)}', 'trocar'),
        # só no cenário: correm por fora, sem cruzar nada
        lig('Maestro → Biblioteca do Maestri', 'M108,85 V16 H1197 V766 H607 V706', 'maestro so-cen'),
        lig('Maestro → Gustavo', 'M92,85 V40 H8 V648 H85', 'maestro so-cen'),
    ]
''' + s[fim:]
rep('viewBox="0 0 1200 770"', 'viewBox="0 0 1200 780"')

# ---------------- CSS
rep("--agente:#2a62a8;--gustavo:#b8462a;--maestro:#a03a6e;--disc:#6f4f92;--agendador:#6b6458;--vigiar:#9a5c0a;--trocar:#3f5a74;--sinc:#3d8a76}",
    "--agente:#2a62a8;--gustavo:#b8462a;--maestro:#0d7480;--disc:#6f4f92;--agendador:#8a6a3a;--confere:#4a433c;--trocar:#3f5a74;--sinc:#3d8a76;--falha:#b3261e}")
rep(""".legenda{display:flex;flex-wrap:wrap;gap:4px 16px;padding:0 24px 6px;font-size:13px;color:var(--suave);list-style:none;margin:0}""",
    """.legendas{padding:0 24px 6px}
.legenda{display:flex;flex-wrap:wrap;gap:4px 16px;padding:0;font-size:13px;color:var(--suave);list-style:none;margin:0 0 3px}
.legenda .tit{font-weight:700;color:var(--tinta);text-transform:uppercase;letter-spacing:.04em;font-size:12px;min-width:92px}
.legenda .sw-conf{height:0;border-top:3px dashed var(--confere);border-radius:0;background:none}""")
rep(".legenda .sw-dec{width:24px;height:10px;border-radius:2px;background:repeating-linear-gradient(90deg,var(--agente) 0 6px,transparent 6px 11px),#f3dc8a}",
    ".legenda .sw-dec{width:24px;height:9px;border-radius:2px;background:repeating-linear-gradient(90deg,var(--agente) 0 6px,transparent 6px 11px),#f8ecbd}")
rep(".lig-fundo{fill:none;stroke:#f3dc8a;stroke-width:13;stroke-linecap:round;stroke-linejoin:round}",
    ".lig-fundo{fill:none;stroke:#f8ecbd;stroke-width:9;stroke-linecap:round;stroke-linejoin:round}\nbody.cen .lig-fundo.aceso{stroke:#f3dc8a;stroke-width:14}")
rep(".lig.vigiar{stroke:var(--vigiar)}", ".lig.confere{stroke:var(--confere);stroke-width:3;stroke-dasharray:10 4 2 4}\n.lig.so-cen{display:none;stroke-width:3.5}\nbody.cen .lig.so-cen.aceso{display:inline}")
rep(".cen-passo{display:flex;", "body.cen .legendas,body.cen .cen-botoes{display:none}\n.cen-passo{position:sticky;top:0;z-index:3;display:flex;")
rep(".cen-n{font-weight:700;font-size:14px;white-space:nowrap}", ".cen-n{font-weight:700;font-size:14px}\n.cen-n .nome{display:block;font-weight:600;color:var(--suave);font-size:13px}")
rep("body.cen .lig.aceso,body.cen .item.aceso{opacity:1}",
    "body.cen .lig.aceso,body.cen .item.aceso{opacity:1}\nbody.cen .mini{opacity:.35}body.cen .mini.aceso{opacity:1;stroke-opacity:1;stroke-width:2.5}")
rep(".marca-passo.agora circle{fill:var(--tinta)}.marca-passo.agora text{fill:#fff}",
    """.marca-passo.agora circle{fill:var(--tinta)}.marca-passo.agora text{fill:#fff}
.marca-passo polygon{fill:#fff;stroke:var(--falha);stroke-width:2.5;stroke-linejoin:round}
.marca-passo.falha text{fill:var(--falha)}.marca-passo.falha.agora polygon{fill:var(--falha)}.marca-passo.falha.agora text{fill:#fff}
body.cen .lig.aceso.falha{stroke:var(--falha);stroke-dasharray:8 5}
body.cen .item.aceso.falha{filter:drop-shadow(0 0 2px var(--falha)) drop-shadow(0 0 5px var(--falha))}
body.cen .bairro.aceso.falha>.zona{stroke:var(--falha);stroke-width:4;stroke-dasharray:9 5}
@media (min-width:761px){body.cen svg.cidade{max-height:calc(100vh - 150px)}}""")

# ---------------- legenda em duas linhas
ini = s.index("LEGENDA = '''"); fim = s.index("def pagina():")
s = s[:ini] + """LEGENDA = '''<div class="legendas">
<ul class="legenda" aria-label="Quem aciona: a linha sai da pessoa">
<li class="tit">Quem aciona</li>
<li><i style="background:var(--agente);height:8px"></i>agentes (a mais grossa: buscar)</li>
<li><i style="background:var(--gustavo)"></i>Gustavo</li>
<li><i style="background:var(--maestro)"></i>maestro</li>
<li class="dica-abre"><span class="ico-abre" aria-hidden="true"></span>cada bairro abre uma ficha: dono, quem aciona, quem lê</li>
</ul>
<ul class="legenda" aria-label="O que corre entre os componentes">
<li class="tit">O que corre</li>
<li><i style="background:var(--disc)"></i>regras (contrato)</li>
<li><i style="background:var(--agendador)"></i>Agendador do Windows (o relógio)</li>
<li><i class="sw-conf"></i>confere, só lê (checkpoint, vigia)</li>
<li><i class="sw-sinc"></i>disco e banco</li>
<li><i style="background:var(--trocar)"></i>troca entre pares</li>
<li><i class="sw-dec"></i>a decidir</li>
<li><i class="sw-cons"></i>a construir</li>
<li><i class="sw-m2"></i>também em outro grupo</li>
</ul></div>'''

""" + s[fim:]

# ---------------- JS
ini = s.index("JS = r'''"); fim = s.index("LEGENDA = '''")
s = s[:ini] + r"""JS = r'''
(function(){
var G=__DADOS__,C=__CEN__;
var NS='http://www.w3.org/2000/svg';
var f=document.getElementById('ficha'),volta=null;
function el(t,c,x){var e=document.createElement(t);if(c)e.className=c;if(x!=null)e.textContent=x;return e}
var CLS={'a decidir':'','não verificado':' nv','a construir':' ac','em curso':' ec'};
function selos(li,ss){ss.forEach(function(s){li.appendChild(el('span','sel'+(CLS[s[0]]||''),s[0]+': '+s[1]))})}
var CAMPOS=[['dono','Dono'],['chega','Por onde chega'],['faz','O que aciona'],['aciona','Quem aciona'],['le','Quem lê'],['ve','Só vê'],['aprova','Aprova'],['tambem','Também em']];
function abrir(id,origem,alvo){var g=G[id];if(!g)return;volta=origem||null;
 var c=document.getElementById('ficha-corpo');c.textContent='';
 c.appendChild(el('h2',null,g.nome));c.appendChild(el('p','frase',g.frase));
 c.appendChild(el('h3',null,id==='gente'?'Quem':'Componentes'));
 var ul=el('ul'),marcado=null;g.itens.forEach(function(i){var li=el('li');li.appendChild(el('b',null,i[0]));li.appendChild(document.createTextNode(i[1]));
  var dl=el('dl');CAMPOS.forEach(function(k){if(i[2][k[0]]){dl.appendChild(el('dt',null,k[1]));dl.appendChild(el('dd',null,i[2][k[0]]))}});
  if(dl.childNodes.length)li.appendChild(dl);selos(li,i[3]);if(alvo&&i[0]===alvo){li.className='alvo';marcado=li}ul.appendChild(li)});c.appendChild(ul);
 if(g.lig.length){c.appendChild(el('h3',null,'Ligações'));var u2=el('ul');g.lig.forEach(function(l){var li=el('li');li.appendChild(el('b',null,l[0]));li.appendChild(document.createTextNode(l[1]));selos(li,l[2]);u2.appendChild(li)});c.appendChild(u2)}
 f.classList.add('aberta');document.getElementById('fechar').focus({preventScroll:true});f.scrollTop=0;
 if(marcado){f.scrollTop=Math.max(0,marcado.offsetTop-80);setTimeout(function(){marcado.classList.add('apaga')},1200)}}
function fechar(){f.classList.remove('aberta');if(volta)volta.focus()}
document.querySelectorAll('[data-abre]').forEach(function(e){
 function vai(ev){var it=ev.target.closest&&ev.target.closest('[data-item]');abrir(e.getAttribute('data-abre'),e,it?it.getAttribute('data-item'):null)}
 e.addEventListener('click',function(ev){ev.stopPropagation();vai(ev)});
 e.addEventListener('keydown',function(ev){if(ev.key==='Enter'||ev.key===' '){ev.preventDefault();ev.stopPropagation();vai(ev)}})});
document.getElementById('fechar').addEventListener('click',fechar);
// cenários: acende o caminho passo a passo
var svg=document.querySelector('svg.cidade'),marcas=document.createElementNS(NS,'g');marcas.setAttribute('aria-hidden','true');svg.appendChild(marcas);
var botoes=document.querySelectorAll('[data-cen]'),painel=document.getElementById('cen-passo'),atual=null,passo=0;
var todos=document.querySelectorAll('[data-cenario]');
function noPasso(e,id,n){return (' '+e.getAttribute('data-cenario')+' ').indexOf(' '+id+':'+n+' ')>=0}
function chave(e){return [e.getAttribute('data-item'),e.getAttribute('data-ligacao'),e.getAttribute('data-grupo'),e.getAttribute('data-cenario')]}
// caixas dos textos do desenho: o número do passo fica a 6 px de qualquer nome
function textos(){var r=[];svg.querySelectorAll('text').forEach(function(t){if(marcas.contains(t))return;var o=t,op=1;while(o&&o!==svg){op*=parseFloat(getComputedStyle(o).opacity);o=o.parentNode}
 if(op<.5)return;var b=t.getBBox();r.push([b.x,b.y,b.x+b.width,b.y+b.height])});return r}
function livre(x,y,caixas){var R=17;return caixas.every(function(b){return x+R<b[0]||x-R>b[2]||y+R<b[1]||y-R>b[3]})}
function candidatos(e){var c=[];if(e.tagName==='path'){var L=e.getTotalLength();[.5,.35,.65,.2,.8].forEach(function(q){var p=e.getPointAtLength(L*q),p2=e.getPointAtLength(Math.min(L,L*q+2));
  var dx=p2.x-p.x,dy=p2.y-p.y,n=Math.hypot(dx,dy)||1;c.push([p.x-dy/n*16,p.y+dx/n*16]);c.push([p.x+dy/n*16,p.y-dx/n*16])});return c}
 var b=e.getBBox();if(e.classList.contains('bairro'))return [[b.x+b.width-20,b.y+b.height-20],[b.x+20,b.y+b.height-20],[b.x+b.width-20,b.y+20]];
 return [[b.x-14,b.y-12],[b.x+b.width+14,b.y-12],[b.x-14,b.y+b.height+12],[b.x+b.width+14,b.y+b.height+12],[b.x+b.width/2,b.y-16],[b.x-16,b.y+b.height/2],[b.x+b.width+16,b.y+b.height/2]]}
function marca(p,n,agora,falha){var g=document.createElementNS(NS,'g');g.setAttribute('class','marca-passo'+(agora?' agora':'')+(falha?' falha':''));
 var f1;if(falha){f1=document.createElementNS(NS,'polygon');f1.setAttribute('points',(p[0])+','+(p[1]-15)+' '+(p[0]+14)+','+(p[1]+10)+' '+(p[0]-14)+','+(p[1]+10))}
 else{f1=document.createElementNS(NS,'circle');f1.setAttribute('cx',p[0]);f1.setAttribute('cy',p[1]);f1.setAttribute('r',11)}
 var tx=document.createElementNS(NS,'text');tx.setAttribute('x',p[0]);tx.setAttribute('y',p[1]+(falha?7:4.5));tx.setAttribute('text-anchor','middle');tx.textContent=n;
 g.appendChild(f1);g.appendChild(tx);marcas.appendChild(g);return g}
function desenhar(){
 todos.forEach(function(e){e.classList.remove('aceso','agora','falha')});marcas.textContent='';
 if(!atual){document.body.classList.remove('cen');painel.hidden=true;return}
 var cen=C[atual],N=cen.passos.length;document.body.classList.add('cen');painel.hidden=false;
 for(var n=1;n<=passo;n++){var fl=cen.passos[n-1][2];
  todos.forEach(function(e){if(noPasso(e,atual,n)){e.classList.add('aceso');if(n===passo)e.classList.add('agora');if(fl)e.classList.add('falha')}})}
 var caixas=textos(),ultima=null;
 for(var n=1;n<=passo;n++){var ch=cen.passos[n-1][1][0],alvo=null;
  todos.forEach(function(e){if(!alvo&&noPasso(e,atual,n)&&chave(e).indexOf(ch)>=0&&!e.classList.contains('lig-fundo'))alvo=e});
  if(!alvo)continue;var cs=candidatos(alvo),p=null;for(var i=0;i<cs.length;i++){if(livre(cs[i][0],cs[i][1],caixas)){p=cs[i];break}}p=p||cs[0];
  ultima=marca(p,n,n===passo,cen.passos[n-1][2]);caixas.push([p[0]-11,p[1]-11,p[0]+11,p[1]+11])}
 document.getElementById('cen-nome').textContent=cen.nome;
 document.getElementById('cen-num').textContent='Passo '+passo+' de '+N+(cen.passos[passo-1][2]?' · falha ou em aberto':'');
 document.getElementById('cen-txt').textContent=cen.passos[passo-1][0];
 document.getElementById('cen-ant').disabled=passo<=1;document.getElementById('cen-prox').disabled=passo>=N;
 botoes.forEach(function(b){b.setAttribute('aria-pressed',b.getAttribute('data-cen')===atual?'true':'false')});
 // a faixa do desenho e a página seguem o passo atual (tela estreita ou baixa)
 if(ultima){var pal=document.querySelector('.palco'),rb=ultima.getBoundingClientRect(),rp=pal.getBoundingClientRect();
  if(rb.left<rp.left+20||rb.right>rp.right-20)pal.scrollLeft+=rb.left-rp.left-rp.width/2;
  var topo=painel.getBoundingClientRect().bottom;if(rb.top<topo+10||rb.bottom>window.innerHeight-10)window.scrollBy(0,rb.top-(topo+window.innerHeight)/2)}}
function sair(){var b=document.querySelector('[data-cen="'+atual+'"]');atual=null;desenhar();if(b)b.focus()}
botoes.forEach(function(b){b.addEventListener('click',function(){atual=b.getAttribute('data-cen');passo=1;desenhar();document.getElementById('cen-prox').focus()})});
document.getElementById('cen-ant').addEventListener('click',function(){if(passo>1){passo--;desenhar()}});
document.getElementById('cen-prox').addEventListener('click',function(){if(atual&&passo<C[atual].passos.length){passo++;desenhar()}});
document.getElementById('cen-sair').addEventListener('click',sair);
document.addEventListener('keydown',function(ev){
 if(ev.key==='Escape'){if(f.classList.contains('aberta'))fechar();else if(atual)sair()}
 if(atual&&!f.classList.contains('aberta')){
  if(ev.key==='ArrowRight'&&passo<C[atual].passos.length){passo++;desenhar()}
  if(ev.key==='ArrowLeft'&&passo>1){passo--;desenhar()}}});
// tela estreita: a faixa abre já centrada no Banco local
function centrar(){var p=document.querySelector('.palco'),b=document.querySelector('[data-item="Banco local"]');
 if(!p||!b||p.scrollWidth<=p.clientWidth+1)return;var rp=p.getBoundingClientRect(),rb=b.getBoundingClientRect();
 p.scrollLeft=Math.max(0,p.scrollLeft+rb.left-rp.left-(rp.width-rb.width)/2)}
if(document.readyState==='complete')centrar();else window.addEventListener('load',centrar);
})();
'''

""" + s[fim:]
rep("#ficha li.alvo{background:#fff6d6;box-shadow:-10px 0 0 #fff6d6,10px 0 0 #fff6d6}",
    "#ficha li.alvo{background:#ffe9a8;box-shadow:-10px 0 0 #ffe9a8,10px 0 0 #ffe9a8;transition:background 1s,box-shadow 1s}\n#ficha li.alvo.apaga{background:#fff6d6;box-shadow:-10px 0 0 #fff6d6,10px 0 0 #fff6d6}")
rep("""<div class="cen-passo" id="cen-passo" hidden aria-live="polite"><span class="cen-n" id="cen-n"></span><span class="cen-txt" id="cen-txt"></span>""",
    """<div class="cen-passo" id="cen-passo" hidden aria-live="polite"><span class="cen-n"><span class="nome" id="cen-nome"></span><span id="cen-num"></span></span><span class="cen-txt" id="cen-txt"></span>""")
rep("""<button type="button" id="cen-sair">Sair</button>""", """<button type="button" id="cen-sair">Sair do cenário</button>""")
open(p, 'w', encoding='utf-8').write(s)
print('ok')
