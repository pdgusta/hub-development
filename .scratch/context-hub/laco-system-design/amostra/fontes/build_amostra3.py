# Amostra (fase 4): a mistura aprovada num canvas de tela inteira (arrastar, zoom, roda). Conteúdo só de descricao-do-hub.md (v3.2).
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

def abre(cx, cy, gid, fx=''):
    f, s, c_ = COR[gid]
    return (f'<g class="abre" aria-hidden="true"><circle{fx} cx="{cx}" cy="{cy}" r="8.5" fill="#fffdf8" stroke="{c_}" stroke-width="1.8"/>'
            f'<path{fx} d="M{cx-4},{cy} H{cx+4} M{cx},{cy-4} V{cy+4}" stroke="{c_}" stroke-width="1.8" stroke-linecap="round"/></g>')

def zona(gid, shape, label_xy, inner='', fixo=False):
    f, s, c_ = COR[gid]
    nome = G[gid]['nome']
    lx, ly = label_xy
    fx = ' data-fixo="1"' if fixo else ''
    return (f'<g class="bairro" data-grupo="{esc(nome)}" data-abre="{gid}"{cen(nome)} tabindex="0" role="button" '
            f'aria-label="Abrir a ficha: {esc(nome)}">'
            f'{shape.replace("/>", f" class=\"zona\" fill=\"{f}\" stroke=\"{s}\"/>", 1)}'
            f'<text{fx} x="{lx+22}" y="{ly}" class="grp" fill="{c_}">{esc(nome)}</text>{abre(lx + 8, ly - 5, gid, fx)}'
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

def lig(de_para, d, cls, decidir=False, fixo=False):
    base = f'<path class="lig-fundo"{cen(de_para)} d="{d}"/>' if decidir else ''
    fx = ' data-fixo="1"' if fixo else ''
    return base + f'<path data-ligacao="{esc(de_para)}"{cen(de_para)}{fx} class="lig {cls}" d="{d}"><title>{esc(de_para)}</title></path>'

# ---- remapeamento vertical da amostra: a fileira de cima e a de baixo ganham 45 unidades cada
import re as _re
def YM(y):
    y = float(y)
    if y <= 230: return y
    if y < 240: return y + (y - 230) * 4.5
    if y <= 700: return y + 45
    if y < 730: return y + 45 + (y - 700) * (70 / 30)
    return y + 115
def _f(v): return ('%.2f' % v).rstrip('0').rstrip('.')
def _mapa_d(d):
    out, cmd, nums = [], None, []
    toks = _re.findall(r'[MLHVQZmlhvqz]|-?\d+(?:\.\d+)?', d)
    i = 0
    res = []
    while i < len(toks):
        t_ = toks[i]
        if _re.match(r'[A-Za-z]', t_):
            cmd = t_; res.append(t_); i += 1; continue
        if cmd in ('M', 'L', 'Q'):
            res.append(t_ + ',' + _f(YM(toks[i+1]))); i += 2
        elif cmd == 'V':
            res.append(_f(YM(t_))); i += 1
        else:
            res.append(t_); i += 1
    s_ = ''
    for r in res:
        if _re.match(r'^[A-Za-z]$', r): s_ += (' ' if s_ else '') + r
        else: s_ += r + ' ' if False else r if s_.endswith(tuple('MLHVQZmlhvqz')) else ' ' + r
    return s_.strip()
def mapear(svg):
    def tag(m):
        nome, at = m.group(1), m.group(2)
        if 'data-fixo' in at: return m.group(0)
        def get(a):
            mm = _re.search(r'\s' + a + r'="(-?[\d.]+)"', at); return float(mm.group(1)) if mm else None
        def put(a, v):
            nonlocal at
            at = _re.sub(r'(\s' + a + r'=")(-?[\d.]+)(")', lambda q: q.group(1) + _f(v) + q.group(3), at, count=1)
        if nome == 'rect':
            y, h = get('y'), get('height')
            if y is not None:
                put('y', YM(y))
                if h is not None: put('height', YM(y + h) - YM(y))
        elif nome == 'text':
            y = get('y')
            if y is not None: put('y', YM(y))
        elif nome == 'circle':
            y = get('cy')
            if y is not None: put('cy', YM(y))
        elif nome == 'line':
            for a in ('y1', 'y2'):
                y = get(a)
                if y is not None: put(a, YM(y))
        elif nome == 'path':
            at = _re.sub(r'(\sd=")([^"]*)(")', lambda q: q.group(1) + _mapa_d(q.group(2)) + q.group(3), at, count=1)
        return '<' + nome + at + '>'
    return _re.sub(r'<(rect|text|circle|line|path)(\s[^>]*)>', tag, svg)

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

def caderno(x, y, gid):  # caderno de papéis da biblioteca do Maestri
    s = COR[gid][1]
    return (f'<rect x="{x}" y="{y}" width="34" height="38" rx="4" fill="#fffdf8" stroke="{s}" stroke-width="2.2"/>'
            + ''.join(f'<line x1="{x+6}" y1="{y+10+i*8}" x2="{x+(28 if i < 3 else 22)}" y2="{y+10+i*8}" stroke="{s}" stroke-width="1.6"/>' for i in range(4)))

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
    z.append(zona('interfaces', '<rect x="215" y="604" width="215" height="131" rx="16"/>', (227, 836),
        inner=item('Obsidian', oficina(285, 645, 'interfaces') + t(349, 675, 'Obsidian') + marca2(340, 650, 'periferia')), fixo=True))
    z.append(zona('ferramentas', '<rect x="455" y="604" width="220" height="131" rx="16"/>', (467, 632), inner=item('Biblioteca do Maestri', caderno(548, 650, 'ferramentas') + t(565, 757, 'Biblioteca do Maestri', anchor='middle', extra=' data-fixo="1"'))))
    z.append(zona('periferia', '<rect x="700" y="604" width="185" height="131" rx="16"/>', (712, 632),
        inner=item('Agendador do Windows', relogio(800, 672, 'periferia') + t(793, 762, 'Agendador do Windows', anchor='middle', extra=' data-fixo="1"'))))
    # o outro par: a mesma planta em miniatura, com a troca chegando ao cofre dele pela mesma altura
    # a miniatura repete a planta já esticada (YM); por isso fica fora do remapeamento (data-fixo)
    k, ox = 0.24, 1022
    oy = YM(262) - (YM(262) - my) * k
    X = lambda x: round(ox + (x - mx) * k, 1)
    Y = lambda y: round(oy + (YM(y) - my) * k, 1)
    alt = YM(750) - my
    mini = f'<rect data-fixo="1" x="{X(mx)}" y="{Y(my)}" width="{710*k:.1f}" height="{alt*k:.1f}" rx="8" class="muralha fantasma"/>'
    mini += ''.join(f'<rect data-fixo="1" x="{X(x)}" y="{Y(y)}" width="{w*k:.1f}" height="{(YM(y+h)-YM(y))*k:.1f}" rx="4" fill="{COR[g][1]}" fill-opacity=".3" stroke="{COR[g][1]}" stroke-opacity=".6" stroke-width="1.2" class="mini"{cen("mini:" + g)}/>'
                    for x, y, w, h, g in QA)
    cofre_b = f'<rect data-fixo="1" x="{X(470)}" y="{Y(356)}" width="{205*k:.1f}" height="{(YM(404)-YM(356))*k:.1f}" rx="4" class="encontro fantasma"/>'
    estrada = ('<rect x="903" y="250" width="112" height="24" rx="4" class="via"/>' +
               ''.join(f'<line x1="{x}" y1="262" x2="{x+8}" y2="262" class="faixa"/>' for x in range(911, 1008, 18)))
    z.append(zona('fora', '<rect x="915" y="140" width="280" height="305" rx="22" stroke-dasharray="7 5"/>', (927, 168),
        inner=item('Rede privada', estrada + t(956, 302, 'Rede privada', anchor='middle')) + mini +
              item('Outro par', cofre_b + t(X(545), Y(750) + 22, 'Outro par', anchor='middle', cls='rot parb', extra=' data-fixo="1"'))))
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
        lig('Agendador do Windows → Sincronizador', 'M783,672 H705 V486 H640', 'agendador'),
        lig('Agendador do Windows → Vigia do sync', 'M817,672 H868 V470 H816', 'agendador'),
        # troca entre pares, nos dois sentidos
        lig('Banco local ↔ Outro par', f'M655,{YM(356)} V{YM(262)} H{X(655)} V{Y(356)}', 'trocar', fixo=True),
        # só no cenário: correm por fora, sem cruzar nada
        lig('Maestro → Biblioteca do Maestri', 'M108,85 V16 H1197 V881 H655 V714 H582', 'maestro so-cen', fixo=True),
        lig('Maestro → Gustavo', 'M92,85 V40 H8 V648 H85', 'maestro so-cen'),
        lig('Checkpoint → Agentes', 'M340,185 H312 V238 H95 V355', 'disc so-cen'),
    ]
    return muralha + ''.join(z) + ''.join(L) + gente

