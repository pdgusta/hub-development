# Retomada do maestro

Reescrita em 2026-10-17 ~04h (Brasília). Atualize a cada evento.

## Mandato (Gustavo, 2026-10-17 ~04h) — vale até ele dizer o contrário

O maestro **orquestra sozinho e decide pelo Gustavo**, com critério "afiado o bastante para não quebrar nada e leve o
bastante para a execução seguir com bom progresso e alinhada ao spec". Decisão crítica que só muda uma decisão já
tomada, sem atrapalhar o resultado final, pode seguir: registre no ticket dono ("decidido pelo maestro, mandato de
2026-10-17") e na lista **Para rever com o Gustavo** abaixo. Só o realmente bloqueante fica para ele, de dia. Liberdade
parcial para abrir e fechar aplicativos e processos da execução. **Contexto do maestro: nunca passar de 700k tokens**;
o auto-compact está ligado em 600k (configuração do Gustavo), então a compactação é automática; mantenha esta retomada em dia para ela. Memória `autonomia-na-construcao`.

## Para rever com o Gustavo

- (técnica, 2026-10-17 ~03h50) O hub-busca expõe só a `search` nos três harnesses (a `read` dele furava o aviso de
  leitura do 15); Claude por `deny` de `mcp__hub-busca__read`. Ticket 15.
- (técnica) Tickets de conserto publicados pelo maestro: 34 (roteamento), 35 (aval sem parecer). Tornar local faz
  `git rm -r --cached` (histórico guarda o antigo). Ticket 33 foi ao Trilho, não à Vela como dizia a opção.

## Leia nesta ordem

Caminhos relativos a `C:\Projetos\context-hub\`.

1. **Este arquivo**, inteiro.
2. `AGENTS.md` e o `MEMORY.md` da memória (já vem no contexto). Memórias que mandam no dia a dia: `autonomia-na-construcao`,
   `maestro-nao-executa`, `contexto-dos-recrutas-40`, `rodadas-pelo-chat`, `rodada-explicacao-acima-das-perguntas`.
3. `.scratch/construcao-do-hub/etapas/regras-da-construcao.md`, inteiro (o que os recrutas seguem).
4. `.scratch/construcao-do-hub/etapas/juntar-tickets.md` e `revisao-em-dupla.md` (o fluxo do Rebite e da dupla).
5. `.scratch/construcao-do-hub/issues/`: a linha `Status:` e `Blocked by:` dos 32 tickets (a fronteira) e o `## Comments`
   dos `claimed`.
6. `.scratch/context-hub/issues/16-passagem-para-a-construcao.md`: só os comentários de 2026-10-16 e 2026-10-17 (fim do
   arquivo; toda decisão do Gustavo está lá, em ordem).
7. Só se precisar: `.scratch/construcao-do-hub/spec.md` (nota "Onde mora o código" no topo) e `spec-partes/`.

Depois, confira o mundo real: `maestri list`, `maestri check` de cada recruta (contexto pela barra), `git -C
C:\context-hub log --oneline -3 integracao`, `etapas/trava-pesada.md` e `etapas/registro-de-juncoes.md`.

## Como a operação funciona agora

- **Construção pelo `/implement-spec`**, invocado pelo Gustavo em 2026-10-16. **Até 4 construtores, cada recruta até 1 subagente por vez mais até 3 Haiku 5.5 médio para tarefa simples ou QA** (Gustavo, 2026-10-17 ~04h; regras atualizadas; o papel ainda diz "sem subagentes", não editar papel em uso). Plano em
  `.scratch/construcao-do-hub/revisao/plano/proposta-de-etapas.md` ("Decidido").
- **Ciclo de um ticket:** o construtor faz (skill `tdd`), pede revisão ao **Fiel**, que revisa em dupla com o
  **Fielzinho**; depois do "passa", o construtor avisa o **Rebite**, que junta em `integracao` (worktree
  `C:\context-hub-wt\integracao`), roda a suíte, resolve o ticket e avisa o maestro. O maestro **não junta nem executa a
  construção** e não é o centro da comunicação (os três construtores estão ligados entre si); ele passa o próximo ticket
  da fronteira, responde perguntas técnicas (registrando no ticket) e decide pelo Gustavo (mandato acima).
- **Decisões do Gustavo (só o bloqueante, de dia):** o portal está **fechado** desde 2026-10-17 00h24 (RAM curta; o servidor parou, o terminal
  "Portal" fica no canvas, religa com `.\iniciar.cmd` na pasta do portal). Enquanto isso, cada rodada é escrita em
  `.scratch/context-hub/portal/rodadas/` (explicação lá; validar com `leitores._parse_perguntas`) e enviada pelo
  **Maestri Chat, thread blue** (`maestri say`, curta, opções e a recomendada); a resposta dele vale como da rodada:
  `estado: absorvida`, nota "respondida pelo Maestri Chat", absorver no ticket dono.
- **Commits do repositório de planejamento** (`C:\Projetos\context-hub`, ramo `main`, sem remoto) a cada rodada absorvida
  ou ticket resolvido; o maestro faz (varredura e git são dele). Rodapé do commit: `Co-Authored-By` e `Claude-Session`.
- **Contexto dos recrutas:** acima de 40%, no próximo ponto seguro o recruta grava `etapas/retomada-<nome>.md` e diz
  "salvo para limpar"; com ele ocioso e sem fila, `MSYS_NO_PATHCONV=1 maestri ask "<nome>" --raw "/clear\r"`, depois
  "leia a sua retomada". No Codex (Fielzinho): `--raw "/new\r"`, `--raw "1"`, retomada. Nada de `&` dentro de comando
  em segundo plano (o envio morre com o shell).
- **Memória da máquina no limite** (commit ~30 de 35,7 GB; o Docker é uma VM Hyper-V de 4 GB fixos; `wsl --shutdown`
  não ajuda). Regra **"Um trabalho pesado por vez"** com a trava `etapas/trava-pesada.md` (Docker, suíte inteira,
  indexação, npm, harness real). Suíte comum: `node --test "agents/code/test/**/*.test.mjs"` sem `HUB_HARNESS_REAL`
  (os de harness ficam pulados; ticket 29); `--test-concurrency=1` sob carga. Se travar de novo, as saídas são do
  Gustavo: baixar a memória do Docker (Settings > Resources) ou aumentar o arquivo de paginação.
- **Codex:** cota de volta desde 01:34.

## Quem está no canvas (2026-10-17 ~04h)

- **Brasa** (Claude Opus 5.5 médio, construtora): **08** (banco: limites e robustez), worktree ticket-08 de 763813a;
  costuras confirmadas (teste Docker `08-banco-limites.test.ps1`, laço `kit/par/banco/laco.ps1` com XML da tarefa sem
  registrar, retrato em `agents/code/test/banco/retrato/`). Limpa ~01h15.
- **Vela** (idem): **28** (pastas locais); depois, o próximo da fronteira. Limpa ~02h30.
- **Trilho** (idem): refaz o real do 12 e do 15 nos três (só a `search` do hub-busca), rodada do Fiel; depois suíte e
  revisão do **35** (código feito, 4a17dbe); depois **33**. Limpo ~02h00.
- **Cinzel** (Claude, construtor novo, ~04h15): **09** (MCP do banco), fork em `C:\Projetos\hub-mcp-banco`. Ligado a
  Brasa, Vela, Trilho, Fiel, Rebite.
- **Fiel** (Claude Opus 5.5 médio): revisor principal; estado em `etapas/estado-revisor.md`. Limpo ~03h55.
- **Fielzinho** (Codex GPT 6-Astra médio): revisor parceiro, com cota; leituras atrasadas na fila do Fiel.
- **Rebite** (Claude): junta e resolve.
- **Portal** (terminal do servidor, parado).

## Placar (2026-10-17 ~04h)

- Resolvidos (19 de 35): 01-07, 12-15, 19, 20, 27, 29-32, 34 (`integracao` 763813a). 26 originais: 13 resolvidos.
- Em curso: 08 (Brasa), 28 (Vela), 35 + real do 12/15 (Trilho). Fila: 09 (Vela), 33 (Trilho).
- Abrem depois: 10 (09+05), 16 (08+10), 22 (10+12), 11 (10), 17 → 18, 21, 23 → 24 → 25; 26 é do Gustavo.

## Decisões do Gustavo em 2026-10-16/17 (detalhe no ticket 16)

Lugar do código (`agents/skills/` para o que o agente chama, `agents/code/` para o motor); tabela `stage`→`status`;
`operations/` não é iniciativa; login dos harnesses no ensaio liberado para a construção inteira; receita da etapa 2
(Brasa 07 e 08); pastas locais (script, vigia roda o gerador, tornar local, `.git/info/exclude`); laço do fim da
resposta (até três devoluções); linha nova no catálogo é livre; três lacunas do acervo (avais em
`agents/maestro/avais/`, o maestro escolhe o verificador, peça sumida vira item da vigia); link fora do hub
`par://<par>/<unidade>/<caminho>`; teste único do gemini liberado; fork do MCP em repositório próprio
`C:\Projetos\hub-mcp-banco`, só local (A); ticket 33 das sobras do link (A). Radar: recrutas em sessões do Claude na
nuvem.

## Diário (mais novo embaixo)

- ~04h: mandato do Gustavo recebido.
- ~04h15: limite 4 construtores e 1 subagente por recruta; Cinzel recrutado para o 09 (a Vela fica no 28).
- ~04h20: mais até 3 subagentes Haiku 5.5 médio por recruta (tarefa simples ou QA); regras e recrutas avisados.
