# Fixture "Horta do bairro" e o contrato `estado-esperado.json`

Projeto fictício e neutro no formato exato do portal. As duas trilhas (dados e tela) só leem esta pasta;
mudá-la é decisão do construtor, avisada ao subagente da trilha de dados.

## Layout

```
horta/                      ← a "raiz" do projeto fictício
  mapa.md  estrategia.md  GLOSSARY.md
  issues/01..10-*.md        ← dez tickets
  cartas/                   ← duas cartas HTML, um dados.js, e um segredo.md (extensão proibida)
  lacos/                    ← dois laços (ver "Laços" abaixo)
    regas/                  ← em voo, como o A.1 da proposta: laco.json, config.json, estado/laco.db (SQLite),
                              estado/despachante.json, livros/*.jsonl
    sementes/               ← terminado, como o A.2: laco.json, config.json, estado/laco_final.json
  portal/                   ← a "pasta do portal" (onde está o projeto.json; raiz = "..")
    projeto.json  cartas.json  lacos.json
    rodadas/                ← uma absorvida, uma aberta com os cinco tipos, uma malformada (pergunta sem id)
    caixa/                  ← casos de recuperação (ver abaixo) e dois pedidos alteracao-laco
estado-esperado.json        ← a resposta de GET /api/estado para esta fixture
```

**Os testes copiam `horta/` para uma pasta temporária antes de subir o servidor**: o arranque apaga
`caixa/.tmp/*` e gera o `.md` que falta, e os testes de `POST` gravam na caixa. Quantas mensagens válidas a caixa
da fixture tem fica em `apoio.MENSAGENS_DA_FIXTURE`.

## O que a fixture cobre

| Caso | Onde |
|---|---|
| todos os estados: `open`, `claimed`, `resolved`, `wontfix` e um desconhecido (`parked`) | tickets 04–07 e 10, 03, 01–02, 08, 09 |
| dependência inexistente | ticket 05 (`Blocked by: 02, 99`) |
| ciclo | 06 ↔ 07 |
| carta mestra e carta histórica; `data.tipo` `feita` e `modificado` | `cartas.json` |
| carta que carrega um arquivo relativo (`dados.js`) | `cartas/mapa-dos-canteiros.html` |
| arquivo com extensão proibida dentro da `pasta` da carta | `cartas/segredo.md` → `/carta/mapa-dos-canteiros/segredo.md` é 404 |
| rodada com os cinco tipos (`escolha`, `varias`, `proposta`, `aprovar`, `texto`), com carta e "por quê" | `2026-10-01-canteiros-e-caminhos-r2.md` |
| rodada absorvida e já respondida | `2026-09-15-escolher-o-terreno-r1.md` + resposta na caixa (`estado: lida`) |
| rodada malformada (pergunta sem `id`) | `2026-10-02-composteira-r1.md` |
| caixa: `.json` sem `.md` (queda entre os passos 1 e 2) | `…-comentario-ticket-04-….json` → o arranque gera o `.md` com `estado: nova` e põe o aviso `pendente` |
| caixa: `.md` sem `.json` | `…-aprovacao-carta-regas-do-poco-….md` → problema "mensagem sem dados", nunca apagado |
| caixa: sobra em `.tmp/` | `caixa/.tmp/sobra-….json` → apagada no arranque, sem problema registrado |
| texto livre que tenta virar frontmatter | o comentário do ticket 04 contém `---` e `estado: lida`; no `.md` gerado cada linha sai com `> ` e o frontmatter continua `estado: nova` |
| `projeto.json` sem `MAESTRI_PIPE` no ambiente | `aviso.disponivel: false` (o teste limpa `MAESTRI_PIPE` e `MAESTRI_TERMINAL_ID` do ambiente) |
| laço em voo com SQLite (uma linha com JSON e `campo`, soma, contagem agrupada), JSON com hora declarada, JSONL, hora de arquivo, `declarado`, precondição `inicio`, `parado`, `esperando_cota`, `onda_atual` | `lacos/regas/laco.json` |
| laço terminado lido de `laco_final.json` (campo com índice negativo, `declarado`), `parado` num banco que não existe (ilegível, nunca "não parado") | `lacos/sementes/laco.json` |
| pedido `mudar-controle` aplicado com recibo válido e `efeito: aguarda` (o `config.json` já tem o valor novo) | `caixa/…-alteracao-laco-pesquisa-de-regas-5b0c7e2a-….md` |
| comentário de nó já lido (encerra na leitura, não é trabalho pendente) | `caixa/…-alteracao-laco-pesquisa-de-regas-8d2f4a61-….md` |

## Como comparar a API real com `estado-esperado.json`

Mesmas chaves e valores, com estas exceções:

- `projeto.gerado_em`: hora de geração;
- `projeto.codigos`: objeto prefixo → explicação em palavras dos códigos internos, `{}` quando o projeto.json não tem `codigos`;
- `rodadas[].base`: sha256 do arquivo (muda com o fim de linha do checkout);
- `cartas[].data.valor` quando `data.tipo == "modificado"`: vem do `mtime` do arquivo;
- `aviso.motivo`: texto livre;
- `problemas[].mensagem` e `rodadas[].erro`: compare só se são nulos ou não (o texto é livre, em palavras). A
  lista de `problemas` é comparada pelo campo `arquivo`.