# ---------------------------------------------------------------- página
CSS = r'''
:root{--papel:#f6f1e7;--tinta:#2b2622;--suave:#4a433c;--linha:#d9cfbf;--cartao:#fffcf6;
--agente:#2a62a8;--gustavo:#b8462a;--maestro:#0d7480;--disc:#6f4f92;--agendador:#8a6a3a;--confere:#4a433c;--trocar:#3f5a74;--sinc:#3d8a76;--falha:#b3261e}
*{box-sizing:border-box}
html,body{margin:0;height:100%;overflow:hidden;background:var(--papel);color:var(--tinta);font-family:"Segoe UI",system-ui,-apple-system,Roboto,sans-serif}
body{display:flex;flex-direction:column;height:100vh;height:100dvh}
.topo{flex:0 0 auto;border-bottom:1px solid var(--linha);background:var(--papel);position:relative;z-index:2}
.tela{flex:1 1 auto;position:relative;overflow:hidden;outline:none;touch-action:none;cursor:default;background:var(--papel);-webkit-user-select:none;user-select:none}
.tela.arrastando{cursor:grabbing}
.tela:focus-visible{box-shadow:inset 0 0 0 3px var(--tinta)}
svg.cidade{display:block;width:100%;height:100%}
.zoom{position:absolute;left:14px;bottom:14px;display:flex;gap:6px;z-index:2}
.zoom button{font:inherit;font-size:18px;font-weight:700;min-width:40px;height:40px;border:1px solid var(--linha);background:var(--cartao);color:var(--tinta);border-radius:10px;cursor:pointer;box-shadow:0 2px 6px rgba(60,40,20,.12)}
.zoom button.txt{font-size:14px;font-weight:600;padding:0 12px}
.zoom button:focus-visible,.topo button:focus-visible{outline:3px solid var(--tinta);outline-offset:2px}
.ajuda{margin-left:auto;font-size:13px;color:var(--suave);padding:4px 0}
.ajuda kbd{font:inherit;font-weight:700;color:var(--tinta)}
.detalhe{display:none}
.perto .detalhe{display:inline}
.etq rect{fill:#fffdf8;stroke-width:1.2}
.etq text{font-size:8.5px;font-weight:600;fill:var(--tinta)}
.etq{cursor:pointer}
.etq:hover rect{stroke:var(--tinta);stroke-width:2}
.dobra{display:none;font:inherit;font-size:13px;border:1px solid var(--linha);background:var(--cartao);border-radius:999px;padding:5px 12px;color:var(--tinta);cursor:pointer}
header{padding:10px 24px 2px;display:flex;flex-wrap:wrap;gap:4px 22px;align-items:baseline}
h1{font-family:Georgia,"Times New Roman",serif;font-size:24px;margin:0;font-weight:700}
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
.cen-passo{margin-top:2px}
.cen-botoes.mais-dir{-webkit-mask-image:linear-gradient(90deg,#000 calc(100% - 64px),transparent);mask-image:linear-gradient(90deg,#000 calc(100% - 64px),transparent)}
.cen-botoes.mais-esq{-webkit-mask-image:linear-gradient(90deg,transparent,#000 48px);mask-image:linear-gradient(90deg,transparent,#000 48px)}
.cen-botoes.mais-esq.mais-dir{-webkit-mask-image:linear-gradient(90deg,transparent,#000 48px,#000 calc(100% - 64px),transparent);mask-image:linear-gradient(90deg,transparent,#000 48px,#000 calc(100% - 64px),transparent)}
.cen-botoes .rot-cen{font-size:13px;font-weight:700;color:var(--suave);margin-right:4px;letter-spacing:.04em;text-transform:uppercase}
.cen-botoes button,.cen-passo button{font:inherit;font-size:14px;border:1px solid var(--linha);background:var(--cartao);color:var(--tinta);border-radius:999px;padding:6px 12px;cursor:pointer}
.cen-botoes button[aria-pressed="true"]{background:var(--tinta);color:#fff;border-color:var(--tinta)}
.cen-botoes button:focus-visible,.cen-passo button:focus-visible,.lista-bairros button:focus-visible,#fechar:focus-visible{outline:3px solid var(--tinta);outline-offset:2px}
body.cen .legendas,body.cen .cen-botoes{display:none}
.cen-passo{display:flex;flex-wrap:wrap;gap:8px 12px;align-items:center;margin-top:8px;padding:8px 12px;border:1px solid var(--linha);border-radius:12px;background:var(--cartao);min-height:46px}
.cen-passo[hidden]{display:none}
.cen-n{font-weight:700;font-size:14px}
.cen-n .nome{display:block;font-weight:600;color:var(--suave);font-size:13px}
.cen-txt{font-size:16px;flex:1 1 260px}
.moldura{position:relative}
.palco{padding:0 16px 0;overflow-x:auto}
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
@media (max-height:800px){
 .legendas{display:none}.legendas.aberta{display:block}.dobra{display:inline-block}
}
@media (max-width:1100px){
 .legendas{display:none}.legendas.aberta{display:block}.dobra{display:inline-block}
 .cen-botoes{flex-wrap:nowrap;overflow-x:auto;padding-bottom:4px;scrollbar-width:thin}.cen-botoes button{white-space:nowrap}
 .ajuda{display:none}header{flex-wrap:nowrap;align-items:center}h1{white-space:nowrap}.ideia{font-size:14px;flex:1 1 280px}.dobra{flex:0 0 auto}
}
@media (max-width:760px){
 header{display:flex;flex-wrap:wrap;padding:8px 12px 2px;gap:4px 10px}h1{font-size:19px;white-space:normal}.ideia{display:none}
 .legendas{padding:0 12px 4px}.legendas{display:none}.legendas.aberta{display:block}
 .dobra{display:inline-block}
 .cenarios{padding:2px 12px 6px}
 .cen-botoes{flex-wrap:nowrap;overflow-x:auto;padding-bottom:4px}
 .cen-botoes button{white-space:nowrap}
 .cen-passo{gap:6px 8px;padding:6px 8px}.cen-txt{font-size:15px;flex-basis:100%}
 .cen-passo button{padding:5px 10px;font-size:13px}
 .ajuda{display:none}
 .zoom{left:10px;bottom:10px}
}
'''

