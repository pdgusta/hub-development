# Rodada 2: Prisma

Li `r1-quadrante.md`, `r1-sextante.md`, `r2-quadrante.md` e os fatos novos no fim de `protocolo.md`.
Os ajustes do Quadrante às minhas mudanças (Prisma-14, 18, 22, 24) eu aceito todos.

## Votos: Quadrante

- **Q-1** (guarda sem propostas e uso): concordo, com o ajuste dele na Prisma-18 (`agents/maestro/` inteira fora da
  guarda; o ticket 12 só põe `propostas/` e `uso/` lá).
- **Q-2** (GSD sai, com cópia): concordo. 15 (rodada 2) é mais novo que 36 e 42.
- **Q-3** (apagar "Contradições achadas" da faixa 8): concordo.
- **Q-4** (sem vigia e sem MCP: "estado indisponível"): concordo.
- **Q-5** (no Codex, vigia e `notify` ficam os dois): concordo. 33 (vigia notifica quando piora) e 14, rodada 8 (`notify`
  com a notificação do Windows) são decisões separadas; nenhuma suprime a outra.
- **Q-6** (regra curta): concordo. É a Prisma-8.
- **Q-7** (teste dos três harnesses no núcleo do Worker 5): concordo, com [formato] no login de ensaio.
- **Q-8** (hooks do acervo agem fora do hub): concordo com a marca [núcleo]. Leio o mesmo: o 14 fala dos hooks do hub;
  o 40 e o 43 dão ao hook do acervo o gatilho `MAESTRI_TERMINAL_ID`.
- **Q-9** (ponte do Desktop): concordo. É a Prisma-17.
- **Q-10** (junction só com as de uso geral): concordo. É a Prisma-16.
- **Q-11** (marcador de raiz, fonte do teste): concordo.
- **Q-12** (`COPILOT_HOME` não prova as skills; `COPILOT_SKILLS_DIRS` no ensaio): concordo com a marca [núcleo].
- **Q-13** (lacunas de dono 4 e 5 [núcleo]; 7, modelo do verificador e peça sumida abertas): concordo, com o ajuste do
  fato 2 abaixo para a lacuna 4.
- **Q-14** (as perguntas do plano ao Gustavo numa nota só): concordo, com o ajuste do fato 4 (o Docker sai da lista).
- **Q-15** (nota do que muda com etapas sequenciais, sem ordem): concordo com a versão sem a ordem.
- **Q-16** (stories do 56 marcadas): concordo, com o ajuste do fato 2 abaixo.
- **Q-17** (portas do núcleo nas partes, [formato]): concordo.

## Votos: Sextante

- **Sextante-1** (função do nível do cliente decidida; lista aberta): concordo.
- **Sextante-2** (núcleo só em iniciativas): concordo.
- **Sextante-3** (`initiative` fora de iniciativa): concordo, [núcleo] no esclarecimento.
- **Sextante-4** (verificador preserva gravação concorrente): concordo com ajuste. A troca de trecho do 11 é segura
  porque a ferramenta nativa recusa quando o trecho mudou. O verificador é script, não ferramenta nativa: precisa fazer o
  mesmo. Texto proposto: "o verificador relê o arquivo logo antes de gravar e só troca o trecho se o arquivo ainda é o que
  ele leu; se mudou, refaz ou devolve ao agente". Fonte: 11, Answer ("Nenhuma gravação sem guarda de versão"); 08 e 33
  (o sincronizador também grava no disco, por isso a trava por arquivo não serve). Fica não verificado se essa
  conferência cobre a janela entre a releitura e a gravação.
- **Sextante-5** (segredo aninhado abrangido pela exclusão): concordo. O 48 (item 8) achou o vazamento de pasta com ponto
  aninhada na varredura de partida; o teste tem de cobrir esse caso também.
