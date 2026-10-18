# Retomada do Cinzel (construtor, Claude)

Leia antes: `etapas/regras-da-construcao.md` (inteiras, com os "Achados comuns"), os tickets 11, 23, 24 e 37 (em
`issues/`, com os comentários) e esta retomada. Gravada em 2026-10-17 13:20, na janela quieta do 25 (só falta o Codex do 11 e do 24, depois das 17h15).

## Agora: nada rodando, nada esperando a trava

- 14:13 (religado depois do /clear): integracao segue c42ffa0, já contida em 11, 23, 24 e 37. Espero 17h15 e a fila (item 4).
- 14:25 (maestro): cota do Codex redefinida pelo Gustavo. Fila: depois da suíte do 42 (Rebite), Codex do 11 (corredor), depois Vela e Brasa; o 24 só depois do 23 juntado. Windows reinicia às 21h: retomada gravada até 20h30.
- 14:58: Codex do 11 PASSA (log 11-harness-3.log, evidência e96cd70; relatório com a rodada 2). Ramo ticket-11 e63d951 (com integracao d298826), 4/4. Rodada 2 pedida ao Fiel. Depois do passa: Rebite. Próximo: Codex do 24 quando o 23 juntar (fila, item 5).
- 15:10: r2 do Fiel VOLTOU (modelo à mão; detector do 43). Conserto 28782df no 11 (MODELO_CODEX; 12 passam + 1 pulado, com integracao 98a7ced) e 65cb752 no 24. Rodada curta pedida. No 24, antes do Codex: juntar a integracao (o harness-real do ramo ainda diz 6.1-sol).
- 15:25: 11 PASSA (Fiel, rodada curta); Rebite avisado (ramo ticket-11 28782df). 24: integracao 98a7ced juntada (769f36f; conflito no harness-real.test.mjs: ficam os dois testes, o do 23 e os do 43); harness-real 9/9, 23-kit 20/20, aceite pulado. Falta o Codex do 24 (fila, depois do 23 juntado) e a revisão.
- 15:45: 23: integracao 98a7ced juntada (2379d38, mesmo conflito do 24, resolvido igual); 29/29 juntos (2x; 1ª rodada teve 1 falha não registrada). Rodada curta pedida ao Fiel; depois, ponta ao Rebite. 24: ticket-23 2379d38 juntado (c544ef4, sem mudança de arquivo).
- 15:55: integracao 51fa382 (11 juntado) no 23 (9fcf4cf, harness-real 9/9) e no 24 (fdcd408, 9/9 + aceite pulado). Fiel avisado da ponta nova.
- 16:40: 37 com a ponta do 18 (4f0b09e) e a integracao a7d1517: 7c54148, 95/95. 16:50: 23 PASSA na junção (Fiel), mas o maestro mandou conserto curto: EPERM passageiro no rename do registro (casa.mjs). Feito em ceda444 (renomear com repetição ~2 s em EPERM/EACCES/EBUSY, nas 4 trocas; 5 testes novos). Rodando harness-real + 23-kit juntos 3x (logs 23-emuso-juntos-N.log); depois rodada curta do Fiel, Rebite junta; levar a ponta ao 24.
- 17:05: 23 juntos 34/34 três vezes; relatório e ticket feitos; rodada curta pedida ao Fiel (ceda444). 24 com o 23 novo: 438e60f. Depois do passa: Rebite junta o 23 (ponta ceda444, com integracao 51fa382 dentro). Codex do 24: janela quieta da noite (~17h30, depois do 22 da Brasa).
- 17:15: 23 PASSA (ceda444); ponta 6bd7fb0 com integracao a7d1517; Rebite avisado. 24 em 71ef8f1. Falta: Codex do 24 na janela da noite (antes, juntar a integracao se andou; MODELO_CODEX = luna), rodada 2 do Fiel, Rebite. 37: espera o 18 (ponta 7c54148).

