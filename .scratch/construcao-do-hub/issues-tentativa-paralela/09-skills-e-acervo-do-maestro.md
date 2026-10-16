# 09: Skills e acervo do maestro

Type: task
Status: claimed
Dono: Worker 9
Com: Prumo 2
Blocked by: None (can start immediately)

Faixa 9 da spec (`../spec.md`, seção "Faixas", Worker 9). Fatia vertical: entrega funcionando de ponta a ponta no hub
de ensaio e no HOME de ensaio, sem esperar as outras faixas.

## O que construir

**Skills e acervo do maestro** (faixa 9 do corte; tickets 15, 40, 43, 44 e comentário de 2026-10-12 do 16), tudo em `agents/` do hub: `skills/routing.yml` (gatilho por palavras do pedido, tipo de nota pelo caminho e papel → skill; camada geral e de papel) com as primeiras linhas (a skill do FreeLLMAPI para pesquisa, `armis-docx`, as skills de design por papel da frente da cidade); o hook de entrada sem IA que confere a tabela e injeta "use a skill X"; a família `maestro-*` (`maestro-acervo` é a porta; catálogo curto e um arquivo por peça) com o primeiro lote do Answer do 40 (papéis genéricos sem nome de cliente e o Designer, a partitura de hoje como receita e o arranjo deste workspace, contratos-opção de roteamento de modelos com o FreeLLMAPI, orquestração e onde abrir, o lembrete e a guarda); o hook de início que só age com `MAESTRI_TERMINAL_ID` e manda começar por `maestro-acervo`; a guarda do acervo (Claude Code: antes da ferramenta, gravar em `agents/skills/**` ou `agents/maestro/**` pede aval, exceção do maestro em `routing.yml`; Codex e Copilot: recusa apontando `agents/maestro/propostas/`); o registro de uso por hook em `agents/maestro/uso/<máquina>.md`; no fim da resposta, registrar se a skill indicada rodou, sem obrigar

## Critério de aceite (de ponta a ponta)

- [ ] testes automatizados dos hooks com a entrada JSON de cada harness: um pedido de pesquisa que não cita o FreeLLMAPI recebe "use a skill" dele (o aceite do ticket 15); sem `MAESTRI_TERMINAL_ID` o hook de início não faz nada, com ele injeta o lembrete; gravar em `agents/skills/` dá `ask` no Claude Code e recusa com o caminho de propostas no Codex e no Copilot, **tanto pelo caminho real quanto pelo da junction** (teste pedido no 16); o maestro grava `routing.yml`; usar uma skill vira linha no registro; `routing.yml` passa no esquema e cada `SKILL.md` da família tem `name` e `description` válidos. Ao vivo, com HOME de ensaio: `claude -p` com o pedido de pesquisa mostra a injeção

## Como segue sem esperar

o hub de ensaio (proposta do Worker 2) para `agents/`; entrega os hooks em `hooks/09-skills/` no formato de fragmento do Worker 8, sem tocar em settings de outra faixa; as junctions são do kit (faixa 8), que liga a minha pasta como ela estiver; o primeiro lote lê o Maestri e o vault só para leitura. Não espera ninguém

## Regras

- Ramo e pasta próprios (git worktree) do repositório do hub em `C:\context-hub`; nada global de verdade sem o aval do
  Gustavo (HOME de ensaio); a execução inteira dura 1 hora: o que não couber vai para "Fica para outra execução" no plano.
- Até 10 subagentes; parte muito complexa: um subagente Fable 5.1 médio.
- Antes de juntar: revisão do Prumo (decisões) e do Prumo 2 (construção).
- Erro achado na spec: corrija a spec na sua faixa.

## Comments

- 2026-10-15 ~21h58 (Worker 9): **parado a pedido do Gustavo (21:56).** Feito: worktree `C:\context-hub-wt\faixa-09`,
  ramo `faixa-09` (da ponta de `integracao`, 69cb383); desenho comum da faixa (layout, variáveis, formatos de entrada e
  saída dos três harnesses, seams) em `execucao/work/09.md`; `hooks/09-skills/lib.mjs` (YAML mínimo, esquema e
  casamento da `routing.yml` por palavras, caminho e papel; caminho real e pela junction; saídas por harness) com
  `hooks/09-skills/test/lib.test.mjs` (4 testes). **Testes não confirmados verdes**: a última execução falhou só porque
  `node --test` recebeu uma pasta (no Node 24, rodar `node --test hooks/09-skills/test/*.test.mjs`). Nada junto em
  `integracao`; nenhum subagente aberto. Falta: `routing.yml` com as primeiras linhas, hooks de entrada, início, guarda
  (com verificador `agent`), uso e fim, `verificar-acervo`, `fragmento.json`, a família `maestro-*` com o primeiro lote,
  `agents/test/09-skills.ps1` e a prova ao vivo com `claude -p`.
