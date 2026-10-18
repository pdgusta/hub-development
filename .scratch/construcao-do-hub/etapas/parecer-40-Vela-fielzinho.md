# Ticket 40 — Vela — parecer independente do Fielzinho

2026-10-17. Ramo ticket-40, worktree C:/context-hub-wt/ticket-40, ponta535d86b. Lidos db6b52c e a curta e581b96/535d86b, sobre e7203b4. Parecer do Fiel ainda não lido.

## Leitura independente

Sem achado novo no escopo. A seção Roteamento de skills está depois de cabeca:fim, transcreve a regra entregue pelo relatório19 e a curta explicita a conjunção dos gatilhos. Conferi a tabela routing.yml e a função indicar: alternativas dentro de palavras, conjunção entre palavras/caminho/papel. O montador copia AGENTS.md da raiz, sem outra versão do texto.

Fontes do requisito: ticket40; relatório19 seção Texto da regra no contrato; spec-partes/faixas-09-10 (Hook de entrada); Answer do ticket resolvido15-roteamento-de-skills (onde não injetar, regra no contrato). A alegação sobre o Copilot é premissa documentada do19, não uma nova medição minha. Uso efetivo da skill pelo Copilot real continua não verificado, explicitamente no relatório40.

## Verificações em andamento

- conferir-cabeca.mjs:1691/2000; diff check e7203b4..535d86b sem erros; worktree inicialmente limpa.
- Teste próprio19-roteamento iniciado, sessão48195, log logs/fielzinho-40-roteamento.log; aguardar término, não duplicar. Sem harness real/Docker.
- 52/52 do relatório40 é declaração da Vela; não localizado log dedicado40 nesta leitura. Não afirmo reprodução desse conjunto.

Veredito e acordo pendentes do teste. Nenhum código/spec/ticket editado.

## Veredito independente: PASSA na curta535d86b
Teste próprio encerrado:20/20,zero pulados,saída0,133,6s. Log logs/fielzinho-40-roteamento.log. Nenhum teste ativo. O teste novo confere a regra na cópia montada e o limite da cabeça. Sem achado novo; acordo comFiel pendente.

