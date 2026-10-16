# Retomada do maestro

Reescrita em 2026-10-16, ~19h40 (Brasília), antes de um /clear pedido pelo Gustavo; completada às ~20h.

## Leia nesta ordem (para ficar na mesma página que a sessão anterior)

Caminhos relativos a `C:\Projetos\context-hub\`. Leia inteiro o que diz "inteiro"; do resto, só o trecho indicado.

1. **Este arquivo**, inteiro.
2. `AGENTS.md` (regras do projeto) e o `MEMORY.md` da memória (já vem no contexto).
3. `.scratch/context-hub/issues/16-passagem-para-a-construcao.md`: só os comentários de **2026-10-16** (o fim do
   arquivo; cada decisão do dia está lá, em ordem).
4. `.scratch/construcao-do-hub/revisao/plano/proposta-de-etapas.md`, inteiro (o plano e a seção "Decidido").
5. `.scratch/construcao-do-hub/etapas/regras-da-construcao.md`, inteiro (como construtores e revisor trabalham).
6. `.scratch/construcao-do-hub/issues/`: a linha `Status:` e `Blocked by:` de cada um dos 26 tickets (dá a fronteira),
   e o `## Comments` dos que estiverem `claimed`.
7. `.scratch/construcao-do-hub/revisao/escolhas-decididas.md`, inteiro (as 23 escolhas e as 4 mudanças do Gustavo).
8. Só se precisar do detalhe: `spec.md` (legenda das marcas no topo e o bloco do Worker do ticket em jogo).

Depois, confira o mundo real (nesta ordem):

- `maestri list` (quem está no canvas) e `maestri check "<nome>"` de cada construtor e do Fiel;
- `.scratch/context-hub/portal/caixa/` por `estado: nova` e `portal/rodadas/` por `estado: aberta`;
- `git -C C:\context-hub branch -vv` e `git -C C:\context-hub worktree list` (ramos `ticket-NN`);
- `.scratch/construcao-do-hub/etapas/*/relatorio*.md` e `parecer-*.md` (o que os construtores e o Fiel gravaram).

Pendências abertas: rodada `2026-10-16-ticket-05-perguntas-do-trilho` (escopo do verificador, tabela `stage`→`status`, `operations/`) e a
proposta da nota de retomada com várias sessões (`.scratch/construcao-do-hub/rascunhos/retomada-com-varias-sessoes.md`,
decidir antes do ticket 18).

## Onde estamos

**A construção do hub está rodando pelo `/implement-spec`** (invocado pelo Gustavo ~19h35), sobre o spec revisto e os
26 tickets publicados por `/to-tickets`.

- Spec: `.scratch/construcao-do-hub/spec.md` + `spec-partes/` (revisão conversada de 3 revisores, acordo em
  `revisao/acordo.md`; as 23 escolhas sem ticket decididas em 4 rodadas com cartas, registro em
  `revisao/escolhas-decididas.md`; marcas `[aceita]`, `[formato]` = plano antigo de 1 hora, não vale; `[ticket aberto:
  56]` = fora da construção). Versões anteriores: `revisao/antes/` e `revisao/antes-das-escolhas/`.
- Plano decidido: `revisao/plano/proposta-de-etapas.md` (seção "Decidido"): etapa zero de provas de risco, depois as
  etapas em sequência; **até 3 agentes**, quem adianta só pega o que não depende de peça que ainda não existe; antes de
  cada etapa o maestro propõe a receita pelo resultado da anterior e conta o que já foi antecipado; o Gustavo ajusta.
- Tickets: `.scratch/construcao-do-hub/issues/01`-`26` (o 26 `ready-for-human`). Mapa etapa → tickets: 0 = 01-03;
  1 = 04-06; 2 = 07-08; 3 = 09-11; 4 = 12-13; 5 = 14-15; 6 = 16-17; 7 = 18; 8 = 19-20; 9 = 21-22; 10 = 23-24;
  11 = 25; depois = 26. Os 11 antigos estão em `issues-tentativa-paralela/`.
