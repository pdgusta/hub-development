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
5. **Decidido pelo Gustavo (rodada "Fim da resposta: quando soltar o agente", opção B):** o fim da resposta devolve até
   três vezes seguidas; na quarta parada ainda com falta, solta e registra a falta no `estado.json` da vigia (para
   aparecer no início da próxima sessão e na tela de estado). Substitui o provisório.
- 2026-10-17: retomada gravada em `etapas/retomada-Vela.md` antes do /clear (commit 286236e, 8/8).
6. **Decisão técnica do maestro (2026-10-17):** `agents/frontmatter/**` entra como `tipo: null` no `paths.yml` (oficina,
   como `agents/code/` e `agents/skills/`): sem cartão da pasta, sem pedir descrição dos 30 esquemas. Só essa linha do
   catálogo do 05 mudou. Commit 33194a1; 50/50 (27, gerador, 05 e 04).
