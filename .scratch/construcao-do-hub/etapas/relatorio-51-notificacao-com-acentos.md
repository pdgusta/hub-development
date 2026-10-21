# Relatório do 51: a notificação da vigia com os acentos certos (Brasa, 2026-10-21)

Ramo `ticket-51` (worktree `C:/context-hub-wt/ticket-51`, de `integracao` e82dd85), commits 02f026c, 16b0715 e fe8be14 (r1).

## A causa (confirmada pelo teste antes do conserto)

A vigia (node) manda o texto em UTF-8 na entrada padrão do `notificar.ps1`, chamado pelo `powershell` 5.1 com `-File`.
O `$input` do 5.1 lê essa entrada na página do console (OEM 850): cada letra acentuada vira dois caracteres. O teste,
antes do conserto, saiu com `replica├º├úo parada h├í 3 min`, o mesmo do print do Gustavo.

## O conserto

`agents/skills/vigia/notificar.ps1`: lê os bytes da entrada padrão (`[Console]::OpenStandardInput()`) e decodifica em
UTF-8. O contrato `HUB_VIGIA_NOTIFICAR` não muda (texto na entrada padrão, 1ª linha o título). Parâmetro novo `-Xml
<arquivo>`: grava o XML do toast nesse arquivo (UTF-8) e não mostra; é a costura do teste. Doc:
`agents/code/docs/componentes/vigia.md` (o texto em UTF-8 e o `-Xml`).

## Teste

`agents/code/test/51-notificar-acentos.test.mjs`: chama o `notificar.ps1` como a vigia o chama (`powershell
-NoProfile -ExecutionPolicy Bypass -File ...`), com título e corpo acentuados (ç, ã, á, é, ô) na entrada, e confere o
XML do toast. Vermelho antes (o texto quebrado acima), verde depois. Só no Windows.

Testes leves rodados no ramo: `16-vigia.test.mjs`, `17-vigia-tela.test.mjs` e o 51: 41/41. Sem trava (nada pesado).

## O que não foi verificado

- O toast de verdade na tela (o teste para no XML, antes do `Show`; o XML que vai ao `LoadXml` é o mesmo texto). A
  conferência visual fica com o Gustavo na próxima notificação.
- O toast disparado pela tarefa agendada (ponto aberto da faixa 7, como antes).

## Rodada 1 do Fiel (VOLTA) e os consertos (fe8be14, com `integracao` 35da1e6 juntada em 4b05241)

1. **`$Xml` e `$xml` eram a mesma variável** (o PowerShell não distingue caixa): sem `-Xml`, o documento do toast
   virava texto pelo `[string]` do parâmetro e o `LoadXml` falhava, sem toast e com código 0. O documento agora é
   `$doc`. O script roda com `$ErrorActionPreference = 'Stop'`: uma falha sai com código diferente de zero, e a vigia
   a registra ("a notificação falhou").
2. **O teste cobre o caminho real**: o `-Xml` grava o XML **do documento do Windows** (`$doc.GetXml()`) depois do
   `LoadXml`, e só para antes do `Show`. Com o defeito do item 1, o teste ficou vermelho (`[System.String] não contém
   um método denominado 'LoadXml'`); com `$doc`, verde. O documento grava a quebra de linha como `\r\n`; o teste a
   normaliza.

Leves 16, 17 e 51: 41/41.
