# 34: Roteamento: uma linha de registro por skill e caminho com barra do Windows

Type: task
Status: resolved
Etapa: conserto do 19 (fora da sequência)
Blocked by: 19

**What to build:** Dois consertos no roteamento de skills (ticket 19, já em `integracao`), achados na leitura tardia do
Fielzinho e aceitos pelo Fiel. (1) `fecharTurno` em `registro.mjs` junta numa linha só as skills de uma linha de papel
e registra só as que rodaram; as indicadas e não usadas somem, e a medição do 15 (ajustar a tabela pelo registro) fica
cega a elas. Passa a escrever uma linha de indicação por skill, com o "rodou" de cada uma. (2) `caminhosDoPedido`
filtra antes de trocar `\` por `/`, então `research\dados.json` não casa o gatilho `caminho` e `research/dados.json`
casa. Normalizar as barras antes do filtro.

**Fonte:** `../etapas/parecer-19-Vela.md` (seção "Leitura do Fielzinho") e `../etapas/parecer-19-Vela-fielzinho.md`.
Regras comuns: `../etapas/regras-da-construcao.md`. Número 33 reservado para a rodada das sobras do link fora do hub.

**Blocked by:** 19 (Roteamento de skills)

- [ ] linha de papel com duas skills, uma usada e outra não: o registro do turno tem uma linha por skill, a usada com
      "rodou" sim e a outra com não
- [ ] pedido que cita `research\dados.json` recebe a mesma indicação que `research/dados.json`
- [ ] a suíte segue verde

## Comments

- 2026-10-17 ~02h15 (maestro): publicado pela proposta do Fiel e da Vela (leitura tardia do 19), como o 30. Dona: a
  Vela, depois que o 31 fechar.
- 2026-10-17 02h24 (Vela): claimed; worktree C:/context-hub-wt/ticket-34 da ponta de integracao.
- 2026-10-17 02h32 (Vela): consertos em cd52173 (barras) e 0e39c35 (uma linha por skill); 19-roteamento 19/19. Falta: suíte inteira (trava com o Fiel), revisão, Rebite. Relatório etapas/relatorio-34-roteamento-registro-por-skill-e-barras.md.
- 2026-10-17 02h41 (Vela): suíte 185/0/8 em 0e39c35; revisão pedida ao Fiel.
- 2026-10-17 02h44 (Vela): Fiel rodada 1 PASSA (com o Fielzinho); passa levado ao Rebite.
- 2026-10-17 03h00 (integrador, Rebite): juntado em `integracao`, commit 763813a (merge `--no-ff` de `ticket-34` 0e39c35, o HEAD da rodada 1 "passa" de Fiel e Fielzinho; junto com o 07, sem arquivo em comum). Testes, com a trava: `node --test --test-concurrency=1 "agents/code/test/**/*.test.mjs"` sem variáveis = 194, 186 verdes, 8 pulados, 0 falhas; `git status` limpo. Ponta a ponta real não precisa (parecer: lógica interna, formato dos eventos não mudou). **Resolvido.**
