---
name: freellmapi-tts-e-transcricao
description: "FreeLLMAPI local (localhost:3001, FREELLM_API_KEY): TTS por idioma (en → Cloudflare MeloTTS, resto → Gemini), nunca model auto; cotas; transcrição para legendas"
metadata:
  node_type: memory
  type: reference
  originSessionId: a8562ee9-94be-4d53-81d8-74e57b69f06b
  modified: 2026-10-11T01:46:17.356Z
---

O gateway FreeLLMAPI roda em `http://localhost:3001/v1` e a chave fica na variável de usuário `FREELLM_API_KEY`
(não aparece no `env` do Git Bash; ler com `[Environment]::GetEnvironmentVariable('FREELLM_API_KEY','User')`).
Fonte: clone local `C:\Projetos\freellmapi` (README e `docs/en/api/01-rest-api.md`); `services/media.ts` mapeia
vozes OpenAI para Gemini (`ash`→Charon, `coral`→Sulafat, `sage`→Sadaltager, `cedar`→Kore).

- **TTS:** `POST /v1/audio/speech` com **modelo explícito, nunca `auto`**: desde que há chaves Cloudflare (2026-10-11), a
  cadeia do `auto` começa no MeloTTS, que o gateway trava em `lang:'en'`. Regra do Gustavo: **inglês → Cloudflare**
  (`@cf/myshell-ai/melotts`, único modelo Cloudflare que funciona; os Deepgram Aura falham porque o gateway manda
  `prompt` em vez de `text`), **qualquer outro idioma → Google** (`gemini-3.1-flash-tts-preview`, depois
  `gemini-2.5-flash-preview-tts` quando o 3.1 devolve 429 de cota diária; reset à meia-noite do Pacífico, 04:00 BRT).
  `voice:"ash"` → Charon no Google; o retorno é WAV/PCM mesmo pedindo mp3; 3 em paralelo sem 429.
- **Cotas (2026-10-11):** Gemini TTS não publica RPM/RPD do nível gratuito (por projeto, ver no AI Studio); Cloudflare
  Workers AI 10k neurons/dia por conta, reset 00:00 UTC, MeloTTS 18,63 neurons/min. Painel só liga/desliga modelos de
  mídia, não reordena; a Fallback Chain é só de chat. Relatório em
  `~/.claude/skills/video-generator-workspace/freellmapi-cotas-tts-2026-10-11.md`.
- **Vozes aprovadas pelo Gustavo (2026-10-11, ouviu os clipes):** MeloTTS em inglês e Gemini 3.1 em pt-BR são ambas boas;
  não julgar qualidade de voz sem ouvir. Ele mantém várias chaves Google para quase nunca bater a cota (cota do Gemini é
  por projeto, não por chave: só chaves de projetos diferentes somam).
- **Transcrição com tempos:** `POST /v1/audio/transcriptions` multipart (`model=auto`, `response_format=verbose_json`,
  `timestamp_granularities[]=word`) devolve `words` e `segments`; alinhar as frases do roteiro às palavras com
  `difflib.SequenceMatcher` dá cues de legenda com ±0,3 s (script `gen2.py` do vídeo 2).

**Como aplicar:** uma requisição por cena, loudnorm `I=-16` e MP3 64k mono no ffmpeg; cues em `cues.json`
`{id:[[ini,fim,texto]]}` que o player lê. Ver [[gemini-tts-interactions-api]] e [[headless-edge-para-qa-visual]].
