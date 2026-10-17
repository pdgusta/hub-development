# Relatório do ticket 29: testes com harness de verdade só sob pedido (Brasa)

Ramo `ticket-29` (worktree `C:\context-hub-wt\ticket-29`), da ponta de `integracao` 8d1d785, que não andou depois.
Commits: 654c329 (o código e o teste), 0266761 (a evidência da rodada pedida).

## O que foi construído

**O módulo:** `agents/code/test/harness-real.mjs`.
- `comHarness(nome, fn)`:
  - Sem `HUB_HARNESS_REAL=1`, registra um teste pulado com o motivo. O corpo `fn` não roda.
  - Com a variável, `fn` vira o corpo de um `describe`, com os ganchos e os testes dentro dele.
- O motivo: `chama harness de verdade (login, cota, evidência versionada): rode com HUB_HARNESS_REAL=1`.
- `relatorioDeHashes({ antes, depois, gravadoEm, rodadas })`: uma linha por arquivo real que mudou. Detalhes em
  "Critérios", item 3.

**Os três testes de harness** passam a usar `comHarness`:
- `provas/03-codex-hooks/prova.test.mjs` (o `codex exec` de verdade, com login);
- `provas/03-codex-hooks/instalar.test.mjs` (o app-server do Codex, sem login);
- `ponta-a-ponta/14-guardas.test.mjs` (Claude, Codex e Copilot de verdade).

O que rodava na carga do arquivo foi para dentro do corpo: a pasta de ensaio, os hashes de antes e o apagar da
evidência do 14. Nenhuma linha de teste mudou, só o recuo; a linha de uso de cada um diz a variável. O `after` do 14
passou a usar `relatorioDeHashes`.

Fora esses três, nenhum teste da suíte chama harness. Procurei por `CODEX_JS`, `claude.exe`, `COPILOT_JS` e
`app-server`; os outros `spawn` chamam só o `node` e o `git`.

## Critérios do ticket

Teste novo: `agents/code/test/harness-real.test.mjs`, no `node --test` comum. Resultado: 5 de 5.

1. **Sem `HUB_HARNESS_REAL`, a suíte inteira não chama harness, não copia login e não muda arquivo versionado. Os
   testes de harness aparecem pulados, com o motivo.**
   - O teste roda os três arquivos num `node --test` filho, sem a variável. O filho tem HOME, TEMP e APPDATA de ensaio
     e o PATH só com o node: se algum corpo rodasse, não acharia harness nem login de verdade.
   - Ele confere quatro coisas: cada arquivo dá um teste de topo `# SKIP` com o motivo, e nada mais; a evidência
     versionada fica com os mesmos hashes; o TEMP de ensaio fica vazio; o HOME de ensaio fica vazio.
   - Vermelho antes do conserto: os três rodaram, falharam sem achar harness, e o 14 apagou a evidência versionada na
     carga do arquivo. Restaurei com `git checkout`.
   - Suíte inteira, `node --test "agents/code/test/**/*.test.mjs"`, sem a variável: 86 testes, 83 passam, 3 pulados
     (log `C:\context-hub-wt\ticket-29\.local\suite-sem-variavel.log`). Nenhum arquivo versionado mudou.
2. **Com `HUB_HARNESS_REAL=1`, a prova 03 e a ponta a ponta do 14 rodam como antes e passam.** Comando:
   `HUB_HARNESS_REAL=1 node --test --test-concurrency=1` dos três arquivos. Resultado: 11 de 11, saída 0 (log
   `.local/harness-real.log`).
   - 14: claude 38 s, codex 23 s, copilot 27 s.
   - Prova 03: o instalador 2 s, o `codex exec` 39 s.
   - A evidência regravada é a desta rodada pedida e foi commitada (0266761).
   - O `--test-concurrency=1` impede a prova 03 e o 14 de rodarem juntos.
3. **Quando a conferência por hash falha, a mensagem diz qual arquivo real mudou.**
   - O que cada linha traz:
     - o arquivo e os dois hashes, curtos;
     - a hora da gravação, pelo mtime do arquivo real;
     - se essa hora caiu na rodada de algum harness (a janela vai do login copiado ao ensaio apagado) ou fora das
       rodadas deste teste.
   - Arquivo que sumiu não tem hora. A linha diz "sem hora de gravação: não dá para saber se foi o teste", sem chutar
     (pedido do maestro).
   - Exemplo: `~/.codex/config.toml mudou (aaaaaaaa → bbbbbbbb), gravado às 2026-10-17T00:17:30.000Z, durante a rodada
     do codex (00:17:21 a 00:17:41)`.
   - Testado em quatro casos: nada mudou, mudou dentro de uma rodada, mudou fora, sumiu ou apareceu.
   - Limite: o mtime é o da última gravação. Duas gravações seguidas mostram só a segunda.
4. **As regras da construção e o `juntar-tickets.md` dizem quando rodar com a variável.** Feito pelo maestro
   (2026-10-16 ~22h): o comando comum e o caso da variável; a regra provisória sai quando o 29 entrar. A sugestão era:
   - O comando comum fica `node --test "agents/code/test/**/*.test.mjs"`, sem a variável.
   - Com a variável e `--test-concurrency=1`, só quando o ticket mexe na prova 03, na guarda do 14 ou nos hooks dos
     harnesses.
   - A regra provisória (deixar as duas pastas de fora) cai quando o 29 entrar em `integracao`.