JS = r'''
(function(){
var G=__DADOS__,C=__CEN__,COR2=__COR__;
var NS='http://www.w3.org/2000/svg';
// ---- canvas: a vista é o viewBox do desenho
var tela=document.getElementById('tela'),svgC=document.querySelector('svg.cidade'),CONT={x:0,y:24,w:1200,h:852},vb=null,MAX=5;
// modo: 'abertura' ou 'tudo' enquanto ninguém mexeu (o redimensionamento refaz o mesmo enquadramento); null depois
var modo='abertura';
function px(){return tela.clientWidth/vb.w}
function aplicar(){svgC.setAttribute('viewBox',vb.x.toFixed(2)+' '+vb.y.toFixed(2)+' '+vb.w.toFixed(2)+' '+vb.h.toFixed(2));
 svgC.classList.toggle('perto',px()>=1.4);var z=document.getElementById('z-nivel');if(z)z.textContent=Math.round(px()*100)+'%'}
// canto dos botões de zoom: o enquadramento desconta a faixa de baixo ou a coluna da esquerda (fica a que dá mais zoom)
function cantoZoom(){var z=document.querySelector('.zoom');if(!z)return {w:0,h:0};return {w:z.offsetLeft+z.offsetWidth+8,h:tela.clientHeight-z.offsetTop+8}}
// caixas do que se vê na planta (itens, bairros, muralha, pessoas): o canto do zoom só conta se cobrir alguma
var CAIXAS=[];svgC.querySelectorAll('.item,.bairro>.zona,.muralha').forEach(function(e){var b=e.getBBox();if(b.width||b.height)CAIXAS.push(b)});
function cobre(r,c){var W=tela.clientWidth,H=tela.clientHeight,e=r.e,x0=CONT.x+CONT.w/2-(r.l+r.w/2)/e,y0=CONT.y+CONT.h/2-(r.t+r.h/2)/e;
 var zx2=x0+c.w/e,zy1=y0+(H-c.h)/e;return CAIXAS.some(function(b){return b.x<zx2&&b.y+b.height>zy1})}
function enquadrar(){var W=tela.clientWidth,H=tela.clientHeight,m=10,c=cantoZoom();
 var t={e:Math.min((W-2*m)/CONT.w,(H-2*m)/CONT.h),l:0,t:0,w:W,h:H};if(!cobre(t,c))return t;
 var a={e:Math.min((W-2*m)/CONT.w,(H-c.h-2*m)/CONT.h),l:0,t:0,w:W,h:H-c.h},b={e:Math.min((W-c.w-2*m)/CONT.w,(H-2*m)/CONT.h),l:c.w,t:0,w:W-c.w,h:H};
 return a.e>=b.e?a:b}
// o menor zoom manual: 35%, ou menos se a cidade inteira só cabe abaixo disso (tela estreita)
function minimo(){return Math.min(.35,enquadrar().e)}
// "Ver tudo" e a tecla 0: a cidade inteira, fora do canto dos botões, em qualquer largura
function tudo(){var W=tela.clientWidth,H=tela.clientHeight,r=enquadrar(),e=r.e;
 vb={w:W/e,h:H/e};vb.x=CONT.x+CONT.w/2-(r.l+r.w/2)/e;vb.y=CONT.y+CONT.h/2-(r.t+r.h/2)/e;aplicar()}
// abertura: tudo à vista só se o menor nome ficar com 13 px ou mais; se não, 75% centrado no Banco local
var ROT=0;svgC.querySelectorAll('text').forEach(function(t){var h=t.getBBox().height;if(h&&(!ROT||h<ROT))ROT=h});
function abertura(){var r=enquadrar();if(r.e*ROT>=13){tudo();return}
 var W=tela.clientWidth,H=tela.clientHeight,e=.75,bl=document.querySelector('[data-item="Banco local"]').getBBox();
 vb={w:W/e,h:H/e};vb.x=bl.x+bl.width/2-vb.w/2;vb.y=bl.y+bl.height/2-vb.h/2;aplicar()}
function ajustarTela(){if(!vb)return;var cx=vb.x+vb.w/2,cy=vb.y+vb.h/2,e=px();var W=tela.clientWidth,H=tela.clientHeight;if(!W||!H)return;vb.w=W/e;vb.h=H/e;vb.x=cx-vb.w/2;vb.y=cy-vb.h/2;aplicar()}
function prender(){var lim=Math.min(vb.w,vb.h)*.5;
 vb.x=Math.min(Math.max(vb.x,CONT.x-vb.w+lim),CONT.x+CONT.w-lim);vb.y=Math.min(Math.max(vb.y,CONT.y-vb.h+lim),CONT.y+CONT.h-lim)}
// zoom em volta de um ponto da tela (sx, sy); sem ponto, em volta do centro da área do desenho
function zoom(f,sx,sy){modo=null;var e=px(),n=Math.min(MAX,Math.max(minimo(),e*f));f=n/e;if(Math.abs(f-1)<1e-4)return;
 if(sx==null){sx=tela.clientWidth/2;sy=tela.clientHeight/2}
 var ux=vb.x+sx/e,uy=vb.y+sy/e;vb.w/=f;vb.h/=f;vb.x=ux-sx/n;vb.y=uy-sy/n;prender();aplicar()}
function andar(dx,dy){modo=null;var e=px();vb.x+=dx/e;vb.y+=dy/e;prender();aplicar()}
function mostrar(x,y){var mx=vb.w*.08,my=vb.h*.08;if(x<vb.x+mx||x>vb.x+vb.w-mx||y<vb.y+my||y>vb.y+vb.h-my){vb.x=x-vb.w/2;vb.y=y-vb.h/2;prender();aplicar()}}
tela.addEventListener('wheel',function(ev){ev.preventDefault();var r=tela.getBoundingClientRect(),k=ev.deltaMode===1?16:ev.deltaMode===2?tela.clientHeight:1,d=ev.deltaY*k,dx=ev.deltaX*k;
 if(ev.ctrlKey||ev.metaKey){zoom(Math.exp(-d*.0018),ev.clientX-r.left,ev.clientY-r.top)}
 else if(ev.shiftKey){andar(dx||d,0)}else{andar(dx,d)}},{passive:false});
tela.addEventListener('contextmenu',function(ev){ev.preventDefault()});
// a área nunca rola: o foco num bairro não pode deslocar o desenho por baixo da vista
tela.addEventListener('scroll',function(){if(tela.scrollTop||tela.scrollLeft){tela.scrollTop=0;tela.scrollLeft=0}});
// arrasto: botão direito ou do meio (captura já no aperto); toque: um dedo anda, dois aproximam.
// O toque só é capturado depois de virar arrasto (6 px): o toque simples chega à ficha ou ao botão.
var toques={},arr=null,suprimir=false;
function ref(id){var t=toques[id];return {x:t.x,y:t.y,mov:true,id:+id}}
tela.addEventListener('mousedown',function(ev){if(ev.button===1||ev.button===2)ev.preventDefault()});
tela.addEventListener('pointerdown',function(ev){suprimir=false;
 if(ev.target.closest&&ev.target.closest('.zoom'))return;
 if(ev.pointerType==='touch'){toques[ev.pointerId]={x:ev.clientX,y:ev.clientY};var ids=Object.keys(toques);
  if(ids.length===1)arr={x:ev.clientX,y:ev.clientY,mov:false,id:ev.pointerId};
  else{arr=ref(ids[0]);try{tela.setPointerCapture(ev.pointerId)}catch(e){}}
  return}
 if(ev.button!==2&&ev.button!==1)return;
 ev.preventDefault();arr={x:ev.clientX,y:ev.clientY,mov:false,id:ev.pointerId};tela.setPointerCapture(ev.pointerId)});
tela.addEventListener('pointermove',function(ev){if(!arr)return;
 if(ev.pointerType==='touch'){if(!toques[ev.pointerId])return;var ids=Object.keys(toques);
  if(ids.length>=2){var a=toques[ids[0]],b=toques[ids[1]],d0=Math.hypot(a.x-b.x,a.y-b.y);toques[ev.pointerId]={x:ev.clientX,y:ev.clientY};
   a=toques[ids[0]];b=toques[ids[1]];var d1=Math.hypot(a.x-b.x,a.y-b.y),r=tela.getBoundingClientRect();
   if(d0>0)zoom(d1/d0,(a.x+b.x)/2-r.left,(a.y+b.y)/2-r.top);return}
  toques[ev.pointerId]={x:ev.clientX,y:ev.clientY}}
 if(ev.pointerId!==arr.id)return;
 var dx=ev.clientX-arr.x,dy=ev.clientY-arr.y;
 if(!arr.mov){if(Math.hypot(dx,dy)<6)return;arr.mov=true;tela.classList.add('arrastando');
  if(ev.pointerType==='touch'){try{tela.setPointerCapture(ev.pointerId)}catch(e){}}}
 andar(-dx,-dy);arr.x=ev.clientX;arr.y=ev.clientY});
// fim do gesto (soltar, cancelar ou perder a captura): a mesma limpeza; de dois dedos para um, a referência vem do dedo que ficou
function solta(ev){
 if(ev.pointerType==='touch'){if(!toques[ev.pointerId])return;delete toques[ev.pointerId];var ids=Object.keys(toques);
  if(ids.length){arr=ref(ids[0]);return}}
 else if(!arr||ev.pointerId!==arr.id)return;
 if(arr&&arr.mov)suprimir=true;arr=null;tela.classList.remove('arrastando')}
['pointerup','pointercancel'].forEach(function(n){tela.addEventListener(n,solta)});
tela.addEventListener('lostpointercapture',function(ev){if(ev.target===tela)solta(ev)});
// o clique que nasce de um arrasto não abre ficha (vale até o próximo aperto)
tela.addEventListener('click',function(ev){if(suprimir){suprimir=false;ev.stopPropagation();ev.preventDefault()}},true);
tela.addEventListener('keydown',function(ev){if(ev.target!==tela)return;var k=ev.key,p=60;
 if(k==='ArrowLeft')andar(-p,0);else if(k==='ArrowRight')andar(p,0);else if(k==='ArrowUp')andar(0,-p);else if(k==='ArrowDown')andar(0,p);
 else if(k==='+'||k==='=')zoom(1.25);else if(k==='-'||k==='_')zoom(1/1.25);else if(k==='0'){modo='tudo';tudo()}else return;ev.preventDefault()});
document.getElementById('z-mais').addEventListener('click',function(){zoom(1.25)});
document.getElementById('z-menos').addEventListener('click',function(){zoom(1/1.25)});
document.getElementById('z-tudo').addEventListener('click',function(){modo='tudo';tudo()});
// o foco que vem do teclado (Tab) num bairro ou pessoa fora da vista leva a vista até ele; o do mouse, não
var porTeclado=false;
document.addEventListener('keydown',function(ev){if(ev.key==='Tab')porTeclado=true},true);
document.addEventListener('pointerdown',function(){porTeclado=false},true);
svgC.addEventListener('focusin',function(ev){if(!porTeclado)return;var b=ev.target.getBBox&&ev.target.getBBox();if(b)mostrar(b.x+b.width/2,b.y+Math.min(b.height/2,40))});
function reajustar(){if(!tela.clientWidth||!tela.clientHeight)return;if(document.body.classList.contains('cen')||!modo)ajustarTela();else if(modo==='tudo')tudo();else abertura()}
if(window.ResizeObserver)new ResizeObserver(reajustar).observe(tela);else window.addEventListener('resize',reajustar);
abertura();window.addEventListener('load',reajustar);
(function(){var r=document.querySelector('.cen-botoes');function marca(){var x=r.scrollLeft,fim=r.scrollWidth-r.clientWidth;r.classList.toggle('mais-esq',x>2);r.classList.toggle('mais-dir',x<fim-2)}
 r.addEventListener('scroll',marca);window.addEventListener('resize',marca);marca();
 r.addEventListener('focusin',function(ev){if(ev.target.scrollIntoView)ev.target.scrollIntoView({block:'nearest',inline:'nearest'})})})();
var dobra=document.getElementById('dobra-leg');dobra.addEventListener('click',function(){var l=document.querySelector('.legendas'),a=l.classList.toggle('aberta');dobra.setAttribute('aria-expanded',a);ajustarTela()});
// ---- camada de detalhe: ao aproximar, cada bairro mostra, em etiquetas pequenas, os componentes que só estavam na ficha
(function(){var DES={};document.querySelectorAll('[data-item]').forEach(function(e){DES[e.getAttribute('data-item')]=1});
 var obst=[];svgC.querySelectorAll('text').forEach(function(t){var b=t.getBBox();obst.push([b.x-8,b.y-6,b.x+b.width+8,b.y+b.height+10])});
 svgC.querySelectorAll('.item').forEach(function(g){var b=g.getBBox();obst.push([b.x-6,b.y-6,b.x+b.width+6,b.y+b.height+6])});
 svgC.querySelectorAll('.lig:not(.so-cen),.lig-fundo').forEach(function(p){var L=p.getTotalLength(),w=parseFloat(getComputedStyle(p).strokeWidth)/2+5;for(var d=0;d<=L;d+=5){var q=p.getPointAtLength(d);obst.push([q.x-w,q.y-w,q.x+w,q.y+w])}});
 svgC.querySelectorAll('.mini,.via,.encontro').forEach(function(r){var b=r.getBBox();obst.push([b.x-2,b.y-2,b.x+b.width+2,b.y+b.height+2])});
 function livreR(a){return a[0]>=0&&obst.every(function(b){return a[2]<b[0]||a[0]>b[2]||a[3]<b[1]||a[1]>b[3]})}
 // põe uma etiqueta dentro do retângulo zr, no primeiro lugar livre (de cima para baixo, da esquerda para a direita)
 function colocar(lay,nome,papel,zr,cor,abre){var t=document.createElementNS(NS,'text');t.textContent=nome;var e=document.createElementNS(NS,'g');e.setAttribute('class','etq');e.setAttribute('data-item',nome);
  if(abre)e.setAttribute('data-abre',abre);e.appendChild(t);lay.appendChild(e);var tb=t.getBBox(),w=tb.width+8,h=13,pos=null;
  for(var y=zr.y+8;y+h<=zr.y+zr.height-6&&!pos;y+=1){for(var x=zr.x+8;x+w<=zr.x+zr.width-8;x+=3){var a=[x,y,x+w,y+h];if(livreR(a)){pos=a;break}}}
  if(!pos){lay.removeChild(e);return false}obst.push([pos[0]-3,pos[1]-3,pos[2]+3,pos[3]+3]);
  var r=document.createElementNS(NS,'rect');r.setAttribute('x',pos[0]);r.setAttribute('y',pos[1]);r.setAttribute('width',w);r.setAttribute('height',h);r.setAttribute('rx',6.5);r.setAttribute('stroke',cor);
  e.insertBefore(r,t);t.setAttribute('x',pos[0]+4);t.setAttribute('y',pos[1]+9.5);
  var ti=document.createElementNS(NS,'title');ti.textContent=nome+': '+papel;e.appendChild(ti);return true}
 // nome sem lugar não some calado: fica no console e em data-sobra-nomes do bairro (a ficha continua com ele)
 function acusar(z,onde,nomes){if(!nomes.length)return;z.setAttribute('data-sobra',nomes.length);z.setAttribute('data-sobra-nomes',nomes.join(' | '));
  if(window.console)console.warn('Camada de detalhe: sem lugar em "'+onde+'" para: '+nomes.join(', ')+'. A ficha ainda mostra; abra espaço no bairro.')}
 document.querySelectorAll('.bairro').forEach(function(z){var gid=z.getAttribute('data-abre'),g=G[gid];if(!g)return;var zr=z.querySelector('.zona').getBBox(),s=COR2[gid];
  var lay=document.createElementNS(NS,'g');lay.setAttribute('class','detalhe');z.appendChild(lay);var sobra=[];
  g.itens.filter(function(i){return !DES[i[0]]}).forEach(function(i){if(!colocar(lay,i[0],i[1],zr,s))sobra.push(i[0])});
  acusar(z,g.nome,sobra)});
 // quem chega sem estar desenhado: o Claude Desktop junto do Gustavo (é ele pelo app) e o cliente junto dos agentes; abrem a ficha "Quem chega"
 (function(){var gente=G.gente;if(!gente)return;var lay=document.createElementNS(NS,'g');lay.setAttribute('class','detalhe');svgC.appendChild(lay);var sobra=[];
  [['Claude Desktop','Gustavo'],['Cliente','Agentes']].forEach(function(p){if(DES[p[0]])return;var it=gente.itens.filter(function(i){return i[0]===p[0]})[0],pe=document.querySelector('.pessoa[data-item="'+p[1]+'"]');if(!it||!pe)return;
   var b=pe.getBBox(),zr={x:4,y:b.y+b.height-4,width:182,height:64};if(!colocar(lay,it[0],it[1],zr,'#4a433c','gente'))sobra.push(it[0])});
  acusar(lay,gente.nome,sobra)})()})();
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
 f.classList.add('aberta');fundo(f.offsetWidth>=window.innerWidth-1);document.getElementById('fechar').focus({preventScroll:true});f.scrollTop=0;
 if(marcado){f.scrollTop=Math.max(0,marcado.offsetTop-80);setTimeout(function(){marcado.classList.add('apaga')},1200)}}
function fundo(v){['.topo','#tela'].forEach(function(q){var e=document.querySelector(q);if(v)e.setAttribute('inert','');else e.removeAttribute('inert')});if(v){f.setAttribute('role','dialog');f.setAttribute('aria-modal','true')}else{f.removeAttribute('role');f.removeAttribute('aria-modal')}}
function fechar(){f.classList.remove('aberta');fundo(false);if(volta)volta.focus({preventScroll:true})}
document.querySelectorAll('[data-abre]').forEach(function(e){
 function vai(ev){var it=ev.target.closest&&ev.target.closest('[data-item]');abrir(e.getAttribute('data-abre'),e,it?it.getAttribute('data-item'):null)}
 e.addEventListener('click',function(ev){ev.stopPropagation();vai(ev)});
 e.addEventListener('keydown',function(ev){if(ev.key==='Enter'||ev.key===' '){ev.preventDefault();ev.stopPropagation();vai(ev)}})});
document.getElementById('fechar').addEventListener('click',fechar);
window.addEventListener('resize',function(){if(!f.classList.contains('aberta'))return;var m=f.offsetWidth>=window.innerWidth-1;
 if(m===(f.getAttribute('aria-modal')==='true'))return;fundo(m);if(m&&!f.contains(document.activeElement))document.getElementById('fechar').focus({preventScroll:true})});
// cenários: acende o caminho passo a passo
var svg=document.querySelector('svg.cidade'),marcas=document.createElementNS(NS,'g');marcas.setAttribute('aria-hidden','true');svg.appendChild(marcas);
var botoes=document.querySelectorAll('[data-cen]'),painel=document.getElementById('cen-passo'),atual=null,passo=0;
var todos=document.querySelectorAll('[data-cenario]');
function noPasso(e,id,n){return (' '+e.getAttribute('data-cenario')+' ').indexOf(' '+id+':'+n+' ')>=0}
function chave(e){return e.getAttribute('data-chave')}
// caixas dos textos do desenho: o número do passo fica a 6 px de qualquer nome
function textos(){var r=[];svg.querySelectorAll('text').forEach(function(t){if(marcas.contains(t))return;var b=t.getBBox();r.push([b.x,b.y,b.x+b.width,b.y+b.height])});return r}
function livre(x,y,caixas){var R=17;if(x<18||x>1182||y<18||y>882)return false;return caixas.every(function(b){return x+R<b[0]||x-R>b[2]||y+R<b[1]||y-R>b[3]})}
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
 if(!atual){document.body.classList.remove('cen');painel.hidden=true;botoes.forEach(function(b){b.setAttribute('aria-pressed','false')});ajustarTela();return}
 var cen=C[atual],N=cen.passos.length,antes=document.body.classList.contains('cen');document.body.classList.add('cen');painel.hidden=false;if(!antes)ajustarTela();
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
  // a vista vai até o número do passo atual se ele estiver fora da tela
 if(ultima){var b=ultima.getBBox();mostrar(b.x+b.width/2,b.y+b.height/2)}}
function sair(){var b=document.querySelector('[data-cen="'+atual+'"]');atual=null;desenhar();if(b)b.focus()}
botoes.forEach(function(b){b.addEventListener('click',function(){atual=b.getAttribute('data-cen');passo=1;desenhar();document.getElementById('cen-prox').focus()})});
document.getElementById('cen-ant').addEventListener('click',function(){if(passo>1){passo--;desenhar()}});
document.getElementById('cen-prox').addEventListener('click',function(){if(atual&&passo<C[atual].passos.length){passo++;desenhar()}});
document.getElementById('cen-sair').addEventListener('click',sair);
document.addEventListener('keydown',function(ev){
 if(ev.key==='Escape'){if(f.classList.contains('aberta'))fechar();else if(atual)sair()}
 if(atual&&!f.classList.contains('aberta')&&document.activeElement!==tela){
  if(ev.key==='ArrowRight'&&passo<C[atual].passos.length){passo++;desenhar()}
  if(ev.key==='ArrowLeft'&&passo>1){passo--;desenhar()}}});

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
                     itens=[[a, b, q, [list(s_) for s_ in ss]] for a, b, q, ss in v['itens']],
                     lig=[[a, b, [list(s_) for s_ in ss]] for a, b, ss in v['lig']]) for k, v in G.items()}
    cen_js = {cid: dict(nome=nome, passos=[[txt, ch, fl] for txt, ch, fl in passos]) for cid, nome, passos in CENARIOS}
    bcen = ''.join(f'<button type="button" data-cen="{cid}" aria-pressed="false">{esc(nome)}</button>' for cid, nome, _ in CENARIOS)
    svg = mapear(cidade())
    for tag in ('<g class="bairro', '<g class="item', '<path data-ligacao', '<path class="lig-fundo', '<rect data-fixo'):
        svg = svg.replace(tag, '\n' + tag)
    faltam = set(CEN) - USADAS
    assert not faltam, faltam
    titulo_p = 'A cidade e quem a aciona'
    ideia = 'Cada linha sai de quem aciona e tem a cor dele. Escolha um cenário para ver o caminho aceso, passo a passo.'
    cor2 = {k: v[1] for k, v in COR.items()}
    return f"""<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8">
<!--
Como atualizar quando um ticket muda o desenho. A fonte é amostra/fontes/build_amostra2.py: prefira mudar lá e regerar
(python -I build_amostra2.py <pasta da amostra>). À mão, mude junto, no mesmo nome exato:
 1. Ficha: no script, o objeto G (bairro -> itens [nome, papel, {{dono, aciona, le, ...}}, selos] e lig [De -> Para, frase, selos]).
 2. Componente desenhado: o <g class="item" data-item="Nome"> no SVG, com data-cenario="cenario:passo" e data-chave.
 3. Ligação: <path data-ligacao="De -> Para"> (e o lig-fundo, se a decidir), com data-cenario e data-chave.
 4. Cenários: o objeto C; cada passo lista as chaves (nomes de itens e ligações) que acende.
 5. Camada de detalhe: nasce de G sozinha (componentes da ficha sem desenho). Nome sem lugar no bairro aparece no console
    e no atributo data-sobra-nomes do bairro: abra espaço ou mude o bairro de tamanho.
--><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{titulo_p}</title><style>{CSS}</style></head>
<body>
<div class="topo">
<header><h1>{titulo_p}</h1><p class="ideia">{esc(ideia)}</p><button type="button" class="dobra" id="dobra-leg" aria-expanded="false">Legenda</button></header>
{LEGENDA}
<section class="cenarios" aria-label="Cenários">
<div class="cen-botoes"><span class="rot-cen">Cenários</span>{bcen}<span class="ajuda">Arraste com o botão direito · <kbd>Ctrl</kbd> + roda: zoom · <kbd>Shift</kbd> + roda: para os lados · aproxime para ver mais nomes</span></div>
<div class="cen-passo" id="cen-passo" hidden aria-live="polite"><span class="cen-n"><span class="nome" id="cen-nome"></span><span id="cen-num"></span></span><span class="cen-txt" id="cen-txt"></span>
<button type="button" id="cen-ant">← Anterior</button><button type="button" id="cen-prox">Próximo →</button><button type="button" id="cen-sair">Sair do cenário</button></div>
</section>
</div>
<main class="tela" id="tela" tabindex="0" aria-label="Planta do hub. Setas andam, + e − aproximam e afastam, 0 mostra tudo.">
<svg class="cidade" viewBox="0 0 1200 900" tabindex="-1" focusable="false" role="group" aria-label="Planta da cidade do par: muralha com nove bairros, as pessoas à esquerda com as linhas do que cada uma aciona, a estrada da rede privada e o outro par em miniatura.">{DEFS}{svg}</svg>
<div class="zoom" role="group" aria-label="Zoom"><button type="button" id="z-menos" aria-label="Afastar">−</button><button type="button" id="z-mais" aria-label="Aproximar">+</button><button type="button" class="txt" id="z-tudo">Ver tudo <span id="z-nivel" aria-hidden="true"></span></button></div>
</main>
<aside id="ficha" aria-live="polite" aria-label="Ficha do bairro"><button id="fechar" type="button">Fechar</button><div id="ficha-corpo"></div></aside>
<script>{JS.replace("__DADOS__", json.dumps(dados, ensure_ascii=False, indent=1)).replace("__CEN__", json.dumps(cen_js, ensure_ascii=False, indent=1)).replace("__COR__", json.dumps(cor2))}</script>
</body></html>"""

with open(os.path.join(OUT, 'amostra.html'), 'w', encoding='utf-8', newline='\n') as fh:
    fh.write(pagina())
print('ok')
