# Teste do canal de aviso do portal

Type: task
Status: resolved
Blocked by:

## Question

O aviso de resposta nova do portal do projeto chega ao maestro em todas as situações da §4.3 da proposta
(`.scratch/context-hub/portal/proposta.md`)? As situações são: maestro parado, maestro ocupado, duas respostas em 5 s,
servidor reiniciado com aviso pendente e nome errado de agente. Este ticket existe só para isso. A rodada de teste
(`portal/rodadas/2026-10-14-teste-do-canal-de-aviso-r1.md`) é respondida pelo Designer, não pelo Gustavo, e as
respostas não decidem nada do context hub. Fica fora do mapa.

Resolvido quando um canal passar em todas as situações, ou quando ficar registrado qual falhou e qual ficou valendo.

## Comments

### 2026-10-14 ~17h35, maestro: teste "maestro parado" (canal A)

- O aviso da resposta de 14:30 (envio `022e4d3f-110b-4b5a-a40a-c86f241bd117`) chegou ao maestro parado, como
  mensagem do terminal "Portal", logo depois de o Designer subir a torre pelo `iniciar.cmd` no canvas. Nenhum
  "respondi" no chat foi preciso.
- Absorvido: o `.md` da caixa passou de `estado: nova` para `lida`.
- Conteúdo da resposta de teste (dada pelo Designer, não decide nada): canal B escolhido para começar, as cinco
  situações marcadas, sequência aprovada, dois campos em branco.
- Antes do passo 2, o terminal "Portal" foi ligado também ao Designer (`maestri connect "Designer" "Portal"`); a
  ligação com o maestro continua.
- **Achado no mesmo teste:** depois do aviso, chegou ao maestro um prompt solto só com "(enviar)", o empurrão de
  texto preso, embora o aviso já tivesse sido entregue. E `GET /api/aviso` seguiu mostrando o envio `022e4d3f…` como
  `pendente` (1 tentativa, sem erro). Risco de reenvio duplicado e de lixo no prompt do maestro. Repassado ao
  Designer para investigar antes do teste do maestro ocupado. **O teste "parado" passou só em parte.**
- **Correção (Designer, 17:08):** teste parado às 16:58, aviso do envio `022e4d3f…` entregue e absorvido. Os dois
  defeitos foram corrigidos no núcleo, com 2 testes novos (122 OK, mais 4 do projeto real). O "(enviar)" solto vinha da
  conferência de texto preso, que procurava a mensagem na tela inteira do check e agora olha só a caixa de digitação.
  O "pendente" falso vinha do reparo de 30 s, que desfazia "enviando" durante o ask; agora só o arranque do servidor
  faz isso. Portal reiniciado às 17:08; a fila mostra `022e4d3f` como entregue.

### 2026-10-14, maestro: teste "maestro ocupado" (canal A)
- O maestro começou às 17:07:43 um turno longo, de uns 4 minutos, vigiando a caixa. O Designer gravou pela API o
  comentário "teste ocupado" (envio `07ac8751-fd3b-4db4-87db-60c43bbde0b0`) às 17:07:56. O arquivo apareceu na caixa
  às 17:07:58, e o aviso do "Portal" chegou ao maestro **dentro do mesmo turno**, como mensagem enfileirada, sem se
  perder. Absorvido: o `.md` da caixa passou para `estado: lida`. No fim do turno, a fila do portal ainda mostrava
  `enviando`, porque o ask espera o maestro parar. **Falta conferir** que vira `entregue` sem um "(enviar)" solto
  (o Designer confere).
- **Fechamento do teste ocupado:** o Designer conferiu que a fila passou de `enviando` para `entregue`, e não chegou
  nenhum "(enviar)" solto ao maestro.

### 2026-10-14 ~17h15, maestro: teste "duas em 5 s" (canal A)

- O Designer gravou dois comentários com 3 s de intervalo: "primeira" (`6216072e-c797-4e1c-9f8e-eb989ba7f776`, 17:14:25)
  e "segunda" (`13f63156-93e0-4ac8-81a9-80e8a4356d9c`, 17:14:28).
- Chegou ao maestro um aviso só com o primeiro, porque o segundo entrou na caixa depois de o ask sair. Na chegada,
  a fila mostrava a primeira como `enviando` e a segunda como `pendente`.
- O maestro conferiu a caixa inteira por `estado: nova` e absorveu **as duas** juntas; os dois `.md` estão em
  `lida`. Nenhuma se perdeu. O aviso da segunda ainda vai chegar; quando chegar, o maestro confere que o `.md` já está
  `lida` e não absorve de novo.
- **Fechamento das duas em 5 s:** nenhum aviso da segunda (`13f63156…`) chegou ao maestro. Em `caixa/.avisos.json`
  ela está `entregue` com **0 tentativas**: o portal não mandou aviso, provavelmente porque o `.md` já estava `lida`.
  Nenhuma se perdeu, porque o maestro absorveu as duas pela caixa. Falta o Designer confirmar que pular aviso de
  mensagem já lida é o comportamento previsto, e não um defeito.

### 2026-10-14 ~17h16, maestro: teste "reinício com aviso pendente" (canal A)

- Comentário "teste reinicio" (`c127aa8a-cdbb-4f7d-ac05-d41a636a95d4`, 17:15:09); o aviso chegou ao maestro.
  Absorvido: o `.md` está `lida`. Na chegada, a API do portal não respondia (servidor reiniciando) e o
  `.avisos.json` mostrava o envio `enviando`, 1 tentativa.

### 2026-10-14 ~17h17, maestro: teste "nome errado de agente" (canal A)

- Comentário "teste nome errado" (`67c287e4-ef70-43e6-ac04-04c53cf57a73`, 17:16:17); o aviso chegou ao maestro na
  **2ª tentativa** (a 1ª, com o nome errado, falhou; depois o Designer devolveu o nome e pediu "tentar de novo").
  Absorvido: o `.md` está `lida`. O erro em palavras mostrado na tela e na API durante a falha fica no registro do
  Designer (`construcao.md`).
- **Balanço do maestro:** nas cinco situações, nenhuma resposta se perdeu e nenhuma foi absorvida duas vezes. Ficam
  duas pendências para o parecer do Prumo: a entrega sem aviso da `13f63156…` (0 tentativas) e o resultado final do
  "parado" depois da correção das 17:08.

### 2026-10-14 ~17h40, maestro: resolvido

- O Prumo aprovou o marco 7 (`portal/revisao-marco7.md`) sem bloqueantes. O **canal A** (o portal avisa o maestro
  pelo terminal "Portal") passou nas cinco situações e ficou valendo; está registrado na §9 da proposta.
- A `13f63156…` com 0 tentativas é o previsto: um envio pendente cujo `.md` já está `lida` é encerrado sem novo aviso.
- Limites registrados pelo Prumo:
  - o tempo-limite e a escada de novas tentativas até `falhou` só foram provados em teste controlado;
  - um erro isolado da suíte não se repetiu e ficou sem causa verificada;
  - o motivo de um aviso que falhou só aparece na API;
  - a conferência de texto preso depende da forma atual do terminal do Claude Code;
  - o canal B não foi validado de ponta a ponta.
- Nota: o Gustavo esperava um vigia do maestro lendo a caixa (canal B) e deixou o canal A seguir porque já funcionava
  (fim do `portal/pedido.md`).
