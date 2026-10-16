# Volta 2: gera conceito-a/b/c.html com os consertos da porta. Conteúdo só do texto-do-hub.md.
import json, sys, os
from html import escape as esc

OUT = sys.argv[1]
D = 'a decidir'
NV = 'não verificado'

# ---------------------------------------------------------------- conteúdo (texto do hub, seções 3, 3.5, 4, 7)
# item: (rótulo, papel, [(selo, texto)]); ligação: (de → para, o que passa, [(selo, texto)])
G = {
 'nucleo': dict(nome='Núcleo de dados do par', frase='Os três guardam ou movem a mesma verdade dentro da máquina.',
   itens=[('Banco local','Guarda a verdade: cada nota com histórico de versões e as versões em conflito; o texto fica cifrado. Vai ao banco todo arquivo comum até 200 MiB.',[(NV,'arquivos entre 50 e 200 MiB; conferir na construção')]),
          ('Vista Markdown','Os arquivos no disco por onde o Gustavo vê e edita o hub; gerada a partir do banco, e a edição volta ao banco.',[]),
          ('Sincronizador','Liga disco e banco local o tempo todo, nos dois sentidos, sem depender do Obsidian aberto; pega o que qualquer agente grava no disco.',[])],
   lig=[('Vista Markdown → Sincronizador → Banco local','Mudanças de arquivo, nos dois sentidos. Sempre.',[])]),
 'portas': dict(nome='Portas do par', frase='Por elas os agentes e os clientes alcançam o núcleo. A camada de busca é a porta do conteúdo.',
   itens=[('Camada de busca','Entrega ao agente o trecho certo sem ele ler tudo; é por ela que o agente chega ao conteúdo. A busca não pode ser feita pelo próprio banco, porque o texto lá é cifrado.',
            [(D,'onde mora: duas opções em teste, busca no disco com alcance pela rede, ou índice dentro da porta do banco'),(D,'ferramenta de busca e modelo de embeddings')]),
          ('Porta do banco','Porta do agente ao banco: lê devolvendo a versão, grava levando a versão lida, e vira conflito visível se ela mudou.',
            [(D,'como os agentes gravam: disco, porta do banco ou os dois, e como conferem a versão no disco'),(NV,'duas instâncias do MCP por par')]),
          ('Porta de leitura','Segunda porta do par, exposta na rede só para os clientes, com token.',[(NV,'duas instâncias do MCP por par')])],
   lig=[('Agentes → Camada de busca','Pergunta → trecho certo. É o caminho normal até o conteúdo.',[(D,'onde a busca mora')]),
        ('Agentes → Porta do banco → Banco local','Leitura com versão; gravação com a versão lida.',[(D,'como os agentes gravam')]),
        ('Cliente → Porta de leitura','Consultas por HTTP com token; nunca recebe a credencial do banco.',[])]),
 'vigilancia': dict(nome='Vigilância', frase='Ligadas à garantia: nada diverge em silêncio.',
   itens=[('Vigia do sync','Confere a cada 5 min as trocas, os conflitos abertos, os binários descartados, os arquivos grandes demais e se o sincronizador está vivo; grava um estado curto e avisa quando piora.',[]),
          ('Avisos','Três saídas da vigia: notificação do Windows, o estado curto lido no início de sessão e um mod do Claude Code que mostra o estado o tempo todo.',[(D,'a forma do mod da vigia')]),
          ('Checagem de sessão','No começo de toda sessão de agente: lê o estado da vigia, informa a hora da última troca e abre a nota de retomada.',[])],
   lig=[('Vigia do sync → Banco local, Sincronizador, Obsidian','Lê o estado das trocas, a cada 5 min.',[]),
        ('Vigia do sync → Avisos','Aviso de divergência quando o estado piora.',[]),
        ('Estado curto e nota de retomada → Checagem de sessão','No início de toda sessão.',[])]),
 'disciplina': dict(nome='Disciplina do agente', frase='Fazem o agente gravar no lugar certo, sem pedido.',
   itens=[('Contrato','As regras do hub para os agentes (AGENTS.md na raiz), incluindo o lugar de cada informação. O hub não tem CLAUDE.md.',[]),
          ('Checkpoint','Ao fim de cada resposta, obriga o agente a manter a nota de retomada em dia e a levar ao hub o que só a memória privada da ferramenta sabe. Hoje garantido só no Claude Code.',[(D,'hooks no Codex e no Copilot')]),
          ('Guarda do acervo','Fiscaliza gravações no acervo do maestro: no Claude Code recusa ou pede aval e exige um verificador noutro modelo; Codex e Copilot deixam propostas.',[(NV,'ligação de pasta no lugar de link, regra pelos dois caminhos no Windows, aval num terminal sem ninguém olhando, tempo do verificador')]),
          ('Registro de uso','Anota, por máquina, quem usa cada peça do acervo; gravado por hook.',[])],
   lig=[('Checkpoint → Nota de retomada','O que a resposta mudou. Ao fim de cada resposta.',[]),
        ('Agentes → Guarda do acervo → Acervo do maestro','Gravação liberada, recusada ou com pedido de aval.',[]),
        ('Hook de uso → Registro de uso','Quem usou qual peça, por máquina.',[]),
        ('Contrato e skills do hub → configuração de cada ferramenta','Link para o AGENTS.md; skills por ligação de pasta. Fixo, montado pelo kit de par.',[(D,'como cada ferramenta carrega contrato e MCP'),(D,'roteamento de skills: como as skills ficam visíveis')])]),
 'conteudo': dict(nome='Conteúdo', frase='As seis raízes, com tudo o que mora dentro delas. É o que o banco guarda e a vista mostra; chega-se a ele pela camada de busca.',
   itens=[('Raiz','Seis raízes, cada uma com comportamento próprio: clients, operations, initiatives, reference, agents e inbox. O que termina vai ao _archive da própria raiz.',[(D,'a árvore abaixo das seis raízes e o frontmatter'),(D,'zonas por ciclo de vida: só aparecem na exploração, não foram fixadas')]),
          ('Iniciativa','Frente de trabalho com identificador, estado e próxima ação; mora numa casa só.',[]),
          ('Nota de retomada','Um arquivo curto por trabalho, sobrescrito, com sete campos; qualquer sessão continua de onde a outra parou.',[]),
          ('Acervo do maestro','Peças prontas para todo maestro do Maestri (papéis, setups, contratos-opção), como família de skills. Opções, não regras.',[]),
          ('Pasta não replicada','Parte do hub numa máquina só, fora do sync e da cópia de segurança.',[(D,'mecanismo: replicação filtrada ou fora do banco'),(D,'perfil por máquina: o que é local de cada uma')])],
   lig=[('Maestro → Acervo do maestro','O maestro começa pelo acervo.',[])]),
 'periferia': dict(nome='Periferia do par', frase='Estão no par, mas não guardam nem movem a verdade do dia a dia.',
   itens=[('Obsidian','Só para ver, editar e resolver conflito; pode ficar fechado. O cofre é a raiz do hub.',[(D,'convivência com o Obsidian do vault enquanto os dois existem')]),
          ('Cópia local (git)','Um .git na raiz de cada máquina: só faz commit e push, nunca escreve no disco do hub.',[]),
          ('Nó da rede','Põe o par na rede privada entre as máquinas.',[])],
   lig=[('Gustavo → Obsidian → Banco local','Edições do Gustavo e conflitos para resolver. Só com o Obsidian aberto.',[]),
        ('Cópia local (git) → Cópia no GitHub','Commit e push da vista, uma vez por dia.',[])]),
 'fora': dict(nome='Fora do par', frase='O outro par fica do outro lado da rede privada, igual a este.',
   itens=[('Rede privada','O único caminho entre pares e entre cliente e par. Nunca exposta à internet.',[]),
          ('Par B','O outro par: cópia completa e editável, trabalha sozinho e troca mudanças direto com este. Nenhum é referência.',[]),
          ('Cópia no GitHub','Cópia de segurança diária da vista, um ramo por máquina. Não é ponto de encontro do sync.',[]),
          ('Cliente','Computador ou sandbox que usa o hub através de um par, sem cópia; só lê por padrão; precisa de um par ligado.',[]),
          ('Claude Desktop','Lê pelo MCP, por uma ponte local até a porta do banco.',[(D,'se grava')]),
          ('Vault (referência)','Só referência: o agente pode ler, o hub não grava nada nele. Só existe no notebook.',[])],
   lig=[('Banco local → Par B','As mudanças do próprio par; contínuo, com os dois ligados, pela rede privada.',[]),
        ('Claude Desktop → Porta do banco','Leitura, por ponte local.',[])]),
 'gente': dict(nome='Quem chega ao hub', frase='Gente e agentes ficam fora dos bairros e chegam pelas portas. A porta diz onde a sessão abre; o conteúdo se alcança pela busca.',
   itens=[('Agentes','Claude Code, Codex e Copilot, dentro ou fora do Maestri.',[]),
          ('Gustavo','Pelo Obsidian, na vista Markdown.',[]),
          ('Maestro','Maestro do Maestri: começa pelo acervo do maestro.',[])],
   lig=[]),
}
PAPEL = {r: p for g in G.values() for (r, p, d) in g['itens']}

