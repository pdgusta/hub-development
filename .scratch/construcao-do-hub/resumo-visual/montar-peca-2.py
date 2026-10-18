# Monta fatos-peca-2.json (a partir de dados-memoria-trava.json e dados-achados.json, mais rótulos curtos
# escritos à mão) e a página peca-2-rio-estreito.html (modelo-peca-2.html com os fatos embutidos).
import json, re, pathlib
from datetime import datetime, timedelta

AQUI = pathlib.Path(__file__).parent
MT = json.loads((AQUI / 'dados-memoria-trava.json').read_text(encoding='utf-8'))
AC = json.loads((AQUI / 'dados-achados.json').read_text(encoding='utf-8'))

def t(s):
    """'2026-10-17 ~03:29 (...)' ou '2026-10-17T05:12:24' -> '2026-10-17T03:29'"""
    if not s: return None
    m = re.search(r'(2026-10-1[67])[ T]~?(\d{1,2}):(\d{2})', s)
    if not m: return None
    return f'{m.group(1)}T{int(m.group(2)):02d}:{m.group(3)}'
aprox = lambda s: bool(s and '~' in s)
dt = lambda s: datetime.fromisoformat(s)
fmt = lambda d: d.strftime('%Y-%m-%dT%H:%M')

# ---------- memória ----------
memoria = []
for p in MT['memoria']:
    if p.get('repete'): continue
    memoria.append({'t': t(p['hora_local']), 'mb': p['mb'], 'ctx': p['contexto'], 'fonte': p['fonte'],
                    **({'fora_da_base': True} if p.get('fora_da_base') else {})})
# sondagens escritas: as do diário/retomada e o mínimo de cada medidor
for p, o in zip(memoria, [x for x in MT['memoria'] if not x.get('repete')]):
    escrever = ('diario' in o['fonte'] or 'retomada' in o['fonte'] or o.get('minimo_do_arquivo')
                or '.status' in o['fonte'] and ('começou' in o['contexto'] or 'mín' in o['contexto']))
    p['escrever'] = bool(escrever)
# 21:10 tem duas medidas (714 com todos religados, 3.000 depois): fica a primeira no rio, a segunda escrita
memoria.sort(key=lambda p: p['t'])

# ---------- encalhes ----------
CONSERTO_MEM = {a['id']: a for a in AC['achados'] if a['tipo'] == 'queda por memória'}
ENC = [  # hora, curto, id do achado de memória (para o "como se resolveu")
    ('2026-10-16T23:05', 'fila Docker do banco do par morta pelo sistema', 'd1-mem-docker-07'),
    ('2026-10-16T23:40', 'a fila do banco do par morre de novo', 'd1-mem-docker-07'),
    ('2026-10-17T00:35', 'suíte da junção parou: memória crítica', 'd1-mem-suite-c1'),
    ('2026-10-17T03:59', 'Docker do teste de limites do banco cai aos 18 min', 'd2-mem-08-docker'),
    ('2026-10-17T05:12', 'arquivo grande do banco: 2.900 → 513 MB', 'd2-mem-08-fatia2-a'),
    ('2026-10-17T07:39', 'arquivo grande de novo: 3.183 → 621 MB', 'd2-mem-08-fatia2-b'),
    ('2026-10-17T08:26', 'Docker do proxy cortado: 613 MB', 'd2-mem-22-docker'),
    ('2026-10-17T13:01', 'prova do hub, rodada 1: corte em 670 MB', 'd2-mem-25-piso'),
    ('2026-10-17T13:13', 'prova do hub, rodada 2: corte em 480 MB', 'd2-mem-25-piso'),
    ('2026-10-17T13:39', 'prova do hub, fase 7: corte em 671 MB', 'd2-mem-25-fase7'),
    ('2026-10-17T14:17', 'prova do hub, fase 4: corte antes de começar (477 MB)', None),
    ('2026-10-17T15:33', 'Codex no proxy cortado: 583 MB', 'd2-mem-22-codex'),
]
cortes = []
for hora, curto, aid in ENC:
    c = next(x for x in MT['cortes'] if t(x['hora']) == hora)
    a = CONSERTO_MEM.get(aid)
    cortes.append({'t': hora, 'curto': curto, 'oque': c['o_que'], 'mb': c.get('mb_no_corte'),
                   'nota': (c.get('nota') or '') + (' (hora aproximada)' if c.get('hora_aproximada') else ''),
                   'conserto': a['conserto'] if a else 'A fase 4 foi para a janela da noite (diário:158); verde às 19:39 (diário:193).',
                   'fonte': c['fonte'] + ('; ' + '; '.join(a['fontes']) if a else '; etapas/diario-da-construcao.md:158,193')})

