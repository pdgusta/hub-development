"""Servidor do painel da construção (contrato.md, seções 1 e 8).

Só lê. Só GET. Só 127.0.0.1. Serve a página (painel/web/) e entrega a pasta da execução em JSON:
  GET /api/execucao                      execucao.json + tickets + quem tem arquivo de eventos
  GET /api/eventos?c=agente:byte,...     só as linhas novas de cada arquivo desde o cursor
Não interpreta eventos: a reconstrução é do navegador (web/leitor.js).

Uso:  python servidor.py [--fixture | --pasta CAMINHO] [--tickets CAMINHO] [--porta 8771]
"""
import argparse
import json
import mimetypes
import os
import re
import sys
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, unquote, urlsplit

AQUI = os.path.dirname(os.path.abspath(__file__))
WEB = os.path.join(AQUI, 'web')
REAL = os.path.normpath(os.path.join(AQUI, '..', 'execucao'))
ISSUES = os.path.normpath(os.path.join(AQUI, '..', 'issues'))  # os tickets moram aqui (convenção do repositório)
FIXTURE = os.path.join(AQUI, 'fixture', 'execucao-fake')
ID = re.compile(r'^[a-z0-9-]+$')
TICKET = re.compile(r'^(\d+)-[^/\\]+\.md$')
MAX_RESPOSTA = 4 * 1024 * 1024  # um pedido de eventos não passa disso; o resto vem no próximo
mimetypes.add_type('text/javascript', '.js')


def agora():
    return datetime.now(timezone.utc).astimezone().isoformat(timespec='seconds')


def ler_texto(caminho):
    with open(caminho, 'rb') as f:
        return f.read().decode('utf-8', errors='replace')


def cabecalho(texto):
    """As linhas do topo do ticket, até a primeira seção."""
    campos, titulo = {}, None
    for linha in texto.splitlines()[:40]:
        if titulo is None and linha.startswith('# '):
            titulo = linha[2:].strip()
            continue
        if linha.startswith('## '):
            break
        m = re.match(r'^([A-Za-z ]+):\s*(.*)$', linha)
        if m:
            campos.setdefault(m.group(1).strip().lower(), m.group(2).strip())
    return titulo, campos


def execucao(pasta, tdir=None):
    problemas, desc, tickets, agentes = [], None, [], []
    if not os.path.isdir(pasta):
        problemas.append({'arquivo': '', 'erro': 'sem-pasta', 'mensagem': 'a pasta da execução não existe (ainda)'})
    else:
        caminho = os.path.join(pasta, 'execucao.json')
        if os.path.isfile(caminho):
            try:
                desc = json.loads(ler_texto(caminho))
            except ValueError as e:
                problemas.append({'arquivo': 'execucao.json', 'erro': 'json', 'mensagem': 'não é JSON: %s' % e})
        else:
            problemas.append({'arquivo': 'execucao.json', 'erro': 'falta', 'mensagem': 'execucao.json não existe'})
        tdir = tdir or os.path.join(pasta, 'tickets')
        for nome in sorted(os.listdir(tdir)) if os.path.isdir(tdir) else []:
            m = TICKET.match(nome)
            if not m:
                continue
            try:
                texto = ler_texto(os.path.join(tdir, nome))
            except OSError as e:
                problemas.append({'arquivo': 'tickets/' + nome, 'erro': 'leitura', 'mensagem': str(e)})
                continue
            titulo, c = cabecalho(texto)
            tickets.append({'arquivo': nome, 'numero': m.group(1), 'titulo': titulo, 'status': c.get('status'),
                            'dono': c.get('dono'), 'com': c.get('com') or None,
                            'blocked_by': re.findall(r'\d+', c.get('blocked by', '')), 'texto': texto})
        edir = os.path.join(pasta, 'eventos')
        for nome in sorted(os.listdir(edir)) if os.path.isdir(edir) else []:
            if nome.endswith('.jsonl') and ID.match(nome[:-6]):
                agentes.append(nome[:-6])
    return {'lido_em': agora(), 'execucao': desc, 'tickets': tickets, 'agentes_com_arquivo': agentes,
            'problemas': problemas}


