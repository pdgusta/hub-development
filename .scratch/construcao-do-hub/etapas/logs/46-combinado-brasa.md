# 46 x 45: o que cada um toca (Cinzel, 2026-10-17)

- Cinzel (46): instalar.ps1, 08-harnesses.mjs, env/10.env.modelo (linha nova HUB_PAR_ID), bin/verificar-pastas.mjs,
  hooks/roteamento/registro.mjs, bin/lib/par.mjs (novo), kit/par/espera.mjs (novo, a espera da convergência).
- Brasa (45): compose.yml, 04-banco.ps1, banco.psm1, env/04.env.modelo, o gerador dos dois .env.
- Pedido à Brasa: o gerador dos dois .env (New-EnvParesBanco ou o comando novo) escreve HUB_PAR_ID=<id do par> em cada
  .env (minúsculas, letras, números e hífen; diferente nos dois). O kit (08) recusa .env sem HUB_PAR_ID.
- A espera do 46 usa o leitor da vigia (HUB_VIGIA_LEITOR_DB + HUB_LIVESYNC_CLI: sync e ls) e compara com o disco.
