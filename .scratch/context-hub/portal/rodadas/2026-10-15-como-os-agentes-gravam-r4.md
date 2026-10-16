---
titulo: O aviso de leitura grande, quando o agente já buscou
ticket: 11
aberta: 2026-10-15
estado: absorvida
---

Você escolheu o meio-termo: um hook avisa, sem recusar, quando o agente abre um arquivo grande do hub sem ter buscado
antes. E perguntou o que acontece quando ele já buscou. Esta é a última pergunta do ticket.

**Como o hook sabe:** ele guarda, num arquivo da sessão, o que a busca devolveu e o que o agente já abriu. No Claude
Code, o hook depois da ferramenta recebe a resposta da busca (o MCP) e o hook antes da leitura vê se ela pede o arquivo
inteiro ou só um trecho (a leitura aceita início e quantidade de linhas). Fonte: documentação de hooks do Claude Code
("PostToolUse... The input includes both `tool_input`... and `tool_response`").

**Para que serve o aviso:** economizar tokens. A busca devolve o trecho certo; o desperdício é ler inteiro um arquivo
grande (a ficha da VOEGOL no vault tem 337 mil caracteres) quando o trecho bastava.

**Não verificado:** no Codex e no Copilot, a leitura passa por comando de shell, e reconhecer uma leitura dentro de um
comando não é confiável; lá o aviso pode falhar em silêncio.

## Quando o agente já buscou
id: ja-buscou
tipo: escolha
recomendada: C

- A: O que conta é de onde veio o arquivo: se alguma busca da sessão devolveu aquele arquivo, abrir passa calado, mesmo inteiro; se nenhuma devolveu, o aviso "busque antes" aparece. Uma vez por arquivo por sessão
- B: O que conta é o jeito de ler: abrir inteiro um arquivo grande avisa "leia só o trecho", tenha buscado ou não; ler um trecho passa calado. Uma vez por arquivo por sessão
- C: Os dois: veio da busca e lê um trecho, passa calado; veio da busca e lê inteiro um arquivo grande, avisa "leia o trecho que a busca apontou"; não veio de nenhuma busca, avisa "busque antes". Uma vez por arquivo por sessão

## Algo mais?
id: algo-mais
tipo: texto
