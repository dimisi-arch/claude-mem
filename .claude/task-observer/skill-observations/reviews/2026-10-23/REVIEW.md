## Skill-Review 2026-10-23 (nachgeholt: der Lauf vom 19.10. blieb liegen)

### Erledigt
- #18, #21 → `install-third-party-skill` gestaged (Version pinnen, Größe als Grund fürs Nachladen, .rev-Prüfung, Sparse Checkout). Baut auf der Kopie vom 11.10. (#9) auf und ersetzt sie.
- #19 → `check-claude-setup.sh` prüft nachgeladene Fremd-Skills nur noch auf Vorhandensein. Lokaler Lauf wieder grün.
- #20 → feste Form für die Abschlussantwort im ADHS-Block von `.claude/hooks/session-start.sh`.
- #22 → geparkt (hyperframes ist fremd; nur eine Meldung an den Autor wäre möglich).

### Upstream-Updates gestaged (`skill-updates/2026-10-23/`, Bundle-Prüfung bestanden)
- task-observer 3.6.0 → 3.7.0 (68 Commits). #6, #7, #8 sind darin noch nicht gelöst und bleiben geparkt.
- ponytail, ponytail-debt, ponytail-gain, ponytail-help → 09c434a
- impeccable → 4901415 (30 Dateien)
- Weiter gültig vom 15.10.: agent-reach (#15), documentation-and-adrs, idea-refine, security-and-hardening

### Aktuell
agent-reach, i-have-adhd, watch, find-skills (Skill-Ordner gleich), niche-research (Ordner gleich), agent-skills (aeac41d, schon gestaged).

### Vorschläge, nicht geändert
- Start-Hooks: remotion 7ba4dcf → 6c67adc, hyperframes v0.8.159 → v0.8.186. Die Hooks laden dank `.rev` jetzt sauber neu.
- graphifyy 0.9.94: der Hook holt immer die neueste.

### Log
- Keine doppelten IDs, `.id-floor` = 23.

### Setup-Check
`bash .claude/scripts/check-claude-setup.sh` → OK

8 bundles staged, 8 bundles presented
