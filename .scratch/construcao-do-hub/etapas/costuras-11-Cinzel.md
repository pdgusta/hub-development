# Ticket 11: costuras propostas (Cinzel, 2026-10-17 ~06h45)

Worktree do hub: `C:/context-hub-wt/ticket-11`, ramo `ticket-11` da ponta de `integracao` 9cc878b. No fork, nenhuma
mudança prevista. Só uma worktree `ticket-11` da `integracao` do fork (34c3e50), para ter um `dist` montado com o 10.

## Costura única: o aceite com os harnesses de verdade

`agents/code/test/ponta-a-ponta/11-mcp-banco.test.mjs`. Segue o molde do `12-busca.test.mjs`: `comHarness` (pulado
sem `HUB_HARNESS_REAL=1`), HOME de ensaio por harness, login copiado e apagado a cada rodada, hashes das pastas reais
antes e depois, e evidência sem login em `evidencia-11/<harness>/`.

**Montagem:**
- Um hub de ensaio do `montar.mjs`, com três marcas aleatórias:
  - **A**, no começo da cabeça do `AGENTS.md`;
  - **B**, no fim dela (a cabeça segue abaixo de 2.000 caracteres; hoje tem 1.691);
  - **C**, no `resumo` de um `.local/vigia/estado.json` de exemplo.
- O fork roda direto (`node dist/main.js`) em 127.0.0.1, numa porta livre, com token. `HUB_ROOT` é o hub de ensaio.
  O nome do servidor nos harnesses é `hub-banco`, com bearer token:
  - Claude Code: `headers` no `.claude.json`;
  - Codex: `bearer_token_env_var`;
  - Copilot: `headers` no `mcp-config.json`.
- **O harness roda fora do hub**, numa pasta vazia. Senão, o Codex e o Copilot leem o `AGENTS.md` do diretório e a
  marca chegaria pelo arquivo, não pelo servidor.
- Um pedido igual para todos, sem shell, sem ler arquivo e sem rede. O harness responde num JSON:
  1. a linha com a marca do começo e a do fim das instruções que o servidor `hub-banco` mandou, ou `NAO-RECEBI`;
  2. o começo da descrição do `write_note` do `hub-banco`;
  3. chamar `estado_do_hub` e copiar o `resumo`.
- Só `estado_do_hub` vai aprovada. As ferramentas de gravação ficam visíveis, para a descrição chegar, mas sem
  aprovação: o `-p` ou o `exec` recusa a chamada.

**O que o teste afirma, e o que só registra:**

| Harness | Afirma | Registra (medida, na evidência e no relatório) |
|---|---|---|
| Claude Code (`claude -p`, haiku) | marcas A e B citadas (as instruções chegam, inteiras até o fim da cabeça); C citada | a regra curta citada ou não (o Claude Code adia as ferramentas MCP, a "busca de ferramentas adiada" do spec) |
| Codex (`codex exec`, gpt-6-luna baixo) | C citada; **a requisição capturada** contém A, e o teste diz em que campo ela vai (instruções do sistema, descrição do grupo de ferramentas ou da ferramenta) | A e B citadas ou não; a regra curta |
| Copilot CLI (`copilot -p`, haiku), **duas sessões** | com `--allow-all-mcp-server-instructions`: A e B citadas, e C; sem a opção: C citada | sem a opção: A citada ou não (a doc diz que só vão as de servidores da lista permitida); a regra curta nas duas |

A regra curta é conferida pelo começo "Antes de gravar, leia `AGENTS.md`". A cabeça tem "Conflito: releia e refaça",
então só esse começo prova que a descrição chegou.

**Captura do Codex:** um proxy local de registro em 127.0.0.1, que repassa ao endereço de verdade e guarda o corpo da
requisição sem o cabeçalho de autorização. O Codex aponta para ele pelo `openai_base_url` do `config.toml` de ensaio
(doc: "Base URL override for the built-in `openai` provider"). A dúvida: com login do ChatGPT, se o Codex respeita
esse campo para o endereço do backend do ChatGPT. Confiro na 1ª rodada do Codex. Se não respeitar, a reserva é um
provedor próprio (`model_providers.<id>` com `base_url` e `requires_openai_auth`); se nada servir, volto ao maestro.

## Escolhas para o maestro

1. **O banco de trás:** o fork em modo local (`VAULT_PATH` = o hub de ensaio), ou o par do 07 com CouchDB (Docker).
   **Recomendo o modo local.** O ticket mede o que chega a cada harness: cabeça, descrições e estado são o mesmo código
   nos dois modos, e a gravação com versão sobre o CouchDB já foi provada no 09 e no 10. Com Docker, seriam dois
   trabalhos pesados ao mesmo tempo (Docker e harness), numa máquina com a memória no limite.
2. **Duas sessões do Copilot** (com e sem a opção): o ticket pede as duas, e as regras dizem "uma sessão por
   harness". Peço o aval para as duas.
3. **Fora:** a "regra seguida" do spec (pedir uma regravação inteira e ver se o agente leu o `AGENTS.md`) e o banco
   recriado no meio da sessão não estão nos critérios do ticket 11. Ficam fora, salvo pedido.

## Sem harness, na suíte comum

Uma parte pura e testável sem harness, com teste em `node --test` comum, sem trava:
- o proxy de registro: repassa e guarda, sem o `Authorization`;
- a leitura de cada saída: acha as marcas e o campo da requisição do Codex.
