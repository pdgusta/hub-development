---
titulo: Acesso dos agentes: teste, porta local, checagem e fim da resposta
ticket: 14
aberta: 2026-10-14
estado: absorvida
---

O ticket decide como cada agente (Claude Code, Codex, Copilot no CLI e no VS Code, Claude Desktop, e recrutas do
Maestri), em cada máquina, recebe o contrato, as skills, o MCP do banco e os dois hooks: o de início de sessão (estado
do sync e nota de retomada) e o de fim da resposta (obriga a gravar a nota).

Muito já está decidido pelos tickets anteriores: o contrato entra pelo arquivo global de cada harness, por link
simbólico; as skills, por junction; o par usa o MCP do banco local com escrita; o cliente usa pela tailnet um MCP só de
leitura, com token. Levantamento completo em `exploracao/anexos/levantamento-14-acesso-dos-agentes.md`.

**Fica para depois, porque depende de outro ticket:**
- qual MCP de busca cada agente carrega e se os clientes passam por um proxy (Camada de busca);
- como o cliente só de leitura grava a nota de retomada, e como o Claude Desktop recebe o contrato (Como os agentes
  gravam no hub).

**O que falta saber:** os hooks de início e de fim só foram lidos na documentação, nunca testados no Codex e no
Copilot. Também não foram testados: o `.git` real substituir o marcador de raiz, o VS Code aceitar um MCP com token, e
a política da empresa barrar o MCP do hub no Copilot.

## Testar o acesso antes de decidir o resto
id: bancada
tipo: escolha
recomendada: A

- A: Um subagente Opus 5.5 médio testa agora, nesta máquina, tudo o que roda por linha de comando: hooks de início e de fim no Codex e no Copilot CLI, o `.git` real numa subpasta e num papel, duas instâncias do MCP do banco, o MCP com token, o contrato carregando em dobro. O que só dá por clique (VS Code e a política da empresa) vira uma lista curta para você. Estimativa de 150 a 250 mil tokens
- B: Só a parte de linha de comando agora; VS Code e política da empresa ficam para a construção
- C: Nenhum teste agora: decido pela documentação e tudo é testado na construção

## O MCP do banco no próprio par
id: porta-local
tipo: escolha
recomendada: A

- A: Preso a 127.0.0.1 e com token, lido de uma variável de ambiente da máquina. Nenhum outro aparelho da rede chega a ele, e um programa local qualquer não grava sem o token
- B: Preso a 127.0.0.1, sem token. Mais simples, mas qualquer programa da máquina grava no banco
- C: Como vem (0.0.0.0, sem token): aceita só pedidos que dizem vir de localhost

## De onde a checagem de início lê o estado do sync
id: checagem
tipo: escolha
recomendada: A

- A: No par, o hook de início lê o arquivo de estado que a vigia grava a cada 5 min (não depende do MCP estar de pé). No cliente, que não tem vigia, o hook pede o estado a uma ferramenta do MCP
- B: Sempre pela ferramenta do MCP, no par e no cliente: um caminho só, mas a checagem falha quando o MCP cai
- C: Só o arquivo da vigia; o cliente fica sem checagem

## O hook de fim da resposta
id: fim
tipo: escolha
recomendada: A

- A: O mesmo script nos três harnesses (Claude Code, Codex, Copilot), sem modelo: confere se a nota de retomada foi tocada nesta resposta e, se não, devolve o agente para gravar. Modelo só entra se o script não bastar
- B: No Claude Code um hook com modelo (ele julga se a nota está boa); no Codex e no Copilot, que não aceitam hook com modelo, o script
- C: Só a regra no contrato, sem hook fora do Claude Code

## O estado da vigia fora do Claude Code
id: vigia
tipo: escolha
recomendada: A

- A: Aceitar: no Codex e no Copilot, o estado aparece só na checagem de início e na notificação do Windows (já decidida). O aviso o tempo todo na tela fica só no Claude Code, pelo mod
- B: Procurar um jeito de mostrar o tempo todo também no Codex e no Copilot (pesquisa a mais)

## Algo mais?
id: algo-mais
tipo: texto
