# Parecer do Fiel — ticket 15, aviso de leitura fora da busca (Trilho)

## Rodada 1 — 2026-10-17 — ramo ticket-15 em c789b9d

Veredito: **passa**. Revisado pelo Fiel sozinho; leitura do Fielzinho fica para depois (cota do Codex), por ordem do
maestro. O aceite real do Codex fica pendente, em commit só de evidência com rodada curta (como no 12).

Conferido: integracao c5b946a ancestral; worktree limpo. Li o ticket 15, o relatório (medida de "grande" só em
agregados, sem caminho nem nome), `leitura.mjs`, os fragmentos e a única mudança no 14 (`relativoAoHub` exportado).
`node --test agents/code/test/15-leitura.test.mjs`: 9/9; `git status` vazio depois.

Critérios: arquivo grande lido sem busca avisa uma vez por arquivo por sessão (testes nos três adaptadores e ponta a
ponta Claude/Copilot pela evidência); trecho apontado lido em trecho fica calado. Nunca recusa (PostToolUse/postToolUse,
doc citada; o `preToolUse` do Copilot falha fechado e foi evitado de propósito).

Ressalvas (não seguram):
- O aviso "busque antes" sai também para o que a busca nunca indexa: caminho com ponto, pasta `local: true` e arquivo
  que não é `.md` (o adaptador do Claude e do Copilot não filtra extensão). Conselho impossível de seguir; calar
  nesses casos (a lista do gerador do 06 diz o que fica fora).
- `HUB_LEITURA_GRANDE` inválido vira `NaN` e cala o aviso sem dizer.
- Estado por sessão em `.local/leitura/` sem limpeza (declarado); leitura por shell do Codex só pelos comandos
  reconhecidos (declarado).
