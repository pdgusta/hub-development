# Como a verdade viaja entre as máquinas

Type: grilling
Status: resolved
Blocked by: 22, 23, 24, 26, 27, 28, 29, 30, 31

## Question

Com a verdade num banco e a vista Markdown de mão dupla ("Markdown: vista ou fonte da verdade"), o
que viaja entre as duas máquinas: o próprio banco (Dolt pelo remote git), uma serialização em texto
que o git junta, ou o `.md`, com o banco reconstruído em cada máquina? A resposta fixa a forma do
banco e põe em revisão, ou confirma, "Ponto de encontro do sync", "Sync que não depende de quem
gravou" e "Divergência e edição concorrente". Insumos: "Sync de banco entre duas máquinas pares" e
"Banco como verdade com vista Markdown editável".

## Comments

- 2026-10-04: rodada 1 em `respostas.md` (R6).
- 2026-10-04: R6 retirada. O Gustavo: "quem disse que é sem servidor?" Servidor é permitido; essa
  restrição nunca foi decisão dele. Pediu para mudar de estratégia: achar oportunidades para chegar ao
  objetivo, com alternativas, sem objeções. Caminhos levantados das pesquisas 23 e 24 (O1 CouchDB +
  LiveSync + MCP; O2 Dolt central; O3 banco central com plugin), com a R7 em `respostas.md`.
- 2026-10-04: R7, "1 pesquisa para cada caminho". Abertas as três pesquisas de montagem (O1, O2, O3), que travam este ticket.
- 2026-10-04: as três pesquisas de montagem terminaram. Rodada 2 em `respostas.md` (R8).
- 2026-10-04, R8: sim aos dois spikes (O3-C e O1) e, antes, um debate entre dois agentes no Maestri, um a favor do Dolt e outro contra, com veredito de Claude. Viraram os tickets 29, 30 e 31.
- 2026-10-06: os dois spikes terminaram ("Spike: Fast Note Sync" e "Spike: CouchDB e LiveSync", com a comparação na Answer do segundo). Este ticket está desbloqueado.
- 2026-10-06, dúvida do Gustavo (Maestri): um plugin próprio do Obsidian resolveria os problemas dos
  spikes? Resposta, como insumo: os dois problemas graves (gravação do agente sem conferir a base;
  agente que não vê conflito) estão no servidor ou no MCP, não no plugin, e um plugin próprio não os
  resolve. Os problemas do plugin são de interface (conflito fantasma e chinês no FNS; "Concat both" por
  caractere e falta de campo editável no LiveSync) e se resolvem com fork ou PR (licenças Apache-2.0 e
  MIT). Escrever um plugin de sync do zero é trabalho de semanas a meses (estimativa minha, não
  medida). "O melhor dos dois mundos" possível: LiveSync com a tela de três vias editável no estilo do
  FNS, como fork do modal (estimativa de 1 a 3 dias, não verificada). O REA (iniciativa
  `reverse-engineering` do vault) serve para software sem código-fonte; os dois projetos são abertos,
  então ele não acrescenta.
- 2026-10-06: ticket reivindicado (wayfinder). Rodada 3 em `respostas.md` (R9): qual caminho vira o
  hub, FNS, LiveSync, LiveSync com tela editável, ou sonda do Dolt antes.
- 2026-10-06, R9: "aceito sua recomendação"; no chat, "acho que é a mesma de A e B (opção C)".

## Answer

**O que viaja entre as máquinas é o banco, por um servidor central: CouchDB + Self-hosted LiveSync,
o caminho O1.** Decisão do Gustavo em 2026-10-06 (R9 em `respostas.md`).

- **Forma do banco:** a do LiveSync no CouchDB. Cada nota é um documento de metadados mais chunks com
  o texto; o histórico de revisões e as folhas em conflito moram no banco e replicam com ele
  ("Spike: CouchDB e LiveSync").
- **Dentro de cada máquina:** o plugin LiveSync mantém a vista `.md` viva nas duas direções; o agente
  grava pelo MCP do es617, num fork nosso.
- **Obrigatório antes de usar (critérios 4 e 5):** a R1 no fork (`read_note` devolve a revisão; a
  gravação leva `base_rev` e vira conflito se a base mudou) e o conflito visível ao agente. Total de
  3 a 3,5 dias de construção ("Spike: CouchDB e LiveSync").
- **Logo depois da construção, não como condição para começar:** a tela de colisão com três vias e
  resultado editável, no estilo do FNS, como fork do modal do LiveSync (1 a 3 dias, estimativa não
  verificada). Com ela o hub chega ao que o Gustavo chamou de "opção C". Entra em "Passagem para a
  construção" como melhoria.
- **Por que não o FNS:** custa cerca de 1 dia menos, mas a gravação do agente com base velha apaga a
  outra versão sem rastro, e a correção seria um fork do servidor Go. Na colisão o "Concat both" do
  LiveSync mutila o texto; até a tela editável chegar, o Gustavo escolhe uma versão e reedita.
- **Dolt:** continua como reserva nomeada ("Debate sobre o Dolt"); a "Sonda do Dolt" segue opcional.
- **Fica para outros tickets:** onde o servidor mora ("Onde o servidor mora"); o que sobra do GitHub,
  do sincronizador e do mecanismo de divergência ("Revisão do sync e da divergência com o banco"); se o
  agente ainda edita o `.md` direto no disco ("Como os agentes gravam no hub"); a busca, que pode
  indexar a vista `.md` em disco ("Camada de busca").
