# Prumo 2: notas (revisor da construção)

Papel: conferir cada faixa como construção: dá para fazer e testar em 1 hora, critério de aceite verificável, nada
global nem serviço de verdade sem o aval do Gustavo.

## Volta 1 (2026-10-15)

Fiz: o **crivo de construção** (oito critérios que toda faixa passa) e o rito de revisão dentro da hora, gravados em
`plano.md` → "Revisão (Prumo e Prumo 2)"; a lista do que tem de estar pronto **antes da hora**; os riscos de tamanho
das faixas 4 e 5; uma alternativa à pergunta do login de ensaio.

Fatos conferidos nesta máquina (comando rodado, 2026-10-15 ~21h45):
- Docker 29.8.2 instalado, mas **o daemon não está rodando** (`docker ps` falha no pipe do Docker Desktop). As faixas
  4, 5 e 7 dependem dele: subir o Docker Desktop é passo de antes da hora.
- Node v24.19.0 (o MCP do es617 pede ≥ 22: ok), npm 11.17.0, Python 3.12.10, git 2.55, ripgrep 14.1.1.
- Modo de desenvolvedor do Windows ligado (`AllowDevelopmentWithoutDevLicense = 1`): link simbólico sem admin.
- `C:\context-hub` ainda não existe.
- `claude --help`: existem `--settings <arquivo-ou-json>`, `--setting-sources <user,project,local>`,
  `--mcp-config` com `--strict-mcp-config` e `--bare` (pula hooks). Dá para testar hooks e MCP de ensaio com o login
  atual sem gravar em `~/.claude`.
- `codex --help`: `-c chave=valor` sobrepõe o `~/.codex/config.toml`; `-p` usa `$CODEX_HOME/<nome>.config.toml`.
  Hooks do Codex por `-c`: **não verificado**.
- `copilot --help`: nenhuma opção de arquivo de configuração alternativo além do `COPILOT_HOME`: **não verificado**
  se há outra saída sem login no HOME de ensaio.

Riscos de tamanho (das fontes do mapa):
- Faixa 5: o ticket 26 estima a guarda de revisão do MCP em **1 a 2 dias**. Na hora cabe só o núcleo: `write_note`
  com `base_rev` que recusa versão velha com conflito visível + `instructions`; o resto vai para outra execução.
  Candidata a Fable.
- Faixa 4: o ticket 30 estima a montagem em **3 a 3,5 dias**; o ticket 47 diz que o CLI `daemon` não tem receita para
  Windows (o 48 diz que roda). Na hora cabe: dois CouchDB locais replicando e o CLI espelhando nos dois sentidos; o
  plugin no Obsidian (GUI) é `ready-for-human`.
- Faixa 3: o download do arctic-embed-m-v2.0 e as dependências precisam vir antes da hora (tamanho não verificado).

Próxima volta: conferir pelo crivo cada faixa que já tiver linha completa (a 1, a 2 e a 8 primeiro).

## Volta 2 (2026-10-15)

Fiz: passei o crivo nas 10 linhas (seção "Crivo aplicado às 10 linhas" do `plano.md`). Achados de construção:
- Sem trava contra o HOME real: um kit rodado sem `HUB_HOME_ENSAIO` gravaria em `~`. Proposta: parar com erro sem a
  variável ou se ela for o `$HOME` real; teste próprio na faixa 8.
- Portas sem dono para a faixa 10 (proxy e dublês): propus 8798, 8790 e 8791; tabela única de portas no plano.
- `kit/par/.env.modelo` escrito por 3, 5, 8 e 10 dá conflito na junção: propus `kit/par/env/<nn>.env` juntado pelo kit.
- `C:\Projetos\spike-livesync\` tem um arquivo de credencial do CouchDB: não li; a faixa 4 não deve copiá-lo.
- Faixa 7 é a mais larga: propus a ordem de corte.
- Minha sub-nota da pergunta do login sumiu do plano (edição simultânea de outro recruta); regravei.

Ponto para o Prumo (decisão, não construção): `kit/`, `hooks/`, `mods/` e `busca/` na raiz do hub não estão nas seis
raízes do ticket 12, e o 33 diz que repositório de código mora fora do hub. Avisei por `maestri ask`.

Próxima volta: conferir se os donos absorveram os itens e se a ordem de corte da hora fecha com o rito.

Volta 2, depois do aviso do Prumo: corrigi o "Antes da hora": as worktrees ficam no repositório de código fora do hub (`$env:HUB_CODIGO`), não no `.git` de `C:\context-hub`.

## Execução (/implement-spec, 2026-10-15 ~21h50)

Papel: reviso as faixas 06 a 10 e o ticket 11 (Worker 8). Pedido de revisão chega por `maestri ask`. Confiro o ramo
`faixa-NN` em `C:\context-hub-wt\faixa-NN` contra o ticket, a spec (`spec.md` + `spec-partes/`) e o crivo; rodo os
testes; devolvo ao worker ou aprovo e aviso `maestri ask "Amigo do Maestro" "aprovado: faixa-NN — <linha>"`.

- Retrato dos globais por hash (sem credencial): `agentes/prumo2-globais-antes.txt` (21:53).
- Script do crivo: scratchpad da sessão, `crivo.sh NN` (ramo e base, arquivos, padrões proibidos, globais).
- Pontos que vou cobrar por faixa (da spec):
  - 06: recusa Write sobre existente (inclusive nunca lido), Codex Add/Delete+Add/Update total, Copilot create; fora do
    hub sai sem efeito; nota sem `status` recusada; aviso de leitura uma vez; caminho pela junction; globais por hash.
  - 07: oito cenários `node --test`; notifica só quando piora; `recuperar` devolve bytes; estado em `.local/vigia/`;
    tarefa só XML/-WhatIf; CouchDB só com dublê (Docker sem aval).
  - 08: kit sem `HUB_HOME_ENSAIO` para (trava); -WhatIf não muda hash; 2ª passada não muda; desfazer volta ao hash;
    `CLAUDE.md` acima para o kit; não cria marcador de raiz; GSD com cópia.
  - 09: hooks com JSON de cada harness; sem rede no hook de entrada; guarda pela junction e pelo real; propostas/ aberta.
  - 10: arquivar/limpar/copia-diaria (remoto nu local, nunca pull/checkout); proxy 401 sem token; leitura recusa gravar.

- 21:56 PARE (Gustavo): parei. Nenhuma revisão feita nem pedida; sem ticket nem ramo meu; nada juntado em integracao. Ao retomar: rodar `crivo.sh NN` no primeiro pedido de revisão.
