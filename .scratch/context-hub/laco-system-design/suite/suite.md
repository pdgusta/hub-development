# Suíte de skills de design (aprovada)

Aprovada pelo maestro em 2026-10-15, na volta 2 de 3. O conteúdo completo está em `categorias-v2.md`: suíte por papel,
`.claude/settings.json` de cada papel, as duas skills nossas e, para cada cópia, a origem, as alterações e a
invocação. A versão 1 e o julgamento estão em `categorias.md` e `julgamento-v1.md`. A suíte entra no acervo do
maestro quando o acervo existir no hub; até lá, mora aqui.

## Por papel (25 skills distintas: 23 copiadas, 2 nossas)

- **UI engineer (14):** web-design-engineer (editada), parallel-concepts, emil-prototype (manual), as cinco
  `law-of-*`, visual-hierarchy, spacing-system, better-colors, better-typography, better-writing, regua-da-cidade.
- **UX revisor (8):** as seis `critique-*`, better-writing, regua-da-cidade.
- **Tech lead (3):** concept-selection, information-architecture (sem card sort nem tree test), regua-da-cidade.
- **QA tester (4):** better-accessibility (só relata), break-ui (numa cópia), regua-da-cidade, medidas-da-peca.

## Decisões do maestro na aprovação

1. **Limiares da régua:** sem pergunta ao Gustavo, que pediu para não escolher. Valem como primeira calibragem, e o
   Tech lead e o UX revisor podem propor ajuste depois dos primeiros conceitos, com o motivo.
   - R1: nenhum cruzamento entre ligações, salvo em ponto de encontro marcado.
   - R2: na visão geral, no máximo 25 rótulos visíveis.
   - R3: folga mínima entre itens vizinhos de 1 altura de rótulo; o espaço entre grupos é pelo menos 1,5 vez o de
     dentro do grupo.
2. **Referências da régua** (capturas a fazer na etapa da equipe, com o Edge sem cabeça):
   - **Elogiadas:**
     - `prototipos/prototipo-09-roteamento-da-pesquisa.html`, o mapa de metrô (diagrama no centro, texto só em
       rótulos);
     - `laco/painel/index.html`, a maré de novos (uma metáfora que carrega a pergunta, números grandes, pouco texto);
     - o portal v2 "Mesa de mapas", pela leitura (fonte confortável, aconchego).
   - **Recusadas:**
     - `laco/painel/sintese.html`, o laudo (texto demais) e a v2 dele (só restilizou);
     - a cidade radial v2 do system design ("poluído, precisa de distância");
     - a "trilha até o cume" do portal (triângulos soltos sem sentido).

   Cada captura vai com uma linha dizendo por que foi elogiada ou recusada, tirada das palavras do Gustavo.
3. **Plugins sincronizados e superpowers desligados** na pasta de cada papel, pelo `settings.json` da v2. Conferido em
   cada recruta ao subir: se `design:*` ainda aparecer, usar `syncClaudeAiPlugins: false` no `.claude/settings.local.json`
   do papel.
4. **Cópias:** ao copiar, fixar de novo o commit, ler inteiros os corpos ainda não lidos (`emil-prototype`, `break-ui`,
   as referências do `web-design-engineer`, o `check_contrast.py`) e levar o `LICENSE` junto.
