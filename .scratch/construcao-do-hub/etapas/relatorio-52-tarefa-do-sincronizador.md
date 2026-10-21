# Relatório do 52: a tarefa hub-sincronizador roda de verdade (Brasa, 2026-10-21)

Ramo `ticket-52` (worktree `C:/context-hub-wt/ticket-52`, de `integracao` e82dd85), commit 2903ab7; `integracao` 35da1e6 juntada.

## A causa

O XML do `Write-TarefaSincronizador` (`agents/code/kit/par/banco/banco.psm1`) tinha `<Command>pwsh.exe</Command>`.
Nesta máquina o pwsh é o da Store (7.6.7): o `pwsh.exe` do PATH é o atalho (reparse point) em
`%LOCALAPPDATA%\Microsoft\WindowsApps`, e o executável real fica em
`C:\Program Files\WindowsApps\Microsoft.PowerShell_7.6.7.0_x64__8wekyb3d8bbwe\pwsh.exe`. O Agendador não achou o nome
solto: `LastTaskResult` 2147942402 (0x80070002) no par A, última tentativa em 21/10 11:08.

## O conserto

`Get-ExecutavelPwsh` (no `banco.psm1`): o pwsh do instalador MSI (`%ProgramFiles%\PowerShell\7\pwsh.exe`) se existir,
porque o caminho é fixo; senão, o executável do pwsh que roda o kit (`(Get-Process -Id $PID).Path`), nunca o atalho. A
ação da tarefa usa esse caminho completo. Doc: `agents/code/docs/componentes/banco-do-par.md`, item 8.

## Teste

`agents/code/test/banco/kit-sem-docker.ps1` (pelo `07-kit-sem-docker.test.mjs`), item 5: a ação é um caminho completo
de um `pwsh.exe` que existe e não é reparse point. Vermelho antes (`pwsh.exe` solto), verde depois. Conferido à mão: o
executável real da Store abre direto, sem o atalho (`Start-Process` com o caminho completo, código de saída 7 devolvido).

Testes leves no ramo: `07-kit-sem-docker`, `38-ensaio-banco`, `45-duas-maquinas-sem-docker`, `46-kit-duas-maquinas`:
28/28. Sem trava.

## Como reaplicar num par já instalado (com o maestro e o Gustavo, depois da junção)

No par, com o hub já na ponta que tem o 52, num `pwsh` (o mesmo que deve rodar a tarefa):

```powershell
$EnvPar = 'C:\hub-transporte\<id do par>.env'
Import-Module C:\context-hub\agents\code\kit\par\banco\banco.psm1 -Force -DisableNameChecking
$par = Read-EnvPar $EnvPar
$xml = Write-TarefaSincronizador $par          # regrava o XML com o caminho completo do pwsh (só se mudou)
Select-String -Encoding Unicode '<Command>' $xml   # confere: caminho completo, não "pwsh.exe"
schtasks /create /tn hub-sincronizador /xml $xml /f   # /f troca a tarefa que já existe
Start-ScheduledTask -TaskName hub-sincronizador
Start-Sleep 20; Get-ScheduledTaskInfo -TaskName hub-sincronizador | Select-Object LastRunTime, LastTaskResult  # 0
```

O `pwsh agents/code/kit/par/04-banco.ps1 -EnvFile <env>` (o passo 04 inteiro, idempotente) também regrava o XML; o
caminho acima mexe só na tarefa. A tarefa registrada fica habilitada (o XML diz `Enabled`).

## Ressalvas

- **Não verificado: a tarefa registrada rodando** (as regras não deixam registrar tarefa na construção). O teste
  confere o XML e que o Agendador aceita a definição (já existia); a conferência final é o `LastTaskResult` 0 na
  reaplicação acima.
- **pwsh da Store:** o caminho tem a versão. Uma atualização automática do pwsh troca a pasta e a tarefa volta a
  falhar (0x80070002) até rodar de novo o bloco acima. Proposta: instalar o pwsh pelo MSI nos dois pares
  (`winget install --id Microsoft.PowerShell --source winget`), e o kit passa a usar o caminho fixo dele sem mudança
  de código; ou uma conferência na vigia (a ação da tarefa aponta para um arquivo que existe). Fora do escopo do 52.
