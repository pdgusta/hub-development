# Parecer do ticket 22 (Brasa): proxy e kit de cliente

## Rodada 1 — 2026-10-17 ~10h30 (Fiel sozinho; Fielzinho sem cota até 12h15, leitura dele pendente)

Ramo `ticket-22` (worktree `C:/context-hub-wt/ticket-22`), HEAD 3894a42 (evidência 83d4361). `integracao` andou pela
junção do 16 (fce0529); merge sem conflito (`git merge-tree`).

**Veredito: VOLTA** (1 conserto). O Codex como cliente segue pendente (cota), como o maestro aceitou.

### Consertos

1. **Trocar um token no `.env` e rodar o passo 10 de novo não tem efeito: o token velho segue valendo** (Fiel).
   `proxy.psm1`, `Start-Proxy`: com o PID de pé e o `config.json` igual, devolve "de pé" e não religa. Mas os tokens
   não estão no config (só `${VAR}`); estão no ambiente do processo, lido na partida. Logo, mudar só o token nunca
   muda o config, e o proxy segue com o token antigo.
   Sonda (cópia do `22-proxy-sem-docker.test.mjs` com um passo a mais, apagada depois): depois da 2ª volta, troquei
   `HUB_PROXY_TOKEN_BANCO_ESCRITA` no `par.env` e rodei o passo: saída 0, "proxy de pé", mesmo PID; token velho →
   **200**; token novo → **401**.
   É o caminho de tirar a gravação de um cliente (o `.env.modelo` diz "o de banco-escrita só quando o Gustavo ligar"):
   revogar não revoga. O mesmo vale para os tokens das instâncias (`HUB_MCP_BANCO_*_TOKEN`) trocados no passo 05: o
   proxy segue mandando o velho e as rotas passam a dar erro de trás.
   Conserto: religar quando o ambiente mudar (por exemplo, guardar na pasta de estado um hash dos tokens da partida e
   comparar), com um caso de teste: troca de token → o velho dá 401 e o novo abre.

### Ressalvas (não bloqueiam)

- **Junção com o 21:** o 21 (Trilho) e o 22 criam o mesmo arquivo novo `agents/code/kit/par/env/10.env.modelo`, com
  conteúdos diferentes (o 21: `HUB_MAQUINA`, `HUB_COPIA_*`; o 22: `HUB_PROXY_*`). Quem juntar depois terá conflito
  add/add; as duas metades têm de ficar. Aviso ao Rebite junto com o passa.
- O lançador `copilot-hub.cmd` passa `--allow-all-mcp-server-instructions`, que hoje não traz nada pelo proxy (achado
  medido); está escrito no relatório.

### Conferido sem conserto

- Aceite 1: busca pelo proxy acha a nota; rota de leitura lê e recusa a gravação, `.md` igual (Docker).
- Aceite 2: rota do cliente grava com `base_rev`, conflito com versão velha, relida grava; sem token e com o de outra
  rota, 401 nas três (Docker e sem Docker).
- Aceite 3: o Host que chega à busca é o endereço dela (sem Docker, MCP falso); busca real pelo proxy no Docker.
- Aceite 4: medido; o proxy não repassa o `instructions` (2.019 direto, 0 pelo proxy). Limite aceito pelo maestro
  (09:49).
- Nenhum token em arquivo (config, ponte, kit); o token da ponte do Desktop fica só no `banco.headers` da pasta de
  estado. Claude e Copilot como cliente: evidência em `ponta-a-ponta/evidencia-22/`, hashes do real iguais.

### Evidências

- `node --test agents/code/test/22-kit-cliente.test.mjs agents/code/test/22-proxy-sem-docker.test.mjs
  agents/code/test/harness-real.test.mjs` (detector do 29): 10/10. `git status` limpo; nenhum `mcp-proxy` de pé.
- `logs/22-docker.log`: 15 PASSA, 0 FALHA, medidas conferidas linha a linha.

## Rodada 2 — 2026-10-17 ~10h55 (Fiel sozinho; leitura do Fielzinho pendente)

Ramo `ticket-22`, HEAD 63cbfd5 (conserto 5abe359 mais `integracao` fce0529 juntada).

**Veredito: PASSA.** O aceite dos harnesses segue pendente só do Codex (depois das 12h15, rodada curta de evidência).

- Conserto 1 feito: `Start-Proxy` guarda `ambiente.sha256` (hash dos tokens da partida, nunca o token) e religa
  quando o hash muda; `Stop-Proxy` apaga o hash. Teste novo no `22-proxy-sem-docker`: token trocado → velho 401,
  novo 200, leitura segue; nenhum arquivo do `mcp-proxy/` tem token.
- Fiel: `22-kit-cliente + 22-proxy-sem-docker + harness-real` 10/10; `git status` limpo; nenhum `mcp-proxy` de pé.
- Sem Docker de novo: a mudança é só na decisão de religar, coberta pelo teste sem Docker; o Docker verde (bae29bd)
  segue valendo para o resto.
- Ressalva do `10.env.modelo` (add/add com o 21) segue: levar ao Rebite.
