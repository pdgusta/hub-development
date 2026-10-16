---
title: Context hub — conceitos e decisões fechadas, com ponteiros
data: 2026-10-10
origem: subagente de pesquisa (Haiku 5.5), ticket 39
fontes: C:\Projetos\context-hub\GLOSSARY.md (inteiro); C:\Projetos\context-hub\.scratch\context-hub\map.md (inteiro); C:\Projetos\context-hub\exploracao\2026-09-28-context-hub.md (linhas 153–230 e 374–421); C:\Projetos\context-hub\.scratch\context-hub\issues\10-contrato-file-first.md (linhas 78–113); C:\Projetos\context-hub\.scratch\context-hub\issues\25-como-a-verdade-viaja-entre-as-maquinas.md (linhas 41–65); C:\Projetos\context-hub\.scratch\context-hub\issues\34-onde-o-servidor-mora.md (linhas 32–67)
aviso: saída de modelo; só o que está nos arquivos; o que está em aberto no mapa fica marcado como **em aberto**.
---

## 1. Objetivo e os cinco critérios de aceite

Fonte: `map.md`, seção "Destination", linhas 7–17.

> O context hub construído e funcionando nas duas máquinas (notebook da ARMIS e máquina pessoal), cumprindo os cinco critérios de aceite:

Critérios (`map.md`, linhas 10–17):

> 1. agentes (Claude Code, Codex, Copilot, dentro ou fora do Maestri), em qualquer máquina, acham o trecho certo sem ler tudo, pela camada de busca;
> 2. o que importa é gravado no lugar certo sem o Gustavo pedir, por um contrato file-first com zonas e checkpoint;
> 3. os `.md` continuam editáveis no Obsidian, a camada de busca está sempre acessível ao agente para buscar e gravar, e o agente também pode editar direto no disco, com sync para a outra máquina;
> 4. nada diverge em silêncio entre as máquinas;
> 5. existe proteção para a edição concorrente.

Nota: a exploração (§7.1, linhas 160–167) traz um objetivo com a marcação "Objetivo proposto (aguarda ajuste do Gustavo)". O texto acima é o do mapa.

## 2. Vocabulário

Fonte: `GLOSSARY.md`, linhas 8–91. Definições citadas como estão no glossário (quebras de linha retiradas).

**Context hub**

> A casa única do contexto, com uma cópia completa em cada máquina. A verdade mora num banco, que o agente lê e grava; o Gustavo vê o hub pela vista Markdown.

**Máquina**

> Cada um dos dois computadores do Gustavo (o notebook da ARMIS e a máquina pessoal). As duas são pares.

**Par**

> Um computador com uma cópia completa e editável do context hub, que trabalha sozinho e troca mudanças direto com outro par. Nenhum par é a referência dos outros. As duas máquinas são pares, e outros podem entrar.

**Cliente**

> Um computador ou sandbox que usa o context hub através de um par, sem cópia própria. Só funciona com um par ligado e, por padrão, só lê.

**Camada de busca**

> O que entrega ao agente o trecho certo do context hub sem que ele leia tudo. Pode também gravar.

**Edição concorrente**

> Duas gravações no mesmo arquivo em que nenhuma vê a outra. Acontece em máquinas diferentes entre um sync e outro, ou com dois agentes na mesma máquina.

**Iniciativa**

> Uma frente de trabalho com identificador estável, estado e próxima ação. É a unidade que mora numa casa só. Esta frente do context hub é uma iniciativa.

**Raiz**

> Uma das seis pastas do primeiro nível do context hub, cada uma com um comportamento próprio: `clients/` (iniciativas de cliente), `operations/` (trabalho contínuo, sem fim), `initiatives/` (iniciativas sem cliente: produtos, frentes, estudo), `reference/` (conhecimento de referência, promovido), `agents/` (a oficina dos agentes: contrato, skills, papéis) e `inbox/` (captura rápida). O que termina vai para o `_archive/` da própria raiz.

**Casa**

