# Como os agentes gravam no hub

Type: prototype
Status: resolved
Blocked by: 09, 10, 25

## Question

O agente grava direto no disco, pelo MCP ou pelos dois? Como relê antes de gravar e se protege por
versão? Toda gravação termina como `.md` no disco (Q5). Inclui "redesenhar como agentes editam o
context-hub" (Q8).

## Comments

- 2026-10-01 (vinda de "Windows ou WSL", rodada 1): ideia do Gustavo, a "luva anticongelamento".
  O agente só consulta o contexto pela camada de busca (MCP) e não lê o hub do jeito que quiser, para
  economizar tokens. Ele mesmo duvida que valha ("talvez o ganho seja só com arquivos muito grandes ou
  em grande quantidade"). Pontos de contato: o critério 3 do destino (o agente também edita direto no
  disco), a §6.2 da exploração (Guild como porta única, substituída na §9) e a lição 4 de "Lições do
  vault" (a camada de busca é a porta de entrada, não a única porta). Decidir aqui se é porta única,
  porta de entrada ou nada, e se isso vale para a leitura, para a gravação ou para as duas.
- 2026-10-02 (vinda de "Divergência e edição concorrente"): a garantia está fixada. Nenhuma gravação
  desfaz outra sem que o agente veja: se o arquivo mudou desde a leitura, a gravação é recusada, e o
  agente relê e refaz. Vale para a gravação direta no disco e para a do MCP. O sincronizador também
  grava no disco e não respeita trava, por isso a trava por arquivo foi descartada. Decidir aqui como
  cada harness e o MCP cumprem isso. Não verificado: quais ferramentas nativas de edição (Claude
  Code, Codex, Copilot) já recusam gravar um arquivo que mudou desde a leitura.
- 2026-10-04 (vinda de "Markdown: vista ou fonte da verdade"): em revisão: a verdade mora num banco, e o `.md` é a vista editável do Gustavo. A Q5 caiu. A pergunta "direto no disco, pelo MCP ou os dois" muda de sentido.
- 2026-10-06 (vinda de "Como a verdade viaja entre as máquinas"): o agente grava pelo MCP do es617
  (fork com `base_rev` e conflito visível). Decidir aqui se ele ainda edita o `.md` direto no disco:
  o plugin LiveSync leva ao banco a edição feita no disco (pegou até com o Obsidian fechado), mas essa
  gravação não confere a base. Antes estava no fog do mapa.
