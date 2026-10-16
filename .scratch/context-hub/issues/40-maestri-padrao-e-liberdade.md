# Maestri: padrão e liberdade

Type: grilling
Status: resolved
Blocked by: 43, 44, 45

## Question

Até onde o uso do Maestri com o hub segue um padrão, e onde o Gustavo fica livre para abrir cada
workspace da forma que precisar? Cobre as variantes de uso (workspace na raiz do hub ou fora dele,
com papel ou sem, maestro e recrutas, partituras, trabalho que roda fora do hub), o que cada uma
exige do hub e da configuração de cada par, e onde mora a fonte de papéis e partituras.

## Comments

- 2026-10-12: aberto a pedido do Gustavo na resposta à R24 de "Portas de entrada do hub" ("no maestri
  acontecerão diversas variantes e eu quero entender bem até onde eu vou seguir um padrão e até onde
  eu vou ter liberdade para abrir da forma que precisar"). A recomendação da R24, ainda não aceita:
  ligar `claude-md-and-agents-md` em cada par pelo kit; workspace do hub abrindo na raiz; papéis em
  `agents/roles/<papel>/role.json` e partituras em `agents/` como fonte, importados à mão para a
  biblioteca do Maestri.
- Fatos de partida: `exploracao/anexos/pesquisa-37-portas/porta-3-4-maestri.md` (onde o papel abre,
  o que o Maestri grava, "Discover Roles", partituras em `~/.maestri/partituras/`) e o grupo A de
  "Testes das portas de entrada" (o papel real só recebe o `AGENTS.md` do hub com
  `claude-md-and-agents-md`; efeito colateral: em todo projeto com `CLAUDE.md` e `AGENTS.md`, os dois
  carregam).
- 2026-10-12, fatos levantados no disco antes da rodada 1 (só leitura, sem prompts copiados): 8
  workspaces; SOC, VOEGOL, SBF e TRF3 abrem na mesma pasta, `C:\Projetos\maestri` (com `.maestri/roles`
  de 28 papéis misturados e a memória automática do Claude compartilhada); "SOC Report Redesign" abre
  num worktree de código; videos-transcriptor e Context Hub em pastas próprias. Os 41 papéis da
  biblioteca são todos de um workspace só (nenhum global) e se repetem por cliente ("Redator",
  "Redator SBF", "Redator TRF3"; o mesmo com Escrivão, Revisor Cruzado, Gestor Git, Scripter). Há uma
  partitura, que guarda `sourceWorkingDirectory` e `sourceWorkspaceId`. Pastas com ponto (como
  `.maestri/`) não replicam pelo LiveSync ("Testes das portas de entrada"), então os arquivos de papel
  que o Maestri grava ficam em cada par. Fora do mapa continuam a migração dos workspaces existentes e
  a skill que aplica e audita o Maestri.
- 2026-10-12: rodada 1 aberta na nota "Rodada atual" (R34 o que é padrão e o que é livre; R35 onde
  cada tipo de workspace abre; R36 ligar `claude-md-and-agents-md` em cada par; R37 teste do Codex e do
  Copilot dentro da pasta de um papel). Recomendações: padrão só para o que leva o contrato ao agente e
  o que grava no hub, o resto livre; workspace de iniciativa abre na pasta da iniciativa, transversal
  na raiz, código no repositório; ligar pelo kit de par; testar antes de decidir.
- 2026-10-12, respostas da rodada 1:
  - **R34, recusada a recomendação (padrão mínimo):** "minha intenção com esse ticket não é definir
    tudo livre e que se dane a facilidade ao ter bons papéis de maestri que eu realmente já precisaria
    prontos para utilizar em outro workspace. Ou reutilizar todo um setup em um workspace novo, mas
    alterando uma coisa ou outra. Citei 2 exemplos, mas eu sei que podem existir 50 facilmente. [...]
    Eu quero construir todo um acervo de possibilidades de setup disponível pro maestro no maestri.
    Quero ter contratos (e quando eu digo contratos, não é regra, são só opções para eu não ter que
    ficar dizendo ou todo maestro ter que descobrir sozinho) de routing de modelos. E etc, etc, etc.
    Essa R34 é literalmente algo muito mais complexo do que você está propondo." O ticket passa a ser
    sobre o **acervo do maestro**: peças prontas e reutilizáveis (papéis, setups inteiros com variação,
    contratos-opção como o roteamento de modelos), não sobre o mínimo obrigatório.
  - **R35 e R36:** "minha resposta do r34 se aplica aqui"; ficam suspensas e voltam depois, já à luz
    do acervo.
  - **R37:** "podemos testar, após focarmos no problema que respondi na r34". Teste aprovado, para
    depois da forma do acervo.
- Nota de escopo: o "contrato de roteamento de tarefas pesadas e simples para modelos do FreeLLMAPI"
  entrou no mapa na rodada 2 do mapeamento (Q8) e nunca virou ticket; cabe aqui como um dos
  contratos-opção do acervo. A "skill de aplicar/auditar do Maestri" segue fora do mapa (Q2, Q8).
- Fatos da CLI (`maestri recruit --help`, `maestri role --help`): por recruta dá para escolher preset
  (Claude Code, Codex, Antigravity, OpenCode, Shell), papel, conta (Claude Code e Codex), pasta,
  floor e workspace; `role create --scope global` cria papel reutilizável em todo workspace. O Maestri
  não tem herança entre papéis nem entre partituras; a partitura embute cópias dos papéis.
- 2026-10-12: rodada 2 aberta na nota "Rodada atual" (R38 o que entra no acervo; R39 até onde vai
  este ticket; R40 como o maestro chega ao acervo e usa; R41 como uma variante reaproveita um setup).
- 2026-10-12, respostas da rodada 2:
  - **R38, os três tipos (papéis, setups, contratos-opção) e mais:** "sugestões suas do que pode entrar
    como peça"; cada peça "não seja algo fixo, mas sim aberta a personalização", para os maestros terem
    "inteligência necessária para me atender caso a caso (workspace aprendendo com workspace e novos
    workspaces nascendo com menos dificuldade no first-setup)". A lista aberta é "oportunidade de
    leitura de documentação e sugestões suas (ou de subagentes)". Nem todo maestro nasce no hub, "mas
    todos os workspaces vão receber a primeira instrução, os roteando ao hub para 'aprenderem a serem
    maestros'". Quer o acervo como "skills ou acervos de skills, assim como o '/maestri list' é" (a
    família de skills oficiais `maestri-*`). Virou "Acervo do maestro: pesquisa de peças", que agora
    bloqueia este ticket.
  - **R39, B:** a forma do acervo e um primeiro lote (escrito na construção), "mas a 'forma' precisa
    ser enriquecida de acordo com o que respondi no R38".
  - **R40, A:** skill global do acervo, ligada por junction, montando sob demanda pela CLI; a busca do
    hub de reserva. A skill que aplica e audita o Maestri "pode ser trazida de volta à vida
    posteriormente, não agora" (segue fora do mapa).
  - **R41, ok:** setups citam papéis e contratos-opção pelo nome, sem copiar prompt; a variante declara
    a base e só o que muda; quem resolve a variante é o maestro, pela skill do acervo.
