"""
Marketing-Orchestrator direkt mit der Claude API.

Demonstriert:
- Natives Tool Use: Werkzeuge als JSON-Schema, Claude entscheidet Reihenfolge
- Extended Thinking: Erweitertes Reasoning-Budget für strategische Entscheidungen
- Prompt Caching: Stabiler Brand-Kontext wird gecacht (bis zu 90 % weniger Kosten
  für gecachte Input-Token bei Produktions-Workflows mit tausenden täglichen Calls)
- Agentic Loop: Tool-Call → Ergebnis verarbeiten → nächster Call → Abschluss

Use Case: Churn-Segment identifizieren → analysieren → Kampagnen-Brief erstellen
"""

import anthropic
import json
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic()

# Modell-Konstanten — sprechende Namen statt Versionsnummern
ORCHESTRATOR_MODEL = "claude-opus-4-6"          # Strategisches Reasoning
WORKER_MODEL = "claude-haiku-4-5-20251001"       # Schnelle Ausführungsaufgaben


# ── Tool-Definitionen ──────────────────────────────────────────────────────────
# Tools sind das Herzstück nativer Claude-Agenten.
# Claude entscheidet selbst, welche Tools wann in welcher Reihenfolge aufzurufen sind.

TOOLS = [
    {
        "name": "get_churn_risk_segment",
        "description": (
            "Ruft Kunden mit erhöhtem Churn-Risiko aus dem CDP ab. "
            "Gibt Segment-ID, Größe und Propensity-Score-Verteilung zurück."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "risk_threshold": {
                    "type": "number",
                    "description": "Minimaler Churn-Propensity-Score (0.0–1.0)"
                },
                "max_customers": {
                    "type": "integer",
                    "description": "Maximale Anzahl zurückgegebener Kunden"
                }
            },
            "required": ["risk_threshold"]
        }
    },
    {
        "name": "create_campaign_brief",
        "description": "Erstellt ein strukturiertes Kampagnen-Brief für das Content-Team.",
        "input_schema": {
            "type": "object",
            "properties": {
                "segment_id": {"type": "string"},
                "campaign_objective": {"type": "string"},
                "key_message": {"type": "string"},
                "channels": {
                    "type": "array",
                    "items": {"type": "string"}
                },
                "urgency": {
                    "type": "string",
                    "enum": ["low", "medium", "high"]
                }
            },
            "required": ["segment_id", "campaign_objective", "key_message", "channels"]
        }
    }
]

# ── Tool-Implementierungen ─────────────────────────────────────────────────────
# In Produktion: Echte CDP/CRM-API-Calls statt simulierter Daten

def get_churn_risk_segment(risk_threshold: float, max_customers: int = 1000) -> dict:
    """Simulierter CDP-API-Call — in Produktion durch echte Segment-Abfrage ersetzen."""
    return {
        "segment_id": f"CHURN_RISK_{int(risk_threshold * 100)}",
        "size": 847,
        "avg_propensity_score": 0.73,
        "top_churn_reasons": ["Preis", "fehlende Features", "schlechter Support"],
        "avg_contract_value": 2400,
        "preferred_channel": "email"
    }


def create_campaign_brief(
    segment_id: str,
    campaign_objective: str,
    key_message: str,
    channels: list,
    urgency: str = "medium"
) -> dict:
    """Erstellt und speichert ein Kampagnen-Brief."""
    brief = {
        "brief_id": f"BRIEF_{segment_id}_{urgency.upper()}",
        "segment_id": segment_id,
        "campaign_objective": campaign_objective,
        "key_message": key_message,
        "channels": channels,
        "urgency": urgency,
        "status": "created",
        "next_step": "Content-Team informieren"
    }
    # In Produktion: Brief in CMS oder Projektmanagement-Tool speichern
    return brief


