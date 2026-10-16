## Faixa 9: Skills e acervo do maestro

Entrega, no par 1 e em HOME de ensaio: a tabela de roteamento de skills com o hook de entrada que a confere, as duas
camadas de skills, a família `maestro-*` com o primeiro lote do acervo, o hook de início que só age no Maestri, a
guarda do acervo nos três harnesses e o registro de uso. Fontes: Answers dos tickets 15, 40, 43, 44 e 39, o comentário
de 2026-10-12 do ticket 16 e as linhas de "Decisions so far" do mapa.

### User stories

1. Como Gustavo, quero que a skill certa dispare sem eu pedir pelo nome, para não depender de a descrição da skill bastar (na frente da cidade, com a suíte instalada, a ferramenta de skill disparou só 2 vezes).
2. Como Gustavo, quero que um pedido de pesquisa que não cita o FreeLLMAPI faça a skill dele disparar, para que o roteamento passe no primeiro caso de teste.
3. Como agente em qualquer harness, quero receber "use a skill X" no contexto quando o meu pedido casa com uma linha da tabela, para saber qual skill usar naquele passo.
4. Como mantenedor do hub, quero que a tabela guarde só o que a descrição da skill não resolve, para que ela não vire uma segunda lista de todas as skills.
5. Como maestro, quero que uma linha da tabela possa casar por palavras do pedido, por tipo de nota (pelo caminho) ou pelo papel do recruta, para cobrir os três jeitos de uma skill ser a certa.
6. Como recruta com um papel, quero que as linhas do meu papel indiquem as skills daquele papel, para não carregar as skills de todos os papéis.
7. Como agente, quero que o hook de entrada funcione sem chamar modelo nenhum, para que ele seja rápido, barato e previsível.
8. Como agente no Codex ou no Copilot, quero que, se o hook de entrada não conseguir injetar o texto, a mesma indicação chegue como regra no contrato do meu harness, para não ficar sem roteamento.
9. Como autor de brief ou de skill de processo, quero citar a skill pelo nome em cada passo, para que o roteamento não dependa só do hook.
10. Como Gustavo, quero que o verificador do fim da resposta registre se a skill indicada rodou, sem obrigar, para saber onde o roteamento falha sem travar o trabalho.
11. Como maestro, quero que o registro aponte a linha da tabela a ajustar, para corrigir sem procurar.
12. Como maestro, quero corrigir a tabela sozinho a partir do registro e avisar o Gustavo em uma linha, para que o roteamento melhore sem rodada de aval.
13. Como Gustavo, quero que a guarda do acervo abra exceção só para o maestro no arquivo da tabela, para que a correção sozinho não fure a guarda do resto do acervo.
14. Como agente em qualquer harness, quero enxergar na junction global só as skills de uso geral (a busca, o FreeLLMAPI, o fluxo do Matt Pocock, a família `maestro-*` e as poucas que servem a qualquer trabalho), para não pagar a lista inteira a cada turno.
15. Como recruta de um papel, quero que as skills do meu papel entrem só na pasta do meu papel, pela receita de setup, para ter o que preciso sem poluir os outros.
16. Como Gustavo, quero que o GSD saia do escopo global com cópia antes, para limpar a camada global sem perder nada.
17. Como Gustavo, quero que a skill `armis-docx`, copiada do vault, entre na tabela, para que o roteamento a alcance.
18. Como maestro, quero que as skills de design por papel da frente da cidade sejam as primeiras linhas de papel da tabela, para começar pelo caso que já mostrou a falha.
19. Como maestro do Maestri, dentro ou fora do hub, quero consultar peças prontas para montar e conduzir um workspace, para não redescobrir nem depender de o Gustavo ditar.
20. Como maestro, quero começar pela skill `maestro-acervo`, que é a porta da família, para achar a skill do assunto que preciso.
21. Como maestro, quero que cada skill `maestro-*` tenha um catálogo curto e um arquivo por peça na própria pasta, para que o acervo cresça sem que o catálogo exploda.
22. Como Gustavo, quero que a família use o prefixo `maestro-`, diferente de `maestri-*`, para que o app do Maestri nunca regrave nem apague o acervo.
23. Como maestro, quero que cada peça seja opção e não regra, e aceite uma versão local por workspace em `maestro/` da pasta onde o workspace abre, para adaptar sem mexer na peça.
24. Como maestro, quero que um setup seja uma receita de comandos da CLI do Maestri que eu executo, para montar o workspace sozinho (eu não aplico partitura).
25. Como Gustavo, quero criar uma partitura pela interface e pedir para guardar, e que o maestro escreva a receita e guarde a partitura junto, para que as partituras não morram e eu possa aplicá-las pela interface.
26. Como maestro, quero que uma variante declare a base e só o que muda, e que setups citem papéis pelo nome, para não copiar peça inteira.
27. Como maestro, quero papéis genéricos, sem nome de cliente (acaba "Redator SBF", "Redator TRF3"), com a parte do cliente vinda do `AGENTS.md` da iniciativa, para reusar o mesmo papel em qualquer iniciativa.
28. Como maestro, quero criar uma versão local de um papel (nome, complexidade, divisão de trabalho) em `maestro/` da iniciativa, para ajustar sem tocar no acervo.
29. Como maestro, quero, na hora de usar um papel, conferir a cópia da biblioteca do Maestri contra o acervo, criar o papel global se faltar e reescrever se estiver diferente, para que a biblioteca siga o acervo.
30. Como Gustavo, quero que o ajuste de papel em uso seja feito só pelo prompt, para não reiniciar os terminais (editar o papel reescreve os arquivos e reinicia os terminais).
31. Como maestro, quero contratos-opção prontos (roteamento de modelos com o FreeLLMAPI para tarefas simples, orquestração e onde abrir), para seguir um jeito recomendado quando ninguém disser outro.
32. Como maestro, quero que o contrato-opção "onde abrir" traga o padrão por tipo (workspace de iniciativa na pasta dela para os três harnesses, o que cruza iniciativas na raiz, código no repositório), para abrir no lugar certo.
33. Como maestro, quero no primeiro lote os papéis frequentes (Receptor, Redator, Revisor Cruzado, Escrivão, Gestor Git, Scripter, Curador de Prints) e o Designer de visuais, com os de nicho como estão, para ter o acervo útil desde o primeiro dia.
34. Como maestro, quero no primeiro lote a partitura de hoje como receita e o arranjo deste workspace, para remontar o workspace atual sem lembrar de cabeça.
35. Como maestro, quero que os tipos de peça ainda sem conteúdo (preset de agente, nota e fichário-modelo, rotina-modelo, receitas de floor e de portal, workspace-modelo, ambiente, subagente, perfil de modelo, skill de procedimento) existam no catálogo e nasçam vazios, para que a primeira peça de cada tipo já tenha lugar.
36. Como maestro, quero que a conta seja campo do setup e do roteamento, não peça própria, para não duplicar setups por conta.
37. Como agente aberto num terminal do Maestri, quero que um hook de início de sessão, que só age quando existe `MAESTRI_TERMINAL_ID`, me lembre de que sou maestro e de onde está o acervo, para a primeira instrução chegar mesmo em workspace novo.
38. Como agente fora do Maestri, quero que esse hook de início não faça nada, para não receber lembrete que não me serve.
39. Como maestro, quero acrescentar sozinho uma variante nova, uma peça nova sem sobreposição ou uma nota de "o que funcionou", para que o acervo aprenda sem pedir aval a cada passo.
40. Como Gustavo, quero dar aval antes de o maestro alterar ou apagar peça citada ou usada, mexer em catálogo ou descrição de skill, acrescentar peça com nome ou gatilho parecido com outra, ou acrescentar contrato-opção que se diz padrão, para que nada que já roda mude sem eu ver.
41. Como Gustavo, quero que o pedido de aval mostre numa tela o que muda (antes e depois), quem é afetado, se a mudança já roda como personalização em algum workspace, a alternativa de virar variante e a recomendação do verificador, para decidir sem abrir arquivo.
42. Como Gustavo, quero que um verificador em outro modelo rode obrigatoriamente antes de o maestro Claude Code alterar uma peça, para que o maestro não aprove a si mesmo.
43. Como Gustavo, quero que a guarda forte rode no escopo do usuário, para valer também dentro da pasta de um papel do Maestri.
44. Como agente no Codex ou no Copilot, quero ter a gravação no acervo recusada com o caminho de `agents/maestro/propostas/`, para contribuir com uma proposta em vez de gravar direto.
45. Como maestro Claude Code, quero avaliar as propostas deixadas em `agents/maestro/propostas/`, para que a contribuição do Codex e do Copilot entre pelo mesmo crivo.
46. Como Gustavo, quero que a guarda pegue a gravação tanto pelo caminho real do hub quanto pelo caminho da junction, para que ninguém contorne a guarda pelo atalho.
47. Como maestro, quero um registro de uso leve (peça, workspace, máquina, data), um arquivo por máquina em `agents/maestro/uso/<máquina>.md`, gravado por hook, para saber se uma peça é usada antes de alterá-la.
48. Como maestro, quero somar ao registro de uso os papéis atribuídos (dos arquivos do Maestri) e as citações entre peças, para saber quem é afetado por uma mudança.
49. Como Gustavo, quero que o hook de uso grave sem atrito para o agente, para que o registro não dependa de o agente lembrar.
50. Como mantenedor, quero que cada skill da família tenha `name` e `description` válidos no padrão de skills, com a descrição no formato "faz X. Use when...", referência cruzada pelo nome e o mesmo preâmbulo, para que as skills se achem entre si.
51. Como integrador (faixa 8), quero receber os hooks desta faixa como fragmento no formato combinado, para juntar sem editar a configuração de outra faixa.

