# Construção do portal: estado para retomar

Quem retoma depois de um `/clear`: leia `proposta.md` (a especificação) e este arquivo. Construtor: Designer
(Claude Opus 5.5, esforço alto; era Fable 5.1, troca pedida pelo Gustavo em 2026-10-14). Revisor: Prumo (`maestri ask "Prumo"`). Pedidos ao maestro: `maestri ask "Claude Code"`.

## Regra fixa: a quem responder (aviso do maestro "Claude Code", 2026-10-15 ~21h30)

Quem coordena a frente do painel e o Designer agora é o maestro **"Amigo do Maestro"**. Entregas e recados vão para ele
(`maestri ask "Amigo do Maestro" "..."` e depois `maestri check "Amigo do Maestro"`), não mais para o "Claude Code".

## Regra fixa: encerrar o Edge das capturas (pedido do maestro, 2026-10-14)

Só se mata o `msedge` do **perfil próprio da captura**, filtrando pela linha de comando que contém o
`--user-data-dir` único daquela captura (PowerShell: `Get-CimInstance Win32_Process -Filter "Name='msedge.exe'" |
Where-Object { $_.CommandLine -match '<perfil>' } | Stop-Process`). **Nunca** por nome de imagem (`taskkill /IM
msedge.exe`), nem por título de janela, nem "todos os msedge". O Edge do Gustavo fica intocado. Vale para mim e para
todo subagente: copiar esta regra em todo brief que mande capturar com o Edge. (Motivo: em 2026-10-14 ~19h36 um
subagente rodou um `taskkill` largo de msedge.)

## Regras fixas das cartas de rodada (retorno do Gustavo pelo maestro, 2026-10-14)

1. Nem toda rodada tem carta: o maestro só pede quando o visual explica algo que o texto não explica.
2. A carta segue **a ordem das perguntas da rodada** (a `prototipo-12-sumario` trocou a ordem: pulos/catálogo,
   órfãos, misc/, contra catálogo, genérico, órfãos da rodada). Copiar esta regra em todo brief de carta.

## Marco atual

**Estado em 2026-10-14, sessão 2 (depois do `/clear`).**
- Marco 3: aprovado pelo Prumo. Marco 4: aprovado pelo Prumo na revisão dirigida.
- Marcos 1–2: as DUAS pendências do Prumo estão em correção por subagente da trilha de dados (lançado nesta sessão);
  quando ele terminar: rodar as suítes, anotar aqui e pedir revisão dirigida ao Prumo.
  Parecer: `C:/Projetos/context-hub/.maestri/roles/d4ce63fd-ce3e-45b5-88f6-6bbd68695030/revisao-dirigida124/parecer.md`.
- Marco 5 (Autorizações): construído e verificado contra a torre real; enviado ao Prumo junto com o 6.
- Marco 6 (Cartas, leitor, Rumo): conferido no navegador, corrigido, `cartas.json` preenchido com as 11 cartas
  (respostas do maestro abaixo), capturas em `conferencia/marco6-*.png`; enviado ao Prumo junto com o 5.
- `projeto.codigos`: feito pelo subagente (`Projeto._ler_codigos`, `montar_estado`, LEIA.md, 4 testes; 105 OK),
  `projeto.json` real com Q e R, fixture `estado-esperado.json` com `"codigos": {}` e linha no `fixtures/LEIA.md`;
  conferido na tela. Contrato na §3.7.

## Feito

- Marco 7, trilha de dados (subagente, 2026-10-14), a conferir nos testes reais: `nucleo/aviso.py` (`Emissor`: thread
  daemon com `Event.wait(5 s)`, acordada pelo `POST /api/caixa` e pelo `tentar`; só com `MAESTRI_PIPE`,
  `MAESTRI_TERMINAL_ID` e executável encontrável; junta os pendentes num `ask` só, 1800 s, nunca dois ao mesmo tempo;
  depois `check` 60 s → `--raw "
"` → `check` → `"(enviar)"`; erro/timeout/check falho → `pendente` com
  `ultimo_erro` e `proximo` +1, +5, +15 min; 4ª falha → `falhou`; `vigiar_uma_vez`/`--vigiar PASTA [--intervalo N]
  [--uma-vez]` para o canal B, marca `entregue` ao imprimir), `torre.py` (`iniciar_emissor`, `acordar_emissor`,
  `--abrir`, print do modo), `leitores.resolver_executavel`, `caixa.Fila` relê `.avisos.json` quando o arquivo muda
  em disco (convivência A/B; pior caso, aviso repetido, nunca perdido), `iniciar.cmd` (`cd /d %~dp0`, confere python,
  `python nucleo	orre.py projeto.json --abrir`, `pause` em erro), LEIA.md com a seção do aviso. 15 testes novos
  com um `maestri` falso em Python (`teste_aviso.py`): 120 OK (eram 105), 4 do projeto real OK, neutralidade vazia,
  RSS do servidor com emissor em repouso 25,6 MiB. Textos para a proposta (§4.3 A e B, §3.5/§3.7 fila, §5.2,
  `aviso.executavel`) estão no relatório do subagente; publicar na proposta quando os testes reais fecharem o canal.
- Marco 6, conferência (construtor, sessão 2, 2026-10-14): capturas em 1600×900, 1280×800 e página inteira
  (`conferencia/marco6-cartas-*`, `marco6-leitor-*`, `marco6-rumo-*`), mais medição por puppeteer (scratchpad,
  `mede_marco6.js`, `mede_miniaturas.js`): zero erros de JS; radar com 10 ecos, nenhum rótulo fora do SVG, nenhuma
  sobreposição; leitor preenche a altura toda (tira 45 px + iframe 855 px); as 11 miniaturas carregam em 2 s no Edge
  (o branco nas capturas por `--virtual-time-budget` é só o instante do screenshot). Correções feitas: miniatura da
  mestra com `loading="eager"`; botão "Abrir <título da carta>" (era "Abrir o System design", fixo; o núcleo é
  genérico); `ticket: null` = "serve ao mapa inteiro" (chip só com ticket real; a string "a confirmar" vira o selo
  âmbar); radar redesenhado: ecos em ângulos iguais com raio alternado, rótulos fora do círculo ligados por linha
  pontilhada (etiqueta de radar), viewBox com margens; classe do SVG `radar-tela` (a antiga `radar` colidia com o
  ícone do menu); ícone do cabeçalho `.rota-atual svg` em 22 px; Rumo empilhado (radar + lista, fora da rota em duas
  colunas, diário, glossário); tira do leitor com propósito recortado a 72 caracteres e o texto completo na dica;
  grupos de cartas fluem lado a lado (um cartão por grupo não ocupa uma linha inteira), cartão em 320 px, chip do
  ticket com reticências; grupo sem ticket se chama "servem ao mapa inteiro (sem ticket dono)"; fundo do iframe do
  leitor em azul-noite; `marcarCodigos` em `torre.js` (ver pendência no "Marco atual").
- Marco 6 (construtor, 2026-10-14), escrito na sessão 1: `web/telas/cartas.js` (carta mestra grande com
  miniatura em escala 0,5; grade por ticket na ordem do plano de voo com miniaturas em escala 0,25 (iframe
  `sandbox="allow-scripts"`, `loading="lazy"`), título, propósito, ticket, decisão em dica, data com tipo; faixa
  "arquivo de cartas" em sépia com selo "histórica"; campos sem fonte mostram "a confirmar"; leitor em tela cheia na
  rota `#/cartas/<id>` usando o `#leitor` do index.html, com tira (propósito, ticket, data, decisão) e ações
  Comentar esta carta / Aprovar / Recusar; o leitor segue a rota e fecha no evento `torre:redesenhando`),
  `web/telas/rumo.js` (radar SVG circular com varredura em CSS e ecos focáveis com dica tema+gatilho, lista ao
  lado; fora da rota em duas colunas; diário de bordo em linha do tempo com `details`; glossário em `dl`), CSS
  correspondente no fim de `torre.css`. Em `torre.js`: `rodapeDeAcoes(alvo, op)` ficou genérico (ticket ou carta;
  chave `tipo:id`; exportado e passado às telas como `u.acoes`), `esquecerAcoes`, evento `torre:redesenhando`
  disparado antes de cada redesenho. Próximo: subir a torre real (8770) e a da fixture (8771), capturar
  `#/cartas`, `#/cartas/<id>` (leitor) e `#/rumo` em 1600×900 e 1280×800, corrigir o que aparecer (provável:
  tamanhos das miniaturas, tira do leitor, posição do formulário de ação no leitor), preencher o `cartas.json`
  real com as respostas abaixo, e só então pedir a revisão dos marcos 5 e 6 ao Prumo.
- Marco 5 (junção, construtor, 2026-10-14), verificado contra a torre real, a entregar ao Prumo:
  `web/telas/autorizacoes.js` + CSS. Lista à esquerda por situação (aguardando você em âmbar, malformadas,
  respondidas com carimbo ENTREGUE | NA FILA, suspensas, absorvidas esmaecidas); rodada à direita com contexto,
  miniatura viva da carta (iframe `sandbox="allow-scripts"`, escala 0,5, link para a tela Cartas) e as perguntas
  como cartões numerados "pergunta N" (o id nunca aparece): `escolha` (rádios + "nenhuma destas, e sim…"),
  `varias` (caixas), `aprovar` (Aprovar | Aprovar com ajuste | Recusar; ajuste e recusa exigem comentário),
  `texto`, `proposta` (tabela editável: editar célula, ligar/desligar, subir/descer e arrastar, + linha `nova-N`,
  remover, "Desfazer tudo", painel "o que mudou" em palavras; só as operações em `pode`); comentário em toda
  pergunta; "por quê" ao expandir; recomendação só marcada, nunca vale como resposta. Rascunho em
  `localStorage` (`torre:<projeto>:<rodada>:<base>`) a cada mudança, com o `envio` dentro; "Enviar à torre" com
  validação local (nada respondido, veredito sem comentário); erro ambíguo (rede/5xx) congela o par
  (envio, corpo) em `emVoo` e "Tentar de novo" reenvia exatamente ele; `409 rodada-mudou` guarda o rascunho e,
  quando a versão nova chega, mostra o rascunho antigo em palavras com "Copiar para a versão nova" / "Descartar";
  `409 envio-conflito` relê a mensagem gravada. Depois de enviar, "o que foi gravado" vem de
  `GET /api/caixa/<envio>` (sobrevive a recarregar) com o estado do aviso; "Corrigir resposta" manda um envio
  novo com `substitui`. Rodadas respondidas/absorvidas mostram a resposta em palavras. Verificado por script
  contra a torre real: cinco tipos preenchidos, recarga mantém o rascunho (inclusive a emenda), 409 real por
  edição do arquivo da rodada → cópia para a versão nova → envio → `.md` no formato da §4.2 com a lista de
  mudanças da proposta e `corpo.respostas.<id>` → lista mostra NA FILA → correção com `substitui`. Capturas em
  `conferencia/marco5-*.png`.
- `projeto.json` real criado na pasta do portal (conteúdo da §3.2), `rodadas/` e `caixa/` criados,
  `cartas.json` inicial só com o System design (`decisao: "a confirmar"`; o resto entra no marco 6 com as
  perguntas ao maestro). A torre do projeto sobe com `python nucleo/torre.py projeto.json` na porta 8770.
- Marco 4 (tela, construtor, 2026-10-14), corrigido depois da recusa, em revisão dirigida: `web/telas/partidas.js` (letreiro de palhetas
  com uma linha por ticket, cascata na entrada, letras que viram só onde o título mudou; filtros por estado e
  tipo em chips com contagem, busca por título ou número; filtros vivem na rota `?estado=&tipo=&q=` e são
  aplicados sem redesenhar; setas, Home/End e Enter no letreiro; vista **Rotas** com o grafo de todas as
  dependências por caminho mais longo, resolvidos esmaecidos, ciclo e dependência inexistente, filtro esmaece
  os nós fora), ações da gaveta em `torre.js` (Comentar, Aprovar, Recusar → `POST /api/caixa`, `envio` UUID
  reaproveitado em "tentar de novo", recusa exige motivo, texto até 20 000, confirmação que sobrevive às
  atualizações até ser dispensada ou a gaveta fechar), CSS correspondente. Verificado por script no Edge
  headless contra a torre real (porta 8771, cópia da fixture): seis arquivos reais gravados na caixa (comentário
  com `---`/`estado: lida` virou três linhas citadas e o frontmatter ficou `estado: nova`), recusa sem motivo
  barrada, filtros e foco na busca sobrevivem a uma mudança real num ticket, Rotas com dicas por foco e Enter.
  Capturas em `conferencia/marco4-*.png`.
