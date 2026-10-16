"""Painel do laço no chat do Maestri: a cada N minutos, manda o estado com `maestri say`.

Uso: python painel.py --minutos 10        (para sozinho quando o laço termina)
     python painel.py --uma-vez --pular-disparo   (pre-run da rotina "Painel do laço" do Maestri)
     python painel.py --uma-vez           (manda um estado e sai)
Não chama modelo nenhum: lê o banco, os livros-razão e o retrato do despachante.
"""
import argparse, glob, json, os, shutil, subprocess, time
from datetime import datetime, timedelta, timezone
from comum import abrir_banco, caminho, ler_controle

BRT = timezone(timedelta(hours=-3))


def hora(ts):
    return datetime.fromtimestamp(ts, BRT).strftime("%H:%M")


def estado():
    con = abrir_banco()
    onda = ler_controle(con, "onda", 1)
    teto = ler_controle(con, "teto") or {}
    hist = ler_controle(con, "historico", [])
    parar = ler_controle(con, "parar", False)
    tent = con.execute("SELECT COALESCE(SUM(tentativas),0) FROM uso").fetchone()[0]
    por_estado = dict(con.execute("""SELECT p.estado, COUNT(*) FROM pedidos p JOIN celulas c ON p.celula=c.id
                                     WHERE c.onda=? GROUP BY 1""", (onda,)).fetchall())
    try:
        d = json.load(open(caminho("estado", "despachante.json"), encoding="utf-8"))
    except OSError:
        d = {}
    agora, aceitos_10, chamadas_10, itens = time.time(), 0, 0, 0
    for f in glob.glob(caminho("livros", "*.jsonl")):
        for l in open(f, encoding="utf-8"):
            r = json.loads(l)
            itens += len(r.get("itens") or [])
            try:
                ts = datetime.strptime(r["ts"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc).timestamp()
            except (KeyError, ValueError):
                continue
            if agora - ts <= 600:
                chamadas_10 += 1
                aceitos_10 += r.get("estado") == "aceito"
    fim_teto = teto.get("inicio", agora) + (teto.get("horas") or 0) * 3600
    linhas = [f"**Laço da pesquisa ampla, {hora(agora)}**" + (" (terminou)" if parar else "")]
    abertos = sum(por_estado.get(k, 0) for k in ("pendente", "em_voo", "adiado"))
    linhas.append(f"- Onda {onda}: {por_estado.get('aceito', 0)} pedidos aceitos, {abertos} em aberto "
                  f"({por_estado.get('em_voo', 0)} em voo, {por_estado.get('adiado', 0)} adiados por cota).")
    linhas.append(f"- Últimos 10 min: {chamadas_10} chamadas, {aceitos_10} aceitas.")
    linhas.append(f"- Tentativas: {tent} de {teto.get('pedidos') or 'sem limite'}; o teto de horas vence às {hora(fim_teto)}.")
    linhas.append(f"- Modelos: {d.get('aptos')} aptos, {d.get('fora_agora')} fora por espera. Itens brutos: {itens}.")
    if hist:
        curva = "; ".join(f"onda {h['onda']}: {h['itens_total']} itens, {h['novos']} novos ({h['taxa_novos']:.0%})" for h in hist[-4:])
        linhas.append(f"- Curva: {curva}. O gate pede duas ondas seguidas abaixo de 5%.")
    else:
        linhas.append("- Curva: nenhuma onda fechada ainda.")
    return "\n".join(linhas), parar


def dizer(texto):
    exe = shutil.which("maestri") or os.environ.get("MAESTRI_CLI", "maestri")
    r = subprocess.run([exe, "say", texto], capture_output=True, text=True, check=False)
    env = {k: v for k, v in os.environ.items() if k.startswith("MAESTRI")}
    with open(caminho("logs", "painel.log"), "a", encoding="utf-8") as f:
        f.write(f"{datetime.now(BRT):%H:%M:%S} exe={exe} rc={r.returncode} out={r.stdout.strip()[:200]} "
                f"err={r.stderr.strip()[:300]} env={env}\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--minutos", type=float, default=10)
    ap.add_argument("--uma-vez", action="store_true")
    ap.add_argument("--pular-disparo", action="store_true",
                    help="sai com código 1: como pre-run de uma rotina do Maestri, manda o estado e impede o disparo")
    ap.add_argument("--dados-segundos", type=float, default=60, help="de quanto em quanto grava painel/dados.js")
    a = ap.parse_args()
    import painel_dados
    ultimo_chat = 0.0
    while True:
        try:
            painel_dados.gravar()
        except Exception as e:  # o painel visual nunca derruba o aviso do chat
            print("dados.js falhou:", repr(e), flush=True)
        texto, parar = estado()
        if time.time() - ultimo_chat >= a.minutos * 60 - 1 or a.uma_vez or parar:
            dizer(texto)
            ultimo_chat = time.time()
        if a.uma_vez or parar:
            break
        time.sleep(a.dados_segundos)
    if a.pular_disparo:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