COR = {  # fundo, traço, texto do nome do bairro
 'nucleo': ('#dcece5', '#3d8a76', '#1d5a4c'),
 'portas': ('#e0e7f4', '#4a6fae', '#2c4f8a'),
 'vigilancia': ('#f6e6c8', '#c08a2e', '#7a4b0a'),
 'disciplina': ('#ece2f1', '#8a62a0', '#5f3a74'),
 'conteudo': ('#f4e7d8', '#b07d4c', '#6f4722'),
 'periferia': ('#e9e7e2', '#8b857b', '#4f4a44'),
 'fora': ('#e6ecf1', '#6d8396', '#3f5163'),
}

# ---------------------------------------------------------------- peças de SVG
def t(x, y, s, cls='rot', anchor='start', extra=''):
    return f'<text x="{x}" y="{y}" class="{cls}" text-anchor="{anchor}"{extra}>{esc(s)}</text>'

def abre(cx, cy, gid):  # sinal de "o bairro abre": círculo com mais, sem texto
    f, s, c = COR[gid]
    return (f'<g class="abre" aria-hidden="true"><circle cx="{cx}" cy="{cy}" r="8.5" fill="#fffdf8" stroke="{c}" stroke-width="1.8"/>'
            f'<path d="M{cx-4},{cy} H{cx+4} M{cx},{cy-4} V{cy+4}" stroke="{c}" stroke-width="1.8" stroke-linecap="round"/></g>')

def zona(gid, shape, label_xy, anchor='start', inner=''):
    f, s, c = COR[gid]
    nome = G[gid]['nome']
    lx, ly = label_xy
    assert anchor == 'start'  # o sinal vai sempre antes do nome
    sinal = abre(lx + 8, ly - 5, gid); lx += 22
    return (f'<g class="bairro" data-grupo="{esc(nome)}" data-abre="{gid}" tabindex="0" role="button" '
            f'aria-label="Abrir a ficha: {esc(nome)}">'
            f'{shape.replace("/>", f" class=\"zona\" fill=\"{f}\" stroke=\"{s}\"/>", 1)}'
            f'<text x="{lx}" y="{ly}" class="grp" text-anchor="{anchor}" fill="{c}">{esc(nome)}</text>{sinal}'
            f'{inner}</g>')

def item(rotulo, corpo, extra_cls=''):
    return (f'<g class="item {extra_cls}" data-item="{esc(rotulo)}"><title>{esc(rotulo)}: {esc(PAPEL.get(rotulo, ""))}</title>'
            f'{corpo}</g>')

def chip(x, y):
    return (f'<g class="decidir"><rect x="{x}" y="{y}" width="70" height="19" rx="9.5" fill="#fff2bf" stroke="#a07800"/>'
            f'<text x="{x+35}" y="{y+13.5}" class="chip" text-anchor="middle">a decidir</text></g>')

