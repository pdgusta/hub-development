# Relatório do ticket 36: os testes apagam a pasta de ensaio, também quando falham

Vela, 2026-10-17. Ramo `ticket-36`, worktree `C:/context-hub-wt/ticket-36`, de `integracao` 9453e3e.

## O que se mediu antes

- Em `%TEMP%`: 1.326 pastas `hub-ensaio-*`. Só 87 nasceram depois que os testes ganharam o `after` com `rmSync`
  (commits de 16/10, 21h07 a 23h00). Quase todas entre 01:06 e 01:09 de 17/10 (19, 20, 27, 05): uma rodada
  interrompida, ao que tudo indica. As outras ~1.240 são de antes da limpeza.
- Os oito arquivos (04, 05, 05n, 14, 19, 20, 27-fim, 27-pastas), verdes e com TEMP isolado: zero sobra.
- Com falha (TEMP de caminho longo, git falhando): o 14 deixou uma pasta.
- Os três jeitos de vazar, achados:
  1. um `rmSync` lança dentro do laço do `after`, e as pastas seguintes ficam;
  2. o arquivo cai no carregamento (o 14 e o 15 montam o hub no topo do arquivo): o executor do `node:test` trata a
     exceção solta e a relança, e nem o `after` nem o `exit` rodam;
  3. `process.exit` no meio, ou queda do processo.

## O que se fez

- `agents/code/test/pasta-de-ensaio.mjs`: `pastaDeEnsaio(prefixo)` e `hubDeEnsaio(prefixo)` (monta pelo `montar.mjs` em
  `<pasta>/hub` e mostra stdout e stderr do montador quando falha).
  - Limpa no `after` e, de reserva, no `exit` e antes do tratador de exceção solta (`prependListener` de
    `uncaughtException` e `unhandledRejection`).
  - Cada pasta tenta sair sozinha, da mais nova para a mais velha (a ponte, junction, sai antes do hub). A que fica é
    nomeada no erro do `after` ("pasta de ensaio não saiu: ...").
- `agents/code/test/36-pasta-de-ensaio.test.mjs`: roda arquivos-modelo com `node --test` e TEMP isolado. Casos: teste
  que falha; queda no carregamento; `process.exit` no meio; pasta presa (um processo vivo com a pasta como diretório de
  trabalho; abrir um arquivo não prende, o Node abre com FILE_SHARE_DELETE) não segura a outra, e a falha a nomeia;
  hub montado; contraprova sem o ajudante (a pasta fica).
- Troca dos ajudantes locais pelo comum: 04, 05-frontmatter, 05-nova-iniciativa, 14, 19, 20, 27-fim-da-resposta,
  27-pastas, 15-leitura (unitário), gerar-exclusoes (06).

## O que ficou de fora, e por quê

- **Ramos abertos** (pedido do maestro: sem conflito para o Rebite). Trocar depois da junção deles:
  - 08: `banco/ensaio.psm1` e `banco/kit-sem-docker.ps1` (aqui entraria o "New-EnsaioBanco apaga a raiz se cair no
    meio");
  - 10: `banco/mcp-banco-sem-docker.ps1` e `09-mcp-banco.test.ps1`;
  - 15: `ponta-a-ponta/15-leitura.test.mjs`;
  - 16 e 17: `16-vigia.test.mjs` e `17-vigia-tela.test.mjs` (arquivos novos nos ramos; passam a usar o ajudante na
    junção ou logo depois).
- **12-busca, 12-kit-busca e 13-gemini**: param processos (busca, dublês) antes de apagar; rodar os três é trabalho
  pesado (indexação). Já limpam no `after`. A troca pede um gancho "antes de apagar" no ajudante; fica para quando
  houver a trava.
- **Pontas a ponta com harness real e prova 03**: já apagam em `finally`/`after`; mexer pede rodada com harness real.
- **29 (`harness-real.test.mjs`)**: já usa `try/finally`.
- **Os `.ps1` de Docker** (07, 09, 28): já têm `finally` com `Remove-EnsaioBanco`.
- **Morte sem aviso** (`taskkill /F`, falta de memória que derruba o processo): nenhum ajudante pega. As 1.326 pastas
  antigas ficam para o Gustavo (pedido do maestro: nada de limpeza em massa).

## Testes

Todos com TEMP isolado (`$TEMP/v36`, caminho curto: no scratchpad, o git falha com "Filename too long").

- `36-pasta-de-ensaio.test.mjs`: 6/6, sem sobra (três vezes o caso da pasta presa; uma falha intermitente dele, o
  processo que prende ainda não tinha subido, foi consertada: o modelo espera o processo gravar `vivo`).
- Verdes, sem sobra: 04 13/13, 05-frontmatter 19/19, 05-nova-iniciativa 4/4, 14 37/37, 19 19/19, 20 22/22,
  27-fim 16/16, 27-pastas 21/21 (15-leitura e gerador, ver a linha final).
- **Falha forçada** (`etapas/logs/falha-forcada-36.sh`: PATH só com o node, o montar.mjs falha depois de a pasta
  nascer), nos dez arquivos trocados: todos falham, nenhuma `hub-ensaio-*` sobra.
- Contraprova na `integracao` 9453e3e, mesma falha forçada: o 14 e o 15 deixam uma pasta cada (queda no
  carregamento); o 27-pastas não deixa (a falha é dentro dos testes).
- Suíte inteira: é do Rebite, na junção.

## Rodada 1 do Fiel: volta (1 conserto)

- A limpeza em `uncaughtException`/`unhandledRejection` apagava as pastas no meio da rodada: dentro de um teste, o
  `node:test` só marca aquele teste como falho e segue. Conserto: nesses dois eventos, limpar só enquanto nenhum teste
  começou (queda no carregamento). A marca é um `beforeEach` da raiz; o `before` da raiz não serve, porque roda também
  quando o arquivo cai no carregamento (visto no teste: a queda voltou a deixar pasta).
- Testes novos em `36-pasta-de-ensaio.test.mjs`: exceção solta e rejeição solta num teste, e o teste seguinte ainda acha
  a pasta. 8/8; a queda no carregamento continua limpando.
- Limite: uma exceção solta num `before` da raiz, antes do primeiro teste, ainda limpa (os testes daquele arquivo já
  não rodam direito nesse caso).
