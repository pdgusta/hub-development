# Rodada 5: Astrolabio (posição final)

Mudo uma vez mais, para fechar: **3 e 4 juntam.** Na r4 voltei a separar; Junco e Cinzel
migraram para a fusão com um argumento melhor que o meu. O de Cinzel, de risco assimétrico, vem do
GLOSSARY: iniciativa é "a unidade que mora numa casa só", com "identificador estável". Se um spike
vira produto, a casa não muda. O de Junco: leitor e promoção não geram consequência de mecanismo, e
"raiz sem consequência é taxonomia", o erro do vault (briefing). Separar depois é mover pastas.

## Os nove, um por um

| # | Posição | O que sustenta |
|---|---|---|
| 1 Clientes | **manter** | PARA Projects, "short-term efforts... with a certain goal" (`01-para.json`); não compartilhável pelo FHS (`08-fhs.json`) |
| 2 Operações contínuas | **manter, separado de 1** | PARA Areas, "continues indefinitely" (`01-para.json`). O destino "compactar" é do hub, não do método |
| 3 Produtos + 4 Estudo | **juntar** (iniciativas sem cliente) | `01-para.json` não os separa: põe certificação em Projects e produto em Projects ou Areas. Sustento por ausência de método e pelo GLOSSARY |
| 5 Referência | **manter**, sem dado de cliente, só sobe sanitizado | Resources (`01-para.json`); References de Steph Ango, "coisas fora do meu mundo" (`07-vault-steph-ango.json`). A regra de sanitizar é do hub |
| 6 Oficina | **manter; perfil de máquina em subpasta não replicada** | `.claude` fixa caminho e separa escopo pessoal de projeto (`15-diretorio-claude.json`); XDG separa config de data (`09-xdg.json`) |
| 7 Entrada | **manter, local por máquina** | GTD sustenta a função capture→clarify, não a pasta (`05-gtd.json`, `nivel_raiz` vazio); XDG runtime aceita limpeza periódica (`09-xdg.json`) |
| 8 Arquivo | **cortar como raiz**: `_arquivo/` dentro de cada raiz | `01-para.json` é o único com `Archives`, e não trata replicação; FHS: o que difere em replicação não divide pasta (`08-fhs.json`) |
| 9 Pessoal | **condicional** à replicação | se não replica, é tipo (`08-fhs.json`); se replica e agentes leem, não tem comportamento próprio. `07-vault-steph-ango.json` dá a raiz ao pessoal, mas sem agentes |

Resultado: **seis raízes** (1, 2, 3+4, 5, 6, 7) e uma condicional (9). A nota de retomada mora dentro
da pasta de cada iniciativa, com nome fixo (precedentes: `10-cline-memory-bank.json`, PARA subpasta por
projeto em `01-para.json`).

## O que ficou em desacordo

**Nenhum de posição entre os três.** Resta uma divergência de mecanismo, que também já se aproximou:
arquivar por pasta `_arquivo/` (Cinzel, Junco, eu desde a r4) ou por propriedade `estado`. Junco
fica com a pasta **só se** mover pasta for seguro no sincronizador; cede à propriedade se não. Cinzel
cede se a busca só filtrar por propriedade. Eu cedi à pasta porque o único método da minha lente que
diz o que fazer com o que envelhece usa pasta (`01-para.json`), e porque a propriedade em `07`
categoriza, não arquiva (`07`, `nao_verificado`). Os dois fatos decisivos não estão em nenhum JSON.

Discordância factual menor entre Junco e Cinzel: se 1 e 2 existem nas duas máquinas, a Entrada
promove localmente ou cruza por SSH. É pergunta ao Gustavo.

## O que os métodos NÃO responderam

1. **Agentes.** Nenhum método de notas foi verificado para agente (`01`, `04`, `05`, `06`, `14`,
   `03`, `07`: nulo ou "não"); Johnny.Decimal só em parte (`02-johnny-decimal.json`).
2. **Quando envelhece.** Nulo em `02`, `04`, `06`, `08`, `10`, `11`, `13`, `14`. "Compactar" não vem de
   método algum.
3. **Replicação e pasta por máquina.** Só a analogia do FHS (`08`). Nenhum JSON trata de duas cópias
   editáveis.
4. **Controle de leitura por agente.** Nem JSON nem GLOSSARY têm mecanismo; é achado, não tipo.
5. **Como a pasta do hub vira o caminho do harness** (`15-diretorio-claude.json` só diz onde ele lê).
6. **Busca por caminho ou propriedade; mover pasta com duas máquinas.** Vão ao ticket 12.
7. **O que é o "pessoal".** Pergunta ao Gustavo.

## Perguntas ao Gustavo

SOC STRATA é cliente ou operação interna? Onde mora cada pasta de cliente, e captura de cliente cai
fora dela? O conteúdo pessoal replica?

**Convergimos** nas posições. Ficam dois testes técnicos para o ticket 12 e três perguntas ao
Gustavo.
