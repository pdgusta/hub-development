# Worker 10: notas

## Volta 1 (2026-10-15)

**Faixa assumida: 10, manutenção e kit de cliente** (linha do Worker 10 no `plano.md`), mantendo "faixa N = Worker N"
do corte do Worker 2. Fronteiras propostas às faixas 3, 4, 5 e 7 em "Fronteiras combinadas"; nenhuma `maestri ask`
nesta volta (os vizinhos estavam no meio da própria volta; recado vai pelo plano).

### O que conferi nas decisões

- Answer do 33: `.git` na raiz de cada máquina, não replica, um ramo por máquina, só commit e push, git nunca faz pull
  nem checkout e não escreve no disco; o GitHub é só cópia de segurança diária.
- Answer do 36 (R25): `_archive/` por raiz; mover é por script que confere se o outro par está em dia e sem edição
  recente (o LiveSync não garante mover pasta com a outra máquina editando). R33: cabeça autossuficiente de **até
  2.000 caracteres** pelo corte de 2.048 do Claude Code; o Worker 1 propôs 2.048 (divergência anotada no plano).
- Answer do 12: `_archive/` dentro de cada raiz, não de cada iniciativa; pastas com ponto não replicam (por isso a data
  do arquivamento vai no nome da pasta, não num arquivo com ponto).
- Rodada 7 do 56 (respostas do Gustavo): "remover" = mover para `_archive/` por 30 dias, depois remover; agente só
  remove com permissão dele ou depois dos 30 dias. Rodada 8: dois dias de distância na cópia bastam.
- Comentário de 2026-10-15 do 16: lacunas de dono que entram na spec. Peguei a 4 (30 dias do `_archive/`) e a 5
  (cabeça do contrato no MCP). Sugeri a 7, 9 e 10 para a faixa 9.
- Answer do 34 e do 14: cliente sem cópia, MCP de um par por HTTP com token; TBXark/mcp-proxy no par, preso à tailnet,
  uma rota e um token por servidor (`/busca/mcp`, `/banco/mcp` só leitura, `/banco-escrita/mcp`); segundo MCP do banco
  com `READ_ONLY=true`, e o cliente nunca recebe a credencial do CouchDB. Não verificados no 14 e que a faixa mede: o
  TBXark repassar o `instructions`; `${env:...}` no `mcp.json` do VS Code.
- Answer do 36: ponte `mcp-remote` do Claude Desktop (a leitura continua; gravar pelo Desktop foi para o 11).

### Riscos da hora

- O binário do TBXark/mcp-proxy vem do GitHub releases: conferir na fonte primária (README) o formato do config e
  se ele aceita token por rota antes de escrever o kit. Não verificado.
- `--allow-all-mcp-server-instructions` é flag de linha de comando do Copilot CLI (Answer do 41); como torná-la
  permanente no kit de cliente (alias, wrapper) não está decidido. Não verificado se há chave de config equivalente.
- Prioridade se faltar tempo: (a)–(e) primeiro; (f) a ponte do Desktop e a rodada ao vivo dos três harnesses pelo
  proxy ficam para outra execução.

### Para a próxima volta

- Ler as respostas das faixas 3, 4, 5 e 7 às fronteiras; conferir com o Worker 5 a leitura do bloco a cada
  `initialize`.
- Conferir a parte da faixa 10 em `spec-partes/` quando existir (pedido do Gustavo: os workers corrigem a sua parte).

## Volta 2 (2026-10-15, última, 3 min)

Corrigi a seção "Worker 10" do `spec.md` (só o trecho): `agents/bin/` não está no ticket 12, então a pasta dos scripts
segue a da faixa 1 (Prumo); `.gitignore` com `.local/` na cópia diária e o item `copia-diaria` com hífen, o nível sendo da
vigia (Worker 7); a porta do proxy no `.env` do kit para o `--allowed-host` da faixa 3 (Worker 3); a ponte do Desktop
cobre busca e banco com escrita (ticket 11, revisão do 36). Não mexi em `spec-partes/faixas-09-10.md` (sem tempo).
Pendente: dono da lacuna 7 (registro do aval de mudança no contrato): o Prumo sugere a faixa 10, eu sugeri a 9.
