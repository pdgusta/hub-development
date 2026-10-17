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
- 01h15: 31 com tudo commitado até cc8c852; relatório escrito. Falta: suíte inteira e ponta a ponta do 20 só Claude (HUB_HARNESS_REAL=1 HARNESSES=claude) no ramo ticket-31, ambos com trava; depois Fiel, Rebite. 01:40: prova do Codex do 20 (ramo ticket-20) com trava.
- 01h20: 32 feito em 94c42ac (worktree C:/context-hub-wt/ticket-32), relatório escrito. Falta: suítes do 31 e do 32 (trava), ponta a ponta Claude do 31, Fiel (pode pedir os dois juntos), Rebite. 01:40 prova Codex do 20.
- 01h26: Fiel rodada 1 VOLTA nos dois; consertos 31 b710f2d (.local/acervo/ recusado), 32 6beaf15 (%20). Rodada 2 pedida. Suítes e Claude real do 31 esperam a trava. 01:40 Codex do 20.
- 01h29: 31 e 32 PASSAM (Fiel rodada 2); levados ao Rebite sem suíte inteira minha (trava). Próximo: 01:40 Codex do 20 (trava); depois, se der, ponta a ponta Claude do 31 (HUB_HARNESS_REAL=1 HARNESSES=claude ponta-a-ponta/20-acervo no ramo ticket-31).
- 01h31: maestro: a ponta a ponta Claude do 31 também é minha, na mesma janela da trava do Codex do 20. Ordem da trava: Trilho, Rebite (suíte 31+32), depois eu; Brasa antes: esperar. Depois: relatório do 31, Fiel confere evidência, avisar Rebite (só então ele resolve o 31).
- 01h51: Rebite juntou 31+32 (integracao 57e85cf, 178/0/8); 32 resolvido; 31 espera minha ponta a ponta Claude + Fiel. Trava com o Trilho (01:50); vigia bcrz6samt pega a trava quando ele largar.
- 02h04: ponta a ponta real achou buraco: Edit LF em peça CRLF passava sem guarda (Claude gravou). Conserto 050fb14 (trocar do 14 casa CRLF) + asserção do Codex pelo registro. integracao juntada. Falta: rodar de novo HARNESSES=claude,codex no ticket-31 (trava; Brasa com ela 01:59), commit da evidência, relatório, Fiel, Rebite.
- 02h06: maestro aprovou; depois de rodar de novo, pedir ao Fiel rodada nova de CÓDIGO (050fb14 + merge), não só evidência. Comentário no ticket 14 feito.
- 02h14: evidência 4e420a6 (2ª rodada real verde Claude+Codex). Rodada nova de código pedida ao Fiel em 4e420a6. Depois do passa: avisar Rebite (junta e resolve o 31). Não mexer na worktree ticket-31.
- 02h16: Fiel trouxe 2 consertos tardios do 19 (parecer-19-Vela.md: fecharTurno uma linha por skill; caminhosDoPedido normalizar barras antes de filtrar); levados ao maestro para ticket novo.
- 02h18: maestro publicou o ticket 34 (issues/34-roteamento-registro-por-skill-e-barras.md, os 2 consertos do 19): meu depois que o 31 fechar. 33 reservado (sobras do link fora do hub, com o Gustavo).

## PRÓXIMO (gravado 2026-10-17 02h22, antes do /clear; contexto acima de 40%)

- Fechados nesta sessão: 30 (juntado, resolvido), 32 (juntado, resolvido), 31 (rodada 3 PASSA; Rebite avisado para
  juntar 4e420a6 e resolver; conferir no ticket se ele resolveu). A prova do Codex do 20 foi feita pelo ramo do 31
  (evidencia-20/codex, hashes-claude-codex.json).
- **Próximo: ticket 34** (`issues/34-roteamento-registro-por-skill-e-barras.md`): os dois consertos tardios do 19 em
  `etapas/parecer-19-Vela.md`: (1) `fecharTurno` (agents/code/hooks/roteamento/registro.mjs): linha de papel com várias
  skills registra uma linha por skill, inclusive as indicadas e não usadas; (2) `caminhosDoPedido`: normalizar as
  barras antes de filtrar (`research\dados.json` tem de casar). Fluxo: Status claimed; worktree
  `git -C C:/context-hub worktree add C:/context-hub-wt/ticket-34 -b ticket-34 integracao`; tdd (teste em
  agents/code/test/19-roteamento.test.mjs); relatório etapas/relatorio-34-...md; Fiel; Rebite.
- Ressalvas levadas ao maestro (não são minhas até ele mandar): asks de nome parecido e da tabela sem registro em
  agents/maestro/avais/ (31).
- Regras novas desta sessão: **trava pesada** (`etapas/trava-pesada.md`: suíte inteira, harness real, Docker, npm,
  indexação; criar com nome/o que/hora, apagar ao fim mesmo falhando; existe e <30 min: esperar). Construtores ligados
  entre si (Trilho, Brasa): assunto entre construtores vai direto. Mudança de código depois do passa: rodada nova de
  código no Fiel.
- Armadilhas: arquivos do repo em CRLF; o Edit do Claude casa old_string LF com CRLF (a guarda agora também). Edit
  multilinha por `node -e` não casa CRLF: usar o Edit. Bash com `&` e redirecionamento prende o comando até o fim.
- 02h21: 31 PASSA rodada 3; Rebite avisado; ressalva (asks sem registro em avais) ao maestro. Próximo: ticket 34.
- 02h32: ticket 34 em curso. Ramo ticket-34 (worktree C:/context-hub-wt/ticket-34), commits cd52173 e 0e39c35, 19-roteamento 19/19, relatório escrito. Falta: suíte inteira (esperar a trava), Fiel, Rebite.
- 02h41: suíte 185/0/8 em 0e39c35; revisão pedida ao Fiel. Não mexer na worktree ticket-34 enquanto ele revisa. Depois do passa: Rebite.
- 02h44: 34 PASSA (rodada 1); Rebite avisado. Próximo: esperar o maestro.

## Ticket 09, MCP do banco com versão (2026-10-17 ~02h55): só leitura até o 07 entrar em integracao

- Maestro: próximo é o 09; até o Rebite resolver o 07, só leitura (nada de worktree nem código). Depois: worktree da
  ponta de integracao e seguir.
