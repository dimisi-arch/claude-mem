# Age of Geschichte – Shorts in Remotion

YouTube-Shorts der Serie „Die Odyssee“, gebaut mit [Remotion](https://www.remotion.dev)
(Videos aus React-Code). Regeln für Stimmen, Look und Aufbau: Notion, Seite
„Geschichtskanal: Kanal-Zentrale“, Abschnitt „Serien-Bibel“.

## Auf dem eigenen PC starten

Voraussetzung: Node.js (ab Version 20). Im Terminal in diesem Ordner:

```bash
npm install
npx remotion studio                      # Vorschau im Browser, alles live ansehen
npx remotion render Odyssee-Teil1 out/teil1.mp4 --crf=16
```

Mit Grafikkarte geht das Rendern schneller, zum Beispiel mit `--gl=angle` unter Windows.

## Aufbau

- `src/style.ts` – Farben, Schriften (Cinzel, Montserrat, GFS Didot), Zufallszahlen mit festem Startwert
- `src/components/` – Bausteine für jede Folge:
  - `KenBurns` – langsamer Zoom oder Schwenk über ein Bild, Überblendung
  - `Captions` – Wort-für-Wort-Untertitel, Schlüsselwort in Gold, Name der Figur über ihrer Zeile
  - `Cards` – animierte Titelkarte, Abspann mit „TEIL n FOLGT“ und Abonnieren-Knopf, Serien-Plakette oben
  - `Atmosphere` – Feuerflackern, aufsteigende Glut, Vignette
- `src/teil1/Teil1.tsx` – Szenenfolge von Teil 1 (welches Bild wann, Zoom, Wackeln bei Felsen und Schrei)
- `src/teil1/captions.json` – Wortzeiten, erzeugt mit `tools/captions.py`
- `public/teil1/` – Bilder (2-fach hochskaliert) und fertig gemischter Ton (`ton.m4a`, -14 LUFS)
- `public/fonts/` – Schriften mit ihren OFL-Lizenzen

## Neuer Teil

1. Bilder nach `public/teilN/`, Tonspur bauen (siehe `.claude/context/youtube-shorts/assemble.py`)
2. `python3 tools/captions.py voice.wav timeline.json src/teilN/captions.json` (mit Grafikkarte: `--device cuda`)
3. `src/teil1/Teil1.tsx` als Vorlage kopieren, Szenen anpassen, in `src/Root.tsx` eintragen
4. Rendern, Stichproben ansehen, für den Versand unter 30 MB: `ffmpeg … -b:v 4600k` (zwei Durchgänge)

Lizenz Remotion: kostenlos für Einzelpersonen und Firmen bis 3 Personen
([remotion.dev/license](https://www.remotion.dev/docs/license/faq)).