- 2026-10-12: "Acervo do maestro: pesquisa de peças" disparada em subagente. Rodada 3 aberta na nota
  "Rodada atual" só com o que não espera a pesquisa (R42: como um workspace devolve ao acervo o que
  aprendeu). Recomendação: o maestro acrescenta peças e variantes sozinho; mudar uma peça-base que
  outras citam pede o seu aval.
- 2026-10-12, resposta da rodada 3:
  - **R42, C com ressalva:** o maestro acrescenta sozinho e alterar ou apagar uma peça citada pede
    aval, "mas com o fato de que acrescentar tem possivelmente casos que quebrariam sim, portanto a
    noção de quando solicitar aval e o que apresentar na solicitação do aval, deve ser algo melhor
    definido". Quer explorar "Claude Mods" no acervo de skills, "tanto no ato de usar, quanto de
    alterar". Exemplo dele: um maestro em Opus percebe que pode alterar uma peça; um mod que age como
    middleware o força a disparar um subagente em Sonnet 5.5 que lista os workspaces que usam a peça,
    ou que detecta se a mudança já roda em algum workspace sem ter virado global. Perguntou se vale
    pesquisa ou ticket próprio. Recomendação dada: vale um ticket de pesquisa (o que um mod ou hook
    consegue interceptar e forçar, e o que existe equivalente no Codex e no Copilot), esperando o ok
    dele para disparar; a regra de quando pedir aval e o que mostrar volta à rodada depois das duas
    pesquisas.
- 2026-10-12: o Gustavo pediu o disparo; aberto "Guarda do acervo: mods e hooks, pesquisa", que também bloqueia este ticket.
- 2026-10-12: "Acervo do maestro: pesquisa de peças" resolvida (Answer naquele ticket). Rodada 4 aberta
  na nota "Rodada atual" com o que não espera a pesquisa dos mods: R43 quais tipos de peça a forma
  admite; R44 como a família de skills se divide e onde as peças moram; R45 setup como receita de
  comandos ou partitura. Recomendações: todos os tipos achados entram como tipos admitidos; família
  `maestro-*` dividida por assunto, cada skill com catálogo curto e um arquivo por peça dentro da
  própria pasta em `agents/skills/`; setup é receita de comandos, partitura exportada é opcional.
