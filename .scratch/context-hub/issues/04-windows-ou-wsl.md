# Windows ou WSL

Type: grilling
Status: resolved
Blocked by: 03, 05

## Question

Onde o hub mora em cada máquina: no sistema de arquivos do Windows ou dentro do WSL? A resposta
também decide o caminho do hub real (`C:\context-hub` ou WSL; §12 da exploração).

## Comments

- 2026-10-01: rodada 1 em `respostas.md` (Q1 motivo do WSL; Q2 onde os agentes rodam na máquina
  pessoal; Q3 onde o hub mora, recomendação NTFS nas duas). Fatos levantados no notebook: Claude Code
  e Codex instalados no Windows; OpenCode só no WSL (Ubuntu-24.04, via nvm); `~/.claude` do WSL com
  GSD e skills de 2026-09-17 a 2026-09-25; Obsidian e Tailscale fora do PATH do Windows.
- 2026-10-01, respostas da rodada 1:
  - **Q1:** ele supunha que o WSL fosse "mais versátil, flexível e recomendado" como store de
    persistência e consulta, "talvez eu esteja confundindo com docker". O OpenSSH nativo do Windows
    "pesa bastante". Sem saber ainda todos os casos de uso, prefere começar pelo Windows e repensar
    quando aparecer um caso de uso que exija o WSL.
  - **Q2:** na máquina pessoal tudo roda no Windows, e o OpenCode só no WSL. O OpenCode era o único
    caminho para os modelos do FreeLLMAPI, e agora ele usa esses modelos pelo Copilot no VS Code: "teoricamente
    todos rodam no windows". O Maestri roda no Windows ("eu acho").
  - **Q2, ideia registrada:** uma "luva anticongelamento": o agente só consulta o contexto pela camada
    de busca (MCP), sem buscar no hub do jeito que quiser, para economizar tokens. Ele mesmo duvida
    ("talvez o ganho seja só com arquivos muito grandes ou em grande quantidade"). Não é questão deste
    ticket: foi para "Como os agentes gravam no hub", que decide o acesso direto ao disco.
  - **Q3:** (a), NTFS nas duas máquinas.
- 2026-10-01: rodada 2 em `respostas.md` (Q4 o OpenCode no critério 1; Q5 o caminho nas duas máquinas).
- 2026-10-01, respostas da rodada 2:
  - **Q4:** (c). O OpenCode sai do critério 1 e o Copilot entra: "também uso o harness do copilot".
  - **Q5:** (a), `C:\context-hub` nas duas máquinas.
- 2026-10-01: rodada 3 em `respostas.md`, com a resposta final e as mudanças no mapa para confirmar.
- 2026-10-01, resposta da rodada 3: Q6 confirmada, e a pesquisa do Copilot cobre os dois ("pesquise
  dos 2"), o modo agente do VS Code e o CLI.

## Answer

Gustavo confirmou em 2026-10-01.

1. **O hub mora no NTFS, em `C:\context-hub`, nas duas máquinas.** Quase tudo que toca o hub roda no
   Windows: Obsidian, Claude Code, Codex, Copilot, Maestri, o OpenSSH do Windows, o Tailscale e o sync
   (Git Bash e Agendador do Windows). A regra da Microsoft é guardar os arquivos do lado de quem
   trabalha neles ("Hub no WSL: comportamento"). O caminho mora no perfil de cada máquina, e não no
   contrato.
2. **O WSL fica fora do hub por ora.** Ele só volta quando surgir um caso de uso que precise dele, e
   então entra como ticket novo. A ideia de que o WSL seria mais versátil como store não tem apoio nas
   pesquisas, e a comparação com o Docker não foi verificada.
3. **Os harnesses do critério 1 passam a ser o Claude Code, o Codex e o Copilot** (modo agente do VS
   Code e CLI). O OpenCode, que só rodava no WSL e servia para chegar ao FreeLLMAPI, sai. Voltar com
   ele significa só acrescentar um adaptador.

Consequências no mapa: o critério 1 do destino foi atualizado; nasceu a pesquisa "Acesso dos agentes:
Copilot", que bloqueia "Acesso dos agentes: decisão"; a ideia da "luva anticongelamento" foi para
"Como os agentes gravam no hub".
