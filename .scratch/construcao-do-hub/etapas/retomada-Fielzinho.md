# Retomada — Fielzinho

Atualizada 2026-10-17. Revisor parceiro do Fiel. Planejamento C:/Projetos/context-hub; código C:/context-hub. Sem subagentes; não editar código/spec/tickets; nada global. pt-BR curto. Releia inteiros revisao-em-dupla.md e regras-da-construcao.md; maestri list. Fiel fecha e responde ao construtor.

## Duas revisões agora

### 07 — Brasa, rodada1

Ramo ticket-07, worktree C:/context-hub-wt/ticket-07, HEAD7fa0e56e04fa30f2236f34b6b68ccffca13cf822; integracao8d1d785 ancestral, limpa. Leitura independente concluída, **VOLTA**, três achados no parecer etapas/parecer-Brasa-fielzinho.md. Enviados por maestri ask Fiel (sessãoexec36961 ainda esperando; Fiel já confirmou recebimento em nova mensagem). Docker somente Fiel:07-banco,prova01,prova02,sincronizador06. Logs novos prometidos em etapas/revisao-07-r1-*.log. Não li parecer dele.

Achados reproduzidos semDocker:
1.Get-PidSincronizador aceita outro node pelo PID/nome e Stop pode matar alheio. Usei node inofensivo próprio, encerrado pelo pai; nenhum processo alheio tocado.
2.Initialize-Dispositivo retorna por isConfigured:true com banco errado/encrypt:false/ofuscação:false apesar envCifra:true.
3.isConfigured salvo antes mark-resolved; falha na aceitação deixa próxima chamada retornar sem aceitá-lo. CLI dublê local injeta falha, mark-resolved chamado só1vez em2tentativas.
Parser7arquivosPS e passo real WhatIf com hashes iguais, saída0. Reproduções em temp próprias apagadas finalmente. Logs daBrasa lidos:24PASSA,17PASSA+2VE,12PASSA,14PASSA, todos saída0. NãoexecuteiDocker. Limites/laço/retrato são08, não cobrar07. Senha da replicação não comparada fica observação, não conserto novo.
Próximo: ler logs próprios doFiel quando avisar; discutir3achados e registrar acordo.

### 27 — Vela, rodada2

Novo pedido doFiel recebido enquanto07roda. Ramo ticket-27, worktree C:/context-hub-wt/ticket-27, HEAD5df8972d1677a37f4df7c38156ddf094812c68b9, limpa, integracao8d1d785 ancestral. Diff8d8f1b9..5df8972 e relatório atualizado lidos; cinco consertos parecem atendidos. **Não li parecer novo doFiel.**
Teste seguro rodando: node --test "agents/code/test/*.test.mjs" agents/code/test/gerar-exclusoes/gerador.test.mjs, sessãoexec29744. Não repetir: coletar resultado. Esperado106/106 (relatório). Ainda não gravei rodada2 no parecer; próximo passo coletar resultado, registrar revisão dos5consertos em etapas/parecer-Vela-fielzinho.md e conversar comFiel.
Evidência nova dos3harnesses lida sem rodar/importar: marca,devolve .secrets,solta semfalta, Copilot continuacao:true. Registro inclui faltas/avisos. hashes-claude-codex-copilot.json:8hashes iguais,3pastas apagadas. Evidência é de falta, não aviso isolado; testes semharness cobrem aviso pelo canal.
Consertos:r2 protege nomes; semarquivos retorna semCLI; avisos entram emdevolução informativa semgastarconta e registro; URIError tratado porlink e subprocesso caído devolvido; par://.secrets recusado. Fora dohub permanece ressalva aomaestro, acordo darodada1.

## Regras de testes

Nova regra: não rodar ponta-a-ponta/ nem provas/03-codex-hooks/. Até29entrar, nunca globrecursivo de todosostestes. Docker/harness sóFiel. .mjs de ponta a ponta roda aoimportar. Rootglob agents/code/test/*.test.mjs + gerador específico é seguro.

## Anteriores

27r1:VOLTA nos5consertos, acordoFiel registrado em parecer-Vela-fielzinho.md.14Trilho passou emdupla, parecer-Trilho-fielzinho.md.05,02,01,06 passaram; pareceres nas subpastas de etapas. Todososachados/evidências emarquivos. Não há decisão exclusiva nochat.

## Atualização posterior

27 rodada2: testes próprios concluídos106/106, saída0,126,0s. Parecer-Vela-fielzinho.md atualizado: PASSA independente. Pedido de acordo enviado aoFiel por maestri ask, sessão98049 pendente. Semnovo bloqueio; todosos5consertos aceitos. Nenhumharnessreal.
07: log próprio doFiel lido parcialmente. WhatIf/subidaA/B verdes; replicaçãoAemrunning falhou(estado vazio),Bpassou. Não éresultadofinal. Registrar diagnóstico dele antes de fechar. Ramo07continua7fa0e56.

## Acordo 27 concluído

Fiel confirmou PASSA na rodada2, fechamento em etapas/parecer-Vela.md. Acordo registrado no parecer próprio. Sem pendência no27; aguardando somente07 (Docker e conferência dos três achados pelo Fiel).
