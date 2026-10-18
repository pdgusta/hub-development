# Parecer do ticket 25 (Vela), 2ª leitura independente, revisão parcial

Subagente do Fiel, 2026-10-17 ~19h. Commit revisado: `5489b3a` (ramo `ticket-25`, contém `integracao` f640bbd), em
worktree destacada minha (`%TEMP%/hub-ensaio-25-seg`, removida no fim). Escopo: fases 1-3, 5, 6 e 7 com Claude e
Copilot; Codex nas fases 1 e 3. Fora: fase 4 e fase 2 do Codex. Não li o parecer do Fiel.

## Veredito: VOLTA

A fase 7 está registrada como verde, mas nenhum harness rodou nela. Além disso, a evidência versionada da manhã foi
sobrescrita por uma rodada que falhou. As fases 1, 2, 3, 5 e 6 (Claude e Copilot) e a fase 1 do Codex estão provadas
pela evidência.

## O que rodei

- Testes leves, com `TEMP`/`TMP` no caminho longo e sem `HUB_HARNESS_REAL`:
  `node --test agents/code/test/harness-real.test.mjs agents/code/test/25-*.test.mjs agents/code/test/ponta-a-ponta/25-hub-inteiro.test.mjs agents/code/test/27-pastas.test.mjs`
  saiu com **42 testes: 41 pass, 0 fail, 1 skip** (a prova real). Bate com o relatório.
- `git merge-tree --write-tree 5489b3a integracao` (ponta atual: 56cd23a, com 22 e 24 juntados): **sem conflito**.
  Nenhum arquivo em comum fora de `evidencia-25/`, `25/` e `harnesses.mjs`.
- Busca de tokens (`ghu_|sk-|refresh_token|access_token|Bearer|eyJ`) em `evidencia-25/` e em `etapas/logs/25-*`:
  **nada**. "Gustavo" aparece só na descrição da `SKILL.md` do arquivar, lida pelo agente. A pasta do usuário virou
  `%USERPROFILE%`/`USUARIO`.
- Uma reprodução mínima do conserto 1, no scratchpad, sem harness e sem Docker (ver abaixo).

## Consertos

1. **Fase 7 em falso verde: o ponta a ponta do 22 não rodou.**
   - `25-hub-inteiro.test.mjs:493-496`: o filho é `node --test ... 22-cliente.test.mjs` com
     `env: { ...process.env, ... }`. Como roda dentro de um `node --test`, ele herda `NODE_TEST_CONTEXT=child-v8`. O
     node então pula os arquivos, sai com 0 e não escreve nada no stdout.
   - Evidência: `evidencia-25/cliente/harnesses/prova.tap` tem **0 bytes** (cee35c1). O `erros.txt` diz:
     `Warning: node:test run() is being called recursively within a test file. skipping running files.`
   - `etapas/logs/25-noite-f7-resumo.md`: só tem as linhas `cliente:subir` (6:32) e `descer`. **Não há linha
     `cliente`**, ou seja, a fase dos harnesses durou menos que uma amostra de 2 s. No log
     `25-prova-noite-f7-b.log`, a fase 7 leva 394.717 ms, quase todos na subida.
   - `etapas/logs/25-noite-f7-hashes-claude-copilot.json`: `"usos": []`. Nenhum login foi copiado, logo nenhum harness
     abriu.
   - Reprodução (node v24.19.0): um `pai.test.mjs` roda por `spawnSync(process.execPath, ['--test', filho])` um filho
     que sempre falha. Saída: `NODE_TEST_CONTEXT= child-v8 status= 0 stdout bytes= 0 stderr= ... skipping running files.`
   - Conserto: tirar `NODE_TEST_CONTEXT` do `env` do filho. Conferir no TAP que há um `ok` por harness pedido e nenhum
     `SKIP`, porque status 0 com TAP vazio tem de falhar. Depois rodar a fase 7 de novo. A tabela da noite e o comentário
     de 18:24 no ticket dizem "fase 7 verde" e precisam ser corrigidos. O livre mínimo de 939 MB vale só para a
     subida da pilha.

