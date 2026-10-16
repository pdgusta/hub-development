# Mapa: context hub

Label: wayfinder:map

## Destination

O context hub construído e funcionando nas duas máquinas (notebook da ARMIS e máquina pessoal),
cumprindo os cinco critérios de aceite:

1. agentes (Claude Code, Codex, Copilot, dentro ou fora do Maestri), em qualquer máquina, acham o
   trecho certo sem ler tudo, pela camada de busca;
2. o que importa é gravado no lugar certo sem o Gustavo pedir, por um contrato file-first com zonas e
   checkpoint;
3. os `.md` continuam editáveis no Obsidian, a camada de busca está sempre acessível ao agente para
   buscar e gravar, e o agente também pode editar direto no disco, com sync para a outra máquina;
4. nada diverge em silêncio entre as máquinas;
5. existe proteção para a edição concorrente.

Rodadas que fixaram o destino e a fronteira: [Mapeamento da frente](mapeamento.md).

## Notes

- Domínio: `GLOSSARY.md` na raiz. Termos do mapa: context hub, máquina, camada de busca, edição
  concorrente, pasta não replicada, sincronizador, colisão real, divergência.
- Leia `exploracao/2026-09-28-context-hub.md` antes de propor desenho; as seções citadas nos tickets
  (§) são dela.
- Tickets `grilling`: skills "grilling" e "domain-modeling". Desde 2026-10-14, as perguntas vão para o portal do
  projeto (`portal/rodadas/`, formato da §4.1 de `portal/proposta.md`; aberto em http://127.0.0.1:8770/ pelo
  terminal "Portal"). A resposta chega à caixa (`portal/caixa/`) e o portal avisa o maestro sozinho. Regra (Gustavo,
  2026-10-14): decisão só no portal, com a explicação na rodada; rodada respondida nunca é reescrita, vira rodada
  nova; o terminal leva o resto e avisa em uma linha. Antes,
  de 2026-10-10 a 2026-10-14, as perguntas iam para a nota "Rodada atual" do Maestri.
  A resposta é absorvida no ticket antes de a nota ser reescrita. Um `grilling` que não fecha em conversa vira protótipo ou abre uma pesquisa.
- Tickets `prototype`: o protótipo é uma página que explica o que o ticket precisa comunicar, com
  diagramas, analogias e texto simples, terminando nas perguntas da rodada; não é simulador para
  estudar (Gustavo, 2026-10-03).
- Tickets `research`: protocolo da §10.4, só fonte primária, e o que não foi conferido fica marcado
  "não verificado". Pesquisa, teste ou varredura só rodam quando o Gustavo pede.
- Exceção ao "planejar, não fazer" (Q7): a construção acontece nos tickets que "Passagem para a
  construção" gera, fora deste mapa, e "Verificação dos cinco critérios nas duas máquinas" fecha o mapa.
- [`system-design.html`](system-design.html): o desenho do hub de bater o olho, aberto no portal
  "System design" do Maestri, ao lado do terminal (pedido do Gustavo, 2026-10-12). A página só muda
  quando um ticket que mexe no desenho é marcado como resolvido, com a data; rodada respondida não a
  muda (Gustavo, 2026-10-13). Os outros visuais mudam quando o maestro pedir.
  Em 2026-10-14, pelo portal (envio `0a4d5c78…`), o Gustavo pediu nova **forma** com o mesmo conteúdo: um
  canvas de tela inteira sem rolagem, arrastar com o botão direito, Ctrl+roda para zoom, Shift+roda para andar na
  horizontal, quase tudo estático e só os cards clicáveis, estilo totalmente diferente, ainda um diagrama de
  system design. Pedido ao Designer. A amostra "planta técnica em papel vegetal" foi **recusada** (envio
  `595b6457…`, 19:08): "você só mudou o estilo, mas o diagrama está literalmente o mesmo". Ele pede outra forma:
  uma vista de cima de uma cidade em 2.5D, com cores, separação lógica de ideias por áreas, pouco texto, visual
  clean, logos e ícones, e agrupamento por cor ou por bairro.
  A amostra "cidade 2.5D" foi **recusada como piloto bom** (envio `b46fdd40…`, 20:33). Ele mantém o estilo e pede:
  - disposição radial, com o banco no centro, as conexões principais (busca, vigia, sincronizador) em volta dele e
    as secundárias ligadas às principais;
  - linhas sem se cruzar;
  - vista mais de cima, menos diagonal;
  - nomes que deixem claro o que cada item referencia;
  - analogia de cidade em que o papel de cada item faça sentido.
  A amostra "cidade radial (v2)" foi **recusada** (envio `81bd19a5…`, 22:01): "tá tudo poluído… não dá pra bater
  o olho e entender. Precisa de distância entre os itens." **Pausado até a página Laços (ticket 55) ficar pronta (pronta em 2026-10-15; volta quando o Gustavo pedir):**
  ele quer um laço só para criar este system design, "tudo totalmente diferente, porém com a mesma ideia de cidade e
  analogia cada um com seu papel", com um agente muito bom em design e demonstração visual de system design e
  diagramas, junto com um muito bom em UI e UX (poluição visual, espaço concorrente, disposição de itens, divisão e
  separação lógica). O detalhe será conversado depois da página Laços.
