# Relatório do ticket 46 (Cinzel): o kit de par pronto para duas máquinas

Ramo `ticket-46` (hub), worktree `C:/context-hub-wt/ticket-46`, de `integracao` dc514db. Costuras aceitas pelo
maestro (2026-10-17 ~22h15), com dois acertos: a variável primeiro e o arquivo de reserva, testado também pelo hook do
fim da resposta; a espera nunca falha a instalação. Combinado com a Brasa (45): `logs/46-combinado-brasa.md`.

## O que foi feito

1. **`HUB_PAR_ID`** (e714e42, 47acc61):
   - o passo 08 lê o id do `.env` do par e o grava em `<hub>/.local/par.json` (`.local/` não replica nem vai ao git);
   - recusa `.env` sem o id ou fora da regra `^[a-z0-9]+(-[a-z0-9]+)*$` (a mesma do `Assert-IdPar` da Brasa no 45);
     com `-WhatIf`, diz que gravaria e não grava;
   - `agents/code/bin/lib/par.mjs` (`parId(raiz, env)`): a variável primeiro; de reserva, o arquivo;
   - quem lê: `bin/verificar-pastas.mjs` (e com ele o fim da resposta, que o chama pelo hook) e o registro de uso do
     roteamento (`hooks/roteamento/registro.mjs`);
   - `env/10.env.modelo` ganhou a linha `HUB_PAR_ID=`; os `.env` de ensaio do 23 e do 24 ganharam `HUB_PAR_ID`.
2. **Espera da convergência** (dfa221a, 4e89be6): passo `espera`, o último da lista padrão, `kit/par/espera.mjs`,
   prazo `-PrazoEspera` (padrão 900 s).
   - Lê o banco pelo leitor da vigia (`HUB_VIGIA_LEITOR_DB`, `sync` e `ls` do CLI) e confere o disco: cada arquivo do
     banco no hub, com o mesmo tamanho.
   - Também pergunta ao outro par (`HUB_VIGIA_OUTRO_PAR_URL`, senão `HUB_OUTRO_PAR_URL`, com o admin dele) as
     mudanças pendentes da tarefa de envio dele para este par: sem isso, um banco ainda pela metade parecia recebido.
   - Banco vazio não conta como recebido.
   - Progresso linha a linha enquanto espera (`recebendo o hub: X de N...`, `o outro par ainda envia: P...`).
   - No fim do prazo: `o par ainda está recebendo o hub: <motivos>; o sincronizador segue em segundo plano. Confira
     depois: node ... --segundos 600`, código 0. Sem leitor ou com o CLI falhando: `não deu para conferir...`, código 0.
   - O `convergiu.mjs` do 25 compara dois discos (A e B); na máquina B só há o banco, por isso a espera não o usa.
3. **Proxy na fila** (56688d9): passo opcional `proxy` (`10-proxy.ps1 -EnvFile`), fora da lista padrão, depois do 05.
4. **O que falta à mão** (56688d9): a saída (linhas `à mão: ...` e a chave `a_mao` do JSON) lista os mods do Claude
   Code, a extensão `onAgentStop` e a `statusLine` do Copilot, o `notify` do Codex, as tarefas agendadas (com os XML
   achados em `<casa>\.hub-kit\tarefas\` e em `HUB_BANCO_ESTADO\tarefa-sincronizador.xml`, e o comando `schtasks`) e,
   sem o passo `proxy`, que o proxy não subiu.

## Testes

- `agents/code/test/46-kit-duas-maquinas.test.mjs` (leve, sem Docker; CLI falso da vigia e um dublê HTTP do outro
  par): 18 testes.
- Arquivos mexidos: `23-kit`, `27-pastas`, `27-fim-da-resposta`, `19-roteamento`, e os ponta a ponta 19, 27 e 24
  (este pulado sem `HUB_HARNESS_REAL`). Resultado em `logs/46-testes-par.log` e `logs/46-testes-kit.log`.
- `agents/code/test/46-espera-banco.test.ps1` (Docker, com a trava): dois pares do 07, o B recebendo a semente; prazo
  curto avisa; prazo do kit converge; a espera concorda com o `convergiu.mjs` (hash); nota nova do A chega. Resultado
  (2026-10-17 ~22h35, com a trava): **6 PASSA**, `logs/46-espera-banco.log`. Prazo de 20 s: "faltam 439 de 566". Prazo
  do kit: convergiu em 315 s, 566 arquivos, 28 linhas de progresso; o `convergiu.mjs` dá os mesmos 566, 0 faltando e 0
  diferentes no hash; a nota nova chegou em 4 s. Contêineres apagados ao fim; trava solta.

## Ressalvas

- O `-Desfazer` não tira o `.local/par.json` (mora no hub, não na casa; é estado da máquina, inofensivo).
- A espera compara tamanho, não hash (o `ls` do CLI dá tamanho, mtime e rev). A prova com Docker confere contra o hash.
- A rede entre as máquinas de verdade (Tailscale) fica para o 26.
