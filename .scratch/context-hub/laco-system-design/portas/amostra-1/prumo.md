# Parecer do Prumo — porta da amostra, volta 1

2026-10-15. Peça: `amostra/amostra.html`. Revisão de código, sem editar a peça.

**Recomendação: volta.** Três bloqueios: ativação por toque, transição da pinça para um dedo e o comando “Ver tudo” em tela estreita.

## Escopo e evidência

Li o brief da porta, o brief da amostra, `amostra.md`, `decisoes.md`, o parecer do Tech lead e o relatório do QA. As referências de linhas abaixo são de `amostra/amostra.html` nesta volta. Inspecionei HTML, CSS, dados embutidos e JavaScript. Não executei testes, navegador, provas ou varreduras adicionais. Resultados de execução citados são do QA; as falhas abaixo são deduções do código, não reproduções em aparelho.

Não reavalio R1 a R6 nem a fidelidade do conteúdo: esses julgamentos pertencem aos outros pareceres.

## Bloqueios

### 1. A captura incondicional do toque impede a ativação dos alvos internos

**Linhas 219–222, 233–234 e 282–285.** Todo `pointerdown` de toque que chega à `.tela` executa `tela.setPointerCapture(ev.pointerId)`, mesmo sem arrastar. O `pointerup` passa a ter a tela como alvo; o clique resultante também é destinado ao elemento capturador. Os tratadores que abrem ficha estão nos bairros e pessoas, descendentes da tela: um clique na tela não passa por eles. O mesmo problema alcança os botões de zoom, que também estão dentro dela (linha 190).

