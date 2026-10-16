# Worker 6: notas

## Volta 1 (2026-10-15)

**Faixa assumida: guardas de gravação e leitura no disco** (faixa 6 do corte do Worker 2). Fontes lidas: Answer do
ticket 11 ("Como os agentes gravam no hub"), Answer do 14 ("Acesso dos agentes: decisão"), "Imposição" do Answer do 12,
`bancada-gravacao-claude-copilot.md` e `bancada-gravacao-codex.md` em `.scratch/context-hub/`.

### O que a faixa entrega

Um hook "antes da ferramenta" (mais um "depois da ferramenta" para guardar o que a busca devolveu), Node ≥ 22, em
`hooks/06-guardas/`:
1. Recusa a regravação inteira de arquivo existente (Claude `Write`; Codex `apply_patch` com `Add File` sobre existente,
   `Delete`+`Add`, `Update` que troca tudo; Copilot `create`). Deixa passar troca de trecho e arquivo novo.
2. Recusa nota fora do esquema, chamando o verificador da faixa 1 com o conteúdo proposto.
3. Aviso de leitura sem recusa: veio da busca e lê trecho, calado; veio da busca e lê inteiro arquivo grande, "leia o
   trecho"; não veio da busca, "busque antes"; uma vez por arquivo por sessão.
4. Sai na hora fora de `HUB_ROOT`.

### Plano de execução dentro da hora (subagentes em paralelo)

- min 0–15: `fragmento.json` dos três harnesses (entregue ao kit); dublês do verificador e da busca; fixtures tiradas
  dos registros da bancada (`C:\Projetos\bancada-acesso\gravacao\`: `logs\hooks.jsonl` do Codex, `logs\hooks.log` do
  Claude e do Copilot).
- min 0–35, em paralelo: subagente por adaptador (Claude, Codex `apply_patch`, Copilot) + um para o aviso de leitura,
  cada um com `node --test`.
- min 35–50: ponta a ponta com `claude -p`, `codex exec`, `copilot -p` (HOME de ensaio se houver login; senão escopo de
  projeto, como a bancada).
- min 50–60: relatório da faixa, valor medido de "leitura grande", entrega aos Prumos.

### Riscos e o que está fora

- Parser do `apply_patch`: a bancada usou heurística por número de linhas; `Move to`, vários caminhos num patch e
  deleção legítima ficaram sem teste. Na hora: cobrir os formatos da bancada mais `Move to` e vários caminhos; deleção
  de arquivo inteiro: **pergunta aberta** (o 11 não decide; hoje o hook da bancada recusaria). Proponho deixar passar
  `Delete File` sozinho (não desfaz edição de ninguém sem rastro? não verificado com o LiveSync) — a conferir com o
  Prumo na volta 2.
- Aviso de leitura no Codex e no Copilot, que leem por shell: fica para outra execução (não verificado no 11); o Copilot
  tem a ferramenta `view` (vista na mensagem do `create` na bancada), então entra se der.
- Hooks no escopo do usuário: não verificado no 11; a prova de ponta a ponta no HOME de ensaio é o que mostra.
- Como o Claude Code acha um HOME de ensaio (variável de configuração): **não verificado**; conferir em fonte primária
  na volta 2 ou com a faixa 8.

### Para a próxima volta

- Conferir se a faixa 1 aceitou "verificador sai 0 para caminho sem esquema".
- Conferir com a faixa 3 o nome da ferramenta de busca.
- Levar ao Prumo a pergunta da deleção inteira.

## Volta 2 (2026-10-15)

- **Fechei a fronteira com a faixa 3 pela fonte primária** (README do obsidian-hybrid-search 0.16.2 via `npm view`,
  "Available MCP tools"): ferramentas `search` e `read` (sem prefixo; `OBSIDIAN_PREFIX` vazio), caminhos relativos ao
  cofre, `read` com `snippet_length`. Consequências: o hook resolve caminho contra `HUB_ROOT`; o `read` da busca sem
  `snippet_length` em arquivo grande também recebe o aviso. Nome do servidor proposto: `hub-busca` (padrão do Worker 5).
  Não verificado: a forma do texto do `search` no MCP (pedido de resposta gravada à faixa 3) e os nomes de ferramenta
  de MCP que o Codex e o Copilot passam ao hook.
- **Crivo do Prumo 2:** comando único `pwsh agents/test/06-guardas.ps1`; caminhos `hooks/06-guardas/**` e
  `agents/test/06-guardas.ps1`; estado por sessão em `.local/guardas/`.
- Pendente para a volta 3: a pergunta da deleção de arquivo inteiro (`Delete File` sozinho) ao Prumo; conferir se a
  faixa 1 aceitou "verificador sai 0 para caminho sem esquema"; `agents/test/` também não está no ticket 12 (mesmo
  ponto do Prumo sobre `agents/bin/`).
