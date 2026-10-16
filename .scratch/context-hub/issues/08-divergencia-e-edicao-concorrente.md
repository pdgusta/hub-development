# Divergência e edição concorrente

Type: prototype
Status: resolved
Blocked by: 06, 07

## Question

O que conta como divergência "não silenciosa", onde o aviso aparece, e como tratar a edição
concorrente entre máquinas e entre dois agentes na mesma máquina (critérios 4 e 5)? O protótipo
reproduz os dois cenários numa cópia descartável para a conversa reagir a algo concreto.

## Comments

- 2026-10-02: protótipo de lógica em
  [`prototipo-08-divergencia.html`](../prototipos/prototipo-08-divergencia.html) (abre com dois
  cliques; tudo em memória, sem git de verdade). Simula as duas máquinas, o GitHub, um sincronizador
  por máquina no estilo do git-sync (intervalo de 15 min) e dois agentes no notebook. As políticas em
  aberto são chaves: colisão entre máquinas (parar e avisar / cópia irmã), dois agentes na mesma
  máquina (nenhuma / conferir a versão ao gravar / trava por arquivo) e o limite do aviso. Oito
  roteiros: caminho feliz; mesmo arquivo em linhas diferentes; colisão real; sincronizador parado em
  silêncio; sem rede; dois agentes no mesmo arquivo; o sincronizador também grava; trava esquecida.
- 2026-10-02: rodada 1 em `respostas.md` (Q1 o que conta como divergência; Q2 onde o aviso aparece;
  Q3 colisão real entre máquinas; Q4 dois agentes na mesma máquina). Achado do protótipo que pesa na
  Q4: o sincronizador também grava no disco, então sem conferir a versão um agente pode desfazer uma
  edição vinda da outra máquina, e o sync leva o estrago de volta sem alerta nenhum (roteiro 7).
- 2026-10-02, respostas da rodada 1: "ok" na Q1 e na Q2; "ok pra recomendação" na Q3 e na Q4.

## Answer

Decidido com o Gustavo em 2026-10-02, depois de rodar o protótipo.

1. **Divergência são três situações, e só elas:** colisão real (as duas máquinas mudaram a mesma
   linha entre duas syncs); máquina sem sincronizar com sucesso há mais de 30 min (dois ciclos), com
   ou sem edição pendente; cópia de conflito aberta (não ocorre com a política escolhida no item 3,
   mas fica na definição). Mudanças em linhas diferentes do mesmo arquivo não contam, porque o git
   junta. Máquina desligada não conta. "Divergência" e "colisão real" entraram no glossário.
2. **O aviso aparece em dois canais, na máquina que travou:** uma notificação do Windows disparada
   pelo sincronizador quando ele falha, e uma checagem no início de toda sessão de agente, que lê o
   estado do sync daquela máquina. Só a checagem pega o sincronizador parado. A outra máquina não tem
   como saber de uma edição que não chegou ao GitHub. Como cada harness faz a checagem vai para
   "Acesso dos agentes: decisão". **Não verificado:** notificação do Windows a partir de tarefa
   agendada em Git Bash; hook de início de sessão no Codex e no Copilot.
3. **Colisão real entre máquinas: parar e avisar, com a junção desfeita.** A máquina com a colisão
   para de enviar tudo, o disco fica com a versão local limpa, sem marcadores de conflito, e um agente
   resolve na sessão que recebe o aviso, com o Gustavo vendo. O git-sync deixa o rebase pendente por
   padrão; o sincronizador do hub desfaz a junção antes de parar. Custo aceito: enquanto não se
   resolve, nem as edições sem colisão daquela máquina saem.
4. **Dois agentes na mesma máquina: conferir a versão ao gravar.** A garantia é que nenhuma gravação
   desfaz outra sem que o agente veja: se o arquivo mudou desde a leitura, a gravação é recusada e o
   agente relê e refaz. O sincronizador conta como mais um escritor no disco; é por ele que a trava
   por arquivo não serve. Como cada harness e o MCP conferem a versão vai para "Como os agentes gravam
   no hub". A edição do Gustavo no Obsidian fica sem proteção (fora de escopo). **Não verificado:**
   quais ferramentas nativas de edição já recusam gravar um arquivo que mudou desde a leitura.

Para a construção: o sincronizador de cada máquina é um envoltório do git-sync (ou equivalente) com
`syncNewFiles`, intervalo de 15 min pelo Agendador do Windows, junção desfeita na colisão,
notificação na falha e um estado local (última sync ok, colisão) que a checagem de sessão lê.

Protótipo: [`prototipo-08-divergencia.html`](../prototipos/prototipo-08-divergencia.html).
- 2026-10-04 (vinda de "Markdown: vista ou fonte da verdade"): em revisão: a definição de divergência e a conferência de versão continuam valendo como garantias; o mecanismo (colisão por linha no git, sincronizador git-sync) depende de "Sync de banco entre duas máquinas pares".
- 2026-10-13 (vinda de "Revisão do sync e da divergência com o banco", resolvida):
  revisão fechada. As garantias ficam (o que conta como
  divergência, aviso por notificação e checagem de sessão, conferência de versão); o mecanismo muda:
  colisão segura só a nota (texto) ou fica com o mais novo e a vigia avisa (binário), em vez de parar a
  máquina; sync parado é a outra máquina ligada e sem troca há mais de 15 min; arquivo acima de 200 MiB
  também conta; a vigia (a cada 5 min) substitui o envoltório do git-sync. Detalhe no Answer de lá.
