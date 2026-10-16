# Retomada do UI engineer (laço do system design)

Gravado em 2026-10-15, antes de um /clear; atualizado no fim da volta 2 da amostra. Serve para eu (UI engineer) retomar sem memória. Leia também o
`CLAUDE.md` do papel (regras do papel: pt-BR, frases curtas, gravar só em `conceitos/` e `amostra/`, Edge com perfil
próprio, dados de cliente só pelo nome da iniciativa, sem códigos internos soltos, avisar com
`maestri ask "Claude Code" "pronto: <caminho>"`).

## Onde estamos

- **Volta 3 (a última) da amostra entregue** (porta `portas/amostra-2/`): `amostra.html` novo, `amostra-v2.html` (volta 2),
  `consertos.md` seção "Volta 3" (com a correção do que a volta 2 afirmou sobre o arrasto de um dedo), decisões 20 a 22.
  Gerador: `fontes/build_amostra3.py` = `build_amostra2.py` + `fontes/patch_v3.py`. Regerar do zero, na pasta `amostra/`:
  `cp fontes/build_amostra.py fontes/build_amostra2.py && python -I fontes/patch_v2.py && python -I fontes/patch_v3.py && python -I fontes/build_amostra3.py .`
  Próximo, de outros: porta da volta 3; depois o Gustavo vê a amostra.
- **Volta 2 da amostra entregue** (consertos da porta `portas/amostra-1/`): `amostra.html` novo, `amostra-v1.html` (volta 1),
  `consertos.md` (linha a linha), `decisoes.md` (13 a 19), `amostra.md` (seção "Volta 2"). Gerador da volta 2:
  `fontes/build_amostra2.py` = `build_amostra.py` + `fontes/patch_v2.py` (que lê `fontes/nav_v2.js`). Para regerar do zero:
  `cp fontes/build_amostra.py fontes/build_amostra2.py && python -I fontes/patch_v2.py && python -I fontes/build_amostra2.py .`
  (na pasta `amostra/`; o patch não roda duas vezes sobre o mesmo arquivo). Próximo: porta da volta 2 (QA com entrada real).
- Fase 4 do `orquestracao.md`: a **amostra** (volta 1) foi entregue e voltou da porta. Próximo passo, de outros: QA testa, UX
  revisor e Tech lead revisam, um revisor de código revisa (até 3 voltas); depois o Gustavo vê. Eu espero a próxima
  tarefa (provavelmente consertos da porta da amostra, em `amostra/`).
- A **mistura** (`conceitos/mistura/`) está fechada: aprovada pelo Gustavo **sem alteração** (carta do Designer). Não
  mexer mais nela. O Gustavo tirou o **teto de 25 rótulos**; as outras regras da régua continuam.
- Os três conceitos antigos (A, B, C) estão em `conceitos/final/`; não mexer (a `carta.html` é do Designer).

## Onde está cada coisa