- 23: conserto do Fielzinho em duas voltas (46897e0, 488b377: mudança e registro que falham devolvem o original); rodada curta PASSA (12:58). Ponta 2d93089 (com integracao c42ffa0), 27/27; Rebite avisado. 24: ponta 542a538 (com o 23 2d93089), 7/7; falta só o Codex.
- Codex SEM COTA até 17h15 (tentativa do 11 às 12:40, log 11-harness-2.log; evidência descartada). Trava solta. Depois das 17h15, pela fila: Codex do 11, depois do 24. integracao c42ffa0 juntada nos ramos às 13:14.
- 37: fechado (rodada curta PASSA em f8e12e3); Rebite tem a ponta. Junta depois do 18.
- Ao voltar: juntar a `integracao` nos ramos se ela andou (testes de cada um), depois o Codex pela fila.
- Codex de verdade: `gpt-6-luna` (regra nova do Gustavo, 14h30: Codex só testes, luna padrão; 6.1-sol só se difícil, dizendo por quê no relatório). Trocado no 11 (e7e1dd3) e no 24 (9936ea2); a constante MODELO_CODEX muda no 43 (Brasa).

## Ticket 37: o fim da resposta vê a gravação pelo shell (em curso)

- **Hub:** worktree `C:/context-hub-wt/ticket-37`, ramo `ticket-37` do `ticket-18` 31afe63; ponta 6b79169 (f8e12e3 + integracao c42ffa0; 14, 17, 18, 27, 37 e harness-real 133/133). Ticket
  `claimed`. Núcleo é da Vela (18/27): dúvida do núcleo, pergunte a ela.
- **Costuras aceitas** (`etapas/costuras-37-Cinzel.md`): Vela, 1/3/4 com ajustes (a)-(d); maestro, 5, 6 e (e).
  - (e) o `anota` ouve o shell (Claude `Bash|PowerShell`, Codex `Bash`, Copilot `bash|powershell`) e cria
    `.local/fim-da-resposta/<sessão>.shell`; o `marcar` o apaga. O fim só varre o `cwd` com esse arquivo.
  - Varredura (`foraDasFerramentas` no `nucleo.mjs`): `mtime >= marca`, fora do `.gravados` de qualquer sessão, pula
    ponto e `node_modules`, corta em 20.000 entradas; aviso mostra até 10 caminhos, "(e mais N)".
  - Nota ou passagem de fora (`ehNota`, agora exportado em `nota.mjs`) entra no `conferirRetomada` e no
    `gravarUltimoAgente` como mudada; o resto vira aviso em "Antes de terminar:" (lista `pedemAcao`), uma vez por turno.
  - Texto: "gravado fora das ferramentas (shell ou outro processo) nesta resposta: ...; a nota de retomada mudou?".
- **Feito:** 977ea86 e c16e53f. `agents/code/test/37-gravacao-pelo-shell.test.mjs` 11/11 (~2 min; ajudante novo
  `eventoDeShell` em `test/gravacao.mjs`). Matchers do shell nos três fragmentos do fim.
- **Fechado:** rodada curta PASSA em f8e12e3 (ressalva da r2 feita, 114/114); Rebite avisado do HEAD novo. Junta depois do 18.
- **Rodada 1 do Fiel VOLTOU** (nota de fora virava falta e ganhava last_agent); conserto 4b695d5 com a Vela (só cala a cobrança, com aviso); 113/113; rodada 2 pedida ~11h05.
- **Feito também (10:25):** 14+18+27+37 105/105; relatório; revisão pedida ao Fiel. Depois do passa: Rebite (junção depois do 18).
- **Falta, antigo (já feito):**
  1. Rodar, sem trava, `node --test agents/code/test/18-retomada.test.mjs agents/code/test/27-fim-da-resposta.test.mjs
     agents/code/test/14-*.test.mjs agents/code/test/37-gravacao-pelo-shell.test.mjs` (~5-8 min). Se algum teste
     confere os matchers dos fragmentos, ajustar.
  2. Conferir se o 23 (kit) lê os fragmentos do fim (`23-kit.test.mjs` no `ticket-23`): a mudança do matcher entra
     sozinha na junção; anotar no relatório.
  3. Relatório `etapas/relatorio-37-fim-ve-gravacao-por-shell.md`: o que fez, testes, e as ressalvas: o sincronizador
     ou outro processo geram aviso se a sessão rodou shell; o `.gravados` de outra sessão some no turno novo dela, e o
     arquivo dela vira "fora das ferramentas"; sem harness real (aceito pelo maestro).
  4. Comentário no ticket 37, revisão ao Fiel; depois do passa, Rebite (junção depois do 18).

