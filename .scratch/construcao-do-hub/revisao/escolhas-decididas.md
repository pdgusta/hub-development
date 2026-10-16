# As 23 escolhas sem ticket: o que o Gustavo decidiu

Numeração da seção (c) do `acordo.md`. Quando as quatro rodadas fecharem, o maestro troca as marcas **[núcleo]** do
spec pela decisão (e escreve o que mudou), numa passada só.

## Carta 2: vigia e manutenção (rodada `2026-10-16-escolhas-do-spec-carta-2`, 16:33, todas A)

- 6. Estado da vigia em `.local/vigia/estado.json`, troca atômica, nível por item, geral = pior: **aceita**.
- 7. Endereço da outra máquina só como sinal; incerto = "informa" com motivo, nunca "ok": **aceita**.
- 8. Falha da cópia diária sai alto (erro, item na vigia, notificação): **aceita**.
- 9. Data no nome da pasta arquivada (`_archive/AAAA-MM-DD--nome/`): **aceita**.
- 10. Limpeza desenhada na tarefa diária, só simulando: **aceita**.
- 22. Avisos do Codex com regra: os dois continuam e **não se repetem enquanto o estado não muda** (muda o spec: a
  política deixa de ser "se houver").

## Carta 1: gravar e ler no banco (rodada `2026-10-16-escolhas-do-spec-carta-1`, 16:52)

- 1. Conflito visível nos dois jeitos (aviso ao ler e `get_conflicts`): **aceita**.
- 2. Cabeça do contrato: bloco do `AGENTS.md` relido a cada conexão, antes do texto do MCP: **aceita**.
- 3. Regra curta: primeira frase em todas, segunda só em gravar e editar; apagar e mover a definir: **aceita**.
- 4. Nome `estado_do_hub`: **aceita**.
- 5. **Mudou (B): três instâncias do MCP do banco por máquina**: leitura, escrita dos agentes da máquina e uma de
  escrita só para o cliente, separada (muda o spec: o núcleo dizia duas, com a de escrita reaproveitada no proxy).
- 21. Caminho ofuscado na cifra de ponta a ponta: **aceita**.

## Carta 4: ficha, porteiros e acervo (rodada `2026-10-16-escolhas-do-spec-carta-4`, 17:14)

- 14. Verificador só completa o dedutível, relendo antes de gravar: **aceita**.
- 15. Porteiro monta a nota final antes de validar: **aceita**.
- 16. Fim de resposta sem modelo: **em aberto**. O Gustavo perguntou "pq essa opção não é um hook ou claude mod, mas sim
  um script?". Resposta: é hook e mod (decisão do acesso dos agentes: mod no Claude Code, hook `Stop` no Codex,
  `agentStop` no Copilot); "script" na carta era quem julga dentro dele (regra fixa × modelo). Volta em rodada nova
  (`2026-10-16-escolhas-do-spec-carta-4-r2`), sem mudar a carta.
- 17. Lembrete e guarda do acervo em qualquer pasta: **aceita**.
- 18. `COPILOT_SKILLS_DIRS` no ensaio: **aceita**.
- 19. `initiative` só em nota de iniciativa: **aceita**.
- 20. **Mudou (B): o `AGENTS.md` da iniciativa nasce à mão**, quando houver regra própria; o script "nova iniciativa"
  não o cria (muda o spec).

## Carta 3: a busca (rodada `2026-10-16-escolhas-do-spec-carta-3`, 17:21)

- 11. **Ajustada pelo Gustavo:** a nota certa entre as 3 primeiras reprova se falhar; o tempo até a nota nova aparecer
  **só é medido**, sem limite de 60 s (muda o spec).
- 12. Contagem e lista das recusadas por cabeçalho quebrado: **aceita**.
- 13. Duas regras de exclusão de tudo com ponto na própria ferramenta: **aceita**.
- 23. Endereço observado atrás do proxy: **aceita**.
- 16 (rodada `2026-10-16-escolhas-do-spec-carta-4-r2`, 17:39): **aceita**: regra fixa, sem IA, dentro do mod e dos hooks
  do fim da resposta ("a nota de retomada mudou?").

## Aplicado no spec (2026-10-16, ~18h)

As 23 escolhas estão decididas. O maestro trocou toda marca **[núcleo]** por **[aceita]** (legenda no topo do
`spec.md`) e escreveu as quatro mudanças do Gustavo: três instâncias do MCP do banco por máquina (núcleo, faixas 3-4,
5-6 e 9-10); o `AGENTS.md` da iniciativa à mão (faixa 1, e saiu o ponto aberto); o tempo da busca só medido (núcleo e
faixa 3); avisos do Codex sem repetição enquanto o estado não muda (núcleo e faixa 7). Cópia de antes desta passada em
`revisao/antes-das-escolhas/`.
