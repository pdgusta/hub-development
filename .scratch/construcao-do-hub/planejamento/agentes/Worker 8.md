# Worker 8: notas

## Volta 1 (2026-10-15)

**Faixa assumida: 8, portas dos harnesses e kit de par** (linha do Worker 8 no `plano.md`). Comecei pela vigia, mas o
Worker 2 já tinha gravado um corte em 10 faixas em que a vigia é a faixa 7 e o kit é a 8; fiquei com a 8 para manter
"faixa N = Worker N" e não colidir com o Worker 7. O que pensei da vigia ficou abaixo como proposta ao Worker 7, e o
contrato do estado da vigia foi para "Fronteiras combinadas".

### Faixa 8: o que conferi nas decisões

- Answer do 14: contrato por link simbólico, skills por junction, hooks no escopo do usuário (no Codex aprovados por
  hash em `hooks.state`; no Copilot só hook de usuário), Codex com `danger-full-access` e `notify`, MCP do hub aprovado
  de antemão (`default_tools_approval_mode="approve"`), MCP do par em 127.0.0.1 com token de variável de ambiente, o
  kit roda o teste mínimo do sandbox elevado a cada atualização do Codex e avisa quando passar.
- Answer do 42: link simbólico pede o modo de desenvolvedor; link físico se solta; editar só dentro do hub.
- Answer do 15: o kit tira o GSD do escopo global, com cópia antes. **Isso supera** o "juntar com o GSD" no
  `~/.copilot/copilot-instructions.md` (Answer do 42 e comentário de 2026-10-12 do 16): com o GSD fora, o arquivo vira só
  o link. A conferir pelo Prumo.
- Comentários do 16: o kit confere que não há `CLAUDE.md` no hub nem acima; o marcador de raiz e o
  `project_root_markers` saíram (2026-10-15); `claude-md-and-agents-md` no Maestri de cada par.
- Answer do 18: o `COPILOT_HOME` desliga `~/.agents/skills`. **Risco para o ensaio:** testar skills do Copilot com
  `COPILOT_HOME` de ensaio não prova a junction; o ensaio precisa trocar o HOME inteiro (`USERPROFILE`) para o Copilot,
  não só o `COPILOT_HOME`. Não verificado se o Copilot CLI respeita `USERPROFILE` trocado.
- Não verificado: `CLAUDE_CONFIG_DIR` como HOME de ensaio do Claude Code e onde o Claude Code guarda MCP de usuário e
  mods dentro dele; ler a fonte primária antes de construir.

### Vigia (proposta ao Worker 7): o que a faixa entregaria

1. `vigia` (um comando, uma passada): lê o CouchDB local e grava o estado. Confere, como no Answer do 33:
   - replicações pelo `_scheduler/docs` (parada há mais de 15 min com o outro par ligado = divergência; outro par
     desligado = só informa a hora da última troca);
   - conflitos abertos (texto) e binários descartados (ramo apagado pela resolução por `mtime`);
   - arquivos acima de 200 MiB no disco (não viajam);
   - sincronizador vivo (o CLI do LiveSync) e o Config Doctor travando o plugin.
2. Estado curto num arquivo local que não replica (proposta abaixo), lido pela checagem de início de sessão.
3. Notificação do Windows **só quando o estado piora** (compara com a passada anterior).
4. `vigia recuperar <caminho>`: grava a versão perdida de um binário num arquivo ao lado (R71).
5. Mod do Claude Code que mostra o estado o tempo todo (forma: linha de status ou faixa acima do prompt, a escolher na
   construção) e o script de `statusLine` do Copilot; no Codex, nada a mais (checagem de início + notificação).
6. A tarefa agendada (a cada 5 min) como XML pronto. **Registrar a tarefa de verdade é `ready-for-human`.**

### Como segue sem esperar ninguém

