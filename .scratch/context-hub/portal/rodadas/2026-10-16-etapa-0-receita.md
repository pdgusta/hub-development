---
titulo: Etapa zero: a receita
ticket: 16
aberta: 2026-10-16
estado: absorvida
---

A etapa zero testa as três peças que nunca foram provadas e podem derrubar o desenho. Como você pediu, cada prova já
usa a forma de configuração que a construção vai usar e termina com uma seção "o que vai doer ao ligar no resultado
final":

1. **Dois CouchDB replicando entre si com os documentos do LiveSync** (o desenho de um banco em cada máquina).
2. **A exclusão de pastas com ponto aninhadas** (`projeto/.venv/`, `clientes/x/.secrets/`) no LiveSync, que no teste do
   disco e banco vazou.
3. **Os hooks do Codex em acesso total**, o modo decidido no acesso dos agentes (só foram provados no modo restrito).

Tudo roda num hub de ensaio e numa pasta de configuração de ensaio, nunca nos seus arquivos de verdade. O resultado vai
para `.scratch/construcao-do-hub/etapas/00-provas/relatorio.md`, com a evidência de cada prova. Etapa zero e etapa 1
não dependem uma da outra, então o esqueleto pode andar junto, dentro do teto de 3 agentes.

## Quem trabalha na etapa zero
id: receita
tipo: escolha
recomendada: A

- A: Dois construtores Claude Opus 5.5 médio no canvas: um faz as provas 1 e 2 (CouchDB e LiveSync), outro a prova 3 (hooks do Codex); mais um revisor Codex no canvas, que confere o relatório e as evidências. O revisor Codex precisa de acesso total, e você o inicia com um comando que eu passo
- B: Um construtor só para as três provas, mais o revisor Codex (mais lento, menos cota)
- C: Os dois construtores, com revisor Claude no lugar do Codex (sem passo seu, mas o mesmo modelo revisa o que escreveu)

## Adiantar a etapa 1 (esqueleto) em paralelo
id: adiantar-esqueleto
tipo: escolha
recomendada: A

- A: Sim: um terceiro construtor Claude Opus 5.5 médio começa o esqueleto (árvore, `AGENTS.md`, esquemas, verificador e hub de ensaio), que não depende das provas; se uma prova mudar algo dele, ele ajusta antes de juntar
- B: Não: o esqueleto só começa quando a etapa zero fechar

## Bancos de ensaio no Docker
id: docker
tipo: escolha
recomendada: A

- A: Sim: as provas 1 e 2 sobem CouchDB descartáveis em 127.0.0.1 no Docker, apagados ao fim da etapa
- B: Não: a etapa zero fica só com a prova 3, e as provas do banco esperam

## Login do Codex na pasta de configuração de ensaio
id: login-codex
tipo: escolha
recomendada: A

- A: Copiar só o arquivo de login do Codex para a pasta de configuração de ensaio durante a prova 3 e apagá-lo ao fim, para o Codex rodar de verdade com os hooks
- B: Sem copiar: a prova 3 roda no escopo do projeto, como a bancada antiga, e o acesso total com a pasta de ensaio fica sem prova

## Algo mais?
id: algo-mais
tipo: texto
