# Passagem para a construção

Type: task
Status: resolved
Blocked by: 02, 04, 06, 08, 09, 11, 12, 15, 33

## Question

Rodar `/to-spec` e `/to-tickets` a partir das decisões do mapa. A construção acontece nos tickets
gerados, fora deste mapa (Q7). Resolvido quando a spec e os tickets de construção existirem.
- 2026-10-10 (vinda de "Onde o servidor mora"): entram na construção: o kit de par (script e `.env`
  modelo: Tailscale, compose CouchDB + MCP, replicação, Setup URI) e o kit de cliente (chave efêmera
  com tag e linha de MCP no harness), com o mínimo de passos; o segundo MCP só de leitura por par e o
  grant que limita os clientes a ele; o primeiro teste é o LiveSync com dois CouchDB replicando entre
  si (se falhar, volta à S1); a consulta ao TI antes do Tailscale no notebook.
- 2026-10-12 (vinda de "Portas de entrada do hub"): entram na construção: o kit de par confere que
  não há `CLAUDE.md` no hub nem acima dele, põe o marcador na raiz e `project_root_markers` no Codex,
  liga `claude-md-and-agents-md` se "Maestri: padrão e liberdade" pedir, cria os links simbólicos do
  contrato (`~/.codex/AGENTS.md`, `~/.copilot/copilot-instructions.md` juntando com o GSD), o import no
  `~/.claude/CLAUDE.md`, as junctions de skills e confere o modo de desenvolvedor do Windows; o script
  que move para o `_archive/` conferindo o outro par; a ponte `mcp-remote` só de leitura do Claude
  Desktop; no fork do MCP, o `instructions` com a cabeça do `AGENTS.md` e a regra curta nas descrições
  das ferramentas de gravação; no kit de cliente, `--allow-all-mcp-server-instructions` e o contrato na
  configuração global; o teste dos três harnesses com o MCP pronto, capturando a requisição do Codex.
- 2026-10-12 (vinda de "Maestri: padrão e liberdade"): entram na construção: a família `maestro-*`
  em `agents/skills/` com as junctions; o primeiro lote do acervo (lista no Answer daquele ticket); a
  guarda do acervo no escopo do usuário de cada par (mod ou hook, verificador em outro modelo, aval) e
  a recusa de gravação no acervo para Codex e Copilot; o hook de início de sessão com
  `MAESTRI_TERMINAL_ID`; o hook de registro de uso; `claude-md-and-agents-md` e o marcador de raiz no
  kit de par. Testes da construção: junction com mod (a doc fala de symlink); regras de caminho pegando
  a gravação pelo caminho da junction e pelo real; `$.ui.ask` num terminal do Maestri sem ninguém
  olhando; tempo de um hook `agent` em Sonnet; hooks de uso e de início no Codex e no Copilot.
- 2026-10-13 (vinda de "Revisão do sync e da divergência com o banco", resolvida):
  entram na construção o sincronizador (CLI do LiveSync como
  tarefa agendada, pelo caminho dos testes oficiais, cada máquina nova aceita com `mark-resolved`, ligado
  antes do plugin), `syncMaxSizeInMB` 200 no CLI e no plugin, a regra de pastas com ponto em qualquer
  nível (testar), o comportamento acima de 50 MiB (testar), a vigia de cada máquina com notificação e o
  comando de recuperar binário, o mod do Claude Code com o estado da vigia e o `.git` de cópia de
  segurança diária.
- 2026-10-14 (vinda da peneira da pesquisa ampla, `estrategia-pos-pesquisa.md`, aceita pelo Gustavo): peças com
  Windows confirmado na régua da pesquisa (`exploracao/anexos/pesquisa-50-sintese.md` §4): SDK Python do MCP v2
  (Python 3.11+); python-frontmatter e PyYAML (`safe_load`); ripgrep; ONNX Runtime com e5-small como reserva
  local de embeddings; Watchman ou watchdog; o proxy de MCP. A linguagem do MCP do es617 (fato a confirmar na
  "Camada de busca") define quais entram.
- 2026-10-14 (vinda de "Camada de busca", os três fatos): o MCP do es617 é TypeScript (Node ≥ 22), então as peças
  Python da lista anterior só entram se houver um processo Python ao lado do MCP. A regra de exclusão do LiveSync
  precisa cobrir arquivos com ponto (`**/.*`), não só pastas.
- 2026-10-14 (Gustavo, chat): **sem consulta ao TI** antes do Tailscale no notebook corporativo. Isso confirma a
  dispensa de 2026-10-10 ("Testes das portas de entrada"), e o item "a consulta ao TI antes do Tailscale no
  notebook" do comentário de 2026-10-10 acima cai.