- Visuais (o `system-design.html`, o `mapeamento.html` e os que vierem) são feitos pelo recruta
  "Designer" (Claude Opus 5.5, esforço médio, papel "Designer de visuais" neste workspace): o maestro
  só pede, nunca edita direto (Gustavo, 2026-10-12). Cada visual novo deve surpreender, com estilo
  próprio.
- Desenhar com pontos de encaixe para o que vai mudar (segunda máquina, versões do Maestri).
- O hub é a casa de tudo; o vault `ai-operating-system` é só referência e não ganha nada do hub
  (nem ponteiro, nem registro, nem mudança). Ver "Workloads piloto".
- Dados de cliente: notas e tickets citam a iniciativa pelo nome; dados pessoais ficam nas pastas de
  origem.
- [`estrategia-pos-pesquisa.md`](estrategia-pos-pesquisa.md): a peneira dos achados da pesquisa ampla
  (agora, construção, radar com gatilho) e a visão nova do hub como lugar que controla harnesses e
  modelos (pedido do Gustavo, 2026-10-14). A visão fica para um segundo mapa, depois da construção (R88, B).

## Decisions so far

<!-- uma linha por ticket resolvido: [título](issues/NN-slug.md): resumo -->

- [Ligar as máquinas com segurança](issues/05-ligar-as-maquinas-com-seguranca.md): GitHub com token
  fine-grained ou deploy key só do hub; Tailscale só no Windows, com grants; OpenSSH do Windows (o
  Tailscale SSH não serve como servidor no Windows) para a pasta não replicada; risco de conflito do
  Tailscale com o software corporativo do notebook.
- [Sync que não depende de quem gravou](issues/07-sync-que-nao-depende-de-quem-gravou.md): nenhuma
  candidata pronta cumpre tudo; o git-sync (commit de tudo, falha alto) é o mais próximo, mas exige
  agendador e um jeito de tornar a falha visível; o modo gerenciado do markdown-vault-mcp não pega
  edição externa.
- [Acesso dos agentes: pesquisa](issues/13-acesso-dos-agentes-pesquisa.md): o contrato do hub entra
  pela camada global de cada harness (o papel do Maestri esconde o `AGENTS.md` do workspace); skills
  precisam de duas entradas (`~/.claude/skills` e `~/.agents/skills`); MCP tem arquivo próprio em cada
  harness; no WSL cada harness usa o home Linux.
- [Hub no WSL: comportamento](issues/03-hub-no-wsl-comportamento.md): os arquivos ficam do lado de quem
  trabalha neles; o cruzamento é lento e não propaga aviso de mudança em nenhum sentido; o Obsidian
  do Windows não suporta cofre no WSL; o Codex prefere NTFS e o OpenCode prefere o WSL; SSH no WSL
  sofre com NAT e desligamento ocioso.
- [Lições do vault](issues/01-licoes-do-vault.md): falha se corrige com mecanismo, nunca com regra
  nova; cada informação tem um lugar só, e o checkpoint grava sem pedido; a porta de entrada é a
  camada de busca; aval só para o contrato, os adaptadores e exclusões grandes; herda isolamento,
  complexidade conquistada e adaptadores idênticos.
- [Windows ou WSL](issues/04-windows-ou-wsl.md): NTFS em `C:\context-hub` nas duas máquinas; WSL
  fora até surgir caso de uso; o critério 1 troca o OpenCode pelo Copilot (VS Code e CLI).
