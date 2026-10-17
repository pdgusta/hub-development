# Relatório do ticket 22: proxy e kit de cliente

Brasa, 2026-10-17. Ramo `ticket-22`, worktree `C:/context-hub-wt/ticket-22`, de `integracao` 9cc878b.

## Costuras (aceitas pelo maestro, 2026-10-17)

1. **Passo 10 do kit de par:** `agents/code/kit/par/10-proxy.ps1` e `proxy/proxy.psm1`.
   - Usa o TBXark/mcp-proxy da release fixa, com SHA-256 conferido.
   - Rotas `busca`, `banco` (instância de leitura 8797) e `banco-escrita` (escrita do cliente 8798), um token por rota.
   - Os tokens ficam no ambiente do processo; o config só leva `${VAR}`.
   - O endereço vem de `HUB_PROXY_ADDR`: na tailnet, o IP Tailscale do par; no ensaio, 127.0.0.1.
2. **Kit de cliente:** `agents/code/kit/cliente/ligar-cliente.ps1`. Liga os três harnesses ao proxy no HOME de cada
   um (no ensaio, as variáveis de HOME de ensaio).
3. **Testes:**
   - sem Docker: `22-kit-cliente.test.mjs` e `22-proxy-sem-docker.test.mjs`, que entram na suíte;
   - com Docker e a trava: `22-proxy.test.ps1`, com o par do 07, a busca e o MCP do banco de verdade, mais um cliente
     de ensaio pelo proxy.
4. **Harnesses de verdade como cliente:** uma sessão de cada, modelos baratos, trava e aval de login, depois do Docker
   verde.

## O que foi feito

### Proxy do par (`agents/code/kit/par/proxy/proxy.psm1`)

- **Binário:** `mcp-proxy` 1.1.0 (release de 2026-09-15) baixado para `<estado do par>/mcp-proxy/`.
  - Confere o SHA-256 do pacote (da lista `checksums.txt` da release) e o do `mcp-proxy.exe`.
  - Só baixa se o exe falta ou não confere.
- **Config v2** (`<estado>/mcp-proxy/config.json`):
  - `type: streamable-http`, `addr` e `baseURL` de `HUB_PROXY_ADDR`;
  - cada servidor com `options.authTokens: ["${HUB_PROXY_TOKEN_<ROTA>}"]`;
  - as duas instâncias do banco com `headers.Authorization: "Bearer ${HUB_MCP_BANCO_<INSTÂNCIA>_TOKEN}"`;
  - `autoReconnect` com `reconnectInterval` de 5 s: o proxy vive mais que a busca e o MCP, e um servidor fora na
    partida entra quando volta (CONFIGURATION.md, `options`).
  - O proxy expande o ambiente por padrão (`-expand-env`). Uma variável ausente vira token vazio, e o proxy recusa
    subir: `authTokens[0] cannot be empty`, conferido à mão.
- **Pronto:** o `/_readyz` responde 200, e cada rota responde 401 sem token. Uma rota que não montou dá 404.
- **Idempotente:** com o mesmo config, os mesmos tokens e o processo de pé, não toca. Config mais novo que o
  processo, ou um token trocado no `.env` (revogar a gravação de um cliente, girar o de uma instância): religa.
  - Os tokens não estão no config: na partida, o passo grava `ambiente.sha256` (hash do ambiente, nunca o token) na
    pasta de estado e compara na volta seguinte (parecer r1, conserto 1; teste: o token velho dá 401, o novo abre).
  - O PID só vale se o processo for o `mcp-proxy.exe` desta pasta com este config.
  - `-WhatIf` só lista; `-Descer` para.
- **Tokens:** um por rota, nenhum igual a outro nem ao de uma instância; o kit recusa repetido.
- **`.env`:** `agents/code/kit/par/env/10.env.modelo` traz `HUB_PROXY_ADDR=127.0.0.1:8790` e os três tokens.

