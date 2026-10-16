# Parecer do Prumo — porta da amostra, volta 2

2026-10-15. Peça: `amostra/amostra.html` (volta 2). **Recomendação: volta**, por uma regressão bloqueante no arrasto com um dedo.

## Escopo e evidência

Conferi os seis pedidos do meu parecer da volta 1 contra `amostra/consertos.md`, `amostra/decisoes.md` e o HTML atual. Li o brief desta porta, o relatório do QA da volta 2, `amostra.md`, o trecho de navegação em `fontes/nav_v2.js`, o roteiro no topo do HTML e a evidência já produzida em `qa/amostra-2/navegacao/toque-alvos.json`.

Não editei a peça e não executei testes, provas ou varreduras. Evidência de execução abaixo é do QA; as referências de linhas são do HTML desta volta. Depois dos pedidos anteriores, examinei apenas problemas introduzidos pelos consertos. Conteúdo aprovado e julgamento visual ficam com Tech lead e UX revisor.

## Conferência dos pedidos da volta 1

| Pedido | Situação e aceite | Evidência |
|---|---|---|
| 1. Toque simples ativa ficha e botão; captura só ao arrastar; suprimir clique do arrasto | **Feito; aceito para ativação.** Há regressão no arrasto, detalhada abaixo. | Linhas 1911–1928: exclui `.zoom`, não captura o primeiro toque no aperto e captura após o limiar. Linhas 1935–1938: marca de supressão sem temporizador, reiniciada no próximo aperto. QA: toque abre Banco local e ativa `+`; o toque seguinte ao arrasto abre ficha. |
| 2. Pinça → um dedo sem salto; limpeza no cancelamento/perda de captura | **Feito parcialmente; aceito o reinício da referência, não aceito o tratamento indiscriminado da perda de captura.** | `ref()` usa as coordenadas atuais do toque restante (1909, 1932–1933). QA: retirada sem salto, movimento seguinte de 2 px e mais oito movimentos corretos. Porém `lostpointercapture` de um descendente também termina o gesto (1936): bloqueio novo. |
| 3. “Ver tudo” e `0` enquadram tudo em 320 px | **Feito; aceito.** | `tudo()` separado de `abertura()`; mínimo manual considera o enquadramento completo (1881–1890). Botão e `0` chamam `tudo()` (1941, 1944). QA: enquadramento completo a 25%, sem itens sob botões, nos dois comandos. O texto de 5 px é o custo da visão geral; a abertura continua em 75%. Legibilidade/conforto são do UX. |
| 4. Semântica do SVG e ficha que cobre a tela | **Feito; aceito no escopo de código, com ressalva de redimensionamento abaixo.** | SVG com `role="group"` e nome (201). Ao abrir, a ficha vira diálogo com `aria-modal` e fundo `inert` se cobre a largura; fechar restaura o fundo e devolve foco (1994–1997). QA confirmou os estados em 320 e nas larguras maiores. Leitor de tela continua **não verificado**. |
| 5. Acusar nomes descartados pelo empacotamento | **Feito; aceito como diagnóstico de edição.** | `acusar()` escreve quantidade, `data-sobra-nomes` e `console.warn` com bairro e nomes (1969–1975); também cobre as etiquetas junto às pessoas (1977–1980). Não é aviso visível ao usuário, mas satisfaz o diagnóstico explícito pedido. QA: 42 de 42 etiquetas, nenhuma sobra. O ramo de sobra não foi exercitado nesta revisão. |
| 6. Formatar SVG/dados e documentar atualização | **Feito; aceito.** | Comentário nas linhas 3–12 relaciona `G`, SVG, ligações, `C`, metadados e diagnóstico de sobra, apontando o gerador. SVG separado por bairro/item/ligação e dados em várias linhas. Elementos individuais ainda têm linhas longas, mas a edição deixou de exigir procurar dentro de uma única linha para a planta inteira. |

A observação menor sobre `deltaMode=2` também foi atendida: a roda normaliza ambos os eixos pela altura da área quando a unidade é página (1900). Não solicito reabrir as recomendações de desempenho da volta 1: o empacotamento continua na inicialização, e o QA não apresenta evidência nova que o torne bloqueante.

## Bloqueio novo: transferência de captura encerra o arrasto de um dedo

