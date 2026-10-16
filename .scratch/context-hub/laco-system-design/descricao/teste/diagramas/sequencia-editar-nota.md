# Diagrama: sequência, o Gustavo edita uma nota no Obsidian

Cenário: a edição nasce na máquina A e chega à máquina B e à busca de B. O caminho de falha é a colisão real (§8.1,
falhas: "o mesmo trecho mudou em B antes da troca"; §8.12). O desenho mostra os dois ramos de um `alt`.

**Faltou:**

1. **Versão do disco B enquanto a nota está em conflito.** A descrição diz que "só aquela nota fica retida" (§8.12,
   passo 2), mas não diz o que a vista Markdown de B mostra para ela: a versão local, a da outra máquina, ou nada.
   Deveria estar em §8.12 e na linha "Vista Markdown" de §3.1. No desenho, fica como "a decidir".
2. **O que a busca de B indexa para a nota em conflito.** §8.12 não menciona a busca. §8.9 e §3.1 ("Camada de busca")
   dizem que a busca enxerga o disco, mas não o que o disco mostra nesse caso. Também fica "a decidir".
3. **Origem da edição de B antes da troca.** §8.1 (falhas) diz só "mudou em B"; não diz se foi Obsidian, agente, disco
   ou outro par. Deveria estar em §8.1 (falhas). Desenhei como "origem não descrita".
4. **Ordem de chegada das duas versões.** §8.12 passo 1 diz "a troca traz as duas versões", sem ordem. §11 marca a
   ordem de chegada depois de um corte como [NV]. Deveria estar em §8.12 ou §8.8.
5. **Caminho da resolução até o disco e a busca de A.** §8.12 passo 7 diz que a resolução "numa máquina limpa o aviso
   na outra" e que a vigia "limpa o estado". Não diz que a resolução segue o caminho de uma edição normal (disco,
   sincronizador, busca). Esse caminho veio de §8.8 passo 3, que é outro cenário.

**Inventei:**

1. **Caminho da resolução (passos 6 a 8 do ramo de falha, e o retorno de B para A).** Supus que a resolução de B segue o
   caminho de §8.8 (banco, sincronizador, disco, busca). Motivo: o desenho precisava mostrar a busca de B depois da
   resolução, e §8.8 é o único caminho descrito para isso.
2. **Ordem das duas trocas no ramo de falha.** Desenhei primeiro o banco A enviando a edição (passo 4, comum aos dois
   ramos) e depois o banco B devolvendo a sua. Motivo: §8.12 passo 1 diz que a troca traz as duas, sem ordem.
3. **Omissões de componentes.** Não desenhei a **busca de A** (o desenho tem só a coluna da busca de B, que é o
   destino pedido pelo cenário), nem a **vigia** e o caminho com o **Obsidian fechado** (§8.12 passo 4). Motivo: o
   cenário pede Obsidian e busca em B; a vigia precisaria de uma coluna própria. Quem quiser esse ramo, precisa de uma
   coluna da vigia e da busca de A.
4. **Obsidian B aberto na colisão.** Desenhei a janela de conflito abrindo em B e em A (§8.12 passo 3). Supus que
   Obsidian A e B estão abertos. A descrição confirma que a janela abre nas duas máquinas quando o Obsidian está aberto.
5. **Gustavo no ramo de resolução.** Coloquei o Gustavo como o ator que escolhe a versão no Obsidian B. §8.12 passo 6
   diz "o Gustavo resolve, ou um agente com ele vendo"; escolhi o Gustavo porque é o caso mais simples. A tela de três
   vias não está no desenho, já que §11 a marca como decidida para logo após a construção.

**Ambíguo:**

1. **Quem leva a mudança de A ao banco: o plugin, o sincronizador, ou os dois.** §8.1 passo 3 diz "O plugin (Obsidian
   aberto) leva a mudança ao banco local; o sincronizador também cobre o caso". §3.1 (Obsidian) diz que o plugin leva
   edições "quando o Obsidian está aberto", e §3.1 (Sincronizador) diz que ele liga disco e banco "sem depender do
   Obsidian aberto". Desenhei o plugin, porque é o caminho do cenário, e deixei o sincronizador de fora desse passo.
2. **A unidade da colisão: o trecho ou a nota.** §8.1 (falhas) e §8.12 falam em "mesmo trecho" mudado dos dois lados.
   §8.12 passo 2 diz "só aquela nota fica retida", e §8.1 (falhas, última linha) fala em "mesma nota" para o agente.
   Não fica claro se a retenção é por trecho ou por nota inteira. O desenho segue a retenção por nota (§8.12 passo 2).
3. **Vista Markdown: gerada a partir do banco ou alimentada pelo disco.** §3.1 (Vista Markdown) diz que a vista é
   "gerada a partir do banco, e a edição volta ao banco". §8.1 passo 2 e §8.2 passo 2 mostram o caminho inverso: o
   Obsidian ou o agente grava no disco, e o sincronizador leva ao banco. Desenhei o segundo, porque o cenário começa
   no Obsidian gravando o `.md`.
