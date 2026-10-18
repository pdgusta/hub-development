# Parecer do ticket 25 (Vela): junção e prova do hub de ensaio inteiro

## Rodada 1, revisão PARCIAL — 2026-10-17 ~19h (Fiel; 2ª leitura por subagente Opus)

Ramo `ticket-25`, ponta **5489b3a** (contém `integracao` f640bbd). Escopo pedido pelo maestro: fases 1-3, 5, 6 e 7
com Claude e Copilot; Codex nas fases 1 e 3. Fora: fase 4 e fase 2 do Codex (descida A→B, rodada curta depois).

**Veredito: VOLTA, em acordo com a 2ª leitura** (`parecer-25-Vela-segunda-leitura.md`). 2 consertos.

### Consertos

1. **A fase 7 passou sem rodar nenhum harness** (Fiel). `25-hub-inteiro.test.mjs:493` abre o
   `node --test 22-cliente.test.mjs` com `env: { ...process.env, ... }`. O `NODE_TEST_CONTEXT` do executor de fora vai
   junto, e o node de dentro não roda nada e sai 0.
   - Evidência: `evidencia-25/cliente/harnesses/prova.tap` vazio (0 bytes); `erros.txt`: "node:test run() is being
     called recursively within a test file. skipping running files."; `etapas/logs/25-noite-f7-resumo.md`: só as fases
     `cliente:subir` (6:32) e `descer`, sem `cliente` (a fase durou 394,7 s, e a subida 6:32: o 22-cliente levou ~2 s);
     `25-noite-f7-hashes-claude-copilot.json`: `usos: []` (nenhum login copiado).
   - Reprodução do Fiel (sonda em `%TEMP%`, apagada): um teste que abre `node --test filho.test.mjs` com
     `{ ...process.env }` dá status 0, TAP vazio e o mesmo aviso; sem o `NODE_TEST_CONTEXT`, roda (`# pass 1`).
   - O padrão certo já está no repositório: `36-pasta-de-ensaio.test.mjs:26` e `harness-real.test.mjs:76`
     (`delete env.NODE_TEST_CONTEXT`).
   - Conserto: tirar o `NODE_TEST_CONTEXT` do ambiente do filho; e a fase conferir no TAP que rodou (`# pass` igual ao
     número de harnesses, `# skipped 0`), para que um filho que não roda nunca dê verde. Teste sem Docker antes (o filho
     com um dublê de `22-cliente` que só passa). Depois, a fase 7 de verdade de novo (com a trava), evidência nova e o
     relatório corrigido (hoje diz "verde (18:15; cee35c1)").
   - Cuidado ao rodar (Fiel e 2ª leitura): o 22-cliente de dentro apaga e grava `evidencia-22/<harness>/` e
     `hashes-*.json` (`22-cliente.test.mjs:25,43,182`), e a evidência do Codex do 22 acabou de entrar na `integracao`.
     O ramo do 25 não pode levar o `evidencia-22` mudado. Se, para isso, for preciso mexer no `22-cliente.test.mjs`
     (arquivo do 22), combine com o maestro antes.
   - Corrigir também o comentário de 18:24 no ticket ("fase 7 verde").

2. **A evidência versionada não sustenta mais o que o relatório cita** (2ª leitura; o Fiel tinha como ressalva, aceito
   como conserto). O commit f5b790b levou `hashes-claude-copilot.json`, `medida.csv` e `resumo.md` da rodada das 18:13
   (1 amostra, `usos: []`). O relatório cita esses arquivos como prova do pico das fases 1-3 e das horas de login, que
   não estão mais na árvore. Causa: nomes fixos a cada rodada (`25-hub-inteiro.test.mjs:506-511`; e a linha 65 apaga a
   fase inteira mesmo numa rodada de um harness só).
   - Conserto: nomear por rodada (ou uma pasta por rodada); repor a evidência da manhã (cópias em
     `etapas/logs/25-medida-fases-1-3.csv`, `25-hashes-fases-1-3.json`, `25-resumo-fases-1-3-claude-copilot.md`);
     versionar os hashes e `usos` do Codex das 18:00 (`etapas/logs/25-codex-luna/hashes-codex.json`).

### Ressalvas (não seguram; entram no relatório)

- A rodada com o `gpt-6.1-sol` (18:08) não deixou `hashes-codex.json` na cópia do log. O registro de login das fases 5
  e 6 se perdeu (deslize relatado); as credenciais saíram iguais em todas as rodadas conferidas.
- "Codex fase 3 verde" não diz nada do Codex: a fase 3 não abre harness (2ª leitura). Tirar da tabela.
- O modelo do Codex não aparece na evidência; gravar `MODELO_CODEX` nos `usos` (2ª leitura).
- Na fase 2, o B é conferido só no `tasks.md` (o `decisions.md` não) (2ª leitura).
- `cliente.ps1` não apaga o seu log em `%TEMP%` (2ª leitura).
- **Pilha registrada sem escrita atômica:** `registrarPilha` grava o JSON direto, e o medidor descarta em silêncio
  (`catch { }`, `medidor.ps1` Get-Pilhas) um JSON lido pela metade. Num corte nessa hora, a pilha não desceria. Gravar
  em `.novo` e renomear.
- **25-medidor intermitente:** o teste "no corte, desce cada pilha registrada…" falhou 1 vez em 4 rodando junto com os
  outros leves (sozinho: 3/3; 4 em paralelo, duas vezes: 8/8). Laço de mais 6 rodadas: 6/6 verdes; 2ª leitura 41/0. Não reproduzi de novo; fica como ressalva.

### O que confere

- Ramo contém `integracao` f640bbd. Leves (`harness-real`, `25-*`, `ponta-a-ponta/25-hub-inteiro`, `27-pastas`):
  41/0/1 em 3 de 4 rodadas (a 4ª, a falha do medidor acima). `git status` limpo.
