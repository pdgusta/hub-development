# Parecer da carta 2: Vigia e manutenção (volta 1)

Revisor: Lente, 2026-10-16. Carta: `carta-2-vigia.html` (Aquarela).
Capturas em `capturas-lente/`: `c2-1600-inteira.png` (fatias `-p0` a `-p5`) e `c2-390-inteira.png` (fatias `-p0` a
`-p12`). A largura de 390 px foi capturada dentro de um iframe de 390 px, porque o Edge sem cabeça não abre janela
com menos de uns 480 px.

## Veredito: volta

No computador, a carta está muito boa. O caderno de aquarela do farol é uma linguagem só dela. O diagrama fica no
centro de cada folha, e as três tintas (ok, informa, divergência) carregam a leitura. A ordem do brief está em todas
as folhas: problema, cena, com a escolha × sem ela. O resumo final segue a numeração da rodada. Os destaques são o
sino da folha 6 e as duas gavetas da folha 4: dá para entender só olhando.

A carta volta por duas razões: no celular, o diagrama vira miniatura, e um fato da folha 6 está impreciso.

## Fatos (spec, acordo seção c, conversa dos revisores)

Estão certos:
- Folha 1: o caminho do arquivo, a troca atômica, o nível por item, o topo igual ao pior, a passada a cada 5 min e
  os leitores. O "o dono da faixa confirma" bate com o spec de antes da revisão.
- Folha 2: os três casos e o incerto como "informa, no mínimo, com o motivo".
- Folha 3: a saída ≠ 0, o item no estado da vigia com nível informa e a regra geral deixada para o ticket 56.
- Folha 4: a data no nome da pasta e o `archived_at` mantido.
- Folha 5: o prazo de 30 dias vem do ticket 56 (laço do system design), e o script de limpeza só simula.

## Consertos

1. **[obrigatório · celular] O diagrama vira miniatura.** Em 390 px, os SVGs das folhas 1, 2, 3, 5 e 6 encolhem para
   cerca de 1/3. O texto fica com uns 5 px. Na folha 1, "conflito de texto" encosta em "divergência". O centro da
   carta deixa de se ler (`c2-390-inteira-p0`, `-p1`, `-p4`). Conserto: abaixo de 820 px, redesenhar a cena em
   coluna, de cima para baixo. Isso vale sobretudo para a folha 1 (vigia → arquivo → leitores), a folha 2 (os três
   casos um embaixo do outro) e a folha 6 (menos turnos, ou o eixo na vertical). Outra saída: dar ao SVG uma largura
   mínima de uns 720 px, dentro de uma moldura que rola para o lado, com a dica "arraste". O texto do diagrama precisa
   de pelo menos 12 px na tela.
2. **[obrigatório · fato] Folha 6, problema.** O texto diz: "o Codex não tem barra de estado, então ganhou dois
   avisos". Só o aviso de fim de turno vem da falta de barra (story 25 da faixa 7). A notificação da vigia quando o
   estado piora vale para todos os harnesses (ticket 33). Conserto, por exemplo: "a vigia já avisa quando o estado
   piora, em qualquer harness; como o Codex não tem barra de estado, ele ganhou também o aviso de fim de turno
   (`notify`), a cada turno com divergência. Juntos, quantas vezes você ouve o sino?"
3. **[celular] O número da folha espreme o texto.** O carimbo com o número ocupa a coluna da esquerda, e o problema
   cabe em uns 190 px (`c2-390-inteira-p1`, `-p4`). Conserto: no celular, pôr o carimbo acima do título, ou do lado
   do rótulo "escolha N da lista de 23", e deixar o texto com a largura toda.
4. **[clareza] Folha 3, quem grava o item.** O rótulo "grava o item" está sobre a seta do estado para o farol.
   Assim, parece que a vigia grava o item. Quem grava é o script da cópia (faixa 10); a vigia só lê e avisa. Conserto:
   levar "grava o item" para a seta que desce do barco até o "estado da vigia", e deixar "lê e avisa" na seta para o
   farol.
5. **[fato, leve] Folha 5, alternativa.** A frase "o desenho volta do zero quando o prazo vier" não está em
   nenhuma fonte. Conserto: tirar a frase, ou escrever "o script teria de ser desenhado de novo quando o prazo vier",
   marcado como consequência.
6. **[opcional] Folha 6, terceira via.** A revisão também propôs deixar a repetição como detalhe da construção, sem
   decidir agora (Quadrante, Q-5, rodada 1). Se couber, uma linha no lado "sem política": "ou: deixar para a
   construção decidir".
7. **[não verificado] A fonte de mão no celular.** Na captura de 390 px, os textos de mão (subtítulo, "com a escolha")
   aparecem numa fonte de reserva, não na mesma do computador. A causa pode ser a captura (iframe e tempo virtual).
   Vale conferir no celular de verdade se a fonte carrega.

Depois dos consertos 1 a 4, a carta passa. Os itens 5 a 7 são para melhorar a leitura.

---

# Volta 2 (2026-10-16): passa

Capturas: `capturas-lente/c2v2-1600-inteira.png` (fatias `-p0` a `-p5`) e `c2v2-390-inteira.png` (fatias `-p0` em diante).

Os consertos foram conferidos:
1. Celular: cada cena fica numa moldura que rola para o lado, com a dica "arraste para o lado →". O texto do diagrama
   se lê na primeira vista (`c2v2-390-inteira-p1`). **Feito.**
2. Folha 6: o problema agora separa a vigia, que avisa em qualquer harness, do `notify`, que vem da falta de barra
   no Codex. Bate com a story 25 da faixa 7 e com o ticket 33. **Feito.**
3. Celular: o carimbo do número fica acima do rótulo, e o texto ocupa a largura toda. **Feito.**
4. Folha 3: "o script grava o item" está na seta que desce do barco, e o farol tem "lê" e "a vigia lê e avisa".
   **Feito.**
5. Folha 5: a frase foi marcada como consequência. **Feito.**
6. Folha 6: a nota da terceira via bate com o Q-5 do Quadrante. **Feito.**

Ressalvas (não seguram a carta):
- Na minha captura de 390 px, a fonte de mão ainda aparece na reserva. Na da Aquarela, ela carregou. A diferença é,
  provavelmente, da captura. Vale olhar num celular de verdade quando der.
- No celular, a moldura começa no canto esquerdo da cena. Na folha 1, a linha do caminho (`context-hub\.local\…`)
  começa cortada à direita, e só se lê arrastando. Aceitável, porque a dica está ali.
