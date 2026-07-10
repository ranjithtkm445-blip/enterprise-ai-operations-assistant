import os
import sys

from crewai import Crew, Process, Task

from backend.agents.definitions import build_agents
from backend.config import get_llm
from backend.db.database import init_db

# Windows console can't render the emoji CrewAI prints in verbose mode
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")


def run_query(user_message: str) -> str:
    init_db()
    agents = build_agents()
    manager_llm = get_llm()

    task = Task(
        description=(
            f'Handle the following business request end-to-end:\n\n"{user_message}"\n\n'
            "Rules:\n"
            "1. Delegate ONLY to agents whose specialty is needed. Do NOT call an agent "
            "unless the request explicitly requires their domain.\n"
            "2. Each specialist MUST use their tool to get real data — no guessing numbers.\n"
            "3. Present the tool output EXACTLY as returned — do not rephrase or summarise "
            "figures. If a quotation was generated, show it line-by-line.\n"
            "4. Keep the final response SHORT and STRUCTURED: use headers, bullet points, "
            "and the raw tool output. No legal disclaimers, payment term inventions, or "
            "filler paragraphs."
        ),
        expected_output=(
            "A short, structured response with clear sections. "
            "Stock check result and quotation figures must be copied verbatim from the tools — "
            "not paraphrased. No invented payment terms or policy filler."
        ),
        agent=None,
    )

    crew = Crew(
        agents=agents,
        tasks=[task],
        process=Process.hierarchical,
        manager_llm=manager_llm,
        verbose=True,
    )

    result = crew.kickoff()
    return str(result)
