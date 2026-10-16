# r3 — Cinzel (lente: sistemas e agentes)

## Fechado, sem mais debate

- **8 Arquivo: cortar como raiz.** Três de três. Estado dentro de cada raiz.
- **2 separado de 1**, pelo destino (compactar × arquivar), com a evidência só do PARA
  (`01-para.json`). Junco e Astrolabio sustentam; eu já cedi na r2.
- **6 Oficina: o perfil de máquina sai da pasta de contrato e skills.** Junco corrigiu um
  deslize meu, e aceito: `15-diretorio-claude.json` diz "OAuth session, per-project trust
  decisions", estado pessoal. "Da máquina" vem do rótulo "perfil de máquina" do próprio briefing, não
  do JSON. O que o JSON sustenta é a separação: `~/.claude.json` guarda "state that does not belong in
  settings.json" (`15-diretorio-claude.json`).
- **5 Referência**, com a regra de Junco (cliente nunca mora em 5, só sobe sanitizado).
- **7 Entrada: local por máquina.** Respondo à pergunta de Astrolabio e Junco: não cria problema novo
  que eu veja, e fecha dois que estavam abertos. (a) Uma pasta só, declarada não replicada, com
  conteúdo diferente em cada máquina: o GLOSSARY pede um valor por pasta, não um conteúdo igual.
  (b) O que o checkpoint promove a 1 ou 2 continua na mesma máquina, porque 1 e 2 também não replicam;
  o que sobe a 3 ou 5 passa pela sanitização que já exigimos. Custo aceito: a outra máquina não vê a
  captura e, com a máquina desligada, ela fica parada (GLOSSARY, "Pasta não replicada"); para algo
  que esvazia em dias, serve. Apoio de sistema: o XDG separa *state* ("not important or portable
  enough" para data) de data (`09-xdg.json`), e runtime pode sofrer limpeza (`09-xdg.json`).

## Onde mudo de novo

**3 × 4: retiro a fusão como padrão.** Junco acertou o que eu errei: "quem lê" é coluna do briefing,
e eu o tratei como não-eixo de sistema. Não é: o `.claude` decide a pasta pelo escopo e pelo leitor,
projeto compartilhado com a equipe × pessoal (`15-diretorio-claude.json`). Em 3 leem agentes no
repositório; em 4 lê o Gustavo (briefing). Isso é critério com sustentação, ainda que de um método só.
A fusão volta só se o Gustavo disser que spike vira produto (pergunta do Junco). Fica como pergunta
a ele, não como posição minha.

## Respostas pendentes

**`_arquivo/` por raiz ou propriedade?** Minha própria pergunta da r2. Resposta: **pasta**. O FHS
separa estático de variável em diretórios diferentes (`08-fhs.json`), e o arquivado é estático. A
declaração de replicação não precisa da pasta (a raiz já a declara); a pasta serve para separar
ativo de arquivado. Se a busca exclui por caminho ou por propriedade não está em nenhum JSON; fica
para o ticket 12 (o briefing já limita frontmatter ao que a busca usa).

**Oficina: outra raiz ou subpasta?** Respondo a Astrolabio: **subpasta** declarada não replicada. O FHS
exige diretórios diferentes, não raízes diferentes (`08-fhs.json`), e a raiz mínima também é critério
dele (`08-fhs.json`: aplicações nunca criam itens na raiz). Menos raízes, mesma regra.

**Nota de retomada.** Concordo com Junco: dentro da pasta de cada iniciativa, com nome fixo. Precedentes:
`activeContext.md` em `memory-bank/` por projeto, "updates most frequently" (`10-cline-memory-bank.json`)
e `MEMORY.md` como índice fixo da memória automática (`15-diretorio-claude.json`). Nome fixo é o que
deixa achar sem busca. Consequência: a nota de um caso de cliente herda "não replicado", então a outra
máquina não a vê. É o custo que Junco nomeou, e é real.

## O que não se resolve nos JSON

1. **Como a pasta do hub vira o caminho que o harness lê** (`.claude/`, `~/.claude/`:
   `15-diretorio-claude.json`). Nenhum JSON diz. Vai ao ticket 12.
2. **9 Pessoal.** Astrolabio propôs uma pergunta só: "há conteúdo pessoal que não pode replicar ou que
   os agentes não podem ler?". A primeira metade é declarável (replicação). A segunda **não**: o
   GLOSSARY só tem a declaração de replicação, e nenhum JSON traz controle por leitor. Se a resposta
   for "agentes não podem ler", o hub não tem mecanismo, e isso é achado, não tipo.
3. **SOC STRATA é cliente ou operação interna?** Não está nos JSON; decide a fronteira de 1 e 2.

## Placar

1 manter · 2 manter separado · 3 manter · 4 manter, fraco, depende do spike · 5 manter com regra ·
6 manter, perfil de máquina em subpasta não replicada · 7 manter, local por máquina · 8 cortar,
`_arquivo/` por raiz · 9 aguarda o Gustavo.
