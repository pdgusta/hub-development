# Lições do vault

Type: grilling
Status: resolved

## Question

Que regras do vault `ai-operating-system` tiraram valor do que ele deveria entregar, e o que o hub não
deve repetir? O agente lê antes as regras do vault (`~/Documents/Projetos/ai-operating-system`), e o
Gustavo aponta as que atrapalharam. Contexto: Q10 em `../mapeamento.md`.

## Comments

- 2026-10-01: rodada 1 em `respostas.md` (Q1 valor que falhou; Q2 regras A/O/?; Q3 levantar
  histórico). Fontes lidas no vault: `AGENTS.md`, `charter.md`, `core/operating-rules.md`,
  `core/context-boundaries.md`, `architecture.md` §3.3, DEC-0014/0015/0016/0018.
- 2026-10-01, respostas da rodada 1:
  - **Q1:** os resultados que mais falharam foram (1) contexto mínimo, confiável e relevante, (4) estado
    sem ler chats e (6) só o contexto necessário. Nas palavras dele: "Era contexto crescendo demais sem
    contrato claro de file-first ou handoff, era leitura excessiva e não apenas do que importa. Era eu
    tendo que apontar pra pastas e arquivos por falta de leitura". (7) nem chegou a existir, porque
    nenhuma rotina foi criada; (8) entregou algum valor, mas pode ser ajustado.
  - **Q2:** **A** (atrapalhou) em concorrência (a), guardrails (b, "ficou excessiva"), processo de
    mudança CHG (f), paridade com evidência (h) e tom e forma (l). **O** (herdar) em isolamento (c),
    complexidade conquistada (d), classificação (e), adaptadores idênticos (g), triagem (i) e leitura
    mínima (j, "porém para o RAG," frase incompleta, vai para a rodada 2). **?** em efeitos externos (k).
  - **Q3:** não levantar o histórico do vault.
- 2026-10-01: rodada 2 em `respostas.md`.
- 2026-10-01, respostas da rodada 2:
  - **Q4:** a porta de entrada passa a ser a camada de busca: "pode ser, o que for mais efetivo e
    plausível é melhor".
  - **Q5:** a causa principal foi (c), não haver contrato de onde gravar; (a), arquivos que só
    cresciam, também acontecia. Muitos arquivos nem chegavam ao `inbox/` ou ao `knowledge/`, e ele
    tinha de pedir. "São só exemplos, não quero aumentar regras pra corrigir algo não funcionando."
  - **Q6:** (i). O agente resolve o que o git resolve e só para, avisando, quando há colisão real.
  - **Q7:** (ii). Pedem aval o contrato do hub, os adaptadores e as exclusões ou reescritas grandes.
- 2026-10-01: rodada 3 em `respostas.md`, com a lista final de lições para confirmar.
- 2026-10-01, resposta da rodada 3: Q8 "ok", a lista como está.

## Answer

Lições do vault `ai-operating-system` para o hub (Gustavo confirmou em 2026-10-01). Os resultados que
mais falharam no vault foram contexto mínimo e confiável, estado sem ler chats e só o contexto
necessário; a causa principal foi não haver contrato de onde gravar.

**Lição de cima, que vale para as outras:** uma falha se corrige com mecanismo, ou tirando regra,
nunca acrescentando regra.

**O que o hub não repete:**
1. Não ter um lugar certo para cada coisa. Cada tipo de informação tem um lugar só, escrito no contrato.
2. Gravar só quando o Gustavo pede. O que importa chega ao lugar certo, inclusive a triagem e a
   promoção, por um mecanismo do hub (o checkpoint), e não por uma regra que o agente precisa lembrar.
3. Arquivos que só crescem. Todo arquivo tem um destino quando envelhece: compactar ou arquivar.
4. Uma cadeia de índices mantida à mão como porta de entrada. A porta é a camada de busca; um índice
   só existe onde a busca não basta.
5. Parar e perguntar a cada colisão. O agente resolve o que o git resolve e só para, avisando, quando
   há colisão real.
6. Aval para tudo. Pedem aval só o contrato do hub, os adaptadores e as exclusões ou reescritas grandes.
7. Cerimônia de mudança (pacote CHG, gates, executor separado do verificador). O hub muda pelo fluxo
   do Matt, com tickets.
8. Evidência por superfície como ritual. Os harnesses são verificados uma vez, no ticket
   "Verificação dos cinco critérios nas duas máquinas".
9. Documento longo e normativo. Textos curtos e diretos, e frontmatter só com o que a busca ou o
   contrato usam.

**O que o hub herda:**
10. Isolamento por domínio e iniciativa, com promoção explícita para compartilhar.
11. Complexidade conquistada: uma camada só entra se resolve um dos cinco critérios.
12. Distinção entre fato, hipótese, decisão e recomendação.
13. Adaptadores idênticos entre os harnesses, onde o harness permitir (o contrato entra pela camada
    global de cada um; ver "Acesso dos agentes: pesquisa").
14. Triagem do que é ambíguo, feita pelo checkpoint, e não a pedido.

**Registro, sem lição:** as rotinas de manutenção nunca chegaram a existir; a continuidade entre
superfícies entregou algum valor; a confirmação para efeitos externos ficou indiferente (GitHub
privado e Tailscale já têm aval).
