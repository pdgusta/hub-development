# Parecer do ticket 23 (Cinzel): kit de par, a forma (esqueleto)

## Rodada 1 — 2026-10-17 ~09h30 (ramo ticket-23, ponta e9dcef7, com integracao e98a891)

Veredito: **VOLTA**, por 1 conserto. Fiel sozinho (Fielzinho sem cota até 12h15; leitura dele pendente). Junção só com
11, 15, 17, 18, 20 e 27 resolvidos (mandato).

### Conferido pelo Fiel

- Árvore limpa antes e depois. `node --test agents/code/test/23-kit.test.mjs`: 13/13 (3 min 26 s). Sem sobra
  `hub-ensaio-23-*` nem `hub-kit-codex-*` em `%TEMP%`.
- **Nada global:** hashes das configurações reais antes e depois do teste (`~/.claude/settings.json`, `CLAUDE.md`,
  `~/.codex/config.toml`, `hooks.json`, `AGENTS.md`, `~/.copilot/config.json`, `mcp-config.json`,
  `copilot-instructions.md`) iguais; listagens de `~/.claude/skills`, `~/.agents/skills`, `~/.copilot/hooks` sem
  mudança de entrada (só o mtime de `~/.claude`, pelas sessões abertas: history, sessions, backups).
- Lidos `instalar.ps1`, `casa.mjs` e `08-harnesses.mjs`: recusa sem `-Casa`/`HUB_HOME_ENSAIO`; `caminho()` recusa
  fora da casa; mover para a cópia antes de tocar; desfazer em ordem inversa, parando se algo mudou depois do kit;
  contrato por link (Codex, Copilot) e import (Claude); junction só das skills com `metadata.camada: geral`; token do
  banco só por variável; GSD tirado pelo manifesto; `hooks.state` com hash do app-server numa cópia.

### Consertos

1. **(Fiel) A junção dos hooks nunca tira o grupo antigo do hub: fragmento que muda duplica o hook.** `juntarHooks`
   (`08-harnesses.mjs`) só acrescenta o grupo que não é igual. Quando um fragmento do hub muda entre passadas
   (atualização do hub; os hooks de 17 e 18 entrando pela "passada seguinte", que é a costura do próprio ticket), o
   grupo velho fica e o novo entra: o hook roda duas vezes (no fim da resposta, dupla devolução; na leitura, aviso
   duplo). Peça tirada do hub deixa hook apontando para pasta que não existe.
   - Sonda (hub do `montar.mjs` com `agents/`, casa de ensaio, `-Passos 08`): 1ª passada, `hooks/leitura/depois` uma
     vez em `.claude/settings.json` e `.codex/hooks.json`; trocado `"timeout": 10` por `15` nos fragmentos `claude` e
     `codex` da leitura; 2ª passada: **duas vezes** em cada. Sonda apagada.
   - Conserto: antes de juntar, tirar os grupos do hub (comando dentro de `<hub>/agents/code/hooks/`) que não estão nos
     fragmentos atuais, e as aprovações `hooks.state` deles; os alheios ficam. Teste: fragmento mudado e peça tirada,
     segunda passada com um grupo só e sem o da peça tirada.

### Ressalvas (não seguram; para o 26)

1. **Desfazer no HOME real:** o desfazer recusa caminho que mudou depois do kit. O Claude regrava `~/.claude.json` a
   cada sessão e o Codex regrava o `config.toml` (lição 2 do 03): no HOME real, o desfazer vai quase sempre parar
   nesses dois. No 26, desfazer por chave (tirar o que o kit pôs) nos arquivos que o harness regrava.
2. As ressalvas 1 a 6 do relatório (mod, extensão, `statusLine`, `notify` composto; `hooks.state` alheio que muda de
   índice; tabelas do GSD no `config.toml`; XML não validado pelo Agendador; como os harnesses enxergam a casa; pontos
   abertos do spec). Em particular: o kit não tem como ligar `--allow-all-mcp-server-instructions` do Copilot por
   arquivo (doc lida pelo Cinzel); quem abre o Copilot passa a opção (24, 26).

