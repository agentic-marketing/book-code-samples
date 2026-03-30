# Kapitel 9 – Claude API Orchestrator (framework-agnostisch)

Vollständiges Beispiel eines Marketing-Orchestrators direkt mit der Anthropic Claude API —
ohne CrewAI oder LangGraph. Demonstriert natives Tool Use, Extended Thinking und Prompt Caching.

## Use Case

Churn-Analyse: Der Orchestrator identifiziert Kunden mit erhöhtem Abwanderungsrisiko,
analysiert das Segment und erstellt ein Kampagnen-Brief für das Content-Team.

## Setup

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env       # ANTHROPIC_API_KEY eintragen
```

## Starten

```bash
# Orchestrator + Unteragent
python orchestrator.py

# Nur Unteragent (Content-Writer)
python subagent.py
```

## Konzepte

| Konzept | Datei | Beschreibung |
|---|---|---|
| Tool Use | `orchestrator.py` | Werkzeugdefinition + Agentic Loop |
| Extended Thinking | `orchestrator.py` | Erweitertes Reasoning für strategische Entscheidungen |
| Prompt Caching | `orchestrator.py` | Stable Brand-Kontext wird gecacht (−90 % Input-Token-Kosten) |
| Multi-Modell | `subagent.py` | Worker-Modell für schnelle Ausführungsaufgaben |

## Wann dieser Ansatz sinnvoll ist

- Du willst volle Kontrolle über den Agentic Loop (kein Framework-Overhead)
- Extended Thinking und Prompt Caching sind für deinen Use Case ökonomisch entscheidend
- Du baust eine eigene Orchestrierungsschicht und integrierst Claude als Kernstück
- Anbieter-Unabhängigkeit ist ein Architekturprinzip

Details: Kapitel 9, Abschnitt „Claude (Anthropic): Der framework-agnostische Weg"