def pessoa(rotulo, x, y, lpos='above'):
    corpo = (f'<rect x="{x-17}" y="{y-25}" width="34" height="38" rx="10" class="anel"/>'
             f'<circle cx="{x}" cy="{y-15}" r="7" class="cabeca"/>'
             f'<path d="M{x-11},{y+8} Q{x-11},{y-6} {x},{y-6} Q{x+11},{y-6} {x+11},{y+8} Z" class="corpo"/>')
    if lpos == 'above':
        corpo += t(x, y - 30, rotulo, 'rot pess', 'middle')
    elif lpos == 'right':
        corpo += t(x + 24, y + 2, rotulo, 'rot pess', 'start')
    else:
        corpo += t(x - 24, y + 2, rotulo, 'rot pess', 'end')
    return (f'<g class="item pessoa" data-item="{rotulo}" data-abre="gente" tabindex="0" role="button" '
            f'aria-label="Abrir a ficha: quem chega ao hub ({rotulo})"><title>{rotulo}: {esc(PAPEL[rotulo])}</title>{corpo}</g>')

def lig(de_para, d, cls):
    return f'<path data-ligacao="{esc(de_para)}" class="lig {cls}" d="{d}"/>'

def nome_linha(x, y, s, cls, anchor='middle'):
    return f'<text x="{x}" y="{y}" class="nlin {cls}" text-anchor="{anchor}">{esc(s)}</text>'

DEFS = '''<defs>
<pattern id="hachura" width="7" height="7" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
<rect width="7" height="7" fill="#fffaf0"/><line x1="0" y1="0" x2="0" y2="7" stroke="#c9a640" stroke-width="2.4"/></pattern>
</defs>'''
HACH = 'fill="url(#hachura)" stroke="#a07800" stroke-dasharray="4 3" stroke-width="2"'

# ---------------------------------------------------------------- Conceito A: linhas de metrô
def est(x, y, cls, r=9, decidir=False):
    if decidir:
        return f'<circle cx="{x}" cy="{y}" r="{r+4}" {HACH}/><circle cx="{x}" cy="{y}" r="{r-3}" class="est {cls}"/>'
    return f'<circle cx="{x}" cy="{y}" r="{r}" class="est {cls}"/>'

def conceito_a():
    z = []
    z.append(zona('disciplina', '<rect x="40" y="60" width="210" height="155" rx="22"/>', (52, 88),
        inner=item('Checkpoint', est(150, 160, 'c-disc') + t(150, 193, 'Checkpoint', anchor='middle'))))
    z.append(zona('conteudo', '<rect x="280" y="40" width="330" height="260" rx="22"/>', (292, 68),
        inner=item('Nota de retomada', est(370, 160, 'c-disc') + t(370, 193, 'Nota de retomada', anchor='middle')) +
              item('Acervo do maestro', est(530, 160, 'c-disc') + t(530, 193, 'Acervo do maestro', anchor='middle'))))
    # portas encostadas no conteúdo: a camada de busca fica na borda comum
    z.append(zona('portas', '<rect x="280" y="300" width="330" height="222" rx="22"/>', (292, 330),
        inner=item('Porta do banco', est(440, 460, 'c-grav') + t(440, 444, 'Porta do banco', anchor='middle'))))
    z.append(zona('vigilancia', '<rect x="745" y="170" width="165" height="150" rx="22"/>', (757, 198),
        inner=item('Vigia do sync', est(880, 255, 'c-vig') + t(862, 260, 'Vigia do sync', anchor='end'))))
    baldeacao = ('<rect data-encontro="Banco local" x="650" y="440" width="150" height="50" rx="25" class="encontro"/>'
                 '<rect x="657" y="447" width="136" height="36" rx="18" fill="none" stroke="#2b2622" stroke-width="1.2"/>')
    z.append(zona('nucleo', '<rect x="630" y="392" width="280" height="258" rx="22"/>', (642, 420),
        inner=item('Banco local', baldeacao + t(725, 471, 'Banco local', anchor='middle')) +
              item('Sincronizador', est(740, 530, 'c-sinc', r=8) + t(760, 535, 'Sincronizador')) +
              item('Vista Markdown', est(740, 600, 'c-sinc', r=8) + t(760, 605, 'Vista Markdown'))))
    z.append(zona('periferia', '<rect x="400" y="560" width="210" height="105" rx="22"/>', (412, 588),
        inner=item('Obsidian', est(540, 625, 'c-edit') + t(522, 630, 'Obsidian', anchor='end'))))
    trilho = ('<rect x="935" y="466" width="125" height="24" rx="6" class="via"/>' +
              ''.join(f'<line x1="{x}" y1="462" x2="{x}" y2="494" class="dormente"/>' for x in range(945, 1060, 16)))
    terminal = ('<rect x="1090" y="456" width="86" height="44" rx="10" class="encontro fantasma"/>'
                '<rect x="1170" y="450" width="8" height="56" rx="2" fill="#6d8396"/>')
    z.append(zona('fora', '<rect x="920" y="380" width="268" height="180" rx="22" stroke-dasharray="7 5"/>', (932, 408),
        inner=item('Rede privada', trilho + t(998, 522, 'Rede privada', anchor='middle')) +
              item('Par B', terminal + t(1128, 484, 'Par B', anchor='middle'))))
    # camada de busca por último entre os bairros: desenhada por cima da borda comum de Conteúdo e Portas
    busca = zona_item_portas_busca_a()
    gente = pessoa('Agentes', 110, 400, 'left') + pessoa('Gustavo', 540, 722, 'right') + pessoa('Maestro', 760, 90, 'right')
    L = [
        lig('Agentes → Camada de busca', 'M124,384 L208,300 H424', 'buscar'),
        lig('Agentes → Porta do banco', 'M124,406 L178,460 H430', 'gravar'),
        lig('Porta do banco → Banco local', 'M450,460 H650', 'gravar'),
        lig('Sincronizador → Banco local', 'M740,522 V490', 'sinc'),
        lig('Vista Markdown → Sincronizador', 'M740,592 V538', 'sinc'),
        lig('Vigia do sync → Banco local', 'M880,267 V452 H800', 'vigiar'),
        lig('Banco local → Par B', 'M800,478 H1090', 'trocar'),
        lig('Gustavo → Obsidian', 'M540,700 V636', 'editar'),
        lig('Obsidian → Banco local', 'M549,616 L662,490', 'editar'),
        lig('Checkpoint → Nota de retomada', 'M159,160 H361', 'disc'),
        lig('Maestro → Acervo do maestro', 'M748,90 H600 L539,151', 'disc'),
    ]
    nomes = nome_linha(250, 290, 'buscar', 'n-busca') + nome_linha(548, 449, 'gravar', 'n-grav')
    return ''.join(z) + busca + ''.join(L) + nomes + gente

