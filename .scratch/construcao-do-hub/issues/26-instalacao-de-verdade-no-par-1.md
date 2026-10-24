# 26: Instalação de verdade nos dois primeiros pares (com o Gustavo)

Type: task
Status: resolved
Etapa: depois da junção
Blocked by: 25, 45, 46 (todos resolvidos)

**What to build:** O hub de verdade nas **duas máquinas**, no mesmo ciclo, à vista do Gustavo (decisão dele, 2026-10-17
~20h, no chat do maestro: prefere ver os efeitos depois de instalar no outro PC a testar sozinho aqui e achar os
problemas só na hora de transportar).
1. **Par 1 (esta máquina):** o kit no HOME real, com cópia e hash antes (desfazer possível).
2. **Par 2 (o outro PC):** lá há Claude Code, Maestri e permissão de administrador, e dá para clonar o repositório do
   hub. O primeiro setup entre os dois primeiros pares pode ser **do jeito mais adequado** (não precisa ser o fluxo
   genérico de "novo par"); esperar o par 2 receber o hub (semente de minutos) e conferir que uma nota gravada num lado
   aparece no outro.
3. Depois, uso normal nas duas; o que aparecer vira ticket de conserto.
O fluxo de **setup num par novo** (genérico, repetível) fica para depois, ajustado com o que se aprender aqui.

**Fonte:** Spec, "Instalar em arquivo global de verdade... sem o aval do Gustavo" (fora de escopo das etapas). Regras comuns: `../etapas/regras-da-construcao.md`.

**Blocked by:** 25 (Junção e prova do hub de ensaio inteiro)

- [x] o kit roda no HOME real com cópia e hash antes
- [x] o Gustavo confere os três harnesses na pasta real

## Comments

- 08:42 (maestro): do 23 (Cinzel): o Copilot não tem chave de configuração nem variável para as instruções do servidor MCP; só a opção `--allow-all-mcp-server-instructions` na linha de comando. Quem abre o Copilot (o preset do Maestri, um atalho) tem de passá-la.
- 2026-10-17 19h50 (maestro): da reprodução do 25 (Brasa, `../etapas/diagnostico-25-nota-nao-desce.md`): um par novo leva minutos para receber o hub (semente de ~520 arquivos, ~4-7 min no ensaio). Na instalação do 2º par, avisar ou esperar a convergência antes de dar por pronto. Também: o 25 fechou o Codex nas fases 1-3 do hub inteiro; nas fases 4-7 o Codex está provado nos tickets de cada peça (17, 18, 21, 22); rodar o Codex nas fases 4-7 do 25 fica opcional, se quiser antes da instalação.
- 2026-10-17 ~20h (Gustavo, chat do maestro): escopo trocado para as duas máquinas (acima). O maestro do outro PC
  será outra sessão; achar um jeito de os dois maestros se comunicarem (pergunta aberta; candidato natural: o próprio
  hub replicado entre os pares, ver o radar na retomada do maestro). Roteiro do 26 a preparar depois do reinício.
- 2026-10-17 ~21h40 (maestro, divergência do Lume): nenhum script do kit nem ticket define `HUB_PAR_ID` (sem ela, nenhum link fora do hub vira `par://`); anotada em `agents/code/docs/componentes/pastas-e-links.md` §5. Na instalação, o kit de par deve gravar `HUB_PAR_ID` de cada par (ex.: no `.env` do par).
- 2026-10-17 ~21h45 (Gustavo, Maestri Chat, thread blue): (1) A: preparo agora, nos tickets 45 (banco entre duas
  máquinas, Brasa) e 46 (kit para duas máquinas, Cinzel); (2) A: depois do 45 e do 46, o Rebite junta `integracao` no
  `main` do `C:\context-hub` e o **Gustavo** faz o push para `pdgusta/context-hub` e clona no outro PC (o maestro nunca
  faz push); (3) A: o fork e o sincronizador do LiveSync por `git bundle` num pendrive ou pasta dele, o `.env` do par B
  só à mão; (4) Tailscale **ainda não** está nas máquinas: o Gustavo instala nas duas antes do passo 4 do roteiro.
