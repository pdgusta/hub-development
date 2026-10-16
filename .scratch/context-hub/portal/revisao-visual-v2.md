# Revisão do marco visual v2 — Prumo, 2026-10-14

## Parecer vigente: APROVADO após revisão dirigida

Os três achados foram corrigidos e conferidos, dentro do escopo determinado pelo Gustavo. **Marco visual v2 aprovado.** Marco 7 permanece fora deste aceite.

1. **Disponibilidade correta:** na fixture própria, 05 informa “espera 1” pelo ticket 99 inexistente; 07 informa “espera 2” por 03 e 06. Removendo apenas 03 na cópia, 07 continua “espera 1” por 06, apesar do ciclo. Cartão, aria-label, nota e placa concordam; Próximo passo não libera falsamente o 05.
2. **Leitura sempre visível:** a faixa fixa da casca permaneceu inteiramente na janela, separada da área de conteúdo, ao focar critério 5, marco 17, conquista 34, folha 52 e margem 32, em 1280×800 e 1600×900.
3. **Dicas sem cobrir vizinhos:** Designs e Decisões usam a mesma faixa reservada. Conferi decisão de carta, código e eco nos dois tamanhos. Nos 16 casos dirigidos, a faixa estava visível, preenchida e sem sobreposição com a tela. Esc dispensa; com placa aberta também a fecha, devolve o foco ao marco e não reabre a leitura.

Código e capturas próprias conferidos. Não repeti a revisão geral nem as suítes: os resultados de 120 + 4 testes abaixo pertencem à primeira revisão. Evidências desta rodada em `C:/Projetos/context-hub/.maestri/roles/d4ce63fd-ce3e-45b5-88f6-6bbd68695030/revisao-visual-v2-dirigida/` (`resultados.json` e capturas); script `review_visual_v2_dirigida_final.py` na pasta do papel. Alteração de fixture somente em cópia temporária própria; servidor próprio encerrado. Sugestão documental não bloqueia este aceite.

## Primeira revisão — histórico, achados encerrados acima

## Escopo da próxima revisão dirigida — determinação do Gustavo

Gustavo cobrou o prazo e determinou: ao receber a correção, conferir **somente os três achados deste parecer**, sem abrir novos achados de acabamento. **Dica ou nota em área fixa e sempre visível resolve os itens 2 e 3.** Só bloquear por erro de informação (ex.: “pode partir” falso) ou quebra de uso. Não exigir outro desenho/posicionador nem transformar sugestões documentais ou estéticas em pendências. Fazer as provas dirigidas necessárias a esses três pontos; não repetir a revisão geral.

**Ainda não aprovo o marco integrado: três achados importantes abaixo.** A linguagem visual e a composição geral das cinco telas estão coerentes com o aval do Gustavo. Recomendo preservar o desenho e corrigir a leitura dos bloqueios e das dicas, sem abrir outro redesenho.

Revisão de `nucleo/web`, servidor real 8770 só para leitura/captura e servidores próprios em 127.0.0.1 sobre cópias temporárias da fixture. Código, capturas próprias e interações conferidos. Marco 7 continua fora deste aceite; não executei aviso real ao maestro.

## Importantes

1. **Layout tratado como disponibilidade: dependência quebrada ou ciclo pode aparecer liberado.** `telas/torre.js`, funções `espera`, `marco`, `mostrarPlaca` e cálculo de `partem`. `espera` elimina a aresta do ciclo e tickets fora do plano para montar o desenho, mas é reutilizada no estado visível e nas frases. Reproduzi:
   - Fixture original, ticket 05: cartão diz **“pode partir”** junto de “depende de 99, que não existe”; placa diz **“nada aberto; pode andar já”**. O próximo passo também filtra só `bloqueios_abertos`, ignorando `bloqueios_inexistentes`.
   - Fixture original, ticket 07: API tem bloqueadores abertos 03 e 06, mas cartão/placa só mostram 03 e “espera 1”.
   - Na cópia própria, removi apenas o bloqueador 03 do 07, mantendo o ciclo 06↔07. API continua com bloqueador aberto 06, mas cartão 07 vira **“pode partir”** e nota/placa dizem que nada aberto o bloqueia. O aviso de ciclo abaixo do mapa não corrige essa indicação contraditória.
   Recomendo separar **arestas para ordenar/desenhar** de **bloqueios reais para informar disponibilidade**. Contagens, nota, `aria-label`, placa e próximo passo devem respeitar bloqueadores abertos, inexistentes e ciclos; ignorar aresta só para desenhar não libera trabalho. Provas: `fronteiras.json`, `fixture-05-liberado-incorreto.png`, `fixture-ciclo-liberado-incorreto.png`.

