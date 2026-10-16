---
titulo: Como a skill certa dispara na hora certa
ticket: 15
aberta: 2026-10-15
estado: absorvida
---

O ticket "Acesso dos agentes" já decidiu **onde as skills moram**: em `agents/skills/` no hub, ligadas por junction em
`~/.claude/skills` (Claude Code) e `~/.agents/skills` (Codex e Copilot), nas duas máquinas. Falta decidir **como a skill
certa dispara**. O primeiro caso de teste é a skill do FreeLLMAPI, que tem de ser usada sem você pedir.

**O que pesa:**
- **A descrição sozinha não basta.** Na frente da cidade do hub, os quatro recrutas de design tinham a suíte de skills
  instalada. A ferramenta de skill disparou só 2 vezes. Os seis `critique-*` do UX revisor nunca rodaram, nem quando ele
  reprovou a affordance. O que funcionou foi o brief citar o arquivo da skill pelo nome.
- **Regra escrita no `AGENTS.md` falha com agente menor** (você, na rodada 17 do ticket 12), e por isso o frontmatter
  ficou imposto por mecanismo.
- **Há mecanismo nos três harnesses.** Os três têm hook na entrada do pedido (`UserPromptSubmit`; no Copilot CLI, a
  extensão `onUserPromptSubmitted` disparou na bancada de acesso). No Claude Code, esse hook injeta contexto
  (`additionalContext`: "wraps the string in a system reminder"), e o `Stop` pode fazer o agente continuar. Não
  verificado: injetar contexto pelo hook de entrada no Codex e no Copilot, e saber, no fim da resposta, se a skill rodou
  nesses dois.

## Como o hub faz a skill certa disparar
id: disparo
tipo: escolha
recomendada: A

- A: Tabela de roteamento e hook de entrada. Uma tabela em `agents/skills/routing.yml` guarda só o que a descrição não resolve: gatilho (palavras do pedido, tipo de nota pelo caminho, papel do recruta) → skill. Na entrada de cada pedido, um hook sem IA confere a tabela e injeta "use a skill X" no contexto. Os briefs e as skills de processo citam a skill pelo nome em cada passo. O verificador do fim registra se a skill indicada rodou, sem obrigar, e esse registro mostra qual linha da tabela precisa de ajuste
- B: Como a A, mas obrigando: se a tabela indicou uma skill e ela não rodou, o verificador do fim faz o agente voltar e rodá-la. Mais garantido, mas força skill quando o gatilho casou por engano
- C: Só texto: a tabela fica no `AGENTS.md` da raiz, e os briefs citam a skill pelo nome. Sem hook, mais simples de construir, e o mesmo arranjo que falhou na frente da cidade

## Algo mais?
id: algo-mais
tipo: texto
