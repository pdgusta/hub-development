# Relatório do ticket 06: gerador de exclusões (Vela)

Ramo `ticket-06` (worktree `C:\context-hub-wt\ticket-06`), da ponta de `integracao` c8d2267, com `integracao` 0d04985
(ticket 05) juntada. Commits até b7cd714.

## O que foi construído

`agents/code/bin/gerar-exclusoes.mjs [<hub>]` (Node ≥ 22, sem pacote de fora). Hub padrão: `HUB_ROOT`, senão a pasta
atual.

**O que ele faz:**
- Percorre o hub sem descer em pasta com ponto e acha cada pasta cujo `index.md` diz `local: true` no frontmatter.
- Escreve no próprio hub duas listas do que fica numa máquina só. Os dois arquivos têm ponto no caminho, então não
  replicam: cada máquina gera os seus.

| Arquivo | Para quem | Conteúdo |
|---|---|---|
| `.livesync/ignore` | o sincronizador (CLI do LiveSync), lido na partida | `.*` e `.*/` (a forma da prova 02) e `<pasta local>/**` |
| `.local/exclusoes/busca.env` | quem sobe a busca (ticket 12) | `OBSIDIAN_IGNORE_PATTERNS=**/.*,**/.*/**,<pasta local>/**` |

**Saída e proteções:**
- Imprime uma linha JSON `{ hub, locais, mudou }`.
- Só regrava o arquivo que mudou. `mudou: true` avisa quem chama que o CLI precisa ser religado, porque ele só relê a
  lista na partida.
