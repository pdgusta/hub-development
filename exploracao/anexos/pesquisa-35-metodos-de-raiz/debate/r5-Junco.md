# r5 — Junco: posição final

## Os nove

| # | Decisão | Método que sustenta |
|---|---|---|
| 1 Clientes | **manter** | Projects (`01-para.json`); dado de cliente não divide pasta com o que replica (`08-fhs.json`) |
| 2 Operações contínuas | **manter, separado de 1** | Areas "continues indefinitely" (`01`); destino compactar × arquivar é do hub, não do método |
| 3 Produtos e frentes | **juntar com 4** | nenhum JSON os separa (`01`); iniciativa mora numa casa só (GLOSSARY) |
| 4 Estudo e laboratório | **juntar com 3** (ver abaixo) | idem |
| 5 Referência | **manter, sem dado de cliente** | Resources (`01`), References (`07-vault-steph-ango.json`), estático (`08`) |
| 6 Oficina | **manter; perfil de máquina em subpasta não replicada** | config × data e state (`09-xdg.json`); caminho fixo e escopo (`15-diretorio-claude.json`) |
| 7 Entrada | **manter, local por máquina, com limite de idade** | variável (`08`), runtime com limpeza (`09`); GTD só sustenta a função (`05-gtd.json`: `nivel_raiz` vazio) |
| 8 Arquivo | **cortar como raiz**; `_arquivo/` dentro de cada raiz | só `01` tem Archives de topo e `01` não trata replicação; diferir em replicação separa (`08`) |
| 9 Pessoal | **condicional** | `/home` opcional (`08`); raiz pessoal (`07`) |

Nome sugerido para 3+4: iniciativas sem cliente.

## Onde a posição mudou, para ninguém ler a tabela como vento

- **3+4:** Cinzel (r4) mostrou que o destino de 4 contém o de 3 (arquivar) mais uma cópia sanitizada
  para 5, enquanto compactar (2) não é subconjunto de arquivar (1). E o risco é assimétrico: se
  spike vira produto, separados mudam a iniciativa de casa; juntos, nada se perde. **Astrolabio**,
  sua r4 diz que "Junco também" mantém 4 separado: isso era a r3; na r4 já tinha juntado. Placar
  2 a 1 pela junção; peço que reconsidere pelo risco.
- **8:** três de três em `_arquivo/`. Meu voto depende de um teste do ticket 12: mover pasta com
  duas máquinas editando não pode virar colisão. Se falhar, cedo para `estado`, como Cinzel (r4)
  condiciona à busca.
- **9:** adoto a regra de Astrolabio. Pessoal que não replica é raiz (FHS). Que replica e agente lê,
  não tem comportamento próprio: cai em 3+4 ou 5. "Agente não pode ler" é achado, não tipo: sem
  mecanismo nos JSON nem no GLOSSARY.

## Em desacordo, e por quê

Nenhum entre posições; 3+4 espera Astrolabio. O que continua é **fato que os JSON não têm**: pasta ×
campo depende de a busca filtrar por caminho e de o sincronizador aguentar mover pasta. É teste.

## O que os métodos NÃO responderam

1. **Pasta não replicada por máquina.** O FHS dá o critério, não o mecanismo (`08`).
2. **Envelhecer.** `nao_verificado` em 02, 04, 06, 08, 10, 11, 13, 14; só `01`, `09` (runtime) e
   `12` (só apagar) dizem algo.
3. **Sanitizar e promover.** `01` marca reaproveitamento como `nao_verificado`.
4. **Edição concorrente.** Nenhum dos quinze a trata.
5. **Nota de retomada.** Só `10` (`activeContext.md`) toca; nenhum diz "sobrescrito".
6. **Como a pasta do hub vira o caminho do harness.** `15` descreve os caminhos, não a ponte.
7. **Fatos do Gustavo:** SOC STRATA é cliente? Em qual máquina mora cada pasta de cliente? O pessoal
   replica? Spike vira produto (só confirma 3+4)?
8. **Captura de cliente na máquina errada.** Uso real, sem método: ticket 12.

Convergimos em oito dos nove; 9 depende de uma resposta, e 3+4 do aceite de Astrolabio.
