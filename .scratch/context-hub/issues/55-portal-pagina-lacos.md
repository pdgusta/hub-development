# Portal: página Laços

Type: task
Status: resolved
Blocked by:

## Question

Uma página nova do portal, abaixo de "Decisões", que mostra qualquer laço em voo, de pesquisa ou de suíte de
testes. Pela ideia do Gustavo, o laço que o maestro monta aparece ali e se edita como num n8n: a página é uma
representação, e o que muda de verdade volta ao maestro como pedido pela caixa. Pedido integral no fim de
`portal/pedido.md`. Fora do mapa (peça do portal), como o ticket 53.

## Comments

- 2026-10-14 ~21h: a carta-proposta "Laços" (`amostras/portal-lacos-proposta.html`, carta `portal-lacos-proposta`)
  foi aprovada pelo Prumo para mostrar (`portal/revisao-lacos-proposta.md`). O aceite não autoriza construir. A
  rodada 1 foi aberta no portal com as três perguntas da carta.
- 2026-10-14 21:11, resposta à rodada 1 (portal, envio `fccf26ce-4671-4134-a524-879a28f24c72`):
  - **Primeiro passo = B:** ver todos os laços e pedir: girar os botões, como o teto e a parada, e pedir parada e
    pausa. Pedido a mais: "também quero mais opções por nó (harness, modelo, etc), com campo para eu comentar. Isso
    dá margem para eu pedir ao maestro uma customização nível nó ou nível laço inteiro."
  - **Nome = Laços.**
  - **Suítes = depois** dos laços de pesquisa.
  - Construção liberada pelas respostas. Vai ao Designer, com revisão do Prumo. O `laco.json` de cada laço é
    escrito pelo maestro, no formato que o Designer fixar.

- 2026-10-14 (~21h30): marco L1 (contrato do `laco.json` e do envio `alteracao-laco`) escrito pelo Designer em
  `portal/proposta.md` §4.4, §4.5 e Anexo A, em revisão pelo Prumo. Respostas de fato do maestro: faixas de
  `gate_novos` de 0,01 a 0,5, teto de 100 a 20.000 tentativas e de 0,5 a 12 h, `trabalhadores_por_gerador` de 1 a 40,
  `max_celulas_novas_por_onda` de 10 a 500. Ids `embeddings-2026-10-14` e `ampla-2026-10-13`, atribuídos pelo registro.
  Os nós são só processos Python, sem recrutas: harness não se aplica, e o modelo é a lista `excluir_manual` do
  despachante. Os estados "esperando cota" e "parado" entram já no contrato. A pesquisa ampla teve 7.382 tentativas
  no fechamento (os 7.388 do ticket 50 somam chamadas em voo). O `excluir_manual` ganha o tipo `lista`, que vale ao
  reiniciar o processo; os dois `LEIA.md` foram corrigidos.
- 2026-10-14 (~21h50): L1 aprovado pelo Prumo (`portal/revisao-lacos-L1.md`). O maestro escreveu os arquivos reais:
  `laco-embeddings/laco.json` e `laco/laco.json` (do Anexo A), `portal/lacos.json` e a chave `"lacos"` no
  `projeto.json`. Ressalvas do anexo: (a) correção do maestro: a pesquisa ampla teve recrutas na partida (Bússola,
  Faísca, Brasa e Centelha, dispensados; Tear decidiu os ambíguos). Como o laço terminou, eles entram só no
  `detalhe` dos nós, sem controle. (b) `pools_aptos` confirmado, com rótulo "pools do gateway com modelo apto".
  (c) `fora_agora` inclui pausas curtas por falha; aceito, e o detalhe do despachante diz isso. O L2 (núcleo)
  está com um subagente do Designer.
- 2026-10-14 (22:01): primeiro uso previsto: o Gustavo recusou a cidade radial v2 e quer **um laço só para criar o
  system design** depois desta página pronta, com um agente forte em design e demonstração visual de system design
  e um forte em UI e UX (ver a nota do system-design no `map.md`). Detalhe a conversar quando a página estiver pronta.
- 2026-10-14 23h10: L2 (núcleo) aprovado pelo Prumo na revisão dirigida; portal real reiniciado com o núcleo novo; `/api/lacos` mostra os dois laços como terminados, 0 problemas. L3 (a tela) em construção por um subagente do Designer.
- 2026-10-14 23:46, comentário do Gustavo (portal, envio `e4d38fa5-f293-4faf-8a66-b646836127d3`): "vi que deixou esse
  ticket como fora da peça pro acervo do maestro, mas vou querer sim no futuro". O "fora do mapa" do topo quer dizer
  só que a construção da página não é um passo do mapa do hub. **Registrado:** o portal com a página Laços entra no
  futuro como peça do acervo do maestro, para servir a outros projetos. Anotado no "Not yet specified" do `map.md`,
  ao lado do template da suíte de busca.
- 2026-10-15: no horizonte (Radar de `estrategia-pos-pesquisa.md`), a pedido do Gustavo: quando esta página ficar pronta, partir do vídeo https://youtu.be/Ysr7oNDajJI para melhorar o recruta Designer, junto com o laço do system design.
- 2026-10-15, **resolvido.** O Designer entregou a tela (L3) e o Prumo aprovou os três marcos (`portal/revisao-lacos-L1.md`,
  `-L2.md`, `-L3.md`; provas em `portal/conferencia/lacos-L3/`; testes: 223 no núcleo e 6 no projeto real). A página
  está no ar no portal real, abaixo de "Decisões": lista dos laços (espera você, em voo, terminados), fluxo de nós com
  uma palavra por seta, gaveta do nó (números lidos, valor configurado, valor em uso, "sua proposta"), botões que viram
  pedido ao maestro pela caixa (mudar valor, parar e, se o laço declarar, pausar e retomar), comentário por nó e pelo
  laço, e o estado de cada pedido (enviado, lido, aplicando, aplicado com recibo, recusado, conflito). Os dois laços
  reais aparecem como terminados, só leitura, com o comentário aberto. Duas decisões aceitas pelo Prumo: conflito de
  laço não entra no contador "aguardando você" (aparece uma faixa na própria página), e um pedido novo para o mesmo
  botão substitui o anterior ainda aberto. **Para o maestro:** o desfecho de um pedido sobre laço, gravado no `.md` da
  caixa, segue a proposta §4.5. **Destravado:** o laço do system design e a melhoria do Designer pelo vídeo, quando o
  Gustavo pedir.
