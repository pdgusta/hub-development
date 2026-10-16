# 14: Guardas: regravação inteira e ficha fora do esquema

Type: task
Status: ready-for-agent
Etapa: 5 (guardas no disco)
Blocked by: 05, 03

**What to build:** O hook antes da ferramenta nos três harnesses: recusa regravar inteiro um arquivo que já existe no hub (com a mensagem que aponta a troca de trecho ou o MCP do banco), deixa passar troca de trecho e arquivo novo, e recusa a nota que ficaria fora do esquema, montando o conteúdo final antes de chamar o verificador. Sai na hora fora do hub.

**Fonte:** Bloco do Worker 6; faixa 6 em `spec-partes/faixas-05-06.md`; tickets 11, 14 e 12; escolha aceita 15. Regras comuns: `../etapas/regras-da-construcao.md`.

**Blocked by:** 05 (Frontmatter imposto: esquemas, verificador e "nova iniciativa"), 03 (Prova: hooks do Codex em acesso total)

- [ ] os casos gravados na bancada passam nos três adaptadores
- [ ] regravar existente é recusado; troca de trecho e arquivo novo passam
- [ ] nota que ficaria sem `status` é recusada
- [ ] fora do hub, o hook não faz nada

## Comments
- 2026-10-16 ~20h20 (maestro): passado ao Trilho, como antecipação da etapa 5 (bloqueios 05 e 03 resolvidos; plano: até 3 agentes, sem depender de peça que não existe). Primeiro commit do ramo, separado: tirar o `README.md` da raiz do hub (decisão do ticket 12: raiz = `AGENTS.md` + seis raízes; era marcador do "Início do hub"), a pedido do maestro pela ressalva do Rebite na junção do 05.