### Implementation decisions

- **Onde as skills moram** (14, 15): todas em `agents/skills/<skill>/` no hub (armazenamento). Exposição: só as de uso geral ficam ligadas por junction em `~/.claude/skills` (Claude Code) e `~/.agents/skills` (Codex e Copilot) nas duas máquinas; as de papel entram só na pasta do papel, pela receita de setup (15, rodada 2; ver "Duas camadas"). As junctions são do kit de par (faixa 8); esta faixa entrega o conteúdo da pasta e a seleção.
- **Tabela de roteamento** (15): `agents/skills/routing.yml`. Cada linha é gatilho → skill, e o gatilho é um de três tipos: palavras do pedido, tipo de nota pelo caminho, papel do recruta. Guarda só o que a descrição não resolve e cobre as duas camadas (geral e de papel). Primeiras linhas: a skill do FreeLLMAPI para pedidos de pesquisa, `armis-docx`, e as skills de design por papel da frente da cidade (o retrato do comentário de 2026-10-15 do ticket 15).
- **Hook de entrada** (15): sem IA. Confere o pedido contra a tabela e injeta no contexto "use a skill X". No Claude Code, pelo contexto adicional do hook de entrada (pesquisa do ticket 44); no Copilot CLI, a extensão `onUserPromptSubmitted` (vista na bancada de acesso). Onde não injetar (Codex e Copilot, não verificado), a linha vira regra no contrato daquele harness, como a checagem de início (14); o texto da regra é entregue à faixa 1.
- **Citação nos passos** (15): briefs e skills de processo citam a skill pelo nome em cada passo. Vale para as peças do acervo que descrevem passos (setups, papéis, contratos-opção de orquestração).
- **Verificador do fim** (15, 14): registra se a skill indicada rodou, sem obrigar, e aponta a linha da tabela a ajustar. Usa o mecanismo de fim de resposta de cada harness decidido no 14 (Claude Code pelo mod com `turn.start`/`classic.Stop`; Copilot pelo hook `agentStop` mais a extensão `onAgentStop`; Codex pelo hook `Stop`), em entrada própria, ao lado da do checkpoint (faixa 2).
- **Ajuste da tabela** (15, rodada 3, B): o maestro corrige a tabela sozinho pelo registro e avisa em uma linha. A guarda do acervo tem exceção para o maestro nesse arquivo.
- **Duas camadas** (15, rodada 2): a junction global leva só as de uso geral (a busca, o FreeLLMAPI, o fluxo do Matt Pocock, a família `maestro-*` e as poucas que servem a qualquer trabalho). As de um papel ficam no acervo e entram só na pasta daquele papel, pela receita de setup. A saída do GSD do escopo global, com cópia antes, é do kit (faixa 8).
- **Família `maestro-*`** (40, 43): uma skill por assunto; `maestro-acervo` é a porta. Cada skill tem `SKILL.md` curto como catálogo e um arquivo por peça na própria pasta (o padrão de referências das skills). Prefixo diferente de `maestri-*`, que o app regrava e apaga (só os sete nomes oficiais). Forma das descrições como a família oficial: "faz X. Use when...", referência cruzada pelo nome, o mesmo preâmbulo.
- **Tipos de peça admitidos** (40, 43): papéis, setups, contratos-opção (roteamento de modelos, orquestração, onde abrir), presets de agente, notas e fichários-modelo, rotinas-modelo, receitas de floor (com os comandos de preparo) e de portal (telas e tamanhos para QA), workspace-modelo (clonar com `workspace create --from`), ambientes (Local, WSL...), subagentes, perfis de modelo (`--model`, `--profile`, endereço de gateway), hooks de início de sessão e skills de procedimento. Conta é campo de setup e de roteamento. Estilo de saída e plugin ficam fora (43: valem pouco).
- **Setup** (40, 43): receita de comandos da CLI que o maestro executa; o maestro não aplica partitura nem configura hooks de floor pela CLI. A partitura é porta de entrada: o Gustavo cria e pede para guardar; o maestro lê o JSON dela em `~/.maestri/partituras/` (só leitura), escreve a receita e guarda a partitura junto. Variante declara a base e só o que muda; setups citam papéis pelo nome.
- **Papéis** (40, R55, R56): genéricos; a parte do cliente vem do `AGENTS.md` da iniciativa. Versão local (nome, complexidade, divisão de trabalho) em `maestro/` da iniciativa (nada com ponto, que não replica; 12). Na hora de usar: compara a cópia da biblioteca do Maestri com o acervo, cria o papel global (papel sem workspace) se faltar e reescreve se estiver diferente. Ajuste de papel em uso só pelo prompt.
- **Personalização local** (40, R50 e R54; 12): em `maestro/` dentro da pasta onde o workspace abre.
- **Primeiro lote** (40, R53): papéis Receptor, Redator, Revisor Cruzado, Escrivão, Gestor Git, Scripter, Curador de Prints e o Designer de visuais; os de nicho como estão. Setups: a partitura de hoje como receita e o arranjo deste workspace. Contratos-opção: roteamento de modelos (com o FreeLLMAPI para tarefas simples), orquestração, onde abrir (padrão: iniciativa na pasta dela para os três harnesses; o que cruza iniciativas na raiz; código no repositório). Peças dos harnesses: o lembrete de início de sessão e a guarda. Os outros tipos nascem vazios. O primeiro lote lê o Maestri e o vault só para leitura.
- **Material de fonte para os contratos-opção de roteamento e orquestração** (39, pesquisa, não decisão do mapa): custo por tarefa e não por token; aliases de modelo e `opusplan`; effort por sessão, terminal ou subagente (`low` para subagentes); refazer em effort maior só com sinal de falha; orçamento por `--max-budget-usd`; orquestrador só com volume independente; medir com `/usage` e `total_cost_usd`. Entra como conteúdo das peças, que são opção.
- **Primeira instrução** (40, R52; 43): o contrato do hub diz "no Maestri, como maestro, comece pela skill `maestro-acervo`" (texto entregue à faixa 1) e um hook de início de sessão no escopo do usuário, que só age com `MAESTRI_TERMINAL_ID`, lembra o agente de que é maestro e de onde está o acervo. Garantido no Claude Code; Codex e Copilot dependem de teste. Esse hook e o hook de uso agem em qualquer pasta, dentro ou fora do hub (40: o acervo serve a todo maestro; 43): são a exceção à regra "sai na hora fora do hub" do 14, que vale para os hooks de início com a vigia, fim e recusa. Leitura conciliadora dos dois tickets, **[núcleo]**. `MAESTRI_TERMINAL_ID` identifica o terminal, não o papel: distinguir maestro de recruta segue pendente.
- **Regras de aval** (40, R47 e R48): livre: variante nova, peça nova sem sobreposição, nota de "o que funcionou". Pede aval: alterar ou apagar peça citada ou usada; mexer no catálogo ou na descrição de uma skill; acrescentar peça com nome ou gatilho parecido; acrescentar contrato-opção que se diz padrão. A tela de aval mostra o que muda (antes e depois), quem é afetado, se já roda como personalização em algum workspace, a alternativa de variante e a recomendação do verificador.
- **Guarda do acervo no Claude Code** (40, R46; 44): forte, no escopo do usuário (plugin do hub como marketplace local, ou pasta em `~/.claude/skills`), para valer dentro de um papel do Maestri. Duas formas admitidas pela fonte: o mod (plugin com funções JS/TS, Claude Code 2.1.287 ou mais nova, API "early access"), que segura `Edit`/`Write` numa pasta e recusa, pede aval (`$.ui.ask`) ou avisa o modelo; ou o hook de settings `PreToolUse` com `deny`/`ask`, cujo filtro por caminho é "best-effort". Verificador em outro modelo obrigatório antes de alterar: pelo hook de settings do tipo `agent` (experimental, aceita `"model"`, rodado pelo harness) ou pelo mod impondo o modelo do subagente e recusando a edição até existir o relatório. Por causa dos 10 s de cada hook do mod (esperar o subagente conta), o desenho é "recusa, roda o verificador, libera com relatório e aval".
- **Guarda do acervo no Codex e no Copilot** (40, R46; 44): não gravam no acervo. Codex: `PreToolUse` em `apply_patch` com `deny` (não tem `ask` nem hook de modelo). Copilot CLI: `preToolUse` com `deny` ou a regra `--deny-tool='write(PATH)'`. A recusa aponta `agents/maestro/propostas/`, onde eles gravam a proposta para um maestro Claude Code avaliar.
- **O que a guarda cobre** (40, Guarda e Quem usa; 15, rodada 3; 12, rodada 12): o acervo, isto é `agents/skills/maestro-*/`, as skills de papel do acervo e a skill "nova iniciativa" (12). `agents/skills/routing.yml` tem a exceção do maestro (15). `agents/maestro/` fica fora da guarda: `propostas/` é aberta a todo harness e `uso/<máquina>.md` é gravado pelo hook de uso (o ticket 12 só põe essas duas pastas ali; nada se infere sobre pastas futuras). Se as skills de uso geral fora da família entram na guarda: aberto.
- **A guarda decide pelo arquivo-alvo, não pela pasta da sessão** (40, R46: escopo do usuário; 16: teste pelo caminho real e pela junction; 44): ela não se desliga só porque a sessão abriu fora do hub; o caminho real da gravação, inclusive via junction, diz se a peça é protegida. Conciliação com o "sai na hora fora do hub" do 14, **[núcleo]**. `MAESTRI_TERMINAL_ID` identifica o terminal, não o papel: distinguir maestro de recruta segue pendente.
- **Registro de uso** (40, R49 e R54; 44): uma linha (peça, workspace, máquina, data) em `agents/maestro/uso/<máquina>.md`, gravada por hook. No Claude Code, o mod vê toda skill carregada (`skill.prompt`, por `/nome`, pela ferramenta Skill ou num subagente); com hooks de settings são dois ganchos (`PreToolUse` em `Skill` e `UserPromptExpansion`). Garantido no Claude Code; Codex e Copilot dependem de teste. Somam-se os papéis atribuídos lidos dos arquivos do Maestri (cada terminal guarda `assignedRoleId`, `command` e a pasta) e as citações entre peças.
- **Contrato dentro do papel** (40, R51; 14): `claude-md-and-agents-md` ligado em cada par pelo kit de par (faixa 8), que confere se continua ligado. Codex e Copilot chegam ao `AGENTS.md` da raiz pelo `.git` da raiz (14, rodada 4; o marcador de raiz caiu).
- **Fronteira com as outras faixas** (plano): os hooks desta faixa vão como fragmento no formato combinado com a faixa 8, em entrada própria por evento (entrada, início, antes da ferramenta, depois da ferramenta, fim), sem editar a configuração de outra faixa. No "antes da ferramenta", esta faixa decide só os caminhos do acervo; a faixa 6 decide o resto.

