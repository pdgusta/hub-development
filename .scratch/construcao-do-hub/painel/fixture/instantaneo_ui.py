"""Fixture instantânea do UI engineer: uma execução parada num momento, no formato do contrato.md.

Não substitui o gerador do QA (fixture/gerar.py, com o tempo andando). Serve para construir e capturar a tela.
Grava em fixture/instantaneo-ui/ (apaga e recria) e em fixture/embutida.js (para abrir web/index.html direto do disco).
O "agora" da fixture é a hora em que roda; a execução começou 140 min antes.

Uso:  python -I fixture/instantaneo_ui.py [--pasta OUTRA]
"""
import argparse
import json
import os
import random
import shutil
from datetime import datetime, timedelta

AQUI = os.path.dirname(os.path.abspath(__file__))
random.seed(16)
AGORA = datetime.now().astimezone().replace(microsecond=0)
T0 = AGORA - timedelta(minutes=140)


def iso(m):
    return (T0 + timedelta(minutes=m)).isoformat()


AGENTES = [('maestro', 'maestro', 'Maestro')] + \
    [('construtor-%d' % i, 'construtor', 'Construtor %d' % i) for i in range(1, 6)] + \
    [('revisor-%d' % i, 'revisor', 'Revisor %d' % i) for i in (1, 2)] + \
    [('testador-%d' % i, 'testador', 'Testador %d' % i) for i in (1, 2)] + \
    [('integrador-1', 'integrador', 'Integrador')] + \
    [('prumo-%d' % i, 'prumo', 'Prumo %d' % i) for i in (1, 2)]

# número, título, Status, Dono (papel), Com, Blocked by
TICKETS = [
    ('01', 'Kit de par: script de instalação', 'resolved', 'construtor', '', ''),
    ('02', 'Compose do CouchDB com o MCP', 'resolved', 'construtor', '', '01'),
    ('03', 'Replicação entre dois CouchDB', 'resolved', 'construtor', '', '02'),
    ('04', 'Setup URI do LiveSync', 'resolved', 'construtor', '', '02'),
    ('05', 'Marcador na raiz do hub', 'resolved', 'construtor', '', ''),
    ('06', 'Conferir que não há CLAUDE.md acima do hub', 'resolved', 'construtor', '', '05'),
    ('07', 'Teste do LiveSync com dois CouchDB', 'testing', 'construtor', 'testador-1', '03, 04'),
    ('08', 'Links simbólicos do contrato', 'resolved', 'construtor', '', '05'),
    ('09', 'Import no CLAUDE.md global', 'review', 'construtor', 'revisor-1', '08'),
    ('10', 'Junctions de skills', 'resolved', 'construtor', '', '08'),
    ('11', 'Modo de desenvolvedor do Windows', 'review', 'construtor', 'revisor-2', ''),
    ('12', 'Kit de cliente: chave efêmera com tag', 'testing', 'construtor', 'testador-2', '01'),
    ('13', 'MCP só de leitura por par', 'review', 'construtor', 'prumo-1', '02'),
    ('14', 'Grant que limita os clientes ao MCP de leitura', 'claimed', 'construtor', 'construtor-1', '13'),
    ('15', 'Linha de MCP no harness do cliente', 'claimed', 'construtor', 'construtor-2', '12'),
    ('16', 'Sincronizador grava a nota de retomada', 'claimed', 'construtor', 'construtor-3', '03'),
    ('17', 'Busca no vault pelo MCP', 'claimed', 'construtor', 'construtor-4', '02'),
    ('18', 'Projeto do Codex com marcador de raiz', 'claimed', 'construtor', 'construtor-5', '05'),
    ('19', 'Ligar o segundo par', 'ready-for-human', 'construtor', '', '01'),
    ('20', 'Kit de par dentro do WSL', 'wontfix', 'construtor', '', ''),
    ('21', 'Replicação com o segundo par', 'open', 'construtor', '', '19'),
    ('22', 'Teste ponta a ponta do cliente', 'open', 'testador', '', '17, 18'),
    ('23', 'Guia de instalação do par', 'open', 'construtor', '', '21'),
    ('24', 'Saúde da replicação no portal', 'open', 'construtor', '', '16'),
    ('25', 'Limpeza dos kits antigos', 'open', 'integrador', '', ''),
]

ev = {a[0]: [] for a in AGENTES}


def e(ag, m, tipo, **k):
    linha = {'t': iso(m), 'agente': ag, 'tipo': tipo}
    linha.update({x: y for x, y in k.items() if y is not None})
    ev[ag].append((m, linha))


