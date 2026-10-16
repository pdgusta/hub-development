# Métodos conhecidos de organizar a raiz

Type: research
Status: resolved

## Question

Como métodos conhecidos de organizar notas, arquivos e memória de agentes cortam o primeiro nível
(PARA, Johnny.Decimal, LYT/ACE, Zettelkasten, GTD, Diátaxis, o vault do Steph Ango, FHS, XDG, Cline
Memory Bank, Basic Memory, memory tool do Claude, Letta, evergreen notes, diretório `.claude`), e o
que isso diz sobre os nove tipos de raiz da rodada 2 de "Arquitetura de pastas e frontmatter do hub"?
Pedido do Gustavo em 2026-10-10 (resposta à R14).

## Comments

- 2026-10-10: método pedido pelo Gustavo. 15 subagentes Haiku 5.5, um por método, com URL fixa e
  esquema fixo (sem decidir o que buscar), cada um grava um JSON em
  `exploracao/anexos/pesquisa-35-metodos-de-raiz/`. Depois, 3 agentes Sonnet 5.5 no Maestri, sem
  subagentes, conversam por até 5 rodadas lendo os JSON e as falas uns dos outros
  (`exploracao/anexos/pesquisa-35-metodos-de-raiz/debate/`). A comparação final de Claude sai só
  dessas rodadas.
- 2026-10-10: 15 JSON gravados (LYT/ACE sem descrição do ACE na fonte; Evergreen, GTD, Letta e
  LYT sem raiz definida). Debate de 5 rodadas com Astrolabio, Cinzel e Junco (Sonnet 5.5, sem a
  ferramenta de subagentes, via `--disallowedTools`), convergência na r5.

## Answer

Comparação final, feita só a partir das 5 rodadas:
[`comparacao-final.md`](../../../exploracao/anexos/pesquisa-35-metodos-de-raiz/comparacao-final.md).

- **Só três métodos dizem algo útil sobre a raiz:** o PARA (separa o que termina do que não termina:
  projeto × área), o FHS (o que não é compartilhável não divide diretório com o que é, e daí sai o
  critério da pasta não replicada) e o `.claude`/XDG (caminho fixo e escopo, config × dados). Os
  outros repetem o vault (Johnny.Decimal com índice, Diátaxis por forma de documento), cortam por
  conceito (Zettelkasten, Evergreen) ou não definem raiz.
- **Posição dos três sobre os nove tipos:** manter 1 (clientes), 2 (operações contínuas), 5
  (referência, sem dado de cliente), 6 (oficina, com o perfil de máquina não replicado) e 7 (entrada,
  local e com limite de idade); juntar 3 e 4 em "iniciativas sem cliente"; o arquivo deixa de ser raiz
  e vira `_arquivo/` dentro de cada uma; o pessoal (9) só é raiz se não replicar.
- **Para testar no ticket 12:** arquivar por pasta ou por propriedade (depende de mover pasta não
  colidir e de a busca filtrar por caminho); captura de cliente na máquina errada.
- **Nenhum método respondeu:** replicação com duas cópias editáveis, destino do que envelhece,
  organização para agentes, ponte da pasta ao harness, controle de leitura por agente, edição
  concorrente.
- **Perguntas ao Gustavo:** SOC STRATA é cliente ou operação; em qual máquina mora cada cliente; o
  pessoal replica; spike vira produto.
