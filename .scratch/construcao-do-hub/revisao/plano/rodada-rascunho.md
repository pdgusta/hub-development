---
titulo: O plano de construção em etapas
ticket: 16
aberta: 2026-10-16
estado: aberta
carta: plano-de-construcao
---

A carta **"plano-de-construcao"** mostra a construção como uma sequência de etapas, uma depois da outra, e por que cada
uma vem depois da anterior: o que ela usa de verdade do que a outra entregou. A proposta escrita está em
`.scratch/construcao-do-hub/revisao/plano/proposta-de-etapas.md`. Em dois pontos a ordem não fecha sozinha (o MCP do
banco e a vigia se pedem; a vigia lê um item que só a manutenção grava): ali a etapa anterior vai com um exemplo e a
posterior confere com o real, sem mudar a ordem. As perguntas que dependem de cada etapa (login dos
harnesses no ensaio, pilotos do vault, teste do gemini, bancos de ensaio no Docker e as três lacunas de dono) vêm na hora
da etapa que as usa.

## 1. A construção em etapas, nesta ordem
id: ordem
tipo: escolha
recomendada: A

- A: Aceitar: uma etapa por vez, cada uma usando a entrega real da anterior, na ordem esqueleto → banco → MCP do banco → busca → guardas no disco → vigia → retomada → skills e acervo → manutenção e kit de cliente → kit de par → junção
- B: Etapas em sequência, mas com outra ordem (diga qual no "Algo mais?")

## 2. Uma etapa zero de provas de risco
id: etapa-zero
tipo: escolha
recomendada: A

- A: Sim: antes de tudo, testar o que pode derrubar o desenho (dois CouchDB replicando com os documentos do LiveSync; a exclusão de pastas com ponto aninhadas no LiveSync; os hooks do Codex em acesso total)
- B: Não: cada risco é testado dentro da etapa que o usa

## 3. Os ramos da execução de ontem
id: ramos-de-ontem
tipo: escolha
recomendada: A

- A: Guardar como referência (`ontem/faixa-NN`) e recomeçar cada etapa da ponta do ramo de integração, consultando o de ontem quando servir
- B: Continuar dos ramos de ontem onde houver trabalho (esqueleto, retomada, busca, vigia, skills)
- C: Apagar os ramos de ontem

## 4. Como cada etapa é executada
id: receita
tipo: escolha
recomendada: A

- A: Antes de cada etapa, o maestro propõe a receita (quem constrói, quem revisa, qual modelo, quantos no canvas) e você ajusta numa rodada curta
- B: Uma receita padrão fixa para todas as etapas, decidida agora (diga qual no "Algo mais?")

## Algo mais?
id: algo-mais
tipo: texto
