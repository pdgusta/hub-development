# Portal do projeto: proposta

Autor: Designer (2026-10-14). Revisor: Prumo. Estado: **aprovada pelo Prumo para iniciar a construção (revisão 3 + ajustes finais, 2026-10-14)**; §1 e §2 alinhadas ao visual v2 construído e §4.3/§9 ao canal de aviso testado (2026-10-14). A
aprovação é do desenho; código, capturas e aviso seguem os portões de cada marco. **Laços (marco L1, 2026-10-14):**
§2.6, §4.4, §4.5, as linhas novas da §3.2, §3.4, §3.5 e §4.3 e o Anexo A: a primeira revisão do Prumo
([`revisao-lacos-L1.md`](revisao-lacos-L1.md)) não aprovou; corrigidos em 2026-10-14 pelos cinco pontos dela e pelas
respostas de fato do maestro, **voltam para revisão dirigida**; não valem como
aprovados até o parecer (brief em [`lacos-brief.md`](lacos-brief.md)).
Pedido e restrições: [`pedido.md`](pedido.md). Este arquivo é a especificação completa para quem constrói: quem
parte dele não precisa de outra conversa. Fatos do projeto só vêm dos arquivos do repositório; o que faltar,
pergunte ao maestro (terminal "Claude Code") com `maestri ask`, nunca invente.

## 1. Tema: Mesa de mapas (visual v2)

**Visual v2, aplicado nas cinco telas com aval do Gustavo e aprovado pelo Prumo em 2026-10-14**
(`revisao-visual-v2.md`). Substitui a "Torre" noturna da primeira versão, que lia mal (fundo escuro, fonte condensada,
caixa alta espaçada). Os nomes internos ficaram (`torre.py`, `torre.css`, rotas `#/torre`, `#/partidas`…); na frente
o Gustavo vê só os nomes abaixo.

O portal é uma **mesa de mapas de uma expedição, de dia**. O Gustavo é a base; o maestro e os agentes são a
expedição. A metáfora acompanha, não obriga: os nomes das telas são os conhecidos, e a expedição entra em ícones,
subtítulos e clima.

| Na mesa | No projeto |
|---|---|
| O destino, com cinco critérios numerados | o destino do mapa (os cinco critérios de aceite) |
| O caminho até o destino | a cadeia de tickets abertos, das dependências reais até o destino |
| Cartas esperando resposta da base | as rodadas do maestro (Responder) |
| Folhas de mapa | os designs (visuais HTML); o System design é a carta mestra |
| No horizonte | o "Radar" da estratégia (bom, sem uso agora, com gatilho) |
| Diário de bordo | as decisões do mapa |
| Legenda do mapa | o glossário |

É genérica: todo workspace de desenvolvimento tem destino, tickets, rodadas, designs e decisões, por isso o núcleo
serve a outros projetos.

### Linguagem visual

- **Papel de dia:** fundo creme `#f3eadb`, cartões `#fbf6ec`, linhas `#d9cdb8`, tinta quase preta `#2b2117`; barra
  lateral de madeira (`#7a4f2a`). Textura só fora das áreas de leitura.
- **Cor por papel, sempre a mesma** (contraste AA medido pelo Prumo):
  - terracota `#9c3a22`: o que espera o Gustavo (rodada aberta, botão de enviar, selo "aguardando você");
  - petróleo `#1f5f73`: o que está vivo agora (ticket em andamento, links, foco);
  - musgo `#3f6b32`: resolvido;
  - tijolo `#9b2a1c`: bloqueado, recusado ou erro;
  - pedra `#5a544b`: aberto, esperando a vez.
- **Tipografia:** títulos em **Fraunces**; texto em **Nunito Sans** (corpo 16 px); códigos e caminhos em
  **JetBrains Mono**. Piso de 14 px em tudo (chips, dicas, metadados); nada de caixa alta espaçada em conteúdo.
  Fontes embarcadas no núcleo (`@fontsource-variable` 5.3.0, licenças OFL, `vendor/VERSOES.md`); nada é baixado em
  tempo de uso.
- **Letreiro de palhetas:** números e títulos que mudam viram letra por letra (CSS/JS próprio), respeitando
  `prefers-reduced-motion`.
- **Ícones:** SVG inline desenhados no próprio núcleo; nada de biblioteca de ícones.
- **Pouco texto na superfície:** palavras-chave, ícones e números; o detalhe vai para camadas (gaveta lateral,
  faixa de leitura, expandir). Nunca código interno solto: "Q7", "R88", "T1" só aparecem ao lado do que são em
  palavras. Números de ticket aparecem pequenos, o título em palavras vem primeiro.
- **Faixa de leitura:** toda dica (passar o mouse, foco ou clique num ponto com explicação) aparece numa faixa
  própria da casca, entre a faixa de aviso e a tela, fora da área que rola, com altura fixa: sempre visível, nunca
  cobre nada. `Esc` a dispensa sem mover o foco.
- **Teclado e foco:** tudo o que aparece ao passar o mouse também aparece com foco de teclado e com clique
  (as dicas são botões). Gavetas e leitor de carta prendem o foco enquanto abertos, fecham com `Esc` e devolvem
  o foco a quem os abriu. O letreiro de tickets navega com setas.
- **Estados que o portal conhece:** `open` → aberto; `claimed` → em andamento; `resolved` → resolvido;
  `wontfix` → descartado (riscado, cinza). Qualquer outro valor → "desconhecido", em cinza, com o valor cru
  ao lado, e entra no painel de problemas (§3.6).

## 2. Telas

Navegação por uma barra lateral de madeira com seis ícones e rótulos: **Início, Tickets, Responder, Designs,
Decisões, Laços** (rotas `#/torre`, `#/partidas`, `#/autorizacoes`, `#/cartas`, `#/rumo`, `#/lacos`; voltar do
navegador funciona; Laços entrou em 2026-10-14, §2.6). Um
selo fixo no topo mostra "N aguardando você" de qualquer tela (rodadas abertas sem resposta mais as cartas que
pedem Aprovar ou Recusar, §3.2) e leva a Responder, ou à carta quando só cartas esperam; ao lado, a luz verde de
"ao vivo".

### 2.1 Início ("O caminho até o destino")

- **Cabeçalho:** "Boa tarde. Aqui está a mesa de hoje.", a data em palavras e a conta curta (tickets feitos,
  abertos, aceite do destino).
- **O caminho até o destino (o diagrama no centro):** uma faixa em colunas, da esquerda para a direita: **Já feito**
  (o número grande de resolvidos e os quadradinhos de cada um), **Agora**, **Em seguida**, **Depois**, **Por fim**
  (as camadas do plano pela dependência `Blocked by:`) e **Destino** (o destino do mapa e os cinco critérios
  numerados com a palavra-chave do `projeto.json`). Cada fio sai de quem bloqueia e chega em quem espera; os
  últimos sem dependente fecham no destino. O ticket em andamento leva o selo "estamos aqui". Cada cartão diz
  "espera N" ou "pode partir" pelos bloqueios **reais** da API (abertos e inexistentes), nunca pelo desenho; ciclo
  vira volta pontilhada em tijolo, com aviso. Escolher um ponto mostra a corrente inteira e a leitura na faixa;
  clicar abre a gaveta do ticket.
- **Os que mais abriram caminho:** os três resolvidos que mais desbloquearam outros.
- **Para responder:** as rodadas abertas (ou "Nenhuma pergunta espera você agora"), a última mensagem gravada com o
  estado do aviso ao maestro e o **próximo passo** em palavras.
- **Últimas decisões do mapa:** as mais recentes da seção "Decisions so far", uma por cartão.

### 2.2 Tickets

- **Todos os tickets:** letreiro de palhetas, uma linha por ticket com número pequeno, título, tipo (ícone +
  palavra: pesquisa, conversa, protótipo, tarefa), estado em palavra e cor, "espera por" (quantos bloqueios abertos).
- Filtros em chips (estado e tipo; o segundo clique desliga) e busca por texto no título.
- **Quem espera quem:** o grafo de todas as dependências (SVG, camadas pelo caminho mais longo, sem biblioteca), com
  os resolvidos esmaecidos; rola na horizontal em vez de encolher.
- **Gaveta do ticket** (abre à direita, não troca de tela): o Markdown do ticket renderizado, "bloqueado por" e
  "bloqueia" com títulos em palavras e clicáveis, as cartas ligadas a ele, as rodadas dele. Ações no rodapé:
  **Comentar**, **Aprovar**, **Recusar** (aprovar/recusar exigem um motivo opcional; tudo vira arquivo na caixa,
  ver §4).

### 2.3 Responder (rodadas)

- Lista à esquerda: rodadas abertas em terracota no topo; respondidas (aguardando o maestro absorver) com carimbo
  "ENTREGUE" ou "NA FILA"; absorvidas esmaecidas, por ticket.
- Rodada aberta à direita: o contexto curto, a carta ligada (miniatura que abre a carta) e as perguntas como
  cartões. Cada tipo de pergunta tem um controle (ver §4.2). A recomendação do maestro vem marcada.
- Rascunho salvo sozinho no navegador (`localStorage`, chave `torre:<nome do projeto>:<id da rodada>:<base>`)
  a cada mudança; **Enviar** grava a resposta e avisa o maestro. Depois de enviar, a rodada mostra "O que foi
  gravado" (lido do servidor, `GET /api/caixa/<envio>`, então sobrevive a recarregar) e o estado do aviso.
- **Fluxo de envio:** a página gera o `envio` (UUID v4) e guarda corpo + `envio` junto do rascunho. Falha de
  rede ou erro 5xx → "tentar de novo" reenvia **o mesmo corpo com o mesmo `envio`**. Depois de um envio aceito,
  qualquer alteração vira **"Corrigir resposta"**: novo `envio`, corpo novo, e o servidor grava com
  `substitui:` apontando para o anterior.
- **Emenda (proposta editável):** a proposta vira uma tabela de cartões editáveis: editar célula, ligar e
  desligar linha, reordenar (arrastar e setas), adicionar e remover; um painel mostra "o que mudou" em
  palavras, e "Desfazer tudo" volta à versão do maestro.

### 2.4 Designs

- Topo: o **System design** como **Carta mestra**, grande, com a data da última mudança. Ele mora aqui (rota
  `#/cartas/system-design`); o arquivo continua no mesmo caminho e o portal "System design" do canvas pode
  apontar para o portal. O portal só o mostra: a página muda apenas quando um ticket que mexe no desenho é
  resolvido, com a data (regra do `map.md`), e quem muda é o Designer a pedido do maestro.
- **Cartas de navegação:** grade das outras cartas com miniatura viva (iframe em escala, carregada sob demanda),
  título, propósito em uma linha, o ticket e a decisão a que serviu, data. Agrupadas por ticket na ordem do plano.
- Cada carta tem uma **situação**: `vigente` (o desenho de hoje) ou `histórica` (serviu a uma rodada que o
  desenho já superou). Carta substituída por outra (campo `substitui` da nova) vira histórica sozinha, com o selo
  "substituída" e a ligação para a nova (§3.7). Históricas ficam no **Arquivo de cartas**, em tom de madeira, com o selo "histórica".
  A data mostrada diz o que é: "arquivo mudado em" (data de modificação) ou "feita em" (só quando um
  comentário de ticket dá a data).
- **Leitor de carta:** a carta em tela cheia dentro do portal (iframe), com uma tira fina com o propósito, o
  ticket, a data e **Comentar esta carta**.

### 2.5 Decisões

- **No horizonte:** os itens do "Radar" da estratégia como ecos numerados sobre o papel, com a lista ao lado; foco
  ou passar o mouse mostra o tema e o gatilho que o traz de volta.
- **Diário de bordo:** as decisões do mapa, da mais recente à primeira (título em palavras + resumo ao expandir).
- **Fora do mapa:** "Not yet specified" e "Out of scope" do mapa, em duas colunas curtas.
- **Legenda do mapa:** termos do `GLOSSARY.md`; os termos aparecem sublinhados em pontilhado em qualquer tela e
  mostram a definição na faixa de leitura.

### 2.6 Laços (marco L1, 2026-10-14)

Decisão do Gustavo no ticket 55: ver todos os laços e **pedir** (girar controles, pedir parada e pausa), com opções
e comentário por nó e pelo laço inteiro. Forma da carta aprovada `portal-lacos-proposta`. **Fora desta fase:** suítes
de teste (vêm depois dos laços de pesquisa) e o esboço a lápis (nós novos, religações, notas adesivas). O portal só
lê os arquivos do laço e grava pedidos na caixa; quem muda o laço é o maestro (§4.4, §4.5).

- **Rotas:** `#/lacos` (lista + o laço escolhido) e `#/lacos/<id do laço>`. Subtítulo "o que roda por trás".
- **Lista à esquerda, em três grupos** (regra exata em `grupo`, §3.4): **Espera você** (terracota: o ticket do laço
  tem rodada aberta que ainda não foi respondida na versão atual, ou um pedido da execução atual está em conflito e
  ainda não foi substituído), **Em voo** (petróleo) e **Terminados** (musgo, esmaecidos). Em voo, a **situação** do
  laço vira selo em palavras (§4.4): "rodando", "esperando cota" (o despachante não tem modelo apto), "sem sinal",
  "parado" (parada gravada, execução ainda não dada por terminada) ou "estado desconhecido". Cada linha: título em
  palavras, ticket pequeno, "sinal há N min" ou "terminou em <data>" e um número-chave. `laco.json` malformado: a
  linha fica, com selo "malformado" e o erro, sem controles.
- **Cabeçalho do laço:** título, ticket, execução, situação, último sinal (hora e fonte) e os botões **Pedir parada** e
  **Pedir pausa**, que só existem para as capacidades que o laço declara (§4.4); o que não foi declarado não vira
  botão. Ao lado da parada, sempre: "até valer, chamadas em voo ainda gastam cota". Laço terminado: nenhum botão de
  pedido, só comentário.
- **Fluxo de nós (o diagrama no centro):** os nós do `laco.json` com forma e ícone pelo papel: **etapa** = cartão
  cheio; **decisão** = losango, com a volta "repete" desenhada em arco (as ondas são repetição com condição de
  parada, não fila); **controle** = botão redondo preso por fio tracejado ao nó que condiciona; **observador** = olho,
  ligado por linha pontilhada "observa", fora da cadeia causal; **fora dos scripts** = cartão em tom de madeira com
  ícone de pessoa, depois de uma linha "fora dos scripts". Cada ligação leva uma palavra. Cada nó mostra até dois
  contadores, cada um com a hora da fonte. Nó com pedido aberto leva o envelope terracota tracejado; o valor do nó
  continua o configurado.