Raiz do laço: `C:\Projetos\context-hub\.scratch\context-hub\laco-system-design\`

| O quê | Caminho |
|---|---|
| Fonte do conteúdo (única) | `descricao/descricao-do-hub.md` (v3.2; marcas [D] [C] [P] [R7] [R8] [R11] [A] [G] [NV] [L]). Não ler `descricao/teste/` nem `descricao/perguntas/`. |
| Régua | `suite/skills/regua-da-cidade/` (`regras.md`, `como-julgar.md`, `referencias/`) |
| Amostra | `amostra/amostra.html`, `amostra.md` (o que mudou, como navegar, conferência), `decisoes.md` (12 decisões), `brief.md` |
| Mistura | `conceitos/mistura/mistura.html` (final), `mistura-v1.html` (volta 1), `mistura.md`, `decisoes.md` (itens 1 a 21), `consertos.md` (volta 2 e acabamento), briefs |
| Pareceres da mistura | `portas/mistura-1/` e `portas/mistura-2/` (tech-lead.md, ux-revisor.md, resultado.md) |
| QA oficial | `qa/` (não gravar lá) |

**Geradores e scripts de trabalho: `amostra/fontes/`** (25 arquivos, copiados do scratchpad da sessão antes do /clear).
- `build_amostra.py` → gera `amostra/amostra.html`: `python -I amostra/fontes/build_amostra.py <pasta amostra>`.
  Grava `amostra.html` direto na pasta dada; rode a partir de qualquer pasta.
- `build_mistura3.py` → gera `conceitos/mistura/mistura.html` (final, acabamento); `build_mistura2.py` = volta 2;
  `build_mistura.py` = volta 1. Não regerar a mistura (está aprovada).
- `build.py`, `build2.py`, `build3.py`, `build4.py` = conceitos A, B, C (voltas 1 a 3 e final); `patch*.py` e `docs3.py`
  = os patches que geraram essas versões (histórico).
- Conferência: `shot.mjs`, `cen-todos.mjs`, `tab-real-b.mjs` (e as variantes `tab-real.mjs`, `-a`, `-m`), `mouse.mjs`;
  `moldura-320-*.html` = molduras de 320 px com iframe (os caminhos dentro delas apontam para o scratchpad antigo:
  ajustar se usar).
- Os scripts `.mjs` recebem o perfil do Edge e a pasta de saída como argumentos: use uma pasta de saída fora de `qa/`
  (o scratchpad da sessão nova) e um perfil `edge-ui-engineer-<algo>` lá dentro.
O scratchpad antigo (`...\a90fe403-4cc9-43b0-a942-97589cde276e\scratchpad\`) pode não existir mais; as capturas e os
JSON de medida que ficaram lá não foram copiados (são refeitos com os scripts).

## A mistura (o que foi aprovado)

Planta da B (duas cidades e a estrada: a cidade do par dentro de uma muralha; o outro par em miniatura do outro lado
da rede privada) + o que veio da A: **a linha sai de quem aciona e tem a cor dele**.
- 9 bairros = os grupos de 5.1 (Núcleo de dados do par, Portas do par, Vigilância, Disciplina do agente, Conteúdo,
  Periferia do par, Interfaces do Gustavo, Ferramentas da máquina, Fora do par). Pessoas fora da muralha: Maestro,
  Agentes, Gustavo. Bolinha colorida = segundo grupo (Contrato em Conteúdo; Nota e Acervo em Disciplina; Obsidian em
  Periferia).
- Cores: agentes azul (buscar é a mais grossa; disco direto tracejado sobre amarelo = a decidir), Gustavo vermelho,
  maestro verde-azulado, regras roxo, agendador marrom, "confere, só lê" tracejado escuro (checkpoint → nota, vigia →
  banco), disco e banco pontilhado verde, troca entre pares ardósia. Porta do banco com contorno tracejado = a construir.
- 20 ligações visíveis + 3 só no cenário (Maestro → Biblioteca do Maestri; Maestro → Gustavo, o aval; Checkpoint →
  Agentes). Nenhuma cruza.
- Fichas por bairro: cada componente com Dono, Quem aciona, Quem lê, Só vê, Aprova, Também em, selos (a decidir, não
  verificado, a construir, em curso). Clique num componente abre a ficha nele.
- 7 cenários (8.1, 8.3, 8.4, 8.5, 8.6, 8.7, 8.8 da descrição), passo a passo, com número no desenho; passo de falha ou
  em aberto = triângulo vermelho e elementos vermelhos tracejados. Marcação `data-cenario="<id>:<n>"` + `data-chave`.
- Decisões que pesaram (detalhe em `conceitos/mistura/decisoes.md`): Gustavo → Obsidian → Vista Markdown (nunca direto
  ao banco); linha do plugin ao banco fora do desenho; dono só na ficha (é o Gustavo em quase tudo); Checkpoint →
  Agentes só no cenário (senão dois roxos colados ou cruzamento); aval sai do Maestro, não do Acervo; Claude Desktop sem
  marca no desenho (seria componente solto).

## A amostra (o que mudou da mistura)

1. **Canvas de tela inteira, sem rolagem**: `body` com 100dvh e `overflow:hidden`; topo (título, legenda em duas linhas,
   cenários + ajuda de navegação na mesma fileira) e `main#tela` (focável) com o SVG a 100%. O zoom e o arrasto mudam o
   **viewBox** (objeto `vb` no JS), não a página. `CONT={x:0,y:24,w:1200,h:852}` é o enquadramento de "Ver tudo".
