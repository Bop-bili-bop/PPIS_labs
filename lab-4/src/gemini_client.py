"""Невеликий клієнт Google Gemini для лабораторної роботи №4."""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai

DEFAULT_MODEL = "gemini-2.5-flash"
ENV_FILE = Path(__file__).resolve().parents[1] / ".env"


class GeminiConfigurationError(RuntimeError):
    """Raised when credentials needed by Gemini are not configured."""


def load_settings() -> tuple[str, str]:
    """Load the API key and model from lab-4/.env or the environment."""
    load_dotenv(ENV_FILE)
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    model = os.getenv("GEMINI_MODEL", DEFAULT_MODEL).strip() or DEFAULT_MODEL
    if not api_key:
        raise GeminiConfigurationError(
            "Gemini API key is not configured. Copy .env.example to .env "
            "and set GEMINI_API_KEY."
        )
    return api_key, model


def create_client() -> tuple[genai.Client, str]:
    """Create an official Google Gen AI client and return it with model name."""
    api_key, model = load_settings()
    return genai.Client(api_key=api_key), model


def generate_text(prompt: str) -> str:
    """Generate one textual answer with Gemini.

    Network and service errors are converted to a clear RuntimeError so a CLI
    caller can report them without exposing credentials or a traceback.
    """
    if not prompt.strip():
        raise ValueError("Prompt must not be empty.")

    client, model = create_client()
    try:
        response = client.models.generate_content(model=model, contents=prompt)
    except Exception as exc:  # SDK exceptions vary by transport/status code.
        raise RuntimeError(f"Gemini request failed: {exc}") from exc

    text = response.text
    if not text:
        raise RuntimeError("Gemini returned an empty text response.")
    return text
