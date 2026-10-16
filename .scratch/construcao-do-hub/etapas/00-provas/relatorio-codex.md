# Relatório da prova 3: hooks do Codex em acesso total (Vela, ticket 03)

Ramo `ticket-03` (worktree `C:\context-hub-wt\ticket-03`), da ponta de `integracao` (69cb383), com `integracao` juntada
de novo em b68f540 (ticket 04). A prova mora em `agents/code/test/provas/03-codex-hooks/` (regra nova do código). Codex CLI **0.162.1**
(a bancada usou 0.161.0). Modelo da prova: `gpt-6-luna`, esforço `low`, passados na linha de comando do teste.

## Resultado: passou

| Critério do ticket 03 | Resultado | Evidência |
|---|---|---|
| Em `codex exec` com acesso total e `CODEX_HOME` de ensaio, o hook de início injeta texto | **Passou** | o agente citou o código único que só o hook conhecia (vem de `.local/vigia/estado.json` do hub de ensaio) |
| O hook antes da ferramenta recusa um `apply_patch` que regrava arquivo existente | **Passou** | `Add File` sobre `nota-existente.md` recusado; o arquivo ficou igual, byte a byte |
| O hook de fim devolve ao agente e depois solta | **Passou** | `devolvido` (nota de retomada sem mudança), o agente fez a troca de trecho, e o hook deu `solto` com `nota_tocada: true` |
| O `notify` dispara | **Passou** | `agent-turn-complete`, mesma sessão, `client: codex_exec` |
| O login copiado foi apagado | **Passou** | `login-apagado.txt`: `…\codex-home\auth.json apagado=true` (cada rodada; a pasta de ensaio inteira também é apagada) |
| Acesso total de fato | **Passou** | o shell gravou `shell-ok.txt` no hub (nesta máquina o shell falha sob sandbox, ver bancada); evento com `permission_mode: bypassPermissions` |

Teste: `node --test agents/code/test/provas/03-codex-hooks/instalar.test.mjs agents/code/test/provas/03-codex-hooks/prova.test.mjs`
→ **8 de 8 verdes**: 3 da composição do instalador e 5 de ponta a ponta. Rodou verde 3 vezes com a versão
final do código dos hooks. Uma rodada intermediária falhou porque o modelo citou só o código, sem as palavras
"sync ok"; a afirmação passou a conferir o código único. Uma regra observada: o modelo varia o formato, e o teste
precisa conferir o dado, não a frase.

Sessão de uma rodada (`agents/code/test/provas/03-codex-hooks/evidencia/eventos.jsonl` guarda a última), em ordem: `inicio` (injetou) → `fim
marca` (UserPromptSubmit) → `antes` (recusa, `apply_patch`) → `fim devolvido` → `fim solto` (nota tocada) → `notify`.
Na pasta `evidencia/` também ficam: a saída JSONL do `codex exec`, o `config.toml` e o `hooks.json` do `CODEX_HOME` de
ensaio. Conferido: nenhum token ou credencial na evidência (busca por `access_token|refresh_token|id_token|api_key|bearer` = 0).

## O que foi construído (`agents/code/test/provas/03-codex-hooks/`, para as etapas seguintes)

- `instalar.mjs <CODEX_HOME> <HUB_ROOT>`: a forma que o kit (faixa 8) vai usar. Ele:
  - junta `fragmento.json` em `<CODEX_HOME>/hooks.json` por evento, sem apagar nada;
  - grava `sandbox_mode = "danger-full-access"` e `notify` no `config.toml`;
  - aprova **só os hooks do fragmento** pelo hash em `[hooks.state.'<chave>']`, com hash e chave lidos do app-server
    (`hooks/list`). Hooks alheios no mesmo `hooks.json` ficam com a confiança que tinham (conserto 1 do Fiel, rodada 1).
  - Idempotente: a segunda passada não muda nada. Três passadas sobre uma config com conteúdo alheio deixaram esse
    conteúdo intacto.
- `hooks/inicio.mjs` (SessionStart), `hooks/antes-da-ferramenta.mjs` (PreToolUse, `apply_patch`), `hooks/fim.mjs`
  (`marca` no UserPromptSubmit, `fim` no Stop) e `hooks/notify.mjs`. Node ≥ 22, `.mjs`, como as faixas 6, 7 e 9.
  Todos saem na hora fora de `HUB_ROOT`.
- `instalar.test.mjs`: a composição, só com o app-server (sem modelo, sem login). O `hooks.json` tem um hook alheio sem
  confiança e outro já confiado, e o instalador roda duas vezes. Resultado:
  - os 4 hooks do fragmento ficam `trusted`;
  - o alheio sem confiança continua sem, e sem linha no `config.toml`;
  - o alheio confiado continua confiado, com o mesmo hash.
- `prova.test.mjs`: o teste de ponta a ponta. Ele monta o hub de ensaio (com `.git`) e o `CODEX_HOME` de ensaio, copia
  só o `auth.json` e o apaga no `after`.

## O que vai doer ao ligar

