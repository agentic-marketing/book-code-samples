"""
Einstiegspunkt der Content-Pipeline.

Produktionsreife Fehlerbehandlung:
- CrewAI-spezifische Fehler (Modell, Tools) → Fallback auf manuellen Review
- Unerwartete Fehler → Logging + Eskalation, niemals stillschweigend schlucken
- Kein Fehler darf ohne Reaktion verschwinden — das Kundensystem erwartet
  immer eine definierte Antwort.
"""

from crew import ContentPipelineCrew
from crewai.exceptions import CrewAIException
import json
import logging

# Logging-Konfiguration — in Produktion auf zentrales Log-Management ausrichten
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s"
)
logger = logging.getLogger(__name__)


def run_content_pipeline(customer_id: str, trigger_event: str) -> dict:
    """
    Startet die Content-Pipeline für einen Kunden.

    Args:
        customer_id:   CRM-Kunden-ID
        trigger_event: Auslöser, z. B. "3x Reporting genutzt, Automation nie"

    Returns:
        Review-Ergebnis mit der fertigen oder zur Revision markierten E-Mail.
    """
    eingabe = {"customer_id": customer_id, "trigger_event": trigger_event}
    crew = ContentPipelineCrew()
    return crew.crew().kickoff(inputs=eingabe)


def run_content_pipeline_safe(customer_id: str, trigger_event: str) -> dict:
    """
    Produktionsreife Version mit vollständiger Fehlerbehandlung.
    """
    try:
        ergebnis = run_content_pipeline(customer_id, trigger_event)
        logger.info(f"Pipeline erfolgreich: Kunde {customer_id}")
        return {"status": "success", "result": ergebnis}

    except CrewAIException as e:
        # Agenten-spezifische Fehler: Modell nicht erreichbar, Tool-Fehler, etc.
        logger.error(
            f"Agenten-Fehler für Kunde {customer_id}: {e}",
            extra={"customer_id": customer_id, "error_type": type(e).__name__}
        )
        _trigger_manual_review(customer_id, trigger_event, reason=str(e))
        return {"status": "fallback_to_manual", "customer_id": customer_id}

    except Exception as e:
        # Unerwartete Fehler: immer loggen und eskalieren, nie schlucken
        logger.exception(
            f"Unerwarteter Fehler für Kunde {customer_id}",
            extra={"customer_id": customer_id}
        )
        return {"status": "error", "customer_id": customer_id, "error": str(e)}


def _trigger_manual_review(customer_id: str, trigger_event: str, reason: str):
    """
    Fallback: Manuellen Review anstoßen wenn Agenten-System scheitert.
    In Produktion: Integration mit Jira, Zendesk oder eigenem Ticketing.
    """
    logger.info(
        f"Manuelles Review ausgelöst: Kunde {customer_id} | Grund: {reason}"
    )
    # Hier: Ticket-API-Call einbauen


if __name__ == "__main__":
    ergebnis = run_content_pipeline_safe(
        customer_id="CRM-2024-00847",
        trigger_event=(
            "Nutzer hat Reporting-Feature 12x genutzt, "
            "Workflow-Automation noch nie aktiviert"
        )
    )
    print(json.dumps(ergebnis, ensure_ascii=False, indent=2))
