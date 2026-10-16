---
titulo: O laço do system design
ticket: 56
aberta: 2026-10-15
estado: absorvida
---

Um laço novo, que aparece na página Laços como os outros: dá para ver cada etapa, comentar e pedir mudança por lá.
O Designer coordena; dois especialistas fazem o trabalho pesado; o Prumo revisa o código; você decide nos pontos marcados
"espera você".

**O vídeo:** "Insane Claude Design Skills You Need To Actually Build Beautiful Sites" (canal AI LABS, 12 min 55 s, de
2026-08-24). Ninguém assistiu ainda. A etapa 1 pega a legenda do YouTube (ou, se não houver, transcreve o áudio pelo
FreeLLMAPI) e, como "absorver" pede, vai às fontes primárias das skills e ferramentas que ele citar, não só ao resumo.

**A régua do system design** (da recusa da cidade v2 e da nota no mapa): linhas sem se cruzar, vista mais de cima,
distância entre os itens, nomes que digam o que cada item referencia, e uma cidade em que o papel de cada item faça
sentido. Reinventar a forma, não restilizar a v2.

## As etapas
id: etapas
tipo: proposta

```json
{
  "colunas": ["etapa", "o que faz", "quem", "sai daqui"],
  "linhas": [
    {"id": "video", "etapa": "1. Absorver o vídeo", "o que faz": "legenda ou transcrição; lista das skills e técnicas citadas; leitura da fonte primária de cada uma; o que serve ao Designer e o que não serve", "quem": "Designer (transcrição pelo FreeLLMAPI)", "sai daqui": "relatório do vídeo e uma lista de mudanças propostas para o Designer"},
    {"id": "aval-video", "etapa": "2. Espera você: as mudanças no Designer", "o que faz": "você aceita, corta ou acrescenta mudanças da lista", "quem": "você, numa rodada", "sai daqui": "as mudanças aceitas, aplicadas antes de desenhar"},
    {"id": "insumo", "etapa": "3. Reunir o conteúdo", "o que faz": "as peças do hub e as ligações entre elas, tiradas das decisões já fechadas no mapa, mais a régua acima", "quem": "Designer", "sai daqui": "uma lista do que entra no desenho, com o papel de cada peça"},
    {"id": "conceitos", "etapa": "4. Três conceitos diferentes", "o que faz": "três formas de cidade de verdade diferentes entre si (não variações de cor), cada uma em esboço rápido", "quem": "especialista em system design e diagramas", "sai daqui": "três esboços com uma frase cada"},
    {"id": "critica", "etapa": "5. Crítica de UI e UX", "o que faz": "cada esboço contra a régua: poluição visual, espaço disputado, disposição, separação lógica; nota e defeitos de cada um", "quem": "especialista em UI e UX", "sai daqui": "um parecer por esboço"},
    {"id": "escolha", "etapa": "6. Espera você: qual conceito", "o que faz": "você escolhe um, mistura ou recusa todos (aí volta à etapa 4)", "quem": "você, numa carta no portal", "sai daqui": "o conceito escolhido"},
    {"id": "construir", "etapa": "7. Construir e revisar", "o que faz": "o especialista em diagramas constrói; o de UI e UX revisa sobre capturas reais da tela; o Prumo revisa o código; repete até o de UI e UX aprovar", "quem": "os dois especialistas e o Prumo", "sai daqui": "o system design novo, numa página à parte"},
    {"id": "entrega", "etapa": "8. Espera você: aprovar", "o que faz": "você aprova ou recusa; só com o aprovado o system-design.html é trocado", "quem": "você, numa carta no portal", "sai daqui": "o system design novo no lugar do antigo"}
  ],
  "pode": ["editar", "remover", "adicionar"]
}
```

Mude, tire ou acrescente etapas.

## Quem são os dois especialistas
id: especialistas
tipo: escolha
recomendada: A

- A: Dois recrutas novos, cada um com papel próprio no acervo do maestro ("Especialista em diagramas de system design" e "Especialista em UI e UX"), Claude Opus 5.5 com esforço alto; o Designer coordena. Ficam disponíveis para outros visuais depois
- B: Dois subagentes do Designer, que somem ao fim do laço: mais barato, mas sem papel que fique no acervo
- C: Como a A, mas o de UI e UX roda no Codex (GPT 6.1 Sol), para a crítica vir de outro modelo

## Quantas voltas na etapa 7
id: teto
tipo: escolha
recomendada: A

- A: Até 3 voltas de construir e revisar; se o de UI e UX não aprovar na terceira, para e espera você. Estimativa: uns 600 mil tokens do Claude no laço inteiro (etapas 1 a 8)
- B: Até 5 voltas, uns 900 mil tokens
- C: Sem teto: só para quando o de UI e UX aprovar

## Algo mais?
id: algo-mais
tipo: texto
