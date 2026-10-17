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

## Rodada nova — 2026-10-17 ~07h45 — ramo ticket-15 em 3d34bd1 (com integracao 9cc878b)

Veredito: **PASSA**, em acordo com o Fielzinho (`parecer-15-Trilho-fielzinho.md`: passa, 9/9, registros reais dos três
conferidos, sem bloqueio novo).

Conferido pelo Fiel:
- integracao 9cc878b ancestral; árvore limpa antes e depois. `node --test agents/code/test/15-leitura.test.mjs`: 9/9.
- Só a search (46e44d2, c1b6133, do 12). Ressalva 2 do 12 r3 feita (3bc8c8b): o `settings.json` de ensaio do Claude
  junta o hook e o deny do `claude-settings.json`.
- 03f85fb: `sandbox_mode = "danger-full-access"` só no `config.toml` da casa de ensaio, como 14, 19, 20 e 27.
- 64d6875: no Codex o hook recebe `mcp__hub_busca__search` (hífen vira sublinhado). Matcher e adaptador do Codex
  trocados; Claude segue com `mcp__hub-busca__search` (evidência dele passa). Nenhum outro hook do Codex casa nome MCP
  hoje (grep em `agents/code/hooks` e `kit`).
- Evidência do Codex (0283b2c): `registro.jsonl` com "busque antes" na leitura inteira sem busca, trecho apontado
  calado, arquivo apontado lido inteiro com "leia o trecho", e a segunda leitura do mesmo arquivo calada (uma vez por
  arquivo). `apagado: true` nos hashes do Codex e dos três.

Ressalva nova (não segura): **nome MCP com hífen no Codex chega ao hook com sublinhado.** Todo matcher futuro do
Codex para `hub-banco` ou outro servidor com hífen precisa do nome com sublinhado (vigia, guarda). Vale avisar o maestro
para virar nota comum. Ressalvas da rodada 1 mantidas.