- 2026-10-14 (Gustavo, chat): **FreeLLMAPI na construção.** Ele passa a rodar só no notebook pessoal, nativo no
  Windows (servidor Node, sem Docker; o README cita ~40 MB de RSS ocioso), com o `.env` (`ENCRYPTION_KEY`) e o
  `freeapi.db` copiados da instalação Docker atual, para as chaves cifradas abrirem. Como o servidor nativo
  escuta em todas as interfaces por padrão (`host: process.env.HOST ?? '::'`, `server/src/lib/config.ts`), ele fica
  preso à interface do Tailscale (`HOST=<IP do Tailscale>`, ou firewall liberando a porta 3001 só para a tailnet),
  com grant só para as máquinas do Gustavo. O notebook corporativo o chama pela tailnet, com uma variável
  `FREELLM_BASE_URL` no lugar do `localhost:3001` fixo. **Até a construção**, o FreeLLMAPI segue no Docker do
  notebook corporativo, porque os testes e spikes para fechar os tickets precisam dele. Consequência anotada: com o
  par pessoal fora do ar, o notebook fica sem embeddings, e isso aciona o item do radar "Ollama ou ONNX como
  reserva local" (`estrategia-pos-pesquisa.md`).
- 2026-10-15 (vinda de "Acesso dos agentes: decisão", rodada 4): o **marcador de raiz sai** do kit, junto com o
  `project_root_markers` no Codex; o `.git` da raiz basta para o Codex e o Copilot chegarem ao `AGENTS.md`.
- 2026-10-15 (vinda do "Laço do system design", seção 13 da descrição v3.1): lacunas de dono que são mecanismo de
  manutenção e entram na spec: quem confere os 30 dias do `_archive/` e apaga; quem atualiza a cabeça do contrato nas
  instruções do MCP quando o `AGENTS.md` muda; onde fica o registro do aval de mudança no contrato; quem escolhe o modelo
  do verificador da guarda do acervo; como o erro de peça citada que sumiu chega ao Gustavo.
