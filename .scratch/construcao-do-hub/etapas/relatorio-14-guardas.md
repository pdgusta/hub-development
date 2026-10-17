# Relatório do ticket 14: guardas de regravação e ficha (Trilho)

## Estado
- 2026-10-17: ticket pego (worktree `C:\context-hub-wt\ticket-14`, ramo `ticket-14`, de `integracao` 0d04985).
- Primeiro commit do ramo (3055de9), separado: **sai o `README.md` da raiz**. Decisão do ticket 12: a raiz tem só o
  `AGENTS.md` e as seis raízes; o README era o marcador do "Início do hub". O `verificar-hub` passa sem ele (só o aviso
  de `agents/blocks.md`, caminho sem tipo).
- `integracao` juntada no ramo duas vezes: 45ec3b0 (ticket 01) e 8b9beef (ticket 06), HEAD ea4d299. 69 testes verdes
  (`node --test "agents/code/test/*.test.mjs"`); ponta a ponta verde nos três harnesses. Pedida a revisão ao Fiel.
- Revisão 1 (Fiel e Fielzinho): volta, dois consertos. (1) O `lerPatch` não fechava a parte no `*** End Patch`: um
  LF, CRLF ou dois LF depois do fim viravam linha do último bloco, a troca não casava e a ficha passava sem conferência.
  Consertado (a parte fecha no fim), com teste nos quatro finais (nenhum, `\n`, `\r\n`, `\n\n`) no Codex e no
  `apply_patch` do Copilot; ponta a ponta do Codex repetida, verde. (2) Este relatório dizia que caminho com ponto
  passa; o certo está abaixo, e um teste fixa a recusa. Commit 73a1917 e seguintes; 71 testes verdes. Pedida a revisão 2.

## O que foi entregue
Tudo em `agents/code/hooks/guardas/` (o que só o harness roda; opção C):
- `antes-da-ferramenta.mjs <claude|codex|copilot> [--hub <raiz>]`: o hook antes da ferramenta, com o evento do harness
  na entrada padrão. Raiz do hub: `--hub`, senão `HUB_ROOT`, senão `C:\context-hub`. Recusa com a resposta do harness
  (`hookSpecificOutput.permissionDecision: "deny"` no Claude Code e no Codex; `permissionDecision: "deny"` no Copilot,
  formato da doc "GitHub Copilot hooks reference" e da bancada); passa sem resposta. Erro dentro da guarda: passa e
  avisa no stderr, sempre com saída 0 (no Copilot, saída ≠ 0 no `preToolUse` recusaria toda chamada).
- `guarda.mjs`: a decisão, a mesma nos três, e um adaptador por harness que traduz o evento em gravações:
  - Claude Code: `Write` (existente = regrava; senão novo), `Edit` e `MultiEdit` (troca de trecho, com o conteúdo final
    montado);
  - Codex: `apply_patch` em `tool_input.command`;
  - Copilot CLI: `create` (existente = regrava), `edit` (troca), e `apply_patch` no mesmo formato do Codex (para os
    modelos GPT; **não exercido**, nem na bancada nem aqui).
- `patch.mjs`: lê o `apply_patch` e aplica os blocos `@@` ao texto atual (igual exata, depois sem espaço no fim, depois
  sem espaço nas pontas, como o Codex 0.161.0 faz, segundo a bancada).
- **Recusa:** regravar inteiro arquivo que já existe no hub, com a mensagem "use a troca de trecho ou o write_note do
  MCP do banco com a versão que você leu"; no Codex, isso cobre `Add File` sobre existente, `Delete File` + `Add File`
  do mesmo caminho, `Update File` que remove tantas linhas quanto o arquivo tem (a heurística da bancada) e `Move to`
  sobre destino existente. **Recusa também** a nota `.md` que ficaria fora do esquema: monta o conteúdo final (arquivo
  novo, ou o atual com a troca) e chama o `analisar` do verificador do ticket 05 (escolha aceita 15). Só o que exige
  juízo recusa; o dedutível o verificador completa depois.
- **Passa:** troca de trecho, arquivo novo dentro do esquema, troca que não casa (a própria ferramenta falha), apagar
  arquivo (`Delete File` sozinho; ver "Fora"), qualquer coisa fora do hub.
- **Caminho com ponto dentro do hub** (`.local/`, `.secrets/`, `projeto/.venv/`): a regravação de existente é
  **recusada** como em qualquer lugar do hub (o spec não abre exceção; acordo de Fiel e Fielzinho); só a conferência da
  ficha fica de fora, porque ali não há nota do hub (o `analisar` ignora caminho com ponto). Arquivo novo passa sem
  frontmatter. Teste: "em caminho com ponto dentro do hub, regravar existente é recusado; nota nova sem frontmatter
  passa".
- **Caminho real:** junction e link simbólico resolvidos antes de comparar com o hub (teste com uma junction para o hub).
- **Registro:** cada chamada que toca o hub vira uma linha em `<hub>/.local/guardas/registro.jsonl` (hora, harness,
  decisão, caminho, motivo). `.local/` é por máquina: não replica nem vai ao git.
