# 10: MCP do banco: três instâncias, cabeça, regra curta e estado

Type: task
Status: resolved
Etapa: 3 (MCP do banco)
Blocked by: 09, 05

**What to build:** O MCP do banco completo: três instâncias por máquina (leitura; escrita dos agentes da máquina; escrita só do cliente), a cabeça do `AGENTS.md` relida a cada conexão e posta antes do texto do upstream, a regra curta nas ferramentas de gravação, a cifra de ponta a ponta, a ferramenta `estado_do_hub` com um estado de exemplo no esquema da vigia, e a recusa de nota fora do esquema pelo verificador.

**Fonte:** Bloco do Worker 5; faixa 5; escolhas aceitas 2, 3, 4 e 21; decisão do Gustavo de três instâncias (escolha 5). Regras comuns: `../etapas/regras-da-construcao.md`.

**Blocked by:** 09 (MCP do banco: gravar com versão e conflito à vista), 05 (Frontmatter imposto: esquemas, verificador e "nova iniciativa")

- [ ] a instância de leitura não lista ferramenta de gravação e recusa gravar; as duas de escrita gravam com a guarda de versão, cada uma com o seu token
- [ ] a conexão traz a cabeça do `AGENTS.md` de ensaio e, trocado o arquivo, a sessão nova traz a cabeça nova
- [ ] as descrições das ferramentas trazem a regra curta como aceita
- [ ] os testes de versão passam de novo com a cifra ligada
- [ ] `estado_do_hub` devolve o estado de exemplo e, sem arquivo, "estado indisponível"
- [ ] nota fora do esquema é recusada

## Comments

- 04:42 (maestro): reservado para o Cinzel (continua no fork). Costuras já; código depois do "passa" do 09, num ramo ticket-10 do fork a partir do ticket-09 (e no hub a partir de ticket-09 ou de integracao com o 09 juntado).

- 04:45 (maestro, mandato): costuras A e B do Cinzel aceitas; decisões (a) portas 8796 escrita do par, 8797 leitura, 8798 escrita do cliente, com URL/TOKEN de cada uma no `.env`; (b) regra curta completa nas 4 ferramentas de gravação (delete e move levam base_rev desde o 09); (c) cabeça ausente ou acima de 2.000: texto do upstream mais a linha "cabeça do AGENTS.md indisponível: <motivo>", nunca cabeça cortada; (d) validação também para nota nova, tipo pelo caminho; (e) estado.json ilegível: "estado indisponível: <motivo>". O caminho e o esquema do `estado.json` combinam com o 16 (Trilho, `agents/skills/vigia/`).

- 2026-10-17 ~04h55 (Cinzel): combinado com o Trilho (16, ramo ticket-16 60756e6, `agents/skills/vigia/SKILL.md`): caminho `<hub>/.local/vigia/estado.json`. Topo: `nivel`, `resumo`, `passada` (ISO; ausente se só outros donos gravaram), `outro_par {situacao, motivo?}` e `vistos` (interno da vigia: o `estado_do_hub` o tira). `itens[]`: `id`, `nivel`, `resumo`, às vezes `fonte`, `caminho`, `parada_desde`, `ultima_troca`. Sem arquivo ou ilegível: "estado indisponível". Estado velho: perguntado ao maestro (sugestão do Trilho: aviso "a vigia não roda desde <hora>" se `passada` > 15 min). Código só depois do "passa" do 09.

- 04:46 (maestro, mandato): estado velho aceito como proposto (Trilho e Cinzel): não vira "indisponível"; passada com mais de 15 min leva o aviso "a vigia não roda desde <hora>"; sem o campo `passada`, sem aviso de idade. O campo `vistos` (interno da vigia) não sai no `estado_do_hub`.

- 2026-10-17 ~05h25 (Cinzel): peguei o 10 (`claimed`). Fork: worktree `C:/Projetos/hub-mcp-banco-wt/ticket-10`, ramo `ticket-10` de `ticket-09` d2a5a40 (o fork principal fica em `ticket-09`). Hub: worktree `C:/context-hub-wt/ticket-10` de `integracao` 9453e3e (com o 09 juntado).
  - Combinado com a Vela (17, reserva da checagem de início): cliente por `HUB_MCP_BANCO_LEITURA_URL/TOKEN`, `Authorization: Bearer`. `estado_do_hub`: `content[0]` text = o JSON do `estado.json` sem `vistos`, ou "estado indisponível: <motivo>"; com `passada` de mais de 15 min, um `content[1]` text "a vigia não roda desde <hora>". Transporte: streamable HTTP do FastMCP, resposta em SSE, `initialize` antes e o `mcp-session-id` nos pedidos seguintes.

