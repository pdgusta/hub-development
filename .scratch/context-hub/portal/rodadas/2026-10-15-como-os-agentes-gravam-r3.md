---
titulo: A busca como porta de leitura, e a gravação com o banco fora
ticket: 11
aberta: 2026-10-15
estado: absorvida
---

Com a gravação decidida (troca de trecho no disco, regravação inteira pelo MCP do banco, hook que recusa a regravação
no disco), sobram duas perguntas para este ticket se resolver.

Em que esta rodada se apoia, já decidido:
- a busca é a porta de entrada, não a única porta ("Lições do vault"); o agente também lê e edita direto no disco
  (critério 3 do destino);
- a busca (obsidian-hybrid-search) só lê; gravar vai pelo disco ou pelo MCP do banco ("Camada de busca" e a rodada 2
  deste ticket);
- uma sessão fora do hub, como cliente, só chega ao hub pela busca e pelo MCP do banco (sem disco);
- falha se corrige com mecanismo, não com regra a lembrar ("Lições do vault").

**A "luva anticongelamento"** é uma ideia sua de 2026-10-01: o agente só consultaria o hub pela busca, sem ler os
arquivos como quiser, para economizar tokens. Você mesmo duvidou na hora: "talvez o ganho seja só com arquivos muito
grandes ou em grande quantidade".

**A porta do banco fora do ar** é uma das lacunas que a descrição do hub listou: se o MCP do banco cai, a troca de trecho
no disco segue funcionando, mas a regravação inteira não tem por onde ir, porque o hook a recusa no disco.

## A busca é a única porta de leitura?
id: luva
tipo: escolha
recomendada: A

- A: Não. A busca é a porta de entrada: o contrato manda buscar antes de abrir arquivos e ler só o trecho que importa, e o agente pode ler no disco o que a busca apontou. Sem hook de leitura
- B: Meio-termo: um hook avisa (sem recusar) quando o agente abre um arquivo grande do hub, acima de um tamanho que a construção mede, sem ter buscado antes na sessão
- C: Sim, porta única: um hook recusa a leitura de `.md` do hub fora da busca. Os agentes leem só trechos, e o que não está na busca (anexos sem texto extraído, imagens) fica fora do alcance deles

## O que o agente faz quando a porta do banco está fora do ar
id: banco-fora
tipo: escolha
recomendada: A

- A: A troca de trecho segue no disco, como sempre; a regravação inteira espera a porta voltar: o agente avisa você na resposta e anota a pendência na nota de retomada. Nenhuma gravação sem guarda de versão
- B: O hook libera a regravação inteira no disco enquanto a porta estiver fora e registra cada uma num log para conferir depois. O trabalho não para, mas essas gravações não conferem a versão
- C: O agente refaz a regravação inteira como uma sequência de trocas de trecho no disco, cada uma conferida pelo próprio trecho. Funciona na maioria dos casos; em arquivo muito mudado, vira muitas trocas

## Algo mais?
id: algo-mais
tipo: texto
