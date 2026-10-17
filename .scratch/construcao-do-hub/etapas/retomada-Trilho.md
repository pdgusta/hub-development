# Retomada do Trilho (construtor), gravada em 2026-10-17 ~10h55 (São Paulo), para limpar (contexto 40%)

Leia antes: `etapas/regras-da-construcao.md` (inteiras, com os Achados comuns novos: caminho longo do HUB_ROOT;
description de SKILL.md sem ': ' solto), `etapas/fila-pesada.md`, os tickets 21 e 16, os relatórios
`etapas/relatorio-16-vigia.md` e `etapas/relatorio-21-arquivar-e-copia.md`. Responda em pt-BR, frases curtas.
Maestro = "Claude Code"; revisor = "Fiel" (o "Fielzinho" lê depois das 12h15); integrador = "Rebite";
construtores: Brasa, Vela, Cinzel. Sem trava minha; nenhum contêiner nem pasta de ensaio minha sobrando.

## Agora (11:40): ticket 38 (ajudante pasta-de-ensaio nos testes que faltaram)
- Worktree C:/context-hub-wt/ticket-38, ramo ticket-38, de integracao 4a47576. Status do ticket: claimed.
- 39: worktree C:/context-hub-wt/ticket-39, ramo ticket-39, de integracao e7203b4 (claimed).
- Plano: (1) pasta-de-ensaio.mjs ganha antesDeApagar(fn) (para processos/dublês antes do rmSync), com caso novo no
  36-pasta-de-ensaio.test.mjs; (2) 12-busca, 12-kit-busca, 13-gemini, ponta-a-ponta 12 e 15 usam hubDeEnsaio/antesDeApagar;
  (3) PS: New-EnsaioBanco apaga a raiz se cair no meio; Remove-EnsaioBanco apaga a raiz mesmo se o Uninstall lançar;
  09/10 com o try logo depois do New-EnsaioBanco; 08 finally com a remoção garantida; sem-docker .ps1 recebem a raiz
  do node (pastaDeEnsaio) por parâmetro; (4) falha forçada e conferir %TEMP%; 16/17 depois de juntados.
- Feito (11:30): 09b11d8 antesDeApagar no ajudante (+2 casos no 36, 10/10); c2eb375 12-busca, 12-kit-busca, 13-gemini,
  ponta a ponta 12 e 15 pelo ajudante; c0bcc5e ensaio.psm1 (New/Remove-EnsaioBanco apagam a raiz quando caem; teste novo
  38-ensaio-banco 2/2), 08/09/10 limpeza garantida, sem-Docker com -Pasta do node (07 e 09 sem Docker verdes; pwsh morto
  no meio: sem sobra). O 09 sem Docker quebra se o caminho crescer (mensagem de recusa quebra de linha): prefixo curto 09sd.
- 38: Fiel PASSA (39/39); espera o Fielzinho (12h15) na ponta 7c87301 (merge do 17), depois Rebite. Agora: ticket 39 (vigia grava mensagem limpa no estado.json; achado da Vela no 17).
  teste que lança, --test-name-pattern), ponta a ponta 12/15 com HUB_HARNESS_REAL=1 HARNESSES=nada (falha antes do login;
  apagar evidencia hashes-nada.json depois). Conferir só os prefixos meus em %TEMP% (antigos: 12k-HTMh3h, 12k-WVNlmd,
  12-Uz6cAf, 12-vS42Wo, 13-NCcZnS). 16 e 17: trocar depois de juntados. Relatório etapas/relatorio-38-...md; revisor Fiel.
- 21 e 16: com o Rebite (junção numa suíte só).

## Antes (10:55)
### A. Ticket 16 (vigia): PASSOU na rodada curta (~11h); passa levado ao Rebite (~11h), ponta 6a0ab17
- Worktree `C:/context-hub-wt/ticket-16`, ramo `ticket-16`, HEAD 6a0ab17 (sobre 0332466, que passou no Fiel r2).
- A junção do Rebite (fce0529) ficou vermelha no 12-busca: a description do SKILL.md da vigia tinha ': ' (YAML
  inválido). Desfeita: integracao voltou a e98a891. Conserto: "do context hub, que lê o banco". 12-busca 9/9 no ramo
  (`logs/trilho-16-12-busca.log`); 16-vigia 19/19 (não muda).
