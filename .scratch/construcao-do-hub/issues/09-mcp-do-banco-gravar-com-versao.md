# 09: MCP do banco: gravar com versão e conflito à vista

Type: task
Status: claimed
Etapa: 3 (MCP do banco)
Blocked by: 07

**What to build:** O fork do MCP do banco grava sempre conferindo a versão lida e mostra o conflito ao agente dos dois jeitos aceitos, contra o banco real da etapa 2.

**Fonte:** Bloco do Worker 5; faixa 5 em `spec-partes/faixas-05-06.md`; tickets 25, 30, 11; escolha aceita 1. Regras comuns: `../etapas/regras-da-construcao.md`.

**Blocked by:** 07 (Banco do par: dois CouchDB, LiveSync e vista `.md`)

- [ ] ler e gravar com a versão lida grava, e a leitura seguinte traz a versão nova
- [ ] gravar com versão velha deixa as duas versões no banco e a resposta diz "conflito: releia e refaça"
- [ ] regravar nota existente sem a versão é recusado
- [ ] a leitura de nota em conflito avisa e lista as versões; a ferramenta de conflitos lista os abertos

## Comments

- 2026-10-17 ~02h50 (maestro): reservado para a Vela; começa quando o 07 for resolvido em `integracao`. Até lá, só leitura (ticket, faixa 5 do spec, relatório do 07).
- 2026-10-17 ~03h00 (Vela): só leitura (ticket, faixa 5, Worker 5, relatório do 07, upstream em C:/Projetos/hub-mcp-banco v0.10.0). Esperando o Gustavo (onde mora o fork) e o 07 em integracao.

- 2026-10-17 ~03h00 (maestro): a Vela perguntou onde mora o fork do es617 (o spec deixou a pergunta aberta). Levado ao Gustavo: rodada `2026-10-17-onde-mora-o-fork-do-mcp` (recomendada A, repositório próprio em `C:\Projetos\hub-mcp-banco`). Respondido pelo maestro: banco de ensaio pelo `ensaio.psm1` do 07 (`hub-ensaio-09-*`, 5996); o fork importa o `lib/frontmatter.mjs` do hub por `HUB_ROOT`, sem segundo validador.

- 2026-10-17 ~03h15 (maestro): o 07 foi resolvido; o 09 segue reservado para a Vela, que começa quando o Gustavo responder sobre o fork (até lá ela faz o 28).

- 2026-10-17 ~04h15 (maestro): troca de dono: o Gustavo subiu o limite para 4 construtores; o **Cinzel** (novo) faz o 09 agora, para o caminho crítico (10, 11, 16, 22) andar. A Vela, que leu o 09 e fez as perguntas, segue no 28 e responde ao Cinzel o que ele precisar. Decisões já tomadas aqui: fork em `C:\Projetos\hub-mcp-banco` (Gustavo, A); banco de ensaio pelo `ensaio.psm1` (`hub-ensaio-09-*`, 5996); o fork importa o `lib/frontmatter.mjs` do hub por `HUB_ROOT`.

- 2026-10-17 ~03h25 (Cinzel): peguei o 09 (`claimed`). Fork: `C:/Projetos/hub-mcp-banco`, ramo `ticket-09` (de v0.10.0; o `package-lock.json` só perde o `jose` opcional, vai ao relatório). Hub: worktree `C:/context-hub-wt/ticket-09` de `integracao` 763813a.
  - Achado: a biblioteca do LiveSync já tem o gancho. `putDBEntry(nota, false, base)` (modo `force-base`) grava a nota como filha da base por `put(..., {force: true})`, que no PouchDB vira `_bulk_docs` com `new_edits=false` e `_revisions` (o caminho do `r1.py`). Os pedaços passam pela própria biblioteca, então saem cifrados com a E2EE. A leitura (`getDBEntry` com `{conflicts: true}`) já traz `_rev` e `_conflicts`. `putDBEntryAsIndependentRoot` serve para criar nota nova sem pisar numa criação simultânea.
  - Costuras propostas ao maestro: (A) e2e do fork contra um CouchDB de ensaio na 5996; (B) teste de ponta a ponta no hub, com o par do 07 (`ensaio.psm1`, `hub-ensaio-09-*`) e o passo `agents/code/kit/par/05-mcp-banco.ps1`, na 8796. Esperando o aval.
