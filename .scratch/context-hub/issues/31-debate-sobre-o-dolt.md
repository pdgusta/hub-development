# Debate sobre o Dolt

Type: task
Status: resolved

## Question

O Dolt (caminho O2) deve ser o caminho do hub, ou ficar como reserva? Dois agentes no Maestri
debatem: um defende o Dolt e o outro o contraria, com base nas pesquisas 24 e 27 e nos caminhos O1 e
O3-C. Claude dá o veredito final. Pedido do Gustavo em 2026-10-04 (R8). Insumo de "Como a verdade
viaja entre as máquinas".

## Comments

- 2026-10-04: debatedores no Maestri: Basalto (Claude Code, papel "Defensor do Dolt") e Cardo (papel
  "Crítico do Dolt"; o preset Codex não subiu e foi trocado por Claude Code). O Gustavo pediu que eles
  conversem entre si: debate direto, conduzido pelo Cardo, em 6 turnos, transcritos na nota "Debate
  Dolt" do canvas. A abertura do Basalto foi recuperada pelo Gustavo e colada na nota. O veredito
  final é de Claude, e a transcrição vai para `exploracao/anexos/debate-31-dolt.md`.
- 2026-10-04: debate encerrado em 6 turnos. Depois do fim, os turnos 4 a 6 sumiram da nota (uma
  regravação com versão velha). Recompus a nota a partir da leitura completa feita antes.

## Answer

Transcrição: [`debate-31-dolt.md`](../../../exploracao/anexos/debate-31-dolt.md). Veredito de Claude, 2026-10-04:

**O Dolt fica como reserva nomeada, não como caminho.** A ordem dos spikes é **Fast Note Sync
primeiro**, depois **CouchDB e LiveSync**.

- **O ponto que decide:** pelos critérios do Gustavo, o que pesa é a parte que ele vê, a vista `.md`
  de mão dupla. Ela vem pronta no FNS e no LiveSync e não existe no Dolt (de 3 a 6 dias de ponte
  própria, de 9 a 20 dias no total). Os dois debatedores concordaram nisso no fechamento.
- **O melhor argumento do Dolt é real, mas não é exclusivo:** o motor recusa o commit com colisão.
  O Cardo mostrou que o O1 também não perde o lado vencido (o CouchDB guarda os ramos em
  `_conflicts` e o LiveSync pergunta) e que o FNS recusa no servidor (código 530 com `baseHash`).
  A diferença entre "regra do motor" e "regra do servidor ou da árvore de revisões" não aparece nos
  critérios.
- **O que a periferia do Dolt custa:** o `dolt-mcp` tem 19★ e está na v0.3.8, o remote git é recente,
  e a ponte seria código nosso, sem usuários. O Basalto concedeu os três pontos.
- **A granularidade favorece o O1:** o LiveSync junta trechos que não se sobrepõem; o Dolt e o FNS
  decidem por nota inteira.
- **A sonda de meio dia** (trigger que recusa versão velha; branch criada a partir de um commit, com
  DOLT_MERGE em colisão) é barata e justa, e ambos a aceitaram. Virou o ticket opcional "Sonda do
  Dolt"; ela só decide se a reserva sobe, e não trava nada. Roda se o Gustavo quiser.
