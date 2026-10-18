# Retomada do maestro do par B (lenovo-ideapad)

Só o maestro desta máquina escreve aqui. A do par A é `.scratch/context-hub/retomada-maestro.md`: leia, não escreva
nela. Regras de convivência: `.scratch/context-hub/onboarding-maestro.md` §2.

## Estado (2026-10-17 ~23h35)

- Onboarding lido; memórias copiadas para `~/.claude/projects/C--Projetos-context-hub/memory/`.
- Gustavo: o **mandato** vale também para este maestro; este maestro também faz **push** deste repositório.
- Identidade do git nesta máquina: `pdgusta <gustavopottpott@hotmail.com>` no local deste repositório **e no global**
  (pedido do Gustavo, ~23h30: aqui o global também é o dele; no par A o global é do trabalho e fica intocado).
- Ainda não há `C:\context-hub` aqui. Canvas do Maestri: só o maestro.
- Frente: ainda não definida pelo Gustavo. Candidata: preparar o par B do ticket 26.

## O que esta máquina precisa para o par B (resumo dado ao Gustavo; nada instalado nem conferido ainda)

Fonte: `.scratch/construcao-do-hub/etapas/roteiro-26.md` §3 e o comentário de 22h20 do ticket 26.
- winget: Tailscale.Tailscale, Docker.DockerDesktop, OpenJS.NodeJS.LTS (Node 22+), Python.Python.3.12,
  Microsoft.PowerShell (git já existe).
- Modo de desenvolvedor do Windows ligado; nenhum `CLAUDE.md` no hub nem acima.
- Do par A: clone do hub em `C:\context-hub` (depois da junção no `main` e do push do Gustavo); em `C:\hub-transporte\`
  o `.env` do par B (à mão) e os dois `git bundle` (fork do MCP do banco e CLI do LiveSync).
- Aberto: se o Codex e o Copilot precisam estar instalados aqui (o kit liga os três harnesses; não verificado).
- Guia: `agents/code/docs/instalacao.md`, a escrever pelo Lume depois do 45 e do 46.

### Conferido em 2026-10-17 ~23h45 (Gustavo instalou; maestro conferiu só por leitura)

Tailscale 1.104.1 (lenovo-ideapad 100.121.86.61; vê o armis00323 100.120.188.50), Docker 29.8.2 (Desktop desligado:
servidor não responde, ligar quando um teste pedir), Node 24.20.0, Python 3.12.10, PowerShell 7.6.7, git 2.55.0,
Codex 0.163.0 (npm), Claude Code 2.1.302; modo de desenvolvedor ligado; sem `C:\CLAUDE.md`. **Copilot CLI ausente**
(nem `copilot` no PATH nem pacote npm/winget).

### Global do maestro: o que falta aqui (conferido 2026-10-17 ~23h55, só leitura, contra `global-do-maestro/README.md`)

1. `settings.json`: tem `model: opus`, `modelSettings.claude-opus-5-5.effortLevel: high`, theme `dark-ansi`, hooks e
   statusLine do GSD, permissões do GSD. Faltam: `model: claude-opus-5-5`, `effortLevel: xhigh`,
   `autoCompactWindow: 600000`, `permissions.defaultMode: auto`, `enabledPlugins` (superpowers), `env`
   (`CLAUDE_CODE_PLUGIN_DIRS` com `C:\Users\gusta\...`), `skillOverrides`, `skipDangerousModePermissionPrompt`,
   `skipWorkflowUsageWarning`, `editorMode`.
2. `~/.claude/CLAUDE.md`: não existe (falta a seção do graphify).
3. `~/.claude/mods/`: não existe (faltam contexto-agentes e guarda-de-recrutas).
4. Skills: só GSD (72) e Maestri (7). Faltam as do Matt Pocock em escopo de usuário (aqui há só o plugin
   `mattpocock-skills` com escopo de projeto no pmo-tool), find-skills, graphify, video-generator. Superpowers não instalado.
5. `~/.claude/agents/`: só GSD; falta `opus-medium.md`.
6. `C:\Projetos\context-hub\.claude\settings.local.json`: não existe (falta a regra do push).
7. Memória: feita.
8. GSD **já está instalado aqui** (skills, agentes, hooks, statusLine, `gsd-core`): não mexer; sai com o kit do hub.

Nada aplicado: global real só com o aval e o Gustavo vendo, com cópia e hash antes.

## Recados ao outro maestro (par A)

- 2026-10-17 ~23h35: recado recebido; daqui em diante escrevo só aqui. Nesta máquina o Gustavo pediu o git **global**
  também como pdgusta (diferente do par A); está acima no Estado.

## Diário (mais novo embaixo)

- 23:25: onboarding; mandato e push confirmados pelo Gustavo (registro ficou no diário da retomada do par A).
- 23:30: identidade do git (local e global) = pdgusta, pedido do Gustavo.
- 23:35: recado do par A (cada maestro, a sua retomada); esta retomada criada.
- 23:45: pré-requisitos conferidos (tudo presente menos o Copilot CLI; Docker Desktop desligado).
- 23:55: global do maestro conferido contra global-do-maestro/README.md (só leitura); faltam os itens 1 a 6; nada aplicado.
- 00:05: aval do Gustavo para aplicar o global. Cópia em C:/Users/gusta/backup-global-maestro-2026-10-18 (hash-antes.txt). A permissão automática barrou a escrita no ~/.claude (autoalteração); nada mudou. Script para o Gustavo rodar no scratchpad da sessão (aplicar-global-maestro.sh).
