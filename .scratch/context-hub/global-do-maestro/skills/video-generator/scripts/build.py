"""Assemble the single-file page (artifact) plus dev/export pages for QA and rendering.
usage: python build.py <project-dir> [--dev]
Reads: src/template.html, src/style.css, src/helpers.js + src/helpers-motion.js + src/player.js, scenes/s*.js,
       assets/icons/*.svg, audio/<id>.mp3, roteiro.json, cues.json (optional)
Writes: dist/<slug>.html (publish this), dist/export.html (UTF-8 wrapped, for MP4 render),
        dist/dev.html (--dev: also includes scenes/_template.js), durations.json"""
import json, base64, re, subprocess, sys, pathlib

P = pathlib.Path(sys.argv[1]).resolve()
DEV = "--dev" in sys.argv
SRC, SCN, ICO, AUD, DIST = P / "src", P / "scenes", P / "assets" / "icons", P / "audio", P / "dist"
DIST.mkdir(exist_ok=True)
roteiro = json.load(open(P / "roteiro.json", encoding="utf-8"))

icons = {}
for f in sorted(ICO.glob("*.svg")):
    txt = f.read_text(encoding="utf-8")
    inner = re.sub(r"^.*?<svg[^>]*>", "", txt, flags=re.S)
    icons[f.stem] = re.sub(r"</svg>\s*$", "", inner, flags=re.S).strip()

audio, durations = {}, {}
for s in roteiro["scenes"]:
    mp3 = AUD / f"{s['id']}.mp3"
    if mp3.exists():
        audio[s["id"]] = "data:audio/mpeg;base64," + base64.b64encode(mp3.read_bytes()).decode()
        durations[s["id"]] = round(float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(mp3)]).decode().strip()), 2)
    else:
        durations[s["id"]] = 20.0
json.dump(durations, open(P / "durations.json", "w"), indent=1)

def narration(s):
    if "lines" in s: return " ".join(l[0] for l in s["lines"])
    return s.get("narration", "")
meta = {"scenes": [{"id": s["id"], "title": s.get("title", s["id"]), "style": s.get("style", ""), "section": s.get("section", ""), "narration": narration(s)} for s in roteiro["scenes"]]}
cues = json.load(open(P / "cues.json", encoding="utf-8")) if (P / "cues.json").exists() else {}
data = (f"window.ROTEIRO={json.dumps(meta, ensure_ascii=False)};\n"
        f"window.DURATIONS={json.dumps(durations)};\n"
        f"window.ICONS={json.dumps(icons)};\n"
        f"window.AUDIO={json.dumps(audio)};\n"
        f"window.CUES={json.dumps(cues, ensure_ascii=False)};\n")
engine = "\n".join((SRC / f).read_text(encoding="utf-8") for f in ["helpers.js", "helpers-motion.js", "player.js"])

def assemble(include_template):
    files = sorted(p for p in SCN.glob("s*.js"))
    if include_template and (SCN / "_template.js").exists():
        files = [SCN / "_template.js"] + files
    scenes = "".join(f"\n/* ---- {p.name} ---- */\n(function(){{\n{p.read_text(encoding='utf-8')}\n}})();\n" for p in files)
    html = (SRC / "template.html").read_text(encoding="utf-8")
    html = html.replace("/*__CSS__*/", (SRC / "style.css").read_text(encoding="utf-8"))
    html = html.replace("/*__DATA__*/", data).replace("/*__ENGINE__*/", engine).replace("/*__SCENES__*/", scenes)
    return html, [p.name for p in files]

WRAP = "<!doctype html><html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'></head><body>{}</body></html>"
html, names = assemble(False)
slug = re.sub(r"[^a-z0-9]+", "-", (re.search(r"<title>(.*?)</title>", html) or [None, "video"])[1].lower()).strip("-") or "video"
(DIST / f"{slug}.html").write_text(html, encoding="utf-8")
(DIST / "export.html").write_text(WRAP.format(html), encoding="utf-8")   # charset-safe copy for the renderer
print(f"dist/{slug}.html {len(html.encode())/1024/1024:.2f} MB scenes: {names}")
if DEV:
    dev, names = assemble(True)
    (DIST / "dev.html").write_text(WRAP.format(dev), encoding="utf-8")
    print("dist/dev.html scenes:", names)
# syntax check of every inline script block
import re as _re
bad = 0
for m in _re.finditer(r"<script>([\s\S]*?)</script>", html):
    r = subprocess.run(["node", "-e", "new Function(require('fs').readFileSync(0,'utf8'))"], input=m.group(1).encode(), capture_output=True)
    if r.returncode: bad += 1; print("SYNTAX ERROR in a script block:", r.stderr.decode()[:300])
print("durations:", durations, "| script blocks bad:", bad)
