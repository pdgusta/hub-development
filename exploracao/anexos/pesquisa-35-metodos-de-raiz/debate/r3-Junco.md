# r3 — Junco

## Fechado (os três concordam)

- **8 Arquivo:** deixa de ser raiz; arquivar é destino dentro de cada raiz (`08-fhs.json`; `01-para.json`
  não trata replicação).
- **2 separado de 1**, por destino (compactar × arquivar), não por "termina" (Cinzel, r2).
- **5 Referência** sem dado de cliente; só sobe sanitizado.
- **7 Entrada** local por máquina, esvaziada pelo checkpoint (`09-xdg.json`, runtime com limpeza).
- **6 Oficina** com o perfil de máquina fora da parte replicada. Cinzel me atribui o contrário na r2; isso era a r1, na r2
  já concedi. Concordo com Astrolabio: subpasta declarada não replicada basta, porque "cada pasta declara" (GLOSSARY). Se é
  `_maquina/` dentro de 6 ou fora, é do ticket 12.

## Desacordo 1: juntar 3 e 4 (Cinzel) ou não (Astrolabio, eu)

Cinzel pediu: provem que "promover ou arquivar" muda o caminho ou o leitor.

1. **Leitor.** O briefing dá 3 = "agentes no repositório", 4 = "ele". Não vem de método nenhum, vem da
   tabela do Gustavo, que é o critério declarado de tipo.
2. **Caminho.** Promover 4 → 5 muda de raiz; 3 não promove. Arquivar não muda (estado).
3. **Consistência.** Cinzel aceitou separar 2 de 1 porque o destino difere. Mesma régua: 4 tem destino
   próprio ("promover ou arquivar"), então 4 se separa de 3. Usar o destino para 2 e recusá-lo para 4
   não se sustenta.

Concedo o que Cinzel acertou: nenhum JSON separa 4 de 3 (`01-para.json` põe os dois em Projects ou
Resources). Se o Gustavo disser que spike vira produto sem promoção, junto sem resistir. Fica a
pergunta ao Gustavo, não um desacordo de método.

## Desacordo 2: `_arquivo/` ou propriedade `estado`? (pergunta de Cinzel)

Cinzel diz que "a busca só enxerga a propriedade". **Isso não está em nenhum JSON**; não vale como
argumento.

Meu critério é "cada informação tem um lugar só": pasta **e** campo seriam duas fontes do mesmo fato,
e divergem (arquivo movido sem o campo atualizado). Escolho um. Voto na **pasta `_arquivo/` dentro da
raiz**, sem campo `estado` espelhado:

- herda a replicação da raiz (FHS, `08`), sem declaração extra;
- o Gustavo vê o destino na vista Markdown sem abrir o frontmatter;
- o frontmatter "só leva o que a busca usa" (briefing): se a busca filtrar por prefixo de caminho,
  o campo é desnecessário. Se não filtrar, o campo vira obrigação de ticket 12, e aí cedo.

Isto é inferência; marco como tal.

## Item novo (Astrolabio perguntou se a Entrada local cria problema)

Cria um, e é de uso, não de método. VOEGOL mora na pasta não replicada da máquina X. Uma captura de
VOEGOL feita na máquina Y é esvaziada pelo checkpoint de Y **para uma pasta que só X tem**,
alcançada por SSH (GLOSSARY). Se X está desligada, a captura espera na Entrada de Y. "Em dias"
aguenta; semanas, não. Nenhum JSON trata disso: vai ao ticket 12, junto com o mecanismo de pasta
não replicada.

## Pergunta única ao Gustavo (junta as três abertas)

1. SOC STRATA é cliente ou operação interna? (decide 2 × 1)
2. Spike ou certificação vira produto na prática? (decide 4 × 3)
3. Há conteúdo pessoal que não pode replicar ou que agente não pode ler? Se não, 9 vai para 2;
   se sim, FHS (`08`) o sustenta como tipo.

## Posição atual

1 manter · 2 manter, separado · 3 manter · 4 manter, fraco, depende da pergunta 2 · 5 manter, sem
dado de cliente · 6 manter, `_maquina/` não replicada · 7 manter, local · 8 cortar, `_arquivo/` por
raiz · 9 aguarda a pergunta 3.

Resta o desacordo com Cinzel sobre 3+4 e sobre pasta × campo.