## Rodada 2 — 2026-10-17 ~10h10 (HEAD f304e6c)

Veredito: **PASSA** (Fiel sozinho; Fielzinho sem cota até 12h15, leitura pendente). Junção só com os bloqueios
resolvidos.

- Conserto 1 feito: `juntarHooks` tira antes o grupo do hub (comando em `<hub>/agents/code/hooks/`) que não está nos
  fragmentos atuais; tira o `hub-<peça>.json` órfão do Copilot; das aprovações `hooks.state` deste `hooks.json` fica
  só a que ainda casa hook e hash. Alheios ficam.
- Sonda da r1 repetida, com um hook alheio no `settings.json`: 1ª passada, leitura uma vez; fragmento da leitura
  mudado, 2ª e 3ª passadas, leitura **uma vez** no Claude e no Codex; alheio mantido; desfazer volta a casa e apaga o
  `.hub-kit`. (A peça tirada vai pelo teste novo do Cinzel; neste ramo não há a pasta da vigia.)
- `23-kit.test.mjs`: 14/14 (Fiel). Hashes das configurações reais e listagens das pastas globais iguais antes e
  depois; sem sobra em `%TEMP%`; árvore limpa.
- Ressalva do desfazer para o 26: anotada pelo Cinzel.

## Reabertura — 2026-10-17 ~10h55: **VOLTA** (achado do Fiel ao revisar o 24)

Errei na rodada 2: não rodei o detector do 29. `node --test agents/code/test/harness-real.test.mjs` no ramo
ticket-23 (f304e6c): **2 falhas**, "23-kit.test.mjs sem comHarness" (o teste sobe o app-server do Codex, uma das
marcas do detector: `harness-real.test.mjs:19`), e o caso "sem HUB_HARNESS_REAL, os testes de harness aparecem
pulados" também falha por isso. A suíte da junção ficaria vermelha.

Conserto 2: conciliar o 23 com o 29 sem perder o teste da forma na suíte comum. A decisão do maestro (resposta 3:
app-server sem modelo e sem login roda sem trava) pede uma exceção explícita e estreita no detector (só o app-server,
sem login nem modelo, com o motivo), ou separar a parte do `hooks.state` num teste atrás do `comHarness`. Escolha do
Cinzel, com o maestro se mexer no 29. Rodar `harness-real.test.mjs` junto.

## Rodada 3 — 2026-10-17 ~11h10 (a419182): **PASSA**

Conserto 2 feito: exceção `SO_APP_SERVER` no detector do 29, só para `23-kit.test.mjs`, com motivo; cai se o arquivo
citar login ou harness com modelo. Teste novo da exceção. `harness-real.test.mjs`: 7/7 no ticket-23 e no ticket-24
(e7d38ae) (Fiel). Árvore limpa.
Ressalva: a exceção olha só o texto do arquivo de teste; o kit roda por `pwsh` (não importado), então um login que
entrasse no `08-harnesses.mjs` não derrubaria a exceção. Hoje o kit não copia login (lido na r1).

## Rodada curta (lição do 21, caminho longo) — 2026-10-17 ~11h20 (Fiel sozinho; leitura do Fielzinho pendente)

Ramo `ticket-23`, HEAD e6e5faa (levado ao `ticket-24` 5325a4b por merge). **Veredito: PASSA**, com 1 pedido de
limpeza antes da junção e 2 ressalvas.

- `instalar.ps1`: hub, casa e `.env` pelo `realpathSync.native` (`Longo`). Teste novo do nome curto: nada na casa com
  `~N`, o hub chega no caminho longo. Fiel: `23-kit + harness-real` 22/22.