def eventos(pasta, cursores):
    arquivos, problemas, total = {}, [], 0
    edir = os.path.join(pasta, 'eventos')
    nomes = list(cursores) if cursores else [n[:-6] for n in (os.listdir(edir) if os.path.isdir(edir) else [])
                                              if n.endswith('.jsonl') and ID.match(n[:-6])]
    for ag in nomes:
        if not ID.match(ag):
            problemas.append({'arquivo': ag, 'erro': 'id', 'mensagem': 'id de agente inválido'})
            continue
        caminho = os.path.join(edir, ag + '.jsonl')
        if not os.path.isfile(caminho):
            continue
        de = cursores.get(ag, 0)
        tam = os.path.getsize(caminho)
        recomecou = de > tam
        if recomecou:
            de = 0
        with open(caminho, 'rb') as f:
            f.seek(de)
            bruto = f.read(max(0, MAX_RESPOSTA - total))
        fim = bruto.rfind(b'\n')  # para na última linha completa
        bruto = bruto[:fim + 1] if fim >= 0 else b''
        total += len(bruto)
        linhas, pos = [], de
        for crua in bruto.split(b'\n')[:-1]:
            n = pos
            pos += len(crua) + 1
            if not crua.strip():
                continue
            try:
                linhas.append(json.loads(crua.decode('utf-8')))
            except ValueError:
                problemas.append({'arquivo': 'eventos/%s.jsonl' % ag, 'erro': 'linha', 'byte': n,
                                  'mensagem': 'linha que não é JSON'})
        arquivos[ag] = {'ate': de + len(bruto), 'linhas': linhas, 'recomecou': recomecou}
    return {'lido_em': agora(), 'arquivos': arquivos, 'problemas': problemas}


class Painel(BaseHTTPRequestHandler):
    pasta = REAL
    tickets = ISSUES
    server_version = 'painel-construcao/1'

    def log_message(self, fmt, *args):
        pass

    def enviar(self, codigo, corpo, tipo='application/json; charset=utf-8'):
        if isinstance(corpo, (dict, list)):
            corpo = json.dumps(corpo, ensure_ascii=False).encode('utf-8')
        self.send_response(codigo)
        self.send_header('Content-Type', tipo)
        self.send_header('Content-Length', str(len(corpo)))
        self.send_header('Cache-Control', 'no-store')
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.end_headers()
        self.wfile.write(corpo)

    def erro(self, codigo, erro, mensagem):
        self.enviar(codigo, {'erro': erro, 'mensagem': mensagem})

    def do_GET(self):
        url = urlsplit(self.path)
        caminho = unquote(url.path)
        # contra rebinding de DNS: só atende quem chamou pelo nome local e pela porta certa
        porta = self.server.server_address[1]
        if (self.headers.get('Host') or '').lower() not in ('127.0.0.1:%d' % porta, 'localhost:%d' % porta):
            return self.erro(403, 'host', 'abra pelo endereço local: http://127.0.0.1:%d/' % porta)
        try:
            if caminho in ('/', ''):
                self.send_response(302)
                self.send_header('Location', '/web/')
                self.send_header('Content-Length', '0')
                self.end_headers()
                return
            if caminho == '/web/':
                caminho = '/web/index.html'
            if caminho == '/api/execucao':
                return self.enviar(200, execucao(self.pasta, self.tickets))
            if caminho == '/api/eventos':
                cur = {}
                for par in ','.join(parse_qs(url.query).get('c', [])).split(','):
                    if not par:
                        continue
                    ag, _, b = par.partition(':')
                    if not ID.match(ag) or not (b or '0').isdigit():
                        return self.erro(400, 'cursor', 'cursor inválido: %s' % par)
                    cur[ag] = int(b or 0)
                return self.enviar(200, eventos(self.pasta, cur))
            if caminho.startswith('/web/'):
                alvo = os.path.normpath(os.path.join(WEB, caminho[5:]))
                if os.path.commonpath([alvo, WEB]) == WEB and os.path.isfile(alvo):
                    tipo = mimetypes.guess_type(alvo)[0] or 'application/octet-stream'
                    if tipo.startswith('text/'):
                        tipo += '; charset=utf-8'
                    with open(alvo, 'rb') as f:
                        return self.enviar(200, f.read(), tipo)
            return self.erro(404, 'nao-achado', 'não existe: %s' % caminho)
        except Exception as e:  # o painel nunca derruba nada; responde o erro e segue
            return self.erro(500, 'interno', str(e))

    def nao(self):
        self.erro(405, 'so-leitura', 'o painel só lê')

    do_POST = do_PUT = do_DELETE = do_PATCH = nao


def main():
    p = argparse.ArgumentParser(description='Painel da construção (só leitura)')
    p.add_argument('--fixture', action='store_true', help='lê painel/fixture/execucao-fake/')
    p.add_argument('--pasta', help='outra pasta de execução')
    p.add_argument('--tickets', help='pasta dos tickets (padrão: ../issues; com --fixture ou --pasta, a subpasta tickets/)')
    p.add_argument('--porta', type=int, default=8771)
    a = p.parse_args()
    Painel.pasta = os.path.abspath(a.pasta) if a.pasta else FIXTURE if a.fixture else REAL
    Painel.tickets = os.path.abspath(a.tickets) if a.tickets else ISSUES if Painel.pasta == REAL else os.path.join(Painel.pasta, 'tickets')
    srv = ThreadingHTTPServer(('127.0.0.1', a.porta), Painel)
    print('painel em http://127.0.0.1:%d/ lendo %s (tickets em %s)' % (a.porta, Painel.pasta, Painel.tickets), flush=True)
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    sys.exit(main())
