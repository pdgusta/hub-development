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
    ('2026-10-16T23:05', 'fila Docker do 07 morta pelo sistema', 'd1-mem-docker-07'),
    ('2026-10-16T23:40', 'a fila do 07 morre de novo', 'd1-mem-docker-07'),
    ('2026-10-17T00:35', 'suíte da junção parou: memória crítica', 'd1-mem-suite-c1'),
    ('2026-10-17T03:59', 'Docker do 08 caiu aos 18 min', 'd2-mem-08-docker'),
    ('2026-10-17T05:12', 'fatia 2 do 08: 2.900 → 513 MB', 'd2-mem-08-fatia2-a'),
    ('2026-10-17T07:39', 'fatia 2 de novo: 3.183 → 621 MB', 'd2-mem-08-fatia2-b'),
    ('2026-10-17T08:26', 'Docker do 22 cortado: 613 MB', 'd2-mem-22-docker'),
    ('2026-10-17T13:01', '25, rodada 1: corte em 670 MB', 'd2-mem-25-piso'),
    ('2026-10-17T13:13', '25, rodada 2: corte em 480 MB', 'd2-mem-25-piso'),
    ('2026-10-17T13:39', '25, fase 7: corte em 671 MB', 'd2-mem-25-fase7'),
    ('2026-10-17T14:17', '25, fase 4: corte antes de começar (477 MB)', None),
    ('2026-10-17T15:33', 'Codex do 22 cortado: 583 MB', 'd2-mem-22-codex'),
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
    codex.append({'ini': ini, 'fim': fim, 'curto': f'sem cota até {fim[11:16].replace(":", "h")}' + (' (Gustavo redefiniu)' if '14:26' in c['volta'] else ''),
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
 'd1-05-intermitente': 'teste do 05 falhou uma vez na junção',
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
 'd2-08-fatia3-falso-passa': 'PASSA sem ter o que conferir (08)',
 'd2-10-docker-crlf': 'teste do 10 esperava LF, veio CRLF',
 'd2-16-caminho-ofuscado': 'caminho ofuscado escondia a folha',
 'd2-10-npm-test-zero': 'npm test rodou 0 testes e deu verde',
 'd2-15-hifen-sublinhado': 'Codex troca hífen por sublinhado',
 'd2-10-temp-curto-fork': 'TEMP em nome curto: 20 testes caem',
 'd2-11-codex-trava-teste': 'Codex travava o processo do teste',
 'd2-18-cobrava-quem-nao-gravou': 'o fim cobrava quem não gravou (18)',
 'd2-21-eperm-rename': 'rename com EPERM ao arquivar',
 'd2-22-frase-no-stderr': 'frase esperada no stdout veio no stderr',
 'd2-25-fase2-tasks': 'teste citava linha já trocada (25)',
 'd2-21-caminho-curto-fswatch': 'caminho curto do Windows aborta o node',
 'd2-16-skill-md-yaml': 'YAML quebrado: junção do 16 desfeita',
 'd2-23-fazer-apaga-original': 'o desfazer apagava o arquivo original',
 'd2-40-roteamento-fora-do-agents': 'roteamento do 19 fora do AGENTS.md',
 'd2-docs-busca-prazo': 'busca estourou o prazo com os docs',
 'd2-22-trust-level': 'kit apagava o trust_level do Codex',
 'd2-42-mod-pelo-atalho': 'mod não via o hub aberto pelo atalho',
 'd2-25-ponte-ramo-errado': 'ponte do 25 no ramo errado do fork',
 'd2-25-nota-nao-desce': 'a nota não descia do par A ao B',
 'd2-27-link-em-codigo-inline': 'link em código inline derruba o 27-pastas',
 'd2-23-eperm-intermitente': 'EPERM passageiro no kit, sob carga',
 'd2-25-fase7-pipe': 'fase 7 presa 28 min num pipe',
 'd2-25-fase2-codex-shell': 'o pedido proibia o shell do Codex',
 'd2-25-fase7-falso-verde': 'fase 7 "verde" sem rodar harness',
}
achados = []
for a in AC['achados']:
    if a['id'] not in CURTO: continue
    ta, tc = t(a['hora_achado']), t(a['hora_conserto'])
    if tc and ta and tc < ta: ta = tc  # conserto registrado antes da hora estimada do achado
    achados.append({'id': a['id'], 't': ta, 't_conserto': tc, 'curto': CURTO[a['id']], 'ticket': a['ticket'], 'quem': a.get('quem_achou'),
                    'quebrou': a['o_que_quebrou'], 'causa': a['causa'], 'conserto': a['conserto'],
                    'aprox': bool(a.get('hora_aproximada')), 'hora_texto': f"achado {a['hora_achado']}; conserto {a['hora_conserto']}",
                    'fontes': a['fontes']})
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
 'Fatia 2 do 08 com menos agentes': ('2026-10-17T09:25', 'fatia 2 com menos agentes abertos'),
 'Guardar os 3 reinícios': ('2026-10-17T10:18', 'guardar os 3 reinícios do Codex'),
 'Testes do Codex com o GPT 6.1 Sol': ('2026-10-17T11:38', 'testes do Codex com o GPT 6.1 Sol'),
 'Um agente só de documentação': ('2026-10-17T12:05', 'um documentador: Lume'),
 'Codex sem cota não para nada': ('2026-10-17T14:28', 'sem cota, o Claude assume'),
 'Codex só para testes': ('2026-10-17T14:33', 'Codex só para testes; Fielzinho sai'),
 'O ticket 26 vira': ('2026-10-17T20:12', '26: instalar nas duas máquinas'),
}
GIT_HORA = {'d7a0f33': '03:19', '2e605d1': '03:23', '8493aaf': '03:25', '41fc0fb': '03:31'}
regras = []
for r in AC['regras_novas']:
    k = next((k for k in PLACA if r['regra'].startswith(k)), None)
    if not k: continue
    hora, curto = PLACA[k]
    regras.append({'t': hora, 'curto': curto, 'texto': r['regra'], 'quem': r['de_quem'], 'fonte': r['fonte']})
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
    decisoes.append({'t': hora, 'curto': curto, 'texto': r['regra'], 'ticket': 'processo', 'rever': False, 'rotulo': True, 'fonte': r['fonte']})
