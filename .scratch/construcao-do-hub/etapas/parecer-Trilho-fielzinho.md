# Parecer — Trilho — ticket 14

Data: 2026-10-17. Revisor: Fielzinho. Rodada 1, leitura independente em curso.
HEAD ea4d29900b2105b0e88b27760fdb05d5e10fccd3, ramo ticket-14 inicialmente limpo.
Veredito preliminar: **volta**. Achado reproduzido pela CLI do hook; suite 69 em curso.
Não li o parecer principal do Fiel. Docker/harness reais ficam exclusivamente com ele.

## Conserto 1 — quebra de linha após End Patch permite retirar status

Em patch.mjs, lerPatch ignora a linha End Patch mas mantém a parte atual; o split adiciona
uma linha vazia final a atual.linhas. aplicarUpdate transforma essa linha em contexto vazio.
Num patch válido que remove apenas status, seguido do fechamento YAML, a sequência
“status + linha vazia” não casa. O resultado undefined é tratado por decidir como uma
ferramenta que falhará sozinha, e a chamada passa sem validação.

Reprodução pela CLI antes-da-ferramenta.mjs codex --hub <fixture>:
- Nota válida em initiatives/ensaio/knowledge/nota.md, com status: em uso antes de ---.
- Patch: Begin Patch / Update File: initiatives/ensaio/knowledge/nota.md / @@ /
  -status: em uso / End Patch (marcadores com os três asteriscos usuais).
- Sem LF após End Patch: deny por falta status.
- Com um LF após End Patch: exit 0, stdout vazio, stderr vazio. Guarda deixa passar.

Fixture preservado: C:/Users/GUSTAV~1.DEL/AppData/Local/Temp/hub-ensaio-revisao-14-CfYV8N.
Catálogo copiado do ramo e nota inventada. Nenhum patch real aplicado, nenhum harness rodado.

Fonte primária do formato, conferida: https://raw.githubusercontent.com/openai/codex/main/codex-rs/apply-patch/src/parser.rs
A gramática admite LF opcional após End Patch (linha 8); parse_patch_text usa trim antes
de separar linhas (linha 179). Assim, a variação é válida no formato, não um patch malformado.
Limite: fonte main atual, sem afirmar identidade binária com o Codex instalado.

Recomendação: terminar a coleta no marcador final/normalizar o envelope como o parser real,
sem confundir a quebra de linha externa com contexto; cobrir pela CLI os dois finais (LF/CRLF)
e exigir recusa nos dois. Não basta registrar undefined como “a ferramenta falha”.

## Conclusão independente da rodada 1

Veredito: **volta**, pelo conserto 1 acima. Suite existente verde não cobre essa variação.
Executei node --test "agents/code/test/*.test.mjs": 69/69, 0 falhas, 0 pulados,
saída 0, duração 79,4 s. Ramo continuou limpo; 8b9beef ancestral (0).

Fontes e leitura: ticket de construção 14, faixa 6 do spec e parte 05-06,
Answer do ticket resolvido 11, trechos de escopo/instalação do 14 resolvido,
esquemas do 12 e verificador do 05 já revisados; relatório da entrega, três módulos
da guarda, fragmentos e testes locais. Conferi os três registros de ponta a ponta da
construtora: em cada harness, regravação recusada, troca permitida, nova nota inválida
recusada e nota válida permitida. Isso não cobre o patch com LF após End Patch.
A execução própria dos harnesses fica com o Fiel; não importei o teste que os executa.

## Ajuste de precisão, sem bloqueio adicional

O relatório diz que “qualquer coisa ... em caminho com ponto” passa. No código, regravação
é recusada antes de analisar ignorar o frontmatter de caminho com ponto. O comportamento
é coerente com recusar regravação de arquivo existente dentro do hub; ajustar a descrição
para distinguir dispensa de frontmatter de dispensa da guarda de regravação.

Limites já declarados permanecem: shell fora do hook; apply_patch do Copilot sem prova
real; leitura/registro de fim de resposta em outros tickets; parser parcial não substitui
os testes contra entradas válidas do apply_patch. A falha encontrada é em formato válido
comum e no aceite explícito “nota que ficaria sem status é recusada”. Não é ampliação de escopo.

Nenhum código, spec, ticket, login ou configuração global foi alterado. Aguardando acordo
com o Fiel, que fecha a lista única e responde ao Trilho.

## Acordo da dupla — 2026-10-17, rodada 1

Veredito conjunto: **volta**. Fiel reproduziu o conserto 1: LF, CRLF e dois LF
após End Patch passam; sem quebra final, a retirada de status é recusada.
Os 69 testes locais também passaram na execução dele.

Fiel confirmou Write sobre .local/x.txt e projeto/.venv/y.cfg recusado. O ajuste de
precisão passa a **conserto 2** na lista única: alinhar relatório e código, com teste.
Concordo com exigir coerência e teste. A escolha do Trilho deve respeitar o escopo já
fixado nos tickets; esta concordância não cria uma exceção nova para regravação no hub.

Fiel fechou a lista única em etapas/parecer-Trilho.md e conduz a devolução ao construtor.
Nenhum teste adicional executado pelo Fielzinho nesta troca.

## Rodada 2 — conferência em curso, 2026-10-17

HEAD 124a643f261598812f2914f3b212d465f63d00c9, ramo limpo, integracao ancestral (0).
Li o diff contra ea4d299 e o relatório atualizado, sem ler a seção nova do Fiel.
O End Patch agora encerra a parte; teste cobre quatro finais em dois adaptadores.
Relatório distingue a guarda de regravação da dispensa de frontmatter em caminhos com ponto,
com teste explícito. Suite local de 71 em execução. Não rodei harness/Docker.
Conferi registro do Codex e hashes-codex.json da construtora: quatro decisões esperadas,
oito hashes antes/depois iguais, cópia de auth.json e apagamento registrados em 23:55:01–23:55:22 UTC.
Essa evidência é da construtora, não uma execução própria de harness pelo Fielzinho.

## Rodada 2 — conclusão independente

Veredito proposto: **passa**. Os dois consertos foram atendidos, sem pendência obrigatória nova.
node --test "agents/code/test/*.test.mjs": 71/71, zero falhas/pulados, saída 0,
duração 88,4 s. HEAD 124a643 confirmado após os testes, ramo limpo.

O caso de regressão cobre os oito pares (Codex/Copilot × sem final/LF/CRLF/dois LF)
e exige recusa por falta status, além de verificar a nota intacta. A parte não recebe
mais a quebra externa ao patch. O teste de caminho com ponto exige recusa de regravação
e permite criação sem frontmatter; relatório e comportamento agora concordam.

Conferi também o diff auxiliar: comentário sobre o limite do aplicador; gerador dos
casos de bancada; nome dos arquivos de hashes por conjunto de harnesses, que evita
sobrescrever o registro anterior. Não executei gerador nem teste de harness real.
Mantêm-se as limitações documentadas da rodada 1, sem apresentá-las como achados novos.
Aguardando acordo do Fiel, que fecha o veredito e responde ao Trilho.

## Acordo da dupla — rodada 2, 2026-10-17

**Passa.** Fiel confirmou o acordo e registrou o fechamento em etapas/parecer-Trilho.md.
Os dois consertos estão atendidos. Revisão encerrada pela dupla; Fiel conduz a resposta
final ao construtor. Nenhum teste adicional necessário ou executado nesta troca.
