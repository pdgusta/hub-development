# Nota de retomada com várias sessões no mesmo trabalho (proposta do maestro, 2026-10-16)

**O problema (Gustavo, 2026-10-16):** "às vezes é o maestro que vai ser limpo, às vezes é uma sessão sozinha, às vezes
é um recruta, e todos atualizam o hub quando necessário. Todos mantendo e atualizando a mesma nota de retomada fica
estranho, e todos editando cada um a sua própria nota também fica estranho." Revisar depois, antes do ticket 18
(retomada).

**O que está decidido** ("Contrato file-first", ticket 10): cada trabalho tem **uma** nota de retomada, curta, com sete
campos, sobrescrita; o hook ao fim de cada resposta obriga a mantê-la em dia. Não diz quem escreve quando há várias
sessões no mesmo trabalho.

## Proposta: a nota do trabalho e as passagens

1. **A nota do trabalho continua uma só** e guarda o estado do trabalho, não de quem trabalha. Só quem **conduz** a
   sobrescreve: o maestro, quando há time; a própria sessão, quando ela está sozinha.
2. **Cada sessão que não conduz** (um recruta, uma sessão paralela) escreve a sua **passagem**: os mesmos sete campos, só
   da parte dela, sobrescrita, num arquivo dela ao lado da nota.
3. **O hook de fim pergunta pela nota de quem está respondendo:** quem conduz → a nota do trabalho; quem não conduz → a
   sua passagem. (Pendente já registrado: o sinal do Maestri não distingue maestro de recruta; o papel resolveria.)
4. **Quem conduz absorve as passagens** na nota do trabalho e apaga a passagem quando a sessão termina ou sai do canvas.
5. **Quem começa lê** a nota do trabalho e, se for retomar uma parte, a passagem daquela parte.

**É o que já funciona hoje na prática:** o maestro mantém `retomada-maestro.md` (a nota de quem conduz), e cada recruta
grava o seu estado no `## Comments` do ticket e no relatório da etapa (as passagens), que o maestro absorve.

## Alternativas

- **Uma nota só, com uma seção por sessão:** todos gravam no mesmo arquivo (colisão de gravação, a nota cresce e deixa
  de ser curta).
- **Uma nota por sessão, sem nota do trabalho:** ninguém gravaria por cima de ninguém, mas quem chega não sabe qual ler
  e o estado do trabalho fica espalhado.

## O que muda se for aceita

O ticket 18 (retomada) ganha a passagem e a regra de quem conduz; o núcleo de seis arquivos da iniciativa pode precisar
de um lugar para as passagens (decisão de "Arquitetura de pastas"), e a regra do contrato global diz quem escreve o quê.
