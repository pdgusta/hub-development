# Portal do projeto: pedido e briefing

Pedido do Gustavo em 2026-10-14, chat Maestri (fio rosa). O texto vai inteiro, porque é a fonte do briefing:

> Senti que isso de ficar abrindo vários designs diferentes em htmls separados sob demanda, ficou um pouco
> desorganizado. Agora eu preciso de um Hub de todos os designs desse projeto, não deve ser só uma pagina com botões
> pra cada design. Deve ser o portal, o lugar onde eu abro e entendo o projeto, pra onde ele ta indo, consiga ver os
> designs e o por quê de existirem, agora não é uma peça visual informativa, é de fato como se fosse um web system
> que me permite também ver/entender e gerenciar o projeto. O system design também mora nele. Peça pro designer
> entender a solicitação e propor um tema que faça sentido. A ideia é além de eu ter o maestri aberto pra falar com o
> maestro, eu ter esse portal aberto num navegador não só pra entender, mas pra poder "gerenciar" o projeto nele. Hoje
> você maestro ta toda hora atualizando a nota aqui no maestri, mas pode atualizar algo ali no portal onde eu poderia
> só aprovar, responder e interagir la e você já receber minha resposta sem eu precisar ficar te respondendo aqui no
> chat.
>
> Quando eu digo "gerenciar" não quero dizer que o designer tem que criar um sistema de devops nele. Fica inviável
> sabe. É algo que pensei aqui e faz sentido pois é até uma ideia pra ter esse portal em todo workspace cujo objetivo
> é o desenvolvimento de algo.
>
> Nele não só o gerenciamento e resposta de tickets seriam um ganho real, mas também até quando eu peço proposta de
> estratégia de roteamento pro maestro, aparecer algo lá no portal, eu poder personalizar, alterar e responder lá no
> portal de forma "seamsly" sei lá como escreve.
>
> Se o designer precisar de ajuda, defina a melhor estratégia de "time" pra ele, seja por subagentes no terminal dele
> ou um agente "ajudante" aqui no maestri. Ele deve decidir tudo sozinho e eu opino no resultado final. Você maestro
> só me chama pra decidir algo crítico. Uma coisa "obrigatória" no processo de criação desse portal é um agente codex
> GPT-6.1 Sol Medium servindo como revisor que vai cooperar com o designer. Eles conversam entre si e o revisor te
> ajuda também no final com o portal criado

## Time

- **Designer**: Claude Opus 5.5, esforço médio, papel "Designer de visuais". Dono do portal; decide o tema, a forma,
  a técnica e se precisa de ajuda: subagentes no terminal dele ou um ajudante no canvas, que ele pede ao maestro.
- **Prumo**: Codex GPT-6.1 Sol, esforço médio, papel "Revisor do portal". Obrigatório. Revisa o tema, a arquitetura,
  o código e a página renderizada, conversando direto com o Designer. No fim, ajuda o maestro a conferir o portal.
- **Troca do Designer (Gustavo, 2026-10-14):** quando o Designer atual (Opus 5.5) entregar a proposta aprovada
  (`proposta.md` nesta pasta), o Designer passa a ser **Claude Fable 5.1 com esforço alto**, que constrói a partir
  desse arquivo. O teto de contexto dele sobe para **50%**; acima disso, `/clear` com o estado em arquivo.
- **Maestro**: só passa o pedido e os fatos do projeto e responde às dúvidas. Chama o Gustavo apenas para decisão
  crítica. O Gustavo opina no resultado final.

## O que o portal precisa ser

1. **Entender o projeto:**
   - o destino;
   - para onde está indo;
   - onde está agora;
   - o que está decidido, aberto e no radar.
2. **Ver os designs e por que existem:** cada visual com o propósito, o ticket e a decisão a que serviu, e quando foi
   feito. Os visuais de hoje:
   - `.scratch/context-hub/system-design.html`, que **mora dentro do portal**;
   - `mapeamento.html`;
   - os `prototipos/*.html`;
   - `laco/painel/*.html`.
3. **Gerenciar sem DevOps:**
   - ver os tickets e o estado deles;
   - responder rodadas;
   - aprovar ou recusar;
   - comentar;
   - personalizar uma proposta do maestro (por exemplo, uma estratégia de roteamento) e devolver a versão alterada.
4. **Volta direta ao maestro:** o que o Gustavo responder no portal chega ao maestro sem ele repetir no chat. Isso
   substitui a nota "Rodada atual".
5. **Reaproveitável:** a ideia é ter esse portal em todo workspace de desenvolvimento. O núcleo deve ser genérico,
   com o conteúdo do projeto separado, para um dia virar peça do acervo do maestro.

## Restrições que já valem neste projeto

- **File-first:** a verdade continua nos arquivos do repositório.
  - O portal lê o mapa (`.scratch/context-hub/map.md`), os tickets (`.scratch/context-hub/issues/*.md`, com
    `Status:`, `Type:` e `Blocked by:`), a estratégia (`estrategia-pos-pesquisa.md`) e o glossário.
  - Uma resposta dada no portal é gravada em arquivo, num lugar e formato que o maestro lê. O maestro absorve a
    resposta no ticket dono, como faz hoje com a nota.
  - Nada depende de serviço externo, nuvem ou conta.
- **Roda local no Windows 11, sem Docker**, aberto num navegador comum. Python 3 e Node estão instalados.
  - Um servidor local pequeno é aceitável.
  - Se servir arquivos, deve escutar só em `127.0.0.1`.
