"""
CRM-Tool für die Content-Pipeline.

In der Produktion: Ersetze die simulierten Daten in _run() durch einen
echten API-Call an dein CRM-System (Salesforce, HubSpot, Dynamics, etc.)
oder eine Datenbankabfrage.

Wichtig: Bevor Kundendaten an die LLM-API gesendet werden, DSGVO-konforme
Datenmaskierung einbauen. Nur Daten übermitteln, die für die Aufgabe
zwingend notwendig sind und für die ein AVV nach Art. 28 DSGVO besteht.
"""

from crewai.tools import BaseTool
from pydantic import BaseModel, Field
import json


class CustomerProfileInput(BaseModel):
    """Eingabe-Schema für das CRM-Tool."""
    customer_id: str = Field(
        description="Die eindeutige Kunden-ID aus dem CRM-System"
    )


class CRMTool(BaseTool):
    name: str = "CRM Kundenprofil-Tool"
    description: str = (
        "Ruft das vollständige Profil eines Kunden ab: demografische Daten, "
        "Nutzungsverhalten, Lifecycle-Status, Kommunikationspräferenzen. "
        "Benötigt eine Customer-ID."
    )
    args_schema: type[BaseModel] = CustomerProfileInput

    def _run(self, customer_id: str) -> str:
        """
        Simuliertes Kundenprofil – in Produktion durch echten CRM-API-Call ersetzen.

        Beispiel für einen echten HubSpot-API-Call:
            import requests
            response = requests.get(
                f"https://api.hubapi.com/contacts/v1/contact/vid/{customer_id}/profile",
                headers={"Authorization": f"Bearer {os.getenv('HUBSPOT_API_KEY')}"}
            )
            return json.dumps(response.json())
        """
        # Simuliertes Profil für Entwicklung und Testing
        profile = {
            "customer_id": customer_id,
            "customer_name": "Maria Schneider",
            "company": "TechMittelstand GmbH",
            "industry": "Fertigung",
            "company_size": "250 Mitarbeiter",
            "active_features": ["Reporting Dashboard", "Team Inbox"],
            "unused_features": ["Workflow Automation", "API Integration"],
            "lifecycle_stage": "aktiv_mit_expansionspotenzial",
            "last_login": "2026-03-18",
            "account_manager": "Thomas Berg",
            "communication_preferences": {
                "preferred_channel": "email",
                "preferred_time": "dienstags_oder_donnerstags",
                "language": "de"
            },
            "risk_signals": [],
            "notes": "Sehr engagiert mit Reporting, fragt regelmäßig nach Automation"
        }
        return json.dumps(profile, ensure_ascii=False, indent=2)
