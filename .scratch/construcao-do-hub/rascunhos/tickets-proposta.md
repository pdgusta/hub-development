# Proposta de tickets da construção (/to-tickets, maestro, 2026-10-16)

Fonte: `spec.md` e `spec-partes/` revistos (23 escolhas aceitas) e o plano decidido (`revisao/plano/proposta-de-etapas.md`,
seção "Decidido"). Fatias verticais, cada uma cabendo numa janela de contexto, com os bloqueios reais. Os 11 tickets
atuais (`issues/01`-`11`, do plano de 1 hora) vão para `issues-tentativa-paralela/` quando estes forem publicados.

| # | Ticket | Bloqueado por | O que entrega, de ponta a ponta | Etapa |
|---|---|---|---|---|
| 01 | Prova: dois CouchDB replicando com o LiveSync | nenhum | nota criada, editada e apagada num par chega ao outro; colisão vira conflito nos dois; E2EE com caminho ofuscado | 0 |
| 02 | Prova: pastas com ponto aninhadas fora do LiveSync | nenhum | nada com ponto, em qualquer nível, chega ao banco nem ao outro disco, também na partida do CLI | 0 |
| 03 | Prova: hooks do Codex em acesso total | nenhum | início, recusa antes do `apply_patch`, fim que devolve e solta, e `notify`, com a pasta de configuração de ensaio | 0 |
| 04 | Esqueleto do hub e hub de ensaio | nenhum | as seis raízes, o `AGENTS.md` com o bloco da cabeça, o `verificar-hub` (estrutura, nenhum `CLAUDE.md`) e o hub de ensaio que as outras etapas usam | 1 |
| 05 | Frontmatter imposto: esquemas, verificador e "nova iniciativa" | 04 | esquemas por tipo; o verificador aceita, recusa e completa o dedutível relendo antes de gravar; o script cria a iniciativa com o núcleo de seis arquivos | 1 |
| 06 | Gerador de exclusões | 04, 02 | a lista do que não replica nem entra na busca (`local: true` e tudo com ponto), lida pelo sync e pela busca | 1 |
| 07 | Banco do par: dois CouchDB, LiveSync e vista `.md` | 01, 04 | nota numa pasta aparece na outra e volta; colisão vira conflito sem perda; nada em claro no banco | 2 |
| 08 | Banco: limites e robustez | 07, 06 | exclusões pelo gerador; 200 MiB; binário perdido num ramo recuperável; kit idempotente; o laço religa; retrato do banco para as etapas seguintes | 2 |
| 09 | MCP do banco: gravar com versão e conflito à vista | 07 | gravar com a versão lida grava; versão velha vira conflito com as duas versões; sem versão é recusado; aviso na leitura e lista de conflitos | 3 |
| 10 | MCP do banco: três instâncias, cabeça, regra curta e estado | 09, 05 | leitura, escrita da máquina e escrita do cliente; cabeça do `AGENTS.md` relida a cada conexão; regra curta; cifra; `estado_do_hub` com estado de exemplo; ficha fora do esquema recusada | 3 |
| 11 | MCP do banco pelos três harnesses | 10, 03 | Claude Code, Codex e Copilot CLI, com a configuração de ensaio, usam o MCP e citam o que receberam dele | 3 |
| 12 | Busca local com aceite | 04, 06 | a busca acha a nota certa entre as 3 primeiras, por palavra e por sentido; mede o tempo da nota nova; conta e lista as recusadas; nada com ponto; endereço estranho recusado | 4 |
| 13 | Gemini pronto e desligado | 12 | a configuração do gemini escrita e desligada; um teste único, se você liberar a cota | 4 |
| 14 | Guardas: regravação inteira e ficha fora do esquema | 05, 03 | nos três harnesses, regravar arquivo existente é recusado e troca de trecho passa; nota que ficaria fora do esquema é recusada | 5 |
| 15 | Guardas: aviso de leitura fora da busca | 14, 12 | ler arquivo grande sem buscar antes dá um aviso por arquivo por sessão | 5 |
| 16 | Vigia: passada, estado e notificação | 08, 10 | a vigia lê o banco real (cifrado), acusa conflito, binário, arquivo grande, sincronizador parado, outro par incerto e Config Doctor; grava o estado; avisa só quando piora; recupera o binário | 6 |
| 17 | Vigia nas telas dos harnesses | 16, 03 | início de sessão com o resumo (e "estado indisponível" sem fonte); `notify` do Codex sem repetir; barra do Copilot; mod do Claude Code | 6 |
| 18 | Retomada: nota de sete campos, início e fim | 04, 17, 03 | o fim da resposta devolve ao agente se a nota não mudou (regra fixa, sem IA) nos três harnesses; a sessão seguinte começa com a nota | 7 |
| 19 | Roteamento de skills | 04 | a tabela e o hook de entrada sem IA injetam "use a skill X"; usar uma skill vira linha no registro | 8 |
| 20 | Acervo do maestro e a guarda dele | 19, 03 | a família `maestro-*`; o lembrete de início com o Maestri; gravar no acervo pede aval no Claude Code e é recusado no Codex e no Copilot, pelo caminho real, pelo atalho e fora do hub | 8 |
| 21 | Arquivar e cópia diária | 08, 16 | arquivar só com o outro par em dia; a cópia diária faz commit e push e, se falhar, sai com erro e acende o item na vigia; conferir a cabeça do contrato | 9 |
| 22 | Proxy e kit de cliente | 10, 12 | um cliente de ensaio busca pelo proxy, lê pela rota de leitura, grava só pela rota do cliente e sem token leva recusa; a ponte do Claude Desktop gerada | 9 |
| 23 | Kit de par: a forma | 11, 15, 17, 18, 20 | o kit, numa pasta de configuração de ensaio, liga contrato, skills de uso geral, MCP e os hooks de todas as etapas; roda duas vezes sem mudar nada e desfaz sem sobra; tira o GSD do global | 10 |
| 24 | Kit de par ao vivo nos três harnesses | 23 | `claude -p`, `codex exec` e `copilot -p` respondem uma pergunta que só o contrato de ensaio sabe | 10 |
| 25 | Junção e prova do hub de ensaio inteiro | 13, 21, 22, 24 | o hub de ensaio inteiro, de ponta a ponta, com todas as peças juntas | 11 |
| 26 | Instalação de verdade no par 1 (com você) | 25 | o kit no seu HOME real, com cópia e hash antes; `ready-for-human` | depois |

**Paralelismo (até 3 agentes):** a fronteira inicial tem 01, 02, 03 e 04 (quatro sem bloqueio); logo depois do 04 entram
o 19 (roteamento de skills) e o 12 (busca, depois do 06). Os tickets 11, 13, 17, 18, 24 e 26 carregam as perguntas de
login, cota do gemini e instalação que você responde na hora; o 20 carrega as três lacunas de dono.
