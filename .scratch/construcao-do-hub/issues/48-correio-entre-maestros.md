# 48: Correio entre os maestros dos dois pares

Type: task
Status: claimed
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

## Pesquisa (2026-10-24, maestro do B)

Fontes: docs do hub (`agents/code/docs/componentes/vigia.md` e `vigia-nas-telas.md`, no `main` a9f1b4d), `maestri
help` e `maestri routine create --help` (CLI 2026-10-24), a ferramenta `ListAgents` do Claude Code e a prática de
2026-10-24.

- **Como os maestros falam hoje:** cada um tem a sua retomada no repositório de planejamento (git,
  `pdgusta/hub-development`). O recado só chega com `push` de um lado e `pull` do outro, e o Gustavo avisa ("o A
  terminou", "fiz o push"). Em 2026-10-24 os dois gravaram no mesmo ticket ao mesmo tempo e o `pull --rebase` deu
  conflito duas vezes.
- **O hub já replica em ~1 min:** nota gravada no disco do B apareceu no banco do A em segundos (passo 10 do par B).
  Com um arquivo por par, ninguém escreve no arquivo do outro e não há conflito do LiveSync.
- **A vigia já tem lugar para isso:** o `estado.json` aceita itens de outros donos (`gravarItem`/`tirarItem`; a vigia
  só regrava os dela, sob trava). Os itens aparecem no início de cada sessão (contexto do modelo), na linha de status
  do Claude Code (mod `vigia-do-hub`, a cada minuto) e do Copilot (60 s), e na notificação do Codex. A linha de status
  é tela: o modelo não a vê no meio de uma sessão.
- **Acordar o maestro parado:** `maestri routine create --every <t> --terminal "<maestro>" --pre-run "<script>"
  --command "{{output}}"` digita a saída do script no terminal do maestro. Não verificado: o que acontece quando a
  saída vem vazia (se a rotina dispara mesmo assim).
- **Entre máquinas pelo Maestri ou pelo Claude Code:** o `maestri` não fala com outra máquina (help inteiro). O
  `ListAgents` do Claude Code lista sessões de outras máquinas só com o Remote Control ligado. Hoje ele vê só a sessão
  `context-hub-b4`, local. Não verificado: se os dois maestros estão na mesma conta da Anthropic.

- [ ] desenho com fonte primária, decidido em rodada
- [ ] cada maestro vê o recado do outro em minutos, sem conflito de escrita

## Comments

- 2026-10-17 ~22h50 (maestro): publicado pela ideia do Gustavo.
- 2026-10-24 (maestro do B): Gustavo: "vamos pro 48". Pesquisa em curso pelo maestro do B.
