# 20: Acervo do maestro e a guarda dele

Type: task
Status: ready-for-agent
Etapa: 8 (skills e acervo)
Blocked by: 19, 03

**What to build:** A família `maestro-*` com o primeiro lote, o lembrete de início que só age dentro do Maestri e a guarda do acervo, que decide pelo arquivo de destino, inclusive pelo atalho e fora do hub. As propostas do Codex e do Copilot e o registro de uso ficam fora da guarda.

**Fonte:** Bloco do Worker 9; tickets 40, 43, 44; escolha aceita 17. Perguntas ao Gustavo na hora: as três lacunas de dono (onde fica o registro do aval de mudança no contrato, quem escolhe o modelo do verificador da guarda, como chega a ele o erro de peça que sumiu). Regras comuns: `../etapas/regras-da-construcao.md`.

**Blocked by:** 19 (Roteamento de skills), 03 (Prova: hooks do Codex em acesso total)

- [ ] sem o Maestri, o hook de início não faz nada; com ele, injeta o lembrete
- [ ] gravar numa peça protegida pede aval no Claude Code e é recusado no Codex e no Copilot, pelo caminho real, pelo atalho e numa sessão fora do hub
- [ ] gravar nas propostas passa; o maestro grava a tabela de roteamento
- [ ] cada peça da família tem nome e descrição válidos

## Comments
