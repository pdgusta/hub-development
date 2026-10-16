# Matriz de responsabilidade: teste da descrição v3

Fonte única: `descricao/descricao-do-hub.md` (v3). Nenhum outro arquivo, nenhuma busca, nenhuma web.
Desenho: `diagramas/matriz-responsabilidade.html`.

## Faltou

Itens que a matriz precisava e a descrição não deu. Cada um com a seção onde deveria estar.

**Componentes sem linha na seção 4** (a seção 4 é a fonte da matriz):
- F1. **Núcleo da iniciativa** (`initiative.md`, `retomada.md`, `tasks.md`, `decisions.md`, `context.md`, `log/`): está em 3.2, sem linha em 4.4. Dono só pela regra "Gustavo é dono de todo o conteúdo" (4, regras da matriz).
- F2. **Blocos da iniciativa**: 3.2, sem linha em 4.4.
- F3. **Variante de setup**: 3.2, sem linha em 4.4.
- F4. **Skills do hub** (`agents/skills/`): 3.2, sem linha em 4.4; 4.4 traz só o catálogo de blocos e a skill "nova iniciativa".
- F5. **Cliente** (computador ou sandbox) como componente: 3.3 e 5.2 falam dele, mas 4.5 não tem linha. Dono não dito em nenhuma fonte.
- F6. **Rede da empresa (Tailscale da empresa)**: 3.3 tem o risco e a dispensa do TI; 4.5 não tem linha.
- F7. **Vault `ai-operating-system`**: 3.3 e 12 dizem "só referência"; nem 4.4 nem 4.5 têm linha, e o dono não é dito.
- F8. **Portas de entrada** (3.4): sessão na raiz, Maestri, Claude Desktop, cliente pelo MCP. Têm estado e alcance em 3.4, mas nenhuma linha em 4 com dono, aciona, lê e só vê por porta.

**Lacunas que a própria descrição marca como sem dono** (cabem em "Aciona" ou "Só vê"):
- F9. **Quem religa a vigia quando ela para** e quem percebe que parou: 4.2 não diz; 8.18 "Vigia: [A]"; 11 lista como lacuna.
- F10. **Quem percebe quando o checkpoint ou a checagem de sessão falha**: 4.3 "quem percebe se falhar [A]"; 8.3 "hook que falha sem aviso: [A]".
- F11. **O que o agente faz com a porta do banco fora do ar** (grava pelo disco ou espera?): 8.6 "não está decidido [A]"; 8.5 e 8.18 "[A]". Afeta a linha Aciona da porta do banco.
- F12. **Quem restaura a cópia do GitHub e o procedimento**: 4.5 "[G, 16]"; 8.15 "o procedimento e se um dia basta [G, 16]".
- F13. **Quem confere os 30 dias do `_archive/` e apaga** (tarefa, hook ou pedido): 8.7 "[A]"; 11 "lacuna".
- F14. **Quem atualiza a cabeça do contrato no MCP** (o começo que o cliente recebe): 8.10 "quem a atualiza [A]"; 11 "lacuna".

## Inventei

- I1. **Formato.** A brief pede SVG embutido. Fiz uma tabela HTML com CSS embutido, sem CDN nem rede: uma matriz é uma grade, e um SVG com 60 linhas de texto ficaria ilegível em telefone. Não sei se o teste pede SVG de propósito.
- I2. **Dono "Gustavo" por regra, não por linha.** Aplicado a Verificador (4.3 não diz quem mantém o modelo), Núcleo da iniciativa, Blocos, Variante, Skills, Sessão na raiz, Maestri e Cliente pelo MCP. A regra está em 4 ("Gustavo é dono de toda a infraestrutura... e de todo o conteúdo"). Em Cliente (F5) deixei "não dito", porque o computador não é dele.
- I3. **Alcance dos hooks.** Checagem de sessão e checkpoint foram desenhados como o 4.3 os descreve, que é o Claude Code. Copilot e Codex diferem (3.1, tabela "O que cada ferramenta recebe"). A matriz não mostra essa diferença por célula; só remete à tabela.
- I4. **Coluna Aprova omitida.** A brief pede quatro colunas (dono, aciona, lê, só vê). A seção 4 tem a quinta, Aprova. A informação existe na fonte, mas não entrou no desenho.

## Ambíguo

- A1. **Vigia: Lê ou Só vê?** A regra da seção 4 diz que "Só vê" é quem "enxerga o estado sem usar o conteúdo". A vigia lê estado, então por essa regra fica em "Só vê". Mas 4.2 põe banco, sincronizador e plugin na coluna "Lê" da vigia, e 4.1 põe a vigia em "Só vê" de banco, sincronizador e Obsidian. As duas colunas dizem coisas diferentes sobre o mesmo par. (Seções 4 regras, 4.1, 4.2.)
- A2. **Claude Desktop grava ou só lê?** Seção 2 diz "gravar é requisito [R7]". 3.4 diz "Leitura pela ponte". 4.1, Porta do banco, põe o Desktop só em "ler". 8.17 diz que a forma de gravar está "[A]". A matriz mostra leitura e marca a gravação como pedida, sem caminho. (Seções 2, 3.4, 4.1, 8.17.)
- A3. **Porta de leitura: aprova gravação?** 4.1 põe "Gustavo libera gravação a cliente (padrão: não)" na coluna Aprova da porta de leitura. 3.1 e 8.10 dizem que a porta de leitura é uma instância `READ_ONLY` que recusa gravação no próprio servidor, e que a gravação ligável é uma **segunda instância** com escrita [R11]. Não fica claro se a porta de leitura passa a gravar ou se é outra peça. (Seções 3.1, 4.1, 8.10.)
- A4. **Cópia no GitHub: restaurar é leitura ou ação?** 4.5 põe "Gustavo, em restauração" na coluna Lê. 8.15 e 8.7 dizem que quem restaura é "um agente com o Gustavo vendo [R7]", e isso é ação, não leitura. A matriz segue a coluna Lê do 4.5 e põe a ação em Aciona. (Seções 4.5, 8.7, 8.15.)
- A5. **O agente pode editar o contrato?** 4.3 põe, em Aciona do Contrato, "agente edita só dentro do hub". 4.6 diz que mudar o contrato "pede aval". 7.2 diz que o agente que acha o contrato desatualizado "edita só dentro do hub... mudar pede aval". Não fica claro se o agente pode editar o contrato com aval ou se não pode. (Seções 4.3, 4.6, 7.2.)
- A6. **Dono da nota de retomada.** 4.4 põe "Gustavo (como todo conteúdo)". A regra de dono da seção 4 diz que, "quando a fonte dá a um agente a decisão do dia a dia, a coluna diz". A fonte diz que o agente da sessão escreve a nota a cada resposta (checkpoint), mas a coluna Dono não diz isso. (Seções 4 regras, 4.4.)
- A7. **Por onde o agente grava?** 4.1 põe "agentes (ler e gravar)" como Aciona da porta do banco. 7.2 e 8.2 mostram gravação direta no disco, sem conferir a versão. 11 diz que "como os agentes gravam" está aberto. A matriz mostra os dois caminhos em linhas diferentes, sem escolher. (Seções 4.1, 7.2, 8.2, 11.)
- A8. **Controle de acesso por pasta como linha.** A célula Dono tem "Gustavo vai desenvolver depois, fora deste projeto". Isso é um plano e não um ator. A seção 9 diz que o hub "não controla acesso por pasta". Eu deixei a linha com "Gustavo, depois", mas a descrição não diz se o componente existe no hub. (Seções 4.5, 9, mapa.)
