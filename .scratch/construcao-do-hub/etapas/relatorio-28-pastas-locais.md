# Relatório do ticket 28: pastas locais, o script e o git (Vela)

Ramo `ticket-28`, worktree `C:/context-hub-wt/ticket-28`, da ponta de `integracao` 763813a (2026-10-17 03h15).
Fonte: rodada `2026-10-16-pastas-locais-depois-do-gerador` (Gustavo, as quatro A), spec faixa 1 "Pasta não replicada",
relatório do 06 ("O que vai doer ao ligar"), lição do 02.

## O que foi construído

- **Skill `agents/skills/nova-pasta-local/`** (`SKILL.md` e `nova-pasta-local.ps1`; o agente a chama, como a "nova
  iniciativa"). Usa o módulo do banco do 07 (`agents/code/kit/par/banco/banco.psm1`): `Stop-Sincronizador`,
  `Start-Sincronizador`, `Invoke-Cli`. O `.env` do par vem de `-EnvFile`, com padrão em `HUB_BANCO_ENV` (aval do
  maestro).
  - **Nova:** para o sincronizador, cria a pasta com o `index.md` mínimo (`title`, `status`, `summary: auto`,
    `local: true`; o `verificar-frontmatter --corrigir` completa o resto), roda o gerador e religa. Pasta que já existe
    e não é local é recusada sem parar nada ("use -TornarLocal").
  - **`-TornarLocal`:** para o sincronizador, põe `local: true` no `index.md` (troca de trecho; cria o cartão mínimo se
    não houver), roda o gerador, lista a pasta no banco local do par (`ls <pasta>/`), marca cada arquivo como apagado
    (`rm`) e leva ao CouchDB (`sync`); a replicação tira a cópia da outra máquina. Depois `git rm -r --cached` (os
    arquivos ficam no disco; a cópia diária leva a remoção ao GitHub) e religa. **O histórico do git ainda guarda as
    versões antigas: a remoção só vale daqui para frente; limpar o histórico não entra** (maestro). O script diz isso
    na saída, e o `SKILL.md` também.
  - **Gerador recusa** (YAML ilegível): o script para com `parou:` e o caminho, deixa o sincronizador parado e avisa
    ("nada replica até religar; resolva e rode de novo"). Rodar de novo termina o que faltou.
- **Gerador** (`agents/code/bin/gerar-exclusoes.mjs`): escreve também o `.git/info/exclude` (caminho por
  `git rev-parse --git-path info/exclude`; só se o hub tem `.git`), num bloco entre `# hub:exclusoes:inicio` e
  `# hub:exclusoes:fim`; o resto do arquivo fica. Conteúdo: `.*`, `!.gitignore`, `!.gitkeep` (o esqueleto versiona os
  dois; dentro de pasta com ponto o git nem entra, então a exceção não a reabre) e `/<pasta local>/`. Não conta no
  `mudou` (o git lê o arquivo a cada comando; nada a religar). Decisão técnica minha, aceita pelo maestro.
- **`AGENTS.md`** (cabeça): "essa pasta nasce ou vira local só pela skill "nova pasta local"". Cabeça com 1.695
  caracteres (limite 2.000).
- **CLI falso** (`agents/code/test/banco/cli-falso.cjs`): ganhou o `daemon` (linha de pronto e fica vivo), para o
  teste sem Docker parar e religar o sincronizador de verdade.

## Testes

| Teste | Resultado |
|---|---|
| `node --test agents/code/test/gerar-exclusoes/gerador.test.mjs` (novo: exclude e `git status`; vermelho antes) | 8/8 |
| `node --test agents/code/test/28-pastas-locais-sem-docker.test.mjs` (nova; pasta existente; YAML ilegível; vermelho antes) | 12 PASSA |
| `node --test agents/code/test/04-esqueleto.test.mjs` (o `AGENTS.md` mudou) | 13/13 |
| `pwsh -NoProfile -File agents/code/test/28-pastas-locais.test.ps1` (Docker, `hub-ensaio-28-a/b`, 5992/5993) | (preencher) |
| suíte inteira | (preencher) |

## O que vai doer ao ligar

- **O histórico do git.** A pasta tornada local sai do índice, mas os commits antigos guardam as versões; se o GitHub
  já as tem, elas ficam lá. Limpar histórico é outra decisão.
- **Tornar local com o banco da outra máquina fora do ar.** A remoção vai ao CouchDB deste par; a outra máquina só
  apaga a cópia quando a replicação chegar. Até lá, a cópia de lá segue no disco dela (e, se alguém editar lá, a
  edição volta ao banco como mudança nova). Não provado com a replicação parada.
- **A vigia.** Rodar o gerador a cada passada e religar quando a lista muda é do ticket 16; aqui só o script.
- **`HUB_BANCO_ENV`.** Quem o põe no ambiente do agente é o kit (faixa 8); sem ele, o script recusa e pede o
  `-EnvFile`.
