# Gera conceito-a/b/c.html da volta 1. Conteúdo só do texto-do-hub.md.
import json, sys, os
from html import escape as esc

OUT = sys.argv[1]

# ---------------------------------------------------------------- conteúdo (texto do hub, seções 3, 3.5, 4, 7)
G = {
 'nucleo': dict(nome='Núcleo de dados do par', frase='Os três guardam ou movem a mesma verdade dentro da máquina.',
   itens=[('Banco local','Guarda a verdade: cada nota com histórico de versões e as versões em conflito; o texto fica cifrado.',None),
          ('Vista Markdown','Os arquivos no disco por onde o Gustavo vê e edita o hub; gerada a partir do banco, e a edição volta ao banco.',None),
          ('Sincronizador','Liga disco e banco local o tempo todo, nos dois sentidos, sem depender do Obsidian aberto; pega o que qualquer agente grava no disco.',None)],
   lig=[('Vista Markdown → Sincronizador → Banco local','Mudanças de arquivo, nos dois sentidos. Sempre.')]),
 'portas': dict(nome='Portas do par', frase='Por elas os agentes e os clientes alcançam o núcleo. A camada de busca é a porta do conteúdo.',
   itens=[('Camada de busca','Entrega ao agente o trecho certo sem ele ler tudo; é por ela que o agente chega ao conteúdo.','Onde mora, a ferramenta e o modelo de embeddings: a decidir.'),
          ('Porta do banco','Porta do agente ao banco: lê devolvendo a versão, grava levando a versão lida, e vira conflito visível se ela mudou.',None),
          ('Porta de leitura','Segunda porta do par, exposta na rede só para os clientes, com token.',None)],
   lig=[('Agentes → Camada de busca','Pergunta → trecho certo. É o caminho normal até o conteúdo.'),
        ('Agentes → Porta do banco → Banco local','Leitura com versão; gravação com a versão lida.'),
        ('Cliente → Porta de leitura','Consultas por HTTP com token; nunca recebe a credencial do banco.')]),
 'vigilancia': dict(nome='Vigilância', frase='Ligadas à garantia: nada diverge em silêncio.',
   itens=[('Vigia do sync','Confere a cada 5 min as trocas, os conflitos abertos, os binários descartados, os arquivos grandes demais e se o sincronizador está vivo; grava um estado curto e avisa quando piora.',None),
          ('Avisos','Três saídas da vigia: notificação do Windows, o estado curto lido no início de sessão e um mod do Claude Code que mostra o estado o tempo todo.',None),
          ('Checagem de sessão','No começo de toda sessão de agente: lê o estado da vigia, informa a hora da última troca e abre a nota de retomada.',None)],
   lig=[('Vigia do sync → Banco local, Sincronizador, Obsidian','Lê o estado das trocas, a cada 5 min.'),
        ('Vigia do sync → Avisos','Aviso de divergência quando o estado piora.'),
        ('Estado curto e nota de retomada → Checagem de sessão','No início de toda sessão.')]),
 'disciplina': dict(nome='Disciplina do agente', frase='Fazem o agente gravar no lugar certo, sem pedido.',
   itens=[('Contrato','As regras do hub para os agentes (AGENTS.md na raiz), incluindo o lugar de cada informação.',None),
          ('Checkpoint','Ao fim de cada resposta, obriga o agente a manter a nota de retomada em dia e a levar ao hub o que só a memória privada da ferramenta sabe. Hoje garantido só no Claude Code.',None),
          ('Guarda do acervo','Fiscaliza gravações no acervo do maestro: no Claude Code recusa ou pede aval e exige um verificador noutro modelo; Codex e Copilot deixam propostas.','Detalhes da guarda: não verificados.'),
          ('Registro de uso','Anota, por máquina, quem usa cada peça do acervo; gravado por hook.',None)],
   lig=[('Checkpoint → Nota de retomada','O que a resposta mudou. Ao fim de cada resposta.'),
        ('Agentes → Guarda do acervo → Acervo do maestro','Gravação liberada, recusada ou com pedido de aval.'),
        ('Hook de uso → Registro de uso','Quem usou qual peça, por máquina.'),
        ('Contrato → configuração de cada ferramenta','Link para o AGENTS.md; fixo, montado pelo kit de par.')]),
 'conteudo': dict(nome='Conteúdo', frase='As seis raízes, com tudo o que mora dentro delas. Chega-se a ele pela camada de busca.',
   itens=[('Raiz','Seis raízes, cada uma com comportamento próprio: clients, operations, initiatives, reference, agents e inbox. O que termina vai ao _archive da própria raiz.',None),
          ('Iniciativa','Frente de trabalho com identificador, estado e próxima ação; mora numa casa só.',None),
          ('Nota de retomada','Um arquivo curto por trabalho, sobrescrito, com sete campos; qualquer sessão continua de onde a outra parou.',None),
          ('Acervo do maestro','Peças prontas para todo maestro do Maestri (papéis, setups, contratos-opção), como família de skills. Opções, não regras.',None),
          ('Pasta não replicada','Parte do hub numa máquina só, fora do sync e da cópia de segurança.','Mecanismo: a decidir.')],
   lig=[('Maestro → Acervo do maestro','O maestro começa pelo acervo.')]),
 'periferia': dict(nome='Periferia do par', frase='Estão no par, mas não guardam nem movem a verdade do dia a dia.',
   itens=[('Obsidian','Só para ver, editar e resolver conflito; pode ficar fechado. O cofre é a raiz do hub.',None),
          ('Cópia local (git)','Um .git na raiz de cada máquina: só faz commit e push, nunca escreve no disco do hub.',None),
          ('Nó da rede','Põe o par na rede privada entre as máquinas.',None)],
   lig=[('Gustavo → Obsidian → Banco local','Edições do Gustavo e conflitos para resolver. Só com o Obsidian aberto.'),
        ('Cópia local (git) → Cópia no GitHub','Commit e push da vista, uma vez por dia.')]),
 'fora': dict(nome='Fora do par', frase='O outro par fica do outro lado da rede privada, igual a este.',
   itens=[('Rede privada','O único caminho entre pares e entre cliente e par. Nunca exposta à internet.',None),
          ('Par B','O outro par: cópia completa e editável, trabalha sozinho e troca mudanças direto com este. Nenhum é referência.',None),
          ('Cópia no GitHub','Cópia de segurança diária da vista, um ramo por máquina. Não é ponto de encontro do sync.',None),
          ('Cliente','Computador ou sandbox que usa o hub através de um par, sem cópia; só lê por padrão; precisa de um par ligado.',None),
          ('Claude Desktop','Lê pelo MCP, por uma ponte local até a porta do banco.','Se grava: a decidir.'),
          ('Vault (referência)','Só referência: o agente pode ler, o hub não grava nada nele. Só existe no notebook.',None)],
   lig=[('Banco local → Par B','As mudanças do próprio par; contínuo, com os dois ligados, pela rede privada.'),
        ('Claude Desktop → Porta do banco','Leitura, por ponte local.')]),
 'gente': dict(nome='Quem chega ao hub', frase='Gente e agentes ficam fora dos bairros e chegam pelas portas. A porta diz onde a sessão abre; o conteúdo se alcança pela busca.',
   itens=[('Agentes','Claude Code, Codex e Copilot, dentro ou fora do Maestri.',None),
          ('Gustavo','Pelo Obsidian, na vista Markdown.',None),
          ('Maestro','Maestro do Maestri: começa pelo acervo do maestro.',None)],
   lig=[]),
}
PAPEL = {r: p for g in G.values() for (r, p, d) in g['itens']}