- `fragmentos/claude.json`, `codex.json`, `copilot.json`: o pedaço de configuração de cada harness, com `{{DIR}}` (a
  pasta do hook) e `{{HUB}}` (a raiz), para o kit (tickets 23 e 24) juntar. Claude: `PreToolUse` com matcher
  `Write|Edit|MultiEdit`; Codex: `PreToolUse` com matcher `apply_patch` (o kit aprova o hash em `hooks.state`, como na
  prova 03); Copilot: `preToolUse` com matcher `create|edit|apply_patch`, em `<COPILOT_HOME>/hooks/*.json`.

## Como provar
```
cd C:\context-hub-wt\ticket-14
node --test "agents/code/test/*.test.mjs"                                  # 71 verdes, sem harness nem login
node --test agents/code/test/ponta-a-ponta/14-guardas.test.mjs             # os três harnesses reais (login de ensaio)
HARNESSES=codex node --test agents/code/test/ponta-a-ponta/14-guardas.test.mjs   # um só
```
- `agents/code/test/14-guardas.test.mjs` (37 testes):
  - **os 24 casos gravados na bancada do ticket 11** (`14-guardas/casos-da-bancada.json`): os 10 eventos crus do Codex
    (`hooks.jsonl`), e os 7 do Claude e os 7 do Copilot remontados com os argumentos reais das ferramentas tirados das
    saídas da bancada (`saida/*.jsonl`), no envelope de cada harness (o stdin cru deles não ficou gravado). Esperado: o
    da tabela da bancada, com a política do hub (todo `Write`/`create` sobre existente recusa, não só o `caso4`).
    Rodam em `agents/code/` do hub de ensaio, que é do hub mas não leva frontmatter;
  - nos três: nota nova sem `status` recusada e com `status` passa; troca que tira o `status` recusada e a que não
    mexe passa; fora do hub, regravação passa sem resposta;
  - junction para o hub; o registro em `.local/guardas/`.
- `agents/code/test/ponta-a-ponta/14-guardas.test.mjs`: uma sessão por harness, num hub de ensaio com os hooks no
  escopo do usuário de um HOME de ensaio. O agente tenta, na ordem: regravar inteiro `context.md`, trocar uma linha
  dele, criar uma nota sem `status` e criar a mesma nota com `status`. Confere o disco e o registro da guarda.
  **Verde nos três** (2026-10-16 23:37–23:38 UTC): Claude Code 2.1.302 com haiku; Codex 0.162.1 com `gpt-6-luna` e
  esforço baixo, em `danger-full-access`; Copilot CLI 1.0.98 com `claude-haiku-5.5`. Evidência em
  `agents/code/test/ponta-a-ponta/evidencia-14/` (registro da guarda, saída e erros de cada harness, hashes),
  com a pasta do usuário trocada por `%USERPROFILE%`/`USUARIO` e sem credencial (busca por
  `access_token|refresh_token|id_token|api_key|bearer|sk-ant|gho_|ghu_` = 0).

## Uso do login no ensaio (aval do Gustavo, rodada 2026-10-16-login-dos-harnesses-no-ensaio)
- 2026-10-16 23:28 (UTC): **rodada sem querer do Claude.** Para conferir a sintaxe do teste de ponta a ponta usei um
  `import()` do arquivo, e ele executou os testes. A rodada do Claude foi inteira, já com o aval: copiou
  `%USERPROFILE%\.claude\.credentials.json` para o `CLAUDE_CONFIG_DIR` de ensaio em `%TEMP%\hub-ensaio-14-*`, rodou
  uma sessão `claude -p` com haiku e apagou a pasta no `finally`. O processo acabou durante a preparação do Codex (antes
  de copiar o `auth.json`) e antes do `after`, e por isso os hashes não foram gravados. Conferido depois: nenhuma cópia
  de login sobrou em `%TEMP%\hub-ensaio-14-*`; a pasta do Codex que ficou (`hub-ensaio-14-JD4QnQ`, só `config.toml` e
  `hooks.json`) foi apagada. Resultado no registro da guarda: as quatro decisões certas.
- Rodadas pelo teste (cada uma copia o login ao preparar e apaga a pasta inteira no `finally`):
  1. ~23:31, os três: Claude e Copilot com as decisões certas da guarda, mas o teste falhou por três causas fora dela
     (abaixo); Codex parou antes de rodar (filtro do hook);
  2. ~23:34 e ~23:35, só o Codex: falhou porque o modelo pôs no patch só um pedaço da linha (`apply_patch
     verification failed`), com a guarda deixando passar, certo;
  3. ~23:36, só o Codex: verde;
  4. **23:37:05–23:38:17, os três: verde.** Copiado e apagado: Claude `.credentials.json` (copiado 23:37:05, pasta
     apagada 23:37:28); Codex `auth.json` (23:37:32 → 23:37:49); Copilot só `lastLoggedInUser` e `loggedInUsers` no
     `config.json` (23:37:53 → 23:38:17; o token fica no cofre do Windows e não foi copiado).
