# Manutenção e kit de cliente

Type: task
Status: ready-for-agent
Dono: Worker 10
Com: Prumo 2
Blocked by:

Faixa 10 da spec (`../spec.md`, seção "Faixas", Worker 10). Fatia vertical: entrega funcionando de ponta a ponta no hub
de ensaio e no HOME de ensaio, sem esperar as outras faixas.

## O que construir

**Manutenção e kit de cliente** (faixa 10 do corte; tickets 33, 34, 36, 14, rodada 7 do 56 e comentário de 2026-10-15 do 16, lacunas de dono 4 e 5), em `agents/bin/` e `kit/cliente/`: (a) `arquivar <pasta>` move para o `_archive/` da própria raiz como `_archive/<AAAA-MM-DD>--<nome>/` (a data viaja no nome, sem arquivo com ponto), só se o outro par estiver em dia (replicação nos dois sentidos sem atraso de 15 min, lida do `_scheduler/docs`) e sem edição recente na pasta; senão recusa dizendo por quê; (b) `limpar-arquivo` apaga do `_archive/` o que passou de 30 dias (é o "depois dos 30 dias" da rodada 7 do 56), com `-WhatIf`; (c) `copia-diaria`: no `.git` da raiz, ramo `par/<máquina>`, só `add`, `commit` e `push`, nunca `pull` nem `checkout`; falha alto (saída ≠ 0 e linha no estado da vigia); (d) `conferir-cabeca`: o bloco `cabeca:inicio/fim` do `AGENTS.md` existe e cabe em 2.000 caracteres (lacuna 5; a atualização em si é o fork relendo o bloco, ver fronteiras); (e) kit de cliente: no par, o TBXark/mcp-proxy com as rotas `/busca/mcp`, `/banco/mcp` (só leitura) e `/banco-escrita/mcp`, um token por rota; no cliente, `ligar-cliente.ps1` grava a linha de MCP com `Authorization: Bearer` de variável de ambiente nos três harnesses, `--allow-all-mcp-server-instructions` no Copilot CLI e o contrato na configuração global, tudo em HOME de ensaio; (f) se couber: a linha da ponte `mcp-remote` do Claude Desktop, gerada e não instalada; (g) `kit/par/10-manutencao.ps1` no contrato do kit, registrando a tarefa diária (cópia + limpeza + cabeça) só com `-WhatIf`

## Critério de aceite (de ponta a ponta)

testes automatizados no hub de ensaio: `arquivar` move com o outro par em dia e recusa com ele atrasado ou com arquivo editado há minutos; `limpar-arquivo` apaga a pasta de 31 dias e mantém a de 29; `copia-diaria` gera commit no ramo do par e empurra para um repositório nu local, e com o remoto quebrado sai ≠ 0 e grava a linha no estado; `conferir-cabeca` recusa bloco ausente ou longo. Ponta a ponta do cliente, tudo em 127.0.0.1 no lugar da tailnet: um cliente de ensaio busca pelo proxy, lê pela rota só de leitura, tem a gravação recusada nela, e sem token leva 401; mede se o proxy repassa o `instructions` (não verificado no 14)

## Como segue sem esperar

busca e banco (faixas 3 e 5): o proxy aponta para as URLs do `.env` do Worker 8; até elas existirem, dois MCP dublês HTTP mínimos (uma ferramenta de busca, uma de leitura e uma de gravação que respeita `READ_ONLY`), trocados pelos reais na segunda passada sem mudar o proxy. Estado do outro par (faixa 4): `arquivar` lê de uma fonte trocável, o `_scheduler/docs` do CouchDB de ensaio ou um JSON de exemplo no mesmo formato desde o minuto 0. Estado da vigia (faixa 7): só acrescento um item `copia_diaria` no formato do Worker 8. Hub de ensaio do Worker 2. Não espera ninguém

## Regras

- Ramo e pasta próprios (git worktree) do repositório do hub em `C:\context-hub`; nada global de verdade sem o aval do
  Gustavo (HOME de ensaio); a execução inteira dura 1 hora: o que não couber vai para "Fica para outra execução" no plano.
- Até 10 subagentes; parte muito complexa: um subagente Fable 5.1 médio.
- Antes de juntar: revisão do Prumo (decisões) e do Prumo 2 (construção).
- Erro achado na spec: corrija a spec na sua faixa.

## Comments
