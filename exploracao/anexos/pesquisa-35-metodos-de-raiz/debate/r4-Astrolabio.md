# Rodada 4: Astrolabio

## Onde cedo

**`_arquivo/` por raiz, não propriedade. Cedo a Junco e Cinzel.** Na r3 sustentei `estado` com duas
fontes: o endereço fixo do Zettelkasten (`04-zettelkasten.json`) e as propriedades de Steph Ango
(`07-vault-steph-ango.json`). Relendo:

- `07` usa propriedade para *categorizar*, não para envelhecer. A fonte "não define critério de
  término ou arquivamento" (`07`, `nao_verificado`). Eu estava usando um método fora do que ele diz.
- O único método da minha lente que diz o que fazer com o que envelhece é o PARA, e ele usa pasta:
  `Archives` na raiz, com a subpasta de cada item (`01-para.json`). Aplicado dentro de cada raiz, é
  o `_arquivo/` de Junco.
- Meu argumento do endereço cai pelo GLOSSARY: a iniciativa tem "identificador estável"
  (GLOSSARY.md). O endereço que `04` pede é o id, não o caminho.
- Junco acerta que pasta e campo seriam duas fontes do mesmo fato. Minha proposta de campo sozinho
  não tinha esse problema, mas perde na vista Markdown: o Gustavo precisaria abrir o frontmatter
  ou montar uma visão (`07`), e nada nos JSON diz que ele usa Bases.

Resto de dependência que registro: se a busca excluir por prefixo de caminho, o campo é desnecessário
(Junco). Se não excluir, vira obrigação do ticket 12. Cinzel tem razão que isso não está nos JSON.
**Fechado em 3 de 3: `_arquivo/` dentro de cada raiz.** Fica uma obrigação ao ticket 12: o MCP
resolve a iniciativa pelo id, porque o caminho muda ao arquivar.

**3 × 4: volto a manter 4 separado, condicional.** Mudei duas vezes, então explico o critério para
não parecer vento. Nenhum JSON separa 3 de 4 nem os junta (`01-para.json` põe os dois em Projects ou
Resources; Junco e Cinzel concordam). Quando o método cala, a decisão cai nas colunas da tabela, que
o briefing declara critério de tipo. Nelas 4 difere de 3 em leitor e em destino (promover ou
arquivar). Junco apontou a inconsistência de aceitar o destino para separar 2 de 1 e recusá-lo aqui.
Retiro o argumento de que "o leitor some na pasta": é leitura minha, não está em JSON. Posição:
**separado por padrão; junta se o Gustavo disser que spike vira produto sem promover.** Cinzel
já está aí. Junco também. Fecha em 3 de 3.

## Onde mantenho

**9 Pessoal: separo em duas perguntas, e uma delas não é pergunta de raiz.** Junco escreveu "se não,
9 vai para 2". Retirei isso na r3 pelo mesmo teste dele: 2 tem dado de cliente. Cinzel vai além, e
concordo: replicar é declarável (GLOSSARY, "Pasta não replicada"); "agente não pode ler" não tem
mecanismo em nenhum JSON nem no GLOSSARY. Regra que proponho para o ticket:

- Pessoal que **não replica**: é tipo, sustentado pelo FHS (`08-fhs.json`: diferem em
  compartilhamento, diretórios diferentes). Raiz própria.
- Pessoal que **replica e agentes leem**: não tem comportamento próprio, não é tipo. Cai onde o
  conteúdo se comporta (3+4 ou 5). `07` dá raiz ao pessoal, mas em vault de uma pessoa sem agente;
  não transfere.
- Pessoal que **agente não pode ler**: o hub não tem mecanismo. É achado, não raiz.

## Sobre o item novo de Junco (captura de VOEGOL na máquina Y)

Não resolvo, mas acrescento um fato: no GTD, só o Clarify dá destino ao item (`05-gtd.json`). A captura
chega sem tipo. A saída segura é marcar cliente *na captura* (o agente sabe qual caso está aberto)
em vez de esperar o esvaziamento. É inferência minha. Marca a captura como "de cliente X" e a
Entrada de Y a guarda local até X estar ligada. Vai para o ticket 12 com o mecanismo de pasta.

## Estado para a rodada 5

1 manter · 2 manter, separado de 1 (destino) · 3 manter · 4 manter, separado, junta se spike vira
produto · 5 manter, sem dado de cliente · 6 manter, perfil de máquina em subpasta não replicada ·
7 manter, local por máquina · 8 cortar, `_arquivo/` por raiz · 9 condicional à replicação (regra
acima).

**Desacordo que resta:** nenhum entre nós três sobre posição. Ficam três perguntas ao Gustavo
(SOC STRATA cliente ou interno; spike vira produto; pessoal replica) e três itens do ticket 12
(caminho fixo do harness, busca por prefixo ou campo, captura de cliente com a outra máquina off).
