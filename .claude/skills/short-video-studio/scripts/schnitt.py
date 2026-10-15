"""Cut the finished vertical video from the chosen scene images and the narration.

Run:  python schnitt.py PROJEKT_DIR [ausgabe.mp4]        (needs only ffmpeg/ffprobe)
Per scene: slow zoom in/out on the image (Ken Burns), vignette, the voice line at its start.
Subtitles: from the scene TEXT (never from a transcript, so voice slips never reach the screen),
3 words at a time, words from "akzent" highlighted, "anzeige" replaces words (dreizehn -> 13).
Sound: voice + optional tick bed, low drone, bell on scenes with "glocke": true, or a music file.
Writes ausgabe.mp4 (default PROJEKT_DIR/folge.mp4) and qa/frame_*.jpg for the final look check.
"""
import sys

sys.dont_write_bytecode = True  # keep the skill folder free of __pycache__
import argparse
import tempfile
from pathlib import Path

from gemeinsam import bildpfad, dauer, lade, sh, tonpfad

PAUSE = 0.45      # air after each line
SCHLUSS = 3.5     # end card seconds
SATZ = ".,:;?!"


def ts(x):
    return f"0:{int(x // 60):02d}:{x % 60:05.2f}"


def ass_text(t):
    return t.replace("{", "(").replace("}", ")").replace("\n", " ")


def untertitel(p, starts, laengen, pfad, W, H):
    akzent = {w.lower() for w in p["akzent"]}
    anzeige = {k.lower(): v for k, v in p["anzeige"].items()}
    kopf = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 0
