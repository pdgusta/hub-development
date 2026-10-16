# Texto do hub

Texto padrão do context hub, para qualquer diagrama nascer só dele. Escrito pelo Tech lead; rodada 2, 2026-10-15
(depois da conferência do maestro, rodada 1).

**Como ler.** Só conta como decidido o que está num ticket resolvido ou nas "Decisions so far" do mapa. A fonte
vem entre parênteses, pelo título do ticket. O resto está marcado **não decidido** ou **não verificado** e reunido
na seção 7. Nomes em **negrito** são termos do `GLOSSARY.md`; componentes sem termo no glossário estão marcados
"(sem termo)". A coluna "rótulo" dá o nome curto que todo diagrama usa.

Aviso de vocabulário: no glossário, **Peça** é uma unidade do acervo do maestro. Por isso este texto chama as partes
do hub de **componentes**. Um diagrama não deve rotular os componentes como "peças".

---

## 1. O que o hub é

O **context hub** é a casa única do contexto que o Gustavo e os agentes leem e gravam. Cada **máquina** tem uma cópia
completa: a verdade mora num banco, o agente lê e grava no banco, e o Gustavo vê e edita o hub pela **vista
Markdown** (glossário; "Markdown: vista ou fonte da verdade").

Duas coisas diferentes, que não se confundem:
- a sessão **abre** numa **porta de entrada** (a principal é a sessão na raiz do hub) ("Portas de entrada do hub");
- o agente **chega ao conteúdo** pela **camada de busca**, não andando pela árvore de pastas. Índice mantido à mão
  só existe onde a busca não basta ("Lições do vault").

**Destino do mapa:** o hub construído e funcionando nas duas máquinas (o notebook da ARMIS e a máquina pessoal),
cumprindo cinco critérios (mapa, Destination):

1. agentes (Claude Code, Codex, Copilot, dentro ou fora do Maestri), em qualquer máquina, acham o trecho certo pela
   camada de busca, sem ler tudo;
2. o que importa é gravado no lugar certo sem o Gustavo pedir (contrato file-first);
3. os `.md` continuam editáveis no Obsidian; a busca está sempre acessível para buscar e gravar; o agente pode
   editar direto no disco, com sync para a outra máquina;
4. nada diverge em silêncio entre as máquinas;
5. existe proteção para a **edição concorrente**.

---

## 2. Princípios do desenho

Regras de forma que valem para todo componente ("Lições do vault"). Um diagrama deve deixá-las visíveis, não só os
componentes.

- **Falha se corrige com mecanismo**, ou tirando regra; nunca acrescentando regra nova.
- **Cada informação tem um lugar só**, escrito no contrato.
- **O checkpoint grava sem pedido:** o que importa chega ao lugar certo por mecanismo do hub, não porque o Gustavo
  pediu nem porque o agente lembrou.
- **A porta de entrada ao conteúdo é a camada de busca** (seção 1).
- **Aval só para o contrato, os adaptadores e as exclusões ou reescritas grandes.**
- **Complexidade conquistada:** uma camada só entra se resolve um dos cinco critérios.

---

## 3. Os componentes

### 3.1 Em cada par (as duas máquinas hoje)

As duas máquinas são **pares**: cada uma tem cópia completa e editável, trabalha sozinha e troca mudanças direto com
a outra. Nenhuma é referência. Outros pares podem entrar (glossário; "Onde o servidor mora"). Sistema: Windows,
disco NTFS, hub em `C:\context-hub`; WSL fora ("Windows ou WSL").

