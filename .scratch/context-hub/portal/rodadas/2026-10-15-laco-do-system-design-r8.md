---
titulo: Mais três perguntas da sua prática
ticket: 56
aberta: 2026-10-15
estado: absorvida
---

As suas 14 respostas da rodada anterior já estão com o Tech lead para a terceira versão da descrição do hub. Ao reescrever,
ele achou mais três coisas que só você sabe. Responda com poucas palavras; a que ficar em branco segue marcada "a decidir
com o Gustavo". Abrir a explicação mostra por que cada uma muda o desenho.

## Você mesmo busca no hub (pelo Obsidian ou pedindo a um agente), ou a busca fica só para os agentes? E o Claude Desktop deve usar a busca do hub?
id: g15
tipo: texto

a busca escolhida (obsidian-hybrid-search, servida aos agentes e aos clientes) não tem hoje um caminho para você nem para o Claude Desktop. Na rodada de "Como os agentes gravam" ficou decidido que o Desktop grava pela pasta conectada e pelo MCP do banco, mas não se ele também busca. Se você ou o Desktop usam a busca, ela ganha mais uma porta (a ponte do Desktop até ela), e a matriz de quem usa o quê muda.

## Quando algo é apagado sem querer (por você no Obsidian ou por um agente fora da regra do `_archive/`), quem recupera: você, pela cópia do GitHub, ou um agente com você vendo? Um dia de distância na cópia basta?
id: g16
tipo: texto

o `_archive/` de 30 dias que você definiu cobre a remoção pedida. A exclusão por engano não passa por ele: ela viaja às duas máquinas em segundos, e o único caminho de volta descrito hoje é a cópia diária no GitHub. As fontes não dizem quem roda a recuperação nem se perder até um dia de trabalho é aceitável.

## Você aceita que conteúdo de cliente vá para os modelos na nuvem que os agentes usam (Claude, Codex, Copilot)? Há iniciativa de cliente que não pode?
id: g17
tipo: texto

na rodada anterior você liberou o cliente no repositório privado do GitHub, mas a parte dos modelos na nuvem ficou sem resposta. Todo texto que um agente lê vai ao provedor do modelo; uma iniciativa que não pode exige uma pasta fora do alcance dos agentes ou um modelo local.