def zona_item_portas_busca_a():
    # mesmo grupo (Portas do par), num <g> à parte para ficar por cima da borda do Conteúdo
    nome = G['portas']['nome']
    return (f'<g data-grupo="{esc(nome)}">' +
            item('Camada de busca', est(440, 300, 'c-busca', r=13, decidir=True) + t(462, 326, 'Camada de busca') + chip(462, 334)) + '</g>')

# ---------------------------------------------------------------- Conceito B: duas cidades e a estrada
def predio(x, y, w, h, gid):
    f, s, c = COR[gid]
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="4" fill="#fffdf8" stroke="{s}" stroke-width="2.5"/>'

def raiz_quarteirao(x0, y0, gid):  # um quarteirão só: seis casinhas encostadas, cada uma com o seu telhado
    f, s, c = COR[gid]
    w, alt = 22.5, [44, 36, 48, 40, 46, 38]
    out = ''
    for i, h in enumerate(alt):
        x, base = x0 + w * i, y0 + 58
        out += (f'<path d="M{x},{base} V{base-h+10} L{x+w/2},{base-h} L{x+w},{base-h+10} V{base} Z" fill="#fffdf8" '
                f'stroke="{s}" stroke-width="2.2" stroke-linejoin="round"/>')
    return out

def armazem(x, y, gid):  # galpão baixo e largo, porta de enrolar, sem janela
    f, s, c = COR[gid]
    ripas = ''.join(f'<line x1="{x+12}" y1="{y+33+i*5}" x2="{x+56}" y2="{y+33+i*5}" stroke="{s}" stroke-width="1.4"/>' for i in range(4))
    return (f'<path d="M{x-4},{y+52} V{y+16} Q{x+34},{y} {x+72},{y+16} V{y+52} Z" fill="#fffdf8" stroke="{s}" stroke-width="2.5" stroke-linejoin="round"/>'
            f'<rect x="{x+10}" y="{y+26}" width="48" height="26" fill="none" stroke="{s}" stroke-width="2.2"/>{ripas}')

def prefeitura(x, y, gid):
    f, s, c = COR[gid]
    cols = ''.join(f'<line x1="{x+10+i*10}" y1="{y+20}" x2="{x+10+i*10}" y2="{y+44}" stroke="{s}" stroke-width="2.5"/>' for i in range(4))
    return (f'<path d="M{x},{y+18} L{x+30},{y} L{x+60},{y+18} Z" fill="#fffdf8" stroke="{s}" stroke-width="2.5" stroke-linejoin="round"/>'
            f'{cols}<rect x="{x-2}" y="{y+44}" width="64" height="7" rx="2" fill="#fffdf8" stroke="{s}" stroke-width="2.5"/>')

def oficina(x, y, gid):  # oficina pequena, telhado de duas águas, porta e janela
    f, s, c = COR[gid]
    return (f'<path d="M{x+4},{y+40} V{y+16} L{x+28},{y+2} L{x+52},{y+16} V{y+40} Z" fill="#fffdf8" stroke="{s}" stroke-width="2.5" stroke-linejoin="round"/>'
            f'<rect x="{x+12}" y="{y+24}" width="12" height="16" fill="none" stroke="{s}" stroke-width="2"/>'
            f'<rect x="{x+32}" y="{y+22}" width="12" height="9" fill="none" stroke="{s}" stroke-width="2"/>')

# quarteirões do par A (x, y, w, h), usados também na miniatura do par B
QA = [(160, 150, 200, 370), (400, 60, 375, 220), (395, 320, 245, 220), (680, 320, 112, 220), (220, 590, 260, 125), (520, 590, 255, 125)]