- [Workloads piloto](issues/02-workloads-piloto.md): nascem no hub esta frente e o que o Gustavo
  disser; conteúdo do vault é copiado e passa a ser trabalhado só no hub (já desejados:
  `armis-docs`, `armis-brand`, skill `armis-docx`); SOC STRATA fora por ora.
- [Ponto de encontro do sync](issues/06-ponto-de-encontro-do-sync.md): só o GitHub privado, com uma
  deploy key por máquina; sem assinatura; o Tailscale fica fora da construção inicial.
- [zvec-grep na camada de busca](issues/19-zvec-grep-na-camada-de-busca.md): serve só para a leitura
  (MCP só de busca); Windows nativo e multilíngue, mas sem frontmatter, fraco em pt-BR no BM25 e
  pré-1.0; sugerido para o spike contra o markdown-vault-mcp.
- [Acesso dos agentes: Copilot](issues/18-acesso-dos-agentes-copilot.md): os dois Copilots (VS Code
  e CLI) leem `~/.copilot`; contrato global em `~/.copilot/copilot-instructions.md`; skills em
  `~/.agents/skills` (a mesma do Codex), mas o `COPILOT_HOME` desliga essa pasta; MCP em
  `~/.copilot/mcp-config.json`; no Maestri entra como preset `custom`.
- [Divergência e edição concorrente](issues/08-divergencia-e-edicao-concorrente.md): divergência é
  colisão real, máquina sem sync há mais de 30 min ou cópia de conflito; aviso por notificação do
  Windows e checagem no início de sessão; colisão para a máquina com a junção desfeita; agentes
  gravam conferindo a versão (o sincronizador também grava).
- [turbovec na camada de busca](issues/20-turbovec-na-camada-de-busca.md): é uma biblioteca de índice
  vetorial (concorrente do FAISS), não uma ferramenta de busca; sem leitura de arquivos, embeddings,
  BM25 ou MCP, e o ganho de escala não pesa no hub; fora do spike.
- [Contrato file-first: zonas e checkpoint](issues/10-contrato-file-first.md): contrato de retomada
  para o hub pronto; uma nota de retomada por trabalho (sete campos, sobrescrita, teste de
  suficiência); regra no contrato global mais hook ao fim da resposta, que também leva ao hub o que só
  a memória privada sabe; a checagem de início de sessão abre a nota; sem revisão pós-sessão nem
  FreeLLMAPI no checkpoint.
- [Varredura de candidatas à camada de busca](issues/21-varredura-de-candidatas-a-camada-de-busca.md):
  a lacuna de vocabulário existia (ck, grepai, mgrep, SeaGOAT, vexor); a melhor nova é o memtomem
  (Markdown como fonte, CI em Windows, alpha, 15 estrelas); o ck é o reserva do zvec-grep.
- [Markdown: vista ou fonte da verdade](issues/22-markdown-vista-ou-fonte.md): a verdade mora num
  banco (forma em aberto) e o agente lê pela forma mais adequada; o `.md` é a vista do Gustavo, que ele
  edita e que volta ao banco. Pôs em revisão as decisões de sync, divergência e busca acima (sync e
  divergência revisados em "Revisão do sync e da divergência com o banco").
- [Sync de banco entre duas máquinas pares](issues/24-sync-de-banco-entre-duas-maquinas.md): os CRDTs
  resolvem colisão em silêncio e ficam fora; o Dolt para e avisa (conflito por célula) e usa o GitHub
  privado como remote git; a alternativa é serializar o banco em texto para o git juntar.
- [Banco como verdade com vista Markdown editável](issues/23-banco-como-verdade-com-vista-markdown.md):
  nenhuma pronta cumpre tudo; as de memória de agentes perdem ou sobrescrevem a edição humana; os
  modelos possíveis são banco replicado com vista viva (LiveSync) ou banco próprio com volta conferida.
- [Montar: CouchDB, LiveSync e MCP](issues/26-montar-couchdb-livesync-mcp.md): quase tudo pronto
  (CouchDB no Windows, LiveSync de mão dupla com merge, MCP HTTP, CLI `mirror`); falta a guarda de
  revisão no MCP (1 a 2 dias), a busca e subir o servidor (container + Tailscale).