- **Limpar antes do Rebite:** a worktree `C:/context-hub-wt/ticket-23` tem uma instalação do kit solta na raiz,
  fora do git: `.agents/`, `.claude/` (com `CLAUDE.md` e skills), `.codex/AGENTS.md`, `.copilot/`, `.hub-kit/registro.json`,
  de 10:40 (antes do commit de 10:50). O registro mostra casa e hub = a própria worktree (links para
  `c:\context-hub-wt\ticket-23\agents.md`). Minha rodada dos testes não a recriou (mtime igual). Desfazer pelo kit
  (`instalar.ps1 -Casa C:/context-hub-wt/ticket-23 -Desfazer`) e conferir `git status` limpo.
- Ressalva 1 (a causa provável da sobra): casa vazia vira a pasta atual. `curto('')` no teste devolve `C:\""`
  (conferido: `for %I in ("") do @echo %~sI`), e o `Longo` não confere a saída do node: se o node falhar, `$Casa` fica
  vazia. Melhor: o `Longo` recusar saída vazia ou código ≠ 0, e o teste afirmar `~N` também na casa e no `.env`
  (hoje só no hub).
- Ressalva 2 (do relatório): o `03-busca.ps1` chamado sozinho ainda usa o `Resolve-Path`.
- Fechamento (~11h45): instalação solta desfeita pelo kit, `git status` limpo; guarda do `Longo` em a9643c6 (para o
  kit se o node não devolve caminho). Fiel: `23-kit + harness-real` 22/22. A ressalva 1 saiu; o PASSA segue.

## Leitura do Fielzinho — 2026-10-17

Leitura tardia das rodadas e9dcef7, f304e6c, a419182 e curta a9643c6. Conferidos instalador, Casa, junção dos hooks, aprovação isolada pelo app-server e editor TOML. As correções das rodadas estão presentes. Worktree atual e05b367: esses arquivos e 23-kit.test.mjs sem alteração desde a9643c6. Prova local do kit em andamento, sem Docker, login ou modelo.

### Achado novo 1 — falha entre copiar e registrar pode perder o original no desfazer

**Recomendação: corrigir antes do uso real.** Em `agents/code/kit/par/kit/casa.mjs:88-91`, `guardar(p)` move o original para `.hub-kit/copias`, `fazer()` executa a troca e só depois o registro recebe a cópia. Se a gravação/criação do link falha (por exemplo, falta de espaço ou permissão), a cópia fica sem registro. `desfazer()` processa apenas o registro e apaga toda `.hub-kit` na linha 136, incluindo esse original não registrado. Viola a cópia e o desfazer pedidos pelo ticket.

Repro isolada: `etapas/logs/repro-23-fielzinho.mjs`; saída em `repro-23-fielzinho.log`, código 0. Cria config.txt de ensaio, chama `Casa.mudar` injetando ENOSPC em `fazer`, depois `desfazer`. Resultado: original_no_destino=false; registro=[]; copia_antes=true; original_depois_do_desfazer=false; copia_depois=false. A exceção é injetada; não foi necessário encher disco nem alterar permissões. Só arquivos sintéticos em TEMP, apagados ao fim.

Conserto proposto: tornar a troca recuperável antes de mover o original (registro de operação pendente ou restauração garantida no catch); o desfazer não pode apagar cópias órfãs. Cobrir falha na troca e no registro, com original preservado e recuperação repetível. A classificação final, já na terceira rodada, fica com o Fiel/maestro; não reabri ticket nem alterei código.

### Achado da leitura do Fielzinho, conferido pelo Fiel (~12h35)
- **Perda do original quando a mudança falha no meio** (Fielzinho). `agents/code/kit/par/kit/casa.mjs:88-91`: o
  `mudar` move o original para `.hub-kit/copias` (`guardar`), chama `fazer()` e só depois grava o registro. Se `fazer`
  lança (ENOSPC, EPERM, link recusado), a cópia fica sem registro; o `desfazer` não a acha e, no fim (`:136`), apaga a
  `.hub-kit` inteira: o original some. Reprodução do Fielzinho (`logs/repro-23-fielzinho.log`): `registro=[]`,
  `copia_antes=true`, `original_depois_do_desfazer=false`, `copia_depois=false`. Conferido no código pelo Fiel.
