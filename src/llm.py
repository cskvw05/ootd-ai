import os
from dotenv import load_dotenv
from crewai import LLM

load_dotenv()


def get_llm() -> LLM:
    """Create and return a Grok-2 LLM instance via xAI's OpenAI-compatible API."""
    return LLM(
        model="grok-2-latest",
        base_url="https://api.x.ai/v1",
        api_key=os.getenv("XAI_API_KEY"),
        temperature=0.7,
        max_tokens=4096,
    )
