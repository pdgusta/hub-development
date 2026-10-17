# 23: Kit de par: a forma

Type: task
Status: ready-for-agent
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