- Marcos 1–2 (dados, subagente, 2026-10-14): `nucleo/leitores.py`, `nucleo/caixa.py`, `nucleo/torre.py`,
  `nucleo/LEIA.md`, `nucleo/testes/{apoio,teste_leitores,teste_caixa,teste_torre}.py`,
  `testes-do-projeto/teste_projeto_real.py`. Rodado pelo construtor: 69 testes do núcleo OK (junction criada sem
  privilégio, não pulado), 4 do projeto real OK (52 tickets, 5 critérios, 0 problemas nos arquivos reais), grep de
  neutralidade vazio (só `__pycache__`, removidos). Relatório do subagente com os desvios de detalhe está na seção
  "Decisões de detalhe" abaixo. Servidor sobre a fixture: copiar `nucleo/testes/fixtures/horta` para uma pasta
  temporária e `python nucleo/torre.py <cópia>/portal/projeto.json` (porta 8771); sobre o projeto real:
  `python nucleo/torre.py projeto.json` (o `projeto.json` real ainda não existe; entra no marco 5).
- Marco 3 (tela, construtor), em revisão dirigida pelo Prumo depois de uma recusa (ver "Revisões"): `nucleo/web/` com `index.html`, `torre.css`, `torre.js` (casca:
  rotas no hash, estado de `/api/estado`, vigia de `/api/versao` a cada 3 s, contador âmbar em palhetas, selo e
  diálogo de problemas, faixa "diga respondi", dicas por hover = foco = clique, glossário sublinhado, gaveta do
  ticket com foco preso e `?ticket=NN` na rota, brisa), `icones.js` (SVG próprios), `telas/torre.js` (pista com as
  luzes dos critérios, altímetro, plano de voo em SVG com camadas da API, ciclo e dependência inexistente, aguardando
  você, últimos pousos) e esboços `telas/{partidas,autorizacoes,cartas,rumo}.js`. Ações da gaveta (Comentar,
  Aprovar, Recusar) estão desenhadas e desligadas até o marco 4. Capturas em `conferencia/marco3-*.png` (1600×900,
  1280×800, gaveta aberta), tiradas com um servidor de desenvolvimento descartável que serve a fixture como API
  (fica no scratchpad do construtor, fora do projeto).
- Marco 0: fixture `nucleo/testes/fixtures/horta/` + `estado-esperado.json` + `fixtures/LEIA.md` (decisões de
  detalhe do esquema, regra de comparação). Gerada por script do construtor; os hashes `base` e `corpo_hash`
  são reais.

## Redireção visual (retorno do Gustavo, 2026-10-14)

Retorno, palavra por palavra (também no fim de `pedido.md`): "não gostei da tipografia, pois não ta legível, as letras
estão muito finas e não dá pra ler a maioria dos textos, não ta aquela fonte gostosa de ler. E também Quero um design
'aconchegante', mais 'vivo' e mais 'interativo'." O maestro pediu a decisão combinada com o Prumo; ele mostra a nova
direção ao Gustavo antes de eu aplicar nas cinco telas. Núcleo (`nucleo/*.py`) e interface de rodadas e caixa não mudam.

**Diagnóstico.** O fundo noturno faz texto claro de peso 400 parecer mais fino do que é; os corpos de 12,5–13,5 px em
cinzas apagados (`--texto-fraco`, `--texto-apagado`) e os rótulos condensados em caixa alta espaçada (Big Shoulders)
completam a ilegibilidade. Só trocar a fonte e clarear o fundo seria "v2 só restilizada" (já recusada noutro visual):
a forma muda.

**Direção proposta ao Prumo (2026-10-14, aguardando o retorno dele): tema "Mesa de mapas".** Uma expedição, de dia:
o Gustavo é a base; maestro e agentes são a expedição. Destino = o cume com cinco bandeiras (critérios); plano de voo =
a trilha desenhada num mapa de papel, com acampamentos (tickets); rodadas = cartas da expedição esperando resposta da
base (papel, selo, carimbo que bate ao aprovar); cartas (designs) = folhas de mapa num quadro de cortiça; radar = "no
horizonte" (binóculo); diário de bordo = diário da expedição; glossário = legenda do mapa. Clima: papel creme, tinta
quase preta, madeira e terracota; cor por papel mantida (terracota = espera você; musgo = resolvido; petróleo = vivo
agora; tijolo = bloqueado/recusado; pedra = aberto). Tipografia embarcada no núcleo: Nunito Sans (corpo 16 px, peso 500),
Fraunces (títulos) e JetBrains Mono (caminhos); contraste AA; nada abaixo de 14 px; sem caixa alta espaçada em
conteúdo. Vivo: trilha que se desenha ao abrir, acampamento de hoje pulsando, brilho quente que apaga no que mudou,
bandeirinha da caixa de correio que sobe com carta esperando. Interativo: mapa com arrastar e zoom, cartões que viram,
carta que abre do envelope, carimbo com batida, filtros táteis; `prefers-reduced-motion` e as mesmas regras de foco,
dica e rota (`data-foco`, `#hash`, dicas-botão) para os roteiros do Prumo continuarem valendo.

**Retorno do Prumo (2026-10-14, `portal/revisao-direcao-visual.md`): direção recomendada para a AMOSTRA, sem aceite
do visual antes de vê-la.** Ajustes incorporados à decisão:
1. A metáfora acompanha, não obriga: os nomes na frente são os conhecidos (Início, Tickets, Responder, Designs,
   Decisões com o horizonte e a legenda/glossário); a expedição entra em ícones, subtítulos e clima. Fluxos que já
   funcionam não mudam só por mudar.
2. A trilha mostra dependências reais e ramificações (o mesmo grafo de hoje), nunca sequência ou progresso inventados;
   as cinco bandeiras do cume seguem o estado dos critérios da API, não a contagem de tickets.
3. O diagnóstico de fonte e fundo é hipótese; o fato é a leitura ruim. As três fontes são candidatas: corpo 16 px ou
   mais, piso de 14 px em tudo (chips, dicas, metadados), pesos reais embarcados, entrelinha e largura de linha
   confortáveis; a amostra traz texto real longo e curto e um título comprido, não só capa; textura só fora das áreas
   de leitura; as cores de estado passam por conferência de contraste.
4. Nada essencial fica escondido em verso, envelope ou arrastar. Interação útil: abrir ticket, explorar dependência,
   filtrar, comparar emenda, confirmar resposta. Zoom e arrastar são opcionais, com teclado, controles e "restaurar
   vista". Brilho só em mudança real de dado (não a cada leitura do vigia); a bandeira distingue "aguarda você" de
   "salvo/aviso entregue"; o carimbo só confirma gravação aceita, nunca finge entrega. Animações discretas e curtas,
   `prefers-reduced-motion`, foco, rolagem e rascunho preservados.
5. A amostra estática decide clima e leitura e traz uma interação pequena demonstrável; o início deixa evidente o que
   espera resposta e o próximo passo.
6. Marco 7 em paralelo com dono separado (subagente no servidor/aviso); qualquer ajuste no front é combinado comigo;
   nenhuma promessa de "volta direta ao maestro" antes da prova real.

**Amostra, primeira revisão do Prumo (2026-10-14, `portal/revisao-amostra-v2.md`): clima e fontes mantidos; quatro
correções feitas.** (1) Texto dentro do SVG encolhia com a escala (15 px viravam 13,2 em 1600 e 10,1 em 1280): os
rótulos viraram botões HTML posicionados por porcentagem sobre o mapa (`--x`/`--y` em unidades do viewBox), com
tamanhos reais; o SVG só desenha fundo, setas e cume; grade em uma coluna até 1400 px. (2) Contraste: `--pedra`
#5a544b, chip "aberto" #4a453d, menu ativo escurece em vez de clarear, setas #6f5a3e (Prumo mede de novo). (3) Fato
do ticket 09 corrigido: só "em andamento; tudo de que dependia já foi resolvido". (4) Setas com ponta (`marker-end`)
de quem bloqueia para quem espera; a trilha decorativa e o "hoje" saíram; o "vivo" fica no anel que pulsa no
acampamento em andamento. Data em "quarta-feira, 14/10/2026"; "Nenhuma pergunta espera você". Devolvida ao Prumo
(segunda revisão pendente).
**Segunda revisão (dirigida, `portal/revisao-amostra-v2-dirigida.md`):** as quatro frentes passaram (contrastes
medidos: chip aberto 7,17:1, pedra 5,65:1, setas 5,15:1, menu ativo 7,63:1). Três pontos corrigidos e devolvidos:
hover do menu escurece; selo "espera N" preso acima da própria tenda (17 e cume subiram, nome do cume à direita,
controles de zoom no canto inferior direito); regra residual de 13,5 px removida (números a 14 px).
**AMOSTRA APROVADA pelo Prumo (2026-10-14, `portal/revisao-amostra-v2-final.md`)** para o maestro apresentar ao
Gustavo (hover 6,61:1; selos nas próprias tendas; 14 px medidos; Enter/setas/Soltar e reduced-motion OK). Aceite só da
amostra: não antecipa a aplicação nas cinco telas nem o marco 7. Encaminhada ao maestro; resposta do Gustavo pendente.

**Ordem.** Marco 7 segue em paralelo. Entrego a AMOSTRA estática da tela de início (`portal/v2/amostra-inicio.html`,
dados reais do projeto copiados no dia) ao Prumo e, pelo maestro, ao Gustavo; só depois do aceite aplico nas cinco
telas (`nucleo/web`, fontes novas em `vendor/fontes` com licenças) e peço a revisão do Prumo como marco "visual v2"
(capturas por tela nos dois tamanhos). Marco 8 confere tudo integrado depois.

## Decisões de detalhe (fora da proposta)

- Tela: a página só usa a API (`/api/estado`, `/api/versao`, `/api/ticket/<n>`); nenhum dado embutido. A gaveta
  tira do Markdown do ticket o `# Título` e as linhas `Type/Status/Blocked by`, que já aparecem em chips.
- Plano de voo: "bloqueado" não ganha cor própria nos nós (quase todo nó fora da primeira camada espera por
  alguém); o nó mostra "espera N" no canto e a cor coral fica para erro (dependência inexistente, ciclo) e para
  o número "bloqueados" do altímetro. Ticket com `Blocked by` inexistente ganha uma caixa fantasma tracejada à
  esquerda ("99 não existe"). O ciclo é desenhado com a aresta ignorada em coral pontilhado e um aviso abaixo.
- Glossário: não marca termos dentro de botões e links (evita botão dentro de botão) nem em títulos grandes.
- A faixa "o maestro não é avisado sozinho" fica sempre até o marco 7 (`CANAL_DE_AVISO_VERIFICADO = false` em
  `torre.js`), e também quando `aviso.disponivel` é falso, com o motivo do servidor.

- Esquema do `/api/estado` fechado em `nucleo/testes/fixtures/LEIA.md` (campos extras: `bloqueios_inexistentes`,
  `ticket_titulo`, `respondida`, `ultima_resposta`, `malformada`, `erro`, `substituida`; ordem; regra de ciclo;
  caminhos relativos a `raiz`).
- `desconhecido` fica fora do plano de voo; `wontfix` e `resolved` não bloqueam.
- Carta: `arquivo` precisa estar diretamente dentro de `pasta` (links relativos da carta resolvem contra
  `/carta/<id>/`).
- A fixture tem a pasta do portal dentro da raiz (`horta/portal/`, `raiz: ".."`), como no projeto real.

## Revisões do Prumo

