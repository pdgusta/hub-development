# Perguntas ao Gustavo (descrição de design do hub, versão 1)

2026-10-15, Tech lead. Só o que é prática sua e as fontes não dizem. Cada pergunta muda o desenho; a descrição marca
o ponto com [G, número]. Ordem: as que mais mudam o desenho primeiro.

1. **Suas máquinas ficam ligadas juntas no dia a dia? Você desliga, hiberna ou fecha o notebook à noite e fora do
   expediente?**
   Por que importa: a troca entre os bancos só acontece com as duas ligadas. Isso define quanto tempo uma mudança
   espera, quão frequente é "a outra máquina desligada" e quanto cresce o risco de colisão. A fonte só diz que elas
   "costumam ficar ligadas juntas".

2. **Quando você pede a um agente para ler, alterar ou remover algo do hub, por onde pede no dia a dia: Claude Code na
   raiz, um workspace do Maestri, o Claude Desktop, o VS Code, outro?**
   Por que importa: a porta principal no desenho é a sessão na raiz. Se a sua prática é outra, os cenários e o
   diagrama de "quem chega" mudam de centro.

3. **Quando você cria uma nota nova no Obsidian, onde ela deve nascer: em `inbox/`, na pasta da iniciativa aberta, ou
   onde você clicar?**
   Por que importa: o Obsidian tem uma pasta padrão para nota nova; o hub não decidiu qual. Nota solta sem lugar vira
   órfã, que é o que o hub quer evitar.

4. **"Remova isto" para você quer dizer apagar ou arquivar? E quem decide que uma iniciativa terminou e roda a
   mudança para o `_archive/`: você, ou o agente quando percebe?**
   Por que importa: apagar viaja às duas máquinas em segundos e só volta pela cópia do dia; arquivar é um script que
   confere a outra máquina antes. O cenário "pedir para remover" depende disso.

5. **Você costuma editar no Obsidian uma nota que um agente está trabalhando ao mesmo tempo?**
   Por que importa: essa edição concorrente está fora do escopo e sem proteção. Se acontece com frequência, ela volta
   a pesar no desenho.

6. **Você aceita que conteúdo de cliente vá para o repositório privado do GitHub na cópia diária, e para os modelos
   na nuvem que os agentes usam? Há iniciativa de cliente que não pode?**
   Por que importa: a cópia diária leva toda a vista, inclusive cliente; isso decorre da decisão, mas não foi
   discutido em separado. Uma resposta "não" cria uma exclusão no git ou uma pasta fora do hub.

7. **Que arquivos que não são texto (docx, xlsx, imagem, PDF) você edita nas duas máquinas?**
   Por que importa: na colisão de binário o hub fica com o mais novo sem perguntar, e só a vigia avisa. Se você
   edita planilhas nas duas, esse caso deixa de ser raro.

8. **Quem usa hoje um computador sem cópia do hub: só você numa sandbox ou máquina de passagem, ou também agentes de
   outras pessoas? Com que frequência?**
   Por que importa: o cliente foi desenhado (porta de leitura, chave temporária), mas sem uso conhecido. A resposta diz
   se ele entra no diagrama principal ou fica na borda.

9. **Onde você quer ver um aviso do hub quando está só no Obsidian, sem sessão de agente aberta? A notificação do
   Windows basta?**
   Por que importa: hoje os avisos são a notificação, o estado na tela do agente e a checagem de sessão. Quem só usa
   o Obsidian pode não ver nada além da notificação.

10. **Quantos agentes costumam trabalhar ao mesmo tempo na mesma iniciativa, na mesma máquina?**
    Por que importa: é o caso mais comum de edição concorrente dentro de uma máquina. A guarda de versão cobre a porta
    do banco, mas não a gravação direta no disco, que ainda está em aberto.

11. **Quem cuida da operação: montar uma máquina nova, revogar a chave de uma máquina devolvida, responder um aviso,
    religar o que parou? Você mesmo, ou um agente com você vendo?**
    Por que importa: as fontes dizem o que pode ser feito, não quem faz. A matriz de responsabilidade fica com buracos
    sem isso.

12. **Em que situação você ligaria os embeddings do Google na busca?**
    Por que importa: ligado, o texto indexado vai ao Google e a busca por sentido passa a depender da rede e da cota. O
    gatilho não foi decidido.

13. **O que você pede ao Claude Desktop sobre o hub: só perguntas, ou também alterações em notas?**
    Por que importa: como o Desktop grava está em aberto. Se é só leitura na prática, o caminho fica simples; se
    altera, precisa da guarda de versão.

14. **Você quer chegar ao hub pelo celular ou pela web?**
    Por que importa: hoje nenhum dos dois alcança a rede privada. Seria uma porta nova, com outro caminho de rede.

## v2 (2026-10-15, depois do teste da versão 1)

15. **Você mesmo busca no hub (pelo Obsidian ou pedindo a busca a um agente), ou a busca é só dos agentes? E o Claude
    Desktop deve usar a busca?**
    Por que importa: a busca decidida é servida aos agentes e aos clientes. Se você ou o Desktop também a usam, ela
    ganha mais um caminho (a ponte do Desktop até a busca) e a matriz de responsabilidade muda.

16. **Quando algo é apagado sem querer, você quer recuperar sozinho, pela cópia do GitHub, ou que um agente faça isso
    com você vendo? Um dia de distância na cópia basta?**
    Por que importa: não há lixeira no hub; a exclusão viaja às duas máquinas em segundos. As fontes não dão o
    procedimento nem quem o roda, e o intervalo da cópia diária define quanto se pode perder.

## v3 (2026-10-15, depois das respostas da rodada 7 e do teste da versão 2)

17. **Você aceita que conteúdo de cliente vá para os modelos na nuvem que os agentes usam (Claude, Codex, Copilot)? Há
    iniciativa de cliente que não pode?**
    Por que importa: na rodada 7 você liberou o cliente no repositório privado do GitHub, mas a parte dos modelos na
    nuvem ficou sem resposta. Todo texto que um agente lê vai ao provedor do modelo.

18. ~~Uma sessão fora do hub, como cliente, deve também gravar no hub?~~ **Respondida** no ticket "Como os agentes
    gravam no hub", rodada 1 (2026-10-15): gravação ligável; o padrão segue só de leitura; quando o Gustavo quiser, o
    cliente recebe o token de uma segunda instância da porta do banco, com escrita e a mesma guarda de versão, só na rede
    privada; a senha do banco fica só nos pares. Já está na descrição (marca [R11]).
