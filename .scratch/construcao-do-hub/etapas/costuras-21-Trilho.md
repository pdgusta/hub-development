# Ticket 21: costuras propostas (Trilho, 2026-10-17 ~07h50)

Ramo `ticket-21`, worktree `C:/context-hub-wt/ticket-21`, de `integracao` 9cc878b com `ticket-16` juntado (c36ece4).
Fonte: Worker 10 do `spec.md`, faixa 10 (`spec-partes/faixas-09-10.md`). Fora: kit de cliente, proxy, ponte do Desktop
(itens e, f do Worker 10: outro ticket); o prazo de 30 dias (56).

## Onde mora (critério "quem chama")
- `agents/skills/arquivar/` (o agente chama): `arquivar.mjs` + `SKILL.md`.
- `agents/code/bin/` (só o kit ou a tarefa rodam): `copia-diaria.mjs`, `conferir-cabeca.mjs`, `limpar-arquivo.mjs`.
  A regra da cabeça sai do `verificar-hub.mjs` para `lib/cabeca.mjs` (os dois usam a mesma).
- Variáveis novas no fragmento `agents/code/kit/par/env/10.env.modelo`: `HUB_MAQUINA` (o nome do ramo
  `par/<máquina>`), `HUB_COPIA_REMOTO` (URL do repositório; no ensaio, um repositório nu numa pasta de ensaio) e
  `HUB_COPIA_CHAVE` (a deploy key, por `GIT_SSH_COMMAND`; vazio no ensaio).

## Costuras (o teste só olha o lado de fora)
1. **`arquivar <pasta> --env <par>.env [--motivo <texto>]`** → a pasta vai para o `_archive/` da pasta-mãe como
   `_archive/<AAAA-MM-DD>--<nome>/` (para as de primeiro nível, o `_archive/` da raiz; é o que o
   `lib/frontmatter.mjs` reconstrói como caminho de origem). Cada nota `.md` com frontmatter do hub ganha
   `archived_at` (e `archive_reason` com `--motivo`), como o `archived.yml` pede. Depois, o `verificar-hub` passa.
   - Antes de mover, confere: as duas replicações (`_scheduler/docs/_replicator/hub-envio-para-o-outro-par` no CouchDB
     do par e no do outro, por `HUB_VIGIA_OUTRO_PAR_URL` ou `HUB_OUTRO_PAR_URL`) em `running` com 0 pendentes; nenhum
     arquivo da pasta mudado há pouco. Senão, recusa (código 1) dizendo por quê, e nada muda.
   - Teste sem Docker (`21-arquivar.test.mjs`): CouchDB dublê dos dois pares (molde do 16). Move; recusa com o outro
     par atrasado (pendentes ou estado ≠ `running`, de cada lado); recusa com edição recente; recusa com o outro par sem
     resposta; recusa destino que já existe.
   - Ponta a ponta com Docker (pela fila, `21-arquivar.test.ps1`): os dois pares do `ensaio.psm1`; move e a mudança
     chega ao B; com a replicação pausada, recusa.
2. **`copia-diaria --env <par>.env`** → no `.git` da raiz: roda o gerador de exclusões (o `.git/info/exclude` leva as
   pastas `local: true`; recusa do gerador = falha); tira do índice o que passou a ser excluído
   (`git ls-files -ci --exclude-standard` → `git rm --cached`); `git add -A`; `commit` (se mudou); `push` para
   `HUB_COPIA_REMOTO`, `HEAD:refs/heads/par/<máquina>`. Nunca `pull`, `fetch`, `checkout`, `reset`, `merge`.
   - O HEAD do hub aponta para `par/<máquina>`: se não aponta, `git symbolic-ref HEAD refs/heads/par/<máquina>`, que não
     escreve no disco (o próximo commit leva a árvore inteira).
   - Falha (gerador, commit ou push): saída ≠ 0 e o item `copia-diaria` (`informa`, com o motivo) no estado da vigia,
     por `gravarItem` (a vigia notifica na passada seguinte). Sucesso tira o item.
   - Teste sem Docker (`21-copia-diaria.test.mjs`): hub de ensaio + repositório nu no `%TEMP%`. Commit no ramo
     `par/<máquina>` do nu; o disco não muda (hash dos arquivos antes e depois); `.local/` e a pasta `local: true` fora
     do commit; sem mudança, nada novo e saída 0; remoto quebrado, saída ≠ 0 e o item no estado; de volta, o item sai.
3. **`conferir-cabeca [<hub>]`** → 0 com a cabeça em ordem; ≠ 0 com o bloco ausente ou acima de 2.000 caracteres,
   dizendo qual. Teste: os três casos.
4. **`limpar-arquivo [<hub>]`, só simulando** (o prazo é do 56): lista as pastas de `_archive/` com a data do nome
   além de 30 dias e diz "simulação: nada apagado". Não há caminho que apague. Teste: a de 31 dias aparece, a de 29 não,
   nada some.

## Perguntas (o spec deixa em aberto)
1. **"Edição recente"**: proponho algum arquivo da pasta com `mtime` nos últimos 15 min (o mesmo limite da replicação;
   o LiveSync grava no disco o que vem do outro par, então o `mtime` local mostra também a edição de lá).
2. **Outro par desligado ou sem resposta**: proponho recusar ("não sei se o outro par está em dia"): o que ele editar
   desligado se separaria da pasta movida ao voltar.
3. **"Em dia"**: proponho as duas replicações em `running` com 0 pendentes agora, mais estrito que os 15 min da vigia
   (lá o limite é para notificar).
4. **`10-manutencao.ps1`** (registrar a tarefa diária, só com `-WhatIf`, item g do Worker 10): entra no 21 ou fica para
   o ticket do kit (23/24)? Proponho fora; o 21 entrega os comandos.

## Respostas (maestro, 2026-10-17 ~07h55)
Sim nas quatro: edição recente = arquivo mudado nos últimos 15 min; outro par desligado ou sem resposta = recusa; em dia
= as duas replicações `running` com 0 pendentes; o `10-manutencao.ps1` vai para o 23.
