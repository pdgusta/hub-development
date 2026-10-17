# Regras da construção em etapas (maestro, 2026-10-16)

Valem para todo construtor e revisor das etapas. Plano decidido: `revisao/plano/proposta-de-etapas.md` (seção
"Decidido") e ticket 16, comentários de 2026-10-16.

## Fontes

- O **spec** é a fonte do que construir: `C:\Projetos\context-hub\.scratch\construcao-do-hub\spec.md` (núcleo, bloco do
  Worker da sua faixa) e `spec-partes\` (a parte da sua faixa). As marcas: **[aceita]** = escolha aceita pelo Gustavo;
  **[formato]** = vinha do plano antigo de 1 hora (minutos, dublês, "se couber", portas por faixa): **não vale mais**, use
  a entrega real da etapa anterior e faça a entrega cheia; **[ticket aberto: 56]** = fora desta construção.
- Os tickets são os 26 de `C:\Projetos\context-hub\.scratch\construcao-do-hub\issues\` (publicados por `/to-tickets`
  em 2026-10-16), com os bloqueios entre si. Os antigos, do plano de 1 hora, estão em `issues-tentativa-paralela\`, só
  para consulta. Grave o seu progresso no `## Comments` do seu ticket (data, hora, o que fez, o que falta).
- Decisão fechada só em ticket resolvido de `C:\Projetos\context-hub\.scratch\context-hub\issues\`. Se precisar de um
  fato que não está escrito, pergunte ao maestro (`maestri ask "Claude Code" "..."`); não invente.

## Onde trabalhar

- Repositório do hub: `C:\context-hub`. **Um ramo e uma worktree por ticket** (`/implement-spec`, invocado pelo
  Gustavo em 2026-10-16), a partir da ponta de `integracao`:
  `git -C C:\context-hub worktree add C:\context-hub-wt\ticket-NN -b ticket-NN integracao`. Confira que a worktree
  parte da ponta de `integracao` (se não, `git reset --hard integracao` nela). Ao pegar o ticket, mude o `Status:` dele
  para `claimed`.
  Commits pequenos, no seu ramo. Nunca mexa em `main`, `integracao` nem nos ramos `tentativa-paralela/*` (esses são
  da execução de 2026-10-15; pode consultar).
- **Onde mora o código** (Gustavo, 2026-10-16, rodada `onde-mora-o-codigo-do-hub-r2`, critério "quem chama"): o
  que um agente chama vira skill em `agents/skills/<peça>/` (a busca, a "nova iniciativa", a vigia, o arquivar); o que
  só o harness ou o kit roda vai em `agents/code/` (`hooks/`, `mods/`, `kit/`, `bin/`, `test/`). As provas da etapa
  zero ficam em `agents/code/test/provas/<prova>/`. Nada de pasta de código na raiz.
- Hub de ensaio: monte um novo em pasta vazia com o `montar.mjs` da ponta de `integracao`; o `C:\context-hub-ensaio`
  guarda uma cópia antiga dos scripts.
- **Nada global de verdade.** Hub de ensaio e pasta de configuração de ensaio (HOME de ensaio por variável de ambiente:
  `CODEX_HOME`, `COPILOT_HOME`, `CLAUDE_CONFIG_DIR` ou equivalente). Nunca grave em `~/.claude`, `~/.codex`,
  `~/.copilot`, `~/.agents` de verdade, nem registre tarefa agendada ou serviço.
- **Login dos harnesses no ensaio** (aval do Gustavo para a construção inteira, rodada
  `2026-10-16-login-dos-harnesses-no-ensaio`, 20:24): construtor ou revisor que precise do Claude Code, do Codex ou do
  Copilot de verdade copia o login para uma pasta de ensaio em `%TEMP%\hub-ensaio-<ticket>-*`: Claude,
  `%USERPROFILE%\.claude\.credentials.json` em `CLAUDE_CONFIG_DIR`; Codex, `%USERPROFILE%\.codex\auth.json` em
  `CODEX_HOME`; Copilot, só os campos de login (`lastLoggedInUser`, `loggedInUsers`) no `config.json` do `COPILOT_HOME`
  (o token fica no cofre do Windows; não copie). Apague ao fim de cada rodada; confira as pastas reais por hash antes e
  depois; modelos baratos (haiku no Claude e no Copilot, gpt-6-luna baixo no Codex); uma sessão por harness; registre
  cada uso no relatório (o que copiou, quando apagou, os hashes).
- Contêineres de ensaio (Docker): só em `127.0.0.1`, nome começando por `hub-ensaio-`, apagados ao fim da etapa.
- Processo longo: em segundo plano, com registro em arquivo; nunca `taskkill` por nome (só o PID que você abriu).

## Como trabalhar

- Construa com a skill `tdd` (chame o Skill tool com `tdd`): teste de ponta a ponta primeiro, na costura mais alta.
- **Sem subagentes.** O Gustavo quer ver o trabalho no canvas.
- Dados de cliente (STRATA, VOEGOL, AVIANCA, TRF3, SBF): só o nome da iniciativa; nada de dado pessoal; notas de ensaio
  com texto inventado.
- Grave o estado em arquivo a cada passo: um `/clear` a qualquer momento não pode perder nada.
- **Contexto acima de 40%** (Gustavo, 2026-10-16): no próximo ponto seguro (commit com testes verdes, ou o fim do
  ticket), grave `C:\Projetos\context-hub\.scratch\construcao-do-hub\etapas\retomada-<seu nome>.md`: ticket, ramo,
  worktree, o que está feito, o que falta (próximo passo exato), decisões e armadilhas do caminho, comandos de teste, e
  copie para o repositório o que estiver só no scratchpad da sessão. Responda ao maestro "<nome>: salvo para limpar". O
  maestro manda o `/clear` e depois "leia a sua retomada"; você relê as regras, o ticket e a retomada e segue.

## Ao terminar

1. Testes verdes no seu ramo; `git merge integracao` no seu ramo se a ponta andou; testes de novo.
2. Peça a revisão ao revisor do canvas: `maestri ask "<revisor>" "<etapa>: pronto para revisão no ramo <ramo>,
   relatório em <caminho>"`. Aplique os consertos (até duas voltas).
3. Depois do "passa", avise o integrador **Rebite** (desde 2026-10-16): `maestri ask "Rebite" "<nome>: ticket NN
   passou na revisão, ramo ticket-NN, testes <resultado>, relatório <caminho>, parecer <caminho>"`. Ele junta em
   `integracao`, roda os testes e resolve o ticket (`juntar-tickets.md`); depois avisa o maestro, que te passa o
   próximo ticket da fronteira. O revisor avisa só o construtor.
