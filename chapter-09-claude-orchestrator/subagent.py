"""
Content-Unteragent mit Worker-Modell.

Demonstriert die Multi-Modell-Strategie:
- Orchestrator (orchestrator.py): Leistungsstarkes Modell für Strategie und Planung
- Unteragent (diese Datei): Schnelles, kosteneffizientes Modell für Ausführungsaufgaben

Warum das ökonomisch relevant ist:
Bei 10.000 täglichen Kunden-Workflows können 95 % der Calls (Ausführung) über
das Worker-Modell laufen — das reduziert die Betriebskosten um Faktor 5–10
gegenüber einem System, das für alles das stärkste Modell einsetzt.
"""

import anthropic
import json
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic()
WORKER_MODEL = "claude-haiku-4-5-20251001"   # Schnell, kosteneffizient


def run_content_subagent(brief: dict) -> str:
    """
    Unteragent: Erstellt E-Mail-Betreffzeilen auf Basis eines Kampagnen-Briefs.
    Einfache Ausführungsaufgabe — kein Extended Thinking, kein Tool Use nötig.

    Args:
        brief: Kampagnen-Brief vom Orchestrator (dict mit campaign_objective, key_message, etc.)

    Returns:
        Drei Betreffzeilen-Vorschläge als Text.
    """
    response = client.messages.create(
        model=WORKER_MODEL,
        max_tokens=500,
        system=(
            "Du bist ein präziser E-Mail-Texter für B2B-SaaS. "
            "Kurz, klar, handlungsorientiert. Keine generischen Floskeln."
        ),
        messages=[
            {
                "role": "user",
                "content": (
                    f"Schreibe drei E-Mail-Betreffzeilen für folgendes Kampagnen-Brief:\n"
                    f"{json.dumps(brief, ensure_ascii=False, indent=2)}\n\n"
                    f"Anforderungen:\n"
                    f"- Max. 60 Zeichen pro Betreffzeile\n"
                    f"- Ton: empathisch, lösungsorientiert\n"
                    f"- Ziel: Öffnungsrate maximieren\n"
                    f"- Keine Spam-Trigger-Wörter ('kostenlos', 'jetzt sofort', etc.)"
                )
            }
        ]
    )
    return response.content[0].text


if __name__ == "__main__":
    # Beispiel-Brief (wie er vom Orchestrator übergeben würde)
    beispiel_brief = {
        "segment_id": "CHURN_RISK_70",
        "campaign_objective": "Churn-Prävention: Kunden mit hohem Abwanderungsrisiko reaktivieren",
        "key_message": "Wir haben gesehen, dass du weniger aktiv bist – gibt es etwas, wobei wir helfen können?",
        "channels": ["email"],
        "urgency": "high"
    }

    print("Generiere Betreffzeilen...\n")
    betreffzeilen = run_content_subagent(beispiel_brief)
    print("── Betreffzeilen-Vorschläge ──────────────────────")
    print(betreffzeilen)
