import sys, os
V = sys.argv[1]
def rep(p, pares):
    p = os.path.join(V, p)
    s = open(p, encoding='utf-8').read()
    for a, b in pares:
        assert s.count(a) == 1, (p, a[:60], s.count(a))
        s = s.replace(a, b)
    open(p, 'w', encoding='utf-8', newline='\n').write(s)

rep('conceito-a.md', [("# Conceito A: Linhas do hub (volta 2)", "# Conceito A: Linhas do hub (volta 3)")])
rep('conceito-b.md', [
 ("# Conceito B: Duas cidades e a estrada (volta 2)", "# Conceito B: Duas cidades e a estrada (volta 3)"),
 ("| Raiz | as seis raízes do conteúdo | um quarteirão com seis telhados | seis, cada uma com seu comportamento, num lugar só |",
  "| Raiz | as seis raízes do conteúdo | um quarteirão de seis casinhas encostadas, cada uma com seu telhado e sua altura | seis lugares distintos, cada um com seu comportamento, num quarteirão só |"),
 ("| Vigia do sync | confere a cada 5 min e avisa | torre de vigia ao lado do cofre | vê o cofre de cima, não guarda nada |",
  "| Vigia do sync | confere a cada 5 min e avisa | torre de vigia (haste e guarita com janela) ao lado do cofre | vê o cofre de cima, não guarda nada |"),
 ("| Obsidian | ver, editar, resolver conflito; pode ficar fechado | oficina de telhado em serra, na periferia | fechada, a cidade segue |",
  "| Obsidian | ver, editar, resolver conflito; pode ficar fechado | oficina pequena de telhado de duas águas, com porta e janela, na periferia | uma bancada que pode fechar, não algo que produz; fechada, a cidade segue |"),
 ("| Rede privada | o único caminho entre pares | a estrada deitada entre as cidades, na altura da rua | nada sai por outro lado; a rua de troca segue por ela |",
  "| Rede privada | o único caminho entre pares | a estrada deitada de muralha a muralha, na altura da rua | nada sai por outro lado; a rua de troca segue por ela |"),
 ("| Par B | o outro par, igual a este | a outra cidade em miniatura: a mesma muralha e os mesmos quarteirões, na mesma disposição | nenhuma é a central; a rua de troca liga cofre a cofre |",
  "| Par B | o outro par, igual a este | a outra cidade em miniatura: a mesma muralha e os mesmos quarteirões, na mesma disposição e com as mesmas cores, mais claras | nenhuma é a central; a rua de troca liga cofre a cofre |"),
])
rep('conceito-c.md', [
 ("# Conceito C: A cidade em corte (volta 2)", "# Conceito C: A cidade em corte (volta 3)"),
 ("""a vigia olha do alto da torre.
""", """a vigia olha do alto da torre.

Na volta 3: um poço tracejado desce da porta da busca até a laje do Conteúdo (forma, não ligação, sem rótulo), para a
busca se ler como a entrada do conteúdo sem decidir onde ela mora. O Maestro chega pela rua, como as outras pessoas, e
desce pela lateral do prédio; o Checkpoint desce por um poço de serviço à direita. Nenhum traço atravessa um andar
onde não para.
"""),
 ("| Maestro | começa pelo acervo do maestro | chega do alto e desce direto à sala do acervo | um destino só |",
  "| Maestro | começa pelo acervo do maestro | chega pela rua, à esquerda, e desce pela lateral do prédio até a sala do acervo | gente chega pela rua; um destino só |"),
 ("| Camada de busca | o agente chega ao conteúdo por ela; onde mora: a decidir (no disco, ou índice dentro da porta do banco) | porta da rua, tracejada, sem seta | é por ela que se entra para achar o conteúdo; sem seta e tracejada, porque a morada dela está em teste |",
  "| Camada de busca | o agente chega ao conteúdo por ela; onde mora: a decidir (no disco, ou índice dentro da porta do banco) | porta da rua, tracejada, sem seta, com um poço tracejado que desce até o andar do Conteúdo | é por ela que se entra para achar o conteúdo; o poço mostra o caminho, e as duas moradas em teste ficam ambas abaixo do térreo |"),
 ("| Checkpoint | ao fim de cada resposta, mantém a nota de retomada em dia | posto no andar de cima, com um cabo que desce até a nota | grava sem pedido, de cima para o conteúdo |",
  "| Checkpoint | ao fim de cada resposta, mantém a nota de retomada em dia | posto no andar de cima, com um cabo que desce pelo poço de serviço até a nota | grava sem pedido, de cima para o conteúdo, sem passar pelas portas |"),
])

p = os.path.join(V, 'decisoes.md')
s = open(p, encoding='utf-8').read()
s = s.replace("Itens 1 a 15: volta 1. Itens 16 em diante: volta 2.", "Itens 1 a 15: volta 1. Itens 16 a 25: volta 2. Itens 26 em diante: volta 3.", 1)
s = s.replace("Medi os três com", """26. **Foco das pessoas: anel com fundo amarelo.** Ao focar ou passar o mouse, aparece em volta da figura um retângulo
    arredondado de traço escuro (2,5 px) com fundo amarelo-claro. O anel fica sempre no desenho, transparente, para a
    caixa da pessoa não mudar de tamanho entre o estado normal e o focado.
27. **No C, o Maestro chega pela rua da esquerda, ao lado dos agentes, e desce pela lateral do prédio** (a segunda saída
    do Tech lead). Um acesso próprio na faixa das portas cruzaria a linha da Porta do banco. Para a lateral funcionar,
    o Acervo do maestro foi para a ponta esquerda do Conteúdo, com o nome em cima.
28. **No C, o Checkpoint desce por um poço de serviço à direita do prédio** (conserto do UX revisor). Para o poço não
    cruzar a linha da vigia, a torre passou para a rua, entre o prédio e a oficina.
29. **No C, o poço da busca é tracejado e claro, sem `data-ligacao` nem rótulo,** e para na laje do Conteúdo.
30. **O ⊕ sempre antes do nome.** Os nomes de bairro que estavam alinhados à direita (Periferia e Fora do par no B)
    agora começam à esquerda, como os outros.
31. **Conferência com Tab real** feita por um script meu, que manda a tecla Tab pelo protocolo de depuração do Edge
    (perfil próprio, fechado no fim). As 10 paradas de cada conceito casam `:focus-visible`; nos bairros o contorno
    fica escuro e com 3,5 px; nas pessoas, o anel aparece.

Medi os três com""", 1)
open(p, 'w', encoding='utf-8', newline='\n').write(s)
print('ok')
