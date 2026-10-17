# Relatório do ticket 20: acervo do maestro e a guarda dele (Vela)

Ramo ticket-20, worktree C:/context-hub-wt/ticket-20, de integracao dc56d47.

## Commits

- 8acd1ce: consertos do 19, separado (ressalvas do parecer-19-Vela.md): o fim da resposta carrega o registro do
  roteamento por import dinâmico dentro do try; bin/lib/caminhos.mjs resolve junction e link simbólico no fim e na
  entrada do roteamento. Suíte 131 verdes, 5 pulados.

## Decisões do maestro (2026-10-17)

1. As três lacunas de dono (registro do aval de mudança, modelo do verificador da guarda, erro de peça que sumiu) foram
   ao Gustavo na rodada 'Acervo do maestro: as três lacunas de dono'. Resposta: pendente.
2. Quem é o maestro: variável própria, HUB_PAPEL=maestro, posta pela receita de setup do papel. Sem ela, quem grava
   agents/skills/routing.yml cai na guarda. **Isso confia no ambiente do terminal: não é autenticação.** Qualquer
   processo que ponha HUB_PAPEL=maestro passa pela exceção.
3. Guarda no Claude Code: hook de settings PreToolUse com ask, no molde da guarda do 14, cumprindo o 'verificador em
   outro modelo obrigatório antes de alterar' do spec (hook do tipo agent com model, ou recusa até existir o relatório).
   Se o hook agent não servir no teste, avisar o maestro para reavaliar o mod.

## Família maestro-* (2cc4eea)

- Cinco skills: maestro-acervo (porta, tipos de peça com os vazios, regras de aval e personalização), maestro-papeis
  (Receptor, Redator, Revisor Cruzado, Escrivão, Gestor Git, Scripter, Curador de Prints, Designer de visuais, regras
  comuns, usar um papel), maestro-setups (bateria de testes, construção em etapas, guardar partitura),
  maestro-contratos (roteamento de modelos, orquestração, onde abrir) e maestro-harnesses (lembrete, guarda).
- Fontes lidas só para leitura: os papéis da biblioteca do Maestri (.maestri/roles/ dos workspaces), a partitura
  'Bateria de testes – provisioning' e o arranjo do workspace Context Hub (~/.maestri/workspaces/). Papéis
  generalizados: sem nome de cliente, sem pessoas; a parte do cliente vem do AGENTS.md da iniciativa.
- **A partitura não foi guardada junto**: as notas dela têm texto de cliente (nomes de pessoas, e-mail, tenant). A
  receita leva só terminais, papéis, modelos e ligações; a peça guardar-partitura.md manda guardar o arquivo só sem
  texto de cliente. Pede confirmação do maestro.
- Descrição no formato do hub ('Use quando ...', como a nova-iniciativa), não 'Use when'.
- Verificador: agents/code/bin/verificar-acervo.mjs (name pelo agentskills.io/specification, lida por curl;
  description até 1024 com 'Use quando'; preâmbulo; porta citada; skills maestro-* citadas existem; links do
  catálogo existem; peça fora do catálogo é aviso).
- Deslize do TDD: o verificador saiu inteiro na primeira fatia; o teste das faltas veio depois e passou de primeira.

## Guarda: por que não o hook agent (doc code.claude.com/docs/en/hooks.md, lida por curl em 2026-10-17)

- O hook agent é experimental, roda um subagente Claude (campo model) e dá ok true/false; filtra por caminho só
  pelo campo if, que é 'best-effort', relativo ao cwd ('Edit(src/**)' casa só a pasta no diretório de trabalho) e
  sem resolver junction. Rodaria um modelo a cada Write/Edit em qualquer pasta, ou deixaria passar o atalho e a
  sessão fora do hub.
- Por isso a via escolhida é a outra que o maestro aceitou: hook de comando PreToolUse, decidindo pelo caminho real;
  recusa a alteração até existir o parecer do verificador em outro modelo para aquela mudança exata; com o parecer,
  pede o aval (ask) mostrando a recomendação.

## Lembrete de início (8301996)

- agents/code/hooks/acervo/inicio.mjs: só age com MAESTRI_TERMINAL_ID; age em qualquer pasta. Claude Code e Codex:
  SessionStart com hookSpecificOutput.additionalContext (doc do Codex, developers.openai.com/codex/hooks.md, por curl);
  Copilot CLI: sessionStart com additionalContext no topo (doc docs.github.com hooks-configuration, por curl).
- Diagnóstico ao vivo (uma chamada, haiku, HOME de ensaio apagado): o Copilot CLI no -p roda o sessionStart de
  arquivo e usa o additionalContext (respondeu a palavra injetada).
- O lembrete diz 'se você é o maestro': todo terminal do Maestri tem MAESTRI_TERMINAL_ID (distinguir maestro de
  recruta segue pendente no spec). Na prova real, sem dizer ao modelo que ele é o maestro, o Copilot respondeu
  'nenhuma'; com 'Você é o maestro deste workspace' no pedido, citou maestro-acervo.

## Guarda do acervo (86a24d9)

- agents/code/hooks/acervo/decidir.mjs, guarda.mjs (reusa ADAPTADORES da guarda do 14), verificar-mudanca.mjs.
- Protege agents/skills/maestro-*/, agents/skills/nova-iniciativa/ e agents/skills/routing.yml. agents/maestro/
  fica fora. **As skills de papel do acervo**: o spec diz que a guarda as cobre, mas onde elas moram não está
  decidido; hoje os papéis são peças de maestro-papeis, já cobertas.
