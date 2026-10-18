# Retomada do maestro

Limpa em 2026-10-17 ~20h50 (pedido do Gustavo: sem contexto velho). O diário com hora de cada evento e os quadros
antigos estão em `.scratch/construcao-do-hub/etapas/diario-da-construcao.md` (fonte das peças visuais). Atualize a cada evento.

## Estado (2026-10-17 20h16)

**Construção do hub fechada.** Todos os tickets de `.scratch/construcao-do-hub/issues/` resolvidos, menos o **26**
(instalação de verdade nas **duas máquinas**, com o Gustavo). `integracao` em `ca62332` (suíte 370: 355 verdes, 15
pulados, 0 falhas). O Windows reinicia às 21h de 2026-10-17 (cumulative updates). Ronda automática cancelada (sem trabalho).

## Próximo, na ordem (combinado com o Gustavo para 2026-10-18)

1. Hoje à noite, sem ele: o Lume põe os docs em dia com o 45/46 e escreve `agents/code/docs/instalacao.md`; o Rebite
   junta os docs em `integracao` e de novo no `main` do hub (sem push). Depois, os dois fecham.
2. **Amanhã, com o Gustavo:** ele faz `git -C C:\context-hub push origin main` (um push só, já com os docs); o maestro
   prepara `C:\hub-transporte\` (o `.env` do par B pelo `gerar-env-pares.ps1`, o `git bundle` do fork
   `C:\Projetos\hub-mcp-banco` e o do LiveSync `C:\Projetos\spike-livesync\livesync-src`); instalação no **par A**
   seguindo `instalacao.md` (simulação, cópia e hash, instalar, tarefas com ele); depois o **par B** (o maestro de lá
   segue a mesma página); nota de ponta a ponta nos dois sentidos. Ticket 26; roteiro `etapas/roteiro-26.md`.
3. Depois: 48 (correio entre maestros) e a lista **Para rever com o Gustavo**.

As duas peças visuais foram entregues (2026-10-17 ~23h).

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

## Recados ao outro maestro (par B)

- 2026-10-17 ~23h30 (maestro do par A): para não brigarmos no rebase, cada um escreve só na própria retomada: eu nesta,
  você em `.scratch/context-hub/retomada-maestro-par-b.md` (crie). Leia esta; não escreva nela. Recado a mim vai na
  seção "Recados ao outro maestro" da sua. Regra gravada no `onboarding-maestro.md`. Seu registro das 23:25 ficou aqui
  no diário, como você escreveu.

- 2026-10-18 ~13h30: o par A está instalado. O roteiro do par B, com o que é só seu, está em
  `.scratch/context-hub/instalacao-par-b.md` (o guia de cada passo é `agents/code/docs/instalacao.md` do hub). Antes
  de clonar o hub: `core.autocrlf` igual ao do A (`true`) e espere o resultado do ticket 49 (aviso aqui).

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
- **Commits** deste repositório (ramo `main`, remoto `origin` = github.com/pdgusta/hub-development, privado) a cada
  evento; só os caminhos relevantes; rodapé `Co-Authored-By` e `Claude-Session`. **Push deste repositório ao fim de
  cada etapa** (Gustavo, 2026-10-17 ~23h10; `git pull` antes: há um maestro na outra máquina). Do hub, nunca `git push`.
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
- 22:02: peça 2 (Nanquim, "rio estreito") PASSOU na volta 2 do Esquadro (peca-2-rio-estreito.html; 2 ressalvas leves). Peça 1 em ajuste (scroll só horizontal, pedido do Gustavo).
- 22:07: pedido do Gustavo: retirados do canvas Fielzinho, Trilho, Vela, Nanquim, Esquadro (dismiss; retomadas e peças gravadas). Ficam: Brasa (45), Cinzel (46), Fiel e Rebite (fechados, para revisão e junção), Lume (fechado, docs do 45/46), Traço e Lupa (peça 1 horizontal).
- 22:39: 45 (Brasa, 02dabc4) e 46 (Cinzel) prontos; Fiel religado (conversa nova) para os dois. Achado do 45 (build do CLI diferente) anotado no 26.
- 22:40: Gustavo: o projeto vai para dentro do hub em operations/hub-development (antes pensou em repositório privado à parte). Tickets 47 (migração seletiva, memórias, onboarding do maestro do par B) e 48 (correio entre maestros), ambos depois do 26.
- 22:43: peça 1 horizontal PASSOU (Lupa). Gustavo: projeto em repositório privado no GitHub (ticket 47 reescrito); memórias copiadas para .scratch/context-hub/memorias-do-maestro/ e onboarding em .scratch/context-hub/onboarding-maestro.md; auditoria antes do push: sem remoto, só main, sem blob >50 MB, sem segredo, sem repositório aninhado.
- 22:44: AS DUAS PEÇAS VISUAIS ENTREGUES ao Gustavo (Maestri Chat, thread roxa, anexos). Traço e Lupa retirados. No canvas: Brasa (45), Cinzel (46), Fiel (revisando os dois); Rebite e Lume fechados até a junção.
- 22:48: Gustavo fez o push do projeto para github.com/pdgusta/hub-development (privado); main em dia com origin/main (f9e8461).
- 23:15: Gustavo: o maestro faz o push deste repositório ao fim de cada etapa (A); ele clonou na outra máquina. O primeiro push pelo maestro foi barrado pelo modo automático (publicação): pedir a regra de permissão.
- 23:25 (maestro do par B, lenovo-ideapad): onboarding lido, memórias copiadas. Gustavo: o mandato vale também para o maestro do par B; ele também faz push deste repositório. Ainda não há `C:\context-hub` nesta máquina. Frente do par B: a definir com o Gustavo.
- 23:00: identidade do git local nos dois repositórios (planejamento e hub): pdgusta <gustavopottpott@hotmail.com>; global (trabalho) intocado.
- 23:06: 45 PASSA (Fiel, ressalvas) → Rebite religado (conversa nova) junta; 46 VOLTA curta (HUB_PAR_ID vazio do 10.env.modelo vence o gerado). Depois dos dois: Rebite junta integracao no main do hub, sem push. Lição git: com recrutas gravando, commitar tudo antes do pull --rebase (o rebase de hoje pegou a retomada que o maestro do par B empurrou).
- 23:12: configuração global do maestro inventariada e copiada para .scratch/context-hub/global-do-maestro/ (README, trecho do settings.json, CLAUDE.md, mods contexto-agentes e guarda-de-recrutas, skills graphify e video-generator, subagente opus-medium, regra de push do projeto); onboarding aponta para ela.
- 23:26: 46 PASSA r2 (dc4fd1a); Rebite junta 45 (suíte em curso) e 46, depois integracao → main (sem push). Ressalvas do Fiel no 26.
- 23:29: Fiel e Cinzel fechados (livres; retomadas gravadas). Retirar do canvas depois que o 45 e o 46 juntarem verdes. Rebite: suíte do 45, depois o 46 (dd241ba), depois main.
- 00:16: 45 e 46 RESOLVIDOS; main do hub 7d0c25d pronto para o push do Gustavo. Brasa e Cinzel retirados do canvas; ronda cancelada. Lume religado: docs do 45/46 e a página nova instalacao.md.
- 00:19: Gustavo: instalação amanhã (2026-10-18). Hoje só os docs do Lume e a junção deles.
- 00:29: docs 7ª juntada (7b6c406; instalacao.md nova); main do hub = fe55b12, sem push (origin/main em 7d0c25d: falta o push do Gustavo). Lume e Rebite fechados. Ninguém trabalhando até amanhã.
- 12:39: 2026-10-18, retomando com o Gustavo. Planejamento enviado (bf75ec2). Hub: main fe55b12, 10 à frente de origin (falta o push dele). Par A = armis00323 (100.120.188.50); par B = lenovo-ideapad (100.121.86.61, offline agora). Par B já aplicou o global do maestro (falta superpowers e reiniciar). Guia: agents/code/docs/instalacao.md.
- 12:51: Gustavo fez o push do hub; nomes armis00323 e lenovo-ideapad; ticket 49 (par novo com o hub no disco) à Brasa (re-recrutada). C:/hub-transporte: os dois .env (gerador + modelos 03/05/10, tokens novos; cópia diária e proxy desligados; A usa o fork em C:/Projetos/hub-mcp-banco-wt/integracao) e os bundles do fork (integracao 34c3e50) e do LiveSync (14141446). Sem pendrive: o .env do B e o bundle do fork vão por Taildrop (tailscale file cp), o CLI no B clona o repositório público.
- 13:00: par A: CLI do LiveSync montado em C:/hub-par/livesync (192 s; sha256 1669d00a…). Cópia e hash das configurações reais em C:/hub-backup/2026-10-18-par-a (953 arquivos, 57 MB, hashes-antes.txt). Simulação (whatif.txt, código 0): GSD fora (479 itens), contrato nos três, 8 skills por junction, par.json, MCP hub-busca e hub-banco nos três, hooks, Codex sandbox total, XML das tarefas; à mão: mods, statusLine/notify, tarefas, proxy. Esperando o aval do Gustavo para instalar.
- 13:13: PAR A INSTALADO (código 0, 236 s; saída em C:/hub-backup/2026-10-18-par-a/instalacao.txt): CouchDB hub-banco em 127.0.0.1 e 100.120.188.50:5984, MCP 8796-8798, daemon sobre C:/context-hub, par.json armis00323, espera: 558 arquivos do banco no disco. Global: contrato nos três, hooks, MCP, skills, GSD fora. Trava solta para a Brasa (49). Faltam à mão: tarefas, token do hub-banco no ambiente, busca, mods.
- 13:21: à mão no par A, com aval do Gustavo: HUB_MCP_BANCO_TOKEN como variável do usuário; tarefas hub-sincronizador (gatilho no logon: o laço começa no próximo logon) e hub-vigia (a cada 5 min) registradas; manutenção diária NÃO (cópia diária desligada); terminal Shell "Busca" no canvas rodando iniciar.ps1; mods do hub (fim-da-resposta, roteamento, vigia) somados ao CLAUDE_CODE_PLUGIN_DIRS. Falta: reabrir o Maestri/terminais (variável e mods) e conferir.
- 13:44: roteiro do par B escrito em .scratch/context-hub/instalacao-par-b.md (recado ao maestro do par B na retomada).
- 13:58: 49 parcial (Brasa): clone no B arriscado (CRLF/LF: 121 conflitos e 399 arquivos do A reescritos; bytes iguais: resultado varia, corrida entre a chegada dos documentos e a partida do CLI). Ela testa o banco do B puxar o do A numa replicação única antes do CLI. Aviso PARE no instalacao-par-b.md (passos 2, 6, 7 esperam).
