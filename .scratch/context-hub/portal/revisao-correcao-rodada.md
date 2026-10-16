# Revisão dirigida — rodada alterada e edição contínua

Prumo, 2026-10-14. **APROVADAS as duas correções.** Sem bloqueantes ou importantes nestes dois pontos; não reabri acabamento nem a revisão geral.

Li o relato original do Gustavo no envio `65ca59e5-e284-4bed-ac34-83105da2b850`, o contrato da §3.7, os fontes alterados e a prova do Designer. Executei **127 testes do núcleo OK** (41,755 s) e **4 do projeto real OK**, com 0 problemas nos arquivos reais.

1. **Rodada reescrita volta a esperar:** na cópia própria, respondi, alterei o arquivo e conferi contador 1, carimbo MUDOU, aviso, formulário novo e resposta anterior. Copiei a resposta anterior e enviei novamente: JSON gravado com `rodada.base` atual e `substitui` apontando para o arquivo anterior; rodada respondida e contador 0. A suíte cobre também rodada absorvida/suspensa, regravação idêntica, ausência de base e recusa do envio sobre base antiga.
2. **Atualização não interrompe escrita:** em Edge headless 1280×800, mantive o mesmo nó de texto, foco, seleção 3–8, valor e rolagem ao alterar outro ticket e a própria rodada. Os details continuaram abertos. Alterar a rodada durante edição exibiu “Ver a versão nova”; a transição explícita ofereceu copiar o rascunho e conservou o texto. Comentários da gaveta e da tira do leitor também preservaram nó/foco/seleção/texto após atualização; o corpo da gaveta recebeu o texto novo do ticket. Zero erros JS no roteiro. Capturas próprias abertas e conferidas.

A prova fornecida pelo Designer complementa com edição da proposta, rascunho persistido, rolagem interna da gaveta e mais um ciclo após a alteração da própria rodada. Não tratei o JSON fornecido como substituto das provas próprias acima.

Evidências próprias em `C:/Projetos/context-hub/.maestri/roles/d4ce63fd-ce3e-45b5-88f6-6bbd68695030/revisao-correcao-rodada/` (`resultados.json` e quatro PNGs); script `review_correcao_rodada.py` na pasta deste papel. Cópia em caminho curto (`C:/tmp/pr-63l9tsm5/h`), preservada; servidor próprio encerrado. Nenhuma escrita na caixa real nem aviso de teste ao maestro.

**Fora deste aceite:** falha com caminhos acima de 260 caracteres, declarada pelo Designer e ainda não corrigida. Não foi investigada nesta revisão; continua pendência separada, sem ser encoberta pelo aceite destes dois defeitos.
