#!/usr/bin/env bash
# Fiel: Docker das revisões do 28 (rodada 3) e do 09 (rodada 1), numa vez só, com a trava pesada.
E=C:/Projetos/context-hub/.scratch/construcao-do-hub/etapas
T=$E/trava-pesada.md
L=$E/logs
if [ -f "$T" ]; then echo "trava ocupada:"; cat "$T"; exit 9; fi
echo "- Fiel (revisor), 2026-10-17 $(date +%H:%M): Docker das revisões do 28 (28-pastas-locais.test.ps1, hub-ensaio-28-a/b) e do 09 (fork e2e hub-ensaio-09-f 5996 + sonda; hub 09-mcp-banco.test.ps1, hub-ensaio-09-a/b 5996/5997). Apago ao fim." > "$T"
trap 'rm -f "$T"; echo "trava apagada $(date +%H:%M)"' EXIT

echo "== 28 $(date +%H:%M)"
(cd C:/context-hub-wt/ticket-28 && pwsh -NoProfile -File agents/code/test/28-pastas-locais.test.ps1) > $L/revisao-28-r3-docker.log 2>&1
echo "28 saida=$?"
echo "== 09 fork $(date +%H:%M)"
(cd C:/Projetos/hub-mcp-banco && node scripts/e2e-banco.mjs test/versao.e2e.test.ts "$L/sonda-09-fiel.e2e.test.ts") > $L/revisao-09-r1-fork.log 2>&1
echo "09 fork saida=$?"
echo "== 09 fork conserto $(date +%H:%M)"
(cd C:/Projetos/hub-mcp-banco-wt/conserto-09 && node scripts/e2e-banco.mjs test/versao.e2e.test.ts "$L/sonda-09-fiel.e2e.test.ts") > $L/revisao-09-conserto-fork.log 2>&1
echo "09 fork conserto saida=$?"
echo "== 09 hub conserto $(date +%H:%M)"
(cd C:/context-hub-wt/conserto-09 && HUB_MCP_BANCO_DIR='C:\Projetos\hub-mcp-banco-wt\conserto-09' pwsh -NoProfile -File agents/code/test/09-mcp-banco.test.ps1) > $L/revisao-09-conserto-hub.log 2>&1
echo "09 hub saida=$?"
echo "== sobras"
docker ps -a --format '{{.Names}}' | grep hub-ensaio || echo "nenhum conteiner hub-ensaio"
ls -d "$LOCALAPPDATA"/Temp/hub-ensaio-* 2>/dev/null || echo "nenhuma pasta hub-ensaio em TEMP"
