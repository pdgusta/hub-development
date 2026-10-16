# Briefing: System design como cidade 2.5D (amostra)

Pedido do Gustavo (2026-10-14, recusa da "planta técnica", texto em
`portal/caixa/2026-10-14-190808-aprovacao-carta-system-design-planta-*.md`): "você só mudou o estilo, mas o
diagrama está literalmente o mesmo. Quero que reimagine como se fosse uma vista de cima de uma cidade (2.5D).
Utilize cores, separação lógica de ideias, comunicação visual clara com pouco texto. Não polua visualmente,
quero visual clean. Faça bom uso de logos/ícones e agrupamento por cores, ou áreas da cidade."

Saída: `.scratch/context-hub/amostras/system-design-cidade.html` (um arquivo, autônomo).
Conferência: `.scratch/context-hub/portal/conferencia/system-design-cidade/`.
Não tocar: `system-design.html`, `amostras/system-design-planta.html`, `portal/cartas.json`, `portal/caixa/`.

## Regras fixas

1. **Conteúdo igual, forma nova.** Os fatos são os do desenho atual: a fonte de verdade do conteúdo é o modelo
   `ROOMS`/`CARDS`/`EDGES` + cabeçalho + legenda de `amostras/system-design-planta.html` (que tem paridade
   124/124 com o `system-design.html`; lista em `portal/conferencia/system-design-amostra/paridade.json`,
   `textos_atual`). Disposição, hierarquia e agrupamento são novos: **nada da grade de cards em colunas**.
   No mapa fica só o essencial (nome + logo/ícone, no máximo um selo curto); o resto (subtítulos, caminhos,
   regras) vai para a **ficha ao clicar**. Todo texto dos 124 tem de existir no mapa, na ficha, no título ou na
   legenda (prova em `paridade.json`, mesmo formato da amostra anterior).
2. **Navegação de canvas igual à pedida:** tela inteira, sem rolagem; botão direito arrasta; Ctrl+roda dá zoom no
   ponto do cursor; Shift+roda anda na horizontal; roda sozinha não faz nada de estranho (pode andar na vertical);
   só os elementos clicáveis (prédios, placas) abrem a ficha; Esc fecha; botão "enquadrar". O código de navegação
   e de ficha da planta pode ser reaproveitado (é encanamento, não forma).
3. **Nada de rede:** fontes em `@font-face` com `data:` base64 (baixe woff2 latin de `@fontsource`/
   `@fontsource-variable` no cdn.jsdelivr.net com versão exata só na construção; anote família e versão num
   comentário). Logos como SVG inline desenhados (Obsidian, CouchDB, Tailscale, GitHub, Claude, Codex/OpenAI,
   Copilot, Docker, MCP, Markdown). Funciona em `file:` e no iframe `sandbox="allow-scripts"` do portal.
4. Nunca código interno sem palavras; pt-BR; nada de nome de pessoa além de "Gustavo" que já está no desenho.

## Conceito: uma ilha-cidade vista de cima, em isométrico (2:1)

A máquina "par 1 · notebook ARMIS · C:\context-hub" é **uma ilha**. A "Par 2 · máquina pessoal" é **a ilha
gêmea**, menor, do outro lado de um canal. O GitHub é um **farol/arquivo em alto-mar**. Água em volta dá o
respiro (clean). Cada grupo de ideias é um **bairro** com chão de uma cor; prédios em blocos isométricos
extrudados (topo claro, duas faces em tons do mesmo matiz, sombra suave), logo/ícone no telhado ou numa
bandeira. Ruas = ligações; nome da rua = a palavra da ligação.

Fluxo de leitura de oeste para leste, como a cidade é atravessada:

