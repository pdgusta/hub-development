---
titulo: A vigia no Codex pelo nome da conversa: o teste passou
ticket: 14
aberta: 2026-10-15
estado: absorvida
---

Na rodada anterior você pediu o teste do caminho pelo nome da conversa. A Sonda Codex o fez (relatório completo em
`bancada-nome-conversa.md`):

- **Um programa separado não alcança um Codex já aberto do jeito comum.** Ele muda o nome guardado da conversa, mas a
  tela aberta não muda, nem depois de um turno novo.
- **Passa se o Codex abre ligado a um servidor compartilhado.** Com o servidor do Codex (o app-server) rodando à parte e
  o Codex aberto ligado a ele (`codex --remote`), um programa ao lado renomeou a conversa três vezes, e o rodapé e o título
  do terminal mudaram sozinhos, sem nenhum turno.
- **O custo:** manter esse servidor vivo, abrir o Codex sempre ligado a ele, achar a conversa certa e lidar com queda e
  reconexão. O nome da conversa vira o estado da vigia também no histórico, e o último estado pode ficar velho se o
  programa parar sem aviso. Não foram testados: muitas horas seguidas, queda e volta, vários Codex abertos, o Codex dentro
  do Maestri e a aba do terminal mostrando o título.

Para publicar o comentário na issue do Codex (#20244): o `gh` não está instalado nesta máquina, e o texto mudou com o
teste. O texto novo, em inglês, reconhece o caminho que passou e pede um item de estado próprio, sem renomear a conversa.

## A vigia na tela do Codex
id: vigia-codex
tipo: escolha
recomendada: A

- A: Fica como decidido na rodada anterior: a vigia na checagem de início e a notificação do Windows no fim de cada turno quando há divergência. O caminho pelo servidor compartilhado fica guardado como reserva, documentado com o teste, até o Codex ter um item de estado próprio
- B: O kit adota o servidor compartilhado: o Codex do hub abre sempre ligado a ele, e um programa ao lado põe o estado da vigia no rodapé e no título. Mais construção e mais uma peça viva em cada máquina; a construção testa as horas seguidas, a queda e o Maestri

## O comentário na issue do Codex
id: comentario-20244
tipo: escolha
recomendada: A

- A: Você publica: o maestro deixa o texto novo pronto num arquivo para você colar na issue #20244, na sua conta
- B: O maestro instala o `gh` (winget), você faz o login uma vez (`! gh auth login` neste terminal), e o maestro publica o texto novo e mostra o link
- C: Não publica: o pedido fica só no radar, e o maestro confere a #20244 quando o Codex for atualizado

## Algo mais?
id: algo-mais
tipo: texto