- Lido: issues/09, spec Worker 5 (spec.md:141-149), faixa 5 (spec-partes/faixas-05-06.md:1-219), relatório do 07.
- Achados: o spec diz "fork local do es617/obsidian-sync-mcp em repositório próprio fora do hub (pergunta abaixo)",
  sem a resposta escrita; existe C:/Projetos/hub-mcp-banco, clone limpo do upstream (origin es617, main 1a4d53f
  v0.10.0, de 2026-10-15 21h49, só package-lock.json mudado); tentativa-paralela/faixa-05 não tem nada além do início.
- Banco de ensaio: o 07 deu agents/code/kit/par/banco/banco.psm1 e agents/code/test/banco/ensaio.psm1
  (New-/Start-/Remove-EnsaioBanco); faixa 5 pede CouchDB em 127.0.0.1:5996, MCP 8796 (escrita) e 8797 (leitura).
- Validador: o do hub é node (agents/code/bin/lib/frontmatter.mjs, validar exportado); o fork TS em Node pode importar
  o mesmo, sem segundo validador (ponto aberto da faixa 5).
- Perguntas levadas ao maestro: onde mora o fork; usar o clone existente; banco de ensaio pelo ensaio.psm1 do 07.
- Leitura do upstream (C:/Projetos/hub-mcp-banco, só leitura): src/vault.ts grava por DirectFileManipulator.put da
  lib/livesync-commonlib (sem revisão de base); readNote devolve só o texto. O r1.py do spike
  (C:/Projetos/spike-livesync/r1.py) grava o pedaço (leaf) e o documento de metadados com _revisions e
  new_edits=false sobre a rev lida, mas sem E2EE: no fork, o pedaço tem de sair cifrado pela própria lib (ver como o
  put monta os pedaços) e só o documento de metadados ir por _bulk_docs new_edits=false. A pergunta "onde mora o fork"
  é do Gustavo (planejamento/agentes/Worker 5.md:6).
- Respostas do maestro (~03h00): (1) onde mora o fork: com o Gustavo pelo chat (recomendação: repositório próprio
  C:/Projetos/hub-mcp-banco). (2) Se for o repositório próprio, usar o clone que existe; conferido: HEAD 1a4d53f =
  tag v0.10.0 = origin/main; o package-lock.json perde 11 linhas (jose 5.10.0, optional/peer), efeito do npm install:
  registrar no relatório. (3) Banco de ensaio pelo ensaio.psm1 do 07 (hub-ensaio-09-*, porta 5996); o fork importa
  agents/code/bin/lib/frontmatter.mjs do hub por HUB_ROOT, sem segundo validador.
- Até a resposta do Gustavo e o 07 em integracao: só leitura.
- 02h52: Rebite: 31 resolvido (e82ce65); 34 juntado em 763813a, suíte dele rodando. Nada a fazer até ele resolver o 34; 09 segue só leitura.
- 03h00: 34 resolvido pelo Rebite (integracao 763813a, 186/0/8). 34 encerrado. Próximo: 09, esperando o Gustavo e o 07.

## Ticket 28, pastas locais: script e git (2026-10-17 ~03h15)

- Maestro: pegar o 28 enquanto o Gustavo não responde sobre o fork (o 09 segue meu). Docker com a trava.
- Ramo ticket-28, worktree C:/context-hub-wt/ticket-28, de integracao 763813a.
- Desenho do 28: skill agents/skills/nova-pasta-local/ (SKILL.md + nova-pasta-local.ps1, importa
  agents/code/kit/par/banco/banco.psm1; -EnvFile do par, padrão $env:HUB_BANCO_ENV; -Pasta <rel>; -TornarLocal).
  Nova: Stop-Sincronizador, cria pasta + index.md local: true, gerador, Start-Sincronizador. Tornar local: Stop, põe
  local: true, gerador, CLI `rm <caminho>` de cada arquivo da pasta (ls <prefixo>) no cli-db do par + `sync`, Start.
  Gerador recusa -> para, mostra o caminho, sincronizador parado e avisado (sai ≠ 0).
- Gerador escreve .git/info/exclude (git rev-parse --git-path info/exclude; só se há .git), num bloco marcado
  (preserva o resto): `.*`, `!.gitignore`, `!.gitkeep` (o esqueleto versiona os dois), `/<pasta local>/`. Não entra no
  `mudou` (git não precisa religar nada).
- Testes: gerador.test.mjs (exclude + git status); sem Docker o YAML ilegível; com Docker (trava) 28-pastas-locais.test.ps1
  sobre ensaio.psm1 (hub-ensaio-28-*).
