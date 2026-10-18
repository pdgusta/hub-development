# Ticket 08 — Brasa — parecer independente do Fielzinho

2026-10-17. Ramo ticket-08, worktree C:/context-hub-wt/ticket-08, ponta124f43d (integracao9cc878b juntada). Árvore limpa antes/depois. Li revisão em dupla e regras atuais, ticket08/relatório completos, diff das peças do08, teste Docker completo, teste semDocker, laço, helpers e os quatro retratos. Conferi spec Worker4/faixa4 e decisões dos tickets33/48 (limite200MiB, exclusões, tarefa, ramo apagado recuperável). Não li o parecer do Fiel desta rodada. Sem subagentes.

## Veredito

**PASSA na leitura do código, com aceite final PENDENTE da fatia2 e da conclusão do Fiel.** Nenhum conserto bloqueante identificado nesta leitura. Isso NÃO é passe final do ticket: prova51/201MiB obrigatória ainda sem sucesso, conforme mandato do maestro nos comentários do08. Docker e fatias novas ficam exclusivamente comFiel.

## Verificação própria

- `pwsh -NoProfile -File agents/code/test/banco/kit-sem-docker.ps1`:21 PASSA, saída0. Inclui14 casos do07, tarefa logon/PT1M/IgnoreNew sem RestartOnFailure, XML aceito pelo COM do Agendador sem registro, idempotência de gravação, limiar200/201MiB e ausência de tarefa registrada.
- `git diff --check 763813a..HEAD`: saída0. Worktree segue limpa.
- Não rodei Docker, harness real, suíte inteira, tarefa agendada nem serviço. O teste de tamanho próprio usa arquivos com SetLength; não prova transporte de51MiB.

## Critérios contra evidência

1. **Exclusões:** .local/08-f1a.log tem14 PASSA da fatia1 (partida e rodando: controle nos dois bancos, nada com ponto/local nos bancos e discoB). É a primeira execução da Brasa; o mesmo log termina com FALHA de60MiB por tempo900s. Não o trato como rodada inteira verde. Não há log08-fatia-1.log nesta leitura; Fiel repetirá1 na hora quieta conforme pedido.
2. **51/201MiB:** ticket ainda escreve60, mas mandato05:16 troca para51 por memória; teste atual segue51. logs/08-fatia-2.log só contém subida dos pares.08-fatias.status registra corte por memória513MB. Critério PENDENTE; nenhuma evidência de sucesso inferida de teste esparso ou de XML.
3. **Binário recuperável:** log08-fatia-3 tem10 PASSA; base33s, mais nova6,4s, ramo apagado nos dois bancos e hash da perdida antes/depois da compactação. Código compara hash recuperado com hA e retira o banco de recuperação no caminho normal. Retrato binario-ramo-apagado.json contém folha viva e folha _deleted:true com path cifrado e ancestral comum. Isso corresponde ao cenário aprovado do48.
4. **Idempotência e laço:** fatia5 tem5 PASSA (inclui subida/limpeza), arquivos/ID e início do contêiner/revisão de replicação/PID iguais nas duas chamadas. Fatia6 tem8 PASSA: nada a fazer preserva PID; CLI morto religa e envia nota; CLI eCouchDB parados religam e retomam nos dois sentidos4,1s; notas anteriores preservadas. O laço não refaz dispositivo nem dados; relê exclusões antes de subir CLI. Se gerador recusa, erro impede a subida.
5. **Retratos:** os quatro JSON existem e foram lidos. Conflito tem _conflicts e info correspondente; binário tem folha apagada; scheduler em dia registra running e source_seq=through_seq (changes_pending:null); parado registra crashing/econnrefused. Logs4 e7 têm5/4 PASSA, respectivamente. São exemplos de estado, não backup restaurável: não incluem chunks nem segredos, como documentado.
6. **Regressão07:** log08-fatia-07 termina tudo passou; status confirma saída0/24PASSA. Registrou180 procurados sem texto claro nos bancos. Evidências acima são da Brasa, não minhas execuções Docker. Estado do corredor confirma saídas0 para3-7 e07 e a cessão/limpeza da trava; testes registram remoção dos contêineres. Não fiz inspeção própria deDocker.

## Ressalvas, sem novos bloqueios

1. `Get-AcimaDoLimite` exclui apenas caminhos com ponto; não exclui pastas local:true. O comentário do teste diz "só o que replicaria", mais forte que a implementação. Busca por chamadas no ramo encontra só os testes08 e07semDocker: não é hoje o detector da vigia. Antes de reutilizar como detector de divergência, filtrar também a lista do gerador; caso contrário, arquivo deliberadamente local pode virar falso aviso. Achado por leitura, não reprodução adicional.
2. `Restore-RamoApagado`, helper de ensaio, não usa finally para apagar cópia/leitor: erro entre criar a cópia e cleanup deixa esses recursos até o teardown dos pares. Não promover essa função sem cleanup garantido para ferramenta de produção; o comando da vigia é outra entrega.
3. XML validado não prova o ciclo real do Agendador nem a vida do daemon filho após terminar laco.ps1. Relatório declara essa pendência; registro real continua fora do ensaio autorizado. Não inventei resultado para ela.