- 2026-10-12 (vinda de "Portas de entrada do hub", revisão da porta do Claude Desktop): o Claude Desktop
  (chat e work, hoje um modo só) também grava no hub; o Gustavo: ele "não deve ser proibido de escrever
  no C:/context-hub diretamente". Fatos de partida (`exploracao/anexos/pesquisa-37-portas/porta-6-claude-sem-disco.md`
  e grupo D de "Testes das portas de entrada"): o Desktop lê e grava pastas locais conectadas ("Claude
  can only read and write files in folders you've connected"); em Pro e Max, desde 2026-10-06, a tarefa
  roda na nuvem e alcança a pasta pelo app aberto; o MCP só chega por ponte stdio (`mcp-remote`), e o
  `instructions` do MCP não chega; se o Desktop lê `AGENTS.md` da pasta não foi verificado (a doc fala de
  "Folder instructions"). Decidir aqui: grava pela pasta conectada (direto no disco), pelo MCP de
  gravação com a guarda de versão, ou pelos dois, e como o contrato chega a ele.
- 2026-10-15 ~14h50: destravado (a "Camada de busca" foi resolvida hoje) e reivindicado pelo maestro. **Rodada 1
  aberta** (`portal/rodadas/2026-10-15-como-os-agentes-gravam-r1.md`), rascunhada por um subagente Opus médio e
  revisada pelo maestro: por onde o agente grava (recomendada: pelos dois caminhos, troca de trecho no disco e
  regravação inteira pelo MCP do banco, com um hook que recusa a regravação inteira no disco), por onde o Claude
  Desktop grava (recomendada: pasta conectada e MCP com escrita) e se o cliente grava (recomendada: gravação ligável
  por cliente). Base da primeira: documentação oficial do Claude Code ("Edit tool behavior" e "Write tool behavior").
  **Não verificado:** o que o `apply_patch` do Codex e a edição do Copilot conferem; se o Cowork lê o `AGENTS.md` e
  confere a versão; se a descrição das ferramentas do MCP chega ao Desktop. Ficou para a rodada 2: a busca como porta
  única de leitura ("luva anticongelamento").
- 2026-10-15 14:54, **rodada 1 respondida** (envio `1b33c719-fc92-41e1-9d5e-5951c15879fb`):
  - **por onde o agente grava = C** (a recomendada era A): antes de decidir, um teste curto do Edit e do Write do Claude
    Code, do `apply_patch` do Codex e da edição do Copilot com o arquivo mudado entre a leitura e a gravação, e do hook
    que recusa a regravação inteira;
  - **Claude Desktop = A:** pelos dois caminhos (pasta conectada no Cowork com "Folder instructions" apontando o
    `AGENTS.md`, e o MCP do banco com escrita pela ponte `mcp-remote`); na pasta conectada, sem a guarda de versão do hub
    até a construção mostrar o que a ferramenta do Cowork confere;
  - **cliente = A:** gravação ligável por cliente (padrão só leitura; uma segunda instância do MCP com escrita e token
    próprio, só na tailnet; a senha do CouchDB só nos pares).
  **Feito:** brief do teste em `bancada-gravacao-brief.md`; o Claude Code e o Copilot com um subagente do maestro, o
  Codex com o recruta Sonda Codex. Entregas em `bancada-gravacao-claude-copilot.md` e `bancada-gravacao-codex.md`.
- 2026-10-15 ~15h: o teste curto foi **interrompido pelo maestro** na pausa (erro: o Gustavo pediu pausa no próximo ponto
  natural). O subagente do Claude Code e do Copilot parou antes de criar arquivos na bancada; a Sonda Codex foi
  interrompida no começo. Globais intactos (hash). Refazer os dois pelo mesmo brief (`bancada-gravacao-brief.md`) ao
  retomar.
- 2026-10-15 ~15h25, **teste curto retomado** (o Gustavo mandou retomar). Sonda Codex entregou
  `bancada-gravacao-codex.md`: o `Update File` do `apply_patch` preserva a mudança externa em outra linha e recusa a
  mudança no próprio trecho; o **`Add File` sobre arquivo existente sobrescreve sem recusar**; o hook `PreToolUse` de
  projeto bloqueou as regravações inteiras testadas e deixou passar o patch parcial e o arquivo novo
  (`workspace-write` + `windows.sandbox="unelevated"`, sem acesso total). Claude Code e Copilot com um subagente, em
  `C:\Projetos\bancada-acesso\gravacao\claude-copilot\`; entrega em `bancada-gravacao-claude-copilot.md`.
- 2026-10-15 ~15h50, **teste curto concluído** (`bancada-gravacao-claude-copilot.md`, `bancada-gravacao-codex.md`). Troca de
  trecho segura nos três (grava mantendo mudança em outra linha; recusa quando o próprio trecho mudou). Regravação
  inteira: o Write do Claude Code recusa arquivo lido e depois mudado (a doc não diz; corrige a tabela da rodada 1), mas
  **regrava sem aviso arquivo existente nunca lido**; o `create` do Copilot recusa qualquer existente; o `Add File` do
  Codex **sobrescreve sem aviso**. Hook antes da ferramenta, no escopo de projeto, recusou a regravação inteira e deixou
  passar troca de trecho e arquivo novo nos três (Claude: `.claude/settings.json` do projeto; Copilot: `.github/hooks/`
  com `GITHUB_COPILOT_PROMPT_MODE_REPO_HOOKS=true` no `-p`; Codex: `workspace-write` + sandbox `unelevated`). Ordem
  leitura → mudança → gravação garantida por hook pós-leitura (Claude/Copilot) e pré-`apply_patch` (Codex). **Não
  verificado:** os mesmos hooks no escopo do usuário. Globais: Codex e Copilot intactos por hash; `~/.claude/settings.json`
  mudou às 15:28:46, sem resto da bancada; causa provável (não verificada): o Claude Code gravou `skipWorkflowUsageWarning`
  quando o maestro lançou o workflow dos juízes do ticket 56 nesse minuto.
  **Rodada 2 aberta** (`portal/rodadas/2026-10-15-como-os-agentes-gravam-r2.md`): a pergunta 1 com o teste (recomendada A).
  A "busca como porta única de leitura" segue para depois.
- 2026-10-15 17:23, **rodada 2 respondida** (envio `a8ce08f5-5db3-491b-806f-4390a520e99d`): **por onde o agente grava = A**
  (a recomendada): pelos dois, cada um no que confere. No disco, só troca de trecho (segura nos três pelo teste); a
  regravação inteira de arquivo existente vai pelo `write_note` do MCP do banco, com a versão lida; um hook antes da
  ferramenta recusa no disco a regravação inteira de arquivo existente (Write do Claude Code, criar e regravação do
  `apply_patch`, criar do Copilot) e manda usar o MCP; arquivo novo nasce no disco.
  **Rodada 3 aberta** (`portal/rodadas/2026-10-15-como-os-agentes-gravam-r3.md`) com o que falta para resolver: a busca
  como porta única de leitura (a "luva anticongelamento"; recomendada: não, porta de entrada pelo contrato) e o que o
  agente faz com a porta do banco fora (lacuna de dono 3 da descrição; recomendada: troca de trecho segue, regravação
  inteira espera, aviso e pendência na nota de retomada).
- 2026-10-15 17:32, **rodada 3 respondida** (envio `cbd97f53-0565-4b26-9726-14428f96e553`):
  - **luva = B** (a recomendada era A): um hook avisa, sem recusar, quando o agente abre um arquivo grande do hub sem ter
    buscado antes na sessão (o tamanho, a construção mede). Pergunta do Gustavo: "e qual seria o comportamento quando o
    agente 'já buscou x arquivo antes na sessão'?" → rodada 4;
  - **banco fora = A:** a troca de trecho segue no disco; a regravação inteira espera a porta voltar; o agente avisa na
    resposta e anota a pendência na nota de retomada; nenhuma gravação sem guarda de versão. Fecha a lacuna de dono 3 da
    descrição.
  **Rodada 4 aberta** (`portal/rodadas/2026-10-15-como-os-agentes-gravam-r4.md`): o aviso quando o agente já buscou
  (recomendada C: veio da busca e lê trecho, calado; veio da busca e lê inteiro grande, "leia o trecho"; não veio de
  busca, "busque antes"; uma vez por arquivo por sessão). Última pergunta do ticket.
- 2026-10-15 17:47, **rodada 4 respondida** (envio `73e9fa2c-0653-4e55-ab8a-9939cc778899`): **aviso = C** (a recomendada):
  veio da busca e lê um trecho, calado; veio da busca e lê inteiro um arquivo grande, "leia o trecho que a busca
  apontou"; não veio de nenhuma busca, "busque antes"; uma vez por arquivo por sessão. Todas as perguntas respondidas.

## Answer

**O agente grava pelos dois caminhos, cada um no que confere: no disco, só troca de trecho; a regravação inteira de um
arquivo que já existe vai pelo `write_note` do MCP do banco, com a versão lida; um hook antes da ferramenta recusa no
disco a regravação inteira e manda usar o MCP; arquivo novo nasce no disco.** Decidido com o Gustavo em 2026-10-15, nas
rodadas 1 a 4 do portal, depois do teste curto na bancada (`bancada-gravacao-claude-copilot.md`,
`bancada-gravacao-codex.md`).

- **Garantia (já fixada):** nenhuma gravação desfaz outra sem que o agente veja; se o arquivo mudou desde a leitura, a
  gravação é recusada, e o agente relê e refaz.
- **O que o teste mostrou (rodada 2):** a troca de trecho é segura nos três harnesses (grava mantendo a mudança em outra
  linha; recusa quando o próprio trecho mudou: Edit do Claude Code, edição do Copilot, `Update File` do `apply_patch`).
  O furo é a regravação inteira: o Write do Claude Code regrava sem aviso um arquivo existente que nunca leu, e o
  `Add File` do Codex sobrescreve sem aviso; o `create` do Copilot recusa qualquer existente. O hook antes da
  ferramenta recusou a regravação inteira e deixou passar a troca de trecho e o arquivo novo nos três (no escopo de
  projeto; Copilot no `-p` com `GITHUB_COPILOT_PROMPT_MODE_REPO_HOOKS=true`; Codex com `workspace-write` e sandbox
  `unelevated`).
- **Por onde o agente grava (rodada 2, A):** troca de trecho no disco; regravação inteira de arquivo existente pelo
  `write_note` do MCP do banco com a versão lida; hook que recusa no disco a regravação inteira (Write do Claude Code,
  criar e regravar do `apply_patch`, criar do Copilot); arquivo novo no disco. Comando de shell (`>`, script) fica
  coberto só pelo contrato.
- **Claude Desktop (rodada 1, A):** pelos dois caminhos: a pasta conectada no Cowork, com "Folder instructions" que
  apontam o `AGENTS.md` da raiz, e o MCP do banco com escrita pela ponte `mcp-remote`. Na pasta conectada, sem a guarda
  de versão do hub até a construção mostrar o que a ferramenta do Cowork confere. O Desktop também usa a busca do hub
  (rodada 8 do "Laço do system design").
- **Cliente (rodada 1, A):** gravação ligável por cliente: o padrão é só leitura; quando o Gustavo quiser, o cliente
  recebe o token de uma segunda instância do MCP do banco, com escrita e a mesma guarda de versão, só na tailnet. A senha
  do CouchDB fica só nos pares. No endereço dos clientes ("Acesso dos agentes: decisão", rodada 7), é a rota
  `/banco-escrita/mcp`, com token próprio.
- **Busca e leitura (rodadas 3 e 4):** a busca é a porta de entrada, não a única. Um hook avisa, sem recusar: veio da
  busca e lê um trecho, calado; veio da busca e lê inteiro um arquivo grande, "leia o trecho que a busca apontou"; não
  veio de nenhuma busca, "busque antes"; uma vez por arquivo por sessão. O hook guarda por sessão o que a busca devolveu
  (no Claude Code, `PostToolUse` recebe `tool_response`) e o que foi aberto. O tamanho de "grande", a construção mede.
- **Banco fora do ar (rodada 3, A):** a troca de trecho segue no disco; a regravação inteira espera a porta voltar; o
  agente avisa na resposta e anota a pendência na nota de retomada. Nenhuma gravação sem guarda de versão.
- **Não verificado, para a construção:** os hooks no escopo do usuário (o teste usou o de projeto); o aviso de leitura no
  Codex e no Copilot, que leem por comando de shell; o que a ferramenta de arquivo do Cowork confere; se a descrição das
  ferramentas do MCP chega ao Desktop; a validação de frontmatter dentro do MCP do banco ("Arquitetura de pastas e
  frontmatter", rodada 18).
