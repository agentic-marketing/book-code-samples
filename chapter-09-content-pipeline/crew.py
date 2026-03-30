"""
Crew-Definition: Alle Agenten und Tasks werden hier zusammengestellt.

Architektur: Supervisor (sequentiell)
- Profil-Analyst → Content-Stratege → E-Mail-Texter → Quality-Reviewer
- Jeder Agent bekommt nur die Informationen, die er für seine Aufgabe braucht
- Übergaben sind typisiert (siehe models/schemas.py)

LLM-Konfiguration: Standardmäßig OpenAI. Für Anthropic Claude:
    llm="claude-sonnet-4-6"  (erfordert ANTHROPIC_API_KEY in .env)
"""

from crewai import Agent, Task, Crew, Process
from crewai.project import CrewBase, agent, crew, task
from crewai.memory import LongTermMemory, ShortTermMemory
from crewai.memory.storage.rag_storage import RAGStorage
from tools.crm_tool import CRMTool
from dotenv import load_dotenv
import os

load_dotenv()

# Standard-LLM — austauschbar gegen "claude-sonnet-4-6" o.ä.
DEFAULT_LLM = os.getenv("LLM_MODEL", "gpt-4o-mini")


@CrewBase
class ContentPipelineCrew:
    """
    Automatisierte Content-Pipeline für personalisierte Trigger-E-Mails.
    Supervisor-Architektur mit klaren Übergaben und Qualitätskontrolle.
    """

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    # ── Agenten ────────────────────────────────────────────────────

    @agent
    def profil_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config["profil_analyst"],
            tools=[CRMTool()],   # Einziger Agent mit Tool-Zugriff
            llm=DEFAULT_LLM,
            max_iter=3,          # Verhindert endlose Schleifen
            verbose=False
        )

    @agent
    def content_stratege(self) -> Agent:
        return Agent(
            config=self.agents_config["content_stratege"],
            tools=[],            # Arbeitet rein kognitiv auf dem Kontext
            llm=DEFAULT_LLM,
            max_iter=3,
            verbose=False
        )

    @agent
    def content_writer(self) -> Agent:
        return Agent(
            config=self.agents_config["content_writer"],
            tools=[],
            llm=DEFAULT_LLM,
            max_iter=3,
            verbose=False
        )

    @agent
    def quality_reviewer(self) -> Agent:
        return Agent(
            config=self.agents_config["quality_reviewer"],
            tools=[],
            llm=DEFAULT_LLM,
            max_iter=2,          # Reviewer braucht weniger Iterationen
            verbose=False
        )

    # ── Tasks ──────────────────────────────────────────────────────

    @task
    def kundenprofil_erstellen(self) -> Task:
        return Task(
            config=self.tasks_config["kundenprofil_erstellen"],
            agent=self.profil_analyst()
        )

    @task
    def content_strategie_entwickeln(self) -> Task:
        return Task(
            config=self.tasks_config["content_strategie_entwickeln"],
            agent=self.content_stratege(),
            context=[self.kundenprofil_erstellen()]   # Abhängigkeit definieren
        )

    @task
    def e_mail_schreiben(self) -> Task:
        return Task(
            config=self.tasks_config["e_mail_schreiben"],
            agent=self.content_writer(),
            context=[
                self.kundenprofil_erstellen(),
                self.content_strategie_entwickeln()
            ]
        )

    @task
    def qualitaet_pruefen(self) -> Task:
        return Task(
            config=self.tasks_config["qualitaet_pruefen"],
            agent=self.quality_reviewer(),
            context=[
                self.kundenprofil_erstellen(),
                self.e_mail_schreiben()
            ]
        )

    # ── Crew ───────────────────────────────────────────────────────

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,   # Supervisor-Muster
            verbose=False,
            # Memory für produktive Umgebungen aktivieren:
            # memory=True,
            # long_term_memory=self._build_long_term_memory(),
        )

    def _build_long_term_memory(self) -> LongTermMemory:
        """
        Persistentes Gedächtnis für Kundenwissen über mehrere Sessions.
        Achtung: Personenbezogene Daten → DSGVO-Speicheranforderungen beachten!
        """
        return LongTermMemory(
            storage=RAGStorage(
                embedder_config={
                    "provider": "openai",
                    "config": {"model": "text-embedding-3-small"}
                },
                type="long_term",
                path="./memory/long_term/"
            )
        )
