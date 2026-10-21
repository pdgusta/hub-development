# Parecer do 51, segunda leitura (Brasa) — veredito: VOLTA

Ramo ticket-51, 16b0715. Só leitura; sondas em %TEMP%\hub-ensaio-51-2l-a (apagadas), sem Show, sem toast.

## Consertos

1. **O caminho real (sem -Xml) quebra no powershell 5.1.** O nome de variável colide: `param([string]$Xml)` e, mais
   abaixo, `$xml = [Windows.Data.Xml.Dom.XmlDocument]::new()`. Variável do PowerShell não distingue maiúscula; o
   `[string]` do parâmetro continua valendo, então a atribuição vira texto e `$xml.LoadXml($texto)` falha.
   Evidência: copiei o notificar.ps1 do ramo sem a linha do `CreateToastNotifier().Show`, rodei com `powershell
   -NoProfile -ExecutionPolicy Bypass -File` e texto na entrada: "[System.String] não contém um método denominado
   'LoadXml'"; `$xml.GetType().FullName` = System.String. Ou seja, depois do conserto a vigia nunca mostra o toast
   (a falha só aparece no stderr: "a notificação falhou"; status pode ser 0 com erro não terminante, então nem isso
   é garantido). Antes do 51 funcionava (não havia o param). Regressão pior que o acento torto.
   Conserto: renomear a variável do documento (ex.: `$doc`) ou o parâmetro (ex.: `-ArquivoXml`). Com `$doc`, a mesma
   sonda chegou ao `LoadXml` sem erro e o tipo é XmlDocument.
2. **O teste não pega o item 1**, porque sempre passa `-Xml` e retorna antes. Acrescentar cobertura do caminho sem
   `-Xml` até antes do `Show` sem mostrar toast: p.ex. um parâmetro/chave de ensaio que faz `LoadXml` e grava
   `$doc.GetXml()` e não chama `Show`, ou ao menos um teste que rode o script sem `-Xml` num ambiente em que o
   `Show` seja trocado. Sem isso a regressão do item 1 volta sem aviso.

## O que confere

- Causa: `$input` do 5.1 lê na página OEM; ler `OpenStandardInput()` como UTF-8 sem BOM é o conserto certo e deixa o
  contrato HUB_VIGIA_NOTIFICAR igual (texto na entrada padrão, 1ª linha título). `vigia.mjs` (~250) não precisa mudar:
  `spawnSync(comando,{shell:true,input:texto,encoding:'utf8'})`; HUB_VIGIA_NOTIFICAR com outro comando não passa por
  este script.
- Teste 51 é bom no que cobre (ç, ã, á, é, ô, título e corpo, via -File como a vigia chama). Só no Windows.
- Doc da vigia atualizada; linha do doc ficou comprida (cosmético).
- Ao juntar: só 3 arquivos, sem sobreposição vista com o resto.

## Ressalvas

- O toast de verdade segue não verificado (já dito no relatório).
- `-Xml` é costura de teste dentro de script de produção; aceitável, mas o item 2 é o que a torna segura.
