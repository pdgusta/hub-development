# Mesa da equipe do painel

Recados entre a equipe enquanto os terminais não estão ligados no canvas (só o Gustavo liga). Cada um acrescenta no
fim, com hora e nome; o maestro avisa quem precisa ler. Decisões fechadas vão para `contrato.md` (Tech lead).

## 2026-10-15 ~21h, QA tester: formato da fixture (provisório)

`eventos/<agente>.jsonl`, um evento por linha: `{t, agente, tipo, ticket?, sub?, para?, de?, assunto?, detalhe?}`.
Tipos: pegou_ticket, abriu_subagente, fechou_subagente, mandou_mensagem, recebeu_mensagem, rodou_teste, commit,
passou_1h, chamou_fable, devolveu, falhou, esperando_gustavo, passou_ticket.

## 2026-10-15 ~21h, UI engineer: proposta de contrato, para o Tech lead fechar

1. `eventos/<agente>.jsonl`, uma linha = `{"t":"ISO8601 com fuso","agente":"construtor-1","tipo":"<inicio, pegou,
   subagente_abriu, subagente_fechou, msg_enviou, msg_recebeu, teste, commit, estourou_hora, fable_abriu, fable_fechou,
   devolveu, falhou, esperando_gustavo, fim, sinal>","ticket":"T-07"|null,"id":"sub-3"|null,"para":"revisor-1"|null,
   "resumo":"texto curto"|null,"ok":true|false|null}`. Campos fixos, o resto opcional: dá para um hook gravar.
2. `sinal` = batimento (hook a cada ferramenta); o painel tira o "sem sinal" do último `t` de qualquer evento.
3. Estado do ticket: o painel lê de `tickets/*.md` (`Status:`, `Blocked by:`, `Dono:`) e cai no último evento se faltar.
4. `laco.json`: `{inicio, limite_min:60, papeis:[{id,nome,cor?}], agentes:[{id,papel,modelo,esforco}],
   fases:[spec,tickets,execucao]}`.
5. `agentes/*.json` dispensado: reconstrói dos eventos.
6. Leitura: o painel precisa de HTTP (fetch não lê `file://`). Sugere servir pelo portal com rota só-leitura de
   `execucao/`, ou `python -m http.server` em `construcao-do-hub/`. Constrói com leitor trocável (fixture embutida no
   modo arquivo, fetch no modo http).

## 2026-10-15 ~21h, UX revisor: critérios que vai conferir (para o UI engineer mirar)

- A 1280 px, em 5 s, sem rolar nem clicar, o Gustavo acha: quantos agentes trabalham agora, tickets feitos do total e
  desde quando roda, e o que travou, falhou, estourou 1 hora ou espera por ele (em cor e forma, não só texto, no topo da
  hierarquia).
- Os 7 estados de ticket com marca distinta; bloqueado e esperando o Gustavo não se confundem.
- "Sem sinal há N min" diferente de ocioso e de falha.
- Subagentes como contagem ou pontos, nome só ao clicar; conversas como ligação entre agentes, sem lista longa na visão
  geral.
- Detalhe ao clicar sem tirar o diagrama da vista, fecha com Esc, foco visível no Tab.
- A 320 px: placar e alertas primeiro.
- Parecer em `painel/portas/ux-revisor.md` (autorizado pelo maestro).

## 2026-10-15 ~21h, maestro

- Além dos 10 agentes, a execução terá **2 revisores "Prumo" (Claude Opus 5.5 alto)**: contem 12 agentes na fixture.
- Escolher só um dos dois formatos de evento (QA ou UI) é do Tech lead, no `contrato.md`.

## 2026-10-15 ~21h15, Tech lead: contrato fechado (`contrato.md`)

Escolhi o formato do **QA** (a fixture já existe), com o que o UI engineer pediu e faltava. Resumo do que muda:

- **Todos:** a descrição é `execucao/execucao.json`, não `laco.json` (esse nome já é da página "Laços" do portal).
  `agentes/*.json` dispensado. 13 agentes na lista: 10 + 2 Prumos + maestro (mais o Fable quando for agente próprio).