pisos = [
    {'t': '2026-10-17T03:59', 'mb': 2000, 'texto': 'Piso do Docker do 08: rodar fatia por fatia só com 2 GB livres; parar abaixo de 700 MB.', 'fonte': 'etapas/diario-da-construcao.md:28'},
    {'t': '2026-10-17T12:48', 'mb': 2500, 'texto': 'Piso do corredor do 25: 2.500 MB livres para começar (o corredor das 12:48 começou com 1.852).', 'fonte': 'etapas/diario-da-construcao.md:151; etapas/logs/25-corredor.status:11'},
    {'t': '2026-10-17T13:03', 'mb': 1800, 'texto': 'Piso do 25 baixado para 1.800 MB (HUB_25_PISO_MB); o corte de 700 MB segue.', 'fonte': 'etapas/diario-da-construcao.md:151'},
]

# ---------- trava (barcos) ----------
PULAR = ('na fila depois', 'SEM a trava')
barcos = []
for b in MT['trava']:
    if any(p in (b.get('o_que') or '') for p in PULAR): continue
    if not b.get('inicio') and not b.get('fim'): continue
    barcos.append({'quem': b['quem'], 'oque': b['o_que'], 'ini': t(b.get('inicio')), 'fim': t(b.get('fim')),
                   'nota': b.get('nota') or '', 'fonte': b['fonte']})
AJUSTE_TRAVA = {  # (quem, o que) -> campos corrigidos na revisão (Esquadro, volta 1), com a fonte
 ('Rebite', 'suíte 41+40+43+docs'): {'fim': '2026-10-17T15:18', 'fonte+': 'etapas/logs/juncao-41-40-43-docs-suite.log (gravado 15:18:09)'},
 ('Vela', 'Codex do 18'): {'ini': '2026-10-17T15:18', 'fim': '2026-10-17T15:19', 'ini_inferido': False,
                           'fonte+': 'etapas/logs/18-codex.log (gravado 15:19:32, 42 s)'},
 ('Brasa', 'Docker do 08 (todas as fatias)'): {'fim': '2026-10-17T03:55', 'fonte+': 'etapas/relatorio-08-banco-limites.md:113 (caiu aos 18 min, ~03:55; o diário registra 03:59)'},
 ('Rebite', 'suíte 24+22'): {'fim': '2026-10-17T19:21', 'fonte+': 'etapas/logs/juncao-24-22-suite.log (gravado 19:20:55)'},
 ('Brasa', 'fatias 2-7 do 08 (corredor 217400)'): {'lado': 1, 'oque': 'corredor das fatias do banco, sem pegar a trava (parado em 2 min)'},
 ('Rebite', 'suíte do 11 + docs 4ª leva'): {'ini': '2026-10-17T15:40', 'ini_inferido': False,
                           'fonte+': 'etapas/logs/juncao-11-docs-suite.log (gravado 16:15:18, ~2.100 s)'},
}
for b in barcos:
    aj = AJUSTE_TRAVA.get((b['quem'], b['oque']))
    if not aj: continue
    aj = dict(aj)
    for k, v in aj.items():
        if k == 'fonte+': b['fonte'] += '; ' + v
        else: b[k] = v
    if b.get('fim'): b.pop('fim_visual', None)
barcos.sort(key=lambda b: b['ini'] or b['fim'])
for i, b in enumerate(barcos):   # pontas sem registro: até o barco vizinho, no máximo 45 min; desenhadas apagadas
    if not b['ini']:
        ant = max((x['fim'] or x['ini'] for x in barcos[:i] if (x['fim'] or x['ini']) <= b['fim']), default=None)
        lim = fmt(dt(b['fim']) - timedelta(minutes=45))
        b['ini'] = max(ant, lim) if ant else lim
        b['ini_inferido'] = True
    if not b['fim']:
        prox = min((x['ini'] or x['fim'] for x in barcos[i+1:] if (x['ini'] or x['fim']) > b['ini']), default=None)
        lim = fmt(dt(b['ini']) + timedelta(minutes=45))
        b['fim_visual'] = min(prox, lim) if prox else lim
# pontas inferidas não invadem o barco vizinho: inferida contra inferida divide ao meio; contra registrada, cede
barcos.sort(key=lambda b: b['ini'])
for a, b in zip([x for x in barcos if not x.get('lado')], [x for x in barcos if not x.get('lado')][1:]):
    fa = a['fim'] or a.get('fim_visual')
    if fa <= b['ini']: continue
    a_inf, b_inf = not a['fim'], bool(b.get('ini_inferido'))
    if a_inf and b_inf:
        meio = fmt(dt(b['ini']) + (dt(fa) - dt(b['ini'])) / 2)
        a['fim_visual'] = meio; b['ini'] = meio
    elif a_inf: a['fim_visual'] = b['ini']
    elif b_inf: b['ini'] = fa
    elif not b.get('lado') and (dt(fa) - dt(b['ini'])).total_seconds() <= 180: b['ini'] = fa  # registros a 1-3 min: o seguinte começa quando o outro solta
# episódio 1: a trava sobrescrita (diário:10-11)
for b in barcos:
    if b['quem'] == 'Trilho' and b['ini'] == '2026-10-17T00:58':
        b['fim'] = '2026-10-17T01:08'; b.pop('fim_visual', None); b['lado'] = 1
        b['nota'] += ' | Às ~01:08 o maestro, limpo, vê as duas suítes juntas e o Trilho para a dele (diário:10).'
    if b['quem'] == 'Brasa' and b['ini'] == '2026-10-17T00:58':
        b['lado'] = -1
