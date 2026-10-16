# Mistura, volta 2: planta da B com as linhas de quem aciona (da A) e cenários acesos. Conteúdo só de descricao-do-hub.md (v3.2).
import json, sys, os
from html import escape as esc

OUT = sys.argv[1]
D, NV, AC, EC = 'a decidir', 'não verificado', 'a construir', 'em curso'

def c(rot, papel, selos=(), **quem):
    return (rot, papel, quem, list(selos))

# ---------------------------------------------------------------- conteúdo (descrição v3.1: seções 2, 3, 4, 5.1, 6)
G = {
 'nucleo': dict(nome='Núcleo de dados do par', frase='Guardam ou movem a mesma verdade dentro da máquina. O banco é a verdade: a edição no disco só conta quando chega a ele.',
  itens=[
   c('Banco local', 'Guarda a verdade: cada nota com o histórico de versões e as versões em conflito, com o texto cifrado. A compactação automática apaga corpos de versões antigas, sem prazo fixo.',
     dono='Gustavo', aciona='sincronizador, plugin, porta do banco, porta de escrita do cliente (se ligada), replicação do outro par',
     le='porta do banco, porta de leitura, sincronizador, plugin, replicação do outro par, vigia (estado das trocas)'),
   c('Vista Markdown', 'Os arquivos no disco, em C:\\context-hub, por onde o Gustavo vê e edita o hub. Espelha o banco nos dois sentidos.',
     dono='Gustavo', aciona='sincronizador, plugin, Gustavo (Obsidian, Explorador), agentes (disco)', le='Gustavo, camada de busca, agentes (disco), cópia diária'),
   c('Sincronizador', 'Liga disco e banco o tempo todo, nos dois sentidos, sem depender do Obsidian aberto; pega o que qualquer programa grava no disco. Volta sozinho em até 1 min se o processo morrer.',
     dono='Gustavo', aciona='Agendador do Windows', le='disco e banco; vigia (se está vivo)'),
   c('Exclusão', 'Regra no sincronizador e no plugin que deixa fora do banco as pastas com ponto, em qualquer nível; precisa cobrir também arquivos com ponto.',
     [(D, 'cobertura: no teste, pastas com ponto aninhadas foram ao banco; teste na construção')],
     dono='Gustavo', aciona='kit de par (configura)', le='sincronizador, plugin')],
  lig=[('Vista Markdown → Sincronizador → Banco local', 'Mudanças de arquivo, nos dois sentidos, sempre que a máquina está ligada; cerca de 2 s, medido com um banco só.', []),
       ('Vista Markdown → plugin → Banco local', 'O mesmo caminho, só com o Obsidian aberto. O primeiro dos dois que vir leva; juntos não criam ciclo.', []),
       ('Banco local → Sincronizador → Vista Markdown', 'O que chegou pela porta ou do outro par desce ao disco: o sincronizador (ou o plugin) escreve; pela porta, cerca de 0,2 s.', [])]),
 'portas': dict(nome='Portas do par', frase='Por elas agentes, clientes, o Gustavo e o Claude Desktop alcançam o núcleo. A porta diz onde a sessão abre; o conteúdo se alcança pela busca.',
  itens=[
   c('Porta do banco', 'Porta do agente ao banco: lê devolvendo a versão; grava levando a versão lida, e a gravação vira conflito visível se a versão mudou. Entrega texto em claro.',
     [(AC, 'a guarda de versão e o aviso de conflito: o servidor pronto grava por cima; obrigatórios antes de usar'), (D, 'como os agentes gravam: disco, porta do banco ou os dois'), (D, 'por onde o Claude Desktop grava'), (D, 'o que o agente faz quando a porta do banco está fora: grava no disco ou espera')],
     dono='Gustavo', aciona='agentes (ler e gravar); Claude Desktop pela ponte (ler; gravar é requisito)', le='agentes, Claude Desktop'),
   c('Camada de busca', 'Entrega o trecho certo sem ler tudo: busca por palavra e por sentido sobre a vista do disco daquela máquina. Só lê; gravar é pela porta do banco.',
     [(NV, 'como o Obsidian chega à busca do hub'), (D, 'por onde o Claude Desktop chega à busca'), (D, 'regra de rede que libera a busca aos clientes'), (D, 'a busca e a porta do banco num endereço só')],
     dono='Gustavo', aciona='agentes, clientes, o Gustavo (pelo Obsidian ou pedindo a um agente) e o Claude Desktop', le='os mesmos', aprova='Gustavo liga o índice do Google'),
   c('Porta de leitura', 'Segunda instância da porta do banco, só de leitura, com token próprio, exposta na rede privada só para os clientes. Recusa gravação no próprio servidor.',
     [(NV, 'formato da recusa; duas instâncias por par em produção')], dono='Gustavo', aciona='clientes (só leitura)', le='clientes'),
   c('Porta de escrita do cliente', 'Outra instância, com escrita e a mesma guarda de versão, só na rede privada. Não existe por padrão: o Gustavo a liga quando quiser.',
     [(EC, 'decidido pelo Gustavo; ticket aberto')], dono='Gustavo', aciona='clientes a quem o Gustavo deu o token', le='clientes', aprova='Gustavo liga e dá o token'),
   c('Índice da busca', 'Arquivo na raiz do hub, um por máquina; tem ponto no nome, então não vai ao banco.', dono='Gustavo', aciona='camada de busca', le='camada de busca'),
   c('Ponte do Desktop', 'MCP local que liga o Claude Desktop à porta do banco pela rede privada.', dono='Gustavo', aciona='Claude Desktop')],
  lig=[('Agentes → Porta do banco → Banco local', 'Leitura com versão; gravação com a versão lida.', [(AC, 'guarda de versão')]),
       ('Agentes → Camada de busca', 'Pergunta → trecho certo, a cada busca.', []),
       ('Obsidian → Camada de busca', 'O Gustavo também busca no hub, pelo Obsidian (ou pedindo a um agente).', [(NV, 'como o Obsidian chega à busca do hub')]),
       ('Claude Desktop → Camada de busca', 'O Claude Desktop também usa a busca do hub.', [(D, 'por onde o Desktop chega à busca')]),
       ('Camada de busca → Vista Markdown', 'Indexa os arquivos quando o disco muda; cada máquina só enxerga o próprio disco.', [(NV, 'tempo de uma edição até a busca')]),
       ('Agentes → Vista Markdown', 'Gravação direto no disco: o sincronizador leva ao banco, sem conferir a versão.', [(D, 'se é o caminho padrão e como conferir a versão no disco')]),
       ('Cliente → Porta de leitura', 'Consultas por HTTP com token; nunca recebe a credencial do banco.', []),
       ('Claude Desktop → Ponte do Desktop → Porta do banco', 'Leitura.', [])]),
 'vigilancia': dict(nome='Vigilância', frase='Garantem que nada diverge em silêncio. O aviso nasce só na máquina que travou.',
  itens=[
   c('Vigia do sync', 'A cada 5 min confere a troca entre os bancos, os conflitos abertos, os binários descartados, os arquivos acima de 200 MiB, se o sincronizador está vivo e se o assistente do plugin travou; grava um estado curto e avisa quando piora.',
     [(D, 'quem percebe que ela parou e quem a religa'), (NV, 'onde o estado curto fica')],
     dono='Gustavo', aciona='Agendador do Windows', le='banco (estado das trocas), sincronizador, plugin, assistente'),
   c('Avisos', 'Três saídas da vigia: a notificação do Windows quando piora, o estado curto lido no início de sessão e o estado na tela do agente.',
     [(EC, 'na tela: barra de estado no Copilot; checagem e notificação no Codex')],
     dono='Gustavo', aciona='vigia', le='checagem de sessão (estado curto)', ve='Gustavo, agentes', tambem='Interfaces do Gustavo (a notificação)'),
   c('Mod de estado', 'Mostra o estado da vigia o tempo todo na sessão do Claude Code; avisa mesmo sem a checagem de início.',
     dono='Gustavo', aciona='vigia', ve='Gustavo e o agente, na sessão do Claude Code', tambem='Interfaces do Gustavo'),
   c('Recuperar binário', 'Recupera para um arquivo ao lado a versão de binário perdida numa colisão.', dono='Gustavo', aciona='um agente com o Gustavo vendo')],
  lig=[('Agendador do Windows → Vigia do sync', 'Dispara a vigia a cada 5 min.', []),
       ('Vigia do sync → Banco local, Sincronizador, plugin', 'Só confere: lê o estado, a cada 5 min; não age no banco.', []),
       ('Vigia do sync → Avisos, Mod de estado', 'Aviso de divergência: quando piora (notificação); sempre (mod).', [])]),
 'disciplina': dict(nome='Disciplina do agente', frase='Fazem o agente gravar no lugar certo, sem pedido. Agem dentro da sessão do agente.',
  itens=[
   c('Contrato', 'As regras do hub para os agentes (AGENTS.md na raiz), com o lugar de cada informação e a primeira instrução do maestro. O hub não tem CLAUDE.md.',
     [(D, 'onde fica o registro do aval'), (D, 'quem atualiza a cabeça do contrato nas instruções do MCP')],
     dono='Gustavo', aciona='ligações da ferramenta; a sessão ao abrir; um agente pode editá-lo só dentro do hub e com o aval do Gustavo',
     le='todo agente; cliente (o começo, pelas instruções do MCP)', aprova='Gustavo aprova toda mudança', tambem='Conteúdo'),
   c('Checagem de sessão', 'Hook no começo de toda sessão: lê o estado da vigia, informa a hora da última troca e abre a nota de retomada.',
     [(D, 'quem percebe se ela falhar'), (D, 'no Codex, em investigação'), (EC, 'no Copilot, o hook de usuário passou no teste')],
     dono='Gustavo', aciona='toda sessão de agente ao abrir', le='estado curto, nota de retomada', ve='agente', tambem='Vigilância'),
   c('Checkpoint', 'Ao fim de cada resposta, se a nota de retomada não reflete a resposta, ou se a memória privada ganhou algo que o hub não tem, obriga o agente a continuar e gravar. O hook não grava; o agente grava.',
     [(D, 'quem percebe se ele falhar; no Codex, em investigação'), (EC, 'no Copilot, hook de fim mais extensão experimental')],
     dono='Gustavo', aciona='o fim de cada resposta', le='nota de retomada, memória privada'),
   c('Ligações da ferramenta', 'A configuração global de cada ferramenta aponta para o contrato e para as skills (import, link simbólico, junction).',
     dono='Gustavo', aciona='kit de par', le='cada ferramenta ao abrir', aprova='Gustavo (são adaptadores)'),
   c('Guarda do acervo', 'No Claude Code, recusa a gravação no acervo, roda o verificador em outro modelo e só libera com relatório e aval do Gustavo. No Codex e no Copilot, recusa toda gravação no acervo.',
     [(NV, 'detalhes da guarda')], dono='Gustavo', aciona='tentativa de gravar no acervo', ve='Gustavo (o pedido de aval)', aprova='Gustavo, depois do verificador'),
   c('Verificador', 'Um modelo diferente que confere uma alteração no acervo.', [(D, 'qual modelo e quem o escolhe')], dono='Gustavo', aciona='guarda do acervo', le='a alteração proposta'),
   c('Hook de uso', 'Grava no registro de uso quem usou qual peça do acervo.', [(D, 'no Codex e no Copilot, depende de teste')], dono='Gustavo', aciona='o uso de uma peça'),
   c('Lembrete do maestro', 'Hook de início que só age em terminal do Maestri; lembra o agente de que é maestro e de onde está o acervo.',
     [(D, 'se age também em terminal de recruta')], dono='Gustavo', aciona='abertura de terminal do Maestri', ve='maestro')],
  lig=[('Contrato → Agentes', 'O contrato chega ao abrir a sessão, conforme a ferramenta e a porta de entrada.', []),
       ('Contrato → Maestro', 'Manda o maestro começar pela skill do acervo; o lembrete reforça.', []),
       ('Checkpoint → Agentes', 'A obrigação de gravar o que a resposta mudou e o que só a memória privada sabe. Ao fim de cada resposta.', []),
       ('Checkpoint → Nota de retomada', 'Só confere se a nota reflete a resposta; o hook não grava.', []),
       ('Agentes → Nota de retomada', 'Quem grava a nota é o agente da sessão, obrigado pelo checkpoint.', []),
       ('Maestro → Gustavo', 'O pedido de aval do acervo: a guarda recusa, o verificador confere, o Gustavo aprova.', []),
       ('Estado curto e nota de retomada → Checagem de sessão', 'Situação do sync e onde o trabalho parou, no início de toda sessão.', []),
       ('Agentes → Guarda do acervo → Acervo do maestro', 'Gravação liberada, recusada ou com aval (Claude Code); recusa e proposta (Codex, Copilot).', []),
       ('Hook de uso → Registro de uso', 'Quem usou qual peça, quando uma peça é usada.', [])]),
 'conteudo': dict(nome='Conteúdo', frase='O que mora dentro do hub: é o que o banco guarda e a vista mostra. Chega-se a ele pela busca.',
  itens=[
   c('Nota de retomada', 'Um arquivo curto por trabalho, sobrescrito, com sete campos; qualquer sessão continua de onde a outra parou.',
     dono='Gustavo; o que escrever é decisão do agente da sessão', aciona='agente da sessão, obrigado pelo checkpoint',
     le='checagem de sessão, qualquer sessão nova, Gustavo, clientes (leitura)', tambem='Disciplina do agente'),
   c('Acervo do maestro', 'Peças prontas para todo maestro, dentro ou fora do hub, como família de skills maestro-* em agents/skills/. Opções, não regras.',
     [(D, 'como o erro de uma peça citada que não existe mais chega ao Gustavo')],
     dono='Gustavo', aciona='maestro (acrescenta sozinho; altera com aval)', le='maestro, recrutas (os papéis)',
     aprova='Gustavo, para alterar ou apagar peça citada ou usada, ou mexer em catálogo ou descrição de skill', tambem='Disciplina do agente'),
   c('Raiz', 'Seis raízes, cada uma com comportamento próprio: clients/, operations/, initiatives/, reference/, agents/ e inbox/. O que termina vai para o _archive/ da própria raiz e fica 30 dias.',
     [(EC, 'níveis da árvore e perfil de cada máquina'), (D, 'quem confere os 30 dias do _archive/ e apaga'), (D, 'como algo volta do _archive/'), (D, 'proteção contra gravar dentro do _archive/'), (D, 'aviso de caminho mudado a quem guardava o caminho antigo')],
     dono='Gustavo', aciona='agentes e Gustavo gravam; o script move ao _archive/', le='todos os que leem o hub', aprova='Gustavo, para reescrita ou exclusão grande'),
   c('inbox/', 'Nota nova do Gustavo nasce sempre aqui; depois ele pede a um agente para padronizar e mover, ou absorver numa nota existente.', dono='Gustavo', aciona='Gustavo, agentes', le='checkpoint (triagem)'),
   c('Iniciativa', 'Frente de trabalho com identificador, estado e próxima ação; mora numa casa só.', dono='Gustavo decide que nasce e que termina', aciona='agentes trabalham nela', le='agentes, Gustavo, clientes (leitura)'),
   c('Núcleo da iniciativa e blocos', 'initiative.md, retomada.md, tasks.md, decisions.md, context.md e log/; blocos somados conforme o trabalho pede.',
     [(EC, 'arquitetura de pastas')], dono='Gustavo', aciona='agentes (a skill "nova iniciativa" cria; o agente da sessão mantém)', le='agentes, Gustavo, clientes (leitura)'),
   c('Catálogo de blocos e skill "nova iniciativa"', 'agents/blocks.md, citado pelo contrato, e a skill que cria pasta, núcleo e blocos por script; a skill só muda com supervisão e aprovação.',
     [(EC, 'arquitetura de pastas')], dono='Gustavo', aciona='agente cria a pasta pela skill', le='agentes', aprova='Gustavo, para mudar a skill'),
   c('Skills', 'Skills do hub, em agents/skills/.', [(D, 'roteamento de skills')], dono='Gustavo', aciona='agentes gravam skills novas; a família maestro-* passa pela guarda',
     le='cada ferramenta, pelas ligações', aprova='Gustavo, para mudar skill do acervo e a skill "nova iniciativa"', tambem='Disciplina do agente'),
   c('Variante e versão local', 'Variante: setup que declara a base e só o que muda. Versão local: ajuste de uma peça para uma iniciativa.', dono='Gustavo', aciona='maestro (sem aval)', le='maestro', tambem='Disciplina do agente'),
   c('Propostas', 'Onde o Codex e o Copilot deixam a mudança que queriam fazer no acervo.', dono='Gustavo', aciona='Codex e Copilot gravam', le='maestro no Claude Code avalia', tambem='Disciplina do agente'),
   c('Registro de uso', 'Um arquivo por máquina: peça, workspace, máquina, data.', dono='Gustavo', aciona='hook de uso', le='maestro', tambem='Disciplina do agente'),
   c('Segredos', 'Pasta .secrets/ dentro da iniciativa, fora do banco e do git.',
     [(D, 'teste que prove que um .secrets/ aninhado não chega ao banco nem ao GitHub; até lá, não está protegido'), (D, 'o que impede segredo em nota comum')],
     dono='Gustavo', aciona='Gustavo, agentes', le='agentes da máquina'),
   c('Pasta não replicada', 'Parte do hub numa máquina só, fora do sync. Hoje não há nenhuma.', [(D, 'mecanismo que a tira do sync')], dono='Gustavo', aciona='ninguém (nenhuma existe)')],
  lig=[('Maestro → Acervo do maestro', 'O maestro começa pelo acervo: lê o catálogo e escolhe setup e papéis.', []),
       ('Agentes → Nota de retomada', 'O agente da sessão grava a nota, obrigado pelo checkpoint.', []),
       ('Checkpoint → Nota de retomada', 'Só confere a nota ao fim de cada resposta; quem grava é o agente.', []),
       ('Codex, Copilot → Propostas → maestro', 'A mudança proposta, quando um maestro avalia.', [])]),
 'interfaces': dict(nome='Interfaces do Gustavo', frase='É por elas que o Gustavo vê, edita e é avisado. A notificação do Windows e o mod de estado também são daqui; estão na ficha da Vigilância.',
  itens=[
   c('Obsidian', 'Onde o Gustavo vê, edita, busca e resolve conflito; pode ficar fechado. O cofre é a raiz do hub. Aberto, o plugin também leva edições do disco ao banco e escreve no disco o que vem do banco.',
     [(D, 'o Obsidian do hub ao lado do cofre do vault')], dono='Gustavo', aciona='Gustavo (abre, fecha, edita, resolve conflito)', le='Gustavo; vigia (assistente travado)', tambem='Periferia do par'),
   c('Janela de conflito', 'Do plugin; abre com o Obsidian aberto, com faixa na nota e contador, nas duas máquinas.', [(AC, 'a tela de três vias editável, fork desta janela, logo depois da construção')],
     dono='Gustavo', aciona='Gustavo, ou um agente com ele vendo')],
  lig=[('Gustavo → Obsidian', 'Edição, criação (em inbox/), busca e resolução de conflito.', []),
       ('Obsidian → Vista Markdown', 'O Obsidian grava o .md no disco; o plugin ou o sincronizador leva ao banco.', []),
       ('Obsidian → Camada de busca', 'O Gustavo busca no hub pelo Obsidian.', [(NV, 'como o Obsidian chega à busca do hub')])]),
 'periferia': dict(nome='Periferia do par', frase='Estão no par, mas não guardam nem movem a verdade do dia a dia.',
  itens=[
   c('Agendador do Windows', 'O serviço do Windows que dispara tarefas sem ninguém pedir: o sincronizador no logon e a cada minuto, a vigia a cada 5 min, a cópia uma vez por dia.',
     dono='Gustavo', aciona='o logon e os intervalos'),
   c('Script do _archive/', 'Move uma pasta para o _archive/ da raiz depois de conferir que o outro par está em dia e sem edição recente.',
     dono='Gustavo', aciona='agente, quando o Gustavo pede para remover ou arquivar', le='estado do outro par', aprova='Gustavo (o pedido de remoção)', tambem='Disciplina do agente'),
   c('Cópia local (git) e cópia diária', 'O .git da raiz faz commit e push uma vez por dia, um ramo por máquina; nunca puxa nem escreve no disco do hub.',
     [(D, 'quem avisa quando a cópia diária falha'), (EC, 'papel de raiz para o Codex')], dono='Gustavo', aciona='Agendador do Windows'),
   c('Assistente do plugin', 'Abre depois de atualizar o plugin e para o sync daquele cofre até alguém responder.', dono='Gustavo', aciona='atualização do plugin', le='vigia', ve='Gustavo', aprova='Gustavo responde'),
   c('Nó da rede', 'Põe o par na rede privada (Tailscale, só no Windows). A chave do nó vence em 180 dias.', dono='Gustavo', aciona='pares, clientes', aprova='Gustavo dá chave a cliente'),
   c('Credenciais', 'Senha do banco, frase-senha, tokens das portas e chave do GitHub. Ficam na máquina, não no hub.', [(NV, 'arquivo exato')], dono='Gustavo', aciona='kit de par', le='banco, portas, sincronizador, plugin, git'),
   c('Kit de par', 'Script e configuração modelo que montam um par: rede, banco e portas, sincronizador, ligações, regras.',
     [(D, 'ordem completa de montagem')], dono='Gustavo', aciona='um agente com o Gustavo vendo; o Gustavo no que só ele consegue', tambem='Disciplina do agente')],
  lig=[('Agendador do Windows → Sincronizador', 'No logon e a cada minuto.', []),
       ('Agendador do Windows → Vigia do sync', 'A cada 5 min.', []),
       ('Cópia diária → Cópia no GitHub', 'Commit e push da vista, uma vez por dia.', [])]),
 'ferramentas': dict(nome='Ferramentas da máquina', frase='São da ferramenta, não do hub; cada máquina tem as suas.',
  itens=[
   c('Biblioteca do Maestri', 'Papéis e partituras no perfil do usuário (~/.maestri), fora do hub.', dono='Gustavo', aciona='app Maestri; maestro pela linha de comando do Maestri (cria e reescreve papéis)', le='Maestri, ao abrir terminais'),
   c('Pasta do papel', '.maestri/roles/<id>/ na pasta do workspace, com os arquivos do papel gravados pelo Maestri. Tem ponto: não replica.', dono='Gustavo', aciona='app Maestri', le='o agente do terminal'),
   c('Memória privada', 'A memória automática de cada ferramenta, no perfil do usuário. Não é o hub: o checkpoint leva ao hub o que só ela sabe.', [(NV, 'se outro agente a lê')],
     dono='Gustavo', aciona='a ferramenta', le='a mesma ferramenta, na mesma máquina'),
   c('Configuração de cada ferramenta', '~/.claude, ~/.codex, ~/.copilot e ~/.agents/skills: ligações para o contrato e as skills, MCP, hooks, mod.', dono='Gustavo', aciona='kit de par (monta)', le='cada ferramenta ao abrir')],
  lig=[('Maestro → Biblioteca do Maestri', 'Cria o papel global se falta, reescreve se difere do acervo, leva a versão local. Na hora de usar um papel.', []),
       ('Checkpoint → Memória privada', 'Confere se ela sabe algo que o hub não tem.', [])]),
 'fora': dict(nome='Fora do par', frase='Não fazem parte da cópia do hub. O outro par é a mesma cidade, do outro lado da rede privada; nenhum é a referência.',
  itens=[
   c('Rede privada', 'O único caminho entre pares e entre cliente e par; nunca exposta à internet.', [(D, 'nada detecta o Funnel ligado por engano')], dono='Gustavo', aciona='pares, clientes', aprova='Gustavo dá chave a cliente'),
   c('Outro par', 'A outra máquina, igual a esta: recebe as mudanças daqui e envia as dela. Cada par envia as suas.', dono='Gustavo', aciona='o banco dele envia; o daqui recebe'),
   c('Cópia no GitHub', 'Cópia de segurança diária da vista, um ramo por máquina; não é ponto de encontro do sync. Para recuperar o que foi apagado sem querer, dois dias de distância bastam.',
     dono='Gustavo', aciona='tarefa diária (push); para restaurar, um agente com o Gustavo vendo, ou ele, por comando', le='quem restaura'),
   c('Vault (referência)', 'Só referência: o agente pode ler, direto no disco; o hub não grava nada nele. Só existe no notebook.', dono='Gustavo', aciona='ninguém do hub grava nele', le='agentes, como referência'),
   c('Gateway de modelos', 'FreeLLMAPI, gateway de modelos gratuitos: só na máquina pessoal, preso à rede privada.', [(D, 'para onde vão as tarefas quando ele cai')], dono='Gustavo', aciona='agentes (roteamento), busca (Google, se ligado)'),
   c('Embeddings na nuvem', 'Segunda opção da busca por sentido, desligada. Ligada, o texto indexado vai ao Google. Conteúdo de cliente pode ir aos modelos na nuvem; nenhuma iniciativa vetada.',
     [(NV, 'se roda ao lado do índice local')], dono='Gustavo', aciona='busca, se ligado', aprova='Gustavo liga'),
   c('Rede da empresa', 'Risco: o software corporativo do notebook pode conflitar com o Tailscale.', [(D, 'o que acontece se a empresa bloquear')], dono='a empresa, fora do controle do Gustavo', aciona='a política da empresa')],
  lig=[('Banco local ↔ Outro par', 'Cada par envia as próprias mudanças ao outro, contínuo, pela rede privada; com a outra desligada, esperam.', [(NV, 'tempo pela rede; ordem de chegada depois de um corte')]),
       ('Agentes → Gateway de modelos', 'Tarefas simples, pelo roteamento.', []),
       ('Agentes → Vault (referência)', 'Leitura de referência, no notebook.', [])]),
 'gente': dict(nome='Quem chega ao hub', frase='Agem de fora dos bairros, pelas portas. O Gustavo é dono de toda a infraestrutura e de todo o conteúdo; operação é feita por um agente com ele vendo.',
  itens=[
   c('Gustavo', 'O dono do hub: vê e edita as notas, acha o que precisa, quer que os agentes guardem sozinhos o que importa e nunca perder trabalho em silêncio.',
     chega='Obsidian; pedindo a agentes; Claude Desktop', faz='o Obsidian (editar, buscar, resolver conflito); a vista pelo Explorador; abre as sessões; pede a agentes ler, alterar e remover',
     aprova='contrato, ligações da ferramenta, mudança em peça usada do acervo, remoção, porta de escrita do cliente, chave de cliente, embeddings do Google'),
   c('Agentes', 'Uma sessão de Claude Code, Codex ou Copilot, dentro ou fora do Maestri. O maestro, os recrutas e os subagentes são agentes.',
     [(D, 'como os agentes gravam: disco, porta do banco ou os dois')],
     chega='porta de entrada; porta do banco; camada de busca; disco', faz='porta do banco (ler e gravar), camada de busca, vista (disco), nota de retomada (obrigado pelo checkpoint), iniciativas, script do _archive/ quando o Gustavo pede'),
   c('Maestro', 'Um agente que orquestra um workspace do Maestri; começa pelo acervo do maestro.',
     chega='sessão do Maestri', faz='acervo do maestro (acrescenta sozinho; altera com aval), variante, versão local, biblioteca do Maestri; avalia propostas; recruta agentes'),
   c('Recruta', 'Um agente num terminal do Maestri, com papel.', [(D, 'outro caminho até o acervo, além da pasta do papel')], chega='terminal com papel, aberto na pasta do papel', faz='a parte dele do trabalho'),
   c('Subagente', 'Ajudante que roda dentro de um agente, sem ocupar terminal.', [(NV, 'se os hooks de sessão valem para ele')], chega='herda a sessão de quem o chamou'),
   c('Claude Desktop', 'O app Claude no Windows, usado pelo Gustavo; não é agente de código. Lê e usa a busca do hub.', [(D, 'por onde grava (gravar é requisito do Gustavo)')],
     chega='ponte local até a porta do banco; a busca do hub', faz='porta do banco (ler), camada de busca'),
   c('Cliente', 'Computador ou sandbox sem cópia do hub; só lê por padrão; precisa de um par ligado.', [(D, 'como escolhe o par; regra de rede da busca'), (D, 'dono do computador de passagem')],
     chega='rede privada até a porta de leitura de um par', faz='porta de leitura; busca; porta de escrita do cliente, se ligada', dono='Gustavo, para o acesso (chave e token)', tambem='Fora do par')],
  lig=[('Gustavo → Agentes', 'Pede: leia, altere, remova. O agente avisa o Gustavo quando algo falha.', []),
       ('Maestro → Gustavo', 'O maestro pede o aval para alterar ou apagar peça usada do acervo.', [])]),
}
QUEM = {r: (p, q) for g in G.values() for (r, p, q, s) in g['itens']}

