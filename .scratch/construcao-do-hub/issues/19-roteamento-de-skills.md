# 19: Roteamento de skills

Type: task
Status: resolved
Etapa: 8 (skills e acervo)
Blocked by: 04

**What to build:** A tabela de roteamento (`routing.yml`) com as primeiras linhas e o hook de entrada sem IA que injeta "use a skill X"; usar uma skill vira linha no registro de uso.

**Fonte:** Bloco do Worker 9; faixa 9 em `spec-partes/faixas-09-10.md`; ticket 15. Regras comuns: `../etapas/regras-da-construcao.md`.

**Blocked by:** 04 (Esqueleto do hub e hub de ensaio)

- [ ] um pedido de pesquisa que não cita o FreeLLMAPI recebe "use a skill" dele
- [ ] a tabela passa no esquema
- [ ] usar uma skill vira linha no registro

## Comments
- 2026-10-16 ~21h55 (maestro): passado à Vela depois do 27 (etapa 1 fechada). Primeiro commit: testes do 27 apagam as próprias pastas do TEMP; limpeza das `hub-ensaio-*` com mais de 2 horas.
- 2026-10-17 (Vela): pego (claimed). Worktree C:/context-hub-wt/ticket-19, ramo ticket-19, de integracao 0a8e17f. Primeiro: limpeza das pastas de TEMP nos testes do 27.
- 2026-10-16 ~22h05 (maestro): perguntas da Vela: (1) skill `freellmapi` (de ensaio no teste); (2) `armis-docx` entra com aviso de ausente, sem recusa; (3) máquina = `HUB_PAR_ID`, workspace = pasta da sessão relativa ao hub, registro pelo mod do Claude Code, Codex e Copilot conferidos na doc; (4) Copilot pela regra do contrato se a doc confirmar que a saída do `userPromptSubmitted` é descartada; extensão anotada para o 23; (5) o registro "a skill rodou" no fim da resposta entra no 19 (spec faixa 9, aceite), pelo hook de fim do 27, sem bloquear.
- 2026-10-16 ~22h10 (maestro): o registro do verificador do fim (indicação e "rodou") mora na mesma tabela de `agents/maestro/uso/<máquina>.md`, colunas data | evento | skill | linha da tabela | rodou | workspace | máquina. Docs conferidas pela Vela: o Copilot descarta a saída do `userPromptSubmitted` de arquivo; o Codex aceita `additionalContext` no `UserPromptSubmit`; nenhum dos dois tem evento de uso de skill (uso e "rodou" não verificados neles).
- 2026-10-17 (Vela): tabela, esquema, hook de entrada, registro de uso e fim feitos (d8e971a, f3915c3, c4e81b5; 16/16). Em curso: prova real nos três.
- 2026-10-17 (Vela): pronto para revisão em 52c6328; 19: 16/16; suíte 128 pass, 0 fail, 5 skip; ponta a ponta dos três verde. Pedida a revisão ao Fiel.
- 2026-10-17 (Vela): rodada 1 PASSA (Fiel; o Fielzinho lê depois). Avisado o Rebite.
- 2026-10-16 22h28 (integrador, Rebite): juntado em `integracao`, commit dc56d47 (merge `--no-ff` de `ticket-19` 52c6328, o HEAD da rodada 1 "passa" do Fiel; árvore juntada idêntica à do ramo). Testes: `node --test "agents/code/test/**/*.test.mjs"` sem variável. Na 1ª rodada, 1 falha intermitente fora deste ticket ("a nota arquivada vale pelo esquema de origem mais archived_at", `05-frontmatter.test.mjs`, 9,1 s); o arquivo sozinho deu 19/19 e a suíte repetida deu 133, 128 verdes, 5 pulados, 0 falhas. A ponta a ponta real não foi repetida: árvore idêntica à revisada. Ressalvas do parecer: `fim-da-resposta.mjs` importa `registro.mjs` no topo, fora do `try` (erro de carga do roteamento derruba o fim inteiro; import dinâmico dentro do `try` isolaria); `dentroDoHub` compara em minúsculas sem resolver junction (o 14 usa `realpathSync.native`); uso e "rodou" no Codex e no Copilot não verificados; o gatilho `pesquis` casa qualquer pedido de pesquisa (ajuste pelo registro, decisão do 15). A leitura do Fielzinho ficou pendente (cota). **Resolvido.**
