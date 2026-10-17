#!/usr/bin/env bash
# Fiel: Docker da revisão do 10 (rodada 2), com a trava pesada: o teste do 10 e o do 09 com o fork do 10.
E=C:/Projetos/context-hub/.scratch/construcao-do-hub/etapas
T=$E/trava-pesada.md
L=$E/logs
if [ -f "$T" ]; then echo "trava ocupada:"; cat "$T"; exit 9; fi
echo "- Fiel (revisor), 2026-10-17 $(date +%H:%M): Docker da revisão do 10 (10-mcp-banco.test.ps1 e 09-mcp-banco.test.ps1, hub-ensaio-10-a/b e hub-ensaio-09-a/b, 5996/5997, MCP 8796-8798). Apago ao fim." > "$T"
trap 'rm -f "$T"; echo "trava apagada $(date +%H:%M)"' EXIT
export HUB_MCP_BANCO_DIR='C:\Projetos\hub-mcp-banco-wt\ticket-10'
echo "== 10 $(date +%H:%M)"
(cd C:/context-hub-wt/ticket-10 && pwsh -NoProfile -File agents/code/test/10-mcp-banco.test.ps1) > $L/revisao-10-r2-docker.log 2>&1
echo "10 saida=$?"
echo "== 09 com o fork do 10 $(date +%H:%M)"
(cd C:/context-hub-wt/ticket-10 && pwsh -NoProfile -File agents/code/test/09-mcp-banco.test.ps1) > $L/revisao-10-r2-docker-09.log 2>&1
echo "09 saida=$?"
echo "== sobras"
docker ps -a --format '{{.Names}}' | grep hub-ensaio || echo "nenhum conteiner hub-ensaio"
