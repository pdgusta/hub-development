# Parecer — Brasa — ticket 01

Data: 2026-10-17. Revisor: Fielzinho. Leitura independente.
Veredito proposto: **passa**, pendente apenas de confirmar com Fiel a limpeza das suas execuções.
Nenhum conserto obrigatório encontrado. Não li o parecer principal.

## Escopo e evidência

Worktree C:/context-hub-wt/ticket-01, HEAD 0c8c63965d3c3f1b6efa323a03a83124019e8fce,
ramo limpo. Base 0d04985 ancestral (exit 0). Li ticket 01, brief, regras, Worker 4,
relatório, Answers dos tickets resolvidos 30/33/34 e ticket 48, já lido inteiro.
Li prova.ps1, banco.psm1, compose e ini. A mudança desde 246393b na prova é o caminho
do montador para agents/code/test, consistente com 05. A ponta corrente de integracao
pode avançar durante esta revisão; não alterei ramo nem worktree.

Conferi os logs originais .local/prova1-cifra.log e prova1-SemCifra.log (saída 0),
prova1-SemSalComum.log (saída 1) e contraprova-b-sync.log (OperationError).
Conferi os logs do Fiel revisao-01-r1-cifrada.log e revisao-01-r1-manter.log:
ambos terminam em “prova 1: tudo passou”, saida=0, com os 90 arquivos do hub atual.
Contagem precisa: cada log tem 17 linhas PASSA e duas linhas VÊ (os discos em conflito).
Não são 19 asserções PASSA. É ajuste de contagem, sem impacto no veredito.

## Aceites conferidos

- Duas tarefas de envio, uma em cada _replicator, confirmadas running.
- Conteúdo inicial comparado por caminho e hash; criação, edição e exclusão nos dois sentidos
  comparadas pelo texto ou pela ausência no destino.
- Após pausa da replicação e edições concorrentes, cada banco apresenta conflito e o leitor
  sync/info/cat-rev recupera as duas versões esperadas da nota específica. A subida de update_seq
  isoladamente seria evidência fraca; a conferência final das duas folhas cobre esse limite.
- E2EE v2 e caminho ofuscado ligados, sal comum gravado antes dos dispositivos. Busca nos docs
  crus não acha os marcadores e nomes da prova. Isso é busca de marcadores, não prova universal
  sobre todo byte de qualquer documento. Fiel informou sonda adicional de nomes do hub sem
  vazamento; não a tomei como evidência própria nem li seu parecer para obtê-la.
- SemSalComum deixa cada banco gerar seu sal e falha na decifragem na evidência original.
- Contêineres definidos só em 127.0.0.1:5994/5995; credenciais de ensaio, ini separado por par,
  processos guardados por PID. Não executei Docker, CLI real, harness ou comandos de limpeza.

## Ressalvas para as próximas etapas

1. A prova 01 não instala as exclusões da 02; o filtro de comparação do hub pula caminhos
   com ponto. Portanto esse verde não afirma que pastas ocultas não vazam. Juntar o ignore
   antes da partida no kit 07; prova específica disso é 02/06.
2. O teste de cifra procura marcadores nos documentos retornados por _all_docs, e não faz
   inspeção exaustiva de todas as folhas/revisões. As duas folhas são recuperadas para provar
   preservação, sem alegar auditoria criptográfica integral.
3. Remove-EnsaioBanco suprime a saída/erro de remoção e não valida exit do compose down.
   A limpeza precisa da confirmação externa do executor, como em 02.
4. Tarefas agendadas, plugin, tailnet, segunda máquina e limites de arquivo são outros tickets.
   O relatório explicita isso e os requisitos do sal e do ini por par para o kit.

Nada de código/spec/tickets/global editado. Fiel fecha o acordo e responde à Brasa.

## Acordo da dupla — 2026-10-17

**Passa.** Fiel aceitou a leitura independente e corrigiu a contagem para 17 PASSA + 2 VÊ.
Confirmou limpeza: execução cifrada pelo finally; na execução -Manter, parada manual dos
PIDs 164840/180044, compose down -v e pasta apagada. docker ps -a e volume ls filtrados
por hub-ensaio-00 ficaram vazios, conforme a conferência do Fiel. Não executei esses comandos.
Fiel registrou o fechamento conjunto no parecer principal. Sem conserto pendente.
