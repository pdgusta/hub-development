# Relatório do ticket 54: a busca sai do vault

Malho (construtor do par B, lenovo-ideapad), 2026-10-24.

- **Ramo:** `ticket-54` na worktree `C:/context-hub-wt/ticket-54`.
- **Ponta de partida:** o ramo **`ticket-53`** (e4ba4b5), porque o 53 não foi juntado e os dois mexem em
  `instalacao.md`.
- **Commits:**
  - dc6c0b0: código e testes;
  - 43ff3f1: docs, skill e guia;
  - a9f1b4d: consertos da revisão.
- **O que não foi feito:** junção, `push` e qualquer mudança em `C:/context-hub` ou no par que está rodando.

## Decisões do construtor

- **Chave `HUB_BUSCA_DIR`** (a sugestão do ticket). Segue o padrão do `HUB_MCP_BANCO_DIR`: a pasta de uma peça, aqui com
  a instalação e o estado dela. O modelo `env/03.env`, que o guia (§3) manda juntar a cada `.env`, ganhou
  `HUB_BUSCA_DIR=C:\hub-par\busca`, ao lado de `banco`, `cli-db` e `livesync`.
- **Ponteiro `<hub>\.local\busca.json`** (`{"dir": "..."}`).
  - Por quê: o `iniciar.ps1` e o `relatorio.mjs` rodam sem o `.env` (quem os chama é o terminal "Busca" e os agentes),
    e o 03 grava o ponteiro.
  - Fica em `.local` porque não replica: cada máquina tem o seu.
  - É separado do `par.json` porque o dono do `par.json` é o 08, e o 03 roda antes dele.
- **O 03 acha a pasta assim:** o `HUB_BUSCA_DIR` do `-EnvFile`; sem `-EnvFile`, o ponteiro (rodar de novo sem o
  `.env`); sem nenhum dos dois, recusa. Também recusa:
  - caminho relativo;
  - pasta dentro do hub;
  - pasta que já existe com outra coisa dentro;
  - num par antigo, pasta noutro disco que o hub.
- **O `instalar.ps1` passa o `-EnvFile` ao 03.** A lista da pesquisa não citava isso, mas é preciso.
- **Par já instalado:**
  - Há `<hub>\.local\busca` e a `HUB_BUSCA_DIR` está vazia: o 03 **renomeia** a pasta para a `HUB_BUSCA_DIR` (mesmo
    disco, sem `npm ci`).
  - A `HUB_BUSCA_DIR` já tem a busca: o 03 apaga a antiga.
  - Com a busca de pé, o Windows recusa, e o passo diz "ela está de pé? Pare-a ... e rode o 03 de novo".
- **Busca sem ponteiro:** o `iniciar.ps1` e o `relatorio.mjs` usam o `.local\busca` de um par de antes do 54, e o
  `iniciar.ps1` avisa para rodar o 03 com `-EnvFile`. Assim, juntar o 54 no hub (que replica para os dois pares) não
  derruba a busca de ninguém antes da mudança.
- **Para onde vão estado e relatório:** o `estado` (`XDG_CACHE_HOME`) vai para `<pasta>\estado` e o `relatorio.json`
  para `<pasta>\relatorio.json`. Só com `HUB_BUSCA_OHS` e sem pasta (os testes), o estado vai para
  `<hub>\.local\busca-estado` e o relatório não é gravado; nenhum dos dois recria o `.local\busca`.
- **O índice fica na raiz do hub** (`<hub>\.obsidian-hybrid-search.db`, `-shm`, `-wal`: 3 arquivos). Isso é **desvio do
  brief**, que dizia "o índice em `estado`". O pacote 0.16.2 fixa o caminho: em `dist/src/config.js`,
  `dbPath = path.join(OBSIDIAN_VAULT_PATH, '.obsidian-hybrid-search.db')`, lido no pacote instalado no B. A doc antiga
  dizia, errado, que o índice ficava em `.local\busca\estado`; foi corrigida.
- **O que a varredura achou:** `proxy.psm1`, `ligar-cliente.ps1` e `08-harnesses.mjs` só usam a rota ou o nome `busca`,
  não o caminho, e não mudaram. O resto de `.local` (vigia, exclusões, `par.json`...) fica onde está.

## O que mudou