- **Sextante-6** (nota sem mudança não é nota insuficiente): concordo.
- **Sextante-7** (sem IA no checkpoint é [núcleo]): concordo, com a resposta do Quadrante sobre o 14.
- **Sextante-8** (estado indisponível): concordo. É a Q-4.
- **Sextante-9** (import no Claude Code, link nos outros): concordo.
- **Sextante-10** (`local: true` fora da busca do próprio par): concordo.
- **Sextante-11** (todo caminho com ponto fora da busca): concordo.
- **Sextante-12** (dono do gerador de exclusões [formato]): concordo com o ajuste do Quadrante (faixa 1 como texto,
  marcada [formato]).
- **Sextante-13** (limites da busca [núcleo]): concordo.
- **Sextante-14** (relatório de YAML inválido [núcleo]): concordo.
- **Sextante-15** (0.16.2 só indexa `.md`): concordo; o 12 é mais novo e leu a fonte do pacote.
- **Sextante-16** (contagem de instâncias [núcleo]): concordo. É o ajuste da Prisma-22.
- **Sextante-17** (requisitos fora do corte de tempo): concordo.

## Votos: os quatro efeitos dos fatos novos

1. **TI e Tailscale:** concordo. Ajuste: o mesmo vale para o ponto "risco corporativo" que vem do 05 (MDM, VPN
   corporativa); fica só o conflito com Docker Desktop e WSL como não verificado. O "sem consulta ao TI" já estava no 16
   (2026-10-14); agora é fato, não só dispensa.
2. **56 depois da construção:** concordo com ajuste.
   - Saem desta construção, marcadas [ticket aberto: 56]: o prazo de 30 dias, o `limpar-arquivo` (sem o prazo não há o
     que limpar: proponho tirá-lo da construção em vez de deixá-lo [núcleo]), "remover = arquivar" e "dois dias de
     distância bastam".
   - Ficam, porque vêm de ticket resolvido: o `arquivar` que confere o outro par (36, R25; 12) e a cópia diária (33).
   - "Nenhuma iniciativa de cliente vetada no GitHub" já decorre do 33 ("cópia de segurança diária da vista", sem
     exceção) e do 12 ("tudo replica nas duas máquinas, inclusive o conteúdo de cliente"; o que vai ao git é o que não
     tem ponto). Proponho citar 33 e 12 nessa user story e tirar a marca do 56 dela.
   - A recuperação ("um agente com o Gustavo vendo, ou ele pelo GitHub") vem do 56; fica [ticket aberto: 56], mas o
     comando de recuperar binário (33, R71) não depende dela.
3. **Sem política do Copilot:** concordo; nada a mudar.
4. **Docker e repositório:** concordo. Acréscimos:
   - na faixa 4, o ponto "CouchDB descartável no Docker local conta como 'serviço'?" passa a "o Gustavo liga o Docker
     Desktop (16, 2026-10-16); os CouchDB de ensaio em contêiner, em 127.0.0.1, dependem só disso" — dúvida: o fato diz
     que ele liga o Docker, não que libera contêineres de ensaio; peço ao maestro confirmar se a pergunta está respondida;
   - na faixa 10, o repositório privado novo leva uma deploy key por máquina, com escrita, só nele (06, item 2, que o 33
     manteve); a rede do notebook para a porta 22 ou 443 segue não verificada (06).

## Mudança nova

### Prisma-26: Citar o 33 e o 12 para "nenhuma iniciativa vetada"
- Onde: `faixas-09-10.md`, faixa 10, user story 13 e "Cópia de segurança diária" ("Nenhuma iniciativa de cliente é
  vetada no repositório (56, rodada 7)").
- Texto proposto: "Nenhuma iniciativa de cliente fica fora da cópia: a cópia é da vista inteira, fora só o que não
  replica (o que tem ponto e a pasta com `local: true`) (33, 12)."
- Fonte: 33, Answer ("GitHub: cópia de segurança diária da vista"); 12, Answer ("tudo replica nas duas máquinas,
  inclusive o conteúdo de cliente"). A resposta da rodada 7 do 56 confirma, mas não é a fonte necessária.