- [Montar: Dolt como servidor central](issues/27-montar-dolt-central.md): núcleo e MCP prontos (um
  servidor local por máquina, sync por pull/push, colisão que para e avisa); falta a vista `.md` de mão
  dupla (3 a 6 dias); total de 9 a 20 dias.
- [Montar: banco central com plugin do Obsidian](issues/28-montar-banco-central-com-plugin-obsidian.md):
  três trilhas prontas; a mais completa é o Fast Note Sync Service (binário Windows, SQLite/Postgres,
  MCP nativo, `baseHash` e Manual Merge), com cerca de 2 dias de construção.
- [Debate sobre o Dolt](issues/31-debate-sobre-o-dolt.md): o Dolt fica como reserva nomeada; a vista
  `.md` de mão dupla vem pronta no FNS e no LiveSync e não existe no Dolt; spikes na ordem FNS e
  depois LiveSync; "Sonda do Dolt" é opcional.
- [Spike: Fast Note Sync](issues/29-spike-fast-note-sync.md): instalação, vista `.md` de mão dupla e
  colisão com Manual Merge funcionaram; a gravação do agente pelo MCP (e pelo REST) não confere a base
  e apagou a outra versão sem rastro, então o C1 é obrigatório; conflito fantasma depois de resolver;
  falta montar cerca de 2 a 2,5 dias.
- [Spike: CouchDB e LiveSync](issues/30-spike-couchdb-livesync.md): vista `.md` de mão dupla e colisão
  funcionaram (aviso nos dois cofres, nada sobrescrito, sem fantasma); o `write_note` do agente com
  base velha também perde a outra versão (com rastro só até a compactação), mas a correção R1 emulada
  virou conflito visível; "Concat both" mutila o texto; falta montar de 3 a 3,5 dias.
- [Como a verdade viaja entre as máquinas](issues/25-como-a-verdade-viaja-entre-as-maquinas.md): o
  banco viaja por um servidor central, CouchDB + LiveSync (O1); fork do MCP do es617 com `base_rev` e
  conflito visível antes de usar; tela de três vias editável logo depois da construção; FNS fora, Dolt
  segue reserva.
- [Onde o servidor mora](issues/34-onde-o-servidor-mora.md): S3, um CouchDB em cada par com
  replicação mestre-mestre pela tailnet; clientes (sandbox, máquina de passagem) usam o MCP de um par
  sem cópia, por padrão só de leitura; kit de par e kit de cliente na construção; o primeiro par nasce
  aqui (S1 até o segundo), e a replicação com o LiveSync é o primeiro teste.
- [Métodos conhecidos de organizar a raiz](issues/35-metodos-de-organizar-a-raiz.md): só o PARA
  (termina × não termina), o FHS (o que não replica não divide pasta) e o `.claude`/XDG (caminho
  fixo) servem à raiz; debate de três agentes propõe seis raízes (clientes, operações contínuas,
  iniciativas sem cliente, referência, oficina, entrada), `_arquivo/` dentro de cada uma e o pessoal
  condicional.
- [Portas de entrada: pesquisa](issues/37-portas-de-entrada-pesquisa.md): sem `.git` no hub, Codex e
  Copilot numa subpasta não chegam ao `AGENTS.md` da raiz; o papel do Maestri o esconde com um
  `CLAUDE.md` próprio; o LiveSync não promete renomear pasta; conector remoto do Claude não alcança a
  tailnet; o `instructions` do MCP leva o `AGENTS.md` a clientes, cortado em 2.048 caracteres no Claude
  Code; cerca de 35 pontos precisam de teste.
- [Testes das portas de entrada](issues/38-testes-das-portas-de-entrada.md): na raiz os três
  harnesses leem o `AGENTS.md`; numa subpasta Codex e Copilot precisam de marcador ou `.git`; `CLAUDE.md`
  acima do hub desliga os `AGENTS.md`; mover pasta com a outra máquina editando separa a edição; pastas
  com ponto não replicam; `instructions` do MCP só chega ao Claude Code; Claude Desktop só por MCP
  stdio, sem o contrato.
- [Contrato pelo MCP: pesquisa](issues/41-contrato-pelo-mcp-pesquisa.md): a descrição das ferramentas
  é o único canal que chega ao modelo nos três harnesses; o `instructions` entra inteiro no Copilot do
  VS Code, sob demanda no Copilot CLI (ou com `--allow-all-mcp-server-instructions`) e vai na requisição
  do Codex sem efeito confirmado; resources e prompts exigem ação do usuário ou do modelo.
