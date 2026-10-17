# 23: Kit de par: a forma

Type: task
Status: claimed
Etapa: 10 (kit de par)
Blocked by: 11, 15, 17, 18, 20, 27

**What to build:** O kit de par, numa pasta de configuração de ensaio: liga o contrato (link simbólico e import), as skills de uso geral por junction, as linhas de MCP nos três harnesses e os hooks de todas as etapas; tira o GSD do escopo global com cópia. Idempotente, com simulação, cópia e hash antes de tocar e desfazer.

**Fonte:** Bloco do Worker 8; faixa 8 em `spec-partes/faixas-07-08.md`; tickets 14, 42, 13, 18, 15. Regras comuns: `../etapas/regras-da-construcao.md`.

**Blocked by:** 11 (MCP do banco pelos três harnesses), 15 (Guardas: aviso de leitura fora da busca), 17 (Vigia nas telas dos harnesses), 18 (Retomada: nota de sete campos, início e fim), 20 (Acervo do maestro e a guarda dele), 27 (O verificador cuida das pastas: traz o fragmento de fim de resposta)

- [ ] roda duas vezes e a segunda não muda nada; desfaz sem sobra
- [ ] cada link aponta para o `AGENTS.md` do hub de ensaio; a junction expõe só as skills de uso geral
- [ ] cada configuração tem as linhas de MCP e os hooks juntados

## Comments
- 2026-10-16 ~21h20 (maestro, da prova 03 da Vela, `etapas/00-provas/relatorio-codex.md`): (1) o `notify` do Codex é um só: o do hub substituiria o do Computer Use, então o kit precisa compor os consumidores num programa só; (2) o Codex regrava o `config.toml`: editar por chave e tabela, nunca por texto; (3) o hash em `hooks.state` aprova o comando, não o conteúdo do script: proteger o script por outro meio; (4) o `Stop` soltou com duas condições verdadeiras (`nota_tocada` e `stop_hook_active`); TUI, toast e segunda máquina não foram provados.
- 2026-10-16 20h32 (integrador, Rebite): lição do ticket 06 (parecer do Fiel, rodada 2, `etapas/01-esqueleto/parecer-Vela.md`): `agents/code/bin/gerar-exclusoes.mjs` recusa com código 2, sem gravar, se algum `index.md` tem YAML ilegível, e isso trava a lista inteira. Quem chama o gerador tem de mostrar esse erro, não engolir. Pasta local criada com o CLI rodando vaza: parar, gerar, religar.
- 2026-10-17 04h08 (integrador, Rebite): lição do 12, rodada 3 (parecer do Fiel, `etapas/parecer-12-Trilho.md`, ressalva 3): `agents/code/kit/par/busca/registro/claude-settings.json` só é usado nos testes. O kit que o instalar tem de **juntar** a regra na `permissions.deny` do `settings.json` de verdade, sem sobrescrever.

- 07:32 (maestro): lição do 15 (Trilho): no Codex, hífen do nome do servidor MCP vira sublinhado no hook; os matchers do kit usam o sublinhado no Codex.

- 07:34 (maestro): do 21: o passo `10-manutencao.ps1` (XML da tarefa diária da cópia e da vigia, sem registrar, com -WhatIf) entra aqui.

- 07:53 (maestro): do 11 (Cinzel, parecer `../etapas/parecer-11-Cinzel.md`): (1) o Copilot sem `--allow-all-mcp-server-instructions` não põe as instruções do servidor no prompt: o kit liga a opção ou põe o hub-banco na lista permitida; (2) o Claude Code adia as ferramentas MCP: a regra curta do `write_note` só chega depois de um ToolSearch; a cabeça do AGENTS.md chega pelas instruções.
- 07:53 (maestro, mandato): começa já com o Cinzel, sobre a ponta de `integracao`: o esqueleto do kit (ordem dos passos, -WhatIf, cópia e hash antes de tocar, desfazer, contrato por link e import, junction das skills, linhas de MCP, GSD fora do global com cópia, `10-manutencao.ps1`); os hooks de 11, 17 e 18 entram por merge quando forem juntados. Junção só com todos os bloqueios resolvidos.
- 2026-10-17 ~08h20 (Cinzel): peguei o 23 (`claimed`). Worktree `C:/context-hub-wt/ticket-23` de `integracao` e2b7607. Costuras propostas ao maestro: `../etapas/costuras-23-Cinzel.md`. O Codex do 11 continua com prioridade às 12h15.

- 08:00 (maestro, mandato): costuras do Cinzel aceitas (`../etapas/costuras-23-Cinzel.md`). (1) skill de uso geral = `metadata.camada: geral` no frontmatter do `SKILL.md` (campo `metadata` do formato de skill), já em busca, maestro-*, nova-iniciativa e nova-pasta-local; (2) arquivo global com texto além do GSD: o kit para e mostra o trecho; pasta de skill de mesmo nome vai para a cópia e vira junction; (3) o app-server do Codex por segundos, sem modelo e sem login, roda sem a trava.
- 2026-10-17 08:45 (Cinzel): esqueleto pronto no ramo `ticket-23` e9dcef7 (com `integracao` e98a891): instalar.ps1, casa com cópia/hash/desfazer, contrato, skills gerais (`metadata.camada: geral`), MCP de busca e banco, hooks com hooks.state, GSD fora, Codex em acesso total, 00 e 10-manutencao. `23-kit.test.mjs` 13/13; com 19, 20 e 04, 67/67. Relatório `../etapas/relatorio-23-kit-de-par-a-forma.md`. Revisão pedida ao Fiel. Fica para depois de 17 e 18: mod, extensão, statusLine e notify composto.
- 2026-10-17 ~09h45 (Cinzel): rodada 1 do Fiel: VOLTA por 1 conserto (grupo do hub velho ficava). Consertado no `ticket-23`; 14/14; rodada 2 pedida. Recado da Vela (18): o `fragmentos/claude.json` do fim da resposta entra sozinho pela junção genérica; o teste lê as peças do repositório.
- 2026-10-17 ~09h55 (Cinzel): rodada 2 do Fiel PASSA (`../etapas/parecer-23-Cinzel.md`), ramo `ticket-23` f304e6c, 14/14. Rebite avisado: junção só com 11, 15, 17, 18, 20 e 27 resolvidos (mandato). Fielzinho lê depois das 12h15.
- 2026-10-17 ~09h35 (Cinzel): reaberto pelo Fiel (detector do 29 sem exceção para o app-server). Conserto a419182: exceção estreita com motivo e teste; `harness-real.test.mjs` 7/7. Rodada 3 pedida.
- 2026-10-17 09:23 (Cinzel): rodada 3 do Fiel PASSA em a419182 (harness-real 7/7 no 23 e no 24). Ressalva: a exceção olha só o texto do teste; o kit roda por pwsh e não é importado. Rebite avisado da ponta nova.

- 10:37 (maestro): lição do 21 (Trilho): o kit grava `HUB_ROOT` e afins no caminho longo do Windows (nome curto faz o `fs.watch` do node abortar, libuv fs-event.c:72).
- 2026-10-17 ~11h10 (Cinzel): lição do 21 aplicada: e6e5faa, o `instalar.ps1` passa hub, casa e .env pelo `realpathSync.native` (o `Resolve-Path` guardava o `GUSTAV~1.DEL`). Teste novo "hub, casa e .env com o nome curto"; o ajudante `ensaio()` usa o caminho longo. 23-kit + harness-real 22/22 (`../etapas/logs/23-nome-curto.log`). Levado ao `ticket-24` por merge (5325a4b). Rodada curta pedida ao Fiel.
