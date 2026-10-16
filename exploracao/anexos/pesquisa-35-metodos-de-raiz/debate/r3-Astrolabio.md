# Rodada 3: Astrolabio

## Fechado entre os três

- **8 Arquivo deixa de ser raiz.** Três de três (Cinzel r2, Junco r2, eu r2).
- **5 Referência sem dado de cliente**, só sobe sanitizado (regra do Junco; Cinzel concorda).
- **7 Entrada local, por máquina**, com o checkpoint como único ponto de saída (Junco, Cinzel; eu
  propus o mesmo na r2). Cinzel nomeou o custo: a outra máquina não vê a captura. Aceito.
- **6 Oficina com perfil de máquina fora.** Junco corrige bem: `15-diretorio-claude.json` diz
  "OAuth session, per-project trust decisions", ou seja, estado pessoal; "da máquina" é inferência.
- **2 separado de 1.** Cinzel saiu da fusão, Junco mantém. Registro: a evidência de método é só
  `01-para.json` (Projects × Areas). O destino "compactar" é do hub, não do PARA, que também manda
  área inativa para o arquivo (`01-para.json`).
- **Nota de retomada dentro da pasta de cada iniciativa** (Junco). Concordo: o PARA dá uma subpasta
  por projeto (`01-para.json`) e o Cline uma pasta por projeto (`10-cline-memory-bank.json`).

## Respondendo a Cinzel: `_arquivo/` por raiz ou propriedade `estado`?

**Propriedade `estado`, no mesmo caminho.** Três razões, todas da minha lente:

1. O Zettelkasten chama o endereço fixo da nota de "alpha e ômega": "tudo se torna possível por
   causa dele" (`04-zettelkasten.json`). Mover a iniciativa para `_arquivo/` muda o endereço e o
   lugar fixo da nota de retomada (restrição do briefing).
2. Steph Ango resolve a mesma tensão por propriedade e visão: `categories` mais Bases dão "um
   panorama" sem mover nada (`07-vault-steph-ango.json`). O que o Gustavo vê arquivado é visão, não
   pasta.
3. O FHS pede pasta quando difere replicação ou compartilhamento (`08-fhs.json`). Arquivada ou
   ativa, a iniciativa continua na mesma raiz e herda a mesma declaração. O eixo estático/variável
   do FHS existe para guardar em sistemas de arquivos diferentes (`08`); aqui não há segundo
   armazenamento.

Custo que assumo: a vista Markdown fica mais cheia, e a busca precisa excluir `estado: arquivado`
por padrão. Junco já disse que o frontmatter cobre a exclusão. Cinzel, se você tem um argumento do
FHS que ainda peça pasta, diga qual.

## Onde mudo

**3 e 4: junto, como Cinzel.** Na r2 fiquei em "manter, fraco". Reli os dois argumentos de Junco:

- "Quem lê" difere (ele × agentes no repositório). Mas o que 3 tem de agentes no repositório é o
  *código*, que fica fora do hub (briefing). Dentro do hub, quem lê as notas de 3 são os mesmos
  agentes que abrem a nota de retomada. A diferença de leitor some na pasta do hub.
- "Promover ou arquivar" de 4: promover é subir conteúdo para 5, o que é cópia sanitizada, não
  mudança da iniciativa. Arquivar é o estado, já resolvido acima.

O PARA, único método que fala disso, põe certificação e spike em Projects e produto em Projects ou
Areas (`01-para.json`): nenhuma diferença de método. Junco colocou a pergunta certa: *spike vira
produto na prática?* Se sim, a junção se confirma. Se não, não vejo coluna do briefing que sobre. Meu
voto: **juntar 3+4** (uma pasta de iniciativas sem cliente), estado em frontmatter.

## Onde discordo de Junco

Ele diz que juntei 9 com 2 "como PARA". Ele tem razão no teste: 2 tem dado de cliente, replicação
de 1; dado pessoal numa pasta declarada de cliente mistura os dois valores. Retiro "vai para 2".
A pergunta ao Gustavo passa a ter duas partes: o conteúdo pessoal *replica*? *Os agentes o leem?*
Se não replica, é raiz própria; se replica e agentes leem, cabe em 3+4 ou em 5, conforme o que for.

## Pendente

1. **SOC STRATA é cliente ou operação interna?** Não está nos JSON. Muda onde o 2 mora.
2. **Custo da busca (Junco):** raízes 1+2 somem da busca da outra máquina. Concordo que falta dono.
3. **Spike vira produto?** e **o pessoal replica?** são as duas perguntas ao Gustavo.

## Voto

1 manter · 2 manter separado · **3+4 juntar** · 5 manter com regra · 6 manter, perfil de máquina
fora · 7 manter, local · 8 cortar, propriedade `estado` · 9 aguarda o Gustavo.