2. **Nota de leitura sai da tela ao focar itens baixos.** A doca evita cobrir os cartões, mas fica dentro da mesma região que rola. No Início real em 1280×800, foco em `criterio-5` deixou o alvo visível em y=433 e a nota **inteira fora da janela**, de y≈−80 até −10. Foco em `conquista-34`: alvo em y≈659, nota de y≈−102 até −10. O texto é preenchido no DOM e anunciado por ARIA, mas o usuário que lê visualmente com teclado/mouse não vê a explicação. Recomendo reservar uma área de leitura que continue visível enquanto os pontos são explorados, sem sobrepor cartões; por exemplo, separar a região que rola do espaço reservado à nota. Não basta preservar o conteúdo da doca durante scroll se ela fica fora da janela. Provas: `fronteiras.json`, `criterio-5-doca-1280.png`, `conquista-34-doca-1280.png`.

3. **Evitar vizinhos não está conectado às outras telas.** `torre.js:posicionarDica` procura obstáculos apenas dentro do ancestral `[data-area-dica]`; os únicos atributos dessa área e de `[data-obstaculo]` estão no Início, que usa doca. Nas outras telas, a lista efetiva de obstáculos fica vazia. Em Designs, foquei a decisão de “Contrato de retomada”: a dica ficou sobre o cartão vizinho **“Super Trunfo da busca”**, cobrindo propósito/metadados. Recomendo cadastrar as áreas/cartões efetivos nas telas com dicas flutuantes e testar o posicionamento contra os vizinhos; se não houver lugar sem sobreposição, usar leitura em espaço reservado ou camada explícita. Provas: `dicas.json` (`area=false`, `obstaculos=0`, interseção com Super Trunfo), `designs-dica-sobre-vizinhos.png`.

## O que passou

- Rodei **120 testes do núcleo, OK**, e **4 testes do projeto real, OK**, com **0 problemas** nos arquivos reais. Isso confirma as suítes atuais; os casos acima são de comportamento visual/semântico não cobertos por elas.
- Sete rotas (Início, Tickets, Quem espera quem, Responder, Designs, leitor e Decisões) capturadas nos dois tamanhos. Capturas abertas de todas as telas em 1280, além de Início/Decisões em 1600, nota, gaveta e rodada da fixture. Estilo, fontes maiores, menu de madeira, formulários, leitor e cores mantêm a direção aprovada. Fonte mínima computada nos conteúdos das sete rotas: **14 px**; nenhuma rolagem horizontal da página. A rolagem interna dos grafos é intencional.
- Fontes e bibliotecas carregam localmente. `VERSOES.md` registra as três novas famílias e licenças; nenhum pedido externo apareceu no roteiro com tráfego externo bloqueado. Não fiz nova auditoria de origem/hash dos pacotes.
- Escolha do marco 03, placa atualizada e foco em `placa-soltar` sobreviveram à alteração real do título do ticket na cópia temporária. Gaveta abriu pela placa; Esc devolveu foco a `placa-abrir`.
- Rascunho de resposta sobreviveu à recarga; envio foi gravado na caixa da fixture e relido; Corrigir iniciou com cópia do texto aceito. Chip de filtro de Tickets desliga no segundo clique.
- Leitor fecha por Esc, volta a `#/cartas` e devolve foco à carta. Dica de No horizonte aparece com foco e Esc a dispensa. Redução de movimento desliga o anel na fixture.
- Nota por hover do 16 no real permaneceu estável após um pequeno aumento de altura (64→≈93 px), sem oscilação no roteiro; Esc com placa fechou placa, restituiu foco e pôs a nota em repouso. O problema da doca é a posição depois de rolar, não seu preenchimento.
- Ciclo, volta pontilhada, dependência inexistente e “espera você” aparecem na fixture; nenhum erro JS. Exibir os avisos é bom, mas precisa corrigir as frases de liberação do achado 1.

## Sugestão documental

Atualizar `proposta.md` para que tema, fontes, títulos das telas e forma do Início reflitam a versão aprovada e construída. O diário tem o aval e a implementação, mas a proposta ainda descreve partes da Torre noturna. Não é novo pedido de autorização; é alinhar o contrato de leitura para a retomada e a conferência final.

Evidências próprias em `C:/Projetos/context-hub/.maestri/roles/d4ce63fd-ce3e-45b5-88f6-6bbd68695030/revisao-visual-v2/`: `resultados.json`, `fronteiras.json`, `dicas.json`, PNGs. Scripts no diretório pai: `review_visual_v2.py`, `review_visual_v2_fronteiras.py`, `review_visual_v2_dica.py`. Servidores próprios encerrados; cópias temporárias preservadas. Mensagens e alterações de ticket só nas cópias próprias; nenhuma escrita de teste no projeto real.
