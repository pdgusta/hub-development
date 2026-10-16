# Mapeamento da frente context-hub (/wayfinder, modo "traçar o mapa")

Registro das rodadas de grilling que fixam o destino e a fronteira do mapa. O mapa (`map.md`) nasce
depois delas e aponta para cá. Cada rodada é gravada quando acontece.

## Ideia de entrada (Gustavo, 2026-09-30)

> Ter um context hub único, com arquivos markdown como fonte da verdade, hospedado neste computador e
> replicado em outro computador, da forma que:
> 1. agentes (Claude Code, Codex, OpenCode, dentro ou fora do Maestri), em qualquer das duas máquinas,
>    achem o trecho certo sem ler tudo, por RAG;
> 2. o que importa seja gravado no lugar certo sem ele pedir, por um contrato file-first com zonas e checkpoint;
> 3. os arquivos markdown continuem editáveis no Obsidian com o RAG/sistema sempre acessível pelo agente
>    para busca e store, mas também que seja possível o agente editar diretamente no disco (e
>    consequentemente sincronizado com a outra máquina);
> 4. nada diverja em silêncio entre as máquinas;
> 5. exista uma proteção de sync para quando tiver edição simultânea na mesma pasta.
>
> Ainda não faço ideia exatamente por onde começar, nem sequer se a ideia faz sentido.

**Diferenças em relação ao objetivo da §7.1 da exploração:**
- "hospedado no computador com mais disco" virou "hospedado **neste** computador". Este computador é o
  notebook da ARMIS (`ARMIS00323`, disco C: com 372 GB usados e 84 GB livres, levantado em 2026-09-30).
- "camada de busca" virou "RAG", e a camada agora também serve para **store** (gravar), não só buscar.
- "dado sensível não vá para onde não deve" saiu do item 4.
- O item 5 (proteção contra edição simultânea) é novo.

## Rodada 1 (2026-09-30): destino e escopo

Perguntas feitas ao Gustavo, com a recomendação de cada uma. Respostas: pendentes.

- **Q1. Que tipo de destino?** Recomendação: o mapa termina quando não falta nenhuma decisão para
  rodar `/to-spec` do hub final. Construir o hub fica para `/to-tickets` → `/implement`.
- **Q2. O que fica dentro e fora deste mapa?** Recomendação: dentro, o hub em si (armazenamento,
  sync, busca, contrato file-first, convivência com o Obsidian e o acesso dos agentes de dentro e de
  fora do Maestri). Fora, a migração dos workspaces existentes, o redesenho do conteúdo do vault, a
  skill de aplicar/auditar do Maestri e a convivência dos frameworks de processo.
- **Q3. Dado de cliente saiu de propósito?** Recomendação: volta como restrição do destino.
- **Q4. "Edição simultânea na mesma pasta" é qual cenário?** Recomendação: os três (duas máquinas
  entre syncs; dois agentes na mesma máquina; Obsidian e agente no mesmo arquivo), cada um com
  mecanismo próprio.
- **Q5. "Store pelo sistema" reabre a §9 (disco como única verdade)?** Recomendação: não. Toda
  gravação termina como arquivo no disco; a camada de busca pode oferecer ferramenta de gravação por
  conveniência.
- **Q6. "Hospedado neste computador" quer dizer o quê?** Recomendação: o notebook da ARMIS guarda a
  cópia de referência; a outra máquina é réplica com direito de editar.

### Respostas da rodada 1 (Gustavo, 2026-09-30)

- **Q1: (b), o hub construído e funcionando nas duas máquinas.** Isto contraria a recomendação.
  Como (b) se encaixa no fluxo `/to-spec` → `/to-tickets` → `/implement` vai para a rodada 2.
- **Q2: "concordo em partes".** Que partes ainda não se sabe; vai para a rodada 2.
- **Q3: dado de cliente não é restrição.** "Essa regra eu criei de bobo: o dado do cliente vai
  continuar tão protegido lá na outra máquina quanto é protegido nessa." Sai do destino. A política de
  dados de cliente da §8 e o ticket candidato da §11 caem junto. A regra do AGENTS.md (notas citam a
  iniciativa pelo nome, dados pessoais ficam nas pastas de origem) é outra coisa e continua valendo.
- **Q4: (a) e (b).** As duas máquinas entre syncs, e dois agentes na mesma máquina. O caso (c),
  Obsidian e agente no mesmo arquivo, fica fora, porque ele raramente edita arquivos no Obsidian.
- **Q5: concorda.** Toda gravação termina como `.md` no disco, e a camada de busca pode gravar por
  conveniência. "Camada de busca" entrou no `GLOSSARY.md`, com "RAG" como termo a evitar.
- **Q6: (b), as duas máquinas são pares.** "Majoritariamente são edições incrementais e, quando
  destrutivas, é documentado." "Hospedado neste computador" só diz onde o hub nasce. Entrou no
  glossário como **Máquina**.

