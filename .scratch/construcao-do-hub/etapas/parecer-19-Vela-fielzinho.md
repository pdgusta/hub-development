# Ticket 19 — Vela — leitura independente tardia do Fielzinho

2026-10-17. Ponta 52c632862aeeb3a84735a145dcc1457faf69203f, worktree C:/context-hub-wt/ticket-19, limpa. Ticket já integrado/resolvido pelo Fiel; este parecer não altera ticket nem veredito dele. Leitura independente sem consultar o parecer do Fiel. Li ticket, relatório, código do roteamento/entrada/estado/uso/mod, testes, Worker 9 do spec, faixa 9 e ticket resolvido 15.

Estado: revisão em conclusão; teste próprio `node --test agents/code/test/19-roteamento.test.mjs` em execução (sessão 13674; pai 209324, filho 206420). Sem Docker nem HUB_HARNESS_REAL. Não repetir enquanto roda.

## Achados

1. **O registro esconde skills indicadas que não rodaram quando outra da mesma linha rodou.** Em fecharTurno, registro.mjs: `rodou` vira sim se `rodaram.length` é diferente de zero; coluna skill passa a conter somente rodaram, descartando as demais. As linhas reais Tech lead/UX/UI têm várias skills. Se só regua-da-cidade rodar, information-architecture e concept-selection não ganham registro de não execução. Isso enfraquece justamente a medição decidida no 15, rodada 1: saber qual skill indicada não rodou para ajustar a linha. Recomendação: uma indicação por skill, mantendo o mesmo id da linha, com sim/não próprio. Achado por leitura; testes atuais usam uma skill por linha no fechamento.

2. **O caminho Windows com barra invertida pode ser eliminado antes de normalizar.** caminhosDoPedido filtra por `/` ou final `.md`, e só depois troca `\` por `/`. Reprodução própria somente em memória, importando indicar: linha `{id:'x', caminho:'**/research/**', skills:['busca']}`; `Leia initiatives/teste/research/dados.json` devolve x, `Leia initiatives\teste\research\dados.json` devolve lista vazia. `.md` seguido de ponto final também não passa no filtro antes de tirar a pontuação. Recomendação: normalizar barras e tirar pontuação antes de selecionar tokens de caminho; cobrir ambas as grafias.

## Evidência real da Vela conferida

- Claude: saída contém additionalContext, leitura da skill de ensaio e resposta ROTEADO-PELO-FREELLMAPI; registro tem uso e indicação sim para freellmapi.
- Codex: resposta cita a instrução do hub e freellmapi, mas diz que a skill não está disponível. Prova injeção, NÃO execução da skill. Registro não verificado condiz com a limitação.
- Copilot: registro indicação não verificado. A prova não demonstra execução pela regra do contrato; o relatório entrega essa regra à faixa 1.
- Arquivos de hashes registram igualdade antes/depois e apagado=true nas três sessões da construtora. Não copiei login nem reexecutei harnesses.
- O hook de entrada não tem chamada de rede/modelo no código lido. Não fiz prova de bloqueio de rede.
- As afirmações de documentação dos harnesses permanecem atribuídas à consulta da construtora; nesta leitura não refiz a consulta à documentação oficial.

## Encaminhamento

Sugestão ao Fiel: corrigir o registro parcial de indicações e a normalização de caminho em ticket/rodada própria, por ser leitura posterior à integração. Não reabrir nem alterar ticket pelo revisor parceiro. Resultado final do teste e acordo ainda pendentes.

## Resultado próprio

Teste encerrado: 16/16 PASSA, 0 falhas, saída 0, 69,7 s. Sessão 13674 encerrada. Os dois casos apontados não são cobertos por esses 16 testes. Leitura independente concluída; recomendo VOLTA técnica pelos dois achados, a encaminhar pelo Fiel por já estar integrado. Acordo pendente.


## Acordo
Fiel concordou com ambos: uma linha por skill indicada; normalizar barras antes do filtro. Registrou em parecer-19-Vela.md. Como já integrado, Vela encaminha ao maestro. Leitura tardia encerrada.

