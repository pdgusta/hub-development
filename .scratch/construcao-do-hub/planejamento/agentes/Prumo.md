# Prumo (revisor das decisões): notas

## Volta 1 (2026-10-15)

Fiz: conferi o corte candidato em 10 faixas (Worker 2) e as linhas dos Workers 1, 2 e 8 contra o `map.md`
("Decisions so far") e os Answers de 02, 09, 10, 11, 12, 14, 15, 25, 33, 34, 36, 40, mais os comentários do ticket 16.
Gravei no `plano.md` a seção "Conferência das decisões (Prumo)": o que nenhuma faixa pega, o que contraria decisão e as
decisões que caíram (para ninguém construir).

### Inventário das decisões que viram construção (fonte por ticket)

- 12: `AGENTS.md` + seis raízes + `_archive/`; `agents/` = `skills/`, `machines/<máquina>.md`, `maestro/propostas/`,
  `maestro/uso/<máquina>.md`, `blocks.md`, `frontmatter/` (`paths.yml` + esquema por tipo, 28 tipos em
  `rascunhos/12-frontmatter-proposta.md`); núcleo de seis arquivos; skill "nova iniciativa" por script (só muda com
  aval); hook antes da gravação recusa fora do esquema (3 harnesses); MCP valida igual; verificador sem IA no fim
  preenche o derivável; `index.md` cartão (`summary: auto`, `local`), criado a 10 arquivos ou com arquivo que a busca
  não lê; `.pdf.md` irmão; links `par://`; script gera a exclusão do sync e da busca (ponto no nome e `local: true`);
  `.obsidian-hybrid-search.db` fora do git e do LiveSync; teste `.secrets/` aninhado antes do primeiro segredo.
- 10: regra no contrato global; fim da resposta confere a nota e a memória privada; início abre a nota.
- 14 (refina 10): fim da resposta no Claude Code é **mod** (`turn.start` + `classic.Stop`); Copilot `agentStop` +
  extensão `onAgentStop` (`--experimental`); Codex hook `Stop`. Início: hook lê o arquivo da vigia; sem ele, ferramenta
  do MCP; cliente, ferramenta do MCP. Estado da vigia: mod (Claude Code), `statusLine` (Copilot), checagem + `notify`
  (Codex). Codex `danger-full-access` + teste mínimo do sandbox elevado a cada atualização; hooks aprovados por hash em
  `hooks.state`; `default_tools_approval_mode="approve"`. MCP do par em 127.0.0.1 com token de variável; cliente pelo
  TBXark/mcp-proxy na tailnet: `/busca/mcp`, `/banco/mcp` (leitura), `/banco-escrita/mcp`.
- 11: troca de trecho no disco; regravação inteira só pelo `write_note` com versão lida; hook recusa regravação inteira
  no disco; arquivo novo no disco; aviso (sem recusa) de leitura fora da busca, uma vez por arquivo por sessão; banco
  fora → regravação espera, anotada na retomada. Desktop: pasta conectada no Cowork com "Folder instructions" +
  MCP com escrita pela ponte `mcp-remote` + busca. Cliente: gravação ligável (segunda instância com escrita).
- 09/54: obsidian-hybrid-search + arctic-embed-m-v2.0 local, `ohs serve` em 127.0.0.1; gemini pelo FreeLLMAPI
  configurado, testado uma vez num índice ao lado, desligado.
- 25/34/33/47/48: CouchDB em cada par; replicação mestre-mestre (cada par empurra as próprias mudanças); fork do es617
  com `base_rev` e conflito visível (obrigatório antes de usar); duas instâncias do MCP por par (READ_ONLY + escrita);
  sincronizador = CLI do LiveSync como tarefa agendada (logon, repete, instância única, `mark-resolved`, antes do
  plugin); `syncMaxSizeInMB` 200 no CLI e no plugin; exclusão `**/.*` e `**/.*/**`; testar pastas com ponto e >50 MiB;
  E2EE, Setup URI e frase-senha por canais separados; GitHub = cópia diária (ramo por máquina, só commit e push).
  Vigia a cada 5 min: `_scheduler/docs`, conflitos, binários descartados, >200 MiB, sincronizador vivo, Config Doctor;
  notificação; estado curto; comando de recuperar binário.
- 36/42: sem `CLAUDE.md` no hub nem acima; import no `~/.claude/CLAUDE.md`; symlink `~/.codex/AGENTS.md` e
  `~/.copilot/copilot-instructions.md` (juntando com o GSD); junctions; modo de desenvolvedor; script do `_archive/`
  conferindo o outro par; `instructions` do fork com a cabeça ≤2.000 caracteres; regra curta nas descrições de gravação;
  kit de cliente com `--allow-all-mcp-server-instructions` e contrato na config global; teste dos três harnesses com o
  MCP pronto capturando a requisição do Codex.
