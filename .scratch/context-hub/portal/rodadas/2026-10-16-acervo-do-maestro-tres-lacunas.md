---
titulo: Acervo do maestro: as três lacunas de dono
ticket: 16
aberta: 2026-10-16
estado: absorvida
---

A Vela está no ticket 20: a família de skills `maestro-*` (o **acervo do maestro**: papéis, receitas de setup,
contratos-opção) e a **guarda** que protege esse acervo. Em "Acervo do maestro" você decidiu as regras de aval: o maestro
acrescenta sozinho uma peça nova ou uma variante, mas **pede o seu aval** para alterar ou apagar uma peça que já é usada,
mexer num catálogo ou acrescentar algo com nome parecido. Antes de alterar, **um verificador em outro modelo** confere a
mudança, e a tela de aval mostra o antes e depois, quem é afetado e a recomendação dele.

Três pontos ficaram sem dono desde a passagem para a construção e voltam agora, como o plano previa:

**1. Onde fica o registro de cada aval.** Quando você aprova uma mudança no acervo, algo precisa guardar o que mudou,
quando, e o que o verificador disse, para o maestro e você poderem consultar depois.

**2. Quem escolhe o modelo do verificador.** A regra diz "outro modelo", mas não diz qual nem quem escolhe.

**3. Como chega a você o erro de uma peça que sumiu.** Se um catálogo cita uma peça que não existe mais (apagada ou
renomeada), alguém precisa ficar sabendo.

## Onde fica o registro de cada aval
id: registro-do-aval
tipo: escolha
recomendada: A

- A: Um arquivo por aval em `agents/maestro/avais/AAAA-MM-DD--<peça>.md`, gravado pela guarda quando você aprova: o antes e depois, quem é afetado, o relatório do verificador e a sua decisão; replica nas duas máquinas e fica fora da guarda (só a guarda escreve ali)
- B: Uma linha por aval numa tabela única, `agents/maestro/avais.md` (data, peça, decisão, onde está o relatório do verificador); mais curto de ler, mas o antes e depois fica só no git
- C: Só no histórico do git do hub (a mensagem do commit da mudança diz quem aprovou); nada a mais para manter, mas consultar exige o git

## Quem escolhe o modelo do verificador
id: modelo-do-verificador
tipo: escolha
recomendada: A

- A: Uma regra fixa, escrita uma vez numa peça do próprio acervo (sob a guarda): o verificador usa um modelo de família diferente da do maestro (maestro Claude → verificador GPT, por exemplo), e só você muda essa regra, com aval
- B: O maestro escolhe a cada vez, desde que seja um modelo diferente do dele, e diz qual usou no pedido de aval
- C: Você escolhe a cada pedido de aval, na própria tela

## Como chega a você o erro de uma peça que sumiu
id: peca-que-sumiu
tipo: escolha
recomendada: A

- A: Vira item da vigia (no `estado.json`): aparece no início da próxima sessão e na tela de estado, e a notificação do Windows sai se o estado piorar, como os outros alertas
- B: O maestro avisa no terminal, numa linha, na próxima vez que abrir o acervo
- C: Só o verificador de forma acusa, nos testes e na manutenção; ninguém é avisado na hora

## Algo mais?
id: algo-mais
tipo: texto