Fato levantado: o vault `ai-operating-system` (`~/Documents/Projetos/ai-operating-system`) tem
`.obsidian/` sem plugins da comunidade (sem `community-plugins.json`). Hoje o Obsidian não faz sync nem git.

## Rodada 2 (2026-09-30): fechar o destino e conhecer a outra máquina

Respostas: pendentes.

- **Q7. Como o destino (b) convive com o fluxo do Matt?** Recomendação (C): o destino é o hub
  funcionando, e os cinco itens da ideia de entrada são os critérios de aceite. O mapa decide,
  um ticket de passagem roda `/to-spec` e `/to-tickets` (a construção acontece fora do mapa) e um
  ticket final verifica os critérios nas duas máquinas. Alternativa (A): o mapa carrega a execução
  pela seção Notes e dispensa `/to-spec`.
- **Q8. Que partes da Q2 mudam?** Recomendação: a mesma da Q2, à espera da correção dele.
- **Q9. Como é a outra máquina?** Sistema operacional; pessoal ou corporativa; se fica ligada ao
  mesmo tempo que o notebook; se estão na mesma rede; que harnesses e se o Maestri rodam nela.
  Não há recomendação, porque são fatos que só ele sabe.

### Respostas da rodada 2 (Gustavo, 2026-10-01)

- **Q7: (C).** O destino é o hub funcionando nas duas máquinas, e os cinco itens da ideia de entrada
  são os critérios de aceite. O mapa decide; um ticket de passagem roda `/to-spec` e `/to-tickets`; a
  construção acontece nesses tickets, fora do mapa; um ticket final verifica os critérios e fecha o mapa.
- **Q8: entram no mapa**, além do "dentro" da Q2:
  - "redesenhar a arquitetura do vault para o context-hub";
  - "redesenhar como agentes editam o context-hub";
  - "acesso por ssh";
  - "context-hub em wsl ao invés do windows local";
  - "sistema de sync/busca como mcp";
  - "contrato de roteamento de tarefas pesadas e simples para modelos do AI provider FreeLLMAPI com
    Unified API Key (OpenAI supported)".
  Continuam **fora**: migrar os workspaces do Maestri, a skill de aplicar/auditar do Maestri e a
  convivência entre superpowers, GSD e Matt. "Redesenhar o conteúdo do vault" foi substituído pela
  arquitetura (ver Q10).
- **Q9: a outra máquina** é Windows, pessoal, fica sempre ligada, está quase sempre na mesma rede que
  o notebook (às vezes em outra), roda todos os harnesses e tem Maestri.

