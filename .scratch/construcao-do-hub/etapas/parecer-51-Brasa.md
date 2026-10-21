# Parecer do 51 (Brasa) — Fiel, 2026-10-21

Ramo `ticket-51` (02f026c, 16b0715), de `integracao` e82dd85. Relatório `etapas/relatorio-51-notificacao-com-acentos.md`.
2ª leitura: subagente Sonnet, `parecer-51-Brasa-segunda-leitura.md`. Acordo nos dois.

## Veredito: VOLTA

A causa e o conserto da leitura estão certos (o `$input` do 5.1 lê na página OEM; ler os bytes da entrada como UTF-8).
O contrato `HUB_VIGIA_NOTIFICAR` não muda. Mas o caminho real, sem `-Xml`, quebrou: a vigia não mostra mais nenhum
toast, e calada.

## Consertos

1. **`$Xml` e `$xml` são a mesma variável** (Fiel e 2ª leitura, cada um por sonda). O PowerShell não distingue caixa.
   `param([string]$Xml)` prende o tipo `[string]`, então `$xml = [Windows.Data.Xml.Dom.XmlDocument]::new()`
   (`notificar.ps1`, logo antes da linha 19) vira texto e `$xml.LoadXml($texto)` falha:
   `[System.String] não contém um método denominado 'LoadXml'` (`notificar.ps1:19`). Conferido no script do ramo
   com texto na entrada e sem `-Xml`: o erro sai antes do `Show`, e o processo **sai com código 0**. A vigia não vê a
   falha. Renomear a variável do documento (ex.: `$doc`) ou o parâmetro. Com `$doc`, a sonda da 2ª leitura chega ao
   `LoadXml` sem erro.
2. **O teste não cobre o caminho real** (2ª leitura). `51-notificar-acentos.test.mjs` sempre passa `-Xml`, e o script
   retorna antes do trecho com defeito. Cobrir o caminho sem `-Xml` até o `LoadXml` sem mostrar toast. Ex.: o `-Xml`
   grava o XML **depois** do `LoadXml` do `XmlDocument` do Windows, ou um `-SemMostrar` que para logo antes do `Show`.
   O teste deve ficar vermelho com o defeito do conserto 1.

## O que o Fiel rodou

- Leves 16, 17, 51 e `harness-real`: 50/50, 0 pulado (verdes com o defeito: é o conserto 2).
- Sondas: `[string]$Xml` + `$xml = XmlDocument` dá `System.String`; o `notificar.ps1` do ramo sem `-Xml` dá o erro
  do `LoadXml` antes do `Show`, sem toast.

## Ressalvas

- O ramo não tem a ponta de `integracao` (35da1e6, só o cabeçalho do teste do 49): `git merge integracao` antes da
  r2, sem conflito esperado.
- O toast na tela segue sem prova visual (o relatório já diz).

## r2 (fe8be14, com integracao 35da1e6 em 4b05241): PASSA em acordo

- Conserto 1: o documento é `$doc`; `$ErrorActionPreference = 'Stop'` faz a falha sair com código 1, e a vigia
  (`vigia.mjs` ~255) registra "a notificação falhou" e segue a passada.
- Conserto 2: o `-Xml` grava `$doc.GetXml()` depois do `LoadXml` e para antes do `Show`. Sonda do Fiel: o script com
  `$doc` trocado de volta por `$xml` sai com código 1; o do ramo sai com 0, e os acentos ficam certos no XML.
- Leves 16, 17, 51 e `harness-real`: 50/50. 2ª leitura r2: PASSA (`parecer-51-Brasa-segunda-leitura-r2.md`).
- Ressalva: o `Show` de verdade (toast na tela) segue sem prova; conferência visual com o Gustavo.
