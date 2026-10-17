
## Fluxo de encaminhamento — atualização do maestro, 2026-10-16

Após o passa, Fiel avisa somente o construtor por maestri ask.
O construtor encaminha ao integrador Rebite; Rebite junta e avisa o maestro.
Não enviar aviso ao maestro a cada passa.
Esta instrução substitui o encaminhamento anterior, inclusive o descrito no papel inicial.
Os avisos dos tickets 04 e 03 anteriores a esta atualização já foram enviados.

## Revisão em dupla — 2026-10-16

Li inteiro revisao-em-dupla.md. A ordem do maestro foi terminar o ticket 05 já em curso
individualmente e começar a dupla no próximo pedido, inclusive nova rodada do ticket 05.
Ticket 05, rodada 1: volta; 28 testes verdes. Achados e reproduções no parecer-Trilho.md.
Nos próximos pedidos, repassar imediatamente ao Fielzinho, fazer leituras independentes,
conversar em até duas trocas, passa só com acordo dos dois; impasse ao maestro.
Docker/harness real só Fiel roda. Sem subagentes. Após passa, avisar só o construtor.

## Estado — tickets 05 e 02, 2026-10-16

05 rodada 2 fechada VOLTA em acordo Fiel/Fielzinho; 32 testes verdes em ambos.
Dois achados adicionais de Fielzinho aceitos (comentario YAML e ficha arquivada).
Trilho avisado. Proxima rodada do 05 e terceira, conforme teto de voltas.
02 rodada 1: leitura de ambos sem bloqueio; Fiel executou verde 12/12 e conferiu limpeza.
Vermelho esperado -SemExclusao em execucao, log revisao-02-sem-exclusao.log.
Falta conferir vermelho e limpeza, trocar acordo por Maestri e fechar parecer/avisar Vela.

## Troca do Fiel — 2026-10-16 ~20h

Fiel agora é Claude Opus 5.5 médio. Li inteiros regras, revisao-em-dupla e este estado.
02, 03, 04 resolvidos e juntados. 05 passou na rodada 3, mas não juntado: quebra prova 02
(banco.psm1:51 chama o montador em agents/test). Trilho troca o caminho, repete 34 testes e
prova 02 e pede rodada curta. Brasa no 01, Vela no 06: vão pedir revisão.
Fielzinho pode estar no limite até 20:26; se não responder, revisar sozinho e anotar no parecer.

## 05 rodada 4 (curta, diff 817f850..a18bbed) — 2026-10-16

Repassado ao Fielzinho. Merge 6b5110e limpo (sem resolução de conflito); a18bbed muda só banco.psm1:51.
Nenhuma outra referência a agents/test no ramo. 34 testes node verdes (Fiel).
Prova 02 rodando em segundo plano: log etapas/01-esqueleto/revisao-05-r4-prova02.log.
Nota para o 01 (Brasa): ramo ticket-01 ainda chama agents\test\hub-de-ensaio nas provas 01 e 02.
Falta: resultado da prova, contêineres hub-ensaio-02 apagados, acordo com Fielzinho, parecer, avisar Trilho.
05 rodada 4: prova 02 PASSA (12 casos, saída 0), limpeza ok. Parecer fechado PASSA pelo Fiel sozinho;
Fielzinho no limite até 20:26, leitura dele pendente. Trilho avisado.

## 01 (Brasa) — 2026-10-16 ~20:15

Rodada órfã da prova 01 (revisor anterior, 20:00, revisao-01-cifrada.log parou na colisão) derrubada:
PIDs 139424/175468, hub-ensaio-00-a/b down -v, TEMP/hub-ensaio-00 apagada. Não há parecer-Brasa ainda.
Brasa juntou integracao (0d04985) e trocou o caminho do montar (0c8c639). Revisar do HEAD do ticket-01.
01: repassado ao Fielzinho (no limite até 20:26). Li ticket, relatório, spec Worker 4, prova.ps1.
Ramo contém integracao; 5 arquivos novos em provas/01-banco; banco.psm1 = cópia da 02 menos 3 acréscimos, mais -SemSalComum.
Achado a conferir: "nada em claro" só busca nomes/textos do teste, não os 44 arquivos do hub de ensaio.
Plano: quando a Brasa avisar, rodar prova com cifra (log revisao-01-r1-cifrada.log) e uma com -Manter para varrer docs crus por nomes do hub.