| Arquivo | Mudança |
|---|---|
| `agents/code/kit/par/03-busca.ps1` | `-EnvFile`, `HUB_BUSCA_DIR`, ponteiro, recusas, mudança do par antigo; saída com `dir` |
| `agents/code/kit/par/instalar.ps1` | passa `-EnvFile` ao 03 |
| `agents/code/kit/par/env/03.env` | `HUB_BUSCA_DIR=C:\hub-par\busca` |
| `agents/skills/busca/iniciar.ps1` | pasta pelo ponteiro (ou a antiga, com aviso); estado na pasta |
| `agents/skills/busca/relatorio.mjs` | pacote e `relatorio.json` pela pasta; BOM; "busca não instalada" |
| `agents/skills/busca/SKILL.md` | uso do 03, onde fica a busca e o índice, o relatório |
| `agents/code/test/12-kit-busca.test.mjs` | reescrito (7 casos, abaixo) |
| `agents/code/test/12-busca/servidor.mjs` | `instalarSeFaltar` com `.env` de ensaio (busca ao lado do hub); `pacoteDoEnsaio` |
| `agents/code/test/12-busca.test.mjs`, `13-gemini.test.mjs`, `13-gemini/teste-unico.mjs` | `pacoteDoEnsaio` |
| `agents/code/test/22-proxy.test.ps1` | o 03 com um `.env` de ensaio (Docker; **não rodei**) |
| docs `busca.md`, `kit-de-par.md`, `instalacao.md`, `operacao.md`, `stack.md` | o caminho novo; guia §10 "Par já instalado: a busca sai do hub", com o comando |
| roteiro `.scratch/context-hub/instalacao-par-b.md` (**sem commit**) | nota no bloco 4; seção "Depois do ticket 54" com os comandos do B |

## Testes

- **`12-kit-busca.test.mjs`**, sozinho, com hub de ensaio e busca de ensaio ao lado (nunca o hub ao vivo): **7/7**. Os
  casos:
  - `-WhatIf` não grava;
  - instala na `HUB_BUSCA_DIR`, sem `.local\busca` e com o ponteiro;
  - rodar de novo não muda nada, com o `.env` ou só com o ponteiro;
  - recusa pasta dentro do hub e recusa sem `.env` nem ponteiro;
  - par antigo: muda de lugar sem reinstalar (a marca do `node_modules\.package-lock.json` não muda);
  - `.local\busca` que sobrou sai do hub;
  - a busca sobe pelo caminho novo, responde 0.16.2 e não cria `.local\busca`.
- **Vermelho antes:** 7/7 falharam ("A parameter cannot be found that matches parameter name 'EnvFile'").
- Uma asserção que eu tinha escrito saiu: o `<pasta>\estado` existir depois da partida. O pacote só cria o estado
  quando grava PID ou log (`local-state.js`, `auto-heal.js`), não no `serve --foreground`. O `XDG_CACHE_HOME` novo
  **não é verificado por teste**.
- **Sozinhos, depois dos consertos:** `12-kit-busca` 7/7, `12-busca` 9/9, `13-gemini` 4/4. O `09-mcp-banco-sem-docker`
  (do 53) não mudou.
- **Suíte inteira**, uma vez, com o código do a9f1b4d (ainda sem commit na hora): 394 testes, **368 passam, 12 falham**,
  14 pulados. As 12 são as mesmas falhas de ambiente do 53:
  - **12-busca (9) e 13-gemini (1):** "busca não ficou pronta em 3 minutos", com a máquina carregada. Sozinhos,
    passam.
  - **25-pares-sem-docker (1):** caminho-padrão do A, `C:\Projetos\hub-mcp-banco-wt\integracao`.
  - **gerar-exclusoes/gerador (1):** caminho-padrão do A, `C:\Projetos\bancada-busca`.
- **Sem teste do `-Desfazer`.** Pela leitura, o `-Desfazer` do kit (o do 08) não toca na instalação da busca, nem antes
  nem depois; o guia diz isso. Não rodei para provar.
- Sem Docker, sem harness de verdade, sem login copiado.

## Revisão (skill `code-review`, desde `ticket-53`)

Os dois eixos rodaram em sequência, por causa da regra de um subagente por vez.