# episódio 3: o deslize (diário:66) — barco ao lado do Rebite
barcos.append({'quem': 'Trilho', 'oque': '12-busca sem a trava (deslize)', 'ini': '2026-10-17T06:50', 'fim': '2026-10-17T06:52',
               'lado': 1, 'nota': 'Rodou ~2 min sem a trava, enquanto o Rebite a segurava; não repetiu.', 'fonte': 'etapas/diario-da-construcao.md:66'})
for b in barcos:
    if b['quem'] == 'Rebite' and b['ini'] == '2026-10-17T06:44': b['lado'] = -1
# episódio 2: a corrida (diário:53) — a Brasa retoma sozinha; o Cinzel era o primeiro da fila
for b in barcos:
    if b['quem'] == 'Brasa' and b['ini'] == '2026-10-17T05:47': b['lado'] = 1
barcos.append({'quem': 'Cinzel', 'oque': 'na vez dele, à espera (fila furada)', 'ini': '2026-10-17T05:47', 'fim': '2026-10-17T05:49',
               'lado': -1, 'fantasma': True, 'nota': 'O Cinzel era o primeiro da fila; pegou a trava às 05:49:01 (10-corredor.status:1).',
               'fonte': 'etapas/diario-da-construcao.md:53; etapas/logs/10-corredor.status:1'})

episodios = [
    {'t': '2026-10-17T01:03', 'curto': 'trava sobrescrita: duas suítes juntas', 'titulo': 'A trava sobrescrita',
     'texto': 'Brasa (00h58) e Trilho (01h06, pelo diário; 00:58 pelo arquivo da trava) rodaram suítes pesadas ao mesmo tempo: a trava de um sobrescreveu a do outro. 1,9 GB livres; a suíte da Brasa deu 2 falhas por tempo na indexação da busca.',
     'conserto': 'O maestro, limpo às ~01:08, viu; o Trilho parou a dele. A Brasa repetiu com a trava e uma suíte por vez (187: 179 verdes, 8 pulados, 0 falhas).',
     'fonte': 'etapas/diario-da-construcao.md:10-11; issues/07:26-28; git 6823e41 (trava-pesada.md às 01:02)'},
    {'t': '2026-10-17T05:48', 'curto': 'corrida na trava: a fila foi furada', 'titulo': 'A corrida na trava',
     'texto': 'O corredor destacado da Brasa (fatias do 08) retomava a trava sozinho entre as fatias e passou na frente do Cinzel, que era o primeiro da fila.',
     'conserto': 'Ordem firme: Cinzel (10), Rebite (suíte 28+09), Brasa (fatias 3-7), Trilho (Codex do 15 após 06:58). O corredor da Brasa parou às 05:48:46.',
     'fonte': 'etapas/diario-da-construcao.md:53; etapas/logs/08-fatias.status:13-15'},
    {'t': '2026-10-17T06:51', 'curto': 'deslize: busca rodada sem a trava', 'titulo': 'O deslize',
     'texto': 'O Trilho rodou o teste da busca (12-busca) sem a trava, por ~2 min, enquanto o Rebite segurava a trava com a suíte do 36 e do 10. Às 06:49 a memória livre estava em 577 MB.',
     'conserto': 'Registrado como deslize; não se repetiu.', 'fonte': 'etapas/diario-da-construcao.md:63,66'},
]

# ---------- janelas quietas ----------
janelas = []
for j in MT['janelas_quietas']:
    limpa = lambda L: [re.sub(r'\s*\(.*\)', '', x) for x in L if not x.startswith('(')]
    fim = t(j['fim']) if j['fim'] else '2026-10-17T18:20'
    janelas.append({'ini': t(j['inicio']), 'fim': fim, 'ficaram': limpa(j['quem_ficou']), 'sairam': limpa(j['quem_saiu']),
                    'rodou': '; '.join(j['o_que_rodou']),
                    'fonte': j['fonte'] + ('' if j['fim'] else '; fim: o Fiel religa "ao fim da janela" (diário:178), religado às 18:20 (diário:185)')})

# ---------- Codex ----------
codex = []
for c in AC['codex_cota']['janelas']:
    ini = t(c['sem_cota_desde']); fim = t(c['volta'])
    codex.append({'ini': ini, 'fim': fim, 'ini_antes': bool(re.search(r'~|antes', c['sem_cota_desde'])), 'curto': f'sem cota até {fim[11:16].replace(":", "h")}' + (' (Gustavo redefiniu)' if '14:26' in c['volta'] else ''),
                  'nota': f"Desde: {c['sem_cota_desde']}. Volta: {c['volta']}.", 'fonte': c['fonte']})
comporta = {'t': '2026-10-17T14:26', 'curto': 'Gustavo redefine a cota do Codex', 'titulo': 'A comporta: cota do Codex redefinida',
            'texto': 'O Gustavo usou 1 dos 3 reinícios semanais da cota (restam 2) e avisou que o Windows reinicia às 21h. Sem isso, o Codex voltaria só às 17:15.',
            'fonte': 'etapas/diario-da-construcao.md:149,160; etapas/diario-da-construcao.md:120'}

