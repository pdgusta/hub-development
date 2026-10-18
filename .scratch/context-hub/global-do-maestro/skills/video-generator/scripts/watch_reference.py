"""Prepare a reference video for a style analyst: transcript as "mm:ss text" lines, low-res download, frames every N s,
2x2 contact sheets, scene-cut detection and a dense burst around the first cuts.
usage: python watch_reference.py <youtube-url-or-id> <out-dir> [--every 15] [--height 480]
Requires yt-dlp (with node as JS runtime), ffmpeg. Outputs: <id>.txt (transcript), <id>.mp4, frames/, sheets/, cuts.txt, burst/.
Why frames: an analyst agent cannot watch video; it reads the transcript plus stills (sheets keep token cost down) and a burst
around a cut to describe how transitions move."""
import sys, subprocess, pathlib, re, argparse, glob

ap = argparse.ArgumentParser()
ap.add_argument("url"); ap.add_argument("out"); ap.add_argument("--every", type=float, default=15); ap.add_argument("--height", type=int, default=480)
a = ap.parse_args()
O = pathlib.Path(a.out).resolve(); O.mkdir(parents=True, exist_ok=True)
vid = re.search(r"(?:v=|youtu\.be/)([\w-]{11})", a.url); vid = vid.group(1) if vid else a.url
url = a.url if a.url.startswith("http") else f"https://www.youtube.com/watch?v={vid}"
run = lambda *c: subprocess.run(list(c), capture_output=True, text=True)

# 1) transcript (manual or auto subs; en-orig first)
run("yt-dlp", "--js-runtimes", "node", "--skip-download", "--write-sub", "--write-auto-sub", "--sub-lang", "en.*,en,en-orig,pt.*", "--sub-format", "vtt", "-o", str(O / f"{vid}.%(ext)s"), url)
vtts = sorted(O.glob(f"{vid}*.vtt"), key=lambda p: (0 if "orig" in p.name else 1, len(p.name)))
if vtts:
    lines, last = [], None
    for raw in vtts[0].read_text(encoding="utf-8", errors="ignore").splitlines():
        m = re.match(r"(\d\d):(\d\d):(\d\d)\.\d+ -->", raw)
        if m: ts = f"{int(m.group(1))*60+int(m.group(2)):02d}:{m.group(3)}"; continue
        t = re.sub(r"<[^>]+>", "", raw).strip()
        if not t or t.startswith(("WEBVTT", "Kind:", "Language:")) or t == last: continue
        last = t; lines.append(f"{ts} {t}")
    (O / f"{vid}.txt").write_text("\n".join(lines), encoding="utf-8"); print("transcript lines:", len(lines))
else:
    print("no subtitles found (try again later: YouTube rate-limits subtitle fetches)")
# 2) description
d = run("yt-dlp", "--js-runtimes", "node", "--skip-download", "--print", "%(title)s | %(channel)s | %(duration)s s\n%(description)s", url)
(O / f"{vid}.description.txt").write_text(d.stdout[:3000], encoding="utf-8")
# 3) low-res video
mp4 = O / f"{vid}.mp4"
if not mp4.exists():
    r = run("yt-dlp", "--js-runtimes", "node", "-f", f"bv*[height<={a.height}]+ba/b[height<={a.height}]", "--merge-output-format", "mp4", "-o", str(mp4), url)
    if not mp4.exists(): run("yt-dlp", "--js-runtimes", "node", "-f", "b[height<=360]", "-o", str(mp4), url)
print("video:", mp4.exists())
# 4) frames + sheets
F, S = O / "frames", O / "sheets"; F.mkdir(exist_ok=True); S.mkdir(exist_ok=True)
run("ffmpeg", "-v", "error", "-y", "-i", str(mp4), "-vf", f"fps=1/{a.every},scale=640:-1", str(F / "f_%03d.jpg"))
fr = sorted(F.glob("f_*.jpg"))
for i in range(0, len(fr) - 3, 4):
    run("ffmpeg", "-v", "error", "-y", "-i", str(fr[i]), "-i", str(fr[i+1]), "-i", str(fr[i+2]), "-i", str(fr[i+3]), "-filter_complex", "[0:v][1:v]hstack[a];[2:v][3:v]hstack[b];[a][b]vstack", str(S / f"sheet_{i//4:02d}.jpg"))
print("frames:", len(fr), "sheets:", len(list(S.glob('*.jpg'))))
# 5) cuts + burst around the first strong cut
c = run("ffmpeg", "-i", str(mp4), "-vf", "select='gt(scene,0.4)',showinfo", "-f", "null", "-")
cuts = [float(m) for m in re.findall(r"pts_time:([\d.]+)", c.stderr)]
(O / "cuts.txt").write_text("\n".join(f"{t:.2f}" for t in cuts), encoding="utf-8"); print("strong cuts at:", [round(t, 1) for t in cuts[:10]])
if cuts:
    B = O / "burst"; B.mkdir(exist_ok=True); t0 = max(0, cuts[0] - 0.6)
    run("ffmpeg", "-v", "error", "-y", "-ss", f"{t0:.2f}", "-t", "1.2", "-i", str(mp4), "-vf", "fps=10,scale=480:-1", str(B / "b_%02d.jpg"))
    print("burst frames:", len(list(B.glob('*.jpg'))))
