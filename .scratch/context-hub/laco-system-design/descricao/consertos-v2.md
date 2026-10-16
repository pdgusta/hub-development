# Consertos da descrição, volta 2

2026-10-15, Tech lead. Fonte dos buracos: `teste/resumo-volta-1.md` e `teste/diagramas/*.md`. Conserto por eixo, não por
pergunta. A v1 está em `descricao-do-hub-v1.md`.

## Regras novas que valem para o texto todo (seção 0)

- Marca **[L]** para leitura minha tirada de afirmações decididas, separada de [D].
- **Construído × desenhado:** peça decidida que ainda precisa ser construída leva "a construir" (resolve o "sim como
  fato" da guarda de versão, que a v1 dava como funcionando em alguns cenários).
- **Lugar × grupo**, com regra para desenhar grupo que atravessa lugares (mapa de grupos).
- **Quem é "agente":** maestro, recrutas e subagentes entram; Claude Desktop não (matriz, ambíguo 5).
- Sinônimos novos: senha do banco ≠ token ≠ frase-senha.

## Atores (seção 2)

- Coluna "onde está" para todo ator; Claude Desktop roda na máquina (resolve a contradição "fora do par").
- "O par" declarado lugar, não ator; Agendador do Windows entrou como ator.
- Cliente: quem está nele não tem vista nem Obsidian; quem dá a chave é o Gustavo.
- Hooks rodam dentro da sessão, configurados no escopo do usuário (resolve o ambíguo hooks × sessão).

## Componentes (seção 3)

- Inventário completo: entraram assistente do plugin, regra de exclusão (vive no sincronizador e no plugin), ponte
  `mcp-remote`, mod de estado, comando de recuperar binário, script do `_archive/`, kit de par, tarefa diária,
  propostas, registro de uso, variante de setup, catálogo de blocos, pasta do papel, Tailscale da empresa.
- Tabela "o que cada ferramenta recebe da disciplina" (Claude Code, Copilot, Codex): contrato na raiz e em subpasta,
  checagem, checkpoint, estado na tela, guarda (com o motivo técnico do Codex e do Copilot), hooks, pastas de skills.
- Corrigido: o Claude Code lê a cadeia de `AGENTS.md` sozinho (decidido, não em curso); o Codex precisava de marcador
  no teste e o `.git` no lugar dele está em curso e não testado com o hub.
- Busca: só lê; a contradição com o glossário ("pode também gravar") ficou explícita.
- Porta de leitura: `READ_ONLY` na instância, recusa no servidor, texto em claro ao cliente (tem a frase-senha).
- Porta do banco: guarda de versão e aviso de conflito "a construir".
- Plugin também escreve no disco; plugin e sincronizador juntos não criam ciclo.
- Por que não há `CLAUDE.md`; modo de desenvolvedor para os links simbólicos; Funnel nunca, e nada detecta se ligado.
- **Errada corrigida (pasta não replicada):** a outra máquina a alcança por SSH (glossário; OpenSSH escolhido em
  "Ligar as máquinas com segurança"); SSH só monta quando surgir o caso. Separadas as duas classes de "fica fora"
  (declarada × pasta com ponto) e dito que raiz e não replicação são critérios independentes.

## Responsabilidade (seção 4)

- Matriz refeita, completa: todo componente de 3.1 a 3.3 com dono, aciona, lê, só vê e **aprova**, em cinco blocos.
  Dono sempre um ator; "—" para ninguém; [G] onde só o Gustavo sabe; [A] para lacuna.
- Resolvidos os ambíguos: dono do acervo (Gustavo) e quem acrescenta (maestro); o Gustavo **aprova** na guarda, não só
  vê; o checkpoint obriga e o agente grava; dono da nota de retomada é o Gustavo (como todo conteúdo) e quem a mantém é
  o agente.
- Entraram: propostas lidas por um maestro no Claude Code; Designer só desenha e o maestro só pede; controle de acesso
  por pasta é do Gustavo, depois; limite de 200 MiB fixado pelo Gustavo e aplicado por configuração; versão local do
  papel vai para a biblioteca do workspace; por que o aval é só para poucas coisas (falha do vault).
- Tela do pedido de aval do acervo com os cinco itens.

## Pertencimento (seção 5)

- Grupos ampliados (todos os componentes têm grupo) e grupo novo "ferramentas da máquina".
- Lugares aninhados na máquina: disco, banco, processos, tarefas agendadas, configuração do usuário, configuração do kit,
  perfil do Maestri, apps, sessão, área de notificação.
- Lugar único × grupo duplo, ligado ao princípio "cada informação tem um lugar só".
- Contradição com "Workloads piloto" resolvida: a frente nasce no hub quando ele existir; hoje mapa e tickets vivem no
  repositório da prova de conceito.
- **Errada corrigida (segredo em pasta com ponto aninhada):** o defeito medido está em 8.16 com todas as letras: pastas
  com ponto aninhadas foram ao banco e à outra máquina; até o teste, segredo ali não está protegido.

## Ligações (seção 6)

- Motivo de cada par enviar as próprias mudanças (o aviso nasce na máquina que travou).
- Entraram: plugin ↔ banco, SSH até a pasta não replicada, propostas → maestro, maestro → biblioteca do Maestri,
  agentes do notebook → FreeLLMAPI (quem o chama).
- Tempos: ~2 s medido com um banco só; tempo pela rede não verificado.
- Instruções do MCP × descrição das ferramentas: só a descrição chega nos três.
- O acervo vale fora do hub.

## Ações práticas (seção 7)

- Entraram: aplicar partitura exige a interface ou a API Wire; partitura como porta do acervo (o Gustavo cria e pede
  para guardar); recuperar algo apagado; montar uma máquina nova; responder rodada; maestro avalia propostas e pede
  visuais; agente que acha o contrato desatualizado edita só dentro do hub.

## Cenários (seção 8)

- Junção automática depende da versão comum ainda estar no banco.
- Unidade da colisão: detectada por trecho, retém a nota inteira; o disco de cada máquina fica com a versão local
  (o plugin segura a descida); a resolução segue o caminho de uma gravação normal.
- Aviso só na máquina que travou; a outra não recebe aviso próprio.
- Banco local caindo e rede caindo: o sincronizador sobrevive e o que mudou chega na volta.
- Papel do Maestri: o que Claude Code, Copilot e Codex recebem; reiniciar o terminal não regrava o papel; guarda só na
  raiz do workspace não alcança o papel.
- Na raiz, a pasta não diz o trabalho: o agente acha a nota pela busca, pelo nome ou pergunta.
- Cliente: recusa no servidor, por que nunca a credencial, proteção do computador de passagem sem decisão.
- Par novo: ordem que as fontes dão, com o que falta.
- Busca sem internet funciona (modelo local).
- Empresa bloqueando o Tailscale; chave do nó vencendo.

## Estado (seções 9 e 11)

- O hub não apaga por idade (compactar ou arquivar).
- Guarda de versão listada como "a construir" no topo da tabela.
- Pendências com a conta da empresa entraram.
- Lacunas sem dono reunidas numa linha.

## Outro

- Por que um banco em cada máquina (sem servidor fixo; nuvem fora porque o Gustavo quer algo pronto logo).

## Perguntas novas ao Gustavo (v2)

- 15: se ele e o Claude Desktop usam a busca.
- 16: como recuperar algo apagado e se um dia de distância basta.
