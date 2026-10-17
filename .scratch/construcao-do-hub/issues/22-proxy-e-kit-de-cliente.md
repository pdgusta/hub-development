# 22: Proxy e kit de cliente

Type: task
Status: claimed
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