COR = {  # fundo, traço, texto do nome do bairro
 'nucleo': ('#dcece5', '#3d8a76', '#1d5a4c'),
 'portas': ('#e0e7f4', '#4a6fae', '#2c4f8a'),
 'vigilancia': ('#f6e6c8', '#c08a2e', '#7a4b0a'),
 'disciplina': ('#ece2f1', '#8a62a0', '#5f3a74'),
 'conteudo': ('#f4e7d8', '#b07d4c', '#6f4722'),
 'periferia': ('#e9e7e2', '#8b857b', '#4f4a44'),
 'interfaces': ('#f7e3dc', '#c46a4a', '#8a3417'),
 'ferramentas': ('#e1eef0', '#4f8a96', '#2d5e68'),
 'fora': ('#e6ecf1', '#6d8396', '#3f5163'),
}

# ---------------------------------------------------------------- cenários (seção 8; as falhas ficam no último passo)
CENARIOS = [  # (texto, chaves, falha ou em aberto); a primeira chave recebe o número
 ('gustavo-edita', 'O Gustavo edita um arquivo', [
   ('O Gustavo abre a nota no Obsidian e edita.', ['Gustavo → Obsidian', 'Gustavo', 'Obsidian'], False),
   ('O Obsidian grava o .md no disco.', ['Obsidian → Vista Markdown', 'Vista Markdown'], False),
   ('O sincronizador (ou o plugin, se o Obsidian está aberto) leva ao banco.', ['Vista Markdown ↔ Sincronizador', 'Sincronizador', 'Sincronizador ↔ Banco local', 'Banco local'], False),
   ('O banco envia a mudança ao outro par, pela rede privada.', ['Banco local ↔ Outro par', 'Rede privada', 'Outro par'], False),
   ('Lá, o disco atualiza e a busca do outro par reindexa.', ['mini:nucleo', 'mini:portas', 'Outro par'], False),
   ('Se o mesmo trecho mudou lá antes da troca: colisão; a vigia avisa.', ['Vigia do sync', 'Vigia do sync → Banco local', 'Banco local'], True)]),
 ('agente-novo', 'Um agente novo abre sessão', [
   ('O Gustavo (ou o Maestri) abre a sessão numa porta de entrada.', ['Gustavo → Agentes', 'Gustavo', 'Agentes'], False),
   ('O contrato chega ao agente.', ['Contrato → Agentes', 'Contrato'], False),
   ('A checagem de sessão lê o estado da vigia e abre a nota de retomada.', ['Nota de retomada', 'Vigia do sync', 'Disciplina do agente'], False),
   ('O agente busca o trecho certo.', ['Agentes → Camada de busca', 'Camada de busca', 'Camada de busca → Vista Markdown', 'Vista Markdown'], False),
   ('Lê e grava pela porta do banco, levando a versão.', ['Agentes → Porta do banco', 'Porta do banco', 'Porta do banco → Banco local', 'Banco local'], False),
   ('Ao fim de cada resposta, o checkpoint cobra o agente e confere a nota; o agente a grava.', ['Agentes → Nota de retomada', 'Checkpoint → Agentes', 'Checkpoint → Nota de retomada', 'Checkpoint', 'Nota de retomada'], False)]),
 ('maestro-novo', 'Um maestro novo abre sessão', [
   ('Uma sessão do Maestri abre; o maestro chega.', ['Maestro'], False),
   ('O contrato (e o lembrete) o manda começar pelo acervo.', ['Contrato → Maestro', 'Contrato'], False),
   ('Lê o catálogo do acervo e escolhe setup e papéis.', ['Maestro → Acervo do maestro', 'Acervo do maestro'], False),
   ('Confere os papéis da biblioteca do Maestri; cria ou reescreve o que difere.', ['Biblioteca do Maestri', 'Maestro → Biblioteca do Maestri', 'Ferramentas da máquina'], False),
   ('O hook de uso registra cada peça usada, no registro de uso do acervo.', ['Acervo do maestro', 'Maestro → Acervo do maestro', 'Disciplina do agente'], False),
   ('Alterar peça usada: no Claude Code, a guarda recusa, o verificador confere e o Gustavo dá o aval.', ['Maestro → Gustavo', 'Gustavo', 'Disciplina do agente', 'Acervo do maestro'], False)]),
 ('pede-ler', 'O Gustavo pede a um agente: leia', [
   ('O Gustavo pede ao agente.', ['Gustavo → Agentes', 'Gustavo', 'Agentes'], False),
   ('O agente acha o trecho pela busca da máquina dele.', ['Agentes → Camada de busca', 'Camada de busca', 'Camada de busca → Vista Markdown', 'Vista Markdown'], False),
   ('Lê pela porta do banco: o texto e a versão.', ['Agentes → Porta do banco', 'Porta do banco', 'Porta do banco → Banco local', 'Banco local'], False),
   ('Se a nota está em conflito, a porta avisa e o agente avisa o Gustavo (a construir).', ['Porta do banco', 'Gustavo → Agentes', 'Gustavo'], True)]),
 ('pede-alterar', 'O Gustavo pede a um agente: altere', [
   ('O Gustavo pede ao agente.', ['Gustavo → Agentes', 'Gustavo', 'Agentes'], False),
   ('O agente lê a nota pela porta e guarda a versão.', ['Agentes → Porta do banco', 'Porta do banco'], False),
   ('Grava levando a versão; se mudou, vira conflito visível (a construir).', ['Porta do banco → Banco local', 'Banco local'], False),
   ('O sincronizador (ou o plugin) escreve no disco; a vista muda em cerca de 0,2 s.', ['Sincronizador ↔ Banco local', 'Sincronizador', 'Vista Markdown ↔ Sincronizador', 'Vista Markdown', 'Obsidian'], False),
   ('O banco envia ao outro par.', ['Banco local ↔ Outro par', 'Rede privada', 'Outro par'], False),
   ('O checkpoint cobra o agente e confere a nota de retomada; o agente a grava.', ['Agentes → Nota de retomada', 'Checkpoint → Agentes', 'Checkpoint → Nota de retomada', 'Checkpoint', 'Nota de retomada'], False),
   ('Em aberto: gravar direto no disco, sem conferir a versão.', ['Agentes → Vista Markdown', 'Vista Markdown'], True)]),
 ('pede-remover', 'O Gustavo pede a um agente: remova', [
   ('O Gustavo pede ("remova a nota X").', ['Gustavo → Agentes', 'Gustavo', 'Agentes'], False),
   ('O script do _archive/ confere se o outro par está em dia e sem edição recente.', ['Banco local ↔ Outro par', 'Outro par', 'Periferia do par'], False),
   ('Move a nota para o _archive/ da raiz; por onde o script grava está em aberto.', ['Agentes → Vista Markdown', 'Vista Markdown', 'Vista Markdown ↔ Sincronizador', 'Sincronizador', 'Sincronizador ↔ Banco local', 'Banco local'], False),
   ('As duas mudanças viajam ao outro par; a busca de cada máquina reindexa.', ['Banco local ↔ Outro par', 'Outro par', 'Camada de busca → Vista Markdown', 'Camada de busca'], False),
   ('Passados 30 dias sem pedido de volta, pode ser apagado. Quem confere: em aberto.', ['Conteúdo', 'Gustavo'], True)]),
 ('outro-par', 'O outro par altera um arquivo', [
   ('Algo muda no banco do outro par.', ['Outro par'], False),
   ('O banco dele envia ao banco daqui, pela rede privada.', ['Banco local ↔ Outro par', 'Rede privada', 'Banco local'], False),
   ('O sincronizador escreve no disco daqui.', ['Sincronizador ↔ Banco local', 'Sincronizador', 'Vista Markdown ↔ Sincronizador', 'Vista Markdown'], False),
   ('A busca daqui reindexa; o Obsidian aberto mostra.', ['Camada de busca → Vista Markdown', 'Camada de busca', 'Obsidian'], False),
   ('Se o mesmo trecho mudou aqui: colisão; a vigia avisa.', ['Vigia do sync', 'Vigia do sync → Banco local', 'Banco local'], True)]),
]
CEN = {}
for cid, _, passos in CENARIOS:
    for n, (_, chaves, _f) in enumerate(passos, 1):
        for k in chaves:
            CEN.setdefault(k, []).append(f'{cid}:{n}')
