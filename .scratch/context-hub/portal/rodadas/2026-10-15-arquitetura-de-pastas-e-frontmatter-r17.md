---
titulo: Os quatro últimos pontos da árvore de pastas
ticket: 12
aberta: 2026-10-15
estado: absorvida
---

Com a rodada dos índices, anexos e títulos, a árvore de pastas e o frontmatter estão quase fechados. Ao rascunhar o
resumo final do ticket, sobraram quatro pontos que a pergunta original pede e nenhuma rodada respondeu. Depois deles, o
ticket se resolve, e o `system-design.html` é atualizado.

Em que esta rodada se apoia, já decidido:
- tudo replica nas duas máquinas, inclusive o conteúdo de cliente; o perfil de cada máquina é um arquivo, sem pasta
  própria;
- o que tem ponto no nome (`.secrets/`, `.maestri/`, `.git`) não vai ao banco nem à outra máquina ("Revisão do sync e
  da divergência", "Maestri: padrão e liberdade");
- o frontmatter só leva o que a busca ou o contrato usam; a busca pesa muito o `title` e, sem ele, usa o nome do arquivo;
- `index.md` em toda pasta que cresce, como sumário (a sua escolha na rodada anterior);
- falha se corrige com mecanismo, não com regra a lembrar; índice mantido à mão desatualiza ("Lições do vault");
- um verificador sem IA roda no fim de cada resposta e completa o que falta (o `title` do núcleo, o `log/` do mês).

## Como uma pasta fica só numa máquina
id: pasta-local
tipo: escolha
recomendada: A

- A: Não há pasta não replicada declarada: o que precisa ficar numa máquina só leva ponto no nome, e só isso. O glossário troca o termo "pasta não replicada" (hoje: "cada pasta declara", "alcançada por SSH") por essa regra
- B: Além do ponto no nome, uma pasta pode se declarar local por um arquivo marcador dentro dela, que o sync e a busca respeitam. Mais construção, sem uso conhecido hoje

## O frontmatter das notas que não são ficha, núcleo nem anexo
id: frontmatter-demais
tipo: escolha
recomendada: A

- A: Livre, só com YAML válido (o verificador avisa o inválido). Os `index.md` ganham `title` pelo verificador, com a pasta e a iniciativa ("Índice · runs · VOEGOL cross-tenant"), para não aparecerem todos como "index" na busca
- B: Livre, só com YAML válido, sem `title` nos `index.md`: na busca eles aparecem como "index", e o caminho da pasta não entra na busca por palavra

## Quem mantém o sumário das pastas que crescem
id: sumario-dono
tipo: escolha
recomendada: A

- A: O verificador mantém a lista de arquivos de cada `index.md` sozinho, e você ou o agente escrevem só o texto livre do topo. "Pasta que cresce" = a partir de 10 arquivos; abaixo disso, sem `index.md`
- B: O agente que cria ou move um arquivo atualiza o `index.md` à mão, e o verificador só avisa quando a lista não bate com a pasta. Também a partir de 10 arquivos
- C: Como a A, mas com outro limite para "pasta que cresce" (diga qual em "Algo mais?")

## O protótipo da árvore
id: prototipo
tipo: escolha
recomendada: A

- A: As cartas aprovadas no caminho (o núcleo e os blocos) bastam como protótipo; o desenho da árvore final entra no `system-design.html` quando o ticket for resolvido
- B: Antes de resolver, o Designer faz um esboço da árvore final com notas de exemplo (ficha com `aliases`, `work/`, `.secrets/`, os `index.md` e o texto dos anexos), numa carta para você aprovar

## Algo mais?
id: algo-mais
tipo: texto
