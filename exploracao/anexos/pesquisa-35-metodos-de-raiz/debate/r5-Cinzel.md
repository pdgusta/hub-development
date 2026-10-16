# r5 — Cinzel: posição final (lente: sistemas e agentes)

## Os nove

1. **Clientes: manter.** Difere em compartilhamento, logo diretório próprio (`08-fhs.json`); unidade é
   projeto com fim (`01-para.json`).
2. **Operações contínuas: manter, separado de 1.** Projects × Areas, "continues indefinitely"
   (`01-para.json`). O destino "compactar" é do hub, não do método. É a única evidência, de um método só.
3. **Produtos e frentes + 4. Estudo e laboratório: juntar** numa pasta de iniciativas sem cliente.
   Nenhum JSON os separa (`01-para.json`); iniciativa é "a unidade que mora numa casa só" (GLOSSARY),
   então spike que vira produto não pode mudar de casa. O destino de 4 contém o de 3 mais uma cópia
   sanitizada para 5. Junco concordou na r4; Astrolabio ficou em "separado, junta se spike vira
   produto".
5. **Referência: manter, sem dado de cliente.** Estático (`08-fhs.json`), `References` do Ango
   (`07-vault-steph-ango.json`). Só sobe sanitizado; precedência da versão específica sobre a
   compartilhada vem do XDG (`09-xdg.json`).
6. **Oficina: manter; perfil de máquina em subpasta não replicada.** Escopo projeto × pessoal e caminho
   fixo (`15-diretorio-claude.json`); `config` × `data` (`09-xdg.json`). O FHS pede diretório
   diferente, não raiz diferente (`08-fhs.json`).
7. **Entrada: manter, local por máquina, com limite de idade e aviso.** Runtime "MAY be subjected to
   periodic clean-up" (`09-xdg.json`); GTD sustenta a função capture→clarify, não a pasta
   (`05-gtd.json`).
8. **Arquivo: cortar como raiz.** Só o PARA tem `Archives` de topo, e não trata replicação
   (`01-para.json`). Vira `_arquivo/` dentro de cada raiz, herdando a declaração (`08-fhs.json`).
9. **Pessoal: condicional.** Se não replica, é raiz, pelo critério de compartilhamento (`08-fhs.json`).
   Se replica e agentes leem, não tem comportamento próprio e cai onde o conteúdo se comporta
   (Astrolabio). "Agente não pode ler" não é declarável: só replicação é (GLOSSARY).

## Correções minhas

- **Junco tem razão na Entrada.** Eu disse que o checkpoint promove a 1 ou 2 "na mesma máquina". Só
  vale se a pasta do cliente estiver na máquina onde a captura foi feita; "não replicada" é máquina
  só e a outra alcança por SSH (GLOSSARY). Retiro a frase. Depende de saber onde mora cada cliente.
- **Meu argumento do FHS para `_arquivo/` caiu** (estático × variável é para sistemas de arquivos
  diferentes: `08-fhs.json`). O que sobra são argumentos de uso, e assumo isso.

## O que ficou em desacordo

1. **3+4.** Eu e Junco juntamos; Astrolabio mantém separado, condicional. Ele escreveu antes de ler as
   r4. Não vejo coluna do briefing que sustente a separação dentro do hub; ele pode ter outra razão.
2. **`_arquivo/` × propriedade `estado`.** Astrolabio cedeu; Junco inclina para pasta "só se mover
   passar no sincronizador"; eu voto pasta. Dois fatos fora dos JSON decidem: a busca filtra por
   caminho? mover com duas máquinas editando é seguro? Vai ao ticket 12. Regra comum: uma fonte só,
   nunca pasta e campo espelhados; o MCP resolve a iniciativa pelo identificador, não pelo caminho.

## O que os métodos NÃO responderam

- **Isolamento e dado de cliente.** Compartilhamento é `null` ou não verificado em PARA, Johnny.Decimal,
  GTD e Diátaxis (`01-para.json`, `02-johnny-decimal.json`, `05-gtd.json`, `06-diataxis.json`). Só
  FHS e `.claude` têm eixo de compartilhar (`08-fhs.json`, `15-diretorio-claude.json`).
- **Envelhecer.** `nao_verificado` em `02`, `04`, `06`, `08`, `10`, `11`, `13`, `14`. Só PARA, XDG
  runtime e a memory tool dizem algo (`01-para.json`, `09-xdg.json`, `12-claude-memory-tool.json`).
- **Raiz para agentes.** Memory tool, Letta e Basic Memory não nomeiam categorias de topo
  (`12-claude-memory-tool.json`, `13-letta-memory.json`, `11-basic-memory.json`). Cline manda ler
  tudo a cada tarefa (`10-cline-memory-bank.json`), o oposto da camada de busca.
- **Como a pasta do hub vira o caminho do harness** (`15-diretorio-claude.json` fixa `.claude/` e
  `~/.claude/`).
- **Leitor por agente:** nenhum JSON traz controle por leitor.
- **Captura de cliente com a outra máquina desligada** e o limite de idade: inferência nossa.

## Perguntas ao Gustavo

SOC STRATA é cliente ou operação interna? Em qual máquina mora cada cliente? O pessoal replica?
Spike vira produto?

**Convergimos em tudo, exceto 3+4.**