- **Hashes (SHA-256, início) das pastas reais, iguais antes e depois da rodada 4:** `.claude/.credentials.json`
  13644f92d00a3ae9; `.claude/settings.json` 411d8d3b13290a5c; `.codex/auth.json` 9e42496b5bd73e15;
  `.codex/config.toml` a6cae9fa9397b2b3; `.codex/hooks.json` d822fa388c1d2f07; `.copilot/config.json`
  283253d40ec4a047; `.copilot/hooks/gsd-session.json` 3382597f61e3a559; `.copilot/hooks/tokenjuice-cli.json`
  c9d58a20aed33c56. Completos em `evidencia-14/hashes-claude-codex-copilot.json`. O teste exige os de configuração
  iguais; os de login ele só registra, porque as sessões de verdade (esta e as dos colegas) renovam o token sozinhas.
- **Rodada 5, só o Codex, depois do conserto 1 da revisão** (2026-10-16 23:55:01–23:55:22 UTC): verde. Copiado
  `%USERPROFILE%\.codex\auth.json` para o `CODEX_HOME` de ensaio às 23:55:01; pasta inteira apagada às 23:55:22.
  Os oito hashes reais iguais antes e depois (`evidencia-14/hashes-codex.json`), os mesmos da rodada 4. Evidência do
  Codex trocada pela desta rodada; sem credencial nem nome do usuário.
- O aviso do maestro (a sessão de ensaio renovar a chave do Claude e o login real pedir `/login`): **não aconteceu**; o
  `.credentials.json` real ficou com o mesmo hash, e esta sessão seguiu sem pedir login.

## O que a ponta a ponta ensinou (para o kit e as próximas etapas)
- **Claude Code barra gravação em caminho curto do Windows** (`GUSTAV~1.DEL`): "suspicious Windows path pattern",
  antes de qualquer hook. O `%TEMP%` desta máquina vem curto; o teste usa o caminho longo
  (`realpathSync.native`). O hub de verdade, `C:\context-hub`, não tem o problema.
- **O `create` do Copilot não cria pasta que falta** ("Parent directory does not exist"). A nota num bloco novo pede a
  pasta antes (a "nova iniciativa" cria as pastas dos blocos).
- **O Codex quer a linha inteira no `apply_patch`**: com só um pedaço, falha "Failed to find expected lines". O pedido
  da prova passou a dar a linha inteira.
- **O Codex devolve o caminho longo** do `hooks.json` no `hooks/list`; comparar caminhos pelo real.
- Nos três, o motivo da recusa chega ao agente: Claude ("PreToolUse:Write hook error: ..."), Codex ("Command blocked by
  PreToolUse hook: ..."), Copilot ("Denied by preToolUse hook: ..."). Os três respeitaram a recusa e seguiram.

## Fora (com o porquê)
- **Apagar arquivo** (`Delete File` sozinho no Codex) passa: o spec deixa "decidir se apagar entra na guarda" aberto, e
  recusar apagaria também os apagamentos legítimos. Não testados (como na bancada): vários caminhos num patch além de
  apagar e criar, links dentro do patch, arquivo vazio, apagar e criar em chamadas separadas.
- **Shell** (redirecionamento, script): fora do hook, coberto só pelo contrato (ticket 11). No Codex com acesso total,
  o shell grava onde quer (prova 03).
- **`apply_patch` do Copilot** (modelos GPT): o adaptador lê, mas não foi exercido.
- **Aviso de leitura** (busque antes / leia o trecho): ticket 15.
- **Verificador no fim da resposta** (Claude pelo mod, Copilot pelo `agentStop`, Codex pelo `Stop`): ticket 27.
- **Instalar de verdade e juntar os fragmentos** com os das outras faixas: kit de par (tickets 23 e 24).
- **Banco fora do ar**: a guarda não depende do banco; regravar continua recusado e a troca passa (é o comportamento de
  sempre).
- O teste de ponta a ponta importa `listarHooks` e `apagarEnsaio` de `provas/03-codex-hooks/instalar.mjs`; quando o kit
  tiver a versão dele, trocar.
- As pastas `%TEMP%\hub-ensaio-14-*` dos testes sem harness (sem login) ficam; cada `node --test` cria algumas.

## Fechamento
- 2026-10-17 ~1h15: revisão 2 (Fiel e Fielzinho): passa, HEAD 124a643. Ressalva do Fiel: as pastas
  `%TEMP%\hub-ensaio-14-*` dos testes sem harness se acumulam (não têm login; cada `node --test` cria algumas). Rebite
  avisado.
- 2026-10-17: ticket 14 juntado em `integracao` (8d1d785) e resolvido pelo Rebite, 81 testes verdes na junção.
