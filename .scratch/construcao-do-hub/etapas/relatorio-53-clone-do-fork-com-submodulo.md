# Relatório do ticket 53: o clone do fork traz o submódulo do LiveSync

Malho (construtor do par B, lenovo-ideapad), 2026-10-24. Ramo `ticket-53` na worktree `C:/context-hub-wt/ticket-53`, a
partir do `main` 70a9f73. Commits: 7e20bee (conserto) e e4ba4b5 (consertos da revisão). Não juntado no `main` e sem
`push` (brief: a junção é do maestro com o Gustavo). `C:/context-hub` não foi tocado, além do registro da worktree e do
ramo no `.git` dele, que o brief manda criar.

## O que mudou

- **Passo 05** (`agents/code/kit/par/mcp-banco/mcp-banco.psm1`, `Install-ForkMcpBanco`):
  - Quando o passo vai montar (o `dist\main.js` falta ou está velho), antes do `npm ci`, ele lê os `path =` do
    `.gitmodules` do fork (`Get-SubmoduloVazio`). Um submódulo sem pasta, ou sem nada além do `.git`, é recusado com:
    `submódulo lib/livesync-commonlib vazio em <pasta> (o clone não o trouxe): rode git -C "<pasta>" submodule update
    --init e o passo de novo`.
  - Um fork já montado roda sem o submódulo e não é recusado.
  - `npm ci` e `npm run build` passam por `Invoke-NpmFork`. Se o npm cai, o erro traz a saída dele, inteira até 60 linhas;
    acima disso, as 20 primeiras e as 40 últimas. O erro de uso do `npm ci` vem no começo da saída; o do tsup e o log do
    npm vêm no fim.
  - As mensagens agora são `npm ci falhou em <pasta> (npm ci --ignore-scripts):` e `build do fork falhou em <pasta>
    (npm run build):`, cada uma seguida da saída do npm.
- **Guia** `agents/code/docs/instalacao.md`, §5: o clone na B passa a ser
  `git clone --recurse-submodules -b integracao <bundle> C:\Projetos\hub-mcp-banco`. A seção diz que o bundle não leva o
  submódulo (vrtmrz/livesync-commonlib, f9f07e97, conferido no fork) e que o `--recurse-submodules` o busca no GitHub,
  por isso precisa de rede. Diz também que o conserto é o `submodule update --init`. O parágrafo do passo 05 ganhou as
  duas recusas novas.
- **Doc do componente** `agents/code/docs/componentes/mcp-do-banco.md`: ganhou o passo 2 do `Install-ForkMcpBanco`, as
  mensagens de erro e a contagem de casos do teste (18 → 23).
- **Doc da infraestrutura de teste** `agents/code/docs/componentes/infraestrutura-de-teste.md`, armadilha "Mensagem que
  quebra de linha": registra o `Test-NaSaida`.
- **Roteiro do par B** `C:/Projetos/context-hub/.scratch/context-hub/instalacao-par-b.md`, passo 2: clone com
  `--recurse-submodules` e um comentário com o conserto. **Sem commit**: o git do planejamento é do maestro.

## Testes

- **Teste novo:** caso 5 de `agents/code/test/banco/mcp-banco-sem-docker.ps1`, que roda pelo
  `09-mcp-banco-sem-docker.test.mjs`, sem Docker e na pasta de ensaio do `pastaDeEnsaio`. A costura é o passo do kit
  chamado como o kit chama (`pwsh 05-mcp-banco.ps1 -EnvFile`), mais o `Install-ForkMcpBanco` direto no caso do fork já
  montado. O fork é inventado: `.gitmodules` real e um build `node -e` que marca que rodou e cai com o
  "Could not resolve ../lib/livesync-commonlib/...". São 5 casos:
  - fork sem o submódulo: para antes do build e diz o comando;
  - submódulo só com o `.git`: conta como vazio;
  - fork já montado: não remonta nem recusa;
  - build que cai: traz a saída do `npm run build`;
  - `npm ci` que cai (sem `package-lock.json`): traz a saída dele.
