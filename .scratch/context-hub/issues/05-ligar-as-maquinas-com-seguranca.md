# Ligar as máquinas com segurança

Type: research
Status: resolved

## Question

Quais são as práticas recomendadas, nas fontes oficiais, para ligar o notebook da ARMIS à máquina
pessoal com Tailscale, SSH (servidor no Windows e no WSL) e um repositório privado no GitHub? Cobrir
os três usos: levar os commits, alcançar a pasta não replicada e operar a outra máquina remotamente.
Contexto: Q11, Q14 e Q15 em `../mapeamento.md`. Seguir o protocolo da §10.4.

## Answer

Relatório completo: [`pesquisa-05-ligar-as-maquinas.md`](../../../exploracao/anexos/pesquisa-05-ligar-as-maquinas.md)
(2026-10-01, fontes primárias citadas). Fatos que os próximos tickets usam:

- **Commits:** o GitHub recomenda o Git Credential Manager para HTTPS. Credencial de menor alcance no
  notebook: fine-grained token só do repositório do hub (`contents:write`) ou deploy key só dele (a
  deploy key não expira). Se a rede bloquear SSH, há SSH pela porta 443. Assinatura de commit por SSH
  é a mais simples. Este uso independe do Tailscale.
- **Tailscale:** instalar só no Windows (Windows e WSL juntos "will not work"). O Tailscale SSH só
  existe como servidor em Linux e macOS, então no Windows vale o OpenSSH comum sobre a tailnet. A
  tailnet nova libera tudo; menor privilégio exige grants. Chaves de nó expiram em 180 dias; a máquina
  pessoal precisa do modo unattended.
- **Risco corporativo:** o Tailscale documenta conflitos com software de segurança e VPN corporativa,
  com WSL e Docker Desktop, e o empregador pode travar por MDM a tailnet permitida. Login com
  identidade corporativa pode cair na tailnet da empresa.
- **OpenSSH no Windows:** a instalação abre a porta 22 de entrada; chroot só para SFTP com
  `ForceCommand internal-sftp`; `PasswordAuthentication` vem ligado; `ForceCommand` não bloqueia
  encaminhamento (`DisableForwarding`); `sftp-server -R` dá somente leitura.
- **`sshd` no WSL:** NAT por padrão e VM que desliga ociosa (`vmIdleTimeout` 60 s).
- **Inferência do relatório (não decisão):** pasta não replicada na máquina pessoal, servida pelo
  OpenSSH do Windows pela tailnet, com grant notebook → pessoal `tcp:22` e SFTP somente leitura;
  operação remota no sentido notebook → pessoal.
- **Não verificado:** escopo do token do GCM; suporte do OpenSSH do Windows a `DisableForwarding`, `-R`
  e chroot; conta Microsoft pessoal com chave; WSL subir no boot; limites do plano Personal do Tailscale.
