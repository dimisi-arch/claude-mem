## Wöchentliche Skill-Review abgeschlossen — 2026-10-15 (geplanter Lauf, Routine „Skill-Verbesserung (Mo + Do)“)

Aktualisierte Skills (1 Beobachtung angewendet, 7 Upstream-Updates), alle unter
`skill-updates/2026-10-15/`, je als Ordner und `.skill`, Bundle-Prüfung bestanden.
Nichts installiert.

**agent-reach** — im lokalen Notizblock: was ohne vidIQ-Guthaben bei TikTok/Reels
nicht geht (Sackgassen, nie Captchas umgehen) und der funktionierende Weg für
YouTube Shorts; mit Herkunftsangabe (einmal beobachtet, 13.10., Cloud). Beobachtung #15.

**ponytail-debt, ponytail-gain, ponytail** — Upstream 9cc65d0 → 84740e3 (bei
ponytail nur SOURCE.md). Ersetzt die Kopien aus dem ungemergten PR #34.
**documentation-and-adrs, idea-refine, security-and-hardening** — Upstream
agent-skills 1401c8b → aeac41d (idea-refine neu in dieser Runde). Ersetzt die
Kopien vom 11.10.
**impeccable** — Upstream d631a88 → a231cc5: 4 Referenzdateien; Version 4.5.2 und
Engine 0.1.14 unverändert. Ersetzt die Kopie aus PR #34.

### Observations Actioned
- #15 — Short-Form-Recherche ohne vidIQ → gestaged (agent-reach).

### Log integrity
- **Doppelte ID 13**: `0013-edge-tts-403-voice-message-fails.md` (08:03 Uhr am 13.10.,
  mit ID-Reservierung) behält die 13; `0013-edge-tts-403-no-fallback.md` (10:36 Uhr,
  ohne Reservierung geschrieben — der Schreiber hat das Skript umgangen) wurde zu
  **#17** umnummeriert und als `superseded` durch #13 markiert (gleicher Befund).
- #14 existiert in keinem Zweig auf main (Lücke, vermutlich auf einem ungemergten Branch).
- `.id-floor` = 17. Hinweis: die Step-1-Liste wurde in diesem Lauf nicht neu
  geschrieben; Abgleich von Hand: am Anfang 9 Dateien, am Ende 9 (0013-no-fallback → 0017).

### Parked
- #3 — Session Start per Hand — wartet auf Upstream (Schritte 1 und 3).

### Bereits in PR #29 bearbeitet (nicht gemergt)
- #6, #7, #8 (Rückmeldungen an den Autor) und #10 (Skill voice-summary). Bitte PR #29 mergen.

### Skipped — deine Entscheidung nötig
1. **#13 Sprachnachricht in der Cloud (edge-tts 403):** Soll `vorlesen.py` eine zweite,
   kostenlose Stimme bekommen, die ohne Internet läuft (Piper, deutsche Stimme
   „thorsten“ — in #16 schon erfolgreich getestet)? Achtung: PR #28 und #30 ändern
   dasselbe Skript und sind noch offen.
2. **#16 neuer Skill „short-video-studio“:** Die Produktionskette für Kurzvideos (Bild,
   Stimme, Untertitel, Schnitt) als Skill einfrieren? Neue Skills legt die Review nicht
   selbst an. PR #44 ergänzt die Beobachtung noch.

### Arrived during this run
- none (nur die Umnummerierung #17)

### Upstream- und Neu-Skill-Prüfung
| Skill | lokal | upstream | Ergebnis |
|---|---|---|---|
| ponytail* | 9cc65d0 | 84740e3 | 3 Ordner gestaged |
| agent-skills (7) | 1401c8b | aeac41d | 3 Skills geändert → gestaged; 4 unverändert |
| impeccable | d631a88 | a231cc5 | gestaged |
| claude-automation-recommender | b8e53f1 | c2bdb42 | Skill-Ordner unverändert |
| agent-reach, find-skills, watch, i-have-adhd | — | gleich | aktuell |
| task-observer | 56e8907 | 56e8907 | aktuell |
| remotion (REV im Hook) | 32b241b (4.0.534) | 7ba4dcf (4.0.535) | Vorschlag wie am 13.10.: REV anheben |
| hyperframes (REV im Hook) | v0.8.151 | v0.8.159 (f35b05f) | Vorschlag: vor dem Anheben die Skill-Ordner vergleichen |
| graphify (PyPI) | ungepinnt | 0.9.91 | Hook holt die neueste |

Neue Skills in github.com/anthropics/skills: keine (HEAD dbd4588). discernment-nudge
weiter empfohlen.

### Aufräumen (deine Entscheidung)
- PR #34 (Review vom 13.10.) ist durch diese Review überholt und kann geschlossen werden.

### Setup-Check
- `bash .claude/scripts/check-claude-setup.sh` → OK

8 bundles staged, 8 bundles presented
