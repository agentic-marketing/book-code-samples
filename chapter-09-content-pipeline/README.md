# Kapitel 9 – Vollständige CrewAI Content-Pipeline

Automatisierte Content-Pipeline für personalisierte E-Mails mit CrewAI.
Supervisor-Architektur: 4 spezialisierte Agenten in sequentiellem Workflow.

## Use Case

Trigger-Event (z. B. Nutzer hat Feature X dreimal genutzt, nie Feature Y aktiviert)
→ Pipeline erstellt personalisierten E-Mail-Content, abgestimmt auf das Kundenprofil.

## Setup

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env       # API-Key eintragen
```

## Starten

```bash
python main.py
```

## Dateistruktur

```
chapter-09-content-pipeline/
├── config/
│   ├── agents.yaml          # Agenten-Definitionen (Rolle, Ziel, Backstory)
│   └── tasks.yaml           # Task-Definitionen mit Abhängigkeiten
├── tools/
│   ├── __init__.py
│   └── crm_tool.py          # CRM-Tool (simuliertes Kundenprofil)
├── models/
│   ├── __init__.py
│   └── schemas.py           # Pydantic-Schemata für typisierte Übergaben
├── crew.py                  # Crew-Definition: Agenten + Tasks zusammenstellen
├── main.py                  # Einstiegspunkt + Fehlerbehandlung
├── requirements.txt
└── .env.example
```

## Anpassen für den Produktionseinsatz

1. `tools/crm_tool.py`: Simuliertes Profil durch echten CRM-API-Call ersetzen
2. `models/schemas.py`: Schemata an dein Datenmodell anpassen
3. `main.py`: Logging-Konfiguration auf deine Infrastruktur ausrichten
4. PII-Datenmaskierung vor LLM-Calls einbauen (Abschnitt 9.5 im Buch)
5. AVV mit LLM-Anbieter abschließen (Abschnitt 9.3 im Buch)