2. Navegação: botão direito ou do meio arrasta; roda = vertical; Shift + roda = horizontal; Ctrl + roda = zoom no
   ponto do mouse; toque: 1 dedo arrasta, pinça dá zoom; teclado no `#tela`: setas, + − e 0. Botões − + "Ver tudo NN%" no
   canto **inferior esquerdo** (no direito passa a linha do maestro à biblioteca, no cenário). Foco (Tab) num bairro fora
   da vista leva a vista até ele; no cenário, a vista vai até o número do passo (`mostrar()`).
3. Vista inicial: enquadrada (93% a 1280 x 1000). Se o enquadramento dá menos de 60% (tela estreita), abre a 75%
   centrada no Banco local. `ResizeObserver` reajusta enquanto ninguém mexeu (`mexeu`).
4. Rótulos novos na vista inicial: "Agendador do Windows" (relógio) e "Biblioteca do Maestri" (caderno). 27 rótulos.
   "Configuração de cada ferramenta" virou etiqueta de detalhe.
5. **Camada de detalhe**: a partir de 140% de zoom (`svgC.classList.toggle('perto', px()>=1.4)`), 40 etiquetas
   (`g.etq` com `data-item`, dentro de `g.detalhe` de cada bairro) com os componentes que só estavam na ficha. O JS
   acha o lugar sozinho no carregamento: varre o retângulo do bairro e evita caixas de textos (margem 8 x 6), itens (6),
   linhas (meia espessura + 5) e miniatura/estrada/cofres. Bairro sem lugar ganha `data-sobra="n"` (hoje nenhum).
6. **Remapeamento vertical** (função `YM` e `mapear()` no gerador): fileira de cima +45 e de baixo +70 unidades para as
   etiquetas caberem. `YM`: y ≤ 230 fica; 230–240 estica até +45; até 700, +45; 700–730 estica até +115; ≥ 730, +115.
   Pós-processa `rect` (y e altura juntos), `text` y, `circle` cy, `line` y1/y2 e `path` d (M, L, Q, V absolutos).
   Elementos com `data-fixo="1"` não são remapeados (a miniatura do outro par, que já é calculada sobre a planta
   remapeada; a linha de troca; os nomes do Agendador, da Biblioteca e de "Interfaces do Gustavo" com o ⊕, postos em
   coordenadas finais). viewBox 0 0 1200 900.
7. O SVG tem `tabindex="-1" focusable="false"` (o Edge o tornava uma parada de Tab vazia).

## Como meço e confiro

Sempre perfil próprio do Edge e, no fim, matar só os msedge cujo comando tenha `edge-ui-engineer-`:
`Get-CimInstance Win32_Process -Filter "name='msedge.exe'" | Where-Object { $_.CommandLine -like '*edge-ui-engineer-*' } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force }`
(nunca taskkill por nome). Há um servidor `python -m http.server 8765` de outra sessão: não mexer.

1. **Medidas** (régua R1–R3, contraste, rolagem): `suite/skills/medidas-da-peca/rodar.ps1 -Raiz <pasta> -Peca amostra.html -Saida <scratchpad>\am-qa -Larguras 320,1280 -SemLinks`.
   Ler o JSON: `rotulos.textos_svg`, `distancias.menores_folgas`, `dentro_do_grupo_mediana_px`, `entre_grupos_minimo_px`.
   Só conta elementos visíveis (as linhas só do cenário e as etiquetas escondidas não entram).
2. **Tab real**: `tab-real-b.mjs <edge> <perfil> <saida> <html>` manda Tab pelo protocolo de depuração (26 paradas) e
   grava `tab-real.json` com tag, `:focus-visible` e estilo. Amostra: 23 paradas (7 cenários, `#tela`, 9 bairros, 3
   pessoas, 3 botões de zoom), todas com foco visível.
3. **Cenários**: `cen-todos.mjs <edge> <perfil> <saida> <html> 1280 1000` percorre os 7 cenários do primeiro ao último
   passo: conta marcas por passo, mede a distância do número atual ao que acende, aperta Esc e lê `aria-pressed` e a
   altura da página. Amostra: 39 passos, todos com número, distância máxima 16, `aria-pressed=false` nos 7, altura 1000.
