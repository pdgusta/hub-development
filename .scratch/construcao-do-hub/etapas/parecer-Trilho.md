# Parecer do Fiel — ticket 14, guardas: regravação e ficha (Trilho)

## Rodada 1 — 2026-10-17 — ramo ticket-14 em ea4d299

Veredito: **volta**. Fiel e Fielzinho de acordo (parecer-Trilho-fielzinho.md, nesta pasta).

Conferido: integracao 8b9beef ancestral de ea4d299; worktree limpo; primeiro commit tira o `README.md` da raiz.
`node --test "agents/code/test/*.test.mjs"`: 69/69 (Fiel e Fielzinho). Ponta a ponta com harness real não repetida
nesta rodada: a evidência em `evidencia-14/` e os registros de login do relatório foram lidos; o conserto 1 pede
repetir só o Codex.

### Consertos

1. **(Fielzinho; reproduzido pelo Fiel) Patch com quebra de linha depois de `*** End Patch` passa sem conferir a
   ficha.** `lerPatch` (`patch.mjs:19`) pula a linha `*** End Patch` mas não fecha a parte atual; a linha vazia que vem
   depois entra nas linhas do bloco, `aplicarUpdate` (`patch.mjs:44`) a põe nas `velhas`, a sequência não casa,
   devolve `undefined`, e `decidir` (`guarda.mjs:119`) pula a análise. Reprodução: `Update File` de
   `clients/aurora/migracao-de-tenant/context.md` no hub de ensaio, removendo só a linha `status:`. Sem nada depois de
   `*** End Patch`: recusa ("falta status"). Com `\n`, `\r\n` ou `\n\n` depois: sai vazio, passa. O parser do Codex
   aceita o LF final (fonte no parecer do Fielzinho), então o patch é aplicado e a nota fica sem `status`.
   Os 10 patches gravados na bancada não têm LF final, por isso os testes não pegaram.
   Conserto: fechar a parte em `*** End Patch` (nada depois entra); testes com `\n`, `\r\n` e `\n\n` depois do fim, no
   Codex e no `apply_patch` do Copilot. Repetir a ponta a ponta do Codex (`HARNESSES=codex`) com a regra do login.
2. **(Fielzinho; conferido pelo Fiel) Relatório diz que caminho com ponto passa; o código recusa a regravação.**
   `decidir` testa `regrava` antes de qualquer dispensa por ponto: `Write` sobre `.local/x.txt` ou
   `projeto/.venv/y.cfg` existentes dentro do hub é recusado (reproduzido). Só o frontmatter é dispensado (`analisar`).
   O spec não decide caminho com ponto na guarda. Conserto (acordo Fiel/Fielzinho): manter o código, sem exceção
   nova para regravação no hub; corrigir a descrição no relatório e pôr um teste que fixe a recusa em caminho com ponto.

### Ressalva (não segura)

- Classe do conserto 1: toda troca que o `aplicarUpdate` não reproduz igual ao Codex passa sem conferência
  (`final === undefined`). É a escolha documentada ("a ferramenta falha sozinha"), mas só vale se os dois aplicadores
  concordarem. Vale um comentário no código dizendo isso.

## Rodada 2 — 2026-10-17 — ramo ticket-14 em 124a643

Veredito: **passa**. Fiel e Fielzinho de acordo (parecer-Trilho-fielzinho.md).

Evidências (Fiel):
1. Diff ea4d299..124a643: `lerPatch` zera a parte em `*** End Patch`; comentário da ressalva em `decidir`; testes novos;
   `gerar-casos.py` (gerador dos casos da bancada) entra no repositório; evidência do Codex refeita.
2. `node --test "agents/code/test/*.test.mjs"`: 71/71. Worktree limpo; integracao 8b9beef ancestral.
3. Minha reprodução da rodada 1 repetida no código novo: fim `''`, `\n`, `\r\n` e `\n\n` depois de `*** End Patch`,
   tirando `status` de `clients/aurora/migracao-de-tenant/context.md`: recusa nos quatro.
4. Evidência e gerador sem credencial nem nome do usuário (busca `access_token|refresh_token|id_token|api_key|bearer|
   sk-ant|gho_|ghu_|gustavo` = 0). Nenhum `.credentials.json` nem `auth.json` nas 33 pastas `%TEMP%\hub-ensaio-14-*`
   (as que sobram são dos testes sem harness, como o relatório diz).
5. Ponta a ponta do Codex: não repetida pelo Fiel; li `evidencia-14/codex/` e `hashes-codex.json` (hashes iguais).

Ressalva: as pastas `hub-ensaio-14-*` dos testes sem harness se acumulam em `%TEMP%` a cada `node --test`; o kit ou
o teste deveria apagá-las no fim.