## Feitos

- 09 e 10: juntados e resolvidos pelo Rebite. Fork `C:/Projetos/hub-mcp-banco`, ramo `integracao` 34c3e50; a pasta
  principal do fork segue no ramo `ticket-09`. Ao remover uma worktree do fork, solte antes as junções:
  `cmd /c rmdir <wt>\node_modules` e `cmd /c rmdir <wt>\lib\livesync-commonlib`.
- **23: rodada 3 PASSA** (09:23) em a419182; Rebite avisado da ponta nova. Antes: PASSA na rodada 2 (`etapas/parecer-23-Cinzel.md`). Ramo `ticket-23` f304e6c, com `integracao`
  e98a891; `23-kit.test.mjs` 14/14 (~3,5 min, sem harness).
  - O Rebite foi avisado. Ele junta quando 11, 15, 17, 18, 20 e 27 estiverem resolvidos.
  - Relatório: `etapas/relatorio-23-kit-de-par-a-forma.md`. Costuras e respostas: `etapas/costuras-23-Cinzel.md`.
  - Segunda leva, depois que 17 e 18 forem juntados (fora do 23 de agora): o mod do Claude Code, a extensão
    `onAgentStop` e a `statusLine` do Copilot, e o `notify` composto do Codex.
  - Os fragmentos de hook novos entram sozinhos. O teste lê as peças do repositório (recado da Vela: o
    `fim-da-resposta/fragmentos/claude.json` do 18).

## Ticket 11: MCP do banco pelos três harnesses (rodada 1 sem conserto; falta o Codex)

- **Hub:** worktree `C:/context-hub-wt/ticket-11`, ramo `ticket-11`, ponta f351463 (com integracao c42ffa0), 9/9.
- **Fork:** worktree `C:/Projetos/hub-mcp-banco-wt/ticket-11`, ramo `ticket-11` = `integracao` 34c3e50, com o `dist`
  montado.
- **Leia:** as costuras (`etapas/costuras-11-Cinzel.md`), o relatório (`etapas/relatorio-11-mcp-do-banco-pelos-harnesses.md`)
  e o parecer (`etapas/parecer-11-Cinzel.md`: rodada 1 sem conserto; as ressalvas foram ao maestro, que as anotou no
  23 e no 25).
- **Código:** `agents/code/test/11-mcp-banco/` (`montagem.mjs`, `captura.mjs`), `agents/code/test/11-mcp-banco.test.mjs`
  (4/4) e `agents/code/test/ponta-a-ponta/11-mcp-banco.test.mjs` (aceite; `RODADAS=`).
- **Passos, às 12h15:**
  1. **FEITO (4bc2c23, 4be0679; ajudante skills-da-maquina.mjs, por estrutura).** Antes de rodar (decisão do maestro, 07:58): tirar da evidência a lista de skills da máquina. Na função que
     limpa a evidência no teste do 11, troque o nome de cada skill de `~/.claude/skills`, `~/.agents/skills` e
     `~/.copilot/skills` por `SKILL-DA-MAQUINA`. Copie o `SKILLS_DA_MAQUINA` e o `limpo` de
     `ticket-24:agents/code/test/ponta-a-ponta/24-kit-ao-vivo.test.mjs`. Limpe também a evidência do Copilot que já
     está no commit (`evidencia-11/copilot-*`) e faça o commit.
  2. Pegar a trava pela fila e rodar, na pasta da construção:
     `pwsh -NoProfile -File etapas/logs/11-corredor.ps1 -Rodadas codex`. O corredor pega e solta a trava; o estado fica
     em `etapas/logs/11-corredor.status` e o log em `11-harness-<n>.log`.
  3. Ler `evidencia-11/codex/lido.json`: em `captura`, o campo em que vão as marcas A e B, a regra e o
     `estado_do_hub`, mais `em_volta_de_A`. Pôr no relatório (rodada 2 e critérios), fazer o commit da evidência e
     pedir a rodada 2 ao Fiel.
  4. Depois do "passa", avisar o Rebite: hub `ticket-11`; o fork não muda.
- **Se o Codex falhar na captura:** o provedor próprio (`model_provider = "hub_captura"`, `requires_openai_auth`,
  `supports_websockets = false`) foi respeitado na rodada 1. Se o backend recusar, a reserva é `openai_base_url`. Se
  nada servir, perguntar ao maestro.

