"""Scaffold a video project folder from the skill's assets.
usage: python new_project.py <project-dir> [--title "Page title"] [--subtitle "one line"]
Creates: src/ (engine parts, style.css, template.html), scenes/_template.js, assets/icons, audio/, qa/, dist/, export/
and a roteiro.json skeleton. Edit src/style.css tokens and src/template.html fonts/title to match the extracted style."""
import argparse, pathlib, shutil, json

SKILL = pathlib.Path(__file__).resolve().parent.parent
ap = argparse.ArgumentParser()
ap.add_argument("project"); ap.add_argument("--title", default="Untitled video"); ap.add_argument("--subtitle", default="")
a = ap.parse_args()
P = pathlib.Path(a.project).resolve()
for d in ["src", "scenes", "assets/icons", "audio", "qa", "dist", "export"]:
    (P / d).mkdir(parents=True, exist_ok=True)
A = SKILL / "assets"
for f in ["helpers.js", "helpers-motion.js", "player.js"]:
    shutil.copy(A / "engine" / f, P / "src" / f)
shutil.copy(A / "style.css", P / "src" / "style.css")
tpl = (A / "template.html").read_text(encoding="utf-8")
tpl = tpl.replace("<title>Claude Code with the Context Hub</title>", f"<title>{a.title}</title>")
(P / "src" / "template.html").write_text(tpl, encoding="utf-8")
shutil.copy(A / "scene-template.js", P / "scenes" / "_template.js")
for svg in (A / "icons").glob("*.svg"):
    shutil.copy(svg, P / "assets" / "icons" / svg.name)
shutil.copy(SKILL / "scripts" / "package.json", P / "export" / "package.json")
if not (P / "roteiro.json").exists():
    json.dump({"voice": "ash", "style": "calm, clear technical narrator", "lang": "en",
               "scenes": [{"id": "s01", "section": "", "title": "Opening", "style": "cold-open",
                           "lines": [["First narrated sentence.", "Primeira frase legendada."]],
                           "visual": "What the viewer sees, beat by beat.", "on_screen_text": ["one", "two"]}]},
              open(P / "roteiro.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("project ready at", P)
print("next: edit src/style.css tokens + src/template.html (title, fonts); write roteiro.json; run gen_tts.py; build.py --dev")
