# Brief da mistura: um conceito de cidade a partir da descrição nova

Do maestro ao UI engineer, 2026-10-15. Etapa 8 do plano (`descricao/plano.md`) e passo 6 da proposta
(`descricao/proposta.md`).

## O que o Gustavo decidiu (rodada 5, resumo fiel)

- **Direção = mistura:** o **conceito B** ("Duas cidades e a estrada", `conceitos/final/conceito-b.*`) é a base; do
  **conceito A** ("Linhas do hub", `conceitos/final/conceito-a.*`) vem o que ele representa melhor: **quem acessa ou é
  responsável por** cada componente.
- Na B, alguns componentes ficam **soltos no meio da cidade**, sem quem os aciona ou responde por eles.
- O desenho tem de mostrar **o que acontece na prática**, não só o que o texto técnico diz. Ele deu dois exemplos do
  erro (a linha dele indo direto ao banco, quando ele edita a vista Markdown; a "disciplina do agente" solta, sem ligação
  ao agente), mas pediu que eles **não** sejam tratados um a um: a fonte certa agora é a descrição nova, feita para
  servir a qualquer diagrama.
- O system design deve responder, **sem texto corrido no desenho**, perguntas como: se o Gustavo edita um arquivo, o
  que acontece; se um agente novo inicia sessão; se um maestro novo inicia sessão; se o Gustavo pede a um agente ler,
  alterar ou remover um arquivo; se o outro par altera um arquivo; e "qual a relação entre X e Y", "quem é responsável
  por X", "X faz parte do grupo de Y".

## Conteúdo

- **Só da descrição nova:** `descricao/descricao-do-hub.md` (v3.1; o Tech lead está fechando, eu aviso quando estiver
  pronta). Ela substitui o `texto-do-hub.md`. Componentes da seção 3, a matriz de responsabilidade da seção 4, os grupos,
  as ações e os cenários. Não leia nada de `descricao/teste/` nem de `descricao/perguntas/`.
- Todo componente tem dono e quem o aciona visíveis (na visão geral ou a um clique); nenhum componente solto.
- **Cenário sem texto:** a cidade ganha um jeito de responder a um cenário acendendo o caminho (ex.: escolher "o Gustavo
  edita um arquivo" e ver o trajeto aceso, passo a passo). Pelo menos os cinco cenários acima. A forma é sua.
- Itens que a descrição marca "[A]" (a decidir) ou "[G, n]" (pergunta ao Gustavo) vão com o selo "a decidir".
- "Componentes", nunca "peças".

## Régua e forma

- Leia de novo a skill `regua-da-cidade` (`laco-system-design/suite/skills/regua-da-cidade/`: `regras.md`,
  `como-julgar.md`, `referencias/`). Teto de 25 rótulos na visão geral;
  o detalhe na ficha. Distância entre os itens; nada de cidade radial com outra roupa.
- Parta do `conceito-b.html` final, com os consertos da volta 3 já aplicados; mantenha a marcação `data-item`,
  `data-grupo`, `data-ligacao`, `data-encontro` e acrescente `data-cenario` nos passos de cada cenário.
- HTML único, CSS e SVG embutidos, sem CDN nem rede; legível em 1280 px e utilizável em 320 px; foco visível com Tab.

## Entrega, em `conceitos/mistura/`

- `mistura.html`; `mistura.md` (a ideia em uma frase, a tabela de papéis, o que veio da B e o que veio da A, como se lê
  um cenário); `decisoes.md` (o que você decidiu sozinho onde caberia pergunta).
- Depois, a porta como antes: o QA mede, o UX revisor e o Tech lead julgam, até 3 voltas; então a carta ao Gustavo.

Ao terminar: `maestri ask "Claude Code" "pronto: <caminho>"`.
