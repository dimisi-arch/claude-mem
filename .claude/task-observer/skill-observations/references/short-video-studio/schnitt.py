"""Schneidet eine Folge aus Szenenbildern und Sprachzeilen zu einem fertigen Hochformat-Video.

Aufruf: python schnitt.py auswahl.json ausgabe.mp4
auswahl.json: [{"nr": 1, "bild": "roh/szene01_v2.png", "glocke": false}, ...]
Ton: ton/zNN.wav pro Szene, Text: ton/zeilen.txt (eine Zeile pro Szene).
"""
import json, subprocess, sys, tempfile
from pathlib import Path

W, H, FPS = 1080, 1920, 30
PAUSE = 0.45            # Luft nach jedem Satz
SCHLUSS = 3.5           # Dauer der Schluss-Tafel
SCHLUESSEL = {"dreizehn", "dreizehnmal", "verboten", "werkstatt", "1906", "köpenick", "uniform", "schuster",
              "zuchthaus", "rathaus", "gehorchten", "quittung", "viertausendzwei", "warnen", "grauer", "mich", "uhr"}
ERSETZE = {"dreizehn": "13", "dreizehnmal": "13-mal", "neunzehnhundertsechs": "1906", "sechzehnter": "16.",
           "siebenundfünfzig": "57", "viertausendzwei": "4.002"}

def sh(*a): subprocess.run(a, check=True)
def dauer(f): return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f],
                                          capture_output=True, text=True).stdout)
def ts(x): return f"0:{int(x // 60):02d}:{x % 60:05.2f}"

def untertitel(zeilen, starts, laengen, pfad):
    kopf = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Sub,DejaVu Sans,84,&H00FFFFFF,&H00FFFFFF,&H00000000,&H80000000,1,0,0,0,100,100,0,0,1,7,3,2,90,90,560,1
