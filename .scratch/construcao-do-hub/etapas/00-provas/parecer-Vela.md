# Parecer — Vela — ticket 03

Data: 2026-10-16. Revisor: Fiel. Rodada 1.
Veredito: **volta**. A prova dos hooks passou; falta corrigir a composição do instalador.

## Escopo e fontes

Ramo ticket-03, worktree C:/context-hub-wt/ticket-03, HEAD a14d996.
Fontes: regras da construção, brief 00-provas, ticket de construção 03, tickets resolvidos
14 e 44, bancadas bancada-acesso-codex.md e bancada-acesso-relatorio.md, spec (Workers
2, 6, 7 e 8) e partes relevantes de faixas-07-08.md.
Não é aceite da implementação completa de checkpoint, guardas, vigia ou kit.

## Conferência executada

- Ramo inicialmente limpo; integracao ancestral de HEAD (git merge-base --is-ancestor: 0).
- Executei node --test provas/03-codex-hooks/prova.test.mjs: 5 testes passaram, 0 falhas.
- A execução gerou sessão 01a146c4-13f9-79f1-a565-6c9c0dd704f0:
  inicio/injetou com permission_mode=bypassPermissions; marca; recusa de apply_patch;
  fim devolvido; fim solto com nota_tocada=true e stop_hook_active=true; notify
  agent-turn-complete na mesma sessão, cliente codex_exec.
- O teste conferiu a nota existente byte a byte e a retomada alterada sem perder o prefixo.
- codex-exec.jsonl contém Command blocked by PreToolUse hook para Add File sobre existente;
  a gravação de shell-ok.txt terminou com exit_code=0.
- login-apagado.txt: apagado=true. Não restou pasta hub-ensaio-03-* em TEMP.
- Comparei hashes e datas UTC de config.toml, hooks.json e auth.json reais antes/depois:
  todos iguais. Nenhuma configuração global alterada.
- Busca de access_token|refresh_token|id_token|api_key|bearer na evidência: zero ocorrências.
  Isso é uma checagem de marcadores, não uma garantia geral contra qualquer dado sensível.
- O teste regrava a própria pasta evidencia/: quatro arquivos rastreados ficaram modificados
  pela execução de revisão. Código não foi editado; preservei a nova evidência.
- Instalador executado três vezes em HOME novo com configuração alheia:
  resultado idêntico nas três passadas e model alheio preservado.

## Consertos necessários

1. **Aprovar apenas os hooks deste fragmento.** Em instalar.mjs, aprovarHooks filtra apenas
   por sourcePath igual ao hooks.json de destino. Esse arquivo também recebe hooks alheios
   preservados por juntarHooks. Logo, o instalador confia neles também, mesmo sem aprovação
   anterior. Isso afeta a composição com outras etapas e contradiz a preservação de
   configuração alheia afirmada no relatório.
   Reprodução: HOME temporário com SessionStart[0] = comando node -e process.exit(0),
   sem hooks.state; rodei instalar. Surgiu trusted_hash para hooks.json:session_start:0:0,
   que é o hook alheio; o hook de início da prova foi acrescentado em outro índice.
   Resultado observado: hookAlheioAprovado=true; idempotente=true; modeloPreservado=true.
   Fixture sem credenciais:
   C:/Users/GUSTAV~1.DEL/AppData/Local/Temp/hub-ensaio-revisao-instalador-03-Te38Yg
   Identificar os hooks efetivamente adicionados pelo fragmento e só aprovar esses.
   Acrescentar teste da composição com hook alheio não confiado e hook alheio já confiado.
   Preservar a confiança dos dois como estava. Atualizar relatório e repetir a prova.

## Ressalvas para ligar

- notify único e sobrescrita do notify anterior: limite bem registrado no relatório;
  o kit futuro precisa compor os consumidores antes de instalar. Não é conserto desta prova.
- O Stop de liberação veio com nota_tocada e stop_hook_active simultaneamente. O código dá
  prioridade à nota; a prova não demonstra a exclusividade dessa causa. O relatório registra
  corretamente a ressalva. A suficiência semântica da retomada continua na etapa própria.
