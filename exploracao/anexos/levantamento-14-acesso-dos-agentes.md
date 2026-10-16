# Levantamento para o ticket 14 (Acesso dos agentes: decisão)

Feito em 2026-10-14 por um subagente de leitura (Explore), a partir dos tickets resolvidos, sem fonte nova. Saída de
modelo: confira no ticket citado antes de usar.

Legenda: **[D]** decidido · **[T]** testado · **[P]** pesquisado com fonte, sem teste · **[NV]** não verificado ·
**[—]** não achado. Números são tickets: 01 Lições do vault, 04 Windows ou WSL, 08 Divergência, 09 Camada de busca
(aberto), 10 Contrato file-first, 11 Como os agentes gravam (aberto), 12 Arquitetura de pastas (aberto), 13 Acesso:
pesquisa, 18 Copilot, 25 Como a verdade viaja, 33 Revisão do sync, 34 Onde o servidor mora, 36 Portas de entrada,
37 Portas: pesquisa, 38 Testes das portas, 40 Maestri: padrão e liberdade, 41 Contrato pelo MCP, 42 Porta do
repositório fora do hub, 43 Acervo: pesquisa, 44 Guarda: mods e hooks, 45 Testes do papel, 46 Copilot Enterprise.
EPP = `estrategia-pos-pesquisa.md`.

## Base comum
- Hub em `C:\context-hub` (NTFS) nas duas máquinas; WSL fora [D 04]. Par = CouchDB + MCP do es617 + Obsidian com
  LiveSync; cliente = sem cópia, usa o MCP de um par pela tailnet [D 34]. Porta principal = sessão na raiz; o hub não
  tem `CLAUDE.md` [D 36]. `.git` na raiz de cada máquina, só cópia de segurança [D 33]. Lição 13: adaptadores
  idênticos onde o harness permitir; falha se corrige com mecanismo [D 01].

## 1. Contrato global
- **Claude Code.** Par: raiz e subpasta leem a cadeia de `AGENTS.md` [T 38]; fora do hub, `@C:/context-hub/AGENTS.md`
  no `~/.claude/CLAUDE.md` [D 36; T 38]. Um `CLAUDE.md` acima do hub desliga os `AGENTS.md` [T 38]. Cliente: três
  canais juntos (R33): `instructions` do fork com a cabeça do `AGENTS.md` (≤ 2.000 caracteres), descrição das
  ferramentas de gravação ("antes de gravar, leia AGENTS.md") e config global onde der [D 36]. `instructions` chegou
  cortado após ~3.300 caracteres [T 38]; a doc diz 2.048 [P 37].
- **Codex.** Par: `~/.codex/AGENTS.md` como link simbólico [D 36; T 42]; import com `@` não funciona [T 42]; teto de
  32 KiB somado [P 13]. Subpasta: marcador na raiz + `project_root_markers` pelo kit [D 36 R23; T 38]; o `.git` real
  pode dispensar o marcador, não testado com o hub [comentário no 14]. Cliente: R33; `instructions` vai como descrição
  do grupo de ferramentas, sem efeito confirmado [T 38; P 41].
- **Copilot CLI.** Par: `~/.copilot/copilot-instructions.md` como link simbólico [D 36; T 42]; hoje esse arquivo tem
  as instruções do GSD e "o kit junta os dois" (como: [—]); `COPILOT_CUSTOM_INSTRUCTIONS_DIRS` não carrega [T 42].
  Abre na pasta da iniciativa [D 36 R57; D 40]. Sem `.git` não lê a raiz; com `.git` lê [T 38]. Cliente: R33 +
  `--allow-all-mcp-server-instructions` pelo kit de cliente [D 36]; efeito precisa de teste [41].
- **Copilot no VS Code.** Par: o mesmo `~/.copilot/copilot-instructions.md` (o Agent Host lê `~/.copilot`) [P 18];
  chegou, mas uma regra trivial não foi seguida pelo Haiku 5.5 nem pelo Grok 4.7 [T 42]. `AGENTS.md` aninhado é
  experimental e desligado; o da raiz exige `.git` [P 37]. Issue #5022: instruções em dobro pela letra do drive
  [NV 18]. Cliente: o `instructions` entra inteiro no modo agente [P 41], sem teste.
- **Claude Desktop.** Sem contrato por arquivo [D 36 R26]; `instructions` do MCP não chega [T 38]. Se lê "Folder
  instructions" da pasta conectada [NV 11]; fica no 11.