**Local:** `amostra.html`, linhas 1927–1936; mesmo código em `amostra/fontes/nav_v2.js`.

O conserto ligou `pointerup`, `pointercancel` e `lostpointercapture` diretamente a `solta()`. Essa função não distingue o elemento que perdeu captura nem uma transferência de captura de um encerramento do gesto.

A sequência é:

1. O toque começa num descendente da tela, que recebe captura implícita do navegador.
2. Ao superar 6 px, a linha 1928 pede captura na `tela`, e a linha 1929 aplica o primeiro deslocamento.
3. A transferência dispara `lostpointercapture` no descendente antigo. O evento borbulha até a tela e chama `solta()`.
4. `solta()` remove o toque de `toques` e, sendo o único, zera `arr`. Os movimentos seguintes chegam à tela, mas param no `if(!arr)return` da linha 1919.

Isso coincide com a evidência do QA, não apenas com uma hipótese: em `toque-alvos.json`, tanto em 1280 × 1000 quanto em 320 × 640, o pedido de **96 × 48 px** resulta em **12 × 6 px**. A sequência registrada contém `lostpointercapture` no SVG/texto/caminho antigo, depois `gotpointercapture` na `MAIN.tela`, seguido de movimentos que não deslocam mais a vista.

A especificação distingue transferência e fim: ao mudar o capturador, emite perda no alvo anterior e ganho no novo; toque tem captura implícita e `lostpointercapture` borbulha. Fontes primárias: [processamento da captura pendente](https://www.w3.org/TR/pointerevents3/#process-pending-pointer-capture), [captura implícita](https://www.w3.org/TR/pointerevents3/#implicit-pointer-capture) e [atributos dos eventos](https://www.w3.org/TR/pointerevents3/#attributes-and-default-actions).

**Correção recomendada:** manter a limpeza comum para encerramentos efetivos, mas filtrar a perda de captura antes de chamá-la. A perda que veio de um descendente durante a transferência para a tela não pode remover o toque ativo. Um caminho é tratar separadamente `lostpointercapture`, conferindo seu alvo e se a tela mantém a captura daquele `pointerId`, além da identidade do ponteiro do gesto. Preservar a limpeza quando a própria tela realmente perder a captura, e o reinício da referência na passagem de dois dedos para um. Corrigir a fonte `nav_v2.js` e o HTML gerado de forma consistente; não apenas o artefato final.

A minha recomendação anterior de “mesma limpeza” foi ampla demais: reaproveitar a rotina é adequado, mas os eventos precisam ser classificados antes. Perder a captura no alvo antigo não significa que o dedo terminou o gesto.

## Ressalva nova, sem bloqueio adicional: modalidade fica presa à largura de abertura

O conserto 4 decide modalidade apenas em `abrir()` (1994). O redimensionamento chama `reajustar()` para o canvas (1950–1951), sem rever `fundo()` enquanto a ficha está aberta. Por leitura: abrir em 1280 e reduzir para 320 deixa uma ficha de largura total não modal; abrir em 320 e ampliar mantém o fundo inerte embora o painel já não cubra a tela. Fechar e reabrir recalcula o estado.

Recomendo sincronizar modalidade com a largura enquanto a ficha estiver aberta, preservando foco e devolução ao fechar. É um caso introduzido pela modalidade responsiva; **não reproduzido nesta revisão**, e não acrescento bloqueio da porta por ele. Se a modalidade for deliberadamente fixa até fechar, registrar essa exceção à decisão 18.

## Consertos para a próxima volta

1. **Bloqueia:** distinguir transferência de captura de encerramento; impedir que `lostpointercapture` do descendente apague o gesto que continua na tela. O arrasto de um dedo precisa continuar por todo o percurso, preservando toque simples, supressão de clique, pinça → um dedo e cancelamento. Na conferência seguinte do QA, usar entrada real do navegador e os mesmos alvos e percurso que demonstraram a regressão.
2. **Recomendado:** recalcular modalidade da ficha aberta ao mudar a largura, ou registrar a exceção de modalidade fixa até fechar.
3. **Documentação associada ao bloqueio 1:** ajustar as afirmações de arrasto conferido em `consertos.md` e `amostra.md` à evidência do QA desta volta; registrar a correção e a nova evidência quando existirem, preservando o histórico.

**volta**
