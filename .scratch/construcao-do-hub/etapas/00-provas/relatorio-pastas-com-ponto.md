# Relatório da prova 2: pastas com ponto fora do LiveSync (Vela, ticket 02)

Ramo `ticket-02` (worktree `C:\context-hub-wt\ticket-02`), da ponta de `integracao` (3857c98). Prova em
`agents/code/test/provas/02-pastas-com-ponto/`.

## Resultado: passou

**A forma que funcionou:** `.livesync/ignore` na raiz do cofre de cada par, com duas linhas:

```
.*
.*/
```

O CLI transforma `.*` em `**/.*` (nome com ponto, em qualquer nível) e `.*/` em `**/.*/**` (tudo dentro de pasta com
ponto), com `dot: true` (`src/apps/cli/serviceModules/IgnoreRules.ts`, commit `14141446`).

| Critério do ticket 02 | Resultado | Evidência |
|---|---|---|
| `projeto/.venv/`, `projeto/.git/`, `clientes/x/.secrets/` e `.oculto/` não chegam ao banco nem ao outro disco, com o CLI rodando | **Passou** | `evidencia/com-exclusao.log`, bloco "CLI rodando" |
| O mesmo na varredura de partida, depois de reiniciar o CLI | **Passou** | mesmo log, bloco "varredura de partida" |
| O relatório diz qual forma funcionou e o que vai doer com o gerador de exclusões (ticket 06) | Feito | este relatório |

**Montagem da prova:**
- Dois pares de ensaio com E2EE e caminho ofuscado, cada um com seu CouchDB 3.5.2: `hub-ensaio-02-a` em
  `127.0.0.1:5996` e `hub-ensaio-02-b` em `127.0.0.1:5997`.
- Uma replicação de envio em cada par (S3) e o CLI do LiveSync em `daemon` como sincronizador.
- A pasta A nasce com o hub de ensaio do ticket 04 (`montar.mjs`).

**Arquivos com ponto criados no A, mais um arquivo de controle sem ponto:**
- `projeto/.venv/lib/…`
- `projeto/.git/HEAD-…`
- `projeto/.cache/…`
- `projeto/.env-…`
- `clientes/x/.secrets/…`
- `.oculto/…`

**O que a prova confere, nos dois momentos:**
- o controle chega ao disco do B;
- nenhum arquivo com parte começando por ponto aparece no disco do B;
- nenhum aparece no banco do A nem no do B. O banco é lido em claro por um dispositivo leitor (`sync` + `ls`), porque o
  caminho fica ofuscado no CouchDB.

**Os dois momentos:**
- "CLI rodando": os arquivos nascem com o `daemon` vivo.
- "Varredura de partida": os arquivos nascem com o CLI do A parado, e ele é religado com o banco local e a
  configuração que já tinha.

`pwsh agents/code/test/provas/02-pastas-com-ponto/prova.ps1` → **12 de 12 PASSA** (`evidencia/com-exclusao.log`).

**O vermelho (`-SemExclusao`, `evidencia/sem-exclusao.log`) reproduz o defeito do ticket 48, agora com E2EE.**
- Tudo que tem ponto aninhado vai ao banco dos dois pares e ao disco do B. Isso inclui os `.gitkeep` do esqueleto do
  hub (`agents/skills/.gitkeep` e outros) e `clients/aurora/migracao-de-tenant/.secrets/leia-me.txt` do hub de ensaio.
- O `.oculto/` do primeiro nível fica fora.
- Numa rodada anterior com a pasta A vazia, os criados com o `daemon` vivo também ficaram fora. Só a varredura de
  partida vazou.

