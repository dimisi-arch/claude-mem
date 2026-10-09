# Agenten-Demo (Lernbeispiel)

Ein kleines Programm, in dem mehrere **Agenten** mit eigenen Rollen
zusammenarbeiten:

1. **Planer** zerlegt die Aufgabe in Schritte.
2. **Autor** schreibt danach einen Text.
3. **Kritiker** nennt Verbesserungen.
4. **Autor** überarbeitet den Text.

Ein Agent ist hier nur ein Name plus eine Rollenbeschreibung (`new Agent(...)`
in `agenten.ts`). Neue Agenten legst du genauso an.

## Starten (auf deinem Computer)

Voraussetzung: Node.js und ein Anthropic-API-Schlüssel
(https://console.anthropic.com — jede Ausführung kostet etwas).

```bash
cd examples/agenten-demo
npm install
export ANTHROPIC_API_KEY="dein-schlüssel"     # Windows PowerShell: $env:ANTHROPIC_API_KEY="dein-schlüssel"
npm start "Schreibe eine kurze Anleitung zum Kaffeekochen"
```

Ohne Aufgabe nimmt das Programm ein Beispiel.

## Hinweise

- Modell: `claude-opus-5-5`. Lehnt es eine Anfrage aus Sicherheitsgründen ab,
  springt automatisch ein Ersatzmodell ein (`fallbacks: "default"`).
- Ein Durchlauf macht 4 Anfragen, also 4 Mal Kosten.
