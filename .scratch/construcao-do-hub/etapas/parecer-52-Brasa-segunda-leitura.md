# Parecer (2ª leitura independente) do 52, Brasa

Ramo `ticket-52` (2903ab7), lido por mim. Sondas em %TEMP%\hub-ensaio-52-2l-a (apagada). Nada registrado nem rodado no Agendador.

## Veredito: passa, com 3 ressalvas (nenhuma conserto obrigatório)

## O que conferi
1. **Causa:** `<Command>pwsh.exe</Command>` solto no XML (diff). O Agendador não resolve pelo PATH do usuário nem abre o atalho da Store: coerente com 0x80070002. Aceito.
2. **Conserto:** `Get-ExecutavelPwsh` prefere `%ProgramFiles%\PowerShell\7\pwsh.exe`, depois `(Get-Process -Id $PID).Path`. O throw só vale se o host não for `pwsh.exe`. Windows PowerShell 5.1 nem importa o módulo (`??` na linha 88), então o throw só pega host embutido: inofensivo.
3. **Chamadores:** `Write-TarefaSincronizador` é chamado só por `Install-ParBanco` (04-banco.ps1, sob o pwsh do instalar) e pelo teste `kit-sem-docker.ps1`. O laço não chama. Exportado por `*-*`, então `Read-EnvPar` e `Get-ExecutavelPwsh` ficam visíveis ao `Import-Module`.
4. **Teste:** `07-kit-sem-docker` roda verde aqui (1/1). Falharia antes: `pwsh.exe` solto não é `IsPathRooted`. (Não revertei o código para ver o vermelho; é dedução do diff.)
5. **Sonda real:** neste par (Armis00323) `Write-TarefaSincronizador` com `.env` real gera `<Command>C:\Program Files\PowerShell\7\pwsh.exe</Command>`.
6. **Idempotência:** a comparação é o XML inteiro (`-ceq`). Sem mudança, o arquivo não é regravado (sonda: `idem: True`). Quando o pwsh muda, o XML muda e é regravado (sonda: troquei o comando no arquivo, regravou). Correto.
7. **hub-vigia (10-manutencao):** sem o mesmo risco. `conhost.exe` fica em System32 (o Agendador acha) e o `node` entra como caminho absoluto via `(Get-Command node).Source` (a tarefa registrada mostra `C:\Program Files\nodejs\node.exe`). Nenhum nome solto que dependa do PATH do usuário.

## Ressalvas
1. **Afirmação do relatório incompleta:** "nesta máquina o pwsh é o da Store" vale só para o PATH. Aqui também existe `C:\Program Files\PowerShell\7\pwsh.exe`, mesma versão 7.6.7. Com o conserto, a tarefa passa a usar o MSI (caminho fixo), não o da Store. Isso já resolve a fragilidade da versão na pasta da Store neste par; a ressalva sobre atualização da Store só vale se o MSI faltar.
2. **Receita de reaplicação:** os comandos estão certos. O `.env` do par A é `C:\hub-transporte\armis00323.env` (o do par B é `lenovo-ideapad.env`); o relatório deixa `<id do par>`, ok. O `Import-Module` aponta o hub (`C:\context-hub`), que só terá o 52 depois da junção, como o relatório já diz. A frase "num pwsh (o mesmo que deve rodar a tarefa)" engana: com o MSI instalado, a tarefa usa o MSI mesmo se o shell for o da Store. Conferir com o `Select-String '<Command>'` do próprio passo resolve.
3. **Critério "a suíte segue verde"** do ticket segue desmarcado; o relatório cita só 4 testes leves (28/28). Não reexecutei a suíte inteira; rodei só o 07. A decisão fica com o integrador.

## O que quebra ao juntar
Nada visto. O diff é só `banco.psm1`, `kit-sem-docker.ps1` e o doc `banco-do-par.md`; não toca os arquivos do 51.
