# Onde o servidor mora

Type: grilling
Status: resolved
Blocked by: 25

## Question

Onde mora o CouchDB (com o MCP do es617 ao lado) que as duas máquinas alcançam? As opções de
"Montar: CouchDB, LiveSync e MCP" (seção 4 de `exploracao/anexos/pesquisa-26-montagem.md`): S1
container numa das máquinas, alcançado pela outra via Tailscale; S2 CouchDB nativo numa das máquinas;
S3 um CouchDB em cada máquina com replicação mestre-mestre; S4 VPS ou Fly.io, com E2EE. Pesam: a
máquina que hospeda precisa estar ligada (ou o PouchDB local segura o trabalho offline, não
verificado); o risco do Tailscale com o software corporativo do notebook ("Ligar as máquinas com
segurança"); o dado de cliente fora das máquinas na S4; e o Tailscale, que "Ponto de encontro do sync"
deixou fora da construção inicial.

## Comments

- 2026-10-06: graduado de "Como a verdade viaja entre as máquinas" (O1 escolhido).
- 2026-10-06: rodada 1 aberta em `respostas.md` (R10: S1 a S5). Recomendação: S4 com E2EE e o MCP do
  es617 em cada máquina, para as máquinas seguirem pares e o Tailscale ficar fora.
- 2026-10-10: R10 respondida: S4 fora (o Gustavo quer algo pronto logo); S5 já estava fora. Rodada 2
  aberta em `respostas.md` (R11: comparação S1 × S2 × S3). Recomendação: S1 com a máquina pessoal
  hospedando; a S3 fica como evolução se o "ligada sempre" pesar.
- 2026-10-10: R11: o Gustavo pende para a S3 (flexibilidade: qualquer computador ou sandbox monta o
  hub; não quer depender da pessoal como host). Rodada 3 em `respostas.md`: como um par novo entra,
  par × cliente, segurança de qualquer lugar. R12: fechar a S3 com pares + clientes pela tailnet e o
  kit de par.
- 2026-10-10: R12 aceita, com o cliente só de leitura (ver Answer).

## Answer

**S3: um CouchDB em cada par, com replicação mestre-mestre pela tailnet. Clientes alcançam um par
pela tailnet, sem cópia própria.** Decisão do Gustavo em 2026-10-10 (R10 a R12 em `respostas.md`).

- **Por que a S3:** o Gustavo não quer depender de uma máquina fixa como host e quer que qualquer
  computador ou sandbox monte o hub. A S4 (nuvem) saiu porque ele quer algo pronto logo; a S5 já
  estava fora; a S1 era a mais viável, mas prende o hub a uma máquina.
- **Par:** computador com cópia completa (CouchDB + MCP do es617 + Obsidian com LiveSync). Replica
  com um par existente por duas tarefas do CouchDB, uma em cada sentido
  ([replication/intro.rst](https://raw.githubusercontent.com/apache/couchdb/main/src/docs/src/replication/intro.rst)).
  Inferência: as duas tarefas podem rodar no notebook, que só sai e não abre porta de entrada. O
  LiveSync entra por um Setup URI copiado de um par que funciona e depois aponta para o CouchDB local.
- **Cliente:** sandbox ou máquina de passagem. Entra na tailnet com chave efêmera e tag, e o agente
  usa o MCP de um par por HTTP com token. Não leva CouchDB nem cópia, mas precisa de um par ligado.
- **Cliente só de leitura:** cada par roda um segundo MCP com `READ_ONLY=true` e token, exposto na
  tailnet; um grant limita a tag dos clientes à porta desse MCP. O cliente nunca recebe a credencial
  do CouchDB, porque o `READ_ONLY` não é garantia no banco (README do es617). Duas instâncias do es617
  por par: inferência, não verificado.
- **Segurança:** tudo só pela tailnet, nunca o Funnel; senha do CouchDB; E2EE do LiveSync; token no
  MCP; Setup URI e frase-senha por canais separados; chaves efêmeras com validade para clientes. Cada
  par guarda a cópia completa e a frase-senha da E2EE, e a regra do dado de cliente (Q3) vale para cada
  um.
- **Para começar logo:** o primeiro par nasce nesta máquina com o compose do spike. Até o segundo par
  existir, é a S1 sem nada a refazer.
- **Primeiro teste da construção:** o LiveSync com dois CouchDB replicando entre si (NV). Se falhar,
  a volta é a S1.
- **Antes de instalar o Tailscale no notebook:** consulta ao TI (política `Tailnet` com `required:` e
  a faixa da VPN, pesquisa 05 §2.7).
- **Fica para outros tickets:**
  - o que conta como "máquina sem sync" e onde o aviso nasce sem ponto de encontro ("Revisão do sync
    e da divergência com o banco");
  - o MCP que cada harness carrega, local ou de cliente ("Acesso dos agentes: decisão");
  - a pasta não replicada, que pode ser replicação filtrada ou ficar fora do banco ("Arquitetura de
    pastas e frontmatter do hub");
  - o kit de par e o kit de cliente ("Passagem para a construção").
- 2026-10-10 (vinda de "Portas de entrada do hub", R21): o Gustavo dispensou a consulta ao TI antes
  de instalar o Tailscale no notebook.
- 2026-10-12 (vinda de "Revisão do sync e da divergência com o banco", R62): cada par dispara a
  replicação das próprias mudanças para o outro, em vez das duas tarefas no notebook; o notebook passa
  a receber conexão, só pela tailnet. Motivo: o aviso de sync parado nasce na máquina que travou.
