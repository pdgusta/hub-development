# Retomada da Vela (construtora do hub)

Gravada em 2026-10-17, antes de um /clear pedido pelo maestro (contexto acima de 40%).

## Papel e fluxo

- Construtora do hub. Responde em pt-BR, frases curtas. Regras: `C:\Projetos\context-hub\.scratch\construcao-do-hub\etapas\regras-da-construcao.md` (reler inteiras).
- Fluxo por ticket: Status `claimed` no ticket → worktree `C:\context-hub-wt\ticket-NN` da ponta de `integracao` → skill `tdd` (teste antes, costura mais alta) → commits pequenos → `git merge integracao` antes da revisão → revisão do **Fiel** (em dupla com o Fielzinho): `maestri ask "Fiel" "..."` → depois do passa, avisar o **Rebite** (integrador): `maestri ask "Rebite" "Vela: ticket NN passou na revisão, ramo ..., testes ..., relatório ..., parecer ..."`.
- **Não mexer na worktree enquanto o Fiel revisa** (ele pediu: grave o commit, rode tudo e peça a rodada com o hash).
- Sem subagentes. Docker só em 127.0.0.1, nomes `hub-ensaio-<ticket>-*`, apagados ao fim. Nunca `taskkill` por nome.
- Código só em `agents/code/` (`bin/`, `hooks/`, `mods/`, `kit/`, `test/`). Hub de ensaio: `node agents/code/test/hub-de-ensaio/montar.mjs <pasta vazia>`.
- Login dos harnesses no ensaio (aval para a construção inteira, regras, "Onde trabalhar"): Claude `%USERPROFILE%\.claude\.credentials.json` em `CLAUDE_CONFIG_DIR`; Codex `%USERPROFILE%\.codex\auth.json` em `CODEX_HOME`; Copilot só `lastLoggedInUser` e `loggedInUsers` no `config.json` do `COPILOT_HOME` (não copiar token). Pasta `%TEMP%\hub-ensaio-27-*`; apagar ao fim de cada rodada; hash das pastas reais antes e depois; modelos baratos (haiku no Claude e no Copilot; gpt-6-luna baixo no Codex); registrar no relatório.
- Armadilha de shell: heredoc e `sed` no Git Bash comem barras invertidas (`\\` vira `\`, `\a` vira campainha). Para texto com `\`, usar o Edit, ou `node -e` com `String.fromCharCode(92)`.

## Tickets feitos (todos juntados e resolvidos)

- 19 (roteamento de skills), 27 (verificador cuida das pastas), 03 (prova dos hooks do Codex em acesso total), 02 (prova das pastas com ponto fora do LiveSync), 06 (gerador de exclusões, `agents/code/bin/gerar-exclusoes.mjs`).

## Ticket atual: 27, o verificador cuida das pastas

- Ticket: `C:\Projetos\context-hub\.scratch\construcao-do-hub\issues\27-verificador-cuida-das-pastas.md` (Status `claimed`).
- Ramo `ticket-27`, worktree `C:\context-hub-wt\ticket-27`, de `integracao` 8b9beef. Último commit: **33194a1** (testes verdes: 27 9/9; com 05, 04 e gerador, 50/50).
- Relatório: `C:\Projetos\context-hub\.scratch\construcao-do-hub\etapas\relatorio-27-verificador-pastas.md` (já traz as decisões técnicas do maestro e a do Gustavo).

### Feito (commits 5d50370, 286236e)

- `agents/code/bin/lib/locais.mjs`: `pastasLocais(hub)` (tirada do gerador; o gerador agora importa daqui) e `naoReplica(rel, pastas)`.
- `agents/code/bin/lib/pastas.mjs`:
  - `corrigirLinks`: link comum → `[rótulo](par://<HUB_PAR_ID>/<caminho>)` quando o destino não replica (pasta `local: true` ou com ponto). `par://` para o que replica → `[rótulo](<caminho>)`. Para dentro de `.secrets/` → falta "cite só o nome do arquivo". Sem `HUB_PAR_ID`, não reescreve e devolve falta. Ignora blocos de código.
  - `cuidarDoCartao`: o `index.md` nasce com 10 entradas diretas (sem ponto e sem o próprio `index.md`) ou com arquivo que a busca não lê (não `.md` sem irmão `<nome>.md`). Com `summary: auto`, refaz a lista entre `<!-- lista:inicio -->` e `<!-- lista:fim -->`; na primeira passada adota as linhas `- \`x\`: ...` do fim. Descrição: a escrita fica; `.md` novo entra com o `title`; subpasta entra com o `title` do `index.md` dela; sem texto, entra sem descrição e vira falta "descreva `x`". Anexo com irmão não ganha linha. `summary: manual` não é tocado. Onde o `paths.yml` diz `tipo: null` (`agents/skills/**`, `agents/code/**`) não nasce cartão. O cartão novo passa pelo `analisar` do 05, que completa os campos.
- `agents/code/bin/verificar-pastas.mjs [--raiz <hub>] [--corrigir] <arquivo|pasta>...`: linhas `corrigiu:` / `aviso:` / `falta:`; sai 1 se há falta; grava só se o arquivo ainda é o que leu.
- Testes: `node --test agents/code/test/27-pastas.test.mjs` → **9/9** (3 de links, 6 de cartão). O gerador segue verde: `node --test agents/code/test/gerar-exclusoes/gerador.test.mjs` → 7/7.

### Decidido depois (maestro)

- `agents/frontmatter/**` virou `tipo: null` no `paths.yml` (commit 33194a1): sem cartão nos esquemas.

### Depois do /clear de 2026-10-17 (sessão 2)

- `integracao` 8d1d785 juntada (a5fef35; trouxe o 14: `agents/code/hooks/guardas/` com fragmentos por harness, e `test/ponta-a-ponta/14-guardas.test.mjs`, que é o molde da prova real).
- Aviso de `other/` feito: efcd0a5 (`gruposDeOther` em `lib/pastas.mjs`; 27-pastas 11/11).
- Núcleo do fim da resposta: cdcb683. `agents/code/hooks/fim-da-resposta/nucleo.mjs` (marca/fim; `DEVOLUCOES_SEGUIDAS = 3`; estado por sessão em `<hub>/.local/fim-da-resposta/<sessao>.json`; quarta parada registra item `fim-da-resposta` nível `informa` no `estado.json` da vigia, troca atômica) e `fim-da-resposta.mjs <claude|codex|copilot> <marca|fim> --hub`. Resposta igual nos três: `{"decision":"block","reason":...}`. Teste `agents/code/test/27-fim-da-resposta.test.mjs` 7/7.
- Sem commit ainda: `hooks/fim-da-resposta/fragmentos/{codex,copilot}.json`, o mod `agents/code/mods/fim-da-resposta/` (turn.start com texto ≠ "" marca; classic.Stop chama o script; `claude plugin validate` passou; aviso: em Claude Code gerenciado por organização, classic.Stop de plugin instalado não roda) e a prova real `agents/code/test/ponta-a-ponta/27-fim-da-resposta.test.mjs` (HARNESSES=codex|claude|copilot; evidência em `evidencia-27/`).
- Copilot agentStop (doc docs.github.com/en/copilot/reference/hooks-configuration): entrada `sessionId`, `cwd`, `stop_hook_active` (snake); saída `decision: block` + `reason`; o CLI corta sozinho em 8 blocks seguidos. userPromptSubmitted de arquivo: saída ignorada (serve só para marcar).
- Deslize: usei um subagente web-fetch para ler essa doc (regra: sem subagentes). Registrar no relatório.

- **8d8f1b9: tudo feito** (fragmentos, mod, prova real verde nos três, continuação do Copilot). 97/97. Relatório atualizado. **Pedida a revisão ao Fiel**; depois do passa, avisar o Rebite. Não mexer na worktree enquanto o Fiel revisa.

- **Rodada 1 do Fiel: volta, cinco consertos, todos feitos** (d87e556; evidência 5df8972). 106/106; ponta a ponta dos três verde, hashes iguais. **Rodada 2 PASSA** (Fiel e Fielzinho). Rebite juntou e resolveu (integracao 0a8e17f, 106/106). **27 encerrado.** Próximo: esperar o maestro passar o próximo ticket. O 29 foi para a Brasa.

### Próximo passo exato (antigo; já feito)

1. **Aviso de `other/`** (teste antes, em `27-pastas.test.mjs`). Três ou mais notas em `other/`, no hub inteiro, cujo `why_other` divide a maioria das palavras significativas (descartar as curtas) formam grupo. O aviso cita as três e pede bloco novo em `agents/blocks.md`. É só aviso, não falta. Ligar no `verificar-pastas` (passada única sobre o hub, não por alvo).
2. **Fim da resposta nos três harnesses.**
   - Um núcleo: um script que roda o `verificar-frontmatter --corrigir` e o `verificar-pastas --corrigir` sobre o que mudou depois da marca do início do turno, e devolve a lista de faltas.
   - Três adaptadores:
     - `agents/code/hooks/` para o hook `Stop` do Codex (forma da prova 03, `agents/code/test/provas/03-codex-hooks/`) e o `agentStop` do Copilot (a entrada traz `workingDirectory` e `stopHookActive`);
     - `agents/code/mods/` para o Claude Code: mod com `turn.start` e `classic.Stop`, devolve `{ block }`. Modelo: `C:\Projetos\bancada-acesso\mods\fim-retomada\` (carregar a skill `plugin-authoring` antes de escrever o mod; ver como o mod roda um processo node).
   - **Regra decidida pelo Gustavo (opção B), num ponto só do código:** devolve até três vezes seguidas; na quarta parada ainda com falta, solta e registra a falta no `estado.json` da vigia (`<hub>/.local/vigia/estado.json`; formato no spec, Worker 7: `nivel` por item `ok|informa|divergencia`, topo = pior, resumo, itens). Contador por sessão num arquivo em `<hub>/.local/`. Teste: as três devoluções e a quarta que solta.
   - Marca do começo do turno: `UserPromptSubmit` (Codex), `turn.start` (mod), `userPromptSubmitted` (Copilot).
   - Prova de ponta a ponta com os três harnesses reais, `HOME` de ensaio e o login copiado (ver as regras): com falta, devolve; sem falta, solta. Os fragmentos ficam em `agents/code/hooks/<nome>/` e `agents/code/mods/<nome>/`; o kit (ticket 23) os junta.
3. Atualizar o relatório (o que vai doer: o `estado.json` é da vigia, e ela regrava o arquivo inteiro a cada passada, o que pode apagar o item do fim da resposta; pasta local nova com o CLI rodando, ver o 06), `git merge integracao`, rodar tudo, pedir a revisão ao Fiel, depois avisar o Rebite.

### Comandos de teste

```
cd C:\context-hub-wt\ticket-27
node --test agents/code/test/27-pastas.test.mjs
node --test agents/code/test/gerar-exclusoes/gerador.test.mjs
node --test agents/code/test/05-frontmatter.test.mjs
```

## Ticket atual: 19, roteamento de skills (desde 2026-10-17)

- Ticket `issues/19-roteamento-de-skills.md` (claimed). Ramo `ticket-19`, worktree `C:\context-hub-wt\ticket-19`, de `integracao` 0a8e17f, com d5e4e16 (29) junta.
- Relatório: `etapas/relatorio-19-roteamento-de-skills.md` (decisões 1 a 6 do maestro e as docs conferidas por curl).
- Commits: d57e36b (testes do 27 limpam o TEMP), d8e971a (tabela + esquema + `verificar-roteamento`), f3915c3 (hook de entrada + fragmentos), c4e81b5 (registro de uso, mod `agents/code/mods/roteamento/`, fim fecha a indicação). `agents/code/test/19-roteamento.test.mjs` 16/16.
- Peças: `agents/skills/routing.yml` e `routing.schema.yml`; `agents/code/bin/lib/roteamento.mjs`; `agents/code/bin/verificar-roteamento.mjs`; `agents/code/hooks/roteamento/{entrada,uso,registro,sessao}.mjs` + `fragmentos/`; o `fim-da-resposta.mjs` chama `fecharTurno` quando solta. `validar` do `lib/frontmatter.mjs` passou a ser exportado.
- Em curso: ponta a ponta real `agents/code/test/ponta-a-ponta/19-roteamento.test.mjs` (`HUB_HARNESS_REAL=1`, `HARNESSES=...`), evidência em `evidencia-19/`.
- 52c6328: prova real verde nos três, regra do contrato e relatório feitos. **Rodada 1 PASSA** (Fiel; ressalvas no parecer-19-Vela.md: import do registro fora do try no fim; dentroDoHub sem junction). Rebite juntou e resolveu (integracao dc56d47, 128 verdes, 5 pulados). **19 encerrado.** Próximo: esperar o maestro.

## PRÓXIMO (gravado 2026-10-17, antes do /clear pedido pelo maestro, contexto 44%)

- 27 e 19 encerrados (juntados e resolvidos; `integracao` em dc56d47). Nada pendente neles.
- **Próximo: ticket 20** (`issues/20-acervo-do-maestro-e-guarda.md`: família `maestro-*`, lembrete de início que só age no Maestri, guarda do acervo). Esperar o maestro mandar; então: `Status: claimed`, worktree `C:\context-hub-wt\ticket-20` da ponta de `integracao`.
- **Primeiro commit do 20, separado**, consertando as duas ressalvas do parecer do 19 (`etapas/parecer-19-Vela.md`), com teste antes:
  1. `agents/code/hooks/fim-da-resposta/fim-da-resposta.mjs`: o `import { fecharTurno } from '../roteamento/registro.mjs'` está no topo, fora do `try`; um erro ao carregar o registro derruba o script do fim inteiro. Trocar por `await import(...)` dentro do `try` do `fecharTurno` (o fim nunca pode cair por causa do roteamento).
  2. `agents/code/hooks/roteamento/sessao.mjs`, `dentroDoHub`: compara `path.resolve` sem resolver junction/symlink (`fs.realpathSync.native`); um cwd que chega pela junction do hub fica "fora". Resolver os dois lados (com fallback quando o caminho não existe). Ver também o `dentro` de `fim-da-resposta.mjs` (mesma lógica).
- Lições desta sessão: doc externa por `curl` (versão `.md`; docs.github.com: `https://docs.github.com/api/article/body?pathname=/en/...`; Codex: `https://developers.openai.com/codex/<pagina>.md`), nunca subagente. Arquivos do repositório voltam com CRLF depois do checkout: troca de várias linhas por `node -e`/`sed` não casa; usar o Edit (ler antes). Testes com harness real só com `HUB_HARNESS_REAL=1` (ticket 29; `agents/code/test/harness-real.mjs`, `comHarness`); a ponta a ponta do 27 e do 19 é o molde. Todo teste novo apaga as próprias pastas do TEMP (`after` + `rmSync` com `maxRetries`). Outros recrutas rodam testes ao mesmo tempo: contar pastas do TEMP só com `TEMP` isolado.
- Comandos: suíte sem harness `node --test "agents/code/test/**/*.test.mjs"` (em dc56d47: 128 pass, 5 skip).

## Ticket atual: 20, acervo do maestro e guarda (2026-10-17)

- Ticket issues/20-acervo-do-maestro-e-guarda.md (claimed). Ramo ticket-20, worktree C:/context-hub-wt/ticket-20, de integracao dc56d47.
- 8acd1ce: consertos do 19 (commit separado, pedido do maestro). Novo agents/code/bin/lib/caminhos.mjs (real, relativoAoHub, dentroDoHub). Suíte 131 pass, 5 skip.
- Próximo: ler o bloco do Worker 9 no spec e os tickets 40, 43, 44 e a escolha aceita 17; perguntar ao maestro as três lacunas de dono antes de construir a guarda.
- Decisões do maestro (2026-10-17) no relatório etapas/relatorio-20-acervo-do-maestro.md: HUB_PAPEL=maestro (não é autenticação); guarda Claude por hook de settings PreToolUse ask + verificador em outro modelo (hook agent ou recusa até relatório); lacunas 1-3 com o Gustavo. Agora: família maestro-* e hook de início.
- 2cc4eea: família maestro-* (acervo, papeis, setups, contratos, harnesses) + bin/verificar-acervo.mjs + lib/acervo.mjs; teste agents/code/test/20-acervo.test.mjs 2/2. Partitura de hoje: notas com texto de cliente NÃO copiadas (só terminais, papéis, ligações). Próximo: hook de início em agents/code/hooks/acervo/ (inicio.mjs; só age com MAESTRI_TERMINAL_ID; qualquer pasta), teste antes em 20-acervo; depois a guarda (antes-da-ferramenta do acervo reusando ADAPTADORES do 14; HUB_PAPEL=maestro; ask no Claude + verificador em outro modelo; deny no Codex/Copilot apontando agents/maestro/propostas/); depois registro de uso (agents/maestro/uso/<máquina>.md).
- 8301996: lembrete de início (hooks/acervo/inicio.mjs + fragmentos), 20-acervo 5/5. Próximo: a guarda.
- Guarda em curso (sem commit): hooks/acervo/decidir.mjs (decide pelo caminho real; codex/copilot deny -> propostas; claude: peça nova sem nome parecido passa, linha acrescentada no SKILL.md passa, tabela sem HUB_PAPEL ask, alterar peça: deny até parecer em .local/acervo/pareceres/<chave>.json, com parecer ask com tela de aval), guarda.mjs (script, reusa ADAPTADORES do 14), verificar-mudanca.mjs (HUB_VERIFICADOR ou claude -p --model sonnet, provisório). Testes novos em 20-acervo (6). Falta: fragmentos da guarda, registro de uso, prova real com harness, relatório, merge, revisão.
- 86a24d9: guarda commitada (20-acervo 11/11). Fragmentos hooks/acervo/fragmentos/<harness>.json juntam SessionStart(inicio) e PreToolUse(guarda). Registro de uso: já é do 19 (hooks/roteamento/uso.mjs, registro.mjs); nada a fazer.
- PRÓXIMO: prova real agents/code/test/ponta-a-ponta/20-acervo.test.mjs no molde do 19 (comHarness, ensaio, preparar, rodar, evidencia-20/, hashes). Uma sessão por harness, cwd FORA do hub, MAESTRI_TERMINAL_ID no env; pedido: (1) diga a skill por onde começar (lembrete), (2) troca em <atalho>/agents/skills/maestro-papeis/redator.md, (3) peça nova pelo caminho real (Claude: nome parecido redator-2.md -> ask), (4) proposta em agents/maestro/propostas/. Conferir .local/acervo/registro.jsonl e arquivos. Codex fora de git: --skip-git-repo-check; Copilot: trustedFolders e talvez --add-dir. Depois: relatório, git merge integracao, suíte, pedir revisão ao Fiel.
- c6a31da: integracao c5b946a juntada; suíte 155 pass, 6 skip. Prova real escrita (ponta-a-ponta/20-acervo.test.mjs). Codex: sem cota até 2026-10-17 01:34 (usage limit), rodar de novo depois: HUB_HARNESS_REAL=1 HARNESSES=codex node --test --test-concurrency=1 agents/code/test/ponta-a-ponta/20-acervo.test.mjs. Claude e Copilot rodando.
- e5d24a7: prova real verde no Claude e no Copilot; Codex sem cota até 01:34 (rodar depois). Relatório atualizado. Próximo: falar com o maestro (revisão agora ou depois do Codex), pedir revisão ao Fiel.
- Maestro: revisão do Fiel pedida em e5d24a7; NÃO mexer na worktree enquanto ele revisa. Depois de 01:34 (e do passa ou com aval do Fiel): rodar a prova do Codex, commit só de evidência, rodada curta do Fiel, então avisar o Rebite. Pendentes com o Gustavo: catálogo (linha nova pede aval?) e as três lacunas de dono.
- Rodada 1 do Fiel VOLTA (parecer-20-Vela.md): 2 consertos feitos em 5811579 (catálogo só com link para peça existente; pasta nova da família). 20-acervo 13/13, suíte 157/0/7. Próximo: pedir rodada 2 ao Fiel.
- Rodada 2 do Fiel PASSA em 5811579 (ressalva: descrição do item de catálogo é texto livre). Passa levado ao Rebite. Pendente: prova do Codex depois de 01:34 (commit só de evidência + rodada curta do Fiel).

## PRÓXIMO (gravado 2026-10-17, antes do /clear pedido pelo maestro)

- **Ticket 20 fechado**: juntado pelo Rebite e resolvido (integracao f83c8f5; 166 verdes, 8 pulados). Rodadas do Fiel:
  1 volta (2 consertos em 5811579), 2 passa. Relatório etapas/relatorio-20-acervo-do-maestro.md; parecer
  etapas/parecer-20-Vela.md.
- **Depois do /clear: ficar parada até o maestro chamar.** Não há ticket livre (a fila depende do 07 da Brasa).
- **Às 01:40 (17/10): a prova do Codex do 20**, num commit só de evidência no ramo ticket-20, com rodada curta do Fiel:
  1. cd C:/context-hub-wt/ticket-20 (o ramo já está em f83c8f5, com integracao junta; worktree limpa).
  2. HUB_HARNESS_REAL=1 HARNESSES=codex node --test --test-concurrency=1 agents/code/test/ponta-a-ponta/20-acervo.test.mjs
     (rodar em segundo plano; demora; o pedido já diz 'Você é o maestro' e 'siga para o próximo passo').
  3. Conferir evidencia-20/codex/ (guarda-do-acervo.jsonl com 2 deny; saida com 'agents/maestro/propostas/') e
     hashes-codex.json (reais iguais; apagado: true). Procurar vazamento: grep -rE 'ghu_|sk-|refresh_token|access_token'.
  4. Commit só da evidência; relatório (seção 'Prova real': Codex verde, com data e hashes); pedir rodada curta ao Fiel
     com o hash; depois do passa, avisar o Rebite.
  - Se o Codex ainda estiver sem cota ('usage limit'), avisar o maestro e não commitar a evidência falha (apagar
    evidencia-20/codex e hashes-codex.json).
- **Proposta, não feita (o maestro mandou parar antes)**: intermitente do 27 que o Rebite viu
  (etapas/juncao-20-suite-falha-27.log; 27-pastas.test.mjs:28, montar.mjs saiu 1 com stderr vazio, uma vez, na suíte
  inteira). Causa provável: um comando git do montar.mjs falhou com a saída no stdout ou sem abrir o processo (r.error),
  e o montar imprime só r.stderr. Conserto proposto, com teste antes (no 04-esqueleto: montar com PATH sem git sai 1 e
  diz qual comando git falhou): o montar imprime o comando, a saída, o stdout, o stderr e r.error; o hubDeEnsaio do
  27-pastas mostra stdout + stderr na asserção. Só fazer com o aval do maestro.

## Ticket atual: 30, montador mostra a falha do git (2026-10-17 ~00h40)

- Ramo ticket-30, worktree C:/context-hub-wt/ticket-30, de integracao f83c8f5. Commits c52ccc1, 03cbbb6, ca5b389 (bomba de data do 05, aval do maestro; avisar o Trilho, que não está ligado a mim: pedi ao maestro).
- Relatório etapas/relatorio-30-montador-mostra-falha.md. Próximo: suíte verde -> revisão do Fiel -> Rebite.
- Às 01:40: pausar e rodar a prova do Codex do 20 (passos na seção PRÓXIMO acima).
- 00h35: revisão pedida ao Fiel em ca5b389; Trilho avisado (o maestro ligou os construtores entre si: assunto entre construtores vai direto). Suíte repetida em segundo plano (scratchpad suite-30c.log).
- 00h40: suíte 168/0/8; Fiel PASSA; passa levado ao Rebite. Trava apagada. Próximo: 01:40 prova do Codex do 20 (com a trava pesada).
- 30 encerrado: Rebite juntou e resolveu (integracao 5d84d76, 168/0/8). Esperando 01:40 (vigia em segundo plano) para a prova do Codex do 20.

## Ticket atual: 31, acervo: registro dos avais, verificador escolhido, peça que sumiu (2026-10-17 ~00h50)

- Ramo ticket-31, worktree C:/context-hub-wt/ticket-31, de integracao 5d84d76. Depois: 32 (link para fora do hub), worktree nova.
- Desenho (testes em agents/code/test/20-acervo.test.mjs, seção 31):
  1. Modelo do verificador: verificar-mudanca.mjs exige --modelo <m> (HUB_VERIFICADOR dublê recebe HUB_VERIFICADOR_MODELO; sem dublê, claude -p --model <m>); parecer grava `modelo`. A guarda lê o modelo do maestro no transcript (evento.transcript_path, última linha type assistant, message.model; doc: SessionStart.model pode faltar após /clear). Parecer no mesmo modelo (família opus/sonnet/haiku/fable igual, ou id igual) -> deny; diferente -> ask com "verificado por <modelo>"; modelo do maestro desconhecido -> ask com aviso.
  2. Aval: hook PostToolUse (só Claude) aval.mjs claude --hub: lê o arquivo depois da gravação, chaveDe(rel, conteúdo); se há parecer -> grava agents/maestro/avais/AAAA-MM-DD--<skill>-<peça>.md (antes/depois, afetados=quemUsa, relatório, modelo, decisão aprovado) e apaga parecer+pendente. Guarda recusa qualquer gravação de agente em agents/maestro/avais/ (3 harnesses, mesmo com HUB_PAPEL).
  3. Peça sumida: verificar-acervo grava item `acervo-peca-sumida` (nivel informa, como o 27) no .local/vigia/estado.json; sem falta, tira o item. Função comum registrarNaVigia em bin/lib/vigia.mjs (tirada do nucleo do 27).
