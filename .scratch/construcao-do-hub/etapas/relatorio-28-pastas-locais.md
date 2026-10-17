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
| `pwsh -NoProfile -File agents/code/test/28-pastas-locais.test.ps1` (Docker, `hub-ensaio-28-a/b`, 5992/5993) | 14 PASSA, saída 0 (log `etapas/logs/28-docker-1.log`; nenhum contêiner sobrou) |
| suíte inteira, `node --test --test-concurrency=1 "agents/code/test/**/*.test.mjs"`, em fc6c78b, com a trava | 196 testes: 188 PASSA, 8 pulados (harness de verdade), 0 falhas (log `etapas/logs/suite-28.log`) |

## O que vai doer ao ligar

- **O histórico do git.** A pasta tornada local sai do índice, mas os commits antigos guardam as versões; se o GitHub
  já as tem, elas ficam lá. Limpar histórico é outra decisão.
- **Tornar local com o banco da outra máquina fora do ar.** A remoção vai ao CouchDB deste par; a outra máquina só
  apaga a cópia quando a replicação chegar. Até lá, a cópia de lá segue no disco dela (e, se alguém editar lá, a
  edição volta ao banco como mudança nova). Não provado com a replicação parada.
- **A vigia.** Rodar o gerador a cada passada e religar quando a lista muda é do ticket 16; aqui só o script.
- **`HUB_BANCO_ENV`.** Quem o põe no ambiente do agente é o kit (faixa 8); sem ele, o script recusa e pede o
  `-EnvFile`.

## A prova com Docker (o que ela mostra)

- **Nova com o sincronizador da A rodando:** a pasta nasce, uma nota entra nela, e uma nota de controle gravada depois
  chega à B; a pasta não está no disco da B nem no banco da A (lido pelo dispositivo leitor).
- **Tornar local:** a pasta `reference/vai-ficar` (duas notas, uma em subpasta, já replicada e já no git) sai do disco
  da B e do banco da A; o sincronizador da A volta (a nota de controle chega à B), e os arquivos da A ficam iguais
  (hash), mais o `index.md` novo. O sincronizador religado não apaga do disco o que foi apagado do banco: a lista nova o
  deixa de fora.
- **Git do hub A:** `git status` não mostra a pasta local nem nada com ponto; a pasta tornada local saiu do índice, e o
  status mostra as duas remoções, para a cópia diária levar.

## Rodada 2 (consertos do parecer da rodada 1)

Commits e134279 (1 e 2) e o seguinte (3), sobre fc6c78b.

1. **`local` só no frontmatter.** O `index.md` passa a ser lido e escrito por `agents/skills/nova-pasta-local/cartao.mjs`,
   com o `separar` do `lib/frontmatter.mjs` (o mesmo que o gerador usa em `lib/locais.mjs`). `marcar` troca a linha
   `local:` só dentro do bloco do frontmatter, ou a acrescenta no fim dele; sem frontmatter, põe um bloco antes; o corpo
   não é tocado; relê e confere. Teste: `local: true` só no corpo não faz a pasta local (nova recusa); `-TornarLocal`
   com `local: true` e com `local: false` no corpo: a pasta entra na lista, o frontmatter diz `local: true`, o corpo
   fica igual.
2. **Caminho real.** O `cartao.mjs ler` resolve o caminho real (`lib/caminhos.mjs`, `real`) e recusa (código 3) quando
   o caminho real relativo ao hub não é o pedido (junction para fora, ou para outro lugar do hub, onde o gerador não
   desce). Roda antes de parar o sincronizador. Teste: junction `reference/atalho` para fora; nova em
   `reference/atalho/sub` e `-TornarLocal` em `reference/atalho` recusados ("fora do hub"), nada criado fora,
   sincronizador com o mesmo PID.
   **Com 1 e 2:** o script só segue (apagar do banco, git, religar, "pronto") se a pasta está em `locais` da saída JSON
   do gerador; senão `parou:` com o caminho, sincronizador parado.
3. **`.claude-plugin/` fica no git.** O bloco do `.git/info/exclude` ganhou `!.claude-plugin/`; os nomes com ponto
   versionados ficam numa lista só (`VERSIONADOS_COM_PONTO`: `.gitignore`, `.gitkeep`, `.claude-plugin/`; conferido
   com `git ls-files`: só esses três). Teste: mod novo `agents/code/mods/novo/.claude-plugin/plugin.json` aparece no
   `git status`. Sonda: `.claude-plugin/` dentro de `.secrets/` não reabre a pasta (status vazio).

O CLI falso ganhou `ls`, `rm` e `sync` (banco vazio), para o `-TornarLocal` sem Docker.

| Teste | Resultado |
|---|---|
| gerador.test.mjs | 8/8 |
| 28-pastas-locais-sem-docker (pastas-locais-sem-docker.ps1) | 24 PASSA (vermelho antes: 11 falhas) |
| Docker 28-pastas-locais.test.ps1 | o Fiel roda na rodada 2, com a trava |
| suíte inteira | não rodada: pela regra nova (2026-10-17), só na junção, pelo Rebite. Em 2eec8e9 (com integracao 3c24d68): gerador + 04-esqueleto 21/21; 28 sem Docker e 07 sem Docker 2/2 |

## Rodada 3 (conserto do parecer da rodada 2)

Commit 5436cad. O `-Titulo` sumia sem aviso: `Invoke-Cartao @('marcar') + $(...)` está em modo de comando, e o `+` e o
título caíam em `$args`. Agora a expressão vai entre parênteses. Teste (vermelho antes): `-Titulo 'Rascunhos da semana'`
grava `title: "Rascunhos da semana"`. Sem Docker: 25 PASSA. As outras chamadas do script recebem uma lista literal só.
