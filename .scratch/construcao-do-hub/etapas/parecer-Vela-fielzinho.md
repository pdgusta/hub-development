# Parecer Fielzinho — Vela, ticket 27, rodada 1

Data: 2026-10-17. Veredito independente: **VOLTA**. Acordo com o Fiel confirmado: VOLTA nos cinco consertos.

## Base e limites

Worktree C:/context-hub-wt/ticket-27; ramo ticket-27; HEAD 8d8f1b9745068a69151cfda6ce8279c68e9b5416. Limpa antes e depois da revisão. integracao 8d1d785ab8102f3ac81f1c48cce261b8af4f8934 é ancestral (merge-base --is-ancestor: saída 0). Não li o parecer do Fiel antes desta leitura.

Fontes lidas: ticket de construção 27 inteiro; regras-da-construcao.md e revisao-em-dupla.md inteiros; ticket resolvido 12 inteiro; faixa 1 do spec, em especial Verificador sem IA, Cartão da pasta, Links e Testing decisions; implementação, testes e fragmentos do 27; extração de pastasLocais do gerador; evidências reais versionadas. Nenhum harness real, Docker, subagente ou escrita global. Não editei código/spec/tickets.

## Consertos

1. **Preservar AGENTS.md e SKILL.md também na conferência de links.** Em agents/code/bin/verificar-pastas.mjs:58, conferirLinks só exclui caminho fora do hub e ponto. Não usa a proteção de nomes do verificador de frontmatter. Reprodução no hub montado: inbox/AGENTS.md com `Consulte [[initiatives/context-hub/labs/ensaio-do-banco]].` virou `Consulte [ensaio-do-banco](par://ensaio/initiatives/context-hub/labs/ensaio-do-banco.md).` pelo CLI com --corrigir; saída 0. Contraria o spec faixa 1: “não toca AGENTS.md nem SKILL.md”. Corrigir e provar ambos os nomes na execução direta e pelo fim.

2. **Não chamar verificar-pastas sem alvo quando o turno não gravou nada.** Em hooks/fim-da-resposta/nucleo.mjs:64–69, arquivos vazios geram alvos vazios. O CLI, verificar-pastas.mjs:94, interpreta isso como o hub inteiro. Reprodução com todos os arquivos explicitamente envelhecidos por utimes para 2000-01-01: gravei inbox/binario.png antes de marcar, marquei e chamei fim sem escrever nada. inbox/index.md não existia antes e passou a existir depois, embora fim retornasse `{soltar:'sem falta'}`. Assim, um turno de leitura faz manutenção e reescrita no hub inteiro, e as faltas ficam filtradas fora de nossos. Retornar sem falta sem executar os verificadores quando não há arquivos mudados; provar que nenhum cartão/nota muda nessa situação.

3. **Entregar os avisos ao agente.** nucleo.mjs:67–76 retém só falta/recusa; descarta todos os avisos, inclusive links corrigidos e promoção de other/. O registro.jsonl também guarda apenas decisão/horário, sem esses avisos (contrário à frase do relatório “fica no registro”). Reprodução: marquei o turno e gravei inbox/nova.md com link para labs local; fim corrigiu para par:// e retornou apenas `{soltar:'sem falta'}`. Nenhum aviso foi entregue. O ticket exige avisar o agente nos dois sentidos e avisar quando três other/ pedem bloco. Entregar avisos pelos adaptadores sem transformar aviso em falta nem consumir devoluções; provar links nos dois sentidos e other/ pelo canal de fim.

4. **Não confundir queda do subprocesso com conferência sem falta.** nucleo.mjs:56–58 ignora status, error e stderr de spawnSync; pastas.mjs:109 usa decodeURI sem tratar URI malformada. Reprodução no hub de ensaio, depois de marcar: inbox/a-uri.md com `[link](invalido%ZZ)` e inbox/z-segredo.md com `[[clients/aurora/migracao-de-tenant/.secrets/leia-me.txt]]`; garanti mtime dos dois posterior à marca via utimes. fim retornou `{soltar:'sem falta'}`. A primeira URI derrubou verificar-pastas antes da segunda nota. Tratar a URI inválida por arquivo, continuar a conferência dos demais e reportar falha do subprocesso; não anunciar “sem falta” quando a conferência caiu. Provar a devolução da falta da segunda nota.

