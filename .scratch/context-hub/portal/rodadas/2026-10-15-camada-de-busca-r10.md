---
titulo: Onde a busca mora, depois da comparação
ticket: 09
aberta: 2026-10-15
estado: absorvida
---

Você pediu para comparar as duas opções no mesmo teste antes de fechar. A comparação terminou: as duas rodaram com o
modelo escolhido hoje (arctic-embed-m-v2.0, local), o mesmo corpus e as mesmas 40 perguntas. A nota vai de 0 a 1:
quanto mais perto de 1, mais vezes a nota certa vem no topo. Com 40 perguntas, diferenças de 0,02 a 0,03 são ruído.

Em que esta rodada se apoia, já decidido:
- a busca é a porta de entrada do agente ("Lições do vault");
- a verdade mora no CouchDB de cada máquina, e o CLI do LiveSync mantém a vista `.md` viva no disco com o Obsidian
  fechado ("Revisão do sync e da divergência");
- clientes (sandbox, máquina de passagem) usam o MCP de uma das duas máquinas pela tailnet, só de leitura ("Onde o
  servidor mora");
- gravar vai pelo MCP do banco, não pela busca;
- a ferramenta pronta, se a busca ficar no disco, é o obsidian-hybrid-search (rodada 7 deste ticket);
- o modelo é o arctic, local, e o gemini-embedding-001 pela API entra depois como segunda opção ligável ("Modelos de
  embeddings da busca").

**As duas opções:**
- **Leve com alcance:** o obsidian-hybrid-search lê a vista `.md` no disco de cada máquina.
- **Robusta:** um índice próprio dentro do MCP do banco, que lê o CouchDB cifrado direto.

**O que a comparação mediu:**

| | Leve com alcance | Robusta |
|---|---|---|
| Busca por sentido, mesmas 112 notas | 0,667 | 0,668 |
| Busca mista (palavra e sentido) | 0,632, a melhor da bancada | 0,567, com uma fusão mais simples (a do obsidian-hybrid-search não foi copiada) |
| Busca por palavra (mesmo desenho nas duas) | 0,504 | 0,495 |
| gemini pela API | não medido; o README documenta API compatível com a da OpenAI | medido: 0,728, a melhor nota da bancada, num índice ao lado do arctic |
| Edição até aparecer na busca | não medido; uma rajada de 200 arquivos ficou toda achável em até 147 s | 2,1 s, lendo o banco cifrado |
| Reindexar tudo | 388 s, 1,5 GB de memória | 277 s pelo banco cifrado (com o modelo da fase 1; com o arctic, não medido), 1,7 GB |
| Notas que ficam de fora | 12 de 124, por frontmatter com YAML inválido | nenhuma |
| Como os clientes chegam | o próprio obsidian-hybrid-search serve MCP por HTTP, com opção de abrir para a rede (README); juntar com o MCP do banco num endereço só é do ticket "Acesso dos agentes: decisão" | pelo MCP do banco, que os clientes já usam |
| Construção | ferramenta pronta, instalada em ~1 min | código dentro da versão modificada do MCP do banco, estimado em 5 a 8 dias (não medido) |

**O que mudou desde a rodada 7:** a dúvida de a Leve depender de um repasse de MCP em stdio no Windows caiu, porque o
obsidian-hybrid-search já fala HTTP. A dúvida de a Robusta não ler o banco cifrado também caiu: ela decifra no próprio
Node em 1,3 s, com texto idêntico ao do cofre.

**O que a comparação não fechou:**
- na Leve, rodar o gemini ao lado do arctic: na bancada, o obsidian-hybrid-search ignorou a opção de escolher o arquivo
  do índice, e trocar de modelo pode exigir reindexar tudo;
- na Robusta: que o MCP do banco use as mesmas funções de decifrar (o código dele não foi lido); exclusão, renomeação,
  conflito e binários não exercitados.

**Por que a Leve:**
- a qualidade empatou com o mesmo modelo (0,667 contra 0,668), e a Leve tem a melhor busca mista;
- ela já está pronta, com servidor HTTP próprio;
- o que a Robusta faz melhor (edição em 2 s, gemini já provado) não muda nenhum critério do hub hoje;
- o protótipo da Robusta fica guardado, com os scripts, e volta se um gatilho disparar.

**Por que o idioma por nota:** o FTS5 do SQLite sem stemmer acertou mais que o Orama (outra biblioteca de busca) com stemmer de português. Na
busca por palavra, 0,449 contra 0,211 a 0,355, nas mesmas 124 notas. Nas perguntas com as palavras do texto, 0,95
contra 0,65 a 0,70. A causa não foi investigada: os dois diferem em mais coisas que o stemmer. Hoje o embedding
multilíngue cobre o inglês sem analisador próprio: as 4 perguntas em inglês acertaram todas na busca mista, já com o modelo da fase 1, mais fraco que o arctic. Pela
lição 9 de "Lições do vault", o frontmatter só leva o que a busca ou o contrato usam.

**Por que preparar o gemini:** o teste dele na Leve é justamente o que a comparação não fechou. Fazê-lo uma vez na
construção, sem ligar, mostra se ele roda ao lado do arctic antes de você precisar.

## Onde a busca mora
id: onde
tipo: escolha
recomendada: A

- A: Leve com alcance: o obsidian-hybrid-search com o arctic no disco de cada máquina, servindo a busca por MCP em HTTP na tailnet. O protótipo da Robusta fica guardado como reserva e volta se a busca precisar mostrar uma gravação em segundos, ou se o gemini não rodar ao lado do arctic
- B: Robusta: um índice próprio dentro da versão modificada do MCP do banco (Node, FTS5 do SQLite, sqlite-vec e o arctic), lendo o CouchDB cifrado, com a fusão do obsidian-hybrid-search copiada. Construção estimada em 5 a 8 dias, não medida
- C: Antes de decidir, um teste curto no obsidian-hybrid-search: o gemini pela API num segundo índice ao lado do arctic, e o tempo de uma edição até a busca com o CLI do LiveSync ligado. Custo estimado: 80 a 150 mil tokens de um subagente Sonnet 5.5, mais a cota do Google para uma indexação completa (orçada antes), cerca de 1 a 2 horas

## A busca escolhe o idioma de cada nota?
id: idioma
tipo: escolha
recomendada: A

- A: Não: um analisador só para português e inglês (FTS5 do SQLite, sem stemmer) e o embedding multilíngue. O frontmatter não ganha campo de idioma por causa da busca, e "Arquitetura de pastas e frontmatter" fica livre desse campo
- B: Sim: cada nota ganha um campo de idioma no frontmatter, detectado pelo lingua-py, e a busca escolhe o analisador por ele. Quem grava o campo fica para "Arquitetura de pastas e frontmatter"; a detecção erra mais em texto curto e em nota que mistura os dois idiomas

## Como o gemini fica ligável
id: gemini
tipo: escolha
recomendada: A

- A: Pronto e desligado: a construção escreve a configuração do gemini pelo FreeLLMAPI e a testa uma vez, num índice ao lado do arctic. Ligar fica a seu critério, a qualquer hora; quando ligado, todo o conteúdo indexado vai ao Google, e a busca por sentido passa a depender da rede e da cota do gateway
- B: Sem preparo: a construção entrega só o arctic, e o gemini é montado quando você pedir

## Algo mais?
id: algo-mais
tipo: texto
