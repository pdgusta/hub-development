# Matriz de responsabilidade: o que a descrição não deu

Desenho: `matriz-responsabilidade.html` (SVG embutido, sem rede). Lido só `descricao-do-hub.md`, versão 1, 2026-10-15.
A matriz tem 44 componentes nas linhas e 16 colunas de ator (15 atores e um "Google (provedor)"). Cobre os
componentes de §3 e os atores de §2, mais o que §4 e §3 nomeiam fora desses lugares.

## Faltou

1. **"O par" como ator (§2 × §4).** §4 usa "o par" como dono de 13 linhas (Banco local, Porta do banco, Porta de
   leitura, Sincronizador, Vigia, Checagem, Checkpoint, Guarda, Registro, Nó, Credenciais, Índice, Camada de busca),
   mas §2 não lista o par como ator. Criei a coluna "O par (esta máquina)" para representá-lo.
2. **Componentes de §3 sem linha em §4.** Só 19 dos 38 componentes de §3 aparecem em §4. Ficaram de fora, entre outros:
   Índice da busca, Avisos, Ligações da ferramenta, Lembrete do maestro, Nó da rede, Credenciais, Configuração do
   Maestri, Memória privada, Raiz, Núcleo, Blocos, Versão local, Skills, Segredos, Pasta não replicada, Cliente,
   Vault, FreeLLMAPI, Embeddings na nuvem (§3.1, §3.2, §3.3). Para a matriz, o papel desses saiu de §3 e de §8.
3. **Componentes citados fora de §3.** Ponte mcp-remote (§2, §3.4, §8.17); Assistente de configuração do plugin
   (§8.1, §8.13); Mod de tela do Claude Code (§3.1 "Avisos", §5.2); Script de arquivamento `_archive/` (§4 Iniciativa,
   §7.1); KeePass (§3.2, §8.16); Pasta do workspace `.maestri/roles/` (§2, §5.2). Acrescentei todos como linhas.
4. **Atores citados fora de §2.** Agendador do Windows ("aciona" em §4, para Sincronizador, Vigia e Cópia; §5.2) e
   Google / provedor do modelo (§3.3, §6, §10: destino do texto indexado e do que o agente lê). Acrescentei as duas
   colunas.
5. **Verificador (§2).** A relação com a guarda do acervo só aparece em §2 e §8.4. Não tem linha em §4 nem em §6.
6. **Dono da nota de retomada (§4).** O dono é "o trabalho", que não é ator de §2. A matriz não tem onde colocá-lo.
7. **Dono não dito.** Não há dono em §3 ou §4 para: Ligações da ferramenta, Configuração do Maestri, Script de
   arquivamento, Segredos da iniciativa, Memória privada, Ponte mcp-remote. Para Config do Maestri, Script e Ponte
   deixei "?". Ligações, Segredos e Memória ficaram com "o par", por inferência minha.
8. **Recruta e Subagente.** §2 os descreve, mas nenhuma linha de §4 nem caminho de §6 os cita. Não há como saber se
   leem o contrato, gravam no acervo ou usam a porta do banco.
9. **Lacunas que a descrição deixa em aberto.** A matriz marca "?" onde a descrição diz a decidir: quem religa a
   vigia parada e quem percebe hook que falha (§11); quem roda a restauração (§4, Cópia local); quem revoga chave
   de máquina (§10, [G, 11]); quem move iniciativa para `_archive/` (§4, [G, 4]); onde nasce nota nova (§7.1,
   [G, 3]).

## Inventei

1. **Coluna "O par (esta máquina)"** para o dono "o par" (ver Faltou 1). É a suposição mais visível da matriz.
2. **Colunas "Agendador do Windows" e "Google (provedor)"** tiradas de §4 e §3.3 (ver Faltou 4).
3. **Seis linhas de componentes** que §3 não lista (ver Faltou 3).
4. **Regra da célula.** Cada célula é o papel do ator sobre o componente. Usei §4 quando o ator aparece numa das
   colunas de §4. Usei §2, §7 e §8 quando o ator age sobre o conteúdo do componente (por exemplo, o agente lê pela
   porta do banco: Banco local × Agente = "A·L"). Quando §4 põe componente como ator (Obsidian aciona banco), a célula
   do ator humano ficou vazia. Relação componente para componente não aparece na matriz (está em §6).
5. **Hooks como ator.** Em "Hooks" marquei "=" nas linhas que são hooks: Checagem, Checkpoint, Registro, Lembrete e
   Guarda. Tratei o ator como a soma desses hooks, como §2 sugere.