4. **Capturas**: `shot.mjs <edge> <perfil> <html> <saida.png> <larg> <alt> [js]` com janela fixa pelo protocolo (é o
   jeito confiável; ver armadilhas). Para ver a camada de detalhe, o JS põe o viewBox direto e a classe `perto`.
5. **Mouse de verdade**: `mouse.mjs` manda arrasto com o botão direito, Ctrl + roda, Shift + roda e clique esquerdo
   por `Input.dispatchMouseEvent`; imprime o viewBox depois de cada um.

Números da amostra entregue: 27 rótulos, 20 ligações visíveis, 0 cruzamentos, folga mínima 22,3 px (rótulo 19 px),
razão entre grupos **1,53** (limite 1,5), contraste 58/58, sem rolagem a 320 e a 1280.

## O que não foi testado

- Toque num aparelho de verdade (arrastar com um dedo, pinça).
- Leitor de tela (os `aria-live` dos passos e o `aria-pressed` só foram lidos como atributo).
- Larguras 768 e 1920 a olho; 1280 x 720 na amostra (na mistura foi conferido).
- O texto dos passos contra a v3.2 é do Tech lead (ele passou a mistura; a amostra usa os mesmos passos).

## Riscos para a porta da amostra

- **Razão entre grupos 1,53, no limite.** O par mais perto é Porta do banco × Agentes (51 px). Subiu a mediana dentro
  dos grupos por causa das fileiras mais altas. Saída: afastar a coluna das pessoas para a esquerda ou aproximar itens
  dentro dos grupos.
- Vista inicial em 93% (a mistura abria perto de 100%): o texto ficou um pouco menor.
- O UX pode achar as etiquetas de detalhe pequenas (8,5 unidades; ~12 px no limiar de 140%) ou coladas em algum nome.
- A linha Maestro → Biblioteca contorna a cidade inteira (aceito na mistura; só aparece no cenário).

## Armadilhas que achei

- **Edge sem cabeça com `--screenshot` e `--virtual-time-budget`**: a janela é redimensionada depois do carregamento;
  o `ResizeObserver` refaz o enquadramento e desfaz um zoom de teste; e a medida inicial pode sair errada (84%). Use
  `shot.mjs` (janela fixa por `Emulation.setDeviceMetricsOverride`).
- `--screenshot` em série falha calado se ficou um msedge vivo com o mesmo perfil: matar os do perfil antes.
- A 320 px, o Edge sem cabeça não respeita `--window-size=320`: usar `shot.mjs` com largura 320 ou uma moldura com
  iframe de 320 px.
- Patches com `assert s.count(a)==1`: se um falha, nada é gravado (o script para antes de escrever). Conferir com grep
  depois; já perdi uma rodada achando que tinha aplicado.
- Heredoc longo no bash quebra ("unexpected EOF"): para script grande, gravar com Write e rodar.
- Em Python, chamar `c(rot, papel, selos, **quem)`: a lista de selos vem **antes** dos argumentos com nome.
- A medida de folga usa a caixa do grupo `g` do item: um retângulo de clique transparente aumentaria a caixa e
  derrubaria a folga. Por isso a área de clique é `pointer-events: bounding-box`.
- O número de passo procura lugar pela `data-chave` do elemento (a miniatura não tem `data-item`); a primeira chave de
  cada passo recebe o número.
- `getBBox` de elemento com `display:none` dá zeros: as etiquetas de detalhe são posicionadas no carregamento com a
  camada já no DOM; a busca de lugar dos números ignora as etiquetas escondidas.
- Rodada 8 do Gustavo (busca pelo Obsidian e pelo Desktop; recuperar pelo GitHub com até 2 dias; cliente pode ir aos
  modelos na nuvem) já está na v3.2 e na peça.

## Volta 2: o que mudou no código (para a volta 3)

