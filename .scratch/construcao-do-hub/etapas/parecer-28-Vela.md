# Ticket 28 — Vela — parecer do Fiel — rodada 1

2026-10-17 ~03h40. Ramo ticket-28, HEAD fc6c78b; contém integracao 763813a. Revisão em dupla com o Fielzinho
(parecer dele: `parecer-28-Vela-fielzinho.md`).

## Veredito: VOLTA

## Consertos

1. **`local` lido por regex no arquivo inteiro** (Fielzinho; Fiel reproduziu). `nova-pasta-local.ps1:38`
   (`$ehLocal = ... -match '(?m)^local:\s*true\s*$'`) casa uma linha do corpo; o gerador lê só o frontmatter
   (`lib/locais.mjs`, `separar(...).dados.local`). Reprodução (`logs/repro-28-fielzinho.ps1`, rodada também pelo
   Fiel): `index.md` sem `local` no YAML e `local: true` no corpo → a skill sai 0, religa e diz "pronto: ... é local";
   o verificador completa `local: false`; `.livesync/ignore` não tem a pasta. Pior com `-TornarLocal` (pelo código):
   o `index.md` não é tocado, o script apaga a pasta do banco e do índice do git, e a religação sobe tudo de novo.
   A troca da linha 53 (`-replace '(?m)^local:.*?(\r?)$'`) também troca linhas `local:` do corpo.
   Conserto: ler e escrever `local` só no frontmatter, com o parser da lib (`separar`), preservando o corpo; teste
   com `local: true` e `local: false` no corpo, nos dois modos.
2. **Caminho conferido só pelo texto** (Fielzinho). Uma junction dentro do hub apontando para fora: a skill cria o
   `index.md` fora do hub, sai 0 e diz "pronto"; o gerador não desce na junction e a pasta não entra na lista.
   Conserto: resolver o destino real (há `lib/caminhos.mjs`) e recusar fora do hub antes de parar o sincronizador.
   **Junto com 1 e 2:** só religar e dizer "pronto" se a pasta está em `locais` da saída JSON do gerador; senão
   `parou:` com o caminho.
3. **`.*` no `.git/info/exclude` esconde o `.claude-plugin/` de mod novo** (Fiel). O hub versiona
   `agents/code/mods/*/.claude-plugin/plugin.json` (`git ls-files`). Sonda: hub de ensaio do `montar.mjs`, gerador do
   ramo, mod novo `agents/code/mods/novo/.claude-plugin/plugin.json` → `git check-ignore -v` responde
   `.git/info/exclude:9:.*`; o `git add` do mod deixa o plugin.json de fora, calado. Os arquivos já versionados seguem
   no git; o que quebra é o próximo mod. Conserto: exceção `!.claude-plugin/` no bloco (como `.gitignore` e
   `.gitkeep`) e teste com um mod novo.

## Evidências do Fiel

- `node --test gerar-exclusoes/gerador.test.mjs 28-pastas-locais-sem-docker.test.mjs`: 9/9 verdes (54 s); árvore limpa.
- Reprodução do Fielzinho rodada pelo Fiel: confirma o 1 e o 2 (YAML final `local: false`, lista sem a pasta;
  `ARQUIVO_FORA=True`). Ensaio do Fiel limpo; sobra do Fielzinho (`%TEMP%/hub-ensaio-28-fielzinho-486c...`, sem
  processo vivo) apagada pelo Fiel.
- Docker (`28-pastas-locais.test.ps1`) não rodado nesta rodada: trava do Trilho (03h30) e o código vai mudar. Roda na
  rodada 2, com a trava.

## Acordo

VOLTA em acordo: o Fielzinho deu VOLTA pelos 1 e 2, e o Fiel aceitou os dois (reproduzidos). O 3 (Fiel) foi
enviado ~03h45; o Fielzinho ficou sem cota até 06h58 antes de responder. A leitura dele sobre o 3 fica pendente
para a rodada 2.

# Rodada 2 — Fiel — 2026-10-17 ~04h30

Ramo ticket-28, HEAD 2eec8e9 (e134279, 39abd57, merge de integracao 3c24d68). Fiel sozinho (Fielzinho sem cota até
06h58; leitura dele pendente, inclusive do 3 da rodada 1).

## Veredito: VOLTA (1 conserto)

## Os três da rodada 1: feitos
- 1: `cartao.mjs` lê e escreve `local` só no frontmatter (`separar`), preservando o corpo. Repro do Fielzinho repetida
  pelo Fiel: `local: true` só no corpo → `recusa: reference/exemplo já existe e não é local`, código 1, sincronizador
  não parado, lista vazia.
- 2: caminho real conferido antes de parar o sincronizador. Repro da junction: `recusa: fora do hub: ...`, código 1,
  `ARQUIVO_FORA=False`. E o script só religa se a pasta está em `locais` do JSON do gerador.
- 3: `VERSIONADOS_COM_PONTO` com `.claude-plugin/`; teste do mod novo em `gerador.test.mjs:132`.

## Conserto
1. **`-Titulo` some calado** (Fiel). `nova-pasta-local.ps1`: `Invoke-Cartao @('marcar') + $(if ($Titulo) ...)` está
   em modo de comando. O `+` e o título viram argumentos soltos; a função não é avançada, então eles caem em `$args`
   sem erro. Prova direta: função igual com `[string[]]$argumentos` recebe `n=1: marcar` com e sem título. Pela skill
   real (hub de ensaio, CLI falso): `-Pasta reference/rascunhos -Titulo 'Rascunhos da semana'` → código 0, mas
   `title: "rascunhos"`. O Docker passa `-Titulo 'Rascunhos de A'` (28-pastas-locais.test.ps1:48) e não confere.
   Conserto: montar a lista entre parênteses, `Invoke-Cartao (@('marcar') + ...)`, e um teste que confira o título.

## Evidências
- Repro dos três casos: script em scratchpad do Fiel (cópia da do Fielzinho + caso do título). Ensaios apagados;
  nenhum `hub-ensaio-28-*` sobrando. Árvore do ramo limpa.
- Docker (`28-pastas-locais.test.ps1`): não rodado; trava do Cinzel (04h09). Roda na rodada 3, com a trava, sobre o
  código final.
- Rodada 3 = teto: passa com ressalvas escritas, depois do Docker.
