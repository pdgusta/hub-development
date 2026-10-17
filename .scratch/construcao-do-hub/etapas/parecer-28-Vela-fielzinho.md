# Ticket 28 — Vela — Fielzinho — rodada 1

2026-10-17. Ponta fc6c78b, worktree C:/context-hub-wt/ticket-28 limpa na partida. Li regras atualizadas, revisão em dupla, ticket28, relatório, código completo da skill/gerador/leitor de locais, testes semDocker/Docker, diff do contrato e testes do gerador. Fonte: spec faixa1 Pasta não replicada, decisão das quatroA. Sem ler parecer do Fiel. Docker é só do Fiel; não executei.

## Veredito provisório: VOLTA

1. **Só o frontmatter define local; regex sobre o corpo deixa pasta replicando e anuncia sucesso.** nova-pasta-local.ps1 calcula ehLocal com regex sobre o arquivo inteiro; também substitui linhas local: no corpo ao converter. O gerador usa separar(...).dados.local, estritamente no frontmatter. Reproduzi pela skill real, em hub de ensaio, CLI falso só para o daemon: index com YAML sem local e exemplo `local: true` no corpo. Chamada SEM -TornarLocal retornou0, religou sincronizador e anunciou pronto/local. Verificador completou YAML com local:false; .livesync/ignore NÃO contém reference/exemplo. Portanto a pasta continua elegível para sync apesar da confirmação, e a recusa de pasta existente foi contornada por texto comum.

Evidência própria: script persistido em etapas/logs/repro-28-fielzinho.ps1, sem Docker/harness. Saída observada: `codigo=0`; `completou ... local ...`; `pronto: reference/exemplo é local`; YAML final `local: false`, corpo `local: true`; lista somente labs já existente. Ensaio temporário exclusivo, daemon falso encerrado por PID pela função do kit e pasta removida no finally com validação do alvo.

Recomendação: ler o marcador com o mesmo parser YAML do gerador; alterar somente o frontmatter (preservar corpo); não relançar o sincronizador nem anunciar pronto sem confirmar que a pasta alvo entrou na exclusão efetiva. Cobrir exemplo local:true no corpo e exemplo local:false no corpo ao tornar local. Também conferir saída do verificador, atualmente ignorada.

## Verificações em andamento

- node --test --test-concurrency=1 agents/code/test/28-pastas-locais-sem-docker.test.mjs agents/code/test/gerar-exclusoes/gerador.test.mjs (sessão7269).
- Log suíteVela lido:196 testes,188pass,8skip,0fail; não é execução própria.
- Prova Docker e limpeza pendentes do Fiel. Não rodei suíte inteira, Docker ou harness; não alterei código/spec/ticket.

## Testes próprios concluídos
Arquivo28semDocker +gerador:9 testes Node passaram,0falhas,saída0,36,1s (o primeiro encapsula12 casos PowerShell). A reprodução adicional do marcador no corpo falha apesar dessa suíte verde. Sem testeDocker próprio. Segunda reprodução por junction em andamento (sessão24701), no mesmo script de evidência; resultado ainda não contado.


## Segundo achado

2. **Caminho da pasta não é conferido pelo destino real.** Reproduzi uma junction reference/atalho para uma pasta irmã fora do hub, ambas dentro do TEMP exclusivo do ensaio. Pedi reference/atalho/local: script sai0, cria index.md FORA do hub, religa e anuncia local; gerador não desce na junction e não inclui esse caminho na lista. Parâmetro documentado como caminho no hub recebe só validação lexical. Recomendo resolver ancestral existente real (há lib/caminhos.mjs no hub), recusar destino fora e validar inclusão efetiva; se junction interna não for suportada, recusar claramente antes de gravar/parar. Não testei tráfego LiveSync por junction; prova é escrita fora do hub e ausência da lista apesar de pronto.

Evidência: logs/repro-28-fielzinho.ps1 e .log. Ambos os comandos da skill saíram0. A segunda execução do script de evidência terminou1 somente na limpeza: sincronizador.log ainda aberto depois de Stop-Sincronizador. Tentativa posterior de remover o alvo exclusivo foi bloqueada pela revisão automática antes de executar, sem motivo específico; não tentei contornar. Limpeza PENDENTE de %TEMP%/hub-ensaio-28-fielzinho-486cf7a99c3b4104ac8432b4d01633c0. Os daemons falsos receberam Stop-Sincronizador no finally; não alego inspeção independente de processo nem pasta removida.

## Estado final independente

VOLTA pelos dois achados. Testes existentes9/9 verdes (12casosPS encapsulados +8testes gerador). Sem Docker/harness. Aguardar acordo e logDocker doFiel. Não há teste próprio rodando.

## Acordo rodada1
Aceito o achado3 doFiel: o bloco .* do exclude não abre .claude-plugin/, embora git ls-files confirme os manifestos dos mods fim-da-resposta e roteamento versionados no hub. Mod novo perderia o manifesto no add comum. Exceção !.claude-plugin/ com teste de mod novo é pertinente ao git (sem mudar exclusão de sync). Acordo VOLTA nos3; confirmar pasta em locais do JSON antes de pronto/religar integra conserto1/2. Fiel confirmou reproduções e limpeza da minha sobra TEMP sem processo vivo. Docker adiado à r2 peloFiel: trava ocupada e código vai mudar. Rodada1 encerrada em acordo.


## Leitura tardia — rodadas 2 e 3 — 2026-10-17

Ponta 5436cad conferida, árvore limpa. Li diff desde fc6c78b, cartao.mjs, script PowerShell, testes, relatório e parecer do Fiel. Consertos aceitos: parser de frontmatter com corpo preservado, recusa por destino real antes de parar o sincronizador, confirmação em locais do gerador antes de prosseguir, exceção .claude-plugin/ no git e parênteses na lista de argumentos do título. O conserto do título da r3 fecha o defeito descrito na r2.

Execução própria na r3: `node --test --test-concurrency=1 agents/code/test/28-pastas-locais-sem-docker.test.mjs agents/code/test/gerar-exclusoes/gerador.test.mjs`: 9/9, saída 0 (57,9 s; primeiro encapsula os 25 casos PS). Diff check fc6c78b..5436cad sem erro. Não reexecutei o código antigo da r2. Li logs/revisao-28-r3-docker.log: 14 PASSA e tudo passa, com controle chegando a B, retirada do banco/disco B, hashes em A preservados e remoções do índice git. Docker executado pelo Fiel, não por mim.

**Sem achado novo; mantenho PASSA da r3 e suas ressalvas.** Não há nova mensagem ao Fiel, conforme pedido de avisar somente achados. Código/spec/ticket intactos.
