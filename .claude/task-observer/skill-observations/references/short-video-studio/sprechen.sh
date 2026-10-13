#!/bin/bash
# Spricht jede Zeile von zeilen.txt einzeln ein (Piper, offline). Aussprache-Korrekturen in aussprache.sed
cd "$(dirname "$0")"; i=0
while IFS= read -r z; do i=$((i+1)); n=$(printf '%02d' $i)
  echo "$z" | sed -f aussprache.sed | uv tool run -q --from piper-tts piper -m de_thorsten.onnx -f z$n.wav --length-scale 1.08 --sentence-silence 0.35 2>/dev/null
done < zeilen.txt