- **Marco 3, 2026-10-14, recusado** (parecer em
  `C:/Projetos/context-hub/.maestri/roles/d4ce63fd-ce3e-45b5-88f6-6bbd68695030/revisao-marco3/parecer.md`; tema e
  composição aprovados). Achados e o que foi feito, todos verificados por script no Edge headless (puppeteer-core,
  no scratchpad do construtor, com um servidor de desenvolvimento que simula 503 e mudança de versão):
  1. Bloqueante, recuperação da API: agora `vigiarVersao` carrega o estado quando não há um, quando a última leitura
     falhou ou quando a versão mudou, e a versão só é consumida junto de um estado lido; a faixa "Estado não lido"
     (vermelha) aparece enquanto `/api/estado` falha com o servidor no ar. Verificado: 2 falhas iniciais → página
     inteira em 7 s; falha no meio de uma mudança → recupera no ciclo seguinte com o dado novo.
  2. Histórico da gaveta: a rota (`?ticket=NN`) virou a verdade; abrir = `pushState`, fechar (X ou Esc) =
     `pushState` sem o ticket; `conciliarGaveta` faz a gaveta seguir a rota (abre, troca, fecha). Verificado:
     03 → fechar → 05 → voltar = fechada → voltar = 03 → voltar = fechada; avançar reabre.
  3. Foco na atualização: menu montado uma vez; elementos interativos têm `data-foco` estável e o foco é devolvido
     pela chave depois de redesenhar; a gaveta aberta é preenchida de novo com o ticket atual (rolagem e foco
     mantidos); `prenderFoco` devolve o foco pela chave se quem abriu foi redesenhado. Verificado.
  4. Hover = foco = clique no plano: arestas, caixa fantasma e pista viraram grupos SVG focáveis com `data-dica`
     (Enter/espaço fixa a dica como o clique), `aria-label` com os nomes, e `aria-describedby="dica"` enquanto a
     dica está visível; nós têm dica com os nomes de quem bloqueia. `<title>` SVG não é mais usado.
  5. Contraste: `--texto-apagado` passou de `#6f7c99` para `#8b98b5` (5,99:1 sobre `#111a2e`, 5,53:1 sobre
     `#16213a`, 5,18:1 sobre `#1a2642`).
  6. `pedir` monta os cabeçalhos por último: `X-Torre` sobrevive ao `Content-Type` de `api.caixa` (verificado:
     o servidor de desenvolvimento devolve o cabeçalho recebido).
  7. Glossário: regex sem flag global para o `test` do TreeWalker; a varredura usa outra, com `lastIndex` zerado.
  Capturas refeitas em `conferencia/marco3-*.png`.

- **Marco 3, revisão dirigida, 2026-10-14: aprovado com ajustes** (parecer em
  `C:/Projetos/context-hub/.maestri/roles/d4ce63fd-ce3e-45b5-88f6-6bbd68695030/revisao-marcos123/parecer.md`).
  Ajuste feito: o foco e a rolagem da gaveta são restaurados de novo depois de o corpo assíncrono chegar
  (`restaurarGaveta`, chamado com o corpo provisório e com o completo), e a troca de ticket solta o listener
  de teclado anterior (`fechar.soltar`). Verificado: foco em `gaveta-lig-01` dentro da gaveta do 03 sobrevive a
  uma mudança real do título do 03. Também: o foco volta a quem abriu a primeira gaveta da cadeia (não ao
  `body`) quando se fecha uma gaveta aberta a partir de outra.
- **Marcos 1–2, 2026-10-14: recusados** (mesmo parecer). Quatro bloqueantes, em correção por subagente:
  (1) caminhos do `projeto.json`/`cartas.json` escapam das bases (sem `commonpath`); (2) ticket em UTF-8 inválido
  derruba `/api/estado` (500); (3) `.json` da caixa com `envio` lista derruba o estado (500); (4) `.avisos.json`
  com `tentativas: "abc"` impede o arranque. Mais: a frase "em respostas.<id>" do `.md` deve ser
  `corpo.respostas.<id>`. Os desvios de detalhe foram aceitos e publicados na proposta (§3.7 nova, §4.2 corrigida).

- **Marco 4, 2026-10-14: recusado** (parecer em
  `C:/Projetos/context-hub/.maestri/roles/d4ce63fd-ce3e-45b5-88f6-6bbd68695030/revisao-marco4/parecer.md`; tema,
  composição e caminho feliz aprovados). Correções feitas:
  1. Retentativa com o par (envio, corpo) congelado: o primeiro envio guarda `emVoo = {corpo, motivo}` e "Tentar de
     novo" manda exatamente esse corpo; editar o texto não muda o que vai. `409 envio-conflito` é tratado como "o
     primeiro envio foi gravado": a página relê `GET /api/caixa/<envio>` e mostra a confirmação. Nunca troca de UUID
     sozinha. A mesma regra vale no formulário de rodada (marco 5), com `emVoo` guardado no rascunho.
  2. Chip de filtro decide pelo valor atual do filtro no clique (desliga no segundo clique; alterna entre chips).
  3. Roving tabindex reconciliado a cada filtro e a cada redesenho (`reconciliarEntrada`): a linha corrente se
     visível, senão a primeira visível; nunca zero linhas no Tab.
  4. Dicas "espera por" e "dependência quebrada" são botões no fluxo do Tab (`data-foco`), com `aria-label` da linha
     dizendo os nomes; clique ou Enter nelas não abre a gaveta (o clique da linha ignora controles internos; o
     keydown da linha só age com a própria linha focada).
  Sugestões documentais atendidas: "byte a byte" retirado deste diário; §3.7 fala em `ultimo_erro`.

- **Marcos 1–2, correções (subagente, 2026-10-14), em revisão dirigida.** (1) Confinamento: `leitores.confinar`
  (`realpath` + `commonpath`, recusa absoluto, `..`, symlink e junction) em todo caminho do `projeto.json` e do
  `cartas.json` e em todo arquivo descoberto (tickets, rodadas, caixa); fora da base vira problema e não é lido
  nem gravado; `caixa` fora da pasta do portal impede subir. (2) UTF-8 inválido: capturado por arquivo em todos os
  leitores, problema "arquivo não é UTF-8 válido", nada substituído; `/api/ticket/<n>` → 422 `arquivo-ilegivel`.
  (3) `.json` da caixa validado na fronteira (tipos e forma de todos os campos, retrato da rodada); arquivo ruim
  vira problema, não é indexado nem ganha `.md`, no ar e no arranque. (4) `.avisos.json` validado registro a
  registro (`validar_registro_de_aviso`); registro ruim descartado com problema, fila recomposta; `proximo` ruim
  não trava `pendentes()`. (5) Frase do `.md`: `corpo.respostas.<id>`. Rodado pelo construtor: 87 testes do núcleo
  OK (eram 69; junction e symlink criados, nada pulado), 4 do projeto real OK, grep de neutralidade vazio.
  Contratos novos publicados na §3.7 da proposta (422, carta fora da raiz, caixa fora do portal).

- **Marco 4, revisão dirigida, 2026-10-14: APROVADO.** O Prumo reproduziu: retentativa depois de resposta perdida e
  edição manteve UUID e corpo e confirmou `repetido`; chip desliga; Tab continua entrando na lista; dicas por
  clique/Enter não abrem a gaveta. Frase `corpo.respostas` e contratos conferidos.
- **Marcos 1–2, revisão dirigida, 2026-10-14: ainda RECUSADOS** (87 + 4 testes passaram lá; os quatro casos antigos
  estão corrigidos). Duas pendências novas, corrigidas abaixo.
- **Marcos 5 e 6, 2026-10-14: RECUSADOS** (parecer em
  `C:/Projetos/context-hub/.maestri/roles/d4ce63fd-ce3e-45b5-88f6-6bbd68695030/revisao-marcos56/parecer.md`;
  composição aprovada). Seis achados e o que foi feito, verificados por script no Edge (scratchpad:
  `verifica_prumo56.js` na torre real 8770 e `verifica_correcao5.js` na fixture limpa 8771; `fontes_ok.js` sem rede):
  1. Corrigir resposta vinha em branco e o substituto apagava as outras respostas: `iniciarCorrecao` lê a resposta
     gravada (`GET /api/caixa/<envio>`) e cria o rascunho como cópia dela, com `envio` novo e `correcao`
     {arquivo, respostas} guardada no rascunho (sobrevive à recarga; `detalhe` reentra no modo correção ao achar
     o rascunho com `correcao`); o aviso "Corrigindo a resposta" mostra ao vivo "Vai mudar: pergunta N (título)" ou
     "Nada mudou ainda"; `substitui` vem de `correcao.arquivo`; "Limpar rascunho" vira "Desistir da correção".
     Verificado: cinco tipos gravados → recarga → Corrigir → tudo preenchido (inclusive a emenda da proposta com as
     três mudanças) → só o texto mudado → recarga → envio: substituto com as cinco respostas, as outras quatro
     idênticas byte a byte no JSON, `substitui` certo, UUID diferente.
  2. Leitor: fechamento único `fecharLeitor` (Esc via `prenderFoco`, X e navegação): solta o foco preso, esvazia,
     muda `location.hash` para `#/cartas` (rota relida, grade redesenhada) e devolve o foco à carta na grade
     reconstruída (`focoPendente` + rAF). Como o redesenho que abre o leitor devolvia o foco à grade pela chave, o
     leitor o prende de novo num `setTimeout(0)`. Verificado: abrir → foco no X; Esc → `#/cartas`, leitor vazio,
     foco na carta; redesenho não reabre; reabrir a mesma carta funciona; X → foco na carta; voltar/avançar no
     histórico abre e fecha.
  3. Glossário: cada par `dt`/`dd` num `div.termo-par` dentro do `dl` (cartão próprio). Verificado: 19 pares, dd
     sempre abaixo do próprio dt no mesmo bloco.
  4. Decisão da carta mestra é `button.com-dica` (Tab alcança; dica por foco, hover e clique), com `data-foco`.
  5. Códigos: `projeto.codigos` passou pelo núcleo (subagente; 105 testes) e o `projeto.json` real tem Q e R;
     verificado na tela Rumo: 8 códigos marcados (R88, Q10, Q2, Q8, Q13, Q4, Q3, R1), `aria-label` em palavras,
     dica por foco. Capturas refeitas em `conferencia/marco6-rumo-*`.
  6. Fontes externas nas cartas antigas (mapeamento, síntese, roteamento, busca desenho novo): baixadas uma vez
     (latin e latin-ext, OFL) e embutidas em `data:` num CSS local (`<pasta>/fontes/<carta>.css`, 300–440 KiB);
     por URL não funciona: o iframe isolado tem origem opaca e o CORS barra o woff2 (`net::ERR_FAILED`, medido).
     Verificado sem rede (tudo fora de 127.0.0.1 abortado): zero pedidos externos ao abrir Cartas e rolar, e as
     quatro cartas renderizam com as próprias famílias (Fraunces, Bricolage Grotesque, Barlow, Archivo…).
     Contrato publicado na §3.7 (Cartas).
- **Marcos 1–2, segunda correção (subagente, sessão 2, 2026-10-14), a devolver em revisão dirigida.**
  (1) `.tmp` da caixa: `caixa.conferir_pasta_tmp` exige que `caixa/.tmp` resolva exatamente para a `.tmp` da caixa
  real; é chamada antes do `makedirs` no arranque (recusa sem tocar no alvo externo), em `escrever_atomico` (com
  `caixa_real`, confere também o destino) e no passo 1 de `reconciliar` (recusada → problema, pula limpeza e
  gravações); item de `.tmp/` que é link nunca é apagado e vira problema; `Projeto.relativo` nomeia atalhos por onde
  estão (o alvo externo não vaza para `/api/estado`). (2) Retrato: `leitores.validar_proposta` (regras da §4.1 numa
  função, células escalares; usada também na leitura da rodada, que agora fica malformada com célula lista/objeto),
  `_validar_retrato_da_rodada` reescrita (tipos, ids únicos, opções, recomendada, proposta só no tipo proposta) e
  `_validar_respostas_da_mensagem` (forma por tipo de pergunta); JSON fora da forma é rejeitado inteiro. 14 testes
  novos (symlink e junction criados, nada pulado; sentinela conferida intacta). Rodado pelo construtor: 101 testes do
  núcleo OK (eram 87), 4 do projeto real OK, grep de neutralidade vazio. Contratos publicados na §3.7.

## Respostas do maestro para o cartas.json (2026-10-14, a gravar no marco 6)

