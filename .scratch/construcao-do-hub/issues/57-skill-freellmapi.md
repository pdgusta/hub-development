# 57: Skill do hub que liga o FreeLLMAPI sob demanda

Type: task
Status: ready-for-agent
Etapa: depois do FreeLLMAPI nativo no par B (2026-10-24)
Blocked by: nenhum

**What to build:** Pedido do Gustavo (2026-10-24 ~18h05): o FreeLLMAPI **não** fica preso a uma sessão nem sobe no
logon. Uma skill do hub, que qualquer agente (Claude Code, Codex, Copilot) usa, liga o servidor **sob demanda** por
script, e ele fica no ar sem depender de nenhuma sessão. Hoje ele roda nativo no par B (`lenovo-ideapad`), v0.11.0
(955e9cf), clone em `C:\Projetos\freellmapi`, banco e `.env` em `C:\freellmapi-data\`, `HOST=0.0.0.0` com a regra do
firewall "FreeLLMAPI (só tailnet)" (TCP 3001, `100.64.0.0/10`). O par A o chama por `FREELLM_BASE_URL`
(`http://100.121.86.61:3001`). Decisão anterior: ticket 16 do planejamento, comentário de 2026-10-14 (nativo, sem
Docker). Histórico: `.scratch/context-hub/retomada-maestro-par-b.md`, diário de 2026-10-24.

- [ ] skill `agents/skills/freellmapi/` (`metadata.camada: geral`, vai às pastas globais pelo 08), escrita com a skill
  `writing-for-agents`; linha no `agents/skills/routing.yml`
- [ ] script com três verbos: `estado` (`GET /api/ping` em `FREELLM_BASE_URL`, ou `http://127.0.0.1:3001`), `ligar`
  (já no ar: não faz nada; não está nesta máquina: diz em que par ele mora e manda pedir ao maestro de lá pelo
  `correio`; está aqui: sobe, espera o ping e diz o resultado) e `desligar` (só o processo que ele subiu)
- [ ] o processo sobe **fora da árvore da sessão** que chamou, para não morrer quando ela fechar. Candidato:
  `Win32_Process.Create` (o pai passa a ser o serviço do WMI). Fonte primária antes; não verificado se o
  `detached` do Node basta com o Claude Code, o Codex e o Copilot
- [ ] o processo herda as variáveis do servidor (`NODE_ENV=production`, `HOST`, `FREEAPI_ENV_PATH`,
  `FREEAPI_DB_PATH`), o log vai para um arquivo e o PID para outro; o `desligar` confere a linha de comando antes de
  parar
- [ ] o que é desta máquina (clone, pasta de dados, porta) fica fora do que replica (`.local/` do hub ou a pasta de
  dados); nada de chave no hub, no log do agente ou na resposta
- [ ] sem tarefa agendada e sem início no logon. Depois da junção: parar o processo de hoje e apagar
  `C:\freellmapi-data\iniciar.ps1`
- [ ] testes (servidor falso numa porta livre: `estado`, `ligar` duas vezes sobe um só, `desligar`) e a doc em
  `agents/code/docs/`

Fora deste ticket: a `FREELLM_API_KEY` do par B (o Gustavo copia do painel) e a reserva do A em
`C:\hub-transporte\freellmapi-do-a\` (apagar quando a skill passar).

## Comments

- 2026-10-24 (maestro do B): aberto a pedido do Gustavo. Dono: maestro do par B.