def tentativa(ag, tk, de, ate, fim='passou', para=None, subs=0, testes=1, falha=False):
    """Uma tentativa num ticket: pega, abre e fecha subagentes, testa, faz commit e passa/resolve."""
    e(ag, de, 'pegou_ticket', ticket=tk)
    for i in range(subs):
        a = de + 2 + i * (ate - de - 4) / max(subs, 1)
        s = '%s-%s-s%d' % (ag, tk, i + 1)
        e(ag, a, 'abriu_subagente', sub=s, assunto='Explorar %s, parte %d' % (dict((t[0], t[1]) for t in TICKETS)[tk].lower(), i + 1), modelo='claude-opus-5-5')
        e(ag, min(ate - 1, a + random.uniform(3, 12)), 'fechou_subagente', sub=s, ok=True)
    for i in range(testes):
        e(ag, ate - 2 - i, 'rodou_teste', ok=not (falha and i == 0), assunto='python -m pytest testes/',
          detalhe='12 passaram' if not falha else '3 falharam')
    if fim == 'passou':
        e(ag, ate - 0.5, 'commit', ok=True, assunto='ticket %s: pronto para a próxima etapa' % tk)
        e(ag, ate, 'passou_ticket', ticket=tk, para=para)
    elif fim == 'resolveu':
        e(ag, ate, 'resolveu_ticket', ticket=tk)


for a in AGENTES:
    e(a[0], 0.2 + AGENTES.index(a) * .1, 'inicio', modelo='claude-opus-5-5')

# o começo: construtores fazem a primeira leva
tentativa('construtor-1', '01', 1, 30, para='revisor', subs=3)
tentativa('construtor-2', '05', 1, 22, para='revisor', subs=2)
tentativa('construtor-3', '02', 31, 62, para='revisor', subs=4)
tentativa('construtor-4', '08', 23, 48, para='revisor', subs=2)
tentativa('construtor-5', '11', 2, 40, para='revisor', subs=1)
tentativa('revisor-1', '01', 31, 40, para='testador')
tentativa('revisor-2', '05', 23, 30, para='testador')
tentativa('testador-1', '01', 41, 52, fim='resolveu', testes=2)
tentativa('testador-2', '05', 31, 38, fim='resolveu', testes=2)
tentativa('construtor-2', '06', 39, 58, para='revisor', subs=2)
tentativa('construtor-1', '04', 63, 80, para='revisor', subs=3)
tentativa('construtor-2', '03', 59, 88, para='revisor', subs=3)
tentativa('construtor-4', '10', 49, 70, para='revisor', subs=2)
tentativa('construtor-1', '12', 31, 60, para='revisor', subs=2)
tentativa('revisor-1', '02', 63, 72, para='testador')
tentativa('revisor-2', '08', 49, 58, para='testador')
tentativa('revisor-1', '06', 73, 80, para='testador')
tentativa('revisor-2', '10', 71, 78, para='testador')
tentativa('revisor-2', '04', 81, 90, para='testador')
tentativa('prumo-1', '12', 61, 75, para='testador')
tentativa('testador-1', '02', 73, 84, fim='resolveu')
tentativa('testador-2', '08', 59, 66, fim='resolveu')
tentativa('testador-1', '06', 85, 92, fim='resolveu')
tentativa('testador-2', '10', 79, 86, fim='resolveu')
tentativa('testador-1', '04', 93, 100, fim='resolveu')
tentativa('testador-2', '03', 100, 108, fim='resolveu')
tentativa('revisor-1', '03', 89, 99, para='testador')
tentativa('integrador-1', '20', 10, 18, fim='resolveu')  # descartado depois: o arquivo diz wontfix
for m, tk in ((53, '01'), (67, '08'), (85, '02'), (93, '06'), (101, '04'), (109, '03')):
    e('integrador-1', m, 'commit', ok=True, assunto='integra o ticket %s na base' % tk)

# o meio: segundo par espera o Gustavo; o 09 e o 13 vão para revisão; o 11 volta da revisão e vai de novo
tentativa('construtor-5', '09', 41, 95, para='revisor', subs=3)
e('construtor-2', 89, 'pegou_ticket', ticket='19')
e('construtor-2', 96, 'esperando_gustavo', ticket='19', detalhe='Ligar o notebook e aprovar o Tailscale nele')
e('construtor-2', 96.5, 'mandou_mensagem', para='maestro', assunto='O 19 precisa do Gustavo: ligar o notebook e aprovar o Tailscale')
e('maestro', 97, 'mandou_mensagem', para='construtor-2', assunto='Anotei para o Gustavo. Pegue o 15 enquanto isso')
tentativa('construtor-3', '13', 63, 100, para='prumo', subs=3)
tentativa('revisor-2', '11', 91, 99, fim='devolveu')
e('revisor-2', 99, 'devolveu', ticket='11', detalhe='Falta conferir o modo de desenvolvedor antes de criar os links')
tentativa('construtor-5', '11', 100, 112, para='revisor', subs=1)