def conceito_b():
    muralha = ('<rect x="190" y="40" width="615" height="690" rx="26" class="muralha"/>'
               '<rect x="200" y="551" width="595" height="18" class="rua"/>'
               # portão sem nome na muralha esquerda, por onde entra o maestro
               '<rect x="183" y="88" width="14" height="24" fill="#f6f1e7"/>'
               '<rect x="181" y="84" width="18" height="5" rx="2" fill="#b9ad98"/><rect x="181" y="111" width="18" height="5" rx="2" fill="#b9ad98"/>')
    z = []
    z.append(zona('portas', '<rect x="160" y="150" width="200" height="370" rx="18"/>', (172, 178),
        inner=item('Camada de busca', f'<rect x="176" y="222" width="28" height="56" rx="6" {HACH}/>' + t(176, 212, 'Camada de busca') + chip(176, 288)) +
              item('Porta do banco', '<rect x="178" y="465" width="24" height="44" rx="6" class="portao"/>' + t(216, 470, 'Porta do banco'))))
    z.append('<rect x="205" y="243" width="195" height="14" class="rua rua-busca"/>')
    z.append(zona('conteudo', '<rect x="400" y="60" width="375" height="220" rx="16"/>', (412, 86),
        inner=item('Raiz', raiz_quarteirao(425, 124, 'conteudo') + t(492, 214, 'Raiz', anchor='middle')) +
              item('Acervo do maestro', armazem(626, 128, 'conteudo') + t(660, 214, 'Acervo do maestro', anchor='middle'))))
    z.append(zona('nucleo', '<rect x="395" y="320" width="245" height="220" rx="16"/>', (407, 346),
        inner=item('Vista Markdown', predio(412, 367, 18, 16, 'nucleo') + t(438, 381, 'Vista Markdown')) +
              item('Sincronizador', predio(412, 417, 18, 16, 'nucleo') + t(438, 431, 'Sincronizador')) +
              item('Banco local', '<rect data-encontro="Banco local" x="412" y="463" width="188" height="48" rx="12" class="encontro cofre"/>' + t(506, 492, 'Banco local', anchor='middle'))))
    z.append(zona('vigilancia', '<rect x="680" y="320" width="112" height="220" rx="16"/>', (686, 346),
        inner=item('Vigia do sync', t(736, 374, 'Vigia do sync', anchor='middle', extra=' textLength="90" lengthAdjust="spacingAndGlyphs"') +
                   '<path d="M716,398 L736,386 L756,398 Z" class="torre"/><rect x="720" y="398" width="32" height="22" class="torre"/>'
                   '<rect x="728" y="404" width="16" height="9" fill="#c08a2e"/>'
                   '<rect x="731" y="420" width="10" height="56" class="torre"/><path d="M722,476 H750" stroke="#c08a2e" stroke-width="3"/>')))
    z.append(zona('disciplina', '<rect x="220" y="590" width="260" height="125" rx="16"/>', (232, 616),
        inner=item('Contrato', prefeitura(250, 638, 'disciplina') + t(326, 676, 'Contrato'))))
    z.append(zona('periferia', '<rect x="520" y="590" width="255" height="125" rx="16"/>', (532, 704),
        inner=item('Obsidian', oficina(540, 636, 'periferia') + t(612, 666, 'Obsidian'))))
    # par B: a mesma planta, em miniatura (0,4), com a rua no mesmo nível da rua do par A
    k, ox, oy = 0.4, 950, 352
    mini = f'<rect x="{ox}" y="{oy}" width="{615*k:.1f}" height="{690*k:.1f}" rx="10" class="muralha fantasma"/>'
    mini += f'<rect x="{ox+4}" y="{oy+(551-40)*k:.1f}" width="{595*k:.1f}" height="{18*k:.1f}" class="rua"/>'
    mini += ''.join(f'<rect x="{ox+(x-190)*k:.1f}" y="{oy+(y-40)*k:.1f}" width="{w*k:.1f}" height="{h*k:.1f}" rx="5" fill="{COR[g][1]}" fill-opacity=".3" stroke="{COR[g][1]}" stroke-opacity=".6" stroke-width="1.2"/>'
                    for (x, y, w, h), g in zip(QA, ['portas', 'conteudo', 'nucleo', 'vigilancia', 'disciplina', 'periferia']))
    cofre_b = f'<rect x="{ox+(412-190)*k:.1f}" y="{oy+(463-40)*k:.1f}" width="{188*k:.1f}" height="{48*k:.1f}" rx="5" class="encontro fantasma"/>'
    estrada = ('<rect x="808" y="548" width="142" height="24" rx="4" class="via"/>' +
               ''.join(f'<line x1="{x}" y1="560" x2="{x+8}" y2="560" class="faixa"/>' for x in range(816, 944, 18)))
    z.append(zona('fora', '<rect x="838" y="312" width="352" height="378" rx="22" stroke-dasharray="7 5"/>', (850, 338),
        inner=item('Rede privada', estrada + t(879, 598, 'Rede privada', anchor='middle')) + mini +
              item('Par B', cofre_b + t(1048, 660, 'Par B', anchor='middle', cls='rot parb'))))
    gente = pessoa('Maestro', 70, 110) + pessoa('Agentes', 70, 345) + pessoa('Gustavo', 70, 650)
    L = [
        lig('Agentes → Camada de busca', 'M90,338 H118 L176,262', 'buscar'),
        lig('Agentes → Porta do banco', 'M90,352 H118 L172,487 H178', 'gravar'),
        lig('Porta do banco → Banco local', 'M202,487 H412', 'gravar'),
        lig('Vista Markdown → Sincronizador', 'M421,383 V417', 'sinc'),
        lig('Sincronizador → Banco local', 'M421,433 V463', 'sinc'),
        lig('Vigia do sync → Banco local', 'M720,440 H580 V463', 'vigiar'),
        lig('Banco local → Par B', f'M600,495 H660 V560 H1080 V{oy+(463+48-40)*k:.1f}', 'trocar'),
        lig('Gustavo → Obsidian', 'M90,655 H118 L150,560 H500 V660 H540', 'editar'),
        lig('Obsidian → Banco local', 'M570,636 V511', 'editar'),
        lig('Maestro → Acervo do maestro', 'M90,104 H660 V136', 'disc'),
    ]
    nomes = nome_linha(168, 238, 'buscar', 'n-busca', 'end') + nome_linha(300, 506, 'gravar', 'n-grav')
    return muralha + ''.join(z) + ''.join(L) + nomes + gente

# ---------------------------------------------------------------- Conceito C: a cidade em corte
def sala(x, y, gid, w=24, h=24):
    f, s, c = COR[gid]
    return f'<rect x="{x-w/2}" y="{y-h/2}" width="{w}" height="{h}" rx="5" fill="#fffdf8" stroke="{s}" stroke-width="2.5"/>'

