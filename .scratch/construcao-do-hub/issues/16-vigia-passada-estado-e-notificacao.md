# 16: Vigia: passada, estado e notificação

Type: task
Status: claimed
Etapa: 6 (vigia)
Blocked by: 08, 10

**What to build:** A vigia lê o banco real (cifrado) e o disco, grava o estado num arquivo local por troca atômica e avisa só quando piora. Confere a ferramenta `estado_do_hub` do MCP com o estado real (até aqui ela usava um exemplo). O item da cópia diária entra como exemplo; a etapa 9 o confere com o real.

**Fonte:** Bloco do Worker 7; faixa 7 em `spec-partes/faixas-07-08.md`; tickets 33, 08, 14, 34, 48; escolhas aceitas 6, 7, 8 e 22. Regras comuns: `../etapas/regras-da-construcao.md`.

**Blocked by:** 08 (Banco: limites e robustez), 10 (MCP do banco: três instâncias, cabeça, regra curta e estado)

- [ ] os cenários dão o estado esperado: tudo em ordem, conflito de texto, binário descartado, replicação parada com o outro par ligado, outro par incerto ("informa" com o motivo), arquivo acima de 200 MiB, sincronizador parado, Config Doctor travado, item da cópia diária
- [ ] a vigia cita a nota pelo caminho decifrado
- [ ] a notificação do Windows sai só na passada que piora
- [ ] o comando de recuperar devolve os bytes do binário perdido
- [ ] o `estado_do_hub` devolve o estado real

## Comments
- 2026-10-16 20h32 (integrador, Rebite): lição do ticket 06 (parecer do Fiel, rodada 2, `etapas/01-esqueleto/parecer-Vela.md`): `agents/code/bin/gerar-exclusoes.mjs` recusa com código 2, sem gravar, se algum `index.md` tem YAML ilegível, e isso trava a lista inteira. Quem chama o gerador tem de mostrar esse erro, não engolir. Pasta local criada com o CLI rodando vaza: parar, gerar, religar.
- 2026-10-16 20:38 (maestro): decisão do Gustavo (rodada `2026-10-16-pastas-locais-depois-do-gerador`, pergunta 2, A): a vigia roda o gerador de exclusões a cada passada; se a lista mudou, religa o sincronizador e avisa; se o gerador recusar (YAML ilegível, código 2), vira item da vigia com o caminho. Entra neste ticket.
- 2026-10-16 21h51 (integrador, Rebite): lição do ticket 27 (parecer do Fiel, `etapas/parecer-Vela.md`, rodadas 1 e 2): o hook `fim-da-resposta` devolve até três vezes e na quarta parada solta para a vigia; os avisos novos dessa quarta parada não são entregues nem marcados como avisados. A vigia precisa casar com o item `fim-da-resposta` que o hook deixa.
- 2026-10-16 23h10 (integrador, Rebite): lição do ticket 12 (parecer do Fiel, `etapas/parecer-12-Trilho.md`, achado 2 do relatório `etapas/relatorio-12-busca.md`): o `reindex` incremental da busca é costura com a vigia.
- 2026-10-17 00:21 (maestro): decisão do Gustavo (rodada `acervo-do-maestro-tres-lacunas`, 3 A): a conferência do acervo grava um item no `estado.json` quando um catálogo cita peça que sumiu (ticket 31); a vigia o lê e mostra como os outros.

- 04:23 (maestro, decidido pelo mandato de 2026-10-17): começa antes dos bloqueios, com o Trilho, sobre a ponta de `integracao` (o 07 já está lá): a passada, o estado por troca atômica, a notificação só quando piora, a citação pelo caminho decifrado e o recuperar. Os cenários que dependem do 08 (binário descartado, acima de 200 MiB, sincronizador parado, laço) e o `estado_do_hub` real (10) entram quando eles forem juntados (`git merge integracao` no ramo). Junção só com 08 e 10 resolvidos.
- 2026-10-17 ~04h50 (Trilho): pego (claimed). Worktree C:/context-hub-wt/ticket-16, ramo ticket-16, de integracao 33b817a. Costuras propostas em etapas/costuras-16-Trilho.md.

- 04:26 (maestro, decidido pelo mandato; o spec deixava "piora" em aberto, faixa 7): **piora = algum item sobe de nível em relação à passada anterior; item novo conta como "ok" antes** (então item novo acima de ok notifica). Sem repetição enquanto nada sobe; um item que desce e volta a subir notifica de novo. Lugar: `agents/skills/vigia/` (spec, "Onde mora o código": a vigia com `vigia recuperar` é skill). Costuras do Trilho aceitas (`etapas/costuras-16-Trilho.md`).
- 2026-10-17 ~05h40 (Trilho): código da vigia feito (ff0f362, 16-vigia.test.mjs 8/8). Docker 1ª rodada: 6 falhas, consertadas em ff0f362, a rodar de novo pela fila. Estado em etapas/retomada-Trilho.md e etapas/costuras-16-Trilho.md.
