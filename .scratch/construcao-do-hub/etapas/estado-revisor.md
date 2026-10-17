
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