- Codex pela constante: `harnesses.mjs:59` usa `MODELO_CODEX`; nenhuma `HUB_MODELO_CODEX` no corredor. O Sol (18:08)
  foi tentado e explicado no relatório (o defeito era do pedido).
- Fase 1: os três acham `inbox/viveiro-na-cobertura.md` (respostas; Claude `claude-haiku-5-5`).
- Fase 2 (Claude, Copilot): `guarda.jsonl` com `recusa` da regravação inteira de `decisions.md`, depois `passa` nas
  trocas; `recebeu` com hash do A = hash do B; `em-claro.json` 189 amostras, nada em claro.
- Fase 3: `recebeu` com hashes iguais depois do reinício.
- Fase 5: a sessão 2 dos dois responde o próximo passo com `ZEBRA-25` (só a nota trazia); registro do fim com devolução.
- Fase 6: os dois arquivam em `operations/_archive/2026-10-17--encerrada-<h>`; cópia diária código 0, ramo
  `par/ensaio-a`.
- Sem token na evidência (grep `ghu_|sk-|refresh_token|access_token|Bearer|eyJ` e usuário); sem `hub-ensaio-25-*` no
  `%TEMP%`.

### Acordo
- 2ª leitura (Opus, worktree destacada de 5489b3a): VOLTA, mesmo conserto 1; conserto 2 dela aceito; o 3 dela entra no
  1 (cuidado com `evidencia-22`). `git merge-tree` com a `integracao` atual (56cd23a, já com 22 e 24): sem conflito.
- Escopo provado: fases 1, 2, 3, 5 e 6 com Claude e Copilot; fase 1 do Codex. A fase 7 volta.
- Próxima rodada (2ª volta): conserto 1 com a fase 7 real de novo e o conserto 2; junta com a rodada curta da fase 4,
  da fase 2 do Codex e do conserto A→B, se a Vela quiser.

## Rodada 2 (2ª volta + rodada curta), 4628138 — 2026-10-17 ~20h (Fiel + 2ª leitura Opus)

Ramo `ticket-25`, HEAD 4628138 (contém `integracao` 56cd23a). **Veredito: PASSA com ressalvas, em acordo com a 2ª
leitura** (`parecer-25-Vela-segunda-leitura.md`, "Rodada 2"). Escopo provado: fases 1-7 com Claude e Copilot; Codex nas
fases 1 e 2. Codex nas fases 4-7 fora do 25 (decisão do maestro, ~19h45).

### Consertos da rodada 1
1. Fase 7 (dac76e6): feito. `25/prova-do-cliente.mjs` tira o `NODE_TEST_CONTEXT` e exige saída 0, `# pass` = harnesses
   e `# skipped 0`; teste com dublê (`25-cliente-sem-docker`). Rodada real b78c49d: `prova.tap` com `# pass 2`,
   `# skipped 0`; `hashes-do-22-cliente.json`: credenciais iguais, logins apagados. `evidencia-22` e `evidencia-24`
   iguais à `integracao` (diff vazio).
2. Evidência por rodada (f6a0f21): feito. `evidencia-25/rodadas/<data-hora>-<harnesses>-f<fases>/`; manhã e Codex
   18:00 repostos; a rodada apaga só `<fase>/<harness>`.

### Rodada curta (fase 4, fase 2 do Codex, descida A→B)
- fc6b10c: o `subir` espera o B convergir (`convergiu.mjs`, regra do gerador, hash igual; teste sem Docker). Evidência:
  530 arquivos em 218 s, 0 faltando, 0 diferente.
- 4a60595: fase 2 do Codex (`gpt-6-luna` nos `usos`): recusa da guarda no `decisions.md`, trocas passam, B com hash
  igual, nada em claro. Fase 4 (Claude, Copilot): conflito aberto; passada `divergencia` com o caminho e notificação;
  `estado_do_hub` conta o mesmo; as duas respostas começam pelo aviso e citam a nota.
- Hashes de todas as rodadas: só `~/.claude.json` mudou (sessões abertas); logins apagados. Sem token na evidência.
- Fiel: leves + vizinhos (`harness-real`, `25-*`, `25-hub-inteiro`, `27-pastas`, `22-kit-cliente`,
  `22-proxy-sem-docker`, `23-kit`) 73/0/1, duas vezes; `git status` limpo. 2ª leitura: 43/0/1; `merge-tree` sem conflito.

### Ressalvas
1. **Corrigir antes de levar ao Rebite (só texto):** "Fica para a instalação" ainda diz "Fases 4-7 a medir". Registrar
   os picos: fase 7 com 835 MB livres (135 acima do corte de 700, máquina quieta), fase 4 com 1.690 MB. É o 2º
   critério do ticket.
2. A pasta `rodadas/2026-10-17-1248-claude-copilot-f1-2-3` guarda a rodada das 12:59 (fases 2 e 3); a busca está em
   `resumo-rodada-1.md`. Nome engana.
3. O `hashes.json` reposto do Codex das 18:00 não tem `modelo`; só a rodada das 19:26 prova o Luna pela evidência.
4. `HARNESSES_F<n>` que não cruza com `HARNESSES` deixa a fase vazia e verde (inclusive a 7). Deveria falhar.
5. Cada rodada real da fase 7 suja o `evidencia-22`, que volta por `git checkout` à mão.
6. `cliente.ps1` deixa `%TEMP%/hub-ensaio-25-subir-22.log` (sem segredo). O 25-medidor teve 1 falha em ~16 rodadas.
7. Seguem as assumidas: B conferido só no `tasks.md`; `write_note` pelos harnesses e reconexão do MCP fora; Codex 4-7
   fora.
