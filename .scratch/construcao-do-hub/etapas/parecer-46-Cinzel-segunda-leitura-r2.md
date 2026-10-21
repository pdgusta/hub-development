# 2ª leitura do 46 (Cinzel), rodada 2: PASSA

Leitura independente do commit dc4fd1a (ramo ticket-46). Sem rodar testes (pedido do Fiel).

## Conferências
(a) Fecha o caso. O `10.env.modelo` não traz mais `HUB_PAR_ID=` (só comentário), e o `lerEnv` do 08 deixa de aceitar vazio sobre valor já lido. Duas barreiras para o mesmo caso.
(b) Nada depende de vazio vencer. 08-harnesses.mjs lê só `env[url]` (exige preenchido, linha 103) e `env.HUB_PAR_ID` (linha 122). espera.mjs lê `HUB_VIGIA_LEITOR_DB`, `HUB_LIVESYNC_CLI`, `HUB_VIGIA_OUTRO_PAR_URL || HUB_OUTRO_PAR_URL`, `HUB_OUTRO_PAR_USER`, `HUB_OUTRO_PAR_PASSWORD ?? ''`; todos são "preenchido ou nada". A regra só ajuda no `||`. Chave só vazia continua vazia (`!(m[1] in env)`). Ninguém precisa apagar valor.
(c) Os leitores PowerShell (`Read-EnvPar`, `Read-EnvMcpBanco`, `Read-EnvProxy`) seguem com "última vence". Chaves que o `New-EnvParesBanco` do 45 escreve: HUB_PAR_ID, HUB_BANCO_CONTEINER/PORTA/ENDERECO/ESTADO, COUCHDB_USER/PASSWORD/DATABASE/PASSPHRASE, HUB_BANCO_SAL, HUB_OUTRO_PAR_URL/USER/PASSWORD, HUB_ROOT, HUB_LIVESYNC_DB/CLI, HUB_VIGIA_LEITOR_DB. Os modelos 03, 05 e 10 têm só HUB_MCP_BUSCA_URL, HUB_MCP_BANCO*, HUB_PROXY*, HUB_MAQUINA, HUB_COPIA_*. Sem interseção: nenhuma chave do gerador reaparece vazia. (O 04.env.modelo repete essas chaves, mas é alternativa ao gerador, não se junta a ele.)
(d) O teste novo monta o caso certo (gerador com `HUB_PAR_ID=casa` + linhas dos 3 modelos, `-Passos 08 -WhatIf`, espera a ação "id do par (casa)"). Ver ressalva 1.

## Consertos
Nenhum.

## Ressalvas
1. O teste passa pelas duas barreiras juntas: sem a mudança no `lerEnv` mas com o modelo limpo, ele passaria também. Não isola a regra nova do `lerEnv`. Aceitável: o caso do parecer (modelo clobbando o id) está coberto.
2. As mudanças no `espera.mjs` fora do conserto (maxBuffer 64 MiB e texto "ainda está vazio") fecham as ressalvas 2 e 4 da rodada 1; conferidas no diff, corretas, teste de texto atualizado junto.
3. Para o 26: `HUB_MAQUINA` e `HUB_PAR_ID` devem ter o mesmo nome (comentário do modelo já diz).
