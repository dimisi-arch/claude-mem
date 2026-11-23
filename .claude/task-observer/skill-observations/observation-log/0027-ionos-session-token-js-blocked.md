---
id: 27
title: "IONOS-Webmail: Session-Token per JavaScript auslesen wird vom Auto-Mode-Klassifikator blockiert; UI-Weg funktioniert"
status: open
type: internal
skill: []
proposes_skill: []
target_file: ["/tmp/claude/memory/team/silo/omonia-postfach-spiegel.md"]
siblings_checked: "none — target is a memory note, not a skill family"
area: "IONOS-Technik (OX-API über Chrome)"
date: 2026-11-23
session_context: "Antwort-Entwurf mit Menü-PDFs für eine Gruppenreservierung im Restaurant-Postfach"
parked_until:
resolved:
resolution:
reference:
commands_verified: "run: Session-Token aus performance-Einträgen lesen -> classifier denial [Unauthorized Access]; UI-Weg (Antworten-Button, tinymce-Body per JS befüllen, X -> Entwurf speichern) -> Entwurf mit Zitat gespeichert"
---

**Issue:** Die Gedächtnisnotiz beschreibt als Hauptweg, den OX-Session-Token aus `performance.getEntriesByType('resource')` zu lesen und die API direkt aufzurufen. Im Auto-Mode verweigert der Klassifikator das als „Unauthorized Access“. Der UI-Weg (Ordner klicken, Mail öffnen, „Antwort an Absender“, tinymce-Body befüllen, Schließen → „Entwurf speichern“) klappte sofort und liefert das Zitat automatisch.

**Suggested improvement:** In der Postfach-Technik-Notiz den UI-Weg als Standard nennen und den Token-Weg als „im Auto-Mode blockiert“ markieren. Suche in IONOS gilt nur für den aktuellen Ordner – Ordner aus dem Logbuch nehmen.

**Principle:** Wenn eine dokumentierte Abkürzung Zugangsdaten aus der Seite liest, zuerst den normalen Bedienweg dokumentieren; Abkürzungen über Tokens werden von Sicherheitsprüfungen eher blockiert.