- Navegação (`nav_v2.js`): `modo` ('abertura' | 'tudo' | null) no lugar de `mexeu`; `enquadrar()` desconta o canto do
  zoom só se ele cobrir item, bairro ou muralha (`CAIXAS`); `tudo()` = "Ver tudo"/`0`; `abertura()` = inteira se
  `e * ROT >= 13` (ROT = menor altura de caixa de texto, em unidades), se não 75% no Banco local; `minimo()` = min(35%,
  enquadramento). Toque: sem captura no aperto, captura só depois de 6 px; `ref()` refaz a referência pelo dedo que
  ficou; `solta()` serve `pointerup`, `pointercancel` e `lostpointercapture`; `suprimir` barra o clique de um arrasto até
  o próximo aperto. Botão direito/meio: `mousedown` e `pointerdown` cancelados (sem foco); `porTeclado` (Tab) libera o
  `mostrar()` do `focusin`; `scroll` da `.tela` volta a 0.
- Camada de detalhe: `colocar()` (passo de 1 unidade na vertical, 3 entre etiquetas) e `acusar()`; obstáculo de texto
  8 dos lados, 6 em cima, 10 embaixo. Pessoas: "Claude Desktop" e "Cliente" com `data-abre="gente"`.
- Linhas só do cenário: Checkpoint → Agentes `M340,185 H312 V238 H95 V355` (sobre o Contrato a partir de y 238);
  Maestro → Biblioteca `fixo` em coordenadas finais `M108,85 V16 H1197 V881 H655 V714 H582`.
- CSS: `.tela` sem seleção; `@media (max-width:1100px)` com legenda recolhida e cenários numa fileira; a 760 o
  cabeçalho volta a quebrar linha (senão o botão Legenda sai da tela a 320).
- Teste de navegação com entrada real: `teste-v2.mjs` (copiado para `fontes/teste-v2.mjs`; args: edge perfil html larg alt pasta-saída). Faz: três arrastos
  com o botão direito, botão do meio, arrasto esquerdo, `+` x3 no centro, `0`, toque no `+`, toque no Banco local,
  arrasto com um dedo, pinça e tirar um dedo. Toque com `Emulation.setTouchEmulationEnabled` + `Input.dispatchTouchEvent`;
  para tirar um dedo, mandar `touchMove` só com o que fica.
- Números da volta 2: iguais à volta 1 nas medidas (27 rótulos, 0 cruzamentos, folga 22,3 px, razão 1,53, contraste
  58/58), Tab 23, cenários 39; 42 etiquetas, nenhuma sobra. Abertura: 93% a 1280 x 1000, 72% inteira a 960 x 800,
  75% a 1280 x 720, 104% a 1920 x 1080, 75% a 320; "Ver tudo" a 320 = 25%.

## Volta 3: o que mudou e o que aprendi

- `patch_v3.py`: `lostpointercapture` só chama `solta()` se `ev.target===tela` (a perda no elemento tocado, quando a
  tela toma a captura, é transferência); `resize` com a ficha aberta refaz `fundo()` e leva o foco a "Fechar" se virou
  modal; `@media (max-height:800px)` recolhe a legenda; `.cen-botoes` ganha `mais-esq`/`mais-dir` (máscara de degradê)
  por JS no `scroll`/`resize`, e o botão focado rola para a vista.
- **Armadilha de teste (me enganou na volta 2):** no `Input.dispatchTouchEvent`, `touchMove` com menos dedos **não**
  solta nenhum; `touchEnd` lista o dedo que **sai** (e um `touchMove` com id já solto cria um dedo novo). E conferir
  o deslocamento obtido contra o pedido, número a número: 8 x 5 de 64 x 40 é falha, não sucesso.
- Scripts: `fontes/toque-alvos-ui.mjs` (roteiro do QA com perfil próprio; args: raiz-do-laço saída.json perfil),
  `fontes/extra-v3.mjs` (arrasto longo, pinça → um dedo, cancelamento, cabeçalhos, fileira, ficha ao redimensionar;
  args: edge perfil html pasta-saída), `fontes/teste-v2.mjs` (pinça corrigida).
- Números da volta 3: medidas iguais (27 rótulos, 0 cruzamentos, folga 22,3, razão 1,53, contraste 58/58), Tab 23,
  cenários 39. Cabeçalho: 185 px a 1280 x 1000, 139 a 1280 x 720, 106 a 960 x 800, 120 a 320 x 640.
