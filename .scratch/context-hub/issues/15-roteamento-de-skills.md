# Roteamento de skills

Type: grilling
Status: resolved
Blocked by: 14

## Question

Como as skills moram no hub e ficam visíveis em todos os harnesses das duas máquinas, e o que entra na
tabela de roteamento (só o que a descrição da skill não resolve)? Primeiro caso de teste: a skill do
freellmapi-mcp tem de ser encontrada e usada sem o Gustavo pedir (Q16).

## Comments

- 2026-10-02 (vinda de "Workloads piloto"): a skill `armis-docx` do vault vai ser copiada para o hub
  nas primeiras fases e melhorada lá; o roteamento precisa alcançá-la.
- 2026-10-15 (vinda do "Laço do system design"): **retrato do uso real de skills instaladas por descrição**, para este
  ticket. Os quatro recrutas da equipe de design tinham a suíte no escopo de projeto (`.maestri/roles/<id>/.claude/skills/`),
  esperando invocação autônoma pela `description`. Nos registros das sessões: o Skill tool disparou 2 vezes em toda a
  frente (Tech lead, `regua-da-cidade`); o resto foi leitura direta dos arquivos que os briefs citavam (`regua-da-cidade`,
  `medidas-da-peca`). Nunca usadas: os seis `critique-*` do UX revisor (que reprovou a affordance sem rodar
  `critique-affordance`), as `law-of-*`, `spacing-system`, `visual-hierarchy`, `web-design-engineer` e `emil-prototype` do
  UI engineer, `information-architecture` e `concept-selection` do Tech lead, `break-ui` do QA. Conclusão de partida: a
  descrição sozinha não basta para a skill disparar; o roteamento precisa dizer qual skill em qual passo. O Gustavo
  deixou o roteamento da frente para este ticket ("deixe esse roteamento de skills pro ticket 15").
- 2026-10-15 ~20h40: desbloqueado (ticket 14 resolvido: skills em `agents/skills/`, junction em `~/.claude/skills` e
  `~/.agents/skills`). **Rodada 1 aberta** (`portal/rodadas/2026-10-15-roteamento-de-skills-r1.md`): como a skill certa
  dispara (recomendada A: tabela `agents/skills/routing.yml` com só o que a descrição não resolve + hook de entrada sem IA
  que injeta "use a skill X" + briefs citando a skill + verificador que registra sem obrigar). Fontes: docs de hooks do
  Claude Code (`additionalContext`, `Stop`) em `exploracao/anexos/pesquisa-44-guarda-do-acervo.md`; extensão
  `onUserPromptSubmitted` do Copilot CLI na bancada de acesso. Não verificado: injetar contexto pelo hook de entrada no
  Codex e no Copilot; saber se a skill rodou nesses dois.
- 2026-10-15 20:39, **rodada 1 respondida** (envio `327bd044-59bd-4ba2-a48e-5d3500e50b11`): **disparo = A** (a
  recomendada). A tabela `agents/skills/routing.yml` guarda só o que a descrição não resolve: gatilho (palavras do
  pedido, tipo de nota pelo caminho, papel do recruta) → skill. Um hook de entrada sem IA confere a tabela e injeta
  "use a skill X". Os briefs e as skills de processo citam a skill pelo nome em cada passo. O verificador do fim
  registra se a skill indicada rodou, sem obrigar, e o registro aponta a linha da tabela a ajustar. Algo mais: em branco.
- 2026-10-15 ~20h45: **rodada 2 aberta** (`portal/rodadas/2026-10-15-roteamento-de-skills-r2.md`): quais skills cada
  agente enxerga (recomendada A: duas camadas, as de uso geral pela junction global e as de papel só na pasta do papel,
  pela receita; o GSD sai do escopo global com cópia). Contagem desta máquina: 121 em `~/.claude/skills` (72 do GSD),
  117 em `~/.agents/skills`. Fonte: docs de skills do Claude Code (nome e descrição no contexto a cada turno; escopos
  pessoal e de projeto), em `exploracao/anexos/pesquisa-39-beneficios-claude-code/02-claude-code-recursos.md`.
