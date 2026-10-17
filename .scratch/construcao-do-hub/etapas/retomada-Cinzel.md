# Retomada do Cinzel (construtor)

**2026-10-17 ~20h45: construção fechada; nada pendente do Cinzel.** Todos os tickets resolvidos, menos o 26
(instalação de verdade, com o Gustavo). `integracao` em ca62332 (suíte 370: 355 verdes, 15 pulados, 0 falhas).
Tickets dele (09, 10, 11, 23, 24, 37) resolvidos; o 24 juntado em a4fa7e3. Versão longa antiga:
`etapas/logs/retomada-Cinzel-antes-17h20.md`.

## Ressalvas e achados que valem

- **24:** os servidores `hub-*` ficam registrados no Codex do ensaio, mas o transporte cai (não sobem no ensaio, como
  combinado). Detalhes em `etapas/relatorio-24-kit-de-par-ao-vivo.md`.
- **Codex e as instruções do MCP** (11): nada no primeiro pedido; chegam só na saída da ferramenta com que o modelo
  lista as ferramentas, à frente da descrição de cada uma.
- **EPERM passageiro no rename** sob carga (23): o kit repete por ~2 s (`renomear` em `kit/par/kit/casa.mjs`).
- Codex só em teste, `gpt-6-luna` por padrão (`MODELO_CODEX` de `harness-real.mjs`); `gpt-6.1-sol` só com
  `HUB_MODELO_CODEX`, dizendo por quê. Nenhum teste escreve o modelo à mão (`harness-real.test.mjs` confere).
- Teste ao vivo do 24: `agents/code/test/ponta-a-ponta/24-kit-ao-vivo.test.mjs`, com `HUB_HARNESS_REAL=1
  HARNESSES=<harness>` e `--test-concurrency=1`; sem a variável, aparece pulado.

## Lições práticas

- `%TEMP%` é curto (`GUSTAV~1.DEL`): `TEMP`/`TMP` = `C:/Users/gustavo.delfino/AppData/Local/Temp` nos testes.
- Arquivo com `\`: só pelo Write ou pelo Edit; depois, `node --check`.
- `maestri ask` sem barra invertida nos caminhos; em segundo plano.
- App-server do Codex numa pasta de ensaio a prende por instantes: apagar com `apagarEnsaio`, com espera.
- Contagem de PASSA: contar as linhas no log, não de cabeça.
- Junção é do construtor: levar a `integracao` ao ramo antes de pedir; o Rebite devolve conflito.

## Como retomar

1. Ler `etapas/regras-da-construcao.md` (inteiras).
2. Aguardar ordem do maestro (`maestri ask "Claude Code" ...`). Não pegar ticket nem trava por conta.
3. O histórico mora nos tickets, relatórios, pareceres e no git.