reinicios = [
    {'t': '2026-10-17T10:05', 't2': '2026-10-17T10:11', 'curto': 'Maestri reiniciado (atualização)', 'oque': 'Maestri reiniciado pelo Gustavo (atualização 0.25.0)',
     'efeito': 'Os sete recrutas voltaram sozinhos, com o contexto; ronda recriada; recados reenviados.', 'fonte': 'etapas/diario-da-construcao.md:117,203'},
    {'t': '2026-10-17T21:10', 'curto': 'Windows reinicia', 'oque': 'Reinício do Windows (atualizações cumulativas), avisado pelo Gustavo às 14:26',
     'efeito': 'O Maestri religou todos em sessões antigas (714 MB livres); o maestro fechou os sem trabalho (3,0 GB livres).', 'fonte': '.scratch/context-hub/retomada-maestro.md:117; etapas/diario-da-construcao.md:160'},
]

# ---------- pedras ----------
CURTO = {
 'd1-07-daemon-trava-chamador': 'daemon do banco prendia quem chamava',
 'd1-pastas-hub-ensaio-14': 'testes deixavam pastas no %TEMP%',
 'd1-07-religar-cli': 'pasta excluída seguia replicando',
 'd1-29-suite-chama-harness': 'a suíte abria os harnesses de verdade',
 'd1-05-intermitente': 'teste do frontmatter falhou uma vez',
 'd1-12-sem-busca-no-ensaio': 'aceite da busca sem a busca instalada',
 'd1-12-tempo-segunda-partida': 'teste da busca dependia do relógio',
 'd1-27-montador-sem-stderr': 'montador caía calado, sem stderr',
 'd1-05-bomba-de-data': 'bomba de data: vermelho à meia-noite',
 'd2-crlf-guarda': 'CRLF furava a guarda de regravação',
 'd2-12-codex-recusa-mcp': 'Codex recusava a busca sem aprovação',
 'd2-15-read-fura-aviso': 'a read da busca furava o aviso',
 'd2-08-ebusy-60mib': 'arquivo de 60 MiB derrubava o CLI',
 'd2-16-docker-6-falhas': 'vigia: 6 falhas na 1ª rodada Docker',
 'd2-36-pastas-1325': '1.325 pastas esquecidas no %TEMP%',
 'd2-08-fatia3-falso-passa': 'PASSA sem ter o que conferir',
 'd2-10-docker-crlf': 'teste do MCP esperava LF, veio CRLF',
 'd2-16-caminho-ofuscado': 'caminho ofuscado escondia a folha',
 'd2-10-npm-test-zero': 'npm test rodou 0 testes e deu verde',
 'd2-15-hifen-sublinhado': 'Codex troca hífen por sublinhado',
 'd2-10-temp-curto-fork': 'TEMP em nome curto: 20 testes caem',
 'd2-11-codex-trava-teste': 'Codex travava o processo do teste',
 'd2-18-cobrava-quem-nao-gravou': 'o fim cobrava quem não gravou',
 'd2-21-eperm-rename': 'rename com EPERM ao arquivar',
 'd2-22-frase-no-stderr': 'frase esperada no stdout veio no stderr',
 'd2-25-fase2-tasks': 'teste da prova citava linha já trocada',
 'd2-21-caminho-curto-fswatch': 'caminho curto do Windows aborta o node',
 'd2-16-skill-md-yaml': 'YAML quebrado: junção da vigia desfeita',
 'd2-23-fazer-apaga-original': 'o desfazer apagava o arquivo original',
 'd2-40-roteamento-fora-do-agents': 'roteamento das skills fora do AGENTS.md',
 'd2-docs-busca-prazo': 'busca estourou o prazo com os docs',
 'd2-22-trust-level': 'kit apagava o trust_level do Codex',
 'd2-42-mod-pelo-atalho': 'mod não via o hub aberto pelo atalho',
 'd2-25-ponte-ramo-errado': 'ponte da prova no ramo errado do fork',
 'd2-25-nota-nao-desce': 'a nota não descia do par A ao B',
 'd2-27-link-em-codigo-inline': 'link dentro de código derruba o verificador',
 'd2-23-eperm-intermitente': 'EPERM passageiro no kit, sob carga',
 'd2-25-fase7-pipe': 'prova do hub presa 28 min num pipe',
 'd2-25-fase2-codex-shell': 'o pedido proibia o shell do Codex',
 'd2-25-fase7-falso-verde': 'prova "verde" sem rodar harness',
}
HORA_ACHADO = {  # hora do achado corrigida na revisão (Esquadro, volta 1), com a fonte
 'd2-25-nota-nao-desce': ('2026-10-17T14:06', 'etapas/diagnostico-25-nota-nao-desce.md (1ª queda A→B às 14:06)'),
 'd2-27-link-em-codigo-inline': ('2026-10-17T15:18', 'issues/44:30 (15:18)'),
 'd1-29-suite-chama-harness': ('2026-10-16T21:20', 'issues/07:24 (~21:20)'),
}
achados = []
for a in AC['achados']:
    if a['id'] not in CURTO: continue
    ta, tc = t(a['hora_achado']), t(a['hora_conserto'])
    ta = HORA_ACHADO.get(a['id'], (ta,))[0]
    if tc and ta and tc < ta: ta = tc  # conserto registrado antes da hora estimada do achado
    for campo in ('o_que_quebrou', 'causa', 'conserto'):
        a[campo] = a[campo].replace('GUSTAV~1.DEL', 'o nome curto do Windows (8.3)')
    a['conserto'] = a['conserto'].replace('Precursor do ticket 36.', 'Precursor do ticket 36 (os testes apagam a pasta de ensaio).')
    achados.append({'id': a['id'], 't': ta, 't_conserto': tc, 'curto': CURTO[a['id']], 'ticket': a['ticket'], 'quem': a.get('quem_achou'),
                    'quebrou': a['o_que_quebrou'], 'causa': a['causa'], 'conserto': a['conserto'],
                    'aprox': bool(a.get('hora_aproximada')),
                    'fontes': a['fontes'] + ([HORA_ACHADO[a['id']][1]] if a['id'] in HORA_ACHADO else [])})