- **Consertado:**
  - o `Move-Item` noutro disco dava o diagnóstico errado ("está de pé?") → mensagem própria;
  - caminho relativo → recusa;
  - o `.env` passa a ser lido com `-LiteralPath`;
  - o `relatorio.mjs` sem ponteiro recriava o `.local/busca` (`mkdirSync`) → não grava;
  - o `iniciar.ps1` com `HUB_BUSCA_OHS` e sem pasta recriava o `.local\busca\estado` → `.local\busca-estado`;
  - ponteiro com BOM no `relatorio.mjs`;
  - o segundo par do teste nascia dentro de um teste → `before`;
  - linha do `.env` de ensaio que ninguém lê.
- **Ficou, com a razão:**
  - O 03 lê o `.env` com o próprio laço e não com o `Read-EnvPar`, que exige as chaves do banco. O 05
    (`Read-EnvMcpBanco`) faz o mesmo.
  - A lógica "ponteiro ou `.local\busca`" fica repetida no `iniciar.ps1` (pwsh, skill) e no `relatorio.mjs` (node): são
    linguagens e donos diferentes, e são 4 linhas cada.
  - Linhas acima de 120 colunas nos `.ps1`, como já há no kit.
  - O `-WhatIf` de um par antigo anuncia também o `npm ci`, que de verdade não rodaria: é ruído, não gravação.
- **Achados sem conserto:** nome curto do Windows (`C:\CONTEX~1`) e junção não são expandidos na recusa "dentro do
  hub". Pelo `instalar.ps1`, o hub já chega em caminho longo.

## Fora da construção: os comandos para os dois pares (maestro, com o Gustavo, depois da junção)

Em cada par, com a busca parada (terminal "Busca": Ctrl+C) e o 54 já no hub:

```powershell
# Par A (armis00323)
$EnvA = 'C:\hub-transporte\armis00323.env'          # conferir o caminho do .env do A
Add-Content $EnvA 'HUB_BUSCA_DIR=C:\hub-par\busca'
pwsh C:\context-hub\agents\code\kit\par\03-busca.ps1 -Hub C:\context-hub -EnvFile $EnvA -WhatIf   # "mudar a busca para C:\hub-par\busca"
pwsh C:\context-hub\agents\code\kit\par\03-busca.ps1 -Hub C:\context-hub -EnvFile $EnvA
Test-Path C:\context-hub\.local\busca                # False
Get-Content C:\context-hub\.local\busca.json         # {"dir":"C:\\hub-par\\busca"}
# terminal "Busca" de novo: pwsh -NoProfile -File C:\context-hub\agents\skills\busca\iniciar.ps1

# Par B (lenovo-ideapad): o mesmo, com $EnvB = 'C:\hub-transporte\lenovo-ideapad.env' (roteiro do B, "Depois do ticket 54")
```

Se a `HUB_BUSCA_DIR` do A não estiver no mesmo disco do hub, o 03 recusa e diz o que fazer: apagar a antiga e
reinstalar.

**Medida no A antes e depois** (último item do ticket). Esta é uma **aproximação** da varredura do CLI, não o código
dele: `readdir` recursivo em todas as pastas, com `lstat` em cada segmento do caminho, como o `scanDirectoryInto` com
`assertNoSymbolicLinks` descrito na pesquisa. Rode antes do passo acima e depois:

```powershell
node -e "const fs=require('fs'),p=require('path');let n=0,l=0;const t=Date.now();function seg(f){let a='';for(const s of f.split(p.sep)){a=a?p.join(a,s):s+p.sep;fs.lstatSync(a);l++}}function d(x){for(const e of fs.readdirSync(x,{withFileTypes:true})){const f=p.join(x,e.name);seg(f);if(e.isDirectory())d(f);else n++}}d(process.argv[1]);console.log(JSON.stringify({arquivos:n,lstat:l,ms:Date.now()-t}))" C:\context-hub
```

No B, a medida do maestro (`varredura.mjs`, scratchpad dele) deu 13,6 s e 8.639 arquivos com a busca no vault. Os
números deste comando não são comparáveis com esses; compare só o antes e o depois dele.

## O que ficou de fora

- O 22-proxy (Docker) foi mudado e não rodou.
- Os avisos do `iniciar.ps1` sem ponteiro (o caminho antigo) não têm teste.
- O índice (3 arquivos) segue no vault, porque o pacote fixa o caminho.
- A mudança nos dois pares e a medida no A ficam com o maestro.
