# Ticket 16 — Trilho — parecer do Fiel — leitura intermediária

2026-10-17 ~06h55. Ramo ticket-16, HEAD aa70e98 (contém integracao 9453e3e; a integracao andou depois). Fiel sozinho
(leitura do Fielzinho pendente). Não conta como rodada: o próprio ticket junta só com o 08 e o 10 resolvidos.

## Veredito: a parte construída não tem conserto; o ticket ainda não passa inteiro

Falta para os critérios:
- Critério 1: cenários de binário descartado na passada, arquivo acima de 200 MiB, sincronizador parado, Config Doctor
  travado, e o gerador de exclusões a cada passada (código 2 vira item com o caminho; decisão do Gustavo de
  2026-10-16 20:38). Dependem do 08.
- Critério 5: o `estado_do_hub` real. O 10 passou (06h40); dá para juntá-lo e provar com o MCP lendo o `estado.json`
  que a vigia gravou.
- O item `fim-da-resposta` casado com o hook do 27 (lição do Rebite, 2026-10-16 21h51).

## Conferido
- `node --test agents/code/test/16-vigia.test.mjs`: 9/9 (Fiel). Árvore limpa.
- Docker do Trilho (`logs/trilho-16-docker-4.log`, aa70e98): 16 PASSA, "tudo passou". Inclui o conflito pelo caminho
  decifrado (sem o id cifrado), uma notificação só na passada que piora e o `recuperar` gravando ao lado os bytes da
  versão perdida, com o original mantido e a cópia do banco apagada. Não repeti o Docker: repito na rodada final,
  com o 08 juntado.
- Piora como o maestro decidiu (04:26): item que sobe de nível; item novo conta como ok; resolvido e voltou notifica.
- Troca atômica (`.novo` e rename); os itens dos outros donos ficam.
- b4e7272 (conserto do 12): a skill da busca não cita mais a `read`; diz para ler pela ferramenta do harness. Certo,
  casa com o 12 rodada 3.

## Ressalvas (para a rodada final)
1. **Atualização perdida:** `gravarPassada` e `gravarItem` fazem ler, mudar e gravar sem trava. Se o hook do 27 (ou
   o 31) grava o seu item entre a leitura e o rename da vigia, o item do hook some. O do `fim-da-resposta` é gravado
   uma vez só, na quarta parada; perdido, não volta. Sugestão: reler logo antes do rename e juntar, ou trava por
   arquivo.
2. Um CouchDB que responde 401 (senha errada) cai como "a tarefa de envio não está no _scheduler" e, depois de 15
   min, vira divergência de replicação com motivo errado. O `pedir` devolve undefined para qualquer resposta que não
   seja ok.
3. O `recuperar` replica o banco inteiro para `<db>-recupera` a cada folha descartada. Com várias folhas, várias
   cópias inteiras. Pesa com o hub grande.

## Rodada final (rodada 1) — 2026-10-17 ~10h50 (HEAD 280b778, com integracao e98a891)

Veredito: **VOLTA**, por 1 conserto. Fiel sozinho (Fielzinho sem cota até 12h15; leitura pendente). As três ressalvas
da leitura intermediária foram feitas (trava no `estado.json`, 401 vira `informa`, `recuperar` com uma cópia só).

Conferido pelo Fiel:
- `node --test agents/code/test/16-vigia.test.mjs`: 19/19 (Fiel). Árvore limpa.
- Docker: não repeti (fila cheia, memória no limite). Li `logs/trilho-16-docker-8.log`, rodado pelo Trilho na mesma
  ponta 280b778: "tudo passou" (20 casos), com binário descartado pelo caminho em claro, `recuperar` com os bytes da
  versão perdida, o original mantido e a cópia do banco apagada, sincronizador parado, laço, lista de exclusões que
  muda e religa, `estado_do_hub` real sem `vistos`, contêineres apagados.
- Cenários do 08: `acima-do-limite` pelo `Get-AcimaDoLimite` consertado no 08 (forma longa, sem pastas locais);
  Config Doctor pela versão da regra (decisão do maestro; não verificado com o Obsidian aberto, declarado).

### Consertos

1. **(Fiel) Conflito de TEXTO resolvido vira "binário descartado".** `descartados()` (`vigia.mjs` ~136-151) conta toda
   folha apagada com `path` ao lado da viva. No fonte do LiveSync, o perdedor de texto é apagado pelo mesmo caminho do
   binário: `resolveByDeletingRevision` → `deleteRevisionFromDB` → `deleteRevisionFromDBCore` → `db.delete(info, rev)`
   (`livesync-commonlib`, `ServiceFileHandlerBase.js:636`), que é o `_deleted` sobre o documento inteiro do achado do
   08. Isso acontece com texto quando os dois lados são iguais (`isSame`, `operations.ts:146-163`) e quando o Gustavo
   escolhe uma versão na janela de conflito. A vigia então acusa "binário descartado em inbox/nota.md" como
   `divergencia`, com notificação, até um `olhei`. O spec (faixa 7) pede o ramo apagado **de binário**.
   - Conserto: só caminho que o LiveSync não trata como texto (`isPlainText`: `.md`, `.txt`, `.svg`, `.html`, `.csv`,
     `.css`, `.js`, `.xml`; `livesync-commonlib/dist/string_and_binary/path.js:135`). Caso no teste sem Docker: folha
     apagada com `path` de uma `.md` ao lado da viva não vira item.
   - Não reproduzido no Docker (a resolução de texto não está no ensaio); achado pela fonte.

### Ressalvas (não seguram)

1. `laco` e `exclusoes` são `informa` novos a cada ação: pela regra de piora (item novo conta como `ok` antes), cada
   religação do CLI pelo laço (ex.: o EBUSY do 08) e cada pasta local nova notificam. Pode virar ruído; rever com o
   uso.
2. A 5ª rodada Docker teve o registro sobrescrito (declarado).

## Rodada 2 — 2026-10-17 ~11h20 (0332466): **PASSA**

Conserto 1 feito: `descartados()` pula caminho que o LiveSync trata como texto (`.md .txt .svg .html .csv .css .js .xml
.canvas`, conferido no `path.js:135-145` da commonlib; o `.canvas` faltava na minha lista). Caso novo sem Docker (.md e
.canvas com folha apagada não viram item). `16-vigia.test.mjs`: 19/19 (Fiel). Árvore limpa. Fiel sozinho (Fielzinho
lê depois). A mudança é só de filtro na passada; o Docker da 8ª rodada segue valendo para o resto. Ressalva do
laco/exclusoes registrada, sem conserto.

## Rodada curta (junção vermelha no 12-busca) — 2026-10-17 ~11h40 (Fiel sozinho; leitura do Fielzinho pendente)

Ramo `ticket-16`, HEAD 6a0ab17. **Veredito: PASSA.**

- O conserto é só a description do `agents/skills/vigia/SKILL.md` (`: ` sem aspas trocado por `, que lê`).
- Fiel: as skills lidas pelo `separar` do hub (`lib/frontmatter.mjs`): a versão antiga (0332466) dá "bad indentation of
  a mapping entry (2:41)"; em 6a0ab17, as 9 skills leem com description. O mesmo no `ticket-21` (10 skills, com o
  arquivar). Não rodei o 12-busca (indexação pesada); vale o log do Trilho `logs/trilho-16-12-busca.log` (9/9).
