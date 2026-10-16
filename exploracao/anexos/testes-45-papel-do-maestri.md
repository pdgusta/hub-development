# Testes 45: papel do Maestri com Codex e Copilot (2026-10-12)

Ticket: "Testes do papel do Maestri com Codex e Copilot" (`.scratch/context-hub/issues/45-testes-do-papel-do-maestri.md`).
Mesmo método do grupo A dos testes 38 (`exploracao/anexos/testes-38-portas/grupo-a-carga-de-instrucoes.md`),
agora com recrutas reais do Maestri abertos na pasta de um papel.

## Método

Hub falso em `C:\teste45\hub\`, sem `.git` e sem nenhum `CLAUDE.md`/`AGENTS.md` em `C:\` (conferido). Cada
arquivo de instrução tem um marcador aleatório gerado na hora (`secrets` do Python); nenhum marcador foi
posto em pergunta a agente.

```
hub/AGENTS.md                         RAIZ-TF7K
hub/HUB.md                            vazio (marcador de raiz para o Codex)
hub/clients/x/AGENTS.md               INIC-QSDC
papel "Papel teste 45" (prompt)       PAPEL-5FVW
linha posta à mão no arquivo do papel REGR-CL5E (teste de regravação)
```

Papel criado com `maestri role create "Papel teste 45" "..."` (escopo do workspace Context Hub). Três recrutas,
todos com `--role "Papel teste 45" --dir C:\teste45\hub\clients\x`:

- **Codex45:** `--preset "Codex"` (o preset roda `codex --no-daemon`).
- **Codex45m:** `--preset "Codex" --command "codex --no-daemon -c \"project_root_markers=['HUB.md']\""`.
- **Copilot45:** `--preset "Shell" --command "copilot"` (não há preset de Copilot; `copilot` sem argumentos
  abre o modo interativo, conforme `copilot --help`).

Pergunta a cada um, por `maestri ask`: "Sem ler arquivos nem rodar comandos: copie qualquer palavra-marcador no
formato PALAVRA-XXXX que esteja nas suas instruções carregadas. Se não houver, diga NENHUM." Nenhum recusou, então
o teste de comportamento não foi preciso. Prova cruzada: `/status` do Codex (linha "Agents.md") e o registro
da sessão do Copilot (`~/.copilot/session-state/<id>/events.jsonl`, mensagem de sistema), que mostram sem
tool call nenhuma quais arquivos entraram.

Versões: Maestri build 87 (sha `9a4e3e5e`, 2026-10-11); codex-cli 0.161.0 (modelo GPT-6-Sol, medium); GitHub
Copilot CLI 1.0.96 (modelo Claude Sonnet 5.5).

## Onde cada recruta abriu e o que o Maestri gravou

Os três abriram na **mesma pasta**: `C:\teste45\hub\clients\x\.maestri\roles\915c7ee5-e2c0-47ff-a550-65370e973d65\`
(cabeçalho do Codex, `/status` e rodapé do Copilot). O id da pasta é o id do papel (`role.json`), não do
terminal: recrutas com o mesmo papel no mesmo `--dir` dividem a pasta.

Conteúdo gravado pelo Maestri no primeiro `recruit`:

| Arquivo | Tamanho | Conteúdo |
|---|---|---|
| `AGENTS.md` | 338 B | bloco `<your_assigned_role>` com o prompt + bloco `<working_directory>` apontando `C:\teste45\hub\clients\x` |
| `CLAUDE.md` | 338 B | idêntico ao `AGENTS.md` (mesmo sha256) |
| `role.json` | 264 B | `id`, `name`, `prompt`, `color`, `icon`, `schemaVersion` |

Nada além disso: nenhum `.codex/` ou config de harness na pasta (o código só grava settings para `gemini`/`qwen`,
pesquisa 43).

## Resultados

| # | Harness | Condição | Carregou | Prova cruzada |
|---|---|---|---|---|
| M1 | Codex | padrão (preset Codex) | só PAPEL | `/status`: "Agents.md: AGENTS.md" |
| M2 | Codex | `-c project_root_markers=['HUB.md']` | RAIZ, INIC, PAPEL | `/status`: "Agents.md: ..\..\..\..\..\AGENTS.md, ..\..\..\AGENTS.md, AGENTS.md" |
| M3 | Copilot CLI | padrão (`copilot`, sem `.git`) | PAPEL, INIC (sem RAIZ) | mensagem de sistema da sessão traz o papel e o `clients/x/AGENTS.md` como `custom_instruction`; nenhum tool call |

Observações:

- **Codex sem marcador** fica preso à pasta do papel: não lê nem o `AGENTS.md` da iniciativa nem o da raiz.
  Com `project_root_markers` e `HUB.md` na raiz, lê a cadeia toda, da raiz ao papel. Igual aos testes 38 (C2, C3).
- **Copilot** sobe até a pasta da iniciativa (`clients/x`, três níveis acima do papel), mas não até a raiz do hub.
  O mecanismo não ficou claro: `copilot instruction list` rodado na pasta do papel lista só "AGENTS.md + CLAUDE.md"
  (da própria pasta) e `~/.copilot/copilot-instructions.md`, mas a sessão real recebeu também o `AGENTS.md` de
  `clients/x`. No teste 38 (P2) o Copilot também leu uma pasta acima e não a raiz. Por que essa pasta e não outra:
  **não verificado**. Pelo teste 38 (P4), um `.git` na raiz do hub resolveria; não foi repetido aqui.
- **Permissões do Codex variaram:** M1 abriu como "Workspace (granular)"; M2 como "Read Only (Ask for approval)".
  Não investigado.

## Regravação dos arquivos do papel

| Passo | O que aconteceu |
|---|---|
| 1º `recruit` (Codex45, 19:49:47) | Maestri cria a pasta e os três arquivos |
| 2º e 3º `recruit` com o mesmo papel (19:51, 19:52) | arquivos **não** reescritos (mtime continua 19:49:47) |
| Linha `REGR-CL5E` acrescentada à mão no `AGENTS.md` e no `CLAUDE.md` | sha muda |
| `maestri recruit --preset "Codex" --replace "Codex45"` (reinício do terminal) | arquivos **não** reescritos (mtime e sha iguais); o Codex reiniciado respondeu "PAPEL-5FVW, REGR-CL5E" |
| `maestri role edit "Papel teste 45" "curto." "bem curto."` | os três arquivos **reescritos** (19:55:48), a linha manual **sumiu**, e os três recrutas reiniciaram sozinhos |

Conclusão: o Maestri **não** regrava os arquivos do papel a cada início de terminal; um ajuste manual sobrevive
a reinício e a novos recrutas. Mas **qualquer edição do prompt do papel reescreve os arquivos do zero** e apaga o
ajuste manual (e reinicia todo terminal com o papel, como diz a Wire). Ajuste manual nesses arquivos é frágil;
o lugar de um ajuste é o prompt do papel.

Outro achado: `maestri role delete "Papel teste 45" --force` **não apagou** a pasta `.maestri\roles\<id>\` do
projeto; ela ficou no disco com os três arquivos.

## Limpeza

- Recrutas Codex45, Codex45m e Copilot45 dispensados (`maestri dismiss`); `maestri list` final mostra só o
  Designer, as notas e os portais de antes.
- Papel apagado (`maestri role delete "Papel teste 45" --force`); `maestri role list` não o mostra; nenhum
  arquivo em `~/.maestri` cita o nome.
- **`C:\teste45` não foi apagado:** a trava de segurança do Claude Code bloqueou o `rm -rf C:\teste45` (exige
  aprovação de uma pessoa). Fica para o Gustavo apagar a pasta (só contém o hub falso e a pasta do papel).
- Conferência por sha256 antes e depois de `~/.claude/settings.json`, `~/.codex/{config.toml,AGENTS.md,hooks.json}`
  e dos JSON/MD de `~/.copilot` e `~/.copilot/hooks`:
  - `~/.claude/settings.json`, `~/.codex/AGENTS.md`, `~/.codex/hooks.json`, `~/.copilot/config.json`
    (inclusive `trustedFolders`), `copilot-instructions.md`, `mcp-config.json`, hooks: **iguais**.
  - **`~/.codex/config.toml` mudou**: ganhou o bloco `[projects.'c:\teste45\hub']` / `trust_level = "trusted"`
    às 19:51:39, na abertura do Codex45m. Causa provável (inferida, a tela não foi vista): com o marcador de raiz,
    o Codex passou a ver `C:\teste45\hub` como projeto não confiável e abriu a tela de confiança logo depois da
    tela de atualização; o Enter que enviei para rodar `/status` escolheu a opção padrão "confiar", e o Codex
    gravou isso. No Codex45 (sem marcador) não houve tela nem gravação. **Não editei o arquivo**, conforme a
    instrução. A entrada é inofensiva (aponta para pasta de teste), mas é uma mudança: o Gustavo decide se
    apaga essas duas linhas.
  - `~/.copilot/command-history-state.json` e `open-sessions-state.json` mudaram: são estado de uso do Copilot
    (histórico do que foi digitado e sessões abertas), não configuração. O histórico guarda a pergunta do teste.
  - A tela de confiança do Copilot apareceu nas duas aberturas e foi respondida com "1. Yes" (sem lembrar a
    pasta); `trustedFolders` não mudou.
  - Sessões novas ficaram nos históricos dos harnesses (`~/.copilot/session-state/`, sessões do Codex), como
    em qualquer uso.

## O que não deu para testar

- Copilot com `.git` na raiz do hub, dentro do papel (o teste 38 já mostrou que `.git` faz o Copilot ler a raiz,
  fora do Maestri).
- Por que o Copilot leu `clients/x` e não a raiz (o `instruction list` não mostra essa fonte).
- Claude Code no papel real: já coberto nos testes 38 (T9, T10), não repetido.
- Se o Maestri reescreve os arquivos em outros gatilhos (atualização do app, `role assign`, troca de escopo do
  papel); só `role edit` foi testado.
- Codex com marcador sem a tela de confiança (por exemplo com a raiz já confiável, ou com `-s`/`-a` explícitos):
  não repetido para não mexer mais no `config.toml`.
