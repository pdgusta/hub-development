# 31: Acervo: registro dos avais, verificador escolhido pelo maestro e peça que sumiu

Type: task
Status: resolved
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
- 2026-10-17 01h15 (Vela): commits 9cb5ac6 (modelo do verificador), 53c3ac7 (avais), 565c87e (peça sumida na vigia), 68deed6, cc8c852. 20-acervo 18/18. Relatório etapas/relatorio-31-acervo-avais-e-verificador.md. Falta: suíte e ponta a ponta do Claude (trava pesada), Fiel, Rebite.
- 2026-10-17 01h28 (Vela): rodada 2 do Fiel PASSA (etapas/parecer-31-Vela.md); passa levado ao Rebite; suíte inteira não rodada por mim (trava pesada ocupada).
- 2026-10-17 01h35 (maestro): a ponta a ponta do Claude com HUB_HARNESS_REAL=1 fica com a Vela (o ticket mexe em hooks; regra do construtor e aval de login), na mesma janela de trava da prova do Codex do 20, no ramo ticket-31. Resultado no relatório; o Fiel confere numa rodada curta de evidência. O Rebite mantém a junção (357a2ba) e só resolve o 31 com a suíte comum verde e essa ponta a ponta verde; o 32 resolve com a suíte.
- 2026-10-17 01h50 (integrador, Rebite): juntado em `integracao`, commit 357a2ba (merge `--no-ff` de `ticket-31` b710f2d, o HEAD da rodada 2 "passa" do Fiel). Suíte inteira com a trava em 57e85cf (31 + 32): `node --test --test-concurrency=1 "agents/code/test/**/*.test.mjs"` = 186, 178 verdes, 8 pulados, 0 falhas; `git status` limpo. **Não resolvido** por ordem do maestro: espera a ponta a ponta do Claude (`HUB_HARNESS_REAL=1`, Vela, no ramo `ticket-31`) e a conferência da evidência pelo Fiel.
- 2026-10-17 02h12 (Vela): ponta a ponta real achou buraco do CRLF (consertado em 050fb14); 2ª rodada verde em Claude e Codex; evidência commitada. Rodada nova de código pedida ao Fiel.
- 2026-10-17 02h20 (Vela): rodada 3 do Fiel PASSA com ressalva (asks de nome parecido e da tabela sem registro em avais/); passa levado ao Rebite; ressalva ao maestro.
- 2026-10-17 02h51 (integrador, Rebite): rodada 3 juntada em `integracao`, commit e82ce65 (merge `--no-ff` de `ticket-31` 4e420a6, o HEAD da rodada 3 "passa com ressalva escrita" de Fiel e Fielzinho: conserto do CRLF no `trocar` da guarda e evidência real do Claude, 31, e do Codex, 20). Testes, com a trava: `node --test --test-concurrency=1 "agents/code/test/**/*.test.mjs"` sem variáveis = 191, 183 verdes, 8 pulados, 0 falhas (10 min); `git status` limpo. Harness real não repetido: a Vela rodou a ponta a ponta no Claude e no Codex em 4e420a6, e os arquivos de hooks e ponta a ponta juntados são idênticos aos do ramo. **Ressalva com conserto para um ticket seguinte** (Fielzinho, aceita pelo Fiel): aval sem parecer não é registrado; o `ask` de nome parecido (`redator-2.md`) e o da tabela sem `HUB_PAPEL` não criam pendência nem parecer, e o `aval.mjs` só registra quando os dois existem. Conserto: pendência para cada `ask` e registro do aval mesmo sem parecer ("sem verificador: dispensado"). Levado ao maestro para virar ticket. **Resolvido.**
- 2026-10-17 02h55 (integrador, Rebite): a ressalva "aval sem parecer não é registrado" virou o ticket 35 (Trilho, `35-aval-sem-parecer-tambem-registrado.md`).
