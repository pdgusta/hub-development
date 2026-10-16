# Ordem de execução (/implement-spec, 2026-10-15)

Para cada Worker N, com o ticket NN = N (o 11 é do Worker 8, depois do 08):

1. Ticket: `C:\Projetos\context-hub\.scratch\construcao-do-hub\issues\NN-*.md`. Spec: `..\spec.md` e a sua parte em
   `..\spec-partes\`. Plano e fronteiras: `..\planejamento\plano.md`. Contrato de eventos do painel:
   `..\painel\contrato.md`.
2. Repositório do hub: `C:\context-hub`, ramo de integração `integracao`. Crie a sua worktree:
   `git -C C:\context-hub worktree add C:\context-hub-wt\faixa-NN -b faixa-NN integracao` e confira que ela parte da
   ponta de `integracao` (se não, `git reset --hard integracao` nela).
3. Mude o `Status:` do ticket para `claimed` e construa com a skill `tdd` (chame o Skill tool com `tdd`). Até 10
   subagentes; parte muito complexa: um subagente Fable 5.1 médio (modelo `fable`, esforço médio).
4. Nada global de verdade: HOME de ensaio. O Docker está desligado até o Gustavo dar o aval (rodada 2 do ticket 16):
   faixas 4, 5 e 7 começam pelos dublês.
5. Ao terminar: faça merge da ponta de `integracao` no seu ramo, rode os testes de novo, peça revisão ao seu Prumo
   (Workers 1-5: Prumo; 6-10: Prumo 2) por `maestri ask`, mude o `Status:` para `review` e avise o seu maestro
   (Workers 1-5: "Claude Code"; 6-10: "Amigo do Maestro") com o ramo e o resultado dos testes.
6. A execução inteira dura 1 hora: ao bater a hora, grave o estado no ticket (`## Comments`) e no plano ("Fica para
   outra execução"), faça commit no seu ramo e avise.
