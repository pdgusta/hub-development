---
titulo: Pode iniciar a pesquisa de modelos de embeddings?
ticket: 54
aberta: 2026-10-14
estado: absorvida
---

O laço da pesquisa ampla foi copiado para `laco-embeddings/` e ajustado para modelos de embeddings. Nada chamou
modelo ainda.

**Como roda:**
- **Onda 1:** 36 perguntas = 6 ângulos × 3 línguas (português, inglês, chinês, porque muitos modelos vêm de
  laboratórios chineses) × 2 formulações. Cada pergunta vai a dois modelos diferentes do FreeLLMAPI.
- **Os seis ângulos:**
  - placares públicos (MTEB, MMTEB);
  - modelos que rodam em CPU no Windows;
  - APIs com nível gratuito;
  - modelos feitos para português;
  - modelos pequenos;
  - técnicas e rerankers.
- **Bola de neve:** cada modelo novo vira "alternativas a X" e "com que se usa X", e os termos que se repetem viram
  pergunta nova.
- **Para sozinho** em duas ondas seguidas com menos de 5% de novos, depois da calibração com 7 sementes escondidas.
  Os modelos nunca veem os nomes das sementes.
- **O juntador agora junta pelo endereço do Hugging Face**, além do GitHub, para o mesmo modelo não aparecer duas
  vezes.
- **Ninguém do Claude vigia os processos:** eu ligo os scripts fora do Claude Code e confiro o painel.
- **No fim:** confiro na fonte primária (model card no Hugging Face, documentação do provedor, placar do MTEB) a
  lista que o laço entregar. Monto a lista curta, que vai para uma bancada só, com os mesmos corpus, 40 perguntas e
  scripts do teste da busca.

**Orçamento:**
- O despachante vê 148 modelos aptos agora.
- Estimativa de 400 a 700 chamadas, com teto de segurança de **1.200 tentativas ou 4 horas**, o que vier primeiro.
  A pesquisa ampla usou 7.388 num dia.
- O despachante gasta no máximo 90% da cota diária de cada pool e respeita o limite por minuto. A Cloudflare
  está sem cota até as 21h, e ele a pula até lá.
- Do Claude, só esta sessão do maestro, para conferir e escrever; nenhum agente extra.

## Pode iniciar?
id: pode-iniciar
tipo: aprovar

## Teto de segurança
id: teto
tipo: escolha
recomendada: A

- A: 1.200 tentativas ou 4 horas
- B: 600 tentativas ou 2 horas
- C: 2.500 tentativas ou 8 horas

## Algo mais?
id: algo-mais
tipo: texto
