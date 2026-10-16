# Parecer do Tech lead, porta da mistura, volta 1

2026-10-15. Peça: `conceitos/mistura/mistura.html`, com `mistura.md` e `decisoes.md`. Fonte: `descricao/descricao-do-hub.md`
(v3.2). Roteiro: `suite/skills/regua-da-cidade/como-julgar.md`. Julgo R4, R5 e R6 e os itens do brief que são meus.

Evidência usada:
- captura do QA a 1280 px (`qa/mistura-1/captura-1280.png`) e o relatório (`qa/mistura-1/relatorio.md`);
- a marcação da peça: 17 `data-item`, 9 `data-grupo`, 20 `data-ligacao`, 37 elementos com `data-cenario`;
- os dados das fichas (objeto `G`) e dos cenários (objeto `C`), lidos do HTML;
- a ordem dos passos acesos (`qa/mistura-1/cenarios/resumo-cenarios.txt`), conferida contra 8.1 a 8.8 da descrição.

---

## 1. Os itens do brief

| Item | Situação | Evidência |
|---|---|---|
| Todo componente com dono e quem aciona visíveis | **passa, com uma falta** | Cada ficha traz dono, aciona, lê, só vê, aprova e "também em", fiéis à matriz da seção 4. Falta um componente: o catálogo de blocos e a skill "nova iniciativa" (3.2; 4.4). Conserto 8. |
| Nenhum componente solto | **falha** | O bairro "Ferramentas da máquina" não tem nenhuma linha. A descrição dá três ligações dele (seção 6 e "Ligações entre grupos"): o maestro cria e reescreve papéis na biblioteca do Maestri; o checkpoint lê a memória privada; o recruta abre na pasta do papel. Conserto 2. |
| Grupos batem com a descrição | **passa** | Os nove bairros são os grupos de 5.1, cada componente no grupo principal, com a bolinha do segundo (Contrato em Conteúdo; Nota de retomada e Acervo em Disciplina; Obsidian em Periferia). "Quem chega" fica fora da muralha, como 5.1 manda. |
| Ligações batem com a descrição | **passa, com dois desvios** | 20 ligações, todas na seção 6. Desvio 1: a linha roxa Checkpoint → Nota de retomada (conserto 1). Desvio 2: Obsidian → Camada de busca desenhada como fato, quando o caminho é não verificado (conserto 5). |
| Cinco cenários na ordem certa | **passa na ordem; falha no caminho em dois** | Os sete cenários seguem 8.1, 8.3, 8.4, 8.5, 8.6, 8.7 e 8.8 passo a passo, na mesma ordem. Mas "maestro novo" (passos 4, 5 e 6) e "remova" (passos 2 e 3) acendem bairros sem linha: o caminho não se forma. Consertos 3 e 4. |
| A busca como porta do conteúdo | **passa** | A linha mais grossa é a de buscar; agentes, o Gustavo (pelo Obsidian) e o Claude Desktop (na ficha) chegam ao conteúdo por ela; a busca lê a vista. Seção 1, "Duas coisas que não se confundem"; 8.9. |
| O Gustavo chega pela vista Markdown | **passa** | Gustavo → Obsidian → Vista Markdown; nenhuma linha dele ao banco. Cenário "o Gustavo edita" segue 8.1: Obsidian grava o `.md`, o sincronizador (ou o plugin) leva ao banco. |
| Itens "a decidir" com selo | **passa, com faltas** | Os "a decidir" das fichas batem com a descrição e com as lacunas de 11 e 13. Não há item "a decidir com o Gustavo" aberto na v3.2 (as perguntas 15, 16 e 17 fecharam na rodada 8). Faltam quatro selos (conserto 8) e um "a decidir" na ligação do Desktop à busca (conserto 5). |
| Rodadas 7 e 8 refletidas | **passa** | O Gustavo e o Claude Desktop usam a busca (ficha de Portas e "Quem chega"); recuperar pela cópia do GitHub com dois dias de distância (ficha de Fora do par); conteúdo de cliente pode ir aos modelos na nuvem (ficha dos embeddings); operação por um agente com o Gustavo vendo. |

---

## 2. As três regras

