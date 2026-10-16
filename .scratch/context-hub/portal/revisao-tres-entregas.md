# Revisão dirigida — três entregas, Prumo, 2026-10-14

**Aprovadas a regra de carta substituída e a carta `prototipo-12-ritmos`. Amostra do System design aprovada para apresentar ao Gustavo**, sem substituir `system-design.html` antes do aval dele. Sem bloqueantes ou importantes pendentes nestes três itens; não reabri acabamento.

## 1. Carta substituída

Código e contrato conferidos: `substitui` é interpretado na leitura, os campos derivados não regravam `cartas.json`, a situação original fica intacta e a antiga passa para o arquivo histórico. Ligações inválidas geram problema; conflito de duas substitutas segue a regra documentada de última entrada. Cadeias apontam a sucessora direta; mestra não é substituída por esta regra.

Execução própria: **135 testes do núcleo OK** (39,991 s), incluindo os oito de substituição, e **4 reais OK**, com 0 problemas. Em cópia curta própria, carta vigente substituída saiu das vigentes, recebeu selo e ligação; clique abriu a nova e o leitor da antiga mostrou “substituída por Regas novas”. Bytes de `cartas.json` idênticos antes/depois da leitura. Captura própria aberta e conferida.

## 2. Carta da rodada 11 do ticket 12

Conferi os seis totais e todas as parcelas mostradas contra `exploracao/anexos/levantamento-12-iniciativas.md`, §2b: 337, 190, 181, 58, 41 e 40 mil caracteres. Contexto/Decisões/Pendências/Atualizações conferem linha a linha. A parcela “ficha, estado e fontes” é o restante calculado dos números arredondados: 6, 14, 29, 6, 3 e 7 mil, respectivamente; não é nova medição independente. As 30 iniciativas estão na §1. Texto renderizado e captura inteira conferidos: sem nomes de pessoas; iniciativas/clientes permanecem identificados.

## 3. Amostra do System design

Conferi o comentário original do Gustavo (envio `0a4d5c78-a55d-4f5b-9784-120175398c55`) e abri a amostra nos dois tamanhos, em `file:` e iframe com `sandbox="allow-scripts"`. Nas quatro combinações, prova própria confirmou:

- paridade exata de **124 textos**, com multiplicidade, sem faltas nem acréscimos no desenho;
- documento sem rolagem horizontal/vertical;
- botão direito arrasta; Ctrl+roda aumenta o zoom; Shift+roda desloca horizontalmente;
- card abre ficha e Esc fecha; enquadramento disponível; zero erro JS no roteiro.

Capturas próprias de enquadramento e ficha abertas. A forma de planta técnica, papel claro, traços e hachuras muda o estilo e preserva a leitura como diagrama de arquitetura. O gosto final é do Gustavo; este parecer autoriza apresentar a **amostra**, não trocar o design vigente.

## Dependência externa corrigida durante esta revisão

As duas páginas novas inicialmente buscavam fontes no jsDelivr. Avisei o Designer; ele embutiu as famílias escolhidas em `data:` no HTML, sem refatoração. Provas próprias após a mudança: zero pedidos externos nas páginas testadas; Barlow Condensed e Architects Daughter carregadas em `file:`; Fraunces, Nunito Sans e JetBrains Mono carregadas no iframe isolado da carta servida pelo portal real. Achado encerrado nestas duas páginas. No retorno, Designer declarou que as cartas históricas/substituídas `prototipo-12-miolo` e `prototipo-12-blocos` ainda usam jsDelivr: dependência externa registrada fora do escopo desta rodada, sem aceite de funcionamento offline delas.

Evidências: `C:/Projetos/context-hub/.maestri/roles/d4ce63fd-ce3e-45b5-88f6-6bbd68695030/revisao-tres-entregas/` (`resultados.json`, `fontes.json`, PNGs); script `review_tres_entregas.py` na pasta deste papel. Escrita só na cópia curta da fixture; servidores próprios encerrados. Nenhuma escrita na caixa real nem troca do System design vigente. Pendência separada de caminhos longos continua fora deste escopo.