- **Banco (CouchDB + LiveSync), de outra faixa:** não espero o par montado. Uso um CouchDB de ensaio só meu (porta de
  teste, dados descartáveis) ou um dublê HTTP com respostas gravadas. Base pronta: a montagem do spike em
  `C:\Projetos\spike-livesync\` (compose, `cdb.py`, `tarefa-cli.xml`); o ticket 48 já recuperou um ramo apagado de
  binário por script. Usar a montagem do spike como fonte de fixture, sem ligar o que estava parado sem aval: a
  combinar com o Prumo 2.
- **Hooks de início de sessão e ferramenta reserva do MCP, de outras faixas:** só leem o arquivo de estado. Contrato
  proposto abaixo; quem os constrói usa um arquivo de exemplo, sem esperar a vigia.

### Contrato proposto: o estado da vigia

- Caminho: `C:\context-hub\.local\vigia\estado.json` (pasta com ponto: não replica, pela regra de exclusão do
  LiveSync; e o que não replica não divide pasta com o que replica). **Proposta minha, não decidida no mapa.**
- Esquema (versão 1):

```json
{
  "versao": 1,
  "gerado_em": "2026-10-15T21:40:00-03:00",
  "maquina": "par-a",
  "nivel": "ok | informa | divergencia",
  "resumo": "uma linha para o mod e a statusLine",
  "outro_par": "ligado | desligado | desconhecido",
  "ultima_troca": "2026-10-15T21:35:00-03:00",
  "itens": [
    {"tipo": "conflito | sync-parado | binario-descartado | arquivo-grande | sincronizador-parado | config-doctor",
     "caminho": "relativo à raiz do hub, quando houver",
     "desde": "ISO 8601",
     "detalhe": "texto curto"}
  ]
}
```

- Escrita atômica (grava em `estado.json.tmp` e renomeia), para quem lê nunca pegar meio arquivo.

### Critério de aceite (verificável dentro da hora)

Seis cenários de ensaio produzem o estado esperado: tudo em ordem; conflito aberto; replicação parada há mais de
15 min com o outro par ligado; outro par desligado (só `informa`); binário descartado; arquivo acima de 200 MiB. A
notificação sai só na passada que piora (notificador dublê no teste automático; uma notificação real à vista do
Gustavo, se ele quiser). `vigia recuperar` grava a versão perdida ao lado com os bytes iguais aos do ramo apagado.

### Não verificado

- O formato exato dos documentos do LiveSync para achar o ramo apagado de binário (o ticket 48 fez, a ler na fonte).
- Como detectar "o Config Doctor travou o plugin" sem o Obsidian aberto.
- A API de mods do Claude Code para a faixa acima do prompt (ticket 44 cita mods; conferir na fonte antes de usar).

### Para a próxima volta

- Fechar com os donos das faixas 3 e 5 (URL e token no `.env.modelo`) e das faixas 2, 6, 7 e 9 (formato do fragmento
  de hook e do mod), por `maestri ask`, e com o Worker 7 o caminho e o esquema do estado da vigia.
- Conferir se a faixa 8 cabe na hora: são três harnesses vezes contrato, skills, MCP e hooks, mais a retirada do GSD;
  dividir por harness entre subagentes.

### Meu corte inicial (antes de ver o do Worker 2; quase igual, ficou o dele)

1. raiz e contrato (seis raízes, `AGENTS.md`, `agents/`, esquemas de frontmatter, `.git`, sem `CLAUDE.md`);
2. banco do par A (CouchDB + sincronizador CLI, exclusão `**/.*`, 200 MiB, `mark-resolved`);
3. MCP do banco (fork do es617 com `base_rev`, conflito visível, `instructions` com a cabeça do `AGENTS.md`);
4. busca (obsidian-hybrid-search com o arctic local, MCP HTTP em 127.0.0.1);
5. hooks dos três harnesses em HOME de ensaio (início, fim, recusa antes da ferramenta, frontmatter);
6. kit de par em HOME de ensaio (links do contrato, junctions, import, modo de desenvolvedor);
7. replicação entre dois CouchDB e kit de cliente (mcp-proxy com rotas e tokens);
8. **vigia** (esta faixa);
9. acervo do maestro e roteamento de skills (família `maestro-*`, guarda, `routing.yml`, hook de entrada);
10. manutenção (`_archive/` com 30 dias, cópia diária no GitHub, verificador de frontmatter, `index.md` com resumo).

## Volta 2 (2026-10-15)

**Fiz:** reescrevi a linha da faixa 8 para caber na hora. A spec (`spec-partes/faixas-07-08.md`) tem 42 histórias;
na hora entra um núcleo de sete partes, em ordem, depois um segundo bloco se o núcleo passar até o min 35, e o resto
vai para "Fica para outra execução". Absorvi e apaguei do plano os itens da faixa 8 do Prumo (sandbox elevado,
`claude-md-and-agents-md`) e do Prumo 2 (trava do HOME real, prova ao vivo dependente do login). Aceitei o `.env`
por fragmento (`kit/par/env/<nn>.env`) do Prumo 2. Fixei os nomes `hub-busca` e `hub-banco` (a faixa 6 precisa trocar
`mcp__busca__*`). Pergunta ao Gustavo: o GSD no arquivo global do Copilot (15 contra 36/42).

**HOME de ensaio por harness (o que sustenta a prova):**
- Claude Code: `CLAUDE_CONFIG_DIR` muda o `~/.claude` inteiro ("All settings, session history, and plugins are stored
  under this path", code.claude.com/docs/en/env-vars, citado em `exploracao/anexos/pesquisa-13-acesso-dos-agentes.md`).
  Sem login no ensaio, `claude -p --settings ... --mcp-config ...` prova hooks e MCP (Prumo 2, `claude --help`).
- Codex: `CODEX_HOME` muda `~/.codex` (contrato, `config.toml`). Mas `~/.agents/skills` vem do `home_dir()` da crate
  `dirs` (`codex-rs/ext/skills/src/host_roots.rs`, citado na pesquisa 13). Não verificado se no Windows ela segue
  `USERPROFILE` (minha lembrança é que usa a API de pasta conhecida, que não segue; **não verificado**).
- Copilot: `COPILOT_HOME` muda `~/.copilot` inteiro, mas desliga `~/.agents/skills` (changelog v1.0.66, pesquisa 18).
- Consequência: a junction em `~/.agents/skills` só se prova na forma no ensaio; ao vivo, só na instalação de
  verdade (`ready-for-human`).

**Não verificado, a ler na fonte antes de construir:** onde o Claude Code guarda o MCP de usuário com
`CLAUDE_CONFIG_DIR` (o `.claude.json`); onde lê mods; a forma do nome de ferramenta MCP no Codex e no Copilot; o
formato do `hooks.state` do Codex (o ticket 14 cita, a bancada `bancada-acesso-codex.md` deve ter).

**Próxima volta:** conferir se a faixa 6 trocou o casamento para `mcp__hub-busca__*`, se as faixas 3 e 5 aceitaram
`kit/par/env/<nn>.env`, e se a 7 aceitou `codex.notify` e `copilot.statusLine` no fragmento.