USADAS = set()
def cen(k):
    if k in CEN:
        USADAS.add(k)
        return f' data-cenario="{" ".join(CEN[k])}" data-chave="{esc(k)}"'
    return ''

# ---------------------------------------------------------------- peças de SVG
def t(x, y, s, cls='rot', anchor='start', extra=''):
    return f'<text x="{x}" y="{y}" class="{cls}" text-anchor="{anchor}"{extra}>{esc(s)}</text>'

def abre(cx, cy, gid):
    f, s, c_ = COR[gid]
    return (f'<g class="abre" aria-hidden="true"><circle cx="{cx}" cy="{cy}" r="8.5" fill="#fffdf8" stroke="{c_}" stroke-width="1.8"/>'
            f'<path d="M{cx-4},{cy} H{cx+4} M{cx},{cy-4} V{cy+4}" stroke="{c_}" stroke-width="1.8" stroke-linecap="round"/></g>')

def zona(gid, shape, label_xy, inner=''):
    f, s, c_ = COR[gid]
    nome = G[gid]['nome']
    lx, ly = label_xy
    return (f'<g class="bairro" data-grupo="{esc(nome)}" data-abre="{gid}"{cen(nome)} tabindex="0" role="button" '
            f'aria-label="Abrir a ficha: {esc(nome)}">'
            f'{shape.replace("/>", f" class=\"zona\" fill=\"{f}\" stroke=\"{s}\"/>", 1)}'
            f'<text x="{lx+22}" y="{ly}" class="grp" fill="{c_}">{esc(nome)}</text>{abre(lx + 8, ly - 5, gid)}'
            f'{inner}</g>')