6. **Diagonal "=".** Sincronizador, Vigia e Cliente são linha e coluna ao mesmo tempo. Marquei "=" onde o componente
   é o próprio ator.
7. **Maestro, Recruta e Subagente como agentes.** Supus que são "sessões de agente" para Checagem e Checkpoint, e que
   leem o contrato e a vista, porque o acervo fica dentro da vista (§4). Recruta ficou sem leitura da vista.
8. **Claude Desktop.** "AL" na Porta do banco, porque §4 põe o Desktop como "aciona (ler)". "A" na Ponte. Gravação
   pelo Desktop ficou em aberto (ver Ambíguo 5).
9. **Cliente lê o contrato** (começo, pela instrução do MCP; §3.4) e a camada de busca (aciona e lê).
10. **Gustavo "V" na Guarda do acervo**, porque §4 põe "Só vê" para o pedido de aval (ver Ambíguo 2).
11. **Estado da linha** veio de §4 quando a linha está lá, e de §3 quando não está. "Pasta não replicada" ficou "A",
    como a descrição marca.
12. **Fora da matriz:** "Colisão real" (§4), que é evento e não componente; e as portas de entrada de §3.4, que são
    caminhos e não componentes (chegam aos atores já representados).

## Ambíguo

1. **Quem é dono do acervo (§4, Acervo do maestro).** Diz "Gustavo aprova alterar e apagar; o maestro acrescenta
   sozinho". A matriz põe o Gustavo como "D·A" e o Maestro como "D·A·L". A descrição não diz se o acervo tem um dono.
2. **Gustavo na guarda do acervo (§4, Guarda; §4, Acervo; §7.3).** §4 põe o Gustavo só como "Só vê", no pedido de
   aval. Mas §4 (Acervo) diz que ele aprova alterar e apagar, e §7.3 diz que o maestro "pede aval". Não está claro se
   ele decide ou só enxerga.
3. **Quem grava no fim da resposta (§3.1, Checkpoint; §8.3, passo 6).** §3.1 diz que o hook "faz o agente continuar
   e gravar"; §8.3 diz que o agente grava. Não está claro se o hook grava ou só obriga o agente.
4. **Gravação do Claude Desktop (§2; §3.4; §4; §8.17).** §2 diz que ele grava "segundo o Gustavo". §3.4 diz que ele
   não recebe o contrato. §4 põe o Desktop só como "aciona (ler)". §8.17 deixa a gravação em aberto. A matriz mostra
   só a leitura.
5. **Quem entra em "agentes" (§4, Porta do banco e Vista; §8.5).** §4 diz "agentes", sem citar Maestro, Recruta ou
   Subagente, que §2 lista como agentes. A matriz presume que sim, mas a descrição não confirma.
6. **Gustavo e a busca (§4, Camada de busca).** §4 põe o Gustavo fora de "Lê" e, numa frase à parte, diz que ele
   "usar a busca" é [A]. A matriz põe "L" com estado A. Não está claro se ele lê.
7. **"Lê: todos" (§4, Iniciativa).** Não diz quem são "todos". Presumi os atores que tocam conteúdo do hub: Gustavo,
   agentes, Maestro, Recruta, Subagente, Claude Desktop, Cliente e Outro par. Outra leitura mudaria as células.
8. **Lembrete do maestro (§3.1) e o terminal do Recruta.** §2 diz que o recruta é um terminal do Maestri. O hook só
   age em terminal do Maestri e lembra o maestro. Não diz se ele também lembra o recruta.
9. **Quem escreve em Configuração do Maestri (§3.1; §5.2; §7.3; §8.4).** §3.1 diz que os papéis ficam no perfil do
   usuário e o Maestri grava `.maestri/roles/`. §7.3 diz que o maestro cria versão local. §8.4 diz que o maestro
   "reescreve se estiver diferente". Não diz se a escrita é do maestro ou do app.
10. **Nota de retomada: dono (§4).** A própria linha diz que o dono é "o trabalho" e, em seguida, que quem mantém é
    "o agente da sessão". O campo do dono está em duas coisas ao mesmo tempo.
11. **Hooks valem em todos os agentes? (§3.1, Checkpoint; §3.4; §8.3, Falhas).** Checkpoint é "garantido no Claude
    Code", no Copilot é hook mais extensão experimental, e no Codex está em investigação. A matriz trata Checagem e
    Checkpoint como valendo para todo agente. A descrição não confirma.
