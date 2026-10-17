# Relatório do ticket 21: arquivar e cópia diária (Trilho)

2026-10-17 ~08h10. Rascunho. ~09h40: conserto do EPERM (9ce2496). ~09h40: Docker 3ª rodada tudo passou (1c87f9b); pronto para o Fiel. Junção depois do 16.

## Estado

- Ramo `ticket-21` (HEAD 5fe3fda: f32bd4c com integracao fce0529, o 16 juntado), worktree `C:\context-hub-wt\ticket-21`, de `integracao` 9cc878b com o
  `ticket-16` juntado (c36ece4), porque o item da cópia diária na vigia é do 16 (maestro, 07:31).
- **Junção só com 08 e 16 resolvidos.** O que depende do 08 entra quando ele for juntado.
- Costuras aceitas: `etapas/costuras-21-Trilho.md`.

## Decisões (maestro, 2026-10-17 ~07h55)

1. Edição recente = arquivo da pasta mudado nos últimos 15 min.
2. Outro par desligado ou sem resposta = recusa.
3. Em dia = as duas replicações de envio em `running`, com 0 pendentes.
4. O `10-manutencao.ps1` (tarefa diária, item g do Worker 10) vai para o 23.

## O que foi construído

- **Skill** `agents/skills/arquivar/` (`arquivar.mjs`, `SKILL.md`):
  `arquivar <pasta> --env <par>.env [--motivo <texto>]` move a pasta para `<pasta-mãe>/_archive/<AAAA-MM-DD>--<nome>/`
  (a de primeiro nível, para o `_archive/` da raiz: é o caminho de origem que o `lib/frontmatter.mjs` reconstrói).
  Cada nota com frontmatter ganha `archived_at` (e `archive_reason` com `--motivo`), por troca de trecho
  (`trocarCampos`, exportada da lib do frontmatter, o mesmo `aplicarTrocas` do verificador). Recusa, com código 1 e o
  motivo: replicação deste par ou do outro fora de dia; CouchDB do outro par sem resposta; arquivo mudado há menos de
  15 min; raiz, pasta inexistente, já num `_archive/`, com ponto, destino existente.
  O que não replica dentro da pasta (`.secrets/`) muda só nesta máquina: a saída lista o que ficou no lugar antigo
  do outro par.
- `agents/code/bin/copia-diaria.mjs --env <par>.env`: roda o gerador de exclusões (o `.git/info/exclude` leva as pastas
  `local: true`); tira do índice o que passou a ser excluído (`git ls-files -ci --exclude-standard` → `git rm --cached`;
  o disco fica); HEAD para `par/<HUB_MAQUINA>` por `git symbolic-ref` (sem checkout); `add -A`; `commit` se mudou;
  `push` para `HUB_COPIA_REMOTO`. Nunca `pull`, `fetch`, `checkout`, `reset`, `merge`. Deploy key por `HUB_COPIA_CHAVE`
  (`GIT_SSH_COMMAND`). Falha: saída 1 e o item `copia-diaria` (`informa`, com o motivo e a hora) por `gravarItem`; a
  cópia seguinte que dá certo o tira.
- `agents/code/bin/conferir-cabeca.mjs [<hub>]`: 0 com a cabeça em ordem (diz o tamanho); 1 com o bloco ausente ou
  acima de 2.000 caracteres. A regra mora em `lib/cabeca.mjs`; o `verificar-hub` passou a usá-la.
- `agents/code/bin/limpar-arquivo.mjs [<hub>] [--hoje]`: **só simula**. Lista as pastas de cada `_archive/` com a data
  do nome além de 30 dias e diz "simulação: nada apagado"; não há caminho que apague (o prazo é do 56).
- Kit: `agents/code/kit/par/env/10.env.modelo` (`HUB_MAQUINA`, `HUB_COPIA_REMOTO`, `HUB_COPIA_CHAVE`).

## Achados

1. No Windows, `process.exit(1)` logo depois de um `fetch` derruba o node (`UV_HANDLE_CLOSING`, código 3221226505):
   o `arquivar` sai por `process.exitCode`. O mesmo conserto na vigia, no ramo do 16 (81b4a3d), juntado aqui
   (4d7853c).
2. O `montar.mjs` commita a pasta local do hub de ensaio (`initiatives/context-hub/labs`) no `main`: a cópia diária a tira
   do índice na primeira passada (caso de teste).
