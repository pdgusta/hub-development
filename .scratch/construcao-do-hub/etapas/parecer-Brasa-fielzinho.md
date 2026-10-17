# Parecer Fielzinho — Brasa, ticket 07, rodada 1

2026-10-17. Veredito independente: **VOLTA**, três consertos reproduzidos. Acordo com o Fiel e logs reais dele pendentes. Sem leitura do parecer do Fiel.

## Base

Ramo ticket-07, worktree C:/context-hub-wt/ticket-07, HEAD 7fa0e56e04fa30f2236f34b6b68ccffca13cf822. Limpa. integracao 8d1d785ab8102f3ac81f1c48cce261b8af4f8934 é ancestral (saída0). Ticket07/relatório/regras/revisão em dupla lidos inteiros; núcleo/Worker4 do spec já lidos na sessão e faixa4 lida; Answers dos tickets resolvidos25/33/34/47/48 conferidos; tickets08 e23 lidos para conferir fronteiras; código/testes/diff das provas lidos. Docker exclusivamente Fiel. Não rodar ponta-a-ponta/ nem provas/03-codex-hooks/. Não editei código/spec/tickets e não usei subagentes.

## Achados independentes já reproduzidos

1. **Identificar o sincronizador além do PID e do nome node.** banco.psm1:211–216 aceita qualquer processo node que ocupe o PID do arquivo. Stop-Sincronizador:236–237 mata esse processo, e Start-Sincronizador:219 deixa de iniciar o daemon por achá-lo vivo. Reprodução própria sem Docker: abri um node inofensivo com setInterval (sem CLI nem banco), gravei só o PID dele no arquivo de ensaio; Get-PidSincronizador devolveu esse PID como sincronizador. PID reutilizado depois da queda/reinício do daemon pode parar outro node do usuário ou impedir a subida. Guardar/conferir identidade do processo (início e comando/CLI/banco/hub) antes de reutilizar/parar. Não matei processo alheio: o único node aberto pela reprodução foi encerrado pelo próprio pai no finally.

2. **Conferir configuração existente antes de reutilizar o dispositivo.** banco.psm1:185 retorna imediatamente se settings.json tem isConfigured:true. Não confere destino, cifra, caminho ofuscado, frase-senha ou limite. Reprodução própria sem Docker/CLI: .env gerado com Cifra:true e Db:hub; settings.json de ensaio isConfigured:true, encrypt:false, usePathObfuscation:false, banco outro-banco. Initialize-Dispositivo retornou normalmente e preservou tudo divergente. Assim, o kit pode anunciar o par novo enquanto o daemon usa outro banco ou grava sem cifra, contrariando entrega e critério nada em claro. Recusar divergência com diagnóstico ou reconciliar de forma segura; não refazer silenciosamente o dispositivo. Provar idempotência no caso correto e recusa/configuração segura no divergente.

## Verificações próprias até aqui

- Parser PowerShell dos sete arquivos .ps1/.psm1 alterados e existentes: sem erros.
- Passo real 04-banco.ps1 -EnvFile <ensaio> -WhatIf: seis passos simulados, arquivos/hashes da pasta de ensaio iguais antes/depois, saída0. Sem Docker.
- Reproduções acima: Node pai cria pasta hub-ensaio-07-revisao-* e script PS temporário; módulo real do ramo importado. Sem mocks nem serviços. Pasta apagada pelo próprio pai em finally, após conferir diretório absoluto/prefixo. Saída0.

## Evidência da Brasa já conferida

Logs .local/07-verde-2.log:24PASSA,saída0; prova01-2.log:17PASSA+2VÊ,saída0; prova02-2.log:12PASSA,saída0;06-2.log:14PASSA,saída0. Consistentes com o relatório. A prova01 registra113 arquivos/28,1s; 07 registra104/53,2s. São logs da construtora, não execução minha. Aguardar os logs próprios do Fiel para encerrar aceite real e limpeza.

## Próximo passo

