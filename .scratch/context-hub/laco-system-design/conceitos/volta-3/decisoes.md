# Decisões (UI engineer, 2026-10-15)

Itens 1 a 15: volta 1. Itens 16 a 25: volta 2. Itens 26 em diante: volta 3.

Pontos em que caberia pergunta e eu decidi sozinho para seguir.

1. **Nota de retomada no bairro Conteúdo.** O texto do hub (3.5) a põe em dois grupos: disciplina do agente e
   conteúdo. Marquei `data-grupo="Conteúdo"`, porque é um arquivo que mora numa raiz; o checkpoint (disciplina) é
   quem grava nela, pela ligação "Checkpoint → Nota de retomada".
2. **Claude Desktop em "Fora do par", não com a gente.** 3.5 o lista no grupo 7 ("Claude Desktop pela ponte"), e a
   frase sobre gente nomeia só Gustavo, agentes e maestro.
3. **Ligação do núcleo partida em dois traços.** A linha "Vista Markdown | Sincronizador ↔ banco local" da seção 4
   virou `Vista Markdown → Sincronizador` e `Sincronizador → Banco local`, para cada traço ter uma ponta só.
4. **Duas ligações vêm da 3.4, não da tabela da seção 4:** `Gustavo → Obsidian` e `Maestro → Acervo do maestro`
   (coluna "Como" de quem chega). Sem elas, gente ficaria solta, sem porta.
5. **"Agentes" no lugar de "Agente".** A seção 4 escreve "Agente"; usei o rótulo da 3.4, "Agentes", em
   `data-ligacao` e no desenho.
6. **Rótulo "Par B".** O outro par não tem linha própria na seção 3; o nome vem da seção 4 ("banco local do par A →
   banco local do par B") e "par" é termo do glossário. A ligação marcada é `Banco local → Par B`.
7. **O que fica fora da visão geral (vai para a ficha do bairro e para o título ao passar o mouse),** para caber em
   25 rótulos. Na volta 1 os três ficaram com 23; na volta 2, com 25 (ver item 16).
   - Nos três: Avisos, Checagem de sessão, Guarda do acervo, Registro de uso, Iniciativa, Pasta não replicada, Cópia
     local (git), Nó da rede, Cópia no GitHub, Cliente, Claude Desktop, Vault (referência), Porta de leitura.
   - Só em A e C fora: Contrato e Raiz. Só em B fora: Checkpoint e Nota de retomada.
   Cada conceito mostra o que a forma dele pede: A, os trajetos; B, os lugares (por isso Raiz e Contrato aparecem);
   C, as faixas de altura.
8. **Ligações que ficam fora da visão geral:** Cliente → Porta de leitura, Claude Desktop → Porta do banco, Agentes →
   Guarda do acervo → Acervo do maestro, Hook de uso → Registro de uso, Vigia do sync → Avisos, Estado curto e nota de
   retomada → Checagem de sessão, Cópia local (git) → Cópia no GitHub, Contrato → configuração de cada ferramenta.
   Todas estão na ficha do bairro. Da linha "Vigia do sync → Banco local, Sincronizador, Obsidian", o desenho mostra
   só o trecho até o banco; a ficha diz os três.
9. **A busca como porta do conteúdo, sem ligação inventada.** A seção 4 não tem "Camada de busca → Conteúdo", então
   não há traço com `data-ligacao` ali. A ideia vai na forma: em A, a estação final da linha buscar fica colada ao
   bairro Conteúdo; em B, uma rua desenhada (forma, não ligação) vai do portão da busca ao bairro; em C, a porta da
   busca é a única que abre para cima, para os andares do conteúdo.
10. **"Vista mais de cima" lida como nível de detalhe.** A régua define pela visão geral (só zonas e ligações
    principais, detalhe numa camada). O conceito C é um corte lateral; se a régua quiser o ângulo literal, C cai.
11. **Nomes das linhas são meus,** tirados dos fluxos da seção 5 (buscar, gravar, sincronizar, troca entre pares,
    vigiar, editar). Ficam só na legenda em HTML, fora do desenho, e não contam como rótulo de item.
12. **"a decidir" com selo e tracejado.** Na visão geral, só a camada de busca aparece com o selo (onde mora, ferramenta
    e modelo, seção 7). Na ficha, os selos marcam todos os assuntos da seção 7 que tocam um componente ou uma ligação
    da peça (lista em `consertos.md`).
13. **Mesmo acabamento nos três.** Mesma paleta, fontes, cores de linha, selo e ficha, para a diferença ficar só na
    forma (teste de troca de acabamento do `parallel-concepts`).
14. **320 px.** O desenho fica numa faixa de 900 px que rola dentro do quadro (a página não rola de lado), e abaixo
    vem a lista dos bairros em botões, que abrem a mesma ficha.
15. **Fontes do sistema** (Georgia e Segoe UI), sem rede. Peso 600 nos rótulos para leitura confortável, como na Mesa
    de mapas.

16. **Nomes das linhas no desenho levam os três a 25 rótulos, o limite.** O UX revisor pediu o nome curto sobre cada
    traço (buscar, gravar). Pus os dois, e só esses dois: as outras linhas seguem só na legenda. Qualquer rótulo a mais
    na visão geral passa do limite; o próximo conserto que pedir texto no desenho tem de tirar outro.
17. **No C, desci o Conteúdo em vez de trocar a chave da altura.** O Tech lead deu duas saídas. Trocar a chave ("a
    altura diz quem age") deixaria o conteúdo no alto, longe do cofre, e o C perderia a ideia dele (quanto mais fundo,
    mais perto da verdade). Descendo o Conteúdo para o primeiro subsolo, a chave vale para tudo. O preço: o andar de
    cima fica só com a disciplina, e a linha da vigia continua longa.
18. **No C, a Porta do banco mantém a seta para baixo.** Ela vai ao banco: isso está decidido (seção 4). Só a Camada de
    busca perdeu a direção, porque a morada dela está em teste.
19. **Nome do bairro em caixa normal, 14 px semibold,** no lugar de caixa alta a 12 ou 13 px. Em caixa alta não cabia
    nos bairros estreitos (Vigilância do B, Disciplina do A).
20. **O sinal de "abre" é desenho, não texto** (⊕ junto do nome do bairro), para não somar rótulo. A legenda diz o que
    ele quer dizer.
21. **No A, a Vigia do sync foi para a direita do bairro Vigilância** e a linha dela entra no Banco local pelo lado
    direito. Com o nome do Núcleo no topo da caixa, uma linha vertical no meio cortaria o nome.
22. **Portão sem nome para o Maestro, no B.** O texto do hub não dá portão ao maestro; desenhei uma abertura na
    muralha, sem rótulo e sem `data-item`, só para a linha não passar por cima do muro.
23. **Par B do B em miniatura a 40%** da planta do par A, com a rua no mesmo nível da rua do par A, para a linha de
    troca seguir reta pela estrada e entrar pela rua dele.
24. **"não verificado" com selo próprio** (cinza-azulado), separado de "a decidir" (amarelo): a seção 7 usa as duas
    palavras para coisas diferentes.
25. **Volta 1 intacta.** Copiei os arquivos e gerei a volta 2 por um gerador novo; nada em `volta-1/` mudou.

26. **Foco das pessoas: anel com fundo amarelo.** Ao focar ou passar o mouse, aparece em volta da figura um retângulo
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

Medi os três com `medidas-da-peca` numa pasta minha (fora de `qa/`), só para conferir antes de entregar. A medição
oficial é do QA.