## Decisões de detalhe do esquema (valem para `leitores.py` e para a tela)

Além do que a §3.4 da proposta mostra:

- **Ordem:** `tickets` por número; `rodadas` por `id` (que começa pela data); `caixa` por `arquivo`;
  `problemas` por `arquivo` e depois `mensagem`; `decisoes` na ordem do mapa; `glossario` e `radar` na
  ordem do arquivo; `cartas` na ordem do `cartas.json`.
- **Caminhos** (`tickets[].arquivo`, `rodadas[].arquivo`, `problemas[].arquivo`, `cartas[].arquivo`): relativos
  a `raiz`, com `/`. Se a pasta do portal estiver fora da raiz, caminho absoluto.
- **Ticket:** `estado` ∈ {open, claimed, resolved, wontfix, desconhecido}; `estado_cru` é o `Status:` como
  está no arquivo. `bloqueado_por` é a lista como escrita (ordem do arquivo). `bloqueios_abertos` = bloqueadores
  que existem e estão `open`, `claimed` ou `desconhecido`, ordenados; `wontfix` e `resolved` não bloqueiam.
  `bloqueios_inexistentes` = números sem arquivo (cada um vira um problema no ticket que o cita). `bloqueia` =
  quem cita este ticket em `Blocked by:`, ordenado. `cartas` = ids do `cartas.json` cujo `ticket` é este.
  Ticket sem `Type:` → `tipo: null`; sem `Status:` → `desconhecido` com `estado_cru: null`. Ticket sem
  `# Título` na primeira linha → título = nome do arquivo sem número, e problema.
- **Plano de voo:** só `open` e `claimed` (resolvidos pousaram, `wontfix` não voa, `desconhecido` fica fora e
  aparece em problemas). Arestas para tickets fora do plano (resolvidos, inexistentes…) são ignoradas na
  camada. Camada = caminho mais longo a partir de quem não tem bloqueio aberto; dentro da camada, por número.
  Ciclo: entre as arestas do ciclo (dependente → bloqueador), ignora-se a de **maior dependente** (empate:
  maior bloqueador), só para desenhar; `ciclos[]` = `{"tickets": [números em ordem crescente],
  "aresta_ignorada": [dependente, bloqueador]}` e um problema no arquivo do dependente.
- **Destino:** `texto` = parágrafos antes da lista numerada, linhas juntadas por um espaço. Cada critério:
  linhas juntadas por espaço, sem o `;` ou `.` final; `palavra` vem do `projeto.json` pela posição (se as
  contagens não baterem, `palavra: null` nos que sobram e um problema no `projeto.json`).
- **Decisões:** `- [Título](issues/NN-slug.md): resumo`; `numero` dos dois dígitos do nome do arquivo; `resumo`
  com as linhas juntadas por espaço, pontuação final mantida. Item que não casa com o formato → problema.
- **Fora da rota:** itens de `## Not yet specified` e `## Out of scope`, texto cru com linhas juntadas por espaço.
- **Radar:** primeira tabela Markdown depois de `### Radar`, sem o cabeçalho e a linha de traços; `tema` e
  `gatilho` crus (podem ter `**`).
- **Glossário:** `**Termo**:` seguido das linhas da definição (juntadas por espaço) até linha em branco ou
  `_Avoid_:`; `evite` = texto depois de `_Avoid_:`, ou `null`.
- **Carta:** o que está no `cartas.json`, mais `ticket_titulo` (título do ticket, ou `null`) e `url`
  (`/carta/<id>/`). `data.tipo == "modificado"` → `valor` é a data (AAAA-MM-DD, hora local) do `mtime` do
  arquivo, e o `valor` do json é ignorado. `arquivo` precisa ficar **diretamente** dentro de `pasta`; senão a
  carta fica na lista com um problema. Arquivo inexistente → problema, carta continua na lista.
- **Substituição de carta:** toda carta traz `substitui` (id escrito no `cartas.json`, ou `null`),
  `substitui_titulo`, `substituida_por` (id da substituta direta, ou `null`), `substituida_por_titulo` e
  `situacao_efetiva`. A carta que outra substitui fica com `situacao_efetiva: "historica"`; as demais repetem a
  `situacao` do arquivo, que nunca é regravada. Casos ruins viram problema e a ligação é ignorada: id inexistente,
  a si mesma, a carta mestra, roda (A substitui B, B substitui A). Duas cartas substituindo a mesma: vale a que
  vem depois no arquivo (só ela ganha `substitui_titulo`), com problema. Cadeia C→B→A: A e B substituídas, cada
  uma apontando a substituta direta.
