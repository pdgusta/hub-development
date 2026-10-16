# Workloads piloto

Type: grilling
Status: resolved
Blocked by: 01

## Question

Que workloads nascem no hub em vez de no vault, e como os dois convivem sem duas casas para o mesmo
fato? Contexto: Q10 em `../mapeamento.md` (o hub não substitui o vault agora; cada workload mora em uma
casa só).

## Comments

- 2026-10-01: rodada 1 em `respostas.md` (Q1 unidade que mora numa casa; Q2 quais pilotos; Q3 o que
  o vault sabe de uma iniciativa do hub; Q4 conhecimento do vault que os pilotos usam). Fatos: o vault
  não tem remoto git; `C:\Projetos\maestri\soc-context` (operação SOC STRATA) já mora fora do vault,
  sem git.
- 2026-10-01, respostas da rodada 1:
  - **Q1:** "pode ser isso". A unidade que mora numa casa é a iniciativa; "casa" entra no glossário.
  - **Q2:** "exatamente como sua recomendação, porém tirando a (b). Apenas (a) e (c)". Pilotos: esta
    frente e as iniciativas novas a partir de agora; a operação SOC STRATA não entra.
  - **Q3:** (ii). O vault não sabe que o hub existe; nenhuma linha nem ponteiro no `registry.md`.
  - **Q4:** "correto". O agente lê o vault pelo localizador, direto no disco; o que um piloto precisar
    na máquina pessoal é movido para o hub com ponteiro no vault; nunca cópia.
- 2026-10-01: rodada 2 em `respostas.md` (Q5 o que impede uma iniciativa nova de nascer no vault;
  Q6 ponteiro no vault ao mover conhecimento, diante da Q3; Q7 iniciativa nova filha de uma do vault).
- 2026-10-02, resposta parcial da rodada 2: **Q5:** "não vamos mexer no vault. Refaça a pergunta
  sabendo disso". A Q5b foi para `respostas.md` (o contrato do hub e o do vault numa sessão aberta no
  vault); Q6 a Q8 seguem abertas.
- 2026-10-02, respostas da rodada 2 (corrigem o rumo das rodadas 1 e 2):
  - **Q5b:** "eu não disse que o vault vai ser descontinuado pelo hub futuramente e que você deve usar
    o vault apenas como referência? Não precisa se preocupar com o vault, só com como o hub vai ser."
  - **Q6:** "não mexer no vault" é não mexer em como ele é. Nada é movido: o conteúdo que for pego do
    vault é **copiado** para o hub, e daí em diante se trabalha nele pelo hub, "e só para o conteúdo
    que já concordamos em 'pegar' do vault".
  - **Q7:** "Não pense em coexistência nem referência cruzada como o final definitivo, é só
    temporário." O vault será superado pelo hub, e o conteúdo relevante dele será movido ou copiado.
  - **Q8:** "Tudo que eu disser que nasce no hub, nasce no hub. E ponto."
  - Consequência: Q3 (ii) fica, por outro motivo (o vault é referência, não lado de integração); Q4
    passa a ser "ler no vault como referência, ou copiar para o hub o que o Gustavo escolher pegar";
    Q5 a Q8 deixam de ser perguntas.
- 2026-10-02: rodada 3 em `respostas.md`, com o entendimento para confirmar.
- 2026-10-02, respostas da rodada 3: **Q9:** "sim", os quatro pontos. **Q10:** "(a), porém os que
  citou do (b) seria ótimo ter no hub nas primeiras fases e com possibilidade de passarem por
  melhorias".

## Answer

Decidido com o Gustavo em 2026-10-02.

**O hub é desenhado como a casa de tudo.** O vault `ai-operating-system` é só referência e vai ser
superado; a convivência é temporária, do começo. O mapa não desenha nada para o vault: nem ponteiro,
nem registro, nem mudança no jeito dele.

1. **Unidade:** a iniciativa é o que mora numa casa só (ver "Iniciativa" e "Casa" no glossário).
2. **O que nasce no hub:** esta frente e tudo o que o Gustavo disser que nasce no hub, sem exceção
   por parentesco, ID ou cliente. A operação SOC STRATA (`soc-context`) fica fora por ora.
3. **Conteúdo do vault:** o que o Gustavo escolher pegar é **copiado** para o hub, e daí em diante
   trabalhado só no hub. O que fica no vault é referência e não conta como segunda casa. Fora isso, o
   agente pode ler o vault como referência, direto no disco (só existe no notebook; não tem remoto).
4. **Sem lista fechada:** a cópia acontece quando o Gustavo disser. Já desejados nas primeiras fases,
   e abertos a melhorias depois de copiados: `knowledge/armis-docs`, `knowledge/armis-brand` e a skill
   `armis-docx`.
5. **Mapa:** "Substituir o vault" sai de "Out of scope" como estava e passa a dizer que aposentar o
   vault fica para depois deste mapa.
