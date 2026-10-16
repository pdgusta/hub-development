# Consertos da descrição, volta 3

2026-10-15, Tech lead. Fonte: `teste/resumo-volta-2.md` e `respostas-do-gustavo-v1.md`. A v2 está em
`descricao-do-hub-v2.md`.

## O padrão das parciais e o conserto de fundo

As respostas paravam no meio porque cada cenário contava um caminho e parava antes do "e depois?": o que o outro lado
vê, o que fica no banco, quem é avisado, quem age. Dois consertos estruturais, que valem para perguntas que nenhum
cenário conta:
- **8.0 Regras gerais de comportamento:** 17 regras (versões e histórico, texto × binário, colisão por trecho e retenção
  por nota, disco × porta, esperar sem perder, aviso só onde travou, as três divergências e o que não é divergência,
  divergência fica até alguém agir, busca só do disco local, remover = arquivar, aval, operação, cliente, concorrência).
  O topo do texto manda começar por elas e seguir até o fim.
- **8.18 Falhas por componente:** para cada componente que para (banco, sincronizador, plugin, porta do banco, porta de
  leitura, busca, vigia, hooks, rede, outro par, FreeLLMAPI, GitHub, assistente do plugin): o que continua, o que para,
  quem é avisado, quem age.

## Cenários

- 8.1: concorrência na mesma máquina nos três caminhos (edição já no banco, só no disco, os dois no disco) e o "depois em B".
- 8.2: arquivo que já estava no banco e cresce além do limite (fica a versão velha na outra); o limite é por arquivo; "depois em B".
- 8.3: busca fora do ar até o fim; sessão fora do hub como cliente (requisito do Gustavo).
- 8.4: peça que sumiu do acervo; como o recruta usa uma peça.
- 8.5: porta do banco fora do ar.
- 8.6: com guarda × sem guarda até o fim (o que some, onde fica, o que o outro par recebe); gravação do outro par entra como conflito, não é recusada; porta fora.
- 8.7: reescrito com remover = arquivar 30 dias; mover é gravar destino e apagar origem; `_archive/` replica, vai ao GitHub e é indexado; volta do arquivo; mover entre raízes.
- 8.8: só a porta do outro par caiu; o que o Gustavo e o agente veem.
- 8.10: de onde vem a instrução do MCP; conflito pela porta de leitura; como o cliente escolhe o par; o que ele vê; Maestri num cliente.
- 8.12: o hub não escolhe em texto; versão não escolhida fica no histórico; tela de três vias é fork da janela do plugin; notas novas com o mesmo caminho; conflito só no frontmatter; conflito nunca resolvido; leitura do conflito em outra máquina.
- 8.13: queda curta; quando o aviso nasce (até ~20 min); dias parada até o fim; outros arquivos da pasta viajam.
- 8.15: por que um ramo por máquina; quanto se pode perder; quem restaura.
- 8.16: arquivo com ponto na raiz testado fora do banco; git e pastas com ponto aninhadas.

## Componentes

- Por que um limite de 200 MiB (pedaços de binário que se acumulam; o banco não é o gargalo).
- Por que pastas com ponto ficam fora e o efeito na organização (`agents/` sem ponto).
- Por que seis raízes; onde moram STRATA e uma frente da VOEGOL.
- Busca: mesmo modelo nas duas máquinas, reindexação depois da troca, onde ficam índice e vetores.
- Catálogo do acervo: um `SKILL.md` curto por skill e um arquivo por peça.

## Pertencimento

- Grupo novo "Interfaces do Gustavo" (Obsidian, janela de conflito e a futura tela de três vias, notificação, mod).
- `inbox/`, `_archive/` e a pasta não replicada entraram no grupo Conteúdo.
- Plugin desligado não é divergência; divergência sem colisão também pede ação.

## Responsabilidade e ações

- 4.6: operação, remover, conferência de versão como garantia de todo agente, divergência sem colisão.
- Cliente: por que sem cópia própria.
- Ações do Gustavo: nota nova em `inbox/`, "remova isto" = arquivar.

## Respostas do Gustavo (rodada 7), marca nova [R7]

| Pergunta | Onde entrou |
|---|---|
| Máquinas ligadas juntas | atores; 8.13; 8.14 |
| Porta principal; sessão fora do hub como cliente igual à raiz | 3.4; 8.0 regra 16; 8.3; 8.10; pergunta nova 18 |
| Nota nova nasce em `inbox/` | 3.2; 7.1 |
| Remover = `_archive/` 30 dias; agente só apaga com permissão ou depois dos 30 dias | 8.0 regra 13; 8.7; 4.3; 4.6; lacuna: quem confere os 30 dias |
| Obsidian e agente na mesma nota: "impossível"; aceita a colisão sem proteção | 8.0 regra 17; 8.1 |
| Cliente no GitHub privado: liberado | 8.15; 10. A parte dos modelos na nuvem ficou sem resposta: pergunta 17 |
| Binários: já tratado | 8.12, com a rodada sobre binários de "Revisão do sync…" conferida no ticket |
| Quem usa cliente | atores |
| Notificação do Windows basta | grupo "Interfaces do Gustavo" |
| Um agente por iniciativa; sem proteção por ora | atores; 8.0 regra 17 |
| Operação: agente com ele vendo | 8.0 regra 15; 4.2 a 4.5; 4.6; 8.11; 8.18 |
| Embeddings do Google: opção, sem depender dela | 3.3; 11 |
| Claude Desktop também altera notas e arquivos | atores; 8.17 |
| Celular e web: não por ora; web = novo cliente pela rede | 3.4; 8.10 |

Perguntas 15 e 16 seguem "a decidir com o Gustavo". Novas: 17 e 18 (seção v3 de `perguntas-ao-gustavo.md`).
