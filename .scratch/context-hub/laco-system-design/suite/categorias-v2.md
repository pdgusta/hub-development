# Categorias da suíte de design (versão 2)

Muda só o que o julgamento da v1 (`julgamento-v1.md`) pediu. As categorias não citadas aqui ficam como na v1 (`categorias.md`), com os ajustes da seção "Efeitos nas outras categorias". "(inferência)" marca palpite meu.

Leituras feitas nesta volta, por `curl` na fonte, só leitura, sem clonar, instalar nem rodar:
- `jakubkrehel/skills` `variant/SKILL.md` e `variant/picker.md`, inteiros.
- `Owl-Listener/designer-skills` `heuristic-evaluation`, `ux-writing` e `information-architecture` (`SKILL.md`), inteiros (49 linhas o último).
- Documentação oficial do Claude Code (`settings-reference` e `skills`), para a chave dos plugins e a precedência de nomes.

Três achados novos que mudam a instalação, antes das categorias:

1. **Os plugins `design:*` não vêm de plugin instalado, vêm da conta claude.ai.** O `enabledPlugins` do usuário só tem `superpowers@claude-plugins-official`. Em `~/.claude/plugins/synced/` estão `design`, `engineering`, `productivity` e `cowork-plugin-management` (lido do `manifest.json` local, marketplace `knowledge-work-plugins`). Pela documentação, cada plugin sincronizado carrega como `<name>@synced`. A chave do `enabledPlugins` é, portanto, `design@synced` etc. (formato abaixo).
2. **Uma skill pessoal vence a de projeto com o mesmo nome.** Existe `~/.claude/skills/prototype` (a do fluxo Matt Pocock). A documentação diz: "Enterprise over personal, and personal over project. With `deploy` in both `~/.claude/skills/` and the project's `.claude/skills/`, `/deploy` runs the personal one". Então `/prototype` na pasta do papel rodaria a skill errada. **A cópia do Emil passa a se chamar `emil-prototype`.** Nenhum outro nome da suíte colide com `~/.claude/skills/` (conferi a lista).
3. **O `@synced` e as skills pessoais continuam carregando** se nada for feito: `superpowers:brainstorming` ("MUST use before any creative work") e `using-superpowers` seriam disparadas em todo recruta. Entram no `settings.json` abaixo.

---

## Categorias que mudam

### Explorar caminhos realmente diferentes e escolher um (muda)

Leitura de `variant` (inteiro) e decisão:
- `variant` pede **um eixo principal** entre cinco que ela mesma lista: estrutura, densidade, ênfase (onde vai a cor cheia), tipografia e voz. Três deles (ênfase, tipografia, voz) são aparência. A skill diz "Different answers, not different tints", mas as variantes dela são respostas diferentes **dentro do mesmo desenho**: a tela e o conteúdo continuam os mesmos.
- A régua do Gustavo é "reinventar a forma em vez de restilizar". O teste do `parallel-concepts` ("o leitor faz algo diferente?") mira a forma; o de `variant` mira a variação ordenada de um eixo. Para três formas de cidade o `parallel-concepts` é o certo (inferência).
- `variant` exige o piso de `better-interface` (onze gatilhos) e as `better-*` instaladas para os eixos. Isso arrasta cinco skills que a suíte não tem.
- O seletor de `variant` (`picker.md`) é mais completo (parâmetro `?__variant=` na URL, setas, `H` esconde, container query), mas o `emil-prototype` já traz um seletor (PICKER.md, ficha) e a amostra é uma página só.
- **Fica a combinação:** `parallel-concepts` decide **o que varia** (autônoma); `emil-prototype` põe os conceitos **atrás do seletor** (manual). **`variant` sai.** Ideias dela que valem na régua: "dar a cada variante conteúdo real, não Lorem ipsum e três linhas", "nunca marcar favorita", "variantes de mesma fidelidade". Vão para `regua-da-cidade` (regra de comparação), não como skill copiada.
- Gatilho em conflito: resolvido. `parallel-concepts` autônoma; `emil-prototype` manual, chamada com `/emil-prototype …` no começo da mensagem do maestro (decisão 1 do julgamento).

### Julgar uma tela já pronta, olhando a captura (muda)

