# Parecer — Trilho — ticket 05

Data: 2026-10-16. Revisor: Fielzinho. Rodada 2, leitura independente.
Veredito proposto: **volta**. Aguardando acordo com o Fiel.

## Escopo e fontes

Ramo ticket-05, worktree C:/context-hub-wt/ticket-05, HEAD 71d12c1a02248cc608624f6c579d996a1ef2be8c.
Li revisao-em-dupla.md, regras-da-construcao.md, brief 01-esqueleto, ticket 05 e seus comentários,
spec (núcleo e Worker 1), faixa 1 de spec-partes/faixas-01-02.md, escolhas aceitas 14/19/20,
ticket resolvido 12 (Answer e rodadas pertinentes) e relatório (Ticket 05/Assinaturas).
Não li o parecer do Fiel nesta revisão.

## Conferência executada

- Ramo limpo antes e depois; HEAD corresponde ao pedido.
- integracao é ancestral de HEAD (git merge-base --is-ancestor, saída 0).
- node --test "agents/code/test/*.test.mjs": 32 passaram, 0 falhas, 0 pulados; duração 73,4 s.
- node agents/code/bin/verificar-hub.mjs .: sem recusa; avisos de caminho sem tipo para
  agents/blocks.md e README.md, e README.md fora das seis raízes. A sequência terminou normalmente.
- Conferi os testes de criação nas duas raízes, repetição sem sobrescrita, campo obrigatório,
  stage, concorrência, --checar, CRLF, arquivo, YAML flow e pasta com ponto.
- O novo bloqueio de mapa flow preserva os bytes; cabeçalho sem fechamento recusa; campos
  multilinha não envolvidos ficam preservados no caso testado. A pasta com ponto não é corrigida
  nem cobrada, mesmo passada diretamente ou pelo --checar.
- Nenhum Docker ou harness real foi executado. Nenhum código, spec, ticket ou configuração global editado.

## Consertos necessários

1. **Preservar comentários e linhas alheias à correção YAML.**
   agents/code/bin/lib/frontmatter.mjs:237 consome toda linha seguinte que começa com espaço.
   Com `type: errado` seguido por `  # Comentário humano a preservar.`, corrigir troca o type
   e apaga o comentário. A comparação de mesmosCampos só vê os valores parseados e permite a perda.
   Reprodução local pela CLI: saída 0, `completou: initiatives/ensaio/research/comentario.md: type`,
   comentário presente antes e ausente depois. Demais campos válidos e corpo preservado.
   O ticket exige completar por trecho; o relatório promete que o resto fica igual.
   Recomendo preservar comentários fora do valor substituído (ou recusar sem gravar quando a
   edição segura não for possível) e cobrir comentário indentado junto ao campo corrigido.

2. **Ler a ficha dentro da pasta arquivada ao deduzir initiative e títulos.**
   frontmatter.mjs:54-67 e 103 convertem o caminho arquivado em caminho ativo também para ler a ficha.
   A conversão serve para descobrir o tipo, mas a ficha continua dentro do arquivo.
   Reprodução: initiatives/_archive/2026-10-16--arquivada/initiative.md contém id: id-arquivado;
   research/nota.md contém initiative: id-arquivado e archived_at. Não existe a pasta ativa.
   --corrigir retorna 0 e troca initiative para arquivada. A ficha arquivada é ignorada.
   Se houver uma iniciativa ativa homônima, a leitura também pode tomar os dados dela.
   Isso quebra a associação nota/ficha ao ligar com arquivar (Worker 10); não exige implementar
   o arquivador agora. A ficha permite id kebab-case, sem obrigar igualdade com o nome da pasta.
   Recomendo separar caminho lógico para o tipo e caminho físico da ficha; testar ID distinto
   do slug e uma pasta ativa homônima. O título do núcleo deve usar a ficha arquivada também.

## Evidências adicionais preservadas

Fixture mínimo de revisão (catálogo copiado do ramo e notas inventadas; não é hub completo):
C:/Users/GUSTAV~1.DEL/AppData/Local/Temp/hub-ensaio-revisao-05-N4GLSx

Comando para ambos os casos:
node C:/context-hub-wt/ticket-05/agents/code/bin/verificar-frontmatter.mjs --raiz <fixture> --corrigir <nota>

