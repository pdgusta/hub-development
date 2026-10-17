# Relatório do ticket 23 (Cinzel): kit de par, a forma

Ramo `ticket-23` (hub), worktree `C:/context-hub-wt/ticket-23`, ponta e9dcef7 (com `integracao` e98a891 juntada).
Costuras e respostas do maestro: `costuras-23-Cinzel.md`. Mandato do maestro (07:53): o esqueleto agora; os hooks de
11, 17 e 18 entram por junção quando forem juntados; a junção em `integracao` só com todos os bloqueios resolvidos
(11, 15, 17, 18, 20, 27).

## O que foi feito

- **Entrada:** `agents/code/kit/par/instalar.ps1`, com `-Casa`, `-Hub`, `-EnvFile`, `-Passos`, `-WhatIf` e
  `-Desfazer`. Sem `-Casa` nem `HUB_HOME_ENSAIO`, recusa: o HOME real é o ticket 26.
- **Ordem dos passos:**
  - 00: conferir;
  - 03 a 05: os instaladores das faixas, enfileirados, cada um com `-WhatIf`;
  - 08: os harnesses (`08-harnesses.mjs`);
  - 10: a manutenção (`10-manutencao.ps1`).
- **A casa** (`kit/casa.mjs`):
  - antes de mudar um caminho, move o que estava para `<casa>/.hub-kit/copias/<carimbo>/`. Mover, e não copiar, faz
    arquivo, pasta, link e junction voltarem como eram;
  - o `registro.json` guarda o antes e o depois de cada caminho;
  - compara o desejado com o atual e só toca quando difere;
  - o desfazer confere se cada caminho está como o kit deixou (senão, para e diz qual), volta tudo em ordem inversa
    e apaga o `.hub-kit`.
- **Passo 08**, nesta ordem:
  1. **Conferência dos contratos globais.** Se `copilot-instructions.md` ou `~/.codex/AGENTS.md` tem texto além do
     bloco do GSD, o kit para e mostra o texto (resposta 2).
  2. **GSD fora do escopo global**, com cópia:
     - pelo manifesto de cada harness (`gsd-file-manifest.json`): a pasta da skill, o `gsd-core` e cada arquivo;
     - o manifesto, o `gsd-install-state.json` e o `gsd-migration-journal`;
     - `hooks/gsd-*` e `skills/gsd-*` (o script de hook do Codex não está no manifesto);
     - os hooks que chamam um script `gsd-*`;
     - o bloco marcado do `copilot-instructions.md`;
     - os comentários `# GSD` do `config.toml`;
     - `~/.agents/skills/gsd-*`.
  3. **Contrato:**
     - Codex: link simbólico `~/.codex/AGENTS.md`;
     - Copilot: link simbólico `~/.copilot/copilot-instructions.md`;
     - Claude Code: a linha `@<hub>/AGENTS.md` no `~/.claude/CLAUDE.md`, que mantém o resto do texto.
  4. **Skills:** uma junction por skill com `metadata.camada: geral` no `SKILL.md` (resposta 1), em `~/.claude/skills`
     e `~/.agents/skills`.
     - Marcadas agora: `busca`, as cinco `maestro-*`, `nova-iniciativa` e `nova-pasta-local`.
     - Uma pasta de mesmo nome vai para a cópia. O resto das pastas globais fica.
  5. **MCP**, com a URL do `.env` do par (registros em `busca/registro/` e no novo `mcp-banco/registro/`):
     - `hub-busca` e `hub-banco` nos três;
     - o `permissions.deny` da busca juntado no `settings.json`;
     - o token do banco só por variável (`${HUB_MCP_BANCO_TOKEN}` no Claude e no Copilot; `bearer_token_env_var` no
       Codex);
     - no Codex, `default_tools_approval_mode = "approve"`.
  6. **Hooks:** todo `agents/code/hooks/<peça>/fragmentos/<harness>.json`, com `{{DIR}}` e `{{HUB}}`, juntado por
     evento.
     - Claude: no `settings.json`. Codex: no `hooks.json`. Copilot: em `~/.copilot/hooks/hub-<peça>.json`.
     - O grupo que já está igual não se repete, e os hooks alheios ficam.
     - No Codex, cada hook do hub é aprovado em `[hooks.state.'<hooks.json>:<evento>:<grupo>:<hook>']` com o hash
       que o app-server calcula numa cópia (ver as sondas).
  7. **Codex:** `sandbox_mode = "danger-full-access"`, por chave.