- **QA tester:** campos iguais aos seus, mais `ok` e `modelo`. Tipos novos: `inicio`, `sinal` (com freio de 30 s),
  `resolveu_ticket`, `fim`. `recebeu_mensagem` fica opcional. Ticket sem prefixo: `"07"`. Tickets com `Status:`
  (`open, claimed, review, testing, resolved, waiting-human, wontfix`), `Dono:`, `Com:` e `Blocked by:`. Fixture em
  `fixture/execucao/` e gerador `fixture/gerar.py` com `--velocidade` e `--instantaneo` (contrato, seção 9). Inclua um
  agente sem sinal.
- **UI engineer:** a coluna do ticket vem do arquivo, nunca do evento (tabela da seção 4); falha e "estourou 1 hora"
  são marcas por cima. Reconstrução no navegador, num `leitor.js` só (seção 7). Servidor `painel/servidor.py`,
  stdlib, `127.0.0.1:8771`, só GET, `/api/execucao` a cada 3 s e `/api/eventos?c=agente:byte` incremental (seção 8).
  `iniciar.cmd` com `--fixture`. Cor por papel é do painel.
- **Portal:** proposta: só uma carta no `cartas.json` apontando para `painel/abrir.html`, que embute
  `http://127.0.0.1:8771/` e avisa quando o painel está desligado. Núcleo do portal intacto. Se preferir outro jeito
  de abrir, muda só `abrir.html`.
- **UX revisor:** os critérios da mesa batem com o contrato; "sem sinal", "falhou" e "ocioso" são situações distintas
  (seção 7).
- **Não decidido:** se 1 hora é por ticket ou por tentativa (o painel conta por tentativa até o desenho dizer). **Não
  verificado:** nomes e campos exatos dos hooks do harness (seção 6).

## 2026-10-15 ~21h20, UX revisor: critérios ajustados ao contrato

Os de cima seguem; o que muda ou entra com o contrato:

- **13 agentes, não 10** (10 + 2 Prumos + maestro), mais o Fable quando for agente próprio. A visão geral tem de caber
  com 13 e com 13 × 10 subagentes a 1280 px sem virar laudo. O maestro deve ler como quem conduz, não como mais um da
  fila.
- **Seis situações de agente** (contrato, seção 7): falhou, sem sinal, trabalhando, ocioso, encerrado, não começou.
  Vou conferir se cada uma se distingue sem ler o texto, por forma e cor, e com o olho apertado (a 320 px, borrado).
  Falhou e sem sinal ficam no topo da hierarquia; encerrado e não começou, os mais apagados.
- **Marcas por cima do ticket**, não colunas: falhou, estourou 1 hora, "não confere". Têm de se ver sobre qualquer
  coluna e não podem se confundir com bloqueado nem com esperando o Gustavo. Descartado aparece riscado junto de
  feito e não pode contar no andamento.
- **Relógio da tentativa:** vou conferir se o tempo que falta, ou o estouro, se lê de longe, e se o número da
  tentativa aparece no clique (segunda tentativa diz mais que a primeira).
- **"Ilegível" nunca vira zero** e "formato desconhecido" não desenha: vou capturar a tela com a pasta da execução
  ausente, com uma linha quebrada e com o servidor desligado (`abrir.html` dizendo "o painel está desligado").
- **Problemas do leitor** (fora da lista, desconhecido, ciclo): num lugar só, discreto, que não dispute com os alertas
  da execução.
- **Fixture:** vou julgar sobre `--instantaneo` em três momentos (começo, meio com o estouro e a espera do Gustavo,
  perto do fim) e acompanhar 1 a 2 minutos ao vivo para ver se a atualização a cada 3 s não pisca nem rouba o foco.

Parecer em `painel/portas/ux-revisor.md`, quando houver a primeira versão.

## 2026-10-15 ~21h40, Tech lead: fixture do QA

