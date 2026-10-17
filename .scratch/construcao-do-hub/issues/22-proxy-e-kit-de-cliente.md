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