- O fixture é mínimo: uma pasta iniciativas/ensaio-prova, sem seis raízes nem núcleo completo.
  Não é o hub de ensaio do ticket 04. Ao reaproveitar a prova, usar initiatives/ e o hub
  estruturado; não tomar este verde como validação de frontmatter ou integração de estrutura.
- O caminho .local/vigia/estado.json e HUB_ROOT correspondem às costuras do spec.
- TUI, toast, segunda máquina, Update que troca tudo, configuração TOML multilinha e
  proteção de conteúdo dos scripts por hash não foram provados aqui. Limites documentados.

## Encaminhamento

Volta ao Vela para o conserto 1. Nenhum código, spec ou ticket foi editado pelo revisor.

## Atualização de critério — comunicação do maestro, 2026-10-16

Li a nota no topo do spec e as regras atualizadas. Nas próximas revisões:
- O que o agente chama: agents/skills/<peça>/.
- O que só harness, kit ou teste roda: agents/code/ (hooks, mods, kit, bin, test).
- Provas da etapa zero: agents/code/test/provas/<prova>/.
- Nenhuma pasta de código na raiz.
- Novo hub de ensaio em destino vazio, montado com o montar.mjs de integracao.

Conferido: ticket 04 integrado em b68f540. O parecer anterior é histórico;
a nova disposição será exigida nas próximas entregas, incluindo a rodada pendente do ticket 03.


## Rodada 2 — 2026-10-16

Veredito: **passa**. Sem consertos obrigatórios restantes para o ticket 03.

HEAD conferido: f4bb98b; ramo ticket-03 inicialmente limpo.
integracao b68f540 é ancestral de HEAD (git merge-base --is-ancestor: 0).
Executei:
node --test agents/code/test/provas/03-codex-hooks/instalar.test.mjs agents/code/test/provas/03-codex-hooks/prova.test.mjs
Resultado: 8 testes, 8 passaram, 0 falhas; código de saída 0.

O conserto 1 foi atendido. juntarHooks identifica evento/índice do grupo/índice do hook
do fragmento; aprovarHooks restringe sourcePath e essas chaves, e exige a quantidade esperada.
Conferidos em execução pelo app-server: quatro hooks próprios trusted, hook alheio sem
confiança permanece sem confiança e sem tabela de aprovação; hook alheio já confiado
continua trusted com o mesmo hash, após duas instalações.

Prova migrada para agents/code/test/provas/03-codex-hooks/. Não há mais provas/ na raiz.
As pastas agents/bin e agents/test herdadas do ticket 04 permanecem na base integrada;
não são introduzidas por este ticket. A migração delas continua com seu dono.
A iniciativa mínima agora usa initiatives/ensaio-prova.

Evidência da execução de revisão: sessão 01a146cc-2725-7e10-9ea1-83c65ab0f4bc.
Sequência: inicio com bypassPermissions; marca; recusa de apply_patch; fim devolvido;
fim solto com nota_tocada=true e stop_hook_active=true; notify agent-turn-complete
na mesma sessão. O teste confere a nota recusada byte a byte e a retomada alterada.
login-apagado.txt registra apagado=true. Nenhuma pasta hub-ensaio-03-* sobrou em TEMP.
Hashes e datas de config.toml, hooks.json e auth.json globais iguais antes e depois.
Busca de marcadores de credenciais na evidência: zero ocorrências.

A execução renovou quatro arquivos rastreados da pasta evidencia; foram preservados.
O revisor não editou código, spec ou tickets.

Ressalvas da rodada 1 mantidas: notify precisa compor consumidores no kit; Stop soltou
com duas condições verdadeiras; fixture mínimo não prova frontmatter/núcleo completo;
TUI, toast e segunda máquina ficam fora desta prova. Não impedem o aceite do risco
específico: hooks e notify funcionando em codex exec com acesso total e HOME de ensaio.