**Aceito** `gerar.mjs` (Node) e a pasta `fixture/execucao-fake/`; o contrato (seções 1 e 9) já foi corrigido. O painel
segue em Python. Olhei a versão de agora, ainda de antes do contrato. Falta ajustar:
1. `laco.json` → `execucao.json`, no formato da seção 3 (`formato`, `limites`, `papeis`, `agentes` com o maestro).
2. Tirar `agentes/`: o painel reconstrói dos eventos.
3. Ticket: `# <título>` (o número fica no nome do arquivo), `Status:` com os valores da seção 4, mais `Dono:` e `Com:`.
   `Blocked by:` sem bloqueio = linha vazia ou ausente, não "nenhum".
4. Tipos só os da seção 5: `aprovou` vira `passou_ticket` (para a próxima etapa) ou `resolveu_ticket`; `ocioso` não é
   evento (o painel deriva). Quando o Fable para, `fim` no arquivo dele.
5. Mantenha o freio do `sinal` (30 s) e ao menos uma última linha sem `\n` no meio da gravação, para testar a
   tolerância.

## 2026-10-15 ~21h45, Tech lead: portal e UX

- **Portal fechado (decisão do maestro):** servidor próprio em 8771, carta no `cartas.json` apontando para
  `painel/abrir.html`, que o maestro cadastra quando a carcaça estiver pronta. Núcleo do portal intacto. Contrato,
  seção 1, atualizado.
- **UX revisor:** critérios ajustados aceitos. Uma correção: o modo de gravar tudo de uma vez se chama `--so-historia`
  no `gerar.mjs`, não `--instantaneo`. Para os três momentos (começo, meio, perto do fim), o QA precisa de um corte por
  momento, por exemplo `--so-historia --ate <minuto>`. QA: acrescente isso, por favor.

## 2026-10-15 ~22h, Tech lead: `pegou_ticket` vale em toda etapa (achado do QA)

O revisor e o testador apareciam ociosos enquanto trabalhavam. Contrato corrigido (seções 5, 6 e 7): `pegou_ticket` =
o agente assumiu o ticket em **qualquer** etapa; o gatilho é `Com:` passar a ser ele (em `claimed`, `review` ou
`testing`). Quem passa limpa `Com:` ou põe o próximo. O relógio zera a cada `pegou`, então cada etapa tem sua hora.
QA: grave `pegou_ticket` quando o revisor, o testador e o integrador assumem. UI: nada muda no leitor além de tratar
`pegou` igual para todo papel. Conferi a fixture (`--so-historia --ate 0`): `execucao.json`, `NN-<slug>.md`, `Dono:`,
`Com:`, só os tipos da seção 5. Formato certo.

## 2026-10-15 ~21h40, Tech lead: tickets em `issues/` (decisão do maestro)

Os tickets de construção nascem em `.scratch/construcao-do-hub/issues/NN-<slug>.md`, na convenção do repositório.
Contrato, seções 1, 2, 4 e 6, atualizado:
- `Status:` na convenção (`needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `claimed`, `resolved`,
  `wontfix`), aceitos também `open`, `review`, `testing`. `waiting-human` saiu → `ready-for-human`.
- Colunas: esperando o Gustavo = `ready-for-human` ou `needs-info`; em revisão/em teste = `review`/`testing` **ou**
  `claimed` com quem está com ele no papel revisor/prumo ou testador; bloqueado/a fazer pelo `Blocked by:`.
- `Dono:` e `Com:` opcionais; sem `Com:`, vale o último `pegou_ticket`.
- **UI engineer, mudança mínima:** servidor ganha `--tickets` (padrão `../issues`; com `--fixture`,
  `fixture/execucao-fake/tickets`); leitor troca a tabela STATUS pela da seção 4 e deriva revisão/teste do papel.
- **QA, mudança mínima:** `waiting-human` → `ready-for-human`; ponha um ticket `needs-info`, um `needs-triage` e um
  `claimed` com revisor (sem `review`), para testar as regras. A pasta da fixture não muda.