- **Recusa (código 2, nada gravado):** pasta local com vírgula, espaço nas pontas ou caractere de padrão
  (`* ? [ ] { } ( ) ! # \`) no nome. A vírgula partiria a lista da busca, e os outros caracteres virariam outra regra,
  sem aviso, nos dois leitores.

## Critérios do ticket

| Critério | Resultado | Evidência |
|---|---|---|
| Uma pasta com `index.md` `local: true` e qualquer caminho com ponto saem na lista gerada | **Passou** | `gerador.test.mjs`, testes 1, 2 e 5 |
| A lista funciona no sincronizador, na forma provada pelo ticket 02 | **Passou** | `sincronizador.ps1`: 14/14 (`evidencia/gerado.log`) |
| A lista funciona na exclusão da busca | **Passou** | `gerador.test.mjs`, teste 3 |

Testes em `agents/code/test/gerar-exclusoes/`, todos sobre o hub de ensaio montado numa pasta vazia pelo `montar.mjs`
da ponta. O hub de ensaio já traz a pasta local `initiatives/context-hub/labs/` e o `.secrets/` aninhado da Aurora.

**`node --test agents/code/test/gerar-exclusoes/gerador.test.mjs` → 7/7:**
- as duas listas, com o conteúdo esperado;
- a busca: a política de exclusão do próprio obsidian-hybrid-search 0.16.2 (`createIgnorePolicy`), com a lista gerada e
  sem o `.gitignore`, aplicada a todos os arquivos do hub de ensaio. Ignora tudo que tem ponto e tudo de `labs/`, e não
  ignora nenhuma nota `.md` que replica. Conferi que o teste distingue: sem a linha da pasta local, `labs/` seria lido;
- rodar de novo sem mudança: não regrava e devolve `mudou: false`;
- `local: True`, `local: TRUE` e fechamento `--- ` contam como pasta local; `local: false` e `local: "true"` não;
- `index.md` com YAML ilegível: recusa (código 2), sem gravar;
- recusa de `a, b`, `rascunho [velho]` e `tudo{x}`, sem gravar.

**`pwsh agents/code/test/gerar-exclusoes/sincronizador.ps1` → 14/14** (`evidencia/gerado.log`).
- Montagem: dois pares de ensaio com E2EE e caminho ofuscado (`hub-ensaio-06-a/b`, `127.0.0.1:5998/5999`), replicação
  de envio em cada um e o CLI em `daemon`. O módulo é o da prova 02 (`banco.psm1`), e o gerador roda em cada par antes
  da partida.
- **CLI rodando:** o hub de ensaio inteiro sobe na primeira partida, e uma nota nova nasce em `labs/`. Nada de `labs/`
  nem com ponto chega ao banco dos dois pares nem ao disco do B; a nota de controle chega.
- **Varredura de partida:** com o CLI do A parado, nascem uma pasta local nova (`rascunho-local/`, com `index.md`
  `local: true`) e um `.cache/` aninhado. O gerador roda de novo e acha a pasta nova; o CLI é religado. Nada vaza.
- **Vermelho (`-SoPonto`, `evidencia/so-ponto.log`):** com a lista da prova 02 (só ponto), os arquivos de `labs/` e de
  `rascunho-local/` vão ao banco dos dois pares e ao disco do B, e o que tem ponto não.
- Contêineres, volumes e pastas `hub-ensaio-06*` apagados ao fim de cada rodada (conferido).

**Costura da busca:** usei a política do próprio pacote, sem subir o servidor nem baixar o modelo. O servidor com
índice de verdade é o aceite do ticket 12, que já prevê "nada com ponto nem de pasta `local: true` aparece".

## O que vai doer ao ligar

1. **Pasta local nova com o CLI rodando vaza.** O observador manda o arquivo na hora, inclusive o próprio `index.md`
   com `local: true`, antes de qualquer gerador rodar. A prova só passou porque a pasta nova nasceu com o CLI parado.
   Quem cria pasta local (skill ou contrato) precisa:
   - parar o sincronizador;
   - criar a pasta;
   - rodar o gerador;
   - religar o sincronizador.
   Alternativa: a pasta nasce com ponto e só perde o ponto depois. Decisão do Gustavo; não inventei.
2. **Quem roda o gerador e religa o CLI:** o kit, na instalação, antes da primeira partida (lição do ticket 02). Depois
   disso, quem? A vigia (ticket 16) ou a tarefa agendada são candidatas: rodar o gerador e, com `mudou`, religar. Não
   está decidido.
3. **Tirar o `local: true`** faz a pasta replicar: o gerador tira a linha, e a varredura de partida manda os arquivos.
   O sentido contrário (pôr `local: true` numa pasta que já replicou) não apaga o que já está no banco e na outra
   máquina. Precisa de limpeza (`rm` do CLI); não está no gerador.
4. **A busca guarda a lista no próprio banco** e a restaura se a variável faltar (README 0.16.2). Então:
   - quem sobe a busca precisa sempre passar o `busca.env`;
   - não foi verificado o que a busca faz com notas já indexadas que passam a ser excluídas (o pacote fala em
     "assinatura" e em varrer as recém-ignoradas).
5. **`local` é lido como o verificador lê** (`separar` de `lib/frontmatter.mjs`, js-yaml; conserto 1 do Fiel,
   rodada 1). O que conta é o booleano verdadeiro: `local: true`, `True` e `TRUE` contam, mesmo com o fechamento `--- `
   com espaço; `local: "true"` (texto) não conta. Um `index.md` com YAML ilegível faz o gerador recusar tudo (código 2),
   porque não dá para saber se a pasta é local. Assim, um frontmatter quebrado trava a geração, que é o mais seguro, mas
   precisa ser consertado antes de o kit seguir.
6. **O git:** o glossário põe a pasta local fora do GitHub, mas o ticket 06 só pede sync e busca, e o spec deixa aberto
   "se o mesmo script gera a exclusão do git". Não gerei. Caminhos possíveis, em aberto:
   - `.git/info/exclude`, que é local e não versionado;
   - o `.gitignore`, que a busca também lê.
7. **O `.livesync/ignore` antigo é trocado inteiro.** Se alguém editar à mão, o gerador desfaz na próxima rodada (o
   cabeçalho do arquivo avisa).

## Estado

- 2026-10-16 ~23h20: ticket pego.
- 2026-10-16 ~23h50: 5/5 e 14/14 verdes depois de juntar `integracao` 0d04985. Pedida a revisão do Fiel e do Fielzinho.
- 2026-10-17 ~0h: rodada 1 = volta (o gerador lia `local` com regex própria). Consertado com o leitor do verificador e testes (`True`, `TRUE`, `--- `, texto, YAML ilegível). 7/7 e 14/14 em b7cd714. Pedida a rodada 2.
- 2026-10-17: integracao andou para 45ec3b0 (ticket 01). Junto depois do parecer da rodada 2, para não mexer na worktree durante a revisão; depois rodo 7 + 14 de novo.