### Testing decisions

- **Costura:** hub de ensaio (na forma do ticket 12, com `agents/skills/` e `agents/maestro/`) e HOME de ensaio. Os hooks são exercidos com a entrada JSON real de cada harness e, ao vivo, pelos harnesses reais em modo não interativo (`claude -p`, `codex exec`, `copilot -p`) com o HOME de ensaio. Nada em `~/.claude`, `~/.codex`, `~/.copilot`, na biblioteca de papéis do Maestri ou na configuração global do Maestri sem aval do Gustavo. `MAESTRI_TERMINAL_ID` é posto no ambiente do teste; o teste num terminal real do Maestri pede aval.
- **Critério de aceite de ponta a ponta:** um pedido de pesquisa que não cita o FreeLLMAPI, feito ao `claude -p` no HOME de ensaio, recebe "use a skill" do FreeLLMAPI e a skill dispara (o verificador do fim registra que rodou); e uma gravação no acervo pelo Codex e pelo Copilot é recusada com o caminho de propostas.
- Roteamento: um pedido que casa por palavras, uma nota pelo caminho e um recruta pelo papel recebem cada um a skill da linha certa; um pedido que não casa não recebe nada.
- Hook de entrada não chama modelo (sem rede durante o hook).
- Verificador do fim: com a skill indicada rodando, registra "rodou"; sem rodar, registra "não rodou" com a linha da tabela, e a resposta não é bloqueada.
- Maestro grava a tabela e passa; outro agente gravando a tabela no Claude Code cai na guarda.
- Hook de início: sem `MAESTRI_TERMINAL_ID`, nada no contexto; com ele, o lembrete com `maestro-acervo` no contexto.
- Guarda no Claude Code: alterar peça citada ou usada pede aval e não libera sem o relatório do verificador; peça nova sem sobreposição passa; mexer no catálogo pede aval. Pelo caminho real e pelo da junction.
- Guarda no Codex e no Copilot: gravação no acervo recusada com o caminho de propostas, pelo caminho real e pelo da junction; gravação em `agents/maestro/propostas/` passa.
- Registro de uso: usar uma skill da família gera uma linha (peça, workspace, máquina, data) no arquivo da máquina do hub de ensaio.
- Forma: a tabela passa num esquema; cada `SKILL.md` da família tem `name` e `description` válidos; cada peça citada num catálogo existe.
- Testes que o ticket 16 pede para a construção: junction com mod (a doc fala de symlink); regra de caminho pela junction e pelo caminho real; `$.ui.ask` num terminal do Maestri sem ninguém olhando; tempo de um hook `agent` em Sonnet; hooks de uso e de início no Codex e no Copilot.

