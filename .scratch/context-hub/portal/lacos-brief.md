# Página "Laços": brief de construção (2026-10-14, ~21h30)

Decisão do Gustavo (rodada do ticket 55, `.scratch/context-hub/issues/55-portal-pagina-lacos.md`): primeiro passo
**B** (ver todos os laços + pedir: girar botões como teto e parada, pedir parada e pausa); nome **"Laços"**; suítes
**depois** dos laços de pesquisa. A mais: em cada nó, mais opções (harness, modelo etc.) e um **campo de comentário
por nó e pelo laço inteiro**, que viram pedidos ao maestro pela caixa ("customização nível nó ou laço").
Construção liberada; revisão do Prumo por marco.

Fontes: carta aprovada `amostras/portal-lacos-proposta.html` (forma e camadas); pareceres do Prumo
`portal/revisao-direcao-lacos.md` e `portal/revisao-lacos-proposta.md` (contrato do pedido); `portal/proposta.md`
(especificação do portal; §4 caixa); `portal/construcao.md` (regras fixas: Edge só pelo perfil).

## Marcos

- **L1 — Contrato (só texto, em `proposta.md`):** (a) formato do `laco.json` (descrição de um laço, escrita pelo
  maestro na pasta do laço): id, título, ticket, execução, nós, ligações, controles editáveis (id, nó, tipo, faixa
  ou valores permitidos, unidade, quando vale, onde está o valor vigente), opções por nó (harness, modelo… como
  controles do tipo escolha), capacidades (parar após a onda, parar de despachar, pausar/retomar só se o laço
  declarar), fontes de estado (arquivos/tabelas a ler, só dentro da pasta do laço) e como ler a revisão da
  configuração; (b) tipo novo de envio **`alteracao-laco`** no contrato da caixa (§4): operações `mudar-controle`,
  `pedir-parada`, `pedir-pausa`, `pedir-retomada`, `comentario-no`, `comentario-laco`; corpo imutável com envio
  (UUID), laço, execução, operação, nó/controle (só ids do `laco.json`), antes/depois tipados, revisão da config
  vista, texto (comentários); estados enviado → lido → aplicado (com recibo: execução, antes/depois, revisão, momento
  de efeito) | recusado | conflito ("você viu / agora está / você pediu") | encerrado-sem-aplicar; quem grava cada
  estado (o portal grava o envio; o maestro grava lido/aplicado/recusado/conflito/encerrado no `.md`, como as
  respostas); o portal nunca escreve na pasta do laço nem executa nada; o navegador só manda ids. (c) A tela (§2):
  "Laços" abaixo de Decisões, lista, fluxo, gaveta do nó, comentário por nó e por laço, sem suítes nesta fase.
  Entrega: diff da proposta + um exemplo de `laco.json` para cada laço real (embeddings e pesquisa ampla) como
  ANEXO da proposta (o maestro escreve os reais) → Prumo → maestro.
- **L2 — Núcleo:** leitor de laços (`laco.json` + estado, só leitura, com hora e "sem sinal"), endpoints, envio
  `alteracao-laco` validado contra o `laco.json` (409 se a revisão mudou), estados lidos do `.md`; testes no padrão da
  suíte do núcleo; fixture com dois laços. → Prumo.
- **L3 — Tela:** página no idioma Mesa de mapas, como a carta aprovada (lista, fluxo de nós, gaveta, botões que viram
  pedido, comentários, estados do pedido); conferência no navegador com a fixture e com o portal real. → Prumo →
  maestro.
