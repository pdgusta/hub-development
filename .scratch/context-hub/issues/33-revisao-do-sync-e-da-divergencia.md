# Revisão do sync e da divergência com o banco

Type: grilling
Status: resolved
Blocked by: 25, 34, 47, 48

## Question

Com o caminho escolhido em "Como a verdade viaja entre as máquinas", o que sobra, muda ou cai em
"Ponto de encontro do sync", "Sync que não depende de quem gravou" e "Divergência e edição
concorrente"? Os três estão resolvidos, mas marcados "em revisão" desde "Markdown: vista ou fonte da
verdade", porque partiam do `.md` levado pelo git. As garantias de "Divergência e edição concorrente"
(o que conta como divergência, aviso, conferência de versão) continuam; o mecanismo é o que se revisa.

## Comments

- 2026-10-06: aberto para que "Passagem para a construção" não use decisões em revisão. Graduado do
  fog "Revisão das decisões apoiadas no Markdown como verdade" do mapa.
- 2026-10-06: o caminho é CouchDB + LiveSync ("Como a verdade viaja entre as máquinas"). Espera
  também "Onde o servidor mora", porque a topologia (servidor numa máquina, mestre-mestre ou VPS)
  muda o que conta como "máquina sem sync" e onde o aviso nasce.
- 2026-10-10 (vinda de "Onde o servidor mora"): S3. Cada par tem o próprio CouchDB e os pares
  replicam direto pela tailnet, sem ponto de encontro. Rever aqui: o que conta como "máquina sem sync"
  (replicação entre pares parada), onde o aviso nasce, o papel que sobra do GitHub e do sincronizador, e
  o termo "Ponto de encontro" do glossário.