> O lugar único onde uma iniciativa é trabalhada. O destino é o context hub ser a casa de tudo; o vault `ai-operating-system` é só referência e será superado. Quando um conteúdo do vault é copiado para o hub, a casa dele passa a ser o hub, e o que ficou no vault não conta como segunda casa.

**Vista Markdown**

> Os arquivos `.md` pelos quais o Gustavo vê e edita o context hub (no Obsidian). Não é a verdade: é gerada a partir do banco, e o que ele edita nela volta para o banco.

**Ponto de encontro**

> O lugar por onde as mudanças do banco passam entre as máquinas. Não é uma máquina, e ninguém trabalha nele.

**Sincronizador**

> O processo de cada máquina que, por intervalo, grava no git tudo o que mudou no disco, busca o que veio do ponto de encontro, junta e envia. Também grava no disco, e conta como mais um escritor.

**Colisão real**

> As duas máquinas mudaram a mesma linha entre duas syncs, e o git não junta sozinho. Mudanças em linhas diferentes do mesmo arquivo não são colisão.

**Divergência**

> Uma colisão real, uma máquina sem sincronizar com sucesso há mais que o limite, ou uma cópia de conflito aberta. Nunca pode ser silenciosa: o aviso aparece na máquina que travou.

Ponteiro para o limite: `map.md`, "Decisions so far", ticket 08 (linhas 81–84), que fixa "máquina sem sync há mais de 30 min".

**Pasta não replicada**

> Parte do context hub que mora numa máquina só, fica fora do sync e do GitHub, e é alcançada pela outra máquina por SSH. A camada de busca da outra máquina não a indexa. Cada pasta declara se é replicada.

Ver o ponto em aberto na seção 5.

**Nota de retomada**

> O arquivo curto, um por trabalho, que permite a qualquer sessão nova (outro agente, modelo ou máquina) continuar de onde a anterior parou: objetivo, onde parou, próximo passo, decisões, o que não deu certo, perguntas abertas, arquivos em jogo. É sobrescrito, não acumulado. Um hook ao fim de cada resposta obriga o agente a mantê-lo em dia.

## 3. Zonas por ciclo de vida

Fonte: exploração, §9, linhas 213–220 (tabela de 2026-09-29).

> | Zona | Exemplos | Quem grava e quando | Indexada pela Guild | Sincronizada |
> |---|---|---|---|---|
> | Canônica | initiative.md, decisões, conhecimento, papéis, contrato | o agente dono, no checkpoint, direto no disco | sim | sim (git) |
> | Trabalho | case.md, queries, CSVs, prints, scripts, rascunhos | os agentes durante a tarefa | a decidir | a decidir (dado sensível) |
> | Efêmera | scratchpad, Temp, Maestri-drops, saídas de teste | qualquer um, a qualquer momento | nunca | nunca |
> | Derivada | índice da Guild, `~/.maestri`, memória privada do Claude | ferramentas | — | nunca (é reconstruível) |

Pontos ligados à tabela:

> **A única ponte da efêmera para as outras zonas é o checkpoint do contrato**, que promove o que importa. O que não foi promovido morre com a sessão, e isso é esperado. (§9, linhas 222–223)

> **Aviso (2026-09-29):** a descrição da Guild nesta seção veio da conversa com outro modelo e **não bate com o README**. Ver a seção 10. (§9, linhas 227–228)

A tabela usa "Guild", termo que o glossário lista como _Avoid_ no lugar de "camada de busca" (`GLOSSARY.md`, linha 30). Nos trechos lidos, o ticket 10 não reescreve a tabela de zonas.

## 4. Decisões fechadas que importam para um vídeo técnico

**4.1 Nota de retomada e hook `Stop` (ticket 10, decidido em 2026-10-04)**

> O hook ao fim de cada resposta (`Stop`) é o que obriga: quando a nota não reflete a resposta, ou a memória privada ganhou algo que o hub não tem, ele faz o agente continuar e gravar.

A nota tem sete campos, é sobrescrita e não acumulada. Os furos aceitos: "o hook não vê o que foi dito no meio de uma resposta longa e não roda quando o Gustavo interrompe." Ponteiros: `10-contrato-file-first.md`, Answer, itens 1–3 (linhas 86–103); `map.md`, "Decisions so far" (linhas 88–92). Não verificado: o equivalente ao `Stop` no Codex e no Copilot (linhas 105–107).

