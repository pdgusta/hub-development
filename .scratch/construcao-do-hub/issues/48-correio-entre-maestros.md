# 48: Correio entre os maestros dos dois pares

Type: task
Status: needs-triage
Etapa: depois do 26 (os dois pares de pé)
Blocked by: 26

**What to build:** O maestro do outro PC é outra sessão; os dois precisam conversar e não pisar um no outro. Ideia do
Gustavo (2026-10-17 ~22h45): **um arquivo de retomada no próprio hub, com cada maestro de cada par lendo por um job**.
Pesquisar na fonte primária antes de desenhar e decidir por rodada:
- recados num caminho que replica (ex.: `operations/hub-development/maestros/`), um arquivo por par para não haver
  conflito de escrita (cada maestro só escreve no seu, lê o do outro), com a vigia ou uma tarefa agendada avisando
  quando o do outro muda (memória `aviso-por-vigia-local`: "chegar ao maestro" = vigia lendo arquivo local);
- o conflito de texto do LiveSync quando os dois escrevem no mesmo arquivo (as duas versões ficam; a vigia acusa);
- algum recurso do Maestri entre máquinas (não verificado).

- [ ] desenho com fonte primária, decidido em rodada
- [ ] cada maestro vê o recado do outro em minutos, sem conflito de escrita

## Comments

- 2026-10-17 ~22h50 (maestro): publicado pela ideia do Gustavo.
