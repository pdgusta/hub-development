---
title: Pesquisa 05: ligar as máquinas com segurança (GitHub privado, Tailscale, servidor SSH)
data: 2026-10-01
origem: subagente de pesquisa (Claude Code), ticket "Ligar as máquinas com segurança"
método: páginas baixadas na íntegra (docs.github.com em Markdown pela API de artigos; tailscale.com/docs em Markdown pelo sufixo `.md`; learn.microsoft.com pelo MCP Microsoft Learn; man.openbsd.org em HTML convertido para texto) e trechos conferidos com grep. Nenhum resumo de WebFetch foi usado como fonte.
aviso: saída de modelo. As citações são literais e foram conferidas no texto da página na data acima. Interpretações e recomendações vêm marcadas como **inferência**. O que não foi conferido está marcado como **não verificado**.
---

# Ligar as máquinas com segurança: o que dizem as fontes oficiais

## Resumo (uma tela)

**1. Levar commits pelo GitHub privado.** O GitHub aceita HTTPS e SSH. Sobre HTTPS, diz que funciona "even if you are behind a firewall or proxy"; sobre SSH, avisa que "firewalls and proxies might refuse to allow SSH connections". Para HTTPS, recomenda Git Credential Manager (GCM) ou GitHub CLI em vez de criar token à mão. Se for preciso criar token, recomenda o **fine-grained PAT**, restrito a repositórios escolhidos, com "the minimal permissions necessary" e com data de validade. O PAT clássico "can access every repository that you can access". A **deploy key** vale para **um repositório só** e é só leitura por padrão, mas o GitHub lista contras: "usually not protected by a passphrase" e "don't have an expiry date". Para assinar commits, SSH é "the simplest to generate", e a mesma chave de autenticação pode ser cadastrada de novo como chave de assinatura. Na conta, o GitHub recomenda TOTP com chaves de segurança como reserva, "instead of SMS"; passkeys são "highly phishing-resistant". Nos termos de serviço, o conteúdo de repositório privado é "confidential", mas há exceções: segurança, varredura automatizada, suporte, integridade do serviço e obrigação legal.

**2. Tailscale.** Instale **só no Windows**, não no WSL. A documentação diz que, com as duas instâncias ativas, o tráfego "will not work" e recomenda "run Tailscale on the Windows host only". A política padrão de uma tailnet nova **libera tudo entre todos os dispositivos**. O menor privilégio exige escrever *grants*: o Tailscale recomenda grants em vez das ACLs legadas. O **servidor do Tailscale SSH só existe em Linux e macOS**, não em Windows. Para alcançar pastas que moram no Windows, sobra o **OpenSSH comum sobre a tailnet**. As chaves de nó expiram em **180 dias** por padrão, e desativar a expiração "reduces security". Em máquina corporativa há dois riscos documentados: (a) conflito com outras VPNs e com software de segurança, que o Tailscale lista nominalmente (CrowdStrike, GlobalProtect, FortiClient, Netskope, WSL, Docker Desktop…), e (b) uma política de MDM chamada `Tailnet` que, com o prefixo `required:`, impede registrar o dispositivo em outra tailnet. A máquina pessoal precisa do **modo unattended** para continuar na tailnet sem ninguém logado.

**3. Servidor SSH.** O **OpenSSH Server nativo do Windows** é instalado como recurso opcional, com conta de administrador. A instalação cria uma regra de firewall que libera a porta 22 de entrada. Ele aceita só `password` e `publickey`. Conta de administrador usa `administrators_authorized_keys` com ACL restrita. `PermitRootLogin` não se aplica: para barrar administradores, use `DenyGroups`. `ChrootDirectory` só vale para SFTP, junto com `ForceCommand internal-sftp`. O shell padrão é o `cmd.exe`. O **`sshd` dentro do WSL 2** enfrenta três obstáculos: a rede é NAT por padrão (fica inalcançável pela LAN sem `portproxy`), a VM desliga ociosa (`vmIdleTimeout` padrão de 60 s) e o Intune pode bloquear a mudança de rede e de firewall. Pelos man pages do OpenSSH, `PasswordAuthentication` vem **ligado por padrão**; `ForceCommand` "does not limit other kinds of access" (por isso entra `DisableForwarding`); e o `sftp-server -R` dá modo somente leitura.

**4. Combinações que as fontes sustentam (inferência a partir das citações):**
- **Commits:** HTTPS com GCM, ou chave SSH por máquina. No notebook corporativo, a credencial deve alcançar só o repositório do hub: fine-grained PAT com `contents:write` e validade, ou deploy key com escrita. Tudo sem passar pelo Tailscale.
- **Pasta não replicada:** a pasta mora na máquina pessoal e é servida pelo OpenSSH do Windows, alcançado pela tailnet. O acesso fica restrito por *grant* (notebook → pessoal, `tcp:22`) e por `Match` com `ForceCommand internal-sftp -R` mais `ChrootDirectory`, o que dá SFTP somente leitura.
- **Operação remota:** do notebook para a máquina pessoal, por SSH (chave, sem senha) ou RDP sobre a tailnet. O RDP exige Windows Pro, Enterprise ou Education na máquina remota. O sentido inverso põe um serviço de entrada no dispositivo corporativo e é o mais arriscado.

---

## 1. Repositório privado no GitHub levando commits de duas máquinas

### 1.1 HTTPS versus SSH