def titulo(rot):
    p, q = QUEM[rot]
    extra = ''.join(f' {k}: {q[c_]}.' for c_, k in (('dono', 'Dono'), ('aciona', 'Quem aciona'), ('faz', 'Aciona')) if q.get(c_))
    return f'<title>{esc(rot)}: {esc(p)}{esc(extra)}</title>'

def item(rotulo, corpo):
    return f'<g class="item" data-item="{esc(rotulo)}"{cen(rotulo)}>{titulo(rotulo)}{corpo}</g>'

def marca2(x, y, gid):  # marca do segundo grupo (seção 5.1: aparece uma vez, com uma marca do segundo)
    f, s, c_ = COR[gid]
    return f'<circle cx="{x}" cy="{y}" r="6" fill="{s}" stroke="#fffdf8" stroke-width="2" class="marca2"><title>Também em: {esc(G[gid]["nome"])}</title></circle>'

def pessoa(rotulo, x, y):
    corpo = (f'<rect x="{x-17}" y="{y-25}" width="34" height="38" rx="10" class="anel"/>'
             f'<circle cx="{x}" cy="{y-15}" r="7" class="cabeca"/>'
             f'<path d="M{x-11},{y+8} Q{x-11},{y-6} {x},{y-6} Q{x+11},{y-6} {x+11},{y+8} Z" class="corpo"/>'
             + t(x - 24, y + 2, rotulo, 'rot pess', 'end'))
    return (f'<g class="item pessoa" data-item="{rotulo}" data-abre="gente"{cen(rotulo)} tabindex="0" role="button" '
            f'aria-label="Abrir a ficha: quem chega ao hub ({rotulo})">{titulo(rotulo)}{corpo}</g>')

def lig(de_para, d, cls, decidir=False):
    base = f'<path class="lig-fundo"{cen(de_para)} d="{d}"/>' if decidir else ''
    return base + f'<path data-ligacao="{esc(de_para)}"{cen(de_para)} class="lig {cls}" d="{d}"><title>{esc(de_para)}</title></path>'

def portao(x, y, h=30):  # abertura na muralha, sem nome
    return (f'<rect x="{x-7}" y="{y-h/2}" width="14" height="{h}" fill="#fbf8f1"/>'
            f'<rect x="{x-9}" y="{y-h/2-5}" width="18" height="5" rx="2" fill="#b9ad98"/><rect x="{x-9}" y="{y+h/2}" width="18" height="5" rx="2" fill="#b9ad98"/>')

DEFS = '''<defs>
<pattern id="hachura" width="7" height="7" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
<rect width="7" height="7" fill="#fffaf0"/><line x1="0" y1="0" x2="0" y2="7" stroke="#c9a640" stroke-width="2.4"/></pattern>
</defs>'''

def predio(x, y, w, h, gid):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="4" fill="#fffdf8" stroke="{COR[gid][1]}" stroke-width="2.5"/>'

def armazem(x, y, gid):
    s = COR[gid][1]
    ripas = ''.join(f'<line x1="{x+12}" y1="{y+33+i*5}" x2="{x+56}" y2="{y+33+i*5}" stroke="{s}" stroke-width="1.4"/>' for i in range(4))
    return (f'<path d="M{x-4},{y+52} V{y+16} Q{x+34},{y} {x+72},{y+16} V{y+52} Z" fill="#fffdf8" stroke="{s}" stroke-width="2.5" stroke-linejoin="round"/>'
            f'<rect x="{x+10}" y="{y+26}" width="48" height="26" fill="none" stroke="{s}" stroke-width="2.2"/>{ripas}')