| Bairro (chão) | Papel na legenda | Prédios (ícone/logo) | Metáfora |
|---|---|---|---|
| **Quem chega** (areia) | Externo | Gustavo (casa, pessoa), Agentes (garagem com Claude/Codex/Copilot no telhado), Clientes (lote cercado: Docker + Claude; selo "aberto" como cone de obra) | moradores e visitantes |
| **Muralha e portões** (lilás) | Entrada | Obsidian (portão com bandeira; selo "pode fechar"), Sessão (portão com terminal; "+ Copilot"), MCP só leitura (catraca/guichê) | o único jeito de entrar |
| **Centro cívico** (azul ardósia) | Contrato / Serviço / Proteção | Contrato (prefeitura com AGENTS.md), MCP · fork es617 (central dos correios), Guarda de versão (guarita escura com cadeado na porta do banco), Busca (canteiro de obras com guindaste, tracejado, "aberto"), Divergência (posto de alarme com sirene) | onde as regras e os serviços moram |
| **Bairro dos dados** (verde-água) | Dados / Serviço | CouchDB (o cofre/torre mais alta da cidade, logo no topo), Vista Markdown (biblioteca/praça), Sincronizador (estação de bombas entre os dois, "sempre ligado"), Vigia · 5 min (farol de vigia, "por máquina"), "se piorar" e "mod fixo" (dois quiosques ao pé do vigia) | a verdade e quem a guarda |
| **Distrito do Acervo do Maestro** (ocre, ao norte) | Acervo / Proteção / Externo | Maestri, Peças (depósito em camadas), Guarda do acervo (guarita escura com escudo), Registro de uso, maestro-* (oficina, peça de quebra-cabeça), Propostas (caixa de correio) | a oficina que equipa os agentes; placa "C:\context-hub\agents\ · replica para as 2 máquinas" |
| **Canal, ponte e mar** (azul) | Rede | Ponte da tailnet entre as ilhas (logo Tailscale na torre da ponte; "cada uma empurra"), Par 2 (ilha gêmea com mini CouchDB), GitHub · cópia (farol em alto-mar; rota pontilhada "diário"; "commit + push") | o que liga as máquinas |
| **Placas da ponte** | Regras do sync | três placas de trânsito clicáveis: "outra máquina desligada", "colisão", "o que vai ao banco"; o texto delas vai para a ficha | as regras na entrada da ponte |

Ligações especiais: "fronteira de gravação" = muro baixo/linha pintada cercando a praça do banco (o fork e a
guarda de versão estão nela); "junction · todo harness" = **túnel** tracejado do Acervo até a garagem dos Agentes;
"contratos-opção" = avenida do Acervo até a prefeitura; "aviso" (violeta, revisão) = linha de sinal da
Divergência até a Sessão; "agente no disco?" e "Desktop grava?" = ruas em obras (terracota tracejada, abertas).

Cores: um matiz por bairro, saturação baixa no chão e média nos telhados; terracota só para o que está "aberto";
escuro (quase preto) só para os prédios de Proteção, em qualquer bairro (é o que a legenda já dizia). Fundo água
clara, ruas brancas/creme. Fonte nova e diferente das anteriores (nem Barlow Condensed nem Architects Daughter):
uma geométrica arredondada e limpa (por exemplo Sora ou Outfit) para nomes; peso forte só no nome do bairro.

Pouco texto no mapa: nome do bairro grande (rótulo pintado no chão, em perspectiva ou em placa), nome do prédio
pequeno em etiqueta, palavra da rua no meio da rua. Título em cartela num canto fixo: "Context hub ·
arquitetura", o subtítulo inteiro e o carimbo "2026-10-13 · sync e divergência resolvidos". Legenda como
chave de mapa (cor do bairro + tipo de rua), compacta, fixa num canto.

Toque vivo e discreto: pontinhos andando nas ruas de fluxo, água com reflexo leve; `prefers-reduced-motion`
desliga. O painel do Maestri congela animação: o desenho tem de ficar bonito parado.

## Ajustes do Prumo (parecer `portal/revisao-direcao-cidade.md`) — valem por cima do que está acima

- **Sem muralha que fecha a cidade.** "Portas" é um bairro de entradas (portões soltos, praça de chegada), não um
  muro com "único jeito de entrar": as rotas abertas "agente no disco?" e "Desktop grava?" seguem direto para a
  Vista Markdown, por fora dos portões. Não sugerir proibição que o desenho não tem.
- **"fronteira de gravação" cerca só o caminho fork → guarda de versão → CouchDB** (o caminho de gravação dos
  agentes); não pode parecer que toda edição Markdown passa por ali (Obsidian → Vista → Sincronizador → CouchDB
  segue por fora).
- **Par 2 é par, não satélite:** ilha gêmea do mesmo peso visual possível (pode ser menor por espaço, mas sem
  hierarquia de "subúrbio"); a ponte "cada uma empurra" é simétrica. GitHub é **só cópia** (rota "diário" saindo da
  Vista Markdown), nunca centro do sync.
- **Túnel = junction LOCAL** maestro-* → Agentes, dentro da ilha, visualmente distinto da tailnet (outra cor/traço).
  O Acervo **replica para as duas máquinas**: placa do distrito diz isso.
- **Placas = regras do sistema, não condição de travessia:** um quadro de regras perto da ponte (não um pedágio):
  máquina desligada só informa e não diverge; colisão de texto segura só a nota; limites na ficha.
- **Distinção além da cor:** cada papel tem também forma/padrão (ex.: Proteção = guarita escura com escudo/cadeado;
  Serviço = prédio com engrenagem/antena; Dados = cilindro/cofre; Entrada = arco de portão; aberto = tracejado +
  cone). Tipos de rua por traço (contínuo, tracejado, pontilhado), não só cor.