- **Gaveta do nó** (à direita, como a do ticket: prende o foco, `Esc` fecha e devolve o foco):
  - **Estado real:** os contadores do nó, cada um com "fonte · hora"; fonte ilegível aparece como "ilegível" com o
    motivo, nunca zero.
  - **Controles e opções do nó** (opções como modelo e harness são controles do tipo escolha ou lista), cada um em
    três linhas separadas:
    - **configurado** (linha cheia, petróleo): "lido de <fonte> às HH:MM" ou "declarado pelo maestro";
    - **em uso**: "confirmado (<como>)", "relido pelo laço a cada ciclo" ou **"não confirmado"** (pedra). O valor
      configurado nunca aparece como efetivo só porque o arquivo é legível: o processo pode ter subido com outro
      valor ou não ter sido religado (§4.4);
    - **sua proposta** (campo tracejado terracota, com a faixa, as opções ou os itens, a unidade e "vale agora | na
      próxima onda | ao reiniciar o processo | na próxima execução"). Lista: os itens em fichas com "remover" e um
      campo "adicionar". **Pedir ao maestro** grava um envio `alteracao-laco` (§4.5). O nó nunca mostra o valor
      proposto como se valesse.
  - **Comentário do nó:** campo de texto e **Enviar comentário** (`comentario-no`).
  - **Pedidos deste nó:** cada um com o estado (abaixo), do mais novo ao mais velho; os substituídos ficam no
    histórico com o desfecho deles.
- **Comentário do laço inteiro:** no rodapé do fluxo, "Para o laço todo", campo e **Enviar comentário**
  (`comentario-laco`).
- **Estados de um pedido**, em palavras e cor, no nó e na gaveta: **enviado** → **lido** ("lido, sem desfecho há N
  min" quando demora) → **aplicando** → **aplicado** (com o recibo: antes → depois e quando valeu; "aguarda efeito:
  <quando>" enquanto não valeu; "configuração gravada; efeito não confirmado" quando o maestro não pôde confirmar) |
  **recusado** (com o motivo) | **conflito** ("você viu X · agora está Y · você pediu Z", com **Propor de novo**, que
  abre um envio novo ligado ao anterior) | **encerrado sem aplicar** (com o motivo). Recibo inválido nunca aparece
  como "aplicado": aparece "recibo inválido" em tijolo, com o erro.
- **Rascunho e envio:** o mesmo fluxo da §2.3 (UUID gerado na página, falha de rede reenvia o mesmo corpo com o
  mesmo `envio`); rascunho no `localStorage`, chave `torre:<nome do projeto>:laco:<id>:<execução>`. O redesenho
  periódico respeita `data-preservar` (§3.7): campo em edição não é trocado.
- **Atualização:** a tela lê `GET /api/lacos` e, com um laço aberto, `GET /api/laco/<id>` a cada 10 s, só enquanto
  está aberta (§3.4).

**Como a tela ficou (marco L3, 2026-10-14; `nucleo/web/telas/lacos.js`).** Lista por grupo à esquerda; à direita o
cabeçalho do laço, o fluxo, e embaixo "Para o laço todo" e "Pedidos"; a gaveta do nó abre por cima, à direita (rota
`#/lacos/<id>?no=<nó>`, elemento próprio `#gaveta-no`). Decisões de detalhe, para outro construtor não fazer diferente:

1. **Fluxo em faixas, com distância:** em cima os botões (`controle`, botão redondo) e os painéis (`observador`, olho
   tracejado), cada um sobre o(s) nó(s) que liga, com o texto à direita do ícone; no meio etapas e decisões em colunas
   pelo caminho mais longo da cadeia (voltas cortadas na ordem do `laco.json`); logo abaixo de um nó, num tom de
   madeira, o trabalho humano que ele **consulta no meio da volta** (um nó `fora-dos-scripts` que recebe de um nó e
   devolve ao mesmo, ex. "Ambíguos"): desce pelo vão à direita e volta pelo vão à esquerda, sem cruzar nada; depois a
   pista das voltas (`repete`, ou ligação para trás), por baixo de tudo, cada uma com pista própria; e a faixa de
   madeira "fora dos scripts" com o trabalho humano depois do laço, em que cada grupo corre da esquerda para a direita
   a partir da coluna de quem o alimenta (recua se passar da largura; outra linha se disputar coluna), rótulo no
   rodapé. Toda linha que sobe ou desce passa pelo vão entre colunas, afastada do texto medido de cada nó, com 26 px
   entre linhas vizinhas. A pílula da palavra desliza pela própria seta até não tocar linha alheia, texto, envelope
   ou outra pílula (a prova confere isso). Em 1600 px os laços deste projeto cabem inteiros; quando não cabem (1280
   px), o fluxo rola dentro do quadro, a borda direita esmaece e um selo "rola →" avisa que continua.
2. **Sob cada nó, só palavra-chave inteira:** o título, até dois contadores como "valor + palavra-chave" ("267 modelos
   usados", "5.526 itens", "2.916 pedidos", "onda 6", "21,7% novos" com barrinhas da série) e o primeiro botão em
   petróleo ("+N" se houver mais; "1 botão" quando ele é uma lista). Rótulo longo vira a forma curta (até a vírgula ou
   a primeira palavra de ligação); se ainda não couber em 22 caracteres, quebra em duas linhas; **nunca reticências**.
   Sem a hora da fonte sob o nó: ela fica na faixa de leitura (com o rótulo completo) e na gaveta; o cabeçalho já tem
   o sinal ou o término. Número ilegível vira o selo "ilegível" em tijolo. Ícone da etapa pela palavra do título
   (plano, despachante, geradores, juntador, conferência, auditoria, síntese; senão uma caixa). Pedido aberto do nó =
   envelope terracota tracejado acima do nó, a 16 px ou mais dele; conflito atual = envelope cheio com "!". O nó
   inteiro (ícone e texto) responde ao clique. Na lista e no cabeçalho, o ticket aparece só como "ticket 54"; o título
   dele vai para a faixa de leitura.
3. **Contador do topo:** conflito de laço **não** entra no "N aguardando você" (a §2 conta rodadas e cartas; contá-lo
   exigiria ler `/api/lacos` em toda tela, contra a §3.4); a rodada aberta do ticket do laço já entra por ser rodada.
   Na tela, o laço em "espera você" mostra o porquê numa faixa terracota (a rodada, com link; ou o pedido em conflito).
4. **Substituição automática:** um `mudar-controle` novo substitui o pedido ainda aberto (`nova`, `lida` ou `conflito`,
   não substituído) do mesmo botão; parada, pausa e retomada substituem uma à outra; comentário nunca. A tela avisa
   "substitui o seu pedido anterior". "Propor de novo" (num conflito do maestro) abre o nó com o valor pedido e liga
   ao pedido em conflito. **Sem referência velha** (revisão do Prumo, 2026-10-15): o rascunho não guarda o alvo de
   `substitui`; guarda só qual alvo a tela mostrou. Na hora de enviar a tela relê o laço e recalcula o alvo. Se ele
   não é mais o que foi mostrado (o maestro deu desfecho enquanto o Gustavo escrevia), ou se a torre responde 400
   `substitui-invalido`, nada sai em silêncio: a tela diz em palavras o que houve ("o pedido que este substituiria, o
   de 01h33 (… para 250 células), já teve desfecho: recusado (motivo: …)") e oferece "Enviar como pedido novo" (UUID
   novo, sem referência) ou, se houver outro pedido aberto do mesmo grupo, "Enviar substituindo o de HH:MM", dizendo
   qual. Valor e texto ficam; a escolha sobrevive à recarga. Vale igual para parada, pausa e retomada. O "tentar de
   novo" de um erro ambíguo de rede não muda: reenvia o mesmo corpo com o mesmo `envio`.
5. **Rascunho:** só nasce quando o Gustavo mexe; `antes` e `revisao` são os que ele viu ao começar. Se a configuração
   muda enquanto ele escreve, a tela avisa e o envio dá 409; aí "Propor sobre o valor atual" refaz o rascunho sobre o
   configurado e a revisão atuais (envio novo), mantendo o valor pedido. 409 com `definicao_mudou: true` diz "a regra
   deste botão mudou"; `null`, "a configuração ou a regra do laço mudou; o portal não sabe qual". Os 400 mais
   prováveis aparecem em palavras pelo código (sem ids crus); erro de rede ou 5xx guarda o corpo e "Tentar de novo"
   reenvia o mesmo `envio`.
6. **Estados na tela:** "lido, sem desfecho há N min" a partir de 10 min contados do envio (a API não dá a hora da
   leitura); trilha enviado → lido → aplicando → aplicado nos pedidos de mudança e parada; comentário lido = musgo.
   Pedidos: os 5 mais novos à mostra, o resto recolhido. Pedido de execução anterior e substituído ficam esmaecidos.
7. **Situação em cor:** rodando = petróleo; esperando cota e parado = pedra; sem sinal e estado desconhecido = pedra
   tracejado; terminado = musgo; malformado = tijolo. Laço terminado: "só leitura", sem botões de pedido e sem "sua
   proposta" na gaveta; os comentários continuam. "Pedir retomada" só existe com `pausar-retomar` e nunca é descrito
   como retomada feita.

## 3. Arquitetura

### 3.1 Forma

Um **servidor local pequeno em Python 3.12, só biblioteca padrão** (`http.server.ThreadingHTTPServer`), mais
uma **página única** em HTML, CSS e JavaScript puros (módulos ES, sem etapa de build). O servidor lê os
arquivos do repositório a cada pedido (nada de banco, nada de cache que minta), devolve JSON e grava só na
caixa. Escuta **apenas em `127.0.0.1`**, porta da configuração (8770 neste projeto).

**Tudo embarcado, nada de CDN em tempo de uso.** Na construção, baixe uma vez para `nucleo/web/vendor/`:
`marked@12.0.2` e `dompurify@3.1.6` (de cdnjs.cloudflare.com) e as fontes em woff2 de `@fontsource`
(cdn.jsdelivr.net/npm, versão exata): no visual v2, `@fontsource-variable` 5.3.0 de Nunito Sans, Fraunces e
JetBrains Mono (as da primeira versão, Big Shoulders Display e IBM Plex, saíram). Registre versão, URL de origem e licença de cada um em `nucleo/web/vendor/VERSOES.md`
e copie os arquivos de licença (MIT para marked, Apache-2.0/MPL-2.0 para DOMPurify, OFL para as fontes).
O portal fica completo sem internet.

### 3.2 Núcleo genérico, conteúdo do projeto e base dos caminhos

```
.scratch/context-hub/portal/          ← "pasta do portal" (onde está o projeto.json)
  pedido.md, proposta.md, construcao.md
  projeto.json      TUDO o que é deste projeto
  cartas.json       registro dos designs
  lacos.json        registro dos laços (o maestro escreve; §4.4)
  rodadas/          o maestro escreve
  caixa/            o portal escreve (o maestro só troca "estado:"; em alteracao-laco, também o desfecho, §4.5)
  conferencia/      PNGs da conferência visual
  iniciar.cmd       sobe o servidor deste projeto
  nucleo/           genérico, copiável para outro workspace sem mudar uma linha
    torre.py        servidor e API          (python nucleo/torre.py <caminho do projeto.json>)
    leitores.py     mapa, tickets, estratégia, glossário, rodadas, cartas
    caixa.py        gravação atômica, idempotência
    aviso.py        fila persistente de avisos ao agente
    web/            index.html, torre.css, torre.js, telas/*.js, icones.js, vendor/
    testes/         unittest + fixtures (um mini-projeto falso completo)
    LEIA.md         instalar o portal noutro workspace
```

**Bases de caminho, sem exceção:**

- `projeto.json` → `raiz` é relativa à pasta do portal; todo outro caminho do `projeto.json` é relativo a
  `raiz`, exceto `rodadas`, `caixa` e `cartas`, relativos à pasta do portal.
- `cartas.json` → `arquivo` e `pasta` relativos a `raiz`.
- `projeto.json` → `lacos` (opcional, desde 2026-10-14) é relativo à pasta do portal, como `cartas`; ausente = a
  tela Laços diz "nenhum laço registrado". `lacos.json` → `pasta` relativa a `raiz`. `laco.json` → todo caminho é
  relativo à pasta do laço (§4.4).
- Rodada → `carta:` é o **id** de uma carta do `cartas.json`, nunca um caminho.
- Toda resolução usa `os.path.realpath` (segue symlink e junction) e exige
  `os.path.commonpath([alvo, base_permitida]) == base_permitida`; fora disso, 404.

`projeto.json` deste projeto:

```json
{
  "nome": "Context hub",
  "raiz": "../../..",
  "porta": 8770,
  "mapa": ".scratch/context-hub/map.md",
  "tickets": ".scratch/context-hub/issues",
  "estrategia": ".scratch/context-hub/estrategia-pos-pesquisa.md",
  "glossario": "GLOSSARY.md",
  "rodadas": "rodadas",
  "caixa": "caixa",
  "cartas": "cartas.json",
  "criterios": [
    {"palavra": "acha"},
    {"palavra": "grava sozinho"},
    {"palavra": "Obsidian e disco"},
    {"palavra": "sem divergência"},
    {"palavra": "edição concorrente"}
  ],
  "aviso": {"agente": "Claude Code", "executavel": "maestri"}
}
```

O texto inteiro de cada critério vem da lista numerada da seção `## Destination` do mapa; o `projeto.json`
só dá a palavra-chave da luz, na mesma ordem. Se as contagens não baterem, o portal mostra as luzes com o
texto do mapa e registra o problema.

`cartas.json`: uma entrada por visual. O construtor preenche a partir dos tickets e do mapa que citam o
arquivo (`grep` por `.html` em `issues/*.md` e `map.md`); campo sem fonte fica `"a confirmar"` e vira
pergunta ao maestro. Nunca suposição.

```json
[
  {
    "id": "system-design",
    "titulo": "System design",
    "arquivo": ".scratch/context-hub/system-design.html",
    "pasta": ".scratch/context-hub",
    "proposito": "o desenho do hub de bater o olho",
    "ticket": null,
    "decisao": "a confirmar",
    "data": {"valor": "2026-10-13", "tipo": "modificado"},
    "situacao": "vigente",
    "mestra": true
  }
]
```

- `pasta` é a raiz dos arquivos que a carta pode carregar (scripts, `dados.js`). O leitor de cartas serve um
  arquivo de `/carta/<id>/<relativo>` só se passar **todas** estas regras:
  1. o caminho real (`realpath`, seguindo symlink e junction) fica dentro da `pasta` da carta;
  2. a extensão está na lista permitida: `.html .htm .js .mjs .css .json .svg .png .jpg .jpeg .gif .webp
     .woff .woff2 .ttf .mp3 .mp4 .webm`; nada de `.md`, `.py`, `.cmd`, `.txt` ou sem extensão;
  3. o caminho real não está dentro da pasta do portal (o que inclui `rodadas/`, `caixa/`, `projeto.json`,
     `cartas.json`), nem é um arquivo do `projeto.json` (mapa, estratégia, glossário), nem fica dentro da
     pasta de tickets, nem tem um componente que comece com ponto.
  Assim a carta mestra, cuja `pasta` é `.scratch/context-hub` inteira, não expõe `map.md` nem a caixa. Para
  `laco/painel/*.html`, `pasta` é `.scratch/context-hub/laco/painel`.
- `data.tipo` é `modificado` (data do arquivo) ou `feita` (data dada por comentário de ticket).
- `pede_veredito: true` (opcional; desde 2026-10-14) marca a carta que espera o Gustavo Aprovar ou Recusar (as
  amostras). Ela conta no "aguardando você" do topo, aparece em "Para responder" no Início e leva o selo "espera
  Aprovar ou Recusar" na grade e no leitor enquanto for vigente (`situacao_efetiva`), não for a mestra e não houver
  na caixa uma `aprovacao` dela (não substituída). Basta gravar o veredito na caixa para sair da conta; o maestro
  depois atualiza `situacao` e `decisao`. Regra só da tela (`app.cartasAguardando` em `web/torre.js`); o núcleo
  repassa a chave como as outras desconhecidas.
- Visuais de hoje: `system-design.html`, `mapeamento.html`, `prototipos/prototipo-08-divergencia.html`,
  `prototipo-09-busca.html`, `prototipo-09-busca-desenho-novo.html`, `prototipo-09-roteamento-da-pesquisa.html`,
  `prototipo-10-contrato.html`, `prototipo-12-pastas.html`, `laco/painel/index.html`, `etapas.html`,
  `sintese.html`. Pistas já levantadas: o protótipo 08 serve a "Divergência e edição concorrente"; os 09 a
  "Camada de busca" (o de roteamento também a "Pesquisa ampla"); o 10 a "Contrato file-first"; o 12 a
  "Arquitetura de pastas e frontmatter"; o painel do laço a "Montar os scripts do laço" e "Pesquisa ampla".
  A situação (vigente ou histórica) de cada protótipo é pergunta ao maestro.

### 3.3 Leitores (formatos de entrada)

- **Tickets:** um arquivo `NN-slug.md` por ticket. `# Título` na primeira linha; linhas `Type:`, `Status:`,
  `Blocked by:` (números separados por vírgula) antes da primeira seção `##`. O número vem do nome do arquivo.
- **Mapa:** seções `## Destination` (parágrafo + lista numerada = critérios), `## Decisions so far` (itens
  `- [Título](issues/NN-slug.md): resumo`, em ordem), `## Not yet specified`, `## Out of scope`, `## Notes`.
- **Estratégia:** a tabela Markdown sob `### Radar` (colunas tema e gatilho).
- **Glossário:** `**Termo**:` seguido do parágrafo de definição; `_Avoid_:` vira "evite".
- **Frontmatter aceito (rodadas e caixa):** bloco entre a primeira linha `---` e a próxima `---`; uma
  `chave: valor` por linha; chave `[a-z_]+`; valor é texto até o fim da linha, sem aspas obrigatórias (aspas
  simples ou duplas em volta são tiradas); sem listas, sem aninhamento, sem multilinha. Chave desconhecida é
  ignorada; linha fora desse formato torna o arquivo malformado.

### 3.4 API

Toda rota `/api/*` responde JSON UTF-8 (as rotas `/`, `/web/*` e `/carta/*` servem HTML, CSS, JS, fontes e
imagens com o tipo certo). Erros da API: `{"erro": "<código>", "mensagem": "<em palavras>", "campo": "<opcional>"}`.

| Método e rota | Faz |
|---|---|
| `GET /` e `/web/<arquivo>` | a página e os estáticos do núcleo |
| `GET /api/estado` | tudo de uma vez (esquema abaixo) |
| `GET /api/ticket/<numero>` | `{"numero": "09", "markdown": "..."}` |
| `GET /api/versao` | `{"versao": "<sha1 das (caminho, mtime, tamanho) lidos>"}`; a página consulta a cada 3 s |
| `GET /carta/<id>/` e `/carta/<id>/<relativo>` | serve a carta e os arquivos da `pasta` dela; id fora do `cartas.json` → 404 |
| `POST /api/caixa` | grava uma mensagem e enfileira o aviso; devolve `{"envio", "arquivo", "repetido": bool}` |
| `GET /api/caixa/<envio>` | o `.json` completo daquela mensagem, mais `estado` (do `.md`) e `aviso` |
| `GET /api/aviso` | `{"disponivel": true, "motivo": null, "canal": "ask", "fila": [...]}` |
| `POST /api/aviso/tentar` | corpo `{"envio": "<uuid>"}`; põe um aviso `falhou` de volta em `pendente`; 404 se não existe |
| `GET /api/lacos` | o resumo de cada laço do `lacos.json` (esquema abaixo); laço com `laco.json` ruim vem com `problema` |
| `GET /api/laco/<id>` | um laço inteiro: descrição, configurados e em uso, contadores, revisão, capacidades e os pedidos dele com estado e recibo; id fora do `lacos.json` → 404 `laco-inexistente`; `laco.json` ilegível ou malformado → 422 `laco-malformado` |

O pedido de alteração de laço **não tem rota própria**: é um tipo novo do mesmo `POST /api/caixa`
(`tipo: alteracao-laco`, §4.5), com a mesma idempotência, os mesmos cabeçalhos exigidos e a mesma gravação da §3.5.
Os laços não entram em `GET /api/estado`, e **as fontes de estado dos laços não entram em `GET /api/versao`**: os
números mudam a cada segundo e fariam a página inteira se redesenhar sem motivo. `GET /api/versao` passa a incluir
só os descritores, o `lacos.json` e cada `laco.json` (mudança de desenho); a tela Laços lê as duas rotas próprias a
cada 10 s enquanto está aberta. As mensagens `alteracao-laco` aparecem em `caixa` do estado como as outras.

`GET /api/lacos`:

```json
[{"id": "modelos-de-embeddings", "titulo": "Modelos de embeddings da busca", "ticket": "54",
  "execucao": "embeddings-2026-10-14", "grupo": "em-voo", "situacao": "rodando", "terminou_em": null,
  "ultimo_sinal": {"hora": "2026-10-14T21:12:40-03:00", "fonte": "estado/despachante.json"},
  "destaque": {"rotulo": "tentativas", "valor": 1684}, "pedidos_abertos": 1, "problema": null}]
```

`grupo` ∈ {`espera-voce`, `em-voo`, `terminado`}, nesta precedência:

1. `terminado` se `execucao.terminou_em` está preenchido (prioritário: laço terminado nunca "espera você");
2. `espera-voce` se (a) o ticket do laço tem rodada `aberta`, legível (não malformada) e **não respondida na versão
   atual** (regra de `respondida` da §3.7), ou (b) existe pedido do laço em `conflito` que é **atual e acionável**:
   da execução atual, sem envio posterior que o `substitui`, e com o laço não terminado;
3. senão `em-voo`.

`situacao` é a do laço (§4.4: `rodando`, `esperando-cota`, `sem-sinal`, `parado`, `terminado`, `desconhecido`),
independente do grupo. `destaque` é o primeiro contador do `laco.json`. `pedidos_abertos` conta os pedidos da
execução atual em `nova`, `lida`, `aplicando` ou `aplicado` com `efeito: aguarda`.

`GET /api/laco/<id>` (resumido):

```json
{"id": "modelos-de-embeddings", "titulo": "...", "ticket": "54",
 "execucao": {"id": "embeddings-2026-10-14", "inicio": "2026-10-14T20:36:47-03:00", "terminou_em": null},
 "grupo": "em-voo", "situacao": "rodando", "lido_em": "2026-10-14T21:13:02-03:00",
 "ultimo_sinal": {"hora": "...", "fonte": "estado/despachante.json"},
 "revisao": "<sha256, §4.4>",
 "nos": [{"id": "parada", "titulo": "Parada", "papel": "decisao", "detalhe": "...", "carta": null}],
 "ligacoes": [{"de": "parada", "para": "geradores", "palavra": "repete", "tipo": "repete"}],
 "controles": [{"id": "trabalhadores_por_gerador", "no": "geradores", "rotulo": "...", "tipo": "inteiro",
                "faixa": [1, 40], "unidade": "trabalhadores", "quando_vale": "ao-reiniciar", "releitura": "ao-ligar",
                "configurado": {"valor": 20, "como": "lido", "fonte": "config.json → trabalhadores_por_gerador",
                                "hora": "...", "ilegivel": null},
                "em_uso": {"estado": "nao-confirmado", "valor": null, "como": null}}],
 "capacidades": [{"id": "parar-apos-onda", "onda_atual": 2}, {"id": "parar-de-despachar"}],
 "contadores": [{"id": "tentativas", "no": "teto", "rotulo": "tentativas", "tipo": "inteiro", "valor": 1684,
                 "fonte": "estado/laco.db → uso (soma de tentativas)", "hora": "...", "ilegivel": null}],
 "pedidos": [{"envio": "<uuid>", "arquivo": "...", "operacao": "mudar-controle", "no": "parada",
              "controle": "gate_novos", "antes": {"tipo": "numero", "valor": 0.15},
              "depois": {"tipo": "numero", "valor": 0.1}, "enviada": "...", "substitui": null,
              "substituido_por": null, "estado": "aplicado",
              "recibo": {"valido": true, "erros": [], "aplicado_em": "...", "efeito": "aguarda", "...": "..."},
              "aviso": "entregue"}],
 "problemas": []}
```

`configurado.como` ∈ {`lido`, `declarado`}; `em_uso.estado` ∈ {`confirmado`, `relido`, `nao-confirmado`} (regra na
§4.4); `recibo.valido: false` traz `erros` em palavras (§4.5).

`GET /api/estado` (resumido):

```json
{
  "projeto": {"nome": "Context hub", "gerado_em": "2026-10-14T15:30:00-03:00"},
  "destino": {"texto": "...", "criterios": [{"n": 1, "palavra": "acha", "texto": "..."}]},
  "tickets": [{"numero": "09", "titulo": "Camada de busca", "tipo": "prototype", "estado": "claimed",
               "estado_cru": "claimed", "bloqueado_por": ["04", "19"], "bloqueios_abertos": [],
               "bloqueia": ["11", "16"], "cartas": ["prototipo-09-busca"], "arquivo": "issues/09-camada-de-busca.md"}],
  "plano_de_voo": {"camadas": [["09", "32"], ["11"], ["12", "14"], ["15"], ["16"], ["17"]], "ciclos": []},
  "decisoes": [{"numero": "05", "titulo": "...", "resumo": "..."}],
  "fora": {"nao_especificado": ["..."], "fora_do_escopo": ["..."]},
  "radar": [{"tema": "...", "gatilho": "..."}],
  "glossario": [{"termo": "Par", "definicao": "...", "evite": "host, servidor, mestre"}],
  "cartas": [{"id": "system-design", "...": "...", "url": "/carta/system-design/"}],
  "rodadas": [{"id": "2026-10-14-camada-de-busca-r5", "titulo": "...", "ticket": "09", "aberta": "2026-10-14",
               "estado": "aberta", "respondida": false, "base": "<sha256 do arquivo>", "carta": "prototipo-09-busca",
               "contexto": "...", "perguntas": [{"id": "faz-agora", "titulo": "...", "tipo": "escolha",
               "recomendada": ["A"], "opcoes": [{"chave": "A", "texto": "..."}], "porque": "...",
               "proposta": null}]}],
  "caixa": [{"arquivo": "2026-10-14-153210-412-resposta-camada-de-busca-r5-7f3a.md", "tipo": "resposta",
             "alvo": "rodada 2026-10-14-camada-de-busca-r5", "estado": "nova", "aviso": "entregue"}],
  "aviso": {"disponivel": true, "motivo": null},
  "problemas": [{"arquivo": "issues/53-x.md", "mensagem": "Status desconhecido: \"parked\""}]
}
```

`POST /api/caixa`, corpo (um dos quatro tipos; o quarto, `alteracao-laco`, está na §4.5):

```json
{
  "envio": "b9c4e2d0-5d1e-4c36-9f0a-1f0a2a6c2e11",
  "tipo": "resposta",
  "rodada": "2026-10-14-camada-de-busca-r5",
  "base": "<sha256 que veio no estado>",
  "respostas": {
    "faz-agora": {"escolha": ["A"], "outra": null, "comentario": "só depois do teste"},
    "formatos": {"escolha": ["md", "txt", "pdf"], "outra": null, "comentario": null},
    "roteamento": {"linhas": [{"id": "gerar", "ativa": true, "valores": {"etapa": "gerar", "...": "..."}}],
                   "comentario": null},
    "pode-iniciar": {"veredito": "aprovado-com-ajuste", "comentario": "rodar só em pt primeiro"},
    "algo-mais": {"texto": null}
  }
}
```

```json
{"envio": "<uuid>", "tipo": "comentario", "alvo": {"tipo": "ticket", "id": "09"}, "texto": "..."}
{"envio": "<uuid>", "tipo": "aprovacao", "alvo": {"tipo": "carta", "id": "prototipo-12-pastas"},
 "veredito": "recusado", "texto": "motivo"}
```

Validação no servidor (falhou → 400 com `campo`):

- `envio` é UUID; `tipo` ∈ {resposta, comentario, aprovacao, alteracao-laco}; corpo ≤ 256 KiB; texto livre
  ≤ 20 000 caracteres por campo. As regras próprias de `alteracao-laco` estão na §4.5.
- `rodada` existe, tem `estado: aberta` e `base` igual ao sha256 atual do arquivo; senão **409**
  `rodada-mudou` (a página guarda o rascunho e mostra a rodada nova lado a lado).
- Cada chave de `respostas` é um `id` de pergunta da rodada; pergunta ausente = **em branco**, nunca a
  recomendação. Uma resposta só com perguntas em branco é recusada (`nada-respondido`).
- `escolha`: chaves existentes; `escolha` (tipo) aceita uma, `varias` aceita uma ou mais; `outra` é texto
  livre opcional ("nenhuma destas, e sim…") e pode vir sozinha.
- `aprovar`: `veredito` ∈ {aprovado, aprovado-com-ajuste, recusado}; `aprovado-com-ajuste` e `recusado`
  exigem `comentario`.
- `proposta`: toda linha tem `id`; ids da rodada que somem = removidas; ids novos são `nova-1`, `nova-2`…;
  `ativa: false` = desligada (fica na versão, marcada); ordem do array = ordem nova; `valores` só com as
  `colunas` da rodada; operação fora de `pode` → 400.
- `alvo` existe no estado do servidor (ticket pelo número, carta pelo id, rodada pelo id); `veredito` de
  `tipo: aprovacao` ∈ {aprovado, recusado}, e `recusado` exige `texto`.
- Na rodada, ids repetidos (perguntas, opções de uma pergunta, linhas de uma proposta) tornam a rodada
  malformada; no corpo, ids de linha repetidos → 400.
- **A idempotência vem antes de tudo isso** (§3.5): um `envio` já gravado responde pelo que foi gravado,
  mesmo que a rodada tenha mudado ou sido absorvida depois.
- `Host` precisa ser `127.0.0.1:<porta>` ou `localhost:<porta>` (senão 403); `POST` exige
  `Content-Type: application/json`, cabeçalho `X-Torre: 1` e `Origin` igual a `http://127.0.0.1:<porta>` ou
  `http://localhost:<porta>` (senão 403). O servidor não envia nenhum cabeçalho CORS.

### 3.5 Caixa: gravação, idempotência e recuperação

**Uma fonte só por mensagem.** O `.json` de cada mensagem é a verdade da caixa: tem o corpo validado, o
`envio`, o sha256 canônico do corpo (`corpo_hash`, de `json.dumps(corpo, sort_keys=True, ensure_ascii=False)`
sem o campo `envio`), o tipo, o alvo, a hora, o `substitui` e, numa resposta, o **retrato da rodada
original**: id, `base`, título, e de cada pergunta o id, título, tipo, opções, recomendação e a proposta-base
(colunas e linhas). O `.md` e a lista de "mudanças" são gerados só do `.json`, nunca da rodada atual, então
regerar depois de a rodada ser editada não muda o sentido da resposta. Todo o resto é derivado dele e pode ser
reconstruído:

| Peça | O que é | Se faltar ou divergir |
|---|---|---|
| `<nome>.json` | a mensagem, imutável | — (é a fonte) |
| `<nome>.md` | a vista para o maestro, gerada do `.json` de forma determinística; só o `estado:` é do maestro | regerado do `.json` no arranque |
| índice de envios | `envio → nome`, **só em memória**, montado lendo os `.json` no arranque | não existe em disco, não diverge |
| `.avisos.json` | registro do que já foi avisado: `envio → {estado, tentativas, ultimo_erro, proximo}` | ausente ou ilegível → recomeça vazio |

- **Nome:** `AAAA-MM-DD-HHMMSS-<tipo>-<slug>-<envio>` (UUID completo). `slug` vem do id da rodada ou do alvo,
  nunca de texto livre. Unicidade garantida pelo UUID.
- **Ordem de gravação** (sob um `threading.Lock`; o servidor recusa subir se a porta estiver ocupada, então há
  um processo só): (1) `.json` em `caixa/.tmp/`, `flush` + `os.fsync`, `os.replace` para `caixa/`;
  (2) `.md` do mesmo jeito; (3) índice em memória; (4) entrada `pendente` na fila.
- **Arranque (reconciliação), antes de aceitar pedidos:**
  1. apaga `caixa/.tmp/*`;
  2. lê todo `caixa/*.json`: monta o índice; `.json` inválido vai para `problemas` e é ignorado;
  3. `.json` sem `.md` (queda entre 1 e 2) → gera o `.md` com `estado: nova`;
  4. `.md` sem `.json` → `problemas` ("mensagem sem dados"), nunca apagado;
  5. todo `.md` com `estado: nova` cujo envio não está `entregue` em `.avisos.json` → `pendente` (queda entre
     2 e 4, ou servidor parado antes do aviso); `enviando` vira `pendente`.
- **Erro de I/O sem reinício:** se o passo 1 confirmou o `.json` e o 2, 3 ou 4 falhou, o `POST` registra o
  envio no índice mesmo assim, responde **500** `gravacao-parcial`, e uma tarefa de reparo (a mesma lógica do
  arranque, rodando a cada 30 s e antes de cada `POST`) completa o `.md` e a fila. O retry da página com o
  mesmo `envio` cai na idempotência e recebe `repetido: true`; nunca nasce outro arquivo.
- **Idempotência, primeira coisa do `POST`** (depois só de Host, Origin, cabeçalho e tamanho): se o `envio`
  está no índice e o `corpo_hash` é igual → **200** com `{"repetido": true}` e o arquivo já gravado, sem
  revalidar rodada, base ou estado; com `corpo_hash` diferente → **409** `envio-conflito`. Só um `envio` novo
  passa pela validação da §3.4.
- **Texto livre nunca vira estrutura:** o frontmatter do `.md` só tem valores gerados pelo servidor (e, depois, os
  que o maestro grava: o `estado:` e, só em `alteracao-laco`, as chaves de desfecho da §4.5); cada linha de texto do
  Gustavo sai prefixada por `> `. Nada que ele escreva (`---`, `estado: lida`) muda o arquivo.
- **Três estados, cada um num lugar:** *salva* = o `.json` existe; *avisada* = `entregue` em `.avisos.json`;
  *lida* = `estado: lida` no `.md` (o maestro troca). Rodada inteira absorvida: o maestro põe
  `estado: absorvida` no arquivo da rodada.
- **Corrigir resposta:** novo `envio`, novo arquivo com `substitui: <nome anterior>`; o portal mostra só o mais
  novo de cada cadeia e o maestro absorve o mais novo.
- O portal **nunca** reescreve um `.md` depois de criá-lo, exceto ao regerar um que faltava no arranque. A
  leitura do `estado:` do `.md` aceita qualquer valor que o maestro escreva (`nova`, `lida`; outro → mostrado cru).
  **Exceção, `alteracao-laco` (§4.5):** o maestro grava também as chaves de desfecho; os estados válidos são os da
  §4.5, e um estado fora deles é mostrado cru, vira problema e não confirma a entrega do aviso.

### 3.6 Falhas e casos ruins

- Cada leitor captura o erro por arquivo e devolve o que conseguiu; o problema vai para `problemas` com o
  arquivo e a mensagem em palavras. Um arquivo ruim nunca derruba a página nem as outras telas.
- Rodada malformada (frontmatter fora do formato, `tipo` desconhecido, pergunta sem `id`, JSON da proposta
  inválido): aparece na lista com selo "malformada" e o erro, sem botão de enviar.
- `Blocked by:` apontando para ticket que não existe: a aresta aparece tracejada em coral com "ticket NN não
  encontrado". Ciclo de dependência: o plano de voo quebra o ciclo na aresta de maior número para desenhar, e
  avisa em `plano_de_voo.ciclos`.
- `projeto.json` ausente ou inválido: o servidor não sobe e diz por quê no terminal.
- A página mostra um selo "⚠ N problemas" no topo; o clique abre a lista.

### 3.7 Contrato fixado na construção (2026-10-14)

Detalhes decididos ao construir os marcos 1–2 e aceitos pelo Prumo; valem sobre o texto das §3.3 a §3.5 e §4
onde divergirem, para outro construtor não implementar um contrato diferente.

**Carta substituída (2026-10-14, pedido do Gustavo):** quem cria uma carta que substitui outra grava
`"substitui": "<id da antiga>"` no `cartas.json`. Na leitura (o arquivo não é regravado) a antiga ganha
`substituida_por` e `situacao_efetiva: historica`: sai das vigentes sozinha e aparece no Arquivo de cartas com o selo
"substituída" e "substituída por <título da nova>" (abre a nova); a nova mostra "substitui <título da antiga>". Id
inexistente, auto-substituição, ciclo, `substitui` fora da forma ou carta mestra como alvo viram problema e a
ligação é ignorada; duas substitutas da mesma: vale a última no arquivo, anotado. Cadeias valem (cada uma aponta a
substituta direta).

**Rodada reescrita (2026-10-14, relato do Gustavo):** `respondida` quer dizer "respondida **na versão atual**": só
vale para rodada `aberta` cujo `base` (sha256) é igual ao `base` da resposta mais nova; se o maestro reescreve a
rodada depois da resposta, ela volta a esperar (entra no "aguardando você", carimbo MUDOU), e a resposta nova sai com
`base` novo e `substitui` a anterior. Rodada `absorvida` ou `suspensa` nunca volta a esperar; resposta sem `base`
conta como atual. **Edição protegida:** o redesenho a cada 3 s não troca nó com `data-preservar` que já está na tela
(formulário da rodada, rodapé de ações aberto, corpo da gaveta, miniatura de carta): texto, foco, cursor, seleção e
rolagem ficam; mudança na própria rodada em edição vira o aviso "A rodada mudou enquanto você escrevia".

**Leitura (§3.3, §4.1):**

- Frontmatter: linha em branco dentro do bloco é tolerada; qualquer outra linha fora de `chave: valor` torna o
  arquivo malformado.
- Rodada também é `malformada` quando: `estado` não é `aberta`, `suspensa` ou `absorvida`; `recomendada` cita
  opção inexistente; `escolha` ou `varias` sem opções; não há perguntas; uma célula da proposta não é escalar
  (texto, número, true/false ou null).
- Cada leitor captura o erro por arquivo, inclusive codificação inválida (não é UTF-8): o arquivo vira um
  problema em palavras e os demais continuam; `/api/ticket/<n>` de um ticket ilegível responde erro controlado,
  nunca 500. Nenhum byte é substituído silenciosamente.
- Confinamento: todo caminho do `projeto.json` e do `cartas.json`, e todo arquivo descoberto nas pastas de
  tickets, rodadas e caixa, passa por `realpath` + `commonpath` contra a base (raiz ou pasta do portal). Fora da
  base (caminho absoluto, `..`, symlink ou junction para fora) o item vira problema e não é lido nem gravado; a
  caixa fora da pasta do portal impede o servidor de subir.

**API (§3.4):**

- Chave desconhecida no corpo do `POST`, ou dentro de uma resposta → 400 `chave-desconhecida`.
- Rodada inexistente → 409 `rodada-mudou`; rodada malformada → 400 `rodada-malformada`;
  `Content-Type` errado → 403 `tipo-de-conteudo`.
- Comentário sozinho numa pergunta conta como respondida; "outra" sozinha também. Só a ausência de tudo é
  "em branco".
- Toda resposta de erro traz `campo` (`null` quando não há). Nas respostas, `arquivo` é o nome sem extensão.
  Os itens de `fila` em `GET /api/aviso` trazem `arquivo`. `POST /api/aviso/tentar` num aviso que não está
  `falhou` responde 200 com o registro como está.
- `GET /api/estado` junta aos `problemas` as falhas de I/O da caixa (gravação parcial, `.avisos.json` ilegível)
  e a fila e os `.json` de mensagem rejeitados na fronteira.
- HTTP/1.1 com keep-alive; `Content-Length` sempre; `Connection: close` nos 403 e 413 antes de ler o corpo.
- `GET /api/ticket/<n>` de arquivo ilegível (UTF-8 inválido ou erro de I/O) → 422 `arquivo-ilegivel`;
  `GET /api/caixa/<envio>` de mensagem ilegível → 422 `mensagem-ilegivel`. Nunca 500 por arquivo ruim.
- Carta com `arquivo` ou `pasta` fora de `raiz` (ou absoluto) fica na lista com problema e `/carta/<id>/…` → 404.
  O servidor recusa subir com `caixa` fora da pasta do portal ("não há onde gravar com segurança"); `raiz` precisa
  ser texto. Caminhos absolutos no `projeto.json` e no `cartas.json` não são aceitos.

**Caixa (§3.5, §4.2):**

- `corpo` gravado é o corpo do `POST` sem o campo `envio` (inclui `substitui` quando veio); `corpo_hash` é o
  sha256 de `json.dumps(corpo, sort_keys=True, ensure_ascii=False)` desse valor. A idempotência compara esse
  hash, isto é, o **valor JSON canônico**, não os bytes do pedido (espaços e ordem das chaves não contam).
- O `.json` traz `alvo.titulo` (título em palavras do alvo no momento do envio) além do esquema do LEIA.md,
  para o `.md` nascer só do `.json`. Numa resposta, traz o retrato da rodada (`rodada`: id, base, titulo,
  ticket, perguntas com id, titulo, tipo, recomendada, opcoes, proposta).
- Validação na fronteira de cada `.json` da caixa (tipos e forma de `envio`, `tipo`, `enviada`, `alvo`,
  `corpo`, `rodada`, `substitui`, `corpo_hash`): arquivo ruim vira problema, não entra no índice e não ganha
  `.md`, tanto no arranque quanto com o servidor no ar.
- `.avisos.json` é validado registro por registro (chave UUID, `estado`, `tentativas` inteiro, `ultimo_erro`,
  `proximo` ISO 8601); registro ruim é descartado com problema e a fila é recomposta das mensagens válidas.
- Reconciliação, passo 5: `falhou` continua `falhou` até "tentar de novo" explícito; só ausente e `enviando`
  voltam a `pendente`. `.md` sem `.json` não entra na fila. Ao ligar o emissor (marco 7), a reconciliação do
  arranque é distinta do reparo durante uma emissão ativa.
- No `.md` de resposta, a linha "versão completa" cita o caminho real do JSON: `corpo.respostas.<id>`.
- Confinamento interno da caixa (revisão dirigida de 2026-10-14): `caixa/.tmp` precisa resolver (`realpath`)
  exatamente para a `.tmp` da caixa real; atalho ou junction no lugar dela, ou `.tmp` que não é pasta, recusa o
  arranque com erro em palavras e nada fora da caixa é criado, lido, gravado ou apagado. A guarda vale em toda
  escrita (`escrever_atomico`) e na limpeza da reconciliação, não só na leitura. Um item dentro de `.tmp/` que
  seja atalho ou junction não é apagado e vira problema em `problemas[]` (nomeado por onde está, nunca pelo
  alvo). Com a `.tmp` trocada em execução, o `POST` falha sem gravar e a reconciliação registra o problema sem
  escrever.
- A validação na fronteira do `.json` de resposta cobre a estrutura interna consumida pela geração do `.md`: o
  retrato da rodada segue as regras da §4.1 (tipo conhecido, ids únicos, opções com chave e texto, recomendada
  existente, proposta-base com colunas de texto, linhas com `id` e células escalares) e `corpo.respostas` segue
  a forma da §3.4 por tipo de pergunta (chaves conhecidas, escolha com chaves existentes, veredito conhecido,
  linhas com `id` texto, `ativa` true/false e `valores` escalares em colunas da proposta). Arquivo fora disso é
  rejeitado inteiro: problema, fora do índice (`nome_de(envio)` é `None`), sem `.md`, no arranque e em execução.
- Problemas sobre um atalho ou junction encontrado dentro do projeto citam o caminho do atalho, não o do alvo.

**`projeto.json` (§3.2):**

- Campo opcional `codigos`: objeto que mapeia um prefixo de uma a três letras (`^[A-Za-z]{1,3}$`) para a
  explicação em palavras do código interno (ex.: `{"Q": "pergunta numerada das rodadas de mapeamento"}`).
  `GET /api/estado` devolve-o em `projeto.codigos`, `{}` quando ausente. Fora da forma (não é objeto, chave fora
  do padrão, valor que não é texto não vazio) o campo inteiro vira `{}` com um problema em palavras em
  `portal/projeto.json`; isso nunca impede o servidor de subir. A tela marca cada ocorrência `<prefixo><número>`
  nos textos como um botão com a explicação por foco, hover e clique (`marcarCodigos`).

**Cartas (§2.4, §3.1):**

- Uma carta é mostrada num iframe de origem opaca (`sandbox="allow-scripts"`), e o portal não emite cabeçalhos
  CORS; por isso uma carta não consegue carregar fonte por URL nem do próprio portal. Carta que precisa de fonte
  própria embute o arquivo em `data:` dentro de um CSS na sua pasta (ex.: `fontes/<carta>.css`); nenhuma carta
  registrada pode pedir nada fora de `127.0.0.1` em tempo de uso.

## 4. Interface com o maestro (o contrato entre os dois)

Regra de dono: **`rodadas/` é do maestro** (o portal só lê); **`caixa/` é do portal** (o maestro só troca o `estado:` do `.md`; em `alteracao-laco`, também as chaves de
desfecho da §4.5). Os tickets continuam a verdade: o maestro absorve a resposta no ticket dono, como hoje faz
com a nota "Rodada atual", que o portal substitui. **A pasta de cada laço é do maestro e dos scripts do laço** (o
portal só lê o que o `laco.json` declara, nunca grava ali nem executa nada); `lacos.json` é do maestro.

### 4.1 Arquivo de rodada (o maestro escreve)

Caminho: `portal/rodadas/AAAA-MM-DD-<slug-do-ticket>-r<N>.md`. O nome sem `.md` é o **id da rodada**,
estável. Uma rodada por arquivo; várias podem estar abertas.

````markdown
---
titulo: O que entra no teste de bancada da busca
ticket: 09
aberta: 2026-10-14
estado: aberta
carta: prototipo-09-busca-desenho-novo
---

Contexto em duas a quatro linhas, Markdown. Sem código interno solto.

## O que a busca faz agora
id: faz-agora
tipo: escolha
recomendada: A

- A: Só achar, sobre a vista em disco de cada máquina
- B: Busca dentro do fork do MCP do banco (3 a 7 dias)

Por quê da recomendação, Markdown livre (aparece ao expandir).

## Que formatos ela precisa achar
id: formatos
tipo: varias
recomendada: md, txt

- md: Markdown
- txt: texto
- pdf: PDF (não verificado em nenhuma candidata)

## Estratégia de roteamento dos geradores
id: roteamento
tipo: proposta

```json
{
  "colunas": ["etapa", "perfil", "motivo"],
  "linhas": [
    {"id": "gerar", "etapa": "gerar", "perfil": "auto:pesquisa", "motivo": "busca do Google"},
    {"id": "juntar", "etapa": "juntar", "perfil": "auto:smart", "motivo": "JSON estável"}
  ],
  "pode": ["editar", "reordenar", "ligar", "adicionar", "remover"]
}
```

## Pode iniciar o teste?
id: pode-iniciar
tipo: aprovar

## Algo mais?
id: algo-mais
tipo: texto
````

Regras:

- Frontmatter (formato da §3.3): `titulo`, `ticket` (número), `aberta` (AAAA-MM-DD) e `estado` obrigatórios;
  `carta` opcional (id do `cartas.json`). `estado`: `aberta` | `suspensa` | `absorvida`. "Respondida" o portal
  deduz pela caixa, o maestro não escreve.
- Cada pergunta: `## Título em palavras`, depois as linhas `id:` (obrigatório, `[a-z0-9-]+`, único na rodada,
  nunca reaproveitado para outra pergunta), `tipo:` (obrigatório) e `recomendada:` (opcional, chaves
  separadas por vírgula). O portal numera "Pergunta 1, 2…" pela ordem, nunca mostra o id.
- Tipos: `escolha` (uma opção), `varias` (uma ou mais), `aprovar` (Aprovar | Aprovar com ajuste | Recusar),
  `texto` (livre), `proposta` (tabela editável a partir do único bloco ```json da pergunta, com `colunas`,
  `linhas` com `id` único, e `pode` ⊆ {editar, reordenar, ligar, adicionar, remover}).
- Opções: linhas `- chave: texto`, chave `[A-Za-z0-9-]+`.
- Toda pergunta aceita comentário; `escolha` e `varias` aceitam também "outra resposta" em texto livre.
- Texto depois das opções (ou do bloco json) é o "por quê", mostrado ao expandir.
- O maestro pode corrigir uma rodada aberta à vontade: o portal compara o sha256 (`base`) e recusa resposta
  feita sobre a versão antiga (409), sem perder o rascunho.
- Recomendação nunca vale como resposta: o que o Gustavo não marcou sai "em branco".

### 4.2 Arquivo de resposta (o portal escreve)

Caminho: `portal/caixa/AAAA-MM-DD-HHMMSS-<tipo>-<slug>-<envio>.md` (UUID completo), com o `.json` irmão, que
é a fonte (§3.5). Exemplo do `.md`:

````markdown
---
tipo: resposta
rodada: 2026-10-14-camada-de-busca-r5
ticket: 09
enviada: 2026-10-14T15:32:10-03:00
envio: b9c4e2d0-5d1e-4c36-9f0a-1f0a2a6c2e11
estado: nova
substitui:
---

# Resposta: O que entra no teste de bancada da busca

## O que a busca faz agora
escolha: A, Só achar, sobre a vista em disco de cada máquina (a recomendada)
comentário:
> só depois do teste

## Que formatos ela precisa achar
escolhas: md, txt, pdf (a recomendada era md, txt)

## Estratégia de roteamento dos geradores
mudanças:
- linha "juntar": perfil de "auto:smart" para "auto:reliable"
- linha nova "nova-1": etapa "conferir", perfil "auto:reliable"
- linha "gerar": desligada
- ordem nova: conferir, juntar, gerar
versão completa: no .json irmão, em corpo.respostas.roteamento

## Pode iniciar o teste?
aprovação: aprovado com ajuste
comentário:
> rodar só em pt primeiro

## Algo mais?
em branco
````

Comentário e aprovação seguem o mesmo frontmatter (`tipo: comentario` ou `tipo: aprovacao`, `alvo: ticket 09`
ou `alvo: carta prototipo-12-pastas`, `veredito:` na aprovação) e o texto em citação.

### 4.3 Como o maestro fica sabendo

**Entrega pelo menos uma vez, absorção idempotente.** Qualquer canal pode repetir um aviso (nova tentativa,
reinício). Por isso o aviso só aponta arquivos, e o maestro absorve pelo arquivo: se o `.md` já está
`estado: lida`, ignora; ao absorver no ticket, cita o `envio` **completo** (UUID) no comentário, e antes de absorver
confere se o ticket já cita aquele UUID. Os 8 primeiros caracteres servem só para exibição no portal. **Exceção,
`alteracao-laco`:** `lida` é intermediário, não absorção; o pedido só sai do trabalho pendente com um desfecho
(§4.5, "Pendente de trabalho ≠ pendente de aviso"); os comentários (`comentario-no`, `comentario-laco`) já
lidos não entram nessa fila, porque a regra deles os encerra na leitura.

A fila (`.avisos.json`, §3.5) é a mesma para os dois canais candidatos abaixo. **Canal A verificado em
2026-10-14 (cinco testes reais registrados em `construcao.md`) e escolhido (§9); o canal B fica como reserva, não
testado de ponta a ponta.** Antes disso, o portal mostrava a faixa "o maestro não é avisado sozinho: diga
'respondi'"; ela continua quando o aviso está indisponível (fora do canvas).

**Como o canal A ficou, depois dos testes reais:**
- O `ask` bloqueia até o maestro ficar ocioso, inclusive quando a mensagem entra no meio de um turno (o Claude Code
  a enfileira e o maestro a lê durante o turno). Enquanto isso o registro fica `enviando`; o reparo de 30 s não mexe
  em `enviando`, só o arranque do servidor o devolve a `pendente`.
- Depois do `ask`, o `check` procura o começo da mensagem **só na caixa de digitação** do maestro (entre as duas
  últimas réguas da tela do Claude Code; sem réguas, as 6 últimas linhas). Achou → Enter; ainda lá → "(enviar)".
  Procurar na tela inteira acusava a mensagem já entregue, que fica no histórico.
- Antes de mandar, todo `pendente` cujo `.md` já está `estado: lida` vira `entregue` sem `ask` (o maestro já
  absorveu; evita aviso repetido depois de um `ask` que esgota o tempo ou de um reinício). Em `alteracao-laco`, vale
  qualquer estado **válido** da §4.5 diferente de `nova`; isso confirma só a entrega, não o fim do trabalho.
- Um `ask` em curso sobrevive à queda do servidor e entrega mesmo assim; no arranque, o registro volta a `pendente`
  e, se o `.md` já está `lida`, vira `entregue` sem reenvio.
- **Entrega provada solta a fila (correção de 2026-10-14, 23h36).** O `ask` só volta quando o maestro fica ocioso; com
  o maestro trabalhando sem parar, o `ask` das 23h32 seguia em curso e a resposta das 23h36 ficou `pendente`, sem
  tentativa, atrás da trava (um envio por vez), e o aviso dela nunca saiu. Agora, enquanto o `ask` não volta, o
  emissor procura prova de entrega a cada 2 s: o `.md` de todas as mensagens do aviso já lido, ou, nos primeiros
  120 s, o começo do UUID de cada envio na tela do `check` **fora** da caixa de digitação (sem espaços nem quebras,
  porque a largura do terminal corta o caminho). Com prova, o aviso vira `entregue`, a trava se solta e o próximo
  aviso pode sair; o `ask` segue sozinho até voltar ou até os 30 min, quando é encerrado. Sem prova, espera o `ask`
  como antes. Continua um envio por vez: o que mudou é que a vez acaba na prova, não na volta do `ask`.
- **Limite do `ask` já provado (revisão do Prumo):** quem o encerra nos 30 min é uma thread do servidor; os 30 min só
  valem **enquanto o portal está no ar**. Na parada normal (Ctrl+C) o emissor encerra os `ask` já provados antes de
  sair; um `ask` ainda sem prova não é encerrado (sobrevive e entrega, como acima). Numa queda abrupta, o `ask`
  provado pode ficar vivo até voltar sozinho, quando o maestro ficar ocioso: é limite declarado. Esse remanescente
  **não** é aviso não entregue (a fila já o tem como `entregue`) e nunca justifica reenviar; para encerrá-lo, o
  procedimento está no `nucleo/LEIA.md` (só os `ask` do próprio portal, criados antes do reinício).

**Canal A (hipótese): `maestri ask` a partir do servidor.** Uma thread manda um aviso por vez, juntando os
pendentes numa mensagem:

```python
subprocess.run([maestri, "ask", agente, mensagem], shell=False, capture_output=True, timeout=1800)
```

`mensagem` = "Portal: N mensagens novas do Gustavo na caixa. <tipo, título em palavras, caminho> por linha.
Absorva no ticket dono e troque estado: nova por lida." Saída 0 = `entregue`; saída diferente de 0, exceção
ou tempo esgotado = `pendente` com nova tentativa em 1, 5 e 15 min, depois `falhou` (visível, com "tentar de
novo" pela API). Fonte: `maestri ask --help` diz que o `ask` bloqueia até o destino ficar ocioso; não diz o
que acontece com o destino no meio de um turno, e a memória do maestro registra texto digitado sem Enter
nesse caso (**não verificado** para este uso). O `maestri` só funciona num terminal do canvas (precisa de
`MAESTRI_PIPE` e `MAESTRI_TERMINAL_ID`): o servidor roda num **terminal próprio no canvas, "Portal"**,
ligado ao "Claude Code".

**Canal B (hipótese): vigia do lado do maestro.** O maestro arma, na sessão dele, o monitor de fundo do
Claude Code (ferramenta `Monitor`) com `python nucleo/aviso.py --vigiar <pasta do portal>`, que imprime uma
linha por mensagem `pendente` (lida da fila e dos `.md`, não da tela) e a marca `entregue` ao imprimir.
Fonte: a descrição da ferramenta `Monitor` no Claude Code diz que cada linha da saída vira uma notificação
no chat e que o monitor expira em no máximo 30 min, com um aviso de expiração para rearmar. Que a notificação
**acorde uma sessão parada** e chegue a uma sessão ocupada sem se perder está **não verificado**.

**Testes, para cada canal tentado** (sem o Gustavo intervir; o maestro combina o momento):

| Teste | Passa se |
|---|---|
| Maestro parado | a mensagem chega, o maestro absorve e troca para `lida` |
| Maestro ocupado | chega depois do turno em curso (ou durante, sem se perder), é absorvida |
| Duas seguidas em 5 s | um aviso só, com as duas, ou dois avisos; nenhuma perdida, nenhuma absorvida duas vezes |
| Reinício do servidor com aviso `pendente` | o aviso sai depois de subir |
| Erro e tempo esgotado (agente com nome errado na configuração) | vira `falhou` visível; "tentar de novo" funciona depois de corrigir |
| Expiração e rearme (só canal B) | depois de 30 min o maestro rearma sozinho e o próximo aviso chega |

Fica valendo o primeiro canal que passar em todos os testes dele (A antes de B). Se nenhum passar, o portal
fica com a faixa "diga 'respondi'" e isso é dito ao maestro como resultado, não escondido.

**Rede de segurança (não é canal):** no começo de cada turno o maestro confere `caixa/` por `estado: nova`, e
também por pedidos `alteracao-laco` em `lida`, `aplicando` ou `aplicado` com `efeito: aguarda` (trabalho ainda sem
desfecho, §4.5). Só pega o que escapou; não faz uma resposta chegar a um maestro parado.

**Acordo com o maestro:** os formatos e o dono das pastas são combinados no marco 3 desta proposta e
registrados na §9; o canal de aviso é acordado na construção, depois dos testes, e registrado na §9 e em
`construcao.md` com a data.

### 4.4 Descrição de laço: `laco.json` (o maestro escreve)

Um laço é um conjunto de scripts que roda por trás (pesquisa em ondas, depois suítes), montado pelo maestro numa
pasta própria. O portal desenha cada laço a partir de **um arquivo de descrição, `laco.json`, na pasta do laço**,
escrito pelo maestro ao montar o laço e atualizado por ele quando o desenho, os controles ou a execução mudam. O
portal nunca o escreve. Exemplos completos dos dois laços deste projeto no Anexo A.

**Registro: `lacos.json` na pasta do portal** (caminho dado por `"lacos": "lacos.json"` no `projeto.json`, §3.2).
Escolhido porque é o mesmo jeito do `cartas.json`: o servidor lê o `projeto.json` só ao subir, mas lê o registro a
cada pedido, então registrar um laço novo não exige reiniciar o portal; e uma lista explícita, em vez de varrer
pastas, não deixa aparecer laço que o maestro não registrou.

```json
[
  {"id": "modelos-de-embeddings", "pasta": ".scratch/context-hub/laco-embeddings"},
  {"id": "pesquisa-ampla", "pasta": ".scratch/context-hub/laco"}
]
```

- `id` `[a-z0-9-]+`, único no registro, estável, igual ao `id` do `laco.json` (diferente → problema e o laço fica
  malformado). Com o id no registro, um `laco.json` ilegível ainda aparece na lista pelo nome.
- `pasta` relativa a `raiz`; precisa ter `laco.json`; não pode estar dentro da pasta do portal nem contê-la.
- A ordem do registro é a ordem da lista dentro de cada grupo.

**Campos do `laco.json`** (UTF-8, JSON puro, ≤ 256 KiB; chave desconhecida é ignorada com problema):

| Campo | Tipo | Exemplo | Regra |
|---|---|---|---|
| `formato` | inteiro | `1` | versão deste contrato; outro valor → malformado |
| `id` | texto | `"modelos-de-embeddings"` | igual ao do registro |
| `titulo` | texto | `"Modelos de embeddings da busca"` | em palavras; é o que a tela mostra |
| `ticket` | texto | `"54"` | número do ticket dono (como na rodada) |
| `execucao` | objeto | `{"id": "embeddings-2026-10-14", "inicio": "2026-10-14T20:36:47-03:00", "terminou_em": null}` | ver abaixo |
| `nos` | lista | `[{"id": "parada", "titulo": "Parada", "papel": "decisao", "detalhe": "..."}]` | ver abaixo |
| `ligacoes` | lista | `[{"de": "parada", "para": "geradores", "palavra": "repete", "tipo": "repete"}]` | ver abaixo |
| `controles` | lista | ver abaixo | o que o Gustavo pode pedir para mudar |
| `capacidades` | lista | `[{"id": "parar-apos-onda", "onda_atual": "onda"}, {"id": "parar-de-despachar"}]` | só estas viram botão |
| `contadores` | lista | ver abaixo | números do estado real a mostrar |
| `sinal` | objeto | `{"fontes": [...], "sem_sinal_apos_s": 300}` | de onde vem "último sinal" |
| `parado` | origem | `{"sqlite": "estado/laco.db", "tabela": "controle", "onde": {"chave": "parar"}, "coluna": "valor", "json": true}` | opcional; verdadeiro = parada gravada |
| `esperando_cota` | objeto | `{"aptos": <origem>, "fora": <origem>}` | opcional; ver "situação" |

- **`execucao`:** `id` (texto `[a-z0-9-]+`, obrigatório) identifica **uma partida do laço**, do plano da onda 1 até
  o fim; religar processos no meio, e pausar e retomar (capacidade `pausar-retomar`), é a mesma execução. Os scripts
  não gravam id de execução: **o id é atribuído pelo maestro no `laco.json`** (padrão: `<laço>-<data de início>`,
  ex. `embeddings-2026-10-14`), nunca lido dos arquivos do laço. O maestro troca o `id` só quando o laço recomeça do
  zero (plano e banco novos) ou parte de novo depois de uma parada definitiva ou do fim. `inicio` (ISO 8601,
  opcional) e `terminou_em` (ISO 8601 ou `null`): o maestro preenche `terminou_em` quando dá a execução por
  terminada; a partir daí o laço vai para "Terminados" e não aceita pedido de mudança, parada ou pausa (comentário
  continua).
- **`nos`:** `id` `[a-z0-9-]+` único no laço; `titulo` em palavras curtas; `papel` ∈ {`etapa`, `decisao`,
  `controle`, `observador`, `fora-dos-scripts`}; `detalhe` (opcional, uma linha, aparece na gaveta; se resume uma
  regra, diz que é resumo ou a descreve inteira); `carta` (opcional, id do `cartas.json`, abre a carta: ex. o painel
  de um observador).
  - `etapa`: script que faz trabalho; `decisao`: ponto em que o laço escolhe por regra (repete ou termina);
    `controle`: limite ou regra que condiciona outro nó, sem trabalho próprio; `observador`: só lê o laço (painel),
    nunca é causa; `fora-dos-scripts`: trabalho de pessoa ou agente conduzido pelo maestro (conferência, auditoria,
    síntese).
- **`ligacoes`:** `de` e `para` são ids de nós; `palavra` é uma palavra (no máximo duas) mostrada na seta; `tipo` ∈
  {`segue` (cadeia de trabalho), `repete` (volta de onda), `condiciona` (controle → nó), `observa` (observador →
  nó)}. Ligação para nó inexistente → malformado.
- **`controles`:** cada um com
  - `id` `[a-z0-9][a-z0-9_-]*`, único no laço (pode ser o nome real da chave, ex. `gate_novos`), estável e nunca
    reaproveitado para outro significado; `no` (id de nó); `rotulo` (em palavras);
  - `tipo` ∈ {`numero`, `inteiro`, `duracao`, `escolha`, `lista`, `texto-curto`};
  - `numero`, `inteiro` e `duracao` exigem `faixa: [mínimo, máximo]` (inclusiva, na unidade gravada); `escolha`
    exige `opcoes: [{"valor": "...", "rotulo": "..."}]` (valores únicos); `texto-curto` aceita até 200 caracteres,
    uma linha;
  - `lista`: um **conjunto de textos** (a ordem não importa; item repetido é erro), que se pede adicionando e
    removendo itens; `itens: {"max": 500, "comprimento": 200}` (quantos itens e o tamanho de cada um, uma linha);
    `opcoes` opcional (se presente, todo item precisa estar nelas);
  - `unidade`: em `duracao` é obrigatória e ∈ {`s`, `min`, `h`} (a unidade em que o valor está gravado); nos outros,
    palavra de exibição opcional (`"tentativas"`); `escala: "porcento"` (opcional, só `numero`) diz que o valor
    gravado é fração e a tela mostra ×100 com "%";
  - `aceita_nulo` (opcional, `false` por padrão) e `nulo` (o que `null` quer dizer, ex. `"sem limite"`);
  - `quando_vale` ∈ {`agora` (no ciclo seguinte do laço, sem religar nada), `proxima-onda` (quando a onda em curso
    fechar), `ao-reiniciar` (quando o processo que lê o valor for religado; o maestro religa ao aplicar),
    `proxima-execucao` (só numa partida nova)};
  - `releitura` ∈ {`continua` (o laço relê a fonte sozinho a cada ciclo), `ao-ligar` (o processo só lê quando sobe:
    aplicar = gravar e religar quem lê), `manual` (o maestro troca à mão: recruta, modelo, harness)};
  - `configurado`: uma **origem** (abaixo) de onde o portal lê o valor **configurado**, ou `{"declarado": <valor>}`
    quando o valor só existe no registro do maestro (ex.: o modelo de um recruta); declarado aparece como "declarado
    pelo maestro", nunca como "lido";
  - `em_uso` (opcional): uma origem que **prova o valor em uso** pelo processo (ex.: uma fonte que o próprio processo
    escreve com o valor que está usando). Ver "Configurado e em uso";
  - `precondicoes` (opcional): `{nome: origem}` com valores de contexto que mudam o sentido do controle sem mudar o
    valor dele (ex.: o `inicio` de onde as horas do teto contam). Entram na revisão.
  - **Opções por nó** (harness, modelo do recruta, esforço e afins) são controles do tipo `escolha` ou `lista` no nó;
    não há outro formato. Exemplo para laços futuros com recrutas (nenhum laço deste projeto tem recruta com controle
    hoje; os da pesquisa ampla, já dispensados, só aparecem no detalhe dos nós):

    ```json
    {"id": "juntador-harness", "no": "juntador", "rotulo": "harness do recruta", "tipo": "escolha",
     "opcoes": [{"valor": "claude-code", "rotulo": "Claude Code"}, {"valor": "codex", "rotulo": "Codex"}],
     "quando_vale": "ao-reiniciar", "releitura": "manual", "configurado": {"declarado": "claude-code"}}
    {"id": "juntador-modelo", "no": "juntador", "rotulo": "modelo do recruta", "tipo": "escolha",
     "opcoes": [{"valor": "claude-opus-5-5", "rotulo": "Claude Opus 5.5"},
                {"valor": "claude-sonnet-5-5", "rotulo": "Claude Sonnet 5.5"},
                {"valor": "claude-haiku-5-5", "rotulo": "Claude Haiku 5.5"},
                {"valor": "claude-fable-5-1", "rotulo": "Claude Fable 5.1"},
                {"valor": "gpt-6.1-sol", "rotulo": "GPT 6.1 Sol (Codex)"}],
     "quando_vale": "ao-reiniciar", "releitura": "manual", "configurado": {"declarado": "claude-sonnet-5-5"}}
    {"id": "juntador-esforco", "no": "juntador", "rotulo": "esforço do recruta", "tipo": "escolha",
     "opcoes": [{"valor": "low", "rotulo": "baixo"}, {"valor": "medium", "rotulo": "médio"},
                {"valor": "high", "rotulo": "alto"}, {"valor": "xhigh", "rotulo": "muito alto"},
                {"valor": "max", "rotulo": "máximo"}],
     "quando_vale": "ao-reiniciar", "releitura": "manual", "configurado": {"declarado": "high"}}
    ```

    No Claude Code valem os modelos Claude e esforço de baixo a máximo; no Codex, `gpt-6.1-sol` com esforço médio ou
    alto. O portal não cruza harness, modelo e esforço: combinação inválida o maestro recusa com o motivo.
- **`capacidades`:** o que o laço sabe fazer quando o maestro aplica um pedido de parada ou pausa. Ids conhecidos:
  - `parar-apos-onda`: a onda em curso fecha e o laço sai (hoje: `parar_apos.py --onda N`); campo `onda_atual`
    (opcional) = id do contador que dá a onda em curso, para a tela sugerir "depois desta onda (N)"; contador
    ilegível → a tela não sugere número nenhum;
  - `parar-de-despachar`: nenhum trabalho novo sai; o que está em voo termina; resultados ficam;
  - `pausar-retomar`: pausa e retomada no mesmo ponto, na mesma execução. **Nenhum laço deste projeto declara hoje**:
    `parar_apos.py` só prova parada depois de uma onda, não pausa genérica nem cancelamento de chamada em voo.
  Id desconhecido → problema e é ignorado. Capacidade não declarada não vira botão nem é aceita no `POST`.
- **`contadores`:** `id` único, `no`, `rotulo`, `tipo` ∈ {`inteiro`, `numero`, `texto`, `hora`, `lista` (lista de
  textos), `contagem` (objeto chave → número, de um agrupamento), `serie` (lista de objetos; `campos` diz quais
  colunas mostrar)}, `escala` opcional como nos controles, `origem` e `hora` (opcional, uma origem que dá a hora do
  dado; sem ela, vale a regra de hora da origem). O primeiro contador da lista é o número-chave da lista de laços.
- **`sinal`:** `fontes` (lista de origens que dão uma hora) e `sem_sinal_apos_s` (inteiro). **Último sinal** = a
  hora mais nova entre as fontes legíveis. A tela diz "último sinal há N min", nunca "vivo": arquivo novo não prova
  processo vivo, e arquivo velho não prova processo morto.

**Situação do laço** (`situacao` na API), a primeira regra que vale, nesta ordem:

1. `terminado`: `execucao.terminou_em` preenchido;
2. `parado`: a origem `parado` lê verdadeiro (parada gravada; a execução ainda não foi dada por terminada);
3. `desconhecido`: nenhuma fonte de `sinal` legível;
4. `sem-sinal`: último sinal mais velho que `sem_sinal_apos_s`;
5. `esperando-cota`: o laço declara `esperando_cota` e `aptos` lê 0, ou `fora` lê um número ≥ `aptos` (o despachante
   não tem modelo apto: nenhum, ou todos fora até a virada da cota); `aptos` ou `fora` ilegível → esta regra não vale
   e a tela anota "cota: ilegível";
6. `rodando`.

"Espera você" (o Gustavo precisa agir) é o **grupo** da §3.4, não uma situação: um laço pode estar "esperando cota" e
"espera você" ao mesmo tempo.

**Origem (de onde ler um valor), sempre dentro da pasta do laço.** Exatamente uma destas formas:

| Forma | Exemplo | Lê |
|---|---|---|
| arquivo JSON | `{"arquivo": "config.json", "campo": "gate_novos"}` | o valor em `campo` |
| JSONL | `{"jsonl": "estado/despachante.log.jsonl", "campo": "gerado_em"}` | `campo` da última linha válida (lê só os últimos 64 KiB) |
| SQLite, uma linha | `{"sqlite": "estado/laco.db", "tabela": "controle", "onde": {"chave": "teto"}, "coluna": "valor", "json": true, "campo": "pedidos"}` | a `coluna` da linha que casa `onde` (igualdade, E); `json: true` decodifica o texto antes de aplicar `campo` |
| SQLite, soma | `{"sqlite": "estado/laco.db", "tabela": "uso", "soma": "tentativas"}` | `SUM` da coluna (`0` se não há linhas) |
| SQLite, contagem | `{"sqlite": "estado/laco.db", "tabela": "pedidos", "contagem": true, "agrupar": "estado"}` | `COUNT(*)`, ou um objeto por valor de `agrupar` |
| hora do arquivo | `{"mtime": "livros/zh.jsonl"}` | a hora de modificação |
| declarado | `{"declarado": "claude-code"}` | o próprio valor (só em `configurado`) |

- `campo` é um caminho com pontos; segmento inteiro indexa lista, negativo conta do fim (`"ondas.-1.taxa_novos"`).
  Sem `campo`, vale o valor inteiro.
- `formato` (opcional) ∈ {`iso`, `epoch`} diz que o valor é uma hora (ISO 8601 ou segundos desde 1970), para
  contadores `hora`, fontes de `sinal` e precondições.
- **Precedência quando falta valor:** (1) SQLite "uma linha" com **mais de uma linha** que casa → ilegível ("mais de
  uma linha"); (2) **nenhuma linha**, arquivo JSON sem o `campo`, ou JSONL sem linha válida → vale `ausente` se a
  origem o declara (ex. `"ausente": null` para "sem teto gravado"), senão ilegível ("sem valor"); (3) valor `null`
  → aceito só em controle com `aceita_nulo`, ou quando veio de `ausente`; senão ilegível; (4) valor do tipo errado →
  ilegível, nunca convertido em silêncio.
- **Hora de cada leitura**, quando o contador não declara `hora`: arquivo e JSONL → hora de modificação do arquivo;
  SQLite → a mais nova entre o banco e o `-wal` dele (com WAL, o arquivo do banco só muda no checkpoint); `mtime` →
  ela mesma.
- **SQLite só leitura:** conexão nova por pedido com `file:<caminho real>?mode=ro` (`uri=True`), `timeout` de 2 s e
  `PRAGMA query_only=ON`, fechada logo depois; nunca `immutable=1` (ignoraria o WAL e mostraria dado velho). Nomes de
  tabela e coluna precisam casar `[A-Za-z_][A-Za-z0-9_]*` e entram na consulta só depois disso; valores de `onde`
  vão como parâmetros. Banco travado, ausente ou sem a tabela → aquele número fica "ilegível" com o motivo.
- Arquivo de origem acima de 16 MiB → "ilegível".

**Configurado e em uso.** O que o portal lê de `configurado` é o que está **gravado ou declarado**, não o que o
processo está usando: um processo pode ter subido com uma opção de linha de comando que passa por cima do arquivo
(ex.: `gerador.py --trabalhadores`), e um processo que lê ao ligar guarda o valor de quando subiu até ser religado. A
API devolve os dois separados e a tela mostra os dois (§2.6):

- `configurado`: `{valor, como: lido|declarado, fonte, hora, ilegivel}`.
- `em_uso.estado`:
  - `confirmado`: (a) o controle declara `em_uso` e ela é legível (a API traz o valor e a fonte, que pode divergir
    do configurado; divergência aparece em tijolo), ou (b) o último pedido aplicado deste controle na execução atual
    tem recibo válido com `efeito: valeu`, o `recibo_depois` igual ao configurado e a revisão atual igual a
    `recibo_revisao` (`como`: "recibo do maestro, <hora>");
  - `relido`: `releitura: continua`, sem `em_uso` declarada, e o laço está `rodando` ou `esperando-cota` (o laço relê
    a fonte a cada ciclo; não é prova de uso, e a tela diz "relido pelo laço a cada ciclo");
  - `nao-confirmado`: todo o resto. É o padrão.
- A revisão, `antes` e `depois` de um pedido comparam **o configurado**, e o texto da tela e do `.md` diz
  "configurado", nunca "em uso".

**Revisão da configuração.** O portal calcula, a cada leitura,
`revisao = sha256(json.dumps(R, sort_keys=True, ensure_ascii=False))`, com

```json
{"laco": "<id>", "execucao": "<execucao.id>",
 "capacidades": [<cada capacidade como declarada>],
 "controles": {"<id do controle>": {
   "definicao": {"no", "tipo", "unidade", "escala", "faixa", "opcoes", "itens", "aceita_nulo",
                 "quando_vale", "releitura", "configurado (a origem declarada)", "em_uso (a origem)",
                 "precondicoes (as origens)"},
   "configurado": <valor>,
   "precondicoes": {"<nome>": <valor>}}}}
```

(em `definicao`, só as chaves que o controle tem). Valor ilegível entra como `{"ilegivel": true}`. **Entram:** a
definição relevante de cada controle (de onde vem, tipo, unidade, faixa, opções), o valor configurado, as
precondições e as capacidades. **Ficam de fora:** contadores, sinal, situação, o valor `em_uso`, as horas de leitura
e os textos (`titulo`, `rotulo`, `detalhe`, `nulo`), porque mudam a cada segundo ou não mudam o sentido de um pedido.
Assim, regravar o teto com `--teto` (que zera o `inicio` mesmo com o mesmo número) muda a revisão pela precondição; e
dois pedidos feitos sobre a mesma revisão nunca são ambos aplicados sem conferência (o segundo vira conflito, §4.5).
O hash é o filtro rápido do `POST`; **ao aplicar, o maestro confere campo a campo** contra o retrato gravado no
pedido (§4.5), nunca só pelo hash.

**Segurança:**

- Todo caminho do `laco.json` é relativo à pasta do laço: sem `..`, sem caminho absoluto, sem letra de unidade,
  sem componente que comece com ponto; resolvido com `realpath` + `commonpath` contra a pasta do laço (§3.2). Fora
  disso, ou atalho/junction para fora: a origem vira problema e não é lida.
- O portal **só lê** a pasta do laço: nunca grava, nunca cria, nunca executa nada ali, nem roda comando declarado em
  `laco.json` (o formato não tem campo de comando; como aplicar cada controle é conhecimento do maestro, no LEIA do
  laço).
- O navegador **só manda ids** (laço, execução, nó, controle, capacidade) e valores tipados; nunca caminho, tabela,
  coluna ou comando. O servidor resolve tudo pelo `laco.json` atual.
- As fontes de um laço não são servidas como arquivo; só os valores declarados saem pela API.

**`laco.json` malformado** (falta campo obrigatório, tipo errado, id repetido, papel ou tipo desconhecido, ligação
ou controle apontando para nó inexistente, faixa invertida, escolha sem opções, lista sem `itens`, `formato`
diferente de 1, caminho fora da pasta): o laço aparece na lista com selo "malformado" e o erro em palavras, sem
controles e sem botões; vai para `problemas`. Uma origem que falha ao ler (arquivo ausente, banco travado) **não**
torna o laço malformado: só aquele número fica "ilegível".

### 4.5 Alteração de laço (o portal escreve; o maestro dá o desfecho)

Tipo novo da caixa, **`alteracao-laco`**: cada pedido feito na tela Laços vira uma mensagem com `.json` (a fonte,
imutável) e `.md` (a vista do maestro), com a mesma gravação, idempotência, reconciliação e confinamento da §3.5 e
§3.7. Nome: `AAAA-MM-DD-HHMMSS-alteracao-laco-<id do laço>-<envio>`. `alvo` no `.json`:
`{"tipo": "laco", "id": "<id>", "titulo": "<título do laço no envio>"}`. **Exceção à regra de dono da caixa:** neste
tipo o maestro, além do `estado:`, preenche as chaves de desfecho do frontmatter (abaixo); nada mais.

**Operações:**

| `operacao` | Campos além de `envio`, `tipo`, `laco`, `execucao`, `operacao`, `revisao` | Exige |
|---|---|---|
| `mudar-controle` | `no`, `controle`, `antes`, `depois`, `texto` (opcional) | controle declarado; execução não terminada |
| `pedir-parada` | `capacidade` (`parar-apos-onda` com `onda`, ou `parar-de-despachar`), `texto` (opcional) | capacidade declarada; execução não terminada |
| `pedir-pausa` | `texto` (opcional) | `pausar-retomar` declarada; execução não terminada |
| `pedir-retomada` | `texto` (opcional) | `pausar-retomar` declarada; execução não terminada e pausada |
| `comentario-no` | `no`, `texto` | nó existe |
| `comentario-laco` | `texto` | — |

Todas aceitam `substitui` (regras abaixo). `pedir-retomada` só existe junto com `pausar-retomar` e retoma **a mesma
execução**. Depois de uma **parada definitiva** ou do fim não há retomada: partir de novo, recomeçar do zero ou
"criar nova execução com estes valores" o Gustavo pede por comentário, e o maestro abre uma execução nova (novo
`execucao.id`).

**Corpo** (`antes` e `depois` são o valor **configurado**, tipados: `{"tipo": <tipo do controle>, "valor": <valor
na unidade gravada>}`; em `lista`, o conjunto inteiro; `valor: null` só com `aceita_nulo`):

```json
{"envio": "3f2b8c1e-7a44-4d0e-9b52-6c1d2e9a0f17", "tipo": "alteracao-laco",
 "laco": "modelos-de-embeddings", "execucao": "embeddings-2026-10-14", "operacao": "mudar-controle",
 "no": "parada", "controle": "gate_novos",
 "antes": {"tipo": "numero", "valor": 0.15}, "depois": {"tipo": "numero", "valor": 0.1},
 "revisao": "<sha256 que veio em GET /api/laco/<id>>", "texto": null}
```

```json
{"envio": "<uuid>", "tipo": "alteracao-laco", "laco": "modelos-de-embeddings", "execucao": "embeddings-2026-10-14",
 "operacao": "pedir-parada", "capacidade": "parar-apos-onda", "onda": 2, "revisao": "<sha256>", "texto": null}
{"envio": "<uuid>", "tipo": "alteracao-laco", "laco": "modelos-de-embeddings", "execucao": "embeddings-2026-10-14",
 "operacao": "comentario-no", "no": "geradores", "revisao": "<sha256>", "texto": "testar só pt primeiro"}
```

O corpo é imutável: reenvio depois de falha usa o mesmo `envio` e o mesmo corpo; depois de um envio aceito, mudar de
ideia é **outro envio** com `substitui: <arquivo anterior>` (como em "Corrigir resposta"). "Propor de novo" depois de
um conflito também é outro envio com `substitui` apontando o pedido em conflito.

**Validação no servidor** (depois da idempotência da §3.5, que vem antes de tudo; falhou → 400 com `campo`, salvo
os 409 indicados):

- `laco` está no `lacos.json` → senão **409** `laco-mudou`; `laco.json` malformado → 400 `laco-malformado`.
- `execucao` é o `execucao.id` atual → senão **409** `execucao-mudou` (vale para todas as operações: um pedido nunca
  passa sozinho para a execução seguinte). Execução com `terminou_em` → **409** `laco-terminou` para tudo menos
  comentários.
- `operacao` é uma das seis; campo que não pertence à operação → 400 `chave-desconhecida`; texto livre ≤ 20 000
  caracteres, obrigatório e não vazio em comentários.
- `mudar-controle`: `controle` existe no `laco.json` e pertence a `no`; `antes.tipo` e `depois.tipo` são o tipo do
  controle; `depois.valor` dentro da `faixa` (inteiro sem fração; `duracao` na unidade gravada), entre as `opcoes`,
  ou, em `lista`, um conjunto sem repetidos com no máximo `itens.max` itens de até `itens.comprimento` caracteres numa
  linha (e todos nas `opcoes`, se houver); `null` só com `aceita_nulo`; `texto-curto` ≤ 200 caracteres numa linha;
  `depois` ≠ `antes` (em lista, como conjunto) → senão 400 `nada-muda`; configurado ilegível → **409**
  `configurado-ilegivel`.
- `pedir-parada`, `pedir-pausa`, `pedir-retomada`: a capacidade está declarada → senão 400 `capacidade-ausente`.
  `onda` (só em `parar-apos-onda`) é inteiro ≥ 1 e, **só quando `onda_atual` é legível**, ≥ a onda em curso; com o
  contador ilegível o servidor não inventa onda nenhuma para comparar, e o maestro revalida o alvo ao aplicar.
- `comentario-no`: `no` existe.
- **`substitui`** (opcional): nome de uma mensagem `alteracao-laco` que existe na caixa, **do mesmo laço e da mesma
  execução**, e compatível: `mudar-controle` só substitui `mudar-controle` do **mesmo controle**; `pedir-parada`,
  `pedir-pausa` e `pedir-retomada` substituem um ao outro; comentários não substituem nem são substituídos. O
  substituído precisa estar em `nova`, `lida` ou `conflito`, e não pode já ter outro substituto. Fora disso → 400
  `substitui-invalido`. Substituir não apaga nada: os dois ficam no histórico.
- **Revisão:** em `mudar-controle`, `revisao` diferente da atual → **409** `laco-mudou`, com `{"erro": "laco-mudou",
  "mensagem": "...", "campo": "revisao", "conflito": {"viu": <antes>, "agora": <configurado atual daquele controle>,
  "pediu": <depois>, "revisao": "<atual>", "definicao_mudou": true|null}}`. A revisão é um hash: diz que algo mudou,
  não o quê. Por isso `definicao_mudou` é `true` só quando está **provado** que a regra deste controle mudou (o tipo
  não é mais o que a página viu, ou o valor pedido não cabe mais na definição atual: faixa, opções, itens, nulo), e
  `null` em todo o resto, que quer dizer "a configuração ou a regra mudou; o portal não sabe qual" (ex.: só o máximo
  da faixa, a unidade, a origem ou a releitura mudaram, e o pedido continua permitido; ou mudou outro controle). Nunca
  `false` por inferência. A tela mostra "você viu / agora está / você pediu", mais "a regra deste controle mudou"
  com `true` e "a configuração ou a regra do laço mudou" com `null`, guarda o rascunho e nada é gravado; a conferência
  campo a campo continua do maestro. `antes` diferente do configurado atual dá o mesmo 409 com `"campo": "antes"`
  (defesa: com a revisão igual não deveria acontecer); aí a revisão é a que a página viu e a definição entra no hash,
  então `definicao_mudou: false` é provado. Nos
  pedidos de parada, pausa e retomada e nos comentários, `revisao` vai só como contexto (o que o Gustavo via) e nunca
  dá 409: eles não dependem dos valores dos controles; execução, capacidade e alvo (nó, onda) são revalidados.

**O `.json`** traz, além do corpo, o **retrato do laço no envio**, para o `.md` nascer só dele e para o maestro
conferir campo a campo: `id`, `titulo`, `ticket`, `execucao`, a `revisao` atual, o nó (`id`, `titulo`), as
capacidades, e, em `mudar-controle`, o controle inteiro como estava (toda a definição da §4.4, o configurado com
fonte e hora, o `em_uso` e os valores das precondições).

**O `.md`**, gerado do `.json`; as chaves de desfecho nascem vazias e **só o maestro as preenche**:

````markdown
---
tipo: alteracao-laco
laco: modelos-de-embeddings
ticket: 54
execucao: embeddings-2026-10-14
operacao: mudar-controle
enviada: 2026-10-14T21:40:12-03:00
envio: 3f2b8c1e-7a44-4d0e-9b52-6c1d2e9a0f17
estado: nova
substitui:
aplicando_desde:
aplicado_em:
efeito:
valeu_em:
recibo_execucao:
recibo_antes:
recibo_depois:
recibo_revisao:
agora_esta:
motivo:
---

# Alteração de laço: Modelos de embeddings da busca

pedido: mudar "novos por onda abaixo de" (nó Parada) de 15% para 10% (configurado)
onde está: config.json, chave gate_novos
vale: na próxima onda; o juntador lê ao ligar (aplicar = gravar e religar o juntador)
revisão vista: <sha256 completo>
texto:
> (em branco)
````

**Chaves de desfecho (o maestro grava; uma linha cada, sem multilinha):**

| Chave | Formato | Regra |
|---|---|---|
| `estado` | um dos estados abaixo | outro valor → "estado desconhecido" + problema |
| `aplicando_desde` | ISO 8601 com fuso | gravado **antes** de qualquer efeito (ver "Como o maestro aplica") |
| `aplicado_em` | ISO 8601 com fuso | ≥ `enviada` e ≥ `aplicando_desde` |
| `efeito` | `valeu`, `aguarda` ou `nao-confirmado` | `valeu` exige `valeu_em` ≥ `aplicado_em`; `aguarda` e `nao-confirmado` exigem `valeu_em` vazio |
| `valeu_em` | ISO 8601 com fuso | só com `efeito: valeu` |
| `recibo_execucao` | texto | igual à `execucao` do pedido |
| `recibo_antes`, `recibo_depois` | **JSON numa linha**: `{"tipo": ..., "valor": ...}` | `mudar-controle`: o tipo do controle do retrato, valor válido para a definição dele; `recibo_antes` = `antes` e `recibo_depois` = `depois` do pedido (outro valor não é "aplicado": é `recusado` ou `conflito`). Parada, pausa, retomada: `{"tipo": "texto", "valor": "parar: sim depois da onda 2"}` |
| `recibo_revisao` | 64 caracteres hexadecimais | a revisão (§4.4) depois de aplicar |
| `agora_esta` | JSON numa linha, tipado | o configurado que o maestro achou, no tipo do controle; ou `{"tipo": "texto", "valor": "<o que mudou na definição>"}` |
| `motivo` | texto, ≤ 500 caracteres | em palavras |

O leitor tira as aspas externas como na §3.3 e decodifica os campos JSON; texto livre do Gustavo nunca entra nessas
chaves (continua em citação no corpo).

**Estados (no `estado:` do `.md`) e quem grava:**

| Estado | Quem grava | A tela mostra | Exige |
|---|---|---|---|
| `nova` | portal, ao gravar | enviado | — (mesmo valor inicial dos outros tipos) |
| `lida` | maestro | lido | — (intermediário: continua pendente de desfecho) |
| `aplicando` | maestro | aplicando | `aplicando_desde` (intermediário: efeito pode estar pela metade) |
| `aplicado` | maestro | aplicado | `aplicado_em`, `recibo_execucao`, `recibo_antes`, `recibo_depois`, `recibo_revisao`, `efeito` (`aguarda` mostra "aguarda efeito: <quando_vale>"; `nao-confirmado` mostra "configuração gravada; efeito não confirmado") |
| `recusado` | maestro | recusado | `motivo` |
| `conflito` | maestro | conflito | `agora_esta`; "você viu" e "você pediu" vêm do `.json` |
| `encerrado-sem-aplicar` | maestro | encerrado sem aplicar | `motivo` (o laço terminou antes; a execução mudou; já estava parado, nada alterado; substituído pelo envio X) |

- O portal grava só o envio (`.json` + `.md` com `estado: nova`); **tudo depois disso é do maestro**, no `.md`. O
  maestro pode passar de `aguarda` a `valeu` mais tarde (troca `efeito` e preenche `valeu_em`). O portal nunca
  reescreve o `.md`.
- **Recibo validado, nunca só presente:** o portal confere cada chave pela tabela acima (formato, tipos, execução
  igual, valores iguais ao pedido e válidos para a definição do retrato, horas em ordem). Falhou → a API traz
  `recibo.valido: false` com os `erros` em palavras, a tela mostra "<estado> com recibo inválido" em tijolo, e o
  problema vai para `problemas`; um recibo inválido nunca é mostrado como "aplicado" nem confirma `em_uso`. O mesmo
  para `recusado` ou `encerrado-sem-aplicar` sem `motivo` e `conflito` sem `agora_esta`.
- Comentários só passam por `nova` → `lida`.

**Pendente de trabalho ≠ pendente de aviso.** A fila de avisos (§4.3) só registra **entrega**: o aviso de um pedido
vira `entregue` quando o `.md` tem qualquer estado **válido** diferente de `nova` (o maestro o leu). Estado
desconhecido não confirma entrega: vira problema e o aviso segue a fila normal. O **trabalho** continua pendente,
file-first, enquanto o pedido estiver em `nova`, `lida`, `aplicando`, ou `aplicado` com `efeito: aguarda`: a rede de
segurança do maestro (§4.3) procura esses estados em `caixa/*-alteracao-laco-*.md` no começo de cada turno e depois
de cada retomada, e a tela mostra "lido, sem desfecho há N min" e "aplicando desde HH:MM".

**Como o maestro aplica** (ele, não o portal; cada passo na hora de aplicar, não só na leitura):

1. **Antes de qualquer efeito, confere o que já foi feito:** o `estado` e as chaves de desfecho do `.md`, o ticket
   dono (já cita este UUID?) e, no próprio laço, sinais do efeito (o configurado já é o `depois`? a parada já está
   gravada?). Pedido já com desfecho → nada a fazer, exceto `aplicado` com efeito "aguarda", que ainda pede a confirmação
   do efeito. Efeito encontrado sem recibo, ou `estado: aplicando` de uma vez
   anterior → **reconcilia**: completa só os passos que faltam e grava o recibo do que observou; nunca repete às
   cegas (em especial: não religa processo de novo e não regrava o teto, que zeraria o `inicio`).
2. Relê o `laco.json` e a situação da execução. Execução terminada ou com outro `id` → `encerrado-sem-aplicar`;
   nunca passa o pedido para a execução seguinte. Pedido substituído ainda em `nova` ou `lida` →
   `encerrado-sem-aplicar` com "substituído pelo envio <UUID>"; o substituto é tratado por si.
3. Em `mudar-controle`, recalcula a revisão e **confere campo a campo** o retrato do `.json` contra o `laco.json` e as
   fontes atuais: nó, controle, tipo, unidade, escala, faixa ou opções ou itens, origem do configurado, precondições
   (ex.: o `inicio` do teto) e o configurado. Valor diferente → `conflito` com `agora_esta`; definição diferente →
   `conflito` (`agora_esta` em texto com o que mudou) ou `recusado` se o pedido deixou de fazer sentido. Nada é
   sobrescrito nem recalculado; nova proposta é outro envio. Em parada, pausa e retomada: revalida a capacidade e o
   alvo temporal (a onda pedida ainda não fechou? o laço está pausado para retomar?).
4. Pedido de parada ou pausa já satisfeito (o laço já estava parado ou pausado) → `encerrado-sem-aplicar` com "já
   estava parado; nada alterado", sem dizer que o pedido causou a mudança.
5. Grava `estado: aplicando` e `aplicando_desde`, aplica pelo mecanismo do laço (o LEIA dele), grava o recibo e
   `estado: aplicado`. Controle com `releitura: ao-ligar` só tem efeito depois de religar quem lê; até lá o recibo diz
   `efeito: aguarda`, e o maestro volta a ele (rede de segurança) para passar a `valeu` ou `nao-confirmado`.
6. Absorve no ticket dono citando o `envio` completo, como na §4.3.

**Parar e pausar, o que o Gustavo precisa saber** (a tela diz junto do botão): até a parada valer, **chamadas já em
voo ainda gastam cota** (o gerador termina o pedido que já pegou, com os reenvios dele); `parar-apos-onda` espera a
onda fechar, o que pode levar muito tempo; e `parar_apos.py` prova só a parada depois de uma onda, **não prova pausa
genérica**, retomada no mesmo ponto nem cancelamento instantâneo, por isso nenhum laço declara `pausar-retomar` hoje.

**Aviso ao maestro:** mesma fila e mesmo canal dos outros tipos (§4.3). Na mensagem, a linha deste tipo diz
"alteração de laço", o título do laço, a operação em palavras e o caminho do `.md`, e a instrução final passa a ser
"Absorva no ticket dono e troque estado: nova por lida; nas alterações de laço, grave o desfecho conforme a §4.5".

**Critérios do L2 para estas regras** (testes no padrão da suíte do núcleo): rodada respondida na versão atual não
põe o laço em "espera você", e rodada reescrita depois da resposta põe; conflito substituído, conflito de execução
anterior e conflito de laço terminado não põem; revisão muda com a regravação do teto que só troca o `inicio` e com
mudança de faixa; `substitui` de outro laço, de outra execução ou de outro controle → 400; recibo com tipo errado,
execução diferente, `depois` diferente do pedido ou horas fora de ordem → "recibo inválido", nunca "aplicado"; estado
desconhecido não marca o aviso como entregue; SQLite com duas linhas, nenhuma linha (com e sem `ausente`) e `null`
seguem a precedência da §4.4.

### 4.6 Contrato fixado na construção do L2 (2026-10-14)

Detalhes decididos ao construir o núcleo dos laços (marco L2) e aceitos pelo Prumo, com as correções da revisão
dirigida (itens 7 e 19, e a robustez dos ids). Valem sobre o texto das §3.4, §4.4 e §4.5 onde divergirem, para outro
construtor não implementar um contrato diferente. O LEIA do núcleo resume o mesmo para quem instala.

**Leitura dos laços (§4.4):**

1. **Problemas dos laços em `GET /api/estado`:** o registro (`lacos.json` ausente, ilegível, id ruim ou repetido),
   o `laco.json` malformado ou com chave desconhecida, e os pedidos com estado desconhecido ou recibo inválido entram
   em `problemas`. Para isso o estado lê só descritores e caixa, nunca as fontes de estado (que mudam a cada segundo).
2. **Campos do `laco.json`:** obrigatórios `formato`, `id`, `titulo`, `ticket`, `execucao`, `nos`, `ligacoes`,
   `controles`, `capacidades`, `contadores` e `sinal`; opcionais `parado` e `esperando_cota`.
3. **Malformado** (o laço aparece pelo id, sem controles nem botões; detalhe 422): campo obrigatório ausente ou de
   tipo errado; `faixa`, `opcoes` ou `itens` num tipo de controle que não os usa; `onda_atual` apontando para contador
   inexistente; origem com mais de uma forma; **id de forma errada** (lista, objeto, número ou booleano onde vai um id:
   nós, ligações, controles, contadores, capacidades, `onda_atual`, execução). O tipo de cada id é conferido antes de
   procurá-lo; um descritor ruim nunca vira erro 500 nem tira os outros laços da lista. Chave desconhecida, inclusive
   dentro de uma origem, e capacidade desconhecida só viram problema.
4. **Caminho ruim em dois níveis:** a regra léxica (absoluto, letra de unidade, `..`, componente com ponto, componente
   vazio) torna o laço malformado; um atalho ou junction que sai da pasta do laço deixa só aquela origem "ilegível",
   com problema, sem ler o alvo.
5. **Arquivo de origem ausente** é ilegível (o `ausente` declarado vale para linha, campo ou registro que não existe,
   não para arquivo que sumiu). **`NULL` numa coluna do SQLite** é valor nulo (regra 3 da precedência), não "sem
   valor".
6. **Hora de uma fonte de sinal:** o valor dela quando a origem tem `formato`; senão, a hora do arquivo (no SQLite, a
   mais nova entre o banco e o `-wal`).

**Pedido `alteracao-laco` (§4.5):**

7. **`definicao_mudou` no 409 de revisão:** `true` só quando provado (tipo diferente, ou valor pedido fora da
   definição atual); `null` quando não se sabe ("a configuração ou a regra mudou"); `false` só no 409 de `antes`, em
   que a revisão é a mesma. Ver o texto da §4.5.
8. **Ordem das conferências em `mudar-controle`:** forma de `antes` e `depois`; configurado ilegível (409
   `configurado-ilegivel`); revisão (409); tipo (400); `antes` diferente do configurado (409); valor (400); valor
   igual ao configurado (400 `nada-muda`). Revisão antes do tipo deixa uma mudança legítima de tipo aparecer como
   conflito.
9. **Onda já passada** em `parar-apos-onda` → 400 `onda-invalida`; com a onda em curso ilegível não há comparação.
10. **Pausa e retomada:** o formato não tem fonte de "está pausado", então o servidor valida só a capacidade
    `pausar-retomar`; o maestro revalida pausa e execução antes de qualquer efeito. O recebimento de `pedir-retomada`
    nunca é apresentado como retomada executada: é um pedido até o desfecho do maestro.
11. **`revisao` no corpo** é obrigatória e bem formada (64 hexadecimais) em todos os pedidos, mas só dá 409 em
    `mudar-controle`; nos outros, é contexto.
12. **Ids no corpo:** `no`, `controle`, `laco`, `execucao`, `capacidade`, `onda` e `substitui` têm o tipo conferido
    antes de qualquer busca; forma errada → 400 com `campo` (`tipo-errado` para `no` e `controle`, os códigos
    próprios para os outros).
13. **Aviso:** a instrução estendida ("nas alterações de laço, grave o desfecho conforme a §4.5") só entra quando o
    aviso tem uma alteração de laço; os outros avisos ficam com o texto da §4.3.

**Desfechos, grupos e contagens:**

14. **`pedidos_abertos`** conta os pedidos da execução atual com trabalho pendente: `nova`, `lida` (menos
    comentários, que encerram na leitura), `aplicando`, `aplicado` com `efeito: aguarda` e estado desconhecido.
15. **Conflito e "espera você":** um `conflito` atual, não substituído, de laço não terminado põe o laço em "espera
    você" mesmo com recibo inválido (o Gustavo precisa ver).
16. **Comentário** em estado diferente de `nova` ou `lida` → recibo inválido.
17. **`aplicando_desde`** também precisa ser igual ou posterior a `enviada`.
18. **Linha malformada em `GET /api/lacos`:** `titulo` = id, `grupo` `em-voo`, `situacao` `desconhecido`, `destaque` e
    `pedidos_abertos` `null`, `problema` em palavras. **Retrato no `.json`:** chave `laco`; em `mudar-controle` inclui
    `definicao` (o controle como declarado no `laco.json`, origens incluídas) e `origem_configurado`; o `.md` ganha as
    linhas controle, configurado no envio, em uso no envio e precondições.

**Cartas diante dos laços (§4.4: as fontes de um laço não são servidas como arquivo):**

19. Uma carta cuja `pasta` é a raiz de um laço registrado, ou a contém (ex.: a carta mestra em
    `.scratch/context-hub`), **não serve nada de dentro desse laço**, nem o próprio HTML. Uma carta cuja `pasta` fica
    **dentro** do laço só serve se for uma **subpasta só de publicação** (um painel, como `laco/painel`): o laço está
    bem formado e nem o `laco.json` nem nenhuma origem declarada (bancos com `-wal`, `-shm` e `-journal`) fica dentro
    dela. Fora disso, nada de dentro do laço sai. Atalhos são resolvidos antes (`realpath`): um atalho do painel para
    uma fonte cai fora da pasta da carta e dá 404. O `dados.js` que o atualizador gera no painel é apresentação, não
    fonte declarada; se um laço passar a declarar um arquivo do painel como fonte, o painel deixa de ser servido até
    a fonte sair dali.

## 5. Plano de construção

Os marcos têm duas trilhas que andam em paralelo até o marco 4 e depois se juntam. Cada marco termina com a
revisão do Prumo (código e, quando houver tela, captura) antes de contar como feito.

| Marco | Trilha | Conteúdo | Depende de |
|---|---|---|---|
| 0 | construtor | a fixture: `nucleo/testes/fixtures/` (§5.1) | — |
| 1 | dados (subagente) | `leitores.py` + testes sobre a fixture e sobre os arquivos reais deste projeto | 0 |
| 2 | dados (subagente) | `torre.py`, `caixa.py`, API da §3.4, segurança, caixa da §3.5, testes | 1 |
| 3 | tela (construtor) | `vendor/`, casca, barra lateral, contador, tela Torre, contra a fixture | 0 |
| 4 | tela (construtor) | Partidas, gaveta com ações, Rotas | 3 |
| 5 | junção | a página passa a ler a API real; Autorizações com os cinco tipos, rascunho, 409, emenda | 2, 4 |
| 6 | junção | `cartas.json` preenchido (perguntas ao maestro), Cartas, leitor de carta, Rumo | 5 |
| 7 | junção | `aviso.py`, `iniciar.cmd`, terminal "Portal" (pedido ao maestro), testes da §4.3 | 5 |
| 8 | junção | conferência final (§6), testes de aceite (§8), revisão final do Prumo, entrega | 6, 7 |

### 5.1 A fixture (marco 0, do construtor)

Antes de abrir as duas trilhas, o construtor escreve `nucleo/testes/fixtures/`, que depois é **só lida** pelas
duas (mudar a fixture é decisão do construtor, avisada ao subagente):

- um projeto fictício e neutro, **"Horta do bairro"**, com o mesmo formato deste: `projeto.json`, `cartas.json`,
  `mapa.md` (destino com três critérios, decisões, fora do escopo), `estrategia.md` com uma tabela de radar,
  `GLOSSARY.md`, uns oito tickets em `issues/` (todos os estados, inclusive `wontfix` e um desconhecido; uma
  dependência inexistente; um ciclo), duas cartas HTML pequenas, `rodadas/` com uma rodada boa dos cinco tipos
  e uma malformada, e `caixa/` com casos de recuperação (`.json` sem `.md`, `.md` sem `.json`, sobra em `.tmp`);
- `estado-esperado.json`: a resposta de `/api/estado` para essa fixture, no esquema da §3.4. É o contrato entre
  as trilhas: a tela usa como dado de exemplo, e o marco 2 tem um teste que compara a API real com ele (mesmas
  chaves e valores, fora `gerado_em` e `base`).

Os testes sobre os arquivos reais deste projeto ficam fora do `nucleo/`, em `portal/testes-do-projeto/`, para o
`grep` de neutralidade do núcleo continuar vazio.

### 5.2 Iniciar

- `iniciar.cmd` roda `python nucleo\torre.py projeto.json` a partir da pasta do portal e abre
  `http://127.0.0.1:8770/` no navegador padrão.
- **Pelo canvas** (terminal "Portal"): herda `MAESTRI_PIPE` e `MAESTRI_TERMINAL_ID`, aviso ativo.
- **Fora do canvas** (duplo clique no Windows): o portal funciona inteiro, o aviso fica `indisponivel` e a
  faixa avisa. O servidor escreve no terminal qual dos dois modos está valendo.
- O terminal "Portal" é PowerShell: sobe com `.\iniciar.cmd`; para parar, Ctrl+C e "S" na pergunta "Deseja
  finalizar o arquivo em lotes (S/N)?".

## 6. Conferência visual

O painel do Maestri congela animações e capturas. Com o servidor no ar, capture com
`msedge.exe --headless=new --disable-gpu --user-data-dir=<perfil único> --window-size=1600,900
--virtual-time-budget=6000 --screenshot=<png> http://127.0.0.1:8770/#/<tela>`; espere o PNG, mate os msedge
daquele perfil, olhe o PNG antes de dizer que está pronto. Cada tela em 1600×900 e 1280×800, mais a gaveta
aberta, uma rodada com os cinco tipos e o leitor de carta. PNGs em `portal/conferencia/`.

## 7. Time e passagem

- **Construtor: Claude Opus 5.5, esforço alto** (o terminal "Designer"; antes foi o Fable 5.1, trocado na construção). Dono da construção e das decisões de detalhe dentro desta proposta. **Teto de contexto: 50%.**
  Antes de chegar nele, e ao fim de cada marco, atualiza `portal/construcao.md` (marco atual, o que está
  feito e conferido, decisões de detalhe tomadas, problemas abertos, próximo passo exato) e pede o `/clear` ao maestro;
  depois do clear, retoma lendo esta proposta e o `construcao.md`.
- **Subagente da trilha de dados** (no terminal do construtor): marcos 1 e 2, com escopo de arquivos fechado
  (`leitores.py`, `torre.py`, `caixa.py`, `nucleo/testes/` menos `fixtures/`, `portal/testes-do-projeto/`),
  sem tocar `web/` nem a fixture.
- **Prumo** (Codex, revisor obrigatório): revisa cada marco, código e captura, por `maestri ask "Prumo"` com
  ask back; ajuda o maestro a conferir o portal no fim.
- **Maestro:** fatos que faltam (situação das cartas, decisões a confirmar), o terminal "Portal" e os testes
  de aviso. O Gustavo opina no resultado final.
- Sem ajudante no canvas: o portal é uma peça só e a coerência visual pede uma mão.

## 8. Pronto quando

Funcional:

- `iniciar.cmd` sobe o servidor em `127.0.0.1` e abre o portal; fora do canvas, a faixa de aviso indisponível
  aparece.
- As cinco telas leem os arquivos reais e mudam sozinhas em até 3 s quando um ticket, o mapa ou uma rodada
  muda.
- Uma rodada com os cinco tipos é respondida de ponta a ponta; o `.md` e o `.json` saem no formato da §4.2;
  o maestro é avisado pelo canal escolhido, e **todos** os testes da §4.3 aplicáveis a esse canal passaram,
  registrados em `construcao.md` e aprovados pelo Prumo. Instalar o vigia sem os testes não conta. Se nenhum
  canal passar, a faixa "diga 'respondi'" é o diagnóstico honesto e o requisito "volta direta ao maestro" fica
  declarado como **não cumprido** na entrega.
- Nos testes de recuperação, o aviso pode repetir (entrega pelo menos uma vez), mas nenhuma mensagem é
  absorvida duas vezes no ticket.
- O System design abre dentro do portal; toda carta tem propósito, ticket, decisão, data com tipo e
  situação, ou "a confirmar" com a pergunta feita ao maestro.

Segurança (testes automáticos em `testes/`):

- `Host` estranho → 403; `Origin` de outro site ou sem `X-Torre` → 403; nenhum cabeçalho CORS na resposta.
- `/carta/<id>/../../map.md`, `%2e%2e`, e um symlink ou junction dentro da `pasta` apontando para fora → 404.
- Corpo acima de 256 KiB → 413; `tipo`, id de pergunta, chave ou alvo inexistente → 400.
- Comentário com `---\nestado: lida` grava como citação e o frontmatter continua `estado: nova`.
- Iframes de carta com `sandbox="allow-scripts"` (sem `allow-same-origin`): a carta não lê a API do portal.
- Markdown de ticket passa por DOMPurify; links externos abrem com `rel="noopener noreferrer"`.

Robustez:

- Mesmo `envio` mandado duas vezes → um arquivo só; 20 envios diferentes em paralelo → 20 arquivos com nomes
  diferentes.
- Servidor derrubado com aviso `pendente` → ao subir, o aviso sai.
- Quedas simuladas entre as etapas da gravação (§3.5), uma de cada: depois do `.json` e antes do `.md`;
  depois do `.md` e antes da fila; com sobra em `.tmp/`; com `.avisos.json` apagado ou corrompido. Em cada uma,
  ao subir: o `.md` existe, o envio está no índice, o aviso sai uma vez, e reenviar o mesmo `envio` devolve
  `repetido: true` sem arquivo novo.
- Mesmo `envio` com corpo diferente → 409 `envio-conflito`; mesmo `envio` depois de a rodada ser absorvida →
  200 `repetido`.
- `/carta/system-design/map.md`, `/carta/system-design/portal/caixa/<algum>.json` e
  `/carta/system-design/portal/projeto.json` → 404.
- Fixtures ruins (rodada malformada, JSON de proposta quebrado, status desconhecido, dependência inexistente,
  ciclo) → aparecem no painel de problemas e o resto da página funciona.

Forma:

- Nenhum código interno solto em nenhuma tela; tudo que aparece no hover aparece com foco e clique.
- Capturas da §6 conferidas; Prumo aprovou cada marco e o final.
- `nucleo/` não cita este projeto: `grep -ri "context hub\|context-hub" nucleo/` vazio.

## 9. Acordo com o maestro

**2026-10-14, aceite do maestro (marco 3):** interface aceita como está: `rodadas/` do maestro e `caixa/` do
portal, com o dono de cada pasta da §4; formatos de rodada (§4.1) e de resposta (§4.2); os dois canais de aviso
(A e B) só valem depois de testados (§4.3); a conferência de `caixa/` por `estado: nova` no começo de cada turno
fica como rede de segurança.

Observação do maestro para o canal A: um `maestri ask` para um Claude Code ocupado costuma ficar digitado sem
Enter até chegar outro `ask`. Testar o caso "ocupado" com cuidado (conferir com `maestri check` se a mensagem
ficou parada na entrada) antes de dar o canal A por aprovado.

**Canal de aviso escolhido (2026-10-14): canal A**, `maestri ask` a partir do servidor no terminal "Portal" do
canvas, ligado ao "Claude Code". Testes reais com o maestro, todos passaram (registro com horas e UUIDs em
`construcao.md`): parado, ocupado (o Claude Code enfileirou e o maestro leu durante o turno; nada ficou digitado
sem Enter), duas em 5 s, reinício e nome errado (`pendente` com o erro na API, nova tentativa ao corrigir; a escada
1/5/15 min até `falhou` está provada nos testes unitários com hora controlada). Nada perdido, nada absorvido duas
vezes. A rede de segurança (conferir `caixa/` por `estado: nova` no começo de cada turno) continua.

## Anexo A. Exemplos de `laco.json` dos dois laços deste projeto (marco L1, 2026-10-14)

Formato da §4.4, com os nomes reais de parâmetros e fontes de estado lidos nas pastas dos laços (`LEIA.md`,
`config.json`, `comum.py`, `despachante.py`, `gerador.py`, `juntador.py`, `parar_apos.py`, `painel_dados.py`), nos
tickets 50 e 54 e nas respostas do maestro de 2026-10-14; bancos abertos só em modo leitura. **O maestro escreve os
arquivos reais** a partir destes: eles ainda não existem nas pastas. Cada exemplo tem, depois do JSON, a tabela do
que é fato (com a fonte) e do que é suposição.

Fatos dos scripts que pesam na descrição (valem para os dois laços, que usam o mesmo código):

- Os dois laços são **só processos Python** ligados por `Start-Process` (despachante, um gerador por grupo, juntador
  e o atualizador do painel). O de embeddings não tem recruta; a pesquisa ampla teve recrutas na partida (Bússola,
  Faísca, Brasa e Centelha, dispensados; o Tear decidiu os ambíguos), que, como o laço terminou, entram só no
  detalhe dos nós Estado no chat e Ambíguos, sem controle (maestro, 2026-10-14). Harness e modelo de recruta não se
  aplicam a esses nós; a única opção de modelo é a lista `excluir_manual` do despachante (modelos do FreeLLMAPI que
  não recebem pedidos).
- `config.json` é lido **uma vez, quando cada processo sobe** (`carregar_config()` no `main` de despachante, gerador
  e juntador; o LEIA dos dois laços foi corrigido pelo maestro em 2026-10-14: `excluir_manual` pede reiniciar o
  despachante). Mudar uma chave dele só vale depois de religar quem a lê. Exceções: `fracao_para_fechar` é relida
  pelo juntador a cada checagem; `gate_novos` é relido pelo `painel_dados.py` (só para mostrar).
- `teto` e `parar` moram no banco, tabela `controle`, e valem no ciclo seguinte, sem religar. O teto é o valor JSON
  `{"pedidos", "horas", "inicio"}`, relido a cada escolha de modelo (`despachante.teto_atingido`). Apesar do nome
  `pedidos`, a unidade efetiva é **tentativas**: o teto é comparado com `SUM(tentativas)` da tabela `uso`. As horas
  contam desde `inicio`. `despachante.py --teto P H` regrava `inicio` com a hora atual (zera o relógio); por isso o
  `inicio` é precondição dos controles do teto, e o maestro, ao mudar o teto, grava direto na tabela `controle`
  preservando `inicio`, sem `--teto`.
- `controle.parar = true` faz geradores e juntador saírem: o gerador deixa de pegar pedido novo e termina o que já
  pegou (por isso chamadas em voo ainda gastam cota); `parar_apos.py --onda N` espera o histórico ter a onda N e
  grava `parar`. É a capacidade `parar-apos-onda`; gravar `parar` direto (comando do LEIA) é `parar-de-despachar`.
  O próprio juntador grava `parar` no fim natural do laço.
- Regra de fim do juntador (`fechar_onda`): depois de duas ondas seguidas abaixo de `gate_novos`, cria uma onda de
  **calibração** (vizinhanças das sementes não achadas); se ela também fica abaixo, é o fim; também é o fim quando
  não há célula nova para a onda seguinte. Os `detalhe` abaixo resumem essa regra e dizem que é resumo.
- `gerador.py --trabalhadores N` passa por cima do `config.json`, e cada processo guarda o valor de quando subiu: o
  `configurado` lido do arquivo pode não ser o em uso. A primeira linha de `logs/gerador-*.out.log` diz "com N
  trabalhadores", mas o nome do log muda a cada religada (`.2`, `.3`), por isso nenhum exemplo declara `em_uso`: o
  em uso desses controles fica "não confirmado" até um recibo com `efeito: valeu`.

### A.1 `laco-embeddings/laco.json` (em voo)

```json
{
  "formato": 1,
  "id": "modelos-de-embeddings",
  "titulo": "Modelos de embeddings da busca",
  "ticket": "54",
  "execucao": {"id": "embeddings-2026-10-14", "inicio": "2026-10-14T20:36:47-03:00", "terminou_em": null},
  "nos": [
    {"id": "plano", "titulo": "Plano", "papel": "etapa", "detalhe": "as células da onda 1"},
    {"id": "despachante", "titulo": "Despachante", "papel": "etapa", "detalhe": "tabela de modelos do gateway a cada 60 s; modelo que falha fica fora por um tempo"},
    {"id": "geradores", "titulo": "Geradores", "papel": "etapa", "detalhe": "grupos pt-en e zh; os modelos só respondem, o script grava"},
    {"id": "juntador", "titulo": "Juntador", "papel": "etapa", "detalhe": "fecha a onda, junta o catálogo, cria a bola de neve"},
    {"id": "parada", "titulo": "Parada", "papel": "decisao", "detalhe": "resumo: 2 ondas abaixo do valor, depois a onda de calibração; ou sem células novas"},
    {"id": "teto", "titulo": "Teto", "papel": "controle", "detalhe": "tentativas ou horas, o que vier antes"},
    {"id": "painel", "titulo": "Painel", "papel": "observador", "detalhe": "observatório; o atualizador relê os dados a cada 30 s"},
    {"id": "conferencia", "titulo": "Conferência", "papel": "fora-dos-scripts", "detalhe": "o maestro confere a lista na fonte primária"}
  ],
  "ligacoes": [
    {"de": "plano", "para": "geradores", "palavra": "células", "tipo": "segue"},
    {"de": "despachante", "para": "geradores", "palavra": "modelos", "tipo": "segue"},
    {"de": "geradores", "para": "juntador", "palavra": "respostas", "tipo": "segue"},
    {"de": "juntador", "para": "parada", "palavra": "taxa", "tipo": "segue"},
    {"de": "parada", "para": "geradores", "palavra": "repete", "tipo": "repete"},
    {"de": "parada", "para": "conferencia", "palavra": "fim", "tipo": "segue"},
    {"de": "teto", "para": "despachante", "palavra": "limita", "tipo": "condiciona"},
    {"de": "painel", "para": "geradores", "palavra": "observa", "tipo": "observa"},
    {"de": "painel", "para": "juntador", "palavra": "observa", "tipo": "observa"}
  ],
  "controles": [
    {"id": "gate_novos", "no": "parada", "rotulo": "novos por onda abaixo de", "tipo": "numero",
     "faixa": [0.01, 0.5], "escala": "porcento", "unidade": "de novos",
     "quando_vale": "proxima-onda", "releitura": "ao-ligar",
     "configurado": {"arquivo": "config.json", "campo": "gate_novos"}},
    {"id": "teto-tentativas", "no": "teto", "rotulo": "tentativas, no máximo", "tipo": "inteiro",
     "faixa": [100, 20000], "unidade": "tentativas", "aceita_nulo": true, "nulo": "sem limite",
     "quando_vale": "agora", "releitura": "continua",
     "configurado": {"sqlite": "estado/laco.db", "tabela": "controle", "onde": {"chave": "teto"},
                     "coluna": "valor", "json": true, "campo": "pedidos", "ausente": null},
     "precondicoes": {"inicio": {"sqlite": "estado/laco.db", "tabela": "controle", "onde": {"chave": "teto"},
                                 "coluna": "valor", "json": true, "campo": "inicio", "formato": "epoch",
                                 "ausente": null}}},
    {"id": "teto-horas", "no": "teto", "rotulo": "horas, no máximo", "tipo": "duracao", "unidade": "h",
     "faixa": [0.5, 12], "aceita_nulo": true, "nulo": "sem limite",
     "quando_vale": "agora", "releitura": "continua",
     "configurado": {"sqlite": "estado/laco.db", "tabela": "controle", "onde": {"chave": "teto"},
                     "coluna": "valor", "json": true, "campo": "horas", "ausente": null},
     "precondicoes": {"inicio": {"sqlite": "estado/laco.db", "tabela": "controle", "onde": {"chave": "teto"},
                                 "coluna": "valor", "json": true, "campo": "inicio", "formato": "epoch",
                                 "ausente": null}}},
    {"id": "trabalhadores_por_gerador", "no": "geradores", "rotulo": "trabalhadores por gerador", "tipo": "inteiro",
     "faixa": [1, 40], "unidade": "trabalhadores", "quando_vale": "ao-reiniciar", "releitura": "ao-ligar",
     "configurado": {"arquivo": "config.json", "campo": "trabalhadores_por_gerador"}},
    {"id": "max_celulas_novas_por_onda", "no": "juntador", "rotulo": "células novas por onda, no máximo",
     "tipo": "inteiro", "faixa": [10, 500], "unidade": "células", "quando_vale": "proxima-onda",
     "releitura": "ao-ligar", "configurado": {"arquivo": "config.json", "campo": "max_celulas_novas_por_onda"}},
    {"id": "fracao_da_cota", "no": "despachante", "rotulo": "parte da cota diária de cada modelo", "tipo": "numero",
     "faixa": [0.1, 1], "escala": "porcento", "unidade": "da cota", "quando_vale": "ao-reiniciar",
     "releitura": "ao-ligar", "configurado": {"arquivo": "config.json", "campo": "fracao_da_cota"}},
    {"id": "excluir_manual", "no": "despachante", "rotulo": "modelos que não recebem pedidos", "tipo": "lista",
     "itens": {"max": 500, "comprimento": 200}, "quando_vale": "ao-reiniciar", "releitura": "ao-ligar",
     "configurado": {"arquivo": "config.json", "campo": "excluir_manual"}}
  ],
  "capacidades": [
    {"id": "parar-apos-onda", "onda_atual": "onda"},
    {"id": "parar-de-despachar"}
  ],
  "contadores": [
    {"id": "tentativas", "no": "teto", "rotulo": "tentativas", "tipo": "inteiro",
     "origem": {"sqlite": "estado/laco.db", "tabela": "uso", "soma": "tentativas"}},
    {"id": "teto-desde", "no": "teto", "rotulo": "horas contadas desde", "tipo": "hora",
     "origem": {"sqlite": "estado/laco.db", "tabela": "controle", "onde": {"chave": "teto"},
                "coluna": "valor", "json": true, "campo": "inicio", "formato": "epoch"}},
    {"id": "onda", "no": "juntador", "rotulo": "onda", "tipo": "inteiro",
     "origem": {"sqlite": "estado/laco.db", "tabela": "controle", "onde": {"chave": "onda"},
                "coluna": "valor", "json": true}},
    {"id": "curva", "no": "parada", "rotulo": "novos por onda", "tipo": "serie",
     "campos": ["onda", "novos", "taxa_novos"],
     "origem": {"sqlite": "estado/laco.db", "tabela": "controle", "onde": {"chave": "historico"},
                "coluna": "valor", "json": true}},
    {"id": "pedidos", "no": "geradores", "rotulo": "pedidos, todas as ondas", "tipo": "contagem",
     "origem": {"sqlite": "estado/laco.db", "tabela": "pedidos", "contagem": true, "agrupar": "estado"}},
    {"id": "aptos", "no": "despachante", "rotulo": "modelos aptos", "tipo": "inteiro",
     "origem": {"arquivo": "estado/despachante.json", "campo": "aptos"},
     "hora": {"arquivo": "estado/despachante.json", "campo": "gerado_em", "formato": "iso"}},
    {"id": "plataformas-aptas", "no": "despachante", "rotulo": "pools do gateway com modelo apto", "tipo": "lista",
     "origem": {"arquivo": "estado/despachante.json", "campo": "pools_aptos"},
     "hora": {"arquivo": "estado/despachante.json", "campo": "gerado_em", "formato": "iso"}}
  ],
  "sinal": {
    "fontes": [
      {"arquivo": "estado/despachante.json", "campo": "gerado_em", "formato": "iso"},
      {"mtime": "livros/pt-en.jsonl"},
      {"mtime": "livros/zh.jsonl"}
    ],
    "sem_sinal_apos_s": 300
  },
  "parado": {"sqlite": "estado/laco.db", "tabela": "controle", "onde": {"chave": "parar"},
             "coluna": "valor", "json": true, "ausente": false},
  "esperando_cota": {
    "aptos": {"arquivo": "estado/despachante.json", "campo": "aptos"},
    "fora": {"arquivo": "estado/despachante.json", "campo": "fora_agora"}
  }
}
```

| Item | Fato ou suposição | Fonte ou motivo |
|---|---|---|
| `id`, `titulo`, `ticket` | fato | título e número do ticket 54 |
| `execucao.id: "embeddings-2026-10-14"` | **atribuído pelo registro, não lido** | nenhum arquivo do laço tem id de execução; o maestro fixou o padrão laço + data de início. Religar os processos (logs `.2` e `.3`) não é execução nova |
| `execucao.inicio` | fato | `controle.teto.inicio` = 1792021007,69 = 2026-10-14 23:36:47 UTC = 20:36:47 local; ticket 54: "contadas desde 20h36" |
| nós, papéis e ligações | fato no essencial | LEIA (papéis, bola de neve, parada por gate e calibração em `juntador.py`), ticket 54 (conferência pelo maestro, painel), maestro (só processos, sem recrutas neste laço). **Suposição:** as palavras das setas e o painel ligado a geradores e juntador |
| controles, origens e quando valem | fato | chaves reais do `config.json` e do `controle.teto`; maestro: `config.json` só ao ligar, teto e parar no ciclo seguinte |
| faixas | fato (confirmadas pelo maestro) | `gate_novos` 0,01–0,5 (hoje 0,15); teto 100–20 000 tentativas e 0,5–12 h (hoje 5 000 tentativas e 2 h desde 20h36; o que vale de fato é o tempo); trabalhadores 1–40 (hoje 20); células novas por onda 10–500 (hoje 120). `fracao_da_cota` 0,1–1 é **suposição** (não estava na lista do maestro) |
| `excluir_manual` como lista | fato | maestro: única opção de modelo do laço; reiniciar o despachante para valer (LEIA corrigido) |
| `inicio` como precondição do teto | fato | `--teto` zera o `inicio`; o maestro grava direto na tabela preservando-o |
| `ausente` do teto e do `parar` | fato | sem linha `teto`, `teto_atingido` não limita; sem linha `parar`, os scripts leem `False` |
| capacidades | fato | `parar_apos.py` e a parada por `controle.parar` (LEIA); `pausar-retomar` fora de propósito |
| contadores | fato | tabelas e chaves de `comum.py`; `estado/despachante.json` reescrito a cada ciclo de 60 s com `gerado_em` |
| `plataformas-aptas` = `pools_aptos` | fato | confirmado pelo maestro (2026-10-14), rótulo "pools do gateway com modelo apto"; o `despachante.json` também tem `familias_aptas`, que não entra |
| `esperando_cota` por `aptos` e `fora_agora` | fato com ressalva | regra do maestro: aptos 0 ou todos fora até a virada. `fora_agora` conta os modelos com `fora_ate` no futuro, o que inclui pausas curtas por falha, não só a virada da cota; aceito pelo maestro, e o detalhe do nó Despachante avisa ("modelo que falha fica fora por um tempo") |
| `sem_sinal_apos_s: 300` | **suposição** | cinco ciclos do despachante; o maestro pode preferir outro limite |
| sinal pelos livros-razão | fato | cada gerador acrescenta uma linha por chamada em `livros/<grupo>.jsonl` |

### A.2 `laco/laco.json` (pesquisa ampla, terminada)

```json
{
  "formato": 1,
  "id": "pesquisa-ampla",
  "titulo": "Pesquisa ampla: lugares e mecanismos de busca",
  "ticket": "50",
  "execucao": {"id": "ampla-2026-10-13", "inicio": "2026-10-13T11:22:00-03:00", "terminou_em": "2026-10-13T15:13:09-03:00"},
  "nos": [
    {"id": "plano", "titulo": "Plano", "papel": "etapa", "detalhe": "98 células da onda 1: 7 ângulos, 7 línguas, 2 formulações"},
    {"id": "despachante", "titulo": "Despachante", "papel": "etapa", "detalhe": "tabela de modelos do gateway a cada 60 s"},
    {"id": "geradores", "titulo": "Geradores", "papel": "etapa", "detalhe": "grupos pt-es, en-de-ru e zh-ja"},
    {"id": "juntador", "titulo": "Juntador", "papel": "etapa", "detalhe": "fecha a onda, junta o catálogo, cria a bola de neve"},
    {"id": "ambiguos", "titulo": "Ambíguos", "papel": "fora-dos-scripts", "detalhe": "o recruta Tear (Sonnet 5.5) decidiu juntar, separar ou quarentena, em catalogo/decisoes.jsonl"},
    {"id": "parada", "titulo": "Parada", "papel": "decisao", "detalhe": "parou depois da onda 5, por decisão do Gustavo; a regra do gate não chegou a valer"},
    {"id": "teto", "titulo": "Teto", "papel": "controle", "detalhe": "tentativas ou horas, o que vier antes"},
    {"id": "mare", "titulo": "Maré de novos", "papel": "observador", "detalhe": "a curva de novos por onda", "carta": "painel-mare"},
    {"id": "chat", "titulo": "Estado no chat", "papel": "observador", "detalhe": "o estado no chat a cada 10 min; na partida, recrutas Bússola, Faísca, Brasa e Centelha acompanharam os processos e foram dispensados"},
    {"id": "conferencia", "titulo": "Conferência", "papel": "fora-dos-scripts", "detalhe": "conferidor sobre os mais citados e as sementes"},
    {"id": "auditoria", "titulo": "Auditoria", "papel": "fora-dos-scripts", "detalhe": "auditoria por amostra"},
    {"id": "sintese", "titulo": "Síntese", "papel": "fora-dos-scripts", "detalhe": "a síntese do maestro", "carta": "painel-sintese"}
  ],
  "ligacoes": [
    {"de": "plano", "para": "geradores", "palavra": "células", "tipo": "segue"},
    {"de": "despachante", "para": "geradores", "palavra": "modelos", "tipo": "segue"},
    {"de": "geradores", "para": "juntador", "palavra": "respostas", "tipo": "segue"},
    {"de": "juntador", "para": "ambiguos", "palavra": "ambíguos", "tipo": "segue"},
    {"de": "ambiguos", "para": "juntador", "palavra": "decisões", "tipo": "segue"},
    {"de": "juntador", "para": "parada", "palavra": "taxa", "tipo": "segue"},
    {"de": "parada", "para": "geradores", "palavra": "repete", "tipo": "repete"},
    {"de": "parada", "para": "conferencia", "palavra": "fim", "tipo": "segue"},
    {"de": "conferencia", "para": "auditoria", "palavra": "amostra", "tipo": "segue"},
    {"de": "auditoria", "para": "sintese", "palavra": "síntese", "tipo": "segue"},
    {"de": "teto", "para": "despachante", "palavra": "limita", "tipo": "condiciona"},
    {"de": "mare", "para": "juntador", "palavra": "observa", "tipo": "observa"},
    {"de": "chat", "para": "geradores", "palavra": "observa", "tipo": "observa"}
  ],
  "controles": [
    {"id": "gate_novos", "no": "parada", "rotulo": "novos por onda abaixo de", "tipo": "numero",
     "faixa": [0.01, 0.5], "escala": "porcento", "unidade": "de novos",
     "quando_vale": "proxima-onda", "releitura": "ao-ligar",
     "configurado": {"arquivo": "config.json", "campo": "gate_novos"}},
    {"id": "teto-tentativas", "no": "teto", "rotulo": "tentativas, no máximo", "tipo": "inteiro",
     "faixa": [100, 20000], "unidade": "tentativas", "aceita_nulo": true, "nulo": "sem limite",
     "quando_vale": "agora", "releitura": "continua", "configurado": {"declarado": 20000}},
    {"id": "teto-horas", "no": "teto", "rotulo": "horas, no máximo", "tipo": "duracao", "unidade": "h",
     "faixa": [0.5, 12], "aceita_nulo": true, "nulo": "sem limite",
     "quando_vale": "agora", "releitura": "continua", "configurado": {"declarado": 6}},
    {"id": "trabalhadores_por_gerador", "no": "geradores", "rotulo": "trabalhadores por gerador", "tipo": "inteiro",
     "faixa": [1, 40], "unidade": "trabalhadores", "quando_vale": "ao-reiniciar", "releitura": "ao-ligar",
     "configurado": {"declarado": 20}},
    {"id": "excluir_manual", "no": "despachante", "rotulo": "modelos que não recebem pedidos", "tipo": "lista",
     "itens": {"max": 500, "comprimento": 200}, "quando_vale": "ao-reiniciar", "releitura": "ao-ligar",
     "configurado": {"arquivo": "config.json", "campo": "excluir_manual"}}
  ],
  "capacidades": [
    {"id": "parar-apos-onda"},
    {"id": "parar-de-despachar"}
  ],
  "contadores": [
    {"id": "tentativas", "no": "teto", "rotulo": "tentativas", "tipo": "inteiro",
     "origem": {"arquivo": "estado/laco_final.json", "campo": "tentativas"}},
    {"id": "itens", "no": "juntador", "rotulo": "itens no catálogo", "tipo": "inteiro",
     "origem": {"arquivo": "estado/laco_final.json", "campo": "itens"}},
    {"id": "curva", "no": "parada", "rotulo": "novos por onda", "tipo": "serie",
     "campos": ["onda", "novos", "taxa_novos"],
     "origem": {"arquivo": "estado/laco_final.json", "campo": "ondas"}},
    {"id": "modelos", "no": "despachante", "rotulo": "modelos usados", "tipo": "inteiro",
     "origem": {"arquivo": "estado/laco_final.json", "campo": "modelos_usados"}}
  ],
  "sinal": {"fontes": [{"arquivo": "estado/laco_final.json", "campo": "terminou_em", "formato": "iso"}],
            "sem_sinal_apos_s": 300},
  "parado": {"sqlite": "estado/laco.db", "tabela": "controle", "onde": {"chave": "parar"},
             "coluna": "valor", "json": true, "ausente": false}
}
```

| Item | Fato ou suposição | Fonte ou motivo |
|---|---|---|
| `id`, `titulo`, `ticket` | fato (id escolhido aqui) | ticket 50; o id `pesquisa-ampla` é proposta |
| `execucao.id: "ampla-2026-10-13"` | **atribuído pelo registro, não lido** | nenhum arquivo do laço tem id de execução; padrão do maestro (laço + data de início) |
| `execucao.inicio` | fato | ticket 50: teto "contado desde a partida, 14:22Z" = 11:22 local |
| `execucao.terminou_em` | fato | `estado/laco_final.json`: `terminou_em` 2026-10-13T18:13:09Z = 15:13:09 local |
| nós e papéis | fato no essencial | LEIA (conferência, auditoria e síntese pelo maestro, fora dos scripts; decisões de ambíguos em `catalogo/decisoes.jsonl`), ticket 50 (parada depois da onda 5; estado no chat por `painel.py`). **Suposição:** ligar a carta `painel-sintese` ("Super Trunfo da busca") ao nó Síntese, e as palavras das setas |
| recrutas só no detalhe, sem opções de recruta | fato | maestro (2026-10-14, corrigindo a resposta anterior): a ampla teve recrutas na partida (Bússola, Faísca, Brasa e Centelha, dispensados; o Tear decidiu os ambíguos). Como o laço terminou, eles entram só no detalhe dos nós `chat` e `ambiguos`, sem controle |
| `gate_novos` no `config.json` | fato | 0,05; a parada real foi por decisão do Gustavo depois da onda 5, sem alcançar o gate nem a calibração |
| teto e trabalhadores **declarados**, não lidos | fato | ticket 50: teto 20 000 tentativas ou 6 h; 20 trabalhadores por gerador ("fica em 20"). Ler do banco ou do `config.json` daria errado: o `config.json` diz 6 (os geradores subiram com `--trabalhadores`) e o `controle.teto` do banco foi regravado depois do fim (11 400 tentativas, 3 h, `inicio` 13/10 21h55 local) |
| contadores do `laco_final.json`, não do banco | fato | o banco seguiu em uso depois do fim (chave `parar_triagem` da triagem; `SUM(tentativas)` hoje 10 534, contra 7 382 no fim do laço) |
| `tentativas` = 7 382 | fato | `laco_final.json`, fechamento às 18:13:09Z (confirmado pelo maestro). Os 7 388 do comentário de 18:13Z do ticket 50 incluem chamadas em voo que terminaram logo depois (log do despachante: 7 386 às 18:13:41Z) |
| faixas | fato | as mesmas do A.1, confirmadas pelo maestro; para um laço terminado não chegam a ser usadas (nenhum pedido de mudança é aceito) |
| `parar-apos-onda` sem `onda_atual` | escolha | o `controle.onda` do banco ficou 6 depois do fim; mostrar "onda 6" num laço terminado enganaria |