2. **A evidência versionada da manhã foi sobrescrita pela rodada que falhou às 18:13.**
   - O commit de código `f5b790b` levou junto `evidencia-25/hashes-claude-copilot.json`, `medida.csv` e `resumo.md`.
     Em 5489b3a, esses arquivos são da fase 7: `medida.csv` tem 1 amostra (`cliente:subir`, 21:13Z),
     `resumo.md` é `cliente:subir 3931 ... 0:00` e o arquivo de hashes tem `"usos": []`.
   - O relatório ("Primeira rodada real") aponta esses arquivos como a prova do pico das fases 1-3 e das horas de login.
     Na árvore, isso já não existe. As cópias certas estão só em `etapas/logs/25-hashes-fases-1-3.json` e
     `25-medida-fases-1-3.csv`.
   - A causa está no código: `25-hub-inteiro.test.mjs:506-511` grava `medida.csv`, `resumo.md`, `corte.json` e
     `hashes-<harnesses>.json` com o mesmo nome a cada rodada. Por isso uma rodada de uma fase só apaga a de outra.
   - Conserto: nomear por rodada ou fase (por exemplo `medida-<fases>-<harnesses>.csv`) e repor a evidência da manhã.
     Versionar também os hashes e `usos` das rodadas que valem: fase 5 (17:22), fase 7 refeita e Codex 18:00
     (`logs/25-codex-luna/hashes-codex.json` não está em `evidencia-25/`).

3. **A fase 7 consertada vai sobrescrever a evidência do ticket 22 ao juntar.**
   - O `22-cliente.test.mjs:25,43,182` grava em `evidencia-22/<harness>/` e em `evidencia-22/hashes-<harnesses>.json`.
     Antes ele apaga as pastas dos harnesses pedidos.
   - Com o conserto 1, cada rodada do 25 troca a evidência já juntada do 22. A `integracao` 56cd23a acabou de receber a
     do Codex: `evidencia-22/codex/*`, `hashes-codex.json`.
   - Conserto: uma variável de pasta de evidência no 22, ou outra forma de mandar a saída do filho para
     `evidencia-25/cliente/`. Como o arquivo é do 22, o caminho deve ser combinado com o maestro.

## Ressalvas (não seguram sozinhas)

- **"Codex fase 3 verde" não diz nada do Codex.** A fase 3 (`:283-294`) não abre harness: reinicia o CouchDB, grava pelo
  disco e confere o B. Nos `usos` de `logs/25-codex-luna/hashes-codex.json` só aparecem `busca` e `pares`. A tabela da
  noite devia dizer "sem harness". O que as costuras pediam (turno 2 gravando pelo MCP sem religar) segue fora, como o
  próprio relatório admite ("O que falta").
- **Modelo do Codex.** O código está certo: `harnesses.mjs:59` usa `MODELO_CODEX`, e o detector "nenhum teste escreve o
  modelo do Codex à mão" passa. Mas a evidência da fase 1 do Codex não prova que a rodada das 18:00 foi no Luna. O
  corredor herda o ambiente de quem o lança, e a rodada das 18:06 usou `HUB_MODELO_CODEX` para o Sol. Sugiro gravar o
  `MODELO_CODEX` efetivo nos `usos`.
- **Fase 2:** o `recebeu` confere no B só o `tasks.md`, não a linha nova do `decisions.md`. A guarda e o B estão
  provados (recusa + 2 passa por harness, hashes A=B, `em_claro: []` em 189 amostras).
- **Fases 5 e 6 sem `usos` versionado.** O registro de login da fase 5 se perdeu (restauração do git antes da leitura, o
  relatório admite). O da fase 6 se perdeu no corte. As credenciais têm o mesmo hash antes e depois em todas as rodadas
  conferidas (`.credentials.json` dfff91dc, `auth.json` 9e42496b). A troca f4ad7edb→dfff91dc foi entre as rodadas, não
  dentro de uma. Só `.claude.json` muda, o que é esperado.
- **Linha 65:** `FASES=1 HARNESSES=codex` apaga `evidencia-25/busca/` inteira, inclusive Claude e Copilot. Hoje dá
  certo porque elas voltam do git à mão. É frágil: o melhor é apagar só `<fase>/<harness>`.
- **`25/cliente.ps1:29`:** o log `%TEMP%/hub-ensaio-25-subir-22.log` não é apagado no `descer` (hoje não existe no
  TEMP).
- **Defasagem de código.** As fases 1-3 rodaram com o código da manhã e a 6 em 87634db. De lá até 5489b3a, a skill do
  arquivar, a cópia diária e os hooks das fases 5 e 6 não mudaram (só `bin/lib/pastas.mjs`, do 44). A evidência segue
  valendo para o código revisado.

## O que confere por fase

| Fase | Harness | Provado pela evidência |
|---|---|---|
| 1 busca | Claude, Copilot, Codex | Sim. `mcp__hub-busca__search` / `hub-busca-search` / `mcp_tool_call server hub-busca` com a query; resposta `inbox/viveiro-na-cobertura.md` nos três |
| 2 pares | Claude, Copilot | Sim. `guarda.jsonl` com recusa no `decisions.md` e depois passa; `tasks.md` com hash A=B; nada em claro |
| 3 banco reiniciado | (sem harness) | Sim, o sincronizador: hash A=B de `inbox/depois-do-reinicio.md` |
| 5 retomada | Claude, Copilot | Sim. `devolveu: true`, depois `soltou: "sem falta"`; a sessão 2 sem nenhuma chamada de ferramenta responde "ZEBRA-25" |
| 6 arquivar | Claude, Copilot | Sim. `arquivar.mjs` chamado pelo agente; `_archive/2026-10-17--encerrada-*` com hash A=B; a cópia diária sai 0 e chega a `par/ensaio-a` |
| 7 cliente | Claude, Copilot | **Não.** A pilha subiu, mas o ponta a ponta do 22 foi pulado (conserto 1) |

