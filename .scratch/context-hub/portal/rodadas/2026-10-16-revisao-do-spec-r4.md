---
titulo: Como o spec fica depois da revisão conversada
ticket: 16
aberta: 2026-10-16
estado: absorvida
---

Os três revisores fecharam as 5 rodadas com **acordo em tudo** (`.scratch/construcao-do-hub/revisao/acordo.md`).
Comparei as duas versões: a de antes está intacta em `revisao/antes/`, e a proposta (`revisao/proposta/`) muda os 6
arquivos, com cerca de 340 linhas novas e 210 tiradas. Conferi o núcleo trecho a trecho: cada mudança bate com o acordo
e cita o ticket resolvido de onde vem.

**O que a proposta muda:**

- Corrige o que contrariava tickets resolvidos. Exemplos: a guarda do acervo deixa de fora as propostas do Codex e do
  Copilot e o registro de uso; o GSD sai do escopo global; a pasta global de skills leva só as de uso geral; sem a vigia
  e sem o MCP, a checagem de início diz "estado indisponível"; a ponte do Claude Desktop tem o mesmo texto em todo lugar.
- **Três itens que estavam como "se couber" viram obrigatórios**, porque os tickets os pedem: a validação de frontmatter
  no MCP do banco, o Config Doctor na vigia e a ponte do Claude Desktop. A construção fica maior.
- O aviso em dobro no Codex, que perguntei antes, já estava decidido: os dois avisos ficam (decisão do acesso dos
  agentes). Só uma eventual regra de repetição é escolha (item 22 abaixo).
- Marca o que depende do formato da execução (vai para a rodada do plano) e o que vem do laço do system design (fica
  fora da construção, como você disse).

**As 23 escolhas que o núcleo do spec fez sem ticket resolvido** (ficaram na proposta, marcadas, esperando você):

1. Conflito visível de dois jeitos: aviso ao ler a nota e uma ferramenta que lista os conflitos abertos.
2. O texto que o MCP entrega ao agente sai de um bloco marcado no `AGENTS.md`, relido a cada conexão, sem cópia.
3. A regra curta das ferramentas de gravação ganha a frase "grave com a versão lida; conflito = releia e refaça" só onde
   a ferramenta leva a versão; apagar e mover ficam a definir.
4. O nome `estado_do_hub` para a ferramenta de estado do MCP.
5. Duas instâncias do MCP do banco por máquina (leitura e escrita), a de escrita servindo também ao cliente.
6. O estado da vigia num arquivo local (`.local/vigia/estado.json`), com nível por item e o geral igual ao pior.
7. A vigia usa o endereço da outra máquina só como sinal; o que for incerto vira, no mínimo, "informa", com o motivo.
8. Falha da cópia diária: o script sai com erro e a vigia ganha um item com notificação.
9. A data do arquivamento vai no nome da pasta arquivada.
10. A limpeza da pasta de arquivo roda na tarefa diária (o prazo de 30 dias fica fora, vem do laço do system design).
11. Aceite da busca: a nota certa entre as 3 primeiras, e uma nota nova encontrável em até 60 segundos.
12. Relatório da busca com quantas notas entraram e quais ficaram fora por frontmatter quebrado.
13. A exclusão de tudo que tem ponto no nome, pela configuração da própria busca.
14. O verificador só completa campos que se calculam, trocando um trecho e relendo o arquivo logo antes de gravar.
15. O hook de gravação monta o arquivo final antes de validar o frontmatter.
16. O registro de fim de resposta roda sem modelo nenhum.
17. Os hooks do acervo do maestro agem em qualquer pasta, dentro ou fora do hub, e a guarda decide pelo arquivo de
    destino.
18. No ensaio, o Copilot acha as skills por uma variável de ambiente, sem dispensar o passo de verdade.
19. O campo de iniciativa só é exigido onde o caminho mostra uma iniciativa.
20. O script "nova iniciativa" cria o `AGENTS.md` da iniciativa.
21. Caminho ofuscado no banco cifrado, como no teste de disco e banco sem o Obsidian.
22. Uma regra de repetição entre o aviso da vigia e o do Codex, se precisar.
23. A busca atrás do proxy aceita o endereço que o proxy de fato repassa.

Ficam para a rodada do plano: o que depende do formato, as três lacunas de dono que seguem abertas (onde fica o registro
do aval de mudança no contrato, quem escolhe o modelo do verificador da guarda, como chega a você o erro de peça que
sumiu) e o aval para os bancos de ensaio no Docker.

## A proposta vira o spec
id: proposta
tipo: escolha
recomendada: A

- A: Sim: a proposta substitui o spec (a versão de antes fica guardada para comparação), com as 23 escolhas decididas na pergunta abaixo
- B: Antes quero ver as mudanças por bloco, em rodadas, para aprovar uma a uma

## As 23 escolhas sem ticket
id: escolhas
tipo: escolha
recomendada: A

- A: Aceitar as 23 como estão
- B: Aceitar todas menos as que eu citar pelo número no "Algo mais?"

## Algo mais?
id: algo-mais
tipo: texto
