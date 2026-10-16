# Brief: o painel da construção do context hub

Do maestro, 2026-10-15 ~20h50. Pedido do Gustavo, verbatim: "já vai despachando os designers [...] pra ir construindo
o painel de construção do context-hub. Já os mande criar o painel de forma que esteja preparado para a execução toda e
como ainda não sabem o desenho proposto, diga para eles montarem a carcaça agora já. Com a proposta do laço aprovada eles
só alteram. A ideia é a execução rodar independente do painel e o painel servir só para eu VER a execução rolando."

## O que vai ser executado (para o painel saber o que mostrar)

O ticket 16 ("Passagem para a construção") vira a construção do hub. O desenho do laço ainda vai ser aprovado pelo
Gustavo; o que já se sabe, pelo pedido dele:

- Primeiro a **spec** (`/to-spec`), depois os **tickets de construção** (`/to-tickets`), fatias verticais, o menos
  horizontais possível, cada um com dono de um papel, `Blocked by` entre eles; depois a **execução**
  (`/implement-spec`).
- **10 agentes Opus 5.5 com esforço alto**, mais **2 revisores "Prumo" (Claude Opus 5.5 alto)**, em paralelo, com **separação de papéis** (construtor, revisor, testador,
  integrador... o desenho final dirá); **cada um pode abrir até 10 subagentes**; tarefa MUITO complexa ganha um agente
  **Fable 5.1 médio** só para ela.
- **Sem limite de tokens, com limite de 1 hora** (provavelmente por ticket ou por tentativa; o desenho dirá).
- **Todos conversam entre si e com o maestro** (por `maestri ask`).
- Haverá tickets que esperam o Gustavo (o segundo par, o notebook, aval) e tickets bloqueados.

## O que o painel é

- **Só leitura e só para ver.** Nenhum botão manda nada para a execução. A execução roda sem o painel; se o painel cair,
  nada para. O painel nunca escreve na pasta da execução.
- **Ao vivo:** atualiza sozinho (sondagem de arquivo, alguns segundos) e mostra a hora do último sinal de cada agente,
  com "sem sinal há N min" quando parar de chegar.
- O que o Gustavo precisa ver de bater o olho: quantos agentes trabalham agora e em quê; o fluxo dos tickets (a fazer,
  em curso, em revisão, em teste, feito, bloqueado, esperando o Gustavo); o relógio de 1 hora de cada um; os subagentes
  de cada agente (até 10) e o Fable quando aparecer; as conversas entre agentes (quem falou com quem, sobre o quê); o
  que travou ou falhou; o andamento geral (tickets feitos / total, desde quando roda).
- Diagrama no centro (o Gustavo elogiou o mapa de metrô e a maré; recusou laudo denso). Pouco texto. Detalhe ao clicar.

## A carcaça, agora

Montem já a estrutura completa, com o que der para fixar sem o desenho: as regiões da tela, o leitor do estado, a
atualização ao vivo, o "sem sinal", e uma **fixture que simula uma execução inteira** (10 agentes, papéis, ~25
tickets com bloqueios, subagentes subindo e descendo, um Fable, conversas, um ticket estourando a 1 hora, um esperando o
Gustavo, uma falha). Quando o desenho do laço for aprovado, o maestro manda as diferenças, e vocês só alteram.

**O contrato de dados é o coração**: a execução escreve, o painel lê. Proposta de partida (o Tech lead fecha):

- Pasta da execução: `.scratch/construcao-do-hub/execucao/` (a execução cria; o painel só lê).
- `execucao/laco.json`: a descrição do laço (papéis, agentes, limites, fases), escrita pelo maestro.
- `execucao/tickets/`: os tickets de construção (Markdown com `Status:` e `Blocked by:`, como em `docs/agents/`).
- `execucao/eventos/<agente>.jsonl`: um arquivo por agente, só acrescentado, um evento por linha (pegou ticket, abriu
  subagente, fechou subagente, mandou mensagem, recebeu mensagem, rodou teste, commit, passou a 1 hora, chamou o Fable,
  devolveu, falhou). **Um arquivo por agente** para dez processos não disputarem o mesmo arquivo. Os eventos devem
  poder ser gravados por hook (mecânico), não pela boa vontade do agente: desenhem o formato pensando nisso.
- `execucao/agentes/<agente>.json`: o estado atual de cada agente, sobrescrito (opcional, se o Tech lead achar que o
  painel não deve reconstruir tudo dos eventos).

## Papéis

- **Tech lead:** fecha o contrato de dados (`painel/contrato.md`, com um exemplo de cada arquivo), a arquitetura do
  painel e onde ele roda. Confira com o recruta **Portal** se o painel vira uma página do portal
  (`http://127.0.0.1:8770/`, que já tem a página "Laços", contrato em `portal/lacos-brief.md` e `portal/proposta.md`)
  ou um servidor próprio; preferência do maestro: o que deixar o Gustavo abrir pelo portal sem acoplar a execução.
- **UI engineer:** constrói a tela e o leitor, sobre a fixture.
- **UX revisor:** confere se dá para entender a execução de bater o olho (Gustavo é a pessoa que olha), e o detalhe ao
  clicar.
- **QA tester:** gera a fixture "ao vivo" (um script que vai acrescentando eventos com o tempo) e testa o painel com
  ela: atualização, "sem sinal", 10 agentes × 10 subagentes, 1280 px e 320 px.

Conversem entre vocês por `maestri ask`. O Tech lead coordena a equipe.

## Regras

- Código e arquivos em `.scratch/construcao-do-hub/painel/`; fixture em `painel/fixture/`. Fora disso, só o que o
  Portal combinar com vocês na pasta dele.
- Capturas e testes de navegador com o Edge sem cabeça: perfil próprio (`--user-data-dir` único); mate só os `msedge`
  desse perfil, nunca `taskkill` por nome.
- Nada de dado de cliente nem dado pessoal na fixture: iniciativas pelo nome, agentes por papel.
- Sem tocar em `~/.claude`, `~/.codex`, `~/.copilot`.
- Ao terminar a carcaça: `maestri ask "Claude Code" "carcaça do painel pronta: <caminho> — <como abrir>"`.
