# Decisões da volta 1 (UI engineer, 2026-10-15)

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
   25 rótulos. Os três ficam com 23.
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
    e modelo, seção 7). Na ficha, o selo também marca Pasta não replicada, Claude Desktop (se grava) e Guarda do acervo
    (detalhes não verificados).
13. **Mesmo acabamento nos três.** Mesma paleta, fontes, cores de linha, selo e ficha, para a diferença ficar só na
    forma (teste de troca de acabamento do `parallel-concepts`).
14. **320 px.** O desenho fica numa faixa de 900 px que rola dentro do quadro (a página não rola de lado), e abaixo
    vem a lista dos bairros em botões, que abrem a mesma ficha.
15. **Fontes do sistema** (Georgia e Segoe UI), sem rede. Peso 600 nos rótulos para leitura confortável, como na Mesa
    de mapas.

Medi os três com `medidas-da-peca` numa pasta minha (fora de `qa/`), só para conferir antes de entregar. A medição
oficial é do QA.