### Out of scope

- A automação que aplica e audita o Maestri (40) e migrar os workspaces existentes (mapa).
- O `freellmapi-mcp` e a skill que ensina a usá-lo; só o roteamento dessa skill entra (mapa, Q13).
- A convivência entre superpowers, GSD e Matt (mapa); aqui só a saída do GSD do escopo global, que é do kit.
- As junctions, a saída do GSD com cópia e `claude-md-and-agents-md` (faixa 8); o texto do contrato (faixa 1); o checkpoint do fim de resposta (faixa 2); as guardas de gravação fora do acervo (faixa 6).
- O hub como lugar que controla como harnesses e modelos trabalham (segundo mapa), inclusive registro de uso além do acervo; o registro de uso do acervo, já decidido, fica.
- Estilo de saída, plugin de harness e atalhos de barra como tipos de peça (43).
- O suite de busca e o portal do projeto como peças do acervo ("Not yet specified" do mapa).

### Pontos abertos para a construção

- Injeção do hook de entrada no Codex e no Copilot (não verificado); se falhar, vale a regra no contrato daquele harness.
- Saber, no fim da resposta, se a skill rodou no Codex e no Copilot (não verificado).
- Onde mora o registro do verificador do fim que aponta a linha da tabela (não decidido).
- A skill do FreeLLMAPI que a tabela aponta precisa existir em `agents/skills/`; a skill em si está fora do escopo (mapa), então qual skill é o alvo do teste de aceite fica a confirmar.
- `armis-docx` depende da cópia dos pilotos do vault (pergunta do Worker 1 ao Gustavo no plano).
- Onde as skills de papel moram dentro do acervo e como a receita de setup as põe na pasta do papel (cópia ou ligação): não decidido.
- Se as skills de uso geral fora da família `maestro-*` também ficam sob a guarda: não decidido (o que a guarda cobre está nas Implementation decisions; o núcleo foi corrigido, não cobre mais `agents/maestro/**`).
- O hook de início age com `MAESTRI_TERMINAL_ID`, mas todo terminal do Maestri, recruta ou maestro, tem essa variável (14). Como o hook distingue o maestro do recruta não está decidido.
- Mod ou hook de settings para a guarda: os dois são admitidos; a escolha sai do teste (junction com mod, `$.ui.ask` sem ninguém olhando, tempo do hook `agent` em Sonnet).
- Lacuna de dono do ticket 16: quem escolhe o modelo do verificador da guarda.
- Lacuna de dono do ticket 16: como o erro de peça citada que sumiu chega ao Gustavo.
- Como a tela de aval é mostrada ao Gustavo (o `$.ui.ask` do mod é o candidato da fonte; não decidido).
- Hooks de uso e de início no Codex e no Copilot (precisam de teste; 40, 44).
- Hooks do usuário "saem na hora fora do hub" (14) e o acervo serve a todo maestro "dentro ou fora do hub" (40, 43): resolvido como leitura conciliadora **[núcleo]** nas Implementation decisions ("Primeira instrução"); pede aval do Gustavo.
- Reescrever na biblioteca do Maestri um papel que esteja diferente (R55) reescreve os arquivos e reinicia os terminais com aquele papel (45). Quando reescrever um papel em uso não está decidido.
- Precisa de teste (43): o FreeLLMAPI em cada harness; se o clone de workspace leva os arquivos da pasta.
- Não verificado (39): como o Maestri abre cada terminal (diretório, `--model`, `--effort`), o que pesa no contrato-opção de roteamento de modelos.
- Quando a guarda e as guardas da faixa 6 respondem no mesmo evento, vale a mais restritiva: proposta do plano, não verificado que os três harnesses juntam assim.