- `heuristic-evaluation` lida inteira: dez heurísticas de Nielsen, "walk through as a new user / experienced user", fluxos de tarefa, severidade 0 a 4, "Multiple evaluators find more issues". É avaliação de **usabilidade de tarefas**. Um diagrama que se lê não tem tarefa. **Sai**, definitivo.
- Entra `regua-da-cidade` no UX revisor (ver categoria nova). As seis `critique-*` ficam como na v1.
- Conflito novo: `regua-da-cidade` x `critique-*` disparam juntas ao rever a captura da cidade. É o desenho (a régua específica + o julgamento geral). A `description` da `regua-da-cidade` manda usar as duas e lista o que cada uma cobre.

### Nomes e textos da interface (muda)

- `ux-writing` lida inteira: categorias genéricas de microcopy (botão, erro, vazio, confirmação, onboarding, CTA), voz e tom, "Write copy before designing the UI", "Test copy with real users". Nada sobre **nomear peças de um sistema**. Duplica `better-writing`. **Sai**, definitivo.
- `information-architecture` lida inteira. Útil: "Taxonomy & Labeling" (nomes consistentes, "avoid internal jargon"), "Scent: navigation labels and category names accurately predict what's inside", "Wayfinding", "Depth vs breadth: 3 levels max", "Common Mistakes" (estruturar pela organização interna e não pelas tarefas). Inútil aqui: card sort, tree test, first-click, o passo "Research" e "Validate", e "category names derived from user vocabulary". **Entra no Tech lead, com cortes** (alterações abaixo).
- `better-writing` sai do Tech lead (evita a briga de "rótulos" com `information-architecture`). Fica no UI engineer e no UX revisor.

### Acabamento e movimento (muda)

- `animate` sai do UI engineer (primeira amostra estática; sem GSAP). `animation-performance` sai do QA por ora (sem animação a medir). As duas voltam juntas se a cidade ganhar movimento. Nada mais muda na categoria.

### Acessibilidade, teclado e contraste (muda)

- `better-accessibility` fica no QA. O `check_contrast.py` do tastemaker deixa de ser "ferramenta solta" e passa a viver dentro de `medidas-da-peca`.
- `better-colors` sai do QA: dispararia no mesmo momento de `medidas-da-peca` ("contraste"). Fica só no UI engineer, para construir a paleta.
- `better-accessibility` diz "Medição de contraste fica com `better-colors`". Na cópia essa frase aponta para `medidas-da-peca`.

### Quebrar a peça: dados extremos, larguras e estados (muda)

- `break-ui` fica no QA, alterada para rodar só numa cópia. As larguras (320, 768, 1280, 1920) e o zoom passam a ser medidos por `medidas-da-peca`; `break-ui` fica com nomes longos, zero itens, RTL e escuro.

### Estudar e copiar uma referência (muda)

- Decisão 4: o tastemaker não entra como skill. As referências elogiadas e recusadas do Gustavo viram imagens e texto dentro de `regua-da-cidade/referencias/`.

### Categoria nova: Régua e medição próprias

- **o que resolve:** o que nenhuma skill de fora cobre: a régua do Gustavo escrita como regras verificáveis, e as medições por script (cruzamentos de linhas, distância entre itens, links, peso, tempo de carga, contraste).
- **skills:** `regua-da-cidade` e `medidas-da-peca`, nossas, descritas abaixo.
- **sobreposições:** com as `critique-*` (julgar a captura) e `better-accessibility` (acessibilidade). Delimitado nos gatilhos abaixo.
- **fica:** as duas.
- **sai:** nada.
- **gatilhos em conflito:** `regua-da-cidade` x `critique-visual-hierarchy`, `-composition` e `-information-density`: mesma situação (olhar a captura da cidade). Desempate: a `description` da régua é específica (system design, cidade, diagrama do hub) e diz "rode junto das críticas gerais"; as críticas gerais valem para as telas do portal. `medidas-da-peca` x `better-accessibility`: a segunda diz o que falha (critério WCAG), a primeira mede; a cópia da segunda aponta para a primeira.
- **riscos:** os scripts são nossos, escritos e lidos pelo maestro antes do uso. Sem rede, exceto `localhost`. Escrevem só em `qa/` da pasta do QA. O único script de fora é `check_contrast.py` (tastemaker), cuja ficha o descreve como "pura computação, sem rede, sem escrita"; o maestro relê antes de copiar.
- **papéis:** `regua-da-cidade`: UI engineer, UX revisor, Tech lead, QA tester. `medidas-da-peca`: QA tester.
- **serve de régua?** sim. É a régua.

