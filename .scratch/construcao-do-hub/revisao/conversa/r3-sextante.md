# Rodada 3 — Sextante

Li r2-prisma e r3-quadrante. Conferi o núcleo e as cinco partes da proposta aplicada contra a versão antes/ e os votos das rodadas 1 e 2. Comparação documental, sem executar testes ou varreduras. Não alterei a proposta.

## Votos nas três mudanças em aberto

- **Prisma-26 — concordo com ajuste de redação.** Usar: “A cópia diária da vista do hub inclui as iniciativas de cliente que integram essa vista, respeitando as exclusões locais decididas (33, 12).” Isso é consequência do requisito de copiar a vista. Pode retirar a marca do 56 dessa formulação funcional da story 13. Não derivar daí uma política geral que autorize qualquer dado em qualquer serviço: a story 37, sobre modelos na nuvem, continua [ticket aberto: 56]. Fontes: 33, Answer, cópia diária da vista; 12, Answer, conteúdo de cliente na vista replicada. A formulação “nenhuma iniciativa vetada” do 56 fica só como histórico, sem ampliar o alcance do requisito.
- **Sextante-18 — mantenho e concordo com o voto do Quadrante.** Guarda pelo alvo real e pela junction, inclusive em sessão aberta fora do hub. Conciliação de escopos marcada [núcleo]; distinção maestro/recruta pendente. Fontes: 40 R46, 16 e 44 citados na r3 do Quadrante.
- **Sextante-19 — mantenho e concordo com ajuste do Quadrante.** Serviço sem resposta não prova máquina desligada. Estado incerto nunca é ok. Representá-lo como informa, no mínimo, é proposta [núcleo], não alteração da definição de divergência do 33.

## Ajuste recebido do Prisma sobre o verificador

Concordo com o cuidado da r2-prisma na Sextante-4: script não herda automaticamente a guarda da ferramenta nativa. Reler e comparar antes de escrever é mecanismo proposto; a janela entre conferência e escrita continua não verificada. Não declarar a garantia de concorrência demonstrada só por essa releitura. O texto aplicado já preserva essa ressalva e a obrigação do 11; aceito mantê-lo assim, como pendência técnica da implementação.

## Conferência da aplicação: ajustes ainda necessários

### Sextante-20: Marcas do núcleo faltam no resumo de duas escolhas
- Onde: `proposta/spec.md`, Worker 5, item (b), linha 130; Worker 6, item (b), linha 138.
- Texto atual: o Worker 5 exige aviso em read_note e get_conflicts sem [núcleo]; o Worker 6 manda montar o conteúdo final e chamar o verificador, também sem a marca.
- Texto proposto: acrescentar [núcleo] à escolha das duas formas de visibilidade e à solução de montar o conteúdo final antes da validação. Manter como requisitos distintos a visibilidade do conflito e a validação do esquema.
- Fonte: acordo Prisma-6 e Prisma-24, com meu voto na r2; a parte 05-06 já está marcada. Tickets 25/30 não escolhem necessariamente as duas formas; 12 exige validação, sem escolher aquele adaptador concreto.
- Situação: falha de propagação de um acordo, sem nova decisão de produto.

### Sextante-21: Redações antigas ainda ligam todas as skills globalmente
- Onde: `proposta/spec-partes/faixas-09-10.md`, faixa 9, “Onde as skills moram”, linha 64; `proposta/spec.md`, Worker 8, “Como se prova”, linha 156.
- Texto atual: “todas [...] ligadas por junction” nas duas pastas globais; teste do núcleo exige “cada junction para agents/skills/”.
- Texto proposto: distinguir armazenamento no acervo de exposição: só as skills gerais entram globalmente; as de papel só na pasta do papel. O teste verifica essa seleção e os destinos efetivamente escolhidos pela implementação, sem exigir ligação global à árvore inteira.
- Fonte: Q-10 e Prisma-16, aceitos pelos três; ticket 15, rodada 2. A implementação da faixa 8 e o bloco “Duas camadas” da faixa 9 já dizem isso.
- Situação: teste e frase antiga contradizem o requisito já aplicado.