## Faixa 10: Manutenção e kit de cliente

Entrega, no par 1 e em hub e HOME de ensaio: o script que move para `_archive/` conferindo o outro par, a cópia de
segurança diária pelo `.git` da raiz, a conferência da cabeça do contrato que o MCP entrega, e o kit de cliente com o
TBXark/mcp-proxy, rotas e tokens. Fontes: Answers dos tickets 33, 36, 34, 14 e 41, comentários do ticket 16 e o Answer
do ticket 11 para a gravação do cliente. O que vinha das rodadas 7 e 8 do ticket 56 (prazo de 30 dias e o apagamento,
"remover = arquivar", política de recuperação, "dois dias bastam", "quem percebe a falha") está marcado
**[ticket aberto: 56]** e fica fora desta construção: o 56 só continua depois dela (16, 2026-10-16).

### User stories

1. Como Gustavo, quero que o que termina vá para o `_archive/` da própria raiz, para tirar do caminho sem perder.
2. Como agente, quero mover uma pasta para o `_archive/` só por um script, para que a mudança não separe edições entre as máquinas (o LiveSync não garante mover pasta com a outra máquina editando).
3. Como agente, quero que o script confira antes se o outro par está em dia e sem edição recente na pasta, para mover só quando é seguro.
4. Como agente, quero que o script recuse e diga por quê quando o outro par estiver atrasado ou a pasta tiver edição recente, para eu saber o que esperar.
5. **[ticket aberto: 56]** Como Gustavo, quero que "remover" queira dizer mover para o `_archive/` por 30 dias e só depois apagar, para ter um mês de volta atrás.
6. **[ticket aberto: 56]** Como Gustavo, quero que um agente só apague de vez com a minha permissão ou depois dos 30 dias, para que nada some antes da hora sem eu saber.
7. **[ticket aberto: 56]** Como Gustavo, quero que alguém confira os 30 dias e apague o que passou do prazo, para que o `_archive/` não cresça para sempre. (O 16, resolvido, cita a lacuna de dono; o prazo em si só está no 56.)
8. Como Gustavo, quero uma cópia de segurança diária da vista no GitHub privado, para ter histórico mesmo que a replicação leve um estrago às duas máquinas em segundos e a compactação apague o histórico do banco.
9. Como Gustavo, quero um `.git` na raiz de cada máquina, sem replicar, com um ramo por máquina, para que as cópias das duas máquinas não se misturem.
10. Como Gustavo, quero que o git só faça commit e push, nunca pull nem checkout, para que ele nunca seja escritor do disco.
11. Como Gustavo, quero que cada máquina empurre com a própria deploy key, para que o acesso ao repositório seja só do hub e por máquina.
12. Como Gustavo, quero que a pasta não replicada (o que tem ponto no nome e a pasta com `local: true`) fique fora do GitHub, para que o que é de uma máquina só não saia dela.
13. Como Gustavo, quero que a cópia diária da vista do hub inclua as iniciativas de cliente que integram essa vista, respeitando as exclusões decididas (o que tem ponto e a pasta com `local: true`), para que a cópia cubra a vista inteira (33, cópia diária da vista; 12, conteúdo de cliente na vista replicada). A formulação "nenhuma iniciativa vetada" da rodada 7 do 56 fica só como histórico, sem ampliar o alcance.
14. **[ticket aberto: 56]** Como Gustavo, quero recuperar um estrago por um agente comigo vendo, ou eu mesmo por comando pelo GitHub, para voltar atrás sem depender de um mecanismo novo. (O comando de recuperar binário, 33 R71, não depende disto.)
15. **[ticket aberto: 56]** Como Gustavo, quero que dois dias de distância na cópia bastem, para que uma cópia diária seja suficiente.
16. Como Gustavo, quero saber quando a cópia diária falha, para não descobrir só na hora de recuperar. (A forma, saída ≠ 0 e item no estado da vigia, é **[núcleo]**; a política geral "quem percebe a falha" é do 56 e fica fora.)
17. Como agente que chega pelo MCP de um par, quero receber no `instructions` do MCP a cabeça do `AGENTS.md`, para conhecer o contrato sem ter o arquivo.
18. Como Gustavo, quero que a cabeça seja autossuficiente e caiba em 2.000 caracteres, para não ser cortada (o Claude Code corta em 2.048).
19. Como Gustavo, quero que a cabeça entregue pelo MCP siga o `AGENTS.md` quando ele muda, para que o cliente não receba contrato velho.
20. Como agente que vai gravar pelo MCP, quero que a descrição de cada ferramenta de gravação comece por "antes de gravar, leia `AGENTS.md`" (36) e, onde a API leva `base_rev`, siga com "grave com a `base_rev` lida; conflito = releia e refaça" (**[núcleo]**), para que a regra chegue pelo único canal que alcança o modelo nos três harnesses.
21. Como Gustavo, quero usar o hub de uma sandbox ou de uma máquina de passagem como cliente, sem cópia própria, para trabalhar de qualquer computador.
22. Como Gustavo, quero que o cliente entre na tailnet com chave efêmera, com validade e com tag, para que o acesso morra sozinho.
23. Como Gustavo, quero que um grant limite a tag dos clientes à porta do proxy no par, para que o cliente não alcance mais nada do par.
24. Como agente no cliente, quero buscar no hub pela rota `/busca/mcp`, para achar o trecho certo como no par.
25. Como agente no cliente, quero ler o banco pela rota `/banco/mcp`, só de leitura, para consultar notas sem risco de gravar.
26. Como Gustavo, quero que o cliente seja só de leitura por padrão e que a gravação seja ligável por cliente, quando eu quiser, pela rota `/banco-escrita/mcp` com token próprio e a mesma guarda de versão, para escolher cliente a cliente quem grava.
27. Como Gustavo, quero um token por rota, de variável de ambiente no cliente, enviado como `Authorization: Bearer` nos três harnesses, para revogar uma rota sem mexer nas outras e não deixar token em arquivo de configuração.
28. Como Gustavo, quero que o cliente nunca receba a credencial do CouchDB, para que o `READ_ONLY` do MCP não seja a única barreira (não é garantia no banco).
29. Como Gustavo, quero tudo só pela tailnet, nunca pelo Funnel, para que o hub não fique exposto na internet.
30. Como Gustavo, quero que o proxy fique preso ao endereço da tailnet do par, para não escutar em outras interfaces.
31. Como agente no Copilot CLI de um cliente, quero que o kit ligue `--allow-all-mcp-server-instructions`, para que o `instructions` do MCP entre no prompt de sistema.
32. Como agente no cliente, quero que o kit ponha o contrato na configuração global do meu harness onde der para instalar, para que o contrato chegue também por arquivo.
33. Como agente no cliente, quero fazer a checagem de início pela ferramenta do MCP, para saber o estado do hub sem o arquivo da vigia.
34. Como agente no Codex de um cliente, quero as ferramentas do MCP do hub aprovadas de antemão, para não parar a cada chamada.
35. Como Gustavo, quero que uma sessão fora do hub, como cliente, funcione igual à do par na busca e nas regras de gravação, para não ter dois jeitos de trabalhar.
36. Como Gustavo, quero instalar o kit de cliente com o mínimo de passos, para ligar uma sandbox depressa.
37. **[ticket aberto: 56]** Como Gustavo, quero que o cliente use os modelos na nuvem com qualquer iniciativa, sem iniciativa de cliente vetada, para não restringir o cliente por iniciativa.

