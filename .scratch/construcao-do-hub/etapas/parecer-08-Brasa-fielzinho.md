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