### Ponte do Claude Desktop e pasta conectada (geradas, não instaladas)

O Desktop roda no par: no glossário, ele não é cliente. O passo 10 gera os arquivos em `<estado do par>/desktop/`:

- `claude_desktop_config.json` com `mcpServers`:
  - `hub-busca`: `npx -y mcp-remote@0.14.3 <HUB_MCP_BUSCA_URL>`;
  - `hub-banco`: a escrita dos agentes do par (8796; ticket 11: o Desktop grava pelo MCP), com
    `--header-file <estado>/desktop/banco.headers`. Assim o token fica fora da linha de comando (README do mcp-remote).
- `pasta-conectada.md`: a pasta a conectar e as Folder instructions, que apontam o `AGENTS.md` do hub, a busca e a
  gravação com `base_rev`.
- Instalar fica com o Gustavo: fundir em `%APPDATA%\Claude\claude_desktop_config.json` e colar as instruções.

### Kit de cliente (`agents/code/kit/cliente/ligar-cliente.ps1`)

- Lê do `.env` do cliente só `HUB_PROXY_URL`. Os tokens ficam no ambiente de quem usa o harness, com os mesmos nomes do
  par: `HUB_PROXY_TOKEN_BUSCA`, `HUB_PROXY_TOKEN_BANCO` e `HUB_PROXY_TOKEN_BANCO_ESCRITA`.
- **Claude Code:**
  - em `.claude.json`, `mcpServers` com `type: http` e `headers.Authorization: "Bearer ${VAR}"`;
  - em `settings.json`, `deny` de `read`, `reindex` e `status` da busca (como no par, ticket 12).
- **Codex:** um bloco marcado no `config.toml` com `bearer_token_env_var`, `enabled_tools = ["search"]` na busca e
  `default_tools_approval_mode = "approve"`.
- **Copilot CLI:** em `mcp-config.json`, `headers` com `${VAR}` e `tools`: na busca, só `search`; no banco, `*`.
- **Por padrão, só leitura.** `-Escrita` liga a terceira rota; rodar sem `-Escrita` a tira.
- **Contrato:** vai num bloco marcado no global de cada harness (`CLAUDE.md`, `AGENTS.md` do `CODEX_HOME` e
  `copilot-instructions.md`), sem tocar no resto do arquivo.
  - Vem do `-Contrato <arquivo>` ou, sem ele, do `AGENTS.md` lido por `read_note` na rota de leitura do proxy.
  - Rodar o kit de novo traz o contrato em dia. Isso fecha, com uma proposta, o ponto aberto "como o contrato vai à
    configuração global no cliente".
- **Lançador:** `-Saida` gera `copilot-hub.cmd`, que chama `copilot --allow-all-mcp-server-instructions %*`.
- **Idempotente:** funde no que existe e só grava o arquivo que mudou. Nenhum arquivo leva token.

## Achados

- **A flag de instructions do Copilot CLI não tem chave de config.** A referência da CLI lista
  `--allow-all-mcp-server-instructions` só como opção de linha de comando. A referência do diretório de config não tem
  chave equivalente. Por isso o kit gera o lançador.
- **O `tar` no PATH do Git Bash é o do MSYS.** Ele lê `C:` como host remoto. O kit usa
  `%SystemRoot%\System32\tar.exe`.
- **Ordem dos `after` no `node:test`.** O `after` do ajudante de pasta de ensaio roda antes do `after` do teste. Por
  isso o executável de um proxy ainda de pé não sai (EPERM). O teste desce o proxy no `finally` do próprio corpo.
- **O Host que o proxy manda à busca** (medido no teste sem Docker, com o MCP falso registrando o cabeçalho) é o do
  endereço da busca, `127.0.0.1:<porta>`. O proxy é cliente MCP do servidor de trás, e não repassa o Host do cliente.
  Logo, a busca não precisa de `--allowed-host`. O Docker confere com a busca de verdade.
