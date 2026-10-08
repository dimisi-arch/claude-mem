// Lernbeispiel: mehrere Agenten mit eigenen Rollen arbeiten nacheinander an einer Aufgabe.
// Start: npm install && npm start "Deine Aufgabe"
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic(); // liest ANTHROPIC_API_KEY aus der Umgebung

// Ein Agent = ein Name + eine Rolle (System-Prompt). Mehr braucht es nicht.
class Agent {
  constructor(
    public name: string,
    private rolle: string,
  ) {}

  async frage(auftrag: string): Promise<string> {
    const antwort = await client.beta.messages.create({
      model: "claude-opus-5-5",
      max_tokens: 16000,
      output_config: { effort: "medium" },
      // Lehnt das Modell aus Sicherheitsgründen ab, springt automatisch ein Ersatzmodell ein.
      betas: ["server-side-fallback-2026-07-01"],
      fallbacks: "default",
      system: this.rolle,
      messages: [{ role: "user", content: auftrag }],
    });

    if (antwort.stop_reason === "refusal") {
      throw new Error(`${this.name} hat die Aufgabe abgelehnt.`);
    }
    return antwort.content
      .filter((b): b is Anthropic.Beta.BetaTextBlock => b.type === "text")
      .map((b) => b.text)
      .join("\n");
  }
}

// Hier legst du deine Agenten an. Einfach weitere hinzufügen oder Rollen ändern.
const planer = new Agent(
  "Planer",
  "Du zerlegst eine Aufgabe in 3 bis 5 kurze, klare Schritte. Antworte nur mit der nummerierten Liste.",
);
const autor = new Agent(
  "Autor",
  "Du schreibst anhand eines Plans einen gut verständlichen Text auf Deutsch.",
);
const kritiker = new Agent(
  "Kritiker",
  "Du prüfst einen Text streng, aber fair. Nenne höchstens 3 konkrete Verbesserungen als Liste.",
);

// Der Ablauf: Planer -> Autor -> Kritiker -> Autor überarbeitet.
async function main() {
  const aufgabe = process.argv[2] ?? "Erkläre in einfachen Worten, wie eine Brotbäckerei am Morgen arbeitet.";
  console.log(`Aufgabe: ${aufgabe}\n`);

  const plan = await planer.frage(aufgabe);
  console.log(`--- ${planer.name} ---\n${plan}\n`);

  const entwurf = await autor.frage(`Aufgabe: ${aufgabe}\n\nPlan:\n${plan}`);
  console.log(`--- ${autor.name} (Entwurf) ---\n${entwurf}\n`);

  const kritik = await kritiker.frage(entwurf);
  console.log(`--- ${kritiker.name} ---\n${kritik}\n`);

  const endfassung = await autor.frage(
    `Überarbeite deinen Text anhand dieser Kritik.\n\nText:\n${entwurf}\n\nKritik:\n${kritik}`,
  );
  console.log(`--- ${autor.name} (Endfassung) ---\n${endfassung}`);
}

main().catch((fehler) => {
  if (fehler instanceof Anthropic.AuthenticationError) {
    console.error("API-Schlüssel fehlt oder ist falsch (ANTHROPIC_API_KEY).");
  } else if (fehler instanceof Anthropic.RateLimitError) {
    console.error("Zu viele Anfragen – bitte kurz warten und erneut starten.");
  } else {
    console.error(fehler instanceof Error ? fehler.message : fehler);
  }
  process.exit(1);
});