def prefeitura(x, y, gid):
    s = COR[gid][1]
    cols = ''.join(f'<line x1="{x+10+i*10}" y1="{y+20}" x2="{x+10+i*10}" y2="{y+44}" stroke="{s}" stroke-width="2.5"/>' for i in range(4))
    return (f'<path d="M{x},{y+18} L{x+30},{y} L{x+60},{y+18} Z" fill="#fffdf8" stroke="{s}" stroke-width="2.5" stroke-linejoin="round"/>'
            f'{cols}<rect x="{x-2}" y="{y+44}" width="64" height="7" rx="2" fill="#fffdf8" stroke="{s}" stroke-width="2.5"/>')

def oficina(x, y, gid):
    s = COR[gid][1]
    return (f'<path d="M{x+4},{y+40} V{y+16} L{x+28},{y+2} L{x+52},{y+16} V{y+40} Z" fill="#fffdf8" stroke="{s}" stroke-width="2.5" stroke-linejoin="round"/>'
            f'<rect x="{x+12}" y="{y+24}" width="12" height="16" fill="none" stroke="{s}" stroke-width="2"/>'
            f'<rect x="{x+32}" y="{y+22}" width="12" height="9" fill="none" stroke="{s}" stroke-width="2"/>')

def cancela(x, y, gid):  # posto de fiscalização: poste e barra listrada
    s = COR[gid][1]
    listras = ''.join(f'<rect x="{x+10+i*14}" y="{y+6}" width="7" height="8" fill="{s}"/>' for i in range(4))
    return (f'<rect x="{x}" y="{y}" width="9" height="52" rx="2" fill="#fffdf8" stroke="{s}" stroke-width="2.5"/>'
            f'<rect x="{x+9}" y="{y+6}" width="58" height="8" rx="2" fill="#fffdf8" stroke="{s}" stroke-width="2"/>{listras}'
            f'<path d="M{x-6},{y+52} H{x+15}" stroke="{s}" stroke-width="3"/>')

def quadro(x, y, gid):  # quadro de recados sobre dois postes
    s = COR[gid][1]
    linhas = ''.join(f'<line x1="{x+8}" y1="{y+10+i*8}" x2="{x+42}" y2="{y+10+i*8}" stroke="{s}" stroke-width="1.6"/>' for i in range(4))
    return (f'<line x1="{x+10}" y1="{y+40}" x2="{x+10}" y2="{y+57}" stroke="{s}" stroke-width="3"/><line x1="{x+40}" y1="{y+40}" x2="{x+40}" y2="{y+57}" stroke="{s}" stroke-width="3"/>'
            f'<rect x="{x}" y="{y}" width="50" height="40" rx="3" fill="#fffdf8" stroke="{s}" stroke-width="2.5"/>{linhas}')

def relogio(cx, cy, gid):
    s = COR[gid][1]
    return (f'<circle cx="{cx}" cy="{cy}" r="17" fill="#fffdf8" stroke="{s}" stroke-width="3"/>'
            f'<path d="M{cx},{cy-10} V{cy} L{cx+7},{cy+5}" fill="none" stroke="#4f4a44" stroke-width="2.6" stroke-linecap="round"/>')

def caixa_ferramentas(x, y, gid):  # dois componentes sem rótulo: a configuração (caixa) e a biblioteca do Maestri (caderno de papéis)
    s = COR[gid][1]
    return (item('Configuração de cada ferramenta', f'<rect x="{x}" y="{y+12}" width="70" height="34" rx="4" fill="#fffdf8" stroke="{s}" stroke-width="2.2"/>'
            f'<path d="M{x+24},{y+12} V{y+4} H{x+46} V{y+12}" fill="none" stroke="{s}" stroke-width="2.2"/><line x1="{x}" y1="{y+24}" x2="{x+70}" y2="{y+24}" stroke="{s}" stroke-width="1.6"/>') +
            item('Biblioteca do Maestri', f'<rect x="{x+100}" y="{y+8}" width="34" height="38" rx="4" fill="#fffdf8" stroke="{s}" stroke-width="2.2"/><line x1="{x+106}" y1="{y+18}" x2="{x+128}" y2="{y+18}" stroke="{s}" stroke-width="1.6"/>'
            f'<line x1="{x+106}" y1="{y+26}" x2="{x+128}" y2="{y+26}" stroke="{s}" stroke-width="1.6"/><line x1="{x+106}" y1="{y+34}" x2="{x+122}" y2="{y+34}" stroke="{s}" stroke-width="1.6"/>'))

# quarteirões do par daqui (x, y, w, h, bairro), repetidos em miniatura no outro par
QA = [(215, 90, 205, 155, 'disciplina'), (450, 90, 435, 155, 'conteudo'), (160, 278, 220, 282, 'portas'), (410, 278, 280, 282, 'nucleo'),
      (720, 278, 165, 282, 'vigilancia'), (215, 604, 215, 131, 'interfaces'), (455, 604, 220, 131, 'ferramentas'), (700, 604, 185, 131, 'periferia')]

def cidade():
    mx, my = 190, 30
    muralha = (f'<rect x="{mx}" y="{my}" width="710" height="720" rx="26" class="muralha"/>'
               '<rect x="200" y="590" width="690" height="14" class="rua"/>'
               + portao(190, 66) + portao(190, 172, 46) + portao(190, 256) + portao(190, 670) + portao(900, 262))
    z = []
    z.append(zona('disciplina', '<rect x="215" y="90" width="205" height="155" rx="16"/>', (227, 118),
        inner=item('Contrato', prefeitura(228, 140, 'disciplina') + t(258, 222, 'Contrato', anchor='middle') + marca2(292, 146, 'conteudo')) +
              item('Checkpoint', cancela(340, 140, 'disciplina') + t(376, 222, 'Checkpoint', anchor='middle'))))
    z.append(zona('conteudo', '<rect x="450" y="90" width="435" height="155" rx="16"/>', (462, 118),
        inner=item('Nota de retomada', quadro(490, 134, 'conteudo') + t(552, 166, 'Nota de retomada') + marca2(542, 134, 'disciplina')) +
              item('Acervo do maestro', armazem(760, 138, 'conteudo') + t(794, 222, 'Acervo do maestro', anchor='middle') + marca2(836, 150, 'disciplina'))))
    z.append(zona('portas', '<rect x="160" y="278" width="220" height="282" rx="18"/>', (172, 306),
        inner=item('Porta do banco', '<rect x="172" y="354" width="36" height="52" rx="8" class="construir"/>'
                                     '<rect x="178" y="360" width="24" height="40" rx="6" class="portao"/>' + t(216, 350, 'Porta do banco')) +
              item('Camada de busca', '<rect x="176" y="460" width="28" height="50" rx="6" class="portao-busca"/>' + t(216, 446, 'Camada de busca'))))
    z.append(zona('nucleo', '<rect x="410" y="278" width="280" height="282" rx="16"/>', (422, 306),
        inner=item('Banco local', '<rect data-encontro="Banco local" x="470" y="356" width="205" height="48" rx="12" class="encontro cofre"/>' + t(572, 386, 'Banco local', anchor='middle')) +
              item('Vista Markdown', '<rect data-encontro="Vista Markdown" x="430" y="460" width="40" height="52" rx="5" class="vitrine"/>'
                                     '<rect x="436" y="468" width="28" height="22" fill="#e9f3ef" stroke="#3d8a76" stroke-width="1.5"/>' + t(448, 448, 'Vista Markdown')) +
              item('Sincronizador', predio(610, 471, 30, 30, 'nucleo') + '<path d="M617,486 h16 M625,478 v16" stroke="#3d8a76" stroke-width="2"/>' + t(680, 532, 'Sincronizador', anchor='end'))))
    z.append(zona('vigilancia', '<rect x="720" y="278" width="165" height="282" rx="16"/>', (732, 306),
        inner=item('Vigia do sync', t(802, 342, 'Vigia do sync', anchor='middle') +
                   '<path d="M782,368 L802,356 L822,368 Z" class="torre"/><rect x="786" y="368" width="32" height="22" class="torre"/>'
                   '<rect x="794" y="373" width="16" height="9" fill="#c08a2e"/>'
                   '<rect x="797" y="390" width="10" height="80" class="torre"/><path d="M788,470 H816" stroke="#c08a2e" stroke-width="3"/>')))
    z.append(zona('interfaces', '<rect x="215" y="604" width="215" height="131" rx="16"/>', (227, 722),
        inner=item('Obsidian', oficina(285, 645, 'interfaces') + t(349, 675, 'Obsidian') + marca2(340, 650, 'periferia'))))
    z.append(zona('ferramentas', '<rect x="455" y="604" width="220" height="131" rx="16"/>', (467, 632), inner=caixa_ferramentas(490, 660, 'ferramentas')))
    z.append(zona('periferia', '<rect x="700" y="604" width="185" height="131" rx="16"/>', (712, 722),
        inner=item('Agendador do Windows', relogio(800, 655, 'periferia'))))
    # o outro par: a mesma planta em miniatura, com a troca chegando ao cofre dele pela mesma altura
    k, ox = 0.24, 1022
    oy = 262 - (262 - my) * k
    X = lambda x: round(ox + (x - mx) * k, 1)
    Y = lambda y: round(oy + (y - my) * k, 1)
    mini = f'<rect x="{X(mx)}" y="{Y(my)}" width="{710*k:.1f}" height="{720*k:.1f}" rx="8" class="muralha fantasma"/>'
    mini += ''.join(f'<rect x="{X(x)}" y="{Y(y)}" width="{w*k:.1f}" height="{h*k:.1f}" rx="4" fill="{COR[g][1]}" fill-opacity=".3" stroke="{COR[g][1]}" stroke-opacity=".6" stroke-width="1.2" class="mini"{cen("mini:" + g)}/>'
                    for x, y, w, h, g in QA)
    cofre_b = f'<rect x="{X(470)}" y="{Y(356)}" width="{205*k:.1f}" height="{48*k:.1f}" rx="4" class="encontro fantasma"/>'
    estrada = ('<rect x="903" y="250" width="112" height="24" rx="4" class="via"/>' +
               ''.join(f'<line x1="{x}" y1="262" x2="{x+8}" y2="262" class="faixa"/>' for x in range(911, 1008, 18)))
    z.append(zona('fora', '<rect x="915" y="140" width="280" height="305" rx="22" stroke-dasharray="7 5"/>', (927, 168),
        inner=item('Rede privada', estrada + t(956, 302, 'Rede privada', anchor='middle')) + mini +
              item('Outro par', cofre_b + t(X(545), Y(720) + 27, 'Outro par', anchor='middle', cls='rot parb'))))
    gente = pessoa('Maestro', 100, 110) + pessoa('Agentes', 100, 380) + pessoa('Gustavo', 100, 670)
    L = [
        # agentes (azul): portas, busca, disco e a nota de retomada
        lig('Agentes → Porta do banco', 'M117,362 H138 L156,380 H178', 'agente'),
        lig('Porta do banco → Banco local', 'M202,380 H470', 'agente'),
        lig('Agentes → Vista Markdown', 'M117,377 H128 L151,414 H420 V466 H430', 'agente disco', decidir=True),
        lig('Agentes → Camada de busca', 'M117,390 H122 L170,485 H176', 'agente busca'),
        lig('Camada de busca → Vista Markdown', 'M204,485 H430', 'agente busca'),
        lig('Agentes → Nota de retomada', 'M117,354 L140,340 V256 H515 V193', 'agente'),
        # o disco e o banco, nos dois sentidos
        lig('Vista Markdown ↔ Sincronizador', 'M470,486 H610', 'sinc'),
        lig('Sincronizador ↔ Banco local', 'M625,471 V404', 'sinc'),
        # Gustavo
        lig('Gustavo → Obsidian', 'M117,670 H289', 'gustavo'),
        lig('Obsidian → Vista Markdown', 'M313,647 V597 H450 V512', 'gustavo'),
        lig('Obsidian → Camada de busca', 'M289,655 H250 V535 H190 V510', 'gustavo'),
        lig('Gustavo → Agentes', 'M100,645 V393', 'gustavo'),
        # regras: o contrato chega ao maestro e aos agentes
        lig('Contrato → Maestro', 'M228,157 H100 V123', 'disc'),
        lig('Contrato → Agentes', 'M226,188 H95 V355', 'disc'),
        # confere (só lê): o checkpoint e a vigia
        lig('Checkpoint → Nota de retomada', 'M407,150 H490', 'confere'),
        lig('Vigia do sync → Banco local', 'M786,379 H675', 'confere'),
        # maestro
        lig('Maestro → Acervo do maestro', 'M117,100 H150 V66 H794 V140', 'maestro'),
        # agendador
        lig('Agendador do Windows → Sincronizador', 'M783,655 H705 V486 H640', 'agendador'),
        lig('Agendador do Windows → Vigia do sync', 'M800,638 V472', 'agendador'),
        # troca entre pares, nos dois sentidos
        lig('Banco local ↔ Outro par', f'M655,356 V262 H{X(655)} V{Y(356)}', 'trocar'),
        # só no cenário: correm por fora, sem cruzar nada
        lig('Maestro → Biblioteca do Maestri', 'M108,85 V16 H1197 V766 H607 V706', 'maestro so-cen'),
        lig('Maestro → Gustavo', 'M92,85 V40 H8 V648 H85', 'maestro so-cen'),
        lig('Checkpoint → Agentes', 'M340,185 H312 V238 H107 V355', 'disc so-cen'),
    ]
    return muralha + ''.join(z) + ''.join(L) + gente

