# Parecer do Fiel — ticket 06, gerador de exclusões (Vela)

## Rodada 1 — 2026-10-16 — ramo ticket-06 em d45be5d

Veredito: **volta**.

Conferido: integracao 0d04985 é ancestral de d45be5d; diff contra integracao = gerador, dois testes, dois logs.
`node --test agents/code/test/gerar-exclusoes/gerador.test.mjs`: 5/5 (Fiel).
Critérios do ticket e relatório conferidos contra o ticket 12 (pasta local = `index.md` com `local: true`) e a forma
do ticket 02 (`.livesync/ignore` com `.*` e `.*/`).

### Consertos

1. **(Fiel) `local` lido diferente do verificador: pasta local vaza calada.** `ehLocal` usa regex própria
   (`/^local:[ \t]*true.../`). O verificador do ticket 05 lê com js-yaml 4 (`lib/frontmatter.mjs`, `separar`), e
   `agents/frontmatter/index.yml` impõe `local: {type: boolean}`. js-yaml aceita `True` e `TRUE` como `true`, e o
   `separar` aceita o fechamento `--- ` com espaço. Reprodução: hub com `reference/x/index.md` =
   `---\nlocal: True\n---` → o gerador devolve `"locais":[]` e a lista sai sem `reference/x/**`. Nota válida no
   verificador, pasta replicada. Conserto: ler com `separar` e `dados.local === true`; teste com `True`, `TRUE`
   e fechamento com espaço.

### Execução de ponta a ponta

`sincronizador.ps1` rodado pelo Fiel às ~20:35: os 7 primeiros casos PASSA; depois o gerador caiu
(`pastas.filter is not a function`, linha 57) porque o worktree estava sendo editado durante a rodada
(mudanças não gravadas em `gerar-exclusoes.mjs` e `gerador.test.mjs`). Não vale como evidência contra d45be5d.
Repito os 14 casos e o `-SoPonto` no commit da próxima rodada. Contêineres e pasta hub-ensaio-06 apagados.
Log: `etapas/01-esqueleto/revisao-06-r1-sincronizador.log`.

### Fielzinho

No limite de uso do Codex até 20:26; leitura dele pendente. Entra na próxima rodada.

### Pedido para a rodada 2

Não editar o worktree enquanto a revisão roda; pedir a rodada com o commit.

## Rodada 2 — 2026-10-16 — ramo ticket-06 em b7cd714

Veredito: **passa**. Sem consertos.

Conserto 1 conferido: `pastasLocais` lê com `separar` (`lib/frontmatter.mjs`) e `dados.local === true`; YAML
ilegível em `index.md` recusa com código 2, sem gravar (falha fechada, melhor que pasta vazando).
Evidências (rodadas pelo Fiel, worktree limpo):
1. `gerador.test.mjs`: 7/7 (novos: `True`, `TRUE`, fechamento `--- `, texto `"true"`, YAML inválido).
2. `sincronizador.ps1`: 14/14, saída 0. Log `revisao-06-r2-sincronizador.log`.
3. `sincronizador.ps1 -SoPonto`: 6 FALHA, saída 1, e só os arquivos de `labs/` e `rascunho-local/` vazam; nada com
   ponto. O teste distingue. Log `revisao-06-r2-so-ponto.log`.
4. Sem contêiner nem pasta hub-ensaio-06 depois das duas rodadas.

Ressalvas (do relatório, decisões do Gustavo, não do ticket): pasta local nova criada com o CLI rodando vaza
(parar, gerar, religar); quem roda o gerador depois da instalação; exclusão do git; limpeza ao pôr `local: true`
numa pasta que já replicou. Um `index.md` ilegível em qualquer pasta trava a atualização da lista inteira: quem
chama (kit, vigia) precisa mostrar o erro, não engolir.

Fielzinho: no limite de uso do Codex até 20:26; a leitura dele fica para depois. Se ele achar algo, entra como
ressalva para o Rebite.

### Fechamento conjunto — ticket 06, rodada 2

Fielzinho leu depois do limite (`etapas/06-gerador-de-exclusoes/parecer-Vela-fielzinho.md`): **passa** em b7cd714,
7/7 rodados por ele, meus logs conferidos. Limpeza do Fiel: sem contêiner nem pasta hub-ensaio-06 depois das duas
rodadas da r2. Ressalvas dele (pasta local criada com o CLI rodando; índice real da busca) já constam acima.
Veredito conjunto: **passa**, Fiel e Fielzinho de acordo.