## Rodada 2 (4628138)

Subagente do Fiel, 2026-10-17 ~20h. Worktree destacada minha de `4628138` (`%TEMP%/hub-ensaio-25-seg2`, removida no
fim). Contém a `integracao` 56cd23a. Não li a rodada 2 do Fiel. Sem harness de verdade, sem Docker.

### Veredito: PASSA

Os dois consertos da rodada 1 foram feitos e têm teste. A evidência nova prova o que o relatório diz para a fase 7, a
fase 2 do Codex, a fase 4 e a convergência. Os dois critérios do ticket estão cumpridos no escopo que o maestro decidiu
(o Codex nas fases 4-7 fica fora). Nenhum conserto segura. Há ressalvas, uma delas para o relatório antes de juntar.

### O que rodei

- Testes leves com `TEMP`/`TMP` no caminho longo e sem `HUB_HARNESS_REAL` (os quatro grupos do brief): **44 testes,
  43 pass, 0 fail, 1 skip** (a prova real). São 2 a mais que na rodada 1: o dublê do cliente e o `convergiu`. O 25-medidor
  passou nesta rodada. Depois dos testes, `git status` limpo.
- Sonda no scratchpad (apagada): `prova-do-cliente.mjs` com e sem a linha `delete filho.NODE_TEST_CONTEXT`, aberto de
  dentro de um `node --test`. Sem a linha: `["# pass NaN, esperado 2","# skipped NaN, esperado 0"]`, ou seja, vermelho.
  Com a linha: `[]`. O conserto é o que faz o teste passar.
- `git diff integracao 4628138 -- evidencia-22 evidencia-24`: **vazio**. `git merge-tree --write-tree 4628138
  integracao`: **sem conflito**. Fora de `evidencia-25/`, `25/` e `25-*`, só difere `harnesses.mjs`, um arquivo novo do
  25 que a `integracao` não tem.
- Busca de tokens (`ghu_|sk-|refresh_token|access_token|Bearer|eyJ`) em `evidencia-25/` e em `etapas/logs/25-*`:
  **nada**. "Gustavo" aparece só no texto do hook da retomada ("pelo nome que o Gustavo der"), que é texto do hub.

### Os consertos da rodada 1

1. **Fase 7 sem harness: feito** (dac76e6). `25/prova-do-cliente.mjs` tira o `NODE_TEST_CONTEXT` do ambiente e só aceita
   saída 0, `# pass` igual ao número de harnesses e `# skipped 0`. O teste com dublê cobre o filho certo, o que pula e o
   que cai.
   - Na evidência (b78c49d), `cliente/harnesses/prova.tap` traz `ok 1 - claude: busca pelo proxy...`, `ok 2 - copilot:
     ...`, `# pass 2`, `# skipped 0` e `erros.txt` vazio. A fase `cliente` aparece no `resumo.md` da rodada
     `1921-claude-copilot-f7` (0:34, livre mínimo 835 MB).
   - `hashes-do-22-cliente.json`: os dois `usos` com `apagado: true`. Credenciais e `.claude.json` iguais antes e
     depois.
2. **Evidência sobrescrita: feito** (f6a0f21). Cada rodada grava em `rodadas/<data-hora>-<harnesses>-f<fases>/`
   (`medida.csv`, `resumo.md`, `corte.json`, `hashes.json`). A rodada apaga só `<fase>/<harness>` dos harnesses dela, o
   que também resolve a ressalva da linha 65. Saíram da raiz os arquivos de 18:15. Foram repostas a manhã (igual a
   `etapas/logs/25-resumo-fases-1-3-claude-copilot.md`) e o `hashes.json` do Codex das 18:00.

### A evidência nova confere com o relatório

- **Convergência** (`subida-dos-pares/pares/subir.json`): `convergiu: true`, 530 arquivos, `faltam: 0`, `diferentes: 0`,
  218 s. O `subir` lança erro se não convergir em 15 min. O teste sem Docker cobre o B vazio, a cópia certa (sem os
  arquivos com ponto e sem a pasta local) e um hash diferente.
- **Fase 2, Codex** (`pares/codex/`):
  - `guarda.jsonl` tem `recusa` no `decisions.md`, que o Codex tentou regravar com `*** Add File`. Depois vêm dois
    `passa` no `decisions.md` e um no `tasks.md`.
  - `recebeu.json`: `recebeu: true` e `hash_a` igual a `hash_b` (14FBB901...).
  - `em-claro.json`: `em_claro: []` em 274 amostras.
  - O `uso` traz `modelo: "gpt-6-luna"`.
