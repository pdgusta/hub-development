---
titulo: Núcleo do spec, bloco 1: os pontos abertos
ticket: 16
aberta: 2026-10-16
estado: absorvida
---

Quem escreveu o spec achou decisões que se contradiziam entre tickets e escolheu uma em cada caso, quase sempre a mais
recente. São sete desempates:

1. **Gravação com versão velha.** "Como os agentes gravam" diz que o banco recusa e o agente relê e refaz; "Como a
   verdade viaja" e o teste do CouchDB dizem que vira um conflito visível, guardado ao lado da outra versão. O spec ficou
   com o conflito visível, e a resposta ao agente diz "releia e refaça".
2. **Claude Desktop.** Um comentário antigo da passagem para a construção dizia que ele só lê; "Como os agentes gravam"
   decidiu que ele grava pelo MCP. O spec ficou com a gravação.
3. **Tamanho do texto que o MCP entrega ao Claude Code.** Uma pesquisa diz que ele corta em 2.048 caracteres, e outra
   observou cerca de 3.300. O spec ficou com o menor, 2.048, por segurança.
4. **Onde o verificador de frontmatter roda.** A arquitetura de pastas o põe no fim da resposta do agente, e o acesso
   dos agentes diz que o Claude Code tem esse fim pelo mod. O spec diz que ele roda onde cada harness tem o seu fim de
   resposta.
5. **O verificador grava sem conferir a versão.** O spec aceita isso porque ele só completa campos que se calculam
   sozinhos, trocando um trecho e nunca o arquivo inteiro.
6. **Marcador de raiz.** Dois tickets antigos põem no kit de par um arquivo que marca a raiz do hub para o Codex. A
   rodada mais recente do acesso dos agentes trocou isso pelo link simbólico no arquivo global. O spec ficou com o mais
   recente: o kit não cria marcador.
7. **GSD no arquivo global do Copilot.** Três tickets juntavam o contrato do hub com o GSD ali; o roteamento de skills
   tirou o GSD do escopo global. O spec ficou com o roteamento.

Dois pontos técnicos também ficaram sem resposta, mas não pedem decisão sua: onde o kit põe o MCP para o Copilot do
VS Code valer em qualquer pasta, e como isolar a pasta de configuração de ensaio sem que o Copilot deixe de ler as skills.
Eles vão para pesquisa em fonte primária antes do plano de construção. Três resumos do mapa ficaram velhos (o da
divergência, o das portas de entrada e o do Copilot) e vou anotar ao lado de cada um a decisão que o trocou.

## Os sete desempates
id: desempates
tipo: escolha
recomendada: A

- A: Aceitar os sete como o spec escolheu
- B: Aceitar todos menos os que eu citar pelo número no "Algo mais?"

## Aviso em dobro no Codex
id: aviso-codex
tipo: escolha
recomendada: A

- A: Um aviso por falha: a vigia avisa você quando a situação piora, e o fim de turno do Codex só repete se essa mesma falha ainda não tiver sido avisada
- B: Os dois convivem: além do aviso da vigia, o Codex lembra a cada fim de turno enquanto a falha durar
- C: Só a vigia avisa, e o Codex não ganha aviso no fim do turno

## Algo mais?
id: algo-mais
tipo: texto
