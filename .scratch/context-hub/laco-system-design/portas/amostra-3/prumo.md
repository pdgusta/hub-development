# Parecer do Prumo — porta da amostra, volta 3

2026-10-15. Peça: `amostra/amostra.html` (volta 3). **Recomendação: passa, sem bloqueio de código nesta porta.**

## Escopo e evidência

Li o brief e o relatório do QA desta volta, meu parecer da volta 2, `consertos.md` (incluindo as correções históricas e a seção Volta 3), `decisoes.md` (20–22) e `amostra.md`. Conferi os trechos pertinentes do HTML, de `fontes/patch_v3.py` e de `fontes/build_amostra3.py`.

Revisão limitada ao bloqueio do toque, à ressalva da modalidade da ficha e à documentação pedida na volta 2. Não editei a peça nem executei testes, provas ou varreduras adicionais. As medições de execução citadas são do QA; as referências de linhas abaixo são do HTML atual. Não reabro os itens aceitos na volta 2 nem substituo os pareceres de conteúdo e UX.

## Pedidos da volta 2

| Pedido | Situação | Evidência e aceite |
|---|---|---|
| 1. Não encerrar o arrasto ao transferir captura do descendente para a tela | **Feito; aceito. Bloqueio encerrado.** | Linhas 1942–1943: `pointerup` e `pointercancel` continuam em `solta()`, mas `lostpointercapture` só chama a rotina quando `ev.target===tela`. A perda que borbulha do descendente não apaga o toque ativo. A correção também consta do gerador da volta 3 e do patch, não apenas do HTML entregue. |
| 2. Modalidade da ficha acompanha a largura com ela aberta | **Feito; aceito no código. Ressalva encerrada.** | Linhas 2013–2014: no `resize`, se a ficha estiver aberta, recalcula se ela cobre a janela e atualiza `fundo()` quando a modalidade muda. Ao virar modal, leva o foco a “Fechar” se estava fora. Linhas 2006–2007: fechar remove a inércia e devolve o foco. |
| 3. Corrigir as afirmações anteriores e registrar evidência nova | **Feito; aceito.** | `consertos.md` preserva as afirmações da volta 2 com notas de correção, registra o resultado errado de 12 × 6 px e os erros da conferência própria, e acrescenta o resultado corrigido. `amostra.md` também corrige a afirmação histórica e descreve a volta 3. |

O filtro de captura corrige a causa identificada: a transferência tem perda no capturador antigo e ganho no novo, sem significar término do gesto. A distinção está alinhada à fonte primária já conferida na volta 2: [Pointer Events — processamento da captura pendente](https://www.w3.org/TR/pointerevents3/#process-pending-pointer-capture).

## Evidência do QA que sustenta o encerramento

O QA repetiu os três alvos que demonstraram a regressão — fundo, Banco local e nome — com entrada real do navegador. Nos cinco tamanhos, o pedido de **96 × 48 px** resultou em **96 × 48 px**, e o percurso contrário de **−150 × −90 px** também terminou com erro de **0 px**. Não abriu ficha após o arrasto; a classe `arrastando` apareceu durante o gesto e saiu ao terminar.

O relatório também confirma toque simples no botão e na ficha, cancelamento com limpeza, pinça seguida de retirada efetiva de um dedo sem salto e deslocamento completo com o dedo restante. Mouse, zoom central, “Ver tudo”/`0` e Tab real continuaram passando. Esses resultados sustentam o aceite do conserto sem a regressão da volta anterior.

A transição de modalidade durante redimensionamento tem conferência própria registrada em `consertos.md` (1280 → 320 → 1280, foco e fechamento). O relatório do QA confirma a modalidade nas larguras fixas, mas não relata essa sequência de redimensionamento. Meu aceite dessa ressalva se apoia na leitura do tratador e na conferência do autor; não apresento a sequência como teste independente do QA.

## Limites do parecer

Toque em aparelho físico e leitor de tela continuam **não verificados**. O QA registrou falha ocasional de geração de `click` com intervalo de aproximadamente 150 ms depois do arrasto, também na volta 2; com 200 ms ou mais, abriu em 8 de 8 tentativas. O registro de que o clique não chegou ao `document` não sustenta atribuir a falha ao tratador de clique da peça. A hipótese de reconhecedor de gestos/emulador permanece hipótese; não a transformo em novo bloqueio de código.

Não encontrei problema novo bloqueante nos trechos revisados. Esta aprovação é a do Prumo; a aprovação conjunta da porta depende dos outros dois pareceres.

## Consertos

Nenhum conserto pendente solicitado pelo Prumo nesta volta.

**passa**
