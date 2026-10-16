# Laço da descrição do hub: plano de execução

Maestro, 2026-10-15, depois da rodada 6 (caminho A; envio `3d827fb8-dafe-44ed-b2b2-f1653dd9ea3f`). A proposta está em
`proposta.md`; aqui ficam quem faz o quê e os limites. Tudo em segundo plano, sem painel.

## Limites do Gustavo

- **Subagentes Haiku 5.5, esforço alto:** tokens ilimitados, até 2 h, no máximo 20 por lote. Os lotes são do maestro
  (abaixo).
- **FreeLLMAPI:** 20 workers, até 40 mil tentativas, para depois de duas ondas seguidas com 15% ou menos de perguntas
  novas (contando a última), ou em 2 h.

## Etapas

| # | Etapa | Quem | Saída |
|---|---|---|---|
| 1a | Perguntas pelo gateway: geradores com lente e tipo, em ondas, até a saturação | FreeLLMAPI (scripts montados por um subagente Opus médio) | `perguntas/gateway/` |
| 1b | Perguntas pelas fontes: cada Haiku lê as fontes de uma lente e escreve perguntas | lote 1 de Haiku (12) | `perguntas/haiku/<lente>.jsonl` |
| 2 | Juntar, tirar repetidas (por sentido), sortear as duas metades por tipo | maestro (script) | `perguntas/visiveis.jsonl`, `perguntas/escondidas.jsonl` |
| 3 | Escrever a descrição nos sete eixos, a partir das fontes e da metade visível; listar o que só o Gustavo sabe | Tech lead | `descricao-do-hub.md`, `perguntas-ao-gustavo.md` (vira rodada) |
| 4 | Responder às escondidas lendo só a descrição | lote 2 de Haiku (10) e modelos do FreeLLMAPI | `teste/respostas/` |
| 5 | Julgar cada resposta contra as fontes: certa, errada, "a descrição não diz" | lote 3 de Haiku (10), conferência do Tech lead nas falhas | `teste/julgamento.jsonl`, `teste/resumo.md` |
| 6 | Três diagramas só a partir da descrição: sequência de um cenário, matriz de responsabilidade, mapa de grupos | lote 4 de Haiku (3) | `teste/diagramas/` |
| 7 | Consertos por eixo; repetir 3 a 6 até 3 voltas, ou até erro e "não diz" ficarem baixos | Tech lead | nova versão da descrição |
| 8 | Conceito da mistura (a B com a responsabilidade da A), feito da descrição nova; porta como antes | UI engineer, QA, UX revisor, Tech lead | `conceitos/mistura/` |

A metade escondida nunca é aberta pelo Tech lead nem pelo UI engineer. Quem escreve a descrição não vê as perguntas
do teste.

## Lentes (as mesmas nos dois geradores)

O Gustavo no dia a dia; um agente de código novo numa sessão; o maestro do Maestri; o outro par; um cliente (sandbox
ou outro computador); as falhas e a divergência; a segurança e o dado de cliente; quem é responsável por quê; os grupos
lógicos e onde cada coisa vive; a vida de uma nota (nascer, mudar, arquivar); um leitor que nunca viu o hub; quem vai
construir o hub.

## Tipos de pergunta

"Se X, o que acontece?"; "qual a relação entre X e Y?"; "quem é responsável por X?"; "X faz parte do grupo de Y?";
"onde X vive?"; "quem vê ou usa X?"; "o que X não faz?"; "em que ordem?"; "e se X falhar?"; "quando X acontece?"; "por
que X existe?"; "o que muda entre X e Y?".

As cinco perguntas do Gustavo (rodada 5) entram como semente nos dois geradores.
