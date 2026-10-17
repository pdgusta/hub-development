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

- 03 (prova dos hooks do Codex em acesso total), 02 (prova das pastas com ponto fora do LiveSync), 06 (gerador de exclusões, `agents/code/bin/gerar-exclusoes.mjs`).

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

### Próximo passo exato

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
