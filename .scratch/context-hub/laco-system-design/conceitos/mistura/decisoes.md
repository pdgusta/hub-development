# Decisões da mistura (o que decidi sozinho onde caberia pergunta)

Fonte: `descricao/descricao-do-hub.md`, v3.2.

1. **Cor da linha = quem aciona** (agentes, Gustavo, maestro). Volta 2: a legenda separa "quem aciona" de "o que corre"
   (regras, agendador, confere, disco e banco, troca), como o UX revisor pediu.
2. **Dono só na ficha.** O dono é o Gustavo em quase tudo (seção 4, regra do dono). Desenhar isso em cada componente
   repetiria o mesmo nome; vai na ficha de cada componente, no título ao passar o mouse e na frase da ficha "Quem
   chega".
3. **Bairros = os nove grupos da seção 5.1**, cada componente no grupo principal e uma bolinha com a cor do segundo
   grupo. Entraram "Interfaces do Gustavo" e "Ferramentas da máquina"; o Obsidian foi para Interfaces (o principal dele
   na tabela de 5.1). O desenho é por grupo; o lugar fica na ficha (regra "lugar × grupo").
4. **Teto de 25 rótulos:** 9 bairros + 3 pessoas + 13 componentes. Para caber:
   - o **Agendador do Windows** é um relógio sem rótulo, com nome no título e na ficha da Periferia. É ele que tira a
     vigia e o sincronizador do "solto";
   - sem nomes de linha ("buscar", "gravar") e sem a etiqueta "a decidir" no desenho. A legenda, fora do desenho, diz
     o que é cada cor, o tracejado sobre amarelo (a decidir) e o contorno tracejado (a construir); as fichas trazem
     cada selo por extenso;
   - Raiz e os outros componentes do Conteúdo ficam na ficha.
5. **Linha direta do plugin ao banco fora da visão geral.** O desenho mostra o caminho da prática: o Obsidian grava no
   disco e o sincronizador leva ao banco. Que o plugin também pode levar (o primeiro que vir) está no passo 3 do
   cenário e na ficha do Núcleo.
6. **Gravar direto no disco** (agentes → Vista Markdown) aparece tracejado sobre amarelo: é permitido, mas se é o
   caminho padrão está em aberto ("Como os agentes gravam no hub").
7. **Porta do banco com contorno tracejado** ("a construir"): a guarda de versão e o aviso de conflito estão decididos,
   mas não construídos (regra 1 da descrição: mostrar como prevista).
8. **Os avisos da vigia ao Gustavo não têm linha.** Uma linha da torre até ele cruzaria a do agendador; o aviso aparece
   no último passo dos cenários de colisão e na ficha da Vigilância (quem só vê).
9. **Checagem de sessão, script do `_archive/`, biblioteca do Maestri e hook de uso não têm prédio.** Nos cenários,
   o passo deles acende o bairro e, na volta 2, também uma linha ou o componente vizinho; o número vai no componente,
   não no nome do bairro.
10. **Rodada 8, confirmada pela v3.2:** o Obsidian ganhou linha até a busca (como ele chega lá: não verificado); o
    Claude Desktop usa a busca (na ficha; por onde: a decidir); recuperar pela cópia do GitHub é por um agente com o
    Gustavo vendo ou por um comando, até dois dias de distância; conteúdo de cliente pode ir aos modelos na nuvem (na
    ficha de Fora do par).
11. **Sete cenários**, não cinco: "pedir a um agente" virou três (ler, alterar, remover), porque os caminhos diferem.
    "Remover" é arquivar por 30 dias (a descrição, 8.7).
12. **O passo do cenário é uma frase curta numa faixa fora do desenho**, com o número no desenho. Nada de texto corrido
    dentro do SVG.
13. **Fora do par:** a miniatura do outro par ficou menor (24%) para a estrada e o nome "Rede privada" ficarem livres.

## Volta 2

14. **Checkpoint → Agentes saiu do desenho** (fica na ficha). O Tech lead deu duas saídas: a roxa só até o agente, ou um
    traço "confere" até a nota. Fiquei com a segunda, porque a linha azul nova (Agentes → Nota de retomada) precisa
    subir pela coluna dos agentes, e com a roxa do checkpoint ali haveria cruzamento ou os dois roxos colados que o UX
    revisor apontou. Resultado: um roxo só chega aos agentes (o contrato), e a nota recebe o azul de quem grava e o
    tracejado de quem confere.
    Acabamento: a roxa Checkpoint → Agentes voltou só no cenário ("agente novo" 6 e "altere" 6), como a do maestro à
    biblioteca.
15. **Ligações só no cenário.** Maestro → Biblioteca do Maestri e Maestro → Gustavo (pedido de aval) só aparecem
    quando o cenário do maestro as acende; no acabamento, também Checkpoint → Agentes. Na visão geral não há caminho sem cruzar: correm por fora da cidade, uma pela
    esquerda, a outra por cima e pela direita. O Tech lead admite isso ("se não couber na visão geral, a linha existe só
    no cenário"). A medição conta só as linhas visíveis.
16. **O aval vai do Maestro ao Gustavo, não do Acervo.** Uma linha do Acervo ao Gustavo cruzaria a do maestro à
    biblioteca. A descrição dá esse caminho (7.3: o maestro "pede aval, com a tela"; 4.6).
17. **Sem linha Agentes → Periferia do par.** O pedido do UX revisor (para o script do `_archive/`) não virou linha: não há ligação na descrição do agente à periferia, e o Tech lead pediu, para o
    mesmo passo, a troca entre pares (o script lê o estado do outro par). Segui o Tech lead (a descrição, 4.3).
18. **Cor do maestro: verde-azulado.** Para não correr ao lado do roxo das regras perto do Maestro. O roxo ficou para o
    contrato.
19. **A vigia e o checkpoint usam o mesmo traço "confere"** (tracejado escuro, fino). Com isso a vigia deixou de ter cor
    própria: são 7 tipos de traço em vez de 8.
20. **Claude Desktop sem marca no desenho** (conserto opcional do Tech lead): uma marca sem linha seria um componente
    solto; ele fica na ficha "Quem chega", com as duas ligações dele.
21. **No modo cenário, a legenda e os botões dão lugar à faixa do passo**, e a cidade encolhe para caber na altura da
    janela. Conferido a 1280 x 720 e a 1280 x 1000. A 320, a faixa do desenho rola até o número do passo atual.
