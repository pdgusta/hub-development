# Contrato do painel da construção

Tech lead, 2026-10-15 ~21h15 (fixture ajustada ~21h40; `pegou_ticket` em toda etapa e tickets em `issues/` ~21h40). **Fechado para a carcaça.** Quando o desenho do laço for aprovado, o maestro manda as
diferenças e este arquivo muda por versão (campo `formato`). Fonte: `brief.md` e a mesa (`mesa.md`).

Regra de ouro: **a execução escreve, o painel lê.** O painel nunca escreve em `execucao/`, não manda nada para a
execução e pode cair sem parar nada. A execução não sabe que o painel existe.

---

## 1. Onde o painel roda

**Servidor próprio, pequeno, e o portal só abre a porta para ele.**

- `painel/servidor.py`: Python 3.12, só biblioteca padrão, `127.0.0.1:8771`, **só GET**. Serve a página e lê
  `execucao/` a cada pedido. Sem cache, sem banco, sem escrita.
- **Duas pastas lidas, as duas só leitura:** `construcao-do-hub/execucao/` (descrição e eventos) e
  `construcao-do-hub/issues/` (os tickets de construção, seção 4). Opções do servidor: `--pasta` (execução) e
  `--tickets` (tickets); `--fixture` aponta as duas para `fixture/execucao-fake/` e `fixture/execucao-fake/tickets/`.
- `painel/iniciar.cmd`: sobe o servidor e abre o navegador. Com `--fixture`, lê `painel/fixture/execucao-fake/` em vez
  da pasta real.
- **Pelo portal (aceito pelo maestro em 2026-10-15; ele cadastra a carta quando a carcaça estiver pronta):** uma carta no `cartas.json` ("Painel da construção") que aponta para
  `painel/abrir.html`. Essa página só embute `http://127.0.0.1:8771/` e, se não responder, diz "o painel está
  desligado: rode `painel\iniciar.cmd`". O núcleo do portal não muda.

Por quê:
- o navegador não lê `file://` com fetch, e uma página estática não lista `eventos/`: precisa de servidor;
- uma rota nova no portal mexe no núcleo (revisão do Prumo, marcos) e acopla o portal à execução;
- `python -m http.server` escuta em todas as interfaces por padrão e devolve listagem em HTML: frágil;
- servidor próprio: o portal cai, o painel segue; o painel cai, a execução segue.

Se um dia o portal abrir de outro jeito (link na barra, gaveta), muda só `abrir.html`, não o contrato.

---

## 2. A pasta da execução

```
.scratch/construcao-do-hub/
  issues/NN-<slug>.md                       tickets de construção (/to-tickets cria; os agentes mudam o Status:)
  execucao/                                 (a execução cria; o painel só lê)
    execucao.json                           descrição da execução (o maestro escreve)
    eventos/<agente>.jsonl                  um arquivo por agente, só acrescentado (os hooks escrevem)
```

- **Os tickets moram em `issues/`, não em `execucao/tickets/`** (decisão do maestro, 2026-10-15 ~21h35): é a
  convenção do repositório (`docs/agents/issue-tracker.md`). Na fixture continuam em `execucao-fake/tickets/`; o
  servidor recebe o caminho, o leitor não sabe a diferença.

- **`execucao.json`, não `laco.json`.** O nome `laco.json` já tem dono: é o formato da página "Laços" do portal
  (proposta do portal, seção 4.4). Se o maestro registrar a construção como laço do portal também, os dois arquivos
  convivem sem brigar.
- **`agentes/<agente>.json` dispensado.** O painel reconstrói o estado dos eventos. Uma fonte só, que não fica velha.

---

## 3. `execucao.json` (o maestro escreve; sobrescreve quando muda)

