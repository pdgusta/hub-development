# Parecer do Tech lead, porta da amostra, volta 2

2026-10-15. Peça: `amostra/amostra.html` (volta 2), com `consertos.md` e `decisoes.md` (13 a 19). Fonte:
`descricao/descricao-do-hub.md` (v3.2). Escopo (brief): o meu conserto da volta 1 e se os consertos mudaram o conteúdo
aprovado. Não reabro o que já passou.

Evidência usada:
- comparação por programa entre `amostra-v1.html` e `amostra.html`: objeto das fichas (`G`), objeto dos cenários (`C`),
  `data-ligacao`, `data-item` e todos os textos do SVG;
- o código das etiquetas novas e a linha `Checkpoint → Agentes` no SVG;
- o relatório do QA (`qa/amostra-2/relatorio.md`).

---

## 1. O meu conserto da volta 1

| # | Conserto | Situação | Conferido em |
|---|---|---|---|
| 1 | Claude Desktop e Cliente na camada de detalhe (opcional) | **feito.** Ao aproximar, "Claude Desktop" aparece embaixo do Gustavo e "Cliente" embaixo dos Agentes. As duas etiquetas abrem a ficha "Quem chega ao hub" já no item. Não somam rótulo à vista inicial (27, igual). Bate com 5.1, que diz que o Desktop é o Gustavo pelo app e roda na máquina, e o cliente é o agente numa sandbox. As duas etiquetas têm o nome da seção 2. | código da camada de detalhe; QA: 42 de 42 etiquetas com lugar |

---

## 2. Os consertos mudaram o conteúdo aprovado?

**Não.**

| O que | v1 x v2 |
|---|---|
| Fichas (`G`): componentes, dono, aciona, lê, só vê, aprova, também em, selos, ligações | **iguais** (só mudou a quebra de linha, conserto 6 do Prumo) |
| Cenários (`C`): 39 passos, frases e o que cada passo acende | **iguais** |
| `data-ligacao` e `data-item` do desenho | **iguais**. As duas diferenças achadas estão num comentário e num molde de código, não no desenho. |
| Textos do SVG (rótulos) | **iguais**: 27 na vista inicial |

**O que mudou de posição e se o papel se mantém:**
- **Checkpoint → Agentes num traço só com o Contrato** (decisões, 15; conserto 6 do UX). A linha é de cenário e
  acende em "agente novo" 6 e "altere" 6. As duas são "regras e hooks", da mesma cor, e chegam ao mesmo ator: juntar
  não troca quem aciona quem. Em "altere" 6 o traço acende sem o Contrato. A frase diz "o checkpoint cobra o agente",
  então não se confunde com o contrato. Bate com 3.1 (Checkpoint obriga o agente). Aceito.
- **A linha do maestro entra na Biblioteca do Maestri pela direita** (conserto 7 do UX). Mesma ligação (4.5:
  o maestro cria e reescreve papéis); só o ponto de entrada mudou. Sem efeito no papel.
- **Folga das etiquetas e enquadramento** (decisões 13, 14, 16 e 17). É posição e zoom, não conteúdo.

---

## 3. As três regras

- **R4 Nomes: passa.** Evidência: 27 rótulos iguais aos da volta 1; 42 etiquetas, as 40 da volta 1 e as duas novas,
  todas com nome da descrição (seções 2 e 3).
- **R5 Papel na cidade: passa.** Evidência: nenhuma ligação nem papel mudou; o traço comum de Contrato e Checkpoint
  mantém quem aciona (acima).
- **R6 Forma nova: passa** (volta 1). A forma é a aprovada.
- R1, R2, R3: não é do meu papel. (QA: igual à volta 1; na camada de detalhe, menor espaço entre textos de 9,5 a 10
  px, já apontado ao UX revisor.)

| Dimensão | Nota | Por quê |
|---|---|---|
| 4 Nomes | 5 | Nada a consertar. |
| 5 Papel na cidade | 5 | Nada a consertar. |
| 6 Forma nova | 5 | Nada a consertar. |
| 7 a 12 | não é do meu papel | UX revisor. |

**Veredito, nas minhas regras: passa.** Consertos: nenhum meu.

---

## 4. Fora do meu papel, para registro

O arrasto com um dedo anda 12 px e para (QA, seção 1). Não é das minhas regras: é do Prumo e do UX revisor. Duas
coisas, porém, tocam no que a peça afirma:
- o `amostra.md` (tabela "Como navegar") promete "arrastar com um dedo" para andar;
- o `consertos.md` (Prumo, item 1) dá o arrasto com um dedo como conferido.

Ou o defeito se corrige, ou os dois textos deixam de afirmar o que a peça não faz. O Gustavo pediu o canvas para o
portal ao lado do terminal, com mouse, então o defeito não tira o conteúdo do lugar. Mas o texto não pode afirmar o
que não acontece.