- **O token do cliente não chega aos servidores de trás.** Cada instância recebe o token dela (teste sem Docker).

## Testes

### Sem Docker (na suíte comum)

`node --test agents/code/test/22-kit-cliente.test.mjs agents/code/test/22-proxy-sem-docker.test.mjs`: 4 passam.

- **Kit de cliente:**
  - os três harnesses, só leitura, com o token de variável e nenhum token em arquivo;
  - `-Escrita` liga a gravação, e a volta sem ela a tira;
  - o que já estava nos arquivos fica, e a segunda volta não grava nada;
  - o contrato vai em bloco e é trocado quando muda;
  - o lançador é gerado.
- **Passo 10:** na frente de três MCP falsos (`agents/code/test/proxy/mcp-falso.mjs`), que registram o método, o Host
  e o Authorization que chegam.
  - Cada rota abre só com o token dela: sem token ou com o de outra rota, 401.
  - Cada instância recebe o token dela.
  - O Host que chega à busca é o endereço dela.
  - O config não leva token.
  - A ponte do Desktop e a pasta conectada são geradas, e o token fica só no `banco.headers`.
  - A segunda volta mantém o mesmo processo.

### Com Docker (trava)

`$env:HUB_MCP_BANCO_DIR='C:/Projetos/hub-mcp-banco-wt/brasa-22'; pwsh -NoProfile -File agents/code/test/22-proxy.test.ps1`

O fork roda numa worktree minha, destacada em `integracao` 34c3e50: a `integracao` do fork é do Rebite (maestro).

**Rodada verde: 2026-10-17 09:39-09:43, janela quieta, ponta `bae29bd`: 15 PASSA, 0 FALHA, 5 MEDIDA.** Log:
`etapas/logs/22-docker.log`; corredor `.local/corredor-22.ps1 -Wsl` (cópia em `etapas/logs/`).

| Caso | Resultado |
|---|---|
| o passo 05 sobe as três instâncias | PASSA |
| o passo 10 sobe o proxy (três rotas; ponte e pasta conectada geradas) | PASSA |
| sem token e com o de outra rota, 401 nas três rotas | PASSA (401, 401, 401 em cada) |
| busca pelo proxy acha a nota | PASSA |
| rota de leitura: lê, não lista nem aceita gravação, `.md` igual | PASSA (8 ferramentas, só leitura) |
| rota do cliente: grava com a versão lida; versão velha = conflito; relida, grava | PASSA (3 casos) |
| instructions pelo proxy contra a instância direto (medida) | MEDIDA: **o proxy não repassa** (2019 caracteres direto; 0 pelo `/banco/mcp`) |
| regra curta nas 4 ferramentas de gravação pelo proxy | PASSA |
| kit de cliente lê o `AGENTS.md` pelo proxy | PASSA |
| ponte do Desktop gerada fala com o MCP do banco (stdio, npm cache no ensaio) | PASSA (12 ferramentas, com `write_note`) |
| `-Descer` para o proxy; com `-Manter`, sobe de novo | PASSA, PASSA |
| nenhum contêiner `hub-ensaio-22-*` sobrou (rodadas sem `-Manter` ou com falha) | PASSA |

**O que o achado do `instructions` quer dizer.** O TBXark/mcp-proxy 1.1.0 não leva o `instructions` do servidor de
trás ao cliente. Pelo proxy, o contrato não chega pelo MCP. Dois caminhos cobrem isso: o kit de cliente grava o
contrato no global de cada harness (lido por `read_note` pelo proxy, PASSA); e a regra curta vai na descrição das 4
ferramentas de gravação, que o proxy repassa (PASSA). Por isso o `--allow-all-mcp-server-instructions` do lançador do
Copilot não traz nada pelo proxy hoje; fica, sem custo, para um proxy que repasse.

