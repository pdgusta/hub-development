"""Roda changes.mjs com a autenticacao do CouchDB do spike (lida pelo cdb.py do proprio spike; nao e impressa).
Com --e2ee, passa tambem a passphrase de teste lida do settings.json do CLI de teste (E2EE_SETTINGS; nao e impressa).
Uso: python lancar-changes.py <banco> [args do changes.mjs...]   (env ROBUSTA_DB opcional)"""
import json, os, subprocess, sys
sys.path.insert(0, r"C:\Projetos\spike-livesync")
import cdb
env = dict(os.environ, COUCH_AUTH=cdb.AUTH)
if "--e2ee" in sys.argv:
    sf = os.environ.get("E2EE_SETTINGS", r"C:\Projetos\bancada-busca\robusta\cli-e2ee\.livesync\settings.json")
    with open(sf, encoding="utf-8") as f:
        env["E2EE_PASSPHRASE"] = json.load(f)["passphrase"]
here = os.path.dirname(os.path.abspath(__file__))
sys.exit(subprocess.run(["node", os.path.join(here, "changes.mjs"), *sys.argv[1:]], env=env).returncode)
