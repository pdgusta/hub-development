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
