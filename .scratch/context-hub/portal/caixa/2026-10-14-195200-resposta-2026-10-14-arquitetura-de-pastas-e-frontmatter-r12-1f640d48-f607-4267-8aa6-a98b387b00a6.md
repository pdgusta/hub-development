---
tipo: resposta
rodada: 2026-10-14-arquitetura-de-pastas-e-frontmatter-r12
ticket: 12
enviada: 2026-10-14T19:52:00-03:00
envio: 1f640d48-f607-4267-8aa6-a98b387b00a6
estado: lida
substitui:
---

# Resposta: Como o agente acha tudo, e nada fica órfão

## O catálogo de blocos
escolha: A, Um arquivo `agents/blocks.md`, citado pelo `AGENTS.md` da raiz: cada bloco com uma linha do que entra, o que não entra e um exemplo, mais a pilha sugerida por tipo; uma skill "nova iniciativa" o usa para criar a pasta, o núcleo e os índices (a recomendada)
comentário:
> e essa skill pode já conter scripts para criar os tipos mecanicamente e os agentes não gastariam tokens. É crucial também ser uma skill que não pode ficar sofrendo alteração por qualquer agente. Só alteraçao sob supervisão e aprovação. Já sofri isso em skills de workspace e agentes no copilot vs code a editando a cada utilização (a skill do ai-soc-report)

## O bloco genérico
escolha: B, `other/`, com a mesma regra (a recomendada era A)

## Como nenhum arquivo fica sem referência
escolha: A, Toda pasta tem um `index.md`, e um verificador sem IA roda no hook do fim de cada resposta: ele acha o arquivo que nenhum índice cita, já o inscreve no `index.md` da pasta como "sem descrição" e avisa o agente para descrevê-lo (a recomendada)
comentário:
> só uma correção: nem toda pasta. Deve ser em toda pasta que sabemos que vai crescer o número de arquivos e não de subpastas de diferentes tipos. 
>
> Exemplo: uma pasta de 'runs/' com várias subpastas 'run-01/' e 'run-02/', etc. Pode ter um 'index.md'. 
>
> Mas uma pasta que contenha sei lá, 3 subpastas, e dentre as subpastas apenas 1 cresce em arquivos, o 'index.md' fica na subpasta.
>
> Não sei se deu pra entender mas é isso

## Algo mais?
> Essa rodada de perguntas não necessariamente precisava de uma nova carta, mas essa que criaram está boa também. Vão ter casos de rodadas de perguntas realmente simples que reconheço que não preciso de uma 'visualização' e espero que tenha a mesma percepção daqui pra frente. Abri a carta.
>
> A carta só troca a ordem das perguntas, mas vi que a recomendação é a mesma. E na carta realmente deixa isso em aberto, essa verificação se o mecanismo de hook pro claude tem correlatos pros outros harnesses e modelos. Sei que no claude pode ser claude mod.
>
> Inclusive me surgiu uma dúvida agora com a carta, Ter esses index.md ao invés de usar o mecanismo de busca é ruim? Sei que ter os 2 é bom, mas em nenhum momento você citou o mecanismo de busca. Será que está fazendo todas essas sugestões apenas com seu conhecimento esquecendo de tudo que decidimos nos outros tickets, ou você já considerou tudo que decidimos do context-hub ? Inclusive considerou o que ainda não decidimos, mas a pesquisa ampla trouxe à luz como oportunidade futura?
