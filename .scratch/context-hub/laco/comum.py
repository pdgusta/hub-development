"""Peças comuns do laço da pesquisa ampla: configuração, banco de estado (SQLite), chamadas ao gateway.

Todos os scripts (despachante, gerador, juntador, plano) abrem o mesmo banco `estado/laco.db`.
O SQLite em modo WAL aguenta vários processos; toda escolha de modelo acontece dentro de uma
transação `BEGIN IMMEDIATE`, então dois geradores nunca gastam a mesma folga de cota.
"""
import json, os, re, sqlite3, time, urllib.error, urllib.parse, urllib.request
from datetime import datetime, timedelta, timezone

AQUI = os.path.dirname(os.path.abspath(__file__))


def caminho(*partes):
    return os.path.join(AQUI, *partes)


def carregar_config():
    with open(caminho("config.json"), encoding="utf-8") as f:
        cfg = json.load(f)
    with open(caminho("plano.json"), encoding="utf-8") as f:
        cfg["metades_da_divisao"] = json.load(f)["metades_da_divisao"]
    cfg["chave"] = segredo(cfg["variavel_chave"])
    cfg["token_painel"] = segredo(cfg["variavel_token_painel"])
    return cfg


def segredo(nome):
    """Lê a variável do ambiente; no Windows, cai para a variável de usuário (o Git Bash não a herda)."""
    v = os.environ.get(nome)
    if v:
        return v
    if os.name == "nt":
        import winreg
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment") as k:
                return winreg.QueryValueEx(k, nome)[0]
        except OSError:
            pass
    raise SystemExit(f"variável {nome} não encontrada")


def agora():
    return time.time()


