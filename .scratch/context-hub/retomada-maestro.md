# Retomada do maestro

Limpa em 2026-10-17 ~20h50 (pedido do Gustavo: sem contexto velho). O diário com hora de cada evento e os quadros
antigos estão em `.scratch/construcao-do-hub/etapas/diario-da-construcao.md` (fonte das peças visuais). Atualize a cada evento.

## Estado (2026-10-17 20h16)

**Construção do hub fechada.** Todos os tickets de `.scratch/construcao-do-hub/issues/` resolvidos, menos o **26**
(instalação de verdade nas **duas máquinas**, com o Gustavo). `integracao` em `ca62332` (suíte 370: 355 verdes, 15
pulados, 0 falhas). O Windows reinicia às 21h de 2026-10-17 (cumulative updates). Ronda automática cancelada (sem trabalho).

## Próximo, na ordem

1. **Duas peças visuais** que resumem a execução, cada detalhe (pedido do Gustavo, 2026-10-17 ~04h40). O que é cada
   uma, o tipo e o detalhe: o maestro decide agora. Um time enxuto por peça, **Designer + Revisor**, cada um com até 2
   subagentes; as duas em paralelo. Fontes: `etapas/diario-da-construcao.md`, `etapas/registro-de-juncoes.md`, os
   `## Comments` dos tickets, pareceres e relatórios em `etapas/`, os commits de `integracao` e deste repositório.
   Memórias: `visuais-pelo-designer`, `visual-diagrama-no-centro`, `legibilidade-dos-titulos`, `headless-edge-para-qa-visual`.
2. **Lume**: docs (`agents/code/docs/`, ramo `docs`) em dia com o 24, o 22 (evidência do Codex) e o 25; o Rebite junta
   (só 12-busca e verificador de pastas; ver `etapas/documentacao-tecnica.md`).
3. **Roteiro do 26** (ticket `issues/26-instalacao-de-verdade-no-par-1.md`): par 1 aqui (kit no HOME real, cópia e hash
   antes); par 2 no outro PC (lá há Claude Code, Maestri, admin; dá para clonar o hub; primeiro setup do jeito mais
   adequado, o fluxo genérico de "par novo" vem depois); esperar o par 2 receber o hub (minutos) e conferir uma nota de
   ponta a ponta. Inclui a comunicação entre os dois maestros (Radar).
4. Rever com o Gustavo a lista abaixo.

## Religar depois do reinício

1. `maestri list`. Religar **só quem tiver trabalho**: no Claude, `maestri ask "<nome>" --raw "claude --resume <id>\r"`
   pelo **PowerShell** (pelo Git Bash, `/exit` e caminhos viram caminho do MSYS), ou `claude` + "leia a sua retomada".
   Depois do reinício de 21h, o Maestri religou todos em sessões **antigas** (da manhã); o maestro fechou os sem
   trabalho. Para religar, prefira **`claude` (conversa nova) + "leia a sua retomada"**: as retomadas estão limpas e
   em dia. Fielzinho saiu da execução (não religar).
2. Ao Lume, ao religar: "44 juntado (df6c2e5); docs 5ª leva (f640bbd); 24 resolvido; 22 com a evidência do Codex; 25 resolvido (ca62332)".
3. Ronda (só se houver trabalho em curso): CronCreate `13,38 * * * *`, prompt "Ronda do maestro ...".
4. Docker Desktop: ligar só quando um teste pedir (`docker desktop start`); parar com `docker desktop stop` (o
   `wsl --shutdown` sozinho não basta: o Docker religa o WSL).

## Mandato (Gustavo, 2026-10-17 ~04h) — vale até ele dizer o contrário

O maestro orquestra sozinho e decide pelo Gustavo, com critério "afiado o bastante para não quebrar nada e leve o
bastante para a execução seguir com bom progresso e alinhada ao spec". Decisão que só muda uma decisão já tomada pode
seguir: registre no ticket dono e em **Para rever** abaixo. Só o realmente bloqueante fica para ele. Liberdade parcial
para abrir e fechar aplicativos e processos da execução. Contexto do maestro: nunca passar de 700k (auto-compact em
600k). Memória `autonomia-na-construcao`.

## Como a operação funciona (o que ainda vale)