COR = {  # fundo, traço, texto do rótulo de bairro
 'nucleo': ('#dcece5', '#3d8a76', '#1d5a4c'),
 'portas': ('#e0e7f4', '#4a6fae', '#2c4f8a'),
 'vigilancia': ('#f6e6c8', '#c08a2e', '#7f4f0c'),
 'disciplina': ('#ece2f1', '#8a62a0', '#5f3a74'),
 'conteudo': ('#f4e7d8', '#b07d4c', '#6f4722'),
 'periferia': ('#e9e7e2', '#8b857b', '#55504a'),
 'fora': ('#e6ecf1', '#6d8396', '#3f5163'),
}

# ---------------------------------------------------------------- peças de SVG
def t(x, y, s, cls='rot', anchor='start', extra=''):
    return f'<text x="{x}" y="{y}" class="{cls}" text-anchor="{anchor}"{extra}>{esc(s)}</text>'

def zona(gid, shape, label_xy, anchor='start', inner=''):
    f, s, c = COR[gid]
    nome = G[gid]['nome']
    lx, ly = label_xy
    return (f'<g class="bairro" data-grupo="{esc(nome)}" data-abre="{gid}" tabindex="0" role="button" '
            f'aria-label="Abrir a ficha: {esc(nome)}">'
            f'{shape.replace("/>", f" class=\"zona\" fill=\"{f}\" stroke=\"{s}\"/>", 1)}'
            f'<text x="{lx}" y="{ly}" class="grp" text-anchor="{anchor}" fill="{c}">{esc(nome)}</text>'
            f'{inner}</g>')

def item(rotulo, corpo, extra_cls=''):
    return (f'<g class="item {extra_cls}" data-item="{esc(rotulo)}"><title>{esc(rotulo)}: {esc(PAPEL.get(rotulo, ""))}</title>'
            f'{corpo}</g>')

