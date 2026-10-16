# Pesquisa ampla: lugares e mecanismos de busca

Type: research
Status: resolved
Blocked by: 49, 52

## Question

Que lugares e mecanismos de busca existem para o hub, e como se combinam? Catálogo, não vencedor, em três
eixos: **lugares** (disco de cada máquina, inclusive no WSL; dentro do MCP do banco; o MCP do banco
repassando à busca do disco; serviço na rede; cópia leve no cliente; vários juntos como reserva, e quem fica
atendido em cada um: agente na máquina, cliente pela tailnet, sandbox sem tailnet, tailnet fora do ar),
**mecanismos** (prontos, peças, conceitos, agregadores e roteadores) e **combinações** leves e robustas.
A régua vira coluna, nunca filtro; nada sai, o que falta vira "o que falta montar"; as candidatas atuais
entram (zvec-grep, memtomem, ck, markdown-vault-mcp, grooveseek e as das pesquisas antigas).

Método aprovado na rodada 6 de "Camada de busca": o laço da
[proposta](../prototipos/proposta-09-roteamento-da-pesquisa.md) (etapas 1 a 6; a etapa 0 é "Preparar o
FreeLLMAPI para a pesquisa da busca"), desenhado em
[`prototipo-09-roteamento-da-pesquisa.html`](../prototipos/prototipo-09-roteamento-da-pesquisa.html).
Geradores gratuitos sem ferramenta de escrita (só `google_search`), livro-razão que retoma, dois modelos de
famílias diferentes por pedido, bola de neve até saturar (duas ondas com menos de 5% de novos, depois da
calibração com as sementes ocultas), Haiku 5.5 junta sem excluir, Sonnet 5.5 confere em fonte primária,
Opus audita ~10% e sintetiza. Colunas: os dez grupos da proposta. Protocolo da §10.4 da exploração.

**Método revisto (2026-10-13):** a [proposta refeita](../prototipos/proposta-50-laco-da-pesquisa.md)
substitui as etapas 0 e 2 e os papéis. O roteamento é do laço (modelos fixados no catálogo inteiro, sem `auto`
nem fallback chain), não há tool calling forçado e o controle é dividido entre recrutas no Maestri.

Ao iniciar: o Gustavo escolhe o teto de segurança (horas ou tokens). Só roda quando ele disser "pode
iniciar".

## Answer

2026-10-14. Síntese: [pesquisa-50-sintese.md](../../../exploracao/anexos/pesquisa-50-sintese.md). Inventário completo:
[pesquisa-50-inventario.md](../../../exploracao/anexos/pesquisa-50-inventario.md). Página visual: `laco/painel/sintese.html`
("Super Trunfo da busca"). Dados em `laco/sintese/`.

- **O CouchDB não enxerga o texto.** O LiveSync grava as notas em pedaços cifrados, então a busca nativa (Nouveau,
  Clouseau, Mango) não serve. "Dentro do banco" passa a ser um índice do próprio MCP do banco, alimentado pelo feed de
  mudanças, com o texto que só o MCP decifra.
- **Lugares:** disco de cada máquina, disco com repasse do MCP pela tailnet, índice dentro do MCP do banco, serviço
  na rede, cópia leve no cliente ou sandbox, e o lado do Obsidian. A matriz de atendimento está na §2.6.
- **Combinações:**
  - Leve: ferramenta pronta no disco, ~1 dia;
  - Leve com alcance: Leve com o repasse na tailnet, +0,5 a 1 dia;
  - Robusta: índice no MCP do banco, ~5 a 8 dias, estimativa não medida;
  - Para sandbox: cópia leve, 1 a 2 dias;
  - Reserva: as três juntas.
- **Nenhuma ferramenta pronta cumpre a régua inteira.** As mais próximas são obsidian-hybrid-search e memtomem, e as
  duas usam SQLite FTS5 sem stemmer de português. Português léxico existe nos motores e bibliotecas (Tantivy, Lucene,
  Bleve, Xapian, Orama, Pagefind, Snowball), não nas ferramentas.
- **Os mais citados do catálogo:**
  - fora pela premissa: Weaviate e o servidor do Milvus (Docker/WSL), pgvector;
  - pesados: Elasticsearch, Solr;
  - parados ou sem português: Whoosh, lunr.js, Chroma.
- **Stack:** com o MCP do banco em Python, todas as peças têm Windows confirmado: SDK do MCP v2, python-frontmatter,
  lingua-py, ONNX Runtime e tantivy-py. Detalhe por área na §4.
- **Cobertura:** 5526 itens do laço → 353 entidades (169 de busca, 184 de stack) e 292 conceitos. A régua com fonte
  cobre 91 itens. O resto está no inventário, com o que o README diz.
- **Recomendação para "Camada de busca"** (a decisão é do Gustavo): um teste de bancada obsidian-hybrid-search contra
  memtomem, sobre conteúdo real em pt e en, decide entre Leve com alcance e Robusta. Antes, confirmar três fatos:
  - se o FreeLLMAPI serve um modelo de embeddings multilíngue;
  - a linguagem do MCP do es617;
  - se a exclusão de pastas com ponto do LiveSync cobre arquivos com ponto.
- **Custo medido da pesquisa toda** (sem contar as conversas do maestro e dos recrutas):
  - ~31,7 milhões de tokens Claude: Haiku 12,0, Sonnet 17,1 e Opus 2,6;
  - FreeLLMAPI: ~10,5 mil tentativas, gratuitas.

## Comments

- 2026-10-13: aberto a partir da R78 de "Camada de busca" (o que a busca faz ficou para esta pesquisa) e
  das rodadas 5 e 6 (escopo e método).
- 2026-10-13: o Gustavo mudou o método ("Preparar o FreeLLMAPI para a pesquisa da busca", rodada 2): todo
  gerador tem ferramenta de busca, porque sem ela inventa URL (na bancada, só 65 de 169 URLs existiam); sem os
  do Google hoje, só modelos com cota por token ou por minuto. Fora do Google o FreeLLMAPI não tem busca, então
  o laço oferece e executa uma função `web_search`; o serviço que ela chama está em aberto.
- 2026-10-13: o Gustavo devolveu o método para a etapa da proposta ("Voltemos a etapa da proposta. Entenda
  minha requisição"). O que ele quer: loop engineering pelo roteamento padrão do gateway (`auto`), com o
  catálogo inteiro (185 modelos prontos, não um perfil de 11), sem forçar tool calling ("quando você chama um
  modelo ele tem busca habilitada"), gerando insumo gigante até o resultado ficar repetitivo (o gate dos 5%
  fica), e não controlado por um só agente. O perfil `pesquisa` de 11 modelos e o ticket "Serviço de busca
  da função web_search" vieram de uma leitura errada minha. Fato a pesar: no gateway, a única busca é o
  `google_search` do Google (`server/src/providers/google.ts`); nenhum modelo do catálogo tem nome de busca
  (search, sonar, online, compound); na bancada, sem ferramenta, 104 de 169 URLs não existiam. Rodada 1 da
  proposta refeita na nota "Rodada atual".
- 2026-10-13: rodada 1 da proposta refeita, respondida:
  1. **Roteamento é meu:** o laço fixa os modelos mecanicamente, com um desenho de chamadas feito a partir do
     levantamento de todos os modelos e cotas, e não usa o `auto`. O motivo: "o routing strategy do freellmapi
     é bem limitado e vai ficar chamando sempre o mesmo modelo até acabar a cota". Não precisa mais de
     fallback chain; falha de uma chave e acerto na outra é normal.
  2. Não forçar tool calling: sim.
  3. Para quando ficar repetitivo (gate dos 5%): sim.
  4. O FreeLLMAPI faz o grosso, e o Claude não: "exato".
  5. O controle não fica num agente só: **A** (vários trabalhadores, scripts em paralelo, cada um com o seu
     livro-razão) e **C** (vários agentes no Maestri, cada um tocando uma parte do laço), "por conta do que
     falei sobre o routing ter que ser algo seu". O B (juntar, conferir e auditar no FreeLLMAPI) não foi
     marcado: segue a proposta aprovada (Haiku, Sonnet, Opus).
- 2026-10-13: rodada 2 da proposta refeita, respondida: os 4 papéis, com ajuste. **Despachante:** Claude
  Opus 5.5. **Geradores (3):** Claude Haiku 5.5. **Juntador:** Claude Sonnet 5.5. O maestro Claude dispara um
  Sonnet 5.5 para a conferência e assume o resto (auditoria e síntese).
- 2026-10-13: [proposta refeita](../prototipos/proposta-50-laco-da-pesquisa.md): papéis, roteamento do
  despachante (universo do catálogo, orçamento por modelo a 90% contando tentativas de chave, par de famílias e
  pools diferentes sorteado por orçamento × acerto, ritmo por pool, JSON no texto, saúde, teto de segurança) e
  o que sai (perfil `pesquisa` como caminho, ticket da `web_search`, etapa 0). Rodada 3 na nota: aprovar.
- 2026-10-13: rodada 3 da proposta refeita, respondida: **A**, aprovada. "Serviço de busca da função
  web_search" saiu do escopo. A pesquisa roda com o "pode iniciar" e o teto (horas ou pedidos).
- 2026-10-13: "pode iniciar" do Gustavo (sem ensaio, resposta B em "Montar os scripts do laço da pesquisa
  ampla"). Falta o teto de segurança.
- 2026-10-13: teto de segurança: **A**, 3000 tentativas ou 6 horas. Estimativa de tokens do Claude dos 5
  recrutas mostrada antes (não medida).
- 2026-10-13 (14:26Z): laço ligado. Recrutas no Maestri: Bússola (Despachante, Opus 5.5), Faísca, Brasa e
  Centelha (Geradores pt-es, en-de-ru e zh-ja, Haiku 5.5) e Tear (Juntador, Sonnet 5.5); papéis "Despachante
  do laço", "Gerador do laço" e "Juntador do laço". As primeiras partidas caíram porque o Bash dos recrutas
  come as barras invertidas do caminho; relançados com barras normais. Teto 3000 tentativas ou 6 h.
- 2026-10-13: teto mudado pelo Gustavo: 20000 tentativas, mantidas as 6 horas (contadas desde a partida,
  14:22Z).
- 2026-10-13: pedido do Gustavo: o estado no chat a cada 10 min. Feito por `laco/painel.py` (lê o banco e os
  livros-razão e manda `maestri say`; não chama modelo e não gasta token do Claude), ligado em segundo plano até
  o laço terminar.
- 2026-10-13 (~15:05Z): a máquina ficou com pouca memória (1,8 GB livres de 15,7) e o Claude Code matou os
  processos em segundo plano de três recrutas (despachante, geradores pt-es e zh-ja). Os 5 processos do laço
  agora rodam fora do Claude Code (`Start-Process`, sem janela, logs em `laco/logs/`). Os recrutas ficam
  parados. O Tear decide os ambíguos quando o maestro chamar (a junção recalcula tudo a cada onda, então a
  decisão pode vir depois). Onda 1 fechada: 554 itens, 300 células na onda 2.
- 2026-10-13: resposta A: dispensados Bússola, Faísca, Brasa e Centelha; fica só o Tear (ambíguos). O maestro
  cobre o papel do despachante (tirar modelo que erra sem parar) pelo painel.
- 2026-10-13: a rotina "Painel do laço" disparou 8 vezes, mas nenhuma mensagem chegou ao chat; no disparo das
  13:07 BRT o pre-run nem chegou a gravar o registro (causa não verificada; o maestro estava ocupado e a rotina
  pula disparo quando o terminal está ocupado). A rotina foi pausada, não apagada, e o painel roda fora do
  Claude Code (`Start-Process`), com as variáveis do terminal do maestro; o envio às 13:08 deu `rc=0`.
- 2026-10-13: onda 2 fechada às 15:59Z: 2100 itens, 1595 novos (76%). Pedido do Gustavo: painel visual da
  execução pelo Designer, "Me surpreenda. E sem muito texto". `painel.py` agora grava `laco/painel/dados.js` a
  cada 60 s (`painel_dados.py`), e a página do Designer (`laco/painel/index.html`) se redesenha sozinha a cada
  30 s, sem o Designer mexer nela a cada estado.
- 2026-10-13: painel visual pronto pelo Designer, sem portal: `laco/painel/index.html` ("maré de novos"). A
  projeção no ritmo atual aponta saturação lá pela onda 12, e o teto de 6 h acaba antes.
- 2026-10-13: o Gustavo pediu duas verificações de "os modelos buscam ou respondem de memória": (1) URLs do
  catálogo por provedor (só GET) e (2) pergunta de atualidade aos ~30 modelos que mais respondem, com e sem
  "busque na web" no começo do prompt (teste da ideia dele de pedir a busca no texto). Também disse: a pesquisa
  já rende mais do que ele esperava (~15 opções novas imaginadas, 3525 itens), há opções para a stack do hub
  inteiro, não só da busca; não quer perder nem o resultado nem a montagem, e quer a "suite de busca" como
  template no acervo do maestro, mais genérica.
- 2026-10-13: teste de atualidade ([`laco/verificacao/atualidade.md`](../laco/verificacao/atualidade.md)): 30
  modelos, com e sem "Search the web first"; gabarito Obsidian 1.14 (changelog oficial, 2026-10-05). 51 de 60
  responderam; **nenhum acertou**, com ou sem o pedido (as versões vão de 1.3 a 1.8, de 2023 a 2025). 15 sem pedido
  e 19 com pedido dizem que buscaram, sem ter buscado. Pedir a busca no texto não liga busca nenhuma; só faz o
  modelo afirmar que buscou.
- 2026-10-13: degraus de trabalhadores (pedido do Gustavo). Base, 6 por gerador: 13,2 aceitas/min, 5% de cota.
  Degrau 1, 12 por gerador (10 min): 15,6 aceitas/min, 5% de cota, 36 em voo (o teto). Cota abaixo de 10%, então
  degrau 2: 20 por gerador.
- 2026-10-13: URLs do catálogo ([`laco/verificacao/urls-por-provedor.md`](../laco/verificacao/urls-por-provedor.md)):
  4231 URLs únicas com GET; 1661 existem (200), 899 não existem (404) e 1272 ficaram sem resposta porque o GitHub
  limitou (429). Por citação, cada provedor fica entre 52% e 76% de URLs reais, sem nenhum perto de 100%: nada
  indica busca em nenhum provedor, o que bate com o teste de atualidade.
- 2026-10-13: degrau 2, 20 por gerador (10 min): 910 chamadas, 53,6 aceitas/min (4x o degrau 1), 8% de cota, 31
  em voo de 60 possíveis (agora o limite são os modelos livres, não os trabalhadores). Fica em 20.
- 2026-10-13: decisão do Gustavo: quando a onda 5 fechar, parar tudo e dar o laço por concluído (sem esperar o gate
  dos 5%), e seguir para as próximas etapas. Ligado `laco/parar_apos.py --onda 5`. Aprendizados que ele registrou:
  dava para ter usado a cota do Google com o `google_search` ligado em vez de gastá-la na bancada, ou pesquisado
  como forçar busca nos outros modelos; a estratégia da suite vai ter aprimoramentos. Pediu estimativa de incluir
  na suite subagentes Claude Haiku 5.5 (ou mais leves) e subagentes Codex num modelo leve com busca na web, com o
  mesmo controle de cota.
- 2026-10-13: estimativa enviada (conferida nas ajudas das CLIs locais): Claude `-p --model haiku --allowedTools
  WebSearch WebFetch --max-budget-usd`; Codex `exec -m <modelo> --output-schema --json` e `--search` (não verificado
  se vale no `exec`). Construção de cerca de 1 dia; 15 a 40 mil tokens de Haiku por pedido com busca, de 5 a 12
  milhões por onda de 300 pedidos; usar só para atualidade, nicho e calibração; 2 ou 3 `claude -p` de cada vez
  nesta máquina (250 a 400 MB cada). Fica como aprimoramento da suite, para o template do acervo do maestro.
- 2026-10-13: correção do Gustavo: os "subagentes" que ele quer são os do próprio harness, disparados por um agente
  no Maestri (não um processo por pedido via script); ele acha que o `claude -p` por script exigiria API, não a
  assinatura.
- 2026-10-13: o Gustavo aceitou a estimativa por ora (não vai aplicar agora), mas criticou: era "achismo" sem
  consultar a documentação, e o paralelismo proposto (5 subagentes com 3 células) foi tímido; ele pensa em uns 30.
  Para o template da suite: paralelismo na casa das dezenas e estimativa com fonte primária.
- 2026-10-13 (18:13Z): laço concluído depois da onda 5, por decisão do Gustavo ("bravo, foi um sucesso"). Curva de
  novos: 100%, 76%, 37%, 27%, 22% (5526 itens; o gate dos 5% não foi alcançado, e a calibração não rodou). 7388
  tentativas. Catálogo: 888 itens com 3 menções ou mais, e 754 com 2 famílias ou mais e URL viva ou bloqueada.
  Quanto às URLs: 1241 itens têm URL real, 1563 só têm URL falsa, 1016 têm URL bloqueada na conferência e 1706 não
  têm URL. Restam 298 casos ambíguos. Rodada na nota: o plano das próximas etapas.
- 2026-10-13: próximas etapas aprovadas (resposta **B**): limpar, triagem, conferência por uns 30 subagentes Sonnet
  depois de um piloto, auditoria por Opus em 10%, síntese. Ajustes do Gustavo: ele dá `/clear` no maestro antes de
  começar, e 50% da triagem vai a subagentes Haiku 5.5, a outra metade ao FreeLLMAPI. Plano completo e ponto de
  partida para a sessão nova: [`proposta-50-depois-do-laco.md`](../prototipos/proposta-50-depois-do-laco.md).
- 2026-10-13 (18:25Z): depois do `/clear`, "vamos começar": **etapa 1 (Limpar) em curso.** O Tear decide os 298
  ambíguos; `baixar_readmes.py` baixa o README bruto (raw.githubusercontent.com, ramo `HEAD`) dos 2040 itens com
  repositório e monta os cartões em `laco/etapas/cartoes/`; `verificar_urls.py --repetir 429,403,URLError
  --trabalhadores 1 --pausa 2` reconfere devagar as URLs bloqueadas (espera o Retry-After depois de 429). O estado das
  etapas fica em `laco/etapas/` e `painel_etapas.py --servico` grava `laco/painel/etapas.js` a cada 60 s. Pedido do
  Gustavo: o Designer adequa o painel às etapas ("agora não são ondas"). Processos fora do Claude Code, logs em
  `laco/logs/`.
- 2026-10-13: Tear decidiu os 298 ambíguos (162 juntar, 106 separar, 193 quarentena; o maestro separou "gin", o
  único que sobrou). `juntador.py --rejuntar` (modo novo: refaz `itens.json` e `ambiguos.json` sem fechar onda; a
  versão anterior fica em `catalogo/itens-antes-de-rejuntar.json`): 5433 itens, 193 em quarentena, 1439 com
  repositório fora da quarentena. O download de READMEs foi reiniciado só para esses 1439 (os primeiros 300: 69% com
  README). Painel do Designer pronto: `laco/painel/etapas.html` ("o garimpo"), aberto no portal "Garimpo";
  `index.html` fica como registro do laço. Prontos para a etapa 2: `etapas/triagem/prompt.md` (o mesmo para as duas
  metades), `triagem_freellm.py` (sorteio com semente fixa; 2 modelos de famílias e pools diferentes por item, pelo
  despachante) e `etapas/triagem/haiku-instrucoes.md` (lotes de 5 por subagente). Folga do FreeLLMAPI hoje: 9262
  tentativas em modelos com limite diário, mais 73 sem limite; a triagem precisa de umas 2000.
- 2026-10-13 (18:39Z): rodada da metade Haiku respondida: **A**, piloto primeiro. O Tear dispara 2 subagentes Haiku
  com 5 itens cada (10 itens, ~0,25 milhão de tokens estimados); o maestro mede os tokens de verdade e traz a conta
  dos restantes; as levas de ~30 subagentes só saem com um segundo aval do Gustavo. O piloto sai quando os READMEs
  terminarem (o sorteio depende de todos os cartões).
- 2026-10-13 (18:51Z): READMEs prontos. Dos 1439 repositórios: 606 com README, 620 sem README pela raw (amostra de 8
  conferida no github.com: todos 404, ou seja, repositórios inventados), 212 mortos (404 na conferência de URLs), 10
  com erro. Sorteio (semente 20261013): 597 itens com README, **298 para o FreeLLMAPI e 299 para o Haiku**. Etapa 1
  marcada como feita (a reconferência de URLs segue ao fundo e não segura nada). **Etapa 2 em curso:** triagem
  FreeLLMAPI ligada com 20 trabalhadores e teto novo (+5000 tentativas, ou seja 12388 no total, ou 6 h); o Tear
  dispara o piloto Haiku (2 subagentes × 5 itens). Pedido do Gustavo: o painel vira uma usina de **dessalinização**
  (o final é água potável) e mostra mais dados do conteúdo e da execução; `painel_etapas.py` ganhou os blocos
  `conteudo` e `execucao`.
- 2026-10-13 (18:54Z): piloto Haiku medido: 2 subagentes × 5 itens, 48 s em paralelo, **140 803 tokens (14,1 mil por
  item)**, 10 de 10 arquivos válidos no esquema do prompt (a estimativa não medida era 20 a 25 mil por item). Conta dos
  289 restantes: ~4,1 milhões de tokens Haiku, em 2 levas de ~30 subagentes. Rodada na nota: segundo aval.
- 2026-10-13: segundo aval do Gustavo: **A**, o Tear solta as 2 levas de ~30 subagentes Haiku para os 289 restantes
  (~4,1 milhões de tokens medidos pelo piloto). Pergunta dele no chat: "dos 5240 itens só 1439 eram repos?" Resposta:
  1439 com repositório no GitHub, 1921 com outro link (988 vivos), 1880 só com o nome (1600 citados uma vez); 895 só
  conceito e ~320 conceito e ferramenta. A triagem atual cobre só os 597 com README; sites, conceitos e só-nome são
  lacuna, e a proposta (sites vivos pelo texto da página, conceitos sem fonte primária, só-nome com uma citação fora)
  vai como a próxima rodada.
- 2026-10-13 (19:20Z): **triagem dos 597 com README concluída.**
  - FreeLLMAPI: 298 itens em 15 min (18:51 a 19:06Z), 596 respostas aceitas, 370 recusadas (301 JSON inválido, 42
    provedor, 27 cota), 2,24 milhões de tokens gratuitos. Os 2 modelos **divergem em 165 dos 298 (55%)**; dos
    concordantes: 37 busca, 32 stack, 28 nada, 36 dúvida.
  - Haiku: 299 itens (piloto + 3 levas, 58 subagentes; o Claude Code limita a 20 simultâneos), ~21 min, **4,51
    milhões de tokens** (piloto incluído), 0 erros. Vereditos: 52 busca, 81 stack, 104 nada, 62 dúvida.
  - Ruído visível: "actix-web" saiu como busca com MCP no FreeLLMAPI; o cartão de `gh:nats-io/nats` mistura o
    README do nats.go com resumos de CouchDB (aviso do Tear). A conferência pega os dois.
- 2026-10-13: decisão do Gustavo sobre a lacuna (no chat): **sites com URL viva entram na triagem, também divididos**
  entre FreeLLMAPI e Haiku; **conceitos vão aos Haiku**, e o resultado deles entra na auditoria; **só nome com uma
  citação fica fora**. O custo Haiku dessas duas frentes é dito antes de soltar.
- 2026-10-13 (19:40Z): sites e conceitos prontos para a triagem. `baixar_sites.py`: 852 itens `web:` com URL viva (fora
  os só-conceito), 767 com texto, 67 com pouco texto, 18 com erro; cartões no mesmo formato (o texto da página no
  campo `readme`). `triagem_freellm.py --sortear-novos web:` acrescentou 766 sites ao sorteio sem refazê-lo: 383
  FreeLLMAPI e 383 Haiku; a triagem FreeLLMAPI dos sites está ligada. `cartoes_conceitos.py`: 895 itens só conceito
  viram 874 cartões (`etapas/conceitos/`, prompt próprio com `concept_en` para agrupar idiomas depois; lotes de 25 por
  subagente). Slug único em todos os scripts. Pedido do Gustavo: o Designer atualiza a usina para o fluxo novo.
  Rodada na nota: custo Haiku de sites e conceitos.
- 2026-10-13: custo Haiku de sites e conceitos: **A**. Os 383 sites saem já (~5,4 milhões de tokens). Nos conceitos,
  primeiro 1 subagente piloto com 25 cartões; se o custo medido ficar até 30% acima dos ~3 milhões estimados, o resto
  segue sem nova pergunta, e se passar disso o maestro volta à nota.
- 2026-10-13 (19:50Z): piloto de conceitos: 1 subagente, 25 cartões, **82 707 tokens (3,3 mil por item)**, 25 de 25
  válidos, ~12 min. Conta dos 874: ~2,9 milhões, dentro do combinado (até 30% acima de 3 milhões), então os 849
  restantes seguem sem nova pergunta.
- 2026-10-13: etapa 3 preparada. `preparar_conferencia.py` monta pacotes (cartão + respostas da triagem) dos itens
  com "search", "stack", dúvida ou divergência; com a triagem parcial dos sites já são 928 (345 dúvida, 269
  divergentes, 158 busca, 156 stack; 465 repositórios e 463 sites). Prompt em `etapas/conferencia/prompt.md`
  (confirma / corrige / rejeita, com o registro final corrigido), instruções para o Tear em `instrucoes.md` (lotes de
  5, Sonnet). Piloto de 10 itens (misturando motivos e fontes) pedido ao Tear, como manda o plano aprovado; as levas
  só saem com o custo dito ao Gustavo.
- 2026-10-13 (~20:05Z): pedido do Gustavo: "o tear tá sobrecarregado, dispare 2 parceiros pra ele". Recrutados Osmose
  e Salina (Sonnet 5.5, papel novo "Despachante de subagentes", fino: só monta fila, dispara, conta e anota levas).
  Divisão: Tear só os sites da triagem Haiku; Osmose os conceitos (fila de trás para a frente, para não colidir); Salina
  a conferência, por ora só o piloto de 10.
- 2026-10-13 (20:03Z): piloto da conferência (Salina, 1 subagente Sonnet, 10 itens): **95 276 tokens (9,5 mil por
  item)**, 106 s, 10 de 10 arquivos. Resultado: 6 rejeita, 3 confirma, 1 corrige; as notas citam o README (ex.: Spark
  NLP pesado demais, natscli é só cliente, PyTerrier exige Java). Fila atual da conferência: 982 itens (vai a ~1050
  quando os sites do Haiku acabarem); conta: ~10 milhões de tokens Sonnet. Rodada na nota.
- 2026-10-13 (20:08Z): conferência: **B**, dividida entre Salina e Tear (quando ele acabar os sites), cada um com até 20
  subagentes Sonnet de cada vez; ~10 milhões de tokens. Salina percorre a fila do início, Tear do fim, conferindo antes
  de cada leva o que já tem resposta. O maestro roda `preparar_conferencia.py` de novo quando os sites acabarem.
- 2026-10-13 (20:17Z): pedido do Gustavo: "pegue 200 conceitos aleatórios e deixe pro freellmapi, pra ir mais rápido".
  `triagem_conceitos_freellm.py` sorteou 200 (semente fixa) entre as posições da fila que a Osmose ainda não pegou
  (`etapas/conceitos/freellm-reservados.json`) e os tria com 1 modelo cada, pelo despachante; grava a resposta no mesmo
  lugar e formato dos subagentes (`respostas/<slug>.json`, com `"via": "freellmapi"`). A Osmose pula os reservados.
- 2026-10-13 (20:25Z): Haiku sites concluídos pelo Tear: 383 itens em 6 levas (77 subagentes), **5,24 milhões de
  tokens**, 0 erros. Os 200 conceitos do FreeLLMAPI ficaram prontos em 7 min (20:17 a 20:24Z). Fila final da
  conferência refeita: **1063 itens** (431 dúvida, 269 divergentes, 191 busca, 172 stack; 465 repositórios e 598
  sites); 110 já conferidos. Conceitos: 456 de 874.
- 2026-10-13 (~21:30Z): **etapa 2 (triagem) concluída.** Conceitos: 874 de 874 (200 pelo FreeLLMAPI, o resto pelos
  Haiku da Osmose, 2,19 milhões de tokens mais o piloto, 0 erros). Vereditos dos conceitos: 546 busca, 168 stack,
  58 nada, 153 dúvida; os mais comuns em inglês: hybrid search (67), bm25 (26), frontmatter filtering, stemming,
  metadata filtering, vector search, portuguese stemming. 51 arquivos gravados com slug errado (cópias a mais;
  todos os 874 têm a resposta certa) foram movidos para `conceitos/respostas-fora-da-fila/`. Osmose limpa com
  `/clear` (pela CLI, com `MSYS_NO_PATHCONV=1`, porque o Git Bash transforma "/clear" em caminho). Conferência: 510 de
  1063.
- 2026-10-13: "osmose também entra": a Osmose confere os 151 itens do meio da fila (posições 457 a 611 de 1063,
  `etapas/conferencia/fila-osmose.json`), entre a Salina (do início) e o Tear (do fim). Faltavam 453.
- 2026-10-13: o Tear passou de 80% de contexto (o teto do Gustavo é 40%). Parou depois da leva 4 (400 itens do fim,
  ~4,6 milhões de tokens), levou `/clear` e retomou do fim pulando a parte da Osmose. Regra nova para os três
  despachantes: nenhuma leva nova acima de 40% de contexto; eles avisam e param. Conferência: 810 de 1063.
- 2026-10-13 (~22:10Z): **etapa 3 (conferência) concluída**: 1063 de 1063, 0 erros; Salina 400 (início), Tear 531
  (fim), Osmose 151 (meio), ~9 colisões sem sobrescrita. **14,2 milhões de tokens Sonnet** (13,4 mil por item; o piloto
  mediu 9,5 mil; a diferença não foi investigada). Resultado: 496 rejeita, 357 corrige, 210 confirma; registro final:
  529 nada, 286 busca, 248 stack. Nos 286 de busca, o README raramente diz MCP (13 sim, 50 não, 223 não diz), Windows
  (42 sim) e português (34 sim). 19 respostas gravadas em cp1252 foram convertidas para UTF-8. Os três despachantes
  levaram `/clear`. Rodada na nota: auditoria.
- 2026-10-13: auditoria: **A**. `preparar_auditoria.py` sorteou 195 itens (semente fixa, estratificado): 107 da
  conferência por resultado e fonte, 88 dos conceitos por veredito. Prompt em `etapas/auditoria/prompt.md`
  (concorda / discorda, gravidade, registro final). O maestro dispara os subagentes Opus; piloto de 1 subagente com 5
  itens antes (se passar de 30% acima dos ~2,7 milhões estimados, volta à nota).
- 2026-10-13: auditoria, piloto (1 Opus, 5 itens, 64 777 tokens) e leva 1 (19 Opus, 95 itens, **1 402 977 tokens**,
  14,8 mil por item; ~5 min). Erro do maestro: soltou a leva 1 sem mostrar antes o número do piloto ao Gustavo (a regra
  dispensava a pergunta, não o aviso). Resultado parcial: dos 98 da conferência auditados, o Opus concorda em 66 e
  discorda em 32 (29 leves, 3 graves: cartão quebrado de kin-openapi, nats.rs marcado útil, Whoosh rejeitado por
  engano). A leva 2 (9 da conferência e 86 conceitos, ~1,4 milhão) espera o ok do Gustavo. Também parada a vigia do
  Tear, que rodava à toa havia mais de 100 min.
- 2026-10-13: ok do Gustavo (no terminal) para a leva 2 da auditoria (lotes 19 a 37).
- 2026-10-13: **etapa 4 (auditoria) concluída.** Leva 2: 19 Opus, 95 itens, 1 095 930 tokens. Total da auditoria:
  **2 563 684 tokens Opus** (piloto 64 777 + leva 1 1 402 977 + leva 2 1 095 930), abaixo dos 2,7 milhões aprovados.
  Conferência (107 auditados): o Opus concorda em 73 e discorda em 34; só **3 graves (2,8%)**, os 31 restantes são
  campos secundários. Conceitos (88 auditados, sem conferência antes): concorda em 51, discorda em 37, **11 graves
  (12,5%)**, quase todos conceitos marcados úteis sem servir ao hub (Groq, Flink, ArangoDB, type hints, logging do
  Tornado), um modelo só em inglês sem dúvida marcada e dois cartões quebrados. Leitura: a cadeia Haiku/FreeLLMAPI →
  Sonnet → Opus é confiável nos projetos; a triagem de conceitos sem fonte primária é generosa e pede filtro na síntese.
- 2026-10-13: o Gustavo achou rasa a proposta da síntese ("precisam estar à altura de todo o trabalho executado até
  aqui"). Refeita em [`proposta-50-sintese.md`](../prototipos/proposta-50-sintese.md) a partir dos dados: as candidatas
  atuais (zvec-grep, memtomem, ck, markdown-vault-mcp, grooveseek...) não estão no catálogo; a régua (MCP, Windows,
  português) é "não se sabe" em ~80% dos projetos de busca; os lugares próprios do hub (dentro do MCP do banco, cópia
  leve no cliente) têm 0 e 2 itens; há duplicatas de entidade; na comparação das metades, dois modelos gratuitos que
  concordam acertam 83% e o Haiku 75%. Proposta: S1 consolidar, S2 fechar a lacuna de atualidade com busca na web, S3
  verificar a régua nos finalistas, S4 síntese de arquitetura, S5 visual.
- 2026-10-13: plano da síntese **aprovado** pelo Gustavo ("agora sim aprovo"): S1 a S5 da
  [proposta](../prototipos/proposta-50-sintese.md); piloto mostrado antes de cada leva de subagentes.
- 2026-10-13: **S1 concluída** (`laco/consolidar.py`, saídas em `laco/sintese/`): 475 entidades úteis (240 busca, 235
  stack) depois de juntar chaves do mesmo projeto; os 31 grupos ambíguos foram decididos por 1 juiz Sonnet (50 821
  tokens); 292 conceitos entram (citados por 2+ cartões ou ligados a um projeto). S2 preparada: 10 temas estreitos
  (`sintese/s2-temas.json`), focados nos lugares que o laço não cobriu e no que mudou desde a varredura de 04/10
  (27 candidatas já conhecidas ficam fora da repetição); subagentes Sonnet com WebSearch e WebFetch, fonte primária com
  citação. Piloto: 2 temas (busca dentro do CouchDB; BM25 em português).
- 2026-10-13: piloto S2 (2 subagentes Sonnet com web): **126 635 tokens** (61 378 e 65 257; ~63 mil por tema, ~1,5 min),
  12 achados com citação. CouchDB: Nouveau (Lucene 10, CouchDB 3.5.2) e Clouseau têm analisador de português; não há busca
  vetorial no CouchDB; Windows do Nouveau não verificado (instalação só para Linux, Java 21). BM25 em português: SQLite
  FTS5, Tantivy, Lucene, Xapian e Bleve com fonte; Meilisearch v1.55 e Typesense sem português conferido. Conta dos 8
  temas restantes: ~0,5 milhão (a estimativa da proposta era de 2 a 4 milhões para S2).
- 2026-10-13: ok do Gustavo; os 8 temas restantes da S2 saíram (8 subagentes Sonnet com web).
- 2026-10-13: **S2 concluída**: 10 temas, 80 achados com citação em `laco/sintese/s2/`, **730 984 tokens Sonnet**
  (~73 mil por tema). Destaques: dentro do CouchDB, Nouveau e Clouseau têm analisador de português, mas não há vetor;
  qmd tem Windows desde a 2.5.2; ck 0.8.1 tem binário Windows, mas sem busca semântica nele; markdown-vault-mcp 5.1 aceita
  endpoint OpenAI-compatível; há proxies MCP leves para o "MCP do banco repassando" (mcp-proxy, TBXark, 1MCP, FastMCP
  mount); o MTEB-BR põe o EmbeddingGemma-300m como melhor pequeno em português; Pagefind e Orama servem à cópia leve.
  S3 preparada: 36 finalistas em 9 lotes de 4 (`sintese/s3-lotes.json`, régua em `s3-instrucoes.md`); piloto de 1 lote.
- 2026-10-13: piloto S3 (1 Sonnet com web, 4 itens): **103 919 tokens** (~26 mil por item, ~3 min). memtomem: alpha, mas
  com CI no Windows e endpoint OpenAI-compatível; qmd: Windows não verificado (CI só Ubuntu e macOS) e sem endpoint
  OpenAI para embeddings; ck: sem endpoint OpenAI (só Mixedbread ou local); grepai: Windows, watcher e endpoint
  configurável, mas sem commit desde 10/09. Conta dos 8 lotes restantes: ~0,83 milhão Sonnet.
- 2026-10-13: "solte os 8": os 8 lotes restantes da S3 saíram (8 Sonnet com web, 32 finalistas).
- 2026-10-13: S3 quase concluída: 33 arquivos de régua com citação em `laco/sintese/s3/` (tabela compacta em
  `sintese/regua.md`); um lote foi repetido por engano de índice (Tantivy em dobro) e o lote de FastEmbed, Meilisearch,
  Typesense e Qdrant foi relançado em 1 subagente. Tokens S3 até aqui: 103 919 (piloto) + 8 lotes (66 405, 69 844,
  70 361, 95 401, 82 913, 87 549, 118 003, 123 860).
- 2026-10-13: **S3 concluída** (36 finalistas, **898 723 tokens Sonnet**, incluído o lote relançado). **S4 escrita:**
  [`pesquisa-50-sintese.md`](../../../exploracao/anexos/pesquisa-50-sintese.md). Principais pontos:
  - a busca nativa do CouchDB não enxerga o texto (pedaços e E2EE do LiveSync), então "dentro do MCP do banco" é um
    índice do próprio MCP alimentado pelo `_changes`;
  - nenhuma ferramenta pronta cumpre a régua inteira, e as que mais se aproximam (obsidian-hybrid-search, memtomem)
    não têm stemmer de português no BM25;
  - combinações C1 (disco), C2 (disco + repasse na tailnet), C3 (índice no MCP do banco), C4 (cópia leve para sandbox)
    e C5 (reserva);
  - recomendação: spike obsidian-hybrid-search contra memtomem, e o resultado decide entre C2 e C3.
  S5: página do Designer pedida.
- 2026-10-13: pouca memória na máquina; a pedido do Gustavo ("pode liberar"), dispensados Tear, Osmose e Salina, e parado o serviço do despachante (a triagem acabou). Fica só o serviço do painel (`painel_etapas.py`). Memória livre depois: 1,2 GB de 15,7.
- 2026-10-13, ponto de retomada (antes do `/clear` do maestro):
  - **Feito:** etapas 1 a 4; S1 a S4 da síntese. Síntese em `exploracao/anexos/pesquisa-50-sintese.md`.
  - **Em curso:** S5. O Designer faz `laco/painel/sintese.html` e avisa o maestro por `maestri ask`.
  - **Quando o aviso chegar:**
    1. marcar a etapa 5 como `feita` em `laco/etapas/marcos.json`, com a parte "página do Designer" em 1/1;
    2. pedir ao Designer que a usina (`etapas.html`) mostre a água potável no copo, com link para `sintese.html`.
  - **Depois, com o Gustavo:**
    - dar este ticket como resolvido, se ele quiser: Answer, linha no mapa e atualização do system design pelo
      Designer;
    - abrir a rodada da "Camada de busca": spike obsidian-hybrid-search contra memtomem; C2 ou C3.
  - **No canvas:** só o Designer. A nota "Rodada atual" está sem rodada. O serviço `painel_etapas.py` segue ligado.
- 2026-10-13: pergunta do Gustavo depois do `/clear`: "e a parte da stack? Só sobraram 36 finalistas mesmo? Nada foi
  perdido?" Conferido por script em `laco/sintese/`:
  - **Os 36 não saíram do catálogo.** Só 12 deles estão entre as 240 entidades de busca (Meilisearch, Qdrant, Typesense,
    OpenSearch, LanceDB, sqlite-vec, txtai, FastEmbed, Manticore, Orama, Pagefind, Obsidian Local REST API); os outros 24
    vêm da S2 e das pesquisas antigas. `s3-lotes.json` foi montado à mão, sem script nem critério gravado. **228 das 240
    entidades de busca não passaram pela régua com fonte**, entre elas Elasticsearch, FAISS, Weaviate, Milvus, Chroma,
    Lucene, Solr, Whoosh, pgvector, lunr.js, MiniSearch e FlexSearch. Nelas a régua segue quase toda "não se sabe" (MCP
    185, Windows 205 e português 200 de 240).
  - **A stack não teve etapa própria.** As 235 entidades de stack não tiveram S2 nem S3. A §4 da síntese cita cerca de 29
    delas, numa lista feita à mão. O registro delas usa os campos da busca (`mechanism` é "other" ou "n/a" em 197 de 235),
    então não há classificação por área do hub (sync, MCP, frontmatter, texto em português, embeddings, extração).
  - **A junção de entidades ficou incompleta:** Weaviate aparece 7 vezes, Lucene 14 vezes e Whoosh 5 vezes. Então "475
    entidades" está inflado.
  - **Nada foi apagado.** Os dados estão em `catalogo-final.json`, e o que caiu foi por regra registrada: 1032 só-nome
    (por decisão do Gustavo), 193 em quarentena, 620 repositórios inventados, 212 mortos, 529 "nada" e 340 grupos de
    conceito com uma citação só. A perda é de **cobertura**: o que existe no catálogo não chegou à síntese.
- 2026-10-13: **S5 entregue** pelo Designer: `laco/painel/sintese.html` ("laudo de potabilidade"; finalistas como tabela
  periódica; conferida no Edge headless, claro e escuro). Etapa 5 marcada como feita em `laco/etapas/marcos.json`. Pedidos
  ao Designer: (1) a usina (`etapas.html`) mostra a água potável no copo, com link para `sintese.html`; (2) correção do
  funil da seção 06, que ia de 5526 a 36: ele termina em 475, e os 36 têm duas entradas (12 do catálogo e 24 da varredura
  com web). Também avisa da lacuna da régua (228 de busca e 235 de stack). O ticket só vira resolvido depois da rodada
  sobre a cobertura.
- 2026-10-13: rodada da cobertura respondida: **A, aprovado.** São 4 passos:
  1. terminar a junção de entidades, por script e com juiz Sonnet nos casos difíceis;
  2. classificar a stack por área do hub, pelo FreeLLMAPI, com 2 modelos concordando;
  3. gerar um inventário completo em anexo, por script;
  4. conferir a régua com fonte em uma segunda lista de ~50 itens (~1,3 milhão de tokens Sonnet), com piloto mostrado
     antes da leva.

  Depois, reescrever as seções de busca e de stack da síntese. O ticket só é resolvido ao fim disso.
- 2026-10-14 (~01:05Z): **cobertura, passo 1 (junção) concluído.** `laco/juntar_entidades.py` agrupa candidatas por
  repositório comum e por nome contido. Na primeira rodada do juiz Sonnet (65 mil tokens), o candidato não listava a
  entidade mais citada entre os membros, e ela ficou de fora em 19 grupos. A rodada foi descartada
  (`entidades2-decisoes-v1-sem-mae.jsonl`) e refeita com o formato corrigido (74 mil tokens). Ajustes do maestro em
  `sintese/entidades2-ajustes.json`: NATS com o nats-server como principal, 2 junções e 13 nomes corrigidos.
  Resultado: **475 → 353 entidades (169 de busca, 184 de stack)**, em `sintese/catalogo-entidades.json`.
  Exemplos: Elasticsearch com 25 componentes, Lucene com 6, Weaviate com 6. Teto do despachante renovado: 11400
  tentativas ou 3 h, a partir de 00:55Z. Piloto da classificação da stack: 5 itens, 13 tentativas, 5 de 5 em acordo.
- 2026-10-14 (~01:15Z): **cobertura, passos 2 e 3 concluídos.**
  - **Passo 2.** As 184 entidades de stack foram classificadas pelo FreeLLMAPI (`laco/classificar_stack.py`, prompt em
    `etapas/stack/prompt.md`), em ~10 min e sem custo Claude. 178 ficaram em acordo e 6 divergentes (sem maioria de 3).
    Por área: Markdown e frontmatter 32, bancos 23, português 21, sync/CouchDB 18, embeddings 18, eventos e vigias 14,
    extração 12, MCP 10, frameworks de agente 9, modelos locais 8, Obsidian 6, API 1, outros 6. Saída em
    `sintese/stack-areas.json`. O encaixe dado pelos modelos é generoso: 94 "central", com DistilBERT e nanomsg entre eles.
  - **Passo 3.** `laco/inventario.py` grava o anexo
    [`pesquisa-50-inventario.md`](../../../exploracao/anexos/pesquisa-50-inventario.md): 169 de busca, 184 de stack por
    área, 23 finalistas que vieram de fora, 292 conceitos e o que ficou fora, com a regra. Ele é refeito quando a régua
    nova chegar.
  - **Nomes errados.** Os nomes vêm da memória dos modelos, e vários não batem com a URL. Exemplos: "Local Search
    Engine" é o Bleve, "PageAssist" é o GPT4All e "pt" é o The Platinum Searcher. 5 foram corrigidos em
    `entidades2-ajustes.json`, e a régua nova confere a identidade pela URL.
- 2026-10-14: **passo 4 preparado.** `laco/selecionar_s6.py` monta a lista por regra (a regra está em
  `sintese/s6-lista.json`):
  - **busca:** as 20 mais citadas sem régua, tirando os serviços só na nuvem, mais as dos lugares vazios (dentro do
    MCP do banco, cópia leve, grep no disco);
  - **stack:** as 3 mais citadas de cada área com encaixe "central" unânime, tirando o que já está decidido, o
    Node.js, o DistilBERT e o fastText.

  São 55 itens (27 de busca e 28 de stack) em 14 lotes de 4. Instruções em `sintese/s6-instrucoes.md`. Piloto: o lote
  6, que mistura busca e stack, com 1 Sonnet.
- 2026-10-14 (~01:25Z): piloto da régua nova (1 Sonnet com web, lote 6: ripgrep-all, Zoekt, The Silver Searcher e
  spaCy): **83 777 tokens (~21 mil por item)**, ~2,3 min, 4 de 4 arquivos com citação em `sintese/s6/`. A identidade
  pela URL funcionou: a URL do spaCy estava errada, e o projeto certo é explosion/spaCy. Conta dos 13 lotes restantes
  (51 itens): ~1,1 milhão de tokens Sonnet, ~1,2 milhão com o piloto, abaixo do 1,3 milhão aprovado. A leva espera o ok
  do Gustavo (rodada na nota).
- 2026-10-14: ok do Gustavo ("aprovado", no chat): soltos os 13 lotes restantes da régua nova (lotes 0 a 5 e 7 a 13),
  com 13 Sonnet com web.
- 2026-10-14 (~01:50Z): **cobertura, passo 4 concluído.** Os 13 lotes da régua nova voltaram com 55 de 55 fichas
  em `sintese/s6/`, sem chave faltando nem repetida. Tokens Sonnet: **1 039 521 com o piloto** (~19 mil por item),
  abaixo do 1,3 milhão aprovado. A API do GitHub limitou vários subagentes, e as datas vieram de feeds e tags ou
  ficaram NV. O MCP do Weaviate, que veio só de resumo de busca, foi rebaixado pelo maestro a NV. O inventário foi
  refeito, com a seção 5 "A régua com fonte, em resumo" (92 fichas, as da S3 e as da S6). No catálogo, 40 de 169
  entidades de busca e 28 de 184 de stack agora têm régua.
- 2026-10-14: **síntese reescrita** (`exploracao/anexos/pesquisa-50-sintese.md`):
  - cabeçalho com o inventário;
  - resumo com o que a segunda régua mostrou;
  - tabela de etapas com as linhas da rodada de cobertura;
  - §2.3 com os mais citados do catálogo;
  - §2.4 e §2.5 com as peças de português e os lugares;
  - C3 com Bleve, Lucene.NET, Xapian, FAISS, hnswlib e lingua-py conforme a linguagem do MCP;
  - **§4 refeita por área**, com o que a régua confirmou e o que é só README;
  - aprendizados e limites.

  A recomendação não muda: teste obsidian-hybrid-search contra memtomem, e o resultado decide entre ferramenta
  pronta no disco com repasse e índice dentro do MCP do banco. Falta a página do Designer.
- 2026-10-14: pedido ao Designer para refazer `laco/painel/sintese.html`, juntando os dados novos da cobertura e o
  retorno do Gustavo sobre a versão "laudo": muita informação, fonte de que ele não gostou, texto demais;
  "simplificar não é cortar info, é comunicar a mesma coisa porém de uma melhor forma". A ideia central e a
  tipografia vão ser repensadas, com diagramas e o detalhe em camadas.
- 2026-10-14: **página da síntese refeita pelo Designer** (`laco/painel/sintese.html`). A versão "laudo" foi guardada no
  scratchpad do Designer.
  - **Ideia central:** um mapa do hub, no espírito do metrô. As zonas são máquina, tailnet e sandbox; os 6 lugares
    aparecem como pinos; as combinações, como linhas coloridas.
  - **Forma:** fonte Segoe UI Variable e detalhe em camadas (hover, expansores e links para o inventário).
  - **Seções:**
    1. mapa e matriz de atendimento;
    2. os caminhos numa régua de dias;
    3. a régua em 6 faixas de veredito, com os itens do catálogo marcados;
    4. a stack num treemap das 12 áreas;
    5. a decisão em fluxograma;
    6. o funil até a junção (475 → 353) e os aprendizados.

  O Designer apontou duas divergências, corrigidas na fonte:
  - a tabela de etapas agora diz "12 no catálogo; 13 e 23 depois da junção (Tantivy)";
  - o inventário diz "92 arquivos, 91 itens", porque o Tantivy tem duas fichas na S3.
- 2026-10-14: o Gustavo recusou a v2 da página ("mande o designer se reinventar e fazer um design completamente
  diferente, ele só mudou a estilização"). O Designer levou `/clear`, porque estava preso às versões anteriores, e recebeu
  um briefing completo: a v2 como referência do que não repetir, as 7 informações essenciais, nenhuma informação
  perdida, pouco texto visível e tipografia nova. A rodada "damos a pesquisa por resolvida?" segue aberta na nota.
- 2026-10-14: **v3 da página pelo Designer: "Super Trunfo da busca"**, uma mesa de cartas (`laco/painel/sintese.html`).
  - **Forma:** o duelo Leve com alcance × Robusta no centro, com o teste obsidian-hybrid-search × memtomem no meio, a vaga
    do troféu ("Gustavo decide") em cima e os 3 fatos a confirmar como cartas viradas.
  - **À esquerda:** a regra da casa (a descoberta) e o placar de 6 lugares × 5 situações, com filtro.
  - **À direita:** as outras cartas e o descarte.
  - **Embaixo, "o baralho que levou à resposta":** a régua, a stack e o funil.
  - Ao clicar, a carta abre ampliada, com peças, falta montar, ganhos, riscos e o que o teste prova.
  - **Fonte:** Bricolage Grotesque + DM Mono; mesa de linho no claro, feltro no escuro; versão de celular conferida.
  - A v2 ficou guardada no scratchpad do Designer.
- 2026-10-14: **resolvido** pelo Gustavo ("sim considere como concluída, mas não inicie nada"). Ele continua em outra
  sessão. Ficam para depois, sem começar agora:
  - atualizar o System design pelo Designer;
  - abrir a rodada da "Camada de busca" (teste de bancada e os 3 fatos).

  Limpeza: parado o serviço do painel, a nota "Rodada atual" esvaziada e o Designer liberado.