def conceito_c():
    fundo = ('<rect x="0" y="320" width="1200" height="480" class="terra"/>'
             '<rect x="260" y="150" width="640" height="170" class="predio"/>'
             '<rect x="954" y="108" width="12" height="212" class="torre-fuste"/>'
             '<rect x="307" y="322" width="30" height="118" rx="3" fill="#fbf3d6" stroke="#a07800" stroke-dasharray="5 4" stroke-width="2"/>'
             '<line x1="0" y1="320" x2="1200" y2="320" class="chao"/>')
    z = []
    z.append(zona('vigilancia', '<rect x="920" y="30" width="230" height="110" rx="18"/>', (932, 58),
        inner=item('Vigia do sync', '<circle cx="960" cy="96" r="13" class="lanterna"/>' + t(983, 101, 'Vigia do sync'))))
    z.append(zona('disciplina', '<rect x="260" y="150" width="640" height="90" rx="0"/>', (272, 176),
        inner=item('Checkpoint', sala(740, 205, 'disciplina') + t(760, 210, 'Checkpoint'))))
    z.append(zona('portas', '<rect x="260" y="270" width="640" height="125" rx="0"/>', (272, 386),
        inner=item('Camada de busca', f'<path d="M304,320 V298 Q304,282 322,282 Q340,282 340,298 V320 Z" {HACH}/>' + t(350, 302, 'Camada de busca') + chip(482, 288)) +
              item('Porta do banco', '<rect x="414" y="348" width="32" height="24" rx="4" class="portao"/><path d="M422,356 L430,365 L438,356" class="seta-porta claro"/>' + t(456, 366, 'Porta do banco'))))
    z.append(zona('conteudo', '<rect x="260" y="440" width="640" height="110" rx="0"/>', (272, 466),
        inner=item('Acervo do maestro', sala(340, 500, 'conteudo') + t(340, 534, 'Acervo do maestro', anchor='middle')) +
              item('Nota de retomada', sala(740, 495, 'conteudo') + t(740, 528, 'Nota de retomada', anchor='middle'))))
    z.append(zona('nucleo', '<rect x="260" y="600" width="640" height="190" rx="0"/>', (272, 626),
        inner=item('Vista Markdown', sala(320, 660, 'nucleo', 20, 20) + t(340, 665, 'Vista Markdown')) +
              item('Sincronizador', sala(320, 720, 'nucleo', 20, 20) + t(340, 725, 'Sincronizador')) +
              item('Banco local', '<rect data-encontro="Banco local" x="500" y="645" width="200" height="70" rx="12" class="encontro cofre"/>' + t(600, 686, 'Banco local', anchor='middle'))))
    z.append(zona('periferia', '<rect x="983" y="205" width="150" height="135" rx="18"/>', (991, 231),
        inner=item('Obsidian', '<path d="M1002,320 V274 L1038,252 L1074,274 V320 Z" fill="#fffdf8" stroke="#8b857b" stroke-width="2.5"/>' + t(1038, 302, 'Obsidian', anchor='middle'))))
    z.append(zona('fora', '<rect x="935" y="675" width="258" height="115" rx="18" stroke-dasharray="7 5"/>', (947, 778),
        inner=item('Rede privada', '<rect x="950" y="688" width="120" height="28" rx="14" class="via"/>' + t(1010, 742, 'Rede privada', anchor='middle')) +
              item('Par B', '<rect x="1100" y="680" width="86" height="44" rx="10" class="encontro fantasma"/>' + t(1143, 708, 'Par B', anchor='middle'))))
    gente = pessoa('Maestro', 42, 320) + pessoa('Agentes', 150, 320) + pessoa('Gustavo', 1168, 320)
    L = [
        lig('Agentes → Camada de busca', 'M166,312 H304', 'buscar'),
        lig('Agentes → Porta do banco', 'M166,330 L196,360 H414', 'gravar'),
        lig('Porta do banco → Banco local', 'M430,372 V578 H540 V645', 'gravar'),
        lig('Vista Markdown → Sincronizador', 'M320,670 V710', 'sinc'),
        lig('Sincronizador → Banco local', 'M320,730 V768 H600 V715', 'sinc'),
        lig('Vigia do sync → Banco local', 'M960,109 V588 H660 V645', 'vigiar'),
        lig('Banco local → Par B', 'M700,702 H1100', 'trocar'),
        lig('Gustavo → Obsidian', 'M1152,312 H1074', 'editar'),
        lig('Obsidian → Banco local', 'M1038,320 V658 H700', 'editar'),
        # checkpoint e maestro descem por fora das salas: o checkpoint pelo poço da direita, o maestro pela lateral esquerda
        lig('Checkpoint → Nota de retomada', 'M740,193 V168 H910 V495 H752', 'disc'),
        lig('Maestro → Acervo do maestro', 'M42,330 V500 H328', 'disc'),
    ]
    nomes = nome_linha(250, 302, 'buscar', 'n-busca') + nome_linha(300, 352, 'gravar', 'n-grav')
    return fundo + ''.join(z) + ''.join(L) + nomes + gente

