# Consertos da descrição, v3.1

2026-10-15, Tech lead. Fonte: `teste/v3/diagramas/*.md`. Sem nova volta de teste. A v3 está em `descricao-do-hub-v3.md`.

## Matriz de responsabilidade (seção 4)

- Linhas novas: núcleo e blocos da iniciativa, variante de setup, skills do hub, cliente (o computador), rede da
  empresa, vault, porta de escrita do cliente (ligável) e a seção **4.7 Portas de entrada** (uma linha por porta).
- Regras novas: a vigia fica sempre em "Lê" (resolve vigia em "Lê" numa tabela e em "Só vê" na outra); dono
  "Gustavo" por regra, marcado [L] quando é só a regra; hooks valem como no Claude Code, com remissão à tabela por
  ferramenta; restaurar é ação.
- Ambíguos resolvidos: Desktop (lê; gravar é requisito, caminho a decidir); porta de leitura não grava, e a gravação
  ligável é outra instância (componente novo em 3.1); restaurar o GitHub saiu de "Lê"; o agente edita o contrato só
  dentro do hub e com aval; nota de retomada com dono Gustavo e decisão do dia a dia do agente; porta do banco diz que
  gravar no disco também é permitido e que o caminho padrão está aberto; controle de acesso por pasta saiu da matriz
  (não é componente).

## Mapa de grupos (seção 5.1)

- Tabela "grupo de cada componente e de cada ator", com grupo principal e o segundo.
- Agendador do Windows em Periferia; outro par em Fora do par; clientes em Quem chega + Fora do par.
- Lista de pertencimento múltiplo completa (mod, notificação, Obsidian, kit de par, script do `_archive/`, pasta do
  papel, contrato), com o principal primeiro.
- "Fora do par" quer dizer fora da cópia, não fora do lugar (resolve o Tailscale da empresa e o vault no notebook).
- Seção nova "Ligações entre grupos" (em 6) e a ligação Gustavo → Obsidian.

## Sequência de editar uma nota (6 e 8.1)

- Banco de B → sincronizador de B (e plugin de B, se aberto): explícito; "o primeiro que vir leva, o outro encontra o
  disco igual".
- A busca de B reindexa **depois** de o disco mudar; o agente de B lê pela porta (padrão), ou o disco sem versão.
- Qual máquina é A não importa; o ~2 s é de um teste com um banco só; tempos pela rede e da reindexação seguem NV.

## Lacunas de dono (seção 13, nova)

13 lacunas de "quem", cada uma com onde aparece e a fonte que a deixa aberta, para levar ao Gustavo: vigia parada,
hook que falha, porta do banco fora, os 30 dias do `_archive/`, cabeça do contrato no MCP, restauração, registro do
aval do contrato, cópia diária falhando, modelo do verificador, peça citada sumida, escolha do par pelo cliente e busca
para cliente, dono do computador do cliente, bloqueio do Tailscale pela empresa.