assert len(achados) == len(CURTO), set(CURTO) - {a['id'] for a in achados}

# ---------- placas (Gustavo) e marcos (maestro) ----------
PLACA = {  # trecho da regra -> (hora, curto)
 'O revisor Fiel passa de Codex': ('2026-10-16T20:12', 'Fiel passa do Codex ao Claude'),
 'Aval para copiar o login': ('2026-10-16T20:24', 'login dos harnesses no ensaio'),
 'Portal fechado por RAM': ('2026-10-17T00:24', 'portal fechado para poupar RAM'),
 'Mandato:': ('2026-10-17T03:19', 'mandato: o maestro decide por mim'),
 'Até 4 construtores': ('2026-10-17T03:23', 'até 4 construtores e 1 subagente'),
 'Mais até 3 subagentes Haiku': ('2026-10-17T03:25', '+3 subagentes Haiku, só tarefa simples'),
 'Pedido: duas peças': ('2026-10-17T03:31', 'ao fim, duas peças visuais'),
 'Fatia 2 do 08 com menos agentes': ('2026-10-17T09:25', 'teste grande do banco com menos agentes'),
 'Guardar os 3 reinícios': ('2026-10-17T10:18', 'guardar os 3 reinícios do Codex'),
 'Testes do Codex com o GPT 6.1 Sol': ('2026-10-17T11:38', 'testes do Codex com o GPT 6.1 Sol'),
 'Um agente só de documentação': ('2026-10-17T12:05', 'um documentador: Lume'),
 'Codex sem cota não para nada': ('2026-10-17T14:28', 'sem cota, o Claude assume'),
 'Codex só para testes': ('2026-10-17T14:33', 'Codex só para testes; Fielzinho sai'),
 'O ticket 26 vira': ('2026-10-17T20:12', 'instalar o hub nas duas máquinas'),
}
TEXTO_REGRA = {
 'Até 4 construtores': 'Até 4 construtores e 1 subagente por recruta (antes: até 3 construtores e nenhum subagente).',
 'Fatia 2 do 08 com menos agentes': 'O arquivo grande do teste de limites do banco (fatia 2, ticket 08) roda com menos agentes abertos: janela quieta (todos salvam e saem, menos quem roda).',
 'O ticket 26 vira': 'A instalação de verdade (ticket 26) vira a instalação nas DUAS máquinas (par 2 no outro PC); comunicação entre os dois maestros no radar.',
}
GIT_HORA = {'d7a0f33': '03:19', '2e605d1': '03:23', '8493aaf': '03:25', '41fc0fb': '03:31'}
regras = []
for r in AC['regras_novas']:
    k = next((k for k in PLACA if r['regra'].startswith(k)), None)
    if not k: continue
    hora, curto = PLACA[k]
    texto = TEXTO_REGRA.get(k, r['regra'])
    regras.append({'t': hora, 'curto': curto, 'texto': texto, 'quem': r['de_quem'], 'fonte': r['fonte']})
assert len(regras) == len(PLACA), [k for k in PLACA if not any(x['texto'].startswith(k) for x in regras)]