1. **O `notify` é um só.** O `config.toml` real já tem um `notify`: o do Computer Use, `codex-computer-use.exe
   turn-ended`. O kit, como está aqui, o **substitui**. O kit de verdade precisa de um programa que chame os dois, ou
   então o Gustavo escolhe. Isso afeta a faixa 8 e a 7.
2. **O Codex regrava o `config.toml`.** Durante a prova, ele acrescentou `[projects.'…\hub'] trust_level = "trusted"`
   ao fim do arquivo, dentro do bloco marcado da minha primeira versão. Uma segunda passada teria apagado essa linha.
   Por isso o instalador edita por chave e por tabela, sem marcadores. A faixa 8 deve seguir assim. Limite: a leitura
   é por linha, e uma chave de topo em várias linhas (array quebrado) não é tratada.
3. **O hash aprova o comando, não o script.** Depois de mudar o conteúdo de `inicio.mjs`, o hash continuou o mesmo e o
   hook continuou `trusted`. A aprovação não protege o conteúdo do script. Ela muda se o comando ou o caminho mudar, e
   a chave inclui o caminho do `hooks.json`. Então:
   - `hooks.state` é por máquina e por pasta;
   - o kit precisa reaprovar sempre que mudar o `hooks.json`;
   - quem protege o script é o `.git` do hub, não o Codex.
4. **Acesso total deixa o shell fora da guarda.** O `PreToolUse` só cobre o `apply_patch`, e na prova o shell gravou
   onde quis. A recusa de regravação vale só para o caminho da ferramenta de patch. O resto fica no contrato (decidido
   no 14; a doc do Codex chama hook de "guardrail").
5. **O fim soltou com duas condições ao mesmo tempo.** No segundo `Stop` vieram `nota_tocada: true` e
   `stop_hook_active: true`. O hook dá prioridade à nota e registra as duas. Se o agente não tocar a nota, a guarda de
   segunda parada solta mesmo assim, para não prender o agente num laço. A faixa 2 decide se isso basta ou se precisa
   de aviso.
6. **Os caminhos são de ensaio.** Os comandos dos hooks apontam para a worktree. Na instalação, eles apontam para
   `C:\context-hub\…`, e os hashes mudam junto (item 3).
7. **Não coberto:**
   - o TUI interativo (só `codex exec`). No TUI, um hook sem aprovação abre a tela `/hooks`, como se viu no teste 11
     do ticket 14;
   - um terminal do Maestri;
   - o toast do Windows pelo `notify` (faixa 7);
   - a regra "não repetir o aviso enquanto o estado não muda";
   - `Update File` que troca o arquivo inteiro (faixa 6);
   - o teste do sandbox elevado a cada atualização (kit).
8. **Segunda máquina:** outro caminho de `CODEX_HOME` muda as chaves de `hooks.state`; o kit tem de rodar lá. Lá o
   sandbox elevado talvez funcione (não verificado), mas a decisão do 14 é acesso total nas duas.
9. **O modelo varia.** A prova depende de o agente seguir o pedido. Ela ficou estável conferindo dados (código, eventos,
   arquivos), não frases.

## O que muda no spec

Nada de decisão. O "não verificado: hooks do Codex com acesso total" (ticket 14, Answer, e "Pontos abertos" do spec)
passa a **verificado**, nesta máquina, na 0.162.1, em `codex exec`. Os itens 1 a 3 acima entram como requisitos do
kit (faixa 8).

## Limpeza

- Login: copiado só `%USERPROFILE%\.codex\auth.json`, a cada rodada, para o `CODEX_HOME` de ensaio. Em todas as
  rodadas ele foi apagado no `after`, junto com a pasta de ensaio (`%TEMP%\hub-ensaio-03-*`). Conferido: nenhuma pasta
  `hub-ensaio-03-*` sobrou.
- Globais: nada gravado em `~/.codex`. `config.toml` (2026-10-15 14:31), `hooks.json` (2026-09-21) e `auth.json`
  (2026-10-15 11:41) mantêm datas anteriores à prova.
- Nenhum contêiner nesta prova. Os rascunhos do scratchpad foram apagados.

## Estado

- 2026-10-16: parado antes a pedido do processo; depois retomado como ticket 03.
- 2026-10-16 ~22h10: 5 de 5 verdes, commits até a14d996. Pedida a revisão do Fiel.
- 2026-10-16 ~22h20: rodada 1 do Fiel = volta (conserto 1: o instalador aprovava hooks alheios). Consertado com teste:
  o vermelho foi reproduzido, e depois o verde veio 4 vezes.
  - A pasta de ensaio às vezes fica presa por instantes no Windows (EPERM ao apagar, sem processo do Codex vivo). A
    limpeza tenta de novo por até 10 s.
  - Prova movida para `agents/code/test/`; hub de ensaio com `initiatives/`; `integracao` juntada (b68f540).
  - 8 de 8 verdes depois do merge e da mudança de lugar. Commits até f4bb98b. Pedida a rodada 2.
- 2026-10-16 ~22h30: rodada 2 do Fiel = passa. Maestro avisado.