### Implementation decisions

- **Mover para o `_archive/`** (36, R25; 12; mapa): cada raiz tem o seu `_archive/` (com sublinhado, não ponto, então replica). Mover é só por script, que antes confere que o outro par está em dia e que a pasta não tem edição recente; se não, recusa dizendo por quê. Motivo testado: mover pasta com a outra máquina editando separa a edição (38).
- **Prazo de 30 dias** (**[ticket aberto: 56]**, rodada 7; fora desta construção): "remover" é mover para o `_archive/` por 30 dias e depois apagar; agente só apaga com permissão do Gustavo ou depois dos 30 dias. O desenho do núcleo, `limpar-arquivo` na tarefa diária com `-WhatIf`, fica como contexto **[núcleo]**; dono e agendamento são **[formato]**.
- **Data do arquivamento** (**[núcleo]**): `_archive/<AAAA-MM-DD>--<nome>/`, a data no nome da pasta (um arquivo de data com ponto não replicaria, 12). Não substitui `archived_at` nem o esquema de origem do catálogo do 12.
- **Estado do outro par** (33, 34): cada par dispara a replicação das próprias mudanças para o outro; o estado das replicações está no `_scheduler/docs` do CouchDB, que a vigia lê. O limite de "parado" decidido é 15 min com a outra máquina ligada; com a outra desligada não é divergência.
- **Cópia de segurança diária** (33, R60; 06): um `.git` na raiz de cada máquina (não replica, porque tem ponto), um ramo por máquina, só commit e push; nunca pull nem checkout; não é escritor do disco. Repositório privado no GitHub (o Gustavo vai criá-lo, 16, 2026-10-16) com deploy key por máquina, com escrita, só nele (06, mantido pelo 33). Pasta não replicada fica fora (glossário). A cópia inclui as iniciativas de cliente que integram a vista, fora só o que não replica (33, 12; a rodada 7 do 56 confirma, mas não é a fonte necessária). Recuperação: um agente com o Gustavo vendo, ou ele por comando pelo GitHub; dois dias de distância bastam (**[ticket aberto: 56]**, rodada 8). A falha da cópia: saída ≠ 0 e item `copia-diaria` no estado da vigia, que notifica (**[núcleo]**; a política geral é do 56). O `.git` da raiz também serve para Codex e Copilot chegarem ao `AGENTS.md` numa subpasta (14, rodada 4); a faixa 1 o cria.
- **Cabeça do contrato no MCP** (36, R33; 41): o fork do MCP do banco (faixa 5) leva no `instructions` o começo do `AGENTS.md`, uma cabeça autossuficiente de até 2.000 caracteres (margem sob o corte de 2.048 do Claude Code). A descrição de cada ferramenta de gravação começa por "antes de gravar, leia `AGENTS.md`" (36; o acréscimo sobre `base_rev` é **[núcleo]**): é o único canal que a fonte mostra chegando ao modelo nos três harnesses (41). A cabeça segue o `AGENTS.md` porque o fork a relê a cada `initialize`, sem cópia (**[núcleo]**, fecha a lacuna de dono 5 do 16); esta faixa só confere que a cabeça existe e cabe (dono **[formato]**).
- **O que cada harness faz com o `instructions`** (41): Claude Code o recebe (corte em 2.048); Copilot no VS Code o põe inteiro no prompt do modo agente se alguma ferramenta do servidor estiver ligada; Copilot CLI só põe os de servidores "allowlisted", e os outros sob demanda, a menos que `--allow-all-mcp-server-instructions` (desde a 1.0.66); Codex o manda na requisição como descrição do grupo de ferramentas, sem efeito confirmado no modelo.
- **Cliente** (34; glossário): sandbox ou máquina de passagem, sem CouchDB nem cópia, que só funciona com um par ligado e por padrão só lê. Entra na tailnet com chave efêmera, com validade e tag. Nunca recebe a credencial do CouchDB; a senha do CouchDB fica só nos pares (11). Tudo só pela tailnet, nunca o Funnel.
- **Proxy de MCP no par** (14, rodada 7): o TBXark/mcp-proxy em cada par, preso ao endereço da tailnet, uma porta, uma rota e um token por servidor: `/busca/mcp` (a busca, obsidian-hybrid-search), `/banco/mcp` (o MCP do banco só de leitura, instância com `READ_ONLY=true` e token; 34) e `/banco-escrita/mcp` (a gravação ligável, instância com escrita e a mesma guarda de versão, token próprio; 11). Atrás do proxy, a busca e o MCP do banco do par seguem presos a 127.0.0.1 (14, rodada 1). A porta do proxy vai no `.env` do kit; a busca só aceita os `Host` permitidos (`--allowed-host`), então, se o proxy repassar o `Host` do cliente (não verificado), ela é configurada com o `Host` realmente observado (**[núcleo]**). As instâncias do MCP do banco: ver faixa 5 (duas por par é **[núcleo]**; leitura por padrão e escrita ligável são requisitos).
- **Grant da tailnet** (34): limita a tag dos clientes à porta do proxy.
- **Kit de cliente** (34, 36, 14; 16): o mínimo de passos: chave efêmera com tag; a linha de MCP em cada harness com o token de variável de ambiente e `Authorization: Bearer`; `--allow-all-mcp-server-instructions` no Copilot CLI; o contrato na configuração global do harness onde der para instalar; no Codex, as ferramentas do MCP do hub aprovadas de antemão (`default_tools_approval_mode="approve"`). Só leitura por padrão; o token de `/banco-escrita/mcp` só vai a um cliente quando o Gustavo pedir.
- **Checagem de início no cliente** (14): pela ferramenta do MCP (a ferramenta é da faixa 5).
- **Fronteira com as outras faixas** (plano): a busca (faixa 3) e o MCP do banco com as duas instâncias (faixa 5) são o que o proxy encaminha; o estado do outro par vem do banco (faixa 4); a falha da cópia diária entra no estado da vigia (faixa 7), que decide o aviso (**[núcleo]**); o registro das tarefas diárias segue o contrato do instalador da faixa 8 (**[formato]**).