5. **Aplicar a regra de .secrets também aos links par:// já existentes.** Em pastas.mjs:141–146, o ramo PAR retorna original assim que naoReplica é verdadeiro, sem passar por emSegredo. Reprodução direta: `[acesso](par://ensaio/clients/aurora/migracao-de-tenant/.secrets/leia-me.txt)` ficou idêntico, avisos=[], faltas=[]. O spec e o ticket resolvido 12 mandam citar só o nome de arquivo de .secrets; trocar o esquema não pode dispensar a regra. Provar a recusa desse formato pelo CLI e fim.

## Conferência do relatório e aceite

- Testes próprios: `node --test "agents/code/test/*.test.mjs"`: 90/90, saída 0, 89,6 s. `node --test agents/code/test/gerar-exclusoes/gerador.test.mjs`: 7/7, saída 0, 4,7 s. Total 97/97, consistente com o relatório. Esses testes não cobrem os consertos acima.
- Cartões: testes cobrem limiar 9/10, PNG sem texto e frontmatter válido, lista idempotente, descrição antiga/texto livre preservados, irmão de anexo e exceção de oficina. Código usa entradas diretas, sem ponto e sem index.md, como decisão técnica do ticket. summary manual preservado.
- Links: os dois sentidos e falta de HUB_PAR_ID passam nos exemplos da suíte; há as lacunas 1, 3, 4 e 5 acima. Links para fora do hub (story 44/spec Links) também não são tratados: exemplos `[[C:/fora/arquivo.md]]` e `[arquivo](file:///C:/fora/arquivo.md)` ficam intocados. Registrar com o Fiel a abrangência dessa exigência, pois o ticket 27 enfatiza o cartão/local e o formato de caminho externo precisa de interpretação.
- other/: grupos por why_other no hub inteiro, aviso único a partir de três; testes 2/3 passam. O aviso é perdido no fim (conserto 3).
- Fim: testes próprios confirmam três devoluções, quarta libera e registra estado, reinício da contagem, continuação Copilot e preservação de itens/pior nível da vigia. O problema da vigia sobrescrever itens externos consta do relatório; é costura para o dono da vigia, ainda não prova de preservação na passada seguinte.
- Evidência real lida, sem executar/importar o teste ponta a ponta: registros Claude e Codex têm marca, devolução, soltura sem falta; Copilot acrescenta marca continuacao:true entre devolução e soltura. Notas finais retiraram o caminho .secrets (Claude/Copilot usam só [[leia-me.txt]], Codex texto simples). O relatório descreve texto simples para os três, mas o resultado atende a regra do nome.
- Hashes: rodada dos três registra três pastas apagadas, sete de oito hashes iguais e config.toml real divergente; repetição Codex registra oito iguais e pasta apagada. Confere com a ressalva do relatório. A causa atribuída às sessões reais é hipótese da construtora, não comprovada por esta revisão.
- O deslize de subagente da construtora está explicitado no relatório; não executei subagentes. O mod foi lido; validação e funcionamento real são evidência da construtora e conferência reservada ao Fiel.

## Reproduções próprias

Scripts Node enviados pela entrada padrão, sem salvar no código. Cada reprodução montou hub com agents/code/test/hub-de-ensaio/montar.mjs em uma pasta temporária hub-ensaio-27-revisao-*, chamou o CLI/núcleo do ramo e apagou a própria pasta em finally. Para evitar ambiguidade de relógio/mtime, no caso 2 envelheci todos os arquivos antes da marca; no caso 4 defini mtime dos dois arquivos para Date.now()+2000 após a marca. Sem credenciais ou harness.

## Conversa em dupla

2026-10-17: Fiel confirmou VOLTA nos cinco consertos. Reproduziu independentemente 2 (CLI sem alvo regravou dois cartões), 4 (URIError com %ZZ) e 5 (par:// para .secrets sem falta). Links fora do hub ficam como ressalva, com ponto aberto ao maestro: o spec pede caminho a partir da raiz do hub, e o critério do ticket 27 cita local:true. Concordo com esse enquadramento. Parecer único em etapas/parecer-Vela.md. Fiel fecha e responde à Vela. Sem acordo pendente nesta rodada; aguardar correção ou próximo pedido.

