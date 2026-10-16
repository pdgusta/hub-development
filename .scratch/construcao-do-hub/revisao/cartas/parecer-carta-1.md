# Parecer da carta 1: Gravar e ler no banco (volta 1)

Revisor: Lente, 2026-10-16. Carta: `carta-1-banco.html` (Designer).
Capturas em `capturas-lente/`: `c1-1600-inteira.png` (fatias `-p0` a `-p5`) e `c1-390-inteira.png` (fatias `-p0` a
`-p5`). A largura de 390 px foi capturada dentro de um iframe de 390 px, porque o Edge sem cabeça não abre janela
com menos de uns 480 px.

## Veredito: volta

No computador, a carta é boa. A agência (guichê = MCP do banco, cofre = CouchDB) é uma linguagem própria, de papel
de banco com guilhoché, e não lembra a carta 2. O mapa "A agência" no topo mostra onde cada escolha mora, o que ajuda
muito. Cada escolha tem problema, escolha do spec e alternativa, e o diagrama compara lado a lado ("as duas", "só o
aviso", "só a lista"). O extrato final segue a numeração da rodada. Os fatos estão certos.

A carta volta por causa do celular: lá, os diagramas viram miniatura e a tabela da escolha 3 se desmonta.

## Fatos (spec, acordo seção c, tickets 30 e 48, conversa dos revisores)

Estão certos:
- Escolha 1: o ticket 30 dá "aviso no `read_note` **ou** `get_conflicts`".
- Escolha 2: o bloco é relido a cada `initialize`, antes do texto original, com o corte em 2.048 e a lacuna de dono 5.
- Escolha 3: a frase ① vem do ticket 36. A alternativa "② nas quatro" é a proposta do Prisma na rodada 1.
- Escolha 4: `estado_do_hub` e o "estado indisponível".
- Escolha 5: a alternativa "três" estava nos pontos abertos da faixa 10 ("podem ser três por par"); "os dois juntos:
  não testado" está certo.
- Escolha 6: o caminho cifrado, tamanho e data zerados, os bytes idênticos e os ~2 s vêm do ticket 48.
- Nenhum nome de cliente aparece (só `‹cliente›`).

## Consertos

1. **[obrigatório · celular] Os diagramas viram miniatura.** Em 390 px, o mapa "A agência" e as cenas das escolhas
   1, 2, 4 e 5 encolhem para uns 25% da largura de desenho. O texto fica com 4 a 6 px. A hierarquia se inverte: no
   celular, o texto das três colunas manda e o diagrama vira enfeite (`c1-390-inteira-p0`, `-p1`, `-p3`).
   Conserto: abaixo de 820 px, empilhar as três opções de cada cena (escolha do spec em cima, alternativas embaixo),
   que já são caixas separadas. Para o mapa da agência e a cena do topo de cada escolha, usar uma moldura que rola
   para o lado, com largura mínima de uns 760 px e a dica "arraste". O texto do diagrama precisa de pelo menos 12 px.
2. **[obrigatório · celular] A tabela da escolha 3 se desmonta.** Em 390 px, as quatro colunas viram duas. O
   cabeçalho "escolha do spec" cai ao lado de "ferramenta", e cada ferramenta ganha uma linha de alternativa sem
   rótulo. Não dá para saber qual marca é de qual coluna (`c1-390-inteira-p2`). Conserto: no celular, um bloco por
   ferramenta, com três linhas rotuladas ("escolha do spec: ① ② ✓", "② nas quatro: ① ② ✓", "só ①: ① · a versão, só ao
   ser recusado"). Outra saída: manter a tabela inteira numa moldura que rola para o lado.
3. **[nome] Escolha 6 com dois nomes.** No mapa e no extrato, ela se chama "envelope sem nome". No título da
   seção, é "Cifra de ponta a ponta com o caminho embaralhado", e a palavra "envelope" não aparece na seção. Conserto:
   pôr o mesmo nome curto nos três lugares, por exemplo um sobretítulo "o envelope sem nome" acima do título da seção 6.
4. **[recomendado · hierarquia] O quadro de texto vem antes do desenho.** Em todas as seis seções, o quadro de três
   colunas (problema, escolha do spec, alternativa) chega antes do diagrama, e o olho cai primeiro no texto. O pedido
   do Gustavo é o diagrama no centro e pouco texto. Conserto sugerido: deixar no topo só o problema, em uma linha, e
   pôr a escolha e a alternativa como legenda curta dentro das caixas do diagrama, que já têm os selos "escolha do
   spec" e "alternativa". Se mantiver o quadro, ponha-o abaixo do desenho.
5. **[leve] Os selos "decidido" no meio da frase** quebram a leitura ("pergunta ao MCP [DECIDIDO]. Só o nome…").
   Conserto: levar o selo para o fim da frase, ou trocar por um sublinhado verde com a legenda que já existe no topo.

Depois dos consertos 1 a 3, a carta passa. Os itens 4 e 5 melhoram a leitura, mas não seguram a carta.

---

# Volta 2 (2026-10-16): passa

Capturas: `capturas-lente/c1v2-1600-inteira.png` e `c1v2-390-inteira.png` (com as fatias `-p*`).

Os consertos foram conferidos:
1. Celular: as opções de cada cena se empilham (escolha do spec em cima). O mapa e as cenas do topo ficam numa
   moldura que rola para o lado, com a dica "arraste", e o texto se lê (`c1v2-390-inteira-p0`, `-p1`). **Feito.**
2. Celular: na escolha 3, cada ferramenta virou um bloco com três linhas rotuladas (escolha do spec, ② nas quatro,
   só ①). Agora se lê sem adivinhar (`c1v2-390-inteira-p4`). **Feito.**
3. Escolha 6: "o envelope sem nome" aparece no mapa, no sobretítulo e no extrato. **Feito.**
4. Hierarquia: no topo, só o problema, terminando na pergunta. A escolha e a alternativa ficam abaixo do desenho, e o
   olho cai primeiro no diagrama. **Feito.**
5. O selo "decidido" está no fim da frase decidida. **Feito.**

Ressalva (não segura a carta): no celular, as molduras que rolam começam no canto esquerdo. Por isso, a primeira vista
do mapa da agência mostra só os agentes e o proxy; o MCP do banco e o cofre só aparecem arrastando. Aceitável, porque
a dica está ali.
