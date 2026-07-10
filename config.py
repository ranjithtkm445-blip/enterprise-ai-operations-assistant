import os

import litellm
from dotenv import load_dotenv

load_dotenv()

# CrewAI 1.15 injects `cache_breakpoint` into messages for Anthropic prompt
# caching. Groq rejects that key. Patch it out before anything else imports it.
import crewai.llms.cache as _cache  # noqa: E402
_cache.mark_cache_breakpoint = lambda msg: msg  # type: ignore[assignment]

from crewai import LLM  # noqa: E402

litellm.drop_params = True

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "groq/llama-3.3-70b-versatile")

if not GROQ_API_KEY:
    raise RuntimeError(
        "GROQ_API_KEY is not set. Copy .env.example to .env and add your Groq API key."
    )


def get_llm() -> LLM:
    return LLM(model=GROQ_MODEL, api_key=GROQ_API_KEY, temperature=0.3)