def chip(x, y):  # "a decidir": sempre o mesmo selo
    return (f'<g class="decidir"><rect x="{x}" y="{y}" width="70" height="19" rx="9.5" fill="#fff2bf" stroke="#a07800"/>'
            f'<text x="{x+35}" y="{y+13.5}" class="chip" text-anchor="middle">a decidir</text></g>')

def pessoa(rotulo, x, y, lpos='below'):
    corpo = (f'<circle cx="{x}" cy="{y-15}" r="7" class="cabeca"/>'
             f'<path d="M{x-11},{y+8} Q{x-11},{y-6} {x},{y-6} Q{x+11},{y-6} {x+11},{y+8} Z" class="corpo"/>')
    if lpos == 'below':
        corpo += t(x, y + 28, rotulo, 'rot pess', 'middle')
    elif lpos == 'above':
        corpo += t(x, y - 30, rotulo, 'rot pess', 'middle')
    elif lpos == 'right':
        corpo += t(x + 18, y + 2, rotulo, 'rot pess', 'start')
    else:
        corpo += t(x - 18, y + 2, rotulo, 'rot pess', 'end')
    return (f'<g class="item pessoa" data-item="{rotulo}" data-abre="gente" tabindex="0" role="button" '
            f'aria-label="Abrir a ficha: quem chega ao hub ({rotulo})"><title>{rotulo}: {esc(PAPEL[rotulo])}</title>{corpo}</g>')

def lig(de_para, d, cls):
    return f'<path data-ligacao="{esc(de_para)}" class="lig {cls}" d="{d}"/>'

DEFS = '''<defs>
<pattern id="hachura" width="7" height="7" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
<rect width="7" height="7" fill="#fffaf0"/><line x1="0" y1="0" x2="0" y2="7" stroke="#c9a640" stroke-width="2.4"/></pattern>
</defs>'''

# ---------------------------------------------------------------- Conceito A: linhas de metrô
def est(x, y, cls, r=9, decidir=False):
    if decidir:
        return f'<circle cx="{x}" cy="{y}" r="{r+4}" fill="url(#hachura)" stroke="#a07800" stroke-dasharray="4 3" stroke-width="2"/><circle cx="{x}" cy="{y}" r="{r-3}" class="est {cls}"/>'
    return f'<circle cx="{x}" cy="{y}" r="{r}" class="est {cls}"/>'

def conceito_a():
    z = []
    z.append(zona('disciplina', '<rect x="40" y="60" width="200" height="140" rx="22"/>', (58, 86),
        inner=item('Checkpoint', est(150, 145, 'c-disc') + t(150, 178, 'Checkpoint', anchor='middle'))))
    z.append(zona('conteudo', '<rect x="280" y="40" width="330" height="200" rx="22"/>', (298, 66),
        inner=item('Nota de retomada', est(370, 145, 'c-disc') + t(370, 178, 'Nota de retomada', anchor='middle')) +
              item('Acervo do maestro', est(530, 145, 'c-disc') + t(530, 178, 'Acervo do maestro', anchor='middle'))))
    z.append(zona('portas', '<rect x="280" y="282" width="330" height="240" rx="22"/>', (298, 308),
        inner=item('Camada de busca', est(440, 340, 'c-busca', r=13, decidir=True) + t(464, 338, 'Camada de busca') + chip(464, 348)) +
              item('Porta do banco', est(440, 460, 'c-grav') + t(440, 492, 'Porta do banco', anchor='middle'))))
    z.append(zona('vigilancia', '<rect x="630" y="190" width="270" height="150" rx="22"/>', (648, 216),
        inner=item('Vigia do sync', est(710, 270, 'c-vig') + t(732, 275, 'Vigia do sync'))))
    z.append(zona('nucleo', '<rect x="630" y="392" width="270" height="250" rx="22"/>', (648, 628),
        inner=item('Banco local', '<rect data-encontro="Banco local" x="650" y="438" width="120" height="44" rx="22" class="encontro"/>' + t(710, 466, 'Banco local', anchor='middle')) +
              item('Sincronizador', est(740, 530, 'c-sinc', r=8) + t(760, 535, 'Sincronizador')) +
              item('Vista Markdown', est(740, 600, 'c-sinc', r=8) + t(760, 605, 'Vista Markdown'))))
    z.append(zona('periferia', '<rect x="400" y="560" width="200" height="105" rx="22"/>', (418, 586),
        inner=item('Obsidian', est(540, 625, 'c-edit') + t(522, 630, 'Obsidian', anchor='end'))))
    z.append(zona('fora', '<rect x="940" y="340" width="245" height="250" rx="22" stroke-dasharray="7 5"/>', (958, 366),
        inner=item('Rede privada', '<rect x="985" y="392" width="56" height="140" rx="10" class="via"/>' + t(1013, 556, 'Rede privada', anchor='middle')) +
              item('Par B', '<rect x="1080" y="438" width="92" height="44" rx="22" class="encontro fantasma"/>' + t(1126, 466, 'Par B', anchor='middle'))))
    gente = pessoa('Agentes', 110, 400, 'left') + pessoa('Gustavo', 540, 722, 'right') + pessoa('Maestro', 760, 90, 'right')
    L = [
        lig('Agentes → Camada de busca', 'M124,384 L188,340 H424', 'buscar'),
        lig('Agentes → Porta do banco', 'M124,404 L180,460 H428', 'gravar'),
        lig('Porta do banco → Banco local', 'M452,460 H650', 'gravar'),
        lig('Sincronizador → Banco local', 'M740,522 V482', 'sinc'),
        lig('Vista Markdown → Sincronizador', 'M740,592 V538', 'sinc'),
        lig('Vigia do sync → Banco local', 'M710,282 V438', 'vigiar'),
        lig('Banco local → Par B', 'M770,460 H1080', 'trocar'),
        lig('Gustavo → Obsidian', 'M540,700 V636', 'editar'),
        lig('Obsidian → Banco local', 'M549,616 L660,482', 'editar'),
        lig('Checkpoint → Nota de retomada', 'M159,145 H361', 'disc'),
        lig('Maestro → Acervo do maestro', 'M748,90 H590 L539,141', 'disc'),
    ]
    return ''.join(z) + ''.join(L) + gente