- 2026-10-15 20:42, **rodada 2 respondida** (envio `48ab1f38-5c28-48da-9a14-fa9eda190871`): **escopo = A** (a
  recomendada): duas camadas. A junction global leva só as skills de uso geral (a busca, o FreeLLMAPI, o fluxo do Matt
  Pocock, a família `maestro-*` e as poucas que servem a qualquer trabalho); as de um papel ficam no acervo e entram só
  na pasta daquele papel, pela receita de setup; o kit tira o GSD do escopo global, com cópia antes; a tabela cobre as
  duas camadas. Algo mais: em branco.
- 2026-10-15 ~20h45: **rodada 3 aberta** (`portal/rodadas/2026-10-15-roteamento-de-skills-r3.md`), a última: quem
  ajusta a tabela quando o registro aponta erro (recomendada A: proposta em `agents/maestro/propostas/`, entra com aval).
  Registrado sem pergunta, para a construção: onde o hook de entrada não injetar (Codex, Copilot), a linha vira regra no
  contrato daquele harness (como a checagem de início, ticket 14); teste de aceite: pedido de pesquisa sem citar o
  FreeLLMAPI faz a skill dele disparar.
- 2026-10-15 20:44, **rodada 3 respondida** (envio `10ce972b-4064-4113-83a3-bc1ce489e27b`): **ajuste = B** (a
  recomendada era A): o maestro corrige a tabela sozinho a partir do registro e avisa em uma linha. Consequência para a
  construção: a guarda do acervo ("Maestri: padrão e liberdade", aval para alterar) abre exceção para o maestro em
  `agents/skills/routing.yml`. Algo mais: em branco. Ticket resolvido.

## Answer

**A skill certa dispara por uma tabela de roteamento e um hook de entrada, e cada agente enxerga só as skills de uso
geral mais as do seu papel** (rodadas 1 a 3, 2026-10-15; onde as skills moram veio de "Acesso dos agentes: decisão").

- **Onde moram (ticket 14):** em `agents/skills/` no hub, ligadas por junction em `~/.claude/skills` (Claude Code) e
  `~/.agents/skills` (Codex e Copilot), nas duas máquinas.
- **Disparo (rodada 1, A):** a tabela `agents/skills/routing.yml` guarda só o que a descrição não resolve: gatilho
  (palavras do pedido, tipo de nota pelo caminho, papel do recruta) → skill. Um hook de entrada sem IA confere a tabela
  e injeta "use a skill X" no contexto. Os briefs e as skills de processo citam a skill pelo nome em cada passo. O
  verificador do fim registra se a skill indicada rodou, sem obrigar. Motivo: na frente da cidade, com a suíte
  instalada, a ferramenta de skill disparou só 2 vezes; a descrição sozinha não basta.
- **Escopo (rodada 2, A):** duas camadas. A junction global leva só as de uso geral (a busca, o FreeLLMAPI, o fluxo do
  Matt Pocock, a família `maestro-*` e as poucas que servem a qualquer trabalho). As de um papel ficam no acervo e
  entram só na pasta daquele papel, pela receita de setup. O kit tira o GSD do escopo global, com cópia antes. A tabela
  cobre as duas camadas.
- **Ajuste (rodada 3, B):** o maestro corrige a tabela sozinho pelo registro e avisa em uma linha; a guarda do acervo
  abre exceção para ele nesse arquivo.
- **Para a construção:**
  - onde o hook de entrada não injetar (Codex e Copilot, não verificado), a linha vira regra no contrato daquele
    harness, como a checagem de início;
  - saber, no fim da resposta, se a skill rodou no Codex e no Copilot (não verificado);
  - teste de aceite: um pedido de pesquisa que não cita o FreeLLMAPI faz a skill dele disparar;
  - a skill `armis-docx` copiada do vault entra na tabela;
  - o retrato da frente da cidade (skills de design por papel) é o primeiro conjunto de linhas de papel.