3. **O rename da pasta dá EPERM com o sincronizador rodando** (Docker, 1ª rodada 08:05 e 2ª 09:05,
   `logs/trilho-21-docker-1.log` e `-2.log`). Causa, provada num teste leve: o CLI observa o hub com o chokidar, que
   abre um `fs.watch` em cada pasta; no Windows, um `fs.watch` numa **subpasta** bloqueia o rename da pasta-mãe; o da
   própria pasta não bloqueia. Esperar não adianta (o CLI segura enquanto roda). O primeiro conserto (22abdd2, esperar
   10 s e recusar "em uso") só mudou a mensagem.
   - Conserto (9ce2496, com aval do maestro, 09h25): tenta o rename da pasta; com EPERM, move **arquivo por arquivo**
     para a pasta nova (o `fs.watch` não impede mover arquivos) e apaga a árvore velha, vazia, por `rmdir` (o que alguém
     gravar nela no meio fica, e a saída diz). Sem parar o sincronizador.
   - Arquivo aberto por um editor sem partilha de apagar: o rename dele falha; espera até 10 s; depois **devolve o que
     já tinha movido**, apaga o destino e recusa "em uso". Nada muda.
   - **No meio da mudança, o outro par pode ver parte dos arquivos no lugar novo e parte no velho** (o CLI manda um
     apagar e um criar por arquivo, como faria com o rename). **O fim é consistente**: o mesmo de um rename da pasta.
   - O node abre arquivo partilhando o apagar: aberto pelo node, o arquivo se move. O teste segura o arquivo como um
     editor (.NET, `FileShare.Read`).

## Testes

- Sem Docker: `node --test agents/code/test/21-*.test.mjs`: conferir-cabeca 4, copia-diaria 4, limpar-arquivo 1,
  arquivar 10 (em 9ce2496: pasta observada como pelo sincronizador; aberto por editor, devolve tudo). Com os afetados (04, 05, 05-nova-iniciativa, 20, 07-kit-sem-docker): 75/75.
- Docker: `pwsh -NoProfile -File agents/code/test/21-arquivar.test.ps1` (hub-ensaio-21-a/b, 5996/5997): arquivar entre
  dois pares (a pasta chega ao B com o `archived_at`); recusa com a replicação parada; cópia com o remoto quebrado sai
  com erro e a passada seguinte da vigia notifica.
  - 1ª (08:05) e 2ª (09:05): o rename deu EPERM (Achado 3).
  - 3ª (09:32, `logs/trilho-21-docker-3.log`, 1c87f9b = 9ce2496 com o ticket-16 0332466 e o 08): **tudo passou** (9
    casos): arquivar move com o sincronizador rodando, a pasta chega ao B e sai do lugar antigo lá, com o
    `archived_at`; recusa com a replicação parada; a cópia empurra o ramo do par; remoto quebrado sai com erro e a
    vigia notifica; os contêineres saem.
- Sem Docker em 1c87f9b: 21-* e afetados (04, 05, 20, 07-kit-sem-docker): 78/78.

## Rodada 1 do Fiel (VOLTA, 2 consertos), feitos em f32bd4c

1. **Pasta de outro disco passava pela guarda** (`D:/fora/pasta`): o `relative` do Windows devolve o caminho absoluto,
   e a guarda olhava o texto já com `/`. Agora `isAbsolute(relative(hub, origem))` recusa "não está dentro do hub".
   Casos novos: `Z:/fora/pasta` e `Z:\fora\pasta`.
2. **Provar que o sincronizador de A segue de pé depois do arquivar.**
   - De onde vinha o `Assertion failed: !_wcsnicmp(filename, dir, dirlen), file src\win\fs-event.c, line 72`: **não
     do Docker** (o `logs/trilho-21-docker-3.log` tem 11 linhas, sem ele). Veio dos testes leves (duas vezes, no
     registro da rodada de 1c87f9b): o observador dublê abortou. Ele observava o hub de ensaio pelo `%TEMP%` com o
     nome curto do Windows (`C:\Users\GUSTAV~1.DEL\...`); o libuv compara o nome do evento com o da pasta observada e
     aborta. O Fiel reproduziu numa sonda: curto aborta, longo fica vivo. Uma sonda minha mais simples (um arquivo só)
     não abortou em nenhum dos dois: o aborto depende de quantos eventos chegam.
   - O CLI de verdade observa o hub pelo caminho longo: `C:\context-hub`; no Docker,
     `C:\Users\gustavo.delfino\AppData\Local\Temp\hub-ensaio-21` (o `GetTempPath` do PowerShell dá o longo).
   - Teste leve: o dublê observa pelo `realpathSync.native` (longo), como o CLI, e o teste confere que ele **segue
     vivo** depois do arquivar e depois do ir-e-voltar do caso "aberto por editor".
   - Docker: depois do arquivar, confere o **mesmo PID** do sincronizador de A e que **uma nota nova em A chega ao
     B**; o registro mostra o caminho do hub e o longo.
   - Achado para o kit (o maestro levou às regras e ao 23): com `HUB_ROOT` em nome curto, o sincronizador pode abortar
     ao arquivar ou ao mover arquivos à mão.
- Ressalvas feitas: a data da mensagem da cópia diária é a local (`sv-SE`), não UTC; o comentário "Troca de trecho"
  voltou para cima do `aplicarTrocas`. Sem conserto: no caminho arquivo por arquivo, subpasta vazia não vai para o
  destino (o LiveSync não replica pasta vazia); falha na devolução sai como exceção, com estado parcial (raro).
- Testes leves em f32bd4c: 21-*, 04, 05, 20: 77/77. Docker 4ª rodada: pela fila (1b).

## O que espera o 08

- Nada do aceite do 21 depende do 08 diretamente; a junção espera o 08 e o 16 resolvidos (o 16 espera o 08).
