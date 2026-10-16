# Descrição de design do context hub

Versão 1, 2026-10-15, escrita pelo Tech lead do laço do system design. Substitui o `texto-do-hub.md` como fonte de
todo diagrama. É um modelo em sete eixos: **atores, componentes, responsabilidade, pertencimento, ações práticas,
cenários e estado de cada afirmação**. Serve a quem nunca viu o hub e a qualquer modelo.

## 0. Como ler

**Estado de cada afirmação.** Toda linha leva uma marca entre colchetes:

| Marca | Quer dizer | Fonte |
|---|---|---|
| **[D]** | Decidido, ou fato medido num ticket resolvido | título do ticket entre aspas, ou "mapa" |
| **[C]** | Em curso: o Gustavo já respondeu a rodada, mas o ticket ainda não fechou. Pode mudar. | ticket aberto |
| **[P]** | Prática: o que o Gustavo faz ou disse que faz | onde ele disse |
| **[A]** | A decidir: ninguém decidiu ainda | ticket aberto ou "não especificado" do mapa |
| **[G]** | A decidir com o Gustavo: só ele sabe; está em `perguntas-ao-gustavo.md` | número da pergunta |
| **[NV]** | Não verificado: dito por inferência ou documentação, sem teste | onde aparece |

Quando a fonte é a mesma de toda a linha, ela vem uma vez só. "Mapa" é o `map.md` da frente.

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

---

## 1. O hub em uma página

O **context hub** é a casa única do contexto que o Gustavo e os agentes leem e gravam [D, glossário]. Ele existe
inteiro em cada **par**: hoje, as duas **máquinas** do Gustavo (o notebook da ARMIS e a máquina pessoal) [D,
"Onde o servidor mora"].

Em cada par há três camadas:
1. **A verdade:** um banco local guarda cada nota com o histórico de versões e as versões em conflito, com o texto
   cifrado [D, "Como a verdade viaja entre as máquinas"; "Onde o servidor mora"].
