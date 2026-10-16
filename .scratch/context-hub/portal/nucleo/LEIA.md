# Núcleo do portal: instalar noutro workspace

O `nucleo/` é genérico: copie a pasta inteira para o workspace novo sem mudar uma linha. Tudo o que é do
projeto entra pelo `projeto.json`, que fica **fora** do núcleo, na "pasta do portal".

## Requisitos

Python 3.12 ou mais novo, só biblioteca padrão. Sem rede, sem pacotes.

## Passos

1. Crie a pasta do portal (por exemplo `<repo>/.scratch/<projeto>/portal/`) e copie `nucleo/` para dentro dela.
2. Escreva `projeto.json` na pasta do portal. Caminhos: `raiz` é relativa à pasta do portal; `mapa`,
   `tickets`, `estrategia` e `glossario` são relativos a `raiz`; `rodadas`, `caixa` e `cartas` são
   relativos à pasta do portal.

   ```json
   {
     "nome": "Nome do projeto",
     "raiz": "../../..",
     "porta": 8770,
     "mapa": "caminho/do/map.md",
     "tickets": "caminho/da/pasta/issues",
     "estrategia": "caminho/da/estrategia.md",
     "glossario": "GLOSSARY.md",
     "rodadas": "rodadas",
     "caixa": "caixa",
     "cartas": "cartas.json",
     "criterios": [{"palavra": "uma palavra por critério do destino, na ordem do mapa"}],
     "aviso": {"agente": "nome do terminal do agente no canvas", "executavel": "maestri"},
     "codigos": {"Q": "pergunta numerada das rodadas de mapeamento", "R": "resposta numerada na estratégia"}
   }
   ```

   `codigos` é **opcional**: objeto que mapeia um prefixo de uma a três letras (`^[A-Za-z]{1,3}$`) para a
   explicação em palavras do código interno que a página encontra nos textos (ex.: "Q7", "R18"). `GET /api/estado`
   devolve-o em `projeto.codigos` (`{}` quando ausente). Fora da forma (não é objeto, chave fora do padrão, valor
   que não é texto não vazio) o campo inteiro vira `{}` com um problema em palavras no `projeto.json`; o servidor
   sobe mesmo assim.

   **Confinamento, sem exceção:** `raiz` pode subir quantos níveis quiser (é a escolha do projeto), mas todo
   outro caminho é resolvido com `realpath` e tem de ficar dentro da sua base (`raiz` ou a pasta do portal).
   Caminho absoluto, `..` que sai da base, symlink ou junction para fora → o item vira um problema em
   `problemas[]` (no `projeto.json`, em palavras) e não é lido; a `caixa` fora da pasta do portal faz o servidor
   recusar subir, porque não há onde gravar com segurança. A mesma regra vale para `arquivo` e `pasta` do
   `cartas.json` (a carta fica na lista com problema e não é servida) e para os arquivos descobertos nas pastas
   de tickets, rodadas e caixa (um atalho para fora é ignorado com problema).

   `lacos` é **opcional** (desde o marco L2): caminho do registro de laços, relativo à pasta do portal, como
   `cartas` (ex.: `"lacos": "lacos.json"`). Ausente = nenhum laço, sem problema. Ver "Laços" abaixo.

3. Escreva `cartas.json` (lista; pode começar como `[]`). Cada carta: `id`, `titulo`, `arquivo` e `pasta`
   (relativos a `raiz`; o arquivo precisa estar diretamente dentro da pasta), `proposito`, `ticket`,
   `decisao`, `data` (`{"valor", "tipo": "modificado" | "feita"}`), `situacao` (`vigente` | `historica`),
   `mestra`. Opcional: `substitui` (id da carta que esta substitui); o portal tira a antiga das vigentes
   sozinho, sem regravar o arquivo (ver `testes/fixtures/LEIA.md`, "Substituição de carta").