### Testing decisions

- **Costura:** hub de ensaio e HOME de ensaio; scripts exercidos direto; o MCP e o proxy exercidos por um cliente de ensaio e pelos harnesses reais em modo não interativo (`claude -p`, `codex exec`, `copilot -p`) com a configuração de cliente no HOME de ensaio; 127.0.0.1 no lugar da tailnet; CouchDB de ensaio (ou um retrato do `_scheduler/docs` no mesmo formato) para o estado do outro par; um repositório nu local no lugar do GitHub. Nada global real sem aval do Gustavo: chave da tailnet, grant, tarefa no Agendador, push ao GitHub de verdade, configuração global dos harnesses.
- **Critério de aceite de ponta a ponta:** a pasta movida pelo script vai para o `_archive/` da raiz dela; a cópia diária gera commit no ramo da máquina; o cliente de ensaio busca pelo proxy e não grava pela rota de leitura.
- Mover: com o outro par em dia e sem edição recente, move; com o outro par atrasado além de 15 min, recusa dizendo por quê; com arquivo editado há pouco na pasta, recusa dizendo por quê.
- Prazo (**[ticket aberto: 56]**, fora do aceite desta construção): o que está no `_archive/` há mais de 30 dias é apagado; o que tem menos fica; antes dos 30 dias só apaga com permissão.
- Cópia diária: gera commit no ramo da máquina e empurra para um repositório nu local (**[formato]**; o push real ao GitHub é `ready-for-human`); o disco não muda (sem pull nem checkout); o que tem ponto e a pasta com `local: true` não entram; com o remoto quebrado, sai ≠ 0 e grava o item no estado da vigia (**[núcleo]**).
- Cabeça: depois de mudar a cabeça do `AGENTS.md` no hub de ensaio, o `instructions` que o MCP entrega é a cabeça nova (prova da faixa 5); cabeça ausente ou acima de 2.000 caracteres é apontada.
- Descrição das ferramentas de gravação começa por "antes de gravar, leia `AGENTS.md`", vista pelo cliente de ensaio através do proxy.
- Proxy: a busca responde pelo proxy (o `Host` que chega é registrado); busca por `/busca/mcp` responde; leitura por `/banco/mcp` responde; gravação por `/banco/mcp` é recusada; sem token ou com token de outra rota, recusado; por `/banco-escrita/mcp` com o token dela, grava com a versão lida e vira conflito visível com versão velha.
- Harnesses como cliente: os três, com a configuração do kit no HOME de ensaio e o token em variável de ambiente, fazem uma busca pelo proxy; o Copilot CLI recebe o `instructions` com `--allow-all-mcp-server-instructions`; a requisição do Codex é capturada para ver o `instructions` (36).
- Kit de cliente idempotente: rodar duas vezes no HOME de ensaio não muda nada na segunda.
- Medir: se o TBXark repassa o `instructions` do MCP (não verificado no 14).