- **Estático primeiro:** sem pontinhos andando nem reflexo contínuo nesta amostra.
- **Teclado:** todo clicável é focável (Tab), Enter/Espaço abre a ficha, Esc fecha e devolve o foco, foco visível;
  ao focar algo fora da vista, a vista anda até ele.

## Critérios de aceite (provas na pasta de conferência)

- **Paridade estrutural** além dos 124 textos (`paridade.json`): todos os componentes (CARDS) presentes com o mesmo
  papel, selo/estado ("aberto", "pode fechar", "+ Copilot", "até 200 MiB", "sempre ligado", "por máquina",
  "commit + push") e subtítulos na ficha deles; todas as 30 arestas (EDGES) com mesma origem, destino, sentido
  (incluindo as de duplo sentido e o par CouchDB ↔ Par 2) e palavra; nenhuma rua sem aresta correspondente (sem
  fluxo inventado). Abrir todas as fichas por script e conferir o conteúdo de cada uma.
- **Forma realmente nova:** nenhuma coluna/grade de cartões; anotar no relatório o arranjo (bairros e posição).
- Fonte mínima efetiva no "enquadrar" **≥ 14 px** em 1280x800 (rótulos do mapa, não só a ficha).
- Fichas alcançáveis e completas depois de pan, de zoom e de "enquadrar"; teclado (Tab/Enter/Esc) testado.

- Capturas Edge headless com a rede bloqueada (`--host-resolver-rules="MAP * ~NOTFOUND, EXCLUDE 127.0.0.1"`):
  `file:` em 1600x900 e 1280x800; iframe sandbox (cópia do `teste-iframe.html` da amostra anterior apontando para
  a nova) nos dois tamanhos; uma com ficha aberta; uma com zoom.
- `paridade.json`: os 124 textos de `textos_atual` achados no mapa/ficha/título/legenda, 0 faltando.
- Interação (adaptar `teste-interacao.js` da amostra anterior): direito arrasta, Ctrl+roda zoom, Shift+roda
  horizontal, clique em prédio abre ficha, clique no chão não abre, Esc fecha, sem rolagem do documento; em `file:`
  e no iframe.
- Fonte mínima renderizada no estado "enquadrar" ≥ 13 px em 1280x800 (rótulos do mapa) — medir.
- `document.fonts`: todas as faces `loaded` com a rede bloqueada; zero pedidos externos.
- Olhar cada PNG antes de dizer que está pronto: nada sobreposto, nenhuma etiqueta cortada, ruas legíveis.

---

# v2 (pedido do Gustavo, 2026-10-14 ~20h33; texto em `portal/caixa/2026-10-14-203331-aprovacao-carta-system-design-cidade-*.md`)

"Esse piloto ta bom, só precisa desses ajustes." **Manter o estilo** (cores, prédios, logos, ficha que esmaece e
acende as ruas, navegação de canvas, fontes embutidas, regras do Prumo da v1). Saída nova:
`amostras/system-design-cidade-v2.html` (a v1 fica como está); provas em `conferencia/system-design-cidade-v2/`.

## 1. Disposição radial a partir do cofre (o principal)

Níveis pela distância no grafo das 30 ligações, a partir do CouchDB (calculado):

| Nível | Peças |
|---|---|
| 0 (centro) | CouchDB |
| 1 (anel em volta) | Sincronizador, Guarda de versão, Busca, Vigia · 5 min, Par 2 (do outro lado da ponte) |
| 2 | Vista Markdown (do Sincronizador), MCP · fork es617 (entre Guarda de versão e Busca, ligado aos dois), Divergência, se piorar, mod fixo (do Vigia) |
| 3 | Sessão, MCP só leitura (do fork), Obsidian, GitHub · cópia (da Vista), Clientes |
| 4 | Contrato, Agentes (da Sessão), Gustavo (do Obsidian) |
| 5+ | Acervo do Maestro inteiro, na periferia, ligado ao Contrato (contratos-opção) e por túnel aos Agentes |

Setores (sugestão; ajuste para zerar cruzamentos): leste = ponte para a ilha do Par 2 com o quadro de regras na
cabeceira; nordeste/norte = Sincronizador → Vista Markdown → (Obsidian → Gustavo) e GitHub no mar; noroeste =
Busca; oeste = Guarda de versão; entre os dois, o fork; sul = Vigia → Divergência, sino e mod fixo; oeste-sudoeste,
anel de fora = Sessão (vizinha do fork e da Divergência), com Contrato e Agentes atrás dela; Acervo como distrito da
periferia oeste. As duas ruas em obras para a Vista ("agente no disco?" e "Desktop grava?") correm pelo anel externo
sem cortar raios. O túnel (junction) pode passar POR BAIXO de ruas (é túnel: desenhar a entrada e a saída e o
trecho subterrâneo apagado) — é o único cruzamento permitido. **Prova: um script de interseção de segmentos sobre
as ruas desenhadas deve dar 0 cruzamentos** (fora o túnel), registrado em `paridade.json`.