- Ambos funcionam para todos os repositórios. Sobre HTTPS: "You can work with all repositories on GitHub over HTTPS, even if you are behind a firewall or proxy." Sobre SSH: "You can work with all repositories on GitHub over SSH, although firewalls and proxies might refuse to allow SSH connections." (https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/about-authentication-to-github)
- Sem a GitHub CLI, HTTPS exige token ou credential helper: "If you authenticate without GitHub CLI, you must authenticate with a personal access token. … Alternatively, you can use a credential helper like Git Credential Manager." A senha não serve: "Password-based authentication for Git has been removed in favor of more secure authentication methods." (mesma página)
- Saída para SSH bloqueado: "Sometimes, firewalls refuse to allow SSH connections entirely. If using HTTPS cloning with credential caching is not an option, you can attempt to clone using an SSH connection made over the HTTPS port. Most firewall rules should allow this, but proxy servers may interfere." (https://docs.github.com/en/authentication/troubleshooting-ssh/using-ssh-over-the-https-port)

### 1.2 Git Credential Manager (HTTPS)

- Recomendação: "If you're cloning GitHub repositories using HTTPS, we recommend you use GitHub CLI or Git Credential Manager (GCM) to remember your credentials." Com o GCM, "you don't have to manually create and store a personal access token, as GCM manages authentication on your behalf". (https://docs.github.com/en/get-started/git-basics/caching-your-github-credentials-in-git)
- No Windows: "Install Git for Windows, which includes GCM." Depois, "your credentials are stored in the Windows credential manager". (mesma página)
- O GitHub repete a preferência na página de PATs: "To access GitHub from the command line, you can use GitHub CLI or Git Credential Manager instead of creating a personal access token." (https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens)
- **Não verificado:** o escopo do token OAuth que o GCM obtém (se alcança todos os repositórios da conta). A documentação do GitHub consultada não diz; a fonte seria o repositório do GCM, que não li.

### 1.3 Personal access tokens: fine-grained versus classic

- "GitHub recommends that you use fine-grained personal access tokens instead of personal access tokens (classic) whenever possible." (https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens)
- Vantagens: "Each token can be further limited to only access specific repositories for that user or organization." e "Each token is granted specific, fine-grained permissions". (mesma página)
- Escopo mínimo: "You should choose the minimal repository access that meets your needs." e "You should choose the minimal permissions necessary for your needs." (mesma página)
- A página traz um modelo pronto para push, com só `contents=write`: "Push access to repositories … `contents=write`". O modelo para leitura é `contents=read`. (mesma página)
- Validade: "GitHub automatically removes personal access tokens that haven't been used in a year. To provide additional security, we highly recommend adding an expiration to your personal access tokens." Na URL de criação, o padrão é "30 days" e o intervalo vai de 1 a 366 dias, ou `none`. (mesma página)
- Risco: "Treat your access tokens like passwords." e "Personal access tokens are like passwords, and they share the same inherent security risks." (mesma página)
- Classic: "Your personal access token (classic) can access every repository that you can access." (mesma página)

### 1.4 Chave SSH da conta

- Algoritmo e passphrase: o GitHub usa `ssh-keygen -t ed25519` no exemplo e pede "a secure passphrase". Para não digitá-la a cada uso, "you can add your key to the SSH agent". (https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent)
- Chave em hardware: "You can further secure your SSH key by using a hardware security key, which requires the physical hardware security key to be attached to your computer when the key pair is used to authenticate with SSH." (https://docs.github.com/en/authentication/connecting-to-github-with-ssh/about-ssh)
- Higiene: "you can regularly review your SSH keys list and revoke any keys that are invalid or have been compromised". E ainda: "If you haven't used your SSH key for a year, then GitHub will automatically delete your inactive SSH key". (mesma página)
- Armadilha no Windows: o OpenSSH do Windows e o `ssh.exe` do Git for Windows coexistem. "Git may still prompt you for your passphrase … when Git for Windows uses its bundled `ssh.exe` … and therefore can't talk to the Windows `ssh-agent` service." A correção documentada é `git config --global core.sshCommand "C:/Windows/System32/OpenSSH/ssh.exe"`. (página de geração de chave, acima)
- A Microsoft avisa que o `ssh-agent` do Windows persiste chaves: "Private keys stored by OpenSSH's ssh-agent service persist across sessions in the Windows registry, potentially causing security risks." (https://learn.microsoft.com/troubleshoot/windows-server/system-management-components/open-client-can-not-connect-server)
- Agent forwarding: "You should only add servers you trust and that you intend to use with agent forwarding." O GitHub também desaconselha `Host *`, porque os servidores "will be able to use them *as you*". (https://docs.github.com/en/authentication/connecting-to-github-with-ssh/using-ssh-agent-forwarding)
- **Inferência:** uma chave SSH cadastrada na conta autentica como o usuário e, portanto, alcança todos os repositórios da conta. Não achei trecho que diga isso literalmente. A conclusão vem do contraste com a deploy key, descrita como "an SSH key that grants access to a single repository".

### 1.5 Deploy key

- Escopo: "a deploy key, which is an SSH key that grants access to a single repository. GitHub attaches the public part of the key directly to your repository instead of a personal account". (https://docs.github.com/en/authentication/connecting-to-github-with-ssh/managing-deploy-keys)
- Escrita: "Deploy keys are read-only by default, but you can give them write access when adding them to a repository." Com escrita, "can perform the same actions as an organization member with admin access, or a collaborator on a personal repository". (mesma página)
- Contras documentados: "Deploy keys are usually not protected by a passphrase, making the key easily accessible if the server is compromised."; "Deploy keys are credentials that don't have an expiry date."; "If the user who created the deploy key is removed from the repository, the deploy key will still be active". (mesma página)
- Uma chave por repositório: "You can't reuse a deploy key for multiple repositories." Para vários repositórios, a página orienta um alias por repositório no `~/.ssh/config`. (mesma página)
- O próprio GitHub sugere outra rota: "For enhanced security and fine-grained control over repository access and permissions, we recommend using a GitHub App instead." (mesma página)

### 1.6 Assinatura de commits

- "For most individual users, GPG or SSH will be the best choice for signing commits. … SSH signatures are the simplest to generate. You can even upload your existing authentication key to GitHub to also use as a signing key." (https://docs.github.com/en/authentication/managing-commit-signature-verification/about-commit-signature-verification)
- O que se ganha com GPG: "A GPG key can expire or be revoked when no longer used." (mesma página)
- Persistência: um commit verificado "remains verified within its repository's network". (mesma página)
- Vigilant mode: "You should only enable vigilant mode if you sign all of your commits and tags … After enabling this mode, any unsigned commits or tags that you generate locally and push to GitHub will be marked 'Unverified.'" (https://docs.github.com/en/authentication/managing-commit-signature-verification/displaying-verification-statuses-for-all-of-your-commits)

### 1.7 Proteção da conta

- 2FA obrigatória para quem contribui código: "As of March 2023, GitHub required all users who contribute code on GitHub.com to enable one or more forms of two-factor authentication (2FA)." (https://docs.github.com/en/authentication/securing-your-account-with-two-factor-authentication-2fa/about-two-factor-authentication)
- Método: "We strongly recommend using a time-based one-time password (TOTP) application to configure 2FA, and security keys as backup methods instead of SMS." (https://docs.github.com/en/authentication/securing-your-account-with-two-factor-authentication-2fa/configuring-two-factor-authentication)
- Passkeys: "These properties make passkeys highly phishing-resistant". Uma passkey em chave FIDO2 é "device-bound" e portátil. (https://docs.github.com/en/authentication/authenticating-with-a-passkey/about-passkeys) Recomendação de reserva: "you should also configure a fallback 2FA method". (página "about 2FA", acima)

### 1.8 Privacidade e acesso a repositórios privados

- Quem acessa: "Private repositories are only accessible to you, people you explicitly share access with, and, for organization repositories, certain organization members." O GitHub acrescenta: "it's still essential to implement strong access controls, multi-factor authentication, and regular audits to mitigate risks." (https://docs.github.com/en/repositories/creating-and-managing-repositories/about-repositories)
- Termos de serviço, seção E: "GitHub considers the contents of private repositories to be confidential to you." O pessoal do GitHub "will not access private repository content without your consent except" nestes casos: "for security purposes; for automated scanning or manual review for known vulnerabilities, active malware, or other content known to violate our Terms of Service; to assist the repository owner with a support matter; to maintain the integrity of the Service; or to comply with our legal obligations". (https://docs.github.com/en/site-policy/github-terms/github-terms-of-service)
- IA: "If you provide your private repository content as Input to AI Features, we may use that Input to provide, develop, train, and improve the Service … Your ability to opt out under Section J.3 applies". Fora isso: "We will not otherwise use your private repository contents to develop or improve the Service." (mesma página)
- Divulgação legal: "we may be compelled by law to disclose the contents of your private repositories." (mesma página)

---

## 2. Tailscale entre o notebook corporativo e a máquina pessoal

### 2.1 Windows ou WSL

- Windows: o instalador `.exe` exige "Windows 10 or later". O login é "using your SSO identity provider". Em implantações gerenciadas, "You can use Windows registry values to apply system policies … Policies are typically distributed using MDM." (https://tailscale.com/docs/install/windows)
- WSL: "Installing Tailscale on WSL 2 is an advanced concept." E sobre rodar nos dois lugares: "If you run Tailscale on both the Windows host and inside WSL 2 at the same time, Tailscale encrypted traffic that flows from WSL 2 over Tailscale on the Windows host will not work … For this reason it is recommended that users run Tailscale on the Windows host only, and not inside WSL 2." (https://tailscale.com/docs/install/windows/wsl2)
- Máquina sempre ligada: "**Windows**: The Tailscale client runs within the user login session by default. When the user signs out or the device restarts, Tailscale disconnects until a user logs in again." A saída é o "unattended mode" ("Unattended mode is only available on Windows."). (https://tailscale.com/docs/how-to/run-unattended)

### 2.2 Controle de acesso: grants, ACLs e política padrão

- Política padrão: "Although access control policies in Tailscale follow a deny-by-default security model, the default access control policy is to allow all devices within a tailnet to connect to each other." (https://tailscale.com/docs/concepts/device-visibility)
- Grants versus ACLs: "Grants and legacy ACLs can coexist in the same tailnet policy file. The recommended best practice is to favor grants for most use cases." Cada grant tem `src`, `dst` e `ip` (por exemplo `"ip": ["tcp:443", "udp:53"]`). (https://tailscale.com/docs/features/access-control/grants)
- Exemplo de isolamento do próprio Tailscale: `"src": ["autogroup:member"], "dst": ["autogroup:self"]`, descrito como "an excellent starting point for implementing the principle of least privilege". Para restringir por função, há o exemplo com `tag:` e `tagOwners`. (https://tailscale.com/docs/reference/examples/grants)
- Boa prática: "Use access controls to define the connections you want to allow in your network, based on job function and following the principle of least privilege." e "Write tests to ensure access controls don't change unexpectedly". (https://tailscale.com/docs/reference/best-practices/security)
- **Inferência:** para este caso, um grant do notebook para a máquina pessoal limitado a `tcp:22` (e `tcp:3389`, se houver RDP), sem grant no sentido inverso. Não escrevi nem validei a sintaxe exata.

### 2.3 Tailscale SSH versus OpenSSH sobre a tailnet

- Servidor do Tailscale SSH: "Tailscale SSH's server component is only available on: Linux; macOS open source `tailscale` + `tailscaled` CLI devices". A seção de limitações repete: "You can currently use Tailscale SSH to connect to only Linux devices and macOS open source … devices. You can connect from any device running Tailscale, regardless of platform." (https://tailscale.com/docs/features/tailscale-ssh)
- Como funciona: "Tailscale claims port `22` for the Tailscale IP address … and routes SSH traffic for the device to an SSH server run by Tailscale … Your SSH configuration (`/etc/ssh/sshd_config`) and keys (`~/.ssh/authorized_keys`) files will not be modified". (mesma página)
- Check mode (reautenticação no provedor de identidade) e o aviso sobre `autogroup:nonroot`: "If you don't remove `autogroup:nonroot` from the `users` field, then anyone permitted by the `src` setting will be able to SSH in as any nonroot user on the `dst` device." (mesma página) O check mode "is only available for Tailscale SSH connections". (página de boas práticas)
- Limitação operacional: "Restarting the Tailscale daemon (`tailscaled`), for example, by performing an upgrade, will stop any existing Tailscale SSH session." (página do Tailscale SSH)
- OpenSSH comum sobre a tailnet: "only people who are part of your network and authorized by your network's access control policies can connect to the SSH server." Com isso, "the risk posed by automated scanning attacks … is eliminated", mas isso "is not a substitute for managing authentication keys and passwords". Ainda: "the SSH server can be configured to restrict which IP addresses a username can connect from. Since the Tailscale IP address of a user's device remains fixed unless it is deleted from the Tailscale network, this can be used as additional proof of the user's identity." (https://tailscale.com/docs/reference/ssh-over-tailscale)
- **Inferência:** como as duas máquinas são Windows, o Tailscale SSH só serviria se o Tailscale rodasse dentro do WSL. Isso esbarra na recomendação de "Windows host only" (2.1). Sobre a tailnet, o caminho que as fontes sustentam é o OpenSSH comum.

### 2.4 MagicDNS

- "MagicDNS automatically registers DNS names for devices in your network." e "Tailnets created on or after October 20, 2022 have MagicDNS enabled by default." O exemplo de uso é `ssh username@monitoring`. (https://tailscale.com/docs/features/magicdns)

### 2.5 Chaves de nó, expiração e proteção da tailnet

- Expiração: "By default, new domains are set with an expiry period of 180 days. If reauthentication does not occur, keys expire and connections to/from the given endpoint will stop working." Sobre renovar remotamente: "`tailscale up --force-reauth` might bring down the tailnet connection and thus should not be done remotely over SSH or RDP without an alternate means to log in". Dispositivos com tag nascem com a expiração desligada: "the tagged device will have key expiry disabled by default". (https://tailscale.com/docs/features/access-control/key-expiry)
- Desligar a expiração: "Disabling key expiry reduces security and can expose your network if the device or key is compromised. Only do this for trusted devices and revoke the key immediately if the device is lost or replaced." (https://tailscale.com/docs/solutions/access-remote-desktops-using-windows-rdp)
- Revogação: "When an Admin removes a device using the admin console, Tailscale immediately revokes its node key." (https://tailscale.com/docs/concepts/node-keys)
- Tailnet Lock: "With Tailnet Lock enabled, even if Tailscale were malicious or Tailscale infrastructure hacked, attackers can't send or receive traffic in your tailnet." Disponível "for the Personal and Enterprise plans". (https://tailscale.com/docs/features/tailnet-lock)
- Aprovação de dispositivo: "Require devices to be approved before they join your network". (página de boas práticas)
- MFA: "Enable multifactor authentication in your identity provider for authenticating to Tailscale, ideally using a hardware token". (página de boas práticas)
- Limite do que o Tailscale protege: "Tailscale does not protect your devices from any other traffic." (página de boas práticas)

### 2.6 Dados que passam pelo Tailscale

- Tráfego: "Is my traffic routed through your servers? No." Quando o tráfego passa por relay DERP, ele "is encrypted". (https://tailscale.com/docs/concepts/traffic-routing-through-tailscale) Mais: "Because Tailscale private keys never leave the local device that generated them, it's impossible for a DERP server to decrypt your traffic." (https://tailscale.com/docs/reference/derp-servers)
- Metadados: o serviço de coordenação "collects and manages device information, such as IP addresses, Tailscale client versions, public keys, location, and operating systems". (https://tailscale.com/docs/concepts/control-data-planes)
- Logs do cliente: dá para desligar com `--no-logs-no-support`, mas "If you block client logging, Tailscale may not be able to provide technical support." (https://tailscale.com/docs/features/logging)

### 2.7 Dispositivo gerenciado pela empresa (MDM, VPN corporativa)

- Software de terceiros: "If your device was supplied by your employer, it is very likely not just a stock macOS or Windows install. It is likely to be running other software." A lista de software que "may or may not cause problems" inclui, entre outros, "CrowdStrike Falcon", "Docker Desktop", "FortiClient", "GlobalProtect VPN", "Netskope", "Cisco Umbrella", "WSL". (https://tailscale.com/docs/reference/interoperability)
- Outras VPNs: "in most cases, you can't use Tailscale alongside other VPNs without a workaround. Usually, this is due to aggressive firewall rules, device limitations, or IP address conflicts." O conflito de faixa é concreto: "If the other VPN uses IP addresses from the Carrier-Grade NAT (CGNAT) range (`100.64.0.0` through `100.127.255.255`) … they will conflict". As soluções de contorno documentadas são "userspace networking" e "split tunnels". (https://tailscale.com/docs/reference/faq/other-vpns)
- Separação entre tailnets: "Devices in different tailnets cannot know about or connect to each other by default." Há uma ressalva: "When you create a Tailscale account using an identity provider with a domain that you own or through a GitHub organization, Tailscale recognizes users as belonging to the same organization. As a result, they will be added to the same tailnet." E ainda: "If you use Tailscale on your work device, your personal devices won't be visible to co-workers unless you've explicitly shared them." (https://tailscale.com/docs/concepts/device-visibility)
- Controle pelo empregador: a política `Tailnet` "lets the organization specify one or more tailnets to suggest or require during device registration … If the policy value is prefixed with `required:`, Tailscale requires one of those values and won't allow devices to be registered in any other tailnet." A política `AllowIncomingConnections` ("shields up") "blocks any incoming connections over Tailscale". Políticas de sistema estão disponíveis "for the Standard, Premium, and Enterprise plans". (https://tailscale.com/docs/features/tailscale-system-policies)
- Vários usuários na mesma máquina: "Use of Tailscale is not recommended on devices used by multiple people, unless shared tailnet access between them is acceptable to your security policies." (página de boas práticas)
- **Inferência:** entre na tailnet pessoal com uma identidade pessoal, não com a conta do domínio do empregador. Antes de instalar, confirme com o TI que o notebook não está sob política `Tailnet` `required:` e que a VPN corporativa não usa a faixa CGNAT.

### 2.8 Alternativas citadas pela própria documentação (sem comparativo)

- Servidor de coordenação próprio: "If you are using a self-managed deployment of Headscale as your control plane, use your Headscale instance's URL." (https://tailscale.com/docs/how-to/set-up-custom-control-server)
- WireGuard, ZeroTier, Mullvad e outros aparecem só na lista de interoperabilidade, como software que pode conflitar. Não aparecem como alternativa recomendada. (página de interoperabilidade)

---

## 3. Servidor SSH

### 3.1 OpenSSH Server nativo do Windows

**Instalação e serviço**
- Pré-requisito: "An account that is a member of the built-in Administrators group." A instalação é por "Optional Features" ou por `Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0`. A partida automática é "OPTIONAL but recommended". (https://learn.microsoft.com/en-us/windows-server/administration/openssh/openssh_install_firstuse)
- Firewall: "Installing OpenSSH Server creates and enables a firewall rule named `OpenSSH-Server-In-TCP`. This rule allows inbound SSH traffic on port 22." (mesma página) **Não verificado:** os perfis de rede (Domínio, Privado, Público) que essa regra cobre. A página não diz.
- Versão: "the in-box OpenSSH Feature on Demand … Microsoft supports and services this version through Windows Update, so it's the recommended option for most users." (mesma página)

**`sshd_config` no Windows**
- Local: "OpenSSH Server reads configuration data from `%programdata%\ssh\sshd_config` by default." Toda mudança "require[s] the service to be restarted". (https://learn.microsoft.com/en-us/windows-server/administration/openssh/openssh-server-configuration)
- Quem entra: "You can control which users and groups can connect to the server by using the `AllowGroups`, `AllowUsers`, `DenyGroups`, and `DenyUsers` directives." Os nomes de conta vão "in lower case". (mesma página)
- Métodos: "For Windows OpenSSH, the only available authentication methods are `password` and `publickey`." (mesma página)
- Administradores: "If the user belongs to the administrator group, `%programdata%/ssh/administrators_authorized_keys` is used instead." O arquivo "must only have permission entries for the `NT Authority\SYSTEM` account and `BUILTIN\Administrators` security group". (mesma página)
- Sem root: "PermitRootLogin: Not applicable in Windows. To prevent administrators from signing in, use Administrators with the `DenyGroups` directive." (mesma página)
- Chroot: "ChrootDirectory … is only supported with SFTP sessions. A remote session into `cmd.exe` doesn't honor `ChrootDirectory`. To set up a sftp-only chroot server, set `ForceCommand` to internal-sftp." (mesma página)
- `Match`: "Upon a match, the subsequent configuration arguments are applied. Match uses the pattern rules covered in the AllowGroups … section." (mesma página)
- Logs: com `SyslogFacility LOCAL0`, "Logs are generated under `%programdata%\ssh\logs`"; nos demais casos vão para ETW. (mesma página)
- Diretivas ausentes no Windows, entre outras: `PermitTunnel`, `X11Forwarding`, `StrictModes`, `AuthorizedKeysCommand`, `PermitUserEnvironment`, `KbdInteractiveAuthentication`. (mesma página)
- Shell padrão: "The initial default in Windows is the Windows command prompt (cmd.exe)." Ele muda no registro, em `HKEY_LOCAL_MACHINE\SOFTWARE\OpenSSH`, valor `DefaultShell`. (mesma página)

**Chaves no Windows**
- Contas: "Key-based authentication in OpenSSH for Windows works with local Windows accounts and Active Directory (domain) accounts. Microsoft Entra ID accounts don't support key-based authentication." (https://learn.microsoft.com/en-us/windows-server/administration/openssh/openssh_keymanagement) **Não verificado:** se uma conta Microsoft pessoal (MSA) funciona como conta local para chave. A página de configuração diz só que "internet-connected accounts are always resolved to their local account name".
- Sessão sem credencial de saída: "A remote session opened via key-based authentication doesn't have associated user credentials. As a result, the session isn't capable of outbound authentication as the user. This behavior is by design." (mesma página) **Não verificado:** o efeito sobre `git push` via GCM a partir de uma sessão SSH.
- Passphrase: "we don't recommend using an empty passphrase, because the passphrase works with the key file to provide two-factor authentication." (mesma página)

### 3.2 `sshd` dentro do WSL 2

- NAT é o padrão: "By default WSL uses a NAT based architecture". Pela LAN, "This isn't the default case in WSL 2. WSL 2 has a virtualized ethernet adapter with its own unique IP address." A saída documentada é `netsh interface portproxy` com `listenaddress=0.0.0.0`, e a Microsoft avisa que isso "means that incoming requests will be accepted from ANY IP address". (https://learn.microsoft.com/en-us/windows/wsl/networking)
- Mirrored: requer "Windows 11 22H2 and higher" e traz "Improved networking compatibility for VPNs" e "Connect to WSL directly from your local area network (LAN)". Exige uma regra no Hyper-V firewall para conexões de entrada (`Set-NetFirewallHyperVVMSetting … -DefaultInboundAction Allow` ou `New-NetFirewallHyperVRule …`). (mesma página)
- Firewall: com Windows 11 22H2 e WSL 2.0.9 ou mais novo, "the Hyper-V firewall feature will be turned on by default". (mesma página) Em ambiente corporativo: "If local rule merging is set to 'No' then WSL networking will not work by default, and your administrator will need to add a firewall rule to allow it." (https://learn.microsoft.com/windows/wsl/troubleshooting)
- Ociosidade: em `.wslconfig`, `vmIdleTimeout` vale `60000`: "The number of milliseconds that a VM is idle, before it is shut down". Em `[general]`, `instanceIdleTimeout` vale `15000` ("Set to -1 to disable auto shutdown"). (https://learn.microsoft.com/en-us/windows/wsl/wsl-config)
- systemd: é opcional, ligado por `[boot] systemd=true` em `/etc/wsl.conf` (o padrão é `false`). (mesma página)
- Controle corporativo pelo Intune: "Allow custom networking configuration … When set to disabled, this policy disables custom networking configuration via .wslconfig (wsl2.networkingmode)". Há também "Allow user setting firewall configuration" e "Allow the Windows Subsystem For Linux". (https://learn.microsoft.com/windows/wsl/intune)
- Permissões: "When a Linux binary inside of WSL accesses a Windows file, it does so with the user permissions of the Windows user that ran `wsl.exe`." (https://learn.microsoft.com/windows/wsl/enterprise)
- **Não verificado:** se o WSL sobe sozinho no boot do Windows sem login e sem tarefa agendada. Também não verificado: se, em modo mirrored, a interface do Tailscale do Windows aparece dentro do WSL e permite servir o `sshd` do WSL pela tailnet.

### 3.3 Hardening (man pages do OpenSSH)

As páginas abaixo são do OpenSSH atual em man.openbsd.org. A versão que acompanha o Windows pode ser mais antiga; veja a lista de diretivas ausentes em 3.1.

- `PasswordAuthentication`: "Specifies whether password authentication is allowed. The default is yes." (https://man.openbsd.org/sshd_config.5) **Inferência:** com chave, defina `no`. A página do Tailscale reforça: "The greatest risk comes from weak passwords, which is why the modern best practice is to disable passwords entirely." (https://tailscale.com/docs/reference/ssh-over-tailscale)
- `PermitRootLogin`: "The default is prohibit-password." (sshd_config.5) No Windows, o equivalente é `DenyGroups` para administradores (3.1).
- `AllowUsers`: "If the pattern takes the form USER@HOST then USER and HOST are separately checked … HOST criteria may additionally contain addresses to match in CIDR address/masklen format." (sshd_config.5) **Inferência:** dá para restringir o usuário à faixa da tailnet (`100.64.0.0/10`), em linha com a sugestão do Tailscale de "restrict which IP addresses a username can connect from".
- `Match` "Introduces a conditional block". Os critérios incluem "User, Group, Host, LocalAddress, LocalPort". (sshd_config.5)
- `ForceCommand`: "Forces the execution of the command specified by ForceCommand, ignoring any command supplied by the client … It is most useful inside a Match block." Mas "This directive does not limit other kinds of access that a client may request via their connection, such as TCP, agent, socket or X11 forwarding. If these are not desired, then they must be explicitly disabled … using the DisableForwarding option." (sshd_config.5)
- `DisableForwarding`: "Disables all forwarding features, including X11, ssh-agent(1), TCP and StreamLocal." (sshd_config.5) **Não verificado:** suporte no OpenSSH do Windows. Ela não aparece na lista de diretivas ausentes, mas a Microsoft também não a documenta.
- `ChrootDirectory`: "checks that all components of the pathname are root-owned directories which are not writable by group or others." (sshd_config.5) **Não verificado:** como essa checagem se traduz em ACLs NTFS no Windows.
- `Subsystem` / `internal-sftp`: "It accepts the same command line arguments as sftp-server". (sshd_config.5) E no `sftp-server`, `-R`: "Places this instance of sftp-server into a read-only mode. Attempts to open files for writing, as well as other operations that change the state of the filesystem, will be denied." (https://man.openbsd.org/sftp-server.8) **Inferência:** `Match User <conta>` + `ForceCommand internal-sftp -R` + `ChrootDirectory <pasta>` + `DisableForwarding yes` dá acesso somente leitura a uma pasta. **Não verificado:** o `-R` no build do Windows.
- `ListenAddress` "Specifies the local addresses sshd(8) should listen on." (sshd_config.5) **Não verificado:** o comportamento no Windows quando o IP do Tailscale ainda não existe na hora em que o serviço sobe.
- Opções em `authorized_keys`: `restrict` ("Enable all restrictions, i.e. disable port, agent and X11 forwarding, as well as disabling PTY allocation and execution of ~/.ssh/rc"); `command="command"` ("the command is executed whenever this key is used for authentication. The command supplied by the user (if any) is ignored", com a ressalva "the client may specify TCP and/or X11 forwarding unless they are explicitly prohibited, e.g. using the restrict key option"); `from="pattern-list"`. Para chaves FIDO, `verify-required` ("Require that signatures made using this key attest that they verified the user, e.g. via a PIN"). (https://man.openbsd.org/sshd.8)

---

## 4. Os três usos: combinações sustentadas e riscos documentados

As combinações são **inferência** montada sobre as citações acima. Os riscos citados são documentais.

### 4.1 Levar commits (as duas máquinas ↔ GitHub privado)

| Combinação | O que a sustenta | Riscos documentados |
|---|---|---|
| HTTPS + GCM nas duas máquinas | Recomendação explícita do GitHub (1.2); HTTPS passa por firewall e proxy (1.1) | Escopo do token do GCM **não verificado**; credencial guardada no Credential Manager do Windows |
| HTTPS + fine-grained PAT só do repositório do hub, `contents:write`, com validade | Repositórios específicos, permissões mínimas e validade (1.3) | "Treat your access tokens like passwords"; renovar ao expirar |
| SSH com chave da conta (ed25519 + passphrase, ou chave em hardware) | Fluxo padrão do GitHub (1.4) | SSH pode ser bloqueado no corporativo (porta 443 como saída); a chave alcança toda a conta (**inferência**); `ssh-agent` do Windows persiste no registro |
| SSH com deploy key de escrita, uma por máquina | Uma chave limitada a um repositório (1.5) | Sem validade, em geral sem passphrase, não ligada ao usuário; o próprio GitHub sugere GitHub App |
| Assinatura SSH (opcional) | "simplest to generate" (1.6) | Sem expiração nativa, ao contrário do GPG |

**Inferência:** no notebook corporativo, a credencial de menor alcance que as fontes sustentam é o fine-grained PAT de um repositório só, com validade, ou a deploy key de um repositório só. A chave SSH de conta e o PAT clássico alcançam todos os repositórios. Este uso não depende do Tailscale.

### 4.2 Alcançar uma pasta não replicada

| Combinação | O que a sustenta | Riscos documentados |
|---|---|---|
| Pasta na máquina pessoal; OpenSSH Server do Windows nela; Tailscale no host Windows das duas máquinas; grant notebook → pessoal `tcp:22`; `Match` + `ForceCommand internal-sftp -R` + `ChrootDirectory` + `DisableForwarding` | Chroot no Windows só via SFTP (3.1); `-R` somente leitura (3.3); OpenSSH sobre a tailnet tira o servidor da internet (2.3); grants por menor privilégio (2.2) | Regra de firewall da porta 22 criada pela instalação (perfis **não verificados**); `PasswordAuthentication` padrão `yes`; política padrão da tailnet libera tudo; `-R`, `DisableForwarding` e chroot no build Windows **não verificados** |
| Mesma pasta, servida pelo `sshd` do WSL | Possível com mirrored ou portproxy (3.2) | VM desliga ociosa; NAT impede acesso da LAN; Intune pode travar o modo de rede; Tailscale no host e no WSL juntos quebra o tráfego (2.1) |
| Pasta no notebook corporativo, servida a partir dele | Tecnicamente igual à primeira linha | Exige admin e porta de entrada no dispositivo do empregador; software corporativo pode conflitar (2.7); o MDM pode impor "shields up" (`AllowIncomingConnections`) |
| Tailscale SSH | Não se aplica a destino Windows (2.3) | Só funcionaria com Tailscale no WSL, o que contraria 2.1 |

### 4.3 Operar a outra máquina remotamente

| Combinação | O que a sustenta | Riscos documentados |
|---|---|---|
| Notebook → pessoal, SSH com chave (shell `cmd`/PowerShell) sobre a tailnet | OpenSSH do Windows (3.1) + tailnet (2.3) | Sessão por chave "isn't capable of outbound authentication as the user"; administrador usa `administrators_authorized_keys`; para evitar admin, `DenyGroups` |
| Notebook → pessoal, RDP sobre a tailnet | Guia oficial do Tailscale (`access-remote-desktops-using-windows-rdp`) | A máquina remota precisa ser "Windows Professional, Enterprise, Education edition, or Windows Server"; sem o modo unattended, o Tailscale cai no logoff ou no reboot (2.1) |
| Manter a máquina pessoal alcançável a longo prazo | Expiração desligada só no nó servidor | "Disabling key expiry reduces security"; `--force-reauth` remoto pode derrubar a conexão (2.5) |
| Pessoal → notebook (operar o corporativo) | Mesmos mecanismos | Põe serviço de entrada no dispositivo corporativo (2.7); política "Restrict multi-user systems" |
| Encaminhar o agente SSH para a outra máquina (para `git push` de lá) | Documentado pelo GitHub | "You should only add servers you trust" (1.4) |

---

## Lacunas e não verificado

1. Escopo do token OAuth do GCM com o GitHub. A fonte seria o repositório do GCM, que não li.
2. Os perfis de firewall (Domínio, Privado, Público) da regra `OpenSSH-Server-In-TCP` e como restringi-la à interface ou à faixa do Tailscale. A Microsoft não documenta isso nas páginas lidas.
3. Suporte, no OpenSSH do Windows, a `DisableForwarding`, a `internal-sftp -R` e ao chroot com ACLs NTFS. A Microsoft não lista essas diretivas como ausentes, mas também não as documenta.
4. Conta Microsoft pessoal (MSA) com autenticação por chave no OpenSSH do Windows. A Microsoft cita só contas locais, de AD e Entra (esta sem suporte).
5. Efeito da sessão SSH sem credencial de saída sobre `git push` via GCM ou sobre o Credential Manager.
6. Se o WSL inicia sozinho no boot sem login, e se o modo mirrored expõe a interface do Tailscale do host ao WSL.
7. Comportamento de `ListenAddress` com IP do Tailscale no boot do Windows.
8. Limites e preço do plano Personal do Tailscale (dispositivos, usuários). Não consultei a página de preços. Também não verifiquei quais provedores de identidade pessoais o Tailscale aceita.
9. Se o empregador já usa Tailscale (política `Tailnet` `required:`) e se a VPN corporativa usa a faixa CGNAT. Só o TI do empregador responde.
10. A afirmação de que a chave SSH da conta alcança todos os repositórios da conta é **inferência**, sem trecho literal conferido.
11. O nome exato do controle "Allow incoming connections" na interface do cliente Windows. Conferi só a política de sistema `AllowIncomingConnections`.
12. As citações do man.openbsd.org descrevem o OpenSSH atual do OpenBSD; o Windows traz um fork da Microsoft (PowerShell/openssh-portable) que pode estar em versão anterior.

## Consultas

**Buscas na web (WebSearch, filtradas para tailscale.com):**
- "Tailscale install Windows WSL 2 kb"
- "Tailscale other VPNs conflict corporate VPN Windows"
- "Tailscale personal tailnet on work device employer managed laptop"

**Buscas no Microsoft Learn (MCP):**
- "WSL enterprise Intune settings control networking mode firewall disable WSL policy"
- "OpenSSH Windows Microsoft account login authorized_keys local account sshd"
- "WSL start automatically at Windows boot without login service keep running" (sem resultado oficial útil; daí a lacuna 6)

**Índices consultados:** https://tailscale.com/llms.txt e https://tailscale.com/docs/llms.txt (lista de páginas; busquei termos como ssh, grant, acl, magicdns, key expiry, tailnet lock, mdm, vpn, windows, wsl, device approval, unattended).

**Páginas baixadas na íntegra e conferidas por trecho:**
- docs.github.com (via `https://docs.github.com/api/article/body?pathname=/en/...`): about-authentication-to-github; managing-your-personal-access-tokens; managing-deploy-keys; about-ssh; generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent; reviewing-your-ssh-keys; working-with-ssh-key-passphrases; using-ssh-agent-forwarding; using-ssh-over-the-https-port; about-commit-signature-verification; telling-git-about-your-signing-key; displaying-verification-statuses-for-all-of-your-commits; about-two-factor-authentication; configuring-two-factor-authentication; about-passkeys; caching-your-github-credentials-in-git; about-remote-repositories; access-permissions-on-github; about-repositories; token-expiration-and-revocation; about-githubs-ip-addresses; reviewing-your-security-log; sudo-mode; github-general-privacy-statement; github-terms-of-service.
- tailscale.com/docs (sufixo `.md`): install/windows; install/windows/wsl2; features/tailscale-ssh; reference/ssh-over-tailscale; features/magicdns; concepts/node-keys; features/access-control/key-expiry; features/tailnet-lock; features/tailscale-system-policies; mdm; reference/faq/other-vpns; reference/interoperability; concepts/device-visibility; reference/best-practices/security; features/access-control/device-management/device-approval; features/access-control/device-management/how-to/set-up; how-to/run-unattended; reference/grants-vs-acls; features/access-control/grants; features/access-control/acls; reference/examples/grants; features/tailnet-policy-file; reference/syntax/policy-file; concepts/traffic-routing-through-tailscale; concepts/control-data-planes; reference/derp-servers; features/logging; solutions/access-remote-desktops-using-windows-rdp; use-cases/personal-or-at-home-use; features/taildrop; reference/tailnet-passkey-admin; how-to/set-up-custom-control-server.
- learn.microsoft.com: windows-server/administration/openssh/openssh-server-configuration; openssh_install_firstuse; openssh_keymanagement; windows/wsl/networking; windows/wsl/wsl-config; trechos de windows/wsl/intune, windows/wsl/enterprise, windows/wsl/troubleshooting e troubleshoot/windows-server/.../open-client-can-not-connect-server (pelos resultados de busca do MCP, que trazem o texto da página).
- man.openbsd.org: sshd_config.5; sshd.8; sftp-server.8; ssh-keygen.1.
