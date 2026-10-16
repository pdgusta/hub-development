# Brief do Tech lead: descrição v3.1 (consertos dos diagramas, sem nova volta de teste)

Do maestro, 2026-10-15. O teste da v3 fechou o laço da descrição pelo critério do plano (3 voltas; erro e "não diz"
baixos): das 193 escondidas que as fontes respondem, 129 certas (67%; v2 65%, v1 65%), 56 parciais, 7 "não diz",
1 errada. Resumo em `teste/resumo-volta-3.md`. O próximo passo é a mistura com o UI engineer, que vai desenhar a partir
da descrição. Antes, um acabamento curto guiado pelos três diagramas da v3:

- `teste/v3/diagramas/matriz-responsabilidade.md`: Faltou 14, Inventei 4, Ambíguo 8;
- `teste/v3/diagramas/mapa-grupos.md`: Faltou 8, Inventei 13, Ambíguo 10;
- `teste/v3/diagramas/sequencia-editar-nota.md`: Faltou 5, Inventei 6, Ambíguo 2.

## O que fazer

Edite `descricao-do-hub.md` no lugar (guarde a v3 como `descricao-do-hub-v3.md`):

1. **Seção 4 completa:** todo componente citado em 3 ganha linha na matriz (dono, quem aciona, quem lê, quem só vê),
   inclusive o núcleo e os blocos da iniciativa, a variante de setup, as skills do hub, o cliente, a rede da empresa, o
   vault de referência e as portas de entrada. Onde a fonte não diz: "[A]" ou "[G, n]", como já faz.
2. **Cada "Inventei" e "Ambíguo"** dos três relatórios: a linha que falta ou se contradiz; resolva com a fonte ou marque
   o estado. Para o mapa de grupos, deixe explícito a que grupo pertence cada componente (uma tabela basta).
3. Os "Faltou" que são decisões abertas ("[A]": quem religa a vigia, quem confere os 30 dias do `_archive/`, quem
   atualiza a cabeça do contrato etc.) não se inventam: liste-os numa seção "Lacunas de dono" com a fonte, para eu levar
   ao Gustavo.

As regras dos briefs anteriores seguem valendo (fontes, estado de cada afirmação, o que não ler). Pode ler
`teste/resumo-volta-3.md` e `teste/v3/diagramas/*.md`; não leia `teste/v3/fatias/`, `respostas/` nem `julgamento/`.

Entrega: `descricao-do-hub.md` (v3.1) e `consertos-v3-1.md`, curto. Ao terminar: `maestri ask "Claude Code" "pronto: <caminho>"`.
