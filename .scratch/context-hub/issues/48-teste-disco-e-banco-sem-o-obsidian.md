# Teste: disco e banco sem o Obsidian

Type: task
Status: resolved
Blocked by: 47

## Question

Teste curto na montagem do spike (`C:\Projetos\spike-livesync\`, conteúdo de teste, sem dado de
cliente), com os itens "Precisa de teste" de "Disco e banco sem o Obsidian: pesquisa", no mínimo:

1. **Arquivos além do `.md` (R68):** PDF, imagem, docx, CSV e um arquivo perto e outro acima do limite de
   tamanho, gravados no disco de um cofre: chegam ao banco? descem no outro cofre? Uma colisão de binário,
   como aparece e como se resolve. Tamanho do banco antes e depois, e depois de editar o binário algumas
   vezes e compactar.
2. **CLI do LiveSync em modo contínuo no Windows, com o Obsidian fechado:** edição de `.md` e de binário no
   disco chega ao banco e ao outro cofre; o que vem do banco desce ao disco; conflito.
3. **Os dois sempre ligados** (plugin no Obsidian e CLI) na mesma pasta: algum grava por cima, duplica ou
   entra em ciclo?
4. **Revezamento:** CLI ligado com o Obsidian fechado e desligado quando ele abre; nada se perde na troca?

Resultado: relatório curto com o que funcionou, o que falhou, o preço de cada um dos três jeitos (os dois
sempre ligados; revezamento; só o CLI, sem plugin) e uma recomendação. Insumo de "Revisão do sync e da
divergência com o banco". Aprovado pelo Gustavo em 2026-10-12 (R69); instala e roda software nesta
máquina, então começa quando ele disser "pode iniciar".

## Comments

- 2026-10-12: "Disco e banco sem o Obsidian: pesquisa" resolvida; a seção "Precisa de teste" de
  [`pesquisa-47-disco-e-banco-sem-o-obsidian.md`](../../../exploracao/anexos/pesquisa-47-disco-e-banco-sem-o-obsidian.md)
  tem 16 itens, que entram aqui junto dos quatro acima. Incluir: colisão de binário (a pesquisa diz que
  o `mtime` mais novo vence sozinho) e onde achar a versão perdida; "Detect all file extensions" no
  Obsidian; o `daemon` instalando e rodando no Windows (LevelDB nativo).
- 2026-10-12 23:50: iniciado (Gustavo: "pode iniciar"). Montagem do spike de pé (`docker compose up -d`);
  auxiliar `C:\Projetos\spike-livesync\cdb.py` (lê a credencial do `.env` por dentro, sem imprimir).
  Estado inicial: 47 documentos, 32 pedaços `h:`, banco com 1,04 MB em disco; plugin nos dois cofres com
  Sync Mode LiveSync, `syncMaxSizeInMB` 50, `customChunkSize` 0, sem E2EE. Uma nota de teste antiga já
  está em conflito (`initiatives/_archive/x/nota-2.md`, de outro teste); fica como está.
- 2026-10-12 23:55, **item 1, extensões no plugin:** com "Detect all file extensions" **desligado**
  (`showUnsupportedFiles` ausente no `app.json`, padrão `false`, conferido no `obsidian.asar`), os onze
  arquivos copiados para `cofre-a/teste/` (`.pdf`, `.png`, `.docx`, `.xlsx`, `.zip`, `.csv`, `.py`,
  `.json`, `.bin`, `.txt`, `.exe`) chegaram ao banco em menos de 10 s e desceram ao cofre B com bytes
  idênticos (sha256). **Contradiz a pesquisa** (que dizia que docx, xlsx, zip e csv só entram com a
  opção ligada): na 1.0.35 o plugin leva qualquer arquivo comum. Tipo no banco: `.md`, `.txt`, `.csv`
  como `plain` (texto, com junção); **todo o resto, inclusive `.py` e `.json`, como `newnote`**
  (binário, sem junção automática). O "Config Doctor" abriu de novo nos dois cofres ao abrir
  ("Enhance chunk size"); ficou sem resposta, e o sync seguiu.
- 2026-10-12 23:55, **item 2, limite de tamanho (`syncMaxSizeInMB` 50):** o limite é em MiB. Um arquivo
  de 49 MiB (51,4 MB) subiu em 502 pedaços de ~100 KiB e desceu íntegro ao B; o banco foi de 1,16 MB a
  70,3 MB em disco (68,6 MB de dados externos: **Base64, +33%** sobre os 51,4 MB). Um de 51 MiB ficou
  fora do banco e do B **sem aviso visível** no Obsidian (só a barra de status com a contagem).
  **Arquivo que cresce além do limite:** o de 49 MiB, aumentado para 52 MiB no A, **não subiu**; o banco
  e o B ficaram com a versão de 49 MiB, sem aviso: divergência silenciosa entre os cofres. A vigia
  precisa listar arquivos acima do limite. O explorador do Obsidian só mostra PDF e PNG; os outros
  arquivos estão no disco e no banco, mas invisíveis na árvore.
- 2026-10-13 00:00: apagar no A o arquivo de 52 MiB (acima do limite, com a versão de 49 MiB no banco)
  **propagou** a exclusão ao B; os 502 pedaços ficaram no banco, e a compactação não liberou nada
  (68,6 MB de dados externos antes e depois). Achado de passagem: `chunkSplitterVersion` é
  `v3-rabin-karp` (pedaços definidos pelo conteúdo, não fixos), o que muda a inferência da pesquisa sobre
  versões de binário (item 5 mede).
- 2026-10-13 00:00, **itens 3 e 4 em curso:** B fechado (WM_CLOSE na janela, sem mexer em mouse ou
  teclado); `amostra.docx` e `amostra.csv` (linha 2) editados no A (subiram, rev 2) e depois no disco do B
  fechado, com conteúdo diferente e data mais nova. Ao reabrir, o B **não sincroniza** enquanto o modal do
  "Config Doctor" ("Enhance chunk size") está aberto: a barra fica "↑0 ↓0" e o banco não recebe nada.
  Marcar `doctorProcessedVersion` no `data.json` com o B fechado não impediu o modal. Aguardando o
  Gustavo clicar no modal do B. Achado para a construção: depois de atualizar o plugin, o sync de um
  cofre pode ficar parado até alguém responder ao Doctor; a vigia precisa pegar isso.
- 2026-10-13 00:05: o Gustavo clicou "No, and do not ask again until the next release" no Doctor do B;
  o B sincronizou na hora.
- **Item 3, colisão de binário (`amostra.docx`):** **confirmado o que a pesquisa disse.** Sem modal,
  sem faixa, sem contador: a versão do B (data mais nova) venceu sozinha, desceu ao disco do A, e a versão
  do A virou um ramo apagado (`3-38b3…`, filho da `2-5b16…` do A). **A versão perdida é recuperável por
  script**, antes e depois da compactação: o ramo apagado é uma folha e guarda a lista de pedaços; o
  `cdb.py` remontou o docx do A ("amostra docx: versão da máquina A"). Pela pesquisa, o GC V3 removeria
  esses pedaços (não testado). Para o Gustavo, a perda é invisível.
- **Item 4, colisão de `.csv`:** comporta-se como `.md`: o modal "Conflicting changes" abriu sozinho nos
  dois cofres (diff por caractere, "Use Base", "Use Conflicted", "Concat both", "Not now"), contador "1"
  na barra, cada disco com a sua versão, as duas folhas no banco. Modal deixado aberto.
- **Item 5, custo em espaço de versões de binário:** docx de 10,9 MB (imagem de ruído, incompressível)
  salvo cinco vezes no A, mudando só o texto. Banco em dados externos: 68,7 → **83,3 MB na 1ª versão
  (+14,6 MB, Base64)**, depois **+0,23 MB por versão** (3 pedaços novos cada), 84,2 MB na 5ª. **Corrige a
  inferência da pesquisa:** com o divisor `v3-rabin-karp` (pedaços pelo conteúdo), a parte do arquivo que
  não muda reaproveita os pedaços. Ressalva: o docx foi gerado com python-docx, que regrava a imagem com
  os mesmos bytes; um salvamento do Word ou do Excel pode reembaralhar o zip (**não verificado**). A
  troca de `customChunkSize` de 0 para 60 não foi testada (o ganho medido tira a prioridade).
- **Item 6, CLI no Windows, instalação:** `git clone` do commit `14141446` (o mesmo da pesquisa), `npm
  install` na raiz (832 pacotes, 2 min, com Node 24) e `npm run build -w self-hosted-livesync-cli` (19 s):
  **funcionou sem compilador**; o LevelDB traz binário pronto para `win32-x64`. `--help` roda. Banco local
  em `cli-db\`, fora do cofre.
- **Item 12, CLI como dispositivo novo:** configurar copiando campos do `data.json` do plugin **não
  serve** (a conexão do plugin fica cifrada e o `sync` falha calado com `no-active-replicator`; o motivo só
  apareceu com uma linha de log posta no build de teste). O caminho que funcionou é o dos testes oficiais
  (`test/test-helpers.sh`): `init-settings --force` e só os campos `couchDB_*`, `liveSync`, `isConfigured`.
  Aí o servidor recusou: **"The remote database is locked and this device is not yet accepted"**. Um
  `mark-resolved` (aceita este dispositivo sem destravar o banco para os outros) resolveu, e o `sync`
  baixou tudo. Não houve aviso de configuração divergente.
- **Item 7, `daemon` contínuo, Obsidian fora (cofre C, só o CLI):** a varredura de partida encheu a pasta
  vazia (14 arquivos, binários íntegros; pulou 12 notas apagadas no banco por teste antigo e o `.csv` em
  conflito). **Depois da partida, nos dois sentidos, em ~2 s:** nota e PNG novos no C chegaram ao A e ao
  B; nota nova no A chegou ao C; edição e exclusão no C chegaram ao A e ao B. **O defeito da #847 não
  apareceu.** **CouchDB parado com o `daemon` rodando:** o processo seguiu vivo (log "fetch failed"), a
  nota gravada no C nesse intervalo chegou ao A e ao B 7 s depois de o CouchDB voltar. **Parada abrupta
  (kill) e volta:** edições feitas no C e no A durante a parada foram trocadas na partida seguinte, nos
  dois sentidos. Ctrl+C não foi testado (processo em segundo plano; o kill é o caso pior).
- **Item 8, pastas com ponto:** com o `daemon` rodando, `projeto/.venv`, `projeto/.git` criados no C
  ficaram fora. **Na varredura de partida, as aninhadas vazaram:** `projeto/.git/HEAD`,
  `projeto/.venv/x.txt` e `projeto/.cache/y.txt` foram ao banco, e **o plugin as gravou no disco do A e do
  B**. Confirma a suspeita da pesquisa. Pastas com ponto **no primeiro nível** (`.git/HEAD`,
  `.oculta/z.txt` na raiz do C) ficaram fora também na partida: o `.git` da raiz do hub (cópia de
  segurança) está a salvo. Para a construção: um `.livesync/ignore` com `**/.*/**` ou equivalente
  (não testado), ou repositórios fora do hub.
- **Item 13, conflito de texto com o CLI:** mesma linha de `do-c.md` mudada no A (plugin) e no C (CLI
  parado), e o CLI religado: o banco guardou as duas folhas; A e B ficaram com a versão do A, o C com a
  sua; o CLI só registrou no log `conflict(s) found` (sem interface); o plugin pôs o conflito na fila do
  modal nos dois cofres (contador 2).
- **Item 14, os dois sempre ligados no cofre A** (plugin com o Obsidian aberto e um segundo `daemon`,
  banco local `cli-db-a`, aceito com `mark-resolved`):
  - **Na partida, o CLI refez a raiz de 8 documentos** que não conhecia: criou uma revisão `1-` nova com o
    mesmo conteúdo e apagou o ramo antigo (comportamento descrito na especificação de conflitos: arquivo
    sem registro de proveniência vira "fresh independent root"). Conteúdo intacto, mas o histórico comum
    se perde, e com ele a base da junção automática desses arquivos.
  - Depois disso, **sem defeito visto:** edição no disco do A (como agente) gerou uma revisão; `write_note`
    e `edit_note` (append) pelo MCP chegaram aos três discos; rajada de 5 gravações com 0,3 s de intervalo
    e um docx salvo juntos terminaram sem conflito, os três cofres idênticos; 60 s parados sem nenhuma
    revisão nova (sem ciclo).
  - O MCP precisou de `docker restart` depois que o CouchDB caiu e voltou (já visto no spike).
- **Item 10, cópia grande para dentro do cofre com o CLI rodando:** arquivo de 40 MiB copiado para o C
  subiu numa revisão só, com o tamanho inteiro, e chegou íntegro ao B (sha256 igual). Nenhuma versão
  pela metade. Só a cópia local foi testada; a vinda do OneDrive não.
- **Item 15, revezamento, primeira metade:** Obsidian do A fechado e só o CLI no A: edição, exclusão
  (`amostra.zip`) e gravação do MCP chegaram aos três discos. **Troca para o plugin:** CLI do A parado
  (kill), uma linha gravada no B e outra no A, Obsidian do A reaberto: **o A não sincronizou** porque o
  Config Doctor abriu no A ("↑0 ↓0"), como antes no B. Aguardando o clique do Gustavo para concluir.
- **Item 15, revezamento, conclusão (depois do segundo clique do Gustavo no Doctor, agora no A):**
  - **CLI → plugin: conflito falso.** `teste/revezamento.md` foi criado pelo MCP e baixado ao disco do A
    pelo CLI, com o Obsidian do A fechado; o A **não** o editou. Com o CLI parado, o B acrescentou uma
    linha; ao reabrir o Obsidian do A, o plugin, sem registro de proveniência para a cópia em disco, a
    gravou como raiz independente (`1-db60…`) e **abriu conflito** com a versão do B (`2-b817…`). O disco
    do A ficou com o texto velho; B e C com a linha nova. A edição real feita no A com nada ligado
    (`do-a.md`) entrou sem conflito.
  - **Plugin → CLI: sem conflito.** Uma linha do B baixada pelo plugin do A, Obsidian do A fechado, CLI do A
    religado com o banco local que já tinha: nenhuma revisão nova, nenhum conflito novo.
  - Conclusão do item: o revezamento cria conflito falso em todo arquivo que o CLI baixou e que mudou no
    banco antes de o plugin voltar. Cada cliente guarda a própria proveniência; um não conhece o que o
    outro gravou no disco.
- **Item 9, CLI como tarefa agendada** (`teste48-livesync-cli`, registrada por XML, sob demanda,
  `cmd /c node … >> logs\tarefa.log`; **apagada no fim**):
  - Rodou e sincronizou (nota gravada no C chegou ao B).
  - **"Reiniciar se falhar" (`RestartOnFailure`, 1 min, 3 vezes) não religa** um processo que morre: depois
    do kill, ficou parado 154 s ("último resultado" 0xFFFFFFFF).
  - **O que funcionou:** gatilho repetido a cada 1 min com `MultipleInstancesPolicy=IgnoreNew`. Depois do
    kill o processo voltou em 50 s, com uma instância só.
  - **CouchDB fora na partida:** o `daemon` sai ("[Daemon] Initial replication failed, cannot continue"); com
    o gatilho de minuto, voltou sozinho quando o CouchDB voltou, e a nota seguinte chegou ao B.
  - Para a construção: gatilho no logon mais repetição de poucos minutos, `IgnoreNew`, e a vigia
    conferindo se o processo vive.
- **Item 11, E2EE com o CLI** (banco separado `obsidian-e2ee`, dois dispositivos só CLI, `encrypt`,
  E2EE v2, metadados internos cifrados e caminho ofuscado): no servidor, cada documento aparece com
  caminho cifrado e `size`, `mtime` e `children` zerados; nenhum texto claro em nenhum documento
  (busca por trechos do conteúdo e dos nomes). **O segundo dispositivo remontou os arquivos com bytes
  idênticos**, e edições depois da partida foram nos dois sentidos em ~2 s. O "metadado vazio" da #835 é,
  neste teste, o desenho da cifra, não perda. Plugin com E2EE não testado.
- 2026-10-13 00:45: montagem devolvida ao estado inicial (Obsidian fechado, `docker compose stop`,
  nenhuma tarefa agendada, nenhum processo do CLI). Ficam em `C:\Projetos\spike-livesync\`: `livesync-src`
  (build), `cli-db*`, `e2ee-db-*`, `cofre-c`, `cofre-e1`, `cofre-e2`, `amostras`, `logs`, `telas` e os
  scripts `cdb.py`, `gera.py`, `tela.ps1`, `janela.ps1`, `tarefa-cli.xml`. O build do CLI tem uma linha de
  log a mais no `sync` (só nesta cópia). Itens 16 (`livesync-bridge`) e a troca de `customChunkSize` não
  foram testados.

## Answer

Teste de 2026-10-12 23:50 a 2026-10-13 00:45, na montagem do spike (CouchDB 3.5.2, plugin LiveSync
1.0.35, CLI do commit `14141446` construído no Windows), com conteúdo de teste. Detalhe e evidências nos
comentários acima.

**R68, arquivos além do `.md`**
1. O plugin leva **qualquer arquivo comum**, com "Detect all file extensions" desligado (a pesquisa
   errou aqui). Só `.md`, `.txt` e `.csv` são texto, com junção; **`.py`, `.json` e todo o resto são
   binário**, sem junção.
2. Limite de 50 **MiB**. Acima dele o arquivo fica fora **sem aviso**, e um arquivo que já estava no banco
   e cresce além dele **para de sincronizar em silêncio** (a outra máquina fica com a versão velha).
3. Espaço: Base64 custa +33% na primeira versão; **versões seguintes reaproveitam pedaços** (divisor por
   conteúdo): docx de 10,9 MB custou 14,6 MB e depois +0,23 MB por versão. Apagar o arquivo não libera os
   pedaços, nem com compactação (só a limpeza manual, não testada).
4. **Colisão de binário: a versão de data mais nova vence sozinha, sem aviso nenhum.** A perdida fica num
   ramo apagado, recuperável por script, também depois da compactação. `.csv` em colisão abre o modal
   como `.md`.
5. Achado lateral: depois de atualizar o plugin, o **Config Doctor abre e o sync daquele cofre fica parado**
   até alguém responder (aconteceu nos dois cofres).

**R69, disco e banco com o Obsidian fechado: o CLI**
6. Constrói e roda no Windows sem compilador. Dispositivo novo é recusado ("not yet accepted") até um
   `mark-resolved`. Configurar copiando o `data.json` do plugin não funciona; o caminho é o dos testes
   oficiais.
7. `daemon`: edições, exclusões e gravações do MCP nos dois sentidos em ~2 s; sobrevive ao CouchDB
   caindo no meio e a kill; cópia de 40 MiB sobe inteira; com E2EE, funciona e não vaza texto claro.
8. **Defeito:** na varredura de partida, **pastas com ponto aninhadas** (`projeto/.git`, `.venv`) vão ao
   banco e o plugin as grava nas outras máquinas. As do primeiro nível (o `.git` da raiz) ficam fora.
9. Como serviço: "reiniciar se falhar" do Agendador não religa o processo; **gatilho repetido a cada
   minuto com "não abrir segunda instância" religou em até 1 min**, inclusive depois do CouchDB fora na
   partida (o `daemon` sai nesse caso).

**Os três jeitos**

| Jeito | Resultado | Preço |
|---|---|---|
| 1. Plugin e CLI sempre ligados na mesma pasta | Sem ciclo, sem conflito, rajadas e MCP limpos | Na primeira partida, o CLI refaz a raiz dos arquivos que não conhece (histórico comum perdido, uma vez); dois processos e dois bancos locais por máquina |
| 2. Revezamento (CLI só com o Obsidian fechado) | Funciona, mas **cria conflito falso** em todo arquivo que o CLI baixou e que mudou antes de o plugin voltar | Conflitos frequentes sem edição real |
| 3. Só o CLI, Obsidian sem plugin | O elo disco-banco mais simples e sempre ligado | Some o modal de conflito; conflito só aparece no log do CLI; a tela de três vias planejada perde a casa |

**Recomendação:** o jeito 1. O CLI como tarefa agendada (logon mais repetição curta) é o elo permanente
entre disco e banco; o plugin fica no Obsidian quando ele está aberto, como interface e modal de conflito.
Para a construção: subir o CLI primeiro em cada máquina, para o refazer da raiz acontecer só uma vez;
excluir pastas com ponto aninhadas (`.livesync/ignore`, não testado); a vigia confere o processo do CLI, o
Doctor aberto e arquivos acima do limite. A colisão de binário silenciosa volta como pergunta em "Revisão
do sync e da divergência com o banco".

**Não testado:** convivência longa (horas ou dias) dos dois clientes; Ctrl+C; cópia vinda do OneDrive;
plugin com E2EE; Word e Excel reais regravando o arquivo; `customChunkSize` 60; GC V3; `.livesync/ignore`.