- [Testes da porta do repositório fora do hub](issues/42-testes-da-porta-do-repositorio-fora-do-hub.md): link
  simbólico no arquivo global de cada harness leva o contrato a Codex e Copilot (CLI e VS Code); junction
  em `~/.agents/skills` leva as skills; link físico se solta quando o arquivo do hub é trocado; editar
  o contrato só dentro do hub.
- [Portas de entrada do hub](issues/36-portas-de-entrada-do-hub.md): a sessão na raiz é a porta
  principal e o hub não tem `CLAUDE.md`; subpasta com marcador para o Codex (o Copilot entrou
  depois, pelo arquivo global); cofre do
  Obsidian na raiz com `_archive/` movido por script; Claude Desktop lê pelo MCP (gravar foi para
  "Como os agentes gravam no hub"); cliente pelo MCP
  recebe o contrato por `instructions`, descrição das ferramentas e kit de cliente; repositório fora
  do hub por link simbólico e junction; o Maestri saiu para ticket próprio.
- [Acervo do maestro: pesquisa de peças](issues/43-acervo-do-maestro-pesquisa.md): além de papéis,
  setups e contratos-opção cabem preset, nota-modelo, rotina-modelo, receita de floor, workspace-modelo,
  receita de portal, ambiente, subagente, perfil de modelo e hook de início; o maestro não aplica
  partitura pela CLI, então setup é receita de comandos; a família `maestri-*` é um SKILL.md por
  assunto; o Maestri não tem instrução global para workspace novo.
- [Guarda do acervo: mods e hooks, pesquisa](issues/44-guarda-do-acervo-mods-e-hooks-pesquisa.md): no
  Claude Code, mod e hook de settings recusam ou pedem aval ao gravar no acervo, veem toda skill
  carregada e podem impor um verificador em outro modelo; o Codex só recusa (sem `ask` nem hook de
  modelo) e o Copilot recusa ou pergunta, sem modelo; o Maestri não registra quem usa uma peça; a
  guarda tem de ficar no escopo do usuário para valer dentro de um papel.
- [Testes do papel do Maestri com Codex e Copilot](issues/45-testes-do-papel-do-maestri.md): na pasta
  de um papel, o Codex só chega à raiz e à iniciativa com o marcador de raiz; o Copilot chega à
  iniciativa mas não à raiz; o Maestri não regrava os arquivos do papel ao reiniciar, mas editar o
  papel os reescreve e reinicia os terminais; recrutas com o mesmo papel e pasta dividem a pasta.
- [Copilot com assinatura Enterprise: pesquisa](issues/46-copilot-com-assinatura-enterprise-pesquisa.md):
  instruções da organização não chegam ao Copilot CLI e chegam ao VS Code (docs se contradizem); nada
  substitui o contrato, só soma; a maior ameaça é a lista de MCP permitidos da empresa, depois a
  política do VS Code que só aceita personalização por plugin e os hooks só da empresa; nesta máquina
  não há política local; `/env`, `/mcp` e "Policy Diagnostics" mostram o que vale.
- [Maestri: padrão e liberdade](issues/40-maestri-padrao-e-liberdade.md): virou o acervo do maestro,
  peças prontas como opção (papéis genéricos, setups como receita com variantes, contratos-opção como
  roteamento de modelos), numa família de skills `maestro-*` em `agents/skills/`; guarda forte no
  Claude Code com aval para alterar, propostas do Codex e do Copilot; workspace de iniciativa abre na
  pasta dela para os três harnesses; `claude-md-and-agents-md` em cada par.
- [Disco e banco sem o Obsidian: pesquisa](issues/47-disco-e-banco-sem-o-obsidian-pesquisa.md): o
  plugin só leva o que o Obsidian enxerga (docx, xlsx, csv pedem "Detect all file extensions"); limite
  padrão de 50 MiB e o CouchDB não é o gargalo; binário vira pedaços Base64 que se acumulam até um GC
  manual; colisão de binário fica com o `mtime` mais novo sem perguntar; o CLI `daemon` leva tudo, mas
  não tem receita para Windows; plugin e CLI na mesma pasta não têm fonte; o `livesync-bridge` não serve.