# ---------------------------------------------------------------- Conceito B: duas cidades e a estrada
def predio(x, y, w, h, gid, decidir=False):
    f, s, c = COR[gid]
    if decidir:
        return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="4" fill="url(#hachura)" stroke="#a07800" stroke-dasharray="4 3" stroke-width="2"/>'
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="4" fill="#fffdf8" stroke="{s}" stroke-width="2.5"/>'

def casas(x0, y0, gid):
    f, s, c = COR[gid]
    out = ''
    for i in range(3):
        for j in range(2):
            x, y = x0 + i * 36, y0 + j * 34
            out += f'<path d="M{x},{y+12} L{x+12},{y} L{x+24},{y+12} V{y+26} H{x} Z" fill="#fffdf8" stroke="{s}" stroke-width="2"/>'
    return out

def conceito_b():
    muralha = ('<rect x="190" y="40" width="545" height="690" rx="26" class="muralha"/>'
               # ruas (só desenho): a rua da busca leva ao conteúdo
               ''
               '<rect x="200" y="551" width="510" height="18" class="rua"/>')
    z = []
    z.append(zona('portas', '<rect x="160" y="150" width="200" height="370" rx="18"/>', (176, 176),
        inner=item('Camada de busca', '<rect x="176" y="222" width="28" height="56" rx="6" fill="url(#hachura)" stroke="#a07800" stroke-dasharray="4 3" stroke-width="2"/>' + t(176, 212, 'Camada de busca') + chip(176, 288)) +
              item('Porta do banco', '<rect x="178" y="465" width="24" height="44" rx="6" class="portao"/>' + t(216, 470, 'Porta do banco'))))
    # a rua da busca: do portão da busca ao conteúdo (desenho, não ligação)
    z.append('<rect x="205" y="243" width="195" height="14" class="rua rua-busca"/>')
    z.append(zona('conteudo', '<rect x="400" y="60" width="300" height="220" rx="16"/>', (416, 86),
        inner=item('Raiz', casas(424, 118, 'conteudo') + t(460, 210, 'Raiz', anchor='middle')) +
              item('Acervo do maestro', predio(596, 128, 48, 50, 'conteudo') + t(620, 210, 'Acervo do maestro', anchor='middle'))))
    z.append(zona('nucleo', '<rect x="395" y="320" width="210" height="220" rx="16"/>', (411, 346),
        inner=item('Vista Markdown', predio(412, 367, 18, 16, 'nucleo') + t(438, 381, 'Vista Markdown')) +
              item('Sincronizador', predio(412, 417, 18, 16, 'nucleo') + t(438, 431, 'Sincronizador')) +
              item('Banco local', '<rect data-encontro="Banco local" x="412" y="463" width="150" height="48" rx="12" class="encontro cofre"/>' + t(487, 492, 'Banco local', anchor='middle'))))
    z.append(zona('vigilancia', '<rect x="620" y="320" width="98" height="220" rx="16"/>', (632, 346),
        inner=item('Vigia do sync', '<rect x="659" y="390" width="16" height="64" class="torre"/><path d="M651,390 L667,372 L683,390 Z" class="torre"/>' + t(669, 524, 'Vigia do sync', anchor='middle', extra=' textLength="88" lengthAdjust="spacingAndGlyphs"'))))
    z.append(zona('disciplina', '<rect x="220" y="590" width="220" height="125" rx="16"/>', (236, 616),
        inner=item('Contrato', predio(240, 640, 40, 46, 'disciplina') + t(294, 668, 'Contrato'))))
    z.append(zona('periferia', '<rect x="460" y="590" width="250" height="125" rx="16"/>', (700, 616), anchor='end',
        inner=item('Obsidian', predio(478, 640, 54, 30, 'periferia') + t(546, 661, 'Obsidian'))))
    # fora do par: a estrada e o outro par, igual a este, visto de longe
    fant = ''.join(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" class="fantasma-bloco"/>' for x, y, w, h in
                   [(930, 330, 70, 100), (1020, 300, 120, 90), (1020, 410, 80, 100), (1110, 410, 40, 100), (930, 530, 100, 60), (1050, 530, 100, 60)])
    z.append(zona('fora', '<rect x="760" y="20" width="425" height="720" rx="22" stroke-dasharray="7 5"/>', (1170, 46), anchor='end',
        inner=item('Rede privada', '<rect x="780" y="40" width="60" height="680" rx="12" class="via"/>' + t(810, 300, 'Rede privada', anchor='middle', extra=' transform="rotate(-90 810 300)"')) +
              '<rect x="900" y="250" width="270" height="380" rx="22" class="muralha fantasma"/>' + fant +
              item('Par B', '<rect x="940" y="545" width="70" height="30" rx="10" class="encontro fantasma"/>' + t(920, 282, 'Par B', cls='rot parb'))))
    gente = pessoa('Maestro', 70, 95, 'above') + pessoa('Agentes', 70, 340, 'above') + pessoa('Gustavo', 70, 640, 'above')
    L = [
        lig('Agentes → Camada de busca', 'M86,326 L162,250 H176', 'buscar'),
        lig('Agentes → Porta do banco', 'M86,352 L170,487 H178', 'gravar'),
        lig('Porta do banco → Banco local', 'M202,487 H412', 'gravar'),
        lig('Vista Markdown → Sincronizador', 'M421,383 V417', 'sinc'),
        lig('Sincronizador → Banco local', 'M421,433 V463', 'sinc'),
        lig('Vigia do sync → Banco local', 'M667,454 V487 H562', 'vigiar'),
        lig('Banco local → Par B', 'M548,511 V560 H940', 'trocar'),
        lig('Gustavo → Obsidian', 'M86,636 L126,560 H492 V640', 'editar'),
        lig('Obsidian → Banco local', 'M522,640 V511', 'editar'),
        lig('Maestro → Acervo do maestro', 'M86,90 H140 L172,22 H620 V128', 'disc'),
    ]
    return muralha + ''.join(z) + ''.join(L) + gente

