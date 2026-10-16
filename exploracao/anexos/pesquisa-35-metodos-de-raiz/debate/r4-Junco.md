# r4 — Junco

## Fechado

8 deixa de ser raiz · 2 separado de 1 · 5 sem dado de cliente · 7 local por máquina · 6 com perfil de
máquina em subpasta não replicada (Cinzel e Astrolabio concordam) · nota de retomada dentro da pasta
da iniciativa, com nome fixo (Cinzel, r3) · 9 aguarda o Gustavo.

## Mudo: 3 e 4 juntam

Na r3 exigi que provassem que o leitor ou o caminho muda. Astrolabio provou o suficiente:

- **Leitor.** O que 3 tem de "agentes no repositório" é o código, fora do hub. Dentro do hub, o
  mesmo agente abre a nota de retomada de um produto e a de um spike. Não nomeio consequência de
  mecanismo (carga, replicação, busca) dessa diferença.
- **Promoção.** Promover é copiar conteúdo sanitizado para 5, o que vale também para um playbook
  nascido num produto. A iniciativa termina em arquivo nos dois. Meu argumento da r3 caiu.
- **Raiz sem consequência é taxonomia**, o erro do vault.

**Cinzel**, sua retirada se apoia em `15-diretorio-claude.json`: "escopo pelo leitor". O JSON diz
projeto compartilhado com a equipe × pessoal. É eixo de **compartilhar**, não de agente × humano;
3 e 4 têm o mesmo usuário e as mesmas máquinas. Peço que reconsidere. Nome sugerido: iniciativas sem
cliente. Reversível: separar depois é mover pastas.

## Continua: `_arquivo/` (Cinzel e eu) × propriedade `estado` (Astrolabio)

Corrijo-me: **o FHS não decide isto**. A propriedade também herda a replicação (a iniciativa não
sai da raiz), e o estático × variável (`08`) existe para sistemas de arquivos diferentes, como
Astrolabio disse. Empate.

O que sobra são dois argumentos de uso, e não se resolvem nos JSON:

- **Pró-propriedade (Astrolabio):** endereço estável. Resposta: o GLOSSARY dá à iniciativa
  "identificador estável" próprio, então o endereço no sentido de `04-zettelkasten.json` (o
  identificador) sobrevive à mudança de pasta. O Ango (`07`) evita pastas em tudo, o que o hub
  não decidiu; serve mal de precedente.
- **Pró-pasta (eu):** o Gustavo navega a vista Markdown por pastas; `estado` esquecido por agente que
  edita o disco faz arquivado aparecer ativo, sem ninguém notar. Pasta esquecida tem o mesmo defeito,
  mas fica visível na lista.

**Por que continua em aberto:** depende de dois fatos que nenhum JSON traz. (1) A camada de busca
filtra por caminho? Se sim, pasta sem campo; se não, propriedade. (2) Mover uma pasta com duas
máquinas editando é seguro no sincronizador? Mudar uma linha de frontmatter é mergeável por linha
(GLOSSARY, colisão real); mover não sei. Isso vai ao ticket 12 com esses dois testes. Minha
inclinação é pasta, **mas só se (2) passar**; se falhar, mudo para propriedade.

## Resposta a Cinzel sobre a Entrada (item 7b)

Cinzel diz que o checkpoint promove a 1 ou 2 "na mesma máquina, porque 1 e 2 também não replicam".
Só vale se a pasta do cliente existe nas duas máquinas, mas "não replicada" é máquina só (GLOSSARY):
captura de VOEGOL na máquina errada ainda cruza por SSH. Se dado de cliente só existe no notebook da
ARMIS, o problema some. Não está nos JSON; pergunta ao Gustavo.

## Perguntas ao Gustavo (quatro)

1. SOC STRATA é cliente ou operação interna? (2 × 1)
2. Em qual máquina mora cada pasta de cliente, e se captura cliente fora dela? (7)
3. O conteúdo pessoal replica? Cinzel está certo de que "agente não pode ler" o hub não declara; é
   achado, não tipo. (9)
4. Spike vira produto? Deixou de ser decisiva para 3+4; só confirma.

## Voto

1 manter · 2 manter, separado · **3+4 juntar** · 5 manter, sem cliente · 6 manter, `_maquina/` não
replicada · 7 manter, local · 8 cortar, destino por raiz (pasta ou propriedade: ticket 12) · 9 aguarda.
