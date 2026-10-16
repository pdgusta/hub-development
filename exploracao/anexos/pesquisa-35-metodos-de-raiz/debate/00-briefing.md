# Debate: métodos conhecidos contra os nove tipos de raiz do context hub

Ticket: `.scratch/context-hub/issues/35-metodos-de-organizar-a-raiz.md`, insumo de
`.scratch/context-hub/issues/12-arquitetura-de-pastas-e-frontmatter.md`.

## O que está em jogo

O Gustavo está desenhando o **context hub**: a casa única do contexto dele e dos agentes (Claude Code,
Codex, Copilot), nas duas máquinas dele. A verdade mora num banco (CouchDB com o plugin LiveSync), e
ele vê e edita o hub como arquivos `.md` no Obsidian (a "vista Markdown"). Agentes buscam e gravam
por um MCP e também podem editar o disco. Vocabulário: `GLOSSARY.md` na raiz do repositório.

A pergunta da vez é **o primeiro nível de pastas (a raiz) do hub**. Antes de escolher, o Gustavo
levantou com o Claude nove tipos candidatos de raiz, tirados do uso real dele, e gostou deles. Agora
quer saber o que os métodos conhecidos dizem sobre esses tipos.

### Os nove tipos candidatos

Um tipo só merece pasta na raiz se o que mora nele **se comporta de um jeito próprio**: se tem dado
de cliente, se termina, quem mais lê e o que acontece quando envelhece.

| Tipo | Exemplos reais | Dado de cliente | Termina? | Quem mais lê | Quando envelhece |
|---|---|---|---|---|---|
| 1. Clientes | VOEGOL, TRF3, ELEMENTIS, SBF, Riachuelo, AVIANCA | sim | sim | ele e os agentes do caso | arquivo |
| 2. Operações contínuas | SOC STRATA (casos, relatório recorrente), SOPs de incidente | sim | não | agentes da rotina | compactar |
| 3. Produtos e frentes próprias | videos-transcriptor, freellmapi-mcp, soc-as-code, report-generator, esta frente | não | por versão | agentes no repositório (o código fica fora do hub) | arquivo |
| 4. Estudo e laboratório | certificações, treinamentos, spikes, testes de modelo | não | sim | ele | promover ou arquivar |
| 5. Conhecimento de referência | armis-docs, armis-brand, playbooks de remediação | às vezes | não | a busca, todos | revisar |
| 6. Oficina dos agentes | contrato global, skills, papéis e equipes do Maestri, perfil de máquina | não | não | os harnesses, por caminho fixo | versionar |
| 7. Entrada | captura rápida, esvaziada pelo checkpoint | às vezes | em dias | o checkpoint | esvaziar |
| 8. Arquivo | o que terminou | às vezes | já terminou | quase ninguém | fica |
| 9. Pessoal? | a confirmar com o Gustavo | — | — | — | — |

### Restrições já decididas (não reabra)

- **Lições do vault** (o sistema anterior dele, que falhou): cada informação tem um lugar só; nada de
  cadeia de índices mantida à mão como porta de entrada (a porta é a camada de busca); todo arquivo
  tem destino quando envelhece (compactar ou arquivar); isolamento por domínio e iniciativa, com
  promoção explícita para compartilhar; frontmatter só com o que a busca ou o contrato usam; textos
  curtos. O vault cortava a raiz por tipo de documento (`charter`, `core`, `decisions`, `knowledge`,
  `initiatives`, `operations`, `skills`, `templates`), e uma iniciativa ficava espalhada.
- **Nota de retomada**: cada trabalho tem uma nota curta num lugar fixo, que a pasta onde a sessão
  abre deixa achar sem busca.
- **Pasta não replicada**: parte do hub pode ficar numa máquina só (dado de cliente). O mecanismo
  ainda está aberto; a raiz deve facilitar declarar isso.
- **Skills e contrato** precisam de caminho fixo, que os harnesses carregam sozinhos.
- O código dos produtos fica nos repositórios deles, fora do hub.

## Insumo

Quinze JSON em `exploracao/anexos/pesquisa-35-metodos-de-raiz/`, um por método, extraídos de fonte
primária com citação literal. Campo `nao_verificado` = a fonte não disse. Use **só** estes JSON, o
`GLOSSARY.md` e este briefing. Nada de web. Toda afirmação sobre um método cita o arquivo JSON (ex.:
`01-para.json`). O que não estiver nos JSON é "não verificado" e não vale como argumento.

## Formato

Cinco rodadas no máximo. Em cada rodada, cada debatedor grava **um** arquivo
`debate/rN-<Nome>.md` (N = número da rodada), com no máximo 600 palavras, e lê os arquivos da
rodada anterior dos outros dois antes de escrever. Responda aos outros pelo nome, concorde, discorde
e mude de posição quando for convencido. Nunca edite o arquivo de outro debatedor.

- Rodada 1: sua leitura dos métodos pela sua lente, e o que ela diz sobre cada um dos nove tipos.
- Rodadas 2 a 4: discussão. Aponte onde os outros erraram, o que falta e o que se resolve.
- Rodada 5 (ou a última): posição final. Para cada um dos nove tipos: manter, juntar com outro,
  separar ou cortar, com o método que sustenta; e o que ficou em desacordo.

Se os três já concordarem em tudo antes da quinta, digam "convergimos" no fim do arquivo.
