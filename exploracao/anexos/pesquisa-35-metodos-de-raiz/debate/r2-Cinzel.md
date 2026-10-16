# r2 — Cinzel (lente: sistemas e agentes)

## O que já dá para fechar

**Arquivo (8): convergimos.** Junco perguntou o que sustenta 8 como raiz além do PARA. Nada. Cline e
`.claude` não dizem nada sobre envelhecer (`10-cline-memory-bank.json`, `15-diretorio-claude.json`),
e FHS e XDG não têm regra de expiração, salvo runtime (`08-fhs.json`, `09-xdg.json`). Só
`01-para.json` tem `Archives` de topo, e `01-para.json` não trata de replicação. Concordo com Junco
e Astrolabio: arquivar é estado dentro de cada raiz, herdando a declaração. Junco admite que o
`_arquivo/` por raiz é inferência dele; eu a sustento pelo FHS (`08-fhs.json`): arquivo único
misturaria os dois valores de replicação, e o GLOSSARY exige um valor por pasta.

**Entrada (7): concordo com Junco**, não replicada por padrão. Ganho adicional: o ciclo "esvaziar em
dias" combina com runtime do XDG, "MAY be subjected to periodic clean-up" (`09-xdg.json`). Custo que
ele não nomeou: a outra máquina não vê a captura (GLOSSARY, "Pasta não replicada"). Para uma entrada
que esvazia em dias, aceito o custo.

**Referência (5): concordo com a regra do Junco** (dado de cliente nunca mora em 5, só sobe
sanitizado). É a promoção explícita do briefing, e o precedente de sistema é o XDG: a versão do
usuário sobrescreve a compartilhada, não o contrário (`09-xdg.json`).

## Onde mudo de posição

**Operações contínuas (2): saio da fusão com 1.** Na r1 eu disse que só o PARA sustenta a separação.
Junco e Astrolabio mostraram que o briefing define tipo por comportamento próprio: "termina?" e "o
que acontece quando envelhece" (briefing). 1 vai para arquivo, 2 compacta. Isso é comportamento, não
estilo. O custo é duas raízes a declarar como não replicadas; aceito. Mantenho que a separação vem do
PARA (`01-para.json`) e não de sistema.

## Onde discordo

**Junco, oficina (6).** Você lista 6 como replicado e mantém inteiro. Pelo seu próprio teste do FHS
(`08-fhs.json`), não passa: contrato, skills e papéis são compartilháveis, mas perfil de máquina é
específico da máquina. O `.claude` separa as duas coisas: `settings.json` do projeto no git e
`~/.claude.json` com sessão e decisões de confiança "that does not belong in settings.json"
(`15-diretorio-claude.json`). Seu `config × data` do XDG (`09-xdg.json`) reforça a separação, não a
fusão. Proposta: 6 fica, o perfil de máquina sai para dentro da pasta não replicada (ou para um `_maquina/`
declarado não replicado dentro de 6). Falta decidir qual dos dois, e isso é do ticket 12.

**Astrolabio, estudo (4) e produtos (3).** Você diz que o PARA põe estudo em Resources e que a
tabela é mais fina. Mas Resources juntaria 4 com 5 (referência), e 4 termina, 5 não (briefing). Meu
argumento pelo GLOSSARY: iniciativa tem "identificador estável, estado e próxima ação", e uma
certificação ou um spike é isso. Então 3 e 4 são iniciativas sem cliente, replicadas, que só diferem
por estado, e o estado vai para o frontmatter (o briefing diz que o frontmatter leva o que a busca
usa). Isso também desfaz sua tensão em 3: o PARA não decide "por versão", mas a propriedade de
replicação separa 3 de 1 e 2 sem precisar do PARA. Junco chamou a evidência de 4 de "fraca"; concordo, e
tiro a conclusão: juntar 3 e 4. Se vocês provarem que "promover ou arquivar" muda o caminho ou o
leitor, mudo.

## O que falta, de que ninguém tratou

1. **O caminho fixo está fora do hub.** `.claude/` do projeto e `~/.claude/` são os lugares que o
   harness lê (`15-diretorio-claude.json`). Como a pasta do hub vira esse caminho não está em nenhum
   JSON; fica "não verificado" e vai ao ticket 12.
2. **Regra de carga não é garantia.** "Rules are guidance Claude reads, not configuration Claude Code
   enforces" (`15-diretorio-claude.json`). O hook da nota de retomada precisa de settings/hook do
   harness, não de pasta.
3. **Raiz mínima.** Aplicações nunca criam arquivos ou subdiretórios na raiz (`08-fhs.json`). A
   consequência para o MCP: gravar só em raízes declaradas, nunca criar raiz nova.

## Posição atual (nove)

1 manter · 2 manter, separado · 3+4 juntar · 5 manter, sem dado de cliente · 6 manter, perfil de
máquina fora · 7 manter, não replicada · 8 cortar, `_arquivo` por raiz · 9 aguardar o Gustavo.

**Pergunta a Astrolabio e Junco:** `_arquivo/` por raiz ou propriedade `estado` no frontmatter? O
FHS pede pasta, mas a busca só enxerga a propriedade.