---

## Efeitos nas outras categorias (resumo)

- Compor a tela pelo modo como o olho agrupa: sem mudança (cinco leis, `visual-hierarchy`, `spacing-system` no UI engineer).
- Construir uma página inteira: `web-design-engineer` fica, com as edições abaixo.
- Cor, letra e medidas: `better-colors`, `better-typography` e `spacing-system` no UI engineer. `better-colors` deixa o QA.
- Páginas de venda e marketing, e o resto de "Fora da suíte": sem mudança. `variant`, `heuristic-evaluation` e `ux-writing` entram em "Fora".

---

## Suíte proposta por papel

Nomes de pasta em `.claude/skills/` do papel. (cop.) = copiada de fora, (nossa) = a escrever.

### UI engineer: 14

1. web-design-engineer (cop., editada)
2. parallel-concepts (cop.)
3. emil-prototype (cop., renomeada, manual)
4. law-of-proximity (cop.)
5. law-of-common-region (cop.)
6. law-of-continuity (cop.)
7. law-of-figure-ground (cop.)
8. law-of-similarity (cop.)
9. visual-hierarchy (cop.)
10. spacing-system (cop.)
11. better-colors (cop.)
12. better-typography (cop.)
13. better-writing (cop.)
14. regua-da-cidade (nossa): o UI engineer a lê antes de construir

### UX revisor: 8

1. critique-visual-hierarchy (cop.)
2. critique-composition (cop.)
3. critique-information-density (cop.)
4. critique-affordance (cop.)
5. critique-color (cop.)
6. critique-typography (cop.)
7. better-writing (cop.)
8. regua-da-cidade (nossa)

Imagens de referência (elogiadas e recusadas) ficam em `regua-da-cidade/referencias/`, não são skill.

### Tech lead: 3

1. concept-selection (cop.)
2. information-architecture (cop., editada)
3. regua-da-cidade (nossa)

### QA tester: 4

1. better-accessibility (cop., editada)
2. break-ui (cop., editada)
3. regua-da-cidade (nossa)
4. medidas-da-peca (nossa)

**Totais: UI engineer 14, UX revisor 8, Tech lead 3, QA tester 4. Skills distintas: 25** (23 copiadas, 2 nossas).

Gatilhos próximos dentro de um mesmo papel, conferidos:
- UI engineer: as cinco leis (o Owl as desempata no texto, fica); `parallel-concepts` (autônoma) x `emil-prototype` (manual): sem disputa.
- UX revisor: seis críticas + `regua-da-cidade`: desempate acima; `better-writing` fala de texto, não de captura.
- Tech lead: `information-architecture` ("rótulos") sem `better-writing`: sem disputa.
- QA: `better-accessibility` (critério) x `medidas-da-peca` (medida) x `break-ui` (dados extremos): complementares; zoom e 320 px aparecem nas três. A `description` de `medidas-da-peca` assume larguras e zoom; a de `break-ui` fica com dados.

---

## `.claude/settings.json` da pasta de cada papel

Arquivo `C:\Projetos\equipe-design\<papel>\.claude\settings.json`:

```json
{
  "enabledPlugins": {
    "design@synced": false,
    "engineering@synced": false,
    "productivity@synced": false,
    "cowork-plugin-management@synced": false,
    "superpowers@claude-plugins-official": false
  }
}
```

Citações da documentação oficial (`https://code.claude.com/docs/en/settings-reference`, seção `enabledPlugins`; lida em 2026-10-15):

- "Turn individual plugins on or off, keyed by `plugin-name@marketplace-name`. A plugin with no entry at any scope falls back to its `defaultEnabled` value." Tipo: "object mapping `plugin-name@marketplace-name` to a Boolean". Escopo: "Any file".
- Exemplo oficial: `"experimental-features@personal": false`.
- Precedência: "Project settings take precedence over user settings, so setting a plugin to `false` in `~/.claude/settings.json` doesn't disable a plugin that the project's `.claude/settings.json` enables." O sentido inverso (projeto `false` vence usuário `true`) decorre da ordem do diagrama de precedência da mesma página: "highest first: managed settings, command line, project local, shared project, user. A key set at a higher level overrides the same key set lower down."
- Plugins sincronizados (`syncClaudeAiPlugins`): "loads each one as `<name>@synced`" e "To turn off one synced plugin rather than all of them, set `"<name>@synced": false` in `enabledPlugins`."
- Nomes `design`, `engineering`, `productivity`, `cowork-plugin-management`: do `manifest.json` de `~/.claude/plugins/synced/` da máquina (lido, não da documentação).