- **Ciclo de um ticket:** construtor (tdd) → Fiel (2ª leitura por subagente Opus 5.5) → Rebite junta em `integracao`
  (`C:\context-hub-wt\integracao`), roda a suíte inteira (só ele, só na junção), resolve e avisa o maestro e o Lume. O
  maestro não junta nem executa; passa ticket, responde, decide.
- **Trabalho pesado:** um por vez, trava `etapas/trava-pesada.md` e fila `etapas/fila-pesada.md`; quem solta avisa o
  próximo. Memória é o gargalo: com Docker, **janela quieta** (os sem trabalho gravam a retomada e saem).
- **Codex só para testes** (Gustavo, 2026-10-17 ~14h35): `gpt-6-luna` por padrão (`MODELO_CODEX` /
  `HUB_MODELO_CODEX`), `gpt-6.1-sol` só se o teste for difícil. Execução e revisão no Claude. Restam 2 reinícios de cota
  do Codex com o Gustavo. Memória `codex-sem-cota-usa-claude`.
- **Limites:** até 4 construtores; cada recruta até 1 subagente + 3 Haiku 5.5 médio para tarefa simples ou QA.
- **Contexto dos recrutas:** acima de 40%, no ponto seguro gravam `etapas/retomada-<nome>.md` e dizem "salvo para
  limpar"; `/clear` (pelo PowerShell; se estiver ocupado, entra na fila) e depois "leia a sua retomada" (conferir que
  chegou).
- **Decisões do Gustavo:** portal fechado (RAM); rodadas em `.scratch/context-hub/portal/rodadas/` e pelo Maestri Chat
  (thread blue), ou no chat do maestro quando ele está presente; registrar no ticket dono.
- **Commits** deste repositório (ramo `main`, sem remoto) a cada evento; só os caminhos relevantes; rodapé
  `Co-Authored-By` e `Claude-Session`. Nunca `git push`, nunca tocar `main`/`tentativa-paralela/*` do hub.
- **Nada global real** sem o aval do Gustavo (`~/.claude`, `~/.codex`, `~/.copilot`, `~/.agents`); cópia de login só
  por aval, apagada ao fim, com hash antes e depois. Dado de cliente só pelo nome da iniciativa.

## Para rever com o Gustavo (decisões tomadas pelo mandato)

- (45) A prova do banco entre máquinas expõe o CouchDB de ensaio no IP Tailscale desta máquina por alguns minutos (só a tailnet do Gustavo, senha aleatória, descida conferida por porta).

- (25) Fechou sem o Codex nas fases 4-7 do hub inteiro; ali o Codex está provado nos tickets de cada peça (17, 18, 21,
  22). Opcional antes da instalação (anotado no 26).
- (25) Nota que não descia do A ao B: não era replicação morta; um par recém-subido recebe a semente inteira (~520
  arquivos, 4-7 min) e a nota nova espera na fila. Conserto só no teste. Na instalação, o 2º par deve avisar ou esperar
  a convergência (anotado no 26).
- (22) O mcp-proxy do spec não repassa o `instructions` do MCP do banco; o contrato chega ao cliente pela regra curta
  das ferramentas e pela configuração global do kit. Consertar ou trocar o proxy: radar.
- (18, **muda o spec**) Várias sessões no mesmo trabalho: quem conduz mantém a `retomada.md`; cada recruta, a sua
  `work/passagem-<terminal>.md`; o início abre as duas.
- (16) Binário descartado é divergência até `vigia recuperar` ou `vigia olhei <caminho>`; "piora" = item sobe de nível
  (item novo conta como ok antes).
- (17) Vigia no Claude Code pela linha de status (`$.ui.status`).
- (15) O hub-busca expõe só a `search` nos três harnesses (Claude por `deny` de `mcp__hub-busca__read`).
- (09) Conflito só quando a base não é mais folha viva; `delete_note` exige `base_rev`; append/prepend sem base gravam
  como filha da versão lida.
- (processo) Vários tickets começaram antes dos bloqueios, juntando só depois; suíte inteira só na junção.

## Para o Gustavo, de dia (não bloqueia)

- Apagar as ~1.325 pastas `hub-ensaio-*` antigas em `%TEMP%` (4,0 GB; sem login dentro). A limpeza em massa pelo
  maestro foi recusada pela permissão automática; os testes já não as deixam (36, 38).

## Radar

