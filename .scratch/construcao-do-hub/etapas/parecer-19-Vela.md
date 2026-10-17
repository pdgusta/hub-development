# Parecer do Fiel — ticket 19, roteamento de skills (Vela)

## Rodada 1 — 2026-10-17 — ramo ticket-19 em 52c6328

Veredito: **passa**, sem consertos. Revisado pelo Fiel; leitura do Fielzinho fica para depois (cota do Codex), por
ordem do maestro. Se ele achar algo, entra como ressalva para o Rebite.

Conferido: integracao d5e4e16 ancestral; worktree limpo. Li o ticket 19, o relatório, `routing.yml`,
`roteamento/entrada.mjs`, `registro.mjs`, `sessao.mjs`, `lib/roteamento.mjs` (`indicar`, `papelDe`) e a ligação no
`fim-da-resposta.mjs` do 27 (num `try` próprio, só quando solta).

Evidências (Fiel):
1. `node --test agents/code/test/19-roteamento.test.mjs`: 16/16.
2. Critérios: pesquisa sem citar o FreeLLMAPI recebe "use a skill `freellmapi`" no Claude Code e no Codex (testes e
   ponta a ponta); no Copilot a saída do `userPromptSubmitted` de arquivo é descartada (doc citada no relatório), e a
   indicação vai pela regra do contrato (texto entregue à faixa 1) — decisão 4 do maestro. A tabela passa no esquema
   (`verificar-roteamento`). Uso de skill vira linha em `agents/maestro/uso/<máquina>.md`.
3. Sonda de costura com o 27: 12 fechamentos de turno geram `agents/maestro/uso/pc.md`; `verificar-frontmatter`
   sai 0 (só o aviso "caminho sem tipo") e `verificar-pastas` não dá falta. O fim da resposta não devolve o agente por
   causa do registro que o próprio hook escreve.
4. Ponta a ponta real: não repetida (regra provisória e cota); evidência `evidencia-19/` e hashes (nenhum mudou)
   conforme o relatório.

Ressalvas (não seguram):
- `fim-da-resposta.mjs` importa `registro.mjs` no topo, fora do `try`: um erro de carga do roteamento derrubaria o fim
  inteiro. Import dinâmico dentro do `try` isolaria.
- `dentroDoHub` compara caminhos em minúsculas, sem resolver junction (o 14 resolve com `realpathSync.native`).
- Uso e "rodou" no Codex e no Copilot: não verificado (sem evento nas docs); "sem rede" garantido só pelo código.
- O gatilho `pesquis` casa qualquer pedido de pesquisa; ajuste pelo registro (decisão do 15).