- 2026-10-12: ticket reivindicado (wayfinder). Fatos conferidos em fonte primária para a rodada 1:
  - o LiveSync junta sozinho mudanças em trechos diferentes da mesma nota quando o banco ainda tem a
    revisão comum; pergunta ao usuário quando os trechos se sobrepõem, quando um lado apaga o que o
    outro mudou, ou quando a revisão comum já foi compactada
    ([specs_conflict_resolution.md](https://raw.githubusercontent.com/vrtmrz/obsidian-livesync/main/docs/specs_conflict_resolution.md));
  - o CouchDB mostra o estado de cada replicação em `_scheduler/docs` (`running`, `pending`,
    `crashing` com novas tentativas, `failed` terminal), com `error_count` e `last_updated`
    ([replicator.rst](https://raw.githubusercontent.com/apache/couchdb/main/src/docs/src/replication/replicator.rst));
  - o CLI do LiveSync tem o modo `daemon` ("Run mirror scan then continuously sync CouchDB <-> local
    filesystem"), mas a instalação documentada é só systemd; no Windows, **não verificado**
    ([CLI README](https://raw.githubusercontent.com/vrtmrz/obsidian-livesync/main/src/apps/cli/README.md)).
- 2026-10-12: rodada 1 na nota "Rodada atual": R60 o papel que sobra do GitHub (recomendação: cópia
  de segurança diária da vista `.md`, um ramo por par); R61 quem liga disco e banco com o Obsidian
  fechado (recomendação: Obsidian sempre aberto, `daemon` do CLI como evolução depois de teste); R62
  quem dispara a replicação (recomendação: cada par empurra as próprias mudanças, para o aviso nascer
  em quem travou); R63 o que conta como par sem sync (recomendação: outro par ligado na tailnet e
  replicação parada há mais de 15 min; outro par desligado só informa); R64 onde o aviso nasce
  (recomendação: vigia agendada em cada par, notificação do Windows e estado lido pela checagem de
  sessão); R65 colisão (recomendação: aceitar o LiveSync, que segura só a nota em colisão; "parar
  tudo" cai; conflito aberto no banco conta como divergência); R66 conferir a versão ao gravar
  (confirmação: garantia fica, mecanismo é o MCP modificado e o LiveSync como escritor do disco); R67
  se as duas máquinas ficam ligadas ao mesmo tempo (sem isso, a replicação direta não anda).
- 2026-10-12, respostas da rodada 1:
  - **R60, B (a contragosto):** o GitHub vira cópia de segurança diária da vista, um ramo por máquina.
    O Gustavo: "de um jeito ou de outro vou ter que ter um .git na raíz. Então opção B mesmo.
    Infelizmente, porque queria evitar ficar tendo que gerenciar um repo privado que praticamente não
    vou usar. a própria sincronização já vai acabar sendo a cópia de segurança". Contraponto que
    sustentou a B: a replicação leva um estrago às duas máquinas em segundos, e a compactação apaga o
    histórico. Consequências: o `.git` na raiz não replica (pastas com ponto ficam fora do LiveSync,
    "Testes das portas de entrada"), então cada máquina tem o seu; o git só faz commit e push, nunca
    pull nem checkout, e não é escritor do disco. Achado de passagem: com `.git` na raiz, Codex e
    Copilot numa subpasta passam a achar a raiz ("Portas de entrada: pesquisa" apontou a falta de
    `.git` como causa); insumo para "Acesso dos agentes: decisão".
  - **R61, aberta:** o Gustavo trouxe arquivos que não são `.md` (também quer no banco) e momentos com
    o Obsidian fechado em que o conteúdo, `.md` ou não, deve chegar ao CouchDB mesmo assim; pede
    alternativa ao plugin. Fatos conferidos depois (documentação do LiveSync): o plugin pula arquivos
    acima de `syncMaxSizeInMB` e os que casam a expressão de exclusão; pastas com ponto só pelo
    "Hidden File Sync", recurso à parte; arquivo binário não tem junção automática (colisão é sempre
    escolher um lado). O CLI tem o modo `daemon` com observador de arquivos (chokidar) e
    `.livesync/ignore`; ao reconciliar, pula documentos em conflito. **Não verificado:** se o plugin
    leva todo tipo de arquivo comum ou só os que o Obsidian reconhece; o `daemon` no Windows; plugin e
    `daemon` na mesma pasta. Segue na rodada 2.
  - **R62, B:** cada máquina dispara a replicação das próprias mudanças para a outra; o notebook passa a
    receber conexão, só pela tailnet. Muda a inferência de "Onde o servidor mora" (as duas tarefas no
    notebook).
  - **R63, "ok" (B, 15 min):** máquina sem sync é a outra estar ligada na tailnet e a replicação não
    rodar há mais de 15 min; com a outra desligada não é divergência, e a checagem de início de sessão
    informa a hora da última troca, sem alarme.
  - **R64, "ok" (A), mais "seria bom ter isso como claude mod 'persistente'":** vigia em cada máquina
    (tarefa agendada a cada 5 min, lê o CouchDB local e se o Obsidian está aberto, grava o estado que a
    checagem lê, notificação do Windows quando piora); e um mod do Claude Code que mostra o estado da
    vigia o tempo todo na sessão (forma, se linha de status ou faixa acima do prompt, na construção).
  - **R65, "ok" (A):** aceita o LiveSync; colisão segura só a nota; "parar tudo" cai; conflito aberto
    no banco conta como divergência até ser resolvido.
  - **R66, "ok":** a conferência de versão fica como garantia; mecanismo no banco é o MCP modificado,
    e o escritor extra do disco é o LiveSync.
  - **R67, A:** as duas máquinas geralmente ficam ligadas juntas; a replicação direta basta.
- 2026-10-12: glossário atualizado com a rodada 1: "Ponto de encontro" saiu; "Colisão real" e
  "Divergência" redefinidas sem o git. "Sincronizador" espera a R69.
- 2026-10-12: rodada 2 na nota "Rodada atual": R68 que arquivos além do `.md` vivem no banco
  (recomendação: todo arquivo comum até um limite, sugestão 50 MB, fora pastas com ponto e a lista de
  exclusão); R69 disco e banco com o Obsidian fechado, com três jeitos de montar com o CLI do LiveSync
  (os dois sempre ligados; revezamento pela vigia; só o CLI, sem plugin) (recomendação: abrir pesquisa
  com teste curto, "Disco e banco sem o Obsidian", e este ticket espera).
- 2026-10-12, respostas da rodada 2:
  - **R68, A, com pergunta:** todo arquivo comum até um limite de tamanho (sugestão 50 MB) vai ao
    banco; ficam fora as pastas com ponto e a lista de exclusão. O Gustavo: "eu quero saber o por que
    binário é um problema, limite do couchdb e impacto". O limite final espera a pesquisa e o teste.
  - **R69, A:** "ok. E nesse teste quero ver isso tudo também com um teste do r68 além de pesquisa na
    documentação". Abertos "Disco e banco sem o Obsidian: pesquisa" e "Teste: disco e banco sem o
    Obsidian" (este depois da pesquisa, quando o Gustavo disser "pode iniciar"). Este ticket fica
    travado nos dois; a escolha entre os três jeitos (os dois sempre ligados, revezamento, só o CLI) e o
    termo "Sincronizador" do glossário voltam aqui com o resultado.
- 2026-10-12: "Disco e banco sem o Obsidian: pesquisa" resolvida. **Correção do que a rodada 2 disse**
  ("binário em colisão: escolher um lado"): no LiveSync 1.0 a colisão de binário é resolvida sozinha
  pelo `mtime` mais novo, mesmo com "Always overwrite with a newer file" desligado, e o outro ramo vira
  revisão apagada (conferido em `docs/specs_conflict_resolution.md`: "This is existing behaviour, not a
  new 1.0 guarantee"). Isso fere "nada diverge em silêncio" para binários e volta aqui como pergunta
  depois do teste (aceitar, aviso da vigia, ou forçar escolha explícita). Outros fatos que pesam na R68:
  o plugin só leva o que o Obsidian enxerga (docx, xlsx, csv pedem "Detect all file extensions"); o
  limite padrão é 50 MiB; versões de binário acumulam pedaços que a compactação não remove (só o GC V3,
  beta e manual).
- 2026-10-13: "Teste: disco e banco sem o Obsidian" resolvido; os dois bloqueios novos fecharam. Volta
  para cá, para a rodada 3: escolher entre os três jeitos (o teste recomenda plugin e CLI sempre ligados,
  o CLI como tarefa agendada; o revezamento cria conflito falso); fixar o que vai ao banco (o plugin leva
  qualquer arquivo; `.py` e `.json` viram binário, sem junção); o limite e o arquivo que passa dele sem
  aviso; a colisão de binário que some em silêncio (a versão perdida só volta por script); as pastas com
  ponto aninhadas que o CLI vaza na partida; o Config Doctor que para o sync; e reescrever
  "Sincronizador" no glossário.
- 2026-10-13: rodada 3 na nota "Rodada atual", com base no teste: R70 o jeito de ligar disco e banco
  (recomendação: plugin e CLI sempre ligados, o CLI como tarefa agendada); R71 a colisão de binário que
  some em silêncio, inclusive `.py` e `.json` (recomendação: a vigia avisa e a versão perdida é
  recuperada por script); R72 o arquivo acima do limite (recomendação: 50 MiB, a vigia lista, e conta
  como divergência); R73 pastas com ponto aninhadas (recomendação: regra de exclusão e código fora do
  hub); R74 a nova definição de "Sincronizador" no glossário.
- 2026-10-13, respostas da rodada 3:
  - **R70, A:** plugin e CLI sempre ligados; o CLI como tarefa agendada (logon mais repetição curta, sem
    segunda instância) é o elo permanente entre disco e banco; o plugin fica no Obsidian quando aberto. O
    Gustavo: "A infelizmente pois manter o obsidian sempre aberto é um custo. Futuramente vou querer
    aprimorar isso." **Mal-entendido a desfazer:** no jeito A o Obsidian não precisa ficar aberto (o CLI
    cuida do disco); isso volta na rodada 4.
  - **R71, A:** a vigia acha os ramos apagados pela resolução automática de binário, avisa, e um comando
    recupera a versão perdida para um arquivo ao lado; conta como divergência até o Gustavo olhar.
  - **R72, C:** subir o limite **e** a vigia listar o que passar dele, contado como divergência. O valor
    fica para a rodada 4.
  - **R73, "ok" (A):** regra que ignora pastas com ponto em qualquer nível, no CLI e no plugin (testar na
    construção), e o contrato diz que repositório de código mora fora do hub.
  - **R74, "ok":** nova definição de "Sincronizador" (glossário atualizado).
- 2026-10-13: rodada 4 na nota "Rodada atual": R75 esclarecimento de que no jeito A o Obsidian pode
  ficar fechado (o CLI cuida do disco; o plugin só para ver, editar e a janela de conflito; conflito com o
  Obsidian fechado aparece pela vigia); R76 o novo limite de tamanho (recomendação: 100 MiB, comportamento
  acima de 50 MiB a conferir na construção).
- 2026-10-13, respostas da rodada 4:
  - **R75, "ok":** no jeito A o Obsidian pode ficar fechado; o CLI cuida do disco o tempo todo, o plugin só
    serve para ver, editar e a janela de conflito, e conflito com o Obsidian fechado aparece pela vigia.
    O "aprimorar no futuro" da R70 deixa de ser sobre o Obsidian aberto.
  - **R76, B:** limite de **200 MiB** (`syncMaxSizeInMB` no CLI e no plugin); a vigia lista o que passar
    dele. Acima de 50 MiB não foi testado: conferir na construção.
- Pelo que vejo, a árvore deste ticket fechou. Rodada 5 (confirmação do resumo) aberta na nota; a
  resolução fica para a próxima sessão, porque esta já resolveu "Teste: disco e banco sem o Obsidian".
- 2026-10-13: glossário: "Divergência" passou a incluir a colisão de binário resolvida sozinha (até o
  Gustavo ver) e o arquivo que não viaja por passar do tamanho máximo. Rodada 5 na nota "Rodada atual":
  R77, confirmação do resumo do ticket (o que sai, como as mudanças viajam, divergência, aviso,
  conferência de versão, pontos para a construção). Próximo passo ao retomar: com o "sim", escrever o
  Answer a partir do resumo da R77, resolver, apontar no mapa, comentar nos tickets 06, 07 e 08, e pedir
  ao Designer a atualização do system-design.html.
- 2026-10-13, resposta da rodada 5: **R77, "ok"**: o resumo confere (texto da rodada 5, reproduzido no
  Answer quando o ticket for resolvido). Entendimento comum alcançado; a resolução fica para a próxima
  sessão (um ticket resolvido por sessão).

## Answer

**As garantias de "Divergência e edição concorrente" ficam; o mecanismo passa do git para o CouchDB +
LiveSync, com um sincronizador de linha de comando e uma vigia em cada máquina.** Resumo confirmado
pelo Gustavo em 2026-10-13 (R77, "ok"), a partir das rodadas 1 a 4 (R60 a R76) acima.

- **O que sai:** o GitHub como ponto de encontro e o termo "Ponto de encontro" do glossário; o
  sincronizador baseado em git (commit, busca e junção a cada 15 min); a regra "colisão para a máquina
  inteira, com a junção desfeita".
- **Como as mudanças viajam:**
  - cada máquina tem o próprio CouchDB e envia as próprias mudanças à outra pela tailnet (R62); as duas
    máquinas costumam ficar ligadas juntas, e a replicação direta basta (R67);
  - **sincronizador:** o CLI do LiveSync como tarefa agendada (no logon, repetindo a cada poucos minutos,
    uma instância só). Liga disco e banco o tempo todo, pega o que qualquer agente grava no disco e não
    depende do Obsidian aberto (R70, R75);
  - **Obsidian com o plugin:** só para ver, editar ou resolver conflito; pode ficar fechado (R75);
  - **o que vai ao banco:** todo arquivo comum até 200 MiB (`syncMaxSizeInMB` no CLI e no plugin). Só
    `.md`, `.txt` e `.csv` são texto, com junção automática; o resto é binário (R68, R76);
  - **fora do banco:** pastas com ponto em qualquer nível, por regra de exclusão no CLI e no plugin; o
    contrato diz que repositório de código mora fora do hub (R73);
  - **GitHub:** cópia de segurança diária da vista, com um `.git` na raiz de cada máquina (não replica),
    um ramo por máquina, só commit e push; o git nunca faz pull nem checkout e não é escritor do disco
    (R60, escolhida a contragosto: a replicação leva um estrago às duas máquinas em segundos, e a
    compactação apaga o histórico).
- **Divergência** (glossário atualizado):
  - colisão real ainda não vista pelo Gustavo: trechos sobrepostos, um lado apaga o que o outro mudou, ou
    falta a versão comum. Texto segura só aquela nota e abre a janela de conflito; conflito aberto conta
    até ser resolvido (R65). Binário fica com a versão de `mtime` mais novo; a vigia acha o ramo apagado,
    avisa e um comando recupera a versão perdida para um arquivo ao lado (R71);
  - máquina que não leva as próprias mudanças à outra há mais de 15 min, com a outra ligada na tailnet.
    Com a outra desligada não é divergência: a checagem de início de sessão informa a hora da última
    troca (R63);
  - arquivo acima de 200 MiB, que não viaja; a vigia lista (R72, R76).
- **Aviso:** uma vigia em cada máquina, tarefa agendada a cada 5 min. Lê o estado das replicações
  (`_scheduler/docs` do CouchDB), conflitos abertos, binários descartados, arquivos acima do limite, se o
  sincronizador está vivo e se o Config Doctor travou o plugin. Notificação do Windows quando piora; um
  estado curto que a checagem de início de sessão lê; e um mod do Claude Code que mostra esse estado o
  tempo todo na sessão (forma, linha de status ou faixa acima do prompt, na construção) (R64).
- **Conferir a versão ao gravar** (fica): no banco, pelo MCP modificado (a gravação leva a versão lida e
  vira conflito se ela mudou). No disco, os escritores extras são o sincronizador e o plugin (R66).
- **Fica para outros tickets:**
  - como cada agente confere a versão ao gravar no disco ("Como os agentes gravam no hub");
  - o `.git` na raiz pode levar Codex e Copilot numa subpasta até o `AGENTS.md` sem marcador, não
    testado com o hub; e o mod da vigia ("Acesso dos agentes: decisão");
  - a busca sobre a vista `.md`: com o sincronizador sempre ligado, a vista de cada máquina fica viva com
    o Obsidian fechado ("Camada de busca");
  - "aprimorar no futuro" da R70 fica sem objeto, já que o Obsidian pode ficar fechado.
- **Para a construção** ("Passagem para a construção"): configurar o sincronizador pelo caminho dos
  testes oficiais e aceitar cada máquina nova com `mark-resolved`; subir o sincronizador antes do plugin;
  testar a regra de pastas com ponto e o comportamento acima de 50 MiB; o mod da vigia no Claude Code.
- **Decisões revisadas:** "Ponto de encontro do sync" (o GitHub vira só cópia de segurança; as deploy
  keys por máquina ficam), "Sync que não depende de quem gravou" (o git-sync sai; o sincronizador é o CLI
  do LiveSync) e "Divergência e edição concorrente" (garantias ficam, mecanismo trocado como acima).
