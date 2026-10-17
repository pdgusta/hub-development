# Retomada — Fielzinho

Atualizada em 2026-10-17. Revisor parceiro do Fiel. Planejamento em C:/Projetos/context-hub; código em C:/context-hub.
Respostas em pt-BR, curtas. Sem subagentes; não editar código, spec ou tickets; nada global. Ao retomar, leia inteiros
revisao-em-dupla.md e regras-da-construcao.md e rode maestri list. Fiel fecha o veredito e responde ao construtor.

## Pendente: ticket 07, Brasa, rodada 1

Ramo ticket-07, worktree C:/context-hub-wt/ticket-07, HEAD 7fa0e56e04fa30f2236f34b6b68ccffca13cf822. Na revisão,
integracao 8d1d785 era ancestral; agora integracao avançou para 0a8e17f com o27. Parecer próprio:
etapas/parecer-Brasa-fielzinho.md. **VOLTA independente; acordo ainda pendente.**

Três achados enviados ao Fiel por maestri ask; ele confirmou recebimento e ainda vai conferir:
1. Get-PidSincronizador aceita qualquer node no PID salvo; Stop pode matar outro processo e Start não subir o daemon.
   Reproduzido com node inofensivo próprio, encerrado pelo pai. Nenhum processo alheio tocado.
2. Initialize-Dispositivo aceita isConfigured:true mesmo com banco errado e cifra/ofuscação desligadas, apesar do env cifrado.
3. isConfigured salvo antes de mark-resolved; após falha na aceitação, segunda chamada retorna sem repetir a aceitação.
   CLI dublê local provou uma chamada mark-resolved em duas tentativas.

Verificações próprias: parser dos sete arquivos PowerShell alterados, sem erros; passo real -WhatIf sem mudar hashes;
reproduções focadas sem Docker, temporários próprios apagados em finally. Logs da Brasa conferidos:24PASSA,
17PASSA+2VÊ,12PASSA,14PASSA, todos saída0. Limites/laço/retrato são do08. Não cobrar no07.

**Docker só Fiel**:07-banco,prova01,prova02,sincronizador06. Logs prometidos em etapas/revisao-07-r1-*.log.
Última leitura parcial do log07:WhatIf e subidaA/B passaram; replicaçãoA em running falhou(estado vazio),B passou.
Não é resultado final. Próximo passo: receber logs/diagnóstico e avaliação dos três achados; registrar acordo.
Não reenviar o pedido igual. Não li parecer do Fiel para substituir a análise própria.

## Ticket 29, Brasa, rodada 1: encerrada em VOLTA

Ramo ticket-29, worktree C:/context-hub-wt/ticket-29, HEAD 02667615efb76a291b5839f0c7770f9d15dffe22.
Parecer próprio separado do07: etapas/parecer-29-Brasa-fielzinho.md. Fiel fechou em etapas/parecer-29-Brasa.md.
Acordo VOLTA nos dois consertos:
1. Meu: incorporar integracao0a8e17f e proteger também ponta-a-ponta/27-fim-da-resposta.test.mjs. Na ponta integrada,
   ele apaga evidência no topo e chama três harnesses sem flag. O29 antigo só cobre03/14. Incluir27 na prova sem flag.
2. Fiel, aceito: prova sem harness deve detectar chamada a harness fora da proteção; não depender só de nomes fixos.

Teste próprio na árvore antiga29, com flag removida do env do filho:86testes,83passam,3pulados,saída0,84,2s.
SHA256 de todos os arquivos versionados antes/depois:nenhum alterado. Log no ramo:
.local/revisao-fielzinho-29-sem-variavel.log. Nenhuma execução com HUB_HARNESS_REAL=1. Evidências opt-in da Brasa
lidas:11/11,hashes14 iguais,pastas/login apagados. Sessões de ask e de teste já encerradas. Sem acordo pendente.
Próximo passo: aguardar correção da Brasa ou outro pedido do Fiel.

## Ticket 27, Vela, rodada 2: PASSA em dupla

HEAD 5df8972d1677a37f4df7c38156ddf094812c68b9, worktree C:/context-hub-wt/ticket-27. Integrado em0a8e17f.
Cinco consertos aceitos:nomes protegidos,turno sem escrita,avisos ao agente/registro,URI e queda do subprocesso,
par:// para .secrets. Parecer próprio etapas/parecer-Vela-fielzinho.md; fechamento do Fiel etapas/parecer-Vela.md.
Testes próprios106/106,saída0,126s. Evidência real lida:três devolvem e soltam;Copilot continuação;8hashes iguais;
3pastas apagadas. Não executei harness. Fora do hub fica ressalva ao maestro. Sem acordo pendente.

## Regras e armadilhas

- Até29 corrigido e integrado, não rodar glob recursivo da suíte em integracao:27 ainda chama harness sem flag.
- No ramo29 revisado, a suíte inteira foi autorizada sem flag. Em qualquer revisão, **não ligar HUB_HARNESS_REAL=1**
  sem pedido específico. Docker/harness só Fiel nas revisões atuais. .mjs de ponta a ponta pode executar ao importar.
- Não importar testes para conferir sintaxe. Ler primeiro a proteção e os efeitos no topo.
- integracao anda; registrar HEAD/base sem fazer merge pelo revisor.
- mtime Windows pode ficar anterior a Date.now dentro do mesmo milissegundo: reproduções usam utimes explícito.
- Maestri ask pode ficar esperando; não reenviar pedido igual. A resposta chega como nova mensagem.
- Todos os achados e acordos estão nos pareceres. Nenhuma decisão depende só do chat.

## Revisões anteriores

14 Trilho passou em dupla:etapas/parecer-Trilho-fielzinho.md.05,02,01,06 passaram; pareceres nas subpastas de etapas.
