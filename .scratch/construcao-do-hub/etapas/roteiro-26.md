# Roteiro do 26: o hub de verdade nas duas máquinas

Rascunho do maestro, 2026-10-17 ~21h50, a partir da documentação técnica do Lume (`agents/code/docs/`, ramo `docs`,
conferida em `integracao` ca62332): `operacao.md`, `arquitetura.md`, `componentes/kit-de-par.md`,
`componentes/banco-do-par.md`. Ticket: `../issues/26-instalacao-de-verdade-no-par-1.md`. "Não verificado" = nenhum
teste provou.

## O que o kit já faz e o que ainda falta para duas máquinas

Faz (provado em casa de ensaio): `instalar.ps1 -Casa -Hub -EnvFile` com os passos 00 (confere), 03 (busca), 04 (banco
do par), 05 (MCP do banco), 08 (liga os três harnesses: contrato, skills, MCP, hooks, GSD fora) e 10 (XML das
tarefas); `-WhatIf` e `-Desfazer`; guarda o que estava.

Falta (achados da construção; viram o **ticket 45, preparo para duas máquinas**, antes da instalação):
1. **Rede entre as máquinas**: o CouchDB publica a porta só em `127.0.0.1`; a replicação entre máquinas é pelo
   endereço Tailscale e **não foi verificada**. Precisa publicar no IP da tailnet (nunca `0.0.0.0`) e provar.
2. **`HUB_PAR_ID`**: nenhum script do kit a define; sem ela, link para fora do hub não vira `par://`.
3. **Esperar a convergência**: um par novo leva minutos para receber o hub (~530 arquivos, 4-7 min no ensaio); o kit
   não espera nem avisa.
4. **Segredos e peças fora do repositório**: a frase-senha e o sal da cifra são os mesmos nos dois pares
   (`New-EnvParesBanco` gera os dois numa máquina; o `.env` do outro par vai por canal separado, nunca pelo git); o
   **CLI do LiveSync** é um build local (`C:\Projetos\spike-livesync\...\dist\index.cjs`) e o **fork do MCP do banco**
   (`C:\Projetos\hub-mcp-banco`) só existe aqui: a outra máquina precisa dos dois.
5. O `10-proxy.ps1` (acesso de clientes) não está na fila do `instalar.ps1`; o mod do Claude Code, a extensão do
   Copilot e o `notify` do Codex não são ligados pelo kit (ressalva do 23).

## Decisões do Gustavo antes de começar

- **D1. Qual código vira o hub de verdade**: juntar `integracao` (ca62332) no `main` do `C:\context-hub` e empurrar
  para o repositório privado já configurado (`origin` = `pdgusta/context-hub` no GitHub), para clonar na outra máquina.
  Recomendação: sim; push só com o seu aval (regra da construção: o maestro nunca faz `git push`).
- **D2. Como levar o que não vai pelo git** (o `.env` do par B, o fork e o CLI do LiveSync): pendrive ou pasta
  compartilhada sua. Recomendação: os dois builds pelo próprio repositório de cada um (o fork tem histórico local; um
  `git bundle` resolve), o `.env` só à mão.
- **D3. Tailscale**: já está nas duas máquinas? É o caminho que o spec escolheu entre os pares.

## Passos

### 1. Ticket 45 (construtores, aqui, com testes)
Os cinco itens acima, com prova no ensaio onde der (a rede entre máquinas de verdade só se prova no passo 4).

### 2. Par A, esta máquina (com você vendo)
1. `pwsh agents/code/kit/par/instalar.ps1 -Casa $HOME -Hub C:\context-hub -EnvFile <parA>.env -WhatIf`: lemos juntos
   o que ele faria.
2. Cópia e hash das configurações reais (`~/.claude`, `~/.claude.json`, `~/.codex`, `~/.copilot`, `~/.agents`).
3. A instalação de verdade; registrar as tarefas (`schtasks /create /tn <nome> /xml <arquivo>`) com você.
4. Conferir: os três harnesses abertos fora do hub veem o contrato; `vigia passada` em `ok`; a busca responde.

### 3. Par B, o outro PC (lá: Claude Code, Maestri, admin)
1. Pré-requisitos que o passo 00 confere: Node 22+, Python, modo de desenvolvedor do Windows ligado, nenhum
   `CLAUDE.md` no hub nem acima; mais Docker Desktop, PowerShell 7 e git.
2. Clonar o hub em `C:\context-hub` (depois do D1); trazer o fork e o CLI do LiveSync (D2); o `.env` do par B.
3. `instalar.ps1 ... -WhatIf`, cópia e hash, a instalação de verdade, as tarefas.

### 4. Ligar os dois e provar
1. Replicação nos dois sentidos pela tailnet; **esperar o par B receber o hub** (minutos).
2. Uma nota gravada no A aparece no B, e uma do B aparece no A; `vigia passada` em `ok` nos dois.
3. Daí em diante, uso normal nas duas; o que aparecer vira ticket de conserto.

### 5. Os dois maestros
O maestro do outro PC é outra sessão. Candidatos para conversarem (estudar na fonte antes de propor): uma pasta de
recados no próprio hub (replica sozinha entre os pares), o git do hub, ou recurso do Maestri entre máquinas (não
verificado).