- O 23 já teve duas voltas (r1 e a reabertura); pelo teto, isto seria um passa com ressalva. Como é perda de arquivo
  do usuário no HOME real (ticket 26), o Fiel levou ao maestro: conserto curto antes da junção (devolver a cópia e
  relançar se `fazer` falhar, ou gravar o registro antes de `fazer`; com teste da falha) ou ressalva para o 26.
- O 24 traz o 23 por merge: o mesmo vale para ele.
- **Decisão do maestro (~12h40): conserto curto antes da junção**; perda de arquivo no HOME real não vai como
  ressalva. Pedido ao Cinzel: se `fazer()` falhar, devolver a cópia ao lugar e relançar o erro, com teste da falha
  (ENOSPC/EPERM simulado); depois rodada curta do Fiel, e o 24 traz por merge.

Prova local concluída da leitura tardia: `node --test agents/code/test/23-kit.test.mjs`, **15/15, saída 0**, 263,8 s. A suíte existente não cobre a falha reproduzida acima. Fiel confirmou o achado; decisão do maestro registrada acima: conserto curto antes da junção. Aguardo a ponta corrigida, sem editar código.

Precisão da prova: o teste foi iniciado em e05b367, mas a worktree avançou para 46897e0 durante a execução. Os 15 casos carregados pertencem ao teste anterior; não uso esse resultado como prova integral da ponta corrigida. Leitura e execução focada dos casos novos serão registradas separadamente.

### Conferência curta de 46897e0 pelo Fielzinho

Os dois testes novos passam (2/2, saída 0, filtro `a mudança que falha`). Minha sonda original também passa a preservar o original antes e depois do desfazer; log `repro-23-fielzinho-corrigido.log`.

**O mesmo achado ainda ocorre se falha a gravação do registro.** O try novo cobre `fazer()`, mas `lerRegistro`, `estado(p)` e `writeFileSync(registro.json)` continuam fora. Sonda `logs/repro-23-registro-fielzinho.mjs` injeta ENOSPC somente no writeFileSync do registro após uma troca bem-sucedida: registro=[]; conteúdo antes/depois do desfazer = novo; copia_depois=false. O original foi perdido no desfazer. Saída em `.log`, código 0, TEMP sintético apagado. Não é novo requisito: a recomendação inicial já pedia cobrir falha na troca e no registro. Recomendo proteger a operação completa, inclusive persistência do registro, preservando o original se a recuperação falhar.

## Rodada curta do conserto (46897e0) — 2026-10-17 ~12h55, em acordo Fiel/Fielzinho: **VOLTA** (conserto incompleto)
- Feito: se `fazer()` falha, o `mudar` tira o que ficou pela metade, devolve o original e relança; teste com ENOSPC
  (arquivo) e EPERM (pasta). Fiel: `23-kit + harness-real` 24/24; a repro original do Fielzinho preserva o original.
- **Falta (Fielzinho, conferido pelo Fiel):** a gravação do registro (`fs.writeFileSync(this.arquivoRegistro, ...)`,
  fim do `mudar`) segue fora do `try`. Com ENOSPC ali: a troca fica feita, `registro=[]`, e o desfazer deixa o texto
  novo e apaga a cópia do original (`logs/repro-23-registro-fielzinho.log`). Pior: uma gravação pela metade corrompe o
  `registro.json`, e aí o desfazer perde o registro de tudo.
  Conserto: pôr no `try` tudo depois do `guardar` (a troca e a gravação do registro); se falhar, desfazer a troca e
  devolver o original; gravar o registro por arquivo temporário e `rename` (nunca pela metade); se a própria devolução
  falhar, não apagar a cópia (deixar a `.hub-kit` e dizer onde está). Teste: ENOSPC na gravação do registro.
- É o mesmo conserto mandado pelo maestro (não perder o original); a próxima rodada curta fecha.

## Rodada curta 2 do conserto (488b377) — 2026-10-17 ~13h30 (Fiel sozinho; Fielzinho sem cota até 17h15)