- 2026-10-17 ~06h00 (Cinzel): fork `ticket-10` 58c8504: cabeça relida a cada sessão (getter no `instructions`), cabeça indisponível dita, regra curta nas 4, `estado_do_hub`, frontmatter pelo verificador do hub (write, edit e move), instância de leitura; `test/hub.e2e.test.ts` 10/10 sem Docker. Hub `ticket-10` f7a8358: passo 05 com as três instâncias (`HUB_ROOT`, `READ_ONLY`, porta e token próprios), sem Docker verde. Falta a costura B com Docker (`10-mcp-banco.test.ps1`) e o relatório. Retomada salva.

- 2026-10-17 ~06h20 (Cinzel): pronto para revisão. Fork `ticket-10` 58c8504 (de `ticket-09` d2a5a40; worktree `C:/Projetos/hub-mcp-banco-wt/ticket-10`). Hub `ticket-10` 6095213 (de `integracao` 9453e3e, a ponta atual). Testes: Docker do 10 com a cifra, 32 PASSA (`etapas/logs/10-docker-3.log`; a 1ª rodada teve 4 falhas do teste, consertadas); o 09 de novo com as três instâncias, 21 PASSA (`10-docker-2.log`); sem Docker 1/1 (18 casos); fork `test/hub.e2e.test.ts` 10/10; upstream 272/1 e 36/7, iguais à base. Relatório `etapas/relatorio-10-mcp-do-banco.md`. Revisão pedida ao Fiel.
- 2026-10-17 ~06h55 (Cinzel): rodada 1 VOLTA (parecer-10-Cinzel.md, 1 conserto: gravar o texto completado pelo verificador). Fork `ticket-10` 1e86ad1: write, edit e move gravam o `novoTexto` e dizem "Completado pelo esquema: ..."; e2e do fork 14/14 (4 casos novos, vermelho antes). Hub `ticket-10` a40ec84: testes Docker com o updated de hoje; caso de inbox completada no 10. Rodada 2 pedida ao Fiel (Docker com ele).
- 2026-10-17 ~06h45 (Cinzel): rodada 2 PASSA (Fiel; parecer-10-Cinzel.md, fim). Docker do Fiel: 10 33 PASSA, 09 21 PASSA. Levado ao Rebite. Correção: a minha rodada de 06h12 deu 32 PASSA (não 34).
- 2026-10-17 07h30 (integrador, Rebite): juntado nos dois repositórios: hub `integracao` 9cc878b (merge `--no-ff` de `ticket-10` 4cf4656; depois do parecer, em a40ec84, só entrou a junção de `integracao`) e fork `integracao` 34c3e50 (merge `--no-ff` de `ticket-10` 1e86ad1, o HEAD do parecer). As duas árvores juntadas são idênticas às dos ramos. Testes: suíte do hub com a trava, junto com o 36: `node --test --test-concurrency=1 "agents/code/test/**/*.test.mjs"` = 210, 202 verdes, 8 pulados, 0 falhas. Unitários do fork (`node --import tsx --test "src/**/*.test.ts"`, com `TEMP`/`TMP` no caminho longo `C:\Users\gustavo.delfino\AppData\Local\Temp`) = 273, 272 passam, 1 falha, a mesma da base (`vault-local.test.ts`, "lists all .md files recursively", separador `\` do Windows); log `etapas/juncao-10-fork-unitarios.log`. Com o TEMP no nome curto (`GUSTAV~1.DEL`) caem 20 testes de caminho (log `etapas/juncao-10-fork-unitarios-temp-curto.log`). O `npm test` do fork roda 0 testes no Windows (aspas simples no script). O Docker (10: 33 PASSA; 09 com o fork do 10: 21 PASSA) e o e2e do hub (14/14) não foram repetidos: o Fiel os rodou nas mesmas pontas. Worktree do fork com junções para `node_modules` e `lib/livesync-commonlib` da cópia principal. A leitura do Fielzinho ficou pendente. **Resolvido.**
