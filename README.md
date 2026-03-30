# Agentic Marketing – Code-Beispiele

Dieses Repository enthält die vollständigen, ausführbaren Code-Beispiele zum Buch
**„Agentic Marketing: Wie Multi-Agenten-Systeme das Marketing neu erfinden"**
von Florian Stompe.

## Warum dieses Repository?

Im Buch selbst stehen nur kurze Code-Fragmente, die das jeweilige Konzept illustrieren.
Vollständige, lauffähige Implementierungen findest du hier – mit ausführlichen Kommentaren,
`requirements.txt` und Anleitungen zum lokalen Start.

## Struktur

| Verzeichnis | Kapitel | Beschreibung |
|---|---|---|
| `chapter-09-content-pipeline/` | Kap. 9 | Vollständiger CrewAI-Workflow: personalisierte E-Mail-Pipeline mit 4 Agenten |
| `chapter-09-claude-orchestrator/` | Kap. 9 | Claude-API-Orchestrator direkt: Churn-Analyse mit Tool Use und Extended Thinking |

## Voraussetzungen

- Python 3.11+
- API-Keys für OpenAI oder Anthropic (je nach Beispiel), in `.env` gesetzt

## Hinweis

Die Beispiele sind Ausgangspunkte, keine produktionsreifen Systeme. Für den Produktionseinsatz
sind zusätzliche Maßnahmen erforderlich: Fehlerbehandlung, DSGVO-konforme Datenhaltung,
Audit-Logging, Secrets-Management. Kapitel 9, Abschnitte 9.4 und 9.5 beschreiben diese
Anforderungen im Detail.