O que não confirmei (sem rodar nada):
- Que `design@synced` com `false` num `.claude/settings.json` de projeto desliga de fato o plugin sincronizado (a documentação dá a regra geral e o `<name>@synced`, não esse caso exato). O maestro confere no recruta, como o plano já prevê, olhando se `design:design-critique` aparece na lista de skills.
- Alternativa documentada se não funcionar: `"syncClaudeAiPlugins": false` em `.claude/settings.local.json`. Escopo oficial: "User, local, or managed ... A repository can't turn it off for you", então não vale no `settings.json` compartilhado, só no `.local`. Mesmo para as skills sincronizadas (`anthropic-skills:*`): `"syncClaudeAiSkills": false`, também só em user, local ou managed.
- As ~110 skills de `~/.claude/skills/` (gsd-*, maestri, matt etc.) continuam carregando. `skillOverrides` (`"off"`, qualquer arquivo) as esconderia, mas "Overrides don't apply to plugin skills". Decisão do maestro: esconder só as que disparam em design, se algum teste mostrar disputa (ponto em aberto).

---

## As duas skills nossas

### regua-da-cidade

- **pasta:** `regua-da-cidade/` com `SKILL.md`, `regras.md`, `referencias/` e `como-julgar.md`. Texto só, sem script.
- **invocação:** autônoma.
- **description (rascunho):** "Judge or build the system-design city diagram of the Context Hub against Gustavo's six rules: lines never cross, top-down overview, minimum distance between items, names that say what each item references, each item's role makes sense in a city, and reinvent the form instead of restyling. Use when building, reviewing, comparing or scoring any version of the city diagram or a capture of it. Run together with the general critiques; for portal screens other than the city, do not use."
- **o que contém:**
  1. `SKILL.md`: quando entra; ordem de uso por papel (o UI engineer lê antes de construir; o UX revisor aplica sobre a captura; o Tech lead aplica R4, R5 e R6 contra o texto do hub; o QA confere o que `medidas-da-peca` mede); formato da resposta: por regra "passa / falha / não verificado", evidência (número ou captura) e conserto; nota por dimensão, que é a porta pedida em `orquestracao.md`.
  2. `regras.md`, as seis regras como regras verificáveis. Cada uma com enunciado, como verificar (olho ou `medidas-da-peca`) e limiar. Os **limiares são minha proposta, o Gustavo confirma**:
     - **R1, linhas sem se cruzar:** zero cruzamentos entre linhas de ligação; exceção só em ponto de encontro marcado (estação de baldeação) (inferência). Medido por `medidas-da-peca/cruzamentos`.
     - **R2, vista mais de cima:** na escala de visão geral, só zonas e ligações principais legíveis; o teste de olho apertado (captura reduzida e borrada) ainda mostra os agrupamentos; limite de rótulos visíveis na visão geral (número a fixar). Medido por captura reduzida e contagem de rótulos.
     - **R3, distância entre os itens:** folga mínima entre caixas de itens vizinhos (a fixar, em múltiplo da altura do rótulo); espaço dentro de um grupo menor que entre grupos (razão mínima 1,5, a confirmar). Medido por `medidas-da-peca/distancias`.
     - **R4, nomes que digam o que o item referencia:** todo rótulo é o nome da peça no texto do hub ou no glossário; nenhum código interno solto (T2, C3 etc.); nenhum nome inventado só para a metáfora. Medido por lista de rótulos extraída da peça contra o glossário, e conferida por pessoa.
     - **R5, uma cidade em que o papel de cada item faça sentido:** tabela item → papel no hub → equivalente na cidade, escrita pelo autor da peça e conferida pelo Tech lead contra o texto do hub; nenhum item cuja função na cidade contradiga a do hub.
     - **R6, reinventar a forma:** o conceito muda o que o leitor faz ou como lê, não só cor, fonte e arredondamento. Teste de `parallel-concepts`: trocar o visual pelo do conceito anterior e ver se ainda é outro desenho. Contra a lista de formas já recusadas.
     - Regras de comparação (ideias do `variant`, só como regra): conceitos com a mesma fidelidade, conteúdo real do hub, sem marcar favorito.
  3. `referencias/`: elogiadas, "mapa de metrô" e "maré"; recusadas, "laudo denso" e "cidade radial v2 restilizada" (decisão do maestro; da memória do Gustavo: simplificar é comunicar melhor, não cortar; reinventar é mudar a forma). **As imagens ainda não estão na pasta**; o maestro deposita e anota por que cada uma foi elogiada ou recusada. Não inventei nada sobre elas.
  4. `como-julgar.md`: roteiro de nota por dimensão (as seis regras mais as dimensões das `critique-*`) e o formato da lista de consertos para a carta ao Gustavo.