- 2026-10-12, respostas da rodada 4:
  - **R43, A:** a forma admite todos os tipos de peça achados (papéis, setups, contratos-opção,
    preset, nota-modelo e fichário-modelo, rotina-modelo, receita de floor, workspace-modelo, receita
    de portal, ambiente, subagente, perfil de modelo, hook de início de sessão, skill de procedimento);
    o primeiro lote escolhe o que nasce preenchido. A conta é campo de setup e roteamento.
  - **R44, B:** família de skills por assunto com prefixo `maestro-` (por exemplo `maestro-acervo` como
    porta, `maestro-papeis`, `maestro-setups`, `maestro-roteamento`, `maestro-orquestracao`), cada uma
    com catálogo curto e um arquivo por peça na própria pasta, em `agents/skills/<skill>/` do hub.
  - **R45, A com ressalva:** setup é receita de comandos da CLI como fonte, mas "as vezes será mais
    conveniente eu selecionar tudo, criar uma partitura e dizer que aquilo quero no acervo de alguma
    forma. Do que eu perder mó tempo pedindo pro maestro salvar aquilo no acervo. Na prática é a opção A,
    mas as partituras não devem morrer". Então a partitura é também uma porta de entrada no acervo: o
    Gustavo cria uma partitura pela interface e pede para guardar; o maestro lê o arquivo dela (JSON em
    `~/.maestri/partituras/`), escreve a receita e guarda a partitura junto, para ele aplicar pela
    interface quando quiser. (A resposta chegou completa depois que a rodada 5 já tinha sido escrita; a
    gravação dele na nota apagou a rodada 5, que foi reescrita.)
- 2026-10-12: "Guarda do acervo: mods e hooks, pesquisa" resolvida (Answer naquele ticket). Rodada 5
  aberta na nota "Rodada atual": R46 que guarda em cada harness; R47 quando pedir aval; R48 o que o
  pedido de aval mostra; R49 como saber quem usa uma peça.
- 2026-10-12, respostas da rodada 5 (todas aceitas):
  - **R46, A:** guarda forte só no Claude Code (mod ou hook no escopo do usuário, com verificador em
    outro modelo obrigatório antes de alterar); no Codex e no Copilot, gravar nas pastas do acervo é
    recusado, e eles contribuem gravando uma proposta numa pasta de propostas, que um maestro Claude
    Code avalia.
  - **R47, ok:** pede aval alterar ou apagar peça citada ou usada; mexer no catálogo ou na descrição de
    uma skill; acrescentar peça com nome ou gatilho parecido com outra; acrescentar contrato-opção que
    se apresenta como padrão. Livre: variante nova, peça nova sem sobreposição, nota de "o que
    funcionou".
  - **R48, ok:** o pedido de aval mostra, numa tela, o que muda (antes e depois), quem é afetado, se a
    mudança já roda como personalização em algum workspace, a alternativa de virar variante e a
    recomendação do verificador.
  - **R49, A com B:** registro de uso leve no hub (peça, workspace, máquina, data), um arquivo por
    máquina, gravado por hook (garantido no Claude Code; Codex e Copilot dependem de teste), mais os
    papéis atribuídos dos arquivos do Maestri e as citações entre peças.
- 2026-10-12: rodada 6 aberta na nota "Rodada atual", retomando as suspensas: R50 onde o workspace
  abre, agora como contrato-opção com um padrão; R51 a opção do Claude Code que lê `CLAUDE.md` e
  `AGENTS.md` juntos; R52 reforço da primeira instrução. O teste com Codex e Copilot dentro da pasta de
  um papel (aprovado na rodada 1) virou "Testes do papel do Maestri com Codex e Copilot".
