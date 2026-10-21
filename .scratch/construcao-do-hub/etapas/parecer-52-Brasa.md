# Parecer do 52 (Brasa) — Fiel, 2026-10-21

Ramo `ticket-52` (2903ab7), contém `integracao` 35da1e6. Relatório `etapas/relatorio-52-tarefa-do-sincronizador.md`.
2ª leitura: subagente Sonnet, `parecer-52-Brasa-segunda-leitura.md`. Acordo nos dois.

## Veredito: PASSA com ressalvas

A causa confere (`<Command>pwsh.exe</Command>` solto; o Agendador não acha pelo PATH, 0x80070002). `Get-ExecutavelPwsh`
dá o caminho completo: o do MSI, senão o pwsh que roda o kit. Só o `Install-ParBanco` (passo 04) e o teste chamam
`Write-TarefaSincronizador`. O teste novo confere caminho absoluto, `pwsh.exe` que existe e não é reparse point:
com o `pwsh.exe` solto ele fica vermelho (`IsPathRooted` falso). A tarefa `hub-vigia` não tem o mesmo risco
(`conhost.exe` de System32 e o node por caminho absoluto).

## O que o Fiel rodou

- Leves `07-kit-sem-docker`, `38-ensaio-banco`, `45-duas-maquinas-sem-docker`, `46-kit-duas-maquinas` e
  `harness-real`: 37/37, 0 pulado.
- Nesta máquina: o pwsh do PATH roda de `C:\Program Files\WindowsApps\Microsoft.PowerShell_7.6.7.0_...\pwsh.exe`, **e
  existe também o MSI** em `C:\Program Files\PowerShell\7\pwsh.exe`. A 2ª leitura gerou o XML com o `.env` do par A
  (sem registrar): `<Command>C:\Program Files\PowerShell\7\pwsh.exe</Command>`.

## Ressalvas (não seguram)

1. **Relatório, "A causa":** "nesta máquina o pwsh é o da Store" vale só para o PATH. O MSI 7.6.7 também está
   instalado e é o que a tarefa vai usar (caminho fixo). A fragilidade da pasta com versão da Store só vale onde não há
   MSI. Ajustar a frase, e a da receita "o mesmo pwsh que deve rodar a tarefa": com o MSI, a tarefa usa o MSI seja
   qual for o shell da receita. O `Select-String '<Command>'` da receita mostra isso.
2. **Receita de reaplicação:** está certa (`Read-EnvPar` exportado; o laço é o do hub importado). No par A, o `.env`
   é o de `C:\hub-transporte\` (a 2ª leitura achou o do par A e o do B lá). A conferência final (`LastTaskResult` 0)
   fica com o maestro e o Gustavo, como o relatório diz.
3. **"A suíte segue verde"** segue desmarcado no ticket: fica com o Rebite na junção.
