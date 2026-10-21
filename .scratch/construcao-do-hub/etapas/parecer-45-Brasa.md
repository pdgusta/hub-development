# Parecer do 45 (Brasa), rodada 1: PASSA, com ressalvas

Fiel, 2026-10-17. Ramo `ticket-45` 02dabc4 (contém `integracao` dc514db). 2ª leitura: subagente Opus 5.5,
`parecer-45-46-segunda-leitura.md`. Em acordo.

## O que conferi
- Junção sem commit 46 + 45 (`%TEMP%/hub-ensaio-45-46-fiel-juncao`, sem conflito). Leves na junção: 45, 46, 23, 27 (2),
  19, 07-kit, 38, 28, 09, 22 (2), 25 (2), 16, harness-real, 24 (pulado): **157/0, 1 pulado**
  (`logs/revisao-45-46-juncao-fiel.log`).
- Provas com a trava: `45-banco-endereco.log` 13/13 (escuta só 127.0.0.1 e 100.120.188.50; nada em 0.0.0.0/::;
  contraprova; tudo descido), `45-montar-cli.log` 6/6. Sem segredo nos logs nem nos diffs.
- Costura com o 46: o gerador escreve `HUB_PAR_ID` (mesma regra do 08), `HUB_VIGIA_LEITOR_DB` (o 04 inicia o leitor) e
  `HUB_OUTRO_PAR_*` (a espera do 46 lê); o `Assert-CliLiveSync` novo não quebra os testes do 46 nem os vizinhos.

## Consertos
Nenhum neste ramo. O conserto da costura do `.env` fica no 46 (linha `HUB_PAR_ID=` vazia do `10.env.modelo`).

## Ressalvas (para o 26 ou rodada curta)
1. `Invoke-Compose`: com `Endereco` nulo, o `compose.endereco.yml` entra e `${HUB_BANCO_ENDERECO}` vazio publicaria em
   todas as interfaces. Hoje todo par vem de `Read-EnvPar` (não é bug vivo). Barato fechar: `${HUB_BANCO_ENDERECO:?}`.
   (2ª leitura)
2. Aceita qualquer IPv4 (ex.: 192.168.x); um aviso fora de `100.64.0.0/10` ajudaria no 26. (2ª leitura)
3. `restart: unless-stopped` com porta presa ao IP do Tailscale: se o Docker subir antes do Tailscale, o contêiner pode
   não subir até o laço religar. Não testado. (2ª leitura)
4. A saída do gerador não manda rodar o `montar-cli-livesync.ps1` (o CLI padrão `C:\hub-par\livesync\...` não existe até
   lá; o 04 recusa com mensagem clara). (2ª leitura)
5. Só IPv4; `git -C` pode dar "dubious ownership" se a pasta do CLI for de outro usuário.