**Veredito: PASSA.** Fecha o conserto mandado pelo maestro.
- `mudar`: a troca e a gravação do registro no mesmo `try`; falhou, tira o que ficou, devolve o original e relança;
  se a devolução falhar, a mensagem diz onde a cópia ficou. `gravarRegistro`: temporário + `rename` (nunca pela
  metade). `desfazer` recusa antes de tocar em nada se há cópia sem registro.
- Fiel: `23-kit + harness-real` 27/27 (casos novos: ENOSPC no registro, inteiro e pela metade; devolução que falha);
  `git status` limpo. As duas repros do Fielzinho contra 488b377: a do `fazer` preserva o original; a do registro
  injetava a falha no caminho antigo (`registro.json`, agora `.novo`) e não disparou, mas o resultado é seguro (o
  desfazer volta o original), e o caso dela está nos testes novos.
- O 24 traz por merge; confiro na rodada dele.

## Rodada curta de junção (2379d38, depois 9fcf4cf) — 2026-10-17 ~16h30 (Fiel + 2ª leitura Sonnet 5.5)

**Junção: PASSA em acordo.** Conflito em `harness-real.test.mjs` resolvido sem perda: ficam a exceção do app-server do
23 (`SO_APP_SERVER`, filtro `!excecao`, teste da exceção estreita) e os dois testes do modelo do 43. `9fcf4cf^2..9fcf4cf`
só acrescenta. 2ª leitura: `23-kit` sozinho 20/20 três vezes; `harness-real` 9/9; árvore limpa, sem sobra no TEMP.

**Achado novo (Fiel), do código do 23, não da junção:** a falha que o Cinzel não registrou é um EPERM intermitente na
troca do registro do kit. `harness-real.test.mjs` + `23-kit.test.mjs` juntos, três vezes: 29/29, 28/29, 28/29 (logs
`logs/revisao-23-juncao-fiel-{1,2,3}.log`), em testes diferentes ("fragmento mudado..." e "a segunda passada não muda
nada"), sempre `passo 08 parou: EPERM: operation not permitted, rename '...\.hub-kit\registro.json.novo' ->
'...\.hub-kit\registro.json'` (`kit/casa.mjs:118`, `gravarRegistro`). O `harness-real` não toca o TEMP do 23: é carga da
máquina mais o Windows segurando o arquivo recém-gravado (antivírus/indexador), caso conhecido do `rename` no Windows
(o graceful-fs repete o rename em EPERM/EACCES por isso). Sozinho, 3 de 3 passam.
Efeito real: na máquina do Gustavo, o kit de par pode parar no passo 08 de vez em quando; o `catch` do `mudar` devolve o
original (seguro), mas a instalação falha e a suíte da junção pode ficar vermelha à toa.
Conserto proposto (curto): repetir o `renameSync` em EPERM/EACCES/EBUSY por pouco tempo (ex.: até ~2 s, com pausa),
no `gravarRegistro` e nas trocas do `guardar`/devolução; teste com um rename que falha EPERM nas primeiras tentativas.
Teto de voltas do 23 já passado: decisão do maestro (conserto curto antes da junção ou ressalva para depois).
Maestro (~16h35): conserto curto antes da junção; rodada curta do Fiel depois.

## Conserto curto ceda444 — 2026-10-17 ~17h25 (Fiel + 2ª leitura Sonnet 5.5)

`renomear` em `kit/casa.mjs:45-59` (até ~2 s, pausa de 100 ms, só EPERM/EBUSY/EACCES) nas quatro trocas (guardar :88,
devolução :119, `gravarRegistro` :134, desfazer :189); nenhum outro rename no kit. 5 testes novos (passageiro nos três
códigos no registro; passageiro ao guardar, devolver e desfazer; EPERM que não passa desiste em ~2 s e o original
volta). Fiel: `harness-real` + `23-kit` juntos 34/34 duas vezes (`logs/revisao-23-conserto-fiel-{1,2}.log`); Cinzel
34/34 três vezes; 2ª leitura: os 5 novos verdes, árvore limpa. **Veredito: PASSA em acordo.** Junção liberada.
