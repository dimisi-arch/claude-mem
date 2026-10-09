"""Build the faster dialogue voice track for Short 1 and a timeline for the renderer.

Narrator pieces are cut from the approved Elias take (voice.mp3) and sped up
with atempo (pitch kept). Character lines come from separate recordings.
Writes voice2.wav and timeline.json into the work dir.
"""
import json
import subprocess
import sys

D = sys.argv[1]
TEMPO = 1.15
LEAD = 0.25
PAD = 0.06

def run(*args):
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *args], check=True)

def dur(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "csv=p=0", path], capture_output=True, text=True, check=True)
    return float(out.stdout)

TRIM = ("silenceremove=start_periods=1:start_threshold=-42dB:start_silence=0.03,"
        "areverse,silenceremove=start_periods=1:start_threshold=-42dB:start_silence=0.05,areverse")
CAVE = "aecho=0.8:0.6:60|140:0.25|0.15"

def narrator(name, t0, t1, src="voice.mp3"):
    out = f"{D}/p_{name}.wav"
    run("-ss", str(max(0, t0 - PAD)), "-to", str(t1 + PAD), "-i", f"{D}/{src}",
        "-af", f"atempo={TEMPO}", "-ar", "48000", "-ac", "1", out)
    return out

def narrator_file(name, src):
    out = f"{D}/p_{name}.wav"
    run("-i", f"{D}/{src}", "-af", f"{TRIM},atempo={TEMPO}", "-ar", "48000", "-ac", "1", out)
    return out

def character(name, src, extra=""):
    out = f"{D}/p_{name}.wav"
    af = TRIM + (("," + extra) if extra else "")
    run("-i", f"{D}/{src}", "-af", af, "-ar", "48000", "-ac", "1", out)
    return out

def chorus(name):
    out = f"{D}/p_{name}.wav"
    pitch = "asetrate=48000*0.9,aresample=48000,atempo=1.11"
    run("-i", f"{D}/c_nb1.mp3", "-i", f"{D}/c_nb2.mp3", "-filter_complex",
        f"[0:a]{TRIM},{pitch}[a];[1:a]{TRIM},{pitch},adelay=70[b];"
        f"[a][b]amix=inputs=2:normalize=0,volume=0.8,{CAVE}",
        "-ar", "48000", "-ac", "1", out)
    return out

# (key, wav, gap after, subtitles as (relative share start, share end, text), speaker)
pieces = [
    ("ody1", character("ody1", "cand_malachi.mp3", "asetrate=48000*0.96,aresample=48000,atempo=1.0417,aecho=0.8:0.5:50:0.12"), 0.45,
     [(0, 1, "„Mein Name ist Niemand.“")], "Odysseus"),
    ("n1", narrator("n1", 4.05, 9.69), 0.25,
     [(0, 1, "Mit diesem einen Satz rettet Odysseus sich und seine Männer vor einem Riesen.")], "Erzähler"),
    ("n2", narrator("n2", 10.07, 17.44), 0.30,
     [(0, 0.52, "Der Zyklop Polyphem hat sie in seiner Höhle eingesperrt,"),
      (0.52, 1, "hinter einem Felsen, den kein Mensch bewegen kann.")], "Erzähler"),
    ("n3", narrator("n3", 18.22, 22.64), 0.25,
     [(0, 0.42, "Odysseus gibt ihm Wein,"), (0.42, 1, "und der Riese fragt nach seinem Namen.")], "Erzähler"),
    ("n4", narrator("n4", 23.38, 24.37), 0.15, [(0, 1, "Odysseus sagt:")], "Erzähler"),
    ("ody2", character("ody2", "c_ody2_malachi.mp3", "asetrate=48000*0.96,aresample=48000,atempo=1.0417,aecho=0.8:0.5:50:0.12"), 0.40,
     [(0, 1, "„Niemand.“")], "Odysseus"),
    ("n5", narrator("n5", 26.99, 31.80), 0.20,
     [(0, 0.53, "Als Polyphem später geblendet brüllt,"),
      (0.53, 1, "kommen seine Nachbarn und fragen:")], "Erzähler"),
    ("nb", chorus("nb"), 0.25, [(0, 1, "„Wer tut dir etwas an?“")], "Zyklopen"),
    ("n6", narrator("n6", 34.49, 35.43), 0.10, [(0, 1, "Und er ruft:")], "Erzähler"),
    ("poly", character("poly", "c_poly.mp3", "asetrate=48000*0.92,aresample=48000," + CAVE), 0.45,
     [(0, 1, "„Niemand!“")], "Polyphem"),
    ("n7", narrator("n7", 37.69, 44.52), 0.35,
     [(0, 0.55, "Die anderen Zyklopen denken, er sei krank, und gehen wieder."),
      (0.55, 1, "Eine List aus einem einzigen Wort.")], "Erzähler"),
    ("end1", narrator("end1", 0.0, 5.10, "end_elias.mp3"), 0.35,
     [(0, 0.64, "Doch der Felsen liegt noch immer vor dem Eingang."),
      (0.64, 1, "Wie kommen sie hier heraus?")], "Erzähler"),
    ("end2", narrator("end2", 8.41, 10.56, "end_elias.mp3"), 0.0,
     [(0, 1, "Abonniere Age of Geschichte.")], "Erzähler"),
]

# concat list with silences
sil = {}
def silence(sec):
    key = f"{sec:.2f}"
    if key not in sil:
        path = f"{D}/sil_{key}.wav"
        run("-f", "lavfi", "-i", "anullsrc=r=48000:cl=mono", "-t", key, path)
        sil[key] = path
    return sil[key]

timeline, files, t = [], [silence(LEAD)], LEAD
for key, wav, gap, subs, speaker in pieces:
    d = dur(wav)
    timeline.append({"key": key, "start": round(t, 3), "end": round(t + d, 3), "speaker": speaker,
                     "subs": [[round(t + a * d, 3), round(t + b * d, 3), text] for a, b, text in subs]})
    files.append(wav)
    t += d
    if gap:
        files.append(silence(gap))
        t += gap
total = round(t + 0.6, 3)
files.append(silence(0.6))

with open(f"{D}/concat.txt", "w") as f:
    for p in files:
        f.write(f"file '{p}'\n")
run("-f", "concat", "-safe", "0", "-i", f"{D}/concat.txt", "-ar", "48000", "-ac", "1", f"{D}/voice2.wav")
json.dump({"total": total, "pieces": timeline}, open(f"{D}/timeline.json", "w"), ensure_ascii=False, indent=1)
print("total", total)
for p in timeline:
    print(f"{p['start']:6.2f}-{p['end']:6.2f} {p['speaker']:9s} {p['subs'][0][2]}")
