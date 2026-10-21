# Parecer do 46 (Cinzel), rodada 1: VOLTA, 1 conserto

Fiel, 2026-10-17. Ramo `ticket-46` 4e89be6 (contém `integracao` dc514db). 2ª leitura: subagente Opus 5.5,
`parecer-45-46-segunda-leitura.md`. Em acordo.

## O que conferi
- Junção sem commit 46 + 45, sem conflito; leves 157/0, 1 pulado (`logs/revisao-45-46-juncao-fiel.log`).
- `46-espera-banco.log` 6 PASSA (315 s, 566 arquivos, igual ao `convergiu.mjs` por hash); sem segredo.
- Id do par: mesma regra no 08 e no `Assert-IdPar` do 45; variável primeiro, `.local/par.json` de reserva; verificador,
  fim da resposta e registro do roteamento testados. Espera: leitor da vigia iniciado pelo 04, id da replicação igual ao
  `Get-IdReplicacao`, sai 0 sempre. Proxy opcional e lista `a_mao` conferem.

## Consertos
1. **(Fiel e 2ª leitura) O `HUB_PAR_ID=` vazio do `10.env.modelo` apaga o id gerado pelo 45.** O gerador do 45 escreve
   `HUB_PAR_ID=<id>` e manda juntar as linhas dos modelos 03, 05 e 10; o `10.env.modelo` (deste ramo) traz
   `HUB_PAR_ID=` vazio; o `lerEnv` do `08-harnesses.mjs:58-65` deixa a última vencer, também vazia.
   Sonda (na junção): `.env` com `HUB_PAR_ID=casa` + as linhas `^[A-Z_]+=` do `10.env.modelo` →
   `instalar.ps1 -Passos 08 -WhatIf` → `passo 08 parou: HUB_PAR_ID falta no .env do par`. No dia do 26 o 04 já subiu o
   banco quando o 08 para, e a mensagem diz "falta" com o id no arquivo.
   Conserto, à sua escolha: tirar `HUB_PAR_ID` do `10.env.modelo` (o gerador escreve; o comentário pode ir para o
   `04.env.modelo`), ou o `lerEnv` do 08 (e o da espera) não deixar vazio apagar valor preenchido / recusar chave
   repetida dizendo as linhas. Teste: o `.env` do `gerar-env-pares.ps1` + os modelos passa no `-Passos 08 -WhatIf` com o
   id gerado (o teste precisa do 45 juntado: junte `ticket-45` ou `integracao` depois do 45).

## Ressalvas
1. `HUB_MAQUINA` (cópia, ramo `par/<máquina>`) e `HUB_PAR_ID` são dois nomes da máquina; o gerador só escreve o segundo.
   Para o 26: dizer que são iguais. O registro de uso muda de `<hostname>.md` para `<id>.md`. (2ª leitura)
2. No par A (semente), a espera diz "o banco do par ainda não tem nada do outro par" enquanto o disco sobe ao banco.
   Só texto. (2ª leitura)
3. A espera usa o mesmo banco local do leitor da vigia; vigia rodando junto pode travá-lo. Improvável na instalação.
4. `spawnSync` do `ls` com `maxBuffer` de 1 MiB: anotar se o hub crescer muito.
5. Tamanho, não hash; `-Desfazer` não tira `.local/par.json` (já ditos no relatório).

---

# Rodada 2 (dc4fd1a): PASSA

Fiel, 2026-10-17. 2ª leitura Sonnet (diff pequeno): `parecer-46-Cinzel-segunda-leitura-r2.md`, PASSA. Em acordo.

- Conserto 1 feito: `HUB_PAR_ID` fora do `10.env.modelo` (só comentário) e o `lerEnv` do 08 e da espera não deixa vazio
  apagar valor lido. Nenhuma chave do gerador do 45 reaparece nos modelos 03, 05 e 10 (os leitores PowerShell, "última
  vence", seguem seguros).
- Sonda na junção dc4fd1a + 45: `.env` do `gerar-env-pares.ps1` + 03 + 05 + 10 + `HUB_PAR_ID=` vazio no fim →
  `-Passos 08 -WhatIf`: `faria: id do par (casa)`, código 0; nada gravado (`.local/` não criado). Isola a regra nova do
  `lerEnv` (ressalva 1 da 2ª leitura coberta pela sonda).
- Leves na junção: 46, 45, 23, 27 (2), 19, harness-real: **117/117** (`logs/revisao-46-r2-juncao-fiel.log`).
- Ressalvas 2 (texto do par A) e 4 (`maxBuffer` 64 MiB) acatadas. Ficam as ressalvas 1, 3 e 5 da rodada 1.