# ---------------------------------------------------------------- Conceito C: a cidade em corte
def sala(x, y, gid, w=24, h=24):
    f, s, c = COR[gid]
    return f'<rect x="{x-w/2}" y="{y-h/2}" width="{w}" height="{h}" rx="5" fill="#fffdf8" stroke="{s}" stroke-width="2.5"/>'

def conceito_c():
    fundo = ('<rect x="0" y="470" width="1200" height="290" class="terra"/>'
             '<line x1="0" y1="470" x2="1200" y2="470" class="chao"/>'
             '<rect x="300" y="90" width="460" height="380" class="predio"/>'
             '<rect x="809" y="100" width="12" height="370" class="torre-fuste"/>')
    z = []
    z.append(zona('vigilancia', '<rect x="775" y="20" width="235" height="120" rx="18"/>', (793, 46),
        inner=item('Vigia do sync', '<circle cx="815" cy="88" r="13" class="lanterna"/>' + t(838, 93, 'Vigia do sync'))))
    z.append(zona('conteudo', '<rect x="300" y="90" width="460" height="140" rx="0"/>', (744, 116), anchor='end',
        inner=item('Acervo do maestro', sala(340, 170, 'conteudo') + t(360, 175, 'Acervo do maestro')) +
              item('Nota de retomada', sala(560, 170, 'conteudo') + t(580, 175, 'Nota de retomada'))))
    z.append(zona('disciplina', '<rect x="300" y="258" width="460" height="104" rx="0"/>', (744, 284), anchor='end',
        inner=item('Checkpoint', sala(560, 316, 'disciplina') + t(580, 321, 'Checkpoint'))))
    z.append(zona('portas', '<rect x="300" y="390" width="460" height="145" rx="0"/>', (744, 414), anchor='end',
        inner=item('Camada de busca', '<path d="M362,470 V436 Q362,418 380,418 Q398,418 398,436 V470 Z" fill="url(#hachura)" stroke="#a07800" stroke-dasharray="4 3" stroke-width="2"/><path d="M372,444 L380,434 L388,444" class="seta-porta"/>' + t(408, 440, 'Camada de busca') + chip(408, 449)) +
              item('Porta do banco', '<rect x="584" y="488" width="32" height="24" rx="4" class="portao"/><path d="M592,496 L600,505 L608,496" class="seta-porta claro"/>' + t(626, 506, 'Porta do banco'))))
    z.append(zona('nucleo', '<rect x="300" y="565" width="470" height="180" rx="0"/>', (316, 734),
        inner=item('Vista Markdown', sala(380, 610, 'nucleo', 20, 20) + t(400, 615, 'Vista Markdown')) +
              item('Sincronizador', sala(380, 680, 'nucleo', 20, 20) + t(380, 711, 'Sincronizador', anchor='middle')) +
              item('Banco local', '<rect data-encontro="Banco local" x="540" y="660" width="160" height="46" rx="10" class="encontro cofre"/>' + t(620, 689, 'Banco local', anchor='middle'))))
    z.append(zona('periferia', '<rect x="890" y="340" width="150" height="150" rx="18"/>', (906, 364),
        inner=item('Obsidian', '<path d="M920,470 V420 L965,396 L1010,420 V470 Z" fill="#fffdf8" stroke="#8b857b" stroke-width="2.5"/>' + t(965, 448, 'Obsidian', anchor='middle'))))
    z.append(zona('fora', '<rect x="800" y="630" width="390" height="120" rx="18" stroke-dasharray="7 5"/>', (818, 654),
        inner=item('Rede privada', '<rect x="812" y="668" width="250" height="34" rx="17" class="via"/>' + t(937, 730, 'Rede privada', anchor='middle')) +
              item('Par B', '<rect x="1095" y="662" width="86" height="46" rx="10" class="encontro fantasma"/>' + t(1138, 690, 'Par B', anchor='middle'))))
    gente = pessoa('Agentes', 200, 450, 'above') + pessoa('Gustavo', 1145, 450, 'above') + pessoa('Maestro', 340, 44, 'right')
    L = [
        lig('Agentes → Camada de busca', 'M214,442 H362', 'buscar'),
        lig('Agentes → Porta do banco', 'M214,458 L256,500 H584', 'gravar'),
        lig('Porta do banco → Banco local', 'M600,512 V660', 'gravar'),
        lig('Vista Markdown → Sincronizador', 'M380,620 V670', 'sinc'),
        lig('Sincronizador → Banco local', 'M390,680 H540', 'sinc'),
        lig('Vigia do sync → Banco local', 'M815,101 V580 H660 V660', 'vigiar'),
        lig('Banco local → Par B', 'M700,685 H1095', 'trocar'),
        lig('Gustavo → Obsidian', 'M1131,444 H1010', 'editar'),
        lig('Obsidian → Banco local', 'M965,470 V612 H686 V660', 'editar'),
        lig('Checkpoint → Nota de retomada', 'M560,304 V182', 'disc'),
        lig('Maestro → Acervo do maestro', 'M340,62 V158', 'disc'),
    ]
    return fundo + ''.join(z) + ''.join(L) + gente