# ---------------------------------------------------------------- página
CSS = r'''
:root{--papel:#f6f1e7;--tinta:#2b2622;--suave:#4a433c;--linha:#d9cfbf;--cartao:#fffcf6;
--buscar:#0b6f7a;--gravar:#1f3b73;--trocar:#8e3b5b;--vigiar:#9a5c0a;--editar:#3d7429;--disc:#6b5f53;--sinc:#5c7391}
*{box-sizing:border-box}
html,body{margin:0;background:var(--papel);color:var(--tinta);font-family:"Segoe UI",system-ui,-apple-system,Roboto,sans-serif}
header{padding:14px 24px 6px;display:flex;flex-wrap:wrap;gap:6px 22px;align-items:baseline}
h1{font-family:Georgia,"Times New Roman",serif;font-size:26px;margin:0;font-weight:700}
.ideia{margin:0;color:var(--suave);font-size:15px;max-width:68ch}
.legenda{display:flex;flex-wrap:wrap;gap:4px 16px;padding:0 24px 6px;font-size:13px;color:var(--suave);list-style:none;margin:0}
.legenda li{display:flex;align-items:center;gap:6px}
.legenda i{display:inline-block;width:24px;height:5px;border-radius:3px}
.legenda .sw-sinc{height:0;border-top:4px dotted var(--sinc);border-radius:0;background:none}
.legenda .sw-dec{width:16px;height:12px;border:1.5px dashed #a07800;background:repeating-linear-gradient(45deg,#fffaf0 0 3px,#e7cf7a 3px 5px)}
.ico-abre{display:inline-block;position:relative;width:17px;height:17px;border:1.6px solid var(--tinta);border-radius:50%;background:#fffdf8}
.ico-abre::before,.ico-abre::after{content:"";position:absolute;left:50%;top:50%;background:var(--tinta);transform:translate(-50%,-50%)}
.ico-abre::before{width:8px;height:1.6px}.ico-abre::after{width:1.6px;height:8px}
.legenda .dica-abre{color:var(--tinta);font-weight:600}
.moldura{position:relative}
.palco{padding:0 16px 12px;overflow-x:auto}
svg.cidade{display:block;width:100%;max-width:1240px;height:auto;margin:0 auto}
.rot{font-size:15px;font-weight:600;fill:var(--tinta)}
.grp{font-size:14px;font-weight:650;letter-spacing:.02em}
.chip{font-size:11.5px;font-weight:700;fill:#5e4600}
.parb{font-size:17px;fill:#3f5163}
.nlin{font-size:13px;font-weight:700;font-style:italic;letter-spacing:.03em}
.n-busca{fill:var(--buscar)}.n-grav{fill:var(--gravar)}
.zona{stroke-width:1.6}
.bairro{cursor:pointer;outline:none}
.bairro:hover .zona,.bairro:focus-visible .zona{stroke:var(--tinta);stroke-width:3.5}
.bairro:hover .abre circle,.bairro:focus-visible .abre circle{fill:var(--tinta)}
.bairro:hover .abre path,.bairro:focus-visible .abre path{stroke:#fff}
.anel{fill:transparent;stroke:transparent;stroke-width:2.5}
.pessoa:hover .anel,.pessoa:focus-visible .anel{fill:#fff2bf;stroke:var(--tinta)}
.pessoa{cursor:pointer;outline:none}
.cabeca,.corpo{fill:var(--tinta);stroke:var(--tinta);stroke-width:1}
.pess{font-weight:700}
.lig{fill:none;stroke-linecap:round;stroke-linejoin:round;stroke-width:6}
.lig.buscar{stroke:var(--buscar);stroke-width:10}
.lig.gravar{stroke:var(--gravar);stroke-width:6}
.lig.trocar{stroke:var(--trocar)}
.lig.vigiar{stroke:var(--vigiar);stroke-width:5}
.lig.editar{stroke:var(--editar);stroke-width:5}
.lig.disc{stroke:var(--disc);stroke-width:4}
.lig.sinc{stroke:var(--sinc);stroke-width:4;stroke-dasharray:1 7}
.est{fill:#fff;stroke-width:4}
.c-busca{stroke:var(--buscar)}.c-grav{stroke:var(--gravar)}.c-vig{stroke:var(--vigiar)}.c-edit{stroke:var(--editar)}
.c-disc{stroke:var(--disc)}.c-sinc{stroke:var(--sinc)}
.encontro{fill:#fff;stroke:var(--tinta);stroke-width:3.5}
.encontro.fantasma{fill:#f3f5f7;stroke:#6d8396;stroke-dasharray:5 4}
.cofre{stroke-width:4.5}
.via{fill:#cfd8e0;stroke:#6d8396;stroke-width:1.5}
.dormente{stroke:#6d8396;stroke-width:3}
.faixa{stroke:#fff;stroke-width:2.5}
.muralha{fill:#fbf8f1;stroke:#b9ad98;stroke-width:6}
.muralha.fantasma{fill:#f2f4f6;stroke:#a9b6c2;stroke-width:3;stroke-dasharray:8 5}
.fantasma-bloco{fill:#e3e8ed;stroke:#b8c3cd;stroke-width:1.2}
.rua{fill:#ece4d4}
.rua-busca{fill:#cfe6e6}
.portao{fill:#fffdf8;stroke:var(--gravar);stroke-width:3}
.torre{fill:#fffdf8;stroke:#c08a2e;stroke-width:2.5}
.torre-fuste{fill:#ead8b5}
.lanterna{fill:#fff3d6;stroke:#c08a2e;stroke-width:4}
.terra{fill:#ede4d3}
.chao{stroke:#9c8f7a;stroke-width:3}
.predio{fill:#fbf8f1;stroke:#b9ad98;stroke-width:4}
.seta-porta{fill:none;stroke:var(--tinta);stroke-width:2.5;stroke-linecap:round;stroke-linejoin:round}
.seta-porta.claro{stroke:var(--gravar)}
#ficha{position:fixed;top:0;right:0;height:100%;width:min(420px,100%);background:var(--cartao);border-left:1px solid var(--linha);
box-shadow:-8px 0 24px rgba(60,40,20,.12);padding:22px 22px 30px;overflow-y:auto;display:none}
#ficha.aberta{display:block}
#ficha h2{font-family:Georgia,serif;font-size:22px;margin:0 0 6px;padding-right:70px}
#ficha .frase{color:var(--suave);margin:0 0 16px;font-size:15px;line-height:1.45}
#ficha ul{list-style:none;margin:0;padding:0}
#ficha li{padding:10px 0;border-top:1px solid var(--linha);font-size:15px;line-height:1.45}
#ficha li b{display:block;font-size:16px}
#ficha h3{font-size:13px;letter-spacing:.06em;text-transform:uppercase;color:var(--suave);margin:20px 0 4px}
#ficha .sel{display:block;width:fit-content;margin-top:5px;background:#fff2bf;border:1px dashed #a07800;color:#5e4600;border-radius:9px;padding:1px 8px;font-size:13px;font-weight:600}
#ficha .sel.nv{background:#eef1f4;border-color:#6d8396;color:#33414f}
#fechar{position:absolute;top:12px;right:12px;border:1px solid var(--linha);background:#fff;border-radius:8px;padding:6px 10px;font:inherit;font-size:14px;cursor:pointer}
.lista-bairros{display:none;padding:0 16px 24px;margin:0;list-style:none}
.lista-bairros button{width:100%;text-align:left;margin:4px 0;padding:10px 12px;border:1px solid var(--linha);border-radius:10px;background:var(--cartao);font:inherit;font-size:15px;color:var(--tinta);cursor:pointer}
.dica{display:none;padding:0 16px;font-size:13px;color:var(--suave);margin:0 0 4px}
@media (max-width:760px){
 header{display:block;padding:12px 16px 4px}h1{font-size:22px}.ideia{max-width:none;overflow-wrap:anywhere}.legenda{padding:0 16px 6px;gap:4px 10px}
 svg.cidade{width:900px;max-width:none}
 .lista-bairros,.dica{display:block}
 .moldura::before,.moldura::after{content:"";position:absolute;top:0;bottom:12px;width:28px;pointer-events:none;z-index:1}
 .moldura::before{left:0;background:linear-gradient(90deg,var(--papel),rgba(246,241,231,0))}
 .moldura::after{right:0;background:linear-gradient(270deg,var(--papel),rgba(246,241,231,0))}
}
'''

