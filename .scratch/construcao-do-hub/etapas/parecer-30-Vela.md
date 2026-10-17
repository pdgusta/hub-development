# Parecer do Fiel — ticket 30, o montador mostra a falha do git (Vela)

## Rodada 1 — 2026-10-17 — ramo ticket-30 em ca5b389

Veredito: **passa**. Revisado pelo Fiel sozinho; leitura do Fielzinho fica para depois (cota), por ordem do maestro.

Conferido: integracao f83c8f5 ancestral; worktree limpo. Diff lido: `montar.mjs` imprime comando, saída (código ou
sinal), stdout, stderr e `r.error`; as asserções que montam hub mostram `stdout + stderr`; o 05 usa `updated` de hoje
nos dois testes que comparavam com data fixa (commit separado, só teste, aval do maestro).

Evidências (Fiel): `node --test 04-esqueleto 05-frontmatter 27-pastas`: 46/46 (inclui os dois testes novos do
montador: sem git no PATH → nomeia `git init` e traz `ENOENT`; `GIT_INDEX_FILE` inválido → nomeia `git add -A` e
traz o stderr do git). Critérios 1 e 2 atendidos.

Critério 3 (suíte verde): não rodei a suíte inteira (regra "um trabalho pesado por vez"; a Vela a repete agora). O
vermelho relatado é só o 12-busca por tempo ("não ficou pronta em 3 minutos"), sob memória no limite; o 30 não toca a
busca, e o 12-busca sozinho passou 9/9. Se a repetição da Vela vier com vermelho fora do 12-busca, a rodada reabre.

Ressalva: a espera de 3 minutos do 12-busca falha sob carga (já visto na junção do 15); é do dono do 12.