- 2026-10-17 ~04h35 (maestro, decidido pelo mandato de 2026-10-17): costuras A (e2e do fork, CouchDB só do fork em 5996, sem cifra) e B (par do 07 com cifra, passo `05-mcp-banco.ps1`, só a instância de escrita 8796) aceitas. Pontos abertos da faixa 5: (a) `edit_note` replace exige `base_rev`; append/prepend com `base_rev` opcional e, sem ela, gravam como filha da versão lida na mesma chamada (nunca por cima às cegas); (b) nota nova sem `base_rev` aceita como raiz; criação simultânea vira conflito; (c) `move_note` recusa destino existente; `delete_note` também exige `base_rev` e, com base velha, vira conflito como a gravação (mesmo caminho do force-base) — se a biblioteca não der isso barato, recusa apagar nota em conflito, registra no relatório e o resto vira ticket seguinte, sem segurar o 09; (d) modo local do upstream com hash do texto como versão; (e) `read_note` com `rev` opcional.
- 2026-10-17 ~03h47 (Cinzel): fork, ramo `ticket-09` (sem commit ainda; esperando a trava para o e2e com Docker):
  - `read_note` devolve `base_rev:` e, em conflito, `CONFLITO` com as versões; `read_note(path, rev)` lê cada uma; `get_conflicts` novo.
  - `write_note`: com base grava como filha (force-base); base velha = "conflito: releia e refaça", as duas folhas ficam; sem base em nota existente ou base inventada = `Recusado:`; nota nova = raiz independente.
  - `edit_note`: replace exige base; append/prepend sem base gravam como filha da versão lida. `delete_note`: exige base, pelo `storeDeletionAtRevision` da lib (apaga como filha da base; base velha = conflito; a leitura mostra a versão viva). `move_note`: exige base da origem, recusa destino existente.
  - Modo local do upstream: versão = hash do texto; base velha recusada com "conflito: releia e refaça".
  - Testes: `test/versao.e2e.test.ts` (costura A, 13 casos, roda por `npm run test:e2e:banco`, que sobe `hub-ensaio-09-f` na 5996 e o apaga). Unitários 272/1 e e2e local 36/7: as falhas são as mesmas da base do upstream no Windows (separador `\`), medidas antes da mudança (`.local/base-unit-2.log`, `.local/e2e-local-base.log` no fork).
  - Próximo: rodar a costura A com a trava (primeiro sem a mudança, para o vermelho), commit; depois a costura B (passo `05-mcp-banco.ps1` e o teste do hub).
- 2026-10-17 ~04h00 (Cinzel): commits. Fork 289ec4c (ramo `ticket-09`: o `package-lock.json` fica fora, é o efeito do `npm install`). Hub ce9790b: o passo `agents/code/kit/par/05-mcp-banco.ps1` com o módulo `mcp-banco/`, o modelo `env/05.env.modelo`, o teste com Docker `agents/code/test/09-mcp-banco.test.ps1` (costura B) e o sem Docker `09-mcp-banco-sem-docker.test.mjs`, que deu 9 PASSA.
  - Mudança de desenho, que vai ao relatório: só é conflito quando a base não é mais uma versão viva, ou seja, quando a gravação abriu um ramo novo. Gravar sobre a versão viva de uma nota já em conflito grava e avisa que o conflito segue aberto. Sem isso, o "reler e regravar" do aceite responderia conflito para sempre.
  - Sou o 2º na fila (`etapas/fila-pesada.md`), depois do Rebite. Na vez: (1) vermelho, com `git checkout 1a4d53f -- src` no fork e `npm run test:e2e:banco`; (2) `git checkout HEAD -- src` e de novo, para o verde; (3) `pwsh -NoProfile -File agents/code/test/09-mcp-banco.test.ps1` na worktree, com log em `etapas/logs/09-docker-1.log`.
- 2026-10-17 ~04h45 (Cinzel): verde e pronto para revisão. Relatório: `etapas/relatorio-09-mcp-do-banco.md`.
  - Fork `ticket-09` em 61a6e70: costura A 12/12, vermelho medido antes; unitários 272/1 e e2e local 36/7, iguais à base do upstream.
  - Hub `ticket-09` em 3d9d0bb, com `integracao` 33b817a juntada: costura B 21 PASSA (`etapas/logs/09-docker-4.log`); sem Docker 12 PASSA.
  - Achados no caminho: o sincronizador do LiveSync funde sozinho conflitos de linhas diferentes (caso 4b, nada se perde); o passo 05 rodava um `dist` velho, e agora remonta quando um fonte é mais novo. Trava solta às 04:37; Rebite avisado.
