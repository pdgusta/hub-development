# 19: Roteamento de skills

Type: task
Status: claimed
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
