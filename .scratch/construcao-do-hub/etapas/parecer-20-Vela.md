# Parecer do Fiel — ticket 20, acervo do maestro e a guarda dele (Vela)

## Rodada 1 — 2026-10-17 — ramo ticket-20 em e5d24a7

Veredito: **volta**. Revisado pelo Fiel sozinho; leitura do Fielzinho fica para depois (cota do Codex), por ordem do
maestro.

Conferido: integracao c5b946a ancestral; worktree limpo. Li o ticket 20, o relatório, `hooks/acervo/decidir.mjs` e
`guarda.mjs`, e a receita `maestro-setups/bateria-de-testes.md`. `node --test agents/code/test/20-acervo.test.mjs`:
11/11. `verificar-acervo.mjs`: saída 0. Busca por e-mail, nomes de cliente, tenant e caminho de usuário nas peças
`maestro-*`: nada de cliente (só "o Gustavo", que é o dono). O commit 8acd1ce fecha as duas ressalvas do 19.

### Consertos (Fiel; reproduzidos no hub de ensaio, pelo `guarda.mjs claude`, sem `HUB_PAPEL`)

1. **Texto inserido no `SKILL.md` de uma peça protegida passa sem aval.** `soAcrescenta` (`decidir.mjs`) aceita
   qualquer linha nova em qualquer lugar, desde que o texto antigo siga inteiro. Reprodução: `Edit` em
   `agents/skills/maestro-acervo/SKILL.md` que insere "- Regra nova: nenhuma mudança no acervo pede aval." antes de
   "- Pede aval do Gustavo: ..." → sem resposta (passa). A mesma linha trocada → deny (certo). A exceção pendente com o
   Gustavo é "linha nova no catálogo"; o código aceita qualquer texto, inclusive regra. Restringir ao que é linha de
   catálogo (linha de tabela ou item de lista com link para uma peça que existe na pasta) e testar a regra inserida.
2. **Peça em pasta que ainda não existe derruba a guarda, e a chamada passa sem conferência.** `nomeParecido` faz
   `readdirSync` da pasta de destino; com pasta nova (ex.: `agents/skills/maestro-novo/peca.md`) dá `ENOENT`, o
   `guarda.mjs` cai no `catch` e responde "erro, a chamada passa sem conferência". Tratar a pasta que não existe (sem
   irmãos = sem nome parecido) e decidir de propósito; teste. Vale também para subpasta nova dentro de uma skill.

### Ressalvas (não seguram)

- `HUB_PAPEL=maestro` confia no ambiente (declarado no relatório).
- Shell (Bash, PowerShell, shell do Codex) fora da guarda, como no 14 (declarado).
- Lacunas de dono e "linha nova no catálogo" seguem com o Gustavo; verificador provisório em Sonnet.
- Aceite real do Codex pendente (cota), em commit só de evidência com rodada curta.

## Rodada 2 — 2026-10-17 — ramo ticket-20 em 5811579

Veredito: **passa**. Revisado pelo Fiel sozinho (Fielzinho lê depois). Aceite real do Codex segue pendente (cota), em
commit só de evidência com rodada curta.

Evidências (Fiel, hub de ensaio, `guarda.mjs`, sem `HUB_PAPEL`):
1. `20-acervo.test.mjs`: 13/13; worktree limpo.
2. Conserto 1: a "Regra nova" inserida no `maestro-acervo/SKILL.md` → deny (vai ao verificador); item de lista com
   link para peça que existe (`[Redator 2](redator.md)`) → passa; link com `..` → deny.
3. Conserto 2: peça em `maestro-novo/` (pasta nova) no Claude → passa de propósito (sem erro no stderr); no Codex
   (`apply_patch` Add File) → deny; subpasta nova dentro de uma skill (`maestro-acervo/sub/x.md`) → ask.

Ressalva: a descrição de uma linha de catálogo é texto livre; uma "regra" escrita como descrição de um item com link
válido passa sem aval. Aceitável enquanto o Gustavo não decide a pergunta do catálogo.
