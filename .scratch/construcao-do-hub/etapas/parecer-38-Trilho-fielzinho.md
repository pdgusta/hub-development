# Ticket 38 — Trilho — parecer independente do Fielzinho

2026-10-17. Ponta 7c87301 conferida (merge do 17), árvore limpa. Li ticket, relatório, diff e7203b4..HEAD, ajudante, novos testes, mudanças nos testes consumidores e logs indicados. Não li parecer do Fiel. Sem Docker, harness real, indexação ou instalação.

## Veredito: VOLTA

### 1. O finally de 09/10 ainda pode abandonar a limpeza antes de Remove-EnsaioBanco

Nos finais de 09-mcp-banco.test.ps1 e 10-mcp-banco.test.ps1, o laço `foreach (...) { Stop-McpBanco $i }` vem antes da remoção do ensaio e não tem proteção própria. Uma exceção interrompe as outras instâncias e impede Remove-EnsaioBanco. Stop-McpBanco usa Stop-Process sem tolerância a erro: por exemplo, o processo pode desaparecer entre Get-PidMcpBanco e Stop-Process.

Reprodução própria sem Docker: logs/repro-38-fielzinho.ps1 extrai pelo AST o finally real dos dois arquivos e o executa com Stop-McpBanco dublê que lança e Remove-EnsaioBanco dublê que registra a chamada. Saída persistida em logs/repro-38-fielzinho.log: nos dois, erro forçado e `Remove-EnsaioBanco chamado=False`. Não criou recurso externo nem alterou código. A saída 0 da sonda confirma a reprodução, não o aceite.

Recomendação: tentar parar cada instância de modo independente e garantir a remoção do ensaio em finally próprio, preservando a primeira falha e respeitando -Manter. Cobrir a falha na parada do MCP, não só Uninstall-ParBanco dentro do helper. No 08, colocar também a preparação/cópia dos logs sob proteção que garanta a limpeza: New-Item dos registros ainda vem antes da proteção (achado por leitura, não executado). O ticket promete limpeza também quando falha; o conserto atual protege o helper, mas não todos os chamadores que podem deixar de chegar a ele.

## Verificações

- Próprio: `node --test --test-concurrency=1 agents/code/test/36-pasta-de-ensaio.test.mjs agents/code/test/38-ensaio-banco.test.mjs agents/code/test/07-kit-sem-docker.test.mjs agents/code/test/09-mcp-banco-sem-docker.test.mjs`: 14/14, saída 0, 55,2 s. Inclui gancho com processo preso, gancho que lança, criação parcial e remoção falhando. Nenhum desses casos injeta falha no Stop-McpBanco do finally do consumidor.
- Diff check e7203b4..HEAD sem erro. A migração usa ajudante comum, ganchos síncronos antes das pastas e mantém a proteção de exceção solta que não encerra o processo. O modelo comum está conforme mandato do maestro, sem execução real nesta revisão.
- Logs do Trilho lidos: leves 23/23, busca 17/17, vigia 19/19. Log de falha forçada mostra também falhas esperadas dos ponta a ponta antes de login (harness nada). A ausência de sobras dessas rodadas é declaração do relatório, não inspeção própria retroativa.
- Docker 08/09/10 dispensado nesta rodada pelo maestro, próximo exercício no 25. Não tratei testes sem Docker como prova da limpeza de contêiner real.

Aguardar acordo do Fiel. Nenhum código/spec/ticket editado.

## Acordo com Fiel

Fiel aceitou o conserto após conferir o código (09:166-169, 10:215-218) e a sonda. VOLTA fechado em parecer-38-Trilho.md.


## Leitura do Fielzinho — rodada 2, 2026-10-17 (após retomada)

Segunda leitura documental da ponta b854a7e, já juntada e resolvida, por orientação do maestro: somente registrar. Conferidos o diff completo 7c87301..b854a7e, o relatório r2, os novos casos do 38-ensaio-banco e o final de logs/trilho-38-r2-leves.log (60 testes, 60 passam, zero falhas).

Concordo com o fechamento do conserto 1: Invoke-Limpeza tenta os passos restantes e relança a primeira queda; 09/10 isolam cada parada do MCP e a remoção; 08 protege também New-Item dos registros e mantém a remoção da raiz como passo separado. Os casos novos extraem os finally reais e injetam as falhas apontadas na r1. Nenhum achado novo nesta leitura do conserto.

Não executei testes nesta retomada. Os 60/60 são evidência do Trilho; os 25/25 e a sonda de escopo das closures são evidência registrada pelo Fiel. Docker continua dispensado nesta rodada, conforme fechamento. Este registro complementa a revisão já encerrada; não reabre o ticket e não altera o veredito do Fiel.