MARCO_REGRA = {  # regras do maestro que viram marco com rótulo
 'Testes com harness de verdade só sob pedido': ('2026-10-16T21:33', 'harness real só sob pedido'),
 'Política de vermelho intermitente': ('2026-10-17T00:02', 'vermelho intermitente: repetir e avisar'),
 'Um trabalho pesado por vez': ('2026-10-17T00:35', 'um trabalho pesado por vez: a trava'),
 'Docker do 08 destacado': ('2026-10-17T04:00', 'fila da trava: quem solta avisa o próximo'),
 'Suíte inteira só na junção': ('2026-10-17T04:15', 'suíte inteira só na junção'),
 'Todo teste novo usa o ajudante': ('2026-10-17T06:09', 'todo teste usa a pasta de ensaio comum'),
 '/exit e caminhos': ('2026-10-17T13:25', '/exit aos recrutas pelo PowerShell'),
 'Nada pesado começa depois': ('2026-10-17T19:13', 'nada pesado depois de 19h45'),
}
decisoes = []
for r in AC['regras_novas']:
    k = next((k for k in MARCO_REGRA if r['regra'].startswith(k)), None)
    if not k: continue
    hora, curto = MARCO_REGRA[k]
    texto = r['regra'].replace('regra provisória até o 29.', 'regra provisória até o ticket 29 (harness só sob pedido).').replace('Docker do 08 destacado', 'Docker do teste de limites do banco (08) destacado')
    decisoes.append({'t': hora, 'curto': curto, 'texto': texto, 'ticket': 'processo', 'rever': False, 'rotulo': True, 'fonte': r['fonte']})
NOME = {'01': 'prova de dois CouchDB', '02': 'prova das pastas com ponto', '03': 'prova dos hooks do Codex', '04': 'esqueleto do hub',
 '05': 'frontmatter imposto', '06': 'gerador de exclusões', '07': 'banco do par', '08': 'limites do banco', '09': 'MCP do banco: gravar com versão',
 '10': 'MCP do banco: instâncias e estado', '11': 'MCP do banco nos três harnesses', '12': 'busca local', '13': 'Gemini pronto e desligado',
 '14': 'guardas de regravação', '15': 'aviso de leitura', '16': 'vigia', '17': 'vigia nas telas', '18': 'retomada', '19': 'roteamento de skills',
 '20': 'acervo do maestro', '21': 'arquivar e cópia diária', '22': 'proxy e kit de cliente', '23': 'kit de par: a forma', '24': 'kit de par ao vivo',
 '25': 'prova do hub inteiro', '26': 'instalação de verdade', '27': 'verificador das pastas', '28': 'pastas locais', '29': 'harness só sob pedido',
 '30': 'montador mostra a falha do git', '31': 'registro dos avais', '32': 'link para fora do hub', '33': 'link fora: imagem e rede',
 '34': 'roteamento: registro por skill', '35': 'aval sem parecer', '36': 'testes apagam a pasta de ensaio', '37': 'fim da resposta vê o shell',
 '38': 'ajudante de pasta nos testes', '39': 'vigia grava mensagem limpa', '40': 'roteamento no AGENTS.md', '41': 'busca sem agents/code',
 '42': 'mod pelo atalho', '43': 'Codex usa o luna', '44': 'verificador pula código'}
