# Parecer Fielzinho — Brasa, ticket 29, rodada 1

2026-10-17. Veredito independente: **VOLTA**, por uma lacuna na costura com o27 já integrado. Teste próprio concluído:83passam,3pulados,0falhas; acordo com o Fiel pendente.

## Base e fontes

Ramo ticket-29, worktree C:/context-hub-wt/ticket-29, HEAD02667615efb76a291b5839f0c7770f9d15dffe22, worktree limpa antes de testar. O ramo parte de integracao8d1d785; agora integracao é0a8e17ff6a192a2e82b3b2bd167858b500006b3b (junção do27). merge-base --is-ancestor integracao HEAD retorna1: falta incorporar essa ponta. Não li o parecer do Fiel.

Ticket29, relatório29, regras-da-construcao e revisao-em-dupla lidos inteiros. juntar-tickets.md lido inteiro e comando comum/condição de opt-in conferidos. Essa manutenção nasce do achado07 e da regra de login; não muda decisões de produto dos tickets resolvidos. Li módulo/testes novos, três arquivos embrulhados, import instalar.mjs (sem execução na carga quando importado), diff ignorando recuo e evidências novas. Sem subagentes, Docker ou harness real; não editei código/spec/tickets.

## Conserto

1. **Incorporar integracao e proteger também a ponta a ponta do27.** integracao0a8e17f contém agents/code/test/ponta-a-ponta/27-fim-da-resposta.test.mjs (do commit5df8972). O arquivo não usa comHarness nem HUB_HARNESS_REAL: no topo calcula HASH_ANTES, apaga evidência-27 dos harnesses e depois registra testes que copiam login e chamam Claude/Codex/Copilot. Conferido por git show integracao:<arquivo>, sem importar/executar. O ramo29 não tem esse arquivo; COM_HARNESS/EVIDENCIAS no teste de proteção só incluem03/14. Uma junção do29 nessa ponta deixa o comando comum continuar chamando os três harnesses pelo27 sem variável, contrariando o critério1 do29. A frase do relatório “fora esses três, nenhum teste da suíte chama harness” ficou desatualizada. Brasa deve incorporar a ponta, embrulhar27 e incluir arquivo/evidência27 na prova sem variável. Rodar suíte resultante sem variável, conferir quatro arquivos de harness pulados, evidências intactas e nenhum login/cota. Não é necessário rodar HUB_HARNESS_REAL=1 de novo para conferir o salto (Fiel determina eventual prova real conforme regra).

## O que atende na árvore revisada

- comHarness só chama describe(fn) com o valor exatamente1; sem variável registra teste pulado com motivo e não executa corpo. Criação de ensaio, hash inicial e apagar evidência ficaram dentro do corpo nos três arquivos antigos.
- Diff -w mantém comportamento/assertivas dos testes reais; além do embrulho, muda uso e diagnóstico por hash.
- Teste próprio de proteção usa HOME/TEMP/APPDATA de ensaio, PATH limitado ao Node e remove flag do filho; confere skip dos três, evidência por hash e pasta HOME/TEMP vazia. Boa prova da árvore antiga; falta incorporar27 para provar a árvore que será juntada.
- relatorioDeHashes inclui caminho/hash antigo/novo, mtime e janela temporal; arquivo ausente não atribui causa. Testes cobrem estável, dentro/fora da janela, sumiu/apareceu. O código informa coincidência temporal; não prova autoria da escrita (limite coerente com o problema).
- Critério4 feito pelo maestro: regras e juntar-tickets dizem comando sem variável; opt-in só quando mexe em prova03/guarda14/hooks, com concorrência1. Essa regra só pode ser liberada após conserto1.

## Evidências reais lidas, sem executar

.local/harness-real.log termina11testes,11passam,3suítes,0falhas,saída0,130,7s. Registro hashes do14:8/8 iguais e3pastas apagadas; horários batem com relatório. Prova03 registra login apagado=true às00:46:26UTC. Nenhuma cópia de login realizada nesta revisão. Caminhos pessoais curtos na evidência03 já existiam e o relatório ressalva; não expus nem copiei dados de clientes.

## Verificação própria em andamento

Node pai tira HUB_HARNESS_REAL do env do filho, retrata por SHA256 todos os arquivos versionados, roda node --test "agents/code/test/**/*.test.mjs" e compara hashes. Log em C:/context-hub-wt/ticket-29/.local/revisao-fielzinho-29-sem-variavel.log. Sessão64002 concluída:saída0,86testes,83passam,3pulados,0falhas,84,2s. Retrato SHA256 de todos os arquivos versionados antes/depois:nenhum alterado. Nenhuma execução com HUB_HARNESS_REAL=1.

## Conversa em dupla

Pendente acordo com o Fiel; ele fecha e responde à Brasa.07 continua pendente em parecer-Brasa-fielzinho.md, separado deste29;27r2 passou em dupla.


## Acordo da rodada 1

2026-10-17: Fiel confirmou **VOLTA**. Conferiu integracao0a8e17f não ancestral e o27 apagando evidência na linha47/chamando os três harnesses. Acrescentou conserto2, aceito pelo Fielzinho: a prova de proteção não deve depender apenas da lista fixa de nomes; deve haver teste sem harness que detecte chamada a harness fora da proteção. Isso fecha o critério global de nenhum harness na suíte comum e evita repetir a lacuna do27. A solução concreta fica com a Brasa.

Resultado próprio comunicado no parecer:83passam,3pulados,0falhas,saída0; nenhum arquivo versionado alterado. Parecer único/fechamento: etapas/parecer-29-Brasa.md. Fiel responde à Brasa. Sem acordo pendente no29; aguardar correção.