Situação de cada carta (vigente = o desenho de hoje; histórica = serviu a rodada que o desenho já superou), dono e
decisão, nas palavras do maestro:

1. `prototipos/prototipo-08-divergencia.html` (ticket 08): **histórica**. As garantias continuam, mas o mecanismo
   (git) foi trocado por CouchDB + LiveSync na "Revisão do sync e da divergência com o banco" (ticket 33).
2. `prototipos/prototipo-09-busca.html` (ticket 09): **histórica** (rodada 1, markdown-vault-mcp contra zvec-grep).
3. `prototipos/prototipo-09-busca-desenho-novo.html` (ticket 09): **histórica**. Serviu à rodada 4; a pesquisa ampla
   trocou as candidatas para obsidian-hybrid-search contra memtomem.
4. `prototipos/prototipo-09-roteamento-da-pesquisa.html`: **histórica**; dono o ticket 09. Serviu à rodada 6 do 09,
   que desenhou o laço; o laço rodou nos tickets 49, 52 e 50, já resolvidos.
5. `prototipos/prototipo-10-contrato.html` (ticket 10): **vigente** (ticket resolvido, sem revisão posterior).
6. `prototipos/prototipo-12-pastas.html` (ticket 12): **histórica**. A rodada 1 do 12 não funcionou para o Gustavo e
   virou a pesquisa "Métodos de organizar a raiz" (35); o ticket 12 segue aberto, sem página nova.
7. `laco/painel/index.html` ("maré de novos") e `laco/painel/etapas.html` ("o garimpo"): **históricas** (painéis ao
   vivo da pesquisa ampla, ticket 50, já resolvida). `laco/painel/sintese.html` ("Super Trunfo da busca", v3):
   **vigente**, é a síntese da pesquisa 50. As v1 (laudo) e v2 (mapa do hub) ficaram no scratchpad do Designer
   anterior; se o arquivo não for achado, registrar só que foram recusadas.
8. `mapeamento.html`: propósito = as rodadas de mapeamento que fixaram o destino (os cinco critérios) e a fronteira do
   mapa. Serviu a = criação do mapa (`mapeamento.md`, rodadas Q1 a Q17). **Vigente** como registro de origem; o
   destino não mudou (a fronteira ganhou itens fora de escopo depois, como o segundo mapa sobre o hub controlar os
   agentes). Sem ticket dono (`ticket: null`).
9. `system-design.html`: propósito = "o desenho do hub de bater o olho; serve ao mapa inteiro e só muda quando um
   ticket que mexe no desenho é resolvido"; `ticket: null`; `decisao`: usar o mesmo texto.

Datas já levantadas (`data.tipo: "modificado"`, a torre lê do arquivo): system-design 2026-10-13, mapeamento
2026-10-12, prot. 08 2026-10-02, 09-busca 2026-10-04, 09-desenho-novo 2026-10-13, 09-roteamento 2026-10-13,
10 2026-10-03, 12 2026-10-10, painel index/etapas/sintese 2026-10-13. `pasta`: `.scratch/context-hub` para o
system-design e o mapeamento; `.scratch/context-hub/prototipos` para os protótipos; `.scratch/context-hub/laco/painel`
para o painel. Decisão a que serviu: para 08, 10, 33, 49, 50, 52 usar o resumo da decisão do mapa (está em
`/api/estado` → `decisoes`); para 09 e 12 (sem decisão) usar o texto do maestro acima.

## Problemas abertos

- **Marcos 1–2 (dados), duas pendências do Prumo (revisão dirigida de 2026-10-14): CORRIGIDAS (ver "Revisões");
  falta só devolver em revisão dirigida, junto com `projeto.codigos`.** Texto original das pendências:
  1. BLOQUEIA: `caixa/.tmp/` com symlink para fora da caixa: o arranque apagou o arquivo sentinela externo e não anotou
     problema. Validar (realpath + commonpath) todo caminho interno da caixa antes de criar, escrever ou limpar; um
     item de `.tmp/` que aponte para fora não é apagado e vira problema.
  2. IMPORTANTE: retrato JSON de resposta com `proposta.colunas = [[]]` passa pela validação, entra no índice, mas não
     gera `.md` (`unhashable list`). Validar os elementos internos (colunas são strings; linhas são dicts com id
     string; valores escalares) e rejeitar o JSON inteiro como mensagem inválida.
  Parecer e evidências: `C:/Projetos/context-hub/.maestri/roles/d4ce63fd-ce3e-45b5-88f6-6bbd68695030/revisao-dirigida124/parecer.md`.
- **Marcos 1–2, 3, 4, 5 e 6: APROVADOS pelo Prumo** (1–2 e 5–6 na revisão dirigida de 2026-10-14, parecer em
  `C:/Projetos/context-hub/.maestri/roles/d4ce63fd-ce3e-45b5-88f6-6bbd68695030/revisao-dirigida1256/parecer.md`;
  ele reproduziu as duas pendências de dados, os seis achados, 105 + 4 testes, neutralidade, capturas próprias).
- Marco 7 em construção: `aviso.py` + `iniciar.cmd` + testes com `maestri` falso (subagente de dados); terminal
  "Portal" e testes da §4.3 com o maestro (construtor). Marcos 7–8 e o canal de aviso ainda NÃO aprovados.
- Canal de aviso ao maestro: não verificado (marco 7).

## Decisões de detalhe da trilha de dados (relatório do subagente, marcos 1–2)

- O teste do marco 1 roda `Caixa.reconciliar()` (arranque) antes de comparar com `estado-esperado.json`: o
  `aviso: "pendente"` do `.json` órfão só existe depois da reconciliação (há um segundo teste mostrando que o
  leitor puro só difere nesse campo).
- Frontmatter: linha em branco dentro do bloco é tolerada.
- Rodada também fica `malformada` com `estado` fora de {aberta, suspensa, absorvida}, `recomendada` apontando
  para opção inexistente, `escolha`/`varias` sem opções, ou sem perguntas.
- POST: chave desconhecida no corpo ou numa resposta → 400 `chave-desconhecida`; rodada inexistente → 409
  `rodada-mudou`; rodada malformada → 400 `rodada-malformada`; Content-Type errado → 403 `tipo-de-conteudo`.
- Comentário sozinho numa pergunta conta como respondida; "outra" sozinha também.
- `corpo_hash` e `corpo` gravados são do corpo sem `envio` (inclui `substitui` quando vem); a idempotência compara o
  valor JSON canônico (`sort_keys`), não os bytes. O `.json` traz `alvo.titulo` a mais, para o `.md` nascer só do `.json`.
- Reconciliação, passo 5: `falhou` não volta a `pendente` sozinho (senão o "falhou visível" sumiria a cada
  30 s); só ausente ou `enviando` viram `pendente`. `.md` sem `.json` não entra na fila.
- `POST /api/aviso/tentar` num aviso que não está `falhou` responde 200 com o registro como está.
- Respostas de erro sempre trazem `campo` (`null` quando não há); `arquivo` nas respostas é o nome sem extensão;
  itens da `fila` em `/api/aviso` trazem `arquivo`. `/api/estado` junta aos `problemas` as falhas de I/O da caixa.
- HTTP/1.1 com keep-alive (`Content-Length` sempre; `Connection: close` nos 403/413 antes de ler o corpo).
- Ponto de ligação do marco 7: `servidor.torre.caixa.fila` (`caixa.Fila`): `pendentes()`,
  `marcar(envio, "enviando" | "entregue" | "pendente" (erro, proximo) | "falhou" (erro))`; `caixa.nome_de(envio)`,
  `caixa.dados_de(nome)`; `Fila.tentar_de_novo` já atende `POST /api/aviso/tentar`; modelo de thread em
  `Torre.iniciar_reparo()`.

## Próximo passo exato

**Marco 7, testes reais do canal A (2026-10-14, a partir de 16:58; "pode subir" do Gustavo pelo maestro).**
- Passo 1: torre 8770 fora do canvas (PID 35592, subida às 14:03 por um Bash meu) derrubada às 16:57. O maestro ligou o
  terminal "Portal" ao Designer (a ligação com ele continua).
- Passo 2, **maestro parado: PASSOU com dois defeitos, corrigidos.** `.\iniciar.cmd` (o Portal é PowerShell) às
  16:58:49; "aviso ao agente: disponível (modo canvas…)". O emissor mandou o `ask` do envio
  `022e4d3f-110b-4b5a-a40a-c86f241bd117` às 16:58:50; o maestro recebeu, absorveu no ticket 53 e pôs o `.md` em
  `estado: lida`. Defeitos vistos pelo maestro e por mim:
  1. **'(enviar)' solto no prompt do maestro.** A conferência do texto preso procurava os 40 primeiros caracteres na
     tela inteira do `check`; a mensagem entregue fica no histórico, então sempre parecia presa → Enter + "(enviar)"
     em toda entrega. Correção: `aviso.texto_no_prompt` olha só a caixa de digitação (entre as duas últimas réguas
     `─` do Claude Code; sem réguas, as 6 últimas linhas). O `maestri` falso do `teste_aviso.py` agora devolve a tela
     com a mensagem no histórico, como a real (o teste de entrega normal exige só `ask` + `check`), e há teste novo
     `test_mensagem_entregue_no_historico_nao_e_texto_preso`.
  2. **Fila mostrando `pendente` (tentativas 1, sem erro) com o aviso já entregue.** O `ask` bloqueia até o agente
     ficar ocioso; o reparo de 30 s (`Caixa.reconciliar`, passo 5) devolvia `enviando` → `pendente` no meio do `ask`
     (gravou às 16:59:20). Só virou `entregue` quando o '(enviar)' voltou (~17:05). Risco: estado falso na tela e o
     vigia do canal B poderia tomar o aviso (duplicado). O emissor em si não duplicaria (trava `lock_envio`).
     Correção: `reconciliar(arranque=True)` só no construtor da `Caixa`; o reparo periódico e o do POST não mexem em
     `enviando`. Teste novo `teste_caixa.test_reparo_periodico_nao_desfaz_enviando`; o de arranque continua.
  Suíte do núcleo: 122 OK em três rodadas (eram 120); numa rodada anterior, logo depois da edição, apareceu 1 erro
  que não guardei e não se repetiu em três rodadas seguidas (anotar ao Prumo como possível teste intermitente).
  4 testes do projeto real OK, 0 problemas. Portal reiniciado às ~17:08 com a correção (Ctrl+C, "S", `.\iniciar.cmd`);
  fila: 022e4d3f `entregue`. O registro no ticket 53 é do maestro (eu não edito tickets).
- Passo 3, **maestro ocupado: PASSOU.** Corpo certo do POST: `texto` no nível de cima (não `corpo.texto`; o 1º POST
  levou 400 `chave-desconhecida`, nada gravado). Envio `07ac8751-fd3b-4db4-87db-60c43bbde0b0` às 17:07:56; o Claude Code
  enfileirou o aviso no turno longo (17:07:43–17:11:48) e o maestro absorveu durante o turno. Ficou `enviando` (não
  mais `pendente` falso) até 17:12:42: o `ask` só voltou quando o maestro ficou ocioso depois do turno seguinte. Nenhum
  '(enviar)' solto. Proteção nova, por causa disso: se o `ask` esgotasse os 30 min depois da entrega, a nova
  tentativa repetiria o aviso; agora `Emissor.ciclo` marca `entregue` sem `ask` todo pendente cujo `.md` já está
  `estado: lida` (como o vigia do canal B já fazia). Teste `test_pendente_ja_lido_vira_entregue_sem_ask`; 123 OK;
  projeto real OK; portal reiniciado às ~17:13.
- Passo 4, **duas em 5 s: PASSOU.** `6216072e-c797-4e1c-9f8e-eb989ba7f776` (17:14:25) e
  `13f63156-93e0-4ac8-81a9-80e8a4356d9c` (17:14:28). A primeira saiu num `ask`; a segunda esperou a trava do emissor
  como `pendente`. O maestro absorveu as duas pela caixa ao receber o primeiro aviso; quando o `ask` voltou, a
  13f63156 já estava `lida` e virou `entregue` com 0 tentativas, sem segundo aviso (17:14:59). **É o previsto**
  (proteção acima), não defeito: nenhuma perdida, nenhuma absorvida duas vezes.
