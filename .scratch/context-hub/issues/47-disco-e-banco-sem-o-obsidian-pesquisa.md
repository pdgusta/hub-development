# Disco e banco sem o Obsidian: pesquisa

Type: research
Status: resolved

## Question

O Gustavo quer que o que cai no disco do hub, `.md` ou não, chegue ao CouchDB mesmo com o Obsidian
fechado, e quer arquivos comuns além do `.md` no banco, até um limite de tamanho (respostas à R61, R68
e R69 de "Revisão do sync e da divergência com o banco", 2026-10-12). Pela fonte primária (documentação,
código e issues oficiais; protocolo da §10.4; nada instalado):

1. **Arquivos além do `.md` no plugin Self-hosted LiveSync:** leva qualquer arquivo comum do cofre ou só
   os que o Obsidian reconhece? Como guarda um binário (chunks, codificação), por que binário não tem
   junção automática, qual o `syncMaxSizeInMB` padrão, e o que acontece com arquivo grande.
2. **Limites do CouchDB e impacto de binários:** `max_document_size`, `max_attachment_size`,
   `max_http_request_size` e outros limites que valem para o formato do LiveSync; o que cada versão nova
   de um binário custa em espaço (chunks repetidos ou novos), na replicação entre pares, na compactação e
   com o E2EE. Pergunta direta do Gustavo: "por que binário é um problema, limite do CouchDB e impacto".
3. **CLI do LiveSync em modo `daemon` no Windows nativo:** como instalar (Node, build), rodar como serviço
   ou tarefa agendada, o observador de arquivos (chokidar) em NTFS, que arquivos leva, banco local
   próprio, comportamento em conflito.
4. **Plugin e CLI na mesma pasta:** o que a fonte diz de dois clientes LiveSync cuidando do mesmo cofre,
   sempre juntos ou em revezamento (o CLI só com o Obsidian fechado).
5. **Outras ferramentas** que ligam disco e CouchDB no formato do LiveSync sem o Obsidian (por exemplo, o
   `livesync-bridge` do mesmo autor, não verificado), com o mesmo recorte dos itens 3 e 4.

Resultado: relatório em `exploracao/anexos/pesquisa-47-disco-e-banco-sem-o-obsidian.md`, com o que não
foi conferido marcado "não verificado" e uma seção "Precisa de teste" que alimenta "Teste: disco e banco
sem o Obsidian".

## Answer

2026-10-12. Relatório: [pesquisa-47-disco-e-banco-sem-o-obsidian.md](../../../exploracao/anexos/pesquisa-47-disco-e-banco-sem-o-obsidian.md).

- **Plugin:** só leva o que o Obsidian enxerga; `.docx`, `.xlsx`, `.zip` e `.csv` exigem "Detect all file
  extensions" ligado no Obsidian (doc de problemas do LiveSync). Pastas com ponto ficam sempre fora.
- **Binário:** é guardado em pedaços Base64 (+33%). A extensão decide o que é texto. **Correção da R61:** colisão
  de binário não pergunta; o `mtime` mais novo vence sozinho e o outro ramo é apagado (código e doc).
- **Limite:** `syncMaxSizeInMB` padrão é 50 (MiB). Acima disso, o arquivo é pulado nos dois sentidos, só com
  aviso no log.
- **CouchDB:** `max_document_size` padrão de 8 MB, que o LiveSync e o spike sobem para 50 MB. O maior pedaço
  tem cerca de 5,6 MB, então o limite do banco não é o gargalo. O formato não usa anexos.
- **Impacto:** cada versão de um binário comprimido gera pedaços quase todos novos (inferência). Eles replicam
  para o outro par e não saem com a compactação; só o GC V3 (beta, manual) os remove.
- **CLI `daemon`:** leva todo arquivo, tem banco LevelDB próprio e conflito sem interface (fica aberto até um
  `resolve`). No Windows não há receita (só systemd ou Docker, CI só Ubuntu). Issue aberta #835 com E2EE.
  Suspeita: filtro de pasta com ponto aninhada no Windows.
- **Plugin e CLI juntos:** nenhuma fonte trata disso. O revezamento está mais perto do desenho; os dois sempre
  ligados é território não documentado.
- **livesync-bridge:** não trata conflito, fixa uma commonlib antiga e tem issues abertas de perda silenciosa.
  Fora como peça principal.
- **Precisa de teste:** 16 itens no relatório, que alimentam "Teste: disco e banco sem o Obsidian".

## Comments

- 2026-10-12: aberto a pedido do Gustavo (R69, A: "ok. E nesse teste quero ver isso tudo também com um
  teste do r68 além de pesquisa na documentação").
