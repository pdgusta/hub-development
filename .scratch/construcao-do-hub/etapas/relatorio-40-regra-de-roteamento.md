# Relatório do ticket 40: a regra de roteamento no AGENTS.md (Vela)

Ramo `ticket-40`, worktree `C:/context-hub-wt/ticket-40`, de `integracao` e7203b4.

## O que mudou

- `AGENTS.md`: seção nova `## Roteamento de skills`, no corpo (depois de `<!-- cabeca:fim -->`), com o texto da regra
  do relatório do 19 ("Texto da regra no contrato"), dito para o Copilot CLI: ler `agents/skills/routing.yml` antes do
  pedido e usar as skills da linha que casa (palavras, caminho, papel), salvo se o pedido já cita outra skill.
  Mudança de redação: uma frase a mais diz que no Claude Code e no Codex o hook já indica.
- O hub de ensaio copia o `AGENTS.md` da raiz (`montar.mjs`, `ESQUELETO`): traz a mesma regra sem mexer no montador.
- A cabeça não mudou: 1.691 de 2.000 (`node agents/code/bin/conferir-cabeca.mjs .`).

## Teste

- Costura: o `AGENTS.md` do hub de ensaio montado pelo `montar.mjs`. Teste novo no fim de
  `agents/code/test/19-roteamento.test.mjs`: a seção está no corpo, aponta `agents/skills/routing.yml`, não entra na
  cabeça, e a cabeça segue no limite (`conferirCabeca`). Vermelho antes da seção, verde depois.
- `node --test agents/code/test/19-roteamento.test.mjs agents/code/test/04-*.test.mjs agents/code/test/21-*.test.mjs`:
  **52/52**. Suíte inteira: na junção (Rebite).

## O que vai doer na junção

- O ticket 18 também acrescenta uma seção (`## Retomada`) logo depois de `<!-- cabeca:fim -->` e uma linha na cabeça.
  As duas inserções caem no mesmo ponto: conflito de texto simples; manter as duas seções (Retomada, depois
  Roteamento) e conferir a cabeça de novo.

## Não verificado

- Se o Copilot de verdade segue a regra (sem harness real neste ticket; o uso de skill no Copilot já era "não
  verificado" no 19).
