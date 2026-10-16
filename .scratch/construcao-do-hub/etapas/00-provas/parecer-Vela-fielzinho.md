# Parecer — Vela — ticket 02

Data: 2026-10-16. Revisor: Fielzinho. Rodada 1, leitura independente.
Veredito proposto: **passa**, condicionado à conferência das execuções Docker pelo Fiel.
Nenhum conserto obrigatório encontrado na leitura. Ainda não é o veredito final da dupla.

## Escopo e fontes

Ramo ticket-02, worktree C:/context-hub-wt/ticket-02, HEAD 6191e40f3ca83bf2a2dcf7fddd58577b1cbc1a8f.
Li regras-da-construcao.md e revisao-em-dupla.md, brief 00-provas, ticket de construção 02,
relatorio-pastas-com-ponto.md, ticket resolvido 48 inteiro e o Answer do 12,
spec (Worker 4 e fronteiras comuns) e ticket 06.
Li todos os sete arquivos adicionados pelo ramo, incluindo as duas evidências.
Não li o parecer do Fiel antes de fechar esta leitura.

Fonte primária conferida localmente: C:/Projetos/spike-livesync/livesync-src,
HEAD 14141446a14deab3353a8864dee41e44c372d006:
- src/apps/cli/serviceModules/IgnoreRules.ts, inteiro;
- src/apps/cli/main.ts, carga das regras e filtros de alvo;
- src/apps/cli/managers/CLIStorageEventManagerAdapter.ts, observador;
- src/apps/cli/commands/runCommand.ts, comandos daemon, sync e ls.
A árvore do upstream mostra package-lock.json modificado; não alterei nada nela.
Não reconstruí nem comparei o bundle compilado com os fontes. O ticket 48 já documenta
uma linha de log extra no build do spike.

## Conferência independente

- Ramo inicialmente limpo e HEAD corresponde ao pedido.
- integracao é ancestral de HEAD (git merge-base --is-ancestor: 0).
- Não executei Docker, CLI real ou harness. Fiel é o executor exclusivo da prova.
- A prova usa 5996/5997 e hub-ensaio-02-a/b, com publicação em 127.0.0.1.
  Não toquei em 5994/5995 nem em recursos da Brasa.
- Configuração gerada liga encrypt/usePathObfuscation, algoritmo v2 e sal comum nos dois
  bancos. Credenciais são inventadas por execução. Há uma replicação de envio por par.
- O ignore é escrito em cada cofre antes de Start-Sincronizador. Linhas .* e .*/.
- A prova cria os caminhos exigidos e controles visíveis em duas fases. Na segunda,
  para A, cria novos arquivos e religa preservando configuração e banco local.
- Confere disco B e bancos A/B em ambas as fases; exige que os controles apareçam nos
  três destinos. Isso evita que um sincronizador parado produza apenas negativos verdes.
- O dispositivo leitor faz sync e ls sem --vault e não recebe o ignore do cofre.
  ls enumera findAllNormalDocs, ignora apagados e não aplica filtro de ponto aos nomes.
  Portanto a exclusão da prova não é artificialmente repetida na leitura dos bancos.
- O log com exclusão registra 12 PASSA; sem exclusão registra seis controles PASSA e
  seis FALHA de exclusão. Os caminhos vazados aparecem explicitamente no segundo log.
- A origem primária confirma: .* vira **/.*; .*/ vira **/.*/**; dot:true; normalização
  das barras; negação lança erro; import: .gitignore importa inclusive as negações.
- main.ts:534 divide o caminho normalizado com path.sep; o observador usa a regex
  /(^|[/\\])\./. A diferença explica a falha na partida do Windows descrita no 48.

## Ressalvas para ligar as etapas

1. Caminho do montador: banco.psm1 chama agents/test/hub-de-ensaio/montar.mjs,
   que existe na base integrada desta revisão. O ticket 05 o move para agents/code/test/.
   Ao juntar os ramos, atualizar a chamada e repetir a prova; não copiar a versão antiga
   para contornar a migração. Não bloqueia isoladamente este HEAD anterior ao 05.
2. O relatório deve ser lido com a precisão do log vermelho: na fase “CLI rodando”,
   os vazamentos listados são os arquivos já presentes no hub antes da partida.
   Os arquivos criados com sufixo rodando aparecem vazados depois do reinício.
   O log não demonstra vazamento novo pelo observador durante a primeira fase.
3. Ausência é observada durante a janela da prova (controle + cinco segundos e leitura
   dos bancos), não por tempo ilimitado. A regra no fonte sustenta o resultado.
4. A prova cobre envio A para B e banco novo, não limpeza de conteúdo já vazado,
   plugin do Obsidian ou segunda máquina. O relatório explicita esses limites.
5. Cleanup está no finally e para somente PIDs guardados, mas suprime a saída do compose
   down e não verifica seu exit code. O Fiel deve confirmar separadamente a ausência dos
   contêineres/volumes e processos desta execução, como a construtora declarou.
6. O gerador 06 deve produzir ignore em cada máquina antes da partida, sem negação;
   mudança exige reinício. O arquivo .livesync/ignore não viaja pela própria replicação.

## Pendência de execução e acordo

Aguardando do Fiel: saídas de prova.ps1 e prova.ps1 -SemExclusao, códigos de saída e
confirmação da limpeza. Recomendo passa se repetirem o verde 12/12 e o vermelho de
exclusão com controles chegando, sem recurso remanescente. Só o Fiel fecha e responde
à construtora. Nenhum código, spec, ticket ou configuração global foi editado.

## Acordo da dupla — 2026-10-16, troca 1

Veredito: **passa**. Concordância do Fielzinho com a proposta do Fiel.
Li os dois logs completos da execução do Fiel nesta pasta:
- revisao-02-com-exclusao.log: 12 PASSA, “prova 2: tudo passou”; código 0 informado pelo Fiel.
- revisao-02-sem-exclusao.log: 6 PASSA dos controles e 6 FALHA de exclusão;
  vazamentos nos bancos A/B e disco B nas duas fases; código 1 esperado informado pelo Fiel.

Fiel confirmou após CADA rodada: zero contêineres/volumes hub-ensaio-02-*, zero node.exe
com argumentos hub-ensaio-02 e ausência de TEMP/hub-ensaio-02. A prova da Brasa nas
portas 5994/5995 foi preservada. Esta confirmação de limpeza é do executor Fiel;
não rodei Docker nem inspeção de processos por conta própria.

A dupla aceita as ressalvas já escritas: atualizar caminho do montador ao integrar 05,
precisão da fase “CLI rodando” no vermelho, janela de observação e limpeza conferida
externamente. Sem consertos obrigatórios. Fiel fecha o parecer principal e responde à Vela.