4. Crie as pastas `rodadas/` (o agente escreve) e `caixa/` (o portal escreve).
5. Suba o servidor a partir da pasta do portal:

   ```
   python nucleo/torre.py projeto.json [--abrir]
   ```

   `--abrir` abre `http://127.0.0.1:<porta>/` no navegador padrão depois de a porta estar aberta; é o que o
   `iniciar.cmd` da pasta do portal usa (duplo clique fora do canvas, ou dentro do terminal do canvas).

   Ele escuta só em `127.0.0.1`, na porta do `projeto.json`, recusa subir se a porta estiver ocupada ou o
   `projeto.json` estiver ausente ou inválido, e diz no terminal se o aviso ao agente está disponível
   (precisa de `MAESTRI_PIPE` e `MAESTRI_TERMINAL_ID` no ambiente e do executável no `PATH`).

## Aviso ao agente (os dois canais)

A fila `caixa/.avisos.json` guarda, por `envio`, `{estado, tentativas, ultimo_erro, proximo}` com `estado` em
`pendente` → `enviando` → `entregue` | `falhou`. Toda mensagem nova entra `pendente`; o que a tira daí é um dos
dois canais abaixo (a mesma fila para ambos; cada canal relê o arquivo antes de marcar e grava de forma atômica;
a `Fila` do servidor relê quando o arquivo muda em disco). Entrega "pelo menos uma vez": um aviso pode repetir,
nunca se perder; o agente ignora um `.md` que já está `estado: lida`.