- Regras e briefs: `etapas/regras-da-construcao.md`, `etapas/00-provas/brief.md`, `etapas/01-esqueleto/brief.md`.
- Repositório do hub `C:\context-hub`: `main` = `integracao` = "Início do hub", `origin` =
  `git@github-context-hub:pdgusta/context-hub.git` (deploy key `~/.ssh/context-hub-par1`). Ramos da execução de
  2026-10-15 renomeados `tentativa-paralela/faixa-NN` (só consulta). Um ramo e uma worktree por ticket:
  `C:\context-hub-wt\ticket-NN`. Sobrou `C:\context-hub-wt\faixa-10-ferramentas\` (download do mcp-proxy), intocado.

## Quem está no canvas (workspace Context Hub)

- **Brasa** (Claude Opus 5.5 médio, "Construtor do hub"): tickets 01 e depois 02.
- **Vela** (idem): ticket 03 (aval: copiar só o `auth.json` do Codex para o `CODEX_HOME` de ensaio e apagar ao fim).
- **Trilho** (idem): ticket 04, depois 05 (o 06 espera o 02).
- **Fiel** (Codex GPT 6.1 Sol médio, acesso total, "Revisor da construção"; iniciado pelo Gustavo, porque o modo
  automático do maestro recusa criar agente sem sandbox): revisa cada ticket antes de juntar; ligado aos três.
- **Fielzinho** (Codex GPT 6-Astra médio, acesso total, "Revisor parceiro da construção"; iniciado pelo Gustavo): revisa em dupla com o Fiel (`construcao-do-hub/etapas/revisao-em-dupla.md`); ligado ao Fiel.
- **Rebite** (Claude, "Integrador da construção"): junta os tickets aprovados; ligado aos construtores, ao Fiel.
- **Aquarela** (Opus 5.5 alto, "Designer de visuais") e **Lente** (Opus 5.5 médio, "Revisor de cartas UI/UX"): ficam
  para as cartas. O Gustavo elogiou as cartas dela (caderno do faroleiro; ateliê de costura); ressalva: tipografia dos
  títulos legível.
- **Portal**: shell rodando o portal em http://127.0.0.1:8770/ (`.\iniciar.cmd` na pasta do portal).

## O ciclo de cada ticket (o que o maestro faz)

1. O construtor termina, pede revisão ao Fiel, aplica consertos (até 2 voltas) e avisa o integrador **Rebite**.
2. O Rebite (Claude, papel "Integrador da construção", desde 2026-10-16 a pedido do Gustavo: "você é o maestro e deve
   estar sempre disponível pra orquestrar") confere o parecer, junta em `integracao` na worktree
   `C:\context-hub-wt\integracao`, roda os testes, resolve o ticket e avisa o maestro (procedimento
   `construcao-do-hub/etapas/juntar-tickets.md`, registro `etapas/registro-de-juncoes.md`). O maestro não é o centro
   da comunicação nem executa a construção em worktree (os recrutas falam entre si e ele recebe o resultado); varredura
   e gestão de git no repositório de planejamento ele faz (Gustavo, 2026-10-16). Passa ao construtor o próximo ticket
   da fronteira (bloqueios e teto de 3).
3. Antes de cada **etapa nova**, rodada curta no portal com a receita (quem constrói, quem revisa, modelo), dizendo o que
   já foi antecipado. Perguntas que vivem nos tickets: login dos harnesses no ensaio (11, 24), cota do gemini (13), as
   três lacunas de dono (20), instalação real (26).
4. No fim de tudo: `code-review` no ramo de integração e um implementador para os consertos; limpar as worktrees.

## Regras de trabalho que valem agora

- Decisão só no portal (`portal/rodadas/`), explicação na própria rodada; rodada respondida nunca é reescrita. Terminal:
  uma linha "Pergunta nova no portal: <título>". Ao receber "Portal: 1 mensagem nova": ler o `.md` em `portal/caixa/`,
  absorver no ticket dono, trocar `estado: nova` por `lida`, marcar a rodada `absorvida`, conferir a caixa inteira.
  Aprovação de carta: atualizar `decisao` no `portal/cartas.json`.
- Processo: só o fluxo do Matt Pocock, invocado pelo Gustavo (o maestro errou ao despachar construtores antes do
  `/implement-spec`; não repetir).
- Trabalho visível: executores e revisores como recrutas no canvas, sem subagentes escondidos.
- Comandos que reiniciam ou removem recrutas levam `# risco-avaliado: <motivo>` (mod `guarda-de-recrutas`); só com o
  recruta ocioso e o trabalho gravado. Recado para recruta ocupado fica na fila; texto preso no prompt: `--raw "\r"`.
