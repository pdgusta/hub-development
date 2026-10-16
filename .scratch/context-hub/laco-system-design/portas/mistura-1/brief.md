# Brief da porta da mistura, volta 1

Do maestro, 2026-10-15. Etapa 8 do plano da descrição (`descricao/plano.md`) e etapa 9 do `orquestracao.md`. Peça:
`conceitos/mistura/mistura.html`, com `mistura.md` (ideia, tabela de papéis, o que veio da B e da A, como se lê um
cenário) e `decisoes.md`. Brief do UI engineer: `conceitos/mistura/brief.md`.

## Contexto (para quem chega sem memória)

O Gustavo viu três conceitos de cidade na carta (A "Linhas do hub", B "Duas cidades e a estrada", C "A cidade em
corte"; finais em `conceitos/final/`) e escolheu a **mistura**: a B como base, e da A quem acessa ou é responsável por
cada componente. Ele apontou que na B alguns componentes ficavam soltos, que a linha dele ia direto ao banco quando na
prática ele edita a vista Markdown, e que a "disciplina do agente" aparecia sem ligação ao agente; e pediu que o desenho
responda, sem texto corrido, a cenários como "se o Gustavo edita um arquivo", "se um agente novo inicia sessão", "se um
maestro novo inicia sessão", "se o Gustavo pede a um agente ler, alterar ou remover", "se o outro par altera um arquivo".
Por isso a descrição do hub foi refeita e testada: a fonte agora é **`descricao/descricao-do-hub.md` (v3.2)**, que
substitui o `texto-do-hub.md`.

## Ordem

1. **QA tester** mede primeiro: `medidas-da-peca` na mistura (larguras 320, 768, 1280 e 1920), saída em
   `qa/mistura-1/`, relatório em `qa/mistura-1/relatorio.md`. Inclui os passos `data-cenario`: cada cenário acende o
   caminho e volta ao normal. Só mede e relata.
2. **UX revisor** e **Tech lead** julgam em paralelo, com o relatório do QA na mão, pelo roteiro de
   `suite/skills/regua-da-cidade/como-julgar.md`:
   - **UX revisor:** R1, R2, R3 e R6 sobre capturas próprias (1280 e 320), as seis dimensões das críticas, foco com Tab
     real em todas as paradas e a leitura dos cenários acesos (dá para seguir sem ler texto?). Parecer em
     `portas/mistura-1/ux-revisor.md`.
   - **Tech lead:** R4, R5 e R6 contra a **descrição v3.2**: todo componente com dono e quem aciona visíveis, nenhum
     componente solto; grupos e ligações batem com a descrição; os cinco cenários acendem o caminho que a descrição
     dá, na ordem certa; a busca como porta do conteúdo; o Gustavo chegando pela vista Markdown; itens "[A]" e "[G]"
     com o selo "a decidir"; as respostas [R7] e [R8] refletidas (o Gustavo e o Claude Desktop também usam a busca).
     Parecer em `portas/mistura-1/tech-lead.md`.

## Critério (de `como-julgar.md`)

Passa com R1 a R6 em "passa" e nenhuma dimensão abaixo de 3. Cada parecer termina com **passa** ou **volta** e a lista
de consertos numerada (o que, onde, por quê). Até 3 voltas; depois, a carta ao Gustavo.

Ao terminar, cada um avisa: `maestri ask "Claude Code" "pronto: <caminho do parecer>"`.
