# Descrição de design do context hub

Versão 2, 2026-10-15, escrita pelo Tech lead do laço do system design. Substitui o `texto-do-hub.md` como fonte de
todo diagrama. É um modelo em sete eixos: **atores, componentes, responsabilidade, pertencimento, ações práticas,
cenários e estado de cada afirmação**. Serve a quem nunca viu o hub e a qualquer modelo. A versão 1 está em
`descricao-do-hub-v1.md`; o que mudou, em `consertos-v2.md`.

## 0. Como ler

**Estado de cada afirmação.** Toda linha leva uma marca entre colchetes:

| Marca | Quer dizer | Fonte |
|---|---|---|
| **[D]** | Decidido, ou fato medido num ticket resolvido | título do ticket entre aspas, ou "mapa" |
| **[C]** | Em curso: o Gustavo já respondeu a rodada, mas o ticket ainda não fechou. Pode mudar. | ticket aberto |
| **[P]** | Prática: o que o Gustavo faz ou disse que faz | onde ele disse |
| **[A]** | A decidir: ninguém decidiu ainda | ticket aberto, "não especificado" do mapa, ou lacuna |
| **[G]** | A decidir com o Gustavo: só ele sabe; está em `perguntas-ao-gustavo.md` | número da pergunta |
| **[NV]** | Não verificado: dito por inferência ou documentação, sem teste | onde aparece |
| **[L]** | Leitura do Tech lead: conclusão tirada de afirmações decididas, sem fonte que a diga com essas palavras | as afirmações de origem |

Quando a fonte é a mesma de toda a linha, ela vem uma vez só. "Mapa" é o `map.md` da frente.

**Três regras de leitura que valem para o texto inteiro:**
1. **Construído × desenhado.** Nada está construído. "O hub faz X" quer dizer "o desenho decidido faz X". Quando uma
   peça decidida ainda precisa ser construída antes de valer (por exemplo, a guarda de versão da porta do banco), a
   linha diz **"a construir"**. Quem desenha deve mostrar essa peça como prevista, não como pronta.
2. **Lugar × grupo.** Um **lugar** é onde a coisa existe de fato (seção 5.2). Um **grupo** é com o que ela faz sentido
   junto (seção 5.1). Um grupo pode atravessar lugares; um diagrama escolhe desenhar um ou outro, e diz qual.
3. **Agente.** "Agente", sem mais, é uma sessão de Claude Code, Codex ou Copilot. O maestro, os recrutas e os
   subagentes **são agentes**, com o que a seção 2 acrescenta. O Claude Desktop **não** é agente de código: é um app
   que o Gustavo usa e que chega por uma ponte.

**Nomes.** Em **negrito**, os termos do `GLOSSARY.md`. Os componentes do hub não se chamam "peças": no glossário,
**peça** é uma unidade do acervo do maestro.

**Sinônimos que o leitor vai encontrar nas fontes:**

| Nome nesta descrição | Também chamado | O que é de fato |
|---|---|---|
| Banco local | CouchDB, o banco | um servidor CouchDB em cada par |
| Sincronizador | CLI do LiveSync, daemon | programa de linha de comando do Self-hosted LiveSync, rodando como tarefa agendada |
| Plugin de sync | LiveSync, plugin | o plugin Self-hosted LiveSync dentro do Obsidian |
| Porta do banco | MCP do banco, MCP do es617, o fork | um servidor MCP (o obsidian-sync-mcp do es617, numa versão modificada) |
| Porta de leitura | MCP só de leitura, segundo MCP | uma segunda instância da porta do banco, só de leitura |
| Camada de busca | busca, OHS, "Leve com alcance" | o obsidian-hybrid-search, com o modelo arctic-embed-m-v2.0, servindo MCP por HTTP |
| Rede privada | tailnet, Tailscale | a rede privada do Tailscale entre as máquinas do Gustavo |
| Cópia no GitHub | cópia de segurança, backup | um repositório privado no GitHub, um ramo por máquina |
| Vigia | vigia do sync | uma tarefa agendada a cada 5 min |
| Checkpoint | hook de fim de resposta, hook `Stop` | um hook que roda ao fim de cada resposta do agente |
| Contrato | `AGENTS.md` da raiz | as regras do hub para os agentes |
| Senha do banco | senha do CouchDB | a credencial de administração do CouchDB; **não** é o token da porta do banco nem a frase-senha |
| Frase-senha | passphrase da E2EE | a chave da cifra de ponta a ponta do LiveSync |

---

## 1. O hub em uma página

O **context hub** é a casa única do contexto que o Gustavo e os agentes leem e gravam [D, glossário]. Ele existe
inteiro em cada **par**: hoje, as duas **máquinas** do Gustavo (o notebook da ARMIS e a máquina pessoal) [D,
"Onde o servidor mora"].

**Por que um banco em cada máquina** [D, "Onde o servidor mora"]: o Gustavo não quer depender de uma máquina fixa como
servidor (isso prenderia o hub a ela) e quer que qualquer computador ou sandbox possa usar o hub. A nuvem saiu porque
ele quer algo pronto logo.

Em cada par há três camadas:
1. **A verdade:** um banco local guarda cada nota com o histórico de versões e as versões em conflito, com o texto
   cifrado [D, "Como a verdade viaja entre as máquinas"; "Onde o servidor mora"].