- Passo 5, **reinício: PASSOU.** `c127aa8a-cdbb-4f7d-ac05-d41a636a95d4` às 17:15:08.969 e Ctrl+C às 17:15:09.590. O
  emissor já tinha lançado o `ask` (PID 41716), que sobreviveu órfão à queda do servidor e entregou o aviso; foi isso
  que chegou ao maestro com a API fora do ar (subida às 17:15:31). No arranque, `enviando` → `pendente` e, como o `.md`
  já estava `lida`, → `entregue` sem reenvio. Obs.: o "Deseja finalizar o arquivo em lotes (S/N)?" do `.cmd` pede um
  "S" depois do Ctrl+C.
- Passo 6, **nome errado: PASSOU.** `aviso.agente` = "Ninguem Aqui" (cópia do original em `%TEMP%`), reinício,
  `67c287e4-ef70-43e6-ac04-04c53cf57a73` às 17:16:17 → `pendente`, tentativas 1, `ultimo_erro` "ask terminou com
  código 1: maestri: Terminal 'Ninguem Aqui' not found", `proximo` +1 min. A tela (Início, Para responder) mostrou
  "Gravado na caixa. o aviso ao maestro ainda não saiu; até lá, diga 'respondi'" (`conferencia/marco7-nome-errado-*`);
  o motivo do erro só aparece na API, não na tela (anotado ao Prumo). Nome devolvido, reinício, `POST
  /api/aviso/tentar` às 17:17:18 → tentativa 2 → `entregue` às 17:17:46; o maestro recebeu e absorveu. A escada
  1/5/15 min até `falhou` fica provada pelos testes unitários com hora controlada.