- Pergunta ao maestro: "tornar local" de pasta já versionada também faz git rm -r --cached?
- 03h05: maestro aceitou git rm -r --cached no 'tornar local'; relatório e aviso do script dizem que o histórico do git guarda as versões antigas (remoção só daqui para frente; limpar histórico fora). '.*' com exceções e -EnvFile/HUB_BANCO_ENV ok. Commit do exclude: e74327c (gerador 8/8). Próximo: o script (teste sem Docker do YAML antes).
- 03h07: Gustavo decidiu (A): fork em C:/Projetos/hub-mcp-banco, repositório próprio fora do hub, só local, um ramo por ticket (ticket-09); no hub, o passo do kit (05-mcp-banco.ps1) e o teste de ponta a ponta; GitHub depois, com aval dele. O 09 é meu depois do 28. O 33 (sobras do 32) vai ao Trilho; ele pode perguntar sobre o 27 e o 32.
- 03h11: 898af49: skill agents/skills/nova-pasta-local/ (SKILL.md, nova-pasta-local.ps1), cli-falso com daemon, teste sem Docker (banco/pastas-locais-sem-docker.ps1 + 28-pastas-locais-sem-docker.test.mjs) 12/12, regra no AGENTS.md. Próximo: teste com Docker 28-pastas-locais.test.ps1 (trava).
- 03h12: fc6c78b: 28-pastas-locais.test.ps1 (Docker, hub-ensaio-28-a/b 5992/5993). Rodando em segundo plano quando a trava do Trilho sair; log etapas/logs/28-docker-1.log. Depois: relatório, merge integracao, suíte, Fiel, Rebite. Depois do 28: 09 (fork em C:/Projetos/hub-mcp-banco, ramo ticket-09).
- 03h17: Docker do 28 verde (14 PASSA, log etapas/logs/28-docker-1.log). integracao não andou. Suíte inteira em segundo plano com a trava (etapas/logs/suite-28.log). Depois: relatório (linha da suíte), Fiel.
- 03h23: maestro: o 09 passou ao Cinzel (quarto construtor); eu sigo no 28 e respondo ao Cinzel sobre o que li do 09 (seção 'Ticket 09' desta retomada). Regra nova: no máximo um subagente por vez, só tarefa fechada e leve. Depois do 28, o maestro passa o próximo.
- 03h25: regra nova: além do subagente, até três subagentes Haiku 5.5 esforço médio (Agent, model haiku, effort medium) só para tarefa simples ou QA; nada de código de produção nem decisão; conferir o que trazem.
- 03h30: suíte 188/0/8 em fc6c78b; revisão pedida ao Fiel. Não mexer na worktree ticket-28 enquanto ele revisa. Depois do passa: Rebite.
- 03h42: rodada 1 do Fiel VOLTA (3 consertos); feitos em e134279 e 39abd57; sem Docker 24, gerador 8/8. Próximo: suíte (trava), pedir rodada 2 ao Fiel (ele roda o Docker).
- 04h16: regra nova: suíte inteira só na junção (Rebite); a minha foi parada antes de começar (trava nunca minha). Rodada 2 pedida ao Fiel em 2eec8e9. Não mexer na worktree.
- 04h27: rodada 2 VOLTA (-Titulo); conserto 5436cad, sem Docker 25. Rodada 3 pedida ao Fiel (ele roda o Docker quando a trava do Cinzel sair). Não mexer na worktree.
- 05h08: 28 PASSA na rodada 3 (Fiel); Rebite avisado (HEAD 5436cad; junção com integracao 33b817a sai limpa, conferido por merge-tree). Ressalvas: Docker não confere o título; leitura do Fielzinho pendente; histórico do git. Próximo: esperar o maestro.

## Ticket 17, vigia nas telas (2026-10-17 ~05h20)

- 28 juntado e resolvido (integracao ea6f353). Próximo do maestro: 17, antes do 16, contra o estado.json de
  etapas/costuras-16-Trilho.md (exemplo fixo nos testes); quando o 16 entrar, merge e troca pelo real. Codex real só
  depois das 06h58.
- Ramo ticket-17, worktree C:/context-hub-wt/ticket-17 (de 9453e3e, já com o 09). Costuras propostas em etapas/costuras-17-Vela.md;
  esperando o maestro antes de codar.
- Docs por curl (scratchpad/docs): Codex notify (config-advanced.md, "Notifications": um argumento JSON, type
  agent-turn-complete, thread-id, turn-id, cwd, input-messages, last-assistant-message); Copilot statusLine
  (cli-config-dir-reference: type command, command = script que recebe o JSON da sessão no stdin e imprime a linha,
  padding, refreshInterval). Mod: $.ui.status(texto); modelo agents/code/mods/fim-da-resposta (HUB_ROOT, $.process.run).
