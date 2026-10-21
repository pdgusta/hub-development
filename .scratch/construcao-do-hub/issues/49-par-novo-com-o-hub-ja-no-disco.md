# 49: Par novo com o hub já no disco

Type: task
Status: resolved
Etapa: preparo do 26 (par B)
Blocked by: 46

**What to build:** No 26, o par B vai ter o hub **clonado em `C:\context-hub`** antes de o banco dele receber a
replicação do par A. Nenhum teste provou o que o CLI do LiveSync faz quando o disco do par novo já tem os mesmos
arquivos que chegam do banco (`agents/code/docs/instalacao.md` §2, "não verificado"). Pode virar conflito em massa
(duas versões de cada nota), ou duplicar, ou ser inócuo. Provar no ensaio, com a trava e Docker:
1. par A de pé com o hub de ensaio; par B com uma cópia **idêntica** do hub no disco (como um clone), banco vazio;
   subir o B pelo kit e esperar a convergência (passo `espera` do 46);
2. contar conflitos no banco (`_conflicts`), arquivos duplicados ou renomeados no disco do B, e o que a vigia diz;
3. repetir com uma diferença pequena entre os discos (um arquivo a mais no B, um alterado), para saber o que ganha.
Se der conflito ou perda, propor o caminho seguro para o 26 (ex.: B sobe com o disco vazio e o código do kit fora do
hub, ou o clone só depois da convergência) e escrever no relatório.

**Fonte:** decisão do Gustavo (2026-10-18 ~12h45: "concordo" com o teste curto enquanto o par A é instalado).

**Blocked by:** 46 (resolvido)

- [x] ensaio com o disco do B igual ao do A: conflitos, duplicados e vigia contados
- [x] ensaio com uma diferença pequena: o que ganha
- [x] recomendação para o par B do 26 no relatório

## Comments

- 2026-10-18 ~12h45 (maestro): publicado. Dona: a Brasa (banco do par, 07/08/45). Prioridade: antes do par B.
- 2026-10-18 ~12h55 (Brasa): peguei. Ramo `ticket-49`, worktree `C:\context-hub-wt\ticket-49`, de `integracao` 7b6c406.
  Teste: `agents/code/test/49-par-novo-com-hub.test.ps1` (portas 5988/5989, contêineres `hub-ensaio-49-a/b`). A sobe
  sozinho e semeia o banco; B ganha um `git clone` do hub de A (mtime de agora, como no 26); o kit sobe o B
  (`-Passos 04,espera`); conta conflitos crus nos dois bancos, revisões, arquivos a mais/a menos/mudados nos dois
  discos e a passada da vigia do B. Caso 2: um arquivo a mais e um alterado no B. Achado de leitura: o `C:\context-hub`
  de A tem os 523 arquivos de texto em CRLF (autocrlf=true do Git for Windows); se o Git do B tiver autocrlf diferente,
  o clone sai em LF e cada arquivo difere. Próximo: rodar com a trava.
- 2026-10-18 ~13h45 (Brasa): trava minha desde 13:14. Duas rodadas cortadas no caso 2 (o clone não tinha os bytes
  do A), mas cada uma mediu um caso útil (registros em `etapas/logs/`):
  - `49-rodada-1-lf.log` (clone com autocrlf=false: 520 de 578 arquivos em LF no B, CRLF no A): **121 conflitos**
    abertos nos dois bancos (76 .md, 42 .txt, 3 .csv), **399 arquivos do disco do A reescritos** com a versão LF do
    B, o disco do B intacto; a vigia do B em divergência; a espera disse "recebeu" em 33 s.
  - `49-rodada-2-dezoito-lf.log` (18 notas do conteudo.mjs em LF no A e CRLF no B): **16 conflitos** nos dois
    bancos, os dois discos intactos (cada par com a sua versão); vigia em divergência; espera "recebeu".
  Conclusão parcial: o LiveSync não trata dois arquivos de mesmo texto e bytes diferentes como iguais; o final de
  linha basta para conflito. Teste corrigido (0970990): no caso 1 o B leva os bytes do A; caso 3 = LF. Rodando de
  novo os casos 1 e 2 (13:45).
