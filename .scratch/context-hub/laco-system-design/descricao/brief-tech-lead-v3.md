# Brief do Tech lead: descrição, volta 3

Do maestro, 2026-10-15. O teste da descrição v2 terminou, com perguntas novas (a metade escondida do gateway, que
ninguém viu):

- **241 escondidas**, respondidas por quem só leu a v2 e julgadas contra as fontes: das 200 que as fontes respondem,
  130 certas (**65%, igual à v1**), 63 parciais, 7 "a descrição não diz", 0 erradas. O "não diz" caiu de 22 para 7 e as
  erradas de 2 para 0, mas as parciais subiram de 49 para 63: a v2 cobre mais assuntos e ainda deixa a resposta pela
  metade. Resumo por eixo, com motivo e fonte de cada buraco, em `teste/resumo-volta-2.md` (sem as perguntas).
- Eixo mais fraco: **cenários (29)**, depois componentes (11), pertencimento (10), ações (6).

## O que fazer

Reescreva `descricao-do-hub.md` (guarde a v2 como `descricao-do-hub-v2.md`):

1. **Consertos do teste da v2, por eixo, não por pergunta.** O problema agora é a resposta parcial: leia os motivos do
   resumo e procure o padrão (o caso de borda que o cenário não leva até o fim, a exceção que não aparece junto da
   regra, o "o que acontece depois" que falta). Conserte a regra ou o cenário de forma que perguntas do mesmo tipo
   saiam inteiras.
2. **As respostas do Gustavo à rodada da prática:** `respostas-do-gustavo-v1.md`. Cada resposta vira afirmação com
   estado "decidido pelo Gustavo (rodada 7 do laço, 2026-10-15)" e entra no eixo certo; tire o "a decidir com o Gustavo"
   que ela fecha. Atenção a três delas: remover = mover para `_archive/` por 30 dias e depois apagar, e o agente só remove
   com a permissão dele ou depois dos 30 dias; binários (ele diz que o caso já foi tratado: é a rodada 71 de "Revisão do
   sync", em que a vigia avisa e recupera; confira no ticket); sessão fora do hub, como cliente, deve funcionar igual à
   da raiz (MCP da busca e as regras de gravação).
3. **Perguntas 15 e 16** (`perguntas-ao-gustavo.md`, v2): foram ao Gustavo numa rodada nova; até a resposta chegar, sigam
   como "a decidir com o Gustavo". Eu mando as respostas quando chegarem.
4. Se surgir pergunta nova que só o Gustavo responde, acrescente a `perguntas-ao-gustavo.md` como "v3".

Mantenha as regras dos briefs anteriores (`brief-tech-lead.md` e `brief-tech-lead-v2.md`): fontes, estado de cada
afirmação e a lista do que não ler, que segue valendo (as escondidas, `perguntas/haiku/`, `perguntas/gateway/`, o ticket
56, as rodadas do laço, a caixa). Pode ler `teste/resumo-volta-1.md`, `teste/resumo-volta-2.md` e `teste/diagramas/*.md`;
não leia `teste/fatias/`, `teste/respostas/`, `teste/julgamento/` nem nada em `teste/v2/` além do resumo.

Entrega: `descricao-do-hub.md` (v3) e uma lista curta `consertos-v3.md`, eixo por eixo, com uma seção para as respostas
do Gustavo. Ao terminar: `maestri ask "Claude Code" "pronto: <caminho>"`.
