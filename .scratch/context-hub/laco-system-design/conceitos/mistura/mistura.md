# Mistura: a cidade e quem a aciona (volta 2)

**A ideia:** a planta da B (a cidade do par dentro da muralha, a estrada e o outro par em miniatura), com as linhas da A
saindo de quem aciona cada componente, na cor de quem aciona; um cenário acende o caminho, passo a passo.

Fonte: `descricao/descricao-do-hub.md` (v3.2), com a rodada 8 do Gustavo (o Gustavo e o Claude Desktop também usam a
busca; recuperar pela cópia do GitHub, por um agente com ele vendo ou por um comando, até dois dias de distância;
conteúdo de cliente pode ir aos modelos na nuvem). A volta 1 está em `mistura-v1.html`; os consertos, em `consertos.md`.

Visão geral: 25 rótulos (9 bairros, 3 pessoas, 13 componentes), 20 ligações visíveis, 0 cruzamentos. Mais três
ligações aparecem só no cenário do maestro (Maestro → Biblioteca do Maestri; Maestro → Gustavo, o pedido de aval), e
uma no fim de resposta do agente (Checkpoint → Agentes: a cancela cobra o agente). O resto está a um clique:
cada bairro abre uma ficha com **dono, quem aciona, quem lê, só vê, aprova e também em** de cada componente (matriz da
seção 4), as ligações do bairro e os selos "a decidir", "a construir", "em curso" e "não verificado". Clicar num
componente abre a ficha do bairro já nele. As pessoas abrem a ficha "Quem chega ao hub" (por onde cada um chega e o
que aciona).

## Tabela de papéis

| Item | Papel no hub (descrição) | Equivalente na cidade | Por que combina |
|---|---|---|---|
| Gustavo | o dono; vê, edita e busca pelo Obsidian; pede a agentes | morador que entra pela porta de trás até a oficina, e que fala com os agentes por fora da muralha | as linhas vermelhas são tudo o que ele aciona: Obsidian, e pelo Obsidian a vista e a busca; e o pedido aos agentes |
| Agentes | sessões de Claude Code, Codex e Copilot | gente fora da muralha, que entra pelos portões | linhas azuis: porta do banco, busca e, tracejado sobre amarelo, o disco direto (a decidir) |
| Maestro | agente que orquestra; começa pelo acervo | visitante que entra por um portão alto e vai ao armazém | a linha magenta vai direto ao acervo; o contrato o manda para lá |
| Contrato | as regras do hub para os agentes | prefeitura | as regras chegam a cada agente e ao maestro por uma linha própria (roxa) |
| Checkpoint | ao fim de cada resposta, obriga o agente a gravar; o hook não grava | cancela de fiscalização | só confere: o traço que sai dela até a nota é o "confere" (tracejado escuro), não o de quem aciona |
| Nota de retomada | onde o trabalho parou; quem grava é o agente da sessão | quadro de recados | a linha azul do agente chega ao quadro; qualquer sessão lê o quadro e continua |
| Acervo do maestro | peças prontas para todo maestro | armazém de porta de enrolar | guarda opções para quem vem buscar |
| Camada de busca | o trecho certo, sem ler tudo; lê a vista | portão largo, de linha grossa, que leva à vitrine | todos chegam ao conteúdo por ela: agentes, o Gustavo pelo Obsidian, o Claude Desktop (na ficha) |
| Porta do banco | lê e grava levando a versão | portão de serviço que dá no cofre; contorno tracejado: a guarda é a construir | leva direto ao banco |
| Banco local | a verdade | cofre (ponto de encontro) | gravar, sincronizar, vigiar e trocar chegam a ele |
| Vista Markdown | os arquivos no disco | vitrine (ponto de encontro) | é o que se vê; o Obsidian grava nela, a busca lê dela |
| Sincronizador | liga disco e banco, nos dois sentidos | casa de máquinas entre a vitrine e o cofre | leva a vitrine ao cofre e o cofre à vitrine |
| Vigia do sync | confere a cada 5 min e avisa | torre de vigia | olha o cofre pelo traço "confere"; não age nele, não guarda nada |
| Agendador do Windows (relógio, sem rótulo) | dispara sincronizador, vigia e cópia diária | relógio da periferia | é quem põe a casa de máquinas e a torre para trabalhar; sem ele, ficariam soltos |
| Obsidian | onde o Gustavo vê, edita, busca e resolve conflito; pode fechar | oficina nas interfaces do Gustavo | uma bancada que pode fechar; fechada, a cidade segue |
| Rede privada | o único caminho entre pares | estrada de muralha a muralha | a troca segue por ela |
| Outro par | a outra máquina, igual | a mesma planta em miniatura | a troca chega ao cofre dela, na mesma altura em que sai do daqui |
| Ferramentas da máquina (bairro), com a configuração (caixa) e a biblioteca do Maestri (caderno), sem rótulo | da ferramenta, não do hub | caixa de ferramentas e caderno de papéis | o maestro vai ao caderno no cenário dele; o nome de cada um vem ao passar o mouse e na ficha |
| Os demais componentes (ficha) | seções 3 e 4 | moradores e serviços do bairro | cada um com dono e quem aciona na ficha |

Bairros: os nove grupos da seção 5.1, cada componente no grupo principal; a bolinha colorida no canto é o segundo
grupo (Contrato também em Conteúdo; Nota de retomada e Acervo também em Disciplina; Obsidian também em Periferia).
"Quem chega" não é bairro: são as pessoas, fora da muralha. O desenho é por grupo; o lugar fica na ficha.

## O que veio da B e o que veio da A

- **Da B:** a planta por lugar dentro da muralha, os quarteirões por bairro, os portões, o cofre, a torre, o armazém, a
  prefeitura, a oficina, a estrada e o outro par como a mesma cidade em miniatura.
- **Da A:** a linha que sai da pessoa e se segue pela cor. Na A a cor era o trajeto; aqui a cor é **quem aciona**. Por
  isso nada fica solto: a disciplina do agente liga ao agente e ao maestro; a vigia e o sincronizador ligam ao
  agendador; o Obsidian liga à vista, não ao banco.
- **Novo:** o traço "confere, só lê", para o checkpoint e a vigia, que olham sem acionar. E o que acontece na prática. O Gustavo edita no Obsidian, o Obsidian grava no disco e o sincronizador leva
  ao banco; o banco não recebe linha direta do Gustavo.

## Como se lê um cenário

1. Escolha um cenário na faixa de cima (sete: o Gustavo edita; agente novo; maestro novo; o Gustavo pede ler, alterar,
   remover; o outro par altera).
2. A cidade apaga; acende só o passo 1, com o número no desenho e uma frase curta na faixa, que fica no lugar dos
   botões e da legenda para a cidade inteira caber na tela.
3. "Próximo" (ou a seta para a direita) acende o passo seguinte; os anteriores ficam acesos, com os números, e o
   trajeto se forma. O passo de falha ou em aberto tem outra marca: triângulo vermelho no lugar do círculo, e o que
   falha fica tracejado ou com brilho vermelho.
4. "Sair" ou Esc volta à visão geral. Cada passo é marcado no código com `data-cenario="<cenário>:<passo>"`.

## O que muda na leitura

- **Em relação à B:** responde "quem aciona isto?" sem abrir nada (siga a linha até a pessoa) e "o que acontece se…?"
  pelo cenário.
- **Em relação à A:** não é só trajeto; o lugar continua contando: vizinhança e quarteirões dizem o grupo.
- **Em relação às recusadas:** sem centro nem anéis; sem texto corrido no desenho (o passo vai numa faixa fora dele);
  o detalhe fica na ficha.