## 2. Ângulo: vista bem mais de cima

Nada de losango a 45°. Chão quase de cima (eixos da tela; achatamento vertical leve, ~0,8–0,9), anéis como círculos
ou elipses suaves; cada prédio mostra o telhado e só uma face frontal curta (altura pequena). Leitura de mapa, não de
maquete diagonal.

## 3. Rótulos sem ambiguidade

Cada nome de prédio colado ao seu prédio, sempre na mesma posição (embaixo, centrado, numa etiqueta que encosta no
prédio). As palavras das ruas têm outro estilo (menores, na cor da rua, sem etiqueta de prédio, sobre a própria
rua, alinhadas a ela) para nunca parecerem nome de prédio. Nome de bairro grande e claro no chão do bairro. Nenhuma
etiqueta mais perto de outro prédio que do seu (prova por script: para cada etiqueta, o prédio mais próximo é o
dono).

## 4. A analogia é o principal

O prédio de cada peça é o que ela faz na cidade, e a ficha abre com **"Na cidade: … — porque …"** (uma linha):

| Peça | Na cidade | Porque |
|---|---|---|
| CouchDB | cofre do banco central, na praça do meio | guarda a verdade e cada revisão |
| Guarda de versão | porteiro do cofre | só deixa gravar quem traz a versão certa (base_rev); barra conflito |
| MCP · fork es617 | agência bancária (guichê) | onde os agentes leem, gravam e buscam |
| Busca | balcão de informações | indexa o cofre e responde a busca (aberto: em obras) |
| Sincronizador | correio | leva e traz cada arquivo entre a biblioteca e o cofre, sempre ligado |
| Vista Markdown | biblioteca pública | todo arquivo comum, em estante aberta |
| Obsidian | sala de leitura da biblioteca | onde se vê e edita; pode fechar |
| Gustavo | morador | edita pela sala de leitura |
| Vigia · 5 min | torre de vigia (guarda) | ronda a cada 5 min: sync, conflito, limite; uma por máquina |
| Divergência | quartel de bombeiros | conflito aberto há mais de 15 min dispara o aviso |
| se piorar | sino de alarme | toca se a situação piora |
| mod fixo | painel luminoso | o estado sempre à vista no Claude |
| Sessão | recepção (check-in) | o agente chega, recebe raiz, iniciativa e link |
| Contrato | prefeitura (as leis) | AGENTS.md e retomada valem para todos |
| MCP só leitura | terminal de consulta | quem vem de fora só consulta |
| Agentes | trabalhadores que chegam | Claude, Codex, Copilot |
| Clientes | visitantes de fora | sandbox lê; Desktop grava (aberto) |
| GitHub · cópia | cartório em outra ilha | guarda uma cópia por dia; não é o sync |
| Par 2 | cidade-irmã | outra máquina, com seu próprio cofre; a ponte da tailnet, cada uma empurra |
| Regras do sync | quadro de avisos da ponte | regras do sistema, não pedágio |
| Acervo do Maestro | escola de ofícios (periferia) | forma e equipa os agentes; replica para as 2 máquinas |
| Maestri | agência de papéis | papéis e lembrete ao abrir sessão |
| Peças | almoxarifado | papéis, receitas, contratos-opção |
| Guarda do acervo | fiscal | outro modelo verifica; mudança só com aval |
| Registro de uso | relógio de ponto | uso por máquina |
| maestro-* | portaria da escola | a porta maestro-acervo |
| Propostas | caixa de sugestões | Codex e Copilot propõem |
| junction · todo harness | túnel | leva o acervo até todos os agentes, dentro da máquina |

Se o prédio da v1 já servia, reaproveite e ajuste para ficar coerente com a tabela.

## Aceite (além do da v1, que continua todo valendo)
- 0 cruzamentos de ruas (fora o túnel), por script; níveis radiais respeitados (distância ao centro cresce com o
  nível), por script.
- Toda etiqueta mais perto do próprio prédio que de qualquer outro, por script.
- Toda ficha com a linha "Na cidade: … — porque …".
- Paridade 124/124, 28 componentes, 30 arestas; interação nos 4 cenários; mínimo ≥ 14 px efetivos em 1280x800.
