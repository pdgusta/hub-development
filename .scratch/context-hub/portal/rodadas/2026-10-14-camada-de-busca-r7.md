---
titulo: Onde a busca do hub mora
ticket: 09
aberta: 2026-10-14
estado: absorvida
---

A decisão principal da "Camada de busca", com o que o teste de bancada já mediu. Qual modelo de embeddings usar
fica para a pesquisa nova de modelos, e vale igual para as duas opções.

Em que esta rodada se apoia, já decidido:
- a busca é a porta de entrada do agente ("Lições do vault");
- a verdade mora no CouchDB de cada máquina, e o CLI do LiveSync mantém a vista `.md` viva no disco mesmo com o
  Obsidian fechado ("Revisão do sync e da divergência");
- clientes (sandbox, máquina de passagem) usam o MCP de um par pela tailnet, só de leitura ("Onde o servidor mora");
- gravar vai pelo MCP do banco, não pela busca (rodada 4 deste ticket);
- a busca acha texto (`.md`, `.txt`, `.csv`); Word, PDF e planilha contam ponto (rodada 4).

O que o teste de bancada mediu, com 40 perguntas sobre o conteúdo real:
- **As duas ferramentas prontas empatam:** obsidian-hybrid-search acertou 75% nos 5 primeiros, e memtomem, 80%.
  A diferença está no ruído (cada pergunta vale 2,5 pontos).
- **O ponto fraco é o mesmo nas duas:** pergunta com as palavras do texto acerta de 90% a 95%; escrita com outras
  palavras ("anotações" por vault), de 45% a 65%. Isso é sinônimo, que embeddings melhores resolvem e que um
  analisador de português não resolve.
- **obsidian-hybrid-search:** reindexa uma rajada de 200 arquivos em até 147 s, ocupa ~100 MB parado, e o índice
  (um arquivo com ponto na raiz) não vai ao banco, como deve ser. Pulou 12 anexos com YAML inválido.
- **memtomem:** o vigia dele só funciona com um cliente MCP conectado; parado, ocupa 372 MB com o e5.

## Onde a busca mora
id: onde
tipo: escolha
recomendada: A

- A: Leve com alcance: uma ferramenta pronta no disco de cada máquina, e um proxy de MCP (TBXark/mcp-proxy ou 1MCP) que junta a busca e o MCP do banco num endereço só na tailnet, para os clientes. Cerca de 0,5 a 1 dia além da instalação
- B: Robusta: um índice próprio dentro do MCP do banco, em Node (o MCP do es617 é TypeScript), com português léxico (Orama com stemmer `pt`) e vetores (sqlite-vec), alimentado pelas mudanças do CouchDB. Estimativa de 5 a 8 dias, não medida, com um protótipo de 1 dia antes
- C: Começar com A e fazer já o protótipo de 1 dia de B, para comparar os dois no mesmo teste antes de fechar

Por que A: a síntese da pesquisa ampla disse "se a ferramenta pronta acertar bem em português, Leve com alcance".
Ela acerta bem nas perguntas com as palavras do texto, e o que falha (sinônimos) falharia igual na Robusta, porque
o stemmer de português junta "busca" e "buscas", não "anotações" e "vault". Quem resolve sinônimo é o embedding,
que serve às duas opções. A B só ganha quando a busca precisar ver a gravação na hora, ou os clientes precisarem
da mesma busca sem proxy; isso fica no radar, com esses gatilhos.

**Não verificado na A:** se o proxy repassa ferramentas stdio no Windows, e a latência pela tailnet. São o primeiro
teste da construção.

## Qual ferramenta pronta, se for A ou C
id: ferramenta
tipo: escolha
recomendada: ohs

- ohs: obsidian-hybrid-search
- memtomem: memtomem

Por que obsidian-hybrid-search: a qualidade empata, mas ele reindexa sozinho sem cliente conectado, ocupa menos
memória parado e o índice fica fora do banco sem regra extra. O memtomem precisa de um cliente MCP aberto para
vigiar o disco, o que não serve a um par sempre ligado.

## Algo mais?
id: algo-mais
tipo: texto
