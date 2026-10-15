"""Shared helpers for the short-video-studio scripts: project file, paths, shell calls."""
import json
import subprocess
import sys
from pathlib import Path

STANDARD = {
    "format": {"breite": 1080, "hoehe": 1920, "fps": 30},
    "stil": "",
    "stimme": {
        "engine": "auto",                 # auto | fish | edge | piper
        "fish_voice": "",                 # Fish Audio voice model id (reference_id)
        "fish_model": "s2.1-pro-free",    # Fish Audio model header
        "edge_voice": "de-DE-ConradNeural",
        "edge_rate": "-6%",
        "edge_pitch": "-5Hz",
        "piper_voice": "de_DE-thorsten-high",
        "tempo": 1.0,                     # 1.0 = normal; Piper length-scale is 1/tempo
    },
    "aussprache": {},                     # word -> respelling, for the voice only
    "anzeige": {},                        # word -> how the subtitle shows it ("dreizehn" -> "13")
    "akzent": [],                         # words highlighted in the subtitles
    "ton": {"ticken": False, "drone": True, "musik": ""},
    "kopfzeile": "",                      # small title line during the first scene
    "abspann": [],                        # end card lines; the last one is highlighted
    "szenen": [],
}


def lade(projekt_dir):
    """Read projekt.json from a project folder and fill in the defaults."""
    d = Path(projekt_dir)
    p = d / "projekt.json"
    if not p.is_file():
        sys.exit(f"Keine projekt.json in {d} (Vorlage: examples/projekt.json im Skill)")
    daten = json.loads(p.read_text(encoding="utf-8"))
    for k, v in STANDARD.items():
        if isinstance(v, dict):
            daten[k] = {**v, **daten.get(k, {})}
        else:
            daten.setdefault(k, v)
    if not daten["szenen"]:
        sys.exit("projekt.json hat keine Szenen")
    for i, s in enumerate(daten["szenen"], 1):
        s.setdefault("nr", i)
        for feld in ("bild", "text"):
            if not s.get(feld):
                sys.exit(f"Szene {s['nr']}: Feld '{feld}' fehlt")
    return d, daten


def nr2(n):
    return f"{int(n):02d}"


def bildpfad(d, s):
    """The chosen image of a scene: 'datei' if set, else bilder/szeneNN_v<variante>.png."""
    if s.get("datei"):
        return d / s["datei"]
    return d / "bilder" / f"szene{nr2(s['nr'])}_v{s.get('variante', 1)}.png"


def tonpfad(d, s):
    return d / "ton" / f"z{nr2(s['nr'])}.wav"


def sh(*a, **kw):
    # -nostdin matters inside loops: without it ffmpeg eats the loop's input.
    a = list(a)
    if a and a[0] == "ffmpeg" and "-nostdin" not in a:
        a.insert(1, "-nostdin")
    return subprocess.run(a, check=True, **kw)


def dauer(f):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(f)],
                         capture_output=True, text=True, check=True).stdout
    return float(out)


def auswahl(daten, nur):
    nur = {int(x) for x in (nur or [])}
    return [s for s in daten["szenen"] if not nur or int(s["nr"]) in nur]
