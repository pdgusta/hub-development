"""Embute uma pasta de execução num .js, para abrir web/index.html direto do disco (file://, sem servidor).

O .js guarda o que o servidor responderia (/api/execucao) e o texto de cada arquivo de eventos; a página lê isso
com a mesma reconstrução do modo HTTP (web/leitor.js, FonteEmbutida). "agora" fixa o relógio da fixture: na página ele
começa ali e anda.

Uso:  python -I fixture/embutir.py PASTA [SAIDA.js] [--agora ISO]
"""
import json
import os
import sys
sys.dont_write_bytecode = True

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(AQUI))
import servidor  # noqa: E402


def embutir(pasta, saida, agora=None):
    api = servidor.execucao(pasta)
    edir = os.path.join(pasta, 'eventos')
    eventos = {}
    for n in sorted(os.listdir(edir)) if os.path.isdir(edir) else []:
        if n.endswith('.jsonl'):
            with open(os.path.join(edir, n), 'rb') as f:
                eventos[n[:-6]] = f.read().decode('utf-8', errors='replace')
    dados = {'agora': agora, 'execucao': api, 'eventos': eventos}
    with open(saida, 'w', encoding='utf-8', newline='\n') as f:
        f.write('// gerado por fixture/embutir.py a partir de %s; não editar\n' % os.path.basename(os.path.normpath(pasta)))
        f.write('window.PAINEL_EMBUTIDO=' + json.dumps(dados, ensure_ascii=False) + ';\n')
    print('embutida em', saida)


if __name__ == '__main__':
    args = [a for a in sys.argv[1:]]
    agora = None
    if '--agora' in args:
        i = args.index('--agora'); agora = args[i + 1]; del args[i:i + 2]
    embutir(args[0], args[1] if len(args) > 1 else os.path.join(AQUI, 'embutida.js'), agora)