Style: Titel,DejaVu Sans,46,&H0000D7FF,&H00FFFFFF,&H00000000,&H80000000,1,0,0,0,100,100,4,0,1,4,2,8,60,60,170,1
Style: Tafel,DejaVu Sans,78,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,1,0,0,0,100,100,0,0,1,0,0,5,80,80,0,1
[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    subs = []
    ev = [f"Dialogue: 0,{ts(0)},{ts(starts[1] if len(starts) > 1 else 4)},Titel,,0,0,0,,DIE 13. STUNDE · FOLGE 1\n"]
    for z, s, l in zip(zeilen, starts, laengen):
        woerter = z.split()
        gew = [len(w) + 2 for w in woerter]; ges = sum(gew); acc = 0; zeiten = []
        for g in gew:
            a = s + 0.15 + (l - 0.5) * acc / ges; acc += g; zeiten.append((a, s + 0.15 + (l - 0.5) * acc / ges))
        i = 0
        while i < len(woerter):
            n = 3
            gruppe = list(range(i, min(i + n, len(woerter))))
            # nach Satzzeichen neue Gruppe beginnen
            for k, j in enumerate(gruppe[:-1]):
                if woerter[j][-1] in ".,:?!": gruppe = gruppe[:k + 1]; break
            teile = []
            for j in gruppe:
                w = woerter[j]; kern = w.strip(".,:?!").lower(); satz = w[len(w.rstrip(".,:?!")):]
                anzeige = ERSETZE.get(kern, w.strip(".,:?!")) + (satz if satz not in "." else "")
                anzeige = anzeige.upper()
                teile.append("{\\c&H00D7FF&}" + anzeige + "{\\c&HFFFFFF&}" if kern in SCHLUESSEL else anzeige)
            subs.append([zeiten[gruppe[0]][0], zeiten[gruppe[-1]][1] + 0.08, ' '.join(teile)])
            i = gruppe[-1] + 1
    for k in range(len(subs) - 1):          # nie zwei Untertitel gleichzeitig (sonst stapelt sie der Renderer)
        subs[k][1] = min(subs[k][1], subs[k + 1][0] - 0.02)
    ev += [f"Dialogue: 0,{ts(a)},{ts(b)},Sub,,0,0,0,,{t}\n" for a, b, t in subs]
    ende = starts[-1] + laengen[-1]
    ev.append(f"Dialogue: 0,{ts(ende + 0.3)},{ts(ende + SCHLUSS)},Tafel,,0,0,0,,FOLGE 2\\N{{\\c&H00D7FF&}}STRASSBURG 1518\n")
    Path(pfad).write_text(kopf + "".join(ev))

def main():
    auswahl = json.load(open(sys.argv[1])); ziel = sys.argv[2]
    zeilen = Path("ton/zeilen.txt").read_text().splitlines()
    tmp = Path(tempfile.mkdtemp())
    starts, laengen, clips = [], [], []
    t = 0.0
    for k, s in enumerate(auswahl):
        wav = f"ton/z{s['nr']:02d}.wav"; d = dauer(wav) + PAUSE
        starts.append(t); laengen.append(d); t += d
        n = int(d * FPS) + 1
        rein = k % 2 == 0      # abwechselnd hinein- und herauszoomen
        z = f"1.0+0.10*on/{n}" if rein else f"1.10-0.10*on/{n}"
        x = "iw/2-(iw/zoom/2)" + ("" if k % 3 else f"+{20}*on/{n}")
        clip = tmp / f"c{k:02d}.mp4"
        sh("ffmpeg", "-v", "error", "-y", "-loop", "1", "-i", s["bild"], "-vf",
           f"scale={W*2}:{H*2}:flags=lanczos,zoompan=z='{z}':x='{x}':y='ih/2-(ih/zoom/2)':d={n}:s={W}x{H}:fps={FPS},"
           f"vignette=PI/5,format=yuv420p", "-t", f"{d:.3f}", "-c:v", "libx264", "-crf", "18", "-preset", "veryfast", str(clip))
        clips.append(clip)
    # Schluss-Tafel: schwarz
    tafel = tmp / "tafel.mp4"
    sh("ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", f"color=c=black:s={W}x{H}:r={FPS}:d={SCHLUSS}",
       "-c:v", "libx264", "-crf", "18", "-preset", "veryfast", "-pix_fmt", "yuv420p", str(tafel))
    clips.append(tafel)
    gesamt = t + SCHLUSS
    (tmp / "liste.txt").write_text("".join(f"file '{c}'\n" for c in clips))
    sh("ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(tmp / "liste.txt"), "-c", "copy", str(tmp / "bild.mp4"))
    untertitel(zeilen[:len(auswahl)], starts, laengen, tmp / "sub.ass")

    # Ton: Stimme pro Szene an ihrer Startzeit, Ticken als Bett, Glockenschlag bei markierten Szenen
    eing = ["-i", str(tmp / "bild.mp4")]; filt = []; mix = []
    for k, s in enumerate(auswahl):
        eing += ["-i", f"ton/z{s['nr']:02d}.wav"]
        filt.append(f"[{k+1}:a]aresample=44100,adelay={int(starts[k]*1000+150)}|{int(starts[k]*1000+150)},volume=1.7[v{k}]"); mix.append(f"[v{k}]")
    m = len(auswahl) + 1
    eing += ["-f", "lavfi", "-i", f"aevalsrc='0.22*sin(2*PI*2400*t)*exp(-120*mod(t,1))*lt(mod(t,1),0.04)':s=44100:d={gesamt}"]
    filt.append(f"[{m}:a]volume=0.6[tick]"); mix.append("[tick]")
    eing += ["-f", "lavfi", "-i", f"aevalsrc='0.05*sin(2*PI*55*t)+0.03*sin(2*PI*82.5*t)':s=44100:d={gesamt}"]
    filt.append(f"[{m+1}:a]afade=t=in:d=2,volume=1[drone]"); mix.append("[drone]")
    glocke = "0.5*(sin(2*PI*392*t)+0.6*sin(2*PI*784*t)+0.3*sin(2*PI*1176*t))*exp(-2.2*t)"
    j = m + 2
    for k, s in enumerate(auswahl):
        if s.get("glocke"):
            eing += ["-f", "lavfi", "-i", f"aevalsrc='{glocke}':s=44100:d=2.5"]
            filt.append(f"[{j}:a]adelay={int(starts[k]*1000)}|{int(starts[k]*1000)},volume=0.8[g{k}]"); mix.append(f"[g{k}]"); j += 1
    filt.append(f"{''.join(mix)}amix=inputs={len(mix)}:duration=longest:normalize=0,alimiter=limit=0.95,afade=t=out:st={gesamt-1.2:.2f}:d=1.2[a]")
    sh("ffmpeg", "-v", "error", "-y", *eing, "-filter_complex",
       ";".join(filt) + f";[0:v]subtitles={tmp/'sub.ass'},fade=t=in:d=0.5[v]",
       "-map", "[v]", "-map", "[a]", "-t", f"{gesamt:.2f}", "-c:v", "libx264", "-crf", "22", "-preset", "slow",
       "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", ziel)
    print(f"fertig: {ziel} ({gesamt:.1f} s)")

if __name__ == "__main__":
    main()
