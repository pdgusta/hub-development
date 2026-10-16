---
titulo: Quatro avais antes da hora de construção
ticket: 16
aberta: 2026-10-15
estado: suspensa
---

Os 12 recrutas fecharam na volta 1 um plano com 10 faixas, cada uma com o que entrega e como segue sem esperar as
outras (`.scratch/construcao-do-hub/planejamento/plano.md`). Ficaram quatro perguntas que só você responde. Todas valem
só para a hora de construção, nesta máquina.

## Contêineres de ensaio no Docker
id: docker
tipo: escolha
recomendada: A

- A: Você liga o Docker Desktop antes da hora (agora ele está desligado), e as faixas do banco, do MCP do banco e da vigia sobem cada uma o seu CouchDB descartável em 127.0.0.1, apagado ao fim. Sem tarefa agendada de verdade: o sincronizador e a vigia rodam em laço no terminal
- B: Sem Docker: essas três faixas testam só contra dublês (respostas gravadas) e o banco de verdade fica para outra execução

## Login dos harnesses na pasta de configuração de ensaio
id: login
tipo: escolha
recomendada: A

- A: Copiar só o arquivo de login do Codex e do Copilot para a pasta de configuração de ensaio e apagá-lo ao fim, para provar que os três harnesses leem o contrato, as skills e o MCP de verdade
- B: Sem copiar login: provar só a forma dos arquivos e, onde der, rodar no escopo do projeto, como a bancada fez

## Copiar os pilotos do vault nesta execução
id: pilotos
tipo: escolha
recomendada: A

- A: Sim: `armis-docs`, `armis-brand` e a skill `armis-docx` são copiados do vault para o hub (o vault não muda), pela faixa do esqueleto, depois de ele estar pronto
- B: Não: ficam para outra execução

## Teste do gemini-embedding-001 pelo FreeLLMAPI
id: gemini
tipo: escolha
recomendada: A

- A: Sim, se o Docker for ligado (o FreeLLMAPI roda nele): uma indexação das cerca de 20 notas de ensaio (texto inventado, sem dado de cliente), da ordem de dezenas de chamadas de embedding; depois a configuração fica escrita e desligada
- B: Não: a configuração fica escrita e desligada, sem teste

## Algo mais?
id: algo-mais
tipo: texto
