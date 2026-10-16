# Testes das portas de entrada

Type: task
Status: resolved

## Question

Rodar os testes que "Portas de entrada: pesquisa" deixou em "Precisa de teste", para que "Portas de
entrada do hub" e o resto de "Arquitetura de pastas e frontmatter do hub" decidam só com fato. Pedido
do Gustavo em 2026-10-10 (resposta à R21): grupos A, B, C e D, sem consulta ao TI.

Grupos (detalhe em `exploracao/anexos/pesquisa-37-portas/porta-*.md`, seção "Precisa de teste"):
- **A. Carga de instruções (AFK, pasta de teste):** quais `AGENTS.md`/`CLAUDE.md` o Claude Code, o
  Codex e o Copilot CLI carregam na raiz e numa subpasta de um hub sem `.git`; `CLAUDE.md` acima
  desligando o `AGENTS.md`; papel do Maestri com e sem `claude-md-and-agents-md` (via `--settings`, sem
  mexer no `~/.claude/settings.json`); `@C:/...` no `CLAUDE.md` global; skill por junction;
  `project_root_markers` no Codex; `COPILOT_CUSTOM_INSTRUCTIONS_DIRS`.
- **B. Obsidian e LiveSync (HITL, ambiente do spike em `C:\Projetos\spike-livesync`):** mover pasta
  para `_archive/` com links e com a outra máquina editando; mover por script; pastas com ponto no
  explorador.
- **C. es617 (ambiente do spike):** corte do `instructions` (2.048 caracteres no Claude Code),
  `READ_ONLY`, duas instâncias no mesmo CouchDB, `search_notes`.
- **D. Tailscale (HITL: instalação e login):** MCP local do Desktop pela tailnet; conector remoto com
  URL da tailnet (esperado falhar); nó efêmero; grants por tag e porta.

## Comments

- 2026-10-10: o Gustavo dispensou a consulta ao TI antes do Tailscale ("o D não precisa de consulta à
  TI nenhum. Posso tudo"). "Claude (com work)" é o modo chat do Claude Desktop, que agora junta chat e
  work (Cowork), fora do modo Code.
- 2026-10-10: Docker Desktop parado nesta máquina; B e C precisam dele ligado.
- 2026-10-10: **grupo A feito** (`exploracao/anexos/testes-38-portas/grupo-a-carga-de-instrucoes.md`).
  Os três harnesses leem o `AGENTS.md` da raiz quando abrem nela. Numa subpasta, o Claude Code lê a
  cadeia inteira; o Codex só com `project_root_markers` (marcador na raiz do hub); o Copilot CLI só
  com `.git` na raiz do hub. Um `CLAUDE.md` em qualquer pasta acima do hub desliga todos os
  `AGENTS.md`. O papel real do Maestri só recebe o `AGENTS.md` com `claude-md-and-agents-md`.
  Import absoluto no `CLAUDE.md` global e skill por junction funcionam no Claude Code.
- 2026-10-10: **grupo C feito** (`exploracao/anexos/testes-38-portas/grupo-c-es617.md`). `READ_ONLY`
  tira as ferramentas de escrita e recusa a chamada direta; duas instâncias convivem no mesmo
  CouchDB; `search_notes` existe só na imagem de 2026-10-09; o `instructions` do MCP chega só ao
  Claude Code, cortado depois de uns 3.300 caracteres; Codex e Copilot não o recebem.
- Grupos B (Obsidian) e D (Tailscale) precisam do Gustavo na tela: roteiro mandado no chat.
- 2026-10-10: **grupo B feito** com o Gustavo (`exploracao/anexos/testes-38-portas/grupo-b-obsidian-livesync.md`).
  Mover pasta sem edição concorrente funciona (Obsidian ou disco). Mover com a outra máquina editando
  gera conflito "editado × apagado" no caminho antigo, e a edição fica separada da nota. O Obsidian
  reescreve links para a forma curta. Pastas com ponto não aparecem nem replicam; `agents/` sim.
- 2026-10-11: **grupo D feito** com o Gustavo (`exploracao/anexos/testes-38-portas/grupo-d-tailscale-e-claude-desktop.md`).
  Grant por tag e porta funciona; o Claude Desktop (chat/work) só chega ao hub por MCP local stdio
  (ponte `mcp-remote` para a URL da tailnet), e o `instructions` do MCP não chega a ele; conector
  remoto por http é barrado no formulário (teste com HTTPS pulado pelo Gustavo).
- **Pendente para fechar este ticket:** o tempo até o nó efêmero `cliente-teste` sumir da tailnet. O
  contêiner foi apagado às 2026-10-11T03:08:52Z, sem `tailscale logout`. Conferir com
  `"C:\Program Files\Tailscale\tailscale.exe" status` (o nó some da lista) ou no painel (Machines);
  anotar o horário no arquivo do grupo D e então resolver o ticket com um Answer que junte os grupos
  A a D.
- Sessão parada pelo Gustavo em 2026-10-11 (vai dar `/clear`). Docker Desktop ficou ligado; spike
  parado.
- 2026-10-11: o cronômetro em segundo plano foi parado pelo Claude Code por falta de memória na
  máquina. Conferência manual às 03:43:35Z (35 minutos depois): o nó `cliente-teste` ainda estava na
  tailnet. O pendente acima continua valendo.
- 2026-10-12: o nó `cliente-teste` não aparece mais no `tailscale status` (16:57:02Z). Anotado no
  grupo D; o momento exato da saída não foi medido (entre 35 min e cerca de 38 h).

## Answer

Os quatro grupos rodaram; detalhe e método em `exploracao/anexos/testes-38-portas/`.

- **A. Carga de instruções:** aberta na raiz, toda sessão (Claude Code, Codex, Copilot CLI) lê o
  `AGENTS.md` do hub. Numa subpasta, o Claude Code lê a cadeia sozinho; o Codex precisa de
  `project_root_markers` e o Copilot CLI de `.git` na raiz do hub. Um `CLAUDE.md` em qualquer pasta
  acima do hub desliga todos os `AGENTS.md`. O papel do Maestri só recebe o `AGENTS.md` do hub com
  `claude-md-and-agents-md`. Para um repositório fora do hub, import absoluto no `CLAUDE.md` global e
  skill por junction funcionam no Claude Code.
- **B. Obsidian e LiveSync:** mover pasta funciona sem edição concorrente; com a outra máquina
  editando, a edição fica separada da nota no caminho antigo (conflito "editado × apagado"). O
  Obsidian reescreve links na forma curta. Pastas com ponto não aparecem nem replicam; `agents/` sim.
- **C. MCP do es617:** `READ_ONLY` funciona no servidor; duas instâncias convivem no mesmo CouchDB;
  `search_notes` só na imagem de 2026-10-09; o `instructions` do MCP chega só ao Claude Code, cortado
  depois de uns 3.300 caracteres.
- **D. Tailscale e Claude Desktop:** grant por tag e porta funciona; o Claude Desktop (chat/work) só
  chega ao hub por MCP local stdio (ponte `mcp-remote` para a URL da tailnet) e não recebe o
  `instructions`; conector remoto por http é barrado (HTTPS não testado, a pedido do Gustavo); um nó
  efêmero apagado sem `logout` sai sozinho, mas leva mais de 35 minutos.