## Uso de harness e login (rodada de 2026-10-17, 00:44 a 00:47 UTC)

- Uma sessão por harness, modelos baratos, como antes: haiku no Claude e no Copilot, gpt-6-luna baixo no Codex.
- Copiado e apagado, pelo registro do próprio 14 (`evidencia-14/hashes-claude-codex-copilot.json`):

| Harness | O que foi copiado | Copiado (UTC) | Apagado (UTC) |
|---|---|---|---|
| Claude | `.credentials.json` | 00:44:22 | 00:44:56 |
| Codex | `auth.json` | 00:45:01 | 00:45:19 |
| Copilot | só os campos de login do `config.json` | 00:45:21 | 00:45:46 |
| Codex, prova 03 | `auth.json` | — | 00:46:26 (`login-apagado.txt`, `apagado=true`) |

- **Hashes das pastas reais, antes e depois:** conferidos por mim, iguais nos seis arquivos (início de cada hash):

| Arquivo | Hash |
|---|---|
| `.claude/.credentials.json` | `13644f92` |
| `.claude/settings.json` | `411d8d3b` |
| `.codex/auth.json` | `9e42496b` |
| `.codex/config.toml` | `36875344` |
| `.codex/hooks.json` | `d822fa38` |
| `.copilot/config.json` | `283253d4` |

  Arquivos: `.local/hashes-reais-antes.txt` e `hashes-reais-depois.txt`.
- Nenhum `auth.json` nem `.credentials.json` sobrou em `%TEMP%\hub-ensaio-*`.

## Avisos (fora do ticket)

- **Pastas que o teste de unidade do 14 deixa.** `agents/code/test/14-guardas.test.mjs`, do Trilho, sem harness,
  deixa pastas `hub-ensaio-14-*` no TEMP a cada rodada (só um hub de ensaio, sem login). Isso confunde quem procura
  sobras da ponta a ponta, que usa o mesmo prefixo. O Trilho já consertou no ramo `ticket-12` (58b9563); chega com o 12.
- **O nome do usuário na evidência da prova 03.** A evidência versionada traz o caminho curto do usuário
  (`GUSTAV~1.DEL`) em `codex-exec.jsonl`, `config.toml`, `eventos.jsonl` e `login-apagado.txt`. Isso já estava no
  commit anterior. A do 14 tira o nome (`semCasa`); a prova 03 não tira.

## Rodada 2 (consertos do parecer da rodada 1)

Ponta `0da445e`, com `integracao` 0a8e17f (ticket 27) juntada em 1736f46.

1. **O 27 protegido.** `ponta-a-ponta/27-fim-da-resposta.test.mjs` foi embrulhado em `comHarness`, como o 14: a
   evidência não é apagada na carga e nenhum harness é chamado sem a variável. O `after` dele usa `relatorioDeHashes`,
   e a linha de uso diz a variável.
   - Vermelho antes: com o 27 incluído no teste, ele apagou `evidencia-27/` na carga. Restaurei com `git checkout`.
2. **Sem lista de nomes.** `harness-real.test.mjs` acha sozinho os arquivos de teste que chegam a um harness ou a um
   login, pelo texto deles e dos módulos locais que importam. As marcas:
   - o Codex: `CODEX_JS`, `codex.js`, `app-server`, `@openai/codex`, `listarHooks`;
   - o Copilot: `COPILOT_JS`, `npm-loader`, `@github/copilot`;
   - o Claude: `claude.exe`;
   - os logins: `.credentials.json`, `auth.json`.

   Cada arquivo achado precisa:
   - ter o corpo sob `comHarness(`;
   - e, sem a variável, dar só um teste de topo pulado, com o motivo, sem mexer em evidência, TEMP nem HOME.

   Os quatro conhecidos (03 instalador, 03 prova, 14, 27) estão numa conferência à parte, para a busca não passar
   vazia.
   - **Contraprova:** um `ponta-a-ponta/zz-contraprova.test.mjs` sem proteção, que chama `claude.exe`, deixou dois
     testes vermelhos ("são achados" e "aparecem pulados"). Depois foi apagado.
   - **Limite:** a busca é por texto. Um teste que chame um harness por um nome fora das marcas (outro binário, um
     caminho montado em partes) escaparia.

**Testes:**
- `harness-real.test.mjs`: 6 de 6.
- Suíte inteira sem a variável: 116 testes, 112 passam, 4 pulados (03 instalador, 03 prova, 14, 27). Log em
  `.local/suite-sem-variavel-2.log`.
- `git status` limpo depois da suíte.
- **A rodada com `HUB_HARNESS_REAL=1` não foi repetida.** A proteção não mudou o caminho real da 03 nem do 14, que
  passaram na rodada 1. O 27 ganhou o embrulho e a mensagem por hash, e não rodei ele de verdade (`node --check` ok).
  Rodo se o Fiel pedir.

