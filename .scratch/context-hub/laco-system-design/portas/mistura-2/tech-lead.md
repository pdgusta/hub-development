# Parecer do Tech lead, porta da mistura, volta 2

2026-10-15. Peça: `conceitos/mistura/mistura.html` (volta 2), com `consertos.md` e `decisoes.md` (14 a 21). Fonte:
`descricao/descricao-do-hub.md` (v3.2). Escopo (brief): os meus 11 consertos da volta 1 e o que eles criaram de novo.
Não reabro o que já passou.

Evidência usada:
- captura do QA a 1280 px (`qa/mistura-2/captura-1280.png`) e o relatório (`qa/mistura-2/relatorio.md`);
- os elementos acesos por passo (`qa/mistura-2/cenarios/resumo-cenarios.txt`), conferidos contra 8.1 a 8.8;
- os dados das fichas (objeto `G`), lidos do HTML: componentes, matriz, selos e ligações;
- os elementos acesos sem marcação (QA, problema 2): o `path` é o halo de fundo (`lig-fundo`) da linha Agentes → Vista
  Markdown; os dois `rect` são quarteirões da miniatura do outro par. Decoração, não ligação: R1 não perde nada.

---

## 1. Os meus consertos da volta 1

| # | Conserto | Situação | Conferido em |
|---|---|---|---|
| 1 | Linha roxa Checkpoint → Nota de retomada | **feito de outro jeito, aceito.** A nota recebe a linha azul Agentes → Nota de retomada (quem grava, 4.4); o checkpoint chega a ela pelo traço "confere, só lê" (4.3, "Lê: nota de retomada"). A roxa Checkpoint → Agentes saiu do desenho e ficou na ficha (decisões, 14). Ver item novo A. | captura 1280; ficha da Disciplina; "agente novo" 6 e "altere" 6 acendem a azul e a de conferir |
| 2 | Ferramentas da máquina sem linha | **feito pela saída que dei** ("se não couber na visão geral, a linha existe só no cenário"). Maestro → Biblioteca do Maestri acende em "maestro novo" 4. Os dois ícones viraram componentes com nome: a caixa é a configuração de cada ferramenta; o caderno, a biblioteca do Maestri. Na ficha, as duas ligações da descrição (Maestro → biblioteca; Checkpoint → memória privada). | `resumo-cenarios.txt`, maestro-novo 4; ficha de Ferramentas |
| 3 | "Maestro novo", passos 4 a 6 sem linha | **feito.** 4 acende a biblioteca e a linha até ela; 5 acende o Acervo (o registro de uso mora em `agents/maestro/uso/`, 3.2); 6 acende a Disciplina e Maestro → Gustavo, com a frase da guarda, do verificador e do aval. O aval sai do maestro: é o que 7.3 diz ("pede aval, com a tela"). Aceito (decisões, 16). | maestro-novo 4 a 6 |
| 4 | "Remova", passos 2 e 3 | **feito.** 2 acende a troca entre pares (o script lê o estado do outro par, 4.3); 3 acende Agentes → Vista Markdown no tracejado "a decidir", e a frase diz que por onde o script grava está em aberto. | pede-remover 2 e 3 |
| 5 | Selos da rodada 8 | **feito.** "Não verificado: como o Obsidian chega à busca do hub" na Camada de busca e nas ligações Obsidian → busca (Portas e Interfaces); "a decidir: por onde o Desktop chega à busca" na Camada de busca e na ligação do Desktop. Bate com 8.9. | fichas de Portas e Interfaces |
| 6 | Sentido das ligações | **feito.** Vista Markdown ↔ Sincronizador, Sincronizador ↔ Banco local, Banco local ↔ Outro par; a frase de "altere" 4 diz quem escreve no disco. Bate com a seção 1 e a seção 6. | marcação; pede-alterar 4 |
| 7 | "Edita" 5 e "leia" 4 sem nada novo | **feito.** "Edita" 5 acende os quarteirões da vista e da busca na miniatura do outro par (8.1, passo 5); "leia" 4 acende Gustavo → Agentes (8.5, passo 4). Ver item novo B. | gustavo-edita 5; pede-ler 4 |
| 8 | Um componente e quatro selos | **feito.** Catálogo de blocos e skill "nova iniciativa" na ficha de Conteúdo, com dono, aciona, aprova e "em curso" (3.2; 4.4). Os quatro selos estão: proteção do `_archive/` e aviso de caminho mudado (Raiz), peça que sumiu (Acervo), porta do banco fora (Porta do banco). | fichas de Conteúdo e Portas |
| 9 | Fonte v3.2 | **feito.** `mistura.md` e `decisoes.md` citam a v3.2; o item 10 diz "confirmada pela v3.2". | os dois `.md` |
| 10 | Vigia → Banco local lê como ação | **feito.** Mesmo traço "confere, só lê" do checkpoint; a legenda diz "confere, só lê". Bate com 4.2 (a vigia está em "Lê"). | captura 1280; legenda |
| 11 | Marca do Claude Desktop (opcional) | **não feito, aceito.** O motivo se sustenta: uma marca sem linha seria um componente solto, o defeito que este laço corrige. O Desktop fica na ficha "Quem chega", com as duas ligações e os dois "a decidir". | decisões, 20 |