# ---------------------------------------------------------------- página
CSS = r'''
:root{--papel:#f6f1e7;--tinta:#2b2622;--suave:#5f574e;--linha:#d9cfbf;--cartao:#fffcf6;
--buscar:#0b7480;--gravar:#2c4f8a;--trocar:#8e3b5b;--vigiar:#a1620c;--editar:#3d7429;--disc:#6b5f53;--sinc:#4a6fae}
*{box-sizing:border-box}
html,body{margin:0;background:var(--papel);color:var(--tinta);font-family:"Segoe UI",system-ui,-apple-system,Roboto,sans-serif}
header{padding:14px 24px 6px;display:flex;flex-wrap:wrap;gap:6px 22px;align-items:baseline}
h1{font-family:Georgia,"Times New Roman",serif;font-size:26px;margin:0;font-weight:700}
.ideia{margin:0;color:var(--suave);font-size:15px;max-width:62ch}
.legenda{display:flex;flex-wrap:wrap;gap:4px 14px;padding:0 24px 6px;font-size:13px;color:var(--suave);list-style:none;margin:0}
.legenda li{display:flex;align-items:center;gap:6px}
.legenda i{display:inline-block;width:22px;height:5px;border-radius:3px}
.legenda .sw-dec{width:16px;height:12px;border:1.5px dashed #a07800;background:repeating-linear-gradient(45deg,#fffaf0 0 3px,#e7cf7a 3px 5px)}
.palco{padding:0 16px 12px;overflow-x:auto}
svg.cidade{display:block;width:100%;max-width:1240px;height:auto;margin:0 auto}
.rot{font-size:15px;font-weight:600;fill:var(--tinta)}
.grp{font-size:12px;font-weight:700;letter-spacing:.08em;text-transform:uppercase}
.chip{font-size:11.5px;font-weight:700;fill:#5e4600}
.parb{font-size:17px;fill:#3f5163}
.zona{stroke-width:1.6}
.bairro{cursor:pointer;outline:none}
.bairro:hover .zona{stroke-width:3}
.bairro:focus-visible .zona,.pessoa:focus-visible .corpo{stroke:var(--tinta);stroke-width:3.5}
.pessoa{cursor:pointer;outline:none}
.cabeca,.corpo{fill:var(--tinta);stroke:var(--tinta);stroke-width:1}
.pess{font-weight:700}
.lig{fill:none;stroke-linecap:round;stroke-linejoin:round;stroke-width:6}
.lig.buscar{stroke:var(--buscar);stroke-width:10}
.lig.gravar{stroke:var(--gravar)}
.lig.trocar{stroke:var(--trocar)}
.lig.vigiar{stroke:var(--vigiar);stroke-width:5}
.lig.editar{stroke:var(--editar);stroke-width:5}
.lig.disc{stroke:var(--disc);stroke-width:4}
.lig.sinc{stroke:var(--sinc);stroke-width:4}
.est{fill:#fff;stroke-width:4}
.c-busca{stroke:var(--buscar)}.c-grav{stroke:var(--gravar)}.c-vig{stroke:var(--vigiar)}.c-edit{stroke:var(--editar)}
.c-disc{stroke:var(--disc)}.c-sinc{stroke:var(--sinc)}
.encontro{fill:#fff;stroke:var(--tinta);stroke-width:3.5}
.encontro.fantasma{fill:#f3f5f7;stroke:#6d8396;stroke-dasharray:5 4}
.cofre{stroke-width:4.5}
.via{fill:#cfd8e0;stroke:#6d8396;stroke-width:1.5}
.muralha{fill:#fbf8f1;stroke:#b9ad98;stroke-width:6}
.muralha.fantasma{fill:#f2f4f6;stroke:#a9b6c2;stroke-width:4;stroke-dasharray:10 6}
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
#ficha{position:fixed;top:0;right:0;height:100%;width:min(400px,100%);background:var(--cartao);border-left:1px solid var(--linha);
box-shadow:-8px 0 24px rgba(60,40,20,.12);padding:22px 22px 30px;overflow-y:auto;display:none}
#ficha.aberta{display:block}
#ficha h2{font-family:Georgia,serif;font-size:22px;margin:0 0 6px}
#ficha .frase{color:var(--suave);margin:0 0 16px;font-size:15px;line-height:1.45}
#ficha ul{list-style:none;margin:0;padding:0}
#ficha li{padding:10px 0;border-top:1px solid var(--linha);font-size:15px;line-height:1.45}
#ficha li b{display:block;font-size:16px}
#ficha h3{font-size:13px;letter-spacing:.08em;text-transform:uppercase;color:var(--suave);margin:20px 0 4px}
#ficha .sel{display:inline-block;margin-top:4px;background:#fff2bf;border:1px dashed #a07800;color:#5e4600;border-radius:9px;padding:1px 8px;font-size:13px;font-weight:600}
#fechar{position:absolute;top:12px;right:12px;border:1px solid var(--linha);background:#fff;border-radius:8px;padding:6px 10px;font:inherit;font-size:14px;cursor:pointer}
.lista-bairros{display:none;padding:0 16px 24px;margin:0;list-style:none}
.lista-bairros button{width:100%;text-align:left;margin:4px 0;padding:10px 12px;border:1px solid var(--linha);border-radius:10px;background:var(--cartao);font:inherit;font-size:15px;color:var(--tinta);cursor:pointer}
.dica{display:none;padding:0 16px;font-size:13px;color:var(--suave);margin:0 0 4px}
@media (max-width:760px){
 header{display:block;padding:12px 16px 4px}h1{font-size:22px}.ideia{max-width:none;overflow-wrap:anywhere}.legenda{padding:0 16px 6px;gap:4px 10px}
 svg.cidade{width:900px;max-width:none}
 .lista-bairros,.dica{display:block}
}
'''