**4.2 Banco com vista Markdown: CouchDB + Self-hosted LiveSync (tickets 22 e 25)**

> **O que viaja entre as máquinas é o banco, por um servidor central: CouchDB + Self-hosted LiveSync, o caminho O1.** (ticket 25, linhas 43–44, decisão de 2026-10-06)

A vista `.md` fica viva nas duas direções pelo plugin LiveSync, e o agente grava pelo MCP do es617 num fork. Antes de usar, é obrigatório: "a R1 no fork (`read_note` devolve a revisão; a gravação leva `base_rev` e vira conflito se a base mudou) e o conflito visível ao agente." (ticket 25, linhas 51–53). O FNS ficou de fora porque "a gravação do agente com base velha apaga a outra versão sem rastro" (linhas 58–59). O ticket 22 tinha deixado a forma do banco em aberto: "a verdade mora num banco (forma em aberto)" (`map.md`, linhas 96–98). Ponteiros: `map.md`, "Decisions so far", tickets 22, 25, 29 e 30. Sobre a topologia "servidor central", ver a seção 5.

**4.3 Pares replicando pela tailnet e clientes só de leitura (ticket 34, decidido em 2026-10-10)**

> **S3: um CouchDB em cada par, com replicação mestre-mestre pela tailnet. Clientes alcançam um par pela tailnet, sem cópia própria.** (ticket 34, linhas 34–35)

Motivo dado: "o Gustavo não quer depender de uma máquina fixa como host e quer que qualquer computador ou sandbox monte o hub" (linhas 37–38). Para clientes, "cada par roda um segundo MCP com `READ_ONLY=true` e token, exposto na tailnet" (linhas 47–48), porque "o `READ_ONLY` não é garantia no banco (README do es617)" (linha 49). "Duas instâncias do es617 por par: inferência, não verificado." (linha 50). O primeiro teste da construção é "o LiveSync com dois CouchDB replicando entre si (NV)" (linhas 57–58). Ponteiros: `34-onde-o-servidor-mora.md`, Answer; `map.md`, "Decisions so far", ticket 34.

**4.4 As seis raízes (ticket 35 no mapa; glossário)**

> debate de três agentes propõe seis raízes (clientes, operações contínuas, iniciativas sem cliente, referência, oficina, entrada), `_arquivo/` dentro de cada uma e o pessoal condicional. (`map.md`, "Decisions so far", ticket 35)

O glossário define as seis raízes com outros nomes de pasta e fala em `_archive/`: `clients/`, `operations/`, `initiatives/`, `reference/`, `agents/`, `inbox/` (`GLOSSARY.md`, linhas 42–48). Há diferença no nome da pasta de arquivo, ver a seção 5.

**4.5 Windows com NTFS, sem WSL por ora (ticket 04)**

> NTFS em `C:\context-hub` nas duas máquinas; WSL fora até surgir caso de uso; o critério 1 troca o OpenCode pelo Copilot (VS Code e CLI). (`map.md`, "Decisions so far", ticket 04)

A exploração dizia, em 2026-09-30: "Ele quer achar o mais adequado às necessidades dele: **nenhuma decisão está fechada**." (§12, linhas 414–415). O mapa registra o ticket 04 como decidido. Como a prova de conceito chega ao hub real em `C:\context-hub` segue em aberto (`map.md`, "Not yet specified").

**4.6 GitHub privado como ponto de encontro do sync (ticket 06)**

> só o GitHub privado, com uma deploy key por máquina; sem assinatura; o Tailscale fica fora da construção inicial. (`map.md`, "Decisions so far", ticket 06)

O ticket 25 deixa para outro ticket "o que sobra do GitHub, do sincronizador e do mecanismo de divergência" (linhas 61–63). O ticket 06 também fica em revisão pelo ticket 22 ("Põe em revisão as decisões de sync, divergência e busca acima.", `map.md`, linhas 97–98).