- **Fecho (2026-10-14, 17:18): canal A aprovado nos cinco testes, do lado do maestro também ("nada perdido, nada
  absorvido duas vezes"); nenhum '(enviar)' solto depois da correção.** Sobre a 13f63156 com 0 tentativas: previsto,
  é a proteção "pendente já `lida` vira `entregue` sem `ask`". Feito: proposta §4.3 (como o canal A ficou), §5.2
  (PowerShell, Ctrl+C + "S") e §9 (canal escolhido, data); `CANAL_DE_AVISO_VERIFICADO = true` em `web/torre.js`
  (faixa "diga 'respondi'" some no canvas; continua fora dele), capturas `conferencia/marco7-canal-verificado-*`.
  Portal no ar no terminal "Portal" (8770). Enviado ao Prumo.
- **MARCO 7 APROVADO pelo Prumo (2026-10-14, `portal/revisao-marco7.md`)**, sem bloqueantes nem importantes. Limites
  registrados por ele: tempo esgotado e escada completa só nos testes controlados; erro isolado da suíte não reproduzido
  (causa não verificada); motivo detalhado do erro só na API. Aceite devolvido ao maestro.
- Pendências depois do marco 7, feitas em 2026-10-14 (~17:30), enviadas ao Prumo:
  1. **"aguardando você" cortado no canto:** a classe genérica `.vazio` (estado vazio das listas, `padding: 10px 0`,
     declarada depois) zerava o recheio lateral do selo quando o contador está em 0. O estado do selo virou
     `.contador.zerado` (`web/torre.js` e `torre.css`), e o "0" ganhou recheio e canto. Captura 2x conferida.
  2. **`proposta.md` alinhada ao visual v2:** §1 virou "Mesa de mapas (visual v2)" (cores, fontes, faixa de leitura)
     e §2 tem os nomes Início/Tickets/Responder/Designs/Decisões, com a forma do Início "O caminho até o destino";
     §3.1 com as fontes novas; cabeçalho diz o que foi alinhado.
- **Marco 8 (2026-10-14, ~17:40–18:10), em revisão final pelo Prumo.**
  - §6: capturas do portal real em `conferencia/marco8/` (Início, Tickets, Quem espera quem, gaveta do 09 e do 16 pela
    rota `?ticket=`, Responder, rodada real dos cinco tipos já respondida, Designs, leitor do System design,
    Decisões; 1600×900 e 1280×800, mais página inteira), `prancha-1280.png`; zero erros de JS, fonte mínima 14 px,
    sem rolagem horizontal. A rodada ABERTA com os cinco tipos está nas capturas da fixture
    (`conferencia/visual-v2/fixture/`).
  - §8: auditoria por subagente, item a item, com prova (teste ou registro): 123 + 4 testes OK; 15 itens cobertos.
    Os parciais foram fechados no navegador com `conferencia/marco8/prova_aceite.js` e `prova_mapa.js` (cópia da
    fixture na 8772, servidor já derrubado) e `prova_codigos.js` (real, só leitura), resultados em `prova_*.json`:
    mudança no mapa aparece em Decisões em 1,1 s e na rodada em 0,8 s; Markdown com `<script>`, `onerror` e link
    externo sai limpo (nenhum script, nenhum `onerror`, link `_blank` com `noopener noreferrer`); iframe de carta com
    `sandbox="allow-scripts"`, a carta não lê `/api/estado` (TypeError) nem o portal (SecurityError).
  - Códigos internos: a varredura achou S3, S1, O1 e C1 soltos nos resumos de decisão. Fatos do maestro → `projeto.json`
    `codigos` ganhou S, O e C, e o R foi corrigido (é a pergunta numerada das rodadas de decisão, não resposta da
    estratégia). Portal reiniciado; agora só sobram "Q1 a Q17" no System design, já explicado em palavras ("rodadas de
    perguntas"), e BM25, que é nome de técnica.
  - Proposta §7: construtor = Claude Opus 5.5, esforço alto. Pendências do marco 7 (selo e proposta) entram nesta
    revisão.
  - Paralelo: carta visual da rodada r8 do ticket 12, feita por subagente (`prototipos/` + `cartas.json`); o id vai
    ao maestro.
  - Dúvida do Prumo na revisão final: o R1 dos tickets 25 e 30 é a correção "ramo de conflito" da pesquisa 26 (linha
    108), não pergunta de decisão. Sem mexer no núcleo: o verbete R do `projeto.json` diz os dois sentidos; portal
    reiniciado, 4 testes reais OK.
- **MARCO 8 E REVISÃO FINAL DO PORTAL APROVADOS pelo Prumo (2026-10-14, `portal/revisao-final.md`)**, sem bloqueantes
  nem importantes; ficam os limites do canal A já registrados. Aceite final devolvido ao maestro.
- Carta da rodada 8 do ticket 12: `prototipo-12-miolo` (`prototipos/prototipo-12-miolo.html`, em `cartas.json`,
  conferência em `conferencia/carta-ticket12/`); id e pontos interpretados (sem pasta `spikes`, esqueleto B sem nomes,
  destinos inferidos, Scripts/Tests da voegol) mandados ao maestro. A rodada 8 já estava absorvida.
- **Pedido novo (2026-10-14, ~18:20): dois defeitos relatados pelo Gustavo** (texto no fim de
  `caixa/2026-10-14-173842-resposta-*-65ca59e5*.md`): (1) rodada reescrita pelo maestro depois da resposta continua
  "entregue" (certo: sha256 atual ≠ `base` da última resposta → volta a esperar, entra no "aguardando você"); (2) a
  tela "se reinicia" enquanto ele digita (redesenho a cada mudança de arquivo). Com um subagente (brief: corrigir,
  testes no núcleo, prova no navegador em `conferencia/correcao-rodada/`, cópia da fixture na 8773). **Próximo:**
  revisar o relatório e o diff, rodar as suítes, mandar ao Prumo, avisar o maestro.
  **Feito pelo subagente (2026-10-14, ~19h), conferido:** (1) `leitores.ligar_respostas` comparava só a existência de
  resposta; agora `respondida` exige `base` da resposta mais nova = `base` atual e rodada `aberta`; Responder mostra
  MUDOU, aviso, formulário da versão nova e "Sua resposta à versão anterior" com "Copiar para o formulário"; envio com
  `base` novo e `substitui`. (2) `vigiarVersao` → `carregarEstado` → `renderizarTela` (`main.replaceChildren`)
  recriava a tela a cada mudança de arquivo; `trocarPreservando` mantém os nós `data-preservar` (formulário, rodapé
  de ações, corpo da gaveta, miniatura). Arquivos: `leitores.py`, `teste_torre.py` (classe `RodadaReescrita`, 4
  testes), `web/torre.js`, `telas/autorizacoes.js`, `telas/cartas.js`, `torre.css`. Conferido por mim: 127 + 4 OK;
  `conferencia/correcao-rodada/prova_correcao.json` `tudo_ok`; captura da rodada reaberta vista. Portal real
  reiniciado. Contrato na §3.7 da proposta. Achado à parte, não corrigido: gravar na caixa falha (500
  `FileNotFoundError`) se o caminho da pasta do projeto passa de 260 caracteres no Windows. **APROVADAS pelo Prumo
  (`portal/revisao-correcao-rodada.md`)**, devolvidas ao maestro; o caminho > 260 fica como pendência separada.
- **Entregues pelos subagentes e conferidos por mim (2026-10-14, ~20h); EM REVISÃO PELO PRUMO, num pedido só:**
  1. **Regra "carta substituída"**: `leitores.calcular_substituicoes` (estado ganha `substitui`, `substitui_titulo`,
     `substituida_por`, `substituida_por_titulo`, `situacao_efetiva`), `telas/cartas.js` (selo "substituída",
     ligações), `torre.css`, `teste_leitores.Substituicao` (8 testes), `estado-esperado.json`, `fixtures/LEIA.md`,
     `nucleo/LEIA.md`. 135 + 4 OK; portal real reiniciado; provas em `conferencia/carta-substituida/` (cópia e
     `real-*`). Regra na proposta §2.4 e §3.7. `cartas.json` real: miolo histórica; blocos substitui miolo; ritmos
     substitui blocos.
  2. **Carta da rodada 11**: `prototipo-12-ritmos` (`prototipos/prototipo-12-ritmos.html`), conferência em
     `conferencia/carta-ticket12-r11/`; id já com o maestro.
  3. **Amostra do System design** "planta técnica em papel vegetal": `.scratch/context-hub/amostras/system-design-planta.html`;
     conferência em `conferencia/system-design-amostra/` (paridade 124/124 textos, 0 faltando; interação OK em file e
     iframe sandbox nos dois tamanhos; fonte mínima 14,1 px em 1280 e 15,9 em 1600). O `system-design.html` atual NÃO
     foi tocado.
  **Achado do Prumo, corrigido (~18:20):** as duas páginas novas puxavam CSS/fontes do jsDelivr. Agora as fontes vão
  embutidas em base64 (`@font-face` com `data:`, subconjunto latin, mesmas famílias e versões: fontsource-variable 5.3.0
  em ritmos; fontsource 5.2.6 em planta); só as linhas 7–9/7–10 mudaram (diff conferido; CRLF da planta mantido). Prova
  com a rede bloqueada em `conferencia/fontes-locais/` (file: das duas e planta no iframe sandbox; todas as faces
  `loaded`). As cartas `miolo` e `blocos` (históricas/substituídas) ainda usam jsDelivr: não tocadas, dito ao Prumo.
  **APROVADAS pelo Prumo (`portal/revisao-tres-entregas.md`, ~18:25):** regra "carta substituída" e carta
  `prototipo-12-ritmos`; amostra do System design aprovada para apresentar ao Gustavo (não substituir o vigente antes
  do aval dele). Devolvido ao maestro. A pedido do maestro, a amostra virou carta própria no `cartas.json`
  (`system-design-planta`, vigente, sem ticket, sem `substitui`) para o Gustavo usar Aprovar/Recusar no leitor; no ar
  no portal real (captura `conferencia/fontes-locais/portal-carta-planta-1600x900.png`). **Próximo:** esperar o aval;
  com aval, copiar a amostra por cima do `system-design.html` e decidir com o maestro o destino da carta-amostra.
- **Planta RECUSADA pelo Gustavo (2026-10-14 19:08, `caixa/...-190808-aprovacao-carta-system-design-planta-*`):
  "só mudou o estilo". Pedido novo pelo maestro: reimaginar como cidade 2.5D vista de cima.** Brief em
  `amostras/system-design-cidade-brief.md` (com a seção "Ajustes do Prumo", parecer de direção em
  `portal/revisao-direcao-cidade.md`). Subagente construindo `amostras/system-design-cidade.html`, provas em
  `conferencia/system-design-cidade/`. **Ao terminar:** olhar as capturas; `cartas.json`: `system-design-planta` →
  `situacao: historica` e decisão "recusada pelo Gustavo em 2026-10-14: só mudou o estilo"; cadastrar
  `system-design-cidade` como carta-amostra (vigente, sem ticket, sem `substitui`); Prumo; avisar o maestro.
  **Feito (~21h):** cidade entregue e polida (Busca junto do canteiro, nomes de bairro dentro do chão, quadro de
  regras com folga); 124/124, 28 componentes, 30 arestas, interação OK em file e iframe, mínimo 14,4 px; Outfit
  5.2.8 embutida. `cartas.json`: planta histórica ("recusada pelo Gustavo"), cidade cadastrada. **APROVADA PELO
  PRUMO para mostrar ao Gustavo** (`portal/revisao-amostra-cidade.md`), devolvida ao maestro. **Próximo:** esperar o
  aval do Gustavo na carta `system-design-cidade`; com aval, copiar por cima do `system-design.html`, conferir no
  portal e em `file:`, e combinar com o maestro o destino da carta-amostra.
- **Pedido novo (2026-10-14 ~20h30; texto em `pedido.md`, seção final): página "Laços" (loops em voo) abaixo de
  Decisões. SÓ A CARTA-PROPOSTA.** Subagente construindo `amostras/portal-lacos-proposta.html` (provas em
  `conferencia/portal-lacos-proposta/`): maquete no idioma Mesa de mapas, fluxo de nós estilo n8n com os laços de
  `laco/` e `laco-embeddings/` (ticket 54) e uma suíte; camadas ligado / vira pedido (envio novo na caixa) / só
  desenho. **APROVADA pelo Prumo para mostrar ao Gustavo** (`portal/revisao-lacos-proposta.md`; direção em
  `revisao-direcao-lacos.md`), cadastrada como `portal-lacos-proposta`, devolvida ao maestro. Correções do Prumo:
  maquete marcada "retrato de 14/10 às 20h14, não atual"; Teto "proposto · sem aprovação"; bloco "A confirmar";
  teto gravado depois = 600 tentativas ou 2 h.
- **Laços: CONSTRUÇÃO LIBERADA (2026-10-14 ~21h30, rodada do ticket 55):** passo B (ver + pedir botões, parada,
  pausa), nome "Laços", suítes depois; a mais: opções por nó (harness, modelo…) e comentário por nó e por laço,
  como pedidos pela caixa. Plano em `portal/lacos-brief.md` (marcos L1 contrato → L2 núcleo → L3 tela; Prumo por
  marco). **L1 em curso por subagente** (edita só `proposta.md`: tela, contrato do `laco.json`, envio
  `alteracao-laco` na §4, endpoints, anexo com os dois exemplos). Ao terminar: conferir o diff, Prumo, e passar o
  formato ao maestro (ele escreve os `laco.json` reais de `laco/` e `laco-embeddings/`). Depois: L2 e L3.
  **Estado (~22h30):** L1 escrito; Prumo NÃO aprovou (`portal/revisao-lacos-L1.md`, 5 importantes: revisão cobre
  definição/precondições como teto.inicio; configurado ≠ em uso; retomada file-first de `lida`/`aguarda` e conferir
  UUID antes de aplicar; recibos tipados + regras gerais + `substitui`; "espera você" só rodada não respondida e
  conflito atual). Respostas de fato do maestro (faixas, ids `embeddings-2026-10-14`/`ampla-2026-10-13` atribuídos,
  nenhum recruta, modelo só no despachante via `excluir_manual`, tipo `lista`, "esperando cota" no contrato, 7.382
  tentativas) e os 5 achados do Prumo foram mandados ao subagente do L1 (retomado). **Feito (~23h):** correção
  aplicada (configurado × em_uso, precondicoes, estado `aplicando`, recibo tipado, `substitui` restrito, "espera
  você" corrigido; ressalvas no anexo: recrutas no ticket 50, `pools_aptos` suposição, `fora_agora` inclui pausas
  curtas). **L1 APROVADO pelo Prumo** (topo de `revisao-lacos-L1.md`); duas ressalvas de redação consolidadas
  (comentários lidos fora da fila de trabalho; `aplicado` com efeito "aguarda" ainda pede confirmação). Formato e
  ressalvas passados ao maestro (ele escreve `portal/lacos.json` e os `laco.json` reais). **L2 EM CURSO por
  subagente** (núcleo: leitor, rotas, envio validado, aviso/rede, fixture com dois laços, testes da §4.5; não toca
  caixa real, pastas dos laços, nem cria laco.json/lacos.json reais, não reinicia o portal). **Próximo:** conferir o
  relatório, rodar as suítes (núcleo + projeto real), mandar ao Prumo; com aval, abrir o L3 (tela) por subagente,
  no idioma Mesa de mapas, como a carta `portal-lacos-proposta`.
  **Sessão 3 (depois do `/clear`):** o maestro escreveu os reais (`laco-embeddings/laco.json`, `laco/laco.json`,
  `portal/lacos.json`, chave `"lacos": "lacos.json"` no `projeto.json`). Anexo A da `proposta.md` alinhado às
  ressalvas dele: a ampla teve recrutas na partida (Bússola, Faísca, Brasa, Centelha dispensados; Tear nos ambíguos),
  só no detalhe dos nós `chat` e `ambiguos`, sem controle; `pools_aptos` = fato, rótulo "pools do gateway com modelo
  apto"; `fora_agora` com pausas curtas aceito, aviso no detalhe do Despachante de embeddings. `terminou_em` de
  embeddings: o maestro preenche depois das 22h36. Subagente do L2 ainda rodando (lançado antes do `/clear`; a
  notificação chega a esta sessão). Ao chegar: conferir o diff, rodar as suítes (núcleo + projeto real, agora com
  os laços reais), mandar ao Prumo **junto com os dois itens abaixo**.
- **Carta do laço da construção (2026-10-15 ~21h; ticket 16, pedido do maestro): `.scratch/construcao-do-hub/
  laco-construcao.html`**, cadastrada como `laco-construcao` (`pede_veredito: true`, pasta `.scratch/construcao-do-hub`;
  o portal não serve o `.md` nem o `painel/`). Mapa de metrô no centro: as 3 fases em coluna (Spec, Tickets, Execução,
  com "2 Prumos revisam · você aprova" entre elas), os 12 recrutas como legenda de cores e a malha "todos ligados entre
  si" (`maestri connect`), o giro (maestro despacha → 7 trilhos de construtores → Prumo das decisões → Prumo da
  construção → testador → integrador → feito, com volta verde "destrava os próximos"), recusa em vermelho, 60 min →
  "maestro divide ou Fable", pesquisador e HOME de ensaio como ramais, "com você" embaixo, painel "só mostra". Depois
  as 2 perguntas da rodada na ordem (papéis; a 1 hora), A recomendada grande, B e C pequenas; a 3ª (conversas) saiu
  da rodada por pedido do maestro e virou fato do mapa. Fontes Barlow em `construcao-do-hub/fontes-carta/`. Prova
  `conferencia/carta-laco-construcao/` (leitor e sozinha, 1280 e 320, sem rolagem lateral, sem erro, nenhum POST); em
  320 o mapa rola dentro do quadro, com a dica.
  Logo depois o maestro a marcou `historica`, sem veredito: a resposta do Gustavo à rodada (21h08) mudou o desenho;
  o plano vigente é `.scratch/construcao-do-hub/planejamento/plano.md`.
- **Carta da amostra (2026-10-15 ~20h; ticket 56, `laco-system-design/carta/brief-designer-amostra.md`):
  `laco-system-design/amostra/carta.html`**, cadastrada como `amostra-da-cidade` (`pede_veredito: true`). Faixa de duas
  linhas (o que mudou, a pergunta, como navegar) e a amostra numa moldura de madeira com a altura visível da carta (o
  canvas se ajusta sozinho; sem redução). Fontes em `amostra/fontes-carta/` (a `amostra/fontes/` é do UI engineer, só
  scripts). Prova `conferencia/carta-amostra/` com mouse de verdade no leitor e sozinha, 1280 e 320: arrasto com o
  botão direito, Ctrl + roda (75% → 178%), Shift + roda e clique na ficha funcionam; o portal não rola nem amplia.
  No leitor a 1280 × 800 a amostra abre a 75% (o quadro de 557 px não dá a cidade inteira com nome ≥ 13 px; regra da
  própria amostra); "Ver tudo" mostra tudo. Na prova, cada tamanho abre página nova (a ficha aberta passava adiante).
- **Carta do esboço da árvore final (2026-10-15 ~18h; ticket 12, `rascunhos/12-brief-esboco.md`):
  `prototipos/prototipo-12-arvore.html`**, cadastrada como `prototipo-12-arvore` (`pede_veredito: true`). Raiz (o
  `AGENTS.md` e seis raízes) → `clients/voegol/cross-tenant/` como planta (núcleo, blocos em uso, o que fica nesta
  máquina); leitor ao lado com a nota de exemplo, cada campo com selo "máquina · origem" ou "escreve"; o `status` comum
  aparece como "a conciliar" (rodada 19, do maestro), sem inventar a conciliação. Mecanismo em três passos no pé.
  Fontes em `prototipos/fontes/arvore.css`. `cartas.json` agora termina com CRLF (preservado). Prova
  `conferencia/carta-12-arvore/`.
- **Carta da mistura (2026-10-15 ~17h; ticket 56, `laco-system-design/carta/brief-designer-mistura.md`):
  `laco-system-design/conceitos/mistura/carta.html`**, cadastrada como `mistura-da-cidade` (`pede_veredito: true`). O
  `cartas.json` agora está com CRLF e indentação 2 sem quebra final (o maestro o regravou): inserir com
  `json.dumps(indent=2, ensure_ascii=False)` + CRLF. Topo com a decisão em dois ramos; as quatro mudanças pedidas
  como mini-desenhos nas cores da peça; convite a três cenários; a peça em 1280×1000 reduzida para caber (abaixo de
  900 px, a forma estreita da própria peça, com rolagem no quadro). Fontes em `mistura/fontes/`. Prova
  `conferencia/carta-mistura/` com a peça final do acabamento: cenário acionado dentro do leitor em 1280 e 320.
- **Carta da direção visual da cidade (2026-10-15 ~13h; ticket 56, laço do system design, pedido do maestro pelo
  `laco-system-design/carta/brief-designer.md`): `laco-system-design/conceitos/final/carta.html`**, cadastrada como
  `direcao-visual-cidade` (`pede_veredito: true`, vigente; a rodada é do maestro). Três pranchas iguais (sem
  favorito) como seletor e o conceito grande embaixo, com a ideia, como se lê e onde é melhor nas palavras dos
  juízes. Fontes embutidas em `fontes/carta.css` (origem opaca no leitor); no leitor a carta não mede o conceito,
  usa as alturas medidas em 1280 (888/888/930; a ficha abre fixa ao lado). Prova `conferencia/carta-direcao-cidade/`
  (sem rolagem lateral na carta em 1280 e 320; a rolagem lateral do leitor em 320 é da casca, igual com outra carta).
  Se o UI engineer mudar a altura de um conceito, atualizar `ALTURA` na carta.
- **L3 entregue pelo subagente (2026-10-15): `web/telas/lacos.js`, rota/menu e `api.lacos/laco` em `torre.js`,
  `#gaveta-no` no index, ícones, CSS, proposta §2.6 (7 decisões de tela; conflito de laço NÃO entra no contador do
  topo por causa da §3.4). Prova 27/27 em `conferencia/lacos-L3/prova.json`; real só leitura. Olhei: forma boa, mas
  legendas cortadas com reticências, hora em cada número, linhas coladas/cruzadas à direita, ticket repetido cortado
  na lista, Parada cortada em 1280 → devolvido ao subagente para limpeza. Depois: olhar de novo, suítes, Prumo.**
  Limpeza feita e conferida por mim (prova 31/31; 223 + 6 OK) e enviada ao Prumo. **Prumo (`revisao-lacos-L3.md`):
  decisões (a) contador sem conflito de laço e (b) substituição automática ACEITAS; L3 NÃO aprovado por uma quebra:
  depois de `400 substitui-invalido` (pedido substituído foi recusado), a tela não oferece retirar a referência e
  repete o 400.** Devolvido ao subagente: recuperação explícita (reler pedidos, enviar como novo com UUID novo,
  preservando valor/texto; não mexer no retry de rede; parada/pausa/retomada também) + dica do contador zerado
  "nenhuma rodada ou carta espera você". Próximo: conferir, suítes, revisão dirigida ao Prumo, maestro.
  **Feito e conferido (captura `subst-B-400-recuperacao` vista; prova `substituicao` 12/12; principal 31/31; 223 + 6
  OK). **L3 APROVADO pelo Prumo (topo de `revisao-lacos-L3.md`); página Laços entregue ao maestro.** Antes, com o aceite: avisar o maestro que a página Laços está no ar (é só
  recarregar o portal; arquivos estáticos) e que o System design pausado pode voltar quando ele pedir.
  Falha que ele viu em `test_erro_vira_pendente…` era minha: o `maestri` falso gravava a mensagem na tela no ask que
  falha; com o falso lento (> `PASSO_OLHAR`), o `check` achava prova falsa. Falso corrigido (ask com erro não grava);
  teste passa com `PASSO_OLHAR` 0,05; `teste_aviso` 22 OK.
- **Defeito do aviso (relatado pelo maestro, 2026-10-14 ~23h45): a resposta f67ac890 (23h36) não foi avisada.**
  Causa verificada: `_entregar` esperava o `ask` voltar (só volta com o maestro ocioso; o das 23h32, PID 63596, durou
  mais de 10 min) segurando `lock_envio`; a f67ac890 ficou `pendente` com 0 tentativas atrás da trava, e a proteção
  "lida vira entregue" também ficava travada. Repetiu-se às 23h46 com o comentário e4d38fa5. Correção em
  `nucleo/aviso.py`: `_ask_com_prova` (Popen com saída em arquivo temporário; a cada `PASSO_OLHAR` 2 s procura prova:
  todos os `.md` lidos, ou, por `OLHAR_TELA_POR` 120 s, `prova_na_tela` = começo do UUID de cada envio fora da caixa
  de digitação, sem espaços); com prova, `entregue` e a vez passa; o `ask` segue em `_acompanhar` até voltar ou até
  `TIMEOUT_ASK`, quando é encerrado; sem prova, como antes. "(enviar)" usa o mesmo caminho. Testes:
  `teste_aviso.EntregaSemEsperarOAsk` (4; o principal falha com a prova desligada: 30,7 s presos, o incidente); o
  `maestri` falso não mostra no histórico o texto preso. 222 OK duas vezes, 6 do projeto real OK. Proposta §4.3 e
  LEIA. Portal real reiniciado às 23h56 (e4d38fa5 já lida → `entregue` sem reenvio; fila vazia). Ressalva do Prumo
  (órfão: a thread que encerra nos 30 min morre com o servidor): `Emissor.parar()` encerra os `ask` já provados
  (teste `test_parada_normal_encerra_os_asks_ja_provados`); proposta §4.3 e LEIA declaram o limite e o procedimento
  para encerrar só os remanescentes próprios depois de queda abrupta. 223 + 6 OK. **APROVADO pelo Prumo
  (`portal/revisao-aviso-sem-espera.md`)**; portal real reiniciado de novo (2026-10-15, logo após 00h), fila vazia.
- **L2 APROVADO pelo Prumo na revisão dirigida (topo de `revisao-lacos-L2.md`; 218 + 6 OK; contrato §4.5–§4.6).
  Portal real reiniciado às 23h10 com o núcleo L2 (fila vazia antes; Ctrl+C, "S", `.\iniciar.cmd`): `/api/lacos` com
  os dois laços reais terminados, 0 problemas. L3 (tela) EM CURSO por subagente (brief na mensagem de lançamento:
  `telas/lacos.js` + CSS, fixture curta na 8775, provas em `conferencia/lacos-L3/`, captura só leitura do real).
  Próximo: conferir capturas e relatório, suítes, Prumo, maestro.**
- **L2 entregue e conferido (206 + 6 OK, 3×; `_trocar` com novas tentativas no `os.replace`, causa do erro
  intermitente). Relatório em `portal/lacos-L2-relatorio.md`. Prumo (`portal/revisao-lacos-L2.md`): contador de
  cartas e cidade v2 APROVADOS; L2 NÃO aprovado por 3 achados (painel na raiz do laço serve `config.json`; id não
  string → 500 em `/api/lacos`; `definicao_mudou: false` falso). Subagente do L2 (`af5136482cff463ac`) retomado
  para corrigir só os três + registrar as decisões na proposta. Próximo: conferir, suítes, revisão dirigida ao
  Prumo. Portal real AINDA NÃO reiniciado (havia aviso `enviando` às 22h45); reiniciar quando a fila esvaziar.**
- **Cidade v2 RECUSADA pelo Gustavo (envio 81bd19a5, 22h01): "tudo poluído, não dá pra bater o olho e entender;
  precisa de distância entre os itens".** System design PAUSADO até a página Laços ficar pronta; depois, um laço
  próprio o recria (totalmente diferente, mesma ideia de cidade e analogia de papéis; um agente forte em system
  design/diagramas e outro em UI/UX). NÃO começar antes do maestro pedir. Feito: `cartas.json` cidade-v2 →
  `situacao: historica`, decisão com a frase. Feito também (a levar ao Prumo com o L2): **contador "aguardando você"
  conta as cartas com `pede_veredito: true`** (vigente, não mestra, sem `aprovacao` não substituída na caixa):
  `app.cartasAguardando` e casca em `web/torre.js` (dica diz quais cartas; só cartas → link para a carta), "Para
  responder" do Início com "Ver e decidir", selo "espera Aprovar ou Recusar" na grade e na tira do leitor
  (`telas/cartas.js`); proposta §2 (selo) e §3.2 (`pede_veredito`). Prova em `conferencia/cartas-aguardando/`
  (`prova.json`: 2 → 1 depois do POST de aprovação, selo some, zero erros de JS). Nenhuma carta real tem a chave
  hoje: cadastrar `pede_veredito: true` nas próximas amostras. Limite: a regra não olha a data; uma carta que mude
  depois de aprovada não volta a contar (para pedir de novo, carta nova com `substitui`).
- **Cidade v2 (radial):** refeita depois da minha recusa interna (cofre fora do centro); agora CouchDB a 0,00% do
  centro, anéis no chão, 0 cruzamentos, 28/28 analogias. Cadastrada `system-design-cidade-v2` com `substitui:
  system-design-cidade` (v1 histórica). **APROVADA pelo Prumo** (`portal/revisao-amostra-cidade-v2.md`; duas frases
  de analogia corrigidas: porteiro "preserva a base_rev e separa versões em conflito, sem sobrescrever"; terminal
  "esta porta oferece só consulta"). Devolvida ao maestro. **Próximo:** aval do Gustavo; com aval, copiar a v2 por
  cima do `system-design.html` e conferir no portal e em `file:`.
- **Cidade recusada como "piloto bom" (2026-10-14 20h33, `caixa/...-203331-aprovacao-carta-system-design-cidade-*`):**
  manter o estilo; disposição radial com o CouchDB no centro (níveis pelo grafo), vista mais de cima, rótulos
  colados, analogia como eixo com "Na cidade: … — porque …" na ficha. Brief na seção "# v2" de
  `amostras/system-design-cidade-brief.md`. Subagente da v1 retomado, construindo `amostras/system-design-cidade-v2.html`
  (provas em `conferencia/system-design-cidade-v2/`). **Ao terminar:** olhar; cadastrar `system-design-cidade-v2` com
  `substitui: system-design-cidade` (v1 fica histórica; decisão da v1: "piloto bom, pediu ajustes"); Prumo; maestro.
- **Carta da rodada 12 do ticket 12: `prototipo-12-sumario` APROVADA pelo Prumo** (`portal/revisao-carta-r12.md`),
  cadastrada com `substitui: prototipo-12-ritmos`, ligada à rodada pelo maestro; corrigido 57→56 (prints de
  `repasse/anexos/prints`). Devolvida ao maestro.
  (Texto antigo:) esperar o parecer do Prumo (chega como mensagem do Prumo neste terminal); corrigir só o
  que ele bloquear; então avisar o maestro: regra + carta aprovadas; amostra aprovada pelo Prumo e pronta para o
  Gustavo ver em `amostras/system-design-planta.html` (substituir o `system-design.html` só com o aval do Gustavo,
  copiando a amostra por cima e conferindo no portal e no `file:`). Pendências conhecidas: faixa branca de ~90 px
  embaixo da carta no leitor do portal (aparece em todas as cartas, nas capturas headless; investigar); gravar na
  caixa falha com caminho > 260 caracteres.
- Em paralelo, cada um com um subagente: (a) carta da rodada 10 do ticket 12 (núcleo + formas A/B/C com SOC STRATA,
  context-hub e VOEGOL; B como peças que se encaixam; nada de `_archive/`/README) → id ao maestro;
  (b) amostra da forma nova do System design (pedido do Gustavo em `caixa/2026-10-14-175212-comentario-carta-system-design-*`):
  mesmo conteúdo, planta técnica em papel vegetal, canvas sem rolagem (direito arrasta, Ctrl+roda zoom, Shift+roda
  horizontal), só os cards clicáveis; amostra em `.scratch/context-hub/amostras/system-design-planta.html`,
  conferência em `conferencia/system-design-amostra/`. Fluxo: olhar → Prumo → maestro; só substituir o
  `system-design.html` com o aval.

**Marco visual v2 APROVADO pelo Prumo (2026-10-14, revisão dirigida só dos três achados; parecer em
`portal/revisao-visual-v2.md`).**

**Visual v2, revisão do Prumo (`portal/revisao-visual-v2.md`): linguagem aprovada, três achados; corrigidos e
devolvidos em revisão dirigida (2026-10-14, ~18h).** Pedido do maestro: fechar rápido, solução simples.
(1) `telas/torre.js`: `espera`/`libera` (sem a volta do ciclo, só o plano) servem só para ordenar e desenhar; rótulo
"espera N"/"pode partir", nota, aria, placa e próximo passo usam `bloqueios_abertos` + `bloqueios_inexistentes` da
API (fixture: 05 "espera 1 · ticket 99, que não existe"; 07 "espera 2" com 03 e 06; cópia sem o 03: 07 "espera 1"
pelo 06; próximo passo não libera o 05). (2) e (3): **toda dica vai para a faixa de leitura `#leitura`**, uma linha
própria da casca (grid `barra leitura`, entre a faixa de aviso e a tela), fora da área que rola, em todas as telas,
altura fixa 72 px; nenhuma dica flutua mais (posicionador removido). Esc dispensa sem mover o foco; o Início troca o
texto de repouso com `repousoDaFaixa`. Verificado: 120 + 4 testes OK; `conferencia/visual-v2/verifica_prumo_v2.js`
(achados 1 e 2) e `verifica_v2.js` OK; capturas refeitas em `conferencia/visual-v2/`. **Próximo:** esperar a
conferência do Prumo; com aceite, avisar o maestro; marco 7 segue segurado; sugestão pendente do Prumo: alinhar
`proposta.md` ao visual v2 (tema, fontes, nomes das telas, forma do Início).

**Marco "visual v2" (2026-10-14, ~17h, sessão 3): aplicado nas cinco telas, em revisão pelo Prumo.** Aval do Gustavo:
"pode aplicar nas cinco telas" (fim do `pedido.md`), mais o pedido do maestro: a dica do hover não pode tapar o cartão
vizinho. Feito (cópias do tema noite em `…/448a6830…/scratchpad/{torre-noite.css,torre-noite.js,telas-noite/}`):
- Fontes do núcleo trocadas por Nunito Sans, Fraunces e JetBrains Mono (@fontsource-variable 5.3.0, conferidas por hash;
  `vendor/VERSOES.md`, licenças OFL; Big Shoulders e IBM Plex removidas; `teste_torre.py` aponta a fonte nova).
- `torre.css`: tokens remapeados para o papel (os nomes antigos ficam: ambar = terracota/espera você, ciano =
  petróleo, verde = musgo, coral = tijolo, cinza = pedra), caixa alta espaçada removida, piso de 14 px, barra de
  madeira, topo, botões, gaveta, diálogos, Tickets (sem plaquetas escuras; título em Fraunces), Quem espera quem (nós
  maiores, rola na horizontal em vez de encolher), Decisões (radar → "No horizonte" sobre papel, ecos numerados com a
  lista ao lado), Designs e Responder (cores e títulos).
- Menu: Início, Tickets, Responder, Designs, Decisões (rotas `#/torre`, `#/partidas`… iguais); ícones novos; avião
  virou etiqueta; títulos de seção em palavras (Todos os tickets, Quem espera quem, No horizonte, Fora do mapa,
  Diário de bordo, Legenda do mapa, Carta mestra…).
- `telas/torre.js` reescrita: a faixa "O caminho até o destino" da amostra v3, gerada da API (camadas do
  `plano_de_voo` → colunas Agora/Em seguida/Depois/Por fim; linhas pela média de quem bloqueia; à margem = sem
  bloqueio aberto e sem dependente; últimos sem dependente → fio "fecha" ao cartucho; ciclo → volta pontilhada em
  tijolo + aviso; `bloqueios_inexistentes` → "depende de N, que não existe"; destaques = 3 resolvidos com mais
  `bloqueia`), Para responder (rodadas abertas, malformadas, última da caixa com o estado do aviso, próximo passo) e
  Últimas decisões.
- Dica: na faixa do Início a leitura vai para uma **nota de leitura** fixa acima do mapa (`data-doca-dica`), que
  nunca cobre cartão; nas outras telas a dica flutuante procura a posição de menor sobreposição com `[data-obstaculo]`,
  dá para entrar nela com o ponteiro, Esc a dispensa sem mover o foco, e rolar só a reposiciona (o foco por teclado
  rolava e apagava a dica).
- Verificado: 120 testes do núcleo + projeto real OK; `verifica_v2.js` (normal e reduced-motion): realce sem
  opacidade, nota por hover e foco, Esc com placa e com lacre, redesenho preserva a escolha, roving, gaveta pela
  placa, dica do horizonte; capturas `conferencia/visual-v2/` (cinco telas + Quem espera quem + leitor, 1600 e 1280,
  tela e página inteira; fixture em `visual-v2/fixture/`: Início com ciclo e dependência quebrada, rodada aberta,
  gaveta). Torre da fixture no ar na 8771 (cópia em `…/448a6830…/scratchpad/horta-v2`).

**Ponto de retomada (2026-10-14, ~15:40, sessão 3, Opus 5.5):** o Gustavo aprovou clima, paleta e tipografia da v2 e
RECUSOU a trilha até o cume (fim do `pedido.md`). Feita a **amostra v3** em `v2/amostra-inicio.html` (a recusada ficou em
`v2/amostra-inicio-trilha-recusada.html`): faixa de largura total "O caminho até o destino" = índice de folhas a tinta
(43 resolvidos + 51 riscado, contagem por tipo) | linha de tinta | marcos a lápis em colunas = camadas do `plano_de_voo`
(Agora, Em seguida, Depois, Por fim), fios sólidos de quem bloqueia para quem espera, 09 "estamos aqui", 32 e 53 "à
margem" | cartucho do destino com os cinco critérios em lacres tracejados e fio "verifica" do 17. Hover/foco acende a
corrente inteira (inclusive os quadrados ancestrais); clique fixa e abre a placa. "Tickets de relance" saiu. Capturas
`conferencia/amostra-v3-*.png`; medição em `conferencia/{mede.js,verifica.js}`. Prumo (`portal/revisao-amostra-v3.md`):
primeira revisão pediu três correções, todas feitas: realce sem opacidade (corrente em borda terracota; folhas não
relacionadas em tinta clara #d3e2ca, 7,26:1; animação `assentar` em fill-mode backwards); dica que se entra com o
ponteiro e que Esc dispensa sem mover foco nem reabrir; textos só afirmam "verificação/aceite final pendente". Sugestão
atendida: "Os que mais abriram caminho" (3 resolvidos com mais `bloqueia`: 25, 22, 34) no lugar da contagem por tipo.
**AMOSTRA V3 APROVADA pelo Prumo (2026-10-14)**, aceite só da amostra. Devolvida ao maestro para o Gustavo. Só aplicar
nas cinco telas depois do aval do Gustavo. Marco 7 continua SEGURADO até o maestro dizer "pode subir".

**Ponto de retomada anterior (2026-10-14, ~15:10; o construtor passou de 45% do contexto e pediu `/clear` ao maestro):**
- Amostra `v2/amostra-inicio.html` APROVADA pelo Prumo e entregue ao maestro, que mostra ao Gustavo (resposta
  dele pendente; chega pelo maestro). Só aplicar a v2 nas cinco telas depois do aceite do Gustavo
  e do parecer do Prumo; o que mudar na amostra por causa deles, mudar antes de aplicar.
- Marco 7: o maestro pediu para SEGURAR o passo 1 (subir o servidor no terminal "Portal") até ele dizer "pode subir"
  (ele ia receber `/clear` e voltar ocioso para o teste "parado"). A sequência completa está abaixo. A torre 8770
  fora do canvas ainda está no ar (derrubar no passo 1). O subagente de dados terminou; relançar um novo só se os
  testes reais pedirem mudança no núcleo.
- Servidor da amostra: `python -m http.server 8765` na pasta `v2` pode estar no ar (descartável).


1. Marco 7, trilha de dados (subagente): `nucleo/aviso.py` (canal A: thread emissora no servidor com `maestri ask`,
   junta pendentes, marca entregue/pendente/falhou com as esperas 1, 5, 15 min; canal B: `--vigiar <pasta>` que
   imprime uma linha por pendente e marca entregue), `iniciar.cmd`, modo canvas/fora do canvas, testes com um
   `maestri` falso. Quando chegar: rodar as suítes, anotar aqui.
2. Marco 7, construtor: pedir ao maestro o terminal "Portal" no canvas (ligado ao "Claude Code") e combinar os
   momentos dos testes da §4.3 (parado, ocupado, duas em 5 s, reinício, erro); rodar os testes do canal A primeiro,
   registrar cada um aqui; se A falhar, B. Registrar o canal escolhido na §9 e aqui, com a data; só então
   `CANAL_DE_AVISO_VERIFICADO = true` em `torre.js`. Entregar ao Prumo por `maestri ask "Prumo"`.
3. Marco 8: conferência final (§6), testes de aceite (§8), revisão final do Prumo, entrega ao maestro.

**Sequência dos testes reais do marco 7 (canal A), combinada com o maestro em 2026-10-14.** Terminal "Portal" (shell,
pasta do portal, ligado ao "Claude Code") já existe; rodada real de teste `rodadas/2026-10-14-teste-do-canal-de-aviso-r1.md`
(ticket 53, criado só para isso, fora do mapa) já foi respondida (14:30, envio `022e4d3f…`, `estado: nova`, aviso
`pendente`). Passos do construtor:
1. Derrubar a torre 8770 que roda fora do canvas (`netstat -ano | grep :8770`, `taskkill //F //PID`).
2. `maestri ask "Portal" --raw "iniciar.cmd
"`; `maestri check "Portal"` precisa mostrar "aviso ao agente: disponível
   (modo canvas…)". O emissor encontra o aviso pendente de 14:30 e manda o `ask` ao "Claude Code": é o teste
   **parado** se o maestro estiver ocioso (combinar antes). Conferir `GET /api/aviso` (`entregue`), `maestri check
   "Claude Code"` (sem texto preso) e o `.md` virando `estado: lida` com o UUID citado no ticket 53.
3. **Ocupado**: o maestro inicia um turno longo (ele escolhe como); o construtor grava um comentário no ticket 53
   via `POST /api/caixa` com `curl` (cabeçalhos `X-Torre: 1`, `Origin: http://127.0.0.1:8770`, `Content-Type:
   application/json`; corpo `{"envio": <uuid4>, "tipo": "comentario", "alvo": {"tipo": "ticket", "id": "53"},
   "corpo": {"texto": "teste ocupado"}}`); passa se chega depois do turno (ou durante, sem se perder) e é absorvido.
4. **Duas em 5 s**: dois `POST` com 2 s de intervalo; um `ask` com as duas ou dois `ask`; nenhuma perdida, nenhuma
   absorvida duas vezes (o maestro confere os UUIDs no ticket).
5. **Reinício**: `POST` e, no mesmo instante, `Ctrl+C` no terminal Portal (`maestri ask "Portal" --raw ""`),
   subir de novo com `iniciar.cmd`; o aviso sai depois de subir (pode repetir: o maestro não absorve duas vezes).
6. **Nome errado**: trocar `aviso.agente` no `projeto.json` para um nome inexistente, reiniciar, `POST`; `GET
   /api/aviso` mostra `pendente` com `ultimo_erro` em palavras e a tela mostra o aviso; devolver o nome, "tentar de
   novo" pela API/tela → entregue. A escada completa 1/5/15 min → `falhou` fica provada pelos testes unitários com
   hora controlada (anotar isso ao Prumo).
7. Registrar cada resultado aqui com hora e UUID; se todos passarem, canal A na §9 e aqui com a data; publicar na
   proposta os textos do subagente (§4.3, §3.5/§3.7, §5.2); `CANAL_DE_AVISO_VERIFICADO = true` em `torre.js`; se A
   falhar em algum, canal B (`python nucleo/aviso.py --vigiar <pasta>` na ferramenta Monitor do maestro) com os mesmos
   testes mais a expiração/rearme de 30 min.

Se esta sessão for limpa no meio do marco 7 (contexto do construtor passou de 40% em 2026-10-14 ~14:30):
- O subagente de dados estava construindo o item 1 (brief: §4.3 + §5.2 + §3.5 + "Ponto de ligação do marco 7";
  canal A com conferência do texto preso via `check` e `--raw "
"`; canal B `--vigiar`; `iniciar.cmd`; testes
  com `maestri` falso em `nucleo/testes/teste_aviso.py`; LEIA.md). Conferir se `nucleo/aviso.py` e
  `nucleo/testes/teste_aviso.py` existem e se a suíte passa; se faltar algo, relançar um subagente com esse brief.
- O maestro recebeu em 2026-10-14 o pedido do terminal "Portal" (`maestri recruit "Portal" --preset "Shell" --dir
  <pasta do portal>`) e de uma rodada real com os cinco tipos em `rodadas/` para os testes da §4.3; esperar a
  resposta dele (chega como mensagem neste terminal) antes de rodar os testes reais.
- Torres no ar: 8770 (real) e 8771 (fixture em `…/Temp/horta-dev`); reiniciar a 8770 depois que `aviso.py` entrar
  em `torre.py`.
3. Torres no ar: real 8770 e fixture 8771 (cópia limpa em `C:/Users/gustavo.delfino/AppData/Local/Temp/horta-dev`,
   com as duas respostas da prova da correção na caixa).

Ferramentas desta sessão no scratchpad `…/508110a4-c16d-4946-ab1e-01b8bf68cea6/scratchpad`: `cap.sh` (cópia; perfil
silenciado; `--virtual-time-budget=9000`), `mede_marco6.js`, `mede_miniaturas.js`, `patch_marco6b.py`,
`patch_marco6c.py`; `node_modules` com puppeteer-core continua no scratchpad antigo
(`…/944115a4-ff54-4e1d-889a-fca9b69c2cd0/scratchpad`, usar `NODE_PATH`).

Ferramentas de verificação que ficaram no scratchpad do construtor (podem ter sumido; são descartáveis):
`servir_fixture.py` (servidor de desenvolvimento), `cap.sh`, `verifica_marco3.js`, `verifica_marco4.js`,
`verifica_marco4b.js`, `verifica_marco5.js`, `verifica_foco_gaveta.js` (puppeteer-core 23.11.1 + msedge
`--remote-debugging-port`). Os servidores das portas 8770/8771/8779 podem estar no ar: matar pela porta
(`netstat -ano | grep :8771`, `taskkill //F //PID`).

## Canal de aviso

**Canal A, desde 2026-10-14** (§9 da proposta): `maestri ask` a partir do servidor no terminal "Portal". Registro dos
testes no "Próximo passo exato" (marco 7).