- 15: `routing.yml`, hook de entrada sem IA, verificador registra sem obrigar, maestro corrige a tabela (exceção na
  guarda), GSD fora do global com cópia, `armis-docx` na tabela, teste de aceite da skill do FreeLLMAPI.
- 40/44: família `maestro-*` (`maestro-acervo` porta), primeiro lote, guarda (mod/hook no escopo do usuário,
  verificador em outro modelo, aval), Codex e Copilot recusados no acervo → `agents/maestro/propostas/`, hook de início
  com `MAESTRI_TERMINAL_ID`, hook de registro de uso, `claude-md-and-agents-md` no Maestri. Testes do comentário de
  2026-10-12 do ticket 16.
- 02: copiar `armis-docs`, `armis-brand`, `armis-docx` quando o Gustavo disser; vault não muda.
- 16 (2026-10-15): cinco lacunas de dono (30 dias do `_archive/`; cabeça do contrato no MCP; registro do aval de mudança
  no contrato; quem escolhe o modelo do verificador da guarda; erro de peça citada que sumiu).
- 25: tela de três vias é "logo depois da construção", não condição.

### Decisões que caíram (armadilhas)

Marcador de raiz e `project_root_markers` (14 r4, 2026-10-15; 36 e 40 ainda os citam); consulta ao TI (Gustavo,
2026-10-14); GitHub como ponto de encontro e git-sync (33); "colisão para a máquina inteira" (33); 30 min → 15 min (33);
Desktop só leitura (36, revisão); "Tailscale fora da construção inicial" (06, revisto por 33/34; o SSH segue fora).

### Para as próximas voltas

- Conferir cada faixa nova contra o inventário acima.
- Ver se Worker 2 ajustou o fim da resposta para o mod do Claude Code e se Worker 1 trocou `agents/bin/`.

## Volta 2 (2026-10-15)

Fiz: conferi as dez faixas (todas assumidas) e reescrevi a seção "Conferência das decisões (Prumo)" do `plano.md`:
o que já foi absorvido sai; ficam os pontos abertos. Movi as fronteiras dos Workers 4 e 7, que tinham caído dentro da
minha seção, para o fim de "Fronteiras combinadas", sem mudar o texto. Corrigi a cabeça do contrato na fronteira do
Worker 1 para 2.000 caracteres (Answer do 36).

Contraria decisão (novos): guarda da faixa 9 pede aval para tudo (40: o maestro acrescenta sozinho); verificador em outro
modelo já tem fonte (44: hook `agent` com `"model"`); faixa 6 recusa `Update File` "que troca tudo" (fora do 11); faixa 7
põe sincronizador parado como `divergencia` imediata (glossário do 33). Seguem abertos: o mod na faixa 2 e `agents/bin/`.

Ponto do Prumo 2 (mensagem na volta 2): `kit/`, `hooks/`, `mods/`, `busca/` na raiz do hub contrariam 12 e 33.
Conferido e registrado no plano como primeiro item de "Contraria decisão" e como pergunta ao Gustavo. Recomendação:
repositório de código fora do hub (`C:\Projetos\context-hub-codigo`), worktrees nele; as faixas usam `$env:HUB_CODIGO` e
`$env:HUB_ROOT` para ninguém esperar a resposta.

Fora do mapa: o ticket 56 está `claimed`; da rodada 7 dele, só os 30 dias entraram (pelo 16). "Nota nova nasce em
`inbox/`" e "agente só remove com permissão" não se constroem agora.

Existe agora `../spec.md` (com `spec-partes/`), que os workers estão corrigindo pela parte deles. O prompt limita a minha
escrita a `planejamento/`, então eu não edito a spec.

Para a volta 3:
- Conferir se "Antes da hora" (seção do Prumo 2) ainda põe as dez worktrees no `.git` de `C:\context-hub`; isso conflita
  com a recomendação do repositório de código.
- Ver se os donos absorveram os itens; conferir a spec contra o inventário só se o maestro pedir.

## Execução (2026-10-15, /implement-spec)

Papel: revisar os ramos `faixa-01` a `faixa-05` (Workers 1 a 5) em `C:\context-hub`, contra as decisões do hub e o
código, quando cada worker pedir. O parecer vai curto no `## Comments` de `issues/NN-*.md`: passa, ou o que consertar.
Aviso o maestro "Claude Code" quando um ticket passar. Ordem: `execucao/ordem.md`.

Pontos que eu levo para a revisão:
- O código mora no próprio `C:\context-hub` (decisão de montagem do maestro). A pergunta sobre onde mora o código não foi
  à rodada 2. Anoto como pendente do Gustavo e não bloqueio worker por isso.
- Faixa 1: `agents/bin/` também está pendente; o mesmo tratamento.
- Faixa 2: o fim da resposta no Claude Code é um mod (ticket 14); conferir.
- Cabeça do contrato: 2.000 caracteres.
- Inventário por ticket: seção "Volta 1" acima.
