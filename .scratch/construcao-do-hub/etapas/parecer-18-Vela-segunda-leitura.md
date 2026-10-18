# Parecer 18 (Vela), segunda leitura independente: PASSA

Ponta 4f0b09e, worktree C:/context-hub-wt/ticket-18.

1. Diff 8cdd2b2..4f0b09e: só dois testes. 18-retomada.test.mjs:126-127 e :143 trocam o modelo por `o-do-usuario`; ponta-a-ponta/18-retomada.test.mjs:20 importa MODELO_CODEX e :136 o usa no `-m`. `grep gpt-[0-9]` no teste leve: vazio. harness-real.mjs:9 define MODELO_CODEX (gpt-6-luna).
2. `git diff integracao 4f0b09e -- AGENTS.md`: só acréscimos (bullet "Retomada" na cabeça e a seção "## Retomada"); "Roteamento de skills" intacta, nada da integracao perdido. conferir-cabeca: 1869 de 2000.
3. Evidência do Codex: registro.jsonl tem marca, fim com devolveu:true (falta: atualizar a retomada.md), fim com soltou "sem falta". sessao-2-resposta.txt = "Pedir ao setor ZEBRA-42 ..."; hashes-codex.json antes = depois nos 8 arquivos; pasta de ensaio apagado:true; sem ghu_/gho_/sk-/refresh_token/access_token. Bate com o relatório.
4. Testes (5 arquivos): 50 testes, 49 passam, 0 falham, 1 pulado (a prova real, por falta de HUB_HARNESS_REAL; esperado). git status --short limpo.

Ressalva menor, sem bloquear: a evidência do Codex foi gravada antes do conserto do nome do modelo; o comportamento é o mesmo (MODELO_CODEX = gpt-6-luna).