def iso(ts=None):
    return datetime.fromtimestamp(ts or agora(), timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


# ---------------------------------------------------------------- banco

ESQUEMA = """
CREATE TABLE IF NOT EXISTS modelos (
  id TEXT PRIMARY KEY,          -- id do catálogo, o que vai no campo "model"
  plataforma TEXT, pool TEXT, familia TEXT,
  rpm INTEGER, rpd INTEGER, chaves INTEGER,
  aceita_rf INTEGER DEFAULT 0,  -- aceitou response_format na bancada
  raciocina INTEGER DEFAULT 0,  -- precisa de max_tokens alto
  status TEXT,                  -- execution_status do gateway
  excluido TEXT,                -- motivo, se não deve receber pedidos
  fora_ate REAL DEFAULT 0,      -- espera depois de falhas ou 429
  falhas_seguidas INTEGER DEFAULT 0,
  acertos INTEGER DEFAULT 0, erros INTEGER DEFAULT 0,
  em_voo INTEGER DEFAULT 0,
  atualizado TEXT
);
CREATE TABLE IF NOT EXISTS uso (       -- tentativas por modelo em cada janela diária
  modelo TEXT, janela TEXT, tentativas INTEGER DEFAULT 0,
  PRIMARY KEY (modelo, janela)
);
CREATE TABLE IF NOT EXISTS ritmo (     -- instantes das chamadas recentes, para o limite por minuto
  chave TEXT, ts REAL
);
CREATE INDEX IF NOT EXISTS ritmo_chave ON ritmo(chave, ts);
CREATE TABLE IF NOT EXISTS celulas (
  id TEXT PRIMARY KEY, onda INTEGER, grupo TEXT, lingua TEXT, angulo TEXT,
  origem TEXT,                  -- plano, bola-de-neve, divisao, calibracao
  prompt TEXT, profundidade INTEGER DEFAULT 0,
  estado TEXT DEFAULT 'pendente'  -- pendente, concluida, esgotada, cancelada
);
CREATE TABLE IF NOT EXISTS pedidos (
  id TEXT PRIMARY KEY, celula TEXT, vaga INTEGER,   -- vaga 0 e 1: os dois modelos do par
  estado TEXT DEFAULT 'pendente',
  -- pendente, em_voo, aceito, adiado, esgotado, dividido, cancelado
  modelo TEXT, tentados TEXT DEFAULT '[]', reenvios INTEGER DEFAULT 0, erro_ultimo TEXT,
  proximo_em REAL DEFAULT 0, em_voo_desde REAL, gerador TEXT
);
CREATE INDEX IF NOT EXISTS pedidos_estado ON pedidos(estado, proximo_em);
CREATE TABLE IF NOT EXISTS controle (chave TEXT PRIMARY KEY, valor TEXT);
"""


def abrir_banco():
    os.makedirs(caminho("estado"), exist_ok=True)
    con = sqlite3.connect(caminho("estado", "laco.db"), timeout=60, isolation_level=None)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA journal_mode=WAL")
    con.execute("PRAGMA busy_timeout=60000")
    con.executescript(ESQUEMA)
    return con


def ler_controle(con, chave, padrao=None):
    r = con.execute("SELECT valor FROM controle WHERE chave=?", (chave,)).fetchone()
    return json.loads(r["valor"]) if r else padrao


def gravar_controle(con, chave, valor):
    con.execute("INSERT INTO controle VALUES (?,?) ON CONFLICT(chave) DO UPDATE SET valor=excluded.valor",
                (chave, json.dumps(valor, ensure_ascii=False)))


def anexar(arquivo, registro):
    """Livro-razão: JSONL só de acréscimo."""
    os.makedirs(os.path.dirname(arquivo), exist_ok=True)
    with open(arquivo, "a", encoding="utf-8") as f:
        f.write(json.dumps(registro, ensure_ascii=False) + "\n")


# ---------------------------------------------------------------- gateway

def http(cfg, metodo, rota, corpo=None, painel=False, timeout=150):
    """Devolve (status, cabeçalhos, json). Nunca levanta exceção de rede: status None e o erro no json."""
    tok = cfg["token_painel"] if painel else cfg["chave"]
    req = urllib.request.Request(cfg["gateway"] + rota, method=metodo,
                                 data=json.dumps(corpo).encode() if corpo is not None else None,
                                 headers={"Authorization": "Bearer " + tok, "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as f:
            return f.status, dict(f.headers), json.load(f)
    except urllib.error.HTTPError as e:
        try:
            d = json.loads(e.read().decode("utf-8", "replace"))
        except Exception:
            d = {}
        return e.code, dict(e.headers or {}), d
    except Exception as e:
        return None, {}, {"error": {"message": f"{type(e).__name__}: {e}"}}


def cabecalho(h, nome):
    for k, v in h.items():
        if k.lower() == nome.lower():
            return urllib.parse.unquote(v)
    return None


# ---------------------------------------------------------------- famílias e janelas

FAMILIAS = [  # ordem importa: o primeiro padrão que casa vence
    ("gemini", r"gemini"), ("gemma", r"gemma|diffusiongemma|sea-lion"), ("gpt-oss", r"gpt-oss"),
    ("nemotron", r"nemotron"), ("llama", r"llama|muse"), ("mistral", r"mistral|ministral|codestral|voxtral|devstral|magistral|pixtral"),
    ("qwen", r"qwen|qwq"), ("deepseek", r"deepseek"), ("glm", r"glm|z-ai|zai"), ("granite", r"granite"),
    ("cohere", r"command|north|aya|c4ai"), ("phi", r"\bphi"), ("kimi", r"kimi|moonshot"), ("minimax", r"minimax"),
    ("hunyuan", r"hunyuan|hy3|tencent"), ("agnes", r"agnes"), ("poolside", r"poolside|laguna"), ("liquid", r"lfm|liquid"),
]


def familia(modelo_id):
    s = modelo_id.lower()
    for nome, padrao in FAMILIAS:
        if re.search(padrao, s):
            return nome
    return re.split(r"[-/:@._]", s.strip("@"))[0] or s


def janela(cfg, plataforma, ts=None):
    """Início da janela diária da plataforma, em UTC (ex.: Google vira às 07:00 UTC = 04:00 BRT)."""
    hora = cfg["virada_utc"].get(plataforma, cfg["virada_utc"]["padrao"])
    t = datetime.fromtimestamp(ts or agora(), timezone.utc)
    ini = t.replace(hour=hora, minute=0, second=0, microsecond=0)
    if t < ini:
        ini -= timedelta(days=1)
    return ini.strftime("%Y-%m-%dT%H")


# ---------------------------------------------------------------- respostas

def extrair_json(texto):
    t = (texto or "").strip()
    if t.startswith("```"):
        t = t.strip("`")
        t = t[t.find("{"):] if "{" in t else t
    try:
        return json.loads(t)
    except Exception:
        pass
    a, b = t.find("{"), t.rfind("}")
    if a >= 0 and b > a:
        try:
            return json.loads(t[a:b + 1])
        except Exception:
            return None
    return None
