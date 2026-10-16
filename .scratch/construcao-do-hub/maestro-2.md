# Amigo do Maestro: como ser maestro aqui (passagem do maestro "Claude Code", 2026-10-15 ~21h40)

O Gustavo te criou para dividir o trabalho comigo. Ele deu **40 minutos** (até ~22h20) para avançar o máximo com 12
recrutas Opus 5.5 alto, sem limite de tokens. Responda sempre em pt-BR.

## Divisão do trabalho

- **Você (Amigo do Maestro): a frente do painel da construção.** Coordena Tech lead, UI engineer, UX revisor e QA
  tester (já ligados a você e entre si) até o painel abrir ao vivo com a fixture e, depois, com a execução de verdade.
  Fontes: `.scratch/construcao-do-hub/painel/brief.md` (o pedido), `painel/contrato.md` (o formato dos dados, do Tech
  lead), `painel/mesa.md` (o registro da equipe). Meta dos 40 min: o painel aberto em `http://127.0.0.1:8771/` com a
  fixture ao vivo, revisado pelo UX e testado pelo QA. Quando abrir, eu (Claude Code) cadastro a carta do portal que
  aponta para `painel/abrir.html`. Também é seu o **Designer** (ligado a você): ele está parado; se o Gustavo aprovar a
  carta `amostra-da-cidade` (ticket 56), peça a ele a troca do `.scratch/context-hub/system-design.html` pela amostra.
- **Eu (Claude Code): a construção.** A rodada Ralph de planejamento dos 12 (`planejamento/`), a spec, os tickets e a
  execução; a caixa do portal (as mensagens do Gustavo chegam a mim).
- Fale comigo por `maestri ask "Claude Code" "<recado>"`, curto, só quando precisar.

## Regras do Gustavo (as que mais pesam)

- **File-first:** grave cada decisão no arquivo dono na hora; um `/clear` a qualquer momento não perde nada.
- **Decisão só no portal** (`.scratch/context-hub/portal/rodadas/`); no terminal, avise em uma linha. Uma decisão por
  vez, sempre com recomendação. Nunca cite código interno (R18, T2) sem dizer o que é.
- **Fonte primária** antes de explicar ferramenta; marque "não verificado" o que não conferiu.
- **Visuais só pelo Designer** ou pela equipe de design, nunca direto pelo maestro.
- **Recrutas:** ligue você mesmo com `maestri connect "A" "B"` (nunca peça ao Gustavo); nunca edite o papel de um
  recruta em uso (`maestri role edit/write/assign` reinicia o terminal e perde o contexto), mande instrução por
  `maestri ask`; `/clear` num recruta só depois que ele gravar a retomada; comando que remove recruta leva o comentário
  `# risco-avaliado: <motivo>`. Ask longo com `run_in_background`. Texto cinza no input do recruta é sugestão, não
  texto real. Maestri pelo Git Bash com `MSYS_NO_PATHCONV=1`.
- **Edge sem cabeça** só com perfil próprio (`--user-data-dir`); mate só os `msedge` desse perfil, nunca
  `taskkill` por nome.
- Não leia arquivos de credencial; não toque em `~/.claude`, `~/.codex`, `~/.copilot` sem cópia e hash.
- Dados de cliente (STRATA, VOEGOL, AVIANCA, TRF3, SBF): só o nome da iniciativa.
- Sem risada no chat; sem subagente Claude por conta própria sem dizer o custo antes (nesta construção o Gustavo
  liberou: sem limite de tokens).
- O "Portal" no `maestri list` é o terminal do servidor do portal (`http://127.0.0.1:8770/`), não um agente: não mande
  `ask` a ele nem o desligue.

## Onde está o quê

- Estado do maestro: `.scratch/context-hub/retomada-maestro.md`. Mapa de decisões: `.scratch/context-hub/map.md`.
  Ticket da construção: `.scratch/context-hub/issues/16-passagem-para-a-construcao.md`.
- Grave o seu estado em `.scratch/construcao-do-hub/maestro-2-retomada.md` a cada passo relevante.

Ao ler isto, responda a mim: `maestri ask "Claude Code" "Amigo do Maestro: li, assumo o painel"` e comece.

## Atualização ~21h50: mais construção para você (pedido do Gustavo: "se ele ficar só com o painel fica fraco")

- **Agora: a rodada Ralph é sua.** Você toca as voltas (`planejamento/volta.sh <N>`, em segundo plano; a volta 1 já
  foi disparada por mim e ainda corre). Pare em no máximo 2 voltas (o tempo é curto). Na **volta 2**, acrescente ao
  `PROMPT.md` (entre voltas, nunca durante): "Se `.scratch/construcao-do-hub/spec.md` existir, confira a parte da spec
  que toca a sua faixa e corrija os erros direto nela (troca de trecho), registrando no `voltas.md`" — o Gustavo pediu
  que os workers arrumem os erros da spec.
- **Eu escrevo a spec** (`/to-spec`, invocado pelo Gustavo), com subagentes, em `.scratch/construcao-do-hub/spec.md`.
  Os tickets de construção vão nascer em `.scratch/construcao-do-hub/issues/NN-slug.md` (convenção do rastreador em
  `docs/agents/issue-tracker.md`), não em `execucao/tickets/`: avise o Tech lead para o painel ler de lá.
- **Na execução: você coordena Worker 6 a 10 e o Prumo 2; eu, Worker 1 a 5 e o Prumo.** Você já está ligado aos 12.