def execute_tool(tool_name: str, tool_input: dict) -> str:
    """Tool-Dispatcher: Name → Implementierung."""
    if tool_name == "get_churn_risk_segment":
        result = get_churn_risk_segment(**tool_input)
    elif tool_name == "create_campaign_brief":
        result = create_campaign_brief(**tool_input)
    else:
        result = {"error": f"Unbekanntes Tool: {tool_name}"}
    return json.dumps(result, ensure_ascii=False)


# ── System-Prompt mit Prompt Caching ──────────────────────────────────────────
# Stabiler Brand-Kontext wird gecacht: API berechnet Input-Token für gecachte
# Blöcke nur beim ersten Call vollständig; Folge-Calls kosten ~10 % davon.

SYSTEM_PROMPT_BLOCKS = [
    {
        "type": "text",
        "text": (
            "Du bist ein Senior Marketing-Orchestrator für ein B2B-SaaS-Unternehmen. "
            "Du analysierst Kundendaten, identifizierst Handlungsbedarf und koordinierst "
            "Kampagnen — datengetrieben, compliance-bewusst und auf messbaren ROI ausgerichtet."
        ),
        "cache_control": {"type": "ephemeral"}   # Dieser Block wird gecacht
    },
    {
        "type": "text",
        "text": (
            "Brand-Guidelines: Ton professionell aber zugänglich. "
            "Keine Versprechen, die wir nicht halten können. "
            "Datenschutz-First: Keine personenbezogenen Rohdaten in Analysen."
        ),
        "cache_control": {"type": "ephemeral"}   # Auch dieser stabile Block wird gecacht
    }
]


# ── Agentic Loop ───────────────────────────────────────────────────────────────

def run_churn_campaign_orchestrator() -> str:
    """
    Orchestrator-Workflow: Tool-Aufruf → Ergebnis → weiterer Tool-Aufruf → Abschluss.

    Extended Thinking aktiviert zusätzliches Reasoning-Budget:
    Das Modell denkt sichtbar nach, bevor es antwortet — besonders wertvoll
    für komplexe Abwägungen (Segment-Auswahl, Kanal-Mix, Dringlichkeit).
    """
    messages = [
        {
            "role": "user",
            "content": (
                "Analysiere unser Churn-Risiko und erstelle einen Aktionsplan. "
                "Fokus auf Kunden mit hohem Risiko (>0.7 Propensity-Score). "
                "Empfehle die wichtigste Maßnahme mit konkretem Brief."
            )
        }
    ]

    # Erster API-Call mit Extended Thinking
    response = client.messages.create(
        model=ORCHESTRATOR_MODEL,
        max_tokens=8000,
        thinking={
            "type": "enabled",
            "budget_tokens": 3000   # Reasoning-Budget; höher = gründlicher, langsamer
        },
        system=SYSTEM_PROMPT_BLOCKS,
        tools=TOOLS,
        messages=messages
    )

    # Agentic Loop: Solange Claude Tools aufruft, führen wir sie aus und antworten
    while response.stop_reason == "tool_use":
        # Tool-Ergebnisse sammeln
        tool_results = []
        for block in response.content:
            if block.type == "tool_use":
                result = execute_tool(block.name, block.input)
                print(f"  → Tool: {block.name} | Input: {block.input}")
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": result
                })

        # Konversation mit Tool-Ergebnissen fortsetzen
        messages.append({"role": "assistant", "content": response.content})
        messages.append({"role": "user", "content": tool_results})

        # Nächster API-Call (ohne Extended Thinking — nur für den ersten Call nötig)
        response = client.messages.create(
            model=ORCHESTRATOR_MODEL,
            max_tokens=4000,
            system=SYSTEM_PROMPT_BLOCKS,
            tools=TOOLS,
            messages=messages
        )

    # Finales Text-Ergebnis extrahieren
    for block in response.content:
        if hasattr(block, "text"):
            return block.text

    return "Kein Ergebnis erhalten."


if __name__ == "__main__":
    print("Starte Churn-Campaign-Orchestrator...\n")
    result = run_churn_campaign_orchestrator()
    print("\n── Orchestrator-Ergebnis ──────────────────────────")
    print(result)