```json
{
  "formato": 1,
  "id": "construcao-2026-10-16",
  "titulo": "Construção do context hub",
  "inicio": "2026-10-16T09:00:00-03:00",
  "terminou_em": null,
  "limites": { "tentativa_min": 60, "subagentes_por_agente": 10, "sem_sinal_apos_s": 300 },
  "fases": [
    { "id": "spec",     "titulo": "Spec",                  "estado": "feita" },
    { "id": "tickets",  "titulo": "Tickets de construção", "estado": "feita" },
    { "id": "execucao", "titulo": "Execução",              "estado": "em-curso" }
  ],
  "papeis": [
    { "id": "construtor", "titulo": "Construtor" },
    { "id": "revisor",    "titulo": "Revisor" },
    { "id": "testador",   "titulo": "Testador" },
    { "id": "integrador", "titulo": "Integrador" },
    { "id": "prumo",      "titulo": "Prumo" },
    { "id": "maestro",    "titulo": "Maestro" }
  ],
  "agentes": [
    { "id": "maestro",      "papel": "maestro",    "titulo": "Maestro",      "modelo": "claude-opus-5-5", "esforco": "alto", "terminal": "Claude Code" },
    { "id": "construtor-1", "papel": "construtor", "titulo": "Construtor 1", "modelo": "claude-opus-5-5", "esforco": "alto", "terminal": "Construtor 1" },
    { "id": "prumo-1",      "papel": "prumo",      "titulo": "Prumo 1",      "modelo": "claude-opus-5-5", "esforco": "alto", "terminal": "Prumo 1" },
    { "id": "fable-1",      "papel": "construtor", "titulo": "Fable do ticket 12", "modelo": "claude-fable-5-1", "esforco": "medio", "terminal": "Fable 1", "temporario": true, "ticket": "12" }
  ],
  "padroes": {
    "teste":  ["^pytest\\b", "^python -m pytest\\b", "^npm (run )?test\\b"],
    "commit": ["^git commit\\b"]
  }
}
```

| Campo | Regra |
|---|---|
| `formato` | `1`. Outro valor → o painel mostra "formato desconhecido" e não desenha. |
| `id` | `[a-z0-9-]+`. Troca só quando a execução recomeça do zero. |
| `inicio`, `terminou_em` | ISO 8601 com fuso. `terminou_em` `null` enquanto roda. "Desde quando roda" sai de `inicio`. |
| `limites` | `tentativa_min` (o relógio de cada ticket), `subagentes_por_agente`, `sem_sinal_apos_s`. **Não decidido** se o limite de 1 hora é por ticket ou por tentativa: o painel conta **por tentativa** (cada `pegou_ticket` zera) até o desenho dizer. |
| `fases` | Na ordem. `estado` ∈ `a-fazer`, `em-curso`, `feita`. |
| `papeis` | Ids `[a-z0-9-]+`. **A cor de cada papel é do painel**, não do arquivo: o desenho final pode trocar papéis sem mexer em cor. |
| `agentes` | `id` = nome do arquivo de eventos. Os 10 agentes, os 2 Prumos e o maestro (13 linhas). `temporario: true` marca quem entra e sai no meio (o Fable, quando for agente próprio). `terminal` é o nome no canvas, só para mostrar. |
| `padroes` | Para o hook classificar comandos (seção 6). Expressões regulares sobre o comando, sem o `cd` da frente. |

Agente que aparece em `eventos/` sem estar em `agentes` → o painel mostra assim mesmo, com o selo "fora da lista".

---

## 4. Tickets: `issues/NN-<slug>.md`

Formato do rastreador do repositório (`docs/agents/issue-tracker.md`): um arquivo por ticket, numerado de `01`,
`Type:`, `Status:` e `Blocked by:` perto do topo, `## Comments` no fim. Os valores de `Status:` são os da convenção:
os de andamento (`claimed`, `resolved`) e os papéis de triagem (`docs/agents/triage-labels.md`). Duas linhas a mais,
**opcionais**: `Dono:` e `Com:`.

```markdown
# Sincronizador grava a nota de retomada

Type: task
Status: claimed
Dono: construtor
Com: construtor-1
Blocked by: 03, 07

## Pronto quando
...

## Comments
```