**Causa, lida no código do CLI (commit `14141446`):**
- **Varredura de partida:** o filtro "parte com ponto" de `main.ts` (~linha 535) divide o caminho com
  `targetPath.split(path.sep)`. No Windows, `path.sep` é `\`, mas o caminho do cofre usa `/`. Então só o primeiro nível
  é barrado.
- **Observador (`daemon`):** usa outra regra, a regex `/(^|[/\\])\./`
  (`managers/CLIStorageEventManagerAdapter.ts:144`), que pega qualquer nível. A Brasa achou o mesmo.
- **O `.livesync/ignore`:** normaliza as barras antes de comparar, por isso fecha a varredura.

## O que vai doer ao ligar (com o gerador de exclusões, ticket 06, e o kit)

1. **O arquivo tem de existir antes da primeira partida do CLI**, em cada par. As regras são lidas só quando o CLI
   começa (`IgnoreRules.load()` em `main.ts`). Então:
   - se o CLI partir uma vez sem o arquivo, o que tem ponto aninhado entra no banco e na outra máquina, e fica lá;
   - mudar o arquivo exige reiniciar o CLI;
   - o kit escreve o `ignore` antes de ligar o sincronizador.
2. **Negação derruba o CLI.** Uma linha começando por `!` faz o `load()` lançar erro, e o CLI não sobe. O gerador
   nunca pode escrever `!`.
3. **`import: .gitignore` herda a negação.** Se o gerador usar essa diretiva e o `.gitignore` do hub tiver uma linha
   `!`, o CLI cai do mesmo jeito. O `.gitignore` de hoje não tem `!`. Mais seguro: o gerador escreve o `ignore` inteiro,
   sem importar. Só a forma exata `import: .gitignore` é aceita; outra forma vira aviso e é ignorada.
4. **O `.livesync/` não replica.** Ele tem ponto, então cada máquina precisa do seu `ignore`, posto pelo kit. A segunda
   máquina não recebe o arquivo pelo banco.
5. **O cofre não pode morar sob pasta com ponto.** A regex do observador olha o caminho absoluto. Um cofre em
   `…\.local\…` não sincroniza nada (achado da Brasa). `C:\context-hub` está bem; ensaios e worktrees também precisam
   estar.
6. **O que já vazou continua no banco.** No spike do ticket 48, o banco já tem `projeto/.git/HEAD` e outros. O kit
   começa de banco novo. Se reaproveitar algum banco, precisa de uma limpeza (`rm` do CLI) antes.
7. **O plugin do Obsidian não foi testado aqui.** No ticket 48, o plugin gravou nos discos A e B o que vazou ao banco.
   Com o `ignore` em todo CLI, nada com ponto chega ao banco por este caminho. Não verificados:
   - se o plugin lê o `.livesync/ignore` (provavelmente não; ele tem a própria lista de exclusões);
   - se o CLI do outro par escreve no disco um arquivo com ponto que entrou no banco por outro caminho.
8. **O que não tem ponto continua com o gerador.** Esta prova cobre só "tem ponto". O resto da lista do ticket 06 (o
   que fica numa máquina só sem ponto no nome) vai no mesmo arquivo, como padrões sem `!`.
9. **Correção na fonte.** O defeito do `split(path.sep)` é do CLI no Windows. Vale um pedido upstream (não aberto). O
   `ignore` continua necessário mesmo depois, porque é a regra do hub (ticket 12).

## O que muda no spec

Nada de decisão. O Worker 4 já previa `.livesync/ignore` com `.*` e `.*/` ("não testado" no 48); agora está
**verificado**, nesta máquina, com E2EE e caminho ofuscado, com o CLI rodando e na varredura de partida. Os itens 1 a 3
acima entram como requisitos do gerador (ticket 06) e do kit.

## Reaproveitamento e limpeza

- **Módulo:** `banco.psm1`, `compose.yml`, `couchdb.ini` e `04.env.modelo` são cópia da prova 01 da Brasa (commit
  `43a4ea9`, combinado com ela). A cópia tem três acréscimos:
  - `Start-Sincronizador -Reiniciar`;
  - `Set-ExclusaoComPonto`;
  - `Get-ArquivosNoBanco`.
  O ticket 07 junta as duas cópias.
- **Achado no caminho:** a primeira cópia, feita antes do commit dela, montava o mesmo `couchdb.ini` nos dois pares. O
  CouchDB regravou nele o admin, o uuid e o secret, e a rodada seguinte foi recusada (`unauthorized`). A versão dela
  já monta uma cópia por par (`HUB_BANCO_INI`). Avisei a Brasa do `.ini` regravado na worktree dela.
- **Contêineres:** `hub-ensaio-02-a` e `-b` são apagados ao fim de cada rodada (`docker compose down -v`). Conferido:
  nenhum contêiner nem volume `hub-ensaio-02-*` ficou. A pasta `%TEMP%\hub-ensaio-02` foi apagada.
- **Pastas que não são minhas:** há várias pastas `%TEMP%\hub-ensaio-02-XXXXXX` (com `hub/` e `fora/` dentro),
  criadas por outro trabalho. Não toquei nelas.
- Nenhum arquivo global foi tocado.

## Estado

- 2026-10-16 ~22h35: ticket pego; worktree criada.
- 2026-10-16 ~23h: vermelho reproduzido, verde 12/12 em três rodadas (a última sobre a cópia alinhada ao commit da
  Brasa). Commit 6191e40. Pedida a revisão do Fiel.
- 2026-10-16 ~23h15: Fiel/Fielzinho = passa. Ressalva: quando o montador mudar para agents/code/test/ (ticket 05), atualizar a chamada no banco.psm1 e repetir. Encaminhado ao Rebite.