- [Teste: disco e banco sem o Obsidian](issues/48-teste-disco-e-banco-sem-o-obsidian.md): o plugin
  leva qualquer arquivo (só md, txt e csv como texto); acima de 50 MiB fica fora sem aviso; versões de
  binário reaproveitam pedaços; colisão de binário some em silêncio (recuperável por script); o CLI roda no
  Windows e aguenta quedas, mas vaza pastas com ponto aninhadas na partida; revezamento cria conflito
  falso; recomendação: plugin e CLI sempre ligados, o CLI como tarefa agendada.
- [Revisão do sync e da divergência com o banco](issues/33-revisao-do-sync-e-da-divergencia.md): as
  garantias ficam e o mecanismo vira CouchDB + LiveSync; cada máquina envia as próprias mudanças à outra
  pela tailnet; o sincronizador é o CLI do LiveSync como tarefa agendada, sem depender do Obsidian; vai ao
  banco todo arquivo comum até 200 MiB, fora pastas com ponto; o GitHub vira cópia de segurança diária;
  uma vigia a cada 5 min avisa colisão, sync parado há 15 min, binário descartado e arquivo grande.
- [Preparar o FreeLLMAPI para a pesquisa da busca](issues/49-preparar-freellmapi-para-a-pesquisa.md):
  levantamento (185 modelos prontos, 32 pools) e bancada (49 com JSON válido; sem busca, só 65 de 169 URLs
  reais) viram a base do despachante da pesquisa ampla; o perfil `pesquisa` e a função `web_search` saíram
  na proposta refeita; a Default fica como está.

- [Montar os scripts do laço da pesquisa ampla](issues/52-montar-os-scripts-do-laco.md): suite em `laco/`
  (despachante com orçamento por modelo, geradores, juntador com bola de neve e gate, painel); rodou 5 ondas.
- [Pesquisa ampla: lugares e mecanismos de busca](issues/50-pesquisa-ampla-lugares-e-mecanismos-de-busca.md): o
  CouchDB só tem pedaços cifrados, então "dentro do banco" vira um índice do MCP do banco; nenhuma ferramenta pronta
  cumpre a régua (as mais próximas, obsidian-hybrid-search e memtomem, não têm stemmer de português); recomendação
  para "Camada de busca": teste obsidian-hybrid-search × memtomem decide entre Leve com alcance (disco + repasse na
  tailnet) e Robusta (índice no MCP do banco). Síntese e inventário em `exploracao/anexos/pesquisa-50-*`.

- [Modelos de embeddings da busca: pesquisa](issues/54-modelos-de-embeddings-da-busca.md): arctic-embed-m-v2.0
  local como padrão nas duas máquinas (MRR 0,60, 46 ms, o único provado no obsidian-hybrid-search, híbrida 0,63);
  gemini-embedding-001 pela API como segunda opção ligável depois, para as buscas por sentido; rerankers no Radar.

- [Camada de busca](issues/09-camada-de-busca.md): Leve com alcance: obsidian-hybrid-search com o arctic local no
  disco de cada máquina, servindo MCP por HTTP na tailnet; a Robusta (índice no MCP do banco) fica de reserva com
  gatilho; um analisador só, sem campo de idioma; o gemini pronto e desligado.
- [Como os agentes gravam no hub](issues/11-como-os-agentes-gravam.md): pelos dois caminhos: troca de trecho no
  disco; regravação inteira de arquivo existente pelo MCP do banco com a versão lida, e um hook que a recusa no disco;
  arquivo novo no disco. Desktop pela pasta conectada e pelo MCP; cliente com gravação ligável; aviso (sem recusa) de
  leitura grande fora da busca; com o banco fora, a regravação espera.
- [Acesso dos agentes: decisão](issues/14-acesso-dos-agentes-decisao.md): contrato por link simbólico e skills por
  junction; hooks no escopo do usuário (início, fim, recusa antes da ferramenta) nos três harnesses; Codex com acesso
  total e o `notify` como aviso da vigia; MCP local em 127.0.0.1 no par e, para o cliente, o TBXark/mcp-proxy na tailnet
  com rotas e tokens de busca, banco e banco com escrita.