- **Rodada:** `ticket_titulo`; `carta` (id ou `null`); `contexto` = Markdown entre o frontmatter e o primeiro
  `##`, `strip()` nas pontas, quebras de linha internas mantidas; `respondida` = existe resposta na caixa para
  esta rodada; `ultima_resposta` = nome (sem extensão) da resposta mais nova da cadeia de `substitui`, ou `null`;
  `malformada` e `erro`. Pergunta: `recomendada` sempre lista (vazia se não há); `opcoes` sempre lista;
  `porque` = texto depois das opções (ou do bloco json), `strip()`, ou `null`; `proposta` só no tipo
  `proposta`. Rodada malformada: `perguntas: []`, `malformada: true`, `erro` em palavras, e os campos do
  frontmatter que deu para ler (os que faltam ficam `null`); também entra em `problemas`.
- **Caixa:** uma entrada por `.json` válido: `arquivo` (nome sem extensão), `tipo`, `alvo`
  (`{"tipo", "id", "titulo"}`, com o título em palavras da rodada, do ticket ou da carta), `ticket`, `enviada`,
  `envio`, `estado` (do `.md`; valor cru), `aviso` (`pendente` | `enviando` | `entregue` | `falhou`, ou `null`
  quando não há registro em `.avisos.json`), `substitui` e `substituida` (há mensagem mais nova apontando para
  esta).
- **Aviso:** `disponivel` é `true` só com `MAESTRI_PIPE` e `MAESTRI_TERMINAL_ID` no ambiente e o executável do
  `projeto.json` encontrado no `PATH`; `motivo` em palavras quando `false`.

## O `.json` da caixa (a fonte de cada mensagem)

```json
{
  "envio": "<uuid>", "tipo": "resposta | comentario | aprovacao", "enviada": "<ISO com fuso>",
  "alvo": {"tipo": "rodada | ticket | carta", "id": "..."}, "ticket": "NN ou null", "substitui": "<nome> ou null",
  "corpo_hash": "<sha256 de json.dumps(corpo, sort_keys=True, ensure_ascii=False)>",
  "corpo": { "...o corpo do POST sem o campo envio..." },
  "rodada": { "só em resposta: id, base, titulo, ticket, perguntas[{id, titulo, tipo, recomendada, opcoes, proposta}]" }
}
```

Em `alteracao-laco` (§4.5 da proposta), `alvo` é `{"tipo": "laco", "id", "titulo"}`, `ticket` é o do laço, e no
lugar de `rodada` vem `laco`, o retrato do laço no envio: `id`, `titulo`, `ticket`, `execucao` (`{id, inicio,
terminou_em}`), `revisao`, `no` (`{id, titulo, papel}` ou `null`), `capacidades` (como na API), `situacao` e, só em
`mudar-controle`, `controle`: o controle como a API o mostra (definição, `configurado` com fonte e hora, `em_uso`,
`precondicoes` com valores) mais `definicao` (o controle como declarado no `laco.json`, origens incluídas) e
`origem_configurado`. O `.md` nasce só desse `.json`.

## Laços (`GET /api/lacos`, `GET /api/laco/<id>`)

Os laços não entram em `GET /api/estado` e por isso não estão no `estado-esperado.json`; os pedidos deles entram na
`caixa` do estado como as outras mensagens, e os problemas (registro, `laco.json` malformado ou com chave
desconhecida, pedido com estado desconhecido ou recibo inválido) entram em `problemas`. Os testes são
`teste_lacos.py`.

- **Cópia avivada.** `apoio.copiar_horta()` põe a hora dos livros-razão de `lacos/regas/livros/` em "agora": o
  sinal do laço em voo é a hora do arquivo, então sem isso ele aparece `sem-sinal`. Para ver a fixture na tela
  fora dos testes, faça o mesmo (`apoio.avivar_laco(<raiz da cópia>)`) ou espere ver "sem sinal".
- **O banco** `lacos/regas/estado/laco.db` (modo de diário DELETE, um arquivo só): `controle(chave, valor)` sem
  chave única (os testes põem duas linhas) com `teto` = `{"pedidos": 5000, "horas": 2, "inicio": 1792021007.69}`,
  `onda` = `2`, `historico` (duas ondas) e `parar` = `false`; `uso(modelo, tentativas)` somando 1684;
  `pedidos(id, estado)` com 40 `feito`, 10 `pendente` e 3 `em_voo`. Os testes abrem cópias dele para escrever
  (simulando o laço); o portal só o abre com `mode=ro`.
- **Esperado no laço em voo:** grupo `em-voo`, situação `rodando`, destaque `tentativas` = 1684, `pedidos_abertos`
  = 1 (o aplicado que aguarda efeito), `gate_novos` configurado 0,1 e em uso `nao-confirmado`, teto `relido`,
  `onda_atual` 2. **No terminado:** grupo e situação `terminado`, destaque 738, `parado` ilegível.
- **Ordem e forma:** a lista segue o `lacos.json`; `pedidos` vêm do mais novo ao mais velho; horas em ISO 8601 no
  fuso local, com segundos; um valor ilegível vem `null` com `ilegivel` em palavras, nunca zero.
- **Linha malformada** em `GET /api/lacos`: `titulo` = id, `grupo` `em-voo`, `situacao` `desconhecido`,
  `destaque` e `pedidos_abertos` `null`, `problema` em palavras.
