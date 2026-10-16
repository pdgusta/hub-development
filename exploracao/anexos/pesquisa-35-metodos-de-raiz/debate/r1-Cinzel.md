# r1 — Cinzel (lente: sistemas e agentes)

## O que os métodos de sistema dizem

- **FHS** separa por dois eixos independentes, compartilhável e variável, e manda pôr em diretórios
  diferentes o que difere em qualquer um (`08-fhs.json`). A raiz leva só o mínimo, e aplicações nunca
  criam arquivos ou subdiretórios nela (`08-fhs.json`). Limite: a tabela que mapeia cada diretório às
  células se perdeu, então só o critério vale (`08-fhs.json`, nao_verificado).
- **XDG** separa pela natureza: data, config, state, cache, runtime (`09-xdg.json`). Só runtime tem
  ciclo de vida definido; data, config, state e cache não têm regra de expiração (`09-xdg.json`).
  Tem regra de precedência: a versão do usuário sobrescreve a do sistema (`09-xdg.json`).
- **.claude** decide a pasta pelo escopo: projeto vai ao git e é compartilhado; `~/.claude` é pessoal,
  nunca commitado (`15-diretorio-claude.json`). Os caminhos são fixos, lidos pelo harness
  (`15-diretorio-claude.json`).
- **Memory tool, Letta, Basic Memory, Cline** não dão taxonomia de raiz. A memory tool tem só o
  prefixo `/memories`, que a aplicação mapeia ao armazenamento (`12-claude-memory-tool.json`). Letta e
  Basic Memory não nomeiam categorias de topo (`13-letta-memory.json`, `11-basic-memory.json`). Cline
  é uma pasta `memory-bank/` por projeto, com seis arquivos núcleo (`10-cline-memory-bank.json`).
  Respondem o que fica *dentro* de uma unidade, não o corte da raiz.

## Achado central

Das colunas da tabela dos nove tipos, só uma é critério de sistema: **dado de cliente = não
compartilhável/não replicado** (`08-fhs.json`; GLOSSARY, "Pasta não replicada"). "Termina?" não é
eixo de nenhum método de sistema (`08-fhs.json`, `09-xdg.json`); vem do PARA, onde projeto termina e
área não (`01-para.json`). E "cada pasta declara se é replicada" (GLOSSARY) significa que **uma pasta
da raiz não pode misturar os dois valores**. Esse é o teste que aplico.

## Os nove tipos

1. **Clientes — manter.** Não compartilhável, termina; cada cliente é uma unidade (`08-fhs.json`,
   `01-para.json`).
2. **Operações contínuas — juntar com 1, ou manter, sem apoio meu.** Tem a mesma propriedade de
   replicação de 1; só difere em não terminar, eixo que vem do PARA (`01-para.json`), não de sistema.
3. **Produtos e frentes — manter.** Sem dado de cliente, compartilhável, versionado. Escopo de
   projeto é o que o `.claude` põe no git (`15-diretorio-claude.json`).
4. **Estudo e laboratório — juntar com 3.** Nenhum método de sistema o distingue de 3: ambos
   compartilháveis, sem cliente. O que sobra é "termina" (`01-para.json`), e isso é estado da
   iniciativa, não corte de raiz. Aceito ser convencido do contrário por Astrolabio ou Junco.
5. **Conhecimento de referência — manter, mas limpar.** É o "estático" do FHS: não muda sem
   intervenção (`08-fhs.json`). A coluna "às vezes" dado de cliente quebra a declaração; referência com
   dado de cliente vai para o cliente.
6. **Oficina dos agentes — separar em dois.** Contrato, skills e papéis são compartilháveis e de
   caminho fixo (`15-diretorio-claude.json`). Perfil de máquina é específico da máquina: nem a raiz do
   FHS é compartilhável (`08-fhs.json`) e `~/.claude.json` guarda estado pessoal da máquina
   (`15-diretorio-claude.json`). Pertence ao não replicado.
7. **Entrada — manter.** É variável, o `/var` do FHS (`08-fhs.json`); o ciclo de vida só existe em
   runtime no XDG (`09-xdg.json`). Problema aberto: capturas com dado de cliente caem numa pasta
   replicada.
8. **Arquivo — cortar como raiz.** Só o PARA tem Archives de topo (`01-para.json`); Cline e `.claude`
   não dizem nada sobre envelhecer (`10-cline-memory-bank.json`, `15-diretorio-claude.json`). Um
   arquivo único mistura cliente (não replicado) e produto (replicado), e não consegue declarar um
   valor. Arquivar deve ser estado dentro de cada tipo.
9. **Pessoal? — sem posição.** `/home` é opcional no FHS (`08-fhs.json`) e a raiz do Steph Ango é o
   pessoal (`07-vault-steph-ango.json`), mas nada nos JSON diz se o conteúdo do Gustavo é replicado.
   Só vira tipo se a replicação for diferente de 3 e 5.

## Para os outros

- Astrolabio, Junco: o que sustenta 2 e 4 separados, se não for replicação?
- Cline manda ler todos os arquivos a cada tarefa (`10-cline-memory-bank.json`); isso não escala ao
  hub e contradiz a camada de busca. Só serve para a nota de retomada.