Consequência: tocar numa ficha ou em “Aproximar” pode não ativar o controle, embora o arrasto funcione. A leitura do QA deixou exatamente essa modalidade sem teste. Fonte primária: [Pointer Events, destino de click/auxclick/contextmenu](https://www.w3.org/TR/pointerevents3/#the-click-auxclick-and-contextmenu-events), que mantém o alvo capturador mesmo depois de `lostpointercapture`.

**Conserto recomendado:** preservar o alvo do toque simples; assumir captura para arrasto apenas após distinguir o gesto, e excluir os botões HTML da manipulação do canvas. Suprimir a ativação depois de um arrasto de forma vinculada ao gesto, sem depender apenas de um `setTimeout(0)`.

### 2. Ao retirar um dedo da pinça, o próximo movimento salta

**Linhas 222–232.** O segundo `pointerdown` substitui `arr.x/y` pelas coordenadas desse dedo. Durante a pinça, a função atualiza `toques`, faz zoom e retorna sem atualizar `arr.x/y`. Quando um dedo sai, `solta()` conserva `arr` enquanto houver outro toque. O movimento seguinte do dedo restante calcula `dx/dy` contra aquelas coordenadas antigas, que podem ser do outro dedo: aplica um deslocamento grande sem o usuário tê-lo feito.

**Conserto recomendado:** ao mudar a quantidade de dedos, reconstruir a referência do gesto a partir do toque restante; separar o estado do arrasto do estado da pinça. Tratar cancelamento e perda de captura com a mesma limpeza. O salto decorre da sequência de atribuições; comportamento em dispositivo real permanece **não verificado**.

### 3. “Ver tudo” não mostra tudo em telas estreitas

**Linhas 202–205, 237 e 240.** O botão e a tecla `0` chamam `ajustar()`. Quando `caber()` retorna menos que `.6`, essa função força `.75` e centraliza no Banco local, repetindo o enquadramento inicial parcial. Exemplo deduzido: com 320 px de largura, `(320−20)/1200 = .25`; a função escolhe `.75`, expondo cerca de 427 das 1200 unidades horizontais. Logo, não enquadra a cidade inteira.

Isso contradiz `amostra.md`, item 2, que promete que “Ver tudo” mostra a cidade inteira. O QA comparou `0` à vista inicial e não clicou no botão; essa equivalência não verifica a promessa.

**Conserto recomendado:** separar a abertura legível em 75% do enquadramento completo solicitado pelo botão/tecla. O enquadramento completo pode precisar ficar abaixo do limite de zoom manual de 35%; resolver essa relação explicitamente, preservando a possibilidade de aproximar depois.

## Acessibilidade no código

Há boa base: `lang="pt-BR"`, botões HTML, nomes nos bairros e pessoas, `tabindex="0"` sem índices positivos, Enter/Espaço para abrir ficha, Esc para fechar, devolução de foco, foco visível previsto no CSS e anúncio dos passos por `aria-live`. Deslocamento e zoom têm alternativas pelo teclado. O QA confirmou parte desses comportamentos; Tab real e leitor de tela não foram executados nesta revisão.

**Recomendação 4, sem bloqueio adicional nesta volta:** rever `role="img"` no SVG interativo (linha 186). Esse papel descreve uma imagem única e tem descendentes apresentacionais na definição ARIA, enquanto o SVG contém os botões dos bairros e pessoas. Não presumir que contar paradas de Tab garante sua exposição a tecnologia assistiva. Recomendo um contêiner sem semântica de imagem atômica, com nome, preservando os controles e escondendo apenas decoração. Fonte: [WAI-ARIA 1.2, img](https://www.w3.org/TR/wai-aria-1.2/#img). O efeito concreto em cada combinação navegador/leitor está **não verificado**.

As etiquetas (linhas 258–264) não são controles focáveis; o teclado abre a ficha completa pelo bairro. Isso preserva acesso ao conteúdo, mas não a seleção direta do componente prometida pelo clique. Se essa seleção for necessária também pelo teclado, recomendo oferecê-la na ficha ou em controles irmãos, evitando botões aninhados no bairro.

A ficha é um `aside` não modal (linha 192), não um diálogo: não considero ausência de contenção de foco uma falha isolada. Em 320 px ela cobre toda a largura, mas o Tab ainda alcança o fundo. Recomendo tornar explícita a interação desejada: se bloquear visualmente o fundo, adotar diálogo modal com foco contido e fundo inerte; se permanecer não modal, garantir retorno compreensível entre ficha e desenho. Fonte para a semântica atual: [APG, complementary landmark](https://www.w3.org/WAI/ARIA/apg/patterns/landmarks/examples/complementary.html).

## Eventos, estrutura e dependências

- Roda: tratador `passive:false`, `preventDefault`, zoom ancorado no ponteiro, Shift para horizontal e roda simples para deslocamento; alinhado ao pedido e à evidência sintética do QA. `deltaMode=1` é convertido, mas `deltaMode=2` não (linha 214): recomendação menor de normalização, sem reprodução nesta revisão.
- Mouse: botão direito e meio entram no arrasto, esquerdo fica para fichas; menu de contexto barrado na tela. Não encontrei bloqueio adicional no caminho do mouse já exercitado pelo QA.
- Nada externo: HTML, CSS, SVG e dados embutidos, fontes de sistema; não há importação de biblioteca ou chamada de rede no código lido. O endereço do namespace SVG não é uma requisição de recurso. O QA também reporta ausência de rede externa.
- Montagem das fichas usa `textContent` e `createTextNode`, sem interpretar o conteúdo como HTML (linhas 267–278). Funções ficam numa IIFE; a separação conceitual entre vista, fichas e cenários existe, embora concentrada no mesmo script.

## Desempenho e atualização após ticket resolvido

**Recomendação 5, sem bloqueio atual: acusar etiquetas sem lugar.** Confirmo a observação do Tech lead: `if(!pos)` remove a etiqueta e apenas incrementa `sobra`; o único sinal final é `data-sobra` (linhas 260–265). As 40 atuais cabem segundo o QA, então não é perda atual de conteúdo; a ficha continua contendo o componente. Ao acrescentar ou renomear um componente, porém, a camada visual pode omiti-lo silenciosamente. Recomendo aviso explícito de edição/diagnóstico com bairro e nomes que sobraram, além de tornar essa condição um critério da próxima conferência do QA. Não basta registrar só o total.

O empacotamento percorre posições em passos de três unidades, comparando cada candidata a todos os obstáculos; as linhas viram muitos obstáculos a cada cinco unidades (251–260). Faz leituras geométricas e inserções DOM síncronas, inclusive para uma camada inicialmente escondida. O QA relata carga virtual de 215–315 ms contra 71 ms da mistura; isso não mede travamento em hardware real. Para 40 etiquetas, não há evidência suficiente de bloqueio de desempenho. Se crescer, recomendo pré-calcular posições na edição da peça ou limitar/indexar a procura; não repetir o empacotamento em cada zoom. Hoje ele roda uma vez, o que é positivo.

**Recomendação 6, sem bloqueio atual: tornar a edição local legível e documentada.** O SVG inteiro está na linha 189; `G`, `C` e cores ficam na linha 195. Atualizar um ticket pode exigir sincronizar ficha, nomes e títulos no SVG, ligações, metadados `data-cenario`/`data-chave` e referências dos passos em `C`. A geração das etiquetas a partir de `G` evita uma duplicação, mas o restante ainda depende de conferência manual. Recomendo formatar essas partes e acrescentar um roteiro curto de atualização, explicitando essas correspondências e o diagnóstico de sobra. Isso cabe no HTML único; não exige framework nem ferramenta de build.

## Consertos para a próxima volta

1. **Bloqueia:** preservar a ativação por toque de fichas e botões ao distinguir toque simples de arrasto; rever captura e supressão do clique.
2. **Bloqueia:** reiniciar a referência do gesto ao passar de dois dedos para um, evitando salto; limpar cancelamento/perda de captura.
3. **Bloqueia:** fazer botão “Ver tudo” e tecla `0` enquadrarem a cidade inteira também em 320 px, separando essa ação da abertura em 75%.
4. **Recomendado:** rever a semântica do SVG interativo e o acesso à ficha quando ela cobre a tela; conferir a exposição dos controles a tecnologia assistiva.
5. **Recomendado:** acusar nomes descartados pelo empacotamento, atendendo à observação do Tech lead.
6. **Recomendado:** formatar SVG/dados e documentar os pontos que mudam quando um ticket altera o desenho.

**volta**