- Com o passa do Fiel: `maestri ask "Rebite" "Trilho: ticket 16 passou (rodada curta), ponta 6a0ab17, ..."` (o Rebite
  pediu o aviso com a ponta nova). Docker do 16 precisa de HUB_MCP_BANCO_DIR=C:/Projetos/hub-mcp-banco-wt/ticket-11.
- Pedido ao Fiel mandado em background; conferir com `maestri check "Fiel"` se chegou (pedido junto com o do 21).
### B. Ticket 21: r2 PASSOU no Fiel; merge da integracao (22) feito, ponta 6b6c65e, 23/23; Fiel conferiu (PASSA); levado ao Rebite (junção espera o 16)
- Worktree `C:/context-hub-wt/ticket-21`, ramo `ticket-21`, HEAD 462b55e.
- Consertos da r1: f32bd4c (outro disco recusado; Docker com o mesmo PID e nota nova ao B; data local na cópia;
  comentário do frontmatter) e 462b55e (SKILL.md do arquivar sem ': '). Docker 4ª tudo passou
  (`logs/trilho-21-docker-4.log`); leves 77/77; 12-busca 9/9 (`logs/trilho-21-12-busca.log`).
- O Assertion fs-event.c era do observador dublê no TEMP curto (GUSTAV~1.DEL), não do Docker; o dublê agora observa
  pelo caminho longo e o teste confere que segue vivo. Achado levado às regras e ao 23 pelo maestro.
- Conflito combinado com a Brasa: o 21 e o 22 criam o mesmo `agents/code/kit/par/env/10.env.modelo` (meu:
  HUB_MAQUINA/HUB_COPIA_*; dela: HUB_PROXY_*). Quem entra por último em integracao faz `git merge integracao` no
  próprio ramo e deixa as duas metades antes de pedir a junção. O 22 foi ao Rebite antes: provavelmente é meu.
- O ramo do 21 contém fce0529 (a junção desfeita do 16). Antes de pedir a junção: `git merge integracao` (com o 16 já
  juntado de novo), testes leves 21-* e afetados (04, 05, 20, 07-kit-sem-docker), e o 12-busca se a ponta mudou skill.
- Com o passa: `maestri ask "Rebite" "Trilho: ticket 21 passou ..."` (ramo, testes, Docker 4ª, relatório, parecer
  `etapas/parecer-21-Trilho.md`).

## Fechados
16 (passou no Fiel, com o Rebite). 12, 13, 33, 35 (juntados). 15 passou no Fiel (3d34bd1), com o Rebite.

## Decisões desta sessão
- Piora = item sobe de nível em relação à passada anterior; item novo conta como `ok`; desce e volta a subir notifica
  de novo (maestro, no ticket 16).
- Estado velho: o `estado_do_hub` (Cinzel, 10) devolve o JSON e o aviso "a vigia não roda desde <hora>" com passada de
  mais de 15 min; tira `vistos`.
- Só a `search` do hub-busca nos três harnesses (12 r3, opção A do maestro).

## Armadilhas
- Guarda de segredo: comando com o texto `.env` em padrão de grep é recusado inteiro (heredoc junto se perde).
- Barra invertida some em heredoc do bash/python: use o Edit para trechos com `\`.
- `maestri ask` para recruta ocupado fica na fila dele: conferir com `maestri check`.
- Dublê HTTP no próprio processo do teste: chamar a vigia com `execFile` (assíncrono), nunca `spawnSync`.
- Write num arquivo existente exige Read antes.
- Python em heredoc come barras invertidas (barra-zero vira NUL, barra-t vira tabulação). Trecho com barra invertida: Edit, ou chr(92); depois cat -A para conferir.
- No Windows, `process.exit` logo depois de um `fetch` derruba o node (UV_HANDLE_CLOSING): use `process.exitCode`.
- No Codex, o nome MCP com hífen chega ao hook com sublinhado (`mcp__hub_busca__search`).
- O fork padrão `C:/Projetos/hub-mcp-banco` não tem o `estado_do_hub`: o Docker do 16 usa `HUB_MCP_BANCO_DIR`.
- Template literal com barra-n dentro de código passado por -e: vira quebra de linha e o filho não compila (o teste trava).
- Filtro de testes por palavra pode puxar teste pesado (12-busca): rode os arquivos pelo nome.
