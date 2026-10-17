# Retomada do maestro

Reescrita em 2026-10-17 ~04h (Brasília). Atualize a cada evento.

## Mandato (Gustavo, 2026-10-17 ~04h) — vale até ele dizer o contrário

O maestro **orquestra sozinho e decide pelo Gustavo**, com critério "afiado o bastante para não quebrar nada e leve o
bastante para a execução seguir com bom progresso e alinhada ao spec". Decisão crítica que só muda uma decisão já
tomada, sem atrapalhar o resultado final, pode seguir: registre no ticket dono ("decidido pelo maestro, mandato de
2026-10-17") e na lista **Para rever com o Gustavo** abaixo. Só o realmente bloqueante fica para ele, de dia. Liberdade
parcial para abrir e fechar aplicativos e processos da execução. **Contexto do maestro: nunca passar de 700k tokens**;
o auto-compact está ligado em 600k (configuração do Gustavo), então a compactação é automática; mantenha esta retomada em dia para ela. Memória `autonomia-na-construcao`.

## Ao fim da execução (ou numa pausa bloqueante que pare tudo)

Pedido do Gustavo (2026-10-17 ~04h40): **duas peças visuais que resumam como foi a execução, cada detalhe**. O que é
cada uma, o detalhe, o tipo: o maestro decide, só nessa hora (não planejar antes). Para cada peça, um time enxuto:
**Designer + Revisor**, cada um com até 2 subagentes; as duas peças rodam em paralelo (2 Designers + 2 Revisores).
Fontes para o detalhe: este diário, `etapas/registro-de-juncoes.md`, os `## Comments` dos tickets, os pareceres e
relatórios em `etapas/`, os commits de `integracao` e do repositório de planejamento. Memórias que valem:
`visuais-pelo-designer`, `visual-diagrama-no-centro`, `legibilidade-dos-titulos`, `headless-edge-para-qa-visual`.
Por isso o diário abaixo registra cada evento com hora.

## Para rever com o Gustavo

- (processo) A suíte inteira roda só na junção, pelo Rebite; o construtor roda os testes do ticket e dos arquivos mexidos. Fila do trabalho pesado em `etapas/fila-pesada.md`.

- (técnica, ~04h35) Pontos abertos da faixa 5 decididos no 09: `delete_note` exige `base_rev` (o spec deixava a guarda em aberto); append/prepend sem base gravam como filha da versão lida.

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
- **Codex:** sem cota de novo até 06:58 de 2026-10-17 (Trilho e Fielzinho). Pendente nessa hora: Codex real do 15; leituras do Fielzinho.

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

- (antes de 01h; ver ticket 16 e registro-de-juncoes) 2026-10-16: recomeço ~14h30, revisão do spec, `/implement-spec`;
  etapas 0 e 1 completas; 15 tickets resolvidos até 00h53; portal fechado 00h24 por RAM; Codex sem cota até 01h34.
- ~01h08: maestro limpo retoma; duas suítes pesadas juntas (Brasa 00h58, Trilho 01h06, a trava sobrescrita), 1,9 GB
  livres; Trilho para a dele. Brasa limpa ~01h15.
- ~01h35: 31 e 32 juntados (Vela); ponta a ponta do Claude do 31 fica com a Vela.
- ~01h50: 32 resolvido; rodada das sobras do link enviada pelo Maestri Chat.
- ~02h00: Trilho limpo; 13 na revisão; teste único do gemini fez 62 pedidos (limite 250).
- ~02h05: 13 passa (r1). A Vela acha o buraco do CRLF na guarda (14/20) pela ponta a ponta do 31; conserto 050fb14.
- ~02h15: ticket 34 (leitura tardia do 19 pelo Fielzinho). ~02h25: ticket 35 (ressalva do 31), Trilho.
- ~02h30: Vela limpa; 13 resolvido (236b3ef). ~02h50: 31 resolvido (e82ce65) com a prova real do Codex do 20.
- ~03h00: rodada do fork do MCP enviada. ~03h10: 07 e 34 resolvidos (763813a): abre 08, 09, 28.
- ~03h15: Brasa no 08, Vela no 28. ~03h30: Gustavo responde pelo celular 1A 2A; ticket 33.
- ~03h50: Codex real: 12 passa (search aprovada no codex.toml), 15 falha: a `read` do hub-busca fura o aviso; decidido
  expor só a `search`. ~03h55: Fiel limpo.
- ~04h: mandato do Gustavo recebido.
- ~04h15: limite 4 construtores e 1 subagente por recruta; Cinzel recrutado para o 09 (a Vela fica no 28).
- ~04h20: mais até 3 subagentes Haiku 5.5 médio por recruta (tarefa simples ou QA); regras e recrutas avisados.
- ~04h35: costuras do Cinzel no 09 aceitas; decidi pelo mandato os pontos abertos da faixa 5 (append/prepend com base opcional, nota nova como raiz, move recusa destino, delete exige base_rev, read com rev). Ticket 09.
- ~04h45: real do 12 nos três passa só com a search (8558abe), rodada do Fiel pedida; 15: Claude e Copilot passam (7ad8dee); Codex sem cota de novo até 06h58 (vale também para o Fielzinho): Codex do 15 depois. Trilho roda a suíte do 35 com a trava.
- 03h47 (relógio real; as horas do diário entre ~03h e ~04h45 acima foram estimadas e estão adiantadas ~1h — use `date` daqui em diante): ronda. Brasa com a trava (teste Docker do 08, desde 03h37); Trilho espera para a suíte do 35; Vela e Cinzel trabalhando; Fiel 14%; memória livre 1,2 GB (vmmemWSL 1,9 GB do Docker); nada a destravar.
- 03:59: 08 Docker caiu por memória; aval para rodar destacado, fatia por fatia, piso 2 GB, parada abaixo de 700 MB.
- 04:00: fila do trabalho pesado criada (etapas/fila-pesada.md; regra: quem solta a trava avisa o próximo): Rebite, Cinzel (09), Brasa (08), Trilho (35). Cinzel com código do 09 pronto (fork sem commit: mandado commitar). Trilho adianta o 33 enquanto espera.
- 04:09: rodada 3 do 12 juntada (3c24d68), suíte 186/0; aceite real do Codex do 12 fechado. Trava passou ao Cinzel (09). Lições no 15 (gravar claude-settings.json na rodada real) e no 23 (kit junta a regra no settings.json).
- 04:15: 33 feito (Trilho, 07e6b92). Decisão do maestro: suíte inteira só na junção (Rebite), não mais no construtor antes da revisão (poupa memória); regra em regras-da-construcao.md; Trilho pede já a revisão do 35 e do 33.
