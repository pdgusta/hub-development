# Instalação do par B (lenovo-ideapad): o que o maestro de lá executa

Reescrito pelo maestro do par A em 2026-10-18 ~15h40, depois do ticket 49 (par novo com o hub no disco; Fiel: o código
passa, a ordem do par B é esta). Fonte dos comandos: a seção "Sequência final do par B (para copiar)" de
`.scratch/construcao-do-hub/etapas/relatorio-49-par-novo-com-hub.md`, adaptada às decisões do Gustavo (abaixo). O guia
de cada peça é `agents/code/docs/instalacao.md` do hub (no clone do kit); onde ele diz "clone em `C:\context-hub`",
**vale este arquivo** (o Lume ainda vai pôr o guia em dia com o 49).

**Por que não clonar o hub em `C:\context-hub`:** o 49 provou que qualquer diferença de bytes entre o clone e o disco
do A (basta o final de linha) vira conflito: 121 conflitos e 399 arquivos do disco do **A** reescritos. O B sobe com a
pasta do hub **vazia**, recebe o hub pelo banco e só depois liga o git.

## O que o par A já fez (não repetir)

- Par A = `armis00323`, Tailscale `100.120.188.50`, instalado em 2026-10-18 ~13h10; o banco tem o hub; a replicação de
  envio do A já aponta para `http://100.121.86.61:5984/hub` e começa sozinha quando o CouchDB do B subir.
- Os dois `.env` nasceram juntos no A (mesma frase-senha e sal). O do B: `HUB_PAR_ID=lenovo-ideapad`,
  `HUB_BANCO_ENDERECO=100.121.86.61`, `HUB_OUTRO_PAR_URL=http://100.120.188.50:5984`,
  `HUB_MCP_BANCO_DIR=C:\Projetos\hub-mcp-banco`, `HUB_LIVESYNC_CLI=C:\hub-par\livesync\src\apps\cli\dist\index.cjs`,
  tokens próprios, `HUB_MAQUINA=lenovo-ideapad`; cópia diária e proxy **desligados**. **Não gere outro `.env`.**

## Decisões do Gustavo que valem aqui (como no A)

- Cópia diária e proxy de clientes desligados por enquanto: **não registrar** a tarefa `hub-manutencao-diaria`.
- Passos à mão aprovados no A: `HUB_MCP_BANCO_TOKEN` como variável do usuário; tarefas `hub-sincronizador` e
  `hub-vigia`; um terminal Shell "Busca" no canvas; os mods do hub no `CLAUDE_CODE_PLUGIN_DIRS`. Confirme com ele aqui.

## O que chega do A por Taildrop (nunca pelo git)