# ---------------------------------------------------------------- página
CSS = r'''
:root{--papel:#f6f1e7;--tinta:#2b2622;--suave:#4a433c;--linha:#d9cfbf;--cartao:#fffcf6;
--agente:#2a62a8;--gustavo:#b8462a;--maestro:#0d7480;--disc:#6f4f92;--agendador:#8a6a3a;--confere:#4a433c;--trocar:#3f5a74;--sinc:#3d8a76;--falha:#b3261e}
*{box-sizing:border-box}
html,body{margin:0;background:var(--papel);color:var(--tinta);font-family:"Segoe UI",system-ui,-apple-system,Roboto,sans-serif}
header{padding:14px 24px 4px;display:flex;flex-wrap:wrap;gap:6px 22px;align-items:baseline}
h1{font-family:Georgia,"Times New Roman",serif;font-size:26px;margin:0;font-weight:700}
.ideia{margin:0;color:var(--suave);font-size:15px;max-width:76ch}
.legendas{padding:0 24px 6px}
.legenda{display:flex;flex-wrap:wrap;gap:4px 16px;padding:0;font-size:13px;color:var(--suave);list-style:none;margin:0 0 3px}
.legenda .tit{font-weight:700;color:var(--tinta);text-transform:uppercase;letter-spacing:.04em;font-size:12px;min-width:92px}
.legenda .sw-conf{height:0;border-top:3px dashed var(--confere);border-radius:0;background:none}
.legenda li{display:flex;align-items:center;gap:6px}
.legenda i{display:inline-block;width:24px;height:5px;border-radius:3px}
.legenda .sw-sinc{height:0;border-top:4px dotted var(--sinc);border-radius:0;background:none}
.legenda .sw-dec{width:24px;height:9px;border-radius:2px;background:repeating-linear-gradient(90deg,var(--agente) 0 6px,transparent 6px 11px),#f8ecbd}
.legenda .sw-cons{width:16px;height:14px;border:2px dashed var(--tinta);border-radius:4px;background:none}
.legenda .sw-m2{width:12px;height:12px;border-radius:50%;background:#8a62a0;border:2px solid #fffdf8;box-shadow:0 0 0 1px #8a62a0}
.ico-abre{display:inline-block;position:relative;width:17px;height:17px;border:1.6px solid var(--tinta);border-radius:50%;background:#fffdf8}
.ico-abre::before,.ico-abre::after{content:"";position:absolute;left:50%;top:50%;background:var(--tinta);transform:translate(-50%,-50%)}
.ico-abre::before{width:8px;height:1.6px}.ico-abre::after{width:1.6px;height:8px}
.legenda .dica-abre{color:var(--tinta);font-weight:600}
.cenarios{padding:4px 24px 4px}
.cen-botoes{display:flex;flex-wrap:wrap;gap:6px;align-items:center}
.cen-botoes .rot-cen{font-size:13px;font-weight:700;color:var(--suave);margin-right:4px;letter-spacing:.04em;text-transform:uppercase}
.cen-botoes button,.cen-passo button{font:inherit;font-size:14px;border:1px solid var(--linha);background:var(--cartao);color:var(--tinta);border-radius:999px;padding:6px 12px;cursor:pointer}
.cen-botoes button[aria-pressed="true"]{background:var(--tinta);color:#fff;border-color:var(--tinta)}
.cen-botoes button:focus-visible,.cen-passo button:focus-visible,.lista-bairros button:focus-visible,#fechar:focus-visible{outline:3px solid var(--tinta);outline-offset:2px}
body.cen .legendas,body.cen .cen-botoes{display:none}
.cen-passo{position:sticky;top:0;z-index:3;display:flex;flex-wrap:wrap;gap:8px 12px;align-items:center;margin-top:8px;padding:8px 12px;border:1px solid var(--linha);border-radius:12px;background:var(--cartao);min-height:46px}
.cen-passo[hidden]{display:none}
.cen-n{font-weight:700;font-size:14px}
.cen-n .nome{display:block;font-weight:600;color:var(--suave);font-size:13px}
.cen-txt{font-size:16px;flex:1 1 260px}
.moldura{position:relative}
.palco{padding:0 16px 0;overflow-x:auto}
svg.cidade{display:block;width:100%;max-width:1240px;height:auto;margin:0 auto}
.rot{font-size:15px;font-weight:600;fill:var(--tinta)}
.grp{font-size:14px;font-weight:650;letter-spacing:.02em}
.parb{font-size:17px;fill:#3f5163}
.zona{stroke-width:1.6}
.bairro{cursor:pointer;outline:none}
.bairro .item{pointer-events:bounding-box}
.bairro:hover>.zona,.bairro:focus-visible>.zona{stroke:var(--tinta);stroke-width:3.5}
.bairro:hover>.abre circle,.bairro:focus-visible>.abre circle{fill:var(--tinta)}
.bairro:hover>.abre path,.bairro:focus-visible>.abre path{stroke:#fff}
.anel{fill:transparent;stroke:transparent;stroke-width:2.5}
.pessoa:hover .anel,.pessoa:focus-visible .anel{fill:#fff2bf;stroke:var(--tinta)}
.pessoa{cursor:pointer;outline:none}
.cabeca,.corpo{fill:var(--tinta);stroke:var(--tinta);stroke-width:1}
.pess{font-weight:700}
.lig{fill:none;stroke-linecap:round;stroke-linejoin:round;stroke-width:5}
.lig.agente{stroke:var(--agente);stroke-width:6}
.lig.agente.busca{stroke-width:10}
.lig.agente.disco{stroke-width:5;stroke-dasharray:9 7}
.lig-fundo{fill:none;stroke:#f8ecbd;stroke-width:9;stroke-linecap:round;stroke-linejoin:round}
body.cen .lig-fundo.aceso{stroke:#f3dc8a;stroke-width:14}
.lig.gustavo{stroke:var(--gustavo)}
.lig.maestro{stroke:var(--maestro);stroke-width:4.5}
.lig.disc{stroke:var(--disc);stroke-width:4}
.lig.agendador{stroke:var(--agendador);stroke-width:4}
.lig.confere{stroke:var(--confere);stroke-width:3;stroke-dasharray:10 4 2 4}
.lig.so-cen{display:none;stroke-width:3.5}
body.cen .lig.so-cen.aceso{display:inline}
.lig.trocar{stroke:var(--trocar);stroke-width:6}
.lig.sinc{stroke:var(--sinc);stroke-width:4;stroke-dasharray:1 7}
.encontro{fill:#fff;stroke:var(--tinta);stroke-width:3.5}
.encontro.fantasma{fill:#f3f5f7;stroke:#6d8396;stroke-dasharray:5 4;stroke-width:2}
.cofre{stroke-width:4.5}
.vitrine{fill:#fffdf8;stroke:#3d8a76;stroke-width:3}
.via{fill:#cfd8e0;stroke:#6d8396;stroke-width:1.5}
.faixa{stroke:#fff;stroke-width:2.5}
.muralha{fill:#fbf8f1;stroke:#b9ad98;stroke-width:6}
.muralha.fantasma{fill:#f2f4f6;stroke:#a9b6c2;stroke-width:2.5;stroke-dasharray:7 4}
.rua{fill:#ece4d4}
.portao{fill:#fffdf8;stroke:var(--agente);stroke-width:3}
.portao-busca{fill:#fffdf8;stroke:var(--agente);stroke-width:4}
.construir{fill:none;stroke:var(--tinta);stroke-width:2;stroke-dasharray:5 4}
.torre{fill:#fffdf8;stroke:#c08a2e;stroke-width:2.5}
/* cenário: o resto apaga, o caminho acende */
body.cen .lig,body.cen .lig-fundo{opacity:.1}
body.cen .item{opacity:.22}
body.cen .bairro>.zona,body.cen .bairro>.grp,body.cen .bairro>.abre{opacity:.4}
body.cen .bairro>g[aria-hidden]:not(.abre){opacity:.3}
body.cen .bairro.aceso>g[aria-hidden]{opacity:.75}
body.cen .lig.aceso,body.cen .item.aceso{opacity:1}
body.cen .mini{opacity:.35}body.cen .mini.aceso{opacity:1;stroke-opacity:1;stroke-width:2.5}
body.cen .bairro.aceso>.zona,body.cen .bairro.aceso>.grp,body.cen .bairro.aceso>.abre{opacity:1}
body.cen .lig.agora{stroke-width:9;filter:drop-shadow(0 0 3px rgba(43,38,34,.45))}
body.cen .lig.agente.busca.agora{stroke-width:13}
body.cen .bairro.agora>.zona{stroke:var(--tinta);stroke-width:4}
body.cen .item.agora{filter:drop-shadow(0 0 4px rgba(43,38,34,.55))}
.marca-passo circle{fill:#fffdf8;stroke:var(--tinta);stroke-width:2}
.marca-passo text{font-size:13px;font-weight:800;fill:var(--tinta)}
.marca-passo.agora circle{fill:var(--tinta)}.marca-passo.agora text{fill:#fff}
.marca-passo polygon{fill:#fff;stroke:var(--falha);stroke-width:2.5;stroke-linejoin:round}
.marca-passo.falha text{fill:var(--falha)}.marca-passo.falha.agora polygon{fill:var(--falha)}.marca-passo.falha.agora text{fill:#fff}
body.cen .lig.aceso.falha{stroke:var(--falha);stroke-dasharray:8 5}
body.cen .item.aceso.falha{filter:drop-shadow(0 0 2px var(--falha)) drop-shadow(0 0 5px var(--falha))}
body.cen .bairro.aceso.falha>.zona{stroke:var(--falha);stroke-width:4;stroke-dasharray:9 5}
@media (min-width:761px){body.cen svg.cidade{max-height:calc(100vh - 150px)}}
#ficha{position:fixed;top:0;right:0;height:100%;width:min(440px,100%);background:var(--cartao);border-left:1px solid var(--linha);
box-shadow:-8px 0 24px rgba(60,40,20,.12);padding:22px 22px 30px;overflow-y:auto;display:none;z-index:5}
#ficha.aberta{display:block}
#ficha h2{font-family:Georgia,serif;font-size:22px;margin:0 0 6px;padding-right:70px}
#ficha .frase{color:var(--suave);margin:0 0 16px;font-size:15px;line-height:1.45}
#ficha ul{list-style:none;margin:0;padding:0}
#ficha li{padding:10px 0;border-top:1px solid var(--linha);font-size:15px;line-height:1.45}
#ficha li.alvo{background:#ffe9a8;box-shadow:-10px 0 0 #ffe9a8,10px 0 0 #ffe9a8;transition:background 1s,box-shadow 1s}
#ficha li.alvo.apaga{background:#fff6d6;box-shadow:-10px 0 0 #fff6d6,10px 0 0 #fff6d6}
#ficha li b{display:block;font-size:16px}
#ficha dl{display:grid;grid-template-columns:max-content 1fr;gap:2px 10px;margin:6px 0 0;font-size:14px}
#ficha dt{font-weight:700;color:var(--suave)}#ficha dd{margin:0}
#ficha h3{font-size:13px;letter-spacing:.06em;text-transform:uppercase;color:var(--suave);margin:20px 0 4px}
#ficha .sel{display:block;width:fit-content;margin-top:5px;background:#fff2bf;border:1px dashed #a07800;color:#5e4600;border-radius:9px;padding:1px 8px;font-size:13px;font-weight:600}
#ficha .sel.nv{background:#eef1f4;border-color:#6d8396;color:#33414f}
#ficha .sel.ac{background:#fff;border-color:var(--tinta);color:var(--tinta)}
#ficha .sel.ec{background:#e6f1ec;border-color:#3d8a76;color:#1d5a4c}
#fechar{position:absolute;top:12px;right:12px;border:1px solid var(--linha);background:#fff;border-radius:8px;padding:6px 10px;font:inherit;font-size:14px;cursor:pointer}
.lista-bairros{display:none;padding:0 16px 24px;margin:0;list-style:none}
.lista-bairros button{width:100%;text-align:left;margin:4px 0;padding:10px 12px;border:1px solid var(--linha);border-radius:10px;background:var(--cartao);font:inherit;font-size:15px;color:var(--tinta);cursor:pointer}
.dica{display:none;padding:0 16px;font-size:13px;color:var(--suave);margin:0 0 4px}
@media (max-width:760px){
 header{display:block;padding:12px 16px 4px}h1{font-size:22px}.ideia{max-width:none;overflow-wrap:anywhere}.legenda{padding:0 16px 6px;gap:4px 10px}
 .cenarios{padding:4px 16px 8px}
 svg.cidade{width:900px;max-width:none}
 .lista-bairros,.dica{display:block}
 .moldura::before,.moldura::after{content:"";position:absolute;top:0;bottom:12px;width:28px;pointer-events:none;z-index:1}
 .moldura::before{left:0;background:linear-gradient(90deg,var(--papel),rgba(246,241,231,0))}
 .moldura::after{right:0;background:linear-gradient(270deg,var(--papel),rgba(246,241,231,0))}
}
'''

