# Mapa de grupos: notas do desenhista

Fonte: só `descricao-do-hub.md` (v3). Diagrama: `mapa-grupos.html`.

## Faltou

- **Ligações entre grupos (5.1 e 6):** a seção 6 liga componentes, não grupos. Tive de agregar as ligações por conta própria; a seção 5.1 não diz nenhuma ligação entre grupos. Onde: 5.1 e 6.
- **Grupo do Agendador do Windows:** é ator (2) e dispara sincronizador, vigia e cópia diária, mas não entra em nenhum grupo de 5.1. Onde: 5.1, 2.
- **Grupo do Outro par:** ator sem grupo em 5.1. Desenhei como caixa fora do par, sem regra dada. Onde: 5.1, 2.
- **Regra para ator que está em dois grupos:** 5.1 diz o caso do Claude Desktop, mas não o dos Clientes (aparecem em "Quem chega" e em "Fora do par"). Onde: 5.1, "Pertence a mais de um grupo".
- **Lista de pertencimento múltiplo incompleta:** a lista de 5.1 deixa de fora Mod de estado (aparece em Vigilância e em Interfaces), Notificação do Windows (Vigilância e Interfaces), Obsidian (Periferia e Interfaces), Kit de par (Periferia e 3.1, Disciplina) e Script do `_archive/` (Periferia e 3.1, Disciplina). Onde: 5.1, "Pertence a mais de um grupo"; 3.1.
- **Grupo de Variante e Versão local de peça:** estão em 3.2 e 4.4, mas 5.1 não as cita. Supus que moram em "Conteúdo" dentro de "acervo". Onde: 5.1, Conteúdo; 3.2.
- **Grupo de Configuração das ferramentas** (`~/.claude`, `~/.codex`, `~/.copilot`): 5.2 lista como lugar, 5.1 não tem grupo para ela além de "Ferramentas da máquina". Supus que cabe lá. Onde: 5.1, 5.2.
- **Gustavo → Obsidian:** a seção 6 não tem a linha. Está só em 7.1 e 4.1. Onde: 6.

## Inventei

- **Layout em grade (3 colunas, 3 linhas):** Quem chega à esquerda; Rede privada e Outro par em faixa de cima; Fora do par em faixa de baixo. A descrição não dá disposição. Escolhi a que mantém as ligações curtas.
- **Um grupo primário por componente:** pela regra "não se desenha o mesmo componente duas vezes" (5.2), cada componente aparece em uma caixa, com "+ grupo" para o segundo. Escolhi o primário pelo maior número de fontes: Checagem de sessão em Disciplina (+ Vigilância); Contrato em Disciplina (+ Conteúdo); Obsidian em Interfaces (+ Periferia); Mod de estado em Vigilância (+ Interfaces); Kit de par em Periferia (+ Disciplina).
- **Desenho por grupo, não por lugar:** os lugares (5.2) ficaram só como texto na lista de ligações e nas caixas. Isso segue a regra de 0 ("um diagrama escolhe desenhar um ou outro, e diz qual").
- **Atores dentro do grupo "Quem chega":** a seção 5.1 põe os atores num grupo. Desenhei esse grupo fora da caixa do par, porque 2 diz que "o par não é ator" e 5.1 diz que eles agem "de fora dos grupos". Mistura de atores e componentes, em um mapa de grupos, é decisão minha.
- **Ligação 1 (Quem chega ↔ Portas):** o Desktop entra pela ponte, e clientes pela porta de leitura. Juntei as três no mesmo traço. Base: 3.4 e 8.10.
- **Ligação 2 e 3 (Quem chega ↔ Disciplina e Ferramentas):** não estão em 6. Vêm de 8.3 (o contrato chega ao agente) e de 3.4 e 8.4 (recruta abre na pasta do papel).
- **Ligação 10 (Vigilância → Disciplina):** o estado curto vem de 6 ("Estado curto e nota de retomada → Checagem de sessão"). Desenhei a seta por baixo do grupo Conteúdo para não cruzar a caixa.
- **Ligação 11 (Disciplina ↔ Ferramentas):** baseada em 3.1 (hooks rodam na configuração do usuário) e em 6 (checkpoint lê a memória privada). Não há frase única que a diga.
- **Ligação 13 (Núcleo ↔ Rede privada ↔ Outro par):** juntei três linhas de 6 ("Banco local do par A → par B", "Rede privada") numa só. Desenhei o trecho Rede ↔ Outro par como traço tracejado sem badge.
- **Ligação 12 (Periferia → GitHub):** a cópia diária é disparada pelo agendador, que não está desenhado. Desenhei direto do grupo Periferia, que tem a cópia local.
- **Não desenhei** Gustavo → Obsidian, Agentes → FreeLLMAPI, Busca → Embeddings, Agendador e Vault (ver a lista no HTML). Foi escolha de espaço, não de regra.
- **Estados dentro do desenho:** só marquei "guarda de versão: a construir" na Porta do banco. Os demais estados ficaram nas fontes da lista de ligações. Fica incompleto para quem quer o estado de cada caixa.
- **Lugar de Tailscale da empresa:** pus na faixa de fora do par, como manda 5.1, embora 5.2 diga que o notebook é o lugar. Mantive a regra do grupo e anotei o risco.