- **o que NÃO contém:** gosto estético genérico (fica nas `critique-*`), animação (a amostra é estática), movimento de dados.
- **riscos:** nenhum (texto). O risco é de **limiar errado**; por isso cada limiar sai marcado como proposto.

### medidas-da-peca

- **pasta:** `medidas-da-peca/` com `SKILL.md`, `medir.html`, `medir.js`, `rodar.ps1` (ou `.sh`), `links.mjs`, `contraste/check_contrast.py` e `LEIA-ME.md` de origem. Escritos e lidos por nós antes do uso.
- **invocação:** autônoma.
- **description (rascunho):** "Measure a built HTML/SVG piece with scripts instead of judging by eye: count crossings between lines, minimum distance between items, rendered text contrast, load size and time, broken links, keyboard focus order and missing names, at several screen widths. Use when testing a page or the city diagram, when a review needs numbers, or when an accessibility check asks to measure contrast. Report only; never edit the piece."
- **o que contém:**
  1. `medir.html` + `medir.js`: página que carrega a peça num iframe do mesmo servidor local e roda as medições no navegador, devolvendo JSON num `<pre id="medidas">`. Roda no Edge sem cabeça (`msedge --headless --dump-dom`, já usado na frente, sem `npm`), com perfil temporário próprio; encerra só o processo do próprio perfil. Medições:
     - **cruzamentos:** amostra cada traço de ligação (`getPointAtLength`) e conta interseções entre pares que não compartilham ponta; lista os pares.
     - **distâncias:** `getBoundingClientRect` de cada item marcado (`data-item`), menor folga entre vizinhos e razão dentro do grupo x entre grupos.
     - **rótulos:** lista todos os textos para conferir contra o glossário (R4).
     - **teclado e foco:** lista os focáveis na ordem, os sem nome acessível, `tabindex` maior que zero, e se cada um muda de aparência ao receber foco (via `el.focus()`).
     - **contraste renderizado:** para cada texto, cor computada contra o fundo efetivo; cálculo igual ao do `check_contrast.py` (conferir a equivalência).
     - **peso e tempo:** bytes por tipo e tempo de carga pela Performance API da página.
  2. `rodar`: roda `medir.html` em 320, 768, 1280 e 1920 px de largura, grava o JSON e uma captura por largura em `qa/` (só no monitor principal; nada de mouse nem teclado, conforme a memória do projeto).
  3. `links.mjs`: Node sem pacote; lê os `href` e `src` da peça, confere se cada alvo local existe (arquivo ou âncora) pelo servidor local. Links externos só são listados, não acessados.
  4. `contraste/check_contrast.py`: **cópia** de `codeswithroh/tastemaker`, `skills/tastemaker/scripts/check_contrast.py`, commit `792a28a820ec4e9159ef8621c21a6c88528bbf2e`, MIT (copyright 2026 codeswithroh; LICENSE junto). Sem alterações no código. Antes de copiar, o maestro relê o script inteiro; a ficha o descreve como cálculo puro, sem rede e sem escrita, e tem `--palette` e `--matrix`. Requer Python 3 (a conferir na máquina).
  5. `LEIA-ME.md`: origem, regras de uso: saída só em `qa/`, sem rede (só `localhost`), sem tocar na peça, matar só o `msedge` do próprio perfil.
- **o que NÃO contém:** teste de usabilidade, gosto, geração de relatório com nota (isso é da `regua-da-cidade`).
- **riscos:** escrita só em `qa/`; `rodar` abre o Edge; sem `npx`, sem rede, sem memória fora do projeto. As amostras de pontos para cruzamento são aproximadas (curvas), então o script reporta "suspeita" a confirmar por olho (inferência).

