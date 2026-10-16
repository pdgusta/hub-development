# Revisão da amostra v3 — Prumo, 2026-10-14

## Parecer vigente: aprovada para apresentação ao Gustavo

**Amostra v3 APROVADA para devolver ao maestro e apresentar ao Gustavo.** As três pendências abaixo foram corrigidas e reproduzidas na revisão dirigida. Não há importante/bloqueante restante neste escopo. Recomendo levar esta forma ao Gustavo, preservando clima, paleta e tipografia já aceitos. A preferência dele pela forma e a integração nas cinco telas continuam como etapas posteriores.

- **Realce legível:** selecionar o 32 mantém opacidade mínima **1** em todos os marcos e folhas, com e sem redução de movimento. O quadrado não relacionado usa de fato `#2f4a2a` sobre `#d3e2ca`, contraste **7,26:1**; não depende mais do esmaecimento. Os marcos mantêm texto legível e o destaque usa bordas/fundos. A animação `assentar` usa preenchimento inicial, sem estado final que sobreponha o destaque.
- **Dica dispensável e percorrível:** foco no lacre “acha” + Esc fecha a dica mantendo foco no lacre. Enter no 16 + Esc fecha placa e dica, foco no 16, sem reabertura imediata. Ponteiro movido do marco para dentro da dica: ela permaneceu aberta depois de 400 ms; movido para fora, fechou. Repetido nos dois tamanhos.
- **Veracidade dos critérios:** cabeçalho, cartucho e dica agora dizem verificação/aceite **final** pendente. Não afirmam cinco estados individuais ausentes da API. Fio “verifica” continua representando a finalidade correta do ticket 17.
- **Resultados em palavras:** destaques 25, 22 e 34 conferem com a API: respectivamente **6, 4 e 4** dependentes diretos, filtrando resolvidos e desempate pelo número. Foco no primeiro mostrou “abriu caminho para” e acendeu só o quadrado 25. A regra é explícita e reproduzível; a retirada dos tipos evita acumular texto no índice.
- **Capturas próprias:** abertas e conferidas em 1600×900 e 1280×800, incluindo seleção do 32 com redução de movimento. A faixa termina em **y≈868 px** na janela de 1600×900, inteira na primeira tela; em 1280×800 termina em y≈1014 px e pede rolagem vertical. Nenhuma rolagem horizontal ou erro JS no roteiro. Isso não exige reduzir as fontes para fazê-la caber em 1280.

Provas vigentes: `C:/Projetos/context-hub/.maestri/roles/d4ce63fd-ce3e-45b5-88f6-6bbd68695030/revisao-amostra-v3-dirigida/` (`resultados.json` e PNGs); script `review_amostra_v3_dirigida.py` no diretório pai. Sem alteração do portal ou escrita em dados reais pelo revisor. Aceite limitado à amostra: Abrir o ticket/navegação ainda demonstrativos; marco 7 e visual integrado não foram aprovados nesta rodada.

## Primeira revisão: histórico, pendências encerradas acima

**Recomendo manter esta forma e corrigir três pontos antes de aprovar a amostra para apresentação.** A faixa de largura total e a separação feito / frentes / verificação / destino dão uma leitura mais clara do caminho do que a trilha recusada. Não recomendo outro redesenho de tema, paleta ou tipografia; estes já foram aceitos pelo Gustavo. A preferência pela nova forma ainda é dele.

Revisado `v2/amostra-inicio.html`, servido em `127.0.0.1:8765`. Capturas próprias no Edge em 1600×900 e 1280×800; início, página inteira e estados interativos. Provas de dados comparadas com `/api/estado` da torre real 8770 e com `map.md` e ticket 17. Não alterei o portal e não revisei o marco 7.

## Importantes

1. **O realce torna conteúdo ainda operável pouco legível.** Regras `.caminho.focado .marco`, `.folha` e `.so-indice`: selecionar a Sonda do Dolt deixa os outros marcos com opacidade **0,32**, inclusive o “estamos aqui”; eles continuam clicáveis. Os quadrados não relacionados ficam com opacidade **0,22 quando reduced-motion está ativo**, e o contraste do número contra o fundo do próprio quadrado cai para aproximadamente **1,38:1**. Sem reduced-motion, a animação `assentar` com preenchimento final mantém a opacidade das folhas em 1 e sobrepõe esse CSS: o mesmo destaque muda de comportamento conforme a preferência de movimento. Recomendo realçar por borda, fundo, cor do fio e/ou selo, preservando texto legível nos demais itens. Se mantiver esmaecimento, medir o contraste composto, não só as cores base. Controles operáveis não ganham a exceção de texto de controle inativo. Referência: [W3C, contraste mínimo](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html). Evidências: `escolhido32-esmaecido-1600.png`, `escolhido32-reduced-1600.png`, `folha01_reduced` no JSON.