---

## 2. O que os consertos criaram de novo

**A. O checkpoint não liga mais ao agente na visão geral.** Com a roxa Checkpoint → Agentes fora do desenho, a
cancela só "confere" a nota. A obrigação que ela impõe ao agente (3.1: "obriga o agente a continuar e gravar"; seção 6,
"Checkpoint | Agente → nota de retomada") se lê pelo triângulo agente grava, checkpoint confere, e a frase do passo
diz o resto. Não contradiz o papel: a cancela de fiscalização confere o quadro, e quem escreve é o agente. Mas a
Disciplina do agente volta a chegar ao agente só pelo Contrato, e foi justamente a ligação da disciplina ao agente que o
Gustavo pediu. Conserto pequeno: a linha só no cenário, como a do maestro à biblioteca (conserto 1 abaixo).

**B. A marca do passo 5 de "o Gustavo edita" não aparece** (QA, problema 1: 4 marcas no passo 5 e 5 no passo 6). O
passo acende certo (miniatura do outro par), mas sem o número o trajeto pula do 4 para o 6. Não é das minhas regras;
registro porque impede ler o cenário que segue 8.1. Conserto 2.

**C. O resto confere.** A ordem dos sete cenários segue 8.1, 8.3, 8.4, 8.5, 8.6, 8.7 e 8.8; os passos de falha (com
o triângulo) são os que a descrição dá como falha ou em aberto: colisão (8.1, 8.8), aviso de conflito a construir
(8.5), gravar no disco sem versão (8.6, "Como os agentes gravam no hub"), quem confere os 30 dias (8.7). "Maestro novo"
5 usa a linha Maestro → Acervo para o hook de uso: quem aciona o hook é o uso de uma peça pelo maestro (4.3), então a
linha não engana. Sem conserto.

---

## 3. As três regras

- **R4 Nomes: passa.** Evidência: os 25 rótulos do desenho são os mesmos da volta 1; os dois ícones de Ferramentas
  ganharam o nome do componente no título e na ficha (rótulos da seção 3.1, "Biblioteca do Maestri" e configuração de
  cada ferramenta), sem rótulo novo no desenho.
- **R5 Papel na cidade: passa.** Evidência: a nota recebe a linha de quem grava (o agente, 4.4) e o traço de quem só
  confere (checkpoint, 4.3); a torre de vigia só olha o cofre (4.2); a cor segue "quem aciona" sem exceção no desenho;
  o bairro de Ferramentas ganha caminho no cenário que o usa. Ressalva: item novo A.
- **R6 Forma nova: passa** (volta 1). Os consertos não mudaram a forma.
- R1, R2, R3: não é do meu papel. (QA: 0 cruzamentos; 25 rótulos; razão entre grupos subiu de 1,53 para 1,68.)

| Dimensão | Nota | Por quê |
|---|---|---|
| 4 Nomes | 5 | Nada a consertar. |
| 5 Papel na cidade | 4 | Conserto pequeno, que não muda a leitura: a obrigação do checkpoint sobre o agente só na ficha e na frase. |
| 6 Forma nova | 5 | Nada a consertar. |
| 7 a 12 | não é do meu papel | UX revisor. |

**Veredito, nas minhas regras: passa.**

---

## 4. Consertos

Nenhum bloqueia a porta nas minhas regras.

1. [R5, pequeno] Cenários "agente novo" 6 e "altere" 6 — o checkpoint não aparece ligado ao agente → acender, só no
   cenário, uma linha roxa Checkpoint → Agentes (como Maestro → Biblioteca do Maestri, decisões 15), para que o passo
   mostre a cancela cobrando o agente e o agente gravando a nota. Se ela colar no roxo do contrato, basta acendê-la no
   passo e deixar o Contrato apagado nele. Evidência: 3.1 Checkpoint; seção 6, "Checkpoint | Agente → nota de
   retomada"; `resumo-cenarios.txt`, agente-novo 6.
2. [Cenário, fora das minhas regras] "O Gustavo edita", passo 5 — a marca numerada não é desenhada → desenhar o 5 junto
   à miniatura do outro par (o passo acende só elementos sem rótulo, e o número parece não achar onde ficar).
   Evidência: QA, problema 1 (4 marcas no passo 5, 5 no passo 6).