- **Vermelho antes do conserto:** os 3 casos da primeira versão falharam com o `build do fork falhou em <pasta>` de
  antes, sem detalhe; os 18 antigos passaram. Os 2 casos que vieram da revisão (`.git` e fork já montado) foram escritos
  junto com o conserto e não foram vistos falhar sozinhos. Pelo código antigo, falhariam: a pasta com `.git` passava pela
  checagem, e a checagem recusava sempre.
- **Arquivo sozinho, no fim:** `node --test agents/code/test/09-mcp-banco-sem-docker.test.mjs` passa. O `.ps1` direto dá
  23 `[PASSA]` e 0 `[FALHA]`.
- **Fork real:** `Get-SubmoduloVazio` em `C:/Projetos/hub-mcp-banco`, que tem o submódulo, devolve 0 vazios. Foi só
  leitura, sem build.
- **Suíte inteira**, uma vez, no 7e20bee (antes dos consertos da revisão), com `node --test
  "agents/code/test/**/*.test.mjs"` e `TEMP` longo: 391 testes, **364 passam, 13 falham**, 14 pulados. Nenhuma falha
  está nos arquivos do ramo. As 13:
  - **12-busca (9) e 13-gemini (1):** "a busca não ficou pronta em 3 minutos", com a máquina carregada pela suíte. O
    `12-busca` sozinho passa 9/9 (156 s). O 13-gemini sozinho não rodei, porque é pesado; a causa é a mesma.
  - **25-pares-sem-docker (1):** `ENOENT` em `C:\Projetos\hub-mcp-banco-wt\integracao\src\tools.ts`, que é o padrão da
    máquina A em `ponta-a-ponta/25/pares.ps1:36`. No B, o fork está em `C:\Projetos\hub-mcp-banco`.
  - **gerar-exclusoes/gerador (1):** o módulo em `C:\Projetos\bancada-busca\...`, padrão da máquina A
    (`gerador.test.mjs:48`), não existe no B.
  - **45-duas-maquinas-sem-docker (1):** saída 3221225477 (0xC0000005, "Fatal error") sob carga. Sozinho, passa duas
    vezes.
- Depois dos consertos da revisão, só o arquivo do ticket foi rodado, porque eles mexem só no passo 05, no teste e nos
  docs.

## Revisão (skill `code-review`, desde `main`)

Os dois eixos rodaram em sequência, e não em paralelo como a skill pede, porque a regra da construção permite só um
subagente por vez.

- **Consertado:**
  - erro do npm só com o começo, que perderia o erro do fim → começo e fim;
  - pasta só com o `.git` → conta como vazia;
  - o `$falhou` repetia o comando → virou `$oQue`;
  - `Invoke-NpmFork` recebia o `$par` inteiro → recebe só a pasta;
  - o `Plano` (espaços colapsados) dava teste instável se a quebra caísse no meio de um caminho → `Test-NaSaida`, que
    compara sem espaço nenhum;
  - o teste dependia do texto "package-lock" do npm → passa a esperar `npm (error|ERR!)`;
  - a armadilha da infraestrutura de teste estava desatualizada;
  - a checagem recusava sempre, mais estrita que "antes do build" → só quando vai montar, e antes do `npm ci`, que leva
    minutos.
- **Ficou, de propósito:** a saída do `npm ci` também aparece no erro. O ticket pede só a do build, mas a causa é a
  mesma (a saída era jogada fora).

## O que ficou de fora

- O `-WhatIf` do passo 05 não confere o submódulo, porque a simulação não chama o `Install-ForkMcpBanco`. O ticket não
  pede isso.
- A checagem é de pasta vazia, não de "submódulo no commit certo": um checkout parcial ou noutro commit passa. Basta
  para o achado (o clone sem `--recurse-submodules` deixa a pasta vazia).
- O 25-pares e o gerar-exclusoes falham no B por caminhos-padrão da máquina A. Fora do escopo; ver se vale um ticket.
- Não houve Docker, harness de verdade nem login copiado.