- 2026-10-12, respostas da rodada 6 (todas "ok"):
  - **R50, A:** onde abrir é contrato-opção do acervo, com padrão por tipo: workspace de iniciativa na
    pasta dela (Copilot recrutado com a pasta de trabalho na raiz), workspace que cruza iniciativas na
    raiz, workspace de código no repositório. A personalização local de uma peça mora na pasta onde o
    workspace abre.
  - **R51, A:** `claude-md-and-agents-md` ligado em cada par pelo kit de par, que confere se continua
    ligado.
  - **R52, B:** primeira instrução = o contrato do hub ("no Maestri, como maestro, comece pela skill
    `maestro-acervo`") mais um hook de início de sessão que só age com `MAESTRI_TERMINAL_ID` e lembra o
    agente de que é maestro e de onde está o acervo (garantido no Claude Code; nos outros, depende de
    teste).
- 2026-10-12: rodada 7 aberta na nota "Rodada atual": R53 o primeiro lote; R54 onde moram a
  personalização local, as propostas e o registro de uso; R55 a cópia do papel na biblioteca do Maestri.
  Espera o teste do papel: se os papéis por cliente viram genéricos com a diferença no `AGENTS.md` da
  iniciativa.
- 2026-10-12: "Testes do papel do Maestri com Codex e Copilot" resolvido (Answer naquele ticket). Para
  a rodada seguinte: com papel, o Copilot recebe o `AGENTS.md` da iniciativa e não o da raiz, então
  "Copilot recrutado com a pasta na raiz" (R50) troca a iniciativa pela raiz; ajuste de papel só pelo
  prompt (editar o papel reescreve os arquivos e reinicia os terminais). Pendências do teste para o
  Gustavo: apagar `C:\teste45` (a trava do Claude Code barrou o subagente; apagada por ele em 2026-10-12) e decidir sobre as duas
  linhas `[projects.'c:\teste45\hub'] trust_level = "trusted"` que o Codex gravou no
  `~/.codex/config.toml`.
- 2026-10-12: a pedido do Gustavo, apagadas as duas linhas da pasta de teste no `~/.codex/config.toml`
  (backup conferido por diff; só elas saíram).
- 2026-10-12, respostas da rodada 7:
  - **R53, A:** primeiro lote = papéis de uso frequente sem nome de cliente (Receptor, Redator, Revisor
    Cruzado, Escrivão, Gestor Git, Scripter, Curador de Prints) e o Designer de visuais, os de nicho como
    estão; setups: a partitura de hoje como receita e o arranjo deste workspace; contratos-opção:
    roteamento de modelos (com o FreeLLMAPI para tarefas simples), orquestração, onde abrir; peças dos
    harnesses: o lembrete de início de sessão e a guarda. Os outros tipos nascem vazios.
  - **R54, ok:** personalização local em `maestro/` dentro da pasta onde o workspace abre; propostas em
    `agents/maestro/propostas/`; registro de uso em `agents/maestro/uso/<máquina>.md`.
  - **R55, A:** na hora de usar um papel, o maestro compara a cópia da biblioteca do Maestri com o
    acervo, cria o papel global se faltar e reescreve se estiver diferente.
- 2026-10-12: rodada 8 aberta na nota "Rodada atual": R56 papéis por cliente viram genéricos; R57 o
  Copilot deixa de abrir na raiz.
- 2026-10-12, respostas da rodada 8:
  - **R56, A com ressalva:** papéis genéricos no acervo, a parte do cliente no `AGENTS.md` da
    iniciativa; mas "nos workspaces, alguma personalização vai ser necessária 'localmente' até por troca
    de nome, ou diferentes complexidades ou quantidade de agentes no workspace. Então o ideal era ter um
    papel genérico pro maestro personalizar caso a caso opcionalmente". Fica: o maestro pode, quando
    quiser, criar a versão local de um papel genérico (nome, complexidade, divisão de trabalho) em
    `maestro/` da iniciativa, e é essa versão que vai para a biblioteca do Maestri daquele workspace.
  - **R57, ok com ressalva:** o Copilot abre na pasta da iniciativa como os outros (revê "Copilot só na
    raiz" das portas de entrada). Ressalva: "o 'copilot cli' utiliza a subscrição github enterprise que
    pode ou não ter uma funcionalidade nativa diferente da que você estava considerando. Por exemplo com
    o 'copilot-instructions' ou o 'github-instructions', nem lembro." Instruções no nível da organização
    ou da empresa no GitHub não foram pesquisadas; recomendação: pesquisa curta, ligada a "Acesso dos
    agentes: decisão", à espera do ok dele.
- 2026-10-12: rodada 9 aberta na nota "Rodada atual": R58 confirmação do resumo do acervo (fim da
  árvore deste ticket); R59 a pesquisa do Copilot com assinatura Enterprise.
- 2026-10-12, respostas da rodada 9:
  - **R58, "sim":** o resumo do acervo do maestro (texto da rodada 9, reproduzido no Answer quando o
    ticket fechar) confere; a árvore deste ticket fechou.
  - **R59, A:** pesquisa curta sobre o que a assinatura GitHub Enterprise pode impor ao Copilot. Virou
    "Copilot com assinatura Enterprise: pesquisa", que bloqueia "Acesso dos agentes: decisão" (não este
    ticket).
- Próximo passo ao retomar: registrar a resolução deste ticket (Answer com o resumo da R58, Status
  resolved, linha no mapa); ficou para a próxima sessão pela regra de um ticket por sessão ("Portas de
  entrada do hub" fechou nesta).

## Answer

Fechado em 2026-10-12 a pedido do Gustavo ("feche agora", exceção à regra de um ticket por sessão),
com as rodadas 1 a 9 (detalhe nos comentários). O ticket deixou de ser "o mínimo obrigatório" e virou
o **acervo do maestro**. Fatos: "Acervo do maestro: pesquisa de peças", "Guarda do acervo: mods e
hooks, pesquisa", "Testes do papel do Maestri com Codex e Copilot".

- **O que é:** o hub guarda peças prontas que todo maestro, dentro ou fora do hub, consulta para montar
  e conduzir um workspace, sem o Gustavo ditar e sem redescobrir. Peças são opções, não regras, e cada
  uma aceita personalização por workspace.
- **Tipos de peça admitidos:** papéis, setups, contratos-opção (roteamento de modelos, orquestração,
  onde abrir), presets, notas e fichários-modelo, rotinas-modelo, receitas de floor e de portal,
  workspace-modelo, ambientes, subagentes, perfis de modelo, hooks de início de sessão, skills de
  procedimento. A conta é campo de setup e roteamento.
- **Forma:** família de skills `maestro-*` por assunto (`maestro-acervo` é a porta), cada uma com
  catálogo curto e um arquivo por peça na própria pasta, em `agents/skills/<skill>/`, ligada por junction
  em `~/.claude/skills` e `~/.agents/skills` (prefixo diferente de `maestri-*`, que o app regrava).
- **Setup:** receita de comandos da CLI que o maestro executa (ele não aplica partitura); a partitura é
  também porta de entrada: o Gustavo cria, pede para guardar, e o maestro escreve a receita e guarda a
  partitura junto. **Variante:** declara a base e só o que muda; setups citam papéis pelo nome.
- **Papéis:** genéricos (acaba "Redator SBF", "Redator TRF3"); a parte do cliente vem do `AGENTS.md` da
  iniciativa; o maestro pode criar uma versão local (nome, complexidade, divisão de trabalho) em
  `maestro/` da iniciativa. Na hora de usar, confere a cópia da biblioteca do Maestri contra o acervo,
  cria o papel global se faltar e reescreve se estiver diferente. Ajuste de papel só pelo prompt (editar
  o papel reescreve os arquivos e reinicia os terminais).
- **Onde abrir (padrão do contrato-opção):** iniciativa na pasta dela, para os três harnesses (o
  Copilot recebe o contrato pelo arquivo global e a parte do cliente pela pasta; revê "Copilot só na
  raiz" de "Portas de entrada do hub"); o que cruza iniciativas na raiz; código no repositório.
- **Contrato dentro do papel:** `claude-md-and-agents-md` ligado em cada par pelo kit; o Codex depende
  do marcador de raiz, também do kit.
- **Primeira instrução:** o contrato manda o maestro começar por `maestro-acervo`, mais um hook de
  início de sessão que só age com `MAESTRI_TERMINAL_ID` (garantido no Claude Code).
- **Aprender e guardar:** o maestro acrescenta sozinho; pede aval para alterar ou apagar peça citada ou
  usada, mexer em catálogo ou descrição de skill, peça com nome ou gatilho parecido, ou contrato-opção
  que se diz padrão. O pedido mostra o que muda, quem é afetado, se já roda como personalização em
  algum workspace, a alternativa de variante e a recomendação do verificador.
- **Guarda:** forte no Claude Code (mod ou hook no escopo do usuário, verificador em outro modelo
  obrigatório antes de alterar); Codex e Copilot não gravam no acervo e deixam propostas em
  `agents/maestro/propostas/`.
- **Quem usa:** registro de uso por máquina em `agents/maestro/uso/<máquina>.md`, gravado por hook,
  mais os papéis atribuídos no Maestri e as citações entre peças.
- **Primeiro lote (escrito na construção):** papéis frequentes sem nome de cliente e o Designer de
  visuais, os de nicho como estão; a partitura de hoje como receita e o arranjo deste workspace;
  roteamento de modelos (com o FreeLLMAPI para tarefas simples, o que cobre o contrato de roteamento
  que entrou no mapa na rodada 2 do mapeamento), orquestração e onde abrir; o lembrete e a guarda.
- **Fora, por ora:** a automação que aplica e audita o Maestri (pode voltar depois).