- **R4 Nomes: passa.** Evidência: os 25 rótulos do desenho são os rótulos da seção 3 (Banco local, Vista Markdown,
  Sincronizador, Porta do banco, Camada de busca, Vigia do sync, Contrato, Checkpoint, Nota de retomada, Acervo do
  maestro, Obsidian, Rede privada, Outro par), os nomes dos grupos de 5.1 e três atores da seção 2. O relógio do
  Agendador do Windows não tem rótulo, mas tem nome no título e na ficha. "Componentes" nos textos; "peça" só no
  sentido de peça do acervo, que é o nome do glossário.
- **R5 Papel na cidade: falha.** Evidência:
  - a linha roxa Checkpoint → Nota de retomada, pela regra da própria peça ("cor = quem aciona"), diz que o hook grava
    a nota. A descrição diz o contrário: "o hook não grava; o agente grava" (3.1, Checkpoint); quem aciona a nota é "o
    agente da sessão, obrigado pelo checkpoint" (4.4). É o mesmo tipo de erro que o Gustavo apontou na B (uma linha
    que não é a prática). Nenhuma linha azul chega à nota;
  - o bairro "Ferramentas da máquina" fica solto, sem linha (item do brief);
  - o resto da tabela de papéis combina com o hub: cofre como verdade, vitrine como vista, casa de máquinas entre os
    dois, torre que só olha, relógio que põe a casa de máquinas e a torre para trabalhar, prefeitura das regras,
    cancela que cobra o agente, armazém de opções, outro par como a mesma planta.
- **R6 Forma nova: passa.** Evidência: a base B foi escolha do Gustavo (rodada 5), então não é a "outra roupa" que a
  regra recusa. O que muda a leitura é novo: a linha sai de quem aciona e se segue pela cor, e o cenário acende o
  trajeto passo a passo. Teste de troca de acabamento: tirando cor e ícones, a B não responde "quem aciona isto?" nem
  "o que acontece se…?"; a mistura responde.
- R1, R2, R3: não é do meu papel. (QA: R2 em 25 exatos; razão entre grupos 1,53 contra 1,5. Os consertos 2 e 3 somam
  linhas; não podem somar rótulo.)

| Dimensão | Nota | Por quê |
|---|---|---|
| 4 Nomes | 5 | Nada a consertar. |
| 5 Papel na cidade | 2 | R5 em falha: uma linha diz que o hook grava a nota; um bairro solto. |
| 6 Forma nova | 5 | Nada a consertar. |
| 7 a 12 | não é do meu papel | UX revisor. |

**Veredito, nas minhas regras: volta.**

---

## 3. Lista de consertos

Primeiro o que falha nas regras e no brief; depois o resto.

1. [R5] Nota de retomada, linha roxa do Checkpoint — diz que o hook grava a nota → a linha que chega à nota sai de
   **Agentes**, em azul (quem grava); a roxa do Checkpoint vai só até o agente (já existe), ou fica até a nota num
   traço que diga "confere", diferente do traço de quem aciona. Os passos "agente novo" 6 e "altere" 6 acendem a azul.
   Evidência: 3.1 Checkpoint; 4.4 Nota de retomada; 6, linha "Checkpoint | Agente → nota de retomada".
2. [R5, brief] Bairro "Ferramentas da máquina" sem linha → ligar ao menos uma das ligações da descrição: Maestro →
   biblioteca do Maestri (cria e reescreve papéis) ou Checkpoint → memória privada (o checkpoint a lê). Sem cruzar
   outra linha; se não couber na visão geral, a linha existe só no cenário que a usa. Dar aos dois ícones do bairro o
   nome do componente no título (qual é a caixa, qual é o documento). Evidência: seção 6; "Ligações entre grupos",
   "Disciplina do agente → Ferramentas da máquina"; captura 1280, bairro sem linha.
3. [Cenário "maestro novo"] Passos 4, 5 e 6 acendem bairros sem linha → passo 4 acende a linha do conserto 2 (Maestro →
   Ferramentas); passo 5 acende o Acervo do maestro junto, porque o registro de uso mora em `agents/maestro/uso/`;
   passo 6 acende a Disciplina (guarda do acervo e verificador) e uma ligação até o Gustavo, e a frase diz a ordem:
   "No Claude Code, a guarda recusa, o verificador confere, e o Gustavo dá o aval". Evidência: 8.4, passos 4, 6 e 7 e
   "Falhas"; QA, passos sem linha.