- 2026-10-15 (Gustavo, no terminal): a sequência da construção é `/to-spec` → `/to-tickets` → `/implement-spec`
  (`/implement` só para um ticket isolado; `AGENTS.md` corrigido). **A spec e os tickets de construção nascem neste
  repositório** (`C:\Projetos\context-hub\.scratch\`), "por enquanto", mesmo que o hub final viva em `C:\context-hub` ou
  no WSL; nada de `/setup-matt-pocock-skills` num repositório novo agora.
- 2026-10-15 ~20h50 (Gustavo, no terminal): **a construção é um laço**, com o desenho mostrado a ele antes. Pedidos:
  **10 agentes Opus 5.5 com esforço alto** em paralelo, **cada um com até 10 subagentes**; tickets **o menos
  horizontais possível**; **separação de papéis**; **sem limite de tokens, com limite de 1 hora**; **todos conversam
  entre si ou com o maestro**; tarefa **MUITO complexa ganha um Fable 5.1 médio** só para ela. Logo depois: **mais 2
  "Prumos" revisores, Claude Opus 5.5 alto** (o Prumo atual sai do Codex e vira um deles). E, já: a equipe de design (UI
  engineer, UX revisor, Tech lead, QA tester) constrói o **painel da construção**, só para ele ver a execução rolando,
  independente da execução; carcaça agora, ajuste depois do laço aprovado. Brief em
  `.scratch/construcao-do-hub/painel/brief.md`; mesa da equipe em `painel/mesa.md` (os recrutas não estão ligados entre
  si no canvas; a CLI não liga). A troca do Prumo pela CLI foi barrada pelo classificador de permissões (pedido ao
  Gustavo). Proposta do laço: `.scratch/construcao-do-hub/laco-proposta.md`.
- 2026-10-15 ~21h10: **rodada 1 aberta** (`portal/rodadas/2026-10-15-passagem-para-a-construcao-r1.md`), com a
  proposta do laço: papéis (recomendada A: 7 construtores, integrador, testador de aceite, pesquisador de fonte e os 2
  Prumos, um das decisões e um do código), a 1 hora (recomendada A: por ticket) e as conversas (recomendada A: ligações
  no canvas ao integrador e aos Prumos). Carta `laco-construcao` pedida ao Designer.
- 2026-10-15 ~21h25: o Gustavo trocou o Prumo pelo terminal (`maestri recruit "Prumo" --command "claude --model
  claude-opus-5-5 --effort high --permission-mode auto" --replace "Prumo"`): agora Claude Opus 5.5 alto, primeiro dos 2
  Prumos. O segundo nasce com os 10 recrutas, depois do laço aprovado.
- 2026-10-15 ~21h35: o maestro errou ao dizer que a CLI não liga terminais: existe `maestri connect "A" "B"` (a busca
  dele no `maestri help` foi cortada). O Gustavo: "eu não vou ligar ninguém a ninguém, você que deve fazer isso". A equipe
  de design foi ligada entre si (seis pares). A 3ª pergunta da rodada 1 (as conversas), ainda sem resposta, saiu da
  rodada: o maestro liga todos com todos pela CLI ao criar os recrutas. Proposta e carta ajustadas.
- 2026-10-15 21:08, **rodada 1 respondida** (envio `d29332f7-210d-47b3-972f-74b2ccbc8818`):
  - **papéis: sem escolha**, com comentário: "Se os tickets forem independentes, pode ser a opção A, ja tem meu aceite. Mas
    se tem relação, faça de forma vertical e despache em grupos lógicos de execução e dê uma parte para cada worker. Não
    deve ser um trabalho horizontal, um worker não deve ficar parado esperando o outro, cada um pode seguir com o que é
    responsável. Inclusive eu quero uma rodada só deles conversando entre eles pra ajustar exatamente a sua proposta de
    execução. Quero uma rodada Ralph engineering só disso. Pode ser com você junto ou não.";
  - **1 hora = C** (a recomendada era A): a execução inteira em 1 hora; o que não couber fica para outra execução.
  A carta `laco-construcao` (pronta pelo Designer às ~21h10, antes da resposta) ficou histórica, sem veredito.
  **Rodada Ralph de planejamento** (Ralph: o mesmo prompt em laço, uma coisa por volta, a mesma pilha a cada volta;
  fonte: ghuntley.com/ralph): `.scratch/construcao-do-hub/planejamento/` (`PROMPT.md`, `plano.md` como fonte única,
  `voltas.md`, `agentes/`). O maestro manda o mesmo prompt aos 12 a cada volta e para quando uma volta inteira não muda
  o plano; o maestro só observa e responde. Os recrutas nascem por `recrutar.sh` (rodado pelo Gustavo: o classificador
  barra o `recruit` com `--permission-mode auto` nesta sessão). Depois: o plano vai ao portal para aprovação.
- 2026-10-15 ~21h30 (Gustavo, no terminal): "não precisa criar o desenho do laço no portal mais, já aprovei e você
  começou". O laço está aprovado; o plano da rodada Ralph segue para a spec sem carta; só as "Perguntas ao Gustavo" do
  plano, se houver, vão ao portal. Pedido junto: desligar todo agente fora de qualquer frente e parado. Conferido: os 12
  da construção estão na volta 1; a equipe de design está na frente do painel; o Designer está parado, mas na frente do
  ticket 56 (troca do `system-design.html` se a carta da amostra for aprovada); o "Portal" é o terminal do servidor.
  Ninguém desligado.
- 2026-10-15 ~21h45 (Gustavo): 40 minutos para avançar o máximo; criou um segundo maestro, **"Amigo do Maestro"**,
  ligado ao maestro, e pediu que ele pegasse parte da construção ("se ele ficar só com o painel fica fraco"). Divisão
  (`.scratch/construcao-do-hub/maestro-2.md`): o Amigo toca a frente do painel, o Designer e a rodada Ralph (no máximo 2
  voltas) e, na execução, Worker 6 a 10 e o Prumo 2; o maestro escreve a spec e toca Worker 1 a 5 e o Prumo.
- 2026-10-15 ~21h50: **`/to-spec` invocado pelo Gustavo** ("com subagentes pra te ajudar, mas os workers devem arrumar
  possíveis erros também"). Spec em `.scratch/construcao-do-hub/spec.md`, organizada pelas 10 faixas que o Worker 2 propôs
  na volta 1 do plano; 5 subagentes escrevem duas faixas cada em `spec-partes/`; na volta 2 da rodada Ralph os workers
  corrigem a parte da sua faixa. Tickets de construção em `.scratch/construcao-do-hub/issues/`.
- 2026-10-15 ~22h: volta 1 da rodada Ralph fechou as 10 faixas no `plano.md` (cada uma com entrega, prova e como segue
  sem esperar). **Rodada 2 aberta** (`portal/rodadas/2026-10-15-passagem-para-a-construcao-r2.md`) com as quatro
  perguntas do plano ao Gustavo: Docker de ensaio (o Docker Desktop está desligado), login dos harnesses no HOME de
  ensaio, copiar os pilotos do vault, teste do gemini pelo FreeLLMAPI (recomendadas: A nas quatro).
- 2026-10-15 ~22h10: **`/to-tickets` invocado pelo Gustavo.** Com ~10 minutos restando, o maestro publicou direto, sem a
  rodada de conferência da skill: 10 tickets, um por faixa, sem bloqueio entre si (cada faixa segue com dublês), e o 11
  (juntar e provar o hub de ensaio inteiro), bloqueado pelos dez. Spec completa com as cinco partes (398 user stories).
  Ticket resolvido.

## Answer

**A construção do hub tem spec e tickets** (2026-10-15), em `.scratch/construcao-do-hub/`: `spec.md` com as 10 faixas
verticais e as partes em `spec-partes/` (398 user stories, as contradições entre tickets e a decisão que vale), e
`issues/01` a `issues/11` (uma faixa por worker, mais a junção). O laço foi aprovado pelo Gustavo: 10 workers e 2 Prumos
Claude Opus 5.5 alto, todos ligados entre si; faixas por grupo lógico, ninguém esperando ninguém; a execução inteira em 1
hora; antes, uma rodada Ralph dos 12 que fechou o plano (`planejamento/plano.md`). Nada global de verdade sem aval: hub e
HOME de ensaio. A construção segue nos tickets, fora deste mapa.
- 2026-10-15 ~22h20 (Gustavo): "pode parar". O maestro pediu aos 12 recrutas e ao Amigo que parem no próximo ponto, sem
  matar ninguém: nada novo, estado no `## Comments` de cada ticket de construção, commit no próprio ramo, nada em
  `integracao`. A construção retoma pelos tickets `.scratch/construcao-do-hub/issues/` e pelos ramos `faixa-NN` de
  `C:\context-hub`.
- 2026-10-16 ~14h30: **recomeço.** O Gustavo tirou do canvas os 10 workers, os 2 Prumos e o time de design do hub (ficaram
  Designer e Portal) e pediu revisar o spec antes de recomeçar. Ramos: commits parciais só nas faixas 01, 02, 03, 07 e 09,
  nenhuma com teste de ponta a ponta verde; nada em `integracao`; nada apagado.
- 2026-10-16 14:28 (rodada `2026-10-16-revisao-do-spec-r1`, Gustavo): **revisão em duas camadas (A).** O núcleo do spec
  com o Gustavo, uma rodada por bloco, começando pelos pontos abertos e pelo formato da execução; as 398 user stories
  passam por um revisor que confere cada uma contra as decisões fechadas no mapa e só traz as divergências, com o custo
  dito antes de rodar. Comentário: "esse revisor deve estar no canvas do maestri" (recruta no canvas, não subagente).
- 2026-10-16 14:30 (rodada `2026-10-16-revisao-do-spec-r2`, Gustavo): **dois revisores no canvas (C)**, um Codex (GPT 6.1
  Sol médio) e um Claude (Opus 5.5 médio), cada um com metade das partes do spec, sem subagentes, divergências em
  `.scratch/construcao-do-hub/revisao/`; nenhum muda o spec (a recomendada era um Codex só).
- 2026-10-16 ~14h35 (Gustavo, no terminal): **depois da revisão do spec, ajustar o plano de construção.** Ideia inicial
  dele: cada "worker" (faixa) vira uma etapa sequencial, e ele diz como executar cada etapa; "mas ajustemos isso"
  (aberto, vira rodada depois da revisão). Revisores recrutados no canvas: Sextante (Codex GPT 6.1 Sol médio) e Prisma
  (Claude Opus 5.5 médio), papel "Revisor de user stories".
- 2026-10-16 ~14h50: Prisma revisando as faixas 5 a 10. **Sextante bloqueado:** o sandbox do Codex no Windows falha ao
  iniciar (`helper_unknown_error: setup refresh had errors`), nem leitura funciona; o modo automático do maestro recusou
  reiniciá-lo em acesso total ("Create Unsafe Agents"), então o reinício fica com o Gustavo. Rodada aberta:
  `2026-10-16-revisao-do-spec-r3` (núcleo, bloco 1: os sete desempates do spec e o aviso em dobro no Codex).
- 2026-10-16 ~15h: o Gustavo liberou as permissões do Sextante; parte das faixas 1 a 4 reenviada, revisão em curso.
- 2026-10-16 ~15h15: revisão das user stories pronta: Prisma 34 divergências (faixas 5 a 10), Sextante 15 (faixas 1 a 4), em `.scratch/construcao-do-hub/revisao/`. Triagem do maestro em `revisao/triagem.md`: correção mecânica (aval em bloco), escolhas do núcleo sem ticket, decisões de verdade, dependem do formato (vão para o plano). Rodadas saem uma por vez, depois da r3.
- 2026-10-16 14:53 (rodada `2026-10-16-revisao-do-spec-r3`, Gustavo): não respondeu os desempates nem o aviso em dobro;
  **mudou o método**: "3 revisores (1 a mais apenas) conversem entre eles por 5 rodadas até entrar num acordo, à luz de
  TODOS os tickets já definidos, como o spec deve ficar. Você compara a versão de antes (a de agora) com a versão proposta
  deles. Daí sim você me pergunta como o spec deve ficar." A triagem (`revisao/triagem.md`) vira insumo dos revisores,
  não rodada direta.
- 2026-10-16 ~15h25: revisão conversada montada: protocolo em `.scratch/construcao-do-hub/revisao/protocolo.md`; spec atual copiado em `revisao/antes/` (intocável) e `revisao/proposta/` (só o relator edita); conversa em `revisao/conversa/rN-<nome>.md`; fechamento em `revisao/acordo.md`. Relator Quadrante (Claude Fable 5.1 médio, papel "Relator do spec") com Prisma e Sextante, ligados entre si; tickets resolvidos divididos em três terços, o 56 tratado como aberto; formato da execução fica marcado, não decidido.
- 2026-10-16 ~15h35 (Gustavo, no terminal), fatos para o plano: (1) o TI já confirmou que o Tailscale no notebook não
  tem risco, problema nem conflito com o software corporativo; (2) o laço do system design (ticket 56) só continua
  depois da construção; (3) as políticas do Copilot da empresa já foram conferidas: não há política aplicada; (4) ele
  vai ligar o Docker Desktop e criar o repositório privado do hub no GitHub, vazio, para ligar ao `C:\context-hub`.
- 2026-10-16 ~15h45: repositório privado `context-hub` criado pelo Gustavo no GitHub (vazio). Chave de deploy do par 1 gerada em `~/.ssh/context-hub-par1` (ed25519, sem frase-senha, para a cópia diária) e bloco `Host github-context-hub` no `~/.ssh/config`. Falta: o Gustavo colar a pública em Deploy keys com escrita; depois `remote add` e push só do `main`.
- 2026-10-16 ~15h50: deploy key adicionada com escrita; `C:\context-hub` ligado a `git@github-context-hub:pdgusta/context-hub.git` (`origin`), `main` enviado e rastreando `origin/main`. Ramos `faixa-NN` e `integracao` ficam só locais.
- 2026-10-16 ~15h55: Docker Desktop ligado pelo Gustavo; servidor 29.8.2 (linux) respondendo. O aval para a construção usar contêineres de ensaio segue na rodada `passagem-para-a-construcao-r2`, que volta com o plano.
- 2026-10-16 ~16h: rodada `passagem-para-a-construcao-r2` (quatro avais) **suspensa**, sem resposta: as perguntas pressupõem a hora de construção e as faixas; o Docker já está ligado; os avais voltam em rodada nova, escrita a partir do plano revisto.
- 2026-10-16 ~16h40: **revisão conversada fechada** (Quadrante): acordo dos três em tudo, `revisao/acordo.md`; proposta em `revisao/proposta/` (6 arquivos, +337/-213 linhas); `antes/` conferido idêntico ao spec original. Maestro conferiu o núcleo trecho a trecho contra o acordo. 23 escolhas do núcleo sem ticket; 3 itens "se couber" viram requisito (validação de frontmatter no MCP, Config Doctor, ponte do Desktop); o aviso em dobro no Codex já era decisão (os dois ficam). Rodada aberta: `2026-10-16-revisao-do-spec-r4`. Ficam para a rodada do plano: formato, 3 lacunas de dono, aval dos bancos de ensaio no Docker (dúvida do Quadrante).
- 2026-10-16 15:40 (rodada `2026-10-16-revisao-do-spec-r4`, Gustavo): **a proposta vira o spec (A).** Aplicado: `spec.md`
  e `spec-partes/` de `.scratch/construcao-do-hub/` trocados pela `revisao/proposta/` (hashes conferidos); a versão de
  antes fica em `revisao/antes/`. **As 23 escolhas sem ticket ficam abertas**: "divida essas 23 escolhas em 4 cartas
  visuais, cada uma é uma rodada. Pode colocar 1 'designer de visuais' pra cada".
- 2026-10-16 ~16h55: 4 cartas das 23 escolhas em produção, brief em `.scratch/construcao-do-hub/revisao/cartas/brief.md`: Designer (gravar e ler no banco: 1-5, 21), Aquarela (vigia e manutenção: 6-10, 22), Nanquim (busca: 11-13, 23), Guache (frontmatter, hooks e acervo: 14-20); todos Claude Opus 5.5 alto, papel "Designer de visuais" (o Designer antigo tinha saído do canvas; recrutado de novo). O maestro cadastra cada carta no `cartas.json` e abre uma rodada por carta, com uma pergunta por escolha na ordem da carta.
- 2026-10-16 ~17h10: a pedido do Gustavo, o maestro agradeceu aos revisores; cada um gravou as lições do processo em `.scratch/construcao-do-hub/revisao/licoes/` (prisma, quadrante, sextante), insumo da rodada do plano; os três saíram do canvas.
- 2026-10-16 ~17h15 (Gustavo): dois revisores de UI/UX para as cartas, papel "Revisor de cartas UI/UX" (Claude Opus 5.5 médio): Lente (Designer e Aquarela) e Esquadro (Nanquim e Guache), ligados aos seus designers; pareceres em `revisao/cartas/parecer-carta-N.md`, até duas voltas; o aviso ao maestro só depois do "passa". Fluxo no fim do `revisao/cartas/brief.md`.
- 2026-10-16 ~17h30: carta 2 (vigia e manutenção, escolhas 6-10 e 22) passou no Lente na volta 2; cadastrada como `escolhas-2-vigia` no `cartas.json`; rodada aberta `2026-10-16-escolhas-do-spec-carta-2` (uma pergunta por folha, na ordem da carta).
- 2026-10-16 ~17h40: carta 3 (busca, escolhas 11-13 e 23) passou no Esquadro na volta 2; cadastrada como `escolhas-3-busca`; rodada aberta `2026-10-16-escolhas-do-spec-carta-3`. Nanquim sobe os rótulos do celular para 12 px.
- 2026-10-16 ~17h50: cartas 1 (gravar e ler no banco, escolhas 1-5 e 21; Lente) e 4 (ficha, porteiros e acervo, escolhas 14-20; Esquadro) passaram na volta 2; cadastradas `escolhas-1-banco` e `escolhas-4-regras`; rodadas abertas `2026-10-16-escolhas-do-spec-carta-1` e `-carta-4`. As quatro rodadas das 23 escolhas estão no portal.
- 2026-10-16 16:33 (rodada `escolhas-do-spec-carta-2`, Gustavo): as seis escolhas da vigia e manutenção (6-10, 22) aceitas como recomendado; a 22 vira regra: os dois avisos do Codex não se repetem enquanto o estado não muda. Registro em `.scratch/construcao-do-hub/revisao/escolhas-decididas.md`; o spec é atualizado numa passada só quando as quatro rodadas fecharem.
- 2026-10-16 16:33 (Gustavo): carta `escolhas-2-vigia` aprovada: "perfeito, gostei demais do design dessa carta" (caderno de aquarela do faroleiro, da Aquarela).
- 2026-10-16 16:52 (rodada `escolhas-do-spec-carta-1`, Gustavo): escolhas 1-4 e 21 aceitas; **a 5 mudou para B: três instâncias do MCP do banco por máquina** (leitura, escrita da máquina e escrita só do cliente). Registro em `revisao/escolhas-decididas.md`.
- 2026-10-16 16:52 (Gustavo): carta `escolhas-1-banco` aprovada: "carta bastante criativa, parabéns" (a agência com guichês e cofre, do Designer).
- 2026-10-16 17:14 (rodada `escolhas-do-spec-carta-4`, Gustavo): escolhas 14, 15, 17, 18 e 19 aceitas; **a 20 mudou para
  B: o `AGENTS.md` da iniciativa nasce à mão**, só com regra própria; a 16 ficou em branco com a pergunta "pq essa opção
  não é um hook ou claude mod, mas sim um script?" (sem mudar o visual): volta em rodada nova. Carta `escolhas-4-regras`
  aprovada, sem comentário.
- 2026-10-16 17:21 (rodada `escolhas-do-spec-carta-3`, Gustavo): escolhas 12, 13 e 23 aceitas; **a 11 ajustada: "entre as 3 primeiras, mas tempo só medido"** (sem o limite de 60 s).
- 2026-10-16 17:39 (rodada `escolhas-do-spec-carta-4-r2`, Gustavo): fim da resposta com regra fixa, sem IA, dentro do mod e dos hooks (A). As 23 escolhas estão decididas; o maestro aplica no spec numa passada só.
- 2026-10-16 ~18h: **as 23 escolhas aplicadas no spec** (marcas [núcleo] → [aceita]; as quatro mudanças do Gustavo escritas; cópia anterior em `revisao/antes-das-escolhas/`). Próximo passo: a rodada do plano de construção (formato da execução, ideia das etapas sequenciais, as três lacunas de dono, os avais suspensos e o Docker de ensaio), com as lições dos revisores em `revisao/licoes/`.
- 2026-10-16 ~18h05 (Gustavo): para as cartas do plano ficam só um designer e um revisor: **Aquarela** (designer da carta 2, a elogiada) e **Lente** (revisor de UI/UX dela). Designer, Nanquim, Guache e Esquadro saíram do canvas, ociosos, com o trabalho gravado em `revisao/cartas/`.
- 2026-10-16 ~18h15: rodada do plano em preparo. Proposta do maestro em `.scratch/construcao-do-hub/revisao/plano/proposta-de-etapas.md`: etapa 0 de provas de risco, depois as faixas na ordem 1, 4, 5, 3, 6, 7, 2, 9, 10, 8 e a junção, cada etapa com a entrega real da anterior; ramos de ontem guardados como `ontem/faixa-NN`; receita de cada etapa proposta pelo maestro e ajustada pelo Gustavo antes dela; perguntas de login, pilotos, gemini, Docker e as três lacunas de dono vão na hora da etapa que as usa. Carta pela Aquarela, revisão do Lente (`revisao/plano/brief-carta.md`).
- 2026-10-16 ~18h30 (Gustavo, no terminal): repositórios de código ficam **fora do hub** (confirma o 12 e a porta do repositório fora do hub do 36/42). Repositório numa pasta `local: true` dentro do hub foi para o radar como tema a testar.
- 2026-10-16 ~18h45: carta `plano-de-construcao` (Aquarela, ateliê de costura; Lente passou na volta 2) cadastrada; rodada aberta `2026-10-16-plano-de-construcao-r1` (ordem das etapas, etapa zero, ramos de ontem, receita de cada etapa).
- 2026-10-16 18:32 (rodada `2026-10-16-plano-de-construcao-r1`, Gustavo):
  1. **Ordem A, com paralelismo de até 3 agentes** (resposta condicional: "se não der, escolho a opção A"; dá): as etapas
     seguem em sequência, e até 3 agentes podem adiantar ao mesmo tempo **só o que não depende do trabalho das etapas
     anteriores** (nada construído sobre peça que ainda não existe, o erro do plano de 1 hora).
  2. **Etapa zero (A)**, com o pedido: "testar porém já tentando prever dificuldades ao ligar o resultado final com o que
     foi testado" (as provas usam a forma de configuração da construção e registram o que vai doer na hora de ligar).
  3. **Ramos de ontem guardados (A), com outro nome** ("'ontem/' é um nome horrível"): renomeados para
     `tentativa-paralela/faixa-NN`; worktrees tiradas; os arquivos soltos das faixas 06 e 10 viraram um commit em seus
     ramos antes. Sobrou `C:\context-hub-wt\faixa-10-ferramentas\` (o download do mcp-proxy 1.1.0), intocado.
  4. **Receita por etapa (A)**, como ele explicou: a cada etapa o maestro propõe como seguir **conforme o resultado e o
     estado da etapa anterior** e diz **o que os agentes já anteciparam** da etapa proposta.
- 2026-10-16 18:34 (Gustavo): carta `plano-de-construcao` aprovada: "design incrível também. Os designers estão pegando o jeito. Só achei a tipografia dos títulos difícil de ler." Rodada aberta: `2026-10-16-etapa-0-receita` (quem trabalha, adiantar o esqueleto, Docker de ensaio, login do Codex no ensaio).
- 2026-10-16 18:38 (rodada `2026-10-16-etapa-0-receita`, Gustavo, todas A): dois construtores Claude Opus 5.5 médio (provas
  1 e 2; prova 3) e um revisor Codex com acesso total, iniciado pelo Gustavo; um terceiro construtor adianta a etapa 1
  (esqueleto); CouchDB de ensaio no Docker em 127.0.0.1, apagados ao fim; login do Codex copiado para a pasta de
  configuração de ensaio só durante a prova 3 e apagado ao fim.
- 2026-10-16 ~18h55: **construção em etapas começou.** Regras comuns em `.scratch/construcao-do-hub/etapas/regras-da-construcao.md`; briefs em `etapas/00-provas/brief.md` e `etapas/01-esqueleto/brief.md`. Papéis "Construtor do hub" e "Revisor da construção". Construtores Claude Opus 5.5 médio: Brasa (provas 1 e 2, ramo `etapa-00-banco`), Vela (prova 3, `etapa-00-codex`), Trilho (etapa 1 adiantada, `etapa-01-esqueleto`). Revisor Codex "Fiel" com acesso total: o Gustavo inicia (o modo automático do maestro recusa criar agente sem sandbox).
- 2026-10-16 ~19h: o Gustavo perguntou "eu não tinha que rodar o implement-spec?". Sim: pelo `AGENTS.md`, a construção vai por `/implement-spec`, invocado por ele, e os tickets vêm de `/to-tickets`. O maestro tinha despachado Brasa, Vela e Trilho direto (erro de processo); os três foram parados no próximo ponto seguro, mal tinham começado. Os tickets atuais (`.scratch/construcao-do-hub/issues/01`-`11`) são do plano de 1 hora e do spec antigo: precisam de `/to-tickets` sobre o spec revisto, com os bloqueios das etapas decididas.
- 2026-10-16 ~19h15: **`/to-tickets` invocado pelo Gustavo.** Proposta de 26 tickets em `.scratch/construcao-do-hub/rascunhos/tickets-proposta.md` (etapa zero 01-03, esqueleto 04-06, banco 07-08, MCP 09-11, busca 12-13, guardas 14-15, vigia 16-17, retomada 18, skills e acervo 19-20, manutenção e cliente 21-22, kit de par 23-24, junção 25, instalação real 26 ready-for-human). Quiz da skill na rodada `2026-10-16-tickets-da-construcao`. Os 11 tickets antigos vão para `issues-tentativa-paralela/` na publicação.
- 2026-10-16 ~19h20: o Gustavo iniciou o revisor Codex **Fiel** (acesso total, papel "Revisor da construção"); o maestro o ligou a Brasa, Vela e Trilho. Os quatro ficam parados até os tickets serem publicados e o `/implement-spec` ser invocado.
- 2026-10-16 18:47 (rodada `2026-10-16-tickets-da-construcao`, Gustavo): granularidade e bloqueios aprovados (A e A), com
  a pergunta "não eram 11 etapas? Pq viraram 26? O que isso impacta no plano?" (respondida no terminal: as etapas seguem
  11 mais a zero; os 26 tickets são as fatias dentro delas). **Tickets publicados** em
  `.scratch/construcao-do-hub/issues/01`-`26` (o 26 `ready-for-human`); os 11 antigos em `issues-tentativa-paralela/`.
  Próximo passo do fluxo: `/implement-spec`, invocado pelo Gustavo.
- 2026-10-16 ~19h35: **`/implement-spec` invocado pelo Gustavo.** Ramo de integração: `integracao` (já existe, igual a `main`). Adaptado às decisões dele: implementadores são recrutas no canvas (Brasa, Vela, Trilho), não subagentes escondidos; revisor Codex Fiel antes de juntar; até 3 agentes; um ramo e uma worktree por ticket (`ticket-NN`); o maestro junta em `integracao` e resolve o ticket. Fronteira inicial pela receita da etapa zero: Brasa 01 e 02, Vela 03, Trilho 04 (depois 05).
- 2026-10-16 ~19h45: o Trilho (ticket 04) perguntou onde mora o código do hub (o spec antigo punha `kit/`, `hooks/`, `mods/`, `busca/` na raiz; o 12 decidiu raiz = `AGENTS.md` + seis raízes, oficina em `agents/`, sem dizer onde fica o código dentro dela) e propôs o script do hub de ensaio (padrão `C:\context-hub-ensaio`, `.git` próprio). Maestro: hub de ensaio aceito; o lugar do código vai na rodada `2026-10-16-onde-mora-o-codigo-do-hub`; até lá o `verificar-hub` só avisa pasta a mais na raiz.
- 2026-10-16 ~19h55 (Gustavo, no terminal): a nota de retomada com várias sessões no mesmo trabalho (maestro, sessão sozinha, recrutas) "vai ser um saco"; revisar depois. Proposta do maestro em `.scratch/construcao-do-hub/rascunhos/retomada-com-varias-sessoes.md`; anotada no ticket 18 como pergunta a decidir antes dele.
- 2026-10-16 19:06 (rodada `2026-10-16-onde-mora-o-codigo-do-hub`, Gustavo): não escolheu; perguntou "qual a diferença entre isso tudo virar skill e ficar só no agents/ ?". Resposta na rodada nova `2026-10-16-onde-mora-o-codigo-do-hub-r2`: funciona igual; a diferença é quem lê (o `SKILL.md` é manual para agente; hooks, mod, kit, verificador e testes ninguém chama numa sessão) e a mistura do motor com o acervo da guarda. Recomendação mudou de "tudo skill" para **C**: o que o agente chama vira skill; o que o harness ou o kit roda vai em `agents/code/` (uma pasta nova em `agents/`). Até a resposta, o Trilho mantém os provisórios `agents/bin/` e `agents/test/`.
- 2026-10-16 19:12 (rodada `2026-10-16-onde-mora-o-codigo-do-hub-r2`, Gustavo): **C, pelo critério "quem chama".** O que um agente chama vira skill em `agents/skills/<peça>/` (busca, "nova iniciativa", vigia com `vigia recuperar`, arquivar); o que só o harness ou o kit roda vai em `agents/code/` (`hooks/`, `mods/`, `kit/`, `bin/`, `test/`). Acrescenta uma pasta ao conteúdo de `agents/` fixado no ticket 12. Aplicado no spec (caminhos `kit/`, `hooks/`, `mods/`, `busca/` trocados; nota no topo; cópia em `construcao-do-hub/revisao/antes-do-lugar-do-codigo/`) e nas regras da construção; repassado a Trilho, Brasa, Vela e Fiel. As provas da etapa zero vão para `agents/code/test/provas/`.
- 2026-10-16 ~21h: ticket 04 juntado em `integracao` (b68f540) e resolvido; Trilho no 05. Ele trouxe quatro pontos: o caminho sem tipo no catálogo (só campos comuns e aviso, sem recusa) o maestro aceitou como técnico; os outros três foram para a rodada `2026-10-16-ticket-05-perguntas-do-trilho` (escopo do verificador fora dos 26 tickets, tabela `stage` → `status`, se `operations/` conta como iniciativa), com as recomendadas como provisórias.
- 2026-10-16 19:21 (rodada `2026-10-16-ticket-05-perguntas-do-trilho`, Gustavo, todas A): (1) as quatro tarefas do verificador fora dos 26 tickets (`index.md`, links `par://`, `other/`, fim da resposta) viram o **ticket 27** da construção, etapa 1, bloqueado por 05 e 06 (o 23 passa a esperar o 27); (2) a **tabela `stage` → `status`** do Trilho (registrada no spec, faixa 1, pontos abertos); (3) **`operations/<operação>/` não conta como iniciativa**: só `clients/<cliente>/<iniciativa>/` e `initiatives/<iniciativa>/` exigem `initiative`. Antes, ~21h20: ticket 03 resolvido e juntado (3857c98); o 02 passou da Brasa para a Vela.
- 2026-10-16 ~21h45 (Gustavo, no terminal): "você é o maestro e deve estar sempre disponível pra orquestrar": as junções em `integracao` passam ao recruta **Rebite** (Claude, papel "Integrador da construção", procedimento `construcao-do-hub/etapas/juntar-tickets.md`); os construtores avisam o Rebite, que junta, testa, resolve e avisa o maestro.
- 2026-10-16 ~21h55 (Gustavo): o Fiel ganha um parceiro, **Fielzinho** (Codex GPT 6-Astra médio, acesso total, papel "Revisor parceiro da construção"), iniciado pelo Gustavo. Revisão em dupla: cada um revisa sozinho, conversam até o acordo, o Fiel fecha o parecer único; passa só com os dois de acordo (`construcao-do-hub/etapas/revisao-em-dupla.md`).
- 2026-10-16 ~20h30 (maestro): o Trilho pediu aval para copiar os logins dos três harnesses para pastas de ensaio (ponta a ponta do 14). Rodada aberta `2026-10-16-login-dos-harnesses-no-ensaio`, valendo para a construção inteira (11, 17, 18, 24 vão pedir o mesmo); até a resposta, o Trilho fecha só a prova pelos eventos gravados.
- 2026-10-16 20:24 (rodada `2026-10-16-login-dos-harnesses-no-ensaio`, Gustavo): **A, aval para a construção inteira.** Qualquer ticket que precise dos harnesses de verdade copia o login dos três para uma pasta de ensaio em `%TEMP%` (Claude: `.credentials.json` em `CLAUDE_CONFIG_DIR`; Codex: `auth.json` em `CODEX_HOME`; Copilot: só os campos de login no `config.json` do `COPILOT_HOME`, token no cofre do Windows, sem cópia), apaga ao fim de cada rodada, confere as pastas reais por hash antes e depois, usa modelos baratos e registra cada uso no relatório. Escrito nas regras da construção; anotado nos tickets 11, 14, 17, 18 e 24.
- 2026-10-16 20:30 (rodada `2026-10-16-etapa-2-receita`, Gustavo): **A.** Etapa 2 (banco): a Brasa (Claude Opus 5.5 médio) faz o 07 e depois o 08; bancos de ensaio no Docker em 127.0.0.1, apagados ao fim; revisão em dupla Fiel e Fielzinho; o Rebite junta.
