"""Narration per scene + caption cue timing.
usage: python gen_tts.py <project-dir> [ids...] [--provider freellmapi|gemini] [--voice ash] [--lang pt-BR|en] [--model id[,id2]] [--workers 3] [--no-cues]
Reads roteiro.json: scenes[].lines = [[narration sentence, caption sentence (optional)], ...]  (or scenes[].narration)
Writes audio/<id>.mp3 (silence-trimmed, loudnorm -16 LUFS, 64k mono), durations.json, cues.json, tts-log.json.
Providers:
  freellmapi  POST $FREELLM_BASE_URL/v1/audio/speech  (base and key FREELLM_API_KEY are Windows *user* env vars, read via
              PowerShell if absent from the shell; base falls back to http://localhost:3001; --base overrides it). Model by language, never "auto": English -> Cloudflare MeloTTS then Gemini; anything else ->
              Gemini 3.1 TTS then 2.5 TTS (the gateway pins MeloTTS to English). Voice names are OpenAI-style, mapped per provider
              (ash->Charon, coral->Sulafat, sage->Sadaltager, cedar->Kore on Gemini). Returns WAV even if mp3 is requested.
  gemini      POST https://generativelanguage.googleapis.com/v1beta/interactions (GEMINI_API_KEY), model gemini-3.8-flash-tts,
              voice e.g. Sulafat (pt-BR female) / Charon; style hint in speech_metadata. Keep workers<=2 (429 otherwise).
Cue timing: transcribes each clip (freellmapi /v1/audio/transcriptions, verbose_json + word timestamps) and aligns the
script sentences to the transcript words with difflib; falls back to proportional timing when words are missing."""
import json, os, re, subprocess, sys, time, pathlib, difflib, concurrent.futures as cf, urllib.request, mimetypes, uuid, base64, argparse

ap = argparse.ArgumentParser()
ap.add_argument("project"); ap.add_argument("ids", nargs="*")
ap.add_argument("--provider", default="freellmapi"); ap.add_argument("--voice", default=None); ap.add_argument("--workers", type=int, default=3)
ap.add_argument("--no-cues", action="store_true"); ap.add_argument("--base", default=None, help="gateway /v1 URL; default: $FREELLM_BASE_URL/v1, else http://localhost:3001/v1")
ap.add_argument("--model", default=None, help="freellmapi: provider model ids tried in order; default depends on --lang")
ap.add_argument("--lang", default=None, help="narration language (pt-BR, en...); default: roteiro.json 'lang', else guessed from the text")
a = ap.parse_args()
P = pathlib.Path(a.project).resolve(); AUD = P / "audio"; AUD.mkdir(exist_ok=True)
script = json.load(open(P / "roteiro.json", encoding="utf-8"))
VOICE = a.voice or script.get("voice", "ash"); STYLE = script.get("style", "")

def guess_lang(text):
    w = set(text.lower().split()); pt = len(w & {"de","que","não","nao","uma","com","para","por","você","voce","mais","como","isso","esse","essa"}); en = len(w & {"the","and","of","to","is","that","with","for","this","you","are","it"})
    return "pt-BR" if pt >= en else "en"
# Provider by language, decided with the user on 2026-10-11: English narration goes to Cloudflare (MeloTTS is the only
# Cloudflare voice that works through the gateway; the Deepgram Aura adapter sends `prompt` where Cloudflare wants `text`),
# everything else goes to Google (the gateway pins MeloTTS to lang 'en', so it cannot speak pt-BR). Gemini stays as the
# last resort for English when the Cloudflare neurons run out.
GEMINI = "gemini-3.1-flash-tts-preview,gemini-2.5-flash-preview-tts"
def models_for(lang):
    if a.model: return a.model
    return "@cf/myshell-ai/melotts," + GEMINI if (lang or "").lower().startswith("en") else GEMINI
