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
- Contêineres de ensaio (Docker): só em `127.0.0.1`, nome começando por `hub-ensaio-`, apagados ao fim da etapa.
- Processo longo: em segundo plano, com registro em arquivo; nunca `taskkill` por nome (só o PID que você abriu).

## Como trabalhar

- Construa com a skill `tdd` (chame o Skill tool com `tdd`): teste de ponta a ponta primeiro, na costura mais alta.
- **Sem subagentes.** O Gustavo quer ver o trabalho no canvas.
- Dados de cliente (STRATA, VOEGOL, AVIANCA, TRF3, SBF): só o nome da iniciativa; nada de dado pessoal; notas de ensaio
  com texto inventado.
- Grave o estado em arquivo a cada passo: um `/clear` a qualquer momento não pode perder nada.

## Ao terminar

1. Testes verdes no seu ramo; `git merge integracao` no seu ramo se a ponta andou; testes de novo.
2. Peça a revisão ao revisor do canvas: `maestri ask "<revisor>" "<etapa>: pronto para revisão no ramo <ramo>,
   relatório em <caminho>"`. Aplique os consertos (até duas voltas).
3. Depois do "passa", avise o integrador **Rebite** (desde 2026-10-16): `maestri ask "Rebite" "<nome>: ticket NN
   passou na revisão, ramo ticket-NN, testes <resultado>, relatório <caminho>, parecer <caminho>"`. Ele junta em
   `integracao`, roda os testes e resolve o ticket (`juntar-tickets.md`); depois avisa o maestro, que te passa o
   próximo ticket da fronteira. O revisor avisa só o construtor.