CURTO_D = {  # decisões "para rever": rótulo curto; hora pelo git quando o diário está adiantado
 'O hub-busca expõe só a search': ('2026-10-17T03:14', 'a busca expõe só a search'),
 'Pontos abertos da faixa 5': ('2026-10-17T03:29', 'faixa 5 do banco decidida (09)'),
 'O 16 começa antes': (None, '16 começa antes dos bloqueios'),
 "'Piora' = algum item": (None, '"piora" = item sobe de nível (16)'),
 'Achados aceitos: o LiveSync': (None, 'conflito só sem base viva (09)'),
 'O 17 começa antes': (None, '17 começa antes do 16'),
 'Vigia no Claude Code pela linha': (None, 'vigia na linha de status (17)'),
 'O 18 começa já': (None, '18 começa sobre o 17'),
 'Opção A:': (None, '18: opção A, muda o spec'),
 'O 23 começa antes': (None, '23 começa antes dos bloqueios'),
 'Binário descartado': (None, 'binário descartado = divergência (16)'),
 'O proxy não repassa': (None, 'proxy sem instructions: no radar (22)'),
 "Conserto candidato 'daemon": (None, '--interval 5: descartado às 18:50'),
 'O 25 fecha sem o Codex': (None, '25 fecha sem o Codex nas fases 4-7'),
 'Nota que não descia': (None, 'nota A→B: conserto só no teste'),
}
GITH = {'O 16 começa antes': '2026-10-17T04:25', "'Piora' = algum item": '2026-10-17T04:28', 'Achados aceitos: o LiveSync': '2026-10-17T04:44'}
for r in AC['decisoes_do_maestro']:
    if r['decisao'].startswith('Suíte inteira só na junção'): continue  # já é marco de regra
    k = next((k for k in CURTO_D if r['decisao'].startswith(k)), None)
    hora = (CURTO_D[k][0] if k and CURTO_D[k][0] else None) or GITH.get(k) or t(r['hora'])
    decisoes.append({'t': hora, 'curto': CURTO_D[k][1] if k else r['decisao'][:60], 'texto': r['decisao'], 'ticket': r['ticket'],
                     'rever': bool(r['para_rever']), 'rotulo': bool(k), 'fonte': r['fonte'] + (' (hora pelo git deste repositório)' if k in GITH or (k and CURTO_D[k][0]) else '')})
decisoes.sort(key=lambda d: d['t'])

numeros = [
    {'valor': '448 MB', 'rotulo': 'a menor memória livre medida (14h18)', 'destaque': True,
     'detalhe': 'Ronda das 14:18, com a fase 4 do ticket 25 (junção e prova do hub inteiro) rodando.', 'fonte': 'etapas/diario-da-construcao.md:159'},
    {'valor': str(len(cortes)), 'rotulo': 'encalhes: trabalho que caiu por falta de memória',
     'detalhe': 'Três mortos pelo sistema (fila Docker do 07, suíte das 00h35, Docker do 08) e nove cortes do medidor abaixo de 700 MB. Fontes de cada um no toque.', 'fonte': 'dados-memoria-trava.json (cortes)'},
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
            'texto': 'O ticket 25 resolvido; suíte 370: 355 verdes, 15 pulados, 0 falhas (ca62332). Só o 26 fica, com o Gustavo.',
            'fonte': 'etapas/diario-da-construcao.md:196; etapas/registro-de-juncoes.md:44'},
  'foz': {'titulo': 'A foz: 20h17, construção fechada',
          'texto': 'O ticket 25 resolvido fecha a construção: a suíte final tem 370 testes, 355 verdes, 15 pulados, 0 falhas (ca62332). Às 21h10 o Windows reinicia; com todos religados, 714 MB livres; fechados os sem trabalho, 3,0 GB. Ficam para o Gustavo: apagar as 1.325 pastas antigas do %TEMP% (4,0 GB) e rever as decisões marcadas no rio (marcos cheios).',
          'fonte': 'etapas/diario-da-construcao.md:196; .scratch/context-hub/retomada-maestro.md:9,68-90,117'},
}
(AQUI / 'fatos-peca-2.json').write_text(json.dumps(fatos, ensure_ascii=False, indent=1), encoding='utf-8')
html = (AQUI / 'modelo-peca-2.html').read_text(encoding='utf-8')
emb = json.dumps(fatos, ensure_ascii=False).replace('</', '<\\/')
(AQUI / 'peca-2-rio-estreito.html').write_text(html.replace('/*FATOS*/', emb), encoding='utf-8')
print('memória', len(memoria), 'encalhes', len(cortes), 'barcos', len(barcos), 'pedras', len(achados),
      'placas', len(regras), 'marcos', len(decisoes), 'janelas', len(janelas), 'codex', len(codex))