Concluir confronto com tickets resolvidos25/33/34/47/48 e costuras; enviar parecer ao Fiel; ler logs novos dele; fechar acordo. Fiel fecha veredito e responde à Brasa.

## Terceiro conserto

3. **Retomar mark-resolved depois de falha na aceitação do dispositivo.** banco.psm1:197–200 grava isConfigured:true antes de chamar mark-resolved e exigir ACCEPTED. Se a aceitação falha, o passo lança erro, mas a próxima chamada cai no retorno antecipado da linha185. Reprodução com CLI de ensaio que cria settings no init-settings, deixa remote-add terminar e faz mark-resolved sair1: primeira chamada lançou “mark-resolved falhou”; segunda retornou normalmente; registro do CLI mostrou mark-resolved chamado uma única vez; settings.isConfigured seguiu True. O dublê só injeta falha no CLI, sem Docker/rede; não é evidência de sync real. Marcar conclusão apenas após aceitação ou registrar/conferir a etapa pendente e retomá-la sem refazer o dispositivo. A aceitação de dispositivo novo é requisito dos tickets resolvidos33/48 e do spec, não melhoria de robustez opcional.

## Confronto final com fonte e costuras

- Os Answers25/33/34 confirmam banco LiveSync, S3 com envio de cada par, vista viva no disco e E2EE. O Answer48 confirma caminho de init-settings/remote-add e aceitação por mark-resolved, e a necessidade de preservar o dispositivo (refazê-lo pode perder a base histórica comum).
- No caminho novo, o módulo sobe CouchDB3.5.2 com senha, ini separado por par, sal comum antes do dispositivo, replicação persistente em _replicator, configura encrypt/usePathObfuscation e limite200, gera exclusão antes do daemon. compose publica só127.0.0.1. A extração deixa uma única cópia do módulo/compose/ini; provas01/02 e sincronizador06 usam ensaio.psm1 sobre o módulo real do kit.
- O teste07 lê as duas folhas pelo dispositivo leitor, além de procurar _conflicts, e confere nomes/trechos do hub nos dois bancos crus. O confronto da cópia inicial também usa hashes. Evidência mais forte que contar só documentos.
- O novo caso de pasta local prova PID trocado e controle chegando enquanto nota local fica. Não garante apagar algo que já vazou: isso pertence ao fluxo do ticket28, e a vigia16/gerador chamam a manutenção. Ressalva do relatório é pertinente.
- Limites60/201MiB, binário recuperável, laço que religa e retrato do banco têm dono explícito no ticket08. Não os cobro como entrega nova do07. Tarefa/serviço de verdade segue proibido no ensaio. Segunda máquina/tailnet e distribuição do build/sal são ressalvas legítimas; não foram provadas por esses logs locais.
- A rodada antiga de node --test do relatório chamou harness indevidamente e teve hash divergente; a causa não foi apurada. Não usei essa execução como prova própria nem reexecutei essas pastas. O07 não altera JavaScript de aplicação; verificação própria foi parser, WhatIf e reproduções focadas do módulo.
- A leitura apontou ainda comparação incompleta na idempotência de Set-ReplicacaoEnvio: compara URLs/usuários, mas não senhas. Fica observação de manutenção de credenciais, sem novo conserto nesta rodada, pois troca de credencial não está no critério do07. Não anunciar que o kit reconcilia qualquer alteração do .env.

## Conversa em dupla

Leitura independente encerrada. Enviar três achados ao Fiel, aguardar os logs Docker dele e fechar acordo. Não há execução própria de Docker/harness. Fiel fecha e responde à Brasa.

## Logs próprios do Fiel — acompanhamento

Leitura parcial de etapas/revisao-07-r1-07-banco.log enquanto a execução ainda está em andamento: WhatIf e subida A/B passaram; replicação A em running falhou (estado vazio); B em running passou. Ainda não é resultado final. Não executei Docker nem alterei a rodada dele. Aguardar diagnóstico/log completo antes do acordo.
