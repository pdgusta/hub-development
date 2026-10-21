# Parecer do 51, segunda leitura, volta r2 (Brasa) — veredito: PASSA

Ramo ticket-51, fe8be14 (diff 16b0715..fe8be14: notificar.ps1, teste 51, cabeçalho do teste 49 vindo da junção). Só leitura; sondas em %TEMP%\hub-ensaio-51-2l-a, apagadas; sem toast.

## Consertos da r1

1. **$Xml/$xml:** feito e certo. O documento agora é `$doc`, com comentário que diz o porquê. Sonda: cópia do script sem a linha do `Show`, rodada sem `-Xml` em powershell 5.1 com `-File`: chega ao `LoadXml` sem erro, status 0.
2. **Cobertura do caminho real:** feita. O `-Xml` agora vem depois do `LoadXml` e grava `$doc.GetXml()`, então o teste passa pelo documento do Windows e para antes do `Show`. O teste ajusta a quebra de linha (o documento grava `\r\n`) e está documentado no cabeçalho. Rodei `node --test agents/code/test/51-notificar-acentos.test.mjs`: 1 passa, 0 falha. Se alguém voltar a colidir o nome, o `LoadXml` falha e o teste vermelho pega.

## `$ErrorActionPreference = 'Stop'`

- Script: erro de .NET ou cmdlet vira terminante. Sonda: `-Xml` em pasta inexistente sai com status 1 e mensagem no stderr (antes, sairia 0). Erro não terminante (Get-Item de caminho que não existe) também sai 1.
- Vigia (`vigia.mjs` ~250, `notificar`): `spawnSync` e `r.status !== 0` agora pegam a falha e registram "a notificação falhou (stderr)"; antes, erro não terminante passava calado com status 0. Não derruba a passada (só `console.error`). Sem mudança necessária no `vigia.mjs`.
- Entrada vazia: não quebra, título "Hub", corpo vazio, status 0.
- Nada novo quebrado: o caminho com acentos e o contrato `HUB_VIGIA_NOTIFICAR` (entrada padrão, 1ª linha título) seguem iguais; `HUB_VIGIA_NOTIFICAR` com outro comando não passa por este script.

## Ressalvas

- O `Show` de verdade segue não verificado (dito no relatório; não mostrei toast).
- Com `Stop`, falha do toast passa a aparecer no log da vigia; é o desejado, mas quem olhava só o status 0 vai ver erros que antes ficavam calados.
- `-Xml` continua sendo costura de teste em script de produção; agora coberta.
- Cabeçalho do teste 49 é só texto, vindo da junção; sem efeito aqui.