Caso 1: initiatives/ensaio/research/comentario.md. Ficha: id-original.
Caso 2: initiatives/_archive/2026-10-16--arquivada/research/nota.md. Ficha: id-arquivado.
Os arquivos após a execução estão preservados. As fichas do fixture têm só id/title para isolar
esta leitura; não foi alegada validação dessas fichas pelo esquema completo.

## Precisão do relatório e limites

- “Nada lido” em caminho com ponto é mais forte que o código: verificar-frontmatter.mjs:64
  lê o arquivo antes de analisar decidir ignorá-lo. Não houve gravação nem exposição do conteúdo
  nos testes; recomendo ajustar a descrição ou antecipar o filtro. Não é o bloqueio principal.
- A janela entre releitura e gravação permanece não verificada, como aceito/documentado.
- Índices, links, fim de resposta, exclusões local:true e provas reais ficam nos tickets próprios.
- As correções da rodada anterior passaram nos casos existentes; os dois achados acima são
  reproduções adicionais. O Fiel fecha o veredito e aplica o limite de voltas da dupla.

## Acordo da dupla — 2026-10-16, troca 1

Fiel aceitou os dois achados e o veredito **volta**, após concluir sua leitura independente.
Confirmou 32 testes verdes na execução dele. Os dois consertos são requisitos existentes;
a correção da ficha arquivada não amplia o ticket para implementar o arquivador.
Autoria dos achados: Fielzinho. “Nada lido” fica como ajuste de precisão, sem bloqueio próprio.
Fiel fecha a lista única no parecer principal e responde ao construtor.

## Rodada 3 — 2026-10-16, conferência em curso

HEAD 817f85045c658345c4d7a033a86c5e4751a2ad76; ramo limpo, integracao ancestral (0).
Leitura independente dos quatro ajustes e do relatório concluída, sem consultar a nova seção do Fiel.
Comentários recuados não são consumidos; comentários inline no trecho impedem a escrita;
a ficha arquivada usa o caminho físico; caminho com ponto é filtrado antes do readFileSync.
Aguardando a conclusão da execução local dos 34 testes e do verificar-hub para fechar este parecer.

## Rodada 3 — conclusão independente

Veredito proposto: **passa com ressalvas já documentadas**, sem conserto obrigatório restante.
HEAD 817f85045c658345c4d7a033a86c5e4751a2ad76. Ramo limpo antes e depois;
integracao ancestral (0). Não li a nova seção do parecer do Fiel.

Executei node --test "agents/code/test/*.test.mjs": 34 passaram, 0 falhas,
0 pulados, código 0, duração 81,5 s.
Executei node agents/code/bin/verificar-hub.mjs .: código 0, só os avisos conhecidos
(agents/blocks.md e README.md sem tipo; README.md na raiz).

Consertos conferidos no diff e nos testes pela CLI:
1. Comentário YAML recuado é preservado byte a byte; comentário na linha do campo
   corrigido provoca recusa sem escrita. A verificação semântica do YAML segue ativa.
2. O caminho lógico ainda determina o tipo, mas lerFicha recebe o caminho físico
   arquivado. Teste com ficha ativa homônima e IDs distintos mantém id-arquivado e
   completa “Retomada · Arquivada”, sem tomar o título ativo.
3. O filtro ficaDeFora foi antecipado ao readFileSync para arquivo com ponto passado
   diretamente. A descrição do --checar agora distingue conteúdo recebido e ignorado.

Sem achado novo nesta conferência. Mantidas as ressalvas: janela entre releitura e
escrita não verificada; edição conservadora pode recusar YAML que não consiga preservar;
índices/links/fim de resposta/local:true e provas reais continuam nos tickets próprios.
Terceira rodada: respeitado o teto de duas voltas. Os achados da rodada 2 foram corrigidos,
não estão sendo aceitos apenas por causa do teto. Nenhum código/spec/ticket foi editado;
nenhum Docker ou harness real executado. Aguardando acordo final com o Fiel.

## Acordo da dupla — rodada 3, 2026-10-16, troca 1

**Passa**, com as limitações documentadas e sem pendência obrigatória.
Fiel confirmou leitura independente, 34/34 testes verdes, verificar-hub 0, HEAD 817f850
limpo e integracao ancestral. Concordou com os consertos e esta proposta.
Fiel fecha o parecer conjunto e responde ao Trilho. Revisão 05 encerrada pela dupla.
