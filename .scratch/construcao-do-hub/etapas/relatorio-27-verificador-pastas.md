# Relatório do ticket 27: o verificador cuida das pastas (Vela)

## Estado

- 2026-10-17: ticket pego; worktree `C:/context-hub-wt/ticket-27` (de `integracao` 8b9beef). Lendo as fontes.
- 2026-10-17: perguntas de fatos ao maestro (par_id, 'parecidas', formato da lista, contagem de 10, quais notas no fim); desenho: núcleo verificar-fim + adaptadores (mod Claude Code, Stop Codex, agentStop Copilot) a partir da bancada de acesso e da prova 03.

## Decisões técnicas do maestro (2026-10-17, resposta às perguntas da Vela)

1. `par_id` desta máquina: variável de ambiente `HUB_PAR_ID`, gravada pelo kit (no ensaio, um nome inventado; os nomes
   reais das máquinas seguem em aberto no spec). Sem ela, o verificador não reescreve e devolve a falta.
2. "Três notas parecidas em `other/`": pelo `why_other`, no hub inteiro (o catálogo de blocos é um só); só aviso.
3. Lista do `index.md` com `summary: auto`: entre `<!-- lista:inicio -->` e `<!-- lista:fim -->`, adotando na primeira
   passada as linhas `- \`x\`: ...` existentes. Descrição: a existente fica; nota `.md` nova entra com o `title`; arquivo
   sem texto entra sem descrição e vira falta ("descreva x"); anexo com texto irmão não ganha linha, só o irmão.
4. "Chega a 10": entradas diretas da pasta (arquivos e subpastas), sem o que tem ponto e sem o próprio `index.md`. "A
   busca não lê": arquivo que não é `.md` e não tem texto irmão.
5. Quando soltar o agente no fim da resposta: foi ao Gustavo (rodada "Fim da resposta: quando soltar o agente"; o spec diz
   que a resposta não termina enquanto houver falta). Provisório: devolve uma vez; na segunda parada seguida, solta e
   registra a falta. Isolado num ponto só do código.
