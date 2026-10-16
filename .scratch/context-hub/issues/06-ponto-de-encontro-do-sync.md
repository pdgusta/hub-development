# Ponto de encontro do sync

Type: grilling
Status: resolved
Blocked by: 05

## Question

Por onde os commits passam entre as máquinas? Ponto de partida (rodada 4): coexistência, com o
GitHub privado levando os commits e o Tailscale atendendo a pasta não replicada e a operação remota.
Confirmar ou mudar à luz da pesquisa de segurança.

## Comments

- 2026-10-02: rodada 1 em `respostas.md` (Q1 só o GitHub como ponto de encontro; Q2 credencial de
  cada máquina; Q3 quando o Tailscale entra; Q4 assinatura de commits). Base: resposta de "Ligar as
  máquinas com segurança".
- 2026-10-02, respostas da rodada 1: (a) nas quatro (Q1 a Q4), como recomendado.

## Answer

Decidido com o Gustavo em 2026-10-02, com base em "Ligar as máquinas com segurança".

1. **O GitHub privado é o único ponto de encontro dos commits.** As duas máquinas fazem push e pull só
   nele, e nenhuma serve repositório para a outra. O sync não depende do Tailscale. "Ponto de
   encontro" entrou no glossário.
2. **Cada máquina tem a própria deploy key**, com escrita, só no repositório do hub. Ela não expira e
   pode ser revogada numa máquina sem afetar a outra. Se a rede bloquear a porta 22, vale o SSH do
   GitHub pela 443. **Não verificado:** se a rede do notebook libera a 22 ou a 443 para o GitHub;
   isso se confere na construção.
3. **O Tailscale (e o OpenSSH do Windows) fica fora da construção inicial.** Entra num ticket de
   construção à parte quando surgir a primeira pasta não replicada ou a primeira necessidade de
   operação remota. Nenhum dos cinco critérios depende dele.
4. **Commits sem assinatura.** Pode entrar depois sem refazer nada.
- 2026-10-04 (vinda de "Markdown: vista ou fonte da verdade"): em revisão: o GitHub foi escolhido para levar `.md` pelo git; com a verdade num banco, o ponto de encontro depende de "Sync de banco entre duas máquinas pares".
- 2026-10-13 (vinda de "Revisão do sync e da divergência com o banco", resolvida):
  revisão fechada. O GitHub deixa de ser ponto de encontro e vira
  cópia de segurança diária da vista, um `.git` na raiz de cada máquina, um ramo por máquina, só commit
  e push; as deploy keys por máquina e os commits sem assinatura ficam. As mudanças viajam entre os dois
  CouchDB pela tailnet, então o Tailscale entra na construção inicial (o item 3 acima cai nessa parte).