com_nome = lambda txt: re.sub(r'\b(\d{2})\b', lambda m: f"{m.group(1)} ({NOME[m.group(1)]})" if m.group(1) in NOME else m.group(1), txt)
CURTO_D = [  # (começo do texto da decisão, rótulo curto em palavras, hora pelo git se o diário está adiantado, texto novo)
 ('Junções mantidas apesar', 'junções mantidas apesar da suíte parada', None, None),
 ('Ponta a ponta do Claude', 'ponta a ponta do Claude fica com a Vela', None, None),
 ('O hub-busca expõe só a search', 'a busca expõe só a search', '2026-10-17T03:14', None),
 ('Pontos abertos da faixa 5', 'regras de gravação do MCP do banco', '2026-10-17T03:29', None),
 ('Rodar destacado, fatia', 'teste do banco fatia por fatia, piso 2 GB', None, None),
 ('O 16 começa antes', 'a vigia começa antes dos bloqueios', '2026-10-17T04:25', None),
 ("'Piora' = algum item", '"piora" na vigia = item sobe de nível', '2026-10-17T04:28', None),
 ('Achados aceitos: o LiveSync', 'conflito só quando a base não está viva', '2026-10-17T04:44', None),
 ('Portas 8796', 'portas e regra curta do MCP do banco', None, None),
 ('Estado velho:', 'estado velho da vigia: aviso após 15 min', None, None),
 ('O 17 começa antes', 'vigia nas telas começa antes da vigia', None, None),
 ('Vigia no Claude Code pela linha', 'vigia no Claude pela linha de status', None, None),
 ('Fatias 3-7 primeiro', 'o arquivo grande do banco por último', None, None),
 ('Ordem firme na fila', 'ordem firme na fila da trava', None, None),
 ('Revisão começa já, com a fatia 2', 'banco vai à revisão sem o arquivo grande', None, None),
 ('Costuras aceitas: proxy TBXark', 'proxy local; harnesses reais como cliente', None, None),
 ('O 18 começa já', 'retomada começa sobre a vigia nas telas', None, None),
 ('Opção A:', 'retomada: opção A (muda o spec)', None, None),
 ('Começa já; costuras: edição recente', 'arquivar começa já, 15 min de folga', None, None),
 ('A fatia 2 vira item do Gustavo', 'arquivo grande do banco fica com o Gustavo', None, None),
 ('O 23 começa antes', 'kit de par começa antes dos bloqueios', None, None),
 ('Skill de uso geral', 'skill de uso geral marcada no kit', None, None),
 ('wsl --shutdown na vez dela', 'desligar o WSL e indexar antes dos pares', None, None),
 ('Binário descartado', 'arquivo descartado pela vigia = divergência', None, None),
 ('Começa já como preparo', 'prova do hub por fases, corte em 700 MB', None, None),
 ('Começa já sobre o ramo do 23', 'kit ao vivo numa casa de ensaio', None, None),
 ('Ressalva 1 do 18 aceita', 'rede da retomada vira ticket próprio', None,
  'Ressalva 1 da retomada (ticket 18) aceita; a gravação pela rede vira um ticket próprio (37, o fim da resposta vê a gravação feita pelo shell).'),
 ('Arquivar move arquivo por arquivo', 'arquivar move arquivo por arquivo', None, None),
 ('Costuras aceitas: varredura', 'fim da resposta: varrer só após shell', None, None),
 ('O proxy não repassa', 'proxy sem as instruções do MCP: no radar', None, None),
 ('Cada fase registra o que subiu', 'o corte do medidor derruba tudo o que subiu', None, None),
 ('Vai ao Rebite já', 'proxy vai à junção; Codex depois', None, None),
 ('A ressalva da rodada 2 entra', 'ressalva entra antes da junção', None, None),
 ('Docker de 08/09/10 dispensado', 'Docker do banco dispensado no ajudante', None,
  'No ajudante de pasta nos testes (ticket 38), o Docker dos testes do banco e do MCP (08, 09, 10) foi dispensado: as fases da prova do hub inteiro (25) já os exercitam.'),
 ('Perda de arquivo no HOME real', 'kit perdia arquivo: conserto antes da junção', None, None),
 ('Manutenção do config.toml', 'config do Codex consertado no ramo do proxy', None, None),
 ('Ticket 41 publicado', 'ticket novo: a busca sem agents/code', None, None),
 ('Piso do corredor 1.800 MB', 'piso do corredor da prova: 1.800 MB', None, None),
 ('Fase 7 sozinha numa janela', 'a fase 7 da prova sozinha numa janela', None, None),
 ('O 12-busca do 41', 'teste da busca fica para a junção', None,
  'O teste da busca (12-busca) do ticket 41 (a busca não indexa agents/code) fica para a junção: a suíte inteira já o roda.'),
 ('41, 40 e 43 resolvidos', '3 tickets resolvidos; verificador vira ticket', None,
  'Os tickets 41 (busca sem agents/code), 40 (roteamento no AGENTS.md) e 43 (Codex usa o luna) resolvidos apesar da falha do teste do verificador de pastas (27-pastas); a documentação fica pendente; a causa vira o ticket 44 (o verificador não lê link dentro de código).'),
 ('Janela quieta da noite', 'janela quieta da noite: um de cada vez', None, None),
 ('Conserto curto do EPERM', 'EPERM do kit: repetir por 2 s', None, None),
 ('Se a fase 4 cair igual', 'teto 20h; Brasa diagnostica se cair', None, None),
 ('Fase 7 agora;', 'Brasa e Vela juntas na nota que não desce', None, None),
 ("Conserto candidato 'daemon", '"--interval 5": descartado às 18:50', None, None),
 ('Ordem: fase 7, fase 4', 'ordem final da prova numa subida só', None,
  'Ordem final da prova do hub inteiro (ticket 25): fase 7, fase 4 e a fase 2 do Codex, numa subida só dos pares; nada pesado depois de 19h45.'),
 ('O 25 fecha sem o Codex', 'a prova fecha sem o Codex no hub inteiro', None, None),
 ('Nota que não descia', 'nota que não desce: conserto só no teste', None, None),
]
for r in AC['decisoes_do_maestro']:
    if r['decisao'].startswith('Suíte inteira só na junção'): continue  # já é marco de regra
    c = next(c for c in CURTO_D if r['decisao'].startswith(c[0]))
    decisoes.append({'t': c[2] or t(r['hora']), 'curto': c[1], 'texto': c[3] or r['decisao'], 'ticket': com_nome(r['ticket']),
                     'rever': bool(r['para_rever']), 'rotulo': True, 'fonte': r['fonte'] + (' (hora pelo git deste repositório)' if c[2] else '')})
decisoes.sort(key=lambda d: d['t'])

numeros = [
    {'valor': '448 MB', 'rotulo': 'a menor memória livre medida (14h18)', 'destaque': True,
     'detalhe': 'Ronda das 14:18, logo depois do corte da fase 4 da prova do hub inteiro (ticket 25), às 14:17:47.', 'fonte': 'etapas/diario-da-construcao.md:159'},
    {'valor': str(len(cortes)), 'rotulo': 'encalhes: trabalho que caiu por falta de memória',
     'detalhe': 'Quatro quedas fora do medidor (a fila Docker do banco do par duas vezes, a suíte da junção das 00h35 e o Docker do teste de limites do banco) e oito cortes do medidor abaixo de 700 MB. Fontes de cada um no toque.', 'fonte': 'dados-memoria-trava.json (cortes)'},
    {'valor': str(len(achados)), 'rotulo': 'pedras: achados que derrubaram algo, cada um com o conserto',
     'detalhe': 'Sem as quedas por memória (são os encalhes) e sem as voltas comuns da revisão (estão na peça 1).', 'fonte': 'dados-achados.json (achados)'},
    {'valor': '3', 'rotulo': 'janelas quietas: o canvas esvazia para o pesado rodar',
     'detalhe': '09:34-10:03, 13:22-14:17 e 16:52 até o Fiel religar às 18:20.', 'fonte': 'etapas/diario-da-construcao.md:109-116, 153-158, 176-185'},
    {'valor': '5', 'rotulo': 'vezes sem cota do Codex',
     'detalhe': '2 no dia 16 e 3 no dia 17; o Gustavo usou 1 dos 3 reinícios de cota às 14:26.', 'fonte': 'etapas/diario-da-construcao.md:9, 26, 79, 149, 160; git 7953b50'},
]