LANG = a.lang or script.get("lang") or guess_lang(" ".join(l[0] for s in script["scenes"] for l in (s.get("lines") or [[s.get("narration", ""), ""]])))
MODELS = models_for(LANG)
print(f"narration language: {LANG}; freellmapi models: {MODELS}")

def user_env(name):
    v = os.environ.get(name)
    if v: return v
    try: return subprocess.check_output(["powershell", "-NoProfile", "-Command", f"[Environment]::GetEnvironmentVariable('{name}','User')"]).decode().strip()
    except Exception: return ""

def retry(fn, tries=8, base=8):
    for i in range(tries):
        try: return fn()
        except Exception as e:
            if i == tries - 1: raise
            time.sleep(base * (i + 1))

def post_json(url, body, headers, timeout=240):
    req = urllib.request.Request(url, data=json.dumps(body).encode(), method="POST", headers=dict(headers, **{"Content-Type": "application/json"}))
    with urllib.request.urlopen(req, timeout=timeout) as r: return r.read(), dict(r.headers)

def post_multipart(url, fields, filepath, headers, timeout=240):
    b = "----vg" + uuid.uuid4().hex; body = b""
    for k, v in fields.items(): body += f"--{b}\r\nContent-Disposition: form-data; name=\"{k}\"\r\n\r\n{v}\r\n".encode()
    body += (f"--{b}\r\nContent-Disposition: form-data; name=\"file\"; filename=\"{pathlib.Path(filepath).name}\"\r\nContent-Type: {mimetypes.guess_type(filepath)[0] or 'application/octet-stream'}\r\n\r\n").encode() + pathlib.Path(filepath).read_bytes() + b"\r\n"
    body += f"--{b}--\r\n".encode()
    req = urllib.request.Request(url, data=body, method="POST", headers=dict(headers, **{"Content-Type": f"multipart/form-data; boundary={b}"}))
    with urllib.request.urlopen(req, timeout=timeout) as r: return json.loads(r.read().decode())

FL_KEY = user_env("FREELLM_API_KEY"); FL_H = {"Authorization": "Bearer " + FL_KEY}
# The gateway moved off this machine (2026-10-24: native on the personal notebook, reached over the tailnet).
a.base = a.base or (user_env("FREELLM_BASE_URL") or "http://localhost:3001").rstrip("/") + "/v1"
G_KEY = user_env("GEMINI_API_KEY")

def synth(text):
    if a.provider == "gemini":
        body = {"model": "gemini-3.8-flash-tts", "input": [{"type": "user_input", "content": [{"type": "text", "text": text, "annotations": [{"type": "speech_metadata", "style": STYLE}]}]}],
                "response_format": {"type": "audio"}, "generation_config": {"speech_config": [{"voice": VOICE}]}}
        data, h = retry(lambda: post_json("https://generativelanguage.googleapis.com/v1beta/interactions", body, {"x-goog-api-key": G_KEY}), base=12)
        return base64.b64decode(json.loads(data)["steps"][0]["content"][0]["data"]), "gemini"
    last = None
    for model in [m.strip() for m in MODELS.split(",") if m.strip()]:
        try:
            data, h = retry(lambda: post_json(a.base + "/audio/speech", {"model": model, "input": text, "voice": VOICE, "response_format": "mp3"}, FL_H), tries=3)
            return data, (h.get("X-Provider") or h.get("x-provider") or "") + ":" + model
        except Exception as e:
            last = e; print(f"  {model}: {e}; trying next model" if "," in MODELS else f"  {model}: {e}")
    raise last

def lines_of(s):
    if "lines" in s: return [(l[0], l[1] if len(l) > 1 else "") for l in s["lines"]]
    return [(s.get("narration", ""), s.get("caption", ""))]