- **Recruta em papel do Maestri.** A pasta do papel recebe `AGENTS.md` e `CLAUDE.md` idênticos e o `role.json`;
  reiniciar não regrava, `role edit` regrava e reinicia [T 45]. Claude Code: opção `claude-md-and-agents-md` ligada em
  cada par pelo kit [D 40 R51; T 38]. Codex: raiz e iniciativa só com o marcador [T 45; D 40]. Copilot CLI: lê papel e
  iniciativa, não a raiz (motivo não explicado) [T 45]; a raiz chega pelo arquivo global [D 40]. O contrato manda o
  maestro começar pela skill `maestro-acervo` [D 40 R52].

## 2. Skills
- Fonte em `agents/skills/<skill>/`; acervo `maestro-*` [D 36, 40]. Claude Code: junction em `~/.claude/skills`
  [D 36; T 38]. Codex, Copilot CLI e VS Code: junction em `~/.agents/skills` [D 36; T 42].
- Riscos: `COPILOT_HOME` desliga `~/.agents/skills` e o Agent Host define essa variável [P 18] (no teste 42 funcionou);
  `copilot skill add` não testado; `ChatStrictPluginOnlyCustomization` bloquearia skills [P 46].
- Cliente: sem cópia, sem junction; nada decidido [—]. Ticket 15 (Roteamento de skills) espera o 14.

## 3. MCP do banco (fork do es617)
- TypeScript, Node ≥ 22 [P 09]; HTTP `/mcp`, porta 8787, endereço padrão 0.0.0.0 [P 37]; um `MCP_AUTH_TOKEN`; sem
  token, só Host local [P 37]. `READ_ONLY` por instância funciona; duas instâncias no mesmo CouchDB convivem [T 38].
  Gravação com `base_rev`, conflito se a base mudou [D 25, 33]. O fork manter as variáveis do upstream [NV 37].
- Par: MCP local em `localhost`, com escrita [D 34]. Cliente: segunda instância `READ_ONLY=true` com token na tailnet,
  grant por tag e porta; o cliente nunca recebe a credencial do CouchDB [D 34; T 38].
- Config por harness [P 13, 18, 37]: Claude Code `claude mcp add --scope user` grava em `~/.claude.json` (estado da
  máquina, não serve para copiar; alternativas `--mcp-config` ou plugin via `CLAUDE_CODE_PLUGIN_DIRS`); Codex
  `~/.codex/config.toml` `[mcp_servers.<id>]` com `url` e `bearer_token_env_var`; Copilot CLI
  `~/.copilot/mcp-config.json` (`headers`, `$VAR`; também plugin, aceita `.claude-plugin`); VS Code: Agent Host lê
  `~/.copilot/mcp-config.json` e `.mcp.json`, e a doc diz "Copilot sessions can currently access only local MCP servers
  that don't require authentication" [P 18]; cabeçalho de token no VS Code [NV 37]. Claude Desktop: `"type": "http"` é
  ignorado; a ponte `npx mcp-remote <url> --allow-http --header …` funciona pela tailnet [T 38]; ler decidido [D 36],
  gravar aberto no 11.

## 4. MCP de busca e proxy
- 09 em aberto (R7 = C; R9 = ajuste da Robusta antes da fase 2): A = obsidian-hybrid-search no disco de cada par e
  proxy de MCP na tailnet para clientes; B = índice dentro do fork do es617.
- Proxy (TBXark/mcp-proxy ou 1MCP) junta MCP do banco (só leitura) e de busca num endpoint HTTP com token [P EPP];
  aceito como "Agora" do 14 (R89). [NV]: repasse de stdio no Windows, latência, repasse do `instructions`.
- Com busca de ferramentas ligada, as definições podem ser adiadas, o que enfraquece o canal da descrição [P 41].

## 5. Checagem de início de sessão
- Decidido: toda sessão lê o estado curto da vigia e avisa divergência [D 08, 33]; abre a nota de retomada do
  trabalho que a pasta identifica (`retomada.md`) [D 10, 12]; mod do Claude Code mostra o estado da vigia o tempo todo
  [D 33 R64]; hook de lembrete do maestro só com `MAESTRI_TERMINAL_ID` [D 40 R52].