## 5. O que ainda está em aberto

**Do mapa, "Not yet specified" (`map.md`, linhas 146–151):**

> - O perfil por máquina (§6.1 da exploração): o que é local de cada máquina e como se declara.
> - O Obsidian com o hub: o hub como cofre próprio, e como ele fica ao lado do cofre do vault enquanto os dois convivem.
> - Como esta prova de conceito vira o hub real em `C:\context-hub`.
> - Usos do FreeLLMAPI no funcionamento do hub além de embeddings (por exemplo, resumos); o checkpoint ficou sem ele.

**Do mapa, "Out of scope" (`map.md`, linhas 155–166), resumido pelas primeiras palavras de cada item:**

- "Aposentar o vault `ai-operating-system`: fica para depois deste mapa".
- "Migrar os workspaces existentes do Maestri; a skill de aplicar/auditar do Maestri; a convivência entre superpowers, GSD e Matt".
- "O `freellmapi-mcp` e a skill que ensina a usá-lo".
- "Edição concorrente entre o Obsidian e um agente no mesmo arquivo (Q4)." Vale notar que o critério 5 do mapa pede "proteção para a edição concorrente".
- "Tailscale e servidor SSH para a pasta não replicada e a operação remota: entram num ticket à parte quando surgir o primeiro caso".
- "Mecanismo de controle de acesso por pasta ... o Gustavo vai desenvolver depois, fora deste projeto".
- "Política de dados de cliente para a segunda máquina: o dado fica tão protegido lá quanto aqui (Q3)."

**Dos tickets, "Fica para outros tickets" (**em aberto**):**

- Ticket 25 (linhas 54–65): o que sobra do GitHub, do sincronizador e do mecanismo de divergência; se o agente ainda edita o `.md` direto no disco; a busca, que pode indexar a vista `.md`; a tela de colisão com três vias, "logo depois da construção" (linhas 54–57).
- Ticket 34 (linhas 61–67): o que conta como "máquina sem sync" e onde o aviso nasce sem ponto de encontro; o MCP que cada harness carrega; a pasta não replicada, "que pode ser replicação filtrada ou ficar fora do banco"; o kit de par e o kit de cliente.

**Inconsistências encontradas nos arquivos lidos (para conferir antes de usar no vídeo):**

1. **Nome da pasta de arquivo.** O glossário fala em `_archive/` (`GLOSSARY.md`, linha 47). O mapa, no ticket 35, fala em `_arquivo/` (`map.md`, "Decisions so far").
2. **Topologia do banco.** O ticket 25 diz "por um servidor central" (linha 43). O ticket 34, de 2026-10-10, substitui a ideia por "um CouchDB em cada par" (linha 34) e diz que a S1 "prende o hub a uma máquina" (linha 39). O mapa não registra essa troca.
3. **Tailscale.** O resumo do ticket 06 no mapa diz "o Tailscale fica fora da construção inicial". O ticket 34 usa a tailnet como transporte entre pares. O mapa não registra essa mudança.
4. **Pasta não replicada.** O glossário diz que ela "é alcançada pela outra máquina por SSH" (`GLOSSARY.md`, linhas 81–83). O ticket 34 deixa em aberto se ela é replicação filtrada ou fica fora do banco (linhas 65–66). O mapa a põe como fora de escopo.
5. **Definições do sync.** Sincronizador, colisão real e divergência no glossário descrevem o modelo de git (`GLOSSARY.md`, linhas 67–84). O mapa e o ticket 22 põem em revisão as decisões de sync, divergência e busca, e o ticket 25 deixa o sincronizador em aberto.
6. **Hook do Stop.** Nos trechos lidos, o hook é tratado como decisão, mas o equivalente no Codex e no Copilot está "não verificado" (ticket 10, linhas 105–107).
7. **Fora desta lista de fontes.** O AGENTS.md da raiz do repositório diz "(`C:\context-hub` ou WSL, ainda em aberto)", o que conflita com a decisão do ticket 04 no mapa. Não li esse arquivo para esta pesquisa; a informação vem do contexto que o agente que me chamou já tinha.