### Out of scope

- O segundo par, a replicação real pela tailnet e a instalação de verdade nos HOMEs reais (`ready-for-human`, plano).
- A tela de colisão de três vias, "logo depois da construção" (25).
- Controle de acesso por pasta (mapa) e a política de dados de cliente para a segunda máquina (mapa, Q3).
- Tailscale e servidor SSH para a pasta não replicada e a operação remota (mapa).
- O fork do MCP do banco em si, com `base_rev`, o `instructions` e as duas instâncias (faixa 5); a busca (faixa 3); a vigia e o aviso (faixa 7); o kit de par (faixa 8).
- A consulta ao TI antes do Tailscale no notebook (caiu em 2026-10-14; em 2026-10-16 o TI confirmou que não há risco nem conflito com o software corporativo, ticket 16).
- O Claude Desktop não é cliente no sentido do glossário. A ponte `mcp-remote` (MCP stdio) para a busca e para o MCP do banco com escrita (11), mais a pasta conectada do Cowork com "Folder instructions" apontando o `AGENTS.md`: conteúdo decidido; o núcleo põe a ponte nesta faixa, gerada e não instalada; dono e "gerar sem instalar" são **[formato]**.

### Pontos abertos para a construção

- Lacuna de dono 4 (16): quem confere os 30 dias do `_archive/` e apaga: fora desta construção (**[ticket aberto: 56]**); o desenho `limpar-arquivo` na tarefa diária é **[núcleo]**, dono e agendamento **[formato]**.
- Lacuna de dono 5 (16): fechada como **[núcleo]**: o fork relê a cabeça a cada `initialize`, sem cópia; esta faixa confere tamanho e existência.
- Lacuna de dono 7 (16): onde fica o registro do aval de mudança no contrato: aberta, sem dono (o plano sugere a faixa 9), para o Gustavo.
- A data do arquivamento: no nome da pasta, **[núcleo]** (ver Implementation decisions).
- O que é "edição recente" para o script de mover, e o que ele faz com o outro par desligado (não decidido).
- Apagar ao fim dos 30 dias contra a Lição do vault "aval só para o contrato, os adaptadores e exclusões grandes": **[ticket aberto: 56]**.
- Quem percebe a falha da cópia diária: a forma desta proposta (saída ≠ 0 e item no estado da vigia) é **[núcleo]**; a decisão geral (vigia parada, hook calado, cópia diária, Tailscale bloqueado; base "notificação do Windows basta") é do 56 e fica fora desta construção.
- Como a cópia diária deixa de fora a pasta com `local: true` (a lista sai da exclusão gerada a partir do `index.md`, que o Prumo põe na faixa 1).
- Arquivos até 200 MiB vão ao banco (33), mas o limite de arquivo do GitHub para a cópia diária não foi conferido (não verificado).
- Restauração: quem faz vem do 56 (**[ticket aberto: 56]**); o comando, não decidido.
- Instâncias do es617 por par: leitura por padrão e escrita ligável, com guarda e token próprio, são requisitos (11, 14, 34); "duas por par, a de escrita reaproveitada atrás do proxy" é **[núcleo]**; as duas juntas no mesmo par: não verificado (34).
- Não verificado (14): o TBXark repassar o `instructions` do MCP; a latência pela tailnet; `${env:...}` no `mcp.json` do VS Code.
- Precisa de teste (41): o efeito de `--allow-all-mcp-server-instructions` no Copilot CLI; como a API da OpenAI mostra ao modelo o `instructions` que o Codex manda (capturar a requisição); o VS Code, que o teste das portas não cobriu. Não verificado (41): que lista é a "allowlisted" do Copilot CLI e o limite de tamanho das descrições.
- Chegar não é obedecer (36): no teste do VS Code o contrato chegou e a regra não foi seguida; a verificação dos cinco critérios precisa medir isso também no cliente.
- Como o contrato vai à configuração global do harness no cliente, que não tem o arquivo do hub para um link simbólico (cópia, e como fica em dia): não decidido.
- Skills e hooks no cliente: nada decidido; o cliente recebe o contrato e o MCP.
- Como o cliente acha o par e qual par usa quando os dois estão ligados (a lacuna 11 do 56 aponta o "endereço dos clientes" da rodada 7 do 14, que fixa o proxy em cada par, sem dizer qual o cliente usa).
- O grant limita a tag à porta do proxy, que atende as três rotas; a separação entre leitura e escrita fica só no token.
- O que o agente no cliente vê quando nenhum par está ligado (o cliente só funciona com um par ligado): não decidido.