# agora
e('construtor-1', 108, 'pegou_ticket', ticket='14')
for i in range(10):  # um agente chega a 10 subagentes abertos
    e('construtor-1', 110 + i * 2.6, 'abriu_subagente', sub='c1-14-s%d' % (i + 1), modelo='claude-opus-5-5',
      assunto=['Ler o grant atual', 'Listar os clientes', 'Testar o grant com chave nova', 'Conferir a tag da chave',
               'Escrever o teste do grant', 'Rodar o teste no par', 'Conferir o MCP de leitura', 'Ver os logs do par',
               'Revisar a documentação do grant', 'Montar o exemplo de cliente'][i])
e('construtor-2', 98, 'pegou_ticket', ticket='15')
for i, m in enumerate((100, 108, 121)):
    e('construtor-2', m, 'abriu_subagente', sub='c2-15-s%d' % (i + 1), modelo='claude-opus-5-5', assunto='Linha de MCP para o harness %d' % (i + 1))
e('construtor-2', 115, 'fechou_subagente', sub='c2-15-s1', ok=True)
e('construtor-3', 101, 'pegou_ticket', ticket='16')
e('construtor-3', 104, 'abriu_subagente', sub='c3-16-s1', modelo='claude-opus-5-5', assunto='Ler como a nota de retomada é usada')
e('construtor-3', 112, 'chamou_fable', ticket='16', sub='fable-16', modelo='claude-fable-5-1',
  assunto='Desenhar a gravação da nota sem perder edição concorrente')
e('construtor-3', 112.1, 'abriu_subagente', sub='fable-16', modelo='claude-fable-5-1',
  assunto='Desenhar a gravação da nota sem perder edição concorrente')
e('construtor-4', 68, 'pegou_ticket', ticket='17')  # vai estourar a 1 hora
for i, m in enumerate((72, 85, 101, 118)):
    e('construtor-4', m, 'abriu_subagente', sub='c4-17-s%d' % (i + 1), modelo='claude-opus-5-5', assunto='Busca no vault, tentativa %d' % (i + 1))
    if i < 2:
        e('construtor-4', m + 9, 'fechou_subagente', sub='c4-17-s%d' % (i + 1), ok=i == 0)
for m in (90, 104, 122):
    e('construtor-4', m, 'rodou_teste', ok=False, assunto='python -m pytest testes/test_busca.py', detalhe='a busca não acha a nota recém-criada')
e('construtor-4', 128, 'passou_1h', ticket='17')
e('construtor-4', 129, 'mandou_mensagem', para='maestro', assunto='O 17 passou de 1 hora: a busca não acha nota recém-criada')
e('maestro', 131, 'mandou_mensagem', para='construtor-4', assunto='Siga mais 15 min; se não fechar, devolva com o que achou')
e('construtor-5', 113, 'pegou_ticket', ticket='18')  # vai falhar
e('construtor-5', 116, 'abriu_subagente', sub='c5-18-s1', modelo='claude-opus-5-5', assunto='Ler a configuração do Codex')
e('construtor-5', 127, 'rodou_teste', ok=False, assunto='python -m pytest testes/test_codex.py', detalhe='config.toml não encontrado')
e('construtor-5', 131, 'falhou', ticket='18', detalhe='O Codex não está instalado nesta máquina: sem config.toml para editar')
e('construtor-5', 131.2, 'mandou_mensagem', para='maestro', assunto='Falhei no 18: o Codex não está instalado aqui')
e('revisor-1', 96, 'pegou_ticket', ticket='09')
e('revisor-1', 118, 'mandou_mensagem', para='construtor-5', assunto='No 09, o import vai antes ou depois do bloco do GSD?')
e('construtor-5', 120, 'mandou_mensagem', para='revisor-1', assunto='Depois do bloco do GSD; está no comentário do ticket')
e('revisor-2', 113, 'pegou_ticket', ticket='11')
e('revisor-2', 125, 'abriu_subagente', sub='r2-11-s1', modelo='claude-opus-5-5', assunto='Conferir o registro do modo de desenvolvedor')
e('prumo-1', 101, 'pegou_ticket', ticket='13')
e('prumo-1', 117, 'mandou_mensagem', para='construtor-3', assunto='No 13, o segundo MCP lê só a pasta do par?')
e('construtor-3', 119, 'mandou_mensagem', para='prumo-1', assunto='Sim, só a pasta do par; o grant fica no 14')
e('prumo-1', 121, 'mandou_mensagem', para='construtor-1', assunto='O 14 depende da resposta do 13: segue o que o construtor 3 disse')
e('testador-1', 101, 'pegou_ticket', ticket='07')
e('testador-1', 103, 'abriu_subagente', sub='t1-07-s1', modelo='claude-opus-5-5', assunto='Subir dois CouchDB')
e('testador-1', 104, 'abriu_subagente', sub='t1-07-s2', modelo='claude-opus-5-5', assunto='Escrever nos dois e comparar')
e('testador-1', 124, 'rodou_teste', ok=True, assunto='python -m pytest testes/test_livesync.py', detalhe='8 passaram')
e('testador-2', 109, 'pegou_ticket', ticket='12')  # vai ficar sem sinal
e('testador-2', 116, 'rodou_teste', ok=True, assunto='python -m pytest testes/test_chave.py', detalhe='5 passaram')
e('testador-2', 123, 'mandou_mensagem', para='construtor-1', assunto='A chave efêmera expira em 1 h ou em 24 h?')
e('construtor-1', 124, 'mandou_mensagem', para='testador-2', assunto='Em 24 h, com a tag cliente')
e('integrador-1', 120, 'mandou_mensagem', para='maestro', assunto='Base integrada até o 03; nada mais pronto para integrar')
e('maestro', 133, 'mandou_mensagem', para='construtor-5', assunto='Vou ver o 18 com o Gustavo; não repita')
e('prumo-2', 60, 'mandou_mensagem', para='maestro', assunto='Sem ticket para mim ainda; espero o 16')
e('prumo-2', 130, 'mandou_mensagem', para='construtor-3', assunto='Quando o Fable fechar, me passe o 16 antes do testador')