- [Arquitetura de pastas e frontmatter do hub](issues/12-arquitetura-de-pastas-e-frontmatter.md): `AGENTS.md` e seis
  raízes em inglês (`clients/` com dois níveis, as outras com um, `_archive/` em cada uma); cada iniciativa nasce com
  um núcleo de seis arquivos por ritmo e soma blocos do catálogo `agents/blocks.md`; frontmatter por tipo, com o tipo
  pelo caminho e esquemas em `agents/frontmatter/`, `status` comum e `stage` do ciclo, imposto por hook, MCP e
  verificador; o `index.md` é o cartão da pasta (`summary: auto`, `local`); anexos com texto em arquivo irmão
  `.pdf.md`; links `par://` só para o que não replica; tudo replica, fora o que tem ponto ou `local: true`.
- [Roteamento de skills](issues/15-roteamento-de-skills.md): tabela `agents/skills/routing.yml` (só o que a descrição
  não resolve) e hook de entrada sem IA que injeta "use a skill X"; briefs citam a skill; o verificador registra sem
  obrigar e o maestro corrige a tabela sozinho, avisando; global só as skills de uso geral, as de papel na pasta do
  papel; o GSD sai do escopo global.
- [Passagem para a construção](issues/16-passagem-para-a-construcao.md): spec e 11 tickets em
  `.scratch/construcao-do-hub/`; laço de 10 workers e 2 Prumos em faixas verticais, execução em 1 hora, hub e HOME de
  ensaio.

## Not yet specified

- O perfil por máquina (§6.1 da exploração): o que é local de cada máquina e como se declara.
- O Obsidian com o hub: o hub como cofre próprio, e como ele fica ao lado do cofre do vault enquanto
  os dois convivem.
- Como esta prova de conceito vira o hub real em `C:\context-hub`.
- Usos do FreeLLMAPI no funcionamento do hub além de embeddings (por exemplo, resumos); o checkpoint
  ficou sem ele ("Contrato file-first: zonas e checkpoint").

- A "suite de busca" (o laço da pesquisa ampla: despachante, geradores, juntador, plano, sementes, painel) como
  template genérico no acervo do maestro, pedido do Gustavo (2026-10-13); o catálogo da pesquisa também serve
  para a stack do hub além da busca.
- O portal do projeto (rodadas, caixa, cartas e a página Laços, ticket 55) como peça do acervo do maestro, para
  reusar em outros projetos (Gustavo, 2026-10-14: "vou querer sim no futuro").

## Out of scope

- O hub como lugar que controla como harnesses e modelos trabalham (política por modelo e harness, gateway
  de modelos, MCP aplicando regra, registro de uso, memória de trabalho contra o esquecimento de contexto): segundo mapa, que começa com o hub construído
  (Gustavo, 2026-10-14; `estrategia-pos-pesquisa.md`, R88). O que este mapa já decidiu sobre contrato,
  skills, hooks e acervo continua aqui.
- [Serviço de busca da função web_search](issues/51-servico-de-busca-da-funcao-web-search.md): a proposta
  refeita da pesquisa ampla não força tool calling, então não há função de busca nem serviço a escolher.
- Aposentar o vault `ai-operating-system`: fica para depois deste mapa; a convivência é temporária,
  e o hub não desenha nada para o vault (Q10; "Workloads piloto").
- Migrar os workspaces existentes do Maestri; a skill de aplicar/auditar do Maestri (pode voltar
  depois, "Maestri: padrão e liberdade"); a convivência
  entre superpowers, GSD e Matt (Q2, Q8).
- O `freellmapi-mcp` e a skill que ensina a usá-lo; só o roteamento dessa skill entra (Q13).
- Edição concorrente entre o Obsidian e um agente no mesmo arquivo (Q4).
- Tailscale e servidor SSH para a pasta não replicada e a operação remota: entram num ticket à parte
  quando surgir o primeiro caso; nenhum dos cinco critérios depende deles ("Ponto de encontro do sync").
- Mecanismo de controle de acesso por pasta (na camada de busca, como guardrail no `AGENTS.md` ou
  outro): o Gustavo vai desenvolver depois, fora deste projeto; por ora tudo vive nas duas máquinas
  ("Arquitetura de pastas e frontmatter do hub", rodada 3).
- Política de dados de cliente para a segunda máquina: o dado fica tão protegido lá quanto aqui (Q3).