JS = r'''
(function(){
var G=__DADOS__;
var f=document.getElementById('ficha'),volta=null;
function el(t,c,x){var e=document.createElement(t);if(c)e.className=c;if(x!=null)e.textContent=x;return e}
function abrir(id,origem){var g=G[id];if(!g)return;volta=origem||null;
 var c=document.getElementById('ficha-corpo');c.textContent='';
 c.appendChild(el('h2',null,g.nome));c.appendChild(el('p','frase',g.frase));
 c.appendChild(el('h3',null,id==='gente'?'Quem':'Componentes'));
 var ul=el('ul');g.itens.forEach(function(i){var li=el('li');li.appendChild(el('b',null,i[0]));li.appendChild(document.createTextNode(i[1]));
  if(i[2]){li.appendChild(document.createElement('br'));li.appendChild(el('span','sel','a decidir: '+i[2].replace(/: a decidir\.$/,'').replace(/^a decidir: /,'')))}ul.appendChild(li)});c.appendChild(ul);
 if(g.lig.length){c.appendChild(el('h3',null,'Ligações'));var u2=el('ul');g.lig.forEach(function(l){var li=el('li');li.appendChild(el('b',null,l[0]));li.appendChild(document.createTextNode(l[1]));u2.appendChild(li)});c.appendChild(u2)}
 f.classList.add('aberta');document.getElementById('fechar').focus()}
function fechar(){f.classList.remove('aberta');if(volta)volta.focus()}
document.querySelectorAll('[data-abre]').forEach(function(e){
 e.addEventListener('click',function(){abrir(e.getAttribute('data-abre'),e)});
 e.addEventListener('keydown',function(ev){if(ev.key==='Enter'||ev.key===' '){ev.preventDefault();abrir(e.getAttribute('data-abre'),e)}})});
document.getElementById('fechar').addEventListener('click',fechar);
document.addEventListener('keydown',function(ev){if(ev.key==='Escape'&&f.classList.contains('aberta'))fechar()});
})();
'''