- **Fase 4, Claude e Copilot** (`vigia/`):
  - `conflito.json` tem `conflito: true`. Na `passada.json`, o nível é `divergencia`, o item tem o caminho
    `inbox/conflito-do-25.md` em claro e a notificação cita esse caminho.
  - `estado-do-hub.json` conta o mesmo conflito.
  - As duas respostas começam pelo aviso: "Vigia do hub: divergência: conflito aberto em `inbox/conflito-do-25.md`..." e
    "**Aviso:** o conflito aberto em `inbox/conflito-do-25.md`...".
- **Hashes** (rodadas 1921 e 1926): `.claude/.credentials.json` dfff91dc e `.codex/auth.json` 9e42496b iguais antes e
  depois. Só o `.claude.json` muda. Todos os `usos` estão com `apagado: true`. Na 1921, os `usos` do 25 estão vazios,
  como esperado: quem copia o login é o 22.

### Ressalvas (não seguram)

1. **"Fica para a instalação" desatualizado.** O relatório ainda diz "(Fases 4-7 a medir quando entrarem.)" e não traz
   o número mais apertado já medido: na fase 7, com a máquina quieta, o livre mínimo foi 835 MB (subida 887 MB). Isso
   fica só 135 MB acima do corte de 700 MB. A fase 2+4 ficou em 1.690 MB. Para a máquina do Gustavo com mais agentes
   abertos, a fase 7 é a candidata a cair. Corrigir o parágrafo antes do Rebite juntar (é só texto).
2. **Nome da rodada da manhã.** A pasta `rodadas/2026-10-17-1248-claude-copilot-f1-2-3/` guarda a rodada 2 da manhã
   (amostras das 12:59), que só tem as fases `pares` e `banco-reiniciado`, e os `usos` só da fase `pares`. A busca e o
   pico de 1.831 MB estão em `evidencia-25/resumo-rodada-1.md`. O nome promete f1, e o relatório não diz que 12:48 e
   12:59 são rodadas diferentes.
3. **Modelo do Codex das 18:00.** O `hashes.json` reposto não tem `modelo`, porque foi gravado antes do conserto. Só a
   rodada das 19:26 prova o Luna pela evidência.
4. **`daFase` vazio passa sem nada.** Se `HARNESSES_F<n>` não tiver interseção com `HARNESSES`, as fases 1, 2, 4, 5 e 6
   rodam o laço vazio e dão verde. A fase 7 também, porque espera `# pass 0`. Melhor falhar quando a lista sair vazia.
5. **A fase 7 suja o `evidencia-22`** a cada rodada real (o 22-cliente regrava). Hoje volta por `git checkout` à mão
   (cópia em `etapas/logs/25-noite-f7-c-evidencia-22/`). Depois da junção, quem rodar a fase 7 na `integracao` precisa
   saber disso. O que os harnesses viram na fase 7 (`lido.json`, `saida.jsonl`) fica só nessa cópia fora do repositório.
   No ramo fica só o TAP.
6. **Log do `cliente.ps1` no TEMP.** `%TEMP%/hub-ensaio-25-subir-22.log` (19:25) continua lá. Não tem segredo: conferi
   `token|pass|eyJ|sk-|ghu_`, e o que aparece é só texto de `[PASSA]`. É a ressalva da rodada 1 se cumprindo. Não apaguei,
   porque não é meu.
7. Seguem as ressalvas da rodada 1 que o relatório já assume: a fase 2 confere no B só o `tasks.md`; o `write_note`
   pelos harnesses e o MCP reconectando depois do reinício ficam fora; o Codex nas fases 4-7 fica fora por decisão do
   maestro (provado nos tickets 17, 18, 21 e 22).

### O que quebra ao juntar

Nada do que vi. Não há conflito com a `integracao`, `evidencia-22` e `evidencia-24` estão iguais e o único arquivo
comum novo é `harnesses.mjs`, do próprio 25. O risco é de operação, não de código: a ressalva 5 e a margem de memória
da fase 7 (ressalva 1).

### Critérios do ticket

- **A prova de ponta a ponta passa com todas as peças juntas:** sim no escopo decidido. As fases 1 a 7 estão verdes com
  Claude e Copilot (a 3 sem harness), e o Codex está verde nas fases 1 e 2. As rodadas foram separadas por memória,
  como as costuras aceitas pediam.
- **O relatório lista o que fica para a instalação e para a segunda máquina:** sim. Estão lá a convergência do par novo
  (ticket 26), a ordem por fases e a ressalva do 11. Falta a atualização da ressalva 1.