JS = r'''
(function(){
var G=__DADOS__,C=__CEN__;
var NS='http://www.w3.org/2000/svg';
var f=document.getElementById('ficha'),volta=null;
function el(t,c,x){var e=document.createElement(t);if(c)e.className=c;if(x!=null)e.textContent=x;return e}
var CLS={'a decidir':'','não verificado':' nv','a construir':' ac','em curso':' ec'};
function selos(li,ss){ss.forEach(function(s){li.appendChild(el('span','sel'+(CLS[s[0]]||''),s[0]+': '+s[1]))})}
var CAMPOS=[['dono','Dono'],['chega','Por onde chega'],['faz','O que aciona'],['aciona','Quem aciona'],['le','Quem lê'],['ve','Só vê'],['aprova','Aprova'],['tambem','Também em']];
function abrir(id,origem,alvo){var g=G[id];if(!g)return;volta=origem||null;
 var c=document.getElementById('ficha-corpo');c.textContent='';
 c.appendChild(el('h2',null,g.nome));c.appendChild(el('p','frase',g.frase));
 c.appendChild(el('h3',null,id==='gente'?'Quem':'Componentes'));
 var ul=el('ul'),marcado=null;g.itens.forEach(function(i){var li=el('li');li.appendChild(el('b',null,i[0]));li.appendChild(document.createTextNode(i[1]));
  var dl=el('dl');CAMPOS.forEach(function(k){if(i[2][k[0]]){dl.appendChild(el('dt',null,k[1]));dl.appendChild(el('dd',null,i[2][k[0]]))}});
  if(dl.childNodes.length)li.appendChild(dl);selos(li,i[3]);if(alvo&&i[0]===alvo){li.className='alvo';marcado=li}ul.appendChild(li)});c.appendChild(ul);
 if(g.lig.length){c.appendChild(el('h3',null,'Ligações'));var u2=el('ul');g.lig.forEach(function(l){var li=el('li');li.appendChild(el('b',null,l[0]));li.appendChild(document.createTextNode(l[1]));selos(li,l[2]);u2.appendChild(li)});c.appendChild(u2)}
 f.classList.add('aberta');document.getElementById('fechar').focus({preventScroll:true});f.scrollTop=0;
 if(marcado){f.scrollTop=Math.max(0,marcado.offsetTop-80);setTimeout(function(){marcado.classList.add('apaga')},1200)}}
function fechar(){f.classList.remove('aberta');if(volta)volta.focus()}
document.querySelectorAll('[data-abre]').forEach(function(e){
 function vai(ev){var it=ev.target.closest&&ev.target.closest('[data-item]');abrir(e.getAttribute('data-abre'),e,it?it.getAttribute('data-item'):null)}
 e.addEventListener('click',function(ev){ev.stopPropagation();vai(ev)});
 e.addEventListener('keydown',function(ev){if(ev.key==='Enter'||ev.key===' '){ev.preventDefault();ev.stopPropagation();vai(ev)}})});
document.getElementById('fechar').addEventListener('click',fechar);
// cenários: acende o caminho passo a passo
var svg=document.querySelector('svg.cidade'),marcas=document.createElementNS(NS,'g');marcas.setAttribute('aria-hidden','true');svg.appendChild(marcas);
var botoes=document.querySelectorAll('[data-cen]'),painel=document.getElementById('cen-passo'),atual=null,passo=0;
var todos=document.querySelectorAll('[data-cenario]');
function noPasso(e,id,n){return (' '+e.getAttribute('data-cenario')+' ').indexOf(' '+id+':'+n+' ')>=0}
function chave(e){return e.getAttribute('data-chave')}
// caixas dos textos do desenho: o número do passo fica a 6 px de qualquer nome
function textos(){var r=[];svg.querySelectorAll('text').forEach(function(t){if(marcas.contains(t))return;var b=t.getBBox();r.push([b.x,b.y,b.x+b.width,b.y+b.height])});return r}
function livre(x,y,caixas){var R=17;if(x<18||x>1182||y<18||y>762)return false;return caixas.every(function(b){return x+R<b[0]||x-R>b[2]||y+R<b[1]||y-R>b[3]})}
function forma(e){if(e.tagName!=='g')return e.getBBox();var x1=1e9,y1=1e9,x2=-1e9,y2=-1e9;
 Array.prototype.forEach.call(e.children,function(k){if(/^(text|title)$/.test(k.tagName)||k.classList.contains('alvo-clique'))return;var b=k.getBBox();if(!b.width&&!b.height)return;
  x1=Math.min(x1,b.x);y1=Math.min(y1,b.y);x2=Math.max(x2,b.x+b.width);y2=Math.max(y2,b.y+b.height)});
 return x1<1e9?{x:x1,y:y1,width:x2-x1,height:y2-y1}:e.getBBox()}
function candidatos(e){var c=[];if(e.tagName==='path'){var L=e.getTotalLength();[.5,.35,.65,.2,.8].forEach(function(q){var p=e.getPointAtLength(L*q),p2=e.getPointAtLength(Math.min(L,L*q+2));
  var dx=p2.x-p.x,dy=p2.y-p.y,n=Math.hypot(dx,dy)||1;c.push([p.x-dy/n*16,p.y+dx/n*16]);c.push([p.x+dy/n*16,p.y-dx/n*16])});return c}
 var b=e.getBBox();if(e.classList.contains('bairro'))return [[b.x+b.width-20,b.y+b.height-20],[b.x+20,b.y+b.height-20],[b.x+b.width-20,b.y+20]];
 b=forma(e);[14,26].forEach(function(d){c.push([b.x-d,b.y-d+2],[b.x+b.width+d,b.y-d+2],[b.x+b.width/2,b.y-d-2],[b.x-d-2,b.y+b.height/2],[b.x+b.width+d+2,b.y+b.height/2],[b.x-d,b.y+b.height+d-2],[b.x+b.width+d,b.y+b.height+d-2],[b.x+b.width/2,b.y+b.height+d+2])});return c}
// sem lugar livre perto: o número encosta no próprio componente, no canto mais longe do nome
function encosta(e){var b=forma(e),t=e.querySelector&&e.querySelector(':scope>text'),cx=b.x+b.width/2,cy=b.y+b.height/2;
 if(e.tagName==='path'){var L=e.getTotalLength(),q=e.getPointAtLength(L/2);return [q.x,q.y-12]}
 var tb=t?t.getBBox():{x:cx,y:cy+1,width:0,height:0},tx=tb.x+tb.width/2,ty=tb.y+tb.height/2;
 return [tx>cx?b.x+4:b.x+b.width-4,ty>cy?b.y+4:b.y+b.height-4]}
function marca(p,n,agora,falha){var g=document.createElementNS(NS,'g');g.setAttribute('class','marca-passo'+(agora?' agora':'')+(falha?' falha':''));
 var f1;if(falha){f1=document.createElementNS(NS,'polygon');f1.setAttribute('points',(p[0])+','+(p[1]-15)+' '+(p[0]+14)+','+(p[1]+10)+' '+(p[0]-14)+','+(p[1]+10))}
 else{f1=document.createElementNS(NS,'circle');f1.setAttribute('cx',p[0]);f1.setAttribute('cy',p[1]);f1.setAttribute('r',11)}
 var tx=document.createElementNS(NS,'text');tx.setAttribute('x',p[0]);tx.setAttribute('y',p[1]+(falha?7:4.5));tx.setAttribute('text-anchor','middle');tx.textContent=n;
 g.appendChild(f1);g.appendChild(tx);marcas.appendChild(g);return g}
function desenhar(){
 todos.forEach(function(e){e.classList.remove('aceso','agora','falha')});marcas.textContent='';
 if(!atual){document.body.classList.remove('cen');painel.hidden=true;botoes.forEach(function(b){b.setAttribute('aria-pressed','false')});return}
 var cen=C[atual],N=cen.passos.length;document.body.classList.add('cen');painel.hidden=false;
 for(var n=1;n<=passo;n++){var fl=cen.passos[n-1][2];
  todos.forEach(function(e){if(noPasso(e,atual,n)){e.classList.add('aceso');if(n===passo)e.classList.add('agora');if(fl)e.classList.add('falha')}})}
 var caixas=textos(),ultima=null;
 for(var n=1;n<=passo;n++){var ch=cen.passos[n-1][1][0],alvo=null;
  todos.forEach(function(e){if(!alvo&&noPasso(e,atual,n)&&chave(e)===ch&&!e.classList.contains('lig-fundo'))alvo=e});
  if(!alvo)continue;var cs=candidatos(alvo),p=null;for(var i=0;i<cs.length;i++){if(livre(cs[i][0],cs[i][1],caixas)){p=cs[i];break}}p=p||encosta(alvo);
  ultima=marca(p,n,n===passo,cen.passos[n-1][2]);caixas.push([p[0]-11,p[1]-11,p[0]+11,p[1]+11])}
 document.getElementById('cen-nome').textContent=cen.nome;
 document.getElementById('cen-num').textContent='Passo '+passo+' de '+N+(cen.passos[passo-1][2]?' · falha ou em aberto':'');
 document.getElementById('cen-txt').textContent=cen.passos[passo-1][0];
 document.getElementById('cen-ant').disabled=passo<=1;document.getElementById('cen-prox').disabled=passo>=N;
 botoes.forEach(function(b){b.setAttribute('aria-pressed',b.getAttribute('data-cen')===atual?'true':'false')});
 // a faixa do desenho e a página seguem o passo atual (tela estreita ou baixa)
 if(ultima){var pal=document.querySelector('.palco'),rb=ultima.getBoundingClientRect(),rp=pal.getBoundingClientRect();
  if(rb.left<rp.left+20||rb.right>rp.right-20)pal.scrollLeft+=rb.left-rp.left-rp.width/2;
  var topo=painel.getBoundingClientRect().bottom;if(rb.top<topo+10||rb.bottom>window.innerHeight-10)window.scrollBy(0,rb.top-(topo+window.innerHeight)/2)}}
function sair(){var b=document.querySelector('[data-cen="'+atual+'"]');atual=null;desenhar();if(b)b.focus()}
botoes.forEach(function(b){b.addEventListener('click',function(){atual=b.getAttribute('data-cen');passo=1;desenhar();document.getElementById('cen-prox').focus()})});
document.getElementById('cen-ant').addEventListener('click',function(){if(passo>1){passo--;desenhar()}});
document.getElementById('cen-prox').addEventListener('click',function(){if(atual&&passo<C[atual].passos.length){passo++;desenhar()}});
document.getElementById('cen-sair').addEventListener('click',sair);
document.addEventListener('keydown',function(ev){
 if(ev.key==='Escape'){if(f.classList.contains('aberta'))fechar();else if(atual)sair()}
 if(atual&&!f.classList.contains('aberta')){
  if(ev.key==='ArrowRight'&&passo<C[atual].passos.length){passo++;desenhar()}
  if(ev.key==='ArrowLeft'&&passo>1){passo--;desenhar()}}});
// tela estreita: a faixa abre já centrada no Banco local
function centrar(){var p=document.querySelector('.palco'),b=document.querySelector('[data-item="Banco local"]');
 if(!p||!b||p.scrollWidth<=p.clientWidth+1)return;var rp=p.getBoundingClientRect(),rb=b.getBoundingClientRect();
 p.scrollLeft=Math.max(0,p.scrollLeft+rb.left-rp.left-(rp.width-rb.width)/2)}
if(document.readyState==='complete')centrar();else window.addEventListener('load',centrar);
})();
'''

