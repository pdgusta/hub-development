# Bancada de gravação — Codex / apply_patch e PreToolUse

Rodada refeita do começo em 15/10/2026, aproximadamente 15:25–15:27 (São Paulo). Executor: Sonda Codex. Escopo exclusivo: `C:\Projetos\bancada-acesso\gravacao\codex\`. Codex CLI **0.161.0**, modelo `gpt-6-luna`, esforço `low`, sem subagentes. Brief e contexto da pergunta 1 lidos no caminho corrigido sob `.scratch\context-hub\portal\rodadas\`.

**Resultado principal:** `Update File` parcial preservou a alteração externa em outra linha e recusou uma alteração incompatível no próprio trecho. **`Add File` sobre um arquivo existente sobrescreveu a alteração externa sem recusar.** O hook de projeto bloqueou as formas de regravação inteira testadas e permitiu o patch parcial e o arquivo novo. Tudo rodou com `workspace-write` e `windows.sandbox="unelevated"`; não foi necessário acesso total.

## Método e ordem comprovada

Cada nota existente começou com:

```text
titulo: teste
alvo: antigo
outra: antiga
```

O agente executou **uma leitura real** por `exec_command`, com `Get-Content` dos nove arquivos existentes. O shell retornou as três linhas originais de cada nota, com sucesso em 1327 ms. Depois o agente chamou `apply_patch` dez vezes separadamente, com patches fixos, sem reler, adaptar ou repetir uma tentativa recusada. O décimo arquivo ainda não existia na leitura.

Um script Python separado, acionado pelo hook `PreToolUse`, alterou cada arquivo imediatamente antes de sua primeira tentativa de patch: `outra: antiga` → `outra: externa`, exceto no caso 2, em que alterou `alvo: antigo` → `alvo: externo`. O script registrou a entrada completa da ferramenta e o conteúdo antes/depois da mudança externa. Nos casos 1–3 ele apenas sincronizou a mudança externa, sem veto; nos arquivos `h-*`, também aplicou a política de bloqueio. Assim a mudança externa ocorreu depois da leitura e antes da verificação/aplicação da ferramenta.

O hook ficou em `gravacao\codex\.codex\hooks.json`, com camada local `config.toml`. O `hooks/list` confirmou origem **project**. Os hashes foram confiados por `-c hooks.state`, apenas na invocação. Nenhuma aprovação persistida foi alterada. `BANCADA_GRAVACAO=1` ativou o teste; `BANCADA_FIM=0` deixou desligado o hook de retomada da bancada anterior.

Para evitar o alias inacessível do PowerShell sob WindowsApps encontrado na pesquisa anterior, retirei entradas `WindowsApps` do **PATH do processo filho somente**. A leitura usou `C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe`. Essa diferença de ambiente está em `run.py`; não mudou PATH global, perfil ou configuração de usuário.

## Tabela caso × ferramenta

A coluna de disco mostra **todo o conteúdo final**, na ordem `titulo / alvo / outra`; `titulo: teste` permaneceu em todos os casos. “Passou” na coluna de gravação significa que a ferramenta aceitou o patch; isso pode representar falha da proteção contra perda de alteração.

| Caso / arquivo | Operação apply_patch | Conteúdo final no disco: titulo / alvo / outra | Resposta real da ferramenta | Resultado |
|---|---|---|---|---|
| 1 — `c1-parcial.md` | `Update File`, só troca `alvo: antigo` | `teste / novo / externa` | `patch: completed` | **Gravação passou**; alteração externa preservada |
| 2 — `c2-conflito.md` | Mesmo patch parcial, alvo mudou externamente | `teste / externo / antiga` | `apply_patch verification failed: Failed to find expected lines` (`alvo: antigo`) | **Gravação recusada**; proteção do trecho passou |
| 3a — `c3-add-existente.md` | `Add File` com todo o conteúdo antigo e alvo novo | `teste / novo / antiga` | `patch: completed` | **Gravação passou; proteção falhou**: `outra: externa` foi perdida |
| 3b — `c3-update-inteiro.md` | `Update File`, remove as três linhas e insere três | `teste / antigo / externa` | `Failed to find expected lines`, incluindo `outra: antiga` | **Gravação recusada**; proteção passou para esse patch |
| 3c — `c3-delete-add.md` | `Delete File` + `Add File` do mesmo caminho, numa chamada | `teste / antigo / externa` | `invalid patch: multiple operations target ...c3-delete-add.md` | **Gravação recusada por formato**, não por conferência de versão |
| 4a — `h-add-existente.md` | `Add File` em existente, política ligada | `teste / antigo / externa` | `Command blocked by PreToolUse hook: BANCADA-GRAVACAO` | **Hook passou**: recusou antes da gravação |
| 4b — `h-update-inteiro.md` | `Update File` removendo as três linhas | `teste / antigo / externa` | Mesmo bloqueio por hook | **Hook passou**: recusou antes da verificação do patch |
| 4c — `h-delete-add.md` | `Delete File` + `Add File` em existente | `teste / antigo / externa` | Mesmo bloqueio por hook | **Hook passou**; aqui o veto veio antes do erro de formato visto em 3c |
| 4d — `h-parcial.md` | `Update File` parcial | `teste / novo / externa` | `patch: completed` | **Hook e gravação passaram**; alteração externa preservada |
| 4e — `h-novo.md` | `Add File` com caminho ainda ausente | `teste / novo / antiga` | `patch: completed` | **Hook e criação passaram** |

Foram conferidos novamente os dez conteúdos finais com assertivas, a execução de dez hooks e os três vetos. O CLI saiu com código 0, embora algumas chamadas individuais tenham falhado como esperado. Esse código de saída não foi usado como prova de sucesso de cada operação.

## O que o hook prova e seus limites

O protótipo examina `tool_input.command`, separa `Add`, `Delete` e `Update`, resolve caminhos dentro da subpasta e recusa, para as notas protegidas:

- `Add` quando o destino já existe;
- `Delete` de arquivo existente, cobrindo a tentativa de apagar/recriar testada;
- `Update` cujo número de linhas removidas cobre todas as linhas atuais.

Ele deixa passar `Update` parcial e `Add` de arquivo ausente. **É um classificador de bancada para os formatos testados**, com uma heurística por quantidade de linhas no `Update`; não é um parser completo nem política pronta para o hub. Deleções legítimas também seriam recusadas. Não foram testados `Move to`, múltiplos caminhos num patch, links, mudança de conteúdo após a saída do hook, arquivo vazio, exclusão e criação em chamadas separadas ou outros meios de gravação. Um teste de hook não demonstra cobertura universal nem controle de concorrência atômico.

O caso 1 comprova que o patch parcial **não recusa qualquer mudança do arquivo desde a leitura**. Ele pode aplicar sobre o arquivo atual quando o trecho esperado ainda encontra correspondência. Portanto isso não equivale à garantia estrita “mudou qualquer parte desde a leitura, recusa e relê”. O caso 3a mostra que permitir todo `apply_patch` como se fosse sempre troca de trecho deixaria uma regravação inteira passar.

## Fontes primárias: promessa documentada e observação

1. [Documentação oficial de apply_patch](https://developers.openai.com/api/docs/guides/tools-apply-patch): trecho **“create, update, and delete files in your codebase using structured diffs”**. Descreve as operações e a aplicação pelo harness; não estabelece nessa passagem um contrato de versão ou hash desde a leitura. É documentação da ferramenta de API; o comportamento específico do CLI acima foi medido, não inferido dessa página.
2. [Documentação oficial dos hooks Codex — PreToolUse](https://learn.chatgpt.com/docs/hooks#pretooluse): trecho **“permissionDecision”: “deny”** e campo `tool_input.command` para `apply_patch`. [Cobertura](https://learn.chatgpt.com/docs/hooks#tool-coverage) declara suporte a `apply_patch` e ressalva caminhos especializados. O teste confirma o veto no caminho efetivamente usado nesta versão.
3. [Código Codex 0.161.0 — file_update.rs](https://github.com/openai/codex/blob/rust-v0.161.0/codex-rs/apply-patch/src/file_update.rs): trecho **“Failed to find expected lines”**. Procura as linhas antigas do chunk no conteúdo disponível e produz esse erro se não as encontra, coerente com os casos 2 e 3b.
4. [Código Codex 0.161.0 — seek_sequence.rs](https://github.com/openai/codex/blob/rust-v0.161.0/codex-rs/apply-patch/src/seek_sequence.rs): trecho **“exact match, then ignoring trailing whitespace”**. O código também tenta aparar os dois lados e normalizar pontuação Unicode. Por isso não se deve descrever a correspondência como igualdade estrita byte a byte. Variações de espaços/pontuação não foram testadas nesta rodada.
5. [Código Codex 0.161.0 — lib.rs](https://github.com/openai/codex/blob/rust-v0.161.0/codex-rs/apply-patch/src/lib.rs): o ramo `Hunk::AddFile` lê conteúdo anterior para o registro `overwritten_content` e chama `write_file_with_missing_parent_retry`. Trecho **“overwritten_content”**. Isso é compatível com a sobrescrita observada em 3a; o nome `Add File` não funcionou como condição “só criar se ausente”.

Não generalizo esses resultados para versões posteriores, outras ferramentas ou todos os patches possíveis. A falha da tentativa de apagar/recriar numa única chamada é um resultado observado do CLI desta rodada; a tentativa em duas chamadas separadas ficou não verificada.

## Evidências e estado final

Todos os artefatos ficam em `C:\Projetos\bancada-acesso\gravacao\codex\`:

- `logs\stderr.txt`: leitura inicial, ordem dos hooks, respostas das ferramentas, erros e vetos;
- `logs\stdout.txt`: resposta final do agente, usada só como informação auxiliar;
- `logs\hooks.jsonl`: dez entradas com patch recebido e conteúdo antes/depois da mudança externa;
- `logs\results.json`: conteúdo final completo dos dez arquivos;
- `logs\prompt.txt`, `run.py` e `hook.py`: pedido exato, orquestração e política usados;
- `logs\hooks-list.txt`: hashes e origem dos hooks; `logs\processos.jsonl`: PIDs e argumentos das invocações;
- `logs\baseline.json` e `logs\final-verification.json`: hashes e conferência final;
- `fontes\`: código primário consultado, fixado na tag 0.161.0.

**Globais intocados.** SHA-256 antes/depois conferido:

| Arquivo | SHA-256 antes = depois |
|---|---|
| `~/.codex/config.toml` | `a6cae9fa9397b2b3c5757642583146a7584b19abc4809af0604a7514eb397de1` |
| `~/.codex/hooks.json` | `d822fa388c1d2f07207616fc672549aec24eb687cd022b6ff5b8405413590f42` |
| `.codex/hooks.json` da raiz da bancada | `82cf7a52ba017fd67d159314f722def0a7aa2e8da8f63617f116c7af9ff79fc6` |

Não escrevi em `~/.claude/` ou `~/.copilot/`, nem em arquivos do outro executor. As duas configurações temporárias da subpasta Codex (`.codex/hooks.json` e `.codex/config.toml`) foram copiadas para `logs\config-local-*` e removidas ao final; o hook deixou de estar instalado. O script permanece como artefato, sem execução automática. Para repetir, é necessário reinstalar a configuração local e limpar os marcadores de mutação; `run.py` sozinho não reinicializa um segundo ensaio.

Os processos de teste terminaram; a verificação por PIDs e descendentes encontrou **zero** restantes (`logs\processos-restantes.json`). Não encerrei processos por nome. Não li credenciais, não usei dados de cliente e não fiz commit. No repositório `context-hub`, só este arquivo de entrega foi escrito.