LEGENDA = '''<ul class="legenda" aria-label="Legenda">
<li><i style="background:var(--buscar);height:8px"></i>buscar</li>
<li><i style="background:var(--gravar)"></i>gravar</li>
<li><i style="background:var(--sinc)"></i>disco e banco</li>
<li><i style="background:var(--trocar)"></i>troca entre pares</li>
<li><i style="background:var(--vigiar)"></i>vigiar</li>
<li><i style="background:var(--editar)"></i>editar (Gustavo)</li>
<li><i style="background:var(--disc)"></i>disciplina e acervo</li>
<li><i class="sw-dec"></i>a decidir</li>
<li>Clique num bairro para abrir a ficha.</li>
</ul>'''

def pagina(letra, titulo, ideia, svg_corpo, aria):
    dados = {k: dict(nome=v['nome'], frase=v['frase'], itens=[[a, b, c] for a, b, c in v['itens']], lig=[[a, b] for a, b in v['lig']]) for k, v in G.items()}
    botoes = ''.join(f'<li><button type="button" data-abre="{k}">{esc(G[k]["nome"])}</button></li>' for k in
                     ['portas', 'conteudo', 'nucleo', 'vigilancia', 'disciplina', 'periferia', 'fora', 'gente'])
    return f'''<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(titulo)}</title><style>{CSS}</style></head>
<body>
<header><h1>{esc(titulo)}</h1><p class="ideia">{esc(ideia)}</p></header>
{LEGENDA}
<p class="dica">Arraste o desenho para os lados; os bairros também estão na lista abaixo.</p>
<main class="palco">
<svg class="cidade" viewBox="0 0 1200 760" role="img" aria-label="{esc(aria)}">{DEFS}{svg_corpo}</svg>
</main>
<ul class="lista-bairros" aria-label="Bairros">{botoes}</ul>
<aside id="ficha" aria-live="polite" aria-label="Ficha do bairro"><button id="fechar" type="button">Fechar</button><div id="ficha-corpo"></div></aside>
<script>{JS.replace("__DADOS__", json.dumps(dados, ensure_ascii=False))}</script>
</body></html>'''

CONCEITOS = [
 ('a', 'Linhas do hub', 'Cada linha é um trajeto do hub; siga uma cor da pessoa até onde ela chega. A linha mais grossa, buscar, termina na porta do conteúdo.',
  conceito_a, 'Conceito A: mapa de linhas. Trajetos de buscar, gravar, trocar entre pares, vigiar e editar, com as estações nos sete bairros.'),
 ('b', 'Duas cidades e a estrada', 'Planta de duas cidades iguais, uma de cada lado da rede privada. Leia por lugar: cada bairro é um quarteirão, e a rua da busca leva ao conteúdo.',
  conceito_b, 'Conceito B: planta da cidade do par A, com portões na muralha, quarteirões por bairro, a estrada da rede privada e o par B igual do outro lado.'),
 ('c', 'A cidade em corte', 'A cidade vista de lado: a gente chega pela rua, as portas ficam no térreo, o conteúdo nos andares e a verdade no subsolo. Leia de cima para baixo.',
  conceito_c, 'Conceito C: corte da cidade. Torre da vigia no alto, conteúdo e disciplina nos andares, portas no térreo, núcleo de dados no subsolo e túnel da rede privada até o par B.'),
]

for letra, titulo, ideia, fn, aria in CONCEITOS:
    with open(os.path.join(OUT, f'conceito-{letra}.html'), 'w', encoding='utf-8', newline='\n') as fh:
        fh.write(pagina(letra, titulo, ideia, fn(), aria))
print('ok')
