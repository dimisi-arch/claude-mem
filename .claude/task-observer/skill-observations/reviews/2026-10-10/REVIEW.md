## Wöchentliche Skill-Review abgeschlossen — 2026-10-10 (geplanter Lauf, Testauslösung)

Aktualisierte Skills (1 Beobachtung, 0 Prinzipien angewendet, 1 Upstream-Update):

**make-scenario-building** — Schritt 5 (Connections) prüft jetzt, ob die
Verbindung ein neues oder außerhalb von Make angelegtes Ziel (z. B. eine
Notion-Datenbank) überhaupt sieht, bevor gebaut wird; Beobachtung #4.
Gestaged unter `skill-updates/2026-10-10/make-scenario-building/` (nur
SKILL.md geändert, +5 Zeilen). Die Aussage ist mit Herkunft formuliert
("einmal beobachtet, bei Notion"), weil sie heute nicht live geprüft wurde.

**task-observer** — Upstream-Update 3.5.0 → 3.6.0 (Commit 56e8907, CC BY 4.0),
unverändert übernommen; die lokale Kopie hatte keine eigenen Änderungen.
Neu u. a. `scripts/session-start-scan.sh` (Schritt-2-Scan als ein Befehl).
Gestaged unter `skill-updates/2026-10-10/task-observer/` und als
`task-observer.skill`; Bundle-Prüfung bestanden.

### Observations Actioned
- #4 — Make-Verbindung sieht neue Notion-Datenbank erst nach Freigabe → gestaged.

### Family coherence
- #4 nennt nur make-scenario-building; Geschwister reference/explore/operations
  wurden beim Erfassen begründet ausgeschlossen. Keine skill-families.md.
- 0 Beobachtungen ohne Geschwister-Prüfung.

### Published skills
- keine (dieses Repo veröffentlicht keine Skills)

### Parked
- #3 — Session Start Protocol per Hand statt mit den mitgelieferten Befehlen —
  Bedingung teilweise erfüllt: Upstream 3.6.0 liefert ein Scan-Skript für
  Schritt 2. Neue Bedingung: entparkt, sobald das gestagte task-observer 3.6.0
  installiert ist; dann prüfen, ob Schritte 1 und 3 noch einen Ein-Befehl-Weg brauchen.
  Zweiter Fall in diesem Lauf (Scan wieder per Hand) → nächste Lösung muss
  strukturell sein: nach Installation das Skript im Routine-Prompt/Hook als einzigen Weg nennen.

### Arrived during this run
- #6 — Bundle-Prüfung meldet Makes `{{now}}`-Syntax als "Edit-Rest" — in diesem
  Lauf selbst erfasst, zielt auf task-observer; bleibt OPEN für die nächste
  Review (das gestagte Upstream-Update behebt es nicht).

### Log integrity
- keine doppelten IDs, `.id-floor` = 6 (stimmt), alle Header konform.
- #2 und #5 (erledigt am 2026-10-09) wurden regulär ins Archiv verschoben.

### Aktivierung (Schritt 1)
- Neu seit 2026-10-09: Session-Start-Hook `.claude/hooks/session-start.sh`
  (nennt Skill-Aufruf und Workspace, nicht den Probe-im-ersten-Batch).
- Neu: Routine "Wöchentliche Skill-Verbesserung". Ihr Prompt wiederholt
  Verfahrensdetails, die in den Skill gehören: die Liste der Status-Werte
  (Schritt 3) und Liefer-Regeln (Schritt 6). Vorschlag: diese Zeilen aus dem
  Routine-Prompt streichen — der Skill selbst legt sie fest, eine Kopie im
  Prompt veraltet unbemerkt.

### Upstream- und Neu-Skill-Prüfung
| Skill | lokal | upstream | Ergebnis |
|---|---|---|---|
| 7 agent-skills (addyosmani) | 1401c8b | 1401c8b | aktuell |
| ponytail* | 9cc65d0 | 9cc65d0 | aktuell |
| frontend-design | — | anthropics/skills HEAD dbd4588 | Inhalt identisch |
| remotion-best-practices (REV im Hook) | 32b241b | 32b241b | aktuell |
| graphify (PyPI graphifyy) | 0.9.82 in diesem Container | 0.9.83 | Hook installiert ungepinnt → holt beim nächsten frischen Start 0.9.83; nichts zu tun |
| task-observer | 3.5.0 | 3.6.0 | **gestaged** (siehe oben) |
| make-scenario-* | 0.2.0 (offizielles Make-Plugin) | nicht automatisch prüfbar (Plugin-Verzeichnis, kein Git-Repo) | in einer Sitzung mit Plugin-Zugang prüfen |

Neue Skills in github.com/anthropics/skills, die zu deiner Arbeit passen
(nur Vorschlag, nichts installiert; alle Apache 2.0 → dürfen ins Repo kopiert werden):
- **discernment-nudge** — hängt nach einem Entwurf (z. B. Gäste-E-Mail, Angebot)
  2–3 gezielte Rückfragen an, die Schwachstellen im Entwurf aufdecken. Passt zu
  deinem Wunsch nach unaufgeforderten Verbesserungsvorschlägen. **Empfehlung.**
- **academy-guide** — empfiehlt passende Claude-Academy-Kurse bei
  "Wie mache ich …"-Fragen zu Claude. Optional, eher für den Einstieg.
- webapp-testing — Playwright-Tests für Web-Apps; nicht nötig (Playwright-MCP vorhanden).
- docx/pdf/pptx/xlsx etc. sind bereits über das anthropic-skills-Plugin verfügbar.

### Setup-Check
- `bash .claude/scripts/check-claude-setup.sh` → OK: skills, hooks, settings and session notes

### Skipped (needs manual review)
- make-scenario-building wurde nicht als `.skill` gepackt: die Bundle-Prüfung
  schlägt bei `{{now}}` in drei Beispiel-JSONs fehl (Fehlalarm, #6). Packen
  von Hand ist nicht erlaubt; geliefert wird das gestagte Verzeichnis.

2 bundles staged, 2 bundles presented (1 als .skill, 1 als Verzeichnis — siehe Skipped)
