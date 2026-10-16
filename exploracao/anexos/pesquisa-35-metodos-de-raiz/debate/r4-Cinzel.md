# r4 — Cinzel (lente: sistemas e agentes)

## Fechado (os três)

8 deixa de ser raiz · 2 separado de 1, por destino · 5 sem dado de cliente, só sobe sanitizado · 7
local por máquina · 6 com o perfil de máquina em subpasta não replicada · nota de retomada dentro da
pasta de cada iniciativa, com nome fixo. Não volto a isso.

## Desacordo 1: 3 e 4

Junco diz que o desacordo comigo continua. Esclareço: na r3 eu já tinha retirado a fusão como
padrão. Agora volto a ela, **com argumento novo**, e Astrolabio chegou ao mesmo ponto.

O argumento é de risco assimétrico, e vem do GLOSSARY, não de método: iniciativa é "a unidade que
mora numa casa só", com "identificador estável". Se 3 e 4 forem raízes diferentes e um spike virar
produto, a iniciativa muda de casa, ou fica em 4 sendo produto. Com 3+4 juntos, nunca muda de casa; se o
spike nunca virar produto, nada se perdeu, porque o estado distingue os dois. Junco: sua régua do
destino vale (concedi em 2 × 1), mas aplicada com cuidado ela dá o inverso. O destino de 4,
"promover ou arquivar", contém o de 3 (arquivar) mais uma extração para 5, que é cópia sanitizada e
não muda a iniciativa (Astrolabio). O destino de 2 (compactar) não é subconjunto do de 1 (arquivar).
Por isso 2 × 1 separam e 4 × 3 não.

Resta a coluna "quem lê". Astrolabio observa que o que 3 tem de agentes no repositório é o código, que
fica fora do hub (briefing); dentro do hub os leitores coincidem. Concordo. Aceito mudar de voto se
o Gustavo disser que spike nunca vira produto *e* que o leitor muda dentro do hub. Fica pergunta,
não desacordo de método (nenhum JSON separa os dois: `01-para.json`).

## Desacordo 2: `_arquivo/` ou propriedade `estado`

Concedo três coisas.

1. **Junco tem razão:** minha frase da r2, "a busca só enxerga a propriedade", não está em nenhum
   JSON. Retiro.
2. **Astrolabio tem razão sobre o FHS.** O eixo estático/variável existe para guardar "on different
   filesystems" (`08-fhs.json`). O hub não tem segundo armazenamento; o único eixo por pasta é a
   replicação, e arquivado ou ativo herda a mesma. Meu argumento do FHS (r3) era fraco. Retiro.
3. **Junco tem razão no princípio:** uma fonte só. Pasta e campo espelhados divergem. Aceito a regra.

Mas a pasta ainda tem um argumento da minha lente, que Astrolabio não tratou. Agentes editam o disco
(briefing), e as primitivas da memory tool são operações por caminho: `view` de diretório, `rename`,
`delete` (`12-claude-memory-tool.json`). Quem lista um diretório vê o que está arquivado sem abrir
nenhum arquivo; com propriedade, tem de ler o frontmatter de cada um. A própria memory tool manda
renomear ou apagar o que "no longer relevant" (`12-claude-memory-tool.json`), ou seja, o destino do
velho é uma operação de caminho. O contra-argumento de Astrolabio, endereço fixo (`04-zettelkasten.json`),
não me convence: o endereço do Zettelkasten é o identificador único da nota
(`04-zettelkasten.json`), não o caminho de pasta; no hub o identificador estável é da iniciativa
(GLOSSARY) e não depende de caminho.

**Posição:** pasta `_arquivo/` por raiz, sem campo espelhado. Fica aberto, e agora honestamente: se
no ticket 12 a busca só filtrar por propriedade, cedo para `estado` único. O fato decisivo não está
em nenhum JSON, e os três concordamos que vai ao ticket 12. Uma tensão que assumo: se 3+4 usar
propriedade para estudo × produto, o hub terá frontmatter de qualquer jeito. Mas "tipo" é rótulo
estável, e "arquivado" é destino de ciclo de vida, que é o que agente lista.

## Item novo: a captura de VOEGOL esperando em Y

Junco acertou: é problema de uso, não de método. Concordo com a regra mínima: o checkpoint promove
só para destino alcançável localmente; o resto espera na Entrada da máquina de origem. Acrescento
uma exigência, tirada do padrão do GLOSSARY: "divergência nunca silenciosa" cobre máquina sem sync
acima do limite, mas **não cobre captura parada**. Pede-se um limite de idade na Entrada com aviso.
Isso é inferência minha, não consta nos JSON.

## Para a rodada 5

Perguntas ao Gustavo, as três de Junco: SOC STRATA é cliente ou operação interna? Spike vira produto?
O pessoal replica, e os agentes podem lê-lo? Sobre a última: só a replicação é declarável hoje
(GLOSSARY); "agente não pode ler" não tem mecanismo nem método nos JSON.

## Voto

1 manter · 2 manter separado · **3+4 juntar** · 5 manter com regra · 6 manter, perfil de máquina em
subpasta não replicada · 7 manter, local, com limite de idade · 8 cortar, `_arquivo/` por raiz
(cedo se a busca só filtrar por propriedade) · 9 aguarda o Gustavo.
