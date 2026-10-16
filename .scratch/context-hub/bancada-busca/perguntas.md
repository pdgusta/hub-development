# Teste de bancada da busca: perguntas

Ticket "Camada de busca" (R91). Corpus: cópia de `.scratch/context-hub/issues/`, `exploracao/` (com `anexos/`) e
`knowledge/armis-docs` do vault. **Esta pasta (`bancada-busca/`) fica fora do corpus.**

- **Tipo L (literal):** a pergunta usa palavras do texto.
- **Tipo P (paráfrase):** a pergunta evita as palavras do texto e testa sinônimos e a parte semântica.
- **Resposta certa:** um dos arquivos listados aparecer entre os 5 primeiros. A posição do primeiro acerto dá o
  MRR.
- **Amostra do Gustavo:** as marcadas com ✱ (10), conferidas antes de rodar.

| # | Tipo | Idioma | Pergunta | Arquivo(s) com a resposta |
|---|---|---|---|---|
| 1 | L | pt | Qual é o limite de tamanho de arquivo que vai ao banco no sync? | `issues/33-revisao-do-sync-e-da-divergencia.md` |
| 2 | L | pt | A verdade do hub mora no Markdown ou num banco? | `issues/22-markdown-vista-ou-fonte.md` |
| 3 ✱ | L | pt | O SQLite FTS5 tem stemmer de português? | `exploracao/anexos/pesquisa-50-sintese.md`, `issues/09-camada-de-busca.md` |
| 4 | L | pt | Por que o Tailscale SSH não serve como servidor no Windows? | `issues/05-ligar-as-maquinas-com-seguranca.md` |
| 5 | L | pt | Quais workloads piloto nascem no hub? | `issues/02-workloads-piloto.md` |
| 6 | L | pt | Quantas deploy keys o GitHub privado usa no ponto de encontro do sync? | `issues/06-ponto-de-encontro-do-sync.md` |
| 7 ✱ | L | pt | O LiveSync leva pastas com ponto aninhadas na varredura de partida? | `issues/48-teste-disco-e-banco-sem-o-obsidian.md` |
| 8 | L | pt | Quais famílias de embeddings o FreeLLMAPI serve? | `issues/09-camada-de-busca.md` |
| 9 | L | pt | Em que linguagem é o MCP do es617? | `issues/09-camada-de-busca.md` |
| 10 | L | pt | Quantos campos tem a nota de retomada? | `issues/10-contrato-file-first.md` |
| 11 | L | pt | Onde fica o contrato global do Copilot? | `issues/18-acesso-dos-agentes-copilot.md` |
| 12 ✱ | L | pt | O que o `COPILOT_HOME` desliga? | `issues/18-acesso-dos-agentes-copilot.md` |
| 13 | L | pt | De quanto em quanto tempo a vigia confere colisão e sync parado? | `issues/33-revisao-do-sync-e-da-divergencia.md` |
| 14 | L | pt | Quantos tokens Sonnet a conferência da pesquisa ampla gastou? | `exploracao/anexos/pesquisa-50-sintese.md` |
| 15 | L | pt | O turbovec é uma ferramenta de busca? | `issues/20-turbovec-na-camada-de-busca.md` |
| 16 | L | pt | Qual foi a melhor candidata nova na varredura de candidatas à camada de busca? | `issues/21-varredura-de-candidatas-a-camada-de-busca.md` |
| 17 | L | pt | O que o "Concat both" faz com o texto no LiveSync? | `issues/30-spike-couchdb-livesync.md` |
| 18 | L | pt | Quantos dias faltam para montar o Fast Note Sync? | `issues/29-spike-fast-note-sync.md` |
| 19 ✱ | L | pt | O que é o Mod. IT.04.02? | `armis-docs/README.md`, `armis-docs/guia-tecnico/README.md` |
| 20 | L | pt | Qual é o `toc_title` da variante pt-BR do guia técnico? | `armis-docs/guia-tecnico/esqueleto-ptbr.md` |
| 21 ✱ | P | pt | Se os dois computadores mexerem no mesmo parágrafo ao mesmo tempo, quem ganha e como fico sabendo? | `issues/08-divergencia-e-edicao-concorrente.md`, `issues/33-revisao-do-sync-e-da-divergencia.md` |
| 22 ✱ | P | pt | Por que a pesquisa embutida do servidor de base de dados não acha trechos das anotações? | `exploracao/anexos/pesquisa-50-sintese.md` |
| 23 | P | pt | Que caminho o texto faz de um computador até o outro? | `issues/25-como-a-verdade-viaja-entre-as-maquinas.md` |
| 24 | P | pt | Cada computador tem o seu próprio servidor ou existe um só no meio? | `issues/34-onde-o-servidor-mora.md` |
| 25 | P | pt | Como um assistente preso numa caixa isolada, sem rede privada, consulta o acervo? | `exploracao/anexos/pesquisa-50-sintese.md`, `issues/34-onde-o-servidor-mora.md` |
| 26 | P | pt | O que aprendemos com o sistema de anotações antigo? | `issues/01-licoes-do-vault.md` |
| 27 ✱ | P | pt | Por que o subsistema Linux do Windows ficou de fora? | `issues/04-windows-ou-wsl.md`, `issues/03-hub-no-wsl-comportamento.md` |
| 28 | P | pt | Como as instruções do projeto chegam a um assistente aberto numa pasta de dentro? | `issues/38-testes-das-portas-de-entrada.md`, `issues/36-portas-de-entrada-do-hub.md` |
| 29 | P | pt | Que jeitos conhecidos de arrumar diretórios foram estudados para o topo do acervo? | `issues/35-metodos-de-organizar-a-raiz.md` |
| 30 ✱ | P | pt | O que acontece quando um documento do Word muda nos dois lados ao mesmo tempo? | `issues/48-teste-disco-e-banco-sem-o-obsidian.md`, `issues/47-disco-e-banco-sem-o-obsidian-pesquisa.md` |
| 31 | P | pt | Como a empresa pode barrar as ferramentas externas no assistente do GitHub? | `issues/46-copilot-com-assinatura-enterprise-pesquisa.md` |
| 32 | P | pt | Por que o banco versionado ao estilo git ficou como plano B? | `issues/31-debate-sobre-o-dolt.md` |
| 33 | P | pt | Como impedir que um assistente mude a biblioteca de papéis sem a minha aprovação? | `issues/44-guarda-do-acervo-mods-e-hooks-pesquisa.md`, `issues/40-maestri-padrao-e-liberdade.md` |
| 34 | P | pt | Que tipos de peças prontas o orquestrador do canvas pode guardar? | `issues/43-acervo-do-maestro-pesquisa.md` |
| 35 | P | pt | Quantas tentativas e quantos itens produziu a rodada com os modelos gratuitos? | `exploracao/anexos/pesquisa-50-sintese.md`, `issues/52-montar-os-scripts-do-laco.md` |
| 36 | P | pt | Até quantas letras das orientações do servidor de ferramentas o assistente da Anthropic aceita? | `issues/37-portas-de-entrada-pesquisa.md`, `issues/41-contrato-pelo-mcp-pesquisa.md` |
| 37 ✱ | P | en | What happens to an agent write made from a stale revision in the CouchDB spike? | `issues/30-spike-couchdb-livesync.md` |
| 38 | P | en | Which proxy can merge two tool servers into one endpoint on the private network? | `exploracao/anexos/pesquisa-50-sintese.md`, `issues/14-acesso-dos-agentes-decisao.md` |
| 39 ✱ | P | en | How should I document settings already applied in a tenant before turning on provisioning? | `armis-docs/configuracoes-aplicadas/README.md` |
| 40 | P | en | Which small open embedding model scores best on Portuguese benchmarks? | `exploracao/anexos/pesquisa-50-sintese.md` |