2. **Dicas não podem ser dispensadas por Esc e não podem ser percorridas com o mouse.** O handler global só chama `soltar()` quando há marco escolhido. Foquei “acha”, apertei Esc: a dica continuou visível. Ao escolher o 16 e apertar Esc, a placa fechou, mas a dica continuou sobre outros marcos. `.dica` tem `pointer-events:none` e o `mouseleave` do disparador a esconde, impedindo entrar na própria dica para lê-la. Recomendo permitir dispensa por Esc sem deslocar foco/ponteiro, evitar reabertura imediata pelo foco restaurado e manter a dica aberta ao mover o ponteiro entre disparador e conteúdo. Referência primária: [W3C, conteúdo em hover/foco](https://www.w3.org/WAI/WCAG22/Understanding/content-on-hover-or-focus.html). Evidências: `esc_criterio_dica=true`, `esc.dica_visivel=true`, captura `escolhido16-1280.png`.

3. **“Nenhum critério verificado” afirma estado individual que a fonte não fornece.** Cabeçalho, cartucho e dicas dos lacres. A API contém os textos dos cinco critérios, sem campo de verificação por critério. O ticket 17 aberto comprova que a **verificação final nas duas máquinas está pendente**; não comprova que cada critério nunca foi verificado isoladamente. Recomendo manter os lacres tracejados como “aceite final pendente” e usar “verificação final pendente” no cabeçalho, sem deduzir cinco estados individuais. Isso resolve com linguagem e não exige mudar o núcleo/API. O fio “verifica” do 17 ao destino é correto como relação de finalidade: a Question do ticket 17 diz que ele verifica os cinco critérios e fecha o mapa; não deve ser entendido como verificação já realizada.

## Veracidade e forma: conferidos

- Os 53 registros copiados têm o mesmo estado e `bloqueado_por` da API real no momento da revisão. Contagens: **43 resolvidos, 1 em andamento, 8 abertos, 1 descartado**. A soma de nove frentes abertas inclui o em andamento, conforme a legenda da amostra.
- Camadas reais: `[09,12,14,32,53]`, `[11,15]`, `[16]`, `[17]`. Os sete marcos do caminho estão nas colunas correspondentes. 32 e 53 foram apresentados à margem; ambos têm `bloqueia=[]`, portanto “ninguém espera por eles” está correto no grafo atual. Isso não quer dizer que sejam dispensáveis.
- O 09 como “estamos aqui” corresponde a `claimed`. 12/14 sem bloqueadores abertos podem partir. As sete relações entre frentes abertas conferem. A contagem de 42 ancestrais resolvidos do 16 é de dependências diretas e transitivas, conforme a dica, não só dos cinco predecessores diretos já resolvidos.
- Não detectei fio de dependência atravessando a caixa de outro marco nos dois tamanhos (amostragem dos paths a cada duas unidades, excluindo origem e destino). Nas capturas, o corredor 09→16 preserva a leitura do 11.
- Sem rolagem horizontal nos dois tamanhos; menor fonte computada de texto visível: **14 px**. Marcas, cartucho, títulos e selos permanecem legíveis no estado normal.
- Contrastes base pedidos: lápis `#6f665a` contra mesa `#f8f0e1` **4,98:1**, contra cartão `#fbf6ec` **5,23:1**; quadrados `#f4f8ef` sobre `#3f6b32` **5,81:1**, sobre `#2f4a2a` **9,15:1**. Passam nesses pares; o problema é o estado esmaecido descrito acima.
- Índice com **uma** entrada no Tab; End levou ao 52, Home ao 01, seta para baixo avançou uma linha (cinco quadrados em 1600, quatro em 1280). Foco e Enter no 16 abriram a placa correta; Esc fechou a placa com foco no marco, ressalvada a dica persistente.
- Redução de movimento desligou anel e animação das folhas. Nenhum erro JS emitido no roteiro.

## Sugestão sobre a leitura de relance

“Já feito” comunica bem **quanto** trabalho terminou, mas os quadrados numerados e os totais por tipo ainda dizem pouco sobre **o que** foi conquistado sem interação. Recomendo dar a duas ou três decisões/resultados já registrados uma frase curta visível, deixando o índice como detalhe explorável: por exemplo, títulos de “Contrato file-first” (10), “Revisão do sync e da divergência” (33) e “Pesquisa ampla de busca” (50), sem reclassificar pesquisa como implementação. Não precisa adicionar texto longo ou reconstruir o diagrama.

“Agora / Em seguida / Depois / Por fim” deve continuar significando **ordem por dependência**, sem promessa de calendário/prioridade. O estado e a dica já ajudam a distinguir o que está em andamento do que apenas pode começar.

Evidências próprias: `C:/Projetos/context-hub/.maestri/roles/d4ce63fd-ce3e-45b5-88f6-6bbd68695030/revisao-amostra-v3/`, com `resultados.json` e PNGs; script `review_amostra_v3.py` no diretório pai. Capturas de início nos dois tamanhos, seleção do 16 e esmaecimento do 32 foram abertas e conferidas. Sem escrita de teste nos dados reais.
