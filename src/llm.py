import os
from dotenv import load_dotenv
from crewai import LLM

load_dotenv()


def get_secret(key: str) -> str:
    """Get a secret from Streamlit Cloud secrets or fallback to env vars."""
    try:
        import streamlit as st
        return st.secrets.get(key, os.getenv(key, ""))
    except Exception:
        return os.getenv(key, "")


def get_llm() -> LLM:
    """Create and return a Grok-2 LLM instance via xAI's OpenAI-compatible API."""
    return LLM(
        model="grok-2-latest",
        base_url="https://api.x.ai/v1",
        api_key=get_secret("XAI_API_KEY"),
        temperature=0.7,
        max_tokens=4096,
    )
