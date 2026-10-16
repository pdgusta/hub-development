# Laços L2, contador e cidade v2 — Prumo, 2026-10-14

## Parecer vigente após correção dirigida

**L2 APROVADO. Os três achados estão resolvidos; pode seguir L3.** Contador e cadastro histórico continuam aprovados. O parecer inicial abaixo permanece como histórico.

Conferidos código, contrato §4.5/§4.6 e as três reproduções próprias, sobre cópia curta:

1. **Exposição de fontes resolvida:** painel na raiz do laço e seu `config.json` agora retornam 404. `carta_pode_servir` só libera subpasta de publicação sem descritor/origem declarada, exige laço bem formado e considera caminhos reais e auxiliares SQLite. Testes de painel legítimo, fontes, atalhos e laço malformado passaram; os testes do projeto real preservam os painéis e seus recursos de apresentação.
2. **Descritor malformado resolvido:** `ligacoes[0].de = []` agora produz `LacoMalformado`; lista HTTP 200, linha ruim marcada e outro laço intacto. Suíte confirma detalhe 422, estado 200 e validação de ids de controles/contadores/capacidades/POST, sem catch geral.
3. **Informação de definição resolvida:** mudança compatível de faixa com hash anterior continua 409, agora com `definicao_mudou: null`. Contrato e testes distinguem desconhecido de mudança provada e do `antes` incompatível sob mesma revisão. Não há mais o falso negativo reproduzido anteriormente.

Execução própria nesta correção: **218 testes do núcleo OK** (97,6 s), **6 do projeto real OK**. `review_l2.py` reexecutado incluindo Edge: contador 2→1 preservado, zero erro JS; resultados atualizados em `revisao-l2/` na pasta do papel. Processos próprios encerrados e cópia removida; nenhuma escrita na caixa real ou implementação. Sem novos achados ou ampliação de escopo.

Próximo: implementar/revisar L3 conforme brief; este aceite é do núcleo, não da tela ainda não entregue.

---

**L2 ainda não aprovado: três achados abaixo. Contador de cartas e cadastro histórico da cidade v2 aprovados.** Revisão restrita a esta entrega, sem reabrir acabamento ou o desenho da cidade.

## Achados do L2

1. **Bloqueia — exceção de painel expõe fontes do laço.** `nucleo/torre.py:564`, decisão 19. A exceção libera qualquer arquivo permitido quando a pasta da carta está dentro do laço, inclusive quando é a própria raiz. Na cópia registrei `painel-regas`, arquivo `lacos/regas/painel.html`, pasta `lacos/regas`: tanto `/carta/painel-regas/` como `/carta/painel-regas/config.json` retornaram **200**, e o segundo trouxe `gate_novos`. Isso viola “fontes não são servidas como arquivo” da §4.4. Recomendo servir o painel e seus recursos de apresentação sem liberar fontes/descritores/bancos/logs; uma pasta exclusiva de publicação, com confinamento e sem atalhos para fontes, é uma solução simples. Cobrir painel na raiz e em subpasta, preservando HTML/CSS/fontes legítimos. O bloqueio pelo ancestral System design é bom, mas não basta.

2. **Importante — descritor malformado quebra a lista inteira.** `nucleo/lacos.py:475` (também associações de nó em controles/contadores). Com `ligacoes[0].de: []`, `validar_laco` levanta `TypeError: unhashable type: 'list'`; na mesma cópia **GET /api/lacos retorna 500 erro-interno**. Deveria retornar a lista, com esse laço malformado e o outro intacto; detalhe deveria ser 422. Validar tipo de ids antes de usá-los em sets/dicts, inclusive os vindos do POST (ex.: `comentario-no.no`), e testar formas lista/objeto. Não ocultar isso em um catch geral que trate todo defeito de programação como arquivo ruim.

3. **Importante — decisão 7 transforma desconhecimento em informação falsa.** `nucleo/lacos.py:1484`. Li a revisão, mudei só o máximo da faixa de `gate_novos` para 0,49 e enviei um pedido ainda permitido, 0,1 → 0,2, com o hash anterior. O 409 está correto, mas traz **`definicao_mudou: false`**, embora a definição tenha mudado. Também ocorre com unidade/origem/releitura sem mudança de tipo. Só hash/tipo/valor não provam ausência de mudança. Recomendo distinguir **desconhecido** de falso no contrato/API, com texto neutro “a configuração ou regra mudou”, ou comparar contra um retrato anterior confiável. Não é necessário guardar histórico só para essa indicação. Manter a recusa 409 e a conferência campo a campo pelo maestro.

## Decisões e partes aceitas

Arquitetura do L2 segue o L1: fontes confinadas e só leitura, SQLite respeitando WAL, endpoints próprios, revisão com definições/precondições, caixa imutável, validação de recibos, grupos atuais, idempotência antes da validação e aviso separado de trabalho pendente. Não encontrei motivo para ampliar esta correção a outro desenho.

Decisão **8** aceita: revisão antes do tipo permite tratar uma mudança legítima de tipo como conflito; forma antes/depois continua validada. Decisão **10** aceita como ajuste explícito do contrato: sem fonte de pausa no formato, o servidor valida a capacidade, e o maestro revalida pausa/execução antes de qualquer efeito. Não apresentar o recebimento como retomada executada. Decisão **11** aceita: revisão bem formada obrigatória em todos os pedidos, contextual fora de mudar-controle. Demais decisões conservadoras aceitas, ressalvados os achados 7/19 e a robustez acima; registrar as decisões no contrato antes do L3.

Retry de `PermissionError` em `_trocar` é limitado, específico e preserva erro persistente; testes novos exercitam ambos os casos. A instabilidade anterior sem causa confirmada continua descrita como tal.

## Contador e carta

**Contador aprovado:** li `app.cartasAguardando`, a casca, Início e Designs. Exige `pede_veredito === true`, vigente efetiva, não mestra e ausência de aprovação não substituída. Aprovação ou recusa encerra essa espera; histórico e cartas substituídas não contam. Limite de não considerar data está declarado, sem promessa de reabrir automaticamente uma carta editada.

Prova própria no Edge, sobre cópia curta: uma rodada + uma carta = **2 aguardando você**; POST de aprovação retornou 200; após recarga = **1 aguardando você**. Capturas abertas, nenhum erro JS. A casca direciona só cartas à primeira carta; com rodada, mantém Responder. Prova fornecida também cobre selo de Designs/leitor.

**Cadastro aprovado:** `system-design-cidade-v2` está histórica, com decisão de recusa do Gustavo e o vínculo `substitui` preservado. Este parecer não reaprova o desenho nem troca o System design vigente.

## Evidência e próximo passo

- Execução própria: **206 testes do núcleo OK** (79,9 s) e **6 do projeto real OK**, estes em portal temporário, só leitura das fontes reais.
- Provas adicionais próprias: `review_l2.py` e `revisao-l2/resultados.json`, `contador-antes.png`, `contador-depois.png`, na pasta deste papel. Cópia em `C:/tmp/pr-l2`, removida ao terminar; servidor e Edge próprios encerrados. Nenhuma escrita na caixa real nem na implementação.
- Próximo: corrigir somente os três achados e devolver revisão dirigida. O L3 pode ser preparado, mas o núcleo ainda não tem aceite para integração final.