---

## Skills copiadas: origem, alterações, invocação

Origem = repositório, caminho, commit. **Os commits são o HEAD de cada repositório em 2026-10-15**, lidos com `git ls-remote <url> HEAD` (só consulta de referência, sem clonar), porque a API do GitHub devolveu "rate limit exceeded" (HTTP 403, sem token). O de `jakubkrehel/skills` bate com o commit anotado na ficha dele (`4c66b1fa…`). Quando o maestro copiar, deve fixar de novo e anotar no `LEIA-ME.md` da skill. Licença: MIT em todos (fichas); levar o `LICENSE` do repositório para dentro de cada pasta copiada (copyrights: Elaya/ConardLi "2026", MC Dean, Emil Kowalski, Jakub Krehel, codeswithroh).

Commits (HEAD em 2026-10-15):
- ConardLi/garden-skills: `7a6d5a72e4f44bb4cc0c23c01b3d97205c723b68`
- Owl-Listener/designer-skills: `9a6930cf84a822eb458624bd11c61aac5bbdf224`
- emilkowalski/skills: `2d228630ba1446365f614a108cb8252f1feda202`
- jakubkrehel/skills: `4c66b1fa86e9ab70187b43d7da9b6fdb29f2ef63`
- codeswithroh/tastemaker: `792a28a820ec4e9159ef8621c21a6c88528bbf2e`

| # | Pasta na cópia | Origem (repo : caminho) | Alterações na cópia | Invocação |
|---|---|---|---|---|
| 1 | web-design-engineer | garden-skills : `skills/web-design-engineer` (SKILL.md e `references/`) | (a) Os três checkpoints (SKILL.md, "Checkpoint 1/2/3", linhas ~148, 160 e 166, e a linha "Honor checkpoints", ~473) viram: gravar a decisão tomada em `decisoes.md` e seguir; quem decide a direção é a porta (Tech lead e UX revisor) e depois o Gustavo na carta. (b) Sai a seção "Design Direction Advisor" (~linhas 195 a 230), a referência `design-directions.md` e a pasta `references/style-recipes/` (restilizar). (c) "Step 0": acrescentar que nada do hub é pesquisado na web e que o passo não se aplica a nomes do hub. (d) Meio: trocar a parte de React e Babel por "HTML, CSS, SVG e JavaScript puro, sem framework, sem build, sem CDN, servido localmente"; apagar `advanced-patterns.md` na parte React/CDN ou o arquivo todo se não sobrar nada útil (a decidir ao ler). (e) Apagar `browser-acceptance.md` da cópia (a aceitação é do QA). (f) Na `description`, tirar "slide decks", "design critique" e "browser acceptance / QA" para não disparar fora do ofício de construir. | autônoma |
| 2 | parallel-concepts | Owl : `prototyping-testing/skills/parallel-concepts` | nenhuma | autônoma |
| 3 | emil-prototype | emilkowalski/skills : `skills/prototype` (SKILL.md e `PICKER.md`) | (a) `name` e pasta mudam de `prototype` para `emil-prototype` (colisão com a skill pessoal `prototype`, ver achado 2). (b) A "Hard Rule 5" (apagar a superfície depois da escolha sem perguntar) vira "nunca apagar amostra sem pedido". (c) Rota de servidor de desenvolvimento sai: só um HTML único em `amostras/`. (d) Mantém `disable-model-invocation: true`. Não li o corpo (a ficha o resume); ler inteiro ao copiar. | **manual** (`/emil-prototype …`) |
| 4 | law-of-proximity | Owl : `ui-design/skills/law-of-proximity` | nenhuma | autônoma |
| 5 | law-of-common-region | Owl : `ui-design/skills/law-of-common-region` | nenhuma | autônoma |
| 6 | law-of-continuity | Owl : `ui-design/skills/law-of-continuity` | nenhuma | autônoma |
| 7 | law-of-figure-ground | Owl : `ui-design/skills/law-of-figure-ground` | nenhuma | autônoma |
| 8 | law-of-similarity | Owl : `ui-design/skills/law-of-similarity` | nenhuma | autônoma |
| 9 | visual-hierarchy | Owl : `ui-design/skills/visual-hierarchy` | nenhuma | autônoma |
| 10 | spacing-system | Owl : `ui-design/skills/spacing-system` | nenhuma | autônoma |
| 11 | better-colors | jakubkrehel/skills : `skills/better-colors` (e `references/`) | nenhuma. A parte que diz "medir o par renderizado" fica; a medição é feita por `medidas-da-peca` (no QA, não neste papel). Não leva o `agents/openai.yaml` (Codex). | autônoma |
| 12 | better-typography | jakubkrehel/skills : `skills/better-typography` | nenhuma; sem `agents/openai.yaml` | autônoma |
| 13 | better-writing | jakubkrehel/skills : `skills/better-writing` | nenhuma; sem `agents/openai.yaml`. Vai ao UI engineer e ao UX revisor (duas cópias iguais). | autônoma |
| 14 | critique-visual-hierarchy | Owl : `visual-critique/skills/critique-visual-hierarchy` | nenhuma | autônoma |
| 15 | critique-composition | Owl : `visual-critique/skills/critique-composition` | nenhuma | autônoma |
| 16 | critique-information-density | Owl : `visual-critique/skills/critique-information-density` | nenhuma | autônoma |
| 17 | critique-affordance | Owl : `visual-critique/skills/critique-affordance` | nenhuma | autônoma |
| 18 | critique-color | Owl : `visual-critique/skills/critique-color` | acrescentar uma linha: "as razões de contraste são estimativas; a medida vem de `medidas-da-peca`" | autônoma |
| 19 | critique-typography | Owl : `visual-critique/skills/critique-typography` | nenhuma | autônoma |
| 20 | concept-selection | Owl : `prototyping-testing/skills/concept-selection` | nenhuma | autônoma |
| 21 | information-architecture | Owl : `ux-strategy/skills/information-architecture` | Cortes: no "Process", os passos 2 "Research" e 4 "Validate" (card sort e tree test); nos "Best Practices", os itens de card sort, tree test e first-click; "Category names derived from user vocabulary" vira "derivados do vocabulário do hub (glossário e texto do hub)"; "Deliverables" ficam só "Sitemap" lido como mapa das peças e "Taxonomy & Labeling". Acrescentar no topo: "No laço não há usuários a testar; o leitor é quem olha a cidade; a fonte dos nomes é o texto do hub." | autônoma |
| 22 | better-accessibility | jakubkrehel/skills : `skills/better-accessibility` (e `references/`) | acrescentar: "No papel QA, relatar, não corrigir"; trocar a frase "contrast measurement belongs to `better-colors`" por "... belongs to `medidas-da-peca`"; sem `agents/openai.yaml` | autônoma |
| 23 | break-ui | emilkowalski/skills : `skills/break-ui` (e `CATALOG.md`) | rodar só numa cópia da peça em `qa/copia/`; fixture e toggle nunca na amostra aprovada; manter "para antes de corrigir". Não li o corpo (a ficha o resume); ler inteiro ao copiar. | autônoma (sem a flag, conferido no frontmatter) |