- **Canal A, emissor no servidor** (`nucleo/aviso.py`, classe `Emissor`): só existe quando o servidor roda num
  terminal do canvas, isto é, com `MAESTRI_PIPE` e `MAESTRI_TERMINAL_ID` no ambiente **e** o executável de
  `aviso.executavel` encontrável (nome no `PATH`, ou caminho com pasta que existe). Uma thread dorme num
  `Event.wait` de 5 s (o `POST /api/caixa` e o `POST /api/aviso/tentar` a acordam antes), junta os `pendente`
  cuja hora chegou numa mensagem só ("Portal: N mensagens novas do Gustavo na caixa." + uma linha
  `- tipo: título; caminho do .md relativo à raiz` por mensagem + "Absorva no ticket dono e troque estado: nova
  por lida.") e roda `<executavel> ask <agente> <mensagem>` (uma entrega por vez; tempo limite 30 min). O `ask` só
  volta quando o agente fica ocioso; enquanto não volta, o emissor procura prova de entrega a cada `PASSO_OLHAR`
  (2 s): o `.md` de todas as mensagens já lido, ou, nos primeiros `OLHAR_TELA_POR` (120 s), o começo do UUID de cada
  envio na tela do `check` fora da caixa de digitação (`prova_na_tela`). Com prova → `entregue` e a vez passa ao
  próximo aviso; o `ask` segue sozinho até voltar ou até os 30 min (`asks_em_curso`). Sem prova, espera o `ask`.
  Os 30 min dependem de uma thread do servidor: valem só com o portal no ar. Na parada normal, `Emissor.parar()`
  encerra os `ask` já provados; um `ask` sem prova fica (sobrevive e entrega). Depois de uma queda abrupta, um
  `ask` provado pode sobrar até voltar sozinho. Ele não é aviso perdido (a fila já diz `entregue`): nunca reenvie
  por causa dele. Para encerrar só os remanescentes do próprio portal, no PowerShell, com `<agente>` do
  `projeto.json` e a hora em que o portal subiu de novo:
  `Get-CimInstance Win32_Process -Filter "Name='maestri.exe'" | Where-Object { $_.CommandLine -match 'ask "<agente>" "Portal: ' -and $_.CreationDate -lt [datetime]'<hora da subida>' }`
  confira na lista e em `GET /api/aviso` que os UUIDs citados na linha de comando estão `entregue`, e só então
  `| Stop-Process`. Nunca encerre por nome de imagem nem um `ask` de outro remetente.
  Saída 0 → confere com `<executavel> check <agente>` se o começo da mensagem ficou digitado sem Enter no
  terminal do agente (acontece quando ele está no meio de um turno): se ficou, manda `ask <agente> --raw "
"`,
  confere de novo e, se ainda está lá, `ask <agente> "(enviar)"`, que leva o texto parado junto; só então
  `entregue`. Saída diferente de 0, exceção, tempo esgotado ou `check` que falha (entrega ambígua) → `pendente`
  com `ultimo_erro` em palavras e `proximo` em 1, 5 e 15 min pelas `tentativas`; na quarta falha, `falhou`
  (visível em `GET /api/aviso`; `POST /api/aviso/tentar {"envio"}` devolve a `pendente` e acorda o emissor). Com
  o canal indisponível nada é marcado por ele: fica `pendente` e `aviso.disponivel: false` com `motivo` em
  palavras em `/api/estado` e `/api/aviso`; a página mostra a faixa "diga 'respondi'".
- **Canal B, vigia do lado do agente**: `python nucleo/aviso.py --vigiar <pasta do portal> [--intervalo 3]
  [--uma-vez]`, processo separado (por exemplo no monitor de fundo da sessão do agente). A cada intervalo lê só a
  fila; havendo `pendente`, lê a caixa e imprime **uma linha** por mensagem pendente (`tipo: título; caminho do
  .md; envio <UUID completo>`) marcando-a `entregue` ao imprimir. Não toca no que está `enviando` (é do canal A),
  `entregue` ou `falhou`; um `pendente` cujo `.md` já está `lida` vira `entregue` sem imprimir. Sai limpo com
  Ctrl+C; `--uma-vez` lê e sai (código 0; 2 se a pasta não tem `projeto.json` legível).

Ao subir, `torre.py` escreve no terminal qual modo está valendo ("aviso ao agente: disponível (modo canvas: emissor
ligado…)" ou "indisponível (…); modo fora do canvas"). Nos testes, `aviso.executavel` aponta para um script `.py`
(o núcleo roda um `.py` com o próprio Python): é assim que o `maestri` falso entra sem rede nem `maestri` real.

## Laços (o que roda por trás; marco L2)

Contrato completo na proposta do portal (§4.4 `laco.json`, §4.5 `alteracao-laco`); aqui, o que instalar exige.

- **Registro** `lacos.json` (na pasta do portal, apontado por `projeto.json` → `lacos`): lista
  `[{"id": "<[a-z0-9-]+>", "pasta": "<relativa a raiz>"}]`, relida a cada pedido (registrar um laço não exige
  reiniciar). A ordem é a da tela. A `pasta` precisa ter `laco.json` e não pode estar dentro da pasta do portal nem
  contê-la. Entrada com id ruim ou repetido vira problema; com pasta ruim, aparece malformada pelo id.
- **Descrição** `laco.json` (na pasta do laço, escrita por quem monta o laço; o portal nunca grava ali): `formato: 1`,
  `id` igual ao do registro, `titulo`, `ticket`, `execucao`, `nos`, `ligacoes`, `controles`, `capacidades`,
  `contadores`, `sinal` (obrigatórios) e `parado`, `esperando_cota` (opcionais). Fora do contrato → o laço aparece
  com `problema` em `GET /api/lacos`, `GET /api/laco/<id>` responde `422 laco-malformado` e o erro vai para
  `problemas` de `GET /api/estado`. Chave desconhecida só vira problema.
- **Fontes de estado**, só leitura e só dentro da pasta do laço: JSON (`arquivo` + `campo`), JSONL (última linha
  válida dos últimos 64 KiB), SQLite (uma linha, soma ou contagem; aberto com `file:<caminho real>?mode=ro`,
  `uri=True`, `timeout` 2 s, `PRAGMA query_only=ON`, conexão por leitura; nomes de tabela e coluna conferidos pelo
  padrão `[A-Za-z_][A-Za-z0-9_]*`, valores do filtro como parâmetros), hora do arquivo (`mtime`) e `declarado`. Todo
  caminho é relativo à pasta do laço: absoluto, letra de unidade, `..` ou componente com ponto tornam o laço
  malformado; atalho ou junction que sai da pasta deixa só aquela origem "ilegível", com problema, sem ler. Fonte
  ausente, travada, acima de 16 MiB ou com valor do tipo errado deixa só aquele número "ilegível" (nunca zero,
  nunca convertido). As fontes nunca saem como arquivo: nem pela API nem por `/carta/…`. Uma carta cuja `pasta` é
  a raiz de um laço registrado, ou a contém, não serve nada de dentro dele; dentro do laço, só serve a carta cuja
  `pasta` é uma subpasta só de publicação (um painel: laço bem formado, sem `laco.json` nem origem declarada dentro
  dela). Detalhes na §4.6 da proposta, item 19.
- **Pedidos** (`POST /api/caixa` com `tipo: alteracao-laco`): validados contra o `laco.json` e as fontes atuais
  (ids, faixa, opções, itens, capacidade, execução, revisão; `409 laco-mudou` traz `conflito` com "você viu /
  agora está / você pediu"). O `.md` nasce com `estado: nova` e as chaves de desfecho vazias; o agente grava o
  estado e o recibo. O portal valida o recibo na leitura (`recibo.valido`, `erros`) e nunca o mostra como aplicado
  quando inválido.
- **Aviso**: o pedido entra na mesma fila. A linha diz "alteração de laço: <título do laço>, <operação>; <caminho>"
  e, quando o aviso tem uma, a instrução final ganha "nas alterações de laço, grave o desfecho conforme a §4.5". Um
  `.md` de alteração em qualquer estado **válido** diferente de `nova` confirma a entrega (o emissor e o vigia
  marcam `entregue` sem avisar); estado desconhecido não confirma nada. Entrega não é fim de trabalho: a API marca
  `trabalho_pendente` em `nova`, `lida` (menos comentários, que encerram na leitura), `aplicando`, `aplicado` com
  `efeito: aguarda` e estado desconhecido; `pedidos_abertos` conta esses da execução atual.

## Formatos que o núcleo lê

Tickets `NN-slug.md` (`# Título`, `Type:`, `Status:`, `Blocked by:`), mapa com `## Destination`,
`## Decisions so far`, `## Not yet specified` e `## Out of scope`, estratégia com uma tabela sob `### Radar`,
glossário com `**Termo**:` e `_Avoid_:`, rodadas e caixa com frontmatter simples. O detalhe do esquema da API
está em `testes/fixtures/LEIA.md`; o exemplo completo de projeto é a fixture `testes/fixtures/horta/`.

Tudo é lido como UTF-8 (BOM tolerado) e nenhum byte é substituído em silêncio: um arquivo que não é UTF-8 válido
vira um problema ("arquivo não é UTF-8 válido") e os demais continuam; `GET /api/ticket/<n>` de um ticket assim
responde `422 arquivo-ilegivel` e `GET /api/caixa/<envio>` de uma mensagem ilegível responde `422 mensagem-ilegivel`,
no formato de erro da API. Um `.json` da caixa fora da forma (tipo ou campo errado) é problema, não é indexado e
não tem a vista `.md` regerada; um registro malformado em `.avisos.json` é descartado com problema e a fila é
recomposta a partir das mensagens. `problemas[]` sai ordenado por `arquivo` e depois `mensagem`.

## Testes

Da pasta do portal:

```
python -m unittest discover -s nucleo/testes -t nucleo/testes -p "teste_*.py" -v
```

Os testes copiam a fixture para uma pasta temporária e sobem o servidor numa porta livre; nada é gravado no
repositório. Testes sobre os arquivos de um projeto específico ficam fora do núcleo (neste workspace, em
`../testes-do-projeto/`), para o núcleo continuar sem citar projeto nenhum.

## Arquivos

- `torre.py`: servidor HTTP e API (`GET /api/estado`, `/api/versao`, `/api/ticket/<n>`, `/api/caixa/<envio>`,
  `/api/aviso`, `/api/lacos`, `/api/laco/<id>`, `POST /api/caixa`, `POST /api/aviso/tentar`, `/carta/<id>/...`,
  `/`, `/web/...`).
- `leitores.py`: leitura pura dos arquivos do projeto para o esquema do estado (inclui o registro `lacos.json`).
- `lacos.py`: os laços, só leitura (`laco.json`, fontes de estado, situação, grupo, revisão, configurado × em uso,
  pedidos com recibo validado) e a validação do `POST` `alteracao-laco`.
- `caixa.py`: gravação atômica, `.md` gerado do `.json`, idempotência, reconciliação e a fila `.avisos.json`
  (`Fila.pendentes()` e `Fila.marcar()` são o ponto onde o envio do aviso se liga).
- `aviso.py`: o aviso ao agente, canal A (`Emissor`, thread do servidor) e canal B (`--vigiar`, processo separado).
- `web/`: a página (HTML, CSS, JS e fontes embarcadas).
- `testes/`: unittest e a fixture.