| Componente | Rótulo | Papel, numa frase | Fonte |
|---|---|---|---|
| Banco local (sem termo; é o CouchDB) | Banco local | Guarda a verdade: cada nota com histórico de versões e as versões em conflito; o texto fica cifrado. | "Como a verdade viaja entre as máquinas"; "Onde o servidor mora"; "Pesquisa ampla: lugares e mecanismos de busca" |
| **Vista Markdown** | Vista Markdown | Os arquivos no disco por onde o Gustavo vê e edita o hub; gerada a partir do banco, e a edição volta ao banco. | glossário; "Markdown: vista ou fonte da verdade" |
| **Sincronizador** | Sincronizador | Liga disco e banco local o tempo todo, nos dois sentidos, sem depender do Obsidian aberto; pega o que qualquer agente grava no disco. Conta como mais um escritor do disco. | "Revisão do sync e da divergência com o banco" |
| Obsidian com o plugin de sync (sem termo) | Obsidian | Só para ver, editar e resolver conflito; pode ficar fechado. O cofre é a raiz do hub. | "Revisão do sync…"; "Portas de entrada do hub" |
| MCP do banco (sem termo) | Porta do banco | Porta do agente ao banco: lê devolvendo a versão, grava levando a versão lida, e vira conflito visível se ela mudou. É uma versão modificada de um MCP pronto. | "Como a verdade viaja…"; "Revisão do sync…" |
| MCP só de leitura (sem termo) | Porta de leitura | Segunda porta do par, exposta na rede só para os clientes, com token. | "Onde o servidor mora" |
| **Camada de busca** | Camada de busca | Entrega ao agente o trecho certo sem ele ler tudo; é por ela que o agente chega ao conteúdo. Onde mora: **não decidido** (seção 7). | glossário; "Lições do vault"; mapa, Destination |
| Vigia (sem termo) | Vigia do sync | Confere a cada 5 min o estado das trocas, conflitos abertos, binários descartados, arquivos grandes demais e se o sincronizador está vivo; grava um estado curto e avisa quando piora. | "Revisão do sync…" |
| Avisos (sem termo) | Avisos | Três saídas da vigia: notificação do Windows, o estado curto lido no início de sessão, e um mod do Claude Code que mostra o estado o tempo todo. | "Revisão do sync…" |
| Checagem de início de sessão (sem termo) | Checagem de sessão | No começo de toda sessão de agente: lê o estado da vigia, informa a hora da última troca e abre a nota de retomada do trabalho. | "Divergência e edição concorrente"; "Contrato file-first: zonas e checkpoint" |
| Hook de fim de resposta (sem termo) | Checkpoint | Obriga o agente a manter a nota de retomada em dia e a levar ao hub o que só a memória privada da ferramenta sabe. Hoje garantido só no Claude Code. | "Contrato file-first…" |
| Contrato (`AGENTS.md` na raiz; sem termo) | Contrato | As regras do hub para os agentes, incluindo o lugar de cada informação. O hub não tem `CLAUDE.md` em lugar nenhum. | "Portas de entrada do hub"; "Lições do vault" |
| Guarda do acervo (sem termo) | Guarda do acervo | Fiscaliza gravações no acervo do maestro. No Claude Code é forte: um mod ou hook no escopo do usuário recusa ou pede aval, vê toda skill carregada e exige um verificador noutro modelo antes de alterar. Codex e Copilot não gravam no acervo: deixam propostas. | "Maestri: padrão e liberdade"; "Guarda do acervo: mods e hooks, pesquisa" |
| Registro de uso (sem termo) | Registro de uso | Anota, por máquina, quem usa cada peça do acervo, gravado por hook; o Maestri sozinho não registra isso. | "Maestri: padrão e liberdade"; "Guarda do acervo…" |
| Cópia de segurança local (sem termo) | Cópia local (git) | Um `.git` na raiz de cada máquina, que não replica; só faz commit e push, nunca escreve no disco do hub. | "Revisão do sync…" |
| Nó da rede privada (sem termo; Tailscale) | Nó da rede | Põe o par na rede privada entre as máquinas. | "Revisão do sync…"; "Ponto de encontro do sync" (revisado) |

### 3.2 O conteúdo do hub (o que mora dentro)

| Componente | Rótulo | Papel | Fonte |
|---|---|---|---|
| **Raiz** (seis) | Raiz | Primeiro nível, cada uma com comportamento próprio: `clients/` (iniciativas de cliente), `operations/` (trabalho contínuo), `initiatives/` (iniciativas sem cliente), `reference/` (referência), `agents/` (a oficina dos agentes: contrato, skills, papéis), `inbox/` (captura rápida). O que termina vai ao `_archive/` da própria raiz. | glossário; "Métodos conhecidos de organizar a raiz" |
| **Iniciativa** | Iniciativa | Frente de trabalho com identificador, estado e próxima ação; mora numa **casa** só. | glossário; "Workloads piloto" |
| **Nota de retomada** | Nota de retomada | Um arquivo curto por trabalho, sobrescrito, com sete campos; permite a qualquer sessão continuar de onde a outra parou. | glossário; "Contrato file-first…" |
| **Acervo do maestro** | Acervo do maestro | Peças prontas (papéis, setups, contratos-opção e outras) para todo maestro do Maestri, como família de skills em `agents/skills/`. Opções, não regras. Propostas do Codex e do Copilot e o registro de uso moram em `agents/maestro/`. | glossário; "Maestri: padrão e liberdade" |
| **Pasta não replicada** | Pasta não replicada | Parte do hub numa máquina só, fora do sync e da cópia de segurança. Mecanismo **não decidido** (seção 7). | glossário; "Onde o servidor mora" |

