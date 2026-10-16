# 01: Prova: dois CouchDB replicando com o LiveSync

Type: task
Status: resolved
Etapa: 0 (provas de risco)
Blocked by: None (can start immediately)

**What to build:** Dois CouchDB de ensaio, um por par, replicando entre si com os documentos do LiveSync, como o desenho decidido (um banco em cada máquina, replicação de envio em cada um). Usa a forma de configuração que a construção vai usar e termina dizendo o que vai doer ao ligar no resultado final.

**Fonte:** Tickets 30, 33, 34 e 48; bloco do Worker 4 no `spec.md`; brief da etapa em `../etapas/00-provas/brief.md`. Regras comuns: `../etapas/regras-da-construcao.md`.

**Blocked by:** None (can start immediately)

- [ ] nota criada, editada e apagada no par A chega ao B, e vice-versa
- [ ] a mesma linha editada nos dois pares com a replicação pausada vira conflito nos dois bancos, sem versão perdida
- [ ] com a cifra de ponta a ponta e o caminho ofuscado ligados, o mesmo vale e nada aparece em claro nos documentos crus
- [ ] relatório com a evidência e a seção "o que vai doer ao ligar"; contêineres apagados ao fim

## Comments

- 2026-10-16 19:10, Brasa: peguei (Status claimed). Worktree `C:\context-hub-wt\ticket-01`, ramo `ticket-01`, a partir de `integracao` (69cb383). Li spec (Worker 4), faixa 4 da parte 03-04, ticket 48 e o CLI do spike. Achado antes de codar: o sal da cifra (`_local/obsidian_livesync_sync_parameters`) e o milestone são documentos `_local`, que a replicação do CouchDB não copia; o kit precisa gravar o mesmo sal nos dois bancos antes do primeiro dispositivo. Plano: `provas/01-banco/` com `compose.yml`, `04.env` (nomes do spec), `subir.ps1`, `descer.ps1` e `prova.ps1` (teste de ponta a ponta). Falta: tudo.
- 2026-10-16 20:40, Brasa: prova verde com cifra, sem cifra e com o `.ini` em CRLF; a contraprova sem o sal comum falha como esperado. Relatório em `etapas/00-provas/relatorio-banco.md`. Commits 43a4ea9 e 246393b. Pedida a revisão ao Fiel.
- 2026-10-16 20h11 (integrador, Rebite): lição do ticket 05 (parecer do Fiel, rodada 4, `etapas/01-esqueleto/parecer-Trilho.md`): o 05 entrou em `integracao` (0d04985) e moveu `agents/test` para `agents/code/test`. O ramo `ticket-01` ainda chama `agents/test/hub-de-ensaio/montar.mjs` em `provas/01-banco/banco.psm1:49` e na cópia da prova 02; ao juntar `integracao`, usar `agents/code/test/hub-de-ensaio/montar.mjs` e repetir a prova.
- 2026-10-16 20:25, Brasa: juntei `integracao` (0d04985, tickets 02 e 05); o `montar.mjs` agora vem de `agents/code/test` (0c8c639). Prova verde de novo do HEAD. Revisão com o Fiel.
- 2026-10-16 20:40, Brasa: o Fiel deu passa na rodada 1, sem consertos (parecer em `etapas/00-provas/parecer-Brasa.md`; ressalvas para o 07). Passado ao Rebite para juntar.
- 2026-10-16 20h28 (integrador, Rebite): juntado em `integracao`, commit 45ec3b0 (merge `--no-ff` de `ticket-01` 0c8c639, o HEAD da rodada 1 "passa" do Fiel; árvore juntada idêntica à do ramo; nenhuma chamada ao caminho antigo `agents/test/hub-de-ensaio`). Testes: `node --test "agents/code/test/*.test.mjs"` + `instalar.test.mjs` do 03 = 37/37 verdes. As provas 01 e 02 (Docker) e a 03 (`codex exec`) não foram repetidas: árvores idênticas às revisadas (a 01 deu 19 PASSA com o Fiel no 0c8c639). Ressalvas do parecer, levadas ao 07: o "nada em claro" só procura o que a prova escreve; nome `hub-ensaio-00-*` contra `hub-ensaio-04-*` do spec; `banco.psm1` duplicado entre 01 e 02. A leitura do Fielzinho ficou pendente (limite de uso). **Resolvido.**
