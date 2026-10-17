# Relatório do ticket 19: roteamento de skills (Vela)

## Estado

- 2026-10-17: ticket pego; worktree `C:/context-hub-wt/ticket-19` (de `integracao` 0a8e17f; junta d5e4e16 depois).
- Primeiro commit do ramo (d57e36b), pedido do maestro: os testes do 27 apagam as próprias pastas temporárias no fim,
  mesmo falhando (`after` + `rmSync` com novas tentativas, como o Trilho no 04, 05 e 14). Provado com `TEMP` isolado:
  zero pastas sobrando nos dois. Depois, apagadas 25 pastas `%TEMP%\hub-ensaio-*` com mais de 2 horas (21 do `-02-`,
  1 `revisao-04`, 2 `revisao-05`, 1 `revisao-instalador-03`), nenhuma falha; as 937 mais novas ficaram.

## Decisões do maestro (2026-10-17, respostas às perguntas da Vela)

1. A skill do FreeLLMAPI se chama `freellmapi`. O teste usa uma skill de ensaio com esse nome no hub de ensaio (a skill
   de verdade está fora do escopo).
2. `armis-docx` entra na tabela com o nome; o verificador da tabela avisa "skill ausente em agents/skills/" sem recusar.
3. Registro de uso: máquina = `HUB_PAR_ID`; workspace = a pasta da sessão relativa ao hub (fora do hub, o caminho
   absoluto); uma linha de tabela por uso; no Claude Code pelo mod. Codex e Copilot: conferir na doc oficial (curl) se há
   evento de uso de skill; o que não for verificado fica marcado "não verificado".
4. Injeção: Claude Code pelo contexto adicional; Codex pelo `UserPromptSubmit` (testar ao vivo); Copilot pela regra no
   contrato (texto entregue à faixa 1 neste relatório), depois de conferir e citar a doc sobre a saída descartada do
   `userPromptSubmitted`. A extensão `onUserPromptSubmitted` fica anotada como possibilidade para o kit (23).
5. O verificador do fim registra se a skill indicada rodou, sem obrigar, e aponta a linha da tabela: entra no 19, pelo
   hook de fim do 27 (`agents/code/hooks/fim-da-resposta/`), sem bloquear a resposta.