2. **A vista:** os arquivos no disco, em `C:\context-hub`, que o Gustavo vê e edita no Obsidian. O sincronizador
   mantém disco e banco iguais o tempo todo, nos dois sentidos [D, "Markdown: vista ou fonte da verdade"; "Revisão do
   sync e da divergência com o banco"; "Windows ou WSL"].
3. **As portas:** os agentes leem e gravam o banco pela porta do banco e acham o conteúdo pela camada de busca
   [D, "Como a verdade viaja…"; "Camada de busca"].

Os pares trocam mudanças direto, pela rede privada: cada um envia as próprias mudanças ao outro. Nenhum é a
referência [D, "Revisão do sync…"; glossário, "Par"]. Uma vez por dia, cada máquina guarda a vista no GitHub, como cópia
de segurança [D, "Revisão do sync…"]. Uma vigia em cada máquina confere a cada 5 minutos se algo diverge e avisa
[D, idem].

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
tickets gerados por "Passagem para a construção" [D, mapa, Notes]. Como a prova de conceito vira o hub real em
`C:\context-hub` [A, mapa, Not yet specified].

**Princípios do desenho** [D, "Lições do vault"]. Valem para todo componente; um diagrama deve deixá-los visíveis:
- uma falha se corrige com **mecanismo**, ou tirando regra, nunca acrescentando regra;
- **cada informação tem um lugar só**, escrito no contrato;
- **o checkpoint grava sem pedido;**
- **a porta de entrada ao conteúdo é a busca**; índice mantido à mão só onde a busca não basta;
- **aval** só para o contrato, os adaptadores e as exclusões ou reescritas grandes;
- **complexidade conquistada:** uma camada só entra se resolve um dos cinco critérios;
- todo arquivo tem destino quando envelhece: compactar ou arquivar;
- textos curtos; frontmatter só com o que a busca ou o contrato usam.

---

## 2. Atores

Quem age no hub, o que quer e por onde chega.

| Ator | Quem é | O que quer | Por onde chega | Estado |
|---|---|---|---|---|
| **Gustavo** | o dono do hub | ver e editar as notas; achar o que precisa; que os agentes guardem sozinhos o que importa; nunca perder trabalho em silêncio | Obsidian (vista Markdown); pedindo a agentes | [D, glossário; mapa, Destination] |
| **Agente de código** | Claude Code, Codex, Copilot (VS Code e linha de comando), dentro ou fora do Maestri | achar o trecho certo sem ler tudo; retomar o trabalho de onde parou; gravar sem desfazer a gravação de outro | sessão numa porta de entrada; porta do banco; camada de busca | [D, "Windows ou WSL"; "Portas de entrada do hub"] |
| **Maestro** | o agente que orquestra um workspace do Maestri | montar e conduzir um workspace sem redescobrir nem depender do Gustavo ditar | sessão do Maestri; começa pelo acervo do maestro | [D, "Maestri: padrão e liberdade"] |
| **Recruta** | um agente num terminal do Maestri, com papel | fazer a parte dele do trabalho | terminal com papel, que abre em `.maestri/roles/<id>/` da pasta do workspace | [D, "Testes do papel do Maestri…"] |
| **Subagente** | ajudante que roda dentro de um agente, sem ocupar terminal | uma tarefa curta | herda a sessão de quem o chamou | [D, "Acervo do maestro: pesquisa de peças"] |
| **Claude Desktop** | o app Claude no Windows (chat e work) | ler o hub quando o Gustavo pede algo por ele; gravar também, segundo o Gustavo | ponte local `mcp-remote` até a porta do banco | leitura [D, "Portas de entrada do hub"]; gravar [A, "Como os agentes gravam no hub"] |
| **Cliente** | computador ou sandbox sem cópia do hub (máquina de passagem, sandbox de teste) | consultar o hub | rede privada até a porta de leitura de um par | [D, "Onde o servidor mora"]; quem usa de fato [G, 8] |
| **Outro par** | a outra máquina, igual a esta | receber as mudanças daqui e enviar as dela | rede privada, de banco a banco | [D, "Revisão do sync…"] |
| **Sincronizador** | processo agendado de cada máquina | manter disco e banco iguais | tarefa agendada no logon, repetindo a cada minuto, uma instância só | [D, "Revisão do sync…"; "Teste: disco e banco sem o Obsidian"] |
| **Vigia** | tarefa agendada de cada máquina | descobrir divergência e avisar | a cada 5 min | [D, "Revisão do sync…"] |
| **Cópia diária** | tarefa de cada máquina que faz commit e push | ter uma cópia de segurança fora das máquinas | uma vez por dia | [D, idem] |
| **Hooks** | checagem de início de sessão, checkpoint, hook de registro de uso, guarda do acervo | impor por mecanismo o que a regra sozinha não garante | configuração de usuário de cada ferramenta | [D, "Contrato file-first…"; "Maestri: padrão e liberdade"]; escopo do usuário nos três [C, "Acesso dos agentes: decisão"] |
| **Verificador** | um modelo diferente que confere uma alteração no acervo | barrar mudança ruim numa peça | chamado pela guarda do acervo, no Claude Code | [D, "Maestri: padrão e liberdade"] |

Gente e agentes ficam do lado de fora dos grupos do hub e chegam pelas portas [D, "Portas de entrada do hub"].

---

## 3. Componentes

Inventário do que existe, por lugar. "Rótulo" é o nome curto que um diagrama usa.

### 3.1 Em cada par

Sistema: Windows, disco NTFS, hub em `C:\context-hub`; WSL fora até surgir caso de uso [D, "Windows ou WSL"].

| Componente | Rótulo | Papel, numa frase | Estado |
|---|---|---|---|
| Banco local (CouchDB) | Banco local | Guarda a verdade: cada nota como um documento de metadados mais pedaços de texto, com histórico de versões e as versões em conflito; o texto fica cifrado de ponta a ponta. | [D, "Como a verdade viaja…"; "Spike: CouchDB e LiveSync"; "Onde o servidor mora"] |
| **Vista Markdown** | Vista Markdown | Os arquivos no disco por onde o Gustavo vê e edita o hub; gerada a partir do banco, e a edição volta ao banco. | [D, glossário; "Markdown: vista ou fonte…"] |
| **Sincronizador** | Sincronizador | Liga disco e banco o tempo todo, nos dois sentidos, sem depender do Obsidian aberto; pega o que qualquer programa grava no disco. Conta como mais um escritor do disco. | [D, "Revisão do sync…"] |
| Obsidian com o plugin de sync | Obsidian | Onde o Gustavo vê, edita e resolve conflito; pode ficar fechado. O cofre é a raiz do hub. O plugin também leva edições ao banco quando o Obsidian está aberto. | [D, "Revisão do sync…"; "Portas de entrada do hub"] |
| Porta do banco (MCP) | Porta do banco | Porta do agente ao banco: lê devolvendo a versão, grava levando a versão lida, e a gravação vira conflito visível se a versão mudou; mostra ao agente que uma nota está em conflito. | [D, "Como a verdade viaja…"]; a guarda de versão e o aviso de conflito **ainda precisam ser construídos** no fork [D, idem] |
| Porta de leitura (segundo MCP) | Porta de leitura | Segunda instância da porta do banco, só de leitura e com token, exposta na rede privada só para os clientes. | [D, "Onde o servidor mora"]; duas instâncias no mesmo banco convivem [D, "Testes das portas de entrada"] |
| **Camada de busca** (obsidian-hybrid-search + arctic-embed-m-v2.0) | Camada de busca | Entrega ao agente o trecho certo sem ele ler tudo: busca por palavra e por sentido sobre a vista Markdown do disco daquela máquina, servida por MCP em HTTP na rede privada. | [D, "Camada de busca"; "Modelos de embeddings da busca"] |
| Índice da busca | Índice da busca | Arquivo `.obsidian-hybrid-search.db` na raiz do hub, um por máquina; tem ponto no nome, então não vai ao banco. | [D, "Camada de busca", teste do arquivo com ponto] |
| Vigia | Vigia do sync | A cada 5 min confere a troca entre os bancos, conflitos abertos, binários descartados, arquivos acima do limite, se o sincronizador está vivo e se o assistente de configuração do plugin travou o sync; grava um estado curto e avisa quando piora. | [D, "Revisão do sync…"] |
| Avisos | Avisos | Saídas da vigia: notificação do Windows quando piora; o estado curto lido no início de sessão; o estado visível o tempo todo na tela do agente. | [D, idem]; na tela: mod no Claude Code, barra de estado no Copilot, checagem e notificação no Codex [C, "Acesso dos agentes: decisão"] |
| Checagem de início de sessão | Checagem de sessão | Hook no começo de toda sessão de agente: lê o estado da vigia, informa a hora da última troca e abre a nota de retomada do trabalho. | [D, "Contrato file-first…"; "Divergência e edição concorrente"] |
| Checkpoint (hook de fim de resposta) | Checkpoint | Ao fim de cada resposta, se a nota de retomada não reflete a resposta, ou se a memória privada da ferramenta ganhou algo que o hub não tem, faz o agente continuar e gravar. | [D, "Contrato file-first…"]: garantido no Claude Code; no Copilot, hook de fim mais extensão experimental [C, "Acesso dos agentes: decisão"]; no Codex [A, idem] |
| Contrato (`AGENTS.md` na raiz) | Contrato | As regras do hub para os agentes, incluindo o lugar de cada informação. O hub não tem `CLAUDE.md` em lugar nenhum. | [D, "Portas de entrada do hub"] |
| Ligações do contrato e das skills | Ligações da ferramenta | Em cada máquina, a configuração global de cada ferramenta aponta para o contrato e as skills do hub (import, link simbólico, junction). | [D, "Portas de entrada do hub"; "Testes da porta do repositório fora do hub"] |
| Guarda do acervo | Guarda do acervo | Fiscaliza gravações no acervo do maestro: no Claude Code recusa ou pede aval e exige um verificador noutro modelo; Codex e Copilot não gravam, deixam propostas. | [D, "Maestri: padrão e liberdade"]; detalhes [NV, "Guarda do acervo: mods e hooks"] |
| Hook de uso e registro de uso | Registro de uso | O hook anota, por máquina, quem usou qual peça do acervo, num arquivo por máquina. | [D, "Maestri: padrão e liberdade"] |
| Hook de início do maestro | Lembrete do maestro | Só age quando a sessão é um terminal do Maestri; lembra o maestro de começar pelo acervo. | [D, idem] |
| Cópia local (`.git` na raiz) | Cópia local (git) | Repositório git de cada máquina, que só faz commit e push uma vez por dia, um ramo por máquina; nunca puxa nem escreve no disco do hub. Também faz o Codex e o Copilot acharem a raiz. | [D, "Revisão do sync…"]; papel de raiz [C, "Acesso dos agentes: decisão"] |
| Nó da rede privada | Nó da rede | Põe o par na rede privada (Tailscale, só no Windows). | [D, "Revisão do sync…"; "Ligar as máquinas com segurança"] |
| Credenciais do par | Credenciais | Senha do banco, frase-senha da cifra, token da porta do banco, chave de escrita no GitHub. Ficam na máquina, não no hub. | [D, "Onde o servidor mora"; "Ponto de encontro do sync"]; onde exatamente [NV] |
| Configuração do Maestri | Maestri | Papéis e partituras ficam no perfil do usuário (`~/.maestri`), fora do hub; o Maestri grava `.maestri/roles/` na pasta do workspace. | [D, "Portas de entrada: pesquisa"; "Maestri: padrão e liberdade"] |
| Memória privada da ferramenta | Memória privada | A memória automática de cada ferramenta (no Claude Code, ligada), no perfil do usuário da máquina. Não é o hub: o checkpoint leva ao hub o que só ela sabe. | [D, "Contrato file-first…"] |

### 3.2 O conteúdo (o que mora dentro do hub)

| Componente | Rótulo | Papel | Estado |
|---|---|---|---|
| **Raiz** (seis) | Raiz | Primeiro nível, cada uma com comportamento próprio: `clients/` (iniciativas de cliente, dois níveis: cliente e iniciativa), `operations/` (trabalho contínuo, sem fim), `initiatives/` (iniciativas sem cliente: produtos, frentes, estudo), `reference/` (conhecimento de referência, promovido), `agents/` (a oficina dos agentes: contrato, skills, papéis, perfil de cada máquina), `inbox/` (captura rápida). O que termina vai para o `_archive/` da própria raiz. | [D, glossário; "Métodos conhecidos de organizar a raiz"]; níveis e `agents/machines/<máquina>.md` [C, "Arquitetura de pastas e frontmatter"] |
| **Iniciativa** | Iniciativa | Frente de trabalho com identificador, estado e próxima ação; mora numa **casa** só. | [D, glossário; "Workloads piloto"] |
| Núcleo da iniciativa | Núcleo | Arquivos de toda iniciativa, separados por ritmo: `initiative.md` (ficha), `retomada.md`, `tasks.md`, `decisions.md`, `context.md`, `log/AAAA-MM.md`; o `AGENTS.md` da iniciativa só com o mapa e as regras próprias. | [C, "Arquitetura de pastas…"] |
| Blocos da iniciativa | Blocos | Subpastas com um nome só, somadas conforme o trabalho pede (`inputs/`, `research/`, `design/`, `plans/`, `deliverables/`, `evidence/`, `tools/`, `runs/`, `work/`, `procedures/`, `cases/`, `queries/`, `knowledge/`, `notes/`, `labs/`, `other/`), descritas em `agents/blocks.md`. | [C, idem] |
| **Nota de retomada** | Nota de retomada | Um arquivo curto por trabalho, sobrescrito, com sete campos (objetivo, onde parou, próximo passo, decisões, o que não deu certo, perguntas abertas, arquivos em jogo); permite a qualquer sessão continuar de onde a outra parou. | [D, "Contrato file-first…"]; arquivo `retomada.md` [C, "Arquitetura de pastas…"] |
| **Acervo do maestro** | Acervo do maestro | Peças prontas (papéis, setups, contratos-opção e outras) para todo maestro, como família de skills `maestro-*` em `agents/skills/`; opções, não regras. Propostas do Codex e do Copilot em `agents/maestro/propostas/`; registro de uso em `agents/maestro/uso/<máquina>.md`. | [D, "Maestri: padrão e liberdade"] |
| Versão local de peça | Versão local | Ajuste de uma peça para uma iniciativa, em `maestro/` dentro da pasta da iniciativa (opcional). | [D, idem] |
| Skills do hub | Skills | Em `agents/skills/<skill>/`, ligadas às pastas de skills de cada ferramenta por junction. | [D, "Portas de entrada do hub"]; como ficam visíveis e o roteamento [A, "Roteamento de skills"] |
| Segredos da iniciativa | Segredos | Pasta `.secrets/` dentro da iniciativa, fora do banco e do git; senhas de contas que acessam ambiente de cliente ficam no KeePass, fora do hub. | [C, "Arquitetura de pastas…"]; a exclusão em qualquer nível precisa ser provada antes do primeiro segredo [C, idem] |
| **Pasta não replicada** | Pasta não replicada | Parte do hub numa máquina só, fora do sync e da cópia no GitHub; a busca da outra máquina não a indexa. Hoje não há nenhuma: tudo vive nas duas máquinas. | conceito [D, glossário]; "nenhuma por ora" [D, mapa, Out of scope]; mecanismo [A, "Arquitetura de pastas…"] |

**O que vai ao banco** [D, "Revisão do sync…"; "Teste: disco e banco sem o Obsidian"]:
- todo arquivo comum até 200 MiB;
- só `.md`, `.txt` e `.csv` são texto, com junção automática; o resto (`.docx`, `.xlsx`, `.pdf`, imagens, `.py`,
  `.json`…) é binário, sem junção;
- pastas com ponto, em qualquer nível, ficam fora; arquivos com ponto também precisam ficar fora (regra a testar na
  construção) [D, "Passagem para a construção", comentário vindo da "Camada de busca"];
- repositório de código mora fora do hub.

**Conteúdo inicial** [D, "Workloads piloto"]: nasce no hub esta frente e o que o Gustavo disser. O que vem do vault
`ai-operating-system` é **copiado** e trabalhado só no hub; o que fica no vault é referência, não segunda casa. Já
desejados: `armis-docs`, `armis-brand` e a skill `armis-docx`. A operação de SOC da iniciativa STRATA fica fora por ora.

### 3.3 Fora das máquinas

| Componente | Rótulo | Papel | Onde | Estado |
|---|---|---|---|---|
| Rede privada (tailnet) | Rede privada | O único caminho entre pares e entre cliente e par; nunca exposta à internet. | serviço Tailscale | [D, "Onde o servidor mora"; "Revisão do sync…"] |
| Repositório privado no GitHub | Cópia no GitHub | Cópia de segurança diária da vista, um ramo por máquina; não é ponto de encontro do sync. | GitHub | [D, "Revisão do sync…"; "Ponto de encontro do sync"] |
| **Cliente** | Cliente | Computador ou sandbox que usa o hub através de um par, sem cópia; só lê por padrão; precisa de um par ligado. | qualquer | [D, glossário; "Onde o servidor mora"] |
| Vault `ai-operating-system` | Vault (referência) | Só referência: o agente pode ler, o hub não grava nada nele, nem ponteiro. Só existe no notebook. | notebook | [D, "Workloads piloto"] |
| FreeLLMAPI | Gateway de modelos | Gateway de modelos gratuitos. Depois da construção roda só na máquina pessoal, preso à rede privada; o notebook o chama pela rede. Serve ao modelo de embeddings do Google (desligado) e ao roteamento de tarefas simples. | máquina pessoal | [P, Gustavo no chat, em "Passagem para a construção"]; roteamento [D, "Maestri: padrão e liberdade"] |
| Modelo de embeddings do Google (gemini-embedding-001) | Embeddings na nuvem | Segunda opção da busca por sentido, configurada e **desligada**. Ligar é escolha do Gustavo; ligado, o conteúdo indexado vai ao Google e a busca por sentido depende da rede e da cota. | Google, pelo FreeLLMAPI | [D, "Camada de busca"; "Modelos de embeddings…"]; o gatilho para ligar [G, 12] |

### 3.4 Portas de entrada

Cada caminho pelo qual alguém chega ao hub. A porta diz **onde a sessão abre**; o conteúdo se alcança pela busca.

| Porta | Quem usa | O que recebe | Estado |
|---|---|---|---|
| Sessão na raiz do hub (a principal) | Gustavo, agentes | Os três harnesses leem o `AGENTS.md` da raiz | [D, "Portas de entrada do hub"; "Testes das portas de entrada"] |
| Sessão numa subpasta | agentes | Claude Code lê a cadeia de `AGENTS.md` sozinho; Codex e Copilot chegam à raiz pelo `.git` da raiz; o Copilot também recebe o contrato pelo arquivo global | [D, idem]; `.git` no lugar do marcador [C, "Acesso dos agentes: decisão"] |
| Maestri (workspace e papel) | maestro, recrutas | Workspace de iniciativa abre na pasta dela; dentro de um papel, o contrato chega pela configuração global e pelo ajuste `claude-md-and-agents-md` | [D, "Maestri: padrão e liberdade"] |
| Obsidian | Gustavo | O cofre é a raiz do hub | [D, "Portas de entrada do hub"] |
| Claude Desktop | Gustavo, pelo app | Leitura pela ponte `mcp-remote`; não recebe o contrato por arquivo nem as instruções do MCP | [D, idem; "Testes das portas de entrada"] |
| Cliente pelo MCP de um par | sandbox, máquina de passagem | O começo do contrato (até ~2.000 caracteres) nas instruções do MCP, a regra curta na descrição das ferramentas de gravação, e o contrato na configuração global onde der para instalar | [D, "Portas de entrada do hub"] |
| Sessão num repositório fora do hub | agentes | Contrato por import (`~/.claude/CLAUDE.md`) e por link simbólico (`~/.codex/AGENTS.md`, `~/.copilot/copilot-instructions.md`); skills por junction | [D, idem; "Testes da porta do repositório…"] |

Porta nova que surgir entra como ticket novo, com a mesma regra: só o que ela precisa [D, "Portas de entrada do hub"].

---

## 4. Responsabilidade

Quem é **dono** (decide como é e responde por ele), quem **aciona** (faz agir), quem **lê** (usa o conteúdo) e quem
**só vê** (enxerga o estado, sem usar).

| Componente | Dono | Aciona | Lê | Só vê | Estado |
|---|---|---|---|---|---|
| Banco local | o par (cada máquina o seu) | sincronizador, plugin, porta do banco, replicação do outro par | porta do banco, porta de leitura, sincronizador, plugin, vigia | — | [D, "Revisão do sync…"; "Onde o servidor mora"] |
| Vista Markdown | Gustavo (é a vista dele) | sincronizador, plugin, Gustavo no Obsidian, qualquer programa que grava no disco | Gustavo, camada de busca, agentes que leem o disco, cópia diária | — | [D, "Markdown: vista ou fonte…"; "Camada de busca"] |
| Sincronizador | o par | Agendador do Windows (logon e repetição) | disco e banco | vigia (se está vivo) | [D, "Revisão do sync…"] |
| Obsidian e plugin | Gustavo | Gustavo (abre e fecha) | Gustavo | vigia (se o assistente travou o sync) | [D, idem] |
| Porta do banco | o par | agentes (ler, gravar), Claude Desktop (ler) | agentes | — | [D, "Como a verdade viaja…"; "Portas de entrada do hub"] |
| Porta de leitura | o par | clientes | clientes | — | [D, "Onde o servidor mora"] |
| Camada de busca | o par (um índice por máquina) | agentes, clientes | agentes, clientes | — | [D, "Camada de busca"]; o Gustavo e o Claude Desktop usarem a busca [A] |
| Vigia | o par | Agendador do Windows | banco, sincronizador, plugin | Gustavo (notificação, estado na tela), agentes (estado curto) | [D, "Revisão do sync…"]; quem religa a vigia se ela parar [A] |
| Contrato | Gustavo: alterar pede aval dele | ligações da ferramenta; a sessão ao abrir | todo agente | — | [D, "Lições do vault"] |
| Checagem de sessão | o par (hook no escopo do usuário) | toda sessão de agente ao abrir | estado curto da vigia, nota de retomada | agente | [D, "Contrato file-first…"]; escopo [C, "Acesso dos agentes: decisão"] |
| Checkpoint | o par (hook) | fim de cada resposta | nota de retomada, memória privada | — | [D, "Contrato file-first…"] |
| Nota de retomada | o **trabalho** a que pertence; quem a mantém é o agente da sessão, obrigado pelo checkpoint | checkpoint | checagem de sessão, qualquer sessão nova, Gustavo | — | [D, idem]; "o trabalho é o dono" é leitura minha da regra "uma por trabalho" |
| Acervo do maestro | Gustavo aprova alterar e apagar; o maestro acrescenta sozinho | maestro | maestro, recrutas | — | [D, "Maestri: padrão e liberdade"] |
| Guarda do acervo | o par (escopo do usuário) | tentativa de gravar no acervo | — | Gustavo (pedido de aval) | [D, idem] |
| Registro de uso | cada máquina, o seu arquivo | hook de uso | maestro (para saber quem usa uma peça) | — | [D, idem] |
| Cópia local e cópia no GitHub | Gustavo | tarefa diária | Gustavo, em restauração | — | [D, "Revisão do sync…"]; quem roda a restauração [A] |
| Rede privada | Gustavo (conta do Tailscale, grants) | pares, clientes | — | — | [D, "Onde o servidor mora"]; quem revoga chaves [G, 11] |
| Iniciativa | Gustavo decide que nasce e que termina | agentes trabalham nela | todos | — | [D, "Workloads piloto"]; quem move para o `_archive/` [G, 4] |
| Colisão real | Gustavo resolve, ou um agente com ele vendo | — | — | Gustavo, agentes (avisos) | [D, "Divergência e edição concorrente"; "Revisão do sync…"] |

**O que o Gustavo decide e o que o agente faz sem perguntar** [D, "Lições do vault"; "Maestri: padrão e liberdade"]:
- pede aval: mudar o contrato, os adaptadores (as ligações de cada ferramenta), exclusões ou reescritas grandes;
  alterar ou apagar peça do acervo já usada ou citada;
- não pede: gravar no lugar certo, manter a nota de retomada, levar ao hub o que só a memória privada sabe, triar o que
  é ambíguo, acrescentar peça nova ao acervo, resolver o que o hub junta sozinho;
- só para e avisa: colisão real.
- Onde fica registrado quem aprovou uma mudança no contrato [A].

---

## 5. Pertencimento

### 5.1 Grupos lógicos

Um grupo diz **o que fica junto e por quê**. Uma coisa pode estar em mais de um grupo; aí a tabela diz os dois.

| Grupo | Membros | Por que ficam juntos | Estado |
|---|---|---|---|
| **Núcleo de dados do par** | banco local, vista Markdown, sincronizador | guardam ou movem a mesma verdade dentro da máquina | [D, "Revisão do sync…"] |
| **Portas do par** | porta do banco, porta de leitura, camada de busca | por elas agentes e clientes alcançam o núcleo | [D, "Como a verdade viaja…"; "Onde o servidor mora"; "Camada de busca"] |
| **Vigilância** | vigia, avisos, checagem de sessão | garantem que nada diverge em silêncio | [D, "Revisão do sync…"; "Divergência…"] |
| **Disciplina do agente** | contrato, checagem de sessão, checkpoint, nota de retomada, guarda do acervo, registro de uso, ligações da ferramenta | fazem o agente gravar no lugar certo, sem pedido | [D, "Contrato file-first…"; "Maestri: padrão e liberdade"] |
| **Conteúdo** | as seis raízes, com iniciativas, notas de retomada, acervo do maestro, skills | é o que o banco guarda e a vista mostra | [D, glossário] |
| **Periferia do par** | Obsidian, cópia local (git), nó da rede | estão no par, mas não guardam nem movem a verdade do dia a dia | [D, "Revisão do sync…"] |
| **Fora do par** | rede privada, cópia no GitHub, clientes, Claude Desktop pela ponte, vault, FreeLLMAPI, embeddings na nuvem | ficam fora das duas cópias | [D, idem] |
| **Quem chega** | Gustavo, agentes, maestro, recrutas, Claude Desktop, clientes | agem de fora, pelas portas | [D, "Portas de entrada do hub"] |

**Pertence a mais de um grupo:**
- **Checagem de sessão:** vigilância (mostra o estado da vigia) e disciplina (abre a nota de retomada).
- **Nota de retomada:** conteúdo (é um arquivo da iniciativa) e disciplina (é o que o checkpoint cobra).
- **Acervo do maestro e skills:** conteúdo (moram em `agents/`) e disciplina (a guarda cuida deles).
- **Camada de busca:** portas (é a entrada ao conteúdo) e, fisicamente, depende da vista Markdown do disco.
- **Obsidian:** periferia (pode fechar) e escritor do banco quando aberto (pelo plugin).
- **Claude Desktop:** quem chega (é o Gustavo pedindo) e fora do par (entra por ponte).
- **Contrato:** conteúdo (é o `AGENTS.md` na raiz, replica como os outros) e disciplina (é a regra).

### 5.2 Onde cada coisa vive de fato

| Lugar | O que vive ali | Replica? | Estado |
|---|---|---|---|
| **Disco do par**, `C:\context-hub` | vista Markdown (todo o conteúdo), contrato, skills, acervo, índice da busca, `.git`, `.secrets/` | a vista sim, pelo banco; índice, `.git` e `.secrets/` não (têm ponto) | [D, "Revisão do sync…"; "Camada de busca"]; `.secrets/` [C] |
| **Banco local do par** | a verdade: notas, versões, conflitos, cifrados | sim, para o outro par | [D, "Como a verdade viaja…"] |
| **Configuração do usuário** de cada ferramenta (`~/.claude`, `~/.codex`, `~/.copilot`, `~/.agents/skills`) | ligações para o contrato e as skills, configuração de MCP, hooks, mod do Claude Code, memória privada | não; cada máquina tem a sua, montada pelo kit de par | [D, "Acesso dos agentes: pesquisa"; "Portas de entrada do hub"]; hooks no escopo do usuário [C] |
| **Perfil do Maestri** (`~/.maestri`) | papéis e partituras do Maestri | não | [D, "Portas de entrada: pesquisa"] |
| **Pasta do workspace** (`.maestri/roles/<id>/`) | arquivos do papel que o Maestri grava | não (tem ponto) | [D, "Testes do papel do Maestri…"] |
| **Agendador do Windows** | sincronizador, vigia, cópia diária | não | [D, "Revisão do sync…"] |
| **Sessão do agente** | o chat, o scratchpad, o raciocínio da sessão | não: morrem com a sessão | [D, "Contrato file-first…"] |
| **Rede privada** | só o caminho entre pares e clientes | — | [D, "Onde o servidor mora"] |
| **GitHub** | cópia diária da vista, um ramo por máquina | — | [D, "Revisão do sync…"] |
| **Máquina pessoal** | FreeLLMAPI (depois da construção) | — | [P, "Passagem para a construção"] |
| **Notebook** | vault `ai-operating-system` | — | [D, "Workloads piloto"] |

**Hoje toda cópia de dado do hub mora nas duas máquinas e no GitHub.** Nada mora numa máquina só: o conteúdo de
cliente também vive nas duas, porque o Gustavo trabalha com cliente também na máquina pessoal [D, mapa, Out of
scope; P, "Arquitetura de pastas…"]. Controle de acesso por pasta fica para depois, fora deste projeto [D, mapa, Out
of scope]. O perfil de cada máquina é um arquivo por máquina em `agents/machines/` [C, "Arquitetura de pastas…"]; o
que ele contém [A, mapa, Not yet specified].

---

## 6. Ligações

Quem fala com quem, o que passa e quando.

| De | Para | O que passa | Quando | Estado |
|---|---|---|---|---|
| Disco (vista) | Sincronizador ↔ banco local | mudanças de arquivo, nos dois sentidos, em cerca de 2 s | sempre que a máquina está ligada e logada | [D, "Revisão do sync…"; "Teste: disco e banco…"] |
| Obsidian (plugin) | Banco local | edições do Gustavo; conflitos para resolver | só com o Obsidian aberto | [D, "Revisão do sync…"] |
| Banco local do par A | Banco local do par B | as mudanças do próprio par (cada par envia as suas) | contínuo, com os dois ligados, pela rede privada | [D, idem] |
| Agente | Porta do banco → banco local | leitura com versão; gravação com a versão lida | a cada leitura e gravação | [D, "Como a verdade viaja…"] |
| Porta do banco | Vista Markdown | a gravação chega ao `.md` em cerca de 0,2 s | logo depois de gravar | [D, "Spike: CouchDB e LiveSync"] |
| Agente | Disco, direto | edição do `.md`; o sincronizador leva ao banco, sem conferir a versão | quando o agente edita o arquivo | permitido pelo critério 3 [D, mapa]; como confere a versão [A, "Como os agentes gravam no hub"] |
| Agente | Camada de busca | pergunta → trecho certo | a cada busca; caminho normal até o conteúdo | [D, "Camada de busca"] |
| Camada de busca | Vista Markdown (disco) | indexa os `.md` | quando o disco muda | [D, idem]; tempo de uma edição até a busca [NV] |
| Cliente | Porta de leitura de um par | consultas por HTTP com token | quando o cliente pede | [D, "Onde o servidor mora"] |
| Cliente | Camada de busca de um par | buscas pela rede privada | quando o cliente pede | servida na rede [D, "Camada de busca"]; regra de rede que libera a busca ao cliente [A] |
| Claude Desktop | Porta do banco, pela ponte | leitura | quando pede | [D, "Portas de entrada do hub"] |
| Agente | Guarda do acervo → acervo | gravação liberada, recusada ou com pedido de aval (Claude Code); proposta no lugar da gravação (Codex, Copilot) | a cada tentativa de alterar uma peça | [D, "Maestri: padrão e liberdade"] |
| Hook de uso | Registro de uso | quem usou qual peça, por máquina | quando uma peça é usada | [D, idem] |
| Vigia | Banco, sincronizador, plugin | lê o estado | a cada 5 min | [D, "Revisão do sync…"] |
| Vigia | Avisos | aviso de divergência | quando piora (notificação); sempre visível (tela) | [D, idem] |
| Estado curto e nota de retomada | Checagem de sessão | situação do sync e onde o trabalho parou | no início de toda sessão | [D, "Contrato file-first…"] |
| Checkpoint | Nota de retomada (e o hub) | o que a resposta mudou; o que só a memória privada sabe | ao fim de cada resposta | [D, idem] |
| Cópia local (git) | Cópia no GitHub | commit e push da vista | uma vez por dia | [D, "Revisão do sync…"] |
| Contrato e skills | Configuração de cada ferramenta | import, link simbólico, junction | fixo, montado pelo kit de par | [D, "Portas de entrada do hub"] |
| Camada de busca | Embeddings na nuvem | texto indexado vai ao Google | só se o Gustavo ligar | [D, "Camada de busca"] |

---

## 7. Ações práticas

O que cada ator faz no dia a dia, nas palavras dele, e o caminho técnico que a ação dispara. O cenário completo, com
falhas, está na seção 8.

### 7.1 O Gustavo

| Ele diz ou faz | O que acontece por baixo | Cenário |
|---|---|---|
| "Edito a nota no Obsidian" | o Obsidian grava o `.md`; o plugin (ou o sincronizador) leva ao banco; o banco envia ao outro par | 8.1 |
| "Edito o arquivo no Explorador, no VS Code, num editor qualquer" | o sincronizador pega a mudança no disco e leva ao banco | 8.2 |
| "Crio uma nota nova" | igual a editar; a pasta onde ela nasce depende de onde ele cria | 8.1; pasta padrão [G, 3] |
| "Jogo uma ideia sem pasta certa" | vai para `inbox/`, a captura rápida; o checkpoint faz a triagem | [D, glossário; "Lições do vault"] |
| "Peço ao agente: leia, altere, remova" | o agente busca, lê pela porta do banco, grava levando a versão | 8.5 a 8.7 |
| "Apago uma pasta no Explorador" | o sincronizador apaga os arquivos no banco; a exclusão viaja | 8.7 |
| "Resolvo um conflito" | a janela de conflito do plugin, com o Obsidian aberto; a vigia limpa o estado | 8.12 |
| "Mudo de máquina no meio da tarefa" | a nota de retomada e o trabalho gravado chegam pela troca entre bancos | 8.14 |
| "Peço algo pelo Claude Desktop" | o Desktop lê pela ponte até a porta do banco; gravar está em aberto | 8.17 |
| "Copio algo do vault antigo" | a cópia nasce no hub e passa a ser a casa; o vault não muda | [D, "Workloads piloto"] |
| "Termino uma iniciativa" | a pasta vai para o `_archive/` da raiz, por um script que antes confere se o outro par está em dia e sem edição recente | [D, "Portas de entrada do hub"]; quem roda [G, 4] |
| "Ligo os embeddings do Google" | o índice ao lado do arctic passa a usar o gemini; o conteúdo indexado vai ao Google | [D, "Camada de busca"] |

### 7.2 Um agente de código

| O agente faz | O que acontece por baixo | Cenário |
|---|---|---|
| Abre uma sessão | o contrato chega; a checagem de sessão mostra o estado do sync e abre a nota de retomada | 8.3 |
| Procura algo | pergunta à camada de busca da máquina dele; recebe o trecho, não o arquivo | 8.9 |
| Lê uma nota | pela porta do banco, recebendo a versão; se a nota está em conflito, a porta diz | 8.5 |
| Grava | pela porta do banco, levando a versão lida; se mudou, vira conflito visível e ele relê e refaz | 8.6 |
| Grava direto no disco | o sincronizador leva ao banco; a versão não é conferida | 8.2 |
| Termina uma resposta | o checkpoint confere a nota de retomada e a memória privada; se falta algo, ele continua e grava | 8.3 |
| Toma uma decisão | grava em `decisions.md` e na nota de retomada (linha e ponteiro) | [D, "Contrato file-first…"]; arquivo [C, "Arquitetura de pastas…"] |
| Não sabe em que pasta gravar | segue o contrato e o catálogo de blocos (`agents/blocks.md`); o que não cabe vai para `other/` | [C, "Arquitetura de pastas…"] |
| Tenta alterar uma peça do acervo | passa pela guarda; no Claude Code, verificador e aval; no Codex e no Copilot, deixa proposta | 8.4 |

### 7.3 O maestro

| O maestro faz | O que acontece por baixo | Estado |
|---|---|---|
| Abre a sessão | o contrato e o hook de início o mandam começar pela skill `maestro-acervo` | [D, "Maestri: padrão e liberdade"] |
| Monta um workspace | escolhe um setup (receita de comandos da CLI que ele mesmo executa; cita papéis pelo nome); confere os papéis da biblioteca do Maestri contra o acervo, cria o que falta e reescreve o que está diferente | [D, idem] |
| Ajusta um papel para uma iniciativa | cria uma versão local em `maestro/` da iniciativa; ajuste de papel em uso só pelo prompt | [D, idem] |
| Acrescenta uma peça | grava sozinho | [D, idem] |
| Altera ou apaga uma peça usada | pede aval ao Gustavo, com o que muda, quem é afetado e a recomendação do verificador | [D, idem] |
| Chama um subagente | o subagente roda dentro dele, sem ocupar terminal | [D, "Acervo do maestro: pesquisa"] |
| Recruta um agente | o Maestri abre um terminal com papel na pasta do workspace | [D, "Testes do papel do Maestri…"] |

### 7.4 Os outros

| Ator | Faz | Caminho | Estado |
|---|---|---|---|
| Outro par | altera uma nota | o banco dele envia; o meu recebe; o meu sincronizador escreve no disco; a minha busca reindexa | 8.8 |
| Cliente | consulta | rede privada → porta de leitura (ou busca) de um par → resposta; nunca grava por padrão | 8.10 |
| Sincronizador | roda | logon e repetição a cada minuto; se cair, volta em até 1 min | [D, "Teste: disco e banco…"] |
| Vigia | confere | a cada 5 min; avisa quando piora | 8.12, 8.13 |
| Cópia diária | guarda | commit e push do ramo da máquina | 8.15 |

---

## 8. Cenários

Do gatilho ao fim, com as falhas no caminho. "Máquina A" é onde a ação nasce; "máquina B", o outro par.

### 8.1 O Gustavo edita uma nota no Obsidian

1. Ele abre a nota no Obsidian da máquina A. O que ele vê é o `.md` do disco, a vista do banco [D, glossário].
2. Ele edita; o Obsidian grava o `.md`.
3. O plugin (Obsidian aberto) leva a mudança ao banco local; o sincronizador também cobre o caso [D, "Revisão do
   sync…"].
4. O banco de A envia a mudança ao banco de B pela rede privada.
5. O sincronizador de B escreve no disco de B; a vista de B atualiza; a busca de B reindexa.

Falhas:
- **B desligada:** a mudança espera no banco de A e viaja quando B ligar. Não é divergência; a checagem de sessão em A
  só informa a hora da última troca [D, "Revisão do sync…"].
- **O mesmo trecho mudou em B antes da troca:** colisão real (8.12).
- **Trechos diferentes mudaram nas duas:** juntam-se sozinhos [D, idem].
- **O assistente de configuração do plugin abriu depois de uma atualização e ninguém respondeu:** o plugin para de
  sincronizar; o sincronizador continua levando o disco ao banco; a vigia avisa [D, "Teste: disco e banco…"; "Revisão
  do sync…"].
- **O Obsidian travou:** o que já foi gravado no disco o sincronizador leva; o que não chegou ao disco [NV].
- **Um agente grava a mesma nota ao mesmo tempo na mesma máquina:** a edição do Gustavo no Obsidian não tem proteção
  contra a do agente no mesmo arquivo; isso está fora do escopo [D, mapa, Out of scope]. Na prática, a gravação do
  agente leva a versão; se a do Gustavo chegou antes ao banco, a do agente vira conflito visível (8.6).

### 8.2 Alguém edita o arquivo direto no disco (agente, Explorador, editor)

1. O arquivo muda no disco da máquina A, com o Obsidian aberto ou fechado.
2. O sincronizador pega a mudança em cerca de 2 s e leva ao banco local [D, "Teste: disco e banco…"].
3. Daí em diante, como 8.1, passos 4 e 5.

Falhas e limites:
- **Não há conferência de versão** nessa gravação: se outro escritor mudou o arquivo no meio, a última gravação vence no
  disco [D, "Como a verdade viaja…", comentário em "Como os agentes gravam"]. Como o agente confere a versão ao gravar
  no disco, e se ele deve gravar no disco [A, "Como os agentes gravam no hub"].
- **Arquivo acima de 200 MiB:** não vai ao banco; fica só em A; a vigia lista (8.13).
- **Arquivo ou pasta com ponto** (`.env`, `.secrets/`, `.venv`): fica fora do banco. Pastas com ponto aninhadas
  vazaram no teste na varredura de partida; a regra para cobrir todos os níveis e arquivos com ponto precisa ser
  testada na construção [D, "Teste: disco e banco…"; "Passagem para a construção"].
- **Sincronizador parado:** a mudança fica só no disco; a vigia percebe em até 5 min e avisa (8.13).

### 8.3 Um agente novo abre uma sessão

1. O Gustavo (ou o Maestri) abre o harness numa porta de entrada; a principal é a raiz do hub.
2. **O contrato chega** [D, "Portas de entrada do hub"; "Testes das portas de entrada"]:
   - na raiz: os três harnesses leem o `AGENTS.md`;
   - numa subpasta: o Claude Code lê a cadeia; o Codex e o Copilot chegam à raiz pelo `.git` da raiz [C, "Acesso dos
     agentes: decisão"]; o Copilot também pelo arquivo global;
   - dentro de um papel do Maestri: pela configuração global de cada ferramenta e pelo `claude-md-and-agents-md`;
   - num repositório fora do hub: por import e links simbólicos.
3. **A checagem de início de sessão** lê o estado da vigia, informa a hora da última troca e abre a nota de retomada
   [D, "Contrato file-first…"].
4. **Qual nota:** a pasta onde a sessão abre diz qual é o trabalho. Se não diz, o agente acha a nota pela busca, pelo
   nome que o Gustavo der, ou pergunta. Não adivinha [D, idem].
5. O agente trabalha: busca (8.9), lê (8.5), grava (8.6).
6. Ao fim de cada resposta, o checkpoint confere se a nota de retomada reflete a resposta e se a memória privada tem algo
   que o hub não tem; se falta, o agente continua e grava [D, idem].

Falhas e limites:
- **Um `CLAUDE.md` em qualquer pasta acima do hub** desliga todos os `AGENTS.md` no Claude Code. O kit de par confere
  que não existe [D, "Testes das portas de entrada"; "Portas de entrada do hub"].
- **Contrato chega, mas o agente não obedece:** medido em teste; o hub não tem mecanismo que pegue isso hoje. A
  verificação dos cinco critérios precisa medir [D, "Portas de entrada do hub"; "Testes da porta do repositório…"].
- **O checkpoint não vê** o que foi dito no meio de uma resposta longa e não roda quando o Gustavo interrompe; só a
  regra cobre esses furos [D, "Contrato file-first…"].
- **Hook que falha sem aviso:** nenhum mecanismo decidido pega isso [A].
- **Codex:** hook de fim de resposta e de início em investigação [A, "Acesso dos agentes: decisão"].
- **Copilot com `COPILOT_HOME` definido:** deixa de ler `~/.agents/skills` [D, "Acesso dos agentes: Copilot"].
- **Busca fora do ar:** o agente ainda acha a nota pela pasta (lugar fixo `retomada.md` na iniciativa) ou pelo nome
  [D, "Contrato file-first…"; C, "Arquitetura de pastas…"].
- **Troca de modelo ou `/clear` no meio do trabalho:** o chat e o raciocínio morrem; continua só o que está no hub
  (nota de retomada, decisões, arquivos) [D, "Contrato file-first…"].

### 8.4 Um maestro novo

1. Uma sessão do Maestri abre (workspace de iniciativa na pasta dela; o que cruza iniciativas, na raiz) [D, "Maestri:
   padrão e liberdade"].
2. O contrato e o hook de início (só age em terminal do Maestri) mandam o maestro começar pela skill `maestro-acervo`
   [D, idem].
3. O maestro lê o catálogo e escolhe as peças: setup, papéis, contratos-opção (roteamento de modelos, orquestração,
   onde abrir). São opções; ele pode recusar [D, idem].
4. Antes de usar um papel, confere a cópia da biblioteca do Maestri contra o acervo; cria o papel global se faltar e
   reescreve se estiver diferente [D, idem].
5. Executa o setup como receita de comandos (o maestro não aplica partitura pela linha de comando) [D, "Acervo do
   maestro: pesquisa"].
6. O hook de uso registra cada peça usada no arquivo da máquina [D, "Maestri: padrão e liberdade"].
7. Se falta uma peça no catálogo, ele a cria e a acrescenta sozinho; alterar ou apagar uma peça usada pede aval [D, idem].

Falhas e limites:
- **Editar o prompt de um papel** reescreve os arquivos do papel, apaga ajuste manual e reinicia todos os terminais
  com aquele papel; reiniciar só o terminal não apaga [D, "Testes do papel do Maestri…"].
- **Codex dentro de um papel** só lê o arquivo do papel, a menos que ache a raiz [D, idem].
- **Alteração no acervo pelo Claude Code:** a guarda recusa, roda o verificador em outro modelo e só libera com relatório
  e aval. O tempo de cada hook é 10 s; esperar o aval não conta [D, "Guarda do acervo: mods e hooks"]; tempo real do
  verificador [NV].
- **FreeLLMAPI fora do ar:** para onde o roteamento manda as tarefas simples [A].
- **Renomear a pasta de uma iniciativa** usada como casa de um workspace [NV].

### 8.5 Pedir a um agente para ler

1. O Gustavo pede ("o que diz a nota X?").
2. O agente acha o trecho pela busca da máquina dele, ou vai direto à nota se sabe onde está [D, "Camada de busca";
   "Lições do vault"].
3. Lê pela porta do banco, recebendo o texto e a versão [D, "Como a verdade viaja…"].
4. Se a nota está em conflito, a porta diz; o agente avisa o Gustavo [D, idem]. (Hoje o MCP pronto devolve só a versão
   vencedora, sem aviso; mostrar o conflito é obrigatório antes de usar [D, "Spike: CouchDB e LiveSync"].)

Falhas: **versão velha** — o agente lê a do banco da máquina dele; se a outra máquina mudou e ainda não trocou, ele lê a
versão anterior. O Gustavo percebe pela hora da última troca na checagem de sessão e pelo estado da vigia [D, "Revisão
do sync…"]. **Busca desatualizada** — a busca só enxerga o que já está no disco daquela máquina [D, "Camada de busca"].

### 8.6 Pedir a um agente para alterar

1. O Gustavo pede ("corrija o erro de digitação na nota X").
2. O agente lê a nota pela porta do banco e guarda a versão.
3. Grava levando a versão lida [D, "Como a verdade viaja…"].
4. Se a nota não mudou no meio: o banco aceita; a vista no disco muda em cerca de 0,2 s; se o Obsidian está aberto, a
   nota na tela atualiza [D, "Spike: CouchDB e LiveSync"].
5. Se mudou: a gravação vira **conflito visível**; o agente relê e refaz [D, "Divergência…"; "Como a verdade viaja…"].
6. O banco envia ao outro par (8.8).
7. Ao fim da resposta, o checkpoint confere a nota de retomada.

Falhas: **enquanto a guarda de versão não existir no fork**, a gravação com versão velha apaga a outra do disco, que
fica no banco só até a compactação [D, "Spike: CouchDB e LiveSync"]. Por isso ela é obrigatória antes de usar. **Agente
grava direto no disco** em vez da porta: 8.2. **Mudar a regra geral do hub** (o contrato): pede aval do Gustavo [D,
"Lições do vault"].

### 8.7 Pedir a um agente para remover

1. O Gustavo pede ("remova a nota X" ou "apague a pasta Y").
2. O agente remove (pela porta do banco ou no disco).
3. A exclusão chega ao banco e viaja ao outro par em segundos.
4. Exclusão ou reescrita grande pede aval antes [D, "Lições do vault"].

Falhas e limites:
- **A outra máquina estava editando a nota:** "um lado apaga o que o outro mudou" é colisão real (8.12) [D, glossário].
- **Apagou sem querer:** a exclusão chega à outra máquina em segundos; a recuperação vem da cópia no GitHub (do último
  dia) ou, para texto, do histórico do banco até a compactação [D, "Revisão do sync…"; "Spike: CouchDB e LiveSync"].
- **Remover é apagar ou arquivar?** O que termina vai para o `_archive/` [D, glossário]; o que o Gustavo quer dizer com
  "remova" [G, 4].
- **Mover ou renomear pasta com a outra máquina editando:** a edição fica separada, como conflito "editado × apagado";
  por isso o script do `_archive/` confere o outro par antes [D, "Testes das portas de entrada"; "Portas de entrada do
  hub"]. Renomear uma nota no Obsidian grava a nova e apaga a antiga; o Obsidian reescreve os links [D, "Portas de
  entrada: pesquisa"; "Testes das portas de entrada"].

### 8.8 O outro par altera uma nota

1. Algo muda no banco de B (Obsidian, agente, disco).
2. O banco de B envia a mudança ao banco de A pela rede privada [D, "Revisão do sync…"].
3. O sincronizador de A escreve no disco de A; a busca de A reindexa; o Obsidian de A, se aberto, mostra.
4. Se a mesma nota mudou em A no mesmo trecho: colisão real (8.12).

Falhas: **A desligada:** espera. **B parada por dias:** quando volta, cada banco envia o que acumulou; o que mudou dos
dois lados no mesmo trecho vira colisão [D, "Revisão do sync…"]. Em que ordem as mudanças chegam [NV].

### 8.9 Buscar

1. O agente pergunta à camada de busca da máquina dele, por MCP [D, "Camada de busca"].
2. A busca combina palavra (FTS5 do SQLite, um analisador só para português e inglês) e sentido (embedding arctic local)
   sobre a vista `.md` daquela máquina [D, idem].
3. Devolve trechos com o caminho; o agente abre só o que precisa.
4. Se vai alterar, grava pela porta do banco (8.6).

Limites [D, "Camada de busca"]:
- a busca não é feita pelo banco, porque o texto lá é cifrado;
- enxerga só o disco daquela máquina: nota da outra máquina ainda não trocada não aparece; pasta não replicada da outra
  máquina não aparece;
- continua funcionando com o Obsidian fechado, porque o sincronizador mantém o disco vivo [D, "Revisão do sync…"];
- enxerga o que está gravado no disco, não o que ainda está só na tela;
- nota com YAML inválido fica fora do índice;
- se lê `.txt` e `.csv` [NV]; autenticação do servidor HTTP da busca [NV]; tempo de uma edição até aparecer [NV];
- o que mais falha são sinônimos (buscar "anotações" e o texto dizer "vault"); quem resolve é o embedding.
- **Máquina sem sincronizar há dias:** a busca mostra o que o disco tem, sem aviso próprio; o aviso vem da vigia e da
  checagem de sessão.
- Índice e busca por `index.md` nas pastas que crescem: em revisão até a busca [C, "Arquitetura de pastas…"].
- A reserva: um índice dentro da porta do banco (a "Robusta"), guardado; volta se a busca precisar mostrar uma gravação
  em segundos ou se o gemini não rodar ao lado do arctic [D, "Camada de busca"].

### 8.10 Um cliente consulta

1. Um sandbox ou máquina de passagem entra na rede privada com chave temporária e etiqueta [D, "Onde o servidor mora"].
2. Uma regra da rede só deixa essa etiqueta chegar à porta de leitura de um par [D, idem].
3. O agente do cliente consulta por HTTP com token; recebe o começo do contrato nas instruções do MCP [D, "Portas de
   entrada do hub"].
4. O par responde com o que está no banco dele.

Limites e falhas:
- **Sem par ligado, o cliente não funciona** [D, glossário].
- **Grava?** Por padrão, não. Quem decide liberar é o Gustavo [D, "Onde o servidor mora"]. Um token de cliente que vaza
  dá leitura, e só de dentro da rede privada.
- **O cliente nunca recebe a credencial do banco** [D, idem].
- **Depois de parar:** o nó temporário sai sozinho da rede de 30 a 60 min após a última atividade (no teste, mais de 35
  min) [D, "Portas de entrada: pesquisa"; "Testes das portas de entrada"]. Validade da chave [A].
- **Busca pelo cliente:** a busca é servida na rede; a regra que a libera à etiqueta do cliente [A].
- **Claude no celular ou na web:** não alcança a rede privada; conector remoto parte dos servidores da Anthropic [D,
  "Portas de entrada: pesquisa"].
- **Pastas com ponto** não estão no banco, então o cliente não as vê.

### 8.11 Um par novo entra

1. Instala o kit de par: rede privada, banco, porta do banco, sincronizador, plugin, ligações das ferramentas [D,
   "Onde o servidor mora"; "Passagem para a construção"].
2. O plugin entra por um link de configuração copiado de um par que funciona; a frase-senha da cifra vem por outro
   canal [D, "Onde o servidor mora"].
3. O sincronizador sobe antes do plugin; o dispositivo novo é recusado até alguém confirmá-lo [D, "Teste: disco e
   banco…"; "Revisão do sync…"].
4. O banco novo replica com o outro: recebe as notas com o histórico que ainda existe (a compactação apaga corpos
   antigos) [D, "Revisão do sync…"].
5. Na primeira partida, o sincronizador refaz a base dos arquivos que não conhece; o histórico comum se perde uma vez
   [D, "Teste: disco e banco…"].

O primeiro teste da construção é justamente dois bancos replicando entre si; se falhar, a volta é um banco só numa
máquina [D, "Onde o servidor mora"].

### 8.12 Uma colisão

**Colisão real:** o mesmo trecho mudou dos dois lados, um lado apagou o que o outro mudou, ou não existe mais a versão
comum [D, glossário].

Texto (`.md`, `.txt`, `.csv`):
1. A troca entre os bancos traz as duas versões; o banco guarda as duas [D, "Spike: CouchDB e LiveSync"].
2. Só aquela nota fica retida; o resto continua viajando [D, "Revisão do sync…"].
3. Com o Obsidian aberto, a janela de conflito abre, com faixa na nota e contador, nas duas máquinas [D, "Spike:
   CouchDB e LiveSync"].
4. Com o Obsidian fechado, a vigia acha o conflito e avisa (notificação, estado na tela, checagem de sessão) [D,
   "Revisão do sync…"].
5. A porta do banco mostra ao agente que a nota está em conflito [D, "Como a verdade viaja…"].
6. O Gustavo resolve, ou um agente com ele vendo. Até chegar a tela de três vias editável, ele escolhe uma versão e
   reedita; "juntar as duas" do plugin mutila o texto [D, "Como a verdade viaja…"].
7. A resolução numa máquina limpa o aviso na outra; a vigia limpa o estado [D, "Spike: CouchDB e LiveSync"].

Binário (`.docx`, `.xlsx`, imagem, PDF…):
1. O hub fica sozinho com a versão de data mais nova, sem perguntar [D, "Revisão do sync…"].
2. A perdida fica guardada; a vigia a acha e avisa.
3. Um comando recupera a versão perdida para um arquivo ao lado [D, idem].

Limites: conflito aberto conta como divergência até ser resolvido; enquanto isso, as outras notas viajam [D, idem].

### 8.13 Uma máquina desligada, parada ou travada

| Situação | O que o hub faz | Estado |
|---|---|---|
| A outra máquina desligada | não é divergência; as mudanças esperam no banco local e viajam quando ela ligar; a checagem de sessão informa a hora da última troca | [D, "Revisão do sync…"] |
| Esta máquina não consegue enviar há mais de 15 min, com a outra ligada | é divergência; o aviso nasce **nesta** máquina, a que travou | [D, idem] |
| O sincronizador parou | a vigia vê em até 5 min; notificação e estado na tela; volta sozinho em até 1 min pela repetição agendada | [D, idem; "Teste: disco e banco…"] |
| O Windows desliga à noite | o sincronizador para com ela; volta no logon | [D, "Revisão do sync…"] |
| O notebook fecha no meio de uma troca | o que já está no banco local fica; viaja quando voltar | [NV] |
| Uma máquina fica dias parada | ao voltar, cada banco envia o que acumulou; mesmo trecho dos dois lados vira colisão | [D, idem] |
| Só o notebook ligado | continua editando, buscando e gravando; guarda tudo para enviar depois; fica sem o FreeLLMAPI (que mora na máquina pessoal) | [D, "Revisão do sync…"; P, "Passagem para a construção"] |
| Um arquivo acima de 200 MiB | não viaja; a vigia lista; conta como divergência enquanto existir | [D, "Revisão do sync…"] |
| A vigia parou | ninguém decidiu quem percebe | [A] |
| A notificação passou despercebida | o estado curto fica gravado; a checagem de sessão o mostra; o mod mostra o tempo todo | [D, idem] |
| A chave do nó na rede privada vence (180 dias) | a máquina sai da rede privada e para de trocar; a outra continua; a vigia vê a troca parada | prazo [D, "Ligar as máquinas com segurança"]; o resto é leitura minha [NV] |

### 8.14 O Gustavo muda de máquina no meio da tarefa

1. Na máquina A, o checkpoint mantém a nota de retomada em dia.
2. A nota viaja ao banco de B como qualquer nota.
3. Na máquina B, a sessão nova abre na pasta do trabalho; a checagem de sessão abre a nota e informa a hora da última
   troca [D, "Contrato file-first…"].

Falha: se A não enviou ainda (desligou antes), B vê a nota velha e a hora da última troca diz isso.

### 8.15 A cópia diária

1. Uma vez por dia, a tarefa de cada máquina faz commit da vista no `.git` da raiz e push para o ramo da máquina no
   GitHub [D, "Revisão do sync…"].
2. O git nunca puxa nem faz checkout; não escreve no disco do hub [D, idem].
3. Cada máquina usa a própria chave de escrita, só desse repositório; a chave não expira e pode ser revogada numa
   máquina sem afetar a outra; commits sem assinatura [D, "Ponto de encontro do sync"].

**Por que não é o sync:** a troca entre bancos levaria um estrago às duas máquinas em segundos, e a compactação apaga o
histórico; o GitHub guarda um dia de distância [D, "Revisão do sync…"].

Limites: a cópia vai **para fora das máquinas**, num repositório privado. Ela leva toda a vista, inclusive o conteúdo
de cliente (decorre da decisão; não foi discutido em separado) [G, 6]. Pastas com ponto e `.secrets/` ficam fora do
git [C, "Arquitetura de pastas…"]. Uma chave que vaza dá leitura e escrita nesse repositório; não chega aos bancos.
**O hub não é um sistema de backup**: a cópia diária é uma rede de segurança, não versão por versão.

### 8.16 Um segredo cai no hub

1. Um agente cola uma senha numa nota, ou cria um `.env` dentro do hub.
2. Nota comum: vai ao banco, ao outro par e à cópia no GitHub. **Nada decidido impede isso** [A].
3. Arquivo ou pasta com ponto (`.env`, `.secrets/`): fica fora do banco e do git, se a regra cobrir todos os níveis
   (teste obrigatório antes do primeiro segredo) [C, "Arquitetura de pastas…"].
4. Senhas de contas que acessam ambiente de cliente ficam no KeePass, fora do hub [C, idem].
5. Se o log do sincronizador guarda trecho de nota [NV].

### 8.17 O Gustavo pede algo pelo Claude Desktop

1. O Desktop chega à porta do banco pela ponte `mcp-remote` (MCP local) [D, "Portas de entrada do hub"].
2. Lê. Não recebe o contrato por arquivo nem as instruções do MCP [D, "Testes das portas de entrada"].
3. Gravar: o Gustavo disse que ele não deve ser proibido de escrever no hub; se grava pela pasta conectada (disco) ou
   pela porta do banco com a guarda de versão [A, "Como os agentes gravam no hub"].
4. Se a conexão cai no meio de uma gravação [NV].

---

## 9. O que o hub não é e não faz

| Afirmação | Estado |
|---|---|
| Não é um repositório git comum: a verdade está num banco; o git só guarda uma cópia diária | [D, "Revisão do sync…"] |
| Não é um sistema de backup | [D, idem] |
| Não junta binários: na colisão fica o mais novo | [D, idem] |
| Não protege a edição do Gustavo no Obsidian contra um agente no mesmo arquivo | [D, mapa, Out of scope] |
| Não controla acesso por pasta | [D, mapa, Out of scope] |
| Não grava nada no vault antigo | [D, "Workloads piloto"] |
| Não controla como ferramentas e modelos trabalham (política por modelo, gateway, regras no MCP): é um segundo mapa | [D, mapa, Out of scope] |
| Não serve à internet: tudo só pela rede privada | [D, "Onde o servidor mora"] |
| Não usa o FreeLLMAPI no checkpoint nem faz revisão depois da sessão | [D, "Contrato file-first…"] |
| Não usa WSL | [D, "Windows ou WSL"] |
| Não tem `CLAUDE.md` | [D, "Portas de entrada do hub"] |
| Não tem operação remota nem SSH por ora | [D, mapa, Out of scope] |

---

## 10. Segurança e dado de cliente

| Afirmação | Estado |
|---|---|
| Tudo só pela rede privada; nunca exposto à internet | [D, "Onde o servidor mora"] |
| Senha no banco; cifra de ponta a ponta na troca; token na porta do banco; link de configuração e frase-senha por canais separados | [D, idem] |
| Cada par guarda a cópia completa e a frase-senha; a regra de dado de cliente vale igual nos dois | [D, idem; mapa, Out of scope] |
| Com a cifra, o banco guarda o texto cifrado; quem lê é quem tem a frase-senha (os pares e a porta do banco) | [D, "Onde o servidor mora"; "Camada de busca"] |
| Se a cifra esconde também os nomes dos arquivos | [NV] |
| Sem a cifra, quem acessa o banco lê o texto | consequência [NV] |
| Cliente: chave temporária, etiqueta, só a porta de leitura; nunca a credencial do banco | [D, "Onde o servidor mora"] |
| Cópia no GitHub: repositório privado; leva toda a vista | [D, "Revisão do sync…"]; com dado de cliente [G, 6] |
| Notas e tickets citam a iniciativa de cliente pelo nome; dados pessoais ficam nas pastas de origem | [D, mapa, Notes] |
| O que o agente lê vai ao provedor do modelo que ele usa; regra para dado de cliente com modelos na nuvem | [G, 6] |
| Embeddings: o padrão é local (o texto não sai da máquina); o do Google, desligado, mandaria o texto indexado ao Google | [D, "Camada de busca"] |
| A política da empresa pode bloquear o MCP do hub; no teste, a conta da empresa não bloqueou, no VS Code nem no CLI | [C, "Acesso dos agentes: decisão"]; risco [D, "Copilot com assinatura Enterprise"] |
| Quem revoga a chave de uma máquina devolvida ou vendida | [G, 11] |

---

## 11. O que ainda não está decidido

Tudo abaixo é proposta, pesquisa em curso ou lacuna. Um diagrama que mostrar estes itens deve marcá-los "a decidir" ou
"não verificado".

| Assunto | Situação | Onde |
|---|---|---|
| Como os agentes gravam: disco, porta do banco ou os dois; conferência de versão no disco; se o Claude Desktop grava e por onde | aberto | "Como os agentes gravam no hub" |
| A busca e a porta do banco num endereço só para o agente | aberto | "Acesso dos agentes: decisão" |
| Fim de resposta e início de sessão no Codex; estado da vigia na tela do Codex | em investigação | idem |
| Árvore dentro da iniciativa e ficha | rodadas respondidas, ticket aberto | "Arquitetura de pastas e frontmatter" |
| Índices (`index.md`) e busca; onde mora o texto extraído de docx, pdf, xlsx | espera a busca, agora decidida | idem |
| Pasta não replicada: mecanismo | aberto; hoje não há nenhuma | idem; mapa |
| Roteamento de skills | aberto | "Roteamento de skills" |
| Perfil por máquina: o que é local e como se declara | não especificado | mapa |
| O Obsidian do hub ao lado do cofre do vault | não especificado | mapa |
| A passagem da prova de conceito ao hub real | aberto | "Passagem para a construção" |
| Usos do FreeLLMAPI além de embeddings | não especificado | mapa |
| Gatilho para ligar os embeddings do Google | Gustavo liga quando quiser; gatilho não definido | "Camada de busca" |
| Tela de colisão com três vias editável | decidida para logo depois da construção | "Como a verdade viaja…" |
| Quem percebe a vigia parada; quem religa | lacuna | — |
| Quem percebe um hook que falha | lacuna | — |
| Regra de rede que libera a busca aos clientes | lacuna | — |
| O que impede segredo dentro de nota comum | lacuna | — |
| Zonas por ciclo de vida (canônica, trabalho, efêmera, derivada) | só na exploração, desenhadas para o disco como verdade; não fixadas | exploração, §9 (fundo) |
| **Não verificado:** duas instâncias da porta do banco por par em produção; arquivos entre 50 e 200 MiB; guarda do acervo em detalhe; autenticação, `.txt` e `.csv` e segundo índice na busca; tempo de edição até a busca; ordem de chegada depois de um corte; o que o plugin perde se o Obsidian trava | conferir na construção | vários |

**Fundo que não vale mais:** a exploração (§7.1, §9) falava em Markdown como fonte da verdade, hub hospedado numa
máquina e git como sync. As três coisas foram trocadas ("Markdown: vista ou fonte…", "Onde o servidor mora",
"Revisão do sync…"). O GitHub como ponto de encontro, o sincronizador por git e "colisão para a máquina inteira" também
saíram ("Revisão do sync…"). A divergência por "30 min sem sync" virou 15 min.

---

## 12. O que não é o hub (e aparece perto dele)

| Coisa | O que é | Relação com o hub | Estado |
|---|---|---|---|
| Biblioteca do Maestri | papéis e partituras no perfil do Maestri (`~/.maestri`), uma por máquina | o acervo do hub é a fonte; o maestro confere a biblioteca contra o acervo e a atualiza | [D, "Maestri: padrão e liberdade"] |
| Skills `maestri-*` | skills que o app Maestri instala e regrava | o acervo usa outro prefixo (`maestro-*`) para não colidir | [D, "Acervo do maestro: pesquisa"] |
| Portal do projeto (rodadas, caixa, cartas, página Laços) | a ferramenta desta frente para o Gustavo decidir: ele responde rodadas; o portal avisa o maestro; o maestro absorve a resposta no ticket; os visuais são feitos pelo Designer, a pedido do maestro | ferramenta da frente que constrói o hub; virar peça do acervo é futuro | [D, mapa, Notes]; como peça [A, mapa, Not yet specified] |
| Mapa e tickets desta frente | o planejamento do hub | vivem no repositório da prova de conceito; o dono das decisões é o Gustavo, que decide no portal | [D, mapa, Notes] |
| Vault `ai-operating-system` | a casa antiga | só referência | [D, "Workloads piloto"] |
| Repositórios de código | código de produto | moram fora do hub; recebem o contrato pela configuração global | [D, "Revisão do sync…"; "Portas de entrada do hub"] |
