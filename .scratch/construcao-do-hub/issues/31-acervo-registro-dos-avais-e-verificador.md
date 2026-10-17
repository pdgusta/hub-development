# 31: Acervo: registro dos avais, verificador escolhido pelo maestro e peça que sumiu

Type: task
Status: ready-for-agent
Etapa: 8 (skills e acervo)
Blocked by: 20

**What to build:** As três lacunas de dono que o Gustavo decidiu depois de o ticket 20 entrar. (1) **Registro do aval:** quando o Gustavo aprova uma mudança no acervo, a guarda grava `agents/maestro/avais/AAAA-MM-DD--<peça>.md` com o antes e depois, quem é afetado, o relatório do verificador, o modelo que o verificou e a decisão; a pasta replica e fica fora da guarda do acervo, mas só a guarda escreve ali (outra gravação nela é recusada). (2) **Modelo do verificador:** o maestro escolhe a cada pedido de aval, desde que seja um modelo diferente do dele, e o pedido de aval diz qual usou; sai o verificador provisório fixo em Sonnet do 20, e a guarda recusa o relatório de um verificador no mesmo modelo do maestro. (3) **Peça que sumiu:** a conferência de forma do acervo, quando um catálogo cita uma peça que não existe, grava um item no `.local/vigia/estado.json` (troca atômica, sem apagar os outros itens, o topo fica o pior, como o fim da resposta do 27); a vigia (ticket 16) o mostra.

**Fonte:** Decisão do Gustavo na rodada `2026-10-16-acervo-do-maestro-tres-lacunas` (1 A, 2 B, 3 A); spec faixa 9 (`spec-partes/faixas-09-10.md`, pontos abertos já marcados como decididos); relatório do 20 (`../etapas/relatorio-20-acervo-do-maestro.md`). Regras comuns: `../etapas/regras-da-construcao.md`.

**Blocked by:** 20 (Acervo do maestro e a guarda dele)

- [ ] com um aval aprovado, nasce o arquivo em `agents/maestro/avais/` com o antes e depois, os afetados, o relatório, o modelo e a decisão; uma gravação de agente nessa pasta é recusada
- [ ] um relatório de verificador no mesmo modelo do maestro é recusado; num modelo diferente, o pedido de aval mostra qual
- [ ] um catálogo que cita uma peça inexistente gera o item na vigia, sem apagar os outros itens

## Comments

- 2026-10-17 ~00h25 (maestro): publicado pela decisão do Gustavo. Dono natural: a Vela, que fez o 20.