4. [Cenário "remova"] Passo 2 acende Periferia e Outro par sem linha; passo 3 acende o sincronizador mas não a ação do
   agente → passo 2 acende a troca entre pares (o script lê o estado do outro par); passo 3 acende Agentes → Vista
   Markdown no tracejado "a decidir", porque por onde o script grava (disco ou porta do banco) não está decidido.
   Evidência: 4.3 Script do `_archive/`, "Lê: estado do outro par"; 8.7 passo 3; 8.6, "Como os agentes gravam no hub"
   [A].
5. [Selos, rodada 8] Ligação Obsidian → Camada de busca desenhada como fato; ligação "Claude Desktop → Camada de busca"
   na ficha de Portas sem selo → a linha do Obsidian fica (o uso foi decidido na rodada 8), com selo "não verificado"
   nas fichas de Interfaces e Portas: "como o Obsidian chega à busca do hub"; a ligação do Desktop leva o selo "a
   decidir": "por onde o Desktop chega à busca". Evidência: 8.9, "Quem usa a busca"; 4.1 Camada de busca.
6. [Cenários, sentido] "Altere" 4 e "outro par altera" 3 acendem "Vista Markdown → Sincronizador → Banco local" para um
   caminho que vai do banco ao disco; "outro par altera" 2 acende "Banco local → Outro par" para a troca que vem de lá
   → nomear essas duas ligações com "↔" na marcação e no título (são de dois sentidos), e a frase de "altere" 4 dizer
   quem escreve: "o sincronizador (ou o plugin) escreve no disco; a vista muda em cerca de 0,2 s". Evidência: seção 1,
   "Vista e banco se espelham nos dois sentidos"; seção 6, linhas 1, 4 e 5.
7. [Cenários] "O Gustavo edita" 5 e "leia" 4 não acendem nada novo (QA) → no 5, acender os quarteirões da vista e da
   busca dentro da miniatura do Outro par; no 4, acender de novo Gustavo → Agentes, porque o agente avisa o Gustavo.
   Evidência: 8.1 passo 5; 8.5 passo 4.
8. [Fichas] Faltam um componente e quatro selos → acrescentar o catálogo de blocos e a skill "nova iniciativa" na ficha
   de Conteúdo (dono Gustavo; aciona: agente cria pasta pela skill; aprova: Gustavo, para mudar a skill; em curso); e os
   selos "a decidir": proteção contra gravar dentro do `_archive/` e aviso de caminho mudado (Raiz, 8.7); como o erro de
   uma peça que sumiu chega ao Gustavo (Acervo, 8.4); o que o agente faz com a porta do banco fora (Porta do banco, 8.6
   e 13). Evidência: 3.2; 4.4; 8.4; 8.6; 8.7.
9. [Fonte] `mistura.md` e `decisoes.md` citam a v3.1, e o item 10 das decisões trata a rodada 8 como aviso do maestro
   "antes de a descrição ter a marca" → citar a v3.2 e a rodada 8 pela descrição. Conferi: o que a peça diz sobre a
   rodada 8 bate com a v3.2; o item 10 pode dizer "confirmado pela v3.2". Evidência: diferença entre v3.1 e v3.2.
10. [R5, pequeno] Linha laranja Vigia do sync → Banco local: pela regra "cor = quem aciona", lê como a vigia agindo no
    banco; ela só lê (4.2) → a legenda diz "vigia (confere)", ou o traço é o mesmo de "confere" do conserto 1.
    Evidência: 4.2 Vigia, coluna "Lê".
11. [Opcional] Claude Desktop e Cliente não estão no desenho, só na ficha "Quem chega". Aceito pelo teto de 25 rótulos.
    Se couber sem mexer na folga: uma marca sem rótulo junto ao Gustavo para o Desktop, com nome no título, como o
    relógio do Agendador. Evidência: 5.1, "Quem chega"; QA, R2 em 25.

Aceito como está, sem conserto: dono só na ficha (decisões, item 2; o brief admite "a um clique"); checagem de sessão,
script do `_archive/`, biblioteca do Maestri e hook de uso sem prédio, desde que os consertos 2 a 4 deem linha aos
passos deles; o tracejado "a decidir" em Agentes → Vista Markdown (gravar no disco é permitido; o caminho padrão e a
conferência de versão estão em aberto); sete cenários em vez de cinco.
