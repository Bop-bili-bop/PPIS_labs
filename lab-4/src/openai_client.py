"""OpenAI Responses API for the assignment; credentials stay in the local .env."""
from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI, OpenAIError

ENV_FILE = Path(__file__).resolve().parents[1] / ".env"


class OpenAIConfigurationError(RuntimeError):
    """Missing credentials or model selection."""


def create_client() -> tuple[OpenAI, str]:
    load_dotenv(ENV_FILE)
    key = os.getenv("OPENAI_API_KEY", "").strip()
    model = os.getenv("OPENAI_MODEL", "").strip()
    if not key or not model:
        raise OpenAIConfigurationError(
            "Set OPENAI_API_KEY and OPENAI_MODEL in lab-4/.env or the environment."
        )
    return OpenAI(api_key=key, timeout=30.0, max_retries=1), model


def generate_text(prompt: str, *, client=None, model: str | None = None,
                  history: list[dict[str, str]] | None = None) -> str:
    """Generate text; append a completed turn only after a successful response."""
    if not prompt.strip():
        raise ValueError("Prompt must not be empty.")
    if client is None:
        client, model = create_client()
    if not model:
        raise ValueError("Model must not be empty.")
    messages = [*(history or []), {"role": "user", "content": prompt}]
    try:
        response = client.responses.create(model=model, input=messages, store=False)
    except OpenAIError as exc:
        # SDK messages may contain request details: do not print them or a key.
        raise RuntimeError(f"OpenAI request failed ({type(exc).__name__}).") from exc
    text = response.output_text
    if not text or not text.strip():
        raise RuntimeError("OpenAI returned an empty text response.")
    if history is not None:
        history.extend([messages[-1], {"role": "assistant", "content": text}])
    return text
