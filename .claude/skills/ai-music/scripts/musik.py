#!/usr/bin/env python3
"""Generate background music with ACE-Step 1.5 via the acemusic.ai cloud API.

Standard library only. The API key comes from the environment variable ACEMUSIC_API_KEY
or, on the PC, from the file ~/.config/acemusic/key (one line). Never pass it as an argument.

  python musik.py "calm ancient greek lyre, mysterious, slow" out.mp3 --sekunden 60
  python musik.py "..." out.mp3 --varianten 3      # out_1.mp3 .. out_3.mp3

Request format adapted from digitalsamba/claude-code-video-toolkit (tools/music_gen.py, MIT).
"""
import argparse
import base64
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

API_URL = "https://api.acemusic.ai/v1/chat/completions"
MODEL = "acemusic/acestep-v1.5-xl-turbo"


def api_key():
    key = os.environ.get("ACEMUSIC_API_KEY", "").strip()
    datei = Path.home() / ".config" / "acemusic" / "key"
    if not key and datei.exists():
        key = datei.read_text(encoding="utf-8").strip()
    return key


def main():
    ap = argparse.ArgumentParser(description="Musik mit ACE-Step (acemusic.ai) erzeugen")
    ap.add_argument("prompt", help="Stil auf Englisch, z. B. 'epic orchestral, ancient greek, slow build'")
    ap.add_argument("ausgabe", help="Zieldatei, .mp3")
    ap.add_argument("--sekunden", type=int, default=60, help="Länge in Sekunden (Standard 60)")
    ap.add_argument("--varianten", type=int, default=1, help="1 bis 4 Versionen auf einmal")
    ap.add_argument("--bpm", type=int)
    ap.add_argument("--tonart", help="z. B. 'D minor'")
    ap.add_argument("--mit-gesang", action="store_true", help="Standard ist instrumental")
    ap.add_argument("--seed", type=int)
    a = ap.parse_args()

    key = api_key()
    if not key:
        sys.exit("FEHLT: ACEMUSIC_API_KEY. Kostenloser Schlüssel: https://acemusic.ai/api-key "
                 "(Cloud: in den Umgebungs-Einstellungen eintragen; PC: in ~/.config/acemusic/key).")

    audio = {"duration": a.sekunden, "format": "mp3", "vocal_language": "en"}
    if a.bpm:
        audio["bpm"] = a.bpm
    if a.tonart:
        audio["key_scale"] = a.tonart
    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": f"<prompt>{a.prompt}</prompt>"}],
        "stream": False,
        "thinking": True,
        "instrumental": not a.mit_gesang,
        "audio_config": audio,
    }
    if a.varianten > 1:
        payload["batch_size"] = max(1, min(a.varianten, 4))
    if a.seed is not None:
        payload["seed"] = a.seed

    req = urllib.request.Request(
        API_URL, data=json.dumps(payload).encode(), method="POST",
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {key}",
                 # Cloudflare in front of the API rejects Python's default user agent (error 1010)
                 "User-Agent": "age-of-geschichte-music/1.0"})
    print(f"Sende an acemusic.ai ({a.sekunden} s, {a.varianten} Variante(n)) … das dauert 1-3 Minuten",
          file=sys.stderr)
    start = time.time()
    try:
        with urllib.request.urlopen(req, timeout=900) as r:
            antwort = json.load(r)
    except urllib.error.HTTPError as e:
        text = e.read().decode(errors="replace")[:300]
        hinweis = " (Schlüssel falsch oder abgelaufen)" if e.code in (401, 403) else ""
        sys.exit(f"FEHLER: acemusic.ai antwortet HTTP {e.code}{hinweis}: {text}")
    except (urllib.error.URLError, TimeoutError) as e:
        sys.exit(f"FEHLER: acemusic.ai nicht erreichbar: {e}")

    nachricht = (antwort.get("choices") or [{}])[0].get("message", {})
    dateien = []
    ziel = Path(a.ausgabe)
    ziel.parent.mkdir(parents=True, exist_ok=True)
    for i, eintrag in enumerate(nachricht.get("audio") or [], 1):
        url = eintrag.get("audio_url", {}).get("url", "")
        if not url.startswith("data:audio"):
            continue
        datei = ziel if a.varianten <= 1 else ziel.with_name(f"{ziel.stem}_{i}{ziel.suffix}")
        datei.write_bytes(base64.b64decode(url.split(",", 1)[1]))
        dateien.append(datei)
    if not dateien:
        sys.exit(f"FEHLER: keine Musik in der Antwort. {str(nachricht.get('content', ''))[:300]}")
    for d in dateien:
        print(d)
    print(f"Fertig in {time.time() - start:.0f} s", file=sys.stderr)


if __name__ == "__main__":
    main()