LEGENDA = '''<div class="legendas">
<ul class="legenda" aria-label="Quem aciona: a linha sai da pessoa">
<li class="tit">Quem aciona</li>
<li><i style="background:var(--agente);height:8px"></i>agentes (a mais grossa: buscar)</li>
<li><i style="background:var(--gustavo)"></i>Gustavo</li>
<li><i style="background:var(--maestro)"></i>maestro</li>
<li><i class="sw-m2"></i>também em outro grupo</li>
<li class="dica-abre"><span class="ico-abre" aria-hidden="true"></span>cada bairro abre uma ficha: dono, quem aciona, quem lê</li>
</ul>
<ul class="legenda" aria-label="O que corre entre os componentes">
<li class="tit">O que corre</li>
<li><i style="background:var(--disc)"></i>regras (contrato)</li>
<li><i style="background:var(--agendador)"></i>Agendador (o relógio)</li>
<li><i class="sw-conf"></i>confere, só lê</li>
<li><i class="sw-sinc"></i>disco e banco</li>
<li><i style="background:var(--trocar)"></i>troca entre pares</li>
<li><i class="sw-dec"></i>a decidir</li>
<li><i class="sw-cons"></i>a construir</li>
</ul></div>'''

def pagina():
    dados = {k: dict(nome=v['nome'], frase=v['frase'],
                     itens=[[a, b, q, [list(s) for s in ss]] for a, b, q, ss in v['itens']],
                     lig=[[a, b, [list(s) for s in ss]] for a, b, ss in v['lig']]) for k, v in G.items()}
    cen_js = {cid: dict(nome=nome, passos=[[txt, ch, fl] for txt, ch, fl in passos]) for cid, nome, passos in CENARIOS}
    botoes = ''.join(f'<li><button type="button" data-abre="{k}">{esc(G[k]["nome"])}</button></li>' for k in
                     ['portas', 'conteudo', 'nucleo', 'vigilancia', 'disciplina', 'interfaces', 'periferia', 'ferramentas', 'fora', 'gente'])
    bcen = ''.join(f'<button type="button" data-cen="{cid}" aria-pressed="false">{esc(nome)}</button>' for cid, nome, _ in CENARIOS)
    svg = cidade()
    faltam = set(CEN) - USADAS
    assert not faltam, faltam
    titulo_p = 'A cidade e quem a aciona'
    ideia = ('A planta das duas cidades, agora com quem age: cada linha sai de quem aciona e tem a cor dele. '
             'Escolha um cenário para ver o caminho aceso, passo a passo.')
    return f'''<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{titulo_p}</title><style>{CSS}</style></head>
<body>
<header><h1>{titulo_p}</h1><p class="ideia">{esc(ideia)}</p></header>
{LEGENDA}
<section class="cenarios" aria-label="Cenários">
<div class="cen-botoes"><span class="rot-cen">Cenários</span>{bcen}</div>
<div class="cen-passo" id="cen-passo" hidden aria-live="polite"><span class="cen-n"><span class="nome" id="cen-nome"></span><span id="cen-num"></span></span><span class="cen-txt" id="cen-txt"></span>
<button type="button" id="cen-ant">← Anterior</button><button type="button" id="cen-prox">Próximo →</button><button type="button" id="cen-sair">Sair do cenário</button></div>
</section>
<p class="dica">Arraste o desenho para os lados; os bairros também estão na lista abaixo.</p>
<div class="moldura"><main class="palco">
<svg class="cidade" viewBox="0 0 1200 780" role="img" aria-label="Planta da cidade do par: muralha com nove bairros, as pessoas à esquerda com as linhas do que cada uma aciona, a estrada da rede privada e o outro par em miniatura.">{DEFS}{svg}</svg>
</main></div>
<ul class="lista-bairros" aria-label="Bairros">{botoes}</ul>
<aside id="ficha" aria-live="polite" aria-label="Ficha do bairro"><button id="fechar" type="button">Fechar</button><div id="ficha-corpo"></div></aside>
<script>{JS.replace("__DADOS__", json.dumps(dados, ensure_ascii=False)).replace("__CEN__", json.dumps(cen_js, ensure_ascii=False))}</script>
</body></html>'''

with open(os.path.join(OUT, 'mistura.html'), 'w', encoding='utf-8', newline='\n') as fh:
    fh.write(pagina())
print('ok')