- Decide pelo caminho real (bin/lib/caminhos.mjs): atalho e sessão fora do hub caem na mesma guarda.
- Codex e Copilot: deny apontando agents/maestro/propostas/. HUB_PAPEL=maestro passa na tabela, nos três.
- Claude Code: peça nova sem nome parecido passa; nome parecido (sem acento, número e hífen, um começa pelo outro)
  pede aval; linha só acrescentada no SKILL.md (cabeçalho igual, texto antigo inteiro dentro do novo) passa, para a
  peça nova poder entrar no catálogo; a tabela sem HUB_PAPEL pede aval; alterar uma peça ou o catálogo: deny até o
  parecer do verificador para aquela mudança exata (chave sha256 de caminho + texto final; pendente e parecer em
  <hub>/.local/acervo/); com o parecer, ask com a tela de aval (o que muda, quem usa pelo registro de uso,
  personalização 'não verificado', alternativa de variante, recomendação do verificador).
- Verificador: HUB_VERIFICADOR, senão 'claude -p --model sonnet' (**provisório**: quem escolhe o modelo é lacuna
  com o Gustavo).
- Pede confirmação do maestro: (a) 'linha acrescentada no catálogo passa' (o spec diz 'mexer no catálogo pede aval'
  e também 'peça nova sem sobreposição é livre'); (b) Bash, PowerShell e o shell do Codex não passam pela guarda
  (ela olha Write/Edit/MultiEdit, apply_patch, create/edit), como a do 14.
- Registro de uso: já entregue no 19 (hooks/roteamento/uso.mjs e registro.mjs); a guarda o deixa fora (testado).

## Testes

- agents/code/test/20-acervo.test.mjs: 11/11 (família, faltas, lembrete nos três, guarda nos três pelo caminho
  real, pelo atalho e fora do hub, propostas, uso, tabela com e sem HUB_PAPEL, parecer e aval com verificador dublê).
- Consertos do 19: 27-fim-da-resposta e 19-roteamento com o atalho e o registro quebrado.
- Suíte depois de juntar integracao c5b946a (c6a31da): 155 pass, 0 fail, 6 pulados.

## Prova real (e5d24a7), HUB_HARNESS_REAL=1

- ponta-a-ponta/20-acervo.test.mjs: sessão aberta FORA do hub, com MAESTRI_TERMINAL_ID; troca pelo atalho, peça nova
  pelo caminho real, proposta pelo atalho.
- Claude Code (haiku): verde. Troca recusada esperando o verificador; redator-2.md pediu aval; proposta gravada.
- Copilot CLI (claude-haiku-5.5): verde. As duas gravações recusadas com o caminho de propostas; proposta gravada.
- Codex (gpt-6-luna baixo): **não rodou**, a conta estava sem cota ('usage limit' até 2026-10-17 01:34).
- Logins copiados para %TEMP%/hub-ensaio-20-* (Claude: .credentials.json; Copilot: só lastLoggedInUser e
  loggedInUsers), apagados ao fim de cada rodada (apagado: true); hashes dos arquivos reais iguais antes e depois
  (evidencia-20/hashes-*.json). Duas rodadas a mais no Copilot e uma no Claude, para ajustar o pedido (o modelo
  parava na primeira recusa).

## Decisões do maestro sobre os três pontos (2026-10-17)

1. Linha acrescentada no catálogo passa sem aval: foi ao Gustavo (rodada 'Catálogo do acervo: linha nova pede
   aval?'). Fica como está até a resposta.
2. Partitura sem o texto de cliente: certo, o acervo é genérico. Guardada só a receita
   (agents/skills/maestro-setups/bateria-de-testes.md). **Ficou de fora**, por ser texto de cliente: o conteúdo das
   notas (o roteiro de testes, o registro dos testes, o plano de seção, os rascunhos e a versão final do e-mail, o
   roteiro de laboratório, a caixa de entrada), o histórico dos terminais (terminalChatArchives) e o próprio arquivo
   .maestripartitura. Ficaram o nome das notas, o dono e as ligações; os codinomes e os comandos dos terminais.
3. Verificador provisório em Sonnet: ok até a rodada das três lacunas de dono.

## Revisão

- Pedida ao Fiel em e5d24a7. A prova do Codex entra depois de 01:34, num commit só de evidência, com rodada curta do
  Fiel.

## Rodada 1 do Fiel: volta, dois consertos (5811579)

1. Texto inserido no SKILL.md passava sem aval. Agora só passa linha de catálogo: linha de tabela ou item de lista
   com link para peça que existe na pasta da skill (sem '..', sem caminho absoluto, sem esquema). Regra ou texto
   novo vai ao verificador e ao aval. Teste: 'no catálogo, só a linha que aponta peça existente passa'.
2. Peça em pasta nova da família (maestro-novo/peca.md) dava ENOENT e a guarda passava sem conferir. Agora é de
   propósito: skill nova da família é peça nova; passa no Claude Code, salvo nome parecido com uma skill maestro-*
   que existe (maestro-papeis-2 pede aval); Codex e Copilot recusam. Teste: 'peça numa skill nova da família'.
- 20-acervo 13/13; suíte 157 pass, 0 fail, 7 pulados.

## Rodada 2 do Fiel: PASSA (5811579)

- Ressalva: a descrição de um item de catálogo é texto livre (a linha só precisa apontar peça existente).
- Pendente: a prova real do Codex (sem cota até 01:34), num commit só de evidência, com rodada curta do Fiel.
