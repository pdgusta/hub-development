# Lições do Prisma: revisão do spec (2026-10-16)

## O que funcionou

- Um arquivo por pessoa por rodada. Ninguém gravou por cima de ninguém, e um `/clear` não perderia nada.
- Só o relator edita a proposta. Os votos ficaram limpos e a proposta não teve duas versões.
- Ids por mudança (`Prisma-n`, `Q-n`, `Sextante-n`). Votar "concordo com ajuste" num id é rápido e rastreável.
- Ler os tickets por inteiro, Comments incluídos. Várias decisões só estão nos Comments: R62 do 33 mudou o 34, a
  revisão do Desktop no 36, o "caminho ofuscado" testado no 48.
- As três marcas: [núcleo], [formato] e [ticket aberto: 56]. Elas separam o que é decisão, o que é escolha sem aval e o
  que é só do plano de execução. Nada precisou ser decidido pelos revisores.
- O diff `antes/` × `proposta/` nas rodadas 3 e 4. Pegou erros de propagação: o núcleo com texto antigo enquanto a
  parte já estava certa.
- Um Codex e dois Claude. O Sextante foi mais estrito sobre o que é decisão e o que é escolha; isso evitou promover
  escolha do núcleo a decisão.

## O que atrapalhou

- A primeira revisão (divergências) tratava o núcleo como fonte. O protocolo depois mudou a regra: núcleo não é
  ticket. Parte do trabalho foi reclassificar.
- A divisão dos tickets não seguia a divisão das faixas. Eu li os tickets do banco e do sync, mas conferi faixas que
  dependem dos tickets do Quadrante (14, 15, 40). Precisei abrir tickets de outro grupo.
- Cinco rodadas foram mais do que o necessário. O acordo de mérito fechou na rodada 2; as rodadas 3 a 5 foram
  conferência. Duas rodadas de mérito e uma de conferência bastariam.
- `maestri ask` espera a resposta e trava o terminal. Rodar em segundo plano resolveu.
- No Bash do Windows, `\v` num caminho dentro de string Python virou tabulação vertical e corrompeu o arquivo. Usar
  string crua ou a ferramenta de edição.

## Armadilhas que o spec e os tickets escondiam

- Decisões em ticket antigo trocadas por um mais novo só nos Comments: 08 → 33 (30 min → 15 min), 06 → 33 (GitHub só
  cópia), 36/42 → 15 (GSD sai), 36/40 → 14 (sem marcador de raiz), 16 → 11 (Desktop grava).
- O núcleo fechava "pontos abertos" das partes sem ticket: duas formas de conflito, cabeça relida a cada `initialize`,
  `estado.json`, data no nome da pasta. Pareciam decisão.
- "Se couber" escondia requisito de ticket: validação de frontmatter no MCP (12), Config Doctor (33), ponte do Desktop
  (11).
- O ticket 56 estava aberto, mas suas respostas apareciam como fonte na faixa 10.
- A E2EE com caminho ofuscado (48) quebra quem lê o CouchDB direto: o MCP e a vigia precisam da frase-senha para achar
  o caminho. Nenhuma parte dizia isso.
- A guarda do acervo no núcleo cobria `agents/maestro/**`, o que recusaria as propostas e o registro de uso que o 40
  manda gravar ali.
- "Duas instâncias" ou "três" do MCP do banco: o 11 e o 34 usam "segunda instância" para coisas diferentes.
- Portas de ensaio diferentes entre núcleo e partes (5986 × 5996, 5987 × 5997).

## Recomendações

- Para a próxima revisão: dividir os tickets pelas faixas que cada revisor confere, não por número.
- Uma rodada de mérito, uma de votos e uma de conferência por diff. Fechar cedo quando houver acordo.
- Fixar a regra "só ticket resolvido decide" antes da primeira leitura, não depois.
- Para o plano de construção: as escolhas [núcleo] da lista (c) do acordo pedem aval do Gustavo antes de construir; levar
  em blocos, não uma a uma.
- Resolver o ticket 56, ou registrar as respostas dele num ticket resolvido, antes de construir o que vem dele.
- Com etapas sequenciais: subir um banco de ensaio só para as faixas 4, 5 e 7, e fazer a faixa 5 antes da 7 (a vigia e a
  checagem usam o MCP como reserva).
- Testar primeiro o que é "não verificado" e pode derrubar o desenho: replicação de dois CouchDB com os documentos do
  LiveSync (34), `.livesync/ignore` com pastas com ponto aninhadas (48), hooks do Codex com `danger-full-access` (14).
- Manter as marcas na spec durante a construção: o worker que acha um [núcleo] sabe que é escolha, não lei.
