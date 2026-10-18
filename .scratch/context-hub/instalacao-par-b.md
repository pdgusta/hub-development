# Instalação do par B (lenovo-ideapad): o que o maestro de lá executa

Escrito pelo maestro do par A em 2026-10-18 ~13h30, depois de instalar o par A. O guia de cada passo é a página do
hub **`C:\context-hub\agents\code\docs\instalacao.md`** (vem no clone do hub). Este arquivo diz só o que é
específico do par B e o que o par A já fez. Ticket: `.scratch/construcao-do-hub/issues/26-instalacao-de-verdade-no-par-1.md`.

## PARE: ainda não clone o hub nem instale (2026-10-18 ~14h)

O ticket 49 (Brasa, parcial) mostrou que **subir o B com o hub já clonado no disco é arriscado**: com final de linha
diferente, 121 conflitos e 399 arquivos do disco do **A** reescritos; com os bytes iguais, o resultado variou entre
nenhum conflito e 400 "binário descartado" e uma nota diferente nos dois discos. Ela está testando o caminho seguro
(o banco do B puxa o do A numa replicação única antes de o CLI do B partir). **Não rode os passos 2, 6 e 7 até o maestro
do A escrever aqui o caminho aprovado.** Os passos 1, 3, 4 e 5 (pré-requisitos, fork, CLI do LiveSync, cópia e hash)
podem seguir, porque nenhum deles toca no hub nem no banco.

## O que o par A já fez (não repetir)

- Par A = `armis00323`, Tailscale `100.120.188.50`, instalado às ~13h10 (CouchDB `hub-banco` em
  `127.0.0.1:5984` e `100.120.188.50:5984`, MCP 8796-8798, daemon do LiveSync sobre `C:\context-hub`, banco com 558
  arquivos). A replicação de envio do A já aponta para `http://100.121.86.61:5984/hub` (o B): começa sozinha quando o
  CouchDB do B subir.
- Os dois `.env` foram gerados **no A** (seção 3 do guia; a frase-senha e o sal da cifra são os mesmos nos dois e só
  podem nascer juntos). O do B já está completo: `HUB_PAR_ID=lenovo-ideapad`, `HUB_BANCO_ENDERECO=100.121.86.61`,
  `HUB_OUTRO_PAR_URL=http://100.120.188.50:5984`, `HUB_MCP_BANCO_DIR=C:\Projetos\hub-mcp-banco`, tokens próprios,
  `HUB_MAQUINA=lenovo-ideapad`; cópia diária e proxy de clientes **desligados** (vazios). **Não gere outro `.env`.**

## O que chega do par A (por Taildrop, nunca pelo git)

O maestro do A manda com `tailscale file cp <arquivo> lenovo-ideapad:` (o Gustavo liga "Send Files" no painel do
Tailscale). No Windows, chega em `C:\Users\<usuário>\Downloads`.
1. `lenovo-ideapad.env`: mova para `C:\hub-transporte\lenovo-ideapad.env` (fora do hub e de repositório git). Ele lê
   o hub inteiro: não copie para outro lugar, não ponha no git.
2. `hub-mcp-banco.bundle`: o fork do MCP do banco (ramo `integracao`, 34c3e50).

## Passos no par B, na ordem (cada um com o Gustavo vendo)

0. **Antes de clonar:** `git config --get core.autocrlf` deve dar `true`, como no A (achado da Brasa no ticket 49:
   no A os textos do hub estão em CRLF; com `false`, cada arquivo do clone difere do banco). E **espere o resultado
   do ticket 49** (o maestro do A avisa na retomada dele): ele diz se o B pode subir com o hub já clonado no disco ou
   se precisa de outro caminho.
1. Pré-requisitos (guia §1): já conferidos por você em 2026-10-17 ~23h45. Ligue o Docker Desktop. O Copilot CLI não
   está no B: o efeito no passo 08 não foi verificado (guia §1); diga ao Gustavo antes.
2. O hub: `git clone https://github.com/pdgusta/context-hub.git C:\context-hub` (o `main` com o guia é o fe55b12 ou
   mais novo). Configure nele `git config --local user.name pdgusta` e `user.email gustavopottpott@hotmail.com`.
3. O fork, do bundle: `git clone -b integracao <Downloads>\hub-mcp-banco.bundle C:\Projetos\hub-mcp-banco`.
4. O CLI do LiveSync, do repositório público (sem bundle): `pwsh C:\context-hub\agents\code\kit\par\montar-cli-livesync.ps1 -Destino C:\hub-par\livesync -WhatIf`, depois sem `-WhatIf` (~3 min no A).
5. Cópia e hash das configurações reais (guia §8). No A foi assim: `.claude\settings.json`, `.claude\CLAUDE.md`,
   `.claude\skills`, `.claude\agents`, `.claude\mods`, `.claude.json`, `.codex\{config.toml,AGENTS.md,hooks.json,skills}`,
   `.copilot\{copilot-instructions.md,config.json,mcp-config.json,hooks}`, `.agents\skills`, `.agents\.skill-lock.json`
   para `C:\hub-backup\<data>-par-b\`, com `hashes-antes.txt` (SHA256 de cada arquivo).
6. Simulação: `pwsh C:\context-hub\agents\code\kit\par\instalar.ps1 -Casa $HOME -Hub C:\context-hub -EnvFile C:\hub-transporte\lenovo-ideapad.env -WhatIf`; leia com o Gustavo (guia §7).
7. A instalação (o mesmo comando sem `-WhatIf`). A espera (guia §10): o banco do B recebe a replicação do A e o daemon
   leva ao disco; na prova do 46, ~566 arquivos em 315 s.
8. À mão, como no A (o Gustavo aprovou lá; confirme aqui):
   - `HUB_MCP_BANCO_TOKEN` como variável do usuário, com o valor do `.env` do B
     (`[Environment]::SetEnvironmentVariable('HUB_MCP_BANCO_TOKEN', <valor>, 'User')`);
   - tarefas: `schtasks /create /tn hub-sincronizador /xml C:\hub-par\banco\tarefa-sincronizador.xml` e
     `schtasks /create /tn hub-vigia /xml $HOME\.hub-kit\tarefas\hub-vigia.xml` (a manutenção diária fica para quando
     a cópia diária for ligada);
   - um terminal Shell "Busca" no canvas do Maestri rodando `pwsh -NoProfile -File C:\context-hub\agents\skills\busca\iniciar.ps1`;
   - os mods do hub no `CLAUDE_CODE_PLUGIN_DIRS` do `settings.json`:
     `;C:\context-hub\agents\code\mods\fim-da-resposta;C:\context-hub\agents\code\mods\roteamento;C:\context-hub\agents\code\mods\vigia`;
   - reabrir o Maestri e os terminais (a variável e os mods só valem para processos novos).
9. Apague `C:\hub-transporte\lenovo-ideapad.env` só depois que a instalação passar (ele é o `-EnvFile` do kit também
   para desfazer e rodar de novo; guarde-o fora do hub, só nesta máquina).
10. Conferir (guia §13): `node C:\context-hub\agents\skills\vigia\vigia.mjs passada --env C:\hub-transporte\lenovo-ideapad.env`
    em `ok`; uma nota de teste gravada no B aparece no A e uma do A aparece no B (o maestro do A grava a dele e avisa).

Registre cada passo na sua retomada (`retomada-maestro-par-b.md`) e dê push: o maestro do A acompanha por ela.
