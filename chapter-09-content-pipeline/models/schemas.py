"""
Pydantic-Schemata für typisierte Übergaben zwischen den Agenten.

Warum typisierte Übergaben?
Ohne Schema kann Agent A Freitext zurückgeben, den Agent B nicht
zuverlässig parsen kann. Mit Schema erzwingen wir exakte Felder
und Datentypen – das macht das System stabil und debuggbar.
"""

from pydantic import BaseModel, Field
from typing import Literal, List, Optional


class CustomerProfile(BaseModel):
    """Ausgabe des Profil-Analysten."""
    customer_name: str
    company: str
    industry: str
    active_features: List[str]
    unused_features: List[str] = []
    lifecycle_stage: Literal[
        "onboarding",
        "aktiv_mit_expansionspotenzial",
        "aktiv_stabil",
        "risiko",
        "inaktiv"
    ]
    risk_signals: List[str] = []
    communication_preferences: dict
    recommended_tone: Literal["professionell", "warm_persönlich", "enthusiastisch"]
    account_manager: Optional[str] = None


class ContentStrategy(BaseModel):
    """Ausgabe des Content-Strategen."""
    core_message: str = Field(description="Kernbotschaft, max. 1 Satz")
    emotional_anchor: str = Field(description="Adressiertes Bedürfnis oder Problem")
    proof_point: str = Field(description="Warum das Angebot für diesen Kunden relevant ist")
    call_to_action: str = Field(description="Gewünschte Handlung des Kunden")
    tone: Literal["professionell", "warm_persönlich", "enthusiastisch"]


class EmailDraft(BaseModel):
    """Ausgabe des E-Mail-Texters."""
    subject_line: str = Field(description="40-60 Zeichen, personalisiert")
    preview_text: str = Field(description="80-100 Zeichen, ergänzt Subject Line")
    salutation: str
    body_paragraphs: List[str] = Field(description="Max. 3 kurze Absätze")
    cta_text: str
    cta_url_placeholder: str
    signature: str


class ReviewResult(BaseModel):
    """Ausgabe des Quality Reviewers."""
    status: Literal["approved", "needs_revision"]
    issues: List[str] = []
    suggestions: List[str] = []
    final_email: Optional[EmailDraft] = None