# batimentos: quem está vivo dá sinal até agora; o testador 2 para aos 126 min (sem sinal há 14 min)
ultimo_sinal = {a[0]: 139.5 for a in AGENTES}
ultimo_sinal['testador-2'] = 126
for ag, _, _ in AGENTES:
    m = 1.0
    while m <= ultimo_sinal[ag]:
        if not any(abs(x - m) < 0.5 for x, _ in ev[ag]):
            e(ag, m, 'sinal')
        m += random.uniform(0.6, 1.6)
    ev[ag] = [x for x in ev[ag] if x[0] <= ultimo_sinal[ag]]


def gravar(pasta):
    if os.path.isdir(pasta):
        shutil.rmtree(pasta)
    os.makedirs(os.path.join(pasta, 'tickets'))
    os.makedirs(os.path.join(pasta, 'eventos'))
    desc = {
        'formato': 1, 'id': 'construcao-fixture-ui', 'titulo': 'Construção do context hub', 'inicio': iso(0),
        'terminou_em': None,
        'limites': {'tentativa_min': 60, 'subagentes_por_agente': 10, 'sem_sinal_apos_s': 300},
        'fases': [{'id': 'spec', 'titulo': 'Spec', 'estado': 'feita'},
                  {'id': 'tickets', 'titulo': 'Tickets de construção', 'estado': 'feita'},
                  {'id': 'execucao', 'titulo': 'Execução', 'estado': 'em-curso'}],
        'papeis': [{'id': p, 'titulo': p.capitalize()} for p in ('construtor', 'revisor', 'testador', 'integrador', 'prumo', 'maestro')],
        'agentes': [{'id': i, 'papel': p, 'titulo': t, 'modelo': 'claude-opus-5-5', 'esforco': 'alto', 'terminal': t} for i, p, t in AGENTES],
        'padroes': {'teste': ['^python -m pytest\\b'], 'commit': ['^git commit\\b']},
    }
    with open(os.path.join(pasta, 'execucao.json'), 'w', encoding='utf-8', newline='\n') as f:
        json.dump(desc, f, ensure_ascii=False, indent=2)
    for n, tit, st, dono, com, bb in TICKETS:
        slug = n + '-' + ''.join(c if c.isalnum() else '-' for c in tit.lower())[:40].strip('-')
        with open(os.path.join(pasta, 'tickets', slug + '.md'), 'w', encoding='utf-8', newline='\n') as f:
            f.write('# %s\n\nType: task\nStatus: %s\nDono: %s\nCom: %s\nBlocked by: %s\n\n## Pronto quando\n\n- (fixture)\n\n## Comments\n' % (tit, st, dono, com, bb))
    for ag, lista in ev.items():
        lista.sort(key=lambda x: x[0])
        with open(os.path.join(pasta, 'eventos', ag + '.jsonl'), 'w', encoding='utf-8', newline='\n') as f:
            for _, linha in lista:
                f.write(json.dumps(linha, ensure_ascii=False) + '\n')
    return desc


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--pasta', default=os.path.join(AQUI, 'instantaneo-ui'))
    a = p.parse_args()
    gravar(a.pasta)
    print('fixture em', a.pasta, 'agora =', AGORA.isoformat())
    # a mesma fixture embutida, para abrir web/index.html direto do disco
    import sys; sys.path.insert(0, AQUI); import embutir
    embutir.embutir(a.pasta, os.path.join(AQUI, 'embutida.js'), AGORA.isoformat())


if __name__ == '__main__':
    main()
