# Ticket 41 — Trilho — parecer independente do Fielzinho

2026-10-17. Leitura tardia de r1 8497eb7 e r2 6a728a40026de86e22e9b1e147743322e19025f5. Worktree C:/context-hub-wt/ticket-41 limpa antes/depois; c42ffa0 ancestral. Parecer do Fiel ainda não lido ao registrar esta análise.

## Veredito proposto: PASSA na r2

Sem conserto novo. O diff próprio sobre c42ffa0 separa agents/code/** exclusivamente na lista da busca. As listas de sincronização e git não ganham essa exclusão. iniciar.ps1 gera e lê a lista a cada partida. O hook usa o caminho real relativo ao hub, com barras normalizadas, e dispensa aviso somente sob agents/code/. A r2 documenta a exclusão e a leitura pelo caminho em agents/skills/busca/SKILL.md; na r1 essa explicação não existia.

Conferidos ticket41 (mandato do maestro), spec Worker3 e aviso de leitura em spec-partes/faixas-05-06, decisões resolvidas09 (Answer) e11 (rodadas3/4 e Answer). A leitura pelo caminho é compatível com busca como porta de entrada, não única; a exceção técnica decorre do mandato41. Fonte primária do mecanismo: C:/Projetos/bancada-busca/ohs/node_modules/obsidian-hybrid-search/README.md, linhas495 e502-509: padrões separados por vírgula, folder/** exclui a árvore, include não vence ignore.

## Evidências

- Próprios na ponta6a728a4: node --test --test-concurrency=1 agents/code/test/15-leitura.test.mjs agents/code/test/gerar-exclusoes/gerador.test.mjs. 18/18, zero pulados, saída0,34,1s. Log: logs/fielzinho-41-leves.log. A política de exclusão do pacote real é exercitada sem servidor/indexação; os hooks recebem eventos sintéticos, sem harness real.
- git diff --check c42ffa0 6a728a4 sem erros. Somente o corpo da skill muda entre r1 e r2; cabeçalho intacto.
- Log Trilho logs/trilho-41-leves-2.log:58/58. Não repeti vigia/tela, que não foram alteradas pelo41.
- Log Trilho logs/trilho-41-12-busca-com-docs.log:9/9, primeira partida50139ms/indexação38s, segunda45480ms/indexação0s,252 notas reaproveitadas. O teste novo grava página de agents/code/docs antes e depois da partida, consulta os três modos e confere a contagem do índice. A presença das14 páginas na worktree provisória é descrita no relatório; não a reinspecionei retroativamente.
- 12-busca da ponta r2 reservado à junção pelo maestro. Não rodei indexação, suíte inteira, Docker, instalação ou harness real. Evidência pesada lida, não produzida por mim.

## Acordo

Pendente de conversa com Fiel. Nenhum código, spec ou ticket editado.

Acordo confirmado pelo Fiel nesta conversa: PASSA na r2, registrado por ele. Ressalva anterior sobre avisos em ponto/local aceita, sem conserto no41.