2. **A vista:** os arquivos no disco, em `C:\context-hub`, que o Gustavo vê e edita no Obsidian [D, "Markdown: vista
   ou fonte da verdade"; "Windows ou WSL"]. **Vista e banco se espelham nos dois sentidos**: quem grava no banco
   (agente pela porta) muda o banco primeiro e a vista logo depois; quem grava no disco (Obsidian, agente, Explorador)
   muda a vista primeiro e o banco logo depois. Em qualquer caso, **o banco é a verdade**: a edição no disco só "conta"
   quando chega ao banco [D, "Markdown: vista ou fonte…"; "Revisão do sync e da divergência com o banco"].
3. **As portas:** os agentes leem e gravam o banco pela porta do banco e acham o conteúdo pela camada de busca
   [D, "Como a verdade viaja…"; "Camada de busca"].

Os pares trocam mudanças direto, pela rede privada: cada um envia as próprias mudanças ao outro. Nenhum é a
referência [D, "Revisão do sync…"; glossário, "Par"]. Cada par envia as suas, em vez de um puxar tudo, para que o aviso
de troca parada nasça na máquina que travou [D, "Onde o servidor mora", comentário de 2026-10-12]. Uma vez por dia,
cada máquina guarda a vista no GitHub, como cópia de segurança [D, "Revisão do sync…"]. Uma vigia em cada máquina
confere a cada 5 minutos se algo diverge e avisa [D, idem].

Em volta disso, a **disciplina do agente** faz o agente gravar no lugar certo sem o Gustavo pedir: o contrato diz onde
cada coisa mora, a checagem de início de sessão abre a nota de retomada, e o checkpoint obriga o agente a mantê-la em
dia [D, "Contrato file-first: zonas e checkpoint"; "Lições do vault"].

**Duas coisas que não se confundem** [D, "Portas de entrada do hub"; "Lições do vault"]:
- a sessão **abre** numa **porta de entrada** (a principal é a sessão na raiz do hub);
- o agente **chega ao conteúdo** pela **camada de busca**, não andando pela árvore de pastas.

**O destino** (mapa, Destination): o hub funcionando nas duas máquinas, cumprindo cinco critérios:
1. agentes (Claude Code, Codex, Copilot, dentro ou fora do Maestri), em qualquer máquina, acham o trecho certo pela
   busca, sem ler tudo;
2. o que importa é gravado no lugar certo sem o Gustavo pedir;
3. os `.md` continuam editáveis no Obsidian, a busca está sempre acessível, e o agente também pode editar direto no
   disco, com sync para a outra máquina;
4. nada diverge em silêncio entre as máquinas;
5. existe proteção para a **edição concorrente**.

**Hoje é uma prova de conceito.** Nada está construído. Os tickets decidem o desenho; a construção vem depois, em
tickets gerados por "Passagem para a construção" [D, mapa, Notes]. Esta frente nasce no hub quando ele existir [D,
"Workloads piloto"]; até lá, mapa e tickets vivem no repositório da prova de conceito (`C:\Projetos\context-hub`). Como
a prova de conceito vira o hub real em `C:\context-hub` [A, mapa, Not yet specified].

**Princípios do desenho** [D, "Lições do vault"]. Valem para todo componente; um diagrama deve deixá-los visíveis:
- uma falha se corrige com **mecanismo**, ou tirando regra, nunca acrescentando regra;
- **cada informação tem um lugar só**, escrito no contrato; por isso uma iniciativa mora numa **casa** só, e uma coisa
  pode pertencer a dois **grupos** lógicos sem ter dois **lugares**;
- **o checkpoint grava sem pedido**, inclusive a triagem e a promoção;
- **a porta de entrada ao conteúdo é a busca**; índice mantido à mão só onde a busca não basta;
- **aval** só para o contrato, os adaptadores e as exclusões ou reescritas grandes. Motivo: no vault, pedir aval para
  tudo foi uma das falhas;
- **complexidade conquistada:** uma camada só entra se resolve um dos cinco critérios;
- todo arquivo tem destino quando envelhece: **compactar ou arquivar**. O hub não apaga nada por idade;
- textos curtos; frontmatter só com o que a busca ou o contrato usam.

---

## 2. Atores

Quem age no hub, o que quer, por onde chega e **onde está**.

| Ator | Quem é | O que quer | Por onde chega | Onde está | Estado |
|---|---|---|---|---|---|
| **Gustavo** | o dono do hub | ver e editar as notas; achar o que precisa; que os agentes guardem sozinhos o que importa; nunca perder trabalho em silêncio | Obsidian; pedindo a agentes; Claude Desktop | diante de uma das máquinas | [D, glossário; mapa, Destination] |
| **Agente** (de código) | uma sessão de Claude Code, Codex ou Copilot (VS Code e linha de comando), dentro ou fora do Maestri | achar o trecho certo sem ler tudo; retomar de onde parou; gravar sem desfazer a gravação de outro | porta de entrada; porta do banco; camada de busca; disco | sessão na máquina | [D, "Windows ou WSL"; "Portas de entrada do hub"] |
| **Maestro** | um agente que orquestra um workspace do Maestri | montar e conduzir um workspace sem redescobrir nem depender do Gustavo ditar | sessão do Maestri; começa pelo acervo do maestro | sessão na máquina | [D, "Maestri: padrão e liberdade"] |
| **Recruta** | um agente num terminal do Maestri, com papel | fazer a parte dele do trabalho | terminal com papel, aberto em `.maestri/roles/<id>/` da pasta do workspace; o que ele recebe do contrato está em 8.3 | sessão na máquina | [D, "Testes do papel do Maestri…"] |
| **Subagente** | ajudante que roda dentro de um agente, sem ocupar terminal | uma tarefa curta | herda a sessão de quem o chamou | dentro da sessão de outro agente | [D, "Acervo do maestro: pesquisa de peças"]; se os hooks de sessão valem para ele [NV] |
| **Claude Desktop** | o app Claude no Windows (chat e work), usado pelo Gustavo | ler o hub quando o Gustavo pede; gravar também, segundo o Gustavo | ponte local `mcp-remote` até a porta do banco | app na máquina | leitura [D, "Portas de entrada do hub"]; gravar [A, "Como os agentes gravam no hub"] |
| **Cliente** | computador ou sandbox sem cópia do hub (máquina de passagem, sandbox de teste); quem está nele não tem vista nem Obsidian, só o agente consultando | consultar o hub | rede privada até a porta de leitura de um par | fora dos pares | [D, "Onde o servidor mora"; glossário]; quem usa de fato e quem recebe a chave [G, 8 e 11] |
| **Outro par** | a outra máquina, igual a esta | receber as mudanças daqui e enviar as dela | rede privada, de banco a banco | a outra máquina | [D, "Revisão do sync…"] |
| **Agendador do Windows** | o serviço do Windows que dispara tarefas | rodar sincronizador, vigia e cópia diária sem ninguém pedir | no logon e em intervalos | cada máquina | [D, "Revisão do sync…"] |
| **Hooks** | checagem de início de sessão, checkpoint, hook de uso, lembrete do maestro, guarda do acervo | impor por mecanismo o que a regra sozinha não garante | configuração de usuário de cada ferramenta; rodam **dentro** da sessão do agente | configuração da máquina | [D, "Contrato file-first…"; "Maestri: padrão e liberdade"]; escopo do usuário nos três [C, "Acesso dos agentes: decisão"]; por ferramenta, ver 3.1 |
| **Verificador** | um modelo diferente que confere uma alteração no acervo | barrar mudança ruim numa peça | chamado pela guarda do acervo, só no Claude Code | sessão na máquina | [D, "Maestri: padrão e liberdade"] |

**"O par" não é ator.** É o lugar: a máquina com cópia completa. Componentes "do par" rodam ali; quem responde por eles
está na seção 4.

Gente e agentes chegam ao hub pelas portas [D, "Portas de entrada do hub"].

---

## 3. Componentes

Inventário completo, por lugar. "Rótulo" é o nome curto que um diagrama usa. A seção 4 dá a responsabilidade de cada
linha; a 5, o grupo e o lugar.

### 3.1 Em cada par

Sistema: Windows, disco NTFS, hub em `C:\context-hub`; WSL fora até surgir caso de uso [D, "Windows ou WSL"].

**Núcleo de dados**

| Componente | Rótulo | Papel, numa frase | Estado |
|---|---|---|---|
| Banco local (CouchDB) | Banco local | Guarda a verdade: cada nota como um documento de metadados mais pedaços de texto, com histórico de versões e as versões em conflito; o texto fica cifrado de ponta a ponta. A compactação automática apaga corpos de versões antigas, sem prazo fixo nas fontes. | [D, "Como a verdade viaja…"; "Spike: CouchDB e LiveSync"; "Onde o servidor mora"] |
| **Vista Markdown** | Vista Markdown | Os arquivos no disco por onde o Gustavo vê e edita o hub; espelha o banco nos dois sentidos (seção 1). | [D, glossário; "Markdown: vista ou fonte…"] |
| **Sincronizador** | Sincronizador | Liga disco e banco o tempo todo, nos dois sentidos, sem depender do Obsidian aberto; pega o que qualquer programa grava no disco. É escritor do disco. Sobrevive ao banco caindo no meio do trabalho; volta sozinho em até 1 min se o processo morrer. | [D, "Revisão do sync…"; "Teste: disco e banco sem o Obsidian"] |
| Obsidian com o plugin de sync | Obsidian | Onde o Gustavo vê, edita e resolve conflito; pode ficar fechado. O cofre é a raiz do hub. Aberto, o plugin também leva edições do disco ao banco e escreve no disco o que vem do banco: é o outro escritor do disco. Plugin e sincronizador ligados juntos na mesma pasta não criam ciclo nem conflito. | [D, "Revisão do sync…"; "Teste: disco e banco…", jeito 1; "Portas de entrada do hub"] |
| Assistente de configuração do plugin (Config Doctor) | Assistente do plugin | Abre depois de atualizar o plugin e para o sync daquele cofre até alguém responder; a vigia confere se ele travou. | [D, "Teste: disco e banco…"; "Revisão do sync…"] |
| Regra de exclusão | Exclusão | Regra configurada **no sincronizador e no plugin** que deixa fora do banco pastas com ponto em qualquer nível; precisa cobrir também arquivos com ponto. | [D, "Revisão do sync…"]; cobertura [A, teste na construção; ver 8.16] |

**Portas**

| Componente | Rótulo | Papel, numa frase | Estado |
|---|---|---|---|
| Porta do banco (MCP) | Porta do banco | Porta do agente ao banco. Lê devolvendo a versão; grava levando a versão lida, e a gravação vira conflito visível se a versão mudou; diz ao agente quando uma nota está em conflito. Tem a frase-senha, então entrega texto em claro a quem a usa. | papel [D, "Como a verdade viaja…"]; a guarda de versão e o aviso de conflito são **a construir** (o MCP pronto grava por cima) [D, "Montar: CouchDB, LiveSync e MCP"; "Spike: CouchDB e LiveSync"] |
| Porta de leitura (segundo MCP) | Porta de leitura | Segunda instância da porta do banco, com `READ_ONLY` ligado para a instância inteira e um token próprio, exposta na rede privada só para os clientes. Recusa gravação no próprio servidor. Entrega texto em claro ao cliente. | [D, "Onde o servidor mora"; "Testes das portas de entrada"]; formato da recusa [NV] |
| **Camada de busca** (obsidian-hybrid-search + arctic-embed-m-v2.0) | Camada de busca | Entrega ao agente o trecho certo sem ele ler tudo: busca por palavra e por sentido sobre a vista do disco daquela máquina, servida por MCP em HTTP na rede privada. **Só lê.** O glossário admite que a camada também grave; a busca decidida não grava, e gravar é pela porta do banco. | [D, "Camada de busca"; "Modelos de embeddings da busca"; glossário] |
| Índice da busca | Índice da busca | Arquivo `.obsidian-hybrid-search.db` na raiz do hub, um por máquina; tem ponto no nome, então não vai ao banco. | [D, "Camada de busca"] |
| Ponte `mcp-remote` | Ponte do Desktop | MCP local (stdio) que liga o Claude Desktop à porta do banco pela URL da rede privada. | [D, "Portas de entrada do hub"; "Testes das portas de entrada"] |

**Vigilância**

| Componente | Rótulo | Papel, numa frase | Estado |
|---|---|---|---|
| Vigia | Vigia do sync | A cada 5 min confere a troca entre os bancos, conflitos abertos, binários descartados, arquivos acima do limite, se o sincronizador está vivo e se o assistente do plugin travou o sync; grava um estado curto e avisa quando piora. | [D, "Revisão do sync…"]; onde o estado curto fica [NV] |
| Avisos | Avisos | Três saídas da vigia: notificação do Windows quando piora; o estado curto, lido no início de sessão; o estado visível o tempo todo na tela do agente. | [D, idem]; na tela: mod no Claude Code, barra de estado no Copilot, checagem e notificação no Codex [C, "Acesso dos agentes: decisão"] |
| Mod de estado (Claude Code) | Mod de estado | Mostra o estado da vigia o tempo todo na sessão do Claude Code; avisa mesmo sem a checagem de início. | [D, "Revisão do sync…"] |
| Comando de recuperar binário | Recuperar binário | Recupera para um arquivo ao lado a versão de binário perdida numa colisão. | [D, idem] |

**Disciplina do agente**

| Componente | Rótulo | Papel, numa frase | Estado |
|---|---|---|---|
| Contrato (`AGENTS.md` na raiz) | Contrato | As regras do hub para os agentes, incluindo o lugar de cada informação e a primeira instrução do maestro. O hub não tem `CLAUDE.md` em lugar nenhum, porque um `CLAUDE.md` acima ou dentro do hub faz o Claude Code deixar de ler os `AGENTS.md`. | [D, "Portas de entrada do hub"; "Maestri: padrão e liberdade"] |
| Ligações do contrato e das skills | Ligações da ferramenta | Em cada máquina, a configuração global de cada ferramenta aponta para o contrato (import no Claude Code; link simbólico no Codex e no Copilot) e para as skills (junction). O link simbólico exige o modo de desenvolvedor do Windows. | [D, "Portas de entrada do hub"; "Testes da porta do repositório fora do hub"] |
| Checagem de início de sessão | Checagem de sessão | Hook no começo de toda sessão de agente: lê o estado da vigia, informa a hora da última troca e abre a nota de retomada. | [D, "Contrato file-first…"; "Divergência e edição concorrente"]; no Codex e no Copilot, ver tabela abaixo |
| Checkpoint (hook de fim de resposta) | Checkpoint | Ao fim de cada resposta, se a nota de retomada não reflete a resposta, ou se a memória privada ganhou algo que o hub não tem, **obriga o agente** a continuar e gravar. O hook não grava; o agente grava. | [D, "Contrato file-first…"] |
| Guarda do acervo | Guarda do acervo | No Claude Code, recusa a gravação no acervo, roda o verificador em outro modelo e só libera com relatório e aval do Gustavo. No Codex e no Copilot, recusa toda gravação no acervo. | [D, "Maestri: padrão e liberdade"]; detalhes [NV, "Guarda do acervo: mods e hooks"] |
| Hook de uso | Hook de uso | Grava no registro de uso quem usou qual peça. | [D, "Maestri: padrão e liberdade"] |
| Lembrete do maestro | Lembrete do maestro | Hook de início que só age em terminal do Maestri; lembra o agente de que é maestro e de onde está o acervo. | [D, idem]; se age também em terminal de recruta [A] |
| Script do arquivo | Script do `_archive/` | Move uma pasta para o `_archive/` da raiz depois de conferir que o outro par está em dia e sem edição recente. | [D, "Portas de entrada do hub"] |
| Kit de par | Kit de par | Script e configuração modelo que montam um par: rede privada, banco e portas, sincronizador, ligações, regras (sem `CLAUDE.md`, `claude-md-and-agents-md` ligado, modo de desenvolvedor). | [D, "Onde o servidor mora"; "Portas de entrada do hub"; "Maestri: padrão e liberdade"] |

**O que cada ferramenta recebe da disciplina:**

| Mecanismo | Claude Code | Copilot | Codex |
|---|---|---|---|
| Contrato na raiz | sim [D] | sim [D] | sim [D] |
| Contrato numa subpasta | sim, lê a cadeia sozinho [D, "Testes das portas de entrada"] | pelo arquivo global [D, "Portas de entrada do hub"]; pelo `.git` da raiz [C] | precisava de marcador no teste [D, "Testes das portas…"]; o `.git` da raiz no lugar do marcador [C, "Acesso dos agentes: decisão"], não testado com o hub [NV] |
| Checagem de início | sim [D] | hook de usuário passou no teste [C] | em investigação [A] |
| Checkpoint | sim, hook `Stop` [D] | hook de fim mais extensão experimental [C] | em investigação [A] |
| Estado da vigia na tela | mod [D] | barra de estado [C] | só checagem e notificação [C] |
| Guarda do acervo | forte: recusa, verificador, aval [D] | recusa; não tem hook que chame modelo [D, "Guarda do acervo: mods e hooks"] | recusa; sem `ask` em hook nem hook de modelo [D, idem] |
| Hook de uso e lembrete | garantidos [D] | dependem de teste [A] | dependem de teste [A] |
| Skills | `~/.claude/skills` [D, "Acesso dos agentes: pesquisa"] | `~/.agents/skills` (e `~/.copilot/skills`); com `COPILOT_HOME` definido deixa de ler `~/.agents/skills` [D, "Acesso dos agentes: Copilot"] | `~/.agents/skills` [D, "Acesso dos agentes: pesquisa"] |

Cada skill do hub precisa de duas entradas, uma em `~/.claude/skills` e outra em `~/.agents/skills` [D, "Acesso dos
agentes: pesquisa"]. Como as skills ficam visíveis e o que entra na tabela de roteamento [A, "Roteamento de skills"].

**Periferia e máquina**

| Componente | Rótulo | Papel, numa frase | Estado |
|---|---|---|---|
| Cópia local (`.git` na raiz) | Cópia local (git) | Repositório git de cada máquina, que só faz commit e push uma vez por dia, um ramo por máquina; nunca puxa nem escreve no disco do hub. Também faz o Copilot (e, em curso, o Codex) achar a raiz. | [D, "Revisão do sync…"]; papel de raiz [C] |
| Tarefa da cópia diária | Cópia diária | Tarefa agendada que faz o commit e o push. | [D, idem] |
| Nó da rede privada | Nó da rede | Põe o par na rede privada (Tailscale, só no Windows). A chave do nó vence em 180 dias; a máquina pessoal precisa do modo sem login. | [D, "Revisão do sync…"; "Ligar as máquinas com segurança"] |
| Credenciais do par | Credenciais | Senha do banco, frase-senha da cifra, token da porta do banco, token da porta de leitura, chave de escrita no GitHub. Ficam na máquina (configuração do kit de par), não no hub. | [D, "Onde o servidor mora"; "Ponto de encontro do sync"]; arquivo exato [NV] |
| Configuração do Maestri | Biblioteca do Maestri | Papéis e partituras no perfil do usuário (`~/.maestri`), fora do hub. | [D, "Portas de entrada: pesquisa"] |
| Pasta do papel | Pasta do papel | `.maestri/roles/<id>/` na pasta do workspace, com o `CLAUDE.md`, o `AGENTS.md` e o `role.json` do papel, gravados pelo Maestri. Tem ponto: não replica. | [D, "Testes do papel do Maestri…"] |
| Memória privada da ferramenta | Memória privada | A memória automática de cada ferramenta (no Claude Code, ligada), no perfil do usuário da máquina. Não é o hub: o checkpoint leva ao hub o que só ela sabe. | [D, "Contrato file-first…"] |

### 3.2 O conteúdo (o que mora dentro do hub)

| Componente | Rótulo | Papel | Estado |
|---|---|---|---|
| **Raiz** (seis) | Raiz | Primeiro nível, cada uma com comportamento próprio: `clients/` (iniciativas de cliente, dois níveis: cliente e iniciativa), `operations/` (trabalho contínuo, sem fim), `initiatives/` (iniciativas sem cliente: produtos, frentes, estudo), `reference/` (conhecimento de referência, promovido), `agents/` (a oficina dos agentes: contrato, skills, papéis, perfil de cada máquina), `inbox/` (captura rápida). O que termina vai para o `_archive/` da própria raiz. | [D, glossário; "Métodos conhecidos de organizar a raiz"]; níveis e `agents/machines/<máquina>.md` [C, "Arquitetura de pastas e frontmatter"] |
| **Iniciativa** | Iniciativa | Frente de trabalho com identificador, estado e próxima ação; mora numa **casa** só. | [D, glossário; "Workloads piloto"] |
| Núcleo da iniciativa | Núcleo | `initiative.md` (ficha), `retomada.md`, `tasks.md`, `decisions.md`, `context.md`, `log/AAAA-MM.md`; o `AGENTS.md` da iniciativa só com o mapa e as regras próprias. | [C, "Arquitetura de pastas…"] |
| Blocos da iniciativa | Blocos | Subpastas com um nome só, somadas conforme o trabalho pede, descritas em `agents/blocks.md`; o que não cabe vai para `other/`. | [C, idem] |
| **Nota de retomada** | Nota de retomada | Um arquivo curto por trabalho, sobrescrito, com sete campos; permite a qualquer sessão continuar de onde a outra parou. É uma nota como as outras: editada no disco, volta ao banco; o histórico fica nas decisões e na cópia diária. | [D, "Contrato file-first…"]; arquivo `retomada.md` [C] |
| **Acervo do maestro** | Acervo do maestro | Peças prontas para todo maestro, **dentro ou fora do hub**, como família de skills `maestro-*` em `agents/skills/` (`maestro-acervo` é a porta); opções, não regras. | [D, "Maestri: padrão e liberdade"; glossário] |
| Variante de setup | Variante | Um setup que declara a base e só o que muda; quem a resolve é o maestro, pela skill do acervo. | [D, "Maestri: padrão e liberdade"] |
| Propostas | Propostas | Pasta `agents/maestro/propostas/`, onde o Codex e o Copilot deixam a mudança que queriam fazer no acervo; um maestro no Claude Code as avalia. | [D, idem] |
| Registro de uso | Registro de uso | `agents/maestro/uso/<máquina>.md`, um arquivo por máquina (peça, workspace, máquina, data); por isso registros das duas máquinas não se misturam. | [D, idem] |
| Versão local de peça | Versão local | Ajuste de uma peça para uma iniciativa, em `maestro/` da pasta onde o workspace abre (opcional). A versão local de um papel é a que vai para a biblioteca do Maestri **daquele workspace**. | [D, idem] |
| Skills do hub | Skills | Em `agents/skills/<skill>/`. | [D, "Portas de entrada do hub"] |
| Catálogo de blocos | Catálogo de blocos | `agents/blocks.md`, citado pelo contrato, mais a skill "nova iniciativa", que cria pasta, núcleo e blocos por script; a skill só muda com supervisão e aprovação. | [C, "Arquitetura de pastas…"] |
| Segredos da iniciativa | Segredos | Pasta `.secrets/` dentro da iniciativa, fora do banco e do git; senhas de contas que acessam ambiente de cliente ficam no KeePass, fora do hub. | [C, idem]; ver 8.16 |
| **Pasta não replicada** | Pasta não replicada | Parte do hub numa máquina só, fora do sync e da cópia no GitHub; a outra máquina a alcança por SSH; a busca da outra máquina não a indexa; cada pasta declara se é replicada. **Hoje não há nenhuma**: tudo vive nas duas máquinas. | conceito [D, glossário]; SSH escolhido como acesso [D, "Ligar as máquinas com segurança"]; SSH e a primeira pasta entram só quando surgir o caso [D, mapa, Out of scope]; mecanismo que a tira do sync [A, "Arquitetura de pastas…"] |

**Duas classes diferentes de "fica fora":** a pasta não replicada é **declarada** pasta a pasta e alcançável por SSH;
pastas e arquivos com ponto ficam fora **por regra de exclusão** e não são alcançáveis pela outra máquina. Uma pasta com
ponto não é pasta não replicada [L, glossário; "Revisão do sync…"].

**Pasta não replicada e raiz são critérios independentes:** uma pasta de `clients/` poderia ser declarada não replicada
[L, glossário, "Raiz" e "Pasta não replicada"]. Hoje nenhuma é.

**O que vai ao banco** [D, "Revisão do sync…"; "Teste: disco e banco sem o Obsidian"]:
- todo arquivo comum até 200 MiB (limite fixado pelo Gustavo e aplicado por configuração no sincronizador e no plugin);
- só `.md`, `.txt` e `.csv` são texto, com junção automática; o resto (`.docx`, `.xlsx`, `.pdf`, imagens, `.py`,
  `.json`…) é binário, sem junção;
- pastas com ponto, em qualquer nível, ficam fora pela regra de exclusão (ver o defeito medido em 8.16);
- repositório de código mora fora do hub.

**Conteúdo inicial** [D, "Workloads piloto"]: nasce no hub esta frente e o que o Gustavo disser. O que vem do vault
`ai-operating-system` é **copiado** e trabalhado só no hub; o que fica no vault é referência, não segunda casa. Já
desejados: `armis-docs`, `armis-brand` e a skill `armis-docx`. A operação de SOC da iniciativa STRATA fica fora por ora.

### 3.3 Fora das máquinas

| Componente | Rótulo | Papel | Onde | Estado |
|---|---|---|---|---|
| Rede privada (tailnet) | Rede privada | O único caminho entre pares e entre cliente e par; nunca exposta à internet (nunca o Funnel do Tailscale). Regras de acesso (grants) por etiqueta e porta. | serviço Tailscale | [D, "Onde o servidor mora"; "Revisão do sync…"]; nada detecta o Funnel ligado por engano [A] |
| Repositório privado no GitHub | Cópia no GitHub | Cópia de segurança diária da vista, um ramo por máquina; não é ponto de encontro do sync. | GitHub | [D, "Revisão do sync…"; "Ponto de encontro do sync"] |
| **Cliente** | Cliente | Computador ou sandbox que usa o hub através de um par, sem cópia; só lê por padrão; precisa de um par ligado. | qualquer | [D, glossário; "Onde o servidor mora"] |
| Vault `ai-operating-system` | Vault (referência) | Só referência: o agente pode ler, direto no disco; o hub não grava nada nele, nem ponteiro. Só existe no notebook. | notebook | [D, "Workloads piloto"] |
| FreeLLMAPI | Gateway de modelos | Gateway de modelos gratuitos. Depois da construção roda só na máquina pessoal, preso à rede privada; o notebook o chama pela rede, por um endereço configurável. Quem o chama: o roteamento de tarefas simples dos agentes e o índice do Google, se ligado. | máquina pessoal | [P, Gustavo no chat, em "Passagem para a construção"]; roteamento [D, "Maestri: padrão e liberdade"]; destino quando cai [A] |
| Modelo de embeddings do Google (gemini-embedding-001) | Embeddings na nuvem | Segunda opção da busca por sentido, configurada num índice ao lado do arctic e **desligada**. Ligar é escolha do Gustavo; ligado, o texto indexado vai ao Google e a busca por sentido depende da rede e da cota. | Google, pelo FreeLLMAPI | [D, "Camada de busca"; "Modelos de embeddings…"]; se roda ao lado do arctic [NV]; gatilho [G, 12] |
| Tailscale da empresa | Rede da empresa | Risco: o software corporativo do notebook pode conflitar com o Tailscale, a empresa pode travar a rede permitida, e entrar com identidade corporativa pode cair na rede da empresa. A consulta ao TI foi dispensada pelo Gustavo. | notebook | risco [D, "Ligar as máquinas com segurança"]; dispensa [P, "Passagem para a construção"]; comportamento se bloquear [A] |

### 3.4 Portas de entrada

Cada caminho pelo qual alguém chega ao hub. A porta diz **onde a sessão abre**; o conteúdo se alcança pela busca.

| Porta | Quem usa | O que recebe | Estado |
|---|---|---|---|
| Sessão na raiz do hub (a principal) | Gustavo, agentes | Os três harnesses leem o `AGENTS.md` da raiz | [D, "Portas de entrada do hub"; "Testes das portas de entrada"] |
| Sessão numa subpasta | agentes | Ver a tabela "O que cada ferramenta recebe" em 3.1 | idem |
| Maestri (workspace e papel) | maestro, recrutas | Workspace de iniciativa abre na pasta dela; o que cruza iniciativas, na raiz; código, no repositório. Dentro de um papel, ver 8.3. | [D, "Maestri: padrão e liberdade"] |
| Obsidian | Gustavo | O cofre é a raiz do hub | [D, "Portas de entrada do hub"] |
| Claude Desktop | Gustavo, pelo app | Leitura pela ponte; não recebe o contrato por arquivo nem as instruções do MCP | [D, idem; "Testes das portas de entrada"] |
| Cliente pelo MCP de um par | sandbox, máquina de passagem | O começo do contrato nas instruções do MCP (que chegam inteiras só ao Claude Code e ao Copilot do VS Code); a regra curta "antes de gravar, leia `AGENTS.md`" na descrição das ferramentas, **o único canal que a fonte mostra chegando ao modelo nos três**; e o contrato na configuração global, onde der para instalar | [D, "Portas de entrada do hub"; "Contrato pelo MCP: pesquisa"] |
| Sessão num repositório fora do hub | agentes | Contrato por import (`~/.claude/CLAUDE.md`) e por link simbólico (`~/.codex/AGENTS.md`, `~/.copilot/copilot-instructions.md`, que hoje tem o GSD; o kit junta os dois); skills por junction; o acervo vale aqui também | [D, idem; "Testes da porta do repositório…"] |

Porta nova que surgir entra como ticket novo, com a mesma regra: só o que ela precisa [D, "Portas de entrada do hub"].

---

## 4. Responsabilidade

**Regras da matriz:**
- **Dono:** quem decide como o componente é e responde por ele. É sempre um ator da seção 2. O Gustavo é dono de toda a
  infraestrutura das máquinas dele e de todo o conteúdo; quando a fonte dá a um agente a decisão do dia a dia, a coluna
  diz.
- **Aciona:** quem faz o componente agir ou grava nele.
- **Lê:** quem usa o conteúdo ou o resultado.
- **Só vê:** quem enxerga o estado sem usar o conteúdo.
- **Aprova:** quem dá o aval, quando há aval.
- "Agentes" inclui maestro, recrutas e subagentes (seção 0). "Hooks" funcionam conforme a ferramenta (tabela em 3.1).
- "—" quer dizer "ninguém" segundo as fontes. "[G, n]" quer dizer "a decidir com o Gustavo".

### 4.1 Núcleo de dados e portas

| Componente | Dono | Aciona | Lê | Só vê | Aprova | Estado |
|---|---|---|---|---|---|---|
| Banco local | Gustavo | sincronizador, plugin, porta do banco, replicação do outro par | porta do banco, porta de leitura, sincronizador, plugin, replicação do outro par | vigia | — | [D, "Revisão do sync…"; "Onde o servidor mora"] |
| Vista Markdown | Gustavo | sincronizador, plugin, Gustavo (Obsidian, Explorador), agentes (disco) | Gustavo, camada de busca, agentes (disco), cópia diária | — | — | [D, "Markdown: vista ou fonte…"; "Camada de busca"] |
| Sincronizador | Gustavo | Agendador do Windows | disco e banco | vigia (se está vivo) | — | [D, "Revisão do sync…"] |
| Obsidian e plugin | Gustavo | Gustavo (abre, fecha, edita, resolve conflito) | Gustavo | vigia (assistente travado) | — | [D, idem] |
| Assistente do plugin | Gustavo | atualização do plugin | — | Gustavo, vigia | Gustavo responde | [D, "Teste: disco e banco…"] |
| Regra de exclusão | Gustavo | kit de par (configura) | sincronizador, plugin | — | — | [D, "Revisão do sync…"] |
| Porta do banco | Gustavo | agentes (ler e gravar), Claude Desktop pela ponte (ler) | agentes, Claude Desktop | — | — | [D, "Como a verdade viaja…"; "Portas de entrada do hub"] |
| Porta de leitura | Gustavo | clientes | clientes | — | Gustavo libera gravação a cliente (padrão: não) | [D, "Onde o servidor mora"] |
| Camada de busca | Gustavo | agentes, clientes | agentes, clientes | — | Gustavo liga o índice do Google | [D, "Camada de busca"]; Gustavo e Claude Desktop usarem a busca [G, 15]; regra de rede para clientes [A] |
| Índice da busca | Gustavo | camada de busca | camada de busca | — | — | [D, idem] |
| Ponte `mcp-remote` | Gustavo | Claude Desktop | — | — | — | [D, "Portas de entrada do hub"] |

### 4.2 Vigilância

| Componente | Dono | Aciona | Lê | Só vê | Aprova | Estado |
|---|---|---|---|---|---|---|
| Vigia | Gustavo | Agendador do Windows | banco, sincronizador, plugin | — | — | [D, "Revisão do sync…"]; quem religa se parar [A] |
| Avisos (notificação, estado curto) | Gustavo | vigia | checagem de sessão (estado curto) | Gustavo, agentes | — | [D, idem] |
| Mod de estado | Gustavo | vigia (o estado que mostra) | — | Gustavo e o agente, na sessão do Claude Code | — | [D, idem] |
| Comando de recuperar binário | Gustavo | Gustavo, ou agente com ele vendo | — | — | — | [D, idem]; quem roda [G, 11] |

### 4.3 Disciplina do agente

| Componente | Dono | Aciona | Lê | Só vê | Aprova | Estado |
|---|---|---|---|---|---|---|
| Contrato | Gustavo | ligações da ferramenta; a sessão ao abrir; agente edita só dentro do hub | todo agente; cliente (o começo) | — | Gustavo aprova toda mudança | [D, "Lições do vault"; "Testes da porta do repositório…"]; onde fica o registro do aval [A] |
| Ligações da ferramenta | Gustavo | kit de par | cada ferramenta ao abrir | — | Gustavo (são adaptadores) | [D, "Portas de entrada do hub"; "Lições do vault"] |
| Kit de par | Gustavo | Gustavo, ao montar um par | — | — | — | [D, "Onde o servidor mora"]; quem liga o modo de desenvolvedor [G, 11] |
| Checagem de sessão | Gustavo | toda sessão de agente ao abrir | estado curto, nota de retomada | agente | — | [D, "Contrato file-first…"] |
| Checkpoint | Gustavo | fim de cada resposta | nota de retomada, memória privada | — | — | [D, idem]; quem percebe se falhar [A] |
| Guarda do acervo | Gustavo | tentativa de gravar no acervo | — | Gustavo (o pedido de aval) | Gustavo, depois do verificador | [D, "Maestri: padrão e liberdade"] |
| Verificador | Gustavo | guarda do acervo | a alteração proposta | — | — | [D, idem] |
| Hook de uso | Gustavo | uso de uma peça | — | — | — | [D, idem] |
| Lembrete do maestro | Gustavo | abertura de terminal do Maestri | — | maestro | — | [D, idem] |
| Script do `_archive/` | Gustavo | [G, 4] | estado do outro par | — | — | [D, "Portas de entrada do hub"] |

### 4.4 Conteúdo

| Componente | Dono | Aciona | Lê | Só vê | Aprova | Estado |
|---|---|---|---|---|---|---|
| Raízes e árvore | Gustavo | agentes e Gustavo gravam; o script move ao `_archive/` | todos os que leem o hub (Gustavo, agentes, Claude Desktop, clientes) | — | Gustavo para reescrita ou exclusão grande | [D, glossário; "Lições do vault"] |
| Iniciativa | Gustavo decide que nasce e que termina | agentes trabalham nela | os mesmos | — | — | [D, "Workloads piloto"]; quem decide que terminou [G, 4] |
| Nota de retomada | Gustavo (como todo conteúdo) | agente da sessão, obrigado pelo checkpoint | checagem de sessão, qualquer sessão nova, Gustavo, clientes (leitura) | — | — | [D, "Contrato file-first…"]; quem confere que ficou certa: só o checkpoint [D, idem] |
| `inbox/` | Gustavo | Gustavo, agentes | checkpoint (triagem) | — | — | [D, glossário; "Lições do vault"] |
| `reference/` (promoção) | Gustavo | checkpoint (promove) | todos | — | — | [D, "Lições do vault"] |
| Acervo do maestro | Gustavo | maestro (acrescenta sozinho; altera com aval) | maestro, recrutas (os papéis) | — | Gustavo, para alterar ou apagar peça citada ou usada, mexer em catálogo ou descrição de skill, peça com nome ou gatilho parecido, ou contrato-opção que se diz padrão | [D, "Maestri: padrão e liberdade"] |
| Propostas | Gustavo | Codex e Copilot gravam | maestro no Claude Code avalia | — | — | [D, idem] |
| Registro de uso | Gustavo | hook de uso | maestro | — | — | [D, idem] |
| Versão local de peça | Gustavo | maestro | maestro; vai para a biblioteca do Maestri do workspace | — | — | [D, idem] |
| Catálogo de blocos e skill "nova iniciativa" | Gustavo | agente cria pasta pela skill | agentes | — | Gustavo, para mudar a skill | [C, "Arquitetura de pastas…"] |
| Segredos (`.secrets/`) | Gustavo | Gustavo, agentes | agentes da máquina | — | — | [C, idem] |
| Pasta não replicada | Gustavo | — (nenhuma existe) | — | — | — | [D, mapa, Out of scope] |

### 4.5 Máquina, rede e fora

| Componente | Dono | Aciona | Lê | Só vê | Aprova | Estado |
|---|---|---|---|---|---|---|
| Cópia local e tarefa diária | Gustavo | Agendador do Windows | — | — | — | [D, "Revisão do sync…"] |
| Cópia no GitHub | Gustavo | tarefa diária (push) | Gustavo, em restauração | — | — | [D, idem]; quem restaura e como [G, 11] |
| Nó da rede, rede privada, grants | Gustavo | pares, clientes | — | — | Gustavo dá chave a cliente | [D, "Onde o servidor mora"]; quem revoga chave [G, 11] |
| Credenciais | Gustavo | kit de par | banco, portas, sincronizador, plugin, git | — | — | [D, "Onde o servidor mora"] |
| Biblioteca do Maestri | Gustavo | app Maestri; maestro pela linha de comando do Maestri (cria e reescreve papéis) | Maestri, ao abrir terminais | — | — | [D, "Maestri: padrão e liberdade"] |
| Pasta do papel | Gustavo | app Maestri (grava ao criar e ao editar o papel) | o agente do terminal | — | — | [D, "Testes do papel do Maestri…"] |
| Memória privada | Gustavo | a ferramenta | a mesma ferramenta, na mesma máquina | — | — | [D, "Contrato file-first…"]; se outro agente a lê [NV] |
| FreeLLMAPI | Gustavo | agentes (roteamento), busca (gemini, se ligado) | — | — | — | [P, "Passagem para a construção"] |
| Embeddings na nuvem | Gustavo | busca, se ligado | — | — | Gustavo liga | [D, "Camada de busca"] |
| Controle de acesso por pasta | Gustavo vai desenvolver depois, fora deste projeto | — | — | — | — | [D, mapa, Out of scope] |

### 4.6 O que o Gustavo decide e o que o agente faz sem perguntar

[D, "Lições do vault"; "Maestri: padrão e liberdade"]
- **Pede aval:** mudar o contrato, os adaptadores (as ligações de cada ferramenta), exclusões ou reescritas grandes;
  no acervo, os casos da linha "Acervo do maestro" acima. O pedido de aval do acervo mostra numa tela o que muda
  (antes e depois), quem é afetado, se a mudança já roda como personalização em algum workspace, a alternativa de
  virar variante e a recomendação do verificador.
- **Não pede:** gravar no lugar certo, manter a nota de retomada, levar ao hub o que só a memória privada sabe, triar
  o que é ambíguo, promover, acrescentar peça ou variante nova sem sobreposição, resolver o que o hub junta sozinho.
- **Só para e avisa:** colisão real.
- **Colisão real:** quem resolve é o Gustavo, ou um agente com ele vendo [D, "Divergência…"; "Revisão do sync…"].

---

## 5. Pertencimento

### 5.1 Grupos lógicos

Um grupo diz **o que fica junto e por quê**. Uma coisa pode estar em mais de um grupo; aí a lista abaixo diz os dois.

| Grupo | Membros | Por que ficam juntos | Estado |
|---|---|---|---|
| **Núcleo de dados do par** | banco local, vista Markdown, sincronizador, regra de exclusão | guardam ou movem a mesma verdade dentro da máquina | [D, "Revisão do sync…"] |
| **Portas do par** | porta do banco, porta de leitura, camada de busca (com o índice), ponte do Desktop | por elas agentes, clientes e o Desktop alcançam o núcleo | [D, "Como a verdade viaja…"; "Onde o servidor mora"; "Camada de busca"] |
| **Vigilância** | vigia, avisos, mod de estado, checagem de sessão, comando de recuperar binário | garantem que nada diverge em silêncio | [D, "Revisão do sync…"; "Divergência…"] |
| **Disciplina do agente** | contrato, ligações da ferramenta, checagem de sessão, checkpoint, nota de retomada, guarda do acervo, verificador, hook de uso, lembrete do maestro | fazem o agente gravar no lugar certo, sem pedido | [D, "Contrato file-first…"; "Maestri: padrão e liberdade"] |
| **Conteúdo** | as seis raízes, iniciativas, núcleo e blocos, notas de retomada, acervo, propostas, registro de uso, skills, catálogo, segredos | é o que o banco guarda e a vista mostra | [D, glossário] |
| **Periferia do par** | Obsidian com o plugin e o assistente, cópia local e tarefa diária, nó da rede, credenciais, kit de par, script do `_archive/` | estão no par, mas não guardam nem movem a verdade do dia a dia | [D, "Revisão do sync…"]; [L] para kit, credenciais e script |
| **Ferramentas da máquina** | biblioteca e pastas de papel do Maestri, memória privada, configuração de cada ferramenta | são da ferramenta, não do hub; cada máquina tem as suas | [D, "Acesso dos agentes: pesquisa"; "Portas de entrada: pesquisa"] |
| **Fora do par** | rede privada, cópia no GitHub, clientes, vault, FreeLLMAPI, embeddings na nuvem, Tailscale da empresa | ficam fora das duas cópias | [D, idem] |
| **Quem chega** | Gustavo, agentes (com maestro, recrutas, subagentes), Claude Desktop, clientes | agem de fora dos grupos, pelas portas | [D, "Portas de entrada do hub"] |

**Pertence a mais de um grupo:**
- **Checagem de sessão:** vigilância (mostra o estado) e disciplina (abre a nota de retomada).
- **Nota de retomada:** conteúdo (é um arquivo da iniciativa) e disciplina (é o que o checkpoint cobra).
- **Acervo, skills, propostas, registro de uso:** conteúdo (moram em `agents/`) e disciplina (a guarda e os hooks
  cuidam deles).
- **Contrato:** conteúdo (é o `AGENTS.md` na raiz, replica como os outros) e disciplina (é a regra).
- **Camada de busca:** portas (é a entrada ao conteúdo); depende da vista do disco.
- **Obsidian:** periferia (pode fechar) e escritor do disco e do banco quando aberto.
- **Claude Desktop:** quem chega (é o Gustavo pedindo); roda **na** máquina, não fora dela.
- **Pasta de cliente:** raiz `clients/`; poderia também ser declarada não replicada (critério independente).

### 5.2 Lugares

Onde cada coisa existe de fato. Lugares se aninham: **a máquina (o par) contém** o disco, o banco, os processos, a
configuração do usuário, os apps e as sessões.

| Lugar | Dentro de | O que vive ali | Replica? | Estado |
|---|---|---|---|---|
| **Disco do par**, `C:\context-hub` | máquina | vista Markdown (todo o conteúdo), contrato, skills, acervo, índice da busca, `.git`, `.secrets/` | a vista sim, pelo banco; índice, `.git` e `.secrets/` não (têm ponto) | [D, "Revisão do sync…"; "Camada de busca"]; `.secrets/` [C] |
| **Banco local** | máquina | a verdade: notas, versões, conflitos, cifrados | sim, para o outro par | [D, "Como a verdade viaja…"] |
| **Processos do par** | máquina | banco, porta do banco, porta de leitura, camada de busca (servidor HTTP), ponte do Desktop | não | [D, "Onde o servidor mora"; "Camada de busca"]; em contêiner ou nativo [NV] |
| **Tarefas agendadas** | máquina | sincronizador, vigia, cópia diária | não | [D, "Revisão do sync…"] |
| **Configuração do usuário** (`~/.claude`, `~/.codex`, `~/.copilot`, `~/.agents/skills`) | máquina | ligações para o contrato e as skills, configuração de MCP, hooks, mod do Claude Code, memória privada | não; montada pelo kit de par | [D, "Acesso dos agentes: pesquisa"; "Portas de entrada do hub"]; hooks no escopo do usuário [C] |
| **Configuração do kit** | máquina | credenciais do par | não | [D, "Passagem para a construção"]; arquivo exato [NV] |
| **Perfil do Maestri** (`~/.maestri`) | máquina | biblioteca do Maestri: papéis e partituras | não | [D, "Portas de entrada: pesquisa"] |
| **Pasta do papel** (`.maestri/roles/<id>/`) | disco, na pasta do workspace | arquivos do papel | não (tem ponto) | [D, "Testes do papel do Maestri…"] |
| **Apps** | máquina | Obsidian com o plugin; Claude Desktop; Maestri | — | [D, "Portas de entrada do hub"] |
| **Sessão do agente** | máquina | o chat, o scratchpad, o raciocínio; os hooks rodam aqui, com o efeito na sessão | não: morrem com a sessão | [D, "Contrato file-first…"] |
| **Área de notificação do Windows** | máquina | a notificação da vigia | não | [D, "Revisão do sync…"] |
| **Rede privada** | fora | só o caminho entre pares e clientes | — | [D, "Onde o servidor mora"] |
| **GitHub** | fora | cópia diária da vista, um ramo por máquina | — | [D, "Revisão do sync…"] |
| **Máquina pessoal** | — | FreeLLMAPI (depois da construção) | — | [P, "Passagem para a construção"] |
| **Notebook** | — | vault `ai-operating-system` | — | [D, "Workloads piloto"] |

**Regra para desenhar um grupo que atravessa lugares** (a disciplina do agente mora no disco, na configuração e na
sessão): ou se desenha por **lugar**, e o grupo vira uma cor ou marca comum aos membros espalhados; ou se desenha por
**grupo**, e o lugar vira etiqueta de cada membro. Não se desenha o mesmo componente duas vezes.

**Hoje toda cópia de dado do hub mora nas duas máquinas e no GitHub.** Nada mora numa máquina só: o conteúdo de
cliente também vive nas duas, porque o Gustavo trabalha com cliente também na máquina pessoal [D, mapa, Out of
scope; P, "Arquitetura de pastas…"]. O perfil de cada máquina é um arquivo por máquina em `agents/machines/` [C,
"Arquitetura de pastas…"]; o que ele contém [A, mapa, Not yet specified].

---

## 6. Ligações

Quem fala com quem, o que passa e quando.

| De | Para | O que passa | Quando | Estado |
|---|---|---|---|---|
| Disco (vista) | Sincronizador ↔ banco local | mudanças de arquivo, nos dois sentidos | sempre que a máquina está ligada e logada; ~2 s medido com um banco só | [D, "Revisão do sync…"; "Teste: disco e banco…"] |
| Disco (vista) | Plugin ↔ banco local | o mesmo, quando o Obsidian está aberto | só com o Obsidian aberto | [D, "Revisão do sync…"] |
| Banco local do par A | Banco local do par B | as mudanças do próprio par (cada par envia as suas) | contínuo, com os dois ligados, pela rede privada; tempo pela rede [NV] | [D, idem] |
| Agente | Porta do banco → banco local | leitura com versão; gravação com a versão lida | a cada leitura e gravação | [D, "Como a verdade viaja…"]; guarda de versão a construir |
| Porta do banco → banco | Vista Markdown | a gravação chega ao `.md` em ~0,2 s | logo depois de gravar | [D, "Spike: CouchDB e LiveSync"] |
| Agente | Disco, direto | edição do `.md`; o sincronizador leva ao banco, sem conferir a versão | quando o agente edita o arquivo | permitido pelo critério 3 [D, mapa]; como confere a versão [A, "Como os agentes gravam no hub"] |
| Agente | Camada de busca | pergunta → trecho certo | a cada busca | [D, "Camada de busca"] |
| Camada de busca | Vista (disco) | indexa os arquivos | quando o disco muda; tempo [NV] | [D, idem] |
| Cliente | Porta de leitura de um par | consultas por HTTP com token | quando o cliente pede | [D, "Onde o servidor mora"] |
| Cliente | Camada de busca de um par | buscas pela rede | quando o cliente pede | servida na rede [D, "Camada de busca"]; regra de rede [A] |
| Claude Desktop | Ponte → porta do banco | leitura | quando pede | [D, "Portas de entrada do hub"] |
| Outra máquina | Pasta não replicada | leitura por SSH | quando houver a primeira pasta | [D, glossário; "Ligar as máquinas com segurança"]; montado só quando surgir o caso [D, mapa, Out of scope] |
| Agente | Guarda do acervo → acervo | gravação liberada, recusada ou com aval (Claude Code); recusa e proposta (Codex, Copilot) | a cada tentativa de alterar uma peça | [D, "Maestri: padrão e liberdade"] |
| Codex, Copilot | Propostas → maestro no Claude Code | a mudança proposta | quando um maestro avalia | [D, idem] |
| Hook de uso | Registro de uso | quem usou qual peça | quando uma peça é usada | [D, idem] |
| Maestro | Biblioteca do Maestri | cria o papel global se falta; reescreve se difere do acervo; leva a versão local | na hora de usar um papel | [D, idem] |
| Vigia | Banco, sincronizador, plugin | lê o estado | a cada 5 min | [D, "Revisão do sync…"] |
| Vigia | Avisos, mod de estado | aviso de divergência | quando piora (notificação); sempre (mod) | [D, idem] |
| Estado curto e nota de retomada | Checagem de sessão | situação do sync e onde o trabalho parou | no início de toda sessão | [D, "Contrato file-first…"] |
| Checkpoint | Agente → nota de retomada | a obrigação de gravar o que a resposta mudou e o que só a memória privada sabe | ao fim de cada resposta | [D, idem] |
| Tarefa diária | Cópia no GitHub | commit e push da vista | uma vez por dia | [D, "Revisão do sync…"] |
| Contrato e skills | Configuração de cada ferramenta | import, link simbólico, junction | fixo, montado pelo kit de par | [D, "Portas de entrada do hub"] |
| Agentes (notebook) | FreeLLMAPI (máquina pessoal) | tarefas simples, pelo roteamento | quando o contrato-opção manda | [D, "Maestri: padrão e liberdade"; P, "Passagem para a construção"] |
| Camada de busca | Embeddings na nuvem | texto indexado | só se o Gustavo ligar | [D, "Camada de busca"] |

---

## 7. Ações práticas

O que cada ator faz no dia a dia, nas palavras dele, e o caminho técnico que a ação dispara. O cenário completo, com
falhas, está na seção 8.

### 7.1 O Gustavo

| Ele diz ou faz | O que acontece por baixo | Cenário |
|---|---|---|
| "Edito a nota no Obsidian" | o Obsidian grava o `.md`; o plugin ou o sincronizador (o primeiro que vir) leva ao banco; o banco envia ao outro par | 8.1 |
| "Edito o arquivo no Explorador, no VS Code, num editor qualquer" | o sincronizador pega a mudança no disco e leva ao banco | 8.2 |
| "Crio uma nota nova" | igual a editar; a pasta onde ela nasce depende de onde ele cria | 8.1; pasta padrão [G, 3] |
| "Jogo uma ideia sem pasta certa" | vai para `inbox/`; o checkpoint faz a triagem | [D, glossário; "Lições do vault"] |
| "Peço ao agente: leia, altere, remova" | o agente busca, lê pela porta do banco, grava levando a versão | 8.5 a 8.7 |
| "Apago uma pasta no Explorador" | o sincronizador apaga no banco; a exclusão viaja | 8.7 |
| "Resolvo um conflito" | a janela de conflito do plugin, com o Obsidian aberto | 8.12 |
| "Mudo de máquina no meio da tarefa" | a nota de retomada chega pela troca entre bancos | 8.14 |
| "Peço algo pelo Claude Desktop" | o Desktop lê pela ponte; gravar está em aberto | 8.17 |
| "Copio algo do vault antigo" | a cópia nasce no hub e passa a ser a casa; o vault não muda | [D, "Workloads piloto"] |
| "Termino uma iniciativa" | a pasta vai para o `_archive/` pelo script | quem roda [G, 4] |
| "Ligo os embeddings do Google" | o índice ao lado do arctic passa a ser usado; o texto indexado vai ao Google | [D, "Camada de busca"] |
| "Monto uma máquina nova" | roda o kit de par (ver 8.11) | 8.11 |
| "Crio uma partitura no Maestri e peço para guardar" | o maestro escreve a receita de comandos e guarda a partitura junto, no acervo | [D, "Maestri: padrão e liberdade"] |
| "Recupero algo apagado" | texto: pega a versão da cópia no GitHub (do último dia) ou, antes da compactação, a versão antiga no banco; binário de colisão: o comando de recuperar | 8.7; procedimento e quem o roda [G, 16] |
| "Respondo uma rodada" | no portal; o resto vai pelo terminal e o maestro avisa em uma linha | seção 12 |

### 7.2 Um agente de código

| O agente faz | O que acontece por baixo | Cenário |
|---|---|---|
| Abre uma sessão | o contrato chega; a checagem de sessão mostra o estado do sync e abre a nota de retomada | 8.3 |
| Procura algo | pergunta à camada de busca da máquina dele; recebe o trecho, não o arquivo | 8.9 |
| Lê uma nota | pela porta do banco, recebendo a versão; se a nota está em conflito, a porta diz (a construir) | 8.5 |
| Grava | pela porta do banco, levando a versão lida; se mudou, vira conflito visível e ele relê e refaz (a construir) | 8.6 |
| Grava direto no disco | o sincronizador leva ao banco; a versão não é conferida | 8.2 |
| Termina uma resposta | o checkpoint confere a nota e a memória privada; se falta algo, o agente continua e grava | 8.3 |
| Toma uma decisão | grava em `decisions.md` e na nota de retomada (linha e ponteiro); o chat não basta, porque morre com a sessão | [D, "Contrato file-first…"]; arquivo [C] |
| Não sabe em que pasta gravar | segue o contrato e o catálogo de blocos; o que não cabe vai para `other/` | [C, "Arquitetura de pastas…"] |
| Tenta alterar uma peça do acervo | passa pela guarda | 8.4 |
| Acha que o contrato está desatualizado | edita só dentro do hub, nunca pelo link (gravar pelo link com ferramenta que cria arquivo novo troca o link por uma cópia); mudar pede aval | [D, "Testes da porta do repositório…"; "Lições do vault"] |

### 7.3 O maestro

| O maestro faz | O que acontece por baixo | Estado |
|---|---|---|
| Abre a sessão | o contrato e o lembrete o mandam começar pela skill `maestro-acervo` | [D, "Maestri: padrão e liberdade"] |
| Monta um workspace | escolhe um setup (receita de comandos que ele executa; cita papéis pelo nome, sem copiar o prompt), ou uma variante; confere cada papel da biblioteca do Maestri contra o acervo, cria o que falta e reescreve o que difere | [D, idem] |
| Quer aplicar uma partitura | não consegue pela linha de comando: aplicar partitura exige a interface do Maestri ou a API Wire; por isso o setup é receita de comandos | [D, "Acervo do maestro: pesquisa"] |
| Ajusta um papel para uma iniciativa | cria uma versão local em `maestro/`; é ela que vai para a biblioteca daquele workspace; ajuste de papel em uso só pelo prompt | [D, "Maestri: padrão e liberdade"] |
| Acrescenta peça ou variante | grava sozinho | [D, idem] |
| Altera ou apaga peça usada | pede aval, com a tela da seção 4.6 | [D, idem] |
| Avalia propostas | lê `agents/maestro/propostas/` (no Claude Code) | [D, idem] |
| Chama um subagente | o subagente roda dentro dele, sem ocupar terminal | [D, "Acervo do maestro: pesquisa"] |
| Recruta um agente | o Maestri abre um terminal com papel na pasta do workspace | [D, "Testes do papel do Maestri…"] |
| Pede um visual | pede ao Designer; o maestro nunca edita o visual direto | [D, mapa, Notes] |

### 7.4 Os outros

| Ator | Faz | Caminho | Estado |
|---|---|---|---|
| Outro par | altera uma nota | o banco dele envia; o meu recebe; o meu sincronizador escreve no disco; a minha busca reindexa | 8.8 |
| Cliente | consulta | rede privada → porta de leitura (ou busca) de um par → resposta; quem está no cliente só vê o que o agente dele mostra | 8.10 |
| Agendador | dispara | sincronizador no logon e a cada minuto; vigia a cada 5 min; cópia uma vez por dia | [D, "Revisão do sync…"; "Teste: disco e banco…"] |

---

## 8. Cenários

Do gatilho ao fim, com as falhas no caminho. "Máquina A" é onde a ação nasce; "máquina B", o outro par.

### 8.1 O Gustavo edita uma nota no Obsidian

1. Ele abre a nota no Obsidian da máquina A. O que ele vê é o `.md` do disco [D, glossário].
2. Ele edita; o Obsidian grava o `.md`.
3. O plugin (Obsidian aberto) ou o sincronizador leva a mudança ao banco local; os dois são escritores e, juntos, não
   criam ciclo [D, "Revisão do sync…"; "Teste: disco e banco…"].
4. O banco de A envia a mudança ao banco de B pela rede privada.
5. O sincronizador de B escreve no disco de B; a vista de B atualiza; a busca de B reindexa.

Falhas:
- **B desligada:** a mudança espera no banco de A e viaja quando B ligar. Não é divergência; a checagem de sessão em A
  só informa a hora da última troca [D, "Revisão do sync…"].
- **O mesmo trecho mudou em B antes da troca** (por qualquer origem: Obsidian, agente, disco): colisão real (8.12).
- **Trechos diferentes mudaram nas duas:** juntam-se sozinhos, **se a versão comum ainda está no banco**. Se a
  compactação já a apagou, vira colisão real [D, "Revisão do sync…"; glossário].
- **O assistente do plugin abriu e ninguém respondeu:** o plugin para; o sincronizador continua; a vigia avisa [D,
  "Teste: disco e banco…"; "Revisão do sync…"].
- **O Obsidian travou ou a máquina reiniciou:** o que já foi gravado no disco o sincronizador leva; o que não chegou ao
  disco [NV].
- **Um agente grava a mesma nota na mesma máquina ao mesmo tempo:** a edição do Gustavo no Obsidian não tem proteção
  contra a do agente no mesmo arquivo; fora do escopo [D, mapa, Out of scope]. Se o agente grava pela porta do banco e
  a edição do Gustavo chegou antes ao banco, a gravação do agente vira conflito visível, quando a guarda existir (8.6).
  Se os dois gravam no disco, a última gravação vence, sem conferência [D, "Revisão do sync…"]; se a edição do
  Gustavo se perde nesse caso [NV].

### 8.2 Alguém edita o arquivo direto no disco (agente, Explorador, editor)

1. O arquivo muda no disco da máquina A, com o Obsidian aberto ou fechado.
2. O sincronizador pega a mudança (~2 s) e leva ao banco local [D, "Teste: disco e banco…"].
3. Daí em diante, como 8.1, passos 4 e 5.

Falhas e limites:
- **Não há conferência de versão** nessa gravação: se outro escritor mudou o arquivo no meio, a última gravação vence no
  disco [D, "Revisão do sync…"]. Como o agente confere a versão no disco, e se ele deve gravar no disco [A, "Como os
  agentes gravam no hub"].
- **Arquivo acima de 200 MiB:** não vai ao banco; fica só em A; a vigia lista (8.13).
- **Arquivo ou pasta com ponto:** ver 8.16.
- **Sincronizador parado:** a mudança fica só no disco; a vigia percebe em até 5 min (8.13).
- **Banco local caiu no meio:** o sincronizador sobrevive e leva a mudança quando o banco volta; uma cópia de 40 MiB
  subiu inteira no teste [D, "Teste: disco e banco…"].

### 8.3 Um agente novo abre uma sessão

1. O Gustavo (ou o Maestri) abre o harness numa porta de entrada; a principal é a raiz do hub.
2. **O contrato chega**, conforme a ferramenta e a porta (tabela em 3.1 e 3.4). Dentro de um papel do Maestri
   [D, "Testes do papel do Maestri…"; "Acesso dos agentes: pesquisa"; "Portas de entrada: pesquisa"]:
   - o Maestri grava na pasta do papel um `CLAUDE.md` e um `AGENTS.md` com o prompt do papel; isso esconde o
     `AGENTS.md` do workspace;
   - **Claude Code** recebe o contrato do hub pela configuração global e pelo `claude-md-and-agents-md`;
   - **Copilot** lê o papel e a iniciativa, não a raiz; o contrato da raiz chega pelo arquivo global;
   - **Codex** só lê o arquivo do papel, a menos que ache a raiz (marcador no teste; `.git` da raiz em curso).
3. **A checagem de início de sessão** lê o estado da vigia, informa a hora da última troca e abre a nota de retomada
   [D, "Contrato file-first…"].
4. **Qual nota:** a pasta onde a sessão abre diz qual é o trabalho. **Na raiz, a pasta não diz**: o agente acha a nota
   pela busca, pelo nome que o Gustavo der, ou pergunta. Não adivinha [D, idem].
5. O agente trabalha: busca (8.9), lê (8.5), grava (8.6).
6. Ao fim de cada resposta, o checkpoint confere a nota e a memória privada; se falta, o agente continua e grava
   [D, idem]. A nota é gravada **antes** de a resposta terminar, porque o hook faz o agente continuar [L].

Falhas e limites:
- **Um `CLAUDE.md` em qualquer pasta acima do hub** desliga todos os `AGENTS.md` no Claude Code; o kit de par confere
  [D, "Testes das portas de entrada"; "Portas de entrada do hub"].
- **Contrato chega, mas o agente não obedece:** medido em teste; o hub não tem mecanismo que pegue isso. A verificação
  dos cinco critérios precisa medir [D, "Portas de entrada do hub"; "Testes da porta do repositório…"].
- **Contrato longo:** pela sessão, o Claude Code carrega o arquivo; o Codex soma até 32 KiB. Pelas instruções do MCP
  (clientes), o Claude Code corta perto de 2.048 caracteres; por isso a cabeça do contrato é autossuficiente em até
  2.000 [D, "Acesso dos agentes: pesquisa"; "Portas de entrada do hub"].
- **O checkpoint não vê** o que foi dito no meio de uma resposta longa e não roda quando o Gustavo interrompe; só a
  regra cobre esses furos, e cabe ao agente atualizar a nota por conta própria [D, "Contrato file-first…"].
- **Hook que falha sem aviso:** nada decidido pega isso [A].
- **Copilot com `COPILOT_HOME` definido:** deixa de ler `~/.agents/skills` [D, "Acesso dos agentes: Copilot"].
- **Busca fora do ar:** o agente ainda acha a nota pela pasta (`retomada.md`) ou pelo nome [D; C].
- **Troca de modelo ou `/clear`:** o chat e o raciocínio morrem; continua só o que está no hub [D, "Contrato
  file-first…"]. A memória privada não basta porque é de uma ferramenta numa máquina [L].
- **Política da empresa:** pode bloquear o MCP do hub; nos testes, a conta da empresa não bloqueou no VS Code nem na
  linha de comando [C, "Acesso dos agentes: decisão"; D, "Copilot com assinatura Enterprise"].

### 8.4 Um maestro novo

1. Uma sessão do Maestri abre (workspace de iniciativa na pasta dela; o que cruza iniciativas, na raiz) [D, "Maestri:
   padrão e liberdade"].
2. O contrato manda o maestro começar pela skill `maestro-acervo`; o lembrete de início reforça [D, idem].
3. O maestro lê o catálogo e escolhe as peças: setup (ou variante), papéis, contratos-opção (roteamento de modelos,
   orquestração, onde abrir). São opções; ele pode recusar [D, idem].
4. Antes de usar um papel, confere a cópia da biblioteca do Maestri contra o acervo; cria o papel global se faltar e
   reescreve se diferir; se há versão local na iniciativa, é ela que vai para a biblioteca do workspace [D, idem].
5. Executa o setup como receita de comandos [D, "Acervo do maestro: pesquisa"].
6. O hook de uso registra cada peça usada no arquivo da máquina [D, "Maestri: padrão e liberdade"].
7. Se falta uma peça no catálogo, ele a cria; alterar ou apagar uma peça usada pede aval [D, idem].

Falhas e limites:
- **Editar o prompt de um papel** reescreve os arquivos do papel, apaga ajuste manual e reinicia todos os terminais com
  aquele papel. **Reiniciar o terminal não regrava** os arquivos do papel [D, "Testes do papel do Maestri…"].
- **Guarda instalada só na raiz do workspace** não alcança o papel; por isso ela fica no escopo do usuário [D, "Guarda
  do acervo: mods e hooks"].
- **Alteração no acervo pelo Claude Code:** recusa, verificador, relatório, aval. Cada hook tem 10 s; esperar o aval
  ou chamar um modelo não conta, esperar um subagente conta [D, idem]; tempo real do verificador [NV].
- **FreeLLMAPI fora do ar:** para onde o roteamento manda as tarefas simples [A].
- **Renomear a pasta de uma iniciativa** usada como casa de um workspace [NV].
- **Recrutas com o mesmo papel e pasta** dividem a pasta [D, "Testes do papel do Maestri…"].

### 8.5 Pedir a um agente para ler

1. O Gustavo pede ("o que diz a nota X?").
2. O agente acha o trecho pela busca da máquina dele, ou vai direto à nota [D, "Camada de busca"; "Lições do vault"].
3. Lê pela porta do banco, recebendo o texto e a versão [D, "Como a verdade viaja…"].
4. Se a nota está em conflito, a porta diz e o agente avisa o Gustavo. **A construir:** o MCP pronto devolve só a
   versão vencedora, sem aviso [D, "Spike: CouchDB e LiveSync"].

Falhas: **versão velha** — o agente lê o banco da máquina dele; se a outra mudou e ainda não trocou, ele lê a anterior.
O Gustavo percebe pela hora da última troca e pelo estado da vigia [D, "Revisão do sync…"]. **Busca desatualizada** —
ver 8.9.

### 8.6 Pedir a um agente para alterar

1. O Gustavo pede ("corrija o erro de digitação na nota X").
2. O agente lê a nota pela porta do banco e guarda a versão.
3. Grava levando a versão lida [D, "Como a verdade viaja…"].
4. Se a nota não mudou no meio: o banco aceita; a vista muda em ~0,2 s; o Obsidian aberto mostra [D, "Spike: CouchDB e
   LiveSync"].
5. Se mudou: a gravação vira **conflito visível**; o agente relê e refaz [D, "Divergência…"; "Como a verdade viaja…"].
6. O banco envia ao outro par (8.8).
7. Ao fim da resposta, o checkpoint confere a nota de retomada.

**A construir, e obrigatório antes de usar:** os passos 3 e 5. Hoje o MCP pronto aceita gravação com versão velha;
a versão do outro some do disco e fica no banco só até a compactação [D, "Spike: CouchDB e LiveSync"; "Como a verdade
viaja…"]. Dois agentes gravando **notas diferentes** não se atrapalham em nenhum caso [L].

Outras falhas: **agente grava no disco** em vez da porta: 8.2. **Mudar a regra geral do hub** (o contrato): pede aval
[D, "Lições do vault"].

### 8.7 Pedir a um agente para remover

1. O Gustavo pede ("remova a nota X" ou "apague a pasta Y").
2. Exclusão ou reescrita grande pede aval antes [D, "Lições do vault"].
3. O agente remove (pela porta do banco ou no disco).
4. A exclusão chega ao banco e viaja ao outro par em segundos.

Falhas e limites:
- **A outra máquina estava editando a nota:** "um lado apaga o que o outro mudou" é colisão real (8.12) [D, glossário].
- **Apagou sem querer:** a exclusão chega à outra máquina em segundos; não há lixeira no hub. A volta é a cópia no
  GitHub (do último dia) ou, para texto, a versão antiga no banco até a compactação, que não tem prazo fixo [D,
  "Revisão do sync…"; "Spike: CouchDB e LiveSync"]. O procedimento e quem o roda [G, 16].
- **Remover é apagar ou arquivar?** O que termina vai para o `_archive/` [D, glossário]; o que o Gustavo quer dizer
  com "remova" [G, 4]. Como algo volta do `_archive/` [A].
- **Mover ou renomear pasta com a outra máquina editando:** a edição fica separada, como conflito "editado × apagado";
  por isso o script do `_archive/` confere o outro par antes [D, "Testes das portas de entrada"; "Portas de entrada do
  hub"]. Renomear uma nota grava a nova e apaga a antiga; o Obsidian reescreve os links [D, "Portas de entrada:
  pesquisa"; "Testes das portas de entrada"].

### 8.8 O outro par altera uma nota

1. Algo muda no banco de B.
2. O banco de B envia a mudança ao banco de A pela rede privada [D, "Revisão do sync…"].
3. O sincronizador de A escreve no disco de A; a busca de A reindexa; o Obsidian de A, se aberto, mostra.
4. Se a mesma nota mudou em A no mesmo trecho: colisão real (8.12).

Falhas: **A desligada:** espera. **Rede caiu:** cada banco guarda o que mudou e envia quando volta [D, "Revisão do
sync…"]. **B parada por dias:** quando volta, cada banco envia o que acumulou; mesmo trecho dos dois lados vira colisão
[D, idem]. Ordem de chegada [NV]. **O banco de A foi apagado inteiro:** se a outra máquina restaura ou replica o
apagamento [NV]; a volta garantida é a cópia no GitHub.

### 8.9 Buscar

1. O agente pergunta à camada de busca da máquina dele, por MCP [D, "Camada de busca"].
2. A busca combina palavra (FTS5 do SQLite, um analisador só para português e inglês) e sentido (embedding arctic
   local) sobre a vista daquela máquina [D, idem].
3. Devolve trechos com o caminho; o agente abre só o que precisa.
4. Se vai alterar, grava pela porta do banco (8.6).

Limites [D, "Camada de busca"]:
- a busca não é feita pelo banco, porque o texto lá é cifrado;
- enxerga só o disco daquela máquina: nota da outra máquina ainda não trocada não aparece; pasta não replicada da outra
  máquina não aparece;
- continua com o Obsidian fechado, porque o sincronizador mantém o disco vivo [D, "Revisão do sync…"];
- enxerga o que está no disco, não o que ainda está só na tela;
- nota com YAML inválido fica fora do índice;
- funciona sem internet, porque o modelo padrão é local [L, "Modelos de embeddings…"]; sem a rede privada, só os
  clientes a perdem;
- se lê `.txt` e `.csv` [NV]; autenticação do servidor HTTP [NV]; tempo de uma edição até aparecer [NV];
- o que mais falha são sinônimos; quem resolve é o embedding;
- **máquina sem sincronizar há dias:** a busca mostra o que o disco tem, sem aviso próprio; o aviso vem da vigia e da
  checagem de sessão;
- a reserva: um índice dentro da porta do banco, guardado; volta se a busca precisar mostrar uma gravação em segundos
  ou se o índice do Google não rodar ao lado do arctic.

### 8.10 Um cliente consulta

1. O Gustavo dá ao sandbox ou máquina de passagem uma chave temporária com etiqueta; ele entra na rede privada [D,
   "Onde o servidor mora"].
2. Uma regra da rede só deixa essa etiqueta chegar à porta de leitura de um par [D, idem].
3. O agente do cliente consulta por HTTP com token; recebe o começo do contrato nas instruções do MCP [D, "Portas de
   entrada do hub"].
4. O par responde com o texto em claro do banco dele.

Limites e falhas:
- **Sem par ligado, o cliente não funciona** [D, glossário]. Com a máquina pessoal desligada, o cliente usa o notebook;
  um par segue funcionando sozinho, um cliente não.
- **Grava?** Por padrão, não: a porta de leitura recusa no próprio servidor. Liberar é decisão do Gustavo [D, "Onde o
  servidor mora"; "Testes das portas de entrada"].
- **Por que nunca a credencial do banco:** o modo só de leitura vale no MCP, não no banco; com a credencial, o cliente
  gravaria direto no banco [D, "Onde o servidor mora"]. Um token de cliente que vaza dá leitura, só de dentro da rede.
- **Depois de parar:** o nó temporário sai sozinho da rede de 30 a 60 min após a última atividade (no teste, mais de 35
  min) [D, "Portas de entrada: pesquisa"; "Testes das portas de entrada"]. Validade da chave [A].
- **Busca pelo cliente:** servida na rede; a regra que a libera à etiqueta [A].
- **Cliente que tenta um computador que não é par:** não há porta nele [L].
- **Proteção do próprio computador de passagem:** nenhuma fonte decide [A].
- **Claude no celular ou na web:** não alcança a rede privada [D, "Portas de entrada: pesquisa"].
- **Pastas com ponto** não estão no banco; o cliente não as vê.

### 8.11 Um par novo entra (ou uma máquina é remontada)

Ordem que as fontes dão [D, "Onde o servidor mora"; "Revisão do sync…"; "Teste: disco e banco…"; "Portas de entrada do
hub"]:
1. Rede privada no Windows (com o modo sem login na máquina pessoal).
2. Banco local e portas (kit de par).
3. Sincronizador, **antes** do plugin: na primeira partida ele refaz a base dos arquivos que não conhece, e o histórico
   comum se perde uma vez; subindo primeiro, isso acontece uma vez só.
4. O dispositivo novo é recusado até alguém confirmá-lo [D, "Teste: disco e banco…"]. Se o banco local aceita gravação
   antes disso, as fontes não dizem.
5. Plugin no Obsidian, por link de configuração copiado de um par que funciona; a frase-senha por outro canal.
6. Ligações das ferramentas (import, links simbólicos com o modo de desenvolvedor ligado, junctions), conferindo que não
   há `CLAUDE.md`.
7. O banco novo replica com o outro e recebe as notas com o histórico que ainda existe.

Ordem completa entre os passos 2 e 6 [A, "Passagem para a construção"]. O primeiro teste da construção é dois bancos
replicando; se falhar, a volta é um banco só numa máquina [D, "Onde o servidor mora"].

### 8.12 Uma colisão

**Colisão real:** o mesmo trecho mudou dos dois lados, um lado apagou o que o outro mudou, ou não existe mais a versão
comum. A colisão é **detectada por trecho** e **retém a nota inteira** [D, glossário; "Revisão do sync…"].

Texto (`.md`, `.txt`, `.csv`):
1. A troca entre os bancos traz as duas versões, em qualquer ordem; o banco guarda as duas [D, "Spike: CouchDB e
   LiveSync"].
2. Só aquela nota fica retida; o resto continua viajando [D, "Revisão do sync…"].
3. **O disco de cada máquina segue com a versão local** daquela nota: o plugin segura a descida da outra até a
   resolução [D, "Spike: CouchDB e LiveSync"]. A busca de cada máquina indexa a versão local [L].
4. Com o Obsidian aberto, a janela de conflito abre, com faixa na nota e contador, nas duas máquinas [D, idem].
5. Com o Obsidian fechado, a vigia acha o conflito e avisa (notificação, estado na tela, checagem de sessão) [D,
   "Revisão do sync…"].
6. A porta do banco mostra ao agente que a nota está em conflito (a construir) [D, "Como a verdade viaja…"].
7. O Gustavo resolve, ou um agente com ele vendo. Até chegar a tela de três vias editável, ele escolhe uma versão e
   reedita; "juntar as duas" do plugin mutila o texto [D, "Como a verdade viaja…"].
8. A resolução é uma gravação normal: vai ao banco, viaja ao outro par, desce ao disco, a busca reindexa; o aviso some
   nas duas máquinas e a vigia limpa o estado [D, "Spike: CouchDB e LiveSync"; L para o caminho].

Binário (`.docx`, `.xlsx`, imagem, PDF…):
1. O hub fica sozinho com a versão de data mais nova, sem perguntar [D, "Revisão do sync…"].
2. A perdida fica guardada; a vigia a acha e avisa.
3. O comando de recuperar põe a versão perdida num arquivo ao lado [D, idem].

Limites: conflito aberto conta como divergência até ser resolvido; enquanto isso, as outras notas viajam [D, idem].

### 8.13 Uma máquina desligada, parada ou travada

| Situação | O que o hub faz | Estado |
|---|---|---|
| A outra máquina desligada | não é divergência; as mudanças esperam no banco local e viajam quando ela ligar; a checagem de sessão informa a hora da última troca | [D, "Revisão do sync…"] |
| Esta máquina não consegue enviar há mais de 15 min, com a outra ligada | é divergência; o aviso nasce **só nesta máquina**, a que travou; a outra não recebe aviso próprio | [D, idem; "Onde o servidor mora"] |
| O sincronizador parou | a vigia vê em até 5 min; volta sozinho em até 1 min pela repetição agendada | [D, idem; "Teste: disco e banco…"] |
| O banco local caiu | o sincronizador sobrevive; o que mudou durante a queda chega sozinho na volta | [D, "Teste: disco e banco…"] |
| O Windows desliga à noite | tudo para com ela; volta no logon | [D, "Revisão do sync…"] |
| O notebook fecha no meio de uma troca | o que já está no banco local fica; viaja quando voltar | [NV] |
| Uma máquina fica dias parada | ao voltar, cada banco envia o que acumulou; mesmo trecho dos dois lados vira colisão | [D, idem] |
| Só o notebook ligado | continua editando, buscando e gravando; guarda tudo para enviar depois; fica sem o FreeLLMAPI | [D, "Revisão do sync…"; P, "Passagem para a construção"] |
| Um arquivo acima de 200 MiB | não viaja; a vigia lista; conta como divergência enquanto existir acima do limite | [D, "Revisão do sync…"] |
| A vigia parou | ninguém decidiu quem percebe nem quem religa | [A] |
| A notificação passou despercebida | o estado curto fica gravado; a checagem de sessão o mostra; o mod mostra o tempo todo | [D, idem] |
| A chave do nó na rede privada vence (180 dias) | a máquina sai da rede privada e para de trocar; a outra continua; a vigia da máquina vencida vê a troca parada | prazo [D, "Ligar as máquinas com segurança"]; o resto [L] |
| A empresa bloqueia o Tailscale no notebook | o notebook para de trocar; o comportamento não foi tratado | risco [D, "Ligar as máquinas com segurança"]; [A] |

### 8.14 O Gustavo muda de máquina no meio da tarefa

1. Na máquina A, o checkpoint mantém a nota de retomada em dia.
2. A nota viaja ao banco de B como qualquer nota (tempo pela rede [NV]).
3. Na máquina B, a sessão nova abre na pasta do trabalho; a checagem de sessão abre a nota e informa a hora da última
   troca [D, "Contrato file-first…"].

Falha: se A não enviou ainda, B vê a nota velha, e a hora da última troca diz isso.

### 8.15 A cópia diária

1. Uma vez por dia, a tarefa de cada máquina faz commit da vista no `.git` da raiz e push para o ramo da máquina no
   GitHub [D, "Revisão do sync…"].
2. O git nunca puxa nem faz checkout; não escreve no disco do hub [D, idem].
3. Cada máquina usa a própria chave de escrita, só desse repositório; a chave não expira e pode ser revogada numa
   máquina sem afetar a outra; commits sem assinatura (pode entrar depois sem refazer nada) [D, "Ponto de encontro do
   sync"].

**Por que não é o sync:** a troca entre bancos leva um estrago às duas máquinas em segundos, e a compactação apaga o
histórico; o GitHub guarda um dia de distância [D, "Revisão do sync…"].

Limites: a cópia leva toda a vista, inclusive o conteúdo de cliente [L, "Revisão do sync…"; G, 6]. O GitHub guarda o
que a vista tem; a outra máquina recebe o que o banco tem: os dois diferem nas pastas com ponto aninhadas que vazaram
ao banco (8.16) e no que mudou desde a última cópia [L]. Uma chave que vaza dá leitura e escrita nesse repositório; não
chega aos bancos. **O hub não é um sistema de backup**: a cópia diária é uma rede de segurança, não versão por versão.

### 8.16 Um segredo cai no hub

1. Um agente cola uma senha numa nota comum: ela vai ao banco, ao outro par e à cópia no GitHub. **Nada decidido
   impede isso** [A].
2. Um arquivo com ponto (`.env`) na raiz de uma pasta: a regra de exclusão precisa cobrir arquivos com ponto; está
   anotada para a construção, sem teste [D, "Passagem para a construção"].
3. Uma pasta com ponto (`.secrets/`): **defeito medido**: na varredura de partida do sincronizador, pastas com ponto
   **aninhadas** (por exemplo `projeto/.venv`) foram ao banco e o plugin as gravou na outra máquina; só as do primeiro
   nível ficaram fora [D, "Teste: disco e banco…"]. Por isso, antes de guardar o primeiro segredo, um teste tem de provar
   que um `.secrets/` aninhado não chega ao banco nem ao GitHub [C, "Arquitetura de pastas…"]. **Até esse teste, um
   segredo em pasta com ponto aninhada não está protegido.**
4. Senhas de contas que acessam ambiente de cliente ficam no KeePass, fora do hub [C, idem].
5. Se o log do sincronizador guarda trecho de nota [NV].

### 8.17 O Gustavo pede algo pelo Claude Desktop

1. O Desktop chega à porta do banco pela ponte `mcp-remote` [D, "Portas de entrada do hub"].
2. Lê. Não recebe o contrato por arquivo nem as instruções do MCP [D, "Testes das portas de entrada"].
3. Gravar: o Gustavo disse que ele não deve ser proibido de escrever no hub; se grava pela pasta conectada (disco) ou
   pela porta do banco com a guarda de versão [A, "Como os agentes gravam no hub"]. O conector remoto não serve: parte
   dos servidores da Anthropic e não alcança a rede privada [D, "Portas de entrada: pesquisa"].
4. Se a conexão cai no meio de uma gravação [NV].

---

## 9. O que o hub não é e não faz

| Afirmação | Estado |
|---|---|
| Não é um repositório git comum: a verdade está num banco; o git só guarda uma cópia diária | [D, "Revisão do sync…"] |
| Não é um sistema de backup | [D, idem] |
| Não junta binários: na colisão fica o mais novo | [D, idem] |
| Não apaga nada por idade: o que envelhece é compactado ou arquivado | [D, "Lições do vault"] |
| Não protege a edição do Gustavo no Obsidian contra um agente no mesmo arquivo | [D, mapa, Out of scope] |
| Não controla acesso por pasta (o Gustavo desenvolve depois, fora deste projeto) | [D, mapa, Out of scope] |
| Não grava nada no vault antigo | [D, "Workloads piloto"] |
| Não controla como ferramentas e modelos trabalham: é um segundo mapa | [D, mapa, Out of scope] |
| Não serve à internet: tudo só pela rede privada, nunca o Funnel | [D, "Onde o servidor mora"] |
| Não usa o FreeLLMAPI no checkpoint nem faz revisão depois da sessão | [D, "Contrato file-first…"] |
| Não usa WSL | [D, "Windows ou WSL"] |
| Não tem `CLAUDE.md` | [D, "Portas de entrada do hub"] |
| Não tem operação remota nem SSH por ora | [D, mapa, Out of scope] |
| A busca não grava | [D, "Camada de busca"] |

---

## 10. Segurança e dado de cliente

| Afirmação | Estado |
|---|---|
| Tudo só pela rede privada; nunca exposto à internet, nunca o Funnel | [D, "Onde o servidor mora"] |
| Quatro proteções diferentes: a **senha do banco** (CouchDB), a **cifra de ponta a ponta** (frase-senha), o **token** de cada porta, e link de configuração e frase-senha por **canais separados** | [D, idem] |
| Cada par guarda a cópia completa e a frase-senha; o conteúdo abre em qualquer par que a tenha; a regra de dado de cliente vale igual nos dois | [D, idem; mapa, Out of scope]; como a frase-senha fica guardada e se recupera [NV] |
| Link de configuração e frase-senha pelo mesmo canal: quem pegar os dois monta um par com o hub inteiro | [L, "Onde o servidor mora"] |
| O banco guarda texto cifrado; quem lê em claro é quem tem a frase-senha: os pares, a porta do banco e a porta de leitura (que entrega texto em claro ao cliente) | [D, "Onde o servidor mora"; "Spike: CouchDB e LiveSync"] |
| Se a cifra esconde também os nomes dos arquivos | [NV] |
| Cliente: chave temporária, etiqueta, só a porta de leitura; nunca a credencial do banco | [D, "Onde o servidor mora"] |
| Cópia no GitHub: repositório privado; leva toda a vista | [D, "Revisão do sync…"]; com dado de cliente [G, 6]; quem lê além do Gustavo [NV] |
| Notas e tickets citam a iniciativa de cliente pelo nome; dados pessoais ficam nas pastas de origem | [D, mapa, Notes] |
| O que o agente lê vai ao provedor do modelo que ele usa; regra para dado de cliente com modelos na nuvem | [G, 6] |
| Embeddings: o padrão é local; o do Google, desligado, mandaria o texto indexado ao Google | [D, "Camada de busca"] |
| Política da empresa pode bloquear o MCP do hub; no teste não bloqueou | [C, "Acesso dos agentes: decisão"]; risco [D, "Copilot com assinatura Enterprise"] |
| Segredos: ver 8.16 | — |
| Quem revoga a chave de uma máquina devolvida ou vendida | [G, 11] |

---

## 11. O que ainda não está decidido

Tudo abaixo é proposta, pesquisa em curso ou lacuna. Um diagrama que mostrar estes itens deve marcá-los "a decidir" ou
"não verificado".

| Assunto | Situação | Onde |
|---|---|---|
| A guarda de versão e o aviso de conflito na porta do banco | decididos, **a construir**, obrigatórios antes de usar | "Como a verdade viaja…" |
| Como os agentes gravam: disco, porta do banco ou os dois; conferência de versão no disco; se o Claude Desktop grava e por onde | aberto | "Como os agentes gravam no hub" |
| A busca e a porta do banco num endereço só | aberto | "Acesso dos agentes: decisão" |
| Fim de resposta e início de sessão no Codex; estado da vigia na tela do Codex; `.git` no lugar do marcador | em investigação ou em curso | idem |
| Pendências com a conta da empresa: se o `mcp.json` do VS Code aceita o token por variável de ambiente; a consulta de política do Copilot de linha de comando, que estourou o tempo | não verificado | idem |
| Árvore dentro da iniciativa e ficha | rodadas respondidas, ticket aberto | "Arquitetura de pastas e frontmatter" |
| Índices (`index.md`) e busca; onde mora o texto extraído de docx, pdf, xlsx | espera a busca, agora decidida | idem |
| Pasta não replicada: mecanismo | aberto; hoje não há nenhuma | idem; mapa |
| Exclusão de pastas e arquivos com ponto em todos os níveis | defeito medido; teste antes do primeiro segredo | "Teste: disco e banco…"; "Arquitetura de pastas…" |
| Roteamento de skills | aberto | "Roteamento de skills" |
| Ordem completa de montagem de um par | trechos decididos; ordem completa não | "Passagem para a construção" |
| Perfil por máquina | não especificado | mapa |
| O Obsidian do hub ao lado do cofre do vault | não especificado | mapa |
| A passagem da prova de conceito ao hub real | aberto | "Passagem para a construção" |
| Usos do FreeLLMAPI além de embeddings; destino quando ele cai | não especificado | mapa |
| Gatilho para ligar os embeddings do Google | Gustavo liga; gatilho não definido | "Camada de busca" |
| Tela de colisão com três vias editável | decidida para logo depois da construção | "Como a verdade viaja…" |
| Lacunas sem dono: quem percebe a vigia parada e quem a religa; quem percebe um hook que falha; regra de rede da busca para clientes; o que impede segredo em nota comum; o que detecta o Funnel ligado; comportamento se a empresa bloquear o Tailscale; procedimento de recuperar texto apagado; como algo volta do `_archive/`; onde fica o registro do aval do contrato; validade da chave do cliente; proteção do computador de passagem | lacuna | — |
| **Não verificado:** duas instâncias da porta do banco por par em produção; arquivos entre 50 e 200 MiB; guarda do acervo em detalhe; autenticação, `.txt` e `.csv` e segundo índice na busca; tempo de edição até a busca; tempo da troca pela rede; ordem de chegada depois de um corte; o que o plugin perde se o Obsidian trava; nomes de arquivo sob a cifra; onde fica o estado curto da vigia | conferir na construção | vários |

**Fundo que não vale mais:** a exploração (§7.1, §9) falava em Markdown como fonte da verdade, hub hospedado numa
máquina e git como sync; as zonas por ciclo de vida (canônica, trabalho, efêmera, derivada) eram desse desenho e não
foram fixadas. O GitHub como ponto de encontro, o sincronizador por git e "colisão para a máquina inteira" saíram. A
divergência por "30 min sem sync" virou 15 min ("Revisão do sync…").

---

## 12. O que não é o hub (e aparece perto dele)

| Coisa | O que é | Relação com o hub | Estado |
|---|---|---|---|
| Biblioteca do Maestri | papéis e partituras no perfil do Maestri (`~/.maestri`), uma por máquina | o acervo é a fonte; o maestro confere e atualiza a biblioteca ao usar um papel; a versão local de um papel vai para a biblioteca daquele workspace | [D, "Maestri: padrão e liberdade"] |
| Skills `maestri-*` | skills que o app Maestri instala e regrava | o acervo usa outro prefixo (`maestro-*`) para não colidir | [D, "Acervo do maestro: pesquisa"] |
| Portal do projeto (rodadas, caixa, cartas, página Laços) | a ferramenta desta frente para o Gustavo decidir: decisão só no portal, com a explicação na rodada; rodada respondida nunca é reescrita, vira rodada nova; o terminal leva o resto e avisa em uma linha; o portal avisa o maestro; o maestro absorve a resposta no ticket | ferramenta da frente que constrói o hub; virar peça do acervo é futuro | [D, mapa, Notes]; como peça [A, mapa, Not yet specified] |
| Visuais (página do system design e outros) | feitos pelo Designer, a pedido do maestro; o maestro só pede, nunca edita direto. A página do system design só muda quando um ticket que mexe no desenho é resolvido | ferramenta da frente | [D, mapa, Notes] |
| Mapa e tickets desta frente | o planejamento do hub; o Gustavo é o dono das decisões | vivem hoje no repositório da prova de conceito; a frente nasce no hub quando ele existir | [D, mapa, Notes; "Workloads piloto"] |
| Vault `ai-operating-system` | a casa antiga | só referência | [D, "Workloads piloto"] |
| Repositórios de código | código de produto | moram fora do hub; recebem o contrato pela configuração global | [D, "Revisão do sync…"; "Portas de entrada do hub"] |