- 2026-10-17 ~22h20 (maestro): passo a passo detalhado mandado ao Gustavo (Maestri Chat, thread roxa): pré-requisitos do par B por winget (Tailscale.Tailscale, Docker.DockerDesktop, OpenJS.NodeJS.LTS, Python.Python.3.12, Microsoft.PowerShell, Git.Git), modo de desenvolvedor; transporte em C:\hub-transporte\ (par-B.env + 2 bundles); clone por https; no par B, o Claude lê `agents/code/docs/instalacao.md` (**a escrever pelo Lume depois do 45 e do 46**).
- 2026-10-17 ~22h40 (maestro): do 45 (Brasa): o index.cjs montado pelo montar-cli-livesync.ps1 tem hash diferente do build daqui (mesmo commit 14141446; npm ci contra o npm install de 13/10). No 26, montar o CLI também no par A, para os dois pares rodarem o mesmo build.
- 2026-10-17 ~23h25 (maestro): ressalvas do Fiel para cá (pareceres do 45 e do 46): HUB_MAQUINA = HUB_PAR_ID (o mesmo nome da máquina; o registro de uso do roteamento passa a <id>.md); `${HUB_BANCO_ENDERECO:?}` no compose; o gerador de .env deve lembrar o `montar-cli-livesync.ps1`.
- 2026-10-18 ~00h25 (maestro): 45 e 46 resolvidos; `main` do hub = 7d0c25d (--no-ff de integracao 8c01cfb), sem push (o push é do Gustavo). Ressalvas do Rebite para cá: do 45, `${HUB_BANCO_ENDERECO:?}` no compose, aviso para endereço fora de 100.64/10, Docker antes do Tailscale não testado, o gerador não manda rodar o montar-cli-livesync, só IPv4 e "dubious ownership" do git; do 46, as ressalvas 1, 3 e 5 da rodada 1. O Lume escreve `agents/code/docs/instalacao.md` para o maestro de cada par seguir.
- 2026-10-18 ~13h (Brasa, leitura no 49): no par A os 523 textos do hub estão em CRLF (core.autocrlf=true do Git for Windows). Se o git do par B tiver autocrlf=false, o clone sai em LF e cada arquivo difere do banco. **No B, conferir `git config --get core.autocrlf` antes de clonar** (deve ser igual ao do A).
- 2026-10-24 ~13h55 (maestro do B, aval do Gustavo): **três harnesses conferidos no B** (lenovo-ideapad), só leitura,
  na pasta real `C:\context-hub`. Claude Code: a sessão do maestro (contrato, lembrete do acervo, MCP hub-banco e
  hub-busca, mods). Codex 0.163.0 (`codex exec -m gpt-6-luna`) e Copilot CLI 1.0.98 (`copilot -p --allow-all-tools`),
  com o mesmo pedido: os dois disseram ter recebido o contrato do AGENTS.md; chamaram `hub-busca/search` e
  `hub-banco/estado_do_hub` (`ok`, envio em dia, outro par ligado); os hooks rodaram (Codex: `PostToolUse` e `Stop`; o
  Copilot leu o `routing.yml` e abriu as skills `busca` e `maestro-acervo`). A pergunta da busca ("como instalar um
  par novo") não achou o guia porque `agents/code/` fica fora da busca de propósito (ticket 41): é escolha da pergunta,
  não falha. `git status` do hub sem mudança. Saídas no scratchpad da sessão (`teste26-codex.txt`,
  `teste26-copilot.txt`). Falta o mesmo no A para marcar a segunda caixa.
- 2026-10-24 ~14h05 (maestro do A): **mesmo teste no A** (armis00323), só leitura, em `C:\context-hub`, pedido do recado do B. **Codex** 0.162.1 (`codex exec -m gpt-6-luna`, saída 0): hooks `SessionStart`, `UserPromptSubmit`, `PostToolUse` e `Stop` rodaram; `hub-busca/search` achou `agents/skills/busca/SKILL.md`; `hub-banco/estado_do_hub`: `ok`, "replicação de envio em dia", outro par ligado; disse ter recebido o contrato do AGENTS.md. **Copilot CLI** 1.0.98 (`copilot -p --allow-all-tools`, saída 1): **bloqueado pela política da organização**. Aqui o Copilot está logado com a conta do GitHub do trabalho (não a pdgusta, como no B): "Third-party MCP servers are disabled by your organization's Copilot policy" (hub-busca e hub-banco bloqueados) e "Access denied by policy settings". Não é defeito do kit. `git status` do hub sem mudança. Saídas no scratchpad da sessão (`teste26-codex.txt`, `teste26-copilot.txt`). Para a segunda caixa: decidir com o Gustavo se o Copilot do A entra com a conta pdgusta ou se o 26 fecha com o Copilot do A fora (anotado).
- 2026-10-24 ~14h25 (maestro do B): **resolvido.** Gustavo (Maestri Chat, thread azul): o Copilot das duas máquinas usa
  a conta do trabalho e deixa de usar MCP; os MCP do hub ficam só no Claude Code e no Codex. Com isso, a segunda caixa
  fica assim: Claude Code e Codex conferidos nas duas máquinas com contrato, hooks, busca e banco; Copilot conferido no
  B com MCP (conta antiga). A mudança para "Copilot sem MCP" é o ticket 55.
- 2026-10-24 ~14h35 (maestro do A): o Copilot do A foi logado na conta SSO do trabalho e o teste passou com MCP (hub-banco e hub-busca), contrato recebido; hub sem mudança. O bloqueio anterior era da conta antiga. Os três harnesses ficam conferidos com MCP nas duas máquinas. Saída: `teste26-copilot-sso.txt` no scratchpad da sessão do A. Consequência para o 55: comentário lá.
