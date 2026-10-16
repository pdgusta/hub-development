# Busca

Type: task
Status: ready-for-agent
Dono: Worker 3
Com: Prumo
Blocked by:

Faixa 3 da spec (`../spec.md`, seção "Faixas", Worker 3). Fatia vertical: entrega funcionando de ponta a ponta no hub
de ensaio e no HOME de ensaio, sem esperar as outras faixas.

## O que construir

**Busca** (faixa 3 do corte; Answers dos tickets 09 e 54, lacunas do Prumo para a faixa 3): (a) `kit/par/03-busca.ps1` no contrato do kit: instala o obsidian-hybrid-search **0.16.2 fixo** com `npm install` local em `C:\context-hub\.local\busca\` (nunca `-g`), com `-WhatIf`; (b) `busca/iniciar.ps1` sobe `ohs serve --foreground` em `127.0.0.1:3939` (padrão do README 0.16.2, rota `/mcp`, HTTP sem estado) sobre o hub, com `LOCAL_EMBEDDING_MODEL=Snowflake/snowflake-arctic-embed-m-v2.0` (variável provada na bancada, `bancada-busca/scripts/robusta/ohs-modelo.py`; **não está no README**) e `OBSIDIAN_IGNORE_PATTERNS` com `**/.*/**` e `**/.*` (o que tem ponto, como no LiveSync) mais o que a faixa 1 gerar para `local: true`; um analisador só, sem campo de idioma; (c) o `.obsidian-hybrid-search.db` (e `-wal`/`-shm`) fora do git e do LiveSync (o `--db` não move o banco, achado da bancada); (d) a configuração do gemini-embedding-001 pelo FreeLLMAPI (`OPENAI_BASE_URL` = `$env:FREELLM_BASE_URL/v1`, nunca `localhost:3001` fixo; `OPENAI_EMBEDDING_MODEL`), escrita em `busca/gemini.env` e **desligada**; testada uma vez num segundo índice, numa cópia do hub de ensaio em porta 3940 (o `--db` não separa índice), se o Gustavo liberar a cota; (e) escreve `HUB_MCP_BUSCA_URL=http://127.0.0.1:3939/mcp` no `.env.modelo` do kit no minuto 5. Ligar no boot (tarefa agendada) fica `ready-for-human`

## Critério de aceite (de ponta a ponta)

`busca/testes/aceite.mjs` (Node ≥ 22, sem pacote de fora, MCP Streamable HTTP por `fetch`: `initialize` e `tools/call search`) contra o hub de ensaio: uma pergunta em pt-BR por palavra (`fulltext`) e uma por paráfrase sem palavra em comum (`semantic`) acham a nota esperada entre as 3 primeiras; uma nota criada no disco durante o teste aparece na busca em até 60 s (mede e grava o tempo); nada com ponto no caminho aparece; `status` mostra indexadas = `.md` válidos, e a lista das recusadas por YAML inválido sai no relatório; pedido com `Host` estranho é recusado. Roda duas vezes seguidas (a segunda reaproveita o índice)

## Como segue sem esperar

hub de ensaio (Worker 2): copio no minuto 0 e escrevo as notas e as perguntas de aceite eu mesmo, sem esperar a faixa 1; exclusão de `local: true` (faixa 1): leio a lista gerada se existir, senão só o padrão de ponto, e entra na segunda passada; kit (faixa 8): só a URL no `.env.modelo` e o meu `03-busca.ps1`; proxy (faixa 10): ela usa a URL; um dublê não é preciso, o servidor de verdade sobe no minuto 10–15; LiveSync (faixa 4): não preciso dele; o tempo "edição no par B → busca no par B" fica para o teste de aceite final, se as duas faixas terminarem

## Regras

- Ramo e pasta próprios (git worktree) do repositório do hub em `C:\context-hub`; nada global de verdade sem o aval do
  Gustavo (HOME de ensaio); a execução inteira dura 1 hora: o que não couber vai para "Fica para outra execução" no plano.
- Até 10 subagentes; parte muito complexa: um subagente Fable 5.1 médio.
- Antes de juntar: revisão do Prumo (decisões) e do Prumo 2 (construção).
- Erro achado na spec: corrija a spec na sua faixa.

## Comments
