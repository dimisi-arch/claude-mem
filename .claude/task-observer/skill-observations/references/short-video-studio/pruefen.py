import sys, subprocess, numpy as np, glob
from faster_whisper import WhisperModel
m = WhisperModel("small", device="cpu", compute_type="int8", cpu_threads=2)
zeilen = open("zeilen.txt").read().splitlines()
for i, f in enumerate(sorted(glob.glob("z*.wav"))):
    a = np.frombuffer(subprocess.run(["ffmpeg","-v","error","-i",f,"-ac","1","-ar","16000","-f","s16le","-"],capture_output=True).stdout,np.int16).astype(np.float32)/32768
    hyp = " ".join(s.text.strip() for s in m.transcribe(a, language="de")[0])
    print(f"{f}: {hyp}\n   soll: {zeilen[i]}")
