# 05: Frontmatter imposto: esquemas, verificador e "nova iniciativa"

Type: task
Status: claimed
Etapa: 1 (esqueleto)
Blocked by: 04

**What to build:** Os esquemas de frontmatter por tipo, o verificador sem IA e o script "nova iniciativa". O verificador só completa campos que se deduzem, trocando um trecho e relendo o arquivo logo antes de gravar. O campo de iniciativa só é exigido onde o caminho mostra uma iniciativa. O script não cria o `AGENTS.md` da iniciativa (ele nasce à mão).

**Fonte:** Bloco do Worker 1; faixa 1; ticket 12; escolhas aceitas 14, 19 e 20 (`../revisao/escolhas-decididas.md`). Regras comuns: `../etapas/regras-da-construcao.md`.

**Blocked by:** 04 (Esqueleto do hub e hub de ensaio)

- [ ] o verificador aceita a nota certa e recusa a sem `status` ou com `stage` fora do ciclo
- [ ] ele completa os campos dedutíveis sem apagar uma edição feita entre a leitura e a gravação
- [ ] o script cria uma iniciativa de ensaio com o núcleo de seis arquivos válidos; rodar de novo não duplica nem sobrescreve

## Comments

- 2026-10-16 ~21h10 (Trilho): ticket pego, `Status: claimed`. Worktree `C:\context-hub-wt\ticket-05`, ramo `ticket-05`,
  a partir de `integracao` (b68f540). Costuras: (1) `node agents/bin/verificar-frontmatter.mjs` (sobre arquivos ou
  pastas, com `--corrigir` para completar o dedutível, e `--checar <caminho>` com o conteúdo na entrada, para o hook do
  14 e o MCP); (2) `node agents/skills/nova-iniciativa/nova-iniciativa.mjs`; (3) o `verificar-hub`, que passa a
  conferir o frontmatter do hub inteiro. Perguntas ao maestro: escopo (index.md, links, other/, fim de resposta),
  tabela stage → status, caminho sem tipo, operations/. Falta: tudo.
- 2026-10-16 ~21h30 (maestro): o Gustavo respondeu as três perguntas do Trilho (rodada `2026-10-16-ticket-05-perguntas-do-trilho`, todas A): as tarefas (e) a (h) do verificador ficam fora do 05, no ticket 27 novo (depois do 05 e do 06); a tabela `stage` → `status` do Trilho vale como está; `operations/<operação>/` não conta como iniciativa. O caminho sem tipo no catálogo (só campos comuns e aviso, sem recusa) foi aceito pelo maestro. Código em `agents/code/` e a "nova iniciativa" em `agents/skills/nova-iniciativa/` (rodada `onde-mora-o-codigo-do-hub-r2`).
- 2026-10-16 ~22h40 (Trilho): pronto no ramo `ticket-05` (HEAD b7c99c8, com `integracao` 3857c98 juntada), 28 testes
  verdes (`node --test "agents/code/test/*.test.mjs"`). Os três critérios cobertos por teste. Código em `agents/code/`
  e a skill em `agents/skills/nova-iniciativa/` (opção C). As quatro tarefas a mais do verificador foram para o ticket
  27. Detalhes no relatório da etapa 1. Falta: revisão do Fiel.
- 2026-10-16 ~23h10 (Trilho): revisão 1 do Fiel: volta, dois consertos (YAML preservado ao corrigir e cabeçalho sem
  fechamento recusado; caminho com ponto de fora também direto e no `--checar`). Feito no commit 71d12c1, 32 testes
  verdes. Falta: revisão 2.
- 2026-10-16 ~23h40 (Trilho): revisão 2 (em dupla): volta, dois consertos (comentário YAML preservado; ficha arquivada
  na nota arquivada) e um ajuste de texto. Feito no commit 817f850, 34 testes verdes. Falta: revisão 3.
- 2026-10-16 ~23h55 (Trilho): revisão 3 (Fiel e Fielzinho): passa, HEAD 817f850, 34 testes verdes. Ressalva: as provas
  01 e 02 chamam `agents/test/hub-de-ensaio/montar.mjs`; na junção, trocar por `agents/code/test/` e repetir. Rebite
  avisado. Falta: junção (Rebite).
- 2026-10-16 20h00 (integrador, Rebite): lição do ticket 02 (parecer do Fiel, `etapas/00-provas/parecer-Vela.md`): a prova 02 chama `agents/test/hub-de-ensaio/montar.mjs` em `agents/code/test/provas/02-pastas-com-ponto/banco.psm1` (cópia do módulo da prova 01). Se este ticket move o montador para `agents/code/test/`, a chamada precisa mudar e a prova 02 ser repetida; não copiar a versão antiga para contornar.
