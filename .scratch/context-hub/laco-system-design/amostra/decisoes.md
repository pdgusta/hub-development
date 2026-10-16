# Decisões da amostra (o que decidi sozinho onde caberia pergunta)

Fonte: `descricao/descricao-do-hub.md`, v3.2. Base: a mistura aprovada (`conceitos/mistura/`, com as decisões de lá).

1. **O zoom muda o recorte (viewBox), não a página.** Assim a página nunca rola, o texto fica nítido em qualquer zoom e
   as medidas do desenho (folga, cruzamentos) valem em qualquer nível.
2. **Roda sem tecla anda para cima e para baixo.** O Gustavo definiu Ctrl + roda (zoom) e Shift + roda (para os
   lados); a roda sozinha completa o par.
3. **O botão do meio também arrasta**, além do direito; o esquerdo fica só para clicar nas fichas. No toque, um dedo
   arrasta e dois aproximam.
4. **As setas fazem duas coisas, conforme o foco:** no desenho, andam; fora dele, num cenário, passam o passo (como na
   mistura). O desenho tem um aviso no nome acessível ("Setas andam, + e − aproximam e afastam, 0 mostra tudo").
5. **Camada de detalhe a partir de 140% de zoom**, não sempre visível. O teto de rótulos saiu, mas "sem poluição"
   continua: 40 nomes a mais na visão inicial seriam a cidade radial recusada. A régua (R2) já põe o detalhe numa
   camada "ao aproximar". As etiquetas ficam escondidas na visão inicial, então a medição mede o que o Gustavo vê ao abrir.
6. **Só dois rótulos novos na visão inicial** (Agendador do Windows e Biblioteca do Maestri): eram os dois componentes
   desenhados sem nome. "Configuração de cada ferramenta" saiu do desenho como ícone e virou etiqueta de detalhe, porque
   o nome não cabe ao lado da biblioteca sem apertar a folga.
7. **Fileiras mais altas.** A de cima ganhou 45 unidades e a de baixo 70, para as etiquetas da Disciplina (6) e da
   Periferia (6) caberem. Custo: a visão inicial abre em 93% a 1280 x 1000 (a mistura abria perto de 100%).
8. **A razão entre grupos ficou em 1,53** (a mistura estava em 1,66). O par mais perto é o mesmo da volta 1, Porta do
   banco e Agentes; o que subiu foi a distância mediana dentro dos grupos, porque as fileiras ficaram mais altas. Passa,
   mas no limite; se a porta pedir folga, o caminho é afastar a coluna das pessoas.
9. **Telas estreitas abrem a 75%, centradas no Banco local**, quando caber tudo deixaria o texto abaixo de 60%. A
   legenda vira um botão "Legenda"; a ajuda de navegação some (fica no nome acessível do desenho e neste `.md`).
10. **Botões de zoom no canto inferior esquerdo.** No direito, a linha do maestro à biblioteca (só no cenário dele)
    passaria por baixo deles.
11. **A lista de bairros em botões, que a mistura tinha a 320 px, saiu**: no canvas, cada bairro se alcança pelo Tab,
    e a vista vai até ele.
12. **O próprio SVG saiu da ordem do Tab** (o Edge o tornava focável); o desenho em si é a área `main`, focável, que
    recebe as setas e o zoom.

## Volta 2

13. **"Menor nome a 13 px" = altura da caixa do menor texto da planta**, como o UX mediu (caixa, não corpo da letra).
    O menor é o nome de bairro (~19 unidades), então a planta abre inteira a partir de ~70%. Abaixo disso, 75% no Banco
    local. Quando o enquadramento dá entre 70% e 75%, abre inteira.
14. **O canto dos botões de zoom só conta se cobrir algo da planta** (item, bairro, muralha). Se cobre, o enquadramento
    desconta a faixa de baixo ou a coluna da esquerda, a que der mais zoom. Assim a 1280 x 1000 segue em 93%.
15. **Checkpoint → Agentes num traço só com o Contrato.** O UX deu duas saídas; escolhi juntar. Pela outra (entrar pelo
    lado de dentro da muralha) a linha passaria a poucos pixels da linha azul que sobe dos agentes até a nota. Juntas,
    as duas regras descem como um traço roxo. A linha do Checkpoint ainda vai até os agentes, então acende sozinha no
    cenário "altere" (sem o Contrato aceso).
16. **Espaço da etiqueta: 10 unidades embaixo de um nome, 6 nos outros lados.** Com 10 em volta toda, "Hook de uso" e
    "Lembrete do maestro" não cabiam na Disciplina. Os dois casos do UX eram de etiqueta logo abaixo do nome.
17. **"Ver tudo" pode ir abaixo de 35%.** O zoom mínimo é 35% ou o enquadramento inteiro, o que for menor (25% a 320
    px), para "Ver tudo" mostrar tudo e ainda deixar aproximar depois. Não há conflito com o UX 5: a abertura e "Ver
    tudo" são funções separadas.
18. **A ficha só é modal quando cobre a tela.** Na largura toda (telas estreitas) vira diálogo modal com o fundo
    inerte; mais estreita, fica painel ao lado, como na mistura.
19. **Cabeçalho compacto já abaixo de 1100 px** (o UX pediu ~1100), não só a 760.

## Volta 3

20. **Perda de captura só encerra o gesto se for da própria tela.** No toque, o elemento tocado tem captura implícita;
    quando a tela toma a captura aos 6 px, o elemento perde e o evento borbulha. Isso é transferência, não fim. Fim é
    `pointerup`, `pointercancel` ou a tela perder a captura. Mantive a captura só depois de 6 px (o UX também deu a saída
    de capturar já no aperto, mas isso tiraria o toque simples das fichas, que o Prumo pediu na volta 1).
21. **A modalidade da ficha acompanha a largura enquanto ela está aberta** (completa a decisão 18). Ao virar modal, o
    foco vai para "Fechar" se estava fora da ficha; ao deixar de ser, o foco fica onde está.
22. **A legenda recolhe também pela altura** (abaixo de 800 px). Os cenários seguem em fileiras que quebram linha
    acima de 1100 px de largura, e a ajuda de navegação continua visível nessas janelas.
