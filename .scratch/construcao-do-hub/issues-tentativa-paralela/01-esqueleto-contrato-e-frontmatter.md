# 01: Esqueleto, contrato e frontmatter

Type: task
Status: ready-for-agent
Dono: Worker 1
Com: Prumo
Blocked by: None (can start immediately)

Faixa 1 da spec (`../spec.md`, seção "Faixas", Worker 1). Fatia vertical: entrega funcionando de ponta a ponta no hub
de ensaio e no HOME de ensaio, sem esperar as outras faixas.

## O que construir

**Esqueleto, contrato e frontmatter** (faixa 1 do corte candidato): `C:\context-hub` com `.git` e sem `CLAUDE.md` no hub nem acima; o `AGENTS.md` (contrato file-first, zonas, porta de entrada pela busca, como gravar); as seis raízes em inglês com `_archive/`; `agents/blocks.md`; esquemas por tipo em `agents/frontmatter/`; o verificador; o script que cria iniciativa com o núcleo de seis arquivos e o `index.md` (`summary: auto`, `local`)

## Critério de aceite (de ponta a ponta)

- [ ] `agents/bin/nova-iniciativa` cria uma iniciativa de ensaio com o núcleo de seis arquivos; `agents/bin/verificar-frontmatter` aceita a nota certa e recusa a sem `status` ou com `stage` fora do ciclo; um `verificar-hub` passa no hub inteiro (estrutura, frontmatter, nenhum `CLAUDE.md`); testes automatizados

## Como segue sem esperar

nada; entrega cedo o que os outros chamam: no min 0–10, os nomes e a assinatura do verificador (fronteiras abaixo); até lá, as faixas usam o hub de ensaio e um verificador dublê

## Regras

- Ramo e pasta próprios (git worktree) do repositório do hub em `C:\context-hub`; nada global de verdade sem o aval do
  Gustavo (HOME de ensaio); a execução inteira dura 1 hora: o que não couber vai para "Fica para outra execução" no plano.
- Até 10 subagentes; parte muito complexa: um subagente Fable 5.1 médio.
- Antes de juntar: revisão do Prumo (decisões) e do Prumo 2 (construção).
- Erro achado na spec: corrija a spec na sua faixa.

## Comments

- 2026-10-15 ~21:57 (Worker 1, PARE do Gustavo às 21:56). Ramo `faixa-01` (worktree `C:\context-hub-wt\faixa-01`),
  nada juntado em `integracao`. **Feito:** commit 1 com a árvore das seis raízes e `_archive/` (`.gitkeep`) e o
  `.gitignore` da raiz (`.local/`, `.secrets/`, `.maestri/`, `.obsidian/`, índice da busca, bloco `# exclusoes`);
  commit 2 (estado parcial) com `agents/frontmatter/verificar.mjs` (parser do subconjunto de YAML, tipo pelo caminho,
  `--checar`, preencher o derivável, conferência de hash antes de gravar), o primeiro teste em
  `agents/test/01-esqueleto.test.mjs` (**ainda não rodado contra o verificador**) e o que os dois subagentes interrompidos
  tinham gravado (esquemas em `agents/frontmatter/`, `AGENTS.md`, `agents/blocks.md`, SKILL.md): **conferir antes de
  usar, podem estar incompletos**. Arquivos do commit 2: agents/frontmatter/verificar.mjs agents/test/01-esqueleto.test.mjs 
  **Falta:** rodar o teste e seguir o TDD (recusa sem `status`, `stage` fora do ciclo, derivação, inbox, ponto e
  `AGENTS.md` intocados, hash); `exclusoes.mjs`; o script da skill `nova-iniciativa` (`criar.mjs`); a cabeça ≤ 2.000
  do `AGENTS.md` conferida; `hooks/01-verificador/fragmento.json`; `agents/test/01-esqueleto.ps1`; revisão do Prumo.
  Mudança sobre o plano: o verificador ficou sem o pacote `yaml` (parser próprio, como as faixas 6 e 9).
