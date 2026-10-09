# Age of Geschichte: Short pipeline

Tools used to cut the YouTube Shorts in the cloud container. The rules for
voices, look and structure live in Notion (page "Geschichtskanal:
Kanal-Zentrale", section "Serien-Bibel"); these scripts implement them.

- `cards.py` - title card ("DIE ODYSSEE · TEIL n") and end card ("TEIL n+1 FOLGT").
- `assemble.py` - builds the dialogue voice track: narrator Elias cut from a
  take and sped up 15 % (atempo), character lines (Odysseus = Malachi,
  Polyphem = Monster, Cyclopes chorus = Ragnar + Grungle) trimmed, pitched and
  given cave echo; writes `voice2.wav` and `timeline.json` (piece times and
  subtitle splits). The `pieces` list is episode-specific: edit it per part.
- `render.py` - renders 1080x1920 frames from `timeline.json`: Ken Burns
  zoom/pan per shot, crossfades, vignette, burned-in German subtitles with the
  keyword in gold and the speaker name above character lines. The `SEGMENTS`
  list (which image when, start/end focus and zoom) is episode-specific.

Finish (from Short 1):

    ffmpeg -i voice2.wav -stream_loop -1 -i atmo.mp3 [-i sfx.mp3 ...] -filter_complex \
      "...amix...,loudnorm=I=-14:TP=-1.5:LRA=11" mix.m4a
    python3 render.py <workdir> video.mp4
    ffmpeg -i video.mp4 -c:v libx264 -preset slow -b:v 4600k -maxrate 6M -bufsize 9M -pass 1 ...
    ffmpeg -i video.mp4 -i mix.m4a ... -pass 2 ... Short.mp4   # ~26 MB, under the 30 MB send limit

Subtitle timing comes from `ffmpeg -af silencedetect=noise=-35dB:d=0.25` on
the narrator take. Always extract frames at every shot change and check them
before delivering. Needs Pillow and numpy (`pip install numpy` if missing).