O maestro do A manda com `tailscale file cp <arquivo> lenovo-ideapad:` (o Gustavo liga "Send Files" no painel do
Tailscale; chega em `C:\Users\<usuário>\Downloads`): `lenovo-ideapad.env` (mova para `C:\hub-transporte\`; ele lê o
hub inteiro: não copie para outro lugar, não ponha no git) e `hub-mcp-banco.bundle` (o fork, ramo `integracao`).

## Os passos, um bloco por vez, lendo a saída (com o Gustavo vendo), em `pwsh`

```powershell
# 0. Variáveis
$Url  = 'https://github.com/pdgusta/context-hub.git'   # o hub privado (o Gustavo empurra o main do A)
$EnvB = 'C:\hub-transporte\lenovo-ideapad.env'
$Hub  = 'C:\context-hub'
$Kit  = 'C:\Projetos\hub-kit'

# 1. Pré-condições: autocrlf igual ao do A; a pasta do hub vazia; nenhum CLAUDE.md acima dela
git config --global core.autocrlf true
if (Test-Path $Hub) { if (Get-ChildItem -Force $Hub) { throw "$Hub não está vazia: pare" } } else { New-Item -ItemType Directory $Hub | Out-Null }

# 2. O kit de fora, o fork e o CLI do LiveSync
git clone -b main $Url $Kit
git clone -b integracao "$HOME\Downloads\hub-mcp-banco.bundle" C:\Projetos\hub-mcp-banco
pwsh "$Kit\agents\code\kit\par\montar-cli-livesync.ps1" -Destino C:\hub-par\livesync -WhatIf
pwsh "$Kit\agents\code\kit\par\montar-cli-livesync.ps1" -Destino C:\hub-par\livesync      # ~3 min; clona o repositório público
```

3. **Cópia e hash das configurações reais** (como no A): `.claude\settings.json`, `.claude\CLAUDE.md`, `.claude\skills`,
   `.claude\agents`, `.claude\mods`, `.claude.json`, `.codex\{config.toml,AGENTS.md,hooks.json,skills}`,
   `.copilot\{copilot-instructions.md,config.json,mcp-config.json,hooks}`, `.agents\skills`, `.agents\.skill-lock.json`
   para `C:\hub-backup\2026-10-18-par-b\`, com `hashes-antes.txt` (SHA256 de cada arquivo).

```powershell
# 4. Simulação e depois banco, busca, MCP e a espera, com a pasta do hub vazia (Docker Desktop ligado)
pwsh "$Kit\agents\code\kit\par\instalar.ps1" -Casa $HOME -Hub $Hub -EnvFile $EnvB -Passos 00,03,04,05,espera -WhatIf
pwsh "$Kit\agents\code\kit\par\instalar.ps1" -Casa $HOME -Hub $Hub -EnvFile $EnvB -Passos 00,03,04,05,espera -PrazoEspera 900
# siga só com "o par recebeu o hub: N arquivos do banco no disco"; senão:
#   node "$Kit\agents\code\kit\par\espera.mjs" --hub $Hub --env $EnvB --segundos 600

# 5. O git, sem tocar nos arquivos que vieram do banco
git -C $Hub init -q -b main
git -C $Hub remote add origin $Url
git -C $Hub fetch -q origin main
git -C $Hub reset -q --mixed origin/main
git -C $Hub branch -q --set-upstream-to=origin/main
$f = @(git -C $Hub -c core.quotePath=false ls-files -d | Where-Object { $_ -match '(^|/)\.' })   # só o que tem ponto
if ($f) { git -C $Hub checkout -- @f }
git -C $Hub config --local user.name pdgusta; git -C $Hub config --local user.email gustavopottpott@hotmail.com
git -C $Hub status --short    # um " D" é nota que o A apagou depois do commit: NÃO restaurar

# 6. O kit do próprio hub: 04 (regrava a tarefa com o laço do hub e o .git/info/exclude), 08 e 10
pwsh "$Hub\agents\code\kit\par\instalar.ps1" -Casa $HOME -Hub $Hub -EnvFile $EnvB -Passos 04,08,10 -WhatIf
pwsh "$Hub\agents\code\kit\par\instalar.ps1" -Casa $HOME -Hub $Hub -EnvFile $EnvB -Passos 04,08,10
# conferir: o XML do laço aponta "$Hub\agents\code\kit\par\banco\laco.ps1"; o .git\info\exclude tem "# hub:exclusoes:inicio"
# (comandos de conferência no relatório do 49, bloco 6)

# 7. Tarefas (com o Gustavo): só estas duas
schtasks /create /tn hub-sincronizador /xml C:\hub-par\banco\tarefa-sincronizador.xml
schtasks /create /tn hub-vigia         /xml "$HOME\.hub-kit\tarefas\hub-vigia.xml"

# 8. O clone de fora sai
Remove-Item -Recurse -Force $Kit
```

9. **À mão, como no A:** `[Environment]::SetEnvironmentVariable('HUB_MCP_BANCO_TOKEN', <valor do .env do B>, 'User')`;
   terminal Shell "Busca" no canvas com `pwsh -NoProfile -File C:\context-hub\agents\skills\busca\iniciar.ps1`; somar ao
   `CLAUDE_CODE_PLUGIN_DIRS` do `settings.json`:
   `;C:\context-hub\agents\code\mods\fim-da-resposta;C:\context-hub\agents\code\mods\roteamento;C:\context-hub\agents\code\mods\vigia`;
   reabrir o Maestri (a variável e os mods só valem para processos novos).
10. **Conferir:** `node C:\context-hub\agents\skills\vigia\vigia.mjs passada --env $EnvB` em `ok`; uma nota de teste
    gravada no B aparece no A e uma do A aparece no B (combine com o maestro do A pela retomada).
11. Guarde `$EnvB` só nesta máquina, fora do hub (é o `-EnvFile` para rodar de novo e desfazer).

O que não foi provado (relatório do 49): o bloco 6 (o 04 do próprio hub depois do git) e o 03 e o 05 com a pasta vazia,
só pela leitura. Pare e avise na sua retomada se algo sair diferente; o maestro do A acompanha por ela.

## Antes do passo 04 (2026-10-21, ticket 52)

Instale o PowerShell 7 pelo MSI, para a tarefa `hub-sincronizador` ter um caminho fixo: `winget install --id
Microsoft.PowerShell --source winget --installer-type wix` (com `--force` se o winget disser que já está instalado), num
terminal com administrador. Confira `C:\Program Files\PowerShell\7\pwsh.exe`.
