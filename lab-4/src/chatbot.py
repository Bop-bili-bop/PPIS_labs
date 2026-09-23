"""Консольний чат-бот на основі Google Gemini."""

from __future__ import annotations

try:
    from .gemini_client import GeminiConfigurationError, create_client
except ImportError:  # Allows: python src/chatbot.py
    from gemini_client import GeminiConfigurationError, create_client


def main() -> int:
    print("Gemini chatbot")
    print("Type 'exit' or 'quit' to finish.")

    try:
        client, model = create_client()
        chat = client.chats.create(model=model)
    except GeminiConfigurationError as exc:
        print(exc)
        return 1
    except Exception as exc:
        print(f"Could not initialize Gemini: {exc}")
        return 1

    while True:
        try:
            message = input("\nYou: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            return 0

        if message.lower() in {"exit", "quit"}:
            print("Goodbye!")
            return 0
        if not message:
            print("Please enter a message.")
            continue

        try:
            response = chat.send_message(message)
            print(f"Gemini: {response.text or '[empty response]'}")
        except Exception as exc:
            print(f"Gemini request failed: {exc}")
            print("You can retry or type 'exit'.")


if __name__ == "__main__":
    raise SystemExit(main())