- Repositórios de código ficam **fora do hub** (decisão de 2026-10-16); repo em pasta `local: true` está no radar.
- Radar novo de 2026-10-16 em `estrategia-pos-pesquisa.md`: Cartographer (CLI v2 entre etapas), claude-mem (referência
  de busca em três camadas), Headroom (teste se a cota travar), OmniRoute (segundo mapa), Claude Code setup (sem link),
  vídeo do Pstack (mesclar com as skills do Matt), repo em `local: true`.

## Fatos de 2026-10-16

- O TI liberou o Tailscale no notebook; não há política do Copilot da empresa; o laço do system design (ticket 56) só
  continua depois da construção; Docker Desktop ligado (servidor 29.8.2).
- A rodada `passagem-para-a-construcao-r2` (quatro avais antigos) está **suspensa**; os avais voltam nos tickets.

## Depois da reescrita (~19h45)



## Depois de ~21h

- Lugar do código decidido (C): skills em `agents/skills/<peça>/` para o que o agente chama; `agents/code/` para hooks, mods, kit, bin, test; provas em `agents/code/test/provas/`. Spec, regras e tickets 12 e 16 atualizados; os quatro recrutas avisados.
- Ticket 04 **resolvido**, juntado em `integracao` (b68f540). Junções feitas na worktree `C:\context-hub-wt\integracao`.
- Trilho no 05 (worktree `ticket-05`), com provisórios das três perguntas da rodada `ticket-05-perguntas-do-trilho`. Ao chegar a resposta: repassar ao Trilho; se a 1 for A, publicar o ticket 27 (verificador: `index.md`, links `par://`, `other/`, fim da resposta; bloqueado por 05 e 06).
- Anotado sem rodada: o `verificar-hub` recusa `CLAUDE.md` em `.maestri/`; só vira decisão se um workspace do Maestri morar no hub.
- ~21h20: ticket 03 **resolvido** e juntado (3857c98); lições para o kit no ticket 23. Vela passou ao 02 (era da Brasa), ligada à Brasa. Brasa segue no 01 (sem commit ainda; prova a mover para `agents/code/test/provas/01-banco/`). Trilho no 05. Depois do 01, Brasa pega o próximo da fronteira (o 19 só depois da etapa 1, pelo plano).
- 19:21 (portal): três perguntas do Trilho respondidas, todas A. Ticket 27 publicado (verificador: `index.md`, `par://`, `other/`, fim da resposta; bloqueado por 05 e 06; o 23 espera o 27). Tabela `stage`→`status` no spec. `operations/` não é iniciativa. Nenhuma rodada aberta.
- ~21h55: Fielzinho no canvas; revisão em dupla. Aquarela e Lente dispensados pelo Gustavo (ociosos, trabalho em `revisao/`).
- ~22h10: **primeiro commit do repositório de planejamento** (`61888ed`, ramo `main`, sem remoto). `.gitignore`: `.maestri/`, cache do Python, capturas de tela das revisões de UI. Varredura antes: nenhum segredo nem e-mail de empresa ou cliente (só falsos positivos em READMEs públicos do laço). Daqui em diante o maestro faz um commit a cada rodada absorvida ou ticket resolvido (o Gustavo liberou varredura e git para o maestro).
- ~20h (relógio da máquina): ticket 02 resolvido e juntado pelo Rebite (c8d2267); Vela no 06. Troca do Fiel por Claude Opus 5.5 médio pedida pelo Gustavo, à espera do Fiel ficar ocioso (monitor).
- ~20h20: ticket 05 resolvido e juntado (0d04985). Trilho no 14 (antecipação da etapa 5) e tira o README.md da raiz no primeiro commit. Fielzinho faz a leitura pendente da rodada 4 do 05 quando a cota voltar (20:26). Fiel agora é Claude Opus 5.5 médio. Etapa 1: falta só o 06 (Vela); depois, rodada da receita da etapa 2 (banco: 07-08, espera o 01 da Brasa).
- ~20h35: ticket 01 resolvido e juntado (45ec3b0); **etapa 0 completa**. Rodada aberta `2026-10-16-etapa-2-receita` (recomendada: Brasa no 07 e depois no 08). Brasa só lendo até a resposta. Vela pega o 27 quando o 06 entrar (fecha a etapa 1).
- 20:30: receita da etapa 2 decidida (A); Brasa no 07, depois o 08.