**O que vai ao banco:** todo arquivo comum até 200 MiB. Só `.md`, `.txt` e `.csv` são texto, com junção automática; o
resto é binário. Pastas com ponto, em qualquer nível, ficam fora. Repositório de código mora fora do hub ("Revisão do
sync…").

**Conteúdo inicial** ("Workloads piloto"):
- nascem no hub esta frente e tudo o que o Gustavo disser que nasce nele;
- o que vem do vault `ai-operating-system` é **copiado** e daí em diante trabalhado só no hub; o que fica no vault é
  referência, não segunda casa. Já desejados: `armis-docs`, `armis-brand` e a skill `armis-docx`;
- a operação de SOC da iniciativa STRATA fica fora por ora.

### 3.3 Fora das máquinas

| Componente | Rótulo | Papel | Onde | Fonte |
|---|---|---|---|---|
| Rede privada (sem termo; tailnet) | Rede privada | O único caminho entre pares e entre cliente e par. | serviço Tailscale | "Onde o servidor mora"; "Revisão do sync…" |
| Repositório privado no GitHub (sem termo) | Cópia no GitHub | Cópia de segurança diária da vista, um ramo por máquina. Não é ponto de encontro do sync. | GitHub | "Revisão do sync…"; "Ponto de encontro do sync" |
| **Cliente** | Cliente | Computador ou sandbox que usa o hub através de um par, sem cópia; só lê por padrão; precisa de um par ligado. | qualquer | glossário; "Onde o servidor mora" |
| Vault `ai-operating-system` (sem termo) | Vault (referência) | Só referência: o agente pode ler, o hub não grava nada nele. Só existe no notebook. | notebook | "Workloads piloto" |

### 3.4 Quem chega ao hub

| Quem | Rótulo | Como | Fonte |
|---|---|---|---|
| Agentes de código | Agentes | Claude Code, Codex e Copilot (do VS Code e de linha de comando), dentro ou fora do Maestri. | mapa, Destination; "Windows ou WSL" |
| Claude Desktop | Claude Desktop | Lê pelo MCP, por uma ponte local. Se grava: **não decidido**. | "Portas de entrada do hub" (revisão de 2026-10-12) |
| O Gustavo | Gustavo | Pelo Obsidian, na vista Markdown. | "Markdown: vista ou fonte…" |
| Maestro do Maestri | Maestro | Começa pelo acervo do maestro. | "Maestri: padrão e liberdade" |

**Portas de entrada** decididas ("Portas de entrada do hub"): sessão na raiz (a principal); sessão numa subpasta;
Maestri (workspace de iniciativa abre na pasta dela, "Maestri: padrão e liberdade"); Obsidian; Claude Desktop;
cliente pelo MCP de um par; sessão num repositório fora do hub. Lembrete: a porta diz onde a sessão abre; o conteúdo
se alcança pela busca (seção 1).

### 3.5 Agrupamentos naturais

O que as fontes sustentam sobre o que fica junto. Não é a metáfora; é a matéria-prima dela.

1. **Núcleo de dados do par:** banco local, vista Markdown, sincronizador. Os três guardam ou movem a mesma verdade
   dentro da máquina ("Revisão do sync…").
2. **Portas do par:** porta do banco, porta de leitura, camada de busca. Por elas os agentes e os clientes alcançam o
   núcleo ("Como a verdade viaja…"; "Onde o servidor mora"; "Lições do vault"). Onde a busca mora ainda é aberto.
3. **Vigilância:** vigia do sync, avisos, checagem de sessão. Ligadas à garantia "nada diverge em silêncio"
   ("Revisão do sync…"; "Divergência…").
4. **Disciplina do agente:** contrato, checkpoint, nota de retomada, guarda do acervo, registro de uso. Fazem o agente
   gravar no lugar certo e sem pedido ("Contrato file-first…"; "Maestri: padrão e liberdade").
5. **Conteúdo:** as seis raízes, com iniciativas, notas de retomada, acervo do maestro e a pasta não replicada dentro
   delas (glossário).
6. **Periferia do par:** Obsidian (opcional, pode ficar fechado), cópia local (git), nó da rede. Estão no par, mas
   não guardam nem movem a verdade do dia a dia.
7. **Fora do par:** rede privada, cópia no GitHub, clientes, Claude Desktop pela ponte, vault como referência. O
   outro par fica do outro lado da rede privada, igual a este.

Gente e agentes (Gustavo, agentes, maestro) ficam do lado de fora de todos os grupos, chegando pelas portas.

---

## 4. As ligações

| De | Para | O que passa | Quando | Fonte |
|---|---|---|---|---|
| Vista Markdown | Sincronizador ↔ banco local | Mudanças de arquivo, nos dois sentidos | Sempre (tarefa agendada no logon, repetindo a cada poucos minutos, uma instância só) | "Revisão do sync…" |
| Obsidian | Banco local | Edições do Gustavo; conflitos para resolver | Só com o Obsidian aberto | "Revisão do sync…" |
| Banco local do par A | Banco local do par B | As mudanças do próprio par; cada par envia as suas | Contínuo, com os dois ligados, pela rede privada | "Revisão do sync…" |
| Agente | Porta do banco → banco local | Leitura com versão; gravação com a versão lida | A cada leitura e gravação | "Como a verdade viaja…" |
| Agente | Camada de busca | Pergunta → trecho certo | A cada busca; é o caminho normal até o conteúdo. Onde a busca mora: **não decidido** | "Lições do vault"; mapa, Destination; "Pesquisa ampla…" |
| Cliente | Porta de leitura de um par | Consultas, por HTTP com token | Quando o cliente pede; nunca recebe a credencial do banco | "Onde o servidor mora" |
| Claude Desktop | Porta do banco, por ponte local | Leitura | Quando pede | "Portas de entrada do hub" |
| Agente | Guarda do acervo → acervo do maestro | Gravação no acervo: liberada, recusada ou com pedido de aval, depois do verificador noutro modelo (Claude Code); proposta em vez de gravação (Codex, Copilot) | A cada tentativa de alterar uma peça | "Maestri: padrão e liberdade"; "Guarda do acervo…" |
| Hook de uso | Registro de uso | Quem usou qual peça, por máquina | Quando uma peça é usada | "Maestri: padrão e liberdade" |
| Vigia do sync | Banco local, sincronizador, Obsidian | Lê estado das trocas, conflitos, binários descartados, arquivos grandes, processo vivo | A cada 5 min | "Revisão do sync…" |
| Vigia do sync | Avisos (notificação, estado curto, mod) | Aviso de divergência | Quando o estado piora (notificação); sempre visível (mod) | "Revisão do sync…" |
| Estado curto e nota de retomada | Checagem de sessão | Situação do sync e onde o trabalho parou | No início de toda sessão | "Divergência…"; "Contrato file-first…" |
| Checkpoint | Nota de retomada (e o hub) | O que a resposta mudou; o que só a memória privada sabe | Ao fim de cada resposta | "Contrato file-first…" |
| Cópia local (git) | Cópia no GitHub | Commit e push da vista | Uma vez por dia | "Revisão do sync…" |
| Contrato e skills do hub | Configuração global de cada ferramenta | Link para o `AGENTS.md`; skills por ligação de pasta | Fixo, montado pelo kit de par | "Portas de entrada do hub"; "Testes da porta do repositório fora do hub" |

---

## 5. Os fluxos

### 5.1 Gravar

1. **Agente pela porta do banco:** lê a nota e recebe a versão; grava levando essa versão; se a nota mudou no meio, a
   gravação vira conflito visível e o agente relê e refaz ("Como a verdade viaja…"; "Divergência…").
2. O banco local guarda; o sincronizador escreve no disco; a vista atualiza ("Revisão do sync…").
3. **Gustavo no Obsidian:** edita o `.md`; a edição volta ao banco pelo plugin ou pelo sincronizador ("Markdown: vista
   ou fonte…"; "Revisão do sync…").
4. **Agente direto no disco:** o sincronizador leva a mudança ao banco ("Revisão do sync…"). Como o agente confere a
   versão ao gravar no disco: **não decidido** ("Como os agentes gravam no hub", aberto).
5. **Agente no acervo do maestro:** passa pela guarda do acervo antes de gravar (seção 4).
6. O banco local envia a mudança ao outro par (5.3).

### 5.2 Buscar

1. O agente chega ao conteúdo pela camada de busca, não andando pela árvore: pergunta e recebe o trecho, não o
   arquivo inteiro ("Lições do vault"; mapa, Destination, critério 1).
2. Abre só o trecho de que precisa; se for alterar, grava (5.1).
3. Fato que pesa no desenho: o banco guarda o texto cifrado, então a busca não pode ser feita pelo próprio banco
   ("Pesquisa ampla…").
4. Onde a busca mora (no disco de cada máquina, com alcance pela rede, ou num índice dentro da porta do banco), qual
   ferramenta e qual modelo: **não decidido** (seção 7).

### 5.3 Sincronizar

1. Uma mudança chega ao banco local (pela porta do banco, pelo Obsidian ou pelo sincronizador).
2. O par que mudou envia ao outro, pela rede privada ("Revisão do sync…").
3. O banco do outro par recebe; o sincronizador de lá escreve no disco; a vista dele atualiza.
4. Mudanças em trechos diferentes da mesma nota se juntam sozinhas ("Revisão do sync…").
5. À parte, uma vez por dia, cada máquina faz a cópia de segurança no GitHub ("Revisão do sync…").

### 5.4 Divergência

Divergência é só isto (glossário; "Revisão do sync…"):
- **colisão real** que o Gustavo ainda não viu resolvida;
- a máquina não leva as próprias mudanças à outra há mais de 15 min, com a outra ligada na rede;
- um arquivo acima de 200 MiB, que não viaja.

A outra máquina desligada não é divergência: a checagem de sessão só informa a hora da última troca.

Passos:
1. **Colisão de texto:** só aquela nota fica retida; o resto continua viajando; abre-se a janela de conflito; o
   conflito aberto conta até ser resolvido.
2. **Colisão de binário:** o hub fica sozinho com a versão mais nova; a vigia acha a versão descartada, avisa, e um
   comando recupera a versão perdida para um arquivo ao lado.
3. **Aviso:** nasce na máquina que travou: notificação do Windows, estado lido no início de sessão, mod do Claude
   Code. Conflito com o Obsidian fechado aparece pela vigia.
4. O Gustavo (ou um agente com ele vendo) resolve; a vigia limpa o estado.

### 5.5 Agentes acessando o hub

1. A sessão **abre** numa porta de entrada; a principal é a raiz ("Portas de entrada do hub").
2. O contrato chega pelo `AGENTS.md` da raiz, ou pela configuração global de cada ferramenta (fora do hub e dentro de
   um papel do Maestri) ("Acesso dos agentes: pesquisa"; "Portas de entrada do hub"). Um cliente recebe o começo do
   contrato pela própria porta de leitura e pela descrição das ferramentas de gravação.
3. A checagem de início de sessão mostra o estado do sync e abre a nota de retomada; se a pasta não indica o trabalho,
   o agente acha a nota pela busca, pelo nome que o Gustavo der, ou pergunta ("Contrato file-first…").
4. O agente **chega ao conteúdo** pela camada de busca (5.2), lê e grava (5.1).
5. Ao fim de cada resposta, o checkpoint confere a nota de retomada e a memória privada ("Contrato file-first…").
6. Dentro do Maestri, o maestro começa pelo acervo do maestro; alterar uma peça passa pela guarda do acervo; usar uma
   peça fica no registro de uso ("Maestri: padrão e liberdade").

Ressalva medida em teste: o contrato chegar não garante que o agente obedeça ("Portas de entrada do hub").

---

## 6. As fronteiras

**O par.** Cópia completa (núcleo de dados, portas, vigilância, disciplina do agente, conteúdo). Trabalha sozinho.
Guarda a frase-senha da cifra e segue a mesma regra de dado de cliente que a outra máquina. Um par novo entra pelo kit
de par ("Onde o servidor mora").

**O cliente.** Sem cópia e sem banco. Entra na rede privada com chave temporária e etiqueta; uma regra da rede só o
deixa chegar à porta de leitura. Nunca recebe a credencial do banco. Sem par ligado, não funciona ("Onde o servidor
mora").

**A rede entre eles.** Tudo só pela rede privada, nunca exposto à internet. Proteções: senha no banco, cifra de ponta a
ponta no sync, token na porta do banco, configuração inicial e frase-senha por canais separados ("Onde o servidor
mora"). Cada par recebe conexão do outro, só pela rede privada ("Revisão do sync…"). O GitHub fica fora da rede privada
e só recebe a cópia de segurança.

**O que fica de fora do desenho** (mapa, Out of scope): o vault `ai-operating-system` além da leitura como referência
(o hub não desenha nada para ele); o hub como controlador de ferramentas e modelos (segundo mapa); edição concorrente
entre o Obsidian e um agente no mesmo arquivo; controle de acesso por pasta; operação remota e servidor SSH até surgir
o primeiro caso.

---

## 7. O que ainda não está decidido

Tudo abaixo é proposta, pesquisa em curso ou lacuna. Um diagrama que mostrar estes itens deve marcá-los como "a
decidir".

| Assunto | Situação | Onde |
|---|---|---|
| Onde a camada de busca mora | Duas opções em teste: busca no disco com alcance pela rede, ou índice dentro da porta do banco | "Camada de busca" (em curso) |
| Ferramenta de busca e modelo de embeddings | Em bancada; o FreeLLMAPI é uma das origens possíveis | "Camada de busca"; "Modelos de embeddings da busca" (em curso) |
| Como os agentes gravam | Disco, porta do banco ou os dois; conferência de versão no disco; se o Claude Desktop grava | "Como os agentes gravam no hub" (aberto) |
| Como cada ferramenta carrega contrato e MCP | Rodadas respondidas, ticket não resolvido; forma do mod da vigia; hooks no Codex e no Copilot | "Acesso dos agentes: decisão" (em curso) |
| Árvore interna e frontmatter | As seis raízes estão no glossário; o resto da árvore e o frontmatter, não | "Arquitetura de pastas e frontmatter do hub" (em curso) |
| Pasta não replicada | Replicação filtrada ou fora do banco; acesso por SSH fora da construção inicial | idem; mapa, Out of scope |
| Roteamento de skills | Como as skills ficam visíveis e o que entra na tabela | "Roteamento de skills" (aberto) |
| Perfil por máquina | O que é local de cada máquina e como se declara | mapa, Not yet specified |
| Obsidian do hub ao lado do cofre do vault | Convivência enquanto os dois existem | mapa, Not yet specified |
| Prova de conceito → hub real em `C:\context-hub` | Como a passagem acontece | mapa, Not yet specified; "Passagem para a construção" (aberto) |
| FreeLLMAPI no funcionamento do hub | Usos além de embeddings | mapa, Not yet specified |
| Zonas por ciclo de vida (canônica, trabalho, efêmera, derivada) | Só aparecem na exploração, §9, desenhadas para o disco como verdade; não foram fixadas depois | exploração, §9 (fundo) |
| Tela de colisão com três vias editável | Decidida para logo depois da construção, não para o começo | "Como a verdade viaja…" |
| Duas instâncias do MCP por par | **Não verificado** | "Onde o servidor mora" |
| Arquivos entre 50 e 200 MiB | **Não verificado**; conferir na construção | "Revisão do sync…" |
| Guarda do acervo em detalhe | **Não verificado**: ligação de pasta no lugar de link, regra pelos dois caminhos no Windows, aval num terminal sem ninguém olhando, tempo do verificador | "Guarda do acervo…" |

Fundo que não vale mais: a exploração, §7.1 e §9, falava em Markdown como fonte da verdade, hub hospedado numa
máquina e git como sync. As três coisas foram trocadas pelos tickets acima ("Markdown: vista ou fonte…", "Onde o
servidor mora", "Revisão do sync…").
