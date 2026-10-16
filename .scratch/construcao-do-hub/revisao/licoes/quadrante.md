# Lições do Quadrante (relator da revisão conversada, 2026-10-16)

## O que funcionou no método

- **Um arquivo por pessoa por rodada.** Ninguém gravou por cima de ninguém. Um `/clear` no meio não perderia nada.
- **Só o relator edita a proposta.** As partes votam em texto; o relator aplica e lista o que aplicou no próprio arquivo
  da rodada. A conferência dos outros fica fácil: diff de `antes/` para `proposta/` contra a lista.
- **Regra clara do que vale como decisão.** "Ticket resolvido; o mais recente vence; o núcleo sozinho não decide; o 56
  é aberto; formato não se decide." Com isso, quase toda divergência virou classificação, não disputa.
- **Três marcas no texto do spec.** [núcleo], [formato] e [ticket aberto: 56] deixaram a proposta legível para o
  Gustavo: ele vê onde dar aval, onde ajustar o plano e o que ficou fora.
- **Divisão dos tickets em três terços.** Cada um leu um terço inteiro e trouxe só o que decide o spec. Cobriu os 55
  tickets sem ninguém ler tudo. O relator conferiu os pontos cruzados (um pedido do Sextante sobre o 14, por exemplo).
- **Ask back pelo Maestri.** "Ao gravar, responda `rodada N gravada`" resolveu a espera sem polling.
- **Ids por mudança.** `Q-n`, `Prisma-n`, `Sextante-n`, `C-n`, `P4-n`: cada voto apontou para uma coisa só.
- **Acordo chegou na rodada 2.** As rodadas 3 e 4 serviram para propagar o acordo a todos os lugares do spec e
  conferir. A 5 só confirmou. Cinco rodadas foi o tamanho certo para um spec de 400 user stories.

## O que atrapalhou

- **Volume de leitura na partida.** Proposta inteira (190 KB) mais 19 tickets mais insumos antes de escrever a rodada 1.
  Inevitável, mas a rodada 1 demorou mais que as outras quatro juntas.
- **Aplicação manual em seis arquivos.** Uma decisão (por exemplo, a regra curta do MCP) aparece no núcleo e em três
  partes. Propagar à mão gerou cinco correções de propagação na rodada 3 e uma na rodada 4. O spec repete muito.
- **Mensagens do Maestri chegam no meio do turno.** Os avisos "rodada gravada" chegaram junto com o resultado do ask;
  funcionou, mas o relator precisa ler os arquivos, não os avisos.
- **Heredoc longo no Bash falhou** (aspas no conteúdo); o Write resolveu. Detalhe de ferramenta.
- **Os fatos novos chegaram no meio da rodada 2.** Foi bom tê-los, mas exigiu um bloco extra de votação. Melhor que
  cheguem antes da rodada 1, quando houver.

## Armadilhas que o spec e os tickets escondiam

- **O núcleo se apresentava como decisão.** O `spec.md` resolvia pontos abertos das partes ("vale o conflito visível",
  "o verificador só completa deriváveis") sem ticket. Metade das 34 divergências do Prisma eram isso. Sem a regra do
  protocolo, o núcleo teria virado lei.
- **O mais recente vence, mas não está sinalizado.** O 15 tira o GSD do global; o 36 e o 42 mandam juntar. O 14 tira o
  marcador de raiz; o 36 e o 40 o põem. O `map.md` ainda carrega as linhas antigas. Quem lê só o mapa erra.
- **Rodada respondida em ticket aberto parecia decisão.** O 56 tem respostas do Gustavo (30 dias, dois dias de
  distância) citadas no spec como "(56, rodada 7)". Sem o status do ticket à mão, passa por fechado.
- **"Se couber" escondia requisito.** Validação de frontmatter no MCP (12), Config Doctor (33), ponte do Desktop (11)
  estavam como opcionais por causa do corte de 1 hora. O corte é formato; o requisito não.
- **Garantia com exceção silenciosa.** "Nenhuma gravação sem guarda de versão" (11) e, logo abaixo, um verificador que
  grava "só campos deriváveis". A exceção não estava em ticket.
- **Resumo do Answer mais frouxo que os comentários.** O 14 resume "link simbólico" para os três harnesses; o teste do
  42 é import no Claude Code. O 14 recomendou "sem modelo" no fim da resposta; a resposta do Gustavo foi outra. Ler o
  Answer não basta; os comentários carregam a decisão real.
- **Fato de bancada tratado como decisão.** "DESCONHECIDO" sem vigia e sem MCP era saída do script de teste, não
  terceira fonte decidida. Serviu como evidência, não como fonte.
- **Mesmo conceito, três redações.** A pergunta "login no HOME de ensaio" aparecia em cada parte com texto diferente.
  Uma nota só no núcleo resolveu.
- **Escopo de hook ambíguo.** "Sai na hora fora do hub" (14) contra "acervo serve a todo maestro, dentro ou fora" (40).
  Os dois tickets falam de hooks diferentes sem dizer isso. Precisou de leitura conciliadora, marcada [núcleo].

## Recomendações para a próxima revisão

- Começar com a regra "o que vale como decisão" e as três marcas já no protocolo. Foi o que mais rendeu.
- Entregar aos revisores, antes da rodada 1, um índice de precedência: para cada tema, qual ticket é o mais recente.
  Evita redescobrir que o 15 vence o 42.
- Marcar no `map.md` as linhas superadas ("vale o 14") em vez de deixar o leitor achar.
- Dar ao relator um passo de propagação explícito: para cada mudança, listar todos os lugares do spec onde ela aparece,
  antes de aplicar. Teria evitado a rodada 3 de correções.
- Fatos novos do Gustavo: antes da rodada 1 ou numa rodada própria, nunca no meio.
- Pedir aos revisores a conferência por diff desde a rodada 2, não só na 4.

## Recomendações para o plano de construção

- **Tirar a repetição do spec.** Uma decisão em um lugar só, e as partes apontam para ele. Hoje a mesma frase mora em
  quatro arquivos e diverge.
- **Pedir o aval das 23 escolhas [núcleo] antes de construir**, em bloco, uma rodada só. Algumas mudam o desenho
  (duas instâncias do MCP, verificador com releitura, hooks do acervo fora do hub).
- **Fechar as perguntas abertas do 16** (login de ensaio, pilotos do vault, cota do gemini) antes de despachar as
  faixas 2, 3, 5, 6 e 8: as provas de ponta a ponta dependem delas.
- **Com etapas sequenciais, trocar dublê por entrega real** e tirar os minutos; os "se couber" voltam a entrega cheia.
  A proposta já diz o que muda, sem ordem; a ordem é do Gustavo.
- **O 56 fica fora.** Nada de `limpar-arquivo` com prazo até o 56 fechar.
- **Confirmar o fato 4 com o Gustavo:** Docker ligado inclui CouchDB de ensaio em contêiner durante a construção?
- **Três lacunas de dono do 16 seguem sem dono:** registro do aval de mudança no contrato, modelo do verificador da
  guarda, erro de peça citada que sumiu. Decidir antes da faixa 9.