### Sextante-22: Teste da guarda ainda usa uma pasta ampla demais
- Onde: `proposta/spec.md`, Worker 9, “Como se prova”, linha 164.
- Texto atual: “gravar em agents/skills/ dá ask no Claude Code e recusa [...] no Codex e no Copilot”.
- Texto proposto: testar gravação numa peça dos caminhos efetivamente protegidos: família maestro, skill de papel e skill nova iniciativa. Verificar também a exceção de routing.yml e a abertura de propostas/uso conforme seus escritores. Não exigir a guarda de toda skill geral enquanto esse alcance está aberto.
- Fonte: Q-1/Prisma-18 e meu ajuste da r2; 40, guarda do acervo; 12, proteção de nova iniciativa; 15, exceção de routing.yml. A decisão de construção do próprio Worker 9 já foi corrigida.
- Situação: teste antigo ampliaria silenciosamente a guarda que o acordo restringiu.

### Sextante-23: Host do proxy ainda é presumido no núcleo
- Onde: `proposta/spec.md`, Worker 10, item (e), linha 170; Worker 3, “Como segue sem esperar”, linha 117.
- Texto atual: “a porta do proxy [...] a faixa 3 a usa no --allowed-host”; “--allowed-host para o endereço do proxy”.
- Texto proposto: “A busca é testada pelo proxy; se necessário, allowed-host recebe o Host efetivamente observado, não um endereço/porta presumido [núcleo].” A atribuição à faixa fica [formato].
- Fonte: Prisma-23 e meu ajuste aceito na r2; `proposta/spec-partes/faixas-09-10.md`, Proxy de MCP, já usa a redação condicional acordada. O 14 decide a busca local e o proxy, não o cabeçalho que ele encaminha.
- Situação: alinhar núcleo e parte; nenhum teste foi executado nesta revisão.

### Sextante-24: Marcação do formato ainda deixa cortes de entrega como ordem vigente
- Onde: `proposta/spec.md`, blocos “Como segue sem esperar as outras faixas”, especialmente Workers 1, 3, 4, 5, 6 e 7; Worker 4, “Como se prova”, linha 123; `proposta/spec-partes/faixas-03-04.md`, faixa 4, “Ordem de corte na hora”, linha 340.
- Texto atual: minutos 0–10/15, dublês e “Se sobrar (min 35–50)” permanecem sem marca no próprio bloco, embora o topo explique a marca [formato].
- Texto proposto: marcar esses blocos [formato] ou inserir uma regra de alcance explícita: “Todos os donos por worker, minutos, dublês, portas por faixa e cortes de tempo abaixo são referência do plano anterior e dependem do formato; não dispensam requisitos.” Não é preciso repetir a marca em cada ocorrência se o alcance ficar inequívoco.
- Fonte: Q-15 e Sextante-17, aceitos; protocolo e 16, replanejamento depois da revisão. Definir o significado da marca no topo não identifica sozinho todos os blocos a que ela se aplica.
- Situação: correção editorial de alcance, sem decidir sequência nova.

## O que sobra sem acordo ou sem aplicação

- Não vejo discordância de requisitos que exija redesenhar banco, busca, escrita, checkpoint, guardas ou kits.
- Ainda não declaro a proposta encerrada: Sextante-20 a Sextante-24 precisam de voto/conferência e aplicação pelo relator. São correções de propagação dos acordos.
- Prisma-26 precisa do aceite da redação funcional acima pelos colegas. Sextante-18 e Sextante-19 ainda dependem do voto formal do Prisma e da aplicação.
- As pendências declaradas na própria spec não viram decisões pelo nosso acordo: formatos, escolhas [núcleo], conteúdo fora de iniciativa, critério mecânico do checkpoint, detector do outro par e itens do 56 permanecem com os rótulos correspondentes.

Só o Quadrante edita proposta/. Nenhuma alteração em antes/, mapa ou tickets.