Fatos levantados:
- `C:\Projetos\freellmapi` é um clone de [tashfeenahmed/freellmapi](https://github.com/tashfeenahmed/freellmapi):
  agrega tiers gratuitos de vários provedores atrás de um endpoint `/v1` compatível com OpenAI, com
  roteador e failover, e também serve embeddings (README, lido em 2026-10-01).
- `C:\Projetos\freellmapi-mcp` é um projeto do Gustavo (GSD) que delega jobs a workers Claude Code
  headless apontados para o FreeLLMAPI. Ele já tem um contrato de routing de modelos em
  `.claude/CLAUDE.md` (seção "Routing de modelos"), com chains `gsd-fast` e `gsd-smart` configuradas
  no dashboard.

## Rodada 3 (2026-10-01): o sentido dos itens novos e o ponto de encontro do sync

A partir desta rodada, as perguntas vão para `respostas.md` na raiz (pedido do Gustavo) e o chat leva
só um aviso. Respostas: pendentes.

- **Q10. O hub substitui o vault?** Recomendação: sim. O vault `ai-operating-system` deixa de existir
  como casa à parte, a arquitetura dele é desenhada neste mapa, e o conteúdo atual entra no hub como
  parte do destino.
- **Q11. Para que serve o "acesso por SSH"?** Recomendação: transporte do git entre as máquinas, com
  a máquina pessoal (sempre ligada) servindo o repositório de encontro.
- **Q12. "Sync/busca como MCP" quer dizer um MCP só?** Recomendação: o MCP é a interface do agente
  para buscar, gravar e ver o estado do sync, mas o sync roda também sem ele, porque edições diretas
  no disco e no Obsidian precisam chegar à outra máquina.
- **Q13. Qual a ligação entre o roteamento FreeLLMAPI e o hub?** Recomendação: o contrato de
  roteamento passa a morar no hub como documento canônico, e o `freellmapi-mcp` aponta para ele.
  Usar o FreeLLMAPI no próprio funcionamento do hub (embeddings, resumos) é decidido em tickets.
- **Q14. O que a ARMIS permite no notebook?** Repositório privado no GitHub pessoal (terceira cópia
  na nuvem); Tailscale ou outra VPN pessoal; SSH saindo do notebook para a máquina pessoal pela
  internet. Sem recomendação: são fatos de política. Já levantado no notebook em 2026-10-01: WSL 2
  instalado (Ubuntu-24.04 e docker-desktop, parados), cliente OpenSSH do Windows presente, sem
  Tailscale e sem servidor SSH.

### Respostas da rodada 3 (Gustavo, 2026-10-01)

- **Q10: "(a) com parte do conteúdo do vault dentro do destino".** O vault continua sendo casa
  própria, e só certos workloads vão ser testados nascendo no hub, em vez de no vault. "As regras
  restritivas do vault quebraram bastante do valor que ele estava proposto para entregar; não quero
  errar nisso e mais algumas coisas no hub." O hub não substitui o vault agora: os dois convivem, e
  cada workload mora em uma casa só.
- **Q11: SSH para (b) e (c).** (b) quando ele quiser que alguns conteúdos ou subpastas do hub sejam
  acessíveis só por SSH, ou opcionalmente; (c) operar a outra máquina remotamente. Ele perguntou qual
  a vantagem de levar os commits por SSH em vez de um repositório privado no GitHub (respondida na
  rodada 4).
- **Q12: igual à recomendação.** O MCP é a interface do agente (buscar, gravar, ver o estado do sync),
  e o sync roda sem depender de quem gravou. Ele perguntou se isso teria de ser criado (respondida na
  rodada 4).
- **Q13:** o `freellmapi-mcp` está em desenvolvimento e não é desta frente, e a skill que ensina a
  usá-lo também fica fora do mapa. Entra no mapa: essa skill estar no **roteamento de skills do hub**.
  A opção (b), usar o FreeLLMAPI no funcionamento do hub (embeddings), "seria bom explorar" e entra
  como opção nos tickets da busca e do checkpoint.
- **Q14:** repositório privado no GitHub pessoal, Tailscale e conexão SSH são permitidos, "mas
  precisamos explorar formas seguras de fazer isso".

## Rodada 4 (2026-10-01): pastas por SSH, roteamento de skills e lista de tickets

O texto completo está em `respostas.md`, que também responde às duas perguntas dele da rodada 3
(SSH × GitHub privado; se o sync teria de ser criado). Respostas: pendentes.

- **Q15. O que são as pastas acessíveis só por SSH?** Recomendação: chamá-las de **pasta não
  replicada** (mora numa máquina só, fora do sync e do GitHub; a outra máquina a alcança por SSH). O
  mecanismo depende de para que servem.
- **Q16. O que é o "roteamento de skills do hub"?** Recomendação: as skills moram no hub, chegam às
  duas máquinas pelo sync e ficam visíveis em todos os harnesses. Uma tabela de roteamento só existe
  onde a descrição da skill não basta para o agente escolher.
- **Q17. A lista de tickets candidatos está certa?** Recomendação: a lista de 16 tickets do
  `respostas.md`, com os itens das Q15 e Q16 ajustados conforme as respostas.

### Respostas da rodada 4 (Gustavo, 2026-10-01)

- **SSH × GitHub privado:** ele prefere a coexistência. O GitHub privado leva os commits, e o
  Tailscale atende as pastas por SSH e a operação remota. É o ponto de partida do ticket "Ponto de
  encontro do sync", que só fecha depois da pesquisa de formas seguras.
- **Q15: igual à recomendação.** O nome é **pasta não replicada**, e cada pasta escolhe se é
  replicada ou não. Os casos de uso reais vão aparecer com o tempo; os três exemplos (a), (b) e (c) já
  bastam para justificar o SSH. Ele perguntou se não seria melhor o hub morar no WSL, já que o SSH
  direto no Windows "pode ter problemas". **Não verificado:** isso entra no escopo dos tickets "Hub no
  WSL: comportamento" e "Ligar as máquinas com segurança", que comparam o servidor SSH no Windows e
  dentro do WSL.
- **Q16: igual à recomendação.** As skills moram no hub, e a tabela de roteamento só cobre o que a
  descrição da skill não resolve. A skill do freellmapi-mcp é o primeiro caso de teste.
- **Q17: a lista está certa**, com uma ressalva: "nem todas vamos conseguir fechar ou ter algo
  palpável só em conversa". Por isso, no `map.md`, os tickets 8, 10, 11 e 12 viraram `prototype`, e
  qualquer ticket `grilling` pode virar protótipo ou abrir uma pesquisa quando a conversa não fechar.
  O antigo ticket 13 ("pesquisa e depois conversa") virou dois, "Acesso dos agentes: pesquisa" e
  "Acesso dos agentes: decisão", e por isso a lista agora tem 17 tickets.

Com a rodada 4, o grilling de mapeamento acabou. O mapa está em [`map.md`](map.md).