- **Passo 10:** grava dois XML em `<casa>/.hub-kit/tarefas/`:
  - `hub-manutencao-diaria.xml`: todo dia, `copia-diaria.mjs --env` e `conferir-cabeca.mjs <hub>`, do 21;
  - `hub-vigia.xml`: a cada 5 min, `vigia.mjs passada --env`, do 16.
  Os dois rodam o `node` por `conhost.exe --headless`. Registrar pede `-Registrar`: os testes nunca o passam, e o
  `instalar.ps1` também não.
- **Conferência 00:**
  - nenhum `CLAUDE.md` no hub nem acima dele: senão, para e diz o caminho;
  - modo de desenvolvedor, lido no registro: se estiver desligado, para e explica, sem ligar;
  - Node ≥ 22 e Python.

## Testes

`agents/code/test/23-kit.test.mjs`, sem harness, com hub e casa de ensaio (`pastaDeEnsaio` e `hubDeEnsaio`). O
app-server do Codex sobe por segundos, sem modelo e sem login, sem a trava (resposta 3).

Resultado: 13/13. Com 20, 19 e 04, que leem os `SKILL.md` marcados, são 67/67 depois da junção de `integracao`
e98a891 (log em `logs/23-testes-1.log`). Nenhuma pasta `hub-ensaio-23-*` nem `hub-kit-codex-*` sobrou.

| Critério do ticket e do spec | Teste |
| --- | --- |
| roda duas vezes e a segunda não muda nada | "a segunda passada não muda nada" (ações vazias e retrato da casa igual); o passo 10 também |
| desfaz sem sobra | "o desfazer volta a casa ao que era"; o do GSD volta tudo, com hooks, MCP e skills |
| a simulação não muda nada e lista o que faria | "com -WhatIf, a casa não muda"; o do passo 10 |
| cada link aponta para o `AGENTS.md` do hub de ensaio | "o contrato chega aos três" |
| a junction expõe só as skills de uso geral | "as skills de uso geral chegam por junction": lista literal; a de papel e a sem camada ficam fora |
| cada configuração tem as linhas de MCP | "as linhas de MCP de busca e de banco chegam aos três": o token não aparece em arquivo nenhum |
| os hooks juntados mantêm os que estavam; os hashes do `hooks.state` batem | "os hooks de todas as peças": o alheio fica em primeiro; cada hook do hub aparece uma vez; os hashes conferem com uma lista independente do app-server |
| `CLAUDE.md` acima do hub: para e diz onde | "com um CLAUDE.md acima do hub" |
| GSD de mentira sai, com cópia, e o contrato entra | "o GSD sai do escopo global" e "copilot-instructions.md com texto além do GSD" |

## Fatos de fonte (lidos por curl em 2026-10-17)

- Claude Code, <https://code.claude.com/docs/en/mcp.md>, "Environment variable expansion in `.mcp.json`":
  - `${VAR}` e `${VAR:-default}` valem em `command`, `args`, `env`, `url` e `headers`; exemplo `"Authorization":
    "Bearer ${API_KEY}"`;
  - a seção vale também no escopo do usuário (`~/.claude.json`): "For a server in the local, project, or user scope
    ... show a `${VAR}` reference by name";
  - as variáveis de credencial do próprio Claude (`ANTHROPIC_*`, `NPM_TOKEN`, `HTTPS_PROXY`...) chegam vazias;
    `HUB_MCP_BANCO_TOKEN` não é uma delas.
