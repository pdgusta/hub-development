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

### Rodada 2, ramo refeito — 2026-10-17 ~11h05
Por ordem do maestro, o `ticket-22` voltou a 5abe359 (o conserto, sem o merge do 16, que o Rebite desfez em
`integracao`; a ponta de `integracao` agora é e98a891 e o ramo a contém). Diferença para 63cbfd5 em `agents/code/kit`:
só `banco.psm1` e `04.env.modelo`, do 16, que o proxy não usa. Fiel: 10/10 de novo, `git status` limpo. **PASSA**
continua.

## Leitura do Fielzinho — rodadas 1 e 2 — 2026-10-17

Conferidos ticket, relatório, proxy, kit cliente e testes. Worktree c1f0fa3; núcleo do 22 sem mudança desde 5abe359. Prova própria: 22-kit-cliente + 22-proxy-sem-docker, **4/4, saída 0**, 54,9 s; árvore limpa. O conserto do hash dos tokens funciona: teste cobre token antigo recusado, novo aceito, rota de leitura preservada. Docker apenas lido em logs/22-docker.log (15 PASSA); lido.json de Claude/Copilot confirma search e read_note, Codex registra cota, não aceite. Nenhum Docker/harness real próprio.

### Achado novo 1 — kit cliente apaga tabela alheia inserida no bloco TOML

`agents/code/kit/cliente/ligar-cliente.ps1:105-115` ainda substitui tudo entre comentários hub-cliente. A lição 2 da prova 03 (`00-provas/relatorio-codex.md:54-56`) já registrou que o Codex insere a tabela projects dentro do bloco marcado e exigiu edição por chave/tabela. No cliente, a passada seguinte apaga essa configuração alheia.

Repro própria `logs/repro-22-fielzinho.mjs` e `.log`: instala numa casa de ensaio, insere `[projects.ensaio]` com trust_level antes do comentário final (a forma observada na prova 03), roda o kit de novo: tabela_alheia_antes=true; tabela_alheia_depois=false. Saída 0, TEMP apagado; não abriu harness. A inserção foi simulada com base na evidência anterior, não observada novamente no Codex atual.

Recomendo trocar somente as tabelas MCP pertencentes ao kit, preservando projects e outras tabelas; teste de repetição depois da inserção. Como o 22 já foi juntado, encaminhar ao maestro pelo construtor. Não alterei ticket, código ou veredito fechado; o resultado desta leitura é achado adicional para decisão do Fiel.

### Fiel sobre a leitura do Fielzinho (~13h00)
- Achado novo 1 **aceito** (conferido: `ligar-cliente.ps1:105-115` troca tudo entre `# hub-cliente:inicio` e
  `# hub-cliente:fim`; a lição 2 da prova 03, `00-provas/relatorio-codex.md:54-56`, diz que o Codex grava
  `[projects.'…'] trust_level` no fim do `config.toml`, dentro do bloco, e que a faixa 8 edita por chave e por tabela).
  O bloco do kit é sempre o último do arquivo, então a tabela do Codex cai dentro dele, e a passada seguinte a apaga.
- O 22 já está juntado: **a Brasa leva ao maestro** (conserto em ticket novo ou de manutenção: trocar só as tabelas
  `mcp_servers.hub-*` por tabela, como o instalador da faixa 8; teste de repetição depois da inserção).
- Acordo: o passa da r2 fica, com este achado em aberto fora do ticket.

## Rodada curta da manutenção (achado do Fielzinho) — 2026-10-17 ~13h40 (Fiel sozinho; Fielzinho sem cota até 17h15)

Ramo `ticket-22`, ponta f6ac76d (7732617 + `integracao` e7203b4). **Veredito: PASSA.**
- `ligar-cliente.ps1`: sem bloco marcado; o `config.toml` é lido em topo e tabelas, e só as `[mcp_servers.hub-*]`
  são trocadas; os marcadores antigos saem. Teste novo no `22-kit-cliente` (Codex acrescenta `[projects]`; formato
  antigo com a tabela dentro do bloco).
- Sonda do Fiel (casa em `%TEMP%`, apagada): formato antigo com `[projects.'C:\velho']` dentro do bloco, mais
  `[mcp_servers.outro]` fora; kit; depois um `[projects]` novo no fim; kit duas vezes: o topo (`model`, `notify`), as
  duas `[projects]` e o `outro` ficam; as `hub-*` saem do lugar velho e vão ao fim, em dia. A repro do Fielzinho dá
  `antes=false` (o marcador onde ela inseria não existe mais).
- Fiel: `22-kit-cliente + 22-proxy-sem-docker + harness-real` 11/11; `git status` limpo; nenhum `mcp-proxy` de pé.
- Ressalva (a mesma da prova 03): a leitura é por linha; uma linha de valor em várias linhas que comece por `[`
  (array aninhado) seria lida como tabela.
- O Codex como cliente segue para depois das 17h15.

## Rodada curta: evidência do Codex como cliente — 2026-10-17 ~18h30 (Fiel + 2ª leitura Opus)

Ramo `ticket-22`, ponta 22811cb (só `evidencia-22/codex/` e `hashes-codex.json` sobre `integracao` f640bbd).
**Veredito: PASSA, em acordo com a 2ª leitura** (`parecer-22-Brasa-segunda-leitura.md`). Sem conserto.
- Modelo: o teste chama `-m MODELO_CODEX` (`22-cliente.test.mjs:102`); `harness-real.mjs:9` = `gpt-6-luna`; o
  corredor não põe `HUB_MODELO_CODEX`.
- Evidência: o Codex chamou `hub-busca/search` e `hub-banco/read_note` pelo proxy; resposta com a nota e a palavra
  rara. Log `logs/22-harness.log` 1/1; `22.status`: trava 17:14:38–17:19:20, 0 contêiner sobrando.
- Login: `auth.json` copiado 20:18:48Z, apagado 20:18:59Z. Hashes reais iguais; só `~/.claude.json` mudou (sessões
  abertas). Grep de token e de usuário: nada.
- Fiel: `22-kit-cliente + 22-proxy-sem-docker + harness-real` 14/14; `git status` limpo.
- Ressalva (2ª leitura): a evidência não grava o modelo; para o radar, pôr `MODELO_CODEX` no `lido.json`.
