# Worker 3: notas

## Faixa: 3, Busca (assumida na volta 1)

Linha completa no `plano.md` (tabela de faixas), fronteiras em "Worker 3 (volta 1)", pergunta do gemini em
"Perguntas ao Gustavo".

## Fatos com fonte

- obsidian-hybrid-search **0.16.2** (`npm view`, 2026-10-15), repo `flowing-abyss/obsidian-hybrid-search`. README
  (`npm view obsidian-hybrid-search readme`): `ohs serve` = MCP por HTTP, padrão `127.0.0.1:3939`, rota `/mcp`,
  Streamable HTTP sem estado (sem `Mcp-Session-Id`); porta ocupada = erro (use `--port`); `--host`, `--allowed-host`
  (ou `OBSIDIAN_MCP_ALLOWED_HOSTS`), `--allow-any-host`; ferramentas `search`, `read`, `reindex`, `status`
  (`OBSIDIAN_PREFIX` muda o nome); `OBSIDIAN_IGNORE_PATTERNS` (padrão `.obsidian/**,templates/**,*.canvas`, persiste no
  banco), `OBSIDIAN_RESPECT_GITIGNORE=true` por padrão; remoto por `OPENAI_BASE_URL`/`OPENAI_EMBEDDING_MODEL`/
  `OPENAI_API_KEY`. Nenhuma autenticação além do `Host`.
- `LOCAL_EMBEDDING_MODEL=Snowflake/snowflake-arctic-embed-m-v2.0`: **não está no README**; provado na bancada
  (`.scratch/context-hub/bancada-busca/scripts/robusta/ohs-modelo.py`, `fase2-modelos.md`: híbrida 0,632, reindexação
  388 s e 1,5 GB para 124 notas). granite falhou por falta de `onnx/model_quantized.onnx`.
- Bancada (`bancada-busca/relatorio.md`): `npm install` local 57 s (avisos de scripts não aprovados, rodou mesmo assim);
  `--db` não move o banco (fica na raiz do cofre); 12 notas com YAML inválido ficam fora; CLI 1 a 3 s por busca; rajada
  de 200 arquivos achável em ≤ 147 s com o watcher.
- Docker Desktop desligado agora (Worker 4) → o FreeLLMAPI (Docker desta máquina) também está fora.

## Orçamento da hora (estimativa)

- 0–5 min: copiar hub de ensaio, URL no `.env.modelo`; disparar `npm install` e a baixa do modelo em segundo plano.
- 5–20: `03-busca.ps1`, `iniciar.ps1`, primeira indexação com arctic (hub de ensaio pequeno: bem abaixo dos 388 s).
- 15–40: `aceite.mjs` (subagente), notas e perguntas de aceite em pt-BR; rodar duas vezes.
- 40–50: gemini escrito; teste único só com o aval (pergunta ao Gustavo).
- 50–60: segunda passada (lista `local: true` da faixa 1, `--allowed-host` do proxy da faixa 10), Prumos.
- Risco: a baixa do arctic (tamanho não medido) e a memória (1,5 GB na bancada) ao lado de nove outras faixas.

## Não verificado

- Se o TBXark/mcp-proxy repassa o `Host` do cliente.
- Se o OHS lê `.txt`/`.csv`; se dois `ohs serve` em portas diferentes convivem (bancada não testou).
- Tempo edição → busca com o CLI do LiveSync ligado.

## Volta 2

- Spec, faixa 3: igual à minha linha do plano; acrescentei no "Como segue sem esperar" o `.gitignore` (faixa 1), o `Host` pelo proxy (faixa 10) e a baixa do arctic no minuto 0.