**Memória** (medidor a cada 5 s, `etapas/logs/medidor-22.log`): pico de 715 MB livres às 09:41, com os dois pares, as
três instâncias, a busca e o proxy de pé; o corte do corredor é 700. vmmemWSL até 2,25 GB. CouchDB com 384 MB por
`docker update` (só no ensaio): 140 e 110 MiB depois da subida, 170 e 138 no fim.

**Voltas antes da verde** (todas descidas e limpas):
1. 08:14: o build do fork falhou; a worktree do fork estava sem o submódulo `lib/livesync-commonlib`. Iniciado.
2. 08:21: sobra da 1ª volta. Com `-Manter`, o teste não descia nada ao falhar. Conserto c95a265: com `-Manter`, a
   pilha só fica de pé se tudo passou. Achado junto: o passo 9 (`-Descer`) derrubava o proxy que os harnesses usam;
   agora ele sobe de novo.
3. 08:23: volume do CouchDB que sobrou da minha limpeza à mão (`docker rm -f` não leva volume).
4. 08:26: CORTADA pelo corredor (613 MB livres) na indexação da busca, com os pares de pé. Consertos (maestro e
   Vela): `wsl --shutdown` antes (`-Wsl` no corredor), a busca indexa antes dos pares (bfe6d6a), 384 MB por CouchDB
   (806898d).
5. 09:22: a busca indexou em 31 s, mas o teste lia "Indexing complete" só do stdout; a frase sai no stderr.
   Conserto bae29bd (lê os dois, como o `12-busca/servidor.mjs`).

### Harnesses de verdade como cliente

`HUB_HARNESS_REAL=1 node --test --test-concurrency=1 agents/code/test/ponta-a-ponta/22-cliente.test.mjs`, com a pilha
de pé (`-Manter`). 2026-10-17 09:47-09:48. Evidência: `agents/code/test/ponta-a-ponta/evidencia-22/` (83d4361).

| Harness | Modelo | Resultado |
|---|---|---|
| Claude Code | haiku | PASSA: `hub-busca` e `hub-banco` conectados; `search` e `read_note` pelo proxy; respondeu a nota marcada |
| Copilot CLI | haiku | PASSA: os dois conectados; `hub-busca-search` e `hub-banco-read_note`; respondeu a nota marcada |
| Codex | gpt-6-luna baixo (09:47) | FALHA por cota: "You've hit your usage limit ... try again at 12:15 PM". Roda de novo depois das 12h15 |

**Login no ensaio** (aval de 2026-10-16): copiados `.claude/.credentials.json` e `.codex/auth.json` e os campos de
login do `config.json` do Copilot para os HOMEs de ensaio em `%TEMP%`, às 12:47 UTC (09:47 local); apagados com a pasta
ao fim. Hashes antes e depois em `evidencia-22/hashes-claude-codex-copilot.json`: todos iguais, salvo
`~/.claude.json`, que as sessões abertas do Claude Code (os terminais do canvas) gravam o tempo todo; o ensaio usa
`CLAUDE_CONFIG_DIR` e não o toca (o mesmo no 15). A evidência não tem token nem pasta do usuário (conferido por
`grep`: só contadores de uso).

**Teste da cota do gpt-6-astra** (regra de ~10h20, depois corrigida pelo Gustavo: o Codex dos testes é o `gpt-6.1-sol`, 97693bb; o astra fica para revisão): um
`codex exec -m gpt-6-astra` de uma palavra numa casa de ensaio, 10:20 local. Copiado `.codex/auth.json` às 10:20:50,
apagado com a casa às 10:20:57; o hash do real ficou igual (`9e42496b5bd7...`). Deu o mesmo limite: o astra divide a
cota com o luna. O Codex como cliente roda depois das 12h15.

## Não verificado

- Na tailnet: latência, o grant da tag e o endereço Tailscale real em `HUB_PROXY_ADDR`. Fora desta construção.
- O Claude Desktop de verdade com a ponte: gerada, não instalada.