Contagem de cópias por papel: UI engineer 13 (nº 1 a 13), UX revisor 7 (14 a 19 mais `better-writing`), Tech lead 2 (20, 21), QA 2 (22, 23). Cada pasta copiada leva `LEIA-ME.md` com origem, commit e lista das alterações acima.

## Pontos em aberto desta volta

1. **Limiares da `regua-da-cidade`:** folga mínima, razão de grupo, limite de rótulos na visão geral. Propostos por mim; o Gustavo ou o maestro confirmam.
2. **Imagens de referência:** elogiadas e recusadas ainda não estão em arquivo que eu tenha visto. O maestro deposita em `regua-da-cidade/referencias/`.
3. **`design@synced: false` num `.claude/settings.json`:** regra geral citada, caso exato não confirmado. Conferir olhando as skills do recruta.
4. **Skills pessoais:** só `prototype` colide por nome (resolvido pela renomeação). Se algum gsd-*, `video-generator` ou `grilling` disparar em tarefa de design, esconder por `skillOverrides` na pasta do papel.
5. **Corpos não lidos:** `emil-prototype`, `break-ui` e as referências de `web-design-engineer` seguem com base na ficha; ler inteiros ao copiar. A parte React de `advanced-patterns.md` pode ou não sobrar.
6. **Python no QA:** `check_contrast.py` pede Python 3; conferir na máquina, ou portar a conta para JS dentro de `medir.js` (inferência: a conta de contraste WCAG é curta).
