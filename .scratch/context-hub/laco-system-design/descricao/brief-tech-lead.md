# Brief do Tech lead: a descrição de design do hub (etapa 3)

Do maestro, 2026-10-15. Leia `proposta.md` e `plano.md` desta pasta: você escreve a descrição nova do hub, que
substitui o `texto-do-hub.md` como fonte de todo diagrama.

## Por que refazer

O Gustavo (rodada 5 do laço) disse que o texto atual limita o hub ao que o maestro e o Tech lead decidiram. Qualquer
agente desenha o que está escrito, não o que acontece na prática. O texto tem só dois eixos, componentes e ligações, e
um diagrama qualquer pede mais. A pergunta dele: "esta descrição consegue ser usada para criar **qualquer** tipo de
diagrama? Ela é rica e genérica o bastante?". O system design deve ser técnico e prático ao mesmo tempo.

## O que escrever: `descricao-do-hub.md`, nos sete eixos

1. **Atores:** quem age (o Gustavo, cada tipo de agente, o maestro, o outro par, o cliente, os processos agendados e os
   hooks), com o que cada um quer.
2. **Componentes:** o que existe e o papel numa frase (o inventário do `texto-do-hub.md` serve de ponto de partida, não
   de forma).
3. **Responsabilidade:** para cada componente, quem é dono, quem o aciona, quem o lê, quem só o vê. Uma tabela.
4. **Pertencimento:** a que grupo lógico cada coisa pertence e por quê, inclusive quando pertence a mais de um; e onde
   ela vive de fato (no disco, no banco, na sessão do agente, na configuração da ferramenta, fora das máquinas).
5. **Ações práticas:** o que cada ator faz no dia a dia, com as palavras dele, ligado ao caminho técnico que a ação
   dispara.
6. **Cenários:** sequências numeradas, do gatilho ao fim, com as falhas no caminho. Cubra pelo menos: editar uma nota
   (no Obsidian e no disco), um agente novo abrindo sessão, um maestro novo, pedir a um agente ler, alterar ou remover,
   o outro par alterar, buscar, um cliente consultar, uma colisão, a máquina desligada, a cópia diária.
7. **Estado de cada afirmação:** decidido (com o título do ticket), prática (o que o Gustavo faz, quando a fonte diz),
   a decidir, não verificado.

Escreva para quem nunca viu o hub e para qualquer modelo, não só para você. Prosa curta com tabelas; nada de detalhe de
implementação que não mude o desenho.

## Fontes

- `.scratch/context-hub/map.md` (Decisions so far inteiro: hoje entraram "Modelos de embeddings da busca" e "Camada de
  busca"), os tickets resolvidos, `GLOSSARY.md`, a exploração §7.1 e §9 como fundo.
- `perguntas/visiveis.jsonl`: 237 perguntas de muitas lentes e tipos. Não as responda uma a uma no texto. Use-as para
  descobrir o que a descrição precisa conter: cada pergunta que você não conseguiria responder com o texto é um eixo ou
  uma linha que falta. Mais perguntas visíveis podem chegar depois (do gateway); o maestro avisa.

**Não leia:** `perguntas/escondidas.jsonl`, nada em `perguntas/haiku/` nem `perguntas/gateway/`, o ticket 56, as rodadas
do laço do system design e a caixa do portal. As escondidas são o teste da sua descrição; se você as vir, o teste não
vale.

## O que só o Gustavo sabe

O que é prática e as fontes não dizem, não invente: marque "a decidir com o Gustavo" e liste em
`perguntas-ao-gustavo.md` (no máximo 15, as que mais mudam o desenho, cada uma com por que importa). Elas viram uma
rodada.

## Entrega

`descricao-do-hub.md` e `perguntas-ao-gustavo.md` nesta pasta. Grave só em `laco-system-design/`. Ao terminar:
`maestri ask "Claude Code" "pronto: <caminho> e quantas perguntas ao Gustavo"`.
