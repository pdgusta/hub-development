---
name: gemini-tts-interactions-api
description: "Como gerar narração pt-BR com o Gemini TTS (Interactions API, voz Sulafat, chave GEMINI_API_KEY no ambiente, limite de taxa)"
metadata:
  node_type: memory
  type: reference
  originSessionId: a8562ee9-94be-4d53-81d8-74e57b69f06b
  modified: 2026-10-10T23:31:23.032Z
---

A chave do Gemini está em `GEMINI_API_KEY` (e `GEMINI_API_KEY_1`) nas variáveis de ambiente do Gustavo.
O TTS atual é pela Interactions API (`POST https://generativelanguage.googleapis.com/v1beta/interactions`,
header `x-goog-api-key`), modelo `gemini-3.8-flash-tts`, corpo com `input[{type:"user_input",content:[{type:"text",
text, annotations:[{type:"speech_metadata", style}]}]}]`, `response_format:{type:"audio"}` e
`generation_config.speech_config:[{voice:"Sulafat"}]`. O áudio volta em `steps[0].content[0].data` (base64 de WAV
24 kHz mono). Voz feminina pt-BR que funcionou: Sulafat (calma, "warm"). Com 6 chamadas paralelas deu HTTP 429;
2 em paralelo com espera de 12 s por tentativa passou.

**Como aplicar:** script `gen.py` do explainer (scratchpad da sessão de 2026-10-10) é o modelo; converter para
MP3 48k com ffmpeg e embutir como data URI (cerca de 0,5 MB por minuto). Ver [[headless-edge-para-qa-visual]].
