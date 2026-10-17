# Parecer do ticket 23 (Cinzel): kit de par, a forma (esqueleto)

## Rodada 1 — 2026-10-17 ~09h30 (ramo ticket-23, ponta e9dcef7, com integracao e98a891)

Veredito: **VOLTA**, por 1 conserto. Fiel sozinho (Fielzinho sem cota até 12h15; leitura dele pendente). Junção só com
11, 15, 17, 18, 20 e 27 resolvidos (mandato).

### Conferido pelo Fiel

- Árvore limpa antes e depois. `node --test agents/code/test/23-kit.test.mjs`: 13/13 (3 min 26 s). Sem sobra
  `hub-ensaio-23-*` nem `hub-kit-codex-*` em `%TEMP%`.
- **Nada global:** hashes das configurações reais antes e depois do teste (`~/.claude/settings.json`, `CLAUDE.md`,
  `~/.codex/config.toml`, `hooks.json`, `AGENTS.md`, `~/.copilot/config.json`, `mcp-config.json`,
  `copilot-instructions.md`) iguais; listagens de `~/.claude/skills`, `~/.agents/skills`, `~/.copilot/hooks` sem
  mudança de entrada (só o mtime de `~/.claude`, pelas sessões abertas: history, sessions, backups).
- Lidos `instalar.ps1`, `casa.mjs` e `08-harnesses.mjs`: recusa sem `-Casa`/`HUB_HOME_ENSAIO`; `caminho()` recusa
  fora da casa; mover para a cópia antes de tocar; desfazer em ordem inversa, parando se algo mudou depois do kit;
  contrato por link (Codex, Copilot) e import (Claude); junction só das skills com `metadata.camada: geral`; token do
  banco só por variável; GSD tirado pelo manifesto; `hooks.state` com hash do app-server numa cópia.

### Consertos

1. **(Fiel) A junção dos hooks nunca tira o grupo antigo do hub: fragmento que muda duplica o hook.** `juntarHooks`
   (`08-harnesses.mjs`) só acrescenta o grupo que não é igual. Quando um fragmento do hub muda entre passadas
   (atualização do hub; os hooks de 17 e 18 entrando pela "passada seguinte", que é a costura do próprio ticket), o
   grupo velho fica e o novo entra: o hook roda duas vezes (no fim da resposta, dupla devolução; na leitura, aviso
   duplo). Peça tirada do hub deixa hook apontando para pasta que não existe.
   - Sonda (hub do `montar.mjs` com `agents/`, casa de ensaio, `-Passos 08`): 1ª passada, `hooks/leitura/depois` uma
     vez em `.claude/settings.json` e `.codex/hooks.json`; trocado `"timeout": 10` por `15` nos fragmentos `claude` e
     `codex` da leitura; 2ª passada: **duas vezes** em cada. Sonda apagada.
   - Conserto: antes de juntar, tirar os grupos do hub (comando dentro de `<hub>/agents/code/hooks/`) que não estão nos
     fragmentos atuais, e as aprovações `hooks.state` deles; os alheios ficam. Teste: fragmento mudado e peça tirada,
     segunda passada com um grupo só e sem o da peça tirada.

### Ressalvas (não seguram; para o 26)

1. **Desfazer no HOME real:** o desfazer recusa caminho que mudou depois do kit. O Claude regrava `~/.claude.json` a
   cada sessão e o Codex regrava o `config.toml` (lição 2 do 03): no HOME real, o desfazer vai quase sempre parar
   nesses dois. No 26, desfazer por chave (tirar o que o kit pôs) nos arquivos que o harness regrava.
2. As ressalvas 1 a 6 do relatório (mod, extensão, `statusLine`, `notify` composto; `hooks.state` alheio que muda de
   índice; tabelas do GSD no `config.toml`; XML não validado pelo Agendador; como os harnesses enxergam a casa; pontos
   abertos do spec). Em particular: o kit não tem como ligar `--allow-all-mcp-server-instructions` do Copilot por
   arquivo (doc lida pelo Cinzel); quem abre o Copilot passa a opção (24, 26).

## Rodada 2 — 2026-10-17 ~10h10 (HEAD f304e6c)

Veredito: **PASSA** (Fiel sozinho; Fielzinho sem cota até 12h15, leitura pendente). Junção só com os bloqueios
resolvidos.

- Conserto 1 feito: `juntarHooks` tira antes o grupo do hub (comando em `<hub>/agents/code/hooks/`) que não está nos
  fragmentos atuais; tira o `hub-<peça>.json` órfão do Copilot; das aprovações `hooks.state` deste `hooks.json` fica
  só a que ainda casa hook e hash. Alheios ficam.
- Sonda da r1 repetida, com um hook alheio no `settings.json`: 1ª passada, leitura uma vez; fragmento da leitura
  mudado, 2ª e 3ª passadas, leitura **uma vez** no Claude e no Codex; alheio mantido; desfazer volta a casa e apaga o
  `.hub-kit`. (A peça tirada vai pelo teste novo do Cinzel; neste ramo não há a pasta da vigia.)
- `23-kit.test.mjs`: 14/14 (Fiel). Hashes das configurações reais e listagens das pastas globais iguais antes e
  depois; sem sobra em `%TEMP%`; árvore limpa.
- Ressalva do desfazer para o 26: anotada pelo Cinzel.
