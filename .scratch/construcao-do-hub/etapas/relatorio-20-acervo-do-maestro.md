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