## Ambíguo

- **Desktop:** 5.1 diz que ele é "quem chega" e também que "roda na máquina, não fora dela". Desenhei como ator fora do par, com a ponte dentro de Portas. Onde: 5.1, "Claude Desktop"; 5.2, "Apps".
- **Kit de par:** 3.1 põe em "Disciplina do agente" (tabela) e 4.3 também; 5.1 põe em "Periferia do par". Escolhi Periferia. Onde: 3.1, 4.3, 5.1.
- **Script do `_archive/`:** 3.1 e 4.3 põem em Disciplina; 5.1 põe em Periferia. Escolhi Periferia. Onde: 3.1, 4.3, 5.1.
- **Checagem de sessão:** 3.1 põe em Disciplina; 5.1 põe em Vigilância e em Disciplina; a própria caixa diz "Vigilância (mostra o estado)" e "disciplina (abre a nota)". Escolhi Disciplina, com "+ Vigilância". Onde: 3.1, 5.1, "Pertence a mais de um grupo".
- **Obsidian:** 5.1 põe em Periferia e em Interfaces do Gustavo; 2 diz que ele "pode ficar fechado" (periferia) e também que é escritor do disco quando aberto. Escolhi Interfaces, com "+ Periferia". Onde: 3.1, 5.1.
- **Mod de estado e notificação:** 5.1 põe em Interfaces e em Vigilância; 3.1 só em Vigilância. Escolhi Vigilância. Onde: 3.1, 5.1.
- **Contrato:** 5.1 põe em Conteúdo e em Disciplina, e a regra de conteúdo ("replica como os outros") e a de disciplina ("é a regra") não dizem qual é o primário. Escolhi Disciplina, com "+ Conteúdo". Onde: 5.1, "Pertence a mais de um grupo".
- **Tailscale da empresa:** 5.1 põe em "Fora do par" ("ficam fora das duas cópias"), e 3.3 e 5.2 põem no notebook. Não é claro se "fora" quer dizer "fora do lugar" ou "fora da cópia". Onde: 3.3, 5.1, 5.2.
- **Vigia e Vigilância:** 5.2 põe a vigia como tarefa agendada (lugar), e 5.1 põe em Vigilância (grupo). Não há conflito, mas o diagrama precisa escolher; desenhei o grupo. Onde: 5.1, 5.2.
- **Pasta do papel:** 3.1 põe na seção "Periferia e máquina"; 5.1 põe em Ferramentas da máquina; 5.2 põe no disco, na pasta do workspace. Escolhi Ferramentas da máquina, por 5.1. Onde: 3.1, 5.1, 5.2.