def tts(s):
    sid = s["id"]; text = " ".join(l[0] for l in lines_of(s)); raw, mp3 = AUD / f"{sid}.raw", AUD / f"{sid}.mp3"; info = {"id": sid}
    if not mp3.exists():
        data, prov = synth(text); raw.write_bytes(data); info["provider"] = prov; info["bytes"] = len(data)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(raw), "-af",
                        "silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse,apad=pad_dur=0.4,loudnorm=I=-16:TP=-1.5:LRA=11",
                        "-ar", "44100", "-c:a", "libmp3lame", "-b:a", "64k", "-ac", "1", str(mp3)], check=True)
    info["dur"] = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(mp3)]).decode().strip())
    return info

norm = lambda w: re.sub(r"[^a-z0-9]", "", w.lower())

def align(s, dur):
    L = lines_of(s); mp3 = AUD / f"{s['id']}.mp3"
    words = []
    if not a.no_cues and FL_KEY:
        try:
            tr = retry(lambda: post_multipart(a.base + "/audio/transcriptions", {"model": "auto", "response_format": "verbose_json", "timestamp_granularities[]": "word"}, mp3, FL_H), tries=3)
            words = tr.get("words") or []
            if not words:
                for seg in tr.get("segments", []):
                    ws = seg["text"].split(); n = max(1, len(ws)); span = seg["end"] - seg["start"]
                    words += [{"word": w, "start": seg["start"] + span * k / n, "end": seg["start"] + span * (k + 1) / n} for k, w in enumerate(ws)]
        except Exception as e:
            print("transcription failed for", s["id"], "->", str(e)[:120], "(proportional timing)")
    sw, owner = [], []
    for li, (en, _) in enumerate(L):
        for w in en.split():
            if norm(w): sw.append(norm(w)); owner.append(li)
    mapidx = {}
    if words:
        tw = [norm(w["word"]) for w in words]
        for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(a=sw, b=tw, autojunk=False).get_opcodes():
            if tag == "equal":
                for k in range(i2 - i1): mapidx[i1 + k] = j1 + k
    cues = []
    for li in range(len(L)):
        idx = [i for i, o in enumerate(owner) if o == li]
        m = [mapidx[i] for i in idx if i in mapidx]
        if m: start, end = words[min(m)]["start"], words[max(m)]["end"]
        else: start, end = (idx[0] / len(sw)) * dur, ((idx[-1] + 1) / len(sw)) * dur
        cues.append([round(start, 2), round(end, 2), L[li][1]])
    for i in range(len(cues)):
        if i > 0 and cues[i][0] < cues[i - 1][1]: cues[i][0] = cues[i - 1][1]
        nxt = cues[i + 1][0] if i + 1 < len(cues) else dur
        cues[i][1] = round(min(max(cues[i][1], cues[i][0] + 0.8), nxt - 0.05 if i + 1 < len(cues) else dur), 2)
    return cues, len(words), len(mapidx)

def work(s):
    info = tts(s); cues, nw, nm = align(s, info["dur"]); info.update({"words": nw, "matched": nm}); return s["id"], info, cues

scenes = [s for s in script["scenes"] if not a.ids or s["id"] in a.ids]
durs = json.load(open(P / "durations.json")) if (P / "durations.json").exists() else {}
cues_all = json.load(open(P / "cues.json", encoding="utf-8")) if (P / "cues.json").exists() else {}
log = {}
with cf.ThreadPoolExecutor(max_workers=(2 if a.provider == "gemini" else a.workers)) as ex:
    for sid, info, cues in ex.map(work, scenes):
        durs[sid] = round(info["dur"], 2); log[sid] = info
        if any(c[2] for c in cues): cues_all[sid] = cues
        print(f"{sid} {info['dur']:6.2f}s provider={info.get('provider')} words={info['words']} matched={info['matched']}")
json.dump(durs, open(P / "durations.json", "w"), indent=1)
json.dump(cues_all, open(P / "cues.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
json.dump(log, open(P / "tts-log.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("total", round(sum(durs.get(s["id"], 0) for s in script["scenes"]), 1), "s")