- 2026-10-18 ~14h35 (Brasa, sessão nova após o reinício do Maestri): casos 4 e 5 rodados (o banco do B puxando o do
  A antes do CLI): 0 conflito, mas 400 "binário descartado" falsos nas duas vigias; descartado. Caso 5 contado à mão
  nos pares que ficaram de pé (`etapas/logs/49-caso-5-contas.json`): 1 conflito nos dois bancos, cada disco com a sua
  versão, o arquivo só do B no A, a vigia dos dois mostra o conflito. Caso 1 com os bytes iguais (rodada 3): 0
  conflito. Recomendação: B sobe com o disco vazio e o git depois (caso 6, commit 5ff0373, não rodado). Docker limpo,
  trava solta 14h35. Relatório: `etapas/relatorio-49-par-novo-com-hub.md`. Falta: revisão pelo maestro; caso 6 se ele
  quiser.
- 2026-10-18 ~14h50 (Brasa): maestro aceitou a recomendação e pediu o caso 6 e a ordem dos passos com o kit de fora.
  Caso 6 ampliado (562555b): 08 e 10 sozinhos com o hub vazio, depois 04+espera, git depois, 08+10 de novo (junctions
  e hooks conferidos). Rodando com a trava (registro `etapas/logs/49-rodada-caso-6.log`).
- 2026-10-18 ~15h25 (Brasa): caso 6 rodado duas vezes. Com a pasta vazia, o 08 para (ENOENT em agents/skills) e o 10
  passa; a espera converge (226-290 s); o git depois deixa o `git status` limpo e traz do commit o que o banco não leva
  (nomes com ponto, como os plugin.json dos mods); o 08 e o 10 depois da espera passam (junctions e hooks conferidos).
  Ordem para o B: 00,03,04,05,espera; git; 08,10. Achado: `.livesync/` fora do `.gitignore`. Commits 562555b, 83344d5,
  8f7f4a6 (este, só a conta das pastas locais, sem nova rodada). Trava solta. Próximo: rodada curta do Fiel, Rebite.
- 2026-10-18 ~15h35 (Brasa): a pedido do Gustavo, o ticket 50 entrou neste ramo (c3f2868: `.livesync/` e
  `.livesync-snapshot.json` no `.gitignore`; o caso 6 sem o filtro). O Fiel revisa até c3f2868.
- 2026-10-18 ~15h55 (Brasa): parecer do Fiel r1, VOLTA só no relatório (`etapas/parecer-49-Brasa.md`). Os 6
  consertos feitos no relatório: receita do B com o kit do próprio hub `-Passos 04,08,10` depois do git (o XML da
  tarefa e o `.git/info/exclude`), as tarefas e a remoção do clone só depois; o checkout só do que tem ponto
  (conferido sem Docker); `core.autocrlf=true` como pré-condição; a causa do `.livesync/`; o comando completo
  (`-Casa`, `-EnvFile`, pasta vazia existente); a lista do que muda na `instalacao.md`. Cabeçalho do teste: os casos
  3, 4 e 5 são medidas (ee71863). Pedido a rodada 2 ao Fiel.
- 2026-10-18 ~16h10 (Brasa): o Fiel liberou o código; o Rebite junta. A pedido do maestro, o relatório ganhou a
  seção "Sequência final do par B (para copiar)": os blocos 0 a 8 em pwsh (pré-condições, clone do kit fora,
  -WhatIf, 00,03,04,05,espera com a parada se não convergir, o git com o checkout só do que tem ponto, o kit do
  próprio hub 04,08,10 com as conferências do XML e do exclude, as três tarefas, apagar o clone). Sintaxe conferida
  pelo parser do pwsh; o bloco 6 só pela leitura.
- 2026-10-18 ~15h15 (Brasa): juntado pelo Rebite (e82dd85, até c3f2868). Pendente: o ee71863 (cabeçalho do teste) fora
  da junção; juntar com o Rebite. Brasa parada (pausa do Gustavo).
- 2026-10-21 12:08 (integrador, Rebite): resolvido. Junções e82dd85 (até c3f2868, 2026-10-18) e 35da1e6 (ee71863,
  cabeçalho do teste). Suíte com --test-concurrency=1 e trava em 35da1e6: 390, 375 verdes, 15 pulados, 0 falhas, git
  limpo (log etapas/logs/juncao-49-suite-2.log; a 1ª, de 2026-10-18, foi parada na pausa e não vale). O teste do 49
  (.ps1, Docker) não repetido: idêntico ao que o Brasa e o Fiel rodaram; nenhum executor percorre *.test.ps1.
  Ressalvas do parecer (Fiel r1, 2ª leitura r2 passa): a receita do par B está no relatório (consertos 1 a 6); os
  casos 3, 4 e 5 são medidas; nunca rodar o 08 no HOME real antes do git; a mudança da instalacao.md é dos docs
  (Lume, 8ª junção).