| Linha | Valores | Quem muda |
|---|---|---|
| `Status:` | convenção: `needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `claimed`, `resolved`, `wontfix`; aceitos também `open` (o "aberto" do rastreador), `review` e `testing` (se a execução quiser marcar a etapa) | o agente, ao mudar de etapa |
| `Dono:` | id de papel (opcional) | quem gera os tickets (`/to-tickets`) |
| `Com:` | id do agente com ele agora; vazio quando ninguém (opcional: sem ele, vale o último `pegou_ticket`) | o agente, junto com `Status:` |
| `Blocked by:` | números, separados por vírgula; ausente ou vazio = sem bloqueio | quem gera os tickets |

**A coluna do ticket vem do arquivo; os eventos só dizem a etapa de um `claimed`.** Os sete estados do brief, pela
ordem (a primeira regra que casa vale):

| Coluna no painel | Regra |
|---|---|
| esperando o Gustavo | `ready-for-human` (precisa de gente) ou `needs-info` (espera resposta de quem pediu) |
| feito | `resolved` (`wontfix` aparece junto, riscado, como "descartado", e não conta no total) |
| em teste | `testing`; ou `claimed` com quem está com ele (`Com:`, senão o último `pegou_ticket`) no papel `testador` |
| em revisão | `review`; ou `claimed` com quem está com ele no papel `revisor` ou `prumo` |
| em curso | `claimed` (qualquer outro papel, ou ninguém) |
| bloqueado | `ready-for-agent`, `needs-triage` ou `open` com algum `Blocked by:` que não está `resolved` (inclusive número inexistente) |
| a fazer | `ready-for-agent`, `needs-triage` ou `open` sem bloqueio aberto; `needs-triage` leva a marca "falta triagem" |

Valor fora da lista → "desconhecido", em cinza, com o valor cru, e entra nos problemas. Ciclo em `Blocked by:` →
problema, sem travar o desenho. Falha e "estourou 1 hora" **não são colunas**: são marcas por cima do ticket,
tiradas dos eventos (seção 7). `waiting-human`, da primeira versão deste contrato, saiu: vale `ready-for-human`.

---

## 5. Eventos: `eventos/<agente>.jsonl`

Parte do formato do QA (a fixture já existe), com o que o UI engineer pediu e faltava: batimento, início, fim, `ok` e
`modelo`. Um evento por linha, UTF-8, JSON de uma linha só, terminada em `\n`.

```json
{"t":"2026-10-16T09:12:03-03:00","agente":"construtor-1","tipo":"pegou_ticket","ticket":"07"}
```

### Campos

| Campo | Tipo | Quando |
|---|---|---|
| `t` | ISO 8601 com fuso | sempre |
| `agente` | id do agente | sempre; igual ao nome do arquivo (diferente → problema, a linha conta para o arquivo) |
| `tipo` | um da tabela abaixo | sempre |
| `ticket` | `"07"` (número, como no nome do arquivo, sem prefixo) | eventos de ticket; opcional nos outros |
| `sub` | id do subagente (o que o hook recebe) | subagentes e Fable |
| `para` | id de agente ou de papel | mensagens e `passou_ticket` |
| `de` | id de agente | `recebeu_mensagem` |
| `assunto` | texto curto, até 120 caracteres | mensagens, subagentes (a descrição), commit (a primeira linha) |
| `detalhe` | texto, até 500 caracteres | falha, teste, o que mais ajudar no clique |
| `ok` | `true` / `false` | `rodou_teste`, `fechou_subagente`, `commit` |
| `modelo` | id do modelo | `inicio`, `abriu_subagente`, `chamou_fable` |

Campo desconhecido é ignorado sem problema (o hook pode gravar mais). Campo que falta e não é obrigatório = `null`.

### Tipos

| Tipo | O que diz | Campos |
|---|---|---|
| `inicio` | o agente subiu | `modelo` |
| `sinal` | batimento; só diz "estou vivo" | — |
| `pegou_ticket` | o agente assumiu o ticket **em qualquer etapa** (construir, revisar, testar, integrar); começa uma tentativa e **zera o relógio** | `ticket` |
| `passou_ticket` | mandou o ticket para a próxima etapa | `ticket`, `para` (papel ou agente) |
| `resolveu_ticket` | deu o ticket por feito | `ticket` |
| `devolveu` | largou o ticket sem terminar (volta a `open`) | `ticket`, `detalhe` |
| `esperando_gustavo` | o ticket parou à espera do Gustavo | `ticket`, `detalhe` (o que ele precisa fazer) |
| `abriu_subagente` | | `sub`, `assunto`, `modelo` |
| `fechou_subagente` | | `sub`, `ok` |
| `chamou_fable` | pediu um Fable para uma tarefa muito complexa | `ticket`, `sub` (se for subagente) ou `para` (se for agente próprio), `modelo` |
| `mandou_mensagem` | `maestri ask` para alguém | `para`, `assunto` |
| `recebeu_mensagem` | **opcional** (ver 6) | `de`, `assunto` |
| `rodou_teste` | | `ok`, `assunto` (o comando), `detalhe` |
| `commit` | | `ok`, `assunto` |
| `passou_1h` | a tentativa passou do limite | `ticket` |
| `falhou` | erro que parou o trabalho | `detalhe`, `ticket` se houver |
| `fim` | a sessão do agente terminou | — |

`resolveu_ticket`, `inicio`, `sinal`, `fim` e os campos `ok` e `modelo` são o que entrou além da lista do QA.
Tipo desconhecido → a linha conta como sinal e entra nos problemas.

### Regras de gravação (para dez processos e hooks)

- **Um arquivo por agente; só acrescentar.** Nunca reescrever, nunca apagar linha.
- **Uma linha por `write`, até 4 KiB**, arquivo aberto em modo de acréscimo. Subagentes do mesmo agente gravam no
  arquivo do agente (o `sub` diz quem).
- **O painel tolera:** última linha sem `\n` (ainda sendo escrita) → ignora até completar; linha que não é JSON →
  pula e conta nos problemas; arquivo que encolheu → relê do zero.
- **Ordem:** a do arquivo. Entre arquivos, por `t`. Relógios são todos da mesma máquina.
- **`sinal` com freio:** o hook só grava se a última linha do arquivo tem mais de 30 s. Qualquer evento conta como
  sinal; o `sinal` só cobre o silêncio entre eventos.

---

## 6. Quem grava cada evento (mecânico, por hook)

Os eventos saem de hooks do harness, não da boa vontade do agente. Um script só (`hook-evento`, da execução, não do
painel) recebe o JSON do hook e grava a linha.

| Tipo | Gatilho |
|---|---|
| `inicio` | hook de início de sessão |
| `sinal` | hook depois de cada ferramenta, com o freio de 30 s |
| `pegou_ticket`, `passou_ticket`, `resolveu_ticket`, `devolveu`, `esperando_gustavo` | hook depois de editar ou gravar um arquivo em `issues/`: o script lê `Status:` e `Com:` novos e compara com o último evento do ticket no próprio arquivo. **`Com:` passou a ser este agente** → `pegou` (em `claimed`, `review` ou `testing`: o revisor e o testador também pegam). **`Com:` deixou de ser este agente com o ticket ainda em `claimed`, `review` ou `testing`** → `passou`, `para` = o agente que `Com:` nomeia agora, ou o papel da etapa seguinte quando `Com:` ficou vazio. `resolved` → `resolveu`; `ready-for-agent`/`open` → `devolveu`; `ready-for-human`/`needs-info` → `esperando`. Quem passa limpa `Com:` (ou põe o próximo); quem pega põe o próprio id. |
| `abriu_subagente`, `fechou_subagente` | hooks antes e depois da ferramenta que abre subagente (descrição e modelo vêm da entrada dela) |
| `chamou_fable` | o mesmo hook de antes, quando o modelo pedido é Fable; quando o Fable é agente próprio, o maestro grava ao abrir |
| `mandou_mensagem` | hook depois de um comando que começa com `maestri ask`: `para` = o primeiro argumento, `assunto` = o começo da mensagem |
| `recebeu_mensagem` | **opcional.** O painel tira "recebeu" do `mandou_mensagem` de quem mandou. Grave só se o harness disser de quem veio. |
| `rodou_teste`, `commit` | hook depois de comando que casa com `padroes.teste` ou `padroes.commit`; `ok` = código de saída 0 |
| `passou_1h` | hook depois de cada ferramenta: se o último `pegou_ticket` do arquivo tem mais de `tentativa_min` e ainda não há `passou_1h` para ele. O painel **também** conta o relógio sozinho, então o evento só confirma. |
| `falhou` | hook de erro da sessão, quando houver; senão, quem supervisiona (maestro) grava |
| `fim` | hook de fim de sessão |

**Não verificado:** os nomes exatos dos hooks e os campos que cada um recebe nesta versão do harness (início e fim de
sessão, subagente, erro). Quem escreve o `hook-evento` confere antes da execução. O painel não depende disso: depende
só das linhas.

---

## 7. O que o painel deriva (não é gravado por ninguém)

| O que | Regra |
|---|---|
| Último sinal do agente | o maior `t` do arquivo |
| **sem sinal há N min** | último sinal mais velho que `sem_sinal_apos_s` e nenhum `fim` depois dele |
| Situação do agente | `falhou` (último evento de trabalho é `falhou`, sem `pegou_ticket` depois) · `sem sinal` · `trabalhando` (com ticket em curso) · `ocioso` (vivo, sem ticket) · `encerrado` (`fim`) · `não começou` (sem arquivo) |
| Ticket do agente agora | o ticket do último `pegou_ticket` sem `passou`/`resolveu`/`devolveu`/`esperando` depois. Vale para todo papel: o revisor que pegou o ticket em `review` está **trabalhando**, não ocioso |
| Relógio da tentativa | agora − `t` do `pegou_ticket`; acima de `tentativa_min` → **estourou** (com ou sem o evento `passou_1h`) |
| Tentativa nº | quantos `pegou_ticket` do mesmo ticket há em todos os arquivos até ali |
| Subagentes abertos | `abriu_subagente` sem `fechou_subagente` com o mesmo `sub` (se o agente der `fim` ou `falhou`, os abertos dele fecham) |
| Fable em ação | subagente aberto ou agente vivo com `modelo` que começa com `claude-fable` |
| Conversas | cada `mandou_mensagem` é uma ligação `agente → para`, com hora e assunto |
| Andamento | tickets `resolved` / total (sem `wontfix`), desde `inicio` |
| Divergência | `Com:` do ticket ≠ agente do último `pegou_ticket` → marca "não confere" no ticket; a coluna segue o arquivo |

---

## 8. A API do servidor (só GET)

- `GET /` e `GET /web/...`: a página.
- `GET /api/execucao`: `{"lido_em": ISO, "execucao": <execucao.json ou null>, "tickets": [{"arquivo", "numero",
  "titulo", "status", "dono", "com", "blocked_by": [...], "texto"}], "agentes_com_arquivo": [...], "problemas":
  [...]}`. Pequeno; a página pede a cada 3 s.
- `GET /api/eventos?c=<agente>:<byte>,<agente>:<byte>`: só o que é novo desde o cursor de cada arquivo.
  Resposta: `{"lido_em": ISO, "arquivos": {"construtor-1": {"ate": 18342, "linhas": [{...}], "recomecou": false}},
  "problemas": [...]}`. Cursor maior que o arquivo → `recomecou: true` e as linhas desde o zero. Sem cursor = desde o
  zero. Para na última linha completa.
- Erros com JSON `{"erro": "...", "mensagem": "em palavras"}`. Caminho só dentro de `execucao/`, ids
  `[a-z0-9-]+`.

O servidor não interpreta eventos: entrega linhas. **A reconstrução (seção 7) é do navegador**, num módulo só
(`leitor.js`), que serve igual para a fixture embutida (modo arquivo, sem servidor) e para o HTTP.

---

## 9. A fixture (QA)

- `painel/fixture/execucao-fake/`, com a mesma forma da seção 2.
- `painel/fixture/gerar.mjs` (Node, sem pacotes; aceito em 2026-10-15: é ferramenta de teste, o painel segue em
  Python): apaga e recria `execucao-fake/` e vai acrescentando eventos com o tempo (~7 min ao vivo). Uma execução
  inteira: 10 agentes + 2 Prumos + maestro, cerca de 25 tickets com bloqueios, subagentes subindo e descendo (um
  agente chega a 10), um Fable, conversas, um ticket que estoura a 1 hora, um que espera o Gustavo, uma falha, agentes
  que ficam sem sinal.
- `--so-historia` grava tudo de uma vez (para captura e teste); `--excesso` passa de 10 subagentes, para ver o painel
  acusar.
- Sem dado de cliente nem pessoal: iniciativas pelo nome, agentes por papel.

## 10. Regras que não mudam com o desenho

- O painel não tem botão que mande nada. Nem link que rode coisa.
- Nunca mostra "zero" quando não conseguiu ler: mostra "ilegível" e o motivo.
- Nada de código interno solto na tela: ticket com número pequeno e título em palavras.
- Datas e horas no fuso da máquina; "há N min" recalculado a cada segundo no navegador, sem pedir ao servidor.