- Mecanismos, todos sem teste: Claude Code `SessionStart` com `additionalContext` [P 39, 43]; mod exige 2.1.287+ e é
  "early access" [P 44]. Codex `SessionStart` em `~/.codex/hooks.json` ou `config.toml`, com `commandWindows`; cada hook
  aceito em `/hooks`, confiança presa ao hash [P 43, 44]. Copilot CLI `sessionStart` em `%USERPROFILE%\.copilot\hooks\`
  [P 43, 44]. VS Code: hooks em Preview; o Agent Host usa a implementação do Copilot SDK; `ChatHooks` não vale nele
  [P 44, 46]; se roda hooks de usuário [NV]. Recruta: hook no escopo do usuário [P 44].
- Cliente: sem vigia; origem do estado não decidida [—].

## 6. Hook ao fim da resposta
- Decidido: regra no contrato global + hook ao fim da resposta que obriga [D 10]; furos aceitos (meio de resposta
  longa, interrupção) [D 10]; registro de uso de peças por hook [D 40 R49]; verificador de órfãos no mesmo hook em
  revisão [12].
- Mecanismos, sem teste [P 39, 44]: Claude Code `Stop` (block/saída 2, `stop_hook_active`, `last_assistant_message`;
  hooks `prompt` e `agent` com modelo); Codex `Stop` com `decision: "block"`, só handlers `command` e `mcp_tool`;
  Copilot CLI `agentStop` com `block`, até 8 vezes, sem hook de modelo; VS Code `Stop` no Local e SDK no Agent Host,
  Preview.
- Cliente: a nota exige gravar, mas o cliente é só leitura [D 34]; não tratado [—].

## 7. Guarda do acervo
- Decidido [D 40 R46]: guarda forte só no Claude Code (mod ou hook de usuário, verificador em outro modelo); Codex e
  Copilot têm a gravação no acervo recusada e deixam propostas em `agents/maestro/propostas/`. Mecanismos [P 44]:
  Codex `PreToolUse` em `apply_patch` com `deny` ("guardrail"); Copilot CLI `preToolUse` deny/ask e `--deny-tool`;
  VS Code Preview. Usa o mesmo canal (hooks e plugin de usuário) da checagem e do `Stop`.

## 8. Copilot Enterprise (tudo [P 46])
- Allowlist de MCP por `serverName`, `serverUrl` ou `serverCommand`; variável não resolvida bloqueia; no CLI a
  checagem fecha na falha. VS Code: `ChatMCP`, `ChatAllowedMcpServers`, `ChatAllowManagedMcpServersOnly`;
  `ChatStrictPluginOnlyCustomization` bloqueia instruções, skills, hooks e MCP avulsos (saída: hub como plugin).
  Hooks da empresa somam; `allowManagedHooksOnly`. Nesta máquina não há política local. O teste 42 com a conta da
  empresa viu contrato e skill chegando; o MCP do hub não entrou.
- Teste pendente: CLI `/env`, `/instructions`, `/mcp`; VS Code "Developer: Policy Diagnostics"; com o MCP do hub
  configurado, ver se aparece "blocked by your enterprise".

## (a) Decisões abertas para o 14
1. Forma do adaptador: config nativa por harness ou plugin do hub.
2. MCP local do par: token e prender a 127.0.0.1.
3. Par e busca: MCPs separados ou pelo proxy local (depende do 09).
4. Endpoint do cliente: proxy ou es617 só leitura direto (depende do 09).
5. Cliente e nota de retomada com MCP só leitura (liga ao 11).
6. Cliente e skills.
7. Origem do estado na checagem: hook, MCP ou os dois; no cliente.
8. Fim da resposta no Codex e no Copilot: script, ou só a regra; no Claude Code `prompt` ou `command`.
9. Estado da vigia fora do Claude Code só na checagem de início.
10. Marcador de raiz com o `.git` real.
11. GSD no arquivo global do Copilot.
12. Contrato carregado em dobro na raiz.
13. Claude Desktop (depende do 11).
14. Plugin para o VS Code agora ou só se o teste Enterprise mostrar a política.

## (b) Fatos que faltam
1. Teste Enterprise com o MCP do hub configurado. 2. VS Code: "só MCP local sem autenticação" ainda vale; localhost
HTTP conta como local; cabeçalho de token. 3. Proxy: stdio no Windows, latência, repasse do `instructions`.
4. Transporte do MCP do obsidian-hybrid-search. 5. Hooks de início e fim no Codex, Copilot CLI e Agent Host (Codex:
pré-aprovar pelo kit ou aceitar à mão a cada hash; VS Code: roda hooks de usuário?). 6. `MAESTRI_TERMINAL_ID` no
hook. 7. `.git` real em subpasta e papel para Codex e Copilot. 8. `--allow-all-mcp-server-instructions`; requisição
do Codex. 9. Duas instâncias do fork; `READ_ONLY` e `MCP_INSTRUCTIONS_FILE` no fork. 10. Claude Desktop: "Folder
instructions", hooks. 11. Mod por junction ou plugin. 12. Instruções em dobro no Agent Host. 13. Content exclusion
por link simbólico. 14. `copilot skill add`.