- Maestro aceitou as costuras e as quatro (1 com o Cinzel; 2 linha de status; 3 .cmd se precisar; 4 linha curta com
  ok, agente calado). Cinzel (10): HUB_MCP_BANCO_LEITURA_URL (http://127.0.0.1:8797/mcp) e
  HUB_MCP_BANCO_LEITURA_TOKEN, Authorization: Bearer (sem token 401); result.content[0] text = JSON do estado.json sem
  vistos, ou 'estado indisponível: <motivo>'; passada > 15 min: content[1] 'a vigia não roda desde <hora>'. Streamable
  HTTP do FastMCP: POST responde text/event-stream ('data: {json}'); Accept: application/json, text/event-stream;
  initialize antes, header mcp-session-id nos pedidos seguintes. O e2e do fork tem um parseSSE que cai para JSON.
- Teste agents/code/test/17-vigia-tela.test.mjs; script agents/code/hooks/vigia/tela.mjs.
- 05h15: 2947951 (início nos três) e 7a3c445 (reserva pelo MCP, node:http sem agente: o fetch deixava conexão viva e o node caía ao sair, asserção do libuv); 17-vigia-tela 10/10. Próximo: notify do Codex.

## PRÓXIMO (gravado 2026-10-17 ~06h00, antes do /clear pedido pelo maestro, contexto 43%)

- Encerrados nesta sessão: 34 (resolvido), 28 (rodada 3 PASSA, juntado: integracao ea6f353). O 09 passou ao Cinzel.
- **Ticket atual: 17, vigia nas telas** (issues/17-vigia-nas-telas-dos-harnesses.md, Status claimed). Ramo ticket-17,
  worktree C:/context-hub-wt/ticket-17, de integracao 9453e3e (com o 09). Costuras aceitas pelo maestro:
  etapas/costuras-17-Vela.md (as quatro respostas: reserva pelo MCP com o Cinzel; mod = linha de status; .cmd só se
  precisar: NÃO precisou; com ok, linha curta e agente calado).
- Commits: 2947951 (início nos três), 7a3c445 (reserva pelo estado_do_hub do MCP), 754e269 (notify do Codex),
  6b39f7a (barra), cb5c01b (fragmentos), 96bddcb (mod). Worktree limpa.
- Peças:
  - agents/code/hooks/vigia/tela.mjs: modos `inicio <claude|codex|copilot>`, `notify '<json>'`, `barra <claude|copilot>`,
    todos com --hub. Regra do texto num lugar só (resumo() e linha()). Reserva por node:http sem agente (o fetch deixava
    conexão viva e o node no Windows caía ao sair: asserção do libuv src\win\async.c); sem process.exit no fim
    (process.exitCode = 0). notify: memória em <hub>/.local/vigia/notify-codex.json (assinatura = itens fora de ok com o
    nível); só avisa com divergência e assinatura nova; falha do notificador não grava a assinatura. Notificador:
    HUB_VIGIA_NOTIFICAR, senão <hub>/agents/skills/vigia/notificar.ps1 (vem com o 16). barra lê só o arquivo (sem MCP).
  - agents/code/hooks/vigia/fragmentos/{claude,codex,copilot,codex-notify,copilot-statusline}.json ({{DIR}}, {{HUB}}).
  - agents/code/mods/vigia/ (plugin vigia-do-hub): session.start + turn.start + $.clock.every(60 s) chamam
    `tela.mjs barra claude` por $.process.run e põem em $.ui.status. hooks/vigia.test.ts (claude plugin test 2/2;
    no kit de teste: mock.env, mock.clock, e hooks do teste devolvem { value: ... }; session.start devolve { cwd }).
- Testes: `node --test agents/code/test/17-vigia-tela.test.mjs` 15/15; `cd agents/code/mods/vigia && claude plugin
  validate . && claude plugin test .` 2/2.
- Achado (fonte: app.js do @github/copilot-win32-x64 1.0.98, função da statusLine): no Windows o statusLine.command roda
  com shell: true, cwd da sessão, JSON da sessão no stdin, limite 10 s; comando com argumentos funciona (sem .cmd).
- **Falta (próximo passo exato):**
  1. Ponta a ponta real: agents/code/test/ponta-a-ponta/17-vigia-tela.test.mjs no molde do 27/19 (comHarness,
     HUB_HARNESS_REAL=1, HARNESSES=claude,copilot agora; codex depois das 06h58), com trava pesada e o aval de login
     (HOME de ensaio, hashes, modelos baratos). Fragmentos de início instalados no HOME de ensaio; estado.json de
     divergência no hub de ensaio: a resposta começa com o aviso; sem arquivo e sem MCP: "estado indisponível"; fora do
     hub: nada. Evidência em evidencia-17/.
  2. Relatório etapas/relatorio-17-vigia-nas-telas.md (escolhas: barra sem MCP; .cmd desnecessário; dois canais no
     Codex; não verificados: toast do notify e statusLine na tela).
  3. Quando o 16 entrar em integracao: git merge integracao e um teste sobre o estado.json que o `vigia passada` grava.
  4. Testes do ticket e dos arquivos mexidos (a suíte inteira é do Rebite), Fiel, Rebite.
- Regras novas desta sessão: suíte inteira só na junção (Rebite); até um subagente por vez (tarefa fechada e leve) e até
  três Haiku 5.5 esforço médio só para tarefa simples ou QA; o Cinzel é o quarto construtor.
- Armadilha repetida: heredoc do Git Bash come `\` (virou `\` e quebrou JS duas vezes): para texto com barra invertida,
  usar o Write/Edit.

## Ticket 36, testes apagam a pasta de ensaio (2026-10-17 ~05h50)

- Maestro: pegar o 36 enquanto o real do 17 espera o Codex (06h58) e a fila; depois voltar ao real do 17 (passos em "PRÓXIMO ~06h00" acima). Não apagar pastas antigas em massa.
- Ramo ticket-36, worktree C:/context-hub-wt/ticket-36. 90f6463: ajudante agents/code/test/pasta-de-ensaio.mjs (pastaDeEnsaio, hubDeEnsaio; after + exit + prependListener uncaughtException) e 36-pasta-de-ensaio.test.mjs (6 casos, arquivos-modelo com TEMP isolado; tirar NODE_TEST_CONTEXT do filho).
- Sem commit ainda: troca nos testes 04, 05, 05n, 14, 15, 19, 20, 27-fim, 27-pastas, gerador (06). Verdes e sem sobra com TEMP isolado.
- Maestro: não trocar em arquivo que ramo aberto mexe (08: ensaio.psm1, kit-sem-docker.ps1; 10: mcp-banco-sem-docker.ps1, 09-mcp-banco.test.ps1; 15: ponta-a-ponta/15; 16, 17: testes novos). Anotado no relatório etapas/relatorio-36-pasta-de-ensaio.md.
- Falha forçada: etapas/logs/falha-forcada-36.sh (PATH só com o node: montar falha). TEMP isolado precisa de caminho curto ($TEMP/v36), senão o git falha com "Filename too long".
- b8e8b03: troca commitada; falha forçada nos dez sem sobra; contraprova na integracao (14 e 15 deixam pasta). Revisão pedida ao Fiel em b8e8b03; não mexer na worktree. Depois do passa: Rebite. Depois: real do 17.
- 06h15 (17): b168ac4 ponta a ponta real escrita (agents/code/test/ponta-a-ponta/17-vigia-tela.test.mjs: por harness, sessão 'divergencia' (resposta começa pelo aviso, cita reuniao; Codex: notify chama o dublê HUB_VIGIA_NOTIFICAR uma vez) e 'indisponivel' (sem estado.json e sem MCP)). 0e74227: o teste unitário do 17 dizia 'codex.json' e o detector do 29 o pegava como harness: fragmento('codex') sem extensão. 17-vigia-tela + 29: 21/21.
- Fila: 3b (real do 17, Claude e Copilot), entre fatias da Brasa: ela avisa 'trava livre, sua vez'; ao fim, devolver a ela com o mesmo aviso. Comando: cd C:/context-hub-wt/ticket-17 && HUB_HARNESS_REAL=1 HARNESSES=claude,copilot node --test --test-concurrency=1 agents/code/test/ponta-a-ponta/17-vigia-tela.test.mjs. Codex depois das 06h58 (HARNESSES=codex).
- 36: revisão pedida ao Fiel em b8e8b03 (não mexer na worktree ticket-36). Maestro pôs nas regras a linha do ajudante.
- 06h25 (17): real Claude+Copilot 4/4 (06:22-06:24, com a trava; devolvida à Brasa). Evidência c629ae5. Relatório etapas/relatorio-17-vigia-nas-telas.md escrito. Falta: Codex depois das 06:58 (fila; trava), merge do 16 quando entrar, Fiel, Rebite.
- 06h25 (36): rodada 1 do Fiel VOLTA (parecer-36-Vela.md): a limpeza em uncaughtException apagava as pastas no meio. Conserto (sem commit ainda): só limpa nesses eventos antes do primeiro teste (marca no beforeEach da raiz; o before da raiz roda até na queda do carregamento). 36-pasta-de-ensaio 8/8. 5b90550: 176/176 sem sobra; rodada 2 pedida ao Fiel. Não mexer na worktree.
- 06:28 (36): rodada 2 PASSA; Rebite avisado. 36 encerrado do meu lado. Próximo: Codex do 17 depois das 06:58 (fila/trava).
- 06:38: trava oferecida pelo Trilho; recusada (Codex só depois das 06:58), passada à Brasa. Pedir a vez de novo depois das 06:58.
- 07:02 (17): integracao 9cc878b juntada (5187a86, com o 36); o teste do 17 usa o ajudante comum (273579f), 15/15 sem sobra. Fila: depois do Trilho, só o Codex do 17; ao soltar, avisar o Cinzel.
- 07:28 (17): Codex 2/2 (86c5a88); trava solta, Cinzel avisado. Revisão pedida ao Fiel em 86c5a88; não mexer na worktree. Depois: merge do 16 quando entrar, teste sobre o estado.json real, rodada nova do Fiel, Rebite.

## Ticket 18, retomada: nota, início e fim (2026-10-17 ~07h40)

- Ramo ticket-18, worktree C:/context-hub-wt/ticket-18 (integracao 9cc878b + ticket-17 86c5a88). Junção só depois do 17 e do 16.
- Costuras em etapas/costuras-18-Vela.md (pergunta das várias sessões: A passagem em work/passagem-<terminal>.md, ou B nota única; fim no mesmo núcleo do 27; início no tela.mjs do 17; aviso da memória do Claude; Copilot sem a extensão onAgentStop). Esperando o maestro.
- 17 em revisão no Fiel (86c5a88): não mexer na worktree ticket-17.
- 07:37 (18): ca2bb45 (fim devolve sem a nota) e 511ad2a (passagem do recruta em work/, work_kind handoff); 18-retomada 5/5. Próximo: sete campos + next_step, last_agent, aviso da memória do Claude, início com a nota, AGENTS.md, ponta a ponta.
- 07:40 (17): rodada 1 VOLTA (estado sem passada); conserto 3e8bbc8, 16/16, mod 2/2; rodada 2 pedida ao Fiel. Não mexer na worktree ticket-17. 18 parado em b2ba08d (próximo: last_agent).
- 07:49 (17): rodada 2 PASSA (3e8bbc8); Rebite avisado (junção só depois do 16; depois do 16: merge, teste sobre estado real, rodada nova).

## PRÓXIMO (gravado 2026-10-17 ~08h40, antes do /clear pedido pelo maestro, contexto 43%)

- Encerrados nesta sessão: 36 (juntado e resolvido, integracao 9cc878b). 17: rodada 2 do Fiel PASSA em 3e8bbc8; Rebite
  avisado; **junção só depois do 16**. Quando o 16 entrar em integracao: no ramo ticket-17, `git merge integracao`, teste
  sobre o estado.json que o `vigia passada` grava (no lugar do exemplo fixo; ver também a ressalva 1 do parecer:
  `outro_par.situacao = nao-verificavel` perde o motivo), rodada nova do Fiel, então o Rebite junta.
- **Ticket atual: 18, retomada** (issues/18-retomada-nota-inicio-e-fim.md, claimed). Ramo ticket-18, worktree
  C:/context-hub-wt/ticket-18 (integracao 9cc878b + ticket-17 até 3e8bbc8, merge 5dedcc1). Junção só depois do 17 e do 16.
- Decidido pelo maestro (07h40): **opção A** (registrada no 18 como mudança do spec para rever com o Gustavo) e as
  costuras de etapas/costuras-18-Vela.md.
- Feito (commits; `node --test agents/code/test/18-retomada.test.mjs` 8/8; com o 27, 24/24):
  - ca2bb45: agents/code/hooks/retomada/nota.mjs (iniciativaDe, recruta, notaDe, conferirRetomada) ligado no
    fim-da-resposta/nucleo.mjs: o turno que gravou numa iniciativa (fora das notas) sem mudar a nota é devolvido (mesma
    conta de 3 do 27).
  - 511ad2a: recruta (MAESTRI_TERMINAL_ID sem HUB_PAPEL=maestro) → passagem `<ini>/work/passagem-<terminal>.md`
    (frontmatter work_kind: handoff, stage: open, agent: <terminal>; a devolução diz isso).
  - b2ba08d: nota que mudou sem um dos sete rótulos (`- **Rótulo:**`) é falta; o next_step o verificador já cobra.
  - c603970: last_agent na retomada.md de quem conduz ("<claude-code|codex|copilot> <modelo>"); modelo: evento.model
    (Codex, doc "Common input fields"), transcript (Claude, modeloDaSessao do acervo/decidir.mjs), Copilot sem modelo.
    fim(hub, sessao, env, quem) agora recebe quem = { harness, modelo, memoria }.
  - b291ca2: memória do Claude (`<CLAUDE_CONFIG_DIR|~/.claude>/projects/<cwd com - no lugar de [^A-Za-z0-9-]>/memory/`)
    que mudou no turno vira aviso único (cabeçalho "Antes de terminar:"), sem gastar devolução.
- **Falta (próximo passo exato):**
  1. Início: no `tela.mjs inicio` (do 17), depois do estado da vigia, a nota da iniciativa onde a sessão abre (subir da
     pasta; `iniciativaDe` do nota.mjs), mais a passagem do recruta, se houver; na raiz ou fora de iniciativa: "nenhuma
     nota aberta; ache o trabalho pela busca, pelo nome que o Gustavo der, ou pergunte"; corte em ~4.000 caracteres com
     o caminho. Teste antes em 18-retomada.test.mjs (com e sem vigia, na raiz, fora do hub, recruta).
  2. AGENTS.md: uma linha na cabeça (hoje 1.695 de 2.000; o verificar-hub mede) e uma seção curta (sete campos, fato e
     hipótese, passagem do recruta, banco fora: troca de trecho e pendência em "Perguntas abertas"). Ver se o
     04-esqueleto/verificar-hub continuam verdes.
  3. Ponta a ponta real agents/code/test/ponta-a-ponta/18-retomada.test.mjs (molde do 17/27; fragmentos do fim do 27
     e do início do 17 no HOME de ensaio; Claude com --plugin-dir do mod fim-da-resposta): sessão 1 numa iniciativa
     (criar nota em research/) → devolve → atualiza a nota (sete campos) → solta; sessão 2 na mesma pasta responde o
     próximo passo pela nota. Pela fila/trava (etapas/fila-pesada.md), harness real só quando a máquina não estiver
     quieta para a Brasa.
  4. Relatório etapas/relatorio-18-retomada.md (escolhas, opção A, Copilot só agentStop, memória só do Claude, fora:
     banco fora, cliente, trabalho fora de iniciativa), Fiel, Rebite.
- Armadilhas desta sessão: o Edit exige ler o arquivo antes (perdi três edições assim); heredoc com 'EOF' preserva
  as barras, mas `\.` em template literal dentro de RegExp vira `\.`; TEMP isolado precisa de caminho curto ($TEMP/v36)
  senão o git dá "Filename too long"; o detector do 29 pega 'codex.json' como codex\.js (usar nome sem extensão).
- 07:58 (18): 8950ed7 início com a nota (nota.mjs retomadaDoInicio; tela.mjs inicio junta depois do estado; corte 4.000; recruta vê a passagem ou onde gravá-la). 18-retomada + 17-vigia-tela 31/31 (teste do ok do 17 olha só o primeiro bloco). Próximo: AGENTS.md (passo 2).
- 08:05 (18): AGENTS.md (linha na cabeça, 1.869/2.000; seção Retomada) commitado. Próximo: ponta a ponta real (passo 3), pela fila/trava.
- 08:10 (18): 68bf70b ponta a ponta real escrita (ponta-a-ponta/18-retomada.test.mjs; sessão 1 em clients/aurora/migracao-de-tenant cria research/ensaio-18.md, fim devolve, nota atualizada, solta, last_agent; sessão 2 sem ferramentas responde ZEBRA-42 pela nota do início). Pedido lugar na fila ao maestro. Codex sem cota até 12:15. Próximo: relatório etapas/relatorio-18-retomada.md.
- 08:15 (18): relatório escrito; ticket comentado. Esperando a Brasa avisar a vez (item 2b da fila): HUB_HARNESS_REAL=1 HARNESSES=claude,copilot node --test --test-concurrency=1 agents/code/test/ponta-a-ponta/18-retomada.test.mjs (com trava). Codex depois das 12h15 com o Cinzel.
- 08:28 (18): trava pega; real Claude+Copilot rodando (log etapas/logs/18-real-1.log). Ao soltar: avisar o Rebite (ordem do maestro).
- 08:35 (18): real Claude+Copilot 2/2; evidência b840812; trava solta, Rebite avisado. Revisão pedida ao Fiel em b840812; NÃO mexer na worktree ticket-18. integracao em e98a891 (08): juntar depois. Codex depois das 12h15 (commit só de evidência + rodada curta).
- 08:40: maestro: preparar o 25 (junção e prova do hub de ensaio inteiro): costuras e roteiro por fases, medir o pico de memória; nada pesado sem a fila; costuras antes de codar.
- 08:55 (25): costuras em etapas/costuras-25-Vela.md (fases 1 busca, 2 pares+gravar+recusa+B recebe+cifra, 3 banco reiniciado, 4 vigia, 5 retomada, 6 arquivar, 7 cliente; medidor 2 s com corte em 700 MB; ponte pares.ps1; orquestrador 25-hub-inteiro.test.mjs; corredor destacado). Perguntas ao maestro: wsl --shutdown no corredor; mem_limit 384 MB por override de ensaio; busca em fase separada; ordem do preparo. Esperando antes de codar.
- 08:35 (18): real Claude+Copilot 2/2; evidência b840812; trava solta, Rebite avisado. Revisão pedida ao Fiel em b840812; NÃO mexer na worktree ticket-18. integracao em e98a891 (08, suíte do Rebite em curso): juntar depois. Codex depois das 12h15 (commit só de evidência + rodada curta).
- 09:00 (25): maestro aceitou as quatro ((1) wsl --shutdown só com a trava e docker ps vazio; (2) override só do ensaio, se o CouchDB cair por ele o relatório diz; (3) busca em fase separada; (4) agora só o leve). Ideia do mem_limit passada à Brasa. Próximo: worktree ticket-25 da ponta de integracao; tdd: ponte pares.ps1, medidor.ps1, módulo comum harnesses.mjs, testes sem Docker.
- 09:02 (18): rodada 1 do Fiel VOLTA (parecer-18-Vela.md): o fim cobra a nota de quem não gravou (mudados() pega todo arquivo com mtime depois da marca). Conserto: só o que esta sessão gravou (caminhos dos eventos de ferramenta da sessão, no arquivo da sessão); teste com duas sessões. Raiz do 27, no núcleo. Antes do 25.
- 09:30 (18): conserto da rodada 1 em e1c5eac (anota no PostToolUse; fim só pela lista da sessão; resolve o 27; research/retomada.md não é nota). 18+27+17+19 69/69. Rodada 2 pedida ao Fiel; real Claude+Copilot de novo pela fila (pedido ao maestro); Codex depois das 12h15. NÃO mexer na worktree ticket-18. Depois: voltar ao preparo do 25 (aceito: worktree ticket-25; ponte, medidor, testes sem Docker).
- 09:35: fila: eu depois do Cinzel (item 2b, real do 18 de novo, HARNESSES=claude,copilot); ao soltar, avisar a Brasa. 25: worktree C:/context-hub-wt/ticket-25 (e98a891), Status claimed. Começando o medidor (agents/code/test/ponta-a-ponta/25/medidor.ps1) com teste sem Docker.
- 09:50 (25): f? medidor commitado (agents/code/test/ponta-a-ponta/25/medidor.ps1 + agents/code/test/25-medidor.test.mjs 4/4). Próximo: ponte pares.ps1 (ensaio.psm1: -Subir/-Descer/-ReiniciarA/-Amostra, estado JSON) com teste sem Docker pelo cli-falso.
- 10:00 (25): ponte agents/code/test/ponta-a-ponta/25/pares.ps1 commitada (teste 25-pares-sem-docker 1/1; os passos com Docker só na prova). integracao e98a891 firme (08 e 15 resolvidos); 18 junta integracao depois da rodada 2 do Fiel. Próximo do 25: orquestrador 25-hub-inteiro.test.mjs (fases 1 e 2 sobre integracao) + módulo comum ponta-a-ponta/harnesses.mjs.
- 10:25 (18): rodada 2 PASSA com ressalvas (e1c5eac); 2 e 3 consertadas em f36df85 (anotar por append + sessão atômica; NotebookEdit); 114/0/8. Rodada curta de código pedida ao Fiel. Ressalva 1 (shell fora da lista) ao maestro. Depois do passa: real Claude+Copilot pela fila (depois do Cinzel; ao soltar avisar a Brasa), commit só de evidência; Codex depois das 12h15. Junção depois do 17 e do 16.
- 10:25 (25): 1c30e48 orquestrador (ponta-a-ponta/25-hub-inteiro.test.mjs, fases 1-3; 4-7 todo) + harnesses.mjs. Falta no preparo: relatório do 25 com o roteiro, corredor destacado (wsl --shutdown, trava), e a primeira rodada real pela fila quando o maestro disser.
- 10:40 (25): corredor 974d74d; relatório etapas/relatorio-25-hub-inteiro.md. Preparo leve pronto. Próximo: rodada real das fases 1-3 pelo corredor, quando o maestro der a vez (Start-Process pwsh -WindowStyle Hidden -ArgumentList '-NoProfile','-File','C:/context-hub-wt/ticket-25/agents/code/test/ponta-a-ponta/25/corredor.ps1','-Fases','1,2,3','-Harnesses','claude,copilot'). 18: esperando a rodada curta do Fiel (f36df85); depois real Claude+Copilot (fila: depois do Cinzel; avisar a Brasa).
- 10:50 (25): fila: 1ª rodada real do 25 depois do Docker do 22 da Brasa (item 3b); a Brasa avisa. Ao fim: mandar ao maestro a tabela de pico por fase (evidencia-25/resumo.md).
- 11:00 (18): rodada curta PASSA em f36df85 (Fiel). Rebite avisado: junção só depois do 17 e do 16; faltam a repetição real Claude+Copilot (fila, depois do Cinzel) e o Codex depois das 12h15, em commits só de evidência com rodada curta.
- 09:13 (relógio): CORREÇÃO: as linhas acima marcadas 09:02 a 11:00 tinham horas estimadas por mim, adiantadas; tudo aquilo aconteceu entre ~08:40 e 09:13. 09:13: trava pega pelo aval do Cinzel; real do 18 de novo (Claude+Copilot) rodando, log etapas/logs/18-real-2.log. Ao fim: avisar a Brasa.
- 09:16 (18): real de novo 2/2 (09:14-09:16), evidência 31afe63; trava solta, Brasa avisada. Pedida rodada curta de evidência ao Fiel. Falta: Codex depois das 12h15.

## PRÓXIMO (gravado 2026-10-17 09:20, antes do /clear pedido pelo maestro, contexto 44%)

### Ticket 18 (retomada): passa; esperando evidência e junção
- Ramo ticket-18, worktree C:/context-hub-wt/ticket-18 (integracao 9cc878b + ticket-17 3e8bbc8; NÃO juntei a integracao
  e98a891 ainda). HEAD 31afe63 (evidência). Código: f36df85.
- Rodadas do Fiel: 1 volta (o fim cobrava a nota de quem não gravou; raiz no núcleo do 27), 2 passa com ressalvas, curta
  (f36df85) passa. Rebite avisado: junção só depois do 17 e do 16. Ressalva 1 (gravação por shell fora da lista) aceita
  pelo maestro; virou o ticket 37.
- Conserto no núcleo (vale para o 27): `fim-da-resposta.mjs <h> anota` no PostToolUse (Claude: fragmentos/claude.json
  no settings, matcher Write|Edit|MultiEdit|NotebookEdit; Codex PostToolUse apply_patch; Copilot postToolUse
  create|edit|apply_patch). Caminhos pelos ADAPTADORES da guarda do 14 (import dinâmico). Lista em
  `<hub>/.local/fim-da-resposta/<sessão>.gravados` (appendFileSync, uma linha por caminho); sessão .json por troca
  atômica; marca de turno novo apaga a lista. Ajudante de teste agents/code/test/gravacao.mjs.
- Esperando: rodada curta de EVIDÊNCIA do Fiel em 31afe63 (pedida 09:17).
- Falta: **Codex real depois das 12h15** (fila; junto com o do Cinzel): `cd C:/context-hub-wt/ticket-18 &&
  HUB_HARNESS_REAL=1 HARNESSES=codex node --test --test-concurrency=1 agents/code/test/ponta-a-ponta/18-retomada.test.mjs`
  com a trava; primeiro uso real do PostToolUse do apply_patch (se não disparar, o fim não devolve: investigar).
  Commit só de evidência, relatório (seção Prova real), rodada curta do Fiel, avisar Rebite. Quando o 16 entrar:
  `git merge integracao` no ramo (e o 17 antes).
- Testes: `node --test agents/code/test/18-retomada.test.mjs agents/code/test/27-fim-da-resposta.test.mjs
  agents/code/test/17-vigia-tela.test.mjs agents/code/test/19-roteamento.test.mjs agents/code/test/14-guardas.test.mjs`
  (com as provas puladas e harness-real: 114 passam, 8 pulados).

### Ticket 25 (junção e prova do hub inteiro): preparo leve pronto
- Ramo ticket-25, worktree C:/context-hub-wt/ticket-25 (de integracao e98a891). Status claimed. HEAD 974d74d.
- Costuras aceitas: etapas/costuras-25-Vela.md (as quatro: wsl --shutdown pelo corredor só com trava e docker ps vazio;
  limite de memória só no ensaio, saiu por `docker update --memory 384m --memory-swap 384m` igual à Brasa no 22; busca
  em fase separada; agora só o leve). Relatório etapas/relatorio-25-hub-inteiro.md.
- Peças: ponta-a-ponta/25/medidor.ps1 (teste 25-medidor 4/4), 25/pares.ps1 (teste 25-pares-sem-docker 1/1),
  ponta-a-ponta/harnesses.mjs (comum), ponta-a-ponta/25-hub-inteiro.test.mjs (fases 1 busca, 2 pares com guarda +
  recebe + claro, 3 banco reiniciado; 4-7 todo), 25/corredor.ps1.
- **Próximo:** a 1ª rodada real entra depois do Docker do 22 da Brasa (fila item 3b); a Brasa avisa. Lançar:
  `Start-Process pwsh -WindowStyle Hidden -ArgumentList '-NoProfile','-File','C:/context-hub-wt/ticket-25/agents/code/test/ponta-a-ponta/25/corredor.ps1','-Fases','1,2,3','-Harnesses','claude,copilot'`
  (o corredor cria e apaga a trava; status em etapas/logs/25-corredor.status, prova em 25-prova.log). Ao fim: mandar
  ao maestro a tabela de pico por fase (agents/code/test/ponta-a-ponta/evidencia-25/resumo.md), avisar o próximo da
  fila, consertar o que os passos com Docker da ponte pedirem (primeiro uso), preencher "Fica para a instalação" no
  relatório.
- Ainda fora (ressalva do 11): write_note pelos harnesses (registro do hub-banco vem com 11/23) e o MCP reconectando.

### Armadilhas desta sessão
- **Hora:** olhar `date` antes de escrever hora em retomada/ticket (escrevi horas estimadas e adiantadas; corrigido).
- CRLF: troca por `node -e` não casa em arquivo CRLF (o 27 ponta a ponta); usar o Edit (ler antes).
- `maestri ask` demora quando o outro responde direto: mandar em segundo plano.
- 09:21 (18): rodada curta de evidência PASSA em 31afe63 (Fiel). Resta só o Codex depois das 12h15 (commit de evidência + rodada curta + aviso ao Rebite).
- 09:33 (25): maestro: janela quieta depois do 21 do Trilho; a Brasa roda o 22 e a fatia 2 do 08; depois eu rodo a 1ª rodada real do 25 (corredor, fases 1-3). Só eu e a Brasa ficam. Esperar o aviso do maestro. 37 (Cinzel): respondi sobre o núcleo (nota pelo shell conta como mudada; aviso em 'Antes de terminar:'; avisados é por turno; falso positivo do sincronizador).
- 09:39 (25): janela aberta. Brasa: 22 e fatia 2 do 08; depois eu. Não mandar mensagem a Rebite, Fiel, Trilho, Cinzel, Fielzinho. Ao fim: tabela de pico por fase ao maestro.
- 09:53 (25): Brasa passou a vez; corredor lançado PID 250324 (fases 1-3, claude+copilot). Status logs/25-corredor.status, prova logs/25-prova.log.
- 09:58 (25): rodada 1 (fases 1-3): fase 1 e 3 passam; fase 2 falhou no Copilot por defeito do teste (o Claude já tinha trocado a linha de tasks.md; o pedido citava o texto antigo). Memória folgada (livre mínimo 1831 MB, na busca). Log e resumo guardados em logs/25-prova-rodada-1.log e logs/25-resumo-rodada-1.md. Conserto 627f1a8. Rodada 2 (fases 2,3) lançada PID 251604.
- 10:02 (25): rodada 2 verde (fases 2,3). Evidência fc678b0; relatório com tabela; ticket comentado. Tabela ao maestro. Próximo: Codex (18 e 25) depois das 12h15 pela fila.

## PRÓXIMO (gravado 2026-10-17 ~10h10, antes do reinício do Maestri)

- **25**: 1ª rodada real verde nas fases 1-3 com Claude e Copilot (rodada 1 09:53: busca e banco reiniciado passam,
  pares caiu por defeito do teste, conserto 627f1a8; rodada 2 09:58: fases 2-3 2/2). Evidência fc678b0 no ramo ticket-25
  (worktree C:/context-hub-wt/ticket-25, HEAD fc678b0). Relatório etapas/relatorio-25-hub-inteiro.md com a tabela de
  pico (já mandada ao maestro). Ticket comentado.
  - Falta: **Codex depois das 12h15** pela fila: Start-Process pwsh -WindowStyle Hidden -ArgumentList '-NoProfile',
    '-File','C:/context-hub-wt/ticket-25/agents/code/test/ponta-a-ponta/25/corredor.ps1','-Fases','1,2,3',
    '-Harnesses','codex' (atenção: a evidência-25 é sobrescrita; copiar resumo/hashes antes, como fiz com
    resumo-rodada-1.md). Fases 4-7 quando 16/17, 18, 21, 22/24 entrarem.
- **18**: tudo passa; falta só o **Codex depois das 12h15** (comando na seção "PRÓXIMO 09:20"), commit só de evidência,
  rodada curta do Fiel, avisar o Rebite.
- **17**: passa; junta depois do 16 (merge integracao no ticket-17, teste sobre o estado.json real, rodada nova do Fiel).
- **37 (Cinzel)**: respondi as costuras do núcleo (nota/passagem pelo shell conta como mudada no conferirRetomada;
  aviso em "Antes de terminar:"; avisados é por turno; falso positivo do sincronizador). Nada meu a fazer.
- Ordem do Codex às 12h15 (fila item 5): Cinzel (11, depois 24) e eu (18, depois 25), um de cada vez; conferir a fila.
- 10:11: Maestri reiniciado; contexto mantido. Nada novo em integracao (e98a891; 16, 17, 18, 21, 22, 24 claimed). Fases 4-7 esperam as junções. 12h15: Codex do 18 e do 25 pela fila (o 25 ainda não está na fila: pedido ao maestro).
- 10:19: regra nova do maestro: no Codex de verdade, o gpt-6-astra está liberado à vontade (ver regras). Em curso: fases 4-7 do 25 contra 16/17/18/21/22 (só leitura); 16 juntado em integracao fce0529 (ainda não resolvido). Ponte pares.ps1 ganhou conflito com base, manutencao, vigia, estado-mcp, copia (sem commit).
- 10:27 (25): 851dcdc: fases 4-7 escritas (puladas até as peças entrarem); ponte com conflito/manutencao/vigia/estado-mcp/copia; 25/cliente.ps1 (pilha do 22); 25-pares-sem-docker 2/2. Relatório atualizado. Próximo: rodada real delas quando 16+17, 18, 21, 22 entrarem (merge integracao no ticket-25); 12h15 Codex do 18 e do 25.
