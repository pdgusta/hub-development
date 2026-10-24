# Narration and captions

`scripts/gen_tts.py` does the work; this file is about the choices.

## Providers

**FreeLLMAPI (gateway at `$FREELLM_BASE_URL/v1`, a Windows *user* env var; since 2026-10-24 it runs on the user's
personal notebook over the tailnet, `http://100.121.86.61:3001`; `localhost:3001` only as the fallback)** — the user's
own pool of free providers.
- Key: Windows *user* environment variable `FREELLM_API_KEY` (not visible in the Git Bash `env`; the script reads it via
  PowerShell). Test first when the user asks: `GET /v1/models` with the bearer, then one short `POST /v1/audio/speech`.
- Request: `{model:"<provider model id>", input, voice, response_format:"mp3"}` with an explicit model, which `gen_tts.py`
  picks from the narration language (`lang` in roteiro.json or `--lang`): **English → `@cf/myshell-ai/melotts`** (Cloudflare,
  10k neurons/day ≈ 9 h of speech; the gateway ignores `voice` for it) **then Gemini; every other language → Gemini**
  (`gemini-3.1-flash-tts-preview`, then `gemini-2.5-flash-preview-tts`). Rule agreed with the user on 2026-10-11. The
  Deepgram Aura models on Cloudflare fail through this gateway (it sends `prompt`, Cloudflare wants `text`): do not list them. Do not use
  `model:"auto"`: the gateway's failover chain is ordered by the dashboard priority and, once a Cloudflare key exists,
  MeloTTS (priority 211) comes before Gemini (213/214) and the gateway sends it `lang:'en'` regardless of the text, so
  a pt-BR script comes back in English (observed 2026-10-11). The response may be WAV regardless of the format asked
  (`X-Provider` says who answered); ffmpeg normalises it.
- Quotas (2026-10-11): Gemini TTS limits are not published for the free tier and are per project, reset at midnight
  Pacific; the 3.1 preview hit `429 exceeded your current quota` after ~20 clips in a day while 2.5 kept answering,
  hence the two-model default. Cloudflare Workers AI: 10,000 neurons/day per account, reset 00:00 UTC
  (MeloTTS 18.63 neurons/min; Aura ≈1.4k–2.7k neurons per 1k characters, i.e. a few minutes of speech per day).
- Voices are OpenAI names mapped per provider (`server/src/services/media.ts` in the gateway's repo): on Gemini
  `ash`→Charon (informative), `coral`→Sulafat (warm, good for pt-BR female), `sage`→Sadaltager, `cedar`→Kore,
  `onyx`→Gacrux, `nova`→Zephyr. Pollinations and SiliconFlow use their own sets. If the user is fine with several voices,
  failover is harmless; for one consistent narrator keep one voice and check `tts-log.json` providers.
- Rate limit header `X-RateLimit-Limit: 120`/min; 3 parallel requests were fine.
- Transcription: `POST /v1/audio/transcriptions` multipart (`model=auto`, `response_format=verbose_json`,
  `timestamp_granularities[]=word`) returns words with times; that is what times the captions.

**Gemini TTS (direct)** — `POST https://generativelanguage.googleapis.com/v1beta/interactions`, header `x-goog-api-key`
(`GEMINI_API_KEY`), model `gemini-3.8-flash-tts`, body `input[{type:"user_input",content:[{type:"text",text,
annotations:[{type:"speech_metadata",style}]}]}]`, `response_format:{type:"audio"}`,
`generation_config.speech_config:[{voice}]`; audio in `steps[0].content[0].data` (base64 WAV 24 kHz). Six parallel calls
hit 429; two with 12 s backoff pass. Voices: Sulafat/Aoede/Leda/Kore female, Charon/Puck/Iapetus male. Languages are
auto-detected; a Portuguese style hint ("narradora calma, clara") helps prosody.

## Script shape that makes captions work

`lines: [[narration sentence, caption sentence], …]` with a 1:1 correspondence. The aligner matches the narration
words to the transcript and gives each caption the span of its sentence; a caption that merges two narration sentences
gets the first sentence's span only. Keep sentences under ~25 words so a caption fits two lines at 25 px.

## Audio processing (what the script applies)

Silence trimmed at both ends (−45 dB), 0.4 s of padding at the end (room for the scene's last beat), `loudnorm
I=-16 TP=-1.5`, MP3 64 kbps mono 44.1 kHz (≈0.5 MB per minute embedded as base64). Durations in `durations.json` are
the ground truth every scene builder receives.

## Caption rendering

The player shows the current cue in `#cap`: bottom-centre, 25 px, max-width 1300, 22 px from the bottom, dark pill
behind white text. The punchline helper clamps its `y` to 712 so a three-line caption never overlaps it. In export mode
captions are drawn into the frames (burned in). A second audio track (a real dub) is a separate `gen_tts.py` run with
`--provider`/`--voice` for the other language plus a second mux; offer it, do not assume it.