JS = r'''
(function(){
var G=__DADOS__;
var f=document.getElementById('ficha'),volta=null;
function el(t,c,x){var e=document.createElement(t);if(c)e.className=c;if(x!=null)e.textContent=x;return e}
function selos(li,ss){ss.forEach(function(s){li.appendChild(el('span','sel'+(s[0]==='não verificado'?' nv':''),s[0]+': '+s[1]))})}
function abrir(id,origem){var g=G[id];if(!g)return;volta=origem||null;
 var c=document.getElementById('ficha-corpo');c.textContent='';
 c.appendChild(el('h2',null,g.nome));c.appendChild(el('p','frase',g.frase));
 c.appendChild(el('h3',null,id==='gente'?'Quem':'Componentes'));
 var ul=el('ul');g.itens.forEach(function(i){var li=el('li');li.appendChild(el('b',null,i[0]));li.appendChild(document.createTextNode(i[1]));selos(li,i[2]);ul.appendChild(li)});c.appendChild(ul);
 if(g.lig.length){c.appendChild(el('h3',null,'Ligações'));var u2=el('ul');g.lig.forEach(function(l){var li=el('li');li.appendChild(el('b',null,l[0]));li.appendChild(document.createTextNode(l[1]));selos(li,l[2]);u2.appendChild(li)});c.appendChild(u2)}
 f.classList.add('aberta');document.getElementById('fechar').focus()}
function fechar(){f.classList.remove('aberta');if(volta)volta.focus()}
document.querySelectorAll('[data-abre]').forEach(function(e){
 e.addEventListener('click',function(){abrir(e.getAttribute('data-abre'),e)});
 e.addEventListener('keydown',function(ev){if(ev.key==='Enter'||ev.key===' '){ev.preventDefault();abrir(e.getAttribute('data-abre'),e)}})});
document.getElementById('fechar').addEventListener('click',fechar);
document.addEventListener('keydown',function(ev){if(ev.key==='Escape'&&f.classList.contains('aberta'))fechar()});
// tela estreita: a faixa abre já centrada no Banco local
function centrar(){var p=document.querySelector('.palco'),b=document.querySelector('[data-item="Banco local"]');
 if(!p||!b||p.scrollWidth<=p.clientWidth+1)return;var rp=p.getBoundingClientRect(),rb=b.getBoundingClientRect();
 p.scrollLeft=Math.max(0,p.scrollLeft+rb.left-rp.left-(rp.width-rb.width)/2)}
if(document.readyState==='complete')centrar();else window.addEventListener('load',centrar);
})();
'''

ICONE_ABRE = '<span class="ico-abre" aria-hidden="true"></span>'
LEGENDA = f'''<ul class="legenda" aria-label="Legenda">
<li><i style="background:var(--buscar);height:8px"></i>buscar</li>
<li><i style="background:var(--gravar)"></i>gravar</li>
<li><i class="sw-sinc"></i>disco e banco</li>
<li><i style="background:var(--trocar)"></i>troca entre pares</li>
<li><i style="background:var(--vigiar)"></i>vigiar</li>
<li><i style="background:var(--editar)"></i>editar (Gustavo)</li>
<li><i style="background:var(--disc)"></i>disciplina e acervo</li>
<li><i class="sw-dec"></i>a decidir</li>
<li class="dica-abre">{ICONE_ABRE}cada bairro abre uma ficha</li>
</ul>'''

def pagina(titulo, ideia, svg_corpo, aria, altura=760):
    dados = {k: dict(nome=v['nome'], frase=v['frase'],
                     itens=[[a, b, [list(s) for s in c]] for a, b, c in v['itens']],
                     lig=[[a, b, [list(s) for s in c]] for a, b, c in v['lig']]) for k, v in G.items()}
    botoes = ''.join(f'<li><button type="button" data-abre="{k}">{esc(G[k]["nome"])}</button></li>' for k in
                     ['portas', 'conteudo', 'nucleo', 'vigilancia', 'disciplina', 'periferia', 'fora', 'gente'])
    return f'''<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(titulo)}</title><style>{CSS}</style></head>
<body>
<header><h1>{esc(titulo)}</h1><p class="ideia">{esc(ideia)}</p></header>
{LEGENDA}
<p class="dica">Arraste o desenho para os lados; os bairros também estão na lista abaixo.</p>
<div class="moldura"><main class="palco">
<svg class="cidade" viewBox="0 0 1200 {altura}" role="img" aria-label="{esc(aria)}">{DEFS}{svg_corpo}</svg>
</main></div>
<ul class="lista-bairros" aria-label="Bairros">{botoes}</ul>
<aside id="ficha" aria-live="polite" aria-label="Ficha do bairro"><button id="fechar" type="button">Fechar</button><div id="ficha-corpo"></div></aside>
<script>{JS.replace("__DADOS__", json.dumps(dados, ensure_ascii=False))}</script>
</body></html>'''

CONCEITOS = [
 ('a', 'Linhas do hub', 'Cada linha é um trajeto do hub; siga uma cor da pessoa até onde ela chega. A linha mais grossa, buscar, termina na entrada do bairro Conteúdo.',
  conceito_a, 'Conceito A: mapa de linhas. Trajetos de buscar, gravar, trocar entre pares, vigiar e editar, com as estações nos sete bairros.', 760),
 ('b', 'Duas cidades e a estrada', 'Planta de duas cidades iguais, ligadas pela estrada da rede privada. Leia por lugar: cada bairro é um quarteirão, e a rua da busca leva ao conteúdo.',
  conceito_b, 'Conceito B: planta da cidade do par A, com portões na muralha, quarteirões por bairro, a estrada da rede privada e o par B com a mesma planta, em miniatura.', 760),
 ('c', 'A cidade em corte', 'Vista de lado: quanto mais fundo, mais perto da verdade. O conteúdo mora no subsolo, junto do cofre.',
  conceito_c, 'Conceito C: corte da cidade. Torre da vigia no alto, disciplina no andar, portas no térreo, conteúdo e núcleo de dados no subsolo, túnel da rede privada até o par B.', 800),
]

for letra, titulo, ideia, fn, aria, alt in CONCEITOS:
    with open(os.path.join(OUT, f'conceito-{letra}.html'), 'w', encoding='utf-8', newline='\n') as fh:
        fh.write(pagina(titulo, ideia, fn(), aria, alt))
print('ok')