## 06 (Vela) rodada 1 — 2026-10-16

Repassado ao Fielzinho. Ramo d45be5d contém integracao 0d04985. gerador.test.mjs 5/5 (Fiel).
Achado 1 (Fiel): ehLocal usa regex própria; verificador (lib/frontmatter.mjs, js-yaml 4, index.yml local boolean)
aceita local: True/TRUE e fechamento '--- ' com espaço; o gerador não reconhece -> pasta vaza calada.
Reproduzido: index.md 'local: True' -> locais []. Conserto: usar separar() da lib e dados.local === true, com teste.
Rodando em segundo plano: prova 01 (revisao-01-r1-cifrada.log) e sincronizador 06 (revisao-06-r1-sincronizador.log).
06 r1: VOLTA (conserto 1, local lido como o verificador). sincronizador.ps1 invalidado: Vela editando worktree durante a rodada.
Parecer em etapas/01-esqueleto/parecer-Vela.md. Vela avisada.
01: prova com cifra do HEAD 0c8c639: 19 PASSA, saída 0, limpa (revisao-01-r1-cifrada.log). Rodando -Manter para sondar nomes do hub nos docs crus (revisao-01-r1-manter.log); depois derrubar com Remove-EnsaioBanco.
06 r2 (b7cd714): conserto 1 feito; gerador 7/7 (Fiel). Rodando sincronizador e -SoPonto (revisao-06-r2-*.log).
Aval do Gustavo (20:24) para login dos harnesses em %TEMP%\hub-ensaio-<ticket>-*: regras-da-construcao.md, "Login dos harnesses no ensaio". Lido; usar só se a revisão exigir, com hashes antes/depois e registro no parecer.
01 r1: PASSA (Fiel sozinho). Sonda -Manter sem vazamento; ensaio derrubado. Parecer etapas/00-provas/parecer-Brasa.md. Brasa avisada.
06 r2: PASSA (Fiel sozinho). 7/7, 14/14, -SoPonto vermelho correto, limpo. Vela avisada.
Pendente: leitura do Fielzinho em 05 r4, 01 r1 e 06 r2 quando ele voltar do limite.
05 r4: Fielzinho PASSA, acordo registrado no parecer-Trilho. Fielzinho de volta; lendo 01, 06, 14.
14 (ramo ea4d299): repassado ao Fielzinho. Revisão do Fiel em curso.
01 e 06: acordo com Fielzinho registrado nos pareceres (passa). 01: contagem corrigida para 17 PASSA + 2 VÊ.
14: Fielzinho investigando patch com newline após End Patch. Fiel: lendo código; falta rodar 69 e decidir ponta a ponta.
14 r1: VOLTA em acordo com Fielzinho. Conserto 1 newline após End Patch (reproduzido), 2 caminho com ponto relatório x código. 69/69 Fiel. Parecer etapas/parecer-Trilho.md. Trilho avisado.
14 r2: PASSA em acordo com Fielzinho. 71/71, reprodução repetida recusa nos 4 finais, sem login sobrando. Trilho avisado.
27 r1: VOLTA em acordo com Fielzinho, 5 consertos (AGENTS/SKILL, sem alvo = hub inteiro, avisos perdidos, %ZZ derruba, par:// .secrets). Fora do hub: ressalva ao maestro. Parecer etapas/parecer-Vela.md. Vela avisada.
REGRA PROVISÓRIA (maestro): até o 29 entrar em integracao, não rodar a suíte inteira; fora ponta-a-ponta/ e provas/03-codex-hooks/ (harness real, login, regravam evidência). Depois do 29: só com HUB_HARNESS_REAL=1.
07 (etapa 2, banco do par): pedido recebido, ponta 7fa0e56. Testes Docker um de cada vez: 07-banco.test.ps1, provas 01 e 02, sincronizador.ps1.
27 r2: PASSA em acordo com Fielzinho (106/106, reproduções ok). Vela avisada.
07 r1: Docker rodando (task baf7s5mpn), logs etapas/revisao-07-r1-*.log. Fielzinho propõe VOLTA com 3 achados (PID qualquer node; Initialize aceita config divergente; isConfigured antes de mark-resolved). Falta conferir os 3 e ler o código.
29 r1 (Brasa): VOLTA em acordo (integracao 0a8e17f traz 27 ponta a ponta sem proteção; pedir proteção que pegue teste novo). Parecer etapas/parecer-29-Brasa.md.
Fielzinho sem cota até 01:34 (maestro): revisar sozinho e registrar leitura pendente (07, 29 e próximos).
29 r2: PASSA (Fiel sozinho). 116/112/4 pulados, git limpo. Brasa avisada.
07: Brasa juntou integracao 0a8e17f (e3ff419) durante meu Docker; código do 07 igual a 7fa0e56.
07 r1: Docker 1ª passada (máquina carregada pela suíte do 29): 07-banco 1 FALHA (replicação A sem estado em 30 s), prova01 ok, prova02 1 FALHA (controle não chegou ao disco B), sincronizador ok; sem sobra. Os 3 achados do Fielzinho confirmados no código (linhas 185, 197/199, 215). Repetindo 07-banco e prova02 (revisao-07-r1b-*.log). Veredito previsto: VOLTA.
07 r1: VOLTA (3 consertos do Fielzinho). Repetição: 07-banco e prova02 passam; vermelhos eram de carga. Parecer etapas/02-banco/parecer-Brasa.md. Brasa avisada.
19 r1 (Vela): PASSA (Fiel sozinho; Fielzinho lê depois). Parecer etapas/parecer-19-Vela.md. Vela avisada.
19 r1 PASSA (Vela avisada). 12 r1 (Trilho, busca, 0ba8532): lido relatório, iniciar.ps1, fragmentos; testes 12-busca + 12-kit rodando (revisao-12-r1-testes.log). Codex do aceite real pendente (cota); Trilho pede rodada curta depois.
12 r1: VOLTA por 1 conserto (12-busca.test.mjs:28 regrava medidas.json versionado; desfiz com checkout). 13/13. Rodada curta junto com evidência do Codex. Parecer etapas/parecer-12-Trilho.md. Trilho avisado.
12 r2 curta: PASSA (cc96be2, 13/13, árvore limpa). Pendente: rodada curta da evidência do Codex depois das 01:34 (São Paulo).
20 r1 (Vela): VOLTA, 2 consertos (soAcrescenta aceita regra inserida no SKILL.md; pasta nova -> ENOENT -> passa). Parecer etapas/parecer-20-Vela.md. Vela avisada.
15 r1 (Trilho): PASSA (9/9, árvore limpa; Codex pendente). Parecer etapas/parecer-15-Trilho.md. Trilho avisado.
20 r2: PASSA (13/13, sondas ok). Vela avisada.
REGRA (maestro): trabalho pesado (Docker, suíte inteira, busca, npm install, harness real) só com etapas/trava-pesada.md (esperar se <30 min; criar com nome/o que/hora; apagar no fim, mesmo falhando). Teste de um arquivo não precisa.
30 r1 (Vela): PASSA (46/46 nos testes ligados; suíte inteira com a Vela; reabre se vermelho fora do 12-busca). Parecer etapas/parecer-30-Vela.md.

## Salvo para limpar — 2026-10-17

Retomada completa em etapas/retomada-Fiel.md (tabela de pareceres, próximos pedidos, regras vivas).
Ocioso. Próximos: 13 (Trilho), 07 r2 (Brasa), rodadas curtas do Codex (12, 15, 20).
Sem Docker nem ensaio de pé.
31 r1 VOLTA (parecer forjável em .local/acervo/pareceres). 32 r1 VOLTA (espaço no caminho gera link quebrado). Pareceres etapas/parecer-31-Vela.md e parecer-32-Vela.md. Vela avisada.
31 r2 e 32 r2: PASSA (19/19, 18/18, sondas ok). Suítes pendentes da trava; reabrem se vermelho. Vela avisada.
13 r1 (Trilho): PASSA (4/4; gemini.env sem chave; contêiner parado). Parecer etapas/parecer-13-Trilho.md. Trilho avisado.

## Fila — 2026-10-17 (cota do Codex voltou às 01h34; Fielzinho livre)

1. 07 r2 (Brasa), depois da suíte dela.
2. 31 rodada nova (Vela, 050fb14: guarda casando CRLF/LF; evidência do Claude e do Codex do 20).
3. Leituras atrasadas do Fielzinho: 13, 31, 32, 30, 20, 15, 12, 19, 29.
Detalhes em etapas/retomada-Fiel.md, seção FILA. Salvo para limpar.
07 r2: VOLTA em acordo com Fielzinho (PID por substring; configurado sem marca refeito calado). 3ª rodada = passa com ressalvas; Docker do Fiel na 3ª, com trava. Brasa avisada.
19: leitura tardia do Fielzinho com 2 achados aceitos (registro por skill; barra do Windows no caminho); 19 já juntado -> Vela leva ao maestro. 07 r3 pedido (6b1d7e8): Docker espera a trava (Rebite). 31 nova rodada (4e420a6) em revisão.
31 r3: PASSA com ressalva (aval de nome parecido/tabela não registrado -> ticket seguinte). Vela avisada.
07 r3: trava pesada criada 02:21 pelo Fiel; Docker rodando em sequência (task de fundo), logs revisao-07-r3-*.log; a trava se apaga no fim do script.
07 r3: PASSA em acordo (Docker 4/4 verde com a trava; trava apagada). Brasa avisada.
34 r1 (Vela): PASSA em acordo (19/19). Vela avisada.

## Salvo para limpar — 2026-10-17 (51%)

Sem revisão em curso; 07, 31 e 34 fechados. Próximos: 35 (Trilho), 28 (Vela), 08 (Brasa), 33; leituras atrasadas do
Fielzinho: 13, 32, 30, 20, 15, 12, 29. Retomada completa em etapas/retomada-Fiel.md. Sem Docker nem trava minha.

## Retomada após /clear — 2026-10-17 ~04h

Li retomada, regras, revisao-em-dupla, estado. Fielzinho com cota. Sem revisão em curso.
Próximos: 12 e 15 voltam (Trilho: fragmento do hub-busca expõe só a search nos três; decisão (A) no ticket 15,
~03h50: Codex enabled_tools, Copilot tools ['search'], Claude deny mcp__hub-busca__read; refazer real do 12 e 15).
Na rodada: conferir nome canônico do deny, que read sumiu do contexto nos três, e o real com a trava pesada.
Depois: 35, 28, 08, 33; leituras atrasadas do Fielzinho.
Regra nova (Gustavo, via maestro, 2026-10-17): no máximo UM subagente por vez, tarefa leve. Quarto construtor: Cinzel (ticket 09), vai pedir revisão ao Fiel.
Regra nova (Gustavo, 2026-10-17): além do subagente, até três subagentes Haiku 5.5 esforço médio, só tarefa simples ou QA (ex.: evidência x critério); veredito é do Fiel.
28 r1 (Vela, fc6c78b): pedido recebido; repassado ao Fielzinho. Revisão do Fiel em curso.
28 r1: parecer-28-Vela.md VOLTA (1 e 2 do Fielzinho reproduzidos; 3 do Fiel: .* no exclude esconde .claude-plugin de mod novo). Docker fica para a r2. Sobra do ensaio do Fielzinho apagada. Aguardando acordo.
28 r1 FECHADO: VOLTA em acordo (1,2 Fielzinho; 3 Fiel, leitura do Fielzinho pendente: sem cota até 06h58). Vela avisada.
12 rodada nova (Trilho, 8558abe): pedido recebido; Fielzinho sem cota até 06h58 -> Fiel sozinho, leitura pendente.
12 r3: PASSA (Fiel sozinho; leitura do Fielzinho pendente). 3 ressalvas, a 2 vai para o 15 (deny do Claude no 15-leitura.test). Trilho avisado.
Maestro (~04h): Codex sem cota até 06h58; Fiel revisa sozinho; leituras do Fielzinho na fila para depois: 28 (achado 3), 12 r3, mais as antigas (13, 32, 30, 20, 15, 12, 29).
Regra nova (maestro, ~04h): construtor roda só os testes do ticket e dos arquivos mexidos; suíte inteira só na junção (Rebite). Não pedir suíte inteira ao construtor. Trilho vai pedir 35 e 33.
35 r1 (Trilho, ebae5ca) e 33 r1 (Trilho, 07e6b92): pedidos recebidos; Fiel sozinho (Fielzinho sem cota até 06h58).
35 r1: PASSA (Fiel sozinho; 22/22). Parecer parecer-35-Trilho.md. 28 r2 pedido (2eec8e9) — na fila depois do 33; Docker espera trava (Cinzel).
33 r1: PASSA com 3 ressalvas (Fiel sozinho; 37/37; sonda de 14 casos). Parecer parecer-33-Trilho.md.
28 r2: VOLTA por 1 conserto (-Titulo perdido no Invoke-Cartao). 1-3 da r1 feitos. Docker na r3 (trava do Cinzel 04h09). Vela avisada.
28 r3 (5436cad): conserto do -Titulo conferido; testes sem Docker rodando; Docker espera trava do Cinzel.
09 r1 (Cinzel): pedido recebido; fork C:/Projetos/hub-mcp-banco 61a6e70 + hub ticket-09 3d9d0bb. Fiel sozinho (Fielzinho sem cota até 06h58). 28 r3: Docker esperando trava do Rebite (04h37).
09 r1: lido relatório, vault.ts e tools.ts. Suspeita: regra "base viva" checada antes de gravar, sem trava -> duas gravações simultâneas da mesma base respondem as duas "saved". Sonda pronta no scratchpad (sonda09.e2e.test.ts), roda na minha vez da fila (28 Docker primeiro).
09 r1: sem Docker 1/1 (12 casos). Fiel 4º na fila-pesada (re-adicionado; o maestro tinha refeito a lista). Na vez: (1) 28 r3 Docker: cd C:/context-hub-wt/ticket-28; pwsh -NoProfile -File agents/code/test/28-pastas-locais.test.ps1 > etapas/logs/revisao-28-r3-docker.log; (2) 09: no fork, node scripts/e2e-banco.mjs test/versao.e2e.test.ts <scratchpad>/sonda09.e2e.test.ts (copiar a sonda para etapas/logs/ antes); (3) 09 hub: pwsh -NoProfile -File agents/code/test/09-mcp-banco.test.ps1. Ressalvas anotadas do 09: move_note conflito na origem não diz que o destino foi gravado; passo 05 com MCP de pé não religa após rebuild.
Maestro: Docker do 28 logo depois do 16 do Trilho; Trilho avisa; ao soltar, avisar a Brasa.
Maestro: depois do Docker do 16 (Trilho), Fiel roda Docker do 28 e do 09 numa vez só; ao soltar, avisar a Brasa.
Docker 28+09 armado em segundo plano: parte sozinho quando a trava do Trilho sumir (script etapas/logs/fiel-docker-28-09.sh; logs revisao-28-r3-docker.log, revisao-09-r1-fork.log, revisao-09-r1-hub.log). Ao fim: avisar a Brasa.
09: Cinzel deixou consertos em ramos à parte (fork hub-mcp-banco-wt/conserto-09 d2a5a40; hub context-hub-wt/conserto-09 ca17738). Script ajustado: 28; fork ticket-09 + sonda (vermelho); fork conserto + sonda; hub conserto com HUB_MCP_BANCO_DIR do conserto. Hub ticket-09 não roda (o conserto contém o mesmo teste e mais).
28 r3: PASSA (Docker 14 PASSA). 09 r1: VOLTA, 3 consertos já nos ramos ticket-09-conserto (Docker: furo reproduzido no ticket-09, conserto 16/16 fork e 21 PASSA hub). Rodada 2 curta = juntar conserto no ticket-09 e conferir árvore. Trava solta 05h05; Brasa avisada. Sobra em TEMP: 1325 pastas hub-ensaio-* de vários tickets (04, 05, 27...), não minhas.
09 r2: PASSA (pontas = testadas no Docker; integracao andou, junta sem conflito). Cinzel avisado.
36 r1 (Vela, b8e8b03): pedido recebido; Fiel sozinho.
36 r1: VOLTA, 1 conserto (uncaughtException/unhandledRejection apagam as pastas no meio; node:test segue). 174/174, 0 sobras. Vela avisada.
10 r1 (Cinzel): pedido; hub ticket-10 6095213, fork hub-mcp-banco-wt/ticket-10 58c8504. Fiel sozinho.
10 r1: VOLTA, 1 conserto (MCP grava content sem as trocas do verificador: nota sem frontmatter em inbox/ passa e fica fora do esquema). 10/10 fork, 1/1 hub. Docker na r2. Cinzel avisado.
10 r2 (fork 1e86ad1, hub a40ec84): conserto conferido no código; e2e fork 14/14. Docker na fila (item 6). 36 r2 (5b90550) pedido.
36 r2: PASSA. Vela avisada.
Docker do 10 r2 pronto: bash etapas/logs/fiel-docker-10.sh (na minha vez; ao soltar, avisar o próximo da fila).
Maestro: Docker do 10 entra primeiro entre fatias da Brasa; Brasa avisada; ao soltar, devolver a ela.
10 r2: PASSA (Docker 33 + 21 PASSA). Trava passada ao Trilho 06h35. Cinzel avisado.
16 r1 (Trilho, aa70e98): pedido recebido; Fiel sozinho.
16: leitura intermediária (não conta rodada). Sem conserto na parte feita; faltam cenários do 08, estado_do_hub real, item fim-da-resposta. 3 ressalvas (atualização perdida no estado.json, 401 vira replicação parada, recuperar copia banco por folha). Trilho avisado.
Salvo para limpar (07h): retomada-Fiel.md atualizada; sem revisão em curso, sem trava minha.

## Retomada após /clear — 2026-10-17 06h45

Li retomada, regras, dupla, fila, estado. Sem revisão em curso. Trava: Rebite (suíte, 06:44).
Codex com cota a partir de 06:58: às 06:59 repasso ao Fielzinho a lista de leituras atrasadas (28 achado 3 + r2 + r3,
12 r3, 35, 33, 09, 36, 10, 16; antigas 13, 32, 30, 20, 15, 12, 29). Próximos pedidos: 15 (Trilho), 16 final, 08.
08 r1 (Brasa, 124f43d): pedido recebido 06:49; repassado ao Fielzinho. Fatia 2 pendente (maestro). Revisão do Fiel em curso.
08 r1: leitura do Fiel feita; parecer-08-Brasa.md provisório: conserto 1 (Get-AcimaDoLimite: relativo cortado com barra no fim/nome curto; lista pasta local), 4 ressalvas. Fatia 1 reroda junto com a 2 (-Fatias 1,2) na hora quieta. Aguardando Fielzinho.
28 r1 achado 3: Fielzinho aceitou (acordo registrado). 08: Fielzinho iniciou leitura independente (sem Docker).
08 r1 FECHADO: VOLTA em acordo (conserto 1). Brasa avisada. 08 r2 pedido (514db7a).
08 r2 (514db7a): conserto conferido, código passa (Fiel). Falta Fielzinho r2 e log das fatias 1,2 (Brasa roda na hora quieta, fila item 4).
08 r2: código PASSA em acordo com Fielzinho; aceite final pende log das fatias 1,2.
15 rodada nova (Trilho, 3d34bd1) e 17 r1 (Vela, 86c5a88) pedidos ~07h35. 08: Brasa roda -Fatias 1,2 na hora quieta (armadilha: por pwsh -File '1,2' vira 12; usar -Command).
15 rodada nova: PASSA em acordo com Fielzinho. Trilho avisado.