[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Sub,DejaVu Sans,84,&H00FFFFFF,&H00FFFFFF,&H00000000,&H80000000,1,0,0,0,100,100,0,0,1,7,3,2,90,90,560,1
Style: Titel,DejaVu Sans,46,&H0000D7FF,&H00FFFFFF,&H00000000,&H80000000,1,0,0,0,100,100,4,0,1,4,2,8,60,60,170,1
Style: Tafel,DejaVu Sans,78,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,1,0,0,0,100,100,0,0,1,0,0,5,80,80,0,1
[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    ev, subs = [], []
    if p["kopfzeile"]:
        ende = starts[1] if len(starts) > 1 else starts[0] + laengen[0]
        ev.append(f"Dialogue: 0,{ts(0)},{ts(ende)},Titel,,0,0,0,,{ass_text(p['kopfzeile'])}\n")
    for s, a0, l in zip(p["szenen"], starts, laengen):
        woerter = s["text"].split()
        gew = [len(w) + 2 for w in woerter]
        ges = sum(gew)
        acc, zeiten = 0, []
        for g in gew:  # time each word in proportion to its length
            a = a0 + 0.15 + (l - PAUSE - 0.05) * acc / ges
            acc += g
            zeiten.append((a, a0 + 0.15 + (l - PAUSE - 0.05) * acc / ges))
        i = 0
        while i < len(woerter):
            gruppe = list(range(i, min(i + 3, len(woerter))))
            for k, j in enumerate(gruppe[:-1]):  # a punctuation mark ends the group
                if woerter[j][-1] in SATZ:
                    gruppe = gruppe[:k + 1]
                    break
            teile = []
            for j in gruppe:
                w = woerter[j]
                kern = w.strip(SATZ + "\"'„“»«").lower()
                zeichen = w[len(w.rstrip(SATZ)):]
                zeig = anzeige.get(kern, w.strip(SATZ + "\"'„“»«")) + ("" if zeichen in ("", ".") else zeichen)
                zeig = ass_text(zeig.upper())
                teile.append("{\\c&H00D7FF&}" + zeig + "{\\c&HFFFFFF&}" if kern in akzent else zeig)
            subs.append([zeiten[gruppe[0]][0], zeiten[gruppe[-1]][1] + 0.08, " ".join(teile)])
            i = gruppe[-1] + 1
    for k in range(len(subs) - 1):  # never two subtitles at once: libass would stack them
        subs[k][1] = min(subs[k][1], subs[k + 1][0] - 0.02)
    ev += [f"Dialogue: 0,{ts(a)},{ts(b)},Sub,,0,0,0,,{t}\n" for a, b, t in subs]
    if p["abspann"]:
        zeilen = [ass_text(z) for z in p["abspann"]]
        text = "\\N".join(zeilen[:-1] + ["{\\c&H00D7FF&}" + zeilen[-1]])
        e = starts[-1] + laengen[-1]
        ev.append(f"Dialogue: 0,{ts(e + 0.3)},{ts(e + SCHLUSS)},Tafel,,0,0,0,,{text}\n")
    Path(pfad).write_text(kopf + "".join(ev), encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("projekt")
    ap.add_argument("ausgabe", nargs="?")
    args = ap.parse_args()
    d, p = lade(args.projekt)
    W, H, FPS = p["format"]["breite"], p["format"]["hoehe"], p["format"]["fps"]
    ziel = Path(args.ausgabe) if args.ausgabe else d / "folge.mp4"
    fehlt = [str(f) for s in p["szenen"] for f in (bildpfad(d, s), tonpfad(d, s)) if not f.is_file()]
    if fehlt:
        raise SystemExit("Fehlt: " + ", ".join(fehlt))
    tmp = Path(tempfile.mkdtemp())
    starts, laengen, clips, t = [], [], [], 0.0
    for k, s in enumerate(p["szenen"]):
        dd = dauer(tonpfad(d, s)) + PAUSE
        starts.append(t)
        laengen.append(dd)
        t += dd
        n = int(dd * FPS) + 1
        z = f"1.0+0.10*on/{n}" if k % 2 == 0 else f"1.10-0.10*on/{n}"  # alternate zoom in / out
        x = "iw/2-(iw/zoom/2)" + ("" if k % 3 else f"+20*on/{n}")
        clip = tmp / f"c{k:02d}.mp4"
        sh("ffmpeg", "-v", "error", "-y", "-loop", "1", "-i", str(bildpfad(d, s)), "-vf",
           f"scale={W * 2}:{H * 2}:force_original_aspect_ratio=increase:flags=lanczos,crop={W * 2}:{H * 2},"
           f"zoompan=z='{z}':x='{x}':y='ih/2-(ih/zoom/2)':d={n}:s={W}x{H}:fps={FPS},vignette=PI/5,format=yuv420p",
           "-t", f"{dd:.3f}", "-c:v", "libx264", "-crf", "18", "-preset", "veryfast", str(clip))
        clips.append(clip)
    schluss = SCHLUSS if p["abspann"] else 0.8
    tafel = tmp / "tafel.mp4"
    sh("ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", f"color=c=black:s={W}x{H}:r={FPS}:d={schluss}",
       "-c:v", "libx264", "-crf", "18", "-preset", "veryfast", "-pix_fmt", "yuv420p", str(tafel))
    clips.append(tafel)
    gesamt = t + schluss
    (tmp / "liste.txt").write_text("".join(f"file '{c}'\n" for c in clips))
    sh("ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(tmp / "liste.txt"), "-c", "copy",
       str(tmp / "bild.mp4"))
    untertitel(p, starts, laengen, tmp / "sub.ass", W, H)

    eing, filt, mix = ["-i", str(tmp / "bild.mp4")], [], []
    for k, s in enumerate(p["szenen"]):
        eing += ["-i", str(tonpfad(d, s))]
        ms = int(starts[k] * 1000 + 150)
        filt.append(f"[{k + 1}:a]aresample=44100,aformat=channel_layouts=mono,adelay={ms}|{ms},volume=1.7[v{k}]")
        mix.append(f"[v{k}]")
    j = len(p["szenen"]) + 1
    ton = p["ton"]
    if ton.get("musik"):
        eing += ["-stream_loop", "-1", "-i", str(d / ton["musik"])]
        filt.append(f"[{j}:a]aresample=44100,volume=0.18,atrim=0:{gesamt:.2f}[mus]")
        mix.append("[mus]")
        j += 1
    if ton.get("ticken"):
        eing += ["-f", "lavfi", "-i", f"aevalsrc='0.22*sin(2*PI*2400*t)*exp(-120*mod(t,1))*lt(mod(t,1),0.04)':s=44100:d={gesamt}"]
        filt.append(f"[{j}:a]volume=0.6[tick]")
        mix.append("[tick]")
        j += 1
    if ton.get("drone"):
        eing += ["-f", "lavfi", "-i", f"aevalsrc='0.05*sin(2*PI*55*t)+0.03*sin(2*PI*82.5*t)':s=44100:d={gesamt}"]
        filt.append(f"[{j}:a]afade=t=in:d=2[drone]")
        mix.append("[drone]")
        j += 1
    glocke = "0.5*(sin(2*PI*392*t)+0.6*sin(2*PI*784*t)+0.3*sin(2*PI*1176*t))*exp(-2.2*t)"
    for k, s in enumerate(p["szenen"]):
        if s.get("glocke"):
            ms = int(starts[k] * 1000)
            eing += ["-f", "lavfi", "-i", f"aevalsrc='{glocke}':s=44100:d=2.5"]
            filt.append(f"[{j}:a]adelay={ms}|{ms},volume=0.8[g{k}]")
            mix.append(f"[g{k}]")
            j += 1
    filt.append(f"{''.join(mix)}amix=inputs={len(mix)}:duration=longest:normalize=0,alimiter=limit=0.95,"
                f"afade=t=out:st={gesamt - 1.2:.2f}:d=1.2[a]")
    sub = str(tmp / "sub.ass").replace("\\", "/").replace(":", "\\:")
    # Bitrate cap: grain or fine detail otherwise blows a 1-minute short up to >100 MB.
    sh("ffmpeg", "-v", "error", "-y", *eing, "-filter_complex",
       ";".join(filt) + f";[0:v]subtitles='{sub}',fade=t=in:d=0.5[v]",
       "-map", "[v]", "-map", "[a]", "-t", f"{gesamt:.2f}", "-c:v", "libx264", "-crf", "21", "-maxrate", "5M",
       "-bufsize", "10M", "-preset", "slow", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k",
       "-movflags", "+faststart", str(ziel))
    qa = d / "qa"
    qa.mkdir(exist_ok=True)
    for name, sek in (("anfang", 1.0), ("mitte", gesamt / 2), ("ende", max(0.5, gesamt - 1.5))):
        sh("ffmpeg", "-v", "error", "-y", "-ss", f"{sek:.2f}", "-i", str(ziel), "-frames:v", "1", "-q:v", "3",
           str(qa / f"frame_{name}.jpg"))
    mb = ziel.stat().st_size / 1e6
    print(f"fertig: {ziel} ({gesamt:.1f} s, {mb:.1f} MB); Kontrollbilder in {qa}")


if __name__ == "__main__":
    main()