- Claude Code, <https://code.claude.com/docs/en/skills.md>: "`metadata` | No | Free-form YAML map for your own
  key-value data ... read by your own tooling from `SKILL.md`. Claude Code doesn't act on its contents". O padrão das
  skills (<https://agentskills.io/specification.md>): "`metadata` | No | Arbitrary key-value mapping".
- Copilot CLI, referência de comandos
  (`docs.github.com/api/article/body?pathname=/en/copilot/reference/copilot-cli-reference/cli-command-reference`):
  - no `mcp-config.json`, `headers` "Supports variable expansion";
  - `env` "Supports `$VAR`, `${VAR}`, and `${VAR:-default}` expansion";
  - `--allow-all-mcp-server-instructions`: "By default, only allowlisted server instructions are included up front;
    other servers' instructions are retrieved on demand."
- Copilot CLI, referência da pasta de configuração (`.../cli-config-dir-reference`): nenhuma chave de configuração nem
  variável de ambiente liga as instruções de todos os servidores, e a lista permitida não é do usuário. **Logo, o kit
  não tem como ligar a opção por arquivo.** Quem abre o Copilot passa `--allow-all-mcp-server-instructions` (o preset
  `custom` do Maestri, user story 40 da faixa 8; tickets 24 e 26).

## Sondas

- 2026-10-17 ~08h20, app-server do Codex (`hooks/list`, sem modelo e sem login), o mesmo `hooks.json` em duas
  pastas:
  - o `currentHash` saiu igual nas duas (`sha256:08eb88...`);
  - a chave é `<caminho do hooks.json>:<evento>:<grupo>:<hook>`;
  - o app-server grava no `CODEX_HOME` (`*.sqlite`, `installation_id`, `skills/`, `tmp/`, `.tmp/`).
  **Por isso o kit lista os hooks numa cópia temporária** do `hooks.json` e do `config.toml` e troca o caminho da
  chave pelo real. A casa não ganha arquivo do app-server, e a segunda passada e o desfazer ficam limpos.
- A forma do GSD foi lida no HOME real, só para leitura:
  - um manifesto por harness em `.claude`, `.codex` e `.copilot`;
  - um bloco marcado no `copilot-instructions.md`;
  - os comentários `# GSD ... managed by gsd-core installer` no `config.toml`;
  - `hooks/gsd-check-update.cmd` no Codex, fora do manifesto;
  - `gsd-*` em `~/.agents/skills`.
  Nada foi gravado.

## Ressalvas e o que fica para depois

1. **Hooks de 11, 17 e 18; mod; extensão; `statusLine`; `notify`.** Os fragmentos novos entram sozinhos na passada
   seguinte. O resto pede código no kit depois do 17 e do 18:
   - o mod do Claude Code;
   - a extensão `onAgentStop` e a `statusLine` do Copilot;
   - o `notify` composto no Codex: o kit deixa o `notify` como está até o consumidor do hub chegar.
   O 11 não tem hook.
2. **Chaves de `hooks.state` de hooks alheios.** O kit tira os grupos do GSD do `hooks.json` do Codex. Quando um
   grupo alheio vem depois de um grupo removido, o índice dele muda. A aprovação que ele tinha no `hooks.state` deixa
   de casar, e o Codex o pede de novo na tela `/hooks`. O kit aprova só os do hub. Ressalva para o 26: conferir no
   HOME real.
3. **A seção do GSD no `config.toml`.** O kit tira só os comentários `# GSD`. Não sei, pela fonte, quais tabelas o
   instalador do GSD grava no Codex (`[agents] max_depth = 1` vem logo depois dos comentários no HOME real). Ficam
   como estão; conferir no 26.
4. **O XML das tarefas não foi registrado nem validado pelo Agendador.** Registrar seria global. O teste lê o XML
   (gatilho, ações, pasta de trabalho). Também não verifiquei se o `conhost.exe --headless` some com a janela no
   gatilho de 5 min (registro no 26).
5. **Precisam do ensaio com harness (24):** como os harnesses enxergam a casa (`CLAUDE_CONFIG_DIR` e companhia, ou o
   HOME de ensaio), o contrato uma vez só e o `COPILOT_SKILLS_DIRS`.
6. **Fora desta forma (pontos abertos do spec):** o `claude-md-and-agents-md` do Maestri, o MCP do Copilot do VS
   Code e o `trust_level` do Codex.

## Rodada 2 (consertos da rodada 1 do Fiel, `parecer-23-Cinzel.md`)

1. **Grupo do hub que saiu dos fragmentos.** Antes de juntar, o kit tira do `settings.json` e do `hooks.json` o grupo
   cujo comando está dentro de `<hub>/agents/code/hooks/` e que não está em nenhum fragmento atual (fragmento mudado
   ou peça tirada). No Copilot, tira `~/.copilot/hooks/hub-<peça>.json` de peça que saiu. No `hooks.state`, das
   aprovações do `hooks.json` da casa fica só a que ainda vale (o hook existe e o hash bate); as do hub são regravadas.
   Os alheios ficam. Teste novo: "fragmento mudado e peça tirada do hub" (timeout trocado nos três fragmentos da
   leitura e a peça do acervo apagada do hub; a segunda passada deixa cada grupo uma vez, nenhum grupo do hub a mais,
   nenhum arquivo `hub-acervo.json` e as aprovações iguais à lista do app-server).
2. **As peças do teste saem do repositório**, não de uma lista literal: o `fragmentos/claude.json` do fim da resposta
   (ramo `ticket-18` e1c5eac, recado da Vela) entra na junção do 18 sem mudar o teste. Conferido que ele tem a mesma
   forma (`hooks.PostToolUse`, `{{DIR}}`, `{{HUB}}`).

Testes: `23-kit.test.mjs` 14/14, ramo `ticket-23` f304e6c. Ressalva nova do Fiel para o 26: o desfazer
para em `~/.claude.json` e `config.toml`, que o harness regrava; lá, desfazer por chave.

## Rodada 3 (reaberto pelo Fiel: o detector do 29)

O `harness-real.test.mjs` (ticket 29) acha pelo texto todo teste que chega a um harness (`app-server` é uma das marcas)
e exige `comHarness`. O 23 sobe o app-server do Codex em toda passada do passo 08 (o hash dos hooks), então pôr só o
`hooks.state` atrás do `comHarness` não basta: o teste inteiro iria para trás da variável e sairia da suíte comum.
Conserto: uma exceção estreita no detector, `SO_APP_SERVER`, com o motivo (só `hooks/list`, sem modelo, sem login,
sem cota; resposta 3 das costuras). A exceção cai se o próprio arquivo citar login ou harness que chama modelo
(`CODEX_JS`, `COPILOT_JS`, `claude.exe`, `npm-loader`, `.credentials.json`, `auth.json`, `'exec'`). Teste novo no
detector: a exceção aponta arquivo que existe, tem motivo, sobe mesmo o app-server e não cita login. Ramo `ticket-23`
a419182: `harness-real.test.mjs` 7/7; `23-kit.test.mjs` sem mudança (14/14 na f304e6c). O `ticket-24` juntou
(e7d38ae): detector 7/7.

## Lição do 21: caminho longo (2026-10-17 ~11h10, e6e5faa)

O `Resolve-Path` guarda o nome curto do Windows (`GUSTAV~1.DEL`), e com ele no `HUB_ROOT` o `fs.watch` do node pode
abortar (Trilho, libuv fs-event.c:72). O `instalar.ps1` agora passa hub, casa e `.env` pelo `realpathSync.native` do
node (função `Longo`): junctions das skills, `{{HUB}}` dos hooks, contrato e XML do passo 10 saem no caminho longo. O
hub real (`C:\context-hub`) não é junction, então o realpath só expande o nome curto. Teste novo: hub, casa e `.env`
dados com o nome curto, e nada na casa com `~1`. O `ensaio()` do teste passou a usar o caminho longo (o `%TEMP%` do
node vem curto). 23-kit + harness-real 22/22. Ressalva: o `03-busca.ps1` chamado sozinho ainda usa o `Resolve-Path`
(pelo `instalar.ps1`, já recebe o caminho longo).