## Ticket 24: kit ao vivo (parte fechada em revisão; falta o Codex)

- **Hub:** worktree `C:/context-hub-wt/ticket-24`, ramo `ticket-24` (do `ticket-23`), ponta 542a538 (com o 23 2d93089, o ajudante das skills e o gpt-6.1-sol). Parecer da rodada 1: sem conserto próprio (`etapas/parecer-24-Cinzel.md`).
- **Leia:** as costuras aceitas (`etapas/costuras-24-Cinzel.md`) e o relatório
  (`etapas/relatorio-24-kit-de-par-ao-vivo.md`). Rodada 1: Claude e Copilot PASSA, às 09:12, log
  `etapas/logs/24-harness-1.log`, evidência no commit.
- **Teste:** `agents/code/test/ponta-a-ponta/24-kit-ao-vivo.test.mjs`.
  - Hub de ensaio com a "Palavra do ensaio" no `AGENTS.md`.
  - O kit roda com `-Passos 08` numa casa de ensaio.
  - Cada harness abre num repositório fora do hub, com a casa como `USERPROFILE` e `HOME`; o Codex usa
    `CODEX_HOME=<casa>\.codex`.
- **Às 12h15, depois do 11:** pegar a trava e rodar no worktree do 24:
  `HUB_HARNESS_REAL=1 HARNESSES=codex node --test --test-concurrency=1 agents/code/test/ponta-a-ponta/24-kit-ao-vivo.test.mjs > <pasta da construção>/etapas/logs/24-harness-2.log 2>&1`.
  Soltar a trava, avisar a Vela (Codex do 18) e anotar no relatório: o Codex respondeu a palavra? Seguiu o
  `CODEX_HOME` e o link `<casa>/.codex/AGENTS.md`? Usou ferramenta? Se a resposta falhar por causa do HOME do Codex,
  ver se ele lê o `~/.agents/skills` real e registrar. Fazer o commit da evidência e pedir a rodada 2 ao Fiel.
- **Depois do "passa":** avisar o Rebite (ramo `ticket-24`; junção depois do 23).

## Fatos de fonte (por curl, 2026-10-17)

- Codex, <https://developers.openai.com/codex/mcp.md>:
  - lê o `instructions` do MCP como "server-wide guidance";
  - "Keep the first 512 characters self-contained";
  - HTTP: `bearer_token_env_var`, `http_headers`, `enabled_tools`, `tools.<tool>.approval_mode`.
- Codex, `config-reference.md`: `openai_base_url`; `model_providers.<id>.base_url`, `requires_openai_auth` e
  `supports_websockets`. O 0.162.1 entra pelo login do ChatGPT (`https://chatgpt.com/backend-api/codex`). O
  `codex exec` fora de repositório git pede `--skip-git-repo-check`.
- Claude Code: `${VAR}` vale nos `headers` do `~/.claude.json`, e o `metadata` do `SKILL.md` é um mapa livre.
- Copilot: `headers` com expansão de variável. As instruções do servidor MCP só entram com
  `--allow-all-mcp-server-instructions`, e não há chave de configuração para isso. Detalhe no relatório do 23.
- App-server do Codex: o hash do hook não depende do caminho, e ele grava sqlite no `CODEX_HOME`. Por isso o kit o
  roda numa cópia.

## Armadilhas

- `%TEMP%` é curto (`GUSTAV~1.DEL`): use `realpath` para o Claude Code e o fork em modo local.
- **Barra invertida:** em heredoc do Bash e em python inline, o `\\` vira `\`. Arquivo com barra invertida, só pelo
  Write ou pelo Edit. Depois de criar um, rode `node --check`.
- `src/*.ts` do fork: editar com o Edit. Os unitários do fork pedem `TEMP` e `TMP` no caminho longo.
- Codex: o hífen do nome do servidor vira sublinhado no hook.
- `maestri ask` sem barra invertida nos caminhos; o `ask` longo vai em segundo plano.
- App-server do Codex numa pasta de ensaio: ela fica presa por instantes. Apague com `apagarEnsaio` (prova 03), com
  espera.
- Contagem de PASSA: conte as linhas no log, não de cabeça.
