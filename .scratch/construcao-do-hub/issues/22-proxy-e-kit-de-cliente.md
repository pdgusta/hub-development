# 22: Proxy e kit de cliente

Type: task
Status: resolved
Etapa: 9 (manutenção e cliente)
Blocked by: 10, 12

**What to build:** O proxy de MCP do par com uma rota e um token por servidor (busca, banco de leitura, banco de escrita do cliente) e o kit de cliente, tudo em 127.0.0.1 no lugar da rede privada. A ponte do Claude Desktop e a pasta conectada geradas, sem instalar.

**Fonte:** Bloco do Worker 10, itens (e) e (f); tickets 34, 36, 14, 11; escolha aceita 23. Regras comuns: `../etapas/regras-da-construcao.md`.

**Blocked by:** 10 (MCP do banco: três instâncias, cabeça, regra curta e estado), 12 (Busca local com aceite)

- [ ] um cliente de ensaio busca pelo proxy, lê pela rota de leitura e tem a gravação recusada nela
- [ ] grava pela rota do cliente com a guarda de versão; sem token leva recusa
- [ ] a busca aceita o endereço que o proxy de fato repassa
- [ ] mede se o proxy repassa o `instructions`

## Comments
- 2026-10-16 23h10 (integrador, Rebite): lição do ticket 12 (parecer do Fiel, `etapas/parecer-12-Trilho.md`): `agents/skills/busca/iniciar.ps1` não passa `--allowed-host`; quando a busca for servida pelo proxy, o Host observado precisa entrar (spec, Worker 3). O servidor da busca também faz `GET registry.npmjs.org/.../latest` a cada partida.

- 06:38 (maestro): abre com o 10 juntado (9cc878b); vai ao primeiro construtor livre (provável: o Trilho, depois do 16).

- 06:50 (maestro): passado à Brasa (o 10 está juntado em 9cc878b; o 12 resolvido).
- 2026-10-17 ~07h20, Brasa: peguei (Status claimed). Worktree `C:/context-hub-wt/ticket-22`, ramo `ticket-22`, de `integracao` 9cc878b. Costuras propostas ao maestro (aguardo): (1) passo do par `agents/code/kit/par/10-proxy.ps1` + `proxy/proxy.psm1`: baixa o TBXark/mcp-proxy v1.1.0 (Windows, SHA-256 conferido) para a pasta de estado do par, gera o config v2 (`addr` 127.0.0.1:<HUB_PROXY_PORTA>, rotas `busca`, `banco`, `banco-escrita`, streamable-http, um token por rota e os tokens das instâncias por `${VAR}` do ambiente, nunca no arquivo), sobe e confere pelo `/_readyz`; idempotente e `-WhatIf`. (2) kit de cliente `agents/code/kit/cliente/ligar-cliente.ps1`: grava no HOME de ensaio a linha de MCP dos três harnesses com `Authorization: Bearer` de variável, `--allow-all-mcp-server-instructions` no Copilot, `default_tools_approval_mode="approve"` no Codex, o contrato na configuração global; só leitura por padrão, `-Escrita` liga a terceira rota; e gera (sem instalar) a ponte `mcp-remote` do Claude Desktop e as "Folder instructions" da pasta conectada. (3) testes: sem Docker (`22-kit-cliente`, entra na suíte: arquivos gerados, nenhum token em arquivo, idempotente, nada fora do HOME de ensaio); com Docker e trava `agents/code/test/22-proxy.test.ps1`: par de ensaio do 07, passo 05 com as três instâncias, busca real, passo 10, e um cliente HTTP de ensaio pelo proxy (busca; leitura; gravação recusada em `/banco/mcp`; gravação com `base_rev` e conflito com versão velha em `/banco-escrita/mcp`; sem token e com token de outra rota, 401; o `Host` que chega à busca registrado; o `instructions` e a regra curta medidos pelo proxy contra a instância direta). (4) a perguntar: os três harnesses de verdade como cliente (spec), com a trava e o aval de login.

- 07:01 (maestro, mandato): costuras da Brasa aceitas (passo 10-proxy com o TBXark/mcp-proxy v1.1.0 do spec, SHA-256 conferido, em 127.0.0.1; kit de cliente no HOME de ensaio; testes sem e com Docker). (4) sim: os três harnesses de verdade como cliente, uma sessão de cada, modelos baratos, com a trava e o aval de login, depois do Docker verde.
- 2026-10-17 ~08h, Brasa: sem Docker verde: kit de cliente (`agents/code/kit/cliente/ligar-cliente.ps1`) e passo 10 do par (`agents/code/kit/par/10-proxy.ps1`, TBXark/mcp-proxy 1.1.0 com SHA-256) com a ponte do Desktop gerada; testes `22-kit-cliente.test.mjs` e `22-proxy-sem-docker.test.mjs`. Falta: o teste Docker `22-proxy.test.ps1` (trava), os harnesses reais e o relatório.

