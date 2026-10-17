# Ticket 31 — Vela — Fielzinho — leitura independente em 4e420a6

2026-10-17. Worktree C:/context-hub-wt/ticket-31 limpa. Li regras comuns, ticket31, relatório completo, fonte Worker9/faixa9 já lida, código decidir/guarda/verificador/aval/vigia/verificar-acervo, fragmento Claude, testes e diff050fb14. Sem ler parecer do Fiel desta rodada. Não executei Docker nem harness real.

## Veredito proposto

**PASSA o conserto CRLF; lacuna de registro de aval a encaminhar ao Fiel.** Como esta leitura tardia também alcança o código do31 já integrado, o Fiel decide se entra como ressalva da terceira rodada (teto das regras) ou correção posterior. Não altero ticket nem código.

## Conserto e evidências

- 050fb14 converte old_string LF para CRLF quando essa é a correspondência presente no arquivo. O final deixa de ser undefined e chega à decisão de proteção. Teste novo cobre caminho real, junction fora do hub, Claude, Codex e Copilot.
- Claude real em evidencia-20/claude/guarda-do-acervo.jsonl: deny para redator.md, com modelo claude-haiku-5-5; ask para redator-2.md. Codex: dois deny com rota agents/maestro/propostas/. A mudança de asserção usa registro da guarda no Codex, sem afirmar que stdout mostrou a recusa.
- hashes-claude-codex.json: configurações e logins iguais antes/depois; ambas as pastas de login com apagado=true. Evidência da Vela, não execução minha. Não prova aprovação interativa do ask: no ensaio não interativo ele é recusado.
- Proteção .local/acervo/ e agents/maestro/avais/ está antes da exceção do maestro e usa alvo resolvido. Sem confundir essa cobertura das ferramentas com barreira a escrita por shell.
- Modelo de maestro desconhecido continua permitindo ask com aviso; é limitação declarada no relatório, sem prova de diversidade nesse caso. A checagem por família funciona no caso coberto opus/sonnet.

## Achado independente reproduzido

1. **Pedido de aval sem parecer não deixa registro quando aprovado.** decidir.mjs retorna ask imediatamente para peça/skill nova de nome parecido (e para routing.yml por não-maestro), sem criar pendência nem parecer. aval.mjs exige ambos os arquivos antes de registrar. Logo, esses avais aprovados não chegam a agents/maestro/avais/, embora o critério1 do31 diga que com um aval aprovado nasce o arquivo.

Reprodução própria sem harness, somente módulo real + PostToolUse sintético, em pasta temporária exclusiva: criei maestro-papeis/redator.md, pedi criação de redator-2.md; decidir devolveu ask (nome parecido); simulei gravação aprovada; executei aval.mjs com evento Write. Resultado: postExit=0, stderr vazio, registroExiste=false. Pasta removida em finally, após conferir raiz/prefixo. Não houve aprovação real nem chamada a modelo: a reprodução prova a falta de registro depois do evento que o hook usa como aprovação.

Recomendação: registrar a pendência também para todos os caminhos que devolvem ask e consumi-la após sucesso; para caso que não exige verificador, registrar essa condição explicitamente, sem inventar parecer/modelo. Cobrir criação de nome parecido. Isso não exige obrigar verificador nesses casos novos: só não perder o aval do Gustavo.

## Testes próprios

Em andamento: node --test --test-concurrency=1 agents/code/test/20-acervo.test.mjs agents/code/test/14-guardas.test.mjs (sessão17732). O arquivo14 já mostrou37 verdes. Aguardar total; não repetir suíte/harness.

## Resultado próprio concluído
20-acervo +14-guardas:57/57 PASSA,0falhas,saída0,130,1s. Sessão17732 encerrada. O caso CRLF novo passou. A reprodução da lacuna de aval permanece fora desses casos. Proposta de veredito desta terceira rodada: PASSA COM RESSALVA do registro incompleto, correção posterior encaminhada pelo Fiel; aguardo acordo. Nenhum teste próprio em execução.


## Acordo encerrado
Fiel confirmou: consertoCRLF aceito (57/57 também na execução dele); concorda com o achado do aval sem parecer não registrado. Terceira rodada: PASSA COM RESSALVA escrita e conserto num ticket seguinte. Veredito único em parecer-31-Vela.md. Leitura31 encerrada em dupla.