fatos = {
  'meta': {'inicio': '2026-10-16T14:30', 'quebra_fim': '2026-10-16T20:00', 'fim': '2026-10-17T21:15', 'mb_max': 4800, 'corte_mb': 700,
           'nota': 'Hora de Brasília. CSVs em UTC convertidos (−3 h). Horas do diário entre ~03h e ~04h45 trocadas pela hora do commit (git deste repositório).'},
  'textos': {
    'subtitulo': 'Os bastidores da construção do context hub, de 16/10 às 14h30 ao reinício do Windows, em 17/10 às 21h10. A largura do rio é a memória livre medida da máquina: onde ele estreita, o trabalho pesado encalha.',
    'como_ler': 'Role para baixo: o tempo desce. Passe o mouse ou toque em qualquer marca para ver o detalhe e a fonte.',
    'quebra_curta': '14h30 às 20h do dia 16: sem medida (escala comprimida)',
    'quebra': '16/10, 14h30 às 20h: revisão do spec e etapa 0, sem medida de memória (escala comprimida)',
    'fontes': 'Diário do maestro (etapas/diario-da-construcao.md), registro de junções, tickets (issues/*.md, ## Comments), pareceres e relatórios em etapas/, medidores e status em etapas/logs/ (CSVs em UTC, convertidos), fila-pesada.md, regras-da-construcao.md, retomada-maestro.md e o git dos dois repositórios. Algumas medidas vêm das worktrees do hub (C:/context-hub-wt/ticket-07 e ticket-25), marcadas no toque. Cada fato com a sua fonte em fatos-peca-2.json.'},
  'cores': {'Brasa': '#d4572a', 'Vela': '#d49a12', 'Trilho': '#5f7d2a', 'Cinzel': '#7a54a8', 'Rebite': '#5d6b78', 'Fiel': '#1f8a8a',
            'maestro': '#1f2a37', 'Lume': '#c75c95', 'Fielzinho': '#8a8a8a'},
  'numeros': numeros, 'memoria': memoria, 'cortes': cortes, 'pisos': pisos, 'trava': barcos, 'episodios_trava': episodios,
  'janelas': janelas, 'codex_inicio': '2026-10-16T20:00', 'codex': codex, 'comporta': comporta, 'reinicios': reinicios,
  'achados': achados, 'regras': regras, 'decisoes': decisoes,
  'fecho': {'t': '2026-10-17T20:17', 'curto': '20h17: construção fechada (suíte 370, 0 falhas)', 'titulo': 'Construção fechada',
            'texto': 'A prova do hub inteiro (ticket 25) resolvida; suíte 370: 355 verdes, 15 pulados, 0 falhas (ca62332). Só a instalação de verdade (ticket 26) fica, com o Gustavo.',
            'fonte': 'etapas/diario-da-construcao.md:196; etapas/registro-de-juncoes.md:44'},
  'foz': {'titulo': 'A foz: 20h17, construção fechada',
          'texto': 'A prova do hub inteiro (ticket 25) resolvida fecha a construção: a suíte final tem 370 testes, 355 verdes, 15 pulados, 0 falhas (ca62332). Às 21h10 o Windows reinicia; com todos religados, 714 MB livres; fechados os sem trabalho, 3,0 GB. Ficam para o Gustavo: apagar as 1.325 pastas antigas do %TEMP% (4,0 GB) e rever as decisões marcadas no rio (marcos cheios).',
          'fonte': 'etapas/diario-da-construcao.md:196; .scratch/context-hub/retomada-maestro.md:9,68-90,117'},
}
(AQUI / 'fatos-peca-2.json').write_text(json.dumps(fatos, ensure_ascii=False, indent=1), encoding='utf-8')
html = (AQUI / 'modelo-peca-2.html').read_text(encoding='utf-8')
emb = json.dumps(fatos, ensure_ascii=False).replace('</', '<\\/')
(AQUI / 'peca-2-rio-estreito.html').write_text(html.replace('/*FATOS*/', emb), encoding='utf-8')
print('memória', len(memoria), 'encalhes', len(cortes), 'barcos', len(barcos), 'pedras', len(achados),
      'placas', len(regras), 'marcos', len(decisoes), 'janelas', len(janelas), 'codex', len(codex))