- **Dois maestros, duas máquinas** (Gustavo, ~20h): o do outro PC será outra sessão; precisam se comunicar. Candidatos
  (fonte primária antes de propor): uma pasta de recados no próprio hub replicado, vigiada por cada lado; o git do hub;
  recurso do Maestri entre máquinas (não verificado). Entra no roteiro do 26.
- Proxy de MCP que repasse o `instructions` (achado do 22).
- Pequeno, sem ticket: a evidência do Codex (`lido.json` do 22 e do 24) não grava o modelo (ressalva do Fiel).
- Worktrees ticket-38, ticket-39 e ticket-41 ainda existem em `C:\context-hub-wt\` (limpar quando convier).
- Trail-Code (`pesquisa-trail-code.md`): ensaio num repositório de iniciativa; Gustavo aceitou deixar para depois do 25.
- Acervo de referências (backlog sem gatilho): vídeos em motion; primeiro item https://youtu.be/mZ27vUoOEB0.

## Leia nesta ordem (caminhos relativos a `C:\Projetos\context-hub\`)

1. Este arquivo.
2. `AGENTS.md` e o `MEMORY.md` (já vêm no contexto).
3. `.scratch/construcao-do-hub/etapas/regras-da-construcao.md`.
4. O ticket 26 e, para as peças visuais, `etapas/diario-da-construcao.md`.
5. Só se precisar: `juntar-tickets.md`, `revisao-em-dupla.md`, `documentacao-tecnica.md`, o spec.

Depois, confira o mundo real: `maestri list`, `git -C C:\context-hub log --oneline -3 integracao`.

## Diário (mais novo embaixo; o anterior está em `etapas/diario-da-construcao.md`)

- 20:50: retomada limpa; diário e quadros antigos movidos para `etapas/diario-da-construcao.md`. Retomadas dos recrutas
  limpas (Vela 633 → 47, Rebite, Fiel 31 pelos próprios; Brasa 236 → 38, Cinzel 33, Trilho 35, Lume 52 com a fila viva, Fielzinho 10 por subagente).
- 21:10: reinício do Windows. O Maestri religou todos (sessões antigas; 714 MB livres). Fechados Brasa, Vela, Trilho, Cinzel, Fiel e Fielzinho (3,0 GB livres). No canvas: maestro, Rebite, Lume (conversa nova: retomada e docs em dia com 24, 22, 25). Próximo: as duas peças visuais.
- 21:16: peças visuais: brief em etapas/../resumo-visual/brief.md; papéis novos (Designer e Revisor do resumo da construção); recrutados Traço+Lupa (peça 1: a construção ticket a ticket) e Nanquim+Esquadro (peça 2: o que atrapalhou e como se resolveu); portas 8771-8774.
- 21:18: Lume: docs em dia (b20bf5f, 11 páginas), 6ª junção com o Rebite. Divergência: HUB_PAR_ID não é definida pelo kit → anotada no ticket 26.
- 21:20: roteiro do 26 rascunhado (etapas/roteiro-26.md): ticket 45 de preparo (rede Tailscale, HUB_PAR_ID, convergência, segredos/fork/CLI, proxy na fila); decisões D1 (integracao→main e push com aval), D2 (levar o que não vai pelo git), D3 (Tailscale).
- 21:21: docs 6ª junção (dc514db) verde sem o 12-busca: regra da junção dos docs atualizada (verificador + 27-pastas; busca não indexa agents/code desde o 41). 821 MB livres com os designers.
- 21:22: docs 6ª junção verde (dc514db); Lume e Rebite fechados (sem fila). No canvas: maestro e os times das peças (Traço+Lupa, Nanquim+Esquadro).
- 21:48: peça 1 (Traço, "A construção, em partitura") PASSOU na volta 2 da Lupa (resumo-visual/peca-1-partitura.html; parecer-peca-1.md). Peça 2 (Nanquim, rio estreito) em revisão do Esquadro.
- 21:54: Gustavo (Maestri Chat): 1A, 2A, 3A; Tailscale ainda não. Tickets 45 (banco entre duas máquinas, Brasa) e 46 (kit para duas máquinas, Cinzel) publicados; 26 bloqueado por 25, 45, 46; depois o Rebite junta integracao no main e o Gustavo faz o push. Brasa e Cinzel religados (conversa nova).
- 21:59: Gustavo: peça 1 com scroll só horizontal (uma linha contínua da execução toda, sem scroll vertical); pedido ao Traço, rodada curta da Lupa.