## Próximo passo

Enviar parecer aoFiel. Aguardar fatias1/2 dele e seus logs/estado para fechar o aceite; a2 não foi dispensada. Nenhuma edição em código/spec/ticket.

## Acordo com Fiel — rodada 1: VOLTA

Aceito promover a ressalva1 ao único conserto bloqueante, reforçada pela sonda independente doFiel. Reli banco.psm1:276-281 e, depois de encerrar minha leitura independente, li parecer-08-Brasa.md. Substring depende de raiz/FullName com grafia e comprimento compatíveis; a barra final e o nome curto quebram essa suposição. Resultados da sonda doFiel: nexos/video.bin e el/clientes/rascunho/video.bin; não são reproduções minhas.

Conserto acordado: GetRelativePath com raiz e arquivo normalizados para a mesma forma real/longa (a troca de Substring sozinha não resolve alias curto versus longo), barras finais tratadas, e exclusão das pastas local:true pela mesma lista/regra do gerador. Testar barra final, nome curto doWindows e201MiB em pasta local no kit-sem-docker. Motivo: a função é entregue à vigia16, e caminho cortado/falso aviso compromete essa costura, mesmo sem consumidor atual no ramo.

Aceito como ressalvas não bloqueantes as quatro doFiel: log doCLI apagado no restart; falha do laço sem laco.log; possível janela doPowerShell (não verificado); retrato sem frase/sal só prova forma, não decifração. Mantidas minhas ressalvas de Restore semfinally e execução real doAgendador não verificada. Sem pedir registro global.

Veredito independente anterior de passe de código substituído por **VOLTA**, somente pelo conserto1 consolidado. Fatias1/2 continuam pendentes paraFiel na r2 ou hora quieta, com trava. Fiel fecha e responde àBrasa. Nenhum teste adicional executado nesta troca.

## Rodada 2 — conserto 1 aceito (514db7a)

2026-10-17. Leitura independente do diff 124f43d..514db7a, relatório Rodada 2, ticket 08, função, teste completo e lib/locais.mjs. Não consultei o parecer do Fiel desta rodada. Ponta conferida: 514db7ac3af79a8d76c71d62b3b241a67d6dadc6; árvore limpa antes e depois.

**PASSA o conserto 1. Nenhum conserto de código pendente nesta rodada.** O aceite final do ticket continua pendente das evidências Docker combinadas (fatias 1 e 2) e do fechamento pelo Fiel. Este parecer não declara essas fatias aprovadas.

1. Caminhos: a raiz passa por realpathSync.native antes da enumeração por -LiteralPath e do GetRelativePath. Assim a enumeração parte da forma longa, compatível com FullName; não há mais corte por comprimento. As barras de saída são normalizadas para `/`.
2. Pastas locais: a função importa pastasLocais de lib/locais.mjs, a mesma função usada pelo gerador. Exclui descendentes com o limite de componente `pasta/`, preserva o filtro de componentes com ponto e recusa índices ilegíveis. A leitura não executa o gerador nem regrava suas listas.
3. Evidência própria: `pwsh -NoProfile -File agents/code/test/banco/kit-sem-docker.ps1`: **24 PASSA, saída 0**, incluindo os três casos novos. O arquivo de 201 MiB dentro de clientes/rascunho com local: true ficou fora. Raiz com barra final e raiz pelo nome curto produziram exatamente anexos/grande.bin. O nome curto usado nesta execução era efetivamente diferente da forma longa (alias 8.3), portanto esse caso não passou por repetir a mesma grafia.

`git diff --check 124f43d..514db7a`: saída 0. Teste encerrou com `kit sem Docker: tudo passou`; nenhuma tarefa registrada. Sem Docker, harness real ou suíte completa. As ressalvas não bloqueantes acordadas na rodada 1 permanecem. Nenhuma edição em código, spec ou ticket.

## Fechamento acompanhado — 2026-10-17

Li o fechamento do Fiel e a evidência posterior `logs/08-fatias-1-2.log`: 18 PASSA, tudo passou; partida e CLI rodando preservam exclusões, 51 MiB chega íntegro, 201 MiB não entra no banco nem chega ao B, permanece identificável em A, contêineres apagados. Concordo com o PASSA e com retirar as pendências dessas duas fatias à luz desse log. Docker não executado por mim. As ressalvas remanescentes continuam conforme o parecer do Fiel.