- 08:29 (maestro, mandato): Docker do 22 cortado pela memória (613 MB) na indexação da busca, com pares e MCP de pé. Liberado: `wsl --shutdown` na vez dela (com a trava e sem contêiner) e indexar a busca antes de subir os pares. Se cortar de novo, vira item do Gustavo.

- 09:49 (maestro, mandato): Docker verde na janela quieta (15/0, bae29bd); Claude e Copilot como cliente passam; Codex depois das 12h15. Achado: o TBXark/mcp-proxy **não repassa o `instructions`** (2.019 caracteres direto, 0 pela rota `/banco/mcp`); a regra curta nas descrições das 4 ferramentas chega. Aceito como limite conhecido: o cliente recebe o contrato pela regra curta e pela configuração global que o kit de cliente grava; consertar o proxy (ou trocar) fica para o radar. Pico de memória: 715 MB livres (corte 700); CouchDB com 384 MB usou 140-170 MiB.
- 2026-10-17 ~09h55, Brasa: Docker VERDE na janela quieta (09:39, ponta bae29bd): 15 PASSA, 0 FALHA. Medido: o proxy não repassa o `instructions` (2019 caracteres direto, 0 pelo proxy); o contrato chega pelo kit de cliente e a regra curta pelas ferramentas. Harnesses como cliente: Claude e Copilot PASSA; Codex só por cota (de novo depois das 12h15). Pico de memória 715 MB livres. Evidência 83d4361; relatório `etapas/relatorio-22-proxy-e-kit-de-cliente.md`. Falta: o Codex depois das 12h15 e a revisão.
- 2026-10-17 ~11h, Brasa: r1 do Fiel VOLTA por 1 conserto (o proxy não religava com token trocado); feito (hash do ambiente da partida, teste novo). r2 PASSA (parecer `etapas/parecer-22-Brasa.md`), ponta 63cbfd5 (depois 5abe359, sem o 16), 10/10 sem Docker. Pendente: o Codex como cliente depois das 12h15 (rodada curta do Fiel) e a leitura do Fielzinho. Ressalva para a junção: o 21 também cria `agents/code/kit/par/env/10.env.modelo` (add/add; as duas metades ficam).

- 10:42 (maestro): r2 do Fiel passa (63cbfd5). Vai ao Rebite já; a evidência do Codex entra depois (rodada curta). O `10.env.modelo` nasce também no 21: o segundo a juntar resolve no próprio ramo.
- 2026-10-17 11h21 (integrador, Rebite): juntado em `integracao`, commit 4a47576 (merge `--no-ff` de `ticket-22` 5abe359). O parecer da rodada 2 do Fiel ("passa") conferiu 63cbfd5, que é 5abe359 mais a junção do 16 (fce0529), desfeita na `integracao` por vermelho no 12-busca; a Brasa tirou o 16 do ramo, e 5abe359 só difere de 63cbfd5 nos arquivos do 16 (conferido por `git diff --name-only`). Testes: `22-kit-cliente` e `22-proxy-sem-docker` 4/4 (log `etapas/logs/juncao-22-leves.log`); suíte `node --test --test-concurrency=1 "agents/code/test/**/*.test.mjs"` sem variáveis, com a trava: 215, 206 verdes, 9 pulados, 0 falhas, `git status` limpo (log `etapas/logs/juncao-22-suite.log`). Docker e harnesses não repetidos: arquivos do 22 idênticos aos revisados (Docker verde bae29bd, `etapas/logs/22-docker.log`; Claude e Copilot passam). **Pendente (maestro, como no 08):** o Codex como cliente depois das 12h15, em commit só de evidência com rodada curta do Fiel; a leitura do Fielzinho. Ressalvas do parecer: `10.env.modelo` add/add com o 21 (quem juntar depois deixa as duas metades: o 21 já fez, 6b6c65e); o `copilot-hub.cmd` passa `--allow-all-mcp-server-instructions`, que hoje não traz nada pelo proxy; o proxy não repassa o `instructions` do MCP (2.019 direto, 0 pelo proxy; limite aceito pelo maestro às 09:49). **Resolvido.**

- 12:39 (maestro, mandato): achado do Fielzinho (aceito pelo Fiel): o kit de cliente troca inteiro o bloco `hub-cliente` do `config.toml` do Codex e apaga o `[projects.*] trust_level` que o Codex grava no fim. Conserto no próprio ramo como manutenção (trocar só as tabelas `[mcp_servers.hub-*]`, teste de repetição), junto com a evidência do Codex; rodada curta do Fiel.