- **Sem códigos internos soltos:** nada de R88, T1 ou Q7 sem dizer em palavras o que são.
- **O que o Gustavo já disse sobre visuais** (memória do maestro):
  - Elogiou o "mapa de metrô" (diagrama no centro, chips, perguntas no fim) e o painel "maré" (metáfora única,
    números grandes, quase nenhum texto).
  - Recusou a página "laudo" (muita informação, fonte de que não gostou, texto demais) e uma v2 que "só mudou a
    estilização".
  - "Simplificar não é cortar info, é comunicar a mesma coisa porém de uma melhor forma": o detalhe vai para camadas
    (expandir, passar o mouse, link).
  - "Reinventar" é mudar a forma, não o acabamento.
  - Ele quer ser surpreendido.
- **Diferença deste pedido:** o portal não é uma página de ler de cima para baixo. É um sistema que se navega e se
  usa, e a regra "sem cliques obrigatórios" das peças visuais não vale aqui.

## Perguntas abertas que o time resolve sozinho

- O tema e a metáfora.
- A arquitetura: página estática com um servidor que lê e grava arquivos, ou outra.
- O formato dos arquivos de rodada e de resposta, combinado com o maestro, porque o maestro escreve as rodadas e lê
  as respostas.
- Como o maestro fica sabendo de uma resposta nova. Hoje o Gustavo avisa "respondi" no chat. Se o portal puder avisar
  o maestro sozinho, melhor, mas isso pede verificação: o maestro está no Maestri e recebe mensagens por
  `maestri ask "Claude Code"`.

## Retorno do Gustavo sobre os marcos 1 a 6 (2026-10-14)

> ja aviso que não gostei da tipografia, pois não ta legível, as letras estão muito finas e não dá pra ler a maioria
> dos textos, não ta aquela fonte gostosa de ler. E também Quero um design "aconchegante", mais "vivo" e mais
> "interativo".

## Aval do Gustavo sobre a amostra v2 "Mesa de mapas" (2026-10-14, tarde)

> a tela agora está com o design bom, aconchegante e gostoso de ler, acertou em cheio. Porém a trilha com esses
> triangulos soltos sem sentido nenhum não me agradou. Reinvente a maneira de apresentar essa trilha, pode
> simplificar e usar mais espaço da tela.

- **Aprovado:** clima, paleta, tipografia e leitura da tela.
- **Recusado:** a "trilha até o cume" (triângulos soltos com setas tracejadas). Reinventar a **forma** de mostrar o
  caminho até o objetivo, não restilizar; pode simplificar e ocupar mais espaço da tela.
- **Designer:** passa de Claude Fable 5.1 para **Claude Opus 5.5, esforço alto** (pedido do Gustavo no mesmo recado).

## Aval do Gustavo sobre a amostra v3 "O caminho até o destino" (2026-10-14, ~16h)

> pode aplicar nas cinco telas

Aprovada a amostra v3 (`v2/amostra-inicio.html`, parecer do Prumo em `revisao-amostra-v3.md`). Ajuste pedido pelo
maestro junto: a dica do passar o mouse não pode cobrir o cartão vizinho.

## Esclarecimento do Gustavo sobre o aviso ao maestro (2026-10-14, ~17h15)

> não po, você e o designer acharam que minha alteração lá tem que chegar aqui no seu chat de alguma forma, mas claro
> que não. É só você colocar um vigia pra ficar aguardando minha alteração lá e esse vigia te acordar.... Não tem pq o
> portal te mandar mensagem aqui no chat. Da forma que falei seria só você ler algum arquivo local. Mas vi que já tão
> conseguindo fazer funcionar então vou deixar, mas me entenderam errado

- **O que ele queria desde o pedido:** um vigia do lado do maestro observando a caixa local e acordando o maestro, que
  então lê o arquivo. O portal não manda nada ao chat. Isso é o canal B (`aviso.py --vigiar` na ferramenta Monitor).
- **O que foi feito:** o canal A, em que o portal manda um `maestri ask` ao maestro.
- **Decisão dele:** deixa o canal A, que já está funcionando.

## Pedido do Gustavo: página de loops em voo (2026-10-14, ~20h30)

Abaixo de "Decisões" no menu lateral, uma página nova:

> uma página que mostra quaisquer loop engineering em voo, seja de pesquisas, seja de suite de testes. peça isso ao
> designer, ela gera uma proposta de como ficaria (uma carta nova) e eu aprovo a ideia ou peço alteração. Ele deve
> propor até qual será o conteúdo dessa nova página e quais funcionalidades podem existir lá. Uma ideia era que
> quando eu pedisse loop engineering pro maestro, o maestro criasse algo lá e eu pudesse "editar" como se fosse n8n.
> Claro que ali seria só uma representação do que está rolando por trás e não necessariamente tudo ali daquela
> página deve estar conectado ao loop rodando em si. Parte disso já vimos funcionar com a pesquisa ampla rodando e
> a cada onda a página atualizando. É parte aquilo, mas o que estou pedindo é deveras diferente ok. Nada de sair
> criando tudo, primeiro a carta-proposta

- Primeiro só a **carta-proposta**: conteúdo, funcionalidades e forma. Nada se constrói antes do aval.
- Exemplos reais para a carta: o laço da pesquisa ampla (`laco/`, painel "maré") e o laço da pesquisa de embeddings
  (`laco-embeddings/`, ticket 54), que vai rodar.
